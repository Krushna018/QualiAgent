from __future__ import annotations

import csv
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from qualiagent.pipeline import QualiAgentPipeline
from qualiagent.repository import clone_repository, load_local_repository


def read_repo_urls(path: str | Path | None = None):
    if path is not None:
        file_path = Path(path)
        with file_path.open("r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    default = ROOT / "data" / "public_repo_list.txt"
    if default.exists():
        with default.open("r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
    return []


def main():
    if len(sys.argv) > 2:
        print("Usage: python scripts/analyze_public_repositories.py [path/to/repo_list.txt]")
        raise SystemExit(2)

    repo_urls = read_repo_urls(sys.argv[1] if len(sys.argv) == 2 else None)
    if not repo_urls:
        print("No GitHub repositories supplied. Add a repo list file or pass one path.")
        raise SystemExit(1)

    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)

    all_rows = []
    provenance_rows = []
    pipeline = QualiAgentPipeline()

    processed = 0
    failed = 0
    for index, url in enumerate(repo_urls, start=1):
        target_dir = ROOT / "data" / "public_repos" / f"repo_{index:02d}"
        try:
            repo_dir = clone_repository(url, target_dir)
        except Exception as exc:
            failed += 1
            print(f"[{index}/{len(repo_urls)}] FAILED {url}: {exc}")
            continue

        artifact = load_local_repository(repo_dir, source_url=url)
        result = pipeline.run(artifact)
        for finding in result["accepted_findings"]:
            row = dict(finding)
            row["repository_url"] = url
            row["source"] = "public_github"
            all_rows.append(row)

        provenance_rows.append({
            "repository": artifact.name,
            "repository_url": url,
            "source": "public_github",
            "test_count": len(artifact.tests),
            "file_count": len(artifact.files),
            "github_metadata": json_dumps(artifact.github_metadata),
        })

        processed += 1
        print(f"[{index}/{len(repo_urls)}] {url} -> {len(result['accepted_findings'])} accepted findings")

    print(f"Processed repositories: {processed}")
    print(f"Failed repositories: {failed}")

    findings_df = pd.DataFrame(all_rows)
    findings_df.to_csv(out_dir / "public_repo_findings.csv", index=False)
    pd.DataFrame(provenance_rows).to_csv(out_dir / "public_repo_provenance.csv", index=False)

    print(f"Saved findings: {out_dir / 'public_repo_findings.csv'}")
    print(f"Saved provenance: {out_dir / 'public_repo_provenance.csv'}")


def json_dumps(value):
    return __import__("json").dumps(value, default=str)


if __name__ == "__main__":
    main()
