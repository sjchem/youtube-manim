"""Scene 10: choosing three is the same act as leaving seven behind."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background, begin_scene, boxed_statement, cue, end_scene, eq,
    outlined_text, paced_play, swap_caption, top_caption,
)
from utils.math_utils import combinations

CLASS_SIZE = 10
PICKED = 3


class Scene10Symmetry(Scene):
    """nCr = nC(n-r), seen rather than proved."""

    def construct(self) -> None:
        play_scene(self)


def student_dot(colour: str = cfg.AVAILABLE, radius: float = 0.4) -> VGroup:
    halo = Circle(radius=radius * 1.35, color=colour, stroke_width=0, fill_color=colour, fill_opacity=0.1)
    disc = Circle(radius=radius, color=colour, stroke_width=4.5, fill_color=cfg.PANEL, fill_opacity=0.9)
    group = VGroup(halo, disc)
    group.halo = halo
    group.disc = disc
    return group


def repaint(dot: VGroup, colour: str, *, fill: float = 0.1, dim: bool = False) -> VGroup:
    fresh = dot.copy()
    fresh.halo.set_fill(colour, opacity=0.0 if dim else fill)
    fresh.disc.set_stroke(colour, width=3 if dim else 5.5)
    fresh.disc.set_fill(cfg.PANEL if dim else colour, opacity=0.5 if dim else 0.3)
    if dim:
        fresh.set_opacity(0.3)
    return fresh


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "10")
    add_cinematic_background(scene)

    heading = top_caption("CHOOSING  IS  ALSO  LEAVING  BEHIND", cfg.UNORDERED)

    # --- 0-12s: ten students --------------------------------------------------
    dots = VGroup(*[student_dot() for _ in range(CLASS_SIZE)])
    dots.arrange(RIGHT, buff=0.34).move_to([0, 2.15, 0])
    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), run_time=0.8)
    paced_play(scene, LaggedStart(*[FadeIn(d, scale=0.6) for d in dots], lag_ratio=0.12), run_time=2.2)
    count_tag = eq("10", cfg.CYAN, 78).move_to([0, -0.1, 0])
    tag_word = outlined_text("STUDENTS", cfg.FONT["small"], cfg.CYAN).next_to(count_tag, DOWN, buff=0.22)
    paced_play(scene, FadeIn(count_tag, scale=1.2), FadeIn(tag_word), run_time=1.0)
    caption = swap_caption(scene, None, "Ten students. Choose three for the trip.", cfg.CYAN)
    cue(scene, started, 12.0)

    # --- 12-30s: choose three ------------------------------------------------
    chosen_indices = (1, 4, 7)
    scene.play(FadeOut(heading, count_tag, tag_word), run_time=0.6)
    for index in chosen_indices:
        paced_play(
            scene,
            Transform(dots[index], repaint(dots[index], cfg.UNORDERED, fill=0.22)),
            run_time=0.8,
        )
    # Dimming the rest makes the chosen three unmistakable before the flip.
    left_behind = [index for index in range(CLASS_SIZE) if index not in chosen_indices]
    paced_play(
        scene,
        *[Transform(dots[index], repaint(dots[index], cfg.SPENT, dim=True)) for index in left_behind],
        run_time=0.9,
    )
    chosen_label = eq(r"\binom{10}{3}", cfg.UNORDERED, 88).move_to([-4.4, -1.35, 0])
    paced_play(scene, FadeIn(chosen_label, scale=1.2), run_time=1.0)
    chosen_value = eq(f"= {combinations(10, 3)}", cfg.UNORDERED, 76).next_to(chosen_label, RIGHT, buff=0.45)
    paced_play(scene, FadeIn(chosen_value, shift=RIGHT * 0.25), run_time=0.9)
    cue(scene, started, 26.0)

    # --- 26-46s: the seven are already decided --------------------------------
    caption = swap_caption(scene, caption, "The moment you choose three, seven are decided too.", cfg.GOLD)
    paced_play(
        scene,
        LaggedStart(
            *[Transform(dots[index], repaint(dots[index], cfg.GOLD, fill=0.18)) for index in left_behind],
            lag_ratio=0.14,
        ),
        run_time=2.4,
    )
    seven = VGroup(
        eq("7", cfg.GOLD, 76),
        outlined_text("LEFT BEHIND", cfg.FONT["tiny"], cfg.GOLD),
    ).arrange(RIGHT, buff=0.3).move_to([3.3, 0.55, 0])
    three = VGroup(
        eq("3", cfg.UNORDERED, 76),
        outlined_text("CHOSEN", cfg.FONT["tiny"], cfg.UNORDERED),
    ).arrange(RIGHT, buff=0.3).move_to([-3.3, 0.55, 0])
    paced_play(scene, FadeIn(three, shift=RIGHT * 0.2), run_time=0.7)
    paced_play(scene, FadeIn(seven, shift=LEFT * 0.2), run_time=0.7)
    cue(scene, started, 40.0)

    # --- 40-58s: invert the highlight ------------------------------------------
    caption = swap_caption(scene, caption, "Flip which side you look at. Nothing else changes.", cfg.PURPLE)
    other_label = eq(r"\binom{10}{7}", cfg.GOLD, 88).move_to([2.5, -1.35, 0])
    other_value = eq(f"= {combinations(10, 7)}", cfg.GOLD, 76).next_to(other_label, RIGHT, buff=0.45)
    paced_play(scene, FadeIn(other_label, scale=1.2), run_time=1.0)
    paced_play(scene, FadeIn(other_value, shift=RIGHT * 0.25), run_time=0.9)
    cue(scene, started, 50.0)

    equal_sign = eq("=", cfg.PURPLE, 96).move_to([0, -1.35, 0])
    paced_play(
        scene,
        Indicate(chosen_value, color=cfg.UNORDERED, scale_factor=1.1),
        Indicate(other_value, color=cfg.GOLD, scale_factor=1.1),
        run_time=1.0,
    )
    paced_play(scene, FadeIn(equal_sign, scale=1.4), run_time=0.9)
    paced_play(scene, Indicate(equal_sign, color=cfg.WHITE, scale_factor=1.2), run_time=1.0)
    cue(scene, started, 58.0)

    # --- 58-70s: the general statement ------------------------------------------
    general = boxed_statement(r"\binom{n}{r} = \binom{n}{n-r}", cfg.PURPLE, 88, tex=True)
    general.move_to([0, -1.5, 0])
    scene.play(
        FadeOut(chosen_label, chosen_value, other_label, other_value, equal_sign, three, seven),
        FadeIn(general, scale=0.92),
        run_time=1.4,
    )
    cue(scene, started, 66.0)

    # --- 66-87s: the whole row, and its mirror ----------------------------------
    caption = swap_caption(scene, caption, "Every row of choices is a mirror.", cfg.PURPLE)
    scene.play(
        FadeOut(dots),
        general.animate.scale(0.72).move_to([0, 3.2, 0]),
        run_time=1.3,
    )

    values = [combinations(CLASS_SIZE, r) for r in range(CLASS_SIZE + 1)]
    tallest = max(values)
    bars = VGroup()
    labels = VGroup()
    base_y = -2.85
    for r, value in enumerate(values):
        height = 0.25 + 3.9 * value / tallest
        colour = cfg.UNORDERED if r in (3, 7) else cfg.PURPLE
        bar = RoundedRectangle(
            width=0.86, height=height, corner_radius=0.08,
            stroke_color=colour, stroke_width=3,
            fill_color=colour, fill_opacity=0.3,
        )
        bar.move_to([-5.6 + 1.12 * r, base_y + height / 2, 0])
        tag = outlined_text(str(r), cfg.FONT["tiny"], cfg.MUTED)
        tag.next_to(bar, DOWN, buff=0.16)
        bars.add(bar)
        labels.add(tag)
    axis = Line([-6.5, base_y, 0], [6.5, base_y, 0], color=cfg.MUTED, stroke_width=3, stroke_opacity=0.5)
    mirror = DashedLine([0, base_y - 0.1, 0], [0, base_y + 4.5, 0], color=cfg.GOLD, stroke_width=4, dash_length=0.16)

    paced_play(scene, Create(axis), run_time=0.6)
    paced_play(
        scene,
        LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.12),
        LaggedStart(*[FadeIn(tag) for tag in labels], lag_ratio=0.12),
        run_time=3.4,
    )
    paced_play(scene, Create(mirror), run_time=0.9)
    paced_play(
        scene,
        Indicate(bars[3], color=cfg.WHITE, scale_factor=1.06),
        Indicate(bars[7], color=cfg.WHITE, scale_factor=1.06),
        run_time=1.3,
    )
    cue(scene, started, 84.0)
    paced_play(scene, Indicate(general, color=cfg.WHITE, scale_factor=1.05), run_time=1.2)

    end_scene(scene, started, cfg.SCENE_DURATIONS["10"])
