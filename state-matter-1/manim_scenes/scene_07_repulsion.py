"""Scene 07 — too close: repulsion. Two atoms approach while a dot traces
their interaction energy, the Lennard-Jones curve from
``physics_models.lennard_jones``: the attraction deepens along the tail, then
the clouds overlap and a steep repulsive wall takes over. The full curve is
named (wall, well, tail) and written as 4 eps [(sigma/r)^12 - (sigma/r)^6];
the atoms settle and vibrate at the minimum, 2^(1/6) sigma, where the
well's depth eps measures how strongly neighbours hold on.
"""

from manim_scenes.common import *

SIGMA = 1.5            # screen units per sigma
ATOMS_AT = np.array([-3.7, 0.35, 0.0])


class Scene07Repulsion(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "07", "Too close: repulsion")
    r = Knob(3.0)
    left, right = Atom2D(ORIGIN, SIGMA / 2, deltas=False), Atom2D(ORIGIN, SIGMA / 2, deltas=False)

    def place(m, sign):
        m.centre = ATOMS_AT + np.array([sign * r.value * SIGMA / 2, 0, 0])

    left.add_updater(lambda m: place(m, -1), index=0)
    right.add_updater(lambda m: place(m, 1), index=0)
    left.refresh(), right.refresh()
    axes = plot_axes((0.85, 3.2), (-1.3, 2.3), x_length=6.0, y_length=5.0, at=[3.6, -0.3, 0], x_label=r"r/\sigma",
                     y_label=r"U", y_color=cfg.WHITE)
    zero = DashedLine(axes.c2p(0.85, 0), axes.c2p(3.2, 0), stroke_color=cfg.MUTED, stroke_width=2, dash_length=0.12)

    def energy(x: float) -> float:
        return float(np.clip(pm.lennard_jones(x), -1.3, 2.3))

    def traced() -> VMobject:
        xs = np.linspace(3.2, max(r.value, 0.95), 90)
        color = cfg.REPEL if r.value < 1.0 else cfg.ATTRACT
        return polyline([axes.c2p(x, energy(x)) for x in xs], color, 6)

    path = live(VMobject(), traced)
    dot = glow_dot(axes.c2p(3.0, energy(3.0)), cfg.GOLD, 0.11)
    dot.add_updater(lambda m: m.move_to(axes.c2p(max(r.value, 0.95), energy(max(r.value, 0.95)))))
    scene.play(FadeIn(left), FadeIn(right), Create(axes), Create(zero), run_time=1.4)
    scene.add(path, dot)
    question = txt("why don't they collapse?", cfg.FONT["label"], cfg.WHITE).move_to([-3.7, 2.6, 0])
    scene.play(FadeIn(question), run_time=0.8)

    # --- 2. Closer: the attraction grows ----------------------------------------------------------------------------
    beat(scene, t, 1)
    pull = VGroup(VecArrow(lambda: left.centre + DOWN * 1.3, lambda: left.centre + DOWN * 1.3 + RIGHT * 0.6, cfg.ATTRACT, width=0.08),
                  VecArrow(lambda: right.centre + DOWN * 1.3, lambda: right.centre + DOWN * 1.3 + LEFT * 0.6, cfg.ATTRACT, width=0.08))
    scene.play(FadeIn(pull), r.to(left, 1.45, run_time=4.5), run_time=4.5)

    # --- 3. Clouds overlap: fierce repulsion ----------------------------------------------------------------------------------
    beat(scene, t, 2)
    lens = Ellipse(width=0.1, height=1.2, stroke_width=0, fill_color=cfg.REPEL, fill_opacity=0.0)
    lens.add_updater(lambda m: m.become(Ellipse(width=max(0.05, (1.02 - r.value) * SIGMA * 1.4), height=SIGMA * 0.9,
                                                stroke_width=0, fill_color=cfg.REPEL,
                                                fill_opacity=float(np.clip((1.02 - r.value) * 6, 0, 0.75))).move_to(ATOMS_AT)))
    push = VGroup(VecArrow(lambda: left.centre + DOWN * 1.3 + RIGHT * 0.1, lambda: left.centre + DOWN * 1.3 + LEFT * 0.7, cfg.REPEL, width=0.09),
                  VecArrow(lambda: right.centre + DOWN * 1.3 + LEFT * 0.1, lambda: right.centre + DOWN * 1.3 + RIGHT * 0.7, cfg.REPEL, width=0.09))
    repel = txt("clouds overlap: repulsion", cfg.FONT["label"], cfg.REPEL).move_to([-3.7, 2.6, 0])
    scene.add(lens)
    scene.play(r.to(left, 1.02, run_time=2.4), run_time=2.4)
    scene.play(fade_through(question, repel), FadeOut(pull), FadeIn(push), r.to(left, 0.93, run_time=3.0), run_time=3.0)
    scene.wait(1.5)

    # --- 4. The full curve: wall, well, tail ---------------------------------------------------------------------------------------
    beat(scene, t, 3)
    full = curve_on(axes, energy, 0.955, 3.2, cfg.WHITE, width=6)
    wall = txt("wall", cfg.FONT["small"], cfg.REPEL).move_to(axes.c2p(1.25, 1.9))
    well = txt("well", cfg.FONT["small"], cfg.ATTRACT).move_to(axes.c2p(1.12, -1.75 + 0.1))
    tail = txt("tail", cfg.FONT["small"], cfg.MUTED).move_to(axes.c2p(2.7, -0.45))
    scene.play(FadeOut(push), FadeOut(repel), r.to(left, 1.6, run_time=1.4), run_time=1.4)
    path.clear_updaters()
    scene.play(FadeOut(path), Create(full), run_time=1.6)
    scene.play(LaggedStart(FadeIn(wall), FadeIn(well), FadeIn(tail), lag_ratio=0.5), run_time=2.0)

    # --- 5. Lennard-Jones: r^-12 repulsion, r^-6 attraction ----------------------------------------------------------------------
    beat(scene, t, 4)
    lj = paint(eq([r"U = 4\varepsilon\Big[", r"\Big(\frac{\sigma}{r}\Big)^{12}", "-", r"\Big(\frac{\sigma}{r}\Big)^{6}", r"\Big]"],
                  cfg.FONT["label"]), {1: cfg.REPEL, 3: cfg.ATTRACT})
    fit_width(lj, 6.0)
    lj.move_to([-3.9, 2.75, 0])
    names = VGroup(txt("repulsion", cfg.FONT["tiny"], cfg.REPEL).next_to(lj[1], DOWN, buff=0.2),
                   txt("attraction", cfg.FONT["tiny"], cfg.ATTRACT).next_to(lj[3], DOWN, buff=0.2))
    scene.play(Write(lj), run_time=1.8)
    scene.play(FadeIn(names), run_time=0.8)

    # --- 6. The balance point at the bottom of the well -------------------------------------------------------------------------
    beat(scene, t, 5)
    rmin = pm.LJ_MINIMUM
    guide = DashedLine(axes.c2p(rmin, -1.0), axes.c2p(rmin, 0.0), stroke_color=cfg.GOLD, stroke_width=2.5, dash_length=0.1)
    settle = txt("balanced: neighbours settle here", cfg.FONT["small"], cfg.GOLD).move_to([-3.7, -2.4, 0])
    scene.play(r.to(left, rmin, run_time=2.2), Create(guide), run_time=2.2)
    scene.play(FadeIn(settle), run_time=0.8)
    for _ in range(3):
        scene.play(r.to(left, rmin * 1.05, run_time=0.7), run_time=0.7)
        scene.play(r.to(left, rmin * 0.975, run_time=0.7), run_time=0.7)
    scene.play(r.to(left, rmin, run_time=0.5), run_time=0.5)

    # --- 7. The depth: how strongly they hold on -------------------------------------------------------------------------------
    beat(scene, t, 6)
    depth = VecArrow(axes.c2p(2.0, 0.0), axes.c2p(2.0, -1.0), cfg.ATTRACT, width=0.07, tip_len=0.2, live=False)
    flat = DashedLine(axes.c2p(rmin, -1.0), axes.c2p(2.1, -1.0), stroke_color=cfg.ATTRACT, stroke_width=2, dash_length=0.1)
    eps = eq(r"\varepsilon", cfg.FONT["body"], cfg.ATTRACT).next_to(depth, RIGHT, buff=0.15)
    ask = chip("so why doesn't every gas collapse?", cfg.WHITE).move_to([-3.7, -2.4, 0])
    fit_width(ask, 6.8)
    scene.play(FadeOut(VGroup(settle, tail)), Create(flat), GrowFromEdge(depth, UP), FadeIn(eps), run_time=1.4)
    scene.play(FadeIn(ask, shift=UP * 0.15), run_time=1.0)
    vibrate = lambda a: rmin * (1 + 0.035 * np.sin(TAU * 1.4 * a * 6))  # noqa: E731
    finish(scene, t, fill=lambda s: [Param(left, lambda: 0.0, lambda a: setattr(r, "value", vibrate(a * s / 6)), 1.0)])
