"""Scene 01 — the hook. A ball is thrown across a 3D field: the reference
throw, 20 m/s at 45 degrees, flown from ``physics_models.REFERENCE``. The
questions (where after one second? how high? how far, at other angles?)
appear as marks on the field. Then the film's central idea is shown before
it is explained: the floor shadow glides steadily, the wall shadow only rises
and falls. The title closes the scene.
"""

from manim_scenes.common import *

ORIGIN_X = LAUNCH_X


class Scene01PredictFlight(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "01")
    stage = field_stage((0.3, -1.7, 0), zoom=1.28, yaw=-0.34, pitch=0.32, x_range=(-6.2, 6.4), z_range=(-2.6, 2.6),
                        wall_x=WALL_X, wall_height=3.0)
    stage.wall.presence = 0.0
    flight = Flight(stage, origin=(ORIGIN_X, 0, 0))
    flight.launcher()
    show(scene, stage, 1.2)

    # --- 1. Throw a ball: it rises, drifts forward, comes back down -------------------------------------
    scene.play(flight.realtime(speed=0.55), run_time=P.flight_time / 0.55)
    scene.wait(0.6)

    # --- 2. Where will it be after one second? ---------------------------------------------------------------
    beat(scene, t, 1)
    rewind(scene, flight)
    scene.play(flight.realtime(1.0, speed=0.55))
    one_s = flight.world(1.0)
    marker = Disc(one_s, 0.32, cfg.GOLD, normal=(0, 0, 1), opacity=0.0, stroke=cfg.GOLD)
    stage.add_body(marker)
    question = Tag(txt("t = 1 s  →  where?", cfg.FONT["label"], cfg.GOLD), one_s, RIGHT * 2.4 + UP * 0.55)
    question.presence = 0.0
    stage.add_overlay(question)
    scene.play(stage.fade(question, 1.0), run_time=0.8)

    # --- 3. How high? How far, at other angles? -------------------------------------------------------------------
    beat(scene, t, 2)
    apex = flight.at_metres(P.vx * P.apex_time, P.max_height)
    top_line = Segment(flight.at_metres(-1.0, P.max_height), flight.at_metres(P.range + 1, P.max_height),
                       cfg.Y_COLOR, width=3, opacity=0.8, dashed=True)
    top_line.presence = 0.0
    how_high = Tag(txt("how high?", cfg.FONT["label"], cfg.Y_COLOR), apex, UP * 0.6)
    how_high.presence = 0.0
    stage.add_body(top_line)
    stage.add_overlay(how_high)
    scene.play(stage.fade(question, 0.0), stage.fade(marker, 0.0), flight.realtime(speed=0.55),
               run_time=(P.flight_time - 1.0) / 0.55)
    scene.play(stage.fade(top_line, 1.0), stage.fade(how_high, 1.0), run_time=0.8)
    others = []
    for model, color in ((pm.TABLE[0], cfg.CYAN), (pm.TABLE[2], cfg.PURPLE)):
        other = Flight(stage, model, origin=(ORIGIN_X, 0, 0), trail=False)
        other.ball.presence = 0.0
        curve = Curve(other.full_path(), color, width=3.5, opacity=0.85, bias=-0.6)
        curve.presence = 0.0
        stage.add_body(curve)
        others.append(curve)
    how_far = Tag(txt("how far?", cfg.FONT["label"], cfg.GREEN), flight.at_metres(P.range, 0), DOWN * 0.55 + RIGHT * 0.3)
    how_far.presence = 0.0
    stage.add_overlay(how_far)
    scene.play(*[stage.fade(c, 1.0) for c in others], stage.fade(how_far, 1.0), run_time=1.6)

    # --- 4. Every instant, a slightly different direction ------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(*[stage.fade(m, 0.0) for m in (*others, top_line, how_high, how_far)], run_time=0.8)
    flight.add_arrow("v", cfg.VELOCITY)
    rewind(scene, flight)
    scene.play(stage.fade(flight.arrows["v"], 1.0), run_time=0.5)
    scene.play(flight.realtime(speed=0.4), run_time=P.flight_time / 0.4)

    # --- 5. Split it into two simpler motions ----------------------------------------------------------------------------
    beat(scene, t, 4)
    flight.add_arrow("vx", cfg.X_COLOR, width=0.06)
    flight.add_arrow("vy", cfg.Y_COLOR, width=0.06)
    rewind(scene, flight)
    scene.play(flight.realtime(0.45, speed=0.4), run_time=0.45 / 0.4)
    scene.play(stage.fade(flight.arrows["vx"], 1.0), stage.fade(flight.arrows["vy"], 1.0), run_time=0.8)
    split = Tag(VGroup(txt("forward", cfg.FONT["small"], cfg.X_COLOR), txt("+", cfg.FONT["small"], cfg.WHITE),
                       txt("up / down", cfg.FONT["small"], cfg.Y_COLOR)).arrange(RIGHT, buff=0.2),
                flight.world(0.45), UP * 1.5 + RIGHT * 0.9)
    split.presence = 0.0
    stage.add_overlay(split)
    scene.play(stage.fade(split, 1.0), run_time=0.6)
    scene.play(flight.realtime(speed=0.4), run_time=(P.flight_time - 0.45) / 0.4)
    scene.play(stage.fade(split, 0.0), *[stage.fade(a, 0.0) for a in flight.arrows.values()], run_time=0.6)

    # --- 6. The floor shadow glides at a steady pace -------------------------------------------------------------------------
    beat(scene, t, 5)
    flight.add_shadows(floor=True, wall_x=WALL_X)
    flight.wall_shadow.presence = 0.0
    flight.add_ghosts([k * P.flight_time / 6 for k in range(7)], alpha=0.0)
    floor_ghosts = [Disc(flight.world(g.when) * np.array([1, 0, 1]) + np.array([0, 0.012, 0]), 0.16, cfg.X_COLOR,
                         opacity=0.55) for g in flight.ghosts]
    for ghost, disc in zip(flight.ghosts, floor_ghosts):
        disc.presence = 0.0
    stage.add_body(*floor_ghosts)
    rewind(scene, flight)
    scene.play(*[stage.fade(d, 1.0) for d in floor_ghosts], run_time=0.6)
    scene.play(flight.realtime(speed=0.5), run_time=P.flight_time / 0.5)

    # --- 7. The wall shadow only goes up, and down -----------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(stage.fade(stage.wall, 1.0), *[stage.fade(d, 0.0) for d in floor_ghosts],
               stage.fade(flight.floor_shadow, 0.0), *stage.turn(yaw=-0.62, run_time=1.2), run_time=1.2)
    rewind(scene, flight, 0.6)
    scene.play(stage.fade(flight.wall_shadow, 1.0), run_time=0.4)
    scene.play(flight.realtime(speed=0.72), run_time=P.flight_time / 0.72)

    # --- 8. Two simple motions at once: we need vectors ------------------------------------------------------------------------------
    beat(scene, t, 7)
    rewind(scene, flight, 0.6)
    steady = Tag(txt("steady", cfg.FONT["label"], cfg.X_COLOR), flight.world(P.flight_time) * np.array([1, 0, 1]),
                 DOWN * 0.5 + LEFT * 0.4)
    updown = Tag(txt("up and down", cfg.FONT["label"], cfg.Y_COLOR), np.array([WALL_X, P.max_height * flight.s, 0]),
                 UP * 0.55 + RIGHT * 0.5)
    for tag in (steady, updown):
        tag.presence = 0.0
    stage.add_overlay(steady, updown)
    scene.play(stage.fade(flight.floor_shadow, 1.0), stage.fade(steady, 1.0), stage.fade(updown, 1.0), run_time=0.6)
    scene.play(flight.realtime(speed=0.5), run_time=P.flight_time / 0.5)
    vectors = result_label("vectors", cfg.GOLD, cfg.FONT["title"]).move_to(UP * 3.3)
    scene.play(FadeIn(vectors, scale=0.9), run_time=0.8)

    # --- 9. Title ------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    card = title_card(cfg.PROJECT_TITLE, cfg.VIDEO_SUBTITLE).move_to(UP * 0.25)
    series = txt(cfg.SERIES_LABEL, cfg.FONT["small"], cfg.MUTED)
    fit_width(series, 12.8)
    series.next_to(card, DOWN, buff=0.6)
    episode = chip("Episode 01", cfg.GOLD).next_to(card, UP, buff=0.5)
    hide(scene, stage, 1.0, FadeOut(vectors))
    scene.play(FadeIn(card, scale=0.94), FadeIn(episode, shift=DOWN * 0.2), run_time=1.4)
    scene.play(FadeIn(series, shift=UP * 0.15), run_time=0.8)
    rule = Line(LEFT * 4.6, RIGHT * 4.6, stroke_color=cfg.GOLD, stroke_width=4).next_to(card, DOWN, buff=0.22)
    scene.play(Create(rule), card.glow.animate.set_stroke(opacity=0.3), run_time=1.6)
    scene.play(card.glow.animate.set_stroke(opacity=0.12), run_time=1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["01"])
