"""Read scattering visually, then pull back from a photographed cricket ball."""
from __future__ import annotations

from pathlib import Path
import numpy as np
from manim import *
import config as cfg
from manim_scenes.common import (
    add_cinematic_background, begin_scene, end_scene, eq, glow_dot,
    narration_wait, outlined_text, paced_play, rutherford_atom,
)
from utils.physics_models import AtomicScale

# Representative order-of-magnitude example, not a universal nuclear radius.
# 0.036 m * (1.4e-10 m / 1e-15 m) = 5.04 km, rounded to about five.
SCALE = AtomicScale(atom_radius=1.4e-10)
BALL_PHOTO = Path(__file__).resolve().parents[1] / 'assets/images/cricket_ball.png'


def _cue(text, color):
    return outlined_text(text, 40, color).move_to([3.55, 0.25, 0])


def _packet(scene, path, run_time=2.2):
    """A moving particle and a quiet trail; no sentence caption needed."""
    packet = glow_dot(path.get_start(), cfg.GOLD, 0.065)
    scene.add(packet)
    paced_play(scene, Create(path), MoveAlongPath(packet, path),
               run_time=run_time, rate_func=linear)
    paced_play(scene, FadeOut(packet), path.animate.set_stroke(opacity=0.12), run_time=0.4)


class Scene07EmptySpace(Scene):
    def construct(self):
        play_scene(self)


def play_scene(scene):
    started = begin_scene(scene, '07')
    add_cinematic_background(scene)
    centre = np.array([-2.6, 0.0, 0.0])
    atom, core, beads = rutherford_atom(atom_radius=2.15, nucleus_radius=0.18, electron_count=5)
    atom.move_to(centre)
    atom[0].set_stroke(cfg.CYAN, width=2.5, opacity=0.65)
    cue = _cue('Mostly open space', cfg.CYAN)
    paced_play(scene, Create(atom[0]), FadeIn(cue), run_time=1.2)
    paths = VGroup(*[
        Line([-5.8, y, 0], [0.3, y, 0], color=cfg.GOLD, stroke_width=2)
        for y in (1.25, -0.85)
    ])
    for path in paths:
        _packet(scene, path)
    paced_play(scene, FadeOut(cue), run_time=0.6)
    narration_wait(scene, 3.1)

    cue = _cue('Positive core', cfg.ORANGE)
    positive = outlined_text('+', 32, cfg.WHITE).move_to(centre)
    paced_play(scene, FadeIn(core, positive, cue), run_time=0.8)
    bent = CubicBezier(
        [-5.8, 0.45, 0], [-2.2, 0.45, 0], [-2.0, 1.0, 0], [-3.9, 2.6, 0],
        color=cfg.ORANGE, stroke_width=3,
    )
    _packet(scene, bent, 3.0)
    paced_play(scene, Indicate(core, color=cfg.GOLD, scale_factor=1.4), run_time=1.0)
    narration_wait(scene, 2)
    paced_play(scene, FadeOut(cue), run_time=0.6)

    cue = _cue('Tiny target', cfg.RED)
    target = Circle(radius=0.8, color=cfg.RED, stroke_width=2).move_to(centre)
    paced_play(scene, FadeIn(cue), Create(target), run_time=0.8)
    paced_play(scene, target.animate.scale(0.3), run_time=2)
    narration_wait(scene, 3.5)
    paced_play(scene, FadeOut(cue, target, paths, bent, positive), run_time=0.8)

    # Carry the same atom into the nucleus explanation instead of a text slide.
    name = outlined_text('NUCLEUS', 44, cfg.RED).move_to([3.55, 0.5, 0])
    mass = outlined_text('Nearly all the mass', 30, cfg.WHITE).next_to(name, DOWN, buff=0.3)
    paced_play(scene, FadeIn(name), Indicate(core, color=cfg.GOLD), run_time=1)
    paced_play(scene, FadeIn(beads, mass), run_time=1.5)
    narration_wait(scene, 3)
    paced_play(scene, FadeOut(name, mass), run_time=0.8)
    narration_wait(scene, 5)

    paced_play(scene, atom.animate.scale(0.80).move_to([-4.2, 0.3, 0]), run_time=1.3)
    atom_size = eq(r'r_{\rm atom}\sim 10^{-10}\,\mathrm{m}', '#B8F3FF', 64)
    nucleus_size = eq(r'r_{\rm nucleus}\sim 10^{-15}\,\mathrm{m}', '#FF989B', 64)
    sizes = VGroup(atom_size, nucleus_size).arrange(DOWN, buff=0.65).move_to([2.1, 0.75, 0])
    radius = Line(core.get_center(), core.get_center()+RIGHT*1.72, color=cfg.CYAN, stroke_width=4)
    paced_play(scene, FadeIn(atom_size), Create(radius), run_time=1)
    narration_wait(scene, 3)
    paced_play(scene, FadeIn(nucleus_size), Indicate(core, color=cfg.RED, scale_factor=1.5), run_time=1)
    ratio = eq(r'\approx 100{,}000\times', cfg.GOLD, 58).move_to([2.1, -1.5, 0])
    narration_wait(scene, 2)
    paced_play(scene, FadeIn(ratio), run_time=0.8)
    narration_wait(scene, 8)
    paced_play(scene, FadeOut(atom, sizes, ratio, radius), run_time=0.8)

    # Use the existing transparent photograph unchanged, preserving its aspect ratio.
    # At 2K its displayed ball is about the source's native 325-pixel diameter.
    ball = ImageMobject(str(BALL_PHOTO)).set_height(2.2)
    ball_name = outlined_text('Imagine this as the nucleus', 34, cfg.GOLD).move_to([0, -1.9, 0])
    paced_play(scene, FadeIn(ball, scale=0.92), FadeIn(ball_name), run_time=1.5)
    narration_wait(scene, 3)
    paced_play(scene, FadeOut(ball_name), ball.animate.shift(UP*0.12), run_time=1)
    narration_wait(scene, 7.5)

    # The photo shrinks continuously into the centre marker: no disconnected cut.
    centre = np.array([-2.6, 0.0, 0.0])
    paced_play(scene, ball.animate.set_height(0.20).move_to(centre), run_time=3,
               rate_func=rate_functions.ease_in_out_sine)
    speck = glow_dot(centre, cfg.RED, 0.045)
    outer = DashedVMobject(Circle(radius=2.65, color=cfg.CYAN, stroke_width=2).move_to(centre), num_dashes=64)
    paced_play(scene, FadeOut(ball), FadeIn(speck), Create(outer), run_time=2.5)

    # A quiet street-grid motif makes the walk relatable without implying a real map.
    blocks = VGroup()
    for x in np.arange(-4.65, -0.3, 0.65):
        for y in np.arange(-1.65, 2.0, 0.65):
            if np.linalg.norm(np.array([x+0.22, y, 0])-centre) < 2.3 and abs(y) > 0.4:
                blocks.add(RoundedRectangle(width=0.44, height=0.40, corner_radius=0.05,
                    stroke_color=cfg.CYAN, stroke_width=0.7, stroke_opacity=0.13,
                    fill_color=cfg.CYAN, fill_opacity=0.025).move_to([x, y, 0]))
    route = Line(centre, centre+RIGHT*2.65, color=cfg.GOLD, stroke_width=4)
    marker = Dot(centre, radius=0.06, color=cfg.WHITE)
    info = VGroup(
        outlined_text(f'About {SCALE.cricket_ball_atom_radius_km:.0f} km', 62, cfg.GOLD),
        outlined_text('Centre to edge', 30, cfg.WHITE),
    ).arrange(DOWN, buff=0.30).move_to([3.6, 0.3, 0])
    paced_play(scene, FadeIn(blocks, marker, info), run_time=1.0)
    paced_play(scene, Create(route), marker.animate.move_to(route.get_end()), run_time=12, rate_func=linear)
    narration_wait(scene, 2)
    paced_play(scene, FadeOut(info), run_time=0.8)
    # Soften the size guide as the narration explains that it is not a wall.
    paced_play(scene, outer.animate.set_stroke(opacity=0.18), run_time=2)
    narration_wait(scene, 5.5)
    paced_play(scene, FadeOut(blocks, outer, route, marker, speck), run_time=0.8)

    # End with a visual region populated by electrons and electric-field cues.
    final_atom, final_core, final_electrons = rutherford_atom(atom_radius=2.55, nucleus_radius=0.18, electron_count=5)
    final_atom.shift(LEFT*2.2)
    fields = VGroup(*[
        Arrow(final_core.get_center()+0.48*np.array([np.cos(a), np.sin(a), 0]),
              final_core.get_center()+1.45*np.array([np.cos(a), np.sin(a), 0]),
              buff=0, color=cfg.ORANGE, stroke_width=1.5, max_tip_length_to_length_ratio=0.12)
        for a in np.linspace(0, TAU, 10, endpoint=False)
    ]).set_opacity(0.3)
    final_cue = _cue('Electrons + fields', cfg.CYAN)
    paced_play(scene, FadeIn(final_atom, fields, final_cue), run_time=1.2)
    narration_wait(scene, 3)
    paced_play(scene, FadeOut(final_cue), run_time=0.8)
    paced_play(scene, final_atom.animate.shift(RIGHT*2.2), fields.animate.shift(RIGHT*2.2), run_time=1.5)
    paced_play(scene, LaggedStart(*[Indicate(e, color=cfg.CYAN, scale_factor=1.25)
                                   for e in final_electrons], lag_ratio=0.4), run_time=4)
    narration_wait(scene, 6)
    end_scene(scene, started, cfg.SCENE_DURATIONS['07'])
