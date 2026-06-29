"""Scene 05 — Patterns, Probability, and Prediction.

Machine learning is pattern recognition under uncertainty.
We see a scatter of data, fit a line (a model), wrap it in a
confidence band (the probability), and then predict.

Narration cue: ~78 seconds
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene, bottom_caption, cinematic_background, end_scene,
    eq, label, narration_wait, paced_play, stat_axes,
)
from utils.math_utils import linear_data, confidence_band


SLOPE     = 0.65
INTERCEPT = 0.15


class Scene05PatternsPrediction(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background(show_bubbles=False))

    axes, ax_labels = stat_axes(
        x_range=[-4.2, 4.2, 2], y_range=[-3.2, 3.2, 1],
        x_length=9.5, y_length=5.8,
        x_label="Feature  x", y_label="Outcome  y",
    )
    axes.move_to(ORIGIN + DOWN * 0.15)

    xs, ys = linear_data(n=18, slope=SLOPE, intercept=INTERCEPT,
                         x_range=(-3.8, 3.8), noise_std=0.50, seed=9)

    # ── Phase 1: Data scatter ────────────────────────────────────────────────
    scatter = VGroup(*[
        Dot(point=axes.c2p(x, y), radius=0.075, color=cfg.ORANGE, fill_opacity=0.85)
        for x, y in zip(xs, ys)
    ])

    cap_scatter = bottom_caption("Observations scattered — is there a pattern?", color=cfg.ORANGE)

    paced_play(scene, Create(axes), FadeIn(*ax_labels), run_time=0.9)
    paced_play(
        scene,
        LaggedStart(*[FadeIn(d, scale=0.5) for d in scatter], lag_ratio=0.07),
        FadeIn(cap_scatter, shift=UP * 0.1),
        run_time=1.8,
    )
    narration_wait(scene, 0.6)

    # ── Phase 2: Regression line — the learned pattern ───────────────────────
    x0, x1 = -3.9, 3.9
    line_start = axes.c2p(x0, SLOPE * x0 + INTERCEPT)
    line_end   = axes.c2p(x1, SLOPE * x1 + INTERCEPT)

    reg_line = Line(line_start, line_end, color=cfg.CYAN, stroke_width=5.5)
    reg_glow = reg_line.copy().set_stroke(cfg.CYAN, width=22, opacity=0.10)

    cap_line = bottom_caption("Statistics finds the underlying pattern.", color=cfg.CYAN)

    paced_play(
        scene,
        FadeIn(reg_glow),
        Create(reg_line),
        FadeOut(cap_scatter),
        FadeIn(cap_line, shift=UP * 0.1),
        run_time=1.3,
        rate_func=smooth,
    )
    narration_wait(scene, 0.5)

    prob_box = RoundedRectangle(
        corner_radius=0.12, width=6.25, height=1.85,
        fill_color=cfg.COLORS["panel"], fill_opacity=0.96,
        stroke_color=cfg.GOLD, stroke_width=2.2,
    )
    prob_eq = eq(r"P(Y \mid X)", color=cfg.GOLD, font_size=cfg.FONT["small"])
    pred_modes = VGroup(
        Text("Regression: predict a number", font_size=22, color=cfg.CYAN),
        Text("Classification: predict a probability", font_size=22, color=cfg.PURPLE),
    ).arrange(DOWN, buff=0.08)
    for mob in pred_modes:
        mob.set_stroke(cfg.BG, width=3, background=True)
    risk_chips = VGroup()
    for txt, col in (("10% risk", cfg.GREEN), ("55% risk", cfg.GOLD), ("92% risk", cfg.RED)):
        chip = RoundedRectangle(
            corner_radius=0.10, width=1.55, height=0.38,
            fill_color=cfg.COLORS["panel2"], fill_opacity=0.95,
            stroke_color=col, stroke_width=1.6,
        )
        chip_text = Text(txt, font_size=17, color=col, weight=BOLD)
        chip_text.set_stroke(cfg.BG, width=2, background=True)
        chip_text.move_to(chip.get_center())
        risk_chips.add(VGroup(chip, chip_text))
    risk_chips.arrange(RIGHT, buff=0.20)
    prob_content = VGroup(prob_eq, pred_modes, risk_chips).arrange(DOWN, buff=0.13)
    prob_panel = VGroup(prob_box, prob_content).move_to(UP * 2.15)
    prob_content.move_to(prob_box.get_center())
    paced_play(scene, FadeIn(prob_panel, shift=DOWN * 0.12), run_time=0.9)
    narration_wait(scene, 2.2)

    # ── Phase 3: Confidence band ─────────────────────────────────────────────
    xs_eval = np.linspace(x0, x1, 80)
    y_lo, y_hi = confidence_band(xs_eval, SLOPE, INTERCEPT, noise_std=0.50, n_obs=18)

    lo_pts = [axes.c2p(x, y) for x, y in zip(xs_eval, y_lo)]
    hi_pts = [axes.c2p(x, y) for x, y in zip(xs_eval, y_hi)]

    band = Polygon(*lo_pts, *hi_pts[::-1],
                   fill_color=cfg.CYAN, fill_opacity=0.14, stroke_width=0)

    lo_line = VMobject().set_points_smoothly(lo_pts).set_stroke(cfg.CYAN, 2.2, 0.45)
    hi_line = VMobject().set_points_smoothly(hi_pts).set_stroke(cfg.CYAN, 2.2, 0.45)

    ci_lbl = label("confidence interval\naverage trend",
                   font_size=cfg.FONT["tiny"], color=cfg.CYAN)
    ci_lbl.next_to(hi_line, UP, buff=0.12).shift(LEFT * 2.2)

    cap_band = bottom_caption("Uncertainty captured — the confidence band.", color=cfg.GOLD)

    paced_play(
        scene,
        FadeIn(band), Create(lo_line), Create(hi_line), FadeIn(ci_lbl),
        FadeOut(prob_panel),
        FadeOut(cap_line), FadeIn(cap_band, shift=UP * 0.1),
        run_time=1.1,
    )
    narration_wait(scene, 0.5)

    # ── Phase 4: New point + prediction ────────────────────────────────────
    x_new   = 2.8
    y_pred  = SLOPE * x_new + INTERCEPT

    y_fit_eval = SLOPE * xs_eval + INTERCEPT
    pred_margin = 1.35 * 0.50
    pred_lo = y_fit_eval - pred_margin
    pred_hi = y_fit_eval + pred_margin
    pred_lo_pts = [axes.c2p(x, y) for x, y in zip(xs_eval, pred_lo)]
    pred_hi_pts = [axes.c2p(x, y) for x, y in zip(xs_eval, pred_hi)]
    pred_band = Polygon(*pred_lo_pts, *pred_hi_pts[::-1],
                        fill_color=cfg.PURPLE, fill_opacity=0.08, stroke_width=0)
    pred_lo_line = VMobject().set_points_smoothly(pred_lo_pts).set_stroke(cfg.PURPLE, 2.0, 0.40)
    pred_hi_line = VMobject().set_points_smoothly(pred_hi_pts).set_stroke(cfg.PURPLE, 2.0, 0.40)
    pi_lbl = label("prediction interval\nsingle new case",
                   font_size=cfg.FONT["tiny"], color=cfg.PURPLE)
    pi_lbl.next_to(pred_hi_line, UP, buff=0.10).shift(RIGHT * 1.85)

    new_dot = Dot(point=axes.c2p(x_new, -2.9), radius=0.10, color=cfg.PURPLE, fill_opacity=0.0)
    scene.add(new_dot)

    cap_predict = bottom_caption("A new input arrives — where does it land?", color=cfg.PURPLE)

    paced_play(
        scene,
        FadeIn(pred_band), Create(pred_lo_line), Create(pred_hi_line), FadeIn(pi_lbl),
        new_dot.animate.set_fill(opacity=1.0).move_to(axes.c2p(x_new, -2.9)),
        FadeOut(cap_band), FadeIn(cap_predict, shift=UP * 0.1),
        run_time=1.1,
    )

    pred_dot = Dot(point=axes.c2p(x_new, y_pred), radius=0.10,
                   color=cfg.GREEN, fill_opacity=0.0)
    pred_v_line = DashedLine(
        axes.c2p(x_new, -3.2), axes.c2p(x_new, y_pred),
        color=cfg.PURPLE, stroke_width=3, stroke_opacity=0.65, dash_length=0.12,
    )
    pred_h_line = DashedLine(
        axes.c2p(-4.2, y_pred), axes.c2p(x_new, y_pred),
        color=cfg.GREEN, stroke_width=3, stroke_opacity=0.65, dash_length=0.12,
    )

    pred_lbl = eq(r"\hat{y}", color=cfg.GREEN, font_size=cfg.FONT["section"])
    pred_lbl.set_stroke(cfg.BG, width=3, background=True)
    pred_lbl.next_to(pred_dot, LEFT, buff=0.20)

    paced_play(
        scene,
        Create(pred_v_line), Create(pred_h_line),
        run_time=0.9,
    )
    paced_play(
        scene,
        pred_dot.animate.set_fill(opacity=1.0),
        FadeIn(pred_lbl),
        run_time=0.7,
    )
    narration_wait(scene, 1.2)

    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["05"])
