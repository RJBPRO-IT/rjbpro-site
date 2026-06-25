#!/usr/bin/env python3
"""
Generate the RJB blog from Markdown.

Source of truth:  posts/*.md   (one file per post; front-matter + Markdown body)
Outputs (rewritten each run):
  - insight-<slug>.html         one styled article page per post
  - insights.html               Insights grid (between POSTS:START / POSTS:END)
  - index.html                  homepage teasers, latest 3 (POSTS:HOME:START / :END)

Usage:
    python3 tools/generate_blog.py            # auto-detect project root
    python3 tools/generate_blog.py --root /path/to/site

Posts are sorted newest-first by `date`. Files whose names start with `_` or `.`
are ignored (e.g. posts/_TEMPLATE.md). Re-running is safe/idempotent.
"""
import argparse
import html
import re
import sys
from datetime import datetime
from pathlib import Path

import markdown

LIST_START, LIST_END = "<!-- POSTS:START -->", "<!-- POSTS:END -->"
HOME_START, HOME_END = "<!-- POSTS:HOME:START -->", "<!-- POSTS:HOME:END -->"
HOME_COUNT = 3

NAV_SCRIPT = """  <script>
    const toggle = document.getElementById('nav-toggle');
    const mobileNav = document.getElementById('nav-mobile');
    toggle.addEventListener('click', () => mobileNav.classList.toggle('open'));
  </script>"""


def find_root(explicit):
    cands = []
    if explicit:
        cands.append(Path(explicit).resolve())
    here = Path(__file__).resolve()
    cands += [Path.cwd().resolve(), here.parent, here.parent.parent]
    for start in cands:
        for d in [start, *start.parents]:
            if (d / "insights.html").is_file() and (d / "posts").is_dir():
                return d
    sys.exit("ERROR: could not find project root (needs insights.html + posts/). Use --root.")


def esc(s):
    return html.escape(str(s), quote=True)


def parse_post(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        sys.exit(f"ERROR: {path.name} is missing front-matter (--- block at the top).")
    fm_raw, body_md = m.group(1), m.group(2)
    fm = {}
    for line in fm_raw.splitlines():
        line = line.rstrip()
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        fm[k.strip().lower()] = v
    for req in ("title", "date", "tag", "excerpt"):
        if req not in fm:
            sys.exit(f"ERROR: {path.name} front-matter missing '{req}'.")
    slug = fm.get("slug") or re.sub(r"[^a-z0-9]+", "-", fm["title"].lower()).strip("-")
    try:
        dt = datetime.strptime(fm["date"], "%Y-%m-%d")
    except ValueError:
        sys.exit(f"ERROR: {path.name} date must be YYYY-MM-DD (got '{fm['date']}').")
    body_html = markdown.markdown(body_md.strip(), extensions=["extra", "sane_lists"])
    return {
        "slug": slug,
        "title": fm["title"],
        "tag": fm["tag"],
        "excerpt": fm["excerpt"],
        "author": fm.get("author", "RJB Contracting"),
        "image": fm.get("image", ""),
        "date": dt,
        "date_str": f"{dt.strftime('%B')} {dt.day}, {dt.year}",
        "body_html": body_html,
    }


def extract_chrome(insights_html):
    """Pull the shared nav (+ mobile nav) and footer from a known-good page."""
    nav = re.search(r'  <nav class="site-nav.*?</nav>\s*<div class="nav-mobile".*?</div>\s*\n',
                    insights_html, re.S)
    footer = re.search(r'  <footer class="site-footer">.*?</footer>', insights_html, re.S)
    if not nav or not footer:
        sys.exit("ERROR: couldn't extract nav/footer from insights.html.")
    return nav.group(0).rstrip("\n"), footer.group(0)


def card_html(p, indent="        "):
    if p["has_image"]:
        img = (f'<div class="insight-card-img">'
               f'<img src="{esc(p["image"])}" alt="{esc(p["title"])}" loading="lazy" /></div>')
    else:
        img = (f'<div class="insight-card-img insight-card-img--empty">'
               f'<span>{esc(p["tag"])}</span></div>')
    return (
        f'{indent}<a class="insight-card" href="insight-{p["slug"]}.html">\n'
        f'{indent}  {img}\n'
        f'{indent}  <div class="insight-card-body">\n'
        f'{indent}    <div class="insight-tag">{esc(p["tag"])}</div>\n'
        f'{indent}    <h3 class="insight-title">{esc(p["title"])}</h3>\n'
        f'{indent}    <p class="insight-excerpt">{esc(p["excerpt"])}</p>\n'
        f'{indent}    <span class="insight-link">Read More &rarr;</span>\n'
        f'{indent}  </div>\n'
        f'{indent}</a>'
    )


def article_page(p, nav, footer):
    if p["has_image"]:
        hero_cls, hero_bg = "", (f'    <div class="page-hero-bg" '
                                 f'style="background-image:url(\'{esc(p["image"])}\');"></div>\n')
    else:
        hero_cls, hero_bg = " article-hero--plain", ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{esc(p['excerpt'])}" />
  <title>{esc(p['title'])} | RJB Contracting</title>
  <link rel="stylesheet" href="css/styles.css" />
</head>
<body style="padding-top:var(--nav-h);">

{nav}

  <!-- ARTICLE HERO -->
  <section class="page-hero article-hero{hero_cls}">
{hero_bg}    <div class="page-hero-content">
      <div class="section-label">{esc(p['tag'])}</div>
      <h1 class="t-section-head">{esc(p['title'])}</h1>
      <p class="article-meta">{esc(p['date_str'])} &middot; {esc(p['author'])}</p>
    </div>
  </section>

  <!-- ARTICLE BODY -->
  <section class="content-section">
    <div class="content-inner">
      <article class="article-body">
{p['body_html']}
      </article>
      <a href="insights.html" class="insight-link" style="display:inline-block;margin-top:2.5rem;">&larr; Back to Insights</a>
    </div>
  </section>

{footer}

{NAV_SCRIPT}
</body>
</html>
"""


def replace_grid(content, start_m, end_m, inner):
    block = f"{start_m}\n{inner}\n      {end_m}"
    if start_m in content:
        return re.sub(re.escape(start_m) + r".*?" + re.escape(end_m),
                      lambda _m: block, content, count=1, flags=re.S)
    open_tag = '<div class="insights-grid">'
    i = content.find(open_tag)
    if i == -1:
        sys.exit("ERROR: no POSTS markers and no <div class=\"insights-grid\"> found.")
    inner_start = i + len(open_tag)
    depth, j, close_idx = 1, inner_start, None
    while j < len(content):
        nd = content.find("<div", j)
        cd = content.find("</div>", j)
        if cd == -1:
            break
        if nd != -1 and nd < cd:
            depth += 1
            j = nd + 4
        else:
            depth -= 1
            if depth == 0:
                close_idx = cd
                break
            j = cd + 6
    if close_idx is None:
        sys.exit("ERROR: could not find the closing </div> of insights-grid.")
    return content[:inner_start] + "\n      " + block + "\n    " + content[close_idx:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    args = ap.parse_args()
    root = find_root(args.root)

    posts = []
    for f in sorted((root / "posts").glob("*.md")):
        if f.name.startswith(("_", ".")):
            continue
        p = parse_post(f)
        p["has_image"] = bool(p["image"]) and (root / p["image"]).is_file()
        posts.append(p)
    if not posts:
        sys.exit("No posts found in posts/ (other than templates).")
    posts.sort(key=lambda p: p["date"], reverse=True)

    insights_html = (root / "insights.html").read_text(encoding="utf-8")
    nav, footer = extract_chrome(insights_html)

    # 1. article pages
    for p in posts:
        (root / f"insight-{p['slug']}.html").write_text(article_page(p, nav, footer), encoding="utf-8")

    # 2. Insights listing grid (all posts)
    listing = "\n".join(card_html(p) for p in posts)
    insights_html = replace_grid(insights_html, LIST_START, LIST_END, listing)
    (root / "insights.html").write_text(insights_html, encoding="utf-8")

    # 3. homepage teasers (latest N)
    home = (root / "index.html").read_text(encoding="utf-8")
    home_cards = "\n".join(card_html(p) for p in posts[:HOME_COUNT])
    home = replace_grid(home, HOME_START, HOME_END, home_cards)
    (root / "index.html").write_text(home, encoding="utf-8")

    missing = [p["slug"] for p in posts if not p["has_image"]]
    print(f"OK  root: {root}")
    print(f"OK  {len(posts)} posts -> article pages + Insights grid + homepage ({HOME_COUNT} teasers)")
    print(f"OK  newest: {posts[0]['title']} ({posts[0]['date_str']})")
    if missing:
        print(f"NOTE  no image yet for: {', '.join(missing)} "
              f"(navy placeholder shown; add images/insights/<slug>.jpg to light them up)")


if __name__ == "__main__":
    main()
