"""The periodic table becomes a map of invisible forces (3D).

Four tabs turn the main-group elements into a heat-map skyline: tower height
and colour both show where a value sits on its own property's range
(``heat_fraction``), so switching tabs changes the data, never the meaning of
a colour. Radius uses one definition (covalent); noble gases have no
comparable radius or electronegativity and stay flat and dim. Electron gain
towers show energy released; tiles that need energy instead are flat orange.
Then the opening paradox is resolved with the same atoms the film began with.
"""

from manim_scenes.common import *

PITCH = 0.62
CENTER = DOWN * 0.35
PROPS = ("radius", "ionization", "electronegativity", "electron_gain")
TAB_NAMES = {"radius": "Radius", "ionization": "Ionization", "electronegativity": "Electronegativity",
             "electron_gain": "Electron gain"}
TOWER = 2.5
TILT = 56 * DEGREES
DROP = IN * 1.05        # the skyline stands below the origin, so tilting keeps it clear of the tabs
ZOOM = 0.88
SCALE = 0.0075
LEFT_AT = np.array([-3.7, 0.35, 0])
RIGHT_AT = np.array([3.7, 0.35, 0])


class Scene18HeatMaps(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def tower(prop: str | None, z: int) -> Prism:
    """One element's prism for a tab (``prop=None``: the flat starting slab)."""
    point = table_point(z, pitch=PITCH, center=CENTER) + DROP
    if prop is None:
        return tile_prism(point, PITCH * 0.86, 0.04, block_color(z), opacity=0.9)
    fraction = heat_fraction(prop, z)
    if ed.is_exception(prop, pm.symbol_of(z)):
        return tile_prism(point, PITCH * 0.86, 0.06, cfg.REQUIRED, opacity=0.95)
    if fraction is None:
        return tile_prism(point, PITCH * 0.86, 0.04, cfg.NO_DATA, opacity=0.9)
    return tile_prism(point, PITCH * 0.86, 0.12 + TOWER * fraction, heat_color(prop, z), opacity=0.95)


def tab_bar(active: str) -> VGroup:
    tabs = VGroup()
    for prop in PROPS:
        on = prop == active
        colour = cfg.GOLD if on else cfg.MUTED
        label = txt(TAB_NAMES[prop], cfg.FONT["small"], cfg.BG if on else cfg.MUTED)
        pill = RoundedRectangle(width=label.width + 0.55, height=label.height + 0.34, corner_radius=0.2,
                                stroke_color=colour, stroke_width=3, fill_color=colour if on else cfg.PANEL,
                                fill_opacity=0.95 if on else 0.8)
        tabs.add(VGroup(pill, label.move_to(pill)))
    tabs.arrange(RIGHT, buff=0.25).move_to([0, 3.72, 0])
    fit_width(tabs, 13.6)
    return tabs


def mini_map(prop: str, center) -> VGroup:
    """A small 2D heat map of the main-group block (8 columns, periods 1-6)."""
    pitch = 0.36
    group = VGroup()
    for z in main_group_zs():
        row, col = pm.position(z)
        index = ed.MAIN_GROUP_COLUMNS.index(col)
        tile = Square(pitch * 0.88, stroke_width=0, fill_color=heat_color(prop, z), fill_opacity=0.95)
        tile.move_to(np.asarray(center) + np.array([(index - 3.5) * pitch, (3.5 - row) * pitch, 0]))
        group.add(tile)
    title = txt(TAB_NAMES[prop] if prop != "radius" else "Atomic radius", cfg.FONT["small"], cfg.WHITE)
    title.next_to(group, UP, buff=0.18)
    result = VGroup(group, title)
    result.tiles, result.title = group, title
    return result


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "18", "The full table")
    table = periodic_table(pitch=PITCH, center=CENTER)
    table.tiles[2].box.set_stroke(cfg.BLUE)
    scene.play(FadeIn(table, scale=0.97), run_time=1.4)

    # --- 1. Tab 1: atomic radius, as towers -------------------------------------------------------------
    beat(scene, t, 1)
    main = main_group_zs()
    slabs = {z: tower(None, z) for z in main}
    flats = VGroup()
    for z in range(1, 119):
        if z in slabs:
            continue
        square = Square(PITCH * 0.86, stroke_color=cfg.MUTED, stroke_width=1, stroke_opacity=0.4,
                        fill_color=cfg.PANEL, fill_opacity=0.85).move_to(table_point(z, pitch=PITCH, center=CENTER) + DROP)
        square.shade_in_3d = True
        flats.add(square)
    towers = VGroup(*[slabs[z] for z in main])
    tabs = tab_bar("radius")
    hud(scene, tabs)
    scene.play(*fade_labels(head, tabs), FadeOut(table), FadeIn(towers), FadeIn(flats), run_time=1.0)
    scene.remove(head)
    move_camera(scene, phi=TILT, theta=-PI / 2, zoom=ZOOM, run_time=3.0,
                added_anims=[Transform(slabs[z], tower("radius", z)) for z in main])
    one_scale = caption("Covalent radius · pm", cfg.MUTED, cfg.FONT["tiny"], y=-4.05)
    hud(scene, one_scale)
    scene.play(FadeIn(one_scale), run_time=0.6)

    # --- 2. Radius: down and to the left ------------------------------------------------------------------
    beat(scene, t, 2)
    note = caption('Radius: generally grows ↓ ←', cfg.CYAN, cfg.FONT["small"], y=-3.35)
    hud(scene, note)
    scene.play(FadeIn(note), run_time=0.7)
    scene.play(Indicate(slabs[55], color=cfg.WHITE, scale_factor=1.0), Indicate(slabs[56], color=cfg.WHITE, scale_factor=1.0),
               run_time=1.2)
    move_camera(scene, phi=TILT, theta=-78 * DEGREES, zoom=ZOOM, run_time=3.0)

    def switch(prop: str, old_tabs: VGroup, old_note: VGroup, text: str, colour: str) -> tuple[VGroup, VGroup]:
        nonlocal one_scale
        units = {"ionization": "First ionization · kJ/mol",
                 "electronegativity": "Pauling scale · no units",
                 "electron_gain": "Energy released · kJ/mol"}
        context = caption(units[prop], cfg.MUTED, cfg.FONT["tiny"], y=-4.05)
        hud(scene, context)
        new_tabs = tab_bar(prop)
        new_note = caption(text, colour, cfg.FONT["small"], y=-3.35)
        hud(scene, new_tabs, new_note)
        scene.play(*fade_labels(old_tabs, new_tabs), *fade_labels(one_scale, context), FadeOut(old_note), run_time=0.5)
        one_scale = context
        scene.play(*[Transform(slabs[z], tower(prop, z)) for z in main], run_time=2.4)
        scene.play(FadeIn(new_note), run_time=0.6)
        return new_tabs, new_note

    # --- 3-4. Tab 2: ionization enthalpy ------------------------------------------------------------------------
    beat(scene, t, 3)
    tabs, note = switch("ionization", tabs, note, 'Ionization: generally rises ↑ →', cfg.GOLD)
    beat(scene, t, 4)
    move_camera(scene, phi=TILT, theta=-100 * DEGREES, zoom=ZOOM, run_time=3.0)
    scene.play(Indicate(slabs[2], color=cfg.WHITE, scale_factor=1.0), run_time=1.0)

    # --- 5. Tab 3: electronegativity ----------------------------------------------------------------------------
    beat(scene, t, 5)
    tabs, note = switch("electronegativity", tabs, note, 'Electronegativity: generally rises ↑ →', cfg.GOLD)

    # --- 6-7. Tab 4: electron gain, with its exceptions ------------------------------------------------------------
    beat(scene, t, 6)
    tabs, note = switch("electron_gain", tabs, note, 'Electron gain: energy released', cfg.GREEN)
    beat(scene, t, 7)
    exceptions = [z for z in main if ed.is_exception("electron_gain", pm.symbol_of(z))]
    orange = caption('Orange: energy required', cfg.REQUIRED, cfg.FONT["tiny"], y=-4.05)
    hud(scene, orange)
    scene.play(*fade_labels(one_scale, orange), run_time=0.6)
    scene.play(*[Indicate(slabs[z], color=cfg.WHITE, scale_factor=1.0) for z in exceptions], run_time=1.4)
    scene.play(Indicate(slabs[17], color=cfg.WHITE, scale_factor=1.0), run_time=1.0)

    # --- 8. Four maps, side by side ------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(towers), FadeOut(flats), FadeOut(VGroup(tabs, note, orange)), run_time=0.8)
    move_camera(scene, phi=0, theta=-PI / 2, zoom=1.0, run_time=1.2)
    head = heading("Four maps, four broad patterns")
    hud(scene, head)
    spots = ((-3.7, 1.35), (3.7, 1.35), (-3.7, -2.5), (3.7, -2.5))
    maps = [mini_map(prop, [x, y, 0]) for prop, (x, y) in zip(PROPS, spots)]
    scene.play(FadeIn(head, shift=DOWN * 0.15), LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in maps], lag_ratio=0.2),
               run_time=1.6)

    # --- 9. The arrows, earned ------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    arrows = VGroup()
    for prop, m in zip(PROPS, maps):
        box = m.tiles
        if prop == "radius":
            start_pt, end_pt = box.get_corner(UR) + DL * 0.25, box.get_corner(DL) + UR * 0.25
        else:
            start_pt, end_pt = box.get_corner(DL) + UR * 0.25, box.get_corner(UR) + DL * 0.25
        arrows.add(glow_arrow(start_pt, end_pt, cfg.TREND_ARROW, 6, tip=0.26))
    scene.play(LaggedStart(*[AnimationGroup(GrowArrow(a.arrow), FadeIn(a[0])) for a in arrows], lag_ratio=0.35), run_time=2.4)
    tendencies = caption("tendencies with reasons, not laws", cfg.GOLD, cfg.FONT["small"], y=-0.3)
    scene.play(FadeIn(tendencies), run_time=0.7)

    # --- 10-12. The opening mystery, solved --------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(VGroup(*maps, arrows, tendencies)), run_time=0.8)
    head = swap_heading(scene, head, "Back to the opening mystery")
    left = Atom(ed.ATOMIC_RADII_PM["Li"] * SCALE, LEFT_AT, charge="+3", core=0.32, count=360, seed=181)
    right = Atom(ed.ATOMIC_RADII_PM["Li"] * SCALE, RIGHT_AT, charge="+3", core=0.32, count=360, seed=182)
    scene.play(FadeIn(left, scale=0.6), FadeIn(right, scale=0.6), run_time=0.8)

    beat(scene, t, 11)
    across = chip('Same shell · stronger attraction', cfg.GOLD, cfg.FONT["tiny"]).move_to([-3.7, -2.75, 0])
    arrows_l = pull_arrows(LEFT_AT, left.radius, pm.slater_zeff(3), count=6)
    scene.play(FadeIn(across, shift=UP * 0.1), FadeIn(arrows_l), run_time=0.8)
    for symbol in ("Be", "B", "C", "N", "O", "F"):
        z = pm.z_of(symbol)
        r = ed.ATOMIC_RADII_PM[symbol] * SCALE
        scene.play(*left.resize(r, 0.32 * (r / left.radius) ** 0.3), *relabel_nucleus(left, f"+{z}"),
                   Transform(arrows_l, pull_arrows(LEFT_AT, r, pm.slater_zeff(z), count=6)), run_time=1.05)

    beat(scene, t, 12)
    down = chip('New shells · farther out', cfg.CYAN, cfg.FONT["tiny"]).move_to([3.7, -2.75, 0])
    scene.play(FadeIn(down, shift=UP * 0.1), run_time=0.7)
    for symbol in ("Na", "K", "Rb", "Cs"):
        z = pm.z_of(symbol)
        r = ed.ATOMIC_RADII_PM[symbol] * SCALE
        n = pm.outer_shell(z)
        scene.play(*right.resize(r, r * (0.25 + 0.07 * (n - 2))), *relabel_nucleus(right, f"+{z}"), run_time=1.45)

    # --- 13. One sentence ----------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    rule = VGroup(txt("tighter pull → smaller", cfg.FONT["body"], cfg.GOLD),
                  txt("new shell → larger", cfg.FONT["body"], cfg.CYAN)).arrange(RIGHT, buff=1.3).move_to([0, -3.6, 0])
    fit_width(rule, 13.4)
    scene.play(FadeIn(rule, shift=UP * 0.15), run_time=0.9)
    scene.play(Indicate(rule, color=cfg.WHITE, scale_factor=1.03), run_time=1.2)

    # --- 14. The same competition, everywhere ----------------------------------------------------------------------------------
    beat(scene, t, 14)
    chain = VGroup(*[chip(word, colour, cfg.FONT["small"]) for word, colour in (
        ("ionization", cfg.GOLD), ("electron gain", cfg.GREEN), ("electronegativity", cfg.CYAN), ("reactivity", cfg.ORANGE))])
    chain.arrange(RIGHT, buff=0.35).move_to([0, 2.85, 0])
    fit_width(chain, 13.6)
    scene.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in chain], lag_ratio=0.3), run_time=1.6)

    # --- 15. Arrows become explanations ----------------------------------------------------------------------------------------
    beat(scene, t, 15)
    scene.play(FadeOut(VGroup(left, right, arrows_l, across, down, rule, chain)), run_time=0.9)
    head = swap_heading(scene, head, "Not a collection of arrows")
    icons = VGroup(*[glow_arrow(ORIGIN, d * 1.1, colour, 6) for d, colour in ((DL, cfg.CYAN), (UR, cfg.GOLD),
                                                                               (UR, cfg.CYAN), (UR, cfg.GREEN))])
    icons.arrange(RIGHT, buff=1.0).move_to([0, 0.3, 0])
    scene.play(LaggedStart(*[GrowArrow(i.arrow) for i in icons], lag_ratio=0.2), *[FadeIn(i[0]) for i in icons], run_time=1.2)

    # --- 16. Three questions ------------------------------------------------------------------------------------------------------
    beat(scene, t, 16)
    questions = VGroup(
        chip('Distance', cfg.CYAN, cfg.FONT["body"]),
        chip('Nuclear attraction', cfg.GOLD, cfg.FONT["body"]),
        chip('Electron arrangement', cfg.GREEN, cfg.FONT["body"]),
    ).arrange(DOWN, buff=0.38).move_to([0, -0.1, 0])
    fit_width(questions, 12.6)
    scene.play(FadeOut(icons, scale=0.6), run_time=0.6)
    for question in questions:
        scene.play(FadeIn(question, shift=RIGHT * 0.25), run_time=0.8)
        scene.wait(1.3)

    # --- 17. A map of invisible forces ---------------------------------------------------------------------------------------------
    beat(scene, t, 17)
    scene.play(FadeOut(questions), FadeOut(head), run_time=0.7)
    final = {z: tower(None, z) for z in main}
    final_towers = VGroup(*final.values())
    final_flats = flats.copy()
    scene.play(FadeIn(final_towers), FadeIn(final_flats), run_time=0.7)
    card = title_card("INVISIBLE FORCES", "the periodic table: a map of", small_first=True)
    card.scale(0.62).move_to([0, 3.4, 0])
    hud(scene, card)
    move_camera(scene, phi=TILT, theta=-80 * DEGREES, zoom=ZOOM, run_time=3.0,
                added_anims=[Transform(final[z], tower("ionization", z)) for z in main])
    scene.play(FadeIn(card, shift=DOWN * 0.15), run_time=1.2)
    scene.begin_ambient_camera_rotation(rate=-0.05)
    cue(scene, t, cfg.SCENE_DURATIONS["18"] - 2.0)
    scene.stop_ambient_camera_rotation()
    end_scene(scene, t, cfg.SCENE_DURATIONS["18"])
