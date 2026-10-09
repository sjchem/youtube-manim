"""Chapter 7 — the binomial theorem.

The formula arrives only now, so each symbol already has a picture: b^k is
k machines saying b, a^(n-k) is the rest saying a, n choose k counts the ways
to pick them, and the sum collects every k. It is then tested at n = 5 and
used once at n = 10 without any multiplication.
"""

from manim_scenes.common import *

N = 5
LHS = slice(0, 5)
SUM, BINOM, A_POW, B_POW = 6, 7, 8, 9


class Scene07Theorem(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def theorem_tex(n: str = "n", size: int | None = None) -> MathTex:
    """(a+b)^n = sum_k (n choose k) a^(n-k) b^k, coloured by meaning."""
    return colored_tex(lhs_parts(n) + [
        (rf"\sum_{{k=0}}^{{{n}}}", "op"),
        (rf"\binom{{{n}}}{{k}}", "coef"),
        (f"a^{{{n}-k}}", "a"),
        ("b^{k}", "b"),
    ], size or cfg.FONT["title"])


def _meaning(scene, formula, index, words, color, machines, word, old=None):
    """Brace one symbol of the formula and give it a short caption."""
    brace = Brace(formula.pieces[index], DOWN, color=color, buff=0.15)
    # Hang it below the whole formula: the sum's lower limit reaches lower than b^k.
    brace.next_to(formula, DOWN, buff=0.12).set_x(formula.pieces[index].get_x())
    label = txt(words, cfg.FONT["body"], color).next_to(brace, DOWN, buff=0.15)
    label.set_x(np.clip(label.get_x(), -7.6 + label.width / 2, 7.6 - label.width / 2))
    dims = [formula.pieces[i].animate.set_opacity(1 if i == index else cfg.CONTEXT_OPACITY)
            for i in range(len(formula.pieces))]
    anims = [FadeIn(brace), FadeIn(label, shift=DOWN * 0.15), *dims]
    if old is not None:
        anims.append(FadeOut(old))
    scene.play(*anims, run_time=0.8)
    if word:
        scene.play(*[m.animate.choose(c) if c in "ab" else m.animate.reset() for m, c in zip(machines, word)],
                   run_time=0.7)
    return VGroup(brace, label)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "07", "The binomial theorem")

    formula = theorem_tex().move_to(UP * 0.4)
    glow = halo(4.2, cfg.LIMIT_COLOR, peak_opacity=0.07).move_to(formula)
    scene.play(FadeIn(glow), Write(formula), run_time=2.4)

    # --- Read it aloud --------------------------------------------------------
    beat(scene, t, 1)
    for part in (VGroup(*formula.pieces[LHS]), formula.pieces[SUM], formula.pieces[BINOM],
                 formula.pieces[A_POW], formula.pieces[B_POW]):
        scene.play(Indicate(part, color=cfg.WHITE, scale_factor=1.12), run_time=1.5)

    # --- From the inside out ------------------------------------------------------
    beat(scene, t, 2)
    head = swap_heading(scene, head, "What each symbol means")
    machines = machine_row(N, width=2.1, height=1.25, door=0.4, y=-2.55)
    scene.play(FadeOut(glow), formula.animate.move_to(UP * 2.0), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in machines], lag_ratio=0.1), run_time=1.0)

    beat(scene, t, 3)
    tag = _meaning(scene, formula, B_POW, "k brackets say b", cfg.B_COLOR, machines, "--b-b")

    beat(scene, t, 4)
    tag = _meaning(scene, formula, A_POW, "the rest say a", cfg.A_COLOR, machines, "aabab", old=tag)

    beat(scene, t, 5)
    tag = _meaning(scene, formula, BINOM, "ways to pick which ones", cfg.GOLD, machines, None, old=tag)
    for word in mu.words_with_b(N, 2):
        scene.play(*[m.animate.choose(c) for m, c in zip(machines, word)], run_time=0.38)

    beat(scene, t, 6)
    tag = _meaning(scene, formula, SUM, "collect every k: 0, 1, ..., n", cfg.LIMIT_COLOR, machines, None, old=tag)
    for k in range(N + 1):
        scene.play(*[m.animate.choose(c) for m, c in zip(machines, "a" * (N - k) + "b" * k)], run_time=0.65)

    beat(scene, t, 7)
    chips = VGroup(chip("choose", cfg.B_COLOR, cfg.FONT["body"]), chip("count", cfg.GOLD, cfg.FONT["body"]),
                   chip("collect", cfg.LIMIT_COLOR, cfg.FONT["body"])).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.9)
    scene.play(FadeOut(tag), FadeOut(machines), formula.animate.set_opacity(1), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(c, scale=1.15) for c in chips], lag_ratio=0.35), run_time=1.6)

    # --- Test it at n = 5 ------------------------------------------------------------
    beat(scene, t, 8)
    head = swap_heading(scene, head, "Test it: n = 5")
    five = theorem_tex(str(N), cfg.FONT["section"]).move_to(UP * 2.3)
    scene.play(FadeOut(chips), ReplacementTransform(formula, five), run_time=1.4)
    scene.play(Indicate(five.pieces[SUM], color=cfg.WHITE), run_time=1.0)

    beat(scene, t, 9)
    xs = [(k - N / 2) * 2.45 for k in range(N + 1)]
    columns = VGroup()
    for k, x in zip(range(N + 1), xs):
        parts = [(rf"\binom{{5}}{{{k}}}", "coef")] + [p for p in mu.term_parts(1, N - k, k) if p[1] != "coef"]
        columns.add(colored_tex(parts, cfg.FONT["body"]).move_to([x, 0.25, 0]))
    marker = VGroup(*[txt(f"k = {k}", cfg.FONT["small"], cfg.MUTED).move_to([x, -0.8, 0]) for k, x in enumerate(xs)])
    scene.play(LaggedStart(*[AnimationGroup(TransformFromCopy(VGroup(*five.pieces[BINOM:]), col), FadeIn(mark))
                             for col, mark in zip(columns, marker)], lag_ratio=0.3), run_time=4.0)

    beat(scene, t, 10)
    values = VGroup(*[term_tex(c, N - k, k, cfg.FONT["section"], show_one=True).move_to([x, -1.55, 0])
                      for k, (c, x) in enumerate(zip(mu.coefficients(N), xs))])
    scene.play(FadeOut(marker), run_time=0.4)
    scene.play(LaggedStart(*[TransformFromCopy(col, val) for col, val in zip(columns, values)], lag_ratio=0.2),
               run_time=2.4)

    beat(scene, t, 11)
    result = expansion_tex(N, cfg.FONT["body"]).move_to(DOWN * 2.95)
    scene.play(TransformFromCopy(values, VGroup(*result.terms)), FadeIn(result.lhs), FadeIn(VGroup(*result.pluses)),
               run_time=1.8)
    frame = glow_frame(result, cfg.GREEN, buff=0.15)
    scene.play(Create(frame), run_time=0.8)
    scene.play(Indicate(VGroup(*[c for c in result.coefs if c is not None]), color=cfg.GREEN), run_time=1.0)

    beat(scene, t, 12)
    scene.play(LaggedStart(*[Indicate(col[0], color=cfg.WHITE, scale_factor=1.25) for col in columns],
                           lag_ratio=0.2), run_time=2.4)
    scene.play(LaggedStart(*[Indicate(v[0], color=cfg.GOLD, scale_factor=1.25) for v in values], lag_ratio=0.2),
               run_time=2.4)

    # --- Any n: the middle of (a+b)^10 ----------------------------------------------------
    beat(scene, t, 13)
    head = swap_heading(scene, head, "Any whole-number power")
    scene.play(FadeOut(VGroup(five, columns, values, result, frame)), run_time=0.8)
    ten = colored_tex(lhs_parts(10, sep=r"\;\to\;") + [(r"\binom{10}{5}", "coef"), ("a^{5}", "a"), ("b^{5}", "b"),
                                                     ("=", "op"), (str(mu.choose(10, 5)), "coef"), ("a^{5}", "a"),
                                                     ("b^{5}", "b")], cfg.FONT["title"]).move_to(UP * 1.2)
    scene.play(Write(VGroup(*ten.pieces[:9])), run_time=1.8)
    scene.play(FadeIn(VGroup(*ten.pieces[9:]), shift=LEFT * 0.3), run_time=1.0)
    row10 = VGroup(*[txt(mu.big_number(c), cfg.FONT["body"], cfg.GOLD) for c in mu.coefficients(10)])
    for k, entry in enumerate(row10):
        entry.move_to([(k - 5) * 1.32, -1.3, 0])
    scene.play(LaggedStart(*[FadeIn(e, shift=UP * 0.2) for e in row10], lag_ratio=0.1), run_time=2.0)
    scene.play(Circumscribe(row10[5], color=cfg.GOLD, buff=0.12), Indicate(ten.pieces[10], color=cfg.GOLD),
               run_time=1.4)

    # --- Look at the exponents -------------------------------------------------------------------
    beat(scene, t, 14)
    again = expansion_tex(N, cfg.FONT["title"]).move_to(DOWN * 0.2)
    scene.play(FadeOut(VGroup(ten, row10)), run_time=0.7)
    scene.play(FadeIn(again, shift=UP * 0.2), run_time=1.0)
    exponents = [piece for piece, role in zip(again.pieces, again.roles) if role in "ab"
                 and piece not in again.lhs]
    scene.play(LaggedStart(*[Indicate(p, color=cfg.WHITE, scale_factor=1.3) for p in exponents], lag_ratio=0.12),
               run_time=3.0)
    scene.play(again.animate.scale(1.05), rate_func=there_and_back, run_time=1.4)
    end_scene(scene, t, cfg.SCENE_DURATIONS["07"])
