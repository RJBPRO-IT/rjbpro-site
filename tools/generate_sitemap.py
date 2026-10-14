"""Generate sitemap.xml for https://rjbpro.com.

Lists every public .html page at its Cloudflare Pages pretty URL (no .html),
with <lastmod> from the file's last git commit. Re-run after adding/removing pages:
    python3 tools/generate_sitemap.py
"""
import pathlib, subprocess, datetime
BASE = "https://rjbpro.com"
root = pathlib.Path(__file__).resolve().parent.parent
EXCLUDE = {
    "404.html",
    "thank-you-contact.html", "thank-you-subcontractor.html",   # form confirmations
    "retail-construction.html", "warehouse-construction.html",  # legacy: 301'd in _redirects
    "asset-maintenance.html",
}
def lastmod(p):
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", p.name],
                         cwd=root, capture_output=True, text=True).stdout.strip()
    return out or datetime.date.today().isoformat()
urls = []
for p in sorted(root.glob("*.html")):
    if p.name in EXCLUDE:
        continue
    path = "/" if p.name == "index.html" else "/" + p.stem
    urls.append((path, lastmod(p)))
urls.sort(key=lambda u: (u[0] != "/", u[0]))
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, lm in urls:
    lines.append(f"  <url><loc>{BASE}{path}</loc><lastmod>{lm}</lastmod></url>")
lines.append("</urlset>")
(root / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote sitemap.xml ({len(urls)} URLs)")
