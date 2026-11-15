"""Scene 02 — from particles to rigid bodies. A ball flies on a 3D parabola and
shrinks to a glowing point (mass, no size). A big wheel spins on the stage:
a bead near the axle and a bead on the rim leave trails of very different
lengths in the same time. The wheel fills with particles; dashed links
between pairs keep their length as it turns (|r_i - r_j| = constant). Three
live 2D panels then show the three motions of a rigid plate: translation
(equal gold arrows), rotation about a fixed axis (arrows grow with r) and
rolling (v_cm + omega x r). Finally one plate shows "where" (its centre) and
"how it is turned" (an angle).
"""

from manim_scenes.common import *

WHEEL_R = 1.9
PLATE = np.array([[-0.75, -0.45], [0.75, -0.45], [0.75, 0.0], [0.0, 0.0], [0.0, 0.55], [-0.75, 0.55]])  # an L-shaped plate


class Scene02RigidBodies(Scene):
    def construct(self) -> None:
        play_scene(self)


def plate_points(centre: np.ndarray, phi: float, scale: float = 1.0) -> np.ndarray:
    c, s = np.cos(phi), np.sin(phi)
    R = np.array([[c, -s], [s, c]])
    pts = (PLATE * scale) @ R.T
    return np.column_stack([pts, np.zeros(len(pts))]) + centre


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "02", "From particles to rigid bodies")

    # --- 1. A thrown ball as a point ---------------------------------------------------------------------
    stage = Stage((0.0, -2.4, 0.0), zoom=1.25, yaw=-0.25, pitch=0.22, sway=0.03)
    floor(stage, 0.0, reach=7.0, opacity=0.22)
    fly = Knob(0.0)
    v0, g = np.array([3.2, 5.2, 0.0]), 4.0

    def ball_at(s: float) -> np.ndarray:
        return np.array([-5.0, 0.25, 0.0]) + v0 * s + np.array([0.0, -0.5 * g * s * s, 0.0])

    span = 2 * v0[1] / g
    ball = Ball(lambda: ball_at(fly.value), 0.25, cfg.BALL)
    trail = Curve(lambda: np.array([ball_at(s) for s in np.linspace(0, max(fly.value, 1e-3), 40)]), cfg.MUTED,
                  width=3, opacity=0.8, dashed=True)
    stage.add_body(trail, ball)
    show(scene, stage, 1.0)
    scene.play(fly.to(stage, span * 0.92, rate_func=linear), run_time=3.2)
    point = glow_dot(stage.screen_point(ball.where()), cfg.BALL, 0.1)
    tag = chip("a point: mass, no size", cfg.BALL).move_to(UP * 2.6)
    scene.play(stage.fade(ball, 0.0), FadeIn(point, scale=0.4), FadeIn(tag, shift=DOWN * 0.1), run_time=1.2)
    scene.wait(1.5)

    # --- 2. A spinning wheel: near the axle vs on the rim ------------------------------------------------------
    beat(scene, t, 1)
    hide(scene, stage, 0.7, FadeOut(point), FadeOut(tag))
    stage = Stage((0.0, -0.35, 0.0), zoom=1.15, yaw=-0.35, pitch=0.18, sway=0.03)
    spin = Knob(0.0)
    w = wheel(stage, ORIGIN, WHEEL_R, lambda: spin.value, half_length=0.14, sectors=8)
    near = rim_marker(stage, w.drum, 0.3, cfg.GOLD, fraction=0.2, radius=0.1)
    far = rim_marker(stage, w.drum, 0.3, cfg.BALL, fraction=0.95, radius=0.12)
    lag = 1.6

    def trail_of(marker_fraction: float):
        def pts():
            angles = np.linspace(spin.value - lag, spin.value, 30)
            return np.array([w.drum.centre + w.drum.axes() @ np.array([WHEEL_R * marker_fraction * np.cos(a + 0.3),
                                                                          WHEEL_R * marker_fraction * np.sin(a + 0.3),
                                                                          0.2]) for a in angles])
        return pts

    near_trail = Curve(trail_of(0.2), cfg.GOLD, width=5)
    far_trail = Curve(trail_of(0.95), cfg.BALL, width=5)
    near_trail.bias = far_trail.bias = 40.0
    stage.add_body(near_trail, far_trail)
    show(scene, stage, 1.0)
    drive(stage, spin, 1.0)
    labels = VGroup(txt("near axle: shorter path", cfg.FONT["small"], cfg.GOLD),
                    txt("rim: longer path", cfg.FONT["small"], cfg.BALL)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    labels.move_to([4.7, 2.5, 0])
    fit_width(labels, 5.6)
    scene.play(FadeIn(labels[0], shift=LEFT * 0.2), run_time=0.8)
    scene.wait(1.2)
    scene.play(FadeIn(labels[1], shift=LEFT * 0.2), run_time=0.8)
    scene.wait(2.0)
    one = caption("one dot can't describe both", cfg.WARNING)
    scene.play(FadeIn(one), run_time=0.8)

    # --- 3. An extended body: many particles -----------------------------------------------------------------------
    beat(scene, t, 2)
    rings = [(0.45, 6), (0.9, 10), (1.35, 14), (1.75, 18)]
    local = np.array([[r * np.cos(2 * np.pi * k / n), r * np.sin(2 * np.pi * k / n)] for r, n in rings for k in range(n)])

    def particle_points() -> np.ndarray:
        F = w.drum.axes()
        c, s = np.cos(spin.value), np.sin(spin.value)
        rot = local @ np.array([[c, s], [-s, c]])
        return np.array([F @ np.array([x, y, 0.2]) for x, y in rot])

    cloud = Dots(particle_points, cfg.CYAN, radius=0.07)
    cloud.bias = 40.0
    cloud.presence = 0.0
    stage.add_body(cloud)
    ext = caption("an extended body: many particles", cfg.CYAN)
    scene.play(stage.fade(cloud, 1.0), stage.fade(near_trail, 0.0), stage.fade(far_trail, 0.0), fade_through(one, ext),
               FadeOut(labels), run_time=1.2)

    # --- 4. Rigid: the distance between any two particles stays fixed -------------------------------------------------
    beat(scene, t, 3)
    pairs = [(0, 30), (8, 40), (20, 47), (3, 25)]
    links = [Segment(lambda i=i: particle_points()[i], lambda j=j: particle_points()[j], cfg.GOLD, width=3.5,
                     opacity=0.95, dashed=True) for i, j in pairs]
    for link in links:
        link.bias = 45.0
        link.presence = 0.0
    stage.add_body(*links)
    law = eq(r"|\vec r_i - \vec r_j| = \text{constant}", cfg.FONT["section"], cfg.WHITE)
    law_box = on_panel(law, cfg.GOLD).move_to([0, 3.0, 0])
    rigid = caption("rigid: fixed separations", cfg.GOLD)
    scene.play(*[stage.fade(link, 1.0) for link in links], fade_through(ext, rigid), run_time=1.2)
    scene.play(FadeIn(law_box, shift=DOWN * 0.15), run_time=1.0)
    scene.wait(2.5)

    # --- 5. An idealisation ------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    model = caption("the rigid-body approximation", cfg.MUTED, cfg.FONT["small"])
    scene.play(fade_through(rigid, model), law_box.animate.set_opacity(0.55), run_time=1.0)

    # --- 6. Three motions: translation ---------------------------------------------------------------------------------------
    beat(scene, t, 5)
    hide(scene, stage, 0.8, FadeOut(law_box), FadeOut(model))
    centres = [np.array([-4.8, -0.5, 0.0]), np.array([0.0, -0.5, 0.0]), np.array([4.8, -0.5, 0.0])]
    frames = VGroup(*[panel(4.5, 4.9, cfg.MUTED, 0.5).move_to(c + UP * 0.2) for c in centres])
    names = VGroup(txt("translation", cfg.FONT["label"], cfg.VELOCITY), txt("rotation", cfg.FONT["label"], cfg.ANGLE),
                   txt("rolling", cfg.FONT["label"], cfg.TORQUE))
    for name, c in zip(names, centres):
        name.move_to(c + UP * 3.1)
    clock = Knob(0.0)
    scene.add(frames[0])

    # Translation: the plate glides back and forth; every arrow is the same.
    def trans_centre() -> np.ndarray:
        return centres[0] + RIGHT * 0.9 * np.sin(0.7 * clock.value) + DOWN * 0.3

    def trans_vel() -> np.ndarray:
        return RIGHT * 0.9 * 0.7 * np.cos(0.7 * clock.value) * 1.4

    plate_a = VMobject(stroke_color=cfg.MUTED, stroke_width=3, fill_color=cfg.PANEL_2, fill_opacity=0.9)
    plate_a.add_updater(lambda m: m.set_points_as_corners([*plate_points(trans_centre(), 0.0), plate_points(trans_centre(), 0.0)[0]]))
    plate_a.update()
    probes = [0, 2, 4]
    arrows_a = [VecArrow(lambda k=k: plate_points(trans_centre(), 0.0)[k], lambda k=k: plate_points(trans_centre(), 0.0)[k] + trans_vel(),
                         cfg.VELOCITY, width=0.07, tip_len=0.22) for k in probes]
    holder = Dot(radius=0.001, fill_opacity=0)
    scene.add(holder)
    drive(holder, clock, 1.0)
    scene.play(FadeIn(frames[0]), FadeIn(names[0]), FadeIn(plate_a), run_time=0.9)
    scene.play(*[a.grow_in(run_time=0.8) for a in arrows_a], run_time=0.8)
    same = txt("same velocity everywhere", cfg.FONT["tiny"], cfg.VELOCITY).move_to(centres[0] + DOWN * 2.6)
    scene.play(FadeIn(same), run_time=0.6)

    # --- 7. Rotation about a fixed axis ----------------------------------------------------------------------------------------
    beat(scene, t, 6)
    pivot = centres[1] + DOWN * 0.1
    phi = lambda: 0.8 * clock.value  # noqa: E731
    plate_b = VMobject(stroke_color=cfg.MUTED, stroke_width=3, fill_color=cfg.PANEL_2, fill_opacity=0.9)
    plate_b.add_updater(lambda m: m.set_points_as_corners([*plate_points(pivot, phi(), 1.25), plate_points(pivot, phi(), 1.25)[0]]))
    plate_b.update()
    axle = glow_dot(pivot, cfg.ANGLE, 0.09)
    omega_b = 0.8 * 1.1

    def tip_b(k):
        p = plate_points(pivot, phi(), 1.25)[k]
        r = p - pivot
        return p + omega_b * np.array([-r[1], r[0], 0.0])

    arrows_b = [VecArrow(lambda k=k: plate_points(pivot, phi(), 1.25)[k], lambda k=k: tip_b(k), cfg.VELOCITY, width=0.07,
                         tip_len=0.22) for k in (0, 1, 4)]
    farther = txt("farther out, faster", cfg.FONT["tiny"], cfg.ANGLE).move_to(centres[1] + DOWN * 2.6)
    scene.play(FadeIn(frames[1]), FadeIn(names[1]), FadeIn(plate_b), FadeIn(axle), run_time=0.9)
    scene.play(*[a.grow_in(run_time=0.8) for a in arrows_b], FadeIn(farther), run_time=0.8)

    # --- 8. Rolling: both ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    r_w = 0.8
    ground_y = centres[2][1] - 1.55
    x_c = lambda: centres[2][0] + 0.45 * np.sin(0.6 * clock.value)  # noqa: E731
    roll_phi = lambda: -0.45 * np.sin(0.6 * clock.value) / r_w  # noqa: E731
    centre_c = lambda: np.array([x_c(), ground_y + r_w, 0.0])  # noqa: E731
    road = Line([centres[2][0] - 2.0, ground_y, 0], [centres[2][0] + 2.0, ground_y, 0], stroke_color=cfg.MUTED, stroke_width=3)
    disc = Circle(radius=r_w, stroke_color=cfg.STEEL, stroke_width=4, fill_color=cfg.DISC_BODY, fill_opacity=0.6)
    disc.add_updater(lambda m: m.move_to(centre_c()))
    spokes = VGroup(*[Line(ORIGIN, RIGHT, stroke_color=cfg.DISC_STRIPE, stroke_width=3) for _ in range(3)])

    def place_spokes(m):
        for k, s in enumerate(m):
            a = roll_phi() + k * 2 * np.pi / 3
            s.put_start_and_end_on(centre_c(), centre_c() + r_w * np.array([np.cos(a), np.sin(a), 0.0]))

    spokes.add_updater(place_spokes)
    spokes.update()
    v_cm = lambda: 0.27 * np.cos(0.6 * clock.value)

    def roll_tip(a0):
        p = centre_c() + r_w * np.array([np.cos(roll_phi() + a0), np.sin(roll_phi() + a0), 0.0])
        rel = p - centre_c()
        return p, p + np.array([v_cm(), 0, 0]) + (v_cm() / r_w) * np.array([rel[1], -rel[0], 0.0])

    arrows_c = [VecArrow(lambda a=a: roll_tip(a)[0], lambda a=a: roll_tip(a)[1], cfg.VELOCITY, width=0.07, tip_len=0.2)
                for a in (np.pi / 2, 0.0, np.pi)]
    both = txt("moves and turns", cfg.FONT["tiny"], cfg.TORQUE).move_to(centres[2] + DOWN * 2.6)
    scene.play(FadeIn(frames[2]), FadeIn(names[2]), Create(road), FadeIn(disc), FadeIn(spokes), run_time=0.9)
    scene.play(*[a.grow_in(run_time=0.8) for a in arrows_c], FadeIn(both), run_time=0.8)

    # --- 9. Where is it, and how is it turned? ----------------------------------------------------------------------------------------
    beat(scene, t, 8)
    q1 = chip("where is it?", cfg.WHITE)
    q2 = chip("how is it turned?", cfg.ANGLE)
    qs = VGroup(q1, q2).arrange(RIGHT, buff=1.2).move_to(DOWN * 3.65)
    scene.play(FadeOut(same), FadeOut(farther), FadeOut(both), run_time=0.6)
    scene.play(FadeIn(q1, shift=UP * 0.1), run_time=0.8)
    scene.play(FadeIn(q2, shift=UP * 0.1), run_time=0.8)
    scene.wait(2.0)
    scene.play(Indicate(q1, color=cfg.GOLD, scale_factor=1.06), run_time=1.0)
    scene.wait(max(time_left(scene, t, 9) - 1.6, 0.1))          # the three panels keep moving
    scene.play(Indicate(q2, color=cfg.ANGLE, scale_factor=1.06), run_time=1.0)
    finish(scene, t)
