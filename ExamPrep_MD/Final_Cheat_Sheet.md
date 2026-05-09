---
title: "BDA Final — Last-Night Cheat Sheet"
subtitle: "Every formula, every algorithm, every trap — 3-page crash recall"
author: "BDA Final Exam Prep · Comprehensive Tutor"
course: "CS-404 Big Data Analytics — Dr. Syed Imran Ali"
exam: "Final ~ 2026-05-16"
---

## §1 — Big-Picture Recall

1. **Big Data = 5V's**: Volume, Velocity, Variety, Veracity, Value.
2. **Apriori principle**: any subset of a frequent itemset is frequent (downward closure).
3. **MinHash** estimates Jaccard similarity; **LSH** finds candidate pairs sub-linearly.
4. **PageRank**: random surfer with teleport $\beta\approx 0.85$ — solves $r = \beta M r + \frac{1-\beta}{N}\mathbf{1}$.
5. **Topic-Sensitive PageRank** teleports only to a topic set $S$, not to all $N$ pages.
6. **Spam farm gain**: $y = \frac{x}{1-\beta^2} + \frac{\beta}{1+\beta}\cdot\frac{m}{N}$ — multiplier $\approx 3.6$ at $\beta=0.85$.
7. **TrustRank** = topic-PR seeded on **trusted** pages; **Spam Mass** $SM = (r - r^+)/r$.
8. **Recommendation**: content-based (item profiles) vs collaborative filtering (user/item similarity).
9. **k-means** minimizes WCSS; centroid = arithmetic mean; needs $k$ known.
10. **BFR / CURE**: streaming/large clustering — DS, CS, RS sets; Mahalanobis distance for membership.
11. **Girvan-Newman**: iteratively remove highest-betweenness edge — bridges break first.
12. **Spectral clustering**: Laplacian $L=D-A$; second-smallest eigenvector (Fiedler) bipartitions.

---

## §2 — Numerical Reference Table

| Algorithm | Key formula | When to use |
|---|---|---|
| **PageRank (basic)** | $r = M r$, with $M_{ij}=1/d_j$ if $j\to i$ | Web ranking, no dead ends |
| **PageRank (taxed)** | $r = \beta M r + \frac{1-\beta}{N}\mathbf{1}$ | Standard ranking, $\beta=0.85$ |
| **PageRank (leak fix)** | $r = \beta M r + \frac{1-S}{N}\mathbf{1}$, $S=\sum r_i$ | Dead-ends present; renormalize |
| **Topic-Sensitive PR** | $r = \beta M r + \frac{1-\beta}{|S|}e_S$ | Personalization on topic set $S$ |
| **Spam Farm** | $y = \frac{x}{1-\beta^2} + \frac{\beta}{1+\beta}\cdot\frac{m}{N}$ | Multiplier on supporter rank |
| **TrustRank** | Topic-PR with $S=$trusted seed set | Detect non-spam |
| **Spam Mass** | $SM = (r - r^+)/r$ | $SM\to 1$ = spam, $\to 0$ = good |
| **HITS hub** | $h = A a$, then normalize | Hub score = sum of authority of out-links |
| **HITS authority** | $a = A^T h$, then normalize | Authority = sum of hubs pointing to it |
| **Jaccard** | $J(A,B) = \frac{|A\cap B|}{|A\cup B|}$ | Set similarity |
| **MinHash** | $\Pr[h(A)=h(B)] = J(A,B)$ | Estimate Jaccard via signatures |
| **LSH (S-curve)** | $\Pr[\text{candidate}] = 1 - (1-s^r)^b$ | Threshold $t\approx (1/b)^{1/r}$ |
| **Apriori support** | $\text{supp}(X) = \frac{|\{T:X\subseteq T\}|}{N}$ | Frequency filter |
| **Confidence** | $\text{conf}(X\to Y) = \frac{\text{supp}(X\cup Y)}{\text{supp}(X)}$ | Rule strength |
| **Lift** | $\text{lift}(X\to Y) = \frac{\text{conf}}{\text{supp}(Y)}$ | Lift > 1 means correlated |
| **PCY pass-1** | hash each pair; bucket count $\geq s$ ⇒ frequent bucket | Memory-efficient pair pruning |
| **PCY pass-2** | candidate iff both items frequent **AND** in frequent bucket | Pair counting only on candidates |
| **SON** | local frequent (per chunk) ⇒ global candidate ⇒ verify | Map-Reduce friendly |
| **k-means** | $\arg\min\sum_{i}\|x_i - \mu_{c(i)}\|^2$ | Spherical/convex clusters, known $k$ |
| **BFR Mahalanobis** | $d_M(x,c)=\sqrt{\sum_{i=1}^d \left(\frac{x_i-c_i}{\sigma_i}\right)^2}$ | Stream point ↔ DS/CS test |
| **BFR threshold** | $d_M < \alpha\sqrt{d}$, typically $\alpha=2\text{ or }3$ | Add to DS if within ellipsoid |
| **CURE shrinkage** | $p' = p + \alpha(\mu - p)$, $\alpha\in[0,1]$ | Move repr. points toward centroid |
| **Girvan-Newman** | Remove $\arg\max$ edge betweenness, repeat | Hierarchical community detection |
| **Modularity Q** | $Q = \frac{1}{2m}\sum_{ij}\left[A_{ij}-\frac{k_ik_j}{2m}\right]\delta(c_i,c_j)$ | Quality of partition |
| **Spectral cut** | Sort Fiedler vector $v_2$; split at 0 (or median) | Min-cut bipartition |
| **Pearson sim** | $\text{sim}(u,v)=\frac{\sum(r_{ui}-\bar r_u)(r_{vi}-\bar r_v)}{\sqrt{\sum(\cdot)^2}\sqrt{\sum(\cdot)^2}}$ | User-user similarity (mean-centered) |
| **Cosine sim** | $\cos(u,v)=\frac{u\cdot v}{\|u\|\|v\|}$ | Item-item, content vectors |
| **Item-Item CF** | $\hat r_{ui}=\frac{\sum_{j\in N}\text{sim}(i,j)\cdot r_{uj}}{\sum_{j\in N}|\text{sim}(i,j)|}$ | Predict user $u$'s rating for item $i$ |
| **Baseline predictor** | $b_{ui}=\mu+b_u+b_i$ | Global + user bias + item bias |
| **CF + baseline** | $\hat r_{ui}=b_{ui}+\frac{\sum\text{sim}(i,j)(r_{uj}-b_{uj})}{\sum|\text{sim}(i,j)|}$ | More accurate prediction |
| **RMSE** | $\sqrt{\frac{1}{n}\sum(\hat r-r)^2}$ | Evaluation metric |
| **Bonferroni FP** | $E[\text{FP}] \approx \binom{N}{k}\cdot p$ | Statistical risk in mining |

---

## §3 — Algorithm Steps Quick-Refresher

**PageRank power iteration (with leak handling):** (1) Init $r^{(0)}=\frac{1}{N}\mathbf{1}$. (2) Compute $r' = \beta M r$. (3) Compute leaked mass $S = \sum_i r'_i$. (4) Re-add: $r^{\text{new}} = r' + \frac{1-S}{N}\mathbf{1}$. (5) Repeat until $\|r^{\text{new}}-r\|_1 < \epsilon$.

**Topic-Sensitive PageRank:** identical to taxed PR, but teleport only redistributes to topic set $S$: $r^{\text{new}} = \beta M r + \frac{1-\beta}{|S|}e_S$, where $e_S$ has $1$ on pages in $S$ and $0$ otherwise.

**MinHash + LSH banding:** (1) Build characteristic matrix (rows=shingles, cols=docs). (2) For each of $n$ hash functions, compute MinHash signature row of length $n$. (3) Split signature into $b$ bands of $r$ rows ($n=br$). (4) Hash each band per doc; same bucket in any band ⇒ candidate pair. (5) Verify candidates by true Jaccard.

**Apriori (with join + prune):** (1) Scan DB, compute $L_1$ (frequent 1-itemsets). (2) Generate $C_k$ from $L_{k-1}$ via **join**: union two $(k-1)$-itemsets sharing first $k-2$ items in lex order. (3) **Prune**: drop any $C_k$ candidate having a $(k-1)$-subset not in $L_{k-1}$. (4) Scan DB to count $C_k$; keep those $\geq s$ as $L_k$. (5) Repeat until $L_k=\emptyset$.

**PCY (Park-Chen-Yu):** *Pass 1:* for each transaction, count single items AND hash every pair into bucket array (count++); after pass, mark buckets with count $\geq s$ as **frequent buckets**. *Pass 2:* candidate pair $(i,j)$ requires (a) both $i,j$ frequent singletons AND (b) hash$(i,j)$ falls in frequent bucket. Count only those candidates.

**k-means:** (1) Pick $k$ initial centroids (random or k-means++). (2) **Assign**: each point ↦ nearest centroid (Euclidean). (3) **Update**: each centroid = mean of its assigned points. (4) Repeat until assignments stable / centroids move $<\epsilon$. Cost = WCSS = $\sum\|x-\mu\|^2$.

**Hierarchical agglomerative:** (1) Each point = own cluster. (2) Find closest cluster pair under chosen linkage (single=min, complete=max, average=avg, Ward=variance-min). (3) Merge them. (4) Update distance matrix. (5) Repeat until 1 cluster (or stop at $k$). Output: dendrogram.

**BFR (DS / CS / RS handling):** Maintain three sets: **DS** (points absorbed into final clusters; keep only $N, \text{SUM}, \text{SUMSQ}$), **CS** (mini-clusters of outliers), **RS** (lone outliers). For each new chunk: (1) For each point, if Mahalanobis distance to a DS centroid $< \alpha\sqrt d$ ⇒ add to DS, update stats. (2) Else, try CS the same way. (3) Else, put in RS. (4) Cluster RS via mini k-means → form/grow CS. (5) Optionally merge close CS clusters. (6) At end, fold remaining CS, RS into DS.

**CURE (Phase 1 + Phase 2):** *Phase 1 (sample):* (a) take random sample fitting in memory; (b) run hierarchical clustering on sample; (c) for each cluster pick $c$ scattered **representative points** (well-spread); (d) **shrink** each representative toward centroid by $\alpha$: $p'=p+\alpha(\mu-p)$. *Phase 2 (full data):* assign every remaining point to the cluster whose nearest representative is closest. Handles non-spherical clusters, robust to outliers.

**Girvan-Newman:** (1) Compute betweenness for every edge (number of shortest paths through it). (2) Remove edge with **max** betweenness. (3) Recompute betweenness on remaining graph. (4) Repeat — graph splits into components → these are communities. (5) Optional: pick partition with max modularity $Q$.

**Spectral clustering:** (1) Build adjacency $A$ and degree $D=\text{diag}(d_i)$. (2) Form Laplacian $L=D-A$ (or normalized $L_{\text{sym}}=I-D^{-1/2}AD^{-1/2}$). (3) Compute eigenvalues; smallest is $0$. (4) Take eigenvector $v_2$ of **second-smallest** eigenvalue (Fiedler vector). (5) Bipartition: nodes with $v_2(i)>0$ vs $\leq 0$ (or split at median). (6) For $k$ clusters: take first $k$ eigenvectors as features, run k-means.

**Item-Item CF prediction:** (1) Compute item-item similarity (Pearson or cosine, often centered). (2) For target $(u,i)$: find neighborhood $N$ = top-$k$ items most similar to $i$ that user $u$ has rated. (3) Predict $\hat r_{ui}=\frac{\sum_{j\in N}\text{sim}(i,j)\cdot r_{uj}}{\sum_{j\in N}|\text{sim}(i,j)|}$. (4) For better accuracy, subtract baseline before weighting and add it back.

---

## §4 — Worked-Numbers Reference Card

| Quantity | Value | Context |
|---|---|---|
| $\beta$ default | $0.85$ | Standard PageRank teleport |
| $1/(1-\beta^2)$ at $\beta=0.85$ | $\approx 3.6$ | Spam-farm rank multiplier |
| $\beta/(1+\beta)$ at $\beta=0.85$ | $\approx 0.459$ | Spam-farm bonus coefficient |
| $1/(1-\beta)$ at $\beta=0.85$ | $\approx 6.67$ | Geometric series sum cap |
| $1/(1-\beta^2)$ at $\beta=0.9$ | $\approx 5.26$ | High teleport multiplier |
| $1/(1-\beta^2)$ at $\beta=0.5$ | $\approx 1.33$ | Low teleport multiplier |
| 3σ rule | $\approx 99.7\%$ | Normal data within $3\sigma$ |
| 2σ rule | $\approx 95.4\%$ | Common BFR threshold |
| Mahalanobis cutoff | $\alpha\sqrt d$, $\alpha=2$ or $3$ | Add point to DS |
| LSH threshold | $t \approx (1/b)^{1/r}$ | Crossover of S-curve |
| $b=20, r=5$ | $t\approx 0.55$ | Typical LSH config |
| $b=50, r=2$ | $t\approx 0.14$ | Loose / many candidates |
| Random surfer steady state | $r_i \propto $ in-flow weighted by source out-deg | Eigenvector of $M$ |
| PCY bucket threshold | support count $s$ | Same threshold as item support |
| Apriori chains | typical 5-7 passes | $L_1\to L_2\to\dots$ |
| Spam Mass good page | $\approx 0$ | $r^+\approx r$ |
| Spam Mass spam page | $\to 1$ | $r^+\ll r$ |

---

## §5 — Top 15 Exam Traps

> **Trap 1**: $M$ is **column-stochastic**, not row-stochastic — column $j$ sums to 1 (out-edges of $j$).

> **Trap 2**: rank uses **SOURCE** out-degree $d_j$, not target in-degree — $M_{ij}=1/d_j$.

> **Trap 3**: Mahalanobis $= \sqrt{\sum_i \left(\frac{x_i-c_i}{\sigma_i}\right)^2}$ — don't forget per-dimension $\sigma_i$.

> **Trap 4**: with dead-ends, leak term is $(1-S)/N$ where $S=\sum r_i$, **NOT** $(1-\beta)/N$.

> **Trap 5**: Apriori **join** — combine two $(k-1)$-itemsets only if they share the **first $k-2$ items in lex order**.

> **Trap 6**: Apriori **prune** — drop $C_k$ if **any** $(k-1)$-subset is missing from $L_{k-1}$.

> **Trap 7**: PCY — frequent **bucket** ≠ frequent **pair**; bucket frequency only **enables** candidacy.

> **Trap 8**: **Pearson = mean-centered cosine** — subtract user's mean rating before cosine.

> **Trap 9**: CF prediction normalizes by $\sum|\text{sim}|$, **not** $\sum\text{sim}$ — negative similarities don't cancel weights.

> **Trap 10**: Spam Mass $SM = (r - r^+)/r$, **NOT** $r^+/r$ — high SM means spam.

> **Trap 11**: **Edge** betweenness ≠ **node** betweenness — Girvan-Newman uses edge.

> **Trap 12**: Laplacian $L = D - A$, **NOT** $A - D$. Sign matters for eigenvalues.

> **Trap 13**: Fiedler vector = eigenvector of the **SECOND-smallest** eigenvalue (smallest is $0$).

> **Trap 14**: k-means centroid is the **mean**, not the median — k-medoids uses medoid.

> **Trap 15**: Single-linkage merges by **MIN** of pairwise distances, complete-linkage by **MAX**, average by mean.

> **Bonus Trap**: Topic-sensitive PR teleport divides by $|S|$, not $N$ — only topic pages get teleport mass.

> **Bonus Trap**: HITS — update $h$ from current $a$ then $a$ from new $h$, normalize each step (else blow-up).

---

## §6 — Time Allocation Strategy (3-hour exam)

- **Section A — short questions (~30 min total)**: ~7 min each. Definitions, small calculations, identify-the-algorithm. **Don't dwell** — write the formula, plug in, move on.
- **Section B — medium (~50 min total)**: ~17 min each. Derive a step or trace 2-3 iterations. Write **every line** of the recurrence — markers reward visible work.
- **Section C — long multi-part (~100 min)**: ~50 min each. Page-rank traces, Apriori with PCY, BFR over a chunk, Girvan-Newman manual.
- **Show every step.** Numerical traces earn partial credit per step — even one correct iteration is worth marks.
- **Reserve a right-margin column** on each answer page for sanity-checks: row sums of $M$, column-stochastic check, total support, $\sum r_i = 1$.
- **Propagate forward**. If part (a) gave a wrong centroid, **still use it** in (b) — markers reward consistent algebra. Don't redo.
- **Box your final answer**. Always.
- **Last 10 min**: re-check obvious arithmetic — column sums, normalization, units.

---

## §7 — Last-Minute Comprehension Triggers

Read these FIRST if blanking on an algorithm:

- **PageRank** → "rank in proportion to **incoming**, divided by **source out-degree**, plus teleport".
- **Topic-PR** → "teleport only to topic set $S$, dilute by $|S|$ not $N$".
- **HITS** → "two scores: hub points to good authorities; authority pointed-to by good hubs".
- **Spam Farm** → "supporter pages siphon back to target via $\beta$ — multiplier $\frac{1}{1-\beta^2}$".
- **TrustRank / Spam Mass** → "topic-PR from trusted seeds; SM measures how little trust the page gets".
- **MinHash** → "row of mins under $n$ hashes; collision probability **equals** Jaccard".
- **LSH** → "split signature into bands; share a bucket in **any** band ⇒ candidate".
- **Apriori** → "**downward-closure**: subsets of frequent are frequent; build $L_k$ from $L_{k-1}$".
- **PCY** → "use spare memory in pass-1 to hash pairs into buckets; pass-2 only counts pairs in frequent buckets".
- **SON** → "local frequent in chunk → global candidate; verify globally; map-reduce friendly".
- **k-means** → "assign-update-repeat; minimize WCSS; spherical clusters only".
- **Hierarchical** → "merge closest; linkage = min/max/avg/Ward; output dendrogram".
- **BFR** → "DS + CS + RS; **Mahalanobis** test for membership in DS".
- **CURE** → "sample, cluster, pick scattered reps, shrink toward centroid by $\alpha$, scan rest".
- **Girvan-Newman** → "highest **edge** betweenness IS the bridge; remove iteratively".
- **Modularity** → "actual within-community edges minus expected by chance — pick partition maxing $Q$".
- **Spectral** → "graph as matrix; smallest non-trivial eigenvector (Fiedler) splits it".
- **Item-Item CF** → "find $k$ similar items the user rated; weighted-avg by similarity".
- **Pearson** → "mean-center then cosine — handles tough/easy raters".
- **Baseline predictor** → "$\mu$ + user bias + item bias; CF predicts the **residual**".
- **Bonferroni** → "if you check too many possibilities, false positives explode — restrict the search".
- **RMSE** → "average squared error, then square-root; sensitive to outliers".

---

### Final 30-Second Mantras

- **PageRank**: $r = \beta M r + \frac{1-\beta}{N}\mathbf{1}$. Leak ⇒ $\frac{1-S}{N}$.
- **LSH**: $1-(1-s^r)^b$, threshold $(1/b)^{1/r}$.
- **Apriori**: join (lex) + prune (subset check) + count.
- **k-means**: assign $\to$ update $\to$ repeat. Minimizes WCSS.
- **BFR**: Mahalanobis $< \alpha\sqrt d$ ⇒ DS.
- **GN**: max edge betweenness ⇒ remove.
- **Spectral**: $L=D-A$; Fiedler $v_2$ splits.
- **CF**: $\hat r = \frac{\sum \text{sim}\cdot r}{\sum |\text{sim}|}$.
- **Spam Mass**: $(r - r^+)/r$ — high = spam.

**Walk in. Box the formula. Show every step. Propagate forward. You've got this.**
