"""Scene 01: a moving car turns "how fast, right now?" into a real question."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    calc_axes,
    car_icon,
    end_scene,
    eq,
    equation_card,
    glow_dot,
    narration_wait,
    outlined_text,
    paced_play,
    secant_line,
    speedometer_icon,
    tangent_line,
    title_card,
)
from utils.math_utils import car_position, car_velocity


class Scene01MovingCar(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "01")
    add_cinematic_background(scene)

    # -- Road and car, along the top third of frame --
    road_y = 3.05
    road = Line([-6.3, road_y, 0], [6.3, road_y, 0], color=cfg.GRAY, stroke_width=6)
    posts = VGroup(*[
        Line([x, road_y - 0.12, 0], [x, road_y + 0.12, 0], color=cfg.MUTED, stroke_width=2, stroke_opacity=0.5)
        for x in np.linspace(-6.0, 6.0, 13)
    ])
    car = car_icon(cfg.CYAN, scale=0.85).move_to([-6.3, road_y + 0.22, 0])

    # -- Position-time graph, filling the lower two-thirds --
    axes = calc_axes(x_range=(0, 5, 1), y_range=(0, 16, 4), x_length=10.2, y_length=4.5).move_to([0, -1.2, 0])
    # These are the first axis labels in the film, so give them enough visual
    # weight to remain unmistakable on a phone screen.
    axis_label_size = cfg.FONT["section"] + 4
    x_label = eq("t", cfg.WHITE, axis_label_size).next_to(axes.x_axis.get_right(), UP, buff=0.14)
    y_label = eq("s(t)", cfg.WHITE, axis_label_size).next_to(axes.y_axis.get_top(), RIGHT, buff=0.14)

    paced_play(
        scene,
        LaggedStart(Create(road), FadeIn(posts), Create(axes), FadeIn(x_label), FadeIn(y_label), lag_ratio=0.15),
        run_time=1.8,
    )
    paced_play(scene, FadeIn(car, shift=RIGHT * 0.15), run_time=0.5)

    def road_x(t: float) -> float:
        return -6.1 + (car_position(t) / 16.0) * 12.2

    t_tracker = ValueTracker(0.0)
    car.add_updater(lambda m: m.move_to([road_x(t_tracker.get_value()), road_y + 0.22, 0]))
    live_curve = always_redraw(
        lambda: axes.plot(car_position, x_range=[0, max(t_tracker.get_value(), 0.001)], color=cfg.CYAN, stroke_width=6)
    )
    live_dot = always_redraw(lambda: glow_dot(axes.c2p(t_tracker.get_value(), car_position(t_tracker.get_value())), cfg.GOLD, 0.09))
    scene.add(live_curve, live_dot)

    caption_1 = bottom_caption("A car eases away from a red light.", cfg.WHITE)
    paced_play(scene, FadeIn(caption_1), run_time=0.6)
    paced_play(scene, t_tracker.animate.set_value(3.0), run_time=7.0, rate_func=rate_functions.ease_in_sine)
    car.clear_updaters()
    car.move_to([road_x(3.0), road_y + 0.22, 0])

    avg_caption = bottom_caption("Average velocity is easy: distance over time.", cfg.GREEN)
    paced_play(scene, ReplacementTransform(caption_1, avg_caption), run_time=0.65)
    avg_formula = equation_card(r"v_{avg}=\frac{\Delta x}{\Delta t}", cfg.GREEN, cfg.FONT["section"])
    avg_formula.to_corner(UR, buff=0.5).shift(DOWN * 0.1)
    paced_play(scene, FadeIn(avg_formula, scale=1.08), run_time=0.8)
    narration_wait(scene, 6.88)

    # -- Beat B: a speedometer answers instantly; our average formula cannot --
    question = bottom_caption("But what is velocity at exactly t = 2 seconds?", cfg.GOLD)
    paced_play(scene, ReplacementTransform(avg_caption, question), run_time=0.7)
    narration_wait(scene, 5.51)

    # Keep the complete speedometer below the road rather than letting the
    # road cut through it. The question mark sits below as part of the icon.
    dial = speedometer_icon(cfg.GOLD, scale=1.15)
    dial.move_to([car.get_right()[0] + 1.25, road_y - 0.68, 0])
    dial_question = eq("?", cfg.GOLD, cfg.FONT["title"]).next_to(dial, DOWN, buff=0.08)
    speed_caption = bottom_caption("A speedometer answers instantly...", cfg.GOLD)
    paced_play(scene, ReplacementTransform(question, speed_caption), FadeIn(dial, scale=1.1), FadeIn(dial_question), run_time=0.9)
    narration_wait(scene, 4.82)

    speed_caption_2 = bottom_caption("...but our formula needs two separate moments.", cfg.WHITE)
    paced_play(scene, ReplacementTransform(speed_caption, speed_caption_2), FadeOut(dial), FadeOut(dial_question), run_time=0.75)
    narration_wait(scene, 5.8)

    # Reveal the film title only after the central mystery has created a
    # reason for it. The existing motion remains the visual thread beneath
    # this short, story-connected interlude.
    story_visuals = VGroup(road, posts, car, axes, x_label, y_label, live_curve, live_dot, avg_formula, speed_caption_2)
    paced_play(scene, FadeOut(story_visuals), run_time=0.55)
    card = title_card("VISUAL CALCULUS", "PART 1  •  FROM LIMITS TO DERIVATIVES", cfg.GOLD)
    paced_play(scene, FadeIn(card, shift=UP * 0.16), run_time=0.8)
    narration_wait(scene, 3.4)
    paced_play(scene, FadeOut(card, shift=UP * 0.12), run_time=0.55)
    paced_play(scene, FadeIn(story_visuals), run_time=0.65)
    narration_wait(scene, 6.2)

    # -- Beat C: pick t and t+h, draw the secant --
    t0 = 2.0
    h_tracker = ValueTracker(1.0)
    p_point = glow_dot(axes.c2p(t0, car_position(t0)), cfg.WHITE, 0.09)
    p_label = eq("P=(t,s(t))", cfg.WHITE, cfg.FONT["small"])
    p_label.next_to(p_point, UP, buff=0.32).shift(LEFT * 0.45)
    pick_caption = bottom_caption("Pick two moments: t, and t plus h.", cfg.WHITE)
    paced_play(scene, ReplacementTransform(speed_caption_2, pick_caption), FadeOut(avg_formula), FadeIn(p_point), FadeIn(p_label), run_time=0.8)
    narration_wait(scene, 4.82)

    q_point = always_redraw(
        lambda: glow_dot(axes.c2p(t0 + h_tracker.get_value(), car_position(t0 + h_tracker.get_value())), cfg.GOLD, 0.085)
    )
    secant = always_redraw(lambda: secant_line(axes, car_position, t0, h_tracker.get_value(), cfg.CYAN))
    h_readout = always_redraw(
        lambda: eq(rf"h={h_tracker.get_value():.3f}", cfg.GOLD, cfg.FONT["body"]).move_to([3.6, 2.45, 0])
    )
    slope_readout = always_redraw(
        lambda: eq(
            rf"\frac{{s(t+h)-s(t)}}{{h}}={car_velocity(t0) + 0.55 * h_tracker.get_value():.2f}",
            cfg.CYAN,
            cfg.FONT["body"],
        ).next_to(h_readout, DOWN, buff=0.22, aligned_edge=LEFT)
    )
    scene.add(secant, q_point, h_readout, slope_readout)
    paced_play(scene, FadeIn(h_readout), FadeIn(slope_readout), run_time=0.7)
    narration_wait(scene, 3.44)

    secant_caption = bottom_caption("That connecting line is a secant.", cfg.CYAN)
    paced_play(scene, ReplacementTransform(pick_caption, secant_caption), run_time=0.7)
    narration_wait(scene, 13.76)

    # -- Beat D: shrink h and watch the secant rotate into the tangent --
    shrink_caption = bottom_caption("Shrink h, and watch the line rotate.", cfg.WHITE)
    paced_play(scene, ReplacementTransform(secant_caption, shrink_caption), run_time=0.65)

    for target_h in (0.4, 0.15, 0.05, 0.015, 0.005, 0.0015):
        paced_play(scene, h_tracker.animate.set_value(target_h), run_time=4.4, rate_func=rate_functions.ease_in_out_sine)
        narration_wait(scene, 1.38)

    # -- Beat E: the tangent settles, and the limit definition is revealed --
    tangent_caption = bottom_caption("It settles on one special line: the tangent.", cfg.GREEN)
    paced_play(scene, ReplacementTransform(shrink_caption, tangent_caption), run_time=0.7)
    tangent = tangent_line(axes, car_position, car_velocity, t0, cfg.GREEN, half_length=1.9)
    paced_play(scene, FadeIn(tangent, scale=1.02), run_time=1.0)
    narration_wait(scene, 4.13)

    definition = eq(r"v(t)=\lim_{h\to 0}\frac{s(t+h)-s(t)}{h}", cfg.WHITE, cfg.FONT["section"])
    # The road/car occupy the upper lane. The definition fits cleanly in the
    # open band between that lane and the graph.
    definition.move_to([2.0, 2.02, 0])
    definition.set_color_by_tex(r"\lim", cfg.PURPLE)
    paced_play(
        scene,
        FadeOut(VGroup(h_readout, slope_readout, p_label)),
        Write(definition),
        run_time=1.6,
    )
    narration_wait(scene, 13.76)

    closing = bottom_caption("That question creates the idea of a limit.", cfg.GOLD)
    paced_play(scene, ReplacementTransform(tangent_caption, closing), run_time=0.7)
    narration_wait(scene, 8.26)

    end_scene(scene, started, cfg.SCENE_DURATIONS["01"])
