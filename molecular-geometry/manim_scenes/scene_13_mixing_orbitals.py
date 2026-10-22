"""Chapter 13 — mixing orbitals: from s and p to the sp hybrid.

Every orbital shape is computed from psi = cos(a) psi_s + sin(a) psi_p
(``utils.orbital_models``; drawn as the textbook polar plot of its angular
density, blue where psi > 0 and rose where psi < 0). The dial drives the
mixing angle a of one orbital continuously from pure s to pure p, with a
live read-out of its s character, cos^2(a). Two sp hybrids are then made
as s + p and s - p, and the two unused p orbitals stay behind in purple.
"""

from manim_scenes.common import *

ORB_AT = np.array([-2.4, -0.2, 0])


class Scene13MixingOrbitals(Scene):
    def construct(self) -> None:
        play_scene(self)


class Dial(VGroup):
    """A slider from pure s (left) to pure p (right) that follows an orbital's mixing angle."""

    def __init__(self, orbital: Orbital, at, length: float = 6.0) -> None:
        super().__init__()
        at = np.asarray(at, dtype=float)
        self.orbital, self.length = orbital, length
        self.left, self.right = at + LEFT * length / 2, at + RIGHT * length / 2
        self.track = Line(self.left, self.right, stroke_color=cfg.MUTED, stroke_width=8)
        self.ends = VGroup(txt("s", cfg.FONT["section"], cfg.BLUE).next_to(self.left, LEFT, buff=0.3),
                           txt("p", cfg.FONT["section"], cfg.BLUE).next_to(self.right, RIGHT, buff=0.3))
        sp = self.spot(om.SP_ALPHA["sp"])
        self.sp_tick = VGroup(Line(sp + DOWN * 0.22, sp + UP * 0.22, stroke_color=cfg.GOLD, stroke_width=6),
                              txt("sp", cfg.FONT["label"], cfg.GOLD).move_to(sp + UP * 0.6))
        self.knob = VGroup(Circle(radius=0.2, stroke_width=0, fill_color=cfg.WHITE, fill_opacity=1),
                           Circle(radius=0.34, stroke_width=0, fill_color=cfg.CYAN, fill_opacity=0.3))
        self._labels: dict[int, Text] = {}
        self.readout = VGroup()
        self.add(self.track, self.ends, self.sp_tick, self.knob, self.readout)
        self.add_updater(lambda m: m._follow())
        self._follow()

    def spot(self, alpha: float) -> np.ndarray:
        return self.left + (self.right - self.left) * (alpha / (np.pi / 2))

    def _follow(self) -> None:
        alpha = self.orbital.plus.alpha
        self.knob.move_to(self.spot(alpha))
        percent = int(round(100 * np.cos(alpha) ** 2))
        if percent not in self._labels:
            self._labels[percent] = txt(f"{percent}% s", cfg.FONT["body"], cfg.WHITE)
        label = self._labels[percent]
        label.move_to(self.knob.get_center() + DOWN * 0.8)
        self.readout.submobjects = [label]


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "13", "Mixing orbitals")

    # --- 1-2. VSEPR gives directions; which orbitals point that way? ---------------------------------------------
    regions_stage = Stage([0, -0.1, 0], zoom=1.0, yaw=0.45, pitch=0.3, spin=0.3)
    RegionModel(regions_stage, pm.ideal_directions(4))
    show(scene, regions_stage, 1.0)
    dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    which = caption("Which orbitals on carbon point this way?", cfg.CYAN)
    scene.play(FadeIn(which), run_time=0.9)

    # --- 3. One 2s sphere, three 2p pairs of lobes ------------------------------------------------------------------
    beat(scene, t, 2)
    hide(scene, regions_stage, 0.8, FadeOut(which))
    s_stage = Stage([-4.6, 0.25, 0], zoom=1.0, pitch=0.25, sway=0.2)
    Orbital(s_stage, ORIGIN, RIGHT, 0.0, units=1.05)
    s_stage.add_body(element_ball("C", ORIGIN, scale=0.35, label=False))
    p_stage = Stage([2.2, 0.25, 0], zoom=1.0, yaw=0.55, pitch=0.35, sway=0.12)
    p_orbs = [Orbital(p_stage, ORIGIN, axis, np.pi / 2, units=0.82) for axis in (RIGHT, UP, OUT)]
    for orb in p_orbs:
        orb.set_presence(0.0)
    p_stage.add_body(element_ball("C", ORIGIN, scale=0.35, label=False))
    # Keep both labels in a fixed row beneath the full rotating lobe envelope.
    names = VGroup(txt("2s", cfg.FONT["section"], cfg.BLUE).move_to([-4.6, -2.95, 0]),
                   txt("2p", cfg.FONT["section"], cfg.BLUE).move_to([2.2, -2.95, 0]))
    show(scene, s_stage, 1.0, FadeIn(names[0]))
    show(scene, p_stage, 0.6, FadeIn(names[1]))
    for orb in p_orbs:
        scene.play(*orb.fade(1.0), run_time=0.9)
    phase = VGroup(txt("+", cfg.FONT["section"], cfg.PHASE_PLUS), txt("−", cfg.FONT["section"], cfg.PHASE_MINUS))
    phase.arrange(RIGHT, buff=0.5).move_to([6.4, 2.6, 0])
    phase_note = txt("wave sign", cfg.FONT["small"], cfg.MUTED).next_to(phase, DOWN, buff=0.25)
    scene.play(FadeIn(phase), FadeIn(phase_note), run_time=0.8)

    # --- 4. At right angles ---------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    right = AngleArc(ORIGIN, RIGHT, UP, 1.0, label=degrees_label(90, cfg.FONT["body"]), label_gap=0.5)
    right.presence = 0.0
    p_stage.add_overlay(right)
    scene.play(p_stage.fade(right, 1.0), run_time=1.0)
    scene.play(p_stage.set_spin(0.3), run_time=1.5)

    # --- 5. Methane's bonds are 109.5 apart: no match ----------------------------------------------------------------------
    beat(scene, t, 4)
    tetra = [Segment(ORIGIN, d * 3.1, cfg.GOLD, 5, 0.95, dashed=True) for d in pm.ideal_directions(4)]
    for seg in tetra:
        seg.presence = 0.0
    p_stage.add_body(*tetra)
    mismatch = caption("Bonds at 109.5°, orbitals at 90°: no match", cfg.RED)
    scene.play(p_stage.fade(right, 0.0), *[p_stage.fade(s, 1.0) for s in tetra], FadeIn(mismatch), run_time=1.4)
    scene.play(p_stage.set_spin(0.0), run_time=1.0)

    # --- 6. Wave functions can be added -----------------------------------------------------------------------------------------
    beat(scene, t, 5)
    hide(scene, s_stage, 0.6, FadeOut(names), FadeOut(mismatch), FadeOut(phase), FadeOut(phase_note))
    hide(scene, p_stage, 0.5)
    mix = eq([r"\psi", "=", r"\cos\alpha\,", r"\psi_s", "+", r"\sin\alpha\,", r"\psi_p"], cfg.FONT["hero"])
    mix[3].set_color(cfg.BLUE)
    mix[6].set_color(cfg.BLUE)
    mix[2].set_color(cfg.GOLD)
    mix[5].set_color(cfg.GOLD)
    mix.move_to([0, 0.6, 0])
    added = caption("Orbitals are wave functions. Wave functions add.", cfg.WHITE)
    scene.play(Write(mix), FadeIn(added), run_time=2.0)

    # --- 7. A new function: a hybrid ------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    hybrid = txt("a hybrid orbital", cfg.FONT["body"], cfg.GOLD).next_to(mix, DOWN, buff=0.6)
    scene.play(FadeIn(hybrid, shift=UP * 0.1), Indicate(mix[0], color=cfg.GOLD), run_time=1.2)

    # --- 8. Turn the dial ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    stage = Stage(ORB_AT + LEFT * 0.6, zoom=1.0, yaw=0.0, pitch=0.2, sway=0.15)
    orbital = Orbital(stage, ORIGIN, RIGHT, 0.0, units=0.78)
    stage.add_body(element_ball("C", ORIGIN, scale=0.35, label=False))
    small_mix = mix.copy().scale(0.62).move_to([3.6, 2.6, 0])
    scene.play(FadeOut(added), FadeOut(hybrid), Transform(mix, small_mix), run_time=0.9)
    dial = Dial(orbital, [3.6, -0.6, 0], length=5.2)
    show(scene, stage, 0.9, FadeIn(dial))
    scene.play(orbital.mix_to(np.radians(28)), run_time=3.0, rate_func=smooth)

    # --- 9. All p: the familiar pair of lobes ---------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(orbital.mix_to(np.pi / 2), run_time=2.6, rate_func=smooth)
    scene.play(orbital.mix_to(om.SP_ALPHA["sp"]), run_time=2.4, rate_func=smooth)
    scene.play(Indicate(dial.sp_tick, color=cfg.WHITE, scale_factor=1.2), run_time=1.0)

    # --- 10. A model, not melting orbitals ---------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    model_note = caption("A model: the same electrons, described differently", cfg.WHITE)
    scene.play(FadeIn(model_note), run_time=1.0)
    scene.play(*stage.turn(yaw=0.7, pitch=0.5), run_time=3.0, rate_func=there_and_back)

    # --- 11. One s + one p -> two sp hybrids ----------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    dial.clear_updaters()
    hide(scene, stage, 0.6, FadeOut(dial), FadeOut(model_note), FadeOut(mix))
    stage = Stage([0, -0.3, 0], zoom=1.0, yaw=0.25, pitch=0.25, sway=0.12)
    s_part = Orbital(stage, ORIGIN, RIGHT, 0.0, units=0.78)
    s_twin = Orbital(stage, ORIGIN, LEFT, 0.0, units=0.78)
    p_part = Orbital(stage, ORIGIN, RIGHT, np.pi / 2, units=0.78)
    stage.add_body(element_ball("C", ORIGIN, scale=0.35, label=False))
    recipe = VGroup(eq(r"s+p", cfg.FONT["section"], cfg.BLUE), eq(r"s-p", cfg.FONT["section"], cfg.BLUE))
    recipe[0].move_to([4.6, 2.5, 0])
    recipe[1].move_to([-4.6, 2.5, 0])
    show(scene, stage, 0.8)
    scene.play(FadeIn(recipe), run_time=0.8)
    scene.play(s_part.mix_to(om.SP_ALPHA["sp"]), s_twin.mix_to(om.SP_ALPHA["sp"]), *p_part.fade(0.0),
               run_time=2.8, rate_func=smooth)

    # --- 12. Opposite directions: 180 degrees ---------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    straight = AngleArc(ORIGIN, RIGHT, LEFT, 1.0, label=degrees_label(180, cfg.FONT["body"]), label_gap=0.55)
    straight.presence = 0.0
    stage.add_overlay(straight)
    two_sp = shape_name("two sp hybrids", cfg.BLUE, cfg.FONT["body"]).move_to([0, -3.0, 0])
    scene.play(stage.fade(straight, 1.0), FadeIn(two_sp), run_time=1.2)
    co2_like = caption("The same line as carbon dioxide", cfg.GOLD)
    scene.play(FadeIn(co2_like), *stage.turn(yaw=0.7), run_time=2.0)

    # --- 13. The unused p orbitals stay behind ---------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    leftovers = [p_orbital(stage, ORIGIN, axis, units=0.6, opacity=0.8) for axis in om.leftover_p("sp")]
    for orb in leftovers:
        orb.set_presence(0.0)
    unused = caption("Two unused p orbitals: ready for π bonds", cfg.PURPLE)
    scene.play(stage.fade(straight, 0.0), *[a for orb in leftovers for a in orb.fade(1.0)], *s_part.fade(0.45),
               *s_twin.fade(0.45), fade_through(co2_like, unused), *stage.turn(yaw=0.35, pitch=0.5), run_time=1.6)
    scene.remove(co2_like)
    # Bounded turns only: a free spin would eventually show the sp axis end-on.
    stage.sway = 0.25
    scene.play(*stage.turn(yaw=0.7), run_time=1.4, rate_func=smooth)
    scene.play(*stage.turn(pitch=0.75), run_time=2.0, rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["13"])
