"""Scene 01 — the hook. One 3D ground holds a straight road and a circular
track. A car drives the road at a steady 20 m/s: its gold velocity arrow
never changes, so a = 0. The same car then laps the track
(``physics_models.HOOK_TRACK``) at the same 20 m/s, read off the same
speedometer, while its velocity arrow keeps turning and frozen copies are
left behind. An orange arrow toward the centre answers the hook before it
is explained. Both cars run in real time, so equal speeds cover equal
distances. The title closes the scene.
"""

from manim_scenes.common import *

TRACK = pm.HOOK_TRACK
R_TRACK = 2.2                         # stage units for the track's 80 m radius
S = R_TRACK / TRACK.r                 # stage units per metre (shared by the road)
ROAD_Y = -2.9                         # the road runs east-west, near the viewer
TRACK_C = ground(0.0, 0.7)
KV = 1.15 / TRACK.v                   # a 20 m/s arrow is 1.15 stage units long
KA = 0.95 / TRACK.accel


class Scene01Hook(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "01")
    stage = field_stage((0.0, -0.55, 0), zoom=1.02, pitch=0.66, half=6.4, step=0.55)
    road_pts = np.array([ground(x, ROAD_Y) for x in np.linspace(-6.4, 6.4, 40)])
    road = Band(road_pts, 0.34, cfg.ROAD, closed=False, edge=cfg.MUTED, centre_line=cfg.WHITE)
    track = Band(ring_points(TRACK_C, R_TRACK, 120), 0.34, cfg.ROAD, edge=cfg.MUTED, centre_line=cfg.WHITE)
    track.presence = 0.0
    stage.add_body(road, track)

    # Car A on the straight road, driven by its own clock (seconds).
    drive = Knob(0.0)
    start_x = -5.6
    where_a = lambda: ground(start_x + pm.HOOK_SPEED * drive.value * S, ROAD_Y)  # noqa: E731
    car_a = car3d(stage, where_a, lambda: 0.0, cfg.CAR, 0.62)
    v_a = Vector(lambda: where_a() + UP * 0.3, lambda: where_a() + UP * 0.3 + RIGHT * pm.HOOK_SPEED * KV, cfg.VELOCITY,
                 width=0.08, tip=0.26)
    v_a.presence = 0.0
    stage.add_overlay(v_a)
    gauge = Speedometer([-6.35, 2.3, 0], top=40, radius=1.25, value=pm.HOOK_SPEED, unit_gap=0.22)
    show(scene, stage, 1.2, FadeIn(gauge))

    # --- 1. Straight road, steady 20 m/s --------------------------------------------------------------------
    scene.play(stage.fade(v_a, 1.0), drive.to(stage, 3.0, run_time=3.0, rate_func=linear), run_time=3.0)
    scene.play(drive.to(stage, 7.0, run_time=4.0, rate_func=linear))

    # --- 2. Not faster, not slower, not turning: a = 0 -------------------------------------------------------------
    beat(scene, t, 1)
    checks = VGroup(txt("speed: constant", cfg.FONT["small"], cfg.WHITE),
                    txt("direction: constant", cfg.FONT["small"], cfg.VELOCITY)).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
    checks.move_to([3.9, 3.3, 0])
    zero = eq(r"\vec a = 0", cfg.FONT["section"], cfg.ACCEL).move_to([3.9, 1.75, 0])
    scene.play(FadeIn(checks[0], shift=DOWN * 0.1), drive.to(stage, 9.0, run_time=2.0, rate_func=linear), run_time=2.0)
    scene.play(FadeIn(checks[1], shift=DOWN * 0.1), drive.to(stage, 11.0, run_time=2.0, rate_func=linear), run_time=2.0)
    scene.play(Write(zero), drive.to(stage, 13.5, run_time=2.5, rate_func=linear), run_time=2.5)
    scene.play(drive.to(stage, 18.0, run_time=4.0, rate_func=linear))

    # --- 3. The same car on a circular track, still 20 m/s -----------------------------------------------------------
    beat(scene, t, 2)
    loop = Circuit(stage, TRACK, centre=TRACK_C, R=R_TRACK, body="car", color=cfg.CAR, kv=KV, ka=KA, car_length=0.62,
                   phase=-np.pi / 2)
    for part in loop.parts:
        part.presence = 0.0
    scene.play(FadeOut(checks), FadeOut(zero), *[stage.fade(p, 0.0) for p in car_a], stage.fade(v_a, 0.0),
               stage.fade(road, 0.25), stage.fade(track, 1.0), run_time=1.0)
    scene.play(*[stage.fade(p, 1.0) for p in loop.parts], *stage.turn(pitch=0.8, run_time=1.2),
               stage.zoom_to(1.42, run_time=1.2), stage.glide([0.0, -0.95, 0], run_time=1.2), run_time=1.2)
    scene.play(loop.run(6.5))

    # --- 4. Same speedometer; the velocity arrow keeps turning ----------------------------------------------------------
    beat(scene, t, 3)
    v_b = loop.add_arrow("v", width=0.08, lift=0.3)
    scene.play(stage.fade(v_b, 1.0), loop.run(loop.t + 1.0), run_time=1.0)
    ghosts = []
    for k in range(4):
        scene.play(loop.run(loop.t + 1.9))
        when = loop.t
        p = loop.world(when) + UP * 0.3
        ghost = Vector(p, p + ground_vec(loop.view.vel(when) * KV), cfg.VELOCITY, width=0.06, tip=0.22, glow=False)
        ghost.presence = 0.0
        stage.add_overlay(ghost)
        ghosts.append(ghost)
        scene.play(stage.fade(ghost, 0.45, run_time=0.3), loop.run(loop.t + 0.3), run_time=0.3)

    # --- 5. Changing direction means changing velocity -------------------------------------------------------------------
    beat(scene, t, 4)
    chain = VGroup(txt("direction changes", cfg.FONT["small"], cfg.VELOCITY), txt("→", cfg.FONT["small"], cfg.WHITE),
                   eq(r"\vec v \text{ changes}", cfg.FONT["small"], cfg.VELOCITY), txt("→", cfg.FONT["small"], cfg.WHITE),
                   eq(r"\vec a \neq 0", cfg.FONT["small"], cfg.ACCEL)).arrange(RIGHT, buff=0.3)
    fit_width(chain, 9.6)
    chain.move_to([2.2, 3.55, 0])
    scene.play(FadeIn(chain[:3], shift=DOWN * 0.1), loop.run(loop.t + 2.5), run_time=2.5)
    scene.play(FadeIn(chain[3:], shift=DOWN * 0.1), loop.run(loop.t + 2.0), run_time=2.0)
    scene.play(loop.run(loop.t + 2.0))

    # --- 6. Accelerating the whole time: the arrow toward the centre -------------------------------------------------------
    beat(scene, t, 5)
    a_b = loop.add_arrow("a", width=0.08, lift=0.3)
    scene.play(*[stage.fade(g, 0.0) for g in ghosts], stage.fade(a_b, 1.0), loop.run(loop.t + 1.0), run_time=1.0)
    scene.play(loop.run(loop.t + 8.0))

    # --- 7. Why? Which way? What force? ----------------------------------------------------------------------------------------
    beat(scene, t, 6)
    questions = VGroup(chip("Why?", cfg.WHITE), chip("Which way?", cfg.ACCEL), chip("What force?", cfg.FORCE))
    questions.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([5.7, 0.9, 0])
    for q in questions:
        scene.play(FadeIn(q, shift=LEFT * 0.2), loop.run(loop.t + 1.6), run_time=1.6)
    scene.play(loop.run(loop.t + 4.0))

    # --- 8. Velocity is a vector; direction matters ---------------------------------------------------------------------------
    beat(scene, t, 7)
    vector = result_label("velocity is a vector", cfg.VELOCITY, cfg.FONT["section"]).move_to([2.2, 3.55, 0])
    scene.play(FadeOut(questions), fade_through(chain, vector), loop.run(loop.t + 1.2), run_time=1.2)
    scene.play(loop.run(loop.t + 6.5))

    # --- 9. Title ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    card = title_card(cfg.PROJECT_TITLE, cfg.VIDEO_SUBTITLE).move_to(UP * 0.25)
    series = txt(cfg.SERIES_LABEL, cfg.FONT["small"], cfg.MUTED)
    fit_width(series, 12.8)
    series.next_to(card, DOWN, buff=0.6)
    episode = chip(cfg.EPISODE_LABEL, cfg.GOLD).next_to(card, UP, buff=0.5)
    hide(scene, stage, 1.0, FadeOut(vector), FadeOut(gauge))
    scene.play(FadeIn(card, scale=0.94), FadeIn(episode, shift=DOWN * 0.2), run_time=1.4)
    scene.play(FadeIn(series, shift=UP * 0.15), run_time=0.8)
    rule = Line(LEFT * 4.6, RIGHT * 4.6, stroke_color=cfg.GOLD, stroke_width=4).next_to(card, DOWN, buff=0.22)
    scene.play(Create(rule), card.glow.animate.set_stroke(opacity=0.3), run_time=1.6)
    scene.play(card.glow.animate.set_stroke(opacity=0.12), run_time=1.4)
    end_scene(scene, t, cfg.SCENE_DURATIONS["01"])
