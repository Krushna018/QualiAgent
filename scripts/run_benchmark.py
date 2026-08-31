
from pathlib import Path
import sys, json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from qualiagent.repository import load_local_repository
from qualiagent.pipeline import QualiAgentPipeline


def main():
    bench = ROOT / "data" / "benchmark_repos"
    if not bench.exists():
        print("Benchmark not found. Run: python scripts/generate_benchmark.py")
        raise SystemExit(1)

    pipeline = QualiAgentPipeline()
    rows = []
    repo_provenance = []
    for repo in sorted(bench.iterdir()):
        if not repo.is_dir():
            continue
        artifact = load_local_repository(repo)
        result = pipeline.run(artifact)
        rows.extend(result["accepted_findings"])
        repo_provenance.append({
            "repository": artifact.name,
            "source": "synthetic_benchmark",
            "test_count": len(artifact.tests),
            "file_count": len(artifact.files),
            "github_metadata": artifact.github_metadata,
        })

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(out / "multi_agent_findings.csv", index=False)
    pd.DataFrame(repo_provenance).to_csv(out / "benchmark_provenance.csv", index=False)
    print("Repositories analyzed:", len(list(bench.iterdir())))
    print("Accepted findings:", len(df))
    print("Saved:", out / "multi_agent_findings.csv")
    print("Saved provenance:", out / "benchmark_provenance.csv")


if __name__ == "__main__":
    main()
