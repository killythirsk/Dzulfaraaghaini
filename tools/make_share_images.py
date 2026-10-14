#!/usr/bin/env python3
"""Make the square link-preview images in images/share/ from the cover and map art.

Why: when a link is shared (WhatsApp, Telegram, Facebook, X, Discord, iMessage ...) the
platform shows one small, roughly square thumbnail taken from the page's og:image. Subject
sheets are almost square, so they show whole. Covers and maps are tall (2:3), and most
platforms crop a tall image to a square slice from its middle, which cuts the title and the
top of the art. These files put the whole cover or map, uncropped, on a dark square, so a
case or gazetteer link previews the same way a subject link does.

    images/covers/<name>.jpg  ->  images/share/cover-<name>.jpg
    images/maps/<name>.jpg    ->  images/share/map-<name>.jpg

Needs Pillow (`pip install pillow`); this is an authoring-time script only, build_site.py
itself still needs nothing but Python. Run it from anywhere after adding or replacing a
cover or a map, then run build_site.py. build_site.py falls back to the original art if a
share image is missing, so forgetting this step never breaks a page.

    python3 tools/make_share_images.py          # only makes missing / outdated files
    python3 tools/make_share_images.py --force  # remakes every file
"""
import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZE = 1200                 # square canvas, px; Facebook / X / WhatsApp all accept this
MARGIN = 48                 # breathing room around the art
BG = (27, 27, 27)           # --night in css/style.css
EDGE = (58, 58, 54)         # --stone: a hairline so dark art still has an edge
LIMIT = 280 * 1024          # stay under ~300 KB: WhatsApp can skip heavier preview images
JOBS = (("covers", "cover"), ("maps", "map"))


def make(src, dst):
    art = Image.open(src).convert("RGB")
    box = SIZE - 2 * MARGIN
    scale = min(box / art.width, box / art.height)
    art = art.resize((round(art.width * scale), round(art.height * scale)), Image.LANCZOS)
    canvas = Image.new("RGB", (SIZE, SIZE), BG)
    x, y = (SIZE - art.width) // 2, (SIZE - art.height) // 2
    canvas.paste(art, (x, y))
    ImageDraw.Draw(canvas).rectangle((x - 1, y - 1, x + art.width, y + art.height), outline=EDGE)
    quality = 84
    while True:
        canvas.save(dst, "JPEG", quality=quality, optimize=True, progressive=True)
        if os.path.getsize(dst) <= LIMIT or quality <= 60:
            return quality
        quality -= 4


def main():
    force = "--force" in sys.argv
    out_dir = os.path.join(ROOT, "images", "share")
    os.makedirs(out_dir, exist_ok=True)
    made = skipped = 0
    for folder, prefix in JOBS:
        src_dir = os.path.join(ROOT, "images", folder)
        for name in sorted(os.listdir(src_dir)):
            if not name.endswith(".jpg") or "thumb" in name:
                continue
            src = os.path.join(src_dir, name)
            dst = os.path.join(out_dir, "%s-%s" % (prefix, name))
            if not force and os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
                skipped += 1
                continue
            q = make(src, dst)
            made += 1
            print("%-34s %4d KB  (quality %d)" % (os.path.relpath(dst, ROOT), os.path.getsize(dst) // 1024, q))
    print("made %d, up to date %d" % (made, skipped))


if __name__ == "__main__":
    main()
