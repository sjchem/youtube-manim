"""Scene 09: the equation gives the law; one measurement picks the world."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    calc_axes,
    dashed_connector,
    end_scene,
    fitted_eq,
    glow_curve,
    glow_dot,
    labelled_axes,
    narration_wait,
    outlined_text,
    paced_play,
    solution_curve,
)
from utils.math_utils import exponential_solution

CONSTANTS = (-1.4, -0.6, -0.15, 0.35, 0.9, 1.5, 2.0, 3.0)
CHOSEN = 2.0
Y_CLIP = (-3.2, 6.2)


class Scene09InitialConditions(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "09")
    add_cinematic_background(scene)

    law = fitted_eq(r"\frac{dy}{dx}=y", cfg.WHITE, cfg.FONT["section"], width=3.0).to_corner(UL, buff=0.5)
    axes = calc_axes((-3, 2, 1), (-3, 6.4, 2), 8.6, 5.6).move_to([0.4, -0.35, 0])
    axis_labels = labelled_axes(axes, "x", "y", cfg.MUTED, cfg.FONT["small"])
    paced_play(scene, FadeIn(law), Create(axes), FadeIn(axis_labels), run_time=1.1)

    # -- Beat 1: every curve the law permits ----------------------------------
    family = VGroup(
        *(
            solution_curve(axes, lambda x, c=constant: exponential_solution(x, c), -3.0, 2.0, cfg.CYAN, 4.4, Y_CLIP)
            for constant in CONSTANTS
        )
    )
    general = fitted_eq(r"y=Ce^{x}", cfg.CYAN, cfg.FONT["section"], width=4.0).to_corner(UR, buff=0.5)
    paced_play(scene, LaggedStart(*(Create(curve) for curve in family), lag_ratio=0.16), run_time=3.4)
    paced_play(scene, FadeIn(general, shift=DOWN * 0.12), run_time=0.9)
    narration_wait(scene, 7.4)

    many = bottom_caption("Every one of these obeys exactly the same law.", cfg.MUTED)
    paced_play(scene, FadeIn(many), run_time=0.8)
    narration_wait(scene, 6.8)
    paced_play(scene, FadeOut(many), run_time=0.5)

    # -- Beat 2: one measurement -----------------------------------------------
    condition = fitted_eq(r"y(0)=2", cfg.GOLD, cfg.FONT["title"], width=4.2)
    condition.move_to([-4.55, 2.45, 0])
    marker = glow_dot(axes.c2p(0, 2), cfg.GOLD, 0.12)
    guides = VGroup(
        dashed_connector(axes.c2p(0, 0), axes.c2p(0, 2), cfg.GOLD, 8, 2.6),
        dashed_connector(axes.c2p(-3, 2), axes.c2p(0, 2), cfg.GOLD, 14, 2.6),
    )
    paced_play(scene, FadeIn(condition, shift=DOWN * 0.12), run_time=0.9)
    paced_play(scene, Create(guides), FadeIn(marker, scale=1.5), run_time=1.2)
    narration_wait(scene, 6.2)

    chosen = glow_curve(solution_curve(axes, lambda x: exponential_solution(x, CHOSEN), -3.0, 2.0, cfg.GREEN, 8, Y_CLIP), cfg.GREEN)
    paced_play(scene, family.animate.set_stroke(opacity=0.13), Create(chosen), run_time=2.0)
    answer = fitted_eq(r"y=2e^{x}", cfg.GREEN, cfg.FONT["title"], width=4.6).move_to([5.35, 2.65, 0])
    answer_plate = SurroundingRectangle(
        answer,
        color=cfg.GREEN,
        buff=0.24,
        corner_radius=0.14,
        stroke_width=3,
        fill_color=cfg.PANEL,
        fill_opacity=0.34,
    )
    paced_play(scene, ReplacementTransform(general, answer), Create(answer_plate), run_time=1.1)
    paced_play(scene, Indicate(VGroup(answer_plate, answer), color=cfg.WHITE, scale_factor=1.06), run_time=0.8)
    narration_wait(scene, 7.4)

    # -- Beat 3: the sentence worth remembering ---------------------------------
    line_1 = outlined_text("The equation gives the law.", cfg.FONT["small"], cfg.CYAN)
    line_2 = outlined_text("The starting point says which world you are in.", cfg.FONT["small"], cfg.GOLD)
    lines = VGroup(line_1, line_2).arrange(DOWN, buff=0.24).to_edge(DOWN, buff=0.12)
    caption_plate = RoundedRectangle(
        width=lines.width + 0.72,
        height=lines.height + 0.42,
        corner_radius=0.16,
        stroke_width=0,
        fill_color=cfg.BG,
        fill_opacity=0.94,
    ).move_to(lines)
    paced_play(scene, FadeIn(caption_plate), FadeIn(line_1), run_time=0.8)
    narration_wait(scene, 4.6)
    paced_play(scene, FadeIn(line_2, shift=UP * 0.12), run_time=0.9)
    narration_wait(scene, 6.2)

    end_scene(scene, started, cfg.SCENE_DURATIONS["09"])
