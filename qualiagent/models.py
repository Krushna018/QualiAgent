
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional

@dataclass
class TestCase:
    __test__ = False
    path: str
    name: str
    source: str

@dataclass
class RepositoryArtifact:
    name: str
    files: Dict[str, str]
    tests: List[TestCase]
    github_metadata: Dict[str, object] = field(default_factory=dict)

@dataclass
class Finding:
    repository: str
    path: str
    test_name: str
    issue_type: str
    severity: str
    confidence: float
    evidence: List[str]
    recommendation: str
    source_agent: str

    def asdict(self):
        return asdict(self)

@dataclass
class ReviewDecision:
    accepted: bool
    rationale: str
    confidence: float
