"""Pydantic models for the AI Secretary System."""
from pydantic import BaseModel


class ClassificationResult(BaseModel):
    team: str
    """Which team should handle this task.
    One of: 'marketing', 'planning', 'accounting', 'document', 'secretary'
    Use 'secretary' when the task does not clearly belong to any specialist team.
    """
    confidence: float
    """Confidence score between 0.0 and 1.0."""
    reasoning: str
    """Brief explanation of why this team was chosen (in the same language as the input)."""
    language: str
    """Detected language of the input: 'ja' for Japanese, 'en' for English, or ISO code."""


class AgentResponse(BaseModel):
    response_text: str
    """The final response to be shown to the user."""
    team_name: str
    """English team identifier, e.g. 'marketing'."""
    team_name_ja: str
    """Japanese team name, e.g. 'マーケティング'."""
    tools_used: list[str]
    """List of tool names that were called during handling."""
