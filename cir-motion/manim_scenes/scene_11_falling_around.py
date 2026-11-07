"""Scene 11 — why doesn't it fall inward? Newton's construction: coast in a
straight line, then a brief nudge toward the centre, again and again. The
vertices and nudge sizes come from ``physics_models.newton_polygon`` (8, 16
and 64 sides): every vertex stays on the circle, so the vertices keep
the same radius; each intervening chord lies inside the circle, and in the limit the
polygon is the circle. Then a = -omega^2 r = -(v^2 / r) r-hat, with the
outward unit vector, and ghost copies showing that the acceleration vector
itself turns: constant magnitude, changing direction.
"""

from manim_scenes.common import *

C = np.array([-3.3, -0.5, 0])
R = 2.6
SCALE = R / P.r                         # screen units per metre
KV = 1.0 / P.v
START = -np.pi / 2 - np.pi / 8           # first chord horizontal along the bottom, moving right


class Scene11FallingAround(Scene):
    def construct(self) -> None:
        play_scene(self)


def polygon(sides: int):
    model = pm.Circular(P.m, P.r, P.v, theta0=START)
    verts, kick = pm.newton_polygon(model, sides)
    screen = np.array([C + np.array([x, y, 0]) * SCALE for x, y in verts])
    return screen, kick, 2 * P.r * np.sin(np.pi / sides) / (P.period / sides)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "11", "Why doesn't it fall inward?")
    view = CircleView(C, R, P, kv=KV, ka=1.5 / P.accel, phase=START + np.pi / 8)
    a_arrow = view.arrow("a", width=0.09)
    scene.play(FadeIn(view.ring), FadeIn(view.hub), FadeIn(view.ball), run_time=0.7)
    scene.add(a_arrow)
    scene.play(a_arrow.grow_in(run_time=0.8), run_time=0.8)
    fall = dashed_path(view.point(), C, cfg.WARNING, width=4, opacity=0.9)
    ask = txt("?", cfg.FONT["title"], cfg.WARNING).next_to(fall.get_center(), RIGHT, buff=0.3)
    scene.play(Create(fall), FadeIn(ask), run_time=1.0)

    # --- 2. Velocity: where it's going. Acceleration: how v changes ------------------------------------------------------
    beat(scene, t, 1)
    v_arrow = view.arrow("v", width=0.09)
    scene.add(v_arrow)
    scene.play(FadeOut(VGroup(fall, ask, head)), v_arrow.grow_in(run_time=0.8), run_time=0.8)
    roles = VGroup(VGroup(eq(r"\vec v", cfg.FONT["body"], cfg.VELOCITY), txt("where it's going", cfg.FONT["small"], cfg.WHITE)).arrange(RIGHT, buff=0.3),
                   VGroup(eq(r"\vec a", cfg.FONT["body"], cfg.ACCEL), txt("how v changes", cfg.FONT["small"], cfg.WHITE)).arrange(RIGHT, buff=0.3))
    roles.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.7, 2.4, 0])
    scene.play(FadeIn(roles[0], shift=LEFT * 0.1), run_time=0.7)
    scene.play(FadeIn(roles[1], shift=LEFT * 0.1), run_time=0.7)

    # --- 3. Coast in a straight line -------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    verts, kick, chord_speed = polygon(8)
    s = Knob(0.0)

    def where() -> np.ndarray:
        k = int(min(np.floor(s.value), len(verts) - 2))
        f = s.value - k
        return verts[k] + (verts[k + 1] - verts[k]) * f

    def heading_vec() -> np.ndarray:
        k = int(min(np.floor(s.value + 1e-9), len(verts) - 2))
        return mu.unit(verts[k + 1] - verts[k])

    scene.play(FadeOut(VGroup(a_arrow, v_arrow, view.ball)), run_time=0.5)
    puck = bead(verts[0], cfg.BALL, 0.16)
    puck.add_updater(lambda m: m.move_to(where()))
    v_poly = VecArrow(where, lambda: where() + heading_vec() * chord_speed * KV * 1.3, cfg.VELOCITY, width=0.09)
    path = VMobject(stroke_color=cfg.WHITE, stroke_width=4, fill_opacity=0)
    path.add_updater(lambda m: m.set_points_as_corners([*verts[:int(np.floor(s.value)) + 1], where()]))
    scene.add(path, puck, v_poly)
    scene.play(FadeIn(puck), v_poly.grow_in(run_time=0.6), run_time=0.6)
    coast = txt("coast", cfg.FONT["label"], cfg.VELOCITY).move_to([3.7, 0.6, 0])
    scene.play(FadeIn(coast), run_time=0.5)
    scene.play(s.to(puck, 1.0 - 1e-6, run_time=2.6, rate_func=linear), run_time=2.6)

    # --- 4. A nudge toward the centre; coast again ----------------------------------------------------------------------------------------
    beat(scene, t, 3)
    nudge_size = kick * KV * 1.3
    first = VecArrow(verts[1], verts[1] + mu.unit(C - verts[1]) * nudge_size, cfg.DELTA_V, width=0.09)
    nudge = txt("nudge", cfg.FONT["label"], cfg.DELTA_V).next_to(coast, DOWN, buff=0.3)
    scene.add(first)
    scene.play(first.grow_in(run_time=0.7), FadeIn(nudge), run_time=0.7)
    scene.play(s.to(puck, 1.0 + 1e-6, run_time=0.4), run_time=0.4)
    scene.play(s.to(puck, 2.0 - 1e-6, run_time=2.4, rate_func=linear), run_time=2.4)

    # --- 5. Coast, nudge, coast, nudge: a polygon whose corners stay at radius r ------------------------------------------------------------------------------
    beat(scene, t, 4)
    nudges = [first]
    for k in range(2, len(verts) - 1):
        arrow = VecArrow(verts[k], verts[k] + mu.unit(C - verts[k]) * nudge_size, cfg.DELTA_V, width=0.08)
        scene.add(arrow)
        nudges.append(arrow)
        scene.play(arrow.grow_in(run_time=0.3), s.to(puck, float(k) + 1e-6, run_time=0.3), run_time=0.3)
        scene.play(s.to(puck, k + 1.0 - 1e-6, run_time=0.75, rate_func=linear), run_time=0.75)
    spokes = VGroup(*[dashed_path(C, v, cfg.POSITION, width=2.5, opacity=0.6) for v in verts[:-1]])
    scene.play(Create(spokes), run_time=0.8)
    same_r = txt("every corner: distance r", cfg.FONT["small"], cfg.POSITION).move_to([3.7, -0.9, 0])
    scene.play(FadeIn(same_r), run_time=0.6)

    # --- 6. Smaller, more frequent nudges: the circle -------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    for m in (puck, path, v_poly):
        m.clear_updaters()
    scene.play(FadeOut(VGroup(puck, v_poly, spokes, *nudges, coast, nudge, same_r)), run_time=0.6)
    count = VGroup(txt("nudges per lap:", cfg.FONT["small"], cfg.MUTED), Integer(8, font_size=50, color=cfg.DELTA_V))
    count.arrange(RIGHT, buff=0.25).move_to([3.7, 0.6, 0])
    scene.play(FadeIn(count), run_time=0.5)
    for sides in (16, 64):
        pts, kick_n, _ = polygon(sides)
        shape = VMobject(stroke_color=cfg.WHITE, stroke_width=4, fill_opacity=0).set_points_as_corners(list(pts))
        marks = VGroup(*[VecArrow(p, p + mu.unit(C - p) * kick_n * KV * 1.3 * 2.2, cfg.DELTA_V, width=0.05, tip_len=0.14, glow=False, live=False)
                         for p in pts[:-1]])
        number = Integer(sides, font_size=50, color=cfg.DELTA_V).move_to(count[1], aligned_edge=LEFT)
        scene.play(FadeOut(path), Create(shape), FadeIn(marks), fade_through(count[1], number), run_time=1.6)
        count.remove(count[1])
        count.add(number)
        scene.wait(1.4)
        scene.play(FadeOut(marks), run_time=0.5)
        path = shape
    pull = VGroup(txt("inward pull", cfg.FONT["label"], cfg.DELTA_V), txt("bends the path", cfg.FONT["label"], cfg.WHITE))
    pull.arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(count, DOWN, buff=0.5)
    scene.play(FadeIn(pull, shift=UP * 0.1), Indicate(view.ring, color=cfg.WHITE, scale_factor=1.0), run_time=1.0)

    # --- 7. a = -omega^2 r = -(v^2 / r) r-hat -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(VGroup(path, count, pull, roles)), run_time=0.6)
    vector_form = eq([r"\vec a", "=", r"-\omega^2\,\vec r", "=", r"-\frac{v^2}{r}\,\hat r"], cfg.FONT["section"])
    paint(vector_form, {0: cfg.ACCEL, 2: cfg.POSITION, 4: cfg.POSITION})
    fit_width(vector_form, 7.0)
    vector_form.move_to([3.7, 2.6, 0])
    scene.play(Write(vector_form), run_time=1.8)
    view.clock.value = 0.6
    a_live, r_live = view.arrow("a", width=0.09), view.arrow("r", width=0.07)
    scene.add(r_live, a_live, view.ball)
    scene.play(FadeIn(view.ball), r_live.grow_in(run_time=0.8), a_live.grow_in(run_time=0.8), run_time=0.8)

    # --- 8. The minus sign: opposite to the outward r-hat ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    r_hat = VecArrow(view.point, lambda: view.point() + view.unit_r() * 0.9, cfg.POSITION, width=0.07)
    hat_tag = eq(r"\hat r", cfg.FONT["body"], cfg.POSITION).next_to(view.point() + view.unit_r() * 0.9, UR, buff=0.08)
    minus = txt("minus: inward", cfg.FONT["small"], cfg.ACCEL).next_to(vector_form, DOWN, buff=0.4)
    scene.add(r_hat)
    scene.play(r_hat.grow_in(run_time=0.7), FadeIn(hat_tag), FadeIn(minus), run_time=0.7)
    scene.wait(2.5)

    # --- 9. Constant magnitude, turning direction -------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(VGroup(r_hat, hat_tag)), run_time=0.4)
    steady = VGroup(eq(r"|\vec a| = \frac{v^2}{r}\ \text{constant}", cfg.FONT["body"], cfg.ACCEL),
                    txt("direction: always changing", cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.3)
    steady.move_to([3.7, -0.4, 0])
    scene.play(FadeIn(steady[0], shift=UP * 0.1), run_time=0.8)
    ghosts = VGroup()
    for k in range(6):
        scene.play(view.run(view.clock.value + P.period / 6, 1.4), run_time=1.4)
        ghost = view.arrow("a", when=view.clock.value, width=0.06, glow=False)
        ghost.alpha = 0.45
        ghost.refresh()
        ghosts.add(ghost)
        scene.add(ghost)
    scene.play(FadeIn(steady[1], shift=UP * 0.1), run_time=0.7)

    # --- 10. Circular motion: a change that is always sideways ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    v_live = view.arrow("v", width=0.09)
    scene.add(v_live)
    close = result_label("velocity changing sideways", cfg.GOLD, cfg.FONT["label"]).move_to([3.7, -2.6, 0])
    scene.play(FadeOut(ghosts), v_live.grow_in(run_time=0.8), FadeIn(close, shift=UP * 0.1), run_time=0.8)
    scene.play(view.run(view.clock.value + P.period * 0.85, 8.5), run_time=8.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["11"])
