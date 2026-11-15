"""Scene 24 — angular momentum. On a 3D floor a particle glides in a straight
line past an origin O: teal r, gold p and the rose L = r x p standing up from
O. The dashed lever arm d_perp is the same at every instant, so the live
|L| readout never changes. The particle then circles O: L = m r v =
m r^2 omega. A disc spins with omega and L = I omega together on its axis.
A tilted dumbbell turning about a vertical axle shows the general case: its
L (computed as the sum of m r x v) sweeps round the axle while omega stays
put; only the component along the axle equals I omega. tau = dL/dt and
tau = I alpha close the scene.
"""

from manim_scenes.common import *

M = 1.0                       # an illustrative particle (no numbers are spoken here)
P_SCALE = 0.6
L_SCALE = 0.35


class Scene24AngularMomentum(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "24", "Angular momentum")
    stage = Stage((1.4, -1.5, 0.0), zoom=1.22, yaw=-0.45, pitch=0.5, sway=0.02)
    floor(stage, 0.0, reach=6.0, opacity=0.22)
    O = np.array([0.0, 0.25, 0.0])               # the origin sits at the particle's height
    s = Knob(-3.2)                                 # position along the straight path
    path_z, speed = 1.6, 1.4

    def particle() -> np.ndarray:
        return np.array([s.value, 0.25, path_z])

    def momentum() -> np.ndarray:
        return M * np.array([speed, 0.0, 0.0])

    def L_vec() -> np.ndarray:
        return np.cross(particle() - O, momentum())

    ball = Ball(particle, 0.2, cfg.BALL)
    o_mark = Tag(VGroup(glow_dot(ORIGIN, cfg.WHITE, 0.08), eq("O", cfg.FONT["label"], cfg.WHITE).shift(DL * 0.35)), O)
    track = Segment(np.array([-4.5, 0.03, path_z]), np.array([4.5, 0.03, path_z]), cfg.MUTED, width=2.5, opacity=0.6, dashed=True)
    stage.add_body(track, ball)
    stage.add_overlay(o_mark)
    show(scene, stage, 1.0)
    q = eq(r"p = m v\ \longrightarrow\ ?", cfg.FONT["section"], cfg.MOMENTUM).move_to([-4.4, 3.0, 0])
    scene.play(FadeIn(q), s.to(stage, -2.4, rate_func=linear), run_time=1.6)

    # --- 2. L = r x p -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    r_vec = Vector(lambda: O, particle, cfg.POSITION, width=0.06, tip=0.22)
    p_vec = Vector(particle, lambda: particle() + momentum() * P_SCALE, cfg.MOMENTUM, width=0.07, tip=0.24)
    L_arrow = Vector(lambda: O, lambda: O + L_vec() * L_SCALE, cfg.ANG_MOMENTUM, width=0.1, tip=0.3)
    labs = [Tag(eq(r"\vec r", cfg.FONT["body"], cfg.POSITION), lambda: 0.5 * (O + particle()), UL * 0.35),
            Tag(eq(r"\vec p", cfg.FONT["body"], cfg.MOMENTUM), lambda: particle() + momentum() * P_SCALE, UP * 0.4),
            Tag(eq(r"\vec L", cfg.FONT["section"], cfg.ANG_MOMENTUM), lambda: O + L_vec() * L_SCALE, RIGHT * 0.5)]
    hidden(r_vec, p_vec, L_arrow, *labs)
    stage.add_overlay(r_vec, p_vec, L_arrow, *labs)
    law = eq(r"\vec L = \vec r \times \vec p", cfg.FONT["title"], cfg.ANG_MOMENTUM).move_to([-4.3, 3.0, 0])
    scene.play(stage.fade(r_vec, 1.0), stage.fade(p_vec, 1.0), stage.fade(labs[0], 1.0), stage.fade(labs[1], 1.0),
               fade_through(q, law), run_time=1.2)
    scene.play(stage.fade(L_arrow, 1.0), stage.fade(labs[2], 1.0), run_time=1.0)

    # --- 3. |L| = r p sin theta = p d_perp ----------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    foot = np.array([0.0, 0.25, path_z])
    lever = Segment(O, foot, cfg.POSITION, width=5, opacity=1.0, dashed=True)
    lever.bias = 3.0
    lever_lab = Tag(eq(r"d_\perp", cfg.FONT["body"], cfg.POSITION), 0.5 * (O + foot), RIGHT * 1.35 + DOWN * 0.6)
    hidden(lever, lever_lab)
    stage.add_body(lever)
    stage.add_overlay(lever_lab)
    mag = eq(r"L = r p \sin\theta = p\, d_\perp", cfg.FONT["section"], cfg.WHITE).next_to(law, DOWN, buff=0.35)
    scene.play(Write(mag), stage.fade(lever, 1.0), stage.fade(lever_lab, 1.0), run_time=1.6)

    # --- 4. A straight line: L is constant -----------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    live = readout(r"|\vec L| =", lambda: float(np.linalg.norm(L_vec())), 2, "", cfg.ANG_MOMENTUM, size=48).move_to([4.6, 3.0, 0])
    scene.play(FadeIn(live), run_time=0.6)
    scene.play(*[stage.fade(lab, 0.0) for lab in labs[:2]], run_time=0.5)
    scene.play(s.to(stage, 3.2, rate_func=linear), run_time=7.0)
    same = caption("zero net force · constant L", cfg.ANG_MOMENTUM)
    scene.play(FadeIn(same), run_time=0.7)

    # --- 5. A circle: L = m r v = m r^2 omega -------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(*[stage.fade(x, 0.0) for x in (ball, r_vec, p_vec, L_arrow, *labs, lever, lever_lab, track)], FadeOut(live),
               FadeOut(same), FadeOut(mag), run_time=0.8)
    phase = Knob(0.0)
    radius = 1.9
    drive(stage, phase, speed / radius)

    def on_circle() -> np.ndarray:
        return O + radius * np.array([np.sin(phase.value), 0.0, np.cos(phase.value)])

    def tangent() -> np.ndarray:
        return np.array([np.cos(phase.value), 0.0, -np.sin(phase.value)])

    ring_path = Curve(np.array([O + radius * np.array([np.sin(a), 0.0, np.cos(a)]) for a in np.linspace(0, 2 * np.pi, 60)]),
                      cfg.MUTED, width=2.5, opacity=0.6, glow=False)
    ball2 = Ball(on_circle, 0.2, cfg.BALL)
    r2 = Vector(lambda: O, on_circle, cfg.POSITION, width=0.06, tip=0.22)
    p2 = Vector(on_circle, lambda: on_circle() + tangent() * speed * P_SCALE, cfg.MOMENTUM, width=0.07, tip=0.24)
    L2 = Vector(lambda: O, lambda: O + np.cross(on_circle() - O, tangent() * speed) * L_SCALE, cfg.ANG_MOMENTUM, width=0.1,
                tip=0.3)
    hidden(ring_path, ball2, r2, p2, L2)
    stage.add_body(ring_path, ball2)
    stage.add_overlay(r2, p2, L2)
    scene.play(*[stage.fade(x, 1.0) for x in (ring_path, ball2, r2, p2, L2)], run_time=1.0)
    circle_eqs = VGroup(eq(r"L = m r v", cfg.FONT["section"], cfg.ANG_MOMENTUM),
                        eq(r"v = r\omega\ \Rightarrow\ L = m r^2 \omega", cfg.FONT["section"], cfg.ANG_MOMENTUM))
    circle_eqs.arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(law, DOWN, buff=0.35).align_to(law, LEFT)
    perp = caption("on a circle, v is perpendicular to r", cfg.WHITE)
    scene.play(FadeIn(perp), Write(circle_eqs[0]), run_time=1.4)
    scene.play(Write(circle_eqs[1]), run_time=1.6)

    # --- 6. A rigid body: L = I omega along the axis ------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(*[stage.fade(x, 0.0) for x in (ring_path, ball2, r2, p2, L2)], FadeOut(perp), FadeOut(circle_eqs), run_time=0.8)
    spin = Knob(0.0)
    drive(stage, spin, 1.3)
    disc = Drum(np.array([0, 0.5, 0]), 1.8, 0.1, cfg.DISC_BODY, axis=(0, 1, 0), spin=lambda: spin.value, stripe=cfg.DISC_STRIPE,
                sectors=8)
    w_vec = Vector(np.array([0.08, 0.62, 0]), np.array([0.08, 2.0, 0]), cfg.OMEGA, width=0.07, tip=0.24)
    L_disc = Vector(np.array([-0.08, 0.62, 0]), np.array([-0.08, 2.9, 0]), cfg.ANG_MOMENTUM, width=0.1, tip=0.3)
    disc_labs = [Tag(eq(r"\vec\omega", cfg.FONT["body"], cfg.OMEGA), np.array([0.1, 2.0, 0]), RIGHT * 0.45),
                 Tag(eq(r"\vec L", cfg.FONT["body"], cfg.ANG_MOMENTUM), np.array([-0.1, 2.9, 0]), LEFT * 0.45)]
    hidden(disc, w_vec, L_disc, *disc_labs)
    stage.add_body(disc)
    stage.add_overlay(w_vec, L_disc, *disc_labs)
    scene.play(stage.fade(disc, 1.0), run_time=0.8)
    scene.play(*[stage.fade(x, 1.0) for x in (w_vec, L_disc, *disc_labs)], run_time=1.0)
    rigid = eq(r"\vec L = I\,\vec\omega", cfg.FONT["title"], cfg.ANG_MOMENTUM)
    rigid_box = boxed(rigid, cfg.RESULT).next_to(law, DOWN, buff=0.4).align_to(law, LEFT)
    sym = txt("fixed symmetry axis", cfg.FONT["small"], cfg.MUTED).next_to(rigid_box, DOWN, buff=0.15)
    scene.play(Write(rigid), FadeIn(sym), run_time=1.4)
    scene.play(Create(rigid_box.frame), run_time=0.6)

    # --- 7. General body: only the axial component is I omega ---------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(*[stage.fade(x, 0.0) for x in (disc, w_vec, L_disc, *disc_labs)], run_time=0.7)
    tilt = 0.6
    arm = 1.6
    centre = np.array([0.0, 1.2, 0.0])

    def masses_at():
        R = mu.rotation_y(spin.value)
        d = np.array([np.sin(tilt), np.cos(tilt), 0.0]) * arm
        return [centre + R @ d, centre - R @ d]

    def L_general() -> np.ndarray:
        w = np.array([0.0, 1.3, 0.0])
        return sum(np.cross(p - centre, np.cross(w, p - centre)) for p in masses_at())

    beads = [Ball(lambda k=k: masses_at()[k], 0.28, cfg.MASS) for k in range(2)]
    tips = [Ball(lambda k=k: masses_at()[k], 0.02, cfg.STEEL, layers=3) for k in range(2)]
    stick = Rod(tips[0], tips[1], width=8, dark="#4A5A68", light="#DCE6EE")
    axle = Segment(centre - np.array([0, 2.0, 0]), centre + np.array([0, 2.4, 0]), cfg.OMEGA, width=3, opacity=0.9, dashed=True)
    w_gen = Vector(centre, centre + np.array([0, 1.5, 0]), cfg.OMEGA, width=0.07, tip=0.24)
    L_gen = Vector(lambda: centre, lambda: centre + L_general() * 0.35, cfg.ANG_MOMENTUM, width=0.1, tip=0.3)
    L_axial = Segment(lambda: centre + np.array([0, (L_general() * 0.35)[1], 0]), lambda: centre + L_general() * 0.35,
                      cfg.ANG_MOMENTUM, width=2.5, opacity=0.8, dashed=True)
    gen_items = [axle, stick, *tips, *beads, L_axial]
    hidden(*gen_items, w_gen, L_gen)
    stage.add_body(*gen_items)
    stage.add_overlay(w_gen, L_gen)
    scene.play(*[stage.fade(x, 1.0) for x in gen_items + [w_gen, L_gen]], run_time=1.0)
    general = eq(r"L_{\parallel} = I_{\parallel}\,\omega", cfg.FONT["section"], cfg.ANG_MOMENTUM)
    general.next_to(sym, DOWN, buff=0.35).align_to(law, LEFT)
    tilt_note = caption("general axis: L need not be parallel to ω", cfg.ANG_MOMENTUM,
                        cfg.FONT["small"])
    scene.play(Write(general), FadeIn(tilt_note), run_time=1.4)

    # --- 8. tau = dL/dt -------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(*[stage.fade(x, 0.0) for x in gen_items + [w_gen, L_gen]], FadeOut(tilt_note),
               FadeOut(VGroup(rigid_box, rigid, sym, general)), FadeOut(law), stage.fade(o_mark, 0.0), run_time=0.8)
    big = eq(r"\vec\tau_{\text{ext}} = {d\vec L \over dt}", cfg.FONT["hero"], cfg.WHITE)
    big_box = boxed(big, cfg.RESULT).move_to(UP * 0.6)
    origin_note = txt("fixed inertial origin O", cfg.FONT["small"], cfg.MUTED).next_to(big_box, UP, buff=0.35)
    scene.play(Write(big), FadeIn(origin_note), run_time=1.6)
    scene.play(Create(big_box.frame), run_time=0.7)

    # --- 9. With I constant: tau = I alpha ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    special = eq(r"I\ \text{constant}:\quad {dL \over dt} = I\,\alpha \ \Rightarrow\ \tau = I\,\alpha", cfg.FONT["section"],
                 cfg.TORQUE).next_to(big_box, DOWN, buff=0.5)
    fit_width(special, 13.0)
    scene.play(Write(special), run_time=1.8)

    # --- 10. Force changes p; torque changes L -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    pair = VGroup(txt("force changes p", cfg.FONT["body"], cfg.FORCE), txt("torque changes L", cfg.FONT["body"], cfg.TORQUE))
    pair.arrange(RIGHT, buff=1.4).move_to(DOWN * 3.6)
    scene.play(FadeIn(pair, lag_ratio=0.3), run_time=1.0)
    finish(scene, t, stage)
