"""Scene 12 — a crowd of molecules. The force on one wall, computed by
``physics_models.wall_force_trace`` for 1, 5, 50 and 5000 molecules with
Maxwell-Boltzmann speeds: sputtering spikes become a ragged pattern, then an
almost flat line (fluctuations shrink like one over the square root of the
hits). In real air ~3e23 hits strike each square centimetre every second: a
3D crowd sparks on its right wall. Summing N molecules and dividing by the
wall's area L^2 gives P = N m <v_x^2> / V.
"""

from manim_scenes.common import *

A = pm.AIR
COUNTS = gd.TRACE_COUNTS
DURATION, BINS, TOP = 30.0, 150, 4.0


class Scene12Crowd(Scene):
    def construct(self) -> None:
        play_scene(self)


def trace_for(axes: Axes, count: int) -> VMobject:
    values, _ = pm.wall_force_trace(count, DURATION, BINS, pm.representative_seed(count, cfg.SEED + count))
    values = np.clip(values, 0, TOP)
    width = DURATION / BINS
    pts = []
    for k, v in enumerate(values):
        pts += [axes.c2p(k * width, v), axes.c2p((k + 1) * width, v)]
    color = cfg.IMPULSE if count < 1000 else cfg.GOLD
    return polyline(pts, color, 3.5 if count < 1000 else 5)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "12", "A crowd of molecules")
    axes = plot_axes((0, DURATION), (0, TOP), x_length=12.0, y_length=4.4, at=[0.2, -0.6, 0], x_label="t", y_label=r"F/\langle F\rangle",
                     y_color=cfg.IMPULSE)
    mean = DashedLine(axes.c2p(0, 1), axes.c2p(DURATION, 1), stroke_color=cfg.GOLD, stroke_width=2.5, dash_length=0.15)
    mean_tag = txt("mean = 1", cfg.FONT["tiny"], cfg.GOLD).next_to(axes.c2p(DURATION, 1), UP, buff=0.12).shift(LEFT * 0.7)
    clip_tag = txt(f"peaks > {TOP:g} clipped", cfg.FONT["tiny"], cfg.MUTED).move_to([3.9, 1.95, 0])
    traces = [trace_for(axes, n) for n in COUNTS]
    names = [txt(f"{n:,} molecule{'s' if n > 1 else ''}", cfg.FONT["section"], cfg.WHITE).move_to([0, 2.65, 0]) for n in COUNTS]
    scene.play(Create(axes), Create(mean), FadeIn(mean_tag), FadeIn(clip_tag), run_time=1.2)
    scene.play(FadeIn(names[0]), Create(traces[0]), run_time=2.4)

    # --- 2. Five: busier, still ragged ------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(fade_through(names[0], names[1]), Transform(traces[0], traces[1]), run_time=1.6)

    # --- 3. Fifty, then five thousand: almost smooth -------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(fade_through(names[1], names[2]), Transform(traces[0], traces[2]), run_time=1.6)
    scene.wait(1.6)
    scene.play(fade_through(names[2], names[3]), Transform(traces[0], traces[3]), run_time=1.8)

    # --- 4. Real air: ~3e23 hits per cm^2 per second; a steady push -------------------------------------------------------------------
    beat(scene, t, 3)
    box = GasBox((-2.4, -0.4, 0), count=160, half_x=1.8, half_z=1.3, height=3.3, floor=-1.65, zoom=1.15, yaw=-0.5,
                 pitch=0.3, speed=2.0, spark_axes=(0,), spark_sides=(1,), spark_size=1.2)
    rate = eq(rf"\approx {sci(A.hits_per_cm2_per_s, 0)}", cfg.FONT["section"], cfg.IMPULSE)
    unit = txt("hits per cm² per second", cfg.FONT["label"], cfg.WHITE)
    fact = VGroup(rate, unit).arrange(DOWN, buff=0.3).move_to([4.2, 1.4, 0])
    scene.play(FadeOut(VGroup(axes, mean, mean_tag, clip_tag, traces[0], names[3])), run_time=0.9)
    show(scene, box.stage, 1.2)
    scene.play(FadeIn(fact, shift=LEFT * 0.2), run_time=1.0)
    steady = result_label("a steady push", cfg.GOLD, cfg.FONT["section"]).move_to([4.2, -1.0, 0])
    scene.play(*box.stage.turn(yaw=-0.3), run_time=4.0)
    scene.play(FadeIn(steady, scale=0.95), run_time=0.9)

    # --- 5. Add all N molecules: total force N m <v_x^2> / L ------------------------------------------------------------------------
    beat(scene, t, 4)
    force = eq([r"F", "=", r"\frac{N m \langle v_x^2\rangle}{L}"], cfg.FONT["section"], cfg.WHITE)
    force[0].set_color(cfg.IMPULSE)
    force.move_to([3.9, 2.0, 0])
    scene.play(FadeOut(VGroup(fact, steady)), run_time=0.7)
    scene.play(Write(force), run_time=1.8)
    avg_note = txt("⟨ ⟩ = average over the molecules", cfg.FONT["small"], cfg.MUTED).next_to(force, DOWN, buff=0.4)
    scene.play(FadeIn(avg_note), run_time=0.8)

    # --- 6. Pressure is force per area: divide by L^2; L^3 = V -------------------------------------------------------------------------
    beat(scene, t, 5)
    per_area = eq([r"P", "=", r"\frac{F}{L^2}", "=", r"\frac{N m \langle v_x^2\rangle}{L^3}"], cfg.FONT["body"], cfg.WHITE)
    per_area[0].set_color(cfg.PRESSURE)
    per_area.move_to([3.9, -0.4, 0])
    volume = eq(r"L^3 = V", cfg.FONT["body"], cfg.VOLUME).next_to(per_area, DOWN, buff=0.45)
    scene.play(FadeOut(avg_note), run_time=0.4)
    scene.play(Write(per_area), run_time=1.4)
    scene.play(FadeIn(volume, shift=UP * 0.1), run_time=1.0)

    # --- 7. P = N m <v_x^2> / V ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    law = paint(eq([r"P", "=", r"\frac{N m \langle v_x^2\rangle}{V}"], cfg.FONT["section"], cfg.WHITE), {0: cfg.PRESSURE})
    result = boxed(law, cfg.GOLD).move_to([3.9, 0.6, 0])
    scene.play(fade_through(VGroup(force, per_area, volume), result), run_time=1.4)

    # --- 8. Pressure: a steady flow of momentum to the walls ------------------------------------------------------------------------------
    beat(scene, t, 7)
    flow = VGroup(txt("pressure =", cfg.FONT["label"], cfg.PRESSURE),
                  txt("momentum / (area × time)", cfg.FONT["label"], cfg.IMPULSE)).arrange(DOWN, buff=0.2)
    fit_width(flow, 7.0)
    flow.move_to([3.9, -1.9, 0])
    scene.play(FadeIn(flow, shift=UP * 0.1), box.cloud.tween("spark", 1.4), run_time=1.2)
    finish(scene, t, box.stage)
