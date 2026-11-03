"""Scene 17 — the constant-acceleration equations. On a velocity-time graph
the line v = v0 + a t rises steadily; the area under it is a rectangle
(v0 t) plus a triangle (one half a t squared), which is the displacement.
Eliminating t gives v^2 = v0^2 + 2a(x - x0). In two dimensions the same
equations are written twice — once for x, once for y — and a side-view
flight shows the two projections riding their axes together.
"""

from manim_scenes.common import *

V0, ACC, T_END = 1.5, 0.9, 4.0          # an illustrative 1D motion for the graph


class Scene17Equations(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "17", "Equations of motion")
    knowns = VGroup(chip('x₀', cfg.POSITION), chip('speed', cfg.VELOCITY), chip('a', cfg.ACCEL))
    knowns.arrange(RIGHT, buff=0.5).move_to(UP * 1.2)
    arrow = VecArrow(DOWN * 0.1, DOWN * 1.2, cfg.WHITE, width=0.08, live=False)
    future = txt('x(t) = ?', cfg.FONT["section"], cfg.GOLD).move_to(DOWN * 1.9)
    scene.play(LaggedStart(*[FadeIn(k, shift=UP * 0.2) for k in knowns], lag_ratio=0.3), run_time=1.8)
    scene.play(FadeIn(arrow), FadeIn(future), run_time=1.0)

    # --- 2. Constant acceleration, one dimension ----------------------------------------------------------------------------
    beat(scene, t, 1)
    clear(scene, head)
    axes = Axes(x_range=(0, 5, 1), y_range=(0, 6, 1), x_length=6.6, y_length=5.0, tips=False,
                axis_config={"stroke_color": cfg.MUTED, "stroke_width": 3}).move_to([-3.6, -0.6, 0])
    t_lab = eq("t", cfg.FONT["body"], cfg.TIME).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
    v_lab = eq("v", cfg.FONT["body"], cfg.VELOCITY).next_to(axes.y_axis.get_end(), UP, buff=0.15)
    scene.play(Create(axes), FadeIn(t_lab), FadeIn(v_lab), run_time=1.2)
    steps = VGroup(*[Line(axes.c2p(k, V0 + ACC * k), axes.c2p(k + 1, V0 + ACC * k), stroke_color=cfg.MUTED, stroke_width=2)
                     for k in range(4)],
                   *[Line(axes.c2p(k + 1, V0 + ACC * k), axes.c2p(k + 1, V0 + ACC * (k + 1)), stroke_color=cfg.ACCEL, stroke_width=4)
                     for k in range(4)])
    scene.play(Create(steps), run_time=1.6)
    same = txt('Δv = aΔt', cfg.FONT["small"], cfg.ACCEL).next_to(axes.c2p(4, 5.2), UP, buff=0.1)
    scene.play(FadeIn(same), run_time=0.6)

    # --- 3. v = v0 + a t: a straight line ---------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    line = axes.plot(lambda x: V0 + ACC * x, x_range=(0, T_END), color=cfg.VELOCITY, stroke_width=6)
    eq1 = paint(eq([r"v", "=", r"v_0", "+", r"a\,t"], cfg.FONT["section"]), {0: cfg.VELOCITY, 2: cfg.VELOCITY, 4: cfg.ACCEL})
    eq1.move_to([3.9, 2.7, 0])
    scene.play(FadeOut(VGroup(steps, same)), Create(line), run_time=1.4)
    scene.play(Write(eq1), run_time=1.2)

    # --- 4. Signed area = displacement
    beat(scene, t, 3)
    area = axes.get_area(line, x_range=(0, T_END), color=cfg.POSITION, opacity=0.35)
    scene.play(FadeIn(area), run_time=1.2)
    area_lab = txt('Δx', cfg.FONT["small"], cfg.POSITION).next_to(axes.c2p(2, 0.6), UP, buff=0.1)
    scene.play(FadeIn(area_lab), run_time=0.6)

    # --- 5. Rectangle + triangle ----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    rect = Polygon(axes.c2p(0, 0), axes.c2p(T_END, 0), axes.c2p(T_END, V0), axes.c2p(0, V0), stroke_color=cfg.POSITION,
                   stroke_width=3, fill_color=cfg.POSITION, fill_opacity=0.45)
    tri = Polygon(axes.c2p(0, V0), axes.c2p(T_END, V0), axes.c2p(T_END, V0 + ACC * T_END), stroke_color=cfg.ACCEL, stroke_width=3,
                  fill_color=cfg.ACCEL, fill_opacity=0.45)
    rect_lab = eq(r"v_0\,t", cfg.FONT["body"], cfg.WHITE).move_to(rect)
    tri_lab = eq(r"\tfrac12 a t^2", cfg.FONT["body"], cfg.WHITE).move_to(tri.get_center() + DOWN * 0.1 + RIGHT * 0.5)
    scene.play(FadeOut(area), fade_through(area_lab, rect_lab), FadeIn(rect), run_time=1.0)
    scene.play(FadeIn(tri), FadeIn(tri_lab), run_time=1.0)

    # --- 6. x = x0 + v0 t + 1/2 a t^2 ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    eq2 = paint(eq([r"x", "=", r"x_0", "+", r"v_0 t", "+", r"\tfrac12 a t^2"], cfg.FONT["section"]),
                {0: cfg.POSITION, 2: cfg.POSITION, 4: cfg.POSITION, 6: cfg.ACCEL})
    eq2.next_to(eq1, DOWN, buff=0.5)
    scene.play(TransformFromCopy(rect_lab, eq2[4]), TransformFromCopy(tri_lab, eq2[6]),
               FadeIn(VGroup(eq2[0], eq2[1], eq2[2], eq2[3], eq2[5])), run_time=1.6)

    # --- 7. Eliminate t: v^2 = v0^2 + 2a(x - x0) ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    eq3 = paint(eq([r"v^2", "=", r"v_0^2", "+", r"2a\,(x - x_0)"], cfg.FONT["section"]), {0: cfg.VELOCITY, 2: cfg.VELOCITY, 4: cfg.ACCEL})
    eq3.next_to(eq2, DOWN, buff=0.5)
    no_t = txt("no t", cfg.FONT["small"], cfg.TIME).next_to(eq3, LEFT, buff=0.35)
    scene.play(Write(eq3), run_time=1.8)
    scene.play(FadeIn(no_t), run_time=0.6)

    # --- 8. Valid when a is constant along that axis ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    box = glow_frame(VGroup(eq1, eq2, eq3), cfg.GOLD, buff=0.3)
    cond = txt('a = constant', cfg.FONT["label"], cfg.GOLD).next_to(box, DOWN, buff=0.3)
    scene.play(Create(box), FadeIn(cond), run_time=1.2)

    # --- 9. Two dimensions: no new equations ---------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    clear(scene, head)
    none = txt('x · y', cfg.FONT["title"], cfg.WHITE)
    scene.play(FadeIn(none, scale=0.95), run_time=1.0)

    # --- 10. The same equations twice ---------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    cols = VGroup(
        VGroup(txt("horizontal", cfg.FONT["body"], cfg.X_COLOR),
               eq(r"x(t) = x_0 + v_{0x} t + \tfrac12 a_x t^2", cfg.FONT["body"], cfg.X_COLOR),
               eq(r"v_x(t) = v_{0x} + a_x t", cfg.FONT["body"], cfg.X_COLOR)).arrange(DOWN, buff=0.35),
        VGroup(txt("vertical", cfg.FONT["body"], cfg.Y_COLOR),
               eq(r"y(t) = y_0 + v_{0y} t + \tfrac12 a_y t^2", cfg.FONT["body"], cfg.Y_COLOR),
               eq(r"v_y(t) = v_{0y} + a_y t", cfg.FONT["body"], cfg.Y_COLOR)).arrange(DOWN, buff=0.35))
    for col in cols:
        fit_width(col, 7.0)
    cols.arrange(RIGHT, buff=0.8).move_to(UP * 0.5)
    divider = Line(UP * 1.6, DOWN * 1.6, stroke_color=cfg.MUTED, stroke_width=2).move_to(cols)
    scene.play(none.animate.scale(0.6).move_to(UP * 2.9), run_time=0.5)
    scene.play(FadeIn(cols[0][0]), FadeIn(cols[1][0]), Create(divider), run_time=0.5)

    # --- 11. x uses horizontal parts, y uses vertical parts ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(Write(cols[0][1]), run_time=1.6)
    scene.play(Write(cols[0][2]), run_time=1.2)
    scene.play(Write(cols[1][1]), run_time=1.6)
    scene.play(Write(cols[1][2]), run_time=1.2)

    # --- 12. Calculate each, then combine ----------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    clear(scene, head)
    grid = plane((0, 45), (0, 12), unit=0.22, at=(-5.0, -2.9, 0), step=5, faint=0.3)
    flight = SideFlight(grid, k=0.07)
    px = always_redraw(lambda: glow_dot(grid.c2p(float(P.x(flight.clock.value)), 0), cfg.X_COLOR, 0.1))
    py = always_redraw(lambda: glow_dot(grid.c2p(0, float(P.y(flight.clock.value))), cfg.Y_COLOR, 0.1))
    guides = always_redraw(lambda: VGroup(
        dashed_path(flight.point(flight.clock.value), grid.c2p(float(P.x(flight.clock.value)), 0), cfg.X_COLOR, 2.4, 0.7),
        dashed_path(flight.point(flight.clock.value), grid.c2p(0, float(P.y(flight.clock.value))), cfg.Y_COLOR, 2.4, 0.7)))
    combine = paint(eq([r"\vec{r}(t)", "=", r"x(t)\,\hat{\imath}", "+", r"y(t)\,\hat{\jmath}"], cfg.FONT["section"]),
                    {0: cfg.POSITION, 2: cfg.X_COLOR, 4: cfg.Y_COLOR}).move_to([3.4, 2.7, 0])
    scene.play(FadeIn(grid), FadeIn(flight.trail), FadeIn(flight.ball), FadeIn(px), FadeIn(py), FadeIn(guides), Write(combine),
               run_time=1.2)
    scene.play(flight.fly(speed=0.55))

    # --- 13. Ready for the flying ball ------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    ready = result_label('Projectile motion', cfg.GOLD, cfg.FONT["section"]).move_to([3.4, 1.4, 0])
    flight.clock.value = 0.0
    scene.play(FadeIn(ready, shift=UP * 0.15), flight.fly(speed=0.5), run_time=P.flight_time / 0.5)
    scene.wait(1.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["17"])
