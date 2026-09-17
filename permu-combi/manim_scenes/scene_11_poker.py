"""Scene 11: two and a half million hands, counted without listing one."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene, bottom_caption, card_back, clear_background, cue, end_scene, eq,
    outlined_text, paced_play, playing_card, team_ring,
)
from manim_scenes.props_3d import hand_cloud
from utils.math_utils import combinations, factorial, tex_number

HAND = (("A", "♠", False), ("K", "♥", True), ("7", "♣", False),
        ("10", "♦", True), ("4", "♠", False))


class Scene11Poker(ThreeDScene):
    """Why a poker hand is a combination, and how big that count is."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: ThreeDScene) -> None:
    started = begin_scene(scene, "11")
    clear_background(scene)
    scene.camera.background_color = "#03152A"
    scene.set_camera_orientation(phi=0, theta=-PI / 2, zoom=1, frame_center=ORIGIN)

    overlays: list[Mobject] = []

    def pin(mob: Mobject) -> Mobject:
        scene.add_fixed_in_frame_mobjects(mob)
        scene.remove(mob)
        overlays.append(mob)
        return mob

    heading = pin(outlined_text("HOW  MANY  POKER  HANDS?", cfg.FONT["body"], cfg.GOLD).move_to([0, 3.4, 0]))

    # --- 0-12s: the deck ------------------------------------------------------
    deck = VGroup()
    for index in range(16):
        card = card_back(1.5, 2.15)
        card.shift(RIGHT * index * 0.035 + UP * index * 0.045 + OUT * index * 0.06)
        deck.add(card)
    deck.move_to([0, 0.35, 0])
    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), run_time=0.8)
    paced_play(scene, FadeIn(deck, scale=0.7), run_time=1.4)
    fifty_two = pin(eq("52", cfg.CYAN, 96).move_to([-4.6, 0.35, 0]))
    fifty_two_tag = pin(outlined_text("CARDS", cfg.FONT["small"], cfg.CYAN).move_to([-4.6, -0.75, 0]))
    paced_play(scene, FadeIn(fifty_two, scale=1.25), FadeIn(fifty_two_tag), run_time=1.0)
    caption = pin(bottom_caption("Deal five cards.", cfg.CYAN))
    paced_play(scene, FadeIn(caption, shift=UP * 0.15), run_time=0.8)
    cue(scene, started, 12.0)
    paced_play(
        scene,
        FadeOut(heading, shift=UP * 0.15),
        FadeOut(fifty_two, fifty_two_tag, shift=LEFT * 0.15),
        run_time=0.5,
    )

    # --- 12-26s: five cards on the table ---------------------------------------
    cards = VGroup(*[playing_card(rank, suit, red=red, width=1.45, height=2.1) for rank, suit, red in HAND])
    spread = VGroup(*[card.copy() for card in cards])
    spread.arrange(RIGHT, buff=0.34).move_to([0, 0.35, 0])
    # Each card only exists once it leaves the deck, so no two faces ever stack.
    for index, card in enumerate(cards):
        card.move_to(deck.get_center())
        scene.add(card)
        paced_play(
            scene,
            Transform(card, spread[index], path_arc=-0.4),
            run_time=0.62,
        )
    paced_play(scene, FadeOut(deck), run_time=0.6)
    cue(scene, started, 20.0)

    # --- 20-36s: rearranging the hand changes nothing ---------------------------
    fresh_caption = pin(bottom_caption("Does the order they arrived in matter?", cfg.GOLD))
    paced_play(scene, FadeOut(caption), FadeIn(fresh_caption, shift=UP * 0.12), run_time=0.7)
    caption = fresh_caption
    seats = [card.get_center() for card in cards]
    for shift_by in (2, 3):
        order = [(index + shift_by) % 5 for index in range(5)]
        paced_play(
            scene,
            *[cards[index].animate.move_to(seats[order[index]]) for index in range(5)],
            run_time=1.5,
            path_arc=PI * 0.45,
        )
        seats = [seats[order.index(index)] for index in range(5)]
    ring = team_ring(2.75, cfg.UNORDERED, [0, 0.35, 0])
    ring.ring.stretch(1.85, 0)
    ring.halo.stretch(1.85, 0)
    paced_play(scene, Create(ring), run_time=1.0)
    same = pin(outlined_text("THE  SAME  HAND", cfg.FONT["body"], cfg.GOLD).move_to([0, -1.55, 0]))
    paced_play(scene, FadeIn(same, shift=UP * 0.15), run_time=0.9)
    cue(scene, started, 34.0)

    # --- 34-48s: so it is a combination ----------------------------------------
    fresh_caption = pin(bottom_caption("Order ignored. That makes it a combination.", cfg.UNORDERED))
    paced_play(scene, FadeOut(caption), FadeIn(fresh_caption, shift=UP * 0.12), run_time=0.7)
    caption = fresh_caption
    notation = pin(eq(r"\binom{52}{5}", cfg.UNORDERED, 110).move_to([0, 0.35, 0]))
    scene.play(
        FadeOut(cards, ring, same),
        FadeIn(notation, scale=1.15),
        run_time=1.4,
    )
    cue(scene, started, 42.0)

    # --- 42-62s: cancel the factorials -----------------------------------------
    steps = (
        r"\binom{52}{5} = \frac{52!}{5!\,47!}",
        r"= \frac{52\times51\times50\times49\times48}{5!}",
        rf"= \frac{{{tex_number(52 * 51 * 50 * 49 * 48)}}}{{{factorial(5)}}}",
    )
    lines = VGroup(*[
        eq(text, colour, 72)
        for text, colour in zip(steps, (cfg.UNORDERED, cfg.CYAN, cfg.GOLD))
    ])
    lines.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([0, 0.55, 0])
    for line in lines:
        pin(line)
    scene.play(ReplacementTransform(notation, lines[0]), run_time=1.2)
    paced_play(scene, FadeIn(lines[1], shift=UP * 0.2), run_time=1.2)
    paced_play(scene, FadeIn(lines[2], shift=UP * 0.2), run_time=1.2)
    cue(scene, started, 52.0)

    answer = pin(eq(tex_number(combinations(52, 5)), cfg.GOLD, 132).move_to([0, -0.2, 0]))
    scene.play(
        FadeOut(lines, caption),
        FadeIn(answer, scale=1.2),
        run_time=1.5,
    )
    caption = pin(bottom_caption("Almost 2.6 million hands.", cfg.GOLD))
    paced_play(scene, FadeIn(caption, shift=UP * 0.15), run_time=0.8)
    paced_play(scene, Indicate(answer, color=cfg.WHITE, scale_factor=1.06), run_time=1.1)
    cue(scene, started, 60.0)

    # --- 60-81s: the flood, seen as depth ---------------------------------------
    cloud = hand_cloud(190, depth=6.5)
    # Flat mini-hands can otherwise draw over the fixed result. Preserve a
    # quiet title band around the number while keeping the cloud dense elsewhere.
    for hand in cloud:
        x, y, _ = hand.get_center()
        if abs(x) < 3.6 and y > 2.2:
            hand.shift(DOWN * (y - (2.05 + 0.08 * abs(x))))
        elif y < -2.55:
            hand.shift(UP * ((-2.42 - 0.06 * abs(x) / 7.4) - y))
    scene.play(
        answer.animate.scale(0.62).move_to([0, 3.25, 0]),
        run_time=1.1,
    )
    fresh_caption = pin(bottom_caption("Counted without listing a single one.", cfg.CYAN))
    paced_play(
        scene,
        LaggedStart(*[FadeIn(hand, scale=0.6) for hand in cloud], lag_ratio=0.004),
        run_time=4.6,
    )
    scene.move_camera(phi=14 * DEGREES, run_time=2.6)
    paced_play(scene, FadeOut(caption), FadeIn(fresh_caption, shift=UP * 0.12), run_time=0.8)
    caption = fresh_caption
    scene.move_camera(phi=0, run_time=2.4)
    cue(scene, started, 79.5)
    paced_play(scene, Indicate(answer, color=cfg.GOLD, scale_factor=1.1), run_time=1.3)

    end_scene(scene, started, cfg.SCENE_DURATIONS["11"])
    scene.remove_fixed_in_frame_mobjects(*overlays)
    scene.set_camera_orientation(phi=0, theta=-PI / 2, zoom=1, frame_center=ORIGIN)
    scene.camera.background_color = cfg.BG
