"""Scene 01 — the hook. A balloon inflates beside a bicycle tyre; air looks
like nothing, yet one square metre of it carries about ten tonnes (computed
from 1 bar). We shrink into the balloon: a 3D glass box of molecules flying
in straight lines, one followed in gold with its zigzag trail, every wall hit
throwing an orange spark. The gas laws float up around the box; the question
lands, and the title closes the scene.
"""

from manim_scenes.common import *

A = pm.AIR


class Scene01Hook(Scene):
    def construct(self) -> None:
        play_scene(self)


def balloon(at, radius: float = 1.25, color: str = cfg.ROSE) -> VGroup:
    """A glossy balloon: shaded body, a highlight, a knot and a curling string."""
    body = VGroup(*[Ellipse(width=2 * radius * f, height=2.3 * radius * f, stroke_width=0,
                            fill_color=mu.mix(mu.shade(color, 0.55), color, 1 - f), fill_opacity=1)
                    .shift(UL * radius * 0.28 * (1 - f)) for f in np.linspace(1.0, 0.35, 9)])
    rim = Ellipse(width=2 * radius, height=2.3 * radius, stroke_color=mu.mix(color, cfg.WHITE, 0.3), stroke_width=2.5,
                  fill_opacity=0)
    shine = Ellipse(width=radius * 0.42, height=radius * 0.7, stroke_width=0, fill_color=cfg.WHITE,
                    fill_opacity=0.35).rotate(0.5).move_to(UL * radius * 0.48)
    bottom = DOWN * 1.15 * radius
    knot = Triangle(stroke_width=0, fill_color=mu.shade(color, 0.7), fill_opacity=1).scale(0.13).move_to(bottom + DOWN * 0.06)
    string = VMobject(stroke_color=cfg.MUTED, stroke_width=2.5).set_points_smoothly(
        [bottom + DOWN * 0.12, bottom + DOWN * 0.6 + RIGHT * 0.14, bottom + DOWN * 1.1 + LEFT * 0.12,
         bottom + DOWN * 1.6 + RIGHT * 0.08])
    group = VGroup(string, body, rim, shine, knot).shift(np.asarray(at, dtype=float))
    group.knot = knot
    return group


def tyre(at, radius: float = 1.25) -> VGroup:
    """A bicycle tyre: dark tread ring, spokes and hub."""
    outer = Annulus(inner_radius=radius * 0.8, outer_radius=radius, stroke_width=0, fill_color="#26323C", fill_opacity=1)
    tread = VGroup(*[Line(UP * radius * 0.86, UP * radius * 0.98, stroke_color="#50606D", stroke_width=4)
                     .rotate(k * TAU / 36, about_point=ORIGIN) for k in range(36)])
    rim = Circle(radius=radius * 0.8, stroke_color=cfg.STEEL, stroke_width=4, fill_opacity=0)
    spokes = VGroup(*[Line(ORIGIN, UP * radius * 0.78, stroke_color=cfg.MUTED, stroke_width=1.6, stroke_opacity=0.8)
                      .rotate(k * TAU / 16, about_point=ORIGIN) for k in range(16)])
    hub = Circle(radius=0.12, stroke_width=0, fill_color=cfg.STEEL, fill_opacity=1)
    return VGroup(outer, tread, rim, spokes, hub).move_to(at)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "01")

    # --- 1. A balloon swells; a tyre turns hard ---------------------------------------------------------------
    knot = np.array([-3.2, -1.7, 0.0])
    b = balloon([-3.2, 0.4, 0.0])
    b.scale(0.35, about_point=knot)
    wheel = tyre([3.4, 0.0, 0.0], 1.6)
    scene.play(FadeIn(b, scale=0.9), run_time=0.8)
    scene.play(b.animate.scale(1 / 0.35, about_point=knot), run_time=3.2, rate_func=smooth)
    scene.play(FadeIn(wheel, shift=LEFT * 0.3), run_time=0.9)
    scene.play(Rotate(wheel, -TAU / 3), run_time=3.0, rate_func=smooth)

    # --- 2. Air looks like nothing ---------------------------------------------------------------------------
    beat(scene, t, 1)
    empty = txt("empty space?", cfg.FONT["section"], cfg.MUTED).move_to([0.2, 2.9, 0])
    scene.play(FadeIn(empty, shift=DOWN * 0.15), FadeOut(wheel, shift=RIGHT * 0.3), run_time=1.0)
    scene.play(b[3].animate.set_opacity(0.6), run_time=1.6, rate_func=there_and_back)

    # --- 3. One square metre carries about ten tonnes ------------------------------------------------------
    beat(scene, t, 2)
    square = Polygon([1.4, -2.2, 0], [5.6, -2.2, 0], [6.4, -0.9, 0], [2.2, -0.9, 0], stroke_color=cfg.PRESSURE,
                     stroke_width=4, fill_color=cfg.PRESSURE, fill_opacity=0.18)
    area = txt("1 m²", cfg.FONT["label"], cfg.WHITE).move_to(square)
    pushes = VGroup(*[VecArrow([x, 1.0, 0], [x, -0.75, 0], cfg.IMPULSE, width=0.07, tip_len=0.22, live=False)
                      for x in np.linspace(2.0, 6.0, 7)])
    tonnes = result_label(f"≈ {fx(A.tonnes_per_square_metre, 0)} tonnes", cfg.GOLD, cfg.FONT["section"]).move_to([3.9, 1.9, 0])
    scene.play(FadeOut(empty), Create(square), FadeIn(area), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.4) for p in pushes], lag_ratio=0.12), run_time=1.6)
    scene.play(FadeIn(tonnes, scale=0.9), run_time=0.9)
    scene.play(pushes.animate.shift(DOWN * 0.12), run_time=0.8, rate_func=there_and_back)

    # --- 4. Shrink yourself and step inside -------------------------------------------------------------------
    beat(scene, t, 3)
    box = GasBox((0.0, -0.3, 0.0), count=130, half_x=2.3, half_z=1.6, height=3.9, floor=-1.95, follow=11, trail=3.5,
                 zoom=1.3, yaw=-0.62, pitch=0.3, speed=1.8, radius=0.085)
    box.cloud.follow_alpha = 0.0
    box.cloud.spark = 0.0
    scene.play(FadeOut(VGroup(square, area, pushes, tonnes)), b.animate.move_to([0, 0.4, 0]), run_time=1.0)
    scene.play(b.animate.scale(9.0).set_opacity(0.0), run_time=2.2, rate_func=rate_functions.ease_in_cubic)
    scene.remove(b)
    show(scene, box.stage, 1.6)

    # --- 5. A crowd of molecules in straight lines --------------------------------------------------------------
    beat(scene, t, 4)
    crowd = txt("a crowd of molecules", cfg.FONT["label"], cfg.CYAN).move_to([4.6, 3.5, 0])
    scene.play(FadeIn(crowd, shift=DOWN * 0.1), run_time=0.8)
    scene.play(box.cloud.tween("follow_alpha", 1.0), run_time=1.2)
    scene.play(*box.stage.turn(yaw=-0.2), run_time=6.0, rate_func=smooth)

    # --- 6. Every strike is a tiny push --------------------------------------------------------------------------
    beat(scene, t, 5)
    push = txt("every strike: a tiny push", cfg.FONT["label"], cfg.IMPULSE).move_to([4.3, 3.5, 0])
    scene.play(fade_through(crowd, push), box.cloud.tween("spark", 1.0), run_time=1.2)
    scene.play(box.stage.zoom_to(1.5), run_time=3.0)

    # --- 7. Countless pushes hold up a car ------------------------------------------------------------------------
    beat(scene, t, 6)
    steady = txt("countless pushes → one steady force", cfg.FONT["label"], cfg.GOLD).move_to([0, 3.5, 0])
    fit_width(steady, 12.5)
    scene.play(fade_through(push, steady), box.stage.zoom_to(1.3), run_time=1.4)
    scene.play(*box.stage.turn(yaw=-0.45), run_time=3.5)

    # --- 8. They obey laws they do not know -------------------------------------------------------------------------
    beat(scene, t, 7)
    laws = VGroup(eq(r"PV = nRT", cfg.FONT["section"], cfg.WHITE), eq(r"P_1V_1 = P_2V_2", cfg.FONT["body"], cfg.PRESSURE),
                  eq(r"V \propto T", cfg.FONT["body"], cfg.VOLUME), eq(r"P_{\text{total}} = \sum P_i", cfg.FONT["body"], cfg.AMOUNT))
    spots = ([-5.6, 2.5, 0], [5.6, 1.7, 0], [-5.7, -1.5, 0], [5.5, -2.3, 0])
    for law, spot in zip(laws, spots):
        law.move_to(spot)
    scene.play(FadeOut(steady), LaggedStart(*[FadeIn(law, shift=UP * 0.2) for law in laws], lag_ratio=0.3), run_time=2.4)
    scene.play(*[law.animate.shift(UP * 0.15) for law in laws], run_time=2.0, rate_func=there_and_back)

    # --- 9. How can randomness be predictable? ------------------------------------------------------------------------
    beat(scene, t, 8)
    question = VGroup(txt("random motion", cfg.FONT["section"], cfg.CYAN), txt("→", cfg.FONT["section"], cfg.WHITE),
                      txt("predictable laws?", cfg.FONT["section"], cfg.GOLD)).arrange(RIGHT, buff=0.3)
    fit_width(question, 13.0)
    question.move_to([0, 3.45, 0])
    scene.play(FadeIn(question, shift=DOWN * 0.15), *[law.animate.set_opacity(0.35) for law in laws], run_time=1.2)

    # --- 10. Title ----------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    card = title_card(cfg.PROJECT_TITLE, cfg.VIDEO_SUBTITLE).move_to(UP * 0.35)
    plate = RoundedRectangle(width=14.2, height=4.4, corner_radius=0.3, stroke_width=0, fill_color=cfg.BG,
                             fill_opacity=0.72).move_to(card)
    series = txt(cfg.SERIES_LABEL, cfg.FONT["small"], cfg.MUTED)
    fit_width(series, 12.8)
    series.next_to(card, DOWN, buff=0.55)
    scene.play(FadeOut(question), FadeOut(laws), box.stage.fade(box.stage, 0.45), FadeIn(plate), run_time=1.0)
    scene.play(FadeIn(card, scale=0.94), run_time=1.4)
    rule = Line(LEFT * 4.6, RIGHT * 4.6, stroke_color=cfg.GOLD, stroke_width=4).next_to(card, DOWN, buff=0.2)
    scene.play(Create(rule), FadeIn(series, shift=UP * 0.15), card.glow.animate.set_stroke(opacity=0.3), run_time=1.4)
    finish(scene, t, box.stage)
