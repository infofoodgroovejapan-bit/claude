"""Task classifier for the AI Secretary System.

Uses claude-haiku-4-5 with prompt caching to cheaply and quickly
determine which specialist team should handle an incoming task.
"""
import json
import os

import anthropic

from .models import ClassificationResult
from .prompts import CLASSIFIER_SYSTEM_PROMPT

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    return _client


def classify(task_text: str) -> ClassificationResult:
    """Classify a task and return which team should handle it.

    Uses claude-haiku-4-5 for speed and cost-efficiency.
    The system prompt is cached after the first call.
    """
    client = _get_client()

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=[
            {
                "type": "text",
                "text": CLASSIFIER_SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": task_text,
            }
        ],
    )

    raw_text = response.content[0].text.strip()

    # Strip markdown code fences if the model added them
    if raw_text.startswith("```"):
        lines = raw_text.splitlines()
        raw_text = "\n".join(
            line for line in lines if not line.startswith("```")
        ).strip()

    data = json.loads(raw_text)
    return ClassificationResult(**data)
