"""Chapter 8 — why the exponents move in opposite directions.

Every product has exactly n = 5 factors, so turning one a into a b moves one
step along the expansion: the power of a drops by one as the power of b rises.
The same trade explains the mirror symmetry n choose k = n choose (n - k)
(picking which say b is picking which say a), and setting a = b = 1 turns
every row into a sum equal to 2^n.
"""

from manim_scenes.common import *

N = 5
EXP_Y = 2.45
LIST_X, TERM_X, LIST_Y = -1.6, 4.3, -1.35


class Scene08Exponents(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _x_of(expansion: MathTex, k: int) -> float:
    return expansion.terms[k].get_x()


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "08", "Opposite exponents")

    expansion = expansion_tex(N, cfg.FONT["section"]).move_to(UP * EXP_Y)
    scene.play(FadeIn(expansion, shift=DOWN * 0.2), run_time=1.0)
    a_row = VGroup(*[txt(str(N - k), cfg.FONT["section"], cfg.A_COLOR).move_to([_x_of(expansion, k), 1.25, 0])
                     for k in range(N + 1)])
    b_row = VGroup(*[txt(str(k), cfg.FONT["section"], cfg.B_COLOR).move_to([_x_of(expansion, k), 0.35, 0])
                     for k in range(N + 1)])
    a_tag = eq("a", cfg.FONT["section"], cfg.A_COLOR).move_to([-7.3, 1.25, 0])
    b_tag = eq("b", cfg.FONT["section"], cfg.B_COLOR).move_to([-7.3, 0.35, 0])
    scene.play(FadeIn(a_tag), run_time=0.5)
    scene.play(LaggedStart(*[FadeIn(n, shift=DOWN * 0.2) for n in a_row], lag_ratio=0.25), run_time=2.6)
    down = Arrow([_x_of(expansion, 0), 0.8, 0], [_x_of(expansion, N), 0.8, 0], buff=0.3, color=cfg.A_COLOR,
                 stroke_width=4, max_tip_length_to_length_ratio=0.03).set_opacity(0.6)
    scene.play(GrowArrow(down), run_time=1.0)

    beat(scene, t, 1)
    scene.play(FadeIn(b_tag), run_time=0.5)
    scene.play(LaggedStart(*[FadeIn(n, shift=UP * 0.2) for n in b_row], lag_ratio=0.25), run_time=2.6)

    beat(scene, t, 2)
    why = txt("?", cfg.FONT["hero"], cfg.ORANGE).move_to([0, -1.4, 0])
    scene.play(FadeIn(why, scale=1.5), run_time=0.8)
    scene.play(Wiggle(why), run_time=1.2)

    # --- Five factors, always ----------------------------------------------------------
    beat(scene, t, 3)
    head = swap_heading(scene, head, "Always five factors")
    word = "a" * N
    letters = choice_list(word, 1.0).move_to([LIST_X, LIST_Y, 0])
    five = count_brace(letters, "5 factors", cfg.MUTED, direction=DOWN, size=cfg.FONT["body"])
    term = term_tex(1, N, 0, cfg.FONT["title"]).move_to([TERM_X, LIST_Y, 0])
    equals = eq("=", cfg.FONT["title"]).move_to([(letters.get_right()[0] + term.get_left()[0]) / 2, LIST_Y, 0])
    scene.play(FadeOut(why), FadeIn(letters, shift=UP * 0.2), run_time=0.9)
    scene.play(FadeIn(five, shift=UP * 0.15), run_time=0.8)
    scene.play(FadeIn(equals), FadeIn(term, shift=LEFT * 0.2), run_time=0.8)

    # --- Trade one a for one b, again and again -------------------------------------------
    beat(scene, t, 4)
    spot = glow_frame(VGroup(expansion.terms[0], a_row[0], b_row[0]), cfg.GOLD, buff=0.15)
    scene.play(Create(spot), run_time=0.8)

    def flip(k: int, run_time: float) -> None:
        nonlocal letters, term, spot
        new_word = "a" * (N - k) + "b" * k
        new_letters = choice_list(new_word, 1.0).move_to(letters)
        new_term = term_tex(1, N - k, k, cfg.FONT["title"]).move_to([TERM_X, LIST_Y, 0])
        new_spot = glow_frame(VGroup(expansion.terms[k], a_row[k], b_row[k]), cfg.GOLD, buff=0.15)
        scene.play(ReplacementTransform(letters[N - k], new_letters[N - k]),
                   *[ReplacementTransform(letters[i], new_letters[i]) for i in range(N) if i != N - k],
                   ReplacementTransform(term, new_term), ReplacementTransform(spot, new_spot), run_time=run_time)
        letters, term, spot = new_letters, new_term, new_spot

    flip(1, 1.4)
    scene.play(Indicate(a_row[1], color=cfg.WHITE), Indicate(b_row[1], color=cfg.WHITE), run_time=0.9)

    beat(scene, t, 5)
    for k in range(2, N + 1):
        flip(k, 1.2)
        scene.play(Indicate(VGroup(a_row[k], b_row[k]), color=cfg.WHITE), run_time=0.4)

    beat(scene, t, 6)
    budget = colored_tex([("(5-k)", "a"), ("+", "op"), ("k", "b"), ("=", "op"), ("5", "coef")], cfg.FONT["title"])
    budget.move_to([0, -3.45, 0])
    scene.play(FadeOut(five), FadeIn(budget, shift=UP * 0.2), run_time=1.0)
    columns = VGroup(*[VGroup(a_row[k], b_row[k]) for k in range(N + 1)])
    scene.play(LaggedStart(*[Indicate(c, color=cfg.GOLD) for c in columns], lag_ratio=0.15), run_time=2.4)

    # --- The mirror ----------------------------------------------------------------------------
    beat(scene, t, 7)
    head = swap_heading(scene, head, "Swap a and b: the mirror")
    scene.play(FadeOut(VGroup(a_row, b_row, a_tag, b_tag, down, spot, letters, equals, term, budget)), run_time=0.8)
    row = VGroup(*[txt(str(c), cfg.FONT["hero"], cfg.GOLD).move_to([_x_of(expansion, k), 0.85, 0])
                   for k, c in enumerate(mu.coefficients(N))])
    scene.play(LaggedStart(*[TransformFromCopy(expansion.coefs[k] if expansion.coefs[k] else expansion.terms[k], e)
                             for k, e in enumerate(row)], lag_ratio=0.1), run_time=1.6)
    mid = (row[0].get_x() + row[N].get_x()) / 2
    mirror = DashedLine([mid, 1.9, 0], [mid, -0.1, 0], color=cfg.MUTED, stroke_width=3)
    scene.play(Create(mirror), run_time=0.6)
    # Each entry trades places with its mirror partner: the row reverses and reads the same.
    homes = [e.get_center() for e in row]
    scene.play(*[e.animate(path_arc=-PI / 2).move_to(homes[N - k]) for k, e in enumerate(row)], run_time=1.8)
    row.submobjects.reverse()
    scene.play(Indicate(row, color=cfg.WHITE, scale_factor=1.05), run_time=0.9)

    beat(scene, t, 8)
    pick = choice_list("bbaaa", 0.95).move_to([-3.5, -1.2, 0])
    say_b = count_brace(VGroup(pick[0], pick[1]), "2 say b", cfg.B_COLOR, size=cfg.FONT["body"])
    say_a = count_brace(VGroup(pick[2], pick[3], pick[4]), "3 say a", cfg.A_COLOR, size=cfg.FONT["body"])
    scene.play(FadeIn(pick, shift=UP * 0.2), run_time=0.8)
    scene.play(FadeIn(say_b, shift=UP * 0.15), run_time=0.8)
    scene.play(FadeIn(say_a, shift=UP * 0.15), run_time=0.8)

    beat(scene, t, 9)
    pairs = VGroup(*[ArcBetweenPoints(row[k].get_bottom() + DOWN * 0.08, row[N - k].get_bottom() + DOWN * 0.08,
                                      angle=PI / 4, stroke_color=cfg.GOLD, stroke_width=3.5, stroke_opacity=0.8)
                     for k in range(3)])
    same = colored_tex([(r"\binom{5}{2}", "coef"), ("=", "op"), (r"\binom{5}{3}", "coef")], cfg.FONT["title"])
    same.move_to([3.9, -2.1, 0])
    scene.play(LaggedStart(*[Create(arc) for arc in pairs], lag_ratio=0.3), run_time=1.4)
    scene.play(Write(same), run_time=1.2)
    scene.play(Indicate(VGroup(row[2], row[3]), color=cfg.WHITE), run_time=1.0)

    beat(scene, t, 10)
    general = colored_tex([(r"\binom{n}{k}", "limit"), ("=", "op"), (r"\binom{n}{n-k}", "limit")], cfg.FONT["title"])
    general.move_to(same)
    scene.play(ReplacementTransform(same, general), run_time=1.2)
    scene.play(Circumscribe(general, color=cfg.LIMIT_COLOR, buff=0.12), run_time=1.4)

    # --- The sum of a row ----------------------------------------------------------------------------
    beat(scene, t, 11)
    head = swap_heading(scene, head, "Set a = b = 1")
    scene.play(FadeOut(VGroup(row, mirror, pick, say_b, say_a, pairs, general)), run_time=0.8)
    ones = [("(", "op"), ("1", "a"), ("+", "op"), ("1", "b"), (")^{5}", "op"), ("=", "op")]
    for k, c in enumerate(mu.coefficients(N)):
        if k:
            ones.append(("+", "op"))
        ones.append((str(c), "coef"))
    substituted = colored_tex(ones, cfg.FONT["title"]).move_to(UP * 0.6)
    scene.play(TransformFromCopy(expansion, substituted), run_time=2.0)
    scene.play(Indicate(VGroup(substituted.pieces[1], substituted.pieces[3]), color=cfg.WHITE, scale_factor=1.3),
               run_time=1.0)

    beat(scene, t, 12)
    total = colored_tex([(r"2^{5}", "ok"), ("=", "op"), (str(mu.row_sum(N)), "ok")], cfg.FONT["hero"]).move_to(DOWN * 1.3)
    scene.play(FadeIn(total, scale=1.15), run_time=1.0)
    lists = txt("every choice list, counted once", cfg.FONT["body"], cfg.GREEN).move_to(DOWN * 2.85)
    scene.play(FadeIn(lists, shift=UP * 0.15), run_time=0.8)

    # --- Why do neighbours add? ------------------------------------------------------------------------
    beat(scene, t, 13)
    head = swap_heading(scene, head, "Why does the addition rule work?")
    scene.play(FadeOut(VGroup(expansion, substituted, total, lists)), run_time=0.8)
    four, six = txt("4", cfg.FONT["hero"], cfg.GOLD), txt("6", cfg.FONT["hero"], cfg.GOLD)
    four.move_to([-1.1, 1.2, 0])
    six.move_to([1.1, 1.2, 0])
    ten = txt("10", cfg.FONT["hero"], cfg.GOLD).move_to([0, -0.9, 0])
    feeds = VGroup(arrow_between(four.get_bottom(), ten.get_top() + LEFT * 0.2, cfg.CYAN, 6),
                   arrow_between(six.get_bottom(), ten.get_top() + RIGHT * 0.2, cfg.CYAN, 6))
    mark = txt("?", cfg.FONT["hero"], cfg.ORANGE).next_to(ten, RIGHT, buff=0.6)
    scene.play(FadeIn(four), FadeIn(six), run_time=0.6)
    scene.play(GrowArrow(feeds[0]), GrowArrow(feeds[1]), FadeIn(ten, shift=DOWN * 0.2), run_time=1.0)
    scene.play(FadeIn(mark, scale=1.4), run_time=0.6)
    scene.play(Wiggle(mark), Indicate(ten, color=cfg.WHITE), run_time=1.4)
    end_scene(scene, t, cfg.SCENE_DURATIONS["08"])
