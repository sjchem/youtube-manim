"""Scene 02: before any formula, the one idea underneath all of them."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background, begin_scene, bottom_caption, boxed_statement, cue, end_scene,
    eq, glow_dot, glow_line, outlined_text, paced_play, shirt_icon, swap_caption, top_caption,
    trouser_icon,
)
from utils.render_helpers import column_positions

SHIRT_COLORS = (cfg.RED, cfg.BLUE, cfg.GREEN)
# Two clearly different greys: the tree only reads if the pairs are telling apart.
TROUSER_COLORS = ("#DCE7EF", "#6C8598")
SHOE_COLORS = (cfg.GOLD, cfg.PURPLE)


class Scene02ChoicesMultiply(Scene):
    """Whenever a process happens in stages, the choices multiply."""

    def construct(self) -> None:
        play_scene(self)


def outfit(shirt_color: str, trouser_color: str, scale: float = 0.52) -> VGroup:
    """One complete outcome: a shirt and a pair of trousers, side by side."""
    pair = VGroup(shirt_icon(shirt_color, 1.0), trouser_icon(trouser_color, 0.92))
    pair.arrange(RIGHT, buff=0.1)
    return pair.scale(scale)


def railway_route(start, end, control_y: float, color: str) -> VGroup:
    """A curved railway drawn with two rails and regularly spaced sleepers."""
    gauge = 0.10
    controls = (-2.6, 2.6)
    upper = CubicBezier(
        start + UP * gauge,
        [controls[0], control_y + gauge, 0],
        [controls[1], control_y + gauge, 0],
        end + UP * gauge,
        color=color,
        stroke_width=3.2,
    )
    lower = CubicBezier(
        start + DOWN * gauge,
        [controls[0], control_y - gauge, 0],
        [controls[1], control_y - gauge, 0],
        end + DOWN * gauge,
        color=color,
        stroke_width=3.2,
    )
    sleepers = VGroup(
        *[
            Line(
                lower.point_from_proportion(index / 18),
                upper.point_from_proportion(index / 18),
                color=cfg.MUTED,
                stroke_width=2.6,
                stroke_opacity=0.9,
            )
            for index in range(1, 18)
        ]
    )
    return VGroup(sleepers, upper, lower)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "02")
    add_cinematic_background(scene)

    heading = top_caption("CHOICES  MULTIPLY", cfg.CYAN)

    # --- 0-13s: the wardrobe ------------------------------------------------
    shirts = VGroup(*[shirt_icon(colour, 1.15) for colour in SHIRT_COLORS])
    shirts.arrange(RIGHT, buff=1.0).move_to([0, 1.25, 0])
    shirt_tag = outlined_text("3 SHIRTS", cfg.FONT["label"], cfg.CYAN).next_to(shirts, UP, buff=0.35)

    trousers = VGroup(*[trouser_icon(colour, 1.15) for colour in TROUSER_COLORS])
    trousers.arrange(RIGHT, buff=1.4).move_to([0, -1.6, 0])
    trouser_tag = outlined_text("2 TROUSERS", cfg.FONT["label"], cfg.PURPLE).next_to(trousers, DOWN, buff=0.3)

    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), run_time=0.8)
    paced_play(scene, LaggedStart(*[FadeIn(s, scale=0.7) for s in shirts], lag_ratio=0.25), run_time=1.5)
    paced_play(scene, FadeIn(shirt_tag, shift=DOWN * 0.15), run_time=0.7)
    cue(scene, started, 7.0)
    paced_play(scene, LaggedStart(*[FadeIn(t, scale=0.7) for t in trousers], lag_ratio=0.3), run_time=1.3)
    paced_play(scene, FadeIn(trouser_tag, shift=UP * 0.15), run_time=0.7)
    cue(scene, started, 13.0)

    caption = bottom_caption("How many different outfits?", cfg.GOLD)
    paced_play(scene, FadeOut(trouser_tag), FadeIn(caption, shift=UP * 0.2), run_time=0.9)
    cue(scene, started, 18.0)

    # --- 18-30s: the first stage fans out ------------------------------------
    stage_xs = (-5.55, -1.35, 1.35)
    shirt_ys = [float(point[1]) for point in column_positions(3, span=4.3)]
    paced_play(
        scene,
        FadeOut(heading, trousers, shirt_tag, caption),
        *[
            shirts[index].animate.scale(0.82).move_to([stage_xs[0], shirt_ys[index], 0])
            for index in range(3)
        ],
        run_time=1.4,
    )

    root = glow_dot([-7.0, 0, 0], cfg.CYAN, 0.1)
    first_edges = VGroup(
        *[glow_line([-6.85, 0, 0], [stage_xs[0] - 0.62, y, 0], cfg.CYAN, 4.5) for y in shirt_ys]
    )
    paced_play(scene, FadeIn(root, scale=0.5), run_time=0.5)
    paced_play(scene, LaggedStart(*[Create(edge) for edge in first_edges], lag_ratio=0.25), run_time=1.6)
    step_one = outlined_text("3 WAYS", cfg.FONT["small"], cfg.CYAN).move_to([-6.35, 3.05, 0])
    paced_play(scene, FadeIn(step_one, shift=DOWN * 0.12), run_time=0.7)
    cue(scene, started, 26.0)

    # --- 26-44s: every shirt meets every pair of trousers ---------------------
    leaf_ys = [float(point[1]) for point in column_positions(6, span=5.9)]
    leaves = VGroup()
    second_edges = VGroup()
    for shirt_index, shirt_colour in enumerate(SHIRT_COLORS):
        for trouser_index, trouser_colour in enumerate(TROUSER_COLORS):
            leaf_index = shirt_index * 2 + trouser_index
            look = outfit(shirt_colour, trouser_colour, 0.7)
            look.move_to([stage_xs[2], leaf_ys[leaf_index], 0])
            edge = glow_line(
                [stage_xs[0] + 0.62, shirt_ys[shirt_index], 0],
                [stage_xs[2] - 0.92, leaf_ys[leaf_index], 0],
                trouser_colour,
                3.6,
            )
            leaves.add(look)
            second_edges.add(edge)

    for shirt_index in range(3):
        pair = VGroup(second_edges[2 * shirt_index], second_edges[2 * shirt_index + 1])
        looks = VGroup(leaves[2 * shirt_index], leaves[2 * shirt_index + 1])
        paced_play(
            scene,
            *[Create(edge) for edge in pair],
            LaggedStart(*[FadeIn(look, shift=RIGHT * 0.3) for look in looks], lag_ratio=0.3),
            run_time=1.6,
        )
    step_two = outlined_text("2 WAYS EACH", cfg.FONT["small"], cfg.PURPLE).move_to([-3.45, -3.55, 0])
    paced_play(scene, FadeIn(step_two, shift=DOWN * 0.12), run_time=0.7)
    cue(scene, started, 38.0)

    # --- 38-54s: count what the tree produced --------------------------------
    numbers = VGroup()
    for index, y in enumerate(leaf_ys):
        tag = outlined_text(str(index + 1), cfg.FONT["label"], cfg.GOLD)
        tag.move_to([stage_xs[2] + 1.5, y, 0])
        numbers.add(tag)
    paced_play(
        scene,
        LaggedStart(*[FadeIn(tag, scale=0.6) for tag in numbers], lag_ratio=0.32),
        run_time=3.2,
    )
    cue(scene, started, 44.0)

    total = eq("6", cfg.GOLD, 120).move_to([5.4, 1.35, 0])
    total_tag = outlined_text("OUTFITS", cfg.FONT["small"], cfg.GOLD).next_to(total, DOWN, buff=0.28)
    paced_play(scene, FadeIn(total, scale=1.3), FadeIn(total_tag), run_time=1.0)
    cue(scene, started, 50.0)

    # --- 50-66s: the count is a product --------------------------------------
    product = VGroup(
        eq("3", cfg.CYAN, 84),
        eq(r"\times", cfg.MUTED, 72),
        eq("2", cfg.PURPLE, 84),
        eq("=", cfg.MUTED, 72),
        eq("6", cfg.GOLD, 84),
    ).arrange(RIGHT, buff=0.3).move_to([5.05, -1.5, 0])
    paced_play(scene, FadeIn(product[0], shift=UP * 0.2), Indicate(step_one, color=cfg.WHITE), run_time=1.0)
    paced_play(scene, FadeIn(VGroup(product[1], product[2]), shift=UP * 0.2), Indicate(step_two, color=cfg.WHITE), run_time=1.1)
    paced_play(scene, FadeIn(VGroup(product[3], product[4]), shift=UP * 0.2), run_time=0.9)
    paced_play(scene, Indicate(product[4], color=cfg.WHITE, scale_factor=1.15), run_time=0.9)
    cue(scene, started, 62.0)

    # --- 62-80s: strip the clothes away, keep the structure -------------------
    scene.play(
        FadeOut(leaves, numbers, second_edges, first_edges, root, shirts, total, total_tag, step_one, step_two),
        product.animate.move_to([0, -2.35, 0]).scale(1.05),
        run_time=1.5,
    )

    stage_boxes = VGroup()
    for index, (count, colour, name) in enumerate(
        ((3, cfg.CYAN, "STEP 1"), (2, cfg.PURPLE, "STEP 2"))
    ):
        dots = VGroup(*[glow_dot(ORIGIN, colour, 0.14) for _ in range(count)])
        dots.arrange(DOWN, buff=0.45)
        frame = RoundedRectangle(
            width=2.9, height=3.1, corner_radius=0.22,
            stroke_color=colour, stroke_width=4, fill_color=cfg.PANEL, fill_opacity=0.55,
        )
        dots.move_to(frame.get_center())
        tag = outlined_text(name, cfg.FONT["small"], colour).next_to(frame, UP, buff=0.26)
        count_tag = eq(f"{count}", colour, 72).next_to(frame, DOWN, buff=0.26)
        box = VGroup(frame, dots, tag, count_tag)
        stage_boxes.add(box)
    stage_boxes.arrange(RIGHT, buff=2.6).move_to([0, 0.95, 0])

    times = eq(r"\times", cfg.WHITE, 90).move_to(
        [(stage_boxes[0].get_right()[0] + stage_boxes[1].get_left()[0]) / 2, 0.95, 0]
    )
    paced_play(scene, LaggedStart(*[FadeIn(box, scale=0.85) for box in stage_boxes], lag_ratio=0.35), run_time=1.8)
    paced_play(scene, FadeIn(times, scale=1.4), run_time=0.8)
    cue(scene, started, 72.0)

    fan = VGroup()
    left_dots = stage_boxes[0][1]
    right_dots = stage_boxes[1][1]
    for left in left_dots:
        for right in right_dots:
            fan.add(
                Line(left.get_center(), right.get_center(), color=cfg.GOLD, stroke_width=2.4, stroke_opacity=0.5)
            )
    paced_play(scene, LaggedStart(*[Create(line) for line in fan], lag_ratio=0.12), run_time=2.4)
    six = outlined_text("6 PATHS", cfg.FONT["label"], cfg.GOLD).move_to([0, 3.35, 0])
    paced_play(scene, FadeIn(six, shift=DOWN * 0.15), run_time=0.8)
    cue(scene, started, 80.0)

    # --- 80-94s: the rule that everything else is built on --------------------
    rule = boxed_statement(
        r"\text{total} = (\text{step 1})\times(\text{step 2})\times\cdots",
        cfg.GOLD,
        cfg.FONT["section"],
        tex=True,
    )
    rule.move_to([0, 0.6, 0])
    scene.play(
        FadeOut(stage_boxes, times, fan, six, product),
        FadeIn(rule, scale=0.9),
        run_time=1.6,
    )
    line = swap_caption(scene, None, "Same number of choices on every branch: multiply.", cfg.CYAN)
    cue(scene, started, 90.0)

    # --- 90-111s: one more stage, to show it never stops ----------------------
    shoes = VGroup(
        *[
            VGroup(
                Ellipse(width=0.86, height=0.42, color=colour, stroke_width=4, fill_color=colour, fill_opacity=0.28),
                Arc(radius=0.3, start_angle=PI * 0.15, angle=PI * 0.7, color=colour, stroke_width=4).shift(LEFT * 0.16 + UP * 0.1),
            )
            for colour in SHOE_COLORS
        ]
    )
    shoes.arrange(RIGHT, buff=0.7).move_to([0, 1.55, 0])
    shoe_tag = outlined_text("NOW ADD 2 PAIRS OF SHOES", cfg.FONT["small"], cfg.GOLD)
    shoe_tag.next_to(shoes, UP, buff=0.3)
    scene.play(
        rule.animate.scale(0.82).move_to([0, -1.35, 0]),
        FadeIn(shoes, scale=0.8),
        FadeIn(shoe_tag, shift=DOWN * 0.12),
        FadeOut(line),
        run_time=1.4,
    )
    grown = VGroup(
        eq("3", cfg.CYAN, 78),
        eq(r"\times", cfg.MUTED, 66),
        eq("2", cfg.PURPLE, 78),
        eq(r"\times", cfg.MUTED, 66),
        eq("2", cfg.GOLD, 78),
        eq("=", cfg.MUTED, 66),
        eq("12", cfg.WHITE, 90),
    ).arrange(RIGHT, buff=0.28).move_to([0, -0.15, 0])
    paced_play(scene, FadeIn(VGroup(*grown[:3]), shift=UP * 0.2), run_time=1.0)
    paced_play(scene, FadeIn(VGroup(grown[3], grown[4]), shift=UP * 0.2), run_time=1.0)
    paced_play(scene, FadeIn(VGroup(grown[5], grown[6]), scale=1.2), run_time=1.0)
    cue(scene, started, 100.0)
    paced_play(scene, Indicate(grown[6], color=cfg.GOLD, scale_factor=1.12), run_time=1.0)
    closing = swap_caption(scene, None, "Every new stage multiplies what came before.", cfg.CYAN)
    cue(scene, started, 108.0)
    paced_play(scene, Indicate(rule, color=cfg.WHITE, scale_factor=1.03), run_time=1.2)
    scene.remove(closing)
    scene.add(closing)

    cue(scene, started, 111.0)
    scene.play(FadeOut(rule, shoes, shoe_tag, grown, closing), run_time=1.1)

    # --- 112-176s: the companion principle — alternatives add ---------------
    heading_or = top_caption("ALTERNATIVES  ADD", cfg.PURPLE)
    question = outlined_text("Travel to school", cfg.FONT["body"], cfg.WHITE)
    question.move_to([0, 2.55, 0])
    paced_play(scene, FadeIn(heading_or, shift=DOWN * 0.15), FadeIn(question), run_time=1.0)

    origin = glow_dot([-5.8, 0.4, 0], cfg.WHITE, 0.16)
    school = glow_dot([5.8, 0.4, 0], cfg.GOLD, 0.2)
    home_tag = outlined_text("HOME", cfg.FONT["small"], cfg.WHITE).next_to(origin, DOWN, buff=0.28)
    school_tag = outlined_text("SCHOOL", cfg.FONT["small"], cfg.GOLD).next_to(school, DOWN, buff=0.28)
    paced_play(scene, FadeIn(origin, scale=0.5), FadeIn(school, scale=0.5),
               FadeIn(home_tag), FadeIn(school_tag), run_time=1.0)
    cue(scene, started, 121.0)

    routes = VGroup(*[
        CubicBezier(origin.get_center(), [-2.6, y, 0], [2.6, y, 0], school.get_center(),
                    color=cfg.CYAN, stroke_width=5)
        for y in (1.0, 0.4, -0.2)
    ])
    bus_tag = outlined_text("3 BUS ROUTES", cfg.FONT["small"], cfg.CYAN).move_to([0, 1.9, 0])
    paced_play(scene, LaggedStart(*[Create(route) for route in routes], lag_ratio=0.3), run_time=2.2)
    paced_play(scene, FadeIn(bus_tag, shift=DOWN * 0.15), run_time=0.8)
    cue(scene, started, 133.0)

    train_routes = VGroup(
        railway_route(origin.get_center(), school.get_center(), 1.72, cfg.PURPLE),
        railway_route(origin.get_center(), school.get_center(), -1.08, cfg.PURPLE),
    )
    train_tag = outlined_text("2 TRAIN ROUTES", cfg.FONT["small"], cfg.PURPLE).move_to([0, -1.3, 0])
    paced_play(scene, LaggedStart(*[Create(route) for route in train_routes], lag_ratio=0.35), run_time=1.8)
    paced_play(scene, FadeIn(train_tag, shift=UP * 0.15), run_time=0.8)
    cue(scene, started, 145.0)

    plus = eq("3+2=5", cfg.GOLD, 108).move_to([0, -2.75, 0])
    or_tag = outlined_text("BUS  OR  TRAIN", cfg.FONT["label"], cfg.GOLD).next_to(plus, UP, buff=0.28)
    paced_play(scene, FadeIn(or_tag), FadeIn(plus, scale=1.2), run_time=1.1)
    paced_play(scene, Indicate(plus, color=cfg.WHITE, scale_factor=1.08), run_time=1.0)
    cue(scene, started, 155.0)

    comparison = VGroup(
        boxed_statement(r"\text{OR}\;\longrightarrow\;\text{ADD}", cfg.PURPLE, cfg.FONT["section"], tex=True),
        boxed_statement(r"\text{AND}\;\longrightarrow\;\text{MULTIPLY}", cfg.CYAN, cfg.FONT["section"], tex=True),
    ).arrange(DOWN, buff=0.55).move_to(ORIGIN)
    scene.play(FadeOut(question, origin, school, home_tag, school_tag, routes, train_routes,
                       bus_tag, train_tag, or_tag, plus),
               FadeIn(comparison[0], shift=RIGHT * 0.25), run_time=1.2)
    paced_play(scene, FadeIn(comparison[1], shift=LEFT * 0.25), run_time=1.0)
    cue(scene, started, 168.0)
    bridge = swap_caption(scene, None, "Next: choices that shrink after every pick.", cfg.GOLD)
    paced_play(scene, Indicate(comparison[1], color=cfg.WHITE, scale_factor=1.04), run_time=1.0)
    cue(scene, started, 175.0)

    end_scene(scene, started, cfg.SCENE_DURATIONS["02"])
