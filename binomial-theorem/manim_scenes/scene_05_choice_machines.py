"""Chapter 5 — five choice machines.

(a+b)^5 is five brackets, and each bracket is a machine that opens exactly one
door. One full set of choices is one choice list and one product (aabab ->
a^3 b^2). There are 2^5 = 32 lists — the 32 products brute force made — and
sorting them by how many b's they contain gives piles of 1, 5, 10, 10, 5, 1.
"""

from manim_scenes.common import *
from utils.render_helpers import grid_positions

N = 5
MACHINE_Y = 2.15
DEMO = "aabab"

BIG_CELL, BAND_CELL, PILE_CELL = 0.42, 0.22, 0.3
BASELINE = -1.95
PILE_STEP = 0.36
LABEL_Y, COUNT_Y, BAND_Y = -2.55, -3.4, 2.6


class Scene05ChoiceMachines(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _pile_x(k: int) -> float:
    return (k - N / 2) * 2.3


def _pile_slot(k: int, j: int) -> np.ndarray:
    return np.array([_pile_x(k), BASELINE + PILE_CELL / 2 + 0.03 + j * PILE_STEP, 0.0])


def _bracket() -> MathTex:
    return colored_tex([("(", "op"), ("a", "a"), ("+", "op"), ("b", "b"), (")", "op")], cfg.FONT["section"])


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "05", "Five choice machines")

    # --- Five brackets ------------------------------------------------------
    machines = machine_row(N, y=MACHINE_Y)
    hero = colored_tex(lhs_parts(N, sep=""), cfg.FONT["hero"]).move_to(DOWN * 0.2)
    scene.play(FadeIn(hero, scale=0.9), run_time=1.0)
    brackets = VGroup(*[_bracket().move_to(m) for m in machines])
    scene.play(ReplacementTransform(hero, brackets), run_time=1.6)
    scene.play(LaggedStart(*[Indicate(b, color=cfg.CYAN) for b in brackets], lag_ratio=0.2), run_time=1.6)

    # --- Each bracket is a machine with two doors ---------------------------------
    beat(scene, t, 1)
    scene.play(*[ReplacementTransform(b, m) for b, m in zip(brackets, machines)], run_time=1.6)
    door_tags = VGroup(
        txt("door a", cfg.FONT["small"], cfg.A_COLOR).next_to(machines[0].doors["a"], DOWN, buff=0.55),
        txt("door b", cfg.FONT["small"], cfg.B_COLOR).next_to(machines[0].doors["b"], DOWN, buff=0.55),
    )
    door_tags[0].shift(LEFT * 0.25)
    door_tags[1].shift(RIGHT * 0.25)
    scene.play(FadeIn(door_tags, shift=UP * 0.15), run_time=0.8)

    beat(scene, t, 2)
    for letter in ("a", "b"):
        scene.play(machines[0].animate.choose(letter), run_time=0.7)
    scene.play(machines[0].animate.reset(), FadeOut(door_tags), run_time=0.6)

    # --- One set of choices: a a b a b -------------------------------------------------
    beat(scene, t, 3)
    cells = VGroup()
    for machine, letter in zip(machines, DEMO):
        cell = choice_cell(letter, 0.85).move_to([machine.get_center()[0], 0.25, 0])
        door = machine.doors[letter]
        scene.play(machine.animate.choose(letter), run_time=0.55)
        scene.play(TransformFromCopy(door, cell), run_time=0.6)
        cells.add(cell)

    beat(scene, t, 4)
    word = choice_list(DEMO, 0.85).move_to([0, 0.25, 0])
    scene.play(*[ReplacementTransform(c, w) for c, w in zip(cells, word)], run_time=1.0)
    product = colored_tex([(letter, letter) for letter in DEMO] + [("=", "op"), ("a^{3}", "a"), ("b^{2}", "b")],
                          cfg.FONT["title"]).move_to([0, -1.25, 0])
    scene.play(*[TransformFromCopy(word[i].glyph, product.pieces[i]) for i in range(N)], run_time=1.2)
    scene.play(FadeIn(VGroup(*product.pieces[N:]), shift=LEFT * 0.3), run_time=1.0)
    scene.play(Circumscribe(VGroup(*product.pieces[N + 1:]), color=cfg.GOLD, buff=0.1), run_time=1.2)

    # --- How many products? ---------------------------------------------------------------
    beat(scene, t, 5)
    how_many = txt("How many?", cfg.FONT["title"], cfg.ORANGE).move_to([0, -0.6, 0])
    scene.play(FadeOut(word), FadeOut(product), *[m.animate.reset() for m in machines], run_time=0.8)
    scene.play(FadeIn(how_many, scale=1.2), run_time=0.7)

    beat(scene, t, 6)
    twos = VGroup(*[txt("2", cfg.FONT["section"], cfg.GOLD).next_to(m, DOWN, buff=0.3) for m in machines])
    for machine, two in zip(machines, twos):
        scene.play(machine.animate.choose("a"), FadeIn(two, shift=DOWN * 0.2), run_time=0.45)
        scene.play(machine.animate.choose("b"), run_time=0.35)
    total = colored_tex([("2", "coef"), (r"\times", "op"), ("2", "coef"), (r"\times", "op"), ("2", "coef"),
                         (r"\times", "op"), ("2", "coef"), (r"\times", "op"), ("2", "coef"), ("=", "op"),
                         ("32", "coef")], cfg.FONT["title"]).move_to([0, -1.1, 0])
    scene.play(FadeOut(how_many),
               *[TransformFromCopy(two, total.pieces[2 * i]) for i, two in enumerate(twos)],
               FadeIn(VGroup(*[total.pieces[2 * i + 1] for i in range(4)])), *[m.animate.reset() for m in machines],
               run_time=1.4)
    scene.play(FadeIn(VGroup(*total.pieces[-2:]), scale=1.3), run_time=0.8)
    scene.play(Indicate(total.pieces[-1], color=cfg.GOLD, scale_factor=1.4), run_time=0.9)

    # --- All thirty-two lists ----------------------------------------------------------------
    beat(scene, t, 7)
    head = swap_heading(scene, head, "All 32 choice lists")
    words = mu.choice_words(N)
    lists = VGroup(*[choice_list(w, BIG_CELL) for w in words])
    for lst, point in zip(lists, grid_positions(len(words), 4, x_step=3.2, y_step=0.56, center=(0.0, -0.25))):
        lst.move_to(point)
    scene.play(FadeOut(VGroup(machines, twos, total)), run_time=0.7)
    scene.play(LaggedStart(*[FadeIn(lst, shift=DOWN * 0.15) for lst in lists], lag_ratio=0.06), run_time=3.0)

    beat(scene, t, 8)
    note = caption("32 choices → 32 products", cfg.ORANGE, cfg.FONT["body"], y=-3.55)
    scene.play(FadeIn(note, shift=UP * 0.15), run_time=0.8)
    scene.play(LaggedStart(*[Indicate(lst, color=cfg.WHITE, scale_factor=1.05) for lst in lists], lag_ratio=0.04),
               run_time=2.6)

    # --- Make room, then sort by number of b's --------------------------------------------------
    beat(scene, t, 9)
    head = swap_heading(scene, head, "Sort by the number of b's")
    band = grid_positions(len(words), 8, x_step=1.62, y_step=0.33, center=(0.0, BAND_Y))
    scene.play(FadeOut(note),
               *[lst.animate.scale(BAND_CELL / BIG_CELL).move_to(p) for lst, p in zip(lists, band)], run_time=1.6)
    floor = Line([_pile_x(0) - 1.2, BASELINE, 0], [_pile_x(N) + 1.2, BASELINE, 0], stroke_color=cfg.MUTED,
                 stroke_width=3)
    labels = VGroup(*[term_tex(1, N - k, k, cfg.FONT["body"]).move_to([_pile_x(k), LABEL_Y, 0]) for k in range(N + 1)])
    scene.play(Create(floor), LaggedStart(*[FadeIn(lab, shift=UP * 0.2) for lab in labels], lag_ratio=0.15),
               run_time=1.6)

    piles = mu.sort_into_piles(N)
    by_word = dict(zip(words, lists))

    def send(k_values, run_time):
        moves = []
        for k in k_values:
            for j, w in enumerate(piles[k]):
                moves.append(by_word[w].animate.scale(PILE_CELL / BAND_CELL).move_to(_pile_slot(k, j)))
        scene.play(LaggedStart(*moves, lag_ratio=0.12), run_time=run_time)

    beat(scene, t, 10)
    send([0], 1.2)
    scene.play(Indicate(labels[0], color=cfg.WHITE), run_time=0.8)
    beat(scene, t, 11)
    send([1], 2.4)
    scene.play(Indicate(labels[1], color=cfg.WHITE), run_time=0.8)
    beat(scene, t, 12)
    send([2], 3.0)
    beat(scene, t, 13)
    send([3, 4, 5], 4.4)

    # --- The piles: 1, 5, 10, 10, 5, 1 --------------------------------------------------------------
    beat(scene, t, 14)
    counts = VGroup(*[txt(str(len(piles[k])), cfg.FONT["title"], cfg.GOLD).move_to([_pile_x(k), COUNT_Y, 0])
                      for k in range(N + 1)])
    for k in range(N + 1):
        pile = VGroup(*[by_word[w] for w in piles[k]])
        scene.play(Indicate(pile, color=cfg.GOLD, scale_factor=1.05), FadeIn(counts[k], shift=UP * 0.2), run_time=0.8)

    beat(scene, t, 15)
    terms = VGroup(*[term_tex(c, N - k, k, cfg.FONT["body"], show_one=True).move_to([_pile_x(k), LABEL_Y - 0.4, 0])
                     for k, c in enumerate(mu.coefficients(N))])
    scene.play(*[ReplacementTransform(VGroup(counts[k], labels[k]), terms[k]) for k in range(N + 1)], run_time=1.8)
    scene.play(LaggedStart(*[Indicate(term[0], color=cfg.GOLD, scale_factor=1.4) for term in terms], lag_ratio=0.15),
               run_time=2.0)

    beat(scene, t, 16)
    total_parts = []
    for k, c in enumerate(mu.coefficients(N)):
        if k:
            total_parts.append(("+", "op"))
        total_parts.append((str(c), "coef"))
    total_parts += [("=", "op"), (str(mu.row_sum(N)), "ok"), ("=", "op"), ("2^{5}", "ok")]
    sum_line = colored_tex(total_parts, cfg.FONT["section"]).move_to([0, BAND_Y - 0.15, 0])
    scene.play(Write(sum_line), run_time=1.8)
    scene.play(Indicate(VGroup(*sum_line.pieces[-3:]), color=cfg.GREEN), run_time=1.0)

    # --- The row is the pile sizes ----------------------------------------------------------------------
    beat(scene, t, 17)
    outline_points = [[_pile_x(0) - 1.0, BASELINE, 0]]
    for k in range(N + 1):
        top = BASELINE + len(piles[k]) * PILE_STEP + 0.05
        outline_points += [[_pile_x(k) - 1.0, top, 0], [_pile_x(k) + 1.0, top, 0]]
    outline_points.append([_pile_x(N) + 1.0, BASELINE, 0])
    outline = VMobject(stroke_color=cfg.GOLD, stroke_width=5).set_points_as_corners(outline_points)
    row = VGroup(*[txt(str(c), cfg.FONT["title"], cfg.GOLD) for c in mu.coefficients(N)])
    for k, entry in enumerate(row):
        entry.move_to([_pile_x(k), BAND_Y - 0.15, 0])
    scene.play(Create(outline), run_time=1.6)
    scene.play(ReplacementTransform(sum_line, row), run_time=1.4)
    scene.play(Indicate(row, color=cfg.WHITE, scale_factor=1.08), run_time=1.0)

    # --- How do we count a pile without listing it? ---------------------------------------------------------
    beat(scene, t, 18)
    focus = VGroup(*[by_word[w] for w in piles[2]])
    rest = VGroup(*[by_word[w] for k in range(N + 1) if k != 2 for w in piles[k]])
    scene.play(FadeOut(row), FadeOut(outline), rest.animate.set_opacity(0.18),
               *[terms[k].animate.set_opacity(cfg.CONTEXT_OPACITY) for k in range(N + 1) if k != 2], run_time=1.0)
    frame = glow_frame(focus, cfg.GOLD, buff=0.15)
    why = txt("?", cfg.FONT["hero"], cfg.ORANGE).next_to(frame, UP, buff=0.25)
    scene.play(Create(frame), FadeIn(why, scale=1.5), run_time=1.0)
    scene.play(Wiggle(why), run_time=1.2)
    scene.play(LaggedStart(*[Indicate(lst, color=cfg.GOLD, scale_factor=1.12) for lst in focus], lag_ratio=0.25),
               run_time=3.0)
    scene.play(Circumscribe(terms[2], color=cfg.GOLD, buff=0.1), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["05"])
