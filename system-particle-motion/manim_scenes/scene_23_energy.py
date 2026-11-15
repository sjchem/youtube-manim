"""Scene 23 — rotational energy and work. A disc spins in place on a 3D
stand: its centre stays put, yet it carries energy. Gold particles on its
face light up with velocity arrows growing with r. The derivation builds:
K_i = 1/2 m_i v_i^2, v_i = r_i omega, sum, omega^2 out, the sum is I:
K_rot = 1/2 I omega^2 (boxed, beside 1/2 M v^2). The driven disc: K =
1/2 x 0.5 x 8^2 = 16 J, a coral bar. Work by a torque through an angle,
W = tau delta theta = 1 x 16 = 16 J, fills a matching bar. Then W as the
integral of tau d theta and the power P = tau omega.
"""

from manim_scenes.common import *

D = pm.DISC
S = 3.0


class Scene23Energy(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "23", "Rotational energy and work")
    spin = Knob(0.0)
    stage = Stage((-3.7, -0.4, 0.0), zoom=1.3, yaw=-0.25, pitch=0.12, sway=0.02)
    drive(stage, spin, 1.2)
    R = D.radius * S * 1.3
    w = wheel(stage, ORIGIN, R, lambda: -spin.value, half_length=0.18, sectors=8)
    centre_mark = com_tag(np.array([0, 0, 0.3]), 0.17)
    stage.add_overlay(centre_mark)
    show(scene, stage, 1.0)
    where = caption("stationary centre · moving particles", cfg.WHITE)
    scene.play(FadeIn(where), run_time=0.8)

    # --- 2. In its particles ----------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    samples = [(0.6, 0.3), (1.2, 1.7), (1.8, 3.4), (0.9, 4.6), (1.5, 5.6)]

    def where_p(r, a0):
        a = a0 - spin.value
        return np.array([r * np.cos(a), r * np.sin(a), 0.25])

    def vel(r, a0):
        a = a0 - spin.value
        return 0.42 * r * np.array([np.sin(a), -np.cos(a), 0.0])

    beads, arrows = [], []
    for r, a0 in samples:
        b = Ball(lambda r=r, a0=a0: where_p(r, a0), 0.1, cfg.GOLD, layers=10)
        b.bias = 50.0
        v = Vector(lambda r=r, a0=a0: where_p(r, a0), lambda r=r, a0=a0: where_p(r, a0) + vel(r, a0), cfg.VELOCITY, width=0.05,
                   tip=0.18)
        hidden(b, v)
        beads.append(b)
        arrows.append(v)
    stage.add_body(*beads)
    stage.add_overlay(*arrows)
    Ki = eq(r"K_i = \tfrac12 m_i v_i^2", cfg.FONT["section"], cfg.ENERGY).move_to([3.4, 2.8, 0])
    scene.play(FadeOut(where), *[stage.fade(b, 1.0) for b in beads], *[stage.fade(a, 1.0) for a in arrows], run_time=1.0)
    scene.play(Write(Ki), run_time=1.2)

    # --- 3. v_i = r_i omega ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    sub = eq(r"v_i = r_i\,\omega", cfg.FONT["body"], cfg.VELOCITY).next_to(Ki, DOWN, buff=0.3)
    Ki2 = eq(r"K_i = \tfrac12 m_i r_i^2 \omega^2", cfg.FONT["section"], cfg.ENERGY).next_to(sub, DOWN, buff=0.3)
    scene.play(FadeIn(sub, shift=UP * 0.1), run_time=0.8)
    scene.play(FadeIn(Ki2, shift=DOWN * 0.1), run_time=1.4)

    # --- 4. Sum: omega out, I inside ----------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    total = eq([r"K_{\text{rot}}", "=", r"\tfrac12", r"\Big(\sum_i m_i r_i^2\Big)", r"\omega^2"], cfg.FONT["section"], cfg.WHITE)
    total[0].set_color(cfg.ENERGY)
    total.next_to(Ki2, DOWN, buff=0.45)
    fit_width(total, 7.6)
    scene.play(Write(total), run_time=1.8)
    brace = Brace(total[3], DOWN, color=cfg.INERTIA)
    I_tag = eq("I", cfg.FONT["section"], cfg.INERTIA).next_to(brace, DOWN, buff=0.08)
    scene.play(GrowFromCenter(brace), FadeIn(I_tag), run_time=0.9)

    # --- 5. K_rot = 1/2 I omega^2 --------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    law = eq(r"K_{\text{rot}} = \tfrac12 I\,\omega^2", cfg.FONT["title"], cfg.ENERGY)
    law_box = boxed(law, cfg.RESULT).move_to([3.4, 1.6, 0])
    partner = eq(r"\leftrightarrow\ \tfrac12 M v^2", cfg.FONT["body"], cfg.MUTED).next_to(law_box, DOWN, buff=0.3)
    scene.play(FadeOut(VGroup(Ki, sub, Ki2, total, brace, I_tag)), run_time=0.6)
    scene.play(Write(law), run_time=1.4)
    scene.play(Create(law_box.frame), FadeIn(partner), run_time=0.8)

    # --- 6. The disc: 16 J ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(*[stage.fade(x, 0.0) for x in beads + arrows], FadeOut(partner),
               VGroup(law_box, law).animate.scale(0.7).move_to([3.0, 3.2, 0]), run_time=0.8)
    K_num = eq(rf"K = \tfrac12({fx(D.inertia, 1)})({fx(D.omega_end)})^2 = {fx(D.kinetic)}\ \mathrm{{J}}", cfg.FONT["section"],
               cfg.ENERGY).move_to([2.6, 1.8, 0])
    fit_width(K_num, 7.8)
    scene.play(Write(K_num), run_time=1.8)
    K_bar = bar_meter(lambda: D.kinetic, D.kinetic, at=[5.5, -1.3, 0], height=2.6, color=cfg.ENERGY, label="K")
    scene.play(FadeIn(K_bar), run_time=0.8)

    # --- 7. Where did 16 J come from? ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    q = caption("where did the energy come from?", cfg.WHITE)
    scene.play(FadeIn(q), run_time=0.6)

    # --- 8. W = tau delta theta ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    pair = VGroup(eq(r"W = F\,\Delta x", cfg.FONT["body"], cfg.MUTED), eq(r"W = \tau\,\Delta\theta", cfg.FONT["section"], cfg.TORQUE))
    pair.arrange(RIGHT, buff=0.6)
    fit_width(pair, 7.6)
    pair.move_to([3.2, 0.4, 0])
    scene.play(FadeOut(q), FadeIn(pair[0]), run_time=0.8)
    scene.play(FadeIn(pair[1], shift=RIGHT * 0.15), run_time=1.4)

    # --- 9. 1 x 16 = 16 J ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    W_num = eq(rf"W = {fx(D.torque)} \times {fx(D.angle_end)} = {fx(D.work)}\ \mathrm{{J}}", cfg.FONT["section"], cfg.TORQUE)
    fit_width(W_num, 5.8)
    W_num.move_to([2.0, -1.0, 0])
    W_bar = bar_meter(lambda: D.work, D.kinetic, at=[6.8, -1.3, 0], height=2.6, color=cfg.TORQUE, label="W")
    scene.play(Write(W_num), FadeIn(W_bar), run_time=1.6)
    equal = eq(r"W = \Delta K", cfg.FONT["section"], cfg.BALANCED).move_to([2.0, -2.3, 0])
    scene.play(FadeIn(equal, shift=UP * 0.1), run_time=0.8)

    # --- 10. Variable torque, power -------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(VGroup(pair, K_num, W_num, equal, K_bar, W_bar)), run_time=0.6)
    more = VGroup(eq(r"W = \int \tau\, d\theta", cfg.FONT["section"], cfg.TORQUE),
                  eq(r"P = \tau\,\omega", cfg.FONT["title"], cfg.ENERGY)).arrange(DOWN, buff=0.5).move_to([3.5, 0.9, 0])
    scene.play(Write(more[0]), run_time=1.2)
    scene.play(Write(more[1]), run_time=1.2)
    uses = txt("motors · turbines · flywheels", cfg.FONT["small"], cfg.MUTED).next_to(more, DOWN, buff=0.4)
    scene.play(FadeIn(uses), run_time=0.7)

    # --- 11. Speaking in angles ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    angles = caption("work and energy, spoken in angles", cfg.ENERGY)
    scene.play(FadeIn(angles), run_time=0.7)
    finish(scene, t, stage)
