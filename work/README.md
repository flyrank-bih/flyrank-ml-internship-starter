# work/ — your space

Everything you build lives here: lane experiments, notebooks, figures, and your capstone
report. The rest of the repo is the shared reference; this folder is yours.

## Rules of the road

1. **Copy, don't edit.** Need to change the pipeline? Copy the script here
   (e.g. `work/scripts/03_train_model_v2.py`) or adjust the feature lists in
   `scripts/ml_utils.py`. The reference pipeline in `scripts/` stays pristine — it's the
   baseline you compare against, and reviewers expect to find it unchanged.
2. **No datasets in git.** CSVs inside `work/` are gitignored, and CI fails if any dataset
   CSV is committed anywhere in the repo. Small summary tables belong in your report as
   markdown, not as data files.
3. **Stay reproducible.** Fix your random seeds and note them in your report. Someone with a
   fresh clone should be able to re-run your work from your instructions alone.
4. **Public-safety language.** Everything here may end up public with your submission:
   observed / measured / directional / decision-support — no client-identifying details,
   no causal claims without a design (see `DATA_USE.md`).

## Suggested layout

```text
work/
  notebooks/            your experiment notebooks
  scripts/              copied + modified pipeline pieces
  figures/              charts for your report
  capstone_report.md    your capstone write-up (start from the template)
```

## Capstone

Copy `capstone_report_template.md` to `capstone_report.md` and fill it in as you go — it
mirrors the eight axes your work is graded on, so writing it early keeps you honest.

## Your assignment index

Your skeleton notebooks are already in `notebooks/` — one per assignment, pre-named.
Tick them off as you go; this table is the map of your work (each badge opens the notebook
in Colab, straight from your repo):

| Notebook | Assignment | Open | Status |
|---|---|---|---|
| `notebooks/w01_research_question.ipynb` | ML-02 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flyrank-bih/flyrank-ml-internship-starter/blob/main/work/notebooks/w01_research_question.ipynb) | ☐ |
| `notebooks/w02_ml_task_framing.ipynb` | ML-03 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flyrank-bih/flyrank-ml-internship-starter/blob/main/work/notebooks/w02_ml_task_framing.ipynb) | ☐ |
| `notebooks/w03_data_contract.ipynb` | ML-04 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flyrank-bih/flyrank-ml-internship-starter/blob/main/work/notebooks/w03_data_contract.ipynb) | ☐ |
| `notebooks/w03_feature_leakage_check.ipynb` | ML-05 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flyrank-bih/flyrank-ml-internship-starter/blob/main/work/notebooks/w03_feature_leakage_check.ipynb) | ☐ |
| `notebooks/w04_signal_audit.ipynb` | ML-06 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flyrank-bih/flyrank-ml-internship-starter/blob/main/work/notebooks/w04_signal_audit.ipynb) | ☐ |
| `notebooks/w04_baseline_score.ipynb` | ML-07 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flyrank-bih/flyrank-ml-internship-starter/blob/main/work/notebooks/w04_baseline_score.ipynb) | ☐ |
| `notebooks/w05_model.ipynb` | ML-08 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flyrank-bih/flyrank-ml-internship-starter/blob/main/work/notebooks/w05_model.ipynb) | ☐ |
| `notebooks/w06_validation_audit.ipynb` | ML-09 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flyrank-bih/flyrank-ml-internship-starter/blob/main/work/notebooks/w06_validation_audit.ipynb) | ☐ |
| `notebooks/w07_action_playbook.ipynb` | ML-10 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flyrank-bih/flyrank-ml-internship-starter/blob/main/work/notebooks/w07_action_playbook.ipynb) | ☐ |
| `notebooks/capstone.ipynb` | ML-11 (the paper mirrors it) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flyrank-bih/flyrank-ml-internship-starter/blob/main/work/notebooks/capstone.ipynb) | ☐ |

When your paper is deployed, put its exact URL in `../submission/paper_url.txt` (one line).
