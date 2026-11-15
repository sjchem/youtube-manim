"""Scene 04 — where is the centre of mass? A uniform sphere, disc and rod turn
on a 3D stage, each with its centre-of-mass target at the geometric centre;
mirror pairs of particles on the disc show why. A hammer (light handle,
heavy iron head) puts its target near the head; a copper ring puts its target
in the empty middle. Then the hammer is tossed: it tumbles, the end of its
head draws a loopy curve, but its centre of mass draws a clean parabola.
"""

from manim_scenes.common import *

HANDLE_M, HEAD_M = 0.5, 1.5           # kg: a light handle, a heavy head (illustrative)
HANDLE_L = 2.6
HEAD_AT = HANDLE_L / 2                # head centre, measured from the handle's centre
COM_LOCAL = HEAD_M * HEAD_AT / (HANDLE_M + HEAD_M)
G_TOSS = 3.6
VX, VY = 3.4, 4.2                      # toss velocity of the centre of mass (screen units / s)


class Scene04WhereCom(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "04", "Where is the centre of mass?")
    stage = Stage((0.0, -0.55, 0.0), zoom=1.3, yaw=-0.2, pitch=0.2, sway=0.04)
    turn = Knob(0.0)
    drive(stage, turn, 0.6)

    # --- 1. Three uniform bodies -----------------------------------------------------------------------------
    sphere_c, disc_c, rod_c = np.array([-3.8, 0.0, 0.0]), np.array([0.0, 0.0, 0.0]), np.array([3.8, 0.0, 0.0])
    sphere = Ball(sphere_c, 0.95, cfg.DISC_BODY)
    equator = Curve(lambda: np.array([sphere_c + 0.97 * np.array([np.cos(a), 0.18 * np.sin(a), np.sin(a)]) @ mu.rotation_y(turn.value).T
                                      for a in np.linspace(0, 2 * np.pi, 40)]), cfg.DISC_STRIPE, width=3, glow=False)
    equator.bias = 2.0
    disc = Drum(disc_c, 1.0, 0.08, cfg.DISC_BODY, pose=lambda: mu.rotation_y(0.35 * np.sin(0.5 * turn.value)) @ mu.rotation_x(0.25),
                spin=lambda: turn.value, stripe=cfg.DISC_STRIPE, sectors=8)
    rod_pose = lambda: mu.rotation_z(0.6 * turn.value)  # noqa: E731
    rod_a = Ball(lambda: rod_c + rod_pose() @ np.array([-1.3, 0, 0]), 0.09, cfg.STEEL, layers=8)
    rod_b = Ball(lambda: rod_c + rod_pose() @ np.array([1.3, 0, 0]), 0.09, cfg.STEEL, layers=8)
    rod = Rod(rod_a, rod_b, width=20, dark="#2E5873", light="#BFE3F7")
    uniform = [sphere, equator, disc, rod_a, rod_b, rod]
    stage.add_body(*uniform)
    targets = [com_tag(c, 0.18) for c in (sphere_c, disc_c, rod_c)]
    hidden(*targets)
    stage.add_overlay(*targets)
    show(scene, stage, 1.0)
    q = caption("always at the geometric centre?", cfg.WHITE)
    scene.play(FadeIn(q), run_time=0.8)

    beat(scene, t, 1)
    names = VGroup(*[txt(n, cfg.FONT["small"], cfg.MUTED).move_to([x, -2.75, 0])
                     for n, x in (("uniform sphere", -5.5), ("uniform disc", 0.0), ("uniform rod", 5.5))])
    scene.play(FadeIn(names, lag_ratio=0.2), FadeOut(q), run_time=1.0)
    for target in targets:
        scene.play(stage.fade(target, 1.0), run_time=0.6)
    yes = caption("uniform and symmetric: at the centre", cfg.BALANCED)
    scene.play(FadeIn(yes), run_time=0.8)

    # --- 2. Symmetry: matching pairs -------------------------------------------------------------------------------
    beat(scene, t, 2)
    pairs_local = [np.array([0.7, 0.3]), np.array([-0.2, 0.75]), np.array([0.45, -0.5])]

    def pair_points() -> np.ndarray:
        F = disc.axes()
        a = turn.value
        c, s = np.cos(a), np.sin(a)
        out = []
        for p in pairs_local:
            q_ = np.array([p[0] * c - p[1] * s, p[0] * s + p[1] * c])
            for sign in (1, -1):
                out.append(disc_c + F @ np.array([sign * q_[0], sign * q_[1], 0.1]))
        return np.array(out)

    mirror = Dots(pair_points, cfg.GOLD, radius=0.1)
    mirror.bias = 3.0
    links = [Segment(lambda k=k: pair_points()[2 * k], lambda k=k: pair_points()[2 * k + 1], cfg.GOLD, width=2.5,
                     opacity=0.9, dashed=True) for k in range(3)]
    for link in links:
        link.bias = 2.5
    hidden(mirror, *links)
    stage.add_body(mirror, *links)
    match = caption("symmetry: opposite mass pairs", cfg.GOLD)
    scene.play(stage.fade(mirror, 1.0), *[stage.fade(l, 1.0) for l in links], fade_through(yes, match), run_time=1.2)

    # --- 3. A hammer: the centre moves toward the heavy head ----------------------------------------------------------
    beat(scene, t, 3)
    scene.play(*[stage.fade(b, 0.0) for b in uniform + [mirror, *links] + targets], FadeOut(names), FadeOut(match), run_time=1.0)
    hammer_c, hammer_turn = Knob(0.0), Knob(0.0)
    base = np.array([-2.6, 0.2, 0.0])
    toss = Knob(-1.0)                    # < 0: resting; >= 0: time since the toss

    # Cache hashing inspects closures even before the toss begins.
    def trail_com(s: float) -> np.ndarray:
        return base + RIGHT * COM_LOCAL + np.array([-2.0 + VX * s, VY * s - 0.5 * G_TOSS * s * s, 0.0])

    def com_point() -> np.ndarray:
        if toss.value < 0:
            return base + RIGHT * COM_LOCAL
        return trail_com(toss.value)

    def pose() -> np.ndarray:
        return mu.rotation_z(hammer_turn.value)

    def at_local(x: float) -> np.ndarray:
        return com_point() + pose() @ np.array([x - COM_LOCAL, 0.0, 0.0])

    handle = Block(lambda: at_local(0.0), (HANDLE_L, 0.16, 0.16), cfg.WOOD, pose=pose)
    head_block = Block(lambda: at_local(HEAD_AT), (0.42, 0.95, 0.42), "#7C8C99", pose=pose)
    hammer_target = com_tag(com_point, 0.19)
    geo_mid = Tag(VGroup(Circle(radius=0.14, stroke_color=cfg.MUTED, stroke_width=3, fill_opacity=0),
                         Line(LEFT * 0.2, RIGHT * 0.2, stroke_color=cfg.MUTED, stroke_width=2),
                         Line(DOWN * 0.2, UP * 0.2, stroke_color=cfg.MUTED, stroke_width=2)),
                  lambda: at_local(0.0))
    hidden(handle, head_block, hammer_target, geo_mid)
    stage.add_body(handle, head_block)
    stage.add_overlay(geo_mid, hammer_target)
    scene.play(stage.fade(handle, 1.0), stage.fade(head_block, 1.0), stage.fade(geo_mid, 1.0), run_time=1.0)
    heavy = Tag(txt("heavy iron head", cfg.FONT["small"], cfg.MASS), lambda: at_local(HEAD_AT), UP * 0.95)
    heavy.presence = 0.0
    stage.add_overlay(heavy)
    scene.play(stage.fade(heavy, 1.0), stage.fade(hammer_target, 1.0), run_time=0.9)
    shift = caption("the centre of mass shifts toward the heavy end", cfg.WHITE)
    scene.play(FadeIn(shift), run_time=0.8)

    # --- 4. A ring: the centre of mass in empty space ------------------------------------------------------------------------
    beat(scene, t, 4)
    ring_c = np.array([3.0, 0.2, 0.0])
    ring = Hoop(ring_c, 1.15, cfg.RING_BODY, pose=lambda: mu.rotation_y(0.5 * np.sin(0.4 * turn.value)) @ mu.rotation_x(0.35),
                spin=lambda: 0.5 * turn.value, width=20)
    ring_target = com_tag(ring_c, 0.19)
    empty = Tag(txt("empty space", cfg.FONT["small"], cfg.COM_GLOW), ring_c, DOWN * 2.2)
    hidden(ring, ring_target, empty)
    stage.add_body(ring)
    stage.add_overlay(ring_target, empty)
    scene.play(stage.fade(ring, 1.0), stage.fade(heavy, 0.0), run_time=1.0)
    scene.play(stage.fade(ring_target, 1.0), run_time=0.8)
    scene.play(stage.fade(empty, 1.0), run_time=0.8)
    no_material = caption("COM can lie in empty space", cfg.COM_GLOW)
    scene.play(fade_through(shift, no_material), run_time=0.8)

    # --- 5. Distribution, not geometry ------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    rule = result_label("set by how the mass is distributed", cfg.RESULT, cfg.FONT["body"]).move_to(UP * 2.9)
    scene.play(FadeIn(rule, shift=DOWN * 0.15), FadeOut(no_material), run_time=1.0)

    # --- 6. Toss the hammer: tumbling body, parabolic centre ---------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(stage.fade(ring, 0.0), stage.fade(ring_target, 0.0), stage.fade(empty, 0.0), stage.fade(geo_mid, 0.0),
               FadeOut(rule), stage.glide((-0.5, -1.5, 0.0)), stage.zoom_to(1.02), run_time=0.8)
    flight = VY * 2 / G_TOSS * 0.98
    com_trail = Curve(lambda: np.array([trail_com(s) for s in np.linspace(0, max(toss.value, 1e-3), 50)]), cfg.WHITE, width=5)
    head_trail = Curve(lambda: np.array([trail_head(s) for s in np.linspace(0, max(toss.value, 1e-3), 80)]), cfg.MASS,
                       width=3, opacity=0.65)
    spin_rate = 4.2

    def trail_head(s: float) -> np.ndarray:
        return trail_com(s) + mu.rotation_z(spin_rate * s) @ np.array([HEAD_AT - COM_LOCAL + 0.2, 0.0, 0.0])

    com_trail.bias = head_trail.bias = 6.0
    stage.add_body(head_trail, com_trail)
    scene.play(toss.to(stage, 0.0), run_time=0.6)
    scene.play(toss.to(stage, flight, rate_func=linear), hammer_turn.to(stage, spin_rate * flight, rate_func=linear),
               run_time=flight)
    watch = caption("tumbling body · parabolic COM", cfg.WHITE)
    scene.play(FadeIn(watch), run_time=0.8)

    # --- 7. A clue ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    clue = result_label("a clue", cfg.RESULT, cfg.FONT["section"]).move_to(UP * 3.0)
    scene.play(FadeIn(clue, scale=1.1), run_time=0.9)
    finish(scene, t, stage)
