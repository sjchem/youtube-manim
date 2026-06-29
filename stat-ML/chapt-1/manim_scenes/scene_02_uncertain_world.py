"""Scene 02 — The Uncertain World.

The real world does not hand us clean data. Every measurement carries
noise. Statistics is the discipline that lets us reason under that
uncertainty rather than pretending it does not exist.

Narration cue: ~47 seconds
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene, bottom_caption, cinematic_background, end_scene,
    eq, glow_dot, narration_wait, paced_play, label,
)
from utils.math_utils import noisy_sine_data


class Scene02UncertainWorld(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background(show_bubbles=True))

    # ── Phase 1: A hidden "truth" — the true sine signal ────────────────────
    caption_truth = bottom_caption("The world has a true pattern…", color=cfg.CYAN)

    true_curve = ParametricFunction(
        lambda t: np.array([t, 1.6 * np.sin(0.6 * t), 0]),
        t_range=[-6.5, 6.5],
        color=cfg.GREEN,
        stroke_width=5.5,
        stroke_opacity=0.0,
    )
    glow_bg = true_curve.copy().set_stroke(cfg.GREEN, width=22, opacity=0.0)
    scene.add(glow_bg, true_curve)

    paced_play(
        scene,
        true_curve.animate.set_stroke(opacity=0.90),
        glow_bg.animate.set_stroke(opacity=0.12),
        FadeIn(caption_truth, shift=UP * 0.1),
        run_time=1.5,
    )
    narration_wait(scene, 0.8)

    # ── Phase 2: Real-world observations — noisy and incomplete ─────────────
    xs, ys_noisy, ys_true = noisy_sine_data(n=55, noise_std=0.55, seed=13)

    obs_dots = VGroup(*[
        Dot(point=[x, y, 0], radius=0.07, color=cfg.ORANGE, fill_opacity=0.82)
        for x, y in zip(xs, ys_noisy)
    ])

    caption_noise = bottom_caption("…but data is noisy and incomplete.", color=cfg.ORANGE)

    paced_play(
        scene,
        LaggedStart(*[FadeIn(d, scale=0.4) for d in obs_dots], lag_ratio=0.04),
        run_time=2.0,
    )
    paced_play(
        scene,
        FadeOut(caption_truth),
        FadeIn(caption_noise, shift=UP * 0.1),
        run_time=0.6,
    )
    narration_wait(scene, 0.6)

    # ── Phase 3: Measurement uncertainty bars on a few points ───────────────
    n_bars = 8
    rng = np.random.default_rng(77)
    bar_indices = rng.choice(len(xs), size=n_bars, replace=False)

    error_bars = VGroup()
    for idx in bar_indices:
        x_pos = xs[idx]
        y_pos = ys_noisy[idx]
        half  = rng.uniform(0.25, 0.55)
        bar   = Line(
            [x_pos, y_pos - half, 0], [x_pos, y_pos + half, 0],
            color=cfg.GOLD, stroke_width=3.5, stroke_opacity=0.78,
        )
        cap_b = Line([x_pos - 0.12, y_pos - half, 0], [x_pos + 0.12, y_pos - half, 0],
                     color=cfg.GOLD, stroke_width=2.5, stroke_opacity=0.78)
        cap_t = Line([x_pos - 0.12, y_pos + half, 0], [x_pos + 0.12, y_pos + half, 0],
                     color=cfg.GOLD, stroke_width=2.5, stroke_opacity=0.78)
        error_bars.add(VGroup(bar, cap_b, cap_t))

    paced_play(
        scene,
        LaggedStart(*[GrowFromCenter(eb) for eb in error_bars], lag_ratio=0.10),
        run_time=1.5,
    )

    uncertainty_tags = VGroup(
        label("missing values", font_size=cfg.FONT["tiny"], color=cfg.PURPLE),
        label("sensor drift", font_size=cfg.FONT["tiny"], color=cfg.GOLD),
        label("noisy labels", font_size=cfg.FONT["tiny"], color=cfg.ORANGE),
    ).arrange(RIGHT, buff=0.42)
    uncertainty_tags.to_edge(UP, buff=0.48)
    paced_play(
        scene,
        LaggedStart(*[FadeIn(t, shift=DOWN * 0.08) for t in uncertainty_tags], lag_ratio=0.18),
        run_time=0.9,
    )
    narration_wait(scene, 0.5)

    # ── Phase 4: Question mark — can we find the true pattern? ──────────────
    paced_play(
        scene,
        true_curve.animate.set_stroke(opacity=0.20),
        glow_bg.animate.set_stroke(opacity=0.04),
        FadeOut(uncertainty_tags),
        run_time=0.75,
    )

    question_mark = Text("?", font_size=180, color=cfg.PURPLE, weight=BOLD)
    question_mark.set_stroke(cfg.BG, width=10, background=True)
    question_mark.set_fill(opacity=0.0)
    scene.add(question_mark)

    caption_q = bottom_caption("Can we recover the truth from the noise?", color=cfg.PURPLE)

    paced_play(
        scene,
        question_mark.animate.set_fill(opacity=0.55),
        FadeOut(caption_noise),
        FadeIn(caption_q, shift=UP * 0.1),
        run_time=1.0,
    )
    narration_wait(scene, 0.5)

    # ── Phase 5: Statistics label ────────────────────────────────────────────
    stat_label = Text("Statistics gives us the tools.", font_size=cfg.FONT["body"],
                      color=cfg.CYAN, weight=BOLD)
    stat_label.set_stroke(cfg.BG, width=5, background=True)
    stat_label.to_edge(UP, buff=0.42)

    paced_play(
        scene,
        question_mark.animate.set_fill(opacity=0.20),
        true_curve.animate.set_stroke(opacity=0.65),
        glow_bg.animate.set_stroke(opacity=0.10),
        FadeIn(stat_label, shift=DOWN * 0.12),
        FadeOut(caption_q),
        run_time=1.1,
    )
    narration_wait(scene, 1.2)

    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["02"])
