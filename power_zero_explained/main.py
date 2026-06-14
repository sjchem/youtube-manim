"""Convenience CLI for previewing or rendering the Manim project."""

from __future__ import annotations

import argparse
import subprocess
import sys

from utils.render_helpers import build_manim_command, scene_choices


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render the zero-power Manim explainer.")
    parser.add_argument(
        "scene",
        nargs="?",
        default="full",
        help="Scene alias to render. Use --list to see choices.",
    )
    parser.add_argument(
        "-q",
        "--quality",
        choices=["l", "m", "h", "p", "k"],
        default="l",
        help="Manim quality preset: l, m, h, p, or k.",
    )
    parser.add_argument("-p", "--preview", action="store_true", help="Open the rendered video after rendering.")
    parser.add_argument("--fps", type=int, default=None, help="Optional output frame rate override.")
    parser.add_argument("-o", "--output-file", default=None, help="Optional Manim output file name.")
    parser.add_argument("--list", action="store_true", help="List available scene aliases.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.list:
        print("\n".join(scene_choices()))
        return 0

    command = build_manim_command(
        scene_name=args.scene,
        quality=args.quality,
        preview=args.preview,
        fps=args.fps,
        output_file=args.output_file,
    )
    print("Running:", " ".join(command))
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    sys.exit(main())
