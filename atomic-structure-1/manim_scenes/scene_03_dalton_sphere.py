"""Scene 03: divide a 3D solid, then reveal Dalton's rotating solid-atom model."""
from __future__ import annotations

import itertools
import numpy as np
from manim import *
import config as cfg
from manim_scenes.common import (
    add_cinematic_background, begin_scene, bottom_caption, check_mark, chip,
    discharge_tube, end_scene, eq, fit_width, glow_dot, halo, hide_background,
    move_3d_view, narration_wait, orbit_hold, outlined_text, paced_play,
    pin_to_frame, restore_background, set_3d_view, stage_banner, top_caption,
    unpin_from_frame,
)

BLOCK_SIZE = 2.8
SPIN_AXIS = np.array([0.25, 1.0, 0.35])
SPIN_RATE = 0.34


def _matter_cube(side: float = BLOCK_SIZE) -> Cube:
    """A solid with shaded faces, rather than a translucent flat square."""
    cube = Cube(side_length=side, fill_opacity=1, stroke_width=1.3,
                stroke_color=cfg.CYAN, fill_color=cfg.BLUE)
    face_colors = ("#2388AD", "#1B5B88", "#54B8D0", "#206F9C", "#7DD9E5", "#18466E")
    for face, color in zip(cube, face_colors):
        face.set_fill(color, opacity=1)
    return cube


def _divide_and_follow(scene: Scene, block: Cube, intro: tuple[Mobject, ...] = ()) -> Cube:
    """Partition a cube into eight actual eighth-volume pieces, then zoom in."""
    planes = VGroup()
    for axis in (RIGHT, UP, OUT):
        plane = Square(side_length=BLOCK_SIZE + 0.35, color=cfg.GOLD,
                       stroke_width=2.2, fill_color=cfg.CYAN, fill_opacity=0.07)
        if np.allclose(axis, RIGHT):
            plane.rotate(PI / 2, axis=UP)
        elif np.allclose(axis, UP):
            plane.rotate(PI / 2, axis=RIGHT)
        planes.add(plane)
    clear_intro = [FadeOut(*intro)] if intro else []
    paced_play(scene, LaggedStart(*[Create(plane) for plane in planes], lag_ratio=0.3),
               *clear_intro, run_time=1.0)
    if intro:
        unpin_from_frame(scene, *intro)

    offsets = [np.array(signs) * BLOCK_SIZE / 4 for signs in itertools.product((-1, 1), repeat=3)]
    pieces = [_matter_cube(BLOCK_SIZE / 2).move_to(offset) for offset in offsets]
    scene.remove(block)
    scene.add(*pieces)
    paced_play(scene, *[piece.animate.shift(offset * 0.90) for piece, offset in zip(pieces, offsets)],
               FadeOut(planes), run_time=1.1, rate_func=rate_functions.ease_in_out_sine)
    # The front/top/right piece is visible from the chosen camera angle.
    chosen = pieces[5]  # (+x, -y, +z)
    discarded = [piece for piece in pieces if piece is not chosen]
    paced_play(scene, chosen.animate.set_stroke(cfg.GOLD, width=2.5), run_time=0.4)
    paced_play(scene, *[FadeOut(piece, shift=piece.get_center() * 0.35) for piece in discarded], run_time=0.7)
    # A camera-like magnification: the selected piece was physically smaller;
    # enlarge only after its neighbours have cleared the frame.
    paced_play(scene, chosen.animate.move_to(ORIGIN).scale(2.0).set_stroke(cfg.CYAN, width=1.3),
               run_time=1.5, rate_func=rate_functions.ease_in_out_sine)
    return chosen


def _luminous_atom(radius: float = 1.20) -> VGroup:
    """Opaque historical sphere with a corona and a moving surface sheen.

    The colour variation makes rotation visible. It is decorative shading,
    not electrons, a nucleus, or an internal structure in Dalton's model.
    """
    preview = config.pixel_height <= 480
    body = Sphere(radius=radius, resolution=(12, 24) if preview else (24, 48), stroke_width=0)
    for patch in body:
        x, y, z = patch.get_center()
        longitude = np.arctan2(y, x)
        sheen = 0.5 + 0.5 * np.cos(longitude - 0.6)
        height = np.clip((z / radius + 1.0) / 2.0, 0, 1)
        patch.set_fill(interpolate_color(ManimColor("#125786"), ManimColor("#B8F3FF"),
                                        0.16 + 0.54 * sheen * height), opacity=1)
    return VGroup(body)


def _atom_aura(scene: ThreeDScene, atom: VGroup, scale: float) -> VGroup:
    """Smooth camera-facing bloom behind the sphere, with no faceted shell."""
    rotation = scene.camera.generate_rotation_matrix()
    view_normal = rotation.T @ OUT
    center = atom.get_center()
    relative = center - scene.camera.frame_center
    depth = 1.24 * scale
    z = np.dot(relative, view_normal)
    # Compensate perspective so a halo behind an off-centre sphere stays centred.
    magnification = 1.0 + depth / (scene.camera.get_focal_distance() - z)
    lateral = relative - z * view_normal
    aura = halo(1.12 * scale * magnification, cfg.CYAN, layers=9, peak_opacity=0.18)
    aura.apply_matrix(rotation.T)
    aura.shift(center - view_normal * depth + lateral * (magnification - 1.0))
    aura.set_shade_in_3d(True)
    return aura


def _molecule(spacing: float = 0.62) -> VGroup:
    """Two of one kind, one of another: chemistry's stubborn whole numbers."""
    oxygen = VGroup(halo(0.32, cfg.RED, 3, 0.16), Dot(ORIGIN, radius=0.32, color=cfg.RED))
    left = VGroup(halo(0.20, cfg.CYAN, 3, 0.16), Dot(ORIGIN, radius=0.20, color=cfg.CYAN))
    right = left.copy()
    left.move_to([-spacing, -0.36, 0])
    right.move_to([spacing, -0.36, 0])
    bonds = VGroup(
        Line(ORIGIN, left.get_center(), color=cfg.MUTED, stroke_width=5),
        Line(ORIGIN, right.get_center(), color=cfg.MUTED, stroke_width=5),
    )
    return VGroup(bonds, oxygen, left, right)


class Scene03DaltonSphere(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "03")
    add_cinematic_background(scene)
    background = hide_background(scene)
    set_3d_view(scene, phi=63 * DEGREES, theta=-55 * DEGREES)

    heading = top_caption("SMALLER AND SMALLER PIECES", cfg.GOLD)
    pin_to_frame(scene, heading)
    portrait = ImageMobject(str(cfg.PROJECT_ROOT / "assets/images/john_dalton_1835.jpg"))
    portrait.height = 3.25
    portrait.move_to([-5.25, 0.35, 0])
    border = SurroundingRectangle(portrait, buff=0.07, color=cfg.MUTED, stroke_width=1.5)
    name = outlined_text("John Dalton", cfg.FONT["small"], cfg.WHITE).next_to(portrait, DOWN, buff=0.25)
    intro = (portrait, border, name)
    pin_to_frame(scene, *intro)
    block = _matter_cube()
    paced_play(scene, FadeIn(heading), FadeIn(block, scale=0.85), FadeIn(portrait),
               FadeIn(border, name), run_time=1.2)
    orbit_hold(scene, 2.0, rate=0.07)
    for division in range(2):
        block = _divide_and_follow(scene, block, intro if division == 0 else ())
    narration_wait(scene, 1.2)

    # The last piece gives way to the model: a lit, solid sphere.
    atom = _luminous_atom()
    paced_play(scene, FadeOut(block, scale=0.2), FadeIn(atom, scale=0.2), run_time=1.8)

    # Keep rotation live during waits, camera sweeps and placement changes.
    # Animate the pose controls instead of the sphere so its updater never pauses.
    anchor = VectorizedPoint(ORIGIN)
    display_scale = ValueTracker(1.0)
    atom._display_scale = 1.0

    def turn_atom(mob, dt):
        mob.rotate(SPIN_RATE * dt, axis=SPIN_AXIS, about_point=mob.get_center())
        scale = display_scale.get_value()
        mob.scale(scale / mob._display_scale, about_point=mob.get_center())
        mob._display_scale = scale
        mob.move_to(anchor.get_center())

    atom.add_updater(turn_atom)
    aura = always_redraw(lambda: _atom_aura(scene, atom, display_scale.get_value()))
    scene.add(aura)
    label = outlined_text("ATOM", cfg.FONT["title"], cfg.WHITE).move_to([0, -2.2, 0])
    meaning = outlined_text("Dalton's solid, indivisible model", cfg.FONT["small"], cfg.MUTED).move_to([0, -3.1, 0])
    pin_to_frame(scene, label, meaning)
    paced_play(scene, FadeIn(label, shift=UP * 0.15), FadeIn(meaning), run_time=1.0)
    orbit_hold(scene, 11.0, rate=0.025)

    # Return to a flat composition; the sphere itself continues to rotate in 3D.
    paced_play(scene, FadeOut(heading, meaning), run_time=0.5)
    unpin_from_frame(scene, heading, meaning)
    move_3d_view(scene, phi=0, theta=-90 * DEGREES, run_time=1.6)
    unpin_from_frame(scene, label)
    paced_play(scene, anchor.animate.move_to([-4.15, 0.35, 0]), display_scale.animate.set_value(0.76),
               label.animate.scale(0.72).move_to([-4.15, -1.35, 0]), run_time=1.4)

    banner = stage_banner("MODEL", "one solid, indivisible ball").move_to([2.4, 2.55, 0])
    paced_play(scene, FadeIn(banner, shift=DOWN * 0.15), run_time=0.8)
    molecule = _molecule().scale(1.25).move_to([2.4, 0.85, 0])
    ratio = eq(r"2:1", cfg.GREEN, cfg.FONT["title"]).next_to(molecule, DOWN, buff=0.60)
    paced_play(scene, FadeIn(molecule, scale=1.1), run_time=1.2)
    paced_play(scene, FadeIn(ratio, shift=UP * 0.12), run_time=0.6)
    narration_wait(scene, 4.2)
    law = chip("always the same whole numbers", cfg.GREEN, cfg.FONT["tiny"]).move_to([2.4, -1.85, 0])
    paced_play(scene, FadeIn(law, shift=UP * 0.12), run_time=0.7)
    narration_wait(scene, 5.0)
    verdict = VGroup(check_mark(0.22, cfg.GREEN),
                     outlined_text("explains how elements combine", cfg.FONT["small"], cfg.GREEN))
    verdict.arrange(RIGHT, buff=0.34).move_to([2.4, -3.0, 0])
    paced_play(scene, FadeIn(verdict, shift=UP * 0.12), run_time=0.8)
    narration_wait(scene, 11.0)

    paced_play(scene, FadeOut(banner, molecule, ratio, verdict, law, label), run_time=0.7)
    paced_play(scene, anchor.animate.move_to([-4.5, 0, 0]), display_scale.animate.set_value(0.65), run_time=0.8)
    question = outlined_text("is it really indivisible?", cfg.FONT["body"], cfg.ORANGE).move_to([1.9, 2.5, 0])
    paced_play(scene, FadeIn(question, shift=DOWN * 0.15), run_time=0.8)
    narration_wait(scene, 3.6)
    tube = discharge_tube(4.6, 1.0, cfg.PURPLE).move_to([2.1, 0.1, 0])
    paced_play(scene, FadeIn(tube), run_time=1.2)
    sparks = VGroup(*[glow_dot([2.1 + x, 0.1, 0], cfg.GOLD, 0.055) for x in np.linspace(-1.7, 1.7, 7)])
    paced_play(scene, LaggedStart(*[FadeIn(spark, scale=1.6) for spark in sparks], lag_ratio=0.2), run_time=1.6)
    caption = bottom_caption("pass electricity through an almost empty tube", cfg.GOLD)
    paced_play(scene, FadeIn(caption), run_time=0.7)
    narration_wait(scene, 9.0)

    # Clear the updater before the fade so it cannot leak into the next chapter.
    atom.clear_updaters()
    aura.clear_updaters()
    scene.remove(anchor, display_scale)
    end_scene(scene, started, cfg.SCENE_DURATIONS["03"])
    restore_background(scene, background)
