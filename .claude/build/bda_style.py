"""Reusable style + helpers for BDA exam-prep PDFs.

Loaded by every per-week builder so font registration, palette, paragraph styles,
auto-fit tables, callouts and matplotlib mathtext rendering live in one place.
"""
from __future__ import annotations

import io
import os
import re
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, Flowable, NextPageTemplate
)


# ─── Palette ──────────────────────────────────────────────────────────────
NAVY      = HexColor("#0B2540")  # body headers
GOLD      = HexColor("#C8A24B")  # accent
INK       = HexColor("#1A1A1A")  # body text
SOFT_INK  = HexColor("#3A3A3A")
SUBTLE    = HexColor("#6B6B6B")
LIGHT_BG  = HexColor("#F4F1EA")  # callout cream
KEY_BLUE  = HexColor("#1F4E79")  # study compass
KEY_BG    = HexColor("#E8F0F8")
EX_GREEN  = HexColor("#1B5E20")  # worked example
EX_BG     = HexColor("#E8F4EA")
DEF_PURP  = HexColor("#4A148C")  # definition callout
DEF_BG    = HexColor("#F1E6F8")
WARN_RED  = HexColor("#B22234")  # exam trap
WARN_BG   = HexColor("#FCE7E9")
PRAC_ORN  = HexColor("#B85C00")  # practice
PRAC_BG   = HexColor("#FFF1E0")
ANS_TEAL  = HexColor("#0E5C5C")  # answer
ANS_BG    = HexColor("#E1F2F2")
REV_RED   = HexColor("#7B1E2B")  # revision sheet
REV_BG    = HexColor("#FBEEEE")
REF_INDIGO= HexColor("#283593")  # reference sheet
REF_BG    = HexColor("#E8EAF6")

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm
USABLE_W = PAGE_W - 2 * MARGIN


# ─── Fonts ────────────────────────────────────────────────────────────────
def register_fonts() -> dict:
    """Register DejaVu (sans + mono) from matplotlib's bundled fonts."""
    mpl_font = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    candidates = {
        "BodyRegular": mpl_font / "DejaVuSans.ttf",
        "BodyBold":    mpl_font / "DejaVuSans-Bold.ttf",
        "BodyItalic":  mpl_font / "DejaVuSans-Oblique.ttf",
        "BodyBoldItalic": mpl_font / "DejaVuSans-BoldOblique.ttf",
        "Mono":        mpl_font / "DejaVuSansMono.ttf",
        "MonoBold":    mpl_font / "DejaVuSansMono-Bold.ttf",
        "Serif":       mpl_font / "DejaVuSerif.ttf",
        "SerifBold":   mpl_font / "DejaVuSerif-Bold.ttf",
        "SerifItalic": mpl_font / "DejaVuSerif-Italic.ttf",
    }
    for name, path in candidates.items():
        if path.exists() and name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, str(path)))
    pdfmetrics.registerFontFamily(
        "BodyRegular",
        normal="BodyRegular", bold="BodyBold",
        italic="BodyItalic", boldItalic="BodyBoldItalic",
    )
    return candidates


# ─── Stylesheet ───────────────────────────────────────────────────────────
def build_stylesheet() -> dict:
    register_fonts()
    s = {}

    s["CoverTitle"] = ParagraphStyle(
        "CoverTitle", fontName="SerifBold", fontSize=30, leading=36,
        alignment=TA_CENTER, textColor=NAVY, spaceAfter=10,
    )
    s["CoverSubtitle"] = ParagraphStyle(
        "CoverSubtitle", fontName="BodyRegular", fontSize=15, leading=20,
        alignment=TA_CENTER, textColor=GOLD, spaceAfter=6,
    )
    s["CoverMeta"] = ParagraphStyle(
        "CoverMeta", fontName="BodyItalic", fontSize=11, leading=15,
        alignment=TA_CENTER, textColor=SUBTLE,
    )
    s["TocTitle"] = ParagraphStyle(
        "TocTitle", fontName="SerifBold", fontSize=20, leading=26,
        alignment=TA_LEFT, textColor=NAVY, spaceAfter=8,
    )
    s["TocItem"] = ParagraphStyle(
        "TocItem", fontName="BodyRegular", fontSize=11, leading=16,
        alignment=TA_LEFT, textColor=INK, leftIndent=4,
    )
    s["TocItemSub"] = ParagraphStyle(
        "TocItemSub", fontName="BodyRegular", fontSize=10, leading=14,
        alignment=TA_LEFT, textColor=SOFT_INK, leftIndent=22,
    )

    s["H1"] = ParagraphStyle(
        "H1", fontName="SerifBold", fontSize=22, leading=28,
        alignment=TA_LEFT, textColor=NAVY, spaceBefore=14, spaceAfter=10,
    )
    s["H2"] = ParagraphStyle(
        "H2", fontName="SerifBold", fontSize=15, leading=20,
        alignment=TA_LEFT, textColor=NAVY, spaceBefore=12, spaceAfter=6,
    )
    s["H3"] = ParagraphStyle(
        "H3", fontName="BodyBold", fontSize=12, leading=16,
        alignment=TA_LEFT, textColor=NAVY, spaceBefore=8, spaceAfter=4,
    )
    s["Body"] = ParagraphStyle(
        "Body", fontName="BodyRegular", fontSize=10.5, leading=15,
        alignment=TA_JUSTIFY, textColor=INK, spaceAfter=6,
    )
    s["BodyTight"] = ParagraphStyle(
        "BodyTight", fontName="BodyRegular", fontSize=10.5, leading=14,
        alignment=TA_JUSTIFY, textColor=INK, spaceAfter=2,
    )
    s["Bullet"] = ParagraphStyle(
        "Bullet", parent=s["Body"], leftIndent=14, bulletIndent=4,
        spaceAfter=3, alignment=TA_LEFT,
    )
    s["NestedBullet"] = ParagraphStyle(
        "NestedBullet", parent=s["Bullet"], leftIndent=28, bulletIndent=18,
        fontSize=10, leading=14,
    )
    s["Caption"] = ParagraphStyle(
        "Caption", fontName="BodyItalic", fontSize=9.5, leading=12,
        alignment=TA_CENTER, textColor=SUBTLE, spaceBefore=2, spaceAfter=8,
    )
    s["Code"] = ParagraphStyle(
        "Code", fontName="Mono", fontSize=9, leading=12, textColor=INK,
        backColor=HexColor("#F2F2F2"), borderPadding=4, leftIndent=4,
    )

    # Callout body styles (used inside framed boxes)
    s["KeyTitle"] = ParagraphStyle(
        "KeyTitle", fontName="BodyBold", fontSize=11, leading=14,
        textColor=KEY_BLUE, spaceAfter=4,
    )
    s["KeyBody"] = ParagraphStyle(
        "KeyBody", fontName="BodyRegular", fontSize=10.5, leading=14,
        textColor=INK,
    )
    s["DefTitle"] = ParagraphStyle(
        "DefTitle", fontName="BodyBold", fontSize=11, leading=14,
        textColor=DEF_PURP, spaceAfter=3,
    )
    s["DefBody"] = ParagraphStyle(
        "DefBody", fontName="BodyRegular", fontSize=10.5, leading=14,
        textColor=INK,
    )
    s["ExTitle"] = ParagraphStyle(
        "ExTitle", fontName="BodyBold", fontSize=11, leading=14,
        textColor=EX_GREEN, spaceAfter=4,
    )
    s["ExBody"] = ParagraphStyle(
        "ExBody", fontName="BodyRegular", fontSize=10.5, leading=14,
        textColor=INK, alignment=TA_LEFT,
    )
    s["WarnTitle"] = ParagraphStyle(
        "WarnTitle", fontName="BodyBold", fontSize=11, leading=14,
        textColor=WARN_RED, spaceAfter=3,
    )
    s["WarnBody"] = ParagraphStyle(
        "WarnBody", fontName="BodyRegular", fontSize=10.5, leading=14,
        textColor=INK,
    )
    s["PracTitle"] = ParagraphStyle(
        "PracTitle", fontName="BodyBold", fontSize=11.5, leading=15,
        textColor=PRAC_ORN, spaceBefore=8, spaceAfter=2,
    )
    s["PracBody"] = ParagraphStyle(
        "PracBody", fontName="BodyRegular", fontSize=10.5, leading=14,
        textColor=INK, alignment=TA_LEFT, spaceAfter=4,
    )
    s["AnsTitle"] = ParagraphStyle(
        "AnsTitle", fontName="BodyBold", fontSize=11.5, leading=15,
        textColor=ANS_TEAL, spaceBefore=8, spaceAfter=2,
    )
    s["AnsBody"] = ParagraphStyle(
        "AnsBody", fontName="BodyRegular", fontSize=10.5, leading=14.5,
        textColor=INK, alignment=TA_LEFT, spaceAfter=4,
    )
    s["RevTitle"] = ParagraphStyle(
        "RevTitle", fontName="BodyBold", fontSize=11, leading=14,
        textColor=REV_RED, spaceAfter=3,
    )
    s["RevBody"] = ParagraphStyle(
        "RevBody", fontName="BodyRegular", fontSize=10, leading=13.5,
        textColor=INK, alignment=TA_LEFT,
    )
    s["RefTitle"] = ParagraphStyle(
        "RefTitle", fontName="BodyBold", fontSize=11, leading=14,
        textColor=REF_INDIGO,
    )
    s["RefBody"] = ParagraphStyle(
        "RefBody", fontName="BodyRegular", fontSize=10, leading=13.5,
        textColor=INK,
    )
    return s


# ─── Equation rendering via matplotlib mathtext ──────────────────────────
_EQ_DIR = Path(".claude/build/_eqcache")
_EQ_DIR.mkdir(parents=True, exist_ok=True)

def eq(latex: str, fontsize: int = 14, dpi: int = 220, color: str = "#101010") -> Image:
    """Render a LaTeX expression to PNG via matplotlib mathtext, return Image flowable."""
    safe = re.sub(r"[^A-Za-z0-9]", "_", latex)[:90]
    out = _EQ_DIR / f"{safe}_{fontsize}.png"
    if not out.exists():
        fig = plt.figure(figsize=(0.01, 0.01))
        text = fig.text(0, 0, f"${latex}$", fontsize=fontsize, color=color)
        fig.canvas.draw()
        bbox = text.get_window_extent()
        w_in = bbox.width / fig.dpi
        h_in = bbox.height / fig.dpi
        fig.set_size_inches(w_in + 0.05, h_in + 0.05)
        fig.savefig(out, dpi=dpi, bbox_inches="tight",
                    transparent=True, pad_inches=0.02)
        plt.close(fig)
    img = Image(str(out))
    # scale to natural size at the document DPI
    px_w, px_h = img.imageWidth, img.imageHeight
    img.drawWidth = (px_w / dpi) * 72
    img.drawHeight = (px_h / dpi) * 72
    return img


def display_eq(latex: str, fontsize: int = 16) -> Table:
    """A centered, padded equation block."""
    e = eq(latex, fontsize=fontsize)
    t = Table([[e]], colWidths=[USABLE_W])
    t.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))
    return t


# ─── Generic figure helper ───────────────────────────────────────────────
_FIG_DIR = Path(".claude/build/_figcache")
_FIG_DIR.mkdir(parents=True, exist_ok=True)

def save_fig(fig, name: str, dpi: int = 160) -> str:
    out = _FIG_DIR / f"{name}.png"
    fig.savefig(out, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return str(out)


def fig_image(path: str, max_w_cm: float = 14.0, max_h_cm: float = 10.0) -> Image:
    img = Image(path)
    pxw, pxh = img.imageWidth, img.imageHeight
    aspect = pxh / pxw
    target_w = max_w_cm * cm
    target_h = target_w * aspect
    if target_h > max_h_cm * cm:
        target_h = max_h_cm * cm
        target_w = target_h / aspect
    img.drawWidth = target_w
    img.drawHeight = target_h
    return img


# ─── Callout box ─────────────────────────────────────────────────────────
def callout(title: str, body_paragraphs: list, *,
            title_style: ParagraphStyle, body_style: ParagraphStyle,
            bg: HexColor, border: HexColor) -> Table:
    """Produce a framed callout flowable. body_paragraphs is a list of
    Paragraph/Image/Table flowables that already exist."""
    title_p = Paragraph(title, title_style)
    inner = [title_p] + body_paragraphs
    # Wrap each body element row-wise inside the table
    rows = [[item] for item in inner]
    tbl = Table(rows, colWidths=[USABLE_W - 14])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("BOX", (0,0), (-1,-1), 0.8, border),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    return tbl


# ─── Auto-sized table ────────────────────────────────────────────────────
def autofit_table(data, *, header: bool = True, header_bg=NAVY,
                  header_fg=colors.white, body_fg=INK,
                  body_font="BodyRegular", body_size=10,
                  caption: str | None = None, caption_style=None,
                  alignments: list[str] | None = None) -> list:
    """Build a Table that auto-sizes columns to content, allowing wrapping.
    Each cell may be a string or a Paragraph."""
    if not data:
        return []
    cols = max(len(r) for r in data)
    # Equalize row lengths
    data = [list(r) + [""] * (cols - len(r)) for r in data]
    # Estimate each cell's text length (paragraph height grows automatically)
    col_widths = [0.0] * cols
    for r, row in enumerate(data):
        for c, cell in enumerate(row):
            if isinstance(cell, Paragraph):
                # ask reportlab to wrap at infinity to measure natural width
                w, _ = cell.wrap(USABLE_W, 1000)
                col_widths[c] = max(col_widths[c], min(w, USABLE_W * 0.55))
            else:
                txt = str(cell)
                # rough char width estimate at 6.2 pt per char for size 10
                est = (max((len(line) for line in txt.splitlines()), default=0) + 1) * 6.2
                col_widths[c] = max(col_widths[c], est)
    # Add padding allowance per column
    col_widths = [max(w + 14, 30) for w in col_widths]  # min 30pt per col
    total = sum(col_widths)
    if total > USABLE_W:
        # scale down proportionally but enforce min width per column
        min_col_w = 30  # don't let a column shrink below 30pt
        # start with scaled widths
        scale = USABLE_W / total
        scaled = [max(w * scale, min_col_w) for w in col_widths]
        # if min-clamping pushed total over USABLE_W, shrink the largest cols only
        excess = sum(scaled) - USABLE_W
        if excess > 0:
            # iteratively trim from biggest cols until we fit
            for _ in range(40):
                idx = max(range(len(scaled)), key=lambda i: scaled[i])
                if scaled[idx] - 1 < min_col_w:
                    break
                scaled[idx] -= excess / max(1, len(scaled))
                excess = sum(scaled) - USABLE_W
                if excess <= 0:
                    break
        col_widths = scaled
    elif total < USABLE_W * 0.6:
        extra = (USABLE_W * 0.7 - total) / cols
        col_widths = [w + extra for w in col_widths]
    # final safety: ensure all >= min and total <= USABLE_W
    col_widths = [max(w, 30) for w in col_widths]
    if sum(col_widths) > USABLE_W:
        scale = USABLE_W / sum(col_widths)
        col_widths = [w * scale for w in col_widths]

    # Convert plain strings to Paragraphs so they wrap inside cells
    P_body = ParagraphStyle("CellBody", fontName=body_font, fontSize=body_size,
                            leading=body_size + 3, textColor=body_fg, alignment=TA_LEFT)
    P_head = ParagraphStyle("CellHead", fontName="BodyBold", fontSize=body_size,
                            leading=body_size + 3, textColor=header_fg, alignment=TA_CENTER)
    new_data = []
    for r, row in enumerate(data):
        new_row = []
        for c, cell in enumerate(row):
            if isinstance(cell, Paragraph) or isinstance(cell, Image):
                new_row.append(cell)
            else:
                style = P_head if (header and r == 0) else P_body
                new_row.append(Paragraph(str(cell).replace("\n", "<br/>"), style))
        new_data.append(new_row)

    tbl = Table(new_data, colWidths=col_widths, repeatRows=1 if header else 0)
    ts = [
        ("GRID", (0,0), (-1,-1), 0.4, HexColor("#C0C0C0")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]
    if header:
        ts += [
            ("BACKGROUND", (0,0), (-1,0), header_bg),
            ("LINEBELOW", (0,0), (-1,0), 0.8, HexColor("#202020")),
        ]
    if alignments:
        for c, a in enumerate(alignments):
            ts.append(("ALIGN", (c,0), (c,-1),
                      {"L":"LEFT","C":"CENTER","R":"RIGHT"}[a.upper()]))
    tbl.setStyle(TableStyle(ts))
    flow = [tbl]
    if caption:
        flow.append(Spacer(1, 2))
        flow.append(Paragraph(f"<i>{caption}</i>",
                              caption_style or ParagraphStyle(
                                  "Cap", fontName="BodyItalic", fontSize=9.2,
                                  alignment=TA_CENTER, textColor=SUBTLE)))
        flow.append(Spacer(1, 6))
    return flow


# ─── Page templates with header/footer ───────────────────────────────────
class HFPageTemplate(PageTemplate):
    def __init__(self, id, frames, header_text="", footer_text="",
                 page_color=NAVY):
        super().__init__(id, frames)
        self.header_text = header_text
        self.footer_text = footer_text
        self.page_color = page_color
    def afterDrawPage(self, canvas, doc):
        canvas.saveState()
        # Top thin rule
        canvas.setStrokeColor(self.page_color)
        canvas.setLineWidth(1.2)
        canvas.line(MARGIN, PAGE_H - MARGIN + 0.4 * cm,
                    PAGE_W - MARGIN, PAGE_H - MARGIN + 0.4 * cm)
        canvas.setFont("BodyRegular", 8.5)
        canvas.setFillColor(SUBTLE)
        canvas.drawString(MARGIN, PAGE_H - MARGIN + 0.55 * cm, self.header_text)
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - MARGIN + 0.55 * cm,
                               "BDA Final Exam Prep")
        # Footer
        canvas.setLineWidth(0.4)
        canvas.line(MARGIN, MARGIN - 0.4 * cm,
                    PAGE_W - MARGIN, MARGIN - 0.4 * cm)
        canvas.drawString(MARGIN, MARGIN - 0.7 * cm, self.footer_text)
        canvas.drawRightString(PAGE_W - MARGIN, MARGIN - 0.7 * cm,
                               f"Page {doc.page}")
        canvas.restoreState()


def make_doc(out_path: str, title: str, header_text: str, footer_text: str
             ) -> BaseDocTemplate:
    doc = BaseDocTemplate(
        out_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN + 0.4 * cm, bottomMargin=MARGIN + 0.6 * cm,
        title=title, author="BDA Exam Prep — Claude Tutor",
    )
    frame_main = Frame(MARGIN, MARGIN, USABLE_W, PAGE_H - 2 * MARGIN,
                       id="main", showBoundary=0)
    frame_cover = Frame(MARGIN, MARGIN, USABLE_W, PAGE_H - 2 * MARGIN,
                        id="cover", showBoundary=0)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame_cover]),
        HFPageTemplate(id="main", frames=[frame_main],
                       header_text=header_text, footer_text=footer_text),
    ])
    return doc


# ─── Cover page builder ───────────────────────────────────────────────────
def cover_block(title: str, subtitle: str, week_label: str, topics: list[str],
                styles: dict, exam_date: str = "Final ~ 2026-05-16") -> list:
    flow = []
    flow.append(Spacer(1, 4 * cm))
    flow.append(Paragraph(title, styles["CoverTitle"]))
    flow.append(Spacer(1, 0.5 * cm))
    # gold rule
    rule = Table([[""]], colWidths=[6*cm], rowHeights=[2])
    rule.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GOLD)]))
    flow.append(KeepTogether([Spacer(1,0.2*cm), rule, Spacer(1,0.4*cm)]))
    flow.append(Paragraph(subtitle, styles["CoverSubtitle"]))
    flow.append(Spacer(1, 1 * cm))
    flow.append(Paragraph(f"<b>{week_label}</b>", styles["CoverMeta"]))
    flow.append(Spacer(1, 0.5 * cm))
    flow.append(Paragraph("<b>Topics covered in this PDF:</b>",
                          ParagraphStyle("CoverTopicsHead",
                                         fontName="BodyBold", fontSize=11,
                                         alignment=TA_CENTER, textColor=NAVY)))
    flow.append(Spacer(1, 0.2 * cm))
    for t in topics:
        flow.append(Paragraph(f"• {t}", ParagraphStyle(
            "CoverTopic", fontName="BodyRegular", fontSize=10.5,
            alignment=TA_CENTER, textColor=INK, leading=15)))
    flow.append(Spacer(1, 1.5 * cm))
    flow.append(Paragraph(f"CS-404 Big Data Analytics &nbsp;·&nbsp; "
                          f"Dr. Syed Imran Ali &nbsp;·&nbsp; {exam_date}",
                          styles["CoverMeta"]))
    flow.append(Spacer(1, 0.4 * cm))
    flow.append(Paragraph("Prepared as a comprehensive professor-grade study tutor.",
                          styles["CoverMeta"]))
    return flow


# ─── Section divider (full-width colored bar) ────────────────────────────
def section_bar(label: str, color: HexColor) -> Table:
    p = Paragraph(f"<font color='white'><b>{label}</b></font>",
                  ParagraphStyle("BarLbl", fontName="BodyBold",
                                 fontSize=12, alignment=TA_LEFT,
                                 textColor=colors.white))
    t = Table([[p]], colWidths=[USABLE_W], rowHeights=[0.7*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),color),
        ("LEFTPADDING",(0,0),(-1,-1),10),
        ("RIGHTPADDING",(0,0),(-1,-1),10),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    return t


def hr() -> Table:
    """Light horizontal rule as a flowable."""
    t = Table([[""]], colWidths=[USABLE_W], rowHeights=[1])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),HexColor("#D8D8D8"))]))
    return t
