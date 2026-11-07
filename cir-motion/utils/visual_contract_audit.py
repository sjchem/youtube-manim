"""Check title lifetimes and the physics the moving pictures claim.

* titles fade in smoothly, expire after their hold, and stay expired;
* comparison circuits advance on one shared physical clock;
* drawn velocity arrows are the numerical derivative of the drawn position
  (tangent, perpendicular to r) at their true length, and drawn acceleration
  arrows point at the centre at their true length, in 2D and on the 3D stage;
* the centrifugal scene's passenger coasts in a straight line until the door
  reaches it, then turns with the car;
* the skidding car of scene 18 follows a circle no tighter than friction allows.

    python -m utils.visual_contract_audit
"""

from __future__ import annotations

import numpy as np
from manim import FadeIn, FadeOut, Scene

import config as cfg
from manim_scenes.common import CircleView, Circuit, field_stage, ground_vec, heading, prepare_scene, run_together
from utils import physics_models as pm
from utils.layout_audit import _invisible
from utils.timing_audit import TimingRenderer
from manim_scenes.stage3d import Vector

P = pm.REFERENCE


def check_titles() -> None:
    probe = Scene(renderer=TimingRenderer())
    prepare_scene(probe)
    sample = heading("Angular velocity")
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
    title = heading("Angular velocity")
    scene.play(FadeIn(title), run_time=0.6)
    assert not _invisible(title), "Opening title must be readable"
    scene.wait(cfg.TIMING["title_hold"] - 0.6 + cfg.TIMING["title_fade"] / 2)
    assert 0 < title._title_alpha < 1, "Title must fade gradually during a hold"
    scene.wait(cfg.TIMING["title_fade"])
    assert _invisible(title), "Title must expire without another narration beat"
    scene.play(FadeOut(title), run_time=0.4)
    scene.add(title)
    scene.update_mobjects(0)
    assert _invisible(title), "A later transition must not resurrect the title"


def check_shared_clocks() -> None:
    stage = field_stage()
    slow = Circuit(stage, P, R=1.5)
    fast = Circuit(stage, pm.DOUBLE_SPEED, R=1.5)
    flat = CircleView(np.zeros(3), 1.0, pm.DOUBLE_RADIUS)
    fast.t, flat.clock.value = 0.3, 0.1
    animation = run_together(stage, [slow, fast, flat], 2.0, run_time=4.0)
    animation.begin()
    for alpha in (0.0, 0.3, 0.7, 1.0):
        animation.interpolate(alpha)
        elapsed = 2.0 * alpha
        assert np.allclose([slow.t, fast.t, flat.clock.value], [elapsed, 0.3 + elapsed, 0.1 + elapsed]), alpha
    animation.finish()


def check_flat_arrows() -> None:
    for model in (P, pm.DOUBLE_SPEED, pm.SpeedingUp(P.r, P.angular_speed, pm.ALPHA)):
        view = CircleView(np.array([1.0, -0.5, 0.0]), 2.0, model)
        scale = view.R / view.r_m                       # screen units per metre
        for when in (0.0, 0.37, 1.9):
            view.clock.value = when
            v, a = view.arrow("v", live=False), view.arrow("a", live=False)
            drawn_v = v.tip() - v.tail()
            h = 1e-6
            numerical = (view.point(when + h) - view.point(when - h)) / (2 * h) / scale
            assert np.allclose(drawn_v / view.kv, numerical, atol=1e-5), "velocity arrow = d(position)/dt"
            assert abs(np.dot(drawn_v, view.point() - view.c)) < 1e-9, "velocity is perpendicular to r"
            drawn_a = a.tip() - a.tail()
            speed = np.linalg.norm(numerical)
            assert np.isclose(np.linalg.norm(drawn_a) / view.ka, speed ** 2 / view.r_m), "|a| arrow = v^2 / r"
            assert np.allclose(mu_unit(drawn_a), mu_unit(view.c - view.point())), "a points at the centre"
            if getattr(model, "alpha", 0.0):
                at = view.arrow("at", live=False)
                drawn_t = at.tip() - at.tail()
                assert np.isclose(np.linalg.norm(drawn_t) / view.ka, view.r_m * model.alpha), "a_t arrow = r alpha"
                assert abs(np.dot(drawn_t, drawn_a)) < 1e-9, "radial and tangential parts are perpendicular"


def mu_unit(v: np.ndarray) -> np.ndarray:
    return v / np.linalg.norm(v)


def check_stage_arrows() -> None:
    stage = field_stage()
    c = Circuit(stage, P, R=2.0, kv=0.3, ka=0.1)
    v, a = c.add_arrow("v"), c.add_arrow("a")
    s = 2.0 / P.r                                    # stage units per metre
    for when in (0.2, 1.1):
        c.t = when
        h = 1e-6
        numerical = (c.world(when + h) - c.world(when - h)) / (2 * h) / s
        drawn = np.asarray(v.end()) - np.asarray(v.start())
        assert np.allclose(drawn / c.kv, numerical, atol=1e-5), "3D velocity arrow = d(position)/dt"
        inward = c.centre + np.array([0, c.height, 0]) - c.world()
        drawn_a = np.asarray(a.end()) - np.asarray(a.start())
        assert np.allclose(mu_unit(drawn_a), mu_unit(inward)), "3D acceleration points at the centre"
        assert np.isclose(np.linalg.norm(drawn_a) / c.ka, P.accel), "3D |a| arrow = v^2 / r"
    assert np.allclose(ground_vec([1, 0]), [1, 0, 0]) and np.allclose(ground_vec([0, 1]), [0, 0, -1]), "north runs away"


def check_centrifugal_ride() -> None:
    from manim_scenes.scene_20_centrifugal import DOOR, Ride

    ride = Ride()
    assert 0 < ride.t_contact < 3.0, "the door must reach the passenger"
    # Before contact the ground-frame path is a straight line at the starting velocity.
    for when in np.linspace(0, ride.t_contact * 0.99, 7):
        assert np.allclose(ride.passenger(when), ride.start + ride.v0 * when), "inertia: straight on"
    assert np.isclose(ride.free_rel(ride.t_contact)[1], -DOOR, atol=2e-3), "contact happens at the outer door"
    # After contact the passenger keeps the same place in the car (turns with it).
    later = ride.t_contact + 1.3
    assert np.allclose(ride.rel(later), ride.rel_contact), "after contact the door carries the passenger round"
    assert ride.rel_contact[1] < 0, "the passenger ends up on the outer side"


def check_arrow_halos() -> None:
    """Projection updates must preserve the requested halo visibility."""
    stage = field_stage()
    rotation = np.eye(3)
    for glow in (False, True):
        arrow = Vector(np.zeros(3), np.array([1.0, 0.0, 0.0]), cfg.VELOCITY, glow=glow)
        arrow.place(stage, rotation, 1.0)
        base = arrow.halo.get_fill_opacity()
        assert (base > 0) if glow else (base == 0), "projection must respect the requested glow setting"
        for visibility in (0.3, 0.0):
            arrow.place(stage, rotation, visibility)
            expected = base * visibility
            assert np.isclose(arrow.halo.get_fill_opacity(), expected), "hidden halos must not reappear during projection"


def check_skid() -> None:
    rho = pm.widest_bend_radius(pm.FAST_SPEED)
    assert np.isclose(pm.FAST_SPEED ** 2 / rho, pm.max_friction_accel()), "skid circle uses all the friction"
    assert rho > pm.CURVE_RADIUS, "the fast car's path is wider than the road"


def main() -> int:
    for check in (check_titles, check_shared_clocks, check_flat_arrows, check_stage_arrows, check_arrow_halos, check_centrifugal_ride, check_skid):
        check()
        print(f"PASS: {check.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
