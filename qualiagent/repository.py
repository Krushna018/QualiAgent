
from __future__ import annotations
import ast
import json
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse

import requests

from .models import RepositoryArtifact, TestCase


def normalize_repo_url(raw: str) -> str:
    if not raw:
        return ""
    value = raw.strip().rstrip("/")
    if value.startswith("git@github.com:"):
        value = "https://github.com/" + value.split("@github.com:", 1)[1]
    if value.startswith("git@"):
        value = "https://" + value[4:]
    if "github.com" in value and not value.startswith("http"):
        value = "https://" + value.replace("\\", "/")
    parsed = urlparse(value)
    if parsed.scheme in {"http", "https"} and parsed.netloc.endswith("github.com"):
        if parsed.path.endswith(".git"):
            return value
        return value
    return value


def fetch_github_repo_metadata(repo_url: str, github_token: str | None = None) -> dict:
    normalized = normalize_repo_url(repo_url)
    parsed = urlparse(normalized)
    if "github.com" not in parsed.netloc:
        return {"source_url": repo_url, "source": "local"}

    path = parsed.path.strip("/")
    if not path or "/" not in path:
        return {"source_url": repo_url, "source": "github"}
    owner, repo = path.split("/", 1)
    repo = repo.split("/", 1)[0].removesuffix(".git")
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github+json"}
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"
    try:
        response = requests.get(api_url, headers=headers, timeout=20)
        response.raise_for_status()
        payload = response.json()
        return {
            "source": "github",
            "source_url": normalized,
            "owner": payload.get("owner", {}).get("login", owner),
            "repo": payload.get("name", repo),
            "full_name": payload.get("full_name", f"{owner}/{repo}"),
            "default_branch": payload.get("default_branch"),
            "stars": payload.get("stargazers_count", 0),
            "forks": payload.get("forks_count", 0),
            "open_issues": payload.get("open_issues_count", 0),
            "language": payload.get("language"),
            "description": payload.get("description"),
            "html_url": payload.get("html_url", normalized),
        }
    except Exception:
        return {"source": "github", "source_url": normalized, "owner": owner, "repo": repo}


def remove_directory(path: Path):
    if not path.exists():
        return
    for child in path.rglob("*"):
        if child.is_file() or child.is_symlink():
            try:
                child.chmod(0o666)
            except Exception:
                pass
        elif child.is_dir():
            try:
                child.chmod(0o777)
            except Exception:
                pass
    shutil.rmtree(path, onerror=lambda func, p, exc_info: (
        setattr(__import__('os'), 'chmod', lambda x, mode: None),
        __import__('os').chmod(p, 0o777),
        func(p)
    ))


def clone_repository(repo_url: str, target_dir: str | Path) -> Path:
    normalized = normalize_repo_url(repo_url)
    dir_path = Path(target_dir)
    if dir_path.exists():
        remove_directory(dir_path)
    dir_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "--depth", "1", normalized, str(dir_path)], check=True, capture_output=True, text=True)
    return dir_path


def load_local_repository(path: str | Path, source_url: str | None = None, github_token: str | None = None) -> RepositoryArtifact:
    root = Path(path)
    files = {}
    tests = []
    github_metadata = fetch_github_repo_metadata(source_url, github_token) if source_url else {}
    for p in root.rglob("*.py"):
        if any(part.startswith(".") for part in p.parts):
            continue
        try:
            src = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = str(p.relative_to(root))
        files[rel] = src

        if p.name.startswith("test_") or "tests" in p.parts:
            try:
                tree = ast.parse(src)
            except SyntaxError:
                continue
            lines = src.splitlines()
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
                    end = getattr(node, "end_lineno", node.lineno)
                    body = "\n".join(lines[node.lineno-1:end])
                    tests.append(TestCase(rel, node.name, body))
    return RepositoryArtifact(name=root.name, files=files, tests=tests, github_metadata=github_metadata)


def load_metadata(path: str | Path):
    p = Path(path)
    return json.loads(p.read_text()) if p.exists() else {}
