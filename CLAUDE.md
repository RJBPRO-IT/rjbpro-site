# CLAUDE.md — RJB Contracting Website

Project context for Claude. If you're working in this folder, read this first. It explains what the site is, how it's built, the rules to follow, and how the two-person team works.

---

## What this is
A static HTML/CSS/JS website for RJB Contracting, a national integrated commercial contractor in Spring City, PA, founded 1992. Visual style is modeled on Turner Construction — full-width heroes, large type, photo cards, clean sections. Self-maintained, hosted on GitHub Pages.

- **Repo:** `github.com/RJBPRO-IT/rjbpro-site` (private)
- **Live URL:** https://rjbpro-it.github.io/rjbpro-site/ (custom domain rjbpro.com is **pending** — not connected yet)
- **Deploys** automatically from the `main` branch, ~1 minute after a push.

---

## Who works here and how
Two people work in parallel, each from their own cloned copy of the repo via **GitHub Desktop**:

- **Kaylah** — website copy and content (the text and structure in the `.html` files).
- **Mary** — photos (the `images/` folder).

Those are different files, so the work rarely collides. Git rhythm for **both people, every session**:

1. **Pull / Fetch origin first** (get the other person's latest).
2. Make changes.
3. **Commit** with a short message.
4. **Push.** The live site updates about a minute later.

If GitHub Desktop reports a **conflict**, stop and coordinate — don't force it.

---

## Hard rules (do not break)
- **No invented facts.** Never add specific stats, client names, project details, or claims that aren't confirmed — flag what needs confirming instead. The Projects section currently uses placeholder names and photos.
- **RJB voice:** confident, plain, no hype. Short sentences, active voice. Avoid buzzwords (leverage, turnkey, best-in-class, industry-leading, seamless, game-changing, etc.).
- **No "self-perform" messaging anywhere** — permanently removed from the site.
- **Don't hand-edit many pages one at a time.** For anything that spans multiple pages (nav, footer, swapping image URLs), write a small **Python script** to batch-edit. Don't manually edit 25+ files.
- **Fonts load locally** from `fonts/` via `@font-face`. Do NOT use the Google Fonts CDN.

---

## Tech stack
Plain HTML, CSS, JS — no framework, no build tools, no npm. CSS custom properties (design tokens) for all colors and fonts. D3.js + TopoJSON for the homepage US map (Albers USA projection, 48 contiguous states, filters out AK/HI). Only CDN scripts; no other dependencies.

---

## Brand system (tokens in `css/styles.css`)
**Colors:** `--navy #002850`, `--navy-dark #001C3A`, `--navy-mid #003668`, `--orange #FF5113`, `--orange-dark #D9420D`, `--white #FFFFFF`, `--gray-mid #616265`, `--gray-light #D9D9D9`, `--gray-bg #F4F4F4`.

**Fonts:** `--font-head` 'League Gothic' (headlines), `--font-museo` 'Museo' (labels/subheads), `--font-body` 'Yantramanav' (body).

**Layout:** `--max-w 1280px`, `--nav-h 80px`, `--transition 0.25s ease`.

---

## Pages
- **Main:** index, about-us, services, sectors, projects, insights, careers, contact-us, subcontractors.
- **Services (7):** service-interior-fit-outs, -rollout-programs, -store-remodels, -rebranding-programs, -eifs-coatings, -site-surveys, -specialized-solutions.
- **Sectors (6):** sector-grocery, -qsr, -retail, -warehouse, -sustainable-infrastructure, -healthcare.
- **Project detail pages (6):** project-01 … project-06 (linked from `projects.html`).
- **Insights posts:** several `insight-*.html`.
- **Legacy (kept but unlinked from nav/footer):** retail-construction, warehouse-construction, asset-maintenance.

---

## Navigation & footer (shared across all pages)
- **Nav:** homepage starts transparent and turns solid navy on scroll; inner pages use solid navy. Desktop has Services/Sectors dropdowns; mobile uses `.nav-mobile-section-label` and `.nav-mobile-child`.
- **Footer:** standardized on **every** page to four blocks — brand, **Company**, **Services (all 7)**, **Connect**. (Standardized across the site; the older 3-link footer is retired.)
- Update either one across all pages with a Python batch script, never by hand.

---

## Images & photos
- All images live in `images/`. **`images/PHOTO-GUIDE.md` is the master list** of every slot: filename, size, and where it's used. Always name files to match it.
- **Naming:** lowercase, hyphens, no spaces. Compress first (Squoosh; under 300KB for cards, under 500KB for heroes).
  - Team photos: `team-firstname-lastname.jpg`
  - Project page hero: `project-0X-hero.jpg`
  - Project gallery: `project-0X-gallery-1.jpg`, `-2.jpg`, …
  - Project thumbnail (Projects page): `project-0X.jpg`
- **Placeholder swap:** some slots (Projects grid thumbnails, project galleries, insights thumbnails, some detail images) still point at Picsum placeholder URLs. A correctly-named local file will NOT appear until those URLs are swapped to local paths — do that swap with a Python script across all HTML, not by hand. (Team photos and page/service/sector/project heroes already point at local files and appear as soon as they're added.)

---

## Current state
- Project detail pages (project-01..06) exist: each has a **Project Details** panel (Client / Sector / Location / Scope), a flexible heading+body area, and a click-to-enlarge **gallery lightbox**. Body copy and gallery photos are placeholders to be filled in.
- Each project's gallery is part of its page (not a separate section).
- Footer standardized sitewide to the 7-service version.
- Careers page: intro copy + Benefits, two buttons (**Work for RJB** → UKG/saashr portal; **Indeed Openings** → Indeed), and the old Open Positions list removed.
- About-us "Meet the Team" section is built and references 45 `team-*.jpg` photos.

---

## Known pending
- Connect custom domain **rjbpro.com**.
- Fill in real project copy + photos (replace placeholders) and run the placeholder→local image swap.
- Insights thumbnails and some detail images still placeholders.

---

## Keeping THIS file in sync
`CLAUDE.md` is a normal file in the repo, so it travels through git like everything else — it updates **when you pull and push, not live.**

To avoid clashes on this shared file:
- **Kaylah owns edits to `CLAUDE.md`.** Mary's Claude reads it for context; if Mary needs something reflected here, tell Kaylah (or pull right before editing and push right after).
- Keep edits to this file small and commit them on their own, so merges stay clean.
- After someone updates and pushes it, the other person pulls to get it; their Claude picks up the new version the next time it reads the folder.

> This file supersedes `PROJECT-INSTRUCTIONS.md`. Keep project context here so there's a single source of truth.
