"""Scene 13: a local rule becomes a slope field, a trajectory, and then a world."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    calc_axes,
    end_scene,
    eq,
    fitted_eq,
    glow_dot,
    hide_background,
    labelled_axes,
    narration_wait,
    orbit_hold,
    orbit_path,
    outlined_text,
    paced_play,
    pin_to_frame,
    restore_background,
    set_3d_view,
    slope_field,
    solution_curve,
    three_d_axes,
)
from utils.math_utils import (
    LOGISTIC_CAPACITY,
    logistic_slope,
    logistic_solution,
    spring_position,
)
from utils.physics_models import CoolingCup, OrbitingBody, SpringOscillator

START_VALUE = 0.25
PLANET = OrbitingBody(mu=1.0, start_radius=2.0, start_speed=0.62)
ORBIT_SECONDS = 13.0


def _mini_panel(title: str, colour: str, plot: callable, x_max: float, y_range: tuple[float, float]) -> VGroup:
    """A small labelled graph used in the closing montage."""
    axes = calc_axes((0, x_max, x_max / 2), (y_range[0], y_range[1], (y_range[1] - y_range[0]) / 2), 4.5, 2.2)
    axes.set_stroke(opacity=0.65)
    curve = axes.plot(plot, x_range=[0, x_max], color=colour, stroke_width=5)
    label = outlined_text(title, cfg.FONT["small"], colour)
    panel = VGroup(axes, curve)
    label.next_to(panel, UP, buff=0.18)
    return VGroup(panel, label)


class Scene13EquationToFuture(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "13")
    background = add_cinematic_background(scene)

    # -- Beat 1: the general shape of every equation in this film -------------
    general = fitted_eq(r"\frac{dy}{dt}=f(y,t)", cfg.WHITE, cfg.FONT["hero"], width=7.4).move_to([0, 0.6, 0])
    paced_play(scene, Write(general), run_time=1.5)
    narration_wait(scene, 8.6)

    # -- Beat 2: it becomes a field, then a single future ----------------------
    logistic_rule = fitted_eq(
        r"\frac{dy}{dt}=ry\!\left(1-\frac{y}{K}\right)", cfg.PURPLE, cfg.FONT["section"], width=5.2
    ).to_corner(UL, buff=0.5)
    paced_play(scene, ReplacementTransform(general, logistic_rule), run_time=1.2)
    axes = calc_axes((0, 8, 2), (0, 3.6, 1), 9.6, 5.2).move_to([-0.4, -0.35, 0])
    axis_labels = labelled_axes(axes, "t", "y", cfg.MUTED, cfg.FONT["small"])
    paced_play(scene, Create(axes), FadeIn(axis_labels), run_time=1.0)

    rows = slope_field(axes, lambda t, y: logistic_slope(t, y), (0.3, 7.7, 0.55), (0.15, 3.45, 0.3), half_length=0.19)
    field = VGroup(*rows)
    paced_play(scene, LaggedStart(*(FadeIn(row) for row in rows), lag_ratio=0.30), run_time=3.6)
    narration_wait(scene, 8.5)

    seed = glow_dot(axes.c2p(0, START_VALUE), cfg.GOLD, 0.11)
    seed_tag = eq(r"y(0)", cfg.GOLD, cfg.FONT["small"]).next_to(axes.c2p(0, START_VALUE), LEFT, buff=0.24)
    paced_play(scene, FadeIn(seed, scale=1.5), FadeIn(seed_tag), run_time=0.9)
    narration_wait(scene, 6.0)

    future = solution_curve(axes, lambda t: logistic_solution(t, START_VALUE), 0.0, 8.0, cfg.GREEN, 8)
    rider = glow_dot(axes.c2p(0, START_VALUE), cfg.GREEN, 0.10)
    ceiling = DashedLine(axes.c2p(0, LOGISTIC_CAPACITY), axes.c2p(8, LOGISTIC_CAPACITY), color=cfg.MUTED, stroke_width=2.6, dash_length=0.14)
    grow_caption = bottom_caption("One rule, one starting point, one future.", cfg.GREEN)
    paced_play(scene, FadeIn(grow_caption), FadeIn(rider), run_time=0.7)
    paced_play(scene, Create(future), MoveAlongPath(rider, future), run_time=6.0, rate_func=rate_functions.ease_in_out_sine)
    paced_play(scene, Create(ceiling), run_time=0.8)
    narration_wait(scene, 8.4)

    paced_play(
        scene,
        FadeOut(VGroup(field, axes, axis_labels, seed, seed_tag, rider, ceiling, grow_caption, logistic_rule)),
        future.animate.set_stroke(opacity=0.0),
        run_time=0.9,
    )
    scene.remove(future)

    # -- Beat 3: the same shape, wearing four different costumes ---------------
    cup = CoolingCup()
    osc = SpringOscillator()
    panels = VGroup(
        _mini_panel("population", cfg.GREEN, lambda t: logistic_solution(t, START_VALUE), 8.0, (0.0, 3.5)),
        _mini_panel("cooling", cfg.ORANGE, cup.temperature, 40.0, (0.0, 100.0)),
        _mini_panel("oscillation", cfg.CYAN, spring_position, 3 * osc.period, (-2.0, 2.0)),
        _mini_panel("decay", cfg.PURPLE, lambda t: 100 * np.exp(-0.35 * t), 8.0, (0.0, 110.0)),
    )
    panels[0].move_to([-3.55, 1.75, 0])
    panels[1].move_to([3.55, 1.75, 0])
    panels[2].move_to([-3.55, -1.95, 0])
    panels[3].move_to([3.55, -1.95, 0])
    paced_play(scene, LaggedStart(*(FadeIn(panel, scale=1.06) for panel in panels), lag_ratio=0.35), run_time=3.6)
    narration_wait(scene, 9.4)
    paced_play(scene, FadeOut(panels), run_time=0.8)

    # -- Beat 4: numerical accumulation when algebra has no tidy answer -------
    update = fitted_eq(
        r"y_{n+1}=y_n+f(y_n,t_n)\,\Delta t",
        cfg.GOLD,
        cfg.FONT["title"],
        width=9.2,
    ).move_to([0, 0.75, 0])
    update_plate = SurroundingRectangle(update, color=cfg.GOLD, buff=0.34, corner_radius=0.18, stroke_width=3.5)
    update_note = outlined_text("state + current rate × tiny time step", cfg.FONT["body"], cfg.MUTED)
    update_note.next_to(update_plate, DOWN, buff=0.58)
    paced_play(scene, Write(update), Create(update_plate), run_time=1.5)
    paced_play(scene, FadeIn(update_note, shift=UP * 0.12), run_time=0.8)
    narration_wait(scene, 7.5)
    paced_play(scene, FadeOut(VGroup(update, update_plate, update_note)), run_time=0.7)

    # -- Beat 5: and the same idea, running a solar system ----------------------
    hide_background(scene)
    space = three_d_axes((-2.6, 2.6, 1), (-2.6, 2.6, 1), (-1.4, 1.4, 1), unit=1.15)
    space.set_stroke(opacity=0.35)
    trajectory = PLANET.trajectory(duration=ORBIT_SECONDS, dt=0.004)
    path = orbit_path(space, trajectory, cfg.CYAN, 4.5)
    star = VGroup(
        Dot3D(point=space.c2p(0, 0, 0), radius=0.30, color=cfg.GOLD),
        Circle(radius=0.55, color=cfg.GOLD, stroke_width=0, fill_color=cfg.GOLD, fill_opacity=0.10).move_to(space.c2p(0, 0, 0)),
    )
    planet = Dot3D(point=space.c2p(*trajectory[0], 0), radius=0.16, color=cfg.CYAN)
    law = fitted_eq(r"m\frac{d^2\vec{r}}{dt^2}=-\frac{GMm}{|\vec{r}|^{3}}\,\vec{r}", cfg.WHITE, cfg.FONT["section"], width=8.0).to_edge(UP, buff=0.40)
    orbit_state = fitted_eq(r"\vec r(0)=\vec r_0,\quad \vec v(0)=\vec v_0", cfg.GOLD, cfg.FONT["small"], width=5.5)
    orbit_state.next_to(law, DOWN, buff=0.28)

    set_3d_view(scene, phi=64 * DEGREES, theta=-72 * DEGREES)
    paced_play(scene, Create(space), FadeIn(star), FadeIn(planet, scale=1.5), run_time=1.4)
    pin_to_frame(scene, law, orbit_state)
    paced_play(scene, FadeIn(law, shift=DOWN * 0.12), FadeIn(orbit_state), run_time=1.0)
    paced_play(scene, MoveAlongPath(planet, path), Create(path), run_time=9.0, rate_func=linear)
    orbit_hold(scene, 5.4)

    paced_play(scene, FadeOut(VGroup(space, star, planet, path, law, orbit_state)), run_time=0.8)
    restore_background(scene, background)

    # -- Beat 6: the sentence this whole film is aiming at -----------------------
    verdict = fitted_eq(
        r"\text{local rule}\;\longrightarrow\;\text{global prediction}",
        cfg.GOLD,
        cfg.FONT["title"],
        width=11.4,
    )
    plate = SurroundingRectangle(verdict, color=cfg.GOLD, buff=0.34, corner_radius=0.18, stroke_width=3.5)
    paced_play(scene, Write(verdict), Create(plate), run_time=1.8)
    narration_wait(scene, 9.0)

    end_scene(scene, started, cfg.SCENE_DURATIONS["13"])
