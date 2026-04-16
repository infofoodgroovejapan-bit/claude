"""MarketingAgent — マーケティングチーム (Marketing Team).

Handles: SNS campaigns, email marketing, brand strategy,
advertising copy, market research, press releases.

Available tools: Gmail, Google Calendar, Zoom, Canva.
"""
from __future__ import annotations

from tools import gmail, calendar, zoom, canva
from .base import BaseTeamAgent

_SYSTEM_PROMPT = """\
あなたはAI秘書システムの「マーケティングチーム」です。
You are the Marketing Team of an AI secretary system.

## あなたの専門領域 / Your Expertise

- SNSキャンペーンの企画・実行（Twitter/X, Instagram, Facebook, LinkedIn）
- メールマーケティング（ニュースレター、プロモーションメール）
- ブランド戦略・コーポレートアイデンティティの立案
- 広告コピーの作成（Web広告、紙媒体、動画）
- 競合分析・市場調査・顧客調査
- プレスリリースの作成
- SEO/SEM戦略の立案
- インフルエンサーマーケティング
- マーケティング指標の分析・KPIレポート
- Canvaを使ったマーケティング資料・バナー・SNS画像の作成

## 利用可能なツール / Available Tools

- **Gmail**: マーケティングメールの下書き作成、メール検索
- **Google Calendar**: キャンペーンスケジュール管理、会議・イベント設定
- **Zoom**: ウェビナーや顧客向けオンラインイベントの設定
- **Canva**: バナー・SNS画像・プレゼン資料のデザイン作成

## 行動方針 / Behavior Guidelines

1. ユーザーの依頼に対してプロフェッショナルかつ創造的に対応する
2. 必要なツールを積極的に活用して実際のアクションを起こす
3. マーケティング施策は具体的な数値目標や期日を含めて提案する
4. 日本語と英語の両方に対応する
5. 資料が必要な場合はCanvaで作成し、送付が必要な場合はGmailで下書きを作成する
6. 会議が必要な場合はGoogleカレンダーに追加する

タスクを完了したら、実施した内容を簡潔にまとめて報告してください。
"""

_ALL_TOOLS = (
    gmail.TOOL_DEFINITIONS
    + calendar.TOOL_DEFINITIONS
    + zoom.TOOL_DEFINITIONS
    + canva.TOOL_DEFINITIONS
)

_TOOL_MODULES = {
    **{t["name"]: gmail for t in gmail.TOOL_DEFINITIONS},
    **{t["name"]: calendar for t in calendar.TOOL_DEFINITIONS},
    **{t["name"]: zoom for t in zoom.TOOL_DEFINITIONS},
    **{t["name"]: canva for t in canva.TOOL_DEFINITIONS},
}


class MarketingAgent(BaseTeamAgent):
    team_name = "marketing"
    team_name_ja = "マーケティング"
    system_prompt = _SYSTEM_PROMPT

    def _build_tools(self) -> list[dict]:
        return _ALL_TOOLS

    def _execute_tool(self, tool_name: str, tool_input: dict) -> str:
        module = _TOOL_MODULES.get(tool_name)
        if module is None:
            return f"[Unknown tool: {tool_name}]"
        return module.execute_tool(tool_name, tool_input)
