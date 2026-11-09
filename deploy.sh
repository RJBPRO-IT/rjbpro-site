#!/usr/bin/env bash
# RJB Contracting — publish / update the live site
# ----------------------------------------------------
# Usage (from the "Creating Website" folder, in Terminal):
#     bash deploy.sh
#   or with your own note:
#     bash deploy.sh "Added new team photos"
#
# This commits everything and pushes to GitHub. Cloudflare Pages then
# rebuilds rjbpro.com automatically a minute or two later.
# (Publishing from GitHub Desktop works the same way.)

set -e
cd "$(dirname "$0")"

# Clear any stale lock left by an interrupted git run
rm -f ".git/index.lock" 2>/dev/null || true

# Regenerate the team section, then keep the SEO setup current
# (extensionless links, canonical tags + schema, sitemap).
# NOTE: tools/generate_blog.py is intentionally NOT run here. posts/ is out of
# sync with the live Insights pages, and running it would publish drafts and
# drop live posts. See CLAUDE.md before running it by hand.
if command -v python3 >/dev/null 2>&1; then
  if [ -f tools/generate_team_section.py ]; then echo "→ Rebuilding team section..."; python3 tools/generate_team_section.py >/dev/null; fi
  if [ -f tools/fix_internal_links.py ]; then echo "→ Fixing internal links..."; python3 tools/fix_internal_links.py; fi
  if [ -f tools/add_seo_head.py ]; then echo "→ Updating canonical tags and schema..."; python3 tools/add_seo_head.py; fi
  if [ -f tools/generate_sitemap.py ]; then echo "→ Rebuilding sitemap..."; python3 tools/generate_sitemap.py; fi
else
  echo "→ (python3 not found — skipping auto-regeneration; run the generators manually if needed)"
fi

echo "→ Staging all changes..."
git add -A

if git diff --cached --quiet; then
  echo "→ No new changes to commit. Pushing existing commits (if any)."
else
  MSG="${1:-Update site $(date '+%Y-%m-%d %H:%M')}"
  git commit -m "$MSG"
  echo "→ Committed: $MSG"
fi

echo "→ Pushing to GitHub (origin/main)..."
git push origin main

echo ""
echo "✅ Pushed. Cloudflare Pages rebuilds in ~1–2 minutes."
echo "   Live site: https://rjbpro.com"
echo "   Added, renamed or removed a page? Resubmit sitemap.xml in Search Console."
