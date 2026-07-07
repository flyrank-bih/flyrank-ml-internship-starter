# Data Dictionary — `content_refresh_anonymized.csv`

One row per content item (page): **30,000 rows × 44 columns**, covering **32 pseudonymized
clients**. All metrics are aggregated over a trailing 90-day window ending at export time.
Keep this file open while you work.

## Read this first — the three rules that prevent 90% of mistakes

1. **Rate columns are ×100 percentages.** `ctr = 0.76` means **0.76%**, not 76%. Applies to
   `ctr`, `engagement_rate`, `scroll_rate`, `ai_traffic_pct`, `trend_pct`.
2. **The label comes from `trend_direction`.** The pipeline defines
   `is_declining_label = (trend_direction == "down")`, so `trend_direction` and `trend_pct`
   must **never** be model features — that's the leakage notebook 02 demonstrates.
3. **IDs are for grouping only.** `content_id` / `client_id` are pseudonyms: use them for
   joins and grouped train/test splits, never as features.

## Identifiers

| Column | Type | Meaning | Notes |
|---|---|---|---|
| `content_id` | text | Pseudonymous page id (`content_` + 12 hex chars) | Unique per row. Grouping/joins only |
| `client_id` | text | Pseudonymous client id (`client_` + 10 hex chars) | 32 distinct values. Use for **client-holdout splits** |

> **Missingness is systematic, not random.** Keyword-context columns are missing along
> `content_type` lines (e.g. `feedly article` rows have no keyword data at all). A blind
> `fillna(0)` therefore encodes content type into your features silently — check missingness
> per content_type before imputing.

## Keyword context (from content metadata)

| Column | Type | Meaning | Notes |
|---|---|---|---|
| `search_volume` | number | Search-volume estimate for the page's target keyword | 0–74,000 in this slice; blank for 2,468 rows with no keyword data |
| `competition` | number | Keyword competition score, 0–1 | Blank when no keyword data |
| `competition_level` | category | `LOW` / `MEDIUM` / `HIGH` | Blank when no keyword data |
| `cpc` | number | Cost-per-click estimate for the target keyword | Blank when no keyword data |
| `content_type` | category | `keyword article` / `feedly article` / `comparison article` | |
| `main_intent` | category | `informational` / `transactional` / `commercial` / `navigational` | Blank when unknown |

## Content properties

| Column | Type | Meaning | Notes |
|---|---|---|---|
| `word_count` | number | Article word count | Blank for 7,699 rows (not measured) |
| `char_count` | number | Article character count | Blank alongside `word_count` |
| `provider_used` | category | LLM provider that generated the article: `openai` / `google` / `other` | Blank when unknown. Not a model feature |
| `model_used` | category | LLM model name (e.g. `gemini-2.5-flash`, `gpt-4o-mini`) | Blank/`unknown` when not recorded. Not a model feature |
| `content_age_days` | number | Days since the content was created | Every row in this slice is ≥ 90 |
| `days_since_last_update` | number | Days since the content was last updated | |

## 90-day activity totals (GSC = Google Search Console, GA4 = Google Analytics)

| Column | Type | Meaning |
|---|---|---|
| `impressions_90d` | number | GSC search impressions (every row in this slice has ≥ 1) |
| `clicks_90d` | number | GSC clicks from search results |
| `pageviews_90d` | number | GA4 pageviews |
| `sessions_90d` | number | GA4 sessions |
| `users_90d` | number | GA4 users |
| `engaged_sessions_90d` | number | GA4 engaged sessions |
| `ai_sessions_90d` | number | GA4 sessions referred from AI tools — **click-throughs from AI assistants, not citations or rankings** |
| `scroll_events_90d` | number | GA4 scroll events |
| `days_with_impressions` | number | Days in the 90-day window with ≥ 1 impression (0–90) |
| `days_with_sessions` | number | Days in the window with ≥ 1 session (0–90) |

## 30-day comparison windows (the trend inputs)

| Column | Type | Meaning |
|---|---|---|
| `impressions_last_30d` | number | Impressions in the most recent 30 days |
| `clicks_last_30d` | number | Clicks, most recent 30 days |
| `sessions_last_30d` | number | Sessions, most recent 30 days |
| `impressions_prev_30d` | number | Impressions in the 30 days before that (days 31–60 back) |
| `clicks_prev_30d` | number | Clicks, days 31–60 back |
| `sessions_prev_30d` | number | Sessions, days 31–60 back |

## Derived rates (all ×100 percentages)

| Column | Formula | Notes |
|---|---|---|
| `ctr` | `clicks_90d / impressions_90d × 100` | 2 decimals. `0.76` = 0.76% |
| `avg_position` | mean GSC position over the window | 1 decimal. Lower is better. **`0` means "no position data", not position zero** (1,205 rows) |
| `engagement_rate` | `engaged_sessions_90d / sessions_90d × 100` | 0–100 |
| `scroll_rate` | `scroll_events_90d / pageviews_90d × 100` | **Can exceed 100** (multiple scroll events per pageview); blank when `pageviews_90d = 0` |
| `ai_traffic_pct` | `ai_sessions_90d / sessions_90d × 100` | **Can exceed 100** (AI-referred sessions are measured independently of total GA4 sessions) |
| `trend_pct` | `(impressions_last_30d − impressions_prev_30d) / impressions_prev_30d × 100` | 1 decimal. Blank when `impressions_prev_30d = 0` (3,388 rows; the prep step fills blanks with 0). **Label source — never a feature** |

## Buckets / tiers (transparent, threshold-based)

| Column | Values | Rule |
|---|---|---|
| `age_tier` | `0-14`, `15-30`, `31-90`, `91-180`, `181-365`, `365+` | From `content_age_days`. This slice only contains `31-90` and up |
| `age_tier_order` | 1–6 | Numeric order of `age_tier` (1 = youngest) |
| `freshness_tier` | `never`, `0-30`, `31-90`, `91-180`, `181+` | From `days_since_last_update`; `never` = no update recorded (0 rows in this slice) |
| `word_count_tier` | `<1000`, `1000-2000`, `2000-3500`, `3500+` | Blank when `word_count` is blank |
| `char_count_tier` | `<8000`, `8000-15000`, `15000-25000`, `25000+` | Blank when `char_count` is blank |
| `impression_tier` | `no_data`, `none`, `low`, `moderate`, `good`, `excellent` | `no_data` = client has no GSC; `none` = 0; `low` > 0; `moderate` ≥ 300; `good` ≥ 3,000; `excellent` ≥ 30,000 |
| `position_tier` | `no_data`, `top_3`, `page_1`, `striking`, `page_3_5`, `deep` | avg position ≤ 3 / ≤ 10 / ≤ 20 / ≤ 50 / > 50 |
| `trend_direction` | `new`, `flat`, `up`, `down`, `stable` | last-30d vs prev-30d impressions: `new` = prev 0 & last > 0; `flat` = both 0; `up` > +20%; `down` < −20%; else `stable`. **Label source — never a feature** |

## Columns the prep step adds (44 → 52 in `refresh_feature_vector.csv`)

`scripts/01_prepare_features.py` fills blanks (numerics → 0, categoricals → `"unknown"`) and adds:

| Column | Meaning |
|---|---|
| `is_declining_label` | **The target.** 1 when `trend_direction == "down"` (16,262 rows = 54.2%), else 0 |
| `log_impressions_90d`, `log_clicks_90d`, `log_sessions_90d`, `log_ai_sessions_90d` | `log1p` of the raw totals (traffic is heavy-tailed) |
| `has_clicks` | 1 when `clicks_90d > 0` |
| `has_ai_sessions` | 1 when `ai_sessions_90d > 0` |
| `measurable_opportunity` | 1 when `impressions_90d ≥ 100` and `sessions_90d > 0` |

Which of the 52 columns the models actually use is defined in one place:
`MODEL_NUMERIC_FEATURES` and `MODEL_CATEGORICAL_FEATURES` in `scripts/ml_utils.py`.

---

# The full warehouse release (weeks 3+)

The starter CSV above is a 30k-row teaching slice. Lane and capstone work run on the **full
pseudonymized warehouse release** — ~79M rows of daily search performance hosted as Parquet on
Hugging Face (gated; notebook 03 walks through access and the DuckDB workflow).

## Tables

| Table | Grain | Use it for |
|---|---|---|
| `dim_clients` | one row per pseudonymized client | history coverage (`gsc_data_start`, `ga4_data_start`), access profile |
| `dim_content` | one row per pseudonymized content item | content metadata, keyword context, joins |
| `fact_content_daily_performance` | report_date × client × content | time-series features, trend labels, forward-window validation. Partitioned by `month=YYYY-MM` |
| `fact_content_query_90d` | client × content × query hash (fixed 90-day window) | query-mix features: diversity, concentration, rare/anonymized tail |

## The three things to know before modeling it

1. **Unbalanced panel.** Per-client history depth differs (some clients have 17 months, some 3).
   `dim_clients.gsc_data_start` is the honest per-client start date — always check it before
   defining a time window, and prefer per-client windows over one global calendar window.
2. **GSC-only early history.** Rows before a client's `ga4_data_start` have GA4 columns
   zero-filled with `ga4_data_available = FALSE` — filter on the flag, don't treat zeros as
   "no engagement".
> ⚠️ **Leakage watch — the query table's window overlaps recent months.**
> `fact_content_query_90d` covers a fixed 90-day window (the most recent ~3 months of the
> snapshot). If your capstone predicts something about *those* months (e.g. "will this page
> decline next month?"), the `impressions_90d` / `*_last30` columns **contain your label period**
> — using them is leakage. Only the `*_prev30` columns are safe as features for a label defined
> on the final month. Always line up your feature window and label window against this table's
> window before you use it.

3. **The query table is internally complete — and *almost* fact-reconciled.** Per content item,
   kept rows (≥ 10 impressions) + `rare_impressions_share` + `anonymized_impressions_share`
   account for exactly 100% of `content_total_impressions_90d`. Against the daily fact summed
   over the same window, ~98.5% of content items match exactly; the rest are items registered
   to the platform **mid-window** — the daily fact only accrues history from registration day,
   while the query table attributes the full window using the current URL map. Treat
   `content_total_impressions_90d` as the query table's own denominator. Grain guard: the
   per-content context columns repeat on every row of that content item — `ANY_VALUE()` them,
   never `SUM()`.
