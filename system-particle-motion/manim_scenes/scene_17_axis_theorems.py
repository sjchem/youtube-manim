"""Scene 17 — two axis theorems. A uniform rod turns about a cyan axis
through its centre; a white parallel axis appears a distance d away and the
parallel-axis theorem I = I_cm + M d^2 is written. The axis slides to the
rod's end while a live readout of I / M L^2 climbs from 1/12 to 1/3, and the
steps 1/12 + 1/4 = 1/3 follow. A small plot of I against the axis position
is a parabola with its minimum at the centre of mass. Then a flat disc with
x, y and z axes: I_z = I_x + I_y, so each diameter carries 1/4 M R^2 — the
disc flips about a diameter, then spins about z.
"""

from manim_scenes.common import *

ROD_L = 3.6
AX = pm.AXES


class Scene17AxisTheorems(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "17", "Two axis theorems")
    stage = Stage((-3.6, -0.8, 0.0), zoom=0.95, yaw=-0.2, pitch=0.42, sway=0.02)
    spin, offset = Knob(0.0), Knob(0.0)          # offset: axis position along the rod, in units of L
    drive(stage, spin, 0.8)

    def end(s: float) -> np.ndarray:
        along = mu.rotation_y(spin.value) @ np.array([1.0, 0.0, 0.0])
        pivot = np.array([0.0, 0.0, 0.0])
        return pivot + along * ROD_L * (s - offset.value)

    a, b = Ball(lambda: end(-0.5), 0.08, cfg.STEEL, layers=6), Ball(lambda: end(0.5), 0.08, cfg.STEEL, layers=6)
    rod = Rod(a, b, width=22, dark="#2E5873", light="#BFE3F7")
    turning_axis = axis_line(stage, [0, -1.5, 0], [0, 1.6, 0], cfg.ANGLE, 0.95, 4)
    centre_mark = com_tag(lambda: end(0.0), 0.16)
    stage.add_body(a, b, rod)
    stage.add_overlay(centre_mark)
    show(scene, stage, 1.0)
    hard = caption("reuse a known moment of inertia", cfg.MUTED)
    scene.play(FadeIn(hard), run_time=0.7)

    # --- 2. Parallel axis ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    parallel = eq(r"\text{parallel axis theorem}", cfg.FONT["body"], cfg.WHITE).move_to([4.3, 3.2, 0])
    d_demo = 1.6
    other = Segment(np.array([d_demo, -1.5, 0.0]), np.array([d_demo, 1.6, 0.0]), cfg.WHITE, width=3.5, opacity=0.9, dashed=True)
    gap = Segment(np.array([0.0, 1.45, 0.0]), np.array([d_demo, 1.45, 0.0]), cfg.POSITION, width=5, opacity=1.0)
    gap_lab = Tag(eq("d", cfg.FONT["section"], cfg.POSITION), np.array([d_demo / 2, 1.45, 0.0]), UP * 0.4)
    hidden(other, gap, gap_lab)
    stage.add_body(other, gap)
    stage.add_overlay(gap_lab)
    scene.play(FadeOut(hard), FadeIn(parallel), run_time=0.8)
    scene.play(stage.fade(other, 1.0), run_time=0.8)
    scene.play(stage.fade(gap, 1.0), stage.fade(gap_lab, 1.0), run_time=0.8)

    # --- 3. I = I_cm + M d^2 ------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    law = eq(r"I = I_{\mathrm{cm}} + M d^2", cfg.FONT["title"], cfg.WHITE)
    law_box = boxed(law, cfg.RESULT).move_to([4.3, 2.0, 0])
    scene.play(Write(law), run_time=1.4)
    scene.play(Create(law_box.frame), run_time=0.6)

    # --- 4. The rod: about the centre, then slide to the end -----------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(stage.fade(other, 0.0), stage.fade(gap, 0.0), stage.fade(gap_lab, 0.0), run_time=0.6)
    live = readout(r"I / ML^2 =", lambda: pm.rod_inertia_about(offset.value), 3, "", cfg.INERTIA, size=46)
    live.move_to([4.3, 0.4, 0])
    centre_case = eq(rf"I_{{\mathrm{{cm}}}} = {ftex(AX.rod_cm)}\,ML^2", cfg.FONT["section"], cfg.INERTIA).move_to([4.3, -0.7, 0])
    scene.play(FadeIn(live), Write(centre_case), run_time=1.2)
    scene.play(offset.to(stage, -0.5), run_time=3.0)
    end_note = eq(r"d = {L \over 2}", cfg.FONT["section"], cfg.POSITION).move_to([4.3, -2.1, 0])
    scene.play(FadeIn(end_note), run_time=0.7)

    # --- 5. 1/12 + 1/4 = 1/3 -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    steps = VGroup(
        eq(rf"I_{{\text{{end}}}} = {ftex(AX.rod_cm)}ML^2 + M\left({{L \over 2}}\right)^2", cfg.FONT["body"]),
        eq(rf"= \left({ftex(AX.rod_cm)} + {ftex(AX.shift)}\right) ML^2 = {ftex(AX.rod_end)}\,ML^2", cfg.FONT["body"]),
    ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    fit_width(steps, 7.4)
    steps.move_to([3.8, -1.75, 0])
    scene.play(FadeOut(centre_case), FadeOut(end_note), run_time=0.5)
    scene.play(Write(steps[0]), run_time=1.8)
    scene.play(Write(steps[1]), run_time=1.8)
    result = glow_frame(steps[1], cfg.RESULT)
    table = caption("just as the table said", cfg.RESULT)
    scene.play(Create(result), FadeIn(table), run_time=0.8)

    # --- 6. The centre-of-mass axis gives the smallest I ----------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(steps), FadeOut(result), FadeOut(table), run_time=0.6)
    plot = plot_axes((-0.6, 0.6), (0, 0.45), x_length=4.4, y_length=2.0, at=[4.0, -1.85, 0], x_label="d/L", y_label="I/ML^2",
                     label_size=30)
    curve = curve_on(plot, pm.rod_inertia_about, -0.5, 0.5, cfg.INERTIA)
    dot = glow_dot(plot.c2p(-0.5, pm.rod_inertia_about(-0.5)), cfg.WHITE, 0.08)
    dot.add_updater(lambda m: m.move_to(plot.c2p(offset.value, pm.rod_inertia_about(offset.value))))
    scene.play(FadeIn(plot), Create(curve), FadeIn(dot), run_time=1.2)
    scene.play(offset.to(stage, 0.0), run_time=2.2)
    smallest = caption("COM axis: minimum I among parallel axes", cfg.BALANCED)
    scene.play(FadeIn(smallest), run_time=0.6)
    scene.play(offset.to(stage, 0.35, rate_func=there_and_back), run_time=2.2)

    # --- 7. Perpendicular axis theorem: planar bodies only -----------------------------------------------------------------------------------------
    beat(scene, t, 6)
    dot.clear_updaters()
    hide(scene, stage, 0.7, FadeOut(VGroup(plot, curve, dot, live, smallest, parallel)),
         VGroup(law_box, law).animate.scale(0.6).move_to([-5.4, 3.3, 0]))
    perp = eq(r"\text{perpendicular axis theorem}", cfg.FONT["body"], cfg.WHITE).move_to([4.0, 3.2, 0])
    flat = txt("flat, planar bodies only", cfg.FONT["small"], cfg.WARNING).next_to(perp, DOWN, buff=0.18)
    scene.play(FadeIn(perp), FadeIn(flat), run_time=0.9)

    # --- 8. I_z = I_x + I_y ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    stage2 = Stage((-3.3, -0.8, 0.0), zoom=1.3, yaw=-0.55, pitch=0.5, sway=0.02)
    flip, twirl = Knob(0.0), Knob(0.0)
    lamina = Drum(ORIGIN, 1.8, 0.04, cfg.DISC_BODY, pose=lambda: mu.rotation_x(flip.value) @ mu.rotation_x(-np.pi / 2),
                  spin=lambda: twirl.value, stripe=cfg.DISC_STRIPE, sectors=8)
    stage2.add_body(lamina)
    axes3 = []
    for d, color, name in ((np.array([1, 0, 0]), cfg.X_COLOR, "x"), (np.array([0, 0, 1]), cfg.Y_COLOR, "y"),
                           (np.array([0, 1, 0]), cfg.Z_COLOR, "z")):
        seg = Segment(-d * 2.6, d * 2.6, color, width=3.5, opacity=0.95)
        seg.bias = 50
        lab = Tag(eq(name, cfg.FONT["section"], color), d * 2.95)
        axes3 += [seg, lab]
        stage2.add_body(seg)
        stage2.add_overlay(lab)
    show(scene, stage2, 1.0)
    perp_law = eq(r"I_z = I_x + I_y", cfg.FONT["title"], cfg.WHITE)
    perp_box = boxed(perp_law, cfg.RESULT).move_to([4.2, 1.6, 0])
    scene.play(Write(perp_law), run_time=1.2)
    scene.play(Create(perp_box.frame), run_time=0.6)

    # --- 9. The disc: 1/2 about z, 1/4 about each diameter ----------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    rows = VGroup(eq(rf"I_z = {ftex(AX.disc_z)}\,MR^2", cfg.FONT["body"], cfg.Z_COLOR),
                  eq(r"I_x = I_y", cfg.FONT["body"], cfg.WHITE),
                  eq(rf"I_x = I_y = {ftex(AX.disc_diameter)}\,MR^2", cfg.FONT["section"], cfg.RESULT)).arrange(DOWN, buff=0.3)
    rows.move_to([4.2, -1.4, 0])
    scene.play(Write(rows[0]), twirl.to(stage2, 2 * np.pi, rate_func=smooth), run_time=2.0)
    scene.play(Write(rows[1]), run_time=1.0)
    scene.play(flip.to(stage2, 2 * np.pi, rate_func=smooth), run_time=2.6)
    scene.play(Write(rows[2]), run_time=1.2)
    scene.play(Create(glow_frame(rows[2], cfg.RESULT)), run_time=0.6)

    # --- 10. Depends on the axis ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    lesson = caption("moment of inertia depends on the axis you choose", cfg.ANGLE)
    scene.play(FadeIn(lesson), run_time=0.8)
    finish(scene, t, stage2, fill=lambda sec: [twirl.to(stage2, 2 * np.pi + sec * 1.2, rate_func=linear)])
