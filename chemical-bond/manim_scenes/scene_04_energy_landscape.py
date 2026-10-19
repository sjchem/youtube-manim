"""The energy landscape of a bond — the film's centrepiece (3D).

One ValueTracker holds the H–H separation in picometres. It drives, in the
same frame, the two nuclei and their shared cloud (top band), the gold dot on
E(r), the live distance readout, and the curve itself, which is traced only
as far as the atoms have actually been. The curve is a Morse model built on
H2's measured bond length (74 pm) and bond enthalpy (436 kJ/mol); its two
algebraic terms are drawn as the "push" and the "pull".

The second half sweeps the same curve around a vertical axis: with one atom
held at the centre, the height of the surface is the energy for every
position of the other atom in a plane, so the valley becomes a circular moat
at the bond length. Seen edge-on, the surface's silhouette is the curve again.
"""

from manim_scenes.common import *

PM = 1 / 50                 # screen units per picometre in the top band
BAND_Y = 2.35
RADIUS = 0.85
WELL_SCALE = 1 / 55         # screen units per picometre on the 3D landscape
WELL_DEPTH = 2.2


class Scene04EnergyLandscape(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def share_for(r: float) -> float:
    """How far the two clouds have merged at separation r (schematic)."""
    return float(mu.smoothstep((210 - r) / (210 - H2[1])))


def bond_length_ring() -> VGroup:
    """Short 3D strokes let Cairo occlude the far arc with the landscape.

    A flat ParametricFunction is painted after every surface face; shading
    one whole curve would still sort it at only one depth. Sorting individual
    strokes places each part of the ring among the neighbouring mesh faces.
    """
    angles = np.linspace(0, TAU, 161)
    points = np.column_stack((H2[1] * WELL_SCALE * np.cos(angles),
                              H2[1] * WELL_SCALE * np.sin(angles),
                              np.full_like(angles, -WELL_DEPTH + 0.05)))
    return VGroup(*[
        Line(first, second, color=cfg.WHITE, stroke_width=6).set_shade_in_3d(True)
        for first, second in zip(points[:-1], points[1:])
    ])


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "04", "The energy landscape")

    # --- 1. Energy against distance -----------------------------------------------------------------
    r = ValueTracker(300.0)
    plot = EnergyPlot(center=DOWN * 1.45, x_length=11.6, y_length=4.3, curve=False)
    plot.shift(RIGHT * 0.35)
    cloud = bind_pair(PairCloud(LEFT, RIGHT, RADIUS, count=480, seed=41, glow=0.13), lambda: r.get_value() * PM,
                      UP * BAND_Y + RIGHT * 0.35)
    cloud.add_updater(lambda m: setattr(m, "share", share_for(r.get_value())), index=0)
    seen = {"low": r.get_value()}

    def traced() -> list[np.ndarray]:
        seen["low"] = min(seen["low"], r.get_value())
        low = max(seen["low"], plot.r_clip())
        return [plot.point(x) for x in np.linspace(low, plot.r_max, 260)]

    trace = VMobject(stroke_color=cfg.ENERGY, stroke_width=6).set_points_as_corners(traced())
    trace_glow = VMobject(stroke_color=cfg.ENERGY, stroke_width=20, stroke_opacity=0.15).set_points_as_corners(traced())
    trace.add_updater(lambda m: m.set_points_as_corners(traced()))
    trace_glow.add_updater(lambda m: m.set_points_as_corners(traced()))
    marker = plot.marker(r)
    readout_value = DecimalNumber(r.get_value(), num_decimal_places=0, font_size=cfg.FONT["label"] * MATH_SCALE,
                                  color=cfg.WHITE)
    readout = VGroup(eq("r =", cfg.FONT["label"], cfg.WHITE), readout_value, txt("pm", cfg.FONT["small"], cfg.MUTED))
    readout.arrange(RIGHT, buff=0.18).move_to([5.5, 3.3, 0])
    readout_value.add_updater(lambda m: m.set_value(r.get_value()))

    scene.play(Create(plot.axes), FadeIn(plot.frame_lines), run_time=1.2)
    model = txt("Morse model · schematic scale", cfg.FONT["tiny"], cfg.MUTED).next_to(plot.y_title, RIGHT, buff=0.7)
    scene.play(FadeIn(plot.labels), FadeIn(model), run_time=0.8)
    scene.add(cloud)
    nuclei = pair_nuclei(cloud, ("+", "+"), radius=0.2)
    scene.play(FadeIn(cloud), FadeIn(nuclei), FadeIn(marker, scale=0.5), run_time=1.0)
    scene.add(trace_glow, trace, marker)
    dismiss_opening_title(scene, t, head)
    scene.play(FadeIn(readout), run_time=0.6)

    # --- 2. Far apart: energy zero ---------------------------------------------------------------------------
    beat(scene, t, 1)
    zero_line = glow_line(plot.axes.c2p(170, 0), plot.axes.c2p(plot.r_max, 0), cfg.WHITE, 3)
    apart = txt("Apart: E = 0", cfg.FONT["small"], cfg.WHITE).next_to(plot.axes.c2p(250, 0), UP, buff=0.42)
    scene.play(Create(zero_line), FadeIn(apart, shift=DOWN * 0.1), track(r, 270), run_time=2.0, rate_func=linear)
    scene.play(track(r, 245), run_time=3.0, rate_func=linear)

    # --- 3. Approach: attractions win, the dot slides downhill ---------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(apart), FadeOut(zero_line), track(r, H2[1] + 18), run_time=4.6, rate_func=smooth)
    downhill = txt("attraction wins", cfg.FONT["small"], cfg.ATTRACT).move_to(plot.axes.c2p(175, -330))
    slope_arrow = Arrow(plot.axes.c2p(205, -120), plot.axes.c2p(140, -300), buff=0, color=cfg.ATTRACT,
                        stroke_width=6, max_tip_length_to_length_ratio=0.2)
    scene.play(FadeIn(downhill), GrowArrow(slope_arrow), track(r, H2[1] + 4), run_time=1.4)

    # --- 4. Too close: the wall ---------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(track(r, 31.5, rate_func=rush_into),
               FadeOut(VGroup(downhill, slope_arrow), rate_func=lambda a: smooth(min(a / 0.3, 1.0))), run_time=2.6)
    wall = txt("repulsion wall", cfg.FONT["small"], cfg.REPEL).move_to(plot.axes.c2p(130, 280))
    wall_arrow = Arrow(wall.get_left() + LEFT * 0.12, plot.point(33) + RIGHT * 0.12,
                       buff=0.05, color=cfg.REPEL, stroke_width=6,
                       max_tip_length_to_length_ratio=0.25)
    scene.play(FadeIn(wall), GrowArrow(wall_arrow), run_time=0.8)
    scene.play(track(r, H2[1] + 22), run_time=1.6, rate_func=rush_from)

    # --- 5. The valley and its lowest point -------------------------------------------------------------------------------
    beat(scene, t, 4)
    for target, run in ((H2[1] - 9, 0.9), (H2[1] + 6, 0.8), (H2[1] - 3, 0.7), (H2[1], 0.6)):
        scene.play(track(r, target), run_time=run, rate_func=smooth)
    trace.clear_updaters()
    trace_glow.clear_updaters()
    full = plot.energy_curve(cfg.ENERGY)
    scene.add(full)
    scene.remove(trace, trace_glow)
    scene.bring_to_front(marker)
    drop = plot.minimum_marks()
    floor_glow = halo(0.6, cfg.ENERGY, layers=5, peak_opacity=0.25).move_to(plot.point(H2[1]))
    scene.play(Create(drop), FadeIn(floor_glow), run_time=0.9)
    lowest = txt("lowest energy", cfg.FONT["small"], cfg.ENERGY).next_to(plot.point(H2[1]), RIGHT, buff=0.55)
    lowest.shift(DOWN * 0.15)
    scene.play(FadeIn(lowest, shift=LEFT * 0.1), run_time=0.8)

    # --- 6. 74 pm: the bond length -------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(VGroup(wall, wall_arrow, lowest)), run_time=0.5)
    r_e_label = txt(f"{bd.BOND_LENGTH_PM['H-H']} pm", cfg.FONT["label"], cfg.ENERGY)
    r_e_label.move_to(plot.axes.c2p(125, -155))
    r_e_leader = Line(plot.point(H2[1]) + UP * 0.18,
                      r_e_label.get_corner(DL) + DOWN * 0.12,
                      color=cfg.ENERGY, stroke_width=2.5)
    left_end, right_end = cloud.ends[0].get_center(), cloud.ends[1].get_center()
    bracket = VGroup(Line(left_end + DOWN * 1.05, right_end + DOWN * 1.05, stroke_color=cfg.ENERGY, stroke_width=5),
                     Line(left_end + DOWN * 0.9, left_end + DOWN * 1.2, stroke_color=cfg.ENERGY, stroke_width=5),
                     Line(right_end + DOWN * 0.9, right_end + DOWN * 1.2, stroke_color=cfg.ENERGY, stroke_width=5))
    bond_length = chip("bond length", cfg.ENERGY, cfg.FONT["small"]).move_to([-4.6, BAND_Y, 0])
    scene.play(FadeIn(r_e_label, shift=UP * 0.1), Create(r_e_leader), Create(bracket), run_time=1.0)
    scene.play(FadeIn(bond_length, shift=RIGHT * 0.15), Indicate(readout, color=cfg.ENERGY), run_time=1.2)

    # --- 7. A model: a long-range pull plus a short-range push ------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(VGroup(bracket, floor_glow)), run_time=0.5)
    pull = plot.term_curve("pull", cfg.ATTRACT)
    push = plot.term_curve("push", cfg.REPEL)
    pull_tag = txt("pull", cfg.FONT["label"], cfg.ATTRACT).move_to(plot.axes.c2p(200, -265))
    push_tag = txt("push", cfg.FONT["label"], cfg.REPEL).move_to(plot.axes.c2p(122, 300))
    scene.play(Create(pull), FadeIn(pull_tag), full.animate.set_stroke(opacity=0.25), run_time=1.6)
    scene.play(Create(push), FadeIn(push_tag), run_time=1.4)
    total_tag = VGroup(txt("push", cfg.FONT["small"], cfg.REPEL), eq("+", cfg.FONT["small"]),
                       txt("pull", cfg.FONT["small"], cfg.ATTRACT), eq("=", cfg.FONT["small"]),
                       txt("valley", cfg.FONT["small"], cfg.ENERGY)).arrange(RIGHT, buff=0.16)
    total_tag.move_to(plot.axes.c2p(232, 300))
    scene.play(full[1].animate.set_stroke(opacity=1), full[0].animate.set_stroke(opacity=0.16), FadeIn(total_tag), run_time=1.2)
    scene.play(Indicate(full[1], color=cfg.WHITE, scale_factor=1.0), run_time=1.0)
    scene.play(Indicate(model, color=cfg.WHITE, scale_factor=1.0), run_time=0.6)

    # --- 8. One more dimension ------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    flat = VGroup(plot, full, pull, push, pull_tag, push_tag, total_tag, model, drop,
                  r_e_label, r_e_leader, readout, bond_length)
    marker.clear_updaters()
    readout_value.clear_updaters()
    scene.play(FadeOut(flat), FadeOut(marker), FadeOut(cloud), FadeOut(nuclei), run_time=1.0)
    for mob in (cloud, *nuclei):
        mob.clear_updaters()
    scene.remove(cloud, nuclei)
    scene.set_camera_orientation(phi=88 * DEGREES, theta=-90 * DEGREES, zoom=0.92)
    profile = ParametricFunction(lambda u: np.array([u * WELL_SCALE, 0, well_height(abs(u), WELL_DEPTH)]),
                                 t_range=[-330, 330, 1], color=cfg.ENERGY, stroke_width=6)
    scene.play(Create(profile), run_time=1.6)
    sectors = []
    grid = well_grid(WELL_DEPTH, WELL_SCALE, segments=40)
    for k in range(8):
        part = GridSurface(grid[:, 5 * k:5 * k + 6], cfg.CYAN, 0.92, colorer=well_colorer(WELL_DEPTH))
        sectors.append(part)

    # --- 9. Hold one atom, let the other wander: the surface --------------------------------------------------------------------
    beat(scene, t, 8)
    centre_atom = nucleus_3d([0, 0, well_height(0, WELL_DEPTH) + 0.24], 0.2)
    scene.play(LaggedStart(*[FadeIn(part) for part in sectors], lag_ratio=0.35),
               Rotate(profile, angle=TAU, axis=OUT, about_point=ORIGIN), run_time=3.0)
    move_camera(scene, phi=62 * DEGREES, theta=-62 * DEGREES, zoom=0.98, run_time=2.6)
    height = caption("height = energy", cfg.ENERGY, cfg.FONT["label"], y=3.45)
    hud(scene, height)
    scene.play(FadeIn(height), FadeIn(centre_atom), run_time=0.8)
    fixed = caption("one atom held at the centre", cfg.WHITE, cfg.FONT["small"], y=-3.85)
    hud(scene, fixed)
    scene.play(FadeIn(fixed), run_time=0.6)

    # --- 10. Every starting point rolls to the same ring -----------------------------------------------------------------------
    beat(scene, t, 9)
    starts = ((300, 0.5), (240, 2.3), (40, 3.9), (280, 5.2))
    balls, trackers = [], []
    for radius_pm, angle in starts:
        tracker = ValueTracker(radius_pm)
        ball = Sphere(radius=0.17, resolution=(10, 6)).set_fill(cfg.ENERGY, 1).set_stroke(width=0)

        def roll(m, tr=tracker, ang=angle):
            rr = tr.get_value()
            m.move_to([rr * WELL_SCALE * np.cos(ang), rr * WELL_SCALE * np.sin(ang), well_height(rr, WELL_DEPTH) + 0.17])

        ball.add_updater(roll)
        roll(ball)
        balls.append(ball)
        trackers.append(tracker)
    scene.play(FadeOut(fixed), *[FadeIn(b, scale=0.4) for b in balls], run_time=0.8)
    scene.begin_ambient_camera_rotation(rate=0.07)
    scene.play(*[track(tr, H2[1] * (1.12 if k % 2 else 0.9)) for k, tr in enumerate(trackers)], run_time=3.0, rate_func=smooth)
    scene.play(*[track(tr, H2[1]) for tr in trackers], run_time=1.6, rate_func=smooth)
    ring = bond_length_ring()
    moat = caption("Bond length: 74 pm", cfg.WHITE, cfg.FONT["small"], y=-3.85)
    hud(scene, moat)
    scene.play(Create(ring), FadeIn(moat), run_time=1.4)

    # --- 11. Slice it: the curve again ----------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.stop_ambient_camera_rotation()
    slice_plane = Polygon([-6.4, 0, -2.6], [6.4, 0, -2.6], [6.4, 0, 2.9], [-6.4, 0, 2.9], stroke_color=cfg.WHITE,
                          stroke_width=2, stroke_opacity=0.5, fill_color=cfg.WHITE, fill_opacity=0.08)
    section = ParametricFunction(lambda u: np.array([u * WELL_SCALE, 0, well_height(abs(u), WELL_DEPTH) + 0.02]),
                                 t_range=[-330, 330, 1], color=cfg.ENERGY, stroke_width=8)
    scene.play(FadeOut(moat), FadeOut(ring), FadeOut(profile), FadeIn(slice_plane), *[FadeOut(b) for b in balls], run_time=1.0)
    for ball in balls:
        ball.clear_updaters()
    scene.play(Create(section), run_time=1.2)
    move_camera(scene, phi=86 * DEGREES, theta=-90 * DEGREES, zoom=0.92, run_time=2.6)
    scene.play(*[part.animate.set_fill(opacity=0.25) for part in sectors], run_time=0.8)
    verdict = VGroup(txt("A bond is not a hook.", cfg.FONT["body"], cfg.WHITE),
                     txt("An energy minimum.", cfg.FONT["body"], cfg.ENERGY)).arrange(DOWN, buff=0.18)
    verdict.move_to([0, -3.35, 0])
    hud(scene, verdict)
    scene.play(FadeIn(verdict[0], shift=UP * 0.1), run_time=0.8)
    scene.play(FadeIn(verdict[1], shift=UP * 0.1), run_time=0.8)
    scene.play(Indicate(section, color=cfg.WHITE, scale_factor=1.0), run_time=1.4)
    move_camera(scene, phi=74 * DEGREES, theta=-80 * DEGREES, zoom=0.98, run_time=3.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["04"])
