"""Scene 04: a clear 3D cathode-ray experiment, followed by Thomson's evidence."""
from __future__ import annotations

import numpy as np
from manim import *
import config as cfg
from manim_scenes.common import (
    add_cinematic_background, begin_scene, check_mark, chip, electron,
    end_scene, eq, fit_width, glow_dot, hide_background, narration_wait,
    outlined_text, paced_play, pin_to_frame, reset_flat_camera,
    restore_background, set_3d_view, top_caption, unpin_from_frame,
)
from utils.physics_models import CathodeRayTube

SCREEN_X = 4.25
FIELD = CathodeRayTube(plate_start=0.1, plate_end=2.25, deflection=0.23)


def _metal_box(dimensions, center, color="#687580") -> Prism:
    return Prism(dimensions=dimensions, fill_color=color, fill_opacity=1,
                 stroke_color="#A2ACAE", stroke_width=0.45).move_to(center)


def _end_ring(x, radius, color=cfg.MUTED, width=2.0):
    return Circle(radius=radius, color=color, stroke_width=width).rotate(PI / 2, axis=UP).shift(RIGHT*x).set_shade_in_3d(True)


def _tube_apparatus():
    """Glass envelope, metal electrodes and screen; no visible beam in vacuum.

    A teaching reconstruction combines the shadow and deflection demonstrations;
    it is not a dimensional replica of one of Thomson's historical tubes.
    """
    def radius(x):
        return 0.60 + 0.68 * np.clip((x + 2.6) / 1.4, 0, 1)

    glass = Surface(lambda x, t: np.array([x, radius(x)*np.cos(t), radius(x)*np.sin(t)]),
                    u_range=(-4.3, 4.4), v_range=(0, TAU), resolution=(12, 24),
                    checkerboard_colors=False, fill_color="#A3DDE7", fill_opacity=0.045,
                    stroke_width=0)
    edges = VGroup(_end_ring(-4.3, 0.60), _end_ring(4.4, 1.28),
                   _end_ring(4.32, 1.28, "#D5EAF0", 1.1))
    for angle in (-PI / 2, 0.8, 2.2):
        shine = ParametricFunction(lambda x, a=angle: np.array([x, radius(x)*np.cos(a), radius(x)*np.sin(a)]),
                                   t_range=(-4.3, 4.4), color="#C5EAF4", stroke_width=1.8)
        shine.set_stroke(opacity=0.42).set_shade_in_3d(True)
        edges.add(shine)
    base = _metal_box((10.1, 2.25, 0.22), [0, 0, -2.0], "#493527")
    stands = VGroup(*[_metal_box((0.28, 0.55, 0.85), [x, 0, -1.48], "#596267") for x in (-3.5, 3.3)])
    # The copper anode is an actual annulus with a clear central aperture.
    cathode = Cylinder(radius=0.43, height=0.10, direction=RIGHT, resolution=(2, 24),
                       fill_color="#8EA5AF", fill_opacity=1, stroke_width=0).move_to([-3.65, 0, 0])
    anode = Annulus(inner_radius=0.17, outer_radius=0.49, fill_color="#BE8E5C", fill_opacity=1,
                    stroke_color="#E3BB87", stroke_width=1.2).rotate(PI/2, axis=UP).shift(LEFT*2.65)
    anode.set_shade_in_3d(True)
    cathode_lead = Line3D([-5, 0, 0], [-3.65, 0, 0], thickness=0.035, color="#89989E")
    anode_lead = Line3D([-2.65, 0, -0.43], [-2.65, 0, -1.80], thickness=0.028, color="#BA8953")
    screen = Circle(radius=1.13, fill_color="#214735", fill_opacity=1,
                    stroke_color="#A0B49D", stroke_width=3).rotate(PI/2, axis=UP).shift(RIGHT*SCREEN_X)
    screen.set_shade_in_3d(True)
    # Fine unnumbered screen ticks make the displacement measurable without prose.
    ticks = VGroup(*[Line([SCREEN_X+0.01, -0.91, z], [SCREEN_X+0.01, -0.81, z],
                         color="#91AA94", stroke_width=1).set_shade_in_3d(True)
                     for z in np.linspace(-0.65, 0.65, 7)])
    return dict(envelope=VGroup(glass, edges), stand=VGroup(base, stands),
                cathode=VGroup(cathode, cathode_lead), anode=VGroup(anode, anode_lead),
                screen=VGroup(screen, ticks))


def _screen_spot(height=0.0):
    spot = glow_dot(ORIGIN, "#A8FF9E", 0.095)
    spot.rotate(PI/2, axis=UP).move_to([SCREEN_X+0.025, 0, height])
    # Emission is unshaded and drawn over the screen. Cairo sorts shaded objects
    # by their centres, which otherwise hides a spot on the lower half of a disc.
    return spot.set_shade_in_3d(False)


def _shadow():
    # A single polygon avoids transparent overlaps at the centre of the cross.
    a, b = 0.16, 0.61
    points = [(-a,b),(a,b),(a,a),(b,a),(b,-a),(a,-a),
              (a,-b),(-a,-b),(-a,-a),(-b,-a),(-b,a),(-a,a)]
    return Polygon(*[[SCREEN_X+0.03, y, z] for y,z in points], fill_color="#07130E",
                   fill_opacity=1, stroke_width=0).set_shade_in_3d(True)


def _label(scene, text, color, position):
    label = outlined_text(text, 30, color).move_to(position)
    pin_to_frame(scene, label)
    scene.remove(label)
    return label


class Scene04CathodeRays(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "04")
    add_cinematic_background(scene)
    background = hide_background(scene)
    set_3d_view(scene, phi=70*DEGREES, theta=-42*DEGREES)
    parts = _tube_apparatus()

    # Assemble one component at a time. Explanation belongs to the voice track.
    paced_play(scene, FadeIn(parts["stand"]), FadeIn(parts["envelope"]), run_time=1.6)
    scene.move_camera(theta=-48*DEGREES, run_time=4.8, rate_func=smooth)
    cathode_label = _label(scene, "Cathode −", cfg.CYAN, [-3.9, 2.0, 0])
    anode_label = _label(scene, "Anode +", cfg.ORANGE, [-1.3, 2.0, 0])
    screen_label = _label(scene, "Screen", cfg.GREEN, [4.1, 1.8, 0])
    labels = (cathode_label, anode_label, screen_label)
    paced_play(scene, FadeIn(parts["cathode"]), FadeIn(cathode_label), run_time=1.0)
    narration_wait(scene, 4.0)
    paced_play(scene, FadeIn(parts["anode"]), FadeIn(anode_label), run_time=1.0)
    narration_wait(scene, 4.0)
    paced_play(scene, FadeIn(parts["screen"]), FadeIn(screen_label), run_time=0.9)
    narration_wait(scene, 3.6)

    voltage = _label(scene, "∼10 kV", cfg.GOLD, [-4.9, -2.65, 0])
    paced_play(scene, FadeIn(voltage), run_time=0.8)
    narration_wait(scene, 1.4)
    spot = _screen_spot()
    paced_play(scene, FadeIn(spot, scale=1.7), run_time=0.6)
    narration_wait(scene, 8.2)

    # Only the screen fluoresces. No luminous path is drawn inside the glass.
    cross = VGroup(_metal_box((0.12, 0.22, 0.85), [1.9,0,0], "#42484A"),
                   _metal_box((0.12, 0.85, 0.22), [1.9,0,0], "#42484A"),
                   _metal_box((0.09, 0.09, 0.70), [1.9,0,-0.75], "#42484A"))
    shadow = _shadow()
    paced_play(scene, FadeIn(cross, shift=UP*0.25), run_time=0.9)
    paced_play(scene, parts["screen"][0].animate.set_fill("#7DBB68", opacity=1), FadeOut(spot), run_time=0.8)
    paced_play(scene, FadeIn(shadow), run_time=0.9)
    narration_wait(scene, 8.2)
    paced_play(scene, FadeOut(cross, shadow), parts["screen"][0].animate.set_fill("#214735", opacity=1),
               FadeIn(spot), run_time=0.8)

    plates = VGroup(_metal_box((2.15,0.85,0.10), [1.175,0,0.92], "#BE8E5C"),
                    _metal_box((2.15,0.85,0.10), [1.175,0,-0.92], "#8EA5AF"))
    plus = _label(scene, "+", cfg.ORANGE, [0.8,1.45,0])
    minus = _label(scene, "−", cfg.CYAN, [0.8,-1.7,0])
    paced_play(scene, FadeIn(plates), FadeIn(plus, minus), run_time=1.0)
    narration_wait(scene, 4.2)
    displacement = FIELD.offset(SCREEN_X)
    paced_play(scene, spot.animate.shift(OUT*displacement), run_time=3.4, rate_func=smooth)
    narration_wait(scene, 5.4)

    # Swap the actual polarity symbols as well as reversing the displacement.
    paced_play(scene, plus.animate.move_to([0.8,-1.7,0]), minus.animate.move_to([0.8,1.45,0]),
               plates[0].animate.set_fill("#8EA5AF"), plates[1].animate.set_fill("#BE8E5C"), run_time=1.1)
    paced_play(scene, spot.animate.shift(IN*2*displacement), run_time=3.8, rate_func=smooth)
    narration_wait(scene, 5.4)

    paced_play(scene, FadeOut(*parts.values(), spot, plates, plus, minus, voltage, *labels), run_time=0.9)
    unpin_from_frame(scene, *labels, plus, minus, voltage)
    reset_flat_camera(scene)
    restore_background(scene, background)

    # Give Thomson and the quantitative result their own uncrowded composition.
    portrait = ImageMobject(str(cfg.PROJECT_ROOT / "assets/images/jj_thomson_1896.jpg"))
    portrait.height = 3.65
    portrait.move_to([-4.65,0.65,0])
    border = SurroundingRectangle(portrait, buff=0.07, color=cfg.MUTED, stroke_width=1.5)
    name = outlined_text("J. J. Thomson", cfg.FONT["small"], cfg.WHITE).move_to([-4.65,-1.62,0])
    date = outlined_text("1897", cfg.FONT["tiny"], cfg.MUTED).next_to(name, DOWN, buff=0.23)
    paced_play(scene, FadeIn(portrait), FadeIn(border, name, date), run_time=1.0)
    ratio = eq(r"\frac{e}{m}", cfg.WHITE, cfg.FONT["hero"]).move_to([0.1,0.9,0])
    measured = eq(r"1.76\times10^{11}\ \text{C}\,\text{kg}^{-1}", cfg.GOLD, cfg.FONT["body"])
    measured.next_to(ratio, RIGHT, buff=0.65)
    paced_play(scene, FadeIn(ratio), run_time=1.0)
    paced_play(scene, FadeIn(measured, shift=RIGHT*0.15), run_time=0.8)
    narration_wait(scene, 5.2)
    tiny = outlined_text(
        f"modern value: about 1/{FIELD.mass_ratio_to_hydrogen:.0f} of hydrogen's mass",
        cfg.FONT["small"], cfg.MUTED,
    )
    fit_width(tiny)
    tiny.move_to([0,-3.35,0])
    paced_play(scene, FadeIn(tiny), run_time=0.8)
    # Reserve the original final comparison sequence and fade, accounting for FPS.
    narration_wait(scene, max(8.0, cfg.SCENE_DURATIONS["04"] - (scene.time-started) - 29.9))
    paced_play(scene, FadeOut(portrait, border, name, date, ratio, measured, tiny), run_time=0.9)

    swap_heading = top_caption("CHANGE EVERYTHING. RUN IT AGAIN.", cfg.GOLD)
    paced_play(scene, FadeIn(swap_heading), run_time=0.8)

    trials = (
        ("different metal", cfg.BLUE),
        ("different gas", cfg.PURPLE),
        ("different tube", cfg.ORANGE),
    )
    columns = VGroup()
    for text, color in trials:
        plate = chip(text, color, cfg.FONT["small"])
        arrow = Arrow(UP * 0.35, DOWN * 0.35, color=cfg.MUTED, stroke_width=4,
                      buff=0.05, max_tip_length_to_length_ratio=0.35)
        bead = electron(0.20)
        columns.add(VGroup(plate, arrow, bead).arrange(DOWN, buff=0.34))
    columns.arrange(RIGHT, buff=1.35).move_to([0, 0.35, 0])

    for column in columns:
        paced_play(scene, FadeIn(column[0], shift=DOWN * 0.15), run_time=0.6)
        paced_play(scene, GrowArrow(column[1]), FadeIn(column[2], scale=1.5), run_time=0.8)
        narration_wait(scene, 3.0)

    same = VGroup(
        check_mark(0.24, cfg.GREEN),
        outlined_text("the same particle, every time", cfg.FONT["body"], cfg.GREEN),
    ).arrange(RIGHT, buff=0.38)
    same.move_to([0, -2.30, 0])
    paced_play(scene, FadeIn(same, shift=UP * 0.15), run_time=0.9)
    narration_wait(scene, 6.0)

    named = outlined_text("ELECTRON", cfg.FONT["title"], cfg.CYAN).move_to([0, -3.45, 0])
    paced_play(scene, FadeIn(named, scale=1.12), run_time=0.9)
    narration_wait(scene, 6.2)

    end_scene(scene, started, cfg.SCENE_DURATIONS["04"])
