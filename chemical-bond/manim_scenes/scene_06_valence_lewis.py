"""Valence electrons and Lewis dots — and the octet as a pattern, not a cause.

Configurations come from the filling model in ``utils.physics_models``, and
every valence count is ``utils.bond_data.VALENCE_ELECTRONS`` (checked against
the narration). Lewis dots fly from the count to the symbol, placed singly
first and then in pairs, so the drawing visibly *is* the count.
"""

from manim_scenes.common import *

ROW = (("H", {"right": 1}),
       ("C", {"up": 1, "right": 1, "down": 1, "left": 1}),
       ("O", {"up": 2, "right": 1, "down": 1, "left": 2}),
       ("Cl", {"up": 2, "right": 1, "down": 2, "left": 2}))
ROW_X = (-5.1, -1.7, 1.7, 5.1)
ROW_Y = 0.55
FILL_ORDER = ("up", "right", "down", "left")


class Scene06ValenceLewis(Scene):
    def construct(self) -> None:
        play_scene(self)


def placement_order(atom: LewisAtom) -> list[VGroup]:
    """Dots in Lewis order: one on each side first, then the second of each pair."""
    first = [atom.slots[side][0] for side in FILL_ORDER if side in atom.slots]
    second = [atom.slots[side][1] for side in FILL_ORDER if side in atom.slots and len(atom.slots[side]) > 1]
    return first + second


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "06", "Valence electrons")

    # --- 1. Carbon: two inner electrons, four outer ------------------------------------------------------
    carbon = Atom(1.9, [-3.6, 0.0, 0], charge="+6", core=0.55, count=420, core_count=160, seed=61, glow=0.18,
                  nucleus_radius=0.32)
    config = eq(r"1s^{2}\;\,2s^{2}\,2p^{2}", 70, cfg.WHITE).move_to([3.3, 1.0, 0])
    config[0][0:3].set_color(cfg.CORE_COLOR)
    config[0][3:].set_color(cfg.ELECTRON_COLOR)
    scene.play(FadeIn(carbon, scale=0.6), run_time=1.4)
    scene.play(Write(config), run_time=1.2)
    dismiss_opening_title(scene, t, head)
    inner = txt("2 inner", cfg.FONT["label"], cfg.CORE_COLOR).next_to(config[0][0:3], DOWN, buff=0.45)
    outer = txt("4 outer", cfg.FONT["label"], cfg.ELECTRON_COLOR).next_to(config[0][3:], DOWN, buff=0.45)
    scene.play(FadeIn(inner, shift=UP * 0.1), run_time=0.7)
    scene.play(FadeIn(outer, shift=UP * 0.1), run_time=0.7)

    # --- 2. The outer electrons do the chemistry -----------------------------------------------------------
    beat(scene, t, 1)
    valence = chip("valence electrons", cfg.ELECTRON_COLOR, cfg.FONT["body"]).move_to([3.3, -1.4, 0])
    scene.play(*carbon.resize(2.15), FadeIn(valence, shift=UP * 0.15), run_time=1.2)
    scene.play(Indicate(config[0][3:], color=cfg.WHITE, scale_factor=1.12), carbon.cloud.fade_to(1.4), run_time=1.2)
    scene.play(carbon.cloud.fade_to(1.0), run_time=0.8)

    # --- 3. The inner electrons sit deep --------------------------------------------------------------------
    beat(scene, t, 2)
    deep = txt("Tightly held core", cfg.FONT["small"], cfg.CORE_COLOR).next_to(carbon.nucleus, DOWN, buff=1.05)
    deep.add_background_rectangle(color=cfg.BG, opacity=0.75, buff=0.08)
    scene.play(carbon.cloud.fade_to(0.35), FadeIn(deep), run_time=1.0)
    scene.play(Indicate(carbon.core, color=cfg.WHITE, scale_factor=1.0), run_time=1.0)
    scene.play(carbon.cloud.fade_to(1.0), FadeOut(deep), run_time=0.8)

    # --- 4. Four atoms, four counts ---------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(VGroup(config, inner, outer, valence)), FadeOut(carbon, scale=0.6), run_time=0.8)
    tiles = VGroup(*[element_tile(pm.z_of(sym), 1.35, number=True, fill=0.24).move_to([x, ROW_Y, 0])
                     for (sym, _), x in zip(ROW, ROW_X)])
    counts = VGroup(*[txt(str(bd.VALENCE_ELECTRONS[sym]), 84, cfg.ELECTRON_COLOR).move_to([x, -2.0, 0])
                      for (sym, _), x in zip(ROW, ROW_X)])
    for tile, number in zip(tiles, counts):
        scene.play(FadeIn(tile, shift=DOWN * 0.15), FadeIn(number, shift=UP * 0.2), run_time=1.1)
    caption_valence = txt("valence electrons", cfg.FONT["label"], cfg.MUTED).move_to([0, -3.35, 0])
    scene.play(FadeIn(caption_valence), run_time=0.6)

    # --- 5. Lewis: the symbol, with its valence electrons as dots ------------------------------------------------
    beat(scene, t, 4)
    atoms = [LewisAtom(sym, layout, size=96, center=[x, ROW_Y, 0], reach=0.24) for (sym, layout), x in zip(ROW, ROW_X)]
    symbols = VGroup(*[a.symbol for a in atoms])
    scene.play(*[FadeThrough(tile, sym) for tile, sym in zip(tiles, symbols)], run_time=1.2)
    lewis = txt("Lewis symbols", cfg.FONT["body"], cfg.GOLD).move_to([0, 3.1, 0])
    scene.play(FadeIn(lewis, shift=DOWN * 0.15), run_time=0.8)

    # --- 6. Dots fly from the count to the symbol ----------------------------------------------------------------------
    beat(scene, t, 5)
    for atom, number in zip(atoms, counts):
        order = placement_order(atom)
        flights = []
        for k, dot in enumerate(order):
            target = dot.get_center()
            dot.move_to(number.get_center())
            flights.append(dot.animate.move_to(target))
        scene.add(*order)
        scene.play(LaggedStart(*flights, lag_ratio=0.18), number.animate.set_opacity(0.35), run_time=1.6)
    singly = txt("singly first, then in pairs", cfg.FONT["small"], cfg.MUTED).move_to([0, 2.3, 0])
    scene.play(FadeIn(singly), run_time=0.6)

    # --- 7. Noble gases: eight, and barely reacting ---------------------------------------------------------------------
    beat(scene, t, 6)
    everything = VGroup(*atoms, counts, caption_valence, singly, lewis)
    scene.play(FadeOut(everything, shift=UP * 0.2), run_time=0.8)
    full = {"up": 2, "right": 2, "down": 2, "left": 2}
    neon = LewisAtom("Ne", full, size=110, center=[-2.6, 0.5, 0], reach=0.28)
    argon = LewisAtom("Ar", full, size=110, center=[2.6, 0.5, 0], reach=0.28)
    scene.play(FadeIn(neon, scale=0.8), FadeIn(argon, scale=0.8), run_time=1.0)
    eights = VGroup(txt("8", 72, cfg.ELECTRON_COLOR).next_to(neon, DOWN, buff=0.45),
                    txt("8", 72, cfg.ELECTRON_COLOR).next_to(argon, DOWN, buff=0.45))
    quiet = chip("barely react", cfg.MUTED, cfg.FONT["label"]).move_to([0, -2.85, 0])
    scene.play(FadeIn(eights, shift=UP * 0.15), run_time=0.7)
    scene.play(FadeIn(quiet, shift=UP * 0.1), run_time=0.7)
    scene.play(Indicate(eights, color=cfg.WHITE, scale_factor=1.15), run_time=1.0)

    # --- 8. In compounds, eight again: the octet rule ---------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(neon, argon, eights, quiet)), run_time=0.7)
    oxygen = txt("O", 110, cfg.WHITE).move_to([0, 0.35, 0])
    hydrogens = VGroup(txt("H", 96, cfg.WHITE).move_to([-2.5, 0.35, 0]), txt("H", 96, cfg.WHITE).move_to([2.5, 0.35, 0]))
    shared = VGroup(*[e_dot(p) for p in (np.array([-1.25, 0.35 + LEWIS_GAP, 0]), np.array([-1.25, 0.35 - LEWIS_GAP, 0]),
                                          np.array([1.25, 0.35 + LEWIS_GAP, 0]), np.array([1.25, 0.35 - LEWIS_GAP, 0]))])
    lone = VGroup(*[e_dot(p) for p in (np.array([-LEWIS_GAP, 1.32, 0]), np.array([LEWIS_GAP, 1.32, 0]),
                                        np.array([-LEWIS_GAP, -0.62, 0]), np.array([LEWIS_GAP, -0.62, 0]))])
    water = eq(r"\mathrm{H_2O}", cfg.FONT["body"], cfg.MUTED).move_to([0, 2.7, 0])
    scene.play(FadeIn(oxygen), FadeIn(hydrogens), FadeIn(water), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in (*shared, *lone)], lag_ratio=0.1), run_time=1.2)
    ring = octet_ring(oxygen, 1.45, cfg.GREEN)
    eight = txt("8", 72, cfg.GREEN).move_to(ring.get_corner(UR) + np.array([0.25, 0.15, 0]))
    scene.play(Create(ring), FadeIn(eight, scale=0.6), run_time=1.0)
    octet = chip("the octet rule", cfg.GOLD, cfg.FONT["body"]).move_to([0, -2.6, 0])
    scene.play(FadeIn(octet, shift=UP * 0.15), run_time=0.8)

    # --- 9. A powerful bookkeeping tool -------------------------------------------------------------------------------------
    beat(scene, t, 8)
    tick = check_mark(0.38).next_to(octet, RIGHT, buff=0.4)
    tool = txt("Electron bookkeeping", cfg.FONT["label"], cfg.GREEN).next_to(octet, DOWN, buff=0.3)
    scene.play(Create(tick), FadeIn(tool, shift=UP * 0.1), run_time=0.9)
    scene.play(Indicate(shared, color=cfg.WHITE, scale_factor=1.3), run_time=1.0)
    scene.play(Indicate(lone, color=cfg.WHITE, scale_factor=1.3), run_time=1.0)

    # --- 10. But not the reason atoms bond --------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(VGroup(tool, tick)), VGroup(oxygen, hydrogens, shared, lone, ring, eight, water).animate.shift(UP * 0.35),
               octet.animate.move_to([0, -1.6, 0]), run_time=0.8)
    want = txt("atoms want eight electrons", cfg.FONT["body"], cfg.MUTED).move_to([0, -2.75, 0])
    scene.play(FadeIn(want, shift=UP * 0.1), run_time=0.8)
    no = strike(want, cfg.REPEL, 8)
    scene.play(Create(no), run_time=0.6)
    scene.play(Wiggle(want, scale_value=1.04), run_time=0.9)

    # --- 11. The cause is still energy ---------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    pattern = txt("A useful pattern", cfg.FONT["label"], cfg.GOLD).move_to([-3.9, -2.75, 0])
    cause = VGroup(txt("Why bond?", cfg.FONT["label"], cfg.WHITE), txt("energy", cfg.FONT["label"], cfg.ENERGY)).arrange(RIGHT, buff=0.2)
    cause.move_to([4.0, -2.75, 0])
    scene.play(*fade_labels(VGroup(want, no), pattern), run_time=0.8)
    scene.play(FadeIn(cause, shift=UP * 0.1), run_time=0.8)
    icon_axes = Axes(x_range=[0, 320, 100], y_range=[-500, 400, 200], x_length=2.6, y_length=1.5, tips=False,
                     axis_config={"stroke_color": cfg.MUTED, "stroke_width": 2, "include_ticks": False})
    icon_curve = icon_axes.plot(lambda r: float(bm.morse(r, *H2)), x_range=[bm.morse_inverse(380, *H2), 320, 1],
                                color=cfg.ENERGY, stroke_width=5, use_smoothing=False)
    icon = VGroup(icon_axes, icon_curve).next_to(cause, UP, buff=0.3)
    scene.play(Create(icon_curve), FadeIn(icon_axes), run_time=1.2)
    because = Arrow(cause.get_left() + LEFT * 0.15, pattern.get_right() + RIGHT * 0.15, buff=0, color=cfg.ENERGY,
                    stroke_width=6, max_tip_length_to_length_ratio=0.12)
    scene.play(GrowArrow(because), run_time=1.0)
    scene.play(Indicate(cause[1], color=cfg.WHITE, scale_factor=1.1), run_time=1.0)
    scene.play(Circumscribe(icon, color=cfg.ENERGY, fade_out=True), run_time=1.6)
    scene.play(FadeOut(VGroup(oxygen, hydrogens, shared, lone, ring, eight, water, octet, pattern, cause, icon, because)),
               run_time=0.8)
    h_left = LewisAtom("H", {"right": 1}, size=110, center=[-4.2, 0.4, 0], reach=0.26)
    h_right = LewisAtom("H", {"left": 1}, size=110, center=[4.2, 0.4, 0], reach=0.26)
    scene.play(FadeIn(h_left, shift=RIGHT * 0.3), FadeIn(h_right, shift=LEFT * 0.3), run_time=0.8)
    scene.play(h_left.animate.move_to([-1.3, 0.4, 0]), h_right.animate.move_to([1.3, 0.4, 0]), run_time=2.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["06"])
