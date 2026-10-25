"""Chapter 09 — helium: extra electrons that cancel the bond.

He2's four electrons fill sigma 1s and then sigma* 1s (``mo_models``); the
balance shows bonding against antibonding electrons, tipping slightly toward
antibonding because the antibonding level rises more than the bonding one
falls. The line-up's bond orders are computed; the footnote's distances come
from ``utils.mo_data`` (Grisenti et al. 2000 for the real, dispersion-bound
helium dimer), drawn to scale against H2.
"""

from manim_scenes.common import *
from manim_scenes.scene_07_h2_plus import PANEL_X, count_chips, one_s_diagram


class Scene09Helium(Scene):
    def construct(self) -> None:
        play_scene(self)


class Balance(VGroup):
    """A beam balance whose tilt can be tweened; pans hold any mobjects."""

    def __init__(self, pivot, half: float = 2.3, left: Mobject | None = None, right: Mobject | None = None) -> None:
        super().__init__()
        self.pivot, self.half, self.tilt = np.asarray(pivot, dtype=float), half, 0.0
        self.post = VGroup(Line(self.pivot, self.pivot + DOWN * 2.0, stroke_color=cfg.MUTED, stroke_width=8),
                           Line(self.pivot + DOWN * 2.0 + LEFT * 0.9, self.pivot + DOWN * 2.0 + RIGHT * 0.9,
                                stroke_color=cfg.MUTED, stroke_width=8),
                           Triangle(stroke_width=0, fill_color=cfg.MUTED, fill_opacity=1).scale(0.22)
                           .move_to(self.pivot + DOWN * 0.12))
        self.beam = Line(LEFT * half, RIGHT * half, stroke_color=cfg.WHITE, stroke_width=8)
        self.pans = VGroup()
        self.loads = [left or VGroup(), right or VGroup()]
        for _ in range(2):
            strings = VGroup(Line(ORIGIN, DOWN * 0.9 + LEFT * 0.55, stroke_color=cfg.MUTED, stroke_width=3),
                             Line(ORIGIN, DOWN * 0.9 + RIGHT * 0.55, stroke_color=cfg.MUTED, stroke_width=3))
            dish = Arc(radius=0.75, start_angle=PI + 0.6, angle=PI - 1.2, stroke_color=cfg.MUTED, stroke_width=5)
            dish.move_to(DOWN * 1.0)
            self.pans.add(VGroup(strings, dish))
        self.add(self.post, self.beam, self.pans, *self.loads)
        self.set_tilt(0.0)

    def set_tilt(self, angle: float) -> None:
        self.tilt = float(angle)
        d = np.array([np.cos(angle), np.sin(angle), 0.0])
        self.beam.put_start_and_end_on(self.pivot - d * self.half, self.pivot + d * self.half)
        for pan, load, side in zip(self.pans, self.loads, (-1, 1)):
            hook = self.pivot + side * d * self.half
            pan.move_to(hook + DOWN * 0.55)
            load.move_to(hook + DOWN * 0.72)

    def tip(self, angle: float, **kwargs) -> Param:
        return Param(self, lambda: self.tilt, self.set_tilt, angle, **kwargs)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "09", "Helium: electrons that cancel")
    he2 = mo.fill("He2")

    # --- 1. Two helium atoms, four electrons ----------------------------------------------------------------------------
    diagram = one_s_diagram(("He", "He"))
    left = diagram.atom_electrons(2, "L")
    right = diagram.atom_electrons(2, "R")
    name = formula("He2", cfg.FONT["title"]).move_to([PANEL_X, 2.5, 0])
    four = txt(f"{len(he2.electrons)} electrons", cfg.FONT["section"], cfg.WHITE).move_to([PANEL_X, 1.3, 0])
    scene.play(FadeIn(diagram), run_time=1.2)
    dismiss_opening_title(scene, t, head, at=2.0)
    scene.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.25) for a in left + right], lag_ratio=0.2), Write(name),
               run_time=1.6)
    scene.play(FadeIn(four, shift=UP * 0.15), run_time=0.8)

    # --- 2. The first two fill sigma 1s ------------------------------------------------------------------------------------
    beat(scene, t, 1)
    sources = [left[0], right[1], right[0], left[1]]
    anims, arrows = fly_electrons(diagram, sources, he2)
    scene.play(*anims[:2], run_time=1.6)

    # --- 3. Full: one place left ------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    full = diagram.highlight("s1s", cfg.CYAN)
    full_word = txt("full", cfg.FONT["body"], cfg.CYAN).next_to(full, DOWN, buff=0.15)
    scene.play(Create(full), FadeIn(full_word), run_time=1.0)
    scene.play(Indicate(VGroup(sources[2], sources[3]), color=cfg.GOLD, scale_factor=1.3), run_time=1.6)

    # --- 4. Up into the antibonding orbital ------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(*anims[2:], FadeOut(full), FadeOut(full_word), run_time=1.8)

    # --- 5. Count: two minus two over two ------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    nb, na = count_chips(diagram, he2)
    numbers = bond_order_numbers(he2.bonding, he2.antibonding, cfg.FONT["title"], show_result=False)
    numbers.move_to([PANEL_X - 0.5, -0.2, 0])
    scene.play(FadeOut(four), FadeIn(nb), FadeIn(na), run_time=0.9)
    scene.play(Write(numbers), run_time=1.6)

    # --- 6. Bond order zero -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    result = eq(["=", md.display_number(he2.bond_order)], cfg.FONT["title"]).next_to(numbers, RIGHT, buff=0.3)
    result[1].set_color(cfg.RED)
    scene.play(Write(result), run_time=0.8)
    scene.play(Indicate(result[1], color=cfg.WHITE, scale_factor=1.5), run_time=1.2)

    # --- 7. The antibonding pair cancels the bonding pair -----------------------------------------------------------------------------------
    beat(scene, t, 6)
    bond_load = VGroup(spin_arrow(1, cfg.BONDING), spin_arrow(-1, cfg.BONDING)).arrange(RIGHT, buff=0.18)
    anti_load = VGroup(spin_arrow(1, cfg.ANTIBONDING), spin_arrow(-1, cfg.ANTIBONDING)).arrange(RIGHT, buff=0.18)
    balance = Balance([PANEL_X, 0.9, 0], half=1.85, left=bond_load, right=anti_load)
    tags = VGroup(txt("bonding", cfg.FONT["small"], cfg.BONDING), txt("antibonding", cfg.FONT["small"], cfg.ANTIBONDING))
    tags[0].move_to([PANEL_X - 1.85, -1.45, 0])
    tags[1].move_to([PANEL_X + 1.85, -1.45, 0])
    scene.play(FadeOut(numbers), FadeOut(result), name.animate.scale(0.7).move_to([PANEL_X, 3.2, 0]), run_time=0.8)
    scene.play(FadeIn(balance), FadeIn(tags), run_time=1.4)
    cancels = caption("The antibonding pair cancels the bonding pair", cfg.WHITE)
    scene.play(FadeIn(cancels), run_time=0.8)

    # --- 8. Slightly more than cancel ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    more = caption("Filled shells: no net covalent bond in this model", cfg.ANTIBONDING)
    scene.play(fade_through(cancels, more), run_time=0.8)
    scene.remove(cancels)
    scene.play(balance.tip(-0.12), run_time=2.4, rate_func=smooth)
    apart = result_label("better off apart", cfg.ANTIBONDING, cfg.FONT["body"]).move_to([PANEL_X, -2.4, 0])
    scene.play(FadeIn(apart, shift=UP * 0.15), run_time=0.8)

    # --- 9. A gas of single atoms ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    atoms = VGroup()
    icon_stage = Stage()
    for _ in range(2):
        atom = Ball(ORIGIN, 0.42, cfg.ELEMENT_COLORS["He"], "He")
        atom.place(icon_stage, np.eye(3), 1.0)
        atoms.add(atom.mob)
    atoms[0].move_to([PANEL_X - 0.5, 0.4, 0])
    atoms[1].move_to([PANEL_X + 0.5, 0.4, 0])
    gas = caption("Helium: a gas of single atoms", cfg.WHITE)
    scene.play(FadeOut(balance), FadeOut(tags), FadeOut(apart), fade_through(more, gas), FadeIn(atoms), run_time=1.0)
    scene.remove(more)
    scene.play(atoms[0].animate.shift(LEFT * 1.6 + UP * 0.3), atoms[1].animate.shift(RIGHT * 1.6 + DOWN * 0.3),
               run_time=2.6, rate_func=smooth)

    # --- 10. More electrons, not more bonding -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    rule = VGroup(txt("more electrons", cfg.FONT["body"], cfg.WHITE), eq(r"\not\Downarrow", cfg.FONT["body"], cfg.RED),
                  txt("more bonding", cfg.FONT["body"], cfg.WHITE)).arrange(DOWN, buff=0.15)
    rule.move_to([PANEL_X, -1.4, 0])
    which = caption("It depends on which orbitals they fill", cfg.GREEN)
    scene.play(FadeIn(rule, shift=UP * 0.15), fade_through(gas, which), run_time=1.2)
    scene.remove(gas)

    # --- 11. A test: remove one electron ----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    question = txt("?", 90, cfg.GOLD).next_to(arrows[3], UP, buff=0.12)
    test = caption("Remove one electron. Which one goes?", cfg.GOLD)
    scene.play(FadeOut(atoms), FadeOut(rule), fade_through(which, test), run_time=1.0)
    scene.remove(which)
    scene.play(FadeIn(question, scale=0.6), run_time=0.8)

    # --- 12. The highest one: He2+ --------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    he2p = mo.fill("He2+")
    gone = he2.electrons[-1]
    assert gone not in he2p.electrons[len(he2p.electrons):]
    scene.play(arrows[3].animate.shift(UP * 2.4).set_opacity(0), FadeOut(question), run_time=1.2)
    survivor = diagram.electrons_for(he2p)[2]
    scene.play(ReplacementTransform(arrows[2], survivor), run_time=0.7)
    nb2, na2 = count_chips(diagram, he2p)
    new_name = formula("He2+", cfg.FONT["title"]).move_to(name.get_center()).scale(0.7)
    plus_numbers = bond_order_numbers(he2p.bonding, he2p.antibonding, cfg.FONT["title"]).move_to([PANEL_X, 0.4, 0])
    scene.play(Transform(nb, nb2), Transform(na, na2), Transform(name, new_name), FadeOut(test), run_time=1.0)
    scene.play(Write(plus_numbers), run_time=1.4)
    exists = result_label("can exist — and does", cfg.GREEN, cfg.FONT["body"]).move_to([PANEL_X, -1.4, 0])
    scene.play(FadeIn(exists, shift=UP * 0.15), run_time=0.8)

    # --- 13. Line them up -------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    keys = ("H2+", "H2", "He2+", "He2")
    rows = [(mo.species(k).tex, mo.bond_order(k), md.display_number(mo.bond_order(k)),
             cfg.RED if mo.bond_order(k) == 0 else cfg.RESULT) for k in keys]
    lineup = compare_bars(rows, max_value=1.0, length=6.0, title="bond order", label_width=1.8)
    lineup.scale(1.35).move_to([0, 0.1, 0])
    scene.play(*[FadeOut(m) for m in (diagram, survivor, arrows[0], arrows[1], nb, na, name, plus_numbers, exists)],
               run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.3) for row in lineup.bars], lag_ratio=0.45), FadeIn(lineup[1]),
               run_time=3.0)
    scene.play(Indicate(lineup.bars[3], color=cfg.RED, scale_factor=1.08), run_time=1.6)

    # --- 14. A footnote: a real, very weakly bound helium pair ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    scene.play(FadeOut(lineup), run_time=0.7)
    span = 11.0
    h2_len = span * md.BOND_LENGTH_PM["H2"] / md.HE2_SEPARATION_PM
    he_pair = VGroup(nucleus_dot([-span / 2, 0.6, 0], cfg.ELEMENT_COLORS["He"], radius=0.12),
                     nucleus_dot([span / 2, 0.6, 0], cfg.ELEMENT_COLORS["He"], radius=0.12))
    he_line = DashedLine([-span / 2, 0.6, 0], [span / 2, 0.6, 0], stroke_color=cfg.PURPLE, stroke_width=3)
    h_pair = VGroup(nucleus_dot([-h2_len / 2, -1.0, 0], cfg.WHITE, radius=0.05),
                    nucleus_dot([h2_len / 2, -1.0, 0], cfg.WHITE, radius=0.05))
    labels = VGroup(eq(r"\text{real }\mathrm{He_2}", cfg.FONT["body"], cfg.PURPLE).move_to([0, 1.35, 0]),
                    eq(r"\mathrm{H_2}", cfg.FONT["body"], cfg.WHITE).move_to([0, -1.75, 0]))
    scale_note = txt("drawn to scale", cfg.FONT["small"], cfg.MUTED).move_to([4.6, -1.0, 0])
    scene.play(FadeIn(he_pair), Create(he_line), FadeIn(labels[0]), run_time=1.4)
    scene.play(FadeIn(h_pair), FadeIn(labels[1]), FadeIn(scale_note), run_time=1.0)
    farther = caption("More than fifty times farther apart than in H₂", cfg.PURPLE)
    scene.play(FadeIn(farther), run_time=0.8)

    # --- 15. Dispersion, not a covalent bond ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 14)
    honest = caption("Bond order zero: no covalent bond — not no attraction", cfg.WHITE)
    weak = chip("held by dispersion: a far weaker pull", cfg.PURPLE).move_to([0, -2.75, 0])
    scene.play(fade_through(farther, honest), FadeIn(weak, shift=UP * 0.15), run_time=1.0)
    scene.remove(farther)
    scene.play(Indicate(weak, color=cfg.WHITE, scale_factor=1.05), run_time=1.6)
    for _ in range(3):
        scene.play(he_pair[0].animate.shift(RIGHT * 0.25), he_pair[1].animate.shift(LEFT * 0.25), run_time=3.0,
                   rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["09"])
