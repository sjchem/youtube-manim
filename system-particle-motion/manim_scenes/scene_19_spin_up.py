"""Scene 19 — a wheel spins up. A 3D wheel with a gold rim bead starts from
rest with the model's constant angular acceleration (2 rad/s^2). For four
real seconds it spins up while live readouts show t, omega, theta and the
revolution count. A labelled four-second snapshot and gentle camera turns accompany the
worked steps: omega = 0 + 2 x 4 = 8 rad/s; theta = 1/2 x 2 x 4^2 = 16 rad;
N = 16 / 2 pi = 2.55 revolutions, which the counter confirms.
"""

from manim_scenes.common import *

W = pm.WHEEL


class Scene19SpinUp(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "19", "A wheel spins up")
    clock = Knob(0.0)
    stage = Stage((-3.6, -0.5, 0.0), zoom=1.45, yaw=-0.3, pitch=0.12, sway=0.02)
    w = wheel(stage, ORIGIN, 1.9, lambda: W.theta_at(clock.value), half_length=0.16, sectors=8)
    marker = rim_marker(stage, w.drum, np.pi / 2, cfg.GOLD, fraction=0.92, radius=0.14)
    stand = Block(np.array([0.0, -1.35, -0.3]), (0.3, 2.7, 0.2), "#3A4A58")
    stage.add_body(stand)
    show(scene, stage, 1.0)
    given = VGroup(eq(r"\omega_0 = 0", cfg.FONT["section"], cfg.ANGLE),
                   eq(rf"\alpha = {fx(W.alpha)}\ \mathrm{{rad/s^2}}", cfg.FONT["section"], cfg.ANGLE)).arrange(DOWN, buff=0.3,
                                                                                                             aligned_edge=LEFT)
    given.move_to([3.4, 2.4, 0])
    scene.play(FadeIn(given[0], shift=LEFT * 0.1), run_time=0.7)
    scene.play(FadeIn(given[1], shift=LEFT * 0.1), run_time=0.8)

    # --- 2. Two questions --------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    qs = VGroup(eq(rf"\omega\ \text{{after}}\ {fx(W.duration)}\ \mathrm{{s}}?", cfg.FONT["body"], cfg.WHITE),
                eq(r"\Delta\theta\ ?", cfg.FONT["body"], cfg.WHITE)).arrange(RIGHT, buff=0.8).move_to([3.4, 0.9, 0])
    scene.play(FadeIn(qs, shift=UP * 0.1, lag_ratio=0.3), run_time=1.0)

    # --- 3. Four live seconds ---------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    reads = VGroup(readout("t =", lambda: clock.value, 2, "s", cfg.WHITE, size=44),
                   readout(r"\omega =", lambda: W.omega_at(clock.value), 2, "rad/s", cfg.ANGLE, size=44),
                   readout(r"\theta =", lambda: W.theta_at(clock.value), 2, "rad", cfg.ANGLE, size=44),
                   readout("N =", lambda: W.theta_at(clock.value) / (2 * np.pi), 2, "rev", cfg.GOLD, size=44))
    reads.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.0, -1.6, 0])
    scene.play(FadeOut(qs), FadeIn(reads), run_time=0.6)
    scene.play(clock.to(stage, W.duration, rate_func=linear), run_time=W.duration)

    # --- 4. omega = 8 rad/s ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    s1 = eq(rf"\omega = \alpha t = {fx(W.omega)}\ \mathrm{{rad/s}}", cfg.FONT["section"], cfg.RESULT)
    scene.play(FadeOut(given), FadeOut(reads[:3]), reads[3].animate.move_to([3.4, -3.4, 0]), run_time=0.8)
    s1.move_to([3.2, 2.6, 0])
    fit_width(s1, 8.2)
    snapshot = chip(f"at {fx(W.duration)} s", cfg.MUTED, cfg.FONT["tiny"]).move_to([-3.6, 3.0, 0])
    scene.play(Write(s1), FadeIn(snapshot), *stage.turn(yaw=-0.2), run_time=1.6)

    # --- 5. theta = 16 rad ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    s2 = eq(rf"\Delta\theta = \tfrac12\alpha t^2 = {fx(W.angle)}\ \mathrm{{rad}}",
            cfg.FONT["section"], cfg.RESULT)
    fit_width(s2, 8.2)
    s2.move_to([3.2, 1.2, 0])
    scene.play(Write(s2), *stage.turn(yaw=-0.1), run_time=1.8)

    # --- 6. 16 / 2 pi = 2.55 revolutions -------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    s3 = eq(rf"N = {{{fx(W.angle)} \over 2\pi}} \approx {fx(W.revolutions, 2)}\ \text{{rev}}", cfg.FONT["section"], cfg.GOLD)
    s3.move_to([3.2, -0.6, 0])
    one_rev = eq(r"1\ \text{rev} = 2\pi\ \text{rad}", cfg.FONT["body"], cfg.MUTED).next_to(s3, DOWN, buff=0.35)
    scene.play(FadeIn(one_rev), run_time=0.8)
    scene.play(Write(s3), *stage.turn(yaw=-0.25), run_time=1.6)

    # --- 7. The counter agrees ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(Create(glow_frame(reads[3], cfg.BALANCED)), Indicate(s3, color=cfg.WHITE, scale_factor=1.03), run_time=1.2)
    finish(scene, t, stage)
