"""Chapter 21 — the cliffhanger: why is oxygen pulled toward a magnet?

The Lewis structure of O2 shows every electron paired, yet liquid oxygen
is attracted into the gap of a magnet (paramagnetism). The droplets'
paths are seeded (``config.SEED``) so the shot repeats exactly. The answer —
two unpaired electrons in molecular orbitals — is left for the next film.
"""

from manim_scenes.common import *

MAGNET_AT = np.array([3.6, 0.2, 0])


class Scene21OxygenMagnet(Scene):
    def construct(self) -> None:
        play_scene(self)


def magnet(at) -> VGroup:
    """A horseshoe magnet with shaded legs and red/blue poles, opening downward."""
    at = np.asarray(at, dtype=float)
    radius, half = 1.25, 0.32
    body = VGroup()
    for fraction in np.linspace(1.0, 0.1, 12):
        tone = mu.mix("#3A4C5C", "#DCE7EF", 1 - fraction)
        body.add(AnnularSector(inner_radius=radius - half * fraction, outer_radius=radius + half * fraction,
                               angle=PI, start_angle=0, stroke_width=0, fill_color=tone, fill_opacity=1))
    legs = VGroup()
    for x, pole in ((-radius, cfg.BLUE), (radius, cfg.RED)):
        legs.add(Rectangle(width=2 * half, height=1.3, stroke_width=0, fill_color="#8FA3B3", fill_opacity=1)
                 .move_to([x, -0.65, 0]))
        legs.add(Rectangle(width=2 * half, height=0.6, stroke_width=0, fill_color=pole, fill_opacity=1)
                 .move_to([x, -1.6, 0]))
    letters = VGroup(txt("S", cfg.FONT["label"], cfg.WHITE).move_to([-radius, -1.6, 0]),
                     txt("N", cfg.FONT["label"], cfg.WHITE).move_to([radius, -1.6, 0]))
    for letter in letters:
        decorative(letter)
    group = VGroup(body, legs, letters).shift(at + UP * 1.0)
    group.scale(1.4, about_point=at)
    group.gap = at + DOWN * 0.75 * 1.4
    return group


def oxygen_molecule(scale: float = 0.27) -> VGroup:
    from manim_scenes.stage3d import _polished_parts

    def atom():
        return VGroup(*_polished_parts(cfg.ELEMENT_COLORS["O"], 24)).scale(scale)

    bond = Line(LEFT * scale * 0.9, RIGHT * scale * 0.9,
                stroke_color=cfg.MUTED, stroke_width=4)
    return VGroup(bond, atom().shift(LEFT * scale * 0.9), atom().shift(RIGHT * scale * 0.9))


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "21", "Why is oxygen magnetic?")

    # --- 1. A question the simple pictures can't answer --------------------------------------------------------------
    lewis = Lewis("O", [("O", 0, 2)], central_lone=[150, 210], at=[-5.3, 0.6, 0], bond=2.5, size=124, ligand_size=124)
    scene.play(Write(lewis), run_time=1.4)
    dismiss_opening_title(scene, t, head, at=2.2)

    # --- 2. Every electron paired... yet pulled toward a magnet ---------------------------------------------------------
    beat(scene, t, 1)
    paired = caption("Lewis: every electron paired", cfg.WHITE)
    scene.play(FadeIn(paired), Indicate(lewis.lone_dots, color=cfg.WHITE, scale_factor=1.4), run_time=1.0)
    pole = magnet(MAGNET_AT)
    scene.play(FadeIn(pole, shift=LEFT * 0.3), run_time=1.0)
    rng = np.random.default_rng(cfg.SEED + 21)
    drops = VGroup()
    paths = []
    for _ in range(9):
        o2 = oxygen_molecule().rotate(rng.uniform(0, PI))
        begin = np.array([rng.uniform(-1.6, 0.8), rng.uniform(-3.0, 1.6), 0])
        end = pole.gap + np.array([rng.uniform(-1.0, 1.0), rng.uniform(-0.55, 0.55), 0])
        o2.move_to(begin)
        drops.add(o2)
        paths.append(end)
    pulled = caption("Yet oxygen is pulled toward a magnet", cfg.BLUE)
    scene.play(FadeIn(drops, lag_ratio=0.1), fade_through(paired, pulled), run_time=1.2)
    scene.remove(paired)
    scene.play(*[d.animate.move_to(p).rotate(0.6) for d, p in zip(drops, paths)], run_time=3.0, rate_func=rush_into)
    question = txt("?", 150, cfg.GOLD).move_to([-1.2, 0.8, 0])
    scene.play(FadeIn(question, scale=0.5), run_time=0.8)

    # --- 3. A deeper theory: electrons over the whole molecule -------------------------------------------------------------
    beat(scene, t, 2)
    cloud = VGroup(*[Ellipse(width=4.6 * f, height=2.2 * f, stroke_width=0, fill_color=cfg.PURPLE, fill_opacity=0.07)
                     for f in np.linspace(1.0, 0.4, 6)]).move_to(lewis.get_center())
    deeper = caption("Electrons spread over the whole molecule", cfg.PURPLE)
    scene.play(FadeIn(cloud), fade_through(pulled, deeper), FadeOut(question), run_time=1.4)
    scene.remove(pulled)
    scene.play(cloud.animate.scale(1.08), run_time=2.0, rate_func=there_and_back)

    # --- 4. Next: molecular orbital theory -----------------------------------------------------------------------------------
    beat(scene, t, 3)
    card = title_card("MOLECULAR ORBITAL THEORY", "NEXT:", small_first=True)
    card.scale(0.95).move_to([0, 0.2, 0])
    tagline = txt("Explained Visually", cfg.FONT["section"], cfg.CYAN).next_to(card, DOWN, buff=0.3)
    scene.play(FadeOut(VGroup(lewis, cloud, deeper, drops, pole)), run_time=0.8)
    scene.play(FadeIn(card, shift=UP * 0.2), run_time=1.2)
    scene.play(FadeIn(tagline, shift=UP * 0.1), run_time=0.8)
    scene.play(Indicate(card.title[1], color=cfg.WHITE, scale_factor=1.03), run_time=1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["21"])
