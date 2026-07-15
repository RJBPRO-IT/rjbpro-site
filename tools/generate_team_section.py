#!/usr/bin/env python3
"""
Generate the "Meet the Team" section of about-us.html from team.json.

Source of truth:   team.json   (edit this: names, titles, order, photos)
Targets (rewritten): about-us.html  (between the TEAM:START / TEAM:END markers)
                     images/PHOTO-DOWNLOAD-LIST.md
                     tools/download_photos.sh

Usage:
    python3 tools/generate_team_section.py            # auto-detect project root
    python3 tools/generate_team_section.py --root /path/to/site

Re-running is safe (idempotent): it only replaces content between the markers.
On first run, if the markers are absent, it rebuilds the #leadership section
(preserving the id so the footer "Leadership" link keeps working) and inserts them.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

MARK_START = ('<!-- TEAM:START - auto-generated from team.json by '
              'tools/generate_team_section.py. Edit team.json and re-run; '
              'do not hand-edit between the markers. -->')
MARK_END = '<!-- TEAM:END -->'


def find_root(explicit: str | None) -> Path:
    """Locate the project root (the folder containing about-us.html)."""
    candidates = []
    if explicit:
        candidates.append(Path(explicit).resolve())
    here = Path(__file__).resolve()
    candidates += [Path.cwd().resolve(), here.parent, here.parent.parent]
    for start in candidates:
        for d in [start, *start.parents]:
            if (d / 'about-us.html').is_file() and (d / 'team.json').is_file():
                return d
    sys.exit('ERROR: could not find a folder containing both about-us.html and '
             'team.json. Pass --root /path/to/site.')


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def build_inner(data: dict) -> str:
    """Build the HTML that lives between the markers (label + heading + groups)."""
    sec = data.get('section', {})
    blurb = sec.get('blurb', '').strip()
    head_margin = '1rem' if blurb else '3rem'
    lines = [
        f'      <div class="section-label">{esc(sec.get("label", "Meet the Team"))}</div>',
        f'      <h2 class="t-section-head" style="margin-bottom:{head_margin};">'
        f'{esc(sec.get("heading", "The team behind the teams."))}</h2>',
    ]
    if blurb:
        lines.append(f'      <p class="t-body" style="max-width:640px;'
                     f'margin-bottom:3rem;">{esc(blurb)}</p>')
    for group in data['groups']:
        members = group.get('members', [])
        if not members:
            continue
        lines.append('      <div class="team-section-group">')
        if group.get('name'):
            lines.append(f'        <h3 class="team-group-label">{esc(group["name"])}</h3>')
        lines.append('        <div class="team-grid">')
        for m in members:
            alt = esc(f'{m["name"]}, {m["title"]}')
            lines.append('          <article class="team-card">')
            lines.append('            <div class="team-card-photo">')
            lines.append(f'              <img src="images/{esc(m["file"])}" '
                         f'alt="{alt}" loading="lazy" />')
            lines.append('            </div>')
            lines.append(f'            <h4 class="team-card-name">{esc(m["name"])}</h4>')
            lines.append(f'            <p class="team-card-title">{esc(m["title"])}</p>')
            lines.append('          </article>')
        lines.append('        </div>')
        lines.append('      </div>')
    return '\n'.join(lines)


def write_section(root: Path, inner: str) -> str:
    html_path = root / 'about-us.html'
    content = html_path.read_text(encoding='utf-8')
    block = f'      {MARK_START}\n{inner}\n      {MARK_END}'

    if 'TEAM:START' in content:
        new_content = re.sub(r'<!-- TEAM:START.*?TEAM:END -->',
                             lambda _: block.strip(), content,
                             count=1, flags=re.S)
        mode = 'updated (between markers)'
    else:
        new_section = (
            '  <!-- MEET THE TEAM - auto-generated from team.json '
            '(see tools/generate_team_section.py) -->\n'
            '  <section class="content-section content-section--gray" id="leadership">\n'
            '    <div class="content-inner">\n'
            f'{block}\n'
            '    </div>\n'
            '  </section>'
        )
        pat = (r'(?:[ \t]*<!-- MEET THE TEAM.*?-->\n)?'
               r'[ \t]*<section[^>]*id="leadership">.*?</section>')
        new_content, n = re.subn(pat, lambda _: new_section, content,
                                 count=1, flags=re.S)
        if n == 0:
            sys.exit('ERROR: no TEAM markers and no <section id="leadership"> found '
                     'in about-us.html. Add <!-- TEAM:START --><!-- TEAM:END --> '
                     'where the section should go.')
        mode = 'inserted (rebuilt #leadership section + added markers)'

    html_path.write_text(new_content, encoding='utf-8')
    return mode


def write_photo_assets(root: Path, data: dict) -> int:
    members = [m for g in data['groups'] for m in g['members']]
    md = ['# Team Photo Download List', '',
          f'{len(members)} photos. Save each into the `images/` folder using the '
          '**Save as** name (the site references these exact filenames).', '',
          'Quickest path: run `bash tools/download_photos.sh` from the project root.', '',
          '| # | Name | Save as | Source |',
          '|---|------|---------|--------|']
    sh = ['#!/usr/bin/env bash',
          '# Auto-generated by tools/generate_team_section.py',
          '# Downloads all team photos into images/ with standardized names.',
          '# Usage:  bash tools/download_photos.sh',
          'cd "$(dirname "$0")/.." || exit 1',
          'mkdir -p images',
          'dl() { echo "downloading $2"; curl -fL --retry 2 -o "images/$2" "$1" '
          '|| echo "  WARNING: failed -> $2"; }', '']
    for i, m in enumerate(members, 1):
        md.append(f'| {i} | {m["name"]} | `images/{m["file"]}` | {m["src"]} |')
        sh.append(f'dl "{m["src"]}" "{m["file"]}"')
    sh.append('echo "Done. Review images/ for any WARNING lines above."')

    (root / 'images').mkdir(exist_ok=True)
    (root / 'images' / 'PHOTO-DOWNLOAD-LIST.md').write_text('\n'.join(md) + '\n',
                                                            encoding='utf-8')
    sh_path = root / 'tools' / 'download_photos.sh'
    sh_path.write_text('\n'.join(sh) + '\n', encoding='utf-8')
    sh_path.chmod(0o755)
    return len(members)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', help='Project root (folder with about-us.html & team.json)')
    args = ap.parse_args()

    root = find_root(args.root)
    data = json.loads((root / 'team.json').read_text(encoding='utf-8'))

    inner = build_inner(data)
    mode = write_section(root, inner)
    count = write_photo_assets(root, data)

    groups = [g['name'] for g in data['groups'] if g.get('members')]
    print(f'OK  root: {root}')
    print(f'OK  about-us.html {mode}')
    print(f'OK  {count} members across {len(groups)} groups: {", ".join(groups)}')
    print('OK  wrote images/PHOTO-DOWNLOAD-LIST.md and tools/download_photos.sh')


if __name__ == '__main__':
    main()
