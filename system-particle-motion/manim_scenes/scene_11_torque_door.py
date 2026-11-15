"""Scene 11 — torque: why doors have handles. A 3D door hangs on a dashed
hinge axis, seen from above and in front. The same green push swings it far
at the handle and barely at the hinge. Then the geometry: teal r from the
axis to the point of push, green F, the purple torque vector up the hinge
axis, the angle theta and a live tau = r F sin(theta) readout. The line of
action extends; the teal lever arm drops perpendicular onto it (tau = F d).
Pushing straight toward the hinge collapses the lever arm: zero torque.
Numbers from the model: 20 N at 0.8 m gives 16 N m, at 0.2 m only 4 N m;
two purple bars compare them.
"""

from manim_scenes.common import *

D = pm.DOOR
S = 3.9                                   # screen units per metre (door width 0.9 m)
HINGE = np.array([-2.6, 0.0, 0.9])
H = 2.6                                   # door height on screen
PUSH_Y = 1.15
F_PER_N = 0.1
TAU_PER_NM = 0.09


class Scene11TorqueDoor(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "11", "Torque: why doors have handles")
    stage = Stage((0.2, -1.6, 0.0), zoom=1.2, yaw=-0.42, pitch=0.62, sway=0.025)
    floor(stage, 0.0, reach=6.0, opacity=0.22, centre=(0.0, 0.0))
    phi = Knob(0.0)                         # door angle
    dist = Knob(D.r_far * S)                # where the push acts, screen units from the axis
    theta = Knob(np.pi / 2)                 # angle between r and F

    def pose() -> np.ndarray:
        return mu.rotation_y(phi.value)

    def along() -> np.ndarray:             # unit vector along the door, away from the hinge
        return pose() @ np.array([1.0, 0.0, 0.0])

    def normal() -> np.ndarray:            # the push direction that opens the door
        return pose() @ np.array([0.0, 0.0, -1.0])

    def P() -> np.ndarray:
        return HINGE + np.array([0, PUSH_Y, 0]) + along() * dist.value

    def F_dir() -> np.ndarray:
        return np.cos(theta.value) * along() + np.sin(theta.value) * normal()

    axis_pt = HINGE + np.array([0, PUSH_Y, 0])
    door = Block(lambda: HINGE + pose() @ np.array([D.width * S / 2, H / 2, 0.0]), (D.width * S, H, 0.1), cfg.WOOD, pose=pose)
    handle = Ball(lambda: HINGE + pose() @ np.array([D.width * S - 0.25, PUSH_Y, -0.1]), 0.09, cfg.GOLD, layers=10)
    wall = Block(HINGE + np.array([-0.9, H / 2 + 0.1, 0.1]), (1.6, H + 0.2, 0.24), "#2C4257")
    hinge_axis = axis_line(stage, HINGE + np.array([0, -0.2, 0]), HINGE + np.array([0, H + 1.3, 0]), cfg.ANGLE, 0.9, 3.5)
    stage.add_body(wall, door, handle)
    push = Vector(lambda: P() - F_dir() * D.force * F_PER_N, P, cfg.FORCE, width=0.11, tip=0.32)
    push.presence = 0.0
    stage.add_overlay(push)
    show(scene, stage, 1.0)
    q = caption("why is the handle far from the hinges?", cfg.WHITE)
    scene.play(FadeIn(q), run_time=0.8)

    # --- 2. Same push: handle vs hinge ----------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(stage.fade(push, 1.0), run_time=0.5)
    scene.play(phi.to(stage, 0.95, rate_func=rate_functions.ease_out_quad), run_time=1.5)
    easy = caption("near the handle: it swings easily", cfg.BALANCED)
    scene.play(fade_through(q, easy), run_time=0.6)
    scene.play(stage.fade(push, 0.0), phi.to(stage, 0.0), run_time=1.0)
    scene.play(dist.to(stage, D.r_near * S), run_time=0.4)
    scene.play(stage.fade(push, 1.0), run_time=0.4)
    scene.play(phi.to(stage, 0.95 * D.r_near / D.r_far, rate_func=rate_functions.ease_out_quad), run_time=1.5)
    barely = caption("near the hinges: it barely moves", cfg.WARNING)
    scene.play(fade_through(easy, barely), run_time=0.6)

    # --- 3. Torque, the turning effect --------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(phi.to(stage, 0.22), dist.to(stage, D.r_far * S), run_time=1.2)
    name = result_label("torque", cfg.TORQUE, cfg.FONT["title"]).move_to([-0.6, 3.15, 0])
    also = txt("(moment of force)", cfg.FONT["small"], cfg.MUTED).next_to(name, RIGHT, buff=0.3)
    scene.play(FadeIn(name, scale=1.1), FadeIn(also), FadeOut(barely), run_time=1.0)

    # --- 4. tau = r x F ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    r_vec = Vector(lambda: axis_pt, P, cfg.POSITION, width=0.07, tip=0.26)
    r_lab = Tag(eq(r"\vec r", cfg.FONT["body"], cfg.POSITION), lambda: 0.5 * (axis_pt + P()), UP * 0.45)
    F_lab = Tag(eq(r"\vec F", cfg.FONT["body"], cfg.FORCE), lambda: P() - F_dir() * D.force * F_PER_N * 0.55, LEFT * 0.45)

    def tau_value() -> float:
        return (dist.value / S) * D.force * np.sin(theta.value)

    tau_base = HINGE + np.array([0, H + 0.15, 0])
    tau_vec = Vector(lambda: tau_base, lambda: tau_base + np.array([0, tau_value() * TAU_PER_NM, 0]), cfg.TORQUE, width=0.1,
                     tip=0.3)
    tau_lab = Tag(eq(r"\vec\tau", cfg.FONT["section"], cfg.TORQUE), lambda: tau_base + np.array([0, tau_value() * TAU_PER_NM, 0]),
                  RIGHT * 0.5)
    hidden(r_vec, r_lab, F_lab, tau_vec, tau_lab)
    stage.add_overlay(r_vec, r_lab, F_lab, tau_vec, tau_lab)
    law = eq(r"\vec\tau = \vec r \times \vec F", cfg.FONT["title"], cfg.TORQUE)
    law.move_to([4.4, 2.3, 0])
    scene.play(stage.fade(r_vec, 1.0), stage.fade(r_lab, 1.0), stage.fade(F_lab, 1.0), run_time=1.0)
    scene.play(Write(law), run_time=1.4)
    scene.play(stage.fade(tau_vec, 1.0), stage.fade(tau_lab, 1.0), run_time=1.0)

    # --- 5. tau = r F sin(theta) ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    arc = Curve(lambda: np.array([P() + 0.55 * (np.cos(a) * along() + np.sin(a) * normal())
                                  for a in np.linspace(0, theta.value, 20)]), cfg.ANGLE, width=4)
    arc.bias = 3.0
    th_lab = Tag(eq(r"\theta", cfg.FONT["body"], cfg.ANGLE),
                 lambda: P() + 0.9 * (np.cos(theta.value / 2) * along() + np.sin(theta.value / 2) * normal()))
    hidden(arc, th_lab)
    stage.add_body(arc)
    stage.add_overlay(th_lab)
    mag = eq(r"\tau = r F \sin\theta", cfg.FONT["section"], cfg.WHITE).next_to(law, DOWN, buff=0.4)
    live = readout(r"\tau =", tau_value, 1, "N m", cfg.TORQUE, size=48).next_to(mag, DOWN, buff=0.35)
    scene.play(Write(mag), stage.fade(arc, 1.0), stage.fade(th_lab, 1.0), run_time=1.2)
    scene.play(FadeIn(live), run_time=0.5)
    scene.play(theta.to(stage, np.radians(40)), run_time=2.0)
    scene.play(theta.to(stage, np.radians(90)), run_time=1.4)

    # --- 6. Line of action and lever arm ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(theta.to(stage, np.radians(55)), run_time=1.2)

    def foot() -> np.ndarray:
        d = F_dir()
        return P() + d * np.dot(axis_pt - P(), d)

    line = Segment(lambda: P() - F_dir() * 4.0, lambda: P() + F_dir() * 1.6, cfg.FORCE, width=3, opacity=0.9, dashed=True)
    arm = Segment(lambda: axis_pt, foot, cfg.POSITION, width=6, opacity=1.0)
    arm.bias = line.bias = 4.0
    arm_lab = Tag(eq(r"d_\perp", cfg.FONT["body"], cfg.POSITION), lambda: 0.5 * (axis_pt + foot()), LEFT * 0.5 + DOWN * 0.2)
    hidden(line, arm, arm_lab)
    stage.add_body(line, arm)
    stage.add_overlay(arm_lab)
    scene.play(stage.fade(line, 1.0), run_time=1.0)
    action = caption("the line of action", cfg.FORCE)
    scene.play(FadeIn(action), run_time=0.6)
    scene.play(stage.fade(arm, 1.0), stage.fade(arm_lab, 1.0), stage.fade(r_lab, 0.0), run_time=1.0)
    lever = eq(r"\tau = F\, d_\perp", cfg.FONT["section"], cfg.POSITION).move_to(mag)
    arm_cap = caption("lever arm: perpendicular distance", cfg.POSITION)
    scene.play(fade_through(action, arm_cap), fade_through(mag, lever), run_time=1.2)
    scene.play(*stage.turn(yaw=-0.2, pitch=0.85), run_time=2.5)

    # --- 7. Push toward the hinge: no torque ---------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(arm_cap), run_time=0.4)
    scene.play(theta.to(stage, np.pi), run_time=2.4)
    none = caption("through hinge: lever arm zero · torque zero", cfg.WARNING)
    scene.play(FadeIn(none), Indicate(live, color=cfg.WARNING), run_time=1.2)
    scene.play(phi.to(stage, 0.22), run_time=1.5)

    # --- 8. 20 N at 0.8 m: 16 N m ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(theta.to(stage, np.pi / 2), stage.fade(line, 0.0), stage.fade(arm, 0.0), stage.fade(arm_lab, 0.0),
               stage.fade(arc, 0.0), stage.fade(th_lab, 0.0), FadeOut(none), *stage.turn(yaw=-0.42, pitch=0.62), run_time=1.4)
    far = eq(rf"\tau = {fx(D.force)} \times {fx(D.r_far, 1)} = {fx(D.tau_far)}\ \mathrm{{N\,m}}", cfg.FONT["section"],
             cfg.TORQUE)
    far.move_to([-1.6, -3.55, 0])
    meters = Tag(txt(f"{fx(D.r_far, 1)} m", cfg.FONT["label"], cfg.POSITION), lambda: 0.5 * (axis_pt + P()), UP * 0.45)
    meters.presence = 0.0
    stage.add_overlay(meters)
    newtons = Tag(txt(f"{fx(D.force)} N", cfg.FONT["label"], cfg.FORCE), lambda: P() - F_dir() * D.force * F_PER_N * 0.55,
                  LEFT * 0.6 + DOWN * 0.2)
    newtons.presence = 0.0
    stage.add_overlay(newtons)
    scene.play(stage.fade(meters, 1.0), *stage_swap(stage, F_lab, newtons), run_time=0.8)
    scene.play(Write(far), run_time=1.6)
    bars = bar_meter(lambda: D.tau_far, D.tau_far, at=[4.9, -1.75, 0], height=2.0, color=cfg.TORQUE)
    bar_lab = txt(f"{fx(D.tau_far)} N m", cfg.FONT["small"], cfg.TORQUE).next_to(bars, UP, buff=0.15)
    scene.play(FadeIn(bars), FadeIn(bar_lab), run_time=0.8)

    # --- 9. 0.2 m: 4 N m ------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    near_meters = Tag(txt(f"{fx(D.r_near, 1)} m", cfg.FONT["label"], cfg.POSITION), lambda: 0.5 * (axis_pt + P()),
                      UP * 0.45 + RIGHT * 0.2)
    near_meters.presence = 0.0
    stage.add_overlay(near_meters)
    scene.play(dist.to(stage, D.r_near * S), *stage_swap(stage, meters, near_meters), run_time=1.6)
    near = eq(rf"\tau = {fx(D.force)} \times {fx(D.r_near, 1)} = {fx(D.tau_near)}\ \mathrm{{N\,m}}", cfg.FONT["section"],
              cfg.TORQUE).move_to(far)
    scene.play(fade_through(far, near), run_time=1.0)
    bars2 = bar_meter(lambda: D.tau_near, D.tau_far, at=[6.6, -1.75, 0], height=2.0, color=cfg.TORQUE)
    bar_lab2 = txt(f"{fx(D.tau_near)} N m", cfg.FONT["small"], cfg.TORQUE).next_to(bars2.frame, UP, buff=0.15)
    scene.play(FadeIn(bars2), FadeIn(bar_lab2), run_time=0.8)
    ratio = txt(f"{fx(D.r_far / D.r_near)}× lever arm → {fx(D.r_far / D.r_near)}× torque", cfg.FONT["small"], cfg.WHITE)
    fit_width(ratio, 3.8)
    ratio.next_to(VGroup(bars, bars2), DOWN, buff=0.3).set_x(5.3)
    scene.play(FadeIn(ratio), run_time=0.8)
    finish(scene, t, stage)
