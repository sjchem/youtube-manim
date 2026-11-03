"""Scene 19 — the launch velocity. A velocity-space close-up at the launcher:
the gold v0 at angle theta resolves into v0 cos(theta) (blue) and
v0 sin(theta) (rose). The reference throw (``physics_models.REFERENCE``,
20 m/s at 45 degrees) gives 14.14 and 14.14 — equal at 45 degrees. Then a
side view: after launch the blue arrow never changes, the rose one shrinks,
flips and grows, and the path bends.
"""

from manim_scenes.common import *

SCALE = 0.26    # screen units per m/s in velocity space


class Scene19Launch(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "19", "The launch velocity")
    o = np.array([-6.0, -2.7, 0])
    speed, angle = Knob(16.0), Knob(62 * DEGREES)
    tip = lambda: o + SCALE * speed.value * np.array([np.cos(angle.value), np.sin(angle.value), 0])  # noqa: E731
    barrel = always_redraw(lambda: Line(o, o + 0.9 * np.array([np.cos(angle.value), np.sin(angle.value), 0]),
                                        stroke_color="#9DB4C7", stroke_width=22))
    base = Circle(radius=0.32, stroke_width=0, fill_color="#5D7488", fill_opacity=1).move_to(o)
    ground = Line([-7.4, o[1], 0], [-0.6, o[1], 0], stroke_color=cfg.MUTED, stroke_width=3)
    v0 = VecArrow(o, tip, cfg.VELOCITY, width=0.13)
    arc = always_redraw(lambda: angle_arc(o, 0, np.degrees(angle.value), 1.2, cfg.WHITE, 4))
    th = eq(r"\theta", cfg.FONT["body"], cfg.WHITE)
    th.add_updater(lambda m: m.move_to(o + 1.6 * np.array([np.cos(angle.value / 2), np.sin(angle.value / 2), 0])))
    v_name = eq(r"\vec{v}_0", cfg.FONT["section"], cfg.VELOCITY)
    v_name.add_updater(lambda m: m.move_to((o + tip()) / 2 + 0.55 * np.array([-np.sin(angle.value), np.cos(angle.value), 0])))
    scene.add(ground, barrel, base, v0)
    scene.play(FadeIn(ground), FadeIn(barrel), FadeIn(base), v0.grow_in(run_time=1.2), run_time=1.2)
    scene.play(Create(arc), FadeIn(th), FadeIn(v_name), run_time=0.8)

    # --- 2. Resolve: v0 cos(theta), v0 sin(theta) -----------------------------------------------------------------------
    beat(scene, t, 1)
    vx = VecArrow(o, lambda: np.array([tip()[0], o[1], 0]), cfg.X_COLOR, width=0.1)
    vy = VecArrow(lambda: np.array([tip()[0], o[1], 0]), tip, cfg.Y_COLOR, width=0.1)
    scene.add(vx, vy)
    scene.play(vx.grow_in(run_time=0.9), run_time=0.9)
    scene.play(vy.grow_in(run_time=0.9), run_time=0.9)
    comps = VGroup(paint(eq([r"v_{0x}", "=", r"v_0\cos\theta"], cfg.FONT["section"]), {0: cfg.X_COLOR, 2: cfg.X_COLOR}),
                   paint(eq([r"v_{0y}", "=", r"v_0\sin\theta"], cfg.FONT["section"]), {0: cfg.Y_COLOR, 2: cfg.Y_COLOR}))
    comps.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.8, 1.8, 0])
    scene.play(Write(comps[0]), run_time=1.2)
    scene.play(Write(comps[1]), run_time=1.2)

    # --- 3. The reference throw: 20 m/s at 45 degrees -------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(speed.to(v0, P.v0, run_time=1.8), angle.to(v0, P.angle * DEGREES, run_time=1.8), run_time=1.8)
    ref = eq([rf"v_0 = {P.v0:.0f}\ \mathrm{{m/s}}", r",\quad", rf"\theta = {P.angle:.0f}^\circ"], cfg.FONT["section"])
    ref.move_to([3.8, 3.3, 0])
    scene.play(fade_through(head, ref), run_time=0.9)

    # --- 4. Horizontal: 14.14 m/s ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    hx = paint(eq([r"v_{0x}", "=", rf"{P.v0:.0f}\cos {P.angle:.0f}^\circ", r"\approx", rf"{VX}\ \mathrm{{m/s}}"], cfg.FONT["body"]),
               {0: cfg.X_COLOR, 4: cfg.X_COLOR})
    hx.move_to([3.8, -0.3, 0])
    scene.play(Write(hx), run_time=1.6)
    vx_tag = eq(VX, cfg.FONT["body"], cfg.X_COLOR).next_to(vx, DOWN, buff=0.25)
    scene.play(FadeIn(vx_tag), run_time=0.6)

    # --- 5. Vertical: also 14.14 m/s ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    hy = paint(eq([r"v_{0y}", "=", rf"{P.v0:.0f}\sin {P.angle:.0f}^\circ", r"\approx", rf"{VY0}\ \mathrm{{m/s}}"], cfg.FONT["body"]),
               {0: cfg.Y_COLOR, 4: cfg.Y_COLOR})
    hy.next_to(hx, DOWN, buff=0.4)
    scene.play(Write(hy), run_time=1.6)
    vy_tag = eq(VY0, cfg.FONT["body"], cfg.Y_COLOR).next_to(vy, RIGHT, buff=0.25)
    scene.play(FadeIn(vy_tag), run_time=0.6)

    # --- 6. Equal at 45 degrees ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    equal = txt("equal at 45°", cfg.FONT["label"], cfg.GOLD).next_to(hy, DOWN, buff=0.35)
    scene.play(FadeIn(equal), Indicate(vx_tag, color=cfg.GOLD), Indicate(vy_tag, color=cfg.GOLD), run_time=1.2)

    # --- 7. Together they rebuild v0 -------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    for m in (th, v_name):
        m.clear_updaters()
    scene.play(FadeOut(VGroup(comps, hx, hy, equal)), run_time=0.6)
    whole = paint(eq([r"\vec{v}_0", "=", r"v_0\cos\theta\,\hat{\imath}", "+", r"v_0\sin\theta\,\hat{\jmath}"], cfg.FONT["section"]),
                  {0: cfg.VELOCITY, 2: cfg.X_COLOR, 4: cfg.Y_COLOR})
    fit_width(whole, 7.6)
    whole.move_to([3.6, 1.0, 0])
    scene.play(Write(whole), run_time=1.8)
    scene.play(Indicate(v0, color=cfg.VELOCITY, scale_factor=1.04), run_time=1.0)

    # --- 8. One throw, two components, treated differently ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    clear(scene)
    grid = plane((0, 45), (0, 12), unit=0.3, at=(-6.8, -3.2, 0), step=5, faint=0.3)
    flight = SideFlight(grid, k=0.075)
    ax_ = flight.arrow("vx", cfg.X_COLOR, width=0.09)
    ay_ = flight.arrow("vy", cfg.Y_COLOR, width=0.09)
    scene.add(grid, flight.trail, flight.ball, ax_, ay_)
    scene.play(FadeIn(grid), FadeIn(flight.ball), ax_.grow_in(run_time=0.8), ay_.grow_in(run_time=0.8), run_time=0.8)
    labels = VGroup(txt('vₓ = constant', cfg.FONT["label"], cfg.X_COLOR), txt('vᵧ(t)', cfg.FONT["label"], cfg.Y_COLOR))
    labels.arrange(RIGHT, buff=0.8).move_to([0, 3.4, 0])
    scene.play(FadeIn(labels), flight.fly(1.0, speed=0.5), run_time=2.0)

    # --- 9. That difference bends the path --------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(flight.fly(speed=0.5))
    bends = result_label('Trajectory', cfg.GOLD, cfg.FONT["body"]).move_to([1.8, 2.5, 0])
    scene.play(FadeIn(bends, shift=UP * 0.15), run_time=0.8)
    scene.wait(2.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["19"])
