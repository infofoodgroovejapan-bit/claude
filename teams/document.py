"""DocumentAgent — 資料作成チーム (Document Creation Team).

Handles: presentations, proposals, meeting minutes, manuals,
reports, infographics, visual design via Canva.

Available tools: Canva, Gmail, GitHub.
"""
from __future__ import annotations

from tools import canva, gmail, github
from .base import BaseTeamAgent

_SYSTEM_PROMPT = """\
あなたはAI秘書システムの「資料作成チーム」です。
You are the Document Creation Team of an AI secretary system.

## あなたの専門領域 / Your Expertise

- プレゼンテーション資料の作成（Canvaを使用）
- 提案書・企画書のデザイン・レイアウト
- 会議議事録のフォーマット化・整理
- マニュアル・手順書の作成
- 報告書・レポートの作成
- インフォグラフィックの作成
- 会社概要・会社案内の作成
- テンプレートの作成・管理
- 既存資料のリデザイン・改善
- Canvaを使ったビジュアルデザイン全般

## 利用可能なツール / Available Tools

- **Canva**: プレゼン・デザイン資料の作成・編集・エクスポート
- **Gmail**: 資料の共有・送付、完成資料の通知
- **GitHub**: 資料のバージョン管理、ドキュメントの共有

## 行動方針 / Behavior Guidelines

1. 視覚的に分かりやすく、プロフェッショナルな資料を作成する
2. 依頼者の意図やターゲットオーディエンスを把握してデザインを決める
3. Canvaで実際に資料を作成し、完成したら共有・送付する
4. 資料の構成（目次・章立て）を提案してから作成に入る
5. 日本語と英語の両方に対応する
6. 完成資料はGmailで関係者に通知する
7. 重要資料はGitHubでバージョン管理する

タスクを完了したら、作成した資料の内容・ページ数・共有方法を簡潔にまとめて報告してください。
"""

_ALL_TOOLS = (
    canva.TOOL_DEFINITIONS
    + gmail.TOOL_DEFINITIONS
    + github.TOOL_DEFINITIONS
)

_TOOL_MODULES = {
    **{t["name"]: canva for t in canva.TOOL_DEFINITIONS},
    **{t["name"]: gmail for t in gmail.TOOL_DEFINITIONS},
    **{t["name"]: github for t in github.TOOL_DEFINITIONS},
}


class DocumentAgent(BaseTeamAgent):
    team_name = "document"
    team_name_ja = "資料作成"
    system_prompt = _SYSTEM_PROMPT

    def _build_tools(self) -> list[dict]:
        return _ALL_TOOLS

    def _execute_tool(self, tool_name: str, tool_input: dict) -> str:
        module = _TOOL_MODULES.get(tool_name)
        if module is None:
            return f"[Unknown tool: {tool_name}]"
        return module.execute_tool(tool_name, tool_input)
