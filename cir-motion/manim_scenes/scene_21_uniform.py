"""Scene 21 — uniform circular motion, summarised on the reference particle:
constant speed, constant |omega|, alpha = 0, and an acceleration that is
entirely radial (v^2 / r inward) with no tangential part. Live readouts
show the speed and omega holding still while the arrows turn.
"""

from manim_scenes.common import *

C = np.array([-3.6, -0.55, 0])
R = 2.3
COL = 3.5
SLOW = 0.4


class Scene21Uniform(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "21")
    chapter_open(scene, 6, "Uniform vs nonuniform circular motion")
    head = heading("Uniform circular motion")
    view = CircleView(C, R, P, kv=1.1 / P.v, ka=1.35 / P.accel)
    v_arrow, a_arrow = view.arrow("v", width=0.09), view.arrow("a", width=0.09)
    scene.play(FadeIn(head, shift=DOWN * 0.18), FadeIn(view.ring), FadeIn(view.hub), FadeIn(view.ball), run_time=0.8)
    scene.add(v_arrow, a_arrow)
    scene.play(v_arrow.grow_in(run_time=0.6), a_arrow.grow_in(run_time=0.6), run_time=0.6)
    scene.play(view.run(2.0, 2.0 / SLOW * 0.5), run_time=2.0 / SLOW * 0.5)

    # --- 2. Speed constant, |omega| constant, alpha = 0 ----------------------------------------------------------------
    beat(scene, t, 1)
    facts = VGroup(number_line(lambda: float(np.linalg.norm(view.vel())), 2, "m/s", cfg.VELOCITY, 54, "v"),
                   number_line(lambda: abs(view.omega()), 2, "rad/s", cfg.ANGLE, 54, "|ω|"),
                   eq(r"\alpha = 0", cfg.FONT["body"], cfg.ANGLE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    facts.move_to([COL, 1.9, 0])
    scene.play(FadeOut(head), FadeIn(facts[0]), view.run(view.clock.value + 0.3, 0.8), run_time=0.8)
    scene.play(FadeIn(facts[1]), view.run(view.clock.value + 0.3, 0.8), run_time=0.8)
    scene.play(FadeIn(facts[2]), view.run(view.clock.value + 0.3, 0.8), run_time=0.8)
    scene.play(view.run(view.clock.value + 1.8, 1.8 / SLOW * 0.6), run_time=1.8 / SLOW * 0.6)

    # --- 3. Entirely radial: v^2 / r inward, no tangential part --------------------------------------------------------------------
    beat(scene, t, 2)
    radial = VGroup(eq(r"a_r = \frac{v^2}{r}\ \text{(inward)}", cfg.FONT["body"], cfg.ACCEL),
                    eq(r"a_t = 0", cfg.FONT["body"], cfg.TANGENTIAL)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    radial.next_to(facts, DOWN, buff=0.6).align_to(facts, LEFT)
    scene.play(Write(radial[0]), view.run(view.clock.value + 0.5, 1.4), run_time=1.4)
    scene.play(FadeIn(radial[1]), view.run(view.clock.value + 0.3, 0.8), run_time=0.8)
    scene.play(view.run(view.clock.value + 2.2, 2.2 / SLOW * 0.6), run_time=2.2 / SLOW * 0.6)

    # --- 4. Redirects v, keeps |v|. What if it speeds up? -----------------------------------------------------------------------------------
    beat(scene, t, 3)
    for m in facts[:2]:
        m.clear_updaters()
    ask = chip("what if it speeds up?", cfg.TANGENTIAL).move_to([COL, -2.65, 0])
    scene.play(FadeIn(ask, shift=UP * 0.1), view.run(view.clock.value + 0.4, 1.0), run_time=1.0)
    scene.play(view.run(view.clock.value + 2.4, 6.0), run_time=6.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["21"])
