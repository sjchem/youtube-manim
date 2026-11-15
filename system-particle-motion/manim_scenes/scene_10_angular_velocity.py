"""Scene 10 — angular velocity as a vector. A 3D turntable spins about a
dashed vertical axis. The cyan omega arrow stands on the axis; a curled cyan
arrow shows the sense of turning (the right-hand rule). The spin slows,
reverses, and omega shrinks through zero and flips downward. Three beads at
1, 2 and 3 times a base radius ride the turntable; a magenta r from a point on
the axis reaches the outer bead, its perpendicular part r_perp dashed; each
bead carries a gold v = omega x r, tangent to its circle, its length
proportional to the distance from the axis.
"""

from manim_scenes.common import *

R_TABLE = 2.4
RADII = (0.75, 1.5, 2.25)
V_SCALE = 0.42
W0 = 1.1
R_COLOR = "#FF5EA8"          # outlined magenta stays distinct on both turntable sectors


class Scene10AngularVelocity(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "10", "Angular velocity as a vector")
    stage = Stage((1.5, -1.2, 0.0), zoom=1.35, yaw=-0.3, pitch=0.5, sway=0.03)
    floor(stage, -1.4, reach=6.0, opacity=0.18)
    angle, w = Knob(0.0), Knob(W0)
    drive(stage, angle, w)
    table = Drum(ORIGIN, R_TABLE, 0.12, cfg.DISC_BODY, axis=(0, 1, 0), spin=lambda: angle.value, stripe=cfg.DISC_STRIPE,
                 sectors=8)
    stand = Drum(np.array([0.0, -0.75, 0.0]), 0.18, 0.6, cfg.STEEL, axis=(0, 1, 0), sectors=2)
    axis = axis_line(stage, [0, -1.4, 0], [0, 2.15, 0], cfg.MUTED, opacity=0.8)
    stage.add_body(stand, table)
    show(scene, stage, 1.0)
    recall = eq(r"\omega = {d\theta \over dt}", cfg.FONT["section"], cfg.OMEGA).move_to([-5.2, 2.6, 0])
    scene.play(Write(recall), run_time=1.2)

    # --- 2. Omega points along the axis ------------------------------------------------------------------------
    beat(scene, t, 1)
    top = np.array([0.0, 0.16, 0.0])
    omega = Vector(lambda: top, lambda: top + np.array([0.0, 1.5 * w.value, 0.0]), cfg.OMEGA, width=0.11, tip=0.34)
    omega_lab = Tag(eq(r"\vec\omega", cfg.FONT["section"], cfg.OMEGA), lambda: top + np.array([0, 1.5 * w.value, 0]),
                    RIGHT * 0.55)
    hidden(omega, omega_lab)
    stage.add_overlay(omega, omega_lab)
    scene.play(stage.fade(omega, 1.0), stage.fade(omega_lab, 1.0), run_time=1.0)
    along = caption("omega points along the axis", cfg.OMEGA)
    scene.play(FadeIn(along), run_time=0.7)

    # --- 3. Right-hand rule; spin the other way and omega flips --------------------------------------------------------
    beat(scene, t, 2)
    curl = turn_arrow_3d(stage, lambda: np.array([0.0, 0.9 * np.sign(w.value) if abs(w.value) > 0.05 else 0.9, 0.0]),
                         (0, 1, 0), 0.6, 0.0, np.radians(260), cfg.OMEGA, width=5)
    hidden(*curl.parts)
    rhr = caption("right-hand rule: thumb along ω", cfg.OMEGA)
    scene.play(*[stage.fade(p, 1.0) for p in curl.parts], fade_through(along, rhr), run_time=1.0)
    scene.wait(1.6)
    scene.play(*[stage.fade(p, 0.0) for p in curl.parts], run_time=0.5)
    scene.play(w.to(stage, -W0, rate_func=smooth), run_time=3.2)
    flips = caption("spin it the other way: omega flips", cfg.OMEGA)
    scene.play(fade_through(rhr, flips), run_time=0.7)
    scene.play(w.to(stage, W0, rate_func=smooth), run_time=2.4)

    # --- 4. A point on the body: v = omega x r ---------------------------------------------------------------------------
    beat(scene, t, 3)
    def bead_at(r: float) -> np.ndarray:
        a = 0.6 + angle.value
        return np.array([r * np.sin(a), 0.2, r * np.cos(a)])

    beads = [Ball(lambda r=r: bead_at(r), 0.12, cfg.GOLD, layers=14) for r in RADII]
    for b in beads:
        b.bias = 50.0
    base = np.array([0.0, -1.0, 0.0])
    r_vec = Vector(lambda: base, lambda: bead_at(RADII[-1]), R_COLOR, width=0.09, tip=0.28, glow=False)
    r_vec.body.set_stroke(cfg.BG, width=2.5)
    r_lab = Tag(eq(r"\vec r", cfg.FONT["body"], R_COLOR).set_stroke(cfg.BG, width=1.2), lambda: 0.5 * (base + bead_at(RADII[-1])), LEFT * 0.4)
    hidden(*beads, r_vec, r_lab)
    stage.add_body(*beads)
    stage.add_overlay(r_vec, r_lab)
    law = eq(r"\vec v = \vec\omega \times \vec r", cfg.FONT["title"], cfg.WHITE)
    law_box = boxed(law, cfg.RESULT).move_to([-5.0, 0.9, 0])
    scene.play(FadeOut(flips), *[stage.fade(b, 1.0) for b in beads], run_time=0.8)
    scene.play(stage.fade(r_vec, 1.0), stage.fade(r_lab, 1.0), run_time=0.8)
    scene.play(Write(law), run_time=1.4)
    scene.play(Create(law_box.frame), run_time=0.6)

    # --- 5. Direction: tangent ----------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    def v_of(r: float) -> np.ndarray:
        p = bead_at(r)
        return np.cross(np.array([0.0, w.value, 0.0]), np.array([p[0], 0.0, p[2]]))

    v_arrows = [Vector(lambda r=r: bead_at(r), lambda r=r: bead_at(r) + v_of(r) * V_SCALE * 1.6, cfg.VELOCITY, width=0.08,
                       tip=0.26) for r in RADII]
    rings = [Curve(np.array([[r * np.sin(a), 0.19, r * np.cos(a)] for a in np.linspace(0, 2 * np.pi, 60)]), cfg.MUTED,
                   width=2, opacity=0.6, glow=False) for r in RADII]
    for ring in rings:
        ring.bias = 40.0
    hidden(*v_arrows[-1:], *rings)
    stage.add_body(*rings)
    stage.add_overlay(v_arrows[-1])
    scene.play(stage.fade(v_arrows[-1], 1.0), *[stage.fade(r, 1.0) for r in rings], run_time=1.0)
    tangent = caption("tangent to the bead's circle", cfg.VELOCITY)
    scene.play(FadeIn(tangent), run_time=0.7)

    # --- 6. Size: omega r_perp ------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    r_perp = Segment(lambda: np.array([0.0, 0.2, 0.0]), lambda: bead_at(RADII[-1]), R_COLOR, width=4, opacity=1.0,
                     dashed=True)
    r_perp.bias = 45.0
    rp_lab = Tag(eq(r"r_\perp", cfg.FONT["body"], R_COLOR).set_stroke(cfg.BG, width=1.2), lambda: 0.5 * bead_at(RADII[-1]) + np.array([0, 0.1, 0]),
                 UP * 0.45)
    hidden(r_perp, rp_lab)
    stage.add_body(r_perp)
    stage.add_overlay(rp_lab)
    size = eq(r"|\vec v| = \omega\, r_\perp", cfg.FONT["section"], cfg.VELOCITY).next_to(law_box, DOWN, buff=0.45)
    scene.play(stage.fade(r_perp, 1.0), stage.fade(rp_lab, 1.0), FadeOut(tangent), run_time=1.0)
    scene.play(Write(size), run_time=1.2)
    ep2 = txt("Episode 02: v = r ω", cfg.FONT["small"], cfg.MUTED).next_to(size, DOWN, buff=0.25)
    scene.play(FadeIn(ep2), run_time=0.6)

    # --- 7. Same omega, different v -------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    hidden(*v_arrows[:-1])
    stage.add_overlay(*v_arrows[:-1])
    scene.play(*[stage.fade(v, 1.0) for v in v_arrows[:-1]], stage.fade(r_vec, 0.0), stage.fade(r_lab, 0.0), run_time=1.0)
    ratio_key = eq(r"r:2r:3r\quad\Rightarrow\quad v:2v:3v", cfg.FONT["body"], cfg.VELOCITY)
    fit_width(ratio_key, 7.0)
    ratio_key.move_to([3.8, 3.0, 0])
    scene.play(FadeIn(ratio_key), stage.fade(omega_lab, 0.0), stage.fade(r_perp, 0.0), stage.fade(rp_lab, 0.0), run_time=0.8)
    twice = caption("same ω · speed proportional to radius", cfg.WHITE)
    scene.play(FadeIn(twice), *stage.turn(yaw=-0.1, pitch=0.62), run_time=2.4)

    # --- 8. Cross product links position, velocity and rotation --------------------------------------------------------------------------
    beat(scene, t, 7)
    nxt = VGroup(eq(r"\vec v = \vec\omega\times\vec r", cfg.FONT["body"], cfg.VELOCITY),
                 txt("next:", cfg.FONT["small"], cfg.MUTED),
                 eq(r"\vec\tau = \vec r\times\vec F", cfg.FONT["body"], cfg.TORQUE)).arrange(RIGHT, buff=0.4)
    nxt.move_to([3.6, 3.1, 0])
    scene.play(FadeOut(twice), fade_through(ratio_key, nxt), run_time=1.0)
    finish(scene, t, stage)
