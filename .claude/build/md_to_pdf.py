"""Convert ExamPrep_MD/*.md to skill-spec-compliant PDF using reportlab+matplotlib.

Implements the /summaryandexamprep skill's PDF technical requirements:
- Cover page (title, subject, exam context)
- Color-coded section bars per content type
- Beginning Key Notes / Body / Worked Examples / Practice / Answers / Revision / Reference
- Callout boxes for definitions, exam traps, examples
- LaTeX equations rendered via matplotlib mathtext (display + inline-fallback)
- Auto-fitted tables (no overflow)
- TTFont-embedded DejaVu fonts
- Practice questions labeled with marks/difficulty
- Revision cards in 2-column grid
- Reference sheet rendered as table

Usage:  python3 .claude/build/md_to_pdf.py <input.md> [output.pdf]
"""
from __future__ import annotations
import re
import sys
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from reportlab.platypus import (
    Paragraph, Spacer, PageBreak, NextPageTemplate, KeepTogether,
    Table, TableStyle, Image
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


# ── Inline transformations ──────────────────────────────────────────────
_DISP_MATH = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
_INLINE_MATH = re.compile(r"\$([^$\n]+?)\$")
_BOLD = re.compile(r"\*\*([^*]+?)\*\*")
_ITAL = re.compile(r"(?<!\*)\*([^*\n]+?)\*(?!\*)")
_CODE = re.compile(r"`([^`\n]+?)`")
_LINK = re.compile(r"\[([^\]]+?)\]\(([^)]+?)\)")


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline_math_to_text(expr: str) -> str:
    """Approximate inline LaTeX math → unicode + reportlab tags."""
    s = expr
    repl = {
        r"\beta": "β", r"\alpha": "α", r"\gamma": "γ", r"\delta": "δ",
        r"\sigma": "σ", r"\mu": "μ", r"\lambda": "λ", r"\theta": "θ",
        r"\varepsilon": "ε", r"\epsilon": "ε", r"\phi": "φ", r"\rho": "ρ",
        r"\sum": "Σ", r"\prod": "Π", r"\int": "∫",
        r"\to": "→", r"\rightarrow": "→", r"\leftarrow": "←", r"\Rightarrow": "⇒",
        r"\cdot": "·", r"\times": "×", r"\pm": "±", r"\div": "÷",
        r"\leq": "≤", r"\geq": "≥", r"\neq": "≠", r"\approx": "≈",
        r"\sim": "∼", r"\propto": "∝", r"\equiv": "≡",
        r"\infty": "∞", r"\partial": "∂", r"\nabla": "∇",
        r"\in": "∈", r"\notin": "∉", r"\subset": "⊂", r"\subseteq": "⊆",
        r"\cup": "∪", r"\cap": "∩", r"\emptyset": "∅",
        r"\sqrt": "√", r"\forall": "∀", r"\exists": "∃",
        r"\angle": "∠", r"\circ": "°",
        r"\mathbf": "", r"\mathrm": "", r"\text": "", r"\mathcal": "",
        r"\frac": "frac", r"\hat": "^", r"\bar": "¯", r"\tilde": "~",
        r"\;": " ", r"\,": " ", r"\!": "", r"\\": " ",
        r"\quad": "    ", r"\qquad": "        ",
        r"\langle": "⟨", r"\rangle": "⟩",
    }
    for k, v in repl.items():
        s = s.replace(k, v)
    s = re.sub(r"\\([a-zA-Z]+)", r"\1", s)  # strip remaining commands
    s = re.sub(r"_\{([^}]+)\}", r"<sub>\1</sub>", s)
    s = re.sub(r"\^\{([^}]+)\}", r"<sup>\1</sup>", s)
    s = re.sub(r"_([A-Za-z0-9+\-])", r"<sub>\1</sub>", s)
    s = re.sub(r"\^([A-Za-z0-9+\-])", r"<sup>\1</sup>", s)
    s = s.replace("{", "").replace("}", "")
    return f"<i>{s}</i>"


def md_inline(text: str) -> str:
    """Convert inline markdown to reportlab paragraph HTML."""
    chunks = []

    def _take(m):
        chunks.append(m.group(0))
        return f"\x00{len(chunks)-1}\x00"

    text = _CODE.sub(_take, text)
    text = _escape(text)
    for i, c in enumerate(chunks):
        text = text.replace(f"\x00{i}\x00",
                            f"<font face='Mono' size='9.5'>{_escape(c[1:-1])}</font>")
    text = _BOLD.sub(r"<b>\1</b>", text)
    text = _ITAL.sub(r"<i>\1</i>", text)
    text = _INLINE_MATH.sub(lambda m: _inline_math_to_text(m.group(1)), text)
    text = _LINK.sub(r"\1", text)
    return text


def strip_yaml(text: str) -> tuple[dict, str]:
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


# ── Block parser ─────────────────────────────────────────────────────────
def parse_md(md: str) -> list[tuple[str, dict]]:
    blocks: list[tuple[str, dict]] = []
    lines = md.splitlines()
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()

        if not s:
            i += 1
            continue

        # horizontal rule
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", s):
            blocks.append(("hr", {}))
            i += 1
            continue

        # fenced code
        if s.startswith("```"):
            fence = s[:3]
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith(fence):
                buf.append(lines[i])
                i += 1
            i += 1
            blocks.append(("code", {"text": "\n".join(buf)}))
            continue

        # heading
        if s.startswith("#"):
            m = re.match(r"^(#{1,6})\s+(.+)$", s)
            if m:
                blocks.append(("heading", {"level": len(m.group(1)),
                                            "text": m.group(2).strip()}))
                i += 1
                continue

        # display math
        if s.startswith("$$"):
            content = s[2:]
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

        # blockquote
        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").lstrip())
                i += 1
            blocks.append(("quote", {"text": " ".join(buf).strip()}))
            continue

        # bullet list
        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < n:
                ln = lines[i]
                bm = re.match(r"^(\s*)[-*]\s+(.*)$", ln)
                if not bm:
                    if not ln.strip():
                        i += 1
                        if i < n and not re.match(r"^\s*[-*]\s+", lines[i]):
                            break
                        continue
                    break
                items.append({"indent": len(bm.group(1)), "text": bm.group(2)})
                i += 1
            blocks.append(("ulist", {"items": items}))
            continue

        # ordered list
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < n:
                ln = lines[i]
                bm = re.match(r"^(\s*)\d+\.\s+(.*)$", ln)
                if not bm:
                    if not ln.strip():
                        i += 1
                        if i < n and not re.match(r"^\s*\d+\.\s+", lines[i]):
                            break
                        continue
                    break
                items.append({"indent": len(bm.group(1)), "text": bm.group(2)})
                i += 1
            blocks.append(("olist", {"items": items}))
            continue

        # pipe table
        if line.lstrip().startswith("|"):
            tbl = []
            while i < n and lines[i].lstrip().startswith("|"):
                row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                tbl.append(row)
                i += 1
            # need at least 2 rows (header + separator) OR 1 row that we treat as a stray
            if len(tbl) < 2:
                # not a real table; render rows as paragraphs
                for r in tbl:
                    blocks.append(("para", {"text": " | ".join(r)}))
                continue
            if all(re.fullmatch(r":?-+:?", c or "") for c in tbl[1]):
                aligns = []
                for c in tbl[1]:
                    if c.startswith(":") and c.endswith(":"):
                        aligns.append("C")
                    elif c.endswith(":"):
                        aligns.append("R")
                    else:
                        aligns.append("L")
                rows = [tbl[0]] + tbl[2:]
            else:
                aligns = ["L"] * len(tbl[0])
                rows = tbl
            # equalize row lengths
            ncols = max(len(r) for r in rows)
            rows = [r + [""] * (ncols - len(r)) for r in rows]
            blocks.append(("table", {"rows": rows, "aligns": aligns[:ncols]}))
            continue

        # paragraph
        buf = []
        while i < n:
            ln = lines[i]
            ls = ln.strip()
            if not ls:
                break
            if (ls.startswith("#") or ls.startswith("|") or ls.startswith(">")
                or ls.startswith("$$") or ls.startswith("```")
                or re.match(r"^\s*[-*]\s+", ln) or re.match(r"^\s*\d+\.\s+", ln)
                or re.fullmatch(r"-{3,}", ls)):
                break
            buf.append(ln)
            i += 1
        blocks.append(("para", {"text": " ".join(buf).strip()}))

    return blocks


# ── Section detection from heading text ─────────────────────────────────
def section_color_from_heading(text: str) -> tuple[HexColor, bool]:
    """Return (color, is_section_bar) based on the heading content."""
    low = text.lower()
    if any(x in low for x in ("key note", "study compass", "things you must")):
        return KEY_BLUE, True
    if any(x in low for x in ("worked", "example")):
        return EX_GREEN, True
    if any(x in low for x in ("practice question", "questions", "mock")):
        return PRAC_ORN, True
    if any(x in low for x in ("answer", "solution")):
        return ANS_TEAL, True
    if any(x in low for x in ("ending key", "revision", "cheat")):
        return REV_RED, True
    if "reference" in low and ("formula" in low or "algorithm" in low or "sheet" in low):
        return REF_INDIGO, True
    if re.match(r"^[\s§\d.]+", text):  # numbered sections
        return NAVY, True
    return NAVY, False


# ── Render ─────────────────────────────────────────────────────────────
def render_practice_question(text: str) -> Paragraph:
    """Format Q1 [Type · marks] heading specially."""
    m = re.match(r"\*\*?Q(\d+)\*?\*?\s*\[([^\]]+)\]\*?\*?\.?\s*(.*)", text)
    if m:
        qid, hdr, body = m.groups()
        return Paragraph(
            f"<b>Q{qid}</b> &nbsp; <font color='#B85C00'>[{hdr}]</font> &nbsp; {body}",
            S["PracBody"])
    return Paragraph(md_inline(text), S["Body"])


def render_answer_heading(text: str) -> Paragraph:
    """Format A1, A2 ... headings."""
    m = re.match(r"\*\*?A(\d+)\*?\*?\.?\s*(.*)", text)
    if m:
        aid, body = m.groups()
        return Paragraph(f"<b>A{aid}.</b> {md_inline(body)}", S["AnsBody"])
    return Paragraph(md_inline(text), S["Body"])


def render(blocks: list, story: list, ctx: dict):
    """Append rendered flowables to story.

    ctx tracks current section (for color + style choices).
    """
    for kind, data in blocks:
        if kind == "heading":
            lvl = data["level"]
            text = data["text"]
            if lvl == 1:
                continue  # skip body H1 — title on cover
            elif lvl == 2:
                color, _ = section_color_from_heading(text)
                story.append(Spacer(1, 0.3 * cm))
                story.append(section_bar(text, color))
                story.append(Spacer(1, 0.2 * cm))
                low = text.lower()
                ctx["section"] = (
                    "practice" if "practice" in low or "question" in low else
                    "answers" if "answer" in low else
                    "examples" if "worked" in low or "example" in low else
                    "revision" if "revision" in low or "ending" in low else
                    "reference" if "reference" in low else
                    "body"
                )
            elif lvl == 3:
                # Worked Example / Q heading
                if re.match(r"\s*Worked Example", text, re.I):
                    story.append(Spacer(1, 0.15 * cm))
                    story.append(Paragraph(f"<b>{md_inline(text)}</b>",
                                           S["ExTitle"]))
                else:
                    story.append(Paragraph(md_inline(text), S["H2"]))
            else:
                story.append(Paragraph(md_inline(text), S["H3"]))

        elif kind == "para":
            t = data["text"]
            # Detect "Q1 [..]" question line in practice section
            if ctx.get("section") == "practice" and re.match(r"\*?\*?Q\d+", t):
                story.append(KeepTogether([
                    render_practice_question(t),
                    Spacer(1, 0.1 * cm),
                ]))
            elif ctx.get("section") == "answers" and re.match(r"\*?\*?A\d+", t):
                story.append(KeepTogether([
                    render_answer_heading(t),
                    Spacer(1, 0.15 * cm),
                ]))
            else:
                story.append(Paragraph(md_inline(t), S["Body"]))

        elif kind == "ulist":
            for item in data["items"]:
                txt = md_inline(item["text"])
                indent = item["indent"]
                style = S["NestedBullet"] if indent >= 2 else S["Bullet"]
                story.append(Paragraph("• " + txt, style))

        elif kind == "olist":
            for n_, item in enumerate(data["items"], start=1):
                txt = md_inline(item["text"])
                story.append(Paragraph(f"{n_}. " + txt, S["Bullet"]))

        elif kind == "code":
            for line in data["text"].split("\n"):
                story.append(Paragraph(_escape(line) or "&nbsp;", S["Code"]))

        elif kind == "quote":
            text = data["text"]
            # Detect callout type: "**EXAM TRAP**", "**Definition**", etc.
            title = "ⓘ Note"
            title_style = S["DefTitle"]
            body_style = S["DefBody"]
            bg = DEF_BG
            border = DEF_PURP
            m = re.match(r"\*\*([^*]+)\*\*\s*[—:.\-]?\s*(.*)", text, re.S)
            if m:
                t_, rest = m.group(1), m.group(2)
                title = t_
                low = t_.lower()
                if "trap" in low or "warn" in low or "mistake" in low:
                    title_style = S["WarnTitle"]; body_style = S["WarnBody"]
                    bg = WARN_BG; border = WARN_RED
                elif "definition" in low or "analogy" in low or "intuition" in low:
                    title_style = S["DefTitle"]; body_style = S["DefBody"]
                    bg = DEF_BG; border = DEF_PURP
                elif "example" in low or "algorithm" in low:
                    title_style = S["ExTitle"]; body_style = S["ExBody"]
                    bg = EX_BG; border = EX_GREEN
                elif "key" in low or "important" in low or "matter" in low:
                    title_style = S["KeyTitle"]; body_style = S["KeyBody"]
                    bg = KEY_BG; border = KEY_BLUE
                text = rest if rest else text
            story.append(callout(title,
                                 [Paragraph(md_inline(text), body_style)],
                                 title_style=title_style, body_style=body_style,
                                 bg=bg, border=border))
            story.append(Spacer(1, 0.15 * cm))

        elif kind == "display_math":
            try:
                story.append(display_eq(data["latex"], fontsize=15))
            except Exception:
                story.append(Paragraph(
                    md_inline(f"${data['latex']}$"), S["Body"]))

        elif kind == "table":
            rows = data["rows"]
            aligns = data["aligns"] or ["L"] * len(rows[0])
            rendered = [[md_inline(c) for c in row] for row in rows]
            # Special handling for revision-card-like tables (2-col with mostly text)
            for flow in autofit_table(rendered, header=True, alignments=aligns):
                story.append(flow)

        elif kind == "hr":
            story.append(Spacer(1, 0.2 * cm))
            story.append(hr())
            story.append(Spacer(1, 0.2 * cm))


# ── TOC builder ─────────────────────────────────────────────────────────
def build_toc(blocks: list) -> list:
    """Generate TOC entries from H2 headings."""
    entries = []
    for kind, data in blocks:
        if kind == "heading" and data["level"] == 2:
            entries.append(data["text"])
    return entries


def render_toc(entries: list[str]) -> list:
    flow = []
    flow.append(Paragraph("Contents", S["TocTitle"]))
    flow.append(hr())
    flow.append(Spacer(1, 0.3 * cm))
    for i, e in enumerate(entries, start=1):
        flow.append(Paragraph(f"<b>{i}.</b> &nbsp; {md_inline(e)}", S["TocItem"]))
    flow.append(PageBreak())
    return flow


# ── Cover topics extraction ─────────────────────────────────────────────
def extract_topics(blocks: list) -> list[str]:
    """Pull short topic bullets from the first ulist after H1/intro."""
    topics: list[str] = []
    seen_h1 = False
    for kind, data in blocks:
        if kind == "heading" and data["level"] == 1:
            seen_h1 = True
            continue
        if kind == "ulist":
            for it in data["items"]:
                t = it["text"]
                # strip markdown formatting
                t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
                t = re.sub(r"\*(.+?)\*", r"\1", t)
                t = re.sub(r"`([^`]+)`", r"\1", t)
                t = re.sub(r"\$([^$]+)\$",
                           lambda m: re.sub(r"\\([a-zA-Z]+)", r"\1", m.group(1)),
                           t)
                t = t.split(".")[0].strip()
                if 5 < len(t) < 110 and len(topics) < 8:
                    topics.append(t)
            if topics:
                return topics
    return topics or ["Comprehensive coverage of this week's BDA syllabus"]


# ── Main ─────────────────────────────────────────────────────────────────
def build_pdf(md_path: str, out_path: str):
    md_text = Path(md_path).read_text(encoding="utf-8")
    meta, body = strip_yaml(md_text)
    title = str(meta.get("title", Path(md_path).stem))
    subtitle = str(meta.get("subtitle", "BDA Final Exam Prep"))
    course = str(meta.get("course", "CS-404 Big Data Analytics"))
    exam = str(meta.get("exam", "Final ~ 2026-05-16"))
    week_label = str(meta.get("week_label", subtitle))

    blocks = parse_md(body)

    doc = make_doc(
        out_path=out_path,
        title=title,
        header_text=title,
        footer_text=f"{course} · Final Exam Prep · Comprehensive Tutor PDF",
    )

    story = []
    # cover page
    topics = extract_topics(blocks)
    story.extend(cover_block(
        title=title,
        subtitle=subtitle,
        week_label=week_label,
        topics=topics,
        styles=S,
        exam_date=exam,
    ))
    story.append(NextPageTemplate("main"))
    story.append(PageBreak())

    # TOC
    toc_entries = build_toc(blocks)
    if toc_entries:
        story.extend(render_toc(toc_entries))

    # body — drop leading H1
    if blocks and blocks[0][0] == "heading" and blocks[0][1]["level"] == 1:
        blocks = blocks[1:]

    ctx = {"section": "body"}
    render(blocks, story, ctx)

    doc.build(story)
    p = Path(out_path)
    print(f"  built  {p.name:50s}  {p.stat().st_size/1024:.1f} KB")


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
