"""Scene 20 — one spin, many motions. A disc faces the viewer on a 3D stage
and spins up with a steady (illustrative) angular acceleration. Three gold
beads ride it at r, 2r and 3r, with gold tangent velocity arrows. These retire,
and the outer bead alone carries blue tangential acceleration r alpha,
orange inward acceleration r omega^2, and their white resultant. The other
beads disappear to keep attention on the perpendicular vector sum.
As omega grows the orange arrow lengthens like omega squared. Shared angular
quantities and the acceleration equations occupy a separate right column.
"""

from manim_scenes.common import *

RADII = (0.75, 1.5, 2.25)
ALPHA = 0.5                  # rad/s^2, an illustrative spin-up (no worked numbers in this scene)
OMEGA0 = 0.4
V_SCALE = 0.55
A_SCALE = 0.6                # one scale for both accelerations, so their lengths compare honestly
SLOW = 0.025                 # physics seconds per film second while the arrows are explained
CENTRE = np.array([-2.4, -0.4, 0.0])


class Scene20ParticleMotion(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "20", "One spin, many motions")
    clock = Knob(0.0)

    def omega() -> float:
        return OMEGA0 + ALPHA * clock.value

    def angle() -> float:
        return OMEGA0 * clock.value + 0.5 * ALPHA * clock.value ** 2

    stage = Stage(CENTRE, zoom=1.25, yaw=0.0, pitch=0.0, sway=0.015)
    disc = Drum(ORIGIN, 2.6, 0.1, cfg.DISC_BODY, spin=angle, stripe=cfg.DISC_STRIPE, sectors=8)
    stage.add_body(disc)
    rate = Knob(SLOW)
    drive(stage, clock, rate)
    show(scene, stage, 1.0)
    slow = chip("slow motion", cfg.MUTED, cfg.FONT["tiny"]).move_to([-6.2, 3.3, 0])
    scene.play(FadeIn(slow), run_time=0.5)

    def bead_at(r: float) -> np.ndarray:
        a = angle() + 0.9
        return np.array([r * np.cos(a), r * np.sin(a), 0.2])

    def tangent(r: float) -> np.ndarray:
        a = angle() + 0.9
        return np.array([-np.sin(a), np.cos(a), 0.0])

    def inward(r: float) -> np.ndarray:
        a = angle() + 0.9
        return -np.array([np.cos(a), np.sin(a), 0.0])

    beads = [Ball(lambda r=r: bead_at(r), 0.13, cfg.GOLD, layers=14) for r in RADII]
    for b in beads:
        b.bias = 50.0
    stage.add_body(*beads)
    shared = VGroup(eq(r"\omega,\ \alpha", cfg.FONT["title"], cfg.ANGLE),
                    txt("shared by every particle", cfg.FONT["tiny"], cfg.ANGLE)).arrange(RIGHT, buff=0.3).move_to([4.2, 2.65, 0])
    scene.play(FadeIn(shared, shift=DOWN * 0.1), run_time=1.0)

    def arrows(vector_fn, color, scale, radii=RADII):
        return [Vector(lambda r=r: bead_at(r), lambda r=r: bead_at(r) + vector_fn(r) * scale, color, width=0.07, tip=0.22)
                for r in radii]

    # --- 2. v = r omega -----------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    v_arrows = arrows(lambda r: tangent(r) * r * omega(), cfg.VELOCITY, V_SCALE)
    hidden(*v_arrows)
    stage.add_overlay(*v_arrows)
    scene.play(*[stage.fade(a, 1.0) for a in v_arrows], run_time=0.9)
    v_eq = eq(r"v = r\,\omega", cfg.FONT["section"], cfg.VELOCITY).move_to([4.2, 1.75, 0])
    scene.play(Write(v_eq), run_time=1.0)

    # --- 3. a_t = r alpha ------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(*[stage.fade(a, 0.0) for a in v_arrows],
               *[stage.fade(b, 0.0) for b in beads[:-1]], run_time=0.5)
    at_arrows = arrows(lambda r: tangent(r) * r * ALPHA, cfg.TANGENTIAL, A_SCALE, radii=RADII[-1:])
    hidden(*at_arrows)
    stage.add_overlay(*at_arrows)
    at_eq = eq(r"a_t = r\,\alpha", cfg.FONT["section"], cfg.TANGENTIAL).move_to([4.2, 0.8, 0])
    scene.play(*[stage.fade(a, 1.0) for a in at_arrows], Write(at_eq), run_time=1.2)

    # --- 4. a_r = r omega^2 -------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    ar_arrows = arrows(lambda r: inward(r) * r * omega() ** 2, cfg.ACCEL, A_SCALE, radii=RADII[-1:])
    hidden(*ar_arrows)
    stage.add_overlay(*ar_arrows)
    ar_eq = eq(r"a_r = r\,\omega^2", cfg.FONT["section"], cfg.ACCEL).move_to([4.2, -0.8, 0])
    scene.play(*[stage.fade(a, 1.0) for a in ar_arrows], Write(ar_eq), run_time=1.2)

    # --- 5. Speed vs direction ------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    roles = VGroup(txt("changes the speed", cfg.FONT["tiny"], cfg.TANGENTIAL).next_to(at_eq, DOWN, buff=0.28),
                   txt("changes the direction", cfg.FONT["tiny"], cfg.ACCEL).next_to(ar_eq, DOWN, buff=0.28))
    scene.play(FadeIn(roles, lag_ratio=0.4), run_time=1.0)

    # --- 6. The total ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    total = arrows(lambda r: tangent(r) * r * ALPHA + inward(r) * r * omega() ** 2, cfg.WHITE, A_SCALE, radii=RADII[-1:])
    hidden(*total)
    stage.add_overlay(*total)
    a_eq = eq(r"a = \sqrt{(r\alpha)^2 + (r\omega^2)^2}", cfg.FONT["section"], cfg.WHITE)
    fit_width(a_eq, 6.3)
    a_box = boxed(a_eq, cfg.RESULT).move_to([4.1, -2.55, 0])
    scene.play(*[stage.fade(a, 1.0) for a in total], Write(a_eq), run_time=1.6)
    scene.play(Create(a_box.frame), run_time=0.6)
    perp = caption("the two parts are perpendicular", cfg.WHITE)
    scene.play(FadeIn(perp), run_time=0.6)

    # --- 7. Faster: the radial part dominates --------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    grows = caption("radial acceleration grows as ω²", cfg.ACCEL)
    scene.play(fade_through(perp, grows), rate.to(stage, 0.16), run_time=1.2)
    scene.wait(max(time_left(scene, t, 7) - 1.4, 0.1))
    scene.play(rate.to(stage, 0.02), run_time=1.0)

    # --- 8. One omega, many motions -------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    summary = caption("one ω · different linear motions", cfg.WHITE)
    scene.play(fade_through(grows, summary), run_time=0.8)
    finish(scene, t, stage)
