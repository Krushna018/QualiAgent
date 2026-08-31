
from __future__ import annotations
from ..models import Finding
from ..rules.static_rules import (
    weak_assertion, duplicate_assertions, excessive_complexity,
    sleep_flakiness, outdated_dependency
)

class StaticAnalysisAgent:
    name = "static_analysis"

    def __init__(self):
        self.checks = [
            ("weak_assertion", "medium", weak_assertion,
             "Replace weak assertions with behavior-specific expectations."),
            ("redundant_assertion", "low", duplicate_assertions,
             "Remove redundant checks or consolidate test intent."),
            ("excessive_test_complexity", "medium", excessive_complexity,
             "Split complex test logic into focused cases and helpers."),
            ("flaky_test_indicator", "high", sleep_flakiness,
             "Replace timing/nondeterministic behavior with deterministic fixtures or controlled clocks."),
            ("outdated_test_dependency", "medium", outdated_dependency,
             "Migrate legacy testing APIs to supported equivalents."),
        ]

    def analyze(self, artifact):
        findings = []
        for tc in artifact.tests:
            for issue_type, severity, fn, rec in self.checks:
                matched, evidence = fn(tc.source)
                if matched:
                    findings.append(Finding(
                        repository=artifact.name,
                        path=tc.path,
                        test_name=tc.name,
                        issue_type=issue_type,
                        severity=severity,
                        confidence=0.88,
                        evidence=evidence,
                        recommendation=rec,
                        source_agent=self.name,
                    ))
        return findings
