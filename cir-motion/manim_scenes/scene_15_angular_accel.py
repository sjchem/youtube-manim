"""Scene 15 — angular acceleration. An omega gauge reads the reference
particle's 2 rad/s. alpha = d omega / dt; in uniform motion the needle never
moves, so alpha = 0 — yet the particle beside it carries an 8 m/s^2 orange
arrow toward the centre. Two cards separate the ideas (alpha tracks the
turning rate; a_c turns the velocity), and the needle finally starts to
climb: what happens when the particle speeds up is the next chapter.
"""

from manim_scenes.common import *

C = np.array([3.6, 0.15, 0])
R = 2.0


class Scene15AngularAccel(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "15", "Angular acceleration")
    gauge = Speedometer([-4.3, 0.35, 0], top=4, radius=1.6, value=P.angular_speed, unit="rad/s", step=1)
    title = eq(r"\omega", cfg.FONT["section"], cfg.ANGLE).next_to(gauge, UP, buff=0.3)
    scene.play(FadeIn(gauge), FadeIn(title), run_time=0.9)
    ask = txt("and if ω changes?", cfg.FONT["label"], cfg.ANGLE).move_to([3.4, 1.2, 0])
    scene.play(FadeIn(ask, shift=UP * 0.1), run_time=0.7)
    scene.play(gauge.value.to(gauge, 3.0, run_time=1.4, rate_func=there_and_back), run_time=1.4)

    # --- 2. alpha = d omega / dt -------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    alpha = paint(eq([r"\alpha", "=", r"\frac{d\omega}{dt}"], cfg.FONT["title"]), {0: cfg.ANGLE, 2: cfg.ANGLE}).move_to([3.4, 1.2, 0])
    unit = txt("rad/s²", cfg.FONT["label"], cfg.MUTED).next_to(alpha, DOWN, buff=0.35)
    scene.play(FadeOut(head), FadeOut(ask), run_time=0.4)
    scene.play(Write(alpha), run_time=1.0)
    scene.play(FadeIn(unit), run_time=0.6)

    # --- 3. Uniform: omega constant, alpha = 0 ---------------------------------------------------------------------------------------
    beat(scene, t, 2)
    zero = eq(r"\alpha = 0", cfg.FONT["section"], cfg.ANGLE).next_to(gauge, RIGHT, buff=0.5)
    scene.play(FadeOut(VGroup(alpha, unit)), FadeIn(zero, shift=UP * 0.1), run_time=0.9)
    scene.play(Indicate(gauge.needle, color=cfg.ANGLE, scale_factor=1.0), run_time=1.2)

    # --- 4. But a_c = 8 m/s^2 ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    view = CircleView(C, R, P, kv=1.0 / P.v, ka=1.3 / P.accel)
    a_arrow = view.arrow("a", width=0.09)
    scene.play(FadeIn(view.ring), FadeIn(view.hub), FadeIn(view.ball), run_time=0.6)
    scene.add(a_arrow)
    scene.play(a_arrow.grow_in(run_time=0.6), view.run(0.3, 0.6), run_time=0.6)
    ac = eq(rf"a_c = {AC}\ \mathrm{{m/s^2}}", cfg.FONT["section"], cfg.ACCEL).move_to([3.6, 2.9, 0])
    scene.play(FadeIn(ac, shift=DOWN * 0.1), view.run(view.clock.value + 0.4, 0.8), run_time=0.8)
    scene.play(view.run(view.clock.value + 2.4, 7.0), run_time=7.0)

    # --- 5. Different changes ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    cards = VGroup(on_panel(VGroup(eq(r"\alpha", cfg.FONT["section"], cfg.ANGLE),
                                   txt("turning rate", cfg.FONT["small"], cfg.WHITE)).arrange(RIGHT, buff=0.25), cfg.ANGLE, 0.25),
                   on_panel(VGroup(eq(r"a_c", cfg.FONT["section"], cfg.ACCEL),
                                   txt("velocity direction", cfg.FONT["small"], cfg.WHITE)).arrange(RIGHT, buff=0.25), cfg.ACCEL, 0.25))
    cards.arrange(RIGHT, buff=0.7).move_to([0, -2.8, 0])
    scene.play(FadeOut(zero), FadeIn(cards[0], shift=UP * 0.1), view.run(view.clock.value + 0.5, 1.0), run_time=1.0)
    scene.play(FadeIn(cards[1], shift=UP * 0.1), view.run(view.clock.value + 0.5, 1.0), run_time=1.0)
    scene.play(view.run(view.clock.value + 2.8, 8.5), run_time=8.5)

    # --- 6. When the particle speeds up ... ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    soon = txt("next: speeding up", cfg.FONT["label"], cfg.TANGENTIAL).move_to([3.6, 2.9, 0])
    scene.play(fade_through(ac, soon), a_arrow.fade_to(0.0, run_time=0.8),
               view.run(view.clock.value + 0.3, 0.8), run_time=0.8)
    # Hand the particle to the model's speeding-up motion at the same spot; the needle now reads it.
    ramp = pm.SpeedingUp(P.r, P.angular_speed, pm.ALPHA)
    faster = CircleView(C, R, ramp, phase=view.theta())
    view.ball.clear_updaters()
    a_arrow.clear_updaters()
    scene.remove(view.ball, a_arrow)
    scene.add(faster.ball)
    # omega(t) = omega0 + alpha t is linear in time, so a linear needle tween stays exactly in step.
    scene.play(faster.run(2.0, 5.5), gauge.value.to(gauge, ramp.omega(2.0), run_time=5.5, rate_func=linear), run_time=5.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["15"])
