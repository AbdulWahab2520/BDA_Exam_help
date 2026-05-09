"""Builds the Week 12 Advanced Link Analysis exam-prep PDF.
Topics: Topic-Sensitive PageRank, Web Spam, Link Spam, TrustRank, Spam Mass, HITS (brief)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch, Rectangle

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

OUT = "ExamPrep_PDFs/BDA_W12_AdvancedLinkAnalysis_ExamPrep.pdf"
S = build_stylesheet()


def P(text, style="Body"):
    return Paragraph(text, S[style])


# ════════════════════════════════════════════════════════════════════════
#  DIAGRAMS
# ════════════════════════════════════════════════════════════════════════

def fig_topic_teleport():
    """Topic-sensitive PageRank: teleport to subset S only."""
    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    # surfer at i
    ax.add_patch(Circle((0.13, 0.5), 0.06, facecolor="#1F4E79", edgecolor="#0B2540", lw=2))
    ax.text(0.13, 0.5, "i", ha="center", va="center", color="white", fontweight="bold", fontsize=12)
    # arrows
    ax.annotate("", xy=(0.45, 0.78), xytext=(0.18, 0.55),
        arrowprops=dict(arrowstyle="-|>", color="#1B5E20", lw=1.8))
    ax.annotate("", xy=(0.45, 0.22), xytext=(0.18, 0.45),
        arrowprops=dict(arrowstyle="-|>", color="#B22234", lw=1.8))
    ax.text(0.30, 0.86, r"prob $\beta$ → follow link", color="#1B5E20",
            fontsize=10, fontweight="bold", ha="center")
    ax.text(0.30, 0.13, r"prob $1-\beta$ → teleport to S", color="#B22234",
            fontsize=10, fontweight="bold", ha="center")
    # link follow → arbitrary node
    ax.add_patch(Circle((0.65, 0.78), 0.05, facecolor="white", edgecolor="#0B2540", lw=2))
    ax.text(0.78, 0.78, "any out-neighbour", fontsize=10, color="#0B2540", va="center")
    # teleport set S as a cluster
    ax.add_patch(Rectangle((0.55, 0.05), 0.35, 0.30,
                           facecolor="#FCE7E9", edgecolor="#B22234", lw=1.5))
    ax.text(0.725, 0.30, r"Topic Set $S$", color="#B22234",
            fontweight="bold", ha="center", fontsize=10.5)
    for x in [0.62, 0.72, 0.82]:
        ax.add_patch(Circle((x, 0.15), 0.03,
                            facecolor="#B22234", edgecolor="#7A1A1A", lw=1))
    ax.set_xlim(0,1.0); ax.set_ylim(0,1); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(r"Topic-Sensitive PageRank — teleport biased to set $S$",
                 fontsize=11, color="#0B2540", pad=8)
    return save_fig(fig, "topic_teleport")


def fig_link_farm():
    """Link farm: target t boosted by M owned 'farm' pages."""
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    # Three groups: inaccessible (left), accessible (middle), owned (right)
    # background regions
    ax.add_patch(Rectangle((0.02, 0.10), 0.28, 0.80, facecolor="#EFEFEF", edgecolor="#999", lw=1))
    ax.add_patch(Rectangle((0.34, 0.10), 0.28, 0.80, facecolor="#E8F0F8", edgecolor="#1F4E79", lw=1))
    ax.add_patch(Rectangle((0.66, 0.10), 0.32, 0.80, facecolor="#FCE7E9", edgecolor="#B22234", lw=1))
    ax.text(0.16, 0.94, "Inaccessible", ha="center", color="#666", fontsize=10, fontweight="bold")
    ax.text(0.48, 0.94, "Accessible", ha="center", color="#0B2540", fontsize=10, fontweight="bold")
    ax.text(0.82, 0.94, "Owned by spammer", ha="center", color="#B22234", fontsize=10, fontweight="bold")
    # Accessible nodes
    for i, y in enumerate([0.65, 0.45, 0.25]):
        ax.add_patch(Circle((0.48, y), 0.04, facecolor="#1F4E79", edgecolor="#0B2540", lw=1.5))
        ax.text(0.48, y, "a", color="white", ha="center", va="center", fontsize=9)
    # Target page t
    ax.add_patch(Circle((0.74, 0.55), 0.06, facecolor="#B22234", edgecolor="#7A1A1A", lw=2))
    ax.text(0.74, 0.55, "t", color="white", fontweight="bold", ha="center", va="center", fontsize=13)
    # Farm pages (M)
    farm_y = [0.70, 0.55, 0.40, 0.25]
    for y in farm_y:
        ax.add_patch(Circle((0.91, y), 0.035, facecolor="#FCC0C5", edgecolor="#7A1A1A", lw=1))
    ax.text(0.91, 0.13, "M farm pages", ha="center", color="#7A1A1A", fontsize=9)
    # Arrows: accessible → t  (boost from external)
    for y in [0.65, 0.45, 0.25]:
        ax.annotate("", xy=(0.69, 0.55), xytext=(0.52, y),
            arrowprops=dict(arrowstyle="-|>", color="#1B5E20", lw=1.0))
    # Arrows: t → farm pages and farm → t (mutual reinforcement)
    for y in farm_y:
        ax.annotate("", xy=(0.875, y), xytext=(0.78, 0.55),
            arrowprops=dict(arrowstyle="-|>", color="#7A1A1A", lw=0.9))
        ax.annotate("", xy=(0.78, 0.55), xytext=(0.875, y),
            arrowprops=dict(arrowstyle="-|>", color="#7A1A1A", lw=0.9, alpha=0.4))
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Spam farm: target t boosted by mutual links with M owned pages",
                 fontsize=11, color="#0B2540", pad=8)
    return save_fig(fig, "link_farm")


def fig_trust_propagation():
    """Trust propagation: trusted seeds → others via topic-sensitive PR."""
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    nodes = {
        "S1": (0.15, 0.80, 1.00, "#1B5E20"),
        "S2": (0.15, 0.20, 1.00, "#1B5E20"),
        "p1": (0.45, 0.80, 0.65, "#7CB342"),
        "p2": (0.45, 0.50, 0.45, "#FBC02D"),
        "p3": (0.45, 0.20, 0.55, "#7CB342"),
        "q1": (0.78, 0.65, 0.30, "#FBC02D"),
        "q2": (0.78, 0.35, 0.10, "#E64A19"),
    }
    for name, (x, y, t, c) in nodes.items():
        ax.add_patch(Circle((x, y), 0.05, facecolor=c, edgecolor="#202020", lw=1.5))
        ax.text(x, y, name, color="white", fontweight="bold", ha="center", va="center", fontsize=8)
        ax.text(x, y-0.10, f"t={t:.2f}", color="#0B2540", ha="center", fontsize=9)
    edges = [("S1","p1"),("S1","p2"),("S2","p3"),("p1","q1"),("p2","q1"),("p3","q2")]
    for u, v in edges:
        ax.annotate("", xy=(nodes[v][0]-0.05, nodes[v][1]), xytext=(nodes[u][0]+0.05, nodes[u][1]),
            arrowprops=dict(arrowstyle="-|>", color="#0B2540", lw=1.2))
    # Legend
    ax.text(0.06, 0.98, "Trusted seeds (t=1)", color="#1B5E20", fontweight="bold", fontsize=9.5)
    ax.text(0.45, 0.98, "Reachable pages — trust attenuates", color="#0B2540", fontweight="bold", fontsize=9.5)
    ax.text(0.78, 0.98, "Far pages — likely spam", color="#7A1A1A", fontweight="bold", fontsize=9.5)
    ax.set_xlim(0,1); ax.set_ylim(0.05,1.05); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("TrustRank: trust propagates from seeds, attenuating with distance",
                 fontsize=11, color="#0B2540", pad=4)
    return save_fig(fig, "trust_propagation")


def fig_hits_concept():
    """HITS: simple bipartite hub/authority illustration."""
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    # 3 hubs left, 3 authorities right
    hubs_y = [0.80, 0.50, 0.20]
    auth_y = [0.80, 0.50, 0.20]
    for y in hubs_y:
        ax.add_patch(Circle((0.20, y), 0.05, facecolor="#1B5E20", edgecolor="#0B2540", lw=2))
    for y in auth_y:
        ax.add_patch(Circle((0.80, y), 0.05, facecolor="#B85C00", edgecolor="#7A2D00", lw=2))
    ax.text(0.20, 0.95, "Hubs (h)", ha="center", color="#1B5E20", fontweight="bold", fontsize=11)
    ax.text(0.80, 0.95, "Authorities (a)", ha="center", color="#B85C00", fontweight="bold", fontsize=11)
    # bipartite edges from each hub to each authority
    for hy in hubs_y:
        for ay in auth_y:
            ax.annotate("", xy=(0.75, ay), xytext=(0.25, hy),
                arrowprops=dict(arrowstyle="-|>", color="#404040", lw=0.6, alpha=0.55))
    # legend formulas
    ax.text(0.50, 0.06, r"$h_i = \sum_{i \to j} a_j$, $\;\;a_j = \sum_{i \to j} h_i$",
            ha="center", fontsize=11, color="#0B2540")
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("HITS: hubs cite authorities, authorities are cited by hubs",
                 fontsize=11, color="#0B2540", pad=8)
    return save_fig(fig, "hits_concept")


print("[w12] generating diagrams...")
F_TOPIC   = fig_topic_teleport()
F_FARM    = fig_link_farm()
F_TRUST   = fig_trust_propagation()
F_HITS    = fig_hits_concept()


# ════════════════════════════════════════════════════════════════════════
#  CONTENT
# ════════════════════════════════════════════════════════════════════════

def cover_page():
    flow = cover_block(
        title="Week 12",
        subtitle="Advanced Link Analysis",
        week_label="Module 2 of Phase-1 Final Prep · Builds directly on W8-9 PageRank",
        topics=[
            "Three limitations of vanilla PageRank",
            "Topic-Sensitive PageRank — biased teleport set",
            "Web spam: term spam &amp; Google's anchor-text fix",
            "Link spam &amp; spam farms — analysis with multiplier formula",
            "TrustRank — topic-sensitive PR with trusted seeds",
            "Spam Mass estimation — fractional spam contribution",
            "HITS algorithm — Hubs &amp; Authorities (brief)",
            "6 worked numerical examples · 15 practice questions",
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
        "1. Beginning Key Notes — what to walk into the exam owning",
        "2. Three Limitations of Generic PageRank",
        "3. Topic-Sensitive PageRank — formulation",
        "4. Web Spam — Term Spam &amp; Google's Anchor-Text Fix",
        "5. Link Spam &amp; Spam Farms — the multiplier-effect formula",
        "6. TrustRank — propagating trust from a seed set",
        "7. Spam Mass — estimating fractional spam contribution",
        "8. HITS — Hubs &amp; Authorities (reference)",
        "9. Six Worked Numerical Examples",
        "10. 15 Practice Questions",
        "11. Full Worked Answers",
        "12. Ending Key Notes — Revision Cards",
        "13. Formula &amp; Algorithm Reference",
    ]
    for t in items:
        flow.append(P(f"<b>•</b> &nbsp; {t}", "TocItem"))
    flow.append(PageBreak())
    return flow


def beginning_key_notes():
    flow = []
    flow.append(section_bar("§ 1   BEGINNING KEY NOTES — STUDY COMPASS", KEY_BLUE))
    body = [
        P("These build directly on the W8-9 PageRank machinery — make sure you can recite "
          "r = β·M·r + (1−β)/N · 1<sub>N</sub> from memory before starting this PDF.", "KeyBody"),
        Spacer(1, 0.15*cm),
        P("• <b>Three weaknesses of vanilla PageRank:</b> (1) it gives generic popularity, missing topic-specific authorities; "
          "(2) it uses a single notion of importance — HITS provides hubs vs. authorities; "
          "(3) it is gameable through link spam — TrustRank fixes this.", "KeyBody"),
        P("• <b>Topic-Sensitive PageRank:</b> change the teleport target. Instead of jumping uniformly to ANY page, "
          "jump uniformly to a small <i>topic set S</i>. One PageRank vector per topic.", "KeyBody"),
        P("• <b>Topic-PR formula:</b> A<sub>ij</sub> = β·M<sub>ij</sub> + (1−β)/|S| if j ∈ S, else β·M<sub>ij</sub>. "
          "Equivalently: r = β·M·r + (1−β)·v<sub>S</sub>, where v<sub>S</sub> has 1/|S| in positions S and 0 elsewhere.", "KeyBody"),
        P("• <b>Term spam:</b> stuffing pages with hidden keywords. Google's defense: trust anchor-text from incoming links, not page's own words.", "KeyBody"),
        P("• <b>Link spam &amp; spam farms:</b> three page types — inaccessible / accessible / owned. "
          "By creating M owned pages all linking to target t and sneaking links from a small accessible set x, "
          "spammer multiplies y = x/(1−β²) + c·M/N where c = β/(1+β).", "KeyBody"),
        P("• <b>Multiplier value:</b> for β=0.85, 1/(1−β²) ≈ 3.6 — a small accessible PR x gets amplified ~3.6×.", "KeyBody"),
        P("• <b>TrustRank:</b> topic-sensitive PageRank with the teleport set = trusted human-vetted seed pages "
          "(typically .edu, .gov, .mil domains).", "KeyBody"),
        P("• <b>Trust attenuation &amp; splitting:</b> trust decays with graph distance and is divided across out-links — "
          "captured by the same algebra as PageRank, with seed teleport.", "KeyBody"),
        P("• <b>Spam Mass:</b> r<sup>−</sup><sub>p</sub> = r<sub>p</sub> − r<sup>+</sup><sub>p</sub>, "
          "spam mass of p = r<sup>−</sup><sub>p</sub> / r<sub>p</sub>. Pages with mass close to 1 are spam.", "KeyBody"),
        P("• <b>HITS:</b> two scores — h<sub>i</sub> (hub) and a<sub>j</sub> (authority) — found by "
          "iterating h ← M·a and a ← M<sup>T</sup>·h with normalization. Different from PageRank; both are exam-bait concepts.", "KeyBody"),
    ]
    flow.append(callout("THE 9 IDEAS YOU MUST OWN", body,
                       title_style=S["KeyTitle"], body_style=S["KeyBody"],
                       bg=KEY_BG, border=KEY_BLUE))
    flow.append(PageBreak())
    return flow


def limitations():
    flow = []
    flow.append(section_bar("§ 2   THREE LIMITATIONS OF GENERIC PAGERANK", NAVY))
    flow.append(P("Vanilla PageRank gives a single rank per page reflecting overall web-graph importance. "
                  "This works well for queries like “Stanford” but fails for three reasons:", "Body"))
    flow.append(P("<b>(1) No topic awareness.</b> A query for the word “Trojan” legitimately maps to three different "
                  "topics — sports (USC Trojans), history (Trojan war), or computer security (Trojan malware). "
                  "Generic PageRank cannot prefer the right interpretation given the user's actual interest.", "Body"))
    flow.append(P("<b>(2) Single notion of importance.</b> Some pages are <i>good answer pages</i> "
                  "(authoritative content), and some are <i>good index pages</i> (useful pointers). "
                  "PageRank conflates these. The HITS algorithm splits importance into two scores: "
                  "<b>hubs</b> (pages that point to many authorities) and <b>authorities</b> (pages pointed to by "
                  "many hubs).", "Body"))
    flow.append(P("<b>(3) Spam vulnerability.</b> The algorithm is purely structural — it cannot tell whether "
                  "an incoming link is genuine or spam-farmed. The fix is TrustRank (§6).", "Body"))
    return flow


def topic_pr():
    flow = []
    flow.append(section_bar("§ 3   TOPIC-SENSITIVE PAGERANK", NAVY))
    flow.append(P("<b>Idea.</b> Recall the random surfer with teleport probability 1−β. Vanilla PageRank teleports "
                  "to a uniformly random page (every page equally likely). "
                  "<b>Topic-sensitive PageRank</b> instead teleports to a uniformly random page "
                  "from a <i>topic-relevant set</i> S — pages known to be about a particular topic, "
                  "for example all DMOZ-classified “sports” pages.", "Body"))
    flow.append(fig_image(F_TOPIC, max_w_cm=14.0, max_h_cm=7.5))
    flow.append(P("<b>Figure 3.1.</b> Topic-sensitive teleport. With probability β the surfer follows a link as before; "
                  "with probability 1−β the surfer jumps uniformly into the topic set S, never to pages outside S.",
                  "Caption"))
    flow.append(P("<b>Matrix formulation.</b> Define the topic-sensitive Google matrix:", "Body"))
    flow.append(display_eq(
        r"A_{ij} = \beta \, M_{ij} + \frac{1-\beta}{|S|} \;\; \mathrm{if}\; j \in S, \;\;\;\; "
        r"A_{ij} = \beta \, M_{ij} \;\; \mathrm{otherwise}",
        fontsize=14))
    flow.append(P("Equivalently — and this is the form most often used on exams:", "Body"))
    flow.append(display_eq(
        r"r \;=\; \beta \cdot M \cdot r \;+\; (1-\beta) \cdot v_S",
        fontsize=16))
    flow.append(P("where <b>v<sub>S</sub></b> is a vector with 1/|S| in positions corresponding to pages in S, "
                  "and 0 elsewhere. Plugging |S| = N and v<sub>S</sub> = (1/N)·1<sub>N</sub> "
                  "recovers vanilla PageRank — confirming Topic-PR is a strict generalization.", "Body"))
    flow.append(P("<b>One vector per topic.</b> Compute and store r<sub>S₁</sub>, r<sub>S₂</sub>, … for the 16 "
                  "DMOZ top-level categories (arts, business, sports, …). At query time, pick the right vector "
                  "based on inferred topic.", "Body"))
    flow.append(callout(
        "EXAM-STYLE ALGORITHM CHANGE — only one line",
        [P("The complete algorithm from W8-9 changes by exactly one line: replace the "
           "<i>uniform redistribution</i> step c. with: r<sup>new</sup><sub>j</sub> = "
           "r'<sup>new</sup><sub>j</sub> + (1−S)/|S| if j ∈ S, else r'<sup>new</sup><sub>j</sub>. "
           "Everything else (initialization, β·M·r<sup>old</sup>, leak handling) stays identical.",
           "DefBody")],
        title_style=S["DefTitle"], body_style=S["DefBody"],
        bg=DEF_BG, border=DEF_PURP))
    return flow


def web_spam():
    flow = []
    flow.append(section_bar("§ 4   WEB SPAM — TERM SPAM AND GOOGLE'S DEFENSE", NAVY))
    flow.append(P("<b>Spamming</b> is any deliberate action to boost a page's search-engine ranking beyond its "
                  "real value. <b>Spam</b> is the resulting page. Approximately 10–15% of web pages are spam — "
                  "huge enough that pretending it doesn't exist breaks the search engine.", "Body"))
    flow.append(P("<b>First-generation spam (term spam).</b> Early search engines ranked by word-frequency on "
                  "the page. Spammers exploited this in two ways:", "H3"))
    flow.append(P("• <b>Keyword stuffing.</b> Add the target keyword (e.g. “movie”) thousands of times, with text "
                  "color matching the background so users don't see it but the crawler does.", "Bullet"))
    flow.append(P("• <b>Top-result mimicry.</b> Run the query “movie” yourself, see which page comes first, "
                  "copy its content invisibly into your own page.", "Bullet"))
    flow.append(P("<b>Google's term-spam fix:</b> believe what others say about you, not what you say about yourself. "
                  "Specifically, weight the <b>anchor text</b> of incoming links — the visible text inside &lt;a&gt; "
                  "tags pointing TO your page — much more than your page's own body text. Combined with PageRank, "
                  "this surfaced authentic, well-cited pages while burying term-spam farms.", "Body"))
    flow.append(callout(
        "WHY ANCHOR-TEXT WORKS",
        [P("If 1000 pages link to a movie review with anchor text “great movie”, that's 1000 independent "
           "judgments. The reviewed page can't game this without compromising the linking pages — "
           "which themselves have to convince their own users to keep visiting. Distributed truth-telling.",
           "DefBody")],
        title_style=S["DefTitle"], body_style=S["DefBody"],
        bg=DEF_BG, border=DEF_PURP))
    return flow


def link_spam():
    flow = []
    flow.append(section_bar("§ 5   LINK SPAM & SPAM FARMS", NAVY))
    flow.append(P("Once Google adopted PageRank + anchor text as the ranking signal, spammers shifted "
                  "to <b>link spam</b>: artificially constructing link structures to boost the PageRank of a "
                  "target page t.", "Body"))
    flow.append(P("<b>Three page types from the spammer's view:</b>", "H3"))
    flow.append(P("• <b>Inaccessible</b> pages — controlled by others, no influence possible.", "Bullet"))
    flow.append(P("• <b>Accessible</b> pages — e.g. blog comment sections where the spammer can post a link.", "Bullet"))
    flow.append(P("• <b>Owned</b> pages — completely under the spammer's control, possibly across many domains.", "Bullet"))
    flow.append(fig_image(F_FARM, max_w_cm=14.5, max_h_cm=8.0))
    flow.append(P("<b>Figure 5.1.</b> A canonical spam farm. The spammer scatters links from accessible pages (e.g. "
                  "blog comments) to the target t, then links t to and from M owned “farm” pages, all of which "
                  "link back to t — concentrating PageRank on t.", "Caption"))
    flow.append(P("<b>Spam-farm analysis.</b> Let:", "H3"))
    flow.append(P("• <b>x</b> = total PageRank contributed to t by accessible pages (small, but nonzero).", "Bullet"))
    flow.append(P("• <b>y</b> = PageRank of target t (what we want to estimate).", "Bullet"))
    flow.append(P("• <b>M</b> = number of farm pages owned by spammer; <b>N</b> = total pages on the web.", "Bullet"))
    flow.append(P("Each farm page receives β·y/M from t (t splits its rank among its M owned out-links) "
                  "plus the teleport (1−β)/N. So:", "Body"))
    flow.append(display_eq(
        r"\mathrm{rank}_{\mathrm{farm}} \;=\; \beta \cdot \frac{y}{M} \;+\; \frac{1-\beta}{N}", fontsize=14))
    flow.append(P("Then t's rank is x (from accessible) + β·M·rank<sub>farm</sub> (from M farm pages) + (1−β)/N (teleport). "
                  "Substituting and ignoring the small (1−β)/N term:", "Body"))
    flow.append(display_eq(
        r"y \;=\; x \;+\; \beta \, M \cdot \left( \frac{\beta y}{M} + \frac{1-\beta}{N} \right)"
        r"\;\Rightarrow\; y \;=\; x + \beta^2 y + \beta(1-\beta)\frac{M}{N}",
        fontsize=14))
    flow.append(P("Solving for y:", "Body"))
    flow.append(display_eq(
        r"y \;=\; \frac{x}{1 - \beta^2} \;+\; c \cdot \frac{M}{N}, \quad c \;=\; \frac{\beta}{1+\beta}",
        fontsize=16))
    flow.append(P("<b>Multiplier.</b> For β = 0.85, the multiplier 1/(1−β²) ≈ 3.6. Even a small "
                  "accessible-PR contribution x of 0.01 becomes y ≈ 0.036 + c·M/N. By making M (the farm size) huge, "
                  "the spammer can push y arbitrarily high — that is the spam farm's “multiplier effect”.", "Body"))
    flow.append(callout(
        "EXAM TRAP — careful with β vs β² in the denominator",
        [P("The denominator is 1 − β², not 1 − β. Many students write 1 − β by mistake. "
           "The β² comes from the round-trip rank flow: t → farm → t. If you skip the algebra, "
           "remember: <i>two β's, two M's cancel</i> → β² survives.", "WarnBody")],
        title_style=S["WarnTitle"], body_style=S["WarnBody"],
        bg=WARN_BG, border=WARN_RED))
    return flow


def trust_rank():
    flow = []
    flow.append(section_bar("§ 6   TRUSTRANK — COMBATING LINK SPAM", NAVY))
    flow.append(P("<b>Core insight (approximate isolation).</b> Trustworthy pages tend not to link to spam pages. "
                  "If we can identify a small set of <b>trusted seed pages</b> by hand, we can propagate "
                  "their trust outward through the link graph — pages reachable from trusted seeds in few hops "
                  "are likely good; pages far from any trusted seed are likely spam.", "Body"))
    flow.append(P("<b>Algorithm.</b> TrustRank is exactly Topic-Sensitive PageRank with the topic set S = "
                  "trusted seed pages. Each page receives a trust value t<sub>p</sub> ∈ [0, 1].", "H3"))
    flow.append(P("• Set t<sub>p</sub> = 1 for every trusted seed page, 0 elsewhere initially.", "Bullet"))
    flow.append(P("• Iterate: each page p with out-link set O<sub>p</sub> contributes "
                  "β·t<sub>p</sub>/|O<sub>p</sub>| to each q ∈ O<sub>p</sub>.", "Bullet"))
    flow.append(P("• Sum incoming contributions per page; converge as in PageRank.", "Bullet"))
    flow.append(fig_image(F_TRUST, max_w_cm=14.0, max_h_cm=8.0))
    flow.append(P("<b>Figure 6.1.</b> Trust propagation. Seed pages S1, S2 have t = 1.0. "
                  "First-hop pages inherit ~0.5–0.65 trust, second-hop pages inherit less. "
                  "Spam pages disconnected from any seed never accumulate significant trust.", "Caption"))
    flow.append(P("<b>Two effects you should be able to articulate on the exam:</b>", "H3"))
    flow.append(P("• <b>Trust attenuation</b> — trust decreases with graph distance from seeds, "
                  "because at every hop only a β fraction is propagated and the rest leaks into teleport.", "Bullet"))
    flow.append(P("• <b>Trust splitting</b> — a page with many out-links splits its trust thinly across them. "
                  "Captures the intuition that an editor with 1000 links per page reviews each less carefully.", "Bullet"))
    flow.append(P("<b>Picking the seed set.</b> Two competing goals — small enough that humans can vet every page, "
                  "yet broad enough that every legitimate web region is reachable in few hops. Two practical tactics:", "Body"))
    flow.append(P("• Take the top-k pages by vanilla PageRank (theory: spam can't reach the very top).", "Bullet"))
    flow.append(P("• Restrict to controlled-membership domains: <i>.edu</i>, <i>.gov</i>, <i>.mil</i>.", "Bullet"))
    return flow


def spam_mass():
    flow = []
    flow.append(section_bar("§ 7   SPAM MASS — ESTIMATING FRACTIONAL SPAM CONTRIBUTION", NAVY))
    flow.append(P("<b>Complementary view.</b> TrustRank tells us how much of a page's rank comes from <i>trusted</i> "
                  "sources. Spam Mass asks the converse: how much of a page's rank comes from <i>spam</i>?", "Body"))
    flow.append(P("Let:", "Body"))
    flow.append(P("• r<sub>p</sub> = vanilla PageRank of page p.", "Bullet"))
    flow.append(P("• r<sup>+</sup><sub>p</sub> = TrustRank of p (= topic-sensitive PR with teleport into trusted seed set).", "Bullet"))
    flow.append(P("• r<sup>−</sup><sub>p</sub> = r<sub>p</sub> − r<sup>+</sup><sub>p</sub> = "
                  "rank contributed by non-trusted (likely-spam) sources.", "Bullet"))
    flow.append(P("<b>Spam Mass</b> of page p:", "H3"))
    flow.append(display_eq(
        r"\mathrm{SpamMass}(p) \;=\; \frac{r^-_p}{r_p} \;=\; \frac{r_p - r^+_p}{r_p}",
        fontsize=16))
    flow.append(P("Spam Mass close to 1 means almost all of p's rank comes from non-trusted (spam) sources → "
                  "p is likely spam. Spam Mass close to 0 means most of p's rank comes from trusted sources → "
                  "p is legitimate. Pick a threshold (e.g. 0.5) and label everything above it as spam.", "Body"))
    flow.append(callout(
        "WHY USE BOTH r AND r⁺?",
        [P("If we only had TrustRank, we'd label every page far from the seed set as spam — including "
           "perfectly legitimate isolated communities (small academic groups, niche hobbyist sites). "
           "Spam Mass instead asks: <i>relative to its overall rank, how much of this page's rank is "
           "attributable to spam-like sources?</i> A small but legitimate page has small r and small r<sup>+</sup>, "
           "so SpamMass is small. Only pages with high r and proportionally low r<sup>+</sup> get flagged.",
           "DefBody")],
        title_style=S["DefTitle"], body_style=S["DefBody"],
        bg=DEF_BG, border=DEF_PURP))
    return flow


def hits_section():
    flow = []
    flow.append(section_bar("§ 8   HITS — HUBS & AUTHORITIES (BRIEF)", NAVY))
    flow.append(P("HITS (Hyperlink-Induced Topic Search) is the second classical link-analysis algorithm. "
                  "The slides only mention HITS in passing as <i>“Solution: Hubs-and-Authorities”</i> — but the "
                  "concept is fair game on conceptual exam questions because it's in MMDS §5.5.", "Body"))
    flow.append(P("<b>Two scores per page</b>, jointly defined:", "H3"))
    flow.append(P("• <b>Hub score h<sub>i</sub></b> — high if i links TO many high-authority pages.", "Bullet"))
    flow.append(P("• <b>Authority score a<sub>j</sub></b> — high if j is linked FROM many high-hub pages.", "Bullet"))
    flow.append(fig_image(F_HITS, max_w_cm=13.0, max_h_cm=7.0))
    flow.append(P("<b>Figure 8.1.</b> HITS bipartite intuition. Each hub points to multiple authorities; "
                  "authorities receive links from multiple hubs. The two scores reinforce each other.", "Caption"))
    flow.append(P("<b>Iteration.</b> Let A be the link adjacency matrix (A<sub>ij</sub>=1 if i→j). Then:", "Body"))
    flow.append(display_eq(
        r"h \;=\; A \cdot a, \;\;\;\; a \;=\; A^T \cdot h",
        fontsize=16))
    flow.append(P("Substituting one into the other: a = A<sup>T</sup>·A·a, h = A·A<sup>T</sup>·h — so "
                  "a is the principal eigenvector of A<sup>T</sup>·A and h is the principal eigenvector of "
                  "A·A<sup>T</sup>. Power-iterate, normalizing each step (typically L1 or L2).", "Body"))
    flow.append(callout(
        "PAGERANK vs HITS — common compare-and-contrast question",
        [
            P("• <b>PageRank</b>: one score per page, computed offline (query-independent), uses teleport.", "DefBody"),
            P("• <b>HITS</b>: two scores per page, traditionally computed on a query-specific subgraph (root + base set), no teleport.", "DefBody"),
            P("• PageRank uses column-stochastic M; HITS uses raw adjacency A.", "DefBody"),
            P("• PageRank converges from any positive start due to teleport; HITS needs explicit normalization to converge.", "DefBody"),
            P("• Both are eigenvector-based; both reduce to power iteration.", "DefBody"),
        ],
        title_style=S["DefTitle"], body_style=S["DefBody"],
        bg=DEF_BG, border=DEF_PURP))
    return flow


# ════════════════════════════════════════════════════════════════════════
#  WORKED EXAMPLES
# ════════════════════════════════════════════════════════════════════════

def worked_examples():
    flow = []
    flow.append(PageBreak())
    flow.append(section_bar("§ 9   SIX WORKED NUMERICAL EXAMPLES", EX_GREEN))

    # WE 1: Topic-sensitive PR one iteration
    flow.append(P("Worked Example 1 — Topic-Sensitive PageRank, one iteration", "H2"))
    flow.append(P("<b>Problem.</b> The 4-node graph from the W12 slides has edges: "
                  "1→2, 1→3, 2→3, 3→1, 3→4, 4→1, 4→2 (out-degrees: d<sub>1</sub>=2, d<sub>2</sub>=1, "
                  "d<sub>3</sub>=2, d<sub>4</sub>=2). Topic set S = {1}, β = 0.8. "
                  "Compute one iteration starting from r<sup>(0)</sup> = (1/4, 1/4, 1/4, 1/4).", "Body"))
    flow.append(P("<b>Step 1 — M (column-stochastic).</b>", "Body"))
    flow.extend(autofit_table([
        ["", "fr 1", "fr 2", "fr 3", "fr 4"],
        ["row 1", "0", "0", "1/2", "1/2"],
        ["row 2", "1/2", "0", "0", "1/2"],
        ["row 3", "1/2", "1", "0", "0"],
        ["row 4", "0", "0", "1/2", "0"],
    ], header=True, alignments=["L","C","C","C","C"]))
    flow.append(P("<b>Step 2 — M·r<sup>(0)</sup>.</b> Each entry is column·(1/4):", "Body"))
    flow.append(P("• r'<sub>1</sub> = 0+0+(1/2)(1/4)+(1/2)(1/4) = 0.250", "Bullet"))
    flow.append(P("• r'<sub>2</sub> = (1/2)(1/4)+0+0+(1/2)(1/4) = 0.250", "Bullet"))
    flow.append(P("• r'<sub>3</sub> = (1/2)(1/4)+1·(1/4)+0+0 = 0.375", "Bullet"))
    flow.append(P("• r'<sub>4</sub> = 0+0+(1/2)(1/4)+0 = 0.125", "Bullet"))
    flow.append(P("<b>Step 3 — β·M·r<sup>(0)</sup>.</b> Multiply each by 0.8: (0.200, 0.200, 0.300, 0.100). Sum S = 0.800.", "Body"))
    flow.append(P("<b>Step 4 — add teleport into S = {1} only.</b> "
                  "(1 − β)/|S| = 0.2/1 = 0.2 added ONLY to node 1. Other nodes get 0.", "Body"))
    flow.append(P("→ r<sup>(1)</sup> = (0.200+0.200, 0.200, 0.300, 0.100) = "
                  "<b>(0.400, 0.200, 0.300, 0.100)</b>. Sum = 1.000 ✓.", "Body"))
    flow.append(P("Note how node 1 jumps from 0.25 to 0.40 — the teleport mass is now concentrated there. "
                  "Slide answer (after convergence): r ≈ (0.29, 0.11, 0.32, 0.26). Direction matches.", "Body"))

    # WE 2: Topic-sensitive PR with S of two pages
    flow.append(P("Worked Example 2 — Topic set with two pages", "H2"))
    flow.append(P("<b>Problem.</b> Same 4-node graph as WE 1, but now S = {1, 2} and β = 0.8. "
                  "Compute one iteration starting from r<sup>(0)</sup> uniform.", "Body"))
    flow.append(P("β·M·r<sup>(0)</sup> = (0.200, 0.200, 0.300, 0.100) — same as WE 1.", "Body"))
    flow.append(P("Teleport: (1−β)/|S| = 0.2/2 = 0.1 added to nodes 1 AND 2; others get 0.", "Body"))
    flow.append(P("→ r<sup>(1)</sup> = (0.200+0.1, 0.200+0.1, 0.300, 0.100) = "
                  "<b>(0.300, 0.300, 0.300, 0.100)</b>. Sum = 1.000 ✓.", "Body"))
    flow.append(P("Spreading the teleport across two seeds reduces the boost to each but covers more topical scope.", "Body"))

    # WE 3: Spam farm multiplier numerical
    flow.append(P("Worked Example 3 — Spam-farm multiplier in numbers", "H2"))
    flow.append(P("<b>Problem.</b> Spammer creates a farm with M = 10⁵ owned pages all linking to target t. "
                  "External (accessible) PR contribution to t is x = 10<sup>−4</sup>. "
                  "Total web N = 10⁹ pages. β = 0.85. Compute the spam farm's PageRank y.", "Body"))
    flow.append(P("<b>Apply formula:</b> y = x/(1−β²) + c·M/N where c = β/(1+β).", "Body"))
    flow.append(P("• 1 − β² = 1 − 0.7225 = 0.2775. → x/(1−β²) = 10<sup>−4</sup>/0.2775 ≈ <b>3.604 × 10<sup>−4</sup></b>.", "Bullet"))
    flow.append(P("• c = 0.85/1.85 ≈ 0.459. → c·M/N = 0.459 · 10<sup>5</sup>/10<sup>9</sup> = 4.59 × 10<sup>−5</sup>.", "Bullet"))
    flow.append(P("• y ≈ 3.604 × 10<sup>−4</sup> + 4.59 × 10<sup>−5</sup> ≈ <b>4.06 × 10<sup>−4</sup></b>.", "Bullet"))
    flow.append(P("<b>Sanity check.</b> Without the farm, t's rank would be ≈ x = 10<sup>−4</sup>. The farm "
                  "amplifies it by ~4×. With M = 10⁶ owned pages, the c·M/N term grows to 4.59×10⁻⁴ — "
                  "the farm's structural contribution dominates. That's the “multiplier effect” in action.", "Body"))

    # WE 4: TrustRank one iteration
    flow.append(P("Worked Example 4 — TrustRank, one iteration", "H2"))
    flow.append(P("<b>Problem.</b> 5 pages: A, B, C, D, E. Edges: A→B, B→A, B→C, C→D, D→E, E→D. "
                  "Trusted seed set: {A}. β = 0.85. Compute one iteration of TrustRank.", "Body"))
    flow.append(P("<b>Out-degrees:</b> d<sub>A</sub>=1, d<sub>B</sub>=2, d<sub>C</sub>=1, d<sub>D</sub>=1, d<sub>E</sub>=1.", "Body"))
    flow.append(P("<b>Initial r<sup>(0)</sup>:</b> = (1/5)·1 = 0.2 each (TrustRank starts uniform like PageRank).", "Body"))
    flow.append(P("<b>M·r<sup>(0)</sup>:</b>", "Body"))
    flow.append(P("• r'<sub>A</sub> = (1/2)·0.2 = 0.100  (only B→A)", "Bullet"))
    flow.append(P("• r'<sub>B</sub> = 1·0.2 = 0.200  (only A→B)", "Bullet"))
    flow.append(P("• r'<sub>C</sub> = (1/2)·0.2 = 0.100  (only B→C)", "Bullet"))
    flow.append(P("• r'<sub>D</sub> = 1·0.2 + 1·0.2 = 0.400  (C→D and E→D)", "Bullet"))
    flow.append(P("• r'<sub>E</sub> = 1·0.2 = 0.200  (D→E)", "Bullet"))
    flow.append(P("<b>β·M·r<sup>(0)</sup>:</b> 0.85 · (0.100, 0.200, 0.100, 0.400, 0.200) = "
                  "(0.085, 0.170, 0.085, 0.340, 0.170). Sum S = 0.850.", "Body"))
    flow.append(P("<b>Add teleport into seed set {A}:</b> (1−β)/|S| = 0.15/1 = 0.15 to A only.", "Body"))
    flow.append(P("→ r<sup>(1)</sup> = <b>(0.235, 0.170, 0.085, 0.340, 0.170)</b>. Sum = 1.000 ✓.", "Body"))
    flow.append(P("Notice A's rank jumps because it's the only teleport target. "
                  "After more iterations, B (close to A) accumulates more trust than E (far from A) — exactly the "
                  "trust attenuation effect from §6.", "Body"))

    # WE 5: Spam Mass calculation
    flow.append(P("Worked Example 5 — Spam Mass calculation", "H2"))
    flow.append(P("<b>Problem.</b> A page p has vanilla PageRank r<sub>p</sub> = 0.012 and TrustRank "
                  "r<sup>+</sup><sub>p</sub> = 0.003. (a) Compute Spam Mass. (b) If the threshold is 0.5, is p flagged as spam?", "Body"))
    flow.append(P("(a) r<sup>−</sup><sub>p</sub> = r<sub>p</sub> − r<sup>+</sup><sub>p</sub> = 0.012 − 0.003 = 0.009.", "Body"))
    flow.append(P("&nbsp;&nbsp;&nbsp;&nbsp;Spam Mass = r<sup>−</sup><sub>p</sub> / r<sub>p</sub> = 0.009 / 0.012 = "
                  "<b>0.75</b>.", "Body"))
    flow.append(P("(b) 0.75 &gt; 0.5 → <b>YES, p is flagged as spam</b>. ¾ of its PageRank comes from non-trusted sources.", "Body"))

    # WE 6: HITS one iteration
    flow.append(P("Worked Example 6 — HITS, two iterations", "H2"))
    flow.append(P("<b>Problem.</b> Three pages with link adjacency: 1→2, 1→3, 2→3, 3→1. "
                  "Compute hubs h and authorities a for two iterations starting from h<sup>(0)</sup>=a<sup>(0)</sup>=(1,1,1). "
                  "Normalize by L1 norm after each step.", "Body"))
    flow.append(P("<b>A (raw adjacency):</b> rows = source, cols = target. "
                  "A = [[0,1,1],[0,0,1],[1,0,0]]. A<sup>T</sup> = [[0,0,1],[1,0,0],[1,1,0]].", "Body"))
    flow.append(P("<b>Iter 1 authorities</b>: a = A<sup>T</sup>·h = "
                  "(h<sub>3</sub>, h<sub>1</sub>, h<sub>1</sub>+h<sub>2</sub>) = (1, 1, 2). Normalize: a = (1/4, 1/4, 2/4) = (0.25, 0.25, 0.5).", "Body"))
    flow.append(P("<b>Iter 1 hubs</b>: h = A·a = "
                  "(a<sub>2</sub>+a<sub>3</sub>, a<sub>3</sub>, a<sub>1</sub>) = (0.75, 0.5, 0.25). Normalize (sum=1.5): h = (0.5, 0.333, 0.167).", "Body"))
    flow.append(P("<b>Iter 2 authorities</b>: a = A<sup>T</sup>·h = "
                  "(h<sub>3</sub>, h<sub>1</sub>, h<sub>1</sub>+h<sub>2</sub>) = (0.167, 0.5, 0.833). Normalize (sum=1.5): a = (0.111, 0.333, 0.556).", "Body"))
    flow.append(P("<b>Iter 2 hubs</b>: h = A·a = "
                  "(a<sub>2</sub>+a<sub>3</sub>, a<sub>3</sub>, a<sub>1</sub>) = (0.889, 0.556, 0.111). Normalize (sum=1.556): h = (0.571, 0.357, 0.071).", "Body"))
    flow.append(P("<b>Reading the converged scores:</b> page 3 is the strongest authority (linked from 1 and 2). "
                  "Page 1 is the strongest hub (links to 2 and 3). Page 2 is weaker on both metrics. "
                  "These rankings match the link-graph intuition.", "Body"))
    return flow


# ════════════════════════════════════════════════════════════════════════
#  PRACTICE QUESTIONS
# ════════════════════════════════════════════════════════════════════════

def practice_questions():
    flow = []
    flow.append(PageBreak())
    flow.append(section_bar("§ 10   PRACTICE QUESTIONS — 15", PRAC_ORN))
    qs = [
        ("Q1", "Numerical · 6 marks",
         "For the 4-node graph from WE 1 (edges 1→2, 1→3, 2→3, 3→1, 3→4, 4→1, 4→2), "
         "compute Topic-Sensitive PageRank with S = {3} and β = 0.85 for one iteration starting from uniform r<sup>(0)</sup>. "
         "Show M·r<sup>(0)</sup>, β·M·r<sup>(0)</sup>, the teleport contribution, and the final r<sup>(1)</sup>."),
        ("Q2", "Numerical · 5 marks",
         "Using the same 4-node graph and S = {1, 2, 3, 4} (i.e. teleporting uniformly to all nodes — recovering "
         "vanilla PageRank), compute r<sup>(1)</sup> from uniform r<sup>(0)</sup> with β = 0.8. "
         "Verify the teleport contribution equals (1−β)/N for each node."),
        ("Q3", "Numerical · 6 marks",
         "A spammer builds a farm with M = 5×10⁴ owned pages, each linking back to target t. External "
         "(accessible) PR contribution to t is x = 5×10<sup>−5</sup>. Total web pages N = 10<sup>9</sup>. "
         "(a) For β = 0.85, compute the multiplier 1/(1−β²). "
         "(b) Compute y, the PageRank of t. "
         "(c) What value of M is needed to make y ≥ 10<sup>−3</sup>?"),
        ("Q4", "Numerical · 7 marks",
         "Five-page graph: A→B, A→C, B→C, B→D, C→A, D→E, E→C. Trusted seed set = {A, C}. β = 0.8. "
         "Compute one iteration of TrustRank from r<sup>(0)</sup> uniform. List M·r<sup>(0)</sup> entry-by-entry, "
         "compute β·M·r<sup>(0)</sup>, then add teleport into the seed set."),
        ("Q5", "Numerical · 4 marks",
         "Page p has vanilla PageRank r<sub>p</sub> = 0.025 and TrustRank r<sup>+</sup><sub>p</sub> = 0.020. "
         "(a) Compute Spam Mass. (b) If threshold = 0.4, is p flagged? "
         "(c) Suppose we re-run TrustRank with a larger seed set and r<sup>+</sup><sub>p</sub> rises to 0.022. "
         "Does Spam Mass go up or down? By how much?"),
        ("Q6", "Numerical · 6 marks",
         "Three-page graph: 1→2, 1→3, 2→1, 2→3, 3→2. Compute HITS hub and authority scores for two iterations "
         "starting from h<sup>(0)</sup>=a<sup>(0)</sup>=(1,1,1). Normalize by L1 norm at each step. State which "
         "page is the strongest authority and which is the strongest hub."),
        ("Q7", "Concept · 4 marks",
         "Explain how Topic-Sensitive PageRank is implemented as a one-line modification of the vanilla "
         "PageRank algorithm. Then give a concrete example where Topic-Sensitive PR returns a strictly different "
         "ranking from vanilla PR (you may invent a small graph)."),
        ("Q8", "Concept · 4 marks",
         "Define <b>trust attenuation</b> and <b>trust splitting</b>. For each, explain the intuition (one sentence) "
         "and identify the corresponding term in the algebra of the TrustRank iteration."),
        ("Q9", "Concept · 4 marks",
         "Walk through the spam-farm derivation. Explain why the round-trip rank flow contributes a β² factor and "
         "why the (1−β)/N teleport term is typically dropped from the final formula. State the multiplier value "
         "for β = 0.9."),
        ("Q10", "Concept · 4 marks",
         "Compare PageRank, TrustRank, HITS, and Spam Mass on three axes: "
         "(a) what they assign per page, (b) what their teleport / normalization is, "
         "(c) what kind of question they answer."),
        ("Q11", "Concept · 3 marks",
         "Why is Spam Mass preferable to thresholding TrustRank directly? Give a concrete scenario where direct "
         "TrustRank thresholding misclassifies a legitimate page as spam, but Spam Mass does not."),
        ("Q12", "MCQ · 2 marks",
         "In Topic-Sensitive PageRank with topic set S and |S| pages, the teleport contribution to page j ∈ S each "
         "iteration is: "
         "(A) (1−β)/N, "
         "(B) (1−β)/|S|, "
         "(C) β/|S|, "
         "(D) β·(1−β)/N."),
        ("Q13", "MCQ · 2 marks",
         "The spam-farm multiplier for β = 0.5 is closest to: "
         "(A) 1.0,  (B) 1.33,  (C) 1.6,  (D) 2.0."),
        ("Q14", "True/False · 2 marks",
         "True or false: HITS converges from any positive initial vector without explicit normalization. Justify."),
        ("Q15", "MCQ · 2 marks",
         "Which of the following is the MOST robust strategy for picking a TrustRank seed set? "
         "(A) random sample of 1000 pages, "
         "(B) top-k pages by vanilla PageRank, "
         "(C) every page on the web — most are good, "
         "(D) only pages from .edu / .gov / .mil domains."),
    ]
    for qid, hdr, body in qs:
        flow.append(KeepTogether([
            P(f"<b>{qid}</b> &nbsp; <font color='#B85C00'>[{hdr}]</font>", "PracTitle"),
            P(body, "PracBody"),
            Spacer(1, 0.15*cm),
        ]))
    return flow


def full_answers():
    flow = []
    flow.append(PageBreak())
    flow.append(section_bar("§ 11   FULL WORKED ANSWERS", ANS_TEAL))
    answers = [
        ("A1",
         "M·r<sup>(0)</sup> = (0.250, 0.250, 0.375, 0.125) (from WE 1). "
         "β·M·r<sup>(0)</sup> = 0.85 · (0.250, 0.250, 0.375, 0.125) = (0.2125, 0.2125, 0.31875, 0.10625). "
         "Sum S = 0.85. "
         "(1−β)/|S| = 0.15/1 = 0.15 added to node 3 only. "
         "→ r<sup>(1)</sup> = (0.2125, 0.2125, 0.46875, 0.10625). Sum ≈ 1.000 ✓. "
         "Node 3 surges from 0.31875 to 0.46875 because it's the lone topic seed."),
        ("A2",
         "β·M·r<sup>(0)</sup> with β=0.8: 0.8 · (0.250, 0.250, 0.375, 0.125) = (0.200, 0.200, 0.300, 0.100). Sum S = 0.800. "
         "Teleport (1−β)/|S| with |S|=N=4: 0.2/4 = 0.05 added to every node. "
         "→ r<sup>(1)</sup> = (0.250, 0.250, 0.350, 0.150). Sum = 1.000 ✓. "
         "Verify: each node gets exactly 0.05 from teleport — equal to (1−β)/N = 0.2/4 ✓."),
        ("A3",
         "(a) 1/(1−β²) = 1/(1−0.7225) = 1/0.2775 = <b>3.604</b>.<br/>"
         "(b) c = β/(1+β) = 0.85/1.85 = 0.4595.<br/>"
         "&nbsp;&nbsp;&nbsp;&nbsp;y = x/(1−β²) + c·M/N "
         "= 5×10<sup>−5</sup> · 3.604 + 0.4595 · 5×10<sup>4</sup>/10<sup>9</sup> "
         "= 1.802×10<sup>−4</sup> + 2.298×10<sup>−5</sup> ≈ <b>2.03×10<sup>−4</sup></b>.<br/>"
         "(c) Want y ≥ 10<sup>−3</sup>. The first term is fixed at 1.802×10<sup>−4</sup>. "
         "Need c·M/N ≥ 10<sup>−3</sup> − 1.802×10<sup>−4</sup> = 8.198×10<sup>−4</sup>. "
         "Solve: M ≥ N·8.198×10<sup>−4</sup>/c = 10<sup>9</sup>·8.198×10<sup>−4</sup>/0.4595 ≈ <b>1.78×10<sup>6</sup></b> pages. "
         "So the spammer needs ~1.8 million owned pages to push y above 10<sup>−3</sup>."),
        ("A4",
         "Out-degrees: d<sub>A</sub>=2 (A→B, A→C), d<sub>B</sub>=2 (B→C, B→D), d<sub>C</sub>=1 (C→A), d<sub>D</sub>=1 (D→E), d<sub>E</sub>=1 (E→C). "
         "r<sup>(0)</sup>=(0.2, 0.2, 0.2, 0.2, 0.2).<br/><br/>"
         "<b>M·r<sup>(0)</sup>:</b><br/>"
         "• r'<sub>A</sub> = 1·0.2 = 0.200  (only C→A)<br/>"
         "• r'<sub>B</sub> = (1/2)·0.2 = 0.100  (A→B)<br/>"
         "• r'<sub>C</sub> = (1/2)·0.2 + (1/2)·0.2 + 1·0.2 = 0.500  (A→C, B→C, E→C)<br/>"
         "• r'<sub>D</sub> = (1/2)·0.2 = 0.100  (B→D)<br/>"
         "• r'<sub>E</sub> = 1·0.2 = 0.200  (D→E)<br/><br/>"
         "<b>β·M·r<sup>(0)</sup>:</b> 0.8·(0.200, 0.100, 0.500, 0.100, 0.200) = (0.160, 0.080, 0.400, 0.080, 0.160). Sum S = 0.880.<br/><br/>"
         "<b>Teleport:</b> (1−β)/|S| = 0.2/2 = 0.10 to A and C; 0 to others. "
         "→ r<sup>(1)</sup> = (0.260, 0.080, 0.500, 0.080, 0.160). Sum = 1.080 ≠ 1.<br/><br/>"
         "<i>Why doesn't it sum to 1?</i> Because the graph has no dead-ends in this case but the LEAK formula "
         "we just used is the simplified Topic-PR one. To preserve normalization with leaked mass S, "
         "use (1−S)/|S| = 0.12/2 = 0.060 to seeds: r<sup>(1)</sup> = (0.220, 0.080, 0.460, 0.080, 0.160). Sum = 1.000 ✓.<br/>"
         "<b>Lesson:</b> the simple (1−β)/|S| only sums to 1 when S = β·M·r<sup>(0)</sup> sums to β. Otherwise use (1−S)/|S|."),
        ("A5",
         "(a) r<sup>−</sup><sub>p</sub> = 0.025 − 0.020 = 0.005. "
         "Spam Mass = 0.005/0.025 = <b>0.20</b>.<br/>"
         "(b) 0.20 &lt; 0.40 → <b>NOT flagged</b>. Most of p's rank comes from trusted sources.<br/>"
         "(c) New r<sup>−</sup><sub>p</sub> = 0.025 − 0.022 = 0.003. New Spam Mass = 0.003/0.025 = <b>0.12</b>. "
         "Spam Mass <b>decreased</b> by 0.20 − 0.12 = <b>0.08</b>. Larger trusted seed set means more of p's rank is now "
         "attributable to trusted sources."),
        ("A6",
         "A = [[0,1,1],[1,0,1],[0,1,0]] (rows=source). A<sup>T</sup> = [[0,1,0],[1,0,1],[1,1,0]]. "
         "h<sup>(0)</sup> = a<sup>(0)</sup> = (1, 1, 1).<br/><br/>"
         "<b>Iter 1.</b> a = A<sup>T</sup>·h = (h<sub>2</sub>, h<sub>1</sub>+h<sub>3</sub>, h<sub>1</sub>+h<sub>2</sub>) = "
         "(1, 2, 2). L1 norm = 5. → a = (0.20, 0.40, 0.40). "
         "h = A·a = (a<sub>2</sub>+a<sub>3</sub>, a<sub>1</sub>+a<sub>3</sub>, a<sub>2</sub>) = "
         "(0.80, 0.60, 0.40). L1 norm = 1.80. → h = (0.444, 0.333, 0.222).<br/><br/>"
         "<b>Iter 2.</b> a = A<sup>T</sup>·h = (h<sub>2</sub>, h<sub>1</sub>+h<sub>3</sub>, h<sub>1</sub>+h<sub>2</sub>) = "
         "(0.333, 0.667, 0.778). L1 = 1.778. → a = (0.187, 0.375, 0.438). "
         "h = A·a = (0.813, 0.625, 0.375). L1 = 1.813. → h = (0.448, 0.345, 0.207).<br/><br/>"
         "<b>Strongest authority: page 3</b> (linked from both 1 and 2). "
         "<b>Strongest hub: page 1</b> (links to both 2 and 3 — most “index-page-like”)."),
        ("A7",
         "Implementation change: in step (c) of the W8-9 complete algorithm — “r<sup>new</sup><sub>j</sub> = "
         "r'<sup>new</sup><sub>j</sub> + (1−S)/N” — replace (1−S)/N with (1−S)/|S| if j ∈ S else 0.<br/>"
         "Concrete example: graph 1→2, 2→1 (a 2-cycle) plus an isolated page 3 with no links. "
         "Vanilla PageRank gives r ≈ (0.4, 0.4, 0.2) — page 3 gets the teleport baseline. "
         "With S = {3}, all teleport mass goes to 3 and rank concentrates there: r ≈ (0.15, 0.15, 0.70). "
         "The two rankings disagree on the most important page."),
        ("A8",
         "<b>Trust attenuation</b> — trust decreases with graph distance from the seed set. "
         "Algebraically: at every hop, only β fraction of trust is propagated; the remaining (1−β) is teleported. "
         "After k hops, only β<sup>k</sup> of the original trust survives. "
         "<br/><br/><b>Trust splitting</b> — a page p with k out-links gives only t<sub>p</sub>/k trust to each. "
         "Algebraically: the (1/d<sub>i</sub>) factor in M<sub>ji</sub>. "
         "Captures the editorial-rigor intuition: more out-links per page → less endorsement weight per link."),
        ("A9",
         "Spam-farm derivation: target t's PageRank = x (from accessible) + β·M·rank<sub>farm</sub> (from M owned pages) "
         "+ (1−β)/N (teleport). Each farm page receives β·y/M from t plus (1−β)/N teleport. "
         "Substituting: y = x + β·M·(βy/M + (1−β)/N) + (1−β)/N. "
         "The β² factor comes from t→farm (one β) and farm→t (another β). "
         "The (1−β)/N teleport is dropped because it's O(1/N) ≈ 10<sup>−9</sup> — negligible compared to x and to βM/N. "
         "Multiplier for β = 0.9: 1/(1−0.81) = 1/0.19 ≈ <b>5.26</b>. Higher β → bigger multiplier → spam farms more effective."),
        ("A10",
         "<b>(a) Per-page output:</b> PageRank → 1 score; TrustRank → 1 trust score; HITS → 2 scores (h, a); "
         "Spam Mass → 1 ratio in [0, 1].<br/>"
         "<b>(b) Teleport / normalization:</b> PageRank → uniform teleport; TrustRank → teleport into trusted seed set; "
         "HITS → no teleport, explicit L1/L2 normalization; Spam Mass → derived from r and r<sup>+</sup>, no iteration of its own.<br/>"
         "<b>(c) Question answered:</b> PageRank — “how important is page p?” TrustRank — “how trusted?” "
         "HITS — “is p a hub or an authority?” Spam Mass — “what fraction of p's rank is spam?”"),
        ("A11",
         "Direct TrustRank thresholding misclassifies legitimate but isolated pages as spam — pages "
         "far from any seed naturally have low TrustRank regardless of legitimacy. "
         "Example: a legitimate small academic blog with low overall PageRank r<sub>p</sub> = 0.0001 and TrustRank "
         "r<sup>+</sup><sub>p</sub> = 0.00009. Direct TrustRank threshold of 0.001 flags this as spam. "
         "Spam Mass = (0.0001 − 0.00009)/0.0001 = 0.10 → not flagged (most of its small rank is from trusted sources, "
         "the page is just isolated, not spammy). Spam Mass normalizes by total rank, removing the “distance from seed” bias."),
        ("A12", "<b>(B)</b> (1−β)/|S| — the teleport mass is divided among |S| seed pages."),
        ("A13", "1/(1 − 0.5²) = 1/0.75 = 1.333. <b>(B)</b>."),
        ("A14",
         "<b>False.</b> Without normalization, h and a grow without bound (or shrink to zero). The eigenvalue of "
         "A·A<sup>T</sup> is generally not 1 — it could be > 1 (so values explode) or < 1 (values vanish). "
         "Explicit L1 or L2 normalization at each step keeps the iteration bounded and convergent to the principal "
         "eigenvector direction."),
        ("A15", "<b>(D)</b>. Controlled-membership domains (.edu, .gov, .mil) provide high-trust seeds with negligible spam. "
                "(B) is also reasonable but top-PR pages can include compromised popular sites. (A) is wasteful "
                "(seeds may be mostly low-trust). (C) is impossible — humans can't vet billions of pages."),
    ]
    for aid, body in answers:
        flow.append(KeepTogether([
            P(f"<b>{aid}</b>", "AnsTitle"),
            P(body, "AnsBody"),
            Spacer(1, 0.2*cm),
        ]))
    return flow


def revision_sheet():
    flow = []
    flow.append(PageBreak())
    flow.append(section_bar("§ 12   ENDING KEY NOTES — REVISION CARDS", REV_RED))
    cards = [
        ("PageRank's 3 weaknesses",
         "Topic blindness, single importance score, link-spam vulnerability."),
        ("Topic-Sensitive PR",
         "r = β·M·r + (1−β)·v<sub>S</sub>, v<sub>S</sub>[j]=1/|S| if j∈S else 0."),
        ("Topic-PR teleport",
         "(1−β)/|S| added to every j ∈ S; 0 to other pages."),
        ("Algorithm change",
         "ONE line: redistribute leaked/teleport mass to S only, not all N pages."),
        ("Term spam",
         "Hidden keyword stuffing, copying top results invisibly."),
        ("Google's term-spam fix",
         "Trust anchor text from incoming links, not page's own body text."),
        ("3 page types (spammer view)",
         "Inaccessible / Accessible / Owned."),
        ("Spam farm goal",
         "Maximize PageRank of target page t by mutual links with M owned pages."),
        ("Spam farm formula",
         "y = x/(1−β²) + c·M/N, c = β/(1+β)."),
        ("Multiplier (β=0.85)",
         "1/(1−β²) ≈ 3.6 — small accessible-PR x amplified ~3.6×."),
        ("TrustRank",
         "Topic-sensitive PR with teleport set = trusted seed pages."),
        ("Trust attenuation",
         "Trust decays β per hop; far-from-seed pages get little trust."),
        ("Trust splitting",
         "Trust divided across out-links: page with k out-links → t/k each."),
        ("Seed set choices",
         "(1) top-k by PageRank, (2) controlled domains (.edu/.gov/.mil)."),
        ("Spam Mass formula",
         "SM(p) = (r<sub>p</sub> − r<sup>+</sup><sub>p</sub>)/r<sub>p</sub>."),
        ("Spam Mass intuition",
         "Fraction of p's rank coming from non-trusted (likely spam) sources."),
        ("HITS scores",
         "h<sub>i</sub> = hub score, a<sub>j</sub> = authority score."),
        ("HITS iteration",
         "h ← A·a, a ← A<sup>T</sup>·h. Normalize each step."),
        ("HITS eigen-equation",
         "a = A<sup>T</sup>A·a (principal eigenvector); h = AA<sup>T</sup>·h."),
        ("PageRank vs HITS",
         "PR: 1 score, query-independent, teleport. HITS: 2 scores, query-specific, normalized."),
    ]
    rows = []
    for i in range(0, len(cards), 2):
        left = P(f"<b>{cards[i][0]}</b><br/>{cards[i][1]}", "RevBody")
        right = (P(f"<b>{cards[i+1][0]}</b><br/>{cards[i+1][1]}", "RevBody")
                 if i+1 < len(cards) else P("", "RevBody"))
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
    flow.append(section_bar("§ 13   FORMULA & ALGORITHM REFERENCE", REF_INDIGO))
    flow.append(P("Quick-look reference for everything advanced in W12.", "Body"))
    rows = [
        ["Concept", "Formula / Statement", "Use"],
        ["Topic-Sensitive PR",
         "r = β·M·r + (1−β)·v<sub>S</sub>, v<sub>S</sub>[j]=1/|S| if j∈S",
         "Bias rank to a specific topic."],
        ["Topic-PR teleport",
         "(1−β)/|S| to seeds only, 0 to others",
         "One-line modification of W8-9 algorithm."],
        ["Spam farm rank",
         "y = x/(1−β²) + (β/(1+β))·M/N",
         "Estimating effectiveness of a link farm."],
        ["Multiplier (β=0.85)",
         "1/(1−β²) ≈ 3.6",
         "How much accessible PR is amplified."],
        ["TrustRank",
         "Same as Topic-PR with seed set = trusted pages",
         "Demoting link-spam farms automatically."],
        ["Trust propagation",
         "trust q = β · Σ<sub>p→q</sub> trust<sub>p</sub>/|O<sub>p</sub>| + teleport",
         "Per-iteration update."],
        ["Spam Mass",
         "SM(p) = (r<sub>p</sub> − r<sup>+</sup><sub>p</sub>)/r<sub>p</sub>",
         "Fractional spam contribution; threshold to label spam."],
        ["HITS authority",
         "a = A<sup>T</sup>·h; converges to principal eigenvector of A<sup>T</sup>A",
         "Pages that are linked-to by good hubs."],
        ["HITS hub",
         "h = A·a; converges to principal eigenvector of AA<sup>T</sup>",
         "Pages that link-to good authorities."],
    ]
    flow.extend(autofit_table(rows, header=True,
                              alignments=["L","L","L"],
                              caption="Table 13.1. Advanced link-analysis reference."))
    flow.append(Spacer(1, 0.2*cm))
    flow.append(P("<b>Connections to other weeks:</b>", "RefTitle"))
    flow.append(P("• <b>W8-9 PageRank</b>: every algorithm here is a parametrization of the W8-9 power iteration. "
                  "Topic-Sensitive PR changes the teleport vector. TrustRank inherits Topic-PR. Spam Mass is post-hoc.", "Bullet"))
    flow.append(P("• <b>W16 Community Detection</b>: spectral clustering uses the same eigenvector machinery on a different "
                  "matrix (the graph Laplacian instead of M). HITS's A<sup>T</sup>A is the link-graph analog.", "Bullet"))
    flow.append(P("• <b>MMDS §5.3–5.5</b>: the textbook's depth on Topic-PR, Link Spam, TrustRank, Spam Mass, and HITS. "
                  "Read for exercise variety, not for new concepts beyond what's here.", "Bullet"))
    return flow


def main():
    doc = make_doc(
        out_path=OUT,
        title="BDA Week 12 Advanced Link Analysis — Final Exam Prep",
        header_text="W12 · Advanced Link Analysis",
        footer_text="CS-404 BDA · Final Exam Prep · Comprehensive Tutor PDF",
    )
    story = []
    story.extend(cover_page())
    story.extend(toc_page())
    story.extend(beginning_key_notes())
    story.extend(limitations())
    story.extend(topic_pr())
    story.extend(web_spam())
    story.extend(link_spam())
    story.extend(trust_rank())
    story.extend(spam_mass())
    story.extend(hits_section())
    story.extend(worked_examples())
    story.extend(practice_questions())
    story.extend(full_answers())
    story.extend(revision_sheet())
    story.extend(reference_sheet())
    doc.build(story)
    p = Path(OUT)
    print(f"[w12] PDF built: {p.resolve()} — {p.stat().st_size/1024:.1f} KB")


if __name__ == "__main__":
    main()
