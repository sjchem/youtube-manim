"""Scene 23 — why a parabola. Time becomes a third axis: each moment of the
reference flight is a point (x, y, t) and the flight is one curve in space.
Turning the stage reads it three ways — from above, x against t is a
straight line (constant v_x, blue); from the side, y against t is a
parabola in time (constant a_y, rose); down the time axis, y against x is
the path itself (gold). Then the same elimination of t in algebra:
y = x tan(theta) - g x^2 / (2 v0^2 cos^2 theta) = A x - B x^2.

Scales: x 0.16 and y 0.30 stage units per metre (y is stretched so the
height reads at this size); t 2.0 units per second.
"""

from manim_scenes.common import *

SX, SY, ST = 0.16, 0.30, 2.0
X0, Y0, Z0 = -P.range * SX / 2, -1.5, -P.flight_time * ST / 2


class Scene23Parabola(Scene):
    def construct(self) -> None:
        play_scene(self)


def world(t: float) -> np.ndarray:
    return np.array([X0 + float(P.x(t)) * SX, Y0 + float(P.y(t)) * SY, Z0 + t * ST])


def curve_points(until: float, project: str | None = None, n: int = 90) -> np.ndarray:
    ts = np.linspace(0.0, max(until, 1e-3), n)
    pts = np.array([world(t) for t in ts])
    if project == "floor":
        pts[:, 1] = Y0
    elif project == "wall":
        pts[:, 0] = X0
    elif project == "front":
        pts[:, 2] = Z0
    return pts


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "23", "Why a parabola?")
    stage = Stage((0.0, -0.75, 0), zoom=1.15, yaw=0.0, pitch=0.0, sway=0.0, distance=40.0)
    clock = Knob(0.0)
    o = np.array([X0, Y0, Z0])
    lengths = (P.range * SX + 0.6, P.max_height * SY + 1.0, P.flight_time * ST + 0.6)
    axes = [Segment(o, o + d * L, c, width=4, opacity=0.9) for d, L, c in
            ((np.array([1, 0, 0]), lengths[0], cfg.X_COLOR), (np.array([0, 1, 0]), lengths[1], cfg.Y_COLOR),
             (np.array([0, 0, 1]), lengths[2], cfg.TIME))]
    tags = [Tag(eq(n, cfg.FONT["body"], c), o + d * (L + 0.35)) for n, d, L, c in
            (("x", np.array([1, 0, 0]), lengths[0], cfg.X_COLOR), ("y", np.array([0, 1, 0]), lengths[1], cfg.Y_COLOR),
             ("t", np.array([0, 0, 1]), lengths[2], cfg.TIME))]
    floor = Grid(o, (1, 0, 0), (0, 0, 1), (0, lengths[0]), (0, lengths[2]), step=0.6, major=0, color=cfg.GRID, opacity=0.35)
    axes[2].presence = tags[2].presence = floor.presence = 0.0
    path = Curve(lambda: curve_points(clock.value), cfg.WHITE, width=5)
    ball = Ball(lambda: world(clock.value), 0.16, cfg.BALL)
    shadows = {name: Curve(lambda n=name: curve_points(clock.value, n), color, width=4, opacity=0.9, bias=-100)
               for name, color in (("floor", cfg.X_COLOR), ("wall", cfg.Y_COLOR), ("front", cfg.GOLD))}
    for c in shadows.values():
        c.presence = 0.0
    stage.add_body(floor, *axes, *shadows.values(), path, ball)
    stage.add_overlay(*tags)
    show(scene, stage, 0.9)
    scene.play(clock.to(stage, P.flight_time, run_time=3.0, rate_func=linear))

    # --- 2. Derive it ------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    derive = txt('y(x) = ?', cfg.FONT["label"], cfg.GOLD).move_to([0, -3.6, 0])
    scene.play(FadeIn(derive), run_time=0.7)

    # --- 3. Time as a third axis ----------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(derive), FadeOut(head), stage.fade(axes[2], 1.0), stage.fade(tags[2], 1.0), stage.fade(floor, 1.0),
               *stage.turn(yaw=-0.5, pitch=0.34, run_time=2.4), stage.zoom_to(0.9, run_time=2.4), run_time=2.4)
    clock.value = 0.0
    scene.play(clock.to(stage, P.flight_time, run_time=4.0, rate_func=linear))
    each = txt('(x, y, t)', cfg.FONT["label"], cfg.WHITE).move_to([3.6, -3.6, 0])
    scene.play(FadeIn(each), run_time=0.7)

    # --- 4. From above: x against t, a straight line ---------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(each), stage.fade(shadows["floor"], 1.0), *[stage.fade(tg, 0.0) for tg in tags],
               *stage.turn(yaw=0.0, pitch=1.52, run_time=2.4), run_time=2.4)
    above = VGroup(txt('x(t)', cfg.FONT["label"], cfg.X_COLOR),
                   txt('vₓ = constant', cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.15).move_to([4.6, 3.0, 0])
    scene.play(FadeIn(above), run_time=0.8)

    # --- 5. From the side: y against t, a parabola in time ----------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(above), stage.fade(shadows["floor"], 0.25), stage.fade(shadows["wall"], 1.0),
               *stage.turn(yaw=PI / 2, pitch=0.0, run_time=2.6), run_time=2.6)
    side = VGroup(txt('y(t)', cfg.FONT["label"], cfg.Y_COLOR),
                  txt('aᵧ = −g', cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.15).move_to([0, 3.0, 0])
    scene.play(FadeIn(side), run_time=0.8)

    # --- 6. Down the time axis: y against x, the path ------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(side), stage.fade(shadows["wall"], 0.25), stage.fade(shadows["front"], 1.0),
               *stage.turn(yaw=0.0, pitch=0.0, run_time=2.6), run_time=2.6)
    front = VGroup(txt('y(x)', cfg.FONT["label"], cfg.GOLD),
                   txt('Trajectory', cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.15).move_to([0, 3.0, 0])
    scene.play(FadeIn(front), run_time=0.8)
    scene.play(*stage.turn(yaw=-0.5, pitch=0.3, run_time=2.4), run_time=2.4)

    # --- 7. Algebra: x = v0 cos(theta) t, solve for t ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(front), run_time=0.3)
    scene.play(stage.glide([-3.7, -0.6, 0], run_time=0.9), stage.zoom_to(0.62, run_time=0.9), run_time=0.9)
    scene.play(*[stage.fade(tg, 1.0) for tg in tags], run_time=0.3)
    s1 = paint(eq([r"x", "=", r"v_0\cos\theta\ ", "t"], cfg.FONT["section"]), {0: cfg.X_COLOR, 3: cfg.TIME})
    s1.move_to([3.6, 3.2, 0])
    scene.play(Write(s1), run_time=1.4)

    # --- 8. t = x / (v0 cos theta) -----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    s2 = paint(eq([r"t", "=", r"\frac{x}{v_0\cos\theta}"], cfg.FONT["section"]), {0: cfg.TIME}).next_to(s1, DOWN, buff=0.45)
    scene.play(Write(s2), run_time=1.4)
    need = txt('v₀cosθ ≠ 0', cfg.FONT["small"], cfg.MUTED).next_to(s2, LEFT, buff=0.4)
    scene.play(FadeIn(need), run_time=0.6)

    # --- 9. Substitute into y ----------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    s3 = paint(eq([r"y", "=", r"v_0\sin\theta\,", "t", r"-\tfrac12 g\,", "t", "^2"], cfg.FONT["body"]), {0: cfg.Y_COLOR, 3: cfg.TIME, 5: cfg.TIME})
    s3.next_to(s2, DOWN, buff=0.45)
    scene.play(FadeOut(need), Write(s3), run_time=1.2)
    scene.play(Indicate(s3[3], color=cfg.TIME, scale_factor=1.4), Indicate(s3[5], color=cfg.TIME, scale_factor=1.4), run_time=1.0)

    # --- 10. The trajectory equation ------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    traj = paint(eq([r"y", "=", r"x\tan\theta", "-", r"\frac{g\,x^2}{2v_0^2\cos^2\theta}"], cfg.FONT["section"]),
                 {0: cfg.Y_COLOR, 2: cfg.X_COLOR, 4: cfg.X_COLOR})
    fit_width(traj, 7.4)
    traj.next_to(s3, DOWN, buff=0.6)
    framed = boxed(traj, cfg.GOLD)
    scene.play(Write(traj), run_time=2.0)
    scene.play(FadeIn(framed[0]), run_time=0.6)
    framed = VGroup(framed[0], traj)

    # --- 11. y = A x - B x^2 ---------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    form = paint(eq([r"y", "=", "A", r"\,x", "-", "B", r"\,x^2"], cfg.FONT["title"]), {0: cfg.Y_COLOR, 2: cfg.GOLD, 3: cfg.X_COLOR,
                                                                                    5: cfg.GOLD, 6: cfg.X_COLOR})
    scene.play(FadeOut(VGroup(s1, s2, s3)), run_time=0.4)
    scene.play(framed.animate.move_to([3.6, 2.4, 0]), run_time=0.4)
    form.next_to(framed, DOWN, buff=0.6)
    consts = txt("A, B: constants", cfg.FONT["small"], cfg.GOLD).next_to(form, DOWN, buff=0.25)
    scene.play(FadeIn(form, shift=DOWN * 0.2), run_time=1.4)
    scene.play(FadeIn(consts), run_time=0.6)

    # --- 12. A quadratic in x: a parabola ---------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    scene.play(*stage.turn(yaw=0.0, pitch=0.0, run_time=1.6), stage.fade(shadows["floor"], 0.0), stage.fade(shadows["wall"], 0.0),
               run_time=1.6)
    quad = txt("quadratic → parabola", cfg.FONT["label"], cfg.GOLD).move_to([-3.7, 2.4, 0])
    scene.play(FadeIn(quad), run_time=0.6)

    # --- 13. It emerges -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    emerges = result_label('y = Ax − Bx²', cfg.GOLD, cfg.FONT["small"])
    fit_width(emerges, 7.2)
    emerges.move_to([3.6, -2.4, 0])
    scene.play(FadeIn(emerges, shift=UP * 0.15), run_time=0.9)
    clock.value = 0.0
    scene.play(clock.to(stage, P.flight_time, run_time=3.0, rate_func=linear))

    # --- 14. Numbers next ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    nxt = chip('T · H · R', cfg.CYAN, cfg.FONT["label"]).move_to([3.6, -3.5, 0])
    scene.play(FadeIn(nxt, shift=UP * 0.2), *stage.turn(yaw=-0.5, pitch=0.3, run_time=2.4), run_time=2.4)
    scene.wait(1.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["23"])
