"""Scene 10: substitution as changing the measuring variable, not a trick."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    paced_play,
)
from utils.math_utils import substitution_inner


class Scene10Substitution(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "10")
    add_cinematic_background(scene)

    original = eq(
        r"\int 2x\cos(x^2)\,dx",
        cfg.WHITE,
        cfg.FONT["title"],
        substrings_to_isolate=["x^2"],
    ).to_edge(UP, buff=0.6)
    paced_play(scene, Write(original), run_time=1.2)
    narration_wait(scene, 5.33)

    highlight = SurroundingRectangle(original.get_part_by_tex("x^2"), color=cfg.GOLD, buff=0.06, corner_radius=0.06)
    paced_play(scene, Create(highlight), run_time=0.8)
    narration_wait(scene, 3.99)
    paced_play(scene, FadeOut(highlight), run_time=0.5)

    sub_group = VGroup(
        eq(r"u=x^2", cfg.GOLD, cfg.FONT["section"]),
        eq(r"du=2x\,dx", cfg.GOLD, cfg.FONT["section"]),
    ).arrange(DOWN, buff=0.3).next_to(original, DOWN, buff=0.5)
    for line in sub_group:
        paced_play(scene, Write(line), run_time=1.0)
        narration_wait(scene, 4.78)

    result = eq(r"\int \cos u\,du", cfg.CYAN, cfg.FONT["title"]).next_to(sub_group, DOWN, buff=0.5)
    paced_play(scene, Write(result), run_time=1.2)
    narration_wait(scene, 6.65)

    paced_play(scene, FadeOut(VGroup(original, sub_group, result)), run_time=0.7)

    # -- Visual: the x-axis stretches nonlinearly into the u-axis -----------
    x_line = NumberLine(x_range=[0, 2.4, 0.5], length=10.5, color=cfg.CYAN, include_numbers=False).move_to([0, 1.6, 0])
    x_tag = eq("x", cfg.CYAN, cfg.FONT["body"]).next_to(x_line, LEFT, buff=0.3)
    u_line = NumberLine(x_range=[0, 5.5, 1], length=10.5, color=cfg.GOLD, include_numbers=False).move_to([0, -1.6, 0])
    u_tag = eq("u", cfg.GOLD, cfg.FONT["body"]).next_to(u_line, LEFT, buff=0.3)
    paced_play(scene, Create(x_line), FadeIn(x_tag), run_time=1.0)
    paced_play(scene, Create(u_line), FadeIn(u_tag), run_time=1.0)
    narration_wait(scene, 3.99)

    sample_xs = (0.0, 0.6, 1.0, 1.4, 1.8, 2.2)
    connectors = VGroup()
    for x_val in sample_xs:
        u_val = substitution_inner(x_val)
        p_x = x_line.n2p(x_val)
        p_u = u_line.n2p(u_val)
        dot_x = glow_dot(p_x, cfg.CYAN, 0.06)
        dot_u = glow_dot(p_u, cfg.GOLD, 0.06)
        link = Line(p_x, p_u, color=cfg.MUTED, stroke_width=2, stroke_opacity=0.6)
        connectors.add(VGroup(dot_x, dot_u, link))
    paced_play(scene, LaggedStartMap(FadeIn, connectors, lag_ratio=0.15), run_time=2.0)
    x_tracker = ValueTracker(0.08)
    moving_pair = always_redraw(
        lambda: VGroup(
            glow_dot(x_line.n2p(x_tracker.get_value()), cfg.CYAN, 0.08),
            glow_dot(u_line.n2p(substitution_inner(x_tracker.get_value())), cfg.GOLD, 0.08),
            Line(
                x_line.n2p(x_tracker.get_value()),
                u_line.n2p(substitution_inner(x_tracker.get_value())),
                color=cfg.WHITE,
                stroke_width=4,
            ),
        )
    )
    scene.add(moving_pair)
    paced_play(scene, x_tracker.animate.set_value(2.2), run_time=6.80, rate_func=rate_functions.ease_in_out_sine)

    stretch_caption = bottom_caption("Equal steps in x become unequal steps in u — that stretch is what du absorbs.", cfg.WHITE)
    paced_play(scene, FadeIn(stretch_caption), run_time=0.9)
    narration_wait(scene, 9.32)
    paced_play(scene, FadeOut(stretch_caption), run_time=0.5)

    key_idea = eq(r"\text{substitution changes coordinates so the structure simplifies}", cfg.GOLD, cfg.FONT["small"]).to_edge(DOWN, buff=0.4)
    paced_play(scene, FadeIn(key_idea), run_time=0.9)
    narration_wait(scene, 7.98)

    end_scene(scene, started, cfg.SCENE_DURATIONS["10"])
