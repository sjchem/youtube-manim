"""Scene 26 — why 45 degrees, and when it fails. Only sin(2 theta) varies, and
sin peaks at 90, so theta = 45. A 3D fan of throws (15 to 75 degrees, each
on its own lane) and a live R(theta) graph show the landing point peaking at
45; 30 and 60 land together at 35.35 m (``physics_models.TABLE``). Then the
limits: a foam ball with quadratic drag (``drag_flight``) lands short and
lopsided, and a 10 m ledge moves the best angle down to 39 degrees.
"""

from manim_scenes.common import *

LOW, MID, HIGH = pm.TABLE
FAN = (15.0, 30.0, 45.0, 60.0, 75.0)
FAN_COLORS = (cfg.TEAL, cfg.CYAN, cfg.GOLD, cfg.PURPLE, cfg.ROSE)
BEST_LEDGE = pm.best_angle_from_height(P.v0, pm.LEDGE_HEIGHT)


class Scene26BestAngle(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "26", "Why forty-five degrees?")
    law = paint(eq([r"R", "=", r"\frac{v_0^2}{g}", r"\,\sin 2\theta"], cfg.FONT["title"]), {0: cfg.GREEN, 3: cfg.GOLD}).move_to([0, 2.3, 0])
    scene.play(Write(law), run_time=1.4)
    under = law.get_bottom()[1] - 0.35
    fixed = txt("fixed", cfg.FONT["small"], cfg.MUTED).move_to([law[2].get_center()[0], under, 0])
    varies = txt("varies", cfg.FONT["small"], cfg.GOLD).move_to([law[3].get_center()[0], under, 0])
    scene.play(FadeIn(fixed), FadeIn(varies), run_time=0.8)

    # --- 2. sin is at most 1: 2 theta = 90 ---------------------------------------------------------------------------------
    beat(scene, t, 1)
    axes = Axes(x_range=(0, 90, 15), y_range=(0, 1.1, 0.5), x_length=7.0, y_length=2.6, tips=False,
                axis_config={"stroke_color": cfg.MUTED, "stroke_width": 3}).move_to([0, -1.4, 0])
    sine = axes.plot(lambda d: np.sin(np.radians(2 * d)), x_range=(0, 90), color=cfg.GOLD, stroke_width=6)
    marks = VGroup(*[txt(f"{d}°", cfg.FONT["tiny"], cfg.MUTED).next_to(axes.c2p(d, 0), DOWN, buff=0.15) for d in (0, 45, 90)])
    ylab = eq(r"\sin 2\theta", cfg.FONT["small"], cfg.GOLD).next_to(axes.y_axis.get_top(), LEFT, buff=0.2)
    scene.play(FadeOut(VGroup(fixed, varies)), Create(axes), FadeIn(marks), FadeIn(ylab), run_time=1.0)
    scene.play(Create(sine), run_time=1.6)
    peak = glow_dot(axes.c2p(45, 1), cfg.GOLD, 0.1, reach=4)
    one = eq(r"\sin 2\theta = 1 \Rightarrow 2\theta = 90^\circ", cfg.FONT["body"], cfg.WHITE).next_to(axes, UP, buff=0.3)
    scene.play(FadeIn(peak, scale=1.4), FadeIn(one), run_time=1.0)

    # --- 3. theta = 45 degrees -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    best = boxed(eq(r"\theta = 45^\circ", cfg.FONT["title"], cfg.GOLD), cfg.GOLD).move_to([0, 2.3, 0])
    scene.play(fade_through(VGroup(law, one), best), run_time=1.0)
    caveat = txt('y𝒻 = y₀ · aₓ = 0 · aᵧ = −g', cfg.FONT["small"], cfg.MUTED).next_to(best, DOWN, buff=0.3)
    scene.play(FadeIn(caveat), run_time=0.7)

    # --- 4. Sweep every angle: a 3D fan --------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    clear(scene)
    stage = field_stage((-2.6, -2.3, 0), zoom=1.05, yaw=-0.55, pitch=0.42, x_range=(-5.0, 5.0), z_range=(-2.6, 2.6), sway=0.03)
    flights = []
    for k, (deg, color) in enumerate(zip(FAN, FAN_COLORS)):
        z = 2.0 - k * 1.0
        flight = Flight(stage, pm.Projectile(P.v0, deg), origin=(-4.4, 0, z), trail_color=color, color=color, radius=0.13)
        apex = flight.world(flight.model.apex_time)
        lane_tag = Tag(txt(f"{deg:.0f}°", cfg.FONT["small"], color), apex, UP * 0.35)
        stage.add_overlay(lane_tag)
        flights.append(flight)
    graph = Axes(x_range=(0, 90, 15), y_range=(0, 45, 10), x_length=4.4, y_length=2.8, tips=False,
                 axis_config={"stroke_color": cfg.MUTED, "stroke_width": 2.5}).move_to([4.8, 0.0, 0])
    g_labels = VGroup(eq(r"R", cfg.FONT["small"], cfg.GREEN).next_to(graph.y_axis.get_top(), LEFT, buff=0.15),
                      eq(r"\theta", cfg.FONT["small"], cfg.GOLD).next_to(graph.x_axis.get_end(), RIGHT, buff=0.15))
    r_curve = graph.plot(lambda d: pm.range_formula(P.v0, d), x_range=(0, 90), color=cfg.GREEN, stroke_width=5)
    show(scene, stage, 0.8, FadeIn(graph), FadeIn(g_labels))
    scene.play(fly_together(flights, run_time=2.3), Create(r_curve), run_time=2.3)

    # --- 5. Same range, different landing times: 35.35 m
    beat(scene, t, 4)
    dots = VGroup(*[glow_dot(graph.c2p(d, pm.range_formula(P.v0, d)), c, 0.08) for d, c in zip(FAN, FAN_COLORS)])
    scene.play(FadeIn(dots), *[stage.fade(f.trail, 0.25) for i, f in enumerate(flights) if i not in (1, 3)],
               *[stage.fade(f.ball, 0.25) for i, f in enumerate(flights) if i not in (1, 3)], run_time=1.0)
    twin = DashedLine(graph.c2p(30, LOW.range), graph.c2p(60, HIGH.range), stroke_color=cfg.WHITE, stroke_width=3)
    same = eq([r"R_{30^\circ} = R_{60^\circ}", r"\approx", rf"{md.fixed(LOW.range, 2)}\ \mathrm{{m}}"], cfg.FONT["body"])
    paint(same, {0: cfg.WHITE, 2: cfg.GREEN})
    fit_width(same, 5.8)
    same.next_to(graph, UP, buff=0.45)
    scene.play(Create(twin), Write(same), run_time=1.6)
    finish = Disc(np.array([-4.4 + LOW.range * flights[0].s, 0.02, 0.0]), 0.3, cfg.GREEN, opacity=0.0, stroke=cfg.GREEN)
    stage.add_body(finish)
    scene.play(Indicate(dots[1], color=cfg.CYAN, scale_factor=1.6), Indicate(dots[3], color=cfg.PURPLE, scale_factor=1.6), run_time=1.2)

    # --- 6. sin 60 = sin 120: complementary angles ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    comp = eq(r"\sin 60^\circ = \sin 120^\circ", cfg.FONT["body"], cfg.GOLD).next_to(same, UP, buff=0.35)
    scene.play(Write(comp), run_time=1.4)
    compl = txt('R(θ) = R(90° − θ)', cfg.FONT["small"], cfg.WHITE)
    fit_width(compl, 5.8)
    compl.next_to(graph, DOWN, buff=0.5)
    scene.play(FadeIn(compl), run_time=0.7)

    # --- 7. The table ---------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    hide(scene, stage, 0.7, FadeOut(VGroup(graph, g_labels, r_curve, dots, twin, same, comp, compl)))
    rows = [("angle", "max height", "flight time", "range")]
    for q in pm.TABLE:
        rows.append((f"{q.angle:.0f}°", f"{md.fixed(q.max_height, 2)} m", f"{md.fixed(q.flight_time, 2)} s", f"{md.fixed(q.range, 2)} m"))
    table = VGroup()
    colors = (cfg.CYAN, cfg.GOLD, cfg.PURPLE)
    for r, row in enumerate(rows):
        line = VGroup(*[txt(cell, cfg.FONT["body"] if r else cfg.FONT["small"], (cfg.MUTED if r == 0 else
                                                                                 (colors[r - 1] if c == 0 else cfg.WHITE)))
                        for c, cell in enumerate(row)])
        for c, cell in enumerate(line):
            cell.move_to([-4.8 + c * 3.2, 1.6 - r * 1.0, 0])
        table.add(line)
    rule = Line([-6.4, 1.15, 0], [6.4, 1.15, 0], stroke_color=cfg.MUTED, stroke_width=2)
    scene.play(FadeIn(table[0]), Create(rule), run_time=0.8)
    for line in table[1:]:
        scene.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in line], lag_ratio=0.15), run_time=1.4)
    ring = VGroup(*[SurroundingRectangle(table[r][3], color=cfg.GREEN, buff=0.12, corner_radius=0.12) for r in (1, 3)])
    scene.play(Create(ring), run_time=1.0)

    # --- 8. Different heights, different times, same range ----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    diff = txt('H₃₀ ≠ H₆₀ · T₃₀ ≠ T₆₀ · R₃₀ = R₆₀', cfg.FONT["label"], cfg.GREEN).move_to(DOWN * 2.6)
    scene.play(FadeIn(diff, shift=UP * 0.15), run_time=0.8)

    # --- 9. Not a universal rule ----------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    clear(scene)
    rule_card = txt('45° ?', cfg.FONT["title"], cfg.RED)
    scene.play(FadeIn(rule_card, scale=0.95), run_time=1.0)

    # --- 10. Air resistance: lopsided, short, best angle below 45 ---------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(rule_card.animate.scale(0.6).move_to(UP * 3.4), run_time=0.7)
    left = plane((0, 45), (0, 12), unit=0.16, at=(-7.3, -2.2, 0), step=5, labels=False, faint=0.25)
    ideal = VMobject(stroke_color=cfg.GOLD, stroke_width=5).set_points_smoothly([left.c2p(x, y) for _, x, y in P.samples(60)])
    drag_samples = pm.drag_flight(P.v0, 45.0)
    drag_rows = np.vstack([drag_samples[::40], drag_samples[-1]])
    dragged = VMobject(stroke_color=cfg.RED, stroke_width=6).set_points_smoothly([left.c2p(x, y) for _, x, y in drag_rows])
    tags = VGroup(txt("no air", cfg.FONT["small"], cfg.GOLD).next_to(left.c2p(36, 6), UR, buff=0.05),
                  txt("with air", cfg.FONT["small"], cfg.RED).next_to(left.c2p(18, 1), DOWN, buff=0.1))
    scene.play(FadeIn(left), Create(ideal), run_time=1.0)
    scene.play(Create(dragged), FadeIn(tags), run_time=2.0)
    best_drag = txt(f"best angle ≈ {pm.best_angle_with_drag(P.v0):.0f}°", cfg.FONT["label"], cfg.RED).next_to(left, UP, buff=0.3)
    scene.play(FadeIn(best_drag), run_time=0.7)

    # --- 11. From a 10 m ledge: about 39 degrees -------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    right = plane((0, 50), (0, 22), unit=0.13, at=(0.9, -2.6, 0), step=5, labels=False, faint=0.25)
    ledge = Rectangle(width=0.5, height=pm.LEDGE_HEIGHT * right.unit, stroke_color=cfg.MUTED, stroke_width=2, fill_color="#2A4D6B",
                      fill_opacity=1).move_to(right.c2p(0, pm.LEDGE_HEIGHT / 2)).align_to(right.c2p(0, 0), RIGHT)
    curves = VGroup()
    for deg, color in ((45.0, cfg.GOLD), (BEST_LEDGE, cfg.GREEN)):
        q = pm.Projectile(P.v0, deg, y0=pm.LEDGE_HEIGHT)
        curves.add(VMobject(stroke_color=color, stroke_width=5).set_points_smoothly([right.c2p(x, y) for _, x, y in q.samples(60)]))
    scene.play(FadeIn(right), FadeIn(ledge), Create(curves[0]), run_time=1.2)
    scene.play(Create(curves[1]), run_time=1.4)
    ledge_lab = VGroup(txt(f"{pm.LEDGE_HEIGHT:.0f} m ledge", cfg.FONT["small"], cfg.MUTED),
                       txt(f"best ≈ {BEST_LEDGE:.0f}°", cfg.FONT["label"], cfg.GREEN)).arrange(DOWN, buff=0.15).next_to(right, UP, buff=0.3)
    scene.play(FadeIn(ledge_lab), run_time=0.7)
    farther = eq(rf"{md.fixed(pm.ledge_range(P.v0, BEST_LEDGE), 1)}\ \mathrm{{m}} > {md.fixed(pm.ledge_range(P.v0, 45.0), 1)}\ \mathrm{{m}}",
                 cfg.FONT["small"], cfg.GREEN).next_to(right.c2p(48, 0), UP, buff=0.4).shift(LEFT * 1.2)
    scene.play(FadeIn(farther), run_time=0.7)

    # --- 12. The equations tell us when they apply ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    clear(scene)
    lesson = VGroup(txt('Prediction', cfg.FONT["section"], cfg.WHITE),
                    txt('Model assumptions', cfg.FONT["section"], cfg.GOLD)).arrange(DOWN, buff=0.3)
    scene.play(FadeIn(lesson[0], shift=UP * 0.15), run_time=0.9)
    scene.play(FadeIn(lesson[1], shift=UP * 0.15), run_time=0.9)
    scene.wait(2.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["26"])
