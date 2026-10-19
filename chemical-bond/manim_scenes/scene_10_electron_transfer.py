"""Does electron transfer pay? The honest ledger for sodium and chlorine.

Removing sodium's outer electron costs +496 kJ/mol; chlorine returns 349 on
taking it (``utils.bond_data``), so the gas-phase transfer alone is uphill by
147. The attraction of one Na+/Cl- pair is shown as a point-charge Coulomb
estimate at the gas-phase NaCl distance (``ion_pair_estimate``, about
-590 kJ/mol) and labelled as an estimate. Every arrow uses one kJ scale.
"""

from manim_scenes.common import *

PER_KJ = 0.0052
LEDGER_Y = -0.75
NA_AT = np.array([1.7, 0.55, 0])
CL_AT = np.array([5.2, 0.55, 0])


class Scene10ElectronTransfer(Scene):
    def construct(self) -> None:
        play_scene(self)


def transfer_electron(point) -> VGroup:
    """A softly lit cyan marker for the tracked electron, without a white dot."""
    return VGroup(halo(0.37, cfg.ELECTRON_COLOR, layers=7, peak_opacity=0.10),
                  polished_ball(0.15, cfg.ELECTRON_COLOR)).move_to(point)


def depth_shaded_atom(atom: Atom, nucleus_radius: float = 0.26) -> Atom:
    """Embed a polished nucleus between rear and front cloud sample bins.

    ElectronCloud bins already run from the far side to the near side by
    sample depth. Keep their existing live updaters, fade and size controls;
    only their draw layers change. Negative layers keep captions in front.
    """
    nucleus = atom.nucleus
    body = polished_ball(nucleus_radius, cfg.NUCLEUS_COLOR).move_to(atom.center_point())
    nucleus.submobjects = [nucleus.glow, body, *([nucleus.label] if nucleus.label is not None else [])]
    nucleus.ball = body
    nucleus.set_z_index(-3)
    if nucleus.label is not None:
        nucleus.label.set_z_index(0)  # annotations stay legible over samples
    for cloud in (atom.core, atom.cloud):
        if cloud is None:
            continue
        # Keep the live controller before its children in Cairo's cache scan.
        cloud.set_z_index(-6, family=False)
        cloud.glow.set_z_index(-5)
        midpoint = len(cloud.dots) // 2
        for index, layer in enumerate(cloud.dots):
            layer.set_z_index(-4 if index < midpoint else -2)
    return atom


def ion_cloud(kind: str, radius: float, center, seed: int) -> Atom:
    colour = cfg.CATION if kind == "+" else cfg.ANION
    # Na+/Cl− labels below describe the whole ion; its nucleus stays positive.
    atom = Atom(radius, center, charge=None, count=300 if kind == "-" else 160, seed=seed, color=colour, glow=0.16,
                nucleus_radius=0.26)
    return depth_shaded_atom(atom)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "10", "Does electron transfer pay?")

    # --- 1. Sodium (one valence electron) and chlorine (seven) --------------------------------------------------
    sodium = depth_shaded_atom(Atom(1.55, NA_AT, charge="Na", core=0.62, count=200, core_count=230,
                                   seed=101, glow=0.12, nucleus_radius=0.26))
    chlorine = depth_shaded_atom(Atom(0.95, CL_AT, charge="Cl", core=0.42, count=380, core_count=150,
                                     seed=102, glow=0.2, nucleus_radius=0.26))
    na_config = eq(r"[\mathrm{Ne}]\,3s^{1}", cfg.FONT["label"], cfg.WHITE).move_to(NA_AT + DOWN * 2.35)
    cl_config = eq(r"[\mathrm{Ne}]\,3s^{2}3p^{5}", cfg.FONT["label"], cfg.WHITE).move_to(CL_AT + DOWN * 2.35)
    na_config[0][4:].set_color(cfg.ELECTRON_COLOR)
    cl_config[0][4:].set_color(cfg.ELECTRON_COLOR)
    scene.play(FadeIn(sodium, scale=0.6), FadeIn(chlorine, scale=0.6), run_time=1.4)
    dismiss_opening_title(scene, t, head)
    scene.play(FadeIn(na_config, shift=UP * 0.1), FadeIn(cl_config, shift=UP * 0.1), run_time=0.9)
    counts = VGroup(txt("1 valence", cfg.FONT["small"], cfg.ELECTRON_COLOR).next_to(na_config, DOWN, buff=0.2),
                    txt("7 valence", cfg.FONT["small"], cfg.ELECTRON_COLOR).next_to(cl_config, DOWN, buff=0.2))
    scene.play(FadeIn(counts), run_time=0.7)

    # --- 2. The familiar story ... ------------------------------------------------------------------------------------
    beat(scene, t, 1)
    electron = transfer_electron(NA_AT + 1.3 * np.array([np.cos(0.6), np.sin(0.6), 0]))
    scene.play(FadeIn(electron, scale=0.4), sodium.cloud.fade_to(0.45), run_time=0.8)
    hop = ArcBetweenPoints(electron.get_center(), CL_AT + np.array([-0.55, 0.6, 0]), angle=-PI / 3)
    story = chip("the familiar story", cfg.MUTED, cfg.FONT["label"]).move_to([3.45, 3.15, 0])
    scene.play(FadeIn(story, shift=DOWN * 0.1), MoveAlongPath(electron, hop), run_time=1.8)
    eights = txt("Two octets", cfg.FONT["small"], cfg.MUTED).next_to(story, DOWN, buff=0.22)
    scene.play(FadeIn(eights), run_time=0.7)
    check = chip("check the energy", cfg.ENERGY, cfg.FONT["label"]).move_to([-4.0, 3.15, 0])
    scene.play(FadeIn(check, shift=DOWN * 0.1), run_time=0.8)
    scene.play(MoveAlongPath(electron, hop.copy().reverse_points()), sodium.cloud.fade_to(1.0), run_time=1.2)
    scene.play(FadeOut(electron), run_time=0.4)

    # --- 3. Ionization: +496 -----------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(VGroup(story, eights, counts)), run_time=0.5)
    ie, ea = bd.IONIZATION_KJ["Na"], bd.ELECTRON_AFFINITY_KJ["Cl"]
    y0 = LEDGER_Y
    y1 = y0 + ie * PER_KJ
    y2 = y1 - ea * PER_KJ
    start_shelf = level_shelf(y0, -7.0, -5.2, cfg.WHITE, r"\mathrm{Na + Cl}", side=DOWN, size=cfg.FONT["label"])
    start_shelf.label.next_to(start_shelf.shelf, DOWN, buff=0.15)
    scene.play(Create(start_shelf.shelf), FadeIn(start_shelf.label), run_time=0.7)
    up = energy_step(-5.05, y0, y1, cfg.REQUIRED, f"+{ie}", side=LEFT, size=cfg.FONT["label"])
    up.tag.next_to(up.arrow, LEFT, buff=0.1).shift(UP * 0.3)
    ionize = eq(r"\mathrm{Na(g)} \rightarrow \mathrm{Na^+(g)} + e^-", cfg.FONT["label"], cfg.REQUIRED).move_to([-2.9, 3.25, 0])
    out = transfer_electron(NA_AT + 1.3 * np.array([np.cos(0.6), np.sin(0.6), 0]))
    scene.play(*fade_labels(check, ionize), run_time=1.0)
    scene.play(FadeIn(out, scale=0.4), sodium.cloud.fade_to(0.0), run_time=0.8)
    scene.play(out.animate.move_to(NA_AT + UP * 2.2 + RIGHT * 1.4), GrowArrow(up.arrow.arrow), FadeIn(up.arrow[0]), FadeIn(up.tag),
               run_time=1.4)
    mid_shelf = level_shelf(y1, -5.2, -3.4, cfg.WHITE)
    scene.play(Create(mid_shelf.shelf), run_time=0.5)

    # --- 4. Electron affinity: -349 -------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    attach = eq(r"\mathrm{Cl(g)} + e^- \rightarrow \mathrm{Cl^-(g)}", cfg.FONT["label"], cfg.RELEASED).move_to([-2.9, 2.4, 0])
    down = energy_step(-3.55, y1, y2, cfg.RELEASED, f"−{ea}", side=RIGHT, size=cfg.FONT["label"])
    scene.play(Write(attach), run_time=1.0)
    scene.play(out.animate.move_to(CL_AT + np.array([-0.6, 0.55, 0])), *chlorine.resize(1.25), GrowArrow(down.arrow.arrow),
               FadeIn(down.arrow[0]), FadeIn(down.tag), run_time=1.5)
    scene.play(FadeOut(out, scale=0.4), run_time=0.4)
    low_shelf = level_shelf(y2, -3.7, 0.0, cfg.WHITE)
    scene.play(Create(low_shelf.shelf), run_time=0.5)

    # --- 5. Net: +147, uphill ----------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    guide = DashedLine([-5.2, y0, 0], [-1.6, y0, 0], stroke_color=cfg.MUTED, stroke_width=2, dash_length=0.1)
    net = energy_step(-1.95, y0, y2, cfg.REQUIRED, f"+{bd.transfer_cost()}", side=LEFT, size=cfg.FONT["label"])
    net.tag.next_to(net.arrow, LEFT, buff=0.12).shift(DOWN * 0.05)
    scene.play(Create(guide), run_time=0.6)
    scene.play(GrowArrow(net.arrow.arrow), FadeIn(net.arrow[0]), FadeIn(net.tag), run_time=1.0)
    uphill = chip("Transfer alone: uphill", cfg.REQUIRED, cfg.FONT["label"]).move_to([-3.9, -2.75, 0])
    scene.play(FadeIn(uphill, shift=UP * 0.1), run_time=0.8)
    unit = txt("kJ/mol", cfg.FONT["tiny"], cfg.MUTED).next_to(start_shelf.label, DOWN, buff=0.3)
    scene.play(FadeIn(unit), run_time=0.5)

    # --- 6. Someone must pay the bill -----------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    explain = txt("Transfer alone?", cfg.FONT["label"], cfg.MUTED).move_to([3.45, 3.15, 0])
    scene.play(FadeOut(VGroup(ionize, attach)), FadeIn(explain), run_time=0.8)
    no = strike(explain, cfg.REPEL, 7)
    scene.play(Create(no), run_time=0.6)
    bill = chip("What lowers the energy?", cfg.GOLD, cfg.FONT["label"]).move_to([3.45, -2.75, 0])
    scene.play(FadeIn(bill, shift=UP * 0.1), Wiggle(uphill, scale_value=1.05), run_time=1.2)

    # --- 7. Opposite ions attract ----------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(VGroup(explain, no, na_config, cl_config)), FadeOut(sodium), FadeOut(chlorine), run_time=0.8)
    cation = ion_cloud("+", 0.62, NA_AT, 103)
    anion = ion_cloud("-", 1.25, CL_AT, 104)
    names = VGroup(eq(r"\mathrm{Na^+}", cfg.FONT["label"], cfg.CATION).move_to(NA_AT + DOWN * 1.05),
                   eq(r"\mathrm{Cl^-}", cfg.FONT["label"], cfg.ANION).move_to(CL_AT + DOWN * 1.95))
    scene.play(FadeIn(cation, scale=0.6), FadeIn(anion, scale=0.6), FadeIn(names), run_time=1.2)
    pull = force_line(cation.center_point, anion.center_point, cfg.ATTRACT, width=8, buff=0.9)
    scene.play(Create(pull), run_time=0.8)
    opposite = txt("opposite charges attract", cfg.FONT["label"], cfg.ATTRACT).move_to([3.45, 2.55, 0])
    scene.play(FadeIn(opposite), run_time=0.7)

    # --- 8. Together, the energy drops far more ----------------------------------------------------------------------------------------
    beat(scene, t, 7)
    pair_energy = bd.ion_pair_estimate(bd.NA_CL_DISTANCE_PM["gas molecule"])
    y3 = y2 + pair_energy * PER_KJ
    def follow_ion_labels(m):
        m[0].move_to(cation.center_point() + DOWN * 1.05)
        m[1].move_to(anion.center_point() + DOWN * 1.95)

    names.add_updater(follow_ion_labels)
    scene.play(cation.glide(NA_AT + RIGHT * 1.1), anion.glide(CL_AT + LEFT * 0.85), FadeOut(opposite), run_time=1.4)
    names.clear_updaters()
    drop = energy_step(-0.3, y2, y3, cfg.RELEASED, f"≈ {signed(round(pair_energy, -1))}", side=RIGHT, size=cfg.FONT["label"])
    scene.play(GrowArrow(drop.arrow.arrow), FadeIn(drop.arrow[0]), FadeIn(drop.tag), FadeOut(bill), run_time=1.3)
    estimate = txt("Point-charge estimate", cfg.FONT["tiny"], cfg.MUTED).move_to([-3.7, -3.85, 0])
    scene.play(FadeIn(estimate), run_time=0.5)
    bottom_shelf = level_shelf(y3, -0.7, 0.7, cfg.WHITE)
    scene.play(Create(bottom_shelf.shelf), run_time=0.5)

    # --- 9. The The whole energy balance -------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    whole = chip('The whole energy balance', cfg.GOLD, cfg.FONT["label"]).move_to([3.45, 3.15, 0])
    below = DashedLine([-5.2, y0, 0], [0.9, y0, 0], stroke_color=cfg.GREEN, stroke_width=3, dash_length=0.12)
    scene.play(FadeIn(whole, shift=DOWN * 0.1), run_time=0.8)
    scene.play(ReplacementTransform(guide, below), run_time=0.8)
    scene.play(Indicate(bottom_shelf, color=cfg.GREEN, scale_factor=1.05), Indicate(uphill, color=cfg.WHITE), run_time=1.2)

    # --- 10. Surrounded ----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    pull.clear_updaters()
    ledger = VGroup(start_shelf, up, mid_shelf, down, low_shelf, net, uphill, unit, drop, estimate, bottom_shelf, below)
    scene.play(FadeOut(pull), FadeOut(names), FadeOut(whole), FadeOut(ledger),
               cation.glide(cation.center_point() + LEFT * 3.45), anion.glide(anion.center_point() + LEFT * 3.45), run_time=0.5)
    centre = (cation.center_point() + anion.center_point()) / 2
    neighbours = VGroup()
    for k, angle in enumerate(np.linspace(0, TAU, 6, endpoint=False)):
        kind = "+" if k % 2 else "-"
        neighbour = ion_ball(kind, 0.42 if kind == "-" else 0.3, polished=True)
        neighbour.kind = kind
        neighbour.move_to(centre + 2.4 * np.array([np.cos(angle), np.sin(angle), 0]))
        neighbours.add(neighbour)
    scene.play(LaggedStart(*[FadeIn(n, shift=(centre - n.get_center()) * 0.3) for n in neighbours], lag_ratio=0.15), run_time=1.6)
    surrounded = txt("More than one neighbour", cfg.FONT["label"], cfg.WHITE).move_to([3.45, -2.9, 0])
    scene.play(FadeIn(surrounded, shift=UP * 0.1), run_time=0.7)

    # --- 11. Build a crystal ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(surrounded), run_time=0.8)
    grid = ion_layers(3, 5, 1.15, [0, 0.2, 0], radius=0.46, polished=True)
    # Move each ion to a site of the same sign, preserving its identity.
    rest = [ball for row in grid for ball in row]
    moves = []
    for neighbour in neighbours:
        target = min((ball for ball in rest if ball.kind == neighbour.kind),
                     key=lambda ball: np.linalg.norm(ball.get_center() - neighbour.get_center()))
        rest.remove(target)
        moves.append(ReplacementTransform(neighbour, target))
    scene.play(FadeOut(cation), FadeOut(anion), *moves, run_time=1.4)
    scene.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in rest], lag_ratio=0.12), run_time=2.0)
    scene.remove(*[b for row in grid for b in row])
    scene.add(grid)
    build = txt("one ion at a time", cfg.FONT["body"], cfg.GOLD).move_to([0, -2.6, 0])
    scene.play(FadeIn(build, shift=UP * 0.1), run_time=0.8)
    scene.play(Indicate(grid, color=cfg.WHITE, scale_factor=1.04), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["10"])
