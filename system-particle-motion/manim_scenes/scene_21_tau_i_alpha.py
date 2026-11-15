"""Scene 21 — Newton's second law for rotation. A disc faces the viewer on a
3D stage with one gold particle m at distance r. A green force on it splits
into a dim radial part and an outlined white tangential part F_t. The radius
r and its arrow are outlined magenta. The derivation
builds line by line on the right: F_t = m a_t, a_t = r alpha, so F_t = m r
alpha; multiplied by r, the torque on that particle is m r^2 alpha. Every
particle then lights up with its own tangential push; alpha comes out of
the sum, the sum of m r^2 is I, the internal torques cancel: tau_net =
I alpha, boxed. A three-row dictionary pairs torque with force, I with mass,
alpha with a; short comparisons explain alpha = tau / I.
"""

from manim_scenes.common import *

CENTRE = np.array([-3.6, -0.5, 0.0])
R_DISC = 2.5
P_ANGLE = np.radians(35)
R_P = 1.9
R_COLOR = "#FF5EA8"          # matches the visible radius in scene 10
FT_COLOR = cfg.WHITE        # outlined white distinguishes tangential force from radius


class Scene21TauIAlpha(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "21", "Newton's second law for rotation")
    stage = Stage(CENTRE, zoom=1.05, yaw=-0.12, pitch=0.1, sway=0.015)
    spin = Knob(0.0)
    drive(stage, spin, 0.25)
    disc = Drum(ORIGIN, R_DISC, 0.1, cfg.DISC_BODY, spin=lambda: spin.value, stripe=cfg.DISC_STRIPE, sectors=8)
    hub = Ball(np.array([0, 0, 0.15]), 0.12, cfg.STEEL, layers=10)
    stage.add_body(disc, hub)
    show(scene, stage, 1.0)
    link = caption("torque and moment of inertia, connected", cfg.WHITE)
    scene.play(FadeIn(link), run_time=0.7)

    # --- 2. One particle; only the tangential push changes its speed ---------------------------------------------------
    beat(scene, t, 1)

    def where(r: float = R_P, extra: float = 0.0) -> np.ndarray:
        a = P_ANGLE + spin.value + extra
        return np.array([r * np.cos(a), r * np.sin(a), 0.2])

    def tangent(extra: float = 0.0) -> np.ndarray:
        a = P_ANGLE + spin.value + extra
        return np.array([-np.sin(a), np.cos(a), 0.0])

    def outward(extra: float = 0.0) -> np.ndarray:
        a = P_ANGLE + spin.value + extra
        return np.array([np.cos(a), np.sin(a), 0.0])

    particle = Ball(lambda: where(), 0.16, cfg.GOLD, layers=14)
    particle.bias = 50.0
    r_vec = Vector(lambda: np.array([0, 0, 0.2]), lambda: where(), R_COLOR, width=0.09, tip=0.28, glow=False)
    r_vec.body.set_stroke(cfg.BG, width=2.5)
    r_lab = Tag(eq("r", cfg.FONT["body"], R_COLOR).set_stroke(cfg.BG, width=1.2), lambda: np.array([-0.6, -1.1, 0.2]), DOWN * 0.2)
    m_lab = Tag(eq("m", cfg.FONT["body"], cfg.GOLD), lambda: np.array([-1.4, 0.5, 0.2]), LEFT * 0.3)
    F_full = Vector(lambda: where(), lambda: where() + 1.4 * tangent() - 0.9 * outward(), cfg.FORCE, width=0.08, tip=0.26)
    F_rad = Vector(lambda: where(), lambda: where() - 0.9 * outward(), cfg.MUTED, width=0.05, tip=0.2)
    F_t = Vector(lambda: where(), lambda: where() + 1.4 * tangent(), FT_COLOR, width=0.105, tip=0.3, glow=False)
    F_t.body.set_stroke(cfg.BG, width=2.5)
    Ft_lab = Tag(eq("F_t", cfg.FONT["body"], FT_COLOR).set_stroke(cfg.BG, width=1.2), lambda: where() + 1.4 * tangent(), UL * 0.4)
    hidden(particle, r_vec, r_lab, m_lab, F_full, F_rad, F_t, Ft_lab)
    stage.add_body(particle)
    stage.add_overlay(r_vec, r_lab, m_lab, F_full, F_rad, F_t, Ft_lab)
    scene.play(FadeOut(link), stage.fade(particle, 1.0), stage.fade(m_lab, 1.0), stage.fade(r_vec, 1.0),
               stage.fade(r_lab, 1.0), run_time=1.0)
    scene.play(stage.fade(F_full, 1.0), run_time=0.8)
    scene.play(stage.fade(F_full, 0.0), stage.fade(F_rad, 0.6), stage.fade(F_t, 1.0), stage.fade(Ft_lab, 1.0), run_time=1.2)
    only = caption("only the tangential part changes its speed", FT_COLOR)
    scene.play(FadeIn(only), run_time=0.6)

    # --- 3. F_t = m a_t = m r alpha -----------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    X = 3.6
    lines = [
        eq(r"F_t = m\,a_t", cfg.FONT["section"], cfg.WHITE),
        eq(r"a_t = r\,\alpha", cfg.FONT["body"], cfg.TANGENTIAL),
        eq(r"F_t = m\,r\,\alpha", cfg.FONT["section"], cfg.WHITE),
    ]
    lines[0].move_to([X, 2.8, 0])
    lines[1].next_to(lines[0], DOWN, buff=0.3)
    lines[2].next_to(lines[1], DOWN, buff=0.3)
    scene.play(FadeOut(only), Write(lines[0]), run_time=1.2)
    scene.play(FadeIn(lines[1], shift=UP * 0.1), run_time=0.8)
    scene.play(Write(lines[2]), run_time=1.2)

    # --- 4. Multiply by r: the torque on one particle ----------------------------------------------------------------------------------
    beat(scene, t, 3)
    torque_one = eq([r"r F_t", "=", r"m r^2 \alpha"], cfg.FONT["section"], cfg.WHITE)
    torque_one[0].set_color(cfg.TORQUE)
    torque_one.next_to(lines[2], DOWN, buff=0.45)
    times_r = txt("× r", cfg.FONT["body"], R_COLOR).next_to(torque_one, LEFT, buff=0.4)
    scene.play(FadeIn(times_r), run_time=0.6)
    scene.play(FadeIn(torque_one, shift=DOWN * 0.12), run_time=1.4)
    tau_i = Brace(torque_one[0], DOWN, color=cfg.TORQUE)
    tau_tag = eq(r"\tau_i", cfg.FONT["body"], cfg.TORQUE).next_to(tau_i, DOWN, buff=0.08)
    scene.play(GrowFromCenter(tau_i), FadeIn(tau_tag), run_time=0.8)

    # --- 5. Every particle ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    extras = [(1.0, 1.3), (0.6, 2.6), (1.5, 3.9), (2.2, 5.0), (1.3, 0.6)]
    others = []
    for r, extra in extras:
        dot_ = Ball(lambda r=r, e=extra: where(r, e), 0.11, cfg.GOLD, layers=10)
        dot_.bias = 50.0
        push = Vector(lambda r=r, e=extra: where(r, e), lambda r=r, e=extra: where(r, e) + 0.7 * tangent(e), FT_COLOR,
                      width=0.075, tip=0.22, glow=False)
        push.body.set_stroke(cfg.BG, width=2.5)
        hidden(dot_, push)
        stage.add_body(dot_)
        stage.add_overlay(push)
        others += [dot_, push]
    scene.play(*[stage.fade(o, 1.0) for o in others], stage.fade(F_rad, 0.0), stage.fade(r_lab, 0.0),
               FadeOut(VGroup(*lines[:2], times_r)), run_time=1.0)
    same_alpha = caption("every particle shares the same alpha", cfg.ANGLE)
    scene.play(FadeIn(same_alpha), run_time=0.6)

    # --- 6. Sum: alpha out, I inside, internal torques cancel ----------------------------------------------------------------------------------
    beat(scene, t, 5)
    summed = eq([r"\sum \tau_i", "=", r"\Big(\sum m_i r_i^2\Big)", r"\alpha"], cfg.FONT["section"], cfg.WHITE)
    summed[0].set_color(cfg.TORQUE)
    summed.move_to([X, -1.2, 0])
    scene.play(FadeOut(same_alpha), FadeOut(VGroup(lines[2], torque_one, tau_i, tau_tag)), run_time=0.6)
    summed.move_to([X, 1.6, 0])
    scene.play(Write(summed), run_time=1.4)
    I_brace = Brace(summed[2], DOWN, color=cfg.INERTIA)
    I_tag = eq("I", cfg.FONT["section"], cfg.INERTIA).next_to(I_brace, DOWN, buff=0.08)
    scene.play(GrowFromCenter(I_brace), FadeIn(I_tag), run_time=0.9)
    internal = txt("internal torques cancel in pairs", cfg.FONT["small"], cfg.FORCE).next_to(I_tag, DOWN, buff=0.35)
    scene.play(FadeIn(internal), run_time=0.7)

    # --- 7. tau_net = I alpha ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    law = eq(r"\tau_{\text{net}} = I\,\alpha", cfg.FONT["hero"], cfg.WHITE)
    law_box = boxed(law, cfg.RESULT).move_to([X, 0.4, 0])
    scene.play(FadeOut(VGroup(summed, I_brace, I_tag, internal)), run_time=0.6)
    scene.play(Write(law), run_time=1.4)
    scene.play(Create(law_box.frame), run_time=0.7)

    # --- 8. The dictionary -----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    dictionary = VGroup(
        eq(r"\tau \;\leftrightarrow\; F", cfg.FONT["body"], cfg.TORQUE),
        eq(r"I \;\leftrightarrow\; m", cfg.FONT["body"], cfg.INERTIA),
        eq(r"\alpha \;\leftrightarrow\; a", cfg.FONT["body"], cfg.ANGLE),
    ).arrange(RIGHT, buff=0.9).move_to([X - 0.2, -1.6, 0])
    fit_width(dictionary, 7.6)
    second = eq(r"F = m a", cfg.FONT["body"], cfg.MUTED).next_to(law_box, UP, buff=0.35)
    scene.play(FadeIn(second), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(d, shift=UP * 0.15) for d in dictionary], lag_ratio=0.4), run_time=1.6)

    # --- 9. alpha = tau / I --------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    alpha_eq = eq(r"\alpha = {\tau \over I}", cfg.FONT["section"], cfg.ANGLE).move_to([X - 1.9, -3.1, 0])
    scene.play(Write(alpha_eq), run_time=1.2)
    rules = VGroup(txt("bigger τ: faster spin-up", cfg.FONT["tiny"], cfg.TORQUE),
                   txt("bigger I: slower spin-up", cfg.FONT["tiny"], cfg.INERTIA)).arrange(DOWN, buff=0.12)
    fit_width(rules, 3.8)
    rules.next_to(alpha_eq, RIGHT, buff=0.4)
    scene.play(FadeIn(rules, lag_ratio=0.4), run_time=1.0)
    finish(scene, t, stage)
