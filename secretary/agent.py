"""SecretaryAgent — the main orchestrator of the AI Secretary System.

Receives tasks, classifies them via the classifier, then delegates
to the appropriate specialist team agent.
"""
from __future__ import annotations

from .classifier import classify
from .models import AgentResponse, ClassificationResult
from .prompts import SECRETARY_SYSTEM_PROMPT


# Team registry is populated lazily on first access to avoid circular imports
# and to keep startup fast. Each team agent is a singleton.
_TEAM_REGISTRY: dict | None = None


def _get_team_registry() -> dict:
    global _TEAM_REGISTRY
    if _TEAM_REGISTRY is None:
        from teams.marketing import MarketingAgent
        from teams.planning import PlanningAgent
        from teams.accounting import AccountingAgent
        from teams.document import DocumentAgent
        from teams.wellbeing import WellbeingAgent

        _TEAM_REGISTRY = {
            "marketing": MarketingAgent(),
            "planning": PlanningAgent(),
            "accounting": AccountingAgent(),
            "document": DocumentAgent(),
            "wellbeing": WellbeingAgent(),
        }
    return _TEAM_REGISTRY


class SecretaryAgent:
    """Top-level orchestrator. Classifies tasks and delegates to team agents."""

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose

    def handle_task(
        self,
        task_text: str,
        pdf_paths: list[str] | None = None,
    ) -> AgentResponse:
        """Classify and delegate a task, returning the final AgentResponse."""
        if self.verbose:
            print("[秘書] タスクを受信しました。分類中...")

        classification = classify(task_text)

        if self.verbose:
            print(
                f"[秘書] 分類結果: {classification.team} "
                f"(信頼度: {classification.confidence:.0%})\n"
                f"[秘書] 理由: {classification.reasoning}"
            )
            if pdf_paths:
                print(f"[秘書] 添付PDF: {', '.join(pdf_paths)}")

        registry = _get_team_registry()

        if classification.team in registry:
            team_agent = registry[classification.team]
            return team_agent.handle(
                task_text,
                context={"classification": classification},
                pdf_paths=pdf_paths,
            )

        # Fallback: secretary handles it directly
        return self._handle_directly(task_text, classification)

    def _handle_directly(
        self, task_text: str, classification: ClassificationResult
    ) -> AgentResponse:
        """Handle a task directly when no specialist team is assigned."""
        import os
        import anthropic

        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=[
                {
                    "type": "text",
                    "text": SECRETARY_SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": task_text}],
        )

        return AgentResponse(
            response_text=response.content[0].text,
            team_name="secretary",
            team_name_ja="秘書",
            tools_used=[],
        )
