
from pathlib import Path
import sys, json

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from qualiagent.repository import load_local_repository
from qualiagent.pipeline import QualiAgentPipeline

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/analyze_repository.py /path/to/python/repository")
        raise SystemExit(2)
    artifact = load_local_repository(sys.argv[1])
    result = QualiAgentPipeline().run(artifact)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
