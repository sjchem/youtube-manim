"""Command-line entry point for 'Vectors & Projectile Motion'.

Examples:
    python main.py list                 # scene list with timestamps
    python main.py chapters             # the nine YouTube chapter markers
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
    "scene_01": ("manim_scenes.scene_01_predict_flight", "Scene01PredictFlight", "Hook: a 3D throw, floor and wall shadows; title"),
    "scene_02": ("manim_scenes.scene_02_three_questions", "Scene02ThreeQuestions", "Position, velocity, acceleration; two cars, one speed"),
    "scene_03": ("manim_scenes.scene_03_scalars", "Scene03Scalars", "Scalar cards, -5 °C, 100 m in 10 s, speedometer"),
    "scene_04": ("manim_scenes.scene_04_vectors", "Scene04Vectors", "Arrows, notation, components preview, east at 20 m/s"),
    "scene_05": ("manim_scenes.scene_05_displacement", "Scene05Displacement", "3-4-5 walk and a 400 m lap on a 3D field"),
    "scene_06": ("manim_scenes.scene_06_why_add", "Scene06WhyAdd", "Same way, opposite ways; commutative, associative"),
    "scene_07": ("manim_scenes.scene_07_drone", "Scene07Drone", "Drone 6 E + 8 N (3D); triangle, parallelogram, cosine law"),
    "scene_08": ("manim_scenes.scene_08_subtraction", "Scene08Subtraction", "-B, (5,3)-(2,1), a car turns a corner: delta v"),
    "scene_09": ("manim_scenes.scene_09_scalar_multiple", "Scene09ScalarMultiple", "k slider; 2A and -A; F = m a on a cart"),
    "scene_10": ("manim_scenes.scene_10_unit_vectors", "Scene10UnitVectors", "i hat, j hat; A hat on the unit circle"),
    "scene_11": ("manim_scenes.scene_11_resolve", "Scene11Resolve", "Light and shadow components; a sled's rope"),
    "scene_12": ("manim_scenes.scene_12_sin_cos", "Scene12SinCos", "Cos and sin components, signs, 10 at 30°, atan2 trap"),
    "scene_13": ("manim_scenes.scene_13_component_sum", "Scene13ComponentSum", "(4,3) + (-2,5) one axis at a time"),
    "scene_14": ("manim_scenes.scene_14_position", "Scene14Position", "Position vectors; moving the origin keeps delta r"),
    "scene_15": ("manim_scenes.scene_15_velocity", "Scene15Velocity", "Chord to tangent; components; roundabout"),
    "scene_16": ("manim_scenes.scene_16_acceleration", "Scene16Acceleration", "Four cars: speed up, brake, turn, both"),
    "scene_17": ("manim_scenes.scene_17_equations", "Scene17Equations", "v-t graph area; three equations; x and y columns"),
    "scene_18": ("manim_scenes.scene_18_projectile", "Scene18Projectile", "Gravity only: a = -g j on a 3D flight"),
    "scene_19": ("manim_scenes.scene_19_launch", "Scene19Launch", "20 m/s at 45°: components 14.14 and 14.14"),
    "scene_20": ("manim_scenes.scene_20_horizontal", "Scene20Horizontal", "Floor shadow strobe: x = 14.14 t"),
    "scene_21": ("manim_scenes.scene_21_vertical", "Scene21Vertical", "Wall shadow, v_y shrinking and growing (3D)"),
    "scene_22": ("manim_scenes.scene_22_top", "Scene22Top", "Frozen at the top: v_y = 0, v_x = 14.14, a = g"),
    "scene_23": ("manim_scenes.scene_23_parabola", "Scene23Parabola", "Space-time curve (3D) and eliminating t"),
    "scene_24": ("manim_scenes.scene_24_time_height", "Scene24TimeHeight", "T = 2 v0 sin / g = 2.89 s; H = 10.20 m"),
    "scene_25": ("manim_scenes.scene_25_range", "Scene25Range", "R = v0^2 sin 2θ / g = 40.82 m"),
    "scene_26": ("manim_scenes.scene_26_best_angle", "Scene26BestAngle", "Fan of angles (3D); 30/60 twins; drag and a ledge"),
    "scene_27": ("manim_scenes.scene_27_challenges", "Scene27Challenges", "Five conceptual questions with countdowns"),
    "scene_28": ("manim_scenes.scene_28_synthesis", "Scene28Synthesis", "Motion → prediction; circular motion teaser"),
    "scene_29": ("manim_scenes.scene_29_subscribe", "Scene29Subscribe", "Subscribe card"),
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
        ["-m", "utils.motion_data"],
        ["-m", "utils.visual_contract_audit"],
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
