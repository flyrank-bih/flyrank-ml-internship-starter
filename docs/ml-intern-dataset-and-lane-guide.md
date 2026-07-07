# FlyRank ML Internship - Intern Dataset and Lane Guide

Status: intern-facing guide for the Applied Search Intelligence track.

Use this with:

- `docs/ml-core-foundation-framework.md` (ships in this repo)
- `docs/intern-free-tooling-guide.md` (ships in this repo)
- the cohort plan and week-by-week curriculum — on the InternHQ board / mentor-provided
- the data export spec — mentor-provided
- the data dictionary and manifests inside the approved dataset release your mentor gives you

> This starter repo ships only the small anonymized starter dataset (`data/raw/content_refresh_anonymized.csv`).
> The larger warehouse **release described below is mentor-provided** — it is not committed to this
> public repo. Request the approved release from your mentor when your lane needs it.

This guide explains how to use the data without turning the internship into a fixed-answer exercise. The goal is not to memorize FlyRank's existing rules. The goal is to understand the problem, inspect the evidence, build a baseline, test a better method, validate it honestly, and turn the result into safe ranked recommendations.

## 0. Source Traceability

This guide is grounded in the repo and BigQuery-derived artifacts, not in memory.

The counts, date windows, and provenance below come from FlyRank's **mentor-side** release
pipeline (BigQuery export, the pseudonymized warehouse release generator and its validation
report). That tooling and the full release are not part of this public starter repo — they are
mentor-provided. What ships here is:

- the runnable starter pipeline (`scripts/01`–`05`, `ml_utils.py`, `run_all.py`);
- its verified committed outputs (`outputs/model_report.md`, `outputs/refresh_queue_sample.csv`, `outputs/charts/`); `outputs/model_results.json` is regenerated when you run the pipeline;
- the small anonymized starter dataset (`data/raw/content_refresh_anonymized.csv`).

Important snapshot rule:

- For warehouse work, use only the approved release your mentor provides.
- Each approved release is a fixed predefined snapshot with the date windows documented below.
- Do not swap in another dataset for internship assignments unless a mentor approves it.
- You never need raw BigQuery credentials, raw client names, raw domains, raw URLs, raw private queries, or raw text.

## 1. Core Contract

The track follows one workflow:

```text
research question -> safe data contract -> signal audit -> baseline score -> selected modeling lane -> validation -> ranked action recommendations
```

The teaching method is:

```text
core idea first -> AI-assisted implementation second -> human judgment last
```

That means:

- Start with the content/search problem, not with a model.
- Use AI to draft code, alternatives, checks, and explanations, but do not let AI decide what is true.
- Treat product scores and flags as useful context, not sacred truth.
- Prefer simple explainable methods until complexity is clearly justified.
- Keep every claim tied to what the data can actually prove.

## 2. Which Data To Use

The internship data is the warehouse-shaped release below, plus the small runnable starter dataset that ships in this repo. Both carry observable signals only.

### Release Provenance

Warehouse-shaped release (mentor-provided):

- Release: [`FlyRank/internship-warehouse`](https://huggingface.co/datasets/FlyRank/internship-warehouse) on Hugging Face (gated — request access, accept the data-use terms, instant approval; notebook 03 shows the DuckDB workflow). Build `flyrank_pseudonymized_warehouse_release_v20260703`.
- Source: `central_data_warehouse`
- Export date: `2026-06-23`
- Freshness lag: 3 days from the export date (2026-07-03), so daily/time-series facts stop at `2026-06-30`
- Chunk size: 10,000 rows per CSV part
- Hash salt source: private ignored file
- Hash salt fingerprint: `7912504bb27e489b`
- Validation result: 0 blocking issues, 0 warnings

> **Iterating on features?** Develop against `fact_content_daily_performance_sample` (the latest full month, 11.7M rows) and run the full fact table only for your final pass — hammering the full table repeatedly can hit Hugging Face rate limits (HTTP 429).

For student work, cite only the approved release counts and date windows below.

### Student-Facing Lane Readiness

| Lane | Status | Default dataset | Allowed output |
|---|---|---|---|
| Ranking Signal Analysis | Core | warehouse release or starter dataset | Signal report and evidence-backed recommendations |
| Refresh / Content Opportunity Scoring | Core | starter playground plus warehouse support | Ranked review queue with scores, actions, and reason codes |
| Structured Content Archetype Clustering | Core | warehouse release or starter dataset | Cluster profiles and action mapping; do not call this semantic clustering |
| CTR / Engagement Opportunity Scoring | Core | warehouse release or starter dataset | Ranked opportunity score; position/volume adjusted |
| AI Referral Opportunity | Advanced | warehouse daily facts (`sessions_ai`; starter dataset: `ai_sessions_90d` / `ai_traffic_pct`) | EDA/ranking only by default; positive examples are sparse |
| Growth / Recovery / Momentum Prediction | Advanced | warehouse daily facts or mentor-built time windows | Future-window model with strict leakage audit |

### Warehouse-Shaped Data

The warehouse-shaped release gives you dimensional and fact tables; you define your own joins, windows, labels, and leakage checks.

Approved warehouse-shaped release — hosted at
[`FlyRank/internship-warehouse`](https://huggingface.co/datasets/FlyRank/internship-warehouse)
(gated; Parquet; see notebook 03). Lane example cuts:
[`FlyRank/internship-lanes`](https://huggingface.co/datasets/FlyRank/internship-lanes). Build id:

```text
flyrank_pseudonymized_warehouse_release_v20260703
```

| Table | Rows | Grain | Main use |
|---|---:|---|---|
| `dim_clients` | 104 | one row per pseudonymized client | grouping, client-level checks, per-client history coverage (`gsc_data_start`, `ga4_data_start`) |
| `dim_content` | 519,606 | one row per pseudonymized content item | content metadata and joins |
| `fact_content_daily_performance` | 78,835,655 | daily x client x content | time-series features, trend labels, forward-window validation |
| `fact_content_query_90d` | 2,414,248 | client x content x query hash (fixed 90-day window) | query-mix features: diversity, concentration, rare/anonymized tail |

Use the warehouse-shaped data when you want the most freedom. You must then write a stronger data contract because you control the joins, windows, labels, and leakage risks.

Fixed snapshot source coverage:

| Source object | Source rows | Clients | Content items | What it contributes |
|---|---:|---:|---:|---|
| `all_content_data` | 520,006 | 84 | 519,606 | Primary content dimension source |
| `daily_content_performance_v2` | 78,835,655 | 70 | 427,292 | Primary daily fact source (v2 full history), excluding the freshest 3 days |

Fixed snapshot date windows:

| Source/date field | Min date | Max date |
|---|---|---|
| `all_content_data.content_created_at` | 2024-10-16 | 2026-07-06 |
| `daily_content_performance_v2.report_date` | 2025-01-27 | 2026-06-30 |

History is an **unbalanced panel**: v2 extends per-client history to everything available (2025-01-27 onward; 9 of 70 clients have 12+ months, enough for seasonality work). Rows before a client's GA4 start are GSC-only with `ga4_data_available = FALSE` — check `dim_clients.gsc_data_start` / `ga4_data_start` before defining any time window.

Daily metric density inside the fixed snapshot:

| Metric presence | Rows |
|---|---:|
| daily fact rows | 78,835,655 |
| rows with GSC impressions | 28,970,051 |
| rows with GSC clicks | 3,112,607 |
| rows with GA4 sessions | 2,778,564 |
| rows with AI sessions | 30,177 |
| rows with scroll events | 600,821 |

Interpretation:

- The search-performance and lifecycle lanes have the strongest data depth.
- CTR and engagement lanes have enough direct signal, but students still need minimum-volume filters.
- AI-referral analysis is useful, but AI-session rows are much thinner than GSC impressions.
- The daily table is large because it is a fact table. Do not flatten it blindly; choose a decision grain and feature/target windows.

How the warehouse release was built:

- `dim_clients` combines covered clients from `dim_clients`, content, and daily performance sources.
- `dim_content` deduplicates content from `all_content_data` and related fact sources into one row per pseudonymized content item.
- `fact_content_daily_performance` applies the 3-day freshness lag: `report_date <= DATE_SUB(DATE('2026-06-23'), INTERVAL 3 DAY)`.
- Raw client names, domains, raw URLs, raw queries, raw keywords, content titles, and bridge files are not released in default tables.

Warehouse candidate keys and joins:

| Table | Candidate key or grain key |
|---|---|
| `dim_clients` | `client_hash_id` |
| `dim_content` | `content_hash_id` |
| `fact_content_daily_performance` | `report_date + client_hash_id + content_hash_id` |

Join rules:

- Join content facts to `dim_content` on `content_hash_id`.
- Join client-level facts to `dim_clients` on `client_hash_id`.
- Use `keyword_hash_id` and `url_hash_id` (on `dim_content`) for grouping, deduplication, leakage checks, and case analysis, not for identity reconstruction.

## 3. Field Types

When you inspect columns, classify them before modeling.

| Field type | Meaning | Example fields | Default use |
|---|---|---|---|
| Join keys | Pseudonymized identifiers used to connect tables | `client_hash_id`, `content_hash_id`, `url_hash_id`, `keyword_hash_id` | Join/group only; do not interpret as meaning |
| Observed signals | Measurements from search, analytics, or content metadata | impressions, clicks, position, CTR, sessions, scroll rate, word count, age | Good candidate features if available before the decision point |
| Derived measurements | Calculations from observed signals | `trend_pct`, age/freshness tiers, position tier | Usually okay if calculated only from the feature window |
| Product context | FlyRank product rule-outputs (`health_score`, `priority_score`, `action_type`, refresh flags), computed by the app and not shipped in the internship data | `health_score`, `priority_score`, `action_type`, `refresh_tier`, flags | Product outputs, not part of the internship dataset; if you ever reproduce one, treat it as context/baseline, never a discovery feature or label |
| Target/proxy fields | What the model or analysis tries to predict or rank | future decline, recovery, top-K action priority, cluster membership | Must be defined in your data contract |
| Raw-origin context | Origin was raw query, URL, title, or client detail before pseudonymization | raw query/URL/title/client fields | Not part of the internship data; keep any outputs public-safe |

## 4. Observable Signals, Not Product Decisions

FlyRank's product computes rule-based decision flags and composite scores with hand-tuned SQL — for example `health_score`, `needs_ctr_fix`, and `is_quick_win`, plus a `priority_score` and an `action_type`. These are how the app decides which pages to surface for action.

Those product decision flags and scores are deliberately **not** part of the internship data. The exported data ships observable search/engagement signals and transparent derived buckets (tiers, `trend_direction`, `trend_pct`, ctr, rates) only. This is observable-only by design so you discover signal from evidence and never reproduce or leak the product's own decisions.

The core principle: predict from pre-decision observable signals; never feed the product's own decision (or the outcome you are predicting) back in as a feature. Doing so creates circular results — the model looks strong because it learned the existing rule, not because it found a better signal.

The strongest supervised labels come from future observed outcomes, not from a current product decision. Prefer labels such as later traffic decline, recovery, CTR change, engagement change, or top-K action quality after a defined decision point. If an assignment ever asks you to reproduce a product flag as a proxy label, say that explicitly and evaluate it as a policy-replication or policy-audit task.

## 5. Starter Playground: What It Proves

The starter playground is a runnable example, not the whole internship. **It is this repo.**

Main input:

```text
data/raw/content_refresh_anonymized.csv
```

Pipeline (run all of it with `python scripts/run_all.py`):

```text
01_prepare_features.py -> 02_baseline_score.py -> 03_train_model.py -> 04_evaluate_and_export.py -> 05_build_pdf_report.py
```

The starter target is:

```text
is_declining_label = trend_direction == "down"
```

This is intentionally simple. It demonstrates the workflow, but it is a current-window derived bucket rather than a future outcome. Treat it as a beginner proxy label, not the ideal capstone target. Stronger capstones should define a future-looking outcome when possible, such as:

```text
features from prior 90 days -> decline or recovery over next 30 days
```

Exact starter feature-prep behavior:

- Input: `data/raw/content_refresh_anonymized.csv`.
- Required columns include `content_id`, `client_id`, `impressions_90d`, `sessions_90d`, `content_age_days`, and `trend_direction`.
- Rows are kept only when `impressions_90d > 0` and `content_age_days >= 90`.
- Rows are deduplicated by `content_id`.
- The exported data ships observable signals only; FlyRank's product decision flags are not included, so there is nothing to strip out. The label is `trend_direction == "down"`.

Starter model features:

- Numeric features: search volume, competition, CPC, word/char count, logged 90d impressions/clicks/sessions/AI sessions, days with impressions/sessions, age, freshness, CTR, average position, engagement rate, scroll rate, and AI traffic percentage.
- Categorical features: competition level, content type, main intent, age tier, freshness tier, word-count tier, impression tier, and position tier.

Exact starter baseline score:

```text
baseline_refresh_score =
  0.40 * visibility_score
+ 0.30 * freshness_risk_score
+ 0.25 * position_opportunity_score
+ 0.05 * depth_gap_score
```

Starter baseline reason-code examples:

- `stale_visible_page`: `days_since_last_update >= 180` and `impressions_90d >= 500`
- `declining_with_demand`: `trend_direction == "down"` and `impressions_90d >= 100`
- `thin_visible_page`: `word_count > 0`, `word_count < 1200`, and `impressions_90d >= 250`
- `page_one_decay_risk`: `avg_position > 0`, `avg_position <= 10`, and `content_age_days >= 180`
- `low_ctr_visible_page`: `impressions_90d >= 500`, `0 < avg_position <= 20`, and `ctr < 0.5`
- `low_engagement_visible_page`: `sessions_90d >= 30` and `engagement_rate` or `scroll_rate` below 30

Exact starter final scoring:

```text
final_refresh_score =
  100 * (0.70 * best_model_probability + 0.30 * normalized_baseline_score)
```

Final starter reason-code examples:

- `model_decline_risk`: model probability >= 0.65
- `visible_model_opportunity`: model probability >= 0.50 and `impressions_90d >= 500`
- `ctr_review_candidate`: `impressions_90d >= 500`, average position 1-20, and `ctr < 0.5`
- `engagement_review_candidate`: `sessions_90d >= 30` and `engagement_rate` or `scroll_rate` below 30

The starter high-confidence label also requires enough evidence: final score above the 80th percentile, `impressions_90d >= 500`, `sessions_90d >= 10`, and model probability >= 0.50.

Starter model result, verified from `outputs/model_results.json` and `outputs/model_report.md`:

| Method | ROC AUC | Average precision | Precision@50 |
|---|---:|---:|---:|
| baseline rules | 0.627 | 0.468 | 0.240 |
| logistic regression | 0.700 | 0.522 | 0.400 |
| decision tree | 0.742 | 0.575 | 0.540 |
| random forest | 0.750 | 0.618 | 0.740 |

Plain meaning:

- Precision@50 asks: among the top 50 pages the system says to review first, how many are actually positive by the chosen label?
- The baseline got about 12 of the top 50 right: `0.240 * 50`.
- The random forest got about 37 of the top 50 right: `0.740 * 50`.
- That is strong evidence that learned ranking can beat a fixed rule on this starter slice.

Scope caveat:

- This result is from a 30,000-row anonymized starter slice.
- It used client-holdout validation.
- It is not a benchmark on the full 69.2M-row daily warehouse.
- The full warehouse gives enough scale and structure for interns to test stronger definitions, but the result has to be earned again with proper validation.

## 6. What "The Right Page To Fix" Means

In this internship, "right page to fix" usually means:

```text
right page to review first, based on evidence and limited capacity
```

It does not mean:

```text
guaranteed page that will recover if edited
```

To prove that a refresh caused recovery, you would need an experiment or stronger causal design. Most capstones are decision-support projects: they rank candidates for human review.

Good candidates usually have:

- enough demand or exposure to matter;
- evidence of movement, weakness, or opportunity;
- an action someone could realistically take;
- reason codes that a reviewer can inspect;
- no obvious leakage or private-data issue;
- no obvious consolidation, seasonality, or noise explanation.

## 7. Decline Versus Consolidation, Seasonality, And Noise

Do not label every drop as decline.

| Pattern | What it means | How to check |
|---|---|---|
| Real decline | The same content loses meaningful visibility, clicks, or position over a sustained window | Compare prior and later windows; check impressions, clicks, position, and persistence |
| Consolidation | One URL drops because another related URL absorbs the demand | Check related content/keyword/url hash groups for demand absorbed by sibling pages |
| Seasonality | Demand naturally drops due to calendar or market timing | Compare to site-level trends, topic groups, or same-period historical behavior where available |
| SERP or AI click loss | Impressions or position may hold while clicks drop | Split impressions, clicks, CTR, position, and AI-session context |
| Noise | Small or low-volume movement with no persistent pattern | Require minimum volume, persistence, and confidence notes |

The line is a definition you choose and defend. A strong definition includes:

- magnitude: for example, a drop greater than a documented threshold;
- window: for example, prior 90 days versus next 30 days;
- persistence: the drop lasts beyond a short blip;
- minimum volume: enough impressions/sessions to avoid pure noise;
- group checks: related pages did not simply absorb the traffic;
- prediction-time discipline: the feature window does not overlap the target window.

## 8. Lane Guide

Each lane should produce the same core artifacts: data contract, signal audit, baseline, model or analysis, validation, ranked action output, and public-safe case study.

### Lane 1: Ranking Signal Analysis

Question:

```text
Which safe content and search signals are associated with visibility, clicks, engagement, or movement?
```

Good data:

- the warehouse release (`dim_content` + `fact_content_daily_performance`) or the starter dataset.

Good methods:

- EDA;
- correlations and grouped summaries;
- simple regressions or classification if a target is defined;
- feature importance from a simple model;
- effect-size reporting.

Output:

- signal report;
- charts;
- practical content recommendations;
- clear caveats that results are observational.

Common mistakes:

- claiming a Google algorithm factor was proven;
- using `health_score` as both feature and target;
- over-interpreting weak correlations.

### Lane 2: Refresh / Content Opportunity Scoring

Question:

```text
Which pages should be reviewed first for refresh, expansion, protection, pruning, or monitoring?
```

Good data:

- the warehouse release (`dim_content` + `fact_content_daily_performance`) or the starter dataset;
- warehouse-shaped daily performance for stronger time-window labels.

Good methods:

- transparent baseline score;
- logistic regression, decision tree, random forest, or gradient boosting where justified;
- ranked queue with reason codes;
- precision@K, recall, average precision, top-20 review.

Useful baseline ideas:

- stale visible page;
- declining with demand;
- thin visible page;
- page-one decay risk;
- CTR or engagement review context.

Output:

- ranked action queue;
- suggested action;
- reason codes;
- confidence label;
- model or analysis card.

Common mistakes:

- treating "declining" as guaranteed refresh ROI;
- using future-window metrics as features;
- hiding the reason behind a high score.

### Lane 3: Structured Content Archetype Clustering

Question:

```text
What performance archetypes exist across the content inventory?
```

Good data:

- the warehouse release (`dim_content` + `fact_content_daily_performance`) or the starter dataset.

The release supports structured clustering from safe metrics, buckets, token counts, and content metadata. It does not support true semantic/text clustering unless a separate approved embedding or safe topic release exists.

Good methods:

- scaling numeric features;
- K-Means or another explainable clustering method;
- PCA or two-dimensional projection for visualization;
- cluster profiling.

Possible archetypes:

- champions;
- rising stars;
- hidden gems;
- stale visible pages;
- weak/no-demand pages;
- engagement-problem pages;
- cannibalization-risk pages.

Output:

- cluster profiles;
- archetype names;
- action mapping such as protect, improve, rewrite, merge, prune, or monitor.

Common mistakes:

- naming clusters before inspecting them;
- treating clusters as true labels;
- using unsafe text fields or raw URLs;
- calling metric/token-count clustering "semantic clustering."

### Lane 4: CTR / Engagement Opportunity Scoring

Question:

```text
Which visible pages under-capture clicks or engagement and deserve metadata, content, or monitoring review?
```

Good data:

- the warehouse release (`dim_content` + `fact_content_daily_performance`) or the starter dataset;
- warehouse-shaped daily performance.

Good features:

- impressions;
- clicks;
- CTR;
- average position;
- position tier;
- intent/content type;
- age and freshness;
- sessions and engagement context.

Good methods:

- expected CTR by position tier;
- residual or gap analysis;
- ranked scoring;
- classification if you define a leakage-safe label.

Output:

- ranked list of CTR or engagement review candidates;
- reason codes such as high impressions, low CTR, strong position, enough volume, enough sessions, or weak engagement;
- action suggestions such as rewrite title/meta, improve intent match, improve snippet structure, improve on-page engagement, or monitor.

Common mistakes:

- comparing CTR across positions without position adjustment;
- ignoring low-volume noise;
- assuming low CTR always means title/meta is bad.

## 9. Advanced / Mentor-Gated Lane Guide

These are not normal beginner capstone choices. Use them only when a mentor approves the data contract, validation plan, and public-output rules.

### Advanced Lane A1: AI Referral Opportunity

Question:

```text
What broad content patterns appear around AI-referred traffic, and where might AI visibility be improved?
```

Good data:

- warehouse daily facts `sessions_ai` from `fact_content_daily_performance` (starter dataset: `ai_sessions_90d` / `ai_traffic_pct`) for AI-referral context;
- warehouse-derived positive/negative examples only if a mentor approves supervised modeling.

Best use:

- EDA;
- broad pattern analysis;
- opportunity ranking;
- careful discussion of data limits.

Important limit:

AI-referral sessions are sparse in the daily facts; treat this as EDA/ranking and do not train a binary classifier on AI sessions alone.

Output:

- pattern report;
- opportunity segments;
- cautious recommendations for content structure, definitions, FAQ blocks, or source clarity.

Common mistakes:

- treating no AI sessions as proof that AI platforms cannot understand the content;
- making strong claims from sparse AI-session data;
- building binary classifiers without valid positive and negative examples;
- claiming AI citations, AI rankings, or AI search visibility when the field only measures clicked-through AI-referral sessions.

### Advanced Lane A2: Growth / Recovery / Momentum Prediction

Question:

```text
Can we predict which pages are likely to decline, recover, or gain momentum?
```

Good data:

- the warehouse release (`dim_content` + `fact_content_daily_performance`) or the starter dataset;
- warehouse-shaped `fact_content_daily_performance` daily windows after a leakage review.

Best label shape:

```text
prior feature window -> future target window
```

Examples:

- prior 90 days of features -> next 30 days decline;
- prior 28 days of features -> next 28 days growth;
- prior state after refresh -> later recovery signal, if safely available.

Good methods:

- time-aware or client-grouped validation;
- logistic regression, tree, random forest, or gradient boosting;
- calibration and threshold review;
- precision@K for review queues.

Output:

- prediction report;
- ranked future-risk or future-opportunity list;
- validation audit;
- explanation of what the model can and cannot claim.

Common mistakes:

- using target-window metrics as features;
- mixing pages from the same client into train and test without a grouped check;
- calling seasonal movement model skill.

## 10. Do Not Do This

- Do not train an AI-session classifier on the sparse AI-session data alone.
- If you ever reproduce or add a product decision flag, `priority_score`, `action_type`, or `health_score`, do not use it as an ordinary model feature — the internship data is observable-only precisely to keep this discipline.
- Do not publish or reconstruct raw query, URL, title, domain, client, category, or keyword examples.
- Do not claim a refresh caused recovery unless there is an explicit experiment or causal design.
- Do not claim Google algorithm factors, AI citations, or AI rankings from these datasets.

## 11. Thresholds And Decision Policies

Thresholds are policy choices, not universal truths.

Examples:

- how many impressions are enough to matter;
- how much of a drop counts as decline;
- where CTR becomes weak for a position tier;
- how many pages fit the review team's capacity;
- what score becomes high confidence.

Good threshold workflow:

1. Start with a simple, explainable rule.
2. Show how many rows it captures.
3. Review examples from the top, middle, and edge cases.
4. Sweep alternative thresholds.
5. Compare precision@K, recall, false positives, and action value.
6. Pick the threshold that matches the decision capacity and risk.
7. Document the tradeoff.

For ranked action work, top-K metrics are often more useful than generic accuracy:

- Precision@20 if a reviewer checks 20 pages.
- Precision@50 if the team can act on 50 candidates.
- Average precision if the whole ranking matters.
- Recall if missing true problems is expensive.

## 12. Validation Rules

A model or analysis is only useful if the validation design matches the problem.

Use:

- train/test split for simple independent examples;
- client/group holdout when pages from the same client may share patterns;
- time-aware split when predicting future movement;
- top-K review for ranked queues;
- cluster stability checks for archetype lanes;
- leakage audit for every lane.

Leakage checklist:

- Are any features calculated after the decision point?
- Does the feature window overlap the target window?
- If you reproduced or added any product output (`health_score`, a decision flag, `priority_score`, or `action_type`), did it slip in as a normal feature?
- Does a derived field directly encode the target?
- Are duplicate or related rows split across train and test in a way that makes the test too easy?
- Are you testing on clients or time periods the model has not effectively memorized?

## 13. Precalculations: How To Use Them

Precalculated columns are allowed and useful. They should make the problem understandable, not remove the thinking.

Good uses:

- understand how FlyRank's existing system frames a page;
- build a transparent baseline;
- compare your model against the existing rule;
- inspect where your model disagrees with the product score;
- explain reason codes in a final action queue.

Risky uses:

- reproducing a product decision flag and then using it as a feature in a discovery model;
- calling a product flag the truth without checking future outcomes;
- optimizing only to match the old rule;
- leaning on a composite score like `health_score` instead of explaining the underlying signals.

If you use a precalculated field, answer:

- What is it trying to measure?
- Was it available at prediction time?
- Is it context, feature, label, or output?
- Could it leak the answer?
- Does the result still make sense if we remove it?

## 14. Public-Safe Output Rules

Your final work must be public-safe.

Allowed:

- pseudonymized IDs;
- aggregated metrics;
- charts from safe data;
- high-level examples;
- cautious observed/directional claims;
- generic content actions.

Not allowed:

- client names;
- domains;
- URLs;
- raw private queries;
- titles or text fields that reveal identity unless specifically approved;
- credentials or BigQuery internals;
- claims that you proved Google's algorithm;
- claims that refresh caused recovery unless you ran a valid causal design.

## 15. Final Capstone Checklist

Before submission, your package should answer:

- What problem are you solving?
- What decision or ranking are you improving?
- What row means one example?
- What data tables did you use?
- Which fields are features, labels/proxies, context, excluded, or leakage-risk?
- What baseline did you build?
- What model or analysis did you choose, and why?
- What split or validation design did you use?
- What metric matches the real decision?
- Did the model beat the baseline? If not, what did you learn?
- What are the top recommendations?
- What reason codes explain them?
- What would make a recommendation wrong?
- What claims are safe, and what claims are not proven?
- Can a mentor rerun or inspect the work?

## 16. One-Sentence Mental Model

You are not building magic SEO automation. You are using safe real-world search and content data to learn which signals help prioritize content decisions, then validating whether that prioritization is better than a transparent rule and explaining where human review is still required.
