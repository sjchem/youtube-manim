"""Small CLI for listing and rendering project scenes."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from utils.render_helpers import QUALITY_PRESETS, list_scenes, render_command


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render the negative-times-negative Manim project.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List available scenes.")

    preview = sub.add_parser("preview", help="Render and open a quick preview.")
    preview.add_argument("scene", nargs="?", default="01", help="Scene key: 01-08 or full.")
    preview.add_argument("--quality", default="preview", choices=QUALITY_PRESETS)

    render = sub.add_parser("render", help="Render a scene without opening it.")
    render.add_argument("scene", help="Scene key: 01-08 or full.")
    render.add_argument("--quality", default="high", choices=QUALITY_PRESETS)

    full = sub.add_parser("full", help="Render the full video.")
    full.add_argument("--quality", default="high", choices=QUALITY_PRESETS)
    full.add_argument("--preview", action="store_true", help="Open the video after rendering.")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parent

    if args.command == "list":
        for key, scene_file, scene_class in list_scenes():
            print(f"{key:>4}  {scene_class:<36} {scene_file}")
        return 0

    if args.command == "preview":
        cmd = render_command(args.scene, args.quality, preview=True)
    elif args.command == "render":
        cmd = render_command(args.scene, args.quality, preview=False)
    else:
        cmd = render_command("full", args.quality, preview=args.preview)

    print(" ".join(cmd))
    return subprocess.run(cmd, cwd=root, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
