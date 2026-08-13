"""Scene 14: Fourier analysis reveals complex signals as rotating sine components."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    outlined_text,
    paced_play,
    section_tag,
)


def square_partial(x: float, terms: int) -> float:
    return float(sum(4 / PI * np.sin((2 * k + 1) * x) / (2 * k + 1) for k in range(terms)))


class Scene14Fourier(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "14")
    add_cinematic_background(scene)
    tag = section_tag("14", "Find the simple motions inside sound")
    paced_play(scene, FadeIn(tag, shift=RIGHT * 0.12), run_time=0.55)

    axes = Axes(
        x_range=[0, 4 * PI, PI],
        y_range=[-1.6, 1.6, 1],
        x_length=11.4,
        y_length=4.8,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.4},
    ).move_to(DOWN * 0.25)
    rich = axes.plot(
        lambda x: np.sin(x) + 0.5 * np.sin(2 * x) + 0.28 * np.sin(3 * x) + 0.16 * np.sin(5 * x),
        x_range=[0, 4 * PI],
        color=cfg.GOLD,
        stroke_width=7,
    )
    title = outlined_text("ONE COMPLEX SIGNAL", cfg.FONT["section"], cfg.GOLD, BOLD).to_edge(UP, buff=0.45)
    paced_play(scene, FadeOut(tag), Create(axes), FadeIn(title), run_time=1.4)
    paced_play(scene, Create(rich), run_time=4.0, rate_func=linear)
    question = outlined_text(
        "Which simple frequencies are hidden inside this shape?",
        cfg.FONT["label"],
        cfg.WHITE,
        BOLD,
    )
    if question.width > cfg.SAFE_WIDTH - 0.5:
        question.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    question.to_edge(DOWN, buff=0.28)
    paced_play(scene, FadeIn(question), run_time=0.7)
    narration_wait(scene, 1.5)

    paced_play(scene, FadeOut(VGroup(axes, rich, title, question)), run_time=0.9)

    component_axes = VGroup()
    curves = VGroup()
    component_labels = VGroup()
    specs = (
        (1, 1.0, cfg.CYAN),
        (2, 0.5, cfg.GREEN),
        (3, 0.28, cfg.PURPLE),
        (5, 0.16, cfg.ORANGE),
    )
    for index, (frequency, amplitude, color) in enumerate(specs):
        ax = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.2, 1.2, 1],
            x_length=10.2,
            y_length=1.15,
            tips=False,
            axis_config={"color": cfg.GRAY, "stroke_width": 1.5},
        ).move_to([1.0, 2.35 - index * 1.48, 0])
        curve = ax.plot(lambda x, f=frequency, a=amplitude: a * np.sin(f * x), x_range=[0, 4 * PI], color=color, stroke_width=4.5)
        label = eq(rf"{amplitude:g}\sin({frequency}\theta)", color, cfg.FONT["small"]).next_to(ax, LEFT, buff=0.25)
        component_axes.add(ax)
        curves.add(curve)
        component_labels.add(label)
    paced_play(scene, LaggedStart(*[Create(ax) for ax in component_axes], lag_ratio=0.18), run_time=1.6)
    for curve, label in zip(curves, component_labels, strict=True):
        paced_play(scene, Create(curve), FadeIn(label), run_time=2.2)
        narration_wait(scene, 0.55)
    sum_caption = outlined_text(
        "Fourier analysis asks: how much of each frequency is present?",
        cfg.FONT["label"],
        cfg.GOLD,
        BOLD,
    )
    if sum_caption.width > cfg.SAFE_WIDTH - 0.5:
        sum_caption.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    sum_caption.to_edge(DOWN, buff=0.28)
    paced_play(scene, FadeIn(sum_caption), run_time=0.8)
    narration_wait(scene, 1.6)

    # Recombine the separated ingredients before changing viewpoints.  This
    # directly mirrors the narration's "nothing was lost" moment.
    recombined_axes = Axes(
        x_range=[0, 4 * PI, PI],
        y_range=[-1.6, 1.6, 1],
        x_length=11.2,
        y_length=4.5,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.2},
    ).move_to(DOWN * 0.25)
    recombined_curve = recombined_axes.plot(
        lambda x: np.sin(x) + 0.5 * np.sin(2 * x) + 0.28 * np.sin(3 * x) + 0.16 * np.sin(5 * x),
        x_range=[0, 4 * PI],
        color=cfg.GOLD,
        stroke_width=7,
    )
    recombined_label = outlined_text(
        "ADD THE VALUES POINT BY POINT → THE ORIGINAL SIGNAL RETURNS",
        cfg.FONT["small"],
        cfg.GOLD,
        BOLD,
    )
    if recombined_label.width > cfg.SAFE_WIDTH - 0.5:
        recombined_label.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    recombined_label.to_edge(UP, buff=0.42)
    paced_play(
        scene,
        FadeOut(VGroup(component_axes, component_labels, sum_caption)),
        Create(recombined_axes),
        TransformFromCopy(curves, recombined_curve),
        FadeIn(recombined_label),
        run_time=1.4,
    )
    narration_wait(scene, 0.8)
    paced_play(scene, FadeOut(VGroup(curves, recombined_axes, recombined_curve, recombined_label)), run_time=0.9)

    # The frequency spectrum shows amplitudes as bars.
    spectrum_axes = Axes(
        x_range=[0, 7, 1],
        y_range=[0, 1.2, 0.25],
        x_length=10.5,
        y_length=5.2,
        tips=True,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.5},
    ).move_to(DOWN * 0.2)
    bars = VGroup()
    bar_labels = VGroup()
    for frequency, amplitude, color in specs:
        start = spectrum_axes.c2p(frequency, 0)
        end = spectrum_axes.c2p(frequency, amplitude)
        bars.add(Line(start, end, color=color, stroke_width=18))
        bar_labels.add(eq(str(frequency), color, cfg.FONT["label"]).next_to(start, DOWN, buff=0.15))
    amplitude_name = outlined_text("AMPLITUDE", cfg.FONT["small"], cfg.WHITE, BOLD).rotate(PI / 2)
    amplitude_name.next_to(spectrum_axes.y_axis, LEFT, buff=0.25)
    frequency_name = outlined_text("FREQUENCY", cfg.FONT["small"], cfg.WHITE, BOLD)
    frequency_name.next_to(spectrum_axes.x_axis, DOWN, buff=0.3)
    time_view = outlined_text("TIME VIEW", cfg.FONT["label"], cfg.CYAN, BOLD).move_to([-5.55, 3.45, 0])
    arrow = DoubleArrow(LEFT * 1.2, RIGHT * 1.2, color=cfg.GOLD, stroke_width=5).to_edge(UP, buff=0.55)
    freq_view = outlined_text("FREQUENCY VIEW", cfg.FONT["label"], cfg.GOLD, BOLD).move_to([5.35, 3.45, 0])
    phase_note = outlined_text("BAR HEIGHT = AMPLITUDE  ·  PHASE ALSO MATTERS", cfg.FONT["tiny"], cfg.WHITE, BOLD)
    phase_note.move_to([2.7, 2.82, 0])
    paced_play(scene, Create(spectrum_axes), FadeIn(amplitude_name), FadeIn(frequency_name), run_time=1.4)
    paced_play(scene, LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.28), FadeIn(bar_labels), run_time=2.2)
    paced_play(scene, FadeIn(time_view), GrowArrow(arrow), FadeIn(freq_view), FadeIn(phase_note), run_time=1.1)
    paced_play(scene, LaggedStart(*[Indicate(bar, color=cfg.WHITE, scale_factor=1.04) for bar in bars], lag_ratio=0.24), run_time=1.7)
    narration_wait(scene, 1.8)

    paced_play(scene, FadeOut(VGroup(spectrum_axes, bars, bar_labels, amplitude_name, frequency_name, time_view, arrow, freq_view, phase_note)), run_time=0.9)

    # Odd harmonics progressively build a square wave.
    square_axes = Axes(
        x_range=[-PI, 3 * PI, PI],
        y_range=[-1.5, 1.5, 1],
        x_length=12.4,
        y_length=4.8,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.3},
    ).move_to(DOWN * 0.25)
    target = square_axes.plot(lambda x: 1 if np.sin(x) >= 0 else -1, x_range=[-PI, 3 * PI, 0.02], color=cfg.GRAY, stroke_width=3, use_smoothing=False)
    target.set_stroke(opacity=0.55)
    paced_play(scene, Create(square_axes), Create(target), run_time=1.5)
    current = square_axes.plot(lambda x: square_partial(x, 1), x_range=[-PI, 3 * PI], color=cfg.CYAN, stroke_width=7)
    label = outlined_text("1 rotating component", cfg.FONT["label"], cfg.CYAN, BOLD).to_edge(UP, buff=0.45)
    paced_play(scene, Create(current), FadeIn(label), run_time=2.0)
    for terms in (2, 3, 5, 9):
        new_curve = square_axes.plot(lambda x, n=terms: square_partial(x, n), x_range=[-PI, 3 * PI, 0.025], color=cfg.CYAN, stroke_width=7)
        new_label = outlined_text(f"{terms} rotating components", cfg.FONT["label"], cfg.CYAN, BOLD).move_to(label)
        paced_play(scene, Transform(current, new_curve), ReplacementTransform(label, new_label), run_time=3.2, rate_func=smooth)
        label = new_label
        narration_wait(scene, 0.7)
    rotation_note = outlined_text("EACH HARMONIC = ONE ROTATING ARROW", cfg.FONT["label"], cfg.CYAN, BOLD).move_to(label)
    gibbs = VGroup(
        Arrow([4.7, 1.75, 0], [4.1, 1.15, 0], color=cfg.GOLD, stroke_width=4, buff=0.08),
        outlined_text("GIBBS RIPPLES", cfg.FONT["small"], cfg.GOLD, BOLD).move_to([5.5, 2.05, 0]),
    )
    applications = outlined_text(
        "SOUND  ·  COMMUNICATION  ·  IMAGING  ·  OPTICS  ·  VIBRATION",
        cfg.FONT["small"],
        cfg.WHITE,
        BOLD,
    ).to_edge(DOWN, buff=0.28)
    paced_play(
        scene,
        ReplacementTransform(label, rotation_note),
        FadeIn(gibbs),
        FadeIn(applications),
        Indicate(current, color=cfg.GOLD),
        run_time=1.2,
    )
    narration_wait(scene, 2.2)
    end_scene(scene, started, cfg.SCENE_DURATIONS["14"])
