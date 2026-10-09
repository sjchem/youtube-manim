"""Chapter 10 — paths through the triangle.

Pascal's triangle becomes a maze: from the apex, each step goes down-left (a)
or down-right (b). A route of five steps is a choice list, and where it ends
depends only on how many b's it took. The ten routes into the 10 are drawn one
by one; the 4 that arrive from the upper-left (last step b) and the 6 from the
upper-right (last step a) show Pascal's rule a third time.
"""

from manim_scenes.common import *

N, K = 5, 2
TOP = np.array([-1.7, 2.55, 0.0])
PX, PY = 1.45, 0.98
NODE_R = 0.36
LIST_X, LIST_TOP, LIST_STEP, LIST_CELL = 5.35, 2.45, 0.5, 0.36


class Scene10Paths(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def point_of(n: int, k: int) -> np.ndarray:
    return pascal_point(n, k, PX, PY, TOP)


def _node(n: int, k: int) -> VGroup:
    disc = Circle(radius=NODE_R, stroke_color=cfg.MUTED, stroke_width=3, fill_color=cfg.PANEL, fill_opacity=1)
    group = VGroup(disc).move_to(point_of(n, k))
    group.disc = disc
    group.set_z_index(2)
    return group


def _value(n: int, k: int, value: int | str, color: str = cfg.GOLD) -> Text:
    label = txt(str(value), cfg.FONT["label"], color)
    label.scale_to_fit_height(min(label.height, NODE_R * 0.95)).move_to(point_of(n, k))
    label.set_z_index(3)
    return label


def _walk(scene, ball, word: str, step_time: float, on_step=None) -> VGroup:
    """Move the ball down a route, leaving a glowing trail; returns the trail."""
    trail = VGroup()
    cells = mu.path_cells(word)
    for i, ((n0, k0), (n1, k1)) in enumerate(zip(cells, cells[1:])):
        seg = glow_line(point_of(n0, k0), point_of(n1, k1), ROLE_COLORS[word[i]], 6).set_z_index(1)
        extra = on_step(i) if on_step else []
        scene.play(Create(seg), ball.animate.move_to(point_of(n1, k1)), *extra, run_time=step_time)
        trail.add(seg)
    return trail


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "10", "Turn the triangle into a maze")

    nodes = {(n, k): _node(n, k) for n in range(N + 1) for k in range(n + 1)}
    scene.play(LaggedStart(*[GrowFromCenter(nodes[(n, k)]) for n in range(N + 1) for k in range(n + 1)],
                           lag_ratio=0.05), run_time=2.2)
    ball = glow_dot(point_of(0, 0), 0.16, cfg.WHITE).set_z_index(5)
    scene.play(FadeIn(ball, scale=0.4), run_time=0.6)

    # --- Two moves at every row -----------------------------------------------------
    beat(scene, t, 1)
    edges = VGroup(glow_line(point_of(0, 0), point_of(1, 0), cfg.A_COLOR, 6),
                   glow_line(point_of(0, 0), point_of(1, 1), cfg.B_COLOR, 6)).set_z_index(1)
    # A large legend beside the maze, so the two moves read on a phone.
    hub = np.array([LIST_X, 1.6, 0])
    left = Arrow(hub, hub + np.array([-1.3, -1.6, 0]), buff=0, color=cfg.A_COLOR, stroke_width=9)
    right = Arrow(hub, hub + np.array([1.3, -1.6, 0]), buff=0, color=cfg.B_COLOR, stroke_width=9)
    scene.play(Create(edges), GrowArrow(left), GrowArrow(right), run_time=1.0)
    scene.play(Indicate(edges, color=cfg.WHITE), run_time=1.0)

    beat(scene, t, 2)
    a_tag = eq("a", cfg.FONT["hero"], cfg.A_COLOR).next_to(left.get_end(), DOWN, buff=0.2)
    b_tag = eq("b", cfg.FONT["hero"], cfg.B_COLOR).next_to(right.get_end(), DOWN, buff=0.2)
    scene.play(FadeIn(a_tag, scale=1.3), FadeIn(b_tag, scale=1.3), run_time=0.9)

    # --- One walk is one choice list --------------------------------------------------------
    beat(scene, t, 3)
    first = "abaab"
    shown = choice_list(first, 0.6).move_to([LIST_X, 1.3, 0])
    scene.play(FadeOut(VGroup(left, right, a_tag, b_tag, edges)), run_time=0.6)
    trail = _walk(scene, ball, first, 1.25, on_step=lambda i: [FadeIn(shown[i], shift=DOWN * 0.2)])

    beat(scene, t, 4)
    end = nodes[(N, K)]
    count_tag = txt("2 right steps", cfg.FONT["body"], cfg.B_COLOR).next_to(end, DOWN, buff=0.3)
    scene.play(end.disc.animate.set_stroke(cfg.GOLD, 6), Flash(end, color=cfg.GOLD, flash_radius=0.6), run_time=1.0)
    scene.play(*[Indicate(trail[i], color=cfg.WHITE) for i, c in enumerate(first) if c == "b"],
               *[Indicate(shown[i], color=cfg.WHITE, scale_factor=1.3) for i, c in enumerate(first) if c == "b"],
               run_time=1.2)
    scene.play(FadeIn(count_tag, shift=UP * 0.15), run_time=0.8)

    beat(scene, t, 5)
    second = "bbaaa"
    shown2 = choice_list(second, 0.6).move_to([LIST_X, 0.4, 0])
    scene.play(trail.animate.set_opacity(0.35), ball.animate.move_to(point_of(0, 0)), run_time=0.8)
    trail2 = _walk(scene, ball, second, 0.75, on_step=lambda i: [FadeIn(shown2[i], shift=DOWN * 0.2)])

    beat(scene, t, 6)
    ask = _value(N, K, "?", cfg.ORANGE)
    scene.play(FadeOut(count_tag), FadeIn(ask, scale=1.4), run_time=0.8)

    # --- All ten routes into the 10 -----------------------------------------------------------
    beat(scene, t, 7)
    head = swap_heading(scene, head, "Every route with two right steps")
    scene.play(FadeOut(VGroup(trail, trail2, shown, shown2)), FadeOut(ball), run_time=0.6)
    routes = mu.paths_to(N, K)
    trails, lists = VGroup(), VGroup()
    tally = ask
    for j, word in enumerate(routes):
        path = path_line(word, point_of, width=5).set_z_index(1)
        row = choice_list(word, LIST_CELL).move_to([LIST_X, LIST_TOP - j * LIST_STEP, 0])
        new_tally = _value(N, K, j + 1)
        scene.play(Create(path), FadeIn(row, shift=LEFT * 0.2), ReplacementTransform(tally, new_tally),
                   run_time=0.9)
        scene.play(path.animate.set_opacity(0.45), run_time=0.25)
        trails.add(path)
        lists.add(row)
        tally = new_tally

    beat(scene, t, 8)
    scene.play(trails.animate.set_opacity(0.9), Indicate(tally, color=cfg.WHITE, scale_factor=1.4), run_time=1.2)
    scene.play(trails.animate.set_opacity(0.55), run_time=0.6)

    # --- Every number counts routes -----------------------------------------------------------------
    beat(scene, t, 9)
    head = swap_heading(scene, head, "Each number counts routes")
    values = {(n, k): _value(n, k, mu.path_counts(N + 1)[n][k]) for n in range(N + 1) for k in range(n + 1)
              if (n, k) != (N, K)}
    scene.play(LaggedStart(*[FadeIn(v, scale=0.6) for v in values.values()], lag_ratio=0.05), run_time=2.2)

    # --- Pascal's rule, a third time ----------------------------------------------------------------------
    beat(scene, t, 10)
    via_left = [p for p, w in zip(trails, routes) if w[-1] == "b"]       # through (4, 1), stepping right
    via_right = [p for p, w in zip(trails, routes) if w[-1] == "a"]      # through (4, 2), stepping left
    scene.play(nodes[(N - 1, K - 1)].disc.animate.set_stroke(cfg.B_COLOR, 6),
               nodes[(N - 1, K)].disc.animate.set_stroke(cfg.A_COLOR, 6), run_time=0.9)
    scene.play(*[p.animate.set_opacity(0.15) for p in via_right], *[p.animate.set_opacity(1) for p in via_left],
               run_time=1.0)
    scene.play(*[p.animate.set_opacity(1) for p in via_right], *[p.animate.set_opacity(0.15) for p in via_left],
               run_time=1.0)
    scene.play(*[p.animate.set_opacity(0.55) for p in trails], run_time=0.6)

    beat(scene, t, 11)
    sum_line = colored_tex([(str(len(via_left)), "b"), ("+", "op"), (str(len(via_right)), "a"), ("=", "op"),
                            (str(len(routes)), "coef")], cfg.FONT["title"]).move_to([LIST_X, -3.2, 0])
    scene.play(Indicate(values[(N - 1, K - 1)], color=cfg.B_COLOR, scale_factor=1.6), run_time=1.0)
    scene.play(Indicate(values[(N - 1, K)], color=cfg.A_COLOR, scale_factor=1.6), run_time=1.0)
    scene.play(Write(sum_line), run_time=1.2)

    # --- Three stories, one set of numbers -----------------------------------------------------------------------
    beat(scene, t, 12)
    head = swap_heading(scene, head, "Paths, choices, coefficients")
    term = term_tex(mu.coefficients(N)[K], N - K, K, cfg.FONT["title"]).move_to([LIST_X, 0.1, 0])
    scene.play(FadeOut(lists), FadeOut(sum_line), run_time=0.6)
    stories = VGroup(
        VGroup(path_line("aabab", lambda n, k: np.array([LIST_X - 1.4 + (k - n / 2) * 0.4, 2.45 - n * 0.27, 0]), 3.5),
               txt("= 10 routes", cfg.FONT["body"], cfg.GOLD).move_to([LIST_X + 1.0, 1.85, 0])),
        VGroup(choice_list("aabab", 0.34).move_to([LIST_X - 1.3, 0.9, 0]),
               txt("= 10 lists", cfg.FONT["body"], cfg.GOLD).move_to([LIST_X + 1.0, 0.9, 0])),
        term.move_to([LIST_X, -0.3, 0]),
    )
    for story in stories:
        scene.play(FadeIn(story, shift=LEFT * 0.3), run_time=1.0)
    scene.play(Indicate(tally, color=cfg.WHITE, scale_factor=1.4), run_time=1.0)

    beat(scene, t, 13)
    head = swap_heading(scene, head, "One structure, three views")
    scene.play(FadeOut(VGroup(*nodes.values(), *values.values(), tally, trails, stories)), run_time=0.8)
    centre = colored_tex([(r"\binom{5}{2}", "coef"), ("=", "op"), ("10", "coef")], cfg.FONT["title"]).move_to(DOWN * 0.3)
    corners = VGroup(chip("Pascal's triangle", cfg.GOLD, cfg.FONT["body"]).move_to([0, 2.45, 0]),
                     chip("Combinations", cfg.B_COLOR, cfg.FONT["body"]).move_to([-4.6, -2.6, 0]),
                     chip("Binomial coefficients", cfg.A_COLOR, cfg.FONT["body"]).move_to([4.3, -2.6, 0]))
    links = VGroup(*[DoubleArrow(corners[i].get_center(), corners[j].get_center(), buff=1.1, color=cfg.CYAN,
                                 stroke_width=4, tip_length=0.22) for i, j in ((0, 1), (1, 2), (2, 0))])
    for link in links:
        link.scale(0.78)
    scene.play(FadeIn(centre, scale=1.2), run_time=0.9)
    scene.play(LaggedStart(*[FadeIn(c, scale=1.1) for c in corners], lag_ratio=0.4), run_time=1.8)
    scene.play(LaggedStart(*[GrowFromCenter(link) for link in links], lag_ratio=0.3), run_time=1.6)
    scene.play(Indicate(corners, color=cfg.WHITE, scale_factor=1.05), run_time=1.2)

    # --- Make the walk random ---------------------------------------------------------------------------------------
    beat(scene, t, 14)
    scene.play(FadeOut(VGroup(centre, corners, links)), run_time=0.6)
    heads, tails = coin("H", 0.9).move_to(DOWN * 0.2), coin("T", 0.9).move_to(DOWN * 0.2)
    scene.play(FadeIn(heads, scale=0.6), run_time=0.6)
    for face in (tails, heads.copy(), tails.copy()):
        scene.play(heads.animate.stretch(0.05, 0), run_time=0.25)
        scene.remove(heads)
        heads = face.copy().stretch(0.05, 0)
        scene.add(heads)
        scene.play(heads.animate.stretch(20, 0), run_time=0.25)
    end_scene(scene, t, cfg.SCENE_DURATIONS["10"])
