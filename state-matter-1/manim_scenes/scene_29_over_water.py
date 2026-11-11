"""Scene 29 — gas collected over water. Bubbles from a generating flask rise
into an upturned jar in a water trough; the gas pushes the water level down.
Water molecules (cyan) evaporate into the collected hydrogen (gold), adding
their own partial pressure. Stacked bars: P_total = P_dry + P_water, so
P_dry = P_total - P_water. At 298 K the aqueous tension is 0.0317 bar
(NCERT Table 5.2): 1.000 bar total gives 0.968 bar of dry gas.
"""

from manim_scenes.common import *

W = pm.OVER_WATER
WATER = "#2E7FBF"


class Scene29OverWater(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "29", "Gas over water")
    trough = Rectangle(width=6.4, height=2.0, stroke_color=cfg.GLASS, stroke_width=4, fill_color=WATER, fill_opacity=0.45).move_to([-2.6, -2.6, 0])
    jar_x, jar_w, jar_top, jar_bottom = -2.0, 1.9, 2.4, -2.9
    level = Knob(jar_top)                                    # water surface inside the jar
    jar = VGroup(Line([jar_x - jar_w / 2, jar_bottom, 0], [jar_x - jar_w / 2, jar_top, 0]),
                 Line([jar_x - jar_w / 2, jar_top, 0], [jar_x + jar_w / 2, jar_top, 0]),
                 Line([jar_x + jar_w / 2, jar_top, 0], [jar_x + jar_w / 2, jar_bottom, 0])).set_stroke(cfg.GLASS, 5, 0.95)
    inside = Rectangle(width=jar_w - 0.1, height=0.1, stroke_width=0, fill_color=WATER, fill_opacity=0.55)
    inside.add_updater(lambda m: m.stretch_to_fit_height(max(level.value - jar_bottom, 0.02)).move_to(
        [jar_x, (level.value + jar_bottom) / 2, 0]))
    tube = VMobject(stroke_color=cfg.STEEL, stroke_width=8).set_points_as_corners(
        [[-6.4, 0.2, 0], [-6.4, -2.2, 0], [-2.4, -2.2, 0], [-2.4, -1.5, 0]])
    flask = VGroup(Circle(radius=0.75, stroke_color=cfg.GLASS, stroke_width=4, fill_color=cfg.PANEL, fill_opacity=0.8).move_to([-6.4, 1.2, 0]),
                   Rectangle(width=0.4, height=0.6, stroke_color=cfg.GLASS, stroke_width=4).move_to([-6.4, 0.25, 0]))
    scene.play(FadeIn(trough), Create(jar), FadeIn(flask), Create(tube), run_time=1.4)
    scene.add(inside)
    inside.update()
    tag = txt("upturned jar, full of water", cfg.FONT["small"], cfg.MUTED).move_to([3.0, 2.8, 0])
    scene.play(FadeIn(tag), run_time=0.8)

    # --- 2. Bubbles rise into the jar; the gas pushes the water down ---------------------------------------------------------
    beat(scene, t, 1)
    rng = np.random.default_rng(cfg.SEED + 29)
    gas = VGroup(*[Dot([jar_x + rng.uniform(-0.75, 0.75), jar_top - 0.15 - rng.uniform(0, 2.6), 0], radius=0.06, color=cfg.GOLD)
                   for _ in range(26)])
    for d in gas:
        d.set_opacity(0)
    bubbles = VGroup(*[Circle(radius=0.09, stroke_color=cfg.WHITE, stroke_width=2).move_to([-2.4 + rng.uniform(-0.1, 0.1), -1.5, 0])
                       for _ in range(8)])
    name = txt("hydrogen collects", cfg.FONT["label"], cfg.GOLD).move_to([3.0, 2.8, 0])
    scene.play(fade_through(tag, name), run_time=0.8)
    scene.play(LaggedStart(*[b.animate.shift(UP * 3.2).set_opacity(0) for b in bubbles], lag_ratio=0.15),
               level.to(inside, -1.6, run_time=4.0), LaggedStart(*[d.animate.set_opacity(1) for d in gas], lag_ratio=0.05),
               run_time=4.0)

    # --- 3. Water evaporates into it: its own partial pressure --------------------------------------------------------------------
    beat(scene, t, 2)
    vapour = VGroup(*[Dot([jar_x + rng.uniform(-0.75, 0.75), -1.5, 0], radius=0.055, color=cfg.CYAN) for _ in range(5)])
    targets = [np.array([jar_x + rng.uniform(-0.75, 0.75), rng.uniform(0.2, 2.1), 0]) for _ in range(5)]
    impure = txt("plus water vapour", cfg.FONT["label"], cfg.CYAN).move_to([3.0, 2.0, 0])
    equal_levels = DashedLine([-3.2, -1.6, 0], [0.6, -1.6, 0],
                              stroke_color=cfg.WHITE, stroke_width=2, dash_length=0.12)
    scene.play(FadeIn(vapour), FadeIn(impure), Create(equal_levels), run_time=0.8)
    scene.play(*[d.animate.move_to(p) for d, p in zip(vapour, targets)], run_time=3.0)

    # --- 4. P_total = P_dry + P_water --------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    base = np.array([6.3, -2.9, 0])
    unit = 4.2
    dry = Rectangle(width=1.1, height=W.P_dry * unit, stroke_width=2, stroke_color=cfg.GOLD, fill_color=cfg.GOLD, fill_opacity=0.85)
    dry.move_to(base + UP * W.P_dry * unit / 2)
    wet = Rectangle(width=1.1, height=max(W.aqueous_tension * unit, 0.06), stroke_width=2, stroke_color=cfg.CYAN, fill_color=cfg.CYAN,
                    fill_opacity=0.95).next_to(dry, UP, buff=0)
    law = eq(r"P_{\text{dry}} = P_{\text{total}} - P_{\text{water}}", cfg.FONT["body"], cfg.WHITE).move_to([2.4, 0.9, 0])
    fit_width(law, 4.8)
    scene.play(FadeOut(VGroup(name, impure)), GrowFromEdge(dry, DOWN), run_time=1.2)
    scene.play(GrowFromEdge(wet, DOWN), run_time=0.8)
    scene.play(Write(law), run_time=1.6)

    # --- 5. At 25 C: 0.0317 bar of vapour; 0.968 bar of dry gas -------------------------------------------------------------------------
    beat(scene, t, 4)
    numbers = VGroup(eq(rf"P_{{\text{{water}}}}(298\,\mathrm{{K}}) = {fx(W.aqueous_tension, 4)}\ \mathrm{{bar}}", cfg.FONT["small"], cfg.CYAN),
                     eq(rf"P_{{\text{{dry}}}} = {fx(W.P_total, 3)} - {fx(W.aqueous_tension, 4)} = {fx(W.P_dry, 3)}\ \mathrm{{bar}}",
                        cfg.FONT["small"], cfg.GOLD)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([2.4, -0.6, 0])
    fit_width(numbers, 4.8)
    scene.play(FadeIn(numbers[0], shift=UP * 0.1), Indicate(wet, color=cfg.WHITE), run_time=1.4)
    scene.wait(2.0)
    scene.play(FadeIn(numbers[1], shift=UP * 0.1), Indicate(dry, color=cfg.WHITE), run_time=1.4)

    # --- 6. Aqueous tension, rising with temperature --------------------------------------------------------------------------------------
    beat(scene, t, 5)
    tension = result_label("aqueous tension: rises with T", cfg.CYAN, cfg.FONT["body"]).move_to([2.6, 2.8, 0])
    fit_width(tension, 8.0)
    scene.play(FadeIn(tension, scale=0.95), run_time=1.0)
    finish(scene, t, fill=lambda s: [*[d.animate.shift(UP * 0.12 * ((k % 3) - 1)) for k, d in enumerate(vapour)]])
