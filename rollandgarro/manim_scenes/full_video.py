"""Render all red clay tennis scenes together from the scene modules."""

from manim import FadeOut

from manim_scenes.common import RedClayScene
from manim_scenes.scene_01_opening import OpeningHookScene
from manim_scenes.scene_02_air_forces import AirForcesScene
from manim_scenes.scene_03_spin_trajectory import SpinTrajectoryScene
from manim_scenes.scene_04_equation_build import EquationBuildScene
from manim_scenes.scene_05_bounce_physics import BouncePhysicsScene
from manim_scenes.scene_06_clay_friction import ClayFrictionScene
from manim_scenes.scene_07_rally_geometry import RallyGeometryScene
from manim_scenes.scene_08_living_clay import LivingClayCourtScene
from manim_scenes.scene_09_final_summary import FinalSummaryScene


SCENE_TIMELINE = [
    (OpeningHookScene, 28),
    (AirForcesScene, 30),
    (SpinTrajectoryScene, 30),
    (EquationBuildScene, 30),
    (BouncePhysicsScene, 30),
    (ClayFrictionScene, 30),
    (RallyGeometryScene, 28),
    (LivingClayCourtScene, 28),
    (FinalSummaryScene, 24),
]


class PreviewCompositeScene(RedClayScene):
    """Fast structural render for checking every scene together."""

    def construct(self):
        for scene_cls, _target_duration in SCENE_TIMELINE:
            scene_cls.construct(self)
            self.play(FadeOut(*self.mobjects), run_time=0.35)


class FinalCompositeScene(RedClayScene):
    """Narration-paced full render, targeted at roughly 4.5 minutes."""

    def construct(self):
        for scene_cls, target_duration in SCENE_TIMELINE:
            start_time = self.time
            scene_cls.construct(self)
            elapsed = self.time - start_time
            remaining = max(0, target_duration - elapsed)
            if remaining > 0:
                self.wait(remaining)
            self.play(FadeOut(*self.mobjects), run_time=0.35)
