"""Scene 07 — where molality matters: freezing-point depression.

Two little molecular panels (a picture, not to scale) freeze on a shared
temperature scale: pure water locks into a lattice at 0 °C, the glucose
solution only at about -1.03 °C (dTf = Kf m, ideal dilute solution, Kf from
``concentration_data``). Then why molality is the natural measure here.
"""

from functools import lru_cache

from manim_scenes.common import *

DROP = pm.freezing_point_drop(REF.molality, cd.KF_WATER)
RISE = pm.boiling_point_rise(REF.molality, cd.KB_WATER)
AXIS_X = 0.6


class Scene07Colligative(Scene):
    def construct(self) -> None:
        play_scene(self)


@lru_cache(maxsize=2)
def sphere_pixels(color: str) -> np.ndarray:
    """Render the shared sphere material once, keeping hundreds of beads cheap."""
    camera = Camera(pixel_width=160, pixel_height=160, frame_width=2.02, frame_height=2.02,
                    background_opacity=0)
    camera.capture_mobjects([Ball(ORIGIN, 1.0, color, layers=48).mob])
    return np.array(camera.get_image())


def sphere(point, color: str, radius: float) -> ImageMobject:
    return ImageMobject(sphere_pixels(color)).set_width(2.02 * radius).move_to(point)


class Jiggle(Group):
    """Shaded spheres jiggling about their homes; ``freeze`` (0..1) pulls the
    blue ones onto a lattice while gold ones are pushed aside."""

    def __init__(self, centre, *, cols: int = 7, rows: int = 5, gold: Sequence[int] = (), seed: int = 0,
                 spacing: float = 0.44) -> None:
        super().__init__()
        rng = np.random.default_rng(cfg.SEED + seed)
        centre = np.asarray(centre, dtype=float)
        count = cols * rows
        self.lattice = np.array([centre + [(c - (cols - 1) / 2) * spacing + (0.5 * spacing if r % 2 else 0),
                                           (r - (rows - 1) / 2) * spacing * 0.87, 0]
                                 for r in range(rows) for c in range(cols)])
        self.homes = self.lattice + np.column_stack([rng.uniform(-0.035, 0.035, (count, 2)), np.zeros(count)])
        self.freqs = rng.uniform(1.5, 3.2, (count, 2))
        self.phases = rng.uniform(0, 2 * np.pi, (count, 2))
        self.gold = set(gold)
        for k in range(count):
            self.add(sphere(self.homes[k], cfg.SOLUTE_DEEP if k in self.gold else cfg.SOLVENT,
                            0.15 if k in self.gold else 0.115))
        self.freeze = Knob(0.0)
        self.clock = 0.0
        frame = RoundedRectangle(width=cols * spacing + 0.7, height=rows * spacing * 0.87 + 0.48, corner_radius=0.2,
                                 stroke_color=cfg.MUTED, stroke_width=2, stroke_opacity=0.5, fill_color=cfg.PANEL,
                                 fill_opacity=0.5).move_to(centre)
        self.frame = frame
        self.add_to_back(frame)

    def start(self) -> None:
        self.add_updater(lambda m, dt: m._tick(dt))

    def _tick(self, dt: float) -> None:
        self.clock += dt
        f = self.freeze.value
        wobble = np.sin(self.freqs * self.clock + self.phases) * 0.025
        for k, mob in enumerate(self.submobjects[1:]):
            amp = 1.0 if k in self.gold else (1 - f)
            loose = self.homes[k] + np.array([wobble[k, 0], wobble[k, 1], 0]) * (0.6 + 0.4 * amp)
            target = loose if k in self.gold else loose * (1 - f) + self.lattice[k] * f
            mob.move_to(target)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "07", "Where molality matters")
    head.set_z_index(20)
    chips = VGroup(chip("freezing point", cfg.CYAN), chip("boiling point", cfg.HEAT),
                   chip("vapour pressure", cfg.MUTED)).arrange(RIGHT, buff=0.4).move_to([0, 1.2, 0])
    scene.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips], lag_ratio=0.25), run_time=1.4)
    share = txt("properties that depend on how many solute particles share the solvent", cfg.FONT["small"], cfg.MUTED)
    fit_width(share, 13.0)
    share.move_to([0, -0.2, 0])
    scene.play(FadeIn(share), run_time=0.8)

    # --- 2. Pure water locks into a crystal at 0 °C -------------------------------------------------------------------
    beat(scene, t, 1)
    axis = NumberLine(x_range=[-2, 1, 1], length=5.6, rotation=PI / 2, include_numbers=False, color=cfg.MUTED,
                      stroke_width=3).move_to([AXIS_X, -0.45, 0])
    nums = VGroup(*[txt(f"{v} °C", cfg.FONT["tiny"], cfg.MUTED).next_to(axis.n2p(v), RIGHT, buff=0.2) for v in (1, 0, -1, -2)])
    pure = Jiggle([-4.4, 1.25, 0], seed=1)
    pure_name = txt("pure water", cfg.FONT["label"], cfg.SOLVENT).next_to(pure.frame, UP, buff=0.15)
    scene.play(FadeOut(head), FadeOut(chips), FadeOut(share), run_time=0.6)
    scene.play(FadeIn(pure), FadeIn(pure_name), Create(axis), FadeIn(nums), run_time=1.2)
    pure.start()
    temp = Knob(1.0)
    pointer = always_redraw(lambda: Triangle(stroke_width=0, fill_color=cfg.CYAN, fill_opacity=1).scale(0.16)
                            .rotate(-PI / 2).move_to(axis.n2p(temp.value) + LEFT * 0.3))
    scene.add(pointer)
    scene.play(temp.to(pointer, 0.0), run_time=2.2)
    scene.play(pure.freeze.to(pure, 1.0), run_time=1.6)
    frozen = VGroup(txt("freezes", cfg.FONT["small"], cfg.CYAN), txt("at 0 °C", cfg.FONT["small"], cfg.CYAN))
    frozen.arrange(DOWN, buff=0.08).next_to(pure.frame, RIGHT, buff=0.25)
    scene.play(FadeIn(frozen), run_time=0.6)

    # --- 3. Glucose gets in the way: colder before it freezes ---------------------------------------------------------
    beat(scene, t, 2)
    sol = Jiggle([-4.4, -2.15, 0], gold=(9, 25), seed=2)
    sol_name = txt("glucose solution", cfg.FONT["label"], cfg.SOLUTE).next_to(sol.frame, UP, buff=0.18)
    note = txt("a picture, not to scale", cfg.FONT["tiny"], cfg.MUTED).move_to([1.6, -3.8, 0])
    scene.play(FadeIn(sol), FadeIn(sol_name), FadeIn(note), run_time=1.0)
    sol.start()
    still = VGroup(txt("still", cfg.FONT["small"], cfg.SOLUTE), txt("liquid", cfg.FONT["small"], cfg.SOLUTE))
    still.arrange(DOWN, buff=0.08).next_to(sol.frame, RIGHT, buff=0.25)
    scene.play(FadeIn(still), run_time=0.6)
    scene.play(temp.to(pointer, -DROP), FadeOut(still), run_time=3.0)
    scene.play(sol.freeze.to(sol, 1.0), run_time=1.6)
    low = Line(axis.n2p(-DROP) + LEFT * 0.25, axis.n2p(-DROP) + RIGHT * 0.25, stroke_color=cfg.SOLUTE, stroke_width=5)
    scene.play(Create(low), run_time=0.5)

    # --- 4. dT = Kf m ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    law = eq([r"\Delta T_f", "=", r"K_f", r"\cdot", "m"], cfg.FONT["title"]).move_to([4.9, 2.55, 0])
    law[4].set_color(cfg.SOLVENT_MASS)
    scene.play(Write(law), run_time=1.4)
    prop = txt("proportional to molality", cfg.FONT["small"], cfg.SOLVENT_MASS).next_to(law, DOWN, buff=0.25)
    scene.play(FadeIn(prop), run_time=0.7)

    # --- 5. Kf for water ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    kf = eq(rf"K_f \approx {fx(cd.KF_WATER, 2)}\ ^\circ\mathrm{{C}}\ \text{{per}}\ \mathrm{{m}}", cfg.FONT["body"])
    fit_width(kf, 5.6)
    kf.move_to([4.9, 0.7, 0])
    scene.play(FadeOut(prop), Write(kf), run_time=1.3)

    # --- 6. 1.86 x 0.556 = about 1.03 °C ------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    calc = eq([rf"{fx(cd.KF_WATER, 2)} \times {m_TEXT}", r"\approx", rf"{fx(DROP, 2)}\ ^\circ\mathrm{{C}}"], cfg.FONT["body"])
    calc[2].set_color(cfg.RESULT)
    fit_width(calc, 5.6)
    calc.move_to([4.9, -0.6, 0])
    scene.play(Write(calc), run_time=1.5)
    freeze_at = txt(f"freezes near −{fx(DROP, 2)} °C", cfg.FONT["small"], cfg.SOLUTE).next_to(sol.frame, DOWN, buff=0.12)
    scene.play(FadeIn(freeze_at), Indicate(low, color=cfg.WHITE), run_time=1.0)

    # --- 7. Boiling shifts too ------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    boil = eq([r"\Delta T_b", "=", r"K_b \cdot m", r"\approx", rf"{fx(RISE, 2)}\ ^\circ\mathrm{{C}}"], cfg.FONT["body"])
    boil[4].set_color(cfg.HEAT)
    fit_width(boil, 5.6)
    boil.move_to([4.9, -2.0, 0])
    scene.play(Write(boil), run_time=1.5)
    up = txt("boils higher", cfg.FONT["small"], cfg.HEAT).next_to(boil, DOWN, buff=0.2)
    scene.play(FadeIn(up), run_time=0.6)

    # --- 8. Why molality? A ratio of particles ---------------------------------------------------------------------------------------
    beat(scene, t, 7)
    for jig in (pure, sol):
        jig.clear_updaters()
    scene.remove(pointer)
    scene.play(FadeOut(Group(pure, pure_name, frozen, sol, sol_name, note, freeze_at, axis, nums, low, kf, calc, boil, up)),
               run_time=0.6)
    scene.play(law.animate.move_to([-3.6, 2.4, 0]), run_time=0.6)
    one = sphere([-5.4, -0.4, 0], cfg.SOLUTE_DEEP, 0.2)
    crowd = Group(*[sphere([-4.2 + (k % 10) * 0.3, 0.9 - (k // 10) * 0.3, 0], cfg.SOLVENT, 0.11)
                   for k in range(100)])
    ratio = txt("solute particles : solvent particles", cfg.FONT["label"], cfg.WHITE).move_to([-3.6, -2.6, 0])
    fit_width(ratio, 7.2)
    scene.play(FadeIn(one, scale=0.5), LaggedStart(*[FadeIn(b, scale=0.5) for b in crowd], lag_ratio=0.01),
               run_time=1.6)
    scene.play(FadeIn(ratio), run_time=0.7)

    # --- 9. Molality is built from those two things ------------------------------------------------------------------------------------
    beat(scene, t, 8)
    m_rule = fraction("m", r"n_{\text{solute}}", r"m_{\text{solvent}}", cfg.AMOUNT, cfg.SOLVENT_MASS, cfg.FONT["section"])
    m_rule.move_to([3.9, 1.6, 0])
    scene.play(Write(m_rule), run_time=1.3)
    per_kg = eq(rf"1\ \mathrm{{kg\ water}} \approx {fx(1000 / pm.M_WATER, 1)}\ \mathrm{{mol}}", cfg.FONT["body"], cfg.SOLVENT_MASS)
    fixed_n = txt("a fixed number of molecules", cfg.FONT["small"], cfg.SOLVENT_MASS)
    kg_group = VGroup(per_kg, fixed_n).arrange(DOWN, buff=0.2).move_to([3.9, -0.6, 0])
    scene.play(FadeIn(kg_group, shift=UP * 0.15), crowd.animate(rate_func=there_and_back).scale(1.03), run_time=1.6)

    # --- 10. Masses don't change with temperature -----------------------------------------------------------------------------------------
    beat(scene, t, 9)
    valid = chip("fixed composition: m stays fixed", cfg.RESULT).move_to([3.9, -2.4, 0])
    fit_width(valid, 7.4)
    scene.play(FadeIn(valid, shift=UP * 0.15), run_time=0.8)
    scene.play(Circumscribe(m_rule[5], color=cfg.SOLVENT_MASS, buff=0.08), run_time=1.4)

    # --- 11. An experiment ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(Group(one, crowd, ratio, law, m_rule, kg_group, valid)), run_time=0.8)
    question = VGroup(txt("Can a concentration change", cfg.FONT["section"], cfg.WHITE),
                      txt("with nothing added or removed?", cfg.FONT["section"], cfg.GOLD)).arrange(DOWN, buff=0.3)
    scene.play(FadeIn(question, shift=UP * 0.2), run_time=1.2)
    scene.play(Indicate(question[1], color=cfg.WHITE, scale_factor=1.04), run_time=1.6)
    scene.play(question.animate.scale(1.05), run_time=7.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["07"])
