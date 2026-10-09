"""Chapter 6 — combinations enter.

A list in the a^3 b^2 pile is fixed by *which two* machines say b, so the pile
is the set of 2-element subsets of five machines. They are listed as a
staircase (pairs starting at machine 1, then 2, ...), collapsed into
10 a^3 b^2, and then counted without listing: 5 * 4 ordered picks, divided by
the 2 orders of each pair. That count is 5 choose 2, and in general n choose k.
"""

from manim_scenes.common import *

N, K = 5, 2
MACHINE_Y = 2.35
PAIRS = list(mu.words_with_b(N, K))           # in the order the narration reads them


class Scene06Combinations(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _stair_point(word: str) -> np.ndarray:
    first, second = mu.b_positions(word)
    column = second - first - 1
    return np.array([(column - 1.5) * 3.15, 0.35 - first * 0.88, 0.0])


def _binom(n: int | str, k: int | str, size: int | None = None, color: str = cfg.GOLD) -> MathTex:
    return eq(rf"\binom{{{n}}}{{{k}}}", size or cfg.FONT["section"], color)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "06", "Take one pile")

    # --- The a^3 b^2 pile --------------------------------------------------------
    hero = term_tex(1, 3, 2, cfg.FONT["hero"]).move_to([1.6, 0.6, 0])
    pile = VGroup(*[choice_list(w, 0.32) for w in PAIRS]).arrange(DOWN, buff=0.06).move_to([-4.6, 0.0, 0])
    scene.play(FadeIn(hero, scale=0.9), LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in pile[::-1]],
                                                   lag_ratio=0.08), run_time=2.0)

    # --- Two b's fix the whole list ---------------------------------------------------
    beat(scene, t, 1)
    demo = choice_list("aabab", 0.95).move_to([1.6, -1.6, 0])
    blanks = VGroup(*[RoundedRectangle(width=0.95, height=0.95, corner_radius=0.19, stroke_color=cfg.MUTED,
                                       stroke_width=3, stroke_opacity=0.6).set_fill(opacity=0).move_to(cell)
                      for cell in demo])
    b_cells = VGroup(*[cell for cell in demo if cell.letter == "b"])
    a_cells = VGroup(*[cell for cell in demo if cell.letter == "a"])
    scene.play(Create(blanks), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(c, scale=1.3) for c in b_cells], lag_ratio=0.4), run_time=1.2)
    scene.play(Indicate(b_cells, color=cfg.WHITE), run_time=0.8)
    forced = txt("the rest is forced", cfg.FONT["small"], cfg.MUTED).next_to(demo, DOWN, buff=0.35)
    scene.play(LaggedStart(*[FadeIn(c) for c in a_cells], lag_ratio=0.2), FadeIn(forced), run_time=1.4)
    scene.remove(blanks)

    # --- A list is a choice of two machines ---------------------------------------------------
    beat(scene, t, 2)
    head = swap_heading(scene, head, "Choose 2 of 5 machines")
    machines = machine_row(N, width=2.2, height=1.25, door=0.4, y=MACHINE_Y, show_index=True)
    set_word(machines, "aabab")
    scene.play(FadeOut(VGroup(hero, pile, forced)), demo.animate.scale(0.55).move_to(_stair_point("aabab")),
               LaggedStart(*[FadeIn(m, shift=DOWN * 0.2) for m in machines], lag_ratio=0.1), run_time=1.4)
    scene.play(*[Indicate(machines[i].tag, color=cfg.B_COLOR, scale_factor=1.6) for i in mu.b_positions("aabab")],
               run_time=0.9)
    scene.play(FadeOut(demo), run_time=0.5)

    # --- The staircase of ten pairs -------------------------------------------------------------
    lists = {}
    for index, start_at in ((3, 0), (4, 1), (5, 2)):
        beat(scene, t, index)
        rows = [w for w in PAIRS if mu.b_positions(w)[0] in ((start_at,) if index < 5 else (2, 3))]
        for w in rows:
            lst = choice_list(w, 0.48).move_to(_stair_point(w))
            lists[w] = lst
            scene.play(*[m.animate.choose(c) for m, c in zip(machines, w)], run_time=0.5)
            scene.play(FadeIn(lst, shift=DOWN * 0.25), run_time=0.55)
    staircase = VGroup(*[lists[w] for w in PAIRS])

    # --- Ten lists, ten copies of a^3 b^2 ---------------------------------------------------------
    beat(scene, t, 6)
    ten_label = txt("10 ways", cfg.FONT["title"], cfg.GOLD).move_to([4.6, -1.75, 0])
    scene.play(*[m.animate.reset() for m in machines], FadeIn(ten_label, scale=1.2), run_time=0.9)
    copies = VGroup(*[term_tex(1, 3, 2, cfg.FONT["body"]).move_to(lists[w]) for w in PAIRS])
    scene.play(LaggedStart(*[ReplacementTransform(lists[w], c) for w, c in zip(PAIRS, copies)], lag_ratio=0.1),
               run_time=2.4)

    beat(scene, t, 7)
    result = term_tex(mu.coefficients(N)[K], N - K, K, cfg.FONT["hero"]).move_to(DOWN * 0.6)
    scene.play(ReplacementTransform(VGroup(*copies, ten_label), result), run_time=1.6)
    box = glow_frame(result, cfg.GOLD, buff=0.25)
    scene.play(Create(box), run_time=0.8)

    # --- Count without listing: ordered picks ----------------------------------------------------------
    beat(scene, t, 8)
    head = swap_heading(scene, head, "Count without listing")
    scene.play(FadeOut(VGroup(result, box)), run_time=0.6)
    first = eq("5", cfg.FONT["title"], cfg.GOLD).move_to([-2.4, -0.1, 0])
    scene.play(LaggedStart(*[Indicate(m.doors["b"], color=cfg.GOLD, scale_factor=1.3) for m in machines],
                           lag_ratio=0.1), FadeIn(first, scale=1.3), run_time=1.4)
    scene.play(machines[1].animate.choose("b"), run_time=0.6)
    second = eq("4", cfg.FONT["title"], cfg.GOLD).move_to([0.0, -0.1, 0])
    times = eq(r"\times", cfg.FONT["section"]).move_to([-1.2, -0.1, 0])
    remaining = [m for i, m in enumerate(machines) if i != 1]
    scene.play(LaggedStart(*[Indicate(m.doors["b"], color=cfg.GOLD, scale_factor=1.3) for m in remaining],
                           lag_ratio=0.1), FadeIn(times), FadeIn(second, scale=1.3), run_time=1.3)
    scene.play(machines[3].animate.choose("b"), run_time=0.6)

    beat(scene, t, 9)
    twenty = colored_tex([("=", "op"), (str(mu.ordered_picks(N, K)), "coef")], cfg.FONT["title"])
    twenty.next_to(second, RIGHT, buff=0.3)
    scene.play(FadeIn(twenty, shift=LEFT * 0.2), run_time=0.8)
    twice = txt("each pair counted twice", cfg.FONT["body"], cfg.ORANGE).move_to([0, -1.3, 0])
    scene.play(FadeIn(twice, shift=UP * 0.2), run_time=0.8)

    # --- 2 then 4 is the same list as 4 then 2 ------------------------------------------------------------
    beat(scene, t, 10)
    same = "ababa"
    orders = VGroup(colored_tex([("2", "b"), (r"\to", "op"), ("4", "b")], cfg.FONT["section"]),
                    colored_tex([("4", "b"), (r"\to", "op"), ("2", "b")], cfg.FONT["section"]))
    orders[0].move_to([-4.2, -2.35, 0])
    orders[1].move_to([4.2, -2.35, 0])
    target = choice_list(same, 0.6).move_to([0, -2.35, 0])
    links = VGroup(arrow_between(orders[0].get_right(), target.get_left(), cfg.MUTED),
                   arrow_between(orders[1].get_left(), target.get_right(), cfg.MUTED))
    scene.play(FadeOut(twice), FadeIn(orders[0], shift=RIGHT * 0.2), run_time=0.7)
    scene.play(GrowArrow(links[0]), FadeIn(target), run_time=0.8)
    scene.play(FadeIn(orders[1], shift=LEFT * 0.2), GrowArrow(links[1]), run_time=0.9)
    scene.play(Indicate(target, color=cfg.WHITE, scale_factor=1.15), run_time=0.9)

    beat(scene, t, 11)
    halved = colored_tex([(r"\frac{5\times 4}{2}", "coef"), ("=", "op"), (str(mu.choose(N, K)), "ok")],
                         cfg.FONT["title"]).move_to([0, -0.2, 0])
    scene.play(FadeOut(VGroup(orders, links, target)),
               ReplacementTransform(VGroup(first, times, second, twenty), halved), run_time=1.3)
    scene.play(Indicate(halved.pieces[-1], color=cfg.GREEN, scale_factor=1.4), run_time=0.9)

    # --- Five choose two ---------------------------------------------------------------------------------------
    beat(scene, t, 12)
    head = swap_heading(scene, head, "Five choose two")
    named = colored_tex([(r"\binom{5}{2}", "coef"), ("=", "op"), (str(mu.choose(N, K)), "coef")], cfg.FONT["hero"])
    named.move_to([0, 0.0, 0])
    gloss = caption("Choose 2 of 5. Order doesn't matter.", cfg.MUTED, cfg.FONT["body"], y=-1.85)
    scene.play(FadeOut(machines), ReplacementTransform(halved, named), run_time=1.3)
    scene.play(FadeIn(gloss, shift=UP * 0.2), run_time=0.8)

    # --- Any pile: choose which k of n brackets say b ---------------------------------------------------------------
    beat(scene, t, 13)
    scene.play(FadeOut(VGroup(named, gloss)), run_time=0.6)
    general = VGroup(*[ChoiceMachine(width=1.6, height=1.0, door=0.3) for _ in range(7)]).arrange(RIGHT, buff=0.22)
    general.move_to([0, 0.9, 0])
    general_word = "abaaaba"
    n_brace = count_brace(general, "n brackets", cfg.LIMIT_COLOR, direction=UP, size=cfg.FONT["body"])
    gen_term = colored_tex([("a^{n-k}", "a"), ("b^{k}", "b")], cfg.FONT["title"]).move_to([0, -1.1, 0])
    which = txt("choose which k say b", cfg.FONT["body"], cfg.B_COLOR).move_to([0, -2.4, 0])
    scene.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in general], lag_ratio=0.08), FadeIn(n_brace),
               run_time=1.4)
    scene.play(*[m.animate.choose(c) for m, c in zip(general, general_word)], Write(gen_term), run_time=1.4)
    scene.play(FadeIn(which, shift=UP * 0.2), run_time=0.8)

    beat(scene, t, 14)
    formula = colored_tex([(r"\binom{n}{k}", "limit"), ("=", "op"), (r"\frac{n!}{k!\,(n-k)!}", "limit")],
                          cfg.FONT["hero"]).move_to([0, 0.5, 0])
    scene.play(FadeOut(VGroup(general, n_brace, which)), gen_term.animate.scale(0.8).move_to([0, 2.55, 0]), run_time=0.9)
    scene.play(Write(formula), run_time=2.0)
    scene.play(Circumscribe(formula, color=cfg.LIMIT_COLOR, buff=0.15), run_time=1.4)

    beat(scene, t, 15)
    worked = colored_tex([(r"\binom{5}{2}", "coef"), ("=", "op"), (r"\frac{5!}{2!\,3!}", "op"), ("=", "op"),
                          (r"\frac{120}{2\cdot 6}", "op"), ("=", "op"), (str(mu.choose(N, K)), "ok")],
                         cfg.FONT["section"]).move_to([0, -2.0, 0])
    for group in ((0, 1, 2), (3, 4), (5, 6)):
        scene.play(FadeIn(VGroup(*[worked.pieces[i] for i in group]), shift=LEFT * 0.2), run_time=0.9)

    # --- Every coefficient is a count ------------------------------------------------------------------------------
    beat(scene, t, 16)
    head = swap_heading(scene, head, "Every coefficient is a count")
    scene.play(FadeOut(VGroup(formula, worked, gen_term)), run_time=0.6)
    xs = [(k - N / 2) * 2.3 for k in range(N + 1)]
    binoms = VGroup(*[_binom(N, k, cfg.FONT["section"]).move_to([x, 1.4, 0]) for k, x in enumerate(xs)])
    values = VGroup(*[txt(str(mu.choose(N, k)), cfg.FONT["title"], cfg.GOLD).move_to([x, -0.15, 0])
                      for k, x in enumerate(xs)])
    letters = VGroup(*[term_tex(1, N - k, k, cfg.FONT["section"]).move_to([x, -1.35, 0]) for k, x in enumerate(xs)])
    scene.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in binoms], lag_ratio=0.12), run_time=1.2)
    for k in range(N + 1):
        scene.play(TransformFromCopy(binoms[k], values[k]), FadeIn(letters[k], shift=UP * 0.15), run_time=0.85)

    beat(scene, t, 17)
    takeaway = caption("10 choices → coefficient 10", cfg.GOLD, cfg.FONT["title"], y=-3.0)
    scene.play(FadeIn(takeaway, scale=1.08), run_time=1.0)
    scene.play(Indicate(values, color=cfg.WHITE, scale_factor=1.1), run_time=1.2)

    beat(scene, t, 18)
    scene.play(FadeOut(VGroup(binoms, letters, takeaway)), values.animate.move_to(UP * 0.2), run_time=1.0)
    scene.play(values.animate.scale(1.15), rate_func=there_and_back, run_time=1.4)
    scene.play(Circumscribe(values, color=cfg.GOLD, buff=0.2), run_time=1.4)
    seed = _binom("n", "k", cfg.FONT["hero"], cfg.LIMIT_COLOR).move_to(UP * 0.2)
    scene.play(ReplacementTransform(values, seed), run_time=1.6)
    scene.play(Flash(seed, color=cfg.LIMIT_COLOR, flash_radius=1.2, line_length=0.35), run_time=1.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["06"])
