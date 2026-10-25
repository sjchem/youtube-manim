"""Chapter 18 — take one electron away from O2, and the bond gets stronger.

Removing the highest-energy electron is the last placement of
``mo_models.fill("O2")``, a pi* electron; ``fill("O2+")`` gives the new
counts, bond order and unpaired electrons. Measured lengths and bond energies
come from ``utils.mo_data``.
"""

from manim_scenes.common import *
from manim_scenes.scene_14_fill_nitrogen import valence_diagram

PANEL_X = 4.95  # More room between the right-hand content and the frame edge.
CHARGES = (1, 0, -1, -2)
SPECIES_BY_CHARGE = {1: "O2+", 0: "O2", -1: "O2-", -2: "O2 2-"}


class Scene18RemoveElectron(Scene):
    def construct(self) -> None:
        play_scene(self)


class ChargeDial(VGroup):
    """A row of charge chips with one highlighted: the molecule's charge."""

    def __init__(self, center, charge: int = 0) -> None:
        super().__init__()
        self.chips = {}
        labels = {1: "+1", 0: "0", -1: "−1", -2: "−2"}
        row = VGroup()
        for q in CHARGES:
            c = chip(labels[q], cfg.MUTED, cfg.FONT["small"])
            self.chips[q] = c
            row.add(c)
        row.arrange(RIGHT, buff=0.22).move_to(center)
        self.title = txt("charge", cfg.FONT["tiny"], cfg.MUTED).next_to(row, UP, buff=0.15)
        self.ring = VGroup()
        self.add(self.title, row, self.ring)
        self.select(charge)

    def select(self, charge: int) -> "ChargeDial":
        self.charge = charge
        target = self.chips[charge]
        self.ring.submobjects = [glow_frame(target, cfg.GOLD, buff=0.06, width=4)]
        return self

    def to(self, charge: int) -> Animation:
        ghost = self.copy().select(charge)
        return Transform(self.ring, ghost.ring)


def species_label(key: str, at) -> MathTex:
    return formula(key, cfg.FONT["title"]).move_to(at)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "18", "Take one electron away")
    o2, o2p = mo.fill("O2"), mo.fill("O2+")

    # --- 1. Oxygen; remove one electron --------------------------------------------------------------------------------------
    diagram = valence_diagram(o2.diagram.kind, "O")
    arrows = diagram.electrons_for(o2)
    dial = ChargeDial([PANEL_X, 3.2, 0], 0)
    name = species_label("O2", [PANEL_X, 2.2, 0]).scale(0.8)
    dismiss_opening_title(scene, t, head, at=1.0)
    scene.play(FadeIn(diagram), *[FadeIn(a) for a in arrows], FadeIn(dial), FadeIn(name), run_time=1.6)
    meter = BondOrderMeter(width=4.0, center=[PANEL_X, -2.6, 0], value=o2.bond_order, label=False)
    scene.play(FadeIn(meter), run_time=1.0)

    # --- 2. The highest one: a pi* electron ------------------------------------------------------------------------------------
    beat(scene, t, 1)
    highest = arrows[len(o2.electrons) - 1]
    assert o2.electrons[-1].level == "p2p*"
    spot = glow_frame(highest, cfg.GOLD, buff=0.1)
    scene.play(Create(spot), run_time=0.8)
    top = caption("The highest-energy electron: one in pi*", cfg.GOLD)
    scene.play(FadeIn(top), run_time=0.6)

    # --- 3. It leaves: O2+ -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    new_name = species_label("O2+", name.get_center()).scale(0.8)
    scene.play(highest.animate.shift(UP * 2.0 + RIGHT * 1.0).set_opacity(0), FadeOut(spot), FadeOut(top), dial.to(1),
               Transform(name, new_name), run_time=1.4)

    # --- 4. Bonding eight, antibonding three ----------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    counts = VGroup(chip(f"bonding: {o2p.bonding}", cfg.BONDING), chip(f"antibonding: {o2p.antibonding}", cfg.ANTIBONDING))
    counts.arrange(DOWN, buff=0.18).move_to([PANEL_X, 0.7, 0])
    scene.play(FadeIn(counts, shift=UP * 0.15), run_time=1.0)

    # --- 5. Two and a half ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    numbers = bond_order_numbers(o2p.bonding, o2p.antibonding, cfg.FONT["body"]).move_to([PANEL_X, -1.0, 0])
    fit_width(numbers, 4.3)
    scene.play(Write(numbers), run_time=1.4)
    scene.play(meter.to(o2p.bond_order), run_time=1.4)

    # --- 6. The bond order went up ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    up = caption("Remove an electron, and the bond gets stronger", cfg.GREEN)
    scene.play(FadeIn(up), Indicate(meter.marker, color=cfg.GREEN, scale_factor=1.6), run_time=1.2)

    # --- 7. The removed electron was antibonding ------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    ghost = spin_arrow(1, cfg.ANTIBONDING).move_to(diagram.slot("p2p*", 1, 1)).set_opacity(0.4)
    against = caption("The removed electron was working against the bond", cfg.ANTIBONDING)
    scene.play(FadeIn(ghost), fade_through(up, against), run_time=1.0)
    scene.remove(up)
    scene.play(Indicate(ghost, color=cfg.ANTIBONDING, scale_factor=1.3), run_time=1.2)

    # --- 8. Experiment agrees: shorter and stronger -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    keys = ("O2", "O2+")
    lengths = compare_bars([(mo.species(k).tex, md.BOND_LENGTH_PM[k], f"{md.BOND_LENGTH_PM[k]:.0f} pm",
                             cfg.CYAN if k == "O2+" else cfg.MUTED) for k in keys], max_value=125, length=4.0,
                           title="bond length")
    strengths = compare_bars([(mo.species(k).tex, md.DISSOCIATION_EV[k], f"{md.DISSOCIATION_EV[k]:.1f} eV",
                               cfg.GREEN if k == "O2+" else cfg.MUTED) for k in keys], max_value=7.0, length=4.0,
                             title="bond strength")
    data = VGroup(lengths, strengths).arrange(DOWN, buff=0.6).move_to([-2.4, -0.1, 0])
    agree = caption("Measured: shorter and stronger", cfg.GREEN)
    scene.play(FadeOut(diagram), *[FadeOut(a) for a in arrows if a is not highest], FadeOut(ghost), FadeOut(against),
               run_time=0.8)
    scene.play(FadeIn(data, shift=UP * 0.15), FadeIn(agree), run_time=1.4)

    # --- 9. One unpaired electron remains: still paramagnetic ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    diagram2 = valence_diagram(o2p.diagram.kind, "O")
    arrows2 = diagram2.electrons_for(o2p)
    scene.play(FadeOut(data), FadeOut(agree), run_time=0.8)
    scene.play(FadeIn(diagram2), *[FadeIn(a) for a in arrows2], run_time=1.0)
    lone = [a for a, p in zip(arrows2, o2p.electrons) if p in set(o2p.unpaired_placements())]
    still = caption(f"Still paramagnetic: {o2p.unpaired} unpaired electron instead of {o2.unpaired}", cfg.UNPAIRED)
    scene.play(*[Indicate(a, color=cfg.WHITE, scale_factor=1.4) for a in lone], FadeIn(still), run_time=1.4)

    # --- 10. Helping or hurting is what matters ----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    rule = caption("What matters: was the electron helping or hurting?", cfg.WHITE)
    scene.play(fade_through(still, rule), run_time=0.8)
    scene.remove(still)
    scene.play(Indicate(numbers[-1], color=cfg.GREEN, scale_factor=1.3), run_time=1.4)

    # --- 11. Add electrons instead? ------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    add = caption("And if we add electrons instead?", cfg.GOLD)
    scene.play(fade_through(rule, add), dial.to(-1), run_time=1.0)
    scene.remove(rule)
    scene.play(dial.to(-2), run_time=1.0)
    scene.play(dial.to(0), run_time=1.0)
    scene.play(Indicate(dial.chips[-1], color=cfg.GOLD, scale_factor=1.15), Indicate(dial.chips[-2], color=cfg.GOLD,
               scale_factor=1.15), run_time=1.4)
    end_scene(scene, t, cfg.SCENE_DURATIONS["18"])
