"""AccountingAgent — 経理チーム (Accounting Team).

Handles: expense reports, financial reports, invoices,
budget management, tax preparation.

Available tools: Gmail, GitHub.
"""
from __future__ import annotations

from tools import gmail, github
from .base import BaseTeamAgent

_SYSTEM_PROMPT = """\
あなたはAI秘書システムの「経理チーム」です。
You are the Accounting Team of an AI secretary system.

## あなたの専門領域 / Your Expertise

- 経費精算の処理・確認・承認フロー管理
- 月次・四半期・年次財務レポートの作成
- 請求書の管理・発行・送付
- 予算管理・コスト分析・予実対比
- 税務申告の準備・サポート
- 給与計算のサポート
- 財務予測・キャッシュフロー管理
- 仕訳・勘定科目管理
- 監査対応・内部統制
- 経費承認フローの管理

## 利用可能なツール / Available Tools

- **Gmail**: 財務レポートの送付、請求書の送受信、経費承認メール
- **GitHub**: 財務データ・レポートのバージョン管理、経費追跡Issue

## 行動方針 / Behavior Guidelines

1. 正確さと整合性を最優先に対応する
2. 金額・日付・勘定科目を常に明確に記載する
3. 財務データの機密性に配慮する
4. 法的・会計的な観点からのリスクを積極的に指摘する
5. 日本語と英語の両方に対応する
6. レポートや請求書はGmailで下書きを作成する
7. 追跡が必要なタスクはGitHub Issueとして登録する

タスクを完了したら、実施した内容（金額・日付・担当者等）を簡潔にまとめて報告してください。
"""

_ALL_TOOLS = gmail.TOOL_DEFINITIONS + github.TOOL_DEFINITIONS

_TOOL_MODULES = {
    **{t["name"]: gmail for t in gmail.TOOL_DEFINITIONS},
    **{t["name"]: github for t in github.TOOL_DEFINITIONS},
}


class AccountingAgent(BaseTeamAgent):
    team_name = "accounting"
    team_name_ja = "経理"
    system_prompt = _SYSTEM_PROMPT

    def _build_tools(self) -> list[dict]:
        return _ALL_TOOLS

    def _execute_tool(self, tool_name: str, tool_input: dict) -> str:
        module = _TOOL_MODULES.get(tool_name)
        if module is None:
            return f"[Unknown tool: {tool_name}]"
        return module.execute_tool(tool_name, tool_input)
