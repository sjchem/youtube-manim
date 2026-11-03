"""Scene 16 — acceleration is any change in velocity. After the
definitions (delta v / delta t, dv/dt, d2r/dt2), four cars in four panels:
speeding up (a along v), braking (a against v), turning at constant speed
(a sideways, inward) and turning while speeding up (a partly forward, partly
inward). In every panel the orange arrow is the direction of delta v.
"""

from manim_scenes.common import *

PANELS = [np.array([-3.9, 0.45, 0]), np.array([3.9, 0.45, 0]), np.array([-3.9, -2.55, 0]), np.array([3.9, -2.55, 0])]
TURN_RADIUS = 0.9
TURN_OFFSET = np.array([1.55, 0.0, 0])
VELOCITY_SCALE = 0.24


class Scene16Acceleration(Scene):
    def construct(self) -> None:
        play_scene(self)


def straight(centre, s: float):
    return centre + np.array([-2.55 + 0.5 * s, -0.55, 0]), 0.0


def turning(centre, s: float):
    c = centre + TURN_OFFSET
    a = -PI / 2 + s / TURN_RADIUS
    return c + TURN_RADIUS * np.array([np.cos(a), np.sin(a), 0]), a + PI / 2


class Panel:
    """One car in one box, with live velocity (gold) and acceleration (orange) arrows."""

    def __init__(self, centre, title: str, kind: str) -> None:
        self.centre, self.kind = centre, kind
        self.s = Knob(0.0)
        self.box = panel(7.2, 2.75, cfg.MUTED, 0.55).move_to(centre)
        self.title = txt(title, cfg.FONT["small"], cfg.WHITE)
        self.title.align_to(self.box, LEFT).shift(RIGHT * 0.35)
        self.title.align_to(self.box, UP).shift(DOWN * 0.25)
        if kind in ("speed up", "brake"):
            track = Line(centre + np.array([-3.2, -0.55, 0]), centre + np.array([3.2, -0.55, 0]), stroke_color=cfg.GRAY,
                         stroke_width=26, stroke_opacity=0.35)
        else:
            track = Circle(radius=TURN_RADIUS, stroke_color=cfg.GRAY, stroke_width=24, stroke_opacity=0.35).move_to(centre + TURN_OFFSET)
        self.track = track
        self.car = Car(cfg.CYAN, 0.66)
        self.car.set_pose(*self.pose())
        self.car.add_updater(lambda m: m.set_pose(*self.pose()))
        self.v = VecArrow(lambda: self.pose()[0], lambda: self.pose()[0] + self.heading() * self.speed() * VELOCITY_SCALE, cfg.VELOCITY,
                          width=0.08, tip_len=0.22)
        self.a = VecArrow(lambda: self.pose()[0], lambda: self.pose()[0] + self.accel(), cfg.ACCEL, width=0.08, tip_len=0.22)
        self.group = VGroup(self.box, self.title, track, self.car, self.v, self.a)

    def pose(self):
        f = straight if self.kind in ("speed up", "brake") else turning
        return f(self.centre, self.s.value)

    def heading(self) -> np.ndarray:
        h = self.pose()[1]
        return np.array([np.cos(h), np.sin(h), 0])

    def speed(self) -> float:
        s = self.s.value
        return {"speed up": 1.0 + 0.9 * s, "brake": max(4.0 - 0.75 * s, 0.6), "turn": 2.6,
                "turn faster": 1.2 + 0.32 * s}[self.kind] * 0.9

    def accel(self) -> np.ndarray:
        fwd = self.heading()
        inward = self.centre + TURN_OFFSET - self.pose()[0]
        inward = inward / max(np.linalg.norm(inward), 1e-6)
        return {"speed up": fwd * 0.95, "brake": -fwd * 0.95, "turn": inward * 0.95,
                "turn faster": (fwd * 0.6 + inward * 0.75)}[self.kind]

    def drive(self, end: float, run_time: float) -> Param:
        return self.s.to(self.car, end, run_time=run_time, rate_func=linear)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "16", "Acceleration")
    picture = txt("speeding up?", cfg.FONT["title"], cfg.WHITE).move_to(UP * 2.1)
    scene.play(FadeIn(picture, shift=UP * 0.15), run_time=1.0)

    # --- 2. Acceleration: the rate velocity changes ------------------------------------------------------------------------
    beat(scene, t, 1)
    rate = txt('Δv / Δt', cfg.FONT["section"], cfg.ACCEL).move_to(UP * 2.1)
    cross = strike(picture)
    scene.play(Create(cross), run_time=0.6)
    scene.play(fade_through(VGroup(picture, cross), rate), run_time=0.9)

    # --- 3. delta v / delta t, dv/dt ----------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    defs = VGroup(paint(eq([r"\vec{a}_{\text{avg}}", "=", r"\frac{\Delta\vec{v}}{\Delta t}"], cfg.FONT["section"]), {0: cfg.ACCEL}),
                  paint(eq([r"\vec{a}", "=", r"\frac{d\vec{v}}{dt}"], cfg.FONT["section"]), {0: cfg.ACCEL})).arrange(RIGHT, buff=1.2)
    defs.next_to(rate, DOWN, buff=0.7)
    scene.play(Write(defs[0]), run_time=1.3)
    scene.play(Write(defs[1]), run_time=1.3)

    # --- 4. The second derivative of position -----------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    second = paint(eq([r"\vec{a}", "=", r"\frac{d^2\vec{r}}{dt^2}"], cfg.FONT["title"]), {0: cfg.ACCEL, 2: cfg.POSITION})
    second.next_to(defs, DOWN, buff=0.6)
    scene.play(Write(second), run_time=1.6)

    # --- 5. Four cars -------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    clear(scene, head)
    panels = [Panel(c, title, kind) for c, title, kind in zip(PANELS, ("speeds up", "brakes", "turns,\nsame speed", "turns,\nspeeds up"),
                                                                ("speed up", "brake", "turn", "turn faster"))]
    for p in panels:
        p.v.alpha = p.a.alpha = 0.0
    scene.play(*[FadeIn(VGroup(p.box, p.title, p.track, p.car)) for p in panels], run_time=1.2)
    for p in panels:
        scene.add(p.v, p.a)
    legend = VGroup(VGroup(VecArrow(LEFT * 0.35, RIGHT * 0.35, cfg.VELOCITY, width=0.07, live=False), eq(r"\vec{v}", cfg.FONT["small"], cfg.VELOCITY)).arrange(RIGHT, buff=0.15),
                    VGroup(VecArrow(LEFT * 0.35, RIGHT * 0.35, cfg.ACCEL, width=0.07, live=False), eq(r"\vec{a}", cfg.FONT["small"], cfg.ACCEL)).arrange(RIGHT, buff=0.15))
    legend.arrange(RIGHT, buff=0.6).move_to([0, 3.35, 0])
    scene.play(FadeOut(head), run_time=0.4)
    scene.play(FadeIn(legend), run_time=0.4)

    def show_panel(p: Panel, end: float, run_time: float) -> None:
        scene.play(p.v.fade_to(1.0, run_time=0.4), p.a.fade_to(1.0, run_time=0.4), run_time=0.4)
        scene.play(p.drive(end, run_time))

    # --- 6. Speeds up: a along v ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    show_panel(panels[0], 5.4, 3.2)

    # --- 7. Brakes: a against v -------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    show_panel(panels[1], 4.6, 3.6)
    too = txt('braking', cfg.FONT["tiny"], cfg.ACCEL).move_to(PANELS[1] + np.array([0.6, 0.35, 0]))
    scene.play(FadeIn(too), run_time=0.6)

    # --- 8. Turns at constant speed: a sideways, inward ------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    show_panel(panels[2], 4.5, 4.0)

    # --- 9. Turns while speeding up: partly forward, partly inward ---------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    show_panel(panels[3], 4.5, 4.0)

    # --- 10. In every case: the direction of delta v ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    rule = paint(eq([r"\vec{a}", r"\ \parallel\ ", r"\Delta\vec{v}"], cfg.FONT["title"]), {0: cfg.ACCEL, 2: cfg.ACCEL})
    back = on_panel(rule, cfg.ACCEL, 0.3, 0.95).move_to(UP * 2.4)
    scene.play(FadeIn(back), *[p.drive(p.s.value + 1.6, 2.4) for p in panels], run_time=2.4)
    scene.play(*[p.drive(p.s.value + 1.4, 2.0) for p in panels], run_time=2.0)

    # --- 11. Constant speed can still mean acceleration ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    clear(scene)
    lines = VGroup(eq(r"|\vec v| = \mathrm{constant},\quad \vec a \ne 0", cfg.FONT["section"], cfg.WHITE),
                   eq(r"\vec v = \mathrm{constant}\ \Rightarrow\ \vec a = 0", cfg.FONT["body"], cfg.ACCEL)).arrange(DOWN, buff=0.5)
    scene.play(FadeIn(lines[0], shift=UP * 0.15), run_time=1.0)
    scene.wait(2.2)
    scene.play(FadeIn(lines[1], shift=UP * 0.15), run_time=1.0)

    # --- 12. Remember this at the top of the flight -----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    scene.play(lines.animate.scale(0.8).move_to(UP * 2.4), run_time=0.8)
    grid = plane((0, 45), (0, 12), unit=0.19, at=(-4.3, -3.2, 0), step=5, labels=False, faint=0.25)
    flight = SideFlight(grid, k=0.07)
    flight.clock.value = P.apex_time
    flight._draw_trail(flight.trail)
    flight.ball.move_to(flight.point(P.apex_time))
    a_top = flight.arrow("a", cfg.ACCEL)
    scene.add(grid, flight.trail, flight.ball, a_top)
    scene.play(FadeIn(grid), FadeIn(flight.trail), FadeIn(flight.ball), a_top.grow_in(run_time=1.0), run_time=1.0)
    ask = txt("at the top?", cfg.FONT["body"], cfg.ACCEL).next_to(flight.point(P.apex_time), RIGHT, buff=1.0)
    scene.play(FadeIn(ask), run_time=0.6)

    # --- 13. Can these definitions predict the future? -----------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    clear(scene)
    predict = txt('r(t) = ?', cfg.FONT["title"], cfg.WHITE)
    scene.play(FadeIn(predict, scale=0.95), run_time=1.0)
    scene.play(Indicate(predict, color=cfg.GOLD, scale_factor=1.05), run_time=1.4)
    scene.wait(2.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["16"])
