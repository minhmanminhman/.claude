# Retrieval

Getting the paper is most of the work. These routes were learned the hard way; they
save an hour each time.

## The tool that fails first

`WebFetch` returns binary garbage for PDFs. It cannot parse them. Do not spend three
calls discovering this again — go straight to `curl` plus text extraction, which is
what `scripts/fetch_papers.py` wraps.

```sh
curl -skL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" -o paper.pdf "$URL"
```

`-s` quiet, `-k` skip certificate checks (some university hosts have stale certs),
`-L` follow redirects, `-A` a browser user agent — several publishers serve a
challenge page to anything that looks scripted.

## Verify before you trust

A 200 response means nothing. Check what landed:

```sh
file -b paper.pdf     # "HTML document text" = a landing page, not the paper
stat -f%z paper.pdf   # a few hundred bytes = a redirect stub
```

Then extract, and check the character count:

```sh
uv run --with pypdf --no-project python -c "
from pypdf import PdfReader
r = PdfReader('paper.pdf')
t = '\n'.join(p.extract_text() or '' for p in r.pages)
open('paper.txt','w').write(t); print(len(r.pages), 'pages', len(t), 'chars')
"
```

**Under ~100 characters per page means an image-only scan.** The text layer is absent
and grep will find nothing — but the paper is *not* lost. **Read the PDF with the
`Read` tool's `pages` parameter**, which renders pages as images you can read
directly (20 pages per request). Foundational papers are disproportionately scans:
discarding them as unreadable throws away the origin of whole literatures. Flag such
a source `[full text, skimmed — read as page images]` and say which pages, or
`[not retrieved]` only if even rendering fails.

Numbers read off a rendered figure or a scanned table are still numbers you took by
eye: mark them `read off Figure N` so a reader knows their precision.

`grep` on extracted text needs `-a`; the output trips grep's binary heuristic and it
will silently print nothing without it.

```sh
grep -a -n "Abstract\|we find\|Table 3" paper.txt | head -30
```

## Where free copies live

**Resolve identifiers; never recall them.** An arXiv ID from memory lands on a real
paper of the wrong field — `1103.1671` is astrophysics, not the microstructure paper
it was assumed to be. Search the exact title, take the ID from the result, and check
the title line `fetch_papers.py` prints back.

**Order by field, not by habit.** For computer science, machine learning and
quantitative finance, arXiv is most of the corpus — try it first and you will often
be done in one call. For economics and finance journals, NBER and author pages carry
what arXiv does not. Working the wrong order costs a dozen wasted calls.

1. **arXiv** — `arxiv.org/abs/{id}`. Quantitative finance, physics-adjacent
   econometrics, machine learning. Often has an HTML rendering, which sidesteps PDF
   extraction entirely.
2. **NBER working papers** — `nber.org/system/files/working_papers/w{N}/w{N}.pdf`.
   Predictable URL, no login. The working-paper version of most US economics and
   finance articles. Flag the version: numbers move between working paper and journal.
3. **Author pages.** The highest-yield route for finance. Faculty sites host final
   PDFs of paywalled articles legitimately. Search `{author} {title} pdf`, and look
   for `.edu` or a personal domain in the results.
4. **SSRN** — abstract pages open, downloads often blocked. Treat as an abstract
   source unless a direct delivery link works.
5. **Institutional repositories** — ORA (Oxford), DSpace, HAL, and university course
   pages like `web.mit.edu/finlunch/...`. Underrated: a repository copy often
   survives when SSRN, ResearchGate and Academia have all dead-ended, and old
   unmaintained course pages hold exactly the draft you want.
6. **Open-access journals** — MDPI, frontier-market and regional journals. Full text,
   no barrier. Note that MDPI returns 403 to some clients while serving the same file
   through a DOI link.
7. **Lab and project mirrors.** Research groups host their own copies under the
   institution that funded the work — IRISA for the product-quantization papers,
   INRIA/HAL-adjacent lab pages, Microsoft Research and Meta AI project pages. This
   is the route that works when the canonical repository sits behind a proof-of-work
   wall, and it is the one most often forgotten.

## Getting the citation, which is half the Sources work

Retrieving the PDF gives you the text. The Sources block also needs volume, issue,
pages and DOI, and papers rarely state their own final pagination — preprints never
do. Two APIs settle it without a browser:

```sh
# Crossref: full bibliographic record from a title
curl -s "https://api.crossref.org/works?rows=3&query.bibliographic=Do+demand+curves+for+stocks+slope+down" \
  | python3 -c "import json,sys; [print(w['title'][0], '|', w.get('container-title',[''])[0], w.get('volume'), w.get('issue'), w.get('page'), w['DOI']) for w in json.load(sys.stdin)['message']['items']]"

# Semantic Scholar: abstracts for paywalled articles, plus venue and year
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=inverted+multi-index&fields=title,venue,year,abstract,externalIds"
```

Semantic Scholar rate-limits at roughly one request per second unauthenticated —
sleep between calls or it starts returning 429s.

## Where they do not

- **ScienceDirect, JSTOR, Wiley** — paywalled, and no user-agent trick changes that.
  Take the abstract, flag it, and move on.
- **ResearchGate** — blocks automated access.
- **Government and ministry PDF portals** — frequently image-only scans of signed
  documents.
- **Proof-of-work walls.** HAL, CORE, CiteSeerX and archive.org increasingly serve an
  Anubis-style computational challenge instead of the file. This is the new paywall.
  Do not try to solve the challenge; find another host or flag the source
  `[not retrieved]`.

## When only the abstract is available

Quote the abstract, attribute it as the abstract, and flag the entry `[abstract]`.
Then look for the number somewhere accountable: later papers that cite it usually
reproduce the headline magnitude, and citing it as `[cited in X]` is honest where
inventing a page number is not.

Never dress up an abstract-only source as a full reading. A reviewer who finds one
such claim discounts every other number in the document.

## Repair every quote you extract

PDF text layers mangle ligatures: `diﬀerence`, `eﬃcient`, `ﬁnding`, `/f_inding`, and
`ﬂow` all come out broken, and hyphenation inserts line breaks mid-word. A quotation
pasted straight from extracted text will contain those artifacts. Fix the ligatures
and rejoin hyphenated words — but change nothing else inside the quotation marks.

## Searching effectively

Search for the paper, not the topic. `"{exact title}" pdf` beats a description of the
finding. When you know the finding but not the paper, name the mechanism and the
market — "index inclusion demand curve slope pdf" — then chase the citation trail: a
recent paper's introduction is the best-curated bibliography available on any topic.

Verify the identity of what you find. A title match is not enough — check the authors,
year, and journal against the citation you were chasing, because retitled working
papers and same-title-different-authors collisions both happen.
