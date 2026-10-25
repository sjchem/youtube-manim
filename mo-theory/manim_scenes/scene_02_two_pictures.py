"""Chapter 02 — two pictures of one bond: valence bond and molecular orbital.

Hydrogen first as two separate 1s orbitals, each with its electron. In the
valence bond picture the overlap holds a localised pair between the nuclei.
In the molecular orbital picture each electron's state spreads over the whole
molecule: the density fog is sampled from |psi|^2 of the computed sigma 1s
orbital. A six-atom row (Huckel coefficients) shows one molecular orbital
stretching across many atoms.
"""

from manim_scenes.common import *

STAGE_AT = np.array([0, 0.1, 0])


class Scene02TwoPictures(Scene):
    def construct(self) -> None:
        play_scene(self)


def series_path(active: int) -> VGroup:
    names = ["Atomic orbitals", "Chemical bonding", "Molecular geometry", "Molecular orbitals"]
    chips = VGroup(*[chip(n, cfg.GOLD if i == active else cfg.MUTED, cfg.FONT["label"]) for i, n in enumerate(names)])
    for i, c in enumerate(chips):
        c.move_to([(-1) ** (i + 1) * 3.4, 0.9 - 1.5 * (i // 2), 0])
    arrows = VGroup(*[Arrow(chips[i].get_right() if i % 2 == 0 else chips[i].get_bottom(),
                            chips[i + 1].get_left() if i % 2 == 0 else chips[i + 1].get_top(),
                            buff=0.12, color=cfg.MUTED, stroke_width=5, tip_length=0.22) for i in range(len(chips) - 1)])
    return VGroup(chips, arrows)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "02", "Two pictures of a bond")

    # --- 1. In this series: shared pairs, overlapping orbitals ------------------------------------------------------
    path = series_path(2).move_to([0, 1.2, 0])
    lewis = VGroup(txt("H", 150), Line(LEFT * 0.75, RIGHT * 0.75, stroke_color=cfg.WHITE, stroke_width=10),
                   txt("H", 150)).arrange(RIGHT, buff=0.3).move_to([0, -1.4, 0])
    scene.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in path[0]], lag_ratio=0.2), Create(path[1]),
               run_time=2.0)
    dismiss_opening_title(scene, t, head, at=3.2)
    scene.play(Write(lewis), run_time=1.4)
    scene.play(Indicate(lewis[1], color=cfg.CYAN, scale_factor=1.2), run_time=1.0)

    # --- 2. Hydrogen: two atoms, one electron each -------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(FadeOut(path), FadeOut(lewis), run_time=0.8)
    stage = Stage(STAGE_AT, zoom=1.15, yaw=0.0, pitch=0.2, sway=0.25)
    cloud = MOCloud(stage, om.MOSpec("s", 1.0, 5.2), opacity=0.55)
    stage_nuclei(stage, cloud)
    state = {"pair": 0.0}

    def electron_spot(side: int):
        def where():
            home = np.array([side * cloud.spec.R / 2 * cloud.units, 0.0, 0.0])
            return home * (1 - state["pair"]) + np.array([0.0, 0.0, 0.0]) * state["pair"]
        return where

    # Fluorescent pink stays distinct from the blue orbital density.
    arrows = []
    for side, spin in ((-1, 1), (1, -1)):
        tag = Tag(spin_arrow(spin, "#FF4DDB", 0.84), electron_spot(side),
                  offset=np.array([0.34 * spin, 0.0, 0.0]))
        stage.add_overlay(tag)
        arrows.append(tag)
    # Leave room below the full cloud silhouette throughout the gentle sway.
    names = [Tag(txt("H", cfg.FONT["body"], cfg.WHITE), lambda s=s: np.array([s * cloud.spec.R / 2 * cloud.units, 0, 0]),
                 offset=np.array([0, -2.35, 0])) for s in (-1, 1)]
    stage.add_overlay(*names)
    show(scene, stage, 1.4)
    one_s = caption("Each atom: one electron in a round 1s orbital", cfg.CYAN)
    scene.play(FadeIn(one_s), run_time=0.8)

    # --- 3. Overlap: a pair settles between the nuclei -----------------------------------------------------------------
    beat(scene, t, 2)
    pairing = Param(stage, lambda: state["pair"], lambda v: state.__setitem__("pair", v), 1.0)
    scene.play(cloud.morph(R=1.6), *[stage.fade(n, 0.0) for n in names], run_time=3.5, rate_func=smooth)
    scene.play(pairing, run_time=2.0, rate_func=smooth)
    pair_glow = Tag(halo(0.7, cfg.GOLD, layers=6, peak_opacity=0.18), np.zeros(3))
    pair_glow.presence = 0.0
    stage.add_overlay(pair_glow)
    scene.play(stage.fade(pair_glow, 1.0), run_time=0.8)

    # --- 4. Valence bond: a handshake between neighbours ------------------------------------------------------------------
    beat(scene, t, 3)
    vb = result_label("Valence bond: a localised pair", cfg.GOLD, cfg.FONT["section"]).move_to([0, 2.75, 0])
    scene.play(FadeOut(one_s), FadeIn(vb, shift=DOWN * 0.2), run_time=1.0)
    hand = caption("Each bond belongs to two particular atoms", cfg.WHITE)
    scene.play(FadeIn(hand), run_time=0.8)

    # --- 5. It explains a great deal --------------------------------------------------------------------------------------
    beat(scene, t, 4)
    wins = VGroup(*[VGroup(check_mark(0.22), txt(w, cfg.FONT["small"], cfg.WHITE)).arrange(RIGHT, buff=0.2)
                    for w in ("shapes", "angles", "hybrid orbitals")]).arrange(RIGHT, buff=0.8).move_to([0, -2.6, 0])
    scene.play(FadeOut(hand), LaggedStart(*[FadeIn(w, shift=UP * 0.15) for w in wins], lag_ratio=0.3), run_time=1.8)

    # --- 6. Another way ----------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    other = caption("Another way to see the same molecule", cfg.CYAN)
    scene.play(FadeOut(wins), FadeOut(vb), fade_through(VGroup(), other), stage.fade(pair_glow, 0.0),
               *[stage.fade(a, 0.0) for a in arrows], run_time=1.2)

    # --- 7. Each electron's state across the whole molecule -----------------------------------------------------------------
    beat(scene, t, 6)
    samples = om.density_samples(om.MOSpec("s", 1.0, 1.6), 1000, seed=cfg.SEED)
    samples = samples[np.linalg.norm(samples * cloud.units, axis=1) < 1.8]
    fog = Fog(samples, STAGE_AT * 0, cfg.DENSITY,
              units=cloud.units, radius=0.03, opacity=0.85)
    fog.presence = 0.0
    stage.add_body(fog)
    mo_title = result_label("Molecular orbital: spread over the molecule", cfg.CYAN, cfg.FONT["section"]).move_to([0, 2.75, 0])
    scene.play(stage.fade(fog, 1.0), *cloud.fade(0.25), fade_through(other, mo_title), run_time=2.0)
    scene.remove(other)
    scene.play(*stage.turn(yaw=0.9, pitch=0.45), run_time=4.0, rate_func=smooth)

    # --- 8. Atomic orbitals in atoms; molecular orbitals in molecules ------------------------------------------------------------
    beat(scene, t, 7)
    rows = VGroup(
        VGroup(txt("atom", cfg.FONT["body"], cfg.MUTED), Arrow(LEFT, RIGHT, color=cfg.MUTED, stroke_width=5),
               txt("atomic orbitals", cfg.FONT["body"], cfg.WHITE)).arrange(RIGHT, buff=0.35),
        VGroup(txt("molecule", cfg.FONT["body"], cfg.CYAN), Arrow(LEFT, RIGHT, color=cfg.CYAN, stroke_width=5),
               txt("molecular orbitals", cfg.FONT["body"], cfg.CYAN)).arrange(RIGHT, buff=0.35),
    ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([0, -2.75, 0])
    scene.play(stage.glide([0, 0.25, 0]), stage.zoom_to(0.9), run_time=1.0)
    scene.play(FadeIn(rows[0], shift=UP * 0.15), run_time=1.0)
    scene.play(FadeIn(rows[1], shift=UP * 0.15), run_time=1.0)
    scene.play(*stage.turn(yaw=0.2, pitch=0.2), run_time=2.4, rate_func=smooth)

    # --- 9. A longer molecule: one orbital across many atoms ----------------------------------------------------------------------
    beat(scene, t, 8)
    _, vectors = pm.huckel_chain(6)
    spacing = 2.6
    chain = PhaseMap(lambda X, Y: om.chain_section(vectors[:, 0], spacing, X, Y), extent=(9.5, 2.6), width=13.0,
                     mode="phase")
    chain.move_to([0, 0.15, 0])
    dots = VGroup(*[nucleus_dot(chain.to_screen((i - 2.5) * spacing, 0)) for i in range(6)])
    across = caption("One molecular orbital, six atoms", cfg.CYAN)
    scene.play(FadeOut(rows), FadeOut(mo_title), stage.fade(stage, 0.0), run_time=1.0)
    scene.remove(stage)
    scene.play(FadeIn(chain), FadeIn(dots), FadeIn(across), run_time=1.6)
    sweep = Line(chain.to_screen(-8.5, -2.3), chain.to_screen(8.5, -2.3), stroke_color=cfg.GOLD, stroke_width=6)
    scene.play(Create(sweep), run_time=2.0)

    # --- 10. Two models, each good at different questions ----------------------------------------------------------------------------
    beat(scene, t, 9)
    left = VGroup(txt("Valence bond", cfg.FONT["title"], cfg.GOLD),
                  txt("localised pairs", cfg.FONT["body"], cfg.WHITE),
                  txt("shapes, hybrids", cfg.FONT["body"], cfg.MUTED)).arrange(DOWN, buff=0.42)
    right = VGroup(txt("Molecular orbital", cfg.FONT["title"], cfg.CYAN),
                   txt("delocalised states", cfg.FONT["body"], cfg.WHITE),
                   txt("energies, magnetism", cfg.FONT["body"], cfg.MUTED)).arrange(DOWN, buff=0.42)
    left.move_to([-4.0, 0.3, 0])
    right.move_to([4.0, 0.3, 0])
    divider = DashedLine([0, 2.2, 0], [0, -1.6, 0], stroke_color=cfg.MUTED, stroke_width=3)
    both = caption("Two models of the same molecule", cfg.WHITE)
    scene.play(FadeOut(chain), FadeOut(dots), FadeOut(sweep), fade_through(across, both), run_time=1.0)
    scene.remove(across)
    scene.play(FadeIn(left, shift=RIGHT * 0.2), FadeIn(right, shift=LEFT * 0.2), Create(divider), run_time=1.4)

    # --- 11. Molecular orbitals are good at magnetism -----------------------------------------------------------------------------------
    beat(scene, t, 10)
    magnetism = right[2]
    scene.play(magnetism.animate.set_color(cfg.GOLD).scale(1.2), run_time=0.8)
    ring = glow_frame(magnetism, cfg.GOLD, buff=0.1)
    scene.play(Create(ring), run_time=0.8)
    scene.play(right.animate.scale(1.05), left.animate.set_opacity(0.55), run_time=5.0, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["02"])
