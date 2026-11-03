"""Check title lifetimes and the physics represented by moving arrows/clocks."""

from __future__ import annotations

import numpy as np
from manim import FadeIn, FadeOut, Scene

import config as cfg
from manim_scenes.common import Flight, SideFlight, field_stage, fly_together, heading, plane, prepare_scene
from manim_scenes.scene_15_velocity import road, road_velocity
from utils import physics_models as pm
from utils.layout_audit import _invisible
from utils.timing_audit import TimingRenderer


def check_titles() -> None:
    probe = Scene(renderer=TimingRenderer())
    prepare_scene(probe)
    sample = heading("Vectors")
    probe.add(sample)
    intro = FadeIn(sample)
    intro.begin()
    intro.update_mobjects(0.1)
    assert _invisible(intro.starting_mobject), "Hidden animation copies must stay hidden"
    intro.interpolate(0.25)
    fill = max(glyph.get_fill_opacity() for glyph in sample.family_members_with_points())
    assert 0 < fill < 1, "FadeIn must interpolate smoothly, rather than snap on"
    intro.finish()

    scene = Scene(renderer=TimingRenderer())
    prepare_scene(scene)
    title = heading("Vectors")
    scene.play(FadeIn(title), run_time=0.6)
    assert not _invisible(title), "Opening title must be readable"
    scene.wait(cfg.TIMING["title_hold"] - 0.6 + cfg.TIMING["title_fade"] / 2)
    assert 0 < title._title_alpha < 1, "Title must fade gradually during a hold"
    scene.wait(cfg.TIMING["title_fade"])
    assert _invisible(title), "Title must expire without another narration beat"
    scene.play(FadeOut(title), run_time=0.4)
    # Existing scenes still refer to their heading at later transitions.
    scene.add(title)
    scene.update_mobjects(0)
    assert _invisible(title), "A later transition must not resurrect the title"


def check_comparison_clocks() -> None:
    for projected in (False, True):
        stage = field_stage() if projected else None
        grid = None if projected else plane((0, 45), (0, 20), unit=0.1, labels=False)
        flights = [Flight(stage, model) if projected else SideFlight(grid, model)
                   for model in (pm.TABLE[0], pm.TABLE[2])]
        animation = fly_together(flights, run_time=3.0)
        animation.begin()
        for alpha in (0.0, 0.25, 0.5, 0.75, 1.0):
            animation.interpolate(alpha)
            elapsed = alpha * pm.TABLE[2].flight_time
            actual = [f.t if projected else f.clock.value for f in flights]
            expected = [min(elapsed, f.model.flight_time) for f in flights]
            assert np.allclose(actual, expected), (projected, alpha, actual, expected)
        animation.finish()


def check_velocity_magnitudes() -> None:
    # A numerical derivative independently checks that tangent arrows retain
    # the speed information, rather than normalising every arrow to one size.
    for u in (0.05, 0.4, 0.95):
        du = 1e-6
        numerical = (road(u + du) - road(u - du)) / (20 * du)
        assert np.allclose(road_velocity(u), numerical, atol=1e-8)
    assert not np.isclose(np.linalg.norm(road_velocity(0.05)), np.linalg.norm(road_velocity(0.4)))


def main() -> int:
    for check in (check_titles, check_comparison_clocks, check_velocity_magnitudes):
        check()
        print(f"PASS: {check.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
