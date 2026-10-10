"""Shielding and the felt charge, then the two effects racing side by side.

Purple bars are Slater's estimate of the effective nuclear charge (the model
in ``pm.slater_zeff``), drawn without numbers because the estimate is rough.
Cloud sizes are NCERT radii on one shared scale for both panels, so the left
(same shell) and right (new shell) atoms can be compared directly.
"""

from manim_scenes.common import *

SODIUM_AT = np.array([-3.2, 0.15, 0])
SCALE = 0.0085
LEFT_AT = np.array([-3.7, 0.55, 0])
RIGHT_AT = np.array([3.7, 0.55, 0])
GAUGE_Y = -2.95
ZEFF_UNIT = 0.42                      # screen length per unit of Z_eff


class Scene04Shielding(Scene):
    def construct(self) -> None:
        play_scene(self)


def radius_of(symbol: str) -> float:
    return ed.ATOMIC_RADII_PM[symbol] * SCALE


def core_of(symbol: str) -> float:
    n = pm.outer_shell(pm.z_of(symbol))
    return radius_of(symbol) * (0.25 + 0.07 * (n - 2))


def zeff_bar(symbol: str, x: float) -> Rectangle:
    length = pm.slater_zeff(pm.z_of(symbol)) * ZEFF_UNIT
    bar = Rectangle(width=length, height=0.34, stroke_width=0, fill_color=cfg.ZEFF_COLOR, fill_opacity=0.9)
    return bar.move_to([x - 1.1 + length / 2, GAUGE_Y, 0])


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "04", "Never alone with the nucleus")

    # --- 1. One outer electron ------------------------------------------------------------
    nucleus = nucleus_core("+11", 0.36).move_to(SODIUM_AT)
    angle = 28 * DEGREES
    outer_at = SODIUM_AT + 2.55 * np.array([np.cos(angle), np.sin(angle), 0])
    electron = glow_dot(outer_at, 0.15)
    pull = Arrow(outer_at, SODIUM_AT + 0.45 * (outer_at - SODIUM_AT) / 2.55, buff=0.15, color=cfg.PULL_COLOR,
                 stroke_width=6, tip_length=0.22, max_tip_length_to_length_ratio=0.3)
    scene.play(FadeIn(nucleus, scale=0.6), FadeIn(electron, scale=0.5), run_time=1.0)
    scene.play(GrowArrow(pull), run_time=0.8)

    # --- 2. Sodium: eleven protons, ten inner electrons --------------------------------------
    head = dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    core = ElectronCloud(1.15, SODIUM_AT, count=300, seed=31, color=cfg.CORE_COLOR, spin=-0.4, glow=0.18)
    outer = ElectronCloud(2.55, SODIUM_AT, count=150, seed=32, glow=0.08)
    scene.play(FadeIn(core, scale=0.6), FadeIn(outer), run_time=1.2)
    scene.bring_to_front(nucleus, electron, pull)
    tags = VGroup(txt("11 protons", cfg.FONT["small"], cfg.PROTON_COLOR),
                  txt("10 inner electrons", cfg.FONT["small"], cfg.CORE_COLOR),
                  txt("1 outer electron", cfg.FONT["small"], cfg.CYAN)).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    tags.move_to([3.6, 1.2, 0])
    for tag in tags:
        scene.play(FadeIn(tag, shift=LEFT * 0.2), run_time=0.6)

    # --- 3. Shielding ----------------------------------------------------------------------------
    beat(scene, t, 2)
    pushes = VGroup()
    for offset in (-0.38, 0.0, 0.38):
        direction = np.array([np.cos(angle + offset), np.sin(angle + offset), 0])
        pushes.add(Arrow(SODIUM_AT + direction * 1.25, SODIUM_AT + direction * 2.0, buff=0, color=cfg.CORE_COLOR,
                         stroke_width=5, tip_length=0.18, max_tip_length_to_length_ratio=0.35))
    scene.play(LaggedStart(*[GrowArrow(p) for p in pushes], lag_ratio=0.2), pull.animate.set_opacity(0.45), run_time=1.2)
    shield = chip("shielding", cfg.CORE_COLOR, cfg.FONT["label"]).move_to([3.6, -0.75, 0])
    scene.play(FadeIn(shield, scale=1.1), run_time=0.7)
    scene.play(electron.animate(rate_func=there_and_back).shift(0.35 * (outer_at - SODIUM_AT) / 2.55), run_time=1.0)

    # --- 4. The felt charge is smaller -----------------------------------------------------------
    beat(scene, t, 3)
    full = Rectangle(width=11 * ZEFF_UNIT * 0.62, height=0.34, stroke_width=0, fill_color=cfg.PROTON_COLOR,
                     fill_opacity=0.9)
    full.move_to([1.6 + full.width / 2, -2.2, 0])
    felt_len = pm.slater_zeff(11) * ZEFF_UNIT * 0.62
    felt = Rectangle(width=felt_len, height=0.34, stroke_width=0, fill_color=cfg.ZEFF_COLOR, fill_opacity=0.9)
    felt.move_to([1.6 + felt_len / 2, -3.05, 0])
    full_tag = txt("nucleus: +11", cfg.FONT["small"], cfg.PROTON_COLOR).next_to(full, UP, buff=0.14, aligned_edge=LEFT)
    felt_tag = txt("felt: much less", cfg.FONT["small"], cfg.ZEFF_COLOR).next_to(felt, RIGHT, buff=0.3)
    scene.play(FadeOut(shield), FadeOut(tags), GrowFromEdge(full, LEFT), FadeIn(full_tag), run_time=0.9)
    scene.play(GrowFromEdge(felt, LEFT), FadeIn(felt_tag), run_time=0.9)

    # --- 5. Z effective ---------------------------------------------------------------------------
    beat(scene, t, 4)
    zeff = eq(r"Z_{\mathrm{eff}}", 80, cfg.ZEFF_COLOR).move_to([3.6, 0.9, 0])
    meaning = txt('charge after shielding', cfg.FONT["small"], cfg.WHITE).next_to(zeff, DOWN, buff=0.25)
    scene.play(Write(zeff), run_time=1.0)
    scene.play(FadeIn(meaning, shift=UP * 0.1), Indicate(felt, color=cfg.WHITE), run_time=1.0)

    # --- 6. Two effects compete ---------------------------------------------------------------------
    beat(scene, t, 5)
    head = swap_heading(scene, head, "Two effects compete")
    sodium = VGroup(nucleus, electron, pull, core, outer, pushes)
    for cloud in (core, outer):
        cloud.clear_updaters()
    scene.play(FadeOut(sodium), FadeOut(VGroup(full, felt, full_tag, felt_tag, zeff, meaning)), run_time=0.9)

    left = Atom(radius_of("Li"), LEFT_AT, charge="+3", core=core_of("Li"), count=320, seed=41, nucleus_radius=0.3)
    right = Atom(radius_of("Li"), RIGHT_AT, charge="+3", core=core_of("Li"), count=320, seed=42, nucleus_radius=0.3)
    divider = DashedLine([0, 2.9, 0], [0, -3.9, 0], stroke_color=cfg.MUTED, stroke_width=2, stroke_opacity=0.5)
    left_name = txt("same shell, more protons", cfg.FONT["small"], cfg.GOLD).move_to([-3.7, -3.85, 0])
    right_name = txt("a new shell", cfg.FONT["small"], cfg.CYAN).move_to([3.7, -3.85, 0])
    left_bar, right_bar = zeff_bar("Li", -3.7), zeff_bar("Li", 3.7)
    gauge_tags = VGroup(eq(r"Z_{\mathrm{eff}}", cfg.FONT["small"], cfg.ZEFF_COLOR).next_to(left_bar, LEFT, buff=0.25),
                        eq(r"Z_{\mathrm{eff}}", cfg.FONT["small"], cfg.ZEFF_COLOR).next_to(right_bar, LEFT, buff=0.25))
    scene.play(FadeIn(left, scale=0.7), FadeIn(right, scale=0.7), Create(divider), run_time=1.0)

    # --- 7. Same shell: protons win ----------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeIn(left_name, shift=UP * 0.15), GrowFromEdge(left_bar, LEFT), FadeIn(gauge_tags[0]), run_time=0.9)
    tiles = VGroup(*[element_tile(pm.z_of(s), 0.5) for s in ("Li", "Be", "B", "C", "N", "O", "F")])
    tiles.arrange(RIGHT, buff=0.06).move_to([-3.7, 2.95, 0])
    marker = glow_frame(tiles[0], cfg.WHITE, buff=0.05)
    scene.play(FadeIn(tiles), Create(marker), run_time=0.8)
    scene.wait(1.6)
    arrows = pull_arrows(LEFT_AT, radius_of("Li"), pm.slater_zeff(3), count=6)
    scene.play(FadeIn(arrows), run_time=0.6)
    for index, symbol in enumerate(("Be", "B", "C", "N", "O", "F"), start=1):
        if index == 3:
            beat(scene, t, 7)
        z = pm.z_of(symbol)
        new_arrows = pull_arrows(LEFT_AT, radius_of(symbol), pm.slater_zeff(z), count=6)
        scene.play(*left.resize(radius_of(symbol), core_of(symbol)), *relabel_nucleus(left, f"+{z}"),
                   Transform(left_bar, zeff_bar(symbol, -3.7)), Transform(arrows, new_arrows),
                   marker.animate.move_to(tiles[index]), run_time=1.05)
    scene.play(Indicate(left_bar, color=cfg.WHITE), run_time=0.9)

    # --- 8. New shell: distance wins ------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeIn(right_name, shift=UP * 0.15), GrowFromEdge(right_bar, LEFT), FadeIn(gauge_tags[1]), run_time=0.9)
    column = VGroup(*[element_tile(pm.z_of(s), 0.5) for s in ("Li", "Na", "K")]).arrange(RIGHT, buff=0.06)
    column.move_to([3.7, 2.95, 0])
    right_marker = glow_frame(column[0], cfg.WHITE, buff=0.05)
    scene.play(FadeIn(column), Create(right_marker), run_time=0.8)
    for index, symbol in enumerate(("Na", "K"), start=1):
        z = pm.z_of(symbol)
        scene.play(*right.resize(radius_of(symbol), core_of(symbol)), *relabel_nucleus(right, f"+{z}"),
                   Transform(right_bar, zeff_bar(symbol, 3.7)), right_marker.animate.move_to(column[index]),
                   run_time=1.6)

    beat(scene, t, 9)
    distance = chip("distance takes over", cfg.CYAN, cfg.FONT["small"]).move_to([3.7, -2.25, 0])
    scene.play(FadeIn(distance, scale=1.1), run_time=0.7)
    scene.play(Flash(right.center_point(), color=cfg.CORE_COLOR, flash_radius=right.core.radius + 0.2, line_length=0.35, num_lines=16), run_time=1.2)

    # --- 9. The contest -------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(VGroup(left, right, divider, left_name, right_name, left_bar, right_bar, gauge_tags, tiles,
                              marker, column, right_marker, distance, arrows)), run_time=0.9)
    head = swap_heading(scene, head, "Every trend: a contest")
    middle = Atom(1.7, [0, 0.2, 0], charge="+", core=0.6, count=420, seed=43, nucleus_radius=0.3)
    scene.play(FadeIn(middle, scale=0.7), run_time=0.9)
    inward = pull_arrows(middle.center_point(), 1.7, 4.0, count=4, phase=PI / 4)
    outward = VGroup(*[Arrow(middle.center_point() + 1.45 * d, middle.center_point() + 2.45 * d, buff=0,
                             color=cfg.CYAN, stroke_width=8, tip_length=0.26)
                       for d in (RIGHT, UP, LEFT, DOWN)])
    pull_side = chip("charge pulls in", cfg.GOLD, cfg.FONT["label"]).move_to([-4.3, -2.75, 0])
    spread_side = chip('distance + shielding', cfg.CYAN, cfg.FONT["label"])
    fit_width(spread_side, 5.2)
    spread_side.move_to([3.75, -2.75, 0])
    scene.play(LaggedStart(*[GrowArrow(a) for a in inward], lag_ratio=0.1), FadeIn(pull_side), run_time=1.0)
    scene.play(LaggedStart(*[GrowArrow(a) for a in outward], lag_ratio=0.1), FadeIn(spread_side), run_time=1.0)
    scene.play(*middle.resize(1.35), run_time=1.2, rate_func=there_and_back)

    beat(scene, t, 11)
    solve = chip('Now: explain the size', cfg.GOLD, cfg.FONT["body"]).move_to([0, -3.8, 0])
    scene.play(FadeIn(solve, shift=UP * 0.2), run_time=0.8)
    scene.play(Circumscribe(solve, color=cfg.GOLD), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["04"])
