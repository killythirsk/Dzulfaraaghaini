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
various stages of publication; four are live on the site so far — see
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

Nav (same on every page): **Home / Book / Lore / About / Contact.**
Notably *not* in the nav: Characters, Scenes — both live inside each
book's own page rather than as their own top-level sections.

```
/index.html            Homepage — hero (with a counts line), every book, a cast wall, a scene band, a lore teaser
/books.html             Full book list (currently four entries)
/books/0000.html          The Sword of Valeria's full page
/books/4099.html          The Ledger of a Single Sweetness's full page
/books/0157.html          The Stolen Prince War's full page
/books/4417.html          The Iron Stiletto War's full page
/lore.html               Glossary index
/lore/<slug>.html          One page per term (cultivator, catalyst; lore/catalyst-tier.html
                            is only a redirect stub to catalyst.html)
/characters/<slug>.html    One page per character (86 total — 10 for
                            Valeria, 28 for the Ledger, 35 for the Stolen
                            Prince War, 13 for the Iron Stiletto War; see §6)
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

All four books share a confirmed, explicit meta-narrative device: a loose
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
when it is merged. Only the four live books are listed; canon-guide cases that
have no book on the site yet (0156, 4442, 0188, 1268, 4425, 3887) are not.

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

Four scenes exist, all in a distinct thick, palette-knife painterly style
that's different from the 13 watercolor character sheets: Vane delivering
the heels, the heels alone on a dais, Corvin and Isolde by a fireplace,
and Ophelia delivering Aurelia's refusal to Beatrice. Scene order and
captions are Claude's inference from the art plus the manuscript's own
outline and chapter titles, not author-confirmed. The manuscript itself
(a complete, "Revision 4 (Final)" draft) was read only for these facts —
it hasn't had any editorial/proofreading pass.

## 7. What's placeholder / incomplete right now

- Genres and page counts are all settled: 102 / 99 / 96 / 109 pages for Books 1–4,
  and no book carries an unconfirmed-genre `editor-note` any more (genres were
  chosen by Claude at the author's instruction).
- The Iron Stiletto War's Google Books link came from the author and hasn't
  been opened by an AI (Google blocks automated fetches) — one click
  confirms it.
- Every book now has a Scenes slider (8 / 19 / 19 / 4 images for Books
  1–4), so the "not yet added" placeholder no longer shows on any page — it
  stays in the generator for any future book added without scene art. The
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
  "More than a dozen novels" total were mentioned early on — only four
  are live.

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
- **Latest merge (0157 scene gallery into master).** The 0157 copy came
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
