# GUIDE — how this repo works

Five minutes here saves you hours later. This is the operating manual: what every file is,
what you may edit, how the pieces connect, and where your own work goes.

## 1. The map

| Path | What it is | Your relationship to it |
|---|---|---|
| `README.md` | Front door: quickstart + safety summary | Read once |
| `GUIDE.md` | This file | Read once, revisit when unsure |
| `SETUP.md` | GitHub + Colab (Week 1) and Hugging Face access (Week 3) — with the silent pitfalls | Follow it at those two moments |
| `DATA_USE.md` | The data rules you agree to by working here | **Read before touching the data** |
| `LICENSE` | MIT — covers the **code** only; the data is governed by `DATA_USE.md` | Reference |
| `data/raw/content_refresh_anonymized.csv` | The one dataset that ships here: 30,000 pseudonymized pages × 44 columns | **Read-only.** Never add files under `data/` |
| `data/processed/` | Intermediate files the pipeline writes (created on first run; gitignored) | Leave alone — delete freely, it regenerates |
| `scripts/01…05` + `run_all.py` | The **reference pipeline**: prepare → baseline → train → evaluate → PDF | **Run it and copy from it — don't edit it.** It's the baseline you compare your work against, and reviewers expect to find it unchanged |
| `scripts/ml_utils.py` | Shared paths, helpers, and the feature lists | The one `scripts/` file you *may* edit — e.g. `MODEL_NUMERIC_FEATURES` to try a feature idea. Note any change in your report |
| `notebooks/01`, `notebooks/02` | Week 1–2 guided notebooks (Colab-ready) | Run top to bottom; do the "your turn" cells |
| `notebooks/03` | Weeks 3+: the **full warehouse release** via DuckDB + Hugging Face | The workflow your lane and capstone run on — aggregate in SQL, model in sklearn |
| `outputs/` | Pipeline results. Three **committed examples** show the target shape (`model_report.md`, `refresh_queue_sample.csv`, `charts/`); everything else regenerates | Regenerated files are gitignored — that's intentional (see FAQ) |
| `work/` | **Yours.** Lane experiments, capstone notebook, report | Everything you build lives here — start with `work/README.md` |
| `docs/data-dictionary.md` | All 44 columns: meaning, scale, gotchas | Keep open while you work |
| `docs/ml-intern-dataset-and-lane-guide.md` | Data safety, the lanes, the capstone workflow | Read in Week 1–2 |
| `docs/ml-core-foundation-framework.md` | The ML-as-a-system map behind the live sessions | Reference |
| `docs/intern-free-tooling-guide.md` | The zero-budget tool stack | Reference |
| `.github/workflows/smoke-test.yml` | CI: re-runs the whole pipeline and fails if any dataset CSV is committed | Keep it green |
| `.github/workflows/personalize.yml` | Runs once right after you create your copy: points every Colab badge at YOUR repo | Automatic — nothing to do |
| `requirements.txt` | pandas, numpy, scikit-learn, matplotlib, reportlab, duckdb, huggingface_hub | `pip install -r requirements.txt` |

## 2. How the pipeline fits together

```text
data/raw/content_refresh_anonymized.csv        (30,000 rows × 44 columns)
      │
      │  01_prepare_features.py    fill blanks, add engineered columns, define the label
      ▼
data/processed/refresh_feature_vector.csv      (52 columns)
      │
      │  02_baseline_score.py      transparent hand-rule score + reason codes
      ▼
data/processed/baseline_refresh_queue.csv
      │
      │  03_train_model.py         3 models, client-holdout split, metrics vs the baseline
      ▼
data/processed/model_predictions.csv  +  outputs/model_results.json
      │
      │  04_evaluate_and_export.py blend model + baseline → final ranked queue, charts, report
      ▼
outputs/refresh_queue.csv, outputs/model_report.md, outputs/charts/
      │
      │  05_build_pdf_report.py
      ▼
outputs/flyrank_refresh_model_results.pdf
```

`python scripts/run_all.py` runs all five stages in order (~1 minute).

**The label:** `is_declining_label = (trend_direction == "down")`. Because the label is
derived from `trend_direction`, neither `trend_direction` nor `trend_pct` may ever be a
model feature — notebook 02 shows you exactly what happens if you leak them in.

**The split:** `03_train_model.py` holds out ~20% of *clients* (not rows), so no client's
pages appear in both train and test. When you evaluate your own models, use the same idea.

## 3. Committed vs regenerated

Git deliberately ignores most of what the pipeline writes (`data/processed/`, `outputs/*.json`,
`outputs/refresh_queue.csv`, the PDF). Only three example outputs are committed so you can see
the target shape before running anything. If `git status` stays quiet after a pipeline run,
nothing is wrong — that's the design: **code and reports go in git, data and generated
artifacts don't.**

## 4. The working rhythm

| When | What you do | Where |
|---|---|---|
| Week 1 | Run the pipeline, make your first real discovery | `notebooks/01_first_look_and_discovery.ipynb` |
| Week 2 | Hand rule vs readable model, leakage lesson | `notebooks/02_your_first_readable_model.ipynb` |
| Weeks 3+ | Learn the full-release workflow (DuckDB over ~79M hosted rows), then your lane | `notebooks/03_working_with_the_full_release.ipynb`, then `work/` (copy pipeline pieces in, don't edit `scripts/`) |
| Capstone | Your `work/` folder **is** the deliverable: code, figures, and `capstone_report.md` | `work/` |

**Do I make my own notebook?** Weeks 1-3: no — run the three provided ones and do the "your
turn" cells (save copies to your repo). Capstone and lane work: **yes** — your own notebooks in
`work/notebooks/`, starting with the setup cell from section 5.

Weekly assignments, live events, and every "what done looks like" live on your **portal board** —
this repo is the technical foundation they all build on.

## 5. Build & submit flow

1. Make your own copy: **Use this template → Create a new repository** (public) on the repo
   page — that copy is your workspace, your submission, and your portfolio. (Prefer the
   terminal? `git clone` this repo and push it to an **empty** repo you own — no README tick,
   or the push is rejected.)
2. Share your repo URL as part of **Assignment 1** on the InternHQ board. That's the only thing
   you ever hand over during the track — nothing gets uploaded to the platform.
3. Build everything in `work/`. Keep `scripts/` pristine. **Every new notebook you create
   (weeks 3+) should start with one setup cell:**
   ```python
   %pip install -q duckdb huggingface_hub pandas scikit-learn matplotlib
   ```
   A fresh Colab/Jupyter kernel doesn't have `duckdb` until you install it in the notebook.
   And **never hardcode your Hugging Face token in a cell** — your repo is public. Use
   `getpass` or Colab's Secrets (🔑) panel; leaked tokens get auto-revoked, but don't test it.
4. Keep CI green: it re-runs the pipeline and **fails if any dataset CSV is committed** —
   your fork inherits that protection.
5. Submitting is simple: for every assignment you submit **your repo URL** on its card in your
   portal — and at the end you submit the capstone the same way, with your deployed paper's URL
   in `submission/paper_url.txt` inside the repo. That's the whole journey.

Working in Colab? *File → Save a copy in GitHub* after each session — opened from your
copy's badges, the dialog comes pre-filled (repo, path, branch), so saving is one OK. Also
*File → Save a copy in Drive* so the session doesn't evaporate. Badges acting up? *File →
Open notebook → GitHub tab* → your repo — see `SETUP.md`, Moment 1.

## 6. Working with an AI assistant

This repo ships its own **skill library** for AI coding assistants (Claude Code, Cursor, Codex,
ChatGPT — any of them). Start every task by telling your assistant:

> Read `skills/README.md`, then load the ONE skill this assignment names on its card.

The router in `skills/README.md` maps every task to its skill. Load one skill at a time — never
all of them (your assistant's memory is small, and stuffing it makes it worse, not better).
Using a chat-only assistant in the browser? Open the skill file on GitHub and paste its content
into your chat first. Repo-reading agents find the router automatically through `AGENTS.md` and
`CLAUDE.md` at the repo root.

## 7. FAQ — the five questions everyone asks

**Git won't add my results / my CSV.**
By design — see section 3. Generated artifacts regenerate; datasets never enter git. Your
findings belong in your report and figures, not in committed data files.

**My numbers differ from the committed report.**
The baseline (Precision@50 = 0.240) reproduces exactly. The random-forest number is
**library-version sensitive**: 0.740 on the stack we ship, but roughly 0.68–0.74 across
older numpy/scikit-learn combinations — the picks at the 50th-place boundary shift.
The stable claim is the **~3x lift over the baseline**, not the third decimal. If you see
0.68-ish, your environment resolved older libraries; `pip install -r requirements.txt` in a
fresh venv gets you the shipped stack.

**"Raw input not found" when running the pipeline.**
The starter CSV was deleted or moved. Restore it:
`git checkout -- data/raw/content_refresh_anonymized.csv`

**How do I add or remove a model feature?**
Edit `MODEL_NUMERIC_FEATURES` / `MODEL_CATEGORICAL_FEATURES` in `scripts/ml_utils.py` and
re-run — or, for bigger experiments, copy `03_train_model.py` into `work/` and modify the
copy. Check `docs/data-dictionary.md` first so you don't leak the label.

**Can I put the mentor-provided warehouse release in this repo?**
No. It stays outside git entirely (CI fails any committed CSV anyway). Work with it locally
and commit only code, aggregates, and write-ups — see `DATA_USE.md`.
