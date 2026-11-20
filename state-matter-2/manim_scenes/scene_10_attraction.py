"""Scene 10 — attraction softens the blow. A close-up of a dense gas beside a
glass wall (a 2D cross-section): cyan molecules jitter in place, faint green
links join near neighbours. A gold molecule is followed. Every neighbour
within reach pulls it with a green arrow whose length falls with distance;
their sum (thick green) is drawn live from the actual positions.

Deep inside, the pulls nearly cancel. As the gold molecule travels to the
wall, its neighbours lie mostly behind it and the sum swings round to point
back into the gas. It strikes the wall more softly: its push on the wall
(orange) falls short of the dashed ideal push, and every molecule arriving at
the wall feels the same backward tug. Two bars compare the pressures, P_real
below P_ideal: a negative deviation. Finally a web of every near pair fades
in — the full treatment averages over all pairs — and the conclusion is
boxed: attraction lowers the pressure.

The molecule layout is seeded; among a few seeds the scene keeps the one whose
interior pulls cancel best, so "the pulls cancel" is true of what is drawn.
"""

from manim_scenes.common import *
from manim_scenes.kit_a import arrow2d, ghost_arrow, ticking
from manim_scenes.kit_d import at_word

REGION = (-7.0, 2.1, -2.75, 2.15)      # x0, x1, y0, y1 of the gas
WALL_X = 2.55
PATH_Y = -0.15
START_X, NEAR_X, HIT_X = -3.3, 1.65, WALL_X - 0.27
REACH = 2.5                            # neighbours closer than this pull the gold molecule
R_MOL = 0.2
COL_X = 5.25


class Scene10Attraction(Scene):
    def construct(self) -> None:
        play_scene(self)


def layout(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = REGION
    pts: list[np.ndarray] = []
    for _ in range(4000):
        p = np.array([rng.uniform(x0, x1), rng.uniform(y0, y1)])
        if START_X - 0.6 < p[0] < x1 and abs(p[1] - PATH_Y) < 0.62:
            continue                     # leave a lane for the gold molecule
        if all(np.linalg.norm(p - q) > 1.0 for q in pts):
            pts.append(p)
    return np.array(pts)


def pull_on(p: np.ndarray, others: np.ndarray) -> np.ndarray:
    """Vector pulls of every neighbour within REACH on a molecule at p (length falls with distance)."""
    d = others - p
    dist = np.linalg.norm(d, axis=1)
    near = (dist < REACH) & (dist > 1e-6)
    return (d[near] / dist[near, None]) * (0.95 * (1.25 / np.maximum(dist[near], 1.25)) ** 2)[:, None]


def pick_layout() -> np.ndarray:
    best, best_score = None, np.inf
    for k in range(8):
        pts = layout(cfg.SEED + 100 + k)
        inside = np.linalg.norm(pull_on(np.array([START_X, PATH_Y]), pts).sum(axis=0))
        wall = np.linalg.norm(pull_on(np.array([NEAR_X, PATH_Y]), pts).sum(axis=0))
        score = inside / max(wall, 1e-6)
        if score < best_score:
            best, best_score = pts, score
    return best


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "10", TITLES["10"])
    base = pick_layout()
    rng = np.random.default_rng(cfg.SEED + 109)
    phase = rng.uniform(0, 2 * np.pi, base.shape)
    omega = rng.uniform(1.6, 2.6, base.shape)
    gold_x = Knob(START_X)
    clock = {"t": 0.0}

    def others() -> np.ndarray:
        return base + 0.07 * np.sin(omega * clock["t"] + phase)

    def gold() -> np.ndarray:
        return np.array([gold_x.value, PATH_Y])

    # --- 0. A dense gas beside a wall -----------------------------------------------------------------------------------
    wall = VGroup(Rectangle(width=0.32, height=6.2, stroke_color=cfg.GLASS, stroke_width=3, fill_color=cfg.GLASS,
                            fill_opacity=0.16).move_to([WALL_X + 0.16, -0.3, 0]),
                  Line([WALL_X, -3.4, 0], [WALL_X, 2.8, 0], stroke_color=cfg.GLASS, stroke_width=6))
    wall_tag = txt("wall", cfg.FONT["label"], cfg.GLASS).next_to(wall, DOWN, buff=0.1).shift(UP * 0.0)
    wall_tag.move_to([WALL_X + 0.16, -3.75, 0])
    mols = VGroup(*[bead(p.tolist() + [0], cfg.MOLECULE, R_MOL, glow=0.4) for p in base])

    def jitter(_):
        pos = others()
        for m, p in zip(mols, pos):
            m.move_to([p[0], p[1], 0])

    web_alpha = Knob(0.0)

    def web() -> VGroup:
        pos = others()
        d = np.linalg.norm(pos[:, None] - pos[None], axis=-1)
        i, j = np.nonzero(np.triu(d < 1.55, 1))
        return VGroup(*[Line([*pos[a], 0], [*pos[b], 0], stroke_color=cfg.ATTRACT, stroke_width=2.5,
                             stroke_opacity=0.35 * web_alpha.value)
                        for a, b in zip(i, j)])

    driver = ticking(VGroup(), lambda s: (clock.__setitem__("t", s), jitter(None)))
    scene.add(driver)
    links = live(VGroup(), web)
    scene.play(FadeIn(wall), FadeIn(wall_tag), LaggedStart(*[FadeIn(m, scale=0.6) for m in mols], lag_ratio=0.03), run_time=2.0)
    at_word(scene, t, 0, "pull", lead=0.3)
    scene.add(links)
    play_in(scene, t, 1, web_alpha.to(links, 1.0), run_time=1.4)

    # --- 1. Deep inside: pulls from every side cancel -------------------------------------------------------------------
    beat(scene, t, 1)

    pull_alpha, net_alpha = Knob(0.0), Knob(0.0)

    def arrows() -> VGroup:
        p = gold()
        group = VGroup()
        for v in pull_on(p, others()):
            group.add(arrow2d([*p, 0], [*(p + v), 0], cfg.ATTRACT, width=0.055, tip_len=0.16,
                              opacity=0.9 * pull_alpha.value))
        return group

    def net() -> VGroup:
        p = gold()
        v = pull_on(p, others()).sum(axis=0) * 1.1
        if np.linalg.norm(v) < 0.08:
            return VGroup(Circle(radius=0.36, stroke_color=cfg.WHITE, stroke_width=3,
                                 stroke_opacity=0.6 * net_alpha.value).move_to([*p, 0]))
        return arrow2d([*p, 0], [*(p + v), 0], cfg.ATTRACT, width=0.14, tip_len=0.34, opacity=net_alpha.value)

    the_one = live(VGroup(), lambda: bead([*gold(), 0], cfg.FOLLOWED, R_MOL * 1.15, glow=1.0))
    pulls = live(VGroup(), arrows)
    total = live(VGroup(), net)
    scene.add(the_one)
    scene.play(FadeIn(the_one, scale=1.5), web_alpha.to(links, 0.45), run_time=1.0)
    at_word(scene, t, 1, "tugged", lead=0.2)
    scene.add(pulls)
    scene.play(pull_alpha.to(pulls, 1.0), run_time=1.0)
    at_word(scene, t, 1, "cancel", lead=0.4)
    cancel_tag = VGroup(txt("net pull", cfg.FONT["label"], cfg.ATTRACT), eq(r"\approx 0", cfg.FONT["section"], cfg.WHITE))
    cancel_tag.arrange(RIGHT, buff=0.2).move_to([START_X, 2.75, 0])
    scene.add(total)
    play_in(scene, t, 2, net_alpha.to(total, 1.0), FadeIn(cancel_tag, shift=DOWN * 0.1), run_time=1.0)

    # --- 2. Near the wall: the neighbours are behind it; the net pull points back ------------------------------------------
    beat(scene, t, 2)
    scene.play(gold_x.to(the_one, NEAR_X, rate_func=smooth), FadeOut(cancel_tag), run_time=4.0)
    at_word(scene, t, 2, "points", lead=0.3)
    back_tag = txt("net pull: back into the gas", cfg.FONT["label"], cfg.ATTRACT).move_to([-1.6, 2.75, 0])
    play_in(scene, t, 3, FadeIn(back_tag, shift=LEFT * 0.15), net_alpha.to(total, 0.5, rate_func=there_and_back), run_time=1.4)

    # --- 3. It strikes more softly; every arriving molecule feels the same tug -----------------------------------------------
    beat(scene, t, 3)
    scene.play(gold_x.to(the_one, HIT_X, rate_func=rush_into), run_time=0.7)
    y_push = PATH_Y
    ideal_push = ghost_arrow([WALL_X + 0.45, y_push, 0], [WALL_X + 3.4, y_push, 0], cfg.MUTED, width=0.24, tip_len=0.5)
    real_push = arrow2d([WALL_X + 0.45, y_push, 0], [WALL_X + 2.4, y_push, 0], cfg.IMPULSE, width=0.24, tip_len=0.5)
    flash = Circle(radius=0.3, stroke_color=cfg.IMPULSE, stroke_width=6).move_to([WALL_X, y_push, 0])
    scene.play(FadeIn(real_push, shift=RIGHT * 0.2), FadeIn(flash), flash.animate.scale(2.2).set_stroke(opacity=0),
               gold_x.to(the_one, NEAR_X - 0.3, rate_func=smooth), run_time=1.2)
    scene.remove(flash)
    soft = txt("softer", cfg.FONT["label"], cfg.IMPULSE).next_to(real_push, DOWN, buff=0.22)
    ideal_lbl = txt("ideal", cfg.FONT["label"], cfg.MUTED).next_to(ideal_push, UP, buff=0.18)
    scene.play(Create(ideal_push), FadeIn(ideal_lbl), FadeIn(soft, shift=UP * 0.1), run_time=1.2)
    at_word(scene, t, 3, "Every", lead=0.2)
    near_wall = [i for i, p in enumerate(base) if p[0] > WALL_X - 1.3]
    tugs = VGroup(*[arrow2d([*base[i], 0], [base[i][0] - 0.8, base[i][1], 0], cfg.ATTRACT, width=0.07, tip_len=0.2)
                    for i in near_wall])
    scene.play(LaggedStart(*[GrowFromPoint(a, a.get_right()) for a in tugs], lag_ratio=0.15), run_time=1.6)
    play_in(scene, t, 4, Indicate(VGroup(*[mols[i] for i in near_wall]), color=cfg.GOLD, scale_factor=1.2), run_time=1.4)

    # --- 4. P_real < P_ideal --------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(VGroup(ideal_push, real_push, soft, ideal_lbl, back_tag)), run_time=0.7)
    base_y = -2.6
    bar_ideal = DashedVMobject(Rectangle(width=1.0, height=3.6, stroke_color=cfg.LIMIT, stroke_width=4), num_dashes=40)
    bar_ideal.move_to([COL_X - 0.8, base_y + 1.8, 0])
    bar_real = Rectangle(width=1.0, height=2.8, stroke_color=cfg.PRESSURE, stroke_width=3, fill_color=cfg.PRESSURE,
                         fill_opacity=0.75).move_to([COL_X + 0.8, base_y + 1.4, 0])
    floor_line = Line([COL_X - 1.7, base_y, 0], [COL_X + 1.7, base_y, 0], stroke_color=cfg.MUTED, stroke_width=3)
    names = VGroup(eq(r"P_{\text{ideal}}", cfg.FONT["label"], cfg.LIMIT).next_to(bar_ideal, DOWN, buff=0.2),
                   eq(r"P_{\text{real}}", cfg.FONT["label"], cfg.PRESSURE).next_to(bar_real, DOWN, buff=0.2))
    names[1].match_y(names[0])
    scene.play(Create(floor_line), Create(bar_ideal), FadeIn(names[0]), run_time=1.2)
    scene.play(GrowFromEdge(bar_real, DOWN), FadeIn(names[1]), run_time=1.2)
    at_word(scene, t, 4, "less", lead=0.3)
    law = eq(r"P_{\text{real}} < P_{\text{ideal}}", cfg.FONT["section"], cfg.WHITE).move_to([COL_X, 2.3, 0])
    play_in(scene, t, 5, Write(law), run_time=1.6)

    # --- 5. A negative deviation ------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    kind = result_label("negative deviation", cfg.ATTRACT, cfg.FONT["label"]).next_to(law, DOWN, buff=0.3)
    play_in(scene, t, 6, FadeIn(kind, shift=UP * 0.1), run_time=1.0)

    # --- 6. A simplification: the full treatment averages over all pairs --------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(tugs), pull_alpha.to(pulls, 0.0), net_alpha.to(total, 0.0), web_alpha.to(links, 2.4), run_time=1.0)
    scene.remove(pulls, total)
    at_word(scene, t, 6, "pair", lead=0.3)
    avg = chip("averaged over every pair", cfg.ATTRACT, cfg.FONT["small"]).move_to([-2.4, 2.75, 0])
    scene.play(FadeIn(avg, shift=DOWN * 0.1), web_alpha.to(links, 1.6, rate_func=there_and_back_with_pause), run_time=1.4)
    at_word(scene, t, 6, "conclusion", lead=0.3)
    verdict = boxed(txt("attraction lowers P", cfg.FONT["label"], cfg.ATTRACT), cfg.GOLD, buff=0.2)
    verdict.move_to([COL_X, -3.6, 0])
    scene.play(FadeOut(names), FadeOut(wall_tag), run_time=0.5)
    scene.play(FadeIn(verdict.body, shift=UP * 0.1), Create(verdict.frame), run_time=1.0)
    finish(scene, t, fill=lambda s: [gold_x.to(the_one, START_X + 1.0, rate_func=smooth)])
