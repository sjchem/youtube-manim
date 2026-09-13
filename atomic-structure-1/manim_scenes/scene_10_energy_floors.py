"""A supported ball on solid steps becomes a diagram of allowed energies."""
from __future__ import annotations

import numpy as np
from manim import *
import config as cfg
from manim_scenes.common import (
    add_cinematic_background, begin_scene, cross_mark, electron, end_scene,
    eq, ionisation_line, narration_wait, outlined_text, paced_play, photon,
)
from utils.physics_models import HydrogenAtom

HYDROGEN = HydrogenAtom()
LABELLED_LEVELS = (1, 2, 3)
COMB_LEVELS = (4, 5, 6, 7, 8, 9)
BASE_Y, LADDER_SPAN = -2.55, 5.35
DEPTH = np.array([0.48, 0.34, 0])
LEFT_X, RIGHT_X = -3.2, 3.2
TREAD_Y = (-1.7, -0.75, 0.2, 1.15)


def level_y(n):
    """Preserve hydrogen's actual relative energy spacing."""
    return BASE_Y + LADDER_SPAN * HYDROGEN.level_height(n)


def _ball(radius=.22):
    """A shaded, uncharged ball for the everyday analogy."""
    body = Circle(radius=radius, stroke_color='#FFDF95', stroke_width=1.1,
                  fill_color='#B57822', fill_opacity=1)
    shades = VGroup(*[
        Circle(radius=radius*size, stroke_width=0, fill_color=color, fill_opacity=1)
        .shift(LEFT*radius*.12+UP*radius*.14)
        for size, color in ((.88, '#D9A340'), (.65, '#F4C66A'), (.40, '#FFE6A7'))
    ])
    glint = Ellipse(width=radius*.45, height=radius*.22, stroke_width=0,
                    fill_color=cfg.WHITE, fill_opacity=.7).shift(LEFT*radius*.28+UP*radius*.48)
    return VGroup(body, shades, glint)


def _ramp():
    a, b = np.array([LEFT_X, TREAD_Y[0], 0]), np.array([RIGHT_X, TREAD_Y[-1], 0])
    foot = np.array([RIGHT_X, -2.3, 0])
    front = Polygon(a, b, foot, [LEFT_X, -2.3, 0], stroke_color='#37708A',
                    stroke_width=1.1, fill_color='#174963', fill_opacity=1)
    end = Polygon(b, b+DEPTH, foot+DEPTH, foot, stroke_color='#28566D',
                  stroke_width=1, fill_color='#102F43', fill_opacity=1)
    surface = Polygon(a, b, b+DEPTH, a+DEPTH, stroke_color='#8FDDF1',
                      stroke_width=1.8, fill_color='#4A9AB3', fill_opacity=1)
    edge = Line(a, b, color='#BDEFF6', stroke_width=2.4)
    normal = np.array([-(b-a)[1], (b-a)[0], 0]); normal /= np.linalg.norm(normal)
    def resting_point(fraction):
        return a+(b-a)*fraction+DEPTH*.5+normal*.22
    return VGroup(front, end, surface, edge), resting_point


def _stairs():
    """Solid front risers and illuminated top faces, all in a fixed oblique view."""
    faces, edges, seats = VGroup(), VGroup(), []
    for i, y in enumerate(TREAD_Y):
        x1, x2 = LEFT_X+1.6*i, LEFT_X+1.6*(i+1)
        a, b = np.array([x1, y, 0]), np.array([x2, y, 0])
        front = Polygon([x1, -2.3, 0], [x2, -2.3, 0], b, a,
                        stroke_color='#34738D', stroke_width=1,
                        fill_color=('#16445D', '#1B516B', '#205A74', '#24627C')[i], fill_opacity=1)
        top = Polygon(a, b, b+DEPTH, a+DEPTH, stroke_color='#84D6E9', stroke_width=1.3,
                      fill_color=('#39829F', '#408EAA', '#479CB4', '#52ADC1')[i], fill_opacity=1)
        if i == 3:
            side = Polygon(b, b+DEPTH, [x2+DEPTH[0], -2.3+DEPTH[1], 0], [x2, -2.3, 0],
                           stroke_color='#2F647A', stroke_width=1, fill_color='#102D40', fill_opacity=1)
            faces.add(side)
        faces.add(front, top)
        edges.add(Line(a, b, color='#B7F0FA', stroke_width=3))
        seats.append((a+b)/2+DEPTH*.5+UP*.22)
    return faces, edges, seats


class Scene10EnergyFloors(Scene):
    def construct(self):
        play_scene(self)


def play_scene(scene):
    started = begin_scene(scene, '10')
    add_cinematic_background(scene)

    # Any supported height on the ramp. The narration supplies the explanation.
    ramp, resting_point = _ramp()
    ball = _ball().move_to(resting_point(.08))
    paced_play(scene, FadeIn(ramp, shift=UP*.08), run_time=1.2)
    paced_play(scene, FadeIn(ball), run_time=.6)
    for fraction in (.38, .77, .23, .90):
        paced_play(scene, ball.animate.move_to(resting_point(fraction)), run_time=1.25,
                   rate_func=rate_functions.ease_in_out_sine)
        narration_wait(scene, .7)
    narration_wait(scene, 2.0)

    # Replace the slope with substantial, shaded steps rather than an outline.
    faces, edges, seats = _stairs()
    paced_play(scene, FadeOut(ramp, ball), run_time=.6)
    paced_play(scene, LaggedStart(*[FadeIn(face, shift=UP*.08) for face in faces], lag_ratio=.07),
               FadeIn(edges), run_time=1.4)
    ball.move_to(seats[3])
    paced_play(scene, FadeIn(ball), run_time=.5)
    for index in (2, 1, 0):
        # An arcing move clears the step before the ball settles on its tread.
        arc = CubicBezier(ball.get_center(), ball.get_center()+UP*.8+LEFT*.3,
                          seats[index]+UP*1.35+RIGHT*.15, seats[index])
        paced_play(scene, MoveAlongPath(ball, arc), run_time=1.1)
        paced_play(scene, Indicate(edges[index], color=cfg.GOLD, scale_factor=1.0), run_time=.7)
        narration_wait(scene, .9)
    narration_wait(scene, 2.0)

    # Emphasise the four supported heights without another sentence slide.
    for edge in edges:
        paced_play(scene, Indicate(edge, color=cfg.GOLD, scale_factor=1.0), run_time=.85)
        narration_wait(scene, .4)
    narration_wait(scene, 2.6)

    # Remove the physical staircase. What remains is an abstract energy diagram.
    paced_play(scene, FadeOut(faces, ball), run_time=.8)
    abstract = VGroup(*[
        Line([-3.15, y, 0], [4.25, y, 0], color=cfg.CYAN, stroke_width=3)
        for y in (-1.8, -.6, .6, 1.8)
    ])
    paced_play(scene, Transform(edges, abstract), run_time=2)
    state = electron(.22).move_to([-2.35, -1.8, 0])
    paced_play(scene, FadeIn(state), run_time=.6)
    impossible = electron(.22).fade(.65).move_to([-2.35, 0, 0])
    cross = cross_mark(.22, cfg.RED).next_to(impossible, RIGHT, buff=.25)
    paced_play(scene, FadeIn(impossible, cross), run_time=.7)
    narration_wait(scene, 2)
    paced_play(scene, FadeOut(impossible, cross), run_time=.7)
    narration_wait(scene, 2.3)

    # Real hydrogen spacing replaces the equally spaced analogy.
    title = outlined_text('HYDROGEN', 36, cfg.GOLD).move_to([0, 3.35, 0])
    paced_play(scene, FadeIn(title), run_time=.6)
    target = VGroup(*[
        Line([-3.15, level_y(n), 0], [4.25, level_y(n), 0], color=cfg.CYAN, stroke_width=3)
        for n in (1, 2, 3, 4)
    ])
    paced_play(scene, Transform(edges, target), state.animate.move_to([-2.35, level_y(1), 0]), run_time=2)
    labels = {n: eq(rf'n={n}', '#C7E7F3', 38).move_to([-3.95, level_y(n), 0]) for n in LABELLED_LEVELS}
    ground = outlined_text('GROUND STATE', cfg.FONT['small'], cfg.GREEN).move_to([-4.85, level_y(1)-.62, 0])
    paced_play(scene, FadeIn(labels[1], ground), run_time=.8)
    narration_wait(scene, 1)
    paced_play(scene, FadeOut(title), run_time=.6)
    for n in (2, 3):
        paced_play(scene, FadeIn(labels[n]), Indicate(edges[n-1], color=cfg.GOLD, scale_factor=1.0), run_time=1.2)
        narration_wait(scene, 1.5)

    comb = VGroup(*[
        Line([-3.15, level_y(n), 0], [4.25, level_y(n), 0], color=cfg.CYAN,
             stroke_width=2, stroke_opacity=.5)
        for n in COMB_LEVELS if n > 4
    ])
    paced_play(scene, LaggedStart(*[FadeIn(rung) for rung in comb], lag_ratio=.25), run_time=1.6)
    limit = ionisation_line(BASE_Y+LADDER_SPAN, line_width=7.4, color='#C8B0FF').shift(RIGHT*.55)
    paced_play(scene, FadeIn(limit), run_time=.8)
    paced_play(scene, Indicate(comb, color=cfg.GOLD, scale_factor=1.0), run_time=1.2)
    narration_wait(scene, 2.5)

    # Time passes with the electron remaining in its stationary ground state.
    clock_centre = np.array([5.3, -.9, 0])
    clock = VGroup(Circle(radius=.5, color=cfg.MUTED, stroke_width=1.6, stroke_opacity=.7),
                   Dot(radius=.035, color=cfg.CYAN)).move_to(clock_centre)
    hand = Line(clock_centre, clock_centre+UP*.36, color=cfg.CYAN, stroke_width=2)
    paced_play(scene, FadeIn(clock, hand), run_time=.8)
    paced_play(scene, Rotate(hand, angle=-TAU*2, about_point=clock_centre), run_time=12, rate_func=linear)
    paced_play(scene, FadeOut(clock, hand), run_time=.7)
    narration_wait(scene, 8.3)

    # The arrows show energy changes; the electron occupies only the end states.
    up = Arrow([-.8, level_y(1), 0], [-.8, level_y(3), 0], color=cfg.GOLD,
               buff=.1, stroke_width=4, max_tip_length_to_length_ratio=.08)
    excited = electron(.22).move_to([-2.35, level_y(3), 0])
    paced_play(scene, GrowArrow(up), Succession(FadeOut(state, run_time=.8), FadeIn(excited, run_time=.8)), run_time=1.6)
    narration_wait(scene, 4)
    paced_play(scene, FadeOut(up), run_time=.5)
    lower = electron(.22).move_to([-2.35, level_y(2), 0])
    color = HYDROGEN.color(3, 2)
    down = Arrow([-.8, level_y(3), 0], [-.8, level_y(2), 0], color=color,
                 buff=.06, stroke_width=4, max_tip_length_to_length_ratio=.22)
    paced_play(scene, GrowArrow(down), Succession(FadeOut(excited, run_time=.4), FadeIn(lower, run_time=.4)), run_time=.8)
    light = photon([-1.6, level_y(2), 0], [-.4, level_y(2), 0], wavelength=.5, color=color, amplitude=.15)
    paced_play(scene, FadeIn(light), run_time=.4)
    paced_play(scene, light.animate.shift(RIGHT*5.4), run_time=3.2, rate_func=linear)
    paced_play(scene, FadeOut(light, down), run_time=.5)
    narration_wait(scene, 2)
    end_scene(scene, started, cfg.SCENE_DURATIONS['10'])
