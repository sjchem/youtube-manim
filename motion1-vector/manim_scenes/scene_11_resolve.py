"""Scene 11 — resolving a vector. Light from straight above casts the
vector's shadow on the x-axis (its horizontal component, blue); light from
the side casts its shadow on the y-axis (the vertical component, rose).
Tip to tail, the two shadows rebuild the arrow exactly. Then a sled pulled
by a rope at 30 degrees (``physics_models.SLED_PULL``): one pull, two
descriptions — part drags the sled forward, part lifts it.
"""

from manim_scenes.common import *

A_V = (4.8, 3.3)
PULL_N, PULL_DEG = pm.SLED_PULL


class Scene11Resolve(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "11")
    opener = txt("Vector components and resolution", cfg.FONT["title"], cfg.WHITE)
    fit_width(opener, 12.4)
    opener.move_to(ORIGIN)
    scene.play(FadeIn(opener, shift=LEFT * 0.3), run_time=0.9)
    scene.wait(1.0)
    scene.play(FadeOut(opener, shift=UP * 0.3), run_time=0.6)
    head = heading("Resolving a vector")
    stage = field_stage((-3.4, -1.8, 0), zoom=0.95, yaw=-0.25, pitch=0.18,
                        x_range=(-2.8, 3.7), z_range=(-1.5, 1.5), sway=0.025)
    origin = np.array([-2.0, 0.0, 0.0])
    end = origin + np.array([*A_V, 0.0])
    corner = origin + np.array([A_V[0], 0.0, 0.0])
    upright = origin + np.array([0.0, A_V[1], 0.0])
    growth, slide = Knob(0.0), Knob(0.0)
    A = Vector(origin, lambda: origin + growth.value * (end - origin), cfg.VEC_A, width=0.13)
    cx = Vector(origin, corner, cfg.X_COLOR, width=0.11)
    cy = Vector(lambda: origin + RIGHT * slide.value,
                lambda: upright + RIGHT * slide.value, cfg.Y_COLOR, width=0.11)
    cx.presence = cy.presence = 0.0
    axes = [Segment(origin, corner + RIGHT * 0.6, cfg.X_COLOR, width=3),
            Segment(origin, upright + UP * 0.7, cfg.Y_COLOR, width=3)]
    a_name = Tag(eq(r"\vec A", cfg.FONT["section"], cfg.VEC_A), (origin + end) / 2, UP * 1.3 + LEFT * 0.25)
    ax_lab = Tag(eq("A_x", cfg.FONT["section"], cfg.X_COLOR), (origin + corner) / 2, DOWN * 0.45)
    ay_lab = Tag(eq("A_y", cfg.FONT["section"], cfg.Y_COLOR),
                 lambda: (origin + upright) / 2 + RIGHT * slide.value, LEFT * 0.55)
    ax_lab.presence = ay_lab.presence = 0.0
    stage.add_body(*axes)
    stage.add_overlay(A, cx, cy, a_name, ax_lab, ay_lab)
    show(scene, stage, 0.8, FadeIn(head, shift=DOWN * 0.15))
    scene.play(growth.to(stage, 1.0, run_time=1.2))

    beat(scene, t, 1)
    qs = VGroup(eq("A_x = ?", cfg.FONT["section"], cfg.X_COLOR),
                eq("A_y = ?", cfg.FONT["section"], cfg.Y_COLOR))
    qs.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([3.9, 1.4, 0])
    scene.play(LaggedStart(*[FadeIn(q, shift=LEFT * 0.2) for q in qs], lag_ratio=0.5), run_time=1.4)

    # Parallel light rays project onto the axes. The lamps mark the lighting
    # direction; they are not point sources (which would distort the shadows).
    beat(scene, t, 2)
    top_lamp = Ball(origin + np.array([A_V[0] / 2, 4.5, 0]), 0.16, cfg.GOLD)
    top_glow = Halo(top_lamp, cfg.GOLD, reach=3.0)
    down_rays = [Segment(origin + np.array([x, 4.2, 0]), origin + np.array([x, 0, 0]),
                         cfg.GOLD, width=2, opacity=0.25) for x in np.linspace(0.2, A_V[0], 8)]
    for body in (top_lamp, top_glow, *down_rays):
        body.presence = 0.0
    stage.add_body(top_glow, top_lamp, *down_rays)
    scene.play(stage.fade(top_lamp, 1.0), stage.fade(top_glow, 1.0), run_time=0.6)
    scene.play(*[stage.fade(ray, 1.0) for ray in down_rays], run_time=1.0)
    scene.play(stage.fade(cx, 1.0), stage.fade(ax_lab, 1.0), run_time=1.0)

    beat(scene, t, 3)
    side_lamp = Ball(origin + np.array([6.0, A_V[1] / 2, 0]), 0.16, cfg.GOLD)
    side_glow = Halo(side_lamp, cfg.GOLD, reach=3.0)
    side_rays = [Segment(origin + np.array([5.7, y, 0]), origin + np.array([0, y, 0]),
                         cfg.GOLD, width=2, opacity=0.25) for y in np.linspace(0.2, A_V[1], 7)]
    for body in (side_lamp, side_glow, *side_rays):
        body.presence = 0.0
    stage.add_body(side_glow, side_lamp, *side_rays)
    scene.play(*[stage.fade(body, 0.0) for body in (top_lamp, top_glow, *down_rays)],
               FadeOut(qs), stage.fade(side_lamp, 1.0), stage.fade(side_glow, 1.0), run_time=0.7)
    scene.play(*[stage.fade(ray, 1.0) for ray in side_rays], run_time=1.0)
    scene.play(stage.fade(cy, 1.0), stage.fade(ay_lab, 1.0), run_time=1.0)

    beat(scene, t, 4)
    original_y = Segment(origin, upright, cfg.Y_COLOR, width=5, opacity=0.2)
    guide = Segment(upright, end, cfg.MUTED, dashed=True, opacity=0.35)
    triangle = Face([origin, corner, end], cfg.VEC_A, opacity=0.06, edge_opacity=0.0)
    stage.add_body(original_y, guide, triangle)
    scene.play(*[stage.fade(body, 0.0) for body in (side_lamp, side_glow, *side_rays)], run_time=0.6)
    scene.play(slide.to(stage, A_V[0], run_time=1.6),
               *stage.turn(yaw=-0.08, pitch=0.10, run_time=1.6), run_time=1.6)
    scene.play(stage.fade(A, 0.35), run_time=0.6)
    scene.play(stage.fade(A, 1.0), run_time=0.8)

    beat(scene, t, 5)
    form = paint(eq([r"\vec{A}", "=", "A_x", r"\,\hat{\imath}", "+", "A_y", r"\,\hat{\jmath}"], cfg.FONT["section"]),
                 {0: cfg.VEC_A, 2: cfg.X_COLOR, 3: cfg.X_COLOR, 5: cfg.Y_COLOR, 6: cfg.Y_COLOR}).move_to([3.9, 1.5, 0])
    fit_width(form, 6.0)
    scene.play(Write(form), run_time=1.6)

    beat(scene, t, 6)
    # Rejoin the components visually; only one endpoint and one vector remain.
    endpoint = Ball(end, 0.14, cfg.VEC_A)
    stage.add_body(endpoint, Halo(endpoint, cfg.VEC_A, reach=2.5))
    scene.play(stage.fade(cx, 0.3), stage.fade(cy, 0.3),
               *stage.turn(yaw=-0.32, pitch=0.22, run_time=1.6), run_time=1.6)

    # --- 8. A sled and a rope -------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    clear(scene)
    snow_y = -2.0
    snow = VGroup(Rectangle(width=16, height=2.6, stroke_width=0, fill_color="#DDEBF5", fill_opacity=0.12).move_to([0, snow_y - 1.3, 0]),
                  Line([-8, snow_y, 0], [8, snow_y, 0], stroke_color="#DDEBF5", stroke_width=4, stroke_opacity=0.7))
    x = Knob(-4.0)
    sled = VGroup(Polygon([-1.1, 0.12, 0], [1.0, 0.12, 0], [1.2, 0.5, 0], [-1.1, 0.5, 0], stroke_color=mu.shade(cfg.ORANGE, 0.6),
                          stroke_width=3, fill_color=cfg.ORANGE, fill_opacity=0.9),
                  VMobject(stroke_color=cfg.MUTED, stroke_width=6).set_points_smoothly([[-1.3, 0.0, 0], [0.9, 0.0, 0], [1.3, 0.25, 0]]),
                  RoundedRectangle(width=1.1, height=0.75, corner_radius=0.1, stroke_color=mu.shade(cfg.CYAN, 0.6), stroke_width=3,
                                   fill_color=cfg.CYAN, fill_opacity=0.8).move_to([-0.3, 0.88, 0]))
    sled.add_updater(lambda m: m.move_to([x.value, snow_y + 0.62, 0]))
    hook = lambda: np.array([x.value + 1.2, snow_y + 0.7, 0])  # noqa: E731
    d = np.array([np.cos(np.radians(PULL_DEG)), np.sin(np.radians(PULL_DEG)), 0])
    rope = always_redraw(lambda: Line(hook(), hook() + d * 4.4, stroke_color="#E8D9B5", stroke_width=4))
    hand = always_redraw(lambda: Circle(radius=0.16, stroke_width=0, fill_color="#F2C39B", fill_opacity=1).move_to(hook() + d * 4.4))
    scene.play(FadeIn(snow), FadeIn(sled), FadeIn(rope), FadeIn(hand), run_time=1.0)
    scene.play(x.to(sled, -3.4, run_time=1.5, rate_func=linear))

    # --- 9. One pull, along the rope: part drags, part lifts -------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    k = 0.055
    F = VecArrow(hook, lambda: hook() + d * PULL_N * k, cfg.VEC_A, width=0.13)
    Fx = VecArrow(hook, lambda: hook() + RIGHT * d[0] * PULL_N * k, cfg.X_COLOR, width=0.1)
    Fy = VecArrow(lambda: hook() + RIGHT * d[0] * PULL_N * k, lambda: hook() + d * PULL_N * k, cfg.Y_COLOR, width=0.1)
    scene.add(F)
    scene.play(F.grow_in(run_time=1.0), run_time=1.0)
    pull = txt('F', cfg.FONT["label"], cfg.VEC_A).move_to([1.0, 2.6, 0])
    scene.play(FadeIn(pull), run_time=0.6)
    scene.add(Fx, Fy)
    scene.play(Fx.grow_in(run_time=0.9), x.to(sled, -3.0, run_time=0.9, rate_func=linear), run_time=0.9)
    drag = txt('Fₓ', cfg.FONT["label"], cfg.X_COLOR)
    drag.add_updater(lambda m: m.next_to(Fx.tip(), DOWN, buff=0.35).shift(LEFT * 1.0))
    scene.play(FadeIn(drag), x.to(sled, -2.8, run_time=0.6, rate_func=linear), run_time=0.6)
    scene.play(Fy.grow_in(run_time=0.9), x.to(sled, -2.4, run_time=0.9, rate_func=linear), run_time=0.9)
    lift = txt('Fᵧ', cfg.FONT["label"], cfg.Y_COLOR)
    lift.add_updater(lambda m: m.next_to(Fy.tip(), RIGHT, buff=0.3).shift(DOWN * 0.5))
    scene.play(FadeIn(lift), x.to(sled, -2.2, run_time=0.6, rate_func=linear), run_time=0.6)

    # --- 10. Same pull, two descriptions --------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    eqs = VGroup(paint(eq([r"F_x", "=", "F", rf"\cos {PULL_DEG:.0f}^\circ"], cfg.FONT["body"]), {0: cfg.X_COLOR}),
                 paint(eq([r"F_y", "=", "F", rf"\sin {PULL_DEG:.0f}^\circ"], cfg.FONT["body"]), {0: cfg.Y_COLOR}))
    eqs.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([4.6, 2.4, 0])
    scene.play(FadeOut(pull), FadeIn(eqs), x.to(sled, -0.8, run_time=6.0, rate_func=linear), run_time=6.0)

    # --- 11. One direction at a time -------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    clear(scene)
    one = result_label('x · y', cfg.GOLD, cfg.FONT["title"]).move_to(UP * 0.8)
    algebra = txt('components', cfg.FONT["body"], cfg.WHITE).next_to(one, DOWN, buff=0.4)
    scene.play(FadeIn(one, shift=UP * 0.15), run_time=1.0)
    scene.play(FadeIn(algebra), run_time=0.8)

    # --- 12. How big is each component? Trigonometry ----------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    scene.play(FadeOut(VGroup(one, algebra)), run_time=0.6)
    trig = VGroup(eq(r"\cos\theta", cfg.FONT["hero"], cfg.X_COLOR), eq(r"\sin\theta", cfg.FONT["hero"], cfg.Y_COLOR)).arrange(RIGHT, buff=1.4)
    scene.play(LaggedStart(*[FadeIn(m, scale=0.9) for m in trig], lag_ratio=0.4), run_time=1.4)
    scene.wait(4.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["11"])
