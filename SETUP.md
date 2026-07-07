# Setup — ten minutes, at two moments

You do **not** need everything on day one. There are exactly two setup moments in this track:

| When | What | Time |
|---|---|---|
| Before Assignment 1 (Week 1) | GitHub + Colab | ~5 min |
| Before Week 3 | Hugging Face data access | ~5 min |

Do each one right before you need it. Every step below includes the mistake that silently
breaks it — read the ⚠️ lines even if you skip everything else.

---

## Moment 1 — GitHub + Colab (before Assignment 1)

1. **Create a GitHub account** (free) at [github.com/join](https://github.com/join) — skip if you have one.
2. **Make your own copy of this repo** — one click, no git needed: on
   [the starter repo page](https://github.com/flyrank-bih/flyrank-ml-internship-starter), press
   **Use this template → Create a new repository** → public → any name → Create.
   You now own a full copy: the notebooks, the pipeline, your `work/` folder, and the CI
   leak-guard that keeps datasets out of git — all of it travels with you.
   ⚠️ Don't create an empty repo by hand instead — an empty repo has no branch, and Colab's
   *Save in GitHub* **silently does nothing** against it (the dialog just closes).
3. **Open Notebook 01** with the Colab badge in the README. It runs in your browser; nothing
   to install. (The badge opens the shared read-only notebook no matter whose README you
   clicked it in — your work becomes yours at the save step below.)
4. **Save your work**: *File → Save a copy in GitHub* → authorize Colab (pick the **same
   account** that owns your copy) → in the Repository dropdown **switch to YOUR copy** (it
   defaults to the shared repo, which you can't write to) → keep the suggested
   `notebooks/...` path, branch `main` → OK. Colab opens the commit on GitHub — that's your
   proof it worked.
   ⚠️ Colab can only see repos of the GitHub account that authorized it. If your repo
   "doesn't appear," you authorized a different account.
5. **Also**: *File → Save a copy in Drive* — a personal backup so a closed tab never eats an
   hour of work. Never submitted, just yours.

**✅ Done when:** the executed notebook shows up in your copy on github.com. That
**`github.com/you/your-repo`** URL is your submission for Assignment 1 — never a
`colab.research.google.com` or `drive.google.com` link.

---

## Moment 2 — Hugging Face data access (before Week 3)

The full warehouse (~79M rows) is hosted on Hugging Face behind a click-through gate.

1. **Create a Hugging Face account** (free) at [huggingface.co/join](https://huggingface.co/join).
2. **Accept the gate — in the browser, first.** Open
   [`FlyRank/internship-warehouse`](https://huggingface.co/datasets/FlyRank/internship-warehouse),
   fill the short form — put **`FlyRank ML Internship 2026`** as your affiliation — tick the
   terms, **Agree**. Access is instant.
   ⚠️ Order matters: a token created *before* you accept the gate gets `401` errors and
   nothing tells you why.
3. **Create a READ token**: huggingface.co → Settings → **Access Tokens** → Create new token →
   type **Read** → name it (e.g. `internship`) → copy it somewhere safe.
   ⚠️ Read, not Write — the track never needs more, and a leaked read token is harmless
   to you.
4. **Use it in notebooks**: paste it at the `getpass` prompt when a notebook asks, or store it
   in Colab's **Secrets** panel (🔑 icon, name it `HF_TOKEN`).
   ⚠️ **Never type the token into a code cell.** Your repo is public — a hardcoded token
   gets committed with your notebook.

**✅ Done when:** the first cells of Notebook 03 print the table row counts.

---

## The one-account rule (saves an hour of confusion)

- The GitHub account **Colab is authorized on** = the account that **owns your submission repo**.
- The Hugging Face account **that accepted the gate** = the account **whose token you paste**.

Mixing accounts is the root of almost every "it doesn't work" — one of each, used everywhere.
