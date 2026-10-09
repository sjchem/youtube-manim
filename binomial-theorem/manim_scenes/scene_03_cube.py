"""Chapter 3 — the cube of a + b, in real 3D.

A cube of edge a + b is cut along all three directions into eight blocks.
Each block is named by the choice each direction made (a or b), so the block
for the choice list ``aab`` is a by a by b. Sorting the eight blocks by shape
gives 1, 3, 3, 1; three small choice machines (one per direction) then show
that "three slabs" means "three ways to choose which direction gets the b".
"""

from itertools import product as cartesian

from manim_scenes.common import *

A, B = 2.0, 1.1
SIDE = A + B
WORDS = ["".join(p) for p in cartesian("ab", repeat=3)]       # x, y, z choices
EXPLODE = 0.5
OBLIQUE = {"phi": 62 * DEGREES, "theta": -52 * DEGREES}
FRONT = {"phi": 72 * DEGREES, "theta": -90 * DEGREES}
LEGEND_X = -5.7
SORT_SCALE = 0.6
DETAIL_SCALE = 0.82  # Leave room for the fixed equations around the rotating blocks.


class Scene03Cube(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _dims(word: str) -> np.ndarray:
    return np.array([A if c == "a" else B for c in word])


def _home(word: str) -> np.ndarray:
    """Where a block sits inside the assembled cube (cube centred on the origin)."""
    low = np.array([0.0 if c == "a" else A for c in word])
    return low + _dims(word) / 2 - SIDE / 2


def _exploded(word: str) -> np.ndarray:
    push = np.array([-1.0 if c == "a" else 1.0 for c in word])
    return _home(word) + push * EXPLODE


def _sorted_spots() -> dict[str, np.ndarray]:
    """A front-facing line-up: groups of 1, 3, 3, 1, all standing on one floor."""
    xs = {0: [-5.2], 1: [-3.1, -1.7, -0.3], 2: [1.3, 2.7, 4.1], 3: [5.6]}
    used = {k: 0 for k in xs}
    spots = {}
    for word in WORDS:
        k = word.count("b")
        x = xs[k][used[k]]
        used[k] += 1
        dz = _dims(word)[2] * SORT_SCALE
        spots[word] = np.array([x, 0.0, -0.4 + dz / 2])
    return spots


def _focus(blocks: dict, chosen) -> list[Animation]:
    chosen = set(chosen)
    return [blk.animate.set_fill(opacity=0.95 if w in chosen else 0.12).set_stroke(opacity=1 if w in chosen else 0.15)
            for w, blk in blocks.items()]


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "03", "The cube of a + b")

    # --- One cube, seen from above, then tilted ----------------------------
    whole = block([SIDE] * 3, cfg.CYAN, 0.35)
    edge = colored_tex([(r"\text{edge} =", "muted"), ("a", "a"), ("+", "op"), ("b", "b")], cfg.FONT["body"])
    edge.move_to(DOWN * 3.55)
    hud(scene, edge)
    scene.play(FadeIn(whole), FadeIn(edge, shift=UP * 0.2), run_time=1.0)
    scene.move_camera(**OBLIQUE, run_time=2.4)

    # --- Cut every edge into a and b -----------------------------------------
    beat(scene, t, 1)
    cut = A - SIDE / 2
    planes = VGroup(
        Square(SIDE).rotate(PI / 2, axis=UP).move_to([cut, 0, 0]),
        Square(SIDE).rotate(PI / 2, axis=RIGHT).move_to([0, cut, 0]),
        Square(SIDE).move_to([0, 0, cut]),
    )
    planes.set_fill(cfg.GOLD, 0.22).set_stroke(cfg.GOLD, 3, 0.9)
    split = colored_tex([(r"\text{edge} =", "muted"), ("a", "a"), ("+", "op"), ("b", "b"),
                         (r"\quad\Rightarrow\quad 2\times2\times2 = 8 \text{ blocks}", "op")], cfg.FONT["body"])
    split.move_to(edge)
    hud(scene, split)
    scene.play(LaggedStart(*[FadeIn(p) for p in planes], lag_ratio=0.5), run_time=2.0)
    blocks = {w: block(_dims(w), mix_color(w.count("b"), 3), 0.9).move_to(_home(w)) for w in WORDS}
    scene.play(FadeOut(whole), FadeOut(planes), FadeIn(VGroup(*blocks.values())),
               ReplacementTransform(edge, split), run_time=1.6)

    # --- Pull them apart ------------------------------------------------------
    beat(scene, t, 2)
    scene.play(*[blk.animate.move_to(_exploded(w)) for w, blk in blocks.items()], FadeOut(split), run_time=2.2)
    scene.begin_ambient_camera_rotation(rate=0.07)

    # --- Name each shape ---------------------------------------------------------
    legend = {}
    for k, y in zip(range(4), (1.9, 0.7, -0.5, -1.7)):
        term = term_tex(1, 3 - k, k, cfg.FONT["section"])
        term.move_to([LEGEND_X, y, 0])
        legend[k] = term
        hud(scene, term)
    counts = {}
    for k in range(4):
        tally = txt(f"× {mu.coefficients(3)[k]}", cfg.FONT["body"], cfg.GOLD)
        tally.next_to(legend[k], RIGHT, buff=0.35)
        counts[k] = tally
        hud(scene, tally)

    for index, k in ((3, 0), (4, 3), (5, 1), (6, 2)):
        beat(scene, t, index)
        members = [w for w in WORDS if w.count("b") == k]
        scene.play(*_focus(blocks, members), FadeIn(legend[k], shift=RIGHT * 0.2), run_time=1.0)
        if len(members) > 1:
            for w in members:
                scene.play(Indicate(blocks[w], color=cfg.WHITE, scale_factor=1.12), run_time=0.9)
        scene.play(FadeIn(counts[k], scale=1.3), run_time=0.7)

    # --- Sort the eight blocks by shape --------------------------------------------
    beat(scene, t, 7)
    scene.stop_ambient_camera_rotation()
    spots = _sorted_spots()
    scene.play(*_focus(blocks, WORDS), FadeOut(VGroup(*legend.values(), *counts.values())), run_time=0.6)
    scene.move_camera(**FRONT, added_anims=[blk.animate.scale(SORT_SCALE).move_to(spots[w])
                                            for w, blk in blocks.items()], run_time=2.4)
    group_x = {0: -5.2, 1: -1.7, 2: 2.7, 3: 5.6}
    labels, tallies = VGroup(), VGroup()
    for k in range(4):
        label = term_tex(1, 3 - k, k, cfg.FONT["section"]).move_to([group_x[k], -1.55, 0])
        tally = txt(str(mu.coefficients(3)[k]), cfg.FONT["title"], cfg.GOLD).move_to([group_x[k], -2.5, 0])
        labels.add(label)
        tallies.add(tally)
    hud(scene, *labels, *tallies)
    scene.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in labels], lag_ratio=0.2), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(m, scale=1.4) for m in tallies], lag_ratio=0.3), run_time=1.2)

    # --- (a+b)^3 ----------------------------------------------------------------------
    beat(scene, t, 8)
    eq3 = expansion_tex(3, cfg.FONT["body"]).move_to(DOWN * 3.6)
    hud(scene, eq3)
    # Fade, never morph, into fixed-in-frame text: a transform in a 3D chapter
    # would leave unregistered glyph copies floating in world space.
    scene.play(Indicate(tallies, color=cfg.WHITE, scale_factor=1.15), run_time=0.8)
    scene.play(FadeIn(eq3.lhs), LaggedStart(*[FadeIn(VGroup(term, *([eq3.pluses[k - 1]] if k else [])), shift=DOWN * 0.3)
                                              for k, term in enumerate(eq3.terms)], lag_ratio=0.3), run_time=1.6)
    scene.play(Circumscribe(eq3, color=cfg.GOLD, buff=0.12), run_time=1.4)

    # --- Why three? One machine per direction ----------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(labels), FadeOut(tallies), run_time=0.6)
    scene.move_camera(**OBLIQUE, added_anims=[blk.animate.scale(DETAIL_SCALE / SORT_SCALE).move_to(_exploded(w) * DETAIL_SCALE)
                                              for w, blk in blocks.items()], run_time=2.4)
    machines = VGroup(*[ChoiceMachine(i + 1, 1.9, 1.1, 0.34) for i in range(3)])
    machines.arrange(DOWN, buff=0.35).move_to([5.55, 0.15, 0])
    axes = VGroup(*[txt(name, cfg.FONT["label"], cfg.MUTED).next_to(m, LEFT, buff=0.25)
                    for name, m in zip(("x", "y", "z"), machines)])
    hud(scene, machines, axes)
    scene.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.3) for m in machines], lag_ratio=0.2), FadeIn(axes),
               run_time=1.2)
    slabs = [w for w in WORDS if w.count("b") == 1]
    beams = [w for w in WORDS if w.count("b") == 2]
    scene.play(*_focus(blocks, slabs), run_time=0.8)

    beat(scene, t, 10)
    for w in slabs:
        scene.play(*_focus(blocks, [w]), *[m.animate.choose(c) for m, c in zip(machines, w)], run_time=0.8)
        scene.play(Indicate(blocks[w], color=cfg.WHITE, scale_factor=1.1), run_time=0.8)

    beat(scene, t, 11)
    for w in beams:
        scene.play(*_focus(blocks, [w]), *[m.animate.choose(c) for m, c in zip(machines, w)], run_time=0.8)
        scene.play(Indicate(blocks[w], color=cfg.WHITE, scale_factor=1.1), run_time=0.8)

    # --- Eight blocks: 2 x 2 x 2 ---------------------------------------------------------
    beat(scene, t, 12)
    eight = colored_tex([(r"2\times2\times2", "coef"), ("=", "op"), ("8", "coef")], cfg.FONT["body"])
    eight.next_to(machines, DOWN, buff=0.4)
    hud(scene, eight)
    scene.play(FadeIn(eight, shift=UP * 0.2), run_time=0.7)
    for w in WORDS:
        scene.play(*_focus(blocks, [w]), *[m.animate.choose(c) for m, c in zip(machines, w)], run_time=0.55)
    scene.play(*_focus(blocks, WORDS), *[m.animate.reset() for m in machines], run_time=0.6)
    scene.begin_ambient_camera_rotation(rate=0.1)

    # --- The fourth power would need a fourth dimension ------------------------------------
    beat(scene, t, 13)
    four = colored_tex(lhs_parts(4, sep=r"\;\to\;") + [(r"\text{4D?}", "muted")], cfg.FONT["section"])
    four.pieces[-1].set_color(cfg.ORANGE)
    four.move_to([-4.4, 2.9, 0])
    hud(scene, four)
    scene.play(FadeIn(four, shift=DOWN * 0.2), run_time=1.0)
    scene.play(Wiggle(four.pieces[-1], scale_value=1.2), run_time=1.2)
    cue(scene, t, 92.5)
    scene.play(*[blk.animate.move_to(_home(w) * DETAIL_SCALE) for w, blk in blocks.items()], FadeOut(eight), run_time=2.0)
    cue(scene, t, 96.0)
    better = machine_row(4, width=2.3, height=1.4, door=0.42, y=-0.2)
    hud(scene, better)
    scene.stop_ambient_camera_rotation()
    scene.play(FadeOut(VGroup(*blocks.values())), FadeOut(machines), FadeOut(axes),
               LaggedStart(*[FadeIn(m, shift=UP * 0.3) for m in better], lag_ratio=0.2), run_time=1.6)
    scene.play(*[m.animate.choose(c) for m, c in zip(better, "abba")], run_time=0.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["03"])
