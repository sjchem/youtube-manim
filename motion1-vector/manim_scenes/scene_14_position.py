"""Scene 14 — position and displacement. A ball moves on a curved path over
a grid; its position vector r (teal) follows it from the origin. Two
moments give r_i, r_f and the displacement delta r (green). Then the origin
itself slides away: both position vectors change, delta r does not. Two
observers on different corners describe the location differently but agree
on the displacement.
"""

from manim_scenes.common import *

UNIT = 0.75
GRID_AT = np.array([-6.6, -2.9, 0])


class Scene14Position(Scene):
    def construct(self) -> None:
        play_scene(self)


def path(s: float) -> np.ndarray:
    """The ball's route in grid coordinates, s in 0..1."""
    return np.array([1.0 + 7.0 * s, 1.0 + 3.2 * np.sin(PI * s * 0.9) + 0.6 * s, 0.0])


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "14")
    opener = txt("Kinematics in one and two dimensions", cfg.FONT["title"], cfg.WHITE)
    fit_width(opener, 12.4)
    opener.move_to(ORIGIN)
    scene.play(FadeIn(opener, shift=LEFT * 0.3), run_time=0.9)
    scene.wait(1.0)
    scene.play(FadeOut(opener, shift=UP * 0.3), run_time=0.6)
    head = heading("Position and displacement")
    grid = plane((-1, 9), (-1, 6), unit=UNIT, at=GRID_AT, labels=False, faint=0.35)
    origin = Knob(0.0)          # 0: the first origin; 1: the moved origin
    o0, o1 = np.array([0.0, 0.0, 0.0]), np.array([-0.5, 3.6, 0.0])
    O = lambda: o0 + (o1 - o0) * origin.value  # noqa: E731
    to_screen = lambda p: grid.c2p(p[0], p[1])  # noqa: E731
    axes = always_redraw(lambda: VGroup(
        Line(to_screen(O() + LEFT * 0.6), to_screen(O() + RIGHT * 9.4), stroke_color=cfg.X_COLOR, stroke_width=3.5),
        Line(to_screen(O() + DOWN * 0.6), to_screen(O() + UP * 6.4), stroke_color=cfg.Y_COLOR, stroke_width=3.5),
        glow_dot(to_screen(O()), cfg.WHITE, 0.08)))
    scene.play(FadeIn(head, shift=DOWN * 0.15), FadeIn(grid), FadeIn(axes), run_time=1.0)
    o_lab = txt("origin", cfg.FONT["small"], cfg.WHITE)
    o_lab.add_updater(lambda m: m.next_to(to_screen(O()), DOWN, buff=0.22))
    scene.play(FadeIn(o_lab), run_time=0.6)

    # --- 2. r = x i + y j ------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    s = Knob(0.15)
    ball = bead(to_screen(path(s.value)), cfg.BALL, 0.18)
    ball.add_updater(lambda m: m.move_to(to_screen(path(s.value))))
    r = VecArrow(lambda: to_screen(O()), lambda: to_screen(path(s.value)), cfg.POSITION, width=0.11)
    scene.add(ball, r)
    scene.play(FadeIn(ball), r.grow_in(run_time=1.0), run_time=1.0)
    form = paint(eq([r"\vec{r}", "=", "x", r"\,\hat{\imath}", "+", "y", r"\,\hat{\jmath}"], cfg.FONT["title"]),
                 {0: cfg.POSITION, 2: cfg.X_COLOR, 3: cfg.X_COLOR, 5: cfg.Y_COLOR, 6: cfg.Y_COLOR}).move_to([4.6, 2.5, 0])
    scene.play(Write(form), run_time=1.4)

    # --- 3. The position vector follows the object --------------------------------------------------------------------------------
    beat(scene, t, 2)
    trail = TracedPath(lambda: ball.get_center(), stroke_color=cfg.MUTED, stroke_width=3, stroke_opacity=0.6)
    scene.add(trail)
    scene.play(s.to(ball, 0.85, run_time=3.8, rate_func=smooth))
    scene.play(s.to(ball, 0.3, run_time=1.0))
    trail.clear_updaters()

    # --- 4. delta r = r_f - r_i ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    si, sf = 0.3, 0.8
    ri = VecArrow(lambda: to_screen(O()), lambda: to_screen(path(si)), cfg.POSITION, width=0.1)
    rf = VecArrow(lambda: to_screen(O()), lambda: to_screen(path(sf)), cfg.POSITION, width=0.1)
    dr = VecArrow(to_screen(path(si)), to_screen(path(sf)), cfg.RESULT, width=0.12)
    ri.alpha = rf.alpha = 0.7
    scene.add(ri)
    scene.play(r.fade_to(0.0, run_time=0.5), run_time=0.5)
    scene.add(rf)
    scene.play(s.to(ball, sf, run_time=1.6), rf.grow_in(run_time=1.6), run_time=1.6)
    scene.add(dr)
    scene.play(dr.grow_in(run_time=1.2), run_time=1.2)
    names = VGroup(eq(r"\vec{r}_i", cfg.FONT["body"], cfg.POSITION), eq(r"\vec{r}_f", cfg.FONT["body"], cfg.POSITION),
                   eq(r"\Delta\vec{r}", cfg.FONT["body"], cfg.RESULT))
    names[0].add_updater(lambda m: m.move_to((to_screen(O()) + to_screen(path(si))) / 2 + LEFT * 0.45 + UP * 0.2))
    names[1].add_updater(lambda m: m.move_to((to_screen(O()) * 0.4 + to_screen(path(sf)) * 0.6) + DOWN * 0.45 + RIGHT * 0.2))
    names[2].move_to((to_screen(path(si)) + to_screen(path(sf))) / 2 + UP * 0.5)
    delta = paint(eq([r"\Delta\vec{r}", "=", r"\vec{r}_f", "-", r"\vec{r}_i"], cfg.FONT["section"]), {0: cfg.RESULT, 2: cfg.POSITION,
                                                                                                    4: cfg.POSITION})
    delta.next_to(form, DOWN, buff=0.55)
    scene.play(FadeIn(names), Write(delta), run_time=1.4)

    # --- 5. In components ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    comps = eq([r"(x_f - x_i)", r"\,\hat{\imath}", "+", r"(y_f - y_i)", r"\,\hat{\jmath}"], cfg.FONT["body"])
    paint(comps, {0: cfg.X_COLOR, 1: cfg.X_COLOR, 3: cfg.Y_COLOR, 4: cfg.Y_COLOR}).next_to(delta, DOWN, buff=0.4)
    scene.play(Write(comps), run_time=1.6)

    # --- 6. Move the origin ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(comps), FadeOut(form), run_time=0.4)
    scene.play(delta.animate.move_to([4.6, 2.6, 0]), run_time=0.4)
    scene.play(origin.to(axes, 1.0, run_time=3.0))

    # --- 7. Position vectors change; displacement doesn't ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    changed = txt('rᵢ · r𝒻', cfg.FONT["label"], cfg.POSITION).move_to([4.6, 1.3, 0])
    kept = txt('Δr', cfg.FONT["label"], cfg.RESULT).next_to(changed, DOWN, buff=0.35)
    scene.play(FadeIn(changed), run_time=0.7)
    scene.play(FadeIn(kept), Indicate(dr, color=cfg.RESULT, scale_factor=1.05), run_time=1.2)
    scene.play(origin.to(axes, 0.0, run_time=2.4))
    scene.play(origin.to(axes, 1.0, run_time=2.4))

    # --- 8. Positions depend on where we stand -----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    stand = txt('origin', cfg.FONT["label"], cfg.WHITE).move_to(DOWN * 3.6)
    scene.play(FadeIn(stand, shift=UP * 0.15), run_time=0.8)

    # --- 9. Two people on two corners ---------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    for m in (*names, o_lab):
        m.clear_updaters()
    scene.play(FadeOut(VGroup(changed, kept, stand, names, o_lab)), run_time=0.6)
    corners = [np.array([0.0, 0.0, 0]), np.array([8.0, 0.0, 0])]
    people = VGroup()
    sights = VGroup()
    for corner, color, label in zip(corners, (cfg.CYAN, cfg.PURPLE), ("observer 1", "observer 2")):
        person = VGroup(Circle(radius=0.16, stroke_width=0, fill_color=color, fill_opacity=1),
                        RoundedRectangle(width=0.32, height=0.42, corner_radius=0.12, stroke_width=0, fill_color=color,
                                         fill_opacity=1).shift(DOWN * 0.38)).move_to(to_screen(corner) + UP * 0.1)
        tag = txt(label, cfg.FONT["tiny"], color).next_to(person, DOWN, buff=0.15)
        people.add(VGroup(person, tag))
        for sv in (si, sf):
            sights.add(VecArrow(to_screen(corner), to_screen(path(sv)), color, width=0.07, live=False))
    scene.play(origin.to(axes, 0.0, run_time=1.0), r.fade_to(0, run_time=1.0), ri.fade_to(0, run_time=1.0),
               rf.fade_to(0, run_time=1.0), run_time=1.0)
    scene.play(FadeIn(people), run_time=0.8)
    for sight in sights:
        sight.set_opacity(0.6)
    scene.play(LaggedStart(*[FadeIn(sv) for sv in sights], lag_ratio=0.3), run_time=1.6)
    agree = txt('Δr', cfg.FONT["label"], cfg.RESULT).move_to([4.0, -3.6, 0])
    scene.play(FadeIn(agree), Indicate(dr, color=cfg.RESULT, scale_factor=1.06), run_time=1.2)

    # --- 10. But how quickly? -----------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    clear(scene)
    q = txt('Δr / Δt', cfg.FONT["title"], cfg.WHITE).move_to(UP * 1.0)
    watch = stopwatch(DOWN * 1.2, 1.0)
    scene.play(FadeIn(q, shift=UP * 0.15), FadeIn(watch), run_time=1.0)
    centre = watch.face.get_center()
    spin = Knob(0.0)
    watch.hand.add_updater(lambda m: m.put_start_and_end_on(centre, centre + 0.72 * np.array([np.sin(spin.value), np.cos(spin.value), 0])))
    scene.play(spin.to(watch, TAU, run_time=3.0, rate_func=linear))

    # --- 11. Velocity ----------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    word = result_label("velocity", cfg.VELOCITY, cfg.FONT["hero"]).move_to(UP * 1.0)
    scene.play(fade_through(q, word), spin.to(watch, 2 * TAU, run_time=3.0, rate_func=linear), run_time=3.0)
    scene.play(spin.to(watch, 3 * TAU, run_time=3.0, rate_func=linear))
    end_scene(scene, t, cfg.SCENE_DURATIONS["14"])
