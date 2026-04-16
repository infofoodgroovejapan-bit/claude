"""PlanningAgent — 企画チーム (Planning Team).

Handles: project planning, business strategy, OKR/KPI management,
meeting scheduling, roadmaps, risk analysis.

Available tools: Gmail, Google Calendar, Zoom, GitHub.
"""
from __future__ import annotations

from tools import gmail, calendar, zoom, github
from .base import BaseTeamAgent

_SYSTEM_PROMPT = """\
あなたはAI秘書システムの「企画チーム」です。
You are the Planning Team of an AI secretary system.

## あなたの専門領域 / Your Expertise

- 新規プロジェクトの企画立案・プロジェクト憲章の作成
- 事業計画書・ビジネスプランの策定
- プロジェクト管理（スケジュール、マイルストーン、リスク管理）
- 製品開発ロードマップの策定
- ビジネス戦略・競争戦略の立案
- KPI設定とOKR管理
- ステークホルダーとの会議設定・アジェンダ作成
- リスク分析と対策立案
- チームへのタスク割り振り・進捗管理
- 会議アジェンダの作成・議事録管理

## 利用可能なツール / Available Tools

- **Gmail**: プロジェクト関係者への連絡、報告メール
- **Google Calendar**: プロジェクト会議・マイルストーン・締め切りの設定
- **Zoom**: プロジェクト会議・ステークホルダーミーティングの設定
- **GitHub**: プロジェクトのIssue管理、タスクトラッキング、ドキュメント管理

## 行動方針 / Behavior Guidelines

1. プロジェクトの全体像を把握し、構造的かつ論理的に対応する
2. 必要なツールを使って実際のスケジュール設定やタスク作成を行う
3. リスクと対策を常に念頭に置いて提案する
4. 期日・担当者・成果物を明確にする
5. 日本語と英語の両方に対応する
6. 会議が必要な場合はGoogleカレンダーに設定し、ZoomのURLも追加する
7. タスク管理が必要な場合はGitHub Issueとして登録する

タスクを完了したら、実施した内容を簡潔にまとめて報告してください。
"""

_ALL_TOOLS = (
    gmail.TOOL_DEFINITIONS
    + calendar.TOOL_DEFINITIONS
    + zoom.TOOL_DEFINITIONS
    + github.TOOL_DEFINITIONS
)

_TOOL_MODULES = {
    **{t["name"]: gmail for t in gmail.TOOL_DEFINITIONS},
    **{t["name"]: calendar for t in calendar.TOOL_DEFINITIONS},
    **{t["name"]: zoom for t in zoom.TOOL_DEFINITIONS},
    **{t["name"]: github for t in github.TOOL_DEFINITIONS},
}


class PlanningAgent(BaseTeamAgent):
    team_name = "planning"
    team_name_ja = "企画"
    system_prompt = _SYSTEM_PROMPT

    def _build_tools(self) -> list[dict]:
        return _ALL_TOOLS

    def _execute_tool(self, tool_name: str, tool_input: dict) -> str:
        module = _TOOL_MODULES.get(tool_name)
        if module is None:
            return f"[Unknown tool: {tool_name}]"
        return module.execute_tool(tool_name, tool_input)
