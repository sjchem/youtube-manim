"""Scene 10 — normality counts reaction equivalents: a computed 3D sulfuric
acid molecule with its two acidic hydrogens glowing teal, N = M x z, and
the catch — z belongs to the reaction, not to the molecule. Normality is
historical and its use is discouraged by IUPAC; the film says so.
"""

from manim_scenes.common import *
from manim_scenes.stage3d import Halo

RX = 3.7


class Scene10Normality(Scene):
    def construct(self) -> None:
        play_scene(self)


def acid_stage(at, zoom: float = 1.7, spin: float = 0.35) -> tuple[Stage, dict, list]:
    stage = Stage(at, zoom=zoom, yaw=0.5, pitch=0.35, spin=spin, sway=0.1)
    model = molecule_model(stage, pm.sulfuric_acid(), scale=0.8, labels=True, radius_scale=1.35)
    halos = [Halo(model["balls"][i], cfg.EQUIVALENT, reach=2.6, peak=0.3) for i in pm.sulfuric_acid().acidic]
    for h in halos:
        h.presence = 0.0
    stage.add_body(*halos)
    return stage, model, halos


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "10", "Normality: counting reaction equivalents")
    question = txt("a different kind of question", cfg.FONT["body"], cfg.CYAN).move_to([0, 0.5, 0])
    scene.play(FadeIn(question, shift=UP * 0.2), run_time=0.9)

    # --- 2. Sulfuric acid, 0.500 M -----------------------------------------------------------------------------
    beat(scene, t, 1)
    bottle = eq_chip(rf"\mathrm{{H_2SO_4}}\quad {fx(pm.ACID_MOLARITY, 3)}\ \mathrm{{M}}", cfg.WHITE, stroke=cfg.SOLUTE)
    bottle.move_to([RX, 2.55, 0])
    scene.play(FadeOut(head), FadeOut(question), FadeIn(bottle, shift=DOWN * 0.2), run_time=1.0)

    # --- 3. One molecule ---------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    stage, model, halos = acid_stage([-3.7, -0.2, 0], zoom=1.45)
    structure_note = txt("structural model; aqueous acid is ionised", cfg.FONT["tiny"], cfg.MUTED)
    fit_width(structure_note, 6.8)
    structure_note.move_to([-3.7, -3.25, 0])
    show(scene, stage, 1.6, FadeIn(structure_note))
    parts = VGroup(txt("1 sulfur", cfg.FONT["small"], cfg.ELEMENT_COLORS["S"]),
                   txt("4 oxygens", cfg.FONT["small"], cfg.ELEMENT_COLORS["O"]),
                   txt("2 hydrogens", cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    parts.move_to([RX, 0.6, 0])
    scene.play(LaggedStart(*[FadeIn(p, shift=LEFT * 0.2) for p in parts], lag_ratio=0.4), run_time=1.6)

    # --- 4. The acidic hydrogens: equivalents -------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(*[stage.fade(h, 1.0) for h in halos], parts[2].animate.set_color(cfg.EQUIVALENT), run_time=1.2)
    proton = eq(r"1\ \mathrm{mol\,H^+}", cfg.FONT["body"], cfg.EQUIVALENT).move_to([RX - 1.2, -1.4, 0])
    one_eq = txt("= 1 eq", cfg.FONT["label"], cfg.EQUIVALENT).next_to(proton, RIGHT, buff=0.3)
    scene.play(FadeIn(proton, scale=0.6), run_time=0.7)
    scene.play(FadeIn(one_eq, shift=LEFT * 0.2), run_time=0.8)

    # --- 5. Normality: equivalents per litre ----------------------------------------------------------------------------
    beat(scene, t, 4)
    rule = fraction("N", r"\text{equivalents}", r"V_{\text{solution}}", cfg.EQUIVALENT, cfg.VOLUME, cfg.FONT["section"])
    rule.move_to([RX, 0.4, 0])
    scene.play(FadeOut(VGroup(parts, proton, one_eq)), run_time=0.6)
    scene.play(Write(rule), run_time=1.6)

    # --- 6. N = M x z -------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    link = eq([r"N", "=", r"M", r"\times", r"z"], cfg.FONT["title"]).move_to([RX, -1.7, 0])
    link[2].set_color(cfg.VOLUME)
    link[4].set_color(cfg.EQUIVALENT)
    scene.play(Write(link), run_time=1.4)
    per_mole = txt("equivalents per mole", cfg.FONT["small"], cfg.EQUIVALENT).next_to(link, DOWN, buff=0.25)
    scene.play(FadeIn(per_mole), run_time=0.7)

    # --- 7. How many protons? -------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(rule), FadeOut(per_mole), run_time=0.4)
    scene.play(link.animate.move_to([RX, 1.2, 0]), run_time=0.6)
    f_q = eq(r"z = \,?", 110, cfg.GOLD).move_to([RX, -1.0, 0])
    scene.play(FadeIn(f_q, scale=0.8), run_time=0.9)

    # --- 8. Tempting: two -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    two = eq(r"z = 2\ ?", 110, cfg.MUTED).move_to(f_q)
    scene.play(fade_through(f_q, two), run_time=0.9)
    scene.remove(f_q)
    scene.play(stage.rock(RIGHT, 0.6), run_time=1.6)

    # --- 9. The reaction decides --------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    decides = result_label("the reaction decides", cfg.GOLD, cfg.FONT["section"]).move_to([RX, -1.0, 0])
    fit_width(decides, 7.4)
    scene.play(fade_through(two, decides), run_time=1.0)
    scene.remove(two)

    # --- 10. Name the reaction first ------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    first = chip("first, name the reaction", cfg.WHITE).move_to([RX, -2.6, 0])
    scene.play(FadeIn(first, shift=UP * 0.15), run_time=0.8)

    # --- 11. Historical ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(VGroup(link, decides, first)), run_time=0.7)
    history = VGroup(txt("historical unit", cfg.FONT["body"], cfg.MUTED),
                     txt("older lab methods · textbooks", cfg.FONT["small"], cfg.MUTED)).arrange(DOWN, buff=0.18)
    history.move_to([RX, 1.2, 0])
    scene.play(FadeIn(history, shift=UP * 0.15), run_time=1.0)

    # --- 12. Today: avoid it -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    advice = VGroup(txt("IUPAC: avoid normality", cfg.FONT["label"], cfg.WARNING),
                    txt("use molarity + a balanced equation", cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.18)
    advice.move_to([RX, -0.6, 0])
    fit_width(advice, 7.4)
    scene.play(FadeIn(advice, shift=UP * 0.15), run_time=1.0)

    # --- 13. The idea is good ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    idea = result_label("the idea: count chemical capacity", cfg.RESULT, cfg.FONT["label"]).move_to([RX, -2.3, 0])
    fit_width(idea, 7.4)
    scene.play(FadeIn(idea, shift=UP * 0.15), *[stage.fade(h, 0.4) for h in halos], run_time=1.0)
    scene.play(*[stage.fade(h, 1.0) for h in halos], run_time=0.8)

    # --- 14. Run it both ways --------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    scene.play(FadeOut(VGroup(history, advice, idea, structure_note)), stage.glide([0.0, 0.3, 0.0]), run_time=1.2)
    arrow_a = glow_arrow([-1.2, -1.4, 0], [-4.6, -2.6, 0], cfg.EQUIVALENT)
    arrow_b = glow_arrow([1.2, -1.4, 0], [4.6, -2.6, 0], cfg.EQUIVALENT)
    lab_a = txt("one proton", cfg.FONT["label"], cfg.EQUIVALENT).move_to([-5.2, -3.3, 0])
    lab_b = txt("two protons", cfg.FONT["label"], cfg.EQUIVALENT).move_to([5.2, -3.3, 0])
    scene.play(GrowFromEdge(arrow_a, UR), GrowFromEdge(arrow_b, UL), run_time=1.0)
    scene.play(FadeIn(lab_a), FadeIn(lab_b), run_time=0.8)
    scene.play(stage.zoom_to(1.65), bottle.animate.move_to([RX + 0.6, 2.55, 0]), run_time=14.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["10"])
