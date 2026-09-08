"""Scene 11: two numbers in, one number out - the same idea, in three dimensions."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    bottom_caption,
    clear_background,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    outlined_text,
    paced_play,
)
from utils.physics_models import descent_path, loss_surface
from utils.render_helpers import fit_width

X_RANGE = (-2.8, 2.8)
Y_RANGE = (-2.8, 2.8)
Z_RANGE = (-2.5, 4.5)


class Scene11HigherDimensions(ThreeDScene):
    """The machine grows a second input slot, and the graph becomes a landscape."""

    def construct(self) -> None:
        play_scene(self)


def _fix(scene: Scene, *mobjects: Mobject) -> None:
    """Pin overlays to the screen, whichever camera this scene happens to own."""
    pin = getattr(scene, "add_fixed_in_frame_mobjects", None)
    if pin is None:
        scene.add(*mobjects)
    else:
        pin(*mobjects)


def _unfix(scene: Scene, *mobjects: Mobject) -> None:
    release = getattr(scene, "remove_fixed_in_frame_mobjects", None)
    if release is not None:
        release(*mobjects)


def _glowing_ball(point: np.ndarray) -> VGroup:
    """Layer translucent 3D shells around a bright, shaded core."""
    outer_halo = Dot3D(point, radius=0.27, color=cfg.GOLD, resolution=(10, 10))
    outer_halo.set_opacity(0.08)
    middle_halo = Dot3D(point, radius=0.20, color="#FFE8A3", resolution=(10, 10))
    middle_halo.set_opacity(0.20)
    core = Dot3D(point, radius=0.14, color="#FFF8D8", resolution=(14, 14))
    core.set_sheen(0.65, UL)
    return VGroup(outer_halo, middle_halo, core)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "11")
    # A flat background plane would tilt with the camera, so this chapter runs
    # on the deep Oceanic clear colour alone.
    clear_background(scene)

    # Open on the front view (phi = 90 degrees): screen-right is x, screen-up is
    # z, and the y axis points straight into the screen. A curve drawn in the
    # x-z plane therefore reads as an ordinary 2D graph until the camera tilts.
    # The lifted focus point keeps the landscape clear of both caption lanes.
    scene.set_camera_orientation(
        phi=90 * DEGREES,
        theta=-90 * DEGREES,
        zoom=1.15,
        frame_center=[0.0, 0.0, 0.75],
    )

    axes = ThreeDAxes(
        x_range=[X_RANGE[0], X_RANGE[1], 1],
        y_range=[Y_RANGE[0], Y_RANGE[1], 1],
        z_range=[Z_RANGE[0], Z_RANGE[1], 2],
        x_length=7.0,
        y_length=7.0,
        z_length=3.1,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.4},
        tips=False,
    )

    prompt = outlined_text("One number in. One number out.", cfg.FONT["body"], cfg.CYAN)
    fit_width(prompt, cfg.SAFE_WIDTH - 1.2)
    prompt.to_edge(UP, buff=0.42)
    signature = eq(r"y=f(x)", cfg.CYAN, cfg.FONT["title"])
    signature.to_edge(DOWN, buff=0.45)

    # --- Start with the curve we already know, drawn where it actually lives.
    known = ParametricFunction(
        lambda t: axes.c2p(t, 0.0, loss_surface(t, 0.0)),
        t_range=[-2.6, 2.6],
        color=cfg.WHITE,
        stroke_width=6,
    )

    _fix(scene, prompt, signature)
    paced_play(scene, FadeIn(prompt, shift=DOWN * 0.2), run_time=0.9)
    paced_play(scene, Create(axes), run_time=1.6)
    paced_play(scene, Create(known), FadeIn(signature, shift=UP * 0.2), run_time=1.8)
    narration_wait(scene, 6.5)

    # --- Tilt into three dimensions: the curve was always a slice.
    scene.move_camera(phi=62 * DEGREES, theta=-58 * DEGREES, run_time=3.4)
    narration_wait(scene, 4.5)
    paced_play(scene, Indicate(known, color=cfg.GOLD, scale_factor=1.0), run_time=1.2)
    narration_wait(scene, 3.5)

    # --- Only now does the second input slot appear.
    second_prompt = outlined_text("What if a machine takes two numbers?", cfg.FONT["body"], cfg.CYAN)
    fit_width(second_prompt, cfg.SAFE_WIDTH - 1.2)
    second_prompt.to_edge(UP, buff=0.42)
    second_slot = eq(r"z=f(x,y)", cfg.WHITE, cfg.FONT["title"])
    second_slot.to_edge(DOWN, buff=0.45)
    _fix(scene, second_prompt, second_slot)
    paced_play(
        scene,
        FadeOut(prompt),
        FadeIn(second_prompt, shift=DOWN * 0.2),
        FadeOut(signature),
        FadeIn(second_slot, shift=UP * 0.2),
        run_time=1.0,
    )
    narration_wait(scene, 7.5)
    prompt = second_prompt
    signature = second_slot

    surface = Surface(
        lambda u, v: axes.c2p(u, v, loss_surface(u, v)),
        u_range=list(X_RANGE),
        v_range=list(Y_RANGE),
        resolution=(12, 12) if config.pixel_height <= 480 else (26, 26),
        fill_opacity=0.86,
        stroke_width=0.7,
        stroke_color=cfg.CYAN,
        checkerboard_colors=["#0E4F80", "#093A60"],
    )
    paced_play(scene, Create(surface), run_time=4.0)
    # Keep the highlighted slice visible above the translucent surface faces.
    known.set_z_index(10)
    scene.bring_to_front(known)
    scene.wait(9.5)

    caption = bottom_caption("Every point on the floor is one input pair.", cfg.GOLD)
    _fix(scene, caption)
    paced_play(scene, FadeOut(signature), FadeIn(caption, shift=UP * 0.2), run_time=0.8)

    # --- One input pair, one height. That is the whole story again.
    sample = (-2.3, 2.1)
    floor_dot = Dot3D(axes.c2p(sample[0], sample[1], 0), radius=0.1, color=cfg.INPUT_COLOR)
    height = loss_surface(*sample)
    lift = DashedLine(
        axes.c2p(sample[0], sample[1], 0),
        axes.c2p(sample[0], sample[1], height),
        color=cfg.GOLD,
        stroke_width=4,
        dash_length=0.14,
    )
    top_dot = Dot3D(axes.c2p(sample[0], sample[1], height), radius=0.1, color=cfg.OUTPUT_COLOR)
    paced_play(scene, FadeOut(known), FadeIn(floor_dot, scale=1.6), run_time=0.7)
    paced_play(scene, Create(lift), run_time=1.0)
    paced_play(scene, FadeIn(top_dot, scale=1.6), run_time=0.6)
    narration_wait(scene, 6.0)

    readout = eq(r"(x,y) \rightarrow \text{height}", cfg.GOLD, cfg.FONT["body"])
    readout.to_edge(UP, buff=0.42)
    _fix(scene, readout)
    paced_play(scene, FadeOut(prompt), FadeIn(readout, shift=DOWN * 0.2), run_time=0.8)
    narration_wait(scene, 5.5)

    # --- Learning, seen as walking downhill on a function.
    new_caption = bottom_caption("An illustrative loss: lower means a better fit.", cfg.PURPLE)
    _fix(scene, new_caption)
    paced_play(scene, FadeOut(caption), FadeIn(new_caption, shift=UP * 0.2), run_time=0.8)
    caption = new_caption

    scene.begin_ambient_camera_rotation(rate=0.06)
    path_points = descent_path(sample, steps=48, learning_rate=0.3)
    walker = _glowing_ball(axes.c2p(*path_points[0]))
    paced_play(scene, FadeOut(VGroup(floor_dot, lift, top_dot)), FadeIn(walker, scale=1.4), run_time=0.9)

    corners = [axes.c2p(*point) for point in path_points]
    trail_curve = VMobject(color=cfg.GOLD, stroke_width=5).set_points_as_corners(corners)
    paced_play(
        scene,
        Create(trail_curve),
        MoveAlongPath(walker, trail_curve),
        run_time=6.5,
        rate_func=rate_functions.ease_in_out_sine,
    )
    narration_wait(scene, 5.0)

    valley = glow_dot(corners[-1], cfg.GREEN, radius=0.11)
    paced_play(scene, FadeIn(valley, scale=1.6), run_time=0.8)
    narration_wait(scene, 9.5)
    scene.stop_ambient_camera_rotation()

    # --- Land the point: it is still input, rule, output.
    closing = eq(r"(x,y) \rightarrow f \rightarrow z", cfg.WHITE, cfg.FONT["title"])
    closing.to_edge(UP, buff=0.42)
    _fix(scene, closing)
    paced_play(scene, FadeOut(readout), FadeIn(closing, shift=DOWN * 0.2), run_time=0.9)
    final_caption = bottom_caption("More inputs. Same idea.", cfg.GOLD)
    _fix(scene, final_caption)
    paced_play(scene, FadeOut(caption), FadeIn(final_caption, shift=UP * 0.2), run_time=0.8)
    narration_wait(scene, 6.0)

    # Return the camera to Manim's default 2D orientation, so the next chapter
    # of the full cut starts square to the screen.
    scene.move_camera(
        phi=0.0,
        theta=-90 * DEGREES,
        zoom=1.0,
        frame_center=[0.0, 0.0, 0.0],
        run_time=1.8,
    )
    # Keep overlays pinned through the closing fade; release them afterwards.

    end_scene(scene, started, cfg.SCENE_DURATIONS["11"])
    fixed = list(getattr(scene.camera, "fixed_in_frame_mobjects", ()))
    if fixed:
        _unfix(scene, *fixed)
