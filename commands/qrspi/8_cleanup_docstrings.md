---
description: Strip dev-process residue from docstrings/comments and tidy temp planning docs before the PR
argument-hint: "thoughts/qrspi/<id>/"
---

# Cleanup Docstrings — Make Comments Stand on Their Own

After implementation, docstrings and comments often carry dev-process residue — `Phase 2`, `Step 3`, pointers to `thoughts/qrspi/.../plan.md`, `Decision:` narration, AI-authorship tags. This step detects that residue on the branch, you rewrite the comments to be self-contained, then optionally remove the temp planning docs before opening the PR.

**Detection is scripted; editing is judgment + approval-gated.** The driver only *reports* candidates — it never edits. You filter false positives, draft rewrites, and **propose the diff before touching any file**.

## Input

The artifact directory is `$ARGUMENTS`. Run from the implementation worktree/branch (the same place `7_implement` ran).

## Process

1. **Report candidates** (three-dot diff = since merge-base with the auto-detected base branch):

   ```bash
   node ~/.claude/commands/qrspi/driver.mjs
   ```

   Machine-readable form for building the diff proposal:

   ```bash
   node ~/.claude/commands/qrspi/driver.mjs --json
   ```

   Different base branch: `node ~/.claude/commands/qrspi/driver.mjs --base develop`.

   The report groups findings by tag (`phase`, `temp-ref`, `decision`, `ai-tag`), each line `file:line  <comment text>`, plus a `temp planning docs` block listing `thoughts/qrspi` docs the branch touched.

2. **Per finding — filter, then rewrite:**
   - **Filter.** The harness flags candidates, not verdicts. Keep domain uses — a comment where "decision"/"phase" describes what the code *is* (e.g. a field named `phase`, a state machine step) is not residue. Leave it.
   - **Rewrite to self-contained.** Drop the dev pointer, keep the meaning. A comment that needs a temp planning doc to be understood is exactly the non-independent case to clean.

3. **Propose the full diff and wait for approval** before editing.

4. **After approval, apply the edits.**

5. **Temp planning docs.** If the driver listed `thoughts/qrspi` docs, offer to remove or archive them before the PR:
   - Confirm the exact list with the user.
   - On approval: `git rm` them (or `git mv` to an archive location if they prefer to keep history). Deletion is irreversible-ish — never remove without explicit confirmation.
   - If the user wants the audit trail kept, skip this step.

## Output

- Docstrings/comments rewritten to stand on their own (approval-gated)
- Temp planning docs removed/archived if the user approved
- Tell the user: "Next: run `/qrspi/9_pr thoughts/qrspi/<id>/`"

## Rules

- The driver never edits — it reports. All edits are yours, proposed as a diff first.
- Filter before rewriting: keep comments where the matched word is domain meaning, not dev residue.
- Bare permanent-doc pointers (e.g. `CLAUDE.md`, a `docs/foo.md` link with no phase/step word) are fine — keep them.
- Never `git rm` temp docs without explicit user confirmation of the exact list.
- Scope is the branch's changed code files only. A docstring on an unchanged file is out of scope by design.

## Troubleshooting

- `fatal: ambiguous argument '<base>...HEAD'` → the base ref doesn't exist locally. Use an existing branch (`git branch -a`) or fetch it.
- `0 code files scanned` → the branch has no changed code files vs base, or you're on the base branch itself.
- `node: command not found` → requires Node ≥ 18. Install Node or run the detection manually with grep over the changed files.
