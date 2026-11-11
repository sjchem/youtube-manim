"""Scene 14 — from motion to temperature. The kinetic pressure equation is
rewritten step by step in one place: 1/3 N m <v^2> = 2/3 N (1/2 m <v^2>)
= 2/3 N <K>; with <K> = 3/2 k_B T the fractions cancel to PV = N k_B T; and
with N = n N_A and N_A k_B = R it becomes PV = nRT. A small live box keeps
moving beside the algebra. Two boxes at the same temperature but different
numbers of molecules then show the difference between temperature (energy
per molecule) and pressure (also how many, in how much room).
"""

from manim_scenes.common import *

EQ_AT = np.array([-2.0, 1.3, 0.0])
NOTE_AT = np.array([-2.0, -1.2, 0.0])


class Scene14Temperature(Scene):
    def construct(self) -> None:
        play_scene(self)


def law(parts, colors) -> MathTex:
    return paint(eq(parts, 64), colors).move_to(EQ_AT)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "14", "From motion to temperature")
    box = GasBox((4.7, -1.2, 0), count=60, half_x=1.1, half_z=0.85, height=2.1, floor=-1.05, zoom=1.0, yaw=-0.5,
                 pitch=0.32, speed=1.3)
    therm = Thermo(box.kelvin, [4.7, 2.0, 0], height=1.7)
    step1 = law([r"PV", "=", r"\tfrac{1}{3} N", r"m\langle v^2\rangle"], {0: cfg.PRESSURE, 2: cfg.LIMIT})
    show(scene, box.stage, 0.9, FadeIn(step1), FadeIn(therm))

    # --- 2. <K> = 1/2 m <v^2>; regroup: 2/3 N (1/2 m <v^2>) ---------------------------------------------------------------
    beat(scene, t, 1)
    k_def = paint(eq([r"\langle K\rangle", "=", r"\tfrac{1}{2} m\langle v^2\rangle"], cfg.FONT["body"]), {0: cfg.GOLD}).move_to(NOTE_AT)
    step2 = law([r"PV", "=", r"\tfrac{2}{3} N", r"\Big(\tfrac{1}{2} m\langle v^2\rangle\Big)"], {0: cfg.PRESSURE, 2: cfg.LIMIT})
    scene.play(FadeIn(k_def, shift=UP * 0.15), run_time=1.2)
    scene.wait(2.5)
    scene.play(fade_through(step1, step2), run_time=1.8)
    brace = Brace(step2[3], DOWN, color=cfg.GOLD, buff=0.1)
    k_tag = eq(r"\langle K\rangle", cfg.FONT["body"], cfg.GOLD).next_to(brace, DOWN, buff=0.12)
    scene.play(FadeIn(brace), FadeIn(k_tag), k_def.animate.shift(DOWN * 0.9).set_opacity(0.5), run_time=1.2)
    scene.wait(2.5)

    # --- 3. PV = 2/3 N <K> -------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    step3 = law([r"PV", "=", r"\tfrac{2}{3} N", r"\langle K\rangle"], {0: cfg.PRESSURE, 2: cfg.LIMIT, 3: cfg.GOLD})
    scene.play(FadeOut(VGroup(brace, k_tag, k_def)), fade_through(step2, step3), run_time=1.4)

    # --- 4. <K> = 3/2 k_B T --------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    k_temp = paint(eq([r"\langle K\rangle", "=", r"\tfrac{3}{2}", r"k_B T"], cfg.FONT["body"]), {0: cfg.GOLD, 3: cfg.TEMPERATURE})
    k_temp.move_to(NOTE_AT)
    scene.play(FadeIn(k_temp, shift=UP * 0.15), run_time=1.2)
    scene.play(Indicate(step3[3], color=cfg.GOLD), Indicate(k_temp[0], color=cfg.GOLD), run_time=1.4)

    # --- 5. Substitute: 2/3 and 3/2 cancel: PV = N k_B T -------------------------------------------------------------------------------
    beat(scene, t, 4)
    step4 = law([r"PV", "=", r"\tfrac{2}{3}", r"N", r"\tfrac{3}{2}", r"k_B T"],
                {0: cfg.PRESSURE, 2: cfg.LIMIT, 4: cfg.LIMIT, 5: cfg.TEMPERATURE})
    scene.play(fade_through(step3, step4), k_temp.animate.set_opacity(0.4), run_time=1.6)
    slashes = VGroup(cancel(step4[2]), cancel(step4[4]))
    scene.play(Create(slashes), run_time=1.0)
    step5 = law([r"PV", "=", r"N", r"k_B T"], {0: cfg.PRESSURE, 3: cfg.TEMPERATURE})
    scene.play(FadeOut(slashes), FadeOut(k_temp), fade_through(step4, step5), run_time=1.6)

    # --- 6. Count in moles: N = n N_A; N_A k_B = R --------------------------------------------------------------------------------------
    beat(scene, t, 5)
    moles = VGroup(eq(r"N = n N_A", cfg.FONT["body"], cfg.AMOUNT), eq(r"N_A k_B = R", cfg.FONT["body"], cfg.WHITE))
    moles.arrange(RIGHT, buff=1.0).move_to(NOTE_AT)
    scene.play(FadeIn(moles[0], shift=UP * 0.15), run_time=1.2)
    scene.wait(1.5)
    scene.play(FadeIn(moles[1], shift=UP * 0.15), run_time=1.2)

    # --- 7. PV = nRT ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    final = paint(eq([r"PV", "=", r"n", r"R", r"T"], cfg.FONT["hero"]), {0: cfg.PRESSURE, 2: cfg.AMOUNT, 4: cfg.TEMPERATURE})
    result = boxed(final, cfg.GOLD).move_to([-1.6, 0.4, 0])
    built = txt("built from moving molecules", cfg.FONT["label"], cfg.MUTED).next_to(result, DOWN, buff=0.45)
    scene.play(FadeOut(moles), fade_through(step5, final), run_time=1.6)
    result = VGroup(result.frame, final)
    scene.play(Create(result[0]), FadeIn(built, shift=UP * 0.1), run_time=1.2)

    # --- 8. Temperature vs pressure: same T, different N -------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(result, built, therm)), box.stage.fade(box.stage, 0.0), run_time=0.9)
    scene.remove(box.stage)
    few = GasBox((-3.6, -0.5, 0), count=90, active=45, seed=cfg.SEED + 14, half_x=1.3, half_z=1.0, height=2.4, floor=-1.2,
                 zoom=1.0, yaw=-0.5, pitch=0.3, speed=1.5, p_ref=0.5)
    many = GasBox((2.0, -0.5, 0), count=90, seed=cfg.SEED + 14, half_x=1.3, half_z=1.0, height=2.4, floor=-1.2,
                  zoom=1.0, yaw=-0.5, pitch=0.3, speed=1.5, p_ref=1.0)
    gauges = VGroup(Gauge(few.pressure, [-6.5, 1.2, 0], radius=0.9, top=2.0), Gauge(many.pressure, [5.1, 1.2, 0], radius=0.9, top=2.0))
    temps = VGroup(readout("T", few.kelvin, 0, "K", cfg.TEMPERATURE, size=46).move_to([-3.6, 2.85, 0]),
                   readout("T", many.kelvin, 0, "K", cfg.TEMPERATURE, size=46).move_to([2.0, 2.85, 0]))
    show(scene, few.stage, 0.9, FadeIn(temps[0]))
    show(scene, many.stage, 0.9, FadeIn(temps[1]))
    scene.play(FadeIn(gauges), run_time=0.9)
    same = txt("same T: same energy per molecule", cfg.FONT["label"], cfg.TEMPERATURE).move_to([-0.8, -2.95, 0])
    fit_width(same, 10.0)
    scene.play(FadeIn(same, shift=UP * 0.1), run_time=0.8)
    scene.wait(2.0)

    # --- 9. Not required to derive; now watch each law -------------------------------------------------------------------------------
    beat(scene, t, 8)
    differ = txt("more molecules per volume: more pressure", cfg.FONT["label"], cfg.PRESSURE).move_to([-0.8, -2.95, 0])
    fit_width(differ, 11.0)
    scene.play(fade_through(same, differ), run_time=1.0)
    scene.wait(2.5)
    laws = VGroup(*[chip(name, color) for name, color in (("Boyle", cfg.PRESSURE), ("Charles", cfg.VOLUME),
                                                          ("Gay-Lussac", cfg.TEMPERATURE), ("Avogadro", cfg.AMOUNT))])
    laws.arrange(RIGHT, buff=0.35).move_to([0, 3.6, 0])
    scene.play(FadeOut(temps), LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in laws], lag_ratio=0.3), run_time=2.0)
    finish(scene, t, many.stage, fill=lambda s: few.stage.turn(yaw=few.stage.yaw + 0.22 * s / 4))
