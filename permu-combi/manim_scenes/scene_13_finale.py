"""Scene 13: one question, two answers — the whole film in one frame."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background, begin_scene, boxed_statement, chip, cue, end_scene, eq,
    glow_line, lock_icon, outlined_text, paced_play, ring_points, slot_row, swap_caption, team_ring,
)


class Scene13Finale(Scene):
    """Factorial, permutation, combination — three answers to one question."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "13")
    add_cinematic_background(scene)

    # --- 0-26s: the same slots, three times ------------------------------------
    columns = []
    specs = (
        ("FACTORIAL", cfg.GOLD, r"n!", "fill every position", 4, 4),
        ("PERMUTATION", cfg.ORANGE, r"\frac{n!}{(n-r)!}", "fill r positions", 4, 2),
        ("COMBINATION", cfg.UNORDERED, r"\frac{n!}{r!\,(n-r)!}", "choose only", 4, 2),
    )
    xs = (-4.9, 0.0, 4.9)
    for (name, colour, formula, note, total, filled), x in zip(specs, xs):
        title = outlined_text(name, cfg.FONT["small"], colour).move_to([x, 3.35, 0])
        if name == "COMBINATION":
            holder = team_ring(1.06, colour, [x, 1.75, 0])
            seats = ring_points(holder, filled, 0.56)
            pieces = VGroup(*[chip("", colour, 0.28) for _ in range(filled)])
            for piece, seat in zip(pieces, seats):
                piece.move_to(seat)
            body = VGroup(holder, pieces)
        else:
            holder = slot_row(
                total,
                ranks=[str(index + 1) for index in range(total)],
                size=0.72,
                buff=0.16,
                color=colour,
                center=[x, 1.85, 0],
            )
            pieces = VGroup()
            for index in range(filled):
                piece = chip("", colour, 0.26).move_to(holder[index].body.get_center())
                pieces.add(piece)
            body = VGroup(holder, pieces)
        # The column title supplies the name; keep the count itself large.
        tex = eq(formula, colour, 82).move_to([x, -0.75, 0])
        if tex.width > 4.4:
            tex.scale_to_fit_width(4.4)
        caption = outlined_text(note, cfg.FONT["tiny"], cfg.MUTED).move_to([x, -2.6, 0])
        columns.append(VGroup(title, body, tex, caption))

    for index, column in enumerate(columns):
        cue(scene, started, 7.0 * index)
        paced_play(scene, FadeIn(column[0], shift=DOWN * 0.15), run_time=0.6)
        paced_play(scene, FadeIn(column[1], scale=0.85), run_time=0.9)
        paced_play(scene, FadeIn(column[2], shift=UP * 0.15), FadeIn(column[3]), run_time=0.9)
    cue(scene, started, 22.0)

    dividers = VGroup(
        glow_line([-2.45, -2.5, 0], [-2.45, 3.0, 0], cfg.MUTED, 1.6),
        glow_line([2.45, -2.5, 0], [2.45, 3.0, 0], cfg.MUTED, 1.6),
    )
    paced_play(scene, LaggedStart(*[Create(line) for line in dividers], lag_ratio=0.3), run_time=1.2)
    caption = swap_caption(scene, None, "Same slots. Different question.", cfg.CYAN)
    cue(scene, started, 28.0)

    # --- 28-52s: compress it into the one decision -----------------------------
    question = boxed_statement("DOES  ORDER  MATTER?", cfg.GOLD, cfg.FONT["body"])
    question.move_to([0, 2.5, 0])
    scene.play(
        FadeOut(*columns, dividers, caption),
        FadeIn(question, scale=0.9),
        run_time=1.6,
    )

    branches = VGroup()
    for word, answer, colour, x in (
        ("YES", "PERMUTATION", cfg.ORANGE, -3.7),
        ("NO", "COMBINATION", cfg.UNORDERED, 3.7),
    ):
        arrow = Arrow([x * 0.32, 1.55, 0], [x, 0.35, 0], color=colour, stroke_width=8, buff=0.05,
                      max_tip_length_to_length_ratio=0.26)
        tag = outlined_text(word, cfg.FONT["section"], colour).move_to([x, -0.35, 0])
        answer_tag = outlined_text(answer, cfg.FONT["label"], colour).move_to([x, -1.55, 0])
        branches.add(VGroup(arrow, tag, answer_tag))
    paced_play(scene, FadeIn(branches[0], shift=DOWN * 0.2), run_time=1.1)
    paced_play(scene, FadeIn(branches[1], shift=DOWN * 0.2), run_time=1.1)
    cue(scene, started, 38.0)

    # --- 38-58s: the closing thought --------------------------------------------
    closing = VGroup(
        outlined_text("These formulas: distinct objects, no repeats.", cfg.FONT["small"], cfg.WHITE),
        outlined_text("Always check what counts as a new outcome.", cfg.FONT["small"], cfg.GOLD),
    ).arrange(DOWN, buff=0.22).move_to([0, -3.1, 0])
    paced_play(scene, FadeIn(closing[0], shift=UP * 0.2), run_time=1.1)
    paced_play(scene, FadeIn(closing[1], shift=UP * 0.2), run_time=1.1)
    cue(scene, started, 46.0)

    # Return to the opening question with the same swap in two different worlds.
    lock = lock_icon(cfg.ORANGE, 0.8).move_to([-3.7, 1.1, 0])
    digits = VGroup(*[outlined_text(d, 64, cfg.GOLD) for d in "123"])
    digits.arrange(RIGHT, buff=0.55).move_to([-3.7, -0.6, 0])
    lock_tag = outlined_text("NEW CODE", cfg.FONT["label"], cfg.ORANGE).move_to([-3.7, -2.0, 0])
    ring = team_ring(1.35, cfg.UNORDERED, [3.7, 0.8, 0])
    people = VGroup(*[chip(letter, cfg.UNORDERED, 0.38) for letter in "ABC"])
    for person, seat in zip(people, ring_points(ring, 3, 0.55)):
        person.move_to(seat)
    team_tag = outlined_text("SAME TEAM", cfg.FONT["label"], cfg.UNORDERED).move_to([3.7, -2.0, 0])
    callback = VGroup(lock, digits, lock_tag, ring, people, team_tag)
    scene.play(FadeOut(question, branches, closing), FadeIn(callback), run_time=1.2)
    cue(scene, started, 49.0)
    paced_play(scene, Swap(digits[0], digits[2], path_arc=PI / 2),
               Swap(people[0], people[2], path_arc=PI / 2), run_time=1.5)
    cue(scene, started, 55.0)

    final = VGroup(
        outlined_text("When I rearrange the same objects,", cfg.FONT["label"], cfg.WHITE),
        outlined_text("have I created something new?", cfg.FONT["body"], cfg.CYAN),
    ).arrange(DOWN, buff=0.3).move_to([0, 0.3, 0])
    scene.play(
        FadeOut(callback),
        FadeIn(final, scale=0.94),
        run_time=1.6,
    )
    cue(scene, started, 57.0)

    rule = glow_line([-5.2, -1.5, 0], [5.2, -1.5, 0], cfg.CYAN, 3)
    paced_play(scene, Create(rule), run_time=1.0)
    verdicts = VGroup(
        outlined_text("YES  →  PERMUTATION", cfg.FONT["label"], cfg.ORANGE),
        outlined_text("NO  →  COMBINATION", cfg.FONT["label"], cfg.UNORDERED),
    ).arrange(DOWN, buff=0.35).move_to([0, -2.55, 0])
    paced_play(scene, FadeIn(verdicts[0], shift=RIGHT * 0.25), run_time=0.9)
    paced_play(scene, FadeIn(verdicts[1], shift=LEFT * 0.25), run_time=0.9)
    cue(scene, started, 69.5)
    paced_play(scene, Indicate(final[1], color=cfg.WHITE, scale_factor=1.05), run_time=1.3)

    end_scene(scene, started, cfg.SCENE_DURATIONS["13"])
