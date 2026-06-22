# GitHub Pages Setup — RJB Contracting Website

## Repo & deploy in ~5 minutes

### Step 1 — Create a new GitHub repo
1. Go to github.com → **New repository**
2. Name it `rjbpro-site` (or whatever you prefer)
3. Set to **Public**
4. Do NOT initialize with a README — leave it empty
5. Click **Create repository**

### Step 2 — Push your files
Open Terminal in the `Creating Website` folder and run:

```bash
git init
git add .
git commit -m "Initial site build"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/rjbpro-site.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

### Step 3 — Enable GitHub Pages
1. In your repo, go to **Settings → Pages**
2. Under **Source**, select **Deploy from a branch**
3. Branch: `main` / Folder: `/ (root)`
4. Click **Save**
5. GitHub will show you your live URL (usually `https://YOUR-USERNAME.github.io/rjbpro-site/`)

Allow 1–2 minutes for the first deploy.

---

## File structure

```
/
├── index.html               ← Homepage
├── about-us.html
├── retail-construction.html
├── warehouse-construction.html
├── asset-maintenance.html
├── projects.html
├── insights.html
├── careers.html
├── contact-us.html
├── subcontractors.html
├── css/
│   └── styles.css
└── fonts/
    ├── Museo700-Regular.otf
    ├── yantramanav-regular.otf
    ├── yantramanav-bold.otf
    ├── yantramanav-black.otf
    ├── yantramanav-medium.otf
    ├── yantramanav-light.otf
    └── yantramanav-thin.otf
```

---

## Swapping placeholder photos

Every hero and card image uses Unsplash URLs — search for the comment `<!-- replace with your photo -->` or look for `images.unsplash.com` in each HTML file. Replace those `src=` values with your own images once you have them.

For local images, drop them in an `/images/` folder and update the paths accordingly.

---

## Custom domain (rjbpro.com)

Once your site is live on GitHub Pages:
1. Go to **Settings → Pages → Custom domain**
2. Enter `rjbpro.com`
3. In your DNS provider, add:
   - `A` records pointing to GitHub's IPs: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - Or a `CNAME` record: `www` → `YOUR-USERNAME.github.io`
4. Check **Enforce HTTPS** once DNS propagates (can take up to 48 hrs)
