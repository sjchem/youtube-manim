"""Hook: two hydrogen atoms meet, settle, and pose the film's question.

The two clouds are one ``PairCloud`` whose dots flow from two round atoms into
one shared cloud as the nuclei reach the bonded distance; the separation is a
tracker, so the clouds and nuclei can never fall out of step. Salt and copper
are previewed with the same crystal and electron-sea objects the film uses
later, so their reappearance in chapters 11 and 13 reads as a promise kept.
"""

from manim_scenes.common import *

ATOM_Y = 0.45
BONDED = 2.1           # bonded separation on screen (schematic)
RADIUS = 1.45


class Scene01InvisibleForce(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "01")

    # --- 1. Two hydrogen atoms drifting in the dark -------------------------------------------------
    gap, cx, cy = ValueTracker(12.0), ValueTracker(0.0), ValueTracker(ATOM_Y)
    cloud = bind_pair(PairCloud(LEFT, RIGHT, RADIUS, count=640, seed=11, glow=0.18, dot_radius=0.034), gap.get_value,
                      lambda: [cx.get_value(), cy.get_value(), 0])
    cloud.set_level(0.0)
    scene.add(cloud)
    nuclei = pair_nuclei(cloud, ("+", "+"), radius=0.27)
    scene.add(nuclei)
    scene.play(track(gap, 8.4), cloud.fade_to(1.0), run_time=3.0, rate_func=rush_from)
    names = VGroup(*[txt("H", cfg.FONT["section"], cfg.MUTED) for _ in range(2)])
    for index, name in enumerate(names):
        name.add_updater(lambda m, i=index: m.move_to(cloud.ends[i].get_center() + DOWN * 2.2))
        name.update(0)
    scene.play(FadeIn(names), run_time=0.7)
    scene.play(*[Indicate(n.ball, color=cfg.WHITE, scale_factor=1.4) for n in nuclei], run_time=1.0)
    scene.play(track(gap, 7.4), run_time=2.6, rate_func=linear)

    # --- 2. Closer: like charges repel ------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(track(gap, 4.6), FadeOut(names), run_time=2.2)
    push_nuclei = force_line(lambda: cloud.ends[0].get_center(), lambda: cloud.ends[1].get_center(), cfg.REPEL,
                             width=6, dashed=True, buff=0.32)
    tag_nn = eq(r"+ \leftrightarrow +", cfg.FONT["body"], cfg.REPEL).move_to([0, ATOM_Y + 2.15, 0])
    scene.play(Create(push_nuclei), FadeIn(tag_nn, shift=DOWN * 0.1), run_time=1.0)
    tag_ee = eq(r"- \leftrightarrow -", cfg.FONT["body"], cfg.REPEL).move_to([0, ATOM_Y - 2.15, 0])
    scene.play(FadeIn(tag_ee, shift=UP * 0.1), Wiggle(VGroup(tag_nn, tag_ee), scale_value=1.08), run_time=1.3)

    # --- 3. Yet they settle together -------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(VGroup(tag_nn, tag_ee)), push_nuclei.animate.set_stroke(opacity=0), run_time=0.5)
    scene.remove(push_nuclei)
    scene.play(track(gap, BONDED), cloud.share_to(1.0), run_time=2.6, rate_func=smooth)
    scene.play(track(gap, BONDED * 1.18), run_time=0.5, rate_func=there_and_back)
    scene.play(track(gap, BONDED * 0.9), run_time=0.45, rate_func=there_and_back)
    left_tick = Line(UP * 0.18, DOWN * 0.18, stroke_color=cfg.WHITE, stroke_width=4)
    bracket = VGroup(Line([-BONDED / 2, ATOM_Y - 2.05, 0], [BONDED / 2, ATOM_Y - 2.05, 0], stroke_color=cfg.WHITE, stroke_width=4),
                     left_tick.copy().move_to([-BONDED / 2, ATOM_Y - 2.05, 0]),
                     left_tick.copy().move_to([BONDED / 2, ATOM_Y - 2.05, 0]))
    one_distance = txt("one stable distance", cfg.FONT["body"], cfg.GOLD).next_to(bracket, DOWN, buff=0.3)
    scene.play(Create(bracket), FadeIn(one_distance, shift=UP * 0.1), run_time=1.0)

    # --- 4. Three questions --------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(VGroup(bracket, one_distance)), run_time=0.5)
    apart = VGroup(glow_arrow([-3.0, ATOM_Y + 0.5, 0], [-5.6, ATOM_Y + 0.5, 0], cfg.MUTED, 6),
                   glow_arrow([3.0, ATOM_Y + 0.5, 0], [5.6, ATOM_Y + 0.5, 0], cfg.MUTED, 6))
    q_apart = chip("fly apart?", cfg.MUTED, cfg.FONT["label"]).move_to([-4.6, ATOM_Y + 1.6, 0])
    scene.play(*[GrowArrow(a.arrow) for a in apart], FadeIn(VGroup(*[a[0] for a in apart])), FadeIn(q_apart), run_time=0.9)
    inward = VGroup(glow_arrow([-5.6, ATOM_Y - 0.5, 0], [-3.1, ATOM_Y - 0.5, 0], cfg.REPEL, 6),
                    glow_arrow([5.6, ATOM_Y - 0.5, 0], [3.1, ATOM_Y - 0.5, 0], cfg.REPEL, 6))
    q_collapse = chip("collapse?", cfg.REPEL, cfg.FONT["label"]).move_to([4.6, ATOM_Y + 1.6, 0])
    scene.play(*[GrowArrow(a.arrow) for a in inward], FadeIn(VGroup(*[a[0] for a in inward])), FadeIn(q_collapse), run_time=0.9)
    holding = txt("What holds them together?", cfg.FONT["title"], cfg.GOLD).move_to([0, -2.85, 0])
    scene.play(FadeIn(holding, shift=UP * 0.15), run_time=0.9)
    scene.play(Indicate(holding, color=cfg.WHITE, scale_factor=1.04), run_time=1.0)

    # --- 5. Salt and copper ask the same question ------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(VGroup(apart, inward, q_apart, q_collapse, holding)), run_time=0.5)
    panels = VGroup(*[panel(4.3, 4.3, cfg.MUTED, 0.55).move_to([x, 0.15, 0]) for x in (-4.75, 0, 4.75)])
    scene.play(track(cx, -4.75), track(cy, 0.35), track(gap, 1.3), cloud.resize_to(0.95), nuclei.animate.scale(0.8),
               FadeIn(panels[0]), run_time=1.2)
    crystal = rock_salt_crystal(1, 0.95, [0, 0.35, 0], cation=0.2, anion=0.33, assembly=0.0, spin=0.3)
    metal = MetalSea(5, 4, 0.72, [4.75, 0.35, 0], core_radius=0.24, electrons=70, seed=12, signs=False)
    scene.add(crystal)
    scene.play(FadeIn(panels[1]), crystal.assemble(1.0), run_time=1.8)
    scene.play(FadeIn(panels[2]), FadeIn(metal), run_time=1.0)
    names = VGroup(eq(r"\mathrm{H_2}", cfg.FONT["label"], cfg.CYAN), txt("salt", cfg.FONT["label"], cfg.WHITE),
                   txt("copper", cfg.FONT["label"], cfg.METAL_CORE))
    for name, box in zip(names, panels):
        name.next_to(box, DOWN, buff=0.28)
    scene.play(LaggedStart(*[FadeIn(n, shift=UP * 0.12) for n in names], lag_ratio=0.25), run_time=1.0)
    ways = VGroup(txt("shared", cfg.FONT["small"], cfg.CYAN), txt("ionic lattice", cfg.FONT["small"], cfg.CATION),
                  txt("delocalised", cfg.FONT["small"], cfg.METAL_CORE))
    for way, box in zip(ways, panels):
        way.next_to(box, UP, buff=0.2)
    scene.play(LaggedStart(*[FadeIn(w) for w in ways], lag_ratio=0.3), run_time=1.2)

    # --- 6. One physics: the title ------------------------------------------------------------------------------
    beat(scene, t, 5)
    everything = VGroup(panels, names, ways)
    scene.play(everything.animate.set_opacity(0.0), crystal.assemble(0.0), metal.fade_to(0.0),
               track(cx, 0.0), track(cy, -2.75), track(gap, 1.6), run_time=1.4)
    scene.remove(everything, crystal, metal)
    card = title_card("CHEMICAL BONDING", "EXPLAINED VISUALLY").move_to(UP * 1.35)
    rule = Line(LEFT * 5.4, RIGHT * 5.4, stroke_color=cfg.CYAN, stroke_width=3).next_to(card, DOWN, buff=0.32)
    part = txt(cfg.PROJECT_PART, cfg.FONT["small"], cfg.MUTED).next_to(rule, DOWN, buff=0.28)
    scene.play(FadeIn(card, shift=DOWN * 0.15), Create(rule), run_time=1.4)
    scene.play(FadeIn(part, shift=UP * 0.1), run_time=0.6)
    scene.play(Indicate(card.title[0], color=cfg.WHITE, scale_factor=1.04), run_time=1.3)
    scene.play(VGroup(card, rule, part).animate.scale(1.04), run_time=2.4, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["01"])
