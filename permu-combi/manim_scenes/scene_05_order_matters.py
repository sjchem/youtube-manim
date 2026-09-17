"""Scene 05: the same three people, and six genuinely different results."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background, begin_scene, boxed_statement, chip, cue, end_scene, eq,
    outlined_text, paced_play, slot_row, swap_caption, top_caption,
)
from utils.math_utils import list_permutations

PEOPLE = ("A", "B", "C")
PERSON_COLORS = {"A": cfg.CYAN, "B": cfg.PURPLE, "C": cfg.GREEN}
RANKS = ("GOLD", "SILVER", "BRONZE")
RANK_COLORS = (cfg.GOLD, cfg.MUTED, cfg.ORANGE)


class Scene05OrderMatters(Scene):
    """A permutation cares where each object lands."""

    def construct(self) -> None:
        play_scene(self)


def colored_word(word: str, font_size: int) -> VGroup:
    """Keep each person's letter bright and consistent across arrangements."""
    return VGroup(
        *[eq(letter, PERSON_COLORS[letter], font_size) for letter in word]
    ).arrange(RIGHT, buff=0.06)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "05")
    add_cinematic_background(scene)

    heading = top_caption("SAME  PEOPLE.  DIFFERENT  RESULT.", cfg.ORANGE)

    # --- 0-12s: one podium, written as three ranked positions ------------------
    slots = slot_row(3, ranks=list(RANKS), size=2.0, buff=1.0, center=[0, 0.95, 0])
    for index, colour in enumerate(RANK_COLORS):
        slots[index].body.set_stroke(colour, width=5)
        slots[index].tag.set_color(colour)
    chips = VGroup(*[chip(name, PERSON_COLORS[name], 0.76) for name in PEOPLE])
    for index, item in enumerate(chips):
        item.move_to(slots[index].body.get_center())

    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), run_time=0.8)
    paced_play(scene, LaggedStart(*[FadeIn(s, shift=UP * 0.25) for s in slots], lag_ratio=0.22), run_time=1.6)
    paced_play(scene, LaggedStart(*[FadeIn(c, scale=0.6) for c in chips], lag_ratio=0.22), run_time=1.5)
    label = colored_word("ABC", 96).move_to([0, -2.1, 0])
    paced_play(scene, FadeIn(label, shift=UP * 0.2), run_time=0.9)
    caption = swap_caption(scene, None, "One podium. Read it left to right.", cfg.CYAN)
    cue(scene, started, 12.0)

    # --- 12-28s: swap the first two ------------------------------------------
    caption = swap_caption(scene, caption, "Now swap just the first two.", cfg.GOLD)
    arc = CurvedArrow(
        slots[0].body.get_top() + UP * 0.22,
        slots[1].body.get_top() + UP * 0.22,
        angle=-PI * 0.75,
        color=cfg.GOLD,
        stroke_width=6,
        tip_length=0.28,
    )
    paced_play(scene, Create(arc), FadeOut(heading, shift=UP * 0.15), run_time=0.9)
    paced_play(scene, Swap(chips[0], chips[1], path_arc=PI * 0.85), run_time=1.4)
    swapped_label = colored_word("BAC", 96).move_to([0, -2.1, 0])
    paced_play(scene, ReplacementTransform(label, swapped_label), FadeOut(arc), run_time=1.0)
    label = swapped_label
    cue(scene, started, 24.0)

    # --- 24-42s: what actually changed ---------------------------------------
    caption = swap_caption(scene, caption, "Same three people. Is it the same result?", cfg.CYAN)
    moves = VGroup(
        VGroup(
            eq("A", cfg.CYAN, 68),
            outlined_text("gold  →  silver", cfg.FONT["label"], cfg.MUTED),
        ).arrange(RIGHT, buff=0.4),
        VGroup(
            eq("B", cfg.PURPLE, 68),
            outlined_text("silver  →  gold", cfg.FONT["label"], cfg.GOLD),
        ).arrange(RIGHT, buff=0.4),
    ).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
    moves.move_to([0, -2.6, 0])
    paced_play(scene, label.animate.move_to([5.4, 0.95, 0]), run_time=0.8)
    paced_play(scene, FadeIn(moves[0], shift=RIGHT * 0.25), Indicate(chips[0], color=cfg.WHITE), run_time=1.2)
    paced_play(scene, FadeIn(moves[1], shift=RIGHT * 0.25), Indicate(chips[1], color=cfg.WHITE), run_time=1.2)
    cue(scene, started, 36.0)

    verdict = VGroup(
        colored_word("ABC", 82),
        eq(r"\neq", cfg.ORANGE, 82),
        colored_word("BAC", 82),
    ).arrange(RIGHT, buff=0.34).move_to([0, -1.75, 0])
    scene.play(FadeOut(moves, label), FadeIn(verdict, scale=1.15), run_time=1.2)
    paced_play(scene, Indicate(verdict, color=cfg.WHITE, scale_factor=1.06), run_time=1.1)
    cue(scene, started, 44.0)

    # --- 44-70s: every one of the six is a different medal ceremony ------------
    caption = swap_caption(scene, caption, "Three people fill three places in six ways.", cfg.ORANGE)
    counter = outlined_text("1 / 6", cfg.FONT["body"], cfg.GOLD).move_to([5.5, 0.95, 0])
    scene.play(FadeOut(verdict), FadeIn(counter), run_time=0.9)

    orderings = list_permutations(PEOPLE)
    current = {name: chips[PEOPLE.index(name)] for name in PEOPLE}
    shown = VGroup()
    for index, word in enumerate(orderings):
        targets = {name: slots[position].body.get_center() for position, name in enumerate(word)}
        fresh_counter = outlined_text(f"{index + 1} / 6", cfg.FONT["body"], cfg.GOLD).move_to(counter.get_center())
        card = colored_word(word, 54)
        card.move_to([-5.5 + 2.2 * index, -2.65, 0])
        shown.add(card)
        paced_play(
            scene,
            *[current[name].animate.move_to(targets[name]) for name in PEOPLE],
            Transform(counter, fresh_counter),
            FadeIn(card, scale=0.7),
            run_time=1.35 if index else 1.0,
            path_arc=PI * 0.35,
        )
    paced_play(
        scene,
        LaggedStart(*[Indicate(card, color=cfg.GOLD, scale_factor=1.2) for card in shown], lag_ratio=0.28),
        run_time=2.6,
    )
    all_six = eq("6", cfg.GOLD, 110).move_to([5.4, -1.0, 0])
    six_tag = outlined_text("PODIUMS", cfg.FONT["tiny"], cfg.GOLD).next_to(all_six, DOWN, buff=0.22)
    paced_play(scene, FadeIn(all_six, scale=1.25), FadeIn(six_tag), run_time=1.0)
    cue(scene, started, 69.0)

    # --- 66-87s: the principle ------------------------------------------------
    principle = boxed_statement(
        "A permutation asks who was chosen — and where each one landed.",
        cfg.ORANGE,
        cfg.FONT["label"],
    )
    principle.move_to([0, 0.35, 0])
    scene.play(
        FadeOut(slots, chips, shown, counter, all_six, six_tag, caption),
        FadeIn(principle, scale=0.92),
        run_time=1.6,
    )
    cue(scene, started, 76.0)

    contrast = VGroup(
        eq(r"\text{who}", cfg.CYAN, 62),
        eq("+", cfg.MUTED, 56),
        eq(r"\text{where}", cfg.ORANGE, 62),
        eq("=", cfg.MUTED, 56),
        eq(r"\text{permutation}", cfg.GOLD, 62),
    ).arrange(RIGHT, buff=0.32).move_to([0, -2.1, 0])
    paced_play(scene, FadeIn(contrast, shift=UP * 0.2), run_time=1.2)
    cue(scene, started, 85.0)
    paced_play(scene, Indicate(contrast[2], color=cfg.WHITE, scale_factor=1.12), run_time=1.2)

    end_scene(scene, started, cfg.SCENE_DURATIONS["05"])
