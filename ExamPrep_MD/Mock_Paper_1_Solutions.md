---
title: "BDA Final — Mock Paper 1 Solutions"
subtitle: "Worked solutions with mark allocation"
author: "BDA Final Exam Prep · Comprehensive Tutor"
course: "CS-404 Big Data Analytics — Dr. Syed Imran Ali"
exam: "Final ~ 2026-05-16"
---

# BDA Final — Mock Paper 1 — Worked Solutions

> **How to use this file.** First attempt the paper *unaided* under timed conditions. Only then read the solutions. For every part you missed, write the *exact* mistake on a separate sheet — most marks lost on this examiner come from arithmetic slips and missing formulas, not from conceptual gaps.

> **Mark allocation philosophy.** This examiner gives **method marks** liberally. Throughout these solutions, the per-line mark hints (e.g. *[1 mark — formula]*, *[1 mark — substitution]*) reflect how he typically allocates partial credit. Even on a wrong final answer, you keep all method marks if you wrote the correct intermediate steps.

---

# SECTION A — Short Numerical (4 × 5 = 20 marks)

---

## Solution A1 [Bonferroni — 5 marks]

**(a) Expected false positives.** *[2 marks]*

$$ \mathbb{E}[\text{FP}] = N \cdot p = 200{,}000 \times 10^{-4} = 20 $$

So we expect **20 false-positive flags per day**.

**(b) Real-fraud fraction.** *[1 mark]*

True positives ≈ 8 per day. Total flagged ≈ false + true = $20 + 8 = 28$. Fraction real = $8 / 28 \approx 0.286$ — about **29% of all flagged transfers are genuine laundering**, the other 71% are noise.

**(c) Bonferroni-corrected threshold.** *[2 marks]*

$$ \alpha_{\text{per-test}} = \frac{\alpha}{N} = \frac{0.05}{200{,}000} = 2.5 \times 10^{-7} $$

The original $p = 10^{-4}$ is **400× too loose** for the family-wise rate to be controlled. Either tighten the per-test threshold to $\le 2.5 \times 10^{-7}$, or pre-filter $N$ down to a much smaller candidate set.

> *Marker note.* Award 2 marks for $N \cdot p = 20$, 1 mark for any reasonable comparison answer in (b), and 2 marks for the correct Bonferroni number with a comment.

---

## Solution A2 [Apriori — 5 marks]

**(a) Singleton supports and $L_1$.** *[2 marks]*

| Item | Baskets containing it | $\sigma$ |
|------|------------------------|----------|
| $A$  | $T_1, T_2, T_3, T_5$   | 4        |
| $B$  | $T_1, T_2, T_4, T_5$   | 4        |
| $C$  | $T_1, T_3, T_4, T_5$   | 4        |
| $D$  | $T_2, T_3, T_4, T_5$   | 4        |
| $E$  | (none)                 | 0        |

With threshold $s = 3$: $L_1 = \{ \{A\}, \{B\}, \{C\}, \{D\} \}$. Item $E$ is dropped.

**(b) $C_2$, support, and $L_2$.** *[3 marks]*

Join + prune from $L_1$ produces every pair of frequent singletons (no pruning shrinks $C_2$ here because every $(k-1) = 1$-subset is in $L_1$):

$$ C_2 = \{ \{A,B\}, \{A,C\}, \{A,D\}, \{B,C\}, \{B,D\}, \{C,D\} \} $$

Count support by scanning every basket:

| Pair      | Baskets containing it | $\sigma$ | Frequent? |
|-----------|------------------------|----------|-----------|
| $\{A,B\}$ | $T_1, T_2, T_5$        | 3        | ✓         |
| $\{A,C\}$ | $T_1, T_3, T_5$        | 3        | ✓         |
| $\{A,D\}$ | $T_2, T_3, T_5$        | 3        | ✓         |
| $\{B,C\}$ | $T_1, T_4, T_5$        | 3        | ✓         |
| $\{B,D\}$ | $T_2, T_4, T_5$        | 3        | ✓         |
| $\{C,D\}$ | $T_3, T_4, T_5$        | 3        | ✓         |

$$ L_2 = \{ \{A,B\}, \{A,C\}, \{A,D\}, \{B,C\}, \{B,D\}, \{C,D\} \} \quad (\text{all six pairs frequent}) $$

> *Marker note.* 1 mark for $L_1$, 1 mark for naming the 6 candidates correctly, 2 marks for the support counts and final $L_2$. No mark deduction if the student also lists $E$ in $C_2$ candidates as long as they correctly drop it for failing the join condition.

---

## Solution A3 [MinHash — 5 marks]

**Hash values for each row:**

| Row $r$ | $h_1(r) = r \bmod 5$ | $h_2(r) = (2r + 3) \bmod 5$ |
|---------|----------------------|------------------------------|
| 1       | 1                    | 5 mod 5 = 0                  |
| 2       | 2                    | 7 mod 5 = 2                  |
| 3       | 3                    | 9 mod 5 = 4                  |
| 4       | 4                    | 11 mod 5 = 1                 |

**(a) Row-by-row trace.** *[4 marks]*

**Initialize** $M_{\text{sig}}$ to all $\infty$:

|       | $C_1$    | $C_2$    | $C_3$    |
|-------|----------|----------|----------|
| $h_1$ | $\infty$ | $\infty$ | $\infty$ |
| $h_2$ | $\infty$ | $\infty$ | $\infty$ |

**Row $r=1$** ($h_1=1$, $h_2=0$). $C_1 = 1$ → update $C_1$. $C_2 = 0$ → skip. $C_3 = 1$ → update $C_3$.

|       | $C_1$ | $C_2$    | $C_3$ |
|-------|-------|----------|-------|
| $h_1$ | 1     | $\infty$ | 1     |
| $h_2$ | 0     | $\infty$ | 0     |

**Row $r=2$** ($h_1=2$, $h_2=2$). $C_1 = 0$ → skip. $C_2 = 1$ → update. $C_3 = 1$ → $\min(1, 2) = 1$, $\min(0, 2) = 0$ (no change).

|       | $C_1$ | $C_2$ | $C_3$ |
|-------|-------|-------|-------|
| $h_1$ | 1     | 2     | 1     |
| $h_2$ | 0     | 2     | 0     |

**Row $r=3$** ($h_1=3$, $h_2=4$). $C_1 = 1$ → $\min(1,3) = 1$, $\min(0,4) = 0$ (no change). $C_2 = 1$ → $\min(2,3) = 2$, $\min(2,4) = 2$ (no change). $C_3 = 0$ → skip.

|       | $C_1$ | $C_2$ | $C_3$ |
|-------|-------|-------|-------|
| $h_1$ | 1     | 2     | 1     |
| $h_2$ | 0     | 2     | 0     |

**Row $r=4$** ($h_1=4$, $h_2=1$). $C_1 = 0$ → skip. $C_2 = 1$ → $\min(2,4) = 2$, $\min(2,1) = 1$ (update $h_2$). $C_3 = 1$ → $\min(1,4) = 1$, $\min(0,1) = 0$ (no change).

**Final signature matrix:**

|       | $C_1$ | $C_2$ | $C_3$ |
|-------|-------|-------|-------|
| $h_1$ | 1     | 2     | 1     |
| $h_2$ | 0     | 1     | 0     |

**(b) Estimate $\hat{J}(C_1, C_3)$.** *[1 mark]*

The two signatures of $C_1$ and $C_3$ are identical: $(1, 0)$ and $(1, 0)$. So both rows agree:

$$ \hat{J}(C_1, C_3) = \frac{\#\text{matching rows}}{\#\text{rows}} = \frac{2}{2} = 1.0 $$

(With only $n = 2$ hash functions this estimator has very high variance; the true Jaccard from the membership matrix is $J(C_1, C_3) = |\{1\}|/|\{1, 2, 3, 4\}| = 1/4 = 0.25$, but the question asks for the *estimate from the signatures*, which is 1.0.)

> *Marker note.* 4 marks for any 4 of (initialise to ∞, correct row-1 trace, correct row-2 trace, correct row-3 trace, correct row-4 trace, correct final matrix). 1 mark for the Jaccard estimate. Forgetting to initialise to $\infty$ is the most common error and costs 1–2 marks.

---

## Solution A4 [Cosine Similarity — 5 marks]

**(a) Raw cosine.** *[4 marks]*

Vectors: $u = (4, 5, 2, 3)$, $v = (5, 3, 4, 4)$.

**Step 1 — dot product.** *[1 mark]*

$$ u \cdot v = (4)(5) + (5)(3) + (2)(4) + (3)(4) = 20 + 15 + 8 + 12 = 55 $$

**Step 2 — norms.** *[2 marks]*

$$ \|u\| = \sqrt{4^2 + 5^2 + 2^2 + 3^2} = \sqrt{16 + 25 + 4 + 9} = \sqrt{54} \approx 7.348 $$

$$ \|v\| = \sqrt{5^2 + 3^2 + 4^2 + 4^2} = \sqrt{25 + 9 + 16 + 16} = \sqrt{66} \approx 8.124 $$

**Step 3 — cosine.** *[1 mark]*

$$ \cos(u, v) = \frac{55}{7.348 \times 8.124} = \frac{55}{59.70} \approx 0.921 $$

The two users are highly similar (raw cosine close to 1 because their rating vectors point in nearly the same direction in $\mathbb{R}^4$).

**(b) From cosine to Pearson.** *[1 mark]*

**Mean-centre each vector before computing cosine.** Replace $u$ with $u_c = u - \bar{u} \mathbf{1}$ and likewise $v_c = v - \bar{v} \mathbf{1}$, where $\bar{u} = (4+5+2+3)/4 = 3.5$ and $\bar{v} = (5+3+4+4)/4 = 4$. Then $\text{Pearson}(u, v) = \cos(u_c, v_c)$. Pearson differs from cosine *only* by this centring step.

> *Marker note.* Full 4 marks for parts of (a) require: 1 for dot, 2 for both norms (1 each), 1 for the final ratio. The 1 mark in (b) is awarded for the keyword **mean-centring**.

---

# SECTION B — Medium Numerical (3 × 10 = 30 marks)

---

## Solution B1 [User-User CF — 10 marks]

**(a) Co-rated items and Sara's mean.** *[2 marks]*

Sara has rated $\{M_1, M_2, M_4, M_5\}$ (she did not rate $M_3$). Each of Ali, Bilal, Hina has rated all five movies, so Sara's set of co-rated items with each of them is $\{M_1, M_2, M_4, M_5\}$.

$$ \bar{r}_{\text{Sara}} = (4 + 3 + 5 + 2)/4 = 14/4 = 3.5 $$

So Sara's centred vector over $(M_1, M_2, M_4, M_5)$ is

$$ \text{Sara}_c = (4-3.5,\; 3-3.5,\; 5-3.5,\; 2-3.5) = (0.5,\; -0.5,\; 1.5,\; -1.5) $$

with $\|\text{Sara}_c\|^2 = 0.25 + 0.25 + 2.25 + 2.25 = 5.0$, so $\|\text{Sara}_c\| = \sqrt{5} \approx 2.236$.

**(b) Pearson similarities.** *[5 marks — about 1.5 marks each]*

**Sara vs Ali** over $(M_1, M_2, M_4, M_5)$. Ali's ratings on those four = $(5, 3, 4, 2)$, mean $= 14/4 = 3.5$.

$$ \text{Ali}_c = (1.5,\; -0.5,\; 0.5,\; -1.5) $$

Numerator:

$$ (0.5)(1.5) + (-0.5)(-0.5) + (1.5)(0.5) + (-1.5)(-1.5) = 0.75 + 0.25 + 0.75 + 2.25 = 4.0 $$

$\|\text{Ali}_c\|^2 = 2.25 + 0.25 + 0.25 + 2.25 = 5.0$, so $\|\text{Ali}_c\| = \sqrt{5} \approx 2.236$.

$$ \text{sim}(\text{Sara}, \text{Ali}) = \frac{4.0}{\sqrt{5} \cdot \sqrt{5}} = \frac{4.0}{5.0} = +0.800 $$

**Sara vs Bilal.** Bilal on $(M_1, M_2, M_4, M_5) = (3, 1, 3, 5)$, mean $= 12/4 = 3.0$. $\text{Bilal}_c = (0,\; -2,\; 0,\; +2)$.

Numerator: $(0.5)(0) + (-0.5)(-2) + (1.5)(0) + (-1.5)(2) = 0 + 1 + 0 - 3 = -2.0$.
$\|\text{Bilal}_c\|^2 = 0 + 4 + 0 + 4 = 8$, so $\|\text{Bilal}_c\| = 2\sqrt{2} \approx 2.828$.

$$ \text{sim}(\text{Sara}, \text{Bilal}) = \frac{-2.0}{\sqrt{5} \cdot 2\sqrt{2}} = \frac{-2.0}{\sqrt{40}} = \frac{-2.0}{6.325} \approx -0.316 $$

**Sara vs Hina.** Hina on $(M_1, M_2, M_4, M_5) = (1, 5, 2, 1)$, mean $= 9/4 = 2.25$. $\text{Hina}_c = (-1.25,\; 2.75,\; -0.25,\; -1.25)$.

Numerator: $(0.5)(-1.25) + (-0.5)(2.75) + (1.5)(-0.25) + (-1.5)(-1.25)$
$= -0.625 - 1.375 - 0.375 + 1.875 = -0.500$.

$\|\text{Hina}_c\|^2 = 1.5625 + 7.5625 + 0.0625 + 1.5625 = 10.75$, so $\|\text{Hina}_c\| = \sqrt{10.75} \approx 3.279$.

$$ \text{sim}(\text{Sara}, \text{Hina}) = \frac{-0.500}{\sqrt{5} \cdot \sqrt{10.75}} = \frac{-0.500}{7.331} \approx -0.068 $$

**Summary:**

| Neighbour | Pearson sim | $|\text{sim}|$ |
|-----------|-------------|----------------|
| Ali       | $+0.800$    | 0.800          |
| Bilal     | $-0.316$    | 0.316          |
| Hina      | $-0.068$    | 0.068          |

**(c) Top-2 neighbours.** *[2 marks]*

By absolute similarity: **Ali** ($0.800$) and **Bilal** ($0.316$).

**(d) Predict Sara's rating for $M_3$.** *[1 mark]*

Use the weighted-average formula with the two neighbours' actual $M_3$ ratings $r(\text{Ali}, M_3) = 4$ and $r(\text{Bilal}, M_3) = 2$:

$$ \hat{r}(\text{Sara}, M_3) = \frac{(0.800)(4) + (-0.316)(2)}{0.800 + 0.316} = \frac{3.200 - 0.632}{1.116} = \frac{2.568}{1.116} \approx 2.30 $$

**Predicted rating ≈ 2.3 stars.**

> *Marker note.* For (b), award 1.5 marks per similarity (1 for the centred vectors and numerator, 0.5 for the final ratio). Award full marks even if signs are accidentally swapped, provided the final top-2 in (c) is consistent. The negative sim for Bilal *correctly* enters the predictor with a minus sign.

---

## Solution B2 [PageRank with Dead-End — 10 marks]

**(a) Build $M$.** *[3 marks]*

Out-degrees: $d_A = 2$ (out-links to $B, C$), $d_B = 1$ (to $C$), $d_C = 1$ (to $A$), $d_D = 0$ (**dead-end**). Column $D$ is therefore **all zeros**.

|       | from $A$ | from $B$ | from $C$ | from $D$ |
|-------|----------|----------|----------|----------|
| row $A$ | 0        | 0        | 1        | 0        |
| row $B$ | 1/2      | 0        | 0        | 0        |
| row $C$ | 1/2      | 1        | 0        | 0        |
| row $D$ | 0        | 0        | 0        | 0        |

**Column sums:** $A$: $1/2 + 1/2 = 1$ ✓. $B$: $1$ ✓. $C$: $1$ ✓. $D$: $0$ ❌ — that's the dead-end signature.

**(b) Three iterations.** *[6 marks — 2 each]*

**Iteration 1.** $r^{(0)} = (0.25, 0.25, 0.25, 0.25)^\top$.

$M r^{(0)}$ row-by-row:
- row $A$: $1 \cdot 0.25 = 0.250$
- row $B$: $0.5 \cdot 0.25 = 0.125$
- row $C$: $0.5 \cdot 0.25 + 1 \cdot 0.25 = 0.375$
- row $D$: $0$

$\beta M r^{(0)} = 0.8 \cdot (0.250, 0.125, 0.375, 0) = (0.200, 0.100, 0.300, 0.000)$.
$S = 0.200 + 0.100 + 0.300 + 0 = 0.600$. Leak $1 - S = 0.400$. Per-node leak $= 0.400/4 = 0.100$.
$r^{(1)} = (0.200 + 0.100,\; 0.100 + 0.100,\; 0.300 + 0.100,\; 0 + 0.100) = (0.300,\; 0.200,\; 0.400,\; 0.100)$. **Sum = 1.000** ✓.

**Iteration 2.** $r^{(1)} = (0.300, 0.200, 0.400, 0.100)$.

$M r^{(1)}$:
- row $A$: $1 \cdot 0.400 = 0.400$
- row $B$: $0.5 \cdot 0.300 = 0.150$
- row $C$: $0.5 \cdot 0.300 + 1 \cdot 0.200 = 0.350$
- row $D$: $0$

$\beta M r^{(1)} = (0.320, 0.120, 0.280, 0.000)$. $S = 0.720$. Leak $= 0.280$. Per-node $= 0.070$.
$r^{(2)} = (0.390,\; 0.190,\; 0.350,\; 0.070)$. **Sum = 1.000** ✓.

**Iteration 3.** $r^{(2)} = (0.390, 0.190, 0.350, 0.070)$.

$M r^{(2)}$:
- row $A$: $1 \cdot 0.350 = 0.350$
- row $B$: $0.5 \cdot 0.390 = 0.195$
- row $C$: $0.5 \cdot 0.390 + 1 \cdot 0.190 = 0.385$
- row $D$: $0$

$\beta M r^{(2)} = (0.280, 0.156, 0.308, 0.000)$. $S = 0.744$. Leak $= 0.256$. Per-node $= 0.064$.
$r^{(3)} = (0.344,\; 0.220,\; 0.372,\; 0.064)$. **Sum = 1.000** ✓.

**(c) Highest / lowest rank, dead-end behaviour.** *[1 mark]*

After iteration 3, **highest = $C$ (0.372)**, **lowest = $D$ (0.064)**. Node $D$ has no in-links (no node points to $D$ in this graph), so the *only* rank flowing into $D$ is the uniform leak-redistribution term $(1-S)/N$. With every iteration $D$ receives exactly $(1-S)/N$ but contributes nothing back to the system — its rank is effectively pinned to that small share.

> *Marker note.* Award 2 marks per iteration for correct $r'^{\text{new}}$, leak, and final $r^{\text{new}}$ with sum-check. Forgetting to redistribute the leak is the single most common error — the symptom is sums dropping below 1.

---

## Solution B3 [k-Means — 10 marks]

**(a) Iteration 1 — assignments.** *[4 marks]*

Initial centroids $c_1 = (2, 2)$, $c_2 = (7, 7)$.

| Point         | $d^2(\cdot, c_1)$            | $d^2(\cdot, c_2)$            | Nearer | Assigned |
|---------------|------------------------------|------------------------------|--------|----------|
| $P_1 = (1,1)$ | $(1)^2 + (1)^2 = 2$          | $(6)^2 + (6)^2 = 72$         | $c_1$  | Cluster 1 |
| $P_2 = (2,1)$ | $0 + 1 = 1$                  | $25 + 36 = 61$               | $c_1$  | Cluster 1 |
| $P_3 = (1,2)$ | $1 + 0 = 1$                  | $36 + 25 = 61$               | $c_1$  | Cluster 1 |
| $P_4 = (8,8)$ | $36 + 36 = 72$               | $1 + 1 = 2$                  | $c_2$  | Cluster 2 |
| $P_5 = (9,8)$ | $49 + 36 = 85$               | $4 + 1 = 5$                  | $c_2$  | Cluster 2 |
| $P_6 = (8,9)$ | $36 + 49 = 85$               | $1 + 4 = 5$                  | $c_2$  | Cluster 2 |

So Cluster 1 = $\{P_1, P_2, P_3\}$, Cluster 2 = $\{P_4, P_5, P_6\}$.

**(b) Recompute centroids.** *[3 marks]*

$$ c_1^{(1)} = \frac{(1+2+1,\; 1+1+2)}{3} = \left( \frac{4}{3},\; \frac{4}{3} \right) \approx (1.333,\; 1.333) $$

$$ c_2^{(1)} = \frac{(8+9+8,\; 8+8+9)}{3} = \left( \frac{25}{3},\; \frac{25}{3} \right) \approx (8.333,\; 8.333) $$

**(c) Iteration 2 — re-assign.** *[2 marks]*

Every point in Cluster 1 lies near $(1, 1)$, much closer to $c_1^{(1)} \approx (1.33, 1.33)$ than to $c_2^{(1)} \approx (8.33, 8.33)$. By symmetry every Cluster-2 point is closer to $c_2^{(1)}$. Spot-check the closest case:

$$ d^2(P_2, c_1^{(1)}) = (2 - 1.333)^2 + (1 - 1.333)^2 \approx 0.444 + 0.111 = 0.556 $$
$$ d^2(P_2, c_2^{(1)}) = (2 - 8.333)^2 + (1 - 8.333)^2 \approx 40.11 + 53.78 = 93.89 $$

So $P_2$ stays in Cluster 1. By the same logic every other point keeps its cluster. **No point changes membership → centroids will not update further → the algorithm has converged.**

**(d) Final clusters.** *[1 mark]*

- Cluster 1 = $\{P_1, P_2, P_3\}$, centroid $(4/3,\; 4/3) \approx (1.333, 1.333)$.
- Cluster 2 = $\{P_4, P_5, P_6\}$, centroid $(25/3,\; 25/3) \approx (8.333, 8.333)$.

> *Marker note.* In (a), squared distances suffice — students who use $\sqrt{}$ at every step waste time and risk arithmetic slips. Full credit either way. In (c), the convergence justification (no membership change ⇒ centroids stable ⇒ done) is the key concept.

---

# SECTION C — Large Multi-Part Numerical (2 × 25 = 50 marks)

---

## Solution C1 [Topic-Sensitive PR + Spam Mass — 25 marks]

**(a) Build $M$.** *[4 marks]*

Out-degrees: $d_1 = 2$ (to 2, 3), $d_2 = 1$ (to 3), $d_3 = 1$ (to 1), $d_4 = 2$ (to 1, 5), $d_5 = 1$ (to 4).

|         | from 1 | from 2 | from 3 | from 4 | from 5 |
|---------|--------|--------|--------|--------|--------|
| row 1   | 0      | 0      | 1      | 1/2    | 0      |
| row 2   | 1/2    | 0      | 0      | 0      | 0      |
| row 3   | 1/2    | 1      | 0      | 0      | 0      |
| row 4   | 0      | 0      | 0      | 0      | 1      |
| row 5   | 0      | 0      | 0      | 1/2    | 0      |

**Column sums:** $1, 1, 1, 1, 1$ ✓. No dead-ends.

**(b) Two iterations of Topic-PR.** *[8 marks — 4 per iteration]*

$v_S = (1, 0, 0, 0, 0)^\top$ since $|S| = |\{1\}| = 1$. $\beta = 0.85$, $1 - \beta = 0.15$.

**Iteration 1.** $r^{(0)} = (0.20, 0.20, 0.20, 0.20, 0.20)^\top$.

$M r^{(0)}$ row-by-row:
- row 1: $1 \cdot r_3 + 0.5 \cdot r_4 = 0.20 + 0.10 = 0.300$
- row 2: $0.5 \cdot r_1 = 0.100$
- row 3: $0.5 \cdot r_1 + 1 \cdot r_2 = 0.100 + 0.200 = 0.300$
- row 4: $1 \cdot r_5 = 0.200$
- row 5: $0.5 \cdot r_4 = 0.100$

Sum = $0.300 + 0.100 + 0.300 + 0.200 + 0.100 = 1.000$ ✓ (column-stochastic, no leak).

$\beta M r^{(0)} = 0.85 \cdot (0.300, 0.100, 0.300, 0.200, 0.100) = (0.255,\; 0.085,\; 0.255,\; 0.170,\; 0.085)$.

Add $(1-\beta) v_S = (0.150, 0, 0, 0, 0)$:

$$ r^{(1)} = (0.405,\; 0.085,\; 0.255,\; 0.170,\; 0.085) $$

Sum = $0.405 + 0.085 + 0.255 + 0.170 + 0.085 = 1.000$ ✓.

**Iteration 2.** $r^{(1)} = (0.405, 0.085, 0.255, 0.170, 0.085)$.

$M r^{(1)}$:
- row 1: $r_3 + 0.5 r_4 = 0.255 + 0.085 = 0.340$
- row 2: $0.5 \cdot r_1 = 0.5 \cdot 0.405 = 0.2025$
- row 3: $0.5 \cdot r_1 + r_2 = 0.2025 + 0.085 = 0.2875$
- row 4: $r_5 = 0.085$
- row 5: $0.5 \cdot r_4 = 0.5 \cdot 0.170 = 0.085$

Sum = $0.340 + 0.2025 + 0.2875 + 0.085 + 0.085 = 1.000$ ✓.

$\beta M r^{(1)} = 0.85 \cdot (0.340, 0.2025, 0.2875, 0.085, 0.085) = (0.289,\; 0.172,\; 0.244,\; 0.072,\; 0.072)$.

Add $(0.150, 0, 0, 0, 0)$:

$$ r^{(2)} = (0.439,\; 0.172,\; 0.244,\; 0.072,\; 0.072) $$

Sum $\approx 1.000$ ✓ (small rounding error in the last decimal).

**(c) Compare to vanilla PageRank.** *[4 marks]*

For vanilla PR, $v = (0.2, 0.2, 0.2, 0.2, 0.2)$ (uniform teleport). Reusing $M r^{(0)}$ from above:

$$ r^{(1)}_{\text{vanilla}} = 0.85 \cdot (0.300, 0.100, 0.300, 0.200, 0.100) + 0.15 \cdot (0.2, 0.2, 0.2, 0.2, 0.2) $$
$$ = (0.255, 0.085, 0.255, 0.170, 0.085) + (0.030, 0.030, 0.030, 0.030, 0.030) $$
$$ = (0.285,\; 0.115,\; 0.285,\; 0.200,\; 0.115) $$

**Comparison after 1 iteration:**

| Node | Topic-PR | Vanilla PR | Δ (topic − vanilla) |
|------|----------|------------|---------------------|
| 1    | 0.405    | 0.285      | **+0.120**          |
| 2    | 0.085    | 0.115      | −0.030              |
| 3    | 0.255    | 0.285      | −0.030              |
| 4    | 0.170    | 0.200      | −0.030              |
| 5    | 0.085    | 0.115      | −0.030              |

**Node 1 gains all of the teleport mass** (the entire $(1-\beta) = 0.15$ instead of $0.15/5 = 0.03$), while every other node loses its $0.03$ share. After several more iterations the teleport-into-1 mass also propagates to nodes 1's neighbours (here: 2 and 3) more than to the disconnected component $\{4, 5\}$. The final stationary distribution will be heavily concentrated on $\{1, 2, 3\}$.

**(d) Spam Mass.** *[5 marks]*

Apply $\mathrm{SM}(p) = (r_p - r^+_p)/r_p$ to each node:

| Node | $r$    | $r^+$  | $r - r^+$ | $\mathrm{SM} = (r-r^+)/r$    |
|------|--------|--------|-----------|------------------------------|
| 1    | 0.30   | 0.40   | $-0.10$   | $-0.10/0.30 \approx -0.333$  |
| 2    | 0.20   | 0.15   | $+0.05$   | $0.05/0.20 = 0.250$          |
| 3    | 0.25   | 0.25   | $0$       | $0/0.25 = 0.000$             |
| 4    | 0.15   | 0.10   | $+0.05$   | $0.05/0.15 \approx 0.333$    |
| 5    | 0.10   | 0.05   | $+0.05$   | $0.05/0.10 = 0.500$          |

**Spam threshold $\mathrm{SM} \ge 0.4$ flags only node 5** ($\mathrm{SM} = 0.50$). Nodes 1, 2, 3, 4 are below threshold and considered legitimate.

*Note on node 1's negative SM:* node 1 receives *more* TrustRank than vanilla PR — that means trusted seeds disproportionately reach node 1, making it strongly trusted. The negative number is a feature, not a bug.

**(e) Effect of lowering $\beta$.** *[4 marks — 1 each]*

Going $\beta = 0.85 \to 0.50$ shifts the random surfer's behaviour from "follow links 85% of the time" to "follow links 50% / teleport 50%." Effects:

1. **Rank of node 1 *increases* further.** With $|S| = 1$ at node 1, lowering $\beta$ raises the teleport coefficient $(1-\beta)$ from $0.15$ to $0.50$ — node 1 now gets $+0.50$ injected per iteration directly. Topic-PR concentrates *more* mass at the seed when $\beta$ shrinks.
2. **Rank of nodes far from node 1 (e.g. 4, 5) *decreases*.** They receive contributions only via link-following from node 1's neighbourhood, which is dampened by $\beta$. Lower $\beta$ means less rank propagates outward, so distant nodes lose mass.
3. **Convergence speeds up.** The iteration is a contraction with rate $\beta$; smaller $\beta$ ⇒ faster convergence (the spectral gap is $1 - \beta$). At $\beta = 0.5$, errors halve every step.
4. **Spam-farm robustness *increases*.** The spam-farm multiplier $1/(1 - \beta^2)$ shrinks: at $\beta = 0.85$ it is $\approx 3.6$, at $\beta = 0.5$ it is $\approx 1.33$. Spammers can no longer boost their target as much.

> *Marker note.* In (b), give 4 marks per iteration: 1 for the $Mr$ row-by-row, 1 for the $\beta M r$ multiplication, 1 for the teleport addition, 1 for the sum-check. In (e), award 1 mark for each of the four sub-bullets; correct direction (up/down/faster) is enough — exact magnitudes not required.

---

## Solution C2 [Community Detection — 25 marks]

**(a) Brandes BFS from source 1.** *[8 marks]*

**BFS levels and shortest-path counts $\sigma$:**

| Level | Node | $\sigma$ | Predecessor(s) in BFS DAG |
|-------|------|----------|---------------------------|
| 0     | 1    | 1        | (root)                    |
| 1     | 2    | 1        | 1                         |
| 1     | 3    | 1        | 1                         |
| 2     | 4    | 1        | 3                         |
| 3     | 5    | 1        | 4                         |
| 3     | 6    | 1        | 4                         |

DAG edges (direction = "downward in level"): $1{\to}2,\; 1{\to}3,\; 3{\to}4,\; 4{\to}5,\; 4{\to}6$. Edges $2\text{-}3$ and $5\text{-}6$ are intra-level → **not in the DAG**, so they receive **0** credit from this source.

**Brandes credit propagation (bottom-up).** Each node starts with self-credit 1; each DAG edge from child $c$ to parent $p$ receives $\text{credit}(c) \cdot \sigma(p)/\sigma(c)$, then $p$ accumulates that flow.

| Step      | Node $c$ (level) | $\text{credit}(c)$ | DAG edge to parent | Edge contribution                       |
|-----------|------------------|--------------------|----------------------|------------------------------------------|
| 1         | 5 (L3)           | 1                  | 4–5                  | $1 \cdot \sigma(4)/\sigma(5) = 1$        |
| 2         | 6 (L3)           | 1                  | 4–6                  | $1 \cdot \sigma(4)/\sigma(6) = 1$        |
| 3         | 4 (L2)           | $1 + 1 + 1 = 3$    | 3–4                  | $3 \cdot \sigma(3)/\sigma(4) = 3$        |
| 4         | 2 (L1)           | $1 + 0 = 1$        | 1–2                  | $1 \cdot \sigma(1)/\sigma(2) = 1$        |
| 5         | 3 (L1)           | $1 + 3 = 4$        | 1–3                  | $4 \cdot \sigma(1)/\sigma(3) = 4$        |

**Edge-betweenness contributions from source $s = 1$:**

| Edge | Contribution from $s = 1$ |
|------|---------------------------|
| 1–2  | 1                         |
| 1–3  | 4                         |
| 2–3  | 0 (not in DAG)            |
| 3–4  | 3                         |
| 4–5  | 1                         |
| 4–6  | 1                         |
| 5–6  | 0 (not in DAG)            |

(The total betweenness summed across all sources, divided by 2, gives the global table provided in part (b): the bridge edge 3–4 wins with $b = 9$.)

**(b) Remove highest-betweenness edge and recompute.** *[5 marks]*

From the supplied table, the highest is **edge 3–4 with $b = 9$**. Removing it disconnects the graph into two components:

- Component 1: triangle on $\{1, 2, 3\}$ with edges $\{1\text{-}2, 1\text{-}3, 2\text{-}3\}$.
- Component 2: triangle on $\{4, 5, 6\}$ with edges $\{4\text{-}5, 4\text{-}6, 5\text{-}6\}$.

**Recompute betweenness within each component.** In a triangle, every pair of nodes is joined by a direct edge of length 1; there are also length-2 alternate paths through the third node, but they are not shortest. So each of the three pairs contributes 1 to its corresponding direct edge:

| Edge (in remaining graph) | $b(e)$ on the post-cut graph |
|---------------------------|------------------------------|
| 1–2                       | 1                            |
| 1–3                       | 1                            |
| 2–3                       | 1                            |
| 4–5                       | 1                            |
| 4–6                       | 1                            |
| 5–6                       | 1                            |

All six remaining edges are tied at $b = 1$. (The single bridge has done all the heavy lifting; once it is gone, no edge stands out.)

**(c) Modularity.** *[8 marks]*

Compute on the **original** graph (before any cut). $m = 7$ edges, so $2m = 14$.

**Step 1 — degrees.** *[2 marks]*

| Node | Neighbours      | $k_i$ |
|------|-----------------|-------|
| 1    | 2, 3            | 2     |
| 2    | 1, 3            | 2     |
| 3    | 1, 2, 4         | 3     |
| 4    | 3, 5, 6         | 3     |
| 5    | 4, 6            | 2     |
| 6    | 4, 5            | 2     |

Check: $\sum_i k_i = 2 + 2 + 3 + 3 + 2 + 2 = 14 = 2m$ ✓.

**Step 2 — community statistics for $C_1 = \{1,2,3\}$ and $C_2 = \{4,5,6\}$.** *[3 marks]*

Internal edges of $C_1$: edges with both endpoints in $\{1, 2, 3\}$ = $\{1\text{-}2,\; 1\text{-}3,\; 2\text{-}3\}$ → $L_1 = 3$.
Sum of degrees: $D_1 = k_1 + k_2 + k_3 = 2 + 2 + 3 = 7$.

Internal edges of $C_2$: edges with both endpoints in $\{4, 5, 6\}$ = $\{4\text{-}5,\; 4\text{-}6,\; 5\text{-}6\}$ → $L_2 = 3$.
$D_2 = k_4 + k_5 + k_6 = 3 + 2 + 2 = 7$.

(The bridge edge 3–4 has one endpoint in $C_1$ and one in $C_2$ — it is *not* internal to either community, so it does **not** count toward $L_1$ or $L_2$.)

**Step 3 — apply the block formula.** *[3 marks]*

$$ Q = \sum_{c \in \{C_1, C_2\}} \left[ \frac{L_c}{m} - \left( \frac{D_c}{2m} \right)^2 \right] $$

$$ Q = \left[ \frac{3}{7} - \left( \frac{7}{14} \right)^2 \right] + \left[ \frac{3}{7} - \left( \frac{7}{14} \right)^2 \right] = 2 \cdot \left[ \frac{3}{7} - \frac{1}{4} \right] $$

$$ = 2 \cdot \left[ \frac{12}{28} - \frac{7}{28} \right] = 2 \cdot \frac{5}{28} = \frac{10}{28} = \frac{5}{14} \approx 0.357 $$

**$Q \approx 0.36$** — strong community structure (typical "good" partitions score $0.3$–$0.7$).

**(d) Laplacian and the Fiedler vector.** *[4 marks]*

Degree matrix $D = \mathrm{diag}(2, 2, 3, 3, 2, 2)$. Adjacency:

$$ A = \begin{pmatrix} 0 & 1 & 1 & 0 & 0 & 0 \\ 1 & 0 & 1 & 0 & 0 & 0 \\ 1 & 1 & 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 & 1 & 1 \\ 0 & 0 & 0 & 1 & 0 & 1 \\ 0 & 0 & 0 & 1 & 1 & 0 \end{pmatrix} $$

**Laplacian** $L = D - A$:

$$ L = \begin{pmatrix} 2 & -1 & -1 & 0 & 0 & 0 \\ -1 & 2 & -1 & 0 & 0 & 0 \\ -1 & -1 & 3 & -1 & 0 & 0 \\ 0 & 0 & -1 & 3 & -1 & -1 \\ 0 & 0 & 0 & -1 & 2 & -1 \\ 0 & 0 & 0 & -1 & -1 & 2 \end{pmatrix} $$

Verify rows sum to 0: row 3: $-1 - 1 + 3 - 1 = 0$ ✓; row 4: $-1 + 3 - 1 - 1 = 0$ ✓; etc.

**Why $\mathbf{1}_6$ is always an eigenvector.** Each row of $L$ sums to zero by construction ($L_{ii} = k_i$ on the diagonal; $L_{ij} = -1$ for each of the $k_i$ neighbours of $i$). Hence $L \cdot \mathbf{1}_6 = \mathbf{0}$, i.e. $\mathbf{1}_6$ is an eigenvector with **eigenvalue $\lambda_1 = 0$**. (This is the trivial "everything in one cluster" mode.)

**Fiedler vector and how it would partition this graph.** The **Fiedler vector** $v_2$ is the eigenvector associated with the second-smallest eigenvalue $\lambda_2 > 0$. Sign-thresholding the entries of $v_2$ gives a 2-way cut: positive entries form one community, negative entries the other. For this barbell graph, $v_2$ would have:

- **Positive entries on $\{1, 2, 3\}$** (one triangle),
- **Negative entries on $\{4, 5, 6\}$** (the other triangle),
- entries closer to zero at the bridge endpoints (nodes 3 and 4) — they sit on the boundary.

This recovers exactly the same partition that Girvan-Newman gives by removing edge 3–4.

> *Marker note.* In (a), award 4 marks for correct BFS levels and $\sigma$ values, and 4 marks for the credit propagation table. In (c), heavily reward the $\sum k_i = 2m$ check — students who skip it often plug $D_c$ into the wrong place. In (d), do *not* deduct marks for not actually computing $\lambda_2$; the question only requires writing $L$ and explaining the Fiedler partition qualitatively.

---

# Final Self-Assessment Table

After grading yourself against these solutions, fill in the table below to direct your revision:

| Question | Marks earned | Marks possible | Topic | Action if < 80% |
|----------|--------------|----------------|-------|-----------------|
| A1       |              | 5              | Bonferroni | Re-read W01 §3 + WE 1 |
| A2       |              | 5              | Apriori | Re-read W02-03 §5 + WE 2 |
| A3       |              | 5              | MinHash | Re-read W04-05 §6 trace |
| A4       |              | 5              | Cosine | Re-read W07 §5 |
| B1       |              | 10             | User-User CF | Re-read W07 WE 2 |
| B2       |              | 10             | PageRank dead-end | Re-read W08-09 §9 + WE 7 |
| B3       |              | 10             | k-Means | Re-read W13-14 §3 |
| C1       |              | 25             | Topic-PR + Spam Mass | Re-read W12 §3, §6, §7 |
| C2       |              | 25             | GN + Spectral | Re-read W16 §3, §4, §5, §7 |
| **Total**|              | **100**        |       |                  |

> **Aim for 65/100.** If you scored below 50, focus the next study session on the lowest-scoring section. If you scored 65+ on the first attempt, move on to Mock Paper 2 (different datasets, same difficulty) and then to past-paper drills.

---

*End of Mock Paper 1 — Worked Solutions.*
