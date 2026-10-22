"""Chapter 04 — counting regions: three rules, the AXmEn code, the steric number.

Each rule is a flat fragment (single, double, triple bond, lone pair) that
points to one region lobe. Ammonia's code and steric number are read off its
Lewis structure: the counts come from the molecule library (valence electrons
give the lone pair), and the closing model is ammonia's own region layout.
"""

from manim_scenes.common import *

ROW_Y = (2.15, 0.85, -0.45, -1.75)


class Scene04CountingRegions(Scene):
    def construct(self) -> None:
        play_scene(self)


def fragment(order: int) -> VGroup:
    """'A' bonded to 'X' with 1-3 lines, or 'A' with a lone pair (order 0)."""
    a = txt("A", cfg.FONT["section"], cfg.WHITE)
    if order == 0:
        dots = dot_pair(ORIGIN, 0, 0.0, cfg.LONE_PAIR_COLOR, radius=0.09, gap=0.2).rotate(PI / 2)
        return VGroup(a, dots.next_to(a, RIGHT, buff=0.3))
    x = txt("X", cfg.FONT["section"], cfg.CYAN)
    offsets = {1: [0.0], 2: [-0.1, 0.1], 3: [-0.17, 0.0, 0.17]}[order]
    lines = VGroup(*[Line(LEFT * 0.55, RIGHT * 0.55, stroke_color=cfg.WHITE, stroke_width=7).shift(UP * o)
                     for o in offsets])
    return VGroup(a, lines, x).arrange(RIGHT, buff=0.2)


def region_icon(lone: bool = False) -> VGroup:
    color = cfg.LONE_PAIR_COLOR if lone else cfg.DOMAIN_COLOR
    lobe = Ellipse(width=1.3 if not lone else 1.05, height=0.5 if not lone else 0.72, stroke_color=color, stroke_width=3,
                   fill_color=color, fill_opacity=0.32)
    core = Circle(radius=0.12, stroke_width=0, fill_color=cfg.WHITE, fill_opacity=1).next_to(lobe, LEFT, buff=-0.05)
    return VGroup(lobe, core)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "04", "Counting regions")
    intro = caption("Count the regions around the central atom", cfg.CYAN)
    scene.play(FadeIn(intro), run_time=0.8)
    dismiss_opening_title(scene, t, head)

    # --- 1-4. Three rules (and the lone pair) -------------------------------------------------------------
    rows = VGroup()
    for k, (order, words) in enumerate(((1, "single bond"), (2, "double bond"), (3, "triple bond"), (0, "lone pair"))):
        frag = fragment(order).move_to([-4.6, ROW_Y[k], 0])
        name = txt(words, cfg.FONT["body"], cfg.PURPLE if order == 0 else cfg.WHITE).move_to([-1.0, ROW_Y[k], 0])
        arrow = Arrow([1.0, ROW_Y[k], 0], [2.2, ROW_Y[k], 0], buff=0, color=cfg.MUTED, stroke_width=6)
        icon = region_icon(order == 0).move_to([3.3, ROW_Y[k], 0])
        count = txt("1 region", cfg.FONT["body"], cfg.PURPLE if order == 0 else cfg.CYAN).move_to([5.6, ROW_Y[k], 0])
        rows.add(VGroup(frag, name, arrow, icon, count))
    for k, index in enumerate((1, 2, 3, 4)):
        beat(scene, t, index)
        row = rows[k]
        anims = [FadeIn(row[0], shift=RIGHT * 0.2), FadeIn(row[1])]
        if k == 0:
            anims.append(FadeOut(intro))
        scene.play(*anims, run_time=0.8)
        scene.play(GrowArrow(row[2]), FadeIn(row[3], scale=0.6), FadeIn(row[4]), run_time=0.9)
        if k == 1:
            same = caption("Both shared pairs point the same way", cfg.WHITE)
            scene.play(Indicate(row[0][1], color=cfg.CYAN, scale_factor=1.3), FadeIn(same), run_time=1.2)
            scene.play(FadeOut(same), run_time=0.5)

    # --- 5. The AXmEn code -------------------------------------------------------------------------------------
    beat(scene, t, 5)
    code = eq(["A", "X_m", "E_n"], 110)
    code[0].set_color(cfg.WHITE)
    code[1].set_color(cfg.DOMAIN_COLOR)
    code[2].set_color(cfg.LONE_PAIR_COLOR)
    code.move_to([0, 1.0, 0])
    keys = VGroup(txt("central atom", cfg.FONT["label"], cfg.WHITE),
                  txt("bonded atoms", cfg.FONT["label"], cfg.DOMAIN_COLOR),
                  txt("lone pairs", cfg.FONT["label"], cfg.LONE_PAIR_COLOR))
    for key, part, x in zip(keys, code, (-4.4, 0.0, 4.4)):
        key.move_to([x, -1.1, 0])
    links = VGroup(*[Line(part.get_bottom() + DOWN * 0.15, key.get_top() + UP * 0.12, stroke_color=key.get_color(),
                          stroke_width=3, stroke_opacity=0.7) for part, key in zip(code, keys)])
    scene.play(FadeOut(rows, shift=LEFT * 0.4), run_time=0.8)
    scene.play(Write(code), run_time=1.4)
    for part, key, link in zip(code, keys, links):
        scene.play(Create(link), FadeIn(key, shift=UP * 0.1), Indicate(part, scale_factor=1.12), run_time=1.0)

    # --- 6. Ammonia: AX3E ---------------------------------------------------------------------------------------
    beat(scene, t, 6)
    nh3 = ml.molecule("NH3")
    lewis = Lewis("N", [("H", 180, 1), ("H", 0, 1), ("H", 270, 1)], central_lone=[90], at=[-4.0, 0.0, 0], bond=2.0)
    name = formula("NH3", cfg.FONT["section"]).next_to(lewis, DOWN, buff=0.55)
    answer = axe_eq(len(nh3.bonds), len(nh3.lone_pairs), 100).move_to([3.4, 1.4, 0])
    scene.play(FadeOut(VGroup(code, keys, links)), run_time=0.5)
    scene.play(FadeIn(lewis), FadeIn(name), run_time=0.6)
    scene.play(LaggedStart(*[Indicate(h, color=cfg.CYAN, scale_factor=1.3) for h in lewis.ligand_symbols],
                           lag_ratio=0.3), FadeIn(answer[:2]), run_time=1.6)
    scene.play(Indicate(lewis.lone_dots, color=cfg.PURPLE, scale_factor=1.6), FadeIn(answer[2]), run_time=1.2)

    # --- 7. Steric number = 3 + 1 = 4 ------------------------------------------------------------------------------
    beat(scene, t, 7)
    total = eq([str(len(nh3.bonds)), "+", str(len(nh3.lone_pairs)), "=", str(nh3.regions)], 100)
    total[0].set_color(cfg.DOMAIN_COLOR)
    total[2].set_color(cfg.LONE_PAIR_COLOR)
    total[4].set_color(cfg.GOLD)
    total.move_to([3.4, -0.2, 0])
    steric = txt("steric number", cfg.FONT["body"], cfg.GOLD).move_to([3.4, -1.5, 0])
    scene.play(Write(total), run_time=1.4)
    frame = glow_frame(total[4], cfg.GOLD, buff=0.2)
    scene.play(Create(frame), FadeIn(steric, shift=UP * 0.1), run_time=1.0)

    # --- 8. The steric number picks the arrangement ---------------------------------------------------------------------
    beat(scene, t, 8)
    stage = Stage([3.6, 0.5, 0], zoom=1.0, yaw=0.5, pitch=0.35, spin=0.5)
    RegionModel(stage, [s.direction for s in nh3.sites], kinds=[s.kind for s in nh3.sites])
    tetra = shape_name(pm.ELECTRON_GEOMETRY[nh3.regions], size=cfg.FONT["body"]).move_to([3.6, -2.55, 0])
    scene.play(FadeOut(answer), FadeOut(total), FadeOut(frame), FadeOut(steric), run_time=0.6)
    show(scene, stage, 1.2, FadeIn(tetra, shift=UP * 0.15))
    scene.play(Indicate(tetra, color=cfg.WHITE, scale_factor=1.05), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["04"])
