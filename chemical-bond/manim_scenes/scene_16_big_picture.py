"""Three bonds, one principle.

The three panels reuse the film's own objects (the shared cloud, the rock-salt
crystal, the electron sea), so the synthesis is visibly a recap. Their
valleys are schematic shapes (labelled so); what they share is the story,
not the numbers. The bond-type map is a van Arkel-Ketelaar triangle drawn
from the Pauling electronegativities in ``utils.bond_data``: x is the mean
electronegativity of the two partners, y their difference.
"""

from manim_scenes.common import *

PANEL_XS = (-4.75, 0.0, 4.75)
PANEL_Y = 1.2
VALLEY_Y = -2.2
TRIANGLE = {"metal": ("Na", "Na"), "Cu": ("Cu", "Cu"), "H2": ("H", "H"), "Cl2": ("Cl", "Cl"), "HCl": ("H", "Cl"),
            "NaCl": ("Na", "Cl"), "MgO": ("Mg", "O")}


class Scene16BigPicture(Scene):
    def construct(self) -> None:
        play_scene(self)


def mini_valley(x: float, depth: float, a: float, r_e: float, color: str) -> VGroup:
    axes = Axes(x_range=[0, 400, 100], y_range=[-900, 300, 300], x_length=3.6, y_length=2.1, tips=False,
                axis_config={"stroke_color": cfg.MUTED, "stroke_width": 2, "include_ticks": False}).move_to([x, VALLEY_Y, 0])
    start = bm.morse_inverse(280, depth, r_e, a)
    curve = axes.plot(lambda r: float(bm.morse(r, depth, r_e, a)), x_range=[start, 400, 1], color=color, stroke_width=6,
                      use_smoothing=False)
    group = VGroup(axes, curve)
    group.axes, group.curve, group.params = axes, curve, (depth, r_e, a)
    return group


def shaded_bead(point, radius: float, color: str) -> VGroup:
    return VGroup(halo(radius * 2.8, color, layers=6, peak_opacity=0.13),
                  polished_ball(radius, color)).move_to(point)


def water_model() -> ProjectedMolecule:
    """Rigid bent water, using the film's molecular colours and geometry."""
    length = bd.MOLECULE_BOND_PM["O-H in H2O"] / 48
    half = np.radians(bd.BOND_ANGLE_DEG["H2O"] / 2)
    sites = np.array([[0, 0, 0], [-length * np.sin(half), -length * np.cos(half), 0],
                      [length * np.sin(half), -length * np.cos(half), 0]])
    return ProjectedMolecule(sites, ["O", "H", "H"], [(0, 1, 1), (0, 2, 1)],
                             {"O": 0.48, "H": 0.31}, {"O": cfg.RED, "H": cfg.WHITE},
                             [0, 1.0, 0], yaw=0.65, tilt=-0.28)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "16", "Three bonds, one principle")

    # --- 1. Side by side ---------------------------------------------------------------------------------------
    boxes = VGroup(*[panel(4.3, 3.6, cfg.MUTED, 0.55).move_to([x, PANEL_Y, 0]) for x in PANEL_XS])
    boxes.set_z_index(-8)
    gap = 1.5
    covalent = bind_pair(PairCloud(LEFT, RIGHT, 1.0, count=420, seed=161, share=1.0, glow=0.15), lambda: gap,
                         [PANEL_XS[0], PANEL_Y, 0])
    scene.add(covalent)
    cov_nuclei = pair_nuclei(covalent, ("+", "+"), radius=0.2, polished=True)
    covalent.set_z_index(-6, family=False)
    for glow in covalent.glows:
        glow.set_z_index(-5)
    for index, samples in enumerate(covalent.dots):
        samples.set_z_index(-4 if index < len(covalent.dots) // 2 else -2)
    for core in cov_nuclei:
        core.set_z_index(-3)
        core.label.set_z_index(0)
    ionic = rock_salt_crystal(1, 0.95, [PANEL_XS[1], PANEL_Y, 0], cation=0.2, anion=0.32, spin=0.25, polished=True)
    ionic._live_draw_order = True
    metal = MetalSea(5, 4, 0.75, [PANEL_XS[2], PANEL_Y, 0], core_radius=0.24, electrons=80, seed=162, polished=True)
    scene.play(FadeIn(boxes), FadeIn(covalent), FadeIn(cov_nuclei), FadeIn(ionic), FadeIn(metal), run_time=1.4)
    dismiss_opening_title(scene, t, head)
    names = VGroup(txt("covalent", cfg.FONT["body"], cfg.CYAN), txt("ionic", cfg.FONT["body"], cfg.CATION),
                   txt("metallic", cfg.FONT["body"], cfg.METAL_CORE))
    for name, box in zip(names, boxes):
        name.next_to(box, UP, buff=0.2)

    # --- 2-4. One line each -----------------------------------------------------------------------------------------
    lines = (("shared density", cfg.CYAN), ("charges in a lattice", cfg.CATION), ("delocalised electrons", cfg.METAL_CORE))
    captions = VGroup()
    for k, (body, colour) in enumerate(lines):
        beat(scene, t, 1 + k)
        caption_k = txt(body, cfg.FONT["small"], colour).next_to(boxes[k], DOWN, buff=0.25)
        captions.add(caption_k)
        scene.play(FadeIn(names[k], shift=DOWN * 0.1), FadeIn(caption_k, shift=UP * 0.1),
                   boxes[k].animate.set_stroke(colour, width=4, opacity=1), run_time=0.9)
        scene.play(Indicate(names[k], color=cfg.WHITE, scale_factor=1.06), run_time=0.9)

    # --- 5. Ask the same question of each ------------------------------------------------------------------------------
    beat(scene, t, 4)
    question = txt("What happens to the energy?", cfg.FONT["body"], cfg.ENERGY).move_to([0, -1.25, 0])
    scene.play(*fade_labels(captions, question), run_time=0.9)

    # --- 6. Each one has a valley ----------------------------------------------------------------------------------------
    beat(scene, t, 5)
    valleys = VGroup(mini_valley(PANEL_XS[0], 436, 0.0194, 74, cfg.CYAN), mini_valley(PANEL_XS[1], 760, 0.012, 140, cfg.CATION),
                     mini_valley(PANEL_XS[2], 340, 0.014, 130, cfg.METAL_CORE))
    scene.play(FadeOut(question), LaggedStart(*[AnimationGroup(FadeIn(v.axes), Create(v.curve)) for v in valleys], lag_ratio=0.3),
               run_time=2.2)
    schematic = txt("schematic shapes", cfg.FONT["tiny"], cfg.MUTED).move_to([0, -3.75, 0])
    scene.play(FadeIn(schematic), run_time=0.5)

    # --- 7. Apart up here, stable down there ----------------------------------------------------------------------------
    beat(scene, t, 6)
    marbles = VGroup()
    paths = []
    for v, colour in zip(valleys, (cfg.CYAN, cfg.CATION, cfg.METAL_CORE)):
        depth, r_e, a = v.params
        marbles.add(shaded_bead(v.axes.c2p(380, float(bm.morse(380, depth, r_e, a))), 0.12, cfg.ENERGY))
        paths.append(v.axes.plot(lambda r, d=depth, e=r_e, w=a: float(bm.morse(r, d, e, w)), x_range=[r_e, 380, 1]).reverse_points())
    scene.play(FadeIn(marbles), run_time=0.5)
    scene.play(*[MoveAlongPath(m, p) for m, p in zip(marbles, paths)], run_time=2.2, rate_func=rush_into)
    same_story = txt("Different bonds · same principle", cfg.FONT["label"], cfg.WHITE).move_to([0, -0.85, 0])
    scene.play(FadeIn(same_story), run_time=0.8)

    # --- 8. Not hooks: arrangements of nuclei and electrons ---------------------------------------------------------------
    beat(scene, t, 7)
    for mob in (covalent, *cov_nuclei):
        mob.clear_updaters()
    scene.play(FadeOut(VGroup(boxes, names, covalent, cov_nuclei, ionic, metal, same_story, schematic)), run_time=0.9)
    ionic.clear_updaters()
    metal.clear_updaters()
    big = EnergyPlot(depth=1, r_e=1, a=1, r_max=400, e_min=-900, e_max=300, x_length=8.0, y_length=4.4, y_step=300,
                     center=[0, -0.6, 0], curve=False, labels=False)
    targets = []
    for v in valleys:
        depth, r_e, a = v.params
        start_r = bm.morse_inverse(280, depth, r_e, a)
        targets.append(big.axes.plot(lambda r, d=depth, e=r_e, w=a: float(bm.morse(r, d, e, w)), x_range=[start_r, 400, 1],
                                     color=v.curve.get_color(), stroke_width=6, use_smoothing=False))
    scene.play(FadeIn(big.axes), *[ReplacementTransform(v.curve, target) for v, target in zip(valleys, targets)],
               *[FadeOut(v.axes) for v in valleys], *[m.animate.move_to(big.axes.c2p(v.params[1], -v.params[0]))
                                                      for m, v in zip(marbles, valleys)], run_time=1.8)
    stem = Line(UP * 0.75, DOWN * 0.1, stroke_color=cfg.MUTED, stroke_width=9)
    bend = Arc(radius=0.32, start_angle=PI, angle=1.15 * PI, arc_center=DOWN * 0.1 + RIGHT * 0.32, stroke_color=cfg.MUTED, stroke_width=9)
    hook = VGroup(stem, bend, txt("hooks?", cfg.FONT["small"], cfg.MUTED).move_to(RIGHT * 1.35 + UP * 0.25)).move_to([-5.2, 2.6, 0])
    scene.play(FadeIn(hook), run_time=0.6)
    hook_strike = strike(hook, cfg.REPEL, 7)
    scene.play(Create(hook_strike), run_time=0.6)
    physics = VGroup(txt("nuclei + electrons", cfg.FONT["label"], cfg.WHITE),
                     txt("electromagnetism + quantum mechanics", cfg.FONT["small"], cfg.MUTED)).arrange(DOWN, buff=0.18).move_to([2.6, 2.75, 0])
    scene.play(FadeIn(physics, shift=DOWN * 0.1), run_time=0.9)

    # --- 9. Stable = low enough energy ----------------------------------------------------------------------------------------
    beat(scene, t, 8)
    low = txt("Stable: lower energy together", cfg.FONT["body"], cfg.ENERGY).move_to([0, -3.6, 0])
    scene.play(FadeIn(low, shift=UP * 0.1), Indicate(marbles, color=cfg.WHITE, scale_factor=1.4), run_time=1.0)

    # --- 10. The periodic trends decide: a bond-type map -------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(VGroup(big.axes, *targets, marbles, hook, hook_strike, physics, low)), run_time=0.8)
    origin = np.array([-4.2, -2.7, 0])
    sx, sy = 2.4, 1.9

    def at(mean: float, delta: float) -> np.ndarray:
        return origin + np.array([(mean - 0.7) * sx, delta * sy, 0])

    corners = (at(0.8, 0), at(3.98, 0), at(2.39, 3.18))
    triangle = Polygon(*corners, stroke_color=cfg.MUTED, stroke_width=3, fill_color=cfg.PANEL, fill_opacity=0.6)
    regions = VGroup(txt("metallic", cfg.FONT["label"], cfg.METAL_CORE).next_to(corners[0], DOWN, buff=0.2),
                     txt("covalent", cfg.FONT["label"], cfg.CYAN).next_to(corners[1], DOWN, buff=0.2),
                     txt("ionic", cfg.FONT["label"], cfg.CATION).next_to(corners[2], UP, buff=0.15))
    axes_note = VGroup(txt("x: mean electronegativity", cfg.FONT["tiny"], cfg.MUTED),
                       txt("y: difference", cfg.FONT["tiny"], cfg.MUTED)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([5.1, 2.6, 0])
    scene.play(Create(triangle), FadeIn(regions), FadeIn(axes_note), run_time=1.2)
    points = VGroup()
    for name, (a, b) in TRIANGLE.items():
        ea, eb = bd.ELECTRONEGATIVITY[a], bd.ELECTRONEGATIVITY[b]
        label = {"metal": "Na", "Cu": "Cu"}.get(name, name)
        tex = rf"\mathrm{{{label[:-1]}_{label[-1]}}}" if label[-1].isdigit() else rf"\mathrm{{{label}}}"
        spot = at((ea + eb) / 2, abs(ea - eb))
        side = UL if name == "NaCl" else UR
        points.add(VGroup(Dot(spot, radius=0.09, color=cfg.WHITE), eq(tex, cfg.FONT["tiny"], cfg.WHITE).next_to(spot, side, buff=0.06)))
    scene.play(LaggedStart(*[FadeIn(p, scale=0.6) for p in points], lag_ratio=0.15), run_time=1.6)
    rules = VGroup(txt("Similar pull → sharing", cfg.FONT["small"], cfg.CYAN), txt("Large Δχ → ionic", cfg.FONT["small"], cfg.CATION),
                   txt("Delocalised → metallic", cfg.FONT["small"], cfg.METAL_CORE)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    rules.move_to([4.9, 0.3, 0])
    scene.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in rules], lag_ratio=0.4), run_time=1.6)

    # --- 11. All tools for describing where the electrons go --------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(VGroup(triangle, regions, axes_note, points, rules)), run_time=0.7)
    hub = txt("where the electrons go", cfg.FONT["body"], cfg.ELECTRON_COLOR).move_to([0, 0.2, 0])
    tools = VGroup(chip("octet rule", cfg.GREEN, cfg.FONT["label"]), chip("Lewis dots", cfg.CYAN, cfg.FONT["label"]),
                   eq_chip(r"\sigma\ \text{and}\ \pi", cfg.PI_COLOR, cfg.FONT["label"]), eq_chip(r"\delta^{+}\ \delta^{-}", cfg.ANION, cfg.FONT["label"]))
    spots = ([-4.4, 2.2, 0], [4.4, 2.2, 0], [-4.4, -1.8, 0], [4.4, -1.8, 0])
    for tool, spot in zip(tools, spots):
        tool.move_to(spot)
    links = VGroup(*[Line(tool.get_center(), hub.get_center(), stroke_color=cfg.MUTED, stroke_width=2, stroke_opacity=0.6, buff=1.1)
                     for tool in tools])
    scene.play(FadeIn(hub, scale=0.9), run_time=0.8)
    scene.play(LaggedStart(*[AnimationGroup(FadeIn(tool, shift=(hub.get_center() - tool.get_center()) * -0.05), Create(link))
                             for tool, link in zip(tools, links)], lag_ratio=0.25), run_time=1.8)

    # --- 12. Underneath, one idea ------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    scene.play(FadeOut(VGroup(tools, links)), hub.animate.scale(0.7).move_to([0, 2.9, 0]).set_opacity(0.5), run_time=1.0)

    # --- 13. Lower energy together than apart ----------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    rule = eq(r"E_{\text{together}} \;<\; E_{\text{apart}}", 80, cfg.WHITE).move_to([0, 0.4, 0])
    rule[0][0].set_color(cfg.ENERGY)
    scene.play(FadeOut(hub), Write(rule), run_time=1.6)
    frame = glow_frame(rule, cfg.ENERGY, buff=0.3)
    scene.play(Create(frame), run_time=0.8)

    # --- 14. That is the chemical bond --------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    bond = txt("That is the chemical bond.", cfg.FONT["title"], cfg.GOLD).move_to([0, -1.7, 0])
    scene.play(FadeIn(bond, shift=UP * 0.15), run_time=1.0)
    scene.play(Indicate(bond, color=cfg.WHITE, scale_factor=1.04), run_time=1.2)

    # --- 15. But the valley says nothing about angles --------------------------------------------------------------------------------------------
    beat(scene, t, 14)
    scene.play(FadeOut(VGroup(rule, frame, bond)), run_time=0.8)
    water = water_model()
    formula = eq(r"\mathrm{H_2O}", 60, cfg.WHITE).move_to([0, 3.1, 0])
    scene.play(FadeIn(water), FadeIn(formula), run_time=1.0)
    scene.play(water.pose_to(-0.65, -0.28), run_time=1.8, rate_func=smooth)
    # Reveal the angle only after perspective has settled into a face-on view.
    scene.play(water.pose_to(0, 0), run_time=0.6)
    oxygen = water.projected_sites[0]
    distance = txt("distance: yes", cfg.FONT["label"], cfg.GREEN).move_to([-4.0, -1.6, 0])
    angle_arc = Arc(radius=0.9, start_angle=-PI / 2 - np.radians(bd.BOND_ANGLE_DEG["H2O"] / 2), angle=np.radians(bd.BOND_ANGLE_DEG["H2O"]),
                    arc_center=oxygen, stroke_color=cfg.GOLD, stroke_width=6)
    angle_q = txt("angle: ?", cfg.FONT["label"], cfg.GOLD).move_to([4.0, -1.6, 0])
    scene.play(FadeIn(distance, shift=UP * 0.1), run_time=0.8)
    scene.play(Create(angle_arc), FadeIn(angle_q, shift=UP * 0.1), run_time=1.0)
    shapes = txt("Next: molecular shape", cfg.FONT["body"], cfg.WHITE).move_to([0, -3.1, 0])
    scene.play(FadeIn(shapes, shift=UP * 0.1), run_time=0.9)
    scene.play(Indicate(angle_arc, color=cfg.WHITE, scale_factor=1.1), run_time=1.2)
    lone = VGroup(*[VGroup(e_dot(oxygen + np.array([x - LEWIS_GAP, 0.78, 0])),
                           e_dot(oxygen + np.array([x + LEWIS_GAP, 0.78, 0]))) for x in (-0.42, 0.42)])
    scene.play(LaggedStart(*[FadeIn(pair, shift=DOWN * 0.2) for pair in lone], lag_ratio=0.4), run_time=1.2)
    scene.play(Indicate(lone, color=cfg.GOLD, scale_factor=1.3), run_time=1.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["16"])
