"""Chapter 13 — two orderings, and the s-p mixing that swaps them.

Both diagrams come from ``mo_models``. The gap axis uses measured average
2s-2p separations (``mo_data.ORBITAL_ENERGY_EV``); as the marker slides, the
diagram is redrawn at mixing strength ``mo_models.mixing_from_gap(gap)`` —
a saturating toy map whose only job is to show the trend: weak mixing at a
large gap (O, F order), strong mixing at a small gap (B, C, N order). Level
spacing is schematic.
"""

from manim_scenes.common import *

GAP_AXIS = PlotFrame([1.3, -1.35, 0], 0.27, 1.0)       # x = gap in eV
ELEMENTS = ("B", "C", "N", "O", "F")
SHIFT = np.array([-6.5, 0.3, 0])                        # the right diagram moves to centre stage


class Scene13Orderings(Scene):
    def construct(self) -> None:
        play_scene(self)


class OrderingDiagram(MODiagram):
    """Keep sigma 2p outside the wider pi pair, including at a crossing."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._place_label("s2p")

    def _place_label(self, key: str) -> None:
        super()._place_label(key)
        if key == "s2p" and "p2p" in self.levels:
            self.labels[key].next_to(self.levels["p2p"], RIGHT, buff=0.35)
            self.labels[key].set_y(self.levels[key].get_y())


def mo_only(kind: str, x: float, mixing: float | None = None, height: float = 6.1, y: float = -0.4) -> MODiagram:
    return OrderingDiagram(mo.diagram(kind, mixing=mixing), center=[x, y, 0], height=height, ao_x=1.25, mo_width=0.78,
                     gap=0.22, aos=False, axis=False)


def crossing_gap() -> float:
    """The 2s-2p gap at which the toy mixing equals the crossing strength."""
    m = mo.crossing_mixing()
    return mo.MIXING_G0_EV * (1 / m - 1) ** (1 / mo.MIXING_POWER)


def slide_gap(diagram: MODiagram, gap: ValueTracker, target: float) -> Param:
    """Move the gap marker and redraw the diagram at the matching toy mixing strength."""
    def put(v):
        gap.set_value(v)
        diagram.set_energies(mo.diagram("unmixed", mixing=mo.mixing_from_gap(v)))
    return Param(diagram, gap.get_value, put, target)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "13", "Two orderings")

    # --- 1. Two versions of the same diagram ------------------------------------------------------------------------------
    left = mo_only("mixed", -3.6)
    right = mo_only("unmixed", 3.6)
    left_title = eq(r"\mathrm{B_2,\ C_2,\ N_2}", cfg.FONT["body"], cfg.WHITE).move_to([-3.6, 3.2, 0])
    right_title = eq(r"\mathrm{O_2,\ F_2}", cfg.FONT["body"], cfg.WHITE).move_to([3.6, 3.2, 0])
    divider = DashedLine([0, 2.9, 0], [0, -3.0, 0], stroke_color=cfg.MUTED, stroke_width=3)
    scene.play(FadeIn(left), FadeIn(right), Create(divider), run_time=1.4)
    dismiss_opening_title(scene, t, head, at=2.4)
    scene.play(FadeIn(left_title), FadeIn(right_title), run_time=0.8)

    # --- 2. Left: pi below sigma 2p --------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    lbox = glow_frame(VGroup(left.level_group("p2p", links=False), left.level_group("s2p", links=False)), cfg.GOLD, buff=0.15)
    scene.play(Create(lbox), run_time=0.8)
    lnote = txt("pi\nbelow\nsigma", cfg.FONT["small"], cfg.GOLD).next_to(lbox, LEFT, buff=0.3)
    scene.play(FadeIn(lnote), run_time=0.6)

    # --- 3. Right: sigma 2p below pi -------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    rbox = glow_frame(VGroup(right.level_group("p2p", links=False), right.level_group("s2p", links=False)), cfg.GOLD, buff=0.15)
    scene.play(Create(rbox), run_time=0.8)
    rnote = txt("sigma\nbelow\npi", cfg.FONT["small"], cfg.GOLD).next_to(rbox, RIGHT, buff=0.6)
    scene.play(FadeIn(rnote), run_time=0.6)

    # --- 4. Why would the order change? -----------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    why = result_label("Why?", cfg.GOLD, cfg.FONT["title"]).move_to([0, -3.45, 0])
    scene.play(FadeIn(why, scale=1.2), run_time=0.8)

    # --- 5. Same symmetry can mix: sigma 2s and sigma 2p ----------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(*[FadeOut(m) for m in (left, left_title, lbox, lnote, rbox, rnote, divider, why, right_title)],
               run_time=0.6)
    scene.play(right.animate.shift(SHIFT), run_time=0.8)
    right.anchor = right.anchor + SHIFT     # keep set_energies() on the moved diagram
    centre = right
    sig_frames = VGroup(centre.highlight("s2s", cfg.CYAN, buff=0.12), centre.highlight("s2p", cfg.CYAN, buff=0.12))
    same = VGroup(txt("both sigma:", cfg.FONT["body"], cfg.CYAN), txt("round about the axis", cfg.FONT["small"], cfg.CYAN))
    same.arrange(DOWN, buff=0.15).move_to([3.6, 1.9, 0])
    scene.play(Create(sig_frames), FadeIn(same), run_time=1.2)

    # --- 6. Close energies push apart -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    push_down = glow_arrow(centre.levels["s2s"].get_left() + LEFT * 0.35 + UP * 0.1,
                           centre.levels["s2s"].get_left() + LEFT * 0.35 + DOWN * 0.42, cfg.CYAN, width=6)
    push_up = glow_arrow(centre.levels["s2p"].get_left() + LEFT * 0.35 + DOWN * 0.1,
                         centre.levels["s2p"].get_left() + LEFT * 0.35 + UP * 0.8, cfg.CYAN, width=6)
    pushes = caption("Lower one pushed down, upper one pushed up", cfg.CYAN)
    scene.play(GrowArrow(push_down[1]), FadeIn(push_down[0]), GrowArrow(push_up[1]), FadeIn(push_up[0]), FadeIn(pushes),
               run_time=1.4)

    # --- 7. s-p mixing depends on the atom's 2s-2p gap ----------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    name = result_label("s–p mixing", cfg.PURPLE, cfg.FONT["title"]).move_to([3.6, 1.9, 0])
    scene.play(fade_through(same, name), run_time=1.0)
    scene.remove(same)
    gap_word = txt("strength depends on the atom's 2s–2p gap", cfg.FONT["small"], cfg.WHITE).next_to(name, DOWN, buff=0.3)
    fit_width(gap_word, 6.6)
    scene.play(FadeIn(gap_word), run_time=0.8)

    # --- 8. Across the period, the gap grows ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    track = Line(GAP_AXIS.point(4.5, 0), GAP_AXIS.point(22.6, 0), stroke_color=cfg.MUTED, stroke_width=6)
    axis_name = txt("2s–2p gap (eV)", cfg.FONT["small"], cfg.MUTED).next_to(track, DOWN, buff=1.0)
    ticks = VGroup()
    for symbol in ELEMENTS:
        gap = md.gap_ev(symbol)
        x = GAP_AXIS.point(gap, 0)
        tick = VGroup(Line(x + DOWN * 0.15, x + UP * 0.15, stroke_color=cfg.WHITE, stroke_width=4),
                      txt(symbol, cfg.FONT["body"], cfg.WHITE).move_to(x + UP * 0.75),
                      txt(f"{gap:.0f}", cfg.FONT["tiny"], cfg.MUTED).move_to(x + DOWN * 0.38))
        ticks.add(tick)
    scene.play(FadeOut(pushes), FadeOut(gap_word), Create(track), FadeIn(axis_name), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(tk, shift=UP * 0.15) for tk in ticks], lag_ratio=0.35), run_time=2.4)

    # --- 9. Large gap: weak mixing, oxygen's order -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    gap = ValueTracker(md.gap_ev("F"))
    marker = VGroup(Triangle(stroke_width=0, fill_color=cfg.GOLD, fill_opacity=1).scale(0.18).rotate(PI),
                    halo(0.3, cfg.GOLD, layers=4, peak_opacity=0.25))
    marker.add_updater(lambda m: m.move_to(GAP_AXIS.point(gap.get_value(), 0) + UP * 1.4))
    live_mix = slide_gap(centre, gap, md.gap_ev("O"))
    scene.play(FadeOut(sig_frames), FadeOut(push_down), FadeOut(push_up), FadeIn(marker), run_time=0.8)
    centre.set_energies(mo.diagram("unmixed", mixing=mo.mixing_from_gap(gap.get_value())))
    scene.play(live_mix, run_time=2.4, rate_func=smooth)
    weak = caption("Large gap: weak mixing; sigma 2p stays below pi", cfg.WHITE)
    order_o = glow_frame(VGroup(centre.level_group("p2p", links=False), centre.level_group("s2p", links=False)), cfg.GOLD,
                         buff=0.15)
    scene.play(FadeIn(weak), Create(order_o), run_time=1.0)

    # --- 10. Shrink the gap: sigma 2p climbs past pi ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    to_b = slide_gap(centre, gap, md.gap_ev("B"))
    strong = caption("Smaller gap: stronger push; sigma 2p crosses above pi", cfg.CYAN)
    scene.play(FadeOut(order_o), fade_through(weak, strong), run_time=0.8)
    scene.remove(weak)
    scene.play(to_b, run_time=5.0, rate_func=smooth)
    order_n = glow_frame(VGroup(centre.level_group("p2p", links=False), centre.level_group("s2p", links=False)), cfg.GOLD,
                         buff=0.15)
    scene.play(Create(order_n), run_time=0.8)

    # --- 11. The crossing: between nitrogen and oxygen ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    g_star = crossing_gap()
    band = Rectangle(width=(md.gap_ev("O") - md.gap_ev("N")) * GAP_AXIS.xscale, height=0.9, stroke_width=0,
                     fill_color=cfg.PURPLE, fill_opacity=0.25).move_to(GAP_AXIS.point((md.gap_ev("O") + md.gap_ev("N")) / 2, 0))
    back = slide_gap(centre, gap, g_star)
    scene.play(FadeOut(order_n), FadeIn(band), FadeOut(strong), run_time=0.8)
    scene.play(back, run_time=2.4, rate_func=smooth)
    level = glow_frame(VGroup(centre.levels["p2p"], centre.levels["s2p"]), cfg.PURPLE, buff=0.12)
    scene.play(Create(level), run_time=0.6)

    # --- 12. A simplified picture of a real push -----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    honest = chip("Toy model: real energies come from calculation and spectroscopy", cfg.PURPLE)
    fit_width(honest, 13.8)
    honest.move_to([0, -3.65, 0])
    scene.play(FadeOut(level), FadeIn(honest, shift=UP * 0.15), run_time=1.0)
    for target in (md.gap_ev("N"), md.gap_ev("O"), md.gap_ev("N")):
        scene.play(slide_gap(centre, gap, target), run_time=2.2, rate_func=smooth)

    # --- 13. Choose the ordering, then fill ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    marker.clear_updaters()
    scene.play(*[FadeOut(m) for m in (marker, track, axis_name, ticks, band, honest, name, centre)], run_time=1.0)
    final_left, final_right = mo_only("mixed", -3.6, height=5.6, y=-0.3), mo_only("unmixed", 3.6, height=5.6, y=-0.3)
    tags = VGroup(eq(r"\mathrm{B_2,\ C_2,\ N_2}", cfg.FONT["body"]).move_to([-3.6, 3.45, 0]),
                  eq(r"\mathrm{O_2,\ F_2}", cfg.FONT["body"]).move_to([3.6, 3.45, 0]))
    scene.play(FadeIn(final_left), FadeIn(final_right), FadeIn(tags), run_time=1.2)
    choose = caption("First choose the ordering. Then fill.", cfg.GREEN)
    scene.play(FadeIn(choose), run_time=0.8)
    for diagram in (final_left, final_right):
        frame = glow_frame(VGroup(diagram.level_group("p2p", links=False), diagram.level_group("s2p", links=False)),
                           cfg.GOLD, buff=0.15)
        scene.play(Create(frame), run_time=0.9)
        scene.play(FadeOut(frame), run_time=0.7)
    scene.play(VGroup(final_left, final_right, tags).animate.shift(UP * 0.08), run_time=4.8, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["13"])
