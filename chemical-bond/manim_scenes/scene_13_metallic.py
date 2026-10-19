"""Metallic bonding: positive cores in a sea of delocalised electrons.

Copper's twelve nearest neighbours are counted from a face-centred cubic
lattice (``utils.bond_models.fcc_sites`` / ``neighbour_shells``) and shown as
a rotating cuboctahedron. The slab is a close-packed layer; its electrons
wander on seeded paths and belong to no core — the electron-sea picture,
labelled as a simplified model of delocalised states. The slip test shows
why: shifted metal layers stay glued, shifted ionic layers face like charges.
"""

from manim_scenes.common import *

SLAB_AT = np.array([-2.5, 0.2, 0])
PANEL_X = 4.55
PANEL_W = 4.6
# A local attraction accent stays distinct from the cyan sea and copper cores.
SEA_ATTRACTION = "#FF4FD8"


class Scene13Metallic(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "13", "Metallic bonding")

    # --- 1. A block of copper: identical atoms ----------------------------------------------------------------
    metal = MetalSea(7, 5, 1.0, SLAB_AT, core_radius=0.3, electrons=140, seed=131, signs=False, polished=True)
    metal.set_level(0.0)
    shells = VGroup(*[Circle(radius=0.48, stroke_color=cfg.ELECTRON_COLOR, stroke_width=3, stroke_opacity=0.7,
                             fill_color=cfg.ELECTRON_COLOR, fill_opacity=0.12).move_to(core)
                      for layer in metal.layers for core in layer])
    scene.add(metal)
    scene.play(FadeIn(metal.cores, lag_ratio=0.02), FadeIn(shells, lag_ratio=0.02), run_time=1.8)
    copper = VGroup(txt("Cu", cfg.FONT["title"], cfg.METAL_CORE), txt("Extended copper crystal", cfg.FONT["small"], cfg.MUTED))
    copper.arrange(DOWN, buff=0.2).move_to([PANEL_X, 2.5, 0])
    dismiss_opening_title(scene, t, head)
    scene.play(FadeIn(copper, shift=DOWN * 0.1), run_time=0.8)

    # --- 2. Twelve neighbours: too many for separate pairs -------------------------------------------------------
    beat(scene, t, 1)
    sites = bm.fcc_sites(1) * np.sqrt(2)
    centre = int(np.argmin(np.linalg.norm(sites, axis=1)))
    nearest = bm.neighbour_shells(sites, shells=1)[0]
    keep = [centre] + [i for i in range(len(sites)) if abs(np.linalg.norm(sites[i] - sites[centre]) - nearest[0]) < 1e-6]
    cluster = ProjectedCrystal(sites[keep], ["Cu"] * len(keep), {"Cu": 0.34}, {"Cu": cfg.METAL_CORE}, 1.3,
                               [PANEL_X, -0.2, 0], spin=0.35, tilt=0.45, polished=True)
    cluster._live_draw_order = True
    scene.add(cluster)
    scene.play(FadeIn(cluster), copper[1].animate.set_opacity(0), run_time=1.0)
    twelve = VGroup(txt(str(nearest[1]), 84, cfg.METAL_CORE), txt("neighbours", cfg.FONT["label"], cfg.WHITE)).arrange(RIGHT, buff=0.25)
    twelve.move_to([PANEL_X, -2.35, 0])
    scene.play(FadeIn(twelve, shift=UP * 0.1), run_time=0.8)
    too_many = txt("Not isolated pairs", cfg.FONT["small"], cfg.REPEL).next_to(twelve, DOWN, buff=0.2)
    fit_width(too_many, PANEL_W)
    scene.play(FadeIn(too_many), run_time=0.7)

    # --- 3. Each atom releases its outer electron --------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(VGroup(twelve, too_many)), FadeOut(cluster), run_time=0.6)
    cluster.clear_updaters()
    scene.play(shells.animate.scale(1.6).set_opacity(0), metal.fade_to(1.0), run_time=2.4)
    scene.remove(shells)
    release = txt("Electrons delocalise", cfg.FONT["label"], cfg.ELECTRON_COLOR).move_to([PANEL_X, 0.9, 0])
    fit_width(release, PANEL_W)
    scene.play(FadeIn(release), run_time=0.7)

    # --- 4. Positive cores, electrons that belong to no atom -----------------------------------------------------------
    beat(scene, t, 3)
    signs = VGroup(*[txt("+", cfg.FONT["tiny"], cfg.BG).move_to(core) for layer in metal.layers for core in layer])
    scene.play(FadeIn(signs), run_time=0.8)
    for layer_index, layer in enumerate(metal.layers):
        for core_index, core in enumerate(layer):
            core.add(signs[layer_index * len(layer) + core_index])
    scene.remove(signs)
    cores_tag = txt("positive ion cores", cfg.FONT["label"], cfg.METAL_CORE).move_to([PANEL_X, 0.1, 0])
    fit_width(cores_tag, PANEL_W)
    scene.play(FadeIn(cores_tag), run_time=0.7)
    delocal = chip("delocalised", cfg.ELECTRON_COLOR, cfg.FONT["label"]).move_to([PANEL_X, -0.85, 0])
    scene.play(FadeIn(delocal, shift=UP * 0.1), run_time=0.8)

    # --- 5. The electron sea (Simplified model) ----------------------------------------------------------------------
    beat(scene, t, 4)
    sea = txt("the electron sea", cfg.FONT["body"], cfg.ELECTRON_COLOR).move_to([PANEL_X, -1.9, 0])
    fit_width(sea, PANEL_W)
    simplified = txt('Simplified model', cfg.FONT["tiny"], cfg.MUTED).next_to(sea, DOWN, buff=0.35)
    scene.play(FadeOut(VGroup(release, cores_tag, delocal)), FadeIn(sea, shift=UP * 0.1), FadeIn(simplified), run_time=0.9)
    scene.play(metal.haze.animate.set_fill(opacity=0.16), run_time=1.0)
    scene.play(metal.haze.animate.set_fill(opacity=0.07), run_time=1.0)

    # --- 6. Sea and cores attract each other: the metallic bond -------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(VGroup(sea, simplified)), run_time=0.6)
    # Keep short arrows bold instead of letting Manim cap their stroke width.
    hugs = VGroup()
    for core in (metal.layers[1][2], metal.layers[2][4], metal.layers[3][1]):
        for angle in np.linspace(0, TAU, 6, endpoint=False):
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            hugs.add(Arrow(core.get_center() + direction * 0.85, core.get_center() + direction * 0.38, buff=0,
                           color=SEA_ATTRACTION, stroke_width=7, tip_length=0.18,
                           max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=20))
    scene.play(LaggedStart(*[GrowArrow(a) for a in hugs], lag_ratio=0.03), run_time=1.4)
    bond = VGroup(txt("sea", cfg.FONT["label"], cfg.ELECTRON_COLOR), eq(r"\leftrightarrow", cfg.FONT["label"], SEA_ATTRACTION),
                  txt("cores", cfg.FONT["label"], cfg.METAL_CORE)).arrange(RIGHT, buff=0.25).move_to([PANEL_X, 0.6, 0])
    metallic = chip("the metallic bond", SEA_ATTRACTION, cfg.FONT["label"]).move_to([PANEL_X, -0.5, 0])
    scene.play(FadeIn(bond, shift=UP * 0.1), run_time=0.7)
    scene.play(FadeIn(metallic, shift=UP * 0.1), run_time=0.8)

    # --- 7. Apply a voltage: the electrons drift --------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(hugs), FadeOut(VGroup(bond, metallic)), run_time=0.6)
    left_end = SLAB_AT + LEFT * (metal.half_w + 0.35)
    right_end = SLAB_AT + RIGHT * (metal.half_w + 0.35)
    plates = VGroup(Line(left_end + UP * 1.8, left_end + DOWN * 1.8, stroke_color=cfg.REPEL, stroke_width=8),
                    Line(right_end + UP * 1.8, right_end + DOWN * 1.8, stroke_color=cfg.ATTRACT, stroke_width=8))
    poles = VGroup(eq("-", 84, cfg.REPEL).next_to(plates[0], UP, buff=0.15), eq("+", 84, cfg.ATTRACT).next_to(plates[1], UP, buff=0.15))
    scene.play(Create(plates), FadeIn(poles), run_time=0.8)
    scene.play(metal.drift_to(1.1), run_time=1.2)
    flow = glow_arrow(SLAB_AT + LEFT * 2.5 + DOWN * 2.85, SLAB_AT + RIGHT * 2.5 + DOWN * 2.85, cfg.ELECTRON_COLOR, 7)
    current = txt("Electron drift", cfg.FONT["label"], cfg.ELECTRON_COLOR).move_to([PANEL_X, 0.4, 0])
    fit_width(current, PANEL_W)
    scene.play(GrowArrow(flow.arrow), FadeIn(flow[0]), FadeIn(current), run_time=1.0)

    # --- 8. Hit it: layers slide, the sea flows along ---------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(metal.drift_to(0.0), FadeOut(VGroup(plates, poles, flow, current)), run_time=1.0)
    hammer = glow_arrow(SLAB_AT + LEFT * 6.0 + UP * 1.0, SLAB_AT + LEFT * 4.9 + UP * 1.0, cfg.GOLD, 10, tip=0.4)
    scene.play(GrowArrow(hammer.arrow), FadeIn(hammer[0]), run_time=0.6)
    top = VGroup(metal.layers[0], metal.layers[1])
    scene.play(top.animate.shift(RIGHT * metal.spacing), hammer.animate.shift(RIGHT * metal.spacing), run_time=1.6)
    bends = chip("it bends", cfg.GREEN, cfg.FONT["label"]).move_to([PANEL_X, 0.4, 0])
    fit_width(bends, PANEL_W)
    scene.play(FadeIn(bends, shift=UP * 0.1), FadeOut(hammer), run_time=0.8)
    scene.play(top.animate.shift(RIGHT * metal.spacing), run_time=1.4)

    # --- 9. Salt: shift one layer and like charges face each other ---------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(metal), FadeOut(bends), FadeOut(copper[0]), run_time=0.7)
    metal.clear_updaters()
    salt = ion_layers(4, 7, 0.95, [-2.6, 0.2, 0], radius=0.38, polished=True)
    scene.play(FadeIn(salt, lag_ratio=0.02), run_time=1.0)
    upper = VGroup(salt[0], salt[1])
    scene.play(upper.animate.shift(RIGHT * 0.95), run_time=1.4)
    pushes = VGroup()
    for col in range(1, 7):
        a = salt[1][col - 1].get_center()
        b = salt[2][col].get_center()
        pushes.add(DoubleArrow(a + DOWN * 0.3, b + UP * 0.3, buff=0, color=cfg.REPEL, stroke_width=5, tip_length=0.16))
    like = txt("like charges meet", cfg.FONT["label"], cfg.REPEL).move_to([PANEL_X, 0.4, 0])
    fit_width(like, PANEL_W)
    scene.play(LaggedStart(*[GrowFromCenter(p) for p in pushes], lag_ratio=0.08), FadeIn(like), run_time=1.2)

    # --- 10. The crystal splits: salt shatters, copper bends ---------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(upper.animate.shift(UP * 1.1 + RIGHT * 0.3).rotate(0.08), FadeOut(pushes), run_time=1.0, rate_func=rush_from)
    crack = VGroup(*[Line([x, -0.25, 0], [x + 0.35, -0.65, 0], stroke_color=cfg.WHITE, stroke_width=3) for x in np.linspace(-5.4, 0.2, 6)])
    scene.play(Create(crack), run_time=0.6)
    verdict = VGroup(txt("salt shatters", cfg.FONT["label"], cfg.REPEL), txt("copper bends", cfg.FONT["label"], cfg.GREEN)).arrange(DOWN, buff=0.3)
    verdict.move_to([PANEL_X, -1.0, 0])
    scene.play(FadeIn(verdict, shift=UP * 0.1), run_time=0.8)

    # --- 11. Shared, transferred, delocalised -----------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(VGroup(salt, crack, like, verdict)), run_time=0.7)
    ways = VGroup(chip("shared", cfg.CYAN, cfg.FONT["section"]), chip("ionic lattice", cfg.CATION, cfg.FONT["section"]),
                  chip("delocalised", cfg.METAL_CORE, cfg.FONT["section"])).arrange(RIGHT, buff=0.6).move_to([0, 0.8, 0])
    scene.play(LaggedStart(*[FadeIn(w, shift=UP * 0.15) for w in ways], lag_ratio=0.3), run_time=1.4)
    lower = txt("Three paths to lower energy", cfg.FONT["title"], cfg.ENERGY).move_to([0, -0.9, 0])
    scene.play(FadeIn(lower, shift=UP * 0.1), run_time=0.8)
    scene.play(Indicate(lower, color=cfg.WHITE, scale_factor=1.04), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["13"])
