
from __future__ import annotations
import ast
import re
from typing import List, Tuple

WEAK_ASSERT_PATTERNS = [
    r"assert\s+True\b",
    r"assert\s+[^=!\n]+\s+is\s+not\s+None",
]

def weak_assertion(source: str) -> Tuple[bool, list[str]]:
    evidence = []
    for pat in WEAK_ASSERT_PATTERNS:
        if re.search(pat, source):
            evidence.append(f"matched weak assertion pattern: {pat}")
    return bool(evidence), evidence

def duplicate_assertions(source: str) -> Tuple[bool, list[str]]:
    lines = [ln.strip() for ln in source.splitlines() if ln.strip().startswith("assert ")]
    seen, dups = set(), []
    for ln in lines:
        if ln in seen:
            dups.append(ln)
        seen.add(ln)
    return bool(dups), [f"duplicate assertion: {d}" for d in dups[:3]]

def excessive_complexity(source: str) -> Tuple[bool, list[str]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False, []
    branches = sum(isinstance(n, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.Match)) for n in ast.walk(tree))
    return branches >= 6, [f"branching constructs in test: {branches}"] if branches >= 6 else []

def sleep_flakiness(source: str) -> Tuple[bool, list[str]]:
    patterns = ["time.sleep(", "sleep(", "random.random(", "datetime.now(", "time.time("]
    hits = [p for p in patterns if p in source]
    return bool(hits), [f"nondeterministic/time-based call: {h}" for h in hits]

def outdated_dependency(source: str) -> Tuple[bool, list[str]]:
    # Demo-oriented patterns for benchmark fixtures. Real projects can extend this rule set.
    patterns = ["mock.patch", "nose.tools", "pytest.yield_fixture"]
    hits = [p for p in patterns if p in source]
    return bool(hits), [f"legacy testing API: {h}" for h in hits]
