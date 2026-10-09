"""Chapter 4 — the triangle builds itself.

The expansions of (a+b)^0 ... (a+b)^5 are stacked with their equals signs
aligned. Stripping the letters leaves only the coefficients, and they settle
into Pascal's triangle. The chapter then gives the algebraic reason for the
addition rule: (a+b)^5 = (a+b)^4 * a + (a+b)^4 * b, and the "times b" copy is
the same row slid one place along — so adding the copies adds neighbours.
"""

from manim_scenes.common import *

ROWS = 6
ROW_Y = [2.65 - 0.92 * n for n in range(ROWS)]
EQUALS_X = -3.2
COLUMN = 2.2                     # spacing of the term columns in the shifted-copy demo
COLUMN_SHIFT = 0.45


class Scene04TriangleBuilds(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _stack_line(n: int) -> MathTex:
    """(a+b)^n = ... with its equals sign on a shared vertical line."""
    line = expansion_tex(n, cfg.FONT["body"])
    equals = line.lhs[-1]
    line.shift([EQUALS_X - equals.get_center()[0], ROW_Y[n] - line.get_center()[1], 0])
    return line


def _column_x(k: int) -> float:
    return COLUMN_SHIFT + (k - 2.5) * COLUMN


def _term_row(coefs, a_total: int, start_k: int, y: float, size: int | None = None) -> VGroup:
    """Terms c * a^(a_total - j) b^(j + start_k)... laid out in the k columns."""
    row = VGroup()
    row.by_k = {}
    for j, c in enumerate(coefs):
        k = j + start_k
        term = term_tex(c, a_total - k, k, size or cfg.FONT["body"]).move_to([_column_x(k), y, 0])
        row.add(term)
        row.by_k[k] = term
    return row


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "04", "Line them up")

    # --- One power at a time ---------------------------------------------------
    lines = [_stack_line(n) for n in range(ROWS)]
    for n, index in zip(range(4), (1, 2, 3, 4)):
        beat(scene, t, index)
        scene.play(FadeIn(lines[n].lhs, shift=RIGHT * 0.3), run_time=0.6)
        scene.play(LaggedStart(*[FadeIn(VGroup(term, *([lines[n].pluses[k - 1]] if k else [])), shift=LEFT * 0.2)
                                 for k, term in enumerate(lines[n].terms)], lag_ratio=0.3), run_time=1.2)
        written = [c for c in lines[n].coefs if c is not None]
        if written:
            scene.play(*[Indicate(c, color=cfg.GOLD, scale_factor=1.4) for c in written], run_time=0.7)
        else:  # (a+b)^1: both coefficients are unwritten 1s
            scene.play(Indicate(lines[n].terms[0]), Indicate(lines[n].terms[1]), run_time=0.7)

    beat(scene, t, 5)
    for n in (4, 5):
        scene.play(FadeIn(lines[n].lhs, shift=RIGHT * 0.3), run_time=0.5)
        scene.play(LaggedStart(*[FadeIn(VGroup(term, *([lines[n].pluses[k - 1]] if k else [])), shift=LEFT * 0.2)
                                 for k, term in enumerate(lines[n].terms)], lag_ratio=0.2), run_time=1.6)

    # --- Strip away the algebra ---------------------------------------------------------
    beat(scene, t, 6)
    triangle = pascal_triangle(ROWS, pitch_x=1.35, pitch_y=0.92, top=UP * ROW_Y[0], size=cfg.FONT["section"])
    moves, fades = [], []
    for n, line in enumerate(lines):
        fades += [line.lhs, *line.pluses]
        for k, term in enumerate(line.terms):
            target = triangle.entries[(n, k)]
            coef = line.coefs[k]
            if coef is None:
                moves.append(ReplacementTransform(term, target))
            else:
                fades += [piece for piece in term if piece is not coef]
                moves.append(ReplacementTransform(coef, target))
    scene.play(*[FadeOut(m) for m in fades], run_time=0.9)
    scene.play(*moves, run_time=2.2)

    beat(scene, t, 7)
    head = swap_heading(scene, head, "Pascal's triangle")
    scene.play(LaggedStart(*[Indicate(triangle_row(triangle, n), color=cfg.WHITE, scale_factor=1.08)
                             for n in range(ROWS)], lag_ratio=0.25), run_time=2.6)
    scene.play(triangle.animate.set_color(cfg.GOLD), Flash(triangle.entries[(0, 0)], color=cfg.GOLD), run_time=0.8)

    # --- The addition rule ------------------------------------------------------------------
    beat(scene, t, 8)
    for (n, k) in ((4, 2), (5, 2)):
        left, right, below = triangle.entries[(n - 1, k - 1)], triangle.entries[(n - 1, k)], triangle.entries[(n, k)]
        feeds = VGroup(arrow_between(left.get_bottom(), below.get_top() + LEFT * 0.15, cfg.CYAN, 5),
                       arrow_between(right.get_bottom(), below.get_top() + RIGHT * 0.15, cfg.CYAN, 5))
        scene.play(GrowArrow(feeds[0]), GrowArrow(feeds[1]), Indicate(left, color=cfg.WHITE),
                   Indicate(right, color=cfg.WHITE), run_time=1.2)
        scene.play(Indicate(below, color=cfg.GREEN, scale_factor=1.5), run_time=0.9)
        scene.play(FadeOut(feeds), run_time=0.5)

    # --- Why? Multiply by one more bracket ------------------------------------------------------
    beat(scene, t, 9)
    head = swap_heading(scene, head, "Why does adding work?")
    scene.play(triangle.animate.scale(0.42).move_to([6.0, 2.0, 0]).set_opacity(cfg.CONTEXT_OPACITY), run_time=1.2)

    beat(scene, t, 10)
    recipe = colored_tex(lhs_parts(5) + lhs_parts(4, sep=r"\cdot")[:] + [("(", "op"), ("a", "a"), ("+", "op"),
                                                                         ("b", "b"), (")", "op")],
                         cfg.FONT["body"]).move_to([-1.3, 2.6, 0])
    scene.play(Write(recipe), run_time=1.4)
    row4 = _term_row(mu.coefficients(4), 4, 0, 1.45)
    scene.play(LaggedStart(*[FadeIn(term, shift=DOWN * 0.2) for term in row4], lag_ratio=0.15), run_time=1.4)

    # --- Times a: same place, one more a ---------------------------------------------------------
    beat(scene, t, 11)
    times_a_label = colored_tex([(r"\times", "op"), ("a", "a")], cfg.FONT["body"]).move_to([-7.0, 0.35, 0])
    times_a = _term_row(mu.coefficients(4), 5, 0, 0.35)
    scene.play(FadeIn(times_a_label, shift=RIGHT * 0.2), run_time=0.6)
    scene.play(*[TransformFromCopy(row4[j], times_a[j]) for j in range(5)], run_time=1.6)

    # --- Times b: one more b, slid one place along ------------------------------------------------
    beat(scene, t, 12)
    times_b_label = colored_tex([(r"\times", "op"), ("b", "b")], cfg.FONT["body"]).move_to([-7.0, -0.75, 0])
    times_b = _term_row(mu.coefficients(4), 5, 1, -0.75)
    in_place = VGroup(*[term_tex(c, 4 - j, j + 1, cfg.FONT["body"]).move_to([_column_x(j), -0.75, 0])
                        for j, c in enumerate(mu.coefficients(4))])
    scene.play(FadeIn(times_b_label, shift=RIGHT * 0.2), run_time=0.6)
    scene.play(*[TransformFromCopy(row4[j], in_place[j]) for j in range(5)], run_time=1.4)
    scene.play(*[ReplacementTransform(in_place[j], times_b[j]) for j in range(5)], run_time=1.4, rate_func=smooth)
    slide = Arrow([_column_x(0) - 0.4, -1.4, 0], [_column_x(1) - 0.4, -1.4, 0], buff=0, color=cfg.B_COLOR,
                  stroke_width=6, max_tip_length_to_length_ratio=0.25)
    scene.play(GrowArrow(slide), run_time=0.7)

    # --- Add the copies -------------------------------------------------------------------------------
    beat(scene, t, 13)
    rule = Line([_column_x(0) - 1.0, -1.75, 0], [_column_x(5) + 1.0, -1.75, 0], stroke_color=cfg.MUTED, stroke_width=3)
    plus = eq("+", cfg.FONT["body"], cfg.MUTED).move_to([-7.0, -1.4, 0])
    scene.play(FadeOut(slide), Create(rule), FadeIn(plus), run_time=0.9)
    columns = [VGroup(*[row.by_k[k] for row in (times_a, times_b) if k in row.by_k]) for k in range(6)]
    scene.play(LaggedStart(*[Indicate(col, color=cfg.WHITE, scale_factor=1.06) for col in columns], lag_ratio=0.2),
               run_time=2.4)

    beat(scene, t, 14)
    times_a_coefs, times_b_coefs, sums = mu.shifted_copies(mu.coefficients(4))
    sum_labels = VGroup()
    for k in range(6):
        pieces = [str(v) for v in (times_a_coefs[k], times_b_coefs[k]) if v]
        sum_labels.add(txt(" + ".join(pieces), cfg.FONT["label"], cfg.GOLD).move_to([_column_x(k), -2.3, 0]))
    for label in sum_labels:
        scene.play(FadeIn(label, shift=DOWN * 0.2), run_time=0.95)

    beat(scene, t, 15)
    row5 = _term_row(sums, 5, 0, -3.3, cfg.FONT["body"])
    scene.play(*[ReplacementTransform(sum_labels[k], row5[k][0] if sums[k] != 1 else row5[k]) for k in range(6)],
               *[FadeIn(VGroup(*row5[k][1:])) for k in range(6) if sums[k] != 1], run_time=1.6)
    frame = glow_frame(row5, cfg.GREEN, buff=0.14)
    scene.play(Create(frame), triangle.animate.set_opacity(1), run_time=1.0)
    scene.play(Indicate(triangle_row(triangle, 5), color=cfg.GREEN, scale_factor=1.2), run_time=1.0)

    # --- But why ten? -----------------------------------------------------------------------------------
    beat(scene, t, 16)
    ten = row5[2]
    others = VGroup(recipe, row4, times_a, times_b, times_a_label, times_b_label, plus, rule,
                    *[row5[k] for k in range(6) if k != 2], frame)
    scene.play(FadeOut(others), triangle.animate.set_opacity(cfg.CONTEXT_OPACITY), ten.animate.scale(1.5).move_to([0, -0.4, 0]),
               run_time=1.4)
    why = txt("?", cfg.FONT["hero"], cfg.ORANGE).next_to(ten, RIGHT, buff=0.5)
    scene.play(FadeIn(why, scale=1.5), Indicate(ten, color=cfg.GOLD), run_time=1.0)

    beat(scene, t, 17)
    head = swap_heading(scene, head, "Choose from each bracket")
    machine = ChoiceMachine(width=2.8, height=1.7, door=0.55).move_to(DOWN * 0.4)
    scene.play(FadeOut(VGroup(triangle, why)), ReplacementTransform(ten, machine), run_time=1.2)
    for letter in ("a", "b", "a", "b", "a", "b", "a", "b"):
        scene.play(machine.animate.choose(letter), run_time=0.55)
    scene.play(machine.animate.reset(), run_time=0.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["04"])
