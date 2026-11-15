"""Command-line entry point for 'System of Particles & Rotational Motion'.

Examples:
    python main.py list                 # scene list with timestamps
    python main.py chapters             # the eleven YouTube chapter markers
    python main.py preview 11           # fast 480p15 preview of one scene
    python main.py scene 11             # one scene at full quality (1080p30)
    python main.py preview all          # every scene as separate previews
    python main.py preview full         # the whole film at preview quality
    python main.py render               # the whole film at 1080p30
    python main.py check                # model + spoken numbers + narration + timing + layout audits
    python main.py export               # narration scripts, ElevenLabs text and cue sheets
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
    "scene_01": ("manim_scenes.scene_01_hook", "Scene01Hook", "One push (3D): a box slides, a door swings, a cylinder rolls; title"),
    "scene_02": ("manim_scenes.scene_02_rigid_bodies", "Scene02RigidBodies", "Point vs wheel (3D); rigid links; translation, rotation, rolling"),
    "scene_03": ("manim_scenes.scene_03_two_masses", "Scene03TwoMasses", "Balance a light rod (3D); x_cm formula; 2 kg at 0, 6 kg at 4 m → 3 m"),
    "scene_04": ("manim_scenes.scene_04_where_com", "Scene04WhereCom", "Sphere, disc, rod, hammer, ring (3D); a tossed hammer's centre on a parabola"),
    "scene_05": ("manim_scenes.scene_05_many_particles", "Scene05ManyParticles", "3D cloud: R_cm = Σ m_i r_i / M; origin-free; solid → ∫ r dm"),
    "scene_06": ("manim_scenes.scene_06_internal_forces", "Scene06InternalForces", "Spring cluster: third-law pairs cancel; F_ext = M a_cm, live"),
    "scene_07": ("manim_scenes.scene_07_firework", "Scene07Firework", "Exploding shell (3D): fragments' centre rides the parabola"),
    "scene_08": ("manim_scenes.scene_08_momentum", "Scene08Momentum", "P = M v_cm; carts 2 kg × 3, 3 kg × −1 → 0.6 m/s through a collision"),
    "scene_09": ("manim_scenes.scene_09_cross_product", "Scene09CrossProduct", "A × B (3D): parallelogram area, right-hand rule, θ sweep, B × A = −A × B"),
    "scene_10": ("manim_scenes.scene_10_angular_velocity", "Scene10AngularVelocity", "ω along the axis (3D turntable); v = ω × r at three radii"),
    "scene_11": ("manim_scenes.scene_11_torque_door", "Scene11TorqueDoor", "3D door: τ = r × F, lever arm; 20 N at 0.8 m → 16, at 0.2 m → 4 N m"),
    "scene_12": ("manim_scenes.scene_12_couple", "Scene12Couple", "A couple (3D bar): ΣF = 0, τ = F d, spin in place"),
    "scene_13": ("manim_scenes.scene_13_equilibrium", "Scene13Equilibrium", "3D seesaw: 100 N × 2 m = 200 N × 1 m; pivot 300 N; then it tips"),
    "scene_14": ("manim_scenes.scene_14_inertia", "Scene14Inertia", "Ring vs disc spin-up (3D); I = Σ m r²; dumbbell 2 → 8 kg m²"),
    "scene_15": ("manim_scenes.scene_15_shapes", "Scene15Shapes", "Three 3D shape comparisons with names and I; coefficient bars; ring = 2 × disc"),
    "scene_16": ("manim_scenes.scene_16_gyration", "Scene16Gyration", "Disc → equivalent ring at k = R/√2 ≈ 0.71 R (3D)"),
    "scene_17": ("manim_scenes.scene_17_axis_theorems", "Scene17AxisTheorems", "Rod axis slides to the end: 1/12 + 1/4 = 1/3; disc I_z = I_x + I_y"),
    "scene_18": ("manim_scenes.scene_18_angular_equations", "Scene18AngularEquations", "x, v, a → θ, ω, α; the three constant-α equations"),
    "scene_19": ("manim_scenes.scene_19_spin_up", "Scene19SpinUp", "Wheel from rest at 2 rad/s² for 4 s (3D, live): 8 rad/s, 16 rad, 2.55 rev"),
    "scene_20": ("manim_scenes.scene_20_particle_motion", "Scene20ParticleMotion", "Three radii: v = rω, a_t = rα, a_r = rω² (live arrows)"),
    "scene_21": ("manim_scenes.scene_21_tau_i_alpha", "Scene21TauIAlpha", "F_t = m r α → τ = m r² α → Σ: τ_net = I α"),
    "scene_22": ("manim_scenes.scene_22_disc", "Scene22Disc", "4 kg, 0.5 m disc on an axle (3D): I = 0.5, τ = 1 N m → α = 2"),
    "scene_23": ("manim_scenes.scene_23_energy", "Scene23Energy", "Σ ½ m v² → ½ I ω²; 16 J = W = τ Δθ; P = τ ω"),
    "scene_24": ("manim_scenes.scene_24_angular_momentum", "Scene24AngularMomentum", "L = r × p (3D); straight line, circle, rigid body; τ = dL/dt"),
    "scene_25": ("manim_scenes.scene_25_skater", "Scene25Skater", "3D skater: I 4 → 2, ω 2 → 4, L = 8; K 8 → 16 J"),
    "scene_26": ("manim_scenes.scene_26_rolling", "Scene26Rolling", "Rolling wheel (3D): v_cm + ωR; top 2v, contact 0; cycloid"),
    "scene_27": ("manim_scenes.scene_27_rolling_energy", "Scene27RollingEnergy", "K = ½Mv²(1 + I/MR²); energy shares ⅓ vs ½"),
    "scene_28": ("manim_scenes.scene_28_race", "Scene28Race", "3D ramp race: block, cylinder, ring; 4.9, 3.27, 2.45 m/s²"),
    "scene_29": ("manim_scenes.scene_29_synthesis", "Scene29Synthesis", "Translation ↔ rotation, pair by pair; the core message"),
    "scene_30": ("manim_scenes.scene_30_subscribe", "Scene30Subscribe", "Subscribe card"),
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
    print("─" * 118)
    starts = scene_starts()
    for key, (_, class_name, title) in SCENE_MAP.items():
        number = key[-2:]
        print(f"{key:<10} {_stamp(starts[number]):>6}  {class_name:<26} {cfg.SCENE_DURATIONS[number]:>5.0f}s  {title}")
    total = sum(cfg.SCENE_DURATIONS.values())
    print("─" * 118)
    print(f"{'FullVideo':<10} {'':>6}  {'FullVideo':<26} {total:>5.0f}s  ({_stamp(total)})\n")


def list_chapters() -> None:
    starts = scene_starts()
    for first, title in cfg.YOUTUBE_CHAPTERS:
        print(f"{_stamp(starts[first])} {title}")


def run_checks() -> int:
    steps = [
        ["-m", "utils.math_utils"],
        ["-m", "utils.physics_models"],
        ["-m", "utils.rotation_data"],
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
    if command == "export":
        return subprocess.run([sys.executable, "-m", "utils.narration_export", *args[1:]], cwd=PROJECT_ROOT,
                              check=False).returncode
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
