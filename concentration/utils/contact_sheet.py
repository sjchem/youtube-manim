"""Tile storyboard PNGs into one contact sheet for quick review.

    python -m utils.contact_sheet scene_05 --cols 3
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

import config as cfg


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prefix", help="File prefix, e.g. scene_05")
    parser.add_argument("--cols", type=int, default=3)
    parser.add_argument("--dir", default="output/storyboard")
    parser.add_argument("--width", type=int, default=560, help="Width of each tile in pixels")
    args = parser.parse_args()

    folder = cfg.PROJECT_ROOT / args.dir
    files = sorted(folder.glob(f"{args.prefix}_play*.png"))
    if not files:
        print("No stills found; run utils.storyboard first.")
        return 1
    tiles = []
    for path in files:
        image = Image.open(path)
        tiles.append(image.resize((args.width, round(args.width * image.height / image.width))))
    w, h = tiles[0].size
    rows = (len(tiles) + args.cols - 1) // args.cols
    sheet = Image.new("RGB", (w * args.cols, h * rows), cfg.BG)
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % args.cols) * w, (index // args.cols) * h))
    out = folder / f"{args.prefix}_sheet.png"
    sheet.save(out)
    print(Path(out).relative_to(cfg.PROJECT_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
