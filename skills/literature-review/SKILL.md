---
name: literature-review
description: Survey the academic literature on a question and write it up as a short, traceable, primary-sourced review laid out problem → methodology → result, saved as literature-review-{problem}.md wherever the repo keeps its notes. Use this whenever the user asks what the literature or the research says about something, wants papers found, read, or summarised, wants to know whether an effect or method is established, asks for a survey or lit review, or hands you an existing notes file and says "rewrite this as a literature review" — and also when a design decision hinges on published evidence and someone needs the evidence gathered before the decision is made. Prefer it over answering from memory any time the answer should cite papers.
---

# Literature review

A literature review earns its keep two ways, and they pull against each other.

**Traceable.** Every number can be followed back to the paper that owns it, and a
reader can tell which problem each paper solved and by what method. Three
commitments get you there: read the paper rather than a write-up of it; mark
honestly what you actually read, because `[full text]` and `[abstract]` are
different kinds of knowledge; and state what the literature settles without
applying it to whatever the reader is building. A review written around one use
case cannot be reused for the next, and its citations quietly become
justifications.

**Short.** A review is a compression of a literature, not a transcript of it. The
judgment you add is what you leave out — which papers collapse into one table row,
which method details change whether a result transfers, which single sentence from
a paper is load-bearing. Reviews fail far more often by padding than by omission,
because padding is easy to produce and looks like rigour.

Hold both. Every number traceable; every paragraph earning its place.

## Length, and what to cut

Set the budget before writing:

| corpus | target | ceiling |
|---|---|---|
| ≤ 8 papers | 200–300 lines | 400 |
| 9–20 papers | 300–500 lines | 700 |
| 20+ papers | 500–700 lines | 900 |

The band is a target and the ceiling is the constraint. **Never drop a traceable
number to reach the band** — collapse a section into a table row instead, and if the
literature genuinely needs the space, land under the ceiling and say why in the
report. Chasing the band past that point costs a trim pass and buys nothing.

Past the ceiling, you are transcribing. Cut in this order:

1. **The third paper making an established point.** Two designs agreeing is
   evidence; five is a bibliography. Corroborating papers become rows in one
   evidence table, not sections of their own.
2. **Method detail that does not change transferability.** Sample period and
   estimator earn their words when they decide whether the result carries to
   another market or dataset. Hardware and software versions rarely do.
3. **Quotes past the first per section.** See below.
4. **Any sentence restating the number in the table above it.**

**The compression test.** Whenever three or more papers report the same quantity,
that is a table, not three paragraphs. Prose is for mechanism — why a result holds,
why two papers disagree. Numbers belong in rows.

**One verbatim quote per section, two where a second carries a distinct claim.** One
or two sentences each. Quote where the author's
exact words carry the claim or where a paraphrase would drift; cite with numbers
everywhere else. A review that quotes everything has transferred no judgment —
picking the one load-bearing sentence *is* the work. Never edit inside quotation
marks: an author's hedges are theirs, and improving them is falsification.

## Workflow

### 1. Fix the question and its boundary

Write down, before reading: the question, the threads that count as on-topic, and
what is excluded. Reviews rot by accretion — every paper suggests two more.

Given an existing notes file, mine it for citations and numbers first. The claims it
flags as second-hand are the ones worth retrieving properly.

**If a file the user named is missing, stop and say so.** Do not reconstruct the
topic from sibling documents: a paper list inferred from the wrong context is worse
than no list, and the user may be able to restore the original in seconds. Treat
every source note as read-only for the whole run — reviews are additive, and nothing
in this workflow has cause to modify or delete the notes it reads.

### 2. Build the paper list, then delegate against it

Name the papers and threads **before** spawning anyone. Then, if you delegate:

- **Partition explicitly.** One agent per thread with a named, disjoint paper list.
  Unpartitioned readers duplicate a third of their work.
- **Wait for every reader you spawn** — writing the review while a reader is still
  out wastes its entire cost and leaves the artifact citing less than you paid for.
  If one must be abandoned, say so in Open items and claim no coverage over its
  thread.
- **Waiting is awkward, so prefer not to need it.** A subagent cannot block on its
  own children, and foreground `sleep` is refused by the harness; polling burns a
  dozen turns per run. If you are yourself a subagent, read inline or spawn readers
  you can wait on synchronously. Delegate in parallel only when the reading is large
  enough that a dozen wasted turns is cheap by comparison.
- **Namespace scratch directories** per agent (`/tmp/litrev-{thread}/`), or two
  agents will fight over the same path.

Tell readers what not to do: no application to any project, no recommendations, no
code. Ask them for the four extractions below, not for prose.

### 3. Retrieve, and verify what landed

`scripts/fetch_papers.py` downloads, extracts text, prints the first line of each
paper so you can confirm identity, and flags image-only scans. Check that first line
— a guessed URL returns a real PDF of the wrong paper, and the byte count will not
tell you. `references/retrieval.md` holds per-publisher routes, the proof-of-work
walls, and how to get citation metadata, which is half the Sources work.

Prefer the journal version, then an author-hosted preprint, then a working paper
(flag the version — numbers move), then the abstract flagged `[abstract]`.

### 4. Extract four things per paper

1. **The problem**, as a question, in the authors' terms.
2. **The method** — design, data, sample, period, estimator — kept to what decides
   transferability.
3. **The result** — numbers with signs, units, t-statistics, sample sizes.
4. **The load-bearing sentence**, verbatim, for the section it will support.

**When an abstract states a result, read the table before quoting it.** Abstracts
round, drop the specification that produced the number, and sometimes report the
significant variant of an insignificant baseline. This is the most common way a
careful review still ends up wrong.

Where two papers disagree, keep both and find the methodological choice behind the
disagreement — that explanation is worth more than either result.

### 5. Write to the layout

Follow `references/layout.md`. Sections are organized by **claim**, not by paper: one
`**Problem.** / **Method.** / **Result.**` triple per claim, however many papers
support it. A paper-per-section review of twenty papers is the bloat failure.

### 6. Prose pass

Omit needless words, drop qualifiers, use positive form, put the finding at the end
of its sentence. `scripts/lint_review.py` checks the mechanical part; invoke
`elements-of-style` if you want the full revision order.

The linter's banned prose, so you write clean instead of repairing: *very, rather,
quite, somewhat, fairly, pretty*; "the fact that", "in order to", "in terms of", "it
is important to note", "it should be noted", "one of the most", "as to whether";
first-person and advisory phrasing (*we should, we need, for us, I recommend, next
step, my …*).

### 7. Place the artifact

Name it `literature-review-{problem}.md`, `{problem}` in kebab-case naming the
question rather than the field. Put it where the repo keeps notes of this kind
(`docs/`, `notes/`, `research/`, a per-experiment directory) and **match the
neighbours' naming style** where one exists, including underscores.

Leave source notes alone. Asked to rewrite a file as a review, write a new file and
say both exist — the original usually carries project-specific reasoning the review
strips on purpose. Offer to delete rather than assuming.

### 8. Lint, then report

Run `scripts/lint_review.py <file>`. Then report in a few lines: the path, the line
count against the budget, the three to five load-bearing findings **with numbers**,
the sharpest conflict in the literature, and any number the user believed that you
found to be wrong, with the source that settled it.

## Scope discipline

**In:** what the papers claim, how they established it, the magnitudes, the
disagreements, what remains open, what could not be verified.

**Out:** what to build, what to measure next, cost or feasibility arithmetic for one
reader, any framing that only makes sense to one project. If the user wants that, it
is a different document — say so and offer it separately.

Two closing sections carry the judgment that *is* in scope: **settled**, the claims
the literature supports, and **open**, the questions it leaves, naming what you could
not verify and what single finding would overturn the review's conclusion. Writing
those honestly is the hardest part of the job and the part a reader trusts most.
