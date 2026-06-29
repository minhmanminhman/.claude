---
description: Structure outline — vertical slices with test checkpoints
model: opus
argument-hint: "thoughts/qrspi/<id>/"
---

# Structure — How Do We Get There?

Create a ~2-page structure outline that breaks the design into **vertical slices** — each independently testable. Show the signatures, types, and phase boundaries — not the full implementation.

## Input

Read `$ARGUMENTS/design.md` and `$ARGUMENTS/research.md`.

## Process

1. **Read both artifacts fully.**

2. **Break the work into vertical slices.** Each slice delivers end-to-end functionality:
   - Crosses all necessary layers (database, service, API, UI) for that slice
   - Can be tested independently after implementation
   - Has a clear verification checkpoint

   **Vertical** (correct):
   > Phase 1: Add the "reticulate" endpoint — migration, store method, API handler, basic UI button. Test: endpoint returns 200, button triggers call.

   **Horizontal** (wrong):
   > Phase 1: All database migrations. Phase 2: All service methods. Phase 3: All API endpoints. Phase 4: All UI changes.

3. **Define the phase order.** Earlier phases should establish foundations that later phases build on. If Phase 3 fails, Phases 1-2 should still be independently valuable.

4. **For each phase, list**:
   - What it accomplishes (1-2 sentences)
   - Files affected
   - Key type signatures or interface changes
   - How to verify it works (automated command + what to check manually)

5. **Write `structure.md`** to the artifact directory:

   ```markdown
   # Structure Outline

   ## Approach
   [1-2 sentences: the implementation strategy from design.md, condensed]

   ## Phase 1: [Name]
   [What this phase delivers end-to-end]

   **Files**: `path/to/file.ext`, `path/to/other.ext`
   **Key changes**:
   - `functionName(param: Type): ReturnType` — new/modified
   - `NewType { field: Type }` — new type

   **Verify**: [project test command] passes; [manual check description]

   ---

   ## Phase 2: [Name]
   ...

   ## Testing Checkpoints
   [Summary of what should be true after each phase, useful for resuming if context resets]
   ```

6. **Hard review loop (codegraph-grounded, up to 3 rounds).** Before showing the user anything, harden the outline against the real codebase.

   **Precondition:** confirm a `.codegraph/` index exists at the repo root. If absent, STOP and tell the user: "Structure review requires a codegraph index — run `codegraph init` in the target repo, then re-run /qrspi/4_structure." Do not review without it.

   For each round `N` from 1 to 3:
   - Spawn the **qrspi-codegraph-reviewer** agent with: `target_doc` = `$ARGUMENTS/structure.md`, `artifact_dir` = `$ARGUMENTS`, `repo_root`, `round` = `N`, and (rounds 2-3) the prior round's findings.
   - Persist its output to `$ARGUMENTS/reviews/structure-round-N.md`.
   - If verdict is **SHIP** → exit the loop.
   - If **NO-SHIP** → revise `structure.md` to address every 🔴 blocker and 🟡 major (re-ground phase boundaries against the real call graph / blast radius), then continue to round `N+1`.

   If round 3 still returns NO-SHIP, surface the unresolved findings to the user: approve as-is, run another round, or edit directly.

7. **Present the hardened outline to the user**, noting the verdict and round count, and wait for feedback. Common adjustments:
   - Reordering phases
   - Splitting a phase that's too large
   - Adding a testing phase between sensitive phases
   - Requesting more detail on a specific phase

## Output

- File written: `thoughts/qrspi/<id>/structure.md`
- Tell the user: "Next: run `/qrspi/5_plan thoughts/qrspi/<id>/`"

## Rules

- ~2 pages max. If it's longer, you're writing the plan, not the outline.
- Vertical slices, not horizontal layers. Every phase must cross all relevant layers.
- Signatures and types, not full implementation. Show WHAT changes, not HOW.
- Each phase must have a verification checkpoint.
- If the design calls for something that can't be sliced vertically, note it explicitly.

## When to Go Back

If you discover the design missed a critical constraint or made a decision based on incorrect assumptions about the codebase, tell the user and suggest re-running `/qrspi/3_design` rather than working around a flawed design.
