"""Electron density as a landscape (3D), then electronegativity on the table.

The surface is ``mu.bond_density``: two atomic humps plus a shared ridge
whose position is set by a "lean" that grows with the electronegativity
difference (lean = ΔEN / 2.4, capped). It illustrates unequal sharing; it is
not a computed molecular density. The surface is rebuilt only while a morph
plays, so between morphs it is a cached, static solid. The table colours are
Pauling electronegativities (main-group elements; noble gases have no
comparable value and stay dim).
"""

from manim_scenes.common import *

SEPARATION = 3.6
HEIGHT = 1.3
FLOOR = IN * 0.45           # reserve a clear strip below the landscape for the caption
PITCH = 0.62
TABLE_AT = DOWN * 0.55


class Scene15BondLandscape(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def density_surface(lean: float) -> Surface:
    peak = HEIGHT * 2.3
    surface = Surface(lambda u, v: np.array([u, v, HEIGHT * mu.bond_density(u, v, SEPARATION, lean)]) + FLOOR,
                      u_range=[-4.4, 4.4], v_range=[-2.2, 2.2], resolution=(34, 14), fill_opacity=0.94,
                      stroke_width=0.4)
    for face in surface:
        height = (face.get_center() - FLOOR)[2] / peak
        colour = mu.scale_color(height, cfg.HEAT_STOPS)
        face.set_fill(colour, 0.94)
        face.set_stroke(interpolate_color(ManimColor(colour), ManimColor(cfg.WHITE), 0.3), width=0.4, opacity=0.5)
    return surface


def lean_for(delta_en: float) -> float:
    return min(delta_en / 2.4, 0.95)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "15", "Electron density, in 3D")

    state = {"lean": 0.0}
    surface = density_surface(0.0)

    def set_lean(value: float) -> None:
        state["lean"] = value
        surface.become(density_surface(value))

    def morph(delta_en: float, run_time: float) -> None:
        scene.play(Tween(surface, lambda: state["lean"], set_lean, lean_for(delta_en)), run_time=run_time)

    scene.set_camera_orientation(phi=62 * DEGREES, theta=-64 * DEGREES, zoom=1.05)
    scene.play(FadeIn(surface), run_time=1.6)
    height_note = caption('Illustrative electron density', cfg.CYAN, cfg.FONT["small"], y=-3.95)
    hud(scene, height_note)
    scene.play(FadeIn(height_note), run_time=0.7)
    scene.begin_ambient_camera_rotation(rate=0.035)

    # --- 1. Identical atoms: a symmetric ridge -------------------------------------------------------
    head = dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    stage = chip('Cl–Cl:  ΔEN = 0', cfg.WHITE, cfg.FONT["small"]).move_to([0, 2.95, 0])
    hud(scene, stage)
    scene.play(FadeIn(stage), run_time=0.7)

    def swap_stage(old: VGroup, text: str, colour: str) -> VGroup:
        new = chip(text, colour, cfg.FONT["small"]).move_to([0, 2.95, 0])
        hud(scene, new)
        scene.play(*fade_labels(old, new), run_time=0.6)
        return new

    # --- 2. One partner pulls harder: the ridge leans --------------------------------------------------
    beat(scene, t, 2)
    delta_hcl = ed.ELECTRONEGATIVITY["Cl"] - ed.ELECTRONEGATIVITY["H"]
    stage = swap_stage(stage, f"H–Cl:  ΔEN ≈ {delta_hcl:.1f}", cfg.CYAN)
    morph(delta_hcl, 2.6)

    # --- 3. A bigger difference -----------------------------------------------------------------------------
    beat(scene, t, 3)
    stage = swap_stage(stage, "ΔEN ≈ 2", cfg.GOLD)
    morph(2.0, 2.4)

    # --- 4. Increasing ionic character; no universal numerical cutoff ----------------------------------------------------------------------
    beat(scene, t, 4)
    delta_nacl = ed.ELECTRONEGATIVITY["Cl"] - ed.ELECTRONEGATIVITY["Na"]
    stage = swap_stage(stage, f"Na–Cl:  ΔEN ≈ {delta_nacl:.1f}", cfg.ORANGE)
    morph(delta_nacl, 2.4)
    scene.wait(0.8)

    # --- 5. Light up the table ------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.stop_ambient_camera_rotation()
    scene.play(FadeOut(surface), FadeOut(stage), FadeOut(height_note), run_time=0.6)
    move_camera(scene, phi=0, theta=-PI / 2, zoom=1.0, run_time=1.0)
    table = periodic_table(pitch=PITCH, center=TABLE_AT, style="silhouette")
    new_head = heading("Electronegativity across the table")
    hud(scene, new_head)
    scene.play(FadeIn(new_head), FadeIn(table), run_time=0.7)
    head = new_head
    main = set(main_group_zs())
    waves = []
    for column in ed.MAIN_GROUP_COLUMNS:
        tiles = [table.tiles[z] for z in main if pm.position(z)[1] == column]
        waves.append(AnimationGroup(*recolor_tiles(tiles, lambda z: heat_color("electronegativity", z), fill=0.85)))
    scene.play(LaggedStart(*waves, lag_ratio=0.2), run_time=1.8)

    # --- 6. Up and to the right ------------------------------------------------------------------------------
    beat(scene, t, 6)
    start_pt = table.tiles[pm.z_of("Cs")].get_center() + RIGHT * 0.2
    end_pt = table.tiles[pm.z_of("F")].get_center() + LEFT * 0.35 + DOWN * 0.15
    rise = glow_arrow(start_pt, end_pt, cfg.TREND_ARROW, 7, tip=0.32)
    legend = heat_legend("low", "high", width=3.4).move_to([3.9, 2.9, 0])
    scene.play(GrowArrow(rise.arrow), FadeIn(rise[0]), FadeIn(legend), run_time=1.2)
    upright = txt('Generally increases ↑ →', cfg.FONT["small"], cfg.WHITE).move_to([-3.6, 2.9, 0])
    scene.play(FadeIn(upright, shift=DOWN * 0.1), run_time=0.7)

    # --- 7. Fluorine on top; caesium near the bottom ---------------------------------------------------------
    beat(scene, t, 7)
    f_tile, cs_tile = table.tiles[pm.z_of("F")], table.tiles[pm.z_of("Cs")]
    f_frame, cs_frame = glow_frame(f_tile, cfg.GOLD, buff=0.05), glow_frame(cs_tile, cfg.CYAN, buff=0.05)
    f_value = txt(f"F ≈ {ed.ELECTRONEGATIVITY['F']:.1f}", cfg.FONT["label"], cfg.GOLD).move_to([0.6, 1.75, 0])
    f_link = Line(f_value.get_right() + RIGHT * 0.1, f_tile.get_left() + LEFT * 0.05, stroke_color=cfg.GOLD, stroke_width=3)
    cs_value = txt(f"Cs {ed.ELECTRONEGATIVITY['Cs']:.2f}", cfg.FONT["label"], cfg.CYAN).move_to(cs_tile.get_center() + DOWN * 2.15 + LEFT * 0.15)
    scene.play(FadeOut(rise), Create(f_frame), FadeIn(f_value, shift=DOWN * 0.1), Create(f_link), run_time=1.0)
    scene.play(Create(cs_frame), FadeIn(cs_value, shift=UP * 0.1), run_time=1.0)

    # --- 8. Same reason as before --------------------------------------------------------------------------------
    beat(scene, t, 8)
    reason = VGroup(chip("small atom", cfg.CYAN, cfg.FONT["small"]), eq("+", cfg.FONT["label"]),
                    VGroup(txt("high", cfg.FONT["small"], cfg.ZEFF_COLOR), eq(r"Z_{\mathrm{eff}}", cfg.FONT["small"], cfg.ZEFF_COLOR))
                    .arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.3)
    reason.move_to([2.6, -3.9, 0])
    scene.play(FadeIn(reason, shift=UP * 0.15), run_time=0.9)
    scene.play(Indicate(f_tile, color=cfg.WHITE, scale_factor=1.25), run_time=1.0)

    # --- 9. Can we predict chemistry? -------------------------------------------------------------------------------
    beat(scene, t, 9)
    ask = chip('Now: predict chemistry', cfg.GOLD, cfg.FONT["body"]).move_to([-3.4, 2.9, 0])
    scene.play(*fade_labels(upright, ask), run_time=0.9)
    scene.play(Circumscribe(ask, color=cfg.GOLD), run_time=1.2)
    na_cl = VGroup(glow_frame(table.tiles[11], cfg.BLUE, buff=0.05), glow_frame(table.tiles[17], cfg.GREEN, buff=0.05))
    scene.play(Create(na_cl), run_time=0.8)
    scene.play(Indicate(table.tiles[11], color=cfg.WHITE, scale_factor=1.3), Indicate(table.tiles[17], color=cfg.WHITE, scale_factor=1.3),
               run_time=1.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["15"])
