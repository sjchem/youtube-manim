"""Scene 05: growth proportional to size, and why e shows up uninvited."""

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
    labelled_axes,
    narration_wait,
    outlined_text,
    paced_play,
)
from utils.math_utils import GROWTH_RATE, GROWTH_RATIO, discrete_growth, exponential_growth
from utils.render_helpers import growth_step_labels

DISH_CENTER = np.array([-3.85, -0.30, 0.0])
DISH_RADIUS = 2.30
GENERATIONS = 4


def _colony(total: int, seed: int = cfg.SEED) -> VGroup:
    """`total` organisms scattered inside the dish, in a fixed random order."""
    rng = np.random.default_rng(seed)
    colony = VGroup()
    while len(colony) < total:
        x, y = rng.uniform(-1, 1, size=2)
        if x * x + y * y > 0.88:
            continue
        point = DISH_CENTER + np.array([x, y, 0.0]) * DISH_RADIUS * 0.92
        colony.add(Dot(point, radius=0.062, color=cfg.GREEN).set_stroke(cfg.BG, width=1.2))
    return colony


class Scene05ExponentialGrowth(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "05")
    add_cinematic_background(scene)

    # -- Beat 1: a colony, and the rule it obeys ------------------------------
    counts = [int(round(value)) for value in discrete_growth(GENERATIONS)]
    dish_rim = Circle(radius=DISH_RADIUS, color=cfg.CYAN, stroke_width=4, fill_color=cfg.PANEL, fill_opacity=0.55).move_to(DISH_CENTER)
    dish_glow = Circle(radius=DISH_RADIUS * 1.06, color=cfg.CYAN, stroke_width=14, stroke_opacity=0.07).move_to(DISH_CENTER)
    colony = _colony(counts[-1])

    paced_play(scene, FadeIn(dish_glow), Create(dish_rim), run_time=1.0)
    paced_play(scene, LaggedStart(*(FadeIn(dot, scale=1.6) for dot in colony[: counts[0]]), lag_ratio=0.008), run_time=2.4)

    rule = fitted_eq(r"\frac{dP}{dt}=kP", cfg.WHITE, cfg.FONT["title"], width=4.6).move_to([3.55, 2.35, 0])
    meaning = outlined_text("more of them → faster growth", cfg.FONT["small"], cfg.CYAN).next_to(rule, DOWN, buff=0.42)
    paced_play(scene, Write(rule), run_time=1.2)
    paced_play(scene, FadeIn(meaning, shift=UP * 0.1), run_time=0.8)
    narration_wait(scene, 10.2)

    # -- Beat 2: generation by generation --------------------------------------
    ladder_labels = growth_step_labels(discrete_growth(GENERATIONS))
    ladder = VGroup(*(eq(text, cfg.GREEN, cfg.FONT["section"]) for text in ladder_labels))
    ladder.arrange(RIGHT, buff=0.52).move_to([3.35, -0.55, 0])
    if ladder.width > 6.6:
        ladder.scale_to_fit_width(6.6)
    arrows = VGroup(
        *(
            Arrow(ladder[i].get_right(), ladder[i + 1].get_left(), color=cfg.GOLD, buff=0.10, stroke_width=3.4, max_tip_length_to_length_ratio=0.35)
            for i in range(len(ladder) - 1)
        )
    )
    ratio_tag = eq(
        rf"\times {GROWTH_RATIO}\quad\Rightarrow\quad k=\ln {GROWTH_RATIO}\approx {GROWTH_RATE:.3f}",
        cfg.GOLD,
        cfg.FONT["small"],
    ).next_to(ladder, DOWN, buff=0.46)

    paced_play(scene, FadeIn(ladder[0]), run_time=0.6)
    for index in range(1, len(ladder)):
        added = colony[counts[index - 1] : counts[index]]
        paced_play(
            scene,
            GrowArrow(arrows[index - 1]),
            FadeIn(ladder[index], shift=RIGHT * 0.12),
            LaggedStart(*(FadeIn(dot, scale=2.0) for dot in added), lag_ratio=0.01),
            run_time=1.8,
        )
    paced_play(scene, FadeIn(ratio_tag), run_time=0.7)
    narration_wait(scene, 11.4)

    jump = bottom_caption("Each step adds a slice of what already exists.", cfg.GOLD)
    paced_play(scene, FadeIn(jump), run_time=0.8)
    narration_wait(scene, 7.8)

    # -- Beat 3: let the steps dissolve into a smooth curve ---------------------
    paced_play(scene, FadeOut(VGroup(ladder, arrows, ratio_tag, jump, meaning)), run_time=0.8)
    paced_play(
        scene,
        VGroup(dish_rim, dish_glow, colony).animate.scale(0.62).move_to([-4.6, 0.15, 0]),
        rule.animate.scale(0.78).to_corner(UR, buff=0.55),
        run_time=1.2,
    )

    axes = calc_axes((0, 4.2, 1), (0, 260, 100), 7.4, 4.9).move_to([1.55, -0.35, 0])
    axis_labels = labelled_axes(axes, "t", "P", cfg.MUTED, cfg.FONT["small"])
    curve = axes.plot(exponential_growth, x_range=[0, 4.2], color=cfg.GREEN, stroke_width=7)
    steps = VGroup(*(glow_dot(axes.c2p(index, value), cfg.GOLD, 0.085) for index, value in enumerate(discrete_growth(GENERATIONS))))
    paced_play(scene, Create(axes), FadeIn(axis_labels), run_time=1.0)
    paced_play(scene, LaggedStart(*(FadeIn(dot, scale=1.4) for dot in steps), lag_ratio=0.25), run_time=1.6)
    paced_play(scene, Create(curve), run_time=2.6, rate_func=rate_functions.ease_in_out_sine)
    solution = fitted_eq(r"P(t)=P_0e^{kt}", cfg.GREEN, cfg.FONT["section"], width=5.4)
    solution.next_to(axes, DOWN, buff=0.34)
    paced_play(scene, FadeIn(solution, shift=UP * 0.12), run_time=1.0)
    narration_wait(scene, 10.2)

    # -- Beat 4: back to dy/dx = y, and the reason e is special -----------------
    paced_play(scene, FadeOut(VGroup(axes, axis_labels, curve, steps, solution, dish_rim, dish_glow, colony, rule)), run_time=0.8)

    special = fitted_eq(r"\frac{d}{dx}e^{x}=e^{x}", cfg.PURPLE, cfg.FONT["hero"], width=7.6).move_to([0, 0.85, 0])
    plate = SurroundingRectangle(special, color=cfg.PURPLE, buff=0.36, corner_radius=0.18, stroke_width=3.5)
    paced_play(scene, Write(special), Create(plate), run_time=1.8)
    narration_wait(scene, 8.0)

    reading = outlined_text("its rate of change is itself", cfg.FONT["body"], cfg.WHITE).next_to(plate, DOWN, buff=0.60)
    paced_play(scene, FadeIn(reading, shift=UP * 0.12), run_time=0.9)
    narration_wait(scene, 5.8)

    verdict = bottom_caption("Whenever growth is proportional to size, e is already there.", cfg.GOLD)
    paced_play(scene, FadeIn(verdict), run_time=0.9)
    narration_wait(scene, 7.2)

    end_scene(scene, started, cfg.SCENE_DURATIONS["05"])
