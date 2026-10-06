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
various stages of publication; seven are live on the site so far, plus
three coming-soon books with a character roster (0188, 2140, 3115) and five
cover-only coming-soon entries (3312, 3887, 4442, 0000B, 2114) — see
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
- **Related Cases / Subjects / Records** are generated from existing data, nothing invented: cases relate by *same catalyst class* (each book's `catalyst.meta`) and *shared faith* (the Religion lore pages' `appears_html` links); subjects relate by character cross-links inside bios (both directions), falling back to the case's principals; records are the scenes whose caption links to that subject; lore pages list the cases where the concept appears. Hand-written thematic links go in **`RELATED_THEMES`** as `(case slug, case slug, "reason")`. "Same Observer" is intentionally absent: each case has a different Observer (see §6).
- **Mobile "see more":** markup opts in with `data-cap="N"` (show N list items, button reveals the rest) or `data-collapse="N"` (clip a block to N rem). `js/site.js` adds the buttons on phones (<= 40rem) only; desktop is untouched, and the Subjects/Records indexes lift the cap while a search or case filter is active.
- **Fix:** the hero "Enter the archive" button sat off-centre because the global `p { max-width: 68ch }` left its paragraph left-aligned; `.hero--home p { margin-inline: auto }` fixes it.

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
/books.html             Full book list (currently fifteen entries: seven published,
                            eight coming-soon — see §6)
/books/0000.html          The Sword of Valeria's full page
/books/4099.html          The Ledger of a Single Sweetness's full page
/books/0157.html          The Stolen Prince War's full page
/books/4417.html          The Iron Stiletto War's full page
/lore.html               Glossary index (plain list on top, then a "Religion"
                            heading over the three faiths — `group` field, §8)
/lore/<slug>.html          One page per term (cultivator, catalyst, faith-of-ardwen,
                            threefold-crown, decree-of-luminescence;
                            lore/catalyst-tier.html is only a redirect stub to
                            catalyst.html)
/characters/<slug>.html    One page per character (175 total — 10 for
                            Valeria, 28 for the Ledger, 35 for the Stolen
                            Prince War, 13 for the Iron Stiletto War, 7 for
                            the Vessel of the Betrayed Host, 12 for the
                            Vessel of Unmediated Grace, 12 for the Songs
                            Never Mention the Cats, 15 for the Third Grain,
                            24 for the Listening Water, 19 for the Heavenly
                            Thunder-Serpent; see §6)
/about.html               Biography only
/contact.html              Royal Road / Instagram / Threads (real; no email, by the author's choice)
```

### 4a. Anatomy of a book detail page
In order: back-link → cover + title + status tags → Book Info (pages,
genre, synopsis) → **Characters** (a `catalog-list` of every character in
*that* book, links to their own page) → **Scenes** (a *horizontal slider*
if the book has any scene art, or a plain "not yet added" note if it
doesn't — see §7 for which is which right now) → a boxed "Read This Book"
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
`catalyst` and/or `envoy` record — the seven published books (4438 included), plus 0188 (both
records), 2140 (envoy only — see §6) and 3115 (both records — see §6) now
that their rosters have been merged in. Canon-guide cases with no book dict
on the site at all (0156, 1268, 4425) or only an empty coming-soon stub with
no cast (3312, 3887, 4442, 0000B, 2114) are not.

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
still carrying the `editor-note` span) — unlike Books 1–4, nobody has
confirmed these for real yet.

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
4417 and 4420 links). **`pages` is still the `EDITOR_PAGES` placeholder** &mdash;
no page count was given and the Google page could not be read. Genre
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
  `~123` pages and suggested genre are still the SLAVE-4420 staging
  copy's own unconfirmed estimate, `editor-note` span and all; resolve
  the same way Books 1–4 were.
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
  "More than a dozen novels" total were mentioned early on — only seven are
  live, plus 0188, 2140 and 3115 with a roster but no synopsis yet (§6).
- **Case 4438** (*The Heavenly Thunder-Serpent*) is live with a full cast,
  scene gallery, both roster records and its Google Books link, but `pages` is
  still the `EDITOR_PAGES` placeholder, and the link hasn't been opened by an
  AI. **Cases 0000B and 2114** are cover-only coming-soon stubs (§6).
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
- **Latest merge (Case 4438 + two stubs, straight into master).** No staging
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
