"""Scene 08 — the film's first big reveal: warm a sealed cylinder of the
reference solution from 20 to 70 °C. The molecules speed up, the liquid
expands (191.0 -> 195 mL, if it expands like water: ``concentration_data``),
and two live meters disagree: molarity falls, molality does not move.

Both meters read the cylinder's own ``volume`` every frame, so the numbers
on screen are the picture's numbers.
"""

from manim_scenes.common import *

CYL = pm.cylinder_profile(radius=0.62, height=4.6, mark_y=4.2, mark_mL=200.0)
HOT = cd.heated()
METER_X = 4.75
INSET_LOW, INSET_HIGH = 187.0, 199.0


class Scene08Temperature(Scene):
    def construct(self) -> None:
        play_scene(self)


class Inset(VGroup):
    """A magnified slice of the cylinder's scale, 187-199 mL, with the liquid in it."""

    def __init__(self, glass: Glassware, centre, height: float = 3.6, width: float = 1.9) -> None:
        super().__init__()
        self.glass, self.h = glass, height
        self.window = RoundedRectangle(width=width, height=height, corner_radius=0.18, stroke_color=cfg.GLASS,
                                       stroke_width=3, fill_color=cfg.PANEL, fill_opacity=0.9).move_to(centre)
        self.bottom = self.window.get_bottom()[1]
        ticks = VGroup()
        labels = VGroup()
        for v in range(int(INSET_LOW) + 1, int(INSET_HIGH)):
            y = self.y_for(v)
            major = v % 5 == 0
            ticks.add(Line([self.window.get_left()[0], y, 0], [self.window.get_left()[0] + (0.6 if major else 0.32), y, 0],
                           stroke_color=cfg.WHITE, stroke_width=3 if major else 2, stroke_opacity=0.85))
            if major:
                labels.add(txt(str(v), cfg.FONT["tiny"], cfg.WHITE).move_to([self.window.get_center()[0] + 0.35, y, 0]))
        self.liquid = always_redraw(self._liquid)
        self.add(self.window, self.liquid, ticks, labels)

    def y_for(self, volume: float) -> float:
        return self.bottom + (volume - INSET_LOW) / (INSET_HIGH - INSET_LOW) * self.h

    def _liquid(self) -> VGroup:
        top = self.y_for(self.glass.volume)
        w = self.window.width - 0.12
        x = self.window.get_center()[0]
        body = Rectangle(width=w, height=max(top - self.bottom - 0.06, 0.01), stroke_width=0, fill_color=cfg.LIQUID,
                         fill_opacity=0.55)
        body.move_to([x, (top + self.bottom + 0.06) / 2, 0])
        meniscus = ArcBetweenPoints([x - w / 2, top + 0.06, 0], [x + w / 2, top + 0.06, 0], angle=0.5,
                                    stroke_color=cfg.CYAN, stroke_width=5)
        return VGroup(body, meniscus)


def side_caption(body: str, color: str) -> Text:
    """A bottom caption kept clear of the cylinder on the left."""
    line = caption(body, color)
    fit_width(line, 9.2)
    return line.set_x(2.75)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "08", "The temperature experiment")
    stage, glass, swarm = solution_stage([-4.7, -3.75, 0], profile=CYL, zoom=1.2, solvent=260, solute=3, seed=8,
                                         lid=True, ticks=[CYL.height_for(v) for v in range(20, 200, 20)],
                                         spin=0.15, amplitude=0.05, solvent_radius=0.04, solute_radius=0.1)
    show(scene, stage, 1.4)
    sealed = txt("sealed", cfg.FONT["small"], cfg.MUTED).move_to([-2.7, 2.15, 0])
    sealed_arrow = Arrow([-3.3, 2.1, 0], [-4.2, 1.9, 0], buff=0, color=cfg.MUTED, stroke_width=4, tip_length=0.2)
    scene.play(FadeIn(sealed), GrowArrow(sealed_arrow), run_time=0.9)

    # --- 2. It reads 191 mL -----------------------------------------------------------------------------------
    beat(scene, t, 1)
    inset = Inset(glass, [-1.6, -0.5, 0])
    link = dashed_path(stage.screen_point(glass.surface_point()) + RIGHT * 0.7, inset.window.get_left() + LEFT * 0.05,
                       cfg.MUTED, 2.4, 0.6)
    readout = VGroup(live_number(lambda: glass.volume, 0, cfg.FONT["body"], cfg.WHITE),
                     txt("mL", cfg.FONT["small"], cfg.WHITE)).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
    readout.next_to(inset, UP, buff=0.25)
    readout[0].add_updater(lambda m: readout.arrange(RIGHT, buff=0.2, aligned_edge=DOWN).next_to(inset, UP, buff=0.25))
    scene.play(FadeOut(head), FadeOut(VGroup(sealed, sealed_arrow)), FadeIn(inset), Create(link), run_time=1.2)
    scene.play(FadeIn(readout), run_time=0.7)

    # --- 3. Two meters ---------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    molarity = Meter("molarity", lambda: REF.n_solute / (glass.volume / 1000.0), 3, r"\mathrm{M}", cfg.VOLUME, width=4.8)
    molality = Meter("molality", lambda: REF.molality, 3, r"\mathrm{m}", cfg.SOLVENT_MASS, width=4.8)
    molarity.move_to([METER_X, 2.05, 0])
    molality.move_to([METER_X, -1.3, 0])
    scene.play(FadeIn(molarity, shift=LEFT * 0.2), run_time=0.9)
    scene.play(FadeIn(molality, shift=LEFT * 0.2), run_time=0.9)

    # --- 4. Warm it ------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    thermo = Thermometer([1.25, -0.6, 0], low=0, high=100, height=3.8)
    degrees = VGroup(live_number(lambda: thermo.celsius.value, 0, cfg.FONT["small"], cfg.HEAT),
                     txt("°C", cfg.FONT["small"], cfg.HEAT)).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
    degrees.next_to(thermo, UP, buff=0.2)
    degrees[0].add_updater(lambda m: degrees.arrange(RIGHT, buff=0.2, aligned_edge=DOWN).next_to(thermo, UP, buff=0.2))
    heat = VGroup(*[Ellipse(width=2.2 * k, height=0.5 * k, stroke_width=0, fill_color=cfg.HEAT, fill_opacity=0.0)
                    for k in (1.0, 0.75, 0.5)]).move_to([-4.7, -3.85, 0])
    scene.play(FadeIn(thermo), FadeIn(degrees), run_time=0.8)
    scene.play(*[h.animate.set_fill(opacity=0.22) for h in heat], thermo.celsius.to(thermo, 45.0),
               set_attr(stage, swarm, "speed", 1.8), run_time=4.5)

    # --- 5. The molecules move faster ---------------------------------------------------------------------------------------
    beat(scene, t, 4)
    faster = txt("faster, further apart", cfg.FONT["small"], cfg.HEAT).move_to([-4.7, 2.6, 0])
    scene.play(FadeIn(faster), thermo.celsius.to(thermo, 70.0), set_attr(stage, swarm, "speed", 2.6),
               set_attr(stage, swarm, "amplitude", 0.09), run_time=6.0)

    # --- 6. The liquid expands: about 195 mL ------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(glass.set_volume(HOT.volume_mL), run_time=6.5)
    scene.play(Indicate(readout, color=cfg.GOLD, scale_factor=1.1), run_time=1.0)

    # --- 7. Molarity has dropped ----------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    drop = numbers_fraction(rf"{N_SOLUTE}\ \mathrm{{mol}}", rf"{fx(HOT.volume_L, 3)}\ \mathrm{{L}}", fx(HOT.molarity, 3),
                            cfg.AMOUNT, cfg.VOLUME, cfg.FONT["label"], result_color=cfg.WARNING)
    drop.next_to(molarity, DOWN, buff=0.25)
    down = Arrow(UP * 0.4, DOWN * 0.4, buff=0, color=cfg.WARNING, stroke_width=8).next_to(molarity.row, RIGHT, buff=0.35)
    scene.play(FadeOut(faster), Write(drop), GrowArrow(down), run_time=1.5)
    scene.play(Indicate(molarity.value, color=cfg.WARNING, scale_factor=1.12), run_time=1.0)

    # --- 8. Molality didn't move ------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    hold = numbers_fraction(rf"{N_SOLUTE}\ \mathrm{{mol}}", rf"{KG}\ \mathrm{{kg}}", m_TEXT, cfg.AMOUNT, cfg.SOLVENT_MASS,
                            cfg.FONT["label"])
    hold.next_to(molality, DOWN, buff=0.25)
    same = check_mark(0.26).next_to(molality.row, RIGHT, buff=0.35)
    scene.play(Write(hold), Create(same), run_time=1.5)
    scene.play(Indicate(molality.value, color=cfg.RESULT, scale_factor=1.12), run_time=1.0)

    # --- 9. Nothing added, nothing removed ----------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    nothing = side_caption("No glucose removed. No water added.", cfg.WHITE)
    scene.play(FadeOut(VGroup(drop, hold)), run_time=0.5)
    scene.play(FadeIn(nothing, shift=UP * 0.15), run_time=0.8)

    # --- 10. Molarity <- volume <- temperature -----------------------------------------------------------------------------------------
    beat(scene, t, 9)
    chain_a = side_caption("molarity ← volume ← temperature", cfg.VOLUME)
    scene.play(fade_through(nothing, chain_a), run_time=1.0)
    scene.remove(nothing)
    scene.play(glass.set_glow(1.0), run_time=1.0)

    # --- 11. Molality <- masses -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    chain_b = side_caption("molality ← masses: unchanged", cfg.SOLVENT_MASS)
    scene.play(fade_through(chain_a, chain_b), glass.set_glow(0.0), set_attr(stage, swarm, "solvent_glow", 1.0), run_time=1.0)
    scene.remove(chain_a)

    # --- 12. Cool it back down ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    scene.play(FadeOut(VGroup(down, same)), set_attr(stage, swarm, "solvent_glow", 0.0), run_time=0.6)
    scene.play(*[h.animate.set_fill(opacity=0.0) for h in heat], thermo.celsius.to(thermo, 20.0),
               glass.set_volume(REF.volume_mL), set_attr(stage, swarm, "speed", 1.0),
               set_attr(stage, swarm, "amplitude", 0.05), run_time=6.5)
    scene.play(Indicate(molarity.value, color=cfg.VOLUME, scale_factor=1.12), run_time=1.0)

    # --- 13. Two measures, behaving differently --------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    final = side_caption("Same glucose. Same water. Two behaviours.", cfg.GOLD)
    scene.play(fade_through(chain_b, final), run_time=1.0)
    scene.remove(chain_b)
    scene.play(thermo.celsius.to(thermo, 70.0), glass.set_volume(HOT.volume_mL), set_attr(stage, swarm, "speed", 2.4),
               run_time=7.5)
    scene.play(thermo.celsius.to(thermo, 20.0), glass.set_volume(REF.volume_mL), set_attr(stage, swarm, "speed", 1.0),
               run_time=7.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["08"])
