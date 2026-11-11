"""Scene 04 — London dispersion. A helium atom's electron cloud, symmetric on
average, flickers lopsided: a temporary dipole (delta labels follow the
bulge). A second atom's cloud responds through the dipole field
(``common.induced_offset``): head to tail along the axis, opposite when side
by side, so the pair always attracts. The energy falls as -1/r^6 (double the
distance: 1/64). Bigger clouds distort more; the noble gases' boiling points
climb from He to Xe (CRC values, said with "about").
"""

from manim_scenes.common import *


class Scene04Dispersion(Scene):
    def construct(self) -> None:
        play_scene(self)


def flicker(clock: Knob, amplitude: float) -> Callable[[], np.ndarray]:
    """A smooth, never-repeating wander of the cloud's centre (two incommensurate tones)."""
    def offset() -> np.ndarray:
        s = clock.value
        return amplitude * np.array([np.sin(1.9 * s) * 0.8 + 0.35 * np.sin(4.7 * s + 1.0),
                                     0.55 * np.sin(2.6 * s + 0.4) + 0.2 * np.sin(5.3 * s), 0.0])
    return offset


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "04", "London dispersion forces")
    clock = Knob(0.0)
    left = Atom2D([-2.2, 0.0, 0], 1.25, label="He")
    scene.play(FadeIn(left, scale=0.9), run_time=1.0)
    avg = txt("on average: symmetric", cfg.FONT["label"], cfg.CLOUD).move_to([3.6, 2.6, 0])
    scene.play(FadeIn(avg), run_time=0.8)

    # --- 2. Electrons move: the cloud flickers -------------------------------------------------------------------
    beat(scene, t, 1)
    wander = flicker(clock, 0.28)
    left.add_updater(lambda m: setattr(m, "offset", wander()), index=0)
    instant = txt("at any instant: lopsided", cfg.FONT["label"], cfg.WHITE).move_to([3.6, 2.6, 0])
    scene.play(fade_through(avg, instant), clock.to(left, 1.5, run_time=1.2), run_time=1.2)
    scene.play(clock.to(left, 9.0, run_time=7.5, rate_func=linear))

    # --- 3. A temporary dipole ------------------------------------------------------------------------------------
    beat(scene, t, 2)
    temp = txt("temporary dipole", cfg.FONT["section"], cfg.GOLD).move_to([3.6, 2.6, 0])
    scene.play(fade_through(instant, temp), clock.to(left, 10.2, run_time=1.2, rate_func=linear), run_time=1.2)
    scene.play(clock.to(left, 15.0, run_time=4.6, rate_func=linear))

    # --- 4. A neighbour: an induced dipole, lined up to attract --------------------------------------------------------
    beat(scene, t, 3)
    right = Atom2D([2.2, 0.0, 0], 1.25, label="He")
    sep = right.centre - left.centre
    right.add_updater(lambda m: setattr(m, "offset", induced_offset(left.offset, sep, 0.75)), index=0)
    induced = txt("induced dipole", cfg.FONT["section"], cfg.PURPLE).move_to([0, 2.9, 0])
    scene.play(FadeOut(temp), clock.to(left, 16.0, run_time=1.0, rate_func=linear), run_time=1.0)
    scene.play(FadeIn(right, shift=LEFT * 0.4), clock.to(left, 17.4, run_time=1.4, rate_func=linear), run_time=1.4)
    scene.play(FadeIn(induced, shift=DOWN * 0.1), clock.to(left, 18.5, run_time=1.0, rate_func=linear), run_time=1.0)
    scene.play(clock.to(left, 28.0, run_time=9.5, rate_func=linear))

    # --- 5. It follows the flicker: London dispersion --------------------------------------------------------------------
    beat(scene, t, 4)
    pull = VGroup(VecArrow([-0.55, -1.9, 0], [-0.05, -1.9, 0], cfg.ATTRACT, width=0.09, live=False),
                  VecArrow([0.55, -1.9, 0], [0.05, -1.9, 0], cfg.ATTRACT, width=0.09, live=False))
    name = result_label("London dispersion force", cfg.ATTRACT, cfg.FONT["section"]).move_to([0, 2.9, 0])
    scene.play(fade_through(induced, name), FadeIn(pull), clock.to(left, 29.5, run_time=1.4, rate_func=linear), run_time=1.4)
    scene.play(clock.to(left, 38.0, run_time=8.5, rate_func=linear))

    # --- 6. Short ranged: -1/r^6; double r, 64 times weaker ----------------------------------------------------------------
    beat(scene, t, 5)
    axes = plot_axes((0.8, 3.2), (-1.1, 0.25), x_length=6.2, y_length=4.2, at=[3.3, -0.4, 0], x_label="r",
                     y_label="U", y_color=cfg.ATTRACT)
    zero = DashedLine(axes.c2p(0.8, 0), axes.c2p(3.2, 0), stroke_color=cfg.MUTED, stroke_width=2, dash_length=0.12)
    law = eq(r"U \propto -\frac{1}{r^6}", cfg.FONT["body"], cfg.ATTRACT).move_to([3.6, 2.85, 0])
    curve = curve_on(axes, lambda r: max(float(pm.dispersion(r)), -1.1), 0.99, 3.2, cfg.ATTRACT)
    pair = VGroup(left, right, pull)
    left.deltas = right.deltas = False      # at half size the delta labels would touch
    scene.play(FadeOut(name), *left.glide([-5.4, 1.2, 0], 0.5), *right.glide([-3.2, 1.2, 0], 0.5),
               pull.animate.scale(0.6).move_to([-4.3, 0.15, 0]), run_time=1.2)
    scene.play(Create(axes), Create(zero), FadeIn(law), run_time=1.2)
    scene.play(Create(curve), clock.to(left, 41.0, run_time=1.6, rate_func=linear), run_time=1.6)
    r1, r2 = 1.15, 2.3
    d1, d2 = Dot(axes.c2p(r1, float(pm.dispersion(r1))), color=cfg.GOLD, radius=0.1), Dot(axes.c2p(r2, float(pm.dispersion(r2))), color=cfg.GOLD, radius=0.1)
    ratio = eq(r"2r:\ \tfrac{1}{64}", cfg.FONT["body"], cfg.GOLD).move_to([-4.2, -1.8, 0])
    scene.play(FadeIn(d1, scale=1.4), run_time=0.6)
    scene.play(TransformFromCopy(d1, d2), run_time=1.0)
    scene.play(FadeIn(ratio, shift=UP * 0.1), clock.to(left, 45.0, run_time=2.0, rate_func=linear), run_time=2.0)
    scene.play(clock.to(left, 48.0, run_time=3.0, rate_func=linear))

    # --- 7. Bigger clouds distort more: polarizability -------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(VGroup(axes, zero, law, curve, d1, d2, ratio, pair)), run_time=0.8)
    small = Atom2D([-3.3, -0.2, 0], 0.7, label="small", deltas=False)
    big = Atom2D([2.6, -0.2, 0], 1.6, label="large", deltas=False)
    field = Knob(0.0)
    small.add_updater(lambda m: setattr(m, "offset", np.array([field.value * 0.12, 0, 0])), index=0)
    big.add_updater(lambda m: setattr(m, "offset", np.array([field.value * 0.55, 0, 0])), index=0)
    word = result_label("more polarizable", cfg.PURPLE, cfg.FONT["body"]).move_to([2.6, 2.6, 0])
    scene.play(FadeIn(small), FadeIn(big), run_time=0.9)
    scene.play(field.to(big, 1.0, run_time=2.0, rate_func=there_and_back_with_pause), run_time=2.0)
    scene.play(FadeIn(word, scale=0.95), field.to(big, 1.0, run_time=2.0, rate_func=there_and_back_with_pause), run_time=2.0)

    # --- 8. Noble gases: boiling points climb with cloud size ---------------------------------------------------------------------
    beat(scene, t, 7)
    names = ["He", "Ne", "Ar", "Kr", "Xe"]
    temps = [pm.NOBLE_BOILING_K[n] for n in names]
    colors = [cfg.ATOM[n] for n in names]
    chart = bar_chart(temps, names, colors, at=[1.3, -0.8, 0], width=10.0, height=2.7,
                      value_labels=[f"{fx(v, 0)} K" for v in temps], bar_width=1.1)
    clouds = VGroup(*[Atom2D(ORIGIN, 0.22 + 0.11 * k, deltas=False) for k in range(5)])
    for k, (cloud, bar) in enumerate(zip(clouds, chart.bars)):
        cloud.centre = np.array([bar.get_center()[0], 2.25, 0])
        jitter = flicker(clock, 0.05 + 0.025 * k)
        cloud.add_updater(lambda m, j=jitter: setattr(m, "offset", j()), index=0)
        cloud.refresh()
    bp = txt("boiling point", cfg.FONT["label"], cfg.MUTED).move_to([-5.2, 2.35, 0])
    scene.play(FadeOut(VGroup(small, big, word)), run_time=0.7)
    scene.play(Create(chart.base), FadeIn(chart.names), FadeIn(clouds), FadeIn(bp), run_time=1.0)
    scene.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in chart.bars], lag_ratio=0.25),
               clock.to(clouds, clock.value + 2.6, rate_func=linear), run_time=2.6)
    scene.play(LaggedStart(*[FadeIn(v, shift=DOWN * 0.1) for v in chart.tops], lag_ratio=0.25),
               clock.to(clouds, clock.value + 1.6, rate_func=linear), run_time=1.6)
    scene.play(Indicate(chart.tops[0], color=cfg.WHITE), Indicate(chart.tops[4], color=cfg.WHITE),
               clock.to(clouds, clock.value + 1.4, rate_func=linear), run_time=1.4)

    # --- 9. Between every pair, polar or not ------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    every = result_label("every pair of molecules", cfg.ATTRACT, cfg.FONT["body"]).move_to([0, 3.35, 0])
    scene.play(FadeIn(every, shift=DOWN * 0.1), clock.to(clouds, clock.value + 0.9, rate_func=linear), run_time=0.9)
    finish(scene, t, fill=lambda s: [clock.to(clouds, clock.value + s, rate_func=linear)])
