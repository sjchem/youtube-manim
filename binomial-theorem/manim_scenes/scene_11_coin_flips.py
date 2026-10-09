"""Chapter 11 — coin flips, a Galton board and the bell curve (3D).

Heads plays a, tails plays b. Five flips are one route down a board of pegs
(an idealised Galton board: every bounce is treated as an independent fair
flip). 64 seeded balls pile up roughly like twice row 5; counting gives the
exact chance 10/32 of two tails. Row 5 then lifts out of the triangle as a 3D
histogram, and longer rows (10 and 20 flips) approach the bell curve.
"""

from manim_scenes.common import *

ROWS = pm.DEMO_ROWS
GTOP = np.array([-3.9, 2.75, 0.0])
GPX, GPY = 0.95, 0.6
FLOOR = -2.65
BALL_R = 0.085
PANEL_X = 3.95


class Scene11CoinFlips(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def peg_point(n: int, k: int) -> np.ndarray:
    return pascal_point(n, k, GPX, GPY, GTOP)


def bin_x(k: int) -> float:
    return float(peg_point(ROWS, k)[0])


def slot(k: int, j: int) -> np.ndarray:
    """Where the j-th ball in bin k comes to rest: four across, stacking up."""
    col, row = j % 4, j // 4
    return np.array([bin_x(k) + (col - 1.5) * 2.2 * BALL_R, FLOOR + BALL_R * 1.2 + row * 2.2 * BALL_R, 0.0])


def ball(color=cfg.CYAN) -> Circle:
    return Circle(radius=BALL_R, stroke_width=0, fill_color=color, fill_opacity=1)


def route_curve(route: str, j: int) -> VMobject:
    """Bounce from peg to peg, then fall straight into the bin."""
    curve = bounce_path(route, peg_point, hop=0.22)
    curve.add_line_to(slot(route.count("b"), j))
    return curve


def coin_row(route: str) -> VGroup:
    return VGroup(*[coin("H" if c == "a" else "T", 0.36) for c in route]).arrange(RIGHT, buff=0.18)


def bars_for(values, unit: float, width: float, gap: float, color: str = cfg.GOLD, opacity: float = 0.75,
             baseline=DOWN * 2.9) -> VGroup:
    return bar_set(values, unit, width, gap, baseline, [color] * len(values), opacity)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "11", "Flip a coin at every step")

    # --- Heads steps left, tails steps right ---------------------------------------
    big = coin("H", 0.9).move_to([PANEL_X, 1.2, 0])
    scene.play(FadeIn(big, scale=0.5), run_time=0.8)
    hint_l = Arrow([PANEL_X - 0.6, 0.05, 0], [PANEL_X - 1.9, -1.4, 0], buff=0, color=cfg.A_COLOR, stroke_width=8)
    hint_r = Arrow([PANEL_X + 0.6, 0.05, 0], [PANEL_X + 1.9, -1.4, 0], buff=0, color=cfg.B_COLOR, stroke_width=8)
    tag_h = txt("H: left", cfg.FONT["body"], cfg.A_COLOR).next_to(hint_l.get_end(), DOWN, buff=0.2)
    tag_t = txt("T: right", cfg.FONT["body"], cfg.B_COLOR).next_to(hint_r.get_end(), DOWN, buff=0.2)
    scene.play(GrowArrow(hint_l), FadeIn(tag_h), run_time=0.9)
    flipped = coin("T", 0.9).move_to(big)
    scene.play(big.animate.stretch(0.05, 0), run_time=0.3)
    scene.remove(big)
    flipped.stretch(0.05, 0)
    scene.add(flipped)
    scene.play(flipped.animate.stretch(20, 0), run_time=0.3)
    scene.play(GrowArrow(hint_r), FadeIn(tag_t), run_time=0.9)

    # --- A board of pegs -----------------------------------------------------------------
    beat(scene, t, 1)
    pegs = VGroup(*[peg(peg_point(n, k), 0.075) for n in range(ROWS) for k in range(n + 1)])
    walls = VGroup(*[Line([bin_x(k) - GPX / 2, peg_point(ROWS, 0)[1] - 0.15, 0], [bin_x(k) - GPX / 2, FLOOR, 0],
                          stroke_color=cfg.MUTED, stroke_width=3, stroke_opacity=0.7) for k in range(ROWS + 2)])
    floor = Line([bin_x(0) - GPX / 2, FLOOR, 0], [bin_x(ROWS) + GPX / 2, FLOOR, 0], stroke_color=cfg.MUTED, stroke_width=3)
    scene.play(LaggedStart(*[FadeIn(p, scale=0.4) for p in pegs], lag_ratio=0.04), Create(walls), Create(floor),
               run_time=2.0)
    scene.play(FadeOut(VGroup(hint_l, hint_r, tag_h, tag_t)), flipped.animate.scale(0.6).move_to([PANEL_X, 2.3, 0]),
               run_time=0.8)

    # --- Drop one ball, then another, then many ----------------------------------------------
    routes = pm.galton_drops()
    filled = [0] * (ROWS + 1)
    balls = VGroup()

    def drop(route: str, step_time: float) -> None:
        k = route.count("b")
        b = ball(cfg.WHITE).move_to(peg_point(0, 0) + UP * 0.35)
        flips = coin_row(route).move_to([PANEL_X, 0.6, 0])
        scene.play(FadeIn(b, scale=0.5), run_time=0.3)
        for i, c in enumerate(route):
            seg = VMobject()
            a, z = peg_point(*mu.path_cells(route)[i]), peg_point(*mu.path_cells(route)[i + 1])
            seg.set_points_smoothly([a + UP * 0.12, (a + z) / 2 + UP * 0.25, z + UP * 0.12])
            scene.play(MoveAlongPath(b, seg), FadeIn(flips[i], scale=0.6), run_time=step_time)
        scene.play(b.animate.move_to(slot(k, filled[k])).set_color(cfg.CYAN), run_time=0.45)
        filled[k] += 1
        balls.add(b)
        scene.play(FadeOut(flips), run_time=0.3)

    beat(scene, t, 2)
    drop(routes[0], 0.42)
    beat(scene, t, 3)
    drop(routes[1], 0.3)

    beat(scene, t, 4)
    rest = []
    for route in routes[2:]:
        k = route.count("b")
        b = ball().move_to(peg_point(0, 0) + UP * 0.35)
        rest.append((b, route_curve(route, filled[k])))
        filled[k] += 1
    scene.play(LaggedStart(*[MoveAlongPath(b, c, rate_func=linear) for b, c in rest], lag_ratio=0.06), run_time=5.6)
    for b, _ in rest:
        balls.add(b)
    scene.add(balls)

    beat(scene, t, 5)
    counts = pm.bin_counts(routes)
    tallies = VGroup(*[txt(str(c), cfg.FONT["small"], cfg.CYAN).move_to([bin_x(k), FLOOR - 0.38, 0])
                       for k, c in enumerate(counts)])
    scene.play(LaggedStart(*[FadeIn(x, shift=UP * 0.15) for x in tallies], lag_ratio=0.1), run_time=1.0)
    why = txt("?", cfg.FONT["hero"], cfg.ORANGE).move_to([PANEL_X, 0.4, 0])
    scene.play(FadeIn(why, scale=1.4), run_time=0.7)

    # --- (H + T)^5: thirty-two equally likely sequences -------------------------------------------
    beat(scene, t, 6)
    head = swap_heading(scene, head, "Count the sequences")
    coins_eq = colored_tex([("(", "op"), (r"\mathrm{H}", "a"), ("+", "op"), (r"\mathrm{T}", "b"), (")^{5}", "op")],
                           cfg.FONT["title"]).move_to([PANEL_X, 2.35, 0])
    scene.play(FadeOut(why), FadeOut(flipped), Write(coins_eq), run_time=1.4)

    beat(scene, t, 7)
    total = colored_tex([("2^{5}", "coef"), ("=", "op"), (str(2 ** ROWS), "coef"),
                         (r"\text{ sequences}", "op")], cfg.FONT["body"]).move_to([PANEL_X, 1.35, 0])
    words = mu.choice_words(ROWS)
    seqs = VGroup(*[choice_list(w, 0.24, glyphs=COIN_GLYPHS) for w in words])
    for s, p in zip(seqs, [np.array([PANEL_X + (i % 4 - 1.5) * 1.62, 0.6 - (i // 4) * 0.34, 0]) for i in range(32)]):
        s.move_to(p)
    scene.play(FadeIn(total, shift=DOWN * 0.15), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(s) for s in seqs], lag_ratio=0.03), run_time=2.0)

    beat(scene, t, 8)
    two = [s for s, w in zip(seqs, words) if w.count("b") == 2]
    others = [s for s, w in zip(seqs, words) if w.count("b") != 2]
    choose_eq = colored_tex([(r"\binom{5}{2}", "coef"), ("=", "op"), (str(mu.choose(ROWS, 2)), "coef")],
                            cfg.FONT["section"]).move_to([PANEL_X, -2.95, 0])
    scene.play(*[o.animate.set_opacity(cfg.CONTEXT_OPACITY) for o in others], run_time=0.9)
    scene.play(LaggedStart(*[Indicate(s, color=cfg.GOLD, scale_factor=1.15) for s in two], lag_ratio=0.1),
               FadeIn(choose_eq), run_time=1.6)

    beat(scene, t, 9)
    chance = colored_tex([(r"P(\text{2 tails})", "op"), ("=", "op"), (r"\frac{10}{32}", "coef"),
                          (r"\approx 0.31", "op")], cfg.FONT["section"]).move_to([PANEL_X, -2.95, 0])
    scene.play(ReplacementTransform(choose_eq, chance), run_time=1.2)
    scene.play(Indicate(chance.pieces[2], color=cfg.GOLD, scale_factor=1.3), run_time=1.0)

    beat(scene, t, 10)
    row = VGroup(*[txt(str(c), cfg.FONT["title"], cfg.GOLD) for c in mu.coefficients(ROWS)])
    row.arrange(RIGHT, buff=0.55).move_to([PANEL_X, 0.2, 0])
    over = colored_tex([(r"\text{each out of }", "muted"), ("32", "coef")], cfg.FONT["body"]).next_to(row, DOWN, buff=0.4)
    scene.play(FadeOut(VGroup(*seqs)), FadeOut(total), FadeOut(chance), run_time=0.7)
    scene.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in row], lag_ratio=0.15), FadeIn(over), run_time=1.6)
    scene.play(LaggedStart(*[Indicate(VGroup(*[b for b in balls if abs(b.get_x() - bin_x(k)) < GPX / 2]),
                                      color=cfg.GOLD) for k in range(ROWS + 1)], lag_ratio=0.15), run_time=2.0)

    # --- Lift the row out of the triangle (3D) ---------------------------------------------------
    beat(scene, t, 11)
    head = swap_heading(scene, head, "Lift the row into a histogram")
    scene.play(FadeOut(VGroup(pegs, walls, floor, balls, tallies, coins_eq, row, over)), run_time=0.8)
    # Row 5 sits just below the origin: the camera tilts about it without moving its frame
    # centre (which would also displace the fixed-in-frame heading).
    tri = pascal_triangle(ROWS + 1, pitch_x=1.25, pitch_y=0.62, top=UP * (ROWS * 0.62 - 2.2),
                          size=cfg.FONT["label"], color=cfg.WHITE)
    # A strong navy outline keeps the numbers readable over the pastel bars.
    tri.set_stroke(cfg.BG, width=4, opacity=1, background=True)
    scene.play(FadeIn(tri, shift=DOWN * 0.2), run_time=1.0)
    columns = VGroup()
    for k, c in enumerate(mu.coefficients(ROWS)):
        base = tri.entries[(ROWS, k)].get_center()
        prism = block([0.85, 0.42, c * 0.3], mix_color(k, ROWS), 0.88).move_to(base + OUT * c * 0.15)
        prism.stretch(0.02, 2, about_edge=IN)
        columns.add(prism)
    upper = VGroup(*[e for (n, _), e in tri.entries.items() if n < ROWS])
    scene.play(upper.animate.set_opacity(cfg.CONTEXT_OPACITY), Indicate(triangle_row(tri, ROWS), color=cfg.WHITE), run_time=0.9)
    scene.add(columns)
    scene.move_camera(phi=66 * DEGREES, theta=-82 * DEGREES, zoom=1.2,
                      added_anims=[c.animate.stretch(50, 2, about_edge=IN) for c in columns], run_time=3.2)
    scene.begin_ambient_camera_rotation(rate=-0.06)
    scene.wait(1.8)
    scene.stop_ambient_camera_rotation()

    # --- Back to the flat picture: a sample wobbles around the exact shape ------------------------------
    beat(scene, t, 12)
    head = swap_heading(scene, head, "Sample and expected counts")
    scene.play(FadeOut(VGroup(tri, columns)), run_time=0.7)
    scene.move_camera(phi=0, theta=-PI / 2, zoom=1, run_time=1.0)
    unit = 0.16
    expected = bars_for([int(x) for x in pm.expected_counts()], unit, 1.1, 0.4, cfg.GOLD, 0.15)
    sample = bars_for(counts, unit, 0.62, 0.88, cfg.CYAN, 0.85)
    legend = VGroup(chip("64 balls", cfg.CYAN, cfg.FONT["body"]),
                    chip("expected: 2 × row 5", cfg.GOLD, cfg.FONT["body"])).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    legend.move_to([-5.0, 1.7, 0])
    scene.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in sample], lag_ratio=0.1), FadeIn(legend[0]), run_time=1.4)
    scene.play(LaggedStart(*[Create(b) for b in expected], lag_ratio=0.1), FadeIn(legend[1]), run_time=1.4)
    many = pm.galton_drops(ROWS, 1024)
    scaled = [c * pm.DEMO_BALLS / len(many) for c in pm.bin_counts(many)]
    sample_more = bars_for(scaled, unit, 0.62, 0.88, cfg.CYAN, 0.85)
    more_chip = chip("1,024 balls (scaled)", cfg.CYAN, cfg.FONT["body"]).move_to(legend[0], aligned_edge=LEFT)
    scene.play(ReplacementTransform(sample, sample_more), ReplacementTransform(legend[0], more_chip), run_time=2.0)
    legend[0] = more_chip

    # --- Longer rows: ten flips, twenty flips --------------------------------------------------------------
    beat(scene, t, 13)
    head = swap_heading(scene, head, "More flips, longer rows")
    row10 = mu.coefficients(10)
    bars10 = bars_for(row10, 3.9 / max(row10), 0.72, 0.2)
    peak = txt(mu.big_number(row10[5]), cfg.FONT["body"], cfg.GOLD).next_to(bars10[5], UP, buff=0.15)
    flips10 = chip("10 flips", cfg.GOLD, cfg.FONT["body"]).move_to([-5.0, 1.7, 0])
    out_of = txt(f"out of {mu.big_number(2 ** 10)}", cfg.FONT["body"], cfg.MUTED).move_to([4.9, 1.7, 0])
    scene.play(FadeOut(VGroup(expected, sample_more, legend)), run_time=0.6)
    scene.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars10], lag_ratio=0.06), FadeIn(flips10), run_time=1.8)
    scene.play(FadeIn(peak, shift=DOWN * 0.15), FadeIn(out_of), run_time=0.9)

    beat(scene, t, 14)
    row20 = mu.coefficients(20)
    unit20 = 3.9 / max(row20)
    bars20 = bars_for(row20, unit20, 0.44, 0.14)
    flips20 = chip("20 flips", cfg.GOLD, cfg.FONT["body"]).move_to(flips10)
    scene.play(FadeOut(VGroup(peak, out_of)), ReplacementTransform(bars10, bars20),
               ReplacementTransform(flips10, flips20), run_time=1.6)
    height = pm.normal_curve(20)
    step = 0.44 + 0.14
    bell = ParametricFunction(lambda s: np.array([(s - 10) * step, -2.9 + height(s) * unit20, 0]), t_range=[0, 20],
                              color=cfg.LIMIT_COLOR, stroke_width=7)
    scene.play(Create(bell), run_time=1.6)

    beat(scene, t, 15)
    glow = bell.copy().set_stroke(cfg.LIMIT_COLOR, 18, 0.25)
    bell_chip = chip("bell approximation", cfg.LIMIT_COLOR, cfg.FONT["body"]).move_to([4.9, 1.7, 0])
    scene.play(FadeIn(glow), FadeIn(bell_chip, scale=1.1), run_time=1.0)
    scene.play(bars20.animate.set_opacity(0.45), run_time=0.8)
    scene.play(Indicate(bell_chip, color=cfg.WHITE), run_time=1.0)

    beat(scene, t, 16)
    last = caption("Counts → probabilities", cfg.GREEN, cfg.FONT["body"], y=-3.7)
    scene.play(FadeIn(last, shift=UP * 0.15), run_time=0.9)
    scene.play(bars20.animate.set_opacity(0.85), run_time=1.2)
    scene.play(ShowPassingFlash(bell.copy().set_stroke(cfg.WHITE, 9), time_width=0.4), run_time=1.6)
    scene.play(Indicate(bell_chip, color=cfg.LIMIT_COLOR), run_time=1.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["11"])
