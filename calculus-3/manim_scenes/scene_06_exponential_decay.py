"""Scene 06: flip one sign, and the same equation runs the world backwards."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    calc_axes,
    chip,
    dashed_connector,
    end_scene,
    eq,
    fitted_eq,
    glow_dot,
    labelled_axes,
    live_readout,
    narration_wait,
    outlined_text,
    paced_play,
    particle_cloud,
)
from utils.math_utils import (
    DECAY_HALF_LIFE,
    DECAY_RATE,
    exponential_decay,
    half_life,
)

PARTICLE_TOTAL = 60
WATCH_SPAN = 3 * DECAY_HALF_LIFE


class Scene06ExponentialDecay(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "06")
    add_cinematic_background(scene)

    # -- Beat 1: one character changes ---------------------------------------
    growth_eq = fitted_eq(r"\frac{dP}{dt}=+kP", cfg.GREEN, cfg.FONT["title"], width=5.2)
    decay_eq = fitted_eq(r"\frac{dN}{dt}=-kN", cfg.ORANGE, cfg.FONT["title"], width=5.2)
    pair = VGroup(growth_eq, decay_eq).arrange(RIGHT, buff=1.5).move_to([0, 0.85, 0])
    versus = outlined_text("vs", cfg.FONT["body"], cfg.MUTED).move_to(pair.get_center())

    paced_play(scene, FadeIn(growth_eq), run_time=0.9)
    paced_play(scene, FadeIn(versus), TransformFromCopy(growth_eq, decay_eq), run_time=1.4)
    sign = SurroundingRectangle(decay_eq, color=cfg.RED, buff=0.26, corner_radius=0.14, stroke_width=3.5)
    paced_play(scene, Create(sign), run_time=0.8)
    narration_wait(scene, 9.5)

    note = outlined_text("the bigger it is, the faster it disappears", cfg.FONT["body"], cfg.ORANGE)
    note.next_to(pair, DOWN, buff=0.85)
    paced_play(scene, FadeIn(note, shift=UP * 0.12), run_time=0.9)
    narration_wait(scene, 6.8)
    paced_play(scene, FadeOut(VGroup(growth_eq, versus, note, sign)), decay_eq.animate.scale(0.72).to_corner(UL, buff=0.5), run_time=1.0)

    # -- Beat 2: particles leaving, quickly then slowly ------------------------
    clock = ValueTracker(0.0)
    particles = particle_cloud(PARTICLE_TOTAL, 3.1, 3.0, cfg.PURPLE, cfg.SEED + 7, radius=0.085)
    particles.move_to([-4.15, -0.35, 0])
    for index, dot in enumerate(particles):
        # The (index+1)-th particle leaves exactly when the exact solution
        # N(t) = N0 e^{-kt} first drops below the number still present.
        expiry = float(np.log(PARTICLE_TOTAL / (index + 0.5)) / DECAY_RATE)

        def fade(mob: Mobject, moment: float = expiry) -> None:
            mob.set_opacity(1.0 if clock.get_value() < moment else 0.0)

        dot.add_updater(fade)
    paced_play(scene, LaggedStart(*(FadeIn(dot, scale=1.4) for dot in particles), lag_ratio=0.012), run_time=1.8)

    axes = calc_axes((0, WATCH_SPAN, DECAY_HALF_LIFE), (0, 70, 30), 7.0, 4.6).move_to([2.15, -0.35, 0])
    axis_labels = labelled_axes(axes, "t", "N", cfg.MUTED, cfg.FONT["small"])
    curve = axes.plot(lambda t: exponential_decay(t, PARTICLE_TOTAL), x_range=[0, WATCH_SPAN], color=cfg.ORANGE, stroke_width=7)
    guide_curve = curve.copy().set_stroke(opacity=0.16)
    tracer = always_redraw(lambda: glow_dot(axes.c2p(clock.get_value(), exponential_decay(clock.get_value(), PARTICLE_TOTAL)), cfg.GOLD, 0.09))
    drawn = always_redraw(
        lambda: axes.plot(lambda t: exponential_decay(t, PARTICLE_TOTAL), x_range=[0, max(clock.get_value(), 0.01)], color=cfg.ORANGE, stroke_width=7)
    )
    counter = live_readout(
        "N=",
        lambda: exponential_decay(clock.get_value(), PARTICLE_TOTAL),
        cfg.WHITE,
        cfg.FONT["body"],
        decimal_places=0,
    ).move_to([-4.15, 1.85, 0])
    paced_play(scene, Create(axes), FadeIn(axis_labels), Create(guide_curve), run_time=1.0)
    scene.add(drawn, tracer, counter)
    paced_play(scene, clock.animate.set_value(WATCH_SPAN), run_time=9.0, rate_func=linear)
    narration_wait(scene, 9.2)

    # -- Beat 3: the half-life, read straight off the curve --------------------
    marks = VGroup()
    for step in (1, 2, 3):
        moment = step * DECAY_HALF_LIFE
        level = exponential_decay(moment, PARTICLE_TOTAL)
        marks.add(dashed_connector(axes.c2p(moment, 0), axes.c2p(moment, level), cfg.MUTED, 9, 2.2))
        marks.add(dashed_connector(axes.c2p(0, level), axes.c2p(moment, level), cfg.MUTED, 12, 2.2))
    half_tag = fitted_eq(
        rf"t_{{1/2}}=\frac{{\ln 2}}{{k}}={half_life():.0f}",
        cfg.PURPLE,
        cfg.FONT["hero"],
        width=6.4,
    )
    half_tag.next_to(axes, UP, buff=0.36)
    paced_play(scene, Create(marks), run_time=1.6)
    paced_play(scene, FadeIn(half_tag, shift=UP * 0.12), run_time=0.9)
    narration_wait(scene, 9.4)

    solution = fitted_eq(r"N(t)=N_0e^{-kt}", cfg.ORANGE, cfg.FONT["section"], width=5.6)
    solution.next_to(axes, DOWN, buff=0.30)
    paced_play(scene, FadeIn(solution, shift=UP * 0.1), run_time=1.0)
    narration_wait(scene, 6.2)

    # -- Beat 4: the same curve, three different worlds -------------------------
    for dot in particles:
        dot.clear_updaters()
    counter.clear_updaters()
    scene.remove(drawn, tracer, counter)
    paced_play(scene, FadeOut(VGroup(particles, axes, axis_labels, guide_curve, marks, half_tag, solution, decay_eq)), run_time=0.8)

    examples = VGroup(
        chip("radioactive atoms", cfg.PURPLE, cfg.FONT["small"]),
        chip("a cooling object", cfg.ORANGE, cfg.FONT["small"]),
        chip("medicine in the blood", cfg.CYAN, cfg.FONT["small"]),
    ).arrange(DOWN, buff=0.48).move_to([0, 0.55, 0])
    paced_play(scene, LaggedStart(*(FadeIn(item, shift=RIGHT * 0.15) for item in examples), lag_ratio=0.35), run_time=2.4)
    narration_wait(scene, 8.5)

    verdict = bottom_caption("Same structure. Opposite worlds. One sign apart.", cfg.WHITE)
    paced_play(scene, FadeIn(verdict), run_time=0.9)
    narration_wait(scene, 5.8)

    end_scene(scene, started, cfg.SCENE_DURATIONS["06"])
