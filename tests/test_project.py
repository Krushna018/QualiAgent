
from pathlib import Path
import sys, tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from qualiagent.repository import load_local_repository, normalize_repo_url
from qualiagent.pipeline import QualiAgentPipeline
from qualiagent.models import RepositoryArtifact, TestCase
from qualiagent.agents.static_analysis import StaticAnalysisAgent

def test_static_agent_detects_weak_assertion():
    art = RepositoryArtifact(
        name="demo",
        files={},
        tests=[TestCase("tests/test_x.py","test_x","def test_x():\n    x=1\n    assert x is not None\n")]
    )
    fs = StaticAnalysisAgent().analyze(art)
    assert any(f.issue_type == "weak_assertion" for f in fs)

def test_pipeline_has_four_agent_stages():
    p = QualiAgentPipeline()
    assert p.context_agent.name == "repository_context"
    assert p.static_agent.name == "static_analysis"
    assert p.quality_agent.name == "test_quality"
    assert p.reviewer_agent.name == "reviewer"

def test_local_repository_loader_extracts_tests(tmp_path):
    (tmp_path/"tests").mkdir()
    (tmp_path/"tests"/"test_a.py").write_text("def test_a():\n    assert 1 == 1\n")
    art = load_local_repository(tmp_path)
    assert len(art.tests) == 1
    assert art.tests[0].name == "test_a"

def test_offline_pipeline_is_runnable():
    art = RepositoryArtifact(
        name="demo",
        files={"tests/test_x.py":"def test_x():\n    assert True\n"},
        tests=[TestCase("tests/test_x.py","test_x","def test_x():\n    assert True\n")]
    )
    out = QualiAgentPipeline().run(art)
    assert "accepted_findings" in out
    assert len(out["accepted_findings"]) >= 1


def test_normalize_repo_url_handles_github_https_and_ssh_forms():
    assert normalize_repo_url("https://github.com/org/repo.git") == "https://github.com/org/repo.git"
    assert normalize_repo_url("git@github.com:org/repo.git") == "https://github.com/org/repo.git"
    assert normalize_repo_url("github.com/org/repo") == "https://github.com/org/repo"
