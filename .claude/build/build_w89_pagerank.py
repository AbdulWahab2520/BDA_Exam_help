"""Builds the Week 8-9 PageRank exam-prep PDF for BDA final.

Run:  cd /Users/awaisshah228/Documents/big-data-analytic && python3 .claude/build/build_w89_pagerank.py
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch

from reportlab.platypus import (
    Paragraph, Spacer, PageBreak, NextPageTemplate, KeepTogether, Table, TableStyle, Image
)
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor

from bda_style import (
    build_stylesheet, make_doc, cover_block, section_bar, hr,
    callout, autofit_table, eq, display_eq, save_fig, fig_image,
    NAVY, GOLD, KEY_BLUE, KEY_BG, EX_GREEN, EX_BG, DEF_PURP, DEF_BG,
    WARN_RED, WARN_BG, PRAC_ORN, PRAC_BG, ANS_TEAL, ANS_BG,
    REV_RED, REV_BG, REF_INDIGO, REF_BG, USABLE_W,
)

OUT = "BDA_W08-09_PageRank_ExamPrep.pdf"
S = build_stylesheet()


# ════════════════════════════════════════════════════════════════════════
#  DIAGRAM GENERATORS
# ════════════════════════════════════════════════════════════════════════

def fig_yam_graph():
    """The canonical 3-node example: y → a, y ↔ a, a → m, m → a."""
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    pos = {"y": (0.15, 0.85), "a": (0.55, 0.30), "m": (0.95, 0.85)}
    for n, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), 0.075, facecolor="#1F4E79",
                            edgecolor="#0B2540", lw=2, zorder=3))
        ax.text(x, y, n, ha="center", va="center",
                color="white", fontsize=14, fontweight="bold", zorder=4)
    edges = [("y","a"),("y","y"),("a","y"),("a","m"),("m","a")]
    # We'll use a simpler set: y→a, a→y, y→m? Actually slide example: y↔a, a→m, m→a, y→y is not present.
    # Slide flow: ry=ry/2+ra/2, ra=ry/2+rm, rm=ra/2 → so y has out-deg 2 (→y? or →a,→m), let's match slide:
    # ry = ry/2 + ra/2 means y receives from itself and a.
    # ra = ry/2 + rm means a receives from y and m.
    # rm = ra/2 means m receives from a.
    # So edges: y→y? But d_y must equal 2 (since rj/dj = ry/2 sent to a and to itself).
    # Actually the slide: y links to itself & a (out=2), a links to y & m (out=2), m links to a (out=1).
    edges = [("y","y"),("y","a"),("a","y"),("a","m"),("m","a")]
    arrow_kw = dict(arrowstyle="-|>", mutation_scale=18,
                    color="#0B2540", lw=1.5, zorder=2,
                    shrinkA=12, shrinkB=12)
    for u, v in edges:
        if u == v:
            # self-loop
            x0, y0 = pos[u]
            ax.add_patch(FancyArrowPatch(
                (x0-0.06, y0+0.05), (x0+0.06, y0+0.05),
                connectionstyle="arc3,rad=2.5", **arrow_kw))
        else:
            ax.annotate("", xy=pos[v], xytext=pos[u],
                        arrowprops=dict(arrowstyle="-|>", color="#0B2540",
                                        lw=1.5, shrinkA=14, shrinkB=14,
                                        connectionstyle="arc3,rad=0.18"))
    ax.set_xlim(0, 1.1); ax.set_ylim(0.05, 1.05)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("3-page web graph (canonical worked example)",
                 fontsize=11, color="#0B2540", pad=8)
    return save_fig(fig, "yam_graph")


def fig_spider_trap():
    """y/a/m where m has only a self-loop (spider trap)."""
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    pos = {"y":(0.15,0.85),"a":(0.55,0.30),"m":(0.95,0.85)}
    for n,(x,y) in pos.items():
        ax.add_patch(Circle((x,y),0.075,
            facecolor="#B22234" if n=="m" else "#1F4E79",
            edgecolor="#0B2540", lw=2, zorder=3))
        ax.text(x,y,n,ha="center",va="center",color="white",
                fontsize=14,fontweight="bold",zorder=4)
    edges = [("y","y"),("y","a"),("a","y"),("a","m"),("m","m")]
    for u,v in edges:
        if u==v:
            x0,y0 = pos[u]
            ax.add_patch(FancyArrowPatch(
                (x0-0.06,y0+0.05),(x0+0.06,y0+0.05),
                connectionstyle="arc3,rad=2.5",
                arrowstyle="-|>",mutation_scale=18,
                color=("#B22234" if u=="m" else "#0B2540"),
                lw=1.6,shrinkA=12,shrinkB=12))
        else:
            ax.annotate("", xy=pos[v], xytext=pos[u],
                arrowprops=dict(arrowstyle="-|>",color="#0B2540",
                                lw=1.5,shrinkA=14,shrinkB=14,
                                connectionstyle="arc3,rad=0.18"))
    ax.text(0.95, 1.00, "spider trap",
            fontsize=10, color="#B22234", ha="center", fontweight="bold")
    ax.set_xlim(0,1.1); ax.set_ylim(0.05,1.10); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Spider trap: m's only out-link is to itself",
                 fontsize=11, color="#0B2540", pad=8)
    return save_fig(fig, "spider_trap")


def fig_dead_end():
    """y/a/m where m has NO out-links (dead end)."""
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    pos = {"y":(0.15,0.85),"a":(0.55,0.30),"m":(0.95,0.85)}
    for n,(x,y) in pos.items():
        ax.add_patch(Circle((x,y),0.075,
            facecolor="#B85C00" if n=="m" else "#1F4E79",
            edgecolor="#0B2540", lw=2, zorder=3))
        ax.text(x,y,n,ha="center",va="center",color="white",
                fontsize=14,fontweight="bold",zorder=4)
    edges = [("y","y"),("y","a"),("a","y"),("a","m")]   # m has NO out-links
    for u,v in edges:
        if u==v:
            x0,y0 = pos[u]
            ax.add_patch(FancyArrowPatch(
                (x0-0.06,y0+0.05),(x0+0.06,y0+0.05),
                connectionstyle="arc3,rad=2.5",
                arrowstyle="-|>",mutation_scale=18,
                color="#0B2540",lw=1.6,shrinkA=12,shrinkB=12))
        else:
            ax.annotate("", xy=pos[v], xytext=pos[u],
                arrowprops=dict(arrowstyle="-|>",color="#0B2540",
                                lw=1.5,shrinkA=14,shrinkB=14,
                                connectionstyle="arc3,rad=0.18"))
    ax.text(0.95, 1.00, "dead-end",
            fontsize=10, color="#B85C00", ha="center", fontweight="bold")
    ax.set_xlim(0,1.1); ax.set_ylim(0.05,1.10); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Dead-end: m has no out-links → mass leaks out",
                 fontsize=11, color="#0B2540", pad=8)
    return save_fig(fig, "dead_end")


def fig_teleport_concept():
    """Conceptual diagram: random surfer with two options."""
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    # left: surfer at node
    surfer = Circle((0.15, 0.5), 0.07, facecolor="#1F4E79",
                    edgecolor="#0B2540", lw=2)
    ax.add_patch(surfer)
    ax.text(0.15, 0.5, "i", ha="center", va="center",
            color="white", fontsize=14, fontweight="bold")
    # arrows splitting
    ax.annotate("", xy=(0.55, 0.78), xytext=(0.21, 0.55),
        arrowprops=dict(arrowstyle="-|>", color="#1B5E20",
                        lw=2.0, shrinkB=2))
    ax.annotate("", xy=(0.55, 0.22), xytext=(0.21, 0.45),
        arrowprops=dict(arrowstyle="-|>", color="#B22234",
                        lw=2.0, shrinkB=2))
    ax.text(0.36, 0.85, r"with prob. $\beta$ → follow link",
            fontsize=10.5, color="#1B5E20", ha="center", fontweight="bold")
    ax.text(0.36, 0.13, r"with prob. $1-\beta$ → teleport",
            fontsize=10.5, color="#B22234", ha="center", fontweight="bold")
    # right: outcomes
    out_nodes = [("0.78,0.78","j (out-neighbor)"),("0.78,0.22","random page k")]
    for spec, lbl in out_nodes:
        x,y = map(float, spec.split(","))
        ax.add_patch(Circle((x,y), 0.06, facecolor="white",
                            edgecolor="#0B2540", lw=2))
        ax.text(x+0.13, y, lbl, fontsize=10, va="center", color="#0B2540")
    ax.set_xlim(0,1.05); ax.set_ylim(0,1); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Random teleport: every step, surfer picks one of two options",
                 fontsize=11, color="#0B2540", pad=8)
    return save_fig(fig, "teleport_concept")


def fig_iteration_convergence():
    """Plot iteration convergence for the canonical y/a/m graph (no traps)
    and for the Google formulation with β=0.8."""
    # Vanilla power iteration (no teleport, no traps): y/a/m
    M = np.array([[0.5, 0.5, 0.0],
                  [0.5, 0.0, 1.0],
                  [0.0, 0.5, 0.0]])
    r = np.array([1/3, 1/3, 1/3])
    history = [r.copy()]
    for _ in range(20):
        r = M @ r
        history.append(r.copy())
    H = np.array(history)
    # Google A with beta=0.8 (no dead-ends here)
    beta = 0.8
    N = 3
    A = beta * M + (1-beta)/N * np.ones((N,N))
    rg = np.array([1/3, 1/3, 1/3])
    hist_g = [rg.copy()]
    for _ in range(20):
        rg = A @ rg
        hist_g.append(rg.copy())
    HG = np.array(hist_g)

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.4))
    labels = ["y", "a", "m"]
    cols = ["#1F4E79", "#1B5E20", "#B85C00"]
    for ax, H_, ttl in [(axes[0], H, "Vanilla (β=1) power iteration"),
                        (axes[1], HG, "Google formulation (β=0.8)")]:
        for i, lab in enumerate(labels):
            ax.plot(range(H_.shape[0]), H_[:, i], "-o",
                    color=cols[i], lw=1.6, ms=4, label=f"$r_{lab}$")
        ax.set_xlabel("iteration t", fontsize=10)
        ax.set_ylabel("rank value", fontsize=10)
        ax.set_title(ttl, fontsize=10.5, color="#0B2540")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9, loc="best", frameon=False)
    fig.tight_layout()
    return save_fig(fig, "iteration_convergence")


def fig_algorithm_flow():
    """Flowchart of the complete PageRank algorithm with leak handling."""
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    nodes = [
        (0.50, 0.94, "Initialize $r^{old}_j = 1/N$ for all j"),
        (0.50, 0.78, r"For each $j$: compute $r'^{new}_j = \sum_{i \to j} \beta \, r^{old}_i / d_i$"),
        (0.50, 0.62, r"Compute $S = \sum_j r'^{new}_j$"),
        (0.50, 0.46, r"$r^{new}_j = r'^{new}_j + (1 - S)/N$  (re-insert leaked mass)"),
        (0.50, 0.30, r"Δ = $\sum_j |r^{new}_j - r^{old}_j|$"),
        (0.50, 0.14, r"If Δ < ε  → STOP   else  $r^{old} \leftarrow r^{new}$, repeat"),
    ]
    for (x, y, txt) in nodes:
        ax.add_patch(FancyBboxPatch((x-0.42, y-0.04), 0.84, 0.08,
                                     boxstyle="round,pad=0.02,rounding_size=0.02",
                                     linewidth=1.2,
                                     edgecolor="#0B2540",
                                     facecolor="#E8F0F8"))
        ax.text(x, y, txt, ha="center", va="center",
                fontsize=10, color="#0B2540")
    # arrows
    for i in range(len(nodes)-1):
        x1,y1,_ = nodes[i]
        x2,y2,_ = nodes[i+1]
        ax.annotate("", xy=(x2, y2+0.04), xytext=(x1, y1-0.04),
                    arrowprops=dict(arrowstyle="-|>", color="#0B2540", lw=1.4))
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    return save_fig(fig, "algorithm_flow")


# Build all figures up-front
print("[w89] generating diagrams...")
F_YAM        = fig_yam_graph()
F_SPIDER     = fig_spider_trap()
F_DEAD       = fig_dead_end()
F_TELEPORT   = fig_teleport_concept()
F_CONVERGE   = fig_iteration_convergence()
F_FLOW       = fig_algorithm_flow()


# ════════════════════════════════════════════════════════════════════════
#  CONTENT BUILDERS
# ════════════════════════════════════════════════════════════════════════

def P(text, style="Body"):
    return Paragraph(text, S[style])


def cover_page():
    flow = cover_block(
        title="Week 08 – 09",
        subtitle="Graph Mining: PageRank",
        week_label="Module 1 of Phase-1 Final Prep · Highest-yield post-mid topic",
        topics=[
            "Web search ranking — links as votes",
            "Flow formulation &amp; matrix form (column-stochastic M)",
            "Eigenvector view &amp; the Power Iteration method",
            "Random walk interpretation, stationary distribution",
            "Dead-ends and spider traps — why naive PageRank fails",
            "Google teleport solution: r = β·M·r + (1−β)/N",
            "Sparse-matrix algorithm with leak re-injection",
            "8 fully worked numerical traces · 15 calibrated practice questions",
        ],
        styles=S,
    )
    flow.append(NextPageTemplate("main"))
    flow.append(PageBreak())
    return flow


def toc_page():
    flow = []
    flow.append(P("Contents", "TocTitle"))
    flow.append(hr())
    flow.append(Spacer(1, 0.3 * cm))
    items = [
        ("1.", "Beginning Key Notes — your study compass"),
        ("2.", "Why PageRank? — the web-search problem"),
        ("3.", "Flow Formulation — links as weighted votes"),
        ("4.", "Matrix Formulation — the stochastic adjacency matrix M"),
        ("5.", "Eigenvector View &amp; Power Iteration"),
        ("6.", "Random Walk Interpretation &amp; Stationary Distribution"),
        ("7.", "Two Convergence Problems — Dead-ends &amp; Spider Traps"),
        ("8.", "The Google Solution — Random Teleports"),
        ("9.", "Sparse Matrix Formulation &amp; the Complete Algorithm"),
        ("10.", "Eight Worked Numerical Examples (exam-style)"),
        ("11.", "Practice Questions (15)"),
        ("12.", "Full Worked Answers"),
        ("13.", "Ending Key Notes — Revision Cards"),
        ("14.", "PageRank Formula &amp; Algorithm Reference Sheet"),
    ]
    for num, txt in items:
        flow.append(P(f"<b>{num}</b> &nbsp; {txt}", "TocItem"))
    flow.append(PageBreak())
    return flow


def beginning_key_notes():
    flow = []
    flow.append(section_bar("§ 1   BEGINNING KEY NOTES — STUDY COMPASS", KEY_BLUE))
    flow.append(Spacer(1, 0.3*cm))
    body = [
        Paragraph(
            "These are the load-bearing ideas you must walk into the exam owning. "
            "Every numerical question on PageRank reduces to applying one of these.",
            S["KeyBody"]),
        Spacer(1, 0.15*cm),
        Paragraph("• <b>Links are votes.</b> A page is important if many important pages link to it. "
                  "Self-referential definition → solve as an eigenvector problem.", S["KeyBody"]),
        Paragraph("• <b>The flow equation:</b> r<sub>j</sub> = Σ<sub>i→j</sub> r<sub>i</sub> / d<sub>i</sub>. "
                  "Each in-link contributes the source page's rank divided by its out-degree.", S["KeyBody"]),
        Paragraph("• <b>Matrix form:</b> r = M·r where M is the column-stochastic transition matrix. "
                  "M<sub>ji</sub> = 1/d<sub>i</sub> if i→j else 0.", S["KeyBody"]),
        Paragraph("• <b>Power iteration:</b> r<sup>(t+1)</sup> = M·r<sup>(t)</sup>, "
                  "started from r<sup>(0)</sup>=[1/N,…,1/N], stop when |r<sup>(t+1)</sup>−r<sup>(t)</sup>|&lt;ε. "
                  "Converges to the principal eigenvector with eigenvalue 1.", S["KeyBody"]),
        Paragraph("• <b>Two failure modes:</b> "
                  "<i>Spider traps</i> absorb all rank, "
                  "<i>dead-ends</i> leak rank out — both break naive PageRank.", S["KeyBody"]),
        Paragraph("• <b>Google fix — random teleports:</b> "
                  "with probability β follow a link, with probability 1−β jump to a uniformly random page. "
                  "β ≈ 0.8–0.9 in practice.", S["KeyBody"]),
        Paragraph("• <b>Google matrix:</b> A = β·M + (1−β)/N · J<sub>N×N</sub>. "
                  "A is stochastic, aperiodic, and irreducible — a unique stationary r exists and power iteration finds it.", S["KeyBody"]),
        Paragraph("• <b>Production form (sparse):</b> "
                  "r<sup>new</sup> = β·M·r<sup>old</sup> + [(1−S)/N]<sub>N</sub> "
                  "where S=Σ(β·M·r<sup>old</sup>)<sub>j</sub>. "
                  "Re-inserting (1−S)/N handles dead-end leakage.", S["KeyBody"]),
        Paragraph("• <b>Numerical exam pattern.</b> The examiner consistently asks you to walk a "
                  "small graph through 2–3 power-iteration steps by hand. "
                  "Master that procedure and 60–70% of the PageRank marks are guaranteed.",
                  S["KeyBody"]),
    ]
    flow.append(callout("THE EIGHT THINGS YOU MUST OWN", body,
                       title_style=S["KeyTitle"], body_style=S["KeyBody"],
                       bg=KEY_BG, border=KEY_BLUE))
    flow.append(PageBreak())
    return flow


def why_pagerank():
    flow = []
    flow.append(section_bar("§ 2   WHY PAGERANK? THE WEB-SEARCH PROBLEM", NAVY))
    flow.append(P("The web is enormous, decentralized, and full of pages all claiming to be relevant. "
                  "Two problems make ranking hard:", "Body"))
    flow.append(P("<b>(1) Trust.</b> Many pages publish information about the same topic. "
                  "Who do you believe? Trustworthy pages tend to link to other trustworthy pages, "
                  "so we can use the link graph itself to surface trust.", "Body"))
    flow.append(P("<b>(2) Relevance amid ambiguity.</b> If a user types <i>“newspaper”</i>, there is no single "
                  "right answer. Pages that genuinely know about newspapers tend to link to many newspapers — "
                  "again, structure in the link graph signals authority.", "Body"))
    flow.append(P("PageRank reframes the search-ranking problem as a question about graph structure: "
                  "<b>given the link graph alone (forget the content for a moment), how important is each page?</b> "
                  "The breakthrough idea — patented by Brin and Page in 1998 — is to define importance "
                  "<i>recursively</i>: a page is important if important pages link to it.", "Body"))
    flow.append(callout(
        "ANALOGY — academic citations",
        [P("Think of academic papers. A paper that is cited 50 times by other heavily-cited papers "
           "is more important than one cited 50 times only by obscure papers. The citing paper's "
           "own importance flows into the cited paper. PageRank is exactly this idea applied to "
           "the web: a hyperlink is the web's version of a citation.", "DefBody")],
        title_style=S["DefTitle"], body_style=S["DefBody"],
        bg=DEF_BG, border=DEF_PURP))
    flow.append(Spacer(1, 0.25*cm))
    flow.append(P("<b>Three guiding ideas before any maths:</b>", "H3"))
    flow.append(P("• <b>In-links are votes</b> — but every vote is not equal.", "Bullet"))
    flow.append(P("• <b>A vote from an important page counts more</b> than a vote from a low-importance page.", "Bullet"))
    flow.append(P("• <b>Each page's vote is split</b> equally among its out-links — so a page with 1000 out-links "
                  "passes only 1/1000 of its rank to each linked target.", "Bullet"))
    flow.append(Spacer(1, 0.2*cm))
    return flow


def flow_formulation():
    flow = []
    flow.append(section_bar("§ 3   FLOW FORMULATION — LINKS AS WEIGHTED VOTES", NAVY))
    flow.append(P("Let r<sub>j</sub> denote the rank (importance score) of page j. "
                  "Let d<sub>i</sub> be the out-degree of page i. "
                  "If page i links to page j, page i contributes r<sub>i</sub> / d<sub>i</sub> "
                  "to page j — its own rank, divided evenly across its out-links. "
                  "Summing over all in-links gives the central <b>flow equation</b>:", "Body"))
    flow.append(display_eq(r"r_j \;=\; \sum_{i \to j} \frac{r_i}{d_i}", fontsize=18))
    flow.append(P("This is a linear equation per page. With N pages we have N equations in N unknowns. "
                  "But the equations are <i>homogeneous</i> — multiplying every r<sub>j</sub> by the "
                  "same constant gives another valid solution. We close the system with a "
                  "normalization constraint:", "Body"))
    flow.append(display_eq(r"\sum_{j} r_j \;=\; 1", fontsize=16))
    flow.append(Spacer(1, 0.2*cm))
    flow.append(fig_image(F_YAM, max_w_cm=12.5, max_h_cm=7.0))
    flow.append(P("<b>Figure 3.1.</b> The canonical 3-node example used throughout the course slides "
                  "and most exam problems. Out-degrees: d<sub>y</sub>=2 (y→y, y→a), d<sub>a</sub>=2 (a→y, a→m), "
                  "d<sub>m</sub>=1 (m→a).", "Caption"))
    flow.append(P("<b>Reading the graph into flow equations.</b> "
                  "y receives from itself (×½) and from a (×½). a receives from y (×½) and from m (×1). "
                  "m receives from a (×½). So:", "Body"))
    flow.append(display_eq(
        r"r_y = \tfrac{r_y}{2} + \tfrac{r_a}{2}, \quad "
        r"r_a = \tfrac{r_y}{2} + r_m, \quad "
        r"r_m = \tfrac{r_a}{2}", fontsize=14))
    flow.append(P("Combined with r<sub>y</sub>+r<sub>a</sub>+r<sub>m</sub>=1, the unique solution is "
                  "r<sub>y</sub>=2/5, r<sub>a</sub>=2/5, r<sub>m</sub>=1/5. "
                  "Gaussian elimination handles this for 3 unknowns; for billions of pages we need a smarter method — "
                  "and that is the matrix / power-iteration approach in §4–§5.", "Body"))
    flow.append(callout(
        "EXAM TRAP — out-degree, not in-degree",
        [P("In <b>r<sub>i</sub>/d<sub>i</sub></b>, d<sub>i</sub> is the <i>source</i> page's out-degree, "
           "not the target's in-degree. Students routinely mix these up under exam pressure. "
           "Always label out-degrees on the graph FIRST, then write the flow equations.",
           "WarnBody")],
        title_style=S["WarnTitle"], body_style=S["WarnBody"],
        bg=WARN_BG, border=WARN_RED))
    return flow


def matrix_formulation():
    flow = []
    flow.append(section_bar("§ 4   MATRIX FORMULATION — STOCHASTIC ADJACENCY M", NAVY))
    flow.append(P("Define the <b>stochastic adjacency matrix</b> M of size N × N as:", "Body"))
    flow.append(display_eq(
        r"M_{ji} \;=\; \begin{cases} 1/d_i & \text{if } i \to j \\ 0 & \text{otherwise} \end{cases}",
        fontsize=14))
    flow.append(P("<b>Read M<sub>ji</sub> as “column i, row j”</b>: it is the share of i's rank that flows to j. "
                  "Each <i>column</i> of M sums to 1 (because page i splits its outflow across "
                  "exactly d<sub>i</sub> out-links, each getting 1/d<sub>i</sub>) — that is what "
                  "<b>column-stochastic</b> means.", "Body"))
    flow.append(callout(
        "DEFINITION — column-stochastic matrix",
        [P("A non-negative matrix whose every column sums to 1. "
           "Crucially, M·v preserves the L1 norm of v: if Σv<sub>i</sub>=1 then Σ(Mv)<sub>j</sub>=1. "
           "This is why power iteration on M does not blow up.", "DefBody")],
        title_style=S["DefTitle"], body_style=S["DefBody"],
        bg=DEF_BG, border=DEF_PURP))
    flow.append(Spacer(1, 0.15*cm))
    flow.append(P("With M defined, the flow equations bundle into a single matrix equation:", "Body"))
    flow.append(display_eq(r"r \;=\; M \cdot r", fontsize=18))
    flow.append(P("<b>Building M for the y/a/m example.</b> Out-degrees are d<sub>y</sub>=2, d<sub>a</sub>=2, "
                  "d<sub>m</sub>=1. Edges and their column-stochastic entries:", "Body"))
    M_table = autofit_table([
        ["from \\\\ to", "y", "a", "m"],
        ["y", "1/2", "1/2", "0"],
        ["a", "1/2", "0", "1"],
        ["m", "0", "1/2", "0"],
    ], header=True, alignments=["L","C","C","C"],
       caption="Table 4.1. Stochastic matrix M for the 3-node graph. Columns sum to 1.")
    flow.extend(M_table)
    flow.append(P("Reading column-by-column: column y sends ½ to y (self-loop) and ½ to a. "
                  "Column a sends ½ to y and ½ to m. Column m sends 1 to a (its only out-link).", "Body"))
    return flow


def eigenvector_power_iter():
    flow = []
    flow.append(section_bar("§ 5   EIGENVECTOR VIEW & POWER ITERATION", NAVY))
    flow.append(P("The equation r = M·r says exactly that r is an <b>eigenvector of M with eigenvalue 1</b>. "
                  "For a column-stochastic non-negative matrix M, the largest eigenvalue is always 1, "
                  "and the corresponding eigenvector — the principal eigenvector — is what we want.", "Body"))
    flow.append(callout(
        "DEFINITION — eigenvector / eigenvalue",
        [P("A non-zero vector x is an eigenvector of A with eigenvalue λ iff <b>A·x = λ·x</b>. "
           "x captures a “direction” that A only stretches/shrinks, never rotates. "
           "PageRank's key insight: r is the eigenvector that M leaves unchanged (λ=1).",
           "DefBody")],
        title_style=S["DefTitle"], body_style=S["DefBody"],
        bg=DEF_BG, border=DEF_PURP))
    flow.append(Spacer(1, 0.15*cm))
    flow.append(P("<b>Power Iteration Method</b> — the algorithm that finds this eigenvector.", "H3"))
    flow.append(P("• Initialize r<sup>(0)</sup> = [1/N, 1/N, …, 1/N]<sup>T</sup>.", "Bullet"))
    flow.append(P("• Iterate: r<sup>(t+1)</sup> = M · r<sup>(t)</sup>.", "Bullet"))
    flow.append(P("• Stop when |r<sup>(t+1)</sup> − r<sup>(t)</sup>|<sub>1</sub> &lt; ε  (small threshold, e.g. 10<sup>−6</sup>).", "Bullet"))
    flow.append(Spacer(1, 0.15*cm))
    flow.append(P("<b>Why does this work?</b> Repeated multiplication by M amplifies the principal "
                  "eigen-direction relative to all others. After enough steps r<sup>(t)</sup> aligns "
                  "with the eigenvector of eigenvalue 1, and applying M one more time changes nothing — "
                  "we have converged.", "Body"))
    flow.append(P("• Typical convergence: ≈ 50 iterations to high precision on web-scale graphs.", "Bullet"))
    flow.append(P("• Each iteration is one sparse matrix–vector multiply: O(N + E) operations where E is the number of edges.", "Bullet"))
    return flow


def random_walk():
    flow = []
    flow.append(section_bar("§ 6   RANDOM WALK INTERPRETATION", NAVY))
    flow.append(P("There is a beautiful probabilistic reading of PageRank. Imagine a <b>random surfer</b> who, "
                  "at each time step, picks one of the current page's out-links uniformly at random and "
                  "follows it. Let p<sub>j</sub>(t) be the probability the surfer is at page j at time t. "
                  "Then:", "Body"))
    flow.append(display_eq(r"p(t+1) \;=\; M \cdot p(t)", fontsize=16))
    flow.append(P("If the random walk reaches a state where p(t+1)=p(t), that p is a <b>stationary distribution</b> "
                  "of the Markov chain. Comparing with r=M·r reveals the punchline: "
                  "<b>PageRank is the stationary distribution of the random surfer.</b>", "Body"))
    flow.append(callout(
        "WHY THIS MATTERS",
        [P("This view turns PageRank from “nice algebra” into something tangible — "
           "r<sub>j</sub> is literally the long-run fraction of time a random surfer spends on page j. "
           "Pages with high PageRank are pages a random web-walker visits often.", "DefBody")],
        title_style=S["DefTitle"], body_style=S["DefBody"],
        bg=DEF_BG, border=DEF_PURP))
    flow.append(Spacer(1, 0.15*cm))
    flow.append(P("<b>Existence and uniqueness</b> require the chain to be:", "H3"))
    flow.append(P("• <b>Stochastic</b> — every column of M sums to 1 (no rank leakage).", "Bullet"))
    flow.append(P("• <b>Aperiodic</b> — the chain is not stuck in a deterministic cycle.", "Bullet"))
    flow.append(P("• <b>Irreducible</b> — every state is reachable from every other state.", "Bullet"))
    flow.append(P("Naive web graphs violate the first two conditions through dead-ends and spider traps. "
                  "That is exactly the problem we tackle next.", "Body"))
    return flow


def convergence_problems():
    flow = []
    flow.append(section_bar("§ 7   TWO CONVERGENCE PROBLEMS", NAVY))
    flow.append(P("Run vanilla power iteration on the real web and one of two pathological behaviours appears.", "Body"))
    flow.append(P("<b>Problem A — Spider traps.</b> A subset of pages whose out-links all point inside the subset. "
                  "Once the random surfer enters, they cannot leave. Over enough iterations the entire rank mass "
                  "concentrates inside the trap, and every page outside it ends with rank 0.", "H3"))
    flow.append(fig_image(F_SPIDER, max_w_cm=12.0, max_h_cm=7.0))
    flow.append(P("<b>Figure 7.1.</b> Spider trap: m's only out-link is to itself. "
                  "Iterating M from r<sup>(0)</sup> = [1/3, 1/3, 1/3] produces a sequence "
                  "r<sup>(1)</sup> = [1/3, 1/6, 1/2], r<sup>(2)</sup> = [1/4, 1/6, 7/12], … converging to "
                  "r<sub>m</sub> = 1, r<sub>y</sub> = r<sub>a</sub> = 0.", "Caption"))
    flow.append(P("<b>Problem B — Dead-ends.</b> A page with no out-links at all. The corresponding column of M "
                  "is entirely zero, M is no longer column-stochastic, and rank mass <i>leaks</i> out of the system. "
                  "Eventually every rank goes to zero.", "H3"))
    flow.append(fig_image(F_DEAD, max_w_cm=12.0, max_h_cm=7.0))
    flow.append(P("<b>Figure 7.2.</b> Dead-end: m has no out-links. "
                  "Column m of M is all zeros. After ~20 iterations the entire rank vector decays to 0.", "Caption"))
    flow.append(callout(
        "ARE THESE THE SAME PROBLEM? — common exam question",
        [P("<b>No.</b> Spider traps don't violate column-stochastic M; they trap the random walk in a sub-region. "
           "Dead-ends literally break column-stochastic M because mass is destroyed at the dead-end. "
           "<b>The same fix solves both</b>, but for different formal reasons — see §8.", "WarnBody")],
        title_style=S["WarnTitle"], body_style=S["WarnBody"],
        bg=WARN_BG, border=WARN_RED))
    return flow


def google_solution():
    flow = []
    flow.append(section_bar("§ 8   THE GOOGLE SOLUTION — RANDOM TELEPORTS", NAVY))
    flow.append(P("Brin and Page's elegant fix is to give the random surfer an <b>escape hatch</b>. "
                  "At every step:", "Body"))
    flow.append(P("• with probability β, the surfer follows one of the current page's out-links uniformly at random;", "Bullet"))
    flow.append(P("• with probability 1−β, the surfer <b>teleports</b> to a uniformly random page in the entire graph.", "Bullet"))
    flow.append(P("Common values β ≈ 0.8–0.9 — meaning the surfer follows links most of the time but "
                  "every ~5–10 steps takes a random jump. This single tweak fixes both pathologies at once.", "Body"))
    flow.append(fig_image(F_TELEPORT, max_w_cm=14.0, max_h_cm=6.0))
    flow.append(P("<b>Figure 8.1.</b> Random teleport mechanism — at every step the surfer flips a "
                  "biased coin and either follows a link (prob. β) or jumps to a random page (prob. 1−β).", "Caption"))
    flow.append(P("<b>The teleport-augmented PageRank equation:</b>", "H3"))
    flow.append(display_eq(
        r"r_j \;=\; \sum_{i \to j} \beta \, \frac{r_i}{d_i} \;+\; (1-\beta) \, \frac{1}{N}",
        fontsize=16))
    flow.append(P("Equivalently, define the <b>Google matrix</b> A:", "Body"))
    flow.append(display_eq(
        r"A \;=\; \beta \, M \;+\; \frac{1-\beta}{N} \, J_{N \times N}", fontsize=16))
    flow.append(P("where J<sub>N×N</sub> is the all-ones matrix. A is column-stochastic, aperiodic, and "
                  "irreducible — a unique stationary distribution r exists, and power iteration "
                  "<b>r<sup>(t+1)</sup> = A · r<sup>(t)</sup></b> finds it.", "Body"))
    flow.append(callout(
        "EQUIVALENT INTUITION — the “tax & redistribute” view",
        [P("Each iteration, tax every page a fraction (1−β) of its current rank, "
           "pool the tax revenue, and redistribute it equally to all N pages. "
           "The remaining β-fraction flows along the link structure as before. "
           "This view often makes hand-computation faster: compute β·M·r first, sum, then add (1−β)/N to every entry.",
           "DefBody")],
        title_style=S["DefTitle"], body_style=S["DefBody"],
        bg=DEF_BG, border=DEF_PURP))
    flow.append(Spacer(1, 0.15*cm))
    flow.append(P("<b>How does this kill spider traps?</b> The teleport gives the surfer a finite "
                  "probability to escape <i>every</i> step. Average time to escape ≈ 1/(1−β) ≈ 5 steps when β=0.8. "
                  "So mass cannot accumulate forever inside any sub-region.", "Body"))
    flow.append(P("<b>How does this kill dead-ends?</b> One option is to pre-process M and remove dead-end nodes "
                  "iteratively (some pages become dead-ends after others are removed — repeat until stable). "
                  "The simpler production approach is to <b>handle leakage explicitly during iteration</b>, which "
                  "is exactly the algorithm in §9.", "Body"))
    flow.append(P("<b>Convergence comparison</b> on the canonical y/a/m graph (no traps/dead-ends in this version):", "Body"))
    flow.append(fig_image(F_CONVERGE, max_w_cm=15.0, max_h_cm=6.5))
    flow.append(P("<b>Figure 8.2.</b> Left — vanilla power iteration converges to (2/5, 2/5, 1/5). "
                  "Right — Google formulation with β=0.8 converges to a slightly more uniform distribution "
                  "≈ (0.21, 0.15, 0.64). The teleport pulls scores toward 1/N.", "Caption"))
    return flow


def complete_algorithm():
    flow = []
    flow.append(section_bar("§ 9   SPARSE MATRIX FORMULATION & THE COMPLETE ALGORITHM", NAVY))
    flow.append(P("On real web graphs M has billions of rows but only ≈ 10–20 non-zeros per column "
                  "(average out-degree). Storing or multiplying the dense Google matrix A is infeasible — "
                  "but A = β·M + (1−β)/N · J<sub>N×N</sub> can be applied without ever forming A:", "Body"))
    flow.append(display_eq(
        r"r^{new} \;=\; \beta \, M \cdot r^{old} \;+\; \tfrac{1-\beta}{N} \, \mathbf{1}_N", fontsize=16))
    flow.append(P("Step 1 multiplies the <i>sparse</i> M with r — cheap. Step 2 just adds a constant to every entry — also cheap.", "Body"))
    flow.append(P("<b>Handling dead-ends without removing them.</b> If M has dead-ends, β·M·r<sup>old</sup> sums to less than 1: "
                  "some mass S leaked. Re-inject the leak uniformly over all N pages:", "Body"))
    flow.append(display_eq(
        r"r^{new}_j \;=\; (\beta M r^{old})_j \;+\; \frac{1-S}{N}, \quad "
        r"S \;=\; \sum_j (\beta M r^{old})_j", fontsize=14))
    flow.append(P("This guarantees Σr<sup>new</sup>=1 every iteration even with dead-ends present — and "
                  "is mathematically equivalent to the Google teleport formulation when there are no dead-ends.", "Body"))
    flow.append(fig_image(F_FLOW, max_w_cm=15.0, max_h_cm=10.5))
    flow.append(P("<b>Figure 9.1.</b> The full PageRank algorithm with leak re-insertion. "
                  "This is the form most often shown on slides and replicated in exam questions.", "Caption"))
    flow.append(callout(
        "ALGORITHM — Complete PageRank (slide form)",
        [
            Paragraph("<b>Input:</b> Directed graph G (may contain spider traps and dead-ends), "
                      "teleport parameter β.", "ExBody"),
            Paragraph("<b>Output:</b> Rank vector r<sup>new</sup>.", "ExBody"),
            Paragraph("1. Initialize r<sup>old</sup><sub>j</sub> = 1/N for all j.", "ExBody"),
            Paragraph("2. Repeat until Σ<sub>j</sub> |r<sup>new</sup><sub>j</sub> − r<sup>old</sup><sub>j</sub>| &lt; ε:", "ExBody"),
            Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;a. For each j: r'<sup>new</sup><sub>j</sub> = Σ<sub>i→j</sub> β · r<sup>old</sup><sub>i</sub> / d<sub>i</sub>", "ExBody"),
            Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;b. S = Σ<sub>j</sub> r'<sup>new</sup><sub>j</sub>", "ExBody"),
            Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;c. For each j: r<sup>new</sup><sub>j</sub> = r'<sup>new</sup><sub>j</sub> + (1 − S)/N", "ExBody"),
            Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;d. r<sup>old</sup> ← r<sup>new</sup>.", "ExBody"),
            Paragraph("3. Return r<sup>new</sup>.", "ExBody"),
        ],
        title_style=S["ExTitle"], body_style=S["ExBody"],
        bg=EX_BG, border=EX_GREEN))
    flow.append(Spacer(1, 0.15*cm))
    flow.append(P("<b>Storage cost.</b> Storing M as a sparse list (page i, out-degree d<sub>i</sub>, list of out-neighbours) "
                  "costs O(N + E) — about 40 bytes per page in 32-bit indexing. Two rank vectors r<sup>old</sup>, r<sup>new</sup> "
                  "cost O(N). Block-stripe schemes split r<sup>new</sup> across multiple blocks so only one block "
                  "of the result vector is in memory at a time — see Topic-Sensitive PageRank in W12 for details.", "Body"))
    return flow


# ════════════════════════════════════════════════════════════════════════
#  WORKED EXAMPLES (eight, calibrated to examiner style)
# ════════════════════════════════════════════════════════════════════════

def worked_examples():
    flow = []
    flow.append(PageBreak())
    flow.append(section_bar("§ 10   EIGHT WORKED NUMERICAL EXAMPLES", EX_GREEN))
    flow.append(P("Every example below is the kind of multi-step trace your examiner expects you to write out. "
                  "Read the worked solution once, then close this PDF and try to reproduce it from scratch on paper.",
                  "Body"))

    # ── WE 1: Build M from a small graph ───────────────────────────────
    flow.append(P("Worked Example 1 — Building the stochastic matrix M from a graph", "H2"))
    flow.append(P("<b>Problem.</b> Given the directed graph with edges "
                  "A→B, A→C, B→C, C→A, C→B, write down the stochastic adjacency matrix M (4 pages: A,B,C,D where D is isolated… "
                  "actually let's keep it 3 pages: A, B, C only).", "Body"))
    flow.append(P("<b>Step 1 — Out-degrees.</b> d<sub>A</sub> = 2 (A→B, A→C). d<sub>B</sub> = 1 (B→C). d<sub>C</sub> = 2 (C→A, C→B).", "Body"))
    flow.append(P("<b>Step 2 — Fill M column-by-column.</b> Column i of M is page i's out-distribution.", "Body"))
    flow.extend(autofit_table([
        ["", "from A", "from B", "from C"],
        ["row A", "0", "0", "1/2"],
        ["row B", "1/2", "0", "1/2"],
        ["row C", "1/2", "1", "0"],
    ], header=True, alignments=["L","C","C","C"],
       caption="M for example 1. Column sums are 1, 1, 1 — column-stochastic ✓"))
    flow.append(P("<b>Step 3 — Verify.</b> Each column sums to 1. M·r computes one round of rank flow.", "Body"))

    # ── WE 2: Power iteration 3 steps on y/a/m ────────────────────────
    flow.append(P("Worked Example 2 — Three power-iteration steps on the canonical y/a/m graph", "H2"))
    flow.append(P("<b>Problem.</b> Using M from §4 (y→y, y→a; a→y, a→m; m→a), perform three power "
                  "iterations starting from r<sup>(0)</sup> = [1/3, 1/3, 1/3]<sup>T</sup> and "
                  "verify the iterates against the slide answer.", "Body"))
    flow.append(P("<b>Setup.</b> The flow equations are r<sub>y</sub>=r<sub>y</sub>/2+r<sub>a</sub>/2,  "
                  "r<sub>a</sub>=r<sub>y</sub>/2+r<sub>m</sub>,  r<sub>m</sub>=r<sub>a</sub>/2.", "Body"))
    flow.append(P("<b>Iteration 1</b> — apply r<sup>(1)</sup> = M·r<sup>(0)</sup> with r<sup>(0)</sup>=(1/3, 1/3, 1/3):", "Body"))
    flow.append(P("• r<sub>y</sub><sup>(1)</sup> = (1/3)/2 + (1/3)/2 = 1/6 + 1/6 = 1/3", "Bullet"))
    flow.append(P("• r<sub>a</sub><sup>(1)</sup> = (1/3)/2 + (1/3) = 1/6 + 2/6 = 3/6 = 1/2", "Bullet"))
    flow.append(P("• r<sub>m</sub><sup>(1)</sup> = (1/3)/2 = 1/6", "Bullet"))
    flow.append(P("→ r<sup>(1)</sup> = (1/3, 1/2, 1/6). Sanity: sum = 2/6+3/6+1/6 = 6/6 = 1 ✓", "Body"))
    flow.append(P("<b>Iteration 2</b> — r<sup>(2)</sup> = M·r<sup>(1)</sup>:", "Body"))
    flow.append(P("• r<sub>y</sub><sup>(2)</sup> = (1/3)/2 + (1/2)/2 = 2/12 + 3/12 = 5/12", "Bullet"))
    flow.append(P("• r<sub>a</sub><sup>(2)</sup> = (1/3)/2 + 1/6 = 2/12 + 2/12 = 4/12 = 1/3", "Bullet"))
    flow.append(P("• r<sub>m</sub><sup>(2)</sup> = (1/2)/2 = 1/4 = 3/12", "Bullet"))
    flow.append(P("→ r<sup>(2)</sup> = (5/12, 4/12, 3/12) = (5/12, 1/3, 1/4). Sum = 12/12 = 1 ✓", "Body"))
    flow.append(P("<b>Iteration 3</b> — using r<sup>(2)</sup> = (5/12, 1/3, 1/4):", "Body"))
    flow.append(P("• r<sub>y</sub><sup>(3)</sup> = (5/12)/2 + (1/3)/2 = 5/24 + 4/24 = 9/24", "Bullet"))
    flow.append(P("• r<sub>a</sub><sup>(3)</sup> = (5/12)/2 + 1/4 = 5/24 + 6/24 = 11/24", "Bullet"))
    flow.append(P("• r<sub>m</sub><sup>(3)</sup> = (1/3)/2 = 1/6 = 4/24", "Bullet"))
    flow.append(P("→ r<sup>(3)</sup> = (9/24, 11/24, 4/24). Sum = 24/24 = 1 ✓", "Body"))
    flow.append(P("<b>Limit.</b> Continuing the iteration, the sequence converges to "
                  "(2/5, 2/5, 1/5) = (0.4, 0.4, 0.2) — exactly what we got by Gaussian elimination earlier.",
                  "Body"))

    # ── WE 3: Spider trap demo ─────────────────────────────────────────
    flow.append(P("Worked Example 3 — Spider trap: rank concentrates at m", "H2"))
    flow.append(P("<b>Problem.</b> Modify the y/a/m graph so m has only a self-loop (m→m). "
                  "Run vanilla power iteration (no teleport) and show how rank flows.", "Body"))
    flow.append(P("New M (column m is all in m's own row):", "Body"))
    flow.extend(autofit_table([
        ["", "from y", "from a", "from m"],
        ["row y", "1/2", "1/2", "0"],
        ["row a", "1/2", "0", "0"],
        ["row m", "0", "1/2", "1"],
    ], header=True, alignments=["L","C","C","C"]))
    flow.append(P("<b>Iter 1</b> from (1/3, 1/3, 1/3): "
                  "r<sub>y</sub> = 1/6+1/6 = 2/6,  r<sub>a</sub> = 1/6+0 = 1/6,  "
                  "r<sub>m</sub> = 1/6+1/3 = 3/6.  → (2/6, 1/6, 3/6).", "Body"))
    flow.append(P("<b>Iter 2:</b> "
                  "r<sub>y</sub> = (2/6)/2 + (1/6)/2 = 3/12,  "
                  "r<sub>a</sub> = (2/6)/2 = 2/12,  "
                  "r<sub>m</sub> = (1/6)/2 + 3/6 = 1/12 + 6/12 = 7/12. "
                  "→ (3/12, 2/12, 7/12).", "Body"))
    flow.append(P("<b>Iter 3:</b> "
                  "r<sub>y</sub> = 3/24+2/24 = 5/24,  "
                  "r<sub>a</sub> = 3/24,  "
                  "r<sub>m</sub> = 2/24 + 14/24 = 16/24. → (5/24, 3/24, 16/24).", "Body"))
    flow.append(P("<b>Trend.</b> r<sub>m</sub> grows monotonically: 1/3 → 3/6 → 7/12 → 16/24 → … → 1. "
                  "y and a both decay to 0. The trap absorbs everything — clearly nonsense as a ranking.", "Body"))

    # ── WE 4: Dead-end demo ────────────────────────────────────────────
    flow.append(P("Worked Example 4 — Dead-end: total rank decays to 0", "H2"))
    flow.append(P("<b>Problem.</b> Now make m a dead-end (no out-links). Show that without "
                  "teleport / leak handling, the total rank decays.", "Body"))
    flow.append(P("M has all-zero column m:", "Body"))
    flow.extend(autofit_table([
        ["", "from y", "from a", "from m"],
        ["row y", "1/2", "1/2", "0"],
        ["row a", "1/2", "0", "0"],
        ["row m", "0", "1/2", "0"],
    ], header=True, alignments=["L","C","C","C"]))
    flow.append(P("<b>Iter 1</b> from (1/3, 1/3, 1/3): "
                  "r = (2/6, 1/6, 1/6).  Sum = 4/6 ≠ 1.  Mass leaked: 1 − 4/6 = 2/6.", "Body"))
    flow.append(P("<b>Iter 2</b> on the un-renormalised vector: "
                  "r = ((2/6)/2 + (1/6)/2, (2/6)/2, (1/6)/2) = (3/12, 2/12, 1/12). Sum = 6/12 = 1/2.", "Body"))
    flow.append(P("<b>Iter 3:</b> "
                  "r = (3/24+2/24, 3/24, 2/24) = (5/24, 3/24, 2/24). Sum = 10/24 ≈ 0.417.", "Body"))
    flow.append(P("Total rank halves roughly every 2–3 iterations. After ~40 iterations everything is ≈ 0.", "Body"))

    # ── WE 5: Google formulation, β=0.8 on y/a/m (no traps) ───────────
    flow.append(P("Worked Example 5 — Google formulation with β = 0.8", "H2"))
    flow.append(P("<b>Problem.</b> Same y/a/m graph as WE 2 (no traps, no dead-ends). "
                  "Use β = 0.8 and compute the first iteration with the Google formulation.", "Body"))
    flow.append(P("<b>Step 1 — build A.</b> A = 0.8·M + 0.2/3 · J<sub>3×3</sub>. "
                  "Each entry: A<sub>ji</sub> = 0.8·M<sub>ji</sub> + 0.0667.", "Body"))
    flow.extend(autofit_table([
        ["A", "from y", "from a", "from m"],
        ["row y", "0.8(1/2)+0.067 = 0.467", "0.8(1/2)+0.067 = 0.467", "0+0.067 = 0.067"],
        ["row a", "0.8(1/2)+0.067 = 0.467", "0+0.067 = 0.067", "0.8(1)+0.067 = 0.867"],
        ["row m", "0+0.067 = 0.067", "0.8(1/2)+0.067 = 0.467", "0+0.067 = 0.067"],
    ], header=True, alignments=["L","C","C","C"],
       caption="Google matrix A = 0.8·M + (0.2/3)·J. Columns sum to 1 (verify mentally)."))
    flow.append(P("<b>Step 2 — A·r<sup>(0)</sup>.</b> r<sup>(0)</sup> = (1/3, 1/3, 1/3).", "Body"))
    flow.append(P("• r<sub>y</sub><sup>(1)</sup> = (1/3)·(0.467 + 0.467 + 0.067) = (1/3)·1.001 ≈ 0.334", "Bullet"))
    flow.append(P("• r<sub>a</sub><sup>(1)</sup> = (1/3)·(0.467 + 0.067 + 0.867) = (1/3)·1.401 ≈ 0.467", "Bullet"))
    flow.append(P("• r<sub>m</sub><sup>(1)</sup> = (1/3)·(0.067 + 0.467 + 0.067) = (1/3)·0.601 ≈ 0.200", "Bullet"))
    flow.append(P("→ r<sup>(1)</sup> ≈ (0.334, 0.467, 0.200). Sum ≈ 1.001 (rounding only).", "Body"))
    flow.append(P("<b>Faster route — the “tax & redistribute” trick.</b> "
                  "Compute β·M·r<sup>(0)</sup> first, then add (1−β)/N to each entry.", "Body"))
    flow.append(P("• β·M·r<sup>(0)</sup>: M·r<sup>(0)</sup> = (1/3, 1/2, 1/6) (from WE 2). "
                  "Multiply by 0.8: (0.267, 0.400, 0.133).", "Bullet"))
    flow.append(P("• Add 0.2/3 = 0.067 to each: (0.333, 0.467, 0.200). ✓ same answer, less arithmetic.", "Bullet"))

    # ── WE 6: Spider trap with β=0.8 (showing fix) ────────────────────
    flow.append(P("Worked Example 6 — Spider trap fixed by teleport (β = 0.8)", "H2"))
    flow.append(P("<b>Problem.</b> Repeat WE 3 (m is a self-loop spider trap) but with the Google "
                  "formulation, β = 0.8. Show that rank no longer concentrates entirely at m.", "Body"))
    flow.append(P("<b>Iteration 1.</b> M·r<sup>(0)</sup> = (2/6, 1/6, 3/6) (from WE 3). "
                  "Multiply by 0.8: (0.267, 0.133, 0.400). "
                  "Add (1−β)/N = 0.067 to each: r<sup>(1)</sup> = (0.333, 0.200, 0.467).", "Body"))
    flow.append(P("<b>Iteration 2.</b> First M·r<sup>(1)</sup> using the spider-trap M:", "Body"))
    flow.append(P("• r<sub>y</sub>′ = 0.333/2 + 0.200/2 = 0.267", "Bullet"))
    flow.append(P("• r<sub>a</sub>′ = 0.333/2 + 0 = 0.167", "Bullet"))
    flow.append(P("• r<sub>m</sub>′ = 0.200/2 + 0.467 = 0.567", "Bullet"))
    flow.append(P("Multiply by β=0.8 → (0.213, 0.133, 0.453). Add 0.067 → r<sup>(2)</sup> = (0.280, 0.200, 0.520).", "Body"))
    flow.append(P("<b>Iteration 3.</b> Repeat: r<sup>(3)</sup> ≈ (0.259, 0.179, 0.563).", "Body"))
    flow.append(P("Continuing to convergence yields approximately r ≈ (0.21, 0.15, 0.64) — "
                  "m is the most important page (correct: it's the most-linked node), but the rank no "
                  "longer collapses to (0,0,1). Teleport prevented absorption.", "Body"))

    # ── WE 7: Dead-end with leak handling ─────────────────────────────
    flow.append(P("Worked Example 7 — Dead-end fixed by re-injecting leaked mass", "H2"))
    flow.append(P("<b>Problem.</b> Repeat WE 4 (m is a dead-end) but using the complete algorithm: "
                  "after each iteration compute S = sum of r′<sup>new</sup>, then add (1−S)/N to every entry.", "Body"))
    flow.append(P("With β = 0.8 and the dead-end M:", "Body"))
    flow.append(P("<b>Iter 1.</b> M·r<sup>(0)</sup> = (2/6, 1/6, 1/6) = (0.333, 0.167, 0.167). "
                  "Multiply by β: r′ = (0.267, 0.133, 0.133). S = 0.533. "
                  "Add (1 − 0.533)/3 = 0.156 to each: r<sup>(1)</sup> ≈ (0.422, 0.289, 0.289). "
                  "Sum = 1.000 ✓.", "Body"))
    flow.append(P("<b>Iter 2.</b> M·r<sup>(1)</sup> = (0.422·0.5 + 0.289·0.5, 0.422·0.5, 0.289·0.5) "
                  "= (0.356, 0.211, 0.144). β·M·r = (0.284, 0.169, 0.116). S = 0.569. "
                  "Add (1−0.569)/3 = 0.144 to each: r<sup>(2)</sup> ≈ (0.428, 0.313, 0.260). Sum ≈ 1.000 ✓.", "Body"))
    flow.append(P("<b>Convergence.</b> The vector approaches roughly (0.41, 0.32, 0.27) — non-zero "
                  "everywhere, no leakage. The same algorithm works regardless of whether the original "
                  "graph had dead-ends or not.", "Body"))

    # ── WE 8: Larger graph A,B,C,D,E with β=0.85 ──────────────────────
    flow.append(P("Worked Example 8 — Larger 5-node graph with β = 0.85 (one iteration)", "H2"))
    flow.append(P("<b>Problem.</b> A graph has nodes {A, B, C, D, E} with edges: "
                  "A→B, A→C, B→C, C→A, D→A, D→B, E→D. Compute one iteration of the Google "
                  "formulation (β = 0.85) starting from the uniform initial vector.", "Body"))
    flow.append(P("<b>Step 1 — out-degrees.</b> d<sub>A</sub>=2, d<sub>B</sub>=1, d<sub>C</sub>=1, d<sub>D</sub>=2, d<sub>E</sub>=1.", "Body"))
    flow.append(P("<b>Step 2 — M (column-stochastic).</b>", "Body"))
    flow.extend(autofit_table([
        ["", "fr A", "fr B", "fr C", "fr D", "fr E"],
        ["row A", "0", "0", "1", "1/2", "0"],
        ["row B", "1/2", "0", "0", "1/2", "0"],
        ["row C", "1/2", "1", "0", "0", "0"],
        ["row D", "0", "0", "0", "0", "1"],
        ["row E", "0", "0", "0", "0", "0"],
    ], header=True, alignments=["L","C","C","C","C","C"]))
    flow.append(P("<b>Note.</b> E has no in-links AND no out-links from anywhere except D→E? Wait — re-read the edges. "
                  "E has no in-links and no out-links to A/B/C/D in the listed edges. "
                  "Actually E has only one out-link (E→D) and no in-links. Column E sums to 1 (the entry M<sub>D,E</sub>=1). ✓", "Body"))
    flow.append(P("<b>Step 3 — initial r<sup>(0)</sup> = 1/5 = 0.2 for every node.</b>", "Body"))
    flow.append(P("<b>Step 4 — M·r<sup>(0)</sup>.</b>", "Body"))
    flow.append(P("• r'<sub>A</sub> = 0·0.2 + 0·0.2 + 1·0.2 + 0.5·0.2 + 0·0.2 = 0.300", "Bullet"))
    flow.append(P("• r'<sub>B</sub> = 0.5·0.2 + 0·0.2 + 0·0.2 + 0.5·0.2 + 0·0.2 = 0.200", "Bullet"))
    flow.append(P("• r'<sub>C</sub> = 0.5·0.2 + 1·0.2 + 0·0.2 + 0·0.2 + 0·0.2 = 0.300", "Bullet"))
    flow.append(P("• r'<sub>D</sub> = 0·0.2 + 0·0.2 + 0·0.2 + 0·0.2 + 1·0.2 = 0.200", "Bullet"))
    flow.append(P("• r'<sub>E</sub> = 0 + 0 + 0 + 0 + 0 = 0.000", "Bullet"))
    flow.append(P("<b>Step 5 — apply β and add teleport.</b> "
                  "β·M·r<sup>(0)</sup> = (0.255, 0.170, 0.255, 0.170, 0.000). "
                  "(1−β)/N = 0.15/5 = 0.030.", "Body"))
    flow.append(P("→ r<sup>(1)</sup> = (0.285, 0.200, 0.285, 0.200, 0.030). Sum = 1.000 ✓", "Body"))
    flow.append(P("Already after one iteration A and C lead — the linkage structure favours them. "
                  "E has no in-links so its rank is exactly the teleport probability mass.", "Body"))
    return flow


# ════════════════════════════════════════════════════════════════════════
#  PRACTICE QUESTIONS (15) and ANSWERS
# ════════════════════════════════════════════════════════════════════════

def practice_questions():
    flow = []
    flow.append(PageBreak())
    flow.append(section_bar("§ 11   PRACTICE QUESTIONS — 15 calibrated to examiner style", PRAC_ORN))
    flow.append(P("Mix: 6 numerical traces, 5 conceptual short-answer, 4 MCQ / true-false. "
                  "Time yourself — aim for ~6 minutes per numerical, ~3 minutes per conceptual, ~1 minute per MCQ. "
                  "Worked answers begin in §12.", "Body"))
    qs = [
        # NUMERICAL ─────────────────────────────────────────────────────
        ("Q1", "Numerical · 6 marks",
         "Consider the directed graph with nodes {A, B, C} and edges A→B, A→C, B→A, C→A, C→B. "
         "(a) Write the stochastic matrix M. (b) Verify M is column-stochastic. "
         "(c) Starting from r<sup>(0)</sup> = [1/3, 1/3, 1/3]<sup>T</sup>, perform two power-iteration "
         "steps without teleport. State the iterate after each step."),
        ("Q2", "Numerical · 8 marks",
         "Using the canonical y/a/m graph from the slides (y→y, y→a; a→y, a→m; m→a) and the Google "
         "formulation with β = 0.8, compute r<sup>(1)</sup> and r<sup>(2)</sup> starting from "
         "r<sup>(0)</sup> = [1/3, 1/3, 1/3]<sup>T</sup>. Use the “tax & redistribute” trick: "
         "compute β·M·r first, then add (1−β)/N to every entry. Show all intermediate values."),
        ("Q3", "Numerical · 7 marks",
         "Consider a graph where node m is a dead-end (no out-links): edges are y→y, y→a, a→y, a→m. "
         "Run two iterations of the COMPLETE PageRank algorithm (with leak re-injection) using β = 0.85, "
         "starting from r<sup>(0)</sup> uniform. After each iteration explicitly compute S "
         "(the sum of β·M·r) and verify the new rank vector sums to 1."),
        ("Q4", "Numerical · 6 marks",
         "A graph has nodes {1, 2, 3, 4} and edges 1→2, 2→3, 3→4, 4→2 (i.e. nodes 2, 3, 4 form a cycle "
         "with 1 feeding into 2). With β = 0.8 and r<sup>(0)</sup> uniform, compute one iteration "
         "of the Google formulation. Comment on whether {2, 3, 4} forms a spider trap."),
        ("Q5", "Numerical · 5 marks",
         "If the rank vector at iteration t is r<sup>(t)</sup> = (0.3, 0.4, 0.3) for the y/a/m graph "
         "(WE 2's graph) and β = 1, compute r<sup>(t+1)</sup>. State |r<sup>(t+1)</sup> − r<sup>(t)</sup>|<sub>1</sub>. "
         "If the convergence threshold is ε = 0.05, has the algorithm converged?"),
        ("Q6", "Numerical · 8 marks",
         "Suppose the stochastic matrix has been pre-computed as "
         "M = [[0, 1/2, 0, 0],[1/2, 0, 1, 0],[0, 1/2, 0, 1],[1/2, 0, 0, 0]] "
         "(columns ordered A, B, C, D). With β = 0.8 and r<sup>(0)</sup> = [1/4, 1/4, 1/4, 1/4]<sup>T</sup>, "
         "perform one full Google-formulation iteration. Show M·r, β·M·r, and the final r<sup>(1)</sup>."),
        # CONCEPTUAL ────────────────────────────────────────────────────
        ("Q7", "Concept · 4 marks",
         "Explain in 4–6 sentences why the rank vector r is described as the principal eigenvector of M with "
         "eigenvalue 1. Why is the largest eigenvalue of a column-stochastic non-negative matrix necessarily 1?"),
        ("Q8", "Concept · 4 marks",
         "Compare and contrast spider traps and dead-ends as failure modes of vanilla PageRank. "
         "For each, state (a) what happens to the rank vector if you keep iterating, (b) which condition "
         "of the Markov-chain stationary-distribution theorem is violated, and (c) how teleport / leak "
         "injection fixes the problem."),
        ("Q9", "Concept · 3 marks",
         "Why do practitioners choose β between 0.8 and 0.9? What is the trade-off as β → 1, and what is "
         "the trade-off as β → 0?"),
        ("Q10", "Concept · 4 marks",
         "State the random-walk interpretation of PageRank. Explain in your own words why the stationary "
         "distribution of the modified Markov chain (with teleport) is unique while the stationary distribution "
         "of the original chain may not be."),
        ("Q11", "Concept · 3 marks",
         "Consider the “tax and redistribute” reformulation: r = β·M·r + (1−β)/N · 1<sub>N</sub>. "
         "Explain why this is equivalent to the Google matrix formulation r = A·r when M has no dead-ends, "
         "and why a leak correction term must be added when M does have dead-ends."),
        # MCQ / T-F ─────────────────────────────────────────────────────
        ("Q12", "MCQ · 2 marks",
         "Which of the following is TRUE for a column-stochastic matrix M? "
         "(A) every row sums to 1, "
         "(B) every column sums to 1 and the largest eigenvalue is exactly 1, "
         "(C) M·r is always a probability distribution if r is, regardless of the graph, "
         "(D) all entries of M are positive."),
        ("Q13", "MCQ · 2 marks",
         "Power iteration r<sup>(t+1)</sup> = M·r<sup>(t)</sup> on a column-stochastic M without traps "
         "or dead-ends will converge to: "
         "(A) the principal eigenvector of M with eigenvalue 1, "
         "(B) any eigenvector of M, "
         "(C) the zero vector, "
         "(D) a vector that depends on the initial r<sup>(0)</sup>."),
        ("Q14", "True/False · 2 marks",
         "True or false: in the Google formulation, increasing β (e.g. from 0.8 to 0.95) makes power "
         "iteration converge faster. Justify in one sentence."),
        ("Q15", "MCQ · 2 marks",
         "If the leaked mass at iteration t is S = 0.92 with β = 0.85 and N = 100, the per-page "
         "leak-correction term added to every entry is closest to: "
         "(A) 0.0008,  (B) 0.0015,  (C) 0.0085,  (D) 0.0500."),
    ]
    for qid, header, body in qs:
        flow.append(KeepTogether([
            P(f"<b>{qid}</b> &nbsp; <font color='#B85C00'>[{header}]</font>", "PracTitle"),
            P(body, "PracBody"),
            Spacer(1, 0.15*cm),
        ]))
    return flow


def full_answers():
    flow = []
    flow.append(PageBreak())
    flow.append(section_bar("§ 12   FULL WORKED ANSWERS", ANS_TEAL))
    flow.append(P("Read each answer line by line. Wherever a step seems to skip arithmetic, work "
                  "it out yourself before reading the next line — this is how exam mastery actually builds.",
                  "Body"))

    answers = [
        ("A1",
         "(a) Out-degrees: d<sub>A</sub>=2 (A→B, A→C), d<sub>B</sub>=1 (B→A), d<sub>C</sub>=2 (C→A, C→B). "
         "M (rows = destination, cols = source A,B,C):<br/><br/>"
         "<font face='Mono'>"
         "&nbsp;&nbsp;row A&nbsp;&nbsp;[ 0&nbsp;&nbsp;1&nbsp;&nbsp;1/2 ]<br/>"
         "&nbsp;&nbsp;row B&nbsp;&nbsp;[ 1/2&nbsp;0&nbsp;&nbsp;1/2 ]<br/>"
         "&nbsp;&nbsp;row C&nbsp;&nbsp;[ 1/2&nbsp;0&nbsp;&nbsp;0&nbsp;&nbsp; ]"
         "</font><br/><br/>"
         "(b) Column sums: col A = 0+1/2+1/2 = 1, col B = 1+0+0 = 1, col C = 1/2+1/2+0 = 1. ✓ column-stochastic.<br/><br/>"
         "(c) <b>Iter 1</b>: r<sub>A</sub>=0·1/3+1·1/3+1/2·1/3 = 1/3+1/6 = 1/2;  "
         "r<sub>B</sub>=1/2·1/3+0+1/2·1/3 = 1/3;  r<sub>C</sub>=1/2·1/3+0+0 = 1/6. "
         "→ r<sup>(1)</sup> = (1/2, 1/3, 1/6). Sum = 6/6 = 1 ✓.<br/>"
         "<b>Iter 2</b>: r<sub>A</sub>=0·(1/2)+1·(1/3)+1/2·(1/6) = 1/3+1/12 = 5/12;  "
         "r<sub>B</sub>=1/2·(1/2)+0+1/2·(1/6) = 1/4+1/12 = 4/12 = 1/3;  "
         "r<sub>C</sub>=1/2·(1/2)+0+0 = 1/4 = 3/12. → r<sup>(2)</sup> = (5/12, 4/12, 3/12). Sum = 1 ✓."),
        ("A2",
         "From WE 2 we know M·r<sup>(0)</sup> = (1/3, 1/2, 1/6) ≈ (0.333, 0.500, 0.167). "
         "<b>Iter 1.</b> β·M·r = 0.8·(0.333, 0.500, 0.167) = (0.267, 0.400, 0.133). "
         "Add (1−β)/N = 0.2/3 = 0.067 to each: r<sup>(1)</sup> = (0.333, 0.467, 0.200). Sum = 1.000 ✓.<br/><br/>"
         "<b>Iter 2.</b> First M·r<sup>(1)</sup>: "
         "r<sub>y</sub>′ = 0.333/2+0.467/2 = 0.400; "
         "r<sub>a</sub>′ = 0.333/2+0.200 = 0.367; "
         "r<sub>m</sub>′ = 0.467/2 = 0.233. "
         "Then β·M·r = (0.320, 0.293, 0.187). Add 0.067: r<sup>(2)</sup> = (0.387, 0.360, 0.253). "
         "Sum = 1.000 ✓."),
        ("A3",
         "Out-degrees: d<sub>y</sub>=2, d<sub>a</sub>=2, d<sub>m</sub>=0 (dead-end). "
         "M has all-zero column m: "
         "M = [[0.5, 0.5, 0],[0.5, 0, 0],[0, 0.5, 0]]. r<sup>(0)</sup> = (1/3, 1/3, 1/3) ≈ (0.333, 0.333, 0.333).<br/><br/>"
         "<b>Iter 1.</b> M·r<sup>(0)</sup> = (0.333, 0.167, 0.167). β·M·r = 0.85·(0.333, 0.167, 0.167) = "
         "(0.283, 0.142, 0.142). S = 0.567. (1−S)/N = 0.433/3 = 0.144. "
         "Add to each: r<sup>(1)</sup> = (0.427, 0.286, 0.286). Sum = 0.999 ≈ 1 ✓.<br/><br/>"
         "<b>Iter 2.</b> M·r<sup>(1)</sup>: r<sub>y</sub>′ = 0.5·0.427+0.5·0.286 = 0.357; "
         "r<sub>a</sub>′ = 0.5·0.427 = 0.214; r<sub>m</sub>′ = 0.5·0.286 = 0.143. "
         "β·M·r<sup>(1)</sup> = (0.303, 0.182, 0.121). S = 0.606. (1−S)/N = 0.394/3 = 0.131. "
         "→ r<sup>(2)</sup> = (0.434, 0.313, 0.252). Sum ≈ 0.999 ✓.<br/><br/>"
         "Notice the rank survives — leakage is fully re-injected."),
        ("A4",
         "Out-degrees: d<sub>1</sub>=1, d<sub>2</sub>=1, d<sub>3</sub>=1, d<sub>4</sub>=1. "
         "M = [[0,0,0,0],[1,0,0,1],[0,1,0,0],[0,0,1,0]] (cols 1,2,3,4). "
         "r<sup>(0)</sup>=(1/4)·1 = 0.25 each. M·r<sup>(0)</sup> = (0, 0.25+0.25, 0.25, 0.25) = "
         "(0, 0.50, 0.25, 0.25). β·M·r = 0.8·(0,0.5,0.25,0.25) = (0, 0.40, 0.20, 0.20). "
         "(1−β)/N = 0.2/4 = 0.05. "
         "→ r<sup>(1)</sup> = (0.05, 0.45, 0.25, 0.25). Sum = 1.00 ✓.<br/><br/>"
         "<b>Spider trap?</b> Yes — once the surfer enters {2,3,4} from node 1 it cannot leave: "
         "2→3→4→2 is a cycle entirely inside the set. Without teleport, all rank flows there. "
         "With β=0.8, teleport pulls back about 0.05 to node 1 every step, so node 1 keeps positive (small) rank."),
        ("A5",
         "M·(0.3, 0.4, 0.3): r<sub>y</sub>=0.3·0.5+0.4·0.5 = 0.35; r<sub>a</sub>=0.3·0.5+0.3 = 0.45; "
         "r<sub>m</sub>=0.4·0.5 = 0.20. r<sup>(t+1)</sup> = (0.35, 0.45, 0.20). "
         "|r<sup>(t+1)</sup>−r<sup>(t)</sup>|<sub>1</sub> = |0.35−0.30|+|0.45−0.40|+|0.20−0.30| = 0.05+0.05+0.10 = 0.20. "
         "0.20 &gt; 0.05, so the algorithm has NOT converged."),
        ("A6",
         "<b>Step 1: M·r<sup>(0)</sup>.</b> r<sup>(0)</sup>=(0.25, 0.25, 0.25, 0.25). "
         "r<sub>A</sub>′ = 0+0.5·0.25+0+0 = 0.125; "
         "r<sub>B</sub>′ = 0.5·0.25+0+1·0.25+0 = 0.375; "
         "r<sub>C</sub>′ = 0+0.5·0.25+0+1·0.25 = 0.375; "
         "r<sub>D</sub>′ = 0.5·0.25+0+0+0 = 0.125. "
         "→ M·r<sup>(0)</sup> = (0.125, 0.375, 0.375, 0.125). Sum = 1 ✓ (no dead-ends here).<br/><br/>"
         "<b>Step 2: β·M·r.</b> 0.8·(0.125, 0.375, 0.375, 0.125) = (0.100, 0.300, 0.300, 0.100). S = 0.800.<br/><br/>"
         "<b>Step 3: add teleport.</b> (1−β)/N = 0.2/4 = 0.05. "
         "→ r<sup>(1)</sup> = (0.150, 0.350, 0.350, 0.150). Sum = 1.000 ✓."),
        ("A7",
         "The flow equation r = M·r is exactly the eigenvalue equation A·x = λ·x with A=M, x=r, λ=1. "
         "So r is an eigenvector of M with eigenvalue 1. For a column-stochastic non-negative matrix M, "
         "the all-ones row vector multiplied by M gives the row of column sums, which is all-ones — "
         "this means the all-ones vector is a LEFT eigenvector with eigenvalue 1. "
         "By the Perron–Frobenius theorem (for non-negative matrices), the largest eigenvalue equals the "
         "spectral radius and is real and ≥ 0. Combined with the row argument, λ<sub>max</sub> = 1, with the "
         "principal RIGHT eigenvector being the stationary PageRank vector r."),
        ("A8",
         "<b>Spider trap.</b> (a) The rank inside the trap grows monotonically; eventually all rank "
         "concentrates in the trap. (b) The Markov chain becomes <i>reducible</i> — once you enter, you "
         "cannot reach states outside the trap. Aperiodicity may also be violated. (c) Teleport gives the "
         "surfer probability 1−β to escape every step, restoring irreducibility. "
         "<br/><br/><b>Dead-end.</b> (a) The total rank decays — eventually every entry approaches 0. "
         "(b) M is no longer column-stochastic (the dead-end's column is all zeros), so M·r does not preserve "
         "the L1 norm. (c) Either remove dead-ends from M before iterating, or leave them in and re-inject "
         "the leaked mass (1−S)/N uniformly to every page each iteration."),
        ("A9",
         "β must balance two effects: (i) <b>fidelity to the link structure</b> — high β means the "
         "rank reflects the actual web topology — and (ii) <b>convergence speed and escape from traps</b> — "
         "lower β means faster escape. <br/>"
         "β → 1: PageRank reduces to vanilla M iteration; spider traps and dead-ends dominate; convergence "
         "becomes slow and the rank may not be unique. <br/>"
         "β → 0: rank approaches the uniform distribution because teleport dominates; the link structure is "
         "ignored. <br/>"
         "β = 0.85 (Google's choice) is empirically the sweet spot."),
        ("A10",
         "Imagine an idealized random surfer: at every page, pick one out-link uniformly at random and follow "
         "it. PageRank r<sub>j</sub> equals the fraction of time, in the long run, that the surfer is at "
         "page j — this is the stationary distribution of the Markov chain whose transition matrix is M.<br/>"
         "Without teleport, the chain may be reducible (spider traps) or sub-stochastic (dead-ends), so a "
         "stationary distribution may not exist or may not be unique. With teleport, the modified chain is "
         "stochastic, irreducible, and aperiodic — by the fundamental theorem of Markov chains, a unique "
         "stationary distribution exists and any starting distribution converges to it."),
        ("A11",
         "Algebraic equivalence (no dead-ends): A = β·M + (1−β)/N · J. "
         "Then A·r = β·M·r + (1−β)/N · J·r. Since Σr<sub>i</sub> = 1, J·r = 1<sub>N</sub> (the all-ones vector "
         "times 1). So A·r = β·M·r + (1−β)/N · 1<sub>N</sub>, exactly the tax-and-redistribute form. ✓<br/>"
         "With dead-ends, M is sub-stochastic so M·r sums to some S &lt; 1. The tax-and-redistribute form "
         "would only redistribute (1−β) mass when in fact (1−β) + (1−S)·β mass needs redistributing. "
         "The fix is to replace (1−β)/N with (1−S)/N, where S = β·Σ(M·r). This guarantees Σr<sup>new</sup>=1."),
        ("A12",
         "<b>(B)</b> is correct. (A) is wrong — column-stochastic means columns sum to 1, not rows. "
         "(C) is wrong if M has dead-ends — sub-stochastic columns cause leakage. "
         "(D) is wrong — column-stochastic only requires non-negative entries, not strictly positive."),
        ("A13",
         "<b>(A)</b> the principal eigenvector with eigenvalue 1. (B) is wrong because power iteration "
         "specifically picks out the dominant eigenvector. (C) is wrong because if r<sup>(0)</sup> sums to 1 "
         "and M is stochastic, every iterate sums to 1. (D) is wrong because — for an irreducible aperiodic "
         "chain — the limit is independent of the starting distribution."),
        ("A14",
         "<b>False.</b> Increasing β makes the second-largest eigenvalue of A closer to 1 (the convergence "
         "rate is governed by |λ<sub>2</sub>| ≈ β), so power iteration converges <i>more slowly</i>. β=0.85 "
         "is a balance: high enough to preserve link signal, low enough to converge in ~50 iterations."),
        ("A15",
         "Per-page leak correction = (1 − S)/N = (1 − 0.92)/100 = 0.08/100 = 0.0008. <b>Answer (A)</b>. "
         "Note: this is independent of β — once you have the leaked mass S, you redistribute the missing "
         "fraction uniformly across all N pages."),
    ]
    for aid, body in answers:
        flow.append(KeepTogether([
            P(f"<b>{aid}</b>", "AnsTitle"),
            P(body, "AnsBody"),
            Spacer(1, 0.2*cm),
        ]))
    return flow


# ════════════════════════════════════════════════════════════════════════
#  REVISION SHEET + REFERENCE SHEET
# ════════════════════════════════════════════════════════════════════════

def revision_sheet():
    flow = []
    flow.append(PageBreak())
    flow.append(section_bar("§ 13   ENDING KEY NOTES — REVISION CARDS", REV_RED))
    flow.append(P("Read these in the last 30 minutes before walking into the hall. "
                  "Every card is one definition / formula / common mistake — bite-sized for last-minute recall.",
                  "Body"))
    cards = [
        ("Out-degree d<sub>i</sub>",
         "Number of out-links from page i. The denominator in the flow equation."),
        ("Flow equation",
         "r<sub>j</sub> = Σ<sub>i→j</sub> r<sub>i</sub>/d<sub>i</sub>. Sum of incoming rank shares."),
        ("Stochastic matrix M",
         "M<sub>ji</sub> = 1/d<sub>i</sub> if i→j else 0. Each <i>column</i> sums to 1."),
        ("Matrix form",
         "r = M·r. Means r is the eigenvector of M with eigenvalue 1."),
        ("Power iteration",
         "r<sup>(t+1)</sup> = M·r<sup>(t)</sup>. Start uniform, ~50 iters to converge."),
        ("Random walk view",
         "r<sub>j</sub> = stationary probability of a random surfer being at page j."),
        ("Stationary distribution conditions",
         "Markov chain must be (i) stochastic, (ii) aperiodic, (iii) irreducible."),
        ("Spider trap",
         "Set of pages whose all out-links stay inside. Rank concentrates in the trap."),
        ("Dead-end",
         "Page with no out-links. Column of M is all-zero → mass leaks → ranks decay to 0."),
        ("Teleport (Google fix)",
         "With prob. 1−β, jump to a random page. β ≈ 0.8–0.9. Fixes both pathologies."),
        ("Google matrix A",
         "A = β·M + (1−β)/N · J<sub>N×N</sub>. Stochastic, aperiodic, irreducible."),
        ("Tax & redistribute",
         "r<sup>new</sup> = β·M·r<sup>old</sup> + (1−β)/N · 1<sub>N</sub> (no dead-ends)."),
        ("Leak handling (with dead-ends)",
         "S = Σ(β·M·r<sup>old</sup>); add (1−S)/N to every entry instead of (1−β)/N."),
        ("Convergence test",
         "|r<sup>(t+1)</sup> − r<sup>(t)</sup>|<sub>1</sub> &lt; ε. Common ε ≈ 10<sup>−6</sup>."),
        ("Common mistake — out vs in",
         "r<sub>i</sub>/d<sub>i</sub>: d<sub>i</sub> is SOURCE i's OUT-degree. Not target's in-degree."),
        ("Common mistake — column vs row",
         "M is column-stochastic. M<sub>ji</sub> = column i, row j. Many students transpose by mistake."),
        ("Eigenvalue intuition",
         "Largest eigenvalue of column-stochastic M is exactly 1. Principal eigenvector = PageRank."),
        ("β semantics",
         "β = expected number of link follows before a teleport. β=0.85 → ~6.7 link clicks on average."),
    ]
    # Build a 2-column table of cards
    rows = []
    for i in range(0, len(cards), 2):
        left = (Paragraph(f"<b>{cards[i][0]}</b><br/>{cards[i][1]}", S["RevBody"])
                if i < len(cards) else Paragraph("", S["RevBody"]))
        right = (Paragraph(f"<b>{cards[i+1][0]}</b><br/>{cards[i+1][1]}", S["RevBody"])
                 if i+1 < len(cards) else Paragraph("", S["RevBody"]))
        rows.append([left, right])
    col_w = (USABLE_W - 4) / 2
    tbl = Table(rows, colWidths=[col_w, col_w])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), REV_BG),
        ("BOX",(0,0),(-1,-1),0.5, REV_RED),
        ("INNERGRID",(0,0),(-1,-1),0.4, HexColor("#D8B0B0")),
        ("LEFTPADDING",(0,0),(-1,-1),8),
        ("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
    ]))
    flow.append(tbl)
    return flow


def reference_sheet():
    flow = []
    flow.append(PageBreak())
    flow.append(section_bar("§ 14   PAGERANK FORMULA & ALGORITHM REFERENCE", REF_INDIGO))
    flow.append(P("Quick-look reference. Memorize the eight rows. Every numerical PageRank exam question "
                  "reduces to one of them.", "Body"))
    flow.append(Spacer(1, 0.2*cm))
    rows = [
        ["Concept", "Formula / Statement", "When to use it"],
        ["Flow equation",
         "r<sub>j</sub> = Σ<sub>i→j</sub> r<sub>i</sub>/d<sub>i</sub>",
         "Defining PageRank from the link graph."],
        ["Matrix form",
         "r = M·r where M<sub>ji</sub>=1/d<sub>i</sub> if i→j else 0",
         "Compact statement; basis of all algorithms."],
        ["Eigenvector view",
         "r is the principal eigenvector of M with eigenvalue 1",
         "Justifying convergence of power iteration."],
        ["Power iteration",
         "r<sup>(t+1)</sup> = M·r<sup>(t)</sup>, r<sup>(0)</sup>=1/N",
         "Practical computation when M is well-behaved."],
        ["Random walk",
         "r is the stationary distribution of the Markov chain M",
         "Probabilistic interpretation; intuition for teleport."],
        ["Google formulation",
         "r = β·M·r + (1−β)/N · 1<sub>N</sub>",
         "Default formula when graph has spider traps but no dead-ends."],
        ["Google matrix",
         "A = β·M + (1−β)/N · J<sub>N×N</sub>",
         "Algebraic / theoretical statement of the teleport fix."],
        ["Complete algorithm (with leak)",
         "r<sup>new</sup><sub>j</sub> = β·(M·r<sup>old</sup>)<sub>j</sub> + (1−S)/N where S=Σ(β·M·r<sup>old</sup>)",
         "Production form — handles dead-ends without removing them."],
        ["Convergence threshold",
         "Stop when Σ<sub>j</sub>|r<sup>new</sup><sub>j</sub>−r<sup>old</sup><sub>j</sub>| &lt; ε",
         "Practical halting criterion. ε ≈ 10<sup>−6</sup>."],
    ]
    flow.extend(autofit_table(rows, header=True,
                              alignments=["L","L","L"],
                              caption="Table 14.1. PageRank reference card."))
    flow.append(Spacer(1, 0.2*cm))
    flow.append(P("<b>Algorithmic complexity quick reference:</b>", "RefTitle"))
    flow.append(P("• One iteration of power method on sparse M: <b>O(N + E)</b> arithmetic operations, where "
                  "E is the number of edges.", "Bullet"))
    flow.append(P("• Storage for sparse M: ~10 bytes per edge (with 32-bit indices) → ~100 GB for the 2014 web "
                  "(~10<sup>10</sup> edges).", "Bullet"))
    flow.append(P("• Typical iterations to converge with β=0.85: 50–100 to ε=10<sup>−6</sup>.", "Bullet"))
    flow.append(P("• Block-stripe matrix update: split r<sup>new</sup> into k blocks, multiply M against each "
                  "in turn — O(N + E) work but only ~N/k working memory.", "Bullet"))
    flow.append(Spacer(1, 0.4*cm))
    flow.append(P("<b>Where this connects to other weeks:</b>", "RefTitle"))
    flow.append(P("• <b>W12 — Topic-Sensitive PageRank, TrustRank, HITS</b>: variants of PageRank that bias "
                  "the teleport vector (instead of uniform 1/N) toward a topic or trust set, plus the "
                  "complementary Hubs-and-Authorities decomposition. Walk into W12 already owning §3–§9 and you "
                  "save ~40% of the prep time.", "Bullet"))
    flow.append(P("• <b>W16 — Community Detection</b>: spectral methods cluster the graph using the same "
                  "eigenvector machinery introduced here, applied to a different matrix (the graph Laplacian).",
                  "Bullet"))
    flow.append(P("• <b>MapReduce iteration</b> (briefly mentioned in slides; depth in MMDS §5.2.2): each "
                  "iteration's matrix–vector multiply distributes across mappers (one per row of M); reducers "
                  "sum the contributions. Beyond the slide-level scope but useful for the lab final.", "Bullet"))
    return flow


# ════════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════════

def main():
    doc = make_doc(
        out_path=OUT,
        title="BDA Week 8-9 PageRank — Final Exam Prep",
        header_text="W08-09 · Graph Mining: PageRank",
        footer_text="CS-404 BDA · Final Exam Prep · Comprehensive Tutor PDF",
    )
    story = []
    story.extend(cover_page())
    story.extend(toc_page())
    story.extend(beginning_key_notes())
    story.extend(why_pagerank())
    story.extend(flow_formulation())
    story.extend(matrix_formulation())
    story.extend(eigenvector_power_iter())
    story.extend(random_walk())
    story.extend(convergence_problems())
    story.extend(google_solution())
    story.extend(complete_algorithm())
    story.extend(worked_examples())
    story.extend(practice_questions())
    story.extend(full_answers())
    story.extend(revision_sheet())
    story.extend(reference_sheet())
    doc.build(story)
    # Verify file exists and print size
    p = Path(OUT)
    print(f"[w89] PDF built: {p.resolve()} — {p.stat().st_size/1024:.1f} KB")


if __name__ == "__main__":
    main()
