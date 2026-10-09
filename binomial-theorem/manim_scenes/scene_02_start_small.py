"""Chapter 2 — start small.

(a+b)^0 and (a+b)^1 are read off directly. (a+b)^2 is drawn as a square of
side a + b: two of its four regions are a-by-b rectangles of equal area, and
sliding them together is where the coefficient 2 comes from. The algebra
then tells the same story — ab and ba are two different choice lists that
multiply to the same product.
"""

from manim_scenes.common import *

A, B = 2.6, 1.6                      # drawn lengths of a and b
X0, Y0 = -1.2, 2.2                   # lift the square clear of the coefficient row
COLUMN_X = -7.2                      # left edge of the little stack of expansions


class Scene02StartSmall(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _region(width: float, height: float, center, color) -> Rectangle:
    return Rectangle(width=width, height=height, stroke_color=cfg.WHITE, stroke_width=3,
                     fill_color=color, fill_opacity=0.0).move_to(center)


def _side_brace(p1, p2, direction, tex_parts) -> VGroup:
    brace = BraceBetweenPoints(p1, p2, direction=direction, color=cfg.MUTED)
    label = colored_tex(tex_parts, cfg.FONT["label"])
    label.next_to(brace, direction, buff=0.12)
    return VGroup(brace, label)


def _ab_label() -> MathTex:
    return colored_tex([("a", "a"), ("b", "b")], cfg.FONT["section"])


def _cube_sketch(side: float = 2.4) -> VGroup:
    """A flat drawing of a cube, to hand over to chapter 3's real 3D cube."""
    depth = np.array([0.9, 0.7, 0])
    front = Square(side, stroke_color=cfg.WHITE, stroke_width=4)
    back = front.copy().shift(depth).set_stroke(cfg.MUTED, 3, 0.7)
    edges = VGroup(*[Line(front.get_corner(c), front.get_corner(c) + depth, stroke_color=cfg.MUTED,
                          stroke_width=3, stroke_opacity=0.7) for c in (UL, UR, DL, DR)])
    return VGroup(back, edges, front)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "02", "Start small")

    hero = colored_tex(lhs_parts(5, sep=""), cfg.FONT["title"]).move_to(UP * 0.3)
    scene.play(FadeIn(hero, scale=0.9), run_time=1.0)
    scene.play(hero.animate.scale(0.5).set_opacity(cfg.CONTEXT_OPACITY), run_time=1.6)

    # --- Powers zero and one ------------------------------------------------
    beat(scene, t, 1)
    line0 = expansion_tex(0, cfg.FONT["body"])
    line0.move_to([COLUMN_X + line0.width / 2, 2.6, 0])
    scene.play(FadeOut(hero), FadeIn(line0, shift=RIGHT * 0.3), run_time=1.0)
    scene.play(Circumscribe(line0.coefs[0], color=cfg.GOLD, buff=0.08), run_time=1.0)

    beat(scene, t, 2)
    line1 = expansion_tex(1, cfg.FONT["body"], coefs=["1", "1"])
    line1.move_to([COLUMN_X + line1.width / 2, 1.75, 0])
    scene.play(FadeIn(line1, shift=RIGHT * 0.3), run_time=1.0)
    scene.play(*[Circumscribe(c, color=cfg.GOLD, buff=0.08) for c in line1.coefs], run_time=1.0)

    # --- A square of side a + b ---------------------------------------------
    beat(scene, t, 3)
    head = swap_heading(scene, head, "Squaring: an area picture")
    side = A + B
    outline = Square(side, stroke_color=cfg.WHITE, stroke_width=4).move_to([X0 + side / 2, Y0 - side / 2, 0])
    top_whole = _side_brace([X0, Y0, 0], [X0 + side, Y0, 0], UP, [("a", "a"), ("+", "op"), ("b", "b")])
    left_whole = _side_brace([X0, Y0 - side, 0], [X0, Y0, 0], LEFT, [("a", "a"), ("+", "op"), ("b", "b")])
    scene.play(Create(outline), run_time=1.2)
    scene.play(FadeIn(top_whole, shift=DOWN * 0.15), FadeIn(left_whole, shift=RIGHT * 0.15), run_time=1.0)

    beat(scene, t, 4)
    cuts = VGroup(
        DashedLine([X0 + A, Y0, 0], [X0 + A, Y0 - side, 0], color=cfg.MUTED, stroke_width=3),
        DashedLine([X0, Y0 - A, 0], [X0 + side, Y0 - A, 0], color=cfg.MUTED, stroke_width=3),
    )
    top_split = VGroup(_side_brace([X0, Y0, 0], [X0 + A, Y0, 0], UP, [("a", "a")]),
                       _side_brace([X0 + A, Y0, 0], [X0 + side, Y0, 0], UP, [("b", "b")]))
    left_split = VGroup(_side_brace([X0, Y0 - A, 0], [X0, Y0, 0], LEFT, [("a", "a")]),
                        _side_brace([X0, Y0 - side, 0], [X0, Y0 - A, 0], LEFT, [("b", "b")]))
    scene.play(Create(cuts), run_time=1.0)
    scene.play(ReplacementTransform(top_whole, top_split), ReplacementTransform(left_whole, left_split), run_time=1.2)

    aa = _region(A, A, [X0 + A / 2, Y0 - A / 2, 0], cfg.A_COLOR)
    stand = _region(B, A, [X0 + A + B / 2, Y0 - A / 2, 0], mix_color(1, 2))
    lie = _region(A, B, [X0 + A / 2, Y0 - A - B / 2, 0], mix_color(1, 2))
    bb = _region(B, B, [X0 + A + B / 2, Y0 - A - B / 2, 0], cfg.B_COLOR)
    scene.add(aa, stand, lie, bb)
    scene.remove(outline, cuts)

    # --- a squared and b squared --------------------------------------------
    beat(scene, t, 5)
    a_sq = term_tex(1, 2, 0, cfg.FONT["section"]).move_to(aa)
    b_sq = term_tex(1, 0, 2, cfg.FONT["section"]).move_to(bb)
    scene.play(aa.animate.set_fill(cfg.A_COLOR, 0.35), Write(a_sq), run_time=1.2)
    scene.play(bb.animate.set_fill(cfg.B_COLOR, 0.22), Write(b_sq), run_time=1.2)

    # --- Two a-by-b rectangles ----------------------------------------------
    beat(scene, t, 6)
    stand_label = _ab_label().move_to(stand)
    lie_label = _ab_label().move_to(lie)
    scene.play(stand.animate.set_fill(mix_color(1, 2), 0.45), lie.animate.set_fill(mix_color(1, 2), 0.45),
               Write(stand_label), Write(lie_label), run_time=1.4)
    ghost = stand.copy().set_fill(opacity=0.15).set_stroke(cfg.GREEN, 5)
    scene.play(Rotate(ghost, PI / 2), run_time=1.0)
    scene.play(ghost.animate.move_to(lie), run_time=1.0)
    scene.play(Indicate(ghost, color=cfg.GREEN, scale_factor=1.04), run_time=0.8)
    scene.play(FadeOut(ghost), run_time=0.5)

    # --- Slide them together: two copies of ab -------------------------------
    beat(scene, t, 7)
    stack_x = 5.45
    scene.play(
        lie.animate.move_to([stack_x, 0.55, 0]), lie_label.animate.move_to([stack_x, 0.55, 0]),
        Rotate(stand, PI / 2), stand_label.animate.move_to([stack_x, -1.15, 0]),
        run_time=1.0,
    )
    scene.play(stand.animate.move_to([stack_x, -1.15, 0]), run_time=0.8)
    two_ab = term_tex(2, 1, 1, cfg.FONT["section"]).next_to(VGroup(lie, stand), DOWN, buff=0.3)
    scene.play(TransformFromCopy(VGroup(lie_label, stand_label), two_ab), run_time=1.0)

    # --- (a+b)^2 = a^2 + 2ab + b^2 --------------------------------------------
    beat(scene, t, 8)
    eq2 = expansion_tex(2, cfg.FONT["body"]).move_to(DOWN * 3.5)
    scene.play(
        TransformFromCopy(a_sq, eq2.terms[0]), TransformFromCopy(two_ab, eq2.terms[1]),
        TransformFromCopy(b_sq, eq2.terms[2]), FadeIn(eq2.lhs), FadeIn(VGroup(*eq2.pluses)),
        run_time=1.6,
    )
    ones = VGroup(*[txt(str(c), cfg.FONT["label"], cfg.GOLD) for c in mu.coefficients(2)])
    for k, one in enumerate(ones):
        one.next_to(eq2.terms[k], UP, buff=0.22)
    # Exponents make the term heights differ; keep 1, 2, 1 on one baseline.
    coefficient_y = max(one.get_y() for one in ones)
    for one in ones:
        one.set_y(coefficient_y)
    scene.play(LaggedStart(*[FadeIn(o, shift=DOWN * 0.15) for o in ones], lag_ratio=0.3), run_time=1.2)

    # --- The algebra agrees ---------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(VGroup(aa, stand, lie, bb, a_sq, b_sq, stand_label, lie_label, two_ab,
                              top_split, left_split, line0, line1, ones)),
               eq2.animate.move_to(DOWN * 2.05), run_time=1.0)
    head = swap_heading(scene, head, "Every term meets every term")
    product = colored_tex(lhs_parts(1, sep="")[:-1] + [(")", "op")] + lhs_parts(1, sep="")[:-1] + [(")", "op")],
                          cfg.FONT["hero"]).move_to(UP * 1.7)
    a1, b1, a2, b2 = product.pieces[1], product.pieces[3], product.pieces[6], product.pieces[8]
    scene.play(FadeIn(product, shift=DOWN * 0.2), run_time=1.0)
    pairs = [(a1, a2, "aa"), (a1, b2, "ab"), (b1, a2, "ba"), (b1, b2, "bb")]
    arcs = VGroup()
    for first, second, word in pairs:
        above = word[0] == "a"
        arc = ArcBetweenPoints(
            (first.get_top() if above else first.get_bottom()) + (UP if above else DOWN) * 0.1,
            (second.get_top() if above else second.get_bottom()) + (UP if above else DOWN) * 0.1,
            # Lower the expression to clear the heading; shallower lower arcs
            # keep the choice tiles below it clear as well.
            angle=-PI / 2 if above else PI / 4, stroke_color=mix_color(word.count("b"), 2), stroke_width=4)
        arcs.add(arc)
    scene.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.3), run_time=1.8)

    beat(scene, t, 10)
    lists = VGroup(*[choice_list(word, 0.72) for _, _, word in pairs])
    terms = VGroup(*[colored_tex([(letter, letter) for letter in word], cfg.FONT["section"]) for _, _, word in pairs])
    for index, (lst, term) in enumerate(zip(lists, terms)):
        x = (index - 1.5) * 3.2
        lst.move_to([x, 0.45, 0])
        term.move_to([x, -0.6, 0])
    for arc, lst, term in zip(arcs, lists, terms):
        scene.play(Indicate(arc, color=cfg.WHITE), FadeIn(lst, shift=DOWN * 0.2), FadeIn(term, shift=DOWN * 0.2),
                   run_time=1.0)
    # Once the arcs disappear, lift the brackets again to leave room for the
    # two choice lists when they stack together in the following beat.
    scene.play(FadeOut(arcs), product.animate.move_to(UP * 2.1).set_opacity(cfg.CONTEXT_OPACITY), run_time=0.6)

    # --- ab and ba merge -------------------------------------------------------
    beat(scene, t, 11)
    ba = terms[2]
    scene.play(Swap(ba.pieces[0], ba.pieces[1]), run_time=0.9)
    scene.play(Indicate(VGroup(terms[1], terms[2]), color=cfg.WHITE), run_time=0.8)
    merged = term_tex(2, 1, 1, cfg.FONT["section"]).move_to([0, -0.6, 0])
    scene.play(
        lists[0].animate.move_to([-4.6, 0.45, 0]), terms[0].animate.move_to([-4.6, -0.6, 0]),
        lists[3].animate.move_to([4.6, 0.45, 0]), terms[3].animate.move_to([4.6, -0.6, 0]),
        lists[1].animate.move_to([0, 0.85, 0]), lists[2].animate.move_to([0, 0.05, 0]),
        ReplacementTransform(VGroup(terms[1], terms[2]), merged),
        run_time=1.4,
    )
    merged.next_to(lists[2], DOWN, buff=0.35)
    scene.play(Indicate(merged.pieces[0], color=cfg.GOLD, scale_factor=1.4), run_time=0.9)

    # --- The 2 counts something ----------------------------------------------
    beat(scene, t, 12)
    pair_frame = glow_frame(VGroup(lists[1], lists[2]), cfg.GOLD, buff=0.16)
    ways = txt("2 ways", cfg.FONT["body"], cfg.GOLD).next_to(pair_frame, RIGHT, buff=0.4)
    scene.play(Create(pair_frame), run_time=0.8)
    scene.play(FadeIn(ways, shift=LEFT * 0.2), run_time=0.7)
    scene.play(TransformFromCopy(ways, eq2.terms[1]), run_time=1.0)
    scene.play(Indicate(eq2.coefs[1], color=cfg.GOLD, scale_factor=1.5), run_time=1.0)

    beat(scene, t, 13)
    takeaway = caption("Coefficients count choices.", cfg.GOLD, cfg.FONT["title"], y=-3.35)
    scene.play(FadeIn(takeaway, scale=1.1), run_time=1.0)
    scene.play(Circumscribe(takeaway, color=cfg.GOLD, buff=0.15), run_time=1.4)

    # --- Next: one more dimension ---------------------------------------------
    beat(scene, t, 14)
    scene.play(FadeOut(VGroup(product, lists, terms[0], terms[3], merged, pair_frame, ways, eq2, takeaway)),
               run_time=0.8)
    flat = Square(2.4, stroke_color=cfg.WHITE, stroke_width=4).move_to(DOWN * 0.2)
    cube = _cube_sketch(2.4).move_to(DOWN * 0.2)
    scene.play(Create(flat), run_time=0.8)
    scene.play(ReplacementTransform(flat, cube[2]), FadeIn(cube[0]), Create(cube[1]), run_time=1.4)
    scene.play(Rotate(cube, 0.25, axis=UP), rate_func=there_and_back, run_time=1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["02"])
