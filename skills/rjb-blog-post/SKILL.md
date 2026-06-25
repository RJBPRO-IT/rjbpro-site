---
name: rjb-blog-post
description: Publish or edit a blog/Insights post on the RJB Contracting website. Use whenever someone wants to add a new article, write a blog post, post an Insight, update or remove an existing post, or change what shows on the Insights page or homepage "From the field" teasers. Triggers include "publish a blog post," "add an insight," "write an article for the site," "new blog post," "post this to Insights," "update the blog," or handing over draft article copy to put on the site. Posts are Markdown files in posts/; a generator turns them into styled article pages and refreshes the Insights grid and homepage teasers. Never hand-edit the generated HTML.
---

# RJB Blog / Insights Publisher

Add posts by writing a Markdown file. A generator builds the styled article page and updates the Insights listing + homepage teasers automatically. Same model as the team page: edit data (here, a Markdown file), run one script, publish.

## How it's wired

- **`posts/*.md`** — one file per post = the **single source of truth** (front-matter + Markdown body).
- **`tools/generate_blog.py`** — reads every post and rewrites:
  - `insight-<slug>.html` — a styled article page per post (uses the site's real nav/footer, pulled from `insights.html`)
  - the **Insights grid** in `insights.html` (between `POSTS:START` / `POSTS:END`) — all posts, newest first
  - the **homepage teasers** in `index.html` (between `POSTS:HOME:START` / `POSTS:HOME:END`) — latest 3
- **`css/styles.css`** already has the article + card styles. No CSS changes needed for routine posts.

**Never hand-edit the HTML between the POSTS markers or the `insight-*.html` pages** — they're overwritten every run. Edit the Markdown.

## Workflow (every time)

1. Create/edit a file in `posts/` (copy `posts/_TEMPLATE.md` for a new one).
2. From the project root, run:
   ```
   python3 tools/generate_blog.py
   ```
3. Publish: `bash deploy.sh` (it re-runs the generators and pushes; live in ~1–2 min).

`deploy.sh` already calls the generator, so for a quick publish you can just edit the Markdown and run `bash deploy.sh`. Run the generator directly when you want to preview the HTML first.

## Front-matter schema

```
---
title: The ROI of 3-Point Locking Across a Retail Portfolio
slug: roi-3-point-locking
date: 2026-05-20
tag: Loss Prevention
author: RJB Contracting
excerpt: One or two sentences shown on the Insights grid and homepage teaser.
image: images/insights/roi-3-point-locking.jpg
---

Markdown body goes here...
```

- **title** — post headline (shown as the article H1 and card title).
- **slug** — used for the filename `insight-<slug>.html` and the card link. Lowercase, hyphens. If omitted, it's derived from the title.
- **date** — `YYYY-MM-DD`. Controls ordering (newest first) and the displayed date.
- **tag** — category label (e.g., Retail Construction, Loss Prevention, Workforce). Shows as the eyebrow.
- **author** — optional; defaults to "RJB Contracting".
- **excerpt** — required; the teaser text and the page meta description.
- **image** — optional. Path like `images/insights/<slug>.jpg`. If the file doesn't exist yet, the card shows a tidy navy placeholder with the category, and the article hero is solid navy — no broken images. Add the file later and re-run to light it up.

Body supports standard Markdown: `##` H2 sections, `###` H3, **bold**, *italic*, [links](#), bullet/numbered lists, and > blockquotes.

## Common tasks

- **New post** → copy `posts/_TEMPLATE.md` to `posts/<slug>.md`, fill it in, run the generator (or just `bash deploy.sh`).
- **Edit a post** → change the Markdown, regenerate.
- **Unpublish/remove** → delete the post's `.md` file and its `insight-<slug>.html`, then regenerate so it drops out of the grid/teasers.
- **Draft (don't publish yet)** → name the file with a leading underscore (e.g., `posts/_draft-my-post.md`); files starting with `_` or `.` are ignored.
- **Add a photo to a post** → drop `images/insights/<slug>.jpg` (landscape ~16:9, see images/PHOTO-GUIDE.md), keep the `image:` path matching, regenerate.

## Self-check before finishing

- Edited the Markdown in `posts/` (not the generated HTML)?
- Generator ran cleanly and reported the expected post count?
- New post's `slug` is unique (no collision with an existing `insight-*.html`)?
- `date` is `YYYY-MM-DD` and `excerpt` is filled in?
- If you removed a post, did you also delete its `insight-<slug>.html`?
