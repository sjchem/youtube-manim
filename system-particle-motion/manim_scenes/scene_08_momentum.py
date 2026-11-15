"""Scene 08 — the momentum of a system. Two carts sit on a 3D frictionless
track with gold velocity arrows. The definitions build above them: P is the
sum of m_i v_i; differentiating M R_cm = sum m_i r_i gives P = M v_cm; dP/dt
= F_ext; with no external force, P is constant. The worked example: 2 kg at
3 m/s and 3 kg at -1 m/s give P = 3 kg m/s and v_cm = 0.6 m/s. The
spring-bumper collision (a velocity-Verlet run from ``physics_models``) then
plays: both velocity arrows swing round, live readouts change, and the
centre-of-mass target and its readout glide on at 0.60 m/s.
"""

from manim_scenes.common import *

C = pm.CARTS
SC = 1.3                                    # screen units per metre
SHIFT = 0.25                                # metres: centres the action on the track
BODY = 2 * C.half_length - 0.2              # drawn body length; 0.1 m spring bumpers on the facing ends
V_SCALE = 0.55
CART_COLORS = ("#4FB3E8", "#C98A4B")


class Scene08Momentum(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "08", "The momentum of a system")
    times, xs, vs = pm.cart_run()
    masses = np.array([C.m1, C.m2])
    clock = Knob(0.0)

    def x_of(k: int) -> float:
        return float(np.interp(clock.value, times, xs[:, k]))

    def v_of(k: int) -> float:
        return float(np.interp(clock.value, times, vs[:, k]))

    def screen_x(x: float) -> float:
        return (x + SHIFT) * SC

    stage = Stage((0.0, -2.35, 0.0), zoom=1.02, yaw=-0.1, pitch=0.3, sway=0.025)
    floor(stage, -0.32, reach=7.5, opacity=0.2)
    rail = Block(np.array([0.0, -0.27, 0.0]), (13.0, 0.08, 0.9), "#3A4A58")
    rail.keep_in_frame = False  # The continuous track extends beyond the camera.
    stage.add_body(rail)
    carts = []
    for k in range(2):
        centre = lambda k=k: np.array([screen_x(x_of(k)), 0.08, 0.0])  # noqa: E731
        body = Block(centre, (BODY * SC, 0.42, 0.62), CART_COLORS[k])
        wheels = [Drum(lambda k=k, dx=dx, dz=dz: np.array([screen_x(x_of(k)) + dx, -0.12, dz]), 0.1, 0.035, "#2A3440",
                       axis=(0, 0, 1), spin=lambda k=k: -screen_x(x_of(k)) / 0.1, stripe=cfg.STEEL, sectors=4)
                  for dx in (-0.28, 0.28) for dz in (-0.33, 0.33)]
        stage.add_body(*wheels, body)
        carts.append(SimpleNamespace(body=body, centre=centre))

    def bumper(k: int):
        """A spring on the facing end of cart k (right end of cart 0, left end of cart 1)."""
        def pts():
            gap = x_of(1) - x_of(0) - BODY
            length = min(0.1, gap / 2)
            sign = 1 if k == 0 else -1
            face = screen_x(x_of(k)) + sign * BODY * SC / 2
            end = face + sign * length * SC
            xs_ = np.linspace(face, end, 9)
            return np.array([[x, 0.08 + (0.1 if i % 2 else -0.1) * (0 < i < 8), 0.0] for i, x in enumerate(xs_)])
        return pts

    springs = [Curve(bumper(k), cfg.STEEL, width=4, glow=False) for k in range(2)]
    stage.add_body(*springs)
    arrows = [Vector(lambda k=k: carts[k].centre() + np.array([0, 0.5, 0]),
                     lambda k=k: carts[k].centre() + np.array([v_of(k) * V_SCALE, 0.5, 0]), cfg.VELOCITY, width=0.09, tip=0.28)
              for k in range(2)]
    stage.add_overlay(*arrows)
    show(scene, stage, 1.0)

    # --- 1. P = sum m_i v_i ------------------------------------------------------------------------------------
    P_def = eq(r"\vec P = \sum_i m_i \vec v_i", cfg.FONT["title"], cfg.MOMENTUM).move_to([0, 2.3, 0])
    scene.play(Write(P_def), run_time=1.6)

    # --- 2. P = M v_cm ------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    chain = VGroup(eq(r"M \vec R_{\mathrm{cm}} = \sum_i m_i \vec r_i", cfg.FONT["body"]),
                   eq(r"\xrightarrow{\ d/dt\ }", cfg.FONT["body"], cfg.MUTED),
                   eq(r"M \vec v_{\mathrm{cm}} = \sum_i m_i \vec v_i", cfg.FONT["body"])).arrange(RIGHT, buff=0.35)
    fit_width(chain, 13.4)
    chain.move_to([0, 2.7, 0])
    scene.play(FadeOut(P_def, shift=UP * 0.3), run_time=0.8)
    scene.play(Write(chain[0]), run_time=1.4)
    scene.play(FadeIn(chain[1], shift=RIGHT * 0.2), run_time=0.8)
    scene.play(Write(chain[2]), run_time=1.4)
    P_law = eq(r"\vec P = M \vec v_{\mathrm{cm}}", cfg.FONT["title"], cfg.WHITE)
    P_box = boxed(P_law, cfg.RESULT).move_to([0, 1.25, 0])
    scene.play(FadeIn(P_law, shift=UP * 0.1), run_time=1.2)
    scene.play(Create(P_box.frame), run_time=0.7)

    # --- 3. dP/dt = F_ext ---------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    dPdt = eq(r"{d\vec P \over dt} = \vec F_{\text{ext}}", cfg.FONT["section"], cfg.WHITE)
    scene.play(FadeOut(chain), run_time=0.3)
    scene.play(P_box.animate.scale(0.75).move_to([-4.0, 2.85, 0]), run_time=0.6)
    dPdt.move_to([2.4, 2.85, 0])
    scene.play(Write(dPdt), run_time=1.4)

    # --- 4. No external force: P is constant ----------------------------------------------------------------------------
    beat(scene, t, 3)
    conserved = eq(r"\vec F_{\text{ext}} = 0 \ \Rightarrow\ \vec P = \text{constant}", cfg.FONT["body"], cfg.BALANCED)
    conserved.move_to([0, 1.45, 0])
    scene.play(Write(conserved), run_time=1.6)
    scene.play(Create(glow_frame(conserved, cfg.BALANCED)), run_time=0.8)

    # --- 5. The two carts ----------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(*[FadeOut(m) for m in scene.mobjects if m not in (stage,) and not getattr(m, "_is_project_background", False)],
               run_time=0.8)
    kg = [Tag(txt(f"{fx(m)} kg", cfg.FONT["label"], cfg.MASS), lambda k=k: carts[k].centre(), DOWN * 0.95)
          for k, m in enumerate(masses)]
    speeds = [Tag(eq(rf"{fx(abs(v))}\ \mathrm{{m/s}}", cfg.FONT["label"], cfg.VELOCITY),
                  lambda k=k: carts[k].centre() + np.array([v_of(k) * V_SCALE / 2, 0.5, 0]), UP * 0.42)
              for k, v in enumerate((C.v1, C.v2))]
    hidden(*kg, *speeds)
    stage.add_overlay(*kg, *speeds)
    frictionless = txt("frictionless track", cfg.FONT["small"], cfg.MUTED).move_to([0, -0.4, 0])
    scene.play(FadeIn(frictionless), *[stage.fade(k, 1.0) for k in kg], run_time=1.0)
    scene.play(*[stage.fade(s, 1.0) for s in speeds], *stage.turn(pitch=0.24), run_time=1.2)
    right = VGroup(txt("right is positive", cfg.FONT["small"], cfg.MUTED),
                   Arrow(LEFT * 0.5, RIGHT * 0.5, stroke_color=cfg.MUTED, buff=0)).arrange(RIGHT, buff=0.25)
    right.move_to([-4.6, 3.2, 0])
    scene.play(FadeIn(right), run_time=0.8)

    # --- 6. P = 2(3) + 3(-1) = 3 ------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    P_num = eq(rf"P = {fx(C.m1)}({fx(C.v1)}) + {fx(C.m2)}({fx(C.v2)}) = {fx(C.momentum)}\ \mathrm{{kg\,m/s}}",
               cfg.FONT["section"], cfg.MOMENTUM)
    fit_width(P_num, 13.4)
    P_num.move_to([0, 2.15, 0])
    scene.play(FadeOut(frictionless), Write(P_num), run_time=2.2)

    # --- 7. v_cm = P / M = 0.6 m/s ---------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    v_num = eq(rf"v_{{\mathrm{{cm}}}} = {{P \over M}} = {{{fx(C.momentum)} \over {fx(C.total)}}} = {fx(C.v_cm, 1)}\ \mathrm{{m/s}}",
               cfg.FONT["section"], cfg.WHITE)
    v_box = boxed(v_num, cfg.RESULT).move_to([0, 0.75, 0])
    scene.play(Write(v_num), run_time=1.8)
    scene.play(Create(v_box.frame), run_time=0.6)

    def com_x() -> float:
        return float((masses @ np.array([x_of(0), x_of(1)])) / masses.sum())

    target = com_tag(lambda: np.array([screen_x(com_x()), 0.95, 0.0]), 0.2)
    v_arrow = Vector(lambda: np.array([screen_x(com_x()), 0.95, 0.0]),
                     lambda: np.array([screen_x(com_x()) + C.v_cm * V_SCALE * 2.2, 0.95, 0.0]), cfg.WHITE, width=0.07, tip=0.24)
    drop = Segment(lambda: np.array([screen_x(com_x()), 0.75, 0.0]), lambda: np.array([screen_x(com_x()), -0.2, 0.0]),
                   cfg.WHITE, width=2.5, opacity=0.7, dashed=True)
    hidden(target, v_arrow, drop)
    stage.add_body(drop)
    stage.add_overlay(target, v_arrow)
    scene.play(stage.fade(target, 1.0), stage.fade(drop, 1.0), run_time=0.8)
    scene.play(stage.fade(v_arrow, 1.0), run_time=0.6)

    # --- 8. The collision -------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(P_num), FadeOut(right), *[stage.fade(s, 0.0) for s in speeds], *[stage.fade(k, 0.0) for k in kg],
               run_time=0.6)
    readouts = VGroup(
        readout(r"v_1 =", lambda: v_of(0), 2, "m/s", cfg.VELOCITY, size=48),
        readout(r"v_2 =", lambda: v_of(1), 2, "m/s", cfg.VELOCITY, size=48),
    ).arrange(RIGHT, buff=1.2).move_to([0, 2.6, 0])
    scene.play(FadeIn(readouts), run_time=0.6)
    scene.play(clock.to(stage, 1.75, rate_func=linear), run_time=5.4)

    # --- 9. The centre does not flinch ------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    vcm_live = readout(r"v_{\mathrm{cm}} =", lambda: float(masses @ np.array([v_of(0), v_of(1)]) / masses.sum()), 2, "m/s",
                       cfg.WHITE, size=52)
    vcm_live.move_to([0, 1.2, 0])
    scene.play(fade_through(VGroup(v_box.frame, v_num), vcm_live), run_time=0.8)
    internal = caption("the collision forces are internal", cfg.FORCE)
    scene.play(FadeIn(internal), clock.to(stage, 2.6, rate_func=linear), run_time=3.6)
    scene.play(Create(glow_frame(vcm_live, cfg.BALANCED)), run_time=0.8)
    finish(scene, t, stage)
