"""Scene 02: differentiation forgets a constant, so integration has to guess."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    dashed_connector,
    end_scene,
    eq,
    fitted_eq,
    glow_dot,
    glow_line,
    labelled_axes,
    narration_wait,
    paced_play,
)
from utils.math_utils import parabola_slope, shifted_parabola

SHIFTS = (4.0, 0.0, -3.0)
SHIFT_COLORS = (cfg.GOLD, cfg.WHITE, cfg.CYAN)
SHIFT_LABELS = (r"y=x^2+4", r"y=x^2", r"y=x^2-3")
TANGENT_X = 1.15


class Scene02MissingConstant(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "02")
    add_cinematic_background(scene)

    axes = Axes(
        x_range=[-2.6, 2.6, 1],
        y_range=[-4, 9, 3],
        x_length=7.4,
        y_length=5.9,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.4},
    ).move_to([-3.5, -0.15, 0])
    # Large single-letter labels remain legible when the video is watched on a phone.
    axis_labels = labelled_axes(axes, "x", "y", cfg.MUTED, cfg.FONT["hero"])
    paced_play(scene, Create(axes), FadeIn(axis_labels), run_time=1.0)

    # -- Beat 1: one shape, three vertical homes ------------------------------
    curves = VGroup(
        *(
            axes.plot(lambda x, c=shift: shifted_parabola(x, c), x_range=[-2.45, 2.45], color=color, stroke_width=6)
            for shift, color in zip(SHIFTS, SHIFT_COLORS)
        )
    )
    tags = VGroup(*(eq(text, color, cfg.FONT["title"]) for text, color in zip(SHIFT_LABELS, SHIFT_COLORS)))
    tags.arrange(RIGHT, buff=0.48)
    if tags.width > 7.0:
        tags.scale_to_fit_width(7.0)
    tags.move_to([3.75, 1.55, 0])

    paced_play(scene, Create(curves[1]), FadeIn(tags[1]), run_time=1.2)
    narration_wait(scene, 1.5)
    paced_play(
        scene,
        Create(curves[0]),
        FadeIn(tags[0]),
        Create(curves[2]),
        FadeIn(tags[2]),
        run_time=1.6,
    )
    narration_wait(scene, 2.0)

    # -- Beat 2: at the same x, every tangent has the same tilt ---------------
    slope = parabola_slope(TANGENT_X)
    tangents = VGroup()
    dots = VGroup()
    for shift, color in zip(SHIFTS, SHIFT_COLORS):
        y0 = shifted_parabola(TANGENT_X, shift)
        direction = np.array([1.0, slope, 0.0])
        direction /= np.linalg.norm(direction)
        unit = axes.x_axis.get_unit_size()
        centre = axes.c2p(TANGENT_X, y0)
        tangents.add(glow_line(centre - direction * 1.05 * unit, centre + direction * 1.05 * unit, cfg.GREEN, 5))
        dots.add(glow_dot(centre, color, 0.08))

    guide = dashed_connector(axes.c2p(TANGENT_X, -4), axes.c2p(TANGENT_X, 9), cfg.MUTED, 22, 2.2)
    paced_play(scene, Create(guide), run_time=0.8)
    paced_play(scene, LaggedStart(*(FadeIn(d) for d in dots), lag_ratio=0.3), run_time=1.0)
    paced_play(scene, LaggedStart(*(Create(t) for t in tangents), lag_ratio=0.3), run_time=1.6)
    narration_wait(scene, 2.5)

    same_slope = fitted_eq(r"\frac{dy}{dx}=2x", cfg.GREEN, cfg.FONT["title"], width=5.2)
    same_slope.move_to([3.75, -1.35, 0])
    arrow_targets = (
        same_slope.get_top() + LEFT * 1.05,
        same_slope.get_top(),
        same_slope.get_top() + RIGHT * 1.05,
    )
    brace_arrows = VGroup(
        *(
            Arrow(
                tag.get_bottom(),
                target,
                color=cfg.MUTED,
                buff=0.18,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.13,
            )
            for tag, target in zip(tags, arrow_targets)
        )
    )
    paced_play(scene, LaggedStart(*(GrowArrow(a) for a in brace_arrows), lag_ratio=0.2), FadeIn(same_slope, shift=UP * 0.15), run_time=1.6)
    paced_play(scene, Indicate(same_slope, color=cfg.WHITE, scale_factor=1.07), run_time=0.8)
    narration_wait(scene, 3.5)

    # -- Beat 3: what integration cannot recover -------------------------------
    question = bottom_caption("Same derivative. So which curve did we start from?", cfg.WHITE)
    paced_play(scene, FadeIn(question), run_time=0.8)
    narration_wait(scene, 3.0)

    paced_play(scene, FadeOut(VGroup(tangents, dots, guide, brace_arrows, question)), run_time=0.7)

    constant = fitted_eq(r"y=x^2+C", cfg.PURPLE, cfg.FONT["title"], width=5.4).move_to([3.9, -1.55, 0])
    paced_play(scene, ReplacementTransform(same_slope, constant), run_time=1.2)
    ghosts = VGroup(
        *(
            axes.plot(lambda x, c=shift: shifted_parabola(x, c), x_range=[-2.45, 2.45], color=cfg.PURPLE, stroke_width=3.2)
            .set_stroke(opacity=0.42)
            for shift in (-1.5, 1.5, 2.8, 6.0)
        )
    )
    paced_play(scene, LaggedStart(*(Create(g) for g in ghosts), lag_ratio=0.15), run_time=1.8)
    narration_wait(scene, 3.5)

    # -- Beat 4: one extra fact collapses the family ---------------------------
    condition = fitted_eq(r"y(0)=3", cfg.GOLD, cfg.FONT["section"], width=4.4)
    condition.next_to(constant, DOWN, buff=0.7)
    target = glow_dot(axes.c2p(0, 3), cfg.GOLD, 0.11)
    paced_play(scene, FadeIn(condition, shift=UP * 0.12), FadeIn(target, scale=1.4), run_time=1.1)
    narration_wait(scene, 3.0)

    chosen = axes.plot(lambda x: shifted_parabola(x, 3.0), x_range=[-2.45, 2.45], color=cfg.GREEN, stroke_width=7)
    survivors = VGroup(curves, ghosts)
    paced_play(scene, survivors.animate.set_stroke(opacity=0.16), Create(chosen), run_time=1.6)
    answer = fitted_eq(r"y=x^2+3", cfg.GREEN, cfg.FONT["section"], width=5.0).move_to(condition)
    paced_play(scene, ReplacementTransform(condition, answer), FadeOut(tags), run_time=1.1)
    narration_wait(scene, 3.5)

    rule = bottom_caption("A rule for change, plus one known moment, picks one curve.", cfg.GREEN)
    paced_play(scene, FadeIn(rule), run_time=0.8)
    narration_wait(scene, 3.0)

    end_scene(scene, started, cfg.SCENE_DURATIONS["02"])
