"""Electronegativity: a tug of war for the shared pair inside a bond.

H-Cl is drawn first with an even (symmetric) shared cloud — labelled as a
convenient sketch — which then slides toward chlorine. Three cards keep
ionization, electron gain and electronegativity apart. The Pauling values
(H 2.20, Cl 3.16) come from ``utils.element_data``.
"""

from manim_scenes.common import *

H_AT = np.array([-2.5, 0.45, 0])
CL_AT = np.array([2.3, 0.45, 0])
SCALE_Y = -0.2
SCALE_LEFT, SCALE_RIGHT = -5.6, 5.6


class Scene14Electronegativity(Scene):
    def construct(self) -> None:
        play_scene(self)


def scale_x(value: float) -> float:
    return SCALE_LEFT + (SCALE_RIGHT - SCALE_LEFT) * value / 4.0


def card(title: list[str], colour: str, lines: list[str], x: float) -> VGroup:
    frame = RoundedRectangle(width=4.5, height=5.2, corner_radius=0.25, stroke_color=colour, stroke_width=3,
                             fill_color=cfg.PANEL, fill_opacity=0.85).move_to([x, -0.55, 0])
    heading_text = VGroup(*[txt(line, cfg.FONT["small"], colour) for line in title]).arrange(DOWN, buff=0.08)
    fit_width(heading_text, 4.1)
    heading_text.move_to(frame.get_top() + DOWN * 0.62)
    body = VGroup(*[txt(line, cfg.FONT["tiny"], cfg.WHITE) for line in lines]).arrange(DOWN, buff=0.14)
    fit_width(body, 4.1)
    body.move_to(frame.get_bottom() + UP * 0.8)
    group = VGroup(frame, heading_text, body)
    group.frame, group.title, group.body = frame, heading_text, body
    return group


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "14", "A tug of war inside a bond")

    # --- 1. Hydrogen chloride ---------------------------------------------------------------------
    hydrogen = Atom(0.75, H_AT, charge="+1", count=120, seed=141, glow=0.1, nucleus_radius=0.26)
    chlorine = Atom(1.3, CL_AT, charge="+17", core=0.55, count=200, seed=142, glow=0.1, nucleus_radius=0.32)
    names = VGroup(txt("H", cfg.FONT["section"], cfg.BLUE).move_to([H_AT[0], -1.75, 0]),
                   txt("Cl", cfg.FONT["section"], cfg.GREEN).move_to([CL_AT[0], -1.75, 0]))
    scene.play(FadeIn(hydrogen, scale=0.6), FadeIn(chlorine, scale=0.6), FadeIn(names), run_time=1.2)
    for atom in (hydrogen, chlorine):
        atom.cloud.set_level(0.35)

    # --- 2. An even sketch --------------------------------------------------------------------------
    head = dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    shared = BondCloud(H_AT, CL_AT, count=360, seed=143, width=0.62)
    scene.play(FadeIn(shared, scale=0.8), run_time=1.2)
    sketch = chip("first sketch: shared evenly", cfg.MUTED, cfg.FONT["small"]).move_to([0, 2.75, 0])
    scene.play(FadeIn(sketch, shift=DOWN * 0.15), run_time=0.7)

    # --- 3. Chlorine pulls harder --------------------------------------------------------------------
    beat(scene, t, 2)
    wrong = cross_mark(0.25).next_to(sketch, RIGHT, buff=0.25)
    scene.play(Create(wrong), run_time=0.5)
    tug = pull_arrows(CL_AT, 1.3, 4.0, count=6)
    scene.play(LaggedStart(*[GrowArrow(a) for a in tug], lag_ratio=0.1), run_time=0.8)
    scene.play(shared.lean_to(0.55), run_time=2.2)

    # --- 4. Partial charges -----------------------------------------------------------------------------
    beat(scene, t, 3)
    plus = eq(r"\delta^{+}", cfg.FONT["section"], cfg.CATION).move_to(H_AT + UP * 1.35)
    minus = eq(r"\delta^{-}", cfg.FONT["section"], cfg.ANION).move_to(CL_AT + UP * 1.9 + RIGHT * 0.2)
    scene.play(*fade_labels(VGroup(sketch, wrong), VGroup(plus, minus)), run_time=1.0)
    scene.play(Indicate(plus, color=cfg.WHITE), Indicate(minus, color=cfg.WHITE), run_time=1.0)

    # --- 5. The name ---------------------------------------------------------------------------------------
    beat(scene, t, 4)
    name = VGroup(txt("electronegativity", cfg.FONT["title"], cfg.GOLD),
                  txt('Attracting shared electrons', cfg.FONT["small"], cfg.WHITE))
    name.arrange(DOWN, buff=0.22).move_to([0, -2.95, 0])
    fit_width(name, 13.4)
    scene.play(FadeOut(names), Write(name[0]), run_time=1.2)
    scene.play(FadeIn(name[1], shift=UP * 0.1), run_time=0.8)

    # --- 6-8. Three ideas, kept apart ------------------------------------------------------------------------
    beat(scene, t, 5)
    head = swap_heading(scene, head, "Three different ideas")
    scene.play(FadeOut(VGroup(hydrogen, chlorine, shared, tug, plus, minus, name)), run_time=0.8)
    ion_card = card(["Ionization", "enthalpy"], cfg.GOLD, ["remove an electron", 'gas-phase atom'], -4.75)
    gain_card = card(["Electron gain", "enthalpy"], cfg.GREEN, ["add an electron", 'gas-phase atom'], 0.0)
    en_card = card(["Electro-", "negativity"], cfg.CYAN, ['attract shared electrons', "inside a bond"], 4.75)
    scene.play(FadeIn(ion_card, shift=UP * 0.2), run_time=0.8)
    a1 = Atom(0.75, ion_card.frame.get_center() + UP * 0.1, charge="+", count=150, seed=144, nucleus_radius=0.22)
    e1 = glow_dot(a1.center_point() + RIGHT * 0.55, 0.12)
    scene.play(FadeIn(a1, scale=0.6), FadeIn(e1), run_time=0.7)
    scene.play(FadeOut(e1, shift=RIGHT * 1.2 + UP * 0.8), run_time=1.0, rate_func=rush_into)

    beat(scene, t, 6)
    scene.play(FadeIn(gain_card, shift=UP * 0.2), run_time=0.8)
    a2 = Atom(0.75, gain_card.frame.get_center() + UP * 0.1, charge="+", count=150, seed=145, nucleus_radius=0.22)
    e2 = glow_dot(a2.center_point() + RIGHT * 1.75 + UP * 1.0, 0.12)
    scene.play(FadeIn(a2, scale=0.6), FadeIn(e2), run_time=0.6)
    scene.play(e2.animate.move_to(a2.center_point() + RIGHT * 0.55), run_time=1.0, rate_func=rush_from)

    beat(scene, t, 7)
    scene.play(FadeIn(en_card, shift=UP * 0.2), run_time=0.8)
    centre = en_card.frame.get_center() + UP * 0.1
    pair = VGroup(nucleus_core(None, 0.17).move_to(centre + LEFT * 1.05), nucleus_core(None, 0.24).move_to(centre + RIGHT * 1.05))
    mini = BondCloud(centre + LEFT * 1.05, centre + RIGHT * 1.05, count=200, seed=146, width=0.45)
    scene.play(FadeIn(pair), FadeIn(mini), run_time=0.8)
    scene.play(mini.lean_to(0.6), run_time=1.6)
    scene.play(Indicate(en_card.frame, color=cfg.CYAN, scale_factor=1.02), run_time=1.0)

    # --- 9. Pauling's scale ------------------------------------------------------------------------------------
    beat(scene, t, 8)
    head = swap_heading(scene, head, "Pauling scale")
    scene.play(FadeOut(VGroup(ion_card, gain_card, en_card, a1, a2, e2, pair, mini)), run_time=0.8)
    axis = Line([SCALE_LEFT, SCALE_Y, 0], [SCALE_RIGHT, SCALE_Y, 0], stroke_color=cfg.MUTED, stroke_width=4)
    ticks = VGroup(*[VGroup(Line([scale_x(v), SCALE_Y - 0.12, 0], [scale_x(v), SCALE_Y + 0.12, 0], stroke_color=cfg.MUTED,
                                 stroke_width=3),
                            txt(str(v), cfg.FONT["small"], cfg.MUTED).move_to([scale_x(v), SCALE_Y - 0.5, 0]))
                     for v in range(5)])
    relative = txt('Relative scale · no units', cfg.FONT["small"], cfg.MUTED).move_to([0, SCALE_Y - 1.2, 0])
    scene.play(Create(axis), FadeIn(ticks), FadeIn(relative), run_time=0.9)
    markers = VGroup()
    for symbol, colour in (("H", cfg.BLUE), ("Cl", cfg.GREEN)):
        value = ed.ELECTRONEGATIVITY[symbol]
        x = scale_x(value)
        markers.add(VGroup(glow_dot([x, SCALE_Y, 0], 0.14, colour),
                           txt(symbol, cfg.FONT["section"], colour).move_to([x, SCALE_Y + 0.85, 0]),
                           txt(f"{value:.1f}", cfg.FONT["label"], cfg.WHITE).move_to([x, SCALE_Y + 1.55, 0])))
    scene.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.2) for m in markers], lag_ratio=0.4), run_time=1.4)

    # --- 10. The bigger the difference ----------------------------------------------------------------------------
    beat(scene, t, 9)
    h_x, cl_x = scale_x(ed.ELECTRONEGATIVITY["H"]), scale_x(ed.ELECTRONEGATIVITY["Cl"])
    gap = BraceBetweenPoints([h_x, SCALE_Y - 0.95, 0], [cl_x, SCALE_Y - 0.95, 0], DOWN, color=cfg.GOLD)
    delta = ed.ELECTRONEGATIVITY["Cl"] - ed.ELECTRONEGATIVITY["H"]
    gap_tag = eq(rf"\Delta \approx {delta:.1f}", cfg.FONT["label"], cfg.GOLD).next_to(gap, DOWN, buff=0.15)
    scene.play(FadeOut(relative), GrowFromCenter(gap), FadeIn(gap_tag), run_time=1.0)
    lopsided = chip('Larger difference → less equal sharing', cfg.CYAN, cfg.FONT["small"]).move_to([0, 2.75, 0])
    scene.play(FadeIn(lopsided, shift=DOWN * 0.15), run_time=0.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["14"])
