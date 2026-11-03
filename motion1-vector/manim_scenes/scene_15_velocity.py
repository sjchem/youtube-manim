"""Scene 15 — velocity. A car on a winding road: the average velocity points
along the chord from start to finish of an interval; shrinking the interval
swings the chord onto the road's tangent, the instantaneous velocity dr/dt.
Its components are dx/dt and dy/dt; its length is the speed. Then a
roundabout at a locked speed: the speed never changes, the velocity arrow
never stops turning.
"""

from manim_scenes.common import *

RING_C, RING_R = np.array([-2.4, -0.6, 0]), 2.2


class Scene15Velocity(Scene):
    def construct(self) -> None:
        play_scene(self)


def road(u: float) -> np.ndarray:
    """The winding road on screen, u in 0..1."""
    x = -6.6 + 12.0 * u
    return np.array([x, -0.9 + 1.5 * np.sin(2.4 * u * PI / 1.6) + 0.8 * u, 0.0])


def tangent(u: float, du: float = 1e-4) -> np.ndarray:
    d = road(u + du) - road(u - du)
    return d / np.linalg.norm(d)


def road_velocity(u: float) -> np.ndarray:
    """Derivative for the road's physical clock t = 10u seconds."""
    return np.array([12.0, 1.5 * (1.5 * PI) * np.cos(1.5 * PI * u) + 0.8, 0.0]) / 10.0


VELOCITY_SCALE = 1.5  # one consistent arrow scale for averages, tangents and components


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "15", "Velocity")
    avg = paint(eq([r"\vec{v}_{\text{avg}}", "=", r"\frac{\Delta\vec{r}}{\Delta t}"], cfg.FONT["title"]),
                {0: cfg.VELOCITY, 2: cfg.RESULT}).move_to([0, 2.5, 0])
    scene.play(Write(avg), run_time=1.4)

    # --- 2. A car on a winding road: the chord --------------------------------------------------------------------------
    beat(scene, t, 1)
    lane = VMobject(stroke_color=cfg.GRAY, stroke_width=40, stroke_opacity=0.32)
    lane.set_points_smoothly([road(u) for u in np.linspace(0, 1, 60)])
    centre = DashedVMobject(VMobject().set_points_smoothly([road(u) for u in np.linspace(0, 1, 60)]), num_dashes=40)
    centre.set_stroke(cfg.WHITE, 2, 0.4)
    u = Knob(0.08)
    car = Car(cfg.CYAN, 0.8)
    car.add_updater(lambda m: m.set_pose(road(u.value), np.arctan2(*tangent(u.value)[[1, 0]])))
    scene.play(avg.animate.scale(0.7).move_to([4.8, 3.3, 0]), FadeIn(lane), FadeIn(centre), FadeIn(car), run_time=1.0)
    scene.play(u.to(car, 0.62, run_time=2.4, rate_func=linear))
    u0 = 0.3
    span = Knob(0.32)
    p = lambda: road(u0)  # noqa: E731
    q = lambda: road(u0 + span.value)  # noqa: E731
    chord = VecArrow(p, q, cfg.RESULT, width=0.1)
    v_avg = VecArrow(p, lambda: p() + (q() - p()) / (span.value * 10) * VELOCITY_SCALE, cfg.VELOCITY, width=0.12)
    dots = VGroup(glow_dot(p(), cfg.WHITE, 0.08))
    q_dot = always_redraw(lambda: glow_dot(q(), cfg.WHITE, 0.08))
    scene.add(chord)
    scene.play(FadeIn(dots), FadeIn(q_dot), chord.grow_in(run_time=1.2), run_time=1.2)
    scene.add(v_avg)
    scene.play(v_avg.grow_in(run_time=1.0), run_time=1.0)
    chord_lab = eq(r"\vec{v}_{\text{avg}}", cfg.FONT["body"], cfg.VELOCITY)
    chord_lab.add_updater(lambda m: m.next_to(v_avg.tip(), UP, buff=0.15))
    scene.play(FadeIn(chord_lab), run_time=0.5)

    # --- 3. Shrink the interval --------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    dt_lab = VGroup(eq(r"\Delta t", cfg.FONT["body"], cfg.TIME), DecimalNumber(span.value * 10, num_decimal_places=2, font_size=56,
                                                                              color=cfg.TIME))
    dt_lab[1].add_updater(lambda m: m.set_value(span.value * 10))
    dt_lab[1].add_updater(lambda m: m.next_to(dt_lab[0], RIGHT, buff=0.3))
    dt_lab.move_to([-4.4, 2.4, 0])
    scene.play(FadeIn(dt_lab), run_time=0.5)
    scene.play(span.to(chord, 0.1, run_time=3.0))
    scene.play(span.to(chord, 0.03, run_time=2.0))

    # --- 4. In the limit: the tangent, dr/dt ---------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(span.to(chord, 0.003, run_time=1.6), chord.fade_to(0.0, run_time=1.6), run_time=1.6)
    inst = paint(eq([r"\vec{v}", "=", r"\frac{d\vec{r}}{dt}"], cfg.FONT["title"]), {0: cfg.VELOCITY}).move_to([1.6, 2.2, 0])
    scene.play(FadeOut(head), Write(inst), run_time=1.4)
    tangent_line = DashedLine(road(u0) - tangent(u0) * 3, road(u0) + tangent(u0) * 3, stroke_color=cfg.MUTED, stroke_width=3)
    scene.play(Create(tangent_line), run_time=1.0)

    # --- 5. Always along the path: tangent ------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    for m in (chord_lab, dt_lab[1]):
        m.clear_updaters()
    scene.play(FadeOut(VGroup(dots, q_dot, chord_lab, dt_lab, tangent_line)), v_avg.fade_to(0, run_time=0.6), run_time=0.6)
    v = VecArrow(lambda: road(u.value), lambda: road(u.value) + road_velocity(u.value) * VELOCITY_SCALE, cfg.VELOCITY, width=0.12)
    u.value = 0.05
    scene.add(v)
    scene.play(v.grow_in(run_time=0.6), run_time=0.6)
    scene.play(u.to(car, 0.95, run_time=4.6, rate_func=linear))

    # --- 6. Components: dx/dt and dy/dt ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(car), v.fade_to(0.0), run_time=0.6)
    u.value = 0.4
    scene.play(FadeIn(car), v.fade_to(1.0), run_time=0.6)
    vx = VecArrow(lambda: road(u.value), lambda: road(u.value) + np.array([road_velocity(u.value)[0], 0, 0]) * VELOCITY_SCALE,
                  cfg.X_COLOR, width=0.09)
    vy = VecArrow(lambda: road(u.value) + np.array([road_velocity(u.value)[0], 0, 0]) * VELOCITY_SCALE,
                  lambda: road(u.value) + road_velocity(u.value) * VELOCITY_SCALE, cfg.Y_COLOR, width=0.09)
    comps = VGroup(paint(eq([r"v_x", "=", r"\frac{dx}{dt}"], cfg.FONT["section"]), {0: cfg.X_COLOR}),
                   paint(eq([r"v_y", "=", r"\frac{dy}{dt}"], cfg.FONT["section"]), {0: cfg.Y_COLOR})).arrange(RIGHT, buff=0.9)
    comps.move_to([2.4, -3.0, 0])
    scene.add(vx, vy)
    scene.play(vx.grow_in(run_time=0.8), vy.grow_in(run_time=0.8), Write(comps), run_time=1.6)

    # --- 7. Its length is the speed ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    speed = paint(eq([r"v", "=", r"\sqrt{v_x^2 + v_y^2}"], cfg.FONT["section"]), {0: cfg.WHITE}).next_to(comps, UP, buff=0.4)
    speed_name = txt("speed", cfg.FONT["label"], cfg.WHITE).next_to(speed, LEFT, buff=0.4)
    scene.play(FadeIn(speed_name), Write(speed), run_time=1.4)

    # --- 8. Speed: how fast. Velocity: how fast and which way ---------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    clear(scene)
    lines = VGroup(VGroup(txt("speed", cfg.FONT["title"], cfg.WHITE), eq(r"|\vec v|", cfg.FONT["body"], cfg.MUTED)).arrange(DOWN, buff=0.25),
                   VGroup(txt("velocity", cfg.FONT["title"], cfg.VELOCITY), txt("how fast + which way", cfg.FONT["body"], cfg.MUTED)).arrange(DOWN, buff=0.25))
    lines.arrange(RIGHT, buff=1.6).move_to(UP * 0.4)
    scene.play(LaggedStart(*[FadeIn(l, shift=UP * 0.2) for l in lines], lag_ratio=0.4), run_time=1.6)

    # --- 9. A roundabout at a locked speed ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(lines), run_time=0.6)
    ring = VGroup(Circle(radius=RING_R, stroke_color=cfg.GRAY, stroke_width=46, stroke_opacity=0.32).move_to(RING_C),
                  Circle(radius=RING_R - 0.75, stroke_color=cfg.GREEN, stroke_width=0, fill_color=cfg.GREEN, fill_opacity=0.12).move_to(RING_C))
    a = Knob(-PI / 2)
    where = lambda: RING_C + RING_R * np.array([np.cos(a.value), np.sin(a.value), 0])  # noqa: E731
    along = lambda: np.array([-np.sin(a.value), np.cos(a.value), 0])  # noqa: E731
    car2 = Car(cfg.CYAN, 0.8)
    car2.add_updater(lambda m: m.set_pose(where(), a.value + PI / 2))
    v2 = VecArrow(where, lambda: where() + along() * 1.7, cfg.VELOCITY, width=0.11)
    gauge = Speedometer([4.4, 0.8, 0], value=12, radius=1.3)
    scene.add(ring, car2, v2)
    scene.play(FadeIn(ring), FadeIn(car2), v2.grow_in(run_time=0.8), FadeIn(gauge), run_time=0.8)
    locked = txt("speed locked", cfg.FONT["label"], cfg.CYAN).next_to(gauge, DOWN, buff=0.35)
    scene.play(FadeIn(locked), a.to(car2, 0.2, run_time=2.4, rate_func=linear), run_time=2.4)

    # --- 10. The arrow keeps turning ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    ghosts = VGroup()
    for k in range(6):
        ang = -PI / 2 + k * TAU / 6
        w = RING_C + RING_R * np.array([np.cos(ang), np.sin(ang), 0])
        d = np.array([-np.sin(ang), np.cos(ang), 0])
        ghosts.add(VecArrow(w, w + d * 1.7, cfg.VELOCITY, width=0.08, live=False).set_opacity(0.45))
    scene.play(FadeIn(ghosts, lag_ratio=0.2), a.to(car2, 2.4, run_time=3.0, rate_func=linear), run_time=3.0)

    # --- 11. Velocity changing at constant speed ------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    verdict = VGroup(txt("speed: constant", cfg.FONT["label"], cfg.CYAN), txt("velocity: changing", cfg.FONT["label"], cfg.VELOCITY))
    verdict.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([4.4, -2.6, 0])
    scene.play(FadeOut(locked), FadeIn(verdict), a.to(car2, 4.4, run_time=3.0, rate_func=linear), run_time=3.0)

    # --- 12. Direction matters as much as size ---------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    scene.play(a.to(car2, 8.0, run_time=5.4, rate_func=linear))

    # --- 13. How do we measure a change in velocity? ------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    clear(scene)
    ask = txt('Δv / Δt', cfg.FONT["section"], cfg.WHITE).move_to(UP * 0.6)
    dv = paint(eq([r"\Delta\vec{v}", "\\ ?"], cfg.FONT["hero"]), {0: cfg.ACCEL}).next_to(ask, DOWN, buff=0.6)
    scene.play(FadeIn(ask, shift=UP * 0.15), run_time=1.0)
    scene.play(Write(dv), run_time=1.2)
    scene.wait(4.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["15"])
