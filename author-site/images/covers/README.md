# Cover images

Each book's cover is referenced by filename, matching the book's slug:
ghost.svg, aldemark.svg, illumaria.svg, carbonecho.svg, 4099.svg.

The .svg files here now are typographic placeholders so the site is not
broken out of the box. When you have real cover art:

1. Save it as images/covers/<slug>.jpg (or .png/.webp) &mdash; e.g. ghost.jpg.
   Aim for roughly 800x1200px (a 2:3 ratio) and under ~300KB.
2. In books.html, index.html (if that book is featured), and
   books/<slug>.html, find the line referencing "<slug>.svg" and change the
   extension to match your new file (e.g. ghost.svg -> ghost.jpg). Use your
   editor's find-and-replace across the project to catch every reference.
