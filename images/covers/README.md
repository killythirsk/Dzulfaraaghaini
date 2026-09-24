# Cover images

Each book's cover is a real JPG here (0000.jpg for The Sword of Valeria,
4099.jpg for The Ledger of a Single Sweetness), already resized and
compressed for the web from the original artwork.

To add a cover for a new book:

1. Save it as `images/covers/<slug>.jpg`, matching the slug you give that
   book in `tools/build_site.py`. Aim for roughly 900x1350px (a 2:3 ratio)
   and well under 500KB — resize/compress the original first if it's
   larger.
2. Set `"cover_file": "<slug>.jpg"` on that book's entry in
   `tools/build_site.py`, then regenerate (see the root `README.md`).

No manual HTML editing needed — the generator wires the filename into
every page that references it.
