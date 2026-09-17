"""Scene 08: three quick situations, and the rule that connects them."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background, begin_scene, boxed_statement, cue, dashed_ring, end_scene,
    eq, outlined_text, paced_play, person_icon, team_ring, top_caption,
)


class Scene08Quiz(Scene):
    """Permutation or combination? Decide by swapping two things."""

    def construct(self) -> None:
        play_scene(self)


def digit_box(value: str, colour: str = cfg.ORANGE, size: float = 1.15) -> VGroup:
    box = RoundedRectangle(
        width=size, height=size * 1.15, corner_radius=0.14,
        stroke_color=colour, stroke_width=4, fill_color=cfg.PANEL, fill_opacity=0.8,
    )
    glyph = outlined_text(value, int(size * 52), colour).move_to(box.get_center())
    group = VGroup(box, glyph)
    group.box = box
    group.glyph = glyph
    return group


def pizza(toppings: list[str], radius: float = 1.75) -> VGroup:
    """A pizza whose three toppings can be rearranged without changing anything."""
    base = Circle(radius=radius, color=cfg.GOLD, stroke_width=5,
                  fill_color="#C88A3A", fill_opacity=0.32)
    crust = Circle(radius=radius * 0.86, color=cfg.GOLD, stroke_width=2.4, stroke_opacity=0.5, fill_opacity=0)
    pieces = VGroup()
    for index, kind in enumerate(toppings):
        angle = TAU * index / len(toppings) + PI / 2
        spot = base.get_center() + radius * 0.48 * np.array([np.cos(angle), np.sin(angle), 0])
        if kind == "mushroom":
            item = VGroup(
                Arc(radius=0.3, start_angle=0, angle=PI, color="#E9DCC8", stroke_width=4,
                    fill_color="#E9DCC8", fill_opacity=0.65),
                Rectangle(width=0.16, height=0.22, color="#E9DCC8", stroke_width=3,
                          fill_color="#E9DCC8", fill_opacity=0.5).shift(DOWN * 0.13),
            )
        elif kind == "olive":
            item = VGroup(
                Circle(radius=0.24, color="#2F4858", stroke_width=4, fill_color="#20323F", fill_opacity=0.95),
                Circle(radius=0.09, color=cfg.RED, stroke_width=2.5, fill_color=cfg.RED, fill_opacity=0.7),
            )
        else:
            item = Polygon(
                [-0.26, -0.2, 0], [0.26, -0.2, 0], [0.0, 0.28, 0],
                color="#FFE29A", stroke_width=4, fill_color="#FFE29A", fill_opacity=0.6,
            )
        item.move_to(spot)
        pieces.add(item)
    group = VGroup(base, crust, pieces)
    group.base = base
    group.pieces = pieces
    return group


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "08")
    add_cinematic_background(scene)

    heading = top_caption("PERMUTATION  OR  COMBINATION?", cfg.GOLD)

    # --- 0-5s: the rule of the game ------------------------------------------
    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), run_time=0.7)
    prompt = VGroup(
        outlined_text("Three quick situations", cfg.FONT["body"], cfg.WHITE),
        outlined_text("Does a swap change the outcome?", cfg.FONT["small"], cfg.CYAN),
    ).arrange(DOWN, buff=0.26).move_to([0, 0.05, 0])
    paced_play(scene, FadeIn(prompt[0], shift=UP * 0.15), run_time=0.7)
    paced_play(scene, FadeIn(prompt[1], shift=UP * 0.15), run_time=0.7)
    cue(scene, started, 5.0)
    paced_play(scene, FadeOut(prompt, heading, shift=UP * 0.2), run_time=0.7)

    def question_caption(text: str, current: Mobject | None = None, colour: str = cfg.WHITE) -> Text:
        fresh = outlined_text(text, cfg.FONT["label"], colour).to_edge(UP, buff=0.42)
        if current is None:
            paced_play(scene, FadeIn(fresh, shift=UP * 0.12), run_time=0.5)
        else:
            paced_play(
                scene,
                FadeOut(current, shift=UP * 0.1),
                FadeIn(fresh, shift=UP * 0.1),
                run_time=0.55,
            )
        return fresh

    def countdown(label_position=(0, -2.9, 0)) -> None:
        """Three compact beats of thinking time."""
        current = None
        for value, colour in (("3", cfg.CYAN), ("2", cfg.GOLD), ("1", cfg.ORANGE)):
            glyph = outlined_text(value, cfg.FONT["body"], colour).move_to(np.array(label_position))
            ring = dashed_ring(np.array(label_position), 0.48, colour, 14, 3.5)
            fresh = VGroup(ring, glyph)
            if current is None:
                paced_play(scene, FadeIn(fresh, scale=1.2), run_time=0.55)
            else:
                paced_play(scene, ReplacementTransform(current, fresh), run_time=0.55)
            current = fresh
        paced_play(scene, FadeOut(current, scale=0.7), run_time=0.3)

    def verdict(word: str, colour: str) -> VGroup:
        badge = boxed_statement(word, colour, cfg.FONT["label"])
        badge.move_to([0, -2.9, 0])
        paced_play(scene, FadeIn(badge, scale=1.08), run_time=0.65)
        paced_play(scene, Indicate(badge, color=cfg.WHITE, scale_factor=1.035), run_time=0.65)
        return badge

    # --- 5-28s: a PIN code ----------------------------------------------------
    question = question_caption("1   A four-digit PIN")
    pin = VGroup(*[digit_box(d, size=0.9) for d in "1528"])
    pin.arrange(RIGHT, buff=0.3).move_to([0, 1.55, 0])
    paced_play(scene, LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in pin], lag_ratio=0.18), run_time=1.0)
    countdown()
    shuffled = VGroup(*[digit_box(d, cfg.ORANGE, 0.9) for d in "8251"])
    shuffled.arrange(RIGHT, buff=0.3).move_to([0, -0.25, 0])
    arrow = Arrow([0, 0.95, 0], [0, 0.38, 0], color=cfg.MUTED, stroke_width=6, buff=0.02,
                  max_tip_length_to_length_ratio=0.5)
    paced_play(scene, GrowArrow(arrow), run_time=0.4)
    paced_play(scene, LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in shuffled], lag_ratio=0.16), run_time=0.9)
    different = outlined_text("A DIFFERENT CODE", cfg.FONT["small"], cfg.RED).move_to([0, -1.55, 0])
    paced_play(scene, FadeIn(different, shift=UP * 0.12), run_time=0.55)
    badge = verdict("ORDER MATTERS", cfg.ORANGE)
    cue(scene, started, 17.0)

    # Codes allow reuse: an ordered outcome need not use the nPr formula.
    repeated = VGroup(*[digit_box(d, size=0.9) for d in "1128"]).arrange(RIGHT, buff=0.3)
    repeated.move_to(shuffled.get_center())
    reuse = outlined_text("DIGITS MAY REPEAT", cfg.FONT["small"], cfg.CYAN).move_to(different)
    count = eq(r"10^4 = 10{,}000", cfg.GOLD, 62).move_to(badge)
    paced_play(scene, ReplacementTransform(shuffled, repeated),
               ReplacementTransform(different, reuse), ReplacementTransform(badge, count), run_time=0.9)
    paced_play(scene, Indicate(repeated[0], color=cfg.CYAN),
               Indicate(repeated[1], color=cfg.CYAN), run_time=0.8)
    cue(scene, started, 27.0)
    scene.play(FadeOut(pin, repeated, arrow, reuse, count, question), run_time=0.8)

    # --- 28-48s: pizza toppings -----------------------------------------------
    question = question_caption("2   Three pizza toppings")
    pie = pizza(["mushroom", "olive", "cheese"], 1.55).move_to([0, 0.5, 0])
    paced_play(scene, FadeIn(pie, scale=0.75), run_time=1.0)
    countdown()
    seats = [piece.get_center() for piece in pie.pieces]
    rotated = seats[1:] + seats[:1]
    paced_play(
        scene,
        *[pie.pieces[i].animate.move_to(rotated[i]) for i in range(3)],
        run_time=1.1,
        path_arc=PI * 0.6,
    )
    paced_play(
        scene,
        *[pie.pieces[i].animate.move_to(seats[(i + 2) % 3]) for i in range(3)],
        run_time=1.1,
        path_arc=PI * 0.6,
    )
    same = outlined_text("STILL THE SAME PIZZA", cfg.FONT["small"], cfg.GREEN).move_to([0, -1.55, 0])
    paced_play(scene, FadeIn(same, shift=UP * 0.12), run_time=0.55)
    badge = verdict("COMBINATION", cfg.GREEN)
    scene.play(pie.animate.scale(1.025), run_time=1.6, rate_func=there_and_back)
    cue(scene, started, 47.0)
    scene.play(FadeOut(pie, same, badge, question), run_time=0.8)

    # --- 48-76s: the same people, with and without roles ----------------------
    question = question_caption("3   Same people, two different questions")
    alice = person_icon(cfg.CYAN, 1.15, "ALICE").move_to([-2.5, 0.9, 0])
    bob = person_icon(cfg.PURPLE, 1.15, "BOB").move_to([2.5, 0.9, 0])
    roles = VGroup(
        outlined_text("PRESIDENT", cfg.FONT["tiny"], cfg.GOLD).move_to([-2.5, -0.65, 0]),
        outlined_text("VICE-PRESIDENT", cfg.FONT["tiny"], cfg.MUTED).move_to([2.5, -0.65, 0]),
    )
    paced_play(scene, FadeIn(alice, shift=RIGHT * 0.25), FadeIn(bob, shift=LEFT * 0.25), run_time=0.9)
    paced_play(scene, FadeIn(roles, shift=UP * 0.15), run_time=0.6)
    countdown()
    paced_play(scene, Swap(alice, bob, path_arc=PI * 0.8), run_time=1.2)
    changed = outlined_text("DIFFERENT ROLES", cfg.FONT["small"], cfg.RED).move_to([0, -1.5, 0])
    paced_play(scene, FadeIn(changed, shift=UP * 0.12), run_time=0.55)
    badge = verdict("PERMUTATION", cfg.ORANGE)
    cue(scene, started, 61.0)

    team_question = outlined_text(
        "No roles: Alice and Bob form one team", cfg.FONT["label"], cfg.UNORDERED,
    ).to_edge(UP, buff=0.42)
    ring = team_ring(2.0, cfg.UNORDERED, [0, 0.45, 0])
    scene.play(
        FadeOut(question, roles, changed, badge),
        FadeIn(team_question, shift=UP * 0.1),
        Create(ring),
        alice.animate.scale(0.75).move_to([-0.9, 0.5, 0]),
        bob.animate.scale(0.75).move_to([0.9, 0.5, 0]),
        run_time=1.1,
    )
    question = team_question
    countdown()
    paced_play(scene, Swap(alice, bob, path_arc=PI * 0.75), run_time=1.1)
    same = outlined_text("STILL THE SAME TEAM", cfg.FONT["small"], cfg.GREEN).move_to([0, -1.85, 0])
    paced_play(scene, FadeIn(same, shift=UP * 0.12), run_time=0.55)
    badge = verdict("COMBINATION", cfg.UNORDERED)
    cue(scene, started, 75.0)
    scene.play(FadeOut(ring, alice, bob, same, badge, question), run_time=0.8)

    # --- 76-90s: the rule to remember ----------------------------------------
    rule = boxed_statement("Did the swap change the outcome?", cfg.GOLD, cfg.FONT["small"])
    rule.move_to([0, 2.15, 0])
    paced_play(scene, FadeIn(rule, scale=0.95), run_time=0.9)

    branches = VGroup()
    for word, answer, colour, x in (("YES", "PERMUTATION", cfg.ORANGE, -3.25), ("NO", "COMBINATION", cfg.UNORDERED, 3.25)):
        arrow = Arrow([x * 0.3, 1.4, 0], [x, 0.35, 0], color=colour, stroke_width=6, buff=0.05,
                      max_tip_length_to_length_ratio=0.28)
        tag = outlined_text(word, cfg.FONT["body"], colour).move_to([x, -0.25, 0])
        answer_tag = outlined_text(answer, cfg.FONT["small"], colour).move_to([x, -1.25, 0])
        branches.add(VGroup(arrow, tag, answer_tag))
    paced_play(scene, FadeIn(branches[0], shift=DOWN * 0.15), run_time=0.75)
    paced_play(scene, FadeIn(branches[1], shift=DOWN * 0.15), run_time=0.75)
    repeat_check = outlined_text("Then ask: can an object be used again?", cfg.FONT["tiny"], cfg.CYAN)
    repeat_check.move_to([0, -2.7, 0])
    paced_play(scene, FadeIn(repeat_check, shift=UP * 0.12), run_time=0.7)
    paced_play(
        scene,
        Indicate(branches[0][2], color=cfg.WHITE, scale_factor=1.12),
        Indicate(branches[1][2], color=cfg.WHITE, scale_factor=1.12),
        run_time=1.0,
    )
    cue(scene, started, 88.5)
    paced_play(scene, Indicate(rule, color=cfg.WHITE, scale_factor=1.025), run_time=0.8)

    end_scene(scene, started, cfg.SCENE_DURATIONS["08"])
