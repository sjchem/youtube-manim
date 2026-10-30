"""Scene 09 — why chemists keep both measures: molarity at the bench,
molality when temperature changes. Then a plot of molarity against molality
for glucose solutions: nearly equal when dilute, apart when strong.

The curve uses ``physics_models.molarity_for_molality`` — a simple model
with a constant apparent molar volume calibrated on the reference solution,
labelled as such on screen.
"""

from manim_scenes.common import *


class Scene09BothMeasures(Scene):
    def construct(self) -> None:
        play_scene(self)


def pipette(color: str = cfg.VOLUME) -> VGroup:
    tube = RoundedRectangle(width=0.16, height=3.2, corner_radius=0.08, stroke_color=cfg.GLASS, stroke_width=3,
                            fill_opacity=0)
    bulb = Ellipse(width=0.62, height=1.0, stroke_color=cfg.GLASS, stroke_width=3, fill_color=color,
                   fill_opacity=0.35).move_to(tube.get_center() + DOWN * 0.3)
    liquid = Rectangle(width=0.1, height=1.9, stroke_width=0, fill_color=color, fill_opacity=0.6)
    liquid.move_to(tube.get_bottom() + UP * 0.95)
    mark = Line(LEFT * 0.16, RIGHT * 0.16, stroke_color=cfg.WHITE, stroke_width=3).move_to(tube.get_center() + UP * 1.05)
    return VGroup(liquid, bulb, tube, mark)


def side(title: str, color: str, x: float) -> VGroup:
    box = RoundedRectangle(width=6.8, height=5.6, corner_radius=0.3, stroke_color=color, stroke_width=3,
                           fill_color=cfg.PANEL, fill_opacity=0.55).move_to([x, -0.35, 0])
    name = txt(title, cfg.FONT["section"], color).move_to([x, 1.9, 0])
    return VGroup(box, name)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "09", "Molarity or molality?")
    left = side("molarity", cfg.VOLUME, -3.7)
    right = side("molality", cfg.SOLVENT_MASS, 3.7)
    scene.play(FadeIn(left, shift=RIGHT * 0.2), FadeIn(right, shift=LEFT * 0.2), run_time=1.2)

    # --- 2. The bench: measure a volume, know the moles ----------------------------------------------------
    beat(scene, t, 1)
    tool = pipette().move_to([-5.6, -0.6, 0])
    reads = VGroup(txt("measure a volume", cfg.FONT["small"], cfg.WHITE),
                   txt("→ know the moles", cfg.FONT["small"], cfg.AMOUNT)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    reads.move_to([-2.9, 0.75, 0])
    scene.play(FadeOut(head), FadeIn(tool, shift=DOWN * 0.3), run_time=0.9)
    drop = bead(tool.get_bottom() + DOWN * 0.1, cfg.VOLUME, 0.08)
    scene.play(FadeIn(reads), drop.animate.shift(DOWN * 0.7).set_opacity(0), run_time=1.4)

    # --- 3. Titrations, dilutions, yields --------------------------------------------------------------------------
    beat(scene, t, 2)
    bench = VGroup(*[chip(w, cfg.VOLUME) for w in ("titrations", "dilutions", "reaction yields")]).arrange(DOWN, buff=0.22)
    bench.move_to([-2.9, -1.35, 0])
    scene.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in bench], lag_ratio=0.35), run_time=1.6)

    # --- 4. When temperature changes ---------------------------------------------------------------------------------
    beat(scene, t, 3)
    thermo = Thermometer([5.6, -0.7, 0], low=-10, high=110, height=3.4)
    scene.play(FadeIn(thermo), run_time=0.7)
    scene.play(thermo.celsius.to(thermo, 95.0), run_time=1.6)
    scene.play(thermo.celsius.to(thermo, -5.0), run_time=1.8)
    safe = txt("temperature changes", cfg.FONT["small"], cfg.WHITE).move_to([2.9, 0.75, 0])
    scene.play(FadeIn(safe), run_time=0.6)

    # --- 5. Freezing, boiling, careful physical chemistry ----------------------------------------------------------------
    beat(scene, t, 4)
    phys = VGroup(*[chip(w, cfg.SOLVENT_MASS) for w in ("freezing points", "boiling points", "physical chemistry")])
    phys.arrange(DOWN, buff=0.22).move_to([2.9, -1.35, 0])
    scene.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in phys], lag_ratio=0.35), thermo.celsius.to(thermo, 20.0),
               run_time=1.6)

    # --- 6. A plot: close when dilute ---------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(VGroup(left, right, tool, reads, bench, thermo, safe, phys)), run_time=0.8)
    axes = Axes(x_range=[0, 3, 1], y_range=[0, 3, 1], x_length=6.2, y_length=5.2, tips=False,
                axis_config={"color": cfg.MUTED, "stroke_width": 3, "include_ticks": True}).move_to([-2.3, -0.45, 0])
    x_name = txt("molality, m (mol/kg)", cfg.FONT["small"], cfg.SOLVENT_MASS).next_to(axes.x_axis, DOWN, buff=0.25)
    ticks = VGroup(*[txt(str(v), cfg.FONT["tiny"], cfg.MUTED).next_to(axes.c2p(v, 0), DOWN, buff=0.12) for v in (1, 2, 3)],
                   *[txt(str(v), cfg.FONT["tiny"], cfg.MUTED).next_to(axes.c2p(0, v), LEFT, buff=0.15) for v in (1, 2, 3)])
    x_name.next_to(ticks[:3], DOWN, buff=0.28)
    y_name = txt("molarity, c (mol/L)", cfg.FONT["small"], cfg.VOLUME).rotate(PI / 2)
    y_name.next_to(ticks[3:], LEFT, buff=0.32).set_y(axes.y_axis.get_center()[1])
    # This is a reference for equal numbers in the stated units, not a second
    # physical quantity plotted on the molarity axis.
    same_line = DashedVMobject(axes.plot(lambda x: x, x_range=[0, 3], color=cfg.SOLVENT_MASS,
                                        stroke_width=6), num_dashes=24, dashed_ratio=0.55)
    curve = axes.plot(lambda x: float(pm.molarity_for_molality(x)), x_range=[0, 3], color=cfg.VOLUME, stroke_width=7)
    lab_m = VGroup(txt("equal numerical values", cfg.FONT["tiny"], cfg.SOLVENT_MASS),
                   txt("(reference)", cfg.FONT["tiny"], cfg.MUTED)).arrange(DOWN, buff=0.06)
    fit_width(lab_m, 3.8)
    lab_m.next_to(axes.c2p(2.3, 2.3), UL, buff=0.2)
    lab_c = txt("molarity", cfg.FONT["small"], cfg.VOLUME).next_to(axes.c2p(3, float(pm.molarity_for_molality(3.0))),
                                                                   RIGHT, buff=0.25)
    model = txt("glucose in water · simple model", cfg.FONT["tiny"], cfg.MUTED).move_to([4.6, -3.35, 0])
    scene.play(Create(axes), FadeIn(ticks), FadeIn(x_name), FadeIn(y_name), FadeIn(model), run_time=1.2)
    scene.play(Create(same_line), FadeIn(lab_m), run_time=1.2)
    scene.play(Create(curve), FadeIn(lab_c), run_time=1.4)
    us = glow_dot(axes.c2p(REF.molality, REF.molarity), cfg.GOLD, 0.08)
    us_label = txt("our glucose", cfg.FONT["tiny"], cfg.GOLD).next_to(us, DR, buff=0.1)
    scene.play(FadeIn(us, scale=0.5), FadeIn(us_label), run_time=0.8)

    # --- 7. Mostly water: nearly equal ---------------------------------------------------------------------------------------
    beat(scene, t, 6)
    dilute = glow_frame(Rectangle(width=1.35, height=1.25).move_to(axes.c2p(0.3, 0.3)), cfg.CYAN, buff=0.05)
    nearly = VGroup(txt("dilute:", cfg.FONT["label"], cfg.CYAN), txt("nearly equal", cfg.FONT["label"], cfg.CYAN))
    nearly.arrange(DOWN, buff=0.1).move_to([5.0, 1.4, 0])
    litre = eq(r"1\ \mathrm{L\ water} \approx 1\ \mathrm{kg}", cfg.FONT["label"], cfg.WHITE).move_to([5.0, 0.15, 0])
    scene.play(Create(dilute), FadeIn(nearly), run_time=1.2)
    scene.play(Write(litre), run_time=1.2)

    # --- 8. Stronger: they drift apart ------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    x_track = Knob(0.3)
    rider_m = always_redraw(lambda: glow_dot(axes.c2p(x_track.value, x_track.value), cfg.SOLVENT_MASS, 0.07))
    rider_c = always_redraw(lambda: glow_dot(axes.c2p(x_track.value, float(pm.molarity_for_molality(x_track.value))),
                                             cfg.VOLUME, 0.07))
    gap = always_redraw(lambda: Line(axes.c2p(x_track.value, float(pm.molarity_for_molality(x_track.value))),
                                     axes.c2p(x_track.value, x_track.value), stroke_color=cfg.WARNING, stroke_width=5))
    scene.add(gap, rider_m, rider_c)
    scene.play(FadeOut(dilute), x_track.to(gap, 2.9), run_time=4.5)
    apart = txt("drift apart", cfg.FONT["label"], cfg.WARNING).move_to([5.0, -1.2, 0])
    reason = txt("solute adds volume and mass, not solvent", cfg.FONT["tiny"], cfg.MUTED).move_to([5.0, -2.0, 0])
    fit_width(reason, 5.4)
    scene.play(FadeIn(apart), FadeIn(reason), run_time=1.0)

    # --- 9. Close is not the same --------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    for mob in (gap, rider_m, rider_c):
        mob.clear_updaters()
    scene.play(FadeOut(VGroup(axes, ticks, x_name, y_name, same_line, curve, lab_m, lab_c, model, us, us_label, nearly, litre,
                              apart, reason, gap, rider_m, rider_c)), run_time=0.8)
    not_same = eq([r"1\ \mathrm{M}", r"\neq", r"1\ \mathrm{m}"], 110)
    not_same[0].set_color(cfg.VOLUME)
    not_same[1].set_color(cfg.WARNING)
    not_same[2].set_color(cfg.SOLVENT_MASS)
    not_same.move_to([0, 0.5, 0])
    bridge = chip("later: density connects them", cfg.ROSE).next_to(not_same, DOWN, buff=0.7)
    scene.play(Write(not_same), run_time=1.4)
    scene.play(FadeIn(bridge, shift=UP * 0.15), run_time=0.8)
    scene.play(not_same.animate.scale(1.06), run_time=6.0)
    scene.play(Indicate(bridge, color=cfg.WHITE, scale_factor=1.05), run_time=1.5)
    scene.play(Circumscribe(not_same, color=cfg.GOLD, buff=0.15), run_time=3.0)
    scene.play(not_same.animate.scale(1 / 1.06), run_time=6.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["09"])
