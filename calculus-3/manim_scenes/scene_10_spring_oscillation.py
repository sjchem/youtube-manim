"""Scene 10: Newton's law is a differential equation, and a spring is its proof."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    block,
    bottom_caption,
    calc_axes,
    compact_axis_labels,
    end_scene,
    eq,
    fitted_eq,
    glow_dot,
    hide_background,
    move_3d_view,
    narration_wait,
    orbit_hold,
    outlined_text,
    paced_play,
    phase_helix,
    pin_to_frame,
    restore_background,
    set_3d_view,
    spring_shape,
    three_d_axes,
)
from utils.physics_models import SpringOscillator

OSC = SpringOscillator(mass=1.0, stiffness=4.0, amplitude=1.5)
WALL_X = -6.75
REST_X = -3.15
RIG_Y = 2.45
CYCLES = 3.0
WATCH = CYCLES * OSC.period


def _wall() -> VGroup:
    post = Line([WALL_X, RIG_Y - 1.05, 0], [WALL_X, RIG_Y + 1.05, 0], color=cfg.MUTED, stroke_width=7)
    hatch = VGroup(
        *(
            Line([WALL_X - 0.28, RIG_Y - 0.95 + 0.34 * i, 0], [WALL_X, RIG_Y - 0.62 + 0.34 * i, 0], color=cfg.GRAY, stroke_width=3)
            for i in range(6)
        )
    )
    floor = Line([WALL_X, RIG_Y - 0.62, 0], [REST_X + 2.35, RIG_Y - 0.62, 0], color=cfg.MUTED, stroke_width=3).set_stroke(opacity=0.5)
    return VGroup(post, hatch, floor)


class Scene10SpringOscillation(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "10")
    background = add_cinematic_background(scene)

    # -- Beat 1: F = ma, rewritten until it becomes an equation of change -----
    newton = fitted_eq("F=ma", cfg.WHITE, cfg.FONT["hero"], width=4.6).move_to([0, 0.9, 0])
    paced_play(scene, Write(newton), run_time=1.2)
    narration_wait(scene, 3.8)

    accel = fitted_eq(r"a=\frac{d^2x}{dt^2}", cfg.CYAN, cfg.FONT["title"], width=5.4).move_to([0, -1.35, 0])
    paced_play(scene, FadeIn(accel, shift=UP * 0.15), run_time=1.1)
    narration_wait(scene, 4.4)

    merged = fitted_eq(r"m\frac{d^2x}{dt^2}=F", cfg.GOLD, cfg.FONT["hero"], width=7.4).move_to([0, 0.9, 0])
    paced_play(scene, ReplacementTransform(newton, merged), FadeOut(accel), run_time=1.6)
    frame = SurroundingRectangle(merged, color=cfg.GOLD, buff=0.36, corner_radius=0.18, stroke_width=3.5)
    paced_play(scene, Create(frame), run_time=0.8)
    narration_wait(scene, 5.4)

    reading = outlined_text("physics does not say where things are — it says how they change", cfg.FONT["body"], cfg.PURPLE)
    if reading.width > cfg.SAFE_WIDTH:
        reading.scale_to_fit_width(cfg.SAFE_WIDTH)
    reading.next_to(frame, DOWN, buff=0.85)
    paced_play(scene, FadeIn(reading, shift=UP * 0.12), run_time=1.0)
    narration_wait(scene, 5.2)
    paced_play(scene, FadeOut(VGroup(merged, frame, reading)), run_time=0.7)

    # -- Beat 2: a real spring, and the force that pulls back -----------------
    rig = _wall()
    clock = ValueTracker(0.0)
    mass = always_redraw(lambda: block(0.86, cfg.GOLD, "m").move_to([REST_X + OSC.position(clock.get_value()), RIG_Y, 0]))
    coil = always_redraw(
        lambda: spring_shape([WALL_X, RIG_Y, 0], [REST_X + OSC.position(clock.get_value()) - 0.43, RIG_Y, 0], 9, 0.26, cfg.CYAN, 4.5)
    )
    rest_mark = DashedLine([REST_X, RIG_Y - 0.95, 0], [REST_X, RIG_Y + 0.95, 0], color=cfg.MUTED, stroke_width=2.6, dash_length=0.12)
    rest_tag = eq("x=0", cfg.MUTED, cfg.FONT["small"]).next_to(rest_mark, DOWN, buff=0.20)

    # The clock starts at zero, where cos is one: the mass is already held out
    # at full amplitude, which is exactly the "pull it back" the narration asks for.
    paced_play(scene, Create(rig), FadeIn(rest_mark), FadeIn(rest_tag), run_time=1.0)
    scene.add(coil, mass)
    narration_wait(scene, 4.0)

    def _restoring_arrow() -> Arrow:
        """Hooke's force under the mass: it flips with the mass and fades at rest."""
        displacement = OSC.position(clock.get_value())
        pull = OSC.restoring_force(displacement)
        magnitude = abs(pull)
        # Never let the arrow collapse to zero length at equilibrium; fade it
        # out instead, so the picture stays honest and Arrow stays valid.
        length = (-1.0 if displacement > 0 else 1.0) * max(magnitude * 0.16, 0.14)
        base = np.array([REST_X + displacement, RIG_Y - 0.86, 0.0])
        arrow = Arrow(base, base + RIGHT * length, color=cfg.RED, buff=0, stroke_width=7, max_tip_length_to_length_ratio=0.35)
        full_scale = OSC.stiffness * OSC.amplitude
        return arrow.set_opacity(float(np.clip(magnitude / full_scale, 0.12, 1.0)))

    force = always_redraw(_restoring_arrow)
    hooke = fitted_eq("F=-kx", cfg.RED, cfg.FONT["title"], width=4.4).move_to([3.6, 2.45, 0])
    scene.add(force)
    paced_play(scene, FadeIn(hooke, shift=DOWN * 0.12), run_time=0.9)
    narration_wait(scene, 4.4)

    pull = outlined_text("farther out → harder the pull back", cfg.FONT["body"], cfg.RED).move_to([3.6, 0.95, 0])
    if pull.width > 6.6:
        pull.scale_to_fit_width(6.6)
    paced_play(scene, FadeIn(pull), run_time=0.8)
    narration_wait(scene, 4.0)

    # -- Beat 3: the equation of motion for this rig ---------------------------
    equation = fitted_eq(r"m\frac{d^2x}{dt^2}=-kx", cfg.WHITE, cfg.FONT["title"], width=6.4).move_to([3.6, -1.15, 0])
    normalized = fitted_eq(r"\frac{d^2x}{dt^2}=-\frac{k}{m}\,x", cfg.GREEN, cfg.FONT["title"], width=6.4).move_to([3.6, -1.15, 0])
    paced_play(scene, FadeOut(pull), FadeIn(equation, shift=UP * 0.12), run_time=1.1)
    narration_wait(scene, 4.4)
    paced_play(scene, ReplacementTransform(equation, normalized), run_time=1.3)
    narration_wait(scene, 4.0)
    initial_state = fitted_eq(r"x(0)=x_0,\qquad x'(0)=v_0", cfg.PURPLE, cfg.FONT["section"], width=6.0)
    initial_state.next_to(normalized, DOWN, buff=0.48)
    state_note = outlined_text("second order → two initial facts", cfg.FONT["small"], cfg.MUTED)
    state_note.next_to(initial_state, DOWN, buff=0.30)
    paced_play(scene, FadeIn(initial_state, shift=UP * 0.12), FadeIn(state_note), run_time=1.0)
    narration_wait(scene, 6.8)
    paced_play(scene, FadeOut(VGroup(hooke, normalized, initial_state, state_note)), run_time=0.6)

    # -- Beat 4: three views of one motion, in step ----------------------------
    graph = calc_axes((0, WATCH, PI), (-2.2, 2.2, 1), 6.6, 2.5).move_to([-3.30, -1.55, 0])
    graph_labels = compact_axis_labels(graph, "t", "x", cfg.WHITE, cfg.FONT["body"])
    phase = calc_axes((-2.3, 2.3, 1), (-3.8, 3.8, 2), 3.9, 3.9).move_to([4.15, -0.55, 0])
    phase_labels = compact_axis_labels(phase, "x", "v", cfg.WHITE, cfg.FONT["body"])

    trace = always_redraw(
        lambda: graph.plot(OSC.position, x_range=[0, max(clock.get_value(), 0.01)], color=cfg.CYAN, stroke_width=5)
    )
    graph_dot = always_redraw(lambda: glow_dot(graph.c2p(clock.get_value(), OSC.position(clock.get_value())), cfg.GOLD, 0.08))
    ellipse = ParametricFunction(
        lambda s: phase.c2p(OSC.amplitude * np.cos(s), -OSC.amplitude * OSC.omega * np.sin(s)),
        t_range=[0, TAU],
        color=cfg.PURPLE,
        stroke_width=4,
    ).set_stroke(opacity=0.45)
    phase_dot = always_redraw(
        lambda: glow_dot(phase.c2p(OSC.position(clock.get_value()), OSC.velocity(clock.get_value())), cfg.PURPLE, 0.09)
    )

    paced_play(scene, Create(graph), FadeIn(graph_labels), Create(phase), FadeIn(phase_labels), run_time=1.2)
    scene.add(trace, graph_dot, ellipse, phase_dot)
    sync_caption = bottom_caption("One motion, three synchronized pictures.", cfg.GOLD)
    paced_play(scene, FadeIn(sync_caption), run_time=0.7)
    paced_play(scene, clock.animate.set_value(WATCH), run_time=13.0, rate_func=linear)
    narration_wait(scene, 5.4)

    # -- Beat 5: lift the phase point into time, and the trajectory is a helix --
    for mobject in (mass, coil, force, trace, graph_dot, phase_dot):
        mobject.clear_updaters()
    paced_play(
        scene,
        FadeOut(VGroup(rig, rest_mark, rest_tag, mass, coil, force, graph, graph_labels, trace, graph_dot, phase, phase_labels, ellipse, phase_dot, sync_caption)),
        run_time=0.8,
    )
    hide_background(scene)

    # Pull the helix down in projected screen space so its top coil remains
    # clear of the fixed solution formula.
    axes_3d = three_d_axes((-2.4, 2.4, 1), (-4, 4, 2), (0, 6.4, 2), unit=0.62).shift(IN * 1.0)
    helix = phase_helix(axes_3d, OSC.position, OSC.velocity, 0.0, WATCH, time_scale=6.4 / WATCH, velocity_scale=1.0, color=cfg.PURPLE, stroke_width=6)
    axis_tags = VGroup(
        eq(r"x\;\text{position}", cfg.CYAN, cfg.FONT["section"]),
        eq(r"v\;\text{velocity}", cfg.GOLD, cfg.FONT["section"]),
        eq(r"t\;\text{time}", cfg.GREEN, cfg.FONT["section"]),
    ).arrange(DOWN, buff=0.30, aligned_edge=LEFT).to_edge(RIGHT, buff=0.55).shift(DOWN * 0.20)
    axis_plate = SurroundingRectangle(
        axis_tags,
        color=cfg.MUTED,
        buff=0.28,
        corner_radius=0.14,
        stroke_width=2,
        stroke_opacity=0.35,
        fill_color=cfg.PANEL,
        fill_opacity=0.72,
    )
    set_3d_view(scene, phi=68 * DEGREES, theta=-58 * DEGREES)
    pin_to_frame(scene, axis_plate, axis_tags)
    paced_play(scene, Create(axes_3d), FadeIn(axis_plate), FadeIn(axis_tags), run_time=1.4)
    paced_play(scene, Create(helix), run_time=4.4, rate_func=rate_functions.ease_in_out_sine)
    orbit_hold(scene, 6.0)

    solution = fitted_eq(r"x(t)=A\cos(\omega t+\phi)", cfg.GREEN, cfg.FONT["title"], width=8.0).to_edge(UP, buff=0.42)
    omega_tag = fitted_eq(r"\omega=\sqrt{\tfrac{k}{m}}", cfg.CYAN, cfg.FONT["section"], width=3.6).to_edge(DOWN, buff=0.55)
    pin_to_frame(scene, solution, omega_tag)
    paced_play(scene, FadeIn(solution, shift=DOWN * 0.12), FadeIn(omega_tag, shift=UP * 0.12), run_time=1.2)
    move_3d_view(scene, phi=58 * DEGREES, theta=-115 * DEGREES, run_time=5.0)
    narration_wait(scene, 4.4)

    paced_play(scene, FadeOut(VGroup(axes_3d, axis_plate, axis_tags, helix, solution, omega_tag)), run_time=0.8)
    restore_background(scene, background)

    # Return to the three synchronized views for the final sentence instead
    # of leaving the caption alone on an empty background.
    final_motion = VGroup(
        rig.copy(),
        rest_mark.copy(),
        rest_tag.copy(),
        coil.copy(),
        mass.copy(),
        force.copy(),
        graph.copy(),
        graph_labels.copy(),
        trace.copy(),
        graph_dot.copy(),
        phase.copy(),
        phase_labels.copy(),
        ellipse.copy(),
        phase_dot.copy(),
    )
    verdict = bottom_caption("Pull it back, and calculus turns one rule into endless oscillation.", cfg.GOLD)
    paced_play(scene, FadeIn(final_motion), FadeIn(verdict), run_time=0.9)
    narration_wait(scene, 4.2)

    end_scene(scene, started, cfg.SCENE_DURATIONS["10"])
