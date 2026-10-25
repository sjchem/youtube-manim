"""Chapter 08 — H2: the second electron pairs, and the bond order becomes one.

Placements and counts come from ``mo_models.fill("H2")``; the bond lengths and
dissociation energies on screen come from ``utils.mo_data`` (Huber and
Herzberg; H2+ exact values).
"""

from manim_scenes.common import *
from manim_scenes.scene_07_h2_plus import PANEL_X, count_chips, one_s_diagram


class Scene08Hydrogen(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "08", "Hydrogen: a full bond")
    before, after = mo.fill("H2+"), mo.fill("H2")

    # --- 1. Add a second electron: H2 ---------------------------------------------------------------------------------
    diagram = one_s_diagram(("H", "H"))
    first = diagram.electrons_for(before)[0]
    scene.play(FadeIn(diagram), FadeIn(first), run_time=1.4)
    dismiss_opening_title(scene, t, head, at=2.4)
    second = diagram.atom_electrons(1, "R")[0]
    name = formula("H2", cfg.FONT["title"]).move_to([PANEL_X, 2.5, 0])
    scene.play(FadeIn(second, shift=DOWN * 0.3), Write(name), run_time=1.2)

    # --- 2. It joins the first, spin the other way ------------------------------------------------------------------------
    beat(scene, t, 1)
    final = diagram.electrons_for(after)
    scene.play(ReplacementTransform(second, final[1], path_arc=0.6), run_time=1.6)
    scene.play(ReplacementTransform(first, final[0]), run_time=0.6)   # now paired: gold turns cyan
    pair = diagram.highlight("s1s", cfg.CYAN)
    scene.play(Create(pair), run_time=0.8)

    # --- 3. Pauli: opposite spins to share an orbital ----------------------------------------------------------------------------
    beat(scene, t, 2)
    pauli = VGroup(spin_arrow(1, cfg.ELECTRON, 0.8), spin_arrow(-1, cfg.ELECTRON, 0.8)).arrange(RIGHT, buff=0.3)
    pauli_text = VGroup(txt("Pauli:", cfg.FONT["body"], cfg.GOLD), txt("one orbital,", cfg.FONT["body"], cfg.WHITE),
                        txt("opposite spins", cfg.FONT["body"], cfg.WHITE)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    pauli_row = VGroup(pauli, pauli_text).arrange(RIGHT, buff=0.5).move_to([PANEL_X, 0.6, 0])
    fit_width(pauli_row, 5.8)
    scene.play(FadeOut(pair), FadeIn(pauli_row, shift=UP * 0.2), run_time=1.2)

    # --- 4. Bond order one -------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    nb, na = count_chips(diagram, after)
    # Match Scene 07: keep the counts outside the molecular levels.
    nb.next_to(diagram.levels["s1s"], DOWN, buff=0.42)
    na.next_to(diagram.levels["s1s*"], UP, buff=0.42)
    numbers = bond_order_numbers(after.bonding, after.antibonding, cfg.FONT["title"]).move_to([PANEL_X, -0.9, 0])
    scene.play(FadeIn(nb), FadeIn(na), FadeOut(pauli_row), run_time=0.8)
    scene.play(Write(numbers), run_time=1.6)

    # --- 5. One full bond: the Lewis line -------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    lewis = VGroup(txt("H", 110), Line(LEFT * 0.6, RIGHT * 0.6, stroke_color=cfg.WHITE, stroke_width=9),
                   txt("H", 110)).arrange(RIGHT, buff=0.25).move_to([PANEL_X, 0.85, 0])
    scene.play(Write(lewis), run_time=1.2)
    scene.play(Indicate(lewis[1], color=cfg.GREEN, scale_factor=1.3), Indicate(numbers[-1], color=cfg.GREEN), run_time=1.2)

    # --- 6. The data agree: shorter and stronger -----------------------------------------------------------------------------------------
    beat(scene, t, 5)
    lengths = compare_bars([(mo.species("H2+").tex, md.BOND_LENGTH_PM["H2+"], f"{md.BOND_LENGTH_PM['H2+']:.0f} pm", cfg.MUTED),
                            (mo.species("H2").tex, md.BOND_LENGTH_PM["H2"], f"{md.BOND_LENGTH_PM['H2']:.0f} pm", cfg.CYAN)],
                           max_value=110, length=2.4, title="bond length")
    energies = compare_bars([(mo.species("H2+").tex, md.DISSOCIATION_EV["H2+"], f"{md.DISSOCIATION_EV['H2+']:.2f} eV", cfg.MUTED),
                             (mo.species("H2").tex, md.DISSOCIATION_EV["H2"], f"{md.DISSOCIATION_EV['H2']:.2f} eV", cfg.GREEN)],
                            max_value=4.6, length=2.4, title="bond strength")
    lengths.move_to([PANEL_X, 1.25, 0])
    energies.move_to([PANEL_X, -1.35, 0])
    scene.play(FadeOut(lewis), FadeOut(numbers), name.animate.move_to([PANEL_X, 3.1, 0]).scale(0.75), run_time=0.8)
    scene.play(FadeIn(lengths, shift=UP * 0.15), run_time=1.0)
    scene.play(FadeIn(energies, shift=UP * 0.15), run_time=1.0)

    # --- 7. Twice the electrons, not quite twice the strength ----------------------------------------------------------------------------------
    beat(scene, t, 6)
    ratio = md.DISSOCIATION_EV["H2"] / md.DISSOCIATION_EV["H2+"]
    note = caption(f"Twice the bonding electrons: about {ratio:.1f}× the strength, not 2×", cfg.GOLD)
    scene.play(FadeIn(note), Indicate(energies.bars[1][1], color=cfg.GOLD, scale_factor=1.05), run_time=1.2)
    guide = caption("Bond order is a guide, not a formula for energy", cfg.WHITE)
    narration_wait(scene, 2.6)
    scene.play(fade_through(note, guide), run_time=0.8)
    scene.remove(note)

    # --- 8. Paired spins: diamagnetic ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    dia = VGroup(result_label("all paired:", cfg.DIAMAGNETIC, cfg.FONT["section"]),
                 result_label("diamagnetic", cfg.DIAMAGNETIC, cfg.FONT["section"])).arrange(DOWN, buff=0.2)
    dia.move_to([PANEL_X, 0.3, 0])
    scene.play(FadeOut(lengths), FadeOut(energies), FadeOut(guide), FadeOut(nb), FadeOut(na), run_time=0.8)
    scene.play(FadeIn(dia, scale=1.1), Indicate(VGroup(*final), color=cfg.WHITE, scale_factor=1.25), run_time=1.4)
    weak = fit_width(txt("pushed out of a field, very weakly", cfg.FONT["small"], cfg.MUTED), 5.6).next_to(dia, DOWN, buff=0.35)
    scene.play(FadeIn(weak), run_time=0.8)

    # --- 9. Always stronger with more electrons? --------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    question = VGroup(txt("more electrons", cfg.FONT["section"], cfg.WHITE), eq(r"\Rightarrow", cfg.FONT["section"]),
                      txt("stronger bond?", cfg.FONT["section"], cfg.GOLD)).arrange(RIGHT, buff=0.3)
    fit_width(question, 13.0)
    question.move_to([0, -3.1, 0])
    scene.play(FadeIn(question, shift=UP * 0.2), FadeOut(weak), run_time=1.0)
    scene.play(Indicate(question[2], color=cfg.WHITE, scale_factor=1.08), run_time=1.4)
    scene.play(question.animate.scale(1.06), run_time=4.0, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["08"])
