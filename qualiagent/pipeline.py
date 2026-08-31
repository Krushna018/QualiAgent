
from __future__ import annotations
from .agents.repository_context import RepositoryContextAgent
from .agents.static_analysis import StaticAnalysisAgent
from .agents.quality_agent import TestQualityAgent
from .agents.reviewer import ReviewerAgent

class QualiAgentPipeline:
    """Four-agent workflow: context -> static analysis -> test quality -> reviewer."""

    def __init__(self):
        self.context_agent = RepositoryContextAgent()
        self.static_agent = StaticAnalysisAgent()
        self.quality_agent = TestQualityAgent()
        self.reviewer_agent = ReviewerAgent()

    def run(self, artifact):
        context = self.context_agent.analyze(artifact)
        candidates = []
        candidates.extend(self.static_agent.analyze(artifact))
        candidates.extend(self.quality_agent.analyze(artifact, context))

        reviewed = []
        for finding in candidates:
            decision = self.reviewer_agent.review(finding, context)
            if decision.accepted:
                row = finding.asdict()
                row["review_confidence"] = decision.confidence
                row["review_rationale"] = decision.rationale
                reviewed.append(row)

        return {
            "context": context,
            "candidate_findings": [f.asdict() for f in candidates],
            "accepted_findings": reviewed,
        }
