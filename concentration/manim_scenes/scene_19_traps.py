"""Scene 19 — five concentration traps. Each statement gets a three-second
countdown, then a visual correction (never just a flashed formula): an
overflowing litre, two denominators, a reaction-dependent factor, a ratio vs
a fraction, and the density behind "1 mg/L = 1 ppm".
"""

from manim_scenes.common import *
from narration import SCRIPT

BEAKER = pm.Profile((0.0, 4.0), (1.3, 1.3), 3.1, 1000.0)
TRAPS = [
    ("To make 1 M, dissolve 1 mol of solute", "in 1 L of water."),
    ("A 1 M solution must", "also be 1 m."),
    ("The normality of H₂SO₄ is always", "twice its molarity."),
    ("Mole fraction = moles of solute", "÷ moles of solvent."),
    ("1 ppm always means", "1 mg per litre."),
]
STATEMENT_BEATS = (1, 3, 5, 7, 9)


class Scene19Traps(Scene):
    def construct(self) -> None:
        play_scene(self)


def statement(k: int) -> VGroup:
    header = chip(f"TRAP {k + 1} OF 5", cfg.WARNING, cfg.FONT["label"])
    lines = VGroup(*[txt(line, cfg.FONT["section"], cfg.WHITE) for line in TRAPS[k]]).arrange(DOWN, buff=0.18)
    fit_width(lines, 12.4)
    group = VGroup(header, lines).arrange(DOWN, buff=0.55).move_to([0, 0.9, 0])
    group.header, group.lines = header, lines
    return group


def ask(scene: Scene, t: float, k: int) -> VGroup:
    """Show trap k (its beat has begun), then count down to just before the reveal."""
    card = statement(k)
    scene.play(FadeIn(card.header, shift=DOWN * 0.15), run_time=0.6)
    scene.play(FadeIn(card.lines, shift=UP * 0.15), run_time=0.9)
    reveal_at = SCRIPT["19"][STATEMENT_BEATS[k] + 1][0]
    cue(scene, t, reveal_at - 3.3)
    countdown(scene, [0, -2.3, 0])
    return card


def lift(scene: Scene, card: VGroup) -> None:
    """Shrink a trap to the top of the frame, greyed, ready to be struck out."""
    scene.play(FadeOut(card.header), run_time=0.3)
    scene.play(card.lines.animate.scale(0.72).move_to([0, 2.7, 0]).set_color(cfg.MUTED), run_time=0.6)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "19", "Five concentration traps")
    intro = VGroup(txt("Five statements.", cfg.FONT["title"], cfg.WHITE),
                   txt("Each one sounds reasonable.", cfg.FONT["body"], cfg.MUTED),
                   txt("Each one is a trap.", cfg.FONT["body"], cfg.WARNING)).arrange(DOWN, buff=0.35).move_to([0, 0.4, 0])
    scene.play(FadeIn(intro[0], shift=UP * 0.15), run_time=0.8)
    scene.play(FadeIn(intro[1]), run_time=0.7)
    scene.play(FadeIn(intro[2]), run_time=0.7)
    scene.play(FadeOut(intro), run_time=0.5)

    # --- Trap 1: 1 mol in 1 L of water ---------------------------------------------------------------------------
    beat(scene, t, 1)
    card = ask(scene, t, 0)
    beat(scene, t, 2)
    lift(scene, card)
    x1 = cross_mark(0.22).next_to(card.lines, LEFT, buff=0.3)
    wrong, wglass, wswarm = solution_stage([-4.0, -3.55, 0], profile=BEAKER, volume=cd.wrong_way_mL(1000.0, 1.0), zoom=1.05,
                                           solvent=260, solute=6, seed=19, mark=True, spin=0.1)
    right, rglass, rswarm = solution_stage([3.3, -3.65, 0], profile=pm.flask_profile(), volume=1000.0, zoom=1.0,
                                           solvent=320, solute=6, seed=91, mark=True, spin=0.1)
    wglass.mark_glow = rglass.mark_glow = 1.0
    scene.play(Create(x1), run_time=0.4)
    show(scene, wrong, 0.8)
    over = VGroup(txt("more than 1 L", cfg.FONT["label"], cfg.WARNING),
                  txt("→ less than 1 M", cfg.FONT["label"], cfg.WARNING)).arrange(DOWN, buff=0.1).move_to([-0.6, 0.6, 0])
    scene.play(FadeIn(over), run_time=0.7)
    show(scene, right, 0.8)
    fix = VGroup(txt("dissolve, then", cfg.FONT["label"], cfg.RESULT), txt("fill to the mark", cfg.FONT["label"], cfg.RESULT))
    fix.arrange(DOWN, buff=0.1).move_to([6.2, 0.6, 0])
    scene.play(FadeIn(fix), run_time=0.7)

    # --- Trap 2: 1 M = 1 m ----------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    hide(scene, wrong, 0.5, FadeOut(VGroup(card.lines, x1, over, fix)))
    hide(scene, right, 0.3)
    card = ask(scene, t, 1)
    beat(scene, t, 4)
    lift(scene, card)
    x2 = cross_mark(0.22).next_to(card.lines, LEFT, buff=0.3)
    pair = VGroup(eq([rf"{M_TEXT}\ \mathrm{{M}}", "=", r"\frac{n_{\text{solute}}}{V_{\text{solution}}}"], cfg.FONT["section"]),
                  eq([rf"{m_TEXT}\ \mathrm{{m}}", "=", r"\frac{n_{\text{solute}}}{m_{\text{solvent}}}"], cfg.FONT["section"]))
    pair[0][2].set_color(cfg.VOLUME)
    pair[1][2].set_color(cfg.SOLVENT_MASS)
    pair.arrange(RIGHT, buff=1.4).move_to([0, -0.4, 0])
    fit_width(pair, 13.6)
    scene.play(Create(x2), FadeIn(pair[0], shift=UP * 0.15), run_time=1.0)
    scene.play(FadeIn(pair[1], shift=UP * 0.15), run_time=1.0)
    diff = txt("different denominators", cfg.FONT["body"], cfg.GOLD).move_to([0, -2.4, 0])
    scene.play(FadeIn(diff), run_time=0.7)

    # --- Trap 3: N is always 2M ---------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(VGroup(card.lines, x2, pair, diff)), run_time=0.5)
    card = ask(scene, t, 2)
    beat(scene, t, 6)
    lift(scene, card)
    x3 = cross_mark(0.22).next_to(card.lines, LEFT, buff=0.3)
    rows = VGroup(eq([r"\text{take one } \mathrm{H^+}:", r"z = 1", r"\Rightarrow", r"N = M"], cfg.FONT["body"]),
                  eq([r"\text{take both}:", r"z = 2", r"\Rightarrow", r"N = 2M"], cfg.FONT["body"]))
    for r in rows:
        r[1].set_color(cfg.EQUIVALENT)
        r[3].set_color(cfg.RESULT)
    rows.arrange(DOWN, buff=0.45).move_to([0, -0.2, 0])
    scene.play(Create(x3), FadeIn(rows[0], shift=UP * 0.15), run_time=1.0)
    scene.play(FadeIn(rows[1], shift=UP * 0.15), run_time=1.0)
    owner = txt("the factor belongs to the reaction", cfg.FONT["body"], cfg.GOLD).move_to([0, -2.4, 0])
    scene.play(FadeIn(owner), run_time=0.7)

    # --- Trap 4: solute / solvent -----------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(card.lines, x3, rows, owner)), run_time=0.5)
    card = ask(scene, t, 3)
    beat(scene, t, 8)
    lift(scene, card)
    x4 = cross_mark(0.22).next_to(card.lines, LEFT, buff=0.3)
    ratio = eq([r"\frac{n_{\text{solute}}}{n_{\text{solvent}}}", "=", rf"\frac{{{N_SOLUTE}}}{{{N_SOLVENT}}}", "=",
                fx(REF.mole_ratio, 4)], cfg.FONT["section"])
    ratio[4].set_color(cfg.WARNING)
    frac = eq([r"\frac{n_{\text{solute}}}{n_{\text{total}}}", "=", rf"\frac{{{N_SOLUTE}}}{{{fx(REF.n_total, 1)}}}", "=", X_TEXT],
              cfg.FONT["section"])
    frac[4].set_color(cfg.RESULT)
    labels = VGroup(txt("mole ratio", cfg.FONT["label"], cfg.WARNING), txt("mole fraction", cfg.FONT["label"], cfg.RESULT))
    block = VGroup(VGroup(labels[0], ratio).arrange(RIGHT, buff=0.5), VGroup(labels[1], frac).arrange(RIGHT, buff=0.5))
    block.arrange(DOWN, buff=0.45, aligned_edge=RIGHT).move_to([0, -0.4, 0])
    fit_width(block, 13.4)
    scene.play(Create(x4), FadeIn(block[0], shift=UP * 0.15), run_time=1.0)
    scene.play(FadeIn(block[1], shift=UP * 0.15), run_time=1.0)
    grows = txt("close here; the gap grows in stronger solutions", cfg.FONT["small"], cfg.GOLD).move_to([0, -2.75, 0])
    fit_width(grows, 13.0)
    scene.play(FadeIn(grows), run_time=0.7)

    # --- Trap 5: 1 ppm = 1 mg/L --------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(VGroup(card.lines, x4, block, grows)), run_time=0.5)
    card = ask(scene, t, 4)
    beat(scene, t, 10)
    lift(scene, card)
    x5 = cross_mark(0.22).next_to(card.lines, LEFT, buff=0.3)
    lines = VGroup(
        VGroup(txt("water", cfg.FONT["body"], cfg.SOLVENT), eq(r"1\ \mathrm{mg/L} \approx 1\ \mathrm{ppm}", cfg.FONT["body"])),
        VGroup(txt("ethanol", cfg.FONT["body"], cfg.ETHANOL),
               eq(rf"1\ \mathrm{{mg/L}} \approx {fx(cd.ppm_in_ethanol_for_1_mg_per_L(), 2)}\ \mathrm{{ppm\ (mass)}}", cfg.FONT["body"])),
    )
    for row in lines:
        row.arrange(RIGHT, buff=0.5)
    lines.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([0, -0.3, 0])
    scene.play(Create(x5), FadeIn(lines[0], shift=UP * 0.15), run_time=1.0)
    scene.play(FadeIn(lines[1], shift=UP * 0.15), run_time=1.0)
    why = eq(rf"1\ \mathrm{{L\ ethanol}} \approx {fx(cd.ETHANOL_DENSITY_20C, 3)}\ \mathrm{{kg}}", cfg.FONT["label"], cfg.MUTED)
    why.move_to([0, -2.4, 0])
    scene.play(FadeIn(why), run_time=0.7)

    # --- One escape route: what's on top, what's on the bottom ------------------------------------------------------------------------
    beat(scene, t, 11)
    scene.play(FadeOut(VGroup(card.lines, x5, lines, why)), run_time=0.6)
    route = eq([r"\frac{", r"\text{what's on top?}", "}{", r"\text{what's on the bottom?}", "}"], cfg.FONT["title"])
    route[1].set_color(cfg.SOLUTE)
    route[3].set_color(cfg.VOLUME)
    route.move_to([0, 0.3, 0])
    fit_width(route, 12.0)
    scene.play(Write(route), run_time=1.8)
    scene.play(Indicate(route[3], color=cfg.WHITE, scale_factor=1.08), run_time=1.2)

    # --- Onward to the map ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    scene.play(route.animate.scale(0.62).move_to([0, 2.75, 0]), run_time=1.0)
    ring = [np.array([2.3 * np.cos(a), 2.3 * np.sin(a) - 0.95, 0]) for a in np.linspace(0, 2 * np.pi, 7)[:-1] + 0.3]
    hub = glow_dot([0, -0.95, 0], cfg.CYAN, 0.12)
    nodes = VGroup(*[glow_dot(p, c, 0.1) for p, c in zip(ring, (cfg.VOLUME, cfg.SOLVENT_MASS, cfg.EQUIVALENT, cfg.AMOUNT,
                                                               cfg.SOLUTION_MASS, cfg.GOLD))])
    spokes = VGroup(*[glow_line([0, -0.95, 0], p, cfg.CYAN, 1.6) for p in ring])
    scene.play(FadeIn(hub, scale=0.5), run_time=0.8)
    scene.play(LaggedStart(*[Create(s) for s in spokes], lag_ratio=0.15), LaggedStart(*[FadeIn(n, scale=0.4) for n in nodes],
                                                                                         lag_ratio=0.15), run_time=3.0)
    scene.play(Rotate(VGroup(spokes, nodes), angle=PI / 3, about_point=[0, -0.95, 0]), run_time=17.5, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["19"])
