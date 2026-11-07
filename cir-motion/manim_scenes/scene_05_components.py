"""Scene 05 — velocity in components, and the space-time helix.

Flat first: the reference particle's position r cos(theta) i + r sin(theta) j
with its blue and rose projections, and theta = omega t + theta0. Then time
becomes a third axis (as in Episode 01's space-time curve): every moment is
a point (r cos theta, r sin theta, t) and the circle stretches into a helix,
first seen face-on down the time axis, then from the side. Its shadow on the
floor is the cosine wave x(t) (blue), on the back wall the sine wave y(t)
(rose). Back to the flat view for the derivative: the velocity's blue and
rose components keep changing while its length stays r|omega|.

Stage scales: 1.25 units per metre across, 1.7 units per second along time.
"""

from manim_scenes.common import *

S = 1.25                     # stage units per metre
ST = 1.7                     # stage units per second of time
SLOW = 0.4
X0 = -P.period * ST * 0.75   # time axis starts here (world x); the helix is centred


class Scene05Components(Scene):
    def construct(self) -> None:
        play_scene(self)


def helix_point(t: float) -> np.ndarray:
    """World point of the moment t: time along +x, x(t) to screen right (world z), y(t) up."""
    x, y = P.position(t)
    return np.array([X0 + t * ST, y * S, x * S])


def helix(until: float, project: str | None = None, n: int = 160) -> np.ndarray:
    ts = np.linspace(0, max(until, 1e-3), n)
    pts = np.array([helix_point(t) for t in ts])
    if project == "floor":
        pts[:, 1] = -P.r * S - 0.35
    elif project == "wall":
        pts[:, 2] = -P.r * S - 0.35
    return pts


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "05", "Velocity in components")
    view = CircleView([-3.6, -0.55, 0], 2.3, P, kv=1.2 / P.v, phase=0.0)
    view.clock.value = 0.55
    axes = VGroup(Line(view.c + LEFT * 2.9, view.c + RIGHT * 2.9, stroke_color=cfg.X_COLOR, stroke_width=3, stroke_opacity=0.8),
                  Line(view.c + DOWN * 2.9, view.c + UP * 2.9, stroke_color=cfg.Y_COLOR, stroke_width=3, stroke_opacity=0.8))
    r = view.arrow("r", width=0.08)
    foot_x = lambda: np.array([view.point()[0], view.c[1], 0])  # noqa: E731
    foot_y = lambda: np.array([view.c[0], view.point()[1], 0])  # noqa: E731
    proj = VGroup(VecArrow(lambda: view.c, foot_x, cfg.X_COLOR, width=0.07, glow=False),
                  VecArrow(lambda: view.c, foot_y, cfg.Y_COLOR, width=0.07, glow=False))
    drops = live(VGroup(), lambda: VGroup(dashed_path(view.point(), foot_x(), cfg.MUTED, 2.5, count=8),
                                          dashed_path(view.point(), foot_y(), cfg.MUTED, 2.5, count=8)))
    angle = live(VMobject(), lambda: arc_mark(view.c, 0.6, 0.0, view.theta() % TAU, cfg.ANGLE))
    scene.play(FadeIn(axes), FadeIn(view.ring), FadeIn(view.hub), run_time=0.8)
    scene.add(r, view.ball, angle)
    scene.play(r.grow_in(run_time=0.8), FadeIn(view.ball), run_time=0.8)
    position = eq([r"\vec r", "=", r"r\cos\theta", r"\,\hat\imath", "+", r"r\sin\theta", r"\,\hat\jmath"], cfg.FONT["section"])
    paint(position, {0: cfg.POSITION, 2: cfg.X_COLOR, 3: cfg.X_COLOR, 5: cfg.Y_COLOR, 6: cfg.Y_COLOR})
    fit_width(position, 7.0)
    position.move_to([3.7, 2.2, 0])
    scene.add(proj, drops)
    scene.play(FadeOut(head), Write(position), *[a.grow_in(run_time=1.4) for a in proj], run_time=1.6)
    scene.play(view.run(view.clock.value + 1.4, 1.4 / SLOW), run_time=1.4 / SLOW)

    # --- 2. theta = omega t + theta0 ----------------------------------------------------------------------------------
    beat(scene, t, 1)
    phase = paint(eq([r"\theta", "=", r"\omega t", "+", r"\theta_0"], cfg.FONT["section"]),
                  {0: cfg.ANGLE, 2: cfg.ANGLE, 4: cfg.ANGLE}).next_to(position, DOWN, buff=0.7)
    scene.play(Write(phase), run_time=1.2)
    scene.play(view.run(view.clock.value + 2.6, 2.6 / SLOW), run_time=2.6 / SLOW)

    # --- 3. omega: how fast the angle grows -----------------------------------------------------------------------------------
    beat(scene, t, 2)
    omega = txt("ω: angular velocity", cfg.FONT["label"], cfg.ANGLE).next_to(phase, DOWN, buff=0.6)
    scene.play(FadeIn(omega, shift=UP * 0.1), Indicate(phase[2], color=cfg.ANGLE), run_time=1.0)
    scene.play(view.run(view.clock.value + 1.5, 1.5 / SLOW), run_time=1.5 / SLOW)

    # --- 4. Time as a third direction: a helix --------------------------------------------------------------------------------------
    beat(scene, t, 3)
    for m in (drops, angle):
        m.clear_updaters()
    clear(scene, run_time=0.6)
    stage = Stage((0.0, -0.2, 0), zoom=1.0, yaw=np.pi / 2, pitch=0.0, sway=0.0, distance=40.0)
    clock = Knob(0.0)
    span = P.period * 1.5
    floor = Grid((X0, -P.r * S - 0.35, -P.r * S - 0.35), (1, 0, 0), (0, 0, 1), (0, span * ST + 0.4), (0, 2 * P.r * S + 0.7),
                 step=0.5, major=0, color=cfg.X_COLOR, opacity=0.2)
    wall = Grid((X0, -P.r * S - 0.35, -P.r * S - 0.35), (1, 0, 0), (0, 1, 0), (0, span * ST + 0.4), (0, 2 * P.r * S + 0.7),
                step=0.5, major=0, color=cfg.Y_COLOR, opacity=0.2, bias=-0.9e4)
    time_axis = Segment(np.array([X0, 0, 0]), np.array([X0 + span * ST + 0.6, 0, 0]), cfg.TIME, width=4, opacity=0.9)
    t_tag = Tag(eq("t", cfg.FONT["body"], cfg.TIME), np.array([X0 + span * ST + 0.95, 0, 0]))
    circle = Curve(np.array([helix_point(s) for s in np.linspace(0, P.period, 90)]), cfg.MUTED, width=3, opacity=0.55)
    path = Curve(lambda: helix(clock.value), cfg.WHITE, width=5)
    ball = Ball(lambda: helix_point(clock.value), 0.17, cfg.BALL)
    shadows = {"floor": Curve(lambda: helix(clock.value, "floor"), cfg.X_COLOR, width=4.5, bias=-100),
               "wall": Curve(lambda: helix(clock.value, "wall"), cfg.Y_COLOR, width=4.5, bias=-100)}
    for item in (floor, wall, time_axis, t_tag, *shadows.values()):
        item.presence = 0.0
    stage.add_body(floor, wall, time_axis, circle, *shadows.values(), path, ball)
    stage.add_overlay(t_tag)
    show(scene, stage, 0.7)
    scene.play(clock.to(stage, P.period * 0.5, run_time=1.6, rate_func=linear))
    scene.play(*stage.turn(yaw=0.55, pitch=0.32, run_time=2.4), stage.fade(time_axis, 1.0, run_time=2.4),
               stage.fade(t_tag, 1.0, run_time=2.4), stage.zoom_to(0.92, run_time=2.4), run_time=2.4)
    scene.play(clock.to(stage, span, run_time=3.6, rate_func=linear))

    # --- 5. Shadows: a cosine on one wall, a sine on the other -------------------------------------------------------------------------
    beat(scene, t, 4)
    clock.value = 0.0
    scene.play(stage.fade(floor, 1.0), stage.fade(wall, 1.0), stage.fade(shadows["floor"], 1.0),
               stage.fade(shadows["wall"], 1.0), *stage.turn(yaw=0.42, pitch=0.42, run_time=1.2), run_time=1.2)
    scene.play(clock.to(stage, span, run_time=5.0, rate_func=linear))
    waves = VGroup(eq(r"x(t) = r\cos\theta", cfg.FONT["body"], cfg.X_COLOR),
                   eq(r"y(t) = r\sin\theta", cfg.FONT["body"], cfg.Y_COLOR)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    waves.move_to([-4.6, 3.1, 0])
    scene.play(FadeIn(waves, shift=DOWN * 0.1), run_time=0.8)
    scene.play(*stage.turn(yaw=0.62, pitch=0.25, run_time=3.0), run_time=3.0)

    # --- 6. Differentiate: the velocity components ---------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    hide(scene, stage, 0.8, FadeOut(waves))
    flat = CircleView([-3.6, -0.55, 0], 2.3, P, kv=1.25 / P.v)
    flat.clock.value = 0.55
    axes = VGroup(Line(flat.c + LEFT * 2.9, flat.c + RIGHT * 2.9, stroke_color=cfg.X_COLOR, stroke_width=3, stroke_opacity=0.8),
                  Line(flat.c + DOWN * 2.9, flat.c + UP * 2.9, stroke_color=cfg.Y_COLOR, stroke_width=3, stroke_opacity=0.8))
    velocity = eq([r"\vec v", "=", r"-r\omega\sin\theta", r"\,\hat\imath", "+", r"r\omega\cos\theta", r"\,\hat\jmath"],
                  cfg.FONT["section"])
    paint(velocity, {0: cfg.VELOCITY, 2: cfg.X_COLOR, 3: cfg.X_COLOR, 5: cfg.Y_COLOR, 6: cfg.Y_COLOR})
    fit_width(velocity, 7.2)
    velocity.move_to([3.7, 1.9, 0])
    derivative = eq(r"\vec v = \frac{d\vec r}{dt}", cfg.FONT["body"], cfg.VELOCITY).next_to(velocity, UP, buff=0.45)
    scene.play(FadeIn(axes), FadeIn(flat.ring), FadeIn(flat.hub), FadeIn(flat.ball), FadeIn(derivative), run_time=0.8)
    scene.play(Write(velocity), run_time=1.8)
    v = flat.arrow("v", width=0.1)
    vx, vy = flat.arrow("vx", width=0.075, glow=False), flat.arrow("vy", width=0.075, glow=False)
    scene.add(v, vx, vy)
    scene.play(v.grow_in(run_time=0.8), run_time=0.8)
    scene.play(vx.grow_in(run_time=0.8), vy.grow_in(run_time=0.8), run_time=0.8)

    # --- 7. Both components keep changing --------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    readout = VGroup(number_line(lambda: float(flat.vel()[0]), 2, "m/s", cfg.X_COLOR, 54, "vₓ"),
                     number_line(lambda: float(flat.vel()[1]), 2, "m/s", cfg.Y_COLOR, 54, "vᵧ")).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    readout.move_to([3.2, -0.2, 0])
    scene.play(FadeIn(readout), run_time=0.6)
    scene.play(flat.run(flat.clock.value + 2.0, 2.0 / SLOW), run_time=2.0 / SLOW)

    # --- 8. The magnitude: sin^2 + cos^2 = 1 -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    for m in readout:
        m.clear_updaters()
    size = eq(r"|\vec v| = \sqrt{r^2\omega^2\,(\sin^2\theta + \cos^2\theta)}", cfg.FONT["body"]).move_to([3.7, 0.3, 0])
    fit_width(size, 6.3)
    one = eq(r"\sin^2\theta + \cos^2\theta = 1", cfg.FONT["body"], cfg.ANGLE).next_to(size, DOWN, buff=0.5)
    scene.play(FadeOut(VGroup(readout, velocity, derivative)), run_time=0.4)
    scene.play(Write(size), run_time=1.4)
    scene.play(FadeIn(one, shift=UP * 0.1), run_time=0.8)
    scene.play(flat.run(flat.clock.value + 1.6, 1.6 / SLOW), run_time=1.6 / SLOW)

    # --- 9. v = r |omega| -----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    result = eq([r"v", "=", r"r\,|\omega|"], cfg.FONT["title"]).next_to(one, DOWN, buff=0.6)
    paint(result, {0: cfg.VELOCITY, 2: cfg.ANGLE})
    framed = boxed(result, cfg.RESULT)
    scene.play(Write(result), run_time=1.2)
    scene.play(FadeIn(framed[0]), flat.run(flat.clock.value + 0.6, 0.6), run_time=0.6)
    scene.play(flat.run(flat.clock.value + 2.6, 2.6 / SLOW), run_time=2.6 / SLOW)
    end_scene(scene, t, cfg.SCENE_DURATIONS["05"])
