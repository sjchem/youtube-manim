"""Chapter 12 — the valence MO diagram, assembled piece by piece, and the three
filling rules.

The diagram is ``mo_models.diagram("unmixed")`` drawn by ``MODiagram``; its
orbital count (8 in, 8 out) is the model's own. The 1s core is shown filled —
bonding and antibonding pair cancel — and set aside. The filling rules are
demonstrated on the diagram; the demonstration electrons illustrate the rules
and are not a particular molecule.
"""

from manim_scenes.common import *

DIAGRAM_AT = np.array([-2.15, -0.15, 0])
PANEL_X = 5.45


class Scene12BuildDiagram(Scene):
    def construct(self) -> None:
        play_scene(self)


def rule_card(number: str, body: str, color: str) -> VGroup:
    head = txt(number, cfg.FONT["section"], color)
    text = VGroup(*[txt(line, cfg.FONT["small"], cfg.WHITE) for line in body.split("\n")]).arrange(DOWN, buff=0.1,
                                                                                                   aligned_edge=LEFT)
    card = VGroup(head, text).arrange(RIGHT, buff=0.3, aligned_edge=UP)
    fit_width(card, 4.2)
    return card


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "12", "Building the energy diagram")
    dia = mo.diagram("unmixed")
    diagram = MODiagram(dia, center=DIAGRAM_AT, height=5.9, ao_x=3.45, mo_width=0.82, ao_width=0.58, gap=0.24)

    # --- 1. Piece by piece --------------------------------------------------------------------------------------------------
    dismiss_opening_title(scene, t, head, at=3.0)

    # --- 2. Energy up; atom A, atom B, molecule in the middle ---------------------------------------------------------------
    beat(scene, t, 1)
    middle = txt("molecule", cfg.FONT["body"], cfg.CYAN).move_to([DIAGRAM_AT[0], diagram.atom_names[0].get_y(), 0])
    scene.play(GrowArrow(diagram.axis[0]), FadeIn(diagram.axis[1]), run_time=0.8)
    scene.play(FadeIn(diagram.atom_names[0], shift=DOWN * 0.15), FadeIn(diagram.atom_names[1], shift=DOWN * 0.15),
               FadeIn(middle, shift=DOWN * 0.15), run_time=1.0)

    # --- 3. The 1s core: full, cancels, set aside ------------------------------------------------------------------------------
    beat(scene, t, 2)
    core = MODiagram(mo.diagram("1s"), center=[DIAGRAM_AT[0], -0.4, 0], height=2.6, ao_x=2.2, mo_width=0.8,
                     ao_width=0.6, atoms=("", ""), axis=False)
    core_arrows = core.electrons_for(mo.Filling(mo.species("He2"), core.dia,
                                                tuple(mo.placements(core.dia, 4))), unpaired_gold=False)
    core_word = txt("1s core: full on both sides", cfg.FONT["small"], cfg.MUTED).next_to(core, DOWN, buff=0.2)
    scene.play(FadeIn(core), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.2) for a in core_arrows], lag_ratio=0.2), FadeIn(core_word),
               run_time=1.4)
    cancel = cross_mark(0.5, cfg.MUTED).move_to(core.levels["s1s"].get_center() + UP * 0.6)
    scene.play(Create(cancel), run_time=0.6)
    narration_wait(scene, 1.6)
    scene.play(VGroup(core, *core_arrows, core_word, cancel).animate.shift(DOWN * 1.2).set_opacity(0), run_time=1.4)
    scene.remove(core, *core_arrows, core_word, cancel)

    # --- 4. The two s orbitals: sigma 2s, sigma* 2s ---------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(middle), Create(diagram.ao_left["2s"]), Create(diagram.ao_right["2s"]),
               FadeIn(diagram.ao_labels["2s"]), run_time=1.0)
    scene.play(*[FadeIn(diagram.level_group(k), shift=UP * 0.1) for k in ("s2s", "s2s*")], run_time=1.6)

    # --- 5. Six p orbitals: head-on sigma pair ----------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(Create(diagram.ao_left["2p"]), Create(diagram.ao_right["2p"]), FadeIn(diagram.ao_labels["2p"]),
               run_time=1.0)
    scene.play(*[FadeIn(diagram.level_group(k), shift=UP * 0.1) for k in ("s2p", "s2p*")], run_time=1.6)

    # --- 6. Sideways: two pi and two pi star ----------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(*[FadeIn(diagram.level_group(k), shift=UP * 0.1) for k in ("p2p", "p2p*")], run_time=1.6)

    # --- 7. Count them: eight in, eight out --------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    ao_lines = VGroup(*[line for side in (diagram.ao_left, diagram.ao_right) for group in side.values() for line in group])
    mo_lines = VGroup(*[line for group in diagram.levels.values() for line in group])
    count = eq([rf"{dia.atomic_orbital_count}", r"\rightarrow", rf"{dia.orbital_count}"], cfg.FONT["hero"], cfg.WHITE)
    count.move_to([PANEL_X, 0.4, 0])
    scene.play(Indicate(ao_lines, color=cfg.GOLD, scale_factor=1.15), FadeIn(count[0]), run_time=1.2)
    scene.play(Indicate(mo_lines, color=cfg.GOLD, scale_factor=1.15), FadeIn(count[1:]), run_time=1.2)
    kept = txt("nothing created,\nnothing lost", cfg.FONT["small"], cfg.GREEN).next_to(count, DOWN, buff=0.4)
    scene.play(FadeIn(kept), count.animate.set_color(cfg.GREEN), run_time=0.8)

    # --- 8. Three rules ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    rules_head = result_label("Filling rules", cfg.GOLD, cfg.FONT["section"]).move_to([PANEL_X, 3.0, 0])
    scene.play(FadeOut(count), FadeOut(kept), FadeIn(rules_head, shift=DOWN * 0.2), run_time=1.0)

    # --- 9. One: lowest energy first ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    rules = VGroup(rule_card("1", "Fill from the\nbottom up", cfg.CYAN), rule_card("2", "Two per orbital,\nopposite spins",
                                                                                     cfg.CYAN),
                   rule_card("3", "Same energy:\nspread out first,\nspins parallel", cfg.GOLD))
    rules.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([PANEL_X, -0.2, 0])
    first = diagram.electron("s2s", 0, 1)
    ladder = glow_arrow(diagram.levels["s2s"].get_left() + LEFT * 0.4 + DOWN * 0.2,
                        diagram.levels["s2s"].get_left() + LEFT * 0.4 + UP * 1.4, cfg.CYAN, width=5)
    scene.play(FadeIn(rules[0], shift=LEFT * 0.2), run_time=0.8)
    scene.play(FadeIn(first, shift=DOWN * 0.6), GrowArrow(ladder[1]), FadeIn(ladder[0]), run_time=1.2)

    # --- 10. Two: two per orbital, opposite spins --------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    second = diagram.electron("s2s", 0, -1)
    scene.play(FadeIn(rules[1], shift=LEFT * 0.2), FadeOut(ladder), run_time=0.8)
    scene.play(FadeIn(second, shift=DOWN * 0.6), run_time=1.0)
    third_try = spin_arrow(1, cfg.RED).move_to(diagram.slot("s2s", 0, 1) + UP * 0.9)
    no = cross_mark(0.22).move_to(third_try)
    scene.play(FadeIn(third_try), run_time=0.5)
    scene.play(Create(no), run_time=0.5)
    scene.play(FadeOut(third_try), FadeOut(no), run_time=0.5)

    # --- 11. Three: spread out, spins parallel ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeIn(rules[2], shift=LEFT * 0.2), run_time=0.8)
    hund = glow_frame(rules[2], cfg.GOLD, buff=0.12)
    scene.play(Create(hund), run_time=0.8)

    # --- 12. Hund's rule ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    name = txt("Hund's rule", cfg.FONT["body"], cfg.GOLD).next_to(hund, DOWN, buff=0.25)
    scene.play(FadeIn(name, shift=UP * 0.15), run_time=0.8)

    # --- 13. Two electrons reach a degenerate pair ---------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    pair_box = diagram.highlight("p2p", cfg.GOLD)
    scene.play(Create(pair_box), run_time=0.8)
    a = spin_arrow(1, cfg.UNPAIRED).move_to(diagram.slot("p2p", 0, 1) + UP * 1.6 + RIGHT * 0.6)
    b = spin_arrow(1, cfg.UNPAIRED).move_to(diagram.slot("p2p", 1, 1) + UP * 1.6 + RIGHT * 0.6)
    scene.play(FadeIn(a), FadeIn(b), run_time=0.6)
    squeeze = spin_arrow(-1, cfg.RED).move_to(diagram.slot("p2p", 0, -1))
    scene.play(a.animate.move_to(diagram.slot("p2p", 0, 1)), b.animate.move_to(diagram.slot("p2p", 0, -1) + UP * 0.9),
               run_time=1.0)
    scene.play(FadeIn(squeeze), run_time=0.4)
    refused = cross_mark(0.22).move_to(squeeze)
    scene.play(Create(refused), run_time=0.4)
    scene.play(FadeOut(squeeze), FadeOut(refused), run_time=0.3)
    scene.play(b.animate.move_to(diagram.slot("p2p", 1, 1)), run_time=1.0)
    aligned = caption("One each, spins aligned", cfg.GOLD)
    scene.play(FadeIn(aligned), run_time=0.6)

    # --- 14. Only a third electron must pair -------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    c = spin_arrow(-1, cfg.ELECTRON).move_to(diagram.slot("p2p", 0, -1) + UP * 1.4)
    scene.play(FadeIn(c), run_time=0.4)
    scene.play(c.animate.move_to(diagram.slot("p2p", 0, -1)), a.animate.set_color(cfg.ELECTRON), run_time=1.0)

    # --- 15. One more twist: the order is not always the same -------------------------------------------------------------------------------------------------------
    beat(scene, t, 14)
    scene.play(*[FadeOut(m) for m in (first, second, a, b, c, aligned, pair_box, rules, hund, name, rules_head)],
               run_time=1.0)
    swap_box = glow_frame(VGroup(diagram.level_group("s2p", links=False), diagram.level_group("p2p", links=False)),
                          cfg.PURPLE, buff=0.18)
    twist = result_label("the order\ncan change", cfg.PURPLE, cfg.FONT["body"]).move_to([PANEL_X, 0.6, 0])
    scene.play(Create(swap_box), FadeIn(twist, shift=LEFT * 0.2), run_time=1.2)

    # --- 16. sigma 2p and the pi pair can swap ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 15)
    question = txt("Why?", cfg.FONT["title"], cfg.GOLD).next_to(twist, DOWN, buff=0.5)
    scene.play(FadeOut(swap_box), FadeIn(question), run_time=0.8)
    scene.play(diagram.mix_to(1.0), run_time=4.0, rate_func=there_and_back_with_pause)
    scene.play(diagram.mix_to(1.0), run_time=3.0, rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["12"])
