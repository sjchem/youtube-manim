"""Command-line entry point for 'Circular Motion'.

Examples:
    python main.py list                 # scene list with timestamps
    python main.py chapters             # the seven YouTube chapter markers
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
    "scene_01": ("manim_scenes.scene_01_hook", "Scene01Hook", "Straight road vs circular track (3D), one speedometer; title"),
    "scene_02": ("manim_scenes.scene_02_acceleration", "Scene02Acceleration", "a = dv/dt; magnitude, direction, or both"),
    "scene_03": ("manim_scenes.scene_03_speed_velocity", "Scene03SpeedVelocity", "5 i and 5 j: same speed, delta v ≈ 7.07 m/s"),
    "scene_04": ("manim_scenes.scene_04_tangent", "Scene04Tangent", "Velocity along the tangent, perpendicular to r (3D)"),
    "scene_05": ("manim_scenes.scene_05_components", "Scene05Components", "r cos θ i + r sin θ j; space-time helix (3D); v = r|ω|"),
    "scene_06": ("manim_scenes.scene_06_one_lap", "Scene06OneLap", "One lap (3D): distance 2πr, displacement 0"),
    "scene_07": ("manim_scenes.scene_07_delta_v", "Scene07DeltaV", "Δv between nearby moments swings to the centre"),
    "scene_08": ("manim_scenes.scene_08_velocity_triangle", "Scene08VelocityTriangle", "Velocity circle; |Δv| = 2v sin(Δθ/2) ≈ vΔθ"),
    "scene_09": ("manim_scenes.scene_09_derivation", "Scene09Derivation", "a = v²/r, two ways; 4²/2 = 8 m/s²"),
    "scene_10": ("manim_scenes.scene_10_speed_radius", "Scene10SpeedRadius", "Double v: ×4; double r: ×½ (3D tracks)"),
    "scene_11": ("manim_scenes.scene_11_falling_around", "Scene11FallingAround", "Newton's coast-and-nudge polygon; a = −ω² r"),
    "scene_12": ("manim_scenes.scene_12_radians", "Scene12Radians", "Radius laid on the arc; s = rθ; 2π rad; signs"),
    "scene_13": ("manim_scenes.scene_13_angular_velocity", "Scene13AngularVelocity", "ω = dθ/dt; v = r|ω|; 3D turntable, 2 and 4 m/s"),
    "scene_14": ("manim_scenes.scene_14_period", "Scene14Period", "T = π s ≈ 3.14 s, f ≈ 0.318 Hz, ω = 2πf"),
    "scene_15": ("manim_scenes.scene_15_angular_accel", "Scene15AngularAccel", "α = dω/dt; α = 0 but a_c = 8 m/s²"),
    "scene_16": ("manim_scenes.scene_16_centripetal_force", "Scene16CentripetalForce", "F = mv²/r = 16 N; a job, not a new force"),
    "scene_17": ("manim_scenes.scene_17_string", "Scene17String", "Ball on a string (3D); the string snaps: tangent"),
    "scene_18": ("manim_scenes.scene_18_car_friction", "Scene18CarFriction", "Flat curve (3D): v_max = √(μgr) ≈ 17.15 m/s"),
    "scene_19": ("manim_scenes.scene_19_satellite", "Scene19Satellite", "Newton's cannon round a 3D Earth; v = √(GM/r)"),
    "scene_20": ("manim_scenes.scene_20_centrifugal", "Scene20Centrifugal", "Inertial vs rotating frame; fictitious mω²r"),
    "scene_21": ("manim_scenes.scene_21_uniform", "Scene21Uniform", "Uniform circular motion: radial only"),
    "scene_22": ("manim_scenes.scene_22_nonuniform", "Scene22Nonuniform", "Speeding up (3D): a_r = 8, a_t = 1, |a| ≈ 8.06"),
    "scene_23": ("manim_scenes.scene_23_table", "Scene23Table", "Speed, direction, or both: the four cases"),
    "scene_24": ("manim_scenes.scene_24_challenges", "Scene24Challenges", "Five conceptual questions with countdowns"),
    "scene_25": ("manim_scenes.scene_25_synthesis", "Scene25Synthesis", "Direction → velocity → acceleration → force"),
    "scene_26": ("manim_scenes.scene_26_subscribe", "Scene26Subscribe", "Subscribe card"),
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
        ["-m", "utils.circle_data"],
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
