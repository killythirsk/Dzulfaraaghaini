# Dzulfaraaghaini — author site

A static site: plain HTML, one CSS file, one small JS file, no build step,
no CMS. Every page works if you just double-click it and open it in a
browser — no server required, locally or once it's live.

**Working with an AI on this project?** Point it at `AI-HANDOFF.md` first —
it has the full technical and story context so you don't have to re-explain
the project from scratch each time.

## Where things stand

Four books are live: *The Sword of Valeria* (Case 0000) — real cover,
synopsis, a full cast of 10 characters, an 8-image scene gallery, and
working "View on Google Books" / "Read on Royal Road" links — *The Ledger
of a Single Sweetness* (Case 4099) — real cover, synopsis, a full cast of
28 characters, a 19-image scene gallery, a confirmed page count (99) and
genre, and a working "View on Google Books" link — *The Stolen Prince
War* (Case 0157) — real cover, synopsis, a full cast of 35 characters, a
19-image scene gallery, a confirmed page count (96), and a working "View
on Google Books" link — and *The Iron Stiletto War* (Case 4417) — real
cover, synopsis, a full cast of 13 characters, a 4-image
scene gallery, and a working "View on Google Books" link, and a confirmed page count (109). The Lore glossary has
two entries, Cultivator (listing every Envoy) and Catalyst (listing every
Catalyst), each built automatically from the books' own data. Images
enlarge on click, and you can step between them without closing the view;
a book's Scenes gallery (when it has one) slides sideways, its Characters
list scrolls normally. Images are protected against casual saving (right-click
and dragging are blocked, and full-size files aren't linked directly) — a
deterrent, not a lock: anything a browser can display can still be captured.

Still open:
- Four of "more than a dozen" novels are live — more can be added the
  same way these were.

## Making changes

**The HTML pages are generated, not hand-written.** `tools/build_site.py`
holds all the page content — including each book's own characters and
scenes, nested right inside that book's entry — and produces every
`.html` file when run:

```
cd tools
python3 build_site.py
```

Run it from inside the `tools/` folder specifically — it figures out
where the rest of the project lives relative to its own location, and
running a copy of it from somewhere else will write files to the wrong
place.

Edit the content inside the script (a character's bio, a synopsis, nav
labels, whatever), then re-run it — don't edit the `.html` files directly,
since the next regeneration will overwrite those edits. If you don't have
a way to run Python, hand-editing the HTML files is still possible (it's
plain HTML), just know the script will be out of sync afterward.

## Folder structure

```
author-site/
├── index.html          Homepage
├── books.html           All books
├── lore.html             Glossary of setting terms/systems
├── about.html             Biography
├── contact.html
├── AI-HANDOFF.md          Full context for an AI continuing this project
├── css/style.css        The only stylesheet — see "Customizing" below
├── js/site.js             Lightbox, scene slider, scroll animation
├── images/
│   ├── covers/           Book cover art
│   ├── characters/        Character portraits (full + small "-thumb" size)
│   ├── scenes/             Gallery art (full + smaller "-grid" size)
│   └── backgrounds/       Optional hero background images (unused so far)
├── books/                One page per book
├── lore/                  One page per glossary term
├── characters/             One page per character, across every book
├── tools/build_site.py     The generator — see "Making changes" above
└── assets/                 favicon.svg / favicon.ico
```

Note on images: everything you upload gets resized and re-compressed
before it's used (originals often run several MB; site copies run well
under 1MB) so the site stays fast. Keep your original files somewhere of
your own — they aren't kept in this project.

## Adding a new book, character, or lore entry

Open `tools/build_site.py`. Books live in the `BOOKS` list near the top —
each book is its own entry with its own nested `"characters"` and
`"scenes"` lists right inside it (a character or scene belongs to one
book, not to the whole site). To add a new book, copy the shape of an
existing entry in `BOOKS`, including its own character/scene lists. To add
a character or scene to a book that already exists, add an entry to that
specific book's `"characters"` or `"scenes"` list. Lore terms are
separate — they live in their own `LORE` list, since they're meant to
apply across books. Regenerate afterward; every page, and every link
between pages, gets created automatically — you don't need to touch any
HTML by hand.

For images: drop the new cover/portrait/scene file into the matching
`images/` subfolder first (resized per the note above), then reference its
filename in the script entry.

## Updating navigation

The header and footer repeat at the top and bottom of every generated
page, but since they're produced by one function in `build_site.py`
(`header_html` / `footer_html`), changing the nav means editing that one
function and regenerating — not hunting through every file by hand.

## Customizing colors and fonts

Everything visual is controlled from the top of `css/style.css`, in the
`:root { ... }` block. Change a color there and it updates everywhere it's
used. The palette is deliberately cool/grey rather than warm parchment, so
illustrated covers with warm, aged-paper tones (like all four current
ones) read as distinct objects against the page instead of blending into it —
keep that contrast in mind if you retheme it later. The site loads one
Google Font (Fraunces, for headings only) and uses your system fonts for
body text; the link is in the `<head>` of every page if you'd rather
remove it and go fully dependency-free.

## Previewing locally

Just open `index.html` in a browser. Every link and asset uses a relative
path, so this works identically whether you're opening the file directly,
serving it locally, or viewing it live on the web.

## Deploying to GitHub Pages

1. Create a repository named exactly `<your-username>.github.io`.
2. Upload the **contents** of this folder — `index.html`, `css/`,
   `images/`, `books/`, `lore/`, `characters/`, `js/`, `tools/`, etc. —
   directly into the root of that repository. **Not** this folder nested
   one level deeper.
   - If you're using GitHub's "Add file → Upload files" button in the
     browser: drag in the individual top-level files and folders so they
     land side by side at the repo root. Dragging a single outer folder
     that contains all of these is what causes things to end up nested one
     level too deep and not load.
   - After uploading, open the repo on GitHub.com and confirm `index.html`
     and the `css` folder are sitting at the same level — if you see an
     extra folder wrapping everything, open it and move its contents up to
     the repo root instead.
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
