# Video on Project Pages

Short version: **videos are never stored in this repo.** They live on RJB's
YouTube channel and get embedded. The repo only holds an 11-character video ID.

---

## Why not put the files in the repo

- GitHub hard-rejects any file over **100 MB**.
- A published GitHub Pages site is capped at **1 GB**; the source repo has the
  same recommended limit. This repo is already ~212 MB of git history plus
  121 MB of images.
- Git keeps **every version of a binary forever**. Replacing a video later does
  not shrink the repo — the old copy stays in history, and Kaylah's and Mary's
  clones both carry it permanently.
- Embedded video streams from YouTube, so it costs nothing against the Pages
  **100 GB/month** bandwidth soft limit.

---

## Uploading a video

1. Upload to the RJB YouTube channel.
2. Set visibility to **Unlisted** — the video works everywhere you embed it,
   but it won't show up in channel listings or YouTube search. (Use **Public**
   only if you also want it findable on YouTube.)
3. Copy the video ID from the URL — the part after `v=`:

   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
                                   ^^^^^^^^^^^  <- this is the ID
   ```

---

## Adding it to a project page

Run from the repo folder:

```bash
python3 tools/add_project_video.py project-02.html dQw4w9WgXcQ \
    --title "Queue Line Install Time-Lapse" \
    --caption "Overnight queue-line installation at a Kohl's location."
```

- `--title` becomes the section heading. Keep it short and plain.
- `--caption` is optional; it prints under the player.
- The section is inserted directly **above the Gallery** block.
- Re-running on the same page **replaces** the existing video.

To take a video off a page:

```bash
python3 tools/add_project_video.py project-02.html --remove
```

Then commit and push as usual.

---

## What the embed does

- Uses `youtube-nocookie.com`, so YouTube doesn't set tracking cookies until
  someone actually plays the video.
- `rel=0` keeps end-of-video suggestions to RJB's own channel instead of
  showing unrelated videos.
- `loading="lazy"` means the player doesn't load until a visitor scrolls to it,
  so it doesn't slow down the top of the page.
- Responsive 16:9 — scales cleanly down to phone width.

---

## Notes

- One video per project page. If a project needs more, make a YouTube playlist
  and embed that, or ask Claude to extend the tool.
- Captions are visible copy — same voice rules as the rest of the site. No hype,
  no invented client detail.
- Client footage may need approval before it goes public. Confirm before
  uploading anything showing a client's store, branding, or staff.
