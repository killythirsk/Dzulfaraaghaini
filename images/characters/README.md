# Character portraits

Every character has two real JPGs here: `<slug>.jpg` (full size, shown on
that character's own page) and `<slug>-thumb.jpg` (a smaller version shown
in the Characters list on their book's page). Both are already resized
and compressed from the original artwork. There's no forced crop — each
image keeps its own natural proportions, so portraits from different
source art can be different shapes without looking wrong.

To add a new character:

1. Save the portrait as `images/characters/<slug>.jpg` (roughly
   900–1000px on the long edge is plenty) and a smaller copy as
   `images/characters/<slug>-thumb.jpg` (around 300–320px on the long
   edge, for the list view).
2. Add an entry to the relevant book's `"characters"` list in
   `tools/build_site.py` — name, epithets, a one-line teaser, a bio
   paragraph, and an optional quote.
3. Regenerate (see the root `README.md`). The character's own page, its
   row in that book's Characters list, and the lightbox all get wired up
   automatically.
