"""Scene 06 — one lap: distance 2 pi r, displacement zero. A runner (the
reference particle: radius 2 m, 4 m/s, a lap in pi seconds) circles a 3D
running track once. A live distance counter climbs to 2 pi r = 12.57 m
while the teal displacement arrow from the start grows, swings round and
shrinks back to nothing. Average velocity over the lap is zero; average
speed is 2 pi r / T = v. Frozen velocity arrows show the velocity turning
at every instant of the lap.
"""

from manim_scenes.common import *

R = 2.6
SLOW = 0.3
TRACK_COLOR = "#A5523F"


class Scene06OneLap(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "06", "One full lap")
    stage = field_stage((2.3, -0.85, 0), zoom=1.2, pitch=0.92, yaw=-0.2, half=3.8)
    lane = Band(ring_points(ORIGIN, R, 160), 0.38, TRACK_COLOR, opacity=0.85, edge=cfg.WHITE, edge_opacity=0.7)
    stage.add_body(lane)
    runner = Circuit(stage, P, R=R, height=0.22, kv=1.2 / P.v, phase=-np.pi / 2, color=cfg.BALL, radius=0.22)
    start_point = runner.floor_point(0.0)
    pin = Disc(start_point + np.array([0, 0.02, 0]), 0.2, cfg.WHITE, opacity=0.9)
    pin_tag = Tag(txt("start", cfg.FONT["tiny"], cfg.WHITE), start_point, DOWN * 0.45)
    stage.add_body(pin)
    stage.add_overlay(pin_tag)
    show(scene, stage, 1.2)
    scene.wait(1.0)

    # --- 2. One lap: distance 2 pi r ------------------------------------------------------------------------------------
    beat(scene, t, 1)
    distance = number_line(lambda: P.v * runner.t, 2, "m", cfg.CYAN, 60, "distance")
    distance.move_to([-4.4, 3.2, 0])
    trail = Curve(lambda: ring_points(ORIGIN, R, 120, -np.pi / 2, -np.pi / 2 + max(runner.view.theta(runner.t) + np.pi / 2, 1e-3),
                                      h=0.03, closed=False), cfg.CYAN, width=5)
    stage.add_body(trail)
    scene.play(FadeOut(head), FadeIn(distance), run_time=0.6)
    scene.play(runner.run(P.period, P.period / 0.32), run_time=P.period / 0.32)
    lap = eq(rf"d = 2\pi r \approx {fx(P.circumference, 2)}\ \mathrm{{m}}", cfg.FONT["body"], cfg.CYAN)
    lap.next_to(distance, DOWN, buff=0.35, aligned_edge=LEFT)
    scene.play(FadeIn(lap, shift=DOWN * 0.1), run_time=0.7)

    # --- 3. Displacement: start to here ---------------------------------------------------------------------------------------
    beat(scene, t, 2)
    distance.clear_updaters()
    runner.t = 0.0
    scene.play(stage.fade(trail, 0.0), FadeOut(VGroup(distance, lap)), run_time=0.6)
    lift = np.array([0, 0.22, 0])
    shift = Vector(start_point + lift, lambda: runner.world(), cfg.POSITION, width=0.09, tip=0.28)
    shift.keep_in_frame = True
    stage.add_overlay(shift)
    size = number_line(lambda: float(np.linalg.norm(runner.world() - start_point - lift)) / R * P.r, 2, "m", cfg.POSITION, 60,
                       "|Δr|")
    size.move_to([-4.6, 3.2, 0])
    scene.play(FadeIn(size), runner.run(0.35, 0.35 / SLOW), run_time=0.35 / SLOW)
    scene.play(runner.run(0.7, 0.35 / SLOW), run_time=0.35 / SLOW)

    # --- 4. It grows, swings, shrinks to nothing -------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(runner.run(P.period, (P.period - 0.7) / SLOW), run_time=(P.period - 0.7) / SLOW)
    back = txt("back at start", cfg.FONT["small"], cfg.POSITION).next_to(size, DOWN, buff=0.3, aligned_edge=LEFT)
    scene.play(FadeIn(back), Indicate(pin_tag.content, color=cfg.POSITION), run_time=0.8)

    # --- 5. Average velocity = 0 ------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    size.clear_updaters()
    average = paint(eq([r"\vec v_{\text{avg}}", "=", r"\frac{\Delta\vec r}{\Delta t}", "=", "0"], cfg.FONT["section"]),
                    {0: cfg.VELOCITY, 2: cfg.POSITION}).move_to([-4.4, 2.8, 0])
    scene.play(FadeOut(VGroup(size, back)), run_time=0.5)
    scene.play(Write(average), run_time=1.4)
    zero_box = boxed(average[4], cfg.RESULT, 0.14)[0]
    scene.play(FadeIn(zero_box), run_time=0.6)

    # --- 6. Average speed = 2 pi r / T = v ---------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    speed = eq([r"\frac{2\pi r}{T}", "=", rf"\frac{{{fx(P.circumference, 2)}\ \mathrm{{m}}}}{{{fx(P.period, 2)}\ \mathrm{{s}}}}",
                r"\approx", rf"{wh(P.v)}\ \mathrm{{m/s}}"], cfg.FONT["body"])
    paint(speed, {0: cfg.CYAN, 4: cfg.VELOCITY})
    fit_width(speed, 6.1)
    speed.next_to(average, DOWN, buff=0.6)
    speed.align_to(average, LEFT)
    scene.play(Write(speed), run_time=1.6)
    runner.t = 0.0
    scene.play(stage.fade(shift, 0.0), runner.run(P.period, P.period / 0.5), run_time=P.period / 0.5)
    same = txt("= constant speed v", cfg.FONT["small"], cfg.VELOCITY).next_to(speed, DOWN, buff=0.3).align_to(speed, LEFT)
    scene.play(FadeIn(same), run_time=0.6)

    # --- 7. Every instant, the velocity was turning -----------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    arrows = []
    for k in range(8):
        when = k * P.period / 8
        p = runner.world(when)
        arrow = Vector(p, p + ground_vec(runner.view.vel(when) * runner.kv), cfg.VELOCITY, width=0.07, tip=0.24)
        arrow.presence = 0.0
        stage.add_overlay(arrow)
        arrows.append(arrow)
    scene.play(FadeOut(VGroup(average, zero_box, speed, same)), run_time=0.5)
    scene.remove(zero_box)
    scene.play(LaggedStart(*[stage.fade(a, 0.9, run_time=0.6) for a in arrows], lag_ratio=0.35), run_time=3.0)
    v_live = runner.add_arrow("v", width=0.09)
    scene.play(stage.fade(v_live, 1.0), runner.run(runner.t + 1.2, 1.2 / 0.5), run_time=2.4)

    # --- 8. Tangent velocity, always changing direction ------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    summary = VGroup(txt("tangent velocity", cfg.FONT["label"], cfg.VELOCITY),
                     txt("changing direction", cfg.FONT["label"], cfg.WHITE)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    summary.move_to([-4.0, 3.0, 0])
    scene.play(FadeIn(summary, shift=DOWN * 0.1), *stage.turn(yaw=0.25, run_time=4.0),
               runner.run(runner.t + 2.0, 4.0), run_time=4.0)
    scene.play(runner.run(runner.t + 2.6, 2.6 / 0.5), run_time=5.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["06"])
