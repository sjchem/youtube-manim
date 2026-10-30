"""Command-line entry point for 'Concentration, Explained Visually'.

Examples:
    python main.py list                 # scene list with timestamps
    python main.py chapters             # the twelve YouTube chapter markers
    python main.py preview 08           # fast 480p15 preview of one scene
    python main.py scene 08             # one scene at full quality (1080p30)
    python main.py preview all          # every scene as separate previews
    python main.py preview full         # the whole film at preview quality
    python main.py render               # the whole film at 1080p30
    python main.py check                # model + spoken numbers + narration + timing + layout audits
    python main.py audio-check          # recorded narration clips vs scene lengths
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
    "scene_01": ("manim_scenes.scene_01_mystery", "Scene01Mystery", "Hook: glucose dissolves (3D); four answers"),
    "scene_02": ("manim_scenes.scene_02_counting_moles", "Scene02CountingMoles", "Masses add on a balance; n = m / M"),
    "scene_03": ("manim_scenes.scene_03_volume_not_additive", "Scene03VolumeNotAdditive", "50 + 50 mL -> 96.5 mL; four quantities"),
    "scene_04": ("manim_scenes.scene_04_molarity", "Scene04Molarity", "Glucose lit, volume outlined (3D); c = n / V"),
    "scene_05": ("manim_scenes.scene_05_volumetric_flask", "Scene05VolumetricFlask", "Wrong way vs filling to the mark (3D)"),
    "scene_06": ("manim_scenes.scene_06_molality", "Scene06Molality", "Solvent lit and weighed; denominator swaps"),
    "scene_07": ("manim_scenes.scene_07_colligative", "Scene07Colligative", "Freezing-point drop from molality"),
    "scene_08": ("manim_scenes.scene_08_temperature", "Scene08Temperature", "Heat a sealed cylinder: M falls, m holds (3D)"),
    "scene_09": ("manim_scenes.scene_09_both_measures", "Scene09BothMeasures", "Bench vs physical chemistry; M vs m plot"),
    "scene_10": ("manim_scenes.scene_10_normality", "Scene10Normality", "H2SO4 molecule (3D); N = M f; deprecation"),
    "scene_11": ("manim_scenes.scene_11_two_reactions", "Scene11TwoReactions", "One proton vs two: 0.500 N vs 1.00 N"),
    "scene_12": ("manim_scenes.scene_12_mole_fraction", "Scene12MoleFraction", "101-molecule crowd (3D); random picks"),
    "scene_13": ("manim_scenes.scene_13_sum_to_one", "Scene13SumToOne", "x's add to one; Raoult's law"),
    "scene_14": ("manim_scenes.scene_14_percent_mass", "Scene14PercentMass", "% w/w on a balance; % w/v in a flask"),
    "scene_15": ("manim_scenes.scene_15_percent_volume", "Scene15PercentVolume", "% v/v to the mark; grams per litre"),
    "scene_16": ("manim_scenes.scene_16_ppm", "Scene16Ppm", "One gold dot in a million; ppm and ppb bases"),
    "scene_17": ("manim_scenes.scene_17_density_bridge", "Scene17DensityBridge", "One-litre cube (3D): density links M and m"),
    "scene_18": ("manim_scenes.scene_18_dilution", "Scene18Dilution", "Particles conserved into a bigger flask (3D)"),
    "scene_19": ("manim_scenes.scene_19_traps", "Scene19Traps", "Five traps with countdowns"),
    "scene_20": ("manim_scenes.scene_20_finale", "Scene20Finale", "The concentration map around the glass (3D)"),
    "scene_21": ("manim_scenes.scene_21_subscribe", "Scene21Subscribe", "Subscribe card"),
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


def _stamp(seconds: float) -> str:
    minutes, rest = divmod(int(seconds), 60)
    return f"{minutes:02d}:{rest:02d}"


def scene_starts() -> dict[str, float]:
    starts, elapsed = {}, 0.0
    for key, duration in cfg.SCENE_DURATIONS.items():
        starts[key] = elapsed
        elapsed += duration
    return starts


def list_scenes() -> None:
    print(f"\n{cfg.PROJECT_TITLE} — {cfg.PROJECT_PART}")
    print("─" * 104)
    starts = scene_starts()
    for key, (_, class_name, title) in SCENE_MAP.items():
        number = key[-2:]
        print(f"{key:<10} {_stamp(starts[number]):>6}  {class_name:<26} {cfg.SCENE_DURATIONS[number]:>5.0f}s  {title}")
    total = sum(cfg.SCENE_DURATIONS.values())
    print("─" * 104)
    print(f"{'FullVideo':<10} {'':>6}  {'FullVideo':<26} {total:>5.0f}s  ({_stamp(total)})\n")


def list_chapters() -> None:
    starts = scene_starts()
    for first, title in cfg.YOUTUBE_CHAPTERS:
        print(f"{_stamp(starts[first])} {title}")


def run_checks() -> int:
    steps = [
        ["-m", "utils.math_utils"],
        ["-m", "utils.physics_models"],
        ["-m", "utils.concentration_data"],
        ["-m", "utils.narration_audit"],
        ["-m", "utils.timing_audit"],
        ["-m", "utils.timing_audit", "--fps", "30"],
        ["-m", "utils.timing_audit", "--full"],
        ["-m", "utils.layout_audit", "--motion"],
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
    if command == "chapters":
        list_chapters()
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
