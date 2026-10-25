"""Chapter 03 — waves add or cancel; then the same thing with two 1s orbitals.

Every curve is coloured by its sign (blue +, rose -). The second wave's phase
and the second orbital's coefficient are live trackers, so reinforcement and
cancellation happen continuously on screen. The 1s profiles are
``physics_models.one_s_profile``; the node of the difference sits exactly
halfway between the nuclei.
"""

from manim_scenes.common import *

WAVE_TOP = PlotFrame([0, 1.35, 0], 1.0, 0.75)
WAVE_SUM = PlotFrame([0, -1.25, 0], 1.0, 0.68)
X_RANGE = (-6.6, 6.6)
ORB = PlotFrame([0, -0.4, 0], 1.55, 2.6)
NUCLEUS = 1.0          # bohr; the profiles sit at -1 and +1
ORB_RANGE = (-4.4, 4.4)


class Scene03Waves(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "03", "Waves add or cancel")

    # --- 1. A wave ------------------------------------------------------------------------------------------------------
    phase = ValueTracker(0.0)
    amp_b = ValueTracker(0.0)
    axis_top, axis_sum = WAVE_TOP.axis(*X_RANGE), WAVE_SUM.axis(*X_RANGE)
    wave_a = signed_curve(lambda x: pm.wave(x), X_RANGE, WAVE_TOP)
    scene.play(Create(axis_top), run_time=0.6)
    scene.play(Create(wave_a), run_time=2.0)
    dismiss_opening_title(scene, t, head, at=3.4)

    # --- 2. Peaks, troughs, and a sign ------------------------------------------------------------------------------------
    beat(scene, t, 1)
    plus = eq("+", cfg.FONT["section"], cfg.PHASE_PLUS).move_to(WAVE_TOP.point(1.0, 1.75))
    minus = eq("-", cfg.FONT["section"], cfg.PHASE_MINUS).move_to(WAVE_TOP.point(3.0, -1.75))
    scene.play(FadeIn(plus, shift=DOWN * 0.15), run_time=0.7)
    scene.play(FadeIn(minus, shift=UP * 0.15), run_time=0.7)
    standing = caption("A wave has peaks, troughs, and a sign", cfg.WHITE)
    scene.play(FadeIn(standing), run_time=0.8)

    # --- 3. In phase: they reinforce ---------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    wave_b = live(lambda: signed_curve(lambda x: pm.wave(x, phase=phase.get_value(), amplitude=amp_b.get_value()),
                                       X_RANGE, WAVE_TOP, plus=cfg.TEAL, minus=cfg.ORANGE, width=4.0))
    total = live(lambda: plain_curve(lambda x: pm.wave(x) + pm.wave(x, phase=phase.get_value(), amplitude=amp_b.get_value()),
                                     X_RANGE, WAVE_SUM, cfg.WHITE, width=7.0))
    sum_label = txt("sum", cfg.FONT["label"], cfg.WHITE).next_to(axis_sum, LEFT, buff=0.25).shift(UP * 0.0)
    fit_width(sum_label, 1.2)
    scene.add(wave_b)
    scene.play(amp_b.animate.set_value(1.0), FadeOut(plus), FadeOut(minus), run_time=1.4)
    scene.play(Create(axis_sum), FadeIn(total), FadeIn(sum_label), run_time=1.2)
    together = caption("Peaks line up: they reinforce", cfg.GREEN)
    scene.play(fade_through(standing, together), run_time=0.8)
    scene.remove(standing)
    scene.play(Indicate(total, color=cfg.GREEN, scale_factor=1.04), run_time=1.2)

    # --- 4. Half a wavelength: they cancel -----------------------------------------------------------------------------------------
    beat(scene, t, 3)
    apart = caption("Peak meets trough: they cancel", cfg.RED)
    scene.play(phase.animate.set_value(0.5), fade_through(together, apart), run_time=3.2, rate_func=smooth)
    scene.remove(together)
    flat = glow_frame(Rectangle(width=13.2, height=0.5).move_to(WAVE_SUM.origin), cfg.RED, buff=0.05)
    scene.play(Create(flat), run_time=0.8)
    scene.play(FadeOut(flat), run_time=0.6)

    # --- 5. Same waves, different phase ------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    same = caption("Same two waves. Different phase.", cfg.CYAN)
    scene.play(fade_through(apart, same), run_time=0.8)
    scene.remove(apart)
    scene.play(phase.animate.set_value(0.0), run_time=2.0, rate_func=smooth)
    scene.play(phase.animate.set_value(0.5), run_time=2.0, rate_func=smooth)

    # --- 6. Now two hydrogen orbitals along the axis -----------------------------------------------------------------------------------------
    beat(scene, t, 5)
    for mob in (wave_a, wave_b, total):
        mob.clear_updaters()
    scene.play(FadeOut(wave_a), FadeOut(wave_b), FadeOut(total), FadeOut(axis_top), FadeOut(axis_sum), FadeOut(sum_label),
               FadeOut(same), run_time=1.0)
    coeff = ValueTracker(1.0)
    shown = ValueTracker(0.0)     # 0: the two orbitals; 1: their combination
    axis = ORB.axis(*ORB_RANGE)
    nuclei = VGroup(*[nucleus_dot(ORB.point(x, 0)) for x in (-NUCLEUS, NUCLEUS)])
    names = VGroup(eq(r"\phi_A", cfg.FONT["body"], cfg.PHASE_PLUS).move_to(ORB.point(-2.6, 0.75)),
                   eq(r"\phi_B", cfg.FONT["body"], cfg.PHASE_PLUS).move_to(ORB.point(2.6, 0.75)))
    phi_a = signed_curve(lambda x: pm.one_s_profile(x, -NUCLEUS), ORB_RANGE, ORB, width=5.0)
    phi_b = live(lambda: signed_curve(lambda x: coeff.get_value() * pm.one_s_profile(x, NUCLEUS), ORB_RANGE, ORB,
                                      width=5.0))
    scene.play(Create(axis), FadeIn(nuclei), run_time=1.0)
    scene.play(Create(phi_a), FadeIn(phi_b), FadeIn(names), run_time=2.0)
    peaks = caption("Each orbital: a sharp peak that fades with distance", cfg.WHITE)
    scene.play(FadeIn(peaks), run_time=0.8)

    # --- 7. Height is psi; sign is phase -----------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    psi_axis = Arrow(ORB.point(-4.2, -0.15), ORB.point(-4.2, 1.2), buff=0, color=cfg.MUTED, stroke_width=5,
                     tip_length=0.24)
    psi_label = eq(r"\psi", cfg.FONT["section"], cfg.WHITE).next_to(psi_axis, LEFT, buff=0.2)
    sign = eq(r"\text{sign} = \text{phase}", cfg.FONT["label"], cfg.PHASE_PLUS).move_to([3.8, 3.0, 0])
    scene.play(GrowArrow(psi_axis), Write(psi_label), run_time=1.0)
    scene.play(FadeIn(sign, shift=DOWN * 0.15), run_time=0.8)

    # --- 8. In phase: they pile up in the middle -------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    combo = live(lambda: signed_curve(lambda x: (pm.one_s_profile(x, -NUCLEUS) + coeff.get_value() *
                                                 pm.one_s_profile(x, NUCLEUS)) * shown.get_value(),
                                      ORB_RANGE, ORB, width=8.0, plus=mu.mix(cfg.PHASE_PLUS, cfg.WHITE, 0.45),
                                      minus=mu.mix(cfg.PHASE_MINUS, cfg.WHITE, 0.3)))
    scene.add(combo)
    add_eq = eq(r"\phi_A + \phi_B", cfg.FONT["section"], cfg.WHITE).move_to([-3.8, 3.0, 0])
    scene.play(shown.animate.set_value(1.0), Write(add_eq), FadeOut(peaks), *dim_curve(phi_a, 0.3),
               run_time=2.0)
    middle = glow_dot(ORB.point(0, 2 * float(pm.one_s_profile(0.0, NUCLEUS))), cfg.GREEN, radius=0.1)
    pile = caption("In phase: the waves pile up in the middle", cfg.GREEN)
    scene.play(FadeIn(middle, scale=0.5), FadeIn(pile), run_time=1.0)

    # --- 9. Subtract: a node halfway -------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    sub_eq = eq(r"\phi_A - \phi_B", cfg.FONT["section"], cfg.WHITE).move_to(add_eq)
    scene.play(coeff.animate.set_value(-1.0), Transform(add_eq, sub_eq), FadeOut(middle), FadeOut(pile),
               run_time=3.2, rate_func=smooth)
    node = glow_dot(ORB.point(0, 0), cfg.GOLD, radius=0.12)
    node_word = txt("node", cfg.FONT["body"], cfg.GOLD).move_to(ORB.point(-1.15, -0.4))
    zero = caption("Halfway between: psi = 0. A node.", cfg.GOLD)
    scene.play(FadeIn(node, scale=0.4), FadeIn(node_word), FadeIn(zero), run_time=1.0)
    scene.play(Indicate(node, color=cfg.WHITE, scale_factor=1.5), run_time=1.2)

    # --- 10. The whole story in miniature ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    story = caption("Add: pile up.   Subtract: a node.", cfg.CYAN)
    scene.play(fade_through(zero, story), run_time=0.8)
    scene.remove(zero)
    scene.play(coeff.animate.set_value(1.0), FadeOut(node), FadeOut(node_word), run_time=2.0, rate_func=smooth)
    scene.play(coeff.animate.set_value(-1.0), run_time=2.0, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["03"])
