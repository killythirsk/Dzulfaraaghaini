# Dzulfaraaghaini — author site

A static site: plain HTML, one CSS file, one small JS file, no build step,
no CMS. Every page works if you just double-click it and open it in a
browser — no server required, locally or once it's live.

**Working with an AI on this project?** Point it at `AI-HANDOFF.md` first —
it has the full technical and story context so you don't have to re-explain
the project from scratch each time.

## Where things stand

Nine books are live. The first four: *The Sword of Valeria* (Case 0000) — real cover,
synopsis, a full cast of 10 characters, an 8-image scene gallery, and
working "View on Google Books" / "Read on Royal Road" links — *The Ledger
of a Single Sweetness* (Case 4099) — real cover, synopsis, a full cast of
28 characters, a 19-image scene gallery, a confirmed page count (99) and
genre, and a working "View on Google Books" link — *The Stolen Prince
War* (Case 0157) — real cover, synopsis, a full cast of 35 characters, a
19-image scene gallery, a confirmed page count (96), and a working "View
on Google Books" link — and *The Iron Stiletto War* (Case 4417) — real
cover, synopsis, a full cast of 13 characters, a 4-image
scene gallery, and a working "View on Google Books" link, and a confirmed page count (109). Five more are live but not described in detail here: *The Vessel of the Betrayed Host* (Case 4420), *The Vessel
of Unmediated Grace* (Case 4555), *The Heavenly Thunder-Serpent* (Case
4438 — real cover, synopsis, a full cast of 19 characters, a 15-image scene
gallery, a working "View on Google Books" link and a confirmed page count of 82) and *The Decree of Luminescence* (Case 2365 — real cover, a full cast of 24 characters, a 15-image scene gallery, 15 records, a working "View on Google Books" link and a confirmed page count of 88 and a genre of Fiction / Fantasy / Historical) and *The Second Hand* (Case 1153 — real cover, a full cast of 19 subjects, 13 records, a working "Read on Google Books" link, 77 pages, genre Fiction / Fantasy / Epic and a synopsis). Nine further books, 0156 (*The Purging of Charsianon*), 0188, 2140, 3115,
0000B, 2231 (*The Stone of the Clean Hand*, with 43 subjects and 14 records), 0247 (*The Tear of the Dragon*, with 17 subjects and 11 records) and 1268
(*Independent Observation*, with 11 subjects, 15 records and a cover), 0202 (*Fossa*, with 27 subjects and 10 records) and 3001
(*The Uncounted Dinar*, with 13 subjects and a cover), are
marked coming-soon but already carry character rosters, and four
more (3312, 3887, 4442, 2114) are cover-only coming-soon entries. The
Lore glossary has eight entries: Cultivator (listing every Envoy) and
Catalyst (listing every Catalyst), each built automatically from the
books' own data, plus three religions — the Faith of Ardwen, the
Threefold Crown, and the Decree of Luminescence — under their own
Religion heading, and three gazetteers (maps with a note on each place) —
Illumaria, shared by Cases 2365 and 4555, the Iron Stiletto War
(Case 4417) and the Vessel of the Betrayed Host (Case 4420) — under a Gazetteers heading; a case page links to its map. Every page's footer shows when the site was last built
(GMT+7), stamped automatically each time `tools/build_site.py` runs. Images
enlarge on click, and you can step between them without closing the view;
a book's Scenes gallery (when it has one) slides sideways, its Characters
list scrolls normally. Images are protected against casual saving (right-click
and dragging are blocked, and full-size files aren't linked directly) — a
deterrent, not a lock: anything a browser can display can still be captured.

Still open:
- Nine of "more than a dozen" novels are live — more can be added the
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
├── records/                One page per record (scene), 197 so far; the share target for a record
├── sitemap.xml / robots.txt   Generated by the build; see "Link previews" below
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

## Change Log

One entry per part: `[PENDING] Part NNNN` while it exists only in a slave's zip, `[MERGED]` once the master has appended it.

### [MERGED] Part 3115 — Case 3115, *The Listening Water*: 24-character roster

Added:
- `characters/` — 24 pages: cao, chunhui, duan, huairen, huaiyu, jian, meilan, mingxuan, observer-471, peizhi, rao, suyin, the-custodian, the-herald, the-kitchen-boy, the-listening-water, the-physician, the-scribes-apprentice, the-soldier-who-killed-huaiyu, the-under-steward, xiaobao, yancheng, yanshuis-third-son, zhuo
- `images/characters/` — 48 files: a portrait and a `-thumb` for each of those 24 slugs

Edited (re-applied to master's own copies; nothing overwritten from the part):
- `tools/build_site.py` — Case 3115's `BOOKS` entry replaced (catalyst *The Listening Water*, envoy Observer 471 "the Salt-Root Woman", 24 characters; `pages`, `genre`, `synopsis_html` and `status` untouched, so the book stays coming-soon); one sentence added to the Cultivator lore text and one to the Catalyst lore text
- `books/3115.html`, `index.html`, `lore/cultivator.html`, `lore/catalyst.html` — regenerated from the script
- `AI-HANDOFF.md` — the slave's 3115 notes carried in (Book write-up in §6, open-items bullet in §7, merge note in §8); site-map character total, lore-roster paragraph and merge labels updated to match
- `README.md` — this entry
- every other page — footer "Site last built" stamp only

Totals: cases 12 -> 12, characters 132 -> 156, scenes 90 -> 90. A recount from the merged site gives the same figures.

Merged: 2026-09-30, 04:36PM GMT+7 - as logged, except: (1) this part's README carried no `[PENDING] Part 3115` entry (first run of the change-log process), so the log was taken from the 3115 write-up in the part's own `AI-HANDOFF.md`, on the author's instruction; (2) that write-up itemises only the generated pages, not `tools/build_site.py`, `AI-HANDOFF.md`, `README.md` or the footer stamp; (3) its "existing 107 characters" was stale (the part was built on 105, master held 132) and reads 132 in master's copy, with the slug-collision check re-run against those 132 (none).

### [MERGED] Part 4438 — Case 4438, *The Heavenly Thunder-Serpent*, plus Cases 0000B and 2114 and a new Case 4420 cover

Added:
- `books/4438.html`, `books/0000b.html`, `books/2114.html` — new book pages
- `characters/` — 19 pages: yue, yongkang-emperor, physician-kao, zheng-kui, zhou-xuan, du-heng, elder-peng, fu-baishi, meng-kuo, sun-lin, mei-suwen, kang-yi, ren-duo, the-heavenly-thunder-serpent, wan-er, pei-rong, yun-wei, master-bai, zhuo-sheng
- `images/characters/` — 38 files: a sheet and a `-thumb` for each of those 19 slugs
- `images/scenes/` — 30 files: a full image and a `-grid` for each of 15 scenes
- `images/covers/` — `4438.jpg`, `0000b.jpg`, `2114.jpg`

Edited:
- `images/covers/4420.jpg` — replaced with the new cover (same name, same 900x1350)
- `tools/build_site.py` — Case 4438's `BOOKS` entry added after 4555 (catalyst, envoy Observer 403, 19 characters, 15 scenes, Google Books link; `pages` left as the placeholder); `0000b` and `2114` stubs appended after 4442; `HOME_SCENES` gained `the-solstice-ascension`; one sentence each added to the Cultivator and Catalyst lore prose
- `books.html`, `index.html`, `lore/cultivator.html`, `lore/catalyst.html` — regenerated from the script
- `AI-HANDOFF.md` — Book write-up for 4438 and the two stubs in §6, open items in §7, merge note in §8; site-map counts and lore-roster paragraph updated
- `README.md` — this entry and the "Where things stand" paragraph
- every other page — footer "Site last built" stamp only

Totals: cases 12 -> 15, characters 156 -> 175, scenes 90 -> 105. A recount from the rebuilt site gives the same figures.

Merged: 2026-10-01, straight into master at the author's request (no staging copy, so no `[PENDING]` entry existed).

### [MERGED] Redesign — archive theme (dark ink / parchment / gold)

Edited: `css/style.css` (palette, fonts, new section 12), `tools/build_site.py` (fonts link, header star mark, home hero + counts, footer quote), `AI-HANDOFF.md` (§3 note), `README.md` (this entry); all pages regenerated. Added: `images/backgrounds/hero.jpg`.
Also added: `characters.html`, `scenes.html` (new top-level index pages with search and case filters), a Featured Case block on the home page, and a mobile menu; nav is now Home / Books / Characters / Scenes / Lore / About / Contact.
Also: CSS and JS links now carry `?v=<build time>` so browsers and the GitHub Pages cache cannot serve a stale stylesheet after a deploy.
Also: the star mark is replaced by the author's calligraphy logo — `assets/logo-gold.png` (hero) and `assets/logo-gold-sm.png` (header) are gold-on-transparent for the dark UI; `assets/logo.png` is the same logo in its original ink colours, transparent, for light backgrounds.
Fixed: the home page Featured Case no longer reuses `.entry-fileno` (the cover-less placeholder box); it has its own `.featured-label` / `.featured-title`.

### [MERGED] Case-archive pass — Cases / Subjects / Records / Archive

Edited: `tools/build_site.py` (nav + labels, `PRINCIPALS`, `RELATED_THEMES`, case grids, READ buttons, subject split, related-cases logic, page templates), `css/style.css` (section 14), `js/site.js` (mobile "see more", `?case=` filter link), `AI-HANDOFF.md` (§3 note), `README.md` (this entry); all pages regenerated.
Changed: nav and headings now read Cases / Subjects / Records / Archive (file names and URLs unchanged); the hero button is centred; published and awaiting-release cases are separate sections; every case page has a READ button at the top and bottom, principal subjects with the rest folded away, and Related Cases; subject and archive pages gained related blocks; long segments fold behind "See more" on phones.
Totals unchanged: cases 15, characters 175, scenes 105.

### [MERGED] Update — Case 4438 page count, Case 0000B cast, new Case 0156 (*The Purging of Charsianon*)

Added:
- `books/0156.html` — new book page (awaiting release)
- `characters/` — 45 pages: 19 for Case 0000B (the-anchorite, aveline, halvard, vasarion, aimeric, ganeth, kest, massinen, berant, dorenzo, corse-0000b, wendrics-wife, wendrics-son, yorbulan, branimir, coren, verrin, the-wounded-archer, the-vault-guard) and 26 for Case 0156 (bardas, theodora, the-carbon-echo, the-quiet-one, keeper-photios, lord-leo, kyr-symeon, kyr-niketas, kyr-andronikos, loukas, melias, brother-ignatios, georgios, petros, basileios, artavasdos, marina, zoe, stephanos, ioannes, theoktistos, kassia, isidoros, lord-constantine, lady-anastasia, ardwen-0156)
- `images/characters/` — 90 files: a sheet and a `-thumb` for each of those 45 slugs
- `images/scenes/` — 28 files: a full image and a `-grid` for each of 14 scenes
- `images/covers/` — `0156.jpg`

Edited:
- `tools/build_site.py` — Case 4438's `pages` set to 82; 19 characters added to the `0000b` stub; Case 0156's `BOOKS` entry added after 3115 (catalyst *The Carbon Echo*, envoy The Quiet One, 26 characters, 14 scenes; `pages`, `genre` and `synopsis_html` left as placeholders, so the book stays awaiting-release); `PRINCIPALS` gained `0156` and `0000b`; one sentence each added to the Cultivator and Catalyst lore prose and one to the Faith of Ardwen's appearances
- `books/4438.html`, `books/0000b.html`, `books.html`, `index.html`, `characters.html`, `scenes.html`, `lore/cultivator.html`, `lore/catalyst.html`, `lore/faith-of-ardwen.html` — regenerated from the script
- `AI-HANDOFF.md` — Book write-up for 0156 and the 0000B cast in §6, §7 bullets, merge note in §8; counts updated
- `README.md` — this entry and the "Where things stand" paragraph
- every other page — footer "Site last built" stamp only

Totals: cases 15 -> 16, characters 175 -> 220, scenes 105 -> 119. A recount from the rebuilt site gives the same figures, and every local link resolves.

Merged: 2026-10-07, straight into master at the author's request (no staging copy, so no `[PENDING]` entry existed).

### [MERGED] Update — where to begin, record lines, share buttons, link previews

Added:
- Home page **Where to begin** block (`#begin`, the last section of the page, linked from the hero button): says there is no first book, each case stands alone and all are connected, then lists the seven published cases by their hook with case and genre. Published case pages carry a one-line "Stands alone" note; the Cases page says the same under its intro.
- Every record (scene) now has a descriptive line, `Subject / Archive` (e.g. *Subject* The Principal Handmaid / *Archive* Case 4099), on the case page, the Records index and its own page. Subjects come from the characters the record's caption links to, or from an optional `"subjects": [slugs]` list on the scene; 36 of 119 records name no subject because their captions link to no one.
- `records/<slug>.html` — 119 new pages, one per record, so a shared record link has its own preview. Each shows the image, the Subject/Archive line, previous/next record and a link to read the case.
- One **Share** button on every case page, subject page and record (case page slider, Records index, record page). Uses the device share sheet where there is one, otherwise copies the link; hidden until `js/site.js` runs.
- Canonical link, Open Graph and Twitter tags on every page except the old redirect stub (case page: cover; subject page: reference sheet; record: the record image; everything else: `images/backgrounds/hero.jpg`). Descriptions for About, Contact, Home, Cases, subject and record pages were rewritten to read well in a preview.
- `sitemap.xml` (367 pages) and `robots.txt`, written by the build.

Edited: `tools/build_site.py` (new `SITE_URL` constant, `head_html`/`page` take `path`/`image`, new helpers `share_btn`, `record_*`, `begin_html`, `record_detail_body`, sitemap/robots writers), `css/style.css` (section 15), `js/site.js` (share buttons), `AI-HANDOFF.md`, `README.md`; every page regenerated.

**Link previews.** All absolute addresses come from `SITE_URL` at the top of `tools/build_site.py` (currently `https://killythirsk.github.io/Dzulfaraaghaini/`). If the site moves to a custom domain or Cloudflare Pages, change that one line and rebuild. Crawlers read `robots.txt` only at the root of a host, so on the current project address it is ignored; submit `sitemap.xml` in Google Search Console instead (it works as written on a custom domain). The art is portrait, so previews use the small "summary" card; landscape 1200x630 images would give larger previews on X and Facebook.

Totals: cases 16, characters 220, records 119; pages in sitemap 367.

### [MERGED] Update — Case 2365 (*The Decree of Luminescence*): 24-subject cast and 15 records

On branch `case-2365-stub`.

Added:
- `characters/` — 24 pages: piero, severin, marcello, livia, faustin, sigrid, arne, ragnvald, fulvio, rufio, nardo, costanza, aldo, lino, nina, tito, the-goldsmith, anselmo, the-granary-physician, the-tanners-widow, the-nameless-girl, the-senior-clerk-of-the-hall, the-interpreter, the-herald-2365
- `images/characters/` — 48 files: a sheet and a `-thumb` for each of those 24 slugs
- `images/scenes/` — 30 files: a full image and a `-grid` for each of 15 scenes
- `records/` — 15 pages, one per scene, generated from the script
- `images/covers/2365.jpg` (cover-only entry, committed earlier on the branch)

Edited:
- `tools/build_site.py` — Case 2365's `BOOKS` entry filled in (cast, scenes, `catalyst` *The Round-Bed*, `envoy` Observer 117 "the Reckoner"); `pages`, `genre` and `synopsis_html` left as the placeholders, so the case stays awaiting release; `PRINCIPALS` gained `2365`; one sentence each added to the Cultivator and Catalyst lore prose; the Decree of Luminescence `appears_html` now names the case
- `books/2365.html`, `books.html`, `index.html`, `characters.html`, `scenes.html`, `lore/cultivator.html`, `lore/catalyst.html`, `lore/decree-of-luminescence.html`, `sitemap.xml` — regenerated from the script
- `AI-HANDOFF.md` — Book write-up for 2365 in §6, §7 bullet, merge note in §8; counts updated
- `README.md` — this entry, the "Where things stand" paragraph and the records count
- every other page — footer "Site last built" stamp only

Totals: cases 16 -> 17, characters 220 -> 244, scenes 119 -> 134; pages in sitemap 367 -> 407. A recount from the rebuilt site gives the same figures, and every local link resolves.

Merged: 2026-10-09, 10:22AM GMT+7, via pull request #1 (`case-2365-stub`). The case was merged as coming-soon; it was published by the next entry below.

### [MERGED] Update — Case 2231 (*The Stone of the Clean Hand*): new 18-subject case, plus Case 2365 published

Straight into `main` at the author's request (no staging copy, so no `[PENDING]` entry existed). The author sent the cover, the manuscript (`Case_2231_The_Stone_of_the_Clean_Hand_2026-10-08_1630PM_GMT+7.md`) and 18 character-dossier sheets; then, for Case 2365, the Google Play Books link (`https://play.google.com/store/books/details?id=spIXEgAAQBAJ`) and a page count of 88.

Added:
- `books/2231.html` — Case 2231, coming-soon (no purchase link was supplied)
- `characters/` — 18 pages: observer-618, shizuka, jokei, sadamune, kanemichi, kurige, bureau-officers, bertran, gersenda, bernat, brunissen, villagers-of-vilarnau, masons-of-castelmaur, castelmaur-men-at-arms, folquet, odilo, guilhem, jaume
- `images/characters/` — 36 files: a sheet and a `-thumb` for each of those 18 slugs
- `images/covers/2231.jpg` (900x1350) and `images/covers/2231-stone-thumb.jpg` (the Catalyst's roster image, a crop of the cover)

Edited:
- `tools/build_site.py` — a full `2231` `BOOKS` entry (18 characters, `catalyst` *The Kiyote Pair*, `envoy` Observer 618 "the Dumb Mason"; `pages`, `genre` and `synopsis_html` left as the placeholders; no scenes); `PRINCIPALS` gained `2231`; one `RELATED_THEMES` row linking 2231 to 4099; one sentence each added to the Cultivator and Catalyst lore prose; the Threefold Crown `appears_html` now names the case. Case 2365: `status` set to published + google-books, `pages` "88", `google_books_url` set (its `genre` and `synopsis_html` are still placeholders)
- `books.html`, `index.html`, `characters.html`, `sitemap.xml`, `lore/cultivator.html`, `lore/catalyst.html`, `lore/threefold-crown.html`, `lore/decree-of-luminescence.html`, `books/2365.html`, `books/4099.html` (related-case line), and the character and record pages of Case 2365 — regenerated from the script
- `AI-HANDOFF.md` — Book write-up for 2231 in §6, the 2365 write-up and §7 bullets, §8 entry; counts updated
- `README.md` — this entry, the previous entry's status, and the "Where things stand" paragraph
- every other page — footer "Site last built" stamp only

Totals: cases 17 -> 18, characters 244 -> 262, records 134 unchanged; pages in sitemap 407 -> 426. A recount from the rebuilt site gives the same figures, and every local link resolves (15,393 checked).

### [PENDING] Update — Case 0247 (*The Tear of the Dragon*): new 17-subject case

On branch `case-0247`, opened as a pull request rather than pushed to `main`, because another session may be working on the repo (no staging copy, so no `[PENDING]` entry existed). The author sent the cover, the manuscript (`Case_0247_The_Tear_of_the_Dragon_2026-10-07_0411AM_GMT_7.md`, not committed), 17 reference sheets and then 11 record paintings.

Added:
- `books/0247.html` — Case 0247, coming-soon (no purchase link was supplied)
- `characters/` — 17 pages: the-hollow-hermit, the-dragons-tear, kuang-zhi, shen-lie, bai-rong, xuanwu-kai, chen-wu, fang, widow-bai, deputy-song, old-cao, xuanwu-kais-son, wei-bo, the-mourning-cord, chen-rui, old-fen, bo
- `images/characters/` — 34 files: a sheet and a `-thumb` for each of those 17 slugs
- `images/covers/0247.jpg` (900x1350)
- `records/` — 11 pages, one per record, generated from the script: not-the-first, three-shepherds-at-the-southern-bank, shen-lie-finds-the-body, bai-rong-at-the-gate, widow-bai-watches-his-hands, old-cao-counts-the-coins, the-fire-in-the-hollow, the-shepherds-reckoning, the-oath-is-invoked, back-up-the-mountain, the-second-emptying
- `images/scenes/` — 22 files: a full image and a `-grid` for each of those 11 records

Edited:
- `tools/build_site.py` — a full `0247` `BOOKS` entry (17 characters, 11 scenes, `catalyst` *The Dragon's Tear*, `envoy` The Hollow Hermit; `pages`, `genre` and `synopsis_html` left as the placeholders); `PRINCIPALS` gained `0247`; one `RELATED_THEMES` row linking 0247 to 4438 through the Xuanwu Sect's founder, Kang Yi; one sentence each added to the Cultivator and Catalyst lore prose
- `books.html`, `index.html`, `characters.html`, `sitemap.xml`, `lore/cultivator.html`, `lore/catalyst.html` — regenerated from the script, as were the related-case lines of `books/0000.html`, `books/0156.html`, `books/0188.html` and `books/4438.html`
- `AI-HANDOFF.md` — Book write-up for 0247 in §6, §7 bullet, §8 entry; counts updated
- `README.md` — this entry and the "Where things stand" paragraph
- every other page — footer "Site last built" stamp only

Totals: cases 18 -> 19, characters (subjects) 262 -> 279, records 134 -> 145; pages in sitemap 426 -> 455. A recount from the rebuilt site gives the same figures, and every local link resolves (16,582 checked).

### [PENDING] Update — Case 1153 (*The Second Hand*): new 19-subject case with 13 records, two gazetteers, and the 2365 / 4555 link

On branch `case-1153`, as a pull request rather than straight into `main`; `main` moved (Case 0247 was merged) while it was open, so it was merged forward and every generated page was rebuilt from the script. The author sent the cover, the manuscript (`Case_1153_The_Eleven-Fingered_Mercy_2026-10-07_1737PM_GMT_7.md`), 20 character-dossier sheets (19 used), 13 scene paintings, a re-send of the Case 2365 manuscript (the same revision 3 the repo already follows, so nothing changed there) and two gazetteer maps (Illumaria for Cases 2365 and 4555, and the Iron Stiletto War for Case 4417). The author also said Cases 2365 and 4555 are the same kingdom, 2365 the founding of its religion and 4555 many years after it.

Added:
- `books/1153.html` — Case 1153, coming-soon (no purchase link, page count, genre or synopsis yet; those stay placeholders)
- `characters/` — 19 pages: levan, bagrat, guram, vazha, demna, observer-419-1153, the-eleven-fingered-hand, the-doctrine-of-the-unbroken-hand, sandro, otar, eka, sulqan, dato, gia, beso, amets, xu-lian, anchorite-of-ardenwake, the-founding-wielder
- `records/` — 13 pages: the-proving-strap-gives, the-king-on-the-northern-wall, the-clockmaker-at-his-stall, the-graft-over-three-nights, levan-counts-his-fingers, demna-before-the-ruling, the-vashtir-snow, the-king-in-the-corridor, the-outer-wall-falls, the-eastern-breach, the-keeper-meets-the-stranger, levan-at-the-workbench-in-otsane, one-attempt-on-valeria
- `lore/illumaria.html`, `lore/iron-stiletto-war.html` — the two gazetteers
- `images/covers/1153.jpg`; `images/characters/` — 38 files (a sheet and a `-thumb` for each of the 19 slugs); `images/scenes/` — 26 files (a full image and a `-grid` for each of 13); `images/maps/` — `illumaria` and `iron-stiletto-war`, each with a `-thumb`

Edited:
- `tools/build_site.py` — a full `1153` `BOOKS` entry (catalyst *The Eleven-Fingered Hand*, envoy Observer 419); `PRINCIPALS` gained `1153`; four `RELATED_THEMES` rows (2365 with 4555, 1153 with 2140, with 0000B and with 0000); two new `LORE` entries with a `map` and a `places` list, a map layout for them (`gazetteer_body`), and a "Gazetteer" card on the case pages that share a map (`gazetteer_cards_html`); the Cultivator lore now allows one Envoy posted to two cases, the Catalyst lore names the eleven-fingered hand, and the Faith of Ardwen, Threefold Crown and Decree of Luminescence entries name the new case or map; the 0000B Anchorite bio, the 0000 Boy bio and the 2140 Observer 419 bio link across to the 1153 pages
- `css/style.css` — a "Gazetteers" section (`.gazetteer`, `.map-figure`, `.places`, `.gz-card`)
- `AI-HANDOFF.md` — Book write-up for 1153 and the gazetteer feature in §6, the "Same Observer" note in §3, site map in §4, open items in §7, §8 entry; counts updated
- `README.md` — this entry and the "Where things stand" paragraph
- `books.html`, `index.html`, `characters.html`, `sitemap.xml`, the lore pages and every case page that gained a link or card — regenerated from the script
- every other page — footer "Site last built" stamp only

Totals (counted against `main` after Case 0247 was merged): cases 19 -> 20, characters 279 -> 298, records 145 -> 158; pages in sitemap 455 -> 490. A recount from the rebuilt site gives the same figures, and every local link resolves (16,945 checked).

### [PENDING] Update — Case 2231 (*The Stone of the Clean Hand*): 25 more subjects and 14 records

On branch `case-2231-records-v2`, as a pull request rather than straight into `main`, because other sessions work on the repo: `main` moved twice while this was prepared (Cases 0247 and 1153 were merged, then the Case 2365 synopsis), so the branch was brought up to date before the final rebuild and the counts below were measured after that. The author sent 14 scene paintings and 25 character sheets (in two messages) and said the manuscript (`Case_2231_The_Stone_of_the_Clean_Hand_2026-10-08_1630PM_GMT_7.md`, revision 7) was context for the GitHub site, not something to edit; it is not committed (the repo is public). The bios and captions were written after reading it in full, and facts that appear only on a sheet are labelled as the sheet's.

Added:
- `characters/` — 25 pages, in roster order: the-kiyote-pair, tsuru, three-senior-priests, sukenori, deputy-minister-of-the-left, bureau-clerk, kaneyoshi, kiyomaro, azuki, kinji, rider-from-the-north, old-master-one-eye, new-left-minister, boy-sovereign-of-himuro, bertrans-sister, ermengarda, smiths-son, weighers-widow, gaucelm, sicard, arnaut, aimeric-2231, ors, count-raimon, basque-guard-of-rocafort. The Baron of Castelmaur is `aimeric-2231` (display name "Aimeric of Castelmaur") because `aimeric` is already Case 0000B's Duke of Vosmark
- `images/characters/` — 50 files (a sheet and a `-thumb` for each of those 25 slugs)
- `records/` — 14 pages, in story order: the-cat-at-the-starting-line, was-my-thumb-right, the-warmed-cushion, the-sparrow-examiner, the-night-before, dawn-at-mikusa, the-stranger-at-the-doorstone, the-weighing, solans-fire, the-barn, the-stone-holds-a-man, the-bridge-at-the-lower-race, the-quarry-gate, the-eleven-sheets
- `images/scenes/` — 28 files: a full image and a `-grid` for each of those 14 records

Edited:
- `tools/build_site.py` — the `2231` dict: 25 new `characters` entries placed in story order among the existing 18, 14 `scenes` (it had none), and the Catalyst roster row's `page` repointed from `books/2231.html` to the new `characters/the-kiyote-pair.html` (its `img` is unchanged); `PRINCIPALS`, `RELATED_THEMES` and `HOME_SCENES` untouched
- `books/2231.html`, `characters.html`, `scenes.html`, `index.html`, `sitemap.xml`, `lore/catalyst.html` and the 15 existing 2231 character pages that gained related subjects or records — regenerated from the script
- `AI-HANDOFF.md` — Book write-up for 2231 in §6, §7 bullet, §8 entry; counts updated
- `README.md` — this entry, the "Where things stand" paragraph and the `records/` count
- every other page — footer "Site last built" stamp and cache-bust query only, deliberately not committed

Totals (counted after the branch was brought up to date with `main`): cases 20 -> 20, characters 298 -> 323, records 158 -> 172; pages in sitemap 490 -> 529. A recount from the rebuilt site gives the same figures, and every local link resolves (18,419 checked).

### [PENDING] Update — Case 1268 (*Independent Observation*): new 11-subject case, plus Case 1153 published

On branch `case-1268`, as a pull request rather than straight into `main`, because other sessions work on the repo (`origin/main` was at `ca8c808`, the merge of PR #6, when the work started). The author sent the cover (titled *Independent Observation*), the manuscript (`Case_1268_The_Eleventh_Astral_Dream_2026-10-01_0518AM_GMT_7.md`, revision 1; its own title is *The Eleventh Astral Dream*), and 11 character sheets, and said Case 1153 is live on Google Books (`https://play.google.com/store/books/details?id=3IYZEgAAQBAJ`). No scene paintings came, so Case 1268 has no records yet. The manuscript is not committed (the repo is public); the bios were written after reading it in full and every number and quoted phrase in them was checked against it by script, with facts that appear only on a sheet labelled as the sheet's.

Added:
- `books/1268.html` — Case 1268, coming-soon (no purchase link, page count, genre, synopsis or records yet; those stay placeholders)
- `characters/` — 11 pages, in roster order: hraban, anchorite-of-ardwen, otker, adaltrude, ansovald, sigward, ymma, the-probe-network, cultivator-observer, solan, elara
- `images/covers/1268.jpg`; `images/characters/` — 22 files (a sheet and a `-thumb` for each of those 11 slugs)

Edited:
- `tools/build_site.py` — Case 1153 `status` is now `["published", "google-books"]` with its `google_books_url`; a full `1268` `BOOKS` entry (catalyst *The Probe Network*, envoy Cultivator Observer, no scenes; `pages`, `genre` and `synopsis_html` left as the placeholders); `PRINCIPALS` gained `1268`; one `RELATED_THEMES` row relating 1268 to 0000; one sentence each added to the Cultivator, Catalyst, Threefold Crown and Faith of Ardwen lore (the Cultivator lore now says "Nearly every case has its own" Envoy, since 1268 has none posted in person)
- `books/1153.html`, its 19 character pages and 13 record pages — regenerated (the case is no longer muted and the record pages gain a Google Books link); `books/0000.html`, `0000b`, `0156`, `0157`, `2140`, `2231` and `4417` (related-case blocks); `books.html`, `index.html`, `characters.html`, `sitemap.xml`, `lore/cultivator.html`, `lore/catalyst.html`, `lore/faith-of-ardwen.html`, `lore/threefold-crown.html` — regenerated from the script
- `AI-HANDOFF.md` — Book write-up for 1268 in §6 (with the judgment calls), 1153 marked published, counts, §7 bullets, §8 entry
- `README.md` — this entry and the "Where things stand" paragraph
- every other page — footer "Site last built" stamp and cache-bust query only, deliberately not committed

Totals: cases 20 -> 21, characters (subjects) 323 -> 334, records 172 (unchanged); pages in sitemap 529 -> 541. A recount from the rebuilt site gives the same figures, and every local link resolves (18,881 checked).

### [PENDING] Update — Case 1268 records (15), Case 4420 gazetteer, gazetteer sharing and square link previews

On branch `case-1268-records-4420-gazetteer`, as a pull request. The author sent 15 scene paintings for Case 1268 and one map for Case 4420, and asked for the 1268 records, the 4420 gazetteer, the gazetteers to be shareable like subjects, and book and gazetteer links to show a thumbnail on other platforms the way subject links do. The 4420 map's printed banner still reads the old title, *The Thermal Vessel War*; the site names the gazetteer *The Vessel of the Betrayed Host* and the image was filed as sent (see `AI-HANDOFF.md` §6).

Added:
- `records/` — 15 pages for Case 1268 (`ymma-wakes-before-dawn` ... `hraban-finds-the-anchorite`); `images/scenes/` — 30 files, a full image and a `-grid` for each
- `lore/vessel-of-the-betrayed-host.html` — the Case 4420 gazetteer; `images/maps/vessel-of-the-betrayed-host.jpg` and its `-thumb`
- `images/share/` — 24 square (1200x1200) link-preview images, one per cover and per map, made by the new `tools/make_share_images.py`

Edited:
- `tools/build_site.py` — 15 `scenes` on the `1268` dict; the new `LORE` entry; a Share button on gazetteer pages; `share_image()` so case and gazetteer pages preview with the square image (falling back to the original art); an optional scene `"title"` (the record's own page then prints the full caption as a paragraph)
- the 21 case pages and the three gazetteer pages (new preview image), the 1268 subject pages (related records), `books/4420.html` (Gazetteer card), `index.html`, `lore.html`, `scenes.html`, `sitemap.xml` — regenerated from the script
- `AI-HANDOFF.md` and `README.md` — this entry, the 1268 records and 4420 gazetteer write-ups, the link-preview note in §3
- every other page — footer "Site last built" stamp and cache-bust query only, deliberately not committed

Totals: cases 21 (unchanged), characters (subjects) 334 (unchanged), records 172 -> 187; pages in sitemap 541 -> 557. Every local link resolves. Link previews were checked in the generated HTML only; a link shared before this change keeps its cached preview until the platform re-fetches it.

### [PENDING] Update — Case 0202 (*Fossa*): new 27-subject case with 10 records

On branch `case-0202-fossa`, as a pull request rather than straight into `main`, because other sessions work on the repo: `main` moved twice while this was prepared (Case 1268, then the Case 1268 records and the Case 4420 gazetteer), so the branch was rebased onto it before the final rebuild and the counts below were measured after that. The author asked for "Case 0202 : Fossa", a publication for the characters, said some of them also appear in Case 2231, and sent the cover, the manuscript (`Case_0202_The_Sun-Turned_Harvest_2026-10-08_1035AM_GMT_7.md`, revision 4; its own title is *The Sun-Turned Harvest*), a publication package, 27 character sheets (17 in a "first batch", then 10 more) and 10 scene paintings. The manuscript and package are not committed (the repo is public). The bios and captions were written after reading the manuscript in full and every number and quoted phrase was checked against it by script; facts that appear only on a sheet are labelled as the sheet's. More characters are expected.

Added:
- `books/0202.html` — Case 0202, coming-soon (no purchase link; `pages`, `genre` and `synopsis_html` stay placeholders)
- `characters/` — 27 pages, in roster order: observer-551, strain-h-202, the-accord-of-montclar, king-ramon-iii, pons, ibrahim-ibn-nasr, ottavio-brandi, matteo, alazais, joan, paciencia, bertran-0202, baron-of-saint-aventin, the-provosts-daughter, the-provosts-sister, smith-of-vilarnau, smiths-wife, arnal, bernat-the-younger, bernat-the-youngers-wife, sergeant-of-the-levy, corporal-of-the-order, goose, elis-mother, vara, genzo, yo-su. `bertran-0202` is a separate page for the man Case 2231 calls `bertran`, because the two manuscripts give him different ages (41 and 38); the pages cross-link
- `images/covers/0202.jpg` and its square link preview `images/share/cover-0202.jpg`; `images/characters/` — 54 files (a sheet and a `-thumb` for each of those 27 slugs)
- `records/` — 10 pages, in manuscript order: the-news-from-the-south, the-stone-at-mikusa, the-bowl-on-the-green, the-lesson-at-the-mill, what-the-tavern-knew, the-fire-in-the-ditch, the-dawn-wall, the-long-graves, the-cairn-on-the-ridge, the-hermit-of-val-muta
- `images/scenes/` — 20 files: a full image and a `-grid` for each of those 10 records

Edited:
- `tools/build_site.py` — a full `0202` `BOOKS` entry (catalyst *Strain H-202*, envoy *Observer 551*, 10 `scenes` each with a short `"title"`); `PRINCIPALS` gained `0202`; one `RELATED_THEMES` row relating 0202 to 2231; one sentence each added to the Cultivator, Catalyst, Faith of Ardwen, Threefold Crown and Decree of Luminescence lore; five reciprocal sentences on the 2231 pages `bertran`, `observer-618`, `villagers-of-vilarnau`, `the-kiyote-pair` and `kaneyoshi`
- `books.html`, `index.html`, `characters.html`, `scenes.html`, `sitemap.xml`, `lore/catalyst.html`, `lore/cultivator.html`, `lore/decree-of-luminescence.html`, `lore/faith-of-ardwen.html`, `lore/threefold-crown.html`, `characters/bertran.html`, `characters/kaneyoshi.html`, `characters/observer-618.html`, `characters/the-kiyote-pair.html`, `characters/villagers-of-vilarnau.html`, and the related-case blocks of `books/0157.html`, `1153`, `1268`, `2140`, `2231`, `2365` and `4555` — regenerated from the script
- `AI-HANDOFF.md` — Book write-up for 0202 in §6 (with the judgment calls), counts, §7 bullet, §8 entry
- `README.md` — this entry, the "Where things stand" paragraph and the `records/` count
- every other page — footer "Site last built" stamp and cache-bust query only, deliberately not committed

Totals (counted after the rebase onto `main`): cases 21 -> 22, characters (subjects) 334 -> 361, records 187 -> 197; pages in sitemap 557 -> 595. A recount from the rebuilt site gives the same figures, and every local link resolves (20,865 checked).

### [PENDING] Update — Case 3001 (*The Uncounted Dinar*): new 13-subject case

On branch `case-3001`, as a pull request rather than straight into `main`, because other sessions work on the repo. The author sent the cover (`30010_5x.jpg`, 1717x2576), the manuscript (`Case_3001_The_Uncounted_Dinar_2026-10-14_1712PM_GMT_7.md`, revision 6) and 13 character sheets, with "read repo, add 3001". The manuscript was read for the bios only and is **not committed** (the repo is public).

Added:
- `books/3001.html` — Case 3001, coming-soon (no purchase link, page count, genre, synopsis or records; those stay placeholders)
- `characters/` — 13 pages, in roster order: malik-ibn-sabir, amina-bint-rashid, sulayman-ibn-ghanim, nur, qasim-al-fahmi, the-dinar, observer-1140, hammad, maliks-cousin, the-smith-of-the-dunes, the-sentry-of-banu-kathir, the-witnessed-akad, the-provincial-archive-clerk
- `images/covers/3001.jpg`; `images/characters/` — 26 files (a sheet and a `-thumb` for each of those 13 slugs); `images/share/cover-3001.jpg` (square link preview, made by `tools/make_share_images.py`)

Edited:
- `tools/build_site.py` — a full `3001` `BOOKS` entry (catalyst *The Dinar*, envoy Observer 1140, no scenes; `pages`, `genre` and `synopsis_html` left as the placeholders) a `PRINCIPALS` entry and one `RELATED_THEMES` row (3001 with 0202: the trader Ibrahim ibn Nasr appears in both)
- `books.html`, `books/3115.html` (a Related Cases card: both cases are "High-Concept, Cultural and Social"), `characters.html`, `index.html` (counts and cast wall), `lore/catalyst.html`, `lore/cultivator.html`, `sitemap.xml` — regenerated from the script
- `AI-HANDOFF.md` — Book write-up for 3001 in §6 (with the judgment calls), counts, §7 bullet, §8 entry
- `README.md` — this entry and the "Where things stand" paragraph
- every other page — footer "Site last built" stamp and cache-bust query only, deliberately not committed

Totals (counted after the rebase onto `main`, which now holds Case 0202): cases 22 -> 23, characters (subjects) 361 -> 374, records 197 (unchanged); pages in sitemap 595 -> 609. Every local link resolves (21,391 checked), and the new and changed pages were opened in Chromium at desktop and phone width with no broken images. **Open questions for the author** are listed in the Case 3001 write-up in `AI-HANDOFF.md` §6; the first is that the cover's tagline reads "RICE." where the manuscript's word is probably "Price". Also flagged there: Ibrahim ibn Nasr's age is 38 on Case 0202's sheet but about 55 by the 3001 manuscript, and `books/0202.html` does not list 3001 as a related case because of the existing six-card cap.
