"""Scene 07: a cup of coffee solves a differential equation on your desk."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    calc_axes,
    compact_axis_labels,
    end_scene,
    eq,
    fitted_eq,
    glow_dot,
    glow_line,
    live_readout,
    mug,
    narration_wait,
    outlined_text,
    paced_play,
)
from utils.physics_models import CoolingCup
from utils.render_helpers import temperature_to_color

CUP = CoolingCup(start=90.0, room=20.0, rate=0.05)
WATCH_MINUTES = 40.0
TUBE_HEIGHT = 3.1
TUBE_BOTTOM = -2.35


def _tube(x: float, label: str, label_color: str) -> VGroup:
    """An empty thermometer body; its column is drawn separately by a tracker."""
    tube = RoundedRectangle(width=0.46, height=TUBE_HEIGHT, corner_radius=0.23, color=cfg.MUTED, fill_color=cfg.PANEL, fill_opacity=0.92, stroke_width=3)
    tube.move_to([x, TUBE_BOTTOM + TUBE_HEIGHT / 2, 0])
    bulb = Circle(radius=0.33, color=cfg.MUTED, fill_color=cfg.PANEL_2, fill_opacity=1, stroke_width=3).move_to([x, TUBE_BOTTOM, 0])
    caption = outlined_text(label, cfg.FONT["small"], label_color).next_to(bulb, DOWN, buff=0.28)
    return VGroup(tube, bulb, caption)


def _column(x: float, temperature: float, ceiling: float = 100.0) -> VGroup:
    """The mercury column plus bulb fill, coloured by how hot the body is."""
    colour = temperature_to_color(temperature)
    height = max(TUBE_HEIGHT * 0.94 * float(np.clip(temperature / ceiling, 0.0, 1.0)), 0.05)
    bar = Rectangle(width=0.24, height=height, color=colour, fill_color=colour, fill_opacity=1, stroke_width=0)
    bar.move_to([x, TUBE_BOTTOM + height / 2, 0])
    bulb = Circle(radius=0.27, color=colour, fill_color=colour, fill_opacity=1, stroke_width=0).move_to([x, TUBE_BOTTOM, 0])
    return VGroup(bulb, bar)


class Scene07NewtonCooling(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "07")
    add_cinematic_background(scene)

    # -- Beat 1: the mug, the room, and the two numbers that matter -----------
    cup = mug(temperature_to_color(CUP.start), 1.5).move_to([-6.15, -0.55, 0])
    steam = VGroup(
        *(
            ArcBetweenPoints(np.array([-6.35 + 0.35 * i, 0.55, 0]), np.array([-6.15 + 0.35 * i, 1.75, 0]), angle=(-1) ** i * 1.1, color=cfg.CYAN, stroke_width=4)
            .set_stroke(opacity=0.45)
            for i in range(3)
        )
    )
    hot_tag = eq(r"90^\circ\text{C}", cfg.ORANGE, cfg.FONT["section"]).next_to(cup, DOWN, buff=0.40)
    room_tag = eq(r"20^\circ\text{C}", cfg.CYAN, cfg.FONT["section"]).move_to([-6.15, 2.45, 0])
    room_word = outlined_text("the room", cfg.FONT["small"], cfg.MUTED).next_to(room_tag, DOWN, buff=0.22)

    paced_play(scene, FadeIn(cup, shift=UP * 0.15), FadeIn(hot_tag), run_time=1.0)
    paced_play(scene, LaggedStart(*(Create(s) for s in steam), lag_ratio=0.25), run_time=1.2)
    paced_play(scene, FadeIn(room_tag), FadeIn(room_word), run_time=0.8)
    narration_wait(scene, 9.0)

    # -- Beat 2: the gap is the whole story ------------------------------------
    clock = ValueTracker(0.0)
    coffee_tube = _tube(-3.95, "COFFEE", cfg.ORANGE)
    room_tube = _tube(-1.65, "ROOM", cfg.CYAN)
    coffee_column = always_redraw(lambda: _column(-3.95, CUP.temperature(clock.get_value())))
    room_column = always_redraw(lambda: _column(-1.65, CUP.room))
    paced_play(scene, FadeIn(coffee_tube), FadeIn(room_tube), run_time=0.9)
    scene.add(coffee_column, room_column)
    narration_wait(scene, 6.4)

    equation = fitted_eq(r"\frac{dT}{dt}=-k\,(T-T_{\text{room}})", cfg.WHITE, cfg.FONT["section"], width=6.6)
    equation.move_to([3.35, 2.80, 0])
    gap_note = outlined_text("driven by the gap", cfg.FONT["small"], cfg.GOLD).next_to(equation, DOWN, buff=0.32)
    paced_play(scene, Write(equation), run_time=1.6)
    paced_play(scene, FadeIn(gap_note), run_time=0.7)
    narration_wait(scene, 10.2)

    # -- Beat 3: watch it cool, fast then slow ----------------------------------
    axes = calc_axes((0, WATCH_MINUTES, 10), (0, 100, 20), 7.2, 3.9).move_to([3.35, -1.05, 0])
    axis_labels = compact_axis_labels(axes, r"t\,(\text{minutes})", r"T\,(^\circ\text{C})", cfg.MUTED, cfg.FONT["small"])
    room_line = Line(axes.c2p(0, CUP.room), axes.c2p(WATCH_MINUTES, CUP.room), color=cfg.CYAN, stroke_width=4)
    room_line_tag = eq(r"T_{\text{room}}", cfg.CYAN, cfg.FONT["small"]).next_to(axes.c2p(WATCH_MINUTES * 0.86, CUP.room), UP, buff=0.16)
    paced_play(scene, Create(axes), FadeIn(axis_labels), run_time=1.0)
    paced_play(scene, Create(room_line), FadeIn(room_line_tag), run_time=0.9)

    drawn = always_redraw(
        lambda: axes.plot(CUP.temperature, x_range=[0, max(clock.get_value(), 0.05)], color=cfg.ORANGE, stroke_width=6)
    )
    head = always_redraw(lambda: glow_dot(axes.c2p(clock.get_value(), CUP.temperature(clock.get_value())), cfg.GOLD, 0.09))
    gap_bar = always_redraw(
        lambda: glow_line(
            axes.c2p(clock.get_value(), CUP.room),
            axes.c2p(clock.get_value(), CUP.temperature(clock.get_value())),
            cfg.GOLD,
            6,
        )
    )
    readout = live_readout(
        r"T-T_{\text{room}}=",
        lambda: CUP.gap(clock.get_value()),
        cfg.GOLD,
        cfg.FONT["small"],
        decimal_places=0,
        suffix=r"^\circ",
    ).move_to([-3.30, 1.95, 0])
    scene.add(drawn, head, gap_bar, readout)
    paced_play(scene, clock.animate.set_value(WATCH_MINUTES), run_time=11.0, rate_func=linear)
    narration_wait(scene, 9.6)

    # -- Beat 4: two tangents make the point ------------------------------------
    early, late = 2.0, 30.0
    tangents = VGroup()
    tags = VGroup()
    for moment, colour, word in ((early, cfg.RED, "steep"), (late, cfg.GREEN, "gentle")):
        slope = CUP.slope(moment)
        unit_x = axes.x_axis.get_unit_size()
        unit_y = axes.y_axis.get_unit_size()
        direction = np.array([unit_x, slope * unit_y, 0.0])
        direction /= np.linalg.norm(direction)
        centre = axes.c2p(moment, CUP.temperature(moment))
        tangents.add(glow_line(centre - direction * 1.25, centre + direction * 1.25, colour, 6))
        tags.add(outlined_text(word, cfg.FONT["small"], colour).move_to(centre + UP * 0.62 + RIGHT * 0.55))
    paced_play(scene, Create(tangents[0]), FadeIn(tags[0]), run_time=1.0)
    narration_wait(scene, 6.2)
    paced_play(scene, Create(tangents[1]), FadeIn(tags[1]), run_time=1.0)
    narration_wait(scene, 6.4)

    solution = fitted_eq(r"T(t)=T_{\text{room}}+(T_0-T_{\text{room}})e^{-kt}", cfg.GREEN, cfg.FONT["body"], width=8.4)
    solution.to_edge(DOWN, buff=0.30)
    paced_play(scene, FadeIn(solution, shift=UP * 0.12), run_time=1.1)
    narration_wait(scene, 7.4)

    paced_play(scene, FadeOut(solution), run_time=0.5)
    verdict = bottom_caption("Big gap, fast cooling. Small gap, slow cooling.", cfg.GOLD)
    paced_play(scene, FadeIn(verdict), run_time=0.9)
    narration_wait(scene, 6.2)

    end_scene(scene, started, cfg.SCENE_DURATIONS["07"])
