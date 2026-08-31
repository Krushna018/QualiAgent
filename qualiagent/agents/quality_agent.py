
from __future__ import annotations
import ast
from ..models import Finding

class TestQualityAgent:
    name = "test_quality"

    def analyze(self, artifact, context):
        findings = []
        for tc in artifact.tests:
            try:
                tree = ast.parse(tc.source)
            except SyntaxError:
                continue

            asserts = sum(isinstance(n, ast.Assert) for n in ast.walk(tree))
            calls = sum(isinstance(n, ast.Call) for n in ast.walk(tree))

            if asserts == 0 and "pytest.raises" not in tc.source:
                findings.append(Finding(
                    repository=artifact.name,
                    path=tc.path,
                    test_name=tc.name,
                    issue_type="missing_oracle",
                    severity="high",
                    confidence=0.84,
                    evidence=[f"assert_count={asserts}", f"call_count={calls}"],
                    recommendation="Add an explicit behavioral oracle or exception expectation.",
                    source_agent=self.name,
                ))

            if len(tc.source.splitlines()) > 45:
                findings.append(Finding(
                    repository=artifact.name,
                    path=tc.path,
                    test_name=tc.name,
                    issue_type="oversized_test",
                    severity="medium",
                    confidence=0.80,
                    evidence=[f"test_length={len(tc.source.splitlines())} lines"],
                    recommendation="Decompose the test into smaller behavior-focused cases.",
                    source_agent=self.name,
                ))
        return findings
