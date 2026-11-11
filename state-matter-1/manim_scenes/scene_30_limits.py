"""Scene 30 — where the ideal gas ends. The story's chain (molecules move,
collisions, pressure, gas laws, PV = nRT) is laid out. Then its hidden
simplifications, each shown: a molecule about to hit the wall is tugged back
by its neighbours and strikes softer (attraction); a box of molecules with
real size gets crowded when squeezed (volume); and the film's own gas has a
spread of speeds, the Maxwell-Boltzmann distribution (histogram of the
sample with the curve from ``physics_models.maxwell_pdf``). Part 2 teaser.
"""

from manim_scenes.common import *

SAMPLE = pm.IdealGas(4000, cfg.SEED + 30)
SPEEDS = np.linalg.norm(SAMPLE.u, axis=1)


def packing_fractions() -> np.ndarray:
    """Ordered packing schematic, rather than a hard-sphere fluid simulation."""
    return np.array(np.meshgrid([0.2, 0.5, 0.8], [0.18, 0.5, 0.82],
                                [0.18, 0.5, 0.82], indexing="ij")).reshape(3, -1).T


class Scene30Limits(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "30", "Where the ideal gas ends")
    box = GasBox((0.0, -0.5, 0), count=120, seed=cfg.SEED + 300, half_x=1.8, half_z=1.3, height=3.2, floor=-1.6, zoom=1.15,
                 yaw=-0.5, pitch=0.3, speed=1.6)
    show(scene, box.stage, 1.2)

    # --- 2. The chain: collisions -> pressure -> laws -> one equation ---------------------------------------------------------
    beat(scene, t, 1)
    links = ["moving molecules", "collisions", "pressure", "gas laws", "PV = nRT"]
    colors = [cfg.MOLECULE, cfg.IMPULSE, cfg.PRESSURE, cfg.VOLUME, cfg.GOLD]
    chips = VGroup(*[chip(name, color, cfg.FONT["small"]) for name, color in zip(links, colors)]).arrange(RIGHT, buff=0.45)
    fit_width(chips, 14.2)
    chips.move_to([0, 3.2, 0])
    arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, stroke_color=cfg.MUTED, stroke_width=4,
                            max_tip_length_to_length_ratio=0.35) for a, b in zip(chips[:-1], chips[1:])])
    scene.play(box.stage.glide([0, -0.9, 0]), box.stage.zoom_to(1.0), run_time=1.0)
    for k, c in enumerate(chips):
        anims = [FadeIn(c, shift=RIGHT * 0.2)]
        if k:
            anims.append(GrowArrow(arrows[k - 1]))
        scene.play(*anims, run_time=1.0)
    scene.wait(3.0)

    # --- 3. A hidden simplification: points, no attractions -------------------------------------------------------------------------
    beat(scene, t, 2)
    hidden = VGroup(chip("points", cfg.LIMIT), chip("no attractions", cfg.LIMIT)).arrange(RIGHT, buff=0.5).move_to([0, -2.9, 0])
    scene.play(LaggedStart(*[FadeIn(h, shift=UP * 0.2) for h in hidden], lag_ratio=0.4), run_time=1.4)
    scene.play(Indicate(hidden, color=cfg.WHITE, scale_factor=1.05), run_time=1.2)

    # --- 4. Real molecules attract: tugged back near the wall, a softer hit -----------------------------------------------------------
    beat(scene, t, 3)
    hide(scene, box.stage, 0.8, FadeOut(hidden), FadeOut(VGroup(chips, arrows)))
    wall = Rectangle(width=0.45, height=4.6, stroke_color=cfg.IMPULSE, stroke_width=3, fill_color=cfg.IMPULSE, fill_opacity=0.25).move_to([3.2, -0.6, 0])
    mover = bead([1.6, -0.6, 0], cfg.FOLLOWED, 0.22, glow=1.0)
    rng = np.random.default_rng(cfg.SEED + 31)
    neighbours = VGroup(*[bead([x, y, 0], cfg.MOLECULE, 0.2) for x, y in zip(rng.uniform(-3.2, 0.2, 7), rng.uniform(-2.4, 1.2, 7))])
    tugs = VGroup(*[VecArrow(lambda: mover.get_center(), lambda n=n: mover.get_center() + 0.85 * mu.unit(n.get_center() - mover.get_center()),
                             cfg.ATTRACT, width=0.05, tip_len=0.16) for n in neighbours[:4]])
    ideal_push = VecArrow([3.45, -0.6, 0], [5.4, -0.6, 0], cfg.IMPULSE, width=0.12, live=False)
    real_push = VecArrow([3.45, -0.6, 0], [4.6, -0.6, 0], cfg.IMPULSE, width=0.12, live=False)
    words = VGroup(txt("neighbours tug it back", cfg.FONT["label"], cfg.ATTRACT), txt("a softer hit", cfg.FONT["label"], cfg.IMPULSE))
    words.arrange(DOWN, buff=0.2).move_to([4.4, 2.3, 0])
    scene.play(FadeIn(wall), FadeIn(neighbours), FadeIn(mover), run_time=1.0)
    scene.play(FadeIn(tugs), FadeIn(words[0]), run_time=1.0)
    scene.play(mover.animate.move_to([2.75, -0.6, 0]), run_time=1.4)
    scene.play(FadeIn(ideal_push.set_opacity(0.35)), run_time=0.6)
    scene.play(FadeOut(ideal_push), FadeOut(tugs), FadeIn(real_push), FadeIn(words[1]), run_time=1.0)

    # --- 5. Real molecules take up space: squeezed hard, crowded ---------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(VGroup(wall, mover, neighbours, real_push, words)), run_time=0.8)
    # Fixed sites isolate the excluded-space geometry: no overlapping spheres
    # or claim that a point-particle simulation includes hard-core collisions.
    crowd = GasBox((-3.0, -0.7, 0), count=27, seed=cfg.SEED + 301, half_x=1.4, half_z=1.1, height=4.0, floor=-2.0, lid="piston",
                   radius=0.28, zoom=0.9, yaw=-0.5, pitch=0.3, speed=1.2)
    crowd.gas.phase[:] = packing_fractions()
    crowd.gas.u[:] = 0
    show(scene, crowd.stage, 0.8)
    space = txt("finite-size schematic", cfg.FONT["label"], cfg.WHITE).move_to([3.4, 1.8, 0])
    scene.play(FadeIn(space), crowd.volume_to(0.5, run_time=4.0), run_time=4.0)
    crowded = txt("no longer negligible", cfg.FONT["label"], cfg.WARNING).next_to(space, DOWN, buff=0.35)
    scene.play(FadeIn(crowded), run_time=0.8)

    # --- 6. Not one speed: the Maxwell-Boltzmann distribution -------------------------------------------------------------------------
    beat(scene, t, 5)
    hide(scene, crowd.stage, 0.8, FadeOut(VGroup(space, crowded)))
    axes = plot_axes((0, 3.0), (0, 1.0), x_length=8.4, y_length=3.6, at=[0.0, 0.0, 0], x_label=r"\text{speed}", y_label="",
                     x_color=cfg.VELOCITY)
    edges = np.linspace(0, 3.0, 25)
    counts, _ = np.histogram(SPEEDS, bins=edges)
    density = counts / (len(SPEEDS) * (edges[1] - edges[0]))
    bars = VGroup(*[Polygon(axes.c2p(a, 0), axes.c2p(b, 0), axes.c2p(b, d), axes.c2p(a, d), stroke_color=cfg.CYAN, stroke_width=1.5,
                            fill_color=cfg.MOLECULE, fill_opacity=0.45) for a, b, d in zip(edges[:-1], edges[1:], density)])
    curve = curve_on(axes, lambda s: float(pm.maxwell_pdf(s)), 0.0, 3.0, cfg.GOLD)
    name = result_label("Maxwell–Boltzmann", cfg.GOLD, cfg.FONT["section"]).move_to([3.4, 1.4, 0])
    scene.play(Create(axes), run_time=0.8)
    scene.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), run_time=2.0)
    scene.play(Create(curve), FadeIn(name, scale=0.95), run_time=1.6)

    # --- 7. When the assumptions fail: real gases, Part 2 ------------------------------------------------------------------------------
    beat(scene, t, 6)
    teaser = VGroup(txt("Part 2", cfg.FONT["section"], cfg.GOLD), txt("real gases", cfg.FONT["section"], cfg.WHITE)).arrange(RIGHT, buff=0.4)
    topics = txt("speed distributions · van der Waals · liquefaction", cfg.FONT["small"], cfg.MUTED)
    fit_width(topics, 11.0)
    card = VGroup(teaser, topics).arrange(DOWN, buff=0.3).move_to([0, -2.6, 0])
    scene.play(FadeOut(name), FadeIn(card, shift=UP * 0.2), run_time=1.4)
    finish(scene, t, fill=lambda s: [curve.animate.set_stroke(opacity=0.6)])
