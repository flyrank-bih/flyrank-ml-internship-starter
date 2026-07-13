---
name: querying-big-datasets
description: Works with datasets far too big to download or load in pandas — SQL over remote Parquet with DuckDB, aggregate-then-model, iterate on samples. Use when a dataset has millions of rows, lives on a remote host (hf:// or s3), or a notebook runs out of memory or hits rate limits.
---

# Querying big datasets

The trick that makes 79 million rows feel small: **never bring the rows to you — send the
question to the rows.** Aggregate in SQL, bring back only the small answer, model on that.

## The pattern

```python
%pip -q install duckdb
import duckdb
con = duckdb.connect()
# remote Parquet reads like a local table — match the path to how the table ships:
# most tables are ONE flat file at the repo root:
REL = "read_parquet('hf://datasets/<org>/<name>/<table>.parquet')"
# partitioned tables are a directory of month folders:
REL = "read_parquet('hf://datasets/<org>/<name>/<table>/month=2026-03/*.parquet')"
# several months: pass an explicit LIST of paths — hf:// does NOT support {brace} globs,
# and pointing the /**/ glob at a flat-file table fails with an opaque HTTP error.
small = con.sql(f"""
    SELECT group_col, SUM(metric) AS total, COUNT(*) AS n
    FROM {REL}
    WHERE date_col >= DATE '2026-01-01'
    GROUP BY group_col
""").df()          # <- pandas gets ONLY the aggregate
```

- `COUNT(*)` and `MIN/MAX(date)` over Parquet touch metadata, not data — they're near-free.
  Start every session with them to confirm you're pointed at the right thing.
- Filter + aggregate in SQL; join small results in pandas; fit sklearn on the small frame.
- For gated remote data, register the token once:
  `con.execute("CREATE OR REPLACE SECRET hf (TYPE huggingface, TOKEN '<token>')")` — and never
  paste a token into a cell in a public repo; use getpass or the notebook's secrets panel.

## Iterate on the sample, finish on the full table

Remote hosts rate-limit repeated heavy scans (you'll see HTTP 429). So:

1. **Develop your query on the sample table** (if the release ships one) or on one month/partition.
2. Get the logic right there — cheap, fast, repeatable.
3. **Run the full scan once**, when the query is final. Cache the result to a local file
   (`df.to_parquet('work/outputs/features.parquet')`) so reruns don't re-scan.

If you get 429 anyway: stop, wait a minute, and switch to the sample. Hammering makes it worse.

## Grain guards (the classic big-table mistake)

In detail tables, per-item context columns repeat on every row. `SUM()` on them double-counts.
Use `ANY_VALUE(context_col)` (or group first at the right grain) — and test the grain with a
`GROUP BY ... HAVING COUNT(*) > 1` probe before trusting any aggregate.

## How to verify

- Your notebook reruns end-to-end in minutes, not hours — because heavy scans happen once and
  cache locally.
- Row counts from your aggregates reconcile with the dataset's published counts.
- No cell holds a raw multi-million-row dataframe. If one does, push that work into SQL.
