"""note monetization toolkit.

note.com には記事投稿用の公開APIが無いため、このモジュールは実際の投稿を
自動化するのではなく、収益化に必要な「型」を自動で組み立てるロジックを
提供します（すべてローカル計算で完結し、外部MCP接続を必要としません）。

生成した本文は Team エージェントが `github_create_or_update_file` で
リポジトリの `content/note/` 配下に保存し、担当者がそれを note のエディタに
貼り付けて公開する運用を想定しています。

収益源として以下の3つを組み合わせます:
  1. 有料記事（一部無料 + 続きは有料）
  2. アフィリエイトリンク（PR表記つき）
  3. メンバーシップ／サポートへの導線
"""
from __future__ import annotations

import datetime as _dt

PAYWALL_MARKER = (
    "<!-- NOTE_PAYWALL_HERE: ここで note エディタの"
    "「ここから先を有料にする」機能を使ってください -->"
)

# フードウェルビーイング領域でよく使うアフィリエイトカテゴリ。
# URLはプレースホルダーなので、実際のアソシエイトID/アフィリエイトIDに
# 差し替えて使用してください。
_AFFILIATE_CATALOG: dict[str, dict] = {
    "supplement": {
        "label": "サプリメント・プロテイン",
        "items": [
            {"name": "ホエイプロテイン（無添加）", "url": "https://www.amazon.co.jp/dp/PLACEHOLDER?tag=YOUR_ASSOCIATE_ID"},
            {"name": "マルチビタミン&ミネラル", "url": "https://hb.afl.rakuten.co.jp/hgc/PLACEHOLDER"},
        ],
    },
    "kitchen_tool": {
        "label": "調理器具・キッチン家電",
        "items": [
            {"name": "デジタルキッチンスケール", "url": "https://www.amazon.co.jp/dp/PLACEHOLDER?tag=YOUR_ASSOCIATE_ID"},
            {"name": "低温調理器", "url": "https://hb.afl.rakuten.co.jp/hgc/PLACEHOLDER"},
        ],
    },
    "fermented_food": {
        "label": "発酵食品・腸活",
        "items": [
            {"name": "生きた乳酸菌ヨーグルトメーカー", "url": "https://www.amazon.co.jp/dp/PLACEHOLDER?tag=YOUR_ASSOCIATE_ID"},
            {"name": "無添加味噌・塩麹セット", "url": "https://hb.afl.rakuten.co.jp/hgc/PLACEHOLDER"},
        ],
    },
    "book": {
        "label": "書籍・レシピ本",
        "items": [
            {"name": "栄養学の入門書", "url": "https://www.amazon.co.jp/dp/PLACEHOLDER?tag=YOUR_ASSOCIATE_ID"},
        ],
    },
    "meal_kit": {
        "label": "ミールキット・食材宅配",
        "items": [
            {"name": "無添加ミールキット定期便", "url": "https://px.a8.net/svt/ejp?a8mat=PLACEHOLDER"},
        ],
    },
}

_DISCLOSURE_TEXT = (
    "※本記事にはアフィリエイト広告（PR）を含みます。"
    "紹介する商品から得た収益の一部は、当メディアの運営費に充てられます。"
)

_PRICING_TIERS = {
    "standard": {"min_yen": 300, "max_yen": 300, "word_count": (1200, 2200)},
    "deep_dive": {"min_yen": 500, "max_yen": 780, "word_count": (2200, 3500)},
    "premium": {"min_yen": 980, "max_yen": 1500, "word_count": (3500, 999999)},
}


TOOL_DEFINITIONS: list[dict] = [
    {
        "name": "note_suggest_pricing",
        "description": (
            "note有料記事の価格帯を提案します / Suggest a price tier for a note paid article.\n"
            "本文の文字数と内容の深さから、300〜1500円の価格帯とその理由を返します。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "word_count": {
                    "type": "integer",
                    "description": "本文全体（無料部分＋有料部分）のおおよその文字数",
                },
                "depth": {
                    "type": "string",
                    "enum": ["standard", "deep_dive", "premium"],
                    "description": (
                        "standard=一般的なまとめ記事, "
                        "deep_dive=独自調査・データ・実践レシピ付き, "
                        "premium=個別プラン・限定コンテンツ・特典付き"
                    ),
                },
            },
            "required": ["word_count", "depth"],
        },
    },
    {
        "name": "note_get_affiliate_links",
        "description": (
            "フードウェルビーイング関連のアフィリエイトリンク候補を取得します / "
            "Get candidate affiliate links for a food-wellbeing content category.\n"
            "PR表記（景品表示法対応）付きで返します。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": list(_AFFILIATE_CATALOG.keys()),
                    "description": "紹介したい商品カテゴリ",
                },
            },
            "required": ["category"],
        },
    },
    {
        "name": "note_format_paid_article",
        "description": (
            "note投稿用に、無料部分＋有料部分＋アフィリエイト＋メンバーシップ導線を"
            "組み合わせた完成原稿を組み立てます / "
            "Assemble a complete note draft with free preview, paywall marker, "
            "paid body, affiliate section, and membership CTA."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "記事タイトル"},
                "free_intro": {
                    "type": "string",
                    "description": "無料公開する導入部分（フックとなる内容、続きが気になる形で終える）",
                },
                "paid_body": {
                    "type": "string",
                    "description": "有料部分の本文（具体的な実践方法・データ・レシピなど）",
                },
                "price_yen": {"type": "integer", "description": "note_suggest_pricingで決めた価格（円）"},
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "noteのハッシュタグ（例: フードウェルビーイング, 腸活, 食習慣）",
                },
                "affiliate_category": {
                    "type": "string",
                    "enum": list(_AFFILIATE_CATALOG.keys()) + ["none"],
                    "description": "本文末に挿入するアフィリエイトカテゴリ。不要な場合は 'none'",
                },
                "include_membership_cta": {
                    "type": "boolean",
                    "description": "note メンバーシップ／サポートへの導線を末尾に入れるか",
                    "default": True,
                },
            },
            "required": ["title", "free_intro", "paid_body", "price_yen", "tags"],
        },
    },
    {
        "name": "note_build_ledger_row",
        "description": (
            "収益台帳（CSV）に追記する1行を組み立てます / "
            "Build one CSV row to append to the revenue ledger.\n"
            "github_get_file_contents で既存台帳を読み、この行を追加してから "
            "github_create_or_update_file で書き戻してください。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "article_title": {"type": "string"},
                "category": {"type": "string", "description": "例: 有料記事 / アフィリエイト / メンバーシップ"},
                "price_yen": {"type": "integer"},
                "note_memo": {"type": "string", "description": "補足メモ（任意）"},
            },
            "required": ["article_title", "category", "price_yen"],
        },
    },
]


def _suggest_pricing(word_count: int, depth: str) -> str:
    tier = _PRICING_TIERS.get(depth, _PRICING_TIERS["standard"])
    lo, hi = tier["word_count"]
    price = tier["min_yen"] if depth != "deep_dive" else round((tier["min_yen"] + tier["max_yen"]) / 2)

    reasoning = []
    if word_count < lo:
        reasoning.append(
            f"文字数（約{word_count}字）が{depth}の目安（{lo}〜{hi}字）よりやや少ないため、"
            "無料部分を増やすか本文を充実させることを検討してください。"
        )
    fit = "適合" if lo <= word_count <= hi else "要調整"

    return (
        f"提案価格: {price}円 (帯: {tier['min_yen']}〜{tier['max_yen']}円)\n"
        f"想定文字数レンジ: {lo}〜{hi}字 / 実際の文字数: 約{word_count}字 [{fit}]\n"
        + ("\n".join(reasoning) if reasoning else "文字数と深さのバランスは目安の範囲内です。")
    )


def _get_affiliate_links(category: str) -> str:
    entry = _AFFILIATE_CATALOG.get(category)
    if entry is None:
        return f"[Unknown affiliate category: {category}]"

    lines = [f"## 関連商品（{entry['label']}）", ""]
    for item in entry["items"]:
        lines.append(f"- [{item['name']}]({item['url']})")
    lines.append("")
    lines.append(_DISCLOSURE_TEXT)
    return "\n".join(lines)


def _format_paid_article(tool_input: dict) -> str:
    title = tool_input["title"]
    free_intro = tool_input["free_intro"]
    paid_body = tool_input["paid_body"]
    price_yen = tool_input["price_yen"]
    tags = tool_input.get("tags", [])
    affiliate_category = tool_input.get("affiliate_category", "none")
    include_membership_cta = tool_input.get("include_membership_cta", True)

    parts = [
        f"# {title}",
        "",
        free_intro.strip(),
        "",
        PAYWALL_MARKER,
        f"（この記事は有料設定を想定しています。参考価格: {price_yen}円）",
        "",
        paid_body.strip(),
        "",
    ]

    if affiliate_category and affiliate_category != "none":
        parts.append(_get_affiliate_links(affiliate_category))
        parts.append("")

    if include_membership_cta:
        parts.append(
            "---\n"
            "この記事が役に立ったら、サポート機能でのご支援や、"
            "フードウェルビーイング メンバーシップ（サークル）へのご参加もお待ちしています。"
            "限定コンテンツや個別相談を継続的にお届けします。"
        )
        parts.append("")

    if tags:
        parts.append(" ".join(f"#{t}" for t in tags))

    return "\n".join(parts)


def _build_ledger_row(tool_input: dict) -> str:
    date_str = _dt.date.today().isoformat()
    title = tool_input["article_title"].replace(",", "、")
    category = tool_input["category"].replace(",", "、")
    price = tool_input["price_yen"]
    memo = tool_input.get("note_memo", "").replace(",", "、")
    return f"{date_str},{title},{category},{price},{memo}"


def execute_tool(name: str, tool_input: dict) -> str:
    """Dispatch note monetization helper calls. Pure local logic, no MCP needed."""
    if name == "note_suggest_pricing":
        return _suggest_pricing(tool_input["word_count"], tool_input["depth"])

    if name == "note_get_affiliate_links":
        return _get_affiliate_links(tool_input["category"])

    if name == "note_format_paid_article":
        return _format_paid_article(tool_input)

    if name == "note_build_ledger_row":
        return _build_ledger_row(tool_input)

    return f"[Unknown note tool: {name}]"
