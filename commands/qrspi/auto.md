---
description: Unattended run from structure to a reviewed, uncommitted diff
model: opus
argument-hint: "thoughts/qrspi/<id>/"
---

# Auto - From Approved Design to Reviewed Diff

Run every stage after an approved design without stopping for the user: structure, plan, test-first implementation, refactor, a hard code review by a different model, fixes, and cleanup. Nothing is committed. The run ends with `report.md` and an uncommitted diff for the user to review.

```
structure + review -> plan -> per phase: red -> green -> mutation check -> refactor -> review 1 -> fix 1 -> review 2 -> fix 2 -> cleanup -> report
```

## Input

`$ARGUMENTS` is the artifact directory with `task.md`, `research.md`, and an approved `design.md`.

## Preconditions

Check these before anything else. If one fails, tell the user what to fix and stop. After this point the run never stops for the user.

- `design.md` has a `## Seams Under Test` section with at least one seam.
- A `.codegraph/` index exists at the repo root.
- On a fresh start only (no `Baseline:` line in `decisions.md`): the working tree is clean outside `thoughts/` (`git status --porcelain -- . ':!thoughts'` prints nothing).

## Start or Resume

Find the first incomplete stage from the files on disk:

1. `plan.md` has an `## Auto Run` section: read `Baseline:` from it. Continue at the first phase with unchecked automated items that is not marked `> BLOCKED`, or else at the first unchecked `## Auto Run` box.
2. `plan.md` exists without `## Auto Run`: append that section (see `5_plan.md` Unattended Mode) and start at implement.
3. `structure.md` exists and `reviews/` holds its last round as SHIP, or `decisions.md` logs the round 3 fix: start at plan.
4. Otherwise start at structure. On a fresh start, create `decisions.md` with `Baseline: <git rev-parse HEAD>`.

## decisions.md

Every choice a stage would have asked the user is logged here, one entry each:

```markdown
## <stage>: <short title>
- **Context**: what needed an answer
- **Options**: what was considered
- **Chosen**: the option taken
- **Why**: the grounded reason, with `file:line`
- **Flag**: unconfirmed seam | blocked | design concern | unfixed finding | none
```

## Stages

1. **Structure.** Follow `4_structure.md` with its Unattended Mode.
2. **Plan.** Follow `5_plan.md` with its Unattended Mode.
3. **Implement.** Follow `7_implement.md` with its Unattended Mode: for each phase, `tester` writes red tests (using scrap tests to probe first), you write the green code, `tester` runs the mutation check, then the full suite runs.
4. **Refactor.** Load the `refactor` skill. Scope: files changed since the baseline, plus direct callers and callees of changed symbols (`codegraph_callers`, `codegraph_callees`, one hop). Behavior must not change, and test assertions stay as they are. Before each step, copy the files it touches to a temp directory outside the repo. Run the full suite after the step, and restore the copies if it fails. This replaces the skill's "commit before and after" rule. Check `Refactor`.
5. **Fable review round N** (N = 1, 2). Spawn `qrspi-fable-reviewer` with `artifact_dir`, `repo_root`, `baseline`, `round` = N and, for round 2, the round 1 findings with how each was resolved. Save its output to `reviews/code-round-N.md`. Check the box.
6. **Fix round N.** Load the `receiving-code-review` skill and check every finding against the code by reproducing its scenario.
   - A confirmed behavior bug: `tester` writes a regression test at a listed seam (red), you fix it (green), and `tester` runs the mutation check.
   - A confirmed finding with no behavior change: fix it directly.
   - A rejected finding: write the reason under `## Response` in `reviews/code-round-N.md`.
   - A finding still failing after 3 attempts: log it with flag `unfixed finding`.

   Check the box. Round 2 fixes are not reviewed again. If round 1 returns `FINDINGS: none`, check fix round 1 and both round 2 boxes with `(skipped: round 1 clean)`.
7. **Cleanup.** Follow `8_cleanup_docstrings.md` with its Unattended Mode. Check `Cleanup`.
8. **Report.** Write `report.md` (below), post the chat summary, and check `Report`.

## Verification Gates

Use the project's test, lint and type check commands named in `plan.md`.

- After each green: the phase's tests. After each phase: the full suite.
- After refactor, after each fix round, and after cleanup: the full suite, lint and type checks.
- A failure that remains after 3 fix attempts is logged and listed in the report, and the run continues.

## report.md

```markdown
# Auto Run Report

Baseline: <sha>. Structure review: <verdict> in <n> rounds. Code review: round 1 <verdict>, round 2 <verdict>.

## Needs Your Attention
[Every decisions.md entry whose flag is not none, failing gates, unfixed findings, manual verification items left unchecked]

## Phases
| Phase | Red | Green | Mutation (tool or hand, killed/total) | Status |

## Code Review
- Fixed: `file:line` - finding
- Rejected: `file:line` - finding - reason

## Unattended Decisions
[One line per decisions.md entry: title and chosen option]

## Cleanup
[Comment rewrites, scrap files deleted, untracked files left in place]

## Files Changed
[`git diff --stat <baseline>` plus new untracked files]

## Verify
[Commands to run, and manual checks from plan.md]
```

The chat summary leads with the outcome, lists "Needs Your Attention", and links `report.md`. Then tell the user: "Next: review the diff, commit, then run `/qrspi/9_pr thoughts/qrspi/<id>/`."

## Rules

- Never commit, push, stash, or run `git checkout`, `git restore` or `git reset` on files. The work is uncommitted.
- Never stop for the user after the preconditions. Log the choice and continue.
- Run at most 3 sub-agents at a time.
- Never remove or move `thoughts/qrspi` docs.
- Checkboxes in `plan.md` are the run's state. Update them as each step finishes.
