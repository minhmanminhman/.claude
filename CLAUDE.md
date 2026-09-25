- Never use em dash, use plain dash "-" instead.
- Do not auto-commit without my instructions.
- Use the Plain English output styles for commit messages. Be concise, DO NOT bloat text, one-liner is prefered.
- Docstrings say what the code does, like API documentation. No results, metrics, progress notes or "why we chose this value". Same rule for comments.
- Technical Priorities: When making technical decisions, prioritize quality, simplicity, robustness, scalability, and long-term maintainability over development speed/estimated cost.
- Bug Fixes: Always start by reproducing the bug in an end-to-end setting to ensure the actual root cause is identified.
- Work in small, shippable units: Break work down into vertical slices and implement one behavior at a time.
- Ground every claim about behavior in the code itself. Docs, docstrings, comments, and READMEs can be stale - read the implementation before drawing a conclusion, and say so when the two disagree.
- NEVER report a value from memory, codebase grounding is a MUST.
- When writing artifacts for human readers, the length should be 300-500 words or 5 minutes read time.
- Prioritize the logic encapsulated than the file growth, human readability over machine readability.

<!-- CODEGRAPH_START -->
## CodeGraph

In repositories indexed by CodeGraph (a `.codegraph/` directory exists at the repo root), reach for it BEFORE grep/find or reading files when you need to understand or locate code:

- **MCP tool** (when available): `codegraph_explore` answers most code questions in one call — the relevant symbols' verbatim source plus the call paths between them, including dynamic-dispatch hops grep can't follow. Name a file or symbol in the query to read its current line-numbered source. If it's listed but deferred, load it by name via tool search.
- **Shell** (always works): `codegraph explore "<symbol names or question>"` prints the same output.

If there is no `.codegraph/` directory, skip CodeGraph entirely — indexing is the user's decision.
<!-- CODEGRAPH_END -->
