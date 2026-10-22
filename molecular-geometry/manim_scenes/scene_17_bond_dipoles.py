"""Chapter 17 — bond dipoles are vectors, and shape decides how they add.

Arrows point toward the atom that pulls the shared electrons harder (the
common chemistry convention; physicists draw the dipole moment the other
way, from minus to plus). Arrow length is proportional to the
electronegativity difference (``physics_models.bond_dipoles``) — an
illustration of direction and symmetry, not a dipole calculation. The
tip-to-tail sums are computed with ``physics_models.tip_to_tail``.
"""

from manim_scenes.common import *

ARROW_SCALE = 1.6       # screen units per unit of electronegativity difference


class Scene17BondDipoles(Scene):
    def construct(self) -> None:
        play_scene(self)


def dipole_vectors(mol: ml.Molecule, model: MoleculeModel) -> list[np.ndarray]:
    ligands = [(s.symbol, model.dirs[i]) for i, s in enumerate(mol.sites) if s.kind == "X"]
    return [v * ARROW_SCALE for v in pm.bond_dipoles(mol.central, ligands, gd.ELECTRONEGATIVITY)]


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "17", "Bond dipoles")
    shape_matters = caption("Bond polarity + shape → molecular polarity", cfg.WHITE)
    scene.play(FadeIn(shape_matters), run_time=0.9)
    dismiss_opening_title(scene, t, head)

    # --- 2. Hydrogen chloride: chlorine pulls harder ------------------------------------------------------------------
    beat(scene, t, 1)
    hcl = ml.diatomic("HCl")
    scale = 2.6 / float(np.ptp(hcl["positions"][:, 0]))
    stage = Stage([0, 0.5, 0], zoom=1.4, pitch=0.12, sway=0.08)
    atoms = [element_ball(sym, pos * scale, scale=1.15) for sym, pos in zip(hcl["symbols"], hcl["positions"])]
    rod = Rod(atoms[0], atoms[1])
    stage.add_body(rod, *atoms)
    en = VGroup(*[txt(f"{sym}: {gd.ELECTRONEGATIVITY[sym]:.2f}", cfg.FONT["body"],
                      cfg.DELTA_PLUS if gd.ELECTRONEGATIVITY[sym] < 3 else cfg.DELTA_MINUS)
                  for sym in hcl["symbols"]])
    en.arrange(RIGHT, buff=2.4).move_to([0, -1.75, 0])
    en_title = txt("electronegativity", cfg.FONT["label"], cfg.MUTED).next_to(en, DOWN, buff=0.25)
    show(scene, stage, 1.0, FadeOut(shape_matters))
    scene.play(FadeIn(en), FadeIn(en_title), run_time=1.0)

    # --- 3. The cloud leans: delta+ and delta- -------------------------------------------------------------------------------
    beat(scene, t, 2)
    cloud = Lobe(lambda: atoms[0].where() + RIGHT * 0.3, RIGHT, 2.9, 0.62, cfg.CYAN,
                 start=0.0, body_opacity=0.2)
    cloud.presence = 0.0
    stage.add_body(cloud)
    deltas = [Tag(eq(r"\delta^{+}", cfg.FONT["section"], cfg.DELTA_PLUS), atoms[0].where(), UP * 0.95),
              Tag(eq(r"\delta^{-}", cfg.FONT["section"], cfg.DELTA_MINUS), atoms[1].where(), UP * 1.05)]
    for d in deltas:
        d.presence = 0.0
        stage.add_overlay(d)
    scene.play(stage.fade(cloud, 1.0), run_time=1.2)
    scene.play(*[stage.fade(d, 1.0) for d in deltas], run_time=1.0)

    # --- 4. A bond dipole: an arrow toward the stronger pull ------------------------------------------------------------------
    beat(scene, t, 3)
    pull = gd.ELECTRONEGATIVITY["Cl"] - gd.ELECTRONEGATIVITY["H"]
    arrow = Vector(lambda: atoms[0].where() + DOWN * 0.95,
                   lambda: atoms[0].where() + DOWN * 0.95 + RIGHT * max(pull * ARROW_SCALE * 2.2, 1.6),
                   cfg.BOND_DIPOLE, width=0.11, tip=0.34)
    arrow.presence = 0.0
    stage.add_overlay(arrow)
    named = caption("A bond dipole: points to the stronger pull", cfg.BOND_DIPOLE)
    scene.play(stage.fade(arrow, 1.0), FadeOut(en), FadeOut(en_title), FadeIn(named), run_time=1.4)

    # --- 5. Size and direction: a vector, and vectors add -------------------------------------------------------------------------
    beat(scene, t, 4)
    vector = caption("Size + direction = a vector. Vectors add.", cfg.WHITE)
    scene.play(fade_through(named, vector), run_time=0.9)
    scene.remove(named)
    demo = VGroup(Arrow([-3.2, -2.3, 0], [-1.2, -2.3, 0], buff=0, color=cfg.BOND_DIPOLE, stroke_width=8),
                  Arrow([-1.2, -2.3, 0], [0.2, -1.4, 0], buff=0, color=cfg.BOND_DIPOLE, stroke_width=8))
    total = Arrow([-3.2, -2.3, 0], [0.2, -1.4, 0], buff=0, color=cfg.NET_DIPOLE, stroke_width=10)
    scene.play(GrowArrow(demo[0]), run_time=0.7)
    scene.play(GrowArrow(demo[1]), run_time=0.7)
    scene.play(GrowArrow(total), run_time=0.8)

    # --- 6. Carbon dioxide: two arrows outward ---------------------------------------------------------------------------------------
    beat(scene, t, 5)
    hide(scene, stage, 0.8, FadeOut(demo), FadeOut(total), FadeOut(vector))
    co2_spec = ml.molecule("CO2")
    stage = Stage([0, 0.6, 0], zoom=1.05, pitch=0.15, sway=0.1)
    co2 = MoleculeModel(stage, co2_spec)
    vecs = dipole_vectors(co2_spec, co2)
    arrows = [Vector(lambda i=i: co2.point(i, 0.25) + UP * 0.62, lambda i=i: co2.point(i, 0.25) + UP * 0.62 + vecs[i], cfg.BOND_DIPOLE,
                     width=0.1, tip=0.32) for i in range(2)]
    for a in arrows:
        a.presence = 0.0
        stage.add_overlay(a)
    name = formula("CO2", cfg.FONT["section"]).move_to([-5.2, 2.6, 0])
    show(scene, stage, 1.0, FadeIn(name))
    scene.play(*[stage.fade(a, 1.0) for a in arrows], run_time=1.2)

    # --- 7. Tip to tail: they cancel ----------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    # Chain the two arrows head to tail below the molecule (nudged apart vertically
    # so the second, which runs back over the first, stays visible).
    links = pm.tip_to_tail([v * 1.4 for v in vecs], start=np.array([0.0, -2.2, 0.0]))
    chain = VGroup(*[Arrow(a, b, buff=0, color=cfg.BOND_DIPOLE, stroke_width=9) for a, b in links])
    chain[0].shift(UP * 0.14)
    chain[1].shift(DOWN * 0.14)
    scene.play(TransformFromCopy(VGroup(*[a.mob for a in arrows]), chain), run_time=1.6)
    net = pm.vector_sum(vecs)
    zero = VGroup(eq(r"\mu = 0", cfg.FONT["section"], cfg.NET_DIPOLE)).next_to(chain, RIGHT, buff=0.6)
    assert np.linalg.norm(net) < 1e-9
    scene.play(FadeIn(zero, scale=1.2), run_time=0.9)

    # --- 8. Polar bonds, nonpolar molecule -------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    nonpolar = caption("Polar bonds, nonpolar molecule", cfg.GREEN)
    scene.play(FadeIn(nonpolar), stage.set_spin(0.4), run_time=1.2)

    # --- 9. Water: both arrows toward oxygen -------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    hide(scene, stage, 0.8, FadeOut(VGroup(chain, zero, nonpolar, name)))
    water = ml.molecule("H2O")
    stage = Stage([0, 1.0, 0], zoom=1.05, pitch=0.1, sway=0.1)
    h2o = MoleculeModel(stage, water, orient=bisect_down(water.sites[2].direction, water.sites[3].direction), lone_pairs=False)
    wvecs = dipole_vectors(water, h2o)
    # Each arrow runs beside its bond, from the hydrogen end toward oxygen.
    w_arrows = [Vector(lambda i=i: h2o.point(i, 0.82) + _offset(h2o, i),
                       lambda i=i, k=k: h2o.point(i, 0.82) + wvecs[k] + _offset(h2o, i), cfg.BOND_DIPOLE, width=0.1,
                       tip=0.32) for k, i in enumerate(h2o.bonded())]
    for a in w_arrows:
        a.presence = 0.0
        stage.add_overlay(a)
    name = formula("H2O", cfg.FONT["section"]).move_to([-5.2, 2.6, 0])
    show(scene, stage, 1.0, FadeIn(name))
    scene.play(*[stage.fade(a, 1.0) for a in w_arrows], run_time=1.2)

    # --- 10. Bent: tip to tail, they don't cancel ----------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    # Separate the vector construction from the molecule; the old chain
    # crossed the left hydrogen and looked like an extra bond.
    scene.play(stage.glide([-3.4, 0.9, 0]), *stage.turn(yaw=0.0, pitch=0.0), run_time=1.0)
    stage.sway = 0.0
    chain_label = txt("tip to tail", cfg.FONT["body"], cfg.BOND_DIPOLE).move_to([3.6, 2.4, 0])
    scene.play(FadeIn(chain_label), run_time=0.5)
    origin = np.array([3.8, -1.6, 0])
    links = pm.tip_to_tail([v * 1.3 for v in wvecs])
    w_chain = VGroup(*[Arrow(origin + a, origin + b, buff=0, color=cfg.BOND_DIPOLE, stroke_width=9) for a, b in links])
    scene.play(TransformFromCopy(VGroup(*[a.mob for a in w_arrows]), w_chain), run_time=1.6)
    w_net = pm.vector_sum(wvecs)
    total = Arrow(origin, origin + w_net * 1.3, buff=0, color=cfg.NET_DIPOLE, stroke_width=12)
    scene.play(GrowArrow(total), run_time=1.0)

    # --- 11. The sum points to the oxygen side: polar ------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    big = Vector(lambda: h2o.origin + UP * 0.2, lambda: h2o.origin + UP * 0.2 + mu.unit(w_net) * 2.0, cfg.NET_DIPOLE,
                 width=0.16, tip=0.42)
    big.presence = 0.0
    stage.add_overlay(big)
    polar = VGroup(eq(r"\mu \neq 0", cfg.FONT["section"], cfg.NET_DIPOLE), txt("polar", cfg.FONT["section"], cfg.GREEN))
    polar.arrange(RIGHT, buff=0.5).move_to([3.6, -2.6, 0])
    scene.play(stage.fade(big, 1.0), FadeIn(polar), run_time=1.2)

    # --- 12. Same bonds, different results: the shape decided ------------------------------------------------------------------------------------
    beat(scene, t, 11)
    decided = caption("Polar bonds. Different shapes. Different sums.", cfg.GOLD)
    scene.play(FadeIn(decided), run_time=0.9)
    scene.play(Indicate(total, color=cfg.WHITE, scale_factor=1.1), run_time=1.2)
    scene.play(*stage.turn(yaw=0.6), run_time=2.6, rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["17"])


def _offset(model: MoleculeModel, i: int) -> np.ndarray:
    """Draw a bond's arrow beside the bond, not on top of it."""
    d = model.dirs[i]
    side = np.cross(d, OUT)
    return mu.unit(side) * 0.38 if np.linalg.norm(side) > 1e-6 else np.zeros(3)
