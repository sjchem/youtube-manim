"""Scene 20 — is there a centrifugal force? One simulation, two frames.

A car starts round a circular road; its passenger starts at the middle of
the car, moving with it. With no force on the passenger, the passenger
coasts in a straight line (inertia) until the outer door reaches them; from
then on the door pushes inward and the passenger turns with the car. The
contact moment is found numerically, not chosen.

Left: seen from the ground (not rotating) — a straight dashed path, then a
green inward push. No outward force anywhere. Right: the same numbers
transformed into the car's rotating frame — the road stands still, the
landmarks wheel round, and the passenger appears thrown outward, as if by a
centrifugal force m omega^2 r that exists only in this frame.
"""

from manim_scenes.common import *

LEFT_C = np.array([-3.85, -0.35, 0])
RIGHT_C = np.array([3.85, -0.35, 0])
RC = 1.5                       # road radius (screen units)
OMEGA = 0.55                    # the car's turning rate (rad per simulation second)
CAR_L = 0.7
CAR_W = CAR_L * 0.52            # the Car prop's own width
DOOR = CAR_W * 0.34             # how far the passenger can move sideways before the door stops them
SLOW = 0.45                     # simulation seconds per film second
LANDMARKS = [(2.55, 0.4), (2.45, 2.3), (2.6, 4.1)]   # (distance, angle) from the road's centre, fixed to the ground


def rot(a: float) -> np.ndarray:
    return np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])


class Ride:
    """The car on its circle (centre at the origin), and a passenger with no force until the door."""

    def __init__(self) -> None:
        self.start = self.car(0.0)
        self.v0 = RC * OMEGA * np.array([0.0, 1.0, 0.0])
        ts = np.linspace(0, 8, 8001)
        side = np.array([self.free_rel(s)[1] for s in ts])
        hit = np.argmax(side <= -DOOR)
        self.t_contact = float(ts[hit])
        self.rel_contact = self.free_rel(self.t_contact)
        self.rel_contact[1] = -DOOR

    def car(self, t: float) -> np.ndarray:
        a = OMEGA * t
        return RC * np.array([np.cos(a), np.sin(a), 0.0])

    def heading(self, t: float) -> float:
        return OMEGA * t + np.pi / 2

    def free_rel(self, t: float) -> np.ndarray:
        """The coasting passenger in car coordinates: x forward, y to the car's left (toward the centre)."""
        p = self.start + self.v0 * t
        return rot(-self.heading(t)) @ (p - self.car(t))

    def rel(self, t: float) -> np.ndarray:
        return self.free_rel(t) if t < self.t_contact else self.rel_contact

    def passenger(self, t: float) -> np.ndarray:
        return self.car(t) + rot(self.heading(t)) @ self.rel(t)

    def in_car_frame(self, point: np.ndarray, t: float) -> np.ndarray:
        """A ground point as seen from the car (car fixed at (RC, 0), nose up)."""
        return np.array([RC, 0.0, 0.0]) + rot(np.pi / 2 - self.heading(t)) @ (point - self.car(t))


class Scene20Centrifugal(Scene):
    def construct(self) -> None:
        play_scene(self)


def panel_with_road(centre, title: str) -> VGroup:
    box = panel(7.3, 6.5, cfg.MUTED, 0.5).move_to(centre + UP * 0.25)
    road = Circle(radius=RC, stroke_color=cfg.GRAY, stroke_width=30, stroke_opacity=0.4).move_to(centre)
    name = txt(title, cfg.FONT["small"], cfg.WHITE).next_to(box.get_top(), DOWN, buff=0.22)
    return VGroup(box, road, name)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "20", "Is there a centrifugal force?")
    ride = Ride()
    clock = Knob(ride.t_contact + 2.0)
    ground_panel = panel_with_road(LEFT_C, "Ground frame")
    car = Car(cfg.CAR, CAR_L)
    car.keep_in_frame = True
    car.add_updater(lambda m: m.set_pose(LEFT_C + ride.car(clock.value), ride.heading(clock.value)))
    rider = bead(LEFT_C + ride.passenger(clock.value), cfg.GOLD, 0.13)
    rider.add_updater(lambda m: m.move_to(LEFT_C + ride.passenger(clock.value)))
    car.update()
    scene.play(FadeIn(ground_panel), FadeIn(car), FadeIn(rider), run_time=0.9)
    pushed = chip("pushed outward?", cfg.WARNING).move_to([3.85, 0.0, 0])
    scene.play(FadeIn(pushed), clock.to(car, clock.value + 2.0, run_time=2.0 / SLOW, rate_func=linear), run_time=2.0 / SLOW)

    # --- 2. From the ground: the passenger keeps going straight ------------------------------------------------------
    beat(scene, t, 1)
    scene.play(FadeOut(head), FadeOut(rider), run_time=0.4)
    clock.value = 0.0
    car.update()
    rider.update()
    scene.play(FadeIn(rider), run_time=0.4)
    straight = dashed_path(LEFT_C + ride.start, LEFT_C + ride.start + ride.v0 * 2.2, cfg.GOLD, width=3, opacity=0.8)
    inertia = VGroup(txt("inertia:", cfg.FONT["tiny"], cfg.GOLD), txt("straight on", cfg.FONT["tiny"], cfg.GOLD)).arrange(DOWN, buff=0.08)
    inertia.move_to([LEFT_C[0], 1.65, 0])
    scene.play(Create(straight), FadeIn(inertia), run_time=0.8)
    scene.play(clock.to(car, ride.t_contact, run_time=ride.t_contact / SLOW * 0.75, rate_func=linear),
               run_time=ride.t_contact / SLOW * 0.75)
    scene.wait(0.6)

    # --- 3. The door pushes inward: that turns you ----------------------------------------------------------------------------------
    beat(scene, t, 2)
    push = VecArrow(lambda: LEFT_C + ride.passenger(clock.value),
                    lambda: LEFT_C + ride.passenger(clock.value) + mu.unit(-ride.passenger(clock.value)) * 0.85, cfg.FORCE, width=0.08)
    scene.add(push)
    door = txt("the door pushes inward", cfg.FONT["small"], cfg.FORCE).move_to(np.array([LEFT_C[0], -2.75, 0]))
    scene.play(push.grow_in(run_time=0.6), FadeIn(door), FadeOut(inertia), run_time=0.6)
    scene.play(clock.to(car, clock.value + 4.0, run_time=4.0 / SLOW, rate_func=linear), run_time=4.0 / SLOW)
    scene.play(clock.to(car, clock.value + 1.6, run_time=1.6 / SLOW, rate_func=linear), run_time=1.6 / SLOW)

    # --- 4. No outward force in this frame --------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    none = VGroup(cross_mark(0.18), txt("no outward force", cfg.FONT["small"], cfg.WHITE)).arrange(RIGHT, buff=0.2)
    none.move_to(LEFT_C + np.array([0, 0.1, 0]))
    scene.play(FadeOut(pushed), FadeIn(none), clock.to(car, clock.value + 1.0, run_time=1.0 / SLOW, rate_func=linear),
               run_time=1.0 / SLOW)
    scene.play(clock.to(car, clock.value + 1.6, run_time=1.6 / SLOW, rate_func=linear), run_time=1.6 / SLOW)

    # --- 5. Ride along: the rotating frame -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    car_panel = panel_with_road(RIGHT_C, "Rotating frame")
    fixed_car = Car(cfg.CAR, CAR_L)
    fixed_car.keep_in_frame = True
    fixed_car.set_pose(RIGHT_C + np.array([RC, 0, 0]), np.pi / 2)
    marks = VGroup()
    for k, (d, a) in enumerate(LANDMARKS):
        spot = d * np.array([np.cos(a), np.sin(a), 0.0])
        tree = VGroup(Circle(radius=0.16, stroke_width=0, fill_color="#3F8F5A", fill_opacity=0.95),
                      Circle(radius=0.07, stroke_width=0, fill_color="#6FBF7A", fill_opacity=1).shift(UL * 0.05))
        def place_tree(m, spot=spot):
            point = RIGHT_C + ride.in_car_frame(spot, clock.value)
            m.move_to(point)
            local = point - RIGHT_C
            clearance = min(3.25 - abs(local[0]), 1.85 - local[1], local[1] + 1.95)
            m.set_opacity(float(np.clip(clearance / 0.25, 0.0, 1.0)))
        tree.add_updater(place_tree)
        marks.add(tree)
    inner = bead(RIGHT_C, cfg.GOLD, 0.13)
    inner.add_updater(lambda m: m.move_to(RIGHT_C + np.array([RC, 0, 0]) + ride.rel(clock.value)[0] * UP + ride.rel(clock.value)[1] * LEFT))
    left_trees = VGroup()
    for d, a in LANDMARKS:
        left_trees.add(VGroup(Circle(radius=0.16, stroke_width=0, fill_color="#3F8F5A", fill_opacity=0.95),
                              Circle(radius=0.07, stroke_width=0, fill_color="#6FBF7A", fill_opacity=1).shift(UL * 0.05))
                       .move_to(LEFT_C + d * np.array([np.cos(a), np.sin(a), 0.0])))
    for m in (*marks, inner):
        m.update()
    push.alpha = 0.0
    scene.play(FadeOut(VGroup(none, door)), FadeIn(car_panel), FadeIn(fixed_car), FadeIn(marks), FadeIn(left_trees), run_time=0.9)
    scene.play(FadeOut(rider), FadeOut(push), run_time=0.3)
    clock.value = 0.0
    rider.update()
    inner.update()
    scene.play(FadeIn(rider), FadeIn(inner), run_time=0.4)
    thrown = txt("seems thrown outward", cfg.FONT["small"], cfg.ROSE).move_to(np.array([RIGHT_C[0], -2.75, 0]))
    scene.play(FadeIn(thrown), clock.to(car, ride.t_contact, run_time=ride.t_contact / SLOW, rate_func=linear),
               run_time=ride.t_contact / SLOW)
    scene.play(clock.to(car, clock.value + 1.6, run_time=1.6 / SLOW, rate_func=linear), run_time=1.6 / SLOW)

    # --- 6. The centrifugal force: m omega^2 r, outward -------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    out = VecArrow(lambda: inner.get_center(), lambda: inner.get_center() + mu.unit(inner.get_center() - RIGHT_C) * 0.85, cfg.ROSE, width=0.08)
    scene.add(out)
    cf = eq(r"F_{\text{cf}} = m\,\omega^2 r", cfg.FONT["body"], cfg.ROSE).move_to([RIGHT_C[0], 1.65, 0])
    scene.play(out.grow_in(run_time=0.7), Write(cf), clock.to(car, clock.value + 0.6, run_time=1.2, rate_func=linear), run_time=1.2)
    scene.play(clock.to(car, clock.value + 3.6, run_time=3.6 / SLOW, rate_func=linear), run_time=3.6 / SLOW)

    # --- 7. Fictitious: it exists because the frame rotates -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    fake = chip("fictitious (inertial) force", cfg.ROSE, cfg.FONT["tiny"]).move_to([RIGHT_C[0], -1.95, 0])
    scene.play(FadeIn(fake), *[Indicate(m, color=cfg.WHITE, scale_factor=1.25) for m in marks], run_time=1.2)
    scene.play(clock.to(car, clock.value + 2.4, run_time=2.4 / SLOW, rate_func=linear), run_time=2.4 / SLOW)

    # --- 8. Centripetal: real, non-rotating frame. Centrifugal: the rotating frame -------------------------------------------------------------------------------------
    beat(scene, t, 7)
    real = VGroup(txt("centripetal", cfg.FONT["label"], cfg.FORCE), txt("real net inward force", cfg.FONT["tiny"], cfg.WHITE)).arrange(DOWN, buff=0.1)
    real.move_to(np.array([LEFT_C[0], -2.75, 0]))
    frame_only = VGroup(txt("centrifugal", cfg.FONT["label"], cfg.ROSE), txt("rotating frame only", cfg.FONT["tiny"], cfg.WHITE)).arrange(DOWN, buff=0.1)
    frame_only.move_to(np.array([RIGHT_C[0], -2.75, 0]))
    push.alpha = 1.0
    scene.add(push)
    scene.play(FadeOut(thrown), FadeOut(fake), clock.to(car, clock.value + 0.2, run_time=0.4, rate_func=linear), run_time=0.4)
    scene.play(FadeIn(real), FadeIn(frame_only), clock.to(car, clock.value + 0.3, run_time=0.6, rate_func=linear), run_time=0.6)
    scene.play(clock.to(car, clock.value + 3.6, run_time=3.6 / SLOW, rate_func=linear), run_time=3.6 / SLOW)

    # --- 9. Circular motion needs a net inward force: tension, friction, gravity ------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    for m in (car, rider, inner, *marks):
        m.clear_updaters()
    clear(scene, run_time=0.7)
    need = txt("circular motion needs a net inward force", cfg.FONT["section"], cfg.FORCE).move_to([0, 1.2, 0])
    fit_width(need, 13.0)
    providers = VGroup(*[chip(name, cfg.FORCE) for name in ("tension", "friction", "gravity")]).arrange(RIGHT, buff=0.6).next_to(need, DOWN, buff=0.7)
    scene.play(FadeIn(need, shift=UP * 0.1), run_time=0.9)
    scene.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in providers], lag_ratio=0.3), run_time=1.5)
    scene.wait(2.4)
    scene.play(*[Indicate(p, color=cfg.FORCE, scale_factor=1.06) for p in providers], run_time=1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["20"])
