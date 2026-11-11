"""Scene 03 — inside versus between. One 3D water molecule turns: its
covalent O-H bonds glow (intramolecular). The camera pulls back to a
tetrahedral cluster of five waters held by dashed green hydrogen bonds
(intermolecular). Bars compare the O-H bond (~460 kJ/mol) with a typical
attraction between waters (~20 kJ/mol). On boiling, the neighbours drift
away intact: the bonds inside survive; only the links between break.
"""

from manim_scenes.common import *


class Scene03InsideBetween(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "03", "Inside versus between")
    stage = Stage((-1.6, -0.2, 0), zoom=2.3, yaw=0.2, pitch=0.25, sway=0.05, spin=0.12)
    molecules, hbonds = water_cluster(scale=0.62)
    spread = Knob(0.0)
    built = []
    for index, atoms in enumerate(molecules):
        o = atoms[0][1]
        local = [(element, position - o) for element, position in atoms]
        centre = (lambda o=o: o * (1 + spread.value)) if index else np.zeros(3)
        m = molecule(stage, local, [(0, 1), (0, 2)], centre=centre)
        if index:
            for part in m.parts:
                part.presence = 0.0
        built.append(m)
    links = []
    for k, (h, acceptor) in enumerate(hbonds):
        if k < 2:     # the centre's H -> neighbour O
            a, b = built[0].balls[1 + k].where, built[1 + k].balls[0].where
        else:         # neighbour's first H -> the centre's O
            a, b = built[1 + k].balls[1].where, built[0].balls[0].where
        link = Segment(a, b, cfg.ATTRACT, width=4, opacity=0.95, dashed=True)
        link.presence = 0.0
        links.append(link)
    stage.add_body(*links)
    show(scene, stage, 1.0)

    # --- 2. Covalent bonds inside: intramolecular -------------------------------------------------------------
    beat(scene, t, 1)
    inside = VGroup(txt("covalent bonds", cfg.FONT["label"], cfg.WHITE),
                    txt("intramolecular: inside", cfg.FONT["small"], cfg.GOLD)).arrange(DOWN, buff=0.2)
    inside.move_to([4.4, 2.2, 0])
    glow = [Halo(ball, cfg.GOLD, reach=1.9, peak=0.2) for ball in built[0].balls]
    for g in glow:
        g.presence = 0.0
    stage.add_body(*glow)
    scene.play(FadeIn(inside, shift=LEFT * 0.2), *[stage.fade(g, 1.0) for g in glow], run_time=1.2)
    scene.play(*[stage.fade(g, 0.3) for g in glow], run_time=1.6, rate_func=there_and_back)
    scene.wait(1.5)

    # --- 3. A glass of water: intermolecular -------------------------------------------------------------------
    beat(scene, t, 2)
    between = VGroup(txt("attractions between", cfg.FONT["label"], cfg.WHITE),
                     txt("intermolecular", cfg.FONT["small"], cfg.ATTRACT)).arrange(DOWN, buff=0.2)
    between.move_to([4.4, -0.4, 0])
    scene.play(stage.zoom_to(1.4), *[stage.fade(g, 0.0) for g in glow], run_time=1.6)
    scene.play(*[stage.fade(p, 1.0) for m in built[1:] for p in m.parts], run_time=1.4)
    scene.play(*[stage.fade(link, 1.0) for link in links], FadeIn(between, shift=LEFT * 0.2), run_time=1.2)
    scene.wait(2.0)

    # --- 4. Much weaker: ~460 vs ~20 kJ/mol ----------------------------------------------------------------------
    beat(scene, t, 3)
    chart = bar_chart([pm.OH_BOND_KJ, pm.H_BOND_KJ], ["O–H bond", "between"], [cfg.GOLD, cfg.ATTRACT], at=[4.3, -0.5, 0],
                      width=4.6, height=3.6, value_labels=[f"≈ {fx(round(pm.OH_BOND_KJ, -1), 0)}", f"≈ {fx(pm.H_BOND_KJ, 0)}"],
                      bar_width=1.2)
    unit = txt("kJ/mol", cfg.FONT["small"], cfg.MUTED).next_to(chart, UP, buff=0.35)
    scene.play(FadeOut(VGroup(inside, between)), stage.glide([-3.2, -0.2, 0]), stage.zoom_to(1.25), run_time=1.0)
    scene.play(Create(chart.base), FadeIn(unit), run_time=0.6)
    scene.play(GrowFromEdge(chart.bars[0], DOWN), FadeIn(chart.names[0]), run_time=1.4)
    scene.play(FadeIn(chart.tops[0]), run_time=0.6)
    scene.play(GrowFromEdge(chart.bars[1], DOWN), FadeIn(chart.names[1]), FadeIn(chart.tops[1]), run_time=1.2)

    # --- 5. Boiling separates whole molecules ---------------------------------------------------------------------
    beat(scene, t, 4)
    boil = VGroup(txt("boiling:", cfg.FONT["label"], cfg.TEMPERATURE),
                  txt("whole molecules separate", cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.2)
    boil.move_to([4.3, 2.6, 0])
    scene.play(fade_through(VGroup(chart, unit), boil), run_time=0.9)
    scene.play(spread.to(stage, 0.9, run_time=3.2, rate_func=smooth), *[stage.fade(link, 0.0) for link in links],
               stage.zoom_to(1.0), run_time=3.2)
    intact = txt("bonds inside: intact", cfg.FONT["small"], cfg.GOLD).next_to(boil, DOWN, buff=0.4)
    scene.play(FadeIn(intact), run_time=0.7)

    # --- 6. Where do attractions come from? ---------------------------------------------------------------------------
    beat(scene, t, 5)
    kinds = VGroup(chip("dispersion", cfg.CLOUD), chip("dipole – dipole", cfg.DELTA_MINUS),
                   chip("dipole – induced dipole", cfg.PURPLE), chip("hydrogen bond", cfg.ATTRACT))
    kinds.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([4.2, -0.6, 0])
    fit_width(kinds, 6.0)
    scene.play(FadeOut(VGroup(boil, intact)), spread.to(stage, 0.0, run_time=1.4), run_time=1.4)
    scene.play(LaggedStart(*[FadeIn(k, shift=LEFT * 0.2) for k in kinds], lag_ratio=0.35), run_time=2.4)
    scene.play(Indicate(kinds[0], color=cfg.CLOUD, scale_factor=1.06), run_time=1.2)
    finish(scene, t, stage)
