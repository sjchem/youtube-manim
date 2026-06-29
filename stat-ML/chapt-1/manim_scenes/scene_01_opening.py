"""Scene 01 — Grand series opening.

Cinematic opener in the style of 3Blue1Brown's Essence of Linear Algebra.
A universe of data points slowly comes alive, the true signal emerges
from the noise, then the course roadmap and Chapter 1 title reveal.

Narration cue: ~55 seconds
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene, cinematic_background, end_scene,
    glow_dot, narration_wait, paced_play, label,
)
from utils.physics_models import course_parts


class Scene01Opening(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background(show_bubbles=True))

    # ── Phase 1: Data universe — dots drift in from all directions ──────────
    rng = np.random.default_rng(42)
    n_signal, n_noise = 38, 50

    # Signal dots (near a sine wave)
    sig_pts = [(rng.uniform(-6.6, 6.6), 0.0) for _ in range(n_signal)]
    sig_pts = [
        (x, 1.4 * np.sin(0.62 * x) + rng.normal(0, 0.28))
        for x, _ in sig_pts
    ]
    signal_group = VGroup(*[
        Dot(point=[x, y, 0], radius=0.072, color=cfg.CYAN, fill_opacity=0.80)
        for x, y in sig_pts
    ])

    # Noise dots (random scatter)
    noise_group = VGroup(*[
        Dot(
            point=[rng.uniform(-6.8, 6.8), rng.uniform(-3.6, 3.6), 0],
            radius=0.042,
            color=cfg.MUTED,
            fill_opacity=0.38,
        )
        for _ in range(n_noise)
    ])

    paced_play(
        scene,
        LaggedStart(*[FadeIn(d, scale=0.3) for d in noise_group], lag_ratio=0.05),
        run_time=1.8,
    )
    paced_play(
        scene,
        LaggedStart(*[FadeIn(d, scale=0.5) for d in signal_group], lag_ratio=0.07),
        run_time=2.0,
    )
    narration_wait(scene, 0.6)

    # ── Phase 2: True signal curve emerges ──────────────────────────────────
    signal_curve = ParametricFunction(
        lambda t: np.array([t, 1.4 * np.sin(0.62 * t), 0]),
        t_range=[-6.8, 6.8],
        color=cfg.WHITE,
        stroke_width=cfg.VISUAL["signal_stroke"],
        stroke_opacity=0.85,
    )
    glow_shadow = signal_curve.copy().set_stroke(cfg.CYAN, width=22, opacity=0.10)
    paced_play(
        scene,
        FadeIn(glow_shadow),
        Create(signal_curve),
        run_time=2.2,
        rate_func=smooth,
    )
    narration_wait(scene, 0.4)

    # ── Phase 3: Dim data → show course title ───────────────────────────────
    paced_play(
        scene,
        signal_group.animate.set_fill(opacity=0.18),
        noise_group.animate.set_fill(opacity=0.12),
        signal_curve.animate.set_stroke(opacity=0.22),
        glow_shadow.animate.set_stroke(opacity=0.04),
        run_time=0.9,
    )

    series_lbl = Text(
        "STATISTICS FOR MACHINE LEARNING",
        font_size=cfg.FONT["small"],
        color=cfg.CYAN,
        weight=BOLD,
    )
    series_lbl.set_stroke(cfg.BG, width=4, background=True)

    title_line1 = Text("Why Statistics", font_size=cfg.FONT["hero"],
                        color=cfg.WHITE, weight=BOLD)
    title_line2 = Text("Matters in ML", font_size=cfg.FONT["hero"],
                        color=cfg.CYAN, weight=BOLD)
    for t in (title_line1, title_line2):
        t.set_stroke(cfg.BG, width=6, background=True)

    title_group = VGroup(series_lbl, title_line1, title_line2).arrange(DOWN, buff=0.3)
    title_group.move_to(ORIGIN + UP * 0.2)

    paced_play(scene, FadeIn(series_lbl, shift=DOWN * 0.12), run_time=0.7)
    paced_play(scene, Write(title_line1), run_time=1.1)
    paced_play(scene, Write(title_line2), run_time=0.9)

    # Underline glow
    underline = Line(
        title_group.get_left() + RIGHT * 0.4, title_group.get_right() - RIGHT * 0.4,
        color=cfg.GOLD, stroke_width=3.5,
    )
    underline.next_to(title_line2, DOWN, buff=0.22)
    paced_play(scene, Create(underline), run_time=0.7)
    narration_wait(scene, 1.0)

    # ── Phase 4: Course roadmap ──────────────────────────────────────────────
    paced_play(
        scene,
        FadeOut(title_group), FadeOut(underline),
        run_time=0.7,
    )

    parts = course_parts()
    boxes = VGroup()
    for i, p in enumerate(parts):
        box = RoundedRectangle(
            corner_radius=0.16, width=2.7, height=1.85,
            fill_color=cfg.COLORS["panel"], fill_opacity=0.88,
            stroke_color=p["color"], stroke_width=2.8,
        )
        p_lbl  = Text(p["part"],     font_size=33, color=p["color"], weight=BOLD)
        t_lbl  = Text(p["title"],    font_size=21, color=cfg.WHITE)
        t_lbl.scale_to_fit_width(min(t_lbl.width, box.width - 0.28))
        ch_lbl = Text(p["chapters"], font_size=20, color=cfg.MUTED)
        content = VGroup(p_lbl, t_lbl, ch_lbl).arrange(DOWN, buff=0.09)
        content.move_to(box.get_center())
        for mob in (p_lbl, t_lbl, ch_lbl):
            mob.set_stroke(cfg.BG, width=2, background=True)
        boxes.add(VGroup(box, content))

    boxes.arrange(RIGHT, buff=0.26).move_to(ORIGIN)

    paced_play(
        scene,
        LaggedStart(*[FadeIn(b, shift=UP * 0.18) for b in boxes], lag_ratio=0.22),
        run_time=1.8,
    )
    narration_wait(scene, 0.5)

    # ── Phase 5: Spotlight Part 1, Chapter 1 ────────────────────────────────
    # Dim parts 2-4, expand Part 1
    paced_play(
        scene,
        boxes[0].animate.scale(1.08),
        boxes[1].animate.set_fill(opacity=0.25),
        boxes[2].animate.set_fill(opacity=0.25),
        boxes[3].animate.set_fill(opacity=0.25),
        run_time=0.75,
    )

    you_are_here = Text("▶  YOU ARE HERE", font_size=cfg.FONT["small"],
                        color=cfg.GOLD, weight=BOLD)
    you_are_here.set_stroke(cfg.BG, width=3, background=True)
    you_are_here.next_to(boxes, DOWN, buff=0.28).set_x(0)

    ch_title = Text("Chapter 1: Why Statistics Matters",
                    font_size=cfg.FONT["tiny"], color=cfg.GOLD)
    ch_title.set_stroke(cfg.BG, width=3, background=True)
    if ch_title.width > cfg.SAFE_WIDTH - 0.8:
        ch_title.scale_to_fit_width(cfg.SAFE_WIDTH - 0.8)
    ch_title.next_to(you_are_here, DOWN, buff=0.15).set_x(0)

    paced_play(scene, FadeIn(you_are_here, shift=UP * 0.10), run_time=0.6)
    paced_play(scene, FadeIn(ch_title, shift=UP * 0.08), run_time=0.6)
    narration_wait(scene, 1.2)

    # ── Phase 6: Closing question ────────────────────────────────────────────
    paced_play(
        scene,
        FadeOut(VGroup(*boxes[1:]), you_are_here, ch_title),
        run_time=0.7,
    )
    paced_play(scene, boxes[0].animate.move_to(UP * 1.5).scale(0.9), run_time=0.6)

    question = VGroup(
        Text("Why do ML engineers", font_size=cfg.FONT["label"],
             color=cfg.WHITE, weight=BOLD),
        Text("need statistics?", font_size=cfg.FONT["label"],
             color=cfg.CYAN, weight=BOLD),
    ).arrange(DOWN, buff=0.18)
    for t in question:
        t.set_stroke(cfg.BG, width=5, background=True)
    question.move_to(DOWN * 0.7)

    paced_play(scene, LaggedStart(*[Write(t) for t in question], lag_ratio=0.5), run_time=1.5)
    narration_wait(scene, 1.5)

    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["01"])
