# note フードウェルビーイング 自動投稿 収益化の仕組み

このドキュメントは、「フードウェルビーイング」noteアカウントの自動投稿を
収益化するために、このリポジトリに組み込んだ仕組みの説明です。

## 1. 収益源（3本柱）

note単体でできる収益化は主に3つあります。今回のシステムはこの3つを
1本の記事の中で組み合わせる構成にしています。

| 収益源 | 仕組み | 本システムでの対応 |
|---|---|---|
| ① 有料記事 | 記事の前半を無料公開し、続きを有料にする | `note_format_paid_article` が無料部分／有料区切り／有料本文を自動組版 |
| ② アフィリエイト | 記事内でサプリ・調理器具等を紹介し成果報酬を得る | `note_get_affiliate_links` が食品ウェルネス関連の商品リンク＋PR表記を挿入 |
| ③ メンバーシップ／サポート | 継続的な支援・会員向け限定コンテンツ | 記事末尾に自動でCTA（呼びかけ文）を挿入 |

## 2. 全体の流れ

```
[毎週月曜 GitHub Actions]
   ↓
Web検索で最新のフードウェルビーイング情報を収集
   ↓
note_suggest_pricing で価格帯を決定 (300〜1500円)
   ↓
note_get_affiliate_links で関連商品＋PR表記を用意
   ↓
note_format_paid_article で完成原稿を組版
   （無料イントロ／有料区切り／有料本文／アフィリエイト／メンバーシップ導線）
   ↓
GitHub content/note/YYYY-MM-DD-<slug>.md に保存
   ↓
data/note_revenue_ledger.csv に想定価格・カテゴリを追記
   ↓
Canvaで告知スライド＆SNS画像を生成、Gmailで完成報告
```

```
[毎月1日 GitHub Actions]
   ↓
Gmailでnoteからの購入/サポート通知メールを検索
   ↓
記事別・種別（有料記事／サポート／メンバーシップ）に集計
   ↓
note_revenue_ledger.csv の想定額と突き合わせ
   ↓
reports/note_revenue/YYYY-MM.md に月次レポートを保存
   ↓
Gmail下書きでサマリーを送付
```

## 3. 重要な前提・制約

- **note には記事投稿・決済結果を取得する公開APIがありません。**
  そのためこのシステムは「note にそのまま貼り付けられる完成原稿」を
  自動生成するところまでを担当します。最終的な有料設定・公開ボタンは
  人が note のエディタ上で行う必要があります。
- **収益集計はメール通知ベースです。** note は記事が購入・サポートされると
  登録メールアドレスに通知が届くため、月次レポートはこの通知メールを
  Gmail検索して集計する方式です。完全に自動化された会計データではない
  ため、月末に一度は台帳（`data/note_revenue_ledger.csv`）と実際の
  note管理画面の数値を突き合わせて確認してください。
- **Gmail / GitHub / Canva ツールは、Claude Code のMCP接続がある実行環境で
  動作します。** 素のGitHub Actionsランナー上でこれらのツール呼び出しが
  失敗する場合は、Claude Code (web/desktop) のセッションから
  `python main.py "..."` 相当のタスクを実行するか、各ツールをMCPなしでも
  動く実APIクライアントに置き換える対応が別途必要です。

## 4. 事前に必要な手動セットアップ

1. **note側の設定**
   - 有料記事を作成できるよう、note で振込先口座を登録しておく
   - メンバーシップ（サークル）機能を使う場合は事前に開設しておく
   - サポート機能（投げ銭）をオンにしておく
2. **アフィリエイト提携の申請**
   - Amazonアソシエイト、楽天アフィリエイト等に登録し、
     `tools/note.py` の `_AFFILIATE_CATALOG` 内のプレースホルダーURL
     （`YOUR_ASSOCIATE_ID` 等）を自分のIDに差し替える
3. **法令対応**
   - アフィリエイトを含む記事には必ずPR表記（`_DISCLOSURE_TEXT`）を残す
     （景品表示法のステルスマーケティング規制対応）
   - 有料コンテンツ販売について、特定商取引法上の表記が必要か
     不明な場合は note のクリエイター向けガイドラインを確認する
4. **GitHub Secrets**
   - `ANTHROPIC_API_KEY` を Settings → Secrets and variables → Actions に登録
     （既存のワークフローで使用中）

## 5. 価格の目安

| 深さ | 目安文字数 | 価格帯 |
|---|---|---|
| standard（一般的なまとめ） | 1,200〜2,200字 | 300円 |
| deep_dive（独自調査・データ・レシピ付き） | 2,200〜3,500字 | 500〜780円 |
| premium（個別プラン・限定特典） | 3,500字〜 | 980〜1,500円 |

価格や文字数レンジは `tools/note.py` の `_PRICING_TIERS` で調整できます。

## 6. 関連ファイル

- `tools/note.py` — 価格提案・アフィリエイト・原稿組版・台帳行の作成ロジック
- `tools/github.py` — note下書き・収益台帳の読み書き（`github_get_file_contents` を追加）
- `teams/marketing.py` — note収益化の標準フローをシステムプロンプトに追加
- `teams/accounting.py` — note売上の月次集計・レポーティングを追加
- `data/note_revenue_ledger.csv` — 記事ごとの想定収益を記録する台帳
- `content/note/` — note投稿用に生成した下書き原稿の保存先
- `reports/note_revenue/` — 月次収益レポートの保存先
- `.github/workflows/food_wellbeing.yml` — 週次の記事生成＋収益化自動化
- `.github/workflows/note_revenue_report.yml` — 月次の収益集計自動化
