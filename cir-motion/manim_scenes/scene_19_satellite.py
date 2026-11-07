"""Scene 19 — why satellites orbit. A turning 3D Earth (a polished globe with
a meridian grid that hides behind it). Newton's cannon fires horizontally
from a tall mountain at four speeds; each path is integrated with RK4 under
inverse-square gravity (``physics_models.cannon_shot``): the first three
land farther and farther round, the fourth (circular speed) never lands.

On that orbit the satellite carries a gold tangent velocity and a green
gravity arrow; beside a dashed straight line it shows how far it has fallen.
Gravity supplies the centripetal force: GMm/r^2 = m v^2/r, the mass cancels,
v = sqrt(GM/r), and a small satellite and a big station share one orbit at
one speed. The real 400 km orbit is then drawn to scale (it hugs the
planet): v ~ 7.67 km/s, gravity still ~ 8.7 m/s^2, T ~ 92 minutes.
"""

from manim_scenes.common import *

RE = 1.75                                  # Earth's radius in stage units
CENTRE = np.zeros(3)
COL = 4.4


class Scene19Satellite(Scene):
    def construct(self) -> None:
        play_scene(self)


def to_stage(points2: np.ndarray, scale: float = RE) -> np.ndarray:
    pts = np.asarray(points2, dtype=float)
    return np.column_stack([pts[:, 0] * scale, pts[:, 1] * scale, np.zeros(len(pts))])


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "19", "Why satellites orbit")
    stage = Stage((-2.5, -0.35, 0), zoom=1.05, yaw=0.0, pitch=0.24, sway=0.02, distance=30.0)
    spin = Knob(0.0)
    globe(stage, CENTRE, RE, spin)
    show(scene, stage, 1.2)
    scene.play(spin.to(stage, 0.9, run_time=3.0, rate_func=linear))
    peak = RE * (1 + pm.CANNON_HEIGHT)
    mountain = Face([np.array([-0.3, RE * 0.97, 0.02]), np.array([0.3, RE * 0.97, 0.02]), np.array([0.0, peak, 0.02])],
                    "#7C8B73", opacity=0.95, edge_opacity=0.9)
    mountain.bias = 5.0
    gun_base = Ball(np.array([0.0, peak + 0.03, 0.03]), 0.06, "#5D7488", layers=10)
    gun_tip = Ball(np.array([-0.2, peak + 0.05, 0.03]), 0.04, "#9DB4C7", layers=8)
    gun = Rod(gun_base, gun_tip, width=10, dark="#24384A", light="#9DB4C7")
    for part in (mountain, gun, gun_base, gun_tip):
        part.presence = 0.0
        part.bias = 6.0
    stage.add_body(mountain, gun, gun_base, gun_tip)
    what = chip("what keeps it on its path?", cfg.WHITE).move_to([COL, 3.0, 0])
    scene.play(FadeOut(head), FadeIn(what), *[stage.fade(p, 1.0) for p in (mountain, gun, gun_base, gun_tip)], run_time=1.0)

    # --- 2. Fire horizontally: faster shots land farther ------------------------------------------------------------------
    beat(scene, t, 1)
    shots = [to_stage(pm.cannon_shot(f)) for f in pm.CANNON_SPEEDS]
    colors = [cfg.ORANGE, cfg.GOLD, cfg.GREEN, cfg.CYAN]
    drawn = []

    def fire(points: np.ndarray, color: str, run_time: float) -> tuple[Curve, Ball]:
        progress = Knob(0.0)
        count = lambda: max(int(progress.value * (len(points) - 1)) + 1, 2)  # noqa: E731
        path = Curve(lambda: points[:count()], color, width=4)
        path.bias = 4.0
        shell = Ball(lambda: points[count() - 1], 0.07, cfg.WHITE, layers=10)
        shell.bias = 7.0
        stage.add_body(path, shell)
        scene.play(progress.to(stage, 1.0, run_time=run_time, rate_func=linear), run_time=run_time)
        drawn.append((path, shell))
        return path, shell

    gravity = txt("gravity", cfg.FONT["label"], cfg.FORCE).move_to([COL, 2.0, 0])
    scene.play(fade_through(what, gravity), run_time=0.8)
    for k in range(2):
        fire(shots[k], colors[k], 3.2)
        scene.wait(0.5)

    # --- 3. Fast enough: the ground curves away as fast as it falls --------------------------------------------------------------------
    beat(scene, t, 2)
    fire(shots[2], colors[2], 3.0)
    fire(shots[3], colors[3], 5.2)
    never = txt("it never lands", cfg.FONT["label"], cfg.CYAN).move_to([COL, 1.0, 0])
    scene.play(FadeIn(never, shift=UP * 0.1), run_time=0.7)

    # --- 4. A satellite is always falling ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(*[stage.fade(item, 0.0) for path, shell in drawn[:3] for item in (path, shell)], stage.fade(drawn[3][1], 0.0),
               FadeOut(VGroup(gravity, never)), *[stage.fade(p, 0.0) for p in (mountain, gun, gun_base, gun_tip)], run_time=0.8)
    r0 = 1 + pm.CANNON_HEIGHT
    orbit_w = 1 / np.sqrt(r0 ** 3)                 # dimensionless angular speed (GM = 1)
    clock = Knob(0.0)
    angle = lambda: np.pi / 2 + orbit_w * clock.value  # noqa: E731
    sat_at = lambda: np.array([np.cos(angle()), np.sin(angle()), 0.0]) * r0 * RE  # noqa: E731
    sat = Ball(sat_at, 0.11, cfg.WHITE, layers=14)
    sat.bias = 8.0
    sat.keep_in_frame = True
    v_sat = Vector(sat_at, lambda: sat_at() + np.array([-np.sin(angle()), np.cos(angle()), 0]) * 1.0, cfg.VELOCITY, width=0.07, tip=0.22)
    g_sat = Vector(sat_at, lambda: sat_at() * (1 - 0.75 / (r0 * RE)), cfg.FORCE, width=0.07, tip=0.22)
    for item in (sat, v_sat, g_sat):
        item.presence = 0.0
    stage.add_body(sat)
    stage.add_overlay(v_sat, g_sat)
    scene.play(stage.fade(sat, 1.0), stage.fade(v_sat, 1.0), stage.fade(g_sat, 1.0), run_time=0.7)
    # From the top: the straight line it would follow, and how far it has fallen below it.
    top = np.array([0.0, r0 * RE, 0.0])
    reach = 0.55
    straight = Curve(np.array([top, top + LEFT * r0 * RE * reach]), cfg.MUTED, width=3, dashed=True, glow=False)
    fallen = Curve(np.array([top + LEFT * r0 * RE * reach, np.array([-np.sin(reach), np.cos(reach), 0]) * r0 * RE]),
                   cfg.FORCE, width=4, dashed=True, glow=False)
    for item in (straight, fallen):
        item.presence = 0.0
        item.bias = 7.5
    stage.add_body(straight, fallen)
    scene.play(stage.fade(straight, 1.0), clock.to(stage, reach / orbit_w, run_time=2.6, rate_func=linear), run_time=2.6)
    falls = txt("falling, all the time", cfg.FONT["label"], cfg.FORCE).move_to([COL, 3.3, 0])
    scene.play(stage.fade(fallen, 1.0), FadeIn(falls), run_time=0.8)
    scene.play(clock.to(stage, clock.value + 0.9 / orbit_w, run_time=3.6, rate_func=linear), run_time=3.6)

    # --- 5. GMm / r^2 = m v^2 / r ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    balance = eq([r"\frac{G M m}{r^2}", "=", r"\frac{m v^2}{r}"], cfg.FONT["section"])
    paint(balance, {0: cfg.FORCE, 2: cfg.FORCE}).move_to([COL, 2.0, 0])
    labels = VGroup(txt("gravity", cfg.FONT["tiny"], cfg.FORCE).next_to(balance[0], DOWN, buff=0.2),
                    txt("needed", cfg.FONT["tiny"], cfg.FORCE).next_to(balance[2], DOWN, buff=0.2))
    scene.play(stage.fade(straight, 0.0), stage.fade(fallen, 0.0), Write(balance), clock.to(stage, clock.value + 0.4 / orbit_w, run_time=1.6, rate_func=linear),
               run_time=1.6)
    scene.play(FadeIn(labels), clock.to(stage, clock.value + 0.2 / orbit_w, run_time=0.8, rate_func=linear), run_time=0.8)
    scene.play(clock.to(stage, clock.value + 1.6 / orbit_w, run_time=6.5, rate_func=linear), run_time=6.5)

    # --- 6. The mass cancels: v = sqrt(GM / r) ----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    speed = paint(eq([r"v", "=", r"\sqrt{\frac{G M}{r}}"], cfg.FONT["title"]), {0: cfg.VELOCITY}).next_to(balance, DOWN, buff=0.75)
    struck = VGroup()
    scene.play(FadeOut(labels), Indicate(balance, color=cfg.FORCE, scale_factor=1.02), run_time=0.9)
    scene.play(Write(speed), clock.to(stage, clock.value + 0.4 / orbit_w, run_time=1.4, rate_func=linear), run_time=1.4)
    speed_box = boxed(speed, cfg.RESULT)[0]
    scene.play(FadeIn(speed_box), clock.to(stage, clock.value + 0.2 / orbit_w, run_time=0.7, rate_func=linear), run_time=0.7)
    scene.play(clock.to(stage, clock.value + 1.6 / orbit_w, run_time=6.5, rate_func=linear), run_time=6.5)

    # --- 7. Small satellite, big station: the same speed ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    lag = 0.55
    station = Ball(lambda: np.array([np.cos(angle() - lag), np.sin(angle() - lag), 0.0]) * r0 * RE, 0.2, "#D9E4EC", layers=18)
    station.bias = 8.0
    station.presence = 0.0
    stage.add_body(station)
    same = VGroup(txt("small or huge:", cfg.FONT["small"], cfg.MUTED), txt("same orbit, same speed", cfg.FONT["small"], cfg.VELOCITY))
    same.arrange(DOWN, buff=0.15).move_to([COL, -2.4, 0])
    scene.play(stage.fade(station, 1.0), stage.fade(g_sat, 0.0), FadeIn(same), clock.to(stage, clock.value + 0.3 / orbit_w, run_time=1.0, rate_func=linear),
               run_time=1.0)
    scene.play(clock.to(stage, clock.value + 1.6 / orbit_w, run_time=6.5, rate_func=linear), run_time=6.5)

    # --- 8. A real orbit, 400 km up: 7.67 km/s ---------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scale = pm.orbit_radius() / pm.R_EARTH
    real = chunked_curve(ring_curve_xy(scale * RE), cfg.GOLD, chunks=24, width=3.5)
    for piece in real:
        piece.presence = 0.0
    orbit_clock = Knob(0.0)
    real_sat = Ball(lambda: np.array([np.cos(orbit_clock.value), np.sin(orbit_clock.value), 0]) * scale * RE,
                    0.08, cfg.WHITE, layers=12)
    real_sat.keep_in_frame = True
    real_sat.presence = 0.0
    stage.add_body(*real, real_sat)

    def advance_orbit(m, dt):
        if m._live:
            orbit_clock.value += dt * 0.42

    stage.add_updater(advance_orbit)
    scene.play(FadeOut(VGroup(same, falls, balance, struck, speed, speed_box)), stage.fade(station, 0.0), stage.fade(sat, 0.0), stage.fade(v_sat, 0.0),
               stage.fade(drawn[3][0], 0.0), stage.fade(real_sat, 1.0), *[stage.fade(p, 1.0) for p in real], run_time=1.0)
    low = Tag(txt("400 km up, to scale", cfg.FONT["small"], cfg.GOLD), np.array([0.0, -scale * RE, 0.0]), DOWN * 0.45)
    low.presence = 0.0
    stage.add_overlay(low)
    v_real = eq(rf"v \approx {fx(pm.orbital_speed() / 1e3, 2)}\ \mathrm{{km/s}}", cfg.FONT["section"], cfg.VELOCITY).move_to([COL, 2.2, 0])
    scene.play(stage.fade(low, 1.0), spin.to(stage, spin.value + 0.4, run_time=1.4, rate_func=linear), run_time=1.4)
    scene.play(FadeIn(v_real, shift=UP * 0.1), spin.to(stage, spin.value + 0.3, run_time=1.0, rate_func=linear), run_time=1.0)
    scene.play(spin.to(stage, spin.value + 1.6, run_time=6.0, rate_func=linear), run_time=6.0)

    # --- 9. Gravity up there: still about 8.7 m/s^2 ---------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    bars = VGroup()
    for name, value, color in (("surface", pm.G, cfg.MUTED), ("400 km up", pm.gravity_at(), cfg.FORCE)):
        bar = Rectangle(width=3.6 * value / pm.G, height=0.32, stroke_width=0, fill_color=color, fill_opacity=0.9)
        row = VGroup(txt(name, cfg.FONT["tiny"], cfg.MUTED), bar, eq(rf"{fx(value, 1)}\ \mathrm{{m/s^2}}", cfg.FONT["small"], color))
        row.arrange(RIGHT, buff=0.25)
        bars.add(row)
    bars.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([COL - 0.2, 0.2, 0])
    fit_width(bars, 6.4)
    scene.play(FadeIn(bars, shift=UP * 0.1), spin.to(stage, spin.value + 0.4, run_time=1.2, rate_func=linear), run_time=1.2)
    not_gone = txt("g ≠ 0", cfg.FONT["small"], cfg.FORCE).next_to(bars, UP, buff=0.25)
    scene.play(FadeIn(not_gone), spin.to(stage, spin.value + 0.3, run_time=0.8, rate_func=linear), run_time=0.8)
    scene.play(spin.to(stage, spin.value + 1.9, run_time=7.5, rate_func=linear), run_time=7.5)

    # --- 10. T = 2 pi sqrt(r^3 / GM) ~ 92 minutes ---------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(VGroup(bars, not_gone, v_real)), run_time=0.6)
    period = eq([r"T", "=", r"\frac{2\pi r}{v}", "=", r"2\pi\sqrt{\frac{r^3}{G M}}"], cfg.FONT["section"]).move_to([COL, 2.1, 0])
    fit_width(period, 6.4)
    minutes = eq(rf"T \approx {wh(int(pm.orbital_period() / 60))}\ \text{{minutes}}", cfg.FONT["section"], cfg.GOLD).next_to(period, DOWN, buff=0.5)
    scene.play(Write(period), spin.to(stage, spin.value + 0.5, run_time=1.8, rate_func=linear), run_time=1.8)
    scene.play(FadeIn(minutes, shift=UP * 0.1), spin.to(stage, spin.value + 0.3, run_time=0.9, rate_func=linear), run_time=0.9)
    scene.play(*stage.turn(yaw=0.35, pitch=0.42, run_time=9.0), spin.to(stage, spin.value + 2.2, run_time=9.0, rate_func=linear), run_time=9.0)

    # --- 11. Ideal circular orbit; the same idea as a ball on a string ----------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    caveat = chip("ideal circular orbit · spherical Earth", cfg.MUTED, cfg.FONT["tiny"]).move_to([COL, -1.4, 0])
    echo = txt("the same idea as a ball on a string", cfg.FONT["small"], cfg.WHITE).next_to(caveat, DOWN, buff=0.4)
    fit_width(echo, 6.6)
    scene.play(FadeIn(caveat), run_time=0.7)
    scene.play(FadeIn(echo, shift=UP * 0.1), run_time=0.8)
    scene.play(*stage.turn(yaw=0.0, pitch=0.24, run_time=8.0), spin.to(stage, spin.value + 2.0, run_time=8.0, rate_func=linear), run_time=8.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["19"])


def ring_curve_xy(radius: float, n: int = 200) -> np.ndarray:
    """A closed circle in the stage's x-y plane (the orbit plane)."""
    a = np.linspace(0, TAU, n)
    return np.column_stack([radius * np.cos(a), radius * np.sin(a), np.zeros(n)])
