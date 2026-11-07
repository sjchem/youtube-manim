"""Scene 17 — a ball on a string, on a smooth 3D table. The reference ball
(0.35x real time) circles a post; the string's green tension is the only
horizontal force, so T = m v^2 / r. Three predictions for the moment the
string snaps — straight out, keep circling, along the tangent — are drawn as
guides. Then it snaps: tension vanishes, and the ball keeps the velocity it
had at that instant, so it travels the tangent in a straight line, covering
equal distances in equal times (strobe ghosts). A 2D inset closes the scene:
on a vertical circle, gravity still acts after release, so the path is a
projectile's parabola (g = 9.8 m/s^2, from the release velocity).
"""

from manim_scenes.common import *

R = 2.4
SLOW = 0.35
H = 0.2
RELEASE = 0.3                 # release angle (rad): the right side, so the tangent runs away from the viewer
POST_TOP = np.array([0.0, 0.42, 0.0])


class Scene17String(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "17", "A ball on a string")
    stage = Stage((0.4, -0.85, 0), zoom=1.22, yaw=-0.3, pitch=0.72, sway=0.03)
    table = Face([ground(-4.2, -3.4), ground(4.2, -3.4), ground(4.2, 3.4), ground(-4.2, 3.4)], "#5B4636", opacity=0.55, edge_opacity=0.7)
    table.bias = -1e4
    sheen = Grid((0, 0.002, 0), (1, 0, 0), (0, 0, 1), (-4.2, 4.2), (-3.4, 3.4), step=0.7, major=0, color="#8C6E57", opacity=0.18)
    base = Ball(np.array([0.0, 0.05, 0.0]), 0.12, "#5D7488", layers=12)
    knob = Ball(POST_TOP, 0.1, "#9DB4C7", layers=12)
    post = Rod(base, knob, width=16, dark="#24384A", light="#9DB4C7")
    stage.add_body(table, sheen, post, base, knob)

    # The ball: on the circle until it is released, then in a straight line at its release velocity.
    orbit = Circuit(stage, P, R=R, height=H, kv=1.15 / P.v, phase=0.0)
    stage.drop(orbit.ball)
    state = {"released": None}
    fly = Knob(0.0)                       # seconds since release (model time)

    def ball_point() -> np.ndarray:
        if state["released"] is None:
            return orbit.world()
        t0 = state["released"]
        return orbit.world(t0) + ground_vec(orbit.view.vel(t0) * (R / P.r)) * fly.value

    ball = Ball(ball_point, 0.2, cfg.BALL)
    ball.keep_in_frame = True
    string = Segment(POST_TOP, ball_point, cfg.WHITE, width=3, opacity=0.9)
    stage.add_body(string, ball)
    show(scene, stage, 1.2)
    scene.play(orbit.run(4.0, 4.0 / SLOW * 0.9), run_time=4.0 / SLOW * 0.9)

    # --- 2. Tangential velocity; the string pulls inward -------------------------------------------------------------------
    beat(scene, t, 1)
    v_arrow = Vector(ball_point, lambda: ball_point() + ground_vec((orbit.view.vel(state["released"] if state["released"] is not None else orbit.t))
                                                                   * orbit.kv), cfg.VELOCITY, width=0.085, tip=0.27)
    pull = Vector(lambda: orbit.world(), lambda: orbit.world() + (POST_TOP * np.array([1, 0, 1]) + np.array([0, H, 0]) - orbit.world()) * 0.42,
                  cfg.FORCE, width=0.09, tip=0.28)
    for a in (v_arrow, pull):
        a.keep_in_frame = True
        a.presence = 0.0
    stage.add_overlay(v_arrow, pull)
    scene.play(FadeOut(head), stage.fade(v_arrow, 1.0), orbit.run(orbit.t + 0.4, 1.0), run_time=1.0)
    scene.play(stage.fade(pull, 1.0), orbit.run(orbit.t + 0.4, 1.0), run_time=1.0)
    tag = Tag(txt("tension", cfg.FONT["small"], cfg.FORCE), lambda: orbit.world() * 0.62, UP * 0.4)
    tag.presence = 0.0
    stage.add_overlay(tag)
    scene.play(stage.fade(tag, 1.0), orbit.run(orbit.t + 1.2, 1.2 / SLOW), run_time=1.2 / SLOW)

    # --- 3. T = m v^2 / r ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    law = paint(eq([r"T", "=", r"\frac{m v^2}{r}"], cfg.FONT["title"]), {0: cfg.FORCE}).move_to([-4.6, 2.9, 0])
    only = txt("the only horizontal force", cfg.FONT["small"], cfg.MUTED).next_to(law, DOWN, buff=0.3)
    scene.play(Write(law), orbit.run(orbit.t + 0.5, 1.4), run_time=1.4)
    scene.play(FadeIn(only), orbit.run(orbit.t + 0.4, 1.0), run_time=1.0)
    # Carry on to the next pass through the release angle.
    laps = np.ceil((orbit.view.theta(orbit.t) - RELEASE) / TAU)
    t_release = (RELEASE + laps * TAU - orbit.view.phase) / P.angular_speed
    scene.play(orbit.run(t_release, (t_release - orbit.t) / SLOW), run_time=(t_release - orbit.t) / SLOW)

    # --- 4. The string snaps: where does it go? -----------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    # Freeze at the release instant and draw the three predictions from there.
    t0 = orbit.t
    here = orbit.world(t0)
    out = ground_vec(orbit.view.unit_r(t0))
    along = ground_vec(orbit.view.unit_t(t0))
    guide_out = Curve(np.array([here, here + out * 2.4]), cfg.WARNING, width=4, dashed=True, glow=False)
    guide_circle = Curve(np.array([orbit.world(t0 + s) for s in np.linspace(0, 1.6, 40)]), cfg.MUTED, width=4, dashed=True, glow=False)
    guide_tangent = Curve(np.array([here, here + along * 4.2]), cfg.GOLD, width=4, dashed=True, glow=False)
    letters = [Tag(chip(c, color, cfg.FONT["small"]), p) for c, color, p in
               (("A", cfg.WARNING, here + out * 2.7), ("B", cfg.MUTED, orbit.world(t0 + 1.75)), ("C", cfg.GOLD, here + along * 4.55))]
    for item in (guide_out, guide_circle, guide_tangent, *letters):
        item.presence = 0.0
    stage.add_body(guide_out, guide_circle, guide_tangent)
    stage.add_overlay(*letters)
    ask = txt("the string snaps: where?", cfg.FONT["label"], cfg.WHITE).move_to([3.8, 3.3, 0])
    scene.play(FadeIn(ask, shift=DOWN * 0.1), stage.fade(tag, 0.0), run_time=0.8)
    for guide, letter in zip((guide_out, guide_circle, guide_tangent), letters):
        scene.play(stage.fade(guide, 1.0), stage.fade(letter, 1.0), run_time=0.7)
    countdown(scene, [5.4, 1.6, 0], 3, cfg.GOLD)

    # --- 5. Not straight outward -----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    no = Tag(cross_mark(0.26), here + out * 1.4)
    no.presence = 0.0
    stage.add_overlay(no)
    scene.play(stage.fade(no, 1.0), stage.fade(guide_out, 0.35), run_time=0.8)
    scene.wait(1.5)

    # --- 6. It snaps: no inward force; the ball keeps its velocity -------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    flash = Disc(lambda: (POST_TOP + here) / 2, 0.3, cfg.WARNING, normal=(0, 1, 0), opacity=0.7, soft=True)
    flash.presence = 0.0
    stage.add_body(flash)
    state["released"] = t0
    scene.play(stage.fade(flash, 1.0, run_time=0.25), stage.fade(string, 0.0, run_time=0.25), stage.fade(pull, 0.0, run_time=0.25),
               *[stage.fade(p, 0.0, run_time=0.25) for p in (guide_out, guide_circle, letters[0], letters[1], no)],
               run_time=0.25)
    scene.play(stage.fade(flash, 0.0), run_time=0.5)
    none = eq(r"F_{\text{horizontal}} = 0", cfg.FONT["body"], cfg.FORCE).next_to(only, DOWN, buff=0.45)
    scene.play(FadeIn(none, shift=UP * 0.1), run_time=0.8)

    # --- 7. Along the tangent, in a straight line --------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    ghosts = []
    step = 0.15
    for k in range(4):
        scene.play(fly.to(stage, fly.value + step, run_time=step / SLOW, rate_func=linear), run_time=step / SLOW)
        g = Ball(ball_point(), 0.16, cfg.BALL, layers=12)
        g.presence = 0.4
        stage.add_body(g)
        ghosts.append(g)
    scene.play(stage.fade(letters[2], 1.0), Indicate(letters[2].content, color=cfg.GOLD, scale_factor=1.15), stage.fade(guide_circle, 0.0),
               run_time=1.0)
    equal = txt("equal steps, equal times", cfg.FONT["small"], cfg.GOLD).next_to(none, DOWN, buff=0.4).align_to(none, LEFT)
    scene.play(FadeIn(equal), run_time=0.6)

    # --- 8. Newton's first law -------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    first = paint(eq([r"\vec F_{\text{net}} = 0", r"\ \Rightarrow\ ", r"\vec v = \text{constant}"], cfg.FONT["body"]), {0: cfg.FORCE, 2: cfg.VELOCITY})
    fit_width(first, 6.5)
    first.move_to([-3.5, 2.7, 0])
    scene.play(FadeOut(VGroup(ask, law, only, none)), stage.fade(letters[2], 0.0), run_time=0.4)
    scene.remove(ask, law, only, none)
    scene.play(FadeIn(first, shift=UP * 0.1), run_time=0.5)

    # --- 9. A force to turn, not to keep moving --------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    turn = VGroup(txt("force needed to turn,", cfg.FONT["label"], cfg.FORCE),
                  txt("not to keep moving", cfg.FONT["label"], cfg.WHITE)).arrange(DOWN, buff=0.15).move_to([3.8, 0.5, 0])
    scene.play(FadeOut(equal), FadeIn(turn, shift=UP * 0.1), run_time=0.9)

    # --- 10. On a vertical circle, gravity still acts: a projectile ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    hide(scene, stage, 0.8, FadeOut(VGroup(first, turn)))
    box = panel(9.0, 6.0, cfg.MUTED, 0.5).move_to([0, -0.4, 0])
    c2 = np.array([-1.9, -0.4, 0])
    s2 = 1.0                                     # screen units per metre
    loop = Circle(radius=P.r * s2, stroke_color=cfg.MUTED, stroke_width=3, stroke_opacity=0.7).move_to(c2)
    release = -40 * DEGREES                      # released on the way up, on the right
    p0 = c2 + P.r * s2 * np.array([np.cos(release), np.sin(release), 0])
    v0 = P.v * np.array([-np.sin(release), np.cos(release), 0])
    flight = Knob(0.0)
    arc_pts = lambda tt: [p0 + (v0 * s + 0.5 * np.array([0, -pm.G, 0]) * s * s) * s2 for s in np.linspace(0, tt, 50)]  # noqa: E731
    path = live(VMobject(), lambda: VMobject(stroke_color=cfg.GOLD, stroke_width=5).set_points_as_corners(arc_pts(max(flight.value, 1e-3))))
    dot = bead(p0, cfg.BALL, 0.15)
    dot.add_updater(lambda m: m.move_to(arc_pts(max(flight.value, 1e-3))[-1]))
    g_arrow = VecArrow(lambda: dot.get_center(), lambda: dot.get_center() + DOWN * 0.8, cfg.ACCEL, width=0.07)
    label = VGroup(txt("vertical circle", cfg.FONT["small"], cfg.MUTED),
                   txt("gravity → parabola", cfg.FONT["small"], cfg.GOLD)).arrange(DOWN, buff=0.3)
    label.next_to(box.get_top(), DOWN, buff=0.3)
    scene.play(FadeIn(box), Create(loop), FadeIn(dot), FadeIn(label[0]), run_time=1.0)
    scene.add(path, g_arrow)
    scene.play(g_arrow.grow_in(run_time=0.5), run_time=0.5)
    scene.play(flight.to(dot, 0.8, run_time=5.0, rate_func=linear), FadeIn(label[1]), run_time=5.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["17"])
