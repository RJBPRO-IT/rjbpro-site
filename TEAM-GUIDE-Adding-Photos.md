# Adding Photos to the RJB Website — Team Guide

This guide is for adding and updating photos on the RJB Contracting website. You don't need to know any code. You'll use a free app called **GitHub Desktop** that does everything with buttons.

Quick division of labor: **you handle photos, Kaylah handles website copy.** Those are different files, so you can both work at the same time without stepping on each other.

---

## One-time setup (about 10 minutes)

1. **Accept the invite.** Kaylah will add you to the project on GitHub. Check your email for an invitation from GitHub and click **Accept**.
2. **Install GitHub Desktop** from https://desktop.github.com — install it and sign in with your GitHub account.
3. **Download the website to your computer:**
   - In GitHub Desktop: **File → Clone repository**
   - Pick **rjbpro/rjbpro-site** from the list
   - Choose where to save it on your computer, then click **Clone**

You now have your own copy of the site.

---

## Every time you add photos

1. **Get the latest first.** Open GitHub Desktop and click **Fetch origin** (and **Pull** if it offers). This pulls in Kaylah's latest changes so you're never out of date.
2. **Open the photos folder.** In GitHub Desktop: **Repository → Show in Finder** (Mac) or **Show in Explorer** (Windows). Open the **`images`** folder.
3. **Compress your photos first.** Go to https://squoosh.app, drop a photo in, and save it smaller — aim for **under 300 KB** for cards and **under 500 KB** for big banner images. Large files slow the site down.
4. **Name each file exactly right** (see naming rules below) and drop it into the `images` folder.
5. **Save your work back to GitHub:**
   - Switch back to GitHub Desktop — your new photos show up in the list on the left.
   - Type a short note in the **Summary** box, like `Add Director team photos`.
   - Click **Commit to main**, then click **Push origin** (top-right).
6. **Done.** The live site updates by itself about a minute later.

---

## Naming rules (this part matters most)

The site only finds a photo if the filename is **exactly** right. Always use **lowercase letters, hyphens instead of spaces, and no capital letters or spaces.**

Most common ones:

| What it's for | Name it | Size (px) |
|---|---|---|
| Team member photo | `team-firstname-lastname.jpg` | square-ish (1:1) |
| Project page banner | `project-01-hero.jpg` (01–06) | 1800 × 600 |
| Project gallery photo | `project-01-gallery-1.jpg`, `-2.jpg`, … | 800 × 600 |
| Project thumbnail (Projects page) | `project-01.jpg` (01–06) | 600 × 450 |

**The complete list of every photo slot** — page banners, service pages, sector pages, and more — lives in the file **`images/PHOTO-GUIDE.md`** inside the project. Open it for the exact name and size of any image on the site.

---

## Good habits

- **Pull before you start, push when you finish.**
- **Only touch the `images` folder.** Leave the `.html`, `.css`, and other files alone — Kaylah is working on those.
- **Don't rename or delete existing files** unless Kaylah asks.
- If GitHub Desktop ever shows a **"conflict,"** or anything looks off, **stop and message Kaylah** — don't force it.

---

## "I added my photo but I don't see it on the site"

Check these in order:

1. Did you **Push** in GitHub Desktop, and wait about a minute?
2. Is the **filename exactly right** — lowercase, hyphens, and the correct slot name?
3. **Hard refresh** the page: **⌘ + Shift + R** (Mac) or **Ctrl + Shift + R** (Windows), or open it in a private/incognito window.
4. A few photo spots (the Projects page thumbnails and the project galleries) currently use temporary placeholder images and need a one-time switch before your photo shows. If you've done everything right and it still doesn't appear, **tell Kaylah** and she'll flip it on.

Check your work at: **https://rjbpro.github.io/rjbpro-site/**

---

*Questions? Message Kaylah. When in doubt, don't force anything — it's easy to fix as long as nothing gets overwritten.*
