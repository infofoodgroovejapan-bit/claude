"""Food Wellbeing Knowledge Base.

Adlerian psychology principles applied to food, social wellbeing data,
SNS content templates, manga/4-koma templates, and note.com article structure.

Imported by FoodWellbeingAgent and embedded into its system prompt at module
load time for prompt caching efficiency.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# 1. Adlerian Psychology Principles × Food
# ---------------------------------------------------------------------------

ADLERIAN_FOOD_PRINCIPLES: list[dict] = [
    {
        "concept": "社会的関心 (Gemeinschaftsgefühl / Social Interest)",
        "concept_en": "Social Interest",
        "description_ja": (
            "アドラーは人間の幸福の核心を「社会への貢献感」に置いた。"
            "食の文脈では、一緒に食卓を囲む行為、地産地消による地域貢献、"
            "フードバンクへの寄付などが社会的関心を育む実践例となる。"
        ),
        "description_en": (
            "Adler placed the sense of contribution to society at the core of human happiness. "
            "In food: sharing meals, buying local produce, donating to food banks are "
            "concrete expressions of Social Interest."
        ),
        "food_applications": [
            "共食（きょうしょく）— 食卓を囲む社会的絆",
            "地産地消 — 地域農家を支える食の選択",
            "フードバンク活動 — 余剰食品を社会へ還元",
            "食育ボランティア — 次世代への食知識の伝達",
        ],
        "wellbeing_dimension": "social",
    },
    {
        "concept": "共同体感覚 (Community Feeling / Sense of Belonging)",
        "concept_en": "Community Feeling",
        "description_ja": (
            "共同体の一員であるという感覚が人を健康にする。"
            "伝統料理を家族や地域と共有すること、食文化を次世代に伝えることが"
            "帰属感と安心感を育む。"
        ),
        "description_en": (
            "The sense of belonging to a community promotes health. "
            "Sharing traditional dishes with family and community, passing food "
            "culture to the next generation nurtures belonging and psychological safety."
        ),
        "food_applications": [
            "家族の食卓 — 毎日の共食が帰属感を強化",
            "郷土料理の継承 — 地域のアイデンティティと食",
            "地域の食祭り・収穫祭 — 共同体で食を祝う",
            "職場・学校の共食 — 日常の共食が信頼を醸成",
        ],
        "wellbeing_dimension": "social",
    },
    {
        "concept": "勇気付け (Encouragement / Mut-machung)",
        "concept_en": "Encouragement",
        "description_ja": (
            "アドラー心理学では「勇気付け」が変容の鍵。食においては、"
            "健康的な食習慣を褒め・励ます環境が持続的な行動変容を生む。"
            "批判や罰ではなく、小さな成功を認める姿勢が重要。"
        ),
        "description_en": (
            "Encouragement is the key to change. Environments that affirm healthy "
            "eating habits produce lasting behaviour change — recognising small wins "
            "rather than punishing failures."
        ),
        "food_applications": [
            "食事日記と自己承認 — 小さな健康行動を記録・称賛",
            "家族での料理チャレンジ — 挑戦を励ます食の環境",
            "ポジティブな食育 — 「ダメ」ではなく「良い選択」を強調",
            "料理の腕前を認める — プロセスを称えるアドラー式フィードバック",
        ],
        "wellbeing_dimension": "psychological",
    },
    {
        "concept": "ライフスタイル (Lifestyle / Lebensstil)",
        "concept_en": "Lifestyle",
        "description_ja": (
            "アドラーは各人が幼少期に形成した「ライフスタイル」を持つとした。"
            "食のライフスタイルは無意識の信念（例：「忙しい人はジャンクフードで良い」）に"
            "左右される。意識化と再学習が健康的な食行動に繋がる。"
        ),
        "description_en": (
            "Adler proposed each person carries a 'Lifestyle' formed in childhood. "
            "Food lifestyles are driven by unconscious beliefs (e.g., 'busy people eat fast food'). "
            "Making these beliefs conscious leads to healthier food behaviour."
        ),
        "food_applications": [
            "食の自動思考の認識 — 「なぜこれを食べるか」を問い直す",
            "マインドフル・イーティング — 意識的に食事と向き合う実践",
            "食の価値観の棚卸し — 自分の食ライフスタイルを可視化",
            "習慣的食パターンの変容 — 小さなステップで食行動を変える",
        ],
        "wellbeing_dimension": "psychological",
    },
    {
        "concept": "目的論 (Teleology / Goal-directedness)",
        "concept_en": "Teleology",
        "description_ja": (
            "アドラーは行動は過去の原因ではなく未来の目的に向かうと考えた。"
            "食においても「なぜ食べるか」（目的）を明確にすることが、"
            "感情的食行動（ストレス食い）の変容を助ける。"
        ),
        "description_en": (
            "Adler believed behaviour is driven by future goals, not past causes. "
            "Clarifying 'why we eat' helps transform emotional eating. "
            "Shifting from 'I eat because I'm stressed' to 'I eat to feel energised' is a teleological reframe."
        ),
        "food_applications": [
            "感情的食行動の目的分析 — ストレス食いの「目的」を探る",
            "食の意図設定 — 「活力のために食べる」意識を持つ",
            "ストレスと食の関係整理 — 食以外のストレス解消法を探索",
            "SMARTゴールでの栄養目標設定 — 具体的な食の未来像を描く",
        ],
        "wellbeing_dimension": "psychological",
    },
    {
        "concept": "劣等感と補償 (Inferiority Feelings & Compensation)",
        "concept_en": "Inferiority & Compensation",
        "description_ja": (
            "アドラーは劣等感（例：体型への不満）が過剰補償（過食・拒食）を引き起こすと指摘。"
            "健全な補償は「より良い栄養知識を得る」「料理スキルを上げる」など建設的方向へ向かう。"
        ),
        "description_en": (
            "Inferiority feelings (e.g., body image dissatisfaction) can lead to "
            "over-compensation (overeating or restrictive eating). "
            "Healthy compensation redirects towards constructive goals: better nutrition knowledge, cooking skills."
        ),
        "food_applications": [
            "ボディイメージと食の関係を整理 — 自己批判から自己理解へ",
            "食への罪悪感の解消 — 「完璧な食事」という幻想から解放",
            "料理学習で自己効力感向上 — 建設的補償の最良例",
            "ヘルスコーチングとの連携 — 専門家と共に補償パターンを変える",
        ],
        "wellbeing_dimension": "psychological",
    },
    {
        "concept": "貢献感 (Sense of Contribution)",
        "concept_en": "Sense of Contribution",
        "description_ja": (
            "「自分は役に立っている」という感覚が幸福の源泉とアドラーは説いた。"
            "食の文脈では料理を作って人に喜ばれること、食育を通じた地域貢献が"
            "強い貢献感をもたらし、ウェルビーイングを向上させる。"
        ),
        "description_en": (
            "The sense of 'I am useful and contributing' is the source of wellbeing. "
            "Cooking for others, contributing to community through food education "
            "bring a powerful sense of contribution and enhance wellbeing."
        ),
        "food_applications": [
            "料理のプレゼント文化 — 手作りで「貢献感」を高める",
            "食育ボランティア — 知識を地域に還元する喜び",
            "職場への手作り差し入れ — 日常の小さな貢献",
            "コミュニティガーデン参加 — 食を育てて地域に貢献",
        ],
        "wellbeing_dimension": "social",
    },
]


# ---------------------------------------------------------------------------
# 2. Social Wellbeing × Food Themes
# ---------------------------------------------------------------------------

SOCIAL_WELLBEING_FOOD_THEMES: list[dict] = [
    {
        "theme": "食の孤独 (Food Isolation / 孤食)",
        "theme_en": "Food Isolation",
        "description_ja": "一人食べ（孤食）の増加と社会的孤立の相関。高齢者・若年単身世帯に深刻。",
        "description_en": "Growing correlation between eating alone and social isolation, especially in elderly and young single households.",
        "statistics_ja": "日本の孤食率は40%超（NHK調査）、孤食が続く高齢者は抑うつリスク2倍",
        "interventions": ["共食推進プログラム", "こども食堂（全国5,000か所超）", "高齢者配食サービス"],
    },
    {
        "theme": "食育と社会資本 (Food Education & Social Capital)",
        "theme_en": "Food Education & Social Capital",
        "description_ja": "食育を通じた社会的絆の形成。学校・地域・家庭での食育が信頼関係を構築。",
        "description_en": "Building social bonds through food education across schools, communities, and families.",
        "statistics_ja": "食育基本法（2005年）制定以来、全国で食育推進計画が展開",
        "interventions": ["学校給食での食育", "地域料理教室", "農業体験プログラム"],
    },
    {
        "theme": "食のダイバーシティ (Food Diversity & Inclusion)",
        "theme_en": "Food Diversity & Inclusion",
        "description_ja": "多文化共生における食の役割。異文化理解と受容を食が橋渡しする。",
        "description_en": "Food as a bridge for cross-cultural understanding and multicultural coexistence.",
        "statistics_ja": "日本在住外国人330万人超（2024年）— 食文化の多様性が急増",
        "interventions": ["多文化食イベント", "国際料理教室", "学校給食の多様化"],
    },
    {
        "theme": "食料安全保障と社会的公正 (Food Security & Social Justice)",
        "theme_en": "Food Security & Social Justice",
        "description_ja": "食へのアクセス格差と社会的公正。経済的弱者が新鮮で栄養ある食にアクセスできる社会。",
        "description_en": "Addressing inequalities in food access. Ensuring economically vulnerable groups can access nutritious food.",
        "statistics_ja": "子どもの貧困率約11%（2022年）、こども食堂利用者は年々増加",
        "interventions": ["フードバンク", "こども食堂", "学校給食費無償化"],
    },
    {
        "theme": "食と精神的健康 (Food & Mental Health)",
        "theme_en": "Food & Mental Health",
        "description_ja": "栄養と精神健康の関係。腸脳軸研究による食と気分・認知の双方向的影響。",
        "description_en": "The gut-brain axis: bidirectional influence of diet on mood and cognition.",
        "statistics_ja": "発酵食品摂取と抑うつリスク低減の相関（複数RCT研究で実証）",
        "interventions": ["マインドフル・イーティング", "発酵食品の普及", "栄養精神医学的アプローチ"],
    },
]


# ---------------------------------------------------------------------------
# 3. Weekly Report Slide Template
# ---------------------------------------------------------------------------

WEEKLY_REPORT_TEMPLATE: dict = {
    "title_ja": "フードウェルビーイング週次レポート",
    "title_en": "Food Wellbeing Weekly Report",
    "slide_structure": [
        {"slide": 1, "title": "表紙", "content": "週次タイトル・日付・アドラー心理学×フードウェルビーイング"},
        {"slide": 2, "title": "今週のアドラー概念", "content": "週替わりのアドラー原則と食への応用"},
        {"slide": 3, "title": "最新ウェルビーイング研究", "content": "ウェブ検索で収集した最新記事・データのインサイト"},
        {"slide": 4, "title": "社会的ウェルビーイング指標", "content": "共食率・孤食率・食育データのビジュアル"},
        {"slide": 5, "title": "今週の実践アクション", "content": "読者が今週試せる3つの食×ウェルビーイング実践"},
        {"slide": 6, "title": "まとめ＋CTA", "content": "核心メッセージ・note記事誘導・研修・講演の問い合わせ先"},
    ],
    "design_style": "professional, warm, nature-inspired (green, earth tones), bilingual",
}


# ---------------------------------------------------------------------------
# 4. SNS Content Templates
# ---------------------------------------------------------------------------

SNS_CONTENT_TEMPLATES: dict = {
    "weekly_series": [
        {
            "day": "月曜",
            "theme": "今週のアドラー概念×食（ウェブ検索記事のインサイトを活用）",
            "format": "学び投稿",
            "structure": "【今週のフードウェルビーイング】\n[アドラー概念名]\n\n[概念の説明 2〜3行]\n\n💡実践例: [具体的な食での応用]\n\n[出典・研究インサイト（ウェブ検索結果から）]\n\n[ハッシュタグ]",
        },
        {
            "day": "火曜",
            "theme": "4コマ漫画：アドラー×食の日常シーン",
            "format": "漫画投稿",
            "structure": "【4コマ漫画】[今週のテーマ]\n\n[コマ1: 起 — 日常の食シーン]\n[コマ2: 承 — 問題・葛藤]\n[コマ3: 転 — アドラー的気づき]\n[コマ4: 結 — 変容・笑い・希望]\n\n[ハッシュタグ]",
        },
        {
            "day": "水曜",
            "theme": "今すぐできる食×ウェルビーイング実践Tips",
            "format": "Tips投稿",
            "structure": "【今日からできる3つのこと】\n\n✅ [Tips 1]\n✅ [Tips 2]\n✅ [Tips 3]\n\nアドラー心理学で言う「[関連概念]」の実践です。\n\n[ハッシュタグ]",
        },
        {
            "day": "木曜",
            "theme": "漫画：食の悩みをアドラー式に解決",
            "format": "漫画投稿",
            "structure": "【アドラー先生に相談】\nお悩み: [読者の食の悩み]\n\n[コマ1: 悩みを抱えるウェルちゃん]\n[コマ2: アドラー先生に相談]\n[コマ3: アドラー的アドバイス]\n[コマ4: 解決・笑顔]\n\n[ハッシュタグ]",
        },
        {
            "day": "金曜",
            "theme": "週次レポート紹介＋note記事誘導",
            "format": "告知＋CTA投稿",
            "structure": "【今週のフードウェルビーイングまとめ】\n\n今週のテーマ: [アドラー概念]\n\n📊 週次レポート: [Canva URL]\n📝 詳しい解説はnoteで→ [URL]\n\n研修・講演のご依頼はプロフのリンクへ\n\n[ハッシュタグ]",
        },
    ],
    "cta_templates": {
        "note": "詳しくはnoteで→ [URL]",
        "inquiry": "フードウェルビーイングの研修・講演・コンサルのご依頼はプロフへ",
        "report": "週次レポートはCanvaで公開中 → [URL]",
    },
    "hashtags": [
        "#フードウェルビーイング",
        "#アドラー心理学",
        "#食と心理",
        "#ウェルビーイング",
        "#食育",
        "#共食",
        "#FoodWellbeing",
        "#AdlerianPsychology",
        "#漫画",
        "#4コマ",
    ],
}


# ---------------------------------------------------------------------------
# 5. Manga / 4-Koma Content Templates
# ---------------------------------------------------------------------------

MANGA_CONTENT_TEMPLATES: dict = {
    "4koma_structure": {
        "format": "4コマ漫画形式（起承転結）",
        "panels": [
            {"panel": 1, "role": "起 — 日常の食シーン・悩みの導入（共感しやすい状況）"},
            {"panel": 2, "role": "承 — 問題の深まり・感情の表現（読者が「わかる！」と感じる）"},
            {"panel": 3, "role": "転 — アドラー的視点の気づき（「なるほど！」の瞬間）"},
            {"panel": 4, "role": "結 — 行動変容・笑い・希望（ポジティブな締めくくり）"},
        ],
        "characters": [
            {"name": "ウェルちゃん", "description": "30代、フードウェルビーイングを学ぶ主人公。食の悩みを抱えながら成長する"},
            {"name": "アドラー先生", "description": "穏やかで励ましてくれるナビゲーター。対話形式でアドラー哲学を伝える"},
        ],
    },
    "scenario_themes": [
        {
            "theme": "コンビニ飯ループ",
            "scenario": "忙しくてコンビニ飯続き → 罪悪感 → 「共同体感覚」で料理は社会貢献と気づく → 週1回だけ手料理チャレンジ",
        },
        {
            "theme": "ダイエット失敗",
            "scenario": "ダイエット失敗の罪悪感 → 自己批判 → 「目的論」で何のために食べるかを問い直す → 活力のために食べる意識に転換",
        },
        {
            "theme": "孤食の寂しさ",
            "scenario": "一人ご飯が続いて寂しい → 孤食の習慣化 → 「共食」の価値に気づく → 月1回の友人との食事を企画",
        },
        {
            "theme": "ストレス食い",
            "scenario": "仕事のストレスで過食 → 自己嫌悪 → 「劣等感と補償」を理解 → 食以外のストレス解消法を探す",
        },
    ],
    "canva_style_prompt": (
        "日本の4コマ漫画スタイル、シンプルでかわいいイラスト、"
        "温かみのあるカラーパレット（グリーン・イエロー・オレンジ系）、"
        "吹き出し付き4コマ構成、教育的でユーモラスな雰囲気、"
        "キャラクター「ウェルちゃん」と「アドラー先生」が登場。"
        "Japanese 4-panel manga (yonkoma) style, simple cute illustration, "
        "warm color palette (greens, yellows, oranges), speech bubbles, "
        "4-panel grid layout, educational and humorous tone."
    ),
    "canva_single_panel_prompt": (
        "日本のかわいいイラストスタイル、フードウェルビーイングをテーマにしたSNS投稿画像、"
        "正方形フォーマット、大きな文字のキャッチコピー、グリーン系カラー。"
        "Cute Japanese illustration style, food wellbeing themed SNS post, "
        "square format, large catchphrase text, green color scheme."
    ),
}


# ---------------------------------------------------------------------------
# 6. note.com Article Template
# ---------------------------------------------------------------------------

NOTE_ARTICLE_TEMPLATE: dict = {
    "target_length": 1700,
    "structure": [
        {
            "section": "タイトル",
            "guideline": "検索キーワードを含む、読者の悩みに刺さるタイトル（例：「なぜ一人で食べると不幸になるのか？アドラー心理学で解説」）",
        },
        {
            "section": "リード文",
            "guideline": "共感フック（あるある悩み）＋この記事で得られること。200字程度。",
        },
        {
            "section": "本論1: 今週のアドラー概念",
            "guideline": "概念の説明＋食への具体的応用例。500字程度。",
        },
        {
            "section": "本論2: 社会データで見る食とウェルビーイング",
            "guideline": "最新ウェブ検索で得た統計・研究データ＋解釈。400字程度。",
        },
        {
            "section": "本論3: 今日からできる3ステップ",
            "guideline": "読者が今週実践できる具体的アクション3つ。400字程度。",
        },
        {
            "section": "まとめ＋CTA",
            "guideline": "要約（3行）＋「フードウェルビーイングの研修・講演・コンサルについてはお問い合わせください」CTA。200字程度。",
        },
    ],
    "seo_keywords": ["フードウェルビーイング", "アドラー心理学", "食と心理", "食育", "社会的ウェルビーイング"],
    "cta": "フードウェルビーイングに関する研修・講演・コンサルティングのご依頼・お問い合わせはこちら。",
}


# ---------------------------------------------------------------------------
# 7. Web Search Query Templates
# ---------------------------------------------------------------------------

SEARCH_QUERIES: list[str] = [
    "フードウェルビーイング 最新 2025",
    "アドラー心理学 食 健康 実践",
    "食 社会的ウェルビーイング 研究",
    "共食 孤食 健康効果 データ",
    "food wellbeing psychology research 2025",
]


# ---------------------------------------------------------------------------
# 8. Canva Prompt Templates
# ---------------------------------------------------------------------------

CANVA_PROMPT_TEMPLATES: dict = {
    "weekly_report": (
        "フードウェルビーイング週次レポート / Food Wellbeing Weekly Report. "
        "プロフェッショナルで温かみのあるプレゼンテーション、6スライド構成。"
        "アドラー心理学と食の社会的ウェルビーイングをテーマに。"
        "自然を感じるカラーパレット（グリーン、アースカラー）。"
        "日本語メインで英語サブタイトル付き。"
        "Professional and warm 6-slide presentation on Adlerian psychology "
        "and food wellbeing. Nature-inspired color palette. Bilingual (JA/EN)."
    ),
    "sns_learning": (
        "フードウェルビーイング SNS学び投稿用画像。"
        "正方形フォーマット（1080x1080px）、大きなキャッチコピー、"
        "グリーン系カラー、シンプルでプロフェッショナルなデザイン。"
        "SNS post for food wellbeing learning. Square format, large headline, green palette."
    ),
    "sns_tips": (
        "フードウェルビーイング 実践Tips SNS画像。"
        "正方形、3つのチェックリスト形式、オレンジ・グリーン系カラー、アイコン使用。"
        "Food wellbeing tips SNS post. Square, checklist format, orange-green colors."
    ),
    "sns_announcement": (
        "フードウェルビーイング 週次まとめ告知画像。"
        "正方形、週次レポートのサムネイル風、CTAボタン付き。"
        "Weekly food wellbeing summary announcement post with CTA."
    ),
    "manga_4koma": MANGA_CONTENT_TEMPLATES["canva_style_prompt"],
    "manga_single": MANGA_CONTENT_TEMPLATES["canva_single_panel_prompt"],
}


# ---------------------------------------------------------------------------
# 9. Build context summary for system prompt embedding
# ---------------------------------------------------------------------------

def build_context_summary() -> str:
    """Return a formatted knowledge base string for embedding in the agent system prompt."""
    lines: list[str] = [
        "## フードウェルビーイング知識ベース / Food Wellbeing Knowledge Base\n",
        "### アドラー心理学の核心概念と食への応用\n",
    ]

    for i, p in enumerate(ADLERIAN_FOOD_PRINCIPLES, 1):
        lines.append(f"**{i}. {p['concept']}**")
        lines.append(f"JA: {p['description_ja']}")
        lines.append(f"EN: {p['description_en']}")
        apps = " / ".join(p["food_applications"])
        lines.append(f"食の応用: {apps}")
        lines.append(f"次元: {p['wellbeing_dimension']}\n")

    lines.append("### 社会的ウェルビーイングと食のテーマ\n")
    for t in SOCIAL_WELLBEING_FOOD_THEMES:
        lines.append(f"**{t['theme']}**")
        lines.append(t["description_ja"])
        lines.append(f"統計: {t.get('statistics_ja', '')}")
        lines.append(f"介入策: {', '.join(t['interventions'])}\n")

    lines.append("### 週次レポートスライド構成\n")
    for s in WEEKLY_REPORT_TEMPLATE["slide_structure"]:
        lines.append(f"スライド{s['slide']}: {s['title']} — {s['content']}")

    lines.append("\n### SNS週次投稿シリーズ\n")
    for series in SNS_CONTENT_TEMPLATES["weekly_series"]:
        lines.append(f"**{series['day']}（{series['format']}）**: {series['theme']}")
        lines.append(f"構成フォーマット:\n{series['structure']}\n")

    lines.append("### 漫画コンテンツシナリオテーマ\n")
    for s in MANGA_CONTENT_TEMPLATES["scenario_themes"]:
        lines.append(f"- **{s['theme']}**: {s['scenario']}")

    lines.append("\n### note記事テンプレート\n")
    for sec in NOTE_ARTICLE_TEMPLATE["structure"]:
        lines.append(f"- **{sec['section']}**: {sec['guideline']}")

    lines.append(f"\n### 週次ウェブ検索クエリ例\n")
    for q in SEARCH_QUERIES:
        lines.append(f"- {q}")

    return "\n".join(lines)
