"""Chapter 19 — add electrons to O2: superoxide and peroxide.

Each added electron is the next placement in ``mo_models`` (both land in
pi*). The four 3D O-O models are drawn with bond lengths proportional to
the measured values in ``utils.mo_data``; the two ion values depend on the
salt and are shown as approximate. Unpaired counts and verdicts are computed.
"""

from manim_scenes.common import *
from manim_scenes.scene_14_fill_nitrogen import valence_diagram
from manim_scenes.scene_18_remove_electron import ChargeDial, species_label

PANEL_X = 4.95  # Match Scene 18’s roomier ion-panel alignment.
SERIES = ("O2+", "O2", "O2-", "O2 2-")


class Scene19AddElectrons(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "19", "Add electrons instead")
    o2, sup, per = mo.fill("O2"), mo.fill("O2-"), mo.fill("O2 2-")

    # --- 1. Add one electron to oxygen ------------------------------------------------------------------------------------
    diagram = valence_diagram(o2.diagram.kind, "O")
    arrows = diagram.electrons_for(o2)
    dial = ChargeDial([PANEL_X, 3.2, 0], 0)
    name = species_label("O2", [PANEL_X, 2.2, 0]).scale(0.8)
    dismiss_opening_title(scene, t, head, at=1.0)
    scene.play(FadeIn(diagram), *[FadeIn(a) for a in arrows], FadeIn(dial), FadeIn(name), run_time=1.6)
    meter = BondOrderMeter(width=4.0, center=[PANEL_X, -2.6, 0], value=o2.bond_order, label=False)
    # The animated readout replaces its text; render its current draw tree.
    meter._live_draw_order = True
    scene.play(FadeIn(meter), run_time=0.8)

    # --- 2. The lowest open spot: pairing in pi* ------------------------------------------------------------------------------
    beat(scene, t, 1)
    extra = sup.electrons[-1]
    assert extra.level == "p2p*"
    incoming = spin_arrow(extra.spin, cfg.ANTIBONDING).move_to(diagram.slot(extra.level, extra.orbital, extra.spin) + UP * 1.6)
    scene.play(FadeIn(incoming, shift=DOWN * 0.3), dial.to(-1), run_time=1.0)
    landing = diagram.electron(extra.level, extra.orbital, extra.spin)
    partner = arrows[[i for i, p in enumerate(o2.electrons) if p.level == extra.level and p.orbital == extra.orbital][0]]
    scene.play(ReplacementTransform(incoming, landing), partner.animate.set_color(cfg.ANTIBONDING), run_time=1.4)

    # --- 3. Superoxide: bond order one and a half ------------------------------------------------------------------------------------
    beat(scene, t, 2)
    sup_name = species_label("O2-", name.get_center()).scale(0.8)
    tag = caption(f"Superoxide: bond order {md.display_number(sup.bond_order)}", cfg.CYAN)
    counts = VGroup(chip(f"bonding: {sup.bonding}", cfg.BONDING), chip(f"antibonding: {sup.antibonding}", cfg.ANTIBONDING))
    counts.arrange(DOWN, buff=0.18).move_to([PANEL_X, 0.7, 0])
    numbers = bond_order_numbers(sup.bonding, sup.antibonding, cfg.FONT["body"]).move_to([PANEL_X, -1.0, 0])
    scene.play(Transform(name, sup_name), FadeIn(tag), FadeIn(counts), run_time=1.0)
    scene.play(Write(numbers), meter.to(sup.bond_order), run_time=1.6)

    # --- 4. One more: peroxide, bond order one -----------------------------------------------------------------------------------------
    beat(scene, t, 3)
    last = per.electrons[-1]
    incoming2 = spin_arrow(last.spin, cfg.ANTIBONDING).move_to(diagram.slot(last.level, last.orbital, last.spin) + UP * 1.6)
    scene.play(FadeIn(incoming2, shift=DOWN * 0.3), dial.to(-2), run_time=0.8)
    landing2 = diagram.electron(last.level, last.orbital, last.spin)
    partner2 = arrows[[i for i, p in enumerate(o2.electrons) if p.level == last.level and p.orbital == last.orbital][0]]
    per_name = species_label("O2 2-", name.get_center()).scale(0.8)
    tag2 = caption(f"Peroxide: bond order {md.display_number(per.bond_order)}", cfg.CYAN)
    counts2 = VGroup(chip(f"bonding: {per.bonding}", cfg.BONDING), chip(f"antibonding: {per.antibonding}", cfg.ANTIBONDING))
    counts2.arrange(DOWN, buff=0.18).move_to(counts)
    numbers2 = bond_order_numbers(per.bonding, per.antibonding, cfg.FONT["body"]).move_to(numbers)
    full = diagram.highlight("p2p*", cfg.ANTIBONDING)
    scene.play(ReplacementTransform(incoming2, landing2), partner2.animate.set_color(cfg.ANTIBONDING), Create(full),
               run_time=1.2)
    scene.play(Transform(name, per_name), Transform(tag, tag2), Transform(counts, counts2), Transform(numbers, numbers2),
               meter.to(per.bond_order), run_time=1.4)

    # --- 5. Each added electron is antibonding ---------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    weakens = caption("Every electron we add lands in an antibonding orbital", cfg.ANTIBONDING)
    scene.play(fade_through(tag, weakens), Indicate(VGroup(landing, landing2), color=cfg.WHITE, scale_factor=1.35), run_time=1.4)

    # --- 6. The bond stretches: four molecules, measured lengths ---------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.remove(tag)
    scene.play(*[FadeOut(m) for m in (diagram, *arrows, landing, landing2, full, dial, name, counts, numbers, meter,
                                       weakens)], run_time=1.0)
    xs = (-5.4, -1.8, 1.8, 5.4)
    stages, rods = [], []
    for key, x in zip(SERIES, xs):
        st = Stage([x, 1.3, 0], zoom=1.0, yaw=0.0, pitch=0.25, sway=0.15)
        _, _, rod = diatomic_model(st, "O", 1, length=1.6)
        st.presence = 0.0
        stages.append(st)
        rods.append(rod)
    labels = VGroup(*[formula(k, cfg.FONT["section"]).move_to([x, 2.85, 0]) for k, x in zip(SERIES, xs)])
    pm_labels = VGroup(*[txt(("≈" if k in md.ION_BOND_LENGTH_PM else "") + f"{md.bond_length(k):.0f} pm",
                             cfg.FONT["body"], cfg.CYAN).move_to([x, -0.15, 0]) for k, x in zip(SERIES, xs)])
    orders = VGroup(*[txt(f"order {md.display_number(mo.bond_order(k))}", cfg.FONT["body"], cfg.GREEN)
                      .move_to([x, -0.85, 0]) for k, x in zip(SERIES, xs)])
    for st in stages:
        scene.add(st)
    scene.play(*[st.fade(st, 1.0) for st in stages], FadeIn(labels), FadeIn(orders), run_time=1.2)
    scene.play(*[stretch_bond(st, rod, md.bond_length(k) / 62.0) for st, rod, k in zip(stages, rods, SERIES)],
               FadeIn(pm_labels), run_time=2.4, rate_func=smooth)
    longer = caption("Lower bond order, longer bond (ion lengths depend on the salt)", cfg.CYAN)
    scene.play(FadeIn(longer), run_time=0.8)

    # --- 7. Magnetism: one, two, one, none ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    spins = VGroup()
    for k, x in zip(SERIES, xs):
        n = mo.unpaired(k)
        if n:
            group = VGroup(*[spin_arrow(1, cfg.UNPAIRED, 0.6) for _ in range(n)]).arrange(RIGHT, buff=0.25)
        else:
            group = txt("none", cfg.FONT["small"], cfg.DIAMAGNETIC)
        spins.add(group.move_to([x, -1.7, 0]))
    verdicts = VGroup(*[txt(mo.fill(k).magnetism, cfg.FONT["small"],
                            cfg.PARAMAGNETIC if mo.fill(k).unpaired else cfg.DIAMAGNETIC).move_to([x, -2.45, 0])
                        for k, x in zip(SERIES, xs)])
    scene.play(FadeOut(longer), LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in spins], lag_ratio=0.3), run_time=1.6)
    scene.play(FadeIn(verdicts), run_time=0.8)
    peroxide = glow_frame(VGroup(spins[3], verdicts[3]), cfg.DIAMAGNETIC, buff=0.12)
    scene.play(Create(peroxide), run_time=0.8)

    # --- 8. Four species, one diagram -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    one = caption("Four species, one diagram: every bond order, every verdict", cfg.GREEN)
    scene.play(FadeOut(peroxide), FadeIn(one), run_time=0.8)
    scene.play(*[st.rock(RIGHT, PI) for st in stages], run_time=3.0, rate_func=smooth)

    # --- 9. Where the electron goes ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    rule = caption("Add one: the bond can weaken. Remove one: it can strengthen.", cfg.WHITE)
    scene.play(fade_through(one, rule), run_time=0.8)
    scene.remove(one)
    scene.play(*[stretch_bond(st, rod, md.bond_length(k) / 62.0 * 1.06) for st, rod, k in zip(stages, rods, SERIES)],
               run_time=2.0, rate_func=there_and_back)
    where = caption("It all depends on where the electron goes", cfg.GOLD)
    scene.play(fade_through(rule, where), run_time=0.8)
    scene.remove(rule)
    scene.play(*[st.turn(yaw=0.8)[0] for st in stages], run_time=3.0, rate_func=smooth)
    scene.play(*[st.turn(yaw=0.0)[0] for st in stages], run_time=3.5, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["19"])
