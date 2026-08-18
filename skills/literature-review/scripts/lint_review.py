#!/usr/bin/env python3
"""Lint a literature review for the failures that survive a careful read.

Checks, in order of how often they bite:

  length       the document stays inside the budget for its corpus size
  padding      one verbatim quote per section, not five
  provenance   every Sources entry carries a read-status flag
  application  no advice, no first person, no reader's project in the prose
  spine        every paper section leads with Problem / Method / Result
  qualifiers   very, rather, quite, somewhat, fairly — outside quotations
  passengers   "the fact that", "in order to", "it is important to note"

Quoted text is exempt from the prose checks: an author's hedges are theirs, and
editing a quotation to read better is falsification.

Usage:
    python lint_review.py literature-review-{problem}.md
"""

import pathlib
import re
import sys
from pathlib import Path

QUALIFIERS = r"\b(very|rather|quite|somewhat|fairly|pretty)\b"
PASSENGERS = [
    "the fact that", "in order to", "in terms of", "it is important to note",
    "it should be noted", "it is interesting that", "one of the most",
    "as to whether", "the reason why is that", "needless to say",
]
APPLICATION = [
    r"\bwe should\b", r"\bwe need\b", r"\bour (?:book|data|strategy|overlay|project|case|universe)\b",
    r"\bfor us\b", r"\bthis (?:project|repo|repository)\b", r"\bI recommend\b",
    r"\bnext step\b", r"\btestable (?:now|here)\b",
]
# lines → ceiling, by number of sources: a review is a compression, not a transcript
BUDGET = ((8, 400), (20, 700), (10**6, 900))
LAYOUT = pathlib.Path(__file__).resolve().parent.parent / "references" / "layout.md"


def documented_flags():
    """Read the accepted vocabulary out of layout.md's flag table.

    Hardcoding it here drifted twice: a flag the template documented was rejected
    by the linter, and the fix was to write a dishonest flag to get a clean pass.
    A check that corrupts provenance is worse than no check, so the table is the
    single source of truth.
    """
    fallback = ["full text", "abstract", "not retrieved", "cited in"]
    try:
        table = LAYOUT.read_text()
    except OSError:
        return fallback
    found = [re.split(r"[,;—]", m.group(1))[0].strip().lower()
             for m in re.finditer(r"^\|\s*`\[([^\]]+)\]`", table, re.M)]
    return found or fallback


FLAGS = documented_flags()
# any honest statement of what was read counts, not just the canonical six
FLAG_SHAPE = re.compile(r"only|paywalled|unverified|scan|not obtained|abstract", re.I)
SPINE_EXEMPT = re.compile(
    r"what each paper|what (?:determines|governs|explains)|disagree|settled|open"
    r"|sources|synthesis|conclusion", re.I
)
# "rather than" is comparative, not an intensifier; same for "further"/"little of"
QUALIFIER_EXEMPT = re.compile(r"\brather\s+than\b|\bquite\s+accurate", re.I)


def strip_quotes(line):
    """Remove quoted spans and code so an author's words are never linted."""
    line = re.sub(r"\$\$.+?\$\$|`[^`]*`", " ", line)
    line = re.sub(r"[\"“][^\"”]*[\"”]", " ", line)
    line = re.sub(r"\*\"[^\"]*\"\*", " ", line)
    return line


def lint(path):
    lines = path.read_text().splitlines()
    findings = []
    in_code = in_sources = in_quote = False
    sections = []  # (heading_line_index, heading_text, body_lines)

    for index, raw in enumerate(lines, start=1):
        if raw.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        if raw.startswith("## "):
            in_sources = bool(re.search(r"^##\s+sources", raw, re.I))
            sections.append([index, raw[3:].strip(), []])
        elif sections:
            sections[-1][2].append((index, raw))

        # Provenance: a bibliography entry names a paper and must say what was read.
        if in_sources and re.match(r"^-\s+\*\*", raw):
            entry = [raw]
            offset = index
            while offset < len(lines) and not re.match(r"^-\s+\*\*", lines[offset]):
                entry.append(lines[offset])
                offset += 1
            blob = re.sub(r"\s+", " ", " ".join(entry))
            found = re.findall(r"\[([^\]]+)\]", blob)
            named = [f for f in found
                     if any(flag in f.lower() for flag in FLAGS) or FLAG_SHAPE.search(f)]
            if not named:
                unknown = [f for f in found if not f.startswith("http")]
                hint = f" (has {unknown})" if unknown else ""
                findings.append((index, "provenance", f"source entry has no read-status flag{hint}"))

        if raw.startswith(">") or raw.startswith("|"):
            continue  # quotations and tables of published values
        was_quoting = in_quote
        if raw.count('"') % 2:
            in_quote = not in_quote          # a quotation spanning several lines
        if was_quoting or in_quote:
            continue

        prose = strip_quotes(raw)
        # comparatives and idioms break across line ends, so judge with the next line
        lookahead = re.sub(
            r"\s+", " ", prose + " " + (strip_quotes(lines[index]) if index < len(lines) else "")
        )

        for hit in re.finditer(QUALIFIERS, prose, re.I):
            if not QUALIFIER_EXEMPT.search(lookahead[max(0, hit.start() - 12):hit.end() + 24]):
                findings.append((index, "qualifier", f"'{hit.group(0)}' — let the number carry it"))
        for phrase in PASSENGERS:
            if phrase in prose.lower():
                findings.append((index, "passenger", f"'{phrase}' — has a shorter form, always"))
        for pattern in APPLICATION:
            hit = re.search(pattern, prose, re.I)
            if hit:
                findings.append((index, "application", f"'{hit.group(0)}' — the review states, it does not advise"))

    for start, heading, body in sections:
        if SPINE_EXEMPT.search(heading) or not re.match(r"^\d+\.", heading):
            continue
        text = "\n".join(line for _, line in body)
        # accept **Result.** and **Result**, — the marker matters, the period does not
        missing = [word for word in ("Problem", "Method", "Result")
                   if not re.search(rf"\*\*{word}[^*\n]{{0,24}}\*\*", text)]
        if missing:
            findings.append((start, "spine", f"section '{heading[:44]}' lacks {', '.join(missing)}"))
        if ">" not in text and '*"' not in text:
            findings.append((start, "spine", f"section '{heading[:44]}' quotes no source verbatim"))

    # length and padding: the two failure modes readers complain about first
    sources, counting = 0, False
    for line in lines:
        if line.startswith("## "):
            counting = bool(re.search(r"^##\s+sources", line, re.I))
        elif counting and re.match(r"^-\s+\*\*", line):
            sources += 1
    ceiling = next(cap for limit, cap in BUDGET if sources <= limit)
    if len(lines) > ceiling:
        findings.append((len(lines), "length",
                         f"{len(lines)} lines over {ceiling} for {sources} sources — "
                         f"collapse corroborating papers into one evidence table"))

    for start, heading, body in sections:
        if not re.match(r"^\d+\.", heading):
            continue
        blocks, prev = 0, False
        for _, line in body:
            quoting = line.startswith(">")
            blocks += quoting and not prev
            prev = quoting
        if blocks > 2:
            findings.append((start, "padding",
                             f"section '{heading[:38]}' has {blocks} quote blocks — "
                             f"keep the one or two that carry distinct claims"))

    return findings


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    total = 0
    for name in sys.argv[1:]:
        path = Path(name)
        findings = lint(path)
        total += len(findings)
        print(f"\n{path}: {len(findings)} findings")
        for line, kind, message in sorted(findings):
            print(f"  {path}:{line}: {kind}: {message}")

    print(f"\n{total} findings. Quotations are exempt by design — fix your prose, never theirs.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
