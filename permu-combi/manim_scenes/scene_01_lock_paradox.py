"""Scene 01: the lock that is badly named, and the question it hides."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    chip, chip_target, clear_background, cue, begin_scene, end_scene, eq, glow_line,
    outlined_text, ring_points, shuffle_inside_ring, slot_row, team_ring,
    title_card, verdict_badge,
)
from manim_scenes.props_3d import padlock, wheel_digit


class Scene01LockParadox(ThreeDScene):
    """A combination lock is really a permutation lock."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: ThreeDScene) -> None:
    started = begin_scene(scene, "01")
    clear_background(scene)
    scene.camera.background_color = "#02101F"
    scene.set_camera_orientation(phi=0, theta=-PI / 2, zoom=1, frame_center=ORIGIN)

    overlays: list[Mobject] = []

    def hud(text: str, position, size: int = 38, color: str = cfg.WHITE) -> Text:
        mob = outlined_text(text, size, color).move_to(np.array(position))
        scene.add_fixed_in_frame_mobjects(mob)
        scene.remove(mob)
        overlays.append(mob)
        return mob

    # --- 0-9s: one object in the dark, turning just enough to feel solid -----
    rng = np.random.default_rng(cfg.SEED)
    dust = VGroup(
        *[
            Dot(
                [rng.uniform(-7.4, 7.4), rng.uniform(-4.1, 4.1), rng.uniform(-3.5, -1.2)],
                radius=rng.uniform(0.008, 0.026),
                color=cfg.CYAN,
                fill_opacity=rng.uniform(0.2, 0.7),
            )
            for _ in range(90)
        ]
    )
    scene.add(dust)

    lock = padlock(cfg.CYAN, scale=1.24).move_to([0, -0.15, 0])
    scene.play(FadeIn(lock, scale=0.7, shift=IN * 0.6), run_time=1.6)

    digits = VGroup()
    for window in lock.windows:
        glyph = wheel_digit("0", cfg.MUTED, 54).move_to(window.get_center())
        digits.add(glyph)
    scene.play(FadeIn(digits), run_time=0.8)
    scene.move_camera(phi=20 * DEGREES, theta=-100 * DEGREES, run_time=2.6)
    opening = hud("A COMBINATION LOCK", [0, 3.15, 0], 44, cfg.CYAN)
    scene.play(FadeIn(opening, shift=DOWN * 0.2), run_time=0.9)
    cue(scene, started, 9.0)

    # --- 9-24s: 1 - 2 - 3 opens it ------------------------------------------
    def turn_wheel(index: int, value: str, color: str, run_time: float = 1.0) -> None:
        """Scroll a new digit up into the window while the wheel turns."""
        window = lock.windows[index]
        fresh = wheel_digit(value, color, 54).move_to(window.get_center() + DOWN * 0.62)
        fresh.set_opacity(0)
        scene.add(fresh)
        scene.play(
            Rotate(lock.wheels[index], angle=-TAU / 3, axis=RIGHT),
            digits[index].animate.shift(UP * 0.62).set_opacity(0),
            fresh.animate.move_to(window.get_center()).set_opacity(1),
            lock.windows[index].animate.set_stroke(color, width=3.6, opacity=1),
            run_time=run_time,
        )
        scene.remove(digits[index])
        digits.submobjects[index] = fresh

    entry = hud("1  →  2  →  3", [0, -3.05, 0], 56, cfg.GOLD)
    scene.play(FadeIn(entry, shift=UP * 0.2), run_time=0.7)
    for index, value in enumerate("123"):
        turn_wheel(index, value, cfg.GOLD, run_time=1.25)
    cue(scene, started, 16.6)

    open_badge = verdict_badge("CLICK", True, scale=1.25).move_to([0, 2.15, 0])
    scene.add_fixed_in_frame_mobjects(open_badge)
    overlays.append(open_badge)
    scene.remove(open_badge)
    scene.play(
        *[d.animate.set_color(cfg.GREEN) for d in digits],
        *[w.animate.set_stroke(cfg.GREEN, width=3.6, opacity=1) for w in lock.windows],
        run_time=0.8,
    )
    scene.play(
        lock.shackle.animate.shift(UP * 0.85).rotate(-0.55, axis=OUT, about_point=lock.legs[1].get_top()),
        FadeIn(open_badge, scale=1.2),
        FadeOut(opening),
        run_time=1.1,
    )
    cue(scene, started, 21.0)
    scene.play(Indicate(open_badge, color=cfg.WHITE, scale_factor=1.08), run_time=0.9)
    cue(scene, started, 24.0)

    # --- 24-38s: the same three digits, reversed, fail ------------------------
    scene.play(
        lock.shackle.animate.rotate(0.55, axis=OUT, about_point=lock.legs[1].get_top()).shift(DOWN * 0.85),
        FadeOut(open_badge, entry),
        *[d.animate.set_color(cfg.MUTED) for d in digits],
        *[w.animate.set_stroke(cfg.CYAN, width=2.6, opacity=0.75) for w in lock.windows],
        run_time=1.2,
    )
    reversed_entry = hud("3  →  2  →  1", [0, -3.05, 0], 56, cfg.ORANGE)
    scene.play(FadeIn(reversed_entry, shift=UP * 0.2), run_time=0.7)
    for index, value in enumerate("321"):
        turn_wheel(index, value, cfg.ORANGE, run_time=1.2)
    cue(scene, started, 31.0)

    locked_badge = verdict_badge("LOCKED", False, scale=1.25).move_to([0, 2.15, 0])
    scene.add_fixed_in_frame_mobjects(locked_badge)
    overlays.append(locked_badge)
    scene.remove(locked_badge)
    scene.play(
        *[d.animate.set_color(cfg.RED) for d in digits],
        *[w.animate.set_stroke(cfg.RED, width=3.6, opacity=1) for w in lock.windows],
        FadeIn(locked_badge, scale=1.2),
        run_time=0.9,
    )
    scene.play(Wiggle(lock.body, scale_value=1.02, rotation_angle=0.03 * TAU), run_time=1.1)
    cue(scene, started, 38.0)

    # --- 38-51s: same digits, different order, different result ---------------
    verdict = hud("SAME DIGITS.  DIFFERENT ORDER.", [0, 3.15, 0], 44, cfg.WHITE)
    scene.play(FadeIn(verdict, shift=DOWN * 0.18), FadeOut(locked_badge), run_time=0.9)

    # Put the two attempts beside each other; the contrast is the whole hook.
    hardware = VGroup(lock, digits)
    scene.play(
        hardware.animate.scale(0.66, about_point=hardware.get_center()).shift(LEFT * 3.7 + DOWN * 0.2),
        FadeOut(reversed_entry),
        run_time=1.3,
    )
    rows = VGroup()
    for code, mark, colour, y in (("1  2  3", "OPEN", cfg.GREEN, 0.95), ("3  2  1", "LOCKED", cfg.RED, -0.85)):
        row = VGroup(
            outlined_text(code, 62, colour),
            outlined_text("→", 54, cfg.MUTED),
            outlined_text(mark, 52, colour),
        ).arrange(RIGHT, buff=0.42)
        row.move_to([3.6, y, 0])
        rows.add(row)
    scene.add_fixed_in_frame_mobjects(rows)
    overlays.append(rows)
    scene.remove(rows)
    scene.play(FadeIn(rows[0], shift=RIGHT * 0.25), run_time=0.9)
    scene.play(FadeIn(rows[1], shift=RIGHT * 0.25), run_time=0.9)
    divider = Line([1.5, 0.05, 0], [5.9, 0.05, 0], color=cfg.MUTED, stroke_width=3, stroke_opacity=0.5)
    scene.add_fixed_in_frame_mobjects(divider)
    overlays.append(divider)
    scene.remove(divider)
    scene.play(Create(divider), run_time=0.6)
    cue(scene, started, 45.2)
    scene.play(
        Indicate(rows[0], color=cfg.WHITE, scale_factor=1.05),
        Indicate(rows[1], color=cfg.WHITE, scale_factor=1.05),
        run_time=1.2,
    )
    cue(scene, started, 48.0)

    scene.move_camera(phi=0, theta=-PI / 2, run_time=2.2)
    scene.play(
        FadeOut(lock, digits, dust, rows, divider),
        run_time=1.1,
    )
    scene.remove_fixed_in_frame_mobjects(*overlays)
    scene.camera.background_color = cfg.BG
    cue(scene, started, 51.5)

    # --- 50-63s: 123 becomes ABC, and ABC is not BAC -------------------------
    numeric = VGroup(*[eq(d, cfg.GOLD, 96) for d in "123"]).arrange(RIGHT, buff=0.9).move_to([0, 0.9, 0])
    scene.play(FadeOut(verdict), FadeIn(numeric, scale=1.15), run_time=0.9)
    letters = VGroup(*[chip(name, cfg.GOLD, 0.62) for name in "ABC"])
    for source, target in zip(numeric, letters):
        target.move_to(source.get_center())
    scene.play(
        *[ReplacementTransform(numeric[i], letters[i]) for i in range(3)],
        run_time=1.1,
    )

    ranked = slot_row(3, ranks=["1st", "2nd", "3rd"], size=1.35, buff=0.5, center=[0, 0.9, 0])
    scene.play(FadeIn(ranked, shift=UP * 0.2), letters.animate.move_to([0, 0.9, 0]).set_opacity(0.0), run_time=0.9)
    scene.remove(letters)
    seated = VGroup()
    for index, name in enumerate("ABC"):
        piece = chip(name, cfg.CHOSEN, 0.48).move_to(ranked[index].body.get_center())
        seated.add(piece)
    scene.play(LaggedStart(*[FadeIn(p, scale=0.6) for p in seated], lag_ratio=0.25), run_time=1.0)

    swapped = eq(r"ABC \;\neq\; BAC", cfg.ORANGE, 86).move_to([0, -1.6, 0])
    scene.play(
        Swap(seated[0], seated[1], path_arc=PI * 0.8),
        run_time=1.0,
    )
    scene.play(FadeIn(swapped, shift=UP * 0.2), run_time=0.8)
    order_label = outlined_text("ORDER MATTERS  →  PERMUTATION", cfg.FONT["body"], cfg.ORANGE)
    order_label.to_edge(DOWN, buff=0.45)
    scene.play(FadeIn(order_label, shift=UP * 0.2), run_time=0.8)
    cue(scene, started, 64.5)

    # --- 63-76s: the same three objects inside one ring ----------------------
    # Keep three clear visual bands: team, equality, and the conclusion.
    # The earlier, larger ring placed its label directly over the equation.
    ring = team_ring(1.45, cfg.UNORDERED, [0, 1.35, 0], label="ONE TEAM")
    seats = ring_points(ring, 3, radius_scale=0.62)
    scene.play(
        FadeOut(ranked, swapped, order_label),
        Create(ring),
        run_time=1.0,
    )
    scene.play(
        *[
            Transform(seated[i], chip_target(seated[i], cfg.UNORDERED).move_to(seats[i]))
            for i in range(3)
        ],
        run_time=1.1,
    )
    shuffle_inside_ring(scene, list(seated), seats, run_time=1.2)
    shuffle_inside_ring(scene, list(seated), seats, run_time=1.2)
    same = eq(r"\{A,B,C\} \;=\; \{B,A,C\}", cfg.UNORDERED, 68).move_to([0, -1.55, 0])
    scene.play(FadeIn(same, shift=UP * 0.2), run_time=0.9)
    group_label = outlined_text("ORDER DOESN'T MATTER  →  COMBINATION", cfg.FONT["body"], cfg.UNORDERED)
    group_label.to_edge(DOWN, buff=0.45)
    scene.play(FadeIn(group_label, shift=UP * 0.15), run_time=0.8)
    cue(scene, started, 77.5)

    # --- 76-84s: the question the whole film answers -------------------------
    question = VGroup(
        outlined_text("So what makes one problem a permutation", cfg.FONT["label"], cfg.WHITE),
        outlined_text("and another a combination?", cfg.FONT["label"], cfg.WHITE),
    ).arrange(DOWN, buff=0.16).move_to([0, -0.2, 0])
    scene.play(
        FadeOut(ring, seated, same, group_label),
        FadeIn(question, shift=UP * 0.2),
        run_time=1.2,
    )
    cue(scene, started, 83.2)
    scene.play(FadeOut(question, shift=UP * 0.3), run_time=0.8)

    # --- 83-91s: title ------------------------------------------------------
    hero = title_card("PERMUTATIONS & COMBINATIONS", cfg.VIDEO_SUBTITLE, cfg.GOLD)
    hero.move_to([0, 0.35, 0])
    beam = glow_line([-6.4, -2.3, 0], [6.4, -2.3, 0], cfg.CYAN, 3)
    scene.play(FadeIn(hero, scale=1.06), run_time=1.2)
    scene.play(Create(beam), run_time=0.8)
    cue(scene, started, 90.4)
    scene.play(Indicate(hero[0], color=cfg.WHITE, scale_factor=1.03), run_time=1.0)

    end_scene(scene, started, cfg.SCENE_DURATIONS["01"])
    scene.set_camera_orientation(phi=0, theta=-PI / 2, zoom=1, frame_center=ORIGIN)
    scene.camera.background_color = cfg.BG
