"""Command-line entry point for 'Why Does Pascal's Triangle Know Algebra?'.

Examples:
    python main.py list                 # chapter list with timestamps
    python main.py preview 05           # fast 480p15 preview of one chapter
    python main.py scene 05             # one chapter at full quality (1080p30)
    python main.py preview all          # every chapter as separate previews
    python main.py preview full         # the whole film at preview quality
    python main.py render               # the whole film at 1080p30
    python main.py check                # maths + narration + timing + layout audits
    python main.py audio-check          # recorded narration clips vs chapter lengths
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parent
for _path in (str(PROJECT_ROOT), str(REPO_ROOT)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import config as cfg  # noqa: E402

SCENE_MAP: dict[str, tuple[str, str, str]] = {
    "scene_01": ("manim_scenes.scene_01_mystery", "Scene01Mystery", "The mystery: predict every coefficient"),
    "scene_02": ("manim_scenes.scene_02_start_small", "Scene02StartSmall", "Start small: (a+b)^2 as area"),
    "scene_03": ("manim_scenes.scene_03_cube", "Scene03Cube", "The cube of a + b (3D)"),
    "scene_04": ("manim_scenes.scene_04_triangle_builds", "Scene04TriangleBuilds", "The triangle builds itself"),
    "scene_05": ("manim_scenes.scene_05_choice_machines", "Scene05ChoiceMachines", "Five choice machines, 32 lists"),
    "scene_06": ("manim_scenes.scene_06_combinations", "Scene06Combinations", "Combinations: five choose two"),
    "scene_07": ("manim_scenes.scene_07_theorem", "Scene07Theorem", "The binomial theorem, read aloud"),
    "scene_08": ("manim_scenes.scene_08_exponents", "Scene08Exponents", "Opposite exponents, symmetry, row sums"),
    "scene_09": ("manim_scenes.scene_09_pascal_rule", "Scene09PascalRule", "Why Pascal's rule works"),
    "scene_10": ("manim_scenes.scene_10_paths", "Scene10Paths", "Paths through the triangle"),
    "scene_11": ("manim_scenes.scene_11_coin_flips", "Scene11CoinFlips", "Coin flips and the bell curve (3D)"),
    "scene_12": ("manim_scenes.scene_12_payoff", "Scene12Payoff", "The final payoff"),
    "scene_13": ("manim_scenes.scene_13_subscribe", "Scene13Subscribe", "Subscribe card"),
}


def _resolve_scene(value: str) -> tuple[str, str, str] | None:
    if value.isdigit():
        value = f"scene_{int(value):02d}"
    normalized = value if value.startswith("scene_") else f"scene_{value[:2]}"
    for key, details in SCENE_MAP.items():
        if normalized == key or value.startswith(key):
            return details
    return None


def _run_manim(module: str, class_name: str, quality: str, *, preview: bool = False) -> int:
    cmd = [
        sys.executable, "-m", "manim", f"-q{quality}",
        "--fps", str(cfg.RENDER["preview_fps"] if preview else cfg.RENDER["fps"]),
        "-r", str(cfg.RENDER["preview_resolution"] if preview else cfg.RENDER["resolution"]),
        f"{module.replace('.', '/')}.py", class_name,
    ]
    print("▶", " ".join(cmd))
    return subprocess.run(cmd, cwd=PROJECT_ROOT, check=False).returncode


def list_scenes() -> None:
    print(f"\n{cfg.PROJECT_TITLE} — {cfg.PROJECT_PART}")
    print("─" * 96)
    elapsed = 0
    for key, (_, class_name, title) in SCENE_MAP.items():
        duration = cfg.SCENE_DURATIONS[key[-2:]]
        start = f"{elapsed // 60:02d}:{elapsed % 60:02d}"
        flag = "3D" if key[-2:] in cfg.THREE_D_SCENES else "  "
        print(f"{key:<10} {start:>6}  {flag}  {class_name:<24} {duration:>5.0f}s  {title}")
        elapsed += int(duration)
    total = sum(cfg.SCENE_DURATIONS.values())
    print("─" * 96)
    minutes, seconds = divmod(int(total), 60)
    print(f"{'FullVideo':<10} {'':>6}      {'FullVideo':<24} {total:>5.0f}s  ({minutes}:{seconds:02d})\n")


def run_checks() -> int:
    steps = [
        ["-m", "utils.math_utils"],
        ["-m", "utils.physics_models"],
        ["-m", "utils.narration_audit"],
        ["-m", "utils.timing_audit"],
        ["-m", "utils.timing_audit", "--full"],
        ["-m", "utils.layout_audit"],
    ]
    for step in steps:
        print("▶ python", " ".join(step), flush=True)
        code = subprocess.run([sys.executable, *step], cwd=PROJECT_ROOT, check=False).returncode
        if code:
            return code
    return 0


def main() -> int:
    args = sys.argv[1:]
    command = args[0] if args else "list"
    if command in {"list", "ls"}:
        list_scenes()
        return 0
    if command == "check":
        return run_checks()
    if command == "audio-check":
        from utils.voiceover import main as audit_audio

        return audit_audio()
    if command == "render":
        return _run_manim("manim_scenes.full_video", "FullVideo", str(cfg.RENDER["youtube_quality"]))
    if command in {"preview", "scene"}:
        if len(args) < 2:
            print(f"Usage: python main.py {command} <scene number or name | all | full>")
            return 2
        preview = command == "preview"
        quality = str(cfg.RENDER["preview_quality"] if preview else cfg.RENDER["youtube_quality"])
        if args[1] == "all":
            for module, class_name, _ in SCENE_MAP.values():
                result = _run_manim(module, class_name, quality, preview=preview)
                if result:
                    return result
            return 0
        if args[1] == "full":
            return _run_manim("manim_scenes.full_video", "FullVideo", quality, preview=preview)
        scene = _resolve_scene(args[1])
        if scene is None:
            print(f"Unknown scene: {args[1]}")
            list_scenes()
            return 2
        module, class_name, _ = scene
        return _run_manim(module, class_name, quality, preview=preview)
    print(f"Unknown command: {command}")
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
