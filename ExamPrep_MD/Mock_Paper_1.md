---
title: "BDA Final — Mock Paper 1"
subtitle: "3-hour final exam · 100 marks · Closed book · Calculator allowed"
author: "BDA Final Exam Prep · Comprehensive Tutor"
course: "CS-404 Big Data Analytics — Dr. Syed Imran Ali"
exam: "Final ~ 2026-05-16"
---

# BDA Final — Mock Paper 1

**Time allowed:** 3 hours (180 minutes) · **Total marks:** 100 · **Pass mark target:** 65/100

---

## Instructions to candidates

1. **Attempt ALL questions.** The paper has three sections (A, B, C) totalling 100 marks.
2. **Show every step.** This examiner awards generous partial credit for correct method even when arithmetic slips. Write the formula first, then plug in numbers, then simplify.
3. **State your assumptions.** When a question is ambiguous (e.g. tie-breaking in $k$-means, which logarithm base), write the assumption you made and proceed.
4. **Calculator** (non-programmable) is permitted. **No notes, no books, no phones.**
5. **Time budget (suggested).** Section A: 30 min · Section B: 50 min · Section C: 100 min.
6. Answer each question on a fresh page. Number every sub-part clearly.

> **READ FIRST.** A question that asks you to "trace" or "walk through" expects the *intermediate state at every step* — not just the final answer. A correct final number with no working scores fewer marks than a wrong final number with clear, correct reasoning.

---

# SECTION A — Short Numerical (4 × 5 marks = 20 marks)

> Roughly 7 minutes per question. Show all arithmetic.

---

## Question A1 [Bonferroni's Principle · 5 marks]

A bank screens $N = 200{,}000$ daily wire transfers for a "money-laundering signature." Under the null hypothesis (no laundering), the per-transfer probability of triggering the signature by random coincidence is $p = 10^{-4}$. Historically, the bank knows that approximately **8 transfers per day** are genuine laundering attempts.

**(a) [2 marks]** Compute the expected number of false-positive flags per day.

**(b) [1 mark]** What fraction of all flagged transfers are *real* laundering (assuming independent counts)?

**(c) [2 marks]** The bank wants the family-wise false-positive rate to be at most $\alpha = 0.05$. State the Bonferroni-corrected per-test threshold and comment on whether the original $p$ satisfies it.

> **Hint.** Expected false positives $= N \cdot p$. Bonferroni-corrected threshold $= \alpha / N$.

---

## Question A2 [Apriori — Support and $L_1, L_2$ · 5 marks]

A small grocery has the following 5 transactions. Items $= \{A, B, C, D, E\}$. Minimum-support threshold $s = 3$ (count, not fraction).

| Basket | Items                |
|--------|----------------------|
| $T_1$  | $\{A, B, C\}$        |
| $T_2$  | $\{A, B, D\}$        |
| $T_3$  | $\{A, C, D\}$        |
| $T_4$  | $\{B, C, D\}$        |
| $T_5$  | $\{A, B, C, D\}$     |

**(a) [2 marks]** Compute $\sigma(\{X\})$ for each item $X$. State $L_1$.

**(b) [3 marks]** Generate $C_2$ from $L_1$ using the join + prune rule, count support for each candidate, and state $L_2$.

> **Hint.** With $|L_1| = m$, $|C_2| = \binom{m}{2}$ before pruning. Show every candidate, even those that fail.

---

## Question A3 [MinHash — Signature Matrix · 5 marks]

The shingle-membership matrix below shows 4 rows and 3 documents $C_1, C_2, C_3$. Two hash functions are given:

- $h_1(x) = x \bmod 5$
- $h_2(x) = (2x + 3) \bmod 5$

| Row $r$ | $C_1$ | $C_2$ | $C_3$ |
|---------|-------|-------|-------|
| 1       | 1     | 0     | 1     |
| 2       | 0     | 1     | 1     |
| 3       | 1     | 1     | 0     |
| 4       | 0     | 1     | 1     |

**(a) [4 marks]** Apply the row-by-row MinHash algorithm to fill the $2 \times 3$ signature matrix $M_{\text{sig}}$. Show the matrix state **after each row** is processed.

**(b) [1 mark]** Estimate $\hat{J}(C_1, C_3)$ from the final signatures.

> **Hint.** Initialise every entry of $M_{\text{sig}}$ to $\infty$. For each row $r$, compute $h_1(r)$ and $h_2(r)$; for every column with a 1 in row $r$, replace its slot with the running minimum.

---

## Question A4 [Cosine Similarity · 5 marks]

Two users rate the same 4 movies on a 1–5 scale:

| User  | $M_1$ | $M_2$ | $M_3$ | $M_4$ |
|-------|-------|-------|-------|-------|
| Usman | 4     | 5     | 2     | 3     |
| Vikas | 5     | 3     | 4     | 4     |

**(a) [4 marks]** Compute the **raw cosine similarity** $\cos(\text{Usman}, \text{Vikas})$ using the rating vectors directly (no mean centring).

**(b) [1 mark]** Briefly state how you would change the calculation to obtain the **Pearson** correlation instead.

> **Hint.** $\cos(u, v) = \dfrac{u \cdot v}{\|u\| \, \|v\|}$. Compute the dot product and the two L2 norms separately.

---

# SECTION B — Medium Numerical (3 × 10 marks = 30 marks)

> Roughly 17 minutes per question. Each question has multiple parts that build on the same dataset.

---

## Question B1 [User-User Collaborative Filtering · 10 marks]

The following 4×5 utility matrix shows ratings on a 1–5 scale. A "?" denotes an unrated movie. We will predict **Sara's rating for $M_3$** using user-user CF with $k = 2$ nearest neighbours and **Pearson correlation** similarity.

| User  | $M_1$ | $M_2$ | $M_3$ | $M_4$ | $M_5$ |
|-------|-------|-------|-------|-------|-------|
| Ali   | 5     | 3     | 4     | 4     | 2     |
| Bilal | 3     | 1     | 2     | 3     | 5     |
| Sara  | 4     | 3     | ?     | 5     | 2     |
| Hina  | 1     | 5     | 5     | 2     | 1     |

**(a) [2 marks]** State which items Sara has co-rated with each other user. Compute Sara's mean rating $\bar{r}_{\text{Sara}}$ over those movies.

**(b) [5 marks]** Compute Pearson similarity $\text{sim}(\text{Sara}, u)$ for $u \in \{\text{Ali, Bilal, Hina}\}$. (Restrict each calculation to the four movies Sara rated.)

**(c) [2 marks]** Identify the top $k = 2$ neighbours by absolute similarity.

**(d) [1 mark]** Predict $\hat{r}(\text{Sara}, M_3)$ using the weighted-average formula $\hat{r}_{xi} = \dfrac{\sum_{y \in N} \text{sim}(x, y) \cdot r_{yi}}{\sum_{y \in N} |\text{sim}(x, y)|}$.

> **Partial credit.** Even if you cannot finish (b), you may use the similarities $\text{sim}(\text{Sara, Ali}) = 0.80$ and $\text{sim}(\text{Sara, Bilal}) = -0.32$ in (c)–(d) for partial credit. State clearly that you are using assumed values.

---

## Question B2 [PageRank with Dead-End · 10 marks]

Consider the following directed graph on 4 nodes:

- Edges: $A \to B$, $A \to C$, $B \to C$, $C \to A$, $D \to (\text{no out-link})$.

Use the **production / leak-handling** form with $\beta = 0.8$, initial vector $r^{(0)} = (1/4, 1/4, 1/4, 1/4) = (0.25, 0.25, 0.25, 0.25)$ in node order $(A, B, C, D)$.

The update rule is:

$$ r'^{\text{new}} = \beta M r^{\text{old}}, \qquad S = \sum_j r'^{\text{new}}_j, \qquad r^{\text{new}}_j = r'^{\text{new}}_j + \frac{1 - S}{N} $$

**(a) [3 marks]** Write down the column-stochastic matrix $M$. Note explicitly which column corresponds to the dead-end and what its entries are.

**(b) [6 marks]** Perform **three** power-iteration steps. After each iteration, report:
- the un-leaked vector $r'^{\text{new}} = \beta M r^{\text{old}}$,
- the leak amount $1 - S$,
- the redistributed result $r^{\text{new}}$,
- and verify $\sum r^{\text{new}} = 1$.

**(c) [1 mark]** State which node has the **highest** rank after iteration 3, and which node has the lowest. Briefly justify why the dead-end node behaves the way it does.

> **Hint.** Round each entry to 3 decimal places. The leak $1 - S$ should be a small positive number after every iteration; if it is negative, you have made an error.

---

## Question B3 [k-Means · 10 marks]

The following six 2-D points are to be clustered with $k$-means, $k = 2$:

$$ P_1 = (1, 1), \;\; P_2 = (2, 1), \;\; P_3 = (1, 2), \;\; P_4 = (8, 8), \;\; P_5 = (9, 8), \;\; P_6 = (8, 9) $$

Initial centroids: $c_1^{(0)} = (2, 2)$, $c_2^{(0)} = (7, 7)$.

**(a) [4 marks]** Iteration 1 — for each point, compute its Euclidean distance to both centroids (you may report distances *or* squared distances) and assign it to the nearest cluster. Present results in a clean table.

**(b) [3 marks]** Recompute the centroids $c_1^{(1)}, c_2^{(1)}$ from the new assignments. Show the arithmetic.

**(c) [2 marks]** Iteration 2 — re-assign every point under the new centroids. Has any point changed cluster? State whether the algorithm has converged and justify.

**(d) [1 mark]** State the final clusters and the final centroids.

> **Tip.** When two distances tie, you may break ties arbitrarily; *state* your tie-break rule.

---

# SECTION C — Large Multi-Part Numerical (2 × 25 marks = 50 marks)

> Roughly 50 minutes per question. These are the equivalent of the midterm's CURE long-form. Multiple parts; later parts build on earlier results — but every part is **independently marked**, so do not skip.

---

## Question C1 [Topic-Sensitive PageRank + Spam Mass · 25 marks]

Consider the following directed graph on **5 nodes** $\{1, 2, 3, 4, 5\}$:

- Edges: $1 \to 2$, $1 \to 3$, $2 \to 3$, $3 \to 1$, $4 \to 1$, $4 \to 5$, $5 \to 4$.

The adjacency lists give out-degrees $d_1 = 2,\; d_2 = 1,\; d_3 = 1,\; d_4 = 2,\; d_5 = 1$. There are **no dead-ends** in this graph.

We will compute **Topic-Sensitive PageRank** with teleport set $S = \{1\}$ and damping $\beta = 0.85$. The update rule:

$$ r^{\text{new}} = \beta \, M \, r^{\text{old}} + (1 - \beta) \, v_S $$

where $v_S$ is a vector with $1/|S|$ in positions corresponding to $S$ and 0 elsewhere — here $v_S = (1, 0, 0, 0, 0)^\top$.

**(a) [4 marks]** Build the column-stochastic transition matrix $M$ from the graph. Present it as a $5 \times 5$ table with columns labelled "from $i$" and rows labelled "to $j$." Verify that every column sums to 1.

**(b) [8 marks]** Starting from $r^{(0)} = (0.2, 0.2, 0.2, 0.2, 0.2)^\top$, perform **two iterations** of Topic-Sensitive PageRank. For each iteration, show:
- $M r^{(t)}$ (intermediate),
- $\beta M r^{(t)}$,
- the teleport addition $(1 - \beta) v_S$,
- $r^{(t+1)}$ rounded to 3 decimals,
- the sum $\sum r^{(t+1)}_j$ (verify $= 1$).

**(c) [4 marks]** A **vanilla** PageRank iteration on the same graph from $r^{(0)}$ would teleport uniformly to all 5 nodes, i.e. with $v = (0.2, 0.2, 0.2, 0.2, 0.2)^\top$ instead of $v_S$. Compute $r^{(1)}_{\text{vanilla}}$ for one iteration, then briefly compare it with $r^{(1)}_{\text{topic}}$ from part (b). Which node gains rank under the topic teleport, and why?

**(d) [5 marks]** Suppose we are also given the following hypothetical TrustRank values $r^+$ (Topic-PR with seed = trusted nodes) and the corresponding *vanilla* PageRank values $r$ (treat both as given inputs for this part):

| Node | $r$ (vanilla PR) | $r^+$ (TrustRank) |
|------|------------------|-------------------|
| 1    | 0.30             | 0.40              |
| 2    | 0.20             | 0.15              |
| 3    | 0.25             | 0.25              |
| 4    | 0.15             | 0.10              |
| 5    | 0.10             | 0.05              |

Compute the **Spam Mass** $\mathrm{SM}(p) = (r_p - r^+_p) / r_p$ for every node. Using a threshold of $\mathrm{SM} \ge 0.4$, identify which node(s) you would label as spam.

**(e) [4 marks]** *Conceptual.* In the topic-sensitive formulation $r = \beta M r + (1-\beta) v_S$, suppose we lower $\beta$ from 0.85 to 0.50 while keeping $S = \{1\}$. Explain in 3–5 lines what happens to:
1. the rank of node 1,
2. the rank of nodes far from node 1 in the graph,
3. the convergence speed of power iteration,
4. the algorithm's robustness to spam farms.

> **Examiner-style hint.** Lay out parts (a) and (b) in a single fat table where each iteration gets one row. Markers can grade much faster, and you can spot-check column sums.

---

## Question C2 [Community Detection — Girvan-Newman + Spectral · 25 marks]

Consider the **undirected** graph on **6 nodes** $\{1, 2, 3, 4, 5, 6\}$:

- Edges (7 total): $\{1\text{-}2,\; 1\text{-}3,\; 2\text{-}3,\; 3\text{-}4,\; 4\text{-}5,\; 4\text{-}6,\; 5\text{-}6\}$.

This is the canonical "barbell": two triangles glued by a single bridge edge $3\text{-}4$.

```
   1            5
   |\          /|
   | \        / |
   |  3 ---- 4  |
   | /        \ |
   |/          \|
   2            6
```

**(a) [8 marks]** Use **Brandes' BFS-based algorithm with source node $s = 1$** to compute, for each edge in the BFS DAG rooted at node 1:
1. the BFS level of every node,
2. the shortest-path count $\sigma(v)$ for every node $v$,
3. the credit propagated along every edge of the DAG (bottom-up).

Present the result as a table of edge betweenness *contributions from source 1* for each of the 7 edges (some will be 0 if the edge is not in the DAG).

**(b) [5 marks]** The **total** edge betweenness (summed over all sources, divided by 2) for this graph is given in the table below. State which edge has the highest betweenness, remove it, and **recompute** the edge betweenness on the remaining graph.

| Edge       | Total $b(e)$ |
|------------|--------------|
| 1–2        | 1            |
| 1–3        | 4            |
| 2–3        | 4            |
| **3–4**    | **9**        |
| 4–5        | 4            |
| 4–6        | 4            |
| 5–6        | 1            |

> **Tip.** After removing the highest-betweenness edge, the graph splits into two disconnected components. Compute betweenness independently *within* each component.

**(c) [8 marks]** Removing the bridge produces the partition $C_1 = \{1, 2, 3\},\; C_2 = \{4, 5, 6\}$. Compute the **modularity** $Q$ of this partition on the **original** (un-cut) graph. Use the block form

$$ Q = \sum_c \left[ \frac{L_c}{m} - \left( \frac{D_c}{2m} \right)^2 \right] $$

where $L_c$ = number of internal edges of community $c$ (both endpoints in $c$), $D_c$ = sum of degrees of nodes in $c$, $m$ = total edges. Show every step (degrees, $m$, $L_c$, $D_c$, then plug in).

**(d) [4 marks]** Build the graph **Laplacian** $L = D - A$ for the original graph, where $D = \mathrm{diag}(k_1, \ldots, k_6)$ and $A$ is the adjacency matrix. Present $L$ as a $6 \times 6$ matrix. Then explain in 3–5 lines:
1. why the all-ones vector $\mathbf{1}_6$ is always an eigenvector of $L$ and what its eigenvalue is,
2. what the **Fiedler vector** is and how its sign pattern would partition this graph (no need to actually solve for eigenvectors numerically — describe the expected sign assignment based on graph structure).

> **Examiner-style hint.** In (c), $\sum_i k_i = 2m$ — double-check this *before* plugging into the formula. In (d), do not try to compute $\lambda_2$ by hand; you only need to write $L$ and discuss the qualitative structure of the Fiedler vector.

---

# Examiner Tips (read before you start writing)

> **Time discipline.** Section A questions are designed to take 7 minutes each. If a Section A question is taking 15 minutes, mark it, move on, and come back at the end. Do **not** sacrifice Section C marks for a stuck Section A part.

> **Show the formula first.** This examiner consistently awards method marks even when the final number is wrong. Write `Pearson sim = num / (||u|| · ||v||)` *before* plugging in numbers — that single line is worth 1–2 marks on its own in most numerical questions.

> **Verify column sums and probability sums.** PageRank vectors must sum to 1 every iteration; column-stochastic $M$ must have every column sum to 1; modularity must satisfy $Q \in [-0.5, 1]$. A 30-second sanity check at the end of each part catches arithmetic slips that would otherwise cost you 4–5 marks.

> **Write down assumptions for ambiguous questions.** If the question says "min-support = 3" but doesn't specify count vs fraction, write *"I am taking $s = 3$ as a count threshold"* and proceed. The examiner cannot deduct marks for an explicit, defensible assumption.

---

*End of Mock Paper 1.*
