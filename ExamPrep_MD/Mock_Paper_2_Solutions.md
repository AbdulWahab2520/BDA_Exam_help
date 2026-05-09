---
title: "BDA Final — Mock Paper 2 · Solutions"
subtitle: "Full step-by-step worked solutions · 100 marks"
author: "BDA Final Exam Prep · Comprehensive Tutor"
course: "CS-404 Big Data Analytics — Dr. Syed Imran Ali"
exam: "Final ~ 2026-05-16"
---

# Mock Paper 2 — Worked Solutions

> Each marking point is shown in **[brackets]** so you can self-grade.

---

## Section A — Short Numerical (20 marks)

### A1. PCY Hash Buckets — Solution (5 marks)

**(a) Hashing each pair** with $h(i,j) = (i \cdot j) \bmod 11$:

| Pair  | $i \cdot j$ | $h(i,j) = i\cdot j \bmod 11$ | Count |
|-------|-------------|------------------------------|-------|
| {1,4} | 4           | **4**                        | 5     |
| {2,3} | 6           | **6**                        | 4     |
| {2,5} | 10          | **10**                       | 6     |
| {3,5} | 15          | **4**                        | 3     |
| {1,6} | 6           | **6**                        | 4     |
| {4,5} | 20          | **9**                        | 7     |
| {3,4} | 12          | **1**                        | 5     |
| {2,4} | 8           | **8**                        | 2     |

Now sum counts per bucket: **[2 marks]**

| Bucket | Pairs in bucket | **Total count** |
|:------:|------------------|:--------------:|
| B0     | —                | 0              |
| B1     | {3,4}            | 5              |
| B2     | —                | 0              |
| B3     | —                | 0              |
| **B4** | {1,4}, {3,5}     | **5 + 3 = 8**  |
| B5     | —                | 0              |
| **B6** | {2,3}, {1,6}     | **4 + 4 = 8**  |
| B7     | —                | 0              |
| B8     | {2,4}            | 2              |
| **B9** | {4,5}            | **7**          |
| B10    | {2,5}            | 6              |

**[1 mark for correct totals]**

**(b)** Frequent buckets (count ≥ 7): **B4, B6, B9**. **[1 mark]**

**(c)** Pair {3,5} hashes to bucket B4 which is **frequent**. PCY does mark {3,5} as a **candidate** for Pass 2 — *however* the pair only needs to **survive** Pass 2 if its actual support reaches the support threshold. Being in a frequent bucket is **necessary but not sufficient**: a frequent bucket can be inflated by other pairs (here {1,4} alone contributed 5/8 of the count). **[1 mark]**

---

### A2. LSH S-curve Probability — Solution (5 marks)

**(a)** Standard LSH banding probability:
$$
\Pr[\text{candidate}] \;=\; 1 - \big(1 - s^{r}\big)^{b}.
$$
**[1 mark]**

**(b)** With $s = 0.6$, $r = 5$, $b = 20$:

- $s^{r} = 0.6^{5} = 0.07776$ **[1 mark]**
- $1 - s^{r} = 0.92224$ **[½ mark]**
- $(1 - s^{r})^{b} = 0.92224^{20}$.
  Taking logs: $\ln(0.92224) = -0.080927 \Rightarrow 20 \cdot (-0.080927) = -1.61855$
  $\Rightarrow 0.92224^{20} = e^{-1.61855} \approx 0.19821$ **[1½ marks]**
- $\Pr = 1 - 0.19821 = \mathbf{0.802}$ (≈ 80.2 %) **[1 mark]**

---

### A3. Recommender Baseline Prediction — Solution (5 marks)

**(a)** $\hat r_{xi} = \mu + b_x + b_i$. **[1 mark]**

**(b)** $\hat r_{xi} = 3.5 + 0.4 + (-0.2) = \mathbf{3.7}$. **[2 marks]**

**(c)** New prediction with $b_j = +0.5$:
$$\hat r_{xj} = 3.5 + 0.4 + 0.5 = 4.4.$$
Change = $4.4 - 3.7 = \mathbf{+0.7}$. **[2 marks]**

(Or: change in item bias alone = $b_j - b_i = 0.5 - (-0.2) = 0.7$.)

---

### A4. Spider Trap vs Dead-End — Solution (5 marks)

- **G1:** $A \leftrightarrow B$, $C \to A$. The set $\{A, B\}$ is a **spider trap** — once the random surfer enters $A$ or $B$ they bounce only between the two; node $C$ has no in-link from $\{A,B\}$, so probability mass leaks **into** the trap and never out. **[2 marks]**

- **G2:** $C$ has out-degree 0 → **dead-end**. PageRank mass leaks out of the system entirely (must be patched by teleport / dead-end removal). **[2 marks]**

- **G3:** $A \to B \to C \to A$ — strongly connected, every node has an out-edge. **Neither** spider trap nor dead-end. **[1 mark]**

---

## Section B — Medium Numerical (30 marks)

### B1. MinHash + LSH — Solution (10 marks)

**(a) Hash table for $x = 1..4$** **[2 marks]**

| $x$ | $h_1 = (x{+}1)\bmod 5$ | $h_2 = (3x{+}1)\bmod 5$ | $h_3 = (2x{+}3)\bmod 5$ | $h_4 = (4x{+}1)\bmod 5$ |
|:---:|:----------------------:|:-----------------------:|:-----------------------:|:-----------------------:|
| 1   | 2                      | 4                       | 0                       | 0                       |
| 2   | 3                      | 2                       | 2                       | 4                       |
| 3   | 4                      | 0                       | 4                       | 3                       |
| 4   | 0                      | 3                       | 1                       | 2                       |

**(b) MinHash signatures.** Take the **min over rows where doc = 1**. **[3 marks]**

- $D_1$ has 1's in $\{r_1, r_2\}$:
  - $h_1: \min(2, 3) = 2$
  - $h_2: \min(4, 2) = 2$
  - $h_3: \min(0, 2) = 0$
  - $h_4: \min(0, 4) = 0$

- $D_2$ has 1's in $\{r_2, r_3, r_4\}$:
  - $h_1: \min(3, 4, 0) = 0$
  - $h_2: \min(2, 0, 3) = 0$
  - $h_3: \min(2, 4, 1) = 1$
  - $h_4: \min(4, 3, 2) = 2$

- $D_3$ has 1's in $\{r_1, r_3, r_4\}$:
  - $h_1: \min(2, 4, 0) = 0$
  - $h_2: \min(4, 0, 3) = 0$
  - $h_3: \min(0, 4, 1) = 0$
  - $h_4: \min(0, 3, 2) = 0$

**Signature matrix $\mathrm{SIG}$:**

|       | $D_1$ | $D_2$ | $D_3$ |
|-------|:-----:|:-----:|:-----:|
| $h_1$ | 2     | 0     | 0     |
| $h_2$ | 2     | 0     | 0     |
| $h_3$ | 0     | 1     | 0     |
| $h_4$ | 0     | 2     | 0     |

**(c) LSH banding ($b = 2$, $r = 2$).** **[5 marks]**

- **Band 1** (rows $h_1, h_2$):
  - $D_1 \to (2, 2)$
  - $D_2 \to (0, 0)$
  - $D_3 \to (0, 0)$
  - $D_2$ and $D_3$ collide → candidate pair $(D_2, D_3)$.

- **Band 2** (rows $h_3, h_4$):
  - $D_1 \to (0, 0)$
  - $D_2 \to (1, 2)$
  - $D_3 \to (0, 0)$
  - $D_1$ and $D_3$ collide → candidate pair $(D_1, D_3)$.

**Candidate pairs after LSH:** $\{(D_1, D_3),\; (D_2, D_3)\}$.

> *Sanity check:* True Jaccard similarities are $J(D_1,D_2) = 1/4$, $J(D_1,D_3) = 1/4$, $J(D_2,D_3) = 2/4 = 0.5$. The high-Jaccard pair $(D_2,D_3)$ is correctly flagged; $(D_1, D_3)$ is a (tolerable) false-positive at this small signature length.

---

### B2. Spam Farm — Solution (10 marks)

**Constants.**
- $\beta = 0.85 \Rightarrow \beta^{2} = 0.7225 \Rightarrow 1 - \beta^{2} = 0.2775$
- $\dfrac{\beta}{1+\beta} = \dfrac{0.85}{1.85} = 0.45946$

**(a)** With $M = 10^{5}$, $N = 10^{9}$, $x = 10^{-4}$: **[5 marks]**

Term 1: $\dfrac{x}{1 - \beta^{2}} = \dfrac{10^{-4}}{0.2775} = 3.6036 \times 10^{-4}$ **[2 marks]**

Term 2: $\dfrac{\beta}{1+\beta} \cdot \dfrac{M}{N} = 0.45946 \cdot \dfrac{10^{5}}{10^{9}} = 0.45946 \cdot 10^{-4} = 4.5946 \times 10^{-5}$ **[2 marks]**

$$
y \;=\; 3.6036 \times 10^{-4} \;+\; 4.5946 \times 10^{-5} \;\approx\; \mathbf{4.063 \times 10^{-4}}.
$$
**[1 mark]**

**(b)** Set $y^{\star} = 10^{-3}$ and solve for $M$: **[5 marks]**

$$
10^{-3} \;=\; 3.6036 \times 10^{-4} \;+\; 0.45946 \cdot \frac{M}{10^{9}}.
$$

$$
0.45946 \cdot \frac{M}{10^{9}} \;=\; 10^{-3} - 3.6036 \times 10^{-4} \;=\; 6.3964 \times 10^{-4}.
$$
**[2 marks]**

$$
\frac{M}{10^{9}} \;=\; \frac{6.3964 \times 10^{-4}}{0.45946} \;=\; 1.3922 \times 10^{-3}.
$$
**[2 marks]**

$$
\boxed{\,M \;\approx\; 1.39 \times 10^{6}\, \text{ farm pages.}\,}
$$
**[1 mark]**

> Roughly **14× more farm pages** than the original $10^{5}$ to multiply the target rank by ~2.5.

---

### B3. BFR — Solution (10 marks)

**(a) Centroid.** **[2 marks]**

$$
\boldsymbol c \;=\; \frac{\mathrm{SUM}}{N} \;=\; \left(\frac{20}{5},\; \frac{15}{5}\right) \;=\; (4,\; 3).
$$

**(b) Variances and standard deviations.** **[3 marks]**

$$
\sigma_x^{2} \;=\; \frac{\mathrm{SUMSQ}_x}{N} - \left(\frac{\mathrm{SUM}_x}{N}\right)^{2} \;=\; \frac{90}{5} - 4^{2} \;=\; 18 - 16 \;=\; 2.
$$

$$
\sigma_y^{2} \;=\; \frac{50}{5} - 3^{2} \;=\; 10 - 9 \;=\; 1.
$$

$$
\sigma_x \;=\; \sqrt{2} \;\approx\; 1.414, \qquad \sigma_y \;=\; 1.
$$

**(c) Mahalanobis distance** for $P = (6, 5)$. **[3 marks]**

$$
d^{2}(P,\boldsymbol c)
\;=\; \left(\frac{6 - 4}{\sqrt{2}}\right)^{2} + \left(\frac{5 - 3}{1}\right)^{2}
\;=\; \frac{4}{2} + 4
\;=\; 2 + 4 \;=\; 6.
$$

$$
d(P,\boldsymbol c) \;=\; \sqrt{6} \;\approx\; \mathbf{2.449}.
$$

**(d) Decision.** Threshold = 3. Since $d \approx 2.449 < 3$, point $P$ **joins the DS** cluster. **[2 marks]**

> The DS summary then updates to $N{=}6$, $\mathrm{SUM}{=}(26, 20)$, $\mathrm{SUMSQ}{=}(126, 75)$.

---

## Section C — Large Multi-Part Numerical (50 marks)

### C1. Hierarchical Clustering + CURE — Solution (25 marks)

**Recap of points:**

| | $P_1$ | $P_2$ | $P_3$ | $P_4$ | $P_5$ | $P_6$ | $P_7$ |
|---|---|---|---|---|---|---|---|
|   | (1,1) | (1.5,1.5) | (5,5) | (3,4) | (4,4) | (10,10) | (9,9.5) |

#### (a) Initial 7 × 7 distance matrix (upper triangle) — 5 marks

Using $d(p,q) = \sqrt{(p_x-q_x)^{2}+(p_y-q_y)^{2}}$:

|        | $P_1$ | $P_2$    | $P_3$    | $P_4$    | $P_5$    | $P_6$     | $P_7$     |
|--------|:-----:|:--------:|:--------:|:--------:|:--------:|:---------:|:---------:|
| $P_1$  | 0     | **0.707**| 5.657    | 3.606    | 4.243    | 12.728    | 11.673    |
| $P_2$  |       | 0        | 4.950    | 2.915    | 3.536    | 12.021    | 10.966    |
| $P_3$  |       |          | 0        | 2.236    | **1.414**| 7.071     | 6.021     |
| $P_4$  |       |          |          | 0        | **1.000**| 9.220     | 8.139     |
| $P_5$  |       |          |          |          | 0        | 8.485     | 7.433     |
| $P_6$  |       |          |          |          |          | 0         | **1.118** |
| $P_7$  |       |          |          |          |          |           | 0         |

**Sample working** (for full marks show 2–3 of these explicitly):

- $d(P_1,P_2) = \sqrt{0.5^2+0.5^2} = \sqrt{0.5} \approx 0.707$
- $d(P_3,P_5) = \sqrt{1+1} = \sqrt{2} \approx 1.414$
- $d(P_4,P_5) = \sqrt{1+0} = 1.000$
- $d(P_6,P_7) = \sqrt{1+0.25} = \sqrt{1.25} \approx 1.118$

**[5 marks: 1 per row of explicit working + 1 for full matrix]**

#### (b) Single-linkage agglomerative — first 4 merges — 10 marks

> Single-link: $d(C_a, C_b) = \min_{p \in C_a,\, q \in C_b} d(p, q)$.

**Merge 1.** Minimum entry = $d(P_1, P_2) = 0.707$.
→ Form cluster $X = \{P_1, P_2\}$. **[2 marks]**

Remaining clusters: $X, \{P_3\}, \{P_4\}, \{P_5\}, \{P_6\}, \{P_7\}$.

Updated single-link distances from $X$ to singletons (min of two old rows):
$d(X, P_3) = \min(5.657, 4.950) = 4.950$,
$d(X, P_4) = \min(3.606, 2.915) = 2.915$,
$d(X, P_5) = \min(4.243, 3.536) = 3.536$,
$d(X, P_6) = \min(12.728, 12.021) = 12.021$,
$d(X, P_7) = \min(11.673, 10.966) = 10.966$.

Other distances are unchanged.

**Merge 2.** Smallest remaining entry = $d(P_4, P_5) = 1.000$.
→ Form cluster $A = \{P_4, P_5\}$. **[2 marks]**

Update distances from $A$ to others:
$d(A, X) = \min(2.915, 3.536) = 2.915$,
$d(A, P_3) = \min(2.236, 1.414) = 1.414$,
$d(A, P_6) = \min(9.220, 8.485) = 8.485$,
$d(A, P_7) = \min(8.139, 7.433) = 7.433$.

**Merge 3.** Smallest remaining entry = $d(P_6, P_7) = 1.118$.
→ Form cluster $Z = \{P_6, P_7\}$. **[2 marks]**

Update distances from $Z$:
$d(Z, X) = \min(12.021, 10.966) = 10.966$,
$d(Z, A) = \min(8.485, 7.433) = 7.433$,
$d(Z, P_3) = \min(7.071, 6.021) = 6.021$.

**Merge 4.** Current cluster set: $X, A, \{P_3\}, Z$.

Pairwise distances:

| pair    | distance |
|---------|---------:|
| $X$–$A$ | 2.915    |
| $X$–$P_3$ | 4.950  |
| $X$–$Z$ | 10.966   |
| **$A$–$P_3$** | **1.414** |
| $A$–$Z$ | 7.433    |
| $P_3$–$Z$ | 6.021  |

Minimum = $d(A, P_3) = 1.414$. → Merge $\{P_3\}$ into $A$, giving cluster $B = \{P_3, P_4, P_5\}$. **[2 marks]**

**Cluster set after merge 4 (3 clusters):**
$$
X = \{P_1, P_2\}, \quad B = \{P_3, P_4, P_5\}, \quad Z = \{P_6, P_7\}.
$$
**[2 marks]**

#### (c) CURE Phase 1 — 7 marks

**Cluster $X = \{P_1, P_2\}$.**
- Centroid $\boldsymbol c_X = (1.25, 1.25)$.
- Distance from each point to $\boldsymbol c_X$: both equal $\sqrt{0.0625+0.0625} = \sqrt{0.125} \approx 0.354$. Tie → pick $P_1$ first.
- Second rep = farthest from $\{P_1\}$ = $P_2$ (only other choice, distance 0.707).
- Reps before shrinking: $\{P_1, P_2\}$.
- Shrink with $\alpha = 0.4$ → $r' = 0.6 r + 0.4 \boldsymbol c_X$:
  - $P_1' = 0.6\,(1,1) + 0.4\,(1.25,1.25) = (0.6+0.5,\; 0.6+0.5) = \mathbf{(1.1,\; 1.1)}$.
  - $P_2' = 0.6\,(1.5,1.5) + 0.4\,(1.25,1.25) = (0.9+0.5,\; 0.9+0.5) = \mathbf{(1.4,\; 1.4)}$.

**[2 marks]**

**Cluster $B = \{P_3, P_4, P_5\}$.**
- Centroid $\boldsymbol c_B = \big(\tfrac{5+3+4}{3},\; \tfrac{5+4+4}{3}\big) = (4,\; 4.333)$.
- Distances to centroid:
  - $d(\boldsymbol c_B, P_3) = \sqrt{1 + (5-4.333)^{2}} = \sqrt{1 + 0.444} = \sqrt{1.444} \approx 1.202$
  - $d(\boldsymbol c_B, P_4) = \sqrt{1 + (4-4.333)^{2}} = \sqrt{1.111} \approx 1.054$
  - $d(\boldsymbol c_B, P_5) = \sqrt{0 + 0.111} \approx 0.333$
  - Farthest = $P_3$ → first rep.
- Second rep = farthest from $\{P_3\}$ among the rest:
  - $d(P_3, P_4) = \sqrt{4+1} = \sqrt{5} \approx 2.236$
  - $d(P_3, P_5) = \sqrt{1+1} = \sqrt{2} \approx 1.414$
  - Farthest = $P_4$ → second rep.
- Reps before shrinking: $\{P_3, P_4\}$.
- Shrink:
  - $P_3' = 0.6\,(5,5) + 0.4\,(4, 4.333) = (3 + 1.6,\; 3 + 1.733) = \mathbf{(4.6,\; 4.733)}$.
  - $P_4' = 0.6\,(3,4) + 0.4\,(4, 4.333) = (1.8 + 1.6,\; 2.4 + 1.733) = \mathbf{(3.4,\; 4.133)}$.

**[3 marks]**

**Cluster $Z = \{P_6, P_7\}$.**
- Centroid $\boldsymbol c_Z = (9.5,\; 9.75)$.
- Distance from each point to $\boldsymbol c_Z$ both equal $\sqrt{0.25+0.0625} = \sqrt{0.3125} \approx 0.559$. Tie → pick $P_6$ first, then $P_7$.
- Reps before shrinking: $\{P_6, P_7\}$.
- Shrink:
  - $P_6' = 0.6\,(10,10) + 0.4\,(9.5, 9.75) = (6 + 3.8,\; 6 + 3.9) = \mathbf{(9.8,\; 9.9)}$.
  - $P_7' = 0.6\,(9, 9.5) + 0.4\,(9.5, 9.75) = (5.4 + 3.8,\; 5.7 + 3.9) = \mathbf{(9.2,\; 9.6)}$.

**[2 marks]**

**Summary of all 6 representatives:**

| Cluster | Centroid           | Rep 1 (shrunken)   | Rep 2 (shrunken)   |
|---------|--------------------|--------------------|--------------------|
| $X$     | $(1.25, 1.25)$     | $(1.1, 1.1)$       | $(1.4, 1.4)$       |
| $B$     | $(4, 4.333)$       | $(4.6, 4.733)$     | $(3.4, 4.133)$     |
| $Z$     | $(9.5, 9.75)$      | $(9.8, 9.9)$       | $(9.2, 9.6)$       |

#### (d) CURE Phase 2 — Assigning $Q = (4.5, 4.2)$ — 3 marks

Distances from $Q$ to every shrunken representative:

| Rep | Coords        | Squared diff $(\Delta x^{2} + \Delta y^{2})$         | Distance |
|-----|---------------|------------------------------------------------------|----------|
| $P_1'$ | $(1.1, 1.1)$ | $(3.4)^{2} + (3.1)^{2} = 11.56 + 9.61 = 21.17$        | 4.601    |
| $P_2'$ | $(1.4, 1.4)$ | $(3.1)^{2} + (2.8)^{2} = 9.61 + 7.84 = 17.45$         | 4.177    |
| $P_3'$ | $(4.6, 4.733)$ | $(0.1)^{2} + (0.533)^{2} = 0.01 + 0.284 = 0.294$    | **0.543** |
| $P_4'$ | $(3.4, 4.133)$ | $(1.1)^{2} + (0.067)^{2} = 1.21 + 0.0045 = 1.2145$  | 1.102    |
| $P_6'$ | $(9.8, 9.9)$ | $(5.3)^{2} + (5.7)^{2} = 28.09 + 32.49 = 60.58$       | 7.784    |
| $P_7'$ | $(9.2, 9.6)$ | $(4.7)^{2} + (5.4)^{2} = 22.09 + 29.16 = 51.25$       | 7.159    |

**Nearest rep = $P_3'$** at distance ≈ **0.543**, which belongs to cluster $B$.

→ Assign $Q$ to **cluster $B = \{P_3, P_4, P_5\}$**. **[3 marks]**

---

### C2. Item-Item CF + RMSE — Solution (25 marks)

#### (a) Pearson item similarities — 8 marks

**Item means** (over **only the rated cells** of that column):

| Item | Ratings           | Mean    |
|------|-------------------|---------|
| $M_1$| 5, 4, 3, 5        | 4.25    |
| $M_2$| 3, 4, 2, 3        | 3.00    |
| $M_3$| 5, 4, 3, 4        | 4.00    |
| $M_4$| 4, 4, 3, 5        | 4.00    |

**[2 marks for the means]**

**$\mathrm{sim}(M_1, M_3)$.** Common users (both items rated): $U_2, U_4, U_5$.

Centered ratings (subtract item mean):

| User | $M_1$ — 4.25 | $M_3$ — 4.00 |
|------|-------------:|-------------:|
| $U_2$| $-0.25$      | $+1.00$      |
| $U_4$| $-1.25$      | $-1.00$      |
| $U_5$| $+0.75$      | $\;\;0.00$   |

Dot product: $(-0.25)(1) + (-1.25)(-1) + (0.75)(0) = -0.25 + 1.25 + 0 = 1.000$.

$\|M_1\| = \sqrt{0.0625 + 1.5625 + 0.5625} = \sqrt{2.1875} \approx 1.479$.
$\|M_3\| = \sqrt{1 + 1 + 0} = \sqrt{2} \approx 1.414$.

$$
\mathrm{sim}(M_1, M_3) = \frac{1.000}{1.479 \times 1.414} = \frac{1.000}{2.092} \approx \mathbf{0.478}.
$$

**[3 marks]**

**$\mathrm{sim}(M_2, M_3)$.** Common users: $U_3, U_4, U_5$.

Centered ratings:

| User | $M_2$ — 3.00 | $M_3$ — 4.00 |
|------|-------------:|-------------:|
| $U_3$| $+1.00$      | $\;\;0.00$   |
| $U_4$| $-1.00$      | $-1.00$      |
| $U_5$| $\;\;0.00$   | $\;\;0.00$   |

Dot product: $(1)(0) + (-1)(-1) + (0)(0) = 1.000$.

$\|M_2\| = \sqrt{1 + 1 + 0} = \sqrt{2} \approx 1.414$.
$\|M_3\| = \sqrt{0 + 1 + 0} = 1$.

$$
\mathrm{sim}(M_2, M_3) = \frac{1.000}{1.414 \times 1} \approx \mathbf{0.707}.
$$

**[3 marks]**

#### (b) Predict $\hat r(U_1, M_3)$ — 8 marks

Items $U_1$ has rated: $M_1, M_2, M_4$. Need similarities to $M_3$ for all three.

We already have $\mathrm{sim}(M_1,M_3) = 0.478$, $\mathrm{sim}(M_2,M_3) = 0.707$.

**$\mathrm{sim}(M_4, M_3)$.** Common users: $U_2, U_3, U_5$.

Centered ratings:

| User | $M_4$ — 4.00 | $M_3$ — 4.00 |
|------|-------------:|-------------:|
| $U_2$| $\;\;0.00$   | $+1.00$      |
| $U_3$| $-1.00$      | $\;\;0.00$   |
| $U_5$| $+1.00$      | $\;\;0.00$   |

Dot product = $0 + 0 + 0 = 0$.

$$
\mathrm{sim}(M_4, M_3) = 0.
$$
**[2 marks]**

**Pick top-$k$ neighbours.** $k = 2$, sort by absolute similarity:

| Item | $|\mathrm{sim}(\cdot, M_3)|$ | Rank |
|------|-----------------------------:|------|
| $M_2$| 0.707                        | 1    |
| $M_1$| 0.478                        | 2    |
| $M_4$| 0.000                        | 3 (drop) |

Neighbour set $N_k = \{M_1, M_2\}$. **[1 mark]**

**Apply weighted-average:**

$$
\hat r(U_1, M_3) \;=\; \frac{0.707 \cdot r(U_1, M_2) + 0.478 \cdot r(U_1, M_1)}{0.707 + 0.478}.
$$

Plug in $r(U_1, M_1) = 5$, $r(U_1, M_2) = 3$:

$$
\hat r(U_1, M_3) \;=\; \frac{0.707 \cdot 3 + 0.478 \cdot 5}{1.185}
\;=\; \frac{2.121 + 2.390}{1.185}
\;=\; \frac{4.511}{1.185}
\;\approx\; \mathbf{3.806}.
$$
**[5 marks: 2 formula + 3 numeric]**

> Sanity: $U_1$ tends to rate high (5 and 4 elsewhere); 3.81 is plausibly "moderate-positive".

#### (c) RMSE — 5 marks

| #  | Predicted | Actual | Error $\hat r - r$ | Squared |
|----|----------:|-------:|-------------------:|--------:|
| 1  | 4         | 5      | $-1$               | 1       |
| 2  | 3         | 4      | $-1$               | 1       |
| 3  | 5         | 4      | $+1$               | 1       |
| 4  | 3         | 4      | $-1$               | 1       |
| 5  | 5         | 5      | $\;\;0$            | 0       |

Sum of squared errors = $1+1+1+1+0 = 4$.
Mean squared error = $4 / 5 = 0.8$.
$$
\mathrm{RMSE} = \sqrt{0.8} \;\approx\; \mathbf{0.894}.
$$
**[5 marks: 2 errors + 1 sum + 1 mean + 1 sqrt]**

#### (d) Why Item-Item CF often beats User-User CF — 4 marks

A solid 3–4 sentence answer should hit:

1. **Stability of profiles.** An item's "personality" (which users like it) changes much more slowly than a user's tastes. Pre-computed item-item similarities therefore stay valid for days/weeks, while user-user similarities drift fast. **[1 mark]**
2. **Cardinality.** In production, $|\text{users}| \gg |\text{items}|$ (e.g. Netflix: hundreds of millions of users vs ~$10^{4}$–$10^{5}$ titles). The $|I| \times |I|$ similarity matrix is feasible to store (millions of entries) where the $|U| \times |U|$ matrix is not (quadrillions). **[1 mark]**
3. **Offline pre-computation.** Item-item similarities can be computed **once** offline and reused for many users; serving a prediction is a small weighted sum over the rated items. User-user requires recomputation as users' rating vectors evolve. **[1 mark]**
4. **Practical accuracy.** Items typically have many more ratings than any single user, giving denser, less-noisy similarity estimates. Empirical evaluations (Sarwar et al. 2001, Linden et al. Amazon 2003) show item-item ≥ user-user in MAE/RMSE. **[1 mark]**

---

## Mark Summary

| Section | Question | Marks |
|---------|----------|------:|
| A       | A1       | 5     |
| A       | A2       | 5     |
| A       | A3       | 5     |
| A       | A4       | 5     |
| **A subtotal** |   | **20** |
| B       | B1       | 10    |
| B       | B2       | 10    |
| B       | B3       | 10    |
| **B subtotal** |   | **30** |
| C       | C1       | 25    |
| C       | C2       | 25    |
| **C subtotal** |   | **50** |
| **Grand Total** |   | **100** |

*— End of Mock Paper 2 Solutions —*
