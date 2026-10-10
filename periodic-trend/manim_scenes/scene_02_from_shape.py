"""From Part 3's answer to this film's question: the four blocks assemble,
the symbols fade, and a heat map washes across the outlines.

The table is computed by the same filling model as Part 3. The wave of colour
is the real first-ionization data (main-group elements), so even the teaser
is a measurement, not decoration.
"""

from manim_scenes.common import *

PITCH = 0.62
CENTER = DOWN * 0.55


class Scene02FromShape(Scene):
    def construct(self) -> None:
        play_scene(self)


def _block_start(letter: str) -> np.ndarray:
    """Each block flies in from its own side, as Part 3's blocks were built."""
    return {"s": LEFT * 3.2, "p": RIGHT * 3.2, "d": UP * 2.4, "f": DOWN * 2.0}[letter]


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "02", 'Last time: orbitals → table shape')

    # --- 1. The four blocks assemble into the table ------------------------------------
    table = periodic_table(pitch=PITCH, center=CENTER)
    table.tiles[2].box.set_stroke(cfg.BLUE)
    for letter in "spdf":
        zs = pm.elements_in_block(letter)
        scene.play(LaggedStart(*[FadeIn(table.tiles[z], shift=-_block_start(letter) * 0.4) for z in zs],
                               lag_ratio=0.6 / max(len(zs), 1)), run_time=1.1)

    beat(scene, t, 1)
    # A compact key in the open area above the transition block, clear of tiles.
    letters = VGroup(*[eq_chip(letter, cfg.BLOCK_COLORS[letter], cfg.FONT["label"])
                       for letter in "spdf"]).arrange(RIGHT, buff=0.4).move_to([-0.9, 2.7, 0])
    scene.play(LaggedStart(*[FadeIn(label, shift=DOWN * 0.15) for label in letters], lag_ratio=0.25),
               run_time=2.0)
    shape = caption('Orbitals → blocks → table', cfg.WHITE, cfg.FONT["small"], y=-3.95)
    scene.play(FadeIn(shape, shift=UP * 0.15), run_time=0.8)

    # --- 2. A new question --------------------------------------------------------------
    beat(scene, t, 2)
    head = swap_heading(scene, head, 'Now: predict chemical behaviour')
    scene.play(FadeOut(letters), FadeOut(shape), run_time=0.9)
    scene.play(Indicate(table, color=cfg.GOLD, scale_factor=1.02), run_time=1.4)

    # --- 3. Symbols fade, outlines stay ---------------------------------------------------
    beat(scene, t, 3)
    symbols = [tile.symbol for tile in table.tiles.values()]
    scene.play(*[s.animate.set_opacity(0) for s in symbols], run_time=1.6)

    # --- 4. Behind every tile is an atom --------------------------------------------------
    beat(scene, t, 4)
    sodium = table.tiles[11]
    boxes = VGroup(*[tile.box for tile in table.tiles.values()])
    # Clear the question heading before the +11 atom takes centre stage.
    scene.play(FadeOut(head), boxes.animate.set_opacity(0.25), run_time=0.6)
    head = None
    atom = Atom(1.55, sodium.get_center(), charge="+11", core=0.6, count=360, seed=12, nucleus_radius=0.3)
    scene.add(atom)
    atom.cloud.set_radius(0.05)
    atom.core.set_radius(0.03)
    scene.play(Glide(atom, [0, 0.35, 0]), *atom.resize(1.55, 0.6), run_time=1.4)
    props = VGroup(chip("size", cfg.CYAN), chip('electron removal', cfg.GOLD),
                   chip('electron gain', cfg.GREEN)).arrange(RIGHT, buff=0.45)
    props.move_to([0, -2.55, 0])
    for prop in props:
        scene.play(FadeIn(prop, shift=UP * 0.2), run_time=0.7)
    scene.play(Indicate(props, color=cfg.WHITE, scale_factor=1.04), run_time=1.0)

    # --- 5. Colour every tile by one property ------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(props), FadeOut(atom), run_time=0.8)
    scene.play(boxes.animate.set_opacity(0.95), run_time=0.6)
    main = set(main_group_zs())
    waves = []
    for column in range(1, 19):
        column_tiles = [table.tiles[z] for z in main if pm.position(z)[1] == column]
        if column_tiles:
            waves.append(AnimationGroup(*recolor_tiles(column_tiles, lambda z: heat_color("ionization", z), fill=0.85)))
    others = [table.tiles[z] for z in table.tiles if z not in main]
    scene.play(LaggedStart(*waves, lag_ratio=0.18), *[tile.box.animate.set_stroke(cfg.MUTED, opacity=0.35)
                                                     .set_fill(cfg.PANEL, 0.6) for tile in others], run_time=2.6)
    legend = heat_legend("low", "high", width=3.6).move_to([3.6, 2.85, 0])
    what = txt("energy to remove an electron", cfg.FONT["tiny"], cfg.MUTED).next_to(legend.bar, DOWN, buff=0.3)
    scene.play(FadeIn(legend), FadeIn(what), run_time=0.8)

    # --- 6. You could memorise arrows ... ----------------------------------------------------
    beat(scene, t, 6)
    corner = table.tiles[2].get_center()
    sweep = glow_arrow(table.tiles[55].get_center() + DOWN * 0.1, corner + LEFT * 0.4 + DOWN * 0.2, cfg.TREND_ARROW, 7)
    scene.play(GrowArrow(sweep.arrow), FadeIn(sweep[0]), run_time=1.2)
    memo = chip("memorise the arrow?", cfg.MUTED, cfg.FONT["small"]).move_to([-3.6, 2.85, 0])
    scene.play(FadeIn(memo, shift=DOWN * 0.15), run_time=0.7)

    # --- 7. ... or understand them -------------------------------------------------------
    beat(scene, t, 7)
    no = cross_mark(0.36).move_to(memo.get_right() + RIGHT * 0.45)
    scene.play(Create(no), run_time=0.6)
    scene.play(FadeOut(sweep, shift=UP * 0.2), FadeOut(VGroup(memo, no)), run_time=0.8)
    better = chip('Three ideas explain the patterns', cfg.GOLD, cfg.FONT["small"]).move_to([-3.75, 2.85, 0])
    fit_width(better, 6.6)
    scene.play(FadeIn(better, shift=DOWN * 0.15), run_time=0.8)

    # --- 8. Three questions -------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(better), FadeOut(legend), FadeOut(what), boxes.animate.set_opacity(0.12), run_time=0.8)
    questions = VGroup(
        chip('1   Distance', cfg.CYAN, cfg.FONT["body"]),
        chip('2   Nuclear attraction', cfg.GOLD, cfg.FONT["body"]),
        chip('3   Electron arrangement', cfg.GREEN, cfg.FONT["body"]),
    ).arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to(DOWN * 0.3)
    fit_width(questions, 13.0)
    for question in questions:
        scene.play(FadeIn(question, shift=RIGHT * 0.3), run_time=0.8)
        scene.wait(1.6)

    # --- 9. Almost every trend comes from them --------------------------------------------------
    beat(scene, t, 9)
    scene.play(LaggedStart(*[Indicate(q, color=cfg.WHITE, scale_factor=1.04) for q in questions], lag_ratio=0.3),
               run_time=2.0)
    frame = glow_frame(questions, cfg.GOLD, buff=0.2)
    scene.play(Create(frame), run_time=1.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["02"])
