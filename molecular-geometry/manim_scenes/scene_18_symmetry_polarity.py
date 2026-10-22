"""Chapter 18 — symmetry decides polarity: bond dipoles summed in 3D.

Each molecule sits on the left; its bond dipoles (``physics_models.bond_dipoles``,
pointing toward the stronger pull, length proportional to the electronegativity
difference) are chained head to tail on a second stage on the right that
turns in step with the molecule, so the chain is seen in three dimensions.
For BF3 and CH4 the chain closes (sum zero, checked numerically); for NH3
it does not, and the net arrow points toward the nitrogen / lone-pair side.
"""

from manim_scenes.common import *

MOL_AT = np.array([-3.4, -0.45, 0])
CHAIN_AT = np.array([3.6, -0.25, 0])
# Screen units per unit of electronegativity difference. C-H dipoles are weak, so
# methane's arrows are drawn larger; the lengths only illustrate direction and symmetry.
SCALE = {"BF3": 1.0, "CH4": 3.0, "NH3": 1.6}


class Scene18SymmetryPolarity(Scene):
    def construct(self) -> None:
        play_scene(self)


class FluorineSafeDipole(Vector):
    """Stop BF3 arrows before any projected fluorine sphere as it turns."""

    def __init__(self, start, end, fluorines) -> None:
        super().__init__(start, end, cfg.BOND_DIPOLE, width=0.1, tip=0.3)
        self.fluorines = fluorines
        self._fluorine_disks = []

    def place(self, stage: Stage, R: np.ndarray, visibility: float) -> None:
        self._fluorine_disks = []
        for atom in self.fluorines:
            screen, size, _ = stage.project(atom.where()[None, :], R)
            self._fluorine_disks.append((screen[0], atom.radius * size[0] + 0.16))
        super().place(stage, R, visibility)

    def _outline(self, p, q, width, tip):
        span = q - p
        length_sq = float(span @ span)
        if length_sq < 1e-8:
            return None
        limit = 1.0
        for centre, radius in self._fluorine_disks:
            delta = centre - p
            along = float(delta @ span) / length_sq
            perpendicular_sq = max(0.0, float(delta @ delta) - along * along * length_sq)
            if perpendicular_sq > radius * radius:
                continue
            half = np.sqrt((radius * radius - perpendicular_sq) / length_sq)
            if along + half >= 0:
                limit = min(limit, max(0.0, along - half))
        return super()._outline(p, p + span * limit, width, tip)


def molecule_with_dipoles(key: str):
    spec = ml.molecule(key)
    stage = Stage(MOL_AT, zoom=0.95, yaw=0.5, pitch=0.35, spin=0.25)
    model = MoleculeModel(stage, spec, lone_pairs=False)
    ligands = [(s.symbol, model.dirs[i]) for i, s in enumerate(spec.sites) if s.kind == "X"]
    vecs = [v * SCALE[key] for v in pm.bond_dipoles(spec.central, ligands, gd.ELECTRONEGATIVITY)]
    arrows = []
    for k, i in enumerate(model.bonded()):
        outward = vecs[k] @ model.dirs[i] > 0
        begin = model.point(i, 0.28 if outward else 0.92)
        if key == "BF3":
            # Keep F readable even when a turning bond becomes foreshortened.
            # The tip-to-tail vector construction keeps its original values.
            arrows.append(FluorineSafeDipole(begin, begin + vecs[k], list(model.atoms.values())))
        else:
            arrows.append(Vector(begin, begin + vecs[k], cfg.BOND_DIPOLE, width=0.1, tip=0.3))
    for a in arrows:
        a.presence = 0.0
        stage.add_overlay(a)
    chain_stage = Stage(CHAIN_AT, zoom=0.95, yaw=0.5, pitch=0.35, spin=0.25)
    # Centre the chain on its stage: start it at minus the mean of its corner points.
    corners = np.array([p for link in pm.tip_to_tail(vecs) for p in link])
    links = pm.tip_to_tail(vecs, start=-corners.mean(axis=0))
    chain = [Vector(a, b, cfg.BOND_DIPOLE, width=0.1, tip=0.3) for a, b in links]
    start_dot = Ball(links[0][0], 0.12, cfg.WHITE)
    start_dot.presence = 0.0
    chain_stage.add_body(start_dot)
    for c in chain:
        c.presence = 0.0
        chain_stage.add_overlay(c)
    for s in (stage, chain_stage):
        s.presence = 0.0
        s.refresh()
    return spec, stage, model, arrows, chain_stage, chain, start_dot, vecs, links


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "18", "Symmetry decides polarity")
    results = {}
    for index, key in ((0, "BF3"), (2, "CH4"), (4, "NH3")):
        if index:
            beat(scene, t, index)
        spec, stage, model, arrows, chain_stage, chain, dot, vecs, links = molecule_with_dipoles(key)
        name = formula(key, cfg.FONT["section"]).move_to([-6.3, 2.85, 0])
        chain_title = txt("tip to tail", cfg.FONT["body"], cfg.BOND_DIPOLE).move_to([CHAIN_AT[0], 2.85, 0])
        scene.add(stage, chain_stage)
        scene.play(stage.fade(stage, 1.0), FadeIn(name), run_time=1.0)
        if index == 0:
            dismiss_opening_title(scene, t, head, at=1.6)
        scene.play(*[stage.fade(a, 1.0) for a in arrows], run_time=1.2)

        # --- chain them head to tail -------------------------------------------------------------------------------
        beat(scene, t, index + 1)
        scene.play(chain_stage.fade(chain_stage, 1.0), chain_stage.fade(dot, 1.0), FadeIn(chain_title), run_time=0.8)
        for c in chain:
            scene.play(chain_stage.fade(c, 1.0), run_time=0.55)
        net = pm.vector_sum(vecs)
        if np.linalg.norm(net) < 1e-9:
            verdict = VGroup(eq(r"\mu = 0", cfg.FONT["section"], cfg.NET_DIPOLE),
                             txt("nonpolar", cfg.FONT["section"], cfg.CYAN)).arrange(RIGHT, buff=0.4)
            verdict.move_to([CHAIN_AT[0], -2.75, 0])
            closes = Halo(dot, cfg.GREEN, reach=4.0, peak=0.35)
            closes.presence = 0.0
            chain_stage.add_body(closes)
            scene.play(chain_stage.fade(closes, 1.0), FadeIn(verdict, shift=UP * 0.1), run_time=1.2)
            results[key] = (stage, chain_stage, name, chain_title, verdict)
            hold = 1.8 if key == "BF3" else 1.1
            scene.play(Indicate(verdict, color=cfg.WHITE, scale_factor=1.05), run_time=hold)
        else:
            total = Vector(links[0][0], links[-1][1], cfg.NET_DIPOLE, width=0.16, tip=0.4)
            total.presence = 0.0
            chain_stage.add_overlay(total)
            scene.play(chain_stage.fade(total, 1.0), run_time=1.2)
            open_note = caption("The bond arrows do not cancel", cfg.WHITE)
            lone = model.lobes[model.lone()[0]]
            scene.play(FadeIn(open_note), stage.fade(lone, 0.6), run_time=1.0)

            # --- the overall dipole points to the nitrogen / lone-pair side -------------------------------------
            beat(scene, t, 6)
            big = Vector(ORIGIN, mu.unit(net) * 2.6, cfg.NET_DIPOLE, width=0.18, tip=0.45)
            big.presence = 0.0
            stage.add_overlay(big)
            verdict = VGroup(eq(r"\mu \neq 0", cfg.FONT["section"], cfg.NET_DIPOLE),
                             txt("polar", cfg.FONT["section"], cfg.GREEN)).arrange(RIGHT, buff=0.4)
            verdict.move_to([CHAIN_AT[0], -2.75, 0])
            scene.play(stage.fade(big, 1.0), FadeOut(open_note), FadeIn(verdict, shift=UP * 0.1), run_time=1.2)
            scene.play(*[s.set_spin(0.0) for s in (stage, chain_stage)], *[x for s in (stage, chain_stage)
                                                                            for x in s.turn(yaw=0.2, pitch=0.15)],
                       run_time=1.6)
            assert net @ model.dirs[model.lone()[0]] > 0, "NH3 net bond dipole should point to the lone-pair side"
            results[key] = (stage, chain_stage, name, chain_title, verdict)
        # clear before the next molecule
        stage_, chain_stage_, name_, chain_title_, verdict_ = results[key]
        if key != "NH3":
            for s in (stage_, chain_stage_):
                s.clear_updaters()
            scene.play(FadeOut(stage_), FadeOut(chain_stage_), FadeOut(VGroup(name_, chain_title_, verdict_)),
                       run_time=0.8)
            scene.remove(stage_, chain_stage_)

    # --- 8. Line them up: symmetric cancel, lopsided add ---------------------------------------------------------------
    beat(scene, t, 7)
    stage_, chain_stage_, name_, chain_title_, verdict_ = results["NH3"]
    for s in (stage_, chain_stage_):
        s.clear_updaters()
    scene.play(FadeOut(stage_), FadeOut(chain_stage_), FadeOut(VGroup(name_, chain_title_, verdict_)), run_time=0.8)
    scene.remove(stage_, chain_stage_)
    # Compare three symmetric molecules, then two polar ones. Five models
    # in one row left too little room for their rotating atom silhouettes.
    def comparison(keys, positions, zoom):
        minis, tags = [], VGroup()
        for key, x in zip(keys, positions):
            small, _ = mini_model(key, [x, 0.65, 0], zoom=zoom, spin=0.0)
            small.sway = 0.22
            minis.append(small)
            polar = gd.DIPOLE_DEBYE[key] > 0
            tag = VGroup(formula(key, cfg.FONT["body"]),
                         txt("polar" if polar else "nonpolar", cfg.FONT["body"],
                             cfg.GREEN if polar else cfg.CYAN)).arrange(DOWN, buff=0.25)
            tags.add(tag.move_to([x, -2.2, 0]))
            scene.add(small)
        return minis, tags

    minis, tags = comparison(("CO2", "BF3", "CH4"), (-4.7, 0, 4.7), 0.76)
    scene.play(*[m.fade(m, 1.0) for m in minis], FadeIn(VGroup(*[tag[0] for tag in tags])), run_time=1.4)
    scene.play(LaggedStart(*[FadeIn(tag[1], shift=UP * 0.1) for tag in tags], lag_ratio=0.3), run_time=1.6)

    # --- 9. Ammonia and water: polar --------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(*[m.fade(m, 0.0) for m in minis], FadeOut(tags), run_time=0.6)
    scene.remove(*minis)
    minis, tags = comparison(("NH3", "H2O"), (-3.7, 3.7), 0.88)
    scene.play(*[m.fade(m, 1.0) for m in minis], FadeIn(tags), run_time=1.2)
    scene.play(*[Indicate(tag[1], color=cfg.WHITE, scale_factor=1.06) for tag in tags], run_time=1.0)

    # --- 10. Shape isn't the only factor -----------------------------------------------------------------------------------------
    beat(scene, t, 9)
    fair = caption("Atoms and bond polarity matter too", cfg.WHITE)
    scene.play(FadeIn(fair), run_time=1.0)

    # --- 11. With identical surrounding atoms, symmetry decides -------------------------------------------------------------------
    beat(scene, t, 10)
    decides = caption("Symmetry can cancel equivalent bond dipoles", cfg.GOLD)
    scene.play(fade_through(fair, decides), run_time=1.0)
    scene.remove(fair)
    from_counting = top_caption("Count regions → find shape → add dipoles", cfg.CYAN)
    scene.play(FadeIn(from_counting), run_time=1.0)
    scene.play(*[m.set_spin(0.08) for m in minis], run_time=2.0)
    scene.play(Indicate(from_counting, color=cfg.WHITE, scale_factor=1.04), run_time=1.4)
    scene.play(*[m.turn(pitch=0.75)[0] for m in minis], run_time=3.0, rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["18"])
