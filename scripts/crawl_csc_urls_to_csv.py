import csv
import os
import re
import sys
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core import CSC_URLS


@dataclass
class ExtractedBlock:
    block_type: str  # text | table
    order: int
    title: str
    content: str


def _clean_text(s: str) -> str:
    s = re.sub(r"\s+", " ", (s or "")).strip()
    return s


def _fetch_html(url: str, timeout: int = 30) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; CSCDataBot/1.0; +https://www.csc.go.kr)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or resp.encoding
    return resp.text


def _extract_blocks_from_html(html: str) -> List[ExtractedBlock]:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Remove global UI chrome that is shared across pages
    for tag in soup.find_all(["header", "nav", "footer", "aside"]):
        try:
            tag.decompose()
        except Exception:
            pass

    # Some pages use wrappers for menu/gnb; remove common patterns if present
    for sel in [
        "#gnb", "#lnb", ".gnb", ".lnb", "#header", "#footer", ".footer", ".header",
        ".sub_visual", ".subVisual", ".breadcrumb", ".location", ".snb",
    ]:
        for node in soup.select(sel):
            try:
                node.decompose()
            except Exception:
                pass

    # Remove tab-like UI blocks often embedded inside the main content
    for sel in [
        ".tab", ".tabs", ".tab_menu", ".tabMenu", ".tabmenu", ".tab_list", ".tabList",
        ".tab_area", ".tabArea", ".sub_tab", ".subTab",
        "[role='tablist']",
    ]:
        for node in soup.select(sel):
            try:
                node.decompose()
            except Exception:
                pass

    def pick_main_node() -> BeautifulSoup:
        candidates = [
            "main",
            "#contents", "#content", "#subContents", "#subContent",
            ".contents", ".content", ".subContents", ".subContent",
            "#container", ".container",
            ".sub_cont", ".sub_conts", ".sub_conts_area",
            ".cont", ".con",
        ]
        for sel in candidates:
            node = soup.select_one(sel)
            if node and _clean_text(node.get_text(" ", strip=True)):
                return node
        return soup.body or soup

    body = pick_main_node()

    blocks: List[ExtractedBlock] = []
    order = 0

    def _is_ui_label(el) -> bool:
        try:
            if el is None:
                return False
            if el.name in {"a", "button"}:
                pass
            else:
                return False

            # Walk up a few levels: tab/menu/list widgets live in UL/OL/DIV with tab/menu classes
            cur = el
            for _ in range(6):
                cur = getattr(cur, "parent", None)
                if cur is None or not getattr(cur, "name", None):
                    break
                cls = " ".join(cur.get("class", []) or [])
                if re.search(r"(tab|menu|gnb|lnb|snb|nav|list)", cls, flags=re.IGNORECASE):
                    return True
                if cur.get("role") in {"tablist", "navigation"}:
                    return True
            return False
        except Exception:
            return False

    def add_text(title: str, content: str, el=None):
        nonlocal order
        content = _clean_text(content)
        if not content:
            return

        # Drop short UI labels (tab/menu titles) that pollute many pages
        if el is not None and _is_ui_label(el):
            if len(content) <= 16 and re.fullmatch(r"[0-9A-Za-z가-힣\s]+", content or ""):
                return

        blocks.append(ExtractedBlock(block_type="text", order=order, title=_clean_text(title), content=content))
        order += 1

    def add_table(title: str, table_rows: List[List[str]]):
        nonlocal order
        if not table_rows:
            return
        joined = "\n".join([" | ".join([_clean_text(c) for c in row]) for row in table_rows])
        joined = joined.strip()
        if not joined:
            return
        blocks.append(ExtractedBlock(block_type="table", order=order, title=_clean_text(title), content=joined))
        order += 1

    # Heuristic: extract headings/paragraphs/lists and tables in DOM order
    current_heading = ""
    for el in body.descendants:
        if not getattr(el, "name", None):
            continue

        if el.name in {"h1", "h2", "h3", "h4"}:
            current_heading = _clean_text(el.get_text(" ", strip=True))
            continue

        if el.name == "table":
            rows = []
            for tr in el.find_all("tr"):
                cells = tr.find_all(["th", "td"])
                if not cells:
                    continue
                rows.append([c.get_text(" ", strip=True) for c in cells])
            add_table(current_heading, rows)
            continue

        if el.name in {"p", "li"}:
            txt = el.get_text(" ", strip=True)
            add_text(current_heading, txt, el=el)
            continue

        # Also capture standalone anchor/button text if it's not UI chrome
        if el.name in {"a", "button"}:
            txt = el.get_text(" ", strip=True)
            add_text(current_heading, txt, el=el)
            continue

    # fallback: if nothing extracted, take full text
    if not blocks:
        add_text("", body.get_text(" ", strip=True))

    # de-duplicate adjacent identical contents
    deduped: List[ExtractedBlock] = []
    last = None
    for b in blocks:
        key = (b.block_type, b.title, b.content)
        if last == key:
            continue
        deduped.append(b)
        last = key
    return deduped


def _safe_filename(name: str) -> str:
    name = re.sub(r"[^0-9A-Za-z가-힣_\-]+", "_", name).strip("_")
    return name or "page"


def write_page_csv(out_dir: str, page_key: str, url: str, blocks: List[ExtractedBlock]) -> str:
    os.makedirs(out_dir, exist_ok=True)
    filename = f"{_safe_filename(page_key)}.csv"
    path = os.path.join(out_dir, filename)

    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["page_key", "url", "block_type", "order", "title", "content"])
        for b in blocks:
            w.writerow([page_key, url, b.block_type, b.order, b.title, b.content])

    return path


def crawl_all(out_dir: str = os.path.join("data", "pages"), limit: Optional[int] = None) -> List[Tuple[str, str]]:
    results = []
    items = list(CSC_URLS.items())
    if limit is not None:
        items = items[:limit]

    for page_key, url in items:
        print(f"[crawl] {page_key}: {url}")
        try:
            html = _fetch_html(url)
            blocks = _extract_blocks_from_html(html)
            path = write_page_csv(out_dir, page_key, url, blocks)
            results.append((page_key, path))
            print(f"  -> wrote {path} (blocks={len(blocks)})")
        except Exception as e:
            print(f"  !! failed: {e}")

    return results


if __name__ == "__main__":
    crawl_all()
