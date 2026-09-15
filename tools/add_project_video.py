#!/usr/bin/env python3
"""
Add (or replace) a YouTube video section on a project page.

The section is inserted directly ABOVE the Gallery block, so it reads:
  Project Details -> body copy -> Video -> Gallery

Usage:
  python3 tools/add_project_video.py project-02.html dQw4w9WgXcQ \
      --title "Queue Line Install Time-Lapse" \
      --caption "Overnight queue-line installation at a Kohl's location."

  # remove a video section
  python3 tools/add_project_video.py project-02.html --remove

Notes:
  - Videos are NOT stored in this repo. They live on RJB's YouTube channel
    and are embedded. See VIDEO-GUIDE.md.
  - Use the 11-character YouTube ID, not the full URL.
    https://www.youtube.com/watch?v=dQw4w9WgXcQ  ->  dQw4w9WgXcQ
"""
import argparse, re, sys, pathlib

START = "<!-- VIDEO:START -->"
END = "<!-- VIDEO:END -->"
GALLERY_ANCHOR = '      <div class="project-gallery">'


def build(video_id, title, caption):
    cap = f'\n        <p class="video-caption">{caption}</p>' if caption else ""
    return f"""      {START}
      <div class="project-video">
        <h2>{title}</h2>
        <div class="video-embed">
          <iframe
            src="https://www.youtube-nocookie.com/embed/{video_id}?rel=0"
            title="{title}"
            loading="lazy"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            referrerpolicy="strict-origin-when-cross-origin"
            allowfullscreen></iframe>
        </div>{cap}
      </div>
      {END}

"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", help="e.g. project-02.html")
    ap.add_argument("video_id", nargs="?", help="11-char YouTube ID")
    ap.add_argument("--title", default="Project Video")
    ap.add_argument("--caption", default="")
    ap.add_argument("--remove", action="store_true")
    a = ap.parse_args()

    path = pathlib.Path(a.page)
    if not path.exists():
        sys.exit(f"ERROR: {path} not found")
    html = path.read_text()

    # strip any existing video section first
    existing = re.search(r"[ \t]*" + re.escape(START) + r".*?" + re.escape(END) + r"\n*", html, re.S)
    if existing:
        html = html[:existing.start()] + html[existing.end():]
        print(f"  removed existing video section from {path.name}")

    if a.remove:
        path.write_text(html)
        print(f"DONE: {path.name} has no video section")
        return

    if not a.video_id:
        sys.exit("ERROR: video_id required (or pass --remove)")
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", a.video_id):
        sys.exit(f"ERROR: '{a.video_id}' is not a valid 11-character YouTube ID.\n"
                 f"       Use just the ID, not the full URL.")
    if GALLERY_ANCHOR not in html:
        sys.exit(f"ERROR: no gallery block found in {path.name}; can't place the video.")

    # Insert above the gallery. If the gallery carries a leading HTML comment,
    # go above that too so the comment stays attached to the gallery it describes.
    anchor = GALLERY_ANCHOR
    m = re.search(r"([ \t]*<!--\s*GALLERY\b.*?-->\n)" + re.escape(GALLERY_ANCHOR), html, re.S)
    if m:
        anchor = m.group(0)
    html = html.replace(anchor, build(a.video_id, a.title, a.caption) + anchor, 1)
    path.write_text(html)
    print(f"DONE: added video {a.video_id} to {path.name}")


if __name__ == "__main__":
    main()
