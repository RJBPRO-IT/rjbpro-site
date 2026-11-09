"""Rename project-01.html ... project-17.html to descriptive URLs.

What it does (one pass, safe to re-run):
  1. Renames each project page file (project-02.html -> project-kohls-queue-line.html).
  2. Rewrites every link to the old page across all .html files
     (href="/project-02" or href="/project-02#x" -> href="/project-kohls-queue-line").
  3. Updates _redirects: old WordPress project URLs now point straight at the new
     page (no double redirect), and each old /project-NN address gets a 301 to
     the new one so existing links and Google's index carry over.

Photos are NOT renamed. images/project-photos/project-02.jpg and the gallery
files keep their numbered names, so Mary's photo naming doesn't change.

To change a name, edit the RENAMES list below BEFORE the first run.
After running, regenerate the sitemap:  python3 tools/generate_sitemap.py

Usage (from the website folder):
    python3 tools/rename_project_pages.py --check   # show what would change
    python3 tools/rename_project_pages.py           # do it
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RENAMES = {
    "project-01": "project-t-mobile-store-remodel",
    "project-02": "project-kohls-queue-line",
    "project-03": "project-petsmart-fish-tank-program",
    "project-04": "project-auntie-annes-fit-out",
    "project-05": "project-weis-markets-remodel",
    "project-06": "project-tesla-charger-installation",
    "project-07": "project-home-depot-restroom-remodel",
    "project-08": "project-target-vandal-glass",
    "project-09": "project-panera-bread-store-refreshes",
    "project-10": "project-amazon-warehouse-remodel",
    "project-11": "project-sams-club-exterior-repaint",
    "project-12": "project-lowes-restroom-remodels",
    "project-13": "project-hair-cuttery-fit-out",
    "project-14": "project-savers-store-conversions",
    "project-15": "project-bobs-discount-furniture-fit-out",
    "project-16": "project-hannaford-store-remodel",
    "project-17": "project-sheetz-survey-program",
}

REDIRECT_HEADER = "# --- Project pages renamed to descriptive URLs (Oct 2026) ---"

# Page links only: href="/project-02", "project-02.html", "/project-02#gallery".
# Image paths like images/project-photos/project-02.jpg are not matched.
LINK = re.compile(r'''(href=["'])(?:\./|/)?(project-\d{2})(?:\.html)?([#?][^"']*)?(["'])''')


def rewrite_links(text):
    n = 0

    def sub(m):
        nonlocal n
        old = m.group(2)
        if old not in RENAMES:
            return m.group(0)
        n += 1
        return f"{m.group(1)}/{RENAMES[old]}{m.group(3) or ''}{m.group(4)}"

    return LINK.sub(sub, text), n


def update_redirects(text):
    # Existing WordPress rules: point straight at the new page.
    for old, new in RENAMES.items():
        text = re.sub(rf"(\s)/{old}(\s+301)", rf"\1/{new}\2", text)
    if REDIRECT_HEADER not in text:
        rules = [REDIRECT_HEADER]
        for old, new in RENAMES.items():
            rules.append(f"/{old}        /{new}   301")
            rules.append(f"/{old}.html   /{new}   301")
        block = "\n".join(rules) + "\n\n"
        # Must sit above the "/project/*" catch-all? No overlap (different path),
        # but keep it near the other project rules for readability.
        marker = "# --- All other WordPress project pages"
        if marker in text:
            text = text.replace(marker, block + marker, 1)
        else:
            text = text.rstrip("\n") + "\n\n" + block
    return text


def main():
    check = "--check" in sys.argv

    # 1. Rename files
    renamed = 0
    for old, new in RENAMES.items():
        src, dst = ROOT / f"{old}.html", ROOT / f"{new}.html"
        if src.exists() and not dst.exists():
            renamed += 1
            if not check:
                src.rename(dst)
        elif src.exists() and dst.exists():
            sys.exit(f"ERROR: both {src.name} and {dst.name} exist. Sort that out first.")

    # 2. Rewrite links
    links = pages = 0
    for path in sorted(ROOT.glob("*.html")):
        src = path.read_text(encoding="utf-8")
        out, n = rewrite_links(src)
        if n:
            links += n
            pages += 1
            if not check:
                path.write_text(out, encoding="utf-8")

    # 3. Redirects
    red = ROOT / "_redirects"
    red_changed = False
    if red.exists():
        before = red.read_text(encoding="utf-8")
        after = update_redirects(before)
        red_changed = after != before
        if red_changed and not check:
            red.write_text(after, encoding="utf-8")

    verb = "Would" if check else "Done:"
    print(f"{verb} rename {renamed} files, rewrite {links} links in {pages} pages, "
          f"{'update' if red_changed else 'no change to'} _redirects")
    if not check and renamed:
        print("Next: python3 tools/generate_sitemap.py")


if __name__ == "__main__":
    main()
