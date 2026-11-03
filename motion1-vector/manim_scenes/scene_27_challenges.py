"""Scene 27 — five conceptual challenges, each with a 3-2-1 countdown and an
animated answer: (1) the top of the flight; (2) a dropped ball and a ball
launched sideways from the same height land together (19.6 m: a 2.00 s
fall, strobed every 0.25 s); (3) 30 and 60 degrees share a range;
(4) constant speed round a circle is acceleration; (5) doubling the launch
speed quadruples the range (``physics_models.DOUBLED``).
"""

from manim_scenes.common import *

DROP_H = pm.DROP_HEIGHT
SIDE_V = pm.SIDE_SPEED
FALL_T = pm.fall_time(DROP_H)


class Scene27Challenges(Scene):
    def construct(self) -> None:
        play_scene(self)


def ask(scene: Scene, number: int, text: str) -> VGroup:
    tag = chip(f"{number}", cfg.GOLD, cfg.FONT["section"])
    words = txt(text, cfg.FONT["label"], cfg.WHITE)
    fit_width(words, 12.4)
    line = VGroup(tag, words).arrange(RIGHT, buff=0.4).move_to(UP * 3.3)
    scene.play(FadeIn(line, shift=DOWN * 0.15), run_time=0.7)
    return line


def answer(scene: Scene, text: str, color: str = cfg.GREEN) -> VGroup:
    label = result_label(text, color, cfg.FONT["label"])
    fit_width(label, 13.4)
    label.move_to(DOWN * 3.55)
    scene.play(FadeIn(label, shift=UP * 0.15), run_time=0.7)
    return label


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "27")
    opener = txt("Conceptual challenges", cfg.FONT["title"], cfg.WHITE)
    fit_width(opener, 12.4)
    opener.move_to(ORIGIN)
    scene.play(FadeIn(opener, shift=LEFT * 0.3), run_time=0.9)
    scene.wait(1.0)
    scene.play(FadeOut(opener, shift=UP * 0.3), run_time=0.6)
    five = txt('5 challenges', cfg.FONT["section"], cfg.GOLD)
    scene.play(FadeIn(five, scale=0.95), run_time=0.8)

    # --- Q1: the top of the flight -------------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(FadeOut(five), run_time=0.4)
    q = ask(scene, 1, 'vᵧ = ?     aᵧ = ?')
    grid = plane((0, 45), (0, 12), unit=0.2, at=(-4.6, -2.6, 0), step=5, labels=False, faint=0.25)
    flight = SideFlight(grid, k=0.07)
    scene.add(grid, flight.trail, flight.ball)
    scene.play(FadeIn(grid), flight.fly(P.apex_time, speed=0.9), run_time=P.apex_time / 0.9)
    countdown(scene, [5.0, 0.0, 0])

    beat(scene, t, 2)
    vx = flight.arrow("vx", cfg.X_COLOR, width=0.09)
    g = flight.arrow("a", cfg.ACCEL, width=0.09)
    scene.add(vx, g)
    scene.play(vx.grow_in(run_time=0.6), g.grow_in(run_time=0.6), run_time=0.6)
    tags = VGroup(eq(r"v_y = 0", cfg.FONT["body"], cfg.Y_COLOR).next_to(flight.point(P.apex_time), UP, buff=0.4),
                  eq(rf"a = g\ \downarrow", cfg.FONT["body"], cfg.ACCEL).next_to(flight.point(P.apex_time), DOWN, buff=1.5))
    scene.play(FadeIn(tags), run_time=0.6)
    a1 = answer(scene, 'vᵧ = 0     aᵧ = −g')

    # --- Q2: dropped vs launched sideways ------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    clear(scene)
    q = ask(scene, 2, 'v₀ᵧ = 0     h₁ = h₂     t₁ ? t₂')
    s = 0.17
    top = np.array([-4.2, -3.1 + DROP_H * s, 0])
    ground_y = -3.1
    ledge = Rectangle(width=2.4, height=DROP_H * s, stroke_color=cfg.MUTED, stroke_width=2, fill_color="#2A4D6B", fill_opacity=1)
    ledge.next_to(top + DOWN * 0.15, DOWN, buff=0).align_to(top, RIGHT)
    floor = Line([-7.5, ground_y, 0], [7.5, ground_y, 0], stroke_color=cfg.MUTED, stroke_width=3)
    clock = Knob(0.0)
    fall = lambda tt: 0.5 * pm.G * tt * tt  # noqa: E731
    drop = bead(top + UP * 0.18, cfg.CYAN, 0.18)
    side = bead(top + UP * 0.18, cfg.BALL, 0.18)
    drop.add_updater(lambda m: m.move_to(top + UP * 0.18 + LEFT * 0.35 + DOWN * min(fall(clock.value), DROP_H) * s))
    side.add_updater(lambda m: m.move_to(top + UP * 0.18 + RIGHT * 0.35 + RIGHT * SIDE_V * clock.value * s
                                         + DOWN * min(fall(clock.value), DROP_H) * s))
    scene.play(FadeIn(ledge), FadeIn(floor), FadeIn(drop), FadeIn(side), run_time=0.8)
    countdown(scene, [4.6, 0.6, 0])

    beat(scene, t, 4)
    strobe = VGroup()
    rungs = VGroup()
    for k in range(1, int(round(FALL_T / 0.25)) + 1):
        tt = k * 0.25
        y = top[1] + 0.18 - fall(tt) * s
        strobe.add(bead([top[0] - 0.35, y, 0], cfg.CYAN, 0.12).set_opacity(0.4),
                   bead([top[0] + 0.35 + SIDE_V * tt * s, y, 0], cfg.BALL, 0.12).set_opacity(0.4))
        rungs.add(DashedLine([top[0] - 0.35, y, 0], [top[0] + 0.35 + SIDE_V * tt * s, y, 0], stroke_color=cfg.MUTED,
                             stroke_width=2, stroke_opacity=0.5))
    scene.play(clock.to(drop, FALL_T, run_time=2.4, rate_func=linear), run_time=2.4)
    scene.play(FadeIn(strobe), Create(rungs), run_time=1.0)
    a2 = answer(scene, 't₁ = t₂')
    same_t = eq(rf"t = \sqrt{{2h/g}} = {md.fixed(FALL_T, 2)}\ \mathrm{{s}}", cfg.FONT["body"], cfg.WHITE).move_to([3.6, 1.2, 0])
    scene.play(FadeIn(same_t), run_time=0.7)

    # --- Q3: 30 vs 60 degrees -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    for m in (drop, side):
        m.clear_updaters()
    clear(scene)
    q = ask(scene, 3, '30° · 60°     R₃₀ ? R₆₀')
    grid = plane((0, 40), (0, 17), unit=0.24, at=(-4.8, -3.0, 0), step=5, labels=False, faint=0.25)
    pair = [SideFlight(grid, pm.TABLE[0], k=0.06, color=cfg.CYAN, trail_color=cfg.CYAN),
            SideFlight(grid, pm.TABLE[2], k=0.06, color=cfg.PURPLE, trail_color=cfg.PURPLE)]
    scene.add(grid, *[f.trail for f in pair], *[f.ball for f in pair])
    scene.play(FadeIn(grid), run_time=0.6)
    countdown(scene, [5.6, 1.0, 0])

    beat(scene, t, 6)
    scene.play(fly_together(pair, run_time=2.6), run_time=2.6)
    mark = glow_dot(grid.c2p(pm.TABLE[0].range, 0), cfg.GREEN, 0.12, reach=4)
    scene.play(FadeIn(mark, scale=1.5), run_time=0.6)
    a3 = answer(scene, f"R₃₀ = R₆₀ ≈ {md.fixed(pm.TABLE[0].range, 2)} m")

    # --- Q4: constant speed, changing direction --------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    clear(scene)
    q = ask(scene, 4, '|v| = constant     a = ?')
    centre = np.array([0, -0.4, 0])
    ring = Circle(radius=2.0, stroke_color=cfg.MUTED, stroke_width=3, stroke_opacity=0.6).move_to(centre)
    spin = Knob(0.0)
    where = lambda: centre + 2.0 * np.array([np.cos(spin.value), np.sin(spin.value), 0])  # noqa: E731
    dot = bead(where(), cfg.BALL, 0.18)
    dot.add_updater(lambda m: m.move_to(where()))
    v = VecArrow(where, lambda: where() + 1.4 * np.array([-np.sin(spin.value), np.cos(spin.value), 0]), cfg.VELOCITY, width=0.1)
    scene.add(ring, dot, v)
    scene.play(FadeIn(ring), FadeIn(dot), v.grow_in(run_time=0.6), run_time=0.6)
    scene.play(spin.to(dot, PI / 2, run_time=1.4, rate_func=linear))
    countdown(scene, [5.4, 0.0, 0])

    beat(scene, t, 8)
    a_arrow = VecArrow(where, lambda: where() + (centre - where()) * 0.45, cfg.ACCEL, width=0.1)
    scene.add(a_arrow)
    scene.play(a_arrow.grow_in(run_time=0.6), run_time=0.6)
    scene.play(spin.to(dot, 2.5 * PI, run_time=3.6, rate_func=linear))
    a4 = answer(scene, 'a ≠ 0')

    # --- Q5: double the launch speed --------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    for m in (dot,):
        m.clear_updaters()
    clear(scene)
    q = ask(scene, 5, 'v₀ → 2v₀     R → ?')
    grid = plane((0, 170), (0, 45), unit=0.08, at=(-6.8, -3.0, 0), step=10, labels=False, faint=0.2)
    slow = SideFlight(grid, P, k=0.03)
    fast = SideFlight(grid, pm.DOUBLED, k=0.03, color=cfg.GREEN, trail_color=cfg.GREEN)
    scene.add(grid, slow.trail, slow.ball, fast.trail, fast.ball)
    scene.play(FadeIn(grid), slow.fly(run_time=1.6), run_time=1.6)
    countdown(scene, [5.6, 1.6, 0])

    beat(scene, t, 10)
    scene.play(fast.fly(run_time=3.0), run_time=3.0)
    marks = VGroup(eq(rf"{RANGE}\ \mathrm{{m}}", cfg.FONT["small"], cfg.GOLD).next_to(grid.c2p(P.range, 0), UP, buff=0.25),
                   eq(rf"{md.fixed(pm.DOUBLED.range, 2)}\ \mathrm{{m}}", cfg.FONT["small"], cfg.GREEN).next_to(grid.c2p(pm.DOUBLED.range, 0), UP, buff=0.25))
    four = eq([r"R \propto v_0^2", r"\ \Rightarrow\ ", r"\times 4"], cfg.FONT["section"], cfg.GREEN).move_to([1.8, 1.2, 0])
    scene.play(FadeIn(marks), Write(four), run_time=1.2)
    a5 = answer(scene, 'R → 4R')

    # --- Close: you understand motion in two dimensions ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    clear(scene)
    done = VGroup(txt('Vectors', cfg.FONT["section"], cfg.WHITE),
                  txt('Motion in 2D', cfg.FONT["title"], cfg.GOLD)).arrange(DOWN, buff=0.4)
    scene.play(FadeIn(done[0], shift=UP * 0.15), run_time=0.8)
    scene.play(FadeIn(done[1], scale=0.95), run_time=1.0)
    scene.wait(2.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["27"])
