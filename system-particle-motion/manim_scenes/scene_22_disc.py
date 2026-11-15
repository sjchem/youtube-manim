"""Scene 22 — spinning up a disc. A uniform solid disc (4 kg, 0.5 m) sits on
a frictionless axle on a 3D stand. I = 1/2 M R^2 = 0.5 kg m^2 is worked out.
A string wound on the rim pulls with a steady 2 N (green), a net torque of
1 N m (purple). alpha = tau / I = 2 rad/s^2, the same as the spinning wheel:
the disc then spins up live for four seconds and its readouts land on
8 rad/s and 16 rad.
"""

from manim_scenes.common import *

D = pm.DISC
W = pm.WHEEL
S = 3.6                         # screen units per metre: R = 0.5 m -> 1.8


class Scene22Disc(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "22", "Spinning up a disc")
    clock = Knob(0.0)
    stage = Stage((-3.4, 0.05, 0.0), zoom=1.2, yaw=-0.35, pitch=0.15, sway=0.02)
    R = D.radius * S
    w = wheel(stage, ORIGIN, R, lambda: -0.5 * D.alpha * min(clock.value, W.duration) ** 2, half_length=0.22, sectors=8)
    rim_marker(stage, w.drum, np.pi / 2, cfg.GOLD, fraction=0.9, radius=0.12)
    axle = Drum(np.array([0, 0, -0.45]), 0.08, 0.35, cfg.STEEL, axis=(0, 0, 1), sectors=2)
    post = Block(np.array([0.0, -1.5, -0.8]), (0.35, 3.0, 0.25), "#3A4A58")
    base = Block(np.array([0.0, -3.05, -0.4]), (2.4, 0.18, 1.6), "#2C3A47")
    stage.add_body(base, post, axle)
    show(scene, stage, 1.0)
    given = VGroup(eq(rf"M = {fx(D.mass)}\ \mathrm{{kg}}", cfg.FONT["section"], cfg.MASS),
                   eq(rf"R = {fx(D.radius, 1)}\ \mathrm{{m}}", cfg.FONT["section"], cfg.POSITION)).arrange(RIGHT, buff=0.8)
    given.move_to([3.9, 3.05, 0])
    R_seg = Segment(np.array([0, 0, 0.25]), np.array([R, 0, 0.25]), cfg.POSITION, width=5, opacity=1.0)
    R_seg.bias = 5.0
    R_seg.presence = 0.0
    stage.add_body(R_seg)
    frictionless = caption("frictionless central axle", cfg.MUTED)
    scene.play(FadeIn(given, lag_ratio=0.3), stage.fade(R_seg, 1.0), FadeIn(frictionless), run_time=1.4)

    # --- 2. I = 1/2 M R^2 = 0.5 --------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    I_steps = VGroup(eq(r"I = \tfrac12 M R^2", cfg.FONT["body"], cfg.INERTIA),
                     eq(rf"= {fx(D.inertia, 1)}\ \mathrm{{kg\,m^2}}", cfg.FONT["body"], cfg.INERTIA))
    I_steps.arrange(DOWN, buff=0.16).move_to([4.6, 1.55, 0])
    scene.play(FadeOut(frictionless), Write(I_steps), run_time=2.4)

    # --- 3. A string pulls 2 N: torque 1 N m ----------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    top = np.array([0.0, R, 0.0])
    string = Segment(top, top + np.array([2.6, 0, 0]), cfg.WHITE, width=3, opacity=0.9)
    string.bias = 6.0
    pull = Vector(top + np.array([2.6, 0, 0]), top + np.array([2.6 + D.string_force * 0.6, 0, 0]), cfg.FORCE, width=0.1,
                  tip=0.3)
    pull_lab = Tag(txt(f"{fx(D.string_force)} N", cfg.FONT["label"], cfg.FORCE), top + np.array([2.6 + D.string_force * 0.3, 0, 0]),
                   DOWN * 0.45)
    hidden(string, pull, pull_lab)
    stage.add_body(string)
    stage.add_overlay(pull, pull_lab)
    scene.play(stage.fade(string, 1.0), stage.fade(pull, 1.0), stage.fade(pull_lab, 1.0), run_time=1.0)
    tau_steps = eq(rf"\tau = F R = {fx(D.torque)}\ \mathrm{{N\,m}}",
                   cfg.FONT["section"], cfg.TORQUE)
    fit_width(tau_steps, 5.4)
    tau_steps.move_to([4.6, 0.15, 0])
    scene.play(Write(tau_steps), run_time=1.8)
    curl = turn_arrow(stage.screen_point(ORIGIN), R * 1.3 * 1.3, np.radians(60), np.radians(-90), cfg.TORQUE, width=7)
    scene.play(FadeIn(curl), run_time=0.6)

    # --- 4. alpha = 2 ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    alpha = eq(rf"\alpha = {{\tau \over I}} = {{{fx(D.torque)} \over {fx(D.inertia, 1)}}} = {fx(D.alpha)}\ \mathrm{{rad/s^2}}",
               cfg.FONT["section"], cfg.ANGLE)
    fit_width(alpha, 5.2)
    alpha_box = boxed(alpha, cfg.RESULT).move_to([4.6, -1.05, 0])
    scene.play(Write(alpha), run_time=1.6)
    scene.play(Create(alpha_box.frame), run_time=0.6)

    # --- 5. Same alpha as the wheel: spin it up -----------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    same = txt("the same α as our spinning wheel", cfg.FONT["small"], cfg.ANGLE)
    fit_width(same, 5.0)
    same.next_to(alpha_box, DOWN, buff=0.25)
    reads = VGroup(readout("t =", lambda: min(clock.value, W.duration), 1, "s", cfg.WHITE, size=44),
                   readout(r"\omega =", lambda: D.alpha * min(clock.value, W.duration), 1, "rad/s", cfg.ANGLE, size=44),
                   readout(r"\theta =", lambda: 0.5 * D.alpha * min(clock.value, W.duration) ** 2, 1, "rad", cfg.ANGLE, size=44))
    reads.arrange(RIGHT, buff=0.6).move_to([2.6, -3.35, 0])
    fit_width(reads, 9.8)
    scene.play(FadeIn(same), FadeIn(reads), FadeOut(curl), run_time=0.8)
    scene.play(clock.to(stage, W.duration, rate_func=linear), run_time=W.duration)
    lines = VGroup(txt("dynamics gives α", cfg.FONT["body"], cfg.TORQUE),
                   txt("kinematics does the rest", cfg.FONT["body"], cfg.ANGLE)).arrange(DOWN, buff=0.15)
    lines.move_to([3.6, 2.6, 0])
    scene.play(FadeOut(VGroup(given, I_steps)), stage.fade(string, 0.0), stage.fade(pull, 0.0),
               stage.fade(pull_lab, 0.0), run_time=0.5)
    scene.play(FadeIn(lines), run_time=0.5)
    scene.play(Create(glow_frame(reads, cfg.BALANCED)), run_time=0.8)
    finish(scene, t, stage)
