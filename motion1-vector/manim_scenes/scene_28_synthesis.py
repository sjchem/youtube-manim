"""Scene 28 — the synthesis. The opening throw returns, the three tools
(vectors, components, equations) line up into the chain
Motion → Vectors → Components → Equations → Prediction, four small icons
show where the same reasoning goes next (orbits, fields, fluids,
engineering), and a ball on a circle — constant speed, turning velocity,
inward acceleration — trails the next episode: circular motion.
"""

from manim_scenes.common import *


class Scene28Synthesis(Scene):
    def construct(self) -> None:
        play_scene(self)


def icon_orbit() -> VGroup:
    sun = Circle(radius=0.22, stroke_width=0, fill_color=cfg.GOLD, fill_opacity=1)
    path = Ellipse(width=1.9, height=1.1, stroke_color=cfg.MUTED, stroke_width=2.5)
    planet = Circle(radius=0.11, stroke_width=0, fill_color=cfg.BLUE, fill_opacity=1).move_to(path.point_from_proportion(0.15))
    return VGroup(path, sun, planet)


def icon_field() -> VGroup:
    charge = Circle(radius=0.2, stroke_width=0, fill_color=cfg.RED, fill_opacity=1)
    lines = VGroup(*[VecArrow(0.3 * np.array([np.cos(a), np.sin(a), 0]), 0.95 * np.array([np.cos(a), np.sin(a), 0]), cfg.CYAN,
                              width=0.05, tip_len=0.15, live=False) for a in np.linspace(0, TAU, 8, endpoint=False)])
    return VGroup(lines, charge)


def icon_fluid() -> VGroup:
    waves = VGroup(*[FunctionGraph(lambda x, k=k: 0.18 * np.sin(3 * x + k) + 0.35 * (k - 1), x_range=(-0.95, 0.95),
                                   color=cfg.BLUE, stroke_width=4) for k in range(3)])
    return waves


def icon_truss() -> VGroup:
    pts = [np.array(p) for p in ((-0.9, -0.4, 0), (0, -0.4, 0), (0.9, -0.4, 0), (-0.45, 0.4, 0), (0.45, 0.4, 0))]
    edges = ((0, 1), (1, 2), (3, 4), (0, 3), (3, 1), (1, 4), (4, 2))
    bars = VGroup(*[Line(pts[a], pts[b], stroke_color=cfg.ORANGE, stroke_width=4) for a, b in edges])
    joints = VGroup(*[Circle(radius=0.06, stroke_width=0, fill_color=cfg.WHITE, fill_opacity=1).move_to(p) for p in pts])
    return VGroup(bars, joints)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "28")
    stage, flight = projectile_stage(wall=True, yaw=-0.5, pitch=0.36)
    flight.add_shadows(floor=True, wall_x=WALL_X)
    question = txt('r(t) = ?', cfg.FONT["section"], cfg.WHITE).move_to(UP * 3.2)
    show(scene, stage, 0.8, FadeIn(question))
    scene.play(flight.realtime(speed=0.6))

    # --- 2. The tools -----------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    hide(scene, stage, 0.7, FadeOut(question))
    tools = VGroup(VGroup(txt("vectors", cfg.FONT["section"], cfg.GOLD), txt('direction', cfg.FONT["small"], cfg.WHITE)),
                   VGroup(txt("components", cfg.FONT["section"], cfg.CYAN), txt('x · y', cfg.FONT["small"], cfg.WHITE)),
                   VGroup(txt("equations", cfg.FONT["section"], cfg.GREEN), txt('r(t)', cfg.FONT["small"], cfg.WHITE)))
    for tool in tools:
        tool.arrange(DOWN, buff=0.2)
    tools.arrange(RIGHT, buff=1.0).move_to(UP * 0.4)
    for tool in tools:
        scene.play(FadeIn(tool, shift=UP * 0.2), run_time=0.9)
        scene.wait(1.6)

    # --- 3. Motion -> vectors -> components -> equations -> prediction -------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(tools), run_time=0.5)
    words = [("Motion", cfg.WHITE), ("Vectors", cfg.GOLD), ("Components", cfg.CYAN), ("Equations", cfg.GREEN), ("Prediction", cfg.ORANGE)]
    chain = VGroup()
    for k, (word, color) in enumerate(words):
        chain.add(chip(word, color, cfg.FONT["label"]))
        if k < len(words) - 1:
            chain.add(txt("→", cfg.FONT["section"], cfg.MUTED))
    chain.arrange(RIGHT, buff=0.22)
    fit_width(chain, 14.6)
    chain.move_to(UP * 2.9)
    scene.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in chain], lag_ratio=0.18), run_time=2.4)

    # --- 4. Two simple motions, and where the idea goes next -------------------------------------------------------------------------------------
    beat(scene, t, 3)
    grid = plane((0, 45), (0, 12), unit=0.17, at=(-7.0, -1.9, 0), step=5, labels=False, faint=0.25)
    side = SideFlight(grid, k=0.06)
    shadows = always_redraw(lambda: VGroup(glow_dot(grid.c2p(float(P.x(side.clock.value)), 0), cfg.X_COLOR, 0.09),
                                           glow_dot(grid.c2p(0, float(P.y(side.clock.value))), cfg.Y_COLOR, 0.09)))
    scene.add(grid, side.trail, side.ball, shadows)
    scene.play(FadeIn(grid), side.fly(speed=0.9), run_time=P.flight_time / 0.9)
    icons = VGroup()
    for make, name in ((icon_orbit, "orbits"), (icon_field, "electric fields"), (icon_fluid, "fluids"), (icon_truss, "engineering")):
        icons.add(VGroup(make(), txt(name, cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.25))
    icons.arrange_in_grid(rows=2, cols=2, buff=(0.9, 0.5)).move_to([3.6, -0.6, 0])
    scene.play(LaggedStart(*[FadeIn(i, scale=0.9) for i in icons], lag_ratio=0.3), run_time=2.6)
    shadows.clear_updaters()

    # --- 5. Waiting: changing direction without changing speed -------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    clear(scene)
    centre = np.array([-3.0, -0.4, 0])
    ring = Circle(radius=2.2, stroke_color=cfg.MUTED, stroke_width=3, stroke_opacity=0.6).move_to(centre)
    spin = Knob(0.0)
    where = lambda: centre + 2.2 * np.array([np.cos(spin.value), np.sin(spin.value), 0])  # noqa: E731
    ball = bead(where(), cfg.BALL, 0.2, glow=0.6)
    ball.add_updater(lambda m: m.move_to(where()))
    v = VecArrow(where, lambda: where() + 1.6 * np.array([-np.sin(spin.value), np.cos(spin.value), 0]), cfg.VELOCITY, width=0.11)
    a = VecArrow(where, lambda: where() + (centre - where()) * 0.45, cfg.ACCEL, width=0.11)
    trace = TracedPath(lambda: ball.get_center(), stroke_color=cfg.GOLD, stroke_width=4, stroke_opacity=0.5, dissipating_time=1.2)
    scene.add(ring, ball, v, a, trace)
    scene.play(FadeIn(ring), FadeIn(ball), v.grow_in(run_time=0.8), a.grow_in(run_time=0.8), run_time=0.8)
    ask = VGroup(txt("same speed,", cfg.FONT["section"], cfg.WHITE), txt("changing direction", cfg.FONT["section"], cfg.VELOCITY))
    ask.arrange(DOWN, buff=0.25).move_to([3.6, 1.2, 0])
    scene.play(FadeIn(ask), spin.to(ball, 1.6 * PI, run_time=6.0, rate_func=linear), run_time=6.0)

    # --- 6. Next: circular motion ----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    nxt = VGroup(txt("NEXT EPISODE", cfg.FONT["small"], cfg.CYAN), txt("Circular Motion", cfg.FONT["title"], cfg.GOLD),
                 txt('a ≠ 0', cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.2)
    fit_width(nxt, 7.0)
    nxt.move_to([3.7, -1.6, 0])
    scene.play(FadeIn(nxt, shift=UP * 0.2), spin.to(ball, 3.2 * PI, run_time=5.0, rate_func=linear), run_time=5.0)
    scene.play(spin.to(ball, 4.0 * PI, run_time=2.4, rate_func=linear))
    end_scene(scene, t, cfg.SCENE_DURATIONS["28"])
