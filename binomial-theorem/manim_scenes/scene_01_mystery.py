"""Chapter 1 — the mystery, followed by the title card.

The film opens with the question of where the coefficients come from.
Then (a+b)^5 is expanded one bracket at a time, the products doubling
2, 4, 8, 16, 32 before anything simplifies. The 32 products then
collapse onto six coefficients — and a triangle built by addition turns out to
hold the very same six numbers. A closing title card introduces the visual
explanation before the film starts small.
"""

from manim_scenes.common import *
from utils.render_helpers import grid_positions

N = 5
BRUTE_CENTER = (0.0, -1.05)


class Scene01Mystery(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _word(word: str) -> MathTex:
    """A raw product such as a a b a b, before like terms are collected."""
    return colored_tex([(letter, letter) for letter in word], cfg.FONT["small"])


def _brute_stage(stage: int) -> VGroup:
    """All 2**stage products after multiplying ``stage`` brackets."""
    words = mu.choice_words(stage)
    group = VGroup(*[_word(w) for w in words])
    points = grid_positions(len(words), min(len(words), 8), x_step=1.62, y_step=0.62, center=BRUTE_CENTER)
    for mob, point in zip(group, points):
        mob.move_to(point)
    group.words = words
    return group


def _product_line() -> MathTex:
    parts = []
    for _ in range(N):
        parts += [("(", "op"), ("a", "a"), ("+", "op"), ("b", "b"), (")", "op")]
    line = colored_tex(parts, cfg.FONT["body"])
    line.factors = [VGroup(*line.pieces[5 * i:5 * i + 5]) for i in range(N)]
    return line


def _counter(value: int) -> VGroup:
    count = txt(str(value), cfg.FONT["section"], cfg.ORANGE)
    unit = txt("products", cfg.FONT["label"], cfg.ORANGE)
    return VGroup(count, unit).arrange(RIGHT, buff=0.25, aligned_edge=DOWN).move_to(DOWN * 3.55)


def _title_card(subtitle_text: str = "Explained visually") -> tuple[Mobject, ...]:
    """Close the mystery with bright, minimal type."""
    title = txt("Binomial Theorem", cfg.FONT["hero"], cfg.GOLD)
    fit_width(title, 13.2)
    title.move_to(UP * 1.65)
    subtitle = txt(subtitle_text, cfg.FONT["label"], cfg.CYAN)
    fit_width(subtitle, 13.2)
    subtitle.move_to(DOWN * 2.05)
    rule = Line(LEFT * 4.0, RIGHT * 4.0, color=cfg.GOLD, stroke_width=4).move_to(UP * 0.9)
    title_glow = halo(4.5, cfg.CYAN, peak_opacity=0.06).move_to(UP * 0.3)
    hero = colored_tex(lhs_parts(N, sep=""), cfg.FONT["hero"])
    hero.move_to(DOWN * 0.45)
    return title, subtitle, rule, title_glow, hero


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "01", "Can we predict every coefficient?")

    # --- Open directly with the mystery ------------------------------------
    hero = colored_tex(lhs_parts(N, sep=""), cfg.FONT["hero"]).move_to(UP * 0.2)
    glow = halo(2.6, cfg.CYAN, peak_opacity=0.08).move_to(UP * 0.2)
    hud(scene, hero)
    scene.play(FadeIn(glow), Write(hero), run_time=1.0)

    # --- Six terms, six unknown coefficients -------------------------------
    beat(scene, t, 1)
    unknown = expansion_tex(N, cfg.FONT["body"], coefs=["{?}"] * (N + 1)).move_to(UP * 2.5)
    scene.play(FadeOut(glow), ReplacementTransform(hero, unknown.lhs), run_time=1.2)
    scene.play(LaggedStart(*[FadeIn(VGroup(term, *([unknown.pluses[k - 1]] if k else [])), shift=DOWN * 0.2)
                             for k, term in enumerate(unknown.terms)], lag_ratio=0.25), run_time=2.2)

    beat(scene, t, 2)
    scene.play(LaggedStart(*[Circumscribe(c, color=cfg.GOLD, buff=0.08, fade_out=True) for c in unknown.coefs],
                           lag_ratio=0.15), run_time=2.4)
    question = caption("Why these coefficients?", cfg.GOLD, cfg.FONT["body"], y=0.4)
    scene.play(FadeIn(question, shift=UP * 0.2), run_time=0.8)

    # --- Brute force: the products double with every bracket ---------------
    beat(scene, t, 3)
    line = _product_line().move_to(UP * 1.3)
    scene.play(FadeOut(question), FadeIn(line, shift=DOWN * 0.2), run_time=1.0)
    scene.play(LaggedStart(*[Indicate(f, color=cfg.CYAN, scale_factor=1.08) for f in line.factors],
                           lag_ratio=0.2), run_time=1.8)

    beat(scene, t, 4)
    stage = _brute_stage(1)
    counter = _counter(2)
    scene.play(line.factors[0].animate.set_opacity(cfg.CONTEXT_OPACITY), TransformFromCopy(line.factors[0], stage),
               FadeIn(counter, shift=UP * 0.15), run_time=0.9)
    for s in range(2, N + 1):
        nxt = _brute_stage(s)
        new_counter = _counter(2 ** s)
        scene.play(
            line.factors[s - 1].animate.set_opacity(cfg.CONTEXT_OPACITY),
            *[TransformFromCopy(stage[i // 2], nxt[i]) for i in range(len(nxt))],
            FadeOut(stage),
            ReplacementTransform(counter, new_counter),
            run_time=1.15,
        )
        stage, counter = nxt, new_counter
    scene.play(counter.animate.scale(1.12).set_color(cfg.RED), rate_func=there_and_back, run_time=0.8)

    # --- Like terms collapse onto six coefficients --------------------------
    beat(scene, t, 5)
    known = expansion_tex(N, cfg.FONT["body"], coefs=[str(c) for c in mu.coefficients(N)]).move_to(UP * 2.5)
    targets = {k: unknown.coefs[k].get_center() for k in range(N + 1)}
    scene.play(
        *[mob.animate.move_to(targets[word.count("b")]).scale(0.25).set_opacity(0)
          for mob, word in zip(stage, stage.words)],
        FadeOut(line), FadeOut(counter),
        run_time=2.2, rate_func=smooth,
    )
    scene.remove(stage)
    scene.play(ReplacementTransform(unknown, known), run_time=1.0)
    scene.play(LaggedStart(*[Flash(c, color=cfg.GOLD, line_length=0.18, flash_radius=0.35) for c in known.coefs],
                           lag_ratio=0.2), run_time=2.0)

    # --- A triangle built by addition --------------------------------------
    beat(scene, t, 6)
    triangle = pascal_triangle(N + 1, pitch_x=1.3, pitch_y=0.66, top=UP * 1.25, size=cfg.FONT["label"])
    upper = [triangle_row(triangle, n) for n in range(N)]
    scene.play(LaggedStart(*[FadeIn(row, shift=DOWN * 0.15) for row in upper], lag_ratio=0.35), run_time=2.4)
    last = triangle_row(triangle, N)
    scene.play(*[TransformFromCopy(known.coefs[k], last[k]) for k in range(N + 1)], run_time=1.8)
    frame = glow_frame(last, cfg.GOLD, buff=0.18)
    scene.play(Create(frame), run_time=0.7)

    beat(scene, t, 7)
    tick = check_mark(0.3).next_to(frame, RIGHT, buff=0.35)
    scene.play(frame.animate.set_color(cfg.GREEN), Create(tick),
               *[c.animate.set_color(cfg.GREEN) for c in known.coefs], run_time=0.9)
    scene.play(*[c.animate.set_color(cfg.GOLD) for c in known.coefs], run_time=0.5)

    # --- Why would addition know algebra? -----------------------------------
    beat(scene, t, 8)
    left, right, below = triangle.entries[(4, 1)], triangle.entries[(4, 2)], triangle.entries[(5, 2)]
    feeds = VGroup(arrow_between(left.get_bottom(), below.get_top() + LEFT * 0.12, cfg.GOLD, 4),
                   arrow_between(right.get_bottom(), below.get_top() + RIGHT * 0.12, cfg.GOLD, 4))
    scene.play(FadeOut(tick), frame.animate.set_color(cfg.GOLD).set_opacity(0.35), GrowArrow(feeds[0]),
               GrowArrow(feeds[1]), run_time=0.9)
    scene.play(Indicate(left, color=cfg.WHITE), Indicate(right, color=cfg.WHITE), run_time=0.8)
    scene.play(Indicate(below, color=cfg.WHITE, scale_factor=1.3), run_time=0.8)
    mystery = txt("?", cfg.FONT["hero"], cfg.ORANGE).move_to(RIGHT * 5.6 + DOWN * 0.4)
    links = VGroup(
        CurvedArrow(mystery.get_top() + UP * 0.1, known.get_right() + DOWN * 0.35 + LEFT * 0.3, angle=0.5,
                    color=cfg.ORANGE, stroke_width=5),
        CurvedArrow(mystery.get_bottom() + DOWN * 0.1, last.get_right() + RIGHT * 0.4 + DOWN * 0.1, angle=-0.5,
                    color=cfg.ORANGE, stroke_width=5),
    )
    scene.play(FadeIn(mystery, scale=1.4), Create(links), run_time=1.2)

    # --- The answer will be about choices -----------------------------------
    beat(scene, t, 9)
    head = swap_heading(scene, head, "A story about choices")
    machines = machine_row(N, width=2.1, height=1.3, door=0.4, y=0.0)
    scene.play(FadeOut(VGroup(known, triangle, frame, feeds, mystery, links)), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(m, shift=UP * 0.3) for m in machines], lag_ratio=0.15), run_time=1.2)
    for word in ("aabab", "babba", "abaab"):
        scene.play(*[m.animate.choose(letter) for m, letter in zip(machines, word)], run_time=0.7)
    scene.play(*[m.animate.reset() for m in machines], run_time=0.6)

    # --- Close the mystery with the film's title ----------------------------
    beat(scene, t, 10)
    title, subtitle, rule, title_glow, hero = _title_card()
    hud(scene, title, subtitle, rule, title_glow, hero)
    scene.play(FadeOut(head), FadeOut(machines), run_time=0.4)
    scene.play(FadeIn(title_glow), FadeIn(title, shift=DOWN * 0.2),
               FadeIn(subtitle, shift=UP * 0.15), Create(rule), Write(hero), run_time=0.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["01"])
