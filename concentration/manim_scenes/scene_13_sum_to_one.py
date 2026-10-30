"""Scene 13 — mole fractions add to one, and Raoult's law: water's vapour
pressure over an ideal solution is x_water times the pure value. The
escaping-vapour animation is a picture; the two pressure readings come from
``physics_models.vapour_pressure_fraction``.
"""

from manim_scenes.common import *
from manim_scenes.stage3d import _sphere_pixels
from functools import lru_cache

X_W = fx(REF.x_solvent, 5)


class Scene13SumToOne(Scene):
    def construct(self) -> None:
        play_scene(self)


@lru_cache(maxsize=4)
def _mist_pixels(variant: int = 0) -> np.ndarray:
    """A feathered, irregular wisp: a visual cue for dispersing water above the surface."""
    y, x = np.mgrid[-1:1:192j, -1:1:192j]
    phase = variant * 0.9
    warped_x = x + 0.12 * np.sin(5 * y + phase)
    warped_y = y + 0.06 * np.sin(5 * x - phase)
    density = np.exp(-2 * ((warped_x / 0.52) ** 2 + (warped_y / 0.38) ** 2))
    density *= 0.82 + 0.10 * np.sin(10 * x + 5 * y + phase) + 0.08 * np.cos(12 * y - 4 * x)
    density /= density.max()
    pixels = np.zeros((192, 192, 4), dtype=np.uint8)
    pixels[:, :, :3] = [190, 222, 235]
    pixels[:, :, 3] = np.round(255 * density).astype(np.uint8)
    return pixels


class Vapour(Group):
    """Shaded liquid particles rise briefly, soften into mist, spread and fade.

    The visible wisps illustrate dispersal; the quantitative pressure readings
    are supplied separately by the physical model.
    """

    def __init__(self, centre, *, width: float = 5.0, rate: float = 1.0, seed: int = 0, gold: bool = False) -> None:
        super().__init__()
        rng = np.random.default_rng(cfg.SEED + seed)
        centre = np.asarray(centre, dtype=float)
        liquid = Rectangle(width=width, height=1.9, stroke_width=0, fill_color=cfg.LIQUID, fill_opacity=0.55)
        liquid.move_to(centre + DOWN * 0.95)
        surface = Ellipse(width=width,height=.42,stroke_color=cfg.CYAN,stroke_width=2.5,
                          fill_color=mu.mix(cfg.LIQUID,cfg.WHITE,.2),fill_opacity=.4).move_to(centre)
        rim = Ellipse(width=width+.12,height=.42,stroke_color=cfg.GLASS,stroke_width=2,
                      stroke_opacity=.6,fill_opacity=0).move_to(centre)
        floor = Ellipse(width=width,height=.42,stroke_color=cfg.GLASS,stroke_width=2,
                        stroke_opacity=.45,fill_color=cfg.LIQUID,fill_opacity=.25).move_to(centre+DOWN*1.9)
        reflection = VGroup(*[Line(centre+np.array([side*(width/2-.12),-.15,0]),
                                  centre+np.array([side*(width/2-.12),-1.75,0]),
                                  stroke_color=cfg.GLASS,stroke_width=5 if side<0 else 2,stroke_opacity=.2)
                               for side in (-1,1)])
        self.top = centre[1]
        inside = Group()
        for _ in range(34):
            particle = ImageMobject(_sphere_pixels(cfg.SOLVENT)).set_width(rng.uniform(0.16, 0.21))
            particle.move_to(centre + np.array([rng.uniform(-width / 2 + 0.2, width / 2 - 0.2),
                                               -rng.uniform(0.25, 1.7), 0]))
            inside.add(particle)
        if gold:
            inside.add(ImageMobject(_sphere_pixels(cfg.SOLUTE_DEEP)).set_width(0.30)
                       .move_to(centre + np.array([0.6, -0.9, 0])))
        self.inside = inside
        self.count = 10
        self.xs = rng.uniform(-width / 2 + 0.3, width / 2 - 0.3, self.count)
        self.phases = rng.uniform(0, 1, self.count)
        self.rate = rate
        self.clock = 0.0
        self.escapees = Group(*[Group(ImageMobject(_sphere_pixels(cfg.SOLVENT)).set_width(0.17),
                                      ImageMobject(_mist_pixels(k % 4))) for k in range(self.count)])
        self.centre = centre
        self.add(liquid, floor, inside, surface, rim, reflection, self.escapees)
        self._place()

    def start(self) -> None:
        self.add_updater(lambda m, dt: m._tick(dt))

    def _tick(self, dt: float) -> None:
        self.clock += dt
        self._place()

    def _place(self) -> None:
        for k, (particle, mist) in enumerate(self.escapees):
            u = (self.clock * 0.32 + self.phases[k]) % 1.0
            shown = 1.0 if k < round(self.count * self.rate) else 0.0
            position = np.array([self.centre[0] + self.xs[k] + 0.22 * np.sin(5 * u + k) * u,
                                 self.top + 0.03 + 1.8 * u, 0])
            # Fade in at the surface and dissolve before the escapee gets high.
            emerge = mu.smoothstep(np.clip(u / 0.08, 0, 1))
            dissolve = mu.smoothstep(np.clip((u - 0.08) / 0.25, 0, 1))
            disperse = 1 - mu.smoothstep(np.clip((u - 0.42) / 0.58, 0, 1))
            particle.move_to(position).set_opacity(shown * emerge * (1 - dissolve))
            mist.set_width(0.45 + 1.25 * u).move_to(position + UP * 0.06)
            mist.set_opacity(shown * 0.42 * dissolve * disperse)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "13", "Mole fractions add to one")
    bar_w = 12.0
    gold_w = bar_w * REF.x_solute
    blue = Rectangle(width=bar_w - gold_w, height=0.8, stroke_width=0, fill_color=cfg.SOLVENT, fill_opacity=0.85)
    gold = Rectangle(width=gold_w, height=0.8, stroke_width=0, fill_color=cfg.SOLUTE, fill_opacity=1)
    bar = VGroup(blue, gold).arrange(RIGHT, buff=0).move_to([0, 2.2, 0])
    frame = SurroundingRectangle(bar, buff=0.06, color=cfg.WHITE, stroke_width=2)
    tag_g = eq(r"x_{\text{glucose}}", cfg.FONT["body"], cfg.SOLUTE).next_to(gold, UP, buff=0.18).shift(LEFT * 0.3)
    scene.play(GrowFromEdge(bar, LEFT), Create(frame), run_time=1.2)
    scene.play(FadeIn(tag_g), run_time=0.5)

    # --- 2. x of water -------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    tag_w = eq(r"x_{\text{water}}", cfg.FONT["body"], cfg.SOLVENT).next_to(blue, DOWN, buff=0.18)
    xw = eq([r"x_{\text{water}}", "=", rf"\frac{{{N_SOLVENT}}}{{{fx(REF.n_total, 1)}}}", r"\approx", X_W], cfg.FONT["section"])
    xw[0].set_color(cfg.SOLVENT)
    xw[4].set_color(cfg.SOLVENT)
    xw.move_to([0, 0.2, 0])
    scene.play(FadeIn(tag_w), Write(xw), run_time=1.8)
    scene.play(FadeOut(head), run_time=0.9)

    # --- 3. Add them: exactly one ----------------------------------------------------------------------------------------
    beat(scene, t, 2)
    total = eq([X_TEXT, "+", X_W, "=", "1"], cfg.FONT["title"]).move_to([0, -1.6, 0])
    total[0].set_color(cfg.SOLUTE)
    total[2].set_color(cfg.SOLVENT)
    total[4].set_color(cfg.RESULT)
    scene.play(Write(total[:3]), run_time=1.4)
    scene.play(Write(total[3:]), run_time=0.8)
    scene.play(Indicate(total[4], color=cfg.WHITE, scale_factor=1.4), frame.animate.set_stroke(cfg.RESULT, width=5),
               run_time=1.0)

    # --- 4. Every molecule has to be something --------------------------------------------------------------------------------
    beat(scene, t, 3)
    always = caption("Every molecule is something: the fractions always add to 1.", cfg.RESULT)
    scene.play(FadeIn(always, shift=UP * 0.15), run_time=0.8)
    scene.play(Indicate(bar, color=cfg.WHITE, scale_factor=1.02), run_time=1.2)

    # --- 5. Molecules competing to escape -----------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(VGroup(bar, frame, tag_g, tag_w, xw, total, always)), run_time=0.7)
    pure = Vapour([-3.7, -1.2, 0], rate=1.0, seed=1)
    sol = Vapour([3.7, -1.2, 0], rate=1.0, seed=2, gold=True)
    names = VGroup(txt("pure water", cfg.FONT["label"], cfg.SOLVENT).move_to([-3.7, -3.55, 0]),
                   txt("our solution", cfg.FONT["label"], cfg.SOLUTE).move_to([3.7, -3.55, 0]))
    scene.play(FadeIn(pure), FadeIn(sol), FadeIn(names), run_time=1.0)
    pure.start()
    sol.start()

    # --- 6. Breaking free: vapour pressure ----------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    escape = txt("breaking free → vapour pressure", cfg.FONT["body"], cfg.CYAN).move_to([0, 1.55, 0])
    fit_width(escape, 12.0)
    scene.play(FadeIn(escape, shift=UP * 0.15), run_time=0.9)

    # --- 7. Raoult's law ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    law = eq([r"P_{\text{water}}", "=", r"x_{\text{water}}", r"\cdot", r"P^{\circ}_{\text{water}}"], cfg.FONT["title"])
    law[2].set_color(cfg.AMOUNT)
    law.move_to([0, 2.45, 0])
    raoult = txt("Raoult's law (ideal solution)", cfg.FONT["small"], cfg.MUTED).next_to(law, DOWN, buff=0.2)
    scene.play(FadeOut(escape), Write(law), run_time=1.6)
    scene.play(FadeIn(raoult), run_time=0.6)

    # --- 8. About one percent lower ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    read_p = eq(rf"P / P^\circ = {fx(1.0, 3)}", cfg.FONT["body"], cfg.SOLVENT).move_to([-3.7, 1.45, 0])
    read_s = eq(rf"P / P^\circ = {fx(pm.vapour_pressure_fraction(REF.x_solvent), 3)}", cfg.FONT["body"], cfg.RESULT)
    read_s.move_to([3.7, 1.45, 0])
    scene.play(FadeOut(raoult), run_time=0.4)
    scene.play(FadeIn(read_p), FadeIn(read_s), run_time=0.7)
    lower = txt("about 1% lower", cfg.FONT["label"], cfg.RESULT).next_to(read_s, DOWN, buff=0.2)
    scene.play(FadeIn(lower), run_time=0.7)

    # --- 9. Where it matters more ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    for v in (pure, sol):
        v.clear_updaters()
    scene.play(FadeOut(Group(pure, sol, names, read_p, read_s, lower)), run_time=0.7)
    uses = VGroup(*[chip(w, cfg.AMOUNT) for w in ("strong solutions", "mixtures of liquids", "the vapour above them")])
    uses.arrange(RIGHT, buff=0.35).move_to([0, 0.4, 0])
    fit_width(uses, 14.0)
    scene.play(LaggedStart(*[FadeIn(u, shift=UP * 0.2) for u in uses], lag_ratio=0.3), run_time=1.6)

    # --- 10. Next: percent ----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(uses), FadeOut(law), run_time=0.7)
    percent = txt("%", 220, cfg.GOLD).move_to([0, 0.2, 0])
    glow = percent.copy().set_fill(opacity=0).set_stroke(cfg.GOLD, width=24, opacity=0.15)
    decorative(glow)
    scene.play(FadeIn(percent, scale=0.6), FadeIn(glow, scale=0.6), run_time=1.2)
    scene.play(percent.animate.scale(1.1), glow.animate.scale(1.1), run_time=8.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["13"])
