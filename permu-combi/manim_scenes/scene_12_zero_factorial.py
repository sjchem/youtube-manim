"""Scene 12: the short answer to why 0! = 1."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background, begin_scene, boxed_statement, chip, cue, end_scene, eq,
    outlined_text, paced_play, swap_caption, team_ring, top_caption,
)


class Scene12ZeroFactorial(Scene):
    """One way to choose everything, so one way to arrange nothing."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "12")
    add_cinematic_background(scene)

    heading = top_caption("WHY  IS  0!  EQUAL  TO  1?", cfg.PURPLE)
    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), run_time=0.8)

    # --- 0-14s: choosing all five ---------------------------------------------
    ring_center = np.array([-3.4, 0.75, 0])
    ring = team_ring(1.9, cfg.UNORDERED, ring_center)
    members = VGroup(*[chip(name, cfg.UNORDERED, 0.36) for name in "ABCDE"])
    member_offsets = (
        [-0.82, 0.5, 0], [0.0, 0.62, 0], [0.82, 0.5, 0],
        [-0.46, -0.55, 0], [0.46, -0.55, 0],
    )
    for member, offset in zip(members, member_offsets):
        member.move_to(ring_center + np.array(offset))
    paced_play(scene, Create(ring), run_time=0.8)
    paced_play(scene, LaggedStart(*[FadeIn(m, scale=0.6) for m in members], lag_ratio=0.15), run_time=1.4)
    only_one = eq(r"\binom{5}{5} = 1", cfg.UNORDERED, 80).move_to([3.25, 0.75, 0])
    paced_play(
        scene,
        FadeIn(only_one, shift=LEFT * 0.25),
        FadeOut(heading, shift=UP * 0.15),
        run_time=1.0,
    )
    caption = swap_caption(scene, None, "There is exactly one way to take everybody.", cfg.UNORDERED)
    scene.play(
        *[
            member.animate.shift(UP * (0.055 + 0.012 * (index % 2)))
            for index, member in enumerate(members)
        ],
        run_time=1.8,
        rate_func=there_and_back,
    )
    scene.play(ring.animate.scale(1.018), run_time=1.5, rate_func=there_and_back)
    cue(scene, started, 14.0)

    # --- 14-30s: but the formula says ------------------------------------------
    formula = eq(r"\binom{5}{5} = \frac{5!}{5!\,\cdot\,0!}", cfg.WHITE, 74).move_to([0, -0.45, 0])
    scene.play(
        FadeOut(ring, members),
        only_one.animate.scale(0.86).move_to([0, 1.9, 0]),
        FadeIn(formula, shift=UP * 0.2),
        run_time=1.2,
    )
    paced_play(scene, Indicate(formula, color=cfg.GOLD, scale_factor=1.025), run_time=1.4)
    cue(scene, started, 20.0)

    demand = boxed_statement("For this to come out as 1:", cfg.GOLD, cfg.FONT["label"])
    demand.move_to([0, 0.55, 0])
    scene.play(
        FadeOut(only_one),
        formula.animate.scale(0.9).move_to([0, -1.15, 0]),
        FadeIn(demand, scale=0.92),
        run_time=1.3,
    )
    answer = eq("0! = 1", cfg.GREEN, 108).move_to([0, 2.35, 0])
    paced_play(scene, FadeIn(answer, scale=1.25), run_time=1.1)
    paced_play(scene, Indicate(answer, color=cfg.WHITE, scale_factor=1.08), run_time=1.0)
    cue(scene, started, 30.0)

    # --- 30-45s: the picture behind it ------------------------------------------
    empty_box = RoundedRectangle(
        width=3.0, height=1.9, corner_radius=0.18,
        stroke_color=cfg.GREEN, stroke_width=4.5, fill_color=cfg.PANEL, fill_opacity=0.5,
    ).move_to([0, 0.5, 0])
    empty_tag = outlined_text("1 ARRANGEMENT:  EMPTY", cfg.FONT["small"], cfg.GREEN)
    empty_tag.next_to(empty_box, DOWN, buff=0.3)
    scene.play(
        FadeOut(demand, formula, caption),
        FadeIn(empty_box, scale=0.85),
        run_time=1.2,
    )
    caption = swap_caption(scene, None, "One way to arrange nothing: do nothing.", cfg.GREEN)
    paced_play(scene, FadeIn(empty_tag, shift=UP * 0.15), run_time=0.9)
    scene.play(empty_box.animate.scale(1.025), run_time=1.8, rate_func=there_and_back)
    cue(scene, started, 41.0)
    paced_play(scene, Indicate(answer, color=cfg.GREEN, scale_factor=1.06), run_time=1.2)

    end_scene(scene, started, cfg.SCENE_DURATIONS["12"])
