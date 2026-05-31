"""Convenience helpers for rendering all scenes in order."""

SCENE_ORDER = [
    ("manim_scenes/scene_01_opening.py", "OpeningHookScene"),
    ("manim_scenes/scene_02_air_forces.py", "AirForcesScene"),
    ("manim_scenes/scene_03_spin_trajectory.py", "SpinTrajectoryScene"),
    ("manim_scenes/scene_04_equation_build.py", "EquationBuildScene"),
    ("manim_scenes/scene_05_bounce_physics.py", "BouncePhysicsScene"),
    ("manim_scenes/scene_06_clay_friction.py", "ClayFrictionScene"),
    ("manim_scenes/scene_07_rally_geometry.py", "RallyGeometryScene"),
    ("manim_scenes/scene_08_living_clay.py", "LivingClayCourtScene"),
    ("manim_scenes/scene_09_final_summary.py", "FinalSummaryScene"),
]


def print_render_commands(quality: str = "-pqh") -> None:
    for file_name, scene_name in SCENE_ORDER:
        print(f"manim {quality} {file_name} {scene_name}")
