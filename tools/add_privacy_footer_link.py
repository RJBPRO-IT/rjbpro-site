#!/usr/bin/env python3
"""
Add a Privacy Policy link as the last item of the footer "Company" column
on every root-level .html page that carries the standard site footer.

Usage:
    python3 tools/add_privacy_footer_link.py

Idempotent: pages whose Company column already links privacy-policy.html are
skipped, so re-running is safe. Pages without the standard footer (or with a
footer that has no Company column) are left untouched and counted separately.
"""
import re
from pathlib import Path

LINK = '<li><a href="privacy-policy.html">Privacy Policy</a></li>'
ROOT = Path(__file__).resolve().parent.parent

# The Company column of the standard footer: <h4>Company</h4> then its <ul>.
COMPANY_UL = re.compile(r"(<h4>Company</h4>\s*<ul>)(.*?)(\n(\s*)</ul>)", re.S)


def process(path):
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    if 'class="site-footer"' not in text:
        return "no-footer"
    m = COMPANY_UL.search(text)
    if not m:
        return "no-company-col"
    if "privacy-policy.html" in m.group(2):
        return "already-linked"
    items = m.group(2)
    ind = re.search(r"\n(\s*)<li>", items)
    indent = ind.group(1) if ind else "            "
    new_block = m.group(1) + items + f"\n{indent}{LINK}" + m.group(3)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text[: m.start()] + new_block + text[m.end():])
    return "updated"


def main():
    results = {}
    for f in sorted(ROOT.glob("*.html")):
        results.setdefault(process(f), []).append(f.name)
    for name in results.get("updated", []):
        print(f"updated   {name}")
    for name in results.get("no-company-col", []):
        print(f"skipped   {name}  (footer has no Company column)")
    for name in results.get("no-footer", []):
        print(f"skipped   {name}  (no standard site footer)")
    n = len(results.get("updated", []))
    print(f"\n{n} file(s) updated, "
          f"{len(results.get('already-linked', []))} already had the link.")


if __name__ == "__main__":
    main()
