#!/usr/bin/env python3
"""
Sitewide nav update (Sept 2026):
  1. Desktop: turns the plain "About Us" link into a dropdown that matches
     Services/Sectors. Items are in-page anchors on about-us.html (one page).
  2. Mobile: rebuilds every page's mobile menu to one standard version
     (About Us + section links, Services + 7, Sectors + 6, Projects, Insights,
     Careers, Start a Project). Several pages were missing Sectors entirely.
  3. Mobile: closes the menu after a link is tapped (needed so same-page
     anchor links on About Us don't leave the menu covering the page).

Idempotent: safe to re-run. Run from the site root:  python3 tools/update_nav_about_dropdown.py
"""
import glob, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ABOUT_ITEMS = [
    ('about-us.html#our-story',   'Our Story'),
    ('about-us.html#how-we-work', 'How We Work'),
    ('about-us.html#leadership',  'Meet the Team'),
    ('about-us.html#safety',      'Safety'),
]
SERVICES = [
    ('service-interior-fit-outs.html', 'Interior Fit-Outs'),
    ('service-rollout-programs.html', 'Rollout Programs'),
    ('service-store-remodels.html', 'Store Remodels'),
    ('service-rebranding-programs.html', 'Rebranding Programs'),
    ('service-eifs-coatings.html', 'EIFS &amp; Coatings'),
    ('service-site-surveys.html', 'Site Surveys'),
    ('service-specialized-solutions.html', 'Specialized Solutions'),
]
SECTORS = [
    ('sector-grocery.html', 'Grocery'),
    ('sector-qsr.html', 'QSR'),
    ('sector-retail.html', 'Retail'),
    ('sector-warehouse.html', 'Warehouse &amp; Distribution'),
    ('sector-sustainable-infrastructure.html', 'Sustainable Infrastructure'),
    ('sector-healthcare.html', 'Healthcare'),
]

def desktop_about(caret):
    items = '\n'.join(f'            <a href="{h}">{t}</a>' for h, t in ABOUT_ITEMS)
    return ('<div class="nav-dropdown">\n'
            f'          <a href="about-us.html" class="nav-dropdown-trigger">About Us <span class="nav-caret">{caret}</span></a>\n'
            '          <div class="nav-dropdown-menu">\n'
            f'{items}\n'
            '          </div>\n'
            '        </div>')

def mobile_block():
    L = ['  <div class="nav-mobile" id="nav-mobile">']
    def group(href, label, kids):
        L.append(f'    <div class="nav-mobile-section-label"><a href="{href}">{label}</a></div>')
        for h, t in kids:
            L.append(f'    <a href="{h}" class="nav-mobile-child">{t}</a>')
    group('about-us.html', 'About Us', ABOUT_ITEMS)
    group('services.html', 'Services', SERVICES)
    group('sectors.html', 'Sectors', SECTORS)
    for h, t in [('projects.html', 'Projects'), ('insights.html', 'Insights'), ('careers.html', 'Careers')]:
        L.append(f'    <a href="{h}">{t}</a>')
    L.append('    <a href="contact-us.html" class="btn btn-orange" style="margin-top:1rem;align-self:flex-start;">Start a Project</a>')
    L.append('  </div>')
    return '\n'.join(L)

OLD_TOGGLE = "toggle.addEventListener('click', () => mobileNav.classList.toggle('open'));"
NEW_TOGGLE = (OLD_TOGGLE + "\n    mobileNav.querySelectorAll('a').forEach(a => "
              "a.addEventListener('click', () => mobileNav.classList.remove('open')));")

# Desktop: plain About Us link immediately inside .nav-links
RE_DESKTOP = re.compile(r'(<div class="nav-links">\s*)<a href="about-us\.html">About Us</a>')
# Mobile: whole block up to the Start a Project button's closing </div>
RE_MOBILE = re.compile(r'[ \t]*<div class="nav-mobile" id="nav-mobile">.*?Start a Project</a>\s*</div>', re.S)

changed, problems = [], []
for f in sorted(ROOT.glob('*.html')):
    s = f.read_text(encoding='utf-8')
    orig = s
    caret = '&#9662;' if 'nav-caret">&#9662;' in s else '▾'
    if RE_DESKTOP.search(s):
        s = RE_DESKTOP.sub(lambda m: m.group(1) + desktop_about(caret), s, count=1)
    elif 'about-us.html" class="nav-dropdown-trigger"' not in s:
        problems.append(f'{f.name}: desktop About Us link not found')
    if RE_MOBILE.search(s):
        s = RE_MOBILE.sub(lambda m: mobile_block(), s, count=1)
    else:
        problems.append(f'{f.name}: mobile nav not found')
    if OLD_TOGGLE in s and NEW_TOGGLE not in s:
        s = s.replace(OLD_TOGGLE, NEW_TOGGLE, 1)
    if s != orig:
        f.write_text(s, encoding='utf-8')
        changed.append(f.name)

print(f'Updated {len(changed)} pages')
for p in problems: print('WARN', p)
