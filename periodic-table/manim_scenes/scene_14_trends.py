"""Why properties change across the table — a tease, drawn to scale.

Atoms are shaded 3D spheres whose radii are single-bond covalent radii
(Cordero et al., 2008), all on one scale: period 2 across the top row, group 1
along the bottom row. Every sphere starts at lithium's size and then takes its
real size, so the trend is seen happening rather than asserted.
"""

from manim_scenes.common import *

ROW = ("Li", "Be", "B", "C", "N", "O", "F")
COLUMN = ("Li", "Na", "K", "Rb", "Cs")
SCALE = 0.0062  # display units per picometre, shared by both rows
TOP_Y = 1.75
BOTTOM_Y = -1.95
GAP = 0.3


class Scene14Trends(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _radius(symbol: str) -> float:
    return pm.COVALENT_RADII_PM[symbol] * SCALE


def _ball(symbol: str, radius: float) -> VGroup:
    z = pm.z_of(symbol)
    sphere = Sphere(radius=radius, resolution=(14, 28))
    sphere.set_fill(block_color(z), opacity=1).set_stroke(width=0)
    label = txt(symbol, cfg.FONT["small"], cfg.BG)
    ball = VGroup(sphere, label)
    ball.sphere, ball.label = sphere, label
    return ball


def _resize(ball: VGroup, radius: float) -> list[Animation]:
    return [ball.sphere.animate.scale_to_fit_width(2 * radius)]


def _row_points(radii: list[float], y: float) -> list[np.ndarray]:
    """Centres for touching-with-a-gap spheres, the whole row centred on x = 0."""
    width = sum(2 * r for r in radii) + GAP * (len(radii) - 1)
    x = -width / 2
    points = []
    for r in radii:
        points.append(np.array([x + r, y, 0]))
        x += 2 * r + GAP
    return points


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "14", "Across → smaller")
    li_r = _radius("Li")
    top_points = _row_points([li_r] * len(ROW), TOP_Y)
    bottom_points = _row_points([_radius(s) for s in COLUMN], BOTTOM_Y)

    row = [_ball(sym, li_r).move_to(p) for sym, p in zip(ROW, top_points)]
    scene.play(FadeIn(row[0], scale=0.5), run_time=1.2)
    to_scale = txt("Relative covalent radii · same scale", cfg.FONT["tiny"], cfg.MUTED).move_to(DOWN * 4.1)
    hud(scene, to_scale)
    scene.play(FadeIn(to_scale), run_time=0.6)

    # --- Across period 2 -----------------------------------------------------------
    beat(scene, t, 1)
    scene.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.3) for b in row[1:]], lag_ratio=0.15), run_time=2.0)

    beat(scene, t, 2)
    charge_y = TOP_Y - li_r - 0.3
    charges = VGroup(*[txt(f"+{pm.z_of(sym)}", cfg.FONT["small"], cfg.PROTON_COLOR).move_to([b.get_x(), charge_y, 0])
                       for sym, b in zip(ROW, row)])
    steps = VGroup(chip("+1 proton", cfg.PROTON_COLOR, cfg.FONT["small"]),
                   chip("+1 electron · same shell", cfg.CYAN, cfg.FONT["small"])).arrange(RIGHT, buff=0.5)
    steps.move_to(DOWN * 0.55)
    scene.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in charges], lag_ratio=0.12), run_time=1.6)
    scene.play(FadeIn(steps, shift=UP * 0.2), run_time=0.8)

    beat(scene, t, 3)
    pulls = VGroup()
    for index, b in enumerate(row):
        width = 2.5 + 1.0 * index
        for angle in (PI / 4, 3 * PI / 4, 5 * PI / 4, 7 * PI / 4):
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            pulls.add(Arrow(b.get_center() + direction * (li_r + 0.12), b.get_center() + direction * (li_r - 0.32),
                            buff=0, stroke_width=width, color=cfg.GOLD, max_tip_length_to_length_ratio=0.5))
    stronger = txt("stronger pull  →", cfg.FONT["label"], cfg.GOLD).move_to(DOWN * 1.45)
    scene.play(LaggedStart(*[GrowArrow(a) for a in pulls], lag_ratio=0.01), FadeIn(stronger), run_time=2.0)

    beat(scene, t, 4)
    scene.play(FadeOut(pulls), run_time=0.4)
    scene.play(LaggedStart(*[AnimationGroup(*_resize(b, _radius(sym))) for sym, b in zip(ROW, row)], lag_ratio=0.25),
               run_time=2.2)

    beat(scene, t, 5)
    ratio = pm.COVALENT_RADII_PM["Li"] / pm.COVALENT_RADII_PM["F"]
    sizes = VGroup(txt(f"Li {pm.COVALENT_RADII_PM['Li']} pm", cfg.FONT["label"], cfg.BLUE),
                   txt(f"F {pm.COVALENT_RADII_PM['F']} pm", cfg.FONT["label"], cfg.GREEN),
                   txt(f"≈ {ratio:.1f}×", cfg.FONT["section"], cfg.GOLD)).arrange(RIGHT, buff=0.5)
    sizes.move_to(DOWN * 1.0)
    scene.play(FadeOut(VGroup(steps, stronger)), FadeIn(sizes, shift=UP * 0.2), run_time=1.0)
    scene.play(Indicate(row[0].sphere, color=cfg.WHITE), Indicate(row[-1].sphere, color=cfg.WHITE), run_time=1.2)

    # --- Down group 1 -------------------------------------------------------------------
    beat(scene, t, 6)
    head = swap_heading(scene, head, "Down → larger")
    column = [_ball(sym, li_r).move_to(p) for sym, p in zip(COLUMN, bottom_points)]
    link = DashedLine(row[0].get_bottom() + DOWN * 0.08, column[0].get_top() + UP * 0.08, stroke_color=cfg.BLUE,
                      stroke_width=3, dash_length=0.08)
    scene.play(FadeOut(sizes), FadeOut(charges), run_time=0.5)
    scene.play(Create(link), LaggedStart(*[FadeIn(b, shift=UP * 0.3) for b in column], lag_ratio=0.2), run_time=1.6)

    beat(scene, t, 7)
    shells = VGroup(*[eq(rf"{n}s^{{1}}", cfg.FONT["small"], cfg.CYAN).move_to([b.get_x(), BOTTOM_Y + li_r + 0.35, 0])
                      for n, b in zip(range(2, 7), column)])
    scene.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.15) for s in shells], lag_ratio=0.25), run_time=1.6)
    new_shell = txt("A new outer shell", cfg.FONT["small"], cfg.CYAN).move_to(UP * 0.1)
    scene.play(FadeIn(new_shell), run_time=0.6)

    beat(scene, t, 8)
    scene.play(FadeOut(shells), FadeOut(link), run_time=0.4)
    scene.play(LaggedStart(*[AnimationGroup(*_resize(b, _radius(sym))) for sym, b in zip(COLUMN, column)], lag_ratio=0.25),
               run_time=2.2)
    grow = pm.COVALENT_RADII_PM["Cs"] / pm.COVALENT_RADII_PM["Li"]
    cs_size = VGroup(txt(f"Cs {pm.COVALENT_RADII_PM['Cs']} pm", cfg.FONT["label"], cfg.BLUE),
                     txt(f"≈ {grow:.1f}× lithium", cfg.FONT["section"], cfg.GOLD)).arrange(RIGHT, buff=0.45)
    cs_size.move_to(UP * 0.1)
    scene.play(ReplacementTransform(new_shell, cs_size), run_time=0.8)

    # --- Grip, ionization energy, metallic character ---------------------------------------
    beat(scene, t, 9)
    head = swap_heading(scene, head, "Size is just the beginning")
    grip = VGroup(txt("tighter grip", cfg.FONT["label"], cfg.GOLD), eq(r"\Rightarrow", cfg.FONT["label"]),
                  txt("harder to ionize", cfg.FONT["label"], cfg.WHITE)).arrange(RIGHT, buff=0.3)
    grip.move_to(UP * 0.1)
    scene.play(ReplacementTransform(cs_size, grip), run_time=0.8)
    tug = glow_dot(row[-1].get_right() + RIGHT * 0.2, 0.09)
    scene.play(FadeIn(tug), run_time=0.3)
    scene.play(tug.animate(rate_func=there_and_back).shift(RIGHT * 0.45), run_time=1.2)
    scene.play(FadeOut(tug), run_time=0.3)

    beat(scene, t, 10)
    across = Arrow([top_points[0][0], 0.55, 0], [top_points[-1][0], 0.55, 0], buff=0, color=cfg.GREEN, stroke_width=7)
    up = Arrow([bottom_points[-1][0], -0.2, 0], [bottom_points[0][0], -0.2, 0], buff=0, color=cfg.GREEN, stroke_width=7)
    ie = txt("ionization energy ↑", cfg.FONT["label"], cfg.GREEN).move_to(UP * 0.17)
    scene.play(FadeOut(grip), GrowArrow(across), GrowArrow(up), FadeIn(ie), run_time=1.4)
    scene.play(Indicate(ie, color=cfg.WHITE, scale_factor=1.06), run_time=0.8)

    beat(scene, t, 11)
    metal = VGroup(txt("metallic character", cfg.FONT["label"], cfg.ORANGE), txt("generally grows down + left", cfg.FONT["small"], cfg.ORANGE))
    metal.arrange(DOWN, buff=0.1).move_to(UP * 0.17)
    scene.play(FadeOut(VGroup(across, up, ie)), FadeIn(metal), run_time=0.9)
    scene.play(Indicate(column[-1].sphere, color=cfg.ORANGE, scale_factor=1.06), run_time=1.2)

    beat(scene, t, 12)
    head = swap_heading(scene, head, "Size · ionization · metallic character")
    cause = VGroup(chip("size", cfg.CYAN, cfg.FONT["small"]), chip("grip", cfg.GREEN, cfg.FONT["small"]),
                   chip("metal / non-metal", cfg.ORANGE, cfg.FONT["small"])).arrange(RIGHT, buff=0.35)
    cause.move_to(UP * 0.42)
    scene.play(FadeOut(metal), LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cause], lag_ratio=0.2), run_time=1.0)
    later = txt("Next: periodic trends", cfg.FONT["tiny"], cfg.MUTED).next_to(cause, DOWN, buff=0.12)
    scene.play(FadeIn(later), run_time=0.5)

    beat(scene, t, 13)
    filling = caption("Structure → properties", cfg.GOLD, cfg.FONT["small"], y=-4.1)
    hud(scene, filling)
    scene.play(FadeOut(to_scale), FadeIn(filling, shift=UP * 0.15), run_time=0.8)
    scene.play(*[Indicate(b.sphere, color=cfg.WHITE, scale_factor=1.04) for b in row + column[1:]], run_time=1.6)
    scene.play(Indicate(filling, color=cfg.WHITE, scale_factor=1.04), run_time=1.4)
    end_scene(scene, t, cfg.SCENE_DURATIONS["14"])
