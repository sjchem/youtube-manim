"""Scene 03 — Signal vs Noise.

A noisy scatter conceals an underlying trend.  Statistical smoothing
reveals the signal — and the residuals (noise) remain visible,
underscoring that noise never fully disappears, only becomes understood.

Narration cue: ~50 seconds
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene, bottom_caption, cinematic_background, end_scene,
    eq, glow_curve, label, narration_wait, paced_play,
    stat_axes,
)
from utils.math_utils import noisy_sine_data, moving_average


class Scene03SignalNoise(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background(show_bubbles=False))

    # ── Phase 1: Noisy scatter ───────────────────────────────────────────────
    axes, axis_labels = stat_axes(
        x_range=[-4, 4, 2], y_range=[-3, 3, 1],
        x_length=9.5, y_length=5.5,
        x_label="Observation", y_label="Value",
    )
    axes.move_to(ORIGIN + DOWN * 0.1)
    axis_labels[0].font_size = cfg.FONT["small"]
    axis_labels[1].font_size = cfg.FONT["small"]

    xs, ys_noisy, ys_true = noisy_sine_data(
        n=70, x_range=(-3.8, 3.8), amplitude=2.0, freq=0.80,
        noise_std=0.65, seed=17,
    )

    scatter_dots = VGroup(*[
        Dot(point=axes.c2p(x, y), radius=0.065, color=cfg.ORANGE, fill_opacity=0.72)
        for x, y in zip(xs, ys_noisy)
    ])

    cap_noisy = bottom_caption("What we observe: noisy, messy data.", color=cfg.ORANGE)

    paced_play(scene, Create(axes), FadeIn(*axis_labels), run_time=0.9)
    paced_play(
        scene,
        LaggedStart(*[FadeIn(d, scale=0.4) for d in scatter_dots], lag_ratio=0.03),
        run_time=2.0,
    )
    paced_play(scene, FadeIn(cap_noisy, shift=UP * 0.1), run_time=0.5)
    narration_wait(scene, 0.6)

    # ── Phase 2: Smoothed signal emerges ────────────────────────────────────
    x_smooth, y_smooth = moving_average(xs, ys_noisy, n_eval=100, bandwidth=0.7)

    smooth_pts = [axes.c2p(x, y) for x, y in zip(x_smooth, y_smooth)]
    smooth_path = VMobject()
    smooth_path.set_points_smoothly(smooth_pts)
    smooth_path.set_stroke(color=cfg.CYAN, width=5.5, opacity=0.92)

    smooth_glow = smooth_path.copy().set_stroke(cfg.CYAN, width=20, opacity=0.10)

    cap_signal = bottom_caption("Statistics extracts the signal…", color=cfg.CYAN)

    paced_play(
        scene,
        FadeOut(cap_noisy),
        FadeIn(cap_signal, shift=UP * 0.1),
        run_time=0.5,
    )
    paced_play(
        scene,
        FadeIn(smooth_glow),
        Create(smooth_path),
        run_time=2.2,
        rate_func=smooth,
    )
    narration_wait(scene, 0.5)

    # ── Phase 3: Residuals — show that noise remains ─────────────────────────
    # Interpolate smooth y at each observed x
    y_at_obs = np.interp(xs, x_smooth, y_smooth)
    residuals = VGroup()
    for x, y_obs, y_fit in zip(xs, ys_noisy, y_at_obs):
        if abs(y_obs - y_fit) > 0.08:
            p0 = axes.c2p(x, y_fit)
            p1 = axes.c2p(x, y_obs)
            residuals.add(Line(p0, p1, color=cfg.RED, stroke_width=2.2, stroke_opacity=0.55))

    cap_residual = bottom_caption("…and the residuals reveal the noise.", color=cfg.RED)

    paced_play(
        scene,
        LaggedStart(*[Create(r) for r in residuals], lag_ratio=0.03),
        FadeOut(cap_signal),
        FadeIn(cap_residual, shift=UP * 0.1),
        run_time=1.4,
    )

    residual_eq = eq(r"\text{residual} = y - \hat{y}",
                     color=cfg.RED, font_size=cfg.FONT["small"])
    residual_eq.to_corner(UR, buff=0.45).shift(DOWN * 0.28)
    paced_play(scene, Write(residual_eq), run_time=0.8)
    narration_wait(scene, 0.6)

    # ── Phase 4: Label the two components ───────────────────────────────────
    signal_tag = Text("SIGNAL", font_size=cfg.FONT["label"], color=cfg.CYAN, weight=BOLD)
    signal_tag.set_stroke(cfg.BG, width=4, background=True)
    signal_tag.move_to(axes.c2p(0.5, 2.5))

    noise_tag = Text("NOISE", font_size=cfg.FONT["label"], color=cfg.RED, weight=BOLD)
    noise_tag.set_stroke(cfg.BG, width=4, background=True)
    noise_tag.move_to(axes.c2p(2.5, -2.2))

    paced_play(
        scene,
        FadeIn(signal_tag, shift=DOWN * 0.12),
        FadeIn(noise_tag, shift=UP * 0.12),
        run_time=0.8,
    )
    narration_wait(scene, 0.5)

    # Equation: Data = Signal + Noise
    data_eq = eq(r"\text{Data} = \text{Signal} + \text{Noise}", color=cfg.WHITE,
                 font_size=cfg.FONT["section"])
    data_eq.set_stroke(cfg.BG, width=4, background=True)
    data_eq.to_edge(UP, buff=0.38)

    paced_play(
        scene,
        FadeOut(cap_residual),
        FadeOut(residual_eq),
        Write(data_eq),
        run_time=1.0,
    )
    narration_wait(scene, 1.2)

    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["03"])
