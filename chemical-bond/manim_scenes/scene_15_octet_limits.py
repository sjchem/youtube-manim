"""The octet rule's limits: a duet, an electron-deficient boron, a twelve-electron
Lewis count around sulfur, and a magnetic oxygen.

The counts are drawn, not asserted: every dot that is counted is on screen
inside the ring that counts it. BF3 uses its common introductory Lewis
structure (six electrons on boron). For SF6 the fluorine lone pairs are left
out for clarity, and "twelve" is labelled as the simple Lewis count. Liquid
oxygen's attraction to a magnet (paramagnetism) is the observation the simple
O=O drawing cannot explain; the film defers molecular orbital theory.
"""

from manim_scenes.common import *

SIZE = 104


class Scene15OctetLimits(Scene):
    def construct(self) -> None:
        play_scene(self)


def radial_pairs(centre, direction, count_dirs: Sequence[float], reach: float = 0.58) -> VGroup:
    """Lone pairs around an atom at given angles (radians) — pairs lie across the radius."""
    pairs = VGroup()
    for angle in count_dirs:
        u = np.array([np.cos(angle), np.sin(angle), 0])
        perp = np.array([-u[1], u[0], 0])
        base = np.asarray(centre, dtype=float) + u * reach
        pairs.add(VGroup(e_dot(base + perp * LEWIS_GAP), e_dot(base - perp * LEWIS_GAP)))
    return pairs


def spoke_molecule(centre_symbol: str, angles: Sequence[float], radius: float, lone_pairs: bool, *,
                   centre=ORIGIN, outer: str = "F") -> VGroup:
    centre = np.asarray(centre, dtype=float)
    core = txt(centre_symbol, SIZE, cfg.WHITE).move_to(centre)
    outers, bonds, shared, lones = VGroup(), VGroup(), VGroup(), VGroup()
    for angle in angles:
        u = np.array([np.cos(angle), np.sin(angle), 0])
        perp = np.array([-u[1], u[0], 0])
        spot = centre + u * radius
        outers.add(txt(outer, int(SIZE * 0.85), cfg.GREEN).move_to(spot))
        bonds.add(Line(centre + u * 0.5, spot - u * 0.45, stroke_color=cfg.WHITE, stroke_width=6))
        mid = centre + u * 0.95
        shared.add(VGroup(e_dot(mid + perp * LEWIS_GAP), e_dot(mid - perp * LEWIS_GAP)))
        if lone_pairs:
            lones.add(radial_pairs(spot, u, [angle, angle + PI / 2, angle - PI / 2], reach=0.55))
    group = VGroup(bonds, core, outers, shared, lones)
    group.core, group.outers, group.bonds, group.shared, group.lones = core, outers, bonds, shared, lones
    return group


def magnet() -> VGroup:
    """A rounded horseshoe with an extruded rim and shaded pole faces."""
    radius, half_width, length = 1.05, 0.19, 1.5
    depth = np.array([0.13, -0.10, 0])

    def dark(color, factor):
        return ManimColor(ManimColor(color).to_rgb() * factor)

    def arc_band(width, color):
        return AnnularSector(inner_radius=radius - width / 2, outer_radius=radius + width / 2,
                             angle=PI, start_angle=0, stroke_width=0, fill_color=color, fill_opacity=1)

    # Filled geometry scales with the model; highlights don't remain flat strokes.
    back = VGroup(arc_band(2 * half_width, "#354858").shift(depth))
    arc = VGroup(arc_band(2 * half_width, dark(cfg.MUTED, 0.25)))
    for fraction in np.linspace(0.99, 0.035, 40):
        brightness = 0.28 + 0.72 * np.sqrt(1 - fraction * fraction)
        arc.add(arc_band(2 * half_width * fraction, dark("#D9E7F1", brightness)))

    legs, caps = VGroup(), VGroup()
    for x, color in ((-radius, cfg.BLUE), (radius, cfg.REPEL)):
        back.add(Rectangle(width=2 * half_width, height=length, stroke_width=0,
                           fill_color=dark(color, 0.35), fill_opacity=1).move_to([x, -length / 2, 0]).shift(depth))
        leg = VGroup(Rectangle(width=2 * half_width, height=length, stroke_width=0,
                              fill_color=dark(color, 0.25), fill_opacity=1).move_to([x, -length / 2, 0]))
        for fraction in np.linspace(0.99, 0.035, 40):
            brightness = 0.28 + 0.72 * np.sqrt(1 - fraction * fraction)
            leg.add(Rectangle(width=2 * half_width * fraction, height=length, stroke_width=0,
                              fill_color=dark(color, brightness), fill_opacity=1)
                    .move_to([x - 0.04 * (1 - fraction), -length / 2, 0]))
        legs.add(leg)
        cap = polished_ball(half_width, color, layers=32).stretch(0.32, 1).move_to([x, -length, 0])
        caps.add(cap)
    tags = VGroup(txt("N", cfg.FONT["small"], cfg.WHITE).next_to(legs[1], RIGHT, buff=0.25),
                  txt("S", cfg.FONT["small"], cfg.WHITE).next_to(legs[0], LEFT, buff=0.25))
    gap_anchor = Dot([0, -length, 0], radius=0.002, fill_opacity=0, stroke_width=0)
    group = VGroup(back, arc, legs, caps, tags, gap_anchor)
    group.gap_anchor = gap_anchor
    return group


def oxygen_drop() -> VGroup:
    """A softly lit pale-blue droplet, preserving the oval silhouette."""
    return polished_ball(0.25, "#9FD8FF").stretch(1.32, 1)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "15", "The octet rule's limits")

    # --- 1. It works beautifully — as a pattern -------------------------------------------------------------------
    tiles = VGroup(*[element_tile(pm.z_of(sym), 1.3, fill=0.24) for sym in ("C", "N", "O", "F")]).arrange(RIGHT, buff=0.45)
    tiles.move_to([0, 1.1, 0])
    rings = VGroup(*[octet_ring(tile, 0.95, cfg.GREEN) for tile in tiles])
    scene.play(LaggedStart(*[FadeIn(tile, shift=DOWN * 0.15) for tile in tiles], lag_ratio=0.15), run_time=1.0)
    dismiss_opening_title(scene, t, head)
    scene.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15), run_time=1.0)
    verdict = VGroup(chip("a pattern", cfg.GREEN, cfg.FONT["body"]), chip("a law", cfg.MUTED, cfg.FONT["body"])).arrange(RIGHT, buff=1.4)
    verdict.move_to([0, -1.6, 0])
    scene.play(FadeIn(verdict[0], shift=UP * 0.1), run_time=0.7)
    scene.play(FadeIn(verdict[1], shift=UP * 0.1), run_time=0.6)
    law_strike = strike(verdict[1], cfg.REPEL, 7)
    scene.play(Create(law_strike), run_time=0.6)

    # --- 2. Hydrogen: a duet ------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(FadeOut(VGroup(tiles, rings, verdict, law_strike)), run_time=0.7)
    h_left, h_right = txt("H", SIZE, cfg.WHITE).move_to([-0.9, 0.6, 0]), txt("H", SIZE, cfg.WHITE).move_to([0.9, 0.6, 0])
    pair = VGroup(e_dot([0, 0.6 + LEWIS_GAP, 0]), e_dot([0, 0.6 - LEWIS_GAP, 0]))
    scene.play(FadeIn(h_left), FadeIn(h_right), FadeIn(pair, scale=0.5), run_time=0.8)
    duet_rings = VGroup(octet_ring(h_left, 1.3, cfg.GREEN, shift=LEFT * 0.2),
                       octet_ring(h_right, 1.3, cfg.GREEN, shift=RIGHT * 0.2))
    scene.play(Create(duet_rings), run_time=0.9)
    duet = VGroup(txt("2", 84, cfg.GREEN), txt("A duet", cfg.FONT["label"], cfg.WHITE)).arrange(RIGHT, buff=0.35)
    duet.move_to([0, -1.5, 0])
    scene.play(FadeIn(duet, shift=UP * 0.1), run_time=0.8)

    # --- 3. Boron trifluoride: six, not eight -----------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(VGroup(h_left, h_right, pair, duet_rings, duet)), run_time=0.6)
    bf3 = spoke_molecule("B", [PI / 2, PI / 2 + TAU / 3, PI / 2 - TAU / 3], 2.05, True, centre=[-1.6, 0.0, 0])
    scene.play(FadeIn(bf3.core), LaggedStart(*[Create(b) for b in bf3.bonds], lag_ratio=0.2), FadeIn(bf3.outers), run_time=1.2)
    scene.play(FadeIn(bf3.lones), FadeIn(bf3.shared), run_time=0.9)
    six_ring = octet_ring(bf3.core, 1.28, cfg.REQUIRED)
    six = VGroup(txt("6", 96, cfg.REQUIRED), txt("not 8", cfg.FONT["body"], cfg.REQUIRED)).arrange(RIGHT, buff=0.3).move_to([4.2, 0.9, 0])
    scene.play(Create(six_ring), FadeIn(six, shift=LEFT * 0.15), run_time=1.0)

    # --- 4. Yet perfectly real, and eager for a pair ------------------------------------------------------------------------
    beat(scene, t, 3)
    real = VGroup(check_mark(0.32), txt("Stable BF₃", cfg.FONT["label"], cfg.GREEN)).arrange(RIGHT, buff=0.3).move_to([4.2, -0.2, 0])
    scene.play(FadeIn(real, shift=UP * 0.1), run_time=0.8)
    guest = VGroup(e_dot([0, LEWIS_GAP, 0], cfg.GOLD), e_dot([0, -LEWIS_GAP, 0], cfg.GOLD)).rotate(PI / 2).move_to([2.2, -2.6, 0])
    eager = txt("Can accept a lone pair", cfg.FONT["label"], cfg.GOLD).move_to([4.2, -1.3, 0])
    scene.play(FadeIn(guest, scale=0.4), FadeIn(eager), run_time=0.8)
    scene.play(guest.animate.move_to(bf3.core.get_center() + np.array([0.75, -0.75, 0])), run_time=1.6)
    scene.play(Indicate(guest, color=cfg.WHITE, scale_factor=1.5), run_time=0.8)

    # --- 5. Sulfur hexafluoride: twelve in the Lewis count -------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(VGroup(bf3, six_ring, six, real, guest, eager)), run_time=0.7)
    sf6 = spoke_molecule("S", [k * TAU / 6 for k in range(6)], 2.25, False, centre=[-1.6, 0.0, 0])
    scene.play(FadeIn(sf6.core), LaggedStart(*[Create(b) for b in sf6.bonds], lag_ratio=0.12), FadeIn(sf6.outers), run_time=1.3)
    scene.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in sf6.shared], lag_ratio=0.12), run_time=1.0)
    twelve_ring = octet_ring(sf6.core, 1.42, cfg.PURPLE)
    twelve = VGroup(txt("12", 96, cfg.PURPLE), txt("in the Lewis count", cfg.FONT["label"], cfg.WHITE)).arrange(DOWN, buff=0.15)
    twelve.move_to([4.3, 0.5, 0])
    scene.play(Create(twelve_ring), FadeIn(twelve, shift=LEFT * 0.15), run_time=1.0)
    hidden = txt("Lewis count · not geometry", cfg.FONT["tiny"], cfg.MUTED).move_to([-1.6, -3.3, 0])
    scene.play(FadeIn(hidden), run_time=0.5)

    # --- 6. Period 3 and beyond: more neighbours -----------------------------------------------------------------------------------
    beat(scene, t, 5)
    beyond = chip("period 3 and beyond", cfg.PURPLE, cfg.FONT["label"]).move_to([4.3, -1.25, 0])
    more = txt("more neighbours", cfg.FONT["label"], cfg.WHITE).next_to(beyond, DOWN, buff=0.25)
    scene.play(FadeIn(beyond, shift=UP * 0.1), FadeIn(more), run_time=0.8)
    scene.play(Indicate(sf6.outers, color=cfg.WHITE, scale_factor=1.15), run_time=1.0)

    # --- 7. Oxygen: the drawing shows every electron paired --------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(VGroup(sf6, twelve_ring, twelve, hidden, beyond, more)), run_time=0.7)
    o_left = LewisAtom("O", {"up": 2, "left": 2}, size=SIZE, center=[-1.25, 0.5, 0], reach=0.26)
    o_right = LewisAtom("O", {"up": 2, "right": 2}, size=SIZE, center=[1.25, 0.5, 0], reach=0.26)
    double = bond_lines(o_left.symbol, o_right.symbol, 2, width=8, gap=0.2)
    scene.play(FadeIn(o_left), FadeIn(o_right), Create(double), run_time=0.9)
    paired = txt("every electron paired?", cfg.FONT["body"], cfg.WHITE).move_to([0, -1.2, 0])
    scene.play(FadeIn(paired, shift=UP * 0.1), run_time=0.8)

    # --- 8. Liquid oxygen sticks to a magnet ---------------------------------------------------------------------------------------
    beat(scene, t, 7)
    o2 = VGroup(o_left, o_right, double)
    scene.play(o2.animate.scale(0.7).move_to([-4.3, 1.4, 0]), paired.animate.scale(0.8).move_to([-4.3, 0.1, 0]), run_time=0.9)
    pole = magnet().scale(1.25).move_to([2.6, 1.3, 0])
    gap = pole.gap_anchor.get_center()
    drops = VGroup(*[oxygen_drop()
                     .move_to(gap + np.array([dx, -dy, 0])) for dx, dy in ((-0.75, 0.15), (-0.25, 0.32), (0.25, 0.3), (0.75, 0.15), (0.0, 0.7))])
    scene.play(FadeIn(pole), run_time=0.7)
    scene.play(LaggedStart(*[FadeIn(d, shift=UP * 0.6) for d in drops], lag_ratio=0.2), run_time=1.2)
    sticks = txt("Liquid O₂ is magnetic", cfg.FONT["label"], cfg.BLUE).move_to([2.6, -1.95, 0])
    scene.play(FadeIn(sticks), run_time=0.7)
    unpaired = VGroup(Arrow(DOWN * 0.35, UP * 0.35, buff=0, color=cfg.SPIN_UP, stroke_width=9, max_tip_length_to_length_ratio=0.35),
                      Arrow(DOWN * 0.35, UP * 0.35, buff=0, color=cfg.SPIN_UP, stroke_width=9, max_tip_length_to_length_ratio=0.35))
    unpaired.arrange(RIGHT, buff=0.35).move_to([2.3, -2.9, 0])
    unpaired_tag = txt("Two unpaired electrons", cfg.FONT["small"], cfg.WHITE).next_to(unpaired, LEFT, buff=0.35)
    scene.play(GrowArrow(unpaired[0]), GrowArrow(unpaired[1]), FadeIn(unpaired_tag), run_time=0.9)
    scene.play(Create(strike(paired, cfg.REPEL, 6)), run_time=0.6)

    # --- 9. A job for molecular orbital theory --------------------------------------------------------------------------------------
    beat(scene, t, 8)
    later = chip("Beyond this model:\nMO theory", cfg.PURPLE, cfg.FONT["label"]).move_to([-4.1, 3.05, 0])
    scene.play(FadeIn(later, shift=DOWN * 0.1), run_time=0.8)
    drop_centre = drops.get_center()
    scene.play(Wiggle(drops, scale_value=1.15, scale_about_point=drop_centre,
                      rotate_about_point=drop_centre), run_time=1.0)

    # --- 10. A shortcut; the rule underneath is energy ----------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(Group(*[m for m in scene.mobjects if not getattr(m, "_is_project_background", False)])), run_time=0.8)
    shortcut = VGroup(check_mark(0.34), txt("Octet rule: useful shortcut", cfg.FONT["body"], cfg.GREEN)).arrange(RIGHT, buff=0.3)
    counting = VGroup(cross_mark(0.3), txt("Eight explains everything", cfg.FONT["body"], cfg.MUTED)).arrange(RIGHT, buff=0.3)
    VGroup(shortcut, counting).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([0, 1.5, 0])
    scene.play(FadeIn(shortcut, shift=UP * 0.1), run_time=0.9)
    scene.play(FadeIn(counting, shift=UP * 0.1), run_time=0.9)
    axes = Axes(x_range=[0, 320, 100], y_range=[-500, 400, 200], x_length=4.6, y_length=2.4, tips=False,
                axis_config={"stroke_color": cfg.MUTED, "stroke_width": 2, "include_ticks": False}).move_to([0, -1.6, 0])
    curve = axes.plot(lambda r: float(bm.morse(r, *H2)), x_range=[bm.morse_inverse(380, *H2), 320, 1], color=cfg.ENERGY,
                      stroke_width=6, use_smoothing=False)
    lowest = txt("Lower energy binds", cfg.FONT["label"], cfg.ENERGY).next_to(axes, RIGHT, buff=0.4)
    scene.play(FadeIn(axes), Create(curve), run_time=1.4)
    marble = VGroup(halo(0.4, cfg.ENERGY, layers=6, peak_opacity=0.13),
                    polished_ball(0.14, cfg.ENERGY)).move_to(axes.c2p(300, 0))
    path = axes.plot(lambda r: float(bm.morse(r, *H2)), x_range=[H2[1], 300, 1]).reverse_points()
    scene.play(FadeIn(marble), FadeIn(lowest, shift=LEFT * 0.1), run_time=0.6)
    scene.play(MoveAlongPath(marble, path), run_time=2.2, rate_func=rush_into)
    scene.play(Flash(marble, color=cfg.ENERGY, line_length=0.3, num_lines=10), run_time=0.8)
    scene.play(Indicate(lowest, color=cfg.WHITE, scale_factor=1.06), run_time=1.2)
    scene.play(Circumscribe(shortcut, color=cfg.GREEN, fade_out=True), run_time=1.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["15"])
