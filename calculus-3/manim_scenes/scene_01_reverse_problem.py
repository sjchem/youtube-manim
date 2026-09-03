"""Scene 01: only the speedometer is visible — can the journey be rebuilt?"""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    area_region,
    begin_scene,
    bottom_caption,
    chip,
    end_scene,
    eq,
    fitted_eq,
    glow_dot,
    live_readout,
    narration_wait,
    labelled_axes,
    outlined_text,
    paced_play,
    speedometer,
    stacked_axes,
    title_card,
)
from utils.physics_models import AcceleratingCar

CAR = AcceleratingCar(rate=2.0)


def _rear_car(scale: float = 1.0) -> VGroup:
    """A rear-facing car whose silhouette agrees with the road perspective."""
    shadow = Ellipse(
        width=2.05,
        height=0.30,
        fill_color=BLACK,
        fill_opacity=0.40,
        stroke_width=0,
    ).shift(DOWN * 0.43)
    wheels = VGroup(
        RoundedRectangle(width=0.28, height=0.58, corner_radius=0.09, color=cfg.GRAY, fill_color="#020A10", fill_opacity=1, stroke_width=2).move_to([-0.72, -0.22, 0]),
        RoundedRectangle(width=0.28, height=0.58, corner_radius=0.09, color=cfg.GRAY, fill_color="#020A10", fill_opacity=1, stroke_width=2).move_to([0.72, -0.22, 0]),
    )
    body = Polygon(
        [-0.88, -0.34, 0],
        [-0.78, 0.28, 0],
        [-0.48, 0.68, 0],
        [0.48, 0.68, 0],
        [0.78, 0.28, 0],
        [0.88, -0.34, 0],
        color=cfg.CYAN,
        fill_color=cfg.CYAN,
        fill_opacity=0.86,
        stroke_width=2.5,
    )
    rear_window = Polygon(
        [-0.47, 0.27, 0],
        [-0.31, 0.57, 0],
        [0.31, 0.57, 0],
        [0.47, 0.27, 0],
        color=cfg.BLUE,
        fill_color=cfg.PANEL_2,
        fill_opacity=0.96,
        stroke_width=2,
    )
    bumper = RoundedRectangle(
        width=1.45,
        height=0.12,
        corner_radius=0.05,
        color=cfg.GRAY,
        fill_color=cfg.GRAY,
        fill_opacity=0.72,
        stroke_width=1.5,
    ).move_to([0, -0.27, 0])
    tail_lights = VGroup(
        RoundedRectangle(width=0.27, height=0.14, corner_radius=0.04, color=cfg.RED, fill_color=cfg.RED, fill_opacity=1, stroke_width=1).move_to([-0.57, -0.04, 0]),
        RoundedRectangle(width=0.27, height=0.14, corner_radius=0.04, color=cfg.RED, fill_color=cfg.RED, fill_opacity=1, stroke_width=1).move_to([0.57, -0.04, 0]),
    )
    plate = RoundedRectangle(
        width=0.34,
        height=0.15,
        corner_radius=0.025,
        color=cfg.WHITE,
        fill_color=cfg.WHITE,
        fill_opacity=0.78,
        stroke_width=1,
    ).move_to([0, -0.05, 0])
    return VGroup(shadow, wheels, body, rear_window, bumper, tail_lights, plate).scale(scale)


def _night_road() -> VGroup:
    """A receding road under a dark horizon, built once for the cold open."""
    horizon = 0.95
    ground = Rectangle(width=17.0, height=5.6, fill_color="#03121F", fill_opacity=1, stroke_width=0)
    ground.move_to([0, horizon - 2.8, 0])
    road = Polygon(
        [-7.4, -3.55, 0],
        [7.4, -3.55, 0],
        [0.72, horizon, 0],
        [-0.72, horizon, 0],
        fill_color="#08161F",
        fill_opacity=1,
        stroke_width=0,
    )
    left_edge = Line([-7.4, -3.55, 0], [-0.72, horizon, 0], color=cfg.BLUE, stroke_width=5, stroke_opacity=0.75)
    right_edge = Line([7.4, -3.55, 0], [0.72, horizon, 0], color=cfg.BLUE, stroke_width=5, stroke_opacity=0.75)
    marks = VGroup()
    for y0, y1, half, opacity in ((-3.10, -2.25, 0.26, 0.92), (-1.75, -1.10, 0.15, 0.78), (-0.70, -0.25, 0.085, 0.62), (0.10, 0.42, 0.045, 0.46)):
        marks.add(
            Polygon([-half, y0, 0], [half, y0, 0], [half * 0.65, y1, 0], [-half * 0.65, y1, 0], fill_color=cfg.GOLD, fill_opacity=opacity, stroke_width=0)
        )
    glow = Circle(radius=1.5, color=cfg.CYAN, stroke_width=0, fill_color=cfg.CYAN, fill_opacity=0.05).move_to([0, horizon, 0])
    skyline = VGroup()
    for x, width, height in ((-4.6, 0.8, 0.68), (-3.7, 0.55, 1.0), (3.4, 0.7, 0.85), (4.3, 0.5, 0.6)):
        skyline.add(Rectangle(width=width, height=height, fill_color=cfg.PANEL_2, fill_opacity=0.8, stroke_width=0).move_to([x, horizon + height / 2, 0]))
    return VGroup(ground, glow, skyline, road, marks, left_edge, right_edge)


class Scene01ReverseProblem(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "01")
    add_cinematic_background(scene)

    # -- Beat 1: a car disappears down a road, leaving only its speedometer --
    road = _night_road()
    car = _rear_car(1.15).move_to([0, -2.50, 0])
    paced_play(scene, FadeIn(road), FadeIn(car, shift=DOWN * 0.2), run_time=1.1)
    paced_play(
        scene,
        car.animate.move_to([0, 0.76, 0]).scale(0.14),
        run_time=3.6,
        rate_func=rate_functions.ease_in_cubic,
    )

    dial, needle = speedometer(1.10, cfg.CYAN)
    dial.move_to([0, -1.38, 0])
    dial_label = outlined_text("ALL YOU CAN SEE", cfg.FONT["small"], cfg.MUTED).next_to(dial, DOWN, buff=0.32)
    paced_play(scene, FadeIn(dial, scale=1.1), FadeIn(dial_label), run_time=0.9)
    paced_play(scene, Rotate(needle, angle=-0.72 * PI, about_point=dial.get_center()), run_time=3.0, rate_func=rate_functions.ease_in_out_sine)

    question = outlined_text("WHERE HAS IT BEEN?", cfg.FONT["title"], cfg.GOLD).to_edge(UP, buff=0.5)
    paced_play(scene, FadeIn(question, shift=DOWN * 0.2), run_time=0.9)
    narration_wait(scene, 3.0)
    paced_play(scene, FadeOut(VGroup(road, car, dial, dial_label, question)), run_time=0.7)

    # -- Beat 2: the rate we are given ---------------------------------------
    top_axes, bottom_axes = stacked_axes((0, 4, 1), (0, 9, 3), (0, 17, 4), x_length=9.4, y_length=2.35)
    # These symbols carry the graph's meaning, so keep them large enough to
    # survive a 16:9 video being reduced to a phone screen.
    top_labels = labelled_axes(top_axes, "t", "v", cfg.CYAN, cfg.FONT["hero"])
    bottom_labels = labelled_axes(bottom_axes, "t", "s", cfg.GOLD, cfg.FONT["hero"])
    velocity = top_axes.plot(CAR.velocity, x_range=[0, 4], color=cfg.CYAN, stroke_width=6)
    rate_tag = eq("v(t)=2t", cfg.CYAN, cfg.FONT["body"])
    known = outlined_text("KNOWN", cfg.FONT["tiny"], cfg.CYAN)
    top_header = VGroup(known, rate_tag).arrange(RIGHT, buff=0.28)
    top_header.next_to(top_axes, UP, buff=0.14).align_to(top_axes, LEFT).shift(RIGHT * 0.55)
    paced_play(scene, Create(top_axes), FadeIn(top_labels), run_time=1.0)
    paced_play(scene, Create(velocity), FadeIn(top_header), run_time=1.3)
    narration_wait(scene, 2.5)

    unknown_tag = eq(r"s(t)=\;?", cfg.GOLD, cfg.FONT["body"])
    unknown = outlined_text("UNKNOWN", cfg.FONT["tiny"], cfg.GOLD)
    bottom_header = VGroup(unknown, unknown_tag).arrange(RIGHT, buff=0.28)
    bottom_header.next_to(bottom_axes, UP, buff=0.14).align_to(bottom_axes, LEFT).shift(RIGHT * 0.55)
    paced_play(scene, Create(bottom_axes), FadeIn(bottom_labels), FadeIn(bottom_header), run_time=1.2)
    narration_wait(scene, 2.0)

    # -- Beat 3: area under v grows while s is rebuilt underneath -------------
    tracker = ValueTracker(0.02)
    shaded = always_redraw(lambda: area_region(top_axes, velocity, 0, max(tracker.get_value(), 0.02), cfg.CYAN, 0.45))
    rebuilt = always_redraw(
        lambda: bottom_axes.plot(CAR.displacement, x_range=[0, max(tracker.get_value(), 0.02)], color=cfg.GOLD, stroke_width=6)
    )
    marker = always_redraw(lambda: glow_dot(bottom_axes.c2p(tracker.get_value(), CAR.displacement(tracker.get_value())), cfg.GOLD, 0.085))
    readout = live_readout(
        r"\text{area}=",
        lambda: CAR.area_under_velocity(0, tracker.get_value()),
        cfg.WHITE,
        cfg.FONT["small"],
        decimal_places=1,
        suffix=r"\text{m}",
    ).move_to([4.35, 3.05, 0])
    scene.add(shaded, rebuilt, marker, readout)
    caption = bottom_caption("Accumulated velocity becomes change in position.", cfg.GOLD)
    paced_play(scene, FadeIn(caption), run_time=0.7)
    paced_play(scene, tracker.animate.set_value(4.0), run_time=9.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 3.0)
    paced_play(scene, FadeOut(caption), run_time=0.5)

    readout.clear_updaters()
    scene.remove(shaded, rebuilt, marker, readout)
    frozen_area = area_region(top_axes, velocity, 0, 4, cfg.CYAN, 0.45)
    frozen_curve = bottom_axes.plot(CAR.displacement, x_range=[0, 4], color=cfg.GOLD, stroke_width=6)
    scene.add(frozen_area, frozen_curve)

    # -- Beat 4: the reverse problem, written down ----------------------------
    panel = VGroup(top_axes, bottom_axes, top_labels, bottom_labels, velocity, frozen_area, frozen_curve, top_header, bottom_header)
    paced_play(scene, panel.animate.scale(0.82).to_edge(UP, buff=0.35), run_time=1.0)

    line_1 = fitted_eq(r"\frac{ds}{dt}=2t", cfg.CYAN, cfg.FONT["section"])
    line_2 = fitted_eq(r"s(t)-s(0)=\int_0^t 2\tau\,d\tau", cfg.WHITE, cfg.FONT["section"])
    line_3 = fitted_eq(r"s(t)=s(0)+t^2", cfg.GREEN, cfg.FONT["section"])
    steps = VGroup(line_1, line_2, line_3).arrange(RIGHT, buff=0.85).to_edge(DOWN, buff=0.55)
    if steps.width > cfg.SAFE_WIDTH:
        steps.scale_to_fit_width(cfg.SAFE_WIDTH)
    arrow_1 = Arrow(line_1.get_right(), line_2.get_left(), color=cfg.MUTED, buff=0.16, stroke_width=4, max_tip_length_to_length_ratio=0.22)
    arrow_2 = Arrow(line_2.get_right(), line_3.get_left(), color=cfg.MUTED, buff=0.16, stroke_width=4, max_tip_length_to_length_ratio=0.22)

    paced_play(scene, FadeIn(line_1, shift=UP * 0.12), run_time=0.9)
    narration_wait(scene, 2.0)
    paced_play(scene, GrowArrow(arrow_1), FadeIn(line_2, shift=UP * 0.12), run_time=1.0)
    narration_wait(scene, 2.0)
    paced_play(scene, GrowArrow(arrow_2), FadeIn(line_3, shift=UP * 0.12), run_time=1.0)
    paced_play(scene, Indicate(line_3, color=cfg.WHITE, scale_factor=1.06), run_time=0.8)
    narration_wait(scene, 2.5)

    paced_play(scene, FadeOut(VGroup(panel, steps, arrow_1, arrow_2)), run_time=0.7)

    # -- Beat 5: the shape of the whole episode --------------------------------
    chips = VGroup(
        chip("rate of change", cfg.CYAN, cfg.FONT["small"]),
        chip("accumulation", cfg.BLUE, cfg.FONT["small"]),
        chip("the motion itself", cfg.GREEN, cfg.FONT["small"]),
    ).arrange(RIGHT, buff=1.05)
    if chips.width > cfg.SAFE_WIDTH:
        chips.scale_to_fit_width(cfg.SAFE_WIDTH)
    arrows = VGroup(
        Arrow(chips[0].get_right(), chips[1].get_left(), color=cfg.GOLD, buff=0.14, stroke_width=5, max_tip_length_to_length_ratio=0.3),
        Arrow(chips[1].get_right(), chips[2].get_left(), color=cfg.GOLD, buff=0.14, stroke_width=5, max_tip_length_to_length_ratio=0.3),
    )
    chain = VGroup(chips, arrows).move_to([0, 0.65, 0])
    paced_play(scene, LaggedStart(FadeIn(chips[0]), GrowArrow(arrows[0]), FadeIn(chips[1]), GrowArrow(arrows[1]), FadeIn(chips[2]), lag_ratio=0.42), run_time=3.2)
    narration_wait(scene, 3.0)
    paced_play(scene, FadeOut(chain), run_time=0.6)

    heading = title_card("VISUAL CALCULUS", "From Integrals to Differential Equations", cfg.GOLD)
    paced_play(scene, FadeIn(heading, shift=UP * 0.15), run_time=1.5)
    narration_wait(scene, 3.0)

    end_scene(scene, started, cfg.SCENE_DURATIONS["01"])
