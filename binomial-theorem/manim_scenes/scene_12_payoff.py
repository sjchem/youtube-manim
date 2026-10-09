"""Chapter 12 — the final payoff.

(a+b)^5 is expanded one last time, now with no multiplication at all: five
machines, six counts, attached powers. The film's chain is then laid out —
expand, choose, count, stack — with the expansion and Pascal's triangle both
growing from one counting structure. A last flourish: with a = 10 and b = 1,
row 4 spells 11^4 = 14641, until carrying breaks the pattern at row 5.
"""

from manim_scenes.common import *
from manim_scenes.scene_07_theorem import theorem_tex

N = 5
XS = [(k - N / 2) * 2.4 for k in range(N + 1)]
CARD_XS = (-5.4, -1.8, 1.8, 5.4)


class Scene12Payoff(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _card(icon: Mobject, x: float) -> VGroup:
    frame = panel(3.0, 2.4, cfg.CYAN, 0.85).move_to([x, 0.7, 0])
    fit_inside(icon, 2.5, 1.9).move_to(frame)
    return VGroup(frame, icon)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "12", "Back to the beginning")

    hero = colored_tex(lhs_parts(N, sep=""), cfg.FONT["hero"]).move_to(UP * 0.1)
    glow = halo(2.8, cfg.GOLD, peak_opacity=0.08).move_to(hero)
    scene.play(FadeIn(glow), Write(hero), run_time=1.6)

    # --- Five machines --------------------------------------------------------
    beat(scene, t, 1)
    lhs = colored_tex(lhs_parts(N, sep=""), cfg.FONT["title"]).move_to(UP * 2.55)
    machines = machine_row(N, width=2.1, height=1.2, door=0.38, y=1.2)
    scene.play(FadeOut(glow), ReplacementTransform(hero, lhs), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.2) for m in machines], lag_ratio=0.1), run_time=1.0)
    for word in ("abaab", "bbaba"):
        scene.play(*[m.animate.choose(c) for m, c in zip(machines, word)], run_time=0.6)

    # --- Count the ways for each number of b's ---------------------------------------
    beat(scene, t, 2)
    binoms = VGroup(*[eq(rf"\binom{{5}}{{{k}}}", cfg.FONT["section"], cfg.GOLD).move_to([x, -0.6, 0])
                      for k, x in enumerate(XS)])
    scene.play(*[m.animate.reset() for m in machines],
               LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in binoms], lag_ratio=0.12), run_time=1.6)

    beat(scene, t, 3)
    counts = VGroup(*[txt(str(mu.choose(N, k)), cfg.FONT["title"], cfg.GOLD).move_to([x, -0.6, 0])
                      for k, x in enumerate(XS)])
    for k in range(N + 1):
        scene.play(*[m.animate.choose(c) for m, c in zip(machines, "a" * (N - k) + "b" * k)],
                   ReplacementTransform(binoms[k], counts[k]), run_time=1.15)

    beat(scene, t, 4)
    terms = VGroup(*[term_tex(c, N - k, k, cfg.FONT["section"], show_one=True).move_to([x, -0.6, 0])
                     for k, (c, x) in enumerate(zip(mu.coefficients(N), XS))])
    scene.play(*[m.animate.reset() for m in machines],
               *[ReplacementTransform(counts[k], terms[k]) for k in range(N + 1)], run_time=1.6)
    scene.play(LaggedStart(*[Indicate(VGroup(*term[1:]), color=cfg.WHITE) for term in terms], lag_ratio=0.12),
               run_time=1.6)

    beat(scene, t, 5)
    result = expansion_tex(N, cfg.FONT["section"]).move_to(DOWN * 2.45)
    scene.play(TransformFromCopy(terms, VGroup(*result.terms)), FadeIn(result.lhs), FadeIn(VGroup(*result.pluses)),
               run_time=1.8)
    frame = glow_frame(result, cfg.GREEN, buff=0.15)
    tick = check_mark(0.3).next_to(frame, DOWN, buff=0.2)
    scene.play(Create(frame), Create(tick), run_time=1.0)
    scene.play(Indicate(result, color=cfg.GREEN, scale_factor=1.03), run_time=1.2)

    # --- The chain: expand -> choose -> count -> stack --------------------------------------
    beat(scene, t, 6)
    head = swap_heading(scene, head, "The picture behind it")
    scene.play(FadeOut(VGroup(lhs, machines, terms, result, frame, tick)), run_time=0.9)
    icons = [
        colored_tex(lhs_parts(N, sep=""), cfg.FONT["section"]),
        choice_list("aabab", 0.42),
        eq(r"\binom{5}{2}", cfg.FONT["title"], cfg.GOLD),
        pascal_triangle(5, pitch_x=0.52, pitch_y=0.4, top=ORIGIN, size=cfg.FONT["small"]),
    ]
    words = [("expand", cfg.WHITE), ("choose", cfg.B_COLOR), ("count", cfg.GOLD), ("stack", cfg.GOLD)]
    cards = [_card(icon, x) for icon, x in zip(icons, CARD_XS)]
    labels = [txt(w, cfg.FONT["title"], c).move_to([x, -1.15, 0]) for (w, c), x in zip(words, CARD_XS)]
    arrows = [Arrow([CARD_XS[i] + 1.5, 0.7, 0], [CARD_XS[i + 1] - 1.5, 0.7, 0], buff=0.05, color=cfg.CYAN,
                    stroke_width=6, max_tip_length_to_length_ratio=0.45) for i in range(3)]

    for index, i in zip((7, 8, 9, 10), range(4)):
        beat(scene, t, index)
        anims = [FadeIn(cards[i], shift=UP * 0.2), FadeIn(labels[i], shift=UP * 0.15)]
        if i:
            anims.append(GrowArrow(arrows[i - 1]))
        scene.play(*anims, run_time=1.1)
        scene.play(Indicate(cards[i][1], color=cfg.WHITE, scale_factor=1.08), run_time=0.9)

    # --- One structure underneath both ------------------------------------------------------------
    beat(scene, t, 11)
    root = chip("one counting structure", cfg.GOLD, cfg.FONT["title"]).move_to(DOWN * 2.95)
    feeds = VGroup(
        CurvedArrow(root.get_left() + LEFT * 0.1, cards[0][0].get_corner(DR) + UP * 0.1 + LEFT * 0.25, angle=-0.6,
                    color=cfg.GOLD, stroke_width=5),
        CurvedArrow(root.get_right() + RIGHT * 0.1, cards[3][0].get_corner(DL) + UP * 0.1 + RIGHT * 0.25, angle=0.6,
                    color=cfg.GOLD, stroke_width=5),
    )
    scene.play(FadeIn(root, scale=1.1), run_time=1.0)
    scene.play(Create(feeds), run_time=1.4)
    scene.play(Indicate(cards[0], color=cfg.GOLD, scale_factor=1.05), Indicate(cards[3], color=cfg.GOLD,
                                                                              scale_factor=1.05), run_time=1.4)

    # --- 11^4 = 14641 ---------------------------------------------------------------------------------
    beat(scene, t, 12)
    head = swap_heading(scene, head, "One last trick")
    scene.play(FadeOut(VGroup(*cards, *labels, *arrows, root, feeds)), run_time=0.8)
    eleven = colored_tex([("(", "op"), ("10", "a"), ("+", "op"), ("1", "b"), (")^{4}", "op"), ("=", "op"),
                          ("11^{4}", "op")], cfg.FONT["hero"]).move_to(UP * 1.9)
    scene.play(Write(eleven), run_time=1.8)

    beat(scene, t, 13)
    row4 = VGroup(*[txt(str(c), cfg.FONT["title"], cfg.GOLD) for c in mu.coefficients(4)]).arrange(RIGHT, buff=0.8)
    row4.move_to(UP * 0.35)
    digits = VGroup(*[txt(d, cfg.FONT["hero"], cfg.GOLD) for d in str(11 ** 4)]).arrange(RIGHT, buff=0.06)
    prefix = colored_tex([("11^{4}", "op"), ("=", "op")], cfg.FONT["hero"])
    answer = VGroup(prefix, digits).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.25)
    scene.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.15) for x in row4], lag_ratio=0.15), run_time=1.2)
    # One group-to-group transform keeps "14641" a single number rather than five loose labels.
    scene.play(FadeIn(prefix), TransformFromCopy(row4, digits), run_time=1.8)
    scene.play(Circumscribe(digits, color=cfg.GOLD, buff=0.12), run_time=1.2)

    beat(scene, t, 14)
    head = swap_heading(scene, head, "Now carry the tens")
    row5 = VGroup(*[txt(str(c), cfg.FONT["body"], cfg.ORANGE if c >= 10 else cfg.GOLD) for c in mu.coefficients(5)])
    row5.arrange(RIGHT, buff=0.42).move_to([-3.4, -3.15, 0])
    carry = colored_tex([("11^{5}", "op"), ("=", "op"), (str(11 ** 5), "coef")], cfg.FONT["section"])
    carry.move_to([3.6, -3.15, 0])
    # The coefficients are place-value contributions; carrying produces the
    # number. An inequality between a coefficient list and an equation would
    # suggest the binomial identity itself has stopped working.
    carry_arrow = Arrow([-0.25, -3.15, 0], [0.75, -3.15, 0], buff=0,
                        color=cfg.ORANGE, stroke_width=5)
    scene.play(FadeIn(row5, shift=UP * 0.15), FadeIn(carry, shift=UP * 0.15), run_time=1.0)
    scene.play(GrowArrow(carry_arrow), *[Indicate(e, color=cfg.ORANGE) for e in row5 if e.text == "10"],
               run_time=1.2)

    # --- The whole story in one line ----------------------------------------------------------------------
    beat(scene, t, 15)
    head = swap_heading(scene, head, "Every coefficient counts choices")
    scene.play(FadeOut(VGroup(eleven, row4, answer, row5, carry, carry_arrow)), run_time=0.8)
    formula = theorem_tex().move_to(UP * 0.7)
    shine = halo(4.4, cfg.GOLD, peak_opacity=0.07).move_to(formula)
    scene.play(FadeIn(shine), Write(formula), run_time=2.2)
    braces = VGroup(
        count_brace(formula.pieces[7], "ways to choose", cfg.GOLD, size=cfg.FONT["body"]),
    )
    braces[0].next_to(formula, DOWN, buff=0.15).set_x(formula.pieces[7].get_x())
    scene.play(FadeIn(braces, shift=UP * 0.15), run_time=1.0)
    scene.play(Indicate(formula.pieces[7], color=cfg.GOLD, scale_factor=1.2), run_time=1.2)
    moral = caption("Every coefficient counts choices.", cfg.GOLD, cfg.FONT["title"], y=-3.1)
    scene.play(FadeIn(moral, shift=UP * 0.15), run_time=1.0)
    scene.play(Circumscribe(formula, color=cfg.GOLD, buff=0.15), run_time=1.6)
    scene.play(formula.animate.scale(1.04), rate_func=there_and_back, run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["12"])
