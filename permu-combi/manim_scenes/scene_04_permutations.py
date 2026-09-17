"""Scene 04: five runners, three medals, and the formula that falls out of it.

The podium is real 3D, but every word on screen is fixed in the frame. A theta
rotation would spin flat text in-plane, so this chapter keeps theta at -90 deg
and lifts the camera with phi alone.
"""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    ProductChain, begin_scene, bottom_caption, boxed_statement, clear_background, cue,
    end_scene, eq, equals_result, medal_icon, outlined_text, paced_play, person_icon,
)
from manim_scenes.props_3d import podium, podium_order
from utils.counting_models import shrinking_pool
from utils.math_utils import factorial, permutations

RUNNERS = ("A", "B", "C", "D", "E")
RUNNER_COLORS = (cfg.CYAN, cfg.BLUE, cfg.GREEN, cfg.PURPLE, cfg.ORANGE)
PODIUM_TILT = 18 * DEGREES


class Scene04Permutations(ThreeDScene):
    """Filling only some of the positions: nPr."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: ThreeDScene) -> None:
    started = begin_scene(scene, "04")
    clear_background(scene)
    scene.set_camera_orientation(phi=0, theta=-PI / 2, zoom=1, frame_center=ORIGIN)

    overlays: list[Mobject] = []

    def pin(mob: Mobject) -> Mobject:
        """Register a flat mobject as HUD, so the camera tilt never distorts it."""
        scene.add_fixed_in_frame_mobjects(mob)
        scene.remove(mob)
        overlays.append(mob)
        return mob

    def say(text: str, colour: str = cfg.GOLD) -> Text:
        return pin(bottom_caption(text, colour))

    heading = pin(outlined_text("FIVE  RUNNERS.  THREE  MEDALS.", cfg.FONT["body"], cfg.CYAN).move_to([0, 3.45, 0]))

    # --- 0-14s: the field ----------------------------------------------------
    runners = VGroup(
        *[person_icon(colour, 1.15, name) for colour, name in zip(RUNNER_COLORS, RUNNERS)]
    )
    runners.arrange(RIGHT, buff=0.95).move_to([0, 1.55, 0])
    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), run_time=0.8)
    paced_play(scene, LaggedStart(*[FadeIn(r, shift=UP * 0.3) for r in runners], lag_ratio=0.2), run_time=2.0)
    caption = say("Everybody runs. Only three finish on the podium.")
    paced_play(scene, FadeIn(caption, shift=UP * 0.15), run_time=0.8)
    cue(scene, started, 14.0)

    # --- 14-26s: the podium, in three dimensions ------------------------------
    stand = podium(1.15).move_to([0, -0.95, 0])
    paced_play(
        scene,
        runners.animate.scale(0.8).move_to([-0.6, 2.8, 0]),
        FadeOut(heading, shift=UP * 0.15),
        FadeOut(caption),
        run_time=1.1,
    )
    scene.play(FadeIn(stand, shift=UP * 0.8), run_time=1.6)
    scene.move_camera(phi=PODIUM_TILT, run_time=2.6)
    gold_index, silver_index, bronze_index = podium_order()
    seats = stand.tops
    caption = say("Three positions. Not three people — three positions.", cfg.ORANGE)
    paced_play(scene, FadeIn(caption, shift=UP * 0.15), run_time=0.8)
    cue(scene, started, 26.0)

    # --- 26-78s: fill gold, then silver, then bronze --------------------------
    chain = ProductChain(shrinking_pool(5, 3), cfg.GOLD, 78)
    chain.move_to([-4.4, -2.95, 0])
    pin(chain)
    counter = eq("5", cfg.CYAN, 96).move_to([-6.4, 2.8, 0])
    pin(counter)
    paced_play(scene, FadeIn(counter, scale=1.25), run_time=0.8)

    medals = (
        ("1", cfg.GOLD, gold_index, "GOLD"),
        ("2", cfg.MUTED, silver_index, "SILVER"),
        ("3", cfg.ORANGE, bronze_index, "BRONZE"),
    )
    winner_order = (2, 0, 4)  # C takes gold, A silver, E bronze
    remaining = list(runners)
    awarded = VGroup()

    for step, ((rank, colour, block_index, name), runner_index) in enumerate(zip(medals, winner_order)):
        cue(scene, started, 27.0 + 15.0 * step)
        choices = 5 - step
        tag = pin(outlined_text(name, cfg.FONT["body"], colour).move_to([4.9, 2.8, 0]))
        paced_play(
            scene,
            FadeIn(tag, shift=DOWN * 0.15),
            Indicate(stand.blocks[block_index], color=colour, scale_factor=1.03),
            run_time=0.9,
        )
        paced_play(
            scene,
            LaggedStart(
                *[Indicate(r, color=cfg.WHITE, scale_factor=1.15) for r in remaining],
                lag_ratio=0.15,
            ),
            run_time=0.6 + 0.34 * choices,
        )
        winner = runners[runner_index]
        seat = seats[block_index]
        paced_play(
            scene,
            winner.animate.scale(0.94).next_to(seat, UP, buff=0.02),
            run_time=1.1,
            path_arc=-0.5,
        )
        medal = medal_icon(rank, colour, 0.8)
        medal.move_to(winner.get_center() + LEFT * 0.62 + UP * 0.1)
        paced_play(scene, FadeIn(medal, scale=0.5), run_time=0.7)
        chain.reveal(scene, step, run_time=0.6)
        remaining = [r for r in remaining if r is not winner]
        fresh = eq(str(choices - 1), cfg.CYAN, 96).move_to(counter.get_center())
        pin(fresh)
        left = VGroup(*remaining).copy().arrange(RIGHT, buff=0.78).move_to([-0.6, 2.8, 0])
        paced_play(
            scene,
            *[Transform(remaining[i], left[i]) for i in range(len(remaining))],
            Transform(counter, fresh),
            FadeOut(tag),
            run_time=0.9,
        )
        awarded.add(medal)

    total = equals_result(chain, str(permutations(5, 3)), cfg.WHITE, 78)
    pin(total)
    paced_play(scene, FadeIn(total, shift=RIGHT * 0.3), run_time=0.9)
    paced_play(scene, Indicate(total[1], color=cfg.GOLD, scale_factor=1.15), run_time=1.0)
    fresh_caption = say("Sixty different podiums.")
    paced_play(scene, FadeOut(caption), FadeIn(fresh_caption, shift=UP * 0.12), run_time=0.7)
    caption = fresh_caption
    # A slow lift, so the finished podium is felt as a solid object.
    scene.move_camera(phi=6 * DEGREES, run_time=2.4)
    scene.move_camera(phi=PODIUM_TILT, run_time=2.1)
    cue(scene, started, 78.0)

    # --- 78-96s: back to flat, and back to 5! ---------------------------------
    scene.move_camera(phi=0, run_time=2.0)
    product = VGroup(chain, total)
    scene.play(
        FadeOut(stand, runners, awarded, counter, caption),
        product.animate.move_to([0, 2.55, 0]),
        run_time=1.5,
    )
    scene.remove_fixed_in_frame_mobjects(*overlays)
    scene.add(product)

    full = VGroup(
        eq("5", cfg.GOLD, 78), eq(r"\times", cfg.MUTED, 66), eq("4", cfg.GOLD, 78),
        eq(r"\times", cfg.MUTED, 66), eq("3", cfg.GOLD, 78), eq(r"\times", cfg.MUTED, 66),
        eq("2", cfg.GRAY, 78), eq(r"\times", cfg.GRAY, 66), eq("1", cfg.GRAY, 78),
    ).arrange(RIGHT, buff=0.26)
    factorial_tag = eq("5!", cfg.GOLD, 86)
    equals = eq("=", cfg.MUTED, 66)
    block = VGroup(factorial_tag, equals, full).arrange(RIGHT, buff=0.26).move_to([0, 0.8, 0])
    paced_play(scene, FadeIn(block, shift=UP * 0.2), run_time=1.2)
    cue(scene, started, 90.0)

    tail = VGroup(*full[5:])
    dead = outlined_text("4th and 5th place don't matter", cfg.FONT["small"], cfg.GRAY)
    dead.next_to(tail, DOWN, buff=0.5)
    paced_play(
        scene,
        tail.animate.set_opacity(0.3),
        FadeIn(dead, shift=UP * 0.15),
        run_time=1.2,
    )
    cue(scene, started, 98.0)

    # --- 98-120s: divide the unwanted tail away -------------------------------
    quotient = MathTex(r"5\times4\times3", r"=", r"\frac{5!}{2!}", font_size=92, color=cfg.WHITE)
    quotient.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    quotient[0].set_color(cfg.GOLD)
    quotient[2].set_color(cfg.GOLD)
    quotient.move_to([0, -1.4, 0])
    paced_play(scene, FadeIn(quotient, shift=UP * 0.2), run_time=1.2)
    cue(scene, started, 106.0)

    why = eq(r"2 = 5 - 3", cfg.CYAN, 74).move_to([0, -2.9, 0])
    paced_play(scene, FadeIn(why, shift=UP * 0.15), run_time=0.9)
    paced_play(scene, Indicate(why, color=cfg.GOLD, scale_factor=1.08), run_time=1.0)
    cue(scene, started, 116.0)

    # --- 116-140s: the notation ----------------------------------------------
    notation = MathTex(r"{}_5P_3", r"=", r"\frac{5!}{(5-3)!}", r"=", str(permutations(5, 3)), font_size=104)
    notation.set_color(cfg.WHITE)
    notation[0].set_color(cfg.ORANGE)
    notation[4].set_color(cfg.GOLD)
    notation.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    notation.move_to([0, 0.15, 0])
    scene.play(
        FadeOut(block, dead, product, why),
        ReplacementTransform(quotient, notation),
        run_time=1.6,
    )
    cue(scene, started, 124.0)

    general = boxed_statement(r"{}_nP_r = \frac{n!}{(n-r)!}", cfg.ORANGE, 92, tex=True)
    general.move_to([0, 0.75, 0])
    scene.play(ReplacementTransform(notation, general), run_time=1.4)
    cue(scene, started, 130.0)

    # --- 130-159s: what the two letters actually mean -------------------------
    meanings = VGroup(
        VGroup(
            eq("n", cfg.CYAN, 88),
            outlined_text("objects available", cfg.FONT["label"], cfg.CYAN),
        ).arrange(RIGHT, buff=0.45),
        VGroup(
            eq("r", cfg.ORANGE, 88),
            outlined_text("positions to fill", cfg.FONT["label"], cfg.ORANGE),
        ).arrange(RIGHT, buff=0.45),
    ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
    meanings.move_to([0, -2.1, 0])
    paced_play(scene, FadeIn(meanings[0], shift=RIGHT * 0.25), run_time=1.0)
    paced_play(scene, FadeIn(meanings[1], shift=RIGHT * 0.25), run_time=1.0)
    cue(scene, started, 140.0)

    check = eq(
        rf"{{}}_5P_3 = \frac{{{factorial(5)}}}{{{factorial(2)}}} = {permutations(5, 3)}",
        cfg.GREEN,
        76,
    )
    check.move_to([0, -2.1, 0])
    scene.play(FadeOut(meanings), FadeIn(check, shift=UP * 0.2), run_time=1.2)
    closing = bottom_caption("Choose, and then arrange. Both at once.", cfg.ORANGE)
    paced_play(scene, FadeIn(closing, shift=UP * 0.15), run_time=0.8)
    cue(scene, started, 156.0)
    paced_play(scene, Indicate(general, color=cfg.WHITE, scale_factor=1.04), run_time=1.3)

    end_scene(scene, started, cfg.SCENE_DURATIONS["04"])
    scene.set_camera_orientation(phi=0, theta=-PI / 2, zoom=1, frame_center=ORIGIN)
