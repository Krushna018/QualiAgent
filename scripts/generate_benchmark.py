
from pathlib import Path
import random
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

ISSUES = [
    "weak_assertion",
    "redundant_assertion",
    "flaky_test_indicator",
    "excessive_test_complexity",
    "outdated_test_dependency",
    "missing_oracle",
]

TEMPLATES = {
    "weak_assertion": """def test_value_{i}():\n    value = {i}\n    assert value is not None\n""",
    "redundant_assertion": """def test_value_{i}():\n    value = {i}\n    assert value >= 0\n    assert value >= 0\n""",
    "flaky_test_indicator": """def test_value_{i}():\n    import time\n    time.sleep(0.01)\n    value = {i}\n    assert value >= 0\n""",
    "excessive_test_complexity": """def test_value_{i}():\n    x={i}\n    if x>=0:\n        if x>=0:\n            if x>=0:\n                if x>=0:\n                    if x>=0:\n                        if x>=0:\n                            assert x>=0\n""",
    "outdated_test_dependency": """def test_value_{i}():\n    import mock\n    with mock.patch("builtins.print"):\n        assert {i} >= 0\n""",
    "missing_oracle": """def test_value_{i}():\n    value = {i} * 2\n    str(value)\n""",
}

def main():
    random.seed(42)
    bench = ROOT/"data"/"benchmark_repos"
    if bench.exists():
        import shutil
        shutil.rmtree(bench)
    bench.mkdir(parents=True)

    manifest = []
    # 30 repositories × 50 tests = exactly 1,500 generated benchmark test cases.
    for r in range(30):
        repo = bench/f"repo_{r:02d}"
        tests = repo/"tests"
        tests.mkdir(parents=True)
        for i in range(50):
            issue = ISSUES[(r*50+i) % len(ISSUES)]
            src = TEMPLATES[issue].format(i=i)
            path = tests/f"test_case_{i:03d}.py"
            path.write_text(src)
            manifest.append({
                "repository": repo.name,
                "path": str(path.relative_to(repo)),
                "test_name": f"test_value_{i}",
                "label": issue,
            })

    (ROOT/"data"/"benchmark_manifest.json").write_text(json.dumps(manifest, indent=2))
    print("Repositories:", 30)
    print("Generated benchmark test cases:", len(manifest))
    print("Manifest:", ROOT/"data"/"benchmark_manifest.json")

if __name__ == "__main__":
    main()
