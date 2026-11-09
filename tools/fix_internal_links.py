"""Rewrite internal links to Cloudflare Pages' extensionless URLs.

Cloudflare Pages serves /about-us.html at /about-us and 308-redirects the .html
URL. Linking to the .html version sends every click (and every Googlebot visit)
through that redirect. This script points internal links straight at the final URL:

    href="about-us.html#leadership"   ->  href="/about-us#leadership"
    href="/careers.html"              ->  href="/careers"
    href="index.html"                 ->  href="/"
    window.location.href = 'thank-you-contact.html'  ->  '/thank-you-contact'

Only links to pages that exist in this folder are touched. External links
(https://...) are left alone. Safe to run more than once.

Usage (from the website folder):
    python3 tools/fix_internal_links.py           # rewrite files
    python3 tools/fix_internal_links.py --check   # report only, change nothing
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = {p.stem for p in ROOT.glob("*.html")}

# href="page.html", href="/page.html", href="./page.html", with optional #fragment or ?query
HREF = re.compile(r'''(href=["'])(?:\./|/)?([a-z0-9][a-z0-9-]*)\.html([#?][^"']*)?(["'])''', re.I)
# JS redirects like window.location.href = 'thank-you-contact.html'
JS = re.compile(r'''(location(?:\.href)?\s*=\s*["'])(?:\./|/)?([a-z0-9][a-z0-9-]*)\.html(["'])''', re.I)


def pretty(stem):
    return "/" if stem == "index" else "/" + stem


def fix(text):
    count = 0

    def href_sub(m):
        nonlocal count
        pre, stem, tail, quote = m.group(1), m.group(2), m.group(3) or "", m.group(4)
        if stem not in PAGES:
            return m.group(0)
        count += 1
        url = pretty(stem)
        if url == "/" and tail.startswith("#"):
            url = "/"  # "/#section" is fine
        return f"{pre}{url}{tail}{quote}"

    def js_sub(m):
        nonlocal count
        if m.group(2) not in PAGES:
            return m.group(0)
        count += 1
        return f"{m.group(1)}{pretty(m.group(2))}{m.group(3)}"

    text = HREF.sub(href_sub, text)
    text = JS.sub(js_sub, text)
    return text, count


def main():
    check = "--check" in sys.argv
    total = files = 0
    for path in sorted(ROOT.glob("*.html")):
        src = path.read_text(encoding="utf-8")
        out, n = fix(src)
        if n:
            files += 1
            total += n
            if not check:
                path.write_text(out, encoding="utf-8")
    verb = "would rewrite" if check else "rewrote"
    print(f"{verb} {total} internal links in {files} pages")
    return 1 if (check and total) else 0


if __name__ == "__main__":
    sys.exit(main())
