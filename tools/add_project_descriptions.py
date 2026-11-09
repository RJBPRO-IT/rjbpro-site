"""Add a one-line description under each project name on projects.html.

Uses the existing .project-loc style (small gray body text). Edit a line in
LINES and re-run to change it; re-running replaces, never duplicates.
    python3 tools/add_project_descriptions.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINES = {
    "project-t-mobile-store-remodel": "An ongoing remodel program covering 10 to 20 stores a year.",
    "project-kohls-queue-line": "Self-checkout registers and new power for queue-line refresh stations, store after store.",
    "project-petsmart-fish-tank-program": "Overnight store refreshes, each finished in five nights while the store stayed open.",
    "project-auntie-annes-fit-out": "Full interior fit-out for Applegreen, from demolition to open-ready in four weeks.",
    "project-weis-markets-remodel": "Grocery remodels of the departments customers use most, about two months per store.",
    "project-tesla-charger-installation": "V3 EV charging stations across the Northeast, 8 to 20 chargers per site.",
    "project-home-depot-restroom-remodel": "A full restroom renovation, from demolition to reopening in 7 days.",
    "project-target-vandal-glass": "Vandal-resistant glass installed and replaced at Target stores nationwide.",
    "project-panera-bread-store-refreshes": "20 to 30 stores a year brought to current brand standards, working overnight.",
    "project-amazon-warehouse-remodel": "A 120,000 sq. ft. warehouse renovation in Delaware, plus a 12,000 sq. ft. addition.",
    "project-sams-club-exterior-repaint": "Exterior repaints nationwide, including a full conversion to Sam's updated colors.",
    "project-lowes-restroom-remodels": "A 5+ year program rebuilding restrooms to Lowe's current brand standard.",
    "project-hair-cuttery-fit-out": "A 1,400 sq. ft. tenant fit-out in Lancaster, PA.",
    "project-savers-store-conversions": "Vacant big-box spaces rebuilt into new Savers stores, about 34,000 sq. ft. each.",
    "project-bobs-discount-furniture-fit-out": "A 37,000 sq. ft. shell rebuilt into a new showroom in Catonsville, MD.",
    "project-hannaford-store-remodel": "A full remodel of a 38,000 sq. ft. supermarket and pharmacy in Meredith, NH.",
    "project-sheetz-survey-program": "More than 700 locations surveyed in three months.",
}

page = ROOT / "projects.html"
s = page.read_text(encoding="utf-8")
done = 0
for slug, line in LINES.items():
    pat = re.compile(
        r'(<a class="project-card" href="/' + re.escape(slug) + r'"[^>]*>\s*<div class="project-info">.*?'
        r'<div class="project-name">[^<]*</div>)(\s*<div class="project-loc">[^<]*</div>)?', re.S)
    m = pat.search(s)
    if not m:
        print(f"NOT FOUND: {slug}")
        continue
    indent = re.search(r'\n([ \t]*)<div class="project-name">', m.group(1)).group(1)
    s = s[:m.start()] + m.group(1) + f'\n{indent}<div class="project-loc">{html.escape(line, quote=False)}</div>' + s[m.end():]
    done += 1
page.write_text(s, encoding="utf-8")
print(f"Added descriptions to {done} of {len(LINES)} project cards")
