"""Chapter 20 — molecules live in 3D: the synthesis, on the opening pair.

Carbon dioxide and water return exactly as the film opened. Layer by layer
they gain what the film built: their electron regions (VSEPR), the hybrid
orbitals along their bonds, and their bond dipoles and sums. Then the flat
Lewis structures from the first shot return, and give way to the turning
3D models for the last line.
"""

from manim_scenes.common import *

CO2_AT = np.array([-4.0, 0.6, 0])
H2O_AT = np.array([4.0, 0.85, 0])


class Scene20BigPicture(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "20", "Molecules live in 3D")
    water = ml.molecule("H2O")
    co2_stage = Stage(CO2_AT, zoom=1.0, yaw=0.55, pitch=0.3, sway=0.15)
    co2 = MoleculeModel(co2_stage, ml.molecule("CO2"))
    h2o_stage = Stage(H2O_AT, zoom=1.0, yaw=-0.3, pitch=0.25, sway=0.15)
    h2o = MoleculeModel(h2o_stage, water, orient=bisect_down(water.sites[2].direction, water.sites[3].direction),
                        lone_pairs=False)
    arcs = [co2.arc(0, 1, radius=1.15, live=True, label_gap=0.55, size=cfg.FONT["body"]),
            h2o.arc(2, 3, radius=1.05, live=True, label_gap=0.5, size=cfg.FONT["body"])]
    for arc in arcs:
        arc.presence = 1.0
    names = VGroup(formula("CO2").move_to([CO2_AT[0], -1.9, 0]), formula("H2O").move_to([H2O_AT[0], -1.9, 0]))
    scene.add(co2_stage, h2o_stage)
    co2_stage.presence = h2o_stage.presence = 0.0
    scene.play(co2_stage.fade(co2_stage, 1.0), h2o_stage.fade(h2o_stage, 1.0), FadeIn(names), run_time=1.4)
    dismiss_opening_title(scene, t, head)

    # --- 2. The answer: how the electrons were arranged -------------------------------------------------------------
    beat(scene, t, 1)
    electrons = caption("Not the number of atoms: the electrons", cfg.PURPLE)
    scene.play(*co2.fade("domains", 1.0), *h2o.fade("domains", 1.0), *h2o.show_lone_pairs(1.0), FadeIn(electrons),
               *[s.fade(a, 0.0) for s, a in zip((co2_stage, h2o_stage), arcs)], run_time=1.6)

    # --- 3. VSEPR: count the regions ----------------------------------------------------------------------------------
    beat(scene, t, 2)
    counts = VGroup(chip("2 regions", cfg.CYAN, cfg.FONT["label"]).move_to([CO2_AT[0], -2.75, 0]),
                    chip("4 regions", cfg.CYAN, cfg.FONT["label"]).move_to([H2O_AT[0], -2.75, 0]))
    vsepr = top_caption("VSEPR predicts the shape", cfg.CYAN)
    scene.play(FadeIn(counts), FadeIn(vsepr), FadeOut(electrons), run_time=1.2)

    # --- 4. Hybridization: orbitals along the bonds -----------------------------------------------------------------------
    beat(scene, t, 3)
    hybrids = [Orbital(co2_stage, ORIGIN, co2._dir(i), om.SP_ALPHA["sp"], units=0.45, opacity=0.55) for i in range(2)]
    hybrids += [Orbital(h2o_stage, ORIGIN, h2o._dir(i), om.SP_ALPHA["sp3"], units=0.38, opacity=0.5,
                        plus=cfg.LONE_PAIR_COLOR if water.sites[i].kind == "E" else cfg.PHASE_PLUS) for i in range(4)]
    for h in hybrids:
        h.set_presence(0.0)
    hybrid_cap = top_caption("Hybridization describes the orbitals", cfg.BLUE)
    scene.play(*co2.fade("domains", 0.0), *h2o.fade("domains", 0.0), *h2o.show_lone_pairs(0.0),
               *[a for h in hybrids for a in h.fade(1.0)], fade_through(vsepr, hybrid_cap), run_time=1.8)
    scene.remove(vsepr)

    # --- 5. Bond polarity + shape ---------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scale = 1.5
    co2_vecs = [v * scale for v in pm.bond_dipoles("C", [("O", co2.dirs[i]) for i in range(2)], gd.ELECTRONEGATIVITY)]
    h2o_vecs = [v * scale for v in pm.bond_dipoles("O", [("H", h2o.dirs[i]) for i in (2, 3)], gd.ELECTRONEGATIVITY)]
    co2_arrows = [Vector(co2.point(i, 0.25) + UP * 0.6, co2.point(i, 0.25) + UP * 0.6 + co2_vecs[i], cfg.BOND_DIPOLE,
                         width=0.09, tip=0.28) for i in range(2)]
    net = pm.vector_sum(h2o_vecs)
    h2o_net = Vector(ORIGIN + UP * 0.2, UP * 0.2 + mu.unit(net) * 2.0, cfg.NET_DIPOLE, width=0.15, tip=0.4)
    for item, stage in [(a, co2_stage) for a in co2_arrows] + [(h2o_net, h2o_stage)]:
        item.presence = 0.0
        stage.add_overlay(item)
    verdicts = VGroup(eq(r"\mu = 0", cfg.FONT["body"], cfg.NET_DIPOLE).move_to(counts[0]),
                      eq(r"\mu \neq 0", cfg.FONT["body"], cfg.NET_DIPOLE).move_to(counts[1]))
    polar_cap = top_caption("Bond polarity + shape", cfg.GREEN)
    scene.play(*[a for h in hybrids for a in h.fade(0.0)], *[co2_stage.fade(a, 1.0) for a in co2_arrows],
               h2o_stage.fade(h2o_net, 1.0), fade_through(hybrid_cap, polar_cap), fade_through(counts, verdicts),
               run_time=1.8)
    scene.remove(hybrid_cap, counts)

    # --- 6. A Lewis structure looks flat ---------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    flats = VGroup(Lewis("C", [("O", 180, 2), ("O", 0, 2)], at=[0, 0.6, 0], bond=1.6, size=80, ligand_size=68),
                   Lewis("O", [("H", 180, 1), ("H", 0, 1)], central_lone=[90, 270], at=[0, -1.5, 0], bond=1.6, size=80,
                         ligand_size=68))
    scene.play(co2_stage.fade(co2_stage, 0.2), h2o_stage.fade(h2o_stage, 0.2), FadeOut(polar_cap), FadeOut(verdicts),
               FadeOut(names), FadeIn(flats), run_time=1.4)
    flat_cap = caption("Flat on paper…", cfg.MUTED)
    scene.play(FadeIn(flat_cap), run_time=0.8)

    # --- 7. ...but molecules live in three dimensions -------------------------------------------------------------------------------------
    beat(scene, t, 6)
    live = caption("…three-dimensional in reality", cfg.CYAN)
    scene.play(FadeOut(flats, scale=0.8), co2_stage.fade(co2_stage, 1.0), h2o_stage.fade(h2o_stage, 1.0),
               *[co2_stage.fade(a, 0.0) for a in co2_arrows], h2o_stage.fade(h2o_net, 0.0),
               co2_stage.glide([-3.6, 0.5, 0]), h2o_stage.glide([3.6, 0.7, 0]), co2_stage.zoom_to(1.2),
               h2o_stage.zoom_to(1.2), fade_through(flat_cap, live), run_time=1.8)
    scene.remove(flat_cap)
    scene.play(co2_stage.set_spin(0.4), h2o_stage.set_spin(-0.35), run_time=1.4)

    # --- 8. And that third dimension changes everything -----------------------------------------------------------------------------------
    beat(scene, t, 7)
    card = title_card("3D CHANGES EVERYTHING", "Shape · fit · attraction · reactivity")
    card.scale(0.72).move_to([0, -2.35, 0])
    scene.play(FadeOut(live), co2_stage.glide([-3.6, 1.8, 0]),
               h2o_stage.glide([3.6, 1.8, 0]), co2_stage.zoom_to(0.86), h2o_stage.zoom_to(0.86),
               co2_stage.set_spin(0.0), h2o_stage.set_spin(0.0),
               *co2_stage.turn(yaw=0.35), *h2o_stage.turn(yaw=-0.35), run_time=1.0)
    scene.play(FadeIn(card, shift=UP * 0.2), run_time=0.6)
    scene.play(Indicate(card.title[0], color=cfg.WHITE, scale_factor=1.03), run_time=1.6)
    scene.play(*h2o.show_lone_pairs(0.8), *co2.fade("domains", 0.6), run_time=2.0)
    scene.play(*co2_stage.turn(pitch=0.65), *h2o_stage.turn(pitch=0.6), run_time=3.0, rate_func=there_and_back)
    scene.play(co2_stage.set_spin(0.0), h2o_stage.set_spin(0.0), run_time=1.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["20"])
