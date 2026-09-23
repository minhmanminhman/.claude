---
name: explain
description: "Write an explainer that builds real intuition, using the ADEPT method (Analogy, Diagram, Example, Plain-English, Technical) from BetterExplained. Use when the user asks to explain, teach, or unpack a concept, asks \"why does X work\", \"how does X actually work\", \"what is X really\", \"walk me through X\", asks for an intuitive or from-scratch explanation of a formula, model, algorithm, or protocol, or asks for a walkthrough of an unfamiliar codebase, module, or system. Produces a Markdown file - or HTML when the idea needs a real diagram - in wherever the repo keeps its notes. Not for one-line factual answers, and not for multi-session curricula (use teach for those)."
---

<!-- argument-hint: [concept, file, or module to explain] -->

# Explain

Turn a concept into an explainer that survives months, not minutes. Blurry to sharp: a rough analogy first, sharpened until the technical form is covered.

The failure this skill exists to prevent: opening with the rigorous definition. That definition is the **most advanced step of thought, not the starting point**. Nobody teaches a child that a cat is `ACATACATACAT`.

## Workflow

1. **Find the seed.** Where was this idea first used? What problem was its inventor actually stuck on? The historical motivation is almost always the analogy you want. For code, the seed is the constraint the module exists to satisfy - read the code and its git history, not just its names.
2. **Draft in the ADEPT order** (see below). Write in pencil: rough analogy, then sharpen.
3. **Cut like a cartoonist.** Exaggerate the one feature that makes the idea what it is. Drop everything else. Photorealism misses the point.
4. **Pick the medium** (see Output).
5. **Run the gate.** Do not deliver until it passes.

## The five stages

Budget by concept size, not a global word cap. One idea: a tight page. A system walkthrough: as long as the parts demand. Every stage appears, even if a stage is two sentences.

**A - Analogy.** Open here. Ground it in something the reader already owns. "Imaginary numbers are a rotation into the second dimension." "The Fourier transform filters a smoothie back into its ingredients." An analogy may be wrong and still useful - it is a raft, not a bridge. State its limit when the limit matters, then move on. Never apologise for it twice.

**D - Diagram.** Mandatory. Half the brain is vision. Degrade gracefully: SVG in HTML, mermaid where it renders, ASCII in a terminal. If the idea is genuinely non-visual, say so in one line and show the shape of the data instead - a small table, a before/after pair. See [references/diagrams.md](references/diagrams.md).

**E - Example.** One concrete case with real numbers or real values from the actual codebase. Not "consider a function f". A 3-4-5 triangle, a $100 deposit, one order hitting one price level, one request through the handler. Walk it end to end.

**P - Plain-English.** Say the idea in a sentence a competent outsider understands. If you cannot, you have not finished understanding it - go back to step 1.

**T - Technical.** Now the formula, the type signature, the invariant, the API contract. Landing here is the point: the reader arrives at rigour already knowing what it means.

## Output

Resolve the destination before writing:

- **Where.** Follow the repo's existing convention - look for `docs/`, `notes/`, `research/`, or wherever explainers already live, and match it. If nothing exists, ask before creating a new top-level directory. Name the file `explain-{topic}.md`.
- **Which format.** Markdown by default. Write HTML instead when the diagram carries the explanation and ASCII or mermaid would lose it - anything geometric, anything with overlapping regions, anything where position encodes meaning. HTML stays a local file. Publish as an Artifact only when the user asks, and load `artifact-design` first if so.

## The gate

Before handing the file over, check every line. Fix what fails, then report the result in one sentence.

- [ ] The first paragraph is an analogy or a concrete question, **not** a definition.
- [ ] A diagram exists, or one line justifies its absence.
- [ ] At least one example runs on real numbers or real code, start to finish.
- [ ] A one-sentence plain-English statement of the idea appears before the formal one.
- [ ] The technical form appears - the explainer lands on rigour, not short of it.
- [ ] The scaffolding is visible. The reader can see how it was derived, not just the polished result.
- [ ] Every hand-wave is flagged as one. No silent gaps.
- [ ] Where the idea is genuinely confusing or was historically distrusted, the explainer says so.
- [ ] No term from the user's own code or domain is explained back to them.
- [ ] Nothing is deferred to "later" that the reader needs now.

Then the reader test, from the author himself:

- **Understandable** - is there an aha moment, and can the idea be said simply?
- **Memorable** - will the analogy, diagram, or example survive six months?
- **Enjoyable** - would anyone want to come back to this?

Priority one for any explanation is: **do not create hate for the subject.**

## Anti-patterns

| Anti-pattern | What it looks like | Do instead |
|---|---|---|
| DNA first | Opens with the formal definition | Open with the analogy; end on the definition |
| Symbol soup | Notation before meaning | Name what each symbol *does* before it appears |
| Photorealism | Every edge case, caveat, and generalisation | Exaggerate the essence, drop the rest |
| Inked-only | Polished result, scaffolding erased | Show the pencil lines and the false starts |
| Buried payoff | The interesting part arrives at the end | Show why it matters in the first three lines |
| False linearity | Implies the idea arrived fully formed | Say it was messy, and why people resisted it |
| Fake clicking | "Clearly", "obviously", "it follows that" | Name the step that is hard, then do it slowly |
| Toy example | "Consider an arbitrary f(x)" | One real case with real numbers |

## References

- [references/adept.md](references/adept.md) - the method's principles, sources, and worked examples across math, software, and quant finance.
- [references/diagrams.md](references/diagrams.md) - the D, and how to degrade it gracefully.
- [templates/explainer.md](templates/explainer.md), [templates/explainer.html](templates/explainer.html) - skeletons.
