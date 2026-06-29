---
description: Grill the user about a feature, grounded in CLAUDE.md + codegraph, until intent and agent understanding align
model: opus
argument-hint: "<feature brief, or leave blank to be prompted>"
---

# Grill — Align Intent Before the Pipeline

The pipeline's entry point. The user briefs a feature; you interrogate it — grounded in the project's own docs and code structure — until your understanding and their intention provably match. Output is a tight `task.md` that the rest of QRSPI builds on.

## Input

The user's feature brief in `$ARGUMENTS` (a sentence, a paragraph, a ticket). If empty, ask the user to brief the feature in 2-3 sentences before doing anything else.

## Grounding (read before grilling)

1. **Read `CLAUDE.md`** (repo root, and any nested CLAUDE.md in directories the brief touches) fully. It encodes the project's conventions, constraints, and vocabulary — your questions must respect them.

2. **Precondition — codegraph index:** confirm a `.codegraph/` index exists at the repo root. If absent, STOP: "Grilling is grounded in codegraph — run `codegraph init` in the target repo first, then re-run /qrspi/0_grill_with_docs." Do not grill ungrounded.

3. **Query `codegraph_explore`** on the areas the brief names — find the symbols, call paths, and blast radius that the feature would touch. You grill from evidence, not from generic templates.

## Process — relentless, one question at a time

Interrogate until intent is unambiguous. **Ask ONE question at a time and wait for the answer** — batching questions is bewildering and produces shallow answers.

For each question:
- Ground it in what you found ("CLAUDE.md says X; codegraph shows the auth flow lives in `mw/auth.rs:40` and routes through `verify()` — does your feature extend that path or replace it?").
- Offer your recommended answer and the trade-off, so the user can correct a wrong assumption cheaply.
- Walk the tree: resolve dependencies between decisions one at a time. Don't move on while an answer is ambiguous.

Cover, at minimum:
- **Exact intent** — what the feature does, and what "done" means observably.
- **Boundaries** — what it explicitly does NOT do.
- **Codebase fit** — which existing patterns/symbols it extends vs. introduces, grounded in codegraph.
- **Constraints** — performance, compatibility, conventions from CLAUDE.md.
- **Unknowns** — anything you cannot ground; flag it for the Research phase rather than guessing.

Stop grilling only when you can restate the feature back to the user and they confirm it matches their intent.

## Output

1. **Determine the artifact directory** (you own its creation):
   - With ticket number: `thoughts/qrspi/PROJ-1234-brief-description/`
   - Without ticket: `thoughts/qrspi/YYYY-MM-DD-brief-description/`
   - Create it: `mkdir -p thoughts/qrspi/<id>/`

2. **Write `task.md`** — the aligned feature brief (2-4 sentences: what's being built and why, reflecting the grilled understanding, not the user's raw first words).

3. **Write `grill-notes.md`** — the decisions, assumptions, and explicitly-deferred unknowns surfaced during grilling, so later phases inherit the reasoning:

   ```markdown
   # Grill Notes

   ## Aligned Intent
   [the restated feature the user confirmed]

   ## Decisions
   - [decision]: [chosen answer] — [why]

   ## Boundaries (NOT doing)
   - [explicit non-goal]

   ## Codebase Grounding
   - [symbol / file:line from codegraph the feature touches]

   ## Deferred to Research
   - [unknown the grill could not resolve]
   ```

4. Tell the user: "Aligned. Next: run `/qrspi/1_question thoughts/qrspi/<id>/`"

## Rules

- Read CLAUDE.md and query codegraph BEFORE the first question. Ungrounded grilling is generic and wastes the user's time.
- One question at a time. Always wait. Always offer a recommended answer.
- `task.md` reflects the *aligned* understanding, not the raw brief.
- Do not write `questions.md` — that is `1_question`'s job. You only align intent and persist it.
- If the brief turns out trivial (no real ambiguity, no design judgment needed), say so — QRSPI is for complex work.
