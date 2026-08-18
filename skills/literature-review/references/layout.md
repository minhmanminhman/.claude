# Layout

Six parts, in this order. Section count follows the number of distinct **claims**,
not the number of papers — see the granularity rule below, which is the difference
between a 400-line review and a 1300-line one.

```markdown
# {Question}: a literature review

{3–5 lines. The question and the shape of its answer. Lead with the finding. If the
honest summary is "the mechanism is established and the magnitudes are too small to
matter", say that here.}

## What each paper solves

| problem | method | resolved by |
|---|---|---|
| {the question, phrased as a question} | {the design, in six words} | {Author (year)} |

## 1. {The claim this section establishes, as a statement}

**Problem.** {What the authors set out to settle, in their terms.}

**Method.** {Design, data, sample, period, estimator — only what decides whether the
result transfers.}

**Result.** {Numbers with signs, units, t-statistics, sample sizes. A table if three
or more papers report the same quantity.}

> {One load-bearing sentence, verbatim.}
> <cite>Author (year), §section</cite>

{1–3 lines on what the result implies for the review's question — mechanism, not
application.}

## {…more sections, one per claim…}

## {N}. Where the papers disagree, and why

{Rank disagreements by explanatory power, strongest first. Each item names the
methodological choice that produces the conflict. Usually one or two uncontrolled
choices explain most apparent contradictions in a literature, and finding them is
worth more than either result.}

## {N+1}. What determines {the quantity the review is about}

{Cross-paper synthesis. Each determinant names which designs measured it. Three
methods reaching one conclusion is evidence no single paper contains.}

## {N+2}. Settled, and open

**Settled.**

- {Claim, flatly, one line each.}

**Open.**

1. **{The open question.}** {Why it is open — conflicting results, a parameter that
   does not transfer, an unreplicated paper, a source you could not retrieve.}

**What would overturn this.** {One or two sentences: the single finding that would
break the review's main conclusion, and where it would come from.}

## Sources

{One line on flag meanings, then entries grouped by thread.}

- **Author (year)**, "Title", *Journal* vol(issue), pages. DOI or <URL> — **[flag]**.
  Owns: {the claims and numbers this paper is the source for — one line}.
```

## Granularity: sections are claims, not papers

One section per claim, carrying however many papers support it. A section covering
several papers gets **one** Problem/Method/Result triple describing the design the
claim rests on, then either:

- `**Corroborating designs.**` followed by a table — one row per supporting paper,
  with its design and its number; or
- one or two sentences naming the papers and what each adds.

Reserve a section of its own for a paper only when it establishes something no other
paper does, or when it is the reason another paper is wrong.

## Rules the layout depends on

**Tables where they compress.** Effect sizes across papers, parameter values, sample
descriptions. Prose for mechanism only.

**"Owns:" on every source, one line.** Naming what each paper is the source for makes
the review auditable in a single pass and stops one number being credited to two
papers. Keep it to a line — a paragraph per source is how the Sources section doubles
the document.

**Formulas in the paper's own notation.** Rename nothing; define each symbol once in
a gloss beneath.

**Read-status flags, one per source:**

| flag | means |
|---|---|
| `[full text]` | retrieved and read the relevant sections |
| `[full text, working-paper version]` | read, but numbers may differ from the journal article |
| `[full text, skimmed]` | retrieved, read selectively — say which parts |
| `[full text via author's long-form version; journal closed]` | the paywalled article is unread; a preprint, slide deck or tech report by the same authors was read. Say which, and whether numbers came off a plot axis |
| `[full text, read by delegated agent]` | a subagent read it and reported; you did not open it |
| `[first-party, revised without notice — accessed YYYY-MM-DD]` | living documentation, wiki, or source code, which changes underneath you |
| `[vendor benchmark]` | numbers published by a party selling the thing measured. Keep these visibly separate from peer-reviewed results |
| `[harness source read]` | you read the benchmark's own code to check what it actually built, rather than trusting its label |
| `[abstract]` | abstract or a secondary reproduction only |
| `[not retrieved]` | could not obtain; say why and where the numbers came from |
| `[cited in X]` | known only through another paper's description |

**A DOI beats a URL** where one exists — links rot, DOIs resolve. Give a URL as well
when the free copy lives somewhere a reader would not guess.

**Numbers you computed are yours.** Anything derived from a paper's parameters, or
read off a plot rather than a table, is marked `derived here` or `read off Figure N`.

## Worked fragment

```markdown
## 4. Forced selling under distress depresses prices, and the depression reverses

**Problem.** Whether selling a manager did not choose depresses prices beyond the
information the selling reveals, and whether the depression reverses.

**Method.** Coval & Stafford cross mutual fund holdings with fund flows, 1980–2003.
Their `PRESSURE` variable measures the fraction of a stock's institutional owners
engaged in forced trade, cut at −15% and +25% (roughly the 5th and 95th percentiles).
The identifying comparison is constrained against unconstrained funds selling equally
widely.

**Result.** −10.1% (t = −11.52) over the event quarter; +7.74% (t = 4.43) recovered
over months +4 to +12. Selling by unconstrained funds shows no such pattern.

> "investors who trade against constrained mutual funds earn highly significant
> returns for providing liquidity when few others are willing or able"
> <cite>Coval & Stafford, NBER WP 11357, abstract</cite>

**Corroborating designs.**

| paper | design | horizon | magnitude |
|---|---|---|---|
| Hendershott & Menkveld (2014) | state-space split of price into efficient plus pressure | 0.54 d half-life | 17bps, large caps |
| Greenwood (2005) | one index redefinition forcing ¥2tn of trade | 20 weeks | >70% of a 19%/−32% move reverses |
```

Note what the fragment does: the method names the identifying comparison rather than
listing the dataset; the corroborating papers are rows, not sections; and one quote
covers the section.
