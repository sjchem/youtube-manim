"""Scene 17 — density is the bridge from molarity to molality. One litre of
the reference solution as a turning 3D cube: its mass from the density, the
glucose in it from the molarity, the rest is water — and molality comes out
at 0.556 again (``physics_models.litre_breakdown``). Then m = c / (rho - c M).
"""

from manim_scenes.common import *

BOX = pm.litre_breakdown()
RX = 4.1
BAR_X = -0.9
BAR_H = 5.0
BAR_BOTTOM = -3.0


class Scene17DensityBridge(Scene):
    def construct(self) -> None:
        play_scene(self)


def litre_cube(at) -> tuple[Stage, Swarm]:
    stage = Stage(at, zoom=1.2, yaw=0.55, pitch=0.38, spin=0.18, sway=0.06)
    h = 1.6
    corners = [np.array([x, y, z]) for x in (-h, h) for y in (-h, h) for z in (-h, h)]
    for i, p in enumerate(corners):
        for q in corners[i + 1:]:
            if np.sum(np.abs(p - q) > 1e-9) == 1:
                stage.add_body(Segment(p, q, cfg.VOLUME, 3.6, 0.95))
    for normal in range(3):
        for side in (-h, h):
            pts = []
            others = [k for k in range(3) if k != normal]
            for s1, s2 in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                p = np.zeros(3)
                p[normal] = side
                p[others[0]], p[others[1]] = s1 * h, s2 * h
                pts.append(p)
            stage.add_body(Face(pts, cfg.VOLUME, opacity=0.06, edge_opacity=0.0))
    swarm = Swarm(stage, Box(half=h), solvent=500, solute=5, seed=cfg.SEED + 17, solute_radius=0.12)
    swarm.solute_glow = 1.0
    return stage, swarm


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "17", "Density connects them")
    cards = VGroup(
        VGroup(txt("molarity", cfg.FONT["section"], cfg.VOLUME), txt("litres of solution", cfg.FONT["label"], cfg.WHITE)),
        VGroup(txt("molality", cfg.FONT["section"], cfg.SOLVENT_MASS), txt("kilograms of solvent", cfg.FONT["label"], cfg.WHITE)),
    )
    for c in cards:
        c.arrange(DOWN, buff=0.2)
    cards.arrange(RIGHT, buff=5.6).move_to([0, 1.0, 0])
    scene.play(FadeIn(cards[0], shift=RIGHT * 0.2), FadeIn(cards[1], shift=LEFT * 0.2), run_time=1.2)

    # --- 2. We need a bridge from volume to mass -------------------------------------------------------------------
    beat(scene, t, 1)
    bridge = glow_arrow(cards[0].get_right() + RIGHT * 0.3, cards[1].get_left() + LEFT * 0.3, cfg.SOLUTION_MASS)
    q = txt("?", cfg.FONT["title"], cfg.GOLD).next_to(bridge, UP, buff=0.15)
    scene.play(GrowFromEdge(bridge, LEFT), FadeIn(q), run_time=1.2)
    words = txt("volume → mass", cfg.FONT["body"], cfg.SOLUTION_MASS).next_to(bridge, DOWN, buff=0.35)
    scene.play(FadeIn(words), run_time=0.7)

    # --- 3. Density: 1.037 g/mL -------------------------------------------------------------------------------------
    beat(scene, t, 2)
    rho = eq([r"\rho", "=", r"\frac{", rf"{fx(REF.solution_g, 1)}\ \mathrm{{g}}", "}{", rf"{V_ML}\ \mathrm{{mL}}", "}", r"\approx",
              rf"{fx(REF.density_g_per_mL, 3)}\ \mathrm{{g/mL}}"], cfg.FONT["section"])
    rho[0].set_color(cfg.SOLUTION_MASS)
    rho[3].set_color(cfg.SOLUTION_MASS)
    rho[5].set_color(cfg.VOLUME)
    rho[8].set_color(cfg.SOLUTION_MASS)
    fit_width(rho, 12.0)
    rho.move_to([0, -1.9, 0])
    density = txt("density", cfg.FONT["body"], cfg.SOLUTION_MASS).move_to(q)
    scene.play(fade_through(q, density), run_time=0.8)
    scene.remove(q)
    scene.play(Write(rho), run_time=1.8)

    # --- 4. One litre as a cube: about 1037 g ------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(VGroup(cards, bridge, words, density)), run_time=0.5)
    scene.play(rho.animate.scale(0.62).move_to([RX + 0.5, 2.7, 0]), run_time=0.6)
    stage, swarm = litre_cube([-4.6, -0.5, 0])
    show(scene, stage, 1.2)
    one_l = txt("1 L", cfg.FONT["section"], cfg.VOLUME).move_to([-4.6, 2.55, 0])
    total_bar = Rectangle(width=0.9, height=BAR_H, stroke_color=cfg.SOLUTION_MASS, stroke_width=3, fill_color=cfg.SOLUTION_MASS,
                          fill_opacity=0.25).move_to([BAR_X, BAR_BOTTOM + BAR_H / 2, 0])
    total = eq(rf"\approx {BOX['total_g']:.1f}\ \mathrm{{g}}", cfg.FONT["body"], cfg.SOLUTION_MASS)
    total.next_to(total_bar, UP, buff=0.2)
    scene.play(FadeIn(one_l), GrowFromEdge(total_bar, DOWN), FadeIn(total), run_time=1.4)

    # --- 5. The glucose in it: about 94 g ------------------------------------------------------------------------------------
    beat(scene, t, 4)
    g_h = BAR_H * BOX["solute_g"] / BOX["total_g"]
    gold_bar = Rectangle(width=0.9, height=g_h, stroke_width=0, fill_color=cfg.SOLUTE, fill_opacity=1)
    gold_bar.move_to([BAR_X, BAR_BOTTOM + BAR_H - g_h / 2, 0])
    glucose = eq([rf"{M_TEXT}\ \mathrm{{mol}} \times {fx(pm.M_GLUCOSE, 0)}\ \mathrm{{g/mol}}", r"\approx",
                  rf"{BOX['solute_g']:.1f}\ \mathrm{{g}}"], cfg.FONT["label"])
    glucose[2].set_color(cfg.SOLUTE)
    fit_width(glucose, 6.0)
    glucose.move_to([RX + 0.5, 1.2, 0])
    scene.play(set_attr(stage, swarm, "solute_glow", 2.0), Write(glucose), run_time=1.5)
    scene.play(GrowFromEdge(gold_bar, UP), set_attr(stage, swarm, "solute_glow", 1.0), run_time=0.9)

    # --- 6. The rest is water: about 942.4 g -------------------------------------------------------------------------------------
    beat(scene, t, 5)
    w_h = BAR_H - g_h
    blue_bar = Rectangle(width=0.9, height=w_h, stroke_width=0, fill_color=cfg.SOLVENT_MASS, fill_opacity=0.85)
    blue_bar.move_to([BAR_X, BAR_BOTTOM + w_h / 2, 0])
    water = eq([rf"{BOX['total_g']:.1f} - {BOX['solute_g']:.1f}", r"\approx", rf"{BOX['solvent_g']:.1f}\ \mathrm{{g}}"],
               cfg.FONT["label"])
    water[2].set_color(cfg.SOLVENT_MASS)
    fit_width(water, 6.0)
    water.move_to([RX + 0.5, -0.1, 0])
    scene.play(Write(water), set_attr(stage, swarm, "solvent_glow", 1.0), run_time=1.4)
    scene.play(GrowFromEdge(blue_bar, DOWN), run_time=1.0)
    w_tag = txt("water", cfg.FONT["small"], cfg.SOLVENT_MASS).next_to(blue_bar, RIGHT, buff=0.2)
    g_tag = txt("glucose", cfg.FONT["small"], cfg.SOLUTE).next_to(gold_bar, RIGHT, buff=0.2)
    scene.play(FadeIn(w_tag), FadeIn(g_tag), run_time=0.6)

    # --- 7. Molality: 0.556 again ---------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    molal = numbers_fraction(rf"{M_TEXT}\ \mathrm{{mol}}", rf"{fx(BOX['solvent_g'] / 1000, 4)}\ \mathrm{{kg}}",
                             rf"{m_TEXT}\ \mathrm{{m}}", cfg.AMOUNT, cfg.SOLVENT_MASS, cfg.FONT["section"])
    fit_width(molal, 5.8)
    molal_box = boxed(molal).move_to([RX + 0.5, -1.9, 0])
    scene.play(FadeIn(molal_box, scale=1.06), set_attr(stage, swarm, "solvent_glow", 0.0), run_time=1.2)
    same = txt("just as before", cfg.FONT["small"], cfg.RESULT).next_to(molal_box, DOWN, buff=0.2)
    scene.play(FadeIn(same), run_time=0.6)

    # --- 8. One formula --------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(glucose, water, molal_box, same, rho)), run_time=0.7)
    law = eq(["m", "=", r"\frac{c}{", r"\rho", "-", r"c\,M_s", "}"], cfg.FONT["hero"])
    fit_width(law, 6.0)
    law.move_to([RX + 0.6, 1.75, 0])
    law[3].set_color(cfg.SOLUTION_MASS)
    law[5].set_color(cfg.SOLUTE)
    units = eq(r"c:\ \mathrm{mol/L}\quad \rho:\ \mathrm{kg/L}\quad M_s:\ \mathrm{kg/mol}",
               cfg.FONT["tiny"], cfg.MUTED)
    fit_width(units, 6.0)
    units.move_to([RX + 0.6, 0.0, 0])
    scene.play(Write(law), FadeIn(units), run_time=1.8)

    # --- 9. Read it ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    reads = VGroup(
        VGroup(eq(r"\rho", cfg.FONT["body"], cfg.SOLUTION_MASS), txt("solution mass per litre", cfg.FONT["small"], cfg.WHITE)),
        VGroup(eq(r"c\,M_s", cfg.FONT["body"], cfg.SOLUTE), txt("solute mass per litre", cfg.FONT["small"], cfg.WHITE)),
        VGroup(eq(r"\rho - c\,M_s", cfg.FONT["body"], cfg.SOLVENT_MASS), txt("solvent mass per litre", cfg.FONT["small"], cfg.WHITE)),
    )
    for r in reads:
        r.arrange(RIGHT, buff=0.3)
    reads.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([RX + 0.6, -1.6, 0])
    fit_width(reads, 6.0)
    for r, bar in zip(reads, (total_bar, gold_bar, blue_bar)):
        scene.play(FadeIn(r, shift=UP * 0.1), Indicate(bar, color=cfg.WHITE, scale_factor=1.04), run_time=1.0)
        narration_wait(scene, 0.8)

    # --- 10. The bridge ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    final = result_label("Density: the bridge between volume and mass", cfg.SOLUTION_MASS, cfg.FONT["label"]).move_to([0, -3.65, 0])
    fit_width(final, 13.0)
    scene.play(FadeOut(reads), FadeIn(final, shift=UP * 0.15), run_time=1.0)
    scene.play(Circumscribe(law, color=cfg.SOLUTION_MASS, buff=0.15), run_time=2.5)
    scene.play(law.animate.scale(1.05), run_time=4.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["17"])
