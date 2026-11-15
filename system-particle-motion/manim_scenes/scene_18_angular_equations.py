"""Scene 18 — rotation's equations of motion. A wheel turns on a small 3D
stage at the top. Two columns open: straight-line motion and rotation about
a fixed axis. Each linear symbol is paired with its angular
partner: x -> theta, v -> omega = d theta / dt, a -> alpha = d omega / dt,
t -> t. Then the three constant-acceleration equations are written on the
left and its rotational twin is revealed on the right; the
three angular equations end boxed in gold.
"""

from manim_scenes.common import *

LEFT_X, RIGHT_X = -3.6, 3.6


class Scene18AngularEquations(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "18", "Rotation's equations of motion")
    stage = Stage((0.0, 1.6, 0.0), zoom=0.9, yaw=-0.2, pitch=0.2, sway=0.02)
    spin = Knob(0.0)
    drive(stage, spin, 0.9)
    wheel(stage, ORIGIN, 1.2, lambda: spin.value, half_length=0.12, sectors=8)
    show(scene, stage, 1.0)
    predict = caption("predict the rotation itself", cfg.WHITE)
    scene.play(FadeIn(predict), run_time=0.7)

    # --- 2. Two columns -----------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    hide(scene, stage, 0.7, FadeOut(predict))
    heads = VGroup(txt("straight line", cfg.FONT["body"], cfg.VELOCITY).move_to([LEFT_X, 3.1, 0]),
                   txt("rotation about a fixed axis", cfg.FONT["body"], cfg.ANGLE).move_to([RIGHT_X, 3.1, 0]))
    rule = Line([0, 2.7, 0], [0, -3.6, 0], stroke_color=cfg.MUTED, stroke_width=2, stroke_opacity=0.5)
    scene.play(FadeIn(heads[0], shift=DOWN * 0.1), FadeIn(heads[1], shift=DOWN * 0.1), Create(rule), run_time=1.0)

    # --- 3. x -> theta, v -> omega, a -> alpha -----------------------------------------------------------------------------
    beat(scene, t, 2)
    pairs = [
        (eq("x", cfg.FONT["section"], cfg.POSITION), eq(r"\theta", cfg.FONT["section"], cfg.ANGLE), None),
        (eq("v", cfg.FONT["section"], cfg.VELOCITY), eq(r"\omega", cfg.FONT["section"], cfg.ANGLE),
         eq(r"= {d\theta \over dt}", cfg.FONT["body"], cfg.ANGLE)),
        (eq("a", cfg.FONT["section"], cfg.ACCEL), eq(r"\alpha", cfg.FONT["section"], cfg.ANGLE),
         eq(r"= {d\omega \over dt}", cfg.FONT["body"], cfg.ANGLE)),
        (eq("t", cfg.FONT["section"], cfg.WHITE), eq("t", cfg.FONT["section"], cfg.WHITE), None),
    ]
    ys = [1.9, 0.75, -0.45, -1.55]
    rows = VGroup()
    for (lin, ang, extra), y in zip(pairs, ys):
        lin.move_to([LEFT_X, y, 0])
        ang.move_to([RIGHT_X - 0.6, y, 0])
        if extra is not None:
            extra.next_to(ang, RIGHT, buff=0.2)
        rows.add(VGroup(lin, ang, *( [extra] if extra is not None else [])))
    for k in range(3):
        lin, ang = rows[k][0], rows[k][1]
        scene.play(FadeIn(lin, shift=RIGHT * 0.1), run_time=0.5)
        scene.play(FadeIn(ang, shift=RIGHT * 0.15), run_time=1.0)
        if len(rows[k]) > 2:
            scene.play(FadeIn(rows[k][2]), run_time=0.6)

    # --- 4. Time is time ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeIn(rows[3][0]), FadeIn(rows[3][1]), run_time=1.0)

    # --- 5. omega = omega_0 + alpha t ----------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    compact = eq(r"x\to\theta \qquad v\to\omega \qquad a\to\alpha \qquad t\to t", cfg.FONT["body"], cfg.ANGLE)
    compact.move_to([0, 3.1, 0])
    scene.play(FadeOut(rows), FadeOut(rule), fade_through(heads, compact), run_time=1.0)
    linear = VGroup(eq(r"v = v_0 + a t", cfg.FONT["section"], cfg.VELOCITY),
                    eq(r"x = x_0 + v_0 t + \tfrac12 a t^2", cfg.FONT["section"], cfg.VELOCITY),
                    eq(r"v^2 = v_0^2 + 2a(x - x_0)", cfg.FONT["section"], cfg.VELOCITY))
    angular = VGroup(eq(r"\omega = \omega_0 + \alpha t", cfg.FONT["section"], cfg.ANGLE),
                     eq(r"\theta = \theta_0 + \omega_0 t + \tfrac12 \alpha t^2", cfg.FONT["section"], cfg.ANGLE),
                     eq(r"\omega^2 = \omega_0^2 + 2\alpha(\theta - \theta_0)", cfg.FONT["section"], cfg.ANGLE))
    for group, x in ((linear, -3.9), (angular, 3.9)):
        for k, line in enumerate(group):
            fit_width(line, 7.0)
            line.move_to([x, 1.15 - 1.3 * k, 0])
    constant = txt("constant angular acceleration", cfg.FONT["small"], cfg.MUTED).move_to([0, 2.25, 0])
    scene.play(Write(linear[0]), FadeIn(constant), run_time=1.2)
    scene.play(FadeIn(angular[0], shift=RIGHT * 0.15), run_time=1.4)

    # --- 6. theta = theta_0 + omega_0 t + 1/2 alpha t^2 ---------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(Write(linear[1]), run_time=1.4)
    scene.play(FadeIn(angular[1], shift=RIGHT * 0.15), run_time=1.6)

    # --- 7. omega^2 = omega_0^2 + 2 alpha (theta - theta_0) ---------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(Write(linear[2]), run_time=1.4)
    scene.play(FadeIn(angular[2], shift=RIGHT * 0.15), run_time=1.6)

    # --- 8. Same structure, new symbols ----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    frame = glow_frame(angular, cfg.RESULT, buff=0.25)
    scene.play(Create(frame), linear.animate.set_opacity(0.5), run_time=1.0)
    same = caption("same structure, new symbols", cfg.RESULT)
    scene.play(FadeIn(same), run_time=0.7)
    finish(scene, t, fill=lambda sec: [Indicate(angular, color=cfg.WHITE, scale_factor=1.02)])
