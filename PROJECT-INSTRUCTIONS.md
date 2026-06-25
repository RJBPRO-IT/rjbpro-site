# RJB Contracting Website — Project Instructions

## Overview
This is a static HTML/CSS/JS website for RJB Contracting (rjbpro.com), a national integrated commercial contractor headquartered in Spring City, PA, founded in 1992. The site is designed to look and feel like Turner Construction's website — full-width heroes, large typography, photo cards, clean sections. It is self-maintained by Kaylah McFarland and hosted on GitHub Pages.

**Project folder:** `/Users/kmcfarland/Claude/Projects/Creating Website/`
**GitHub repo:** `github.com/rjbpro/rjbpro-site` (private)
**Live URL:** GitHub Pages (custom domain rjbpro.com pending)

---

## Tech Stack
- Plain HTML, CSS, JavaScript — no framework
- CSS custom properties (design tokens) for all colors and fonts
- D3.js + TopoJSON for the US map on the homepage
- GitHub Pages for hosting
- No build tools, no npm, no dependencies beyond CDN scripts

---

## Brand System

### Colors (CSS tokens in `css/styles.css`)
```css
--navy:      #002850
--navy-dark: #001C3A
--navy-mid:  #003668
--orange:    #FF5113
--orange-dark: #D9420D
--white:     #FFFFFF
--gray-mid:  #616265
--gray-light: #D9D9D9
--gray-bg:   #F4F4F4
```

### Fonts
```css
--font-head:  'League Gothic', 'Arial Narrow', sans-serif
--font-museo: 'Museo', Georgia, serif
--font-body:  'Yantramanav', 'Helvetica Neue', Arial, sans-serif
```

Font files are in `fonts/`:
- `LeagueGothic-Regular.ttf` (loaded locally via @font-face — do NOT use Google Fonts CDN)
- `LeagueGothic_Condensed-Regular.ttf`
- `LeagueGothic_SemiCondensed-Regular.ttf`
- `LeagueGothic-Regular-VariableFont_wdth.ttf`
- `Museo700-Regular.otf`
- `yantramanav-regular.otf`, `-bold.otf`, `-black.otf`, `-medium.otf`, `-light.otf`, `-thin.otf`

### Other tokens
```css
--max-w:     1280px
--nav-h:     80px
--transition: 0.25s ease
```

---

## Site Structure — 25 HTML Pages

### Main pages
- `index.html` — Homepage
- `about-us.html` — About Us (needs Meet the Team section)
- `services.html` — Services landing page
- `sectors.html` — Sectors landing page
- `projects.html` — Projects
- `insights.html` — Insights / blog
- `careers.html` — Careers
- `contact-us.html` — Contact
- `subcontractors.html` — Subcontractors

### Service pages (7)
- `service-interior-fit-outs.html`
- `service-rollout-programs.html`
- `service-store-remodels.html`
- `service-rebranding-programs.html`
- `service-eifs-coatings.html`
- `service-site-surveys.html`
- `service-specialized-solutions.html`

### Sector pages (6)
- `sector-grocery.html`
- `sector-qsr.html`
- `sector-retail.html`
- `sector-warehouse.html`
- `sector-sustainable-infrastructure.html`
- `sector-healthcare.html`

### Legacy pages (kept but may be reviewed)
- `retail-construction.html`
- `warehouse-construction.html`
- `asset-maintenance.html`

---

## Navigation

Every page uses the same nav pattern. The homepage nav starts transparent and turns solid navy on scroll. All inner pages use solid navy nav.

Desktop nav has dropdown menus on Services and Sectors:
```html
<div class="nav-dropdown">
  <a href="services.html" class="nav-dropdown-trigger">Services <span class="nav-caret">▾</span></a>
  <div class="nav-dropdown-menu">
    <!-- 7 service links -->
  </div>
</div>
```

Mobile nav uses `.nav-mobile-section-label` for parent items and `.nav-mobile-child` for child links.

**Important:** When updating nav across all pages, use a Python script to batch-replace — do not manually edit 25 files.

---

## Homepage Sections (in order)
1. Hero (full-width photo + headline)
2. Trusted By bar (client logo wordmarks as inline SVGs)
3. Stats bar — 48 States Served / 1992 Founded / 1 Point of Accountability / 1,000+ Projects Completed Annually
4. Services section (3 cards: Store Remodels, Rollout Programs, View All Services)
5. US Map (D3.js, 48 contiguous states, orange fill, white borders)
6. Testimonial
7. Insights cards
8. Subcontractor CTA
9. Footer

### Removed sections
- Self-perform section — **permanently removed**. Do not add back any "self-perform" messaging anywhere on the site.

---

## Images

All images live in `images/`. The file `images/PHOTO-GUIDE.md` lists every image slot with filename, dimensions, and which page it appears on.

### Current status
Hero images (5), service page heroes (7), sector page heroes (7), homepage service cards (3) — all in place with real RJB photos.

Remaining placeholders (still using Picsum/Unsplash URLs):
- Service/sector detail inline images
- Project photos (project-01.jpg through project-06.jpg)
- Insights thumbnails (insight-01.jpg through insight-06.jpg)
- Miscellaneous images

### Adding new photos
Drop correctly-named JPG files into `images/` — the site picks them up automatically. Recommended compression: under 300KB for cards, under 500KB for heroes. Use Squoosh (squoosh.app) to compress.

### Swapping placeholders
When new local images are added, run a Python replacement script to swap the external URLs for local paths across all HTML files. Do not manually edit each page.

---

## Key Design Decisions
- **No self-perform messaging** — removed entirely from all pages and CSS
- **Navy color:** `#002850` (darker than original `#004065` but not as dark as `#001F3D`)
- **Hero headline:** "The contractor behind America's biggest *brands.*" (not "retail brands")
- **Stats bar:** 4 stats (48 states, 1992, 1 point of accountability, 1,000+ projects annually)
- **Client logos:** Inline SVG wordmarks (not external image APIs — those require auth)
- **League Gothic:** Loaded from local font file, not Google Fonts CDN
- **US Map:** D3.js + TopoJSON, Albers USA projection, filters out AK (FIPS 02) and HI (FIPS 15)

---

## Pending / In Progress
- **Meet the Team section** on `about-us.html` — grid of photo cards with name and title. Photo naming: `team-firstname-lastname.jpg` in `images/` folder.
- Remaining placeholder images (projects, insights, detail images)
- Push all recent changes to GitHub

---

## GitHub Workflow
```bash
git add .
git commit -m "describe what changed"
git push
```
Run from the `Creating Website` folder in Terminal. The repo is private. GitHub Pages deploys automatically from the `main` branch.

---

## File Structure
```
Creating Website/
├── index.html
├── about-us.html
├── [22 other .html files]
├── css/
│   └── styles.css
├── fonts/
│   ├── LeagueGothic-Regular.ttf
│   ├── Museo700-Regular.otf
│   └── yantramanav-*.otf
└── images/
    ├── PHOTO-GUIDE.md
    ├── hero-homepage.jpg
    └── [all other images]
```
