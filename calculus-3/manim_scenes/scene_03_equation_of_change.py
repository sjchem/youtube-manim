"""Scene 03: dy/dx = y — an equation that describes a rule, not a curve."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    calc_axes,
    dashed_connector,
    end_scene,
    eq,
    fitted_eq,
    glow_dot,
    labelled_axes,
    narration_wait,
    outlined_text,
    paced_play,
    slope_tick,
)
from utils.math_utils import self_slope

PROBES = (
    (-2.0, 1.0, cfg.CYAN),
    (0.9, 2.0, cfg.GOLD),
    (2.0, -1.0, cfg.ORANGE),
)


class Scene03EquationOfChange(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "03")
    add_cinematic_background(scene)

    # -- Beat 1: the equation arrives on its own -----------------------------
    headline = fitted_eq(r"\frac{dy}{dx}=y", cfg.WHITE, cfg.FONT["hero"], width=6.4)
    halo = SurroundingRectangle(headline, color=cfg.PURPLE, buff=0.42, corner_radius=0.20, stroke_width=3.5)
    paced_play(scene, Write(headline), run_time=1.4)
    paced_play(scene, Create(halo), run_time=0.8)
    narration_wait(scene, 7.2)

    reading = outlined_text("the slope equals the height", cfg.FONT["body"], cfg.PURPLE)
    reading.next_to(halo, DOWN, buff=0.55)
    paced_play(scene, FadeIn(reading, shift=UP * 0.15), run_time=0.9)
    narration_wait(scene, 7.0)

    # -- Beat 2: move it aside and go looking for the rule in the plane -------
    paced_play(
        scene,
        FadeOut(reading),
        FadeOut(halo),
        headline.animate.scale(0.82).to_corner(UL, buff=0.48),
        run_time=1.2,
        rate_func=rate_functions.ease_in_out_sine,
    )

    axes = calc_axes((-3, 3, 1), (-3, 3, 1), 8.6, 5.6).move_to([0.2, -0.35, 0])
    axis_labels = labelled_axes(axes, "x", "y", cfg.MUTED, cfg.FONT["hero"])
    paced_play(scene, Create(axes), FadeIn(axis_labels, shift=UP * 0.08), run_time=1.1, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 4.6)

    # -- Beat 3: sample the rule at three different heights -------------------
    for index, (x, y, color) in enumerate(PROBES):
        slope = self_slope(x, y)
        dot = glow_dot(axes.c2p(x, y), color, 0.095)
        tick = slope_tick(axes, x, y, slope, color, half_length=0.62, stroke_width=7)
        guide = dashed_connector(axes.c2p(-3, y), axes.c2p(x, y), cfg.MUTED, 14, 2.0)
        height_tag = eq(f"y={y:.0f}", color, cfg.FONT["body"]).next_to(axes.c2p(-3, y), LEFT, buff=0.22)
        slope_tag = eq(f"\\text{{slope}}={slope:.0f}", color, cfg.FONT["section"])
        # The left probe is close to the vertical axis, so its enlarged label
        # sits above the segment; the other two have clear space to the right.
        if index == 0:
            slope_tag.next_to(tick, UP, buff=0.28)
        else:
            slope_tag.next_to(tick, RIGHT, buff=0.34)

        paced_play(
            scene,
            FadeIn(height_tag, shift=RIGHT * 0.10),
            Create(guide),
            FadeIn(dot, scale=1.3),
            run_time=0.9,
            rate_func=rate_functions.ease_in_out_sine,
        )
        paced_play(
            scene,
            GrowFromCenter(tick),
            FadeIn(slope_tag, shift=LEFT * 0.12),
            run_time=0.9,
            rate_func=rate_functions.ease_in_out_sine,
        )
        narration_wait(scene, 5.1 if index < 2 else 5.9)
        if index < len(PROBES) - 1:
            paced_play(scene, FadeOut(VGroup(guide, height_tag)), run_time=0.4)
        else:
            paced_play(scene, FadeOut(VGroup(guide, height_tag)), run_time=0.5)

    narration_wait(scene, 6.0)

    # -- Beat 4: what kind of instruction this really is ----------------------
    verdict_1 = outlined_text("It never says where the curve is.", cfg.FONT["body"], cfg.MUTED)
    verdict_2 = outlined_text("It says how the curve is allowed to move.", cfg.FONT["body"], cfg.GOLD)
    verdict = VGroup(verdict_1, verdict_2).arrange(DOWN, buff=0.28).to_edge(DOWN, buff=0.40)
    paced_play(scene, FadeIn(verdict_1), run_time=0.8)
    narration_wait(scene, 3.4)
    paced_play(scene, FadeIn(verdict_2, shift=UP * 0.12), run_time=0.9)
    paced_play(scene, Indicate(verdict_2, color=cfg.WHITE, scale_factor=1.05), run_time=0.8)
    narration_wait(scene, 4.6)

    end_scene(scene, started, cfg.SCENE_DURATIONS["03"])
