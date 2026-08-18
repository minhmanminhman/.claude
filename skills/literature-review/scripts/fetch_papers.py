#!/usr/bin/env python3
"""Download papers, extract their text, and report what is actually readable.

WebFetch cannot parse PDFs and a 200 response proves nothing — publishers serve
landing pages, redirect stubs and image-only scans that look like successes. This
downloads, then tells you which files hold real text.

Usage:
    uv run --with pypdf --no-project python fetch_papers.py OUTDIR URL [URL ...]
    uv run --with pypdf --no-project python fetch_papers.py OUTDIR --from-file urls.txt

urls.txt lines are `name<TAB>url` or bare urls (name inferred from the URL).
Writes OUTDIR/{name}.pdf and OUTDIR/{name}.txt, prints one line per paper, and exits
nonzero if any paper came back unreadable.
"""

import re
import subprocess
import sys
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
MIN_CHARS_PER_PAGE = 100  # below this the PDF is an image scan with no text layer


def slug(url):
    # keep the whole basename: Path.stem cuts arXiv ids at the dot, so 1011.6402
    # and 1011.9999 would both become "1011" and silently overwrite each other
    name = Path(url.split("?")[0]).name or "paper"
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:48]


def download(url, path):
    subprocess.run(
        ["curl", "-skL", "-A", UA, "--max-time", "120", "-o", str(path), url],
        check=False,
    )
    return path.exists() and path.stat().st_size > 0


def extract(pdf, txt):
    """Return (pages, chars) or None when the file is not a parseable PDF."""
    from pypdf import PdfReader

    try:
        reader = PdfReader(str(pdf))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as error:
        return None, str(error)
    txt.write_text(text)
    return (len(reader.pages), len(text), first_line(text)), None


def first_line(text):
    """The title, usually — the only cheap check that the URL returned the right paper."""
    for line in text.splitlines():
        line = " ".join(line.split())
        if len(line) > 12:
            return line[:90]
    return "(no text)"


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        return 2

    outdir = Path(args[0])
    outdir.mkdir(parents=True, exist_ok=True)

    targets = []
    if args[1] == "--from-file":
        for line in Path(args[2]).read_text().splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            name, _, url = line.partition("\t")
            targets.append((name.strip(), url.strip()) if url.strip() else (slug(name), name.strip()))
    else:
        targets = [(slug(url), url) for url in args[1:]]

    unreadable = 0
    for name, url in targets:
        pdf = outdir / f"{name}.pdf"
        if not download(url, pdf):
            print(f"{name:24s} DOWNLOAD FAILED   {url}")
            unreadable += 1
            continue

        size = pdf.stat().st_size
        kind = subprocess.run(["file", "-b", str(pdf)], capture_output=True, text=True).stdout.strip()
        if "PDF" not in kind:
            # a landing page or a redirect stub, saved with a .pdf name
            print(f"{name:24s} NOT A PDF ({size}B: {kind[:40]}) — open {url} by hand")
            unreadable += 1
            continue

        result, error = extract(pdf, outdir / f"{name}.txt")
        if error:
            print(f"{name:24s} UNPARSEABLE       {error[:60]}")
            unreadable += 1
            continue

        pages, chars, title = result
        per_page = chars / max(pages, 1)
        verdict = "OK" if per_page >= MIN_CHARS_PER_PAGE else "IMAGE SCAN — no text layer, flag [not retrieved]"
        print(f"{name:24s} {pages:4d}p {chars:8d} chars ({per_page:5.0f}/page)  {verdict}")
        print(f"{'':24s} → {title}")
        if per_page < MIN_CHARS_PER_PAGE:
            unreadable += 1

    print(f"\n{len(targets)} requested, {unreadable} unreadable. Text alongside each PDF in {outdir}/")
    print("CHECK EVERY → LINE: a guessed URL returns a real PDF of the wrong paper.")
    print("Grep needs -a on extracted text: grep -a -n 'Abstract\\|we find' file.txt")
    return 1 if unreadable else 0


if __name__ == "__main__":
    sys.exit(main())
