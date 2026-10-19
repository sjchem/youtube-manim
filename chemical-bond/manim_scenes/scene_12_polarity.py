"""Bond polarity: one shared cloud that leans, and a continuum instead of two boxes.

Electronegativities are Pauling values from ``utils.bond_data``. The cloud's
lean is set by the electronegativity difference (lean = delta EN / 2.4,
capped), the same illustrative rule as Part 4's density landscape; the
spectrum marker sits at the actual delta EN. The cloud is an illustration of
unequal sharing, not a computed molecular orbital, and the spectrum's
boundaries are drawn dashed and then dissolved because they are conventions.
"""

from manim_scenes.common import *

LEFT_AT = np.array([-2.1, 1.55, 0])
RIGHT_AT = np.array([2.1, 1.55, 0])
BAR_Y = -2.55
TEXT_Y = -0.72
EN_DROP = DOWN * 1.3
BAR_HALF = 5.6
EN_MAX = 3.2


class Scene12Polarity(Scene):
    def construct(self) -> None:
        play_scene(self)


def lean_for(delta: float) -> float:
    return float(min(delta / 2.4, 0.93))


def bar_x(delta: float) -> float:
    return -BAR_HALF + 2 * BAR_HALF * min(delta, EN_MAX) / EN_MAX


def spectrum_bar() -> VGroup:
    steps = 48
    stops = (cfg.CYAN, cfg.BLUE, cfg.PURPLE)
    cells = VGroup(*[Rectangle(width=2 * BAR_HALF / steps, height=0.42, stroke_width=0,
                               fill_color=mu.scale_color(i / (steps - 1), stops), fill_opacity=1) for i in range(steps)])
    cells.arrange(RIGHT, buff=0).move_to([0, BAR_Y, 0])
    frame = RoundedRectangle(width=2 * BAR_HALF + 0.1, height=0.52, corner_radius=0.12, stroke_color=cfg.MUTED, stroke_width=2,
                             fill_opacity=0).move_to(cells)
    return VGroup(cells, frame)


def shaded_core(label: str, radius: float) -> VGroup:
    core = nucleus_core(label, radius, polished=True)
    core.set_z_index(-3)
    core.label.set_z_index(0)
    return core


def layer_cloud(cloud) -> None:
    """Place the shaded nuclei inside the sampled electronic cloud."""
    cloud.set_z_index(-6, family=False)
    glows = cloud.glows if isinstance(cloud, PairCloud) else [cloud.glow]
    for glow in glows:
        glow.set_z_index(-5)
    for index, samples in enumerate(cloud.dots):
        samples.set_z_index(-4 if index < len(cloud.dots) // 2 else -2)


MODEL_PM = 1 / 58  # Both molecules use one bond-length scale.


def polarity_molecule(kind: str, center, *, yaw: float, tilt: float) -> ProjectedMolecule:
    if kind == "CO2":
        length = bd.MOLECULE_BOND_PM["C=O in CO2"] * MODEL_PM
        sites = np.array([[-length, 0, 0], [0, 0, 0], [length, 0, 0]])
        symbols, bonds = ["O", "C", "O"], [(0, 1, 2), (1, 2, 2)]
    else:
        length = bd.MOLECULE_BOND_PM["O-H in H2O"] * MODEL_PM
        half = np.radians(bd.BOND_ANGLE_DEG["H2O"] / 2)
        sites = np.array([[0, 0, 0], [-length * np.sin(half), -length * np.cos(half), 0],
                          [length * np.sin(half), -length * np.cos(half), 0]])
        symbols, bonds = ["O", "H", "H"], [(0, 1, 1), (0, 2, 1)]
    return ProjectedMolecule(sites, symbols, bonds, {"O": 0.43, "C": 0.37, "H": 0.26},
                             {"O": cfg.RED, "C": "#9AA8B5", "H": cfg.WHITE}, center, yaw=yaw, tilt=tilt)


def dipole_arrow(start, end, color=cfg.ANION) -> VGroup:
    """Chemical dipole convention: a crossed positive tail points to oxygen."""
    start, end = np.asarray(start, dtype=float), np.asarray(end, dtype=float)
    direction = end - start
    direction /= np.linalg.norm(direction)
    side = np.array([-direction[1], direction[0], 0]) * 0.10
    return VGroup(Arrow(start, end, buff=0, color=color, stroke_width=6,
                        max_tip_length_to_length_ratio=0.22),
                  Line(start - side, start + side, color=color, stroke_width=4))


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "12", "Bond polarity")

    # --- 1. Two extremes, and the space between -----------------------------------------------------------------
    gap = 1.7
    h2 = bind_pair(PairCloud(LEFT, RIGHT, 1.15, count=460, seed=121, share=1.0, glow=0.14), lambda: gap, [-4.6, 0.6, 0])
    scene.add(h2)
    h2_nuclei = pair_nuclei(h2, ("H", "H"), radius=0.26, polished=True)
    layer_cloud(h2)
    for core in h2_nuclei:
        core.set_z_index(-3)
        core.label.set_z_index(0)
    salt = rock_salt_crystal(1, 0.95, [4.6, 0.6, 0], cation=0.2, anion=0.32, spin=0.25, polished=True)
    salt._live_draw_order = True
    tags = VGroup(txt("perfect sharing", cfg.FONT["label"], cfg.CYAN).move_to([-4.6, -1.55, 0]),
                  txt("near-total transfer", cfg.FONT["label"], cfg.CATION).move_to([4.6, -1.55, 0]))
    scene.play(FadeIn(h2), FadeIn(h2_nuclei), FadeIn(salt), run_time=1.2)
    dismiss_opening_title(scene, t, head)
    scene.play(FadeIn(tags, shift=UP * 0.1), run_time=0.8)
    between = txt("?", 130, cfg.GOLD).move_to([0, 0.6, 0])
    scene.play(FadeIn(between, scale=0.5), run_time=0.8)

    # --- 2. Electronegativity: the pull on shared electrons --------------------------------------------------------
    beat(scene, t, 1)
    h2.clear_updaters()
    for core in h2_nuclei:
        core.clear_updaters()
    scene.play(FadeOut(VGroup(h2, h2_nuclei, salt, tags, between)), run_time=0.8)
    definition = VGroup(txt("electronegativity", cfg.FONT["title"], cfg.GOLD),
                        txt("Pull on shared electrons", cfg.FONT["label"], cfg.WHITE)).arrange(DOWN, buff=0.3)
    definition.move_to([0, 2.6, 0])
    scene.play(FadeIn(definition[0], shift=DOWN * 0.1), run_time=0.8)
    scene.play(FadeIn(definition[1]), run_time=0.8)

    # --- 3. H-H: same pull, symmetric --------------------------------------------------------------------------------
    beat(scene, t, 2)
    cloud = BondCloud(LEFT_AT, RIGHT_AT, count=520, seed=122, width=0.8, glow=0.18, dot_radius=0.034)
    layer_cloud(cloud)
    left_core = shaded_core("H", 0.3).move_to(LEFT_AT)
    right_core = shaded_core("H", 0.3).move_to(RIGHT_AT)
    ed_left, ed_right = (chip(f"{bd.ELECTRONEGATIVITY['H']:.2f}", cfg.GOLD, cfg.FONT["label"]).move_to(LEFT_AT + EN_DROP),
                              chip(f"{bd.ELECTRONEGATIVITY['H']:.2f}", cfg.GOLD, cfg.FONT["label"]).move_to(RIGHT_AT + EN_DROP))
    scene.play(FadeOut(definition[1]), definition[0].animate.scale(0.75).move_to([0, 3.45, 0]), run_time=0.7)
    definition = definition[0]
    scene.play(FadeIn(cloud), FadeIn(left_core), FadeIn(right_core), run_time=1.0)
    scene.play(FadeIn(ed_left, shift=UP * 0.1), FadeIn(ed_right, shift=UP * 0.1), run_time=0.7)
    pulls = VGroup(glow_arrow(LEFT_AT + RIGHT * 0.9, LEFT_AT + LEFT * 0.5, cfg.GOLD, 6),
                   glow_arrow(RIGHT_AT + LEFT * 0.9, RIGHT_AT + RIGHT * 0.5, cfg.GOLD, 6))
    pulls.shift(UP * 1.25)
    scene.play(*[GrowArrow(a.arrow) for a in pulls], FadeIn(VGroup(*[a[0] for a in pulls])), run_time=0.8)

    # --- 4. H-Cl: chlorine about 3.2, hydrogen about 2.2 --------------------------------------------------------------------
    beat(scene, t, 3)
    new_right = shaded_core("Cl", 0.36).move_to(RIGHT_AT)
    new_en = chip(f"{bd.ELECTRONEGATIVITY['Cl']:.2f}", cfg.GOLD, cfg.FONT["label"]).move_to(RIGHT_AT + EN_DROP)
    scene.play(FadeThrough(right_core, new_right), FadeThrough(ed_right, new_en), run_time=1.0)
    right_core, ed_right = new_right, new_en
    stronger = glow_arrow(RIGHT_AT + LEFT * 0.9 + UP * 1.25, RIGHT_AT + RIGHT * 1.0 + UP * 1.25, cfg.GOLD, 10, tip=0.36)
    scene.play(FadeOut(pulls[1]), GrowArrow(stronger.arrow), FadeIn(stronger[0]), run_time=0.9)
    bar = spectrum_bar()
    marker = Triangle(fill_color=cfg.WHITE, fill_opacity=1, stroke_width=0).scale(0.18).rotate(PI).move_to([bar_x(0), BAR_Y + 0.5, 0])
    scene.play(FadeIn(bar), FadeIn(marker), run_time=0.8)

    # --- 5. The cloud shifts toward chlorine -------------------------------------------------------------------------------
    beat(scene, t, 4)
    delta_hcl = bd.delta_en("H", "Cl")
    scene.play(cloud.lean_to(lean_for(delta_hcl)), marker.animate.move_to([bar_x(delta_hcl), BAR_Y + 0.5, 0]), run_time=2.4)
    delta_tag = eq(rf"\Delta\chi = {delta_hcl:.2f}", cfg.FONT["small"], cfg.WHITE).next_to(marker, UP, buff=0.12)
    scene.play(FadeIn(delta_tag), run_time=0.6)

    # --- 6. Partial charges -------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    plus = eq(r"\delta^{+}", 96, cfg.CATION).move_to(LEFT_AT + LEFT * 1.45 + UP * 0.35)
    minus = eq(r"\delta^{-}", 96, cfg.ANION).move_to(RIGHT_AT + RIGHT * 1.45 + UP * 0.35)
    scene.play(FadeOut(VGroup(pulls[0], stronger)), run_time=0.5)
    scene.play(FadeIn(minus, shift=DOWN * 0.15), run_time=0.8)
    scene.play(FadeIn(plus, shift=DOWN * 0.15), run_time=0.8)
    formula = eq(r"\mathrm{H^{\delta+}\!-\!Cl^{\delta-}}", 64, cfg.WHITE).move_to([0, TEXT_Y, 0])
    formula[0][1:3].set_color(cfg.CATION)
    formula[0][-2:].set_color(cfg.ANION)
    scene.play(Write(formula), run_time=1.2)

    # --- 7. A polar covalent bond ---------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    polar = chip("Polar covalent", cfg.BLUE, cfg.FONT["label"]).move_to([0, TEXT_Y, 0])
    scene.play(FadeThrough(formula, polar), run_time=1.0)
    scene.play(cloud.fade_to(1.5), run_time=0.5)
    scene.play(cloud.fade_to(1.0), run_time=0.5)

    # --- 8. Sodium and chlorine: a difference of more than two -------------------------------------------------------------------
    beat(scene, t, 7)
    new_left = shaded_core("Na", 0.34).move_to(LEFT_AT)
    na_en = chip(f"{bd.ELECTRONEGATIVITY['Na']:.2f}", cfg.GOLD, cfg.FONT["label"]).move_to(LEFT_AT + EN_DROP)
    scene.play(FadeThrough(left_core, new_left), FadeThrough(ed_left, na_en), FadeOut(polar), FadeOut(delta_tag), run_time=1.0)
    left_core, ed_left = new_left, na_en
    delta_nacl = bd.delta_en("Na", "Cl")
    big_delta = eq(rf"\Delta\chi = {delta_nacl:.2f}", cfg.FONT["small"], cfg.WHITE)
    scene.play(marker.animate.move_to([bar_x(delta_nacl), BAR_Y + 0.5, 0]), run_time=1.4)
    big_delta.next_to(marker, UP, buff=0.12)
    scene.play(FadeIn(big_delta), run_time=0.6)

    # --- 9. The cloud slides onto chlorine: better described as ions -----------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(cloud.lean_to(lean_for(delta_nacl)), run_time=2.4)
    ions = VGroup(eq(r"\mathrm{Na^{+}}", 80, cfg.CATION).move_to(plus).shift(LEFT * 0.2), eq(r"\mathrm{Cl^{-}}", 80, cfg.ANION).move_to(minus).shift(RIGHT * 0.2))
    scene.play(FadeThrough(plus, ions[0]), FadeThrough(minus, ions[1]), run_time=1.0)
    scene.play(Indicate(ions, color=cfg.WHITE, scale_factor=1.08), run_time=1.0)

    # --- 10. Not two boxes: a continuum ---------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    boxes = VGroup(chip("covalent", cfg.CYAN, cfg.FONT["body"]), chip("ionic", cfg.CATION, cfg.FONT["body"])).arrange(RIGHT, buff=2.4)
    boxes.move_to([0, TEXT_Y, 0])
    scene.play(FadeIn(boxes, shift=UP * 0.1), run_time=0.8)
    cut = VGroup(strike(boxes[0], cfg.REPEL, 6), strike(boxes[1], cfg.REPEL, 6))
    scene.play(Create(cut), run_time=0.7)
    continuum = txt("a continuum", cfg.FONT["title"], cfg.GOLD).move_to([0, TEXT_Y, 0])
    scene.play(*fade_labels(VGroup(boxes, cut), continuum), Indicate(bar, color=cfg.WHITE, scale_factor=1.02),
               run_time=1.2)

    # --- 11. Equal, unequal, mostly ionic ---------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    zones = VGroup(txt("equal sharing", cfg.FONT["small"], cfg.CYAN).move_to([-4.1, BAR_Y - 0.62, 0]),
                   txt("unequal sharing", cfg.FONT["small"], cfg.BLUE).move_to([0, BAR_Y - 0.62, 0]),
                   txt("mostly ionic", cfg.FONT["small"], cfg.PURPLE).move_to([4.1, BAR_Y - 0.62, 0]))
    scene.play(LaggedStart(*[FadeIn(z, shift=UP * 0.1) for z in zones], lag_ratio=0.35), FadeOut(continuum), run_time=1.6)

    # --- 12. Boundaries are conventions --------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    walls = VGroup(*[DashedLine([x, BAR_Y - 0.45, 0], [x, BAR_Y + 0.45, 0], stroke_color=cfg.WHITE, stroke_width=4, dash_length=0.08)
                     for x in (-2.0, 2.0)])
    scene.play(Create(walls), run_time=0.8)
    convention = txt("No sharp boundary", cfg.FONT["label"], cfg.WHITE).move_to([0, TEXT_Y, 0])
    scene.play(FadeIn(convention), run_time=0.8)
    scene.play(walls.animate.set_opacity(0).stretch(1.6, 1), run_time=1.6)
    scene.remove(walls)

    # --- 13. A little sharing in salt; a little ionic character in HCl -------------------------------------------------------------------
    beat(scene, t, 12)
    examples = VGroup()
    for delta, label, colour in ((0.0, r"\mathrm{H_2}", cfg.CYAN), (delta_hcl, r"\mathrm{HCl}", cfg.BLUE), (delta_nacl, r"\mathrm{NaCl}", cfg.PURPLE)):
        dot = Dot([bar_x(delta), BAR_Y, 0], radius=0.11, color=cfg.WHITE)
        tag = eq(label, cfg.FONT["small"], colour).move_to([bar_x(delta), BAR_Y + 0.95, 0])
        examples.add(VGroup(dot, tag))
    scene.play(*fade_labels(VGroup(marker, big_delta, convention), examples),
               run_time=1.4)
    nuance = txt("Mixed bonding character", cfg.FONT["small"], cfg.WHITE).move_to([0, TEXT_Y + 0.3, 0])
    scene.play(FadeIn(nuance), run_time=0.8)
    scene.play(cloud.lean_to(0.82), run_time=1.2, rate_func=there_and_back)

    # --- 14. Rotating 3D models, then a clear vector comparison -------------------------------
    beat(scene, t, 13)
    scene.play(FadeOut(VGroup(cloud, left_core, right_core, ed_left, ed_right, ions, nuance, definition, examples, bar, zones)),
               run_time=0.7)
    co2 = polarity_molecule("CO2", [-3.55, 0.65, 0], yaw=-0.7, tilt=0.3)
    water = polarity_molecule("H2O", [3.55, 1.0, 0], yaw=0.65, tilt=-0.25)
    shape = chip("Polarity also depends on shape", cfg.GOLD, cfg.FONT["label"]).move_to([0, 3.2, 0])
    names = VGroup(eq(r"\mathrm{CO_2}", 64, cfg.WHITE).move_to([-3.55, -1.65, 0]),
                   eq(r"\mathrm{H_2O}", 64, cfg.WHITE).move_to([3.55, -1.65, 0]))
    scene.play(FadeIn(shape), FadeIn(co2), FadeIn(water), FadeIn(names), run_time=0.9)
    scene.play(co2.pose_to(0.65, 0.3), water.pose_to(-0.65, -0.25), run_time=3.4, rate_func=smooth)
    # Settle face-on before comparing vectors: equal bond dipoles must have
    # equal projected lengths, and water's resultant points toward oxygen.
    scene.play(co2.pose_to(0, 0), water.pose_to(0, 0), run_time=1.0)
    carbon = co2.projected_sites[1]
    co2_dipoles = VGroup(*[dipole_arrow(carbon + UP * 0.95 + RIGHT * side * 0.15,
                                       co2.projected_sites[index] + UP * 0.95)
                           for index, side in ((0, -1), (2, 1))])
    scene.play(*[GrowArrow(a[0]) for a in co2_dipoles], *[FadeIn(a[1]) for a in co2_dipoles], run_time=1.0)
    scene.add(co2_dipoles)
    cancel = txt("Cancel · non-polar", cfg.FONT["label"], cfg.CYAN).move_to([-3.55, -2.6, 0])
    scene.play(FadeIn(cancel), run_time=0.7)

    oxygen = water.projected_sites[0]
    water_dipoles = VGroup()
    for index, side in ((1, -1), (2, 1)):
        hydrogen = water.projected_sites[index]
        direction = oxygen - hydrogen
        direction /= np.linalg.norm(direction)
        offset = np.array([side * direction[1], -side * direction[0], 0]) * 0.38
        water_dipoles.add(dipole_arrow(hydrogen + offset + direction * 0.18,
                                      oxygen + offset - direction * 0.42))
    scene.play(*[GrowArrow(a[0]) for a in water_dipoles], *[FadeIn(a[1]) for a in water_dipoles], run_time=1.0)
    scene.add(water_dipoles)
    net = dipole_arrow([3.55, -1.05, 0], [3.55, 0.36, 0], cfg.GOLD)
    scene.play(GrowArrow(net[0]), FadeIn(net[1]), run_time=1.0)
    scene.add(net)
    polar_molecule = txt("Add · polar", cfg.FONT["label"], cfg.ANION).move_to([3.55, -2.6, 0])
    scene.play(FadeIn(polar_molecule), run_time=0.7)
    scene.play(Indicate(co2_dipoles, color=cfg.WHITE, scale_factor=1.0),
               Indicate(net, color=cfg.WHITE, scale_factor=1.0), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["12"])
