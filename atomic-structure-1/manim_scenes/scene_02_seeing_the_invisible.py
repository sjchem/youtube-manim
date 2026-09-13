"""Scene 02: the dark room. How do you learn the shape of something you cannot see?"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    dark_room_background,
    end_scene,
    fit_width,
    glow_dot,
    halo,
    narration_wait,
    outlined_text,
    paced_play,
    polyline,
    top_caption,
)
from utils.physics_models import HiddenObject

ROOM = HiddenObject(center=(1.15, 0.0), radius=1.28)
SLOW_SHOTS = (-2.30, -0.95, 0.05)
FAST_SHOTS = (
    -2.70, -2.05, -1.55, -1.15, -0.90, -0.72, -0.38, -0.12,
    0.20, 0.32, 0.66, 0.85, 0.98, 1.18, 1.90, 2.55,
)


def _ball(color: str = cfg.CYAN, radius: float = 0.11) -> VGroup:
    return VGroup(halo(radius, color, layers=3, peak_opacity=0.18), Dot(ORIGIN, radius=radius, color=color))


def _throw(scene: Scene, launch_height: float, color: str, run_time: float, trail_opacity: float = 0.55) -> np.ndarray | None:
    """Fire one ball, leave its track behind, and return where it struck."""
    points = ROOM.path_points(launch_height)
    track = polyline(points, color, stroke_width=3.4, smooth=False).set_stroke(opacity=trail_opacity)
    ball = _ball(color)
    ball.move_to([points[0][0], points[0][1], 0.0])
    scene.add(ball)
    scene.play(
        MoveAlongPath(ball, track),
        Create(track),
        run_time=run_time,
        rate_func=linear,
    )
    scene.remove(ball)
    impact = ROOM.impact_point(launch_height)
    return impact


class Scene02SeeingTheInvisible(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "02")
    room = dark_room_background()
    scene.add(room)

    # -- Beat 1: there is something in here, and you will never see it --------
    prompt = top_caption("A COMPLETELY DARK ROOM", cfg.MUTED)
    paced_play(scene, FadeIn(prompt), run_time=0.9)
    hidden = Circle(
        radius=ROOM.radius,
        color=cfg.GRAY,
        stroke_width=0,
        fill_color="#0A1A24",
        fill_opacity=1.0,
    ).move_to([ROOM.center[0], ROOM.center[1], 0.0])
    scene.add(hidden)
    unseen = outlined_text("something is in it", cfg.FONT["body"], cfg.GRAY)
    unseen.move_to([0, -3.0, 0])
    paced_play(scene, FadeIn(unseen), run_time=0.9)
    narration_wait(scene, 4.6)
    paced_play(scene, FadeOut(unseen), run_time=0.6)

    # -- Beat 2: throw one ball at a time, and watch what comes back ----------
    method = bottom_caption("so throw something at it", cfg.GOLD)
    paced_play(scene, FadeIn(method), run_time=0.7)

    marks = VGroup()
    callouts = {0: ("STRAIGHT THROUGH", cfg.MUTED), 1: ("IT CAME BACK", cfg.GOLD)}
    for index, height in enumerate(SLOW_SHOTS):
        impact = _throw(scene, height, cfg.CYAN, run_time=3.0 - 0.3 * index)
        if impact is not None:
            spark = glow_dot([impact[0], impact[1], 0.0], cfg.GOLD, 0.075)
            marks.add(spark)
            paced_play(scene, FadeIn(spark, scale=1.6), run_time=0.45)
        if index in callouts:
            text, tone = callouts[index]
            note = outlined_text(text, cfg.FONT["small"], tone)
            note.move_to([-4.4, 2.55 if index == 0 else -2.35, 0])
            paced_play(scene, FadeIn(note, shift=UP * 0.12), run_time=0.6)
            narration_wait(scene, 2.2)
            paced_play(scene, FadeOut(note), run_time=0.4)
        narration_wait(scene, 1.5)

    paced_play(scene, FadeOut(method), run_time=0.5)
    read_out = bottom_caption("misses and bounces both constrain the hidden shape", cfg.GOLD)
    paced_play(scene, FadeIn(read_out), run_time=0.7)
    narration_wait(scene, 3.0)
    paced_play(scene, FadeOut(read_out), run_time=0.5)

    # -- Beat 3: many balls, and the edge starts to draw itself ---------------
    for height in FAST_SHOTS:
        impact = _throw(scene, height, cfg.BLUE, run_time=0.80, trail_opacity=0.30)
        if impact is not None:
            marks.add(glow_dot([impact[0], impact[1], 0.0], cfg.GOLD, 0.07))
    scene.add(marks)
    pattern = bottom_caption("every bounce records one point on a surface", cfg.GOLD)
    paced_play(scene, FadeIn(pattern), run_time=0.7)
    paced_play(scene, LaggedStart(*[Indicate(mark, color=cfg.WHITE, scale_factor=1.5) for mark in marks], lag_ratio=0.12), run_time=2.6)
    narration_wait(scene, 3.4)
    paced_play(scene, FadeOut(pattern), run_time=0.5)

    # -- Beat 4: the shape was never seen, only inferred ----------------------
    outline = DashedVMobject(
        Circle(radius=ROOM.radius, color=cfg.GREEN, stroke_width=6).move_to([ROOM.center[0], ROOM.center[1], 0.0]),
        num_dashes=48,
    )
    paced_play(scene, Create(outline), run_time=2.8)
    revealed = Circle(
        radius=ROOM.radius,
        color=cfg.GREEN,
        stroke_width=4,
        fill_color=cfg.GREEN,
        fill_opacity=0.18,
    ).move_to([ROOM.center[0], ROOM.center[1], 0.0])
    paced_play(scene, FadeIn(revealed), FadeOut(marks), run_time=1.1)
    verdict = bottom_caption("the paths reveal clues to the hidden shape", cfg.GREEN)
    paced_play(scene, FadeIn(verdict), run_time=0.8)
    narration_wait(scene, 4.7)

    # -- Beat 5: this is the whole story of the atom --------------------------
    paced_play(scene, FadeOut(verdict, prompt), run_time=0.6)
    bridge = outlined_text("we could not look inside an atom", cfg.FONT["body"], cfg.WHITE)
    bridge_2 = outlined_text("so we disturbed it, and watched what came back", cfg.FONT["body"], cfg.GOLD)
    stack = VGroup(bridge, bridge_2).arrange(DOWN, buff=0.42).move_to([0, -2.75, 0])
    for line in stack:
        fit_width(line, cfg.SAFE_WIDTH - 0.8)
    paced_play(scene, FadeIn(bridge, shift=UP * 0.15), run_time=0.9)
    paced_play(scene, FadeIn(bridge_2, shift=UP * 0.15), run_time=0.9)
    narration_wait(scene, 4.6)

    end_scene(scene, started, cfg.SCENE_DURATIONS["02"], fade_background=True)
    add_cinematic_background(scene)
