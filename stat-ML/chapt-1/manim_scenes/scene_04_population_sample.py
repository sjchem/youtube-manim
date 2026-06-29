"""Scene 04 — Population vs Sample.

We can never observe everything.  Statistics lets us draw trustworthy
conclusions from a small slice (sample) of a much larger whole
(population), and quantifies exactly how confident we should be.

Narration cue: ~67 seconds
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene, bottom_caption, cinematic_background, end_scene,
    eq, label, narration_wait, paced_play,
)
from utils.math_utils import population_dots


class Scene04PopulationSample(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background(show_bubbles=False))

    rng = np.random.default_rng(55)
    pts = population_dots(n=200, spread=(3.5, 2.2), seed=55)
    # Clip to frame
    pts = pts[(np.abs(pts[:, 0]) < 6.5) & (np.abs(pts[:, 1]) < 3.4)]

    # ── Phase 1: Full population of dots ────────────────────────────────────
    pop_dots = VGroup(*[
        Dot(point=[x, y, 0], radius=0.050, color=cfg.MUTED, fill_opacity=0.50)
        for x, y in pts
    ])

    pop_label = Text("POPULATION", font_size=cfg.FONT["title"], color=cfg.WHITE, weight=BOLD)
    pop_label.set_stroke(cfg.BG, width=6, background=True)
    pop_label.to_edge(UP, buff=0.42)

    pop_count = Text(f"N  =  {len(pts)}  individuals",
                     font_size=cfg.FONT["body"], color=cfg.MUTED)
    pop_count.set_stroke(cfg.BG, width=4, background=True)
    pop_count.next_to(pop_label, DOWN, buff=0.22)

    cap_pop = bottom_caption("The full population — too large to measure entirely.", color=cfg.WHITE)

    paced_play(
        scene,
        FadeIn(pop_label, shift=DOWN * 0.1),
        FadeIn(pop_count, shift=DOWN * 0.1),
        run_time=0.8,
    )
    paced_play(
        scene,
        LaggedStart(*[FadeIn(d, scale=0.3) for d in pop_dots], lag_ratio=0.02),
        FadeIn(cap_pop, shift=UP * 0.1),
        run_time=2.5,
    )
    narration_wait(scene, 0.6)

    # ── Phase 2: Sample — highlight a random subset ──────────────────────────
    n_sample = 25
    sample_idx = rng.choice(len(pts), size=n_sample, replace=False)

    sample_dots = VGroup(*[
        Dot(point=[pts[i, 0], pts[i, 1], 0],
            radius=0.088, color=cfg.CYAN, fill_opacity=0.92)
        for i in sample_idx
    ])

    sample_label = Text("SAMPLE", font_size=cfg.FONT["title"], color=cfg.CYAN, weight=BOLD)
    sample_label.set_stroke(cfg.BG, width=6, background=True)
    sample_label.to_edge(UP, buff=0.42)

    sample_count = Text(f"n  =  {n_sample}  observations",
                        font_size=cfg.FONT["body"], color=cfg.CYAN)
    sample_count.set_stroke(cfg.BG, width=4, background=True)
    sample_count.next_to(sample_label, DOWN, buff=0.22)

    cap_sample = bottom_caption("We measure a sample — and estimate the rest.", color=cfg.CYAN)

    paced_play(
        scene,
        pop_dots.animate.set_fill(opacity=0.18),
        Transform(pop_label, sample_label),
        Transform(pop_count, sample_count),
        FadeOut(cap_pop),
        FadeIn(cap_sample, shift=UP * 0.1),
        run_time=0.85,
    )
    paced_play(
        scene,
        LaggedStart(*[FadeIn(d, scale=0.6) for d in sample_dots], lag_ratio=0.08),
        run_time=1.5,
    )
    narration_wait(scene, 0.5)

    rep_box = RoundedRectangle(
        corner_radius=0.12, width=4.9, height=1.55,
        fill_color=cfg.COLORS["panel"], fill_opacity=0.86,
        stroke_color=cfg.ORANGE, stroke_width=2.0,
    )
    rep_title = Text("Representative sample", font_size=cfg.FONT["tiny"],
                     color=cfg.ORANGE, weight=BOLD)
    rep_title.set_stroke(cfg.BG, width=3, background=True)
    rep_lines = VGroup(
        Text("reflects the population", font_size=20, color=cfg.WHITE),
        Text("large data can still be biased", font_size=20, color=cfg.RED),
    ).arrange(DOWN, buff=0.05)
    for mob in rep_lines:
        mob.set_stroke(cfg.BG, width=2, background=True)
        mob.scale_to_fit_width(4.3)
    rep_content = VGroup(rep_title, rep_lines).arrange(DOWN, buff=0.14)
    rep_panel = VGroup(rep_box, rep_content).to_corner(DR, buff=0.50).shift(UP * 1.08)
    rep_content.move_to(rep_box.get_center())

    paced_play(scene, FadeIn(rep_panel, shift=LEFT * 0.12), run_time=0.8)
    narration_wait(scene, 0.9)

    # ── Phase 3: Population mean μ vs sample mean x̄ ────────────────────────
    true_mean_x = float(pts[:, 0].mean())
    samp_mean_x = float(pts[sample_idx, 0].mean())

    # Vertical mean lines
    pop_mean_line = DashedLine(
        [true_mean_x, -3.5, 0], [true_mean_x, 3.5, 0],
        color=cfg.GREEN, stroke_width=3.5, stroke_opacity=0.70, dash_length=0.14,
    )
    samp_mean_line = DashedLine(
        [samp_mean_x, -3.5, 0], [samp_mean_x, 3.5, 0],
        color=cfg.GOLD, stroke_width=3.5, stroke_opacity=0.70, dash_length=0.14,
    )

    mu_label = eq(r"\mu", color=cfg.GREEN, font_size=cfg.FONT["section"])
    mu_label.next_to(pop_mean_line, UP, buff=0.18)
    mu_label.set_stroke(cfg.BG, width=3, background=True)

    xbar_label = eq(r"\bar{x}", color=cfg.GOLD, font_size=cfg.FONT["section"])
    xbar_label.next_to(samp_mean_line, UP, buff=0.18)
    xbar_label.set_stroke(cfg.BG, width=3, background=True)

    cap_mean = bottom_caption(r"x̄  ≈  μ  (with uncertainty)", color=cfg.GOLD)

    paced_play(
        scene,
        Create(pop_mean_line), FadeIn(mu_label),
        FadeOut(cap_sample),
        FadeOut(rep_panel),
        run_time=0.9,
    )
    paced_play(
        scene,
        Create(samp_mean_line), FadeIn(xbar_label),
        FadeIn(cap_mean, shift=UP * 0.1),
        run_time=0.9,
    )

    repeat_means = []
    for _ in range(3):
        idx = rng.choice(len(pts), size=n_sample, replace=False)
        repeat_means.append(float(pts[idx, 0].mean()))
    repeat_lines = VGroup(*[
        DashedLine(
            [xm, -3.05, 0], [xm, 3.05, 0],
            color=cfg.GOLD, stroke_width=2.0, stroke_opacity=0.32,
            dash_length=0.12,
        )
        for xm in repeat_means
    ])
    repeat_lbl = label("other samples shift x-bar", font_size=cfg.FONT["tiny"], color=cfg.GOLD)
    repeat_lbl.to_corner(DL, buff=0.55).shift(UP * 0.45)
    paced_play(
        scene,
        LaggedStart(*[Create(line) for line in repeat_lines], lag_ratio=0.20),
        FadeIn(repeat_lbl, shift=RIGHT * 0.08),
        run_time=0.9,
    )
    narration_wait(scene, 0.6)

    # ── Phase 4: Confidence interval bracket ────────────────────────────────
    se    = 1.0 / np.sqrt(n_sample)  # schematic SE
    lo    = samp_mean_x - 1.5 * se * 3.0   # scale for visibility
    hi    = samp_mean_x + 1.5 * se * 3.0

    ci_line = Line([lo, -0.15, 0], [hi, -0.15, 0],
                   color=cfg.GOLD, stroke_width=5, stroke_opacity=0.85)
    ci_lo   = Line([lo, -0.35, 0], [lo,  0.05, 0],
                   color=cfg.GOLD, stroke_width=4, stroke_opacity=0.85)
    ci_hi   = Line([hi, -0.35, 0], [hi,  0.05, 0],
                   color=cfg.GOLD, stroke_width=4, stroke_opacity=0.85)
    ci_grp  = VGroup(ci_line, ci_lo, ci_hi)

    ci_lbl = Text("95% CI", font_size=cfg.FONT["label"], color=cfg.GOLD, weight=BOLD)
    ci_lbl.set_stroke(cfg.BG, width=3, background=True)
    ci_lbl.next_to(ci_line, DOWN, buff=0.18)

    paced_play(
        scene,
        Create(ci_grp), FadeIn(ci_lbl),
        FadeOut(repeat_lbl),
        run_time=0.85,
    )

    eval_box = RoundedRectangle(
        corner_radius=0.12, width=4.15, height=0.92,
        fill_color=cfg.COLORS["panel"], fill_opacity=0.82,
        stroke_color=cfg.PURPLE, stroke_width=2.2, stroke_opacity=0.70,
    )
    eval_text = VGroup(
        Text("ML test set", font_size=cfg.FONT["tiny"], color=cfg.PURPLE, weight=BOLD),
        Text("sample of future cases", font_size=cfg.FONT["tiny"], color=cfg.WHITE),
    ).arrange(DOWN, buff=0.05)
    eval_note = VGroup(eval_box, eval_text).to_corner(DR, buff=0.55).shift(UP * 0.55)
    eval_text.move_to(eval_box.get_center())
    paced_play(scene, FadeIn(eval_note, shift=LEFT * 0.12), run_time=0.75)
    narration_wait(scene, 1.2)

    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["04"])
