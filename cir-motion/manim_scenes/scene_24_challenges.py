"""Scene 24 — five conceptual challenges, each with a 3-2-1 countdown and an
animated answer: (1) the string breaks: along the tangent; (2) constant
speed round a circle: still accelerating; (3) double the speed on the same
circle: four times the acceleration (arrows at true length from
``physics_models.DOUBLE_SPEED``); (4) a satellite in an ideal circular
orbit: accelerating toward Earth's centre; (5) alpha = 0 while
a_c = v^2 / r is not.
"""

from manim_scenes.common import *

C = np.array([-2.6, -0.6, 0])
R = 2.0
COUNT_AT = [5.2, 0.4, 0]


class Scene24Challenges(Scene):
    def construct(self) -> None:
        play_scene(self)


def ask(scene: Scene, number: int, latex: str) -> VGroup:
    tag = chip(f"{number}", cfg.GOLD, cfg.FONT["section"])
    words = eq(latex, cfg.FONT["body"], cfg.WHITE)
    fit_width(words, 11.6)
    line = VGroup(tag, words).arrange(RIGHT, buff=0.4).move_to(UP * 3.3)
    scene.play(FadeIn(line, shift=DOWN * 0.15), run_time=0.7)
    return line


def answer(scene: Scene, text: str, color: str = cfg.GREEN) -> VGroup:
    words = eq(text, cfg.FONT["body"], color)
    fit_width(words, 4.4)
    label = boxed(words, color, 0.2)
    label.move_to([5.2, -1.5, 0])
    scene.play(FadeIn(label, shift=UP * 0.15), run_time=0.7)
    return label


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "24")
    chapter_open(scene, 7, "Thought experiments and conclusion")
    five = txt("5 challenges", cfg.FONT["section"], cfg.GOLD)
    scene.play(FadeIn(five, scale=0.95), run_time=0.8)

    # --- Q1: the string breaks ----------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(FadeOut(five), run_time=0.4)
    q = ask(scene, 1, r"\text{The string breaks. Where does the ball go?}")
    # Released on the right side (theta = 0.3 rad at 0.6 T), so the tangent runs upward, clear of the captions.
    view = CircleView(C, R, P, kv=1.1 / P.v, phase=0.3 - 0.6 * P.period * P.angular_speed)
    string = live(VMobject(), lambda: Line(C, view.point(), stroke_color=cfg.WHITE, stroke_width=3))
    scene.play(FadeIn(view.ring), FadeIn(view.hub), FadeIn(view.ball), FadeIn(string), run_time=0.7)
    scene.play(view.run(P.period * 0.6, 3.0), run_time=3.0)
    here, out, along = view.point(), view.unit_r(), view.unit_t()
    options = VGroup(dashed_path(here, here + out * 1.6, cfg.WARNING, width=4, opacity=0.9),
                     DashedVMobject(Arc(radius=R, start_angle=view.theta(), angle=1.4, arc_center=C, stroke_color=cfg.MUTED,
                                        stroke_width=4), num_dashes=14),
                     dashed_path(here, here + along * 2.2, cfg.GOLD, width=4, opacity=0.9))
    letters = VGroup(chip("A", cfg.WARNING, cfg.FONT["small"]).move_to(here + out * 1.95),
                     chip("B", cfg.MUTED, cfg.FONT["small"]).move_to(view.at_angle(view.theta() + 1.55, 1.18)),
                     chip("C", cfg.GOLD, cfg.FONT["small"]).move_to(here + along * 2.5 + RIGHT * 0.45))
    scene.play(Create(options), FadeIn(letters), run_time=1.0)
    countdown(scene, COUNT_AT)

    beat(scene, t, 2)
    string.clear_updaters()
    fly = Knob(0.0)
    view.ball.clear_updaters()
    view.ball.add_updater(lambda m: m.move_to(here + along * fly.value))
    v = VecArrow(lambda: view.ball.get_center(), lambda: view.ball.get_center() + along * view.kv * P.v, cfg.VELOCITY, width=0.09)
    scene.add(v)
    scene.play(FadeOut(string), FadeOut(options), FadeOut(letters), v.grow_in(run_time=0.4), run_time=0.4)
    scene.play(fly.to(view.ball, 1.8, run_time=1.6, rate_func=linear), run_time=1.6)
    a1 = answer(scene, r"\text{C: tangent}")

    # --- Q2: constant speed -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    view.ball.clear_updaters()
    clear(scene, run_time=0.6)
    q = ask(scene, 2, r"|\vec v| = \text{constant on a circle.}\quad \vec a = 0\,?")
    view = CircleView(C, R, P, kv=1.1 / P.v, ka=1.3 / P.accel)
    v = view.arrow("v", width=0.09)
    scene.add(view.ring, view.hub, view.ball, v)
    scene.play(FadeIn(VGroup(view.ring, view.hub, view.ball)), v.grow_in(run_time=0.6), run_time=0.6)
    scene.play(view.run(1.0, 2.6), run_time=2.6)
    countdown(scene, COUNT_AT)

    beat(scene, t, 4)
    a = view.arrow("a", width=0.09)
    scene.add(a)
    scene.play(a.grow_in(run_time=0.6), view.run(view.clock.value + 0.3, 0.6), run_time=0.6)
    a2 = answer(scene, r"\vec a\ne 0")
    scene.play(view.run(view.clock.value + 1.2, 3.0), run_time=3.0)

    # --- Q3: double the speed -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    for m in (view.ball, v, a):
        m.clear_updaters()
    clear(scene, run_time=0.6)
    q = ask(scene, 3, r"\text{Same circle, speed doubled: } a_c \to\ ?")
    ka = 0.055
    slow = CircleView([-4.6, -0.6, 0], 1.7, P, kv=0.22, ka=ka)
    fast = CircleView([0.0, -0.6, 0], 1.7, pm.DOUBLE_SPEED, kv=0.22, ka=ka)
    parts = [slow.arrow("v", width=0.08), fast.arrow("v", width=0.08)]
    scene.add(slow.ring, slow.ball, fast.ring, fast.ball, *parts)
    tags = VGroup(eq("v", cfg.FONT["body"], cfg.VELOCITY).next_to(slow.ring, UP, buff=0.25),
                  eq("2v", cfg.FONT["body"], cfg.VELOCITY).next_to(fast.ring, UP, buff=0.25))
    scene.play(FadeIn(VGroup(slow.ring, slow.ball, fast.ring, fast.ball, tags)), *[p.grow_in(run_time=0.6) for p in parts], run_time=0.7)
    scene.play(run_together(slow.ball, [slow, fast], 0.8, 3.2), run_time=3.2)
    countdown(scene, COUNT_AT)

    beat(scene, t, 6)
    acc = [slow.arrow("a", width=0.08), fast.arrow("a", width=0.08)]
    scene.add(*acc)
    scene.play(*[p.grow_in(run_time=0.6) for p in acc], run_together(slow.ball, [slow, fast], 0.15, 0.6), run_time=0.6)
    a3 = answer(scene, r"a_c\to4a_c")
    scene.play(run_together(slow.ball, [slow, fast], 0.8, 3.2), run_time=3.2)

    # --- Q4: a satellite in a circular orbit ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    for m in (slow.ball, fast.ball, *parts, *acc):
        m.clear_updaters()
    clear(scene, run_time=0.6)
    q = ask(scene, 4, r"\text{A satellite, constant speed, circular orbit. Accelerating?}")
    earth = bead(C, cfg.EARTH, 0.9)
    orbit = CircleView(C, R, P, kv=1.0 / P.v, ka=1.1 / P.accel, ball_color=cfg.WHITE, ball_radius=0.12)
    v = orbit.arrow("v", width=0.08)
    scene.add(earth, orbit.ring, orbit.ball, v)
    scene.play(FadeIn(VGroup(earth, orbit.ring, orbit.ball)), v.grow_in(run_time=0.6), run_time=0.7)
    scene.play(orbit.run(1.0, 2.8), run_time=2.8)
    countdown(scene, COUNT_AT)

    beat(scene, t, 8)
    pull = orbit.arrow("a", cfg.FORCE, width=0.09)
    scene.add(pull)
    scene.play(pull.grow_in(run_time=0.6), orbit.run(orbit.clock.value + 0.2, 0.6), run_time=0.6)
    a4 = answer(scene, r"\text{Yes: inward}")
    scene.play(orbit.run(orbit.clock.value + 1.2, 3.4), run_time=3.4)

    # --- Q5: alpha = 0 with a != 0? ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    for m in (orbit.ball, v, pull):
        m.clear_updaters()
    clear(scene, run_time=0.6)
    q = ask(scene, 5, r"\alpha = 0 \quad\text{and}\quad a \neq 0\ \text{at the same time?}")
    view = CircleView([-0.6, -0.6, 0], R, P, kv=1.0 / P.v, ka=1.3 / P.accel)
    gauge = Speedometer([-5.0, -0.3, 0], top=4, radius=1.3, value=P.angular_speed, unit="rad/s", step=1)
    omega_tag = eq(r"\omega", cfg.FONT["body"], cfg.ANGLE).next_to(gauge, UP, buff=0.25)
    v = view.arrow("v", width=0.09)
    scene.add(view.ring, view.hub, view.ball, v)
    scene.play(FadeIn(VGroup(view.ring, view.hub, view.ball, gauge, omega_tag)), v.grow_in(run_time=0.6), run_time=0.7)
    scene.play(view.run(1.0, 2.6), run_time=2.6)
    countdown(scene, COUNT_AT)

    beat(scene, t, 10)
    a = view.arrow("a", width=0.09)
    scene.add(a)
    zero = eq(r"\alpha = 0", cfg.FONT["body"], cfg.ANGLE).next_to(gauge, DOWN, buff=0.35)
    scene.play(a.grow_in(run_time=0.6), FadeIn(zero), view.run(view.clock.value + 0.3, 0.7), run_time=0.7)
    a5 = answer(scene, r"\alpha=0,\quad a_c\ne0")
    scene.play(view.run(view.clock.value + 1.4, 4.0), run_time=4.0)

    # --- Close: replay and explain the arrows -------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    for m in (view.ball, v, a):
        m.clear_updaters()
    clear(scene, run_time=0.7)
    close = VGroup(txt("surprised?", cfg.FONT["section"], cfg.WHITE),
                   txt("replay it, and explain the arrows", cfg.FONT["title"], cfg.GOLD)).arrange(DOWN, buff=0.4)
    fit_width(close, 13.0)
    scene.play(FadeIn(close[0], shift=UP * 0.15), run_time=0.8)
    scene.play(FadeIn(close[1], scale=0.95), run_time=1.0)
    scene.wait(1.8)
    scene.play(Indicate(close[1], color=cfg.GOLD, scale_factor=1.04), run_time=1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["24"])
