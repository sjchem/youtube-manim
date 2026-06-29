"""Scene 06 — Why Models Fail: Overfitting.

A model that memorises training data learns noise, not signal.
It fits every point perfectly — and fails completely on new data.
Statistics teaches us to distinguish models that generalise from
models that merely memorise.

Narration cue: ~58 seconds
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene, bottom_caption, cinematic_background, end_scene,
    label, narration_wait, paced_play, stat_axes,
)
from utils.math_utils import linear_data, overfit_poly_points


SLOPE     = 0.55
INTERCEPT = 0.10


class Scene06Overfitting(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background(show_bubbles=False))

    axes, ax_labels = stat_axes(
        x_range=[-4, 4, 2], y_range=[-3.0, 3.0, 1],
        x_length=9.5, y_length=5.8,
        x_label="x  (feature)", y_label="y  (target)",
    )
    axes.move_to(ORIGIN + DOWN * 0.1)

    # Fixed training data
    xs_train, ys_train = linear_data(
        n=10, slope=SLOPE, intercept=INTERCEPT,
        x_range=(-3.5, 3.5), noise_std=0.55, seed=31,
    )

    # ── Phase 1: Training data appears ──────────────────────────────────────
    train_dots = VGroup(*[
        Dot(point=axes.c2p(x, y), radius=0.085,
            color=cfg.CYAN, fill_opacity=0.90)
        for x, y in zip(xs_train, ys_train)
    ])
    train_lbl = label("Training data", font_size=cfg.FONT["label"], color=cfg.CYAN)
    train_lbl.set_stroke(cfg.BG, width=3, background=True)
    train_lbl.to_corner(UL, buff=0.55).shift(DOWN * 0.6)

    cap_train = bottom_caption("We train on a small set of examples.", color=cfg.CYAN)

    paced_play(scene, Create(axes), FadeIn(*ax_labels), run_time=0.9)
    paced_play(
        scene,
        LaggedStart(*[FadeIn(d, scale=0.5) for d in train_dots], lag_ratio=0.10),
        FadeIn(train_lbl), FadeIn(cap_train, shift=UP * 0.1),
        run_time=1.6,
    )
    narration_wait(scene, 0.6)

    # ── Phase 2: Good linear fit (generalises) ───────────────────────────────
    x0, x1 = -3.9, 3.9
    ls  = axes.c2p(x0, SLOPE * x0 + INTERCEPT)
    le  = axes.c2p(x1, SLOPE * x1 + INTERCEPT)

    good_line = Line(ls, le, color=cfg.GREEN, stroke_width=5.5)
    good_glow = good_line.copy().set_stroke(cfg.GREEN, width=22, opacity=0.10)

    good_lbl = label("Simple model — generalises", font_size=cfg.FONT["small"], color=cfg.GREEN)
    good_lbl.set_stroke(cfg.BG, width=3, background=True)
    good_lbl.to_corner(UR, buff=0.55).shift(DOWN * 0.5)

    cap_good = bottom_caption("A simple fit captures the trend.", color=cfg.GREEN)

    paced_play(
        scene,
        FadeIn(good_glow), Create(good_line),
        FadeIn(good_lbl),
        FadeOut(cap_train), FadeIn(cap_good, shift=UP * 0.1),
        run_time=1.2,
    )
    narration_wait(scene, 0.6)

    # ── Phase 3: Overfit polynomial (memorises noise) ────────────────────────
    xs_sorted = np.sort(xs_train)
    sort_idx  = np.argsort(xs_train)
    ys_sorted = ys_train[sort_idx]

    x_poly, y_poly = overfit_poly_points(xs_sorted, ys_sorted, n_eval=140)

    over_pts  = [axes.c2p(x, y) for x, y in zip(x_poly, y_poly)]
    over_path = VMobject().set_points_smoothly(over_pts)
    over_path.set_stroke(color=cfg.RED, width=5.0, opacity=0.90)
    over_glow = over_path.copy().set_stroke(cfg.RED, width=20, opacity=0.10)

    over_lbl = label("Complex model — memorises noise", font_size=cfg.FONT["small"], color=cfg.RED)
    over_lbl.set_stroke(cfg.BG, width=3, background=True)
    over_lbl.next_to(good_lbl, DOWN, buff=0.18)
    if over_lbl.get_right()[0] > cfg.SAFE_WIDTH / 2:
        over_lbl.shift(LEFT * (over_lbl.get_right()[0] - cfg.SAFE_WIDTH / 2 + 0.1))

    train_error = label("Training error: ~0", font_size=cfg.FONT["tiny"], color=cfg.RED)
    train_error.next_to(train_lbl, DOWN, buff=0.14).align_to(train_lbl, LEFT)

    cap_over = bottom_caption("An overfit model memorises the training data.", color=cfg.RED)

    paced_play(
        scene,
        FadeIn(over_glow), Create(over_path),
        FadeIn(over_lbl), FadeIn(train_error, shift=UP * 0.08),
        FadeOut(cap_good), FadeIn(cap_over, shift=UP * 0.1),
        run_time=2.0,
        rate_func=smooth,
    )
    narration_wait(scene, 0.6)

    # ── Phase 4: New unseen test point ──────────────────────────────────────
    x_test  = 1.8
    y_true  = SLOPE * x_test + INTERCEPT + 0.20   # near true line
    y_good  = SLOPE * x_test + INTERCEPT
    y_bad   = float(np.polyval(
        np.polyfit(xs_sorted, ys_sorted, min(len(xs_sorted) - 1, 9)), x_test
    ))
    y_bad   = float(np.clip(y_bad, -2.8, 2.8))

    test_dot = Dot(point=axes.c2p(x_test, -3.5), radius=0.10,
                   color=cfg.PURPLE, fill_opacity=0.0)
    scene.add(test_dot)

    cap_test = bottom_caption("New data — how does each model do?", color=cfg.PURPLE)

    paced_play(
        scene,
        test_dot.animate.set_fill(opacity=1.0).move_to(axes.c2p(x_test, y_true)),
        FadeOut(cap_over), FadeIn(cap_test, shift=UP * 0.1),
        run_time=0.8,
    )
    narration_wait(scene, 0.4)

    # Green prediction arrow (good)
    arr_good = Arrow(
        axes.c2p(x_test, y_true), axes.c2p(x_test, y_good),
        buff=0, color=cfg.GREEN, stroke_width=5,
        max_tip_length_to_length_ratio=0.25,
    )
    # Red prediction arrow (bad)
    arr_bad = Arrow(
        axes.c2p(x_test, y_true), axes.c2p(x_test, y_bad),
        buff=0, color=cfg.RED, stroke_width=5,
        max_tip_length_to_length_ratio=0.25,
    )

    check = Text("✓", font_size=cfg.FONT["section"], color=cfg.GREEN, weight=BOLD)
    check.set_stroke(cfg.BG, width=3, background=True)
    check.next_to(arr_good, RIGHT, buff=0.18)

    cross = Text("✗", font_size=cfg.FONT["section"], color=cfg.RED, weight=BOLD)
    cross.set_stroke(cfg.BG, width=3, background=True)
    cross.next_to(arr_bad, RIGHT, buff=0.18)

    paced_play(scene, GrowArrow(arr_good), FadeIn(check), run_time=0.8)
    paced_play(scene, GrowArrow(arr_bad),  FadeIn(cross), run_time=0.8)

    test_error = label("Test error reveals it", font_size=cfg.FONT["tiny"], color=cfg.GOLD)
    test_error.next_to(test_dot, DOWN, buff=0.22).shift(RIGHT * 0.55)
    paced_play(scene, FadeIn(test_error, shift=DOWN * 0.08), run_time=0.55)
    narration_wait(scene, 0.5)

    # Final caption
    cap_final = bottom_caption("Fitting the training data ≠ generalising to new data.", color=cfg.GOLD)
    paced_play(
        scene,
        FadeOut(cap_test), FadeIn(cap_final, shift=UP * 0.1),
        run_time=0.6,
    )
    narration_wait(scene, 1.3)

    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["06"])
