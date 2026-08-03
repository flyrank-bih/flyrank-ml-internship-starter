# Capstone Report — Content Refresh Opportunity Scoring Engine

**Author:** Muhammad Taha Nadeem  
**Lane:** Refresh / Content Opportunity Scoring  
**Repo:** https://github.com/tahashyk84/FlyRank-Internship-Ml  
**Date:** August 2026  

---

## 0. Abstract

How can search editorial teams systematically prioritize content updates across client domains without relying on manual intuition? We analyzed an anonymized dataset of 30,000 content pages across 32 client domains using pre-decision performance metrics aggregated over 90-day windows. We trained a Random Forest classifier evaluated on an honest domain-grouped holdout split (`GroupShuffleSplit` by `client_id`) to prevent data leakage across client domains. The model achieved an honest ROC-AUC of 0.624 and a Precision-Recall AUC (PR-AUC) of 0.652, outperforming a naive baseline heuristic (PR-AUC of 0.512). The output is a prioritized Content Action Playbook featuring explicit reason codes and human-in-the-loop review guards for directional decision support.

---

## 1. Problem framing

* **Decision Supported:** Batch prioritization of content refresh, rewrite, and internal linking optimizations during quarterly content review cycles.
* **Unit of Analysis:** Individual content page (aggregated over a 90-day performance snapshot).
* **Target Output:** Continuous decay probability score ($[0, 1]$), mapped to explicit action categories and reason codes.
* **Human Action:** Editorial teams allocate budget and writing resources based on ranked queue priority instead of auditing pages randomly.
* **Cost of Wrong Call:**
  * *False Positive:* Unnecessary editorial spend allocated to stable pages.
  * *False Negative:* High-value decaying pages are ignored, leading to cumulative organic search traffic loss.
* **Why Data/ML Helps:** Human teams cannot manually track subtle ranking drops and scroll-rate decay across thousands of multi-tenant client URLs simultaneously. Machine learning identifies complex non-linear degradation signatures across multiple metrics.

---

## 2. Data safety

* **Dataset Used:** `content_refresh_anonymized.csv` (30,000 rows, 32 client domains).
* **Deliberately Excluded Columns:**
  * `trend_direction` & `trend_pct`: Excluded to prevent direct target leakage (label-derived target fields).
  * `client_id`: Used strictly as a grouping variable for domain-level splitting (`GroupShuffleSplit`), never as an input feature.
* **Public Safety Verification:** All client IDs are pseudonymous hashes (e.g., `client_7f2253d7e2`). No private URLs, client brand names, or unmasked search queries exist in `work/` or public artifacts.

---

## 3. Baseline

* **Rule/Score:** Naive Age-Based Heuristic (Flagging any content page with `content_age_days > 180` as declining).
* **Why Fair:** Represents standard industry practice where editorial teams refresh older content purely based on published age.
* **Baseline Performance (evaluated on the exact same holdout split):**
  * **Base Rate (Declining Class %):** ~48.2%
  * **Baseline Accuracy:** 51.4%
  * **Baseline PR-AUC:** 0.512
  * **Baseline ROC-AUC:** 0.508

---

## 4. Model / analysis

* **Method:** Random Forest Classifier (`n_estimators=100`, `max_depth=10`, `min_samples_leaf=5`, `random_state=42`).
* **Feature List:**
  * `impressions_90d`: 90-day impression volume.
  * `sessions_90d`: 90-day organic session count.
  * `avg_position`: Average search engine rank position.
  * `ctr`: Click-through rate.
  * `scroll_rate`: User engagement depth signal.
  * `content_age_days`: Age of page content in days.
* **Target Proxy Definition:** Binary indicator (`is_declining_label`) derived from `trend_direction == 'down'`.

---

## 5. Evaluation

* **Split Strategy:** `GroupShuffleSplit` by `client_id` (70% train / 30% test across 32 unique client domains).
* **Why Grouped:** Multi-tenant domain data creates massive data leakage if split randomly, as domain-specific baseline performance leaks between train and test sets. Grouping by `client_id` tests the model exclusively on unseen web domains.
* **Model vs. Baseline (Grouped Holdout Split):**
  * **Base Rate:** 48.2%
  * **Model PR-AUC:** 0.652 (vs. Baseline 0.512)
  * **Model ROC-AUC:** 0.624 (vs. Baseline 0.508)
* **Error Analysis:**
  * **Extreme False Positives:** High-impression pages with deep scroll depth flagged due to slight ranking slips (handled via human review rules).
  * **Extreme False Negatives:** Rapidly declining pages with recent publication dates (<60 days) where age signals lagged behind traffic drop.

---

## 6. Interpretation

* **Top Feature Importances:**
  1. `impressions_90d` (0.305): Driving signal for visibility decay.
  2. `content_age_days` (0.249): Non-linear threshold effect after ~180 days.
  3. `avg_position` (0.236): Direct indicator of ranking slips beyond page 1.
* **Surprises / Negative Results:** Click-through rate (`ctr`, 0.069) and `sessions_90d` (0.060) had lower feature importance than raw impressions and position rank, showing that visibility drops precede traffic loss.

---

## 7. Recommendation

* **Action Playbook Archetypes:**
  1. `Full Content Rewrite` (`REASON_AGED_HIGH_DECAY`): High probability decay on stale content (`prob >= 0.70`, `age > 180d`).
  2. `Title & Meta Optimization` (`REASON_LOW_CTR_SERP`): Low CTR despite active impressions (`prob >= 0.50`, `ctr < 0.03`).
  3. `Internal Linking Boost` (`REASON_RANKING_SLIP`): Keywords slipping beyond page 1 (`prob >= 0.50`, `pos > 15`).
  4. `Maintain & Monitor` (`REASON_STABLE`): Normal baseline performance.
* **Human Review & No-Go Guards:** 23.9% of border cases (probabilities between 0.45–0.55 and all YMYL/Legal pages) require mandatory human review. Automated execution on compliance or legal pages is strictly prohibited.
* **Limits:** Model outputs are directional decision-support signals, not guarantees of rank recovery or causal impact.

---

## 8. Reproducibility

* **Execution Environment:** Python 3.10+, `scikit-learn>=1.2.0`, `pandas>=2.0.0`, `seaborn>=0.12.0`.
* **Random Seed:** `42` across all splitters and estimators.
* **Commands to Run:**
  ```bash
  git clone [https://github.com/tahashyk84/FlyRank-Internship-Ml.git](https://github.com/tahashyk84/FlyRank-Internship-Ml.git)
  cd FlyRank-Internship-Ml
  pip install -r requirements.txt
  jupyter nbconvert --to notebook --execute work/notebooks/capstone.ipynb
