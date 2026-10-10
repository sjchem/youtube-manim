"""The ionization mountain range (3D).

The first ionization enthalpies of Z = 1..86 (NIST) are drawn as a line,
then as bars, and the bars swing up out of the screen into a landscape while
the camera tilts down to meet them. Every bar height is the measured value on
one scale; bar colour is the film's heat scale. The camera only rotates; the
content is moved to the origin instead of moving frame_center.
"""

from manim_scenes.common import *

AXES_AT = np.array([0.2, -0.45, 0])
TOP = 2500
DEPTH = 2.5         # the landscape stands on a floor this far below the origin
NOBLES = (2, 10, 18, 36, 54, 86)
ALKALIS = (3, 11, 19, 37, 55)


class Scene10IonizationLandscape(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "10", 'First ionization · Z = 1–86')
    series = ed.ionization_series()
    peak = max(value for _, value in series)

    axes = trend_axes(13.4, 5.3, TOP, 500, x_count=len(series)).move_to(AXES_AT)
    unit = txt("kJ/mol", cfg.FONT["tiny"], cfg.MUTED).next_to(axes.y_tick_labels[-1], UP, buff=0.25)
    z_axis = txt("atomic number  →", cfg.FONT["tiny"], cfg.MUTED).next_to(axes.c2p(len(series) / 2, 0), DOWN, buff=0.25)
    points = [axes.c2p(z, value) for z, value in series]
    line = glow_polyline(points, cfg.CYAN, 3.5)
    scene.play(Create(axes), FadeIn(unit), FadeIn(z_axis), run_time=1.2)
    # Let the graph draw continuously while the opening title clears at 4 s.
    scene.play(Create(line, rate_func=linear),
               FadeOut(head, rate_func=lambda a: smooth(np.clip((a * 4.6 - 1.6) / 0.6, 0, 1))),
               run_time=4.6)
    scene.camera.remove_fixed_in_frame_mobjects(head)
    head = None

    # --- 1. A repeating pattern ------------------------------------------------------------------
    beat(scene, t, 1)
    periods = [(1, 2), (3, 10), (11, 18), (19, 36), (37, 54), (55, 86)]
    bands = VGroup(*[Rectangle(width=axes.c2p(b + 0.5, 0)[0] - axes.c2p(a - 0.5, 0)[0], height=5.3, stroke_width=0,
                               fill_color=cfg.CYAN if i % 2 else cfg.BLUE, fill_opacity=0.06)
                     .move_to([(axes.c2p(a - 0.5, 0)[0] + axes.c2p(b + 0.5, 0)[0]) / 2, axes.c2p(0, TOP / 2)[1], 0])
                     for i, (a, b) in enumerate(periods)])
    scene.play(LaggedStart(*[FadeIn(band) for band in bands], lag_ratio=0.2), run_time=1.6)

    # --- 2. Peaks: the noble gases -------------------------------------------------------------------
    beat(scene, t, 2)
    peak_tags = VGroup(*[txt(pm.symbol_of(z), cfg.FONT["small"], cfg.GOLD).next_to(points[z - 1], UP, buff=0.14)
                         for z in NOBLES])
    peak_dots = VGroup(*[glow_dot(points[z - 1], 0.09, cfg.GOLD) for z in NOBLES])
    scene.play(LaggedStart(*[AnimationGroup(FadeIn(d, scale=0.4), FadeIn(tag, shift=DOWN * 0.1))
                             for d, tag in zip(peak_dots, peak_tags)], lag_ratio=0.25), run_time=2.4)
    closed = chip('Closed shells: tightly held', cfg.GOLD, cfg.FONT["small"]).move_to([3.4, 2.9, 0])
    scene.play(FadeIn(closed, shift=DOWN * 0.15), run_time=0.7)

    # --- 3. Cliffs: the alkali metals ----------------------------------------------------------------------
    beat(scene, t, 3)
    low_tags = VGroup(*[txt(pm.symbol_of(z), cfg.FONT["small"], cfg.CYAN).next_to(points[z - 1], DOWN, buff=0.14)
                        for z in ALKALIS])
    low_dots = VGroup(*[glow_dot(points[z - 1], 0.09, cfg.CYAN) for z in ALKALIS])
    scene.play(LaggedStart(*[AnimationGroup(FadeIn(d, scale=0.4), FadeIn(tag, shift=UP * 0.1))
                             for d, tag in zip(low_dots, low_tags)], lag_ratio=0.25), run_time=2.2)
    fresh = chip('A fresh outer shell', cfg.CYAN, cfg.FONT["small"]).move_to([3.4, 2.9, 0])
    scene.play(*fade_labels(closed, fresh), run_time=0.7)

    # --- 4. The graph becomes a landscape ------------------------------------------------------------------
    beat(scene, t, 4)
    base_y = axes.c2p(0, 0)[1]
    width = (axes.c2p(2, 0)[0] - axes.c2p(1, 0)[0]) * 0.78
    bars = VGroup()
    for z, value in series:
        height = axes.c2p(0, value)[1] - base_y
        colour = mu.scale_color(value / peak, cfg.HEAT_STOPS)
        bar = Prism(dimensions=[width, height, 0.55], fill_color=colour, fill_opacity=0.95, stroke_width=0.4,
                    stroke_color=interpolate_color(ManimColor(colour), ManimColor(cfg.WHITE), 0.4))
        bar.move_to([axes.c2p(z, 0)[0], base_y + height / 2, 0])
        bars.add(bar)
    scene.play(FadeIn(bars), line.animate.set_opacity(0.0), FadeOut(VGroup(peak_dots, low_dots)), run_time=1.4)
    scene.play(FadeOut(VGroup(axes, unit, z_axis, bands, peak_tags, low_tags, line, fresh)),
               bars.animate.shift(UP * (-base_y) + LEFT * AXES_AT[0] + IN * DEPTH), run_time=1.0)
    landscape = caption('Same data · 3D view', cfg.CYAN, cfg.FONT["small"], y=-3.9)
    hud(scene, landscape)
    move_camera(scene, phi=72 * DEGREES, theta=-72 * DEGREES, zoom=0.92, run_time=3.0,
                added_anims=[Rotate(bars, PI / 2, axis=RIGHT, about_point=IN * DEPTH)])
    scene.play(FadeIn(landscape), run_time=0.6)

    # --- 5. Each climb is one period ----------------------------------------------------------------------
    beat(scene, t, 5)
    climb = caption("each climb = one period", cfg.GOLD, cfg.FONT["small"], y=-3.9)
    hud(scene, climb)
    scene.play(*fade_labels(landscape, climb), run_time=0.6)
    for a, b in ((3, 10), (11, 18)):
        scene.play(LaggedStart(*[Indicate(bars[z - 1], color=cfg.WHITE, scale_factor=1.0) for z in range(a, b + 1)],
                               lag_ratio=0.15), run_time=1.5)

    # --- 6. The peaks fall going down -------------------------------------------------------------------------
    beat(scene, t, 6)

    ridge = VMobject(stroke_color=cfg.GOLD, stroke_width=6).set_points_as_corners([bars[z - 1].get_zenith() for z in NOBLES])
    valley = VMobject(stroke_color=cfg.CYAN, stroke_width=6).set_points_as_corners([bars[z - 1].get_zenith() for z in ALKALIS])
    lower = caption('Down a group: lower peaks', cfg.GOLD, cfg.FONT["small"], y=-3.9)
    hud(scene, lower)
    scene.play(*fade_labels(climb, lower), Create(ridge), run_time=1.6)
    scene.play(Create(valley), run_time=1.2)
    move_camera(scene, phi=66 * DEGREES, theta=-58 * DEGREES, zoom=0.92, run_time=3.0)

    # --- 7. The rule: the mirror image of size ----------------------------------------------------------------
    beat(scene, t, 7)
    rule = VGroup(chip('Across: generally rises', cfg.GOLD, cfg.FONT["small"]),
                  chip('Down: generally falls', cfg.CYAN, cfg.FONT["small"])).arrange(RIGHT, buff=0.5).move_to([0, 2.95, 0])
    mirror = caption('Opposite broad trend to size', cfg.WHITE, cfg.FONT["small"], y=-3.9)
    hud(scene, rule, mirror)
    scene.play(FadeOut(lower), FadeIn(rule, shift=DOWN * 0.15), run_time=0.8)
    scene.play(FadeIn(mirror), run_time=0.7)
    scene.wait(1.0)

    # --- 8. Back to flat: period 2 is not smooth -------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(VGroup(ridge, valley)), FadeOut(VGroup(rule, mirror)), run_time=0.6)
    move_camera(scene, phi=0, theta=-PI / 2, zoom=1.0, run_time=2.4,
                added_anims=[Rotate(bars, -PI / 2, axis=RIGHT, about_point=IN * DEPTH)])
    others = VGroup(*[bars[z - 1] for z in range(1, 87) if not 3 <= z <= 10])
    scene.play(FadeOut(others), run_time=0.6)
    close = []
    for i, z in enumerate(range(3, 11)):
        height = ed.ionization_kj(z) / TOP * 4.6
        bar = bars[z - 1]
        target = Prism(dimensions=[0.82, height, 0.5], fill_color=bar.get_fill_color(), fill_opacity=0.95,
                       stroke_width=0.6, stroke_color=cfg.WHITE).move_to([-4.2 + 1.2 * i, -2.75 + height / 2, 0])
        close.append(Transform(bar, target))
    symbols = VGroup(*[txt(pm.symbol_of(z), cfg.FONT["small"], block_color(z)).move_to([-4.2 + 1.2 * i, -3.25, 0])
                       for i, z in enumerate(range(3, 11))])
    hud(scene, symbols)
    scene.play(*close, FadeIn(symbols), run_time=1.4)
    dips = VGroup()
    for z in (5, 8):  # B after Be, O after N
        before, after = bars[z - 2].get_top(), bars[z - 1].get_top()
        dips.add(CurvedArrow(before + UP * 0.35, after + UP * 0.22, angle=-PI / 2.4, color=cfg.RED, stroke_width=8,
                             tip_length=0.28))
    wrong = caption('Two revealing dips', cfg.RED, cfg.FONT["small"], y=2.95)
    hud(scene, wrong)
    scene.play(LaggedStart(*[Create(d) for d in dips], lag_ratio=0.5), FadeIn(wrong), run_time=1.2)
    pairs = VGroup(*[txt(f"{pm.symbol_of(a)} {ed.ionization_kj(a)}  →  {pm.symbol_of(b)} {ed.ionization_kj(b)}",
                         cfg.FONT["small"], cfg.WHITE) for a, b in ((4, 5), (7, 8))]).arrange(DOWN, buff=0.25)
    pairs.move_to([-3.55, 1.45, 0])
    hud(scene, pairs)
    scene.play(LaggedStart(*[FadeIn(v, shift=UP * 0.1) for v in pairs], lag_ratio=0.3),
               *[bars[z - 1].animate.set_fill(cfg.RED) for z in (5, 8)], run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["10"])
