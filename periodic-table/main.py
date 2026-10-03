"""Command-line entry point for 'Why Does the Periodic Table Have This Shape?'.

Examples:
    python main.py list                 # chapter list with timestamps
    python main.py preview 06           # fast 480p15 preview of one chapter
    python main.py scene 06             # one chapter at full quality
    python main.py preview all          # every chapter as separate previews
    python main.py preview full         # the whole film at preview quality
    python main.py render               # the whole film at 1080p30
    python main.py check                # model + narration + timing + layout audits
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
    "scene_01": ("manim_scenes.scene_01_hook", "Scene01Hook", "Hook: why this shape? (3D)"),
    "scene_02": ("manim_scenes.scene_02_atomic_number", "Scene02AtomicNumber", "Protons give the order, not the shape"),
    "scene_03": ("manim_scenes.scene_03_electrons", "Scene03Electrons", "Where does each new electron go?"),
    "scene_04": ("manim_scenes.scene_04_four_shapes", "Scene04FourShapes", "s p d f: capacities become widths (3D)"),
    "scene_05": ("manim_scenes.scene_05_period_one", "Scene05PeriodOne", "Building period 1, and helium's seat"),
    "scene_06": ("manim_scenes.scene_06_period_two", "Scene06PeriodTwo", "Building period 2, electron by electron"),
    "scene_07": ("manim_scenes.scene_07_groups", "Scene07Groups", "A group is a recurring electron pattern"),
    "scene_08": ("manim_scenes.scene_08_group_chemistry", "Scene08GroupChemistry", "Alkali metals and noble gases (3D)"),
    "scene_09": ("manim_scenes.scene_09_period_four", "Scene09PeriodFour", "4s before 3d: the transition metals"),
    "scene_10": ("manim_scenes.scene_10_filling_order", "Scene10FillingOrder", "The filling order and the n + l rule"),
    "scene_11": ("manim_scenes.scene_11_f_block", "Scene11FBlock", "Cutting out the f block"),
    "scene_12": ("manim_scenes.scene_12_four_blocks", "Scene12FourBlocks", "Four blocks, four shapes (3D)"),
    "scene_13": ("manim_scenes.scene_13_periods", "Scene13Periods", "Why the rows repeat: 2, 8, 8, 18..."),
    "scene_14": ("manim_scenes.scene_14_trends", "Scene14Trends", "Atomic size across and down (3D)"),
    "scene_15": ("manim_scenes.scene_15_reconstruction", "Scene15Reconstruction", "The final reconstruction (3D)"),
    "scene_16": ("manim_scenes.scene_16_subscribe", "Scene16Subscribe", "Subscribe card"),
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
    print("─" * 92)
    elapsed = 0
    for key, (_, class_name, title) in SCENE_MAP.items():
        duration = cfg.SCENE_DURATIONS[key[-2:]]
        start = f"{elapsed // 60:02d}:{elapsed % 60:02d}"
        flag = "3D" if key[-2:] in cfg.THREE_D_SCENES else "  "
        print(f"{key:<10} {start:>6}  {flag}  {class_name:<24} {duration:>5.0f}s  {title}")
        elapsed += int(duration)
    total = sum(cfg.SCENE_DURATIONS.values())
    print("─" * 92)
    minutes, seconds = divmod(int(total), 60)
    print(f"{'FullVideo':<10} {'':>6}      {'FullVideo':<24} {total:>5.0f}s  ({minutes}:{seconds:02d})\n")


def run_checks() -> int:
    steps = [
        ["-m", "utils.physics_models"],
        ["-m", "utils.narration_audit"],
        ["-m", "utils.timing_audit"],
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
