"""Sharing electrons: H2, Cl2, O2, N2 and bond order.

The hydrogen molecule is the same PairCloud as chapters 01 and 03, so the
Lewis dots are introduced *on top of* a cloud the viewer already trusts — and
are then dissolved back into it ("not two balls"). The Lewis drawings move
the actual unpaired dots into the shared positions, so each bond is visibly
one electron from each atom. Valence counts come from ``utils.bond_data``.
"""

from manim_scenes.common import *

CLOUD_Y = 0.75
LEWIS_Y = 0.35
SIZE = 110


class Scene07Covalent(Scene):
    def construct(self) -> None:
        play_scene(self)


def share_pairs(scene: Scene, left: LewisAtom, right: LewisAtom, donors: list[tuple[VGroup, VGroup]],
                spacing: float, run_time: float = 1.4) -> list[VGroup]:
    """Bring two atoms together and move each (left, right) electron pair between them."""
    scene.play(left.animate.move_to([-spacing, LEWIS_Y, 0]), right.animate.move_to([spacing, LEWIS_Y, 0]), run_time=1.0)
    columns = pair_targets(left.symbol, right.symbol, len(donors), column_gap=0.34)
    moves, pairs = [], []
    for (from_left, from_right), (top, bottom) in zip(donors, columns):
        for atom, dot in ((left, from_left), (right, from_right)):
            for group in atom.slots.values():
                if dot in group.submobjects:
                    group.remove(dot)   # the electron now belongs to the bond, not the atom
        moves += [from_left.animate.move_to(top), from_right.animate.move_to(bottom)]
        pair = VGroup(from_left, from_right)
        scene.add(pair)
        pairs.append(pair)
    scene.play(*moves, run_time=run_time)
    return pairs


def to_lines(scene: Scene, left: LewisAtom, right: LewisAtom, pairs: list[VGroup], run_time: float = 1.0) -> VGroup:
    lines = bond_lines(left.symbol, right.symbol, len(pairs), width=8, gap=0.2)
    scene.play(*[ReplacementTransform(pair, line) for pair, line in zip(pairs, lines)], run_time=run_time)
    return lines


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "07", "Sharing electrons")

    # --- 1. Two hydrogen atoms, one electron each -------------------------------------------------------
    gap = ValueTracker(5.6)
    cloud = bind_pair(PairCloud(LEFT, RIGHT, 1.45, count=640, seed=71, glow=0.17, dot_radius=0.034), gap.get_value,
                      UP * CLOUD_Y)
    scene.add(cloud)
    nuclei = pair_nuclei(cloud, ("+", "+"), radius=0.28)
    scene.play(FadeIn(cloud), FadeIn(nuclei, scale=0.6), run_time=1.2)
    dismiss_opening_title(scene, t, head)

    # --- 2. The clouds merge ---------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(track(gap, 2.2), cloud.share_to(1.0), run_time=3.2, rate_func=smooth)
    spread = txt("Two electrons, shared density", cfg.FONT["label"], cfg.CYAN).move_to([0, -2.1, 0])
    scene.play(FadeIn(spread, shift=UP * 0.1), run_time=0.8)

    # --- 3. Density between the nuclei, attracted by both -----------------------------------------------------
    beat(scene, t, 2)
    middle = glow_dot(UP * CLOUD_Y, 0.16, cfg.WHITE)
    to_left = force_line(middle.get_center, lambda: cloud.ends[0].get_center(), cfg.ATTRACT, width=8, buff=0.3)
    to_right = force_line(middle.get_center, lambda: cloud.ends[1].get_center(), cfg.ATTRACT, width=8, buff=0.3)
    scene.play(FadeOut(spread), FadeIn(middle, scale=0.4), run_time=0.7)
    scene.play(Create(to_left), Create(to_right), run_time=1.0)
    both = txt("attracted by both nuclei", cfg.FONT["label"], cfg.ATTRACT).move_to([0, -2.1, 0])
    scene.play(FadeIn(both, shift=UP * 0.1), Indicate(middle, color=cfg.ATTRACT, scale_factor=1.5), run_time=1.0)
    scene.play(Indicate(middle, color=cfg.WHITE, scale_factor=1.4), run_time=1.0)

    # --- 4. That is the covalent bond -------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(both), FadeOut(middle), line_gain(to_left, 0), line_gain(to_right, 0), run_time=0.6)
    to_left.clear_updaters()
    to_right.clear_updaters()
    scene.remove(to_left, to_right)
    covalent = chip("Covalent: a shared pair", cfg.CYAN, cfg.FONT["body"]).move_to([0, 3.1, 0])
    scene.play(FadeIn(covalent, shift=DOWN * 0.15), run_time=0.9)
    scene.play(cloud.fade_to(1.35), run_time=0.8)
    scene.play(cloud.fade_to(1.0), run_time=0.8)

    # --- 5. Drawn as a line, or as a pair of dots -----------------------------------------------------------------
    beat(scene, t, 4)
    line_form = VGroup(txt("H", 96, cfg.WHITE), Line(LEFT * 0.55, RIGHT * 0.55, stroke_color=cfg.WHITE, stroke_width=9),
                       txt("H", 96, cfg.WHITE)).arrange(RIGHT, buff=0.22).move_to([-3.4, -2.35, 0])
    dot_left, dot_right = txt("H", 96, cfg.WHITE), txt("H", 96, cfg.WHITE)
    VGroup(dot_left, dot_right).arrange(RIGHT, buff=0.95).move_to([3.4, -2.35, 0])
    pair_dots = VGroup(e_dot(dot_left.get_right() + RIGHT * 0.47 + UP * LEWIS_GAP),
                       e_dot(dot_left.get_right() + RIGHT * 0.47 + DOWN * LEWIS_GAP))
    scene.play(FadeIn(line_form, shift=UP * 0.15), run_time=0.9)
    scene.play(FadeIn(VGroup(dot_left, dot_right), shift=UP * 0.15), FadeIn(pair_dots, scale=0.5), run_time=0.9)
    same = eq("=", cfg.FONT["title"], cfg.MUTED).move_to([0, -2.35, 0])
    scene.play(FadeIn(same), run_time=0.5)

    # --- 6. Not two balls: two electrons spread through the cloud -------------------------------------------------
    beat(scene, t, 5)
    balls = VGroup(glow_dot(UP * CLOUD_Y + UP * 0.22, 0.13), glow_dot(UP * CLOUD_Y + DOWN * 0.22, 0.13))
    scene.play(TransformFromCopy(pair_dots, balls), run_time=1.2)
    not_balls = txt("Dots are symbols", cfg.FONT["label"], cfg.REPEL).move_to([0, -0.95, 0])
    scene.play(FadeIn(not_balls), Wiggle(balls, scale_value=1.3), run_time=1.1)
    scene.play(balls.animate.set_opacity(0).scale(4), cloud.fade_to(1.5), run_time=1.6)
    spread_out = txt("Two electrons, one cloud", cfg.FONT["label"], cfg.CYAN).move_to([0, -0.95, 0])
    scene.play(FadeThrough(not_balls, spread_out), cloud.fade_to(1.0), run_time=1.0)
    scene.remove(balls)

    # --- 7. Opposite spins -------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    spins = VGroup(Arrow(DOWN * 0.45, UP * 0.45, buff=0, color=cfg.SPIN_UP, stroke_width=10, max_tip_length_to_length_ratio=0.35),
                   Arrow(UP * 0.45, DOWN * 0.45, buff=0, color=cfg.SPIN_DOWN, stroke_width=10, max_tip_length_to_length_ratio=0.35))
    spins.arrange(RIGHT, buff=0.3).move_to([4.9, CLOUD_Y, 0])
    opposite = txt("opposite spins", cfg.FONT["label"], cfg.WHITE).next_to(spins, DOWN, buff=0.3)
    scene.play(FadeOut(spread_out), GrowArrow(spins[0]), run_time=0.7)
    scene.play(GrowArrow(spins[1]), FadeIn(opposite, shift=UP * 0.1), run_time=0.8)
    region = txt("One bonding orbital", cfg.FONT["small"], cfg.MUTED).next_to(opposite, DOWN, buff=0.2)
    scene.play(FadeIn(region), Indicate(spins, color=cfg.WHITE, scale_factor=1.15), run_time=1.0)

    # --- 8. Chlorine: seven valence electrons ------------------------------------------------------------------------
    beat(scene, t, 7)
    cloud.clear_updaters()
    for core in nuclei:
        core.clear_updaters()
    scene.play(FadeOut(VGroup(cloud, nuclei, covalent, line_form, dot_left, dot_right, pair_dots, same, spins, opposite, region)),
               run_time=0.8)
    cl_left = LewisAtom("Cl", {"up": 2, "left": 2, "down": 2, "right": 1}, size=SIZE, center=[-3.4, LEWIS_Y, 0], reach=0.26)
    cl_right = LewisAtom("Cl", {"up": 2, "right": 2, "down": 2, "left": 1}, size=SIZE, center=[3.4, LEWIS_Y, 0], reach=0.26)
    scene.play(FadeIn(cl_left, shift=RIGHT * 0.3), FadeIn(cl_right, shift=LEFT * 0.3), run_time=1.0)
    sevens = VGroup(txt("7", 72, cfg.ELECTRON_COLOR).next_to(cl_left, DOWN, buff=0.45),
                    txt("7", 72, cfg.ELECTRON_COLOR).next_to(cl_right, DOWN, buff=0.45))
    scene.play(FadeIn(sevens, shift=UP * 0.1), run_time=0.7)
    singles = VGroup(cl_left.slots["right"][0], cl_right.slots["left"][0])
    scene.play(Indicate(singles, color=cfg.GOLD, scale_factor=1.8), run_time=1.2)

    # --- 9. The singles pair up: one shared pair ----------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(sevens), run_time=0.4)
    pairs = share_pairs(scene, cl_left, cl_right, [(cl_left.slots["right"][0], cl_right.slots["left"][0])], 1.2)
    single_bond = txt("One pair → single bond", cfg.FONT["label"], cfg.CYAN).move_to([0, -2.4, 0])
    scene.play(FadeIn(single_bond, shift=UP * 0.1), run_time=0.8)

    # --- 10. Lone pairs ---------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    lone = VGroup(*[cl_left.slots[s] for s in ("up", "left", "down")], *[cl_right.slots[s] for s in ("up", "right", "down")])
    halos = VGroup(*[RoundedRectangle(width=p.width + 0.3, height=p.height + 0.3, corner_radius=0.15, stroke_color=cfg.GOLD,
                                      stroke_width=3, fill_opacity=0).move_to(p) for p in lone])
    scene.play(FadeOut(single_bond), LaggedStart(*[Create(h) for h in halos], lag_ratio=0.1), run_time=1.4)
    lone_tag = txt("Lone pairs", cfg.FONT["label"], cfg.GOLD).move_to([0, -2.4, 0])
    scene.play(FadeIn(lone_tag, shift=UP * 0.1), run_time=0.8)
    scene.play(Indicate(lone, color=cfg.GOLD, scale_factor=1.25), run_time=1.0)

    # --- 11. Count around either chlorine: eight -----------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(halos), FadeOut(lone_tag), run_time=0.5)
    ring_left = octet_ring(cl_left.symbol, 1.12, cfg.GREEN, shift=RIGHT * 0.2)
    ring_right = octet_ring(cl_right.symbol, 1.12, cfg.GREEN, shift=LEFT * 0.2)
    scene.play(Create(ring_left), run_time=0.9)
    eight_left = txt("6 + 2 = 8", cfg.FONT["label"], cfg.GREEN).next_to(ring_left, DOWN, buff=0.3).shift(LEFT * 1.1)
    scene.play(FadeIn(eight_left, shift=UP * 0.1), run_time=0.7)
    scene.play(Create(ring_right), run_time=0.9)
    eight_right = txt("6 + 2 = 8", cfg.FONT["label"], cfg.GREEN).next_to(ring_right, DOWN, buff=0.3).shift(RIGHT * 1.1)
    scene.play(FadeIn(eight_right, shift=UP * 0.1), Indicate(pairs[0], color=cfg.WHITE, scale_factor=1.4), run_time=1.0)

    # --- 12. Oxygen: two short ------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    scene.play(FadeOut(VGroup(cl_left, cl_right, *pairs, ring_left, ring_right, eight_left, eight_right)), run_time=0.7)
    o_left = LewisAtom("O", {"up": 2, "left": 2, "right": 1, "down": 1}, size=SIZE, center=[-3.4, LEWIS_Y, 0], reach=0.26)
    o_right = LewisAtom("O", {"up": 2, "right": 2, "left": 1, "down": 1}, size=SIZE, center=[3.4, LEWIS_Y, 0], reach=0.26)
    scene.play(FadeIn(o_left, shift=RIGHT * 0.3), FadeIn(o_right, shift=LEFT * 0.3), run_time=1.0)
    sixes = VGroup(txt("6", 72, cfg.ELECTRON_COLOR).next_to(o_left, DOWN, buff=0.45),
                   txt("6", 72, cfg.ELECTRON_COLOR).next_to(o_right, DOWN, buff=0.45))
    short = chip("two short of eight", cfg.MUTED, cfg.FONT["label"]).move_to([0, 2.6, 0])
    scene.play(FadeIn(sixes, shift=UP * 0.1), FadeIn(short, shift=DOWN * 0.1), run_time=0.9)
    unpaired = VGroup(o_left.slots["right"][0], o_left.slots["down"][0], o_right.slots["left"][0], o_right.slots["down"][0])
    scene.play(Indicate(unpaired, color=cfg.GOLD, scale_factor=1.8), run_time=1.2)

    # --- 13. Two shared pairs: a double bond -------------------------------------------------------------------------------------
    beat(scene, t, 12)
    scene.play(FadeOut(sixes), FadeOut(short), run_time=0.4)
    o_pairs = share_pairs(scene, o_left, o_right, [(o_left.slots["right"][0], o_right.slots["left"][0]),
                                                   (o_left.slots["down"][0], o_right.slots["down"][0])], 1.25, run_time=1.2)
    o_lines = to_lines(scene, o_left, o_right, o_pairs, run_time=0.9)
    double = txt("double bond", cfg.FONT["label"], cfg.CYAN).move_to([0, -2.2, 0])
    scene.play(FadeIn(double), run_time=0.5)
    o2 = VGroup(o_left, o_right, o_lines)

    # --- 14. Nitrogen: three shared pairs, a triple bond -----------------------------------------------------------------------
    beat(scene, t, 13)
    scene.play(o2.animate.scale(0.55).move_to([-4.6, 2.55, 0]), FadeOut(double), run_time=0.8)
    n_left = LewisAtom("N", {"left": 2, "up": 1, "right": 1, "down": 1}, size=SIZE, center=[-3.4, LEWIS_Y, 0], reach=0.26)
    n_right = LewisAtom("N", {"right": 2, "up": 1, "left": 1, "down": 1}, size=SIZE, center=[3.4, LEWIS_Y, 0], reach=0.26)
    scene.play(FadeIn(n_left, shift=RIGHT * 0.3), FadeIn(n_right, shift=LEFT * 0.3), run_time=0.8)
    n_pairs = share_pairs(scene, n_left, n_right, [(n_left.slots["up"][0], n_right.slots["up"][0]),
                                                   (n_left.slots["right"][0], n_right.slots["left"][0]),
                                                   (n_left.slots["down"][0], n_right.slots["down"][0])], 1.3, run_time=1.2)
    n_lines = to_lines(scene, n_left, n_right, n_pairs, run_time=0.9)
    triple = txt("Triple bond", cfg.FONT["label"], cfg.CYAN).move_to([0, -2.2, 0])
    scene.play(FadeIn(triple), run_time=0.6)
    n2 = VGroup(n_left, n_right, n_lines)

    # --- 15. Bond order ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 14)
    h_line = VGroup(txt("H", SIZE, cfg.WHITE), Line(LEFT * 0.6, RIGHT * 0.6, stroke_color=cfg.WHITE, stroke_width=8),
                    txt("H", SIZE, cfg.WHITE)).arrange(RIGHT, buff=0.24)
    scene.play(FadeOut(triple), FadeOut(o2), FadeOut(n2), run_time=0.4)
    targets = [np.array([-1.0, y, 0]) for y in (2.0, 0.2, -1.75)]
    h_line.scale(0.7).move_to(targets[0])
    o2.scale(1.0 / 0.55 * 0.7).move_to(targets[1])
    n2.scale(0.7).move_to(targets[2])
    scene.play(FadeIn(h_line), FadeIn(o2), FadeIn(n2), run_time=1.2)
    orders = VGroup(*[txt(str(k), 84, cfg.GOLD).move_to([3.6, target[1], 0]) for k, target in zip((1, 2, 3), targets)])
    order_tag = chip("bond order", cfg.GOLD, cfg.FONT["label"]).move_to([3.6, 3.25, 0])
    scene.play(FadeIn(order_tag, shift=DOWN * 0.1), LaggedStart(*[FadeIn(o, scale=0.6) for o in orders], lag_ratio=0.3), run_time=1.4)

    # --- 16. The puzzle: are the two pairs of a double bond the same? ---------------------------------------------------------------
    beat(scene, t, 15)
    scene.play(FadeOut(VGroup(h_line, n2, orders[0], orders[2])), o2.animate.scale(1.5).move_to([0, 0.5, 0]),
               orders[1].animate.move_to([3.9, 0.5, 0]), run_time=1.1)
    first, second = o_lines
    scene.play(first.animate.set_stroke(cfg.SIGMA_COLOR, width=11), second.animate.set_stroke(cfg.PI_COLOR, width=11), run_time=0.9)
    puzzle = txt("the same?", cfg.FONT["title"], cfg.GOLD).move_to([0, -1.85, 0])
    question = txt("?", 110, cfg.GOLD).next_to(o2, UP, buff=0.35)
    scene.play(FadeIn(puzzle, shift=UP * 0.15), FadeIn(question, scale=0.5), run_time=0.9)
    scene.play(Wiggle(VGroup(first, second), scale_value=1.15), run_time=1.3)
    scene.play(Indicate(first, color=cfg.WHITE), run_time=0.9)
    scene.play(Indicate(second, color=cfg.WHITE), run_time=0.9)

    # --- 17. Look at the orbitals -----------------------------------------------------------------------------------------------------
    beat(scene, t, 16)
    scene.play(FadeOut(VGroup(puzzle, question, orders[1], order_tag)), o2.animate.move_to([0, 2.3, 0]).scale(0.75), run_time=0.9)
    lobes = VGroup()
    for x in (-1.7, 1.7):
        lobes.add(Ellipse(width=1.35, height=2.0, stroke_color=cfg.PI_COLOR, stroke_width=4, fill_color=cfg.PI_COLOR,
                          fill_opacity=0.25).move_to([x, -0.45, 0]))
        lobes.add(Ellipse(width=1.35, height=2.0, stroke_color=cfg.PI_COLOR, stroke_width=4, fill_color=cfg.PI_COLOR,
                          fill_opacity=0.25).move_to([x, -2.45, 0]))
    cores = VGroup(*[nucleus_core(None, 0.16).move_to([x, -1.45, 0]) for x in (-1.7, 1.7)])
    scene.play(FadeIn(cores), LaggedStart(*[GrowFromCenter(l) for l in lobes], lag_ratio=0.2), run_time=1.6)
    orbitals = txt("Orbital overlap", cfg.FONT["body"], cfg.PI_COLOR).move_to([4.9, -1.45, 0])
    scene.play(FadeIn(orbitals, shift=LEFT * 0.15), run_time=0.8)
    side = txt("side by side?", cfg.FONT["label"], cfg.MUTED).move_to([-4.9, -1.45, 0])
    scene.play(FadeIn(side, shift=RIGHT * 0.15), run_time=0.8)
    scene.play(VGroup(lobes[0], lobes[1]).animate.shift(RIGHT * 0.75), VGroup(lobes[2], lobes[3]).animate.shift(LEFT * 0.75),
               cores[0].animate.shift(RIGHT * 0.75), cores[1].animate.shift(LEFT * 0.75), run_time=3.0)
    scene.play(Indicate(lobes, color=cfg.WHITE, scale_factor=1.05), run_time=1.2)
    scene.play(Wiggle(orbitals, scale_value=1.06), run_time=1.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["07"])
