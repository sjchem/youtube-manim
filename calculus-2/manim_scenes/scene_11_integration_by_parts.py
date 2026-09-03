"""Scene 11: integration by parts falls out of a rectangle that grows on two sides."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    end_scene,
    eq,
    narration_wait,
    paced_play,
)


class Scene11IntegrationByParts(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "11")
    add_cinematic_background(scene)

    intro = eq(r"\text{area}=uv", cfg.WHITE, cfg.FONT["title"]).to_edge(UP, buff=0.55)
    paced_play(scene, Write(intro), run_time=1.0)
    narration_wait(scene, 5.08)

    # Use the generous open canvas: the geometry should be readable before it
    # shares the frame with the algebra.
    scale = 1.40
    u_val, v_val, du_val, dv_val = 3.0, 2.0, 0.55, 0.45
    bl = np.array([-2.6, -2.0, 0.0])
    w, h = u_val * scale, v_val * scale
    dw, dh = du_val * scale, dv_val * scale

    base = Polygon(bl, bl + RIGHT * w, bl + RIGHT * w + UP * h, bl + UP * h, color=cfg.WHITE, fill_color=cfg.PANEL, fill_opacity=0.85, stroke_width=3)
    u_label = eq("u", cfg.WHITE, cfg.FONT["body"]).next_to(base, DOWN, buff=0.2)
    v_label = eq("v", cfg.WHITE, cfg.FONT["body"]).next_to(base, LEFT, buff=0.2)
    paced_play(scene, FadeIn(base), FadeIn(u_label), FadeIn(v_label), run_time=1.0)
    narration_wait(scene, 5.08)

    grow_caption = bottom_caption("Let both sides grow a little.", cfg.GOLD)
    paced_play(scene, FadeIn(grow_caption), run_time=0.7)
    narration_wait(scene, 3.82)
    paced_play(scene, FadeOut(grow_caption), run_time=0.5)

    right_strip = Polygon(
        bl + RIGHT * w, bl + RIGHT * (w + dw), bl + RIGHT * (w + dw) + UP * h, bl + RIGHT * w + UP * h,
        color=cfg.GOLD, fill_color=cfg.GOLD, fill_opacity=0.55, stroke_width=2,
    )
    right_label = eq(r"v\,du", cfg.GOLD, cfg.FONT["body"]).next_to(right_strip, RIGHT, buff=0.20)
    top_strip = Polygon(
        bl + UP * h, bl + RIGHT * w + UP * h, bl + RIGHT * w + UP * (h + dh), bl + UP * (h + dh),
        color=cfg.CYAN, fill_color=cfg.CYAN, fill_opacity=0.55, stroke_width=2,
    )
    top_label = eq(r"u\,dv", cfg.CYAN, cfg.FONT["body"]).next_to(top_strip, UP, buff=0.20)
    corner = Polygon(
        bl + RIGHT * w + UP * h, bl + RIGHT * (w + dw) + UP * h, bl + RIGHT * (w + dw) + UP * (h + dh), bl + RIGHT * w + UP * (h + dh),
        color=cfg.MUTED, fill_color=cfg.MUTED, fill_opacity=0.5, stroke_width=1.5,
    )
    corner_label = eq(r"du\,dv", cfg.MUTED, cfg.FONT["small"]).next_to(corner, UR, buff=0.08)

    paced_play(scene, GrowFromEdge(right_strip, LEFT), FadeIn(right_label), run_time=2.8, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 2.18)
    paced_play(scene, GrowFromEdge(top_strip, DOWN), FadeIn(top_label), run_time=2.8, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 2.18)
    paced_play(scene, GrowFromPoint(corner, corner.get_corner(DL)), FadeIn(corner_label), run_time=2.2)
    narration_wait(scene, 2.16)

    negligible = bottom_caption("The corner shrinks fastest — ignore it in the limit.", cfg.MUTED)
    paced_play(scene, FadeIn(negligible), run_time=0.7)
    paced_play(
        scene,
        corner.animate.scale(0.14, about_point=corner.get_corner(DL)).set_opacity(0.08),
        FadeOut(corner_label),
        run_time=5.0,
        rate_func=rate_functions.ease_in_out_sine,
    )
    narration_wait(scene, 1.36)
    paced_play(scene, FadeOut(negligible), run_time=0.5)

    diagram = VGroup(base, u_label, v_label, right_strip, right_label, top_strip, top_label, corner)
    formula_group = VGroup(
        eq(r"d(uv)=u\,dv+v\,du", cfg.WHITE, cfg.FONT["body"]),
        eq(r"u\,dv=d(uv)-v\,du", cfg.GOLD, cfg.FONT["body"]),
    ).arrange(DOWN, buff=0.40).move_to([3.75, 0.65, 0])
    paced_play(scene, diagram.animate.scale(0.80).to_edge(LEFT, buff=0.55), run_time=0.8)
    for line in formula_group:
        paced_play(scene, Write(line), run_time=1.0)
        narration_wait(scene, 5.60)

    result = eq(r"\int u\,dv = uv-\int v\,du", cfg.GREEN, cfg.FONT["title"]).next_to(formula_group, DOWN, buff=0.58)
    if result.width > 5.8:
        result.scale_to_fit_width(5.8)
        result.next_to(formula_group, DOWN, buff=0.55)
    paced_play(scene, FadeOut(intro), Write(result), run_time=1.3)
    box = SurroundingRectangle(result, color=cfg.GREEN, buff=0.26, corner_radius=0.12)
    paced_play(scene, Create(box), run_time=0.8)
    narration_wait(scene, 8.90)

    closing = bottom_caption("Not a formula to memorize — a rectangle, rearranged.", cfg.WHITE)
    paced_play(scene, FadeIn(closing), run_time=0.9)
    narration_wait(scene, 6.36)

    end_scene(scene, started, cfg.SCENE_DURATIONS["11"])
