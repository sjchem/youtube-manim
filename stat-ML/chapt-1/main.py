"""CLI entry point for Statistics for ML — Part 1, Chapter 1.

Usage
-----
List all scenes:
    python main.py list

Preview one scene (low quality, fast):
    python main.py preview scene_01
    python main.py preview scene_06_overfitting

Render the full video at YouTube quality:
    python main.py render

Render a single scene at YouTube quality:
    python main.py scene scene_03
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# Ensure imports work when run from any directory.
PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT    = PROJECT_ROOT.parent.parent
for _p in (str(PROJECT_ROOT), str(REPO_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import config as cfg  # noqa: E402  (must be after sys.path setup)

SCENE_MAP: dict[str, tuple[str, str]] = {
    "scene_01": ("manim_scenes.scene_01_opening",       "Scene01Opening"),
    "scene_02": ("manim_scenes.scene_02_uncertain_world","Scene02UncertainWorld"),
    "scene_03": ("manim_scenes.scene_03_signal_noise",  "Scene03SignalNoise"),
    "scene_04": ("manim_scenes.scene_04_population_sample","Scene04PopulationSample"),
    "scene_05": ("manim_scenes.scene_05_patterns_prediction","Scene05PatternsPrediction"),
    "scene_06": ("manim_scenes.scene_06_overfitting",   "Scene06Overfitting"),
    "scene_07": ("manim_scenes.scene_07_bias_variance", "Scene07BiasVariance"),
    "scene_08": ("manim_scenes.scene_08_statistics_layer","Scene08StatisticsLayer"),
    "scene_09": ("manim_scenes.scene_09_subscribe",     "Scene09Subscribe"),
}

FULL_VIDEO_MODULE = "manim_scenes.full_video"
FULL_VIDEO_CLASS  = "FullVideo"


def _manim(module: str, class_name: str, quality: str, extra: list[str] | None = None) -> int:
    cmd = [
        sys.executable, "-m", "manim",
        f"-q{quality}",
        "--fps", str(cfg.RENDER["fps"]),
        f"{module.replace('.', '/')}.py",
        class_name,
        *(extra or []),
    ]
    print("▶", " ".join(cmd))
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    return result.returncode


def cmd_list() -> None:
    print(f"\n{'─'*60}")
    print(f"  {cfg.PROJECT_TITLE}")
    print(f"  {cfg.SERIES_LABEL}  —  {cfg.SERIES_PART}")
    print(f"{'─'*60}")
    for key, (_, cls) in SCENE_MAP.items():
        dur = cfg.SCENE_DURATIONS.get(key.split("_")[1], "?")
        print(f"  {key:<12}  {cls:<32}  ~{dur}s")
    print(f"\n  full video → {FULL_VIDEO_CLASS}")
    print(f"{'─'*60}\n")


def cmd_preview(scene_key: str) -> int:
    key = scene_key if scene_key.startswith("scene_") else f"scene_{scene_key[:2]}"
    # Accept partial names like "scene_06" or "scene_06_overfitting"
    match = None
    for k in SCENE_MAP:
        if k == key or scene_key.startswith(k):
            match = k
            break
    if match is None:
        print(f"Unknown scene: {scene_key}")
        print("Run  python main.py list  to see available scenes.")
        return 1
    module, cls = SCENE_MAP[match]
    return _manim(module, cls, cfg.RENDER["preview_quality"])


def cmd_scene(scene_key: str) -> int:
    key = scene_key if scene_key.startswith("scene_") else f"scene_{scene_key[:2]}"
    match = None
    for k in SCENE_MAP:
        if k == key or scene_key.startswith(k):
            match = k
            break
    if match is None:
        print(f"Unknown scene: {scene_key}")
        return 1
    module, cls = SCENE_MAP[match]
    return _manim(module, cls, cfg.RENDER["youtube_quality"])


def cmd_render() -> int:
    return _manim(FULL_VIDEO_MODULE, FULL_VIDEO_CLASS, cfg.RENDER["youtube_quality"])


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] == "list":
        cmd_list()
        return
    command = args[0]
    if command == "preview":
        if len(args) < 2:
            print("Usage: python main.py preview <scene_key>")
            sys.exit(1)
        sys.exit(cmd_preview(args[1]))
    elif command == "scene":
        if len(args) < 2:
            print("Usage: python main.py scene <scene_key>")
            sys.exit(1)
        sys.exit(cmd_scene(args[1]))
    elif command == "render":
        sys.exit(cmd_render())
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
