---
title: "BDA Week 12 — Advanced Link Analysis"
subtitle: "Topic-Sensitive PageRank · Web Spam · TrustRank · Spam Mass · HITS"
author: "BDA Final Exam Prep · Comprehensive Tutor"
course: "CS-404 Big Data Analytics — Dr. Syed Imran Ali"
exam: "Final ~ 2026-05-16"
---

# Week 12 · Advanced Link Analysis

> Builds directly on W8-9 PageRank. Make sure you can recite $r = \beta M r + (1-\beta)/N \cdot \mathbf{1}_N$ from memory before starting this document.

---

## §1 — Beginning Key Notes (Study Compass)

The 9 ideas you must walk into the exam owning:

1. **Three weaknesses of vanilla PageRank.** (1) generic popularity misses topic-specific authorities; (2) single notion of importance — HITS provides hubs vs. authorities; (3) gameable through link spam — TrustRank fixes this.
2. **Topic-Sensitive PageRank.** Change the teleport target. Instead of jumping uniformly to ANY page, jump uniformly to a small *topic set* $S$. One PageRank vector per topic.
3. **Topic-PR formula.** $A_{ij} = \beta M_{ij} + (1-\beta)/|S|$ if $j \in S$, else $\beta M_{ij}$. Equivalently: $r = \beta M r + (1-\beta) v_S$, where $v_S$ has $1/|S|$ in positions $S$ and 0 elsewhere.
4. **Term spam.** Stuffing pages with hidden keywords. Google's defense: trust anchor-text from incoming links, not page's own words.
5. **Link spam & spam farms.** Three page types — *inaccessible* / *accessible* / *owned*. Spammer creates $M$ owned pages all linking to target $t$ and sneaks a tiny external boost $x$ from accessible pages.
6. **Spam farm formula.** $y = x/(1-\beta^2) + c \cdot M/N$, where $c = \beta/(1+\beta)$. For $\beta = 0.85$, the multiplier $1/(1-\beta^2) \approx 3.6$.
7. **TrustRank.** Topic-sensitive PageRank with the teleport set = trusted human-vetted seed pages (typically `.edu`, `.gov`, `.mil` domains).
8. **Spam Mass.** $\mathrm{SM}(p) = (r_p - r^+_p)/r_p$ where $r^+_p$ is TrustRank. Pages with mass close to 1 are spam.
9. **HITS.** Two scores — $h_i$ (hub) and $a_j$ (authority). Iterate $h \leftarrow A a$ and $a \leftarrow A^T h$ with normalization. Different from PageRank; both are exam-bait concepts.

---

## §2 — Three Limitations of Generic PageRank

Vanilla PageRank gives a single rank per page reflecting overall web-graph importance. This works well for queries like "Stanford" but fails for three reasons:

**(1) No topic awareness.** A query for "Trojan" maps to three different topics — sports (USC Trojans), history (Trojan war), or computer security (Trojan malware). Generic PageRank cannot prefer the right interpretation given the user's actual interest.

**(2) Single notion of importance.** Some pages are *good answer pages* (authoritative content), and some are *good index pages* (useful pointers). PageRank conflates these. The HITS algorithm splits importance into two scores: **hubs** (pages that point to many authorities) and **authorities** (pages pointed to by many hubs).

**(3) Spam vulnerability.** The algorithm is purely structural — it cannot tell whether an incoming link is genuine or spam-farmed. The fix is TrustRank.

---

## §3 — Topic-Sensitive PageRank

**Idea.** Recall the random surfer with teleport probability $1-\beta$. Vanilla PageRank teleports to a uniformly random page (every page equally likely). **Topic-sensitive PageRank** instead teleports to a uniformly random page from a *topic-relevant set* $S$ — pages known to be about a particular topic, for example all DMOZ-classified "sports" pages.

### Matrix formulation

Define the topic-sensitive Google matrix:

$$ A_{ij} = \beta M_{ij} + \frac{1-\beta}{|S|} \;\;\text{if } j \in S, \quad A_{ij} = \beta M_{ij} \;\;\text{otherwise} $$

Equivalently — and this is the form most often used on exams:

$$ r = \beta M r + (1 - \beta) \cdot v_S $$

where $v_S$ is a vector with $1/|S|$ in positions corresponding to pages in $S$, and 0 elsewhere. Plugging $|S| = N$ and $v_S = (1/N) \mathbf{1}_N$ recovers vanilla PageRank — Topic-PR is a strict generalization.

**One vector per topic.** Compute and store $r_{S_1}, r_{S_2}, \ldots$ for the 16 DMOZ top-level categories (arts, business, sports, …). At query time, pick the right vector based on inferred topic.

> **Algorithm change — only one line.** The complete algorithm from W8-9 changes by exactly one line: replace the *uniform redistribution* step with: $r^{new}_j = r'^{new}_j + (1-S)/|S|$ if $j \in S$, else $r'^{new}_j$. Everything else stays identical.

### Slide example (4-node graph)

The slides show a 4-node graph with edges $1 \to 2$, $1 \to 3$, $2 \to 3$, $3 \to 1$, $3 \to 4$, $4 \to 1$, $4 \to 2$. Out-degrees: $d_1 = 2$, $d_2 = 1$, $d_3 = 2$, $d_4 = 2$. Selected slide answers:
- $S = \{1\}$, $\beta = 0.8$: converged $r \approx (0.29, 0.11, 0.32, 0.26)$
- $S = \{1, 2, 3, 4\}$, $\beta = 0.8$: $r \approx (0.13, 0.10, 0.39, 0.36)$ — equivalent to vanilla PageRank
- $S = \{1\}$, $\beta = 0.7$: $r \approx (0.39, 0.14, 0.27, 0.19)$ — lower $\beta$ concentrates more rank in the seed.

---

## §4 — Web Spam: Term Spam & Google's Defense

**Spamming** is any deliberate action to boost a page's search-engine ranking beyond its real value. **Spam** is the resulting page. Approximately 10–15% of web pages are spam.

### First-generation spam (term spam)

Early search engines ranked by word-frequency on the page. Spammers exploited this in two ways:

- **Keyword stuffing.** Add the target keyword (e.g. "movie") thousands of times, with text color matching the background so users don't see it but the crawler does.
- **Top-result mimicry.** Run the query "movie" yourself, see which page comes first, copy its content invisibly into your own page.

### Google's term-spam fix

Believe what others say about you, not what you say about yourself. Specifically, weight the **anchor text** of incoming links — the visible text inside `<a>` tags pointing TO your page — much more than your page's own body text. Combined with PageRank, this surfaced authentic, well-cited pages while burying term-spam farms.

> **Why anchor-text works.** If 1000 pages link to a movie review with anchor text "great movie", that's 1000 independent judgments. The reviewed page can't game this without compromising the linking pages — which themselves have to convince their own users to keep visiting. Distributed truth-telling.

---

## §5 — Link Spam & Spam Farms

Once Google adopted PageRank + anchor text as the ranking signal, spammers shifted to **link spam**: artificially constructing link structures to boost the PageRank of a target page $t$.

### Three page types from the spammer's view

- **Inaccessible** pages — controlled by others, no influence possible.
- **Accessible** pages — e.g. blog comment sections where the spammer can post a link.
- **Owned** pages — completely under the spammer's control, possibly across many domains.

### Spam-farm analysis

Let:
- $x$ = total PageRank contributed to $t$ by accessible pages (small, but nonzero).
- $y$ = PageRank of target $t$ (what we want to estimate).
- $M$ = number of farm pages owned by spammer.
- $N$ = total pages on the web.

Each farm page receives $\beta y / M$ from $t$ (which splits its rank among $M$ owned out-links) plus the teleport $(1-\beta)/N$. So:

$$ \mathrm{rank}_{\mathrm{farm}} = \beta \cdot \frac{y}{M} + \frac{1-\beta}{N} $$

Then $t$'s rank is $x$ (from accessible) + $\beta M \cdot \mathrm{rank}_{\mathrm{farm}}$ (from $M$ farm pages) + $(1-\beta)/N$ (teleport):

$$ y = x + \beta M \cdot \left( \frac{\beta y}{M} + \frac{1-\beta}{N} \right) = x + \beta^2 y + \beta(1-\beta) \frac{M}{N} $$

Solving for $y$ (and dropping the $(1-\beta)/N$ as negligible):

$$ y = \frac{x}{1 - \beta^2} + c \cdot \frac{M}{N}, \qquad c = \frac{\beta}{1+\beta} $$

**Multiplier.** For $\beta = 0.85$, $1/(1-\beta^2) \approx 3.6$. Even a small accessible-PR contribution $x = 0.01$ becomes $y \approx 0.036 + c \cdot M/N$. By making $M$ huge, the spammer can push $y$ arbitrarily high — that is the spam farm's "multiplier effect".

> **EXAM TRAP.** The denominator is $1 - \beta^2$, not $1 - \beta$. The $\beta^2$ comes from the round-trip rank flow: $t \to \mathrm{farm} \to t$.

---

## §6 — TrustRank: Combating Link Spam

**Core insight (approximate isolation).** Trustworthy pages tend not to link to spam pages. If we can identify a small set of **trusted seed pages** by hand, we can propagate their trust outward through the link graph — pages reachable from trusted seeds in few hops are likely good; pages far from any trusted seed are likely spam.

### Algorithm

TrustRank is exactly Topic-Sensitive PageRank with the topic set $S$ = trusted seed pages. Each page receives a trust value $t_p \in [0, 1]$.

- Set $t_p = 1$ for every trusted seed page, 0 elsewhere initially.
- Iterate: each page $p$ with out-link set $O_p$ contributes $\beta t_p / |O_p|$ to each $q \in O_p$.
- Sum incoming contributions per page; converge as in PageRank.

### Two effects you should be able to articulate on the exam

- **Trust attenuation** — trust decreases with graph distance from seeds, because at every hop only a $\beta$ fraction is propagated and the rest leaks into teleport.
- **Trust splitting** — a page with many out-links splits its trust thinly across them. Captures the intuition that an editor with 1000 links per page reviews each less carefully.

### Picking the seed set

Two competing goals — small enough that humans can vet every page, yet broad enough that every legitimate web region is reachable in few hops. Two practical tactics:
- Take the top-$k$ pages by vanilla PageRank (theory: spam can't reach the very top).
- Restrict to controlled-membership domains: `.edu`, `.gov`, `.mil`.

---

## §7 — Spam Mass: Estimating Fractional Spam Contribution

**Complementary view.** TrustRank tells us how much of a page's rank comes from *trusted* sources. Spam Mass asks the converse: how much of a page's rank comes from *spam*?

Let:
- $r_p$ = vanilla PageRank of page $p$.
- $r^+_p$ = TrustRank of $p$ (= topic-sensitive PR with teleport into trusted seed set).
- $r^-_p = r_p - r^+_p$ = rank contributed by non-trusted (likely-spam) sources.

**Spam Mass** of page $p$:

$$ \mathrm{SpamMass}(p) = \frac{r^-_p}{r_p} = \frac{r_p - r^+_p}{r_p} $$

Spam Mass close to 1 means almost all of $p$'s rank comes from non-trusted sources → $p$ is likely spam. Spam Mass close to 0 means most of $p$'s rank comes from trusted sources → $p$ is legitimate. Pick a threshold (e.g. 0.5) and label everything above it as spam.

> **Why use both r and r⁺?** If we only had TrustRank, we'd label every page far from the seed set as spam — including perfectly legitimate isolated communities. Spam Mass instead asks: *relative to its overall rank, how much of this page's rank is attributable to spam-like sources?* Removes the "distance from seed" bias.

---

## §8 — HITS: Hubs & Authorities (Brief)

HITS (Hyperlink-Induced Topic Search) is the second classical link-analysis algorithm. The slides only mention HITS in passing as "Solution: Hubs-and-Authorities" — but the concept is fair game on conceptual exam questions because it's in MMDS §5.5.

### Two scores per page

- **Hub score $h_i$** — high if $i$ links TO many high-authority pages.
- **Authority score $a_j$** — high if $j$ is linked FROM many high-hub pages.

### Iteration

Let $A$ be the link adjacency matrix ($A_{ij} = 1$ if $i \to j$). Then:

$$ h = A \cdot a, \qquad a = A^T \cdot h $$

Substituting one into the other: $a = A^T A \cdot a$, $h = A A^T \cdot h$ — so $a$ is the principal eigenvector of $A^T A$ and $h$ is the principal eigenvector of $A A^T$. Power-iterate, normalizing each step (typically L1 or L2).

### PageRank vs HITS — common compare-and-contrast question

- **PageRank**: one score per page, computed offline (query-independent), uses teleport.
- **HITS**: two scores per page, traditionally computed on a query-specific subgraph (root + base set), no teleport.
- PageRank uses column-stochastic $M$; HITS uses raw adjacency $A$.
- PageRank converges from any positive start due to teleport; HITS needs explicit normalization.
- Both are eigenvector-based; both reduce to power iteration.

---

## §9 — Six Worked Numerical Examples

### Worked Example 1 — Topic-Sensitive PageRank, one iteration

**Problem.** 4-node graph (edges $1 \to 2$, $1 \to 3$, $2 \to 3$, $3 \to 1$, $3 \to 4$, $4 \to 1$, $4 \to 2$). $S = \{1\}$, $\beta = 0.8$. Compute one iteration from uniform $r^{(0)} = (1/4)\mathbf{1}$.

**M (column-stochastic):**

|       | fr 1 | fr 2 | fr 3 | fr 4 |
|-------|------|------|------|------|
| row 1 | 0    | 0    | 1/2  | 1/2  |
| row 2 | 1/2  | 0    | 0    | 1/2  |
| row 3 | 1/2  | 1    | 0    | 0    |
| row 4 | 0    | 0    | 1/2  | 0    |

**$M r^{(0)}$:**
- $r'_1 = 0 + 0 + (1/2)(1/4) + (1/2)(1/4) = 0.250$
- $r'_2 = (1/2)(1/4) + 0 + 0 + (1/2)(1/4) = 0.250$
- $r'_3 = (1/2)(1/4) + 1 \cdot (1/4) + 0 + 0 = 0.375$
- $r'_4 = 0 + 0 + (1/2)(1/4) + 0 = 0.125$

**$\beta M r^{(0)}$:** $0.8 \cdot (\ldots) = (0.200, 0.200, 0.300, 0.100)$. Sum $S = 0.800$.

**Add teleport into $S = \{1\}$:** $(1-\beta)/|S| = 0.2/1 = 0.2$ added to node 1 only.

$r^{(1)} = (0.400, 0.200, 0.300, 0.100)$. Sum $= 1.000$ ✓.

Node 1 jumps from 0.25 to 0.40 — teleport mass concentrated there.

### Worked Example 2 — Topic set with two pages

**Problem.** Same 4-node graph, $S = \{1, 2\}$, $\beta = 0.8$.

$\beta M r^{(0)} = (0.200, 0.200, 0.300, 0.100)$ (same as WE 1).

Teleport: $(1-\beta)/|S| = 0.1$ to nodes 1 AND 2.

$r^{(1)} = (0.300, 0.300, 0.300, 0.100)$. Sum $= 1.000$ ✓.

### Worked Example 3 — Spam-farm multiplier in numbers

**Problem.** Spammer creates $M = 10^5$ owned pages, all linking back to target $t$. External PR contribution $x = 10^{-4}$. $N = 10^9$. $\beta = 0.85$.

$1 - \beta^2 = 0.2775$. So $x/(1-\beta^2) = 10^{-4}/0.2775 \approx 3.604 \times 10^{-4}$.

$c = 0.85/1.85 \approx 0.459$. $c \cdot M/N = 0.459 \cdot 10^5/10^9 = 4.59 \times 10^{-5}$.

$y \approx 3.604 \times 10^{-4} + 4.59 \times 10^{-5} \approx 4.06 \times 10^{-4}$.

**Sanity check.** Without the farm, $t$'s rank would be $\approx x = 10^{-4}$. The farm amplifies it by $\sim 4 \times$. With $M = 10^6$, $c \cdot M/N$ grows to $4.59 \times 10^{-4}$ — farm structure dominates.

### Worked Example 4 — TrustRank, one iteration

**Problem.** 5 pages: $A, B, C, D, E$. Edges: $A \to B$, $B \to A$, $B \to C$, $C \to D$, $D \to E$, $E \to D$. Trusted seed set $\{A\}$. $\beta = 0.85$.

Out-degrees: $d_A = 1$, $d_B = 2$, $d_C = 1$, $d_D = 1$, $d_E = 1$. $r^{(0)} = (0.2)\mathbf{1}$.

**$M r^{(0)}$:**
- $r'_A = (1/2)(0.2) = 0.100$  (only $B \to A$)
- $r'_B = 1 \cdot 0.2 = 0.200$
- $r'_C = (1/2)(0.2) = 0.100$
- $r'_D = 1 \cdot 0.2 + 1 \cdot 0.2 = 0.400$ ($C \to D$ and $E \to D$)
- $r'_E = 1 \cdot 0.2 = 0.200$

**$\beta M r^{(0)}$:** $0.85 \cdot (\ldots) = (0.085, 0.170, 0.085, 0.340, 0.170)$. $S = 0.850$.

**Teleport into $\{A\}$:** $(1-\beta)/|S| = 0.15/1 = 0.15$ to A only.

$r^{(1)} = (0.235, 0.170, 0.085, 0.340, 0.170)$. Sum $= 1.000$ ✓.

A's rank jumps because it's the only teleport target.

### Worked Example 5 — Spam Mass calculation

**Problem.** $r_p = 0.012$, $r^+_p = 0.003$. (a) Compute Spam Mass. (b) Threshold 0.5: spam?

(a) $r^-_p = 0.012 - 0.003 = 0.009$. SpamMass $= 0.009/0.012 = 0.75$.

(b) $0.75 > 0.5$ → **YES, flagged as spam**. ¾ of its rank is from non-trusted sources.

### Worked Example 6 — HITS, two iterations

**Problem.** 3 pages with adjacency: $1 \to 2$, $1 \to 3$, $2 \to 3$, $3 \to 1$. Compute $h, a$ for two iterations from $h^{(0)} = a^{(0)} = (1, 1, 1)$. Normalize by L1 each step.

$A = \begin{pmatrix} 0 & 1 & 1 \\ 0 & 0 & 1 \\ 1 & 0 & 0 \end{pmatrix}$ (rows = source). $A^T = \begin{pmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 1 & 1 & 0 \end{pmatrix}$.

**Iter 1.** $a = A^T h = (h_3, h_1, h_1 + h_2) = (1, 1, 2)$. L1 = 4. $a = (0.25, 0.25, 0.50)$.

$h = A a = (a_2 + a_3, a_3, a_1) = (0.75, 0.50, 0.25)$. L1 = 1.5. $h = (0.500, 0.333, 0.167)$.

**Iter 2.** $a = A^T h = (h_3, h_1, h_1+h_2) = (0.167, 0.500, 0.833)$. L1 = 1.5. $a = (0.111, 0.333, 0.556)$.

$h = A a = (0.889, 0.556, 0.111)$. L1 = 1.556. $h = (0.571, 0.357, 0.071)$.

**Strongest authority: page 3** (linked from 1 and 2). **Strongest hub: page 1** (links to 2 and 3).

---

## §10 — Practice Questions (15)

**Q1 [Numerical · 6 marks].** 4-node graph from WE 1. Compute Topic-PR with $S = \{3\}$, $\beta = 0.85$, one iteration from uniform.

**Q2 [Numerical · 5 marks].** Same 4-node graph, $S = \{1, 2, 3, 4\}$ (vanilla equivalent), $\beta = 0.8$. Compute one iteration. Verify the teleport contribution equals $(1-\beta)/N$ per node.

**Q3 [Numerical · 6 marks].** Spammer creates $M = 5 \times 10^4$ pages, $x = 5 \times 10^{-5}$, $N = 10^9$, $\beta = 0.85$. (a) Compute multiplier. (b) Compute $y$. (c) What $M$ to make $y \geq 10^{-3}$?

**Q4 [Numerical · 7 marks].** Five-page graph: $A \to B$, $A \to C$, $B \to C$, $B \to D$, $C \to A$, $D \to E$, $E \to C$. Trusted seeds $\{A, C\}$, $\beta = 0.8$. One iteration of TrustRank from uniform.

**Q5 [Numerical · 4 marks].** $r_p = 0.025$, $r^+_p = 0.020$. (a) SpamMass. (b) Threshold 0.4: flagged? (c) New $r^+_p = 0.022$ — SpamMass change?

**Q6 [Numerical · 6 marks].** 3-page graph: $1 \to 2$, $1 \to 3$, $2 \to 1$, $2 \to 3$, $3 \to 2$. HITS for two iterations, L1-normalize each step. Strongest authority? Strongest hub?

**Q7 [Concept · 4 marks].** Topic-PR is a one-line modification of vanilla PR. Give an example where they return strictly different rankings.

**Q8 [Concept · 4 marks].** Define trust attenuation and trust splitting. Identify each in the algebra of TrustRank.

**Q9 [Concept · 4 marks].** Walk through the spam-farm derivation. Why $\beta^2$? Why drop $(1-\beta)/N$? Multiplier for $\beta = 0.9$?

**Q10 [Concept · 4 marks].** Compare PageRank, TrustRank, HITS, Spam Mass on (a) per-page output, (b) teleport/normalization, (c) question answered.

**Q11 [Concept · 3 marks].** Why is Spam Mass preferable to thresholding TrustRank directly? Concrete misclassification scenario.

**Q12 [MCQ · 2 marks].** Topic-PR teleport contribution to $j \in S$ each iteration:
(A) $(1-\beta)/N$  (B) $(1-\beta)/|S|$  (C) $\beta/|S|$  (D) $\beta(1-\beta)/N$

**Q13 [MCQ · 2 marks].** Spam-farm multiplier for $\beta = 0.5$:
(A) 1.0  (B) 1.33  (C) 1.6  (D) 2.0

**Q14 [True/False · 2 marks].** HITS converges from any positive initial vector without normalization. Justify.

**Q15 [MCQ · 2 marks].** Most robust TrustRank seed set strategy:
(A) random sample of 1000  (B) top-k by PageRank  (C) every page on the web  (D) `.edu` / `.gov` / `.mil` only

---

## §11 — Full Worked Answers

**A1.** $M r^{(0)} = (0.250, 0.250, 0.375, 0.125)$. $\beta M r = 0.85 \cdot (\ldots) = (0.2125, 0.2125, 0.31875, 0.10625)$. $(1-\beta)/|S| = 0.15$ to node 3. $r^{(1)} = (0.2125, 0.2125, 0.46875, 0.10625)$.

**A2.** $\beta M r = (0.200, 0.200, 0.300, 0.100)$. Teleport $0.2/4 = 0.05$ to every node. $r^{(1)} = (0.250, 0.250, 0.350, 0.150)$. ✓ each node gets exactly $(1-\beta)/N$.

**A3.** (a) $1/(1-0.7225) = 3.604$. (b) $c = 0.4595$. $y = 5 \times 10^{-5} \cdot 3.604 + 0.4595 \cdot 5 \times 10^4/10^9 = 1.802 \times 10^{-4} + 2.298 \times 10^{-5} \approx 2.03 \times 10^{-4}$. (c) Need $M \geq 10^9 \cdot (10^{-3} - 1.802 \times 10^{-4})/0.4595 \approx 1.78 \times 10^6$ pages.

**A4.** Out-degrees: $d_A = 2, d_B = 2, d_C = 1, d_D = 1, d_E = 1$.
- $r'_A = 1 \cdot 0.2 = 0.200$ (C→A)
- $r'_B = (1/2)(0.2) = 0.100$ (A→B)
- $r'_C = (1/2)(0.2) + (1/2)(0.2) + 1 \cdot 0.2 = 0.500$ (A,B,E→C)
- $r'_D = (1/2)(0.2) = 0.100$ (B→D)
- $r'_E = 1 \cdot 0.2 = 0.200$ (D→E)

$\beta M r = (0.160, 0.080, 0.400, 0.080, 0.160)$. $S = 0.880$. To preserve $\sum = 1$: use $(1-S)/|S| = 0.06$ on A and C. $r^{(1)} = (0.220, 0.080, 0.460, 0.080, 0.160)$.

**A5.** (a) $r^-_p = 0.005$. SpamMass $= 0.005/0.025 = 0.20$. (b) $0.20 < 0.40$ → NOT flagged. (c) New $r^-_p = 0.003$. New SpamMass $= 0.12$. Decreased by 0.08.

**A6.** $A = \begin{pmatrix} 0 & 1 & 1 \\ 1 & 0 & 1 \\ 0 & 1 & 0 \end{pmatrix}$. $A^T = \begin{pmatrix} 0 & 1 & 0 \\ 1 & 0 & 1 \\ 1 & 1 & 0 \end{pmatrix}$. $h^{(0)} = a^{(0)} = (1, 1, 1)$.

Iter 1: $a = A^T h = (1, 2, 2)$. L1 = 5. $a = (0.20, 0.40, 0.40)$. $h = A a = (0.80, 0.60, 0.40)$. L1 = 1.80. $h = (0.444, 0.333, 0.222)$.

Iter 2: $a = A^T h = (0.333, 0.667, 0.778)$. L1 = 1.778. $a = (0.187, 0.375, 0.438)$. $h = (0.813, 0.625, 0.375)$. L1 = 1.813. $h = (0.448, 0.345, 0.207)$.

**Strongest authority: page 3. Strongest hub: page 1.**

**A7.** Modify ONE line of the W8-9 algorithm: redistribute leaked mass to $S$ only. Example: 2-cycle $1 \to 2$, $2 \to 1$ + isolated page 3. Vanilla PR: $r \approx (0.4, 0.4, 0.2)$. With $S = \{3\}$: $r \approx (0.15, 0.15, 0.70)$. Different #1.

**A8. Trust attenuation** — at each hop, only $\beta$ fraction propagates → after $k$ hops, only $\beta^k$ survives. **Trust splitting** — page with $k$ out-links splits trust by $1/k$. Captured by $1/d_i$ in $M_{ji}$.

**A9.** $y = x + \beta M (\beta y / M + (1-\beta)/N) + (1-\beta)/N$. Round-trip $t \to \mathrm{farm} \to t$ gives $\beta^2$. $(1-\beta)/N$ is $O(1/N) \approx 10^{-9}$ — negligible. For $\beta = 0.9$: $1/(1-0.81) \approx 5.26$.

**A10.**
- **Per-page output.** PR: 1 score; TrustRank: 1 trust score; HITS: 2 scores; SpamMass: 1 ratio.
- **Teleport/normalization.** PR: uniform; TrustRank: trusted seeds; HITS: no teleport, L1/L2 norm; SpamMass: derived (no iteration).
- **Question.** PR: "important?"; TrustRank: "trusted?"; HITS: "hub or authority?"; SpamMass: "fraction from spam?"

**A11.** Direct TrustRank thresholding misclassifies legitimate isolated pages (low $r^+$ regardless of legitimacy). E.g., legit blog with $r_p = 10^{-4}$, $r^+_p = 9 \times 10^{-5}$. Threshold 0.001 flags as spam. SpamMass $= 0.10$ → not flagged. Normalization removes "distance bias".

**A12.** **(B)** $(1-\beta)/|S|$.

**A13.** $1/(1 - 0.25) = 1.333$. **(B)**.

**A14. False.** $h, a$ explode or vanish without normalization since the eigenvalue of $A^T A$ is generally not 1.

**A15.** **(D)**. Controlled domains have negligible spam. (B) is reasonable but top-PR pages can include compromised popular sites.

---

## §12 — Ending Key Notes (Revision Cards)

| Card                          | Quick-fact                                                                  |
|-------------------------------|-----------------------------------------------------------------------------|
| PR's 3 weaknesses             | Topic blind / single score / link-spam vulnerable                           |
| Topic-PR formula              | $r = \beta M r + (1-\beta) v_S$, $v_S[j] = 1/|S|$ if $j \in S$              |
| Topic-PR teleport             | $(1-\beta)/|S|$ to every $j \in S$, 0 to others                             |
| Algorithm change              | ONE line: redistribute to S only                                            |
| Term spam                     | Hidden keyword stuffing, copying top results                                |
| Google's term-spam fix        | Trust anchor text, not page's own body                                      |
| 3 page types                  | Inaccessible / Accessible / Owned                                           |
| Spam farm goal                | Maximize PR of target $t$ via mutual links with $M$ owned pages             |
| Spam farm formula             | $y = x/(1-\beta^2) + c \cdot M/N$, $c = \beta/(1+\beta)$                    |
| Multiplier ($\beta = 0.85$)   | $1/(1-\beta^2) \approx 3.6$                                                  |
| TrustRank                     | Topic-PR with seeds = trusted pages                                          |
| Trust attenuation             | Trust decays $\beta$ per hop                                                 |
| Trust splitting               | Page with $k$ out-links splits trust by $1/k$                                |
| Seed set choices              | Top-$k$ by PR, controlled domains (`.edu`/`.gov`/`.mil`)                     |
| Spam Mass formula             | $\mathrm{SM}(p) = (r_p - r^+_p)/r_p$                                         |
| Spam Mass intuition           | Fraction of $p$'s rank from non-trusted sources                              |
| HITS scores                   | $h_i$ hub, $a_j$ authority                                                   |
| HITS iteration                | $h \leftarrow A a$, $a \leftarrow A^T h$, normalize each step                |
| HITS eigen-equation           | $a$ = principal eigenvector of $A^T A$                                       |
| PR vs HITS                    | PR: 1 score, query-indep, teleport. HITS: 2 scores, query-spec, normalize.   |

---

## §13 — Formula & Algorithm Reference

| Concept                  | Formula                                                                | Use                                            |
|--------------------------|------------------------------------------------------------------------|------------------------------------------------|
| Topic-Sensitive PR       | $r = \beta M r + (1-\beta) v_S$                                        | Bias rank to a specific topic.                 |
| Topic-PR teleport        | $(1-\beta)/|S|$ to seeds only                                          | One-line modification of W8-9 algorithm.        |
| Spam farm rank           | $y = x/(1-\beta^2) + (\beta/(1+\beta)) \cdot M/N$                      | Estimating link-farm effectiveness.            |
| TrustRank                | Same as Topic-PR with trusted seeds                                    | Demoting link-spam farms automatically.        |
| Trust propagation        | $t_q = \beta \sum_{p \to q} t_p / |O_p| + \mathrm{teleport}$           | Per-iteration update.                          |
| Spam Mass                | $\mathrm{SM}(p) = (r_p - r^+_p)/r_p$                                   | Fractional spam contribution.                  |
| HITS authority           | $a = A^T h$ → principal eigenvector of $A^T A$                         | Pages linked-to by good hubs.                  |
| HITS hub                 | $h = A a$ → principal eigenvector of $A A^T$                           | Pages linking-to good authorities.             |

**Connections to other weeks:**
- **W8-9 PageRank.** Every algorithm here is a parametrization of W8-9 power iteration.
- **W16 Community Detection.** Spectral clustering uses the same eigenvector machinery on the graph Laplacian.

---

*End of W12 Advanced Link Analysis exam-prep document.*
