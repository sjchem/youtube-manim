"""Scene 02 — what acceleration means in physics. A speedometer sweeps from
20 to 60 km/h (the everyday picture), then a = dv/dt replaces it. Velocity
is an arrow, so it can change three ways, shown in three panels: its length
grows, it turns at fixed length, or both. Then the opening's two cars return
as small diagrams: on the straight road the arrow never changes (a = 0); on
the track it keeps turning (a != 0). The key idea closes the scene.
"""

from manim_scenes.common import *

PANEL_X = (-4.7, 0.0, 4.7)
PANEL_Y = -0.35


class Scene02Acceleration(Scene):
    def construct(self) -> None:
        play_scene(self)


def arrow_panel(x: float, title: str) -> tuple[VGroup, Knob, Knob, VecArrow]:
    """A panel with one velocity arrow whose length and angle are live knobs."""
    box = panel(4.3, 4.2, cfg.MUTED, 0.55).move_to([x, PANEL_Y, 0])
    head = txt(title, cfg.FONT["small"], cfg.WHITE).next_to(box.get_top(), DOWN, buff=0.28)
    length, angle = Knob(1.4), Knob(0.35)
    tail = np.array([x - 0.9, PANEL_Y - 1.4, 0])
    arrow = VecArrow(tail, lambda: tail + length.value * np.array([np.cos(angle.value), np.sin(angle.value), 0]),
                     cfg.VELOCITY, width=0.1, tip_len=0.3)
    return VGroup(box, head), length, angle, arrow


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "02", "What is acceleration?")
    gauge = Speedometer([0, -0.4, 0], top=80, radius=1.9, value=20.0, unit="km/h", step=10)
    scene.play(FadeIn(gauge), run_time=0.8)
    faster = chip("speeding up", cfg.WHITE).move_to([0, 2.45, 0])
    scene.play(FadeIn(faster), gauge.value.to(gauge, 60.0, run_time=3.2), run_time=3.2)
    scene.wait(1.0)

    # --- 2. a = dv/dt ------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    cross = strike(faster.label)
    scene.play(Create(cross), run_time=0.6)
    definition = eq([r"\vec a", "=", r"\frac{d\vec v}{dt}"], cfg.FONT["hero"])
    paint(definition, {0: cfg.ACCEL, 2: cfg.VELOCITY})
    framed = boxed(definition, cfg.RESULT, buff=0.3)
    scene.play(FadeOut(VGroup(faster, cross)), FadeOut(gauge), run_time=0.8)
    scene.play(Write(definition), run_time=1.6)
    scene.play(FadeIn(framed[0]), run_time=0.6)

    # --- 3. Velocity is a vector: magnitude and direction --------------------------------------------------------------
    beat(scene, t, 2)
    framed = VGroup(framed[0], definition)
    scene.play(framed.animate.scale(0.62).move_to([0, 3.0, 0]), run_time=0.8)
    tail = np.array([-1.6, -1.2, 0])
    tip = tail + np.array([3.0, 1.4, 0])
    big = VecArrow(tail, tip, cfg.VELOCITY, width=0.13, tip_len=0.38)
    scene.add(big)
    scene.play(big.grow_in(run_time=0.9), run_time=0.9)
    mag = txt("magnitude = speed", cfg.FONT["small"], cfg.WHITE)
    label_at(mag, big, side=DOWN, buff=0.35)
    direction = txt("direction", cfg.FONT["small"], cfg.VELOCITY).next_to(tip, RIGHT, buff=0.3)
    scene.play(FadeIn(mag), run_time=0.6)
    scene.play(FadeIn(direction), run_time=0.6)

    # --- 4-6. Three ways to change ---------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(VGroup(big, mag, direction)), run_time=0.6)
    panels = [arrow_panel(x, name) for x, name in zip(PANEL_X, ("magnitude", "direction", "both"))]
    scene.play(FadeIn(panels[0][0]), run_time=0.5)
    scene.add(panels[0][3])
    scene.play(panels[0][3].grow_in(run_time=0.5), run_time=0.5)
    scene.play(panels[0][1].to(panels[0][3], 2.7, run_time=2.0, rate_func=there_and_back_with_pause), run_time=2.0)

    beat(scene, t, 4)
    scene.play(FadeIn(panels[1][0]), run_time=0.4)
    scene.add(panels[1][3])
    scene.play(panels[1][3].grow_in(run_time=0.4), run_time=0.4)
    scene.play(panels[1][2].to(panels[1][3], 1.5, run_time=2.2), run_time=2.2)

    beat(scene, t, 5)
    scene.play(FadeIn(panels[2][0]), run_time=0.4)
    scene.add(panels[2][3])
    scene.play(panels[2][3].grow_in(run_time=0.4), run_time=0.4)
    scene.play(panels[2][1].to(panels[2][3], 2.4, run_time=2.4), panels[2][2].to(panels[2][3], 1.35, run_time=2.4),
               run_time=2.4)

    # --- 7. Every one is acceleration ----------------------------------------------------------------------------------------
    beat(scene, t, 6)
    marks = VGroup(*[eq(r"\vec a \neq 0", cfg.FONT["body"], cfg.ACCEL).move_to([x, PANEL_Y - 2.7, 0]) for x in PANEL_X])
    scene.play(LaggedStart(*[FadeIn(m, shift=UP * 0.12) for m in marks], lag_ratio=0.25), run_time=1.4)

    # --- 8. Straight road: a = 0. Circular track: a != 0 -------------------------------------------------------------------------
    beat(scene, t, 7)
    clear(scene, framed)
    road_box = panel(6.8, 4.6, cfg.MUTED, 0.55).move_to([-3.7, -0.45, 0])
    loop_box = panel(6.8, 4.6, cfg.MUTED, 0.55).move_to([3.7, -0.45, 0])
    lane = Line([-6.7, -1.2, 0], [-0.7, -1.2, 0], stroke_color=cfg.GRAY, stroke_width=22, stroke_opacity=0.45)
    view = CircleView([3.7, -0.75, 0], 1.45, P, kv=1.3 / P.v, ka=0.95 / P.accel, phase=-np.pi / 2)
    # The camera follows car A: it stays centred while the lane's dashes stream past
    # at exactly the ball's screen speed, read from the same clock.
    pace = view.R * P.angular_speed            # screen units per second of model time
    car_at = np.array([-3.9, -1.2, 0])
    dashes = VMobject(stroke_color=cfg.WHITE, stroke_width=3, stroke_opacity=0.6, fill_opacity=0)

    def stream(m):
        m.clear_points()
        for k in range(8):
            x = -6.6 + (k * 0.75 - pace * view.clock.value) % 6.0
            m.start_new_path(np.array([x, -1.2, 0.0]))
            m.add_line_to(np.array([min(x + 0.35, -0.7), -1.2, 0.0]))

    stream(dashes)
    dashes.add_updater(stream)
    car = Car(cfg.CAR, 0.72)
    car.set_pose(car_at, 0.0)
    v_line = VecArrow(car_at, car_at + RIGHT * view.kv * P.v, cfg.VELOCITY, width=0.09, tip_len=0.26)
    v_loop = view.arrow("v", width=0.09, tip_len=0.26)
    a_loop = view.arrow("a", width=0.09, tip_len=0.26)
    a_loop.alpha = 0.0
    names = VGroup(txt("A: straight", cfg.FONT["small"], cfg.WHITE).next_to(road_box.get_top(), DOWN, buff=0.25),
                   txt("B: circle", cfg.FONT["small"], cfg.WHITE).next_to(loop_box.get_top(), DOWN, buff=0.25))
    scene.play(FadeIn(VGroup(road_box, loop_box, lane, names)), FadeIn(dashes), FadeIn(view.ring), FadeIn(view.ball),
               FadeIn(car), run_time=0.9)
    scene.add(v_line, v_loop, a_loop)
    scene.play(v_line.grow_in(run_time=0.5), v_loop.grow_in(run_time=0.5), run_time=0.5)
    same = lambda seconds: (view.run(view.clock.value + seconds * 0.5, seconds),)  # noqa: E731  half real time
    scene.play(*same(4.0), run_time=4.0)
    zero = eq(r"\vec a = 0", cfg.FONT["body"], cfg.ACCEL).next_to(road_box.get_bottom(), UP, buff=0.3)
    nonzero = eq(r"\vec a \neq 0", cfg.FONT["body"], cfg.ACCEL).next_to(loop_box.get_bottom(), UP, buff=0.3)
    scene.play(FadeIn(zero), *same(2.0), run_time=2.0)
    scene.play(*same(3.0), run_time=3.0)
    scene.play(FadeIn(nonzero), a_loop.fade_to(1.0, run_time=0.8), *same(2.0), run_time=2.0)
    scene.play(*same(2.5), run_time=2.5)

    # --- 9. Constant speed does not mean constant velocity -------------------------------------------------------------------------
    beat(scene, t, 8)
    clear(scene)
    lines = VGroup(eq(r"|\vec v| = \text{constant}\ \ \not\Rightarrow\ \ \vec v = \text{constant}", cfg.FONT["section"]),
                   eq(r"\vec a = 0\ \iff\ \vec v = \text{constant}", cfg.FONT["section"], cfg.ACCEL)).arrange(DOWN, buff=0.7)
    fit_width(lines, 12.6)
    scene.play(FadeIn(lines[0], shift=UP * 0.15), run_time=1.0)
    scene.wait(2.5)
    scene.play(FadeIn(lines[1], shift=UP * 0.15), run_time=1.0)
    key = boxed(lines[1], cfg.RESULT)
    scene.play(FadeIn(key[0]), run_time=0.7)
    scene.wait(2.0)
    scene.play(Indicate(lines[0], color=cfg.VELOCITY, scale_factor=1.03), run_time=1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["02"])
