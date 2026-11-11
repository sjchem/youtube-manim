"""Scene 06 — induced dipoles and hydrogen bonds. Hydrogen chloride's
delta-plus end pulls an argon atom's cloud toward it: a dipole-induced dipole
attraction, also -1/r^6. Then directional hydrogen bonding:
a 3D water dimer (the electron-poor hydrogen glows delta-plus), the full
tetrahedral network with four dashed hydrogen bonds, and ammonia accepting a
hydrogen bond on its nitrogen lone pair. A temperature scale ends it: H2S
boils near -60 C, water at 100 C.
"""

from manim_scenes.common import *

SCALE = 0.62           # stage units per angstrom


class Scene06HydrogenBonds(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "06", "Induced dipoles and hydrogen bonds")
    cl = bead([-4.6, -0.2, 0], cfg.ATOM["Cl"], 0.55)
    h = bead([-3.45, -0.2, 0], cfg.ATOM["H"], 0.3)
    bond = Line([-4.1, -0.2, 0], [-3.7, -0.2, 0], stroke_color=cfg.WHITE, stroke_width=10)
    minus = txt("δ−", 36, cfg.DELTA_MINUS).next_to(cl, UP, buff=0.18)
    plus = txt("δ+", 36, cfg.DELTA_PLUS).next_to(h, UP, buff=0.18)
    hcl = VGroup(bond, cl, h, minus, plus)
    names = VGroup(txt("HCl", cfg.FONT["small"], cfg.WHITE).next_to(VGroup(cl, h), DOWN, buff=0.5))
    argon = Atom2D([0.2, -0.2, 0], 1.25, label="Ar")
    pull = Knob(0.0)
    argon.add_updater(lambda m: setattr(m, "offset", np.array([-0.42 * pull.value, 0, 0])), index=0)
    scene.play(FadeIn(hcl), FadeIn(names), FadeIn(argon), run_time=1.2)

    # --- 2. The dipole distorts argon's cloud: an induced dipole ---------------------------------------------------
    beat(scene, t, 1)
    tag = txt("induced dipole", cfg.FONT["section"], cfg.PURPLE).move_to([0.2, 2.6, 0])
    scene.play(pull.to(argon, 1.0, run_time=2.4), run_time=2.4)
    scene.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.8)
    arrows = VGroup(VecArrow([-1.6, -2.0, 0], [-2.4, -2.0, 0], cfg.ATTRACT, width=0.08, live=False),
                    VecArrow([-2.9, -2.0, 0], [-2.1, -2.0, 0], cfg.ATTRACT, width=0.08, live=False))
    scene.play(FadeIn(arrows), run_time=0.8)

    # --- 3. Also -1/r^6 ---------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    law = VGroup(txt("dipole – induced dipole", cfg.FONT["label"], cfg.WHITE),
                 eq(r"U \propto -\frac{1}{r^6}", cfg.FONT["body"], cfg.ATTRACT)).arrange(DOWN, buff=0.3).move_to([4.6, 0.2, 0])
    scene.play(FadeIn(law, shift=LEFT * 0.2), run_time=1.2)

    # --- 4. The hydrogen bond ------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    hb = result_label("the hydrogen bond", cfg.ATTRACT, cfg.FONT["section"]).move_to([0, 3.0, 0])
    scene.play(FadeOut(VGroup(hcl, names, argon, tag, arrows, law)), run_time=0.8)
    scene.play(FadeIn(hb, scale=0.95), run_time=0.9)

    # --- 5. Hydrogen on O, N or F: nearly bare, strongly positive ------------------------------------------------------
    beat(scene, t, 4)
    stage = Stage((-0.6, -0.5, 0), zoom=1.85, yaw=-0.3, pitch=0.2, sway=0.04)
    molecules, hbonds = water_cluster(SCALE)
    built = []
    for index, atoms in enumerate(molecules):
        m = molecule(stage, atoms, [(0, 1), (0, 2)])
        built.append(m)
        if index > 1:
            for part in m.parts:
                part.presence = 0.0
    links = []
    for k in range(4):
        a, b = (built[0].balls[1 + k].where, built[1 + k].balls[0].where) if k < 2 else (built[1 + k].balls[1].where,
                                                                                         built[0].balls[0].where)
        link = Segment(a, b, cfg.ATTRACT, width=4.5, opacity=0.95, dashed=True)
        link.presence = 0.0
        links.append(link)
    stage.add_body(*links)
    bare = Halo(built[0].balls[1], cfg.DELTA_PLUS, reach=2.6, peak=0.3)
    bare.presence = 0.0
    stage.add_body(bare)
    plus_tag = Tag(txt("δ+", 36, cfg.DELTA_PLUS), built[0].balls[1].where, UP * 0.5 + LEFT * 0.2)
    plus_tag.presence = 0.0
    stage.add_overlay(plus_tag)
    show(scene, stage, 1.0, FadeOut(hb))
    note = VGroup(txt("H on O, N or F:", cfg.FONT["label"], cfg.WHITE),
                  txt("electron-poor · δ+", cfg.FONT["label"], cfg.DELTA_PLUS)).arrange(DOWN, buff=0.22)
    note.move_to([4.2, 2.6, 0])
    scene.play(FadeIn(note, shift=LEFT * 0.2), stage.fade(bare, 1.0), stage.fade(plus_tag, 1.0), run_time=1.4)
    scene.play(stage.fade(links[0], 1.0), *stage.turn(yaw=0.2), run_time=3.0)

    # --- 6. A lone pair on the neighbour; up to four links: a network ------------------------------------------------------
    beat(scene, t, 5)
    four = txt("up to four per molecule", cfg.FONT["label"], cfg.ATTRACT).move_to([4.2, 2.6, 0])
    scene.play(fade_through(note, four), stage.fade(bare, 0.0), stage.fade(plus_tag, 0.0), stage.zoom_to(1.25),
               stage.glide([-0.8, -0.4, 0]), run_time=1.4)
    for m, link in zip(built[2:], links[1:]):
        scene.play(*[stage.fade(p, 1.0) for p in m.parts], stage.fade(link, 1.0), run_time=0.9)
    scene.play(*stage.turn(yaw=1.2), run_time=6.0)

    # --- 7. Ammonia: an H bond to the nitrogen lone pair -------------------------------------------------------------------
    beat(scene, t, 6)
    t0 = mu.unit(molecules[0][1][1])
    n_at = t0 * (0.96 + 2.0) * SCALE
    pose = mu.rotation_between([0, 1, 0], -t0)
    nh3 = molecule(stage, [(e, pose @ p) for e, p in ammonia_atoms(SCALE)], [(0, 1), (0, 2), (0, 3)], centre=n_at)
    for p in nh3.parts:
        p.presence = 0.0
    to_n = Segment(built[0].balls[1].where, nh3.balls[0].where, cfg.ATTRACT, width=4.5, opacity=0.95, dashed=True)
    to_n.presence = 0.0
    stage.add_body(to_n)
    amm = txt("ammonia: N lone pair", cfg.FONT["label"], cfg.ATOM["N"]).move_to([4.2, 2.6, 0])
    scene.play(*[stage.fade(p, 0.0) for p in built[1].parts], stage.fade(links[0], 0.0), fade_through(four, amm), run_time=1.0)
    scene.play(*[stage.fade(p, 1.0) for p in nh3.parts], stage.fade(to_n, 1.0), run_time=1.2)

    # --- 8. H2S near -60 C; water 100 C ------------------------------------------------------------------------------------
    beat(scene, t, 7)
    axis = NumberLine(x_range=[-100, 120, 20], length=5.6, rotation=PI / 2, stroke_color=cfg.MUTED, stroke_width=3,
                      include_tip=False).move_to([3.4, -0.4, 0])
    def mark(celsius: float, label: str, color: str) -> VGroup:
        p = axis.n2p(celsius)
        tick = Line(p + LEFT * 0.3, p + RIGHT * 0.3, stroke_color=color, stroke_width=6)
        words = txt(label, cfg.FONT["small"], color).next_to(tick, RIGHT, buff=0.25)
        return VGroup(tick, words)
    h2s = mark(pm.HYDRIDE_BOILING_C["H2S"], f"H₂S  {fx(pm.HYDRIDE_BOILING_C['H2S'], 0)} °C", cfg.ATOM["S"])
    h2o = mark(pm.HYDRIDE_BOILING_C["H2O"], f"H₂O  {fx(pm.HYDRIDE_BOILING_C['H2O'], 0)} °C", cfg.CYAN)
    gap = VecArrow(axis.n2p(pm.HYDRIDE_BOILING_C["H2S"]) + LEFT * 0.6, axis.n2p(pm.HYDRIDE_BOILING_C["H2O"]) + LEFT * 0.6,
                   cfg.ATTRACT, width=0.1, live=False)
    why = txt("hydrogen bonds", cfg.FONT["small"], cfg.ATTRACT).next_to(gap, LEFT, buff=0.25)
    bp = txt("boiling point", cfg.FONT["small"], cfg.MUTED).next_to(axis, UP, buff=0.3)
    scene.play(FadeOut(amm), stage.glide([-3.6, -0.4, 0]), stage.zoom_to(1.0), run_time=1.2)
    scene.play(Create(axis), FadeIn(bp), run_time=1.0)
    scene.play(FadeIn(h2s, shift=RIGHT * 0.2), run_time=1.0)
    scene.play(FadeIn(h2o, shift=RIGHT * 0.2), run_time=1.0)
    scene.play(GrowFromEdge(gap, DOWN), FadeIn(why), run_time=1.4)

    # --- 9. Hydrogen bonds hold liquid water together ------------------------------------------------------------------------
    beat(scene, t, 8)
    holds = result_label("holds liquid water together", cfg.ATTRACT, cfg.FONT["body"]).move_to([-3.4, 3.1, 0])
    scene.play(FadeIn(holds, shift=DOWN * 0.1), run_time=0.9)
    finish(scene, t, stage)
