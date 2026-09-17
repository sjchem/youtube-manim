"""Scene 06: restricted arrangements through blocks and gaps."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background, begin_scene, boxed_statement, cue, end_scene, eq,
    outlined_text, paced_play, swap_caption, top_caption,
)


class Scene06BlockGap(Scene):
    """Make restrictions visible, then count the visible structure."""

    def construct(self) -> None:
        play_scene(self)


def letter_tile(letter: str, color: str) -> VGroup:
    box = RoundedRectangle(
        width=1.25, height=1.25, corner_radius=0.14,
        stroke_color=color, stroke_width=4,
        fill_color=cfg.PANEL, fill_opacity=0.78,
    )
    glyph = outlined_text(letter, 54, color).move_to(box)
    return VGroup(box, glyph)


def student_figure(kind: str, color: str, variant: int = 0, scale: float = 1.0) -> VGroup:
    """Small, readable cartoon students for the gap-method demonstration."""
    skin = ("#F4C7A1", "#C98F65", "#8D5A43")[variant % 3]
    hair_color = ("#38261D", "#7A4B2A", "#182A3A")[variant % 3]

    head = Circle(
        radius=0.21, color=cfg.WHITE, stroke_width=2.4,
        fill_color=skin, fill_opacity=1,
    ).move_to([0, 0.43, 0])
    eyes = VGroup(
        Dot([-0.075, 0.45, 0], radius=0.018, color=cfg.BG),
        Dot([0.075, 0.45, 0], radius=0.018, color=cfg.BG),
    )
    smile = Arc(radius=0.075, start_angle=PI, angle=PI, color=cfg.BG, stroke_width=2)
    smile.move_to([0, 0.37, 0])
    hair = Arc(radius=0.205, start_angle=0, angle=PI, color=hair_color, stroke_width=8)
    hair.move_to([0, 0.49, 0])

    arms = VGroup(
        Line([-0.2, 0.05, 0], [-0.38, -0.21, 0], color=skin, stroke_width=5),
        Line([0.2, 0.05, 0], [0.38, -0.21, 0], color=skin, stroke_width=5),
    )
    legs = VGroup(
        Line([-0.11, -0.43, 0], [-0.14, -0.73, 0], color=cfg.WHITE, stroke_width=5),
        Line([0.11, -0.43, 0], [0.14, -0.73, 0], color=cfg.WHITE, stroke_width=5),
    )

    if kind == "girl":
        body = Polygon(
            [-0.19, 0.16, 0], [0.19, 0.16, 0], [0.34, -0.47, 0], [-0.34, -0.47, 0],
            color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.68,
        )
        pigtails = VGroup(
            Circle(radius=0.075, color=hair_color, stroke_width=2,
                   fill_color=hair_color, fill_opacity=1).move_to([-0.24, 0.38, 0]),
            Circle(radius=0.075, color=hair_color, stroke_width=2,
                   fill_color=hair_color, fill_opacity=1).move_to([0.24, 0.38, 0]),
        )
        clip_x = -0.17 if variant % 2 == 0 else 0.17
        clip = Dot([clip_x, 0.58, 0], radius=0.045, color=cfg.GOLD if variant % 2 == 0 else cfg.ORANGE)
        figure = VGroup(legs, arms, body, pigtails, head, hair, clip, eyes, smile)
    else:
        body = RoundedRectangle(
            width=0.5, height=0.6, corner_radius=0.1,
            color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.62,
        ).move_to([0, -0.15, 0])
        collar = Line([-0.13, 0.11, 0], [0.13, 0.11, 0], color=cfg.WHITE, stroke_width=2.2)
        figure = VGroup(legs, arms, body, collar, head, hair, eyes, smile)

    return figure.scale(scale)


def gentle_bob(scene: Scene, figures: Mobject, run_time: float = 2.2) -> None:
    """Keep a narrated composition alive without distracting from the count."""
    scene.play(
        *[
            figure.animate.shift(UP * (0.07 + 0.015 * (index % 2))).rotate(0.018 * (-1) ** index)
            for index, figure in enumerate(figures)
        ],
        run_time=run_time,
        rate_func=there_and_back,
    )


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "06")
    add_cinematic_background(scene)

    heading = top_caption("WHEN  ARRANGEMENTS  HAVE  RULES", cfg.ORANGE)
    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), run_time=0.8)

    # --- 0-78s: block method -------------------------------------------------
    prompt = outlined_text("Arrange MATH — keep A and T together", cfg.FONT["body"], cfg.WHITE)
    prompt.move_to([0, 2.6, 0])
    tiles = VGroup(
        letter_tile("M", cfg.CYAN), letter_tile("A", cfg.GOLD),
        letter_tile("T", cfg.GOLD), letter_tile("H", cfg.PURPLE),
    ).arrange(RIGHT, buff=0.5).move_to([0, 0.85, 0])
    paced_play(scene, FadeIn(prompt, shift=UP * 0.15), run_time=0.8)
    paced_play(scene, LaggedStart(*[FadeIn(tile, scale=0.7) for tile in tiles], lag_ratio=0.2), run_time=1.5)
    caption = swap_caption(scene, None, "The restriction becomes a shape we can move.", cfg.GOLD)
    scene.play(
        tiles[1].animate.shift(UP * 0.08),
        tiles[2].animate.shift(UP * 0.08),
        run_time=1.8,
        rate_func=there_and_back,
    )
    cue(scene, started, 14.0)

    block = SurroundingRectangle(VGroup(tiles[1], tiles[2]), color=cfg.GOLD,
                                 buff=0.18, corner_radius=0.18, stroke_width=6)
    block_tag = outlined_text("ONE BLOCK", cfg.FONT["small"], cfg.GOLD).next_to(block, DOWN, buff=0.25)
    paced_play(scene, Create(block), FadeIn(block_tag),
               FadeOut(heading, shift=UP * 0.15), run_time=1.1)
    scene.play(
        VGroup(tiles[1], tiles[2], block, block_tag).animate.shift(RIGHT * 0.34),
        run_time=2.2,
        rate_func=there_and_back,
    )
    cue(scene, started, 25.0)

    objects = VGroup(
        tiles[0].copy(), VGroup(tiles[1].copy(), tiles[2].copy(), block.copy()), tiles[3].copy()
    )
    objects[1][0:2].arrange(RIGHT, buff=0.12)
    objects[1][2].surround(objects[1][0:2], buff=0.16)
    objects.arrange(RIGHT, buff=0.8).move_to([0, 0.65, 0])
    scene.play(FadeOut(tiles, block, block_tag), FadeIn(objects, scale=0.85), run_time=1.2)
    three = eq("3!", cfg.CYAN, 104).move_to([-2.2, -1.65, 0])
    three_tag = outlined_text("ARRANGE 3 OBJECTS", cfg.FONT["tiny"], cfg.CYAN).next_to(three, DOWN, buff=0.22)
    paced_play(scene, FadeIn(three, scale=1.2), FadeIn(three_tag), run_time=1.0)
    scene.play(
        LaggedStart(*[Indicate(item, color=cfg.CYAN, scale_factor=1.06) for item in objects], lag_ratio=0.25),
        run_time=2.1,
    )
    cue(scene, started, 40.0)

    reversed_pair = VGroup(letter_tile("T", cfg.GOLD), letter_tile("A", cfg.GOLD))
    reversed_pair.arrange(RIGHT, buff=0.12).move_to(objects[1][0:2])
    paced_play(scene, ReplacementTransform(objects[1][0:2], reversed_pair), run_time=1.2,
               path_arc=PI / 2)
    inside = eq("2!", cfg.GOLD, 104).move_to([2.2, -1.65, 0])
    inside_tag = outlined_text("ORDER INSIDE", cfg.FONT["tiny"], cfg.GOLD).next_to(inside, DOWN, buff=0.22)
    paced_play(scene, FadeIn(inside, scale=1.2), FadeIn(inside_tag), run_time=1.0)
    paced_play(scene, Indicate(reversed_pair, color=cfg.GOLD, scale_factor=1.06), run_time=1.6)
    cue(scene, started, 53.0)

    answer = boxed_statement(r"3!\times2!=12", cfg.GREEN, 94, tex=True).move_to([0, 0.45, 0])
    scene.play(FadeOut(prompt, objects, reversed_pair, three, three_tag, inside, inside_tag),
               FadeIn(answer, scale=0.9), run_time=1.2)
    caption = swap_caption(scene, caption, "Keep together: bind a block, then count it.", cfg.GREEN)
    cue(scene, started, 70.0)
    paced_play(scene, Indicate(answer, color=cfg.WHITE, scale_factor=1.06), run_time=1.0)

    # --- 78-179s: gap method -------------------------------------------------
    scene.play(FadeOut(answer, caption), run_time=1.0)
    gap_heading = top_caption("KEEP  TWO  GIRLS  APART", cfg.PURPLE)
    boys = VGroup(*[student_figure("boy", cfg.CYAN, i, 1.0) for i in range(3)])
    for boy, x in zip(boys, (-3.1, 0.0, 3.1)):
        boy.move_to([x, 1.05, 0])
    paced_play(scene, FadeIn(gap_heading, shift=DOWN * 0.15), run_time=0.8)
    paced_play(scene, LaggedStart(*[FadeIn(boy, scale=0.7) for boy in boys], lag_ratio=0.25), run_time=1.3)
    boys_count = eq("3!", cfg.CYAN, 88).move_to([5.75, 1.05, 0])
    paced_play(scene, FadeIn(boys_count, shift=LEFT * 0.2), run_time=0.8)
    gentle_bob(scene, boys)
    cue(scene, started, 92.0)

    gaps = VGroup()
    gap_xs = [-4.7, -1.55, 1.55, 4.7]
    for index, x in enumerate(gap_xs):
        marker = DashedVMobject(
            RoundedRectangle(width=1.05, height=1.55, corner_radius=0.14,
                             color=cfg.GOLD, stroke_width=3), num_dashes=12,
        ).move_to([x, 1.05, 0])
        number = outlined_text(str(index + 1), cfg.FONT["tiny"], cfg.GOLD).next_to(marker, DOWN, buff=0.18)
        gaps.add(VGroup(marker, number))
    paced_play(scene, LaggedStart(*[FadeIn(gap) for gap in gaps], lag_ratio=0.2),
               FadeOut(gap_heading, shift=UP * 0.15), run_time=1.5)
    caption = swap_caption(scene, None, "Three arranged boys create four safe gaps.", cfg.GOLD)
    scene.play(
        LaggedStart(*[Indicate(gap[0], color=cfg.GOLD, scale_factor=1.04) for gap in gaps], lag_ratio=0.22),
        run_time=2.4,
    )
    cue(scene, started, 108.0)
    paced_play(scene, FadeOut(caption), run_time=0.6)
    caption = None

    choose = eq(r"\binom{4}{2}", cfg.GOLD, 100).move_to([-2.0, -1.55, 0])
    choose_tag = outlined_text("CHOOSE 2 GAPS", cfg.FONT["tiny"], cfg.GOLD).next_to(choose, DOWN, buff=0.2)
    paced_play(scene, Indicate(gaps[0], color=cfg.WHITE), Indicate(gaps[2], color=cfg.WHITE), run_time=1.0)
    girls = VGroup(
        student_figure("girl", cfg.PURPLE, 0, 0.95),
        student_figure("girl", cfg.PURPLE, 1, 0.95),
    )
    girls[0].move_to(gaps[0][0]); girls[1].move_to(gaps[2][0])
    paced_play(scene, FadeIn(girls, scale=0.65), FadeIn(choose), FadeIn(choose_tag), run_time=1.1)
    gentle_bob(scene, girls)
    cue(scene, started, 126.0)

    arrange = eq("2!", cfg.PURPLE, 100).move_to([2.0, -1.55, 0])
    arrange_tag = outlined_text("ARRANGE THE GIRLS", cfg.FONT["tiny"], cfg.PURPLE).next_to(arrange, DOWN, buff=0.2)
    paced_play(scene, Swap(girls[0], girls[1], path_arc=PI / 2), run_time=1.2)
    paced_play(scene, FadeIn(arrange), FadeIn(arrange_tag), run_time=0.8)
    paced_play(scene, Indicate(VGroup(girls, arrange), color=cfg.PURPLE, scale_factor=1.04), run_time=1.7)
    cue(scene, started, 141.0)

    result = boxed_statement(r"3!\times\binom{4}{2}\times2!=72", cfg.GREEN, 82, tex=True)
    result.move_to([0, -1.65, 0])
    scene.play(FadeOut(choose, choose_tag, arrange, arrange_tag),
               FadeIn(result, shift=UP * 0.2), run_time=1.1)
    paced_play(scene, Indicate(result, color=cfg.WHITE, scale_factor=1.035), run_time=1.8)
    cue(scene, started, 154.0)

    summary = VGroup(
        boxed_statement("TOGETHER  →  BLOCK", cfg.ORANGE, cfg.FONT["body"]),
        boxed_statement("APART  →  GAPS", cfg.PURPLE, cfg.FONT["body"]),
    ).arrange(DOWN, buff=0.48).move_to([0, -1.45, 0])
    scene.play(FadeOut(boys, boys_count, gaps, girls, result), FadeIn(summary), run_time=1.2)
    caption = swap_caption(scene, None, "Draw the restriction before choosing a formula.", cfg.GOLD)
    cue(scene, started, 171.0)
    paced_play(scene, Indicate(summary, color=cfg.WHITE, scale_factor=1.03), run_time=1.0)
    cue(scene, started, 178.0)

    end_scene(scene, started, cfg.SCENE_DURATIONS["06"])
