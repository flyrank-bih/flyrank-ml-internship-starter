---
name: flyrank-data
description: The FlyRank internship datasets — the 30k-row starter CSV and its gotchas, the ~79M-row warehouse release tables and grains, panel warnings, access, and iteration rules. Load for EVERY task that touches the data. (Project-specific: delete this folder when reusing the skill library elsewhere.)
---

# FlyRank internship data

Two datasets. The small one ships in this repo; the big one is hosted and gated.

## 1. Starter dataset (in this repo)

`data/raw/content_refresh_anonymized.csv` — 30,000 rows × 44 columns, one row per pseudonymized
content item, 32 clients, trailing-90-day metrics. Full column reference: `docs/data-dictionary.md`
(keep it open). The gotchas that cause 90% of mistakes:

- **Rate columns are ×100 percentages**: `ctr = 0.76` means 0.76%, not 76%. Applies to ctr,
  engagement_rate, scroll_rate, ai_traffic_pct, trend_pct.
- **`avg_position = 0` means "no data"**, not rank zero (1,205 rows).
- **`scroll_rate` and `ai_traffic_pct` can exceed 100** — numerator and denominator come from
  different measurement systems. Not a bug; read the dictionary.
- **The label trap:** `is_declining_label` is derived from `trend_direction`, which is computed
  from `trend_pct`. Therefore `trend_direction` and `trend_pct` are NEVER features.
- **Missingness follows content_type** (one type has ~100% missing keyword data; another ~28%
  missing word_count) — a blind fillna(0) injects a category signal. Add has_-flags instead.
- **IDs (`content_id`, `client_id`) are pseudonyms:** grouping/joining/splitting only, never
  features. Use client_id for grouped train/test splits.

## 2. Warehouse release (Hugging Face, gated — instant approval)

`hf://datasets/FlyRank/internship-warehouse` — build v20260703:

| Table | Rows | Grain |
|---|---|---|
| `dim_clients` | 104 | one per pseudonymized client |
| `dim_content` | 519,606 | one per content item |
| `fact_content_daily_performance` | 78,835,655 | report_date × client × content (partitioned by month) |
| `fact_content_daily_performance_sample` | ~11.7M | same grain — the FINAL MONTH (June 2026) only; fine for query mechanics, NEVER for label logic |
| `fact_content_query_90d` | 2,414,248 | client × content × query hash, fixed 90-day window |

Dates: 2025-01-27 → 2026-06-30 (~17 months). Position column is `gsc_avg_position`.

**Panel warnings (they are real):**
- History depth differs wildly per client — check `dim_clients.gsc_data_start` before defining
  any time window; prefer per-client windows over one global calendar window.
- Rows before a client's `ga4_data_start` have GA4 columns zero-FILLED with
  `ga4_data_available = FALSE` — filter on the flag; zeros there are not "no engagement".
- A third of clients have little or no usable search/analytics history — expect to filter.
- The query table's per-content context columns repeat on every row: `ANY_VALUE()` them, never
  `SUM()`. Its 90-day window overlaps the snapshot's final months — if your label lives in the
  last 30 days, only `*_prev30`-style columns are safe features (window alignment first!).

**Access + iteration rules:** request gate access once (instant), READ token via Colab
Secrets (`HF_TOKEN`) or env var — never pasted in a cell (public repo!). Iterate on a
**mid-panel month partition** (e.g. `month=2026-03`), not the `_sample`: the `_sample` is the
panel's LAST month, i.e. the natural outcome window of any past→future label — develop label
logic there and you are developing inside your own test window. Treat the final month as a
sealed test month. Run the full 79M scan ONCE when the query is final and cache the result to
`work/outputs/`. Repeated full scans hit HTTP 429 rate limits.

## How to verify

- Start any session with `COUNT(*)` + `MIN/MAX(report_date)` on your table and match the
  numbers above.
- Grain-probe before aggregating: `GROUP BY <grain cols> HAVING COUNT(*) > 1 LIMIT 5` → empty.
- If a number looks absurd (a 400% rate, a giant ratio from 12 rows), re-read the gotchas
  before celebrating.
