"""Same ten electrons, four different nuclei, four different sizes.

The four clouds start identical (the oxide size) and contract to their own
ionic radii (Pauling values, as quoted by NCERT) as the proton count is
revealed. Arrow thickness is Slater's felt charge for each ion.
"""

from manim_scenes.common import *

IONS = (("O2-", "O", "2-", 8), ("F-", "F", "-", 9), ("Na+", "Na", "+", 11), ("Mg2+", "Mg", "2+", 12))
XS = (-5.25, -1.75, 1.75, 5.25)
Y = 0.6
SCALE = 0.0095
NAME_Y = -1.75
COUNT_Y = -2.5
VALUE_Y = -3.25


class Scene08Isoelectronic(Scene):
    def construct(self) -> None:
        play_scene(self)


def size(key: str) -> float:
    return ed.IONIC_RADII_PM[key] * SCALE


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "08", "Same electrons, different size")

    start_size = size("O2-")
    ions, names = [], []
    for index, ((key, base, charge, _), x) in enumerate(zip(IONS, XS)):
        ion = Atom(start_size, [x, Y, 0], charge=None, core=None, count=380, seed=81 + index, nucleus_radius=0.3,
                   glow=0.18)
        ions.append(ion)
        colour = cfg.ANION if "-" in charge else cfg.CATION
        names.append(eq(ion_tex(base, charge), cfg.FONT["section"], colour).move_to([x, NAME_Y, 0]))
    scene.play(LaggedStart(*[FadeIn(ion, scale=0.6) for ion in ions], lag_ratio=0.2), run_time=1.6)
    scene.play(LaggedStart(*[FadeIn(n, shift=UP * 0.15) for n in names], lag_ratio=0.15), run_time=1.2)

    # --- 1. Ten electrons each -----------------------------------------------------------------
    head = dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    counts = [txt("10 electrons", cfg.FONT["small"], cfg.CYAN).move_to([x, COUNT_Y, 0]) for x in XS]
    for count in counts:
        scene.play(FadeIn(count, shift=UP * 0.1), run_time=0.45)
    same = eq(r"1s^{2}\,2s^{2}\,2p^{6}", cfg.FONT["label"], cfg.GREEN).move_to([0, 2.95, 0])
    scene.play(Write(same), run_time=1.0)

    # --- 2. Only the nucleus differs ------------------------------------------------------------
    beat(scene, t, 2)
    reveal = []
    for ion, (_, _, _, protons) in zip(ions, IONS):
        reveal += relabel_nucleus(ion, f"+{protons}")
    scene.play(LaggedStart(*reveal, lag_ratio=0.15), run_time=1.6)
    scene.play(*[Flash(ion.center_point(), color=cfg.PROTON_COLOR, flash_radius=0.5, num_lines=10) for ion in ions],
               run_time=0.9)

    # --- 3. Stronger pull, smaller cloud ------------------------------------------------------------
    beat(scene, t, 3)
    arrows = [pull_arrows(ion.center_point(), start_size, pm.slater_zeff(protons, 10), count=6)
              for ion, (_, _, _, protons) in zip(ions, IONS)]
    scene.play(*[FadeIn(a) for a in arrows], run_time=0.8)
    shrink = []
    for ion, arrow_set, (key, _, _, protons) in zip(ions, arrows, IONS):
        shrink += ion.resize(size(key))
        shrink.append(Transform(arrow_set, pull_arrows(ion.center_point(), size(key), pm.slater_zeff(protons, 10), count=6)))
    scene.play(*shrink, run_time=2.6)

    # --- 4. The numbers -----------------------------------------------------------------------------
    beat(scene, t, 4)
    values = [txt(f"{ed.IONIC_RADII_PM[key]} pm", cfg.FONT["label"], cfg.WHITE).move_to([x, VALUE_Y, 0])
              for (key, *_), x in zip(IONS, XS)]
    scene.play(LaggedStart(*[FadeIn(v, shift=UP * 0.15) for v in values], lag_ratio=0.3), run_time=1.8)
    trend = glow_arrow([XS[0] - 0.6, -3.9, 0], [XS[-1] + 0.6, -3.9, 0], cfg.GOLD, 5)
    scene.play(GrowArrow(trend.arrow), FadeIn(trend[0]), run_time=0.9)

    # --- 5. Less than half --------------------------------------------------------------------------
    beat(scene, t, 5)
    ghost = DashedVMobject(Circle(radius=size("O2-"), stroke_color=cfg.MUTED, stroke_width=3), num_dashes=40)
    ghost.move_to(ions[-1].center_point())
    half = chip('Mg²⁺ < half of O²⁻', cfg.GOLD, cfg.FONT["small"]).move_to([3.5, 2.95, 0])
    scene.play(FadeOut(same), FadeOut(VGroup(*arrows)), Create(ghost), FadeIn(half, shift=DOWN * 0.15), run_time=1.2)
    scene.play(Indicate(values[0], color=cfg.WHITE), Indicate(values[-1], color=cfg.WHITE), run_time=1.2)

    # --- 6. The nucleus decides ------------------------------------------------------------------------
    beat(scene, t, 6)
    rule = chip('More protons → smaller', cfg.WHITE, cfg.FONT["label"]).move_to([0, 2.95, 0])
    fit_width(rule, 13.0)
    scene.play(*fade_labels(half, rule), run_time=0.9)
    scene.play(*[Flash(ion.center_point(), color=cfg.GOLD, flash_radius=0.45, num_lines=10) for ion in ions], run_time=1.0)

    # --- 7. Next question --------------------------------------------------------------------------------
    beat(scene, t, 7)
    next_q = chip('How hard to remove one?', cfg.GOLD, cfg.FONT["body"]).move_to([0, 2.95, 0])
    fit_width(next_q, 13.0)
    scene.play(*fade_labels(rule, next_q), run_time=0.9)
    target = ions[2]
    tug = glow_dot(target.center_point() + RIGHT * size("Na+") * 0.8, 0.13)
    scene.play(FadeIn(tug, scale=0.4), run_time=0.4)
    scene.play(tug.animate(rate_func=there_and_back).shift(RIGHT * 0.9 + UP * 0.4), run_time=1.6)
    scene.play(tug.animate(rate_func=there_and_back).shift(RIGHT * 0.9 + UP * 0.4), run_time=1.4)
    end_scene(scene, t, cfg.SCENE_DURATIONS["08"])
