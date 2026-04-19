"""Web search tool using DuckDuckGo (no API key required).

Provides web_search and fetch_webpage tools for retrieving current
wellbeing blog articles and research to enrich SNS content.
"""
from __future__ import annotations

TOOL_DEFINITIONS = [
    {
        "name": "web_search",
        "description": (
            "Search the web for recent articles, blog posts, and news about food wellbeing, "
            "Adlerian psychology, nutrition, and related topics. "
            "Returns titles, URLs, and snippets. Use for finding current research and insights."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query in Japanese or English",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Number of results to return (1-5, default 3)",
                    "default": 3,
                },
                "region": {
                    "type": "string",
                    "description": "Search region: 'jp-ja' for Japan/Japanese, 'wt-wt' for worldwide",
                    "default": "jp-ja",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "fetch_webpage",
        "description": (
            "Fetch and extract the main text content from a webpage URL. "
            "Use this to get the full content of a found article for summarisation."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Full URL of the webpage to fetch",
                },
                "max_chars": {
                    "type": "integer",
                    "description": "Maximum characters to return (default 3000)",
                    "default": 3000,
                },
            },
            "required": ["url"],
        },
    },
]


def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "web_search":
        return _web_search(
            tool_input["query"],
            tool_input.get("max_results", 3),
            tool_input.get("region", "jp-ja"),
        )
    if tool_name == "fetch_webpage":
        return _fetch_webpage(tool_input["url"], tool_input.get("max_chars", 3000))
    return f"[Unknown tool: {tool_name}]"


def _web_search(query: str, max_results: int, region: str) -> str:
    try:
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                from ddgs import DDGS
            except ImportError:
                from duckduckgo_search import DDGS  # type: ignore[no-redef]

        results: list[str] = []
        with DDGS() as ddgs:
            for backend in ("html", "lite", "auto"):
                try:
                    hits = ddgs.text(query, region=region, max_results=max_results, backend=backend)
                    if hits:
                        results = [f"**{r['title']}**\nURL: {r['href']}\n{r['body']}" for r in hits]
                        break
                except Exception:
                    continue
        return "\n\n---\n\n".join(results) if results else "検索結果が見つかりませんでした（ネットワーク制限の可能性があります）。"
    except ImportError:
        return "[web_search] ddgs パッケージがインストールされていません。pip install ddgs を実行してください。"
    except Exception as e:
        return f"[web_search エラー] {e}"


def _fetch_webpage(url: str, max_chars: int) -> str:
    try:
        import requests
        from html.parser import HTMLParser

        resp = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0 (compatible; WellbeingBot/1.0)"},
        )
        resp.raise_for_status()

        class _TextExtractor(HTMLParser):
            def __init__(self) -> None:
                super().__init__()
                self.text: list[str] = []
                self._skip = False

            def handle_starttag(self, tag: str, attrs: list) -> None:
                if tag in ("script", "style", "nav", "footer", "header", "aside"):
                    self._skip = True

            def handle_endtag(self, tag: str) -> None:
                if tag in ("script", "style", "nav", "footer", "header", "aside"):
                    self._skip = False

            def handle_data(self, data: str) -> None:
                if not self._skip and data.strip():
                    self.text.append(data.strip())

        parser = _TextExtractor()
        parser.feed(resp.text)
        return " ".join(parser.text)[:max_chars]
    except Exception as e:
        return f"[fetch_webpage エラー] {e}"
