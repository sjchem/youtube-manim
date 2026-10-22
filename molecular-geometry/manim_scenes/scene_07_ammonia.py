"""Chapter 07 — one lone pair: ammonia, and the two kinds of geometry.

One model carries the whole chapter. It starts as methane's four regions;
the carbon becomes nitrogen, the top site becomes a lone pair (nitrogen's
lone-pair count comes from its valence electrons in the molecule library),
and the purple lobe is shown and hidden to switch between the electron
geometry and the molecular geometry. Finally the three bonds close from the
ideal 109.5 degrees to ammonia's measured angle, read live from the model.
"""

from manim_scenes.common import *

MODEL_AT = np.array([-2.2, -0.35, 0])
PANEL_X = 4.3


class Scene07Ammonia(Scene):
    def construct(self) -> None:
        play_scene(self)


class RepulsionArrow(Body):
    """A 3D arrow occluded by atoms and regions in front of it."""

    def __init__(self, start, end) -> None:
        super().__init__()
        self.arrow = Vector(start, end, cfg.RED, width=0.06, tip=0.2)
        self.mob = self.arrow.mob

    def place(self, stage: Stage, R: np.ndarray, visibility: float) -> None:
        self.arrow.place(stage, R, visibility)
        points = np.array([self.arrow.start(), self.arrow.end()])
        self.depth_key = float(stage.project(points, R)[2].mean())


def valence_dots(symbol: str, count: int, at) -> VGroup:
    """A Lewis dot symbol: one pair on top, then single dots round the sides."""
    letter = txt(symbol, 110, cfg.WHITE).move_to(at)
    singles = []
    spots = [(0.0, -0.78), (-0.78, 0.0), (0.78, 0.0)]
    pair = dot_pair(np.asarray(at, dtype=float), 90, 0.82, cfg.CYAN, radius=0.1, gap=0.24)
    for dx, dy in spots[:count - 2]:
        singles.append(Circle(radius=0.1, stroke_width=0, fill_color=cfg.CYAN, fill_opacity=1)
                       .move_to(np.asarray(at, dtype=float) + np.array([dx, dy, 0])))
    group = VGroup(letter, pair, *singles)
    group.letter, group.pair, group.singles = letter, pair, VGroup(*singles)
    return group


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "07", "Ammonia: one lone pair")
    nh3 = ml.molecule("NH3")
    lone_site = sorted(nh3.lone_pair_indices())[0]

    # --- 1. Methane's four regions ------------------------------------------------------------------------
    stage = Stage(MODEL_AT, zoom=1.12, yaw=0.5, pitch=0.3, sway=0.12)
    model = MoleculeModel(stage, ml.molecule("CH4"), domains=True)
    name = formula("CH4", cfg.FONT["section"]).move_to([PANEL_X, 2.75, 0])
    show(scene, stage, 1.0, FadeIn(name))
    dismiss_opening_title(scene, t, head)
    scene.play(stage.set_spin(0.3), run_time=1.0)

    # --- 2. Carbon becomes nitrogen: five valence electrons --------------------------------------------------------
    beat(scene, t, 1)
    scene.play(stage.set_spin(0.0), *stage.turn(yaw=0.5), run_time=0.8)
    nitrogen = valence_dots("N", gd.VALENCE_ELECTRONS["N"], [PANEL_X, 0.55, 0])
    new_name = formula("NH3", cfg.FONT["section"]).move_to(name)
    scene.play(*model.swap_center("N"), fade_through(name, new_name), FadeIn(nitrogen), run_time=1.4)
    scene.remove(name)
    three = txt("3 for bonds", cfg.FONT["body"], cfg.CYAN).move_to([PANEL_X, -1.55, 0])
    scene.play(nitrogen.singles.animate.set_color(cfg.CYAN), FadeIn(three), Indicate(nitrogen.singles, scale_factor=1.6),
               run_time=1.4)

    # --- 3. The other two stay home: a lone pair -------------------------------------------------------------------
    beat(scene, t, 2)
    two = txt("2 stay: lone pair", cfg.FONT["body"], cfg.PURPLE).move_to([PANEL_X, -2.35, 0])
    scene.play(nitrogen.pair.animate.set_color(cfg.PURPLE), FadeIn(two), Indicate(nitrogen.pair, scale_factor=1.6),
               run_time=1.2)
    scene.play(*model.to_lone_pair(lone_site), run_time=1.8)

    # --- 4. Still a region: it takes up space and pushes -------------------------------------------------------------
    beat(scene, t, 3)
    pushes = caption("A lone pair still takes up space", cfg.PURPLE)
    scene.play(FadeOut(VGroup(nitrogen, three, two)), FadeIn(pushes), run_time=0.8)
    lobe = model.lobes[lone_site]
    scene.play(model.stretch(lone_site, model.lengths[lone_site]), stage.fade(lobe, 0.45), run_time=0.8)
    scene.play(stage.fade(lobe, 1.0), run_time=0.8)
    scene.play(stage.set_spin(0.35), run_time=1.2)

    # --- 5. Four regions: tetrahedral; AX3E -------------------------------------------------------------------------------
    beat(scene, t, 4)
    code = axe_eq(len(nh3.bonds), len(nh3.lone_pairs), cfg.FONT["section"]).move_to([PANEL_X, 1.8, 0])
    corners = [model._site_point(i) for i in range(4)]
    tetra = faces(stage, corners, ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)))
    regions = txt("4 regions", cfg.FONT["body"], cfg.CYAN).move_to([PANEL_X, 0.95, 0])
    scene.play(FadeOut(pushes), FadeIn(code, shift=UP * 0.1), FadeIn(regions), *[stage.fade(f, 1.0) for f in tetra],
               run_time=1.4)
    egeo = shape_name(nh3.electron_geometry, cfg.CYAN, cfg.FONT["body"]).move_to([PANEL_X, 0.2, 0])
    scene.play(FadeIn(egeo, shift=UP * 0.1), run_time=0.9)

    # --- 6. Shape means: where are the atoms? -------------------------------------------------------------------------------
    beat(scene, t, 5)
    atoms_only = caption("Shape: look only at the atoms", cfg.WHITE)
    scene.play(*[stage.fade(f, 0.0) for f in tetra], FadeIn(atoms_only), stage.set_spin(0.0), run_time=1.0)
    scene.play(*stage.turn(yaw=0.35, pitch=0.18), run_time=1.6)

    # --- 7. Hide the lone pair ----------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(stage.fade(lobe, 0.0), *model.fade("domains", 0.0), run_time=1.6)

    # --- 8. A pyramid with a triangular base -----------------------------------------------------------------------------------
    beat(scene, t, 7)
    pyramid_corners = [lambda: model.origin] + [model._site_point(i) for i in model.bonded()]
    pyramid = faces(stage, pyramid_corners, ((1, 2, 3), (0, 1, 2), (0, 2, 3), (0, 1, 3)), cfg.GREEN, 0.1, 0.55)
    mgeo = shape_name(nh3.shape, size=cfg.FONT["body"]).move_to([PANEL_X, -1.45, 0])
    scene.play(*[stage.fade(f, 1.0) for f in pyramid], FadeOut(atoms_only), run_time=1.2)
    scene.play(FadeIn(mgeo, shift=UP * 0.1), stage.set_spin(0.3), run_time=1.0)

    # --- 9. Electron geometry: every region --------------------------------------------------------------------------------------
    beat(scene, t, 8)
    e_title = txt("electron geometry", cfg.FONT["label"], cfg.MUTED).next_to(egeo, UP, buff=0.2)
    scene.play(FadeOut(regions), run_time=0.4)
    scene.play(*[stage.fade(f, 0.0) for f in pyramid], stage.fade(lobe, 1.0), *model.fade("domains", 1.0),
               FadeIn(e_title), Indicate(egeo, color=cfg.WHITE, scale_factor=1.06), run_time=1.2)
    scene.play(*[stage.fade(f, 1.0) for f in tetra], run_time=1.0)

    # --- 10. Molecular geometry: only the atoms ------------------------------------------------------------------------------------
    beat(scene, t, 9)
    m_title = txt("molecular geometry", cfg.FONT["label"], cfg.MUTED).next_to(mgeo, UP, buff=0.2)
    scene.play(*[stage.fade(f, 0.0) for f in tetra], stage.fade(lobe, 0.0), *model.fade("domains", 0.0),
               *[stage.fade(f, 1.0) for f in pyramid], FadeIn(m_title), Indicate(mgeo, color=cfg.WHITE, scale_factor=1.06),
               run_time=1.6)

    # --- 11. Invisible, yet it decided the shape ------------------------------------------------------------------------------------
    beat(scene, t, 10)
    decided = caption("Invisible in the shape. It decided the shape.", cfg.PURPLE)
    scene.play(stage.fade(lobe, 0.55), FadeIn(decided), run_time=1.2)
    scene.play(stage.fade(lobe, 0.25), run_time=1.6, rate_func=there_and_back)

    # --- 12. Measure the angle: not 109.5 ---------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    bonds = model.bonded()
    arc = model.arc(bonds[1], bonds[2], radius=1.1, live=True, label_gap=0.6, size=cfg.FONT["body"])
    scene.play(*[stage.fade(f, 0.0) for f in pyramid], FadeOut(decided), stage.set_spin(0.0), stage.fade(lobe, 1.0),
               *stage.turn(yaw=0.0, pitch=0.25), run_time=1.6)
    scene.play(stage.fade(arc, 1.0), run_time=0.9)

    # --- 13. About 107: the bonds squeeze together ------------------------------------------------------------------------------------
    beat(scene, t, 12)
    scene.play(*[model.aim(i, nh3.sites[i].direction) for i in bonds], run_time=3.2, rate_func=smooth)
    squeezed = caption("Bonds squeezed slightly closer", cfg.GOLD)
    scene.play(FadeIn(squeezed), run_time=0.8)

    # --- 14. Held by one nucleus, the lone pair spreads and crowds ---------------------------------------------------------------------
    beat(scene, t, 13)
    scene.play(*model.fade("domains", 0.8), FadeOut(squeezed), run_time=1.2)
    held = caption("One nucleus holds it: it spreads wide", cfg.PURPLE)
    shoves = [RepulsionArrow(model._site_point(lone_site, 0.8), model._site_point(i, 0.72))
              for i in bonds]
    # These arrows belong to the molecule's depth-sorted world, so the
    # rear arrow passes behind nitrogen instead of covering its symbol.
    for s in shoves:
        s.presence = 0.0
        stage.add_body(s)
    scene.play(FadeIn(held), *[stage.fade(s, 0.85) for s in shoves], run_time=1.2)
    scene.play(*stage.turn(yaw=0.6), run_time=3.0, rate_func=there_and_back)
    scene.play(*[stage.fade(s, 0.0) for s in shoves], run_time=1.4)
    scene.play(stage.set_spin(0.25), run_time=1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["07"])
