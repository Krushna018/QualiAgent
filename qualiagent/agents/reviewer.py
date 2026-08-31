
from __future__ import annotations
import json
from ..models import ReviewDecision
from ..llm.provider import LLMProvider

class ReviewerAgent:
    name = "reviewer"

    def __init__(self, llm=None):
        self.llm = llm or LLMProvider()

    def review(self, finding, context):
        # Deterministic evidence-aware fallback keeps the project fully runnable offline.
        if not self.llm.enabled:
            evidence_strength = min(1.0, 0.45 + 0.15 * len(finding.evidence))
            accepted = finding.confidence >= 0.75 and len(finding.evidence) > 0
            return ReviewDecision(
                accepted=accepted,
                rationale="Accepted from traceable static/test evidence." if accepted else "Insufficient traceable evidence.",
                confidence=round((finding.confidence + evidence_strength) / 2, 3),
            )

        system = (
            "You are a software-quality reviewer. Return JSON with keys "
            "accepted:boolean, rationale:string, confidence:number. "
            "Reject unsupported claims and reason only from supplied evidence."
        )
        user = json.dumps({
            "finding": finding.asdict(),
            "repository_context": context,
        }, indent=2)
        obj = self.llm.complete_json(system, user)
        return ReviewDecision(
            accepted=bool(obj["accepted"]),
            rationale=str(obj["rationale"]),
            confidence=float(obj["confidence"]),
        )
