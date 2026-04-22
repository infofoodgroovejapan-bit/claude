#!/usr/bin/env python3
"""AI Secretary System — CLI entry point.

Usage:
  python main.py "来月のマーケティング戦略会議をカレンダーに追加して"
  python main.py --verbose "新製品の企画書を作って"
  echo "Q3経費レポートを送ってください" | python main.py
  python main.py --interactive
"""
import argparse
import os
import sys
from pathlib import Path

# Load .env before importing any module that uses ANTHROPIC_API_KEY
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass  # python-dotenv not installed; rely on environment variable

# Verify API key is present
if not os.environ.get("ANTHROPIC_API_KEY"):
    print(
        "エラー / Error: ANTHROPIC_API_KEY が設定されていません。\n"
        ".env ファイルに ANTHROPIC_API_KEY=sk-... を追加するか、"
        "環境変数として設定してください。",
        file=sys.stderr,
    )
    sys.exit(1)

from secretary.agent import SecretaryAgent  # noqa: E402 (after env setup)


def _print_response(response, verbose: bool) -> None:
    """Print the agent response, with optional verbose metadata."""
    try:
        from rich.console import Console
        from rich.markdown import Markdown
        from rich.panel import Panel

        console = Console()

        if verbose:
            team_label = f"{response.team_name_ja} ({response.team_name})"
            console.print(f"\n[bold cyan]担当チーム:[/bold cyan] {team_label}")
            if response.tools_used:
                console.print(
                    f"[bold cyan]使用ツール:[/bold cyan] {', '.join(response.tools_used)}"
                )
            console.print()

        console.print(Markdown(response.response_text))

    except ImportError:
        # Fallback without rich
        if verbose:
            print(f"\n[担当チーム: {response.team_name_ja} / {response.team_name}]")
            if response.tools_used:
                print(f"[使用ツール: {', '.join(response.tools_used)}]")
            print()
        print(response.response_text)


def _run_interactive(secretary: SecretaryAgent) -> None:
    """Run a multi-turn interactive session."""
    print("AI秘書システム / AI Secretary System")
    print("終了するには 'exit' または Ctrl+C を入力してください。")
    print("-" * 50)

    while True:
        try:
            task = input("\nタスク / Task > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nセッションを終了します。")
            break

        if task.lower() in {"exit", "quit", "終了", "q"}:
            print("セッションを終了します。")
            break

        if not task:
            continue

        response = secretary.handle_task(task)
        _print_response(response, verbose=secretary.verbose)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI Secretary System — タスクを専門チームに割り振るAI秘書",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例 / Examples:
  python main.py "来月のマーケティング戦略会議をカレンダーに追加して"
  python main.py --verbose "新製品の企画書を作って"
  python main.py --verbose "今月の経費精算レポートを経理担当に送って"
  python main.py --verbose "新商品発表のプレゼン資料を作って"
  python main.py --pdf survey.pdf "アンケートからウェルビーイングを分析してください"
  python main.py --pdf q1.pdf --pdf q2.pdf "ウェルビーイングのトレンド分析をして"
  echo "Q3の売上レポートを作成して" | python main.py
  python main.py --interactive
""",
    )
    parser.add_argument(
        "task",
        nargs="?",
        help="実行するタスク (省略するとstdinから読み込みます)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="担当チームと使用ツールを表示する",
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="対話モード（複数タスクを連続して入力できます）",
    )
    parser.add_argument(
        "--pdf",
        metavar="FILE",
        action="append",
        dest="pdf_paths",
        default=None,
        help=(
            "添付するPDFファイルのパス（複数指定可） / "
            "Path to a PDF file to attach (repeatable). "
            "Example: --pdf survey1.pdf --pdf survey2.pdf"
        ),
    )

    args = parser.parse_args()
    secretary = SecretaryAgent(verbose=args.verbose)

    if args.interactive:
        _run_interactive(secretary)
        return

    # Get task from argument or stdin
    task_text = args.task
    if task_text is None:
        if not sys.stdin.isatty():
            task_text = sys.stdin.read().strip()
        else:
            parser.print_help()
            sys.exit(1)

    if not task_text:
        print("エラー: タスクが指定されていません。", file=sys.stderr)
        sys.exit(1)

    # Validate PDF paths before sending to the API
    if args.pdf_paths:
        for pdf_path in args.pdf_paths:
            if not os.path.exists(pdf_path):
                print(
                    f"エラー: PDFファイルが見つかりません: {pdf_path}",
                    file=sys.stderr,
                )
                sys.exit(1)
            if not pdf_path.lower().endswith(".pdf"):
                print(
                    f"エラー: PDF形式のファイルを指定してください: {pdf_path}",
                    file=sys.stderr,
                )
                sys.exit(1)

    response = secretary.handle_task(task_text, pdf_paths=args.pdf_paths)
    _print_response(response, verbose=args.verbose)


if __name__ == "__main__":
    main()
