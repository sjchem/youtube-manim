"""Scene 24 — time of flight and maximum height, on a y-t graph of the
reference throw. y(T) = 0 factors into T = 0 (launch) or T = 2 v0 sin / g =
2.89 s; the apex sits halfway, at t_H = v0 sin / g = 1.44 s, where v_y = 0;
substituting gives H = v0^2 sin^2 / 2g = 10.20 m. A steeper throw at the
same speed has a bigger vertical component and climbs higher.
"""

from manim_scenes.common import *

STEEP = pm.TABLE[2]


class Scene24TimeHeight(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "24")
    opener = txt("Flight time, maximum height and range", cfg.FONT["title"], cfg.WHITE)
    fit_width(opener, 12.4)
    opener.move_to(ORIGIN)
    scene.play(FadeIn(opener, shift=LEFT * 0.3), run_time=0.9)
    scene.wait(0.9)
    scene.play(FadeOut(opener, shift=UP * 0.3), run_time=0.6)
    head = heading("Flight time and height")
    rules = VGroup(chip('y𝒻 = y₀', cfg.CYAN), chip("constant g", cfg.ACCEL), chip("no air", cfg.MUTED))
    rules.arrange(RIGHT, buff=0.4).move_to(UP * 2.9)
    scene.play(FadeIn(head, shift=DOWN * 0.15), LaggedStart(*[FadeIn(r, shift=DOWN * 0.2) for r in rules], lag_ratio=0.3), run_time=1.4)

    # --- 2. How long in the air? Until y returns to zero ----------------------------------------------------------------
    beat(scene, t, 1)
    axes = Axes(x_range=(0, 3.2, 0.5), y_range=(0, 12, 2), x_length=6.6, y_length=4.6, tips=False,
                axis_config={"stroke_color": cfg.MUTED, "stroke_width": 3}).move_to([-3.7, -0.6, 0])
    labels = VGroup(eq("t", cfg.FONT["body"], cfg.TIME).next_to(axes.x_axis.get_end(), RIGHT, buff=0.15),
                    eq("y", cfg.FONT["body"], cfg.Y_COLOR).next_to(axes.y_axis.get_top(), UP, buff=0.1))
    clock = Knob(0.0)
    curve = always_redraw(lambda: axes.plot(lambda x: float(P.y(x)), x_range=(0, max(clock.value, 0.01)), color=cfg.Y_COLOR,
                                            stroke_width=6))
    dot = always_redraw(lambda: glow_dot(axes.c2p(clock.value, float(P.y(clock.value))), cfg.BALL, 0.09))
    scene.play(FadeOut(rules), Create(axes), FadeIn(labels), run_time=1.0)
    scene.add(curve, dot)
    scene.play(clock.to(axes, P.flight_time, run_time=2.6, rate_func=linear))
    land = glow_dot(axes.c2p(P.flight_time, 0), cfg.GREEN, 0.11, reach=4)
    scene.play(FadeIn(land, scale=1.4), run_time=0.6)

    # --- 3. Set y(T) = 0 and factor -------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    col_x = 0.5
    e1 = paint(eq([r"0", "=", r"v_0\sin\theta\,T", r"-\tfrac12 g T^2"], cfg.FONT["body"]), {2: cfg.Y_COLOR, 3: cfg.ACCEL})
    e2 = paint(eq([r"0", "=", "T", r"\left(v_0\sin\theta - \tfrac12 g T\right)"], cfg.FONT["body"]), {2: cfg.TIME})
    e1.move_to([col_x, 2.1, 0], aligned_edge=LEFT)
    e2.next_to(e1, DOWN, buff=0.35).align_to(e1, LEFT)
    scene.play(Write(e1), run_time=1.4)
    scene.play(Write(e2), run_time=1.4)

    # --- 4. T = 0: the launch ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    root0 = VGroup(eq("T = 0", cfg.FONT["body"], cfg.MUTED), txt("launch", cfg.FONT["small"], cfg.MUTED)).arrange(RIGHT, buff=0.3)
    root0.next_to(e2, DOWN, buff=0.4).align_to(e1, LEFT)
    start_dot = glow_dot(axes.c2p(0, 0), cfg.MUTED, 0.1, reach=4)
    scene.play(FadeIn(root0), FadeIn(start_dot), run_time=1.0)

    # --- 5. T = 2 v0 sin(theta) / g ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    flight_t = paint(eq([r"T", "=", r"\frac{2v_0\sin\theta}{g}"], cfg.FONT["section"]), {0: cfg.TIME})
    flight_t.next_to(root0, DOWN, buff=0.4).align_to(e1, LEFT)
    box_t = boxed(flight_t, cfg.TIME)
    scene.play(Write(flight_t), run_time=1.4)
    scene.play(FadeIn(box_t[0]), run_time=0.5)

    # --- 6. About 2.89 s -----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    t_num = eq([r"\approx", rf"{T_FLIGHT}\ \mathrm{{s}}"], cfg.FONT["body"], cfg.TIME).next_to(box_t, RIGHT, buff=0.3)
    t_tag = eq(rf"{T_FLIGHT}\ \mathrm{{s}}", cfg.FONT["small"], cfg.GREEN).next_to(axes.c2p(P.flight_time, 0), DOWN, buff=0.7)
    scene.play(FadeIn(t_num), FadeIn(t_tag), run_time=1.0)

    # --- 7. Rise time = fall time -------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    half = DashedLine(axes.c2p(P.apex_time, 0), axes.c2p(P.apex_time, P.max_height), stroke_color=cfg.WHITE, stroke_width=3)
    sym = VGroup(Line(axes.c2p(0, -0.9), axes.c2p(P.apex_time - 0.03, -0.9), stroke_color=cfg.GOLD, stroke_width=5),
                 Line(axes.c2p(P.apex_time + 0.03, -0.9), axes.c2p(P.flight_time, -0.9), stroke_color=cfg.GOLD, stroke_width=5))
    scene.play(Create(half), run_time=0.8)
    scene.play(Create(sym), run_time=0.8)
    up_down = txt("rise = fall", cfg.FONT["label"], cfg.GOLD).next_to(sym, DOWN, buff=0.15)
    scene.play(FadeIn(up_down), run_time=0.6)

    # --- 8. Maximum height: v_y = 0 at the top -----------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(e1, e2, root0, start_dot)), FadeOut(head), run_time=0.4)
    scene.play(VGroup(box_t, t_num).animate.move_to([col_x, 3.0, 0], aligned_edge=LEFT), run_time=0.5)
    apex = glow_dot(axes.c2p(P.apex_time, P.max_height), cfg.GOLD, 0.11, reach=4)
    vy0 = paint(eq([r"v_y", "=", r"v_0\sin\theta - g\,t", "= 0"], cfg.FONT["body"]), {0: cfg.Y_COLOR})
    vy0.move_to([col_x, 1.6, 0], aligned_edge=LEFT)
    scene.play(FadeIn(apex, scale=1.4), Write(vy0), run_time=1.4)

    # --- 9. t_H = v0 sin(theta) / g = 1.44 s ---------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    t_h = paint(eq([r"t_H", "=", r"\frac{v_0\sin\theta}{g}", r"\approx", rf"{T_TOP}\ \mathrm{{s}}"], cfg.FONT["body"]),
                {0: cfg.TIME, 4: cfg.TIME}).next_to(vy0, DOWN, buff=0.4).align_to(vy0, LEFT)
    scene.play(Write(t_h), run_time=1.6)
    th_tag = eq(rf"{T_TOP}\ \mathrm{{s}}", cfg.FONT["small"], cfg.GOLD).next_to(axes.c2p(P.apex_time, 0), DOWN, buff=0.3)
    scene.play(FadeOut(up_down), FadeOut(sym), run_time=0.35)
    scene.play(FadeIn(th_tag), run_time=0.35)

    # --- 10. Into the height equation ------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    sub = paint(eq([r"H", "=", r"v_0\sin\theta\,t_H - \tfrac12 g\,t_H^2"], cfg.FONT["body"]), {0: cfg.Y_COLOR})
    sub.next_to(t_h, DOWN, buff=0.4).align_to(t_h, LEFT)
    scene.play(Write(sub), run_time=1.4)

    # --- 11. H = v0^2 sin^2(theta) / 2g --------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    h_eq = paint(eq([r"H", "=", r"\frac{v_0^2\sin^2\theta}{2g}"], cfg.FONT["section"]), {0: cfg.Y_COLOR})
    h_eq.next_to(sub, DOWN, buff=0.4).align_to(sub, LEFT)
    box_h = boxed(h_eq, cfg.Y_COLOR)
    scene.play(Write(h_eq), run_time=1.4)
    scene.play(FadeIn(box_h[0]), run_time=0.5)

    # --- 12. 20^2 sin^2 45 / (2 x 9.8) ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    scene.play(FadeOut(VGroup(vy0, sub)), run_time=0.4)
    scene.play(t_h.animate.move_to([col_x, 1.22, 0], aligned_edge=LEFT),
               box_h.animate.move_to([col_x, -0.62, 0], aligned_edge=LEFT), run_time=0.5)
    nums = eq([r"H", "=", rf"\frac{{{P.v0:.0f}^2\,\sin^2 {P.angle:.0f}^\circ}}{{2 \times {G_TEXT}}}"], cfg.FONT["label"])
    paint(nums, {0: cfg.Y_COLOR}).next_to(box_h, DOWN, buff=0.4).align_to(box_h, LEFT)
    scene.play(Write(nums), run_time=1.6)

    # --- 13. About 10.20 m ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    h_num = eq([r"\approx", rf"{H_MAX}\ \mathrm{{m}}"], cfg.FONT["section"], cfg.Y_COLOR).next_to(nums, RIGHT, buff=0.3)
    h_line = DashedLine(axes.c2p(0, P.max_height), axes.c2p(P.apex_time, P.max_height), stroke_color=cfg.Y_COLOR, stroke_width=3)
    h_tag = eq(rf"{H_MAX}\ \mathrm{{m}}", cfg.FONT["small"], cfg.Y_COLOR).next_to(axes.c2p(0.4, P.max_height), UP, buff=0.15)
    scene.play(FadeIn(h_num), Create(h_line), FadeIn(h_tag), run_time=1.2)

    # --- 14. Steeper throw: a bigger vertical component ------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    for m in (curve, dot):
        m.clear_updaters()
    clear(scene)
    grid = plane((0, 45), (0, 17), unit=0.2, at=(-6.6, -3.2, 0), step=5, faint=0.3)
    low, steep = SideFlight(grid, P, k=0.06), SideFlight(grid, STEEP, k=0.06, color=cfg.PURPLE, trail_color=cfg.PURPLE)
    arrows = [low.arrow("vy", cfg.Y_COLOR, width=0.08), steep.arrow("vy", cfg.Y_COLOR, width=0.08)]
    scene.add(grid, low.trail, steep.trail, low.ball, steep.ball, *arrows)
    scene.play(FadeIn(grid), FadeIn(low.ball), FadeIn(steep.ball), *[a.grow_in(run_time=0.8) for a in arrows], run_time=0.8)
    names = VGroup(txt(f"{P.angle:.0f}°", cfg.FONT["label"], cfg.GOLD), txt(f"{STEEP.angle:.0f}°", cfg.FONT["label"], cfg.PURPLE))
    names.arrange(DOWN, buff=0.3).move_to([3.0, 1.6, 0])
    scene.play(FadeIn(names), low.fly(P.apex_time, speed=0.5), steep.fly(STEEP.apex_time, speed=0.5),
               run_time=STEEP.apex_time / 0.5)

    # --- 15. It rises higher ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 14)
    heights = VGroup(eq(rf"H \approx {H_MAX}\ \mathrm{{m}}", cfg.FONT["body"], cfg.GOLD),
                     eq(rf"H = {md.fixed(STEEP.max_height, 2)}\ \mathrm{{m}}", cfg.FONT["body"], cfg.PURPLE))
    for h, n in zip(heights, names):
        h.next_to(n, RIGHT, buff=0.4)
    scene.play(FadeIn(heights), low.fly(speed=0.5), steep.fly(speed=0.5), run_time=(STEEP.flight_time - STEEP.apex_time) / 0.5)
    angle_too = txt('H(θ)', cfg.FONT["label"], cfg.WHITE).move_to([2.6, 3.0, 0])
    scene.play(FadeIn(angle_too), run_time=0.7)
    scene.wait(2.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["24"])
