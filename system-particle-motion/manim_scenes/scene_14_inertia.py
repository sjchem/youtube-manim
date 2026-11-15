"""Scene 14 — why mass isn't enough. Two crates on 3D ice take the same push;
the heavier one picks up speed more slowly. Then a copper ring and a blue
disc of equal mass and radius take the same purple torque: the disc spins up
twice as fast (alpha = tau / I from the model). Dots show where each one's
mass sits. I = sum m r_perp^2 is written, with the integral and the unit; the
square is highlighted. A dumbbell (two 1 kg beads on a light rod) has
I = 2 kg m^2 at 1 m and 8 kg m^2 at 2 m; side by side under the same torque,
the spread-out one spins up four times more slowly.
"""

from manim_scenes.common import *

B = pm.DUMBBELL
S = 1.3                         # screen units per metre (dumbbell)
R_BODY = 1.45                   # ring / disc radius on screen
SPIN_T = 4.0


class Scene14Inertia(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "14", "Why mass isn't enough")
    stage = Stage((0.0, -1.9, 0.0), zoom=1.1, yaw=-0.15, pitch=0.35, sway=0.02)
    ice = floor(stage, 0.0, reach=7.0, opacity=0.2)
    clock = Knob(0.0)
    light = Block(lambda: np.array([-4.5 + 0.5 * 1.2 * clock.value ** 2, 0.35, -1.0]), (0.7, 0.7, 0.7), "#C98A4B")
    heavy = Block(lambda: np.array([-4.5 + 0.5 * 0.4 * clock.value ** 2, 0.55, 1.2]), (1.1, 1.1, 1.1), "#8A5A3C")
    pushes = [Vector(lambda: np.array([-4.5 + 0.5 * a * clock.value ** 2 - w / 2 - 1.2, y, z]),
                     lambda: np.array([-4.5 + 0.5 * a * clock.value ** 2 - w / 2, y, z]), cfg.FORCE, width=0.1, tip=0.3)
              for a, w, y, z in ((1.2, 0.7, 0.35, -1.0), (0.4, 1.1, 0.55, 1.2))]
    stage.add_body(light, heavy)
    stage.add_overlay(*pushes)
    show(scene, stage, 1.0)
    tags = [Tag(txt(s, cfg.FONT["label"], cfg.MASS), lambda b=b: b.centre(), UP * 0.9) for b, s in ((light, "m"), (heavy, "3m"))]
    stage.add_overlay(*tags)
    scene.play(clock.to(stage, 3.0, rate_func=linear), run_time=3.0)
    lin = eq(r"a = {F \over m}", cfg.FONT["section"], cfg.WHITE).move_to([4.6, 2.8, 0])
    scene.play(Write(lin), run_time=1.0)

    # --- 2. A ring and a disc: same mass, same radius ----------------------------------------------------------
    beat(scene, t, 1)
    hide(scene, stage, 0.7, FadeOut(lin))
    stage = Stage((0.0, -0.5, 0.0), zoom=1.3, yaw=-0.12, pitch=0.18, sway=0.02)
    ang_r, ang_d = Knob(0.0), Knob(0.0)
    ring_c, disc_c = np.array([-3.0, 0.0, 0.0]), np.array([3.0, 0.0, 0.0])
    ring = Hoop(ring_c, R_BODY, cfg.RING_BODY, spin=lambda: ang_r.value, width=20, stripes=4)
    disc = Drum(disc_c, R_BODY, 0.1, cfg.DISC_BODY, spin=lambda: ang_d.value, stripe=cfg.DISC_STRIPE, sectors=8)
    hub_r = Ball(ring_c, 0.1, cfg.STEEL, layers=8)
    spokes = []
    for k in range(4):
        tip_ball = Ball(lambda k=k: ring.point(k * np.pi / 2), 0.03, cfg.RING_BODY, layers=4)
        spokes += [tip_ball, Rod(hub_r, tip_ball, width=3, dark="#5A4030", light="#C9A27E")]
    stage.add_body(*spokes, ring, hub_r, disc)
    show(scene, stage, 1.0)
    same = VGroup(txt("ring", cfg.FONT["label"], cfg.RING_BODY).move_to([-3.9, -2.75, 0]),
                  txt("disc", cfg.FONT["label"], cfg.DISC_STRIPE).move_to([3.9, -2.75, 0]),
                  txt("same M, same R", cfg.FONT["body"], cfg.WHITE).move_to([0, 3.0, 0]))
    scene.play(FadeIn(same, lag_ratio=0.2), run_time=1.2)

    # --- 3. Same torque: the disc spins up faster -------------------------------------------------------------------------
    beat(scene, t, 2)
    taus = [turn_arrow(stage.screen_point(c) + DOWN * 0.0, R_BODY * 1.3 + 0.35, np.radians(60), np.radians(80), cfg.TORQUE,
                       width=8) for c in (ring_c, disc_c)]
    tau_tags = [eq(r"\tau", cfg.FONT["section"], cfg.TORQUE).move_to(stage.screen_point(c) + UP * 2.25 + LEFT * 0.4)
                for c in (ring_c, disc_c)]
    scene.play(*[FadeIn(a) for a in taus], *[FadeIn(x) for x in tau_tags], run_time=0.8)
    # alpha = tau / I with I_ring = M R^2 and I_disc = M R^2 / 2: the disc gets twice the angular acceleration.
    a_ring = 1.0
    a_disc = a_ring * float(pm.shape("ring").coefficient / pm.shape("disc").coefficient)
    s = Knob(0.0)
    holder = Dot(radius=0.001, fill_opacity=0)
    holder.add_updater(lambda m: (setattr(ang_r, "value", 0.5 * a_ring * s.value ** 2),
                                  setattr(ang_d, "value", 0.5 * a_disc * s.value ** 2)))
    scene.add(holder)
    scene.play(s.to(stage, SPIN_T, rate_func=linear), run_time=SPIN_T)
    faster = caption("same torque · faster disc spin-up", cfg.WHITE)
    scene.play(FadeIn(faster), run_time=0.6)

    # --- 4. Where the mass sits ------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    holder.clear_updaters()
    scene.play(*[FadeOut(a) for a in taus + tau_tags], run_time=0.5)
    ring_pts = np.array([ring_c + R_BODY * np.array([np.cos(a), np.sin(a), 0.12]) for a in np.linspace(0, 2 * np.pi, 28, endpoint=False)])
    rng = np.random.default_rng(cfg.SEED + 14)
    rr = np.sqrt(rng.random(70)) * R_BODY * 0.97
    aa = rng.random(70) * 2 * np.pi
    disc_pts = np.column_stack([disc_c[0] + rr * np.cos(aa), rr * np.sin(aa), np.full(70, 0.16)])
    dots = [Dots(ring_pts, cfg.GOLD, radius=0.07), Dots(disc_pts, cfg.GOLD, radius=0.07)]
    for d in dots:
        d.bias = 5.0
    hidden(*dots)
    stage.add_body(*dots)
    scene.play(*[stage.fade(d, 1.0) for d in dots], FadeOut(faster), run_time=1.0)
    where = caption("ring: all at the rim. disc: much of it near the axis", cfg.GOLD)
    scene.play(FadeIn(where), run_time=0.7)

    # --- 5. I = sum m r_perp^2 ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    hide(scene, stage, 0.8, FadeOut(same), FadeOut(where))
    law = eq([r"I", "=", r"\sum_i m_i\, ", r"r_{i\perp}^2"], cfg.FONT["hero"] * 0.85, cfg.WHITE)
    law[0].set_color(cfg.INERTIA)
    law[3].set_color(cfg.POSITION)
    law_box = boxed(law, cfg.RESULT).move_to([0, 2.0, 0])
    name = txt("moment of inertia", cfg.FONT["body"], cfg.INERTIA).next_to(law_box, UP, buff=0.35)
    scene.play(FadeIn(name, shift=DOWN * 0.1), Write(law), run_time=1.8)
    scene.play(Create(law_box.frame), run_time=0.7)

    # --- 6. r_perp, the integral, the unit ------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    meaning = txt("r⊥: each particle's distance from the axis", cfg.FONT["small"], cfg.POSITION).next_to(law_box, DOWN, buff=0.4)
    integral = eq(r"I = \int r_\perp^2\, dm", cfg.FONT["section"], cfg.WHITE).next_to(meaning, DOWN, buff=0.45)
    unit = eq(r"[I] = \mathrm{kg\,m^2}", cfg.FONT["body"], cfg.INERTIA).next_to(integral, DOWN, buff=0.35)
    scene.play(FadeIn(meaning), run_time=0.8)
    scene.play(Write(integral), run_time=1.4)
    scene.play(FadeIn(unit), run_time=0.8)

    # --- 7. The square ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    square_glow = glow_frame(law[3], cfg.POSITION, buff=0.1)
    scene.play(Create(square_glow), Indicate(law[3], color=cfg.POSITION, scale_factor=1.15), run_time=1.2)
    far = caption("distance from the axis is squared", cfg.POSITION)
    scene.play(FadeIn(far), run_time=0.6)

    # --- 8. Dumbbell at 1 m: I = 2 ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(name, meaning, integral, unit, square_glow, far)),
               VGroup(law_box, law).animate.scale(0.6).move_to([-5.0, 3.2, 0]), run_time=0.9)
    stage = Stage((0.0, -1.5, 0.0), zoom=1.3, yaw=-0.2, pitch=0.3, sway=0.02)
    spin_a, reach_a = Knob(0.0), Knob(B.r_in)
    spin_motor = drive(stage, spin_a, 0.8)

    def dumbbell(stage_: Stage, centre, spin: Knob, reach: Knob):
        centre = np.asarray(centre, dtype=float)
        ends = [Ball(lambda s=s: centre + mu.rotation_y(spin.value) @ np.array([s * reach.value * S, 0, 0]), 0.3, cfg.MASS)
                for s in (-1, 1)]
        hub = Ball(centre, 0.08, cfg.STEEL, layers=8)
        tips = [Ball(lambda s=s: centre + mu.rotation_y(spin.value) @ np.array([s * 2.15 * S, 0, 0]), 0.04, cfg.STEEL, layers=4)
                for s in (-1, 1)]
        rods = [Rod(hub, tp, width=7, dark="#4A5A68", light="#DCE6EE") for tp in tips]
        axis = Segment(centre + np.array([0, -1.3, 0]), centre + np.array([0, 1.6, 0]), cfg.ANGLE, width=3, opacity=0.85,
                       dashed=True)
        stage_.add_body(axis, *tips, *rods, hub, *ends)
        return ends

    ends_a = dumbbell(stage, np.array([0.0, 0.6, 0.0]), spin_a, reach_a)
    show(scene, stage, 1.0)
    kg = [Tag(txt(f"{fx(B.mass)} kg", cfg.FONT["label"], cfg.MASS), lambda e=e: e.where(), UP * 0.9) for e in ends_a]
    stage.add_overlay(*kg)
    I1 = eq(rf"I = {fx(B.mass)}({fx(B.r_in)})^2 + {fx(B.mass)}({fx(B.r_in)})^2 = {fx(B.i_in)}\ \mathrm{{kg\,m^2}}",
            cfg.FONT["section"], cfg.INERTIA)
    fit_width(I1, 13.4)
    I1.move_to(DOWN * 3.5)
    scene.play(Write(I1), run_time=1.8)

    # --- 9. Slide out to 2 m: I = 8 -------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    stage.remove_updater(spin_motor)
    scene.play(spin_a.to(stage, 0.0), run_time=0.7)
    scene.play(reach_a.to(stage, B.r_out), run_time=1.8)
    I2 = eq(rf"I = {fx(B.mass)}({fx(B.r_out)})^2 + {fx(B.mass)}({fx(B.r_out)})^2 = {fx(B.i_out)}\ \mathrm{{kg\,m^2}}",
            cfg.FONT["section"], cfg.INERTIA).move_to(I1)
    fit_width(I2, 13.4)
    scene.play(fade_through(I1, I2), run_time=1.0)

    # --- 10. Four times larger: four times slower to spin up -----------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    hide(scene, stage, 0.7)
    stage = Stage((0.0, -1.3, 0.0), zoom=0.95, yaw=-0.15, pitch=0.3, sway=0.02)
    ang_in, ang_out = Knob(0.0), Knob(0.0)
    dumbbell(stage, np.array([-3.8, 0.6, 0.0]), ang_in, Knob(B.r_in))
    dumbbell(stage, np.array([3.0, 0.6, 0.0]), ang_out, Knob(B.r_out))
    show(scene, stage, 0.8)
    labels = VGroup(eq(rf"I = {fx(B.i_in)}", cfg.FONT["section"], cfg.INERTIA).move_to([-3.6, 2.4, 0]),
                    eq(rf"I = {fx(B.i_out)}", cfg.FONT["section"], cfg.INERTIA).move_to([3.0, 2.4, 0]))
    scene.play(FadeOut(VGroup(I2, law_box, law)), run_time=0.4)
    scene.play(FadeIn(labels), run_time=0.3)
    s2 = Knob(0.0)
    holder2 = Dot(radius=0.001, fill_opacity=0)
    holder2.add_updater(lambda m: (setattr(ang_in, "value", 0.5 * 1.6 * s2.value ** 2),
                                   setattr(ang_out, "value", 0.5 * 1.6 * s2.value ** 2 * B.i_in / B.i_out)))
    scene.add(holder2)
    same_tau = caption(f"same torque: {fx(B.i_out / B.i_in)}× I → ¼ α", cfg.TORQUE,
                       cfg.FONT["body"])
    scene.play(FadeIn(same_tau), run_time=0.6)
    scene.play(s2.to(stage, 5.0, rate_func=linear), run_time=5.0)
    finish(scene, t, stage, fill=lambda sec: [s2.to(stage, 5.0 + sec, rate_func=linear)])
