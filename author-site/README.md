# [Author Name] — author site

A static site: plain HTML, one CSS file, no build step, no CMS. Every page
works if you just double-click it and open it in a browser — no server
required, locally or once it's live.

## Start here (before this goes live)

1. **Find-and-replace `[Author Name]`** across every file with your real name
   or pen name. It appears in the header, footer, and page titles on every
   page.
2. **Replace the placeholder email** in `contact.html` (`author@example.com`).
3. **Read through `books.html`, `worlds.html`, and the pages in `/books` and
   `/worlds`.** Four of the five books (everything except *The Ledger of a
   Single Sweetness* / Case 4099) use invented placeholder statuses, hooks,
   and synopses so the layout has something to show. Anything in italics,
   or called out in an HTML comment, is a note to you, not real copy —
   search for `editor-note` to find all of it.
4. **Swap in real cover art** when you have it — see
   `images/covers/README.md`.
5. **Add your bio** to `about.html` and the short version on `index.html`.

## Folder structure

```
author-site/
├── index.html          Homepage
├── books.html           All books
├── worlds.html          All worlds
├── about.html
├── contact.html
├── css/style.css        The only stylesheet — see "Customizing" below
├── images/
│   ├── covers/           Book cover art (placeholders included)
│   ├── characters/        Optional character portraits
│   └── backgrounds/       Optional hero background images
├── books/                One page per book
├── worlds/                One page per world
└── assets/                 favicon.svg / favicon.ico
```

## Adding a new book

1. Copy an existing file in `/books` (pick one with a similar status) and
   rename it to the new book's slug, e.g. `books/newbook.html`.
2. Edit the title, world link, status tags, synopsis, characters, and
   purchase links inside it.
3. Add a cover image to `images/covers/` (see that folder's README).
4. Add a matching entry to `books.html` (copy one `<article class="entry">`
   block and edit it) and, if you want it featured, to `index.html`.
5. Add it to the "Related Books" list on the relevant page in `/worlds`.

## Adding a new world

1. Copy an existing file in `/worlds` and rename it to the new world's slug.
2. Edit the overview, timeline, locations, and characters.
3. Add an entry to `worlds.html` and, if you like, the homepage's world
   index list.

## Updating navigation

The header and footer are repeated at the top and bottom of every file
(there's no shared template — that's the trade-off for having zero build
step). If you add or rename a nav item, you'll need to update it in every
HTML file. For a dozen-plus pages this is manageable with your editor's
find-and-replace; if the site grows a lot larger, that's the point at which
a static site generator might start to pay for itself — not needed for now.

## Customizing colors and fonts

Everything visual is controlled from the top of `css/style.css`, in the
`:root { ... }` block. Change a color there and it updates everywhere it's
used. The site currently loads one Google Font (Fraunces, for headings only)
and uses your system fonts for body text; the link is in the `<head>` of
every page if you'd rather remove it and go fully dependency-free.

## Images

See the `README.md` inside each `images/` subfolder for size and format
guidance. Short version: covers around 800×1200px, keep files under a few
hundred KB, and JPG/WebP for photos or painted art.

## Previewing locally

Just open `index.html` in a browser. Every link and asset uses a relative
path, so this works identically whether you're opening the file directly,
serving it locally, or viewing it live on the web.

## Deploying to GitHub Pages

1. Create a repository named exactly `<your-username>.github.io`.
2. Push the **contents** of this folder to the root of that repository's
   main branch (not this folder nested inside another one — the files
   listed above should sit at the repo root).
3. GitHub Pages usually turns itself on automatically for a repo named this
   way. If it doesn't, go to the repo's Settings → Pages and set the source
   to the main branch, root folder.
4. The site will be live at `https://<your-username>.github.io`.

A `.nojekyll` file is already included at the root — it tells GitHub Pages
to serve the files exactly as they are, skipping its default Jekyll
processing, which this site doesn't need.

## Moving to Cloudflare Pages later

Nothing about this structure is GitHub-specific, so the move is just a
hosting change: connect this same repository to Cloudflare Pages, leave the
build command empty, and set the output directory to the repo root. No
files need to move or change.
