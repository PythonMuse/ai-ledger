# CLAUDE.md

Guidance for Claude Code working in this repository.

## What this project is

This repo (**ai-ledger**, published at [github.com/PythonMuse/ai-ledger](https://github.com/PythonMuse/ai-ledger)) is PythonMuse's flagship publication: practical, article-by-article guidance on using AI tools (primarily Claude Code) for accounting, finance, and business workflows. It is the source material other PythonMuse projects — including [PythonMuse-Training](https://github.com/PythonMuse) courses — teach from, so accuracy, tone, and terminology set here should be treated as canonical, not a draft to be improved on elsewhere.

## Our mission

PythonMuse exists to educate, inspire, and equip accounting, finance, and business professionals for the era of AI and automation. The goal is to make AI practical, approachable, responsible, and useful for real professionals — especially those trying to understand how AI can support their work without losing judgment, ethics, controls, or professional skepticism.

When in doubt, use this as the decision filter: **does this help professionals learn, feel encouraged, and become better prepared for the AI-powered future?** If yes, it's likely aligned with PythonMuse.

## Tone and brand

Every article, script, and piece of content should feel:

- Educational, not salesy
- Practical, not theoretical
- Encouraging, not intimidating
- Professional, but still human
- Curious, humble, and responsible

We are not here to shame people for being behind on AI — we are here to help them take the next step. Avoid overhyped AI claims, fear-based messaging, overly technical language without explanation, and anything that implies AI replaces professional judgment.

## Operating boundaries

- Draft freely; do not publish, push, or send anything externally without approval (Lana/Patrick Toohey).
- Don't upload confidential, sensitive, or restricted information (internal strategy, financial data, client/vendor details, credentials, unpublished drafts) into this or any AI tool — see `docs/rules-of-the-road.md` in the PythonMuse-Training repo if you need the full definitions.
- AI output here is a draft input, not a finished deliverable — human review owns the final call, especially anything presented as accounting, tax, legal, or compliance guidance (this repo carries the "educational purposes only, not professional advice" disclaimer in `README.md`).
- Sample data must be safe to publish: synthetic or anonymized, never real client/financial data.

## Repo layout

- `articles/<NN-topic-name>/` — one self-contained folder per article: `README.md` (the article), `visuals/` (charts), `data/` (sample CSVs), `generate_visuals.py` (script to reproduce the charts). This is the core content of the repo.
- `data_raw/` — raw/working data that hasn't been shaped into an article's `data/` folder yet.
- `templates/`, `examples/` — reusable patterns (skills, workings templates, trust-but-verify checklists) referenced across articles.
- `community/` — `roadmap.md` and `ideas-wanted.md`, the public-facing plan and open asks.
- `docs/` — brand assets (`PythonMuseLogo.PNG`, brand color guide, `PythonMuse_BrandSample.xlsx`).
- `scripts/` — repo-level utilities (e.g. newsletter/email preview tooling), not article-specific.
- `.claude/commands/` — `/publish-article` (standard article format + audit checklist) and `/update-status` (refresh `StatusUpdate.md`).
- `NOTES.md`, `StatusUpdate.md`, `plan.md`, `backlog.md` — running session/project state; read these for current context before assuming what's done vs. outstanding.

## Working conventions

- New articles are drafted on a dedicated `article/NN-slug` branch created from `main` — never committed straight to `main`. Once the draft is ready, Claude pushes that branch to `origin` (with explicit confirmation, per Operating boundaries below) and stops there: opening the pull request on GitHub.com, contributor review, and merging into `main` are done by the user. This is separate from the external-contributor fork+PR flow described in `CONTRIBUTING.md`.
- New articles follow the numbered folder pattern above; update the article index table in root `README.md` when adding one.
- Run `/publish-article` against a new or edited article before treating it as ready — it enforces the standard title/byline/date/related-links format.
- Byline is `PythonMuse LLC` for all new articles (articles 01–15 use `Svetlana Toohey` — leave those as-is).
- Content license is CC BY-NC-SA 4.0; code (`.py` files) is MIT — see `LICENSE` / `LICENSE-CODE`. Don't introduce content or code that can't carry those licenses.
- Run `/update-status` at the end of a session to keep `StatusUpdate.md` current for the next session.
