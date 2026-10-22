- Never use em dash, use plain dash "-" instead.
- Do not auto-commit without my instructions.
- Use the Plain English output styles for commit messages. Be concise, DO NOT bloat text, one-liner is prefered.
- Docstrings say what the code does, like API documentation. No results, metrics, progress notes or "why we chose this value". Same rule for comments.
- Technical Priorities: When making technical decisions, prioritize quality, simplicity, robustness, scalability, and long-term maintainability over development speed/estimated cost. Prioritize the logic encapsulated than the file growth, human readability over machine readability.
- Bug Fixes: Always start by reproducing the bug in an end-to-end setting to ensure the actual root cause is identified.
- Work in small, shippable units: Break work down into vertical slices and implement one behavior at a time.
- Ground every claim about behavior in the code itself. Docs, docstrings, comments, and READMEs can be stale - read the implementation before drawing a conclusion, and say so when the two disagree. NEVER report a value from memory, codebase grounding is a MUST.
- Show, don't only tell, and build the picture up diagram by diagram. Open the diff, the code, or the debugger when that is the fastest way to land it. Draw when a picture lands faster than words. For anything with three or more moving parts, do not draw one diagram with all of them at once. Draw a short series instead, where each diagram redraws the last and adds a single part, so the reader watches the system assemble. A single all-at-once diagram, especially one saved for the end, is a reference, not teaching. Concretely, to teach a flow from A to B to C, draw it three times. First A to B. Then redraw and add C. Then redraw and add the return edge or the next piece. Match the medium to the idea, and use both kinds when both help. A diagram fits a flow or structure where the labels carry the meaning. In terminal replies, draw diagrams as plain-text box art in a code block. Use Mermaid only in files or pages that render it. When the idea is spatial, like layout, overlap, scroll position, or a before and after, reach for the image-generation tool and draw it marker-on-whiteboard style with a few short labels, since image models garble long text. Generate that picture, don't settle for describing it in words. The build-up rule holds for generated images too. A single simple point needs no figure.
- Spawn at most 3 sub-agents.

<!-- CODEGRAPH_START -->
## CodeGraph

In repositories indexed by CodeGraph (a `.codegraph/` directory exists at the repo root), reach for it BEFORE grep/find or reading files when you need to understand or locate code:

- **MCP tool** (when available): `codegraph_explore` answers most code questions in one call — the relevant symbols' verbatim source plus the call paths between them, including dynamic-dispatch hops grep can't follow. Name a file or symbol in the query to read its current line-numbered source. If it's listed but deferred, load it by name via tool search.
- **Shell** (always works): `codegraph explore "<symbol names or question>"` prints the same output.

If there is no `.codegraph/` directory, skip CodeGraph entirely — indexing is the user's decision.
<!-- CODEGRAPH_END -->
