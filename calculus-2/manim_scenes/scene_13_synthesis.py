"""Scene 13: position, velocity, and accumulation reunite — the Fundamental Theorem, in full."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    area_region,
    begin_scene,
    bottom_caption,
    calc_axes,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    outlined_text,
    paced_play,
    tangent_line,
)
from utils.math_utils import position_profile, velocity_profile


class Scene13Synthesis(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "13")
    add_cinematic_background(scene)

    # -- Beat 1: one motion, viewed two directions at once ------------------
    top_axes = calc_axes(x_range=(0, 4, 1), y_range=(0, 11, 5), x_length=9.2, y_length=2.9).move_to([0, 1.9, 0])
    top_tag = eq("s(t)", cfg.WHITE, cfg.FONT["small"]).next_to(top_axes, LEFT, buff=0.3)
    bottom_axes = calc_axes(x_range=(0, 4, 1), y_range=(0, 5, 2.5), x_length=9.2, y_length=2.5).move_to([0, -2.1, 0])
    bottom_tag = eq("v(t)=s'(t)", cfg.CYAN, cfg.FONT["small"]).next_to(bottom_axes, LEFT, buff=0.3)
    top_curve = top_axes.plot(position_profile, x_range=[0, 4], color=cfg.WHITE, stroke_width=6)
    bottom_curve = bottom_axes.plot(velocity_profile, x_range=[0, 4], color=cfg.CYAN, stroke_width=6)

    paced_play(scene, Create(top_axes), FadeIn(top_tag), Create(top_curve), run_time=1.1)
    paced_play(scene, Create(bottom_axes), FadeIn(bottom_tag), run_time=0.9)
    narration_wait(scene, 4.72)

    t_tracker = ValueTracker(0.15)
    tangent = always_redraw(lambda: tangent_line(top_axes, position_profile, velocity_profile, t_tracker.get_value(), cfg.GOLD, half_length=0.5))
    top_dot = always_redraw(lambda: glow_dot(top_axes.c2p(t_tracker.get_value(), position_profile(t_tracker.get_value())), cfg.GOLD, 0.09))
    bottom_dot = always_redraw(lambda: glow_dot(bottom_axes.c2p(t_tracker.get_value(), velocity_profile(t_tracker.get_value())), cfg.GOLD, 0.09))
    scene.add(tangent, top_dot, bottom_dot)
    diff_caption = bottom_caption("Differentiate position: the tangent's slope is velocity.", cfg.GOLD)
    paced_play(scene, FadeIn(tangent), FadeIn(top_dot), Create(bottom_curve), FadeIn(bottom_dot), FadeIn(diff_caption), run_time=1.2)
    paced_play(scene, t_tracker.animate.set_value(3.85), run_time=8.22, rate_func=rate_functions.ease_in_out_sine)
    paced_play(scene, FadeOut(diff_caption), run_time=0.5)

    area_under_v = always_redraw(lambda: area_region(bottom_axes, bottom_curve, 0, max(0.05, t_tracker.get_value()), cfg.GREEN, 0.4))
    scene.add(area_under_v)
    int_caption = bottom_caption("Integrate velocity: the accumulated area is displacement.", cfg.GREEN)
    paced_play(scene, FadeIn(int_caption), run_time=0.8)
    t_tracker.set_value(0.15)
    paced_play(scene, t_tracker.animate.set_value(3.85), run_time=8.22, rate_func=rate_functions.ease_in_out_sine)

    paced_play(scene, FadeOut(VGroup(top_axes, top_tag, top_curve, bottom_axes, bottom_tag, bottom_curve, tangent, top_dot, bottom_dot, area_under_v, int_caption)), run_time=0.8)

    # -- Beat 2: the two boxed statements -------------------------------------
    box_top = eq(r"\text{Position} \xrightarrow{\;\text{differentiate}\;} \text{Velocity}", cfg.GOLD, cfg.FONT["section"])
    box_bottom = eq(r"\text{Velocity} \xrightarrow{\;\text{integrate}\;} \text{Position change}", cfg.GREEN, cfg.FONT["section"])
    box_group = VGroup(box_top, box_bottom).arrange(DOWN, buff=0.65)
    outline_top = SurroundingRectangle(box_top, color=cfg.GOLD, buff=0.30, corner_radius=0.15, stroke_width=3.5)
    outline_bottom = SurroundingRectangle(box_bottom, color=cfg.GREEN, buff=0.30, corner_radius=0.15, stroke_width=3.5)
    paced_play(scene, FadeIn(box_top), Create(outline_top), run_time=1.1)
    narration_wait(scene, 6.30)
    paced_play(scene, FadeIn(box_bottom), Create(outline_bottom), run_time=1.1)
    narration_wait(scene, 7.86)
    paced_play(scene, FadeOut(VGroup(box_top, box_bottom, outline_top, outline_bottom)), run_time=0.7)

    # -- Beat 3: the Fundamental Theorem, both forms --------------------------
    ftc_1 = eq(r"\frac{d}{dx}\!\left(\int_a^x f(t)\,dt\right)=f(x)", cfg.CYAN, cfg.FONT["title"])
    if ftc_1.width > cfg.SAFE_WIDTH:
        ftc_1.scale_to_fit_width(cfg.SAFE_WIDTH)
    ftc_1.move_to([0, 1.5, 0])
    ftc_1_box = SurroundingRectangle(ftc_1, color=cfg.CYAN, buff=0.28, corner_radius=0.14)
    paced_play(scene, FadeIn(ftc_1), run_time=1.3)
    paced_play(scene, Create(ftc_1_box), run_time=0.7)
    narration_wait(scene, 9.44)

    ftc_2 = eq(r"\int_a^b f(x)\,dx = F(b)-F(a)", cfg.GREEN, cfg.FONT["title"]).move_to([0, -0.7, 0])
    ftc_2_box = SurroundingRectangle(ftc_2, color=cfg.GREEN, buff=0.28, corner_radius=0.14)
    paced_play(scene, FadeIn(ftc_2), run_time=1.3)
    paced_play(scene, Create(ftc_2_box), run_time=0.7)
    narration_wait(scene, 6.30)

    where_label = eq("F'(x)=f(x)", cfg.WHITE, cfg.FONT["small"]).next_to(ftc_2, DOWN, buff=0.6)
    paced_play(scene, FadeIn(where_label), run_time=0.9)
    narration_wait(scene, 9.44)

    paced_play(scene, FadeOut(VGroup(ftc_1, ftc_1_box, ftc_2, ftc_2_box, where_label)), run_time=0.8)

    # -- Beat 4: the closing idea ------------------------------------------------
    closing_1 = eq(r"\text{Derivatives look at change locally.}", cfg.CYAN, cfg.FONT["section"])
    closing_2 = eq(r"\text{Integrals rebuild the whole from tiny local changes.}", cfg.GOLD, cfg.FONT["section"])
    if closing_1.width > cfg.SAFE_WIDTH:
        closing_1.scale_to_fit_width(cfg.SAFE_WIDTH)
    if closing_2.width > cfg.SAFE_WIDTH:
        closing_2.scale_to_fit_width(cfg.SAFE_WIDTH)
    paced_play(scene, Write(closing_1), run_time=1.2)
    narration_wait(scene, 7.86)
    paced_play(scene, closing_1.animate.shift(UP * 0.8), run_time=0.6)
    closing_2.next_to(closing_1, DOWN, buff=0.5)
    paced_play(scene, Write(closing_2), run_time=1.3)
    narration_wait(scene, 9.44)
    paced_play(scene, FadeOut(VGroup(closing_1, closing_2)), run_time=0.7)

    # -- Beat 5: the visual story arc -----------------------------------------
    chain_words = ("Changing\nMotion", "Derivative", "Optimization", "Tiny\nPieces", "Accumulation", "Integral", "Fundamental\nTheorem")
    chain_colors = (cfg.WHITE, cfg.GOLD, cfg.ORANGE, cfg.CYAN, cfg.BLUE, cfg.CYAN, cfg.GREEN)
    boxes = VGroup()
    for word, color in zip(chain_words, chain_colors):
        label = Text(word, font_size=cfg.FONT["tiny"], color=color, weight=BOLD, line_spacing=0.85).set_stroke(cfg.BG, width=3, opacity=0.9, background=True)
        frame = RoundedRectangle(width=label.width + 0.4, height=label.height + 0.4, corner_radius=0.12, color=color, stroke_width=2.5, fill_color=cfg.PANEL, fill_opacity=0.75)
        boxes.add(VGroup(frame, label))
    row_1 = VGroup(*boxes[:4]).arrange(RIGHT, buff=0.32)
    row_2 = VGroup(*boxes[4:]).arrange(RIGHT, buff=0.32)
    full_chain = VGroup(row_1, row_2).arrange(DOWN, buff=0.4).move_to(ORIGIN)
    paced_play(scene, LaggedStart(*(FadeIn(box, shift=UP * 0.1) for box in boxes), lag_ratio=0.18), run_time=5.2)
    narration_wait(scene, 7.04)

    final_caption = bottom_caption("Two sides of the same idea, from start to finish.", cfg.WHITE)
    paced_play(scene, FadeIn(final_caption), run_time=0.9)
    narration_wait(scene, 9.44)

    # Hand the visual story directly to the next lesson.
    paced_play(scene, FadeOut(full_chain), FadeOut(final_caption), run_time=0.7)
    next_label = outlined_text("NEXT VIDEO", cfg.FONT["body"], cfg.GREEN)
    next_rule = Line(LEFT * 2.1, RIGHT * 2.1, color=cfg.GOLD, stroke_width=4)
    next_title = outlined_text("From Integrals to Differential Equations", cfg.FONT["title"], cfg.CYAN)
    if next_title.width > cfg.SAFE_WIDTH:
        next_title.scale_to_fit_width(cfg.SAFE_WIDTH)
    teaser = VGroup(next_label, next_rule, next_title).arrange(DOWN, buff=0.32).move_to(ORIGIN)
    paced_play(
        scene,
        FadeIn(next_label, shift=UP * 0.12),
        Create(next_rule),
        FadeIn(next_title, shift=UP * 0.12),
        run_time=1.3,
    )
    narration_wait(scene, 6.0)

    end_scene(scene, started, cfg.SCENE_DURATIONS["13"])
