"""Scene 09: identical objects and combinations inside geometry."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background, begin_scene, boxed_statement, cue, end_scene, eq,
    outlined_text, paced_play, swap_caption, top_caption,
)


class Scene09AlikeGeometry(Scene):
    """Remove invisible swaps, then count vertex selections."""

    def construct(self) -> None:
        play_scene(self)


def letter_disc(letter: str, color: str) -> VGroup:
    disc = Circle(radius=0.58, color=color, stroke_width=4,
                  fill_color=cfg.PANEL, fill_opacity=0.85)
    glyph = outlined_text(letter, 48, color).move_to(disc)
    return VGroup(disc, glyph)


def gentle_breathe(scene: Scene, mob: Mobject, run_time: float = 2.0, scale: float = 1.02) -> None:
    """Keep a narrated idea moving without changing its final layout."""
    scene.play(mob.animate.scale(scale), run_time=run_time, rate_func=there_and_back)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "09")
    add_cinematic_background(scene)

    heading = top_caption("WHEN  SOME  OBJECTS  LOOK  ALIKE", cfg.PURPLE)
    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), run_time=0.8)

    # --- 0-96s: LEVEL and invisible swaps -----------------------------------
    colors = {"L": cfg.CYAN, "E": cfg.GOLD, "V": cfg.PURPLE}
    letters = VGroup(*[letter_disc(char, colors[char]) for char in "LEVEL"])
    letters.arrange(RIGHT, buff=0.55).move_to([0, 1.75, 0])
    paced_play(scene, LaggedStart(*[FadeIn(letter, scale=0.65) for letter in letters], lag_ratio=0.18), run_time=1.5)
    caption = swap_caption(scene, None, "Five positions suggest five factorial.", cfg.CYAN)
    naive = MathTex(r"5!", "=", "120", font_size=82).move_to([0, -0.15, 0])
    naive.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    naive[0].set_color(cfg.PURPLE)
    naive[1].set_color(cfg.MUTED)
    naive[2].set_color(cfg.GOLD)
    paced_play(scene, FadeIn(naive, shift=UP * 0.2), run_time=1.0)
    scene.play(
        letters[0].animate.shift(UP * 0.07),
        letters[4].animate.shift(UP * 0.07),
        run_time=1.8,
        rate_func=there_and_back,
    )
    cue(scene, started, 18.0)

    before = outlined_text("LEVEL", cfg.FONT["body"], cfg.WHITE).move_to([0, -1.6, 0])
    paced_play(scene, FadeIn(before), FadeOut(heading, shift=UP * 0.15), run_time=0.7)
    paced_play(scene, Swap(letters[0], letters[4], path_arc=PI / 2), run_time=1.3)
    same_l = outlined_text("STILL LEVEL", cfg.FONT["small"], cfg.CYAN).next_to(before, DOWN, buff=0.22)
    paced_play(scene, FadeIn(same_l), run_time=0.8)
    paced_play(scene, Indicate(VGroup(letters[0], letters[4]), color=cfg.CYAN, scale_factor=1.045), run_time=1.6)
    cue(scene, started, 34.0)

    two_l = eq("2!", cfg.CYAN, 74).move_to([-2.2, -0.35, 0])
    l_tag = outlined_text("SWAP THE Ls", cfg.FONT["tiny"], cfg.CYAN).next_to(two_l, DOWN, buff=0.2)
    paced_play(scene, FadeOut(naive), FadeIn(two_l), FadeIn(l_tag), run_time=0.9)
    paced_play(scene, Swap(letters[1], letters[3], path_arc=-PI / 2), run_time=1.3)
    two_e = eq("2!", cfg.GOLD, 74).move_to([2.2, -0.35, 0])
    e_tag = outlined_text("SWAP THE Es", cfg.FONT["tiny"], cfg.GOLD).next_to(two_e, DOWN, buff=0.2)
    paced_play(scene, FadeIn(two_e), FadeIn(e_tag), run_time=0.8)
    paced_play(scene, Indicate(VGroup(letters[1], letters[3]), color=cfg.GOLD, scale_factor=1.045), run_time=1.6)
    cue(scene, started, 51.0)

    formula = boxed_statement(r"\frac{5!}{2!\,2!}=30", cfg.GREEN, 78, tex=True).move_to([0, -0.6, 0])
    scene.play(FadeOut(before, same_l, two_l, two_e, l_tag, e_tag),
               FadeIn(formula, scale=0.9), run_time=1.1)
    caption = swap_caption(scene, caption, "Divide by swaps that create no visible change.", cfg.GREEN)
    gentle_breathe(scene, formula, run_time=1.8, scale=1.018)
    cue(scene, started, 68.0)

    general = boxed_statement(r"\frac{n!}{p!\,q!\,r!\cdots}", cfg.PURPLE, 72, tex=True)
    general.move_to([0, -0.55, 0])
    scene.play(ReplacementTransform(formula, general), run_time=1.2)
    counts = outlined_text("p, q, r, … are repetition counts", cfg.FONT["small"], cfg.MUTED)
    counts.next_to(general, DOWN, buff=0.3)
    paced_play(scene, FadeIn(counts, shift=UP * 0.15), run_time=0.8)
    paced_play(scene, Indicate(counts, color=cfg.WHITE, scale_factor=1.025), run_time=1.5)
    cue(scene, started, 84.0)
    bridge = swap_caption(scene, caption, "Now let a choice draw a geometric object.", cfg.GOLD)
    scene.play(
        *[letter.animate.shift(UP * (0.05 + 0.012 * (index % 2))) for index, letter in enumerate(letters)],
        run_time=1.8,
        rate_func=there_and_back,
    )
    cue(scene, started, 94.0)

    # --- 96-179s: diagonals as selections of two vertices -------------------
    scene.play(FadeOut(letters, general, counts, bridge), run_time=1.0)
    geometry_heading = top_caption("COMBINATIONS  INSIDE  GEOMETRY", cfg.UNORDERED)
    paced_play(scene, FadeIn(geometry_heading, shift=DOWN * 0.15), run_time=0.8)

    radius = 2.0
    diagram_center = np.array([-2.25, 0.35, 0])
    points = [diagram_center + radius * np.array([np.cos(PI / 2 + k * TAU / 6), np.sin(PI / 2 + k * TAU / 6), 0])
              for k in range(6)]
    vertices = VGroup(*[Dot(point, radius=0.11, color=cfg.GOLD) for point in points])
    labels = VGroup(*[
        outlined_text(str(i + 1), 26, cfg.GOLD).move_to(
            diagram_center + (point - diagram_center) * 1.18
        )
        for i, point in enumerate(points)
    ])
    paced_play(scene, LaggedStart(*[FadeIn(v, scale=0.4) for v in vertices], lag_ratio=0.15), run_time=1.2)
    paced_play(scene, FadeIn(labels), FadeOut(geometry_heading, shift=UP * 0.15), run_time=0.7)
    scene.play(
        LaggedStart(*[Indicate(vertex, color=cfg.WHITE, scale_factor=1.35) for vertex in vertices], lag_ratio=0.18),
        run_time=2.1,
    )
    cue(scene, started, 108.0)

    segments = VGroup()
    sides = VGroup()
    diagonals = VGroup()
    for i in range(6):
        for j in range(i + 1, 6):
            is_side = (j - i == 1) or (i == 0 and j == 5)
            line = Line(points[i], points[j], color=cfg.MUTED if is_side else cfg.CYAN,
                        stroke_width=4 if is_side else 3, stroke_opacity=0.9)
            segments.add(line)
            (sides if is_side else diagonals).add(line)
    paced_play(scene, LaggedStart(*[Create(line) for line in segments], lag_ratio=0.08), run_time=3.0)
    pairs = MathTex(r"\binom{6}{2}", "=", "15", font_size=72).move_to([3.65, 1.15, 0])
    pairs.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    pairs[0].set_color(cfg.UNORDERED)
    pairs[1].set_color(cfg.MUTED)
    pairs[2].set_color(cfg.GOLD)
    pairs_tag = outlined_text("VERTEX PAIRS", cfg.FONT["tiny"], cfg.UNORDERED).next_to(pairs, DOWN, buff=0.22)
    paced_play(scene, FadeIn(pairs), FadeIn(pairs_tag), run_time=0.9)
    scene.play(
        diagonals.animate.set_stroke(opacity=0.48),
        run_time=1.8,
        rate_func=there_and_back,
    )
    cue(scene, started, 130.0)

    paced_play(scene, sides.animate.set_color(cfg.GRAY).set_opacity(0.3), run_time=1.0)
    subtraction = eq(r"15-6=9", cfg.GOLD, 72).move_to([3.65, -0.65, 0])
    side_tag = outlined_text("REMOVE 6 SIDES", cfg.FONT["tiny"], cfg.GOLD).next_to(subtraction, DOWN, buff=0.22)
    paced_play(scene, FadeIn(subtraction), FadeIn(side_tag), run_time=0.9)
    paced_play(scene, Indicate(diagonals, color=cfg.GREEN, scale_factor=1.02), run_time=1.2)
    scene.play(
        LaggedStart(*[
            ShowPassingFlash(line.copy().set_color(cfg.GREEN).set_stroke(width=6), time_width=0.5)
            for line in diagonals
        ], lag_ratio=0.12),
        run_time=2.4,
    )
    cue(scene, started, 145.0)

    result = boxed_statement(
        r"\text{diagonals}=\binom{n}{2}-n", cfg.UNORDERED, 60, tex=True, max_width=5.5,
    )
    result.move_to([3.65, -0.65, 0])
    paced_play(
        scene,
        FadeOut(pairs, pairs_tag, subtraction, side_tag),
        FadeIn(result, shift=UP * 0.18),
        run_time=1.0,
    )
    gentle_breathe(scene, result, run_time=1.7, scale=1.018)
    cue(scene, started, 157.0)

    triangle = Polygon(points[0], points[2], points[4], color=cfg.PURPLE,
                       stroke_width=7, fill_color=cfg.PURPLE, fill_opacity=0.2)
    triangle_count = boxed_statement(r"\text{choose 3 vertices}\;\longrightarrow\;\binom{n}{3}",
                                     cfg.PURPLE, 48, tex=True, max_width=5.5)
    triangle_count.move_to([3.65, -0.65, 0])
    paced_play(scene, FadeIn(triangle, scale=0.7), run_time=0.9)
    scene.play(
        ReplacementTransform(result, triangle_count),
        run_time=1.1,
    )
    paced_play(
        scene,
        LaggedStart(*[Indicate(vertices[index], color=cfg.PURPLE, scale_factor=1.4) for index in (0, 2, 4)], lag_ratio=0.25),
        run_time=1.8,
    )
    cue(scene, started, 169.0)
    closing = swap_caption(scene, None, "Choose the vertices; geometry builds the object.", cfg.PURPLE)
    paced_play(scene, Indicate(triangle, color=cfg.WHITE, scale_factor=1.04), run_time=1.0)
    cue(scene, started, 178.0)

    end_scene(scene, started, cfg.SCENE_DURATIONS["09"])
