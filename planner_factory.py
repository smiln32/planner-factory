#!/usr/bin/env python3
"""Generate full-page, Canva-importable US Letter planner HTML from JSON.

The output uses ordinary HTML text, divs, borders, checkboxes, lines, and tables
so Canva can import the design as editable elements rather than a flat page image.

Usage:
    python planner_factory.py planner_spec.json output.html
    python planner_factory.py planner_spec.json output.html --validate-only
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path
from typing import Any

PAGE_W = 816
PAGE_H = 1056
HEADER_TOP = 24
HEADER_H = 66
FOOTER_BOTTOM = 10
SAFE_BOTTOM = 1030
FILL_TARGET = 980
CONTENT_TOP, CONTENT_BOTTOM, CONTENT_W, GAP = 104, 1030, 760, 14

CSS = r"""
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#ececec;font-family:"Aptos","Helvetica Neue",Arial,sans-serif;color:#343a38}
@page{size:Letter;margin:0}
.page{position:relative;width:816px;height:1056px;margin:0 auto;background:#fff;page-break-after:always;overflow:hidden}
.page:last-child{page-break-after:auto}
.header{position:absolute;left:28px;top:24px;width:760px;height:66px;border-radius:10px;background:var(--theme);display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:0 16px}
.title{font-family:Georgia,"Times New Roman",serif;font-size:23px;font-weight:700;line-height:1.05;letter-spacing:-.25px;margin:0 0 5px;text-wrap:balance}
.subtitle{font-size:10px;line-height:1.1;color:#4d4d4d;margin:0}
.footer{position:absolute;left:28px;bottom:10px;width:760px;height:16px;display:flex;justify-content:space-between;align-items:center;font-size:8px;color:#8c8c8c}
.box{position:absolute;border:1.2px solid #5c5c5c;border-radius:10px;background:#fff;overflow:hidden}
.head{height:32px;display:flex;align-items:center;padding:0 12px;font-size:10.5px;font-weight:700;border-bottom:1.2px solid #5c5c5c;letter-spacing:.15px}
.sage{background:#dfe9df}.lav{background:#e8dfea}.blue{background:#dce8ee}.warm{background:#f0e6e2}.rose{background:#eee0dd}.ivory{background:#fbf9f6}
.body{height:calc(100% - 32px);padding:11px 13px;background:#fff}
.prompt{font-size:9px;font-weight:700;margin:0 0 4px}
.line{height:22px;border-bottom:1px solid #b9b9b9}
.line.tight{height:18px}.line.tall{height:27px}
.grid-lines{display:grid;height:100%;grid-template-rows:repeat(var(--rows),1fr);gap:0}
.check-row{display:grid;grid-template-columns:14px 1fr;gap:8px;align-items:center;height:24px;font-size:9.5px}
.check{width:10px;height:10px;border:1px solid #5c5c5c}
.radio{width:10px;height:10px;border:1px solid #5c5c5c;border-radius:50%}
.pill-row{display:flex;gap:12px;flex-wrap:wrap;align-items:center;font-size:9px;margin-bottom:4px}
.pill{display:flex;align-items:center;gap:5px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:12px;height:100%}
.label{font-size:9.5px;font-weight:700;margin-bottom:4px}
.small{font-size:8.5px;color:#555}.callout{font-size:10px;line-height:1.35}
.table{width:100%;border-collapse:collapse;table-layout:fixed;font-size:8px}
.table th,.table td{border:1px solid #7f7f7f;padding:4px;vertical-align:top}
.table th{background:#f5f5f5;font-weight:800;text-transform:uppercase;text-align:center}
.table td{height:31px}.center{text-align:center}
"""


def e(value: Any) -> str:
    return escape(str(value), quote=True)


def line_html(rows: int, line_class: str = "line") -> str:
    return "".join(f'<div class="{e(line_class)}"></div>' for _ in range(rows))


def checklist_html(items: list[str], blank_rows: int = 0) -> str:
    out = []
    for item in items:
        out.append(f'<div class="check-row"><div class="check"></div><div>{e(item)}</div></div>')
    for _ in range(blank_rows):
        out.append('<div class="check-row"><div class="check"></div><div class="line tight"></div></div>')
    return "".join(out)


def choices_html(options: list[str], control: str = "radio", lines_after: int = 0) -> str:
    control_class = "radio" if control == "radio" else "check"
    pills = "".join(
        f'<div class="pill"><div class="{control_class}"></div><span>{e(opt)}</span></div>'
        for opt in options
    )
    return f'<div class="pill-row">{pills}</div>' + line_html(lines_after)


def render_content(content: dict[str, Any]) -> str:
    kind = content.get("type", "lines")
    prompt = content.get("prompt")
    prefix = f'<div class="prompt">{e(prompt)}</div>' if prompt else ""

    if kind == "lines":
        rows = int(content.get("rows", 6))
        return prefix + f'<div class="grid-lines" style="--rows:{rows}">{line_html(rows)}</div>'

    if kind == "checklist":
        return prefix + checklist_html(
            [str(x) for x in content.get("items", [])],
            int(content.get("blank_rows", 0)),
        )

    if kind == "choices":
        return prefix + choices_html(
            [str(x) for x in content.get("options", [])],
            str(content.get("control", "radio")),
            int(content.get("lines_after", 0)),
        )

    if kind == "callout":
        text = content.get("text", "")
        rows = int(content.get("rows", 0))
        callout = f'<div class="callout">{e(text)}</div>'
        return prefix + callout + (f'<div class="grid-lines" style="--rows:{rows}">{line_html(rows)}</div>' if rows else "")

    if kind == "table":
        columns = content.get("columns", [])
        rows = int(content.get("rows", 10))
        th = []
        for col in columns:
            width = col.get("width")
            style = f' style="width:{e(width)}"' if width else ""
            th.append(f'<th{style}>{e(col.get("label", ""))}</th>')
        td_row = "<tr>" + "".join("<td></td>" for _ in columns) + "</tr>"
        return prefix + f'<table class="table"><tr>{"".join(th)}</tr>{td_row * rows}</table>'

    if kind == "split":
        left = render_content(content.get("left", {"type": "lines", "rows": 5}))
        right = render_content(content.get("right", {"type": "lines", "rows": 5}))
        return prefix + f'<div class="two-col"><div>{left}</div><div>{right}</div></div>'

    if kind == "custom_html":
        # Deliberately opt-in. The JSON author is responsible for valid HTML.
        return prefix + str(content.get("html", ""))

    raise ValueError(f"Unsupported content type: {kind}")


def render_box(block: dict[str, Any]) -> str:
    x = int(block["x"]); y = int(block["y"])
    w = int(block["w"]); h = int(block["h"])
    title = e(block.get("title", ""))
    color = e(block.get("color", "sage"))
    body = render_content(block.get("content", {"type": "lines", "rows": 6}))
    return (
        f'<div class="box" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
        f'<div class="head {color}">{title}</div><div class="body">{body}</div></div>'
    )


def validate_uniqueness_and_collisions(spec: dict[str, Any]) -> list[str]:
    findings, concepts, phrases = [], {}, {}
    for page_no, page in enumerate(spec.get("pages", []), 1):
        concept = re.sub(r"[^a-z0-9]+", " ", str(page.get("concept", page.get("title", ""))).lower()).strip()
        if concept in concepts: findings.append(f"ERROR: Pages {concepts[concept]} and {page_no} repeat the same concept.")
        elif concept: concepts[concept] = page_no
        blocks = page.get("blocks", [])
        for block_no, block in enumerate(blocks, 1):
            phrase = block.get("content", {}).get("prompt") or block.get("title", "")
            phrase = re.sub(r"[^a-z0-9]+", " ", str(phrase).lower()).strip()
            if len(phrase) >= 12 and phrase in phrases: findings.append(f"Page {page_no}, block {block_no}: repeats wording from page {phrases[phrase][0]}, block {phrases[phrase][1]}.")
            elif phrase: phrases[phrase] = (page_no, block_no)
        for a, first in enumerate(blocks):
            for b, second in enumerate(blocks[a + 1:], a + 2):
                if all(k in first and k in second for k in ("x", "y", "w", "h")) and first["x"] < second["x"] + second["w"] and first["x"] + first["w"] > second["x"] and first["y"] < second["y"] + second["h"] and first["y"] + first["h"] > second["y"]:
                    findings.append(f"ERROR: Page {page_no}, blocks {a + 1} and {b} overlap.")
    return findings
def validate(spec: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    pages = spec.get("pages", [])
    if not pages:
        warnings.append("ERROR: No pages were defined.")
        return warnings

    for idx, page in enumerate(pages, start=1):
        blocks = page.get("blocks", [])
        if not blocks:
            warnings.append(f"Page {idx}: no blocks defined.")
            continue
        bottoms = []
        for n, block in enumerate(blocks, start=1):
            try:
                x, y, w, h = (int(block[k]) for k in ("x", "y", "w", "h"))
            except (KeyError, TypeError, ValueError):
                warnings.append(f"Page {idx}, block {n}: invalid x/y/w/h.")
                continue
            if x < 0 or y < 0 or x + w > PAGE_W or y + h > PAGE_H:
                warnings.append(f"Page {idx}, block {n}: outside the 816 x 1056 page.")
            if y < 100:
                warnings.append(f"Page {idx}, block {n}: begins too close to the header.")
            if y + h > SAFE_BOTTOM:
                warnings.append(f"Page {idx}, block {n}: extends below the safe content bottom ({SAFE_BOTTOM}px).")
            bottoms.append(y + h)
        if bottoms and max(bottoms) < FILL_TARGET:
            warnings.append(
                f"Page {idx}: content stops at {max(bottoms)}px; extend it to at least {FILL_TARGET}px so the page feels full."
            )
    warnings.extend(validate_uniqueness_and_collisions(spec))
    return warnings


def render(spec: dict[str, Any]) -> str:
    set_title = e(spec.get("set_title", "Canva Planner Set"))
    footer_label = e(spec.get("footer_label", "Planner"))
    pages = []
    for idx, page in enumerate(spec.get("pages", []), start=1):
        theme = e(page.get("theme", "#b2c6b1"))
        title = e(page.get("title", f"PAGE {idx}"))
        subtitle = e(page.get("subtitle", ""))
        blocks = "".join(render_box(b) for b in page.get("blocks", []))
        label = e(page.get("label", page.get("title", f"Page {idx}")))
        pages.append(
            f'<section class="page" data-document-role="page" data-label="{label}" style="--theme:{theme}">'
            f'<div class="header"><div class="title">{title}</div><div class="subtitle">{subtitle}</div></div>'
            f'{blocks}'
            f'<div class="footer"><span>{footer_label}</span><span>{idx} of {len(spec.get("pages", []))}</span></div>'
            f'</section>'
        )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{set_title}</title><style>{CSS}</style></head><body>'
        + "".join(pages)
        + '</body></html>'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="Planner JSON specification")
    parser.add_argument("output", type=Path, help="Output HTML path")
    parser.add_argument("--validate-only", action="store_true", help="Validate without writing HTML")
    args = parser.parse_args()

    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Could not read spec: {exc}", file=sys.stderr)
        return 2

    warnings = validate(spec)
    for warning in warnings:
        print(warning, file=sys.stderr)
    if any(w.startswith("ERROR") for w in warnings):
        return 2
    if args.validate_only:
        return 1 if warnings else 0

    args.output.write_text(render(spec), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())




