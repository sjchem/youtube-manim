"""Scene 22 — same cause, different outcome. Two identical samples heated
from 300 K to 450 K side by side: a free, weighted piston (Charles) and a
rigid lid (Gay-Lussac). The same microscopic change (molecules speed up)
gives a larger volume at 1.00 bar on the left and 1.50 bar in the same
volume on the right, both read from the model. A car tyre after a long drive
is the rough everyday case (not perfectly rigid; no numbers claimed).
"""

from manim_scenes.common import *


class Scene22SideBySide(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "22", "Same cause, different outcome")
    kw = dict(count=90, seed=cfg.SEED + 22, half_x=1.15, half_z=0.9, height=1.8, floor=-0.9, heater=True, zoom=0.95,
              yaw=-0.5, pitch=0.3, speed=1.5, spark_axes=(1,), spark_sides=(1,))
    free = GasBox((-4.5, -0.8, 0), lid="weight", **kw)
    rigid = GasBox((1.4, -0.8, 0), lid="rigid", **kw)
    gauges = VGroup(Gauge(free.pressure, [-1.7, 1.55, 0], top=2.0, radius=0.8, step=0.25),
                    Gauge(rigid.pressure, [4.3, 1.55, 0], top=2.0, radius=0.8, step=0.25))
    volumes = VGroup(readout("V", lambda: 2.0 * free.chamber.volume_ratio(), 2, "L", cfg.VOLUME, size=38).move_to([-4.6, 3.2, 0]),
                     readout("V", lambda: 2.0 * rigid.chamber.volume_ratio(), 2, "L", cfg.VOLUME, size=38).move_to([1.3, 3.2, 0]))
    names = VGroup(txt("free piston", cfg.FONT["small"], cfg.MUTED).move_to([-4.6, 2.45, 0]),
                   txt("rigid walls", cfg.FONT["small"], cfg.MUTED).move_to([1.3, 2.45, 0]))
    show(scene, free.stage, 0.8, FadeIn(names[0]))
    show(scene, rigid.stage, 0.8, FadeIn(names[1]))
    scene.play(FadeIn(gauges), FadeIn(volumes), run_time=1.0)

    # --- 2. The same heating: molecules speed up in both ----------------------------------------------------------------------
    beat(scene, t, 1)
    same = txt("same change: faster molecules", cfg.FONT["label"], cfg.TEMPERATURE).move_to([-1.6, -2.8, 0])
    scene.play(*free.heater_on(1.0), *rigid.heater_on(1.0), run_time=1.0)
    scene.play(free.heat_to(360, run_time=3.0), rigid.heat_to(360, run_time=3.0), free.cloud.tween("warmth", 0.25, run_time=3.0),
               rigid.cloud.tween("warmth", 0.25, run_time=3.0), free.volume_to(1.2, run_time=3.0), FadeIn(same), run_time=3.0)

    # --- 3. Free piston: expands, same P. Rigid: same V, P rises ---------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(free.heat_to(450, run_time=4.0), rigid.heat_to(450, run_time=4.0), free.cloud.tween("warmth", 0.45, run_time=4.0),
               rigid.cloud.tween("warmth", 0.45, run_time=4.0), free.volume_to(1.5, run_time=4.0), run_time=4.0)
    outcome = VGroup(txt("V grows, P same", cfg.FONT["label"], cfg.VOLUME).move_to([-4.6, -2.8, 0]),
                     txt("V same, P rises", cfg.FONT["label"], cfg.PRESSURE).move_to([1.3, -2.8, 0]))
    scene.play(FadeOut(same), run_time=0.4)
    scene.play(FadeIn(outcome), run_time=0.6)
    scene.play(Indicate(gauges[1].readout, color=cfg.PRESSURE), Indicate(volumes[0], color=cfg.VOLUME), run_time=1.4)

    # --- 4. One microscopic change, two outcomes -------------------------------------------------------------------------------
    beat(scene, t, 3)
    held = result_label("only what is held constant differs", cfg.GOLD, cfg.FONT["body"])
    fit_width(held, 11.0)
    held.move_to([-1.6, -3.0, 0])
    plate = VGroup()
    scene.play(FadeOut(VGroup(outcome, names)), run_time=0.6)
    scene.play(FadeIn(held, scale=0.95), run_time=1.0)
    scene.wait(1.5)

    # --- 5. Car tyres, roughly -------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    hide(scene, free.stage, 0.6)
    hide(scene, rigid.stage, 0.6, FadeOut(VGroup(gauges, volumes, held)))
    tyre = VGroup(Annulus(inner_radius=1.05, outer_radius=1.7, stroke_width=0, fill_color="#26323C", fill_opacity=1),
                  VGroup(*[Line(UP * 1.12, UP * 1.62, stroke_color="#50606D", stroke_width=5).rotate(k * TAU / 30, about_point=ORIGIN)
                           for k in range(30)]),
                  Circle(radius=1.05, stroke_color=cfg.STEEL, stroke_width=5, fill_color="#3B4A56", fill_opacity=1),
                  Circle(radius=0.3, stroke_width=0, fill_color=cfg.STEEL, fill_opacity=1)).move_to([-4.0, -0.3, 0])
    warmth = Annulus(inner_radius=1.05, outer_radius=1.75, stroke_width=0, fill_color=cfg.HOT_COLOR, fill_opacity=0.0).move_to(tyre)
    reading = Knob(1.0)
    tyre_gauge = Gauge(lambda: reading.value, [0.2, -0.1, 0], top=2.0, radius=1.0, step=0.25, unit="")
    tyre_gauge.remove(tyre_gauge.readout, tyre_gauge.unit)   # a needle only: the narration claims no number here
    scene.play(FadeIn(tyre), FadeIn(warmth), FadeIn(tyre_gauge), run_time=1.0)
    drive = txt("after a long drive", cfg.FONT["label"], cfg.WHITE).move_to([4.6, 2.4, 0])
    scene.play(FadeIn(drive), Rotate(tyre, -TAU, run_time=3.0), warmth.animate.set_fill(opacity=0.45),
               reading.to(tyre_gauge, 1.08, run_time=3.0), run_time=3.0)
    rough = VGroup(txt("warmer air: higher reading", cfg.FONT["small"], cfg.TEMPERATURE),
                   txt("not perfectly rigid: an estimate", cfg.FONT["small"], cfg.MUTED)).arrange(DOWN, buff=0.25).move_to([4.6, 1.2, 0])
    fit_width(rough, 5.6)
    scene.play(FadeIn(rough), run_time=1.0)
    scene.play(Rotate(tyre, -TAU, run_time=4.0), run_time=4.0)

    # --- 6. Constant P: V ~ T. Constant V: P ~ T ---------------------------------------------------------------------------------------
    beat(scene, t, 5)
    laws = VGroup(eq(r"P \text{ constant}:\ V \propto T", cfg.FONT["body"], cfg.VOLUME),
                  eq(r"V \text{ constant}:\ P \propto T", cfg.FONT["body"], cfg.PRESSURE)).arrange(DOWN, buff=0.4).move_to([2.6, -2.5, 0])
    scene.play(FadeIn(laws[0], shift=UP * 0.1), run_time=1.0)
    scene.play(FadeIn(laws[1], shift=UP * 0.1), run_time=1.0)
    finish(scene, t, fill=lambda s: [Rotate(tyre, -TAU * s / 4)])
