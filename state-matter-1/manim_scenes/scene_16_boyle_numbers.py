"""Scene 16 — Boyle in numbers. The worked example (4 L at 1 bar, compressed
isothermally to 2 L) runs in the 3D piston: the viewer predicts, then the
piston halves the volume and the gauge reads 2.00 bar, computed by the model.
P against 1/V is a straight line through the origin. Hyperbolas at three
temperatures (isotherms, P = nRT/V with nR fixed by the 300 K sample) move
outward as the gas warms: PV grows in step with T.
"""

from manim_scenes.common import *

B = pm.BOYLE


class Scene16BoyleNumbers(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "16", "Boyle in numbers")
    box = GasBox((-4.4, -0.75, 0), count=110, seed=cfg.SEED + 16, half_x=1.35, half_z=1.05, height=2.9, floor=-1.45,
                 lid="piston", zoom=1.0, yaw=-0.5, pitch=0.3, speed=1.6, p_ref=B.P1, spark_axes=(1,), spark_sides=(1,))
    gauge = Gauge(box.pressure, [-0.9, 1.75, 0], top=3.0, radius=0.95)
    volume = readout("V", lambda: B.V1 * box.chamber.volume_ratio(), 2, "L", cfg.VOLUME, size=40).move_to([-4.4, 3.3, 0])
    given = VGroup(eq(rf"V_1 = {fx(B.V1, 0)}\ \mathrm{{L}}", cfg.FONT["body"], cfg.VOLUME),
                   eq(rf"P_1 = {fx(B.P1, 0)}\ \mathrm{{bar}}", cfg.FONT["body"], cfg.PRESSURE),
                   eq(rf"V_2 = {fx(B.V2, 0)}\ \mathrm{{L}}", cfg.FONT["body"], cfg.VOLUME),
                   eq(r"P_2 = \ ?", cfg.FONT["body"], cfg.GOLD)).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to([3.6, 0.4, 0])
    show(scene, box.stage, 1.0, FadeIn(gauge), FadeIn(volume))
    scene.play(LaggedStart(*[FadeIn(g, shift=LEFT * 0.2) for g in given[:3]], lag_ratio=0.5), run_time=2.4)
    scene.play(FadeIn(given[3], shift=LEFT * 0.2), run_time=0.8)

    # --- 2. Pause and predict ------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    countdown(scene, [6.2, -2.6, 0], 3)

    # --- 3. P2 = P1 V1 / V2 = 2 bar ---------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    work = eq(rf"P_2 = \frac{{P_1 V_1}}{{V_2}} = \frac{{{fx(B.P1, 0)} \times {fx(B.V1, 0)}}}{{{fx(B.V2, 0)}}} = {fx(B.P2, 0)}\ \mathrm{{bar}}",
              cfg.FONT["body"], cfg.WHITE).move_to([2.8, -2.7, 0])
    fit_width(work, 8.6)
    scene.play(Write(work), run_time=2.2)
    scene.play(box.volume_to(B.V2 / B.V1, run_time=3.5), run_time=3.5)
    answer = eq(rf"P_2 = {fx(B.P2, 0)}\ \mathrm{{bar}}", cfg.FONT["body"], cfg.GOLD).move_to(given[3])
    scene.play(fade_through(given[3], answer), run_time=0.8)

    # --- 4. Half the volume, twice the pressure -----------------------------------------------------------------------------------
    beat(scene, t, 3)
    slogan = result_label("half the volume, twice the pressure", cfg.GOLD, cfg.FONT["body"]).move_to([3.7, 3.0, 0])
    fit_width(slogan, 6.4)
    scene.play(FadeIn(slogan, scale=0.95), run_time=1.0)

    # --- 5. P against 1/V: a straight line ---------------------------------------------------------------------------------------
    beat(scene, t, 4)
    k = B.P1 * B.V1
    axes = plot_axes((0, 0.85), (0, 3.2), x_length=5.4, y_length=4.2, at=[3.6, -0.2, 0], x_label=r"1/V", y_label="P",
                     x_color=cfg.VOLUME, y_color=cfg.PRESSURE, x_ticks=(0.25, 0.5, 0.75), y_ticks=(1, 2, 3))
    line = Line(axes.c2p(0, 0), axes.c2p(0.78, k * 0.78), stroke_color=cfg.PRESSURE, stroke_width=6)
    points = VGroup(*[glow_dot(axes.c2p(1 / v, k / v), cfg.GOLD, 0.09) for v in (8.0, 5.0, 4.0, 2.0, 1.4)])
    scene.play(FadeOut(VGroup(given[:3], answer, work, slogan)), run_time=0.8)
    scene.play(Create(axes), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(p, scale=1.4) for p in points], lag_ratio=0.25), run_time=1.6)
    scene.play(Create(line), run_time=1.4)
    through = txt("through the origin", cfg.FONT["small"], cfg.PRESSURE).next_to(axes.c2p(0.42, 0.55), RIGHT, buff=0.1)
    scene.play(FadeIn(through), run_time=0.8)

    # --- 6. Isotherms: warmer, the curve moves outward -------------------------------------------------------------------------------
    beat(scene, t, 5)
    iso_axes = plot_axes((0, 7.0), (0, 3.2), x_length=5.4, y_length=4.2, at=[3.6, -0.2, 0], x_label="V", y_label="P",
                         x_color=cfg.VOLUME, y_color=cfg.PRESSURE, x_ticks=(2, 4, 6), y_ticks=(1, 2, 3))
    temps = (300.0, 450.0, 600.0)
    curves = VGroup(*[curve_on(iso_axes, lambda v, T=T: k * T / pm.ROOM_T / v, k * T / pm.ROOM_T / 3.15, 7.0,
                               mu.mix(cfg.CYAN, cfg.HOT_COLOR, i / 2)) for i, T in enumerate(temps)])
    # A legend, top right: where the curves converge, labels on the curves would collide.
    tags = VGroup(*[txt(f"{T:.0f} K", cfg.FONT["tiny"], mu.mix(cfg.CYAN, cfg.HOT_COLOR, i / 2))
                    for i, T in enumerate(temps)][::-1]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([5.7, 1.3, 0])
    tags = VGroup(*tags[::-1])
    name = txt("isotherms", cfg.FONT["label"], cfg.WHITE).move_to([3.0, 2.75, 0])
    scene.play(FadeOut(VGroup(points, line, through)), fade_through(axes, iso_axes), box.volume_to(1.0, run_time=1.0), run_time=1.0)
    scene.play(Create(curves[0]), FadeIn(tags[0]), FadeIn(name), run_time=1.4)
    scene.play(box.heat_to(450, run_time=2.0), box.cloud.tween("warmth", 0.3, run_time=2.0), Create(curves[1]),
               FadeIn(tags[1]), run_time=2.0)
    scene.play(box.heat_to(600, run_time=2.0), box.cloud.tween("warmth", 0.6, run_time=2.0), Create(curves[2]),
               FadeIn(tags[2]), run_time=2.0)
    outward = VecArrow(iso_axes.c2p(1.8, 0.9), iso_axes.c2p(3.0, 2.0), cfg.TEMPERATURE, width=0.07, live=False)
    scene.play(GrowFromPoint(outward, outward.tail()), run_time=0.8)

    # --- 7. PV grows with T --------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    grows = eq(r"PV \propto T", cfg.FONT["section"], cfg.GOLD).move_to([3.0, 2.75, 0])
    scene.play(fade_through(name, grows), run_time=1.0)
    scene.play(box.heat_to(pm.ROOM_T, run_time=2.4), box.cloud.tween("warmth", 0.0, run_time=2.4), run_time=2.4)
    finish(scene, t, box.stage)
