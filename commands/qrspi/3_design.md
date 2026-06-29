---
description: Design discussion — align on where we are going before planning how
model: opus
argument-hint: "thoughts/qrspi/<id>/"
---

# Design — Where Are We Going?

Create a ~200-line design document that captures the current state, desired end state, design decisions, and patterns to follow. This is the **lowest-cost point for direction changes** — get alignment here before investing in detailed planning.

## Input

Read `$ARGUMENTS/task.md`, `$ARGUMENTS/questions.md`, and `$ARGUMENTS/research.md`.

## Process

1. **Read all three artifacts fully.** `task.md` tells you what we're building. `research.md` tells you what exists. Understand both before proceeding.

2. **Targeted exploration**: If the research revealed areas that need deeper investigation for design decisions, spawn **codebase-pattern-finder** or **codebase-analyzer** agents to examine specific patterns or approaches.

3. **Present open questions and wait for answers.** Before writing anything, you MUST:
   - List 3-5 design questions that require human judgment
   - Present options with trade-offs for each, grounded in what the research found
   - Wait for the user to respond

   Example:
   ```
   Before I write the design document, I need your input:

   **Q1: Data model approach**
   The research shows two patterns in the codebase:
   - Option A: [pattern from research.md] — used in [file:line], simpler but less flexible
   - Option B: [pattern from research.md] — used in [file:line], more complex but extensible
   Which fits this use case?

   **Q2: ...**
   ```

   Do NOT skip this step. Do NOT write the design document without user input.

4. **Write `design.md`** (~200 lines) to the artifact directory:

   ```markdown
   # Design Discussion

   ## Current State
   [What exists today, grounded in research findings with file:line refs]

   ## Desired End State
   [What we're building and how to verify it's correct]

   ## Patterns to Follow
   [Existing codebase patterns the implementation should match, with file:line refs.
   Flag any patterns the research found that should NOT be followed.]

   ## Design Decisions
   1. **[Decision name]**: [chosen option] — [why]
   2. **[Decision name]**: [chosen option] — [why]
   ...

   ## What We're NOT Doing
   [Explicit scope boundaries to prevent creep]

   ## Open Risks
   [Anything uncertain that might surface during implementation]
   ```

5. **Hard review loop (codegraph-grounded, up to 3 rounds).** Before showing the user anything, harden the draft against the real codebase.

   **Precondition:** confirm a `.codegraph/` index exists at the repo root (`codegraph_explore` depends on it). If absent, STOP and tell the user: "Design review requires a codegraph index — run `codegraph init` in the target repo, then re-run /qrspi/3_design." Do not review without it.

   For each round `N` from 1 to 3:
   - Spawn the **qrspi-codegraph-reviewer** agent with: `target_doc` = `$ARGUMENTS/design.md`, `artifact_dir` = `$ARGUMENTS`, `repo_root`, `round` = `N`, and (rounds 2-3) the prior round's findings.
   - Persist its output to `$ARGUMENTS/reviews/design-round-N.md`.
   - If verdict is **SHIP** → exit the loop.
   - If **NO-SHIP** → revise `design.md` to address every 🔴 blocker and 🟡 major finding (ground each fix in research/codegraph; do not hand-wave), then continue to round `N+1`.

   If round 3 still returns NO-SHIP, do NOT loop further. Surface the unresolved findings to the user and let them decide: approve as-is, run another round, or edit directly.

6. **Present the hardened design to the user** for review, noting the review verdict and how many rounds it took. Iterate until they approve.

## Output

- File written: `thoughts/qrspi/<id>/design.md`
- Tell the user: "Next: run `/qrspi/4_structure thoughts/qrspi/<id>/`"

## Rules

- ~200 lines max. This is a steering document, not a specification.
- Every pattern reference must cite `file:line` from the research.
- You MUST ask questions and wait before writing. No exceptions.
- "Patterns to Follow" is critical — call out both good and bad patterns found in the codebase.
- "What We're NOT Doing" prevents scope creep downstream.

## When to Go Back

If the research is missing critical information needed for design decisions — the questions missed an important area of the codebase — tell the user and suggest re-running `/qrspi/1_question` and `/qrspi/2_research` to fill the gap before proceeding with an incomplete design.
