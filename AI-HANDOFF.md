# AI Handoff — Dzulfaraaghaini author site

This file exists so a different AI assistant (or a fresh session of any AI)
can pick this project up with full context. It was written by Claude
(Anthropic) across a long build session and updated as the project grew.
If you're an AI reading this: everything below is real project history,
not a hypothetical — please don't contradict it without the author telling
you to.

If you're the author: this is the technical/narrative memory for whoever
helps you next. `README.md` (same folder) is the short human-facing guide;
this one is longer and more exhaustive on purpose.

## 1. What this is

A static personal website for **Dzulfaraaghaini**, a pen name for an indie
writer of speculative fiction (more than a dozen novels exist across
various stages of publication; nine are live on the site so far (Case 1153 went live on Google Books on 2026-10-14), plus
eleven coming-soon books with a character roster (0156, 0188, 2140, 3115, 0000B, 2231, 0247, 1268, 0202, 3001, 4181) and four
cover-only coming-soon entries (3312, 3887, 4442, 2114) — see
§7). The site is a portfolio + a lore glossary for the setting(s) the
books share.

**Hard constraints, stated by the author at the start and still in force:**
- Pure static HTML/CSS + a small amount of vanilla JS. No CMS, no database,
  no backend, no React/Vue/etc., no build step required to *serve* the
  site.
- No payment processing; external retailers and reading platforms (Google
  Books, Amazon Kindle, Royal Road) are linked out to.
- Hosted on GitHub Pages now (repo must be named `<username>.github.io`),
  with an explicit requirement that a future move to Cloudflare Pages needs
  **zero structural changes** — just repoint the host.
- Should not feel like an online store. Purchase links are deliberately
  the last thing on a book's page, not the first thing a visitor sees.
- Simple enough for a non-developer to maintain by hand if needed.

## 2. How content actually gets built — read this before editing anything

**The HTML files in this repo are generated, not hand-written.**
`tools/build_site.py` is a plain Python script with no third-party
dependencies. It contains all page content as Python data (titles, bios,
captions, cross-links) and a set of small template functions, and it
writes out every `.html` file in the project when run.

```
cd tools
python3 build_site.py
```

Run from anywhere — the script locates the project root relative to its
own file location (two directories up from wherever this copy of the file
actually sits), so **always run the copy at `tools/build_site.py`, from
inside that `tools/` folder.** Running a copy of the script from somewhere
else will compute the wrong project root and write files to the wrong
place — this happened once already during development; see §8.

**Rule: don't hand-edit the generated `.html` files.** Any direct edit to
`index.html`, `books/0000.html`, `characters/*.html`, etc. will be silently
overwritten the next time someone runs the script. Edit the data or
template functions inside `build_site.py` instead, then regenerate.

(If whoever's reading this has no code execution available at all, hand-
editing the static files directly is still *possible* — they're just HTML
— but `build_site.py` will drift out of sync with the live site when you
do that. Try to reconcile the two eventually, or note clearly that the
generator is now stale.)

**Data model, as of this writing:** a single `BOOKS` list, one dict per
book. Each book dict carries its own metadata (`title`, `status`, `cover_file`,
`case_tag`, `pages`, `genre`, `synopsis_html`) *and* two lists nested
directly inside it: `"characters"` and `"scenes"`. The "Read This Book"
panel is driven entirely by `status`: each read/purchase platform is a tag
in that list (`"google-books"`, `"kindle"`, `"royal-road"` so far) paired
with its own `"<platform>_url"` field (`google_books_url`, `kindle_url`,
`royal_road_url`); `book_detail_body()` checks each tag and appends a
button only if it's present, so a book can carry any combination — Book 1
currently has both `google-books` and `royal-road` at once, Books 2, 3
and 4 each have just `google-books`. Adding a fourth platform later
means one more `if
"<tag>" in b["status"]:` line there, one more entry in `TAG_LABELS`, and
the matching `"<tag>_url"` field on whichever book dict uses it. Characters and scenes belong to one specific book, not to the
site globally — the Sword of Valeria, Ledger, Stolen Prince War and
Iron Stiletto War casts are four completely separate lists and don't mix. A separate `LORE` list holds the
glossary, which *is* sitewide (not book-scoped), since it's meant to
describe things that can recur across books. Adding a new book means
adding a new dict to `BOOKS` with its own `"characters": [...]` and
`"scenes": [...]`; adding a character or scene to an existing book means
appending to that book's own nested list. The `write()` loop at the bottom
of the script iterates over `BOOKS` and, for each one, over its nested
characters — that's what actually produces every `books/<slug>.html` and
`characters/<slug>.html` file, so nothing needs to be added to the loop
itself when the lists grow.

**Character slugs share one namespace across all books.** Each becomes
`characters/<slug>.html`, and the generator silently overwrites a page if
two books use the same slug (there are no duplicates now; §10 has a check).
Other cases in the author's canon reuse names already taken here — a Lady
Aurelia in Case 4425 and a King Osric in Case 3887, against this site's
`aurelia` and `osric`, which belong to the Iron Stiletto War — so give a
newcomer a disambiguated slug like `aurelia-4425`, the same way
`observer-0157` and `observer-4099` are kept apart.

Images are **not** generated by the script — they're pre-processed JPEGs
already sitting in `images/covers/`, `images/characters/`, and
`images/scenes/` (resized and compressed from whatever the author
uploaded; originals were not kept). The script only references them by
filename.

## 3. Design system

**Update (Oct 2026): the site was re-themed to the author's "archive" mockup** (dark ink header/hero/footer, parchment page, gold accent; Playfair Display + Lora + Source Code Pro). The "cool grey, not warm parchment" bullets below describe the *previous* theme and are superseded: current tokens are in `:root` plus the "12. Archive theme" block at the end of `css/style.css`. Covers get a shadow and hairline outline so they still stand off the warmer ground. The hero image `images/backgrounds/hero.jpg` is a crop from the author's mockup (placeholder; swap in a proper image under the same name). Also added from the mockup: top-level `characters.html` and `scenes.html` (search + per-case filter chips, driven by `BOOKS`), a Featured Case block on the home page (Case 4555), and a mobile hamburger menu. Not built: a category-tabbed Lore page, a global cross-site search, a mobile bottom tab bar.

**Update (Oct 2026, case-archive pass).** The site now speaks in archive terms. Nav and headings: Books -> **Cases**, Characters -> **Subjects**, Scenes -> **Records**, Lore -> **Archive**, "Coming Soon" -> **Awaiting Release**. File names and URLs were deliberately NOT changed (`books.html`, `characters.html`, ...), so every shared link still works. What was added, all in `tools/build_site.py` + CSS section 14 + `js/site.js`:
- **Cases page / home:** *Published Cases* (grid, count) and *Cases Awaiting Release* (separate dark band, desaturated covers) via `published_section_html()` / `awaiting_band_html()`. Home shows the published grid plus a link to `books.html#awaiting`.
- **Case page:** dominant `READ ON GOOGLE BOOKS` button under the title and again after the Records (`cta_html()`; falls back to Kindle / Royal Road if there is no Google Books link; awaiting cases get no READ button). Subjects are split into **Principal Subjects** and a folded `<details>` "N additional subjects documented" (`subjects_section_html()`), with a link to `characters.html?case=<slug>` (the index reads `?case=`). Principals are set per case in the **`PRINCIPALS`** dict at the top of the script (author-confirmed only for 4099; the rest are a first pass, edit freely). Cases with 7 or fewer subjects (`SPLIT_MIN`) show everyone as principal; a case with no `PRINCIPALS` entry falls back to its first six.
- **Related Cases / Subjects / Records** are generated from existing data, nothing invented: cases relate by *same catalyst class* (each book's `catalyst.meta`) and *shared faith* (the Religion lore pages' `appears_html` links); subjects relate by character cross-links inside bios (both directions), falling back to the case's principals; records are the scenes whose caption links to that subject; lore pages list the cases where the concept appears. Hand-written thematic links go in **`RELATED_THEMES`** as `(case slug, case slug, "reason")`. "Same Observer" is not a generated relation: each case has its own Observer, with **one exception on file, Observer 419**, who is the Envoy of both 2140 and 1153 (Case 1268 has no Envoy posted in person; its `envoy` roster record is the Custodian-Office analyst, §6) (a hand-written `RELATED_THEMES` row links the two; the Cultivator lore says so; see §6).
- **Mobile "see more":** markup opts in with `data-cap="N"` (show N list items, button reveals the rest) or `data-collapse="N"` (clip a block to N rem). `js/site.js` adds the buttons on phones (<= 40rem) only; desktop is untouched, and the Subjects/Records indexes lift the cap while a search or case filter is active.
- **Fix:** the hero "Enter the archive" button sat off-centre because the global `p { max-width: 68ch }` left its paragraph left-aligned; `.hero--home p { margin-inline: auto }` fixes it.

**Update (Oct 2026, discoverability pass).** All in `tools/build_site.py` + CSS section 15 + `js/site.js`:
- **Absolute URLs come from one constant, `SITE_URL`** (top of the script; today `https://killythirsk.github.io/Dzulfaraaghaini/`, a GitHub Pages *project* address, which is why the repo is not named `<username>.github.io`). Canonical links, Open Graph/Twitter tags, share-button URLs and `sitemap.xml` all derive from it. Relative links everywhere else are unchanged. Change it when the host changes.
- **`page()` takes `path=` (the page's own file name), `image=`, `image_alt=`, `og_type=`.** Passing `path` is what switches on the canonical link, OG/Twitter tags and the sitemap entry, so any new page type must pass it. `image` falls back to `DEFAULT_OG_IMAGE`. Twitter card is `summary_large_image` only for images at least 1.5x wider than tall (none today; all the art is portrait).
- **Records have their own pages**, `records/<scene-slug>.html` (`record_detail_body()`), because a scene had no URL of its own to share or preview. Scene slugs share one namespace across books (checked: no duplicates); keep it that way. The old lightbox links are untouched.
- **Record line (Subject / Archive)** is `record_meta_html()`. Subjects = characters linked from the caption, or an optional `"subjects": [character slugs]` on the scene dict, which wins when present. Nothing is guessed; records with neither show Archive only.
- **Share buttons** (`share_btn()`) carry `data-share-url/-title/-text` and are `hidden` until `js/site.js` shows them. New page types that should be shareable need one.
- **Where to begin** (`begin_html()`, home `#begin`, deliberately the last section of the home page; the hero's second button jumps to it) lists published cases by `hook`, case tag and genre (editor-note spans stripped). It is generated, so a newly published case appears automatically. The author's rule behind it: no required starting point, each case stands alone, all are connected. **A published case's `hook` should be a one-sentence promise in the shape of the others** ("A pair of chrome heels, and the war two crowns paid for them."), not the cover's five-word tagline; a tagline kept as a placeholder hook on a coming-soon case should be rewritten when the case is published (2365 and 1153 were, 2026-10-16, using only details from their own synopsis and roster text). The `hook` also feeds the case cards, share text and meta descriptions.
- **`robots.txt` is ignored on the project address** (crawlers read it only at the host root); `sitemap.xml` has to be submitted in Search Console. Image protection is unchanged, but note that `og:image` necessarily names the image file for previews to work.

**Update (Oct 2026, link previews, gazetteer sharing, record titles).** Three small things, all in `tools/build_site.py`:
- **Gazetteer pages have a Share button** under the title (`gazetteer_body`), the same `share_btn()` the subject and record pages use.
- **Case and gazetteer links now preview with a square image.** Those pages already carried Open Graph / Twitter tags, but pointing at the tall 2:3 cover or map; platforms that show one small square thumbnail (X's `summary` card, WhatsApp, Telegram, Facebook, iMessage) cut a slice from the middle of a tall image, losing the title, while subject sheets are nearly square (980x1045) and show whole. `images/share/cover-<name>.jpg` and `images/share/map-<name>.jpg` (1200x1200: the whole cover or map on the `--night` ground, each under 280 KB) are made from `images/covers/` and `images/maps/` by **`tools/make_share_images.py`** (needs Pillow; `build_site.py` itself still needs nothing). `share_image()` picks the share file and falls back to the original art if it has not been made, so a missing file never breaks a page. **After adding or replacing a cover or map, run `python3 tools/make_share_images.py`, then `build_site.py`.** Subject and record previews were left alone. Platforms cache a link's preview by page URL, so a link shared before this change keeps its old preview until the platform is made to re-fetch it (Facebook's Sharing Debugger "Scrape Again", etc.); that is the platform's cache, not a site fault. This could not be tested on the live platforms from the build environment (outbound access to the site is blocked there); the tags were checked in the generated HTML only.
- **A scene may carry an optional `"title"`.** `record_title()` uses it for the record's heading, page title and share title, and the record's own page then prints the full caption as a paragraph (`record-caption`). Without `"title"` nothing changes: the caption is still its own heading. The 15 Case 1268 records use it because their captions run to two or three sentences.

**Update (2026-10-17, home counts, featured case, connected cases, metadata).** All in `tools/build_site.py` + `css/style.css`:
- **The home hero's stats row (24 Cases / 428 Subjects / 212 Records) is now three links**, to `books.html`, `characters.html` and `scenes.html` (the Cases, Subjects and Records indexes). Built in `index_body()`; styled by `.ledger-stats a` in the Archive theme block of `css/style.css`. The numbers are still counted from `BOOKS`.
- **The Featured Case block has two buttons, in this order: Open case, then Read on Google Books** (`featured_html()`, using `read_buttons()`, so it follows the case's primary read link and opens in a new tab). Layout is `.featured-actions` (a wrapping flex row; full-width stacked on phones).
- **`CONNECTED_CASES`** (a dict just above `BOOKS`) makes a published case's "Stands alone" note add "It is connected to Case NNNN (Title)." It is set both ways for **4555 and 2365**, at the author's request; add a pair in both directions to connect others. This is separate from `RELATED_THEMES`, which only feeds the "Related Cases" panel.
- **Metadata given by the author:** Case 4420 is 130 pages, genre *Fiction / Fantasy / Epic* (replacing the staging copy's `~123` estimate and suggested genre); Case 2365 genre is *Fiction / Fantasy / Historical*; Case 1153 is 77 pages, genre *Fiction / Fantasy / Epic*, with a synopsis written from manuscript revision 4 (the author pasted it). These three genres use the plain Google Books category form with slashes, unlike the older cases' dotted lists. The 1153 synopsis names the cover title, *The Second Hand*, not the manuscript title.

Everything visual is CSS custom properties at the top of `css/style.css`
(`:root { ... }`) — change a value there, it updates everywhere.

- **Palette is deliberately cool grey, not warm parchment.** This was a
  direct fix: the author's illustrated cover/character art is
  warm-toned/aged-paper-colored, and an early warm-parchment page
  background made covers blend into the page instead of standing out. All four
  covers on the site now (and all 86 character portraits) are warm/sepia
  watercolor-style art, so this contrast is doing real work — don't revert
  it without checking current art first.
  - `--paper: #e3e6e7` / `--paper-deep: #d3d7d8` (backgrounds)
  - `--ink: #202225` / `--ink-soft: #5b6266` (text)
  - `--accent: #33436e` / `--accent-deep: #202c49` (links, the one accent
    color used sitewide — deliberately just one)
  - `--rule: #b7bcbe` (hairline borders)
- **Type:** Fraunces (Google Fonts, headings/display only — one family,
  loaded once) + a system-serif stack for body text (`Charter`, `Georgia`,
  etc. — zero network cost).
- **Visual language:** "archive/ledger," not "SaaS card kit." Listings
  (`.catalog-list` / `.entry`) are bibliography-style rows with hairline
  dividers, not boxed cards with drop shadows. Sharp corners throughout
  (no `border-radius` anywhere) — a deliberate "cut paper / index card"
  choice.
- **Character portraits are never forced into a fixed crop.** Early on,
  `.character-portrait` had a hardcoded `aspect-ratio`, copied from the
  Sword of Valeria art's own proportions. When the Ledger cast arrived with
  noticeably different natural ratios per image (some much squarer, one
  much taller), that hardcoded ratio would have cropped several of them.
  It was removed — portraits now size naturally (`width` fixed, `height:
  auto`), same as the Scenes gallery already did. Don't reintroduce a
  forced ratio there.
- **Motion is slight, on purpose, requested explicitly by the author.**
  Hover states, a staggered hero entrance on page load, scroll-reveal on
  catalog rows, and lightbox open/close/navigate all animate gently
  (≤ 0.6s, small distances, no bounce/spring). **Everything must degrade
  to zero motion under `prefers-reduced-motion: reduce`** — already wired
  up and should stay that way for anything new.
- No image ever gets forced into a cropped aspect ratio unless it's a
  small fixed-size thumbnail in a list row (covers, character-list
  thumbnails). Larger displays keep each image's natural proportions.

## 4. Site map

Nav (same on every page): **Home / Books / Characters / Scenes / Lore / About / Contact.**
Notably *not* in the nav: Characters, Scenes — both live inside each
book's own page rather than as their own top-level sections.

```
/index.html            Homepage — hero (with a counts line), every book, a cast wall, a scene band, a lore teaser
/books.html             Full book list (currently twenty-three entries: nine published, fourteen coming-soon — see §6)
/books/0000.html          The Sword of Valeria's full page
/books/4099.html          The Ledger of a Single Sweetness's full page
/books/0157.html          The Stolen Prince War's full page
/books/4417.html          The Iron Stiletto War's full page
/lore.html               Glossary index (plain list on top, then a "Religion"
                            heading over the three faiths, then a "Gazetteers" heading over the three map pages — `group` field, §8)
/lore/<slug>.html          One page per term (cultivator, catalyst, faith-of-ardwen,
                            threefold-crown, decree-of-luminescence, and the two
                            gazetteers illumaria, iron-stiletto-war and vessel-of-the-betrayed-host;
                            lore/catalyst-tier.html is only a redirect stub to
                            catalyst.html)
/characters/<slug>.html    One page per character (428 total — 10 for
                            Valeria, 28 for the Ledger, 35 for the Stolen
                            Prince War, 13 for the Iron Stiletto War, 7 for
                            the Vessel of the Betrayed Host, 12 for the
                            Vessel of Unmediated Grace, 12 for the Songs
                            Never Mention the Cats, 15 for the Third Grain,
                            24 for the Listening Water, 19 for the Heavenly
                            Thunder-Serpent, 26 for the Purging of
                            Charsianon, 19 for the Empty Hand, 24 for the Decree of Luminescence, 43 for the Stone of the Clean Hand, 17 for the Tear of the Dragon, 19 for the Second Hand, 11 for Independent Observation, 27 for Fossa, 13 for the Uncounted Dinar, 54 for the Sable Skin; see §6)
/about.html               Biography only
/contact.html              Royal Road / Instagram / Threads (real; no email, by the author's choice)
```

### 4a. Anatomy of a book detail page
In order: back-link → cover + title + status tags → Book Info (pages,
genre, synopsis) → **Characters** (a `catalog-list` of every character in
*that* book, links to their own page) → **Scenes** (a *horizontal slider*
if the book has any scene art, or a plain "not yet added" note if it
doesn't — see §7 for which is which right now) → a **Gazetteer** card, only on a
case that shares a map (2365, 4555, 4417, 4420; see §6) → a boxed "Read This Book"
purchase panel.

The Characters vs. Scenes layout difference (vertical list vs. horizontal
slider) was a deliberate, discussed decision — see §8.

## 5. Interactive features (all in `js/site.js`, one small vanilla file)

**Lightbox.** Any image wrapped in `<a class="lightbox-link" href="full-
size.jpg">` opens full-size in a fading/scaling overlay on click. If the
link also has `data-group="covers"` / `"characters"` / `"scenes"`, the
overlay gains Next/Prev navigation (buttons, arrow keys, swipe on touch)
that cycles through every other `lightbox-link` sharing that group *on the
current page* — it wraps around at each end, and shows "3 of 10 —
description." Groups naturally stay scoped correctly per book without any
extra work: a book's characters only ever appear in the DOM on that book's
own page, so `data-group="characters"` on the Ledger's page can only ever
cycle through the Ledger's 28, never Valeria's 10, the Stolen Prince
War's 35, or the Iron Stiletto War's 13. The one group that
*does* span across books is `"covers"` on `books.html`/`index.html`,
where clicking any book's cover lets you page between all of them.

**Image protection (deterrent only).** Every lightbox link is
`<a class="lightbox-link" href="#" data-full="…">`: the full-size path lives in
`data-full`, not `href`, so middle-click / "open in new tab" / "save link as"
no longer land on the file. `site.js` also blocks the context menu and
dragging on images, CSS turns off `user-drag`, `user-select` and iOS
`touch-callout` on `img`, the lightbox image has `pointer-events: none`, and
every page carries `<meta name="robots" content="noimageindex">`. None of this
is a real lock — a browser must receive an image to show it, so dev tools,
screenshots and the network tab still work; don't promise the author more.
New lightbox links must use `href="#" data-full="…"`, never a bare `href`.

**Scene slider.** `.scene-gallery` is a natively horizontally-scrollable
`<ul>` (`overflow-x: auto`, scroll-snap). The `‹ ›` buttons next to the
"Scenes" heading call `scrollBy()` by one item-width and disable
themselves at each end. Only rendered at all if the book's `"scenes"` list
is non-empty; otherwise the section just shows a plain placeholder
paragraph and none of the slider markup/JS targets exist on that page.

**Scroll reveal.** `.catalog-list .entry` rows fade/rise into view via
`IntersectionObserver` — entirely skipped (not just visually disabled) for
`prefers-reduced-motion`.

## 6. The story so far — established canon, don't contradict

**Author:** Dzulfaraaghaini (he/him). Real biography, used verbatim on
`/about.html`:

> Dzulfaraaghaini is a writer of speculative fiction concerned with the
> fragility of human systems. His novels explore the rise and collapse of
> kingdoms, the evolution of faiths, and the unintended consequences of
> ordinary objects placed in extraordinary circumstances. Rather than
> focusing on heroes and villains, his work examines the institutions,
> beliefs, and social structures that govern entire societies — and the
> small moments of pride, fear, vanity, or misunderstanding that can bring
> those structures down. He is particularly interested in the relationship
> between history and memory: the gap between events as they occurred, and
> the stories later generations tell about them.

### The Cultivator mechanic (the thread connecting every book)

All five books share a confirmed, explicit meta-narrative device: a loose
organization called **the Cultivators** (originally just "observers")
selects a subject in some world, delivers a **Catalyst** — an item or
event with real power — directly into that subject's hands (or, in Case
0157, into a hillside for someone to find), then quietly files a numbered
**Case** report on what happens next. Field agents work disguised, through
numbered "deployment archetypes." Cases are classified by **numbered range
and by a named Class** — confirmed directly in the Ledger manuscript: Case
4099 falls under "**Mundane Class**" (4000–4999); Case 4417, the Iron
Stiletto War, sits in the same numbered range, a second data point for it.
The Stolen Prince War manuscript confirms a second Class directly: Case
0157 is filed as "**Mythic Class**," without a numbered range given on the
page. What separates the two Classes, what else exists between or beyond
them, and where Case 0000 (an actual sentient sword) falls by comparison,
is *not* established on the site — don't invent it. The lore page is now
**Catalyst** (renamed from Catalyst Tier at the author's request): it describes
what a Catalyst *is*, not the tier system, and each catalyst row just shows its
class (Mundane / Mythic) in its meta line.

**Lore rosters.** Every book dict carries a `"catalyst"` and an `"envoy"`
record (`name`, `meta`, `page`, `img`, `html`). `lore/cultivator.html` lists one
Envoy row per book and `lore/catalyst.html` one Catalyst row per book,
automatically. The author's rule: **every Envoy goes on lore/cultivator and
every Catalyst on lore/catalyst** — a new book's dict must include both records
when it is merged. Listed there: every book whose dict actually carries a
`catalyst` and/or `envoy` record — the eight published books (4438 and 2365 included), plus 0188 (both
records), 2140 (envoy only — see §6), 3115 (both records — see §6), 0156 (both records — see §6), 2231 (both records — see §6) and 0247, 1268, 0202 and 3001 (both records each — see §6) now that their rosters have been merged in. Canon-guide cases
with no book dict on the site at all (4425) or only an empty coming-soon
stub or a cast with no catalyst/envoy record (3312, 3887, 4442, 0000B, 2114, 4181) are not.

**Important:** the Observer/Envoy in each book is a *different individual*.
Ardwen (Sword of Valeria), the unnamed Observer (the Ledger), the Observer
at the bottom of the Golden Catacomb (the Stolen Prince War), and Vane (the
Iron Stiletto War) are four separate people — different appearance,
different disguise, different case. The Ledger's Observer has personally
logged "eleven thousand and one" cases by the time his closes; Ardwen is
specifically "Observer 000"; Vane is "the Wanderer," deployed as a hermit.
**Case 0157 breaks the delivery pattern rather than extending it:** nobody
hands its Catalyst to anyone — the Golden Catacomb is found, not given —
and its Observer is a stationary, unnamed old man seated at Level 101
(page: `observer-0157`), who hands Nairi her brother's recovered armor
without a word and apparently files the closing Custodian Diagnostic Log
himself. He has no name or number on the page; don't invent either, and
don't merge him with any other Observer.

### Book 1: *The Sword of Valeria* (Case 0000)

102 pages, published, real Google Books link in the script
(`BOOKS[0]["google_books_url"]`). Genre: Epic Fantasy · War & Military
Fiction (chosen by Claude at the author's instruction; no "suggested" label). Full synopsis is in the script and on the page —
not reproduced here for length. Ten characters: **the Boy** (protagonist,
deliberately unnamed, only epithets — one of which, "the Reckoner," is
*also* used by a completely different character in this same book, a
masked assassin — a flagged, unresolved naming collision, not an error on
this site's part), **Ardwen** (Observer 000, delivers the sword),
**Valeria** (the sword itself, written as a character), **Old Ren**
(raises the Boy), **Maren** (princess, later empress, believes in him),
**King Wendric** (fails to lift the sword, dies later still doubting his
legitimacy), **Corse** (Wendric's steward), **King Ossory** (false-flag
war conspiracy), **Cadmon** (later King of Ossory, the war's real
architect), and **the Reckoner (Assassin)** (hired to kill the Boy, spares
him). Eight scenes in chronological order (Claude's inference, not
author-confirmed) — see the script's `"scenes"` list on this book for the
exact order and captions.

### Book 2: *The Ledger of a Single Sweetness* (Case 4099)

Status: **Published**, with a confirmed Google Books link (`google_books_url`,
same field/pattern as Book 1) — no longer Coming Soon. Pages: **99**
(confirmed). Genre: **Literary Fiction &middot; Historical Fantasy &middot;
War & Military Fiction** — three real BISAC-style categories from the
author directly, not a guess, so the old single-genre `editor-note` wrapper
was dropped for this book. Cover file is literally named `Forty_Two_Entries`
by the author, which lines up exactly with the book's own core image:
**forty-two named casualties**, reconstructed one by one in the
manuscript's closing section. That "forty-two" is the actual organizing
device of the whole story — it's in the synopsis and the hook ("Forty-two
names, and the sweetness that cost them.") on purpose.

The premise: a Cultivator field agent enters a Heian-court-flavored society
disguised as a traveling confectioner and introduces a glass jar of pink
candy. The **Principal Handmaid** — the court's sole, absolute authority
on social rank — starts handing pieces out as rewards for small graces.
Receiving one turns out to be dangerous: most recipients die, are exiled,
or are executed over the course of the story, as court jealousy curdles
into an organized retaliation once the Handmaid's **Second Handmaid**,
Suzuriko, is passed over one time too many. Twenty-eight characters have
pages (26 individuals, one collective entry, and the catalyst itself):

| Slug | Name | One-line role |
|---|---|---|
| `tsuguo` | Tsuguo | Gambler; wins at dice against three ministers, becomes a target |
| `yorinaga` | Yorinaga | Falconer; dies in an "accident" after a hawk brings back a warm hare |
| `nariyuki` | Nariyuki | Poet; pushed from a balcony after a stone is deliberately swept |
| `kotone` | Kotone | 11-year attendant; executed on forged treason evidence |
| `principal-handmaid` | The Principal Handmaid | Court's sole rank-arbiter; the case's primary subject; dies in the tower fire |
| `rin` | Rin | Calligrapher; later "one of the season's casualties" |
| `michiko` | Michiko | Provincial cousin; a kindness from the capital ends her life |
| `emi` | Emi | Tutor; exiled over a resemblance in handwriting, dies in winter |
| `ai` | Ai | Court artisan; dies of an alleged fever with her partner Nozomi |
| `kaoru` | Kaoru | Twin gardener (with Fuyu); dies in the retaliatory campaign |
| `nozomi` | Nozomi | Court artisan; dies of an alleged fever with her partner Ai |
| `fuyu` | Fuyu | Twin gardener (with Kaoru); survives, grieving |
| `observer-4099` | The Observer | The Cultivator field agent running this case (see above — not Ardwen) |
| `suzuriko` | Suzuriko | Second Handmaid; architect of the retaliation; survives 31 years after |
| `nine-threads` | The Nine Threads | The retaliatory faction Suzuriko organizes — a collective entry, not one person; 5 named roles (Strategist, Forger, Poisoner, Broker, Keeper), 4 more "debts" left unnamed |
| `fujiko` | Fujiko | Court lady; a too-precise compliment gets her caught up in the reckoning |
| `tomoe` | Tomoe | Seamstress; later "one of the season's casualties" |
| `yuki` | Yuki | Lady-in-waiting; one of three rewarded for presence alone, becomes a casualty |
| `chiyo` | Chiyo | Wet-nurse; calms an infant prince, poisoned in the same porridge she made for others |
| `norikuni` | Norikuni | Court physician, advisor to the Handmaid; tries to warn her, dies of the poisoning he'd learned to diagnose |
| `the-sweets` | The Sweets | The jar of pink candy itself, treated as a character in its own right (cf. Valeria in Book 1) |
| `chika` | Chika | Lady-in-waiting; the second of the "three," rewarded for presence alone, becomes a casualty |
| `hana` | Hana | Calligraphy student, later instructor; keeps her own private ledger of bead recipients; survives |
| `sukeko` | Sukeko | Chrysanthemum expert; identifies eleven varieties in one afternoon, writes to her betrothed |
| `tadamori` | Tadamori | Kemari player; a 400-kick run earns a bead and, soon after, invented debts and a staged death |
| `obaa` | Obaa | Elderly seamstress supervisor; dressed three Handmaids before this one, becomes a casualty |
| `saemon` | Saemon | Minor scribe; a flawless sutra copy earns a bead, doesn't survive "the Harvest" |
| `nightingale` | Nightingale | Biwa player; a mourning song earns a bead, her hands are ruined in a staged "accident" |

**Hana** and **Norikuni** were the two names flagged in an earlier revision
of this file as real figures missing pages "because the author's own list
for this batch didn't include them yet." That batch has now arrived (this
revision) and both are added above — treat that flag as resolved, not as
an open item anymore.

One gap of the same kind is now open: Chika's own sheet describes her as
one of **three** ladies-in-waiting rewarded for presence and a correctly
timed smile, and Yuki's sheet shows her among the same group — but only
two of the three (Yuki, Chika) have been named and given pages so far. If
a third lady-in-waiting shows up in a future batch, add her the same way;
don't invent her in the meantime.

The book's cover file (`images/covers/4099.jpg`) already carries the same
"四十二の記 / FORTY TWO ENTRIES" calligraphy treatment as a standalone
title-card image the author has since sent separately — visually the same
piece, not a different or replacement cover. It wasn't wired in anywhere
new on this pass; there's currently no template slot on this site for a
freestanding title/divider card outside of a book cover.

Nineteen scenes now exist (the Ledger had none before this revision) — see
the script's `"scenes"` list on this book for the exact order and captions.
A few are worth flagging because they name or confirm plot mechanics not
spelled out anywhere else on the site: one scene shows a member of the
**Nine Threads** studying rows of handwriting samples labeled "Kotone"
under a heading of "SECRET INSTRUCTIONS" — direct visual confirmation of
*how* Kotone's forged treason evidence (§6 table, above) was actually
produced, not just that it existed. Another shows the Principal Handmaid
with three physical rows of beads labeled "Confirmed Dead," "Suspected
Victims," and "Unproven Names" — the clearest on-page depiction of what
"the Ledger" in the book's own title literally is. Two separate scenes
depict "the Nine Threads" — one the group itself (five women, fans raised,
plotting together) and one just their emblem (a blackened hand with nine
red threads tied to its fingertips) — kept as two distinct scene entries
rather than merged, since the manuscript batch supplied them as two
different images.

### Book 3: *The Stolen Prince War* (Case 0157)

96 pages, published, real Google Play Books link in the script
(`BOOKS[2]["google_books_url"]`) — treated as "published" on the same
basis as Book 1 (real cover, real synopsis, working purchase link, author-
confirmed page count), not as a guess. Genre: Epic Fantasy · Dungeon Fantasy · War &
Military Fiction (chosen by Claude at the author's instruction). Scene 17 of 19
(`the-weaver-falls`, file slug kept for continuity) depicts **the Nursemaid**, not
the Weaver Who Outlived Her Thread — corrected at the author's request.
Classification is confirmed, unusually: the manuscript's own
opening line reads "*Classification: Mythic Class. Archive: Cultivator
Terrarium Studies.*" — see the Cultivator-mechanic note above.

The manuscript's own title is "CASE 0157 — THE GOLDEN CATACOMB," and it
calls the war itself "the War of the Stolen Prince" in-text; the cover art
and the author both use "The Stolen Prince War," which is what's live on
the site. Both refer to the same book — not a title change mid-project,
just two names for the same thing (this is also why the source manuscript
file is named `Case_0157_The_Golden_Catacomb-FINAL.md` rather than
matching the cover).

The premise: a debt-poor kingdom, Ashkevar, finds a hundred-level dungeon
(the Catalyst, delivered as a discovery rather than handed to anyone) on a
hillside above the town of Har-Peleg. A neighboring highland kingdom,
Vantashen, sends its own delvers down — including a prince, Vartaz. Vartaz
dies when two rival parties collide in a guarded hall (the Ember Judge's
chamber, Level 40) and the room's own grace-count mechanism — built to
clear six fighters, not judge between two kingdoms — triggers on
schedule. Vantashen's king, Torvash, chooses war anyway, deliberately
pushed there by his son's own tutor, the hierarch Doreth, who tells
himself he's building the dead boy a monument rather than a lie. Three
years of war end in a negotiated "White Peace" and a dynastic marriage
(Nairi of Vantashen to Boaz of Ashkevar) that quietly unites both crowns.
Years later, Nairi leads twelve delvers — including Vahan and a hired
porter, Peled — back down to Level 101, where the Observer (the dungeon's
builder, a Cultivator field agent presenting as an ordinary old man) hands
her Vartaz's recovered, fire-damaged armor without explanation: literal
proof the death was mechanical, not martial. She chooses not to correct
the official record anyway.

**Previously flagged, now resolved:** an earlier pass on this book noted
that Vartaz, Doreth, Nairi, Ezra, Netzer, Berel, Shira, Tamir, Amitai, the
Ember Judge, the Widow (of the Tenth Hall), and the Weaver Who Outlived
Her Thread were all confirmed in the manuscript but had no art and
weren't on the site. A second batch of 18 sheets has since arrived
covering essentially every named figure and guardian left in the
manuscript, including several this file hadn't even surfaced yet (Boaz,
the Observer, the Hundred-Handed Reckoner, the Nursemaid, the Level 71
Guardian). All 18 are now on the site. Treat that flag as resolved the
same way Book 2's Hana/Norikuni gap was — if a *new* named figure shows up
in a future batch, add them the same way; don't invent one in the
meantime.

Thirty-five characters have pages now, covering the full cast the author
has sent art for. In addition to the seventeen from the first pass
(Hovan, Tirtzah, Vahan, Oren, the White Draught, Yudith, the Golden
Catacomb, the Magistrate of Empty Chairs, Sentinel of Dust, Elad, Vasak,
Torvash, Doron, the Multitude, Araxi, Ammiel, the Tide That Forgot the
Sea), the second batch added: **Peled** (porter, Nairi's Level 101
expedition), **the Weaver Who Outlived Her Thread** (Level 85 guardian,
paired with the Widow), **Doreth** (Hierarch of Solan, Vartaz's tutor and
the war's real architect), **the Ember Judge** (Level 40 guardian, kills
Vartaz), **the Hundred-Handed Reckoner** (Level 100, the last guardian
before 101), **the Widow of the Tenth Hall** (Level 10 guardian —
formal name for the guardian Chapter 4, "The Widow Who Would Not Be
Buried," is about), **the Nursemaid** (Level 54 guardian, guards the
approach to the heat-hallucination anomaly at 55), **Vartaz** (Prince of
Vantashen, Torvash's son), **Tamir** (founding five, breaks the first
guardian's arm with a mattock), **Boaz** (King Ammiel's second grandson,
later Nairi's husband and co-ruler), **the Observer** (slug
`observer-0157` — the Cultivator field agent who built and runs the
Catacomb; disambiguated from Book 2's `observer-4099` the same way),
**Berel** (founding five, proposes the first expedition, owns the "old
ruins kept old gold" line — see correction below), **Level 71 Guardian**
(a chorus of screaming carved faces; no fancier in-manuscript name was
given, so none was invented), **Netzer** (the shepherd who finds the
entrance), **Ezra** (Tirtzah's student, the guild's foremost theorist),
**Shira** (founding five, later captain, present at both the Widow's
discovery and Vartaz's death), **Nairi** (Vartaz's sister, later sole
ruler of both kingdoms), and **Amitai** (the court scribe who records
Nairi's account). Nineteen scenes were added in a later pass — see the
script's `"scenes"` list on this book for the exact order and captions, and
§7 for how they're ordered.

Quick reference — all 35 (the first 17 in the order they were added, then the
second batch; one-line roles are the site's own teasers):

| Slug | Name | One-line role |
|---|---|---|
| `hovan` | Hovan | Vantashen levy soldier; killed at a river crossing by a panicked shot |
| `tirtzah` | Tirtzah | Guild guide; dies testing her student Ezra's theory about a guarded hall |
| `vahan` | Vahan | Vantashen guard captain, Torvash's old captain; one of Nairi's twelve on the Level 101 expedition; shown a dead sister's face by the cold-corridor anomaly |
| `oren` | Oren | Delving captain; dies sealing Har-Peleg's wall breach with the fire that saves it |
| `the-white-draught` | The White Draught | The dungeon's rare healing vial, treated as its own entry |
| `yudith` | Yudith | Keeper of the Vigil of Ardwen; objects to the dungeon on doctrinal grounds, proven right too late |
| `the-golden-catacomb` | The Golden Catacomb | The Catalyst itself — the hundred-level structure, treated as a character (cf. Valeria, the Sweets) |
| `the-magistrate-of-empty-chairs` | The Magistrate of Empty Chairs | Guardian, Level 65 — a courtroom that refills with copies of defeated guardians |
| `sentinel-of-dust` | Sentinel of Dust | Guardian, Level 5 — the dungeon's first named guardian, kills Doron |
| `elad` | Elad | Har-Peleg baker's apprentice; kills Hovan by accident, learns his name 11 years later |
| `vasak` | Vasak | Vantashen general/councilor; argued against the war for a year and was right |
| `torvash` | Torvash | King of Vantashen; grief over his son's death drives him to war, abdicates after |
| `doron` | Doron | Founding Five delver; survives the founding party's first guardian but dies to the Sentinel of Dust on Level 5 |
| `the-multitude` | The Multitude | Guardian anomaly, appears off the normal every-fifth-level pattern |
| `araxi` | Araxi | Miller's daughter, engaged to Hovan the night before he's mustered |
| `ammiel` | Ammiel | King of Ashkevar; manages the diplomatic fallout, elevates his grandson Boaz to heir |
| `the-tide-that-forgot-the-sea` | The Tide That Forgot the Sea | Guardian, Level 20 — an environmental flood guardian, no body or source |
| `peled` | Peled | A porter hired to carry what the rest of the party can't — and to complain about it with real eloquence. |
| `the-weaver-who-outlived-her-thread` | The Weaver Who Outlived Her Thread | A guardian who weaves a single chamber-spanning thread before combat begins — and it doesn't break until you do. |
| `doreth` | Doreth | Prince Vartaz's tutor of eleven years, who turns his own grief for the boy into a war he tells himself is a monument. |
| `the-ember-judge` | The Ember Judge | The guardian whose floor-vent mechanism, triggered by two overlapping parties, kills Prince Vartaz. |
| `the-hundred-handed-reckoner` | The Hundred-Handed Reckoner | Not a being. A ledger made flesh, armed with a stylus, a scale, a blade, and a tally plate. |
| `the-widow-of-the-tenth-hall` | The Widow of the Tenth Hall | A veiled guardian who weeps a corrosive mist when struck — and turns out to be no widow at all. |
| `the-nursemaid` | The Nursemaid | A gentle, maternal guardian whose anatomy grows steadily, deliberately wrong the longer you look at it. |
| `vartaz` | Vartaz | A prince who travels to Ashkevar in disguise to prove himself — and dies to a mechanism, not a rival. |
| `tamir` | Tamir | A farmhand who breaks the dungeon's first skeleton apart with nothing but his own mattock. |
| `boaz` | Boaz | A coppersmith's apprentice turned second-in-line heir, who reads every clause twice before he'll sign it. |
| `observer-0157` | The Observer | The old man at the bottom of the hole, who built every level of it and remembers everything anyone ever left behind. |
| `berel` | Berel | The one who first says the doorway is worth opening — and spends the rest of his life letting the legends grow. |
| `level-71-guardian` | Level 71 Guardian | Dozens of carved stone faces, all screaming in perfect silence, all at once. |
| `netzer` | Netzer | A shepherd who goes looking for free firewood to pay a debt, and finds a hundred-level dungeon instead. |
| `ezra` | Ezra | The guild's foremost theorist of the dungeon, who never again tests an unproven idea on anyone but himself. |
| `shira` | Shira | Present at the founding, present at the Widow's discovery, present at Vartaz's death — and the one who mentors Nairi. |
| `nairi` | Nairi | Vartaz's own sister, who eventually holds the literal proof of how he died in her own two hands — and says nothing. |
| `amitai` | Amitai | The literal-minded scribe trusted to record Nairi's account — who can't quite leave a silence unexplained. |

**Two corrections made to the first batch once the second batch arrived:**
Doron's reference sheet had included the line "carries the guilt for
eleven years before learning the dead man's name," which contradicted his
own confirmed death at Level 5 and duplicated Elad's arc almost verbatim —
flagged rather than used the first time. Berel's own sheet (second batch)
directly attributes "Old ruins kept old gold" to himself, with the
manuscript agreeing, which confirms that line was never Doron's to begin
with; it's been moved to Berel's entry and dropped from Doron's (now
`"quote": None`). Separately, the manuscript is explicit that **Tamir**,
not Doron, lands the founding party's one real blow (breaking the first
skeleton's arm with a farm mattock) — Doron's bio no longer claims a
"first blow" that was never his. Both fixes are content corrections, not
just flags; no further action needed unless the author disagrees.

### Book 4: *The Iron Stiletto War* (Case 4417)

Status: **Published**, with a Google Books link supplied by the author
(`google_books_url` on this book's dict, `BOOKS[3]`) — wired in without
being opened, since Google blocks automated fetches, so it's worth one
click to confirm it lands on the right book. Pages: **109** (author-confirmed). Genre: Epic Fantasy · Political
Intrigue · War & Military Fiction (chosen by Claude at the author's
instruction; no "suggested" label).

The premise: **Vane** ("the Wanderer"), a Cultivator field agent disguised
as a hermit, delivers a pair of indestructible chrome stiletto heels to
**Queen Aurelia** of Solis as Case 4417 — inside the Mundane Class range (4000–4999),
a second data point for that range alongside Case 4099. Aurelia
wears them to the Great Concord; **Duchess Beatrice** of Ironhold is
publicly humiliated by them and refuses to let it go. What starts as
wounded vanity escalates into a full war between Solis and Ironhold: the
Order of the Pale Cloth (High Cleric **Ambrose**) declares the heels
heretical, **Baron Corvin** plays both sides for his own gain while
extracting intelligence from **Isolde** (wife of peace-favoring **Lord
Fenric**), the siege reaches Solis, and **Duke Aldous** is killed by
Aurelia's own heel in the Great Hall. Aurelia is deposed shortly after.
Chancellor **Wren** — who has Corvin quietly poisoned once his scheming is
proven — ends up ruling both crowns for eleven years afterward, and the
novel is partly framed as his own private, unburned letters looking back
on it. Thirteen characters have pages: **Osric** (Ironhold's steward),
**Wren**, **Ophelia** (Aurelia's messenger), **Iset** (Beatrice's
spymaster), **Fenric**, **Beatrice**, **Corvin**, **Aldous**, **Vane**,
**Isolde**, **Ballard** (Solis's army commander), **Ambrose**, and
**Aurelia**.

The chrome heels themselves were *not* given their own character page
(unlike Valeria in Book 1 or The Sweets in Book 2) — the batch didn't
include a matching character-sheet-style portrait of them alone, only a
close-up in the separate painterly "scene" art style, so it was used as a
scene instead (`the-chrome-heels`). If the author sends a proper
character-sheet portrait of the heels later, add it as a fourteenth
character following the object-as-character pattern (epithets ending in
"the Catalyst of Case 4417," per The Sweets' precedent) and move the
close-up scene image over to be its portrait.

Eleven scenes exist, all in a distinct thick, palette-knife painterly
style that's different from the 13 watercolor character sheets: the
original four were Vane delivering the heels, the heels alone on a dais,
Corvin and Isolde by a fireplace, and Ophelia delivering Aurelia's refusal
to Beatrice; the latest merge (§8) added seven more that master had been
missing — Vane alone by candlelight, Aurelia at the Great Concord, Aurelia
crossing the hall, Aurelia enthroned, Corvin presenting Isolde with dyed
silks, Ophelia glancing back down a corridor, and Beatrice's prison visit
to the deposed Aurelia. Scene order and captions for the original four are
Claude's inference from the art plus the manuscript's own outline and
chapter titles, not author-confirmed; the later seven were taken exactly
as the SLAVE-4417 staging copy had them, interleaved into the existing
sequence rather than re-derived. The manuscript itself (a complete,
"Revision 4 (Final)" draft) was read only for these facts — it hasn't had
any editorial/proofreading pass.

### Book 5: *The Vessel of the Betrayed Host* (Case 4420)

**Renamed from *The Thermal Vessel War*, at the author's request.** The old
title survives nowhere on the site or in this script — every reference
(title field, the inline `<em>` mention inside the synopsis, nav/roster/
cast-wall auto-links) now reads *The Vessel of the Betrayed Host*, which
was already the in-story name the synopsis gives the relic once Yvaine
cases it in silver ("renamed the Vessel of the Betrayed Host"). The book's
own title now simply matches the object's own in-fiction name, the same
way *The Vessel of Unmediated Grace* (Case 4555) is object-named rather
than war-named. Don't reintroduce the old title from memory.

Status: **Published**, with a Google Books link supplied in the
SLAVE-4420 staging copy (`google_books_url` on `BOOKS[4]`) — wired in
without being opened, same caveat as Book 4's. Pages/genre are still that
copy's own unconfirmed estimate (`~123` pages, suggested genre, both
still carrying the `editor-note` span) — unlike Books 1–4, nobody had
confirmed these for real yet. **Superseded 2026-10-17: the author gave 130 pages and the genre
*Fiction / Fantasy / Epic*, and both now stand without the `editor-note` span.**

The premise: House Skarth has carried one steel flask for four centuries
without asking where it came from — family legend says it came down from
the dragon who keeps Mount Skahr, and it never lets its contents go cold.
When **Duke Maros**, humiliated by a rival's gift of a stag's head, drags
a royal hunt two hundred miles into the northern tundra to answer it,
**Baron Kaelen** of House Skarth joins on guest-right alone. Eleven nights
in, starving and out of other food, Kaelen finally opens the flask to
feed the King — the broth hits the cold air as a white cloud, and **Sir
Corvus**, a royal guard still reliving a spore-cave that nearly killed him
eleven months earlier, kills Kaelen on reflex before the cup arrives. The
Crown's own account is accurate in every clause and never mentions broth;
House Skarth reads it as a signed confession. Kaelen's twin, **Yvaine**,
cuts her hair, takes his mail, climbs the mountain for a blessing, and
leads the northern clans south with the flask — now cased in silver and
renamed the Vessel of the Betrayed Host — at the front of the column.
**Duke Vane** of the Southern March (a different man from Book 4's Vane
the Wanderer; the bio flags this explicitly, and the site file uses the
`vane-4420` slug to keep the two pages apart) sells a broken Maros his
rescue at ruinous cost, hires the thief **Soren** to steal the relic back,
and dies never understanding what he actually fought over. No southern
chronicle will name the war honestly; it comes down in the histories as
the Great Winter Pestilence. Seven characters have pages: **Kaelen**,
**Yvaine**, **Maros**, **Corvus**, **Vane** (`vane-4420`), **Soren**, and
the Envoy, **Observer 814**.

Like the chrome heels in Book 4, the flask itself has no dedicated
character page — the roster thumbnail on the Catalyst lore page points at
a scene image (`soren-with-the-flask`) instead, the same pattern, for the
same reason (no standalone portrait of the object came with this batch).
`BOOKS[4]`'s `catalyst`/`envoy` summary dicts didn't exist yet in the
SLAVE-4420 copy — that field was added to master's schema after this
staging copy forked — so both were written fresh during the merge:
catalyst **The Steel Flask** (Mundane Class, matching Case 4099 and Case
4417 in that range) and envoy **Observer 814**, &ldquo;the
Dragon-Speaker,&rdquo; so Book 5 doesn't silently drop out of either
roster (see below, &ldquo;Rosters&rdquo;). Seventeen scenes exist, in the
same palette-knife painterly style as Book 4's; order and captions came
from the SLAVE-4420 copy as authored and were not independently
re-verified against a manuscript by this session.

### Books with a roster but no synopsis yet: 0188 and 2140

Two more `BOOKS` entries now carry a full cast even though `status` is
still `["coming-soon"]` — don't read "coming-soon" as "no content." 0188
has a real synopsis with estimated page count and suggested genre; 2140
still has the bare `EDITOR_*` placeholders for all three. Don't flip
either to `published` without the author confirming the details first.

**Case 0188, *The Songs Never Mention the Cats*.** Merged in from a
staging copy (SLAVE-0188) that forked from master and filled in a full
synopsis, a 12-character cast, a 12-scene gallery, and both a `catalyst`
(**The Eternal-Grief Lily**, Mythic Class) and `envoy` (**Somadatta**,
Envoy Archetype 03) record — so, unusually for a coming-soon book, it
already carries a real synopsis and both roster records. Its `~40` pages
and suggested genre are the staging copy's own unconfirmed values, with
the same `editor-note` spans Book 5 has, and the status tag is still
coming-soon. Cast: Dharmasena, Chandralekha,
Haridasa, Somadatta, the Eternal-Grief Lily, Vaidyanatha, Kamalini, Dhumra
(Kamalini's cat), Govinda, Bhadraka, Dhanapala, Ravisena.

**Case 2140, *The Third Grain*.** Merged in from a separate staging copy
(SLAVE-2140) that added a 15-character cast only — `pages`, `genre`, and
`synopsis_html` are still the bare `EDITOR_*` placeholders, unlike 0188.
Cast: Garibald, Observer 419, Teudis, Garibald's Mother, Landulf, Gisela,
Ansfrid, Grimoald, Gisulf, Grimoald's Father, Grimoald's Wife, Adelrada,
Vitalis, Ranulf, the Eldest Witness of the Writ. The staging copy had no
`envoy`/`catalyst` records either (it forked before this schema field
existed on stub books, the same gap Book 5 had — see §8); an `envoy`
record for **Observer 419** ("Itinerant Clockmaker") was written fresh
during the merge, from his own character bio, so 2140 isn't silently
absent from `lore/cultivator.html`. **No `catalyst` record was added** —
the precision bearing itself has no character portrait and no scene image
to point a roster thumbnail at (2140's `scenes` list is still empty), so
inventing one would mean a broken `<img>` on the Catalyst lore page. Add
it once real art exists for the bearing itself or a scene depicting it.

### Book: *The Listening Water* (Case 3115)

Status: **Coming soon** — not yet published. This pass added only the
character roster (24 pages, plus fresh `catalyst`/`envoy` summary dicts)
from a batch called `WEB CHANGE 3`, which included 24 character-sheet
portraits and the complete manuscript (used for context only, per the
author's own instruction: &ldquo;add 3115 char, i include the manuscript
draft for context&rdquo;). `pages`, `genre`, `synopsis_html`, and `status`
are untouched and still the `EDITOR_*` placeholders; no scene art has
arrived yet either. (Note: this file has no dedicated write-up for Book
6, Case 4555, *The Vessel of Unmediated Grace* — it was merged in a
session that didn't update this doc. Its data is complete and live on the
site; only this handoff's own notes are behind. Worth a future pass
filling that gap in separately.)

The premise, reconstructed from the manuscript for this write-up (not
author-confirmed as final jacket copy): the Threefold Crown faith's
Father's Reckoning makes whoever a ceremony declares a father to be the
*legal* father, regardless of blood — precedent: the **Duke of Yanshui's
Third Son** inherits over two blood cousins. King **Huairen** of Qinghe
is 79 and dying, slowly poisoned by his own Queen's steward, **Cao**, on
Chancellor **Jian**'s orders. Nine years earlier, Queen **Meilan** had an
affair with the King's own half-brother, **Huaiyu** (March-Lord of
Beiyan); their son, Prince Jiyun, was sealed to the throne as Huairen's
own by **Warden Peizhi**'s Reckoning. The whole plot turns on a
Cultivator Catalyst: **the Listening Water**, a stoppered bottle of 5
sips smuggled into Qinghe as ordinary trade stock by **Observer 471**
(&ldquo;the Salt-Root Woman&rdquo;), sold on by **the Under-Steward** of
the palace kitchens. A sip grants 15 minutes of a nearby animal's own
perception. Maid **Suyin** drinks one by accident via the Queen's caged
finch and learns the truth about Jiyun's parentage; she's found dead days
later (**the Kitchen Boy** finds the body; **the Physician**, deliberately
not **Mingxuan**, rules it an accidental fall) after court poet
**Yancheng** unwittingly tips off the household through his beloved
**Chunhui**. Mingxuan (the King's own alchemist) becomes the story's
investigator, eventually using the Water himself, tracing the King's
poisoning through the King's own lapdog **Xiaobao**'s fear of Cao's step,
and getting smuggled out of Jinlu by chamberlain **Duan** once Jian
recasts his own investigation as a coup. War follows Huairen's death;
General **Zhuo** shelters the loyalists at Wanling, his own standing
order gets Yancheng killed by young officer **Rao** (who confesses to
Mingxuan 11 months later), and Huaiyu himself dies at the Shuang ford,
shot by **the Soldier Who Killed Huaiyu**, never knowing the boy he was
fighting over was his own son. It ends on the Jinlu Concord, and an
epilogue beat decades later: **the Scribe's Apprentice** asks an old
Mingxuan the one true question anyone in Qinghe ever asks him outright,
and neither of them writes down his answer.

Twenty-four characters have pages, added in this one batch: **Huairen**,
**Meilan**, **Huaiyu**, **the Listening Water** (the Catalyst, treated as
a character per The Sweets' precedent), **Suyin**, **Mingxuan**, **Cao**,
**Duan**, **Jian**, **Peizhi**, **Yancheng**, **Chunhui**, **the
Physician**, **the Kitchen Boy**, **the Custodian** (Cultivator oversight
staff — distinct from a field Envoy, no disguise or ground presence, just
audits terrarium records), **Zhuo**, **Rao**, **the Soldier Who Killed
Huaiyu**, **the Herald** (`the-herald`), **the Under-Steward**, **the
Scribe's Apprentice** (`the-scribes-apprentice`), **Duke of Yanshui's
Third Son** (`yanshuis-third-son`), **Xiaobao**, and the Envoy, **Observer
471** (`observer-471`). No slug collisions with the existing 132
characters, so none needed disambiguation. Cultivator and Catalyst lore
prose each picked up one new line for this data point, the same way Case
4420's did.

The reference-sheet art for this batch is a different in-house style from
earlier books' character portraits: each sheet is itself a dense, labeled
design document (name, role, age, a physical-traits list, an in-world
quote where the author chose to give one, small captioned story-moment
vignettes), not just a single portrait plus a detail crop. Nothing about
the schema needed to change for it — full/thumb images are still a
straight proportional resize of the whole sheet (980w / 320w, same as
every other character), and the `alt` text template (&ldquo;Character
reference sheet for %s&rdquo;) turns out to describe this whole site's
character art exactly, not just this batch's.

### Book: *The Heavenly Thunder-Serpent* (Case 4438)

Status: **Published** (Google Books). Added straight into master (no staging
copy) from a batch containing the cover, the complete manuscript
(`Case_4438_The_Heavenly_Thunder-Serpent_2026-09-14_1215PM_GMT_7_FINAL.md`), a
zip of 19 character reference sheets and 15 scene paintings, and the Google
Books link `https://play.google.com/store/books/details?id=hRoSEgAAQBAJ`
(not opened by an AI: Google blocks automated fetches, the same gap as the
4417 and 4420 links). **`pages` was the `EDITOR_PAGES` placeholder when first merged; the author has since given it as 82** (Oct 2026 update) &mdash;
the Google page itself still could not be read. Genre
(*Historical Fantasy &middot; Political Intrigue &middot; Tragedy*) is Claude's call
(§8). The synopsis, character bios and scene captions were written from the
manuscript and the sheets; they are not author-confirmed jacket copy.

The premise: a fisherman, **Ren Duo**, is shocked by something black under a
fallen lintel in the flooded ruins below Nine Bends and does the honest
thing &mdash; tells the magistrate. The Yan court takes the creature alive (six
men drown securing the transport), the Chief Alchemist **Zhou Xuan** names its
water the Nectar of the Thunder Dao, and court Reckoner **Mei Suwen** keeps the
only accurate ledger of its discharge intervals. The **Yongkang Emperor**,
raised on a prophecy that Heaven owes him a debt, enters the water in full
ceremonial armor at the Solstice Trial and dies; his son **Prince Yue**, the
one man who understood Mei Suwen's numbers, turns the Second Trial into a
purge &mdash; twelve ranking officials enter the basin, eleven die, the eleventh
man to enter survives because the eel has nothing left. A southern warlord,
**Du Heng**, takes Yujing, has the basin filled with stone, and the chronicles
record that the Fetus of the Chaos Epoch departed the world of its own accord.
The Cultivator's own log: Case Study 4,438, Mundane Class, **Elder Peng**
(Observer 403) having entered the unauthorized phrase &ldquo;rounding error&rdquo;
eleven times.

Nineteen characters have pages, in this order (the first six feed the
homepage cast wall): `mei-suwen`, `yue`, `yongkang-emperor`, `ren-duo`,
`the-heavenly-thunder-serpent` (the Catalyst, treated as a character per the
Listening Water precedent), `elder-peng` (the Envoy), `wan-er`, `sun-lin`,
`kang-yi`, `zhou-xuan`, `fu-baishi`, `physician-kao`, `zheng-kui`,
`meng-kuo`, `pei-rong`, `du-heng`, `master-bai`, `zhuo-sheng`, `yun-wei`. No
slug collisions with the existing 156. Fifteen scenes, in story order (first
`the-net-meets-the-serpent`, last `the-teahouse`); the homepage scene band
gets the eighth entry `the-solstice-ascension`. Catalyst record: the eel
(Mundane Class), pointing at its character page; Envoy record: Observer 403
(&ldquo;the Hermit of Nine Bends&rdquo;), pointing at Elder Peng's page. Cultivator
and Catalyst lore prose each picked up one new line, as with 4420 and 3115.

Judgment calls worth knowing: (1) **Kang Yi's sheet contradicts itself** &mdash;
it says both &ldquo;25 years of service&rdquo; and &ldquo;nineteen years,&rdquo; and lists
&ldquo;25 years old&rdquo;; the manuscript says nineteen, so the page says nineteen and
gives no age. (2) **Observer 403** and the **141 local years** come from
Elder Peng's sheet only; the manuscript never numbers him. Master Bai's age
(66), the name &ldquo;Heaven-Shattering Thunder Strike&rdquo; and Pei Rong's being the
*second* to enter the water likewise come from the sheets. (3) One scene
(`the-eleventh-entrant`) shows an unnamed man standing unharmed in the basin;
it is captioned as the survivor of the Second Trial from the image alone &mdash;
change the caption if the author meant someone else. (4) &ldquo;The Reckoner&rdquo; is
Mei Suwen's title here, a third use alongside the Boy's epithet and the
assassin's contract-name in Case 0000 (see that book's naming-collision note
above); they are different characters, and no slug collides. (5) The canon
guide lists a **Case 0333 &ldquo;Thunder-Serpent Eel&rdquo; (Mythic Class)**; this
manuscript is **Case 4438, Mundane Class** and never mentions 0333, so the
site follows the manuscript. Whether they are the same story is the author's
call.

Images: cover 900w; character sheets 980w / 320w thumb; scenes 1000px long
edge / 450px grid &mdash; the same specs as every other book. The Case 4420 cover
was replaced in the same pass (new file, same name `4420.jpg`, same 900x1350).

### Book: *The Purging of Charsianon* (Case 0156)

Status: **Coming soon** (awaiting release; the author's word was &ldquo;not published&rdquo;). Added
straight into master from a batch of: the cover (`0156_0_5x.jpg`, titled **The Purging of
Charsianon**, tagline &ldquo;Ledger. Unhastening. Reconstruction. Arithmetic. Filed.&rdquo;),
26 character reference sheets, 14 scene paintings, and the manuscript
`Case_0156_The_Vault_of_the_Carbon_Echo_2026-10-01_0444AM_GMT_7.md` (revision 3, about 14,700
words), which arrived in a follow-up message. **`pages`, `genre` and `synopsis_html` are
untouched `EDITOR_*` placeholders** (the 3115 precedent: manuscript used for context only).

**Title:** the site follows the cover, *The Purging of Charsianon*. The manuscript's own title is
*The Vault of the Carbon Echo*, and the manuscript's epilogue says the surviving chronicles
remember the affair as &ldquo;the Purging of Charsianon&rdquo; &mdash; so the cover title is the in-world
chronicle name. (Same pattern as 0000B, whose cover title differs from its manuscript's.) If the
author would rather have *The Vault of the Carbon Echo* as the site title, it is one string in the `0156` dict.

The premise, from the manuscript (not author-confirmed jacket copy): a goatherd, **Georgios**,
chasing a nanny goat, leans across the threshold of a buried, dormant bio-reconstruction beacon
under Hemiakmon Ridge (**the Carbon Echo**; Mythic Class, 0000 Series) and notices nothing. Six
years on, its containment faults climb (13, 21, 34, 55, 89) and the valley hears a keening it calls a
demon. **Lord Bardas** of Charsianon, who hears an unbalanced ledger rather than a ghost story,
rides up with twelve knights; the chamber takes a full accounting of all thirteen, discards the
originals, and returns exact copies, flawless in everything measurable and flattened in affect. Bardas
forgives debts, loses all use for favor and fear, and becomes perfectly, unbearably just. His wife
**Theodora** is the first to name the absence. **Keeper Photios** of the Dorylaion Vigil names it the
Doctrine of the Stolen Vessel (and wants the tithes of Charsianon's own House of Vigil back),
**Lord Leo** supplies a forty-acre grudge and a speech, **Lord Constantine** and **Lady Anastasia**
join for fishing rights and a marriage, and the mercenary **Melias** commands 1,100 spears and 400
horse. Bardas does the arithmetic and walks out of his own gate unarmed with the Twelve; all thirteen
are executed, Bardas last by **Loukas**, who asks for last words and is given a lecture on the
blade's metallurgy. The resulting panic burns the countryside. The Custodian's log (the **Quiet One**,
a child-shaped Observer who has watched four generations and may only record) flags Bardas's
voluntary self-termination as a calculation no standing model predicted.

Twenty-six characters have pages, in this order (the first six feed the homepage cast wall and are
the case's principals): `bardas`, `theodora`, `the-carbon-echo` (the Catalyst, treated as a
character per The Sweets' precedent), `the-quiet-one` (the Envoy), `keeper-photios`, `lord-leo`,
`kyr-symeon`, `kyr-niketas`, `kyr-andronikos`, `loukas`, `melias`, `brother-ignatios`,
`georgios`, `petros`, `basileios`, `artavasdos`, `marina`, `zoe`, `stephanos`, `ioannes`,
`theoktistos`, `kassia`, `isidoros`, `lord-constantine`, `lady-anastasia`, `ardwen-0156`. Fourteen
scenes in story order (first `the-goatherd-and-the-fissure`, last `the-burning`). Catalyst record:
the Carbon Echo (&ldquo;Mythic Class&rdquo;, which also makes 0000 and 0157 its automatic related cases);
Envoy record: the Quiet One (&ldquo;Custodian Observer&rdquo;, no observer number given anywhere).
Cultivator and Catalyst lore prose each picked up one new line, and the Faith of Ardwen's
`appears_html` gained a sentence naming 0156, so the faith-sharing logic now relates it to 0000 and 0157.

Judgment calls worth knowing: (1) **`ardwen` was taken** (Case 0000's Observer 000), so this goddess is
`ardwen-0156`; her page links back to the 0000 page. Her sheet is *traditional iconography* (crown, tear,
white lily, &ldquo;Mother of Mercy&rdquo;) while the manuscript says Houses of Vigil are unadorned by any
image; the page reports both and does not reconcile them. (2) **Photios**: the sheet says *Bishop of
Dorylaion*, but manuscript revision 2 deliberately changed bishop to **Keeper** (Ardwen-world
vocabulary), so the page says Keeper and the slug is `keeper-photios`. (3) The Carbon Echo's
sheet says &ldquo;memory rewritten&rdquo;; the manuscript says memory was copied faithfully in everything
measurable. The page uses the manuscript and quotes only the sheet's limbic-resonance / affect notes.
(4) The analyst note in the Archival Log calls its subject &ldquo;Subject B. (primary reconstruction)&rdquo;;
Bardas's page treats that as him, which is an inference. (5) **Scene captions are written from the
images and the manuscript.** `the-valley-listens` is the vaguest (a night village under a swirling sky
beside the ridge); `the-chamber-takes-its-count` shows thirteen figures before a column of light in a
crystalline hall, captioned as the chamber scene rather than the undercroft council; `a-justice-without-warmth`
is captioned from chapter 8 (Bardas reviewing judgments). Change any that miss. (6) Isidoros's &ldquo;ages
unusually slowly&rdquo; is from his sheet only; the manuscript only has a villager wondering about him once.

Images: cover 900x1350; character sheets 980w / 320w thumb; scenes 1000px long edge / 450px grid &mdash;
the same specs as every other book.

### Book: *The Decree of Luminescence* (Case 2365)

Status: **Published** (2026-10-10), with `pages` "88" and a Google Play Books link
(`https://play.google.com/store/books/details?id=spIXEgAAQBAJ`; the link has not been opened by an AI),
both sent by the author in chat, which is the confirmation to publish. It was merged into `main` as
coming-soon on 2026-10-09 via pull request #1. **`synopsis_html` was written on 2026-10-12** (three
paragraphs, in the house style of the other published cases, drafted by Claude from manuscript revision 3
at the author's request; it is not author-confirmed jacket copy, so the author may want to rewrite it).
**`genre` is still an `EDITOR_*` placeholder**, so the page shows an empty genre spot until the author sends it. Built on
branch `case-2365-stub` from: the cover
(`images/covers/2365.jpg`, tagline "Ash. Roll. Residue. Append. Nil."), 24 character reference
sheets (two batches), 15 scene paintings, and the manuscript
`Case_2365_The_Decree_of_Luminescence_Final.md` (revision 3). **`genre` and
`synopsis_html` were originally left as untouched `EDITOR_*` placeholders** (the 0156 / 3115 precedent: the manuscript
was used for the bios and captions only); the synopsis was filled in later, as noted above, and the author gave the genre on 2026-10-17 (*Fiction / Fantasy / Historical*). The case was first committed as a cover-only stub, then
filled in.

The premise, from the manuscript (not author-confirmed jacket copy): Vallombra, a terraced kingdom
that rules by arithmetic and keeps the Concord of the Year (the sky shows up on the dates in the
Table), is buried in ash when the Ashduct hills breathe. Its Reckoner, **Severin**, extends the
year's grace from three days to a season and, on the morning of the third spring's First Furrow,
states a false figure: the sun will stand over the Round at the sixth hour. He is **Observer 117**,
Custodian of record for a dormant aperture unit (**the Round-Bed**) beneath the tower; he activates
it and the ash parts in a hard-edged column, the Standing Noon, held open for 421 days. His senior
apprentice **Piero** compiles the Roll of the Lit, from which a copyist's guttering lamp drops 311
names of the Saltway Quarter. Hungry Verrenhal marches south under **Sigrid** (the Staff-Keeper, who
says on the first day that the light has an edge, so someone is holding it); a herald's mistranslation
of "the low hour" sends four thousand uncovered northerners across the line into noon, and the
wardens of **Rufio**'s Edge loose for eleven minutes (2,304 dead, six of the Order). **Faustin**
the king dies of the soup he ladles. **Marcello** finds the omitted column and the forged names, and
he and Piero vow to correct it in the open on the day **Livia** is twenty-one, a promise deferred for
three centuries. Piero's scaffold hardens into the Decree of Luminescence, Vallombra becomes
Illumaria, and the Order writes one word, *Nil*, every evening. The Corps' closing audit files it all.
It is the founding of the faith that the lore page and Case 4555 already describe.

Twenty-four characters have pages, in this order (the first six feed the homepage cast wall and are the
case's principals, a first pass): `piero`, `severin` (the Envoy), `marcello`, `livia`, `faustin`,
`sigrid`, then `arne`, `ragnvald`, `fulvio`, `rufio`, `nardo`, `costanza`, `aldo`, `lino`, `nina`,
`tito`, `the-goldsmith`, `anselmo`, `the-granary-physician`, `the-tanners-widow`, `the-nameless-girl`,
`the-senior-clerk-of-the-hall`, `the-interpreter`, `the-herald-2365`. Fifteen scenes in story order:
`the-share-breaks`, `the-standing-noon-opens`, `the-crowds-come-to-the-light`, `piero-reads-the-gold`,
`the-reckoner-is-taken-up`, `the-lamp-that-guttered`, `the-host-crosses-the-pass`,
`sigrid-reads-the-edge`, `the-parley-at-the-saltway-gate`, `the-blinding`, `the-king-ladles-the-soup`,
`marcello-reconciles-the-roll`, `the-child-queen-is-crowned`, `the-grand-basilica`,
`the-first-judgment`. Roster records: Catalyst **The Round-Bed**, Envoy **Observer 117** ("the
Reckoner", page `severin`). Cultivator and Catalyst lore prose each picked up one sentence; the Decree
of Luminescence `appears_html` now names this case, so the faith-sharing logic relates 2365 and 4555.

Judgment calls worth knowing: (1) **The Catalyst has no character sheet**, so its roster row links to
the case page and borrows a scene image (`the-standing-noon-opens-grid.jpg`), the same way Case 4417's
chrome heels do. The name is the manuscript's own designation ("the Round-bed", Interlude II). Its
`meta` reads "Atmospheric aperture unit" because the manuscript gives no Class for 2365 (only the
number, 2,365); don't invent one. If a sheet arrives, add a `the-round-bed` character page and repoint
the record. (2) **`the-herald-2365`**: `the-herald` is Case 3115's. No other slug collided. (3) The
**Marcello** sheet calls him "senior apprentice alongside Piero" while the manuscript calls Piero the
senior of the seven; the page follows the sheet and keeps both. (4) **Scene art versus text.** The
parley painting puts Piero's party on the lit side but a helmeted soldier and a book-holder on
Sigrid's (the text has Rufio and Marcello with Piero) and a blindfolded figure on the lit side, so the
caption names only Piero and Sigrid. `the-reckoner-is-taken-up` shows a stair and a boy where the text
has the parapet and a 24-year-old; the caption follows the text. `the-host-crosses-the-pass` shows the
gold glow far below, so it sits at Chapter 10 rather than the Chapter 4 departure. (5) The
Interpreter, the Nameless Girl and the Granary Physician's looks are the sheets' own inventions, and
their bios say so. Costanza's "holds her pen still" and Anselmo's glass-dust hands and cough are from
the sheets too and are labelled as such. (6) Nina is never shown alive; her sheet draws her only as
remembered. (7) Images: cover 900x1350; sheets 980w / 320w thumb; scenes 1000px long edge / 450px
grid, the same specs as every other book. Every portrait and scene was checked against its name
on a contact sheet of the files as built.

### Book: *The Stone of the Clean Hand* (Case 2231)

Status: **Coming soon** (awaiting release; no purchase link was supplied). Added straight into
`main`, the cover-and-sheets pass in one go, from: the cover (`images/covers/2231.jpg`, tagline
"Cat. Hand. Stone. Signature. Omitted."), 18 character-dossier sheets, and the manuscript
`Case_2231_The_Stone_of_the_Clean_Hand_2026-10-08_1630PM_GMT+7.md` (revision 7). **`pages`, `genre`
and `synopsis_html` are untouched `EDITOR_*` placeholders**, and there are **no scenes** yet
(`scenes: []` in that first pass; the 14 records and 25 more Subjects came later, see the update
paragraph at the end of this section). The manuscript was used for the bios only.

The premise, from the manuscript (not author-confirmed jacket copy): the subject world is 812-G.
Himuro, the Japanese side, is the successor population of the court of Case 4099 (hence the
`RELATED_THEMES` row linking the two). Vilarnau and Castelmaur are in Auvarre, under the Threefold
Crown. **Observer 618**, a mute stonecutter, is the Dumb Mason of a pair of matched one-way
matter-transit stones, the **Kiyote Pair**: one stands in a shrine, the other on a village green.
A cat, the Fifth Article, the Stone's tally, the Hearth Weighing and distraint, a night of torches,
the quarry gate, Lasserra and a nineteen-year wait are the beats; the ending is open. By the
author's Revision 6, **Higaide** is not dead, and returns after Cases 0202, 1414, 0333 and 0456.
In the Threefold Crown's lore, a hearth-priest's honest report of a stranger's bow to Solan's Fire
and refusal of the feast-pig reaches Hierarch **Odilo** at Castelmaur, who lays the temple's interdict
on a whole lane until its idol is cast down. That is the sentence the lore page now carries.

In the first pass eighteen characters had pages, in this order: `observer-618` (the Envoy), `shizuka`, `jokei`
(Jōkei, written with ō on the page), `sadamune`, `kanemichi`, `kurige`, `bureau-officers`,
`bertran`, `gersenda`, `bernat`, `brunissen`, `villagers-of-vilarnau`, `masons-of-castelmaur`,
`castelmaur-men-at-arms`, `folquet`, `odilo`, `guilhem`, `jaume`. The `PRINCIPALS` entry (the six who
feed the homepage cast wall, a first pass) is `observer-618`, `shizuka`, `jokei`, `sadamune`,
`bertran`, `gersenda`. Roster records: Catalyst **The Kiyote Pair** ("Matched one-way matter-transit
stones", page `books/2231.html`), Envoy **Observer 618** ("the Dumb Mason", page `observer-618`).
Cultivator and Catalyst lore prose each picked up one sentence, and the Threefold Crown's
`appears_html` now names this case (it also changed "And in" to "In" at the start of the 2140 sentence
before it, so that "And in" only opens the last sentence).

**Only characters with a sheet have pages** (18 in the first pass, 43 now; see below). Higaide (the
protagonist), Arikuni, Yasutsugu, Tamenaga, Narimune, Peire and Guiraut still have no sheet and so no
page. Don't invent them; add them when art arrives, and add them to the roster in story order.

Judgment calls worth knowing: (1) **The Catalyst's roster image**
(`covers/2231-stone-thumb.jpg`) is a 2:3 crop of the cover (the hand, the green vein and the
notches, no title text). A Kiyote Pair sheet has since arrived: `the-kiyote-pair` is a character page
and the roster row's page now points to it (the image is unchanged). (2) The `hook` is the cover's own tagline,
verbatim. (3) Observer 618's "thirty-one years" as a quarry-hand is 12 + 19 (the manuscript gives the
two figures separately); don't re-derive it differently. (4) Details that come from the *sheets* and
not the manuscript are labelled as such in the bios: Kurige's age (7) and white sock, the Bureau
Officers, Jaume. (5) 2231 shares the Threefold Crown with 0157, 4417 and 2140, so the faith-sharing
logic relates them automatically. (6) Slugs: `jokei` and the rest did not collide with any existing
slug; character slugs are one global namespace (checked). (7) **Lesson from this run:** the first
draft of the bios was written before the manuscript had been read, and it contained errors (an
invented Bureau-Officers bow, a wrong order of Observer 618's dust, bow and bread-heel sequence, a
misattributed "four for four" line, and a few wrong details for Bernat, the Masons, the men-at-arms,
Odilo and Gersenda). All of them were corrected against the manuscript, and a script then checked
every capitalised name and number in the bios against the manuscript text. Read the manuscript
before writing a bio, not after. (8) Images: cover 900x1350; sheets 980w / 320w thumb, the same
specs as every other book; every portrait was identified by looking at its title strip, never by
the order of the attachments.

**Update: 25 more Subjects and 14 Records (branch `case-2231-records-v2`, pull request, 2026-10-13).**
The author sent 14 scene paintings and 25 character sheets in two messages and said the manuscript
(revision 7) was context, and that the work belonged on the GitHub site, not in the manuscript. Case 2231
now has **43 Subjects and 14 Records**. New Subjects, in roster order: `the-kiyote-pair` (the Catalyst,
as an object), `tsuru`, `three-senior-priests`, `sukenori`, `deputy-minister-of-the-left`,
`bureau-clerk`, `kaneyoshi`, `kiyomaro`, `azuki`, `kinji`, `rider-from-the-north`,
`old-master-one-eye`, `new-left-minister`, `boy-sovereign-of-himuro`, `bertrans-sister`,
`ermengarda`, `smiths-son`, `weighers-widow`, `gaucelm`, `sicard`, `arnaut`, `aimeric-2231`, `ors`,
`count-raimon`, `basque-guard-of-rocafort`; the full roster order is in `build_site.py`. **Slug note:**
`aimeric` already belongs to Case 0000B's Duke of Vosmark, so the Baron of Castelmaur is
`aimeric-2231` (display name "Aimeric of Castelmaur"). Records, in story order:
the-cat-at-the-starting-line, was-my-thumb-right, the-warmed-cushion, the-sparrow-examiner,
the-night-before, dawn-at-mikusa, the-stranger-at-the-doorstone, the-weighing, solans-fire, the-barn,
the-stone-holds-a-man, the-bridge-at-the-lower-race, the-quarry-gate, the-eleven-sheets; their order and
captions are Claude's, from the paintings and the manuscript, not author-confirmed.

Judgment calls: (a) several new sheets are for people the manuscript hardly describes (the Deputy
Minister of the Left, the Bureau Clerk, Kinji, the Rider, the Basque Guard, Bertran's Sister, the
Weigher's Widow, the Three Senior Priests). Those bios stay inside the manuscript's own sentences, say
when it is silent, and give ages as "by his/her sheet" in the epithets; where the manuscript states an
age (Kiyomaro 9, Tsuru 6, Aimeric 50, Arnaut 45, Bertran 38 and so on) it is plain. (b) The Old Master is
"a one-eyed veteran", "his old master" and "old One-Eye" in the text, never stated to be one man; the
sheet takes them as one and the entry says so. (c) The manuscript puts Sicard both at the head of the
men on the mill ladder and outside holding the horses; his entry reports both and does not reconcile
them. (d) The paintings differ from the text in places and the captions follow the text: the Mikusa
Stone is painted as an upright pillar, not the knee-high block of chapter 5, and fewer than the nine
witnesses are visible. (e) Higaide, Arikuni, Yasutsugu, Tamenaga, Narimune, Peire, Guiraut, Pons,
Lady Adalaïs and others still have no sheet and so no page; their names are plain text in the bios and
captions, never links. (f) The Kiyote Pair page describes the pair as the manuscript does (Interlude I
and the dust in Epilogue iii) and labels the colour notes as the sheet's. Images: sheets 980w / 320w
thumb, scenes long side 1000 with a 0.45x grid image, identified by looking at each sheet's title.
Checks run after rebuilding: 18,419 local links all resolve, no duplicate character or scene slugs,
sitemap 490 -> 529, key pages opened in Chromium with no broken images. Totals: characters 298 -> 323,
records 158 -> 172.

### Book: *The Tear of the Dragon* (Case 0247)

Status: **Coming soon** (awaiting release; no purchase link was supplied). Added on branch
`case-0247` (opened as a pull request, not pushed to `main`, so that another session working on the
repo is not disturbed), the cover-and-sheets pass and then the records, from: the cover
(`images/covers/0247.jpg`, tagline "Copied. Borrowed. Ledger. Unwilling. Hollow.", used verbatim as the
`hook`), 17 reference sheets, 11 record paintings, and the manuscript
`Case_0247_The_Tear_of_the_Dragon_2026-10-07_0411AM_GMT_7.md` (revision 5), which was used for the
bios, the two roster records and the record captions only and is **not committed** (the repo is
public). **`pages`, `genre` and `synopsis_html` are untouched `EDITOR_*` placeholders.** The case has
**11 records** (scenes), in story order, in the palette-knife painterly style of Books 4 and 5; their
order and captions are Claude's inference from the art and the manuscript, not author-confirmed.

The premise, from the manuscript (not author-confirmed jacket copy): the culture is Tang Chinese
(inferred from naming, not stated in-text), no religion is named, and the setting is Mount Qingxuan.
**Kuang Zhi**, 71, founder of the Hollow Pine Sect, climbs alone to the **Dragon's Tear**, a spring
that copies the complete memory and skill of the last person to touch its waters into the next person
who drinks, and deposits forty years of technique there with seven drops of blood and his whole face
under the water; he dies before dawn with **the Hollow Hermit** (the Envoy, a Custodian of
"Terrarium Designation Qingxuan") sitting three feet away. Eighty-nine hours later three shepherds,
Chen Wu, Fang and **Bai Rong**, drink at the screened southern grazing bank, and Bai Rong, drinking
last and longest, receives it. Kuang Zhi's heir **Shen Lie**, back from an errand two days south,
tracks him through **Old Cao**, who sells the same location to the Xuanwu Sect for a second fee. A
strand of Kuang Zhi's undyed hemp mourning cord, snapped from Shen Lie's wrist in the ambush, is read
by the Xuanwu searchers as proof of an assassin; **Xuanwu Kai**, whose only son died in the clearing,
invokes the founding oath's clause and declares war. The war lasts forty-one days and kills perhaps
sixty to avenge one. Bai Rong survives a second submersion and Shen Lie receives a compound deposit,
and rebuilds Hollow Pine on the same mountain. The chronicles call it the War of the Stolen Style.

**Connections.** Revision 5 of the manuscript names the Xuanwu Sect's founder as General **Kang Yi**,
last Grand Marshal of the Yan's northern garrisons, which is the existing `kang-yi` page of Case 4438;
Xuanwu Kai's bio links to it and `RELATED_THEMES` has a row linking 0247 to 4438. Its closing log files
it under Mythic Class "alongside Case 0000 for deposit-mechanism similarity", and its Catalyst's
`meta` is "Mythic Class", so the automatic same-class links relate it to 0000, 0157 and 0188. Don't
state more about the Yan than the manuscript and 4438 already say.

Seventeen characters have pages, in this order: `the-hollow-hermit` (the Envoy), `the-dragons-tear`
(the Catalyst), `kuang-zhi`, `shen-lie`, `bai-rong`, `xuanwu-kai`, `chen-wu`, `fang`, `widow-bai`,
`deputy-song`, `old-cao`, `xuanwu-kais-son`, `wei-bo`, `the-mourning-cord`, `chen-rui`, `old-fen`, `bo`.
Roster records: Catalyst **The Dragon's Tear** ("Mythic Class", page `the-dragons-tear`; it has a
sheet, so unlike 2231 it needed no cover crop), Envoy **The Hollow Hermit** ("Custodian, Terrarium
Designation Qingxuan", page `the-hollow-hermit`). The manuscript gives him no personal or archetype
number; don't invent one. The `PRINCIPALS` entry is `bai-rong`, `shen-lie`, `kuang-zhi`, `xuanwu-kai`,
`the-dragons-tear`, `the-hollow-hermit`, a first pass. **The home cast wall takes the first six
subjects in list order, not `PRINCIPALS`**, so those same six were put first in the list and the rest
follow in story order.

Judgment calls worth knowing: (1) Two sheets are things, not people: the Dragon's Tear (the Catalyst
as a character, as with the Sweets and the Golden Catacomb) and the Mourning Cord (a relic of its own).
(2) The heir has no name in the manuscript, so his slug is `xuanwu-kais-son`; `fang` and `bo` collided
with nothing (checked; slugs are one global namespace). (3) Ages: the manuscript gives Bai Rong 31, the
young master 22 and Bo "perhaps fourteen"; every other age comes from a sheet and is labelled "by his
sheet" in the epithet (Kuang Zhi's sheet says 71, and the manuscript only says he reached his
conclusion "somewhere in his sixty-eighth year"). (4) The Dragon's Tear's sheet shows the water
unnaturally cold for Kuang Zhi and unnaturally warm for Bai Rong; the manuscript says only that the
second time it was not as cold as water at that altitude had any right to be, so the bio labels the
colder/warmer detail as the sheet's. The Hollow Hermit's and Shen Lie's sheets say outright that their
appearance is invented. (5) **The Xuanwu Kai's Son sheet has a garbled second "Physical Traits" block
(nonsense text)**; the bio uses only the manuscript and the sheet's first block. Replace the sheet if a
clean one arrives. (6) **A manuscript inconsistency, not resolved in the bios:** Chapters Seven and
Nine have Widow Bai waiting with the herd in the hollow (frightened, half a mile off; later selling
cheese to a trader), while Chapter Twelve has her three valleys away buying salt on the morning of the
ambush and told by a note to wait at her sister's house. Her bio follows the Chapter Seven/Nine and
Epilogue version and leaves the salt and the note out. (7) No sheet exists for Deputy Song's junior,
Kuang Zhi's two seniors, the provincial governor or the retired soldier of the six hundred, so none
has a page; don't invent them. (8) Images: cover 900x1350 (from a 1717x2576 upload); sheets 980w with a
320w thumb, except the Mourning Cord (941w source, not upscaled). The order of the attachments matched
the order shown (checked at the two odd-sized sheets, the Mourning Cord and the Dragon's Tear), and
every sheet was confirmed from a contact sheet of its title strip before it was filed. (9) The bios
were written after reading the manuscript, then every word and number in them was checked against it by
script; what the script could not find is sheet-sourced appearance detail, labelled as such.

The 11 records, in story order: `not-the-first` (Ch. 1), `three-shepherds-at-the-southern-bank` (Ch. 2),
`shen-lie-finds-the-body` (Ch. 3), `bai-rong-at-the-gate` and `widow-bai-watches-his-hands` (Ch. 4),
`old-cao-counts-the-coins` (Ch. 5), `the-fire-in-the-hollow` (Ch. 6), `the-shepherds-reckoning` (Ch. 7),
`the-oath-is-invoked` (Ch. 8), `back-up-the-mountain` (Ch. 9), `the-second-emptying` (Ch. 10). Judgment
calls: (a) **`the-oath-is-invoked` is read as Xuanwu Kai** (the grey-robed students, blue banners and
the black and silver robe match his sheet and Chapter 8), but the painting gives him long white hair
where his sheet says black streaked with grey; it could be a different Grandmaster, so the author
should confirm. Its caption names no hair colour. (b) In `three-shepherds-at-the-southern-bank` the
caption does not say which of the two shepherds is Chen Wu and which is Fang. (c) The unnamed distant
figure with a staff in `shen-lie-finds-the-body` is not named in the caption. (d) Scene slugs share one
namespace across books (checked: none collide). (e) No record was added for Chapter 11 or 12 or the
epilogue; there is no painting for them.

### Book: *The Second Hand* (Case 1153)

Status: **Published** since 2026-10-14, when the author reported it live on Google Books and gave the link (`status` is `["published", "google-books"]` and `google_books_url` is `https://play.google.com/store/books/details?id=3IYZEgAAQBAJ`; Google blocks automated fetches, so the link has not been opened by an AI). **`pages` (77), `genre` (*Fiction / Fantasy / Epic*) and `synopsis_html` were filled in on 2026-10-17** (the author gave the first two and pasted the manuscript for the synopsis); they were `EDITOR_*` placeholders before that. It was added, while still coming-soon, on branch `case-1153`, as a pull
request rather than straight into `main`, from: the cover (`images/covers/1153.jpg`, tagline "Hand.
Debt. Doctrine. Mercy. Exile."), 20 character-dossier sheets (19 used), 13 scene paintings and the
manuscript `Case_1153_The_Eleven-Fingered_Mercy_2026-10-07_1737PM_GMT_7.md`. **`pages`, `genre` and
`synopsis_html` are untouched `EDITOR_*` placeholders.** The manuscript was read in full before the
bios were written, and used for the bios and the scene captions.

**Title discrepancy:** the cover says *The Second Hand*; the manuscript file and its heading say *The
Eleven-Fingered Mercy*. The site uses the cover's title, because that is what the author called it
("the cover of 1153 : The Second Hand"). Ask the author if the manuscript title is meant to replace it.

The premise, from the manuscript (not author-confirmed jacket copy): the kingdom of Sarkveti, whose
royal city is Tavgora, keeps the Threefold Crown. At a sanctioned ritual combat exercise, the Proving, a
re-buckled strap gives way and cuts the left hand of **Levan**, the king's son. **Observer 419**, posted
to Tavgora as a clockmaker, fits him over three nights with a grafted prosthetic left hand, **the
eleven-fingered hand** (two opposed thumbs and two folding rows of fingers). The Hierarch **Demna** rules,
on the old **Doctrine of the Unbroken Hand**, that a hand which hides its absence is no hand; the king
**Guram**'s nephew **Bagrat** cannot bear to owe his cousin an arm; a civil war follows, and **Otar** and
eleven former patients carry Levan out of the falling city to **Otsane**, a hidden Vigil-of-Ardwen
theocracy, where he lives as "Mikel". The Ardenwake thread (a pilgrim rumor reaching the cathedral where
the sword **Valeria** stands) is cited secondhand.

Nineteen characters have pages, in this order: `levan`, `bagrat`, `guram`, `vazha`, `demna`,
`observer-419-1153` (the Envoy), `the-eleven-fingered-hand` (the Catalyst), `the-doctrine-of-the-unbroken-hand`,
`sandro`, `otar`, `eka`, `sulqan`, `dato`, `gia`, `beso`, `amets`, `xu-lian`, `anchorite-of-ardenwake`,
`the-founding-wielder`. The `PRINCIPALS` entry is `levan`, `bagrat`, `vazha`, `demna`,
`observer-419-1153`, `the-eleven-fingered-hand` (a first pass; edit freely). Roster records: Catalyst
**The Eleven-Fingered Hand** ("Grafted prosthetic left hand", page `the-eleven-fingered-hand`), Envoy
**Observer 419** (`&ldquo;the clockmaker&rdquo; &middot; also the Envoy of Case 2140`, page `observer-419-1153`).
The catalyst `meta` is my wording, and the `hook` was the cover's tagline until 2026-10-16, when it was rewritten as a one-sentence line for Where to begin; the `meta` is
the thing the "same catalyst class" relation keys on, so it is unique on purpose.

Thirteen records, in this order: `the-proving-strap-gives`, `the-king-on-the-northern-wall`,
`the-clockmaker-at-his-stall`, `the-graft-over-three-nights`, `levan-counts-his-fingers`,
`demna-before-the-ruling`, `the-vashtir-snow`, `the-king-in-the-corridor`, `the-outer-wall-falls`,
`the-eastern-breach`, `the-keeper-meets-the-stranger`, `levan-at-the-workbench-in-otsane`,
`one-attempt-on-valeria`. Every painting was identified by viewing it; the captions come from the
manuscript. The last one names no one (the kneeling figure is unnamed in the painting and the
manuscript's ritual is only "the Empty Hand"), so its caption links only Valeria.

**Cross-links the author asked for.** Xu Lian is also in Case 0000B; the 0000B Anchorite bio now links his
page. The anchorite on the sheet is the main protagonist of 0000B, and `anchorite-of-ardenwake` is a
separate page here (cited secondhand, with the sheet's "adds no new physical detail" respected) that links
back to `the-anchorite`. `the-founding-wielder` is the boy of Case 0000 and links to `the-boy`, whose bio
links forward. Observer 419 is the same agent as Case 2140's, so **`observer-419-1153` is a second page**,
not a reuse of `observer-419` (character slugs are one global namespace, and each page belongs to one
case); the two bios link to each other, the Cultivator lore text allows the one exception to "no two are
the same person", and a `RELATED_THEMES` row relates 1153 to 2140, to 0000B and to 0000.

Judgment calls worth knowing: (1) **Levan has two sheets**; the one used is the second one sent
(sheet B); the other is unused. (2) **Vazha's sheet gives an age that cannot be squared with the manuscript**
(he outlives the war by nearly thirty years), so no age is stated and the bio says so. (3) **Bagrat's sheet
footnote says he reigns twenty-seven years; the manuscript (revision 4, the latest) says twenty-six
everywhere**, so the site says 26. (4) Details that come from the *sheets* and not the manuscript are
labelled as such in the bios ("The sheet draws him…"); Eka's and Beso's looks are said, on the
sheets themselves, to be invented or reconstructed. (5) The Doctrine of the Unbroken Hand and the Hand have sheets, so both are
character pages rather than lore. (6) The manuscript gives Observer 419's watching as both seventeen and eighteen years;
the bios use eighteen, matching Levan's eighteen years and the night the city falls. (7) 1153 shares the Threefold Crown and the
Faith of Ardwen, so the faith relations pick up 0157, 4417, 2140 and 2231 (Crown) and 0000,
0157 and 0156 (Ardwen) automatically; the two `appears_html` paragraphs name the case. (8) **Lesson, repeated from 2231:** the
scene images were first written under working names that did not match the slugs in the data, which the
link check caught; rename the files or the data before the check, never after. (9) A record's
Subject line comes from the characters its caption links, so *The Outer Wall Falls* lists Bagrat and Vazha
although neither is in the picture (it shows the burning city and the siege engines); it was left that way
because the record is about their act, and an empty `"subjects"` list falls back to the caption links.
(10) Images: cover 900x1350; sheets 980w / 320w thumb; scenes 1000px long edge / 450px grid; maps as
supplied (1024x1536, 575 KB) plus a 450w thumb, the same specs as every other book. Originals were not
committed.

### Book: *Independent Observation* (Case 1268)

Status: **Coming soon** (awaiting release; no purchase link). Added on branch `case-1268`, as a pull request
rather than straight into `main`, from: the cover (`images/covers/1268.jpg`, tagline "Altitude. Round. Audit.
Dormant. Unhastening.", used verbatim as the `hook`), 11 character sheets and the manuscript
`Case_1268_The_Eleventh_Astral_Dream_2026-10-01_0518AM_GMT_7.md` (revision 1), which was used for the bios only
and is **not committed** (the repo is public). **`pages`, `genre` and `synopsis_html` are untouched `EDITOR_*`
placeholders.** No scene paintings came with it at first; 15 were added later (see "Records added to Case 1268"
below).

**Title discrepancy** (the same shape as 1153): the cover says *Independent Observation*, which is also what the
author called it ("Case 1268 : Independent Observation") and is the manuscript's Chapter III heading; the manuscript
file and its heading say *The Eleventh Astral Dream*. The site uses the cover's title. Ask the author if the
manuscript title is meant to appear anywhere.

The premise, from the manuscript (not author-confirmed jacket copy): **Aldemark**, a Frankish-rooted theocracy "circa
the turn of the ninth century", is governed by the Threefold Crown, whose three Triarchs are **Ansovald** (Auron's
seat), **Adaltrude** (Elara's) and **Sigward** (Solan's). A network of dormant probes seeded generations earlier
begins, on a schedule fixed before the seeding, to give the sleeping people of one village at a time an unmediated
vantage above their world: eleven days of visitation, eleven months of silence. Halstead is first (**Ymma** dreams
first; the farmhand **Otker** reports the world is round and will not recant), and Warden **Hraban**, sent from
Ansdorf, asks for guidance before he asks for punishment. The Crown purges Halstead (forty-one dead), and nine
villages in all burn or purge themselves, while one unaffiliated Ardwenist **Anchorite** is present at every
burning. Aschendale's elders decline the tithe, which turns the dreaming into an audit of the Crown; the eleventh
selection falls on the capital, Dornhal, and on the Triarchs themselves, who split three ways. The Crown survives as a
faith rather than a government, Elara's seat absorbs the temple's civil authority, Hraban breaks, resigns and lives
thirteen more years, and the Anchorite, who had asked the sky to let her come and reached a dormant presence that
answers to the Sky-Answerer and the Unhastening, goes back to the road. The Custodian log counts 1,211 dead.

Eleven characters have pages, in this order: `hraban`, `anchorite-of-ardwen`, `otker`, `adaltrude`, `ansovald`,
`sigward` (the six principals), then `ymma`, `the-probe-network` (the Catalyst), `cultivator-observer`, `solan`,
`elara`. The `PRINCIPALS` entry is those first six, a first pass; **the home cast wall takes the first six
subjects in list order, so they are first in the list too.** Roster records: Catalyst **The Probe Network**
(`meta` "Distributed autonomous celestial probe network", unique on purpose so no automatic same-class link is
invented), Envoy **Cultivator Observer** (see judgment call 1).

Judgment calls worth knowing: (1) **No Envoy, but an Observer sheet.** The manuscript header says "None assigned
&mdash; autonomous network; no Envoy delivers or observes in person", yet one sheet is titled "Cultivator Observer /
Observer / Case 1268 / Custodian-Office Analytical Authority". The `envoy` roster record is that sheet, labelled "no
Envoy posted in person", so the case still appears in the Cultivator roster; the Cultivator lore now says "Nearly every
case has its own" and gained one sentence. The sheet gives no gender and the bio uses no pronoun. If the author wants
the case to have no Envoy at all, delete the `envoy` dict and the page. (2) **The Case 0000 link is an inference.** The
dormant presence in the Anchorite's ascent answers to "the Sky-Answerer, the Unhastening"; the Archival Log speaks of a
designation filed under "a name that had once belonged to a sword", of a valley watched through "one boy's natural
life" and of at least six earlier sealed case files. That matches Case 0000's Ardwen (Observer 000), the sword Valeria
and the boy, but the manuscript never names Case 0000. The Anchorite's bio says the echoes "point toward" Ardwen and
links the `ardwen` page, and a `RELATED_THEMES` row relates 1268 to 0000; the Ardwen page itself was **not** edited.
Ask the author before saying more. (3) **Sheet pull-quotes that are not in the manuscript:** Hraban, Adaltrude, Sigward
and the Cultivator Observer each carry one, and each bio says so. Otker's, Ansovald's and the Anchorite's quotes are the
manuscript's. (4) **Adaltrude's vestment colours disagree with Elara's sheet.** Her sheet says "Elara's traditional
colors" and draws blue and ivory ("Elara blue" in its palette); the Elara sheet is deep red and cream (and Solan's flame
red and white). Both are given as drawn; the author should say which is right. (5) **Sigward's age:** the manuscript
calls him "a young man defending an old institution"; his sheet's trait list says middle-aged to older adult, while its
caption says "a younger man in the service of an old institution". Left as it stands. (6) **Years:** Adaltrude is
twenty-six years in office at the Aschendale vote and twenty-eight at the eleventh dream (read as two moments);
Ansovald's nineteen years governing the defense and twenty-eight of clerical career match his sheet; Hraban is
seventeen years by his file and twenty-six by the Custodian log, which says the file was never revised. (7) **Solan and
Elara are temple iconography**, their sheets say so and their bios say the gods take no part in the events. **There is
no Auron sheet, so no Auron page; don't invent one.** (8) **Ymma's fate is not in the manuscript**, so her bio does not
say. **The Anchorite is never named**, and the manuscript gives no name to the junior Warden, the Inquisitor, the
Tallyman, the woman of Ansdorf who told no one, the spearman at Reinfeld or the blacksmith of Faldrun; none has a sheet,
so none has a page. (9) **Counts:** the manuscript says "nine burnings" although ten villages were selected (Aschendale
was never purged; Wulfsholt and Stonewick purged themselves); the bios say "nine burnings" as it does. The log counts
1,104 dead across ten selections and 1,211 after the eleventh (107 more from riot, reprisal and clergy who could not bear
what they had seen); Halstead is 41. (10) Images: cover 900x1350 (from a 1717x2576 upload); sheets 980w with a 320w thumb;
every sheet was identified from a contact sheet of its title strip before it was filed (the upload order was not the
display order). Originals were not committed. (11) The bios were written after reading the manuscript in full, then every
number and quoted phrase in them was checked against it by script; what the script could not find is sheet-sourced
detail (labelled as such), "Case 0000", and one spoken line the manuscript splits in two.

**Records added to Case 1268 (15).** The author sent 15 paintings in one batch ("case 1268 update records"),
unnamed and unordered. Each was identified by looking at it against the subject sheets and the bios already on the
site (nothing was read from the manuscript, which is not in the repo), then filed in the order the bios tell the
story: `ymma-wakes-before-dawn`, `a-dreamer-drifts-toward-the-moon`, `the-world-seen-from-the-moon`,
`hraban-questions-otker`, `a-village-after-the-purge`, `the-anchorite-kneels-in-halstead`,
`the-singing-at-grenmoor`, `the-iron-globe-at-faldrun`, `the-boundary-stone-at-aschendale`,
`the-anchorite-is-taken-at-reinfeld`, `the-anchorite-asks-to-come`, `the-anchorite-rises-above-aldemark`,
`the-dormant-figure`, `the-eleventh-dream-over-dornhal`, `hraban-finds-the-anchorite`. Each has a short `"title"`
(§3) and a one- to three-sentence caption written only from what the bios say and what the painting shows.
Judgment calls: (1) **Three records name no subject on purpose.** The two moon paintings (a barefoot dreamer
drifting toward the moon; a young man on it looking back at the world) could be Ymma, Otker or neither (Ymma's own
sheet shows her floating toward a full moon), and the burned village with one man under a torn banner could be
Halstead or another village and Hraban or another man. Ask the author who they are. (2) **The three Triarchs in the
Dornhal painting are named by vestment colour:** the figures in black and gold, crimson and ivory, and pale blue
match Ansovald's, Sigward's and Adaltrude's sheets, so the caption links all three without saying which is which.
(3) **Settings come from the bios, not from the art alone:** the shrine of fieldstone and unbleached cloth is
Grenmoor's (the Star-Walkers), the iron globe is Faldrun's, the stone with the sunburst is Aschendale's boundary
stone, the arrest is Reinfeld's, the grey-coated man at the crossroads shrine is Hraban after his resignation and the
two hollows in the ash are the Anchorite's knees in Halstead. If the author says a painting shows something else,
change its caption. (4) The tall pale figure with black hair and red eyes is drawn as the bios describe the dormant
presence; the Case 0000 link is still not stated anywhere on the site. (5) Images: full image long edge 1000 px,
grid 450 px, as everywhere (178-259 KB each); originals were not committed. (6) Records 172 -> 187.

### Book: *Fossa* (Case 0202)

Status: **Coming soon** (awaiting release; no purchase link). Added on branch `case-0202-fossa`, as a pull request
rather than straight into `main`, from: the cover (`images/covers/0202.jpg`, titled FOSSA, tagline "Swarm. Ditch.
Signature. Tithe. Miracle.", used verbatim as the `hook`), 27 character sheets (17 in the author's "first batch", then
10 more), 10 scene paintings, the manuscript `Case_0202_The_Sun-Turned_Harvest_2026-10-08_1035AM_GMT_7.md`
(revision 4) and a publication package (`The_Sun-Turned_Harvest_publication.MD`). The manuscript and the package were
used for the bios and records only and are **not committed** (the repo is public). **`pages`, `genre` and
`synopsis_html` are untouched `EDITOR_*` placeholders.** The package contains a drafted synopsis and genre
suggestion, which can be adopted on request. The author called the upload "first batch of the char", so **more
characters are expected**.

**Title discrepancy** (the same shape as 1153 and 1268): the author, the cover and one of the package's title options
say *Fossa*; the manuscript file and the package's working title say *The Sun-Turned Harvest*. The site uses *Fossa*.
Ask the author if the working title is meant to appear anywhere.

The premise, from the manuscript (not author-confirmed jacket copy): **Auvarre**, a small Occitan-flavoured Frankish
kingdom of the Lauze valley, in the barony of Castelmaur (the village of **Vilarnau**, the Mill of the Two Weirs, the
Throat gorge and its Dawn Wall). On the eleventh of Garren the Cultivator Envoy **Observer 551**, in the guise of the
rat-catcher Ratièr, breaks one clay bait-pot of **Strain H-202** in the roosting scrub ahead of a migrating swarm of
red grasshoppers. The infected swarm turns to the sun at first light and dies on the east-facing cliff with a
thirty-three-band collar (1, 1, 2, 3, 5, 8, 13), and the dead are edible. The stranger of Case 2231, **Tomobe no
Higaide**, who has been displaced onto the Stone at Vilarnau, says one word on the green (`fossa`, which in the dialect
means a long trench, a grave and a plague-pit) and heads the digging of the three ranks of trench in the Narrow of the
Throat that hold the swarm. The three altars (Hierarch **Odilo** of the Threefold Crown, the Provost of the Last Order,
Decree of Luminescence, here **Ottavio Brandi**, and the Keeper **Alazaïs** of the Faith of Ardwen) then claim the harvest
under **the Accord of Montclar**, the charter of the Right of First Naming; the Keeper says she does not know. After
the duel at the Edge on the third of Iverin (**Bertran** loses it for the Threefold), Odilo declares the Accord void
on the fifth of Iverin and is believed by eleven of the realm's seventeen barons; the Last Order calls the crown's
loan; King Ramon III signs, on the ninth of Lorren in the third winter, an instrument that divides Auvarre into two
countries, the Lit Reach and the Baronies. It is called the War of the Tithe and lasts thirty-three months. Vilarnau
is burned, a stone is left standing in the ashes, and the histories call the whole thing "the gift of the three crowns"
with no ditch and no stranger in it. Higaide's own end is **not** in this case: the manuscript says he returns "after
Cases 0202, 1414, 0333 and 0456" (see the 2231 write-up).

Twenty-seven pages, in this order: `observer-551` (the Envoy), `strain-h-202` (the Catalyst), `the-accord-of-montclar`,
`king-ramon-iii`, `pons`, `ibrahim-ibn-nasr`, `ottavio-brandi`, `matteo`, `alazais`, `joan`, `paciencia`,
`bertran-0202`, `baron-of-saint-aventin`, `the-provosts-daughter`, `the-provosts-sister`, `smith-of-vilarnau`,
`smiths-wife`, `arnal`, `bernat-the-younger`, `bernat-the-youngers-wife`, `sergeant-of-the-levy`,
`corporal-of-the-order`, `goose`, `elis-mother`, `vara`, `genzo`, `yo-su`. The `PRINCIPALS` entry is
`alazais`, `ottavio-brandi`, `bertran-0202`, `king-ramon-iii`, `strain-h-202`, `observer-551` (a first pass; the rest
sit behind "21 additional subjects documented"). Roster records: Catalyst **Strain H-202**, Envoy **Observer 551**.
Ten records, in manuscript order: `the-news-from-the-south`, `the-stone-at-mikusa`, `the-bowl-on-the-green`,
`the-lesson-at-the-mill`, `what-the-tavern-knew`, `the-fire-in-the-ditch`, `the-dawn-wall`, `the-long-graves`,
`the-cairn-on-the-ridge`, `the-hermit-of-val-muta`. Each carries a short `"title"` (§3) and a caption of 41-53 words
(the site median is about 32; the long captions the first draft had were cut). The old woman with the wooden spoon
appears only in `the-bowl-on-the-green`. The cover also has a square link-preview image,
`images/share/cover-0202.jpg`, made with `tools/make_share_images.py`.

**Characters shared with Case 2231** (the author said some appear in both). Where a person is the same man in both
cases but the two manuscripts do not agree, he has a **separate, cross-linked page**, as with `aimeric-2231`:
`bertran-0202` sits beside 2231's `bertran`. Others who appear in both (Arnaut, Brunissen, Gaucelm, Gersenda,
Kaneyoshi, the Kiyote pair, the villagers of Vilarnau, Observer 618) already had pages and are linked from the
0202 pages rather than duplicated. A `RELATED_THEMES` row relates 0202 with 2231. Reciprocal sentences were added to
2231's `bertran`, `observer-618`, `villagers-of-vilarnau`, `the-kiyote-pair` and `kaneyoshi` pages, and to the
Cultivator, Catalyst, Faith of Ardwen, Threefold Crown and Decree of Luminescence lore (each carries a link to
`books/0202.html`, which is also what puts 0202 in that faith's "Appears in" list and related cases).

Judgment calls worth knowing: (1) **Bertran's age is not reconciled.** 0202 says he is 41, 2231 says 38; both pages say
so. (2) **Kaneyoshi's stay in the smith's loft** is 11 days in 0202 and 3 days in 2231; both pages say the files are
not reconciled. (3) **The Stone's last use is told two ways.** In 0202 Vara kneels at it; in 2231 the Custodian
reduces the western stone to dust. The Kiyote-pair page now says the two files tell its end differently; nothing was
harmonised. (4) **Vara's hair:** the sheet draws white-silver; the publication package's notes say dark brown.
The page follows the sheet and says so; the author should say which is right. (5) **Sheet-only detail** (pull-quotes,
ages, palettes) is labelled "the sheet's ... are its own" in the bios; the Baron of Saint-Aventin's quotation "No
creditor in grey shall take our grain" is the sheet's gloss, not the manuscript's. (6) **No sheet, no page.** The
manuscript has Elis, Elis's great-grandmother, Peire, Lo Rog, the old woman with the wooden spoon (she is in the
`the-bowl-on-the-green` record only), the Sergeant Who Lost His Truncheon, Gersenda's family and more; none came
with a sheet, so none has a page and none appears as a link. **Don't invent pages for them**; they appear as plain
text where a bio needs them. (7) **Odd-shaped sheets:** Matteo's and Elis's Mother's sheets are not 2:3; they were
resized with the others and load, but check how their roster tiles crop if anyone complains. (8) **Scene order** is
manuscript order, not the upload order. (9) **Numbers:** the seventeen barons, the eleven who believe the
Accord void and the date of the fifth of Iverin are the manuscript's; Ottavio's "Arnaut's compromise paper" is the
paper on unsealing barns, not a partition paper. (10) Images: cover 900x1350; 27 sheets 980w with a 320w thumb;
10 scenes at 1000px long edge with a `-grid.jpg`; all progressive JPEG; each sheet and painting was identified from
a contact sheet before it was filed (the upload order was not the display order). Originals were not committed.
(11) The bios were written after reading the manuscript in full; every number and quoted phrase was then checked
against it by script, and the wording the check flagged (the corporal, the goose, Genzo, the Baron, the sister,
Bernat's wife) was cut back to what the manuscript supports.

### Book: *The Uncounted Dinar* (Case 3001)

Status: **Coming soon** (awaiting release; no purchase link). Added on branch `case-3001`, as a pull request rather
than straight into `main`, from: the cover (`images/covers/3001.jpg`, tagline "Rice. Grievance. Ledger.
Stillness. Vindication.", used verbatim as the `hook`), 13 character sheets and the manuscript
`Case_3001_The_Uncounted_Dinar_2026-10-14_1712PM_GMT_7.md` (revision 6), which was used for the bios only and is
**not committed** (the repo is public). **`pages`, `genre` and `synopsis_html` are untouched `EDITOR_*`
placeholders.** No scene paintings came with it, so `"scenes"` is empty. The cover and the manuscript agree on the
title.

The premise, from the manuscript (not author-confirmed jacket copy): a Cultivator Envoy, **Observer 1140** ("the
Empty-Handed"), is fed a poor shepherd's last meal and leaves him a single gold dinar that returns to its most
recently and legitimately established owner the morning after it is spent. **Malik ibn Sabir** of the Banu
Kathir spends it, notches it, and gives it to **Amina bint Rashid** of the Banu Harith in the marriage akad (the
coin's rule: a witnessed akad transfers it; absent one, an owner's death gives it to whoever's hand next closes
around it). Amina leaves him, is murdered by the thief **Zaid**, and the Banu Harith under **Sulayman ibn
Ghanim**, her uncle, seize Malik, doubting the case but unable to be seen doing nothing. A war of some three
hundred lives follows; Zaid dies of excess in a river-city wine-house after confessing to **Nur**, who takes the
coin and, nearly two years later, passes it by akad to the scholar **Qasim al-Fahmi**. He sends the truth north,
melts the coin and scatters it in the dunes; Malik is released, and the archive files the war as the *Grazing
Rights Dispute of the Two Confederations*. Culture per the manuscript header: Central Arabian Bedouin
confederations (Banu Kathir, Banu Harith), plus Andalusi Arabs for the trader Ibrahim ibn Nasr; religion none
named, so no lore page was touched.

Thirteen characters have pages, in this order: `malik-ibn-sabir`, `amina-bint-rashid`, `sulayman-ibn-ghanim`,
`nur`, `qasim-al-fahmi`, `the-dinar` (the six principals; the `PRINCIPALS` entry is those six, a first pass, and the
home cast wall takes the first six subjects in list order), then `observer-1140`, `hammad`, `maliks-cousin`,
`the-smith-of-the-dunes`, `the-sentry-of-banu-kathir`, `the-witnessed-akad`, `the-provincial-archive-clerk`.
Roster records: Catalyst **The Dinar** (`meta` "High-Concept, Cultural and Social", which is the manuscript
header's class and is also Case 3115's, so the two cases relate automatically as "same catalyst class"), Envoy
**Observer 1140**.

Judgment calls worth knowing: (1) **The cover's tagline reads "RICE."** The manuscript never uses the word, and
"price" occurs eight times in it, so this is probably a typo for "Price" on the cover. The `hook` follows the cover
verbatim, as for every other case; ask the author whether to fix the cover or the hook. (2) **Owner counts.** The
Nur sheet calls her the dinar's "third legitimate owner" and the Qasim sheet calls him "Fourth Owner". The
manuscript has five holders in five transfers (Malik, Amina, Zaid, Nur, Qasim) and says Zaid became "exactly as
legitimate an owner as a shepherd's bride", so the bios say fourth and fifth and quote the sheet labels. Ask the
author if the sheets are meant to stand. (3) **Sulayman's private visit.** His sheet (one panel and one line of
text) puts it with "a Banu Kathir family his raiders had wronged"; the manuscript's family is a Banu Harith family
whose stored grain the Banu Kathir burned. The bio follows the manuscript and says so. (4) **Qasim's scar.** The
manuscript says he scored the coin's *face*; the Dinar sheet draws a testing scar on the rim beside Malik's notch.
The Dinar's bio says so. (5) **The Smith.** The manuscript says Qasim melted the coin "in a smith's forge he paid
for" and does not say who worked the metal; the sheet shows the smith melting it over three labelled days, in a
palm-ringed town, and gives him an age of about forty. Those are the sheet's and the bio says so. His trait list
says "dark incurious eyes" while an expression panel reads "Curiosity (Suppressed)", so the bio says only "dark
eyes". (6) **Malik's flock.** The sheet draws a large flock of sheep behind him; the manuscript gives him four
goats, later six. His bio notes it. (7) **Pull-quotes.** Amina's is the manuscript's narration of her, not a line
she speaks (her bio says so); the first sentence of Hammad's is the manuscript's and the rest is the sheet's;
the Sentry's is the sheet's own; Observer 1140's and the Akad's are the manuscript's. Observer 1140's quote is
one line the manuscript splits around "the stranger said". (8) **The Witnessed Akad is an institution, not a
person.** It is filed as a Subject, the way the Golden Catacomb and the Nine Threads are, because its sheet
came with the cast; it could instead be an Archive entry. Ask the author. (9) **No sheet, so no page, so don't
invent one:** Zaid (the murderer, who is named in the bios in plain text without a link), the garrison captain,
the boy Salim, the Banu Harith rider the Sentry kills, the caravan's chief factor. (10) **Case 0202 and Ibrahim
ibn Nasr.** The trader reappears thirty-four years later in Case 0202 (*Fossa*, Observer 551), which landed on
`main` while this branch was open and already has an `ibrahim-ibn-nasr` page. Amina's bio links that page;
Observer 1140's closing bio links Ibrahim, `books/0202.html` and `characters/observer-551.html`; and a
`RELATED_THEMES` row ("Same trader: Ibrahim ibn Nasr ...") ties 3001 to 0202. `books/3001.html` shows both 3115
(same catalyst class) and 0202 as related cases. `books/0202.html` does **not** show 3001, because
`related_cases()` caps at six and ranks by number of reasons, so a one-reason match sits behind 0202's
two-reason cards; that is the existing six-card cap, not a bug, and the site logic was left alone. **Age
mismatch to raise with the author:** the 0202 sheet gives Ibrahim as 38, but the 3001 manuscript has him
twenty-one in his first season and riding north thirty-four years later (about 55). Neither page was edited. (11) **Ages are the sheets'** (Sulayman 58-62, Hammad
57-60, Malik early-to-mid twenties, Amina 23, Nur late twenties, Qasim 27-29, the Sentry 15-17, the Cousin
mid-to-late twenties, the Smith about forty, the Clerk 35-45); the manuscript gives only Amina's twenty-two, "nineteen
years" for Sulayman and "half his age" for the Sentry. The Cousin's gender is the sheet's too. (12) Dates: Amina
is murdered on the twenty-sixth of Deyren and Zaid dies on the nineteenth of Havren, as in the manuscript's
thirteen-month calendar. (13) Images: cover 900x1350 (from a 1717x2576 upload); sheets 980w with a 320w thumb
(Hammad's is shorter, 980x1170); every sheet was identified from a contact sheet of its title strip before it was
filed (the upload order was not the display order). Originals were not committed. (14) The bios were written
after reading the manuscript in full, then every italicised or quoted phrase in them was checked against it by
script; what the script could not find is sheet-sourced and labelled as such.

### Book: *The Sable Skin* (Case 4181)

Status: **Coming soon** (awaiting release; no purchase link). Added on branch `case-4181-sable-skin`, as a pull
request rather than straight into `main`, from: the cover (`images/covers/4181.jpg`, tagline "Oath. Dust. Doorless.
Uncounted. Mare.", used verbatim as the `hook`), 17 character sheets, one map (the Gazetteer) and the manuscript
`Case_4181_The_Sable_Skin_2026-10-13_1415PM_GMT_7.md`, which was used for the bios only and is **not committed**
(the repo is public). The author's brief was "add 4181 / gazetteer / the main character are higaide from 2231 so
make sure to link him to 4181 and vice versa / 17 characters dossier attached / and last a cover". **`pages`,
`genre` and `synopsis_html` are untouched `EDITOR_*` placeholders.** The first drop had no scene paintings; 15 came
later and are now `"scenes"` (see "Subjects and records added to Case 4181 (37 + 15)" below). The cover and the
manuscript agree on the title.

The premise, from the manuscript (not author-confirmed jacket copy): an Observer, **614** ("the Black-Salt
Peddler"), sells a journeyman smith in the Low Market of Marnholt, capital of the kingdom of Austrenne, a linen sack
of black powder (2.16 kg, 144 horn-scoop measures, "black salt") for his last nine pennies. **Ansbert** of the Low
Forge, his wife Hiltrude and his apprentice Lantfrid find that a scoop in the crucible makes a sword that does not
break under the Hammer-Oath Guild's Third Stroke; the Guild dies, the Duke of Tarnwald's steward **Odilo** buys the
swords and, with the King's Chancellor **Ricbert**, the clerk Marl's count of them, King **Theudebald** dies leaving a succession written with an
ambiguous pronoun, and at the Ordeal two sound blades leave the Law with no verdict. The war ends on the Uncounted
Day, the one unwritten day of the year, when a mercenary company of eighty sits down in the road and the Duke dies
at the crown of the Nine Arches after a captain bars the great gate on a word it was never meant to carry.
**Tomobe no Higaide**, the survivor of Case 2231 (a sword-captain of Himuro who touched the Stone and came out at
Vilarnau), walks into the case as an "uncontrolled variable" (the Observer's own words) and ends entered on the
Order's roll twice, as "Higa" and "idem". Religion: the Threefold Crown. The manuscript header says World 812-G is
shared with Case 2,231 and is "the same world as Case 4,099, a different population".

The first drop gave seventeen characters pages, the six principals first and then the rest in story order: `ansbert`, `wolfram`,
`brun`, `wido`, `sigebert-marl`, `theudebald`, `rich-merchants-son`, `carters-wife`, `old-sot-by-the-fire`,
`ruodhard`, `waldradas-nephew`, `ricbert`, `nailer`, `boy-with-the-basin`, `the-dukes-pages`, `sexton`, `gerold`.
37 more were added later (54 in all, listed below). The `PRINCIPALS` entry is those first six, a first pass, and the
home cast wall takes the first six subjects in list order, so it still shows the same six; the other 48 sit under
"Additional Case Records".
**There is no `catalyst` or `envoy` record**, because neither the sack nor Observer 614 came with a sheet, so
neither the Cultivator nor the Catalyst roster lists 4181, and `catalyst`/`envoy` are simply omitted from the dict
(`_class_of` and the roster code use `.get`, so this is safe).

**How Higaide is linked, both ways.** He has no sheet and therefore no page, so the link is case-level and in
prose. (a) `RELATED_THEMES` row `("4181", "2231", "Same stranger: ...")`: each case page shows the other as a
Related Case with that reason. (b) The bios of `ansbert`, `brun`, `carters-wife`, `waldradas-nephew`, `wolfram` and
`wido` link him, in plain text, to `books/2231.html` (and Ansbert's links the Stone to
`characters/the-kiyote-pair.html`). (c) Two reciprocal sentences were added to 2231 bios: `observer-618` (Observer
614 files him as "the surviving subject of Case 2,231, closed in the previous season by a different Custodian") and
`the-kiyote-pair` (the Stone's end as he remembers it). (d) The Gazetteer's `appears_html` names both
`books/4181.html` and `books/2231.html`, so its card shows on both case pages; the map draws Castelmaur, Vilarnau
and Lasserra, which are 2231's places. (e) The Threefold Crown's `appears_html` gained a 4181 sentence that also
points back at 2231 (Rothari's "He was merely early"). **If the author later sends Higaide's sheet, give him a
page and link it from all of these.**

Judgment calls worth knowing: (1) **Who is the main character.** The author calls Higaide the main character; the
manuscript files him as an uncontrolled variable and builds the case around Ansbert's household. The pages follow
the author where they use a word ("protagonist" in the RELATED_THEMES row and the Gazetteer), and otherwise
describe what the manuscript shows. (2) **No sheet, so no page, so don't invent one:** Observer 614, the sack
(Catalyst) and Higaide in the first drop, and with them Hiltrude, Lantfrid, Gundobad Rotger the Guildmaster, Odilo
the steward, Duke Waldo, Adalgund, Rothari, Hagen Brandt, Theodard, Ragnulf, Berthar and the one-eyed Lombard, all of
whom have pages now (the 37 + 15 block below). Observer 614, the sack and Higaide still have none. (3) **Brun's age.** The sheet says "about 19 at the opening"; the manuscript has him walking the wheel
for about three years, six more after the war, then dying "in his twenty-sixth year", which does not add up. The
bio reports both. (4) **The copper penny.** Chapter 7 has Higaide give a copper penny to Waldrada's nephew for the
news of a sermon; chapters 14 and 16 have the same penny in Lantfrid's left sleeve and returned by Hiltrude "as the
coin he had once given a boy for the news of a sermon". Nothing says how it passed. The nephew's bio reports both.
(5) **The map against the manuscript.** The map prints Marnholt apart at the cliff top and the High Town, Middle
Town and Low Market as separate names; the manuscript makes Marnholt the whole city and the three its parts. The
mountains and glacier at the head of the map are not in the manuscript. A bridge with a gate-tower, a forge with
smoke and a hamlet with salt-pans are drawn without labels; the manuscript has a nine-arch bridge, the Low Forge and
the Salt Landing. The Gazetteer reports all this in its text and does not say the unlabelled drawings are those
places. (6) **Two sextons, one sheet.** The manuscript has a bell-loft sexton who tolls midnight and a "Hierarch's
sexton" in the almonry yard who feeds Brun oats; the sheet draws one man and captions him both ways. The page joins
them and says the manuscript does not. (7) **Two Odilos.** The steward of Tarnwald in this case shares a name with
the Hierarch Odilo of 2231 and 0202; Gerold's bio says they are different men and links the Hierarch. (8) **Ages
and looks are the sheets'** unless the manuscript gives them (Ansbert 41, Marl 35, Wolfram 33/34, Wido 23, Ricbert's
thirty years in practice, Theudebald 63/64, the two pages' 15, the basin boy's 11); each bio says which is which.
(9) **Theudebald's reign.** Chapter 1 has him ruling thirty-one years, chapter 12 and the sheet thirty-three. The bio
says so. (10) **Higaide's chronology follows 2231's** (three months at Vilarnau, nineteen years at Lasserra, the Stone
gone on the first morning of Averin); Case 0202 tells the end of the Stone differently and is already flagged as
unreconciled on the Kiyote Pair's page. 4181 was **not** tied to 0202 or to 4099 on the site, although the manuscript
says the same world as 4099; 4181 does share the Threefold Crown with 0202 and shows it as a Related Case there.
Ask the author whether to add either link. (11) **"Sisuka."** The manuscript's dawn-word is a woman's name, and 2231's
Shizuka is not connected to it anywhere; no page makes the connection. (12) **Pull-quotes** are all the manuscript's
own words (checked by script; three differ only in trailing punctuation: "I will think," "Feed the ox," and "I
thought of it three times,"), except where a bio says it is the sheet's. (13) **Principals** are a first pass, picked by how much of the
plot each carries; the author may want a different six. (14) Images: cover 900x1350; sheets and a
thumb for each of the 17 slugs; map `images/maps/sable-skin.jpg` with a 450w thumb; share images
`images/share/cover-4181.jpg` and `map-sable-skin.jpg`; every sheet was identified from its title strip before it
was filed (the upload order was not the display order). Originals were not committed. (15) The bios were written
after reading the manuscript in full, then every quoted or italicised phrase in them was checked against it by
script; what the script could not find is sheet-sourced and labelled as such.

**Subjects and records added to Case 4181 (37 + 15).** Branch `case-4181-more-subjects`, pull request. The author
sent, in three drops: 20 more character sheets ("additional character dossier for 4181 / add to repo"), 17 more
("second batch of character dossier for 4181 / continue"), and then 15 scene paintings with the publication-prep file
`The_Sable_Skin_publication.MD` ("this is the scene for 4181, and publication file for context / continue").
4181 goes from 17 subjects to 54 and from no records to 15; the site goes from 391 to 428 subjects and from 197 to
212 records. **Neither the manuscript nor the publication file was to hand for the bios**, which say so ("Written from
the sheet, from what the other Case 4181 pages already say, and from the character notes in the case's
publication-prep file; the manuscript itself was not to hand."), and state what is "the sheet's own". The
publication file (Part 2, a character bible with chapter-referenced Role notes; Part 3, the 15 image prompts) is
**not committed** (the repo is public), nor are the original images. `pages`, `genre` and `synopsis_html` are still
`EDITOR_*` placeholders; Part 4/5 of the publication file has material for them if the author wants it.

*Subjects.* Batch 1 (20): `hiltrude`, `gisalbert`, `journeyman-cooper`, `waldrada`, `girl-behind-the-bar`, `donkey`,
`abbess-of-the-vineyard-convent`, `the-mended-stirrup`, `sunnhild`, `one-eyed-lombard`, `ragnulf`, `berthar`,
`young-levy-archer`, `nurse-of-waldo`, `eschwin-aunt`, `carpenter`, `sacristan`, `rothari`, `theodard-of-lorrenne`,
`chlodio`. Batch 2 (17): `adalgund`, `waldo`, `gundobad-rotger`, `lantfrid`, `hagen-brandt`, `odilo-4181`, `aldemar`,
`ebbo-of-eschwin`, `peire`, `landings-priest`, `prior`, `berthars-two-sons`, `sentry-at-the-river-gate`,
`boy-with-the-cracked-knife`, `barge-hand`, `carter`, `drover-from-the-north`. All sit after `gerold` in the list.
Character slugs are one global namespace, so Odilo the steward of Tarnwald is `odilo-4181`, not `odilo` (the Hierarch of
2231 and 0202). Sheets are 980w with a 320w `-thumb`, progressive JPEG Q85, as before.

*Records.* 15, in chapter order, each with a `"title"` (sentence case, from Part 3 of the publication file), `alt` and a
`caption_html` that links the character pages: `the-black-salt-peddlers-trestle` (Ch. 2),
`one-hundred-and-forty-four-heaps` (2), `the-man-who-bowed-to-the-ox` (3), `the-broom-and-the-crucible` (4),
`the-third-stroke-in-the-proof-hall` (5), `prior-and-the-bow` (5), `what-the-taverns-called-it` (6),
`the-end-of-the-shingle` (7), `yoake-breaks` (8), `the-doorless-armory` (9), `the-bedchamber-with-no-door` (12),
`thirteen-strokes-at-the-altar-of-oaths` (13), `we-are-nobodys-and-we-are-sitting` (15), `the-nine-arches` (16),
`the-sable-skin-in-the-hall` (18). Images are `images/scenes/<slug>.jpg` (1000 px long edge) and `-grid.jpg` (450 px).
The uploads came in no particular order; each was matched to its prompt from a contact sheet before it was filed.
Where Higaide is in a scene he is linked to `books/2231.html`, because he has no page of his own.

*Cross-links.* About 45 edits across the 17 older 4181 bios (Ansbert's "no sheet in this batch" sentence now links
Hiltrude, Lantfrid and Gundobad; the Duke's Pages gained a Sacristan sentence; Waldrada's Nephew gained "The
apprentice's own sheet draws the penny at his left cuff."), and the `sable-skin` Gazetteer and `threefold-crown`
lore now link the drover, Waldrada, Theudebald, Adalgund, Peire and Rothari, and the Landing's Priest's verdict.
`RELATED_THEMES`, `CONNECTED_CASES` and `PRINCIPALS` were not touched.

*What the publication notes settled* (and the bios now say): Prior is a female goose; Yoake is Higaide's broken
sword; the thirteen strokes are the crossings of the Ordeal between Theodard and Ebbo; the carpenter takes the
bedchamber door; the Landing's Priest's verdict of "forsworn" is the one Rothari declares void.

*Still hedged on the pages, and why:* the Countess's steward is taken to be Aldemar; the sentry's "boy from the
forge" and the Young Levy Archer's running figure are not asserted to be Lantfrid; the old man in the Boy with the
Cracked Knife's sheet is presumably Gundobad, but the beard differs; the Sacristan's goose is presumably Prior;
Berthar's "steward" is presumably Odilo; the Lombard's ox is presumably Brun; Peire is taken to be the boy of 2231
grown (hedged). **Discrepancies to ask the author about:** the Eschwin Aunt's sheet draws the Countess as a fair young
woman in blue, against Adalgund's own sheet; Brun's age (already item 3); Rothari's bedding stair (his sheet draws it
going down, the notes put it up the almonry stair); the carter in the notes may be two carters merged.

*Still no sheet, so no page:* Higaide, Observer 614, the sack, and the Himuro and Vilarnau figures the publication
notes list (the Boy-Sovereign, the Child of Himuro, the Hired Witness, the Two Ministers, the Miller's Widow).

### Gazetteers (new Archive group, 2365 + 4555 and 4417)

The author sent two map images and asked for them to go "into something else", not into the subjects or
records: *Illumaria* (shared by Cases 2365 and 4555) and *The Iron Stiletto War — Gazetteer* (Case 4417).
They are two new `LORE` entries (`illumaria`, `iron-stiletto-war`) in a new `group: "Gazetteers"`, so
the Archive index shows them under their own heading, and the home page's Archive list names them. A
gazetteer entry carries two extra fields: **`map`** (`file`, the image slug under `images/maps/`, and
`alt`) and **`places`** (a list of `(name, note_html)` pairs). `lore_detail_body` hands any entry with a
`map` to **`gazetteer_body`**: the map (opens in the lightbox, group `maps`) beside "About the Map",
"Places" and "Appears In", then the usual "Cases Where This Appears". `lore_cases` still reads the case
slugs out of `appears_html`, so that paragraph must link `../books/<slug>.html`. A case page whose slug
appears there gets a **Gazetteer** card (`gazetteer_cards_html`, `#gazetteer`) between Records and the
purchase panel. CSS is the "Gazetteers" section at the end of `css/style.css`.

**The Case 2365 / 4555 link.** The author said they are the same kingdom, 2365 the founding of its
religion and 4555 many years after it. Recorded in four places: the Illumaria map page (which prints both
names, as the map does: *Vallombra / Illumaria*), a `RELATED_THEMES` row ("Same kingdom: Case 2365 is the
founding of its religion, Case 4555 is set many years after"), the Decree of Luminescence lore (which
points at the map), and the map's own "Appears In". Livia's epithet already read "Princess of Vallombra,
then Queen of Illumaria". The lore says "Three centuries on" while Observer 902's bio says "four centuries
of reports"; that disagreement was there already and has not been resolved.

**Place notes use only what the case files say.** Every note was written from the existing bios and
captions; a place the files never mention says "Marked on the map; no case file describes it yet" (Tanners'
Row, Furrow reserve, Round-bed, the Greywater, the Greywater crossing and the Stonewic Hills). Don't fill
those in from imagination; add a sentence when a manuscript names them. "Unknown Lands" is noted as such.
Two labels on the 4417 map are damaged and were left as printed (the eastern marches carries a doubled
"the"; the western "Lands" label is cropped by the margin); they are not mentioned on the site.

### Gazetteer of the Vessel of the Betrayed Host (Case 4420)

A third map, for Case 4420, is `LORE` entry `vessel-of-the-betrayed-host` (`group: "Gazetteers"`, image
`images/maps/vessel-of-the-betrayed-host.jpg` plus its `-thumb`), in the same shape as the other two, so the Archive
index, the home page's Archive list, the sitemap and a Gazetteer card on `books/4420.html` came with it.
**The map's printed banner still reads the old title, *The Thermal Vessel War*,** which Book 5 above says the author
renamed away from. The page title, slug, alt text and every other word of the site use *The Vessel of the Betrayed
Host*; the image was filed exactly as the author sent it. If the author wants the banner changed, replace
`images/maps/vessel-of-the-betrayed-host.jpg` (and the `-thumb`) under the same names and run
`python3 tools/make_share_images.py --force`. Printed on the map: Mount Skahr, House Skarth, Kettish, House Varga,
House Tolvin, the Broken Glacier, Cindale, Thornfield, Sumne, and the labels tundra, ice line, northern marches,
western march, southern marches and lowlands. Notes use only the case file: Mount Skahr (Observer 814, the
Dragon-Speaker, and Yvaine's climb), House Skarth, the Broken Glacier (Maros's hunt, and the existing record), Cindale
(the holdfast Yvaine spares), Sumne (Soren leaves it within the month), the tundra, the ice line (the black-fletched
arrow record) and the northern and southern marches (Maros's and Vane's countries). **Unfiled, and said so on the
page:** Kettish, House Varga, House Tolvin, Thornfield, the western march and the lowlands. The map does not label
Karhold Keep or Vane Keep, and the page says so rather than choosing a drawn castle for either; it does not say Sumne
is where Vane sits, only what the file says.

### Cast added to Case 0000B (*Sword of Valeria: The Empty Hand*)

Nineteen character reference sheets (`char.zip`) were added to the `0000b` stub. **No manuscript came with
them**, so `pages`, `genre` and `synopsis_html` are still `EDITOR_*`, there is no `catalyst`/`envoy`
record, and the bios use only what the sheets print. The sheets' setting: Ardenwake, a holy city besieged
eleven times; **Valeria** (the sword) is lifted at the eleventh siege by **the Anchorite** of the Vigil of
Ardwen after five centuries of failed attempts; the sheets' world includes Pax Aldrovana, the Corvane
Imperium, Rovain, Solvarre, Vosmark, Cassoria, Belnograd, Velmoro, the Sarnak Horde and the Tazenna
Reach. The inference that 0000B is the published form of the canon guide's *Pax Aldrovana* continuation
(see below) is now supported by the sheets themselves, which say &ldquo;Aldrovan (Pax Aldrovana)&rdquo; on
several of them.

In order: `the-anchorite`, `aveline`, `halvard`, `vasarion`, `aimeric`, `ganeth` (the six principals, and the
homepage wall), then `kest`, `massinen`, `berant`, `dorenzo`, `corse-0000b`, `wendrics-wife`, `wendrics-son`,
`yorbulan`, `branimir`, `coren`, `verrin`, `the-wounded-archer`, `the-vault-guard`. The principals are a first
pass, edit them freely. Judgment calls: (1) **`corse` was taken** by Case 0000's steward to King Wendric;
this sheet's Corse has the same office and the same king, so it is `corse-0000b` and links back to the
0000 page, but whether they are literally the same man is the author's call. (2) `wendric`, `valeria`
and `ardwen` are Case 0000 pages and are linked rather than duplicated; there is no 0000B sheet for Wendric
himself. (3) Verrin's and the Anchorite's sheets say outright that their appearance details are invented.
(4) The Anchorite's sheet names a second protagonist, **Xu Lian**, who had no page here. The author has since said the Anchorite is the main protagonist of 0000B; the bio now says so, and links Xu Lian's page, which was filed under Case 1153 (`xu-lian`). Xu Lian is **not** in the 0000B roster, since no 0000B sheet or manuscript describes him; add one when that material arrives. (5) Several
sheets show scenes (e.g. the Vault Guard's &ldquo;Witnessing&rdquo; panel) that the pages describe only by caption;
the bios deliberately stop where the sheets stop.

### Cover-only entries added with it: Case 0000B and Case 2114

Both are `coming-soon` stubs in the same shape as 3312 / 3887 / 4442: cover,
`case_tag`, a one-line `hook` taken from the cover's own tagline, and the
bare `EDITOR_*` placeholders for pages, genre and synopsis; no cast, scenes,
`catalyst` or `envoy` record (so neither appears in the lore rosters). They
sit at the end of `BOOKS`, in the order the author listed them.

- **`0000b` &mdash; *Sword of Valeria: The Empty Hand*** (Case 0000B). The slug is
  lowercase on purpose (GitHub Pages URLs are case-sensitive); the on-page tag
  reads &ldquo;Case 0000B.&rdquo; Cover tagline: &ldquo;Want. Reflex. Ledger. Exception.
  Unrecorded.&rdquo; It appears to be the published form of the canon guide's
  *Pax Aldrovana* continuation of Case 0000 (guide &sect;6.1) &mdash; an inference
  from the tagline and the title, not something the author has said.
- **`2114` &mdash; *A Fraction of an Inch*** (Case 2114). Cover tagline:
  &ldquo;Arithmetic. Regalia. Convergence. Warning. Still uncounted.&rdquo; Nothing else
  is known about it here, and the canon guide has no entry for Case 2114.

## 7. What's placeholder / incomplete right now

- Genres and page counts are settled for Books 1–4: 102 / 99 / 96 / 109
  pages, none carrying an unconfirmed-genre `editor-note` (chosen by
  Claude at the author's instruction). **Book 5 is the exception** — its
  `~123` pages and suggested genre were the SLAVE-4420 staging
  copy's own unconfirmed estimate, `editor-note` span and all; **resolved 2026-10-17**
  (130 pages, *Fiction / Fantasy / Epic*, given by the author).
- **0188 and 2140 are roster-only** (§6). Both are still `coming-soon`;
  0188's pages/genre are unconfirmed estimates, and 2140 has no synopsis,
  page count, or genre at all, no scene art (so its Scenes slider shows the
  "not yet added" placeholder), and no `catalyst` record. Wait for the
  author's confirmation before flipping either to `published`.
- The Iron Stiletto War's and The Vessel of the Betrayed Host's Google Books links
  both came in on their staging copies and haven't been opened by an AI
  (Google blocks automated fetches) — one click each confirms them.
- Every book now has a Scenes slider (8 / 19 / 19 / 11 / 17 images for
  Books 1–5), so the "not yet added" placeholder no longer shows on any
  page — it stays in the generator for any future book added without
  scene art. The
  Stolen Prince War's scenes are ordered chronologically by story event
  (discovery → founding-five deaths → the Widow → the Ember Judge →
  Vartaz's death → the war years → Nairi's Level 101 expedition), not by
  the order the art arrived in — if more scene art comes in later, slot it
  in by where the moment falls in the story, not just appended to the end.
- The chrome heels (Case 4417's Catalyst) have no character page — see §6,
  Book 4, for why and what to do if a proper portrait arrives.
- The lore entry formerly called Catalyst Tier is now **Catalyst** (see §6, "Lore
  rosters"). The full tier system is still not documented on the site.
- The Stolen Prince War's manuscript cast is fully illustrated (35
  characters — see §6). If a genuinely new named figure turns up in the
  manuscript later, add them the same way; don't invent one in the
  meantime.
- Doron's quote and "first blow" claim were corrected once Berel's and
  Tamir's own sheets arrived and confirmed those details belonged to them,
  not him — see §6 for what changed and why.
- Contact page is real: Royal Road (author profile 1068950), Instagram
  @killythirsk, Threads @killythirsk (`SOCIALS` in the script, also used by the
  footer). There is deliberately **no email** — don't add one.
- The four earlier placeholder-only books (Ghost, Aldemark, Illumaria,
  Carbon Echo Beacon) that existed at one point are still not on the site.
  "More than a dozen novels" total were mentioned early on — only eight are
  live, plus 0188, 2140 and 3115 with a roster but no synopsis yet (§6).
- **Case 4438** (*The Heavenly Thunder-Serpent*) is live with a full cast,
  scene gallery, both roster records, its Google Books link and a confirmed
  page count (82); the link hasn't been opened by an AI. **Case 2114** is a
  cover-only coming-soon stub, **Case 0000B** is coming-soon with a 19-character
  cast but no pages, genre, synopsis or catalyst/envoy record, and **Case 0156**
  (*The Purging of Charsianon*) is coming-soon with a 26-character cast, 14
  scenes and both roster records but no pages, genre or synopsis (§6).
- **Case 2365** (*The Decree of Luminescence*) is **published**: a 24-character
  cast, 15 scenes, both roster records, 88 pages and a Google Play Books link
  (not opened by an AI), merged via PR #1 and published on 2026-10-10. Its
  `synopsis_html` was drafted on 2026-10-12 (Claude, from the manuscript; not
  author-confirmed), its `genre` is still a placeholder, and its Catalyst has no
  sheet (§6).
- **Case 2231** (*The Stone of the Clean Hand*) is coming-soon with a
  43-character cast (the Catalyst has its own page, `the-kiyote-pair`), 14 records and both roster
  records, but no pages, genre or synopsis. Its principals Higaide, Arikuni, Yasutsugu and others
  still have no sheet (§6).
- **Case 0247** (*The Tear of the Dragon*) is coming-soon with a 17-character
  cast, 11 records and both roster records but no pages, genre or synopsis (§6). The
  Xuanwu Kai's Son sheet has a garbled second traits block, and the manuscript contradicts itself on
  where Widow Bai was during the ambush.
- **Case 1153** (*The Second Hand*) is **published** (the author reported it live
  on Google Books on 2026-10-14 and gave the link; not opened by an AI), with a
  19-character cast, 13 records and both roster records; page count, genre and synopsis
  were added 2026-10-17 (§3). The manuscript title
  differs from the cover title (*The Eleven-Fingered
  Mercy*). Vazha, Bagrat and the unnamed kneeling figure are flagged in §6.
  The people the manuscript names with a real part to play all
  have pages; groups such as the three court doctors, the eleven escorts and the Vashtir
  raiders do not, and shouldn't be invented one by one.
- **Case 4181** (*The Sable Skin*) is coming-soon with a 54-subject cast, 15 records and a gazetteer, but no catalyst
  or envoy record, page count, genre, synopsis or purchase link (§6). Higaide is the protagonist per the
  author but has no sheet, so no page: he is linked to and from Case 2231 at case level (§6). Observer 614, the
  sack and most of the named cast have no sheet either. The map's Marnholt differs from the manuscript's, Brun's
  sheet age does not fit the manuscript, and the copper penny is told two ways; all flagged in §6.
- **Case 3001** (*The Uncounted Dinar*) is coming-soon with a 13-character cast and both roster
  records, but no page count, genre, synopsis, records or purchase link (§6). The cover's tagline
  reads "Rice", probably a typo for "Price"; the sheets' owner counts for Nur and Qasim, Sulayman's
  private visit, Qasim's scar and the Akad's filing as a Subject are flagged in §6. Zaid has no
  sheet, so no page; Ibrahim ibn Nasr's page comes from Case 0202, and his age there (38) does not match
  3001 (about 55).
- **Case 1268** (*Independent Observation*) is coming-soon with an 11-character cast
  and both roster records and 15 records, but no page count, genre, synopsis or purchase link
  (§6). The manuscript title differs from the cover title (*The Eleventh Astral
  Dream*); the Cultivator Observer's place on the Envoys roster, the Case 0000
  echo, Adaltrude's vestment colours and Sigward's age are flagged in §6. There is
  no Auron sheet.
- **Case 0202** (*Fossa*) is coming-soon with a 27-character cast, both roster
  records and ten records (scene paintings), but no `pages`, `genre`, `synopsis_html`
  or purchase link (§6). The title on the manuscript differs from the cover (*The
  Sun-Turned Harvest*); more characters are expected from the author. Bertran's age,
  Kaneyoshi's days in the loft and the Stone's last use disagree with Case 2231 and
  are flagged on the pages and in §6; Vara's hair colour (sheet vs. package notes)
  is open.
- **Gazetteers** (`illumaria`, `iron-stiletto-war`, `vessel-of-the-betrayed-host`): six places on the first two maps
  and six on the 4420 map (Kettish, House Varga, House Tolvin, Thornfield, the western march, the lowlands) have no
  case-file text yet (§6); add notes as manuscripts name them. The 4420 map's banner still prints the old title (§6).
- **Case 3115** (*The Listening Water*) now has its full 24-character
  cast and fresh `catalyst`/`envoy` records (see the Book write-up above),
  but is still `coming-soon`: no confirmed `pages`, `genre`, or
  `synopsis_html`, and no scene art yet. Resolve the same way Books 1–4
  were once the author sends more.

## 8. Decisions already made — please don't relitigate these without cause

- **Book entries stack on phones.** At ≤ 36rem, `.entry--book` (books list and
  homepage) puts the cover above the title, tags and blurb, like a card, instead
  of cover-left/text-right. Character rows keep the side-by-side layout.
- **Images are deterred, not locked** — see §5. Full-size URLs stay in
  `data-full`. The author asked for images to be non-downloadable; the honest
  limit was explained to them.
- **Genres are Claude's call**, shown plainly with no "suggested" marker.
- **No email address anywhere on the site.**
- **Rosters** on lore/cultivator and lore/catalyst are generated from each
  book's `envoy` / `catalyst` record — see §6.
- **Homepage fullness:** a counts line, a cast wall (first six characters of
  each book) and a scene band (`HOME_SCENES`) were added because the site read
  as empty to a visitor; they draw only on existing images.
- **No login/CMS/upload feature.** Explicitly turned down as not
  achievable with any real security on a static site; GitHub repo access
  already *is* the access control. Agreed workflow: keep sending images
  through chat for someone with code execution to wire in.
- **Characters stay a vertical list; only Scenes slides horizontally**,
  and only for books that actually have scene art. This contrast was
  deliberate, discussed directly with the author.
- **Uploaded images are always resized/compressed before use**, never
  committed at original resolution (originals often run 3–6MB each; site
  copies run well under 1MB). Keep doing this for any new art.
- **Character portraits never get forced into a uniform crop** — see §3.
  This was a real bug found and fixed when the Ledger cast's more varied
  image proportions exposed a hardcoded ratio that had gone unnoticed with
  Valeria's more uniform set.
- **Always run `tools/build_site.py` from inside the `tools/` folder.**
  The script computes its own project root as two directories up from its
  own file location. Running a stray copy of the script from elsewhere
  (e.g. a copy left sitting one level up) silently writes output to the
  wrong place with no error — this happened once during development and
  had to be cleaned up. If output ever looks like it didn't update
  anything, check *where* the script actually wrote to before assuming the
  content itself is wrong.
- **Staging copies get merged into master, not swapped for it.** New books
  are built in a separate staging ("slave") copy of the site, named by case
  number (`0157.zip`, `4417.zip`), and then merged into `master.zip`. A
  staging copy is a fork of master from one moment in time, so it can come
  back *behind* master on everything else — the 0157 copy had no Ledger
  scenes or link, no Royal Road link and no clickable status tags; the 4417
  copy had no 0157 at all. Never overwrite master with one. Instead: take
  master as the base, splice in only the new book's dict (plus any lore
  text it changes), union the new image files (checking that no same-named
  file differs), regenerate, then diff the regenerated HTML against the
  previous master's — only the new pages and the pages the new book
  legitimately touches (`index.html`, `books.html`, the lore pages,
  cross-linked characters) should change.
- **Latest update (more subjects and records for Case 4181 — branch `case-4181-more-subjects`, pull request, 2026-10-21/22).**
  The author sent 20 and then 17 more character sheets for 4181, then 15 scene paintings and the case's
  publication-prep file ("this is the scene for 4181, and publication file for context / continue"). Done: 37 new
  `characters` and 15 `scenes` in the `4181` dict (after `gerold`; `PRINCIPALS`, `RELATED_THEMES`, `pages`, `genre`
  and `synopsis_html` untouched), about 45 cross-link edits in the 17 older bios, and links added in the `sable-skin`
  and `threefold-crown` lore. Images: 74 character files and 30 scene files. Recount after rebuilding: cases 24
  (unchanged), characters 391 -> 428, records 197 -> 212, sitemap 628 -> 680; every local link resolves (25,901
  checked), no duplicate character slugs, and the new and changed pages were opened in Chromium at desktop and phone
  width. Only files that really changed were committed; the footer-stamp-only pages were left alone. The publication
  file, the manuscript and the original images were not committed. **Open questions for the author** are in the
  "37 + 15" block in §6: the Eschwin Aunt's Countess, Brun's age, Rothari's stair, the two carters, and the still-hedged
  identifications.
- **Earlier update (Case 4181 added — branch `case-4181-sable-skin`, pull request, 2026-10-17/18).**
  The author sent the cover (`41810_5x.jpg`), the manuscript, one map and 17 character sheets, with "add 4181 /
  gazetter / the main character are higaide from 2231 so make sure to link him to 4181 and vice versa / 17
  characters dossier attached / and last a cover". Done: a full `4181` dict (17 `characters`, no `catalyst` or
  `envoy`, no scenes; `pages`, `genre` and `synopsis_html` left as the `EDITOR_*` placeholders), a `PRINCIPALS`
  entry, one `RELATED_THEMES` row (4181 with 2231, same stranger), a new `sable-skin` Gazetteer `LORE` entry, one
  sentence in the Threefold Crown lore, and two reciprocal sentences on 2231 bios (`observer-618`,
  `the-kiyote-pair`). Images: 1 cover, 34 character files, the map and its thumb, 2 share images. Recount after
  rebuilding: cases 23 -> 24, characters 374 -> 391, records 197 (unchanged), sitemap 609 -> 628; every local link
  resolves (22,086 checked), no duplicate character slugs, and the new and changed pages were opened in Chromium at
  desktop and phone width with no horizontal overflow. Only files that really changed were committed; the
  footer-stamp-only pages were left alone, as before. The manuscript and the original images were not committed.
  **Open questions for the author** are the numbered judgment calls in §6, first among them whether Higaide gets a
  sheet of his own, and the three that touch the manuscript (Brun's age, the copper penny, the map's Marnholt).
- **Earlier update (Case 3001 added — branch `case-3001`, pull request, 2026-10-15).**
  The author sent the cover (`30010_5x.jpg`), the manuscript (revision 6) and 13 character sheets, with "read
  repo, add 3001". Done: a full `3001` dict (13 `characters`, `catalyst` The Dinar, `envoy` Observer 1140, no
  scenes; `pages`, `genre` and `synopsis_html` left as the `EDITOR_*` placeholders), a `PRINCIPALS` entry and one `RELATED_THEMES` row (3001 with 0202, same
  trader); no
  lore text changed (the Cultivator and Catalyst rosters pick the case up automatically, and Case 3115 gains a
  Related Cases card because both share a catalyst class). Images: 1 cover, 26 character files, 1 share image.
  Recount after rebasing onto `main` (which now holds 0202) and rebuilding: cases 22 -> 23, characters 361 -> 374,
  records 197 (unchanged), sitemap 595 -> 609; every local link resolves (21,391 checked) and the new and changed pages were opened in Chromium at desktop
  and phone width with no broken images (the home page's 13px horizontal overflow at 390px wide is on `main`
  too and was not touched). Only files that really changed were committed (the script, the new pages and
  images, `books.html`, `books/3115.html`, `characters.html`, `index.html`, the two lore rosters,
  `sitemap.xml` and these two docs); the footer-stamp-only pages were left alone, as before. The manuscript
  was not committed. **Open questions for the author** are the numbered judgment calls in §6, first among them
  the cover's "Rice." and the sheets' owner counts.
- **Earlier update (Case 0202 added — branch `case-0202-fossa`, pull request, 2026-10-15).**
  The author asked to add "Case 0202 : Fossa", a publication for the characters, said some also appear in
  2231, attached the manuscript, and sent the cast in two rounds ("first batch of the char : 17 char", then
  10 more characters and 10 scene paintings). Done: a full `0202` dict (27 `characters`, `catalyst` Strain
  H-202, `envoy` Observer 551, 10 `scenes`, `status` coming-soon, placeholders for `pages` / `genre` /
  `synopsis_html`), a `PRINCIPALS` entry, one `RELATED_THEMES` row (0202 with 2231), one sentence each in
  the Cultivator, Catalyst, Faith of Ardwen, Threefold Crown and Decree of Luminescence lore, and five
  reciprocal sentences on 2231 pages (`bertran`, `observer-618`, `villagers-of-vilarnau`,
  `the-kiyote-pair`, `kaneyoshi`). The 10 `scenes` carry the short `"title"` that PR #8 introduced. Images: 1 cover, its square
  `images/share/cover-0202.jpg`, 54 character files (27 slugs x full + thumb) and 20 scene
  files (10 x full + grid). `main` moved (Case 1268, PR #7, then Case 1268 records and the 4420 gazetteer, PR #8) while this was prepared, so the branch was rebased
  onto it twice and the counts re-measured after the second rebase: cases 21 -> 22, characters 334 -> 361, records 187 ->
  197, sitemap 557 -> 595; every local link resolves (20,865 checked) and the new and changed pages were opened in Chromium with no
  broken images or script errors. Shared-person rule: a man who is the same in both cases but told differently
  gets a separate cross-linked page (`bertran-0202`, like `aimeric-2231`). The manuscript and the publication
  package were not committed. `HOME_SCENES` was not changed. Only files that really changed were committed; the
  footer-stamp-only pages were left alone, as before.
- **Earlier update (Case 1268 records, Case 4420 gazetteer, gazetteer sharing and square link previews — branch `case-1268-records-4420-gazetteer`, pull request, 2026-10-14).**
  The author sent 15 scene paintings for Case 1268 and one map for Case 4420, and asked for the 1268 records, the
  4420 gazetteer, the gazetteers to be shareable like subjects, and book and gazetteer links to show a thumbnail on
  other platforms the way subject links do. Done: 15 `scenes` on the `1268` dict (each with an optional short
  `"title"`, §3); a `vessel-of-the-betrayed-host` `LORE` entry; a Share button on gazetteer pages; square preview
  images (`images/share/`, 24 files) wired into book and gazetteer pages through `share_image()`, with
  `tools/make_share_images.py` to make them; 15 x 2 record images and the map plus its thumb. Recount after
  rebuilding: cases 21 (unchanged), characters 334 (unchanged), records 172 -> 187, sitemap 541 -> 557; every local
  link resolves; the new and changed pages were opened in Chromium with no broken images. Only files that really
  changed were committed (the footer-stamp-only pages were left alone, as before). **Open questions for the author:**
  who the dreamer in the two moon paintings is, who the man in the burned village is, and whether the 4420 map's
  banner should keep the old title (§6). Link previews could not be tested on the live platforms from here.
- **Earlier update (Case 1268 added, Case 1153 published — branch `case-1268`, pull request, 2026-10-14).**
  The author sent the cover (titled *Independent Observation*), the manuscript
  (`Case_1268_The_Eleventh_Astral_Dream_2026-10-01_0518AM_GMT_7.md`, revision 1) and 11 character
  sheets, with "char included, manuscript included", and said Case 1153 is live on Google Books
  (`https://play.google.com/store/books/details?id=3IYZEgAAQBAJ`). Done: 1153 `status` is now
  `["published", "google-books"]` with its `google_books_url` (page count, genre and synopsis still
  placeholders); a full `1268` dict (11 characters, `catalyst` The Probe Network, `envoy` Cultivator
  Observer, no scenes) with a `PRINCIPALS` entry and one `RELATED_THEMES` row (1268 with 0000); one
  new sentence each in the Cultivator, Catalyst, Threefold Crown and Faith of Ardwen lore (the
  Cultivator lore also now says "Nearly every case has its own" Envoy). Images: 1 cover and 22
  character files (11 slugs x full + thumb). Recount after rebuilding: cases 20 -> 21, characters
  323 -> 334, records 172 unchanged, sitemap 529 -> 541; every local link resolves (18,881 checked)
  and the new and changed pages were opened in Chromium at desktop and phone width with no broken
  images (the home page's 13px horizontal overflow at 390px wide is on `main` too and was not
  touched). Publishing 1153 also changed its 19 character pages and 13 record pages (its case card
  is no longer muted; each record page gains a Read link) and the related-case blocks of 0000,
  0000B, 0156, 0157, 2140, 2231 and 4417. The manuscript was not committed. `HOME_SCENES` was not
  changed. Only files that really changed were committed; the footer-stamp-only pages (482) were left
  alone, as before.
- **Earlier update (Case 2231 — 25 more Subjects and 14 Records, branch `case-2231-records-v2`, pull request, 2026-10-13).**
  The author sent 14 scene paintings and 25 character sheets in two rounds, told us other AIs use the
  repo too, and asked us to watch the Subject and Record counts. `main` moved while this was prepared
  (0247 and 1153 were merged, then the Case 2365 synopsis), so the branch was brought up to date before the
  final rebuild and the counts re-measured: characters 298 -> 323, records 158 -> 172, sitemap
  490 -> 529; Case 2231 is now 43 Subjects and 14 Records. The 2231 dict gained 25 `characters` entries,
  14 `scenes` and a Catalyst roster `page` pointing at the new `the-kiyote-pair` page; `aimeric-2231` is a
  new slug because `aimeric` is taken (§6 has the full list and the judgment calls). Only the files that
  really changed were committed (the script, the new pages and images, `books/2231.html`, `characters.html`,
  `scenes.html`, `index.html`, `sitemap.xml`, `lore/catalyst.html`, 15 existing 2231 character pages and
  these two docs); the footer-stamp-only pages were left alone. Every local link resolves (18,419 checked).
- **Earlier update (Case 2365 synopsis — branch `case-2365-synopsis`, 2026-10-12).** The author asked
  for the missing synopsis of Case 2365 to be written from the manuscript (revision 3, re-attached in chat;
  the repo itself holds no manuscript files). Done: `synopsis_html` on the `2365` dict in
  `tools/build_site.py` is now three paragraphs in the house style (premise, the Roll and the Saltway,
  the Decree and the Corps' closing log), linking Severin, Faustin, Piero, Sigrid, Marcello and Livia;
  every figure in it was checked against the manuscript. `genre` is still a placeholder. The site was
  regenerated, but a rebuild restamps the build time and cache-bust query on all ~490 pages, so only the
  three files that actually changed were committed (`tools/build_site.py`, `books/2365.html`, this file);
  the next full rebuild will refresh the stamps everywhere.
- **Earlier update (Case 1153 + two gazetteers + the 2365 / 4555 link — branch `case-1153`, pull request).** The
  author sent the cover, the manuscript and 20 character sheets (19 used, one a duplicate) and 13 scene
  paintings for Case 1153, a re-send of the Case 2365 manuscript (the same revision 3), and two map images.
  They also said 2365 and 4555 are the same kingdom, that Xu Lian is in 0000B, that Observer 419 is also
  Case 2140's Observer, that the founding wielder is the boy of Case 0000, and that the Anchorite is the
  main protagonist of 0000B. Done: a full `1153` dict (19 characters, 13 scenes, `catalyst`, `envoy`) with
  a `PRINCIPALS` entry and four `RELATED_THEMES` rows; two gazetteer `LORE` entries and the `gazetteer_body`
  / `gazetteer_cards_html` code and CSS (§6); cross-link edits to the 0000B Anchorite, 0000 Boy and 2140
  Observer 419 bios; sentences in the Cultivator, Catalyst, Faith of Ardwen, Threefold Crown and Decree of
  Luminescence lore. Images: 1 cover, 38 character files, 26 scene files, 4 map files. Recount after
  rebuilding (against `main` after Case 0247 was merged in): cases 19 -> 20, characters 279 -> 298, records
  145 -> 158, sitemap 455 -> 490; every local link in every page resolves (16,945 checked), and the new pages were opened in Chromium at desktop and
  phone width with no overflow or broken images. `HOME_SCENES` was not changed.
- **Earlier update (Case 0247 — on branch `case-0247`, as a pull request).** The author sent the cover,
  the manuscript and 17 reference sheets for Case 0247 in one message, asking for the cover and then
  the cast, and then, in a second message, 11 record paintings, with an instruction to be mindful of
  other AIs working on the repo and of the subject and record counts. Done: a full `0247` dict (17
  characters, 11 scenes, `catalyst`, `envoy`) with a `PRINCIPALS` entry, a `RELATED_THEMES` row
  linking 0247 to 4438 through the Xuanwu Sect's founder Kang Yi, and one new sentence each in the
  Cultivator and Catalyst lore prose. Images: 1 cover, 34 character files (17 slugs x full + thumb), 22
  scene files (11 slugs x full + grid; full is 1000px on the long side, grid 450px, as in the existing
  scenes). Recount after rebuilding: cases 18 -> 19, characters 262 -> 279, records 134 -> 145 (the
  11 new records, and nothing else), sitemap 426 -> 455; every local link in every page resolves
  (16,582 checked). The manuscript was not committed. `HOME_SCENES` was not changed. Because another
  session may be working on `main`, this was not pushed there: `origin/main` was checked before the
  work started and again before the push (see the README entry), and every generated page, the
  sitemap and the counts are rebuilt from the script, so if `main` has moved, rebase the branch,
  re-run `tools/build_site.py` and take the regenerated pages rather than hand-merging them. Lessons
  kept: bios written after reading the manuscript and checked against it by script; every sheet and
  every painting identified from a contact sheet, not by position; the home cast wall is the first six
  subjects in list order; a record's Subject line comes from the characters its caption links, so a
  caption that names someone who is not in the picture needs an explicit `"subjects"` list (the
  Second Emptying and the Shepherd's Reckoning have one).
- **Earlier update (Case 2231 + Case 2365 link and pages — straight into `main`).** The author
  sent the cover, the manuscript and 18 character-dossier sheets for Case 2231, then, for Case 2365,
  the Google Play Books link and "88 page". Done: a full `2231` dict (18 characters, `catalyst`,
  `envoy`, no scenes) with a `PRINCIPALS` entry, a `RELATED_THEMES` row linking 2231 to 4099, one new
  sentence each in the Cultivator and Catalyst lore prose, and one in the Threefold Crown's
  `appears_html`; and `status`, `pages` and `google_books_url` for 2365, which makes it published
  (the author's link and page count are the confirmation). Images: 2 covers (the cover and the
  Catalyst thumb), 36 character files (18 slugs x full + thumb). Recount after rebuilding: cases
  17 -> 18, characters 244 -> 262, records 134 unchanged, sitemap 407 -> 426; every local link in
  every page resolves (15,393 checked), and the new and changed pages were opened in Chromium with no
  broken images. `HOME_SCENES` was not changed. Lessons: read the manuscript before writing the bios
  (the first draft had errors, now corrected and checked by script), and identify sheets by looking
  at them.
- **Earlier update (Case 2365 — on branch `case-2365-stub`, merged into `main` on 2026-10-09 via PR #1).** The author sent
  the cover, then 24 character sheets and 15 scene paintings in two batches through chat, plus the
  manuscript. Done: a full `2365` dict (24 characters, 15 scenes, `catalyst`, `envoy`) with a
  `PRINCIPALS` entry, one new sentence each in the Cultivator and Catalyst lore prose, and the Decree
  of Luminescence `appears_html` naming the case. Images: 1 cover, 48 character files (24 slugs x
  full + thumb), 30 scene files (15 slugs x full + grid). Recount after rebuilding: cases 16 -> 17,
  characters 220 -> 244, scenes 119 -> 134, sitemap 367 -> 407; every local link in every page
  resolves (14,685 checked), and the new pages were opened in Chromium. `HOME_SCENES` was not changed.
  Lesson from this run: the order of attached files does not necessarily match the order the images
  are displayed in, so identify each image by looking at it (a contact sheet), never by position.
- **Earlier update (4438 page count, 0000B cast, new Case 0156 — straight into master).**
  The author sent the whole site as `Dzulfaraaghaini.zip` plus `char.zip` (0000B),
  `0156.zip` + the cover + the manuscript, and the line &ldquo;4438 page number is 82&rdquo;.
  Done: `pages` for 4438 set to `"82"`; 19 characters added to the `0000b` stub and a
  `PRINCIPALS` entry; a full new `0156` dict (26 characters, 14 scenes, `catalyst`, `envoy`)
  placed after 3115, with a `PRINCIPALS` entry; one new sentence each in the Cultivator and
  Catalyst lore prose; one new sentence in the Faith of Ardwen's `appears_html`. Images: 1 cover,
  90 character files (45 slugs x full + thumb), 28 scene files (14 slugs x full + grid). Recount
  after rebuilding: cases 15 -> 16, characters 175 -> 220, scenes 105 -> 119; every local link in
  every page resolves. `HOME_SCENES` was not changed (no 0156 scene on the homepage band).
- **Earlier merge (Case 4438 + two stubs, straight into master).** No staging
  copy this time: the author sent the files with the request. Added: the full
  Case 4438 dict (synopsis, 19 characters, 15 scenes, `catalyst`, `envoy`,
  Google Books link), placed after 4555 so the published books stay grouped;
  two coming-soon stubs (`0000b`, `2114`) appended after 4442; an eighth
  `HOME_SCENES` entry (`the-solstice-ascension`); one new sentence each
  in the Cultivator and Catalyst lore prose. Images: 4 covers (three new, and
  `4420.jpg` replaced in place), 38 character files (19 slugs x full + thumb),
  30 scene files (15 slugs x full + grid). Case 4420's old cover was not
  otherwise touched. Recount after rebuilding: cases 12 -> 15, characters
  156 -> 175, scenes 90 -> 105; every local link in every page resolves.
- **Earlier merge (Case 3115 characters into master).** From a batch
  called `WEB CHANGE 3` (24 character-sheet portraits, plus the complete
  manuscript supplied only for context, per the author's own one-line
  instruction): the previously-empty Book, Case 3115 (*The Listening
  Water*), got its full 24-character cast — see the Book write-up in §6
  above for the complete list and plot summary — plus fresh
  `catalyst`/`envoy` summary dicts (**The Listening Water**, High-Concept/
  Cultural-and-Social; **Observer 471**, &ldquo;the Salt-Root
  Woman&rdquo;), written fresh the same way Book 5's were, so this book
  doesn't silently drop out of either lore roster. Cultivator and Catalyst
  lore prose each picked up one new line, the same pattern as the Case
  4420 merge. `pages`, `genre`, `synopsis_html`, and `status` were left
  untouched (still `coming-soon`) — this batch was characters only, no
  scene art and no publish-readiness signal from the author. No slug
  collisions with the existing cast, so nothing needed disambiguating.
  Images were a pure addition (48 new files, 24 slugs × full + thumb);
  after regenerating, only `books/3115.html`, `index.html`,
  `lore/cultivator.html`, `lore/catalyst.html`, and the 24 new character
  pages changed (the footer build stamp, which every rebuild refreshes on all
  pages, aside) — confirmed by diffing against the pre-merge master.
- **Earlier merge (0188 + 2140 rosters into master), plus revisions.** Two
  staging copies came back at once, both clean forks of master whose only
  differences were additions — checked with a full diff of `build_site.py`
  and a byte-compare of every shared image (no same-named file differed,
  and the two copies' new files didn't overlap). From the first
  (SLAVE-0188): the full Case 0188 dict (synopsis, 12 characters, 12
  scenes, `catalyst`, `envoy`) replaced master's empty stub, its 48 new
  images came across (24 character, 24 scene), and `HOME_SCENES` got a
  seventh entry (`the-granary-of-rats`). From the second (SLAVE-2140): the
  15-character cast replaced master's empty `characters` list for Case
  2140, plus 30 new character images (it had no scene art) — nothing else:
  no synopsis, no `catalyst`/`envoy`, no scenes. An `envoy` record for
  Observer 419 was written fresh (§6); a `catalyst` record deliberately
  was not, for lack of any art to point at. Both books stay `coming-soon`.
  The two large dict splices were done by script from the staging files
  rather than retyped, so the prose is byte-identical to them.
- **Retitle: *The Thermal Vessel War* → *The Vessel of the Betrayed Host*
  (Case 4420).** Author's request. One title field plus the single inline
  `<em>` mention in the synopsis; everything else follows from the title
  field on rebuild. No occurrence of the old title remains in the
  generated site or the script (it survives only in this file's history
  notes, marked as such).
- **Build timestamp in every footer.** `BUILD_TIME` (top of
  `build_site.py`) is computed with `datetime.now()` in GMT+7 each time
  the script runs and printed as "Site last built …" under the footer of
  every page (`footer_html`, styled by `.build-info`). It is never
  hand-edited or stored: it is simply when this version was generated,
  and because a revision on a static site only takes effect once it is
  rebuilt, it doubles as the "last revised" marker. The format matches the
  canon guide's own (`YYYY-MM-DD, HH:MMAM/PM GMT+7`). Note that
  `import build_site` from Python regenerates the whole site as a side
  effect (the script has no `__main__` guard), which also refreshes it.
- **Religion added to the lore.** Three new `LORE` entries — *The Faith of
  Ardwen* (`faith-of-ardwen`), *The Threefold Crown* (`threefold-crown`),
  *The Decree of Luminescence* (`decree-of-luminescence`) — drawn from the
  author's canon guide and written in the same glossary voice as
  Cultivator/Catalyst. They are the first entries to use `appears_html`
  (hand-written "Appears In" prose) rather than a `roster`, because a
  faith isn't one-per-book (Case 0157 alone carries two). Each carries
  `"group": "Religion"`, which `lore_index_html` uses to list them under
  their own **Religion** heading on `lore.html`; entries with no `group`
  (Cultivator, Catalyst) stay in the plain list above it. The Ardwen slug
  is `faith-of-ardwen`, not `ardwen`, so it can't be mistaken for the
  character page of the same name. The pages stick to what believers
  themselves would say: none states the Cultivator connection behind a
  faith's founding, since each book's own page is where that belongs and a
  glossary entry is where a new visitor lands first. Cross-links go to
  existing pages only (Ardwen, Valeria, Yudith, Doreth, the Ember Judge,
  Ambrose, the Third Grain courtroom judge, Aethelgard, Sarel, Fenn, the
  Drowned Road anchorite).
- **Earlier merge (4420 + 4417 scenes into master).** From the SLAVE-4420
  copy: an entirely new Book 5, then titled *The Thermal Vessel War*
  (Case 4420, since renamed — see Book 5 above) — 7
  characters (Yvaine, Kaelen, Maros, Corvus, Soren, Observer 814, and
  Duke Vane, disambiguated to the `vane-4420` slug since it's a different
  character from Book 4's own Vane) and a 17-scene gallery, published
  with the staging copy's own cover and Google Books link. That copy
  forked before master's `catalyst`/`envoy` roster-summary fields
  existed, so both were written fresh for this book (catalyst: **The
  Steel Flask**; envoy: **Observer 814**, &ldquo;the
  Dragon-Speaker&rdquo;) so Book 5 doesn't silently drop out of the
  lore rosters below. From the SLAVE-4417 copy: the **7 scenes Book 4's
  own dict was still missing** (`vane-by-candlelight`, `aurelia-at-the-
  great-concord`, `aurelia-crosses-the-hall`, `aurelia-on-the-throne`,
  `corvin-brings-the-dye`, `ophelia-in-the-corridor`,
  `beatrice-visits-aurelia`) — master had somehow been left at 4 despite
  SLAVE-4417 itself always having had 11; Book 4 is now the full gallery.
  Cultivator and Catalyst lore prose each picked up one new line for the
  Case 4420 data point, and `HOME_SCENES` got a fifth entry
  (`yvaine-in-the-south`). Images were a pure union, no conflicts. Book
  5's pages/genre are still the staging copy's own estimated/suggested
  values — unconfirmed, unlike Books 1–4 (see §7).
- **Earlier merge (0157 scene gallery into master).** The 0157 copy came
  back with one thing master lacked: the Stolen Prince War's 19-scene
  gallery. Its characters, synopsis, cover, page count and lore text were
  identical to master's (or behind it — no Ledger scenes or link, no Royal
  Road link, no clickable status tags, no Book 4), so only the 19-entry
  `"scenes"` list on the 0157 dict and its 38 image files (`<slug>.jpg` +
  `<slug>-grid.jpg` per scene) were taken. Images were a pure union with no
  conflicts, and after regenerating, `books/0157.html` was the only page
  that changed.
- **Earlier merge (0157 + 4417 into master).** From the 0157 copy: 18 new
  Stolen Prince War characters, newer text for five existing ones (Doron,
  Tirtzah, Vahan, the White Draught, the Golden Catacomb), and the synopsis
  wording that names Vartaz and Nairi. From the 4417 copy: Book 4 (13
  characters, 4 scenes, cover `4417.jpg`), published with the
  author-supplied Google Books link. The two lore pages' book
  cross-references were merged by hand. Images were a pure union with no
  conflicts.

## 9. Deployment

- Repo must be named `<username>.github.io` for GitHub Pages to auto-
  serve it at the root domain.
- **Upload the *contents* of this folder to the repo root — not this
  folder nested one level deeper.** This tripped the author up once
  already. `README.md` has the detailed steps.
- `.nojekyll` is already present at the root; keep it.
- Moving to Cloudflare Pages later: connect the repo, leave the build
  command empty, set output directory to the repo root. Nothing else
  changes.

## 10. Quick self-check after making changes

From inside the `tools/` folder:

```bash
python3 build_site.py
```

Then, from the project root, this catches the most common mistakes
(broken relative links) before you hand anything back:

```bash
python3 - << 'EOF'
import re, os
problems, checked = [], 0
for dp, _, fs in os.walk("."):
    for f in fs:
        if not f.endswith(".html"): continue
        hf = os.path.join(dp, f)
        content = open(hf, encoding="utf-8").read()
        for m in re.finditer(r'(?:href|src)="([^"]+)"', content):
            url = m.group(1)
            if url.startswith(("http://", "https://", "mailto:", "#")): continue
            checked += 1
            target = os.path.normpath(os.path.join(dp, url))
            if not os.path.isfile(target):
                problems.append((hf, url))
print(f"checked {checked} local links:", "all OK" if not problems else problems)
EOF
```

And this catches duplicate character slugs, which the generator would
otherwise resolve silently by overwriting a page (it also matches the two
lore slugs; that's harmless):

```bash
python3 - << 'EOF'
import re, collections
src = open("tools/build_site.py", encoding="utf-8").read()
slugs = re.findall(r'"slug": "([^"]+)", "name":', src)
print([s for s, n in collections.Counter(slugs).items() if n > 1] or "no duplicate character slugs")
EOF
```

If you have a real browser available (e.g. Playwright), it's worth
actually clicking through anything you change rather than just reasoning
about the CSS/JS — that's how the flex-stretch image distortion bug, the
forced-aspect-ratio crop bug, and the wrong-output-directory bug all got
caught during this build, well before the author ever saw them.
