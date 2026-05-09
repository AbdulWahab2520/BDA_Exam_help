"""Convert a single ExamPrep_MD/*.md file to a polished PDF using reportlab.

Usage:  python3 .claude/build/md_to_pdf.py ExamPrep_MD/W13-14_Clustering.md

Parses a subset of GitHub-flavored markdown:
- YAML front matter (title, subtitle, week_label, ...)
- # / ## / ### headings (## treated as section bars)
- paragraphs, bold (**...**), italic (*...*), inline code (`...`), inline math ($...$)
- bullet lists (- or *), numbered lists (1.)
- pipe tables (| col | col |)
- fenced code blocks ```...```
- block quotes (> ...) → renders as callout box
- horizontal rule (---)
- display math ($$...$$) → matplotlib-rendered image
"""
from __future__ import annotations
import re
import sys
import io
import yaml
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from reportlab.platypus import (
    Paragraph, Spacer, PageBreak, NextPageTemplate, KeepTogether, Table, TableStyle, Image
)
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

from bda_style import (
    build_stylesheet, make_doc, cover_block, section_bar, hr,
    callout, autofit_table, eq, display_eq, save_fig, fig_image,
    NAVY, GOLD, KEY_BLUE, KEY_BG, EX_GREEN, EX_BG, DEF_PURP, DEF_BG,
    WARN_RED, WARN_BG, PRAC_ORN, PRAC_BG, ANS_TEAL, ANS_BG,
    REV_RED, REV_BG, REF_INDIGO, REF_BG, USABLE_W,
)


S = build_stylesheet()


# ── inline transformations ──────────────────────────────────────────────
_DISP_MATH = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
_INLINE_MATH = re.compile(r"\$([^$\n]+?)\$")
_BOLD = re.compile(r"\*\*([^*]+?)\*\*")
_ITAL = re.compile(r"(?<!\*)\*([^*\n]+?)\*(?!\*)")
_CODE = re.compile(r"`([^`\n]+?)`")
_LINK = re.compile(r"\[([^\]]+?)\]\(([^)]+?)\)")


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _md_inline_to_html(text: str) -> str:
    """Convert inline markdown to reportlab paragraph HTML.
    Math is replaced with a placeholder and re-injected as inline images later
    — but here, we approximate inline math by italic monospace rendering since
    full inline math image embedding is fiddly in reportlab paragraphs.
    """
    # protect inline code first (no further replacement inside)
    chunks = []

    def _take(m):
        chunks.append(m.group(0))
        return f"{len(chunks)-1}"

    text = _CODE.sub(_take, text)

    # escape HTML-significant chars
    text = _escape(text)

    # restore code chunks
    for i, c in enumerate(chunks):
        text = text.replace(f"{i}",
                            f"<font face='Mono' size='10'>{_escape(c[1:-1])}</font>")

    # bold, italic
    text = _BOLD.sub(r"<b>\1</b>", text)
    text = _ITAL.sub(r"<i>\1</i>", text)

    # inline math — render as italic Serif w/ approximations
    def _inline_math_render(m):
        expr = m.group(1)
        # Map common LaTeX to plaintext-with-styling that reportlab can show
        s = expr
        s = s.replace(r"\beta", "β").replace(r"\alpha", "α").replace(r"\gamma", "γ")
        s = s.replace(r"\sigma", "σ").replace(r"\mu", "μ").replace(r"\lambda", "λ")
        s = s.replace(r"\delta", "δ").replace(r"\varepsilon", "ε").replace(r"\epsilon", "ε")
        s = s.replace(r"\sum", "Σ").replace(r"\prod", "Π").replace(r"\int", "∫")
        s = s.replace(r"\to", "→").replace(r"\leftarrow", "←")
        s = s.replace(r"\cdot", "·").replace(r"\times", "×").replace(r"\pm", "±")
        s = s.replace(r"\leq", "≤").replace(r"\geq", "≥").replace(r"\neq", "≠")
        s = s.replace(r"\approx", "≈").replace(r"\sim", "∼").replace(r"\propto", "∝")
        s = s.replace(r"\infty", "∞").replace(r"\partial", "∂")
        s = s.replace(r"\in", "∈").replace(r"\notin", "∉").replace(r"\subset", "⊂")
        s = s.replace(r"\cup", "∪").replace(r"\cap", "∩").replace(r"\emptyset", "∅")
        s = s.replace(r"\sqrt", "√").replace(r"\mathbf", "").replace(r"\mathrm", "")
        s = s.replace(r"\frac", "frac").replace(r"\text", "")
        s = re.sub(r"\\([a-zA-Z]+)", r"\1", s)  # strip remaining commands
        # subscripts and superscripts (only single-char or {…} groups)
        s = re.sub(r"_\{([^}]+)\}", r"<sub>\1</sub>", s)
        s = re.sub(r"\^\{([^}]+)\}", r"<sup>\1</sup>", s)
        s = re.sub(r"_([A-Za-z0-9])", r"<sub>\1</sub>", s)
        s = re.sub(r"\^([A-Za-z0-9])", r"<sup>\1</sup>", s)
        s = s.replace("{", "").replace("}", "")
        return f"<i>{s}</i>"

    text = _INLINE_MATH.sub(_inline_math_render, text)

    # links (we keep visible label only)
    text = _LINK.sub(r"\1", text)

    return text


def _strip_yaml_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, parts[2].lstrip("\n")


# ── Block-level parser ───────────────────────────────────────────────────
def parse_md(md: str) -> list[tuple[str, dict]]:
    """Return a list of (kind, data) blocks."""
    blocks: list[tuple[str, dict]] = []
    lines = md.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # blank line
        if not stripped:
            i += 1
            continue

        # horizontal rule
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", stripped):
            blocks.append(("hr", {}))
            i += 1
            continue

        # fenced code block
        if stripped.startswith("```"):
            fence = stripped[:3]
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith(fence):
                buf.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            blocks.append(("code", {"text": "\n".join(buf)}))
            continue

        # headings
        if stripped.startswith("#"):
            m = re.match(r"^(#{1,4})\s+(.+)$", stripped)
            if m:
                level = len(m.group(1))
                blocks.append(("heading", {"level": level, "text": m.group(2).strip()}))
                i += 1
                continue

        # display math
        if stripped.startswith("$$"):
            # could be one-line $$...$$ or multi-line
            content = stripped[2:]
            if content.endswith("$$") and len(content) > 2:
                blocks.append(("display_math", {"latex": content[:-2].strip()}))
                i += 1
                continue
            buf = [content] if content else []
            i += 1
            while i < n and "$$" not in lines[i]:
                buf.append(lines[i])
                i += 1
            if i < n:
                tail = lines[i].split("$$", 1)[0]
                if tail:
                    buf.append(tail)
                i += 1
            blocks.append(("display_math", {"latex": " ".join(buf).strip()}))
            continue

        # block quote / callout (consecutive >-lines)
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").lstrip())
                i += 1
            blocks.append(("quote", {"lines": buf}))
            continue

        # bullet list (- or *)
        if re.match(r"^[\s]*[-*]\s+", line):
            items = []
            while i < n:
                ln = lines[i]
                bm = re.match(r"^([\s]*)[-*]\s+(.*)$", ln)
                if not bm:
                    if not ln.strip():
                        i += 1
                        if i < n and not re.match(r"^[\s]*[-*]\s+", lines[i]):
                            break
                        else:
                            continue
                    break
                indent = len(bm.group(1))
                items.append({"indent": indent, "text": bm.group(2)})
                i += 1
            blocks.append(("ulist", {"items": items}))
            continue

        # numbered list (1. )
        if re.match(r"^[\s]*\d+\.\s+", line):
            items = []
            while i < n:
                ln = lines[i]
                bm = re.match(r"^([\s]*)\d+\.\s+(.*)$", ln)
                if not bm:
                    if not ln.strip():
                        i += 1
                        if i < n and not re.match(r"^[\s]*\d+\.\s+", lines[i]):
                            break
                        else:
                            continue
                    break
                items.append({"indent": len(bm.group(1)), "text": bm.group(2)})
                i += 1
            blocks.append(("olist", {"items": items}))
            continue

        # pipe table (| ... | ... |)
        if line.lstrip().startswith("|"):
            tbl = []
            while i < n and lines[i].lstrip().startswith("|"):
                row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                tbl.append(row)
                i += 1
            # second row is alignment row like | --- | :---: | ---: |
            if len(tbl) >= 2 and all(re.fullmatch(r":?-+:?", c) for c in tbl[1]):
                aligns = []
                for c in tbl[1]:
                    if c.startswith(":") and c.endswith(":"):
                        aligns.append("C")
                    elif c.endswith(":"):
                        aligns.append("R")
                    else:
                        aligns.append("L")
                blocks.append(("table", {"rows": [tbl[0]] + tbl[2:], "aligns": aligns}))
            else:
                blocks.append(("table", {"rows": tbl, "aligns": None}))
            continue

        # paragraph (collect contiguous non-blank lines that don't start a new block)
        buf = []
        while i < n:
            ln = lines[i]
            ls = ln.strip()
            if not ls:
                break
            if ls.startswith("#") or ls.startswith("|") or ls.startswith(">") \
               or ls.startswith("$$") or ls.startswith("```") \
               or re.match(r"^[\s]*[-*]\s+", ln) or re.match(r"^[\s]*\d+\.\s+", ln) \
               or re.fullmatch(r"-{3,}", ls):
                break
            buf.append(ln)
            i += 1
        blocks.append(("para", {"text": " ".join(buf).strip()}))

    return blocks


# ── Render blocks → reportlab flowables ─────────────────────────────────
def render_blocks(blocks: list, story: list):
    """Append rendered flowables for each block to story."""
    for kind, data in blocks:
        if kind == "heading":
            lvl = data["level"]
            txt = _md_inline_to_html(data["text"])
            if lvl == 1:
                # Skip H1 inside body (already on cover)
                story.append(Spacer(1, 0.2*cm))
                story.append(Paragraph(txt, S["H1"]))
            elif lvl == 2:
                # Use a section bar for ## headings (these are §1, §2 style)
                story.append(Spacer(1, 0.3*cm))
                # detect a §-prefix and choose colour
                color = NAVY
                low = data["text"].lower()
                if "key note" in low or "study compass" in low:
                    color = KEY_BLUE
                elif "worked" in low or "example" in low:
                    color = EX_GREEN
                elif "practice" in low or "question" in low:
                    color = PRAC_ORN
                elif "answer" in low:
                    color = ANS_TEAL
                elif "revision" in low or "ending key" in low:
                    color = REV_RED
                elif "reference" in low or "formula" in low and "algorithm" in low:
                    color = REF_INDIGO
                story.append(section_bar(data["text"], color))
                story.append(Spacer(1, 0.2*cm))
            elif lvl == 3:
                story.append(Paragraph(txt, S["H2"]))
            else:
                story.append(Paragraph(txt, S["H3"]))

        elif kind == "para":
            txt = _md_inline_to_html(data["text"])
            story.append(Paragraph(txt, S["Body"]))

        elif kind == "ulist":
            for item in data["items"]:
                indent = item["indent"]
                txt = _md_inline_to_html(item["text"])
                style = S["NestedBullet"] if indent >= 2 else S["Bullet"]
                story.append(Paragraph("• " + txt, style))

        elif kind == "olist":
            for n, item in enumerate(data["items"], start=1):
                txt = _md_inline_to_html(item["text"])
                story.append(Paragraph(f"{n}. " + txt, S["Bullet"]))

        elif kind == "code":
            code_style = ParagraphStyle("Code", parent=S["Code"],
                                        fontName="Mono", fontSize=9, leading=12)
            for line in data["text"].split("\n"):
                story.append(Paragraph(_escape(line) or "&nbsp;", code_style))

        elif kind == "quote":
            text = " ".join(data["lines"])
            html = _md_inline_to_html(text)
            box = callout("ⓘ NOTE", [Paragraph(html, S["DefBody"])],
                          title_style=S["DefTitle"], body_style=S["DefBody"],
                          bg=DEF_BG, border=DEF_PURP)
            story.append(box)

        elif kind == "display_math":
            try:
                story.append(display_eq(data["latex"], fontsize=15))
            except Exception:
                # fallback to raw text if mathtext can't parse
                story.append(Paragraph(f"<i>{_escape(data['latex'])}</i>", S["Body"]))

        elif kind == "table":
            rows = data["rows"]
            aligns = data["aligns"] or ["L"] * (len(rows[0]) if rows else 1)
            # convert each cell's MD inline syntax to HTML
            rendered = []
            for r, row in enumerate(rows):
                rendered.append([_md_inline_to_html(c) for c in row])
            for flow in autofit_table(rendered, header=True, alignments=aligns):
                story.append(flow)

        elif kind == "hr":
            story.append(Spacer(1, 0.2*cm))
            story.append(hr())
            story.append(Spacer(1, 0.2*cm))


# ── Main ─────────────────────────────────────────────────────────────────
def build_pdf(md_path: str, out_path: str):
    md_text = Path(md_path).read_text(encoding="utf-8")
    meta, body = _strip_yaml_front_matter(md_text)
    title = meta.get("title", Path(md_path).stem)
    subtitle = meta.get("subtitle", "BDA Final Exam Prep")
    course = meta.get("course", "CS-404 Big Data Analytics")
    exam = meta.get("exam", "")
    week_label = meta.get("week_label", subtitle)

    # Extract topics for cover from the H1 + first key-notes bullets if available
    blocks = parse_md(body)
    topics = []
    for kind, data in blocks:
        if kind == "ulist" and len(topics) < 8:
            for it in data["items"]:
                t = re.sub(r"\*\*(.+?)\*\*", r"\1", it["text"])
                t = re.sub(r"`([^`]+)`", r"\1", t)
                t = t.split(".")[0]
                if 5 < len(t) < 130:
                    topics.append(t)
                if len(topics) >= 7:
                    break
            if len(topics) >= 7:
                break

    if not topics:
        topics = ["Comprehensive prep for this week's BDA topic"]

    doc = make_doc(
        out_path=out_path,
        title=str(title),
        header_text=str(title),
        footer_text=f"{course} · Final Exam Prep · Comprehensive Tutor PDF",
    )
    story = []
    story.extend(cover_block(
        title=str(title),
        subtitle=str(subtitle),
        week_label=str(week_label),
        topics=topics,
        styles=S,
        exam_date=str(exam) or "Final ~ 2026-05-16",
    ))
    story.append(NextPageTemplate("main"))
    story.append(PageBreak())

    # Drop the leading H1 (title) from body if present, since we put it on the cover
    if blocks and blocks[0][0] == "heading" and blocks[0][1]["level"] == 1:
        blocks = blocks[1:]

    render_blocks(blocks, story)
    doc.build(story)
    p = Path(out_path)
    print(f"  built: {p}  —  {p.stat().st_size/1024:.1f} KB")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 md_to_pdf.py <input.md> [output.pdf]")
        sys.exit(1)
    src = sys.argv[1]
    if len(sys.argv) >= 3:
        dst = sys.argv[2]
    else:
        stem = Path(src).stem
        dst = f"ExamPrep_PDFs/BDA_{stem}_ExamPrep.pdf"
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    build_pdf(src, dst)
