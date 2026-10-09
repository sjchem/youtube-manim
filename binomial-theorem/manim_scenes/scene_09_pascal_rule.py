"""Chapter 9 — why Pascal's rule works, by counting.

The ten lists with two b's are split by one question about the last machine:
does it say b (then one more b among the first four: 4 choose 1 = 4) or a
(then both b's among the first four: 4 choose 2 = 6)? 4 + 6 = 10 with nothing
counted twice. The same in/out split gives n choose k = (n-1 choose k-1) +
(n-1 choose k), and it is exactly chapter 4's "times b / times a" copies.
"""

from manim_scenes.common import *

N, K = 5, 2
CELL = 0.4
LEFT_X, RIGHT_XS = -4.6, (1.55, 4.45)
GROUP_TOP, GROUP_STEP = -0.75, 0.5


class Scene09PascalRule(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _binom(n, k) -> str:
    return rf"\binom{{{n}}}{{{k}}}"


def _rule(n, k, size, role="coef") -> MathTex:
    return colored_tex([(_binom(n, k), role), ("=", "op"), (_binom(f"{n}-1" if isinstance(n, str) else n - 1,
                                                                   f"{k}-1" if isinstance(k, str) else k - 1), role),
                        ("+", "op"), (_binom(f"{n}-1" if isinstance(n, str) else n - 1, k), role)], size)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "09", "Why does 4 + 6 make 10?")

    # --- The claim ------------------------------------------------------------
    four, six = txt("4", cfg.FONT["hero"], cfg.GOLD).move_to([-5.6, 1.4, 0]), txt("6", cfg.FONT["hero"], cfg.GOLD).move_to([-3.4, 1.4, 0])
    ten = txt("10", cfg.FONT["hero"], cfg.GOLD).move_to([-4.5, -0.6, 0])
    feeds = VGroup(arrow_between(four.get_bottom(), ten.get_top() + LEFT * 0.2, cfg.CYAN, 6),
                   arrow_between(six.get_bottom(), ten.get_top() + RIGHT * 0.2, cfg.CYAN, 6))
    claim = _rule(N, K, cfg.FONT["title"]).move_to([2.6, 0.4, 0])
    scene.play(FadeIn(VGroup(four, six)), GrowArrow(feeds[0]), GrowArrow(feeds[1]), FadeIn(ten), run_time=1.4)
    scene.play(Write(claim), run_time=2.0)
    scene.play(Indicate(claim.pieces[0], color=cfg.WHITE), Indicate(ten, color=cfg.WHITE), run_time=1.0)
    scene.play(Indicate(VGroup(claim.pieces[2], claim.pieces[4]), color=cfg.WHITE),
               Indicate(VGroup(four, six), color=cfg.WHITE), run_time=1.0)

    # --- The ten lists -----------------------------------------------------------
    beat(scene, t, 1)
    words = list(mu.words_with_b(N, K))
    lists = {w: choice_list(w, CELL) for w in words}
    for i, w in enumerate(words):
        lists[w].move_to([(i % 5 - 2) * 2.85, 1.45 if i < 5 else 0.75, 0])
    scene.play(FadeOut(VGroup(four, six, ten, feeds)), claim.animate.scale(0.72).move_to(UP * 2.5), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(lists[w], shift=DOWN * 0.15) for w in words], lag_ratio=0.08), run_time=1.6)

    beat(scene, t, 2)
    head = swap_heading(scene, head, "Watch the last machine")
    lasts = VGroup(*[glow_frame(lists[w][-1], cfg.GOLD, buff=0.06, width=3) for w in words])
    scene.play(LaggedStart(*[Create(f) for f in lasts], lag_ratio=0.08), run_time=1.6)

    # --- Two groups ---------------------------------------------------------------------
    beat(scene, t, 3)
    says_b = chip("last says b", cfg.B_COLOR, cfg.FONT["body"]).move_to([LEFT_X, -0.05, 0])
    says_a = chip("last says a", cfg.A_COLOR, cfg.FONT["body"]).move_to([sum(RIGHT_XS) / 2, -0.05, 0])
    divider = DashedLine([-1.35, -0.55, 0], [-1.35, -3.9, 0], color=cfg.MUTED, stroke_width=3)
    scene.play(FadeOut(lasts), FadeIn(says_b, shift=DOWN * 0.15), FadeIn(says_a, shift=DOWN * 0.15), Create(divider),
               run_time=1.2)
    with_b, with_a = mu.split_by_last(N, K)

    beat(scene, t, 4)
    scene.play(LaggedStart(*[lists[w].animate.move_to([LEFT_X, GROUP_TOP - j * GROUP_STEP, 0])
                             for j, w in enumerate(with_b)], lag_ratio=0.2), run_time=2.0)
    scene.play(*[lists[w][-1].animate.set_opacity(cfg.CONTEXT_OPACITY) for w in with_b], run_time=0.6)
    scene.play(*[Indicate(cell, color=cfg.WHITE, scale_factor=1.3) for w in with_b
                 for cell in lists[w][:-1] if cell.letter == "b"], run_time=1.0)
    left_count = colored_tex([(_binom(N - 1, K - 1), "coef"), ("=", "op"), (str(len(with_b)), "coef")],
                             cfg.FONT["section"]).move_to([LEFT_X, -3.5, 0])
    scene.play(FadeIn(left_count, shift=UP * 0.2), run_time=0.9)

    beat(scene, t, 5)
    scene.play(LaggedStart(*[lists[w].animate.move_to([RIGHT_XS[j // 3], GROUP_TOP - (j % 3) * GROUP_STEP, 0])
                             for j, w in enumerate(with_a)], lag_ratio=0.15), run_time=2.2)
    scene.play(*[lists[w][-1].animate.set_opacity(cfg.CONTEXT_OPACITY) for w in with_a], run_time=0.6)
    scene.play(*[Indicate(cell, color=cfg.WHITE, scale_factor=1.3) for w in with_a
                 for cell in lists[w][:-1] if cell.letter == "b"], run_time=1.0)
    right_count = colored_tex([(_binom(N - 1, K), "coef"), ("=", "op"), (str(len(with_a)), "coef")],
                              cfg.FONT["section"]).move_to([sum(RIGHT_XS) / 2, -3.5, 0])
    scene.play(FadeIn(right_count, shift=UP * 0.2), run_time=0.9)

    beat(scene, t, 6)
    total = colored_tex([("4", "coef"), ("+", "op"), ("6", "coef"), ("=", "op"), (str(mu.choose(N, K)), "ok")],
                        cfg.FONT["title"]).move_to([-0.8, 1.15, 0])
    scene.play(FadeIn(total, scale=1.15), run_time=0.9)
    scene.play(claim.animate.set_color(cfg.GREEN), run_time=0.8)
    scene.play(Indicate(VGroup(*lists.values()), color=cfg.WHITE, scale_factor=1.03), run_time=1.2)

    # --- In general: the newest item is in or out ---------------------------------------------
    beat(scene, t, 7)
    head = swap_heading(scene, head, "In or out?")
    scene.play(FadeOut(VGroup(*lists.values(), says_a, says_b, divider, left_count, right_count, total, claim)),
               run_time=0.8)
    items = VGroup(*[Circle(radius=0.36, stroke_color=cfg.CYAN, stroke_width=4, fill_color=cfg.PANEL, fill_opacity=1)
                     for _ in range(7)]).arrange(RIGHT, buff=0.4).move_to(UP * 1.85)
    newest = items[-1]
    newest.set_stroke(cfg.GOLD, 6)
    n_brace = count_brace(items, "n items, choose k", cfg.LIMIT_COLOR, direction=UP, size=cfg.FONT["body"])
    scene.play(LaggedStart(*[GrowFromCenter(c) for c in items], lag_ratio=0.1), FadeIn(n_brace), run_time=1.4)
    scene.play(Flash(newest, color=cfg.GOLD, flash_radius=0.6), newest.animate.set_fill(cfg.GOLD, 0.3), run_time=0.8)
    in_chip = chip("newest is in", cfg.B_COLOR, cfg.FONT["body"]).move_to([-3.9, 0.8, 0])
    in_rest = colored_tex([(_binom("n-1", "k-1"), "limit")], cfg.FONT["section"]).move_to([-3.9, -0.65, 0])
    in_arrow = arrow_between(newest.get_bottom(), in_chip.get_top(), cfg.B_COLOR)
    scene.play(GrowArrow(in_arrow), FadeIn(in_chip), run_time=1.0)
    scene.play(FadeIn(in_rest, shift=DOWN * 0.2), run_time=1.0)

    beat(scene, t, 8)
    out_chip = chip("newest is out", cfg.A_COLOR, cfg.FONT["body"]).move_to([3.9, 0.8, 0])
    out_rest = colored_tex([(_binom("n-1", "k"), "limit")], cfg.FONT["section"]).move_to([3.9, -0.65, 0])
    out_arrow = arrow_between(newest.get_bottom(), out_chip.get_top(), cfg.A_COLOR)
    scene.play(GrowArrow(out_arrow), FadeIn(out_chip), run_time=1.0)
    scene.play(FadeIn(out_rest, shift=DOWN * 0.2), run_time=1.0)

    beat(scene, t, 9)
    rule = _rule("n", "k", cfg.FONT["title"], role="limit").move_to(DOWN * 2.75)
    scene.play(TransformFromCopy(VGroup(in_rest, out_rest), VGroup(rule.pieces[2], rule.pieces[4])),
               FadeIn(VGroup(rule.pieces[0], rule.pieces[1], rule.pieces[3])), run_time=1.8)
    scene.play(Circumscribe(rule, color=cfg.LIMIT_COLOR, buff=0.12), run_time=1.4)

    # --- That is the triangle's addition rule --------------------------------------------------------
    beat(scene, t, 10)
    head = swap_heading(scene, head, "The addition rule, explained")
    scene.play(FadeOut(VGroup(items, n_brace, in_chip, out_chip, in_arrow, out_arrow, in_rest, out_rest)), run_time=0.8)
    upper_left = eq(_binom("n-1", "k-1"), cfg.FONT["section"], cfg.GOLD).move_to([-2.0, 1.75, 0])
    upper_right = eq(_binom("n-1", "k"), cfg.FONT["section"], cfg.GOLD).move_to([2.0, 1.75, 0])
    below = eq(_binom("n", "k"), cfg.FONT["section"], cfg.GOLD).move_to([0, -0.55, 0])
    joins = VGroup(arrow_between(upper_left.get_bottom(), below.get_top() + LEFT * 0.2, cfg.B_COLOR, 6),
                   arrow_between(upper_right.get_bottom(), below.get_top() + RIGHT * 0.2, cfg.A_COLOR, 6))
    tags = VGroup(txt("in", cfg.FONT["body"], cfg.B_COLOR).next_to(joins[0], LEFT, buff=0.15),
                  txt("out", cfg.FONT["body"], cfg.A_COLOR).next_to(joins[1], RIGHT, buff=0.15)).shift(DOWN * 0.2)
    scene.play(FadeIn(upper_left), FadeIn(upper_right), run_time=0.8)
    scene.play(GrowArrow(joins[0]), GrowArrow(joins[1]), FadeIn(below, shift=DOWN * 0.2), run_time=1.2)
    scene.play(FadeIn(tags, scale=1.2), run_time=0.8)
    scene.play(Indicate(below, color=cfg.WHITE, scale_factor=1.25), run_time=1.0)

    # --- The same split, in algebra's clothes ---------------------------------------------------------------
    beat(scene, t, 11)
    scene.play(FadeOut(VGroup(upper_left, upper_right, below, joins, tags)), run_time=0.7)
    recipe = colored_tex(lhs_parts(N) + lhs_parts(N - 1, sep=r"\cdot"), cfg.FONT["section"]).move_to([-1.6, 1.4, 0])
    machine = ChoiceMachine(width=2.5, height=1.5, door=0.5).next_to(recipe, RIGHT, buff=0.35)
    scene.play(FadeIn(recipe, shift=RIGHT * 0.2), FadeIn(machine, shift=LEFT * 0.2), run_time=1.0)
    times_a = colored_tex([(r"\times", "op"), ("a", "a"), (r":\ \text{newest says } a", "a")], cfg.FONT["body"])
    times_b = colored_tex([(r"\times", "op"), ("b", "b"), (r":\ \text{newest says } b", "b")], cfg.FONT["body"])
    times_a.move_to([-3.6, -0.45, 0])
    times_b.move_to([3.6, -0.45, 0])
    scene.play(machine.animate.choose("a"), FadeIn(times_a, shift=DOWN * 0.15), run_time=1.0)
    scene.play(machine.animate.choose("b"), FadeIn(times_b, shift=DOWN * 0.15), run_time=1.0)
    scene.play(Indicate(rule, color=cfg.WHITE, scale_factor=1.05), run_time=1.2)
    scene.play(machine.animate.reset(), run_time=0.6)

    beat(scene, t, 12)
    head = swap_heading(scene, head, "Next: paths")
    scene.play(FadeOut(VGroup(recipe, machine, times_a, times_b, rule)), run_time=0.8)
    triangle_pegs = VGroup(*[peg(pascal_point(n, k, 1.2, 0.85, UP * 2.0)) for n in range(5) for k in range(n + 1)])
    route = path_line("abab", lambda n, k: pascal_point(n, k, 1.2, 0.85, UP * 2.0), width=6)
    scene.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in triangle_pegs], lag_ratio=0.05), run_time=1.4)
    scene.play(LaggedStart(*[Create(seg) for seg in route], lag_ratio=0.6), run_time=2.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["09"])
