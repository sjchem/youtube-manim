"""Follow energy into a gas, light through a prism, and spectra into a clue."""
from __future__ import annotations

import numpy as np
from manim import *
import config as cfg
from manim_scenes.common import (
    add_cinematic_background, begin_scene, continuous_spectrum, end_scene,
    energy_staircase, eq, glow_dot, glow_line, line_spectrum, narration_wait,
    outlined_text, paced_play, photon, prism,
)
from utils.physics_models import HydrogenAtom
from utils.render_helpers import spectrum_positions
from utils.math_utils import wavelength_to_hex

BALMER = HydrogenAtom().balmer_series(6)
WIDTH = 10.0
LOW, HIGH = 380, 720
SCREEN_HEIGHT = 4.4
SCREEN_CENTRE = np.array([4.8, -1.0, 0])


def _tube(width=4.6, height=0.8):
    """Glass, metallic terminals and a restrained pink discharge, in layers."""
    glass = RoundedRectangle(width=width, height=height, corner_radius=height/2,
        stroke_color='#B7E4F6', stroke_width=2, fill_color='#193950', fill_opacity=0.3)
    glow = VGroup(*[
        RoundedRectangle(width=width-0.3+pad, height=height*0.48+pad,
            corner_radius=(height*0.48+pad)/2, stroke_width=0,
            fill_color='#F59AD9', fill_opacity=opacity)
        for pad, opacity in ((0.3, 0.04), (0.12, 0.10), (0, 0.32))
    ])
    caps = VGroup(*[
        RoundedRectangle(width=0.20, height=height*0.77, corner_radius=0.04,
            stroke_color='#BCD1D9', stroke_width=1.2, fill_color='#607887', fill_opacity=1)
        .move_to([x, 0, 0]) for x in (-width/2+0.16, width/2-0.16)
    ])
    sheen = Line([-width*0.38, height*0.32, 0], [width*0.38, height*0.32, 0],
                 color=cfg.WHITE, stroke_width=2, stroke_opacity=0.5)
    gas = VGroup(*[Dot([x, y, 0], radius=0.035, color='#ECBEF8')
                  for x, y in ((-1.3, .08), (-.7, -.12), (0, .1), (.65, -.1), (1.3, .05))])
    gas.stretch_to_fit_width(width*0.62)
    return VGroup(glow, glass, caps, sheen, gas)


def _wave_packet(scene, start, end, color, duration=1.8):
    direction = np.array(end)-np.array(start)
    unit = direction/np.linalg.norm(direction)
    packet = photon(start, np.array(start)+unit*0.9, wavelength=0.3,
                    color=color, amplitude=0.10)
    paced_play(scene, FadeIn(packet), run_time=0.2)
    paced_play(scene, packet.animate.shift(direction), run_time=duration, rate_func=linear)
    paced_play(scene, FadeOut(packet), run_time=0.2)


def _wave_colour(nm):
    """Follow spectral hues through the transition, with a little white for clarity."""
    return interpolate_color(ManimColor(wavelength_to_hex(nm)), ManimColor('#FFFFFF'), .22)


def _wavelength_demo(scene):
    nm, phase = ValueTracker(656), ValueTracker(0)
    anchor, baseline, amplitude = -1.6, 0.1, 0.48

    def make_wave():
        length = 3.2*nm.get_value()/656
        xs = np.linspace(-5.7, 5.7, 300)
        points = np.column_stack((xs, baseline+amplitude*np.cos(TAU*(xs-anchor)/length-phase.get_value()), np.zeros_like(xs)))
        wave = VMobject().set_points_smoothly(points).set_stroke(_wave_colour(nm.get_value()), width=4)
        return VGroup(wave.copy().set_stroke(width=14, opacity=0.09), wave)

    wave = always_redraw(make_wave)
    paced_play(scene, FadeIn(wave), run_time=1)
    paced_play(scene, phase.animate.set_value(TAU), run_time=2.4, rate_func=linear)
    # The phase is now one full turn: both measured points are actual crests.
    def marks():
        length = 3.2*nm.get_value()/656
        x1, x2 = anchor, anchor+length
        color = _wave_colour(nm.get_value())
        return VGroup(
            DashedLine([x1, baseline+amplitude, 0], [x1, 1.7, 0], color=color, stroke_width=1.5),
            DashedLine([x2, baseline+amplitude, 0], [x2, 1.7, 0], color=color, stroke_width=1.5),
            DoubleArrow([x1, 1.55, 0], [x2, 1.55, 0], color=color, buff=0, stroke_width=3),
            Dot([x1, baseline+amplitude, 0], radius=0.055, color=color),
            Dot([x2, baseline+amplitude, 0], radius=0.055, color=color),
        )
    measure = always_redraw(marks)
    symbol = eq(r'\lambda', cfg.WHITE, 62).move_to([0, 2.25, 0])
    symbol.add_updater(lambda m: m.set_x(anchor+1.6*nm.get_value()/656))
    longer = outlined_text('Longer', 36, '#FF8883').move_to([0, -1.3, 0])
    paced_play(scene, FadeIn(measure, symbol, longer), run_time=0.7)
    narration_wait(scene, 2.0)
    shorter = outlined_text('Shorter', 36, '#90FFC2').move_to(longer)
    paced_play(scene, nm.animate.set_value(530),
               Succession(FadeOut(longer, run_time=.4), Wait(2.2), FadeIn(shorter, run_time=.4)),
               run_time=3)
    narration_wait(scene, 1.4)
    paced_play(scene, nm.animate.set_value(410), shorter.animate.set_color('#C8AEFF'), run_time=2.4)
    narration_wait(scene, 1)
    measure.clear_updaters()
    symbol.clear_updaters()
    paced_play(scene, FadeOut(measure, symbol, shorter), run_time=0.6)
    paced_play(scene, phase.animate.set_value(TAU*2.3), run_time=2.6, rate_func=linear)
    wave.clear_updaters()
    paced_play(scene, FadeOut(wave), run_time=0.7)


def _horizontal_spectrum(wavelengths, y):
    plate, lines = line_spectrum(wavelengths, width=WIDTH, height=0.85, low_nm=LOW, high_nm=HIGH)
    return VGroup(plate, lines).shift(UP*y)


class Scene09LightBarcode(Scene):
    def construct(self):
        play_scene(self)


def play_scene(scene):
    started = begin_scene(scene, '09')
    add_cinematic_background(scene)

    # A powered discharge: current reaches the gas, then light leaves it.
    heading = outlined_text('LIGHT FROM ATOMS', 44, cfg.GOLD).move_to([0, 3.1, 0])
    tube = _tube().move_to([-1.7, 0.6, 0])
    glow = tube[0]
    tube.remove(glow)
    name = outlined_text('HYDROGEN', 30, cfg.CYAN).move_to([-1.7, 1.6, 0])
    power = RoundedRectangle(width=1.7, height=0.7, corner_radius=0.12,
        fill_color='#19364A', fill_opacity=1, stroke_color=cfg.MUTED, stroke_width=1.5).move_to([-1.7, -1.8, 0])
    bolt = VMobject(color=cfg.GOLD, stroke_width=4).set_points_as_corners([
        [-1.55, -1.57, 0], [-1.85, -1.82, 0], [-1.59, -1.82, 0], [-1.84, -2.03, 0]])
    wires = VGroup(*[
        VMobject(color=cfg.MUTED, stroke_width=2).set_points_as_corners(points)
        for points in (
            [[-2.55, -1.8, 0], [-4.4, -1.8, 0], [-4.4, .6, 0], [-3.84, .6, 0]],
            [[.44, .6, 0], [.9, .6, 0], [.9, -1.8, 0], [-.85, -1.8, 0]],
        )
    ])
    paced_play(scene, FadeIn(tube, heading, name), run_time=1)
    paced_play(scene, Create(wires), FadeIn(power, bolt), run_time=1.2)
    narration_wait(scene, 1)
    paced_play(scene, FadeOut(heading, name), run_time=0.6)
    current = glow_dot(wires[0].get_start(), cfg.GOLD, 0.06)
    scene.add(current)
    paced_play(scene, MoveAlongPath(current, wires[0]), run_time=2, rate_func=linear)
    scene.add(glow)
    scene.bring_to_front(tube)
    paced_play(scene, current.animate.move_to([-1.7, .6, 0]), FadeIn(glow), run_time=0.8)
    scene.remove(current)
    for (_, _, color), y in zip(BALMER[:3], (1.7, 0.7, -0.35)):
        _wave_packet(scene, [.4, .6, 0], [4.8, y, 0], color, duration=1.8)
    narration_wait(scene, 2.0)
    paced_play(scene, FadeOut(tube, glow, power, bolt, wires), run_time=0.8)

    _wavelength_demo(scene)

    # The same source position, prism and screen are kept through both trials.
    glass = prism(1.7, cfg.CYAN).move_to([-1.2, 1.6, 0])
    # A second face gives the glass a little depth without moving the labels.
    rear_face = glass[1].copy().shift(RIGHT*.18+UP*.16).set_fill('#246A85', opacity=0.20).set_stroke(width=1.2, opacity=.4)
    glass.add_to_back(rear_face)
    bulb = VGroup(
        Circle(radius=.27, stroke_color=cfg.WHITE, stroke_width=2, fill_color='#FFF2CA', fill_opacity=.9),
        Line([-.09, -.1, 0], [.09, .1, 0], color=cfg.GOLD, stroke_width=3),
    ).move_to([-5, 1.6, 0])
    source_name = outlined_text('White light', 32, cfg.WHITE).move_to([-5, 2.45, 0])
    beam = VGroup(glow_line([-4.7, 1.6, 0], [-1.85, 1.6, 0], cfg.WHITE, width=4),
                  glow_line([-1.85, 1.6, 0], [-.53, 1.4, 0], cfg.WHITE, width=2))
    band = continuous_spectrum(width=SCREEN_HEIGHT, height=.72, low_nm=LOW, high_nm=HIGH, slices=160)
    # Close Cairo's subpixel seams between adjacent coloured slices.
    for strip in band[0]:
        strip.set_stroke(strip.get_fill_color(), width=1.1, opacity=1)
    band.rotate(PI/2).move_to(SCREEN_CENTRE)
    spectrum_name = outlined_text('Continuous', 34, cfg.WHITE).move_to([4.7, 2.15, 0])
    exit_point = np.array([-.53, 1.4, 0])
    wavelengths = np.linspace(LOW+10, HIGH-10, 35)
    fan = VGroup(*[
        Line(exit_point, [4.42, SCREEN_CENTRE[1]+y, 0], color=wavelength_to_hex(nm),
             stroke_width=2.5, stroke_opacity=.40)
        for nm, y in zip(wavelengths, spectrum_positions(wavelengths, LOW, HIGH, SCREEN_HEIGHT))
    ])
    paced_play(scene, FadeIn(bulb, source_name, glass), Create(beam), run_time=1.6)
    paced_play(scene, LaggedStart(*[Create(ray) for ray in fan], lag_ratio=.035), FadeIn(band, spectrum_name), run_time=2)
    narration_wait(scene, 2.5)
    paced_play(scene, FadeOut(source_name, spectrum_name), run_time=.7)
    paced_play(scene, ShowPassingFlash(fan.copy().set_stroke(opacity=.8), time_width=.25), run_time=3.5)
    narration_wait(scene, 2)

    hydrogen = _tube(width=2.3, height=.55).move_to([-5, 1.6, 0])
    hname = outlined_text('HYDROGEN', 32, cfg.CYAN).move_to([-5, 2.45, 0])
    hbeam = VGroup(glow_line([-3.75, 1.6, 0], [-1.85, 1.6, 0], '#E7A3F0', width=4),
                   glow_line([-1.85, 1.6, 0], [-.53, 1.4, 0], '#E7A3F0', width=2))
    plate, lines = line_spectrum([w for _, w, _ in BALMER], width=SCREEN_HEIGHT, height=.72, low_nm=LOW, high_nm=HIGH)
    barcode = VGroup(plate, lines).rotate(PI/2).move_to(SCREEN_CENTRE)
    paced_play(scene, FadeOut(bulb, band, fan), FadeIn(hydrogen, hname, plate),
               ReplacementTransform(beam, hbeam), run_time=1.5)
    selected_rays = VGroup()
    for line, (_, nm, color) in zip(lines, BALMER):
        endpoint = line.get_left()
        ray = Line(exit_point, endpoint, color=color, stroke_width=2.7, stroke_opacity=.60)
        selected_rays.add(ray)
        paced_play(scene, Create(ray), run_time=.7)
        paced_play(scene, FadeIn(line), run_time=.5)
        narration_wait(scene, 1.5)
    four = outlined_text('4 visible lines', 34, cfg.GOLD).move_to([4.7, 2.15, 0])
    paced_play(scene, FadeIn(four), run_time=.7)
    narration_wait(scene, 3)
    paced_play(scene, FadeOut(four, hname), run_time=.7)
    narration_wait(scene, 4)

    # Turn the same measured lines into a horizontal barcode for comparison.
    paced_play(scene, FadeOut(hydrogen, hbeam, glass, selected_rays), run_time=.8)
    target = _horizontal_spectrum([w for _, w, _ in BALMER], -.2)
    paced_play(scene, Transform(barcode, target, path_arc=-PI/3), run_time=2)
    question = outlined_text('Why these colours?', 44, cfg.GOLD).move_to([0, 2, 0])
    paced_play(scene, FadeIn(question), run_time=.8)
    narration_wait(scene, 3)
    paced_play(scene, FadeOut(question), run_time=.7)
    # A replay lights exactly the same four positions, with no new text card.
    paced_play(scene, LaggedStart(*[Indicate(line, color=line._spectral_color, scale_factor=1.05)
        for line in barcode[1]], lag_ratio=.6), run_time=3.8)
    narration_wait(scene, 3)

    paced_play(scene, barcode.animate.shift(UP*1.5), run_time=1.2)
    hname = outlined_text('HYDROGEN', 32, cfg.CYAN).move_to([0, 2.25, 0])
    helium_wavelengths = [447.1, 471.3, 492.2, 501.6, 587.6, 667.8]
    helium = _horizontal_spectrum(helium_wavelengths, -1.15)
    hename = outlined_text('HELIUM', 32, cfg.GOLD).move_to([0, -.2, 0])
    paced_play(scene, FadeIn(hname, helium, hename), run_time=1.4)
    scan = Line([-5.3, -1.8, 0], [-5.3, 1.95, 0], color=cfg.WHITE, stroke_width=1.5, stroke_opacity=.5)
    scene.add(scan)
    paced_play(scene, scan.animate.shift(RIGHT*10.6), run_time=6, rate_func=linear)
    paced_play(scene, FadeOut(scan), run_time=.5)
    narration_wait(scene, 4)
    # Carry the hydrogen pattern into the distant-star example. The faint
    # reference positions make a small collective wavelength shift visible.
    star = VGroup(glow_dot([-6.1, 1.3, 0], '#E6F3FF', .10),
        Star(n=4, outer_radius=.24, inner_radius=.065, color='#E6F3FF',
             stroke_width=0, fill_opacity=1).move_to([-6.1, 1.3, 0]))
    paced_play(scene, FadeOut(helium, hename), FadeIn(star), run_time=1)
    reference = barcode[1].copy().fade(.84)
    scene.add(reference)
    # An illustrative common redshift: lambda_observed = (1+z)*lambda_rest.
    shifts = [RIGHT*(nm*.015*WIDTH/(HIGH-LOW)) for _, nm, _ in BALMER]
    paced_play(scene, *[line.animate.shift(delta) for line, delta in zip(barcode[1], shifts)], run_time=2.5)
    narration_wait(scene, 1)
    paced_play(scene, *[line.animate.shift(-delta) for line, delta in zip(barcode[1], shifts)], run_time=2.5)
    paced_play(scene, FadeOut(reference), run_time=1)
    # Brightness changes do not move a line's wavelength position.
    paced_play(scene, barcode[1][0].animate.fade(.25), barcode[1][2].animate.fade(.5), run_time=2)
    narration_wait(scene, 4)
    paced_play(scene, FadeOut(hname, barcode, star), run_time=.8)

    # A visual hand-off to Bohr's staircase, with no full-sentence closing slide.
    wave = photon([-5.3, .5, 0], [-2.7, .5, 0], wavelength=.75, color=cfg.CYAN, amplitude=.3)
    steps, _ = energy_staircase(width=3.6, height=2.6, steps=4, color=cfg.GOLD)
    steps.move_to([2.5, .2, 0])
    question = outlined_text('Energy?', 46, cfg.GOLD).move_to([0, 2.5, 0])
    paced_play(scene, FadeIn(wave, question), run_time=1)
    paced_play(scene, Create(steps), run_time=2.5)
    narration_wait(scene, 2)
    paced_play(scene, FadeOut(question), run_time=.6)
    narration_wait(scene, 7)
    end_scene(scene, started, cfg.SCENE_DURATIONS['09'])
