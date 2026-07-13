# Setup — ten minutes, at two moments

You do **not** need everything on day one. There are exactly two setup moments in this track:

| When | What | Time |
|---|---|---|
| Before Assignment 1 (Week 1) | GitHub + Colab | ~5 min |
| Before Week 3 | Hugging Face data access | ~5 min |

Do each one right before you need it — with ONE exception worth doing on day one: create your free Hugging Face account and request access to the [internship warehouse dataset](https://huggingface.co/datasets/FlyRank/internship-warehouse) now. Approval is instant, and the data will already be waiting when Week 3 needs it (the token itself stays a Moment-2 job). Every step below includes the mistake that silently
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
3. **Give it ~30 seconds, then refresh your new repo's page.** A tiny automatic commit
   ("Point Colab badges at this copy") lands right after creation — it rewires every Colab
   badge in YOUR copy so notebooks open from your repo, with your saved work, and save back
   to it with everything pre-filled.
   ⚠️ Always click badges in **your** copy's README, not on the shared starter page — the
   shared page's badges open read-only previews you can't save to directly.
4. **Open Notebook 01** with its Colab badge in **your** README. It runs in your browser;
   nothing to install.
5. **Save your work**: *File → Save a copy in GitHub* → authorize Colab (pick the **same
   account** that owns your copy) → the dialog is already pre-filled with your repo, the
   right path, and branch `main` → **OK**. Colab opens the commit on GitHub — that's your
   proof it worked. Leave "Include a link to Colaboratory" ticked — it keeps an open-in-Colab
   badge at the top of the saved notebook.
   ⚠️ Colab can only see repos of the GitHub account that authorized it. If your repo
   "doesn't appear," you authorized a different account.
6. **Also**: *File → Save a copy in Drive* — a personal backup so a closed tab never eats an
   hour of work. Never submitted, just yours.

**✅ Done when:** the executed notebook shows up in your copy on github.com **and, when you
open the file there, the cell outputs are visible under the cells.** No outputs means Colab
saved an unrun copy — back in Colab: **Runtime → Run all**, then save again. That
**`github.com/you/your-repo`** URL is your submission for Assignment 1 — never a
`colab.research.google.com` or `drive.google.com` link.

**Badges opening the shared repo instead of yours?** (You made your copy before the badge
rewiring existed, or Actions is turned off on your repo.) Use Colab's built-in opener — same
result, two more clicks: **File → Open notebook → GitHub tab** → paste
`github.com/you/your-repo` → pick the notebook. Save is pre-filled exactly the same way, and
Colab's **Recent** tab remembers it from then on.

**Seeing an OLD version of your notebook?** Don't panic — your work is safe. Colab sometimes
shows a cached copy; the badges carry a cache-buster to prevent this, but if it ever happens
anyway: check your repo on github.com first (your saved version is there), then reopen via
the badge or **File → Open notebook → GitHub tab**.

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
