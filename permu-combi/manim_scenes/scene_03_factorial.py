"""Scene 03: a factorial is just choices running out, one position at a time."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    ProductChain, add_cinematic_background, begin_scene, book_icon, boxed_statement, cue,
    end_scene, eq, equals_result, glow_slot, outlined_text, paced_play, slot_row,
    swap_caption, top_caption,
)
from utils.counting_models import shrinking_pool
from utils.math_utils import factorial

BOOK_COLORS = (cfg.RED, cfg.BLUE, cfg.GREEN, cfg.PURPLE)
BOOK_NAMES = ("A", "B", "C", "D")


class Scene03Factorial(Scene):
    """Four books, four shelf positions, and a pool that keeps shrinking."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "03")
    add_cinematic_background(scene)

    heading = top_caption("ARRANGE  ALL  FOUR", cfg.CYAN)

    # --- 0-10s: four books ---------------------------------------------------
    books = VGroup(
        *[book_icon(colour, 1.25, name) for colour, name in zip(BOOK_COLORS, BOOK_NAMES)]
    )
    books.arrange(RIGHT, buff=0.9).move_to([0, 1.85, 0])
    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), run_time=0.8)
    paced_play(scene, LaggedStart(*[FadeIn(b, shift=DOWN * 0.4) for b in books], lag_ratio=0.22), run_time=1.9)
    caption = swap_caption(scene, None, "How many different orders can they sit in?", cfg.GOLD)
    cue(scene, started, 10.0)

    # --- 10-18s: four positions on the shelf ---------------------------------
    slots = slot_row(4, ranks=["1st", "2nd", "3rd", "4th"], size=1.42, buff=0.55, center=[0, -0.75, 0])
    paced_play(scene, LaggedStart(*[FadeIn(s, shift=UP * 0.25) for s in slots], lag_ratio=0.2), run_time=1.6)
    caption = swap_caption(scene, caption, "Fill the positions one at a time.", cfg.CYAN)
    cue(scene, started, 16.0)
    # The bottom band now belongs to the product, so the caption steps aside.
    paced_play(scene, FadeOut(heading, shift=UP * 0.15), FadeOut(caption, shift=DOWN * 0.2), run_time=0.7)
    caption = None
    cue(scene, started, 18.0)

    # --- 18-70s: the pool shrinks by one at every step ------------------------
    # The factors come from the model, so the animation and the arithmetic
    # can never drift apart.
    chain = ProductChain(shrinking_pool(4, 4), cfg.GOLD, 72)
    chain.move_to([-1.35, -2.65, 0])

    counter = eq("4", cfg.CYAN, 110).move_to([-5.9, 1.85, 0])
    counter_tag = outlined_text("CHOICES", cfg.FONT["tiny"], cfg.CYAN).next_to(counter, DOWN, buff=0.22)
    paced_play(scene, FadeIn(counter, scale=1.3), FadeIn(counter_tag), run_time=1.0)

    remaining = list(books)
    order = (1, 3, 0, 2)  # B, D, A, C — a genuine arrangement, not the obvious one
    for step, book_index in enumerate(order):
        # Leave room to explain each shrinking pool before the next pick.
        cue(scene, started, 19.0 + 12.0 * step)
        choices = 4 - step
        glow_slot(scene, slots[step], cfg.CHOSEN, run_time=0.45)
        paced_play(
            scene,
            LaggedStart(
                *[Indicate(b, color=cfg.WHITE, scale_factor=1.12) for b in remaining],
                lag_ratio=0.16,
            ),
            run_time=0.5 + 0.32 * choices,
        )
        chosen = books[book_index]
        landing = chosen.copy().scale_to_fit_height(slots[step].body.height * 0.82)
        landing.move_to(slots[step].body.get_center())
        paced_play(scene, Transform(chosen, landing, path_arc=-0.6), run_time=0.9)
        remaining = [b for b in remaining if b is not chosen]
        chain.reveal(scene, step, run_time=0.55)
        if remaining:
            fresh = eq(str(choices - 1), cfg.CYAN, 110).move_to(counter.get_center())
            left = VGroup(*remaining).copy()
            left.arrange(RIGHT, buff=0.9).move_to([0, 1.85, 0])
            paced_play(
                scene,
                *[Transform(remaining[i], left[i]) for i in range(len(remaining))],
                Transform(counter, fresh),
                run_time=0.85,
            )
        else:
            gone = eq("0", cfg.MUTED, 110).move_to(counter.get_center())
            paced_play(scene, Transform(counter, gone), run_time=0.7)
    caption = swap_caption(scene, caption, "ONE CHOICE USED PER POSITION", cfg.CYAN)
    cue(scene, started, 66.0)

    # --- 66-86s: the product the animation just built -------------------------
    paced_play(scene, FadeOut(counter, counter_tag), chain.animate.move_to([-1.35, -2.65, 0]), run_time=0.8)
    result = equals_result(chain, str(factorial(4)), cfg.WHITE, 72)
    paced_play(scene, FadeIn(result, shift=RIGHT * 0.25), run_time=0.9)
    paced_play(scene, Indicate(result[1], color=cfg.GOLD, scale_factor=1.18), run_time=1.0)
    caption = swap_caption(scene, caption, "Twenty-four different shelves.", cfg.GOLD)
    cue(scene, started, 80.0)

    # --- 80-98s: the notation ------------------------------------------------
    product_block = VGroup(chain, result)
    factorial_form = MathTex(r"4!", "=", str(factorial(4)), font_size=104)
    factorial_form.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    factorial_form[0].set_color(cfg.CYAN)
    factorial_form[1].set_color(cfg.MUTED)
    factorial_form[2].set_color(cfg.GOLD)
    factorial_form.move_to([0, -3.15, 0])
    scene.play(
        FadeOut(books, slots, caption),
        ReplacementTransform(product_block, factorial_form),
        run_time=1.5,
    )
    paced_play(scene, factorial_form.animate.move_to([0, 0.9, 0]).scale(1.15), run_time=1.1)
    name_tag = outlined_text("“FOUR FACTORIAL”", cfg.FONT["label"], cfg.GOLD)
    name_tag.next_to(factorial_form, DOWN, buff=0.55)
    paced_play(scene, FadeIn(name_tag, shift=UP * 0.2), run_time=0.9)
    cue(scene, started, 92.0)

    # --- 92-114s: the general shape ------------------------------------------
    general = MathTex(r"n!", "=", r"n\,(n-1)\,(n-2)\cdots 2\cdot 1", font_size=68)
    general.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    general[0].set_color(cfg.GOLD)
    general[1].set_color(cfg.MUTED)
    general[2].set_color(cfg.WHITE)
    general.move_to([0, 0.75, 0])
    scene.play(
        FadeOut(name_tag),
        ReplacementTransform(factorial_form, general),
        run_time=1.3,
    )
    meaning = boxed_statement(
        "A factorial is what happens when every step costs one choice.",
        cfg.CYAN,
        cfg.FONT["label"],
    )
    meaning.move_to([0, -1.65, 0])
    paced_play(scene, FadeIn(meaning, scale=0.92), run_time=1.1)
    cue(scene, started, 104.0)
    paced_play(scene, Indicate(general, color=cfg.GOLD, scale_factor=1.04), run_time=1.2)
    cue(scene, started, 110.0)

    # --- 110-139s: how violently it grows -------------------------------------
    growth_heading = top_caption("HOW  FAST  FACTORIALS  GROW", cfg.PURPLE)
    scene.play(FadeOut(meaning), FadeIn(growth_heading, shift=DOWN * 0.15),
               general.animate.scale(0.72).move_to([0, 3.15, 0]), run_time=1.2)

    bar_left = -5.9
    bar_max = 11.4
    axis = Line([bar_left, -2.9, 0], [bar_left + bar_max, -2.9, 0], color=cfg.MUTED, stroke_width=3, stroke_opacity=0.4)
    scene.play(Create(axis), run_time=0.6)
    scale_tag = outlined_text("COMPRESSED LOG SCALE", cfg.FONT["tiny"], cfg.MUTED)
    scale_tag.move_to([0, -1.35, 0])
    paced_play(scene, FadeIn(scale_tag), run_time=0.6)

    display = None
    bar = None
    for value in (1, 2, 3, 4, 5, 6, 8, 10, 12):
        total = factorial(value)
        width = float(np.interp(np.log10(total + 1), [0, np.log10(factorial(12))], [0.6, bar_max]))
        fresh_bar = RoundedRectangle(
            width=width, height=0.62, corner_radius=0.14,
            stroke_color=cfg.PURPLE, stroke_width=3,
            fill_color=cfg.PURPLE, fill_opacity=0.32,
        )
        fresh_bar.move_to([bar_left + width / 2, -2.35, 0])
        label = eq(rf"{value}! = {total:,}".replace(",", "{,}"), cfg.WHITE, 78)
        label.move_to([0, 0.35, 0])
        if bar is None:
            paced_play(scene, FadeIn(label, scale=1.2), GrowFromEdge(fresh_bar, LEFT), run_time=1.3)
            bar = fresh_bar
        else:
            # Transform keeps the same on-screen bar and re-shapes it, so the
            # growth reads as one object stretching rather than a cut.
            paced_play(
                scene,
                ReplacementTransform(display, label),
                Transform(bar, fresh_bar),
                run_time=1.3,
            )
        display = label
    closing = swap_caption(scene, None, "Twelve books: nearly half a billion shelves.", cfg.PURPLE)
    cue(scene, started, 136.5)
    paced_play(scene, Indicate(display, color=cfg.PURPLE, scale_factor=1.08), run_time=1.2)
    scene.remove(closing)
    scene.add(closing)

    end_scene(scene, started, cfg.SCENE_DURATIONS["03"])
