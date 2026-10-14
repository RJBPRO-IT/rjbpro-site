"""Build 404.html from thank-you-contact.html's nav/footer chrome.

Cloudflare Pages serves 404.html (with a real 404 status) for any unknown path.
Without it, Pages falls back to index.html with a 200 — the soft-404 problem.
All asset/link paths are made root-absolute because the 404 page can be served
at any depth (e.g. /old/wordpress/path/).
Re-run after nav/footer changes:  python3 tools/build_404.py
"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "thank-you-contact.html").read_text(encoding="utf-8")

head_new = '''<meta name="robots" content="noindex" />
  <meta name="description" content="Page not found." />
  <title>Page Not Found | RJB Contracting</title>'''
src = re.sub(r'<meta name="description"[^>]*/>\s*<title>.*?</title>', head_new, src, flags=re.S)

body_new = '''<!-- 404 -->
  <section class="content-section" style="padding:8rem 0;">
    <div class="content-inner" style="text-align:center;max-width:640px;">
      <div class="section-label">Page Not Found</div>
      <h1 class="t-section-head" style="margin-bottom:1.25rem;">This page isn't here.</h1>
      <p class="t-body" style="font-size:1.1rem;">The link may be out of date, or the address may have a typo. Some pages moved when we rebuilt our site.</p>
      <p class="t-body">Start from the homepage, or reach out and we'll point you in the right direction.</p>
      <div style="margin-top:2rem;display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
        <a href="index.html" class="btn btn-orange btn-arrow">Back to Home</a>
        <a href="projects.html" class="btn btn-outline">See Our Projects</a>
        <a href="contact-us.html" class="btn btn-outline">Contact Us</a>
      </div>
    </div>
  </section>'''
src, n = re.subn(r'<!-- CONFIRMATION -->.*?</section>', body_new, src, flags=re.S)
assert n == 1, "confirmation block not found"

# Root-absolute paths for local links/assets (leave http(s), mailto, #, / alone)
src = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|/)([^"]+)"', r'\1="/\2"', src)
src = src.replace('href="/index.html"', 'href="/"')

(root / "404.html").write_text(src, encoding="utf-8")
print("wrote 404.html")
