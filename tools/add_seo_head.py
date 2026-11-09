"""Add canonical tags to every public page and Organization schema to the homepage.

Canonical tag: tells Google the one official address for each page
(https://rjbpro.com/about-us), so versions like /about-us.html or ?utm=...
are treated as the same page.

Organization schema: a hidden block of business details (name, address,
email, logo, LinkedIn) on the homepage that Google reads for search results
and to match the site to the Google Business listing. No phone number.

Safe to re-run: both blocks sit between SEO:START / SEO:END markers and are
replaced, not duplicated. Re-run after adding or renaming pages.

Usage (from the website folder):
    python3 tools/add_seo_head.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://rjbpro.com"

# Pages that should NOT get a canonical (same list the sitemap skips).
SKIP = {
    "404.html",
    "thank-you-contact.html", "thank-you-subcontractor.html",
    "retail-construction.html", "warehouse-construction.html",
    "asset-maintenance.html",
}

ORG = {
    "@context": "https://schema.org",
    "@type": "GeneralContractor",
    "name": "RJB Contracting",
    "legalName": "RJB Contracting, Inc.",
    "url": f"{BASE}/",
    "logo": f"{BASE}/images/rjb-logo.png",
    "image": f"{BASE}/images/rjb-logo.png",
    "email": "info@rjbpro.com",
    "foundingDate": "1992",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "562 Ridge Road",
        "addressLocality": "Spring City",
        "addressRegion": "PA",
        "postalCode": "19475",
        "addressCountry": "US",
    },
    "areaServed": {"@type": "Country", "name": "United States"},
    "sameAs": ["https://www.linkedin.com/company/rjbpro"],
}

BLOCK = re.compile(r"\n?[ \t]*<!-- SEO:START -->.*?<!-- SEO:END -->", re.S)


def build(path):
    url = f"{BASE}/" if path.name == "index.html" else f"{BASE}/{path.stem}"
    lines = ["  <!-- SEO:START -->", f'  <link rel="canonical" href="{url}" />']
    if path.name == "index.html":
        data = json.dumps(ORG, indent=2, ensure_ascii=False).replace("\n", "\n  ")
        lines.append(f'  <script type="application/ld+json">\n  {data}\n  </script>')
    lines.append("  <!-- SEO:END -->")
    return "\n".join(lines)


def main():
    done = 0
    for path in sorted(ROOT.glob("*.html")):
        if path.name in SKIP:
            continue
        html = path.read_text(encoding="utf-8")
        html = BLOCK.sub("", html)
        if "</title>" not in html:
            print(f"SKIPPED (no <title>): {path.name}")
            continue
        html = html.replace("</title>", "</title>\n" + build(path), 1)
        path.write_text(html, encoding="utf-8")
        done += 1
    print(f"Added canonical tags to {done} pages; Organization schema on index.html")


if __name__ == "__main__":
    main()
