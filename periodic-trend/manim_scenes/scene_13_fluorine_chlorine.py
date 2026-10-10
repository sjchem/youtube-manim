"""Fluorine versus chlorine: the electron gain surprise.

The bars are the NCERT electron gain enthalpies. The explanation is a
schematic balance under each atom: a gold bar for the nucleus's pull on the
newcomer, a red bar for the push of the electrons already there, and a green
bar for what is left. Only the green bars carry data (their ratio is the
measured 328 : 349); the gold and red lengths are illustrative.
"""

from manim_scenes.common import *

F_AT = np.array([-3.7, 0.65, 0])
CL_AT = np.array([3.7, 0.65, 0])
BAR_BASE = -2.9
BAR_SCALE = 4.6 / 360


class Scene13FluorineChlorine(Scene):
    def construct(self) -> None:
        play_scene(self)


def gain_bar(symbol: str, x: float) -> VGroup:
    value = ed.ELECTRON_GAIN_KJ[symbol]
    height = -value * BAR_SCALE
    colour = cfg.RELEASED
    bar = Rectangle(width=1.2, height=height, stroke_width=2, stroke_color=colour, fill_color=colour, fill_opacity=0.5)
    bar.move_to([x, BAR_BASE + height / 2, 0])
    amount = txt(signed(value), cfg.FONT["section"], cfg.WHITE).next_to(bar, UP, buff=0.15)
    name = txt(pm.NAMES[symbol], cfg.FONT["small"], block_color(pm.z_of(symbol))).next_to(bar, DOWN, buff=0.18)
    group = VGroup(bar, amount, name)
    group.bar, group.amount, group.name = bar, amount, name
    return group


def subshell_beads(center, radius: float, count: int = 5, phase: float = 0.4) -> VGroup:
    """Count the five p electrons schematically; bead positions are not orbits."""
    return VGroup(*[glow_dot(np.asarray(center) + p, 0.11) for p in mu.ring_points(count, radius, phase)])


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "13", "Fluorine or chlorine?")

    small_scale = 0.0125
    fluorine = Atom(ed.ATOMIC_RADII_PM["F"] * small_scale, [-4.6, 0.6, 0], charge="+9", core=0.2, count=380, seed=131)
    chlorine = Atom(ed.ATOMIC_RADII_PM["Cl"] * small_scale, [-1.4, 0.6, 0], charge="+17", core=0.45, count=380, seed=132)
    names = VGroup(txt("F", cfg.FONT["section"], cfg.GREEN).move_to([-4.6, -1.5, 0]),
                   txt("Cl", cfg.FONT["section"], cfg.GREEN).move_to([-1.4, -1.5, 0]))
    scene.play(FadeIn(fluorine, scale=0.6), FadeIn(chlorine, scale=0.6), FadeIn(names), run_time=1.2)
    which = chip("which releases more energy?", cfg.GOLD, cfg.FONT["label"]).move_to([-3.0, 2.85, 0])
    scene.play(FadeIn(which, shift=DOWN * 0.15), run_time=0.8)

    # --- 1. The guess: fluorine ------------------------------------------------------------------
    head = dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    pull = pull_arrows(fluorine.center_point(), fluorine.radius, pm.slater_zeff(9), count=6)
    guess = chip("guess: fluorine (smaller)", cfg.MUTED, cfg.FONT["small"]).move_to([-3.0, -2.55, 0])
    scene.play(LaggedStart(*[GrowArrow(a) for a in pull], lag_ratio=0.1), FadeIn(guess, shift=UP * 0.15), run_time=1.2)

    # --- 2. Fluorine: -328 ----------------------------------------------------------------------------
    beat(scene, t, 2)
    f_bar = gain_bar("F", 2.6)
    scene.play(GrowFromEdge(f_bar.bar, DOWN), FadeIn(f_bar.name), run_time=1.0)
    unit = txt("kJ/mol", cfg.FONT["small"], cfg.MUTED).move_to([3.9, -3.95, 0])
    scene.play(FadeIn(f_bar.amount, shift=UP * 0.1), FadeIn(unit), run_time=0.6)

    # --- 3. Chlorine: -349, more! ------------------------------------------------------------------------
    beat(scene, t, 3)
    cl_bar = gain_bar("Cl", 5.2)
    scene.play(GrowFromEdge(cl_bar.bar, DOWN), FadeIn(cl_bar.name), run_time=1.0)
    scene.play(FadeIn(cl_bar.amount, shift=UP * 0.1), run_time=0.6)
    wrong = cross_mark(0.28).next_to(guess, RIGHT, buff=0.25)
    more = chip("chlorine releases more", cfg.GREEN, cfg.FONT["small"]).move_to([3.9, 2.85, 0])
    scene.play(Create(wrong), FadeIn(more, scale=1.15), Flash(cl_bar.bar.get_top(), color=cfg.GREEN), run_time=1.0)

    # --- 4. Zoom in: fluorine's crowded outer shell -----------------------------------------------------------
    beat(scene, t, 4)
    head = swap_heading(scene, head, "Zoom in: the outer shell")
    scene.play(FadeOut(VGroup(fluorine, chlorine, names, which, pull, guess, wrong, more, f_bar, cl_bar, unit)), run_time=0.8)
    big_f = Atom(1.15, F_AT, charge="+9", core=0.3, count=240, seed=133, glow=0.14)
    big_cl = Atom(1.8, CL_AT, charge="+17", core=0.7, count=240, seed=134, glow=0.12)
    f_ring = subshell_beads(F_AT, 0.85)
    cl_ring = subshell_beads(CL_AT, 1.45)
    f_name = VGroup(txt("fluorine", cfg.FONT["label"], cfg.GREEN), eq(r"2p", cfg.FONT["label"], cfg.GREEN)).arrange(RIGHT, buff=0.3)
    f_name.move_to([F_AT[0], -1.95, 0])
    scene.play(FadeIn(big_f, scale=0.6), FadeIn(f_name), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in f_ring], lag_ratio=0.12), run_time=1.2)
    five = txt('2p: five electrons', cfg.FONT["small"], cfg.WHITE).move_to([F_AT[0], 2.75, 0])
    scene.play(FadeIn(five, shift=DOWN * 0.1), run_time=0.7)

    # --- 5. The newcomer is pushed back --------------------------------------------------------------------------
    beat(scene, t, 5)
    f_new = glow_dot(F_AT + np.array([2.6, 1.5, 0]), 0.14, cfg.WHITE)
    scene.play(FadeIn(f_new, scale=0.4), run_time=0.4)
    f_spot = F_AT + np.array([1.05, 0.45, 0])
    scene.play(f_new.animate.move_to(f_spot), run_time=1.0, rate_func=rush_from)
    pushes = VGroup(*[Arrow(d.get_center(), d.get_center() + (f_spot - d.get_center()) * 0.62, buff=0.12, color=cfg.RED,
                            stroke_width=5, tip_length=0.16, max_tip_length_to_length_ratio=0.45)
                      for d in f_ring if np.linalg.norm(d.get_center() - f_spot) < 1.6])
    scene.play(LaggedStart(*[GrowArrow(p) for p in pushes], lag_ratio=0.1), run_time=0.9)
    scene.play(f_new.animate(rate_func=there_and_back).shift(RIGHT * 0.35 + UP * 0.15), run_time=0.8)
    scene.play(f_new.animate(rate_func=there_and_back).shift(RIGHT * 0.3 + UP * 0.1), run_time=0.7)
    crowded = chip("strong repulsion", cfg.RED, cfg.FONT["small"]).move_to([F_AT[0], -2.85, 0])
    scene.play(FadeIn(crowded, shift=UP * 0.1), run_time=0.6)

    # --- 6. Chlorine: more room ---------------------------------------------------------------------------------------
    beat(scene, t, 6)
    cl_name = VGroup(txt("chlorine", cfg.FONT["label"], cfg.GREEN), eq(r"3p", cfg.FONT["label"], cfg.GREEN)).arrange(RIGHT, buff=0.3)
    cl_name.move_to([CL_AT[0], -1.95, 0])
    scene.play(FadeIn(big_cl, scale=0.6), FadeIn(cl_name), FadeOut(five), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in cl_ring], lag_ratio=0.12), run_time=1.0)
    cl_new = glow_dot(CL_AT + np.array([-3.0, 1.9, 0]), 0.14, cfg.WHITE)
    cl_spot = CL_AT + np.array([-1.65, 0.5, 0])
    scene.play(FadeIn(cl_new, scale=0.4), run_time=0.3)
    scene.play(cl_new.animate.move_to(cl_spot), run_time=1.0, rate_func=rush_from)
    room = chip('More room · less repulsion', cfg.GREEN, cfg.FONT["small"]).move_to([CL_AT[0], -2.85, 0])
    scene.play(FadeIn(room, shift=UP * 0.1), run_time=0.6)

    # --- 7. Pull minus crowding: the net welcome -----------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(pushes), FadeOut(crowded), FadeOut(room), FadeOut(f_name), FadeOut(cl_name), run_time=0.5)
    net_f, net_cl = -ed.ELECTRON_GAIN_KJ["F"], -ed.ELECTRON_GAIN_KJ["Cl"]
    per_kj = 2.4 / net_cl
    balances = []
    for centre, pull_len, net in ((F_AT, 3.6, net_f), (CL_AT, 3.0, net_cl)):
        left = centre[0] - 1.15
        rows = VGroup()
        for y, length, colour, offset in ((-2.0, pull_len, cfg.PULL_COLOR, 0.0),
                                         (-2.6, pull_len - net * per_kj, cfg.RED, net * per_kj),
                                         (-3.2, net * per_kj, cfg.GREEN, 0.0)):
            rows.add(Rectangle(width=length, height=0.38, stroke_width=0, fill_color=colour, fill_opacity=0.9)
                     .move_to([left + offset + length / 2, y, 0]))
        balances.append(rows)
    labels = VGroup(txt("pull", cfg.FONT["tiny"], cfg.PULL_COLOR), txt("crowding", cfg.FONT["tiny"], cfg.RED),
                    txt("net welcome", cfg.FONT["tiny"], cfg.GREEN)).arrange(DOWN, buff=0.26, aligned_edge=RIGHT)
    labels.move_to([-5.95, -2.6, 0])
    scene.play(FadeIn(labels), *[GrowFromEdge(b[0], LEFT) for b in balances], run_time=0.8)
    scene.play(*[GrowFromEdge(b[1], RIGHT) for b in balances], run_time=0.8)
    scene.play(*[GrowFromEdge(b[2], LEFT) for b in balances], run_time=0.8)
    note = txt('Illustrative balance · measured net', cfg.FONT["tiny"], cfg.MUTED).move_to([0, -3.95, 0])
    scene.play(FadeIn(note), run_time=0.5)
    tug_rows = balances + [labels, note]

    # --- 8. The record holder ---------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    record = chip('Cl: greatest energy release', cfg.GREEN, cfg.FONT["small"]).move_to([0, 2.95, 0])
    fit_width(record, 13.0)
    scene.play(FadeIn(record, shift=DOWN * 0.15), run_time=0.9)
    scene.play(Flash(CL_AT, color=cfg.GREEN, flash_radius=2.3, num_lines=16), run_time=1.2)

    # --- 9. Another way to attract electrons ----------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(VGroup(*tug_rows, f_new, cl_new, f_ring, cl_ring, record)), run_time=0.8)
    head = swap_heading(scene, head, "Another way to attract electrons")
    scene.play(Glide(big_f, [-1.35, 0.3, 0]), Glide(big_cl, [1.35, 0.3, 0]), run_time=1.8)
    share = chip("sharing, inside a bond", cfg.CYAN, cfg.FONT["label"]).move_to([0, -2.9, 0])
    scene.play(FadeIn(share, shift=UP * 0.15), run_time=0.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["13"])
