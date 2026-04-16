"""BaseTeamAgent — shared agentic tool loop for all specialist teams.

All team agents inherit from this class.  The core agentic loop
(send → tool_use → execute → repeat → end_turn) lives here so
individual team modules stay thin.
"""
from __future__ import annotations

import os
from abc import ABC, abstractmethod

import anthropic

from secretary.models import AgentResponse, ClassificationResult

_MODEL = "claude-sonnet-4-6"
_MAX_ITERATIONS = 10


class BaseTeamAgent(ABC):
    """Abstract base class for all specialist team agents."""

    team_name: str = ""
    team_name_ja: str = ""
    system_prompt: str = ""
    available_tools: list[dict] = []

    # Maps tool name -> executor module (set in subclass __init__)
    _tool_executors: dict  # {tool_name: callable(name, input) -> str}

    def __init__(self) -> None:
        self._tool_executors = {}
        self._client: anthropic.Anthropic | None = None

    def _get_client(self) -> anthropic.Anthropic:
        if self._client is None:
            self._client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        return self._client

    @abstractmethod
    def _build_tools(self) -> list[dict]:
        """Return the list of Anthropic tool definitions for this team."""
        ...

    @abstractmethod
    def _execute_tool(self, tool_name: str, tool_input: dict) -> str:
        """Execute a tool call and return the result as a string."""
        ...

    def handle(self, task_text: str, context: dict | None = None) -> AgentResponse:
        """Entry point called by SecretaryAgent.

        Runs the agentic loop and returns an AgentResponse.
        """
        classification: ClassificationResult | None = (
            context.get("classification") if context else None
        )

        system = [
            {
                "type": "text",
                "text": self.system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ]

        messages: list[dict] = [{"role": "user", "content": task_text}]
        tools = self._build_tools()
        tools_used: list[str] = []

        final_response = self._run_tool_loop(messages, tools, system, tools_used)

        # Extract text from final response
        response_text = ""
        for block in final_response.content:
            if hasattr(block, "text"):
                response_text = block.text
                break

        return AgentResponse(
            response_text=response_text,
            team_name=self.team_name,
            team_name_ja=self.team_name_ja,
            tools_used=tools_used,
        )

    def _run_tool_loop(
        self,
        messages: list[dict],
        tools: list[dict],
        system: list[dict],
        tools_used: list[str],
    ) -> anthropic.types.Message:
        """Core agentic loop. Mutates messages and tools_used in place."""
        client = self._get_client()

        for _ in range(_MAX_ITERATIONS):
            kwargs: dict = {
                "model": _MODEL,
                "max_tokens": 8096,
                "system": system,
                "messages": messages,
            }
            if tools:
                kwargs["tools"] = tools

            response = client.messages.create(**kwargs)

            if response.stop_reason == "end_turn":
                return response

            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})
                tool_results = []

                for block in response.content:
                    if block.type == "tool_use":
                        tools_used.append(block.name)
                        result = self._execute_tool(block.name, block.input)
                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result,
                            }
                        )

                messages.append({"role": "user", "content": tool_results})
                continue

            # Any other stop reason (e.g. max_tokens): return what we have
            return response

        return response  # type: ignore[return-value]
