
from __future__ import annotations
import json
from ..llm.provider import LLMProvider

class LLMReasoningAgent:
    """
    Optional single-agent / LLM reasoning path used for experiments.
    The main pipeline remains runnable without network access.
    """
    name = "llm_reasoner"

    def __init__(self, llm=None):
        self.llm = llm or LLMProvider()

    def enabled(self):
        return self.llm.enabled

    def assess(self, test_source: str, repository_context: dict):
        if not self.llm.enabled:
            return None
        system = (
            "Analyze a Python test for software-quality debt. "
            "Return JSON: issue_type, severity, confidence, evidence, recommendation. "
            "Use only concrete evidence in the test."
        )
        user = json.dumps({
            "context": repository_context,
            "test_source": test_source,
        })
        return self.llm.complete_json(system, user)
