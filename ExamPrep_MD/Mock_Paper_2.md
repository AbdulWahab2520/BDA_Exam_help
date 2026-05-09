---
title: "BDA Final — Mock Paper 2"
subtitle: "3-hour final exam · 100 marks · Closed book · Calculator allowed"
author: "BDA Final Exam Prep · Comprehensive Tutor"
course: "CS-404 Big Data Analytics — Dr. Syed Imran Ali"
exam: "Final ~ 2026-05-16"
---

# BDA Final — Mock Paper 2

> **Time:** 3 hours · **Total marks:** 100 · **Pass target:** ≥ 65/100
> **Instructions:**
> 1. Answer **ALL** questions. Section A is short numerical, B is medium, C is large multi-part.
> 2. Show **every step** of your numerical work. Final answers without working get **half** marks at most.
> 3. Round final numerical answers to **3 decimal places** unless asked otherwise.
> 4. State any assumption you make explicitly.
> 5. Calculator allowed. Closed book — no notes.

> **Mark distribution at a glance**
> · Section A (4 × 5) = 20 marks
> · Section B (3 × 10) = 30 marks
> · Section C (2 × 25) = 50 marks
> · **Total = 100 marks**

---

## Section A — Short Numerical (4 × 5 = 20 marks)

### A1. PCY Hash Buckets (5 marks)

In the **first pass** of the **PCY (Park–Chen–Yu)** algorithm we have already computed item supports; all single items shown below are frequent. The following candidate **pairs of items** (using item IDs 1..6) have been streamed. Use the hash function

$$
h(i, j) = (i \cdot j) \bmod 11
$$

to hash each pair into one of 11 buckets (B0..B10). The support count of each pair is also given.

| Pair {i,j} | Support count |
|------------|---------------|
| {1, 4}     | 5             |
| {2, 3}     | 4             |
| {2, 5}     | 6             |
| {3, 5}     | 3             |
| {1, 6}     | 4             |
| {4, 5}     | 7             |
| {3, 4}     | 5             |
| {2, 4}     | 2             |

The minimum support threshold for a **frequent bucket** is $s = 7$.

**(a)** Compute the bucket index $h(i, j)$ for every pair and the **total count** in each bucket. *(3 marks)*

**(b)** List all **frequent buckets** (count ≥ 7). *(1 mark)*

**(c)** Pair {3, 5} happens to fall into a frequent bucket. Does PCY mark {3, 5} as a candidate for Pass 2? Justify in **one line**. *(1 mark)*

---

### A2. LSH S-curve Probability (5 marks)

You have signature length 100, partitioned into **b = 20 bands of r = 5 rows each**. Two documents have Jaccard similarity $s = 0.6$.

**(a)** Write the standard LSH "S-curve" formula for the probability that the pair becomes a **candidate** under banding. *(1 mark)*

**(b)** Compute the **numerical probability** that this pair is a candidate. Show intermediate values $s^r$, $(1 - s^r)^b$, and the final answer to 3 decimal places. *(4 marks)*

---

### A3. Recommender Baseline Prediction (5 marks)

For a Netflix-style rating system you are given:

- Global mean rating $\mu = 3.5$
- User bias $b_x = +0.4$  *(user X tends to rate higher than average)*
- Item bias $b_i = -0.2$  *(item i tends to be rated lower than average)*

**(a)** Write the **baseline predictor** formula $\hat r_{xi}$. *(1 mark)*

**(b)** Compute $\hat r_{xi}$ for user X on item i. *(2 marks)*

**(c)** Suppose item $i$ is later replaced with a popular item $j$ where $b_j = +0.5$. By how much does the baseline prediction for the same user **change**? *(2 marks)*

---

### A4. PageRank — Spider Trap vs Dead-End (5 marks)

For each of the three small directed web-graphs below, identify whether it contains a **spider trap**, a **dead-end**, or **neither**. Justify each answer in **one line**.

**Graph G1:** $A \to B$, $\;B \to A$, $\;C \to A$. *(2 marks)*

**Graph G2:** $A \to B$, $\;B \to C$, and $C$ has **no outgoing edges**. *(2 marks)*

**Graph G3:** $A \to B$, $\;B \to C$, $\;C \to A$. *(1 mark)*

---

## Section B — Medium Numerical (3 × 10 = 30 marks)

### B1. MinHash Signatures + LSH Banding (10 marks)

You are given the following **shingle/document membership matrix** (1 = shingle present in document) over rows $r_1, r_2, r_3, r_4$ and three documents $D_1, D_2, D_3$:

|         | $D_1$ | $D_2$ | $D_3$ |
|---------|:-----:|:-----:|:-----:|
| $r_1$   | 1     | 0     | 1     |
| $r_2$   | 1     | 1     | 0     |
| $r_3$   | 0     | 1     | 1     |
| $r_4$   | 0     | 1     | 1     |

Use the four hash functions (rows are numbered $x = 1..4$):

$$
h_1(x) = (x + 1) \bmod 5, \quad
h_2(x) = (3x + 1) \bmod 5,
$$
$$
h_3(x) = (2x + 3) \bmod 5, \quad
h_4(x) = (4x + 1) \bmod 5.
$$

**(a)** Build a 4×4 table giving $h_1(x), h_2(x), h_3(x), h_4(x)$ for $x = 1, 2, 3, 4$. *(2 marks)*

**(b)** Construct the **MinHash signature matrix** (4 rows × 3 columns) by applying all four hash functions over the membership matrix. Show **at least one column** of step-by-step minimisation. *(3 marks)*

**(c)** Now run **LSH banding** with $b = 2$ bands and $r = 2$ rows per band. State the band-vector for each document in each band, and identify all **candidate pairs**. *(5 marks)*

---

### B2. Spam Farm — Target Rank Calculation (10 marks)

A spam farm consists of $M$ pages all linking back to a target page $t$. Let:

- Teleport / damping factor: $\beta = 0.85$
- Total web size: $N = 10^{9}$
- "Honest" mass arriving at $t$ from outside the farm: $x = 10^{-4}$

The achievable PageRank of the target $t$ under the standard farm-attack model is

$$
y \;=\; \frac{x}{1 - \beta^{2}} \;+\; \frac{\beta}{1 + \beta} \cdot \frac{M}{N}.
$$

**(a)** With $M = 10^{5}$ farm pages, compute $y$. Show $1-\beta^2$, $\beta/(1+\beta)$, and the two additive terms separately. *(5 marks)*

**(b)** The attacker now wants to push the target rank up to $y^{\star} = 10^{-3}$. **How many farm pages $M$** are needed? Express in scientific notation to 3 significant figures. *(5 marks)*

---

### B3. BFR — Classify a New Point (10 marks)

A 2-D **BFR** Discard-Set (DS) cluster currently has the summary statistics

$$
N = 5, \quad \mathrm{SUM} = (20,\; 15), \quad \mathrm{SUMSQ} = (90,\; 50).
$$

A new streaming point $P = (6,\; 5)$ arrives. Use a **Mahalanobis threshold of 3**.

**(a)** Compute the cluster **centroid** $\boldsymbol c$. *(2 marks)*

**(b)** Compute the **per-dimension variance** $\sigma_x^{2}, \sigma_y^{2}$ and standard deviations $\sigma_x, \sigma_y$. *(3 marks)*

**(c)** Compute the **Mahalanobis distance** $d(P, \boldsymbol c)$. *(3 marks)*

**(d)** Decide whether $P$ joins the **DS**, the **CS** (compressed set), or the **RS** (retained set). Justify against the threshold. *(2 marks)*

> *Hint:* In BFR with diagonal covariance, $d^{2}(P, \boldsymbol c) = \sum_{i} \left(\frac{p_{i} - c_{i}}{\sigma_{i}}\right)^{2}$.

---

## Section C — Large Multi-Part Numerical (2 × 25 = 50 marks)

### C1. Hierarchical Clustering + CURE (25 marks)

Consider the following **seven 2-D points**:

| Point | Coordinates  |
|-------|--------------|
| $P_1$ | $(1, 1)$     |
| $P_2$ | $(1.5, 1.5)$ |
| $P_3$ | $(5, 5)$     |
| $P_4$ | $(3, 4)$     |
| $P_5$ | $(4, 4)$     |
| $P_6$ | $(10, 10)$   |
| $P_7$ | $(9, 9.5)$   |

Use **Euclidean distance** throughout. Round distances to **3 decimal places** when reporting (but keep extra precision in intermediate work).

**(a)** Compute the **upper-triangular 7 × 7 Euclidean distance matrix** between every pair of points. *(5 marks)*

**(b)** Run **agglomerative hierarchical clustering with single-linkage**. Show the **first 4 merges**, and after each merge write the **updated cluster set** and the **distance** at which the merge happened. State which clusters remain after merge #4. *(10 marks)*

**(c)** After merge #4 you should have **3 clusters**. Apply **CURE Phase 1**:
1. For each cluster, pick **k = 2 representative points** by **farthest-point selection** (start with the point farthest from the centroid, then the point farthest from those already chosen).
2. **Shrink** each representative toward its cluster centroid by $\alpha = 0.4$:
   $$
   r' \;=\; (1 - \alpha)\, r \;+\; \alpha\, \boldsymbol c.
   $$

List the centroid and the two shrunken representatives for each cluster. *(7 marks)*

**(d)** A new query point $Q = (4.5,\; 4.2)$ arrives. Apply **CURE Phase 2**: compute the distance from $Q$ to **every shrunken representative**, identify the nearest one, and assign $Q$ to the corresponding cluster. *(3 marks)*

---

### C2. Item-Item Collaborative Filtering + RMSE (25 marks)

You are given the **5-user × 4-movie utility matrix** below. A dash "—" denotes a missing rating.

|        | $M_1$ | $M_2$ | $M_3$ | $M_4$ |
|--------|:-----:|:-----:|:-----:|:-----:|
| $U_1$  | 5     | 3     | —     | 4     |
| $U_2$  | 4     | —     | 5     | 4     |
| $U_3$  | —     | 4     | 4     | 3     |
| $U_4$  | 3     | 2     | 3     | —     |
| $U_5$  | 5     | 3     | 4     | 5     |

**(a)** Using **Pearson** (mean-centered cosine) item-similarity restricted to **commonly-rated users**, compute:

- $\mathrm{sim}(M_1, M_3)$
- $\mathrm{sim}(M_2, M_3)$

Show item-mean computation, centered ratings, dot-product, both norms, and the final correlation to 3 d.p. *(8 marks)*

**(b)** Predict $\hat r(U_1, M_3)$ using **Item-Item collaborative filtering** with the **k = 2 most similar items** (by absolute similarity) **out of those $U_1$ has rated**. You will need $\mathrm{sim}(M_4, M_3)$ as well — compute it. Then write the prediction formula and evaluate it to 3 d.p. *(8 marks)*

> *Hint:* Use the standard weighted-average rule
> $$\hat r(u, i) \;=\; \frac{\sum_{j \in N_k} \mathrm{sim}(i, j)\, r(u, j)}{\sum_{j \in N_k} |\mathrm{sim}(i, j)|}.$$

**(c)** A held-out test set produces the following 5 (predicted, actual) pairs:

| #  | Predicted | Actual |
|----|----------:|-------:|
| 1  | 4         | 5      |
| 2  | 3         | 4      |
| 3  | 5         | 4      |
| 4  | 3         | 4      |
| 5  | 5         | 5      |

Compute the **RMSE** to 3 d.p. *(5 marks)*

**(d)** **Conceptual:** explain in **3–4 sentences** why **Item-Item CF often outperforms User-User CF in production-scale recommender systems**. Mention at least: **(i)** stability of item profiles vs user profiles over time, **(ii)** typical ratio of users to items, **(iii)** offline pre-computation feasibility. *(4 marks)*

---

## Examiner Tips (read before you start writing)

> 1. **Show the formula first**, then plug in numbers. Even one wrong arithmetic step still earns the formula mark.
> 2. **Don't round too early.** Carry 4–5 decimal places internally; round only the final answer.
> 3. **Label every table and matrix.** Examiner cannot give partial credit on an unlabelled cell.
> 4. **PCY**: a frequent **bucket** does **not** automatically make every pair in it a candidate — the pair itself must be in the surviving "frequent bucket" bitmap **and** both its items must be frequent.
> 5. **MinHash:** a column's signature is the **minimum** over rows where the document has a 1, computed independently per hash function.
> 6. **BFR threshold of 3** means **Mahalanobis distance ≤ 3**, i.e. ~3σ in the normalised space. Compare $d$, **not** $d^{2}$.
> 7. **CURE shrink:** $r' = (1-\alpha) r + \alpha c$ moves the representative **toward** the centroid. With $\alpha = 0.4$ you keep 60% of the rep's coords + 40% of the centroid's.
> 8. **Item-Item CF:** centre each **item column** by **its own mean**, and compute the dot product over **only the users common to both items**.
> 9. **RMSE** $= \sqrt{\frac{1}{n}\sum (\hat r - r)^{2}}$ — do **not** forget the square root or the division by $n$.
> 10. Manage your time: A ≈ 25 min, B ≈ 50 min, C ≈ 95 min, leaving ~10 min to check arithmetic.

*— End of Mock Paper 2 —*
