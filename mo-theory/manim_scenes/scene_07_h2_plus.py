"""Chapter 07 — H2+: one electron, half a bond.

The electron's slot comes from ``mo_models.fill("H2+")`` and the bond order
from its bonding / antibonding counts. The energy curve on the right is the
LCAO result (``physics_models.h2plus_energies``); the white point is the exact
minimum from ``mo_data`` (deeper, at a shorter distance).
"""

from manim_scenes.common import *

DIAGRAM_AT = np.array([-3.3, -0.35, 0])
PANEL_X = 4.75     # the right-hand panel spans x = 1.8 .. 7.7
PLOT = PlotFrame([1.6, -0.4, 0], 0.7, 0.62)


class Scene07H2Plus(Scene):
    def construct(self) -> None:
        play_scene(self)


def one_s_diagram(atoms: tuple[str, str], molecule: str | None = None) -> MODiagram:
    """The 1s diagram on the left half of the frame, shared by chapters 07-09."""
    return MODiagram(mo.diagram("1s"), center=DIAGRAM_AT, height=5.0, ao_x=2.9, mo_width=1.2, ao_width=1.0,
                     atoms=atoms, molecule=molecule)


def count_chips(diagram: MODiagram, filling: mo.Filling) -> tuple[VGroup, VGroup]:
    """'bonding: n' and 'antibonding: n' chips beside the two levels."""
    nb = chip(f"bonding: {filling.bonding}", cfg.BONDING).next_to(diagram.labels["s1s"], RIGHT, buff=0.3)
    na = chip(f"antibonding: {filling.antibonding}", cfg.ANTIBONDING).next_to(diagram.labels["s1s*"], RIGHT, buff=0.3)
    return nb, na


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "07", "One electron, half a bond")
    filling = mo.fill("H2+")

    # --- 1. Build molecules one electron at a time ----------------------------------------------------------------------
    diagram = one_s_diagram(("H", "H⁺"))
    scene.play(FadeIn(diagram), run_time=1.6)
    dismiss_opening_title(scene, t, head, at=3.0)

    # --- 2. Two protons, one electron: H2+ ---------------------------------------------------------------------------------
    beat(scene, t, 1)
    lone = diagram.atom_electrons(1, "L")[0]
    name = formula("H2+", cfg.FONT["title"]).move_to([PANEL_X, 2.4, 0])
    parts = VGroup(txt("2 protons", cfg.FONT["body"], cfg.WHITE), txt("1 electron", cfg.FONT["body"], cfg.UNPAIRED))
    parts.arrange(DOWN, buff=0.3).move_to([PANEL_X, 0.9, 0])
    scene.play(FadeIn(lone, shift=DOWN * 0.3), Write(name), run_time=1.2)
    scene.play(FadeIn(parts, shift=UP * 0.2), run_time=1.0)

    # --- 3. Into the lowest orbital ---------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    anims, arrows = fly_electrons(diagram, [lone], filling)
    scene.play(*anims, run_time=1.6)
    lowest = diagram.highlight("s1s", cfg.GOLD)
    scene.play(Create(lowest), run_time=0.8)
    scene.play(FadeOut(lowest), run_time=0.6)

    # --- 4. Keep score: bond order ---------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    title = result_label("Bond order", cfg.GOLD, cfg.FONT["title"]).move_to([PANEL_X, 2.4, 0])
    scene.play(FadeOut(parts), FadeOut(name), run_time=0.5)
    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)

    # --- 5. The formula -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    formula_tex = bond_order_formula(cfg.FONT["section"]).move_to([PANEL_X, 0.9, 0])
    fit_width(formula_tex, 5.8)
    scene.play(Write(formula_tex), run_time=1.6)
    legend = VGroup(txt("bonding electrons", cfg.FONT["small"], cfg.BONDING),
                    txt("antibonding electrons", cfg.FONT["small"], cfg.ANTIBONDING)).arrange(DOWN, buff=0.18)
    legend.move_to([PANEL_X, -0.7, 0])
    scene.play(FadeIn(legend), run_time=0.8)

    # --- 6. One minus zero, over two ------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    nb, na = count_chips(diagram, filling)
    # Stack the counts outside the levels, keeping the calculation panel clear.
    nb.next_to(diagram.levels["s1s"], DOWN, buff=0.42)
    na.next_to(diagram.levels["s1s*"], UP, buff=0.42)
    numbers = bond_order_numbers(filling.bonding, filling.antibonding, cfg.FONT["title"]).move_to([PANEL_X, -0.95, 0])
    scene.play(FadeIn(nb), FadeIn(na), FadeOut(legend), run_time=1.0)
    scene.play(Write(numbers[:5]), run_time=1.4)
    scene.play(Write(numbers[5:]), run_time=1.0)

    # --- 7. Half a bond! --------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    half = result_label("half a bond!", cfg.GREEN, cfg.FONT["title"]).move_to([PANEL_X, -2.4, 0])
    scene.play(FadeIn(half, scale=1.15), Indicate(numbers[-1], color=cfg.WHITE, scale_factor=1.3), run_time=1.2)

    # --- 8. It really exists ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(*[FadeOut(m) for m in (title, formula_tex, numbers, half)], run_time=0.8)
    real = VGroup(formula("H2+", cfg.FONT["title"]), txt("is real", cfg.FONT["section"], cfg.GREEN)).arrange(RIGHT, buff=0.3)
    real.move_to([PANEL_X, 2.3, 0])
    length = chip(f"bond length ≈ {md.BOND_LENGTH_PM['H2+']:.0f} pm", cfg.WHITE).move_to([PANEL_X, 1.1, 0])
    scene.play(FadeIn(real, shift=DOWN * 0.2), run_time=1.0)
    scene.play(FadeIn(length, shift=UP * 0.15), run_time=1.0)

    # --- 9. LCAO predicts a valley; the exact one is deeper ---------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    x_axis = Arrow(PLOT.point(0.8, 0), PLOT.point(8.6, 0), buff=0, color=cfg.MUTED, stroke_width=4, tip_length=0.2)
    lcao = plain_curve(lambda r: np.minimum(pm.h2plus_energies(r)[0] * pm.HARTREE_EV, 2.5), (1.0, 8.4), PLOT,
                       cfg.BONDING, width=5)
    exact = glow_dot(PLOT.point(md.H2PLUS_EXACT_RE_BOHR, -md.H2PLUS_EXACT_DE_EV), cfg.WHITE, radius=0.1)
    r_min, depth = pm.h2plus_minimum()
    lcao_min = glow_dot(PLOT.point(r_min, -depth), cfg.BONDING, radius=0.09)
    keys = VGroup(txt("LCAO", cfg.FONT["small"], cfg.BONDING), txt("exact", cfg.FONT["small"], cfg.WHITE))
    keys[0].next_to(lcao_min, RIGHT, buff=0.3)
    keys[1].next_to(exact, DOWN, buff=0.25)
    scene.play(FadeOut(length), real.animate.move_to([PANEL_X, 2.9, 0]), GrowArrow(x_axis), run_time=0.8)
    scene.play(Create(lcao), run_time=1.6)
    scene.play(FadeIn(lcao_min), FadeIn(keys[0]), run_time=0.6)
    scene.play(FadeIn(exact, scale=0.5), FadeIn(keys[1]), run_time=0.8)
    bound = caption("Both agree: H₂⁺ is bound", cfg.GREEN)
    scene.play(FadeIn(bound), run_time=0.8)

    # --- 10. A bond without a pair ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    no_pair = caption("A bond doesn't always need a shared pair", cfg.GOLD)
    scene.play(fade_through(bound, no_pair), Indicate(arrows[0], color=cfg.WHITE, scale_factor=1.3), run_time=1.2)
    scene.remove(bound)
    scene.play(arrows[0].animate.scale(1.15), run_time=2.0, rate_func=there_and_back)
    scene.play(Indicate(exact, color=cfg.GOLD, scale_factor=1.4), run_time=1.6)
    scene.play(Indicate(lcao_min, color=cfg.GOLD, scale_factor=1.4), run_time=1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["07"])
