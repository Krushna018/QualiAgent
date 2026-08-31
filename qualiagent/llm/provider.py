
from __future__ import annotations
import json
import os
import requests

class LLMProvider:
    """
    OpenAI-compatible chat-completions provider.

    Configure:
      QUALIAGENT_LLM_BASE_URL=https://api.openai.com/v1
      QUALIAGENT_LLM_API_KEY=...
      QUALIAGENT_LLM_MODEL=...

    It also works with compatible local endpoints when supplied by the user.
    """

    def __init__(self):
        self.base_url = os.getenv("QUALIAGENT_LLM_BASE_URL")
        self.api_key = os.getenv("QUALIAGENT_LLM_API_KEY")
        self.model = os.getenv("QUALIAGENT_LLM_MODEL")

    @property
    def enabled(self):
        return bool(self.base_url and self.model)

    def complete_json(self, system: str, user: str) -> dict:
        if not self.enabled:
            raise RuntimeError("LLM provider is not configured.")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }
        r = requests.post(
            self.base_url.rstrip("/") + "/chat/completions",
            headers=headers,
            json=payload,
            timeout=90,
        )
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
        return json.loads(content)
