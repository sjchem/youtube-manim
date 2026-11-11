"""Scene 23 — Avogadro's law. A weighted piston holds the pressure and the
temperature is steady; a valve pumps molecules into the box (the gas model
activates them at the inlet). More molecules hit the walls more often, the
gauge rises above 1 bar and the piston climbs, lagging, until the molecules
are spread as thinly as before: twice the molecules, twice the volume, the
same 1.00 bar. V is proportional to n. Breathing in is the everyday case.
"""

from manim_scenes.common import *

N0 = 70                 # molecules at the start (one "mole" on screen)


class Scene23Avogadro(Scene):
    def construct(self) -> None:
        play_scene(self)


def lungs(at) -> VGroup:
    """Two lobes and a windpipe (2D); scale the lobes about their centres to breathe."""
    at = np.asarray(at, dtype=float)
    left = Ellipse(width=1.5, height=2.4, stroke_color=cfg.ROSE, stroke_width=3, fill_color=cfg.ROSE, fill_opacity=0.25).move_to(at + LEFT * 0.95)
    right = Ellipse(width=1.5, height=2.4, stroke_color=cfg.ROSE, stroke_width=3, fill_color=cfg.ROSE, fill_opacity=0.25).move_to(at + RIGHT * 0.95)
    pipe = VGroup(Line(at + UP * 2.2, at + UP * 0.6, stroke_color=cfg.MUTED, stroke_width=8),
                  Line(at + UP * 0.6, at + LEFT * 0.6 + UP * 0.2, stroke_color=cfg.MUTED, stroke_width=6),
                  Line(at + UP * 0.6, at + RIGHT * 0.6 + UP * 0.2, stroke_color=cfg.MUTED, stroke_width=6))
    group = VGroup(left, right, pipe)
    group.lobes = VGroup(left, right)
    return group


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "23", "Add more molecules")
    box = GasBox((-4.3, -1.15, 0), count=2 * N0, active=N0, seed=cfg.SEED + 23, half_x=1.3, half_z=1.0, height=1.9, floor=-0.95,
                 lid="weight", inlet=True, zoom=1.0, yaw=-0.5, pitch=0.3, speed=1.5, spark_axes=(1,), spark_sides=(1,))
    gauge = Gauge(box.pressure, [-0.6, 2.0, 0], top=2.0, radius=0.9, step=0.25)
    volume = readout("V", lambda: 2.0 * box.chamber.volume_ratio(), 2, "L", cfg.VOLUME, size=40).move_to([-4.3, 3.4, 0])
    amount = readout("n", lambda: box.cloud.active_count() / N0, 2, "× n₁", cfg.AMOUNT, size=40).move_to([-0.6, -0.6, 0])
    show(scene, box.stage, 1.0, FadeIn(gauge), FadeIn(volume), FadeIn(amount))

    # --- 2. T constant, P constant (weight); pump in molecules --------------------------------------------------------------
    beat(scene, t, 1)
    held = VGroup(txt("T constant", cfg.FONT["label"], cfg.TEMPERATURE), txt("external P fixed", cfg.FONT["label"], cfg.PRESSURE))
    held.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([3.8, 2.4, 0])
    pump = Tag(txt("pump in", cfg.FONT["small"], cfg.GOLD), lambda: box.pipe_in + np.array([-1.0, 1.1, 0.0]), UP * 0.2)
    pump.presence = 0.0
    box.stage.add_overlay(pump)
    scene.play(FadeIn(held, shift=LEFT * 0.2), run_time=1.0)
    scene.play(box.stage.fade(pump, 1.0), run_time=0.8)
    scene.wait(3.0)

    # --- 3. More molecules: more hits; the push beats the weight; the piston rises -------------------------------------------
    beat(scene, t, 2)
    added = {"n": 0}

    def pump_to(value: float) -> None:
        while added["n"] < int(value):
            box.cloud.activate(N0 + added["n"], inlet=(0.03, 0.55, 0.5), axis=0)
            added["n"] += 1

    feed = Param(box.stage, lambda: float(added["n"]), pump_to, float(N0), rate_func=linear)
    more = txt("added gas → expansion", cfg.FONT["label"], cfg.IMPULSE).move_to([3.8, 0.9, 0])
    scene.play(feed, box.volume_to(1.35, run_time=6.0, rate_func=rate_functions.ease_in_quad), FadeIn(more), run_time=6.0)
    scene.play(box.volume_to(1.75, run_time=3.5), run_time=3.5)

    # --- 4. It stops when they are spread as thinly as before ---------------------------------------------------------------------
    beat(scene, t, 3)
    thin = txt("expansion restores density", cfg.FONT["label"], cfg.PRESSURE).move_to([3.8, 0.9, 0])
    scene.play(fade_through(more, thin), box.volume_to(2.0, run_time=3.0), box.stage.fade(pump, 0.0), run_time=3.0)
    scene.play(Indicate(gauge.readout, color=cfg.PRESSURE), Indicate(volume, color=cfg.VOLUME), run_time=1.6)
    scene.wait(3.5)

    # --- 5. Double the molecules, double the volume: V ~ n ------------------------------------------------------------------------
    beat(scene, t, 4)
    axes = plot_axes((0, 2.4), (0, 5.0), x_length=4.6, y_length=2.8, at=[3.9, -1.85, 0], x_label="n", y_label="V",
                     x_color=cfg.AMOUNT, y_color=cfg.VOLUME, x_ticks=(1, 2), y_ticks=(2, 4))
    line = Line(axes.c2p(0, 0), axes.c2p(2.3, 4.6), stroke_color=cfg.VOLUME, stroke_width=5)
    dots = VGroup(*[glow_dot(axes.c2p(n, 2 * n), cfg.GOLD, 0.1) for n in (1, 2)])
    scene.play(FadeOut(VGroup(held, thin)), run_time=0.4)
    scene.play(Create(axes), run_time=0.6)
    scene.play(FadeIn(dots), Create(line), run_time=1.4)
    prop = eq(r"V \propto n", cfg.FONT["section"], cfg.AMOUNT).move_to([3.8, 2.4, 0])
    scene.play(FadeIn(prop, shift=DOWN * 0.1), run_time=0.9)

    # --- 6. V1/n1 = V2/n2 -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    law = boxed(paint(eq([r"\frac{V_1}{n_1}", "=", r"\frac{V_2}{n_2}"], cfg.FONT["section"]), {0: cfg.VOLUME, 2: cfg.VOLUME}), cfg.GOLD)
    law.move_to([3.8, 2.4, 0])
    scene.play(fade_through(prop, law), run_time=1.2)

    # --- 7. Twice the molecules need not mean twice the pressure -----------------------------------------------------------------------
    beat(scene, t, 6)
    compare = VGroup(eq(r"2n,\ V \Rightarrow P \times 2", cfg.FONT["body"], cfg.WARNING),
                     eq(r"2n,\ 2V \Rightarrow P \times 1", cfg.FONT["body"], cfg.ATTRACT)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    compare.move_to([4.5, 0.65, 0])
    scene.wait(0.4)
    scene.play(FadeIn(compare[0], shift=LEFT * 0.2), run_time=0.6)
    scene.play(FadeIn(compare[1], shift=LEFT * 0.2), run_time=1.0)
    scene.wait(3.0)

    # --- 8. Breathing in -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    hide(scene, box.stage, 0.8, FadeOut(VGroup(gauge, volume, amount, axes, line, dots, compare)), law.animate.move_to([4.2, 2.8, 0]))
    chest = lungs([-2.6, -0.6, 0])
    breath = txt("chest expands → air enters", cfg.FONT["label"], cfg.WHITE).move_to([2.6, -2.6, 0])
    fit_width(breath, 8.2)
    scene.play(FadeIn(chest), FadeIn(breath), run_time=1.0)
    stream = VGroup(*[Dot([-2.6, 3.2 - 0.35 * k, 0], radius=0.05, color=cfg.MOLECULE) for k in range(6)])
    scene.play(chest.lobes.animate.scale(1.18), run_time=0.8)
    scene.play(stream.animate.shift(DOWN * 2.0).set_opacity(0.2), run_time=1.7)
    finish(scene, t, fill=lambda s: [chest.lobes.animate.scale(1 / 1.18)])
