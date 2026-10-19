"""Valence bond theory, part 2: pi bonds, and multiple bonds read as sigma + pi (3D).

The pi surfaces are isosurfaces of the side-by-side p + p combination from
``utils.bond_models``; morphing the separation merges the upper lobes above
the axis and the lower lobes below it, leaving a nodal plane on the axis.
The "head-on versus sideways" bars are the computed overlap integrals at the
display bond distance (zeta R ~ 4.7, like carbon 2p at a C-C bond), where
head-on overlap is larger — the reason a pi bond is typically weaker.
O2 is drawn in the simple valence-bond picture (sigma + one pi); chapter 15
returns to what that picture misses. Multiple-bond contributions are shown
in separate panels, followed by a schematic end-on cross-section.
"""

from manim_scenes.common import *

FAR_P = 11.0


class Scene09PiBonds(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def pi_pair(separation: float, *, turned: bool = False, color: str = cfg.PI_COLOR, xs_count: int = 34,
            segments: int = 16) -> VGroup:
    """Upper and lower lobes of one pi bond (along z, or along y when ``turned``)."""
    lobes = VGroup()
    for upper in (True, False):
        surface = Isosurface(lambda v, up=upper: pi_grid(v, up, xs_count, segments), separation, color, 0.62,
                             colorer=orbital_shade(color))
        if turned:
            surface.turned(PI / 2, RIGHT)
        lobes.add(surface)
    return lobes


def morph_all(surfaces: Iterable[Isosurface], value: float, **kwargs) -> list[Animation]:
    return [s.morph_to(value, **kwargs) for s in surfaces]


def bonded_nuclei(separation: float, scale: float = P_SCALE) -> VGroup:
    half = separation / 2 * scale
    return VGroup(nucleus_3d([-half, 0, 0], 0.13), nucleus_3d([half, 0, 0], 0.13))


def nodal_plane() -> VGroup:
    """Tile the node so its near/far pieces sort between the two pi lobes."""
    xs, ys = np.linspace(-4.6, 4.6, 19), np.linspace(-2.2, 2.2, 11)
    xx, yy = np.meshgrid(xs, ys, indexing="ij")
    grid = np.stack((xx, yy, np.zeros_like(xx)), axis=-1)
    plane = GridSurface(grid, cfg.REPEL, opacity=0.10)
    corners = [(-4.6, -2.2, 0), (4.6, -2.2, 0), (4.6, 2.2, 0), (-4.6, 2.2, 0)]
    border = VGroup()
    for first, last in zip(corners, corners[1:] + corners[:1]):
        points = np.linspace(first, last, 20)
        border.add(*[Line(a, b, color=cfg.REPEL, stroke_width=2, stroke_opacity=0.6)
                     .set_shade_in_3d(True) for a, b in zip(points[:-1], points[1:])])
    return VGroup(plane, border)


def component_card(kind: str, x: float, *, width: float = 4.15) -> VGroup:
    """One contribution per panel; copies share the same bond-axis orientation.

    Rotate the local geometry, then place it on a flat-camera presentation.
    This keeps the three panels separate, with no camera sweep through labels.
    """
    color = {"sigma": cfg.SIGMA_COLOR, "pi": cfg.PI_COLOR, "pi2": cfg.PI_COLOR_2}[kind]
    if kind == "sigma":
        cloud = GridSurface(sigma_p_grid(bm.P_BOND, 34, 14), color, 0.80, colorer=orbital_shade(color))
    else:
        cloud = pi_pair(bm.P_BOND, turned=kind == "pi2", color=color, xs_count=28, segments=14)
        cloud.set_fill(opacity=0.80)
    axis = DashedLine([-4, 0, 0], [4, 0, 0], color=cfg.MUTED, stroke_width=2, dash_length=0.12)
    geometry = VGroup(cloud, bonded_nuclei(bm.P_BOND), axis)
    geometry.rotate(35 * DEGREES, OUT, about_point=ORIGIN)
    geometry.rotate(60 * DEGREES, RIGHT, about_point=ORIGIN)
    geometry.scale(0.49).shift([x, 0.35, 0])
    frame = RoundedRectangle(width=width, height=4.4, corner_radius=0.18,
                             stroke_color=color, stroke_width=1.8, stroke_opacity=0.45,
                             fill_opacity=0).move_to([x, 0.45, 0])
    label = eq(r"\sigma" if kind == "sigma" else r"\pi", 68, color).move_to([x, 2.1, 0])
    return VGroup(frame, geometry, label)


def bond_formula(symbol: str, count: int) -> VGroup:
    parts = [eq(rf"\mathrm{{{symbol}_2}}\;=", 62, cfg.WHITE), eq(r"\sigma", 68, cfg.SIGMA_COLOR)]
    if count >= 2:
        parts += [eq("+", 54, cfg.MUTED), eq(r"\pi", 68, cfg.PI_COLOR)]
    if count >= 3:
        parts += [eq("+", 54, cfg.MUTED), eq(r"\pi", 68, cfg.PI_COLOR_2)]
    return VGroup(*parts).arrange(RIGHT, buff=0.22).move_to([0, -3.2, 0])


def end_on_view() -> VGroup:
    """Schematic density cross-section, looking along the common bond axis."""
    shapes = VGroup()
    for y in (-1.15, 1.15):
        shapes.add(Ellipse(width=0.95, height=1.55, color=cfg.PI_COLOR,
                           fill_color=cfg.PI_COLOR, fill_opacity=0.8, stroke_width=2).move_to([0, y + 0.25, 0]))
    for x in (-1.15, 1.15):
        shapes.add(Ellipse(width=1.55, height=0.95, color=cfg.PI_COLOR_2,
                           fill_color=cfg.PI_COLOR_2, fill_opacity=0.8, stroke_width=2).move_to([x, 0.25, 0]))
    shapes.add(Circle(radius=0.36, color=cfg.SIGMA_COLOR, fill_color=cfg.SIGMA_COLOR,
                      fill_opacity=0.95, stroke_width=0).move_to([0, 0.25, 0]))
    shapes.add(eq(r"\pi", 52, cfg.PI_COLOR).move_to([0, 2.65, 0]),
               eq(r"\pi", 52, cfg.PI_COLOR_2).move_to([2.65, 0.25, 0]),
               eq(r"\sigma", 44, cfg.WHITE).move_to([0, 0.25, 0]))
    return shapes.scale(0.82).shift(DOWN * 0.15)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "09", "Pi bonds")
    scene.set_camera_orientation(phi=66 * DEGREES, theta=-74 * DEGREES, zoom=1.0)

    # --- 1. Two p orbitals, parallel, side by side -----------------------------------------------------------
    pi = pi_pair(FAR_P)
    nuclei = VGroup(nucleus_3d([-1, 0, 0], 0.13), nucleus_3d([1, 0, 0], 0.13))

    def place(m: Mobject) -> None:
        half = pi[0].value / 2 * P_SCALE
        m[0].move_to([-half, 0, 0])
        m[1].move_to([half, 0, 0])

    nuclei.add_updater(place)
    place(nuclei)
    axis = DashedLine([-5.4, 0, 0], [5.4, 0, 0], stroke_color=cfg.WHITE, stroke_width=3, dash_length=0.14)
    scene.play(FadeIn(pi), FadeIn(nuclei), Create(axis), run_time=1.6)
    parallel = caption("Parallel p orbitals", cfg.PI_COLOR, cfg.FONT["label"], y=-3.55)
    hud(scene, parallel)
    scene.play(FadeIn(parallel), run_time=0.7)
    dismiss_opening_title(scene, t, head)

    # --- 2. Upper lobes overlap above, lower lobes below -----------------------------------------------------
    beat(scene, t, 1)
    scene.play(*morph_all(pi, bm.P_BOND), run_time=3.6, rate_func=smooth)
    above = caption("Density above and below the axis", cfg.WHITE, cfg.FONT["label"], y=-3.55)
    hud(scene, above)
    scene.play(*fade_labels(parallel, above), run_time=0.8)
    nuclei.clear_updaters()

    # --- 3. A pi bond -------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    pi_label = VGroup(eq(r"\pi", 120, cfg.PI_COLOR), txt("pi bond", cfg.FONT["body"], cfg.PI_COLOR)).arrange(RIGHT, buff=0.35)
    pi_label.move_to([0, 3.15, 0])
    hud(scene, pi_label)
    scene.play(FadeIn(pi_label, scale=0.8), run_time=0.9)
    move_camera(scene, phi=74 * DEGREES, theta=-58 * DEGREES, zoom=1.02, run_time=3.0)

    # --- 4. A flat node on the axis ---------------------------------------------------------------------------------
    beat(scene, t, 3)
    node = nodal_plane()
    zero = caption("π node through the bond axis", cfg.REPEL, cfg.FONT["label"], y=-3.55)
    hud(scene, zero)
    scene.play(*fade_labels(above, zero), FadeIn(node), axis.animate.set_stroke(cfg.REPEL, width=5), run_time=1.2)
    move_camera(scene, phi=84 * DEGREES, theta=-90 * DEGREES, zoom=1.02, run_time=2.6)
    scene.play(Indicate(axis, color=cfg.WHITE), run_time=1.0)

    # --- 5. Sideways overlap is smaller ---------------------------------------------------------------------------------
    beat(scene, t, 4)
    head_on, sideways = bm.p_overlap(bm.P_BOND, "sigma"), bm.p_overlap(bm.P_BOND, "pi")
    unit = 13.0
    bars = VGroup()
    for k, (name, value, colour) in enumerate((("head-on", head_on, cfg.SIGMA_COLOR), ("sideways", sideways, cfg.PI_COLOR))):
        label = txt(name, cfg.FONT["label"], colour)
        bar = Rectangle(width=value * unit, height=0.42, stroke_width=0, fill_color=colour, fill_opacity=0.9)
        row = VGroup(label, bar).arrange(RIGHT, buff=0.35)
        bar.align_to(np.array([-2.0, 0, 0]), LEFT)
        label.next_to(bar, LEFT, buff=0.35)
        row.move_to([0.2, -2.55 - 0.65 * k, 0], coor_mask=np.array([0, 1, 0]))
        bars.add(row)
    overlap_title = txt("overlap", cfg.FONT["small"], cfg.MUTED).next_to(bars, UP, buff=0.18).align_to(bars[0][1], LEFT)
    hud(scene, bars, overlap_title)
    scene.play(FadeOut(zero), FadeOut(node), axis.animate.set_stroke(cfg.WHITE, width=3), run_time=0.7)
    move_camera(scene, phi=66 * DEGREES, theta=-74 * DEGREES, zoom=0.95, run_time=1.4)
    scene.play(FadeIn(overlap_title), *[GrowFromEdge(row[1], LEFT) for row in bars], *[FadeIn(row[0]) for row in bars],
               run_time=1.4)
    weaker = VGroup(eq(r"\pi", 72, cfg.PI_COLOR), txt("typically weaker than", cfg.FONT["label"], cfg.WHITE),
                    eq(r"\sigma", 72, cfg.SIGMA_COLOR)).arrange(RIGHT, buff=0.25).move_to([0, 3.15, 0])
    hud(scene, weaker)
    scene.play(*fade_labels(pi_label, weaker), run_time=0.9)

    # --- 6. Separate contributions, rather than transparent clouds on top of one another ---
    beat(scene, t, 5)
    scene.play(FadeOut(VGroup(bars, overlap_title, weaker, *pi, nuclei, axis)), run_time=0.7)
    scene.set_camera_orientation(phi=0, theta=-PI / 2, gamma=0, zoom=1.0)
    separate = caption("Same bond · separate contributions", cfg.GOLD, cfg.FONT["label"], y=3.2)
    hud(scene, separate)
    sigma_card = component_card("sigma", -3.1, width=5.2)
    pi_card = component_card("pi", 3.1, width=5.2)
    adds = VGroup(eq(r"\sigma", 80, cfg.SIGMA_COLOR), eq("+", 64, cfg.MUTED),
                  eq(r"\pi", 80, cfg.PI_COLOR)).arrange(RIGHT, buff=0.3).move_to([0, -3.2, 0])
    hud(scene, adds)
    scene.play(FadeIn(separate), FadeIn(sigma_card), run_time=1.2)
    scene.play(FadeIn(pi_card), FadeIn(adds), run_time=1.2)
    scene.play(Indicate(adds[0], color=cfg.WHITE, scale_factor=1.15), run_time=0.9)

    # --- 7. Read the number of contributions ------------------------------------------------
    beat(scene, t, 6)
    read = caption("Read the bonds again", cfg.GOLD, cfg.FONT["body"], y=3.2)
    hud(scene, read)
    scene.play(FadeOut(VGroup(sigma_card, pi_card, adds)), *fade_labels(separate, read), run_time=0.9)

    # --- 8. Hydrogen: one central sigma cloud ------------------------------------------------
    beat(scene, t, 7)
    h2 = GridSurface(sigma_s_grid(bm.S_BOND), cfg.SIGMA_COLOR, 0.8, colorer=orbital_shade(cfg.SIGMA_COLOR))
    hydrogen = VGroup(h2, bonded_nuclei(bm.S_BOND, ORB_SCALE))
    hydrogen.scale(1.05).shift(UP * 0.4)
    h_label = bond_formula("H", 1)
    hud(scene, h_label)
    scene.play(FadeIn(hydrogen), FadeIn(h_label), run_time=1.0)
    scene.play(Indicate(h_label[1], color=cfg.WHITE, scale_factor=1.15), run_time=0.8)

    # --- 9. Double bond: reveal sigma first, then pi in its own view --------------------------
    beat(scene, t, 8)
    double_title = caption("Double bond", cfg.GOLD, cfg.FONT["body"], y=3.2)
    o_label = bond_formula("O", 2)
    o_sigma = component_card("sigma", -3.1, width=5.2)
    o_pi = component_card("pi", 3.1, width=5.2)
    simple = caption("Same bond · separate views · simplified model", cfg.MUTED, cfg.FONT["tiny"], y=-2.3)
    hud(scene, double_title, o_label, simple)
    scene.play(FadeOut(VGroup(hydrogen, h_label)), *fade_labels(read, double_title), run_time=0.6)
    scene.play(FadeIn(o_sigma), FadeIn(o_label[:2]), FadeIn(simple), run_time=0.9)
    cue(scene, t, 69.0)
    scene.play(FadeIn(o_pi), FadeIn(o_label[2:]), run_time=1.2)
    # Keep revealed pieces under one HUD parent for the later replacement.
    scene.add(o_label)
    scene.play(Indicate(o_label[1], color=cfg.WHITE, scale_factor=1.12),
               Indicate(o_label[-1], color=cfg.WHITE, scale_factor=1.12), run_time=0.9)

    # --- 10. Triple bond: three separate panels, one contribution at a time ------------------
    beat(scene, t, 9)
    triple_title = caption("Triple bond", cfg.GOLD, cfg.FONT["body"], y=3.2)
    n_label = bond_formula("N", 3)
    n_cards = VGroup(component_card("sigma", -4.6), component_card("pi", 0), component_card("pi2", 4.6))
    hud(scene, triple_title, n_label)
    scene.play(FadeOut(VGroup(o_sigma, o_pi, o_label)), *fade_labels(double_title, triple_title), run_time=0.6)
    scene.play(FadeIn(n_cards[0]), FadeIn(n_label[:2]), run_time=0.8)
    cue(scene, t, 80.5)
    scene.play(FadeIn(n_cards[1]), FadeIn(n_label[2:4]), run_time=0.8)
    scene.play(FadeIn(n_cards[2]), FadeIn(n_label[4:]), run_time=0.8)
    scene.add(n_label)

    # --- 11. An uncluttered end-on cross-section explains the perpendicular directions -------
    beat(scene, t, 10)
    end_title = caption("Along the bond axis", cfg.GOLD, cfg.FONT["body"], y=3.45)
    section_note = caption("Schematic cross-section", cfg.MUTED, cfg.FONT["tiny"], y=2.65)
    directions = caption("One σ + two perpendicular π", cfg.WHITE, cfg.FONT["label"], y=-2.3)
    section = end_on_view()
    hud(scene, end_title, section_note, directions, section)
    scene.play(FadeOut(n_cards), FadeOut(simple), *fade_labels(triple_title, end_title), run_time=0.7)
    scene.play(FadeIn(section), FadeIn(section_note), FadeIn(directions), run_time=1.2)
    scene.play(Indicate(n_label[1], color=cfg.WHITE, scale_factor=1.15), run_time=0.8)
    scene.play(Indicate(VGroup(n_label[3], n_label[5]), color=cfg.WHITE, scale_factor=1.0), run_time=0.9)

    # --- 12. A clean count and line-bond summary, without another cloud overlay ---------------
    beat(scene, t, 11)
    summary_title = caption("Count the contributions", cfg.GOLD, cfg.FONT["body"], y=3.2)
    rows = VGroup()
    for y, name, symbol, count in ((1.65, "single", "H", 1), (0, "double", "O", 2), (-1.65, "triple", "N", 3)):
        label = txt(name, cfg.FONT["label"], cfg.WHITE).move_to([-5.35, y, 0])
        formula = bond_formula(symbol, count)
        formula.remove(formula[0])
        formula.arrange(RIGHT, buff=0.22).move_to([-0.8, y, 0])
        left = txt(symbol, cfg.FONT["section"], cfg.WHITE).move_to([3.35, y, 0])
        right = txt(symbol, cfg.FONT["section"], cfg.WHITE).move_to([5.5, y, 0])
        bonds = VGroup(*[Line([3.85, y + (k - (count - 1) / 2) * 0.18, 0],
                             [5.0, y + (k - (count - 1) / 2) * 0.18, 0],
                             stroke_color=cfg.WHITE, stroke_width=5) for k in range(count)])
        rows.add(VGroup(label, formula, left, right, bonds))
    not_linear = caption("Bond strengths are not simple multiples", cfg.REPEL, cfg.FONT["small"], y=-3.2)
    hud(scene, summary_title, rows, not_linear)
    scene.play(FadeOut(VGroup(section, section_note, directions, n_label)),
               *fade_labels(end_title, summary_title), run_time=0.7)
    scene.play(LaggedStart(*[FadeIn(row) for row in rows], lag_ratio=0.2), run_time=1.2)
    scene.play(FadeIn(not_linear), run_time=0.8)

    # --- 13. A smooth shaded atom pair bridges to unequal sharing -----------------------------
    beat(scene, t, 12)
    scene.play(FadeOut(VGroup(rows, not_linear, summary_title)), run_time=0.7)
    fair = txt("Equal sharing", cfg.FONT["body"], cfg.CYAN).move_to([0, 1.8, 0])
    unfair = txt("What if sharing is unequal?", cfg.FONT["body"], cfg.GOLD).move_to([0, 0.35, 0])
    lopsided = VGroup(polished_ball(0.55, "#E8F1F8").move_to([-1.8, -1.65, 0]),
                     polished_ball(0.85, cfg.GREEN).move_to([1.55, -1.65, 0]))
    # A diffuse electronic-charge patch replaces the old hard glowing bead.
    sharing = soft_glow(cfg.CYAN, layers=18, peak_opacity=0.10).stretch_to_fit_width(1.6).stretch_to_fit_height(0.55)
    sharing.move_to([-0.3, -1.65, 0])
    hud(scene, fair, unfair, lopsided, sharing)
    scene.play(FadeIn(fair), FadeIn(lopsided), run_time=0.9)
    scene.play(FadeIn(sharing), run_time=0.6)
    cue(scene, t, 112.5)
    scene.play(FadeIn(unfair), run_time=0.8)
    scene.play(sharing.animate.shift(RIGHT * 1.05).stretch(0.6, 0), run_time=1.8)
    scene.play(Indicate(unfair, color=cfg.WHITE, scale_factor=1.05), run_time=0.9)
    end_scene(scene, t, cfg.SCENE_DURATIONS["09"])
