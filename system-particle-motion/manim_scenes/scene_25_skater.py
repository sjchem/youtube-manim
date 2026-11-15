"""Scene 25 — the spinning skater. With no external torque, L is constant.
A stylised skater turns on 3D ice, arms out. Live readouts follow the model
(``physics_models.SKATER``: a body plus two arms as point masses): I = 4,
omega = 2, L = 8. The arms pull in to the model's radius for I = 2; the spin
visibly speeds up and the readouts land on omega = 4 with L still 8. Two
coral bars show K rising from 8 J to 16 J; green inward arrows on the hands
show the muscles' pull doing the extra 8 J of work. The closing chips: L
conserved, K not.
"""

from manim_scenes.common import *

K = pm.SKATER


class Scene25Skater(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "25", "The spinning skater")
    law = VGroup(eq(r"\vec\tau_{\text{ext}} = 0", cfg.FONT["section"], cfg.TORQUE),
                 eq(r"\Rightarrow\ {d\vec L \over dt} = 0", cfg.FONT["section"], cfg.WHITE),
                 eq(r"\Rightarrow\ \vec L = \text{constant}", cfg.FONT["section"], cfg.BALANCED)).arrange(RIGHT, buff=0.35)
    fit_width(law, 13.4)
    law.move_to(UP * 0.4)
    for part in law:
        scene.play(FadeIn(part, shift=RIGHT * 0.15), run_time=0.9)
    cons = result_label("conservation of angular momentum", cfg.BALANCED, cfg.FONT["body"]).next_to(law, DOWN, buff=0.6)
    scene.play(FadeIn(cons), run_time=0.8)

    # --- 2. I omega constant ------------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    Iw = eq([r"I", r"\,\omega", r"= \text{constant}"], cfg.FONT["title"], cfg.WHITE)
    Iw[0].set_color(cfg.INERTIA)
    Iw[1].set_color(cfg.OMEGA)
    Iw.move_to([0, 1.7, 0])
    scene.play(FadeOut(cons), law.animate.scale(0.6).move_to([0, 3.4, 0]), run_time=0.8)
    scene.play(Write(Iw), run_time=1.2)
    seesaw = caption("smaller I, bigger omega", cfg.OMEGA)
    scene.play(FadeIn(seesaw), run_time=0.6)

    # --- 3. The skater, arms out ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(VGroup(law, Iw, seesaw)), run_time=0.6)
    stage = Stage((-2.7, -3.3, 0.0), zoom=1.65, yaw=-0.2, pitch=0.22, sway=0.02)
    ice = Grid((0, 0, 0), (1, 0, 0), (0, 0, 1), (-4.0, 4.0), (-3.0, 3.0), step=0.5, major=4, color=cfg.ICE, opacity=0.2,
               fill=cfg.ICE, fill_opacity=0.07)
    stage.add_body(ice)
    angle, reach = Knob(0.0), Knob(K.r_out)

    def omega() -> float:
        return K.omega_at(reach.value)

    drive(stage, angle, omega)
    skater = SkaterModel(stage, np.zeros(3), lambda: angle.value, lambda: reach.value, scale=1.6)
    axis = axis_line(stage, [0, -0.1, 0], [0, 3.6, 0], cfg.OMEGA, 0.7)
    show(scene, stage, 1.0)
    reads = VGroup(readout("I =", lambda: K.inertia(reach.value), 1, "kg m²", cfg.INERTIA, size=46),
                   readout(r"\omega =", omega, 1, "rad/s", cfg.OMEGA, size=46),
                   readout("L =", lambda: K.inertia(reach.value) * omega(), 1, "kg m²/s", cfg.ANG_MOMENTUM, size=46))
    reads.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([4.0, 2.2, 0])
    scene.play(FadeIn(reads[0]), FadeIn(reads[1]), run_time=0.9)

    # --- 4. L = 4 x 2 = 8 ----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeIn(reads[2]), run_time=0.7)
    L_num = eq(rf"L = {fx(K.i_out)} \times {fx(K.omega_out)} = {fx(K.momentum)}", cfg.FONT["body"], cfg.ANG_MOMENTUM)
    L_num.move_to([4.0, 0.3, 0])
    scene.play(Write(L_num), run_time=1.2)

    # --- 5. Arms in: I drops to 2 -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(reach.to(stage, K.r_in, rate_func=smooth), run_time=3.0)
    faster = caption("arms in: the spin speeds up", cfg.OMEGA)
    scene.play(FadeIn(faster), run_time=0.6)

    # --- 6. L stays 8: omega = 8 / 2 = 4 ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    w_num = eq(rf"\omega = {{{fx(K.momentum)} \over {fx(K.i_in)}}} = {fx(K.omega_in)}\ \mathrm{{rad/s}}", cfg.FONT["section"],
               cfg.OMEGA)
    w_box = boxed(w_num, cfg.RESULT).move_to([4.0, -1.45, 0])
    no_torque = txt("negligible external torque\nabout the spin axis", cfg.FONT["tiny"], cfg.MUTED)
    fit_width(no_torque, 6.0)
    no_torque.move_to([4.0, -0.05, 0])
    scene.play(FadeOut(faster), fade_through(L_num, no_torque), run_time=0.7)
    scene.play(Write(w_num), run_time=1.4)
    scene.play(Create(w_box.frame), Indicate(reads[2], color=cfg.BALANCED), run_time=1.0)
    doubles = caption("the spin doubles", cfg.RESULT)
    scene.play(FadeIn(doubles), run_time=0.6)

    # --- 7. Kinetic energy: 8 J -> 16 J -----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(VGroup(w_box, w_num, no_torque, doubles)), reads.animate.scale(0.9).move_to([4.5, 2.8, 0]), run_time=0.8)
    K_steps = VGroup(eq(rf"K_1 = \tfrac12({fx(K.i_out)})({fx(K.omega_out)})^2 = {fx(K.k_out)}\ \mathrm{{J}}", cfg.FONT["body"], cfg.ENERGY),
                     eq(rf"K_2 = \tfrac12({fx(K.i_in)})({fx(K.omega_in)})^2 = {fx(K.k_in)}\ \mathrm{{J}}", cfg.FONT["body"], cfg.ENERGY))
    K_steps.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.4, 0.8, 0])
    fit_width(K_steps, 6.8)
    bars = VGroup(bar_meter(lambda: K.k_out, K.k_in, at=[2.6, -1.5, 0], height=1.8, color=cfg.ENERGY, label="K_1"),
                  bar_meter(lambda: K.k_in, K.k_in, at=[4.2, -1.5, 0], height=1.8, color=cfg.ENERGY, label="K_2"))
    scene.play(Write(K_steps[0]), FadeIn(bars[0]), run_time=1.4)
    scene.play(Write(K_steps[1]), FadeIn(bars[1]), run_time=1.4)

    # --- 8. Where did 8 J come from? ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    extra = eq(rf"+{fx(K.work)}\ \mathrm{{J}}\ ?", cfg.FONT["section"], cfg.WARNING).move_to([5.9, -1.2, 0])
    scene.play(FadeIn(extra, scale=1.1), run_time=0.8)

    # --- 9. The muscles do work ------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(reach.to(stage, K.r_out, rate_func=smooth), run_time=1.6)
    pulls = [Vector(lambda k=k: skater.hand_point(k),
                    lambda k=k: skater.hand_point(k) + 0.9 * mu.unit(np.array([0.0, skater.hand_point(k)[1], 0.0]) - skater.hand_point(k)),
                    cfg.FORCE, width=0.08, tip=0.24) for k in range(2)]
    hidden(*pulls)
    stage.add_overlay(*pulls)
    scene.play(*[stage.fade(p, 1.0) for p in pulls], run_time=0.6)
    scene.play(reach.to(stage, K.r_in, rate_func=smooth), run_time=2.4)
    work = caption("inward force + inward motion → positive work", cfg.FORCE)
    scene.play(FadeIn(work), FadeOut(extra), run_time=0.7)

    # --- 10. Internal forces: L unchanged, K changed -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    internal = caption("internal work changes K · total L stays fixed", cfg.WHITE)
    scene.play(fade_through(work, internal), *[stage.fade(p, 0.0) for p in pulls], run_time=0.9)

    # --- 11. Two answers ------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    verdict = VGroup(VGroup(txt("L conserved", cfg.FONT["body"], cfg.BALANCED), check_mark(0.25)).arrange(RIGHT, buff=0.25),
                     VGroup(txt("K not conserved", cfg.FONT["body"], cfg.WARNING), cross_mark(0.2)).arrange(RIGHT, buff=0.25))
    verdict.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.6, -1.2, 0])
    scene.play(FadeOut(internal), FadeOut(bars), FadeOut(K_steps), run_time=0.6)
    scene.play(FadeIn(verdict, lag_ratio=0.3), run_time=1.0)
    finish(scene, t, stage)
