"""Scene 07 — Bias-Variance Tradeoff.

The dartboard metaphor makes bias and variance intuitive:
• High bias  → predictions consistently off-target (underfitting)
• High variance → predictions wildly scattered (overfitting)
• The sweet spot → low bias AND low variance

Narration cue: ~77 seconds
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene, bottom_caption, cinematic_background, end_scene,
    label, narration_wait, paced_play,
)
from utils.physics_models import bias_variance_shots


class Scene07BiasVariance(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background(show_bubbles=False))

    # ── Build one dartboard ──────────────────────────────────────────────────
    def make_target(pos: list[float]) -> VGroup:
        rings = VGroup()
        specs = [
            (2.05, cfg.COLORS["line"],     0.06),
            (1.40, cfg.MUTED,              0.09),
            (0.82, cfg.ORANGE,             0.12),
            (0.32, cfg.GREEN,              0.40),
        ]
        for r, col, op in specs:
            rings.add(Circle(radius=r, color=col, stroke_width=2.2,
                             fill_color=col, fill_opacity=op))
        cross_h = Line([-2.2, 0, 0], [2.2, 0, 0],
                       color=cfg.MUTED, stroke_width=1.0, stroke_opacity=0.35)
        cross_v = Line([0, -2.2, 0], [0, 2.2, 0],
                       color=cfg.MUTED, stroke_width=1.0, stroke_opacity=0.35)
        rings.add(cross_h, cross_v)
        return rings.move_to(pos)

    # ── Layout: 2 × 2 grid of dartboards ────────────────────────────────────
    board_scale = 0.40
    positions = {
        "high_bias":     [-3.5,  1.45, 0],
        "high_variance": [ 3.5,  1.45, 0],
        "both_bad":      [-3.5, -1.55, 0],
        "ideal":         [ 3.5, -1.55, 0],
    }
    colors = {
        "high_bias":     cfg.ORANGE,
        "high_variance": cfg.PURPLE,
        "both_bad":      cfg.RED,
        "ideal":         cfg.GREEN,
    }
    titles = {
        "high_bias":     "High Bias\n(Underfitting)",
        "high_variance": "High Variance\n(Overfitting)",
        "both_bad":      "High Bias +\nHigh Variance",
        "ideal":         "Low Bias +\nLow Variance  ✓",
    }

    boards = {}
    for key, pos in positions.items():
        boards[key] = make_target(pos).scale(board_scale)

    board_labels = {}
    for key, pos in positions.items():
        tl = Text(titles[key], font_size=22,
                  color=colors[key], weight=BOLD)
        tl.set_stroke(cfg.BG, width=3, background=True)
        if key in ("high_bias", "high_variance"):
            tl.next_to(boards[key], UP, buff=0.16)
        else:
            tl.next_to(boards[key], DOWN, buff=0.16)
        if tl.width > 3.1:
            tl.scale_to_fit_width(3.1)
        board_labels[key] = tl

    # ── Phase 1: Show all dartboards ─────────────────────────────────────────
    cap_intro = bottom_caption("Think of predictions as dart throws at a target.", color=cfg.WHITE)

    paced_play(
        scene,
        LaggedStart(*[FadeIn(b) for b in boards.values()], lag_ratio=0.22),
        FadeIn(cap_intro, shift=UP * 0.1),
        run_time=1.5,
    )
    paced_play(
        scene,
        LaggedStart(*[FadeIn(bl) for bl in board_labels.values()], lag_ratio=0.22),
        run_time=1.2,
    )
    narration_wait(scene, 0.5)

    # ── Phase 2: Add darts to each board ────────────────────────────────────
    dot_groups = {}
    seed_map = {
        "high_bias": 101,
        "high_variance": 102,
        "both_bad": 103,
        "ideal": 104,
    }
    for key, pos in positions.items():
        shots = bias_variance_shots(scenario=key, n=10, seed=seed_map[key])
        scale = board_scale
        dots  = VGroup(*[
            Dot(
                point=[pos[0] + x * scale, pos[1] + y * scale, 0],
                radius=0.065,
                color=colors[key],
                fill_opacity=0.88,
            )
            for x, y in shots
        ])
        dot_groups[key] = dots

    cap_shots = bottom_caption("Every prediction lands somewhere…", color=cfg.WHITE)

    paced_play(
        scene,
        FadeOut(cap_intro),
        FadeIn(cap_shots, shift=UP * 0.1),
        run_time=0.5,
    )

    for key in ("high_bias", "high_variance", "both_bad", "ideal"):
        paced_play(
            scene,
            LaggedStart(*[GrowFromCenter(d) for d in dot_groups[key]], lag_ratio=0.08),
            run_time=0.9,
        )

    narration_wait(scene, 0.5)

    # ── Phase 3: Highlight the ideal quadrant ────────────────────────────────
    ideal_halo = Circle(
        radius=1.32 * board_scale, color=cfg.GREEN,
        stroke_width=5, stroke_opacity=0.0, fill_opacity=0.0,
    ).move_to(positions["ideal"])

    cap_ideal = bottom_caption("Statistics guides us toward the sweet spot.", color=cfg.GREEN)

    paced_play(
        scene,
        ideal_halo.animate.set_stroke(opacity=0.70),
        FadeOut(cap_shots),
        FadeIn(cap_ideal, shift=UP * 0.1),
        run_time=0.8,
    )
    paced_play(
        scene,
        Indicate(dot_groups["ideal"], color=cfg.GREEN, scale_factor=1.10),
        run_time=0.8,
    )
    narration_wait(scene, 0.5)

    # ── Phase 4: Equation card ───────────────────────────────────────────────
    eq_text = Text(
        "Expected Test Error  =  Bias²  +  Variance  +  Irreducible Noise",
        font_size=cfg.FONT["label"],
        color=cfg.WHITE,
        weight=BOLD,
    )
    eq_text.set_stroke(cfg.BG, width=5, background=True)
    eq_text.scale_to_fit_width(cfg.SAFE_WIDTH - 0.6)
    eq_text.to_edge(UP, buff=0.38)

    paced_play(
        scene,
        FadeOut(cap_ideal),
        Write(eq_text),
        run_time=1.2,
    )
    narration_wait(scene, 0.8)

    chart_axes = Axes(
        x_range=[0, 10, 5], y_range=[0, 6, 3],
        x_length=7.1, y_length=3.0,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.0, "include_tip": False},
        tips=False,
    ).move_to(DOWN * 0.70)
    y_label = label("error", font_size=cfg.FONT["tiny"], color=cfg.MUTED)
    y_label.rotate(PI / 2).next_to(chart_axes.y_axis, LEFT, buff=0.18)

    xs_curve = np.linspace(0.7, 9.3, 80)
    train_y = 4.7 * np.exp(-0.23 * xs_curve) + 0.55
    test_y = 0.13 * (xs_curve - 5.2) ** 2 + 1.15
    train_curve = VMobject().set_points_smoothly(
        [chart_axes.c2p(x, y) for x, y in zip(xs_curve, train_y)]
    ).set_stroke(cfg.CYAN, width=4.0, opacity=0.92)
    test_curve = VMobject().set_points_smoothly(
        [chart_axes.c2p(x, y) for x, y in zip(xs_curve, test_y)]
    ).set_stroke(cfg.GOLD, width=4.0, opacity=0.92)
    train_lbl = label("training error", font_size=20, color=cfg.CYAN)
    train_lbl.next_to(train_curve, RIGHT, buff=0.15)
    test_lbl = label("test error", font_size=20, color=cfg.GOLD)
    test_lbl.next_to(test_curve, RIGHT, buff=0.15)
    simple_lbl = label("too simple", font_size=20, color=cfg.ORANGE)
    simple_lbl.next_to(chart_axes.c2p(1.2, 0), DOWN, buff=0.36)
    balanced_lbl = label("balanced", font_size=20, color=cfg.GREEN)
    balanced_lbl.next_to(chart_axes.c2p(5.2, 0), DOWN, buff=0.36)
    complex_lbl = label("too complex", font_size=20, color=cfg.RED)
    complex_lbl.next_to(chart_axes.c2p(8.7, 0), DOWN, buff=0.36)

    solutions = VGroup()
    for txt, col in (("more data", cfg.GREEN), ("regularisation", cfg.GOLD), ("better features", cfg.CYAN)):
        chip = RoundedRectangle(
            corner_radius=0.10, width=1.85, height=0.42,
            fill_color=cfg.COLORS["panel"], fill_opacity=0.88,
            stroke_color=col, stroke_width=1.5,
        )
        chip_text = Text(txt, font_size=17, color=col, weight=BOLD)
        chip_text.set_stroke(cfg.BG, width=2, background=True)
        if chip_text.width > 1.62:
            chip_text.scale_to_fit_width(1.62)
        chip_text.move_to(chip.get_center())
        solutions.add(VGroup(chip, chip_text))
    solutions.arrange(RIGHT, buff=0.24).to_edge(DOWN, buff=0.36)

    board_scene = VGroup(
        *boards.values(),
        *board_labels.values(),
        *dot_groups.values(),
        ideal_halo,
    )
    paced_play(
        scene,
        FadeOut(board_scene),
        Create(chart_axes), FadeIn(y_label),
        run_time=1.0,
    )
    paced_play(
        scene,
        Create(train_curve), Create(test_curve),
        FadeIn(train_lbl), FadeIn(test_lbl),
        run_time=1.15,
    )
    paced_play(
        scene,
        LaggedStart(FadeIn(simple_lbl), FadeIn(balanced_lbl), FadeIn(complex_lbl), lag_ratio=0.15),
        LaggedStart(*[FadeIn(s, shift=UP * 0.08) for s in solutions], lag_ratio=0.14),
        run_time=1.1,
    )
    narration_wait(scene, 1.5)

    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["07"])
