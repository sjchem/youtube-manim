"""Scene 07: a combination is a permutation with the order divided away."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    ProductChain, add_cinematic_background, begin_scene, boxed_statement, chip, chip_target,
    cue, end_scene, eq, equals_result, glow_slot, outlined_text, paced_play, slot_row,
    swap_caption, team_ring, top_caption,
)
from utils.counting_models import shrinking_pool
from utils.math_utils import (
    combinations, factorial, list_combinations, list_permutations, permutations,
)

STUDENTS = ("A", "B", "C", "D", "E")
STUDENT_COLORS = {
    "A": cfg.CYAN, "B": cfg.PURPLE, "C": cfg.GREEN, "D": cfg.BLUE, "E": cfg.ORANGE,
}


class Scene07Combinations(Scene):
    """Choosing three students, when nobody gets a title."""

    def construct(self) -> None:
        play_scene(self)


def ordered_card(word: str, size: float = 0.56, colour: str = cfg.ORANGE) -> VGroup:
    """Three ranked boxes: one ordered arrangement, drawn small."""
    boxes = VGroup()
    for letter in word:
        box = RoundedRectangle(
            width=size, height=size, corner_radius=0.08,
            stroke_color=colour, stroke_width=2.6,
            fill_color=cfg.PANEL, fill_opacity=0.7,
        )
        glyph = outlined_text(letter, int(size * 62), STUDENT_COLORS[letter])
        glyph.move_to(box.get_center())
        boxes.add(VGroup(box, glyph))
    boxes.arrange(RIGHT, buff=0.08)
    boxes.word = word
    return boxes


def team_badge(word: str, radius: float = 0.74) -> VGroup:
    """One unordered group: letters sitting inside a single green ring."""
    ring = Circle(radius=radius, color=cfg.UNORDERED, stroke_width=3.6,
                  fill_color=cfg.UNORDERED, fill_opacity=0.08)
    halo = Circle(radius=radius * 1.05, color=cfg.UNORDERED, stroke_width=12,
                  stroke_opacity=0.10, fill_opacity=0)
    letters = VGroup(
        *[outlined_text(letter, 34, STUDENT_COLORS[letter]) for letter in word]
    ).arrange(RIGHT, buff=0.1)
    letters.move_to(ring.get_center())
    group = VGroup(halo, ring, letters)
    group.ring = ring
    return group


def gentle_breathe(scene: Scene, mob: Mobject, run_time: float = 2.0, scale: float = 1.025) -> None:
    """Add calm motion while narration continues over one composition."""
    scene.play(mob.animate.scale(scale), run_time=run_time, rate_func=there_and_back)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "07")
    add_cinematic_background(scene)

    heading = top_caption("A  TEAM  OF  THREE", cfg.UNORDERED)

    # --- 0-18s: five students, three places, no titles ------------------------
    people = VGroup(*[chip(name, STUDENT_COLORS[name], 0.66) for name in STUDENTS])
    people.arrange(RIGHT, buff=0.8).move_to([0, 2.2, 0])
    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), run_time=0.8)
    paced_play(scene, LaggedStart(*[FadeIn(p, scale=0.6) for p in people], lag_ratio=0.2), run_time=1.9)
    caption = swap_caption(scene, None, "Five students. Pick three for the science team.", cfg.UNORDERED)
    scene.play(
        *[person.animate.shift(UP * (0.06 + 0.01 * (index % 2))) for index, person in enumerate(people)],
        run_time=2.1,
        rate_func=there_and_back,
    )
    cue(scene, started, 12.0)

    caption = swap_caption(scene, caption, "First, count it the way we counted podiums.", cfg.ORANGE)
    paced_play(scene, Indicate(people, color=cfg.ORANGE, scale_factor=1.035), run_time=1.5)
    cue(scene, started, 18.0)

    # --- 18-42s: the podium method gives 60 -----------------------------------
    slots = slot_row(3, ranks=["1st", "2nd", "3rd"], size=1.5, buff=0.7, center=[0, -0.15, 0])
    paced_play(scene, LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in slots], lag_ratio=0.2),
               FadeOut(heading, shift=UP * 0.15), run_time=1.3)

    chain = ProductChain(shrinking_pool(5, 3), cfg.ORANGE, 76)
    chain.move_to([-1.5, -2.55, 0])
    picked = (0, 1, 2)
    remaining = list(people)
    for step, index in enumerate(picked):
        glow_slot(scene, slots[step], cfg.ORANGE, run_time=0.4)
        paced_play(
            scene,
            LaggedStart(*[Indicate(p, color=cfg.WHITE, scale_factor=1.12) for p in remaining], lag_ratio=0.14),
            run_time=0.5 + 0.3 * (5 - step),
        )
        target = chip_target(people[index], cfg.ORANGE).scale_to_fit_height(slots[step].body.height * 0.78)
        target.move_to(slots[step].body.get_center())
        paced_play(scene, Transform(people[index], target, path_arc=-0.55), run_time=0.85)
        remaining = [p for p in remaining if p is not people[index]]
        chain.reveal(scene, step, run_time=0.5)
        if remaining:
            # The pool re-centres, so the shrinking is visible rather than implied.
            left = VGroup(*remaining).copy().arrange(RIGHT, buff=0.8).move_to([0, 2.2, 0])
            paced_play(
                scene,
                *[Transform(remaining[i], left[i]) for i in range(len(remaining))],
                run_time=0.6,
            )
    sixty = equals_result(chain, str(permutations(5, 3)), cfg.GOLD, 76)
    paced_play(scene, FadeIn(sixty, shift=RIGHT * 0.25), run_time=0.9)
    caption = swap_caption(scene, caption, "Sixty. But something is wrong.", cfg.RED)
    paced_play(scene, Indicate(VGroup(chain, sixty), color=cfg.GOLD, scale_factor=1.04), run_time=1.5)
    cue(scene, started, 44.0)

    # --- 44-70s: the same three people, six ways ------------------------------
    scene.play(
        FadeOut(VGroup(*remaining), slots),
        VGroup(chain, sixty).animate.scale(0.8).move_to([4.7, 3.1, 0]),
        run_time=1.3,
    )
    trio = VGroup(*[people[index] for index in picked])
    paced_play(scene, trio.animate.arrange(RIGHT, buff=0.7).move_to([0, 2.55, 0]), run_time=1.0)

    words = list_permutations("ABC")
    cards = VGroup(*[ordered_card(word, 0.72) for word in words])
    cards.arrange_in_grid(rows=2, cols=3, buff=(0.95, 0.75))
    # The cards live on the left so the collapsing ring has its own clear space.
    cards.move_to([-3.4, -0.35, 0])
    caption = swap_caption(scene, caption, "Take A, B and C. The count treats these as six.", cfg.ORANGE)
    paced_play(
        scene,
        LaggedStart(*[FadeIn(card, scale=0.7) for card in cards], lag_ratio=0.22),
        run_time=3.2,
    )
    cue(scene, started, 60.0)
    paced_play(
        scene,
        LaggedStart(*[Indicate(card, color=cfg.GOLD, scale_factor=1.12) for card in cards], lag_ratio=0.25),
        run_time=2.6,
    )
    cue(scene, started, 68.0)

    # --- 68-92s: they all collapse into one team ------------------------------
    caption = swap_caption(scene, caption, "But a team has no first place.", cfg.UNORDERED)
    ring = team_ring(1.55, cfg.UNORDERED, [3.55, -0.35, 0])
    paced_play(scene, Create(ring), run_time=1.0)
    for index, card in enumerate(cards):
        paced_play(
            scene,
            card.animate.scale(0.18).move_to(ring.ring.get_center()).set_opacity(0),
            run_time=0.75 if index else 0.95,
            path_arc=PI * 0.4,
        )
        scene.remove(card)
    inside = VGroup(*[outlined_text(letter, 62, STUDENT_COLORS[letter]) for letter in "ABC"])
    inside.arrange(RIGHT, buff=0.34).move_to(ring.ring.get_center())
    paced_play(scene, FadeIn(inside, scale=0.6), Flash(ring.ring.get_center(), color=cfg.UNORDERED, line_length=0.4), run_time=1.0)
    same = eq(r"\{A,B,C\}", cfg.UNORDERED, 78).move_to([3.55, -2.55, 0])
    paced_play(scene, FadeIn(same, shift=UP * 0.2), run_time=0.9)
    gentle_breathe(scene, VGroup(ring, inside), run_time=1.8)
    cue(scene, started, 88.0)

    # --- 88-112s: the size of the overcount ------------------------------------
    caption = swap_caption(scene, caption, "Six orderings. One single team.", cfg.UNORDERED)
    overcount = eq(rf"3! = {factorial(3)}", cfg.GOLD, 86).move_to([-4.5, 0.55, 0])
    over_tag = outlined_text("WAYS TO REORDER\nTHE SAME THREE", cfg.FONT["tiny"], cfg.GOLD)
    over_tag.next_to(overcount, DOWN, buff=0.3)
    paced_play(scene, FadeIn(overcount, shift=RIGHT * 0.25), run_time=1.0)
    paced_play(scene, FadeIn(over_tag), run_time=0.8)
    paced_play(scene, Indicate(overcount, color=cfg.WHITE, scale_factor=1.06), run_time=1.5)
    cue(scene, started, 98.0)

    verdict = boxed_statement("Every real team was counted six times.", cfg.RED, cfg.FONT["label"])
    verdict.move_to([0, -3.1, 0])
    paced_play(scene, FadeOut(same, caption), FadeIn(verdict, scale=0.92), run_time=1.2)
    caption = None
    gentle_breathe(scene, verdict, run_time=1.6, scale=1.018)
    cue(scene, started, 106.0)

    divide = MathTex(
        str(permutations(5, 3)), r"\div", str(factorial(3)), r"=", str(combinations(5, 3)),
        font_size=100,
    )
    divide[0].set_color(cfg.GOLD)
    divide[1].set_color(cfg.MUTED)
    divide[2].set_color(cfg.GOLD)
    divide[3].set_color(cfg.MUTED)
    divide[4].set_color(cfg.UNORDERED)
    divide.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    divide.move_to([-2.15, 0.15, 0])
    divide_tag = outlined_text("DIVIDE OUT THE 6 ORDERS", cfg.FONT["small"], cfg.GOLD)
    divide_tag.next_to(divide, DOWN, buff=0.36)
    scene.play(
        FadeOut(overcount, over_tag, trio, chain, sixty),
        VGroup(ring, inside).animate.scale(0.9).move_to([4.55, 0.35, 0]),
        FadeIn(VGroup(divide[0], divide[1], divide[2]), shift=RIGHT * 0.25),
        run_time=1.5,
    )
    paced_play(
        scene,
        FadeIn(VGroup(divide[3], divide[4]), shift=RIGHT * 0.25),
        FadeIn(divide_tag, shift=UP * 0.15),
        run_time=1.1,
    )
    paced_play(scene, Indicate(divide[4], color=cfg.GOLD, scale_factor=1.14), run_time=1.3)
    cue(scene, started, 116.0)

    # --- 116-142s: the ten teams themselves ------------------------------------
    scene.play(
        FadeOut(ring, inside, verdict, divide, divide_tag),
        run_time=1.4,
    )
    heading = top_caption("THE  TEN  REAL  TEAMS", cfg.UNORDERED)
    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), run_time=0.8)

    teams = VGroup(*[team_badge(word, 0.82) for word in list_combinations(STUDENTS, 3)])
    teams.arrange_in_grid(rows=2, cols=5, buff=(0.75, 0.8))
    teams.move_to([0, 0.35, 0])
    paced_play(
        scene,
        LaggedStart(*[FadeIn(badge, scale=0.6) for badge in teams], lag_ratio=0.18),
        run_time=4.2,
    )
    paced_play(
        scene,
        LaggedStart(*[Indicate(badge, color=cfg.WHITE, scale_factor=1.12) for badge in teams], lag_ratio=0.2),
        run_time=3.0,
    )
    ten = eq(str(combinations(5, 3)), cfg.UNORDERED, 104).move_to([0, -2.75, 0])
    paced_play(scene, FadeIn(ten, scale=1.25),
               FadeOut(heading, shift=UP * 0.15), run_time=1.0)
    cue(scene, started, 137.0)

    # --- 134-160s: the notation -----------------------------------------------
    choose = MathTex(
        r"\binom{5}{3}", r"=", r"\frac{{}_5P_3}{3!}", r"=",
        rf"\frac{{{permutations(5, 3)}}}{{{factorial(3)}}}", r"=", str(combinations(5, 3)),
        font_size=88,
    )
    choose.set_color(cfg.WHITE)
    choose[0].set_color(cfg.UNORDERED)
    choose[2].set_color(cfg.ORANGE)
    choose[6].set_color(cfg.UNORDERED)
    choose.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    choose.move_to([0, -2.6, 0])
    paced_play(scene, teams.animate.scale(0.82).move_to([0, 1.25, 0]), FadeOut(ten), run_time=1.1)
    paced_play(scene, FadeIn(choose[0], scale=1.2), run_time=1.0)
    paced_play(scene, FadeIn(VGroup(choose[1], choose[2]), shift=RIGHT * 0.2), run_time=1.1)
    paced_play(scene, FadeIn(VGroup(choose[3], choose[4]), shift=RIGHT * 0.2), run_time=1.1)
    paced_play(scene, FadeIn(VGroup(choose[5], choose[6]), shift=RIGHT * 0.2), run_time=1.1)
    paced_play(scene, Indicate(choose[6], color=cfg.GOLD, scale_factor=1.12), run_time=1.3)
    cue(scene, started, 148.0)

    # --- 148-172s: substitute, and the general formula --------------------------
    expanded = MathTex(r"\binom{5}{3}", r"=", r"\frac{5!}{3!\,(5-3)!}", font_size=96)
    expanded.set_color(cfg.WHITE)
    expanded[0].set_color(cfg.UNORDERED)
    expanded[2].set_color(cfg.GOLD)
    expanded.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    expanded.move_to([0, -2.35, 0])
    scene.play(ReplacementTransform(choose, expanded), run_time=1.5)
    paced_play(scene, Indicate(expanded[2], color=cfg.GOLD, scale_factor=1.035), run_time=1.5)
    cue(scene, started, 156.0)

    general = boxed_statement(r"\binom{n}{r} = \frac{n!}{r!\,(n-r)!}", cfg.UNORDERED, 88, tex=True)
    general.move_to([0, 0.35, 0])
    scene.play(
        FadeOut(teams),
        ReplacementTransform(expanded, general),
        run_time=1.6,
    )
    gentle_breathe(scene, general, run_time=1.7, scale=1.018)
    cue(scene, started, 166.0)

    # --- 166-194s: the sentence worth remembering -------------------------------
    key = VGroup(
        outlined_text("A combination is a permutation", cfg.FONT["body"], cfg.WHITE),
        outlined_text("with the unnecessary order divided away.", cfg.FONT["body"], cfg.UNORDERED),
    ).arrange(DOWN, buff=0.22).move_to([0, -2.4, 0])
    paced_play(scene, FadeIn(key[0], shift=UP * 0.2), run_time=1.1)
    paced_play(scene, FadeIn(key[1], shift=UP * 0.2), run_time=1.1)
    paced_play(scene, Indicate(key[1], color=cfg.GOLD, scale_factor=1.025), run_time=1.6)
    cue(scene, started, 178.0)

    split = VGroup(
        eq(r"\text{permutations}", cfg.ORANGE, 58),
        eq(r"\div", cfg.MUTED, 58),
        eq("r!", cfg.GOLD, 58),
        eq("=", cfg.MUTED, 58),
        eq(r"\text{combinations}", cfg.UNORDERED, 58),
    ).arrange(RIGHT, buff=0.3).move_to([0, 2.55, 0])
    paced_play(scene, FadeIn(split, shift=DOWN * 0.2), run_time=1.3)
    cue(scene, started, 190.5)
    paced_play(scene, Indicate(general, color=cfg.WHITE, scale_factor=1.04), run_time=1.3)
    paced_play(scene, Indicate(split[2], color=cfg.WHITE, scale_factor=1.15), run_time=1.1)

    end_scene(scene, started, cfg.SCENE_DURATIONS["07"])
