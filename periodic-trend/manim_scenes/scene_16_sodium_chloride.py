"""Sodium gives, chlorine takes — and why the crystal, not the transfer, pays.

The electron transfer is drawn as a simplified model. The energy ledger is
honest about it: removing sodium's electron (+496 kJ/mol) costs more than
chlorine releases on taking it (−349 kJ/mol), so isolated gas-phase transfer
is uphill (+147). The rock-salt crystal is hand-projected 3D (each Na+ has six
Cl− neighbours and vice versa); ion sizes are shrunk so the arrangement shows.
"""

from manim_scenes.common import *

SCALE = 0.0105
NA_AT = np.array([-3.8, 0.35, 0])
CL_AT = np.array([3.8, 0.35, 0])
LEDGER_X = -4.6
LEDGER_BASE = -2.4
PER_KJ = 0.0058


class Scene16SodiumChloride(Scene):
    def construct(self) -> None:
        play_scene(self)


def ledger_step(y0: float, y1: float, x: float, colour: str, label: str) -> VGroup:
    shelf = Line([x - 0.45, y1, 0], [x + 0.45, y1, 0], stroke_color=colour, stroke_width=5)
    arrow = Arrow([x, y0, 0], [x, y1, 0], buff=0.04, color=colour, stroke_width=7, tip_length=0.22,
                  max_tip_length_to_length_ratio=0.25)
    tag = txt(label, cfg.FONT["small"], colour).next_to(arrow, RIGHT, buff=0.15)
    return VGroup(arrow, shelf, tag)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "16", "Sodium gives, chlorine takes")

    # --- 1. Two atoms --------------------------------------------------------------------------------
    sodium = Atom(ed.ATOMIC_RADII_PM["Na"] * SCALE, NA_AT, charge="+11", core=ed.IONIC_RADII_PM["Na+"] * SCALE,
                  count=170, core_count=330, seed=161, glow=0.1)
    chlorine = Atom(ed.ATOMIC_RADII_PM["Cl"] * SCALE, CL_AT, charge="+17", core=0.42, count=420, seed=162, glow=0.2)
    na_name = eq(r"\mathrm{Na}", cfg.FONT["section"], cfg.BLUE).move_to([NA_AT[0], -2.15, 0])
    cl_name = eq(r"\mathrm{Cl}", cfg.FONT["section"], cfg.GREEN).move_to([CL_AT[0], -2.15, 0])
    scene.play(FadeIn(sodium, scale=0.6), FadeIn(chlorine, scale=0.6), FadeIn(na_name), FadeIn(cl_name), run_time=1.2)

    # --- 2. Sodium: one loose outer electron -----------------------------------------------------------
    head = dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    spot = NA_AT + 1.55 * np.array([np.cos(0.5), np.sin(0.5), 0])
    electron = glow_dot(spot, 0.15)
    na_fact = VGroup(txt("ionization", cfg.FONT["tiny"], cfg.MUTED),
                     txt(f"{ed.ionization_kj('Na')} kJ/mol · low", cfg.FONT["small"], cfg.GOLD)).arrange(DOWN, buff=0.1)
    na_fact.move_to([NA_AT[0], -3.15, 0])
    scene.play(FadeIn(electron, scale=0.4), FadeIn(na_fact, shift=UP * 0.1), run_time=1.0)

    # --- 3. Chlorine: one short ---------------------------------------------------------------------------
    beat(scene, t, 2)
    cl_fact = VGroup(txt("electron gain", cfg.FONT["tiny"], cfg.MUTED),
                     txt(f"{signed(ed.ELECTRON_GAIN_KJ['Cl'])} kJ/mol", cfg.FONT["small"], cfg.GREEN)).arrange(DOWN, buff=0.1)
    cl_fact.move_to([CL_AT[0], -3.15, 0])
    short = chip('One electron short', cfg.GREEN, cfg.FONT["small"]).move_to([CL_AT[0], 2.45, 0])
    scene.play(FadeIn(cl_fact, shift=UP * 0.1), FadeIn(short, shift=DOWN * 0.1), run_time=1.0)

    # --- 4. The transfer (a simplified model) ----------------------------------------------------------------
    beat(scene, t, 3)
    model = txt("simplified model", cfg.FONT["tiny"], cfg.MUTED).move_to([0, -0.9, 0])
    route = ArcBetweenPoints(spot, CL_AT + np.array([-0.85, 0.45, 0]), angle=-PI / 3)
    scene.play(FadeIn(model), MoveAlongPath(electron, route), run_time=2.0)

    # --- 5. Ions form ----------------------------------------------------------------------------------------
    beat(scene, t, 4)
    na_ion = eq(r"\mathrm{Na}^{+}", cfg.FONT["section"], cfg.CATION).move_to(na_name)
    cl_ion = eq(r"\mathrm{Cl}^{-}", cfg.FONT["section"], cfg.ANION).move_to(cl_name)
    scene.play(sodium.cloud.fade_to(0), *chlorine.resize(ed.IONIC_RADII_PM["Cl-"] * SCALE), FadeOut(electron),
               FadeThrough(na_name, na_ion), FadeThrough(cl_name, cl_ion), FadeOut(short), run_time=1.8)
    sizes = VGroup(txt("smaller", cfg.FONT["small"], cfg.CATION).move_to(NA_AT + UP * 2.2),
                   txt("larger", cfg.FONT["small"], cfg.ANION).move_to(CL_AT + UP * 2.45))
    scene.play(FadeIn(sizes), run_time=0.7)

    # --- 6. Opposite ions attract --------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(VGroup(sizes, model, na_fact, cl_fact)), run_time=0.4)
    na_to, cl_to = np.array([0.4, 0.35, 0]), np.array([4.9, 0.35, 0])
    scene.play(sodium.glide(na_to), chlorine.glide(cl_to), na_ion.animate.move_to([na_to[0], -2.15, 0]),
               cl_ion.animate.move_to([cl_to[0], -2.15, 0]), run_time=1.6)
    attract = DoubleArrow([na_to[0] + 1.15, 0.35, 0], [cl_to[0] - 2.0, 0.35, 0], buff=0, color=cfg.GOLD, stroke_width=6,
                          tip_length=0.2)
    scene.play(GrowFromCenter(attract), run_time=0.7)

    # --- 7. The honest ledger: the transfer alone is uphill ---------------------------------------------------------
    beat(scene, t, 6)
    ie, eg = ed.ionization_kj("Na"), ed.ELECTRON_GAIN_KJ["Cl"]
    start_shelf = Line([LEDGER_X - 1.6, LEDGER_BASE, 0], [LEDGER_X - 0.7, LEDGER_BASE, 0], stroke_color=cfg.WHITE, stroke_width=5)
    start_tag = txt("Na + Cl", cfg.FONT["tiny"], cfg.WHITE).next_to(start_shelf, DOWN, buff=0.12)
    up = ledger_step(LEDGER_BASE, LEDGER_BASE + ie * PER_KJ, LEDGER_X - 1.15, cfg.REQUIRED, f"+{ie}")
    down = ledger_step(LEDGER_BASE + ie * PER_KJ, LEDGER_BASE + (ie + eg) * PER_KJ, LEDGER_X + 0.35, cfg.RELEASED, signed(eg))
    net = ledger_step(LEDGER_BASE, LEDGER_BASE + (ie + eg) * PER_KJ, LEDGER_X + 1.85, cfg.REQUIRED, f"+{ie + eg}")
    ledger_unit = txt("kJ/mol", cfg.FONT["tiny"], cfg.MUTED).move_to([LEDGER_X, -3.25, 0])
    scene.play(Create(start_shelf), FadeIn(start_tag), FadeIn(ledger_unit), run_time=0.6)
    scene.play(GrowArrow(up[0]), Create(up[1]), FadeIn(up[2]), run_time=0.9)
    scene.play(GrowArrow(down[0]), Create(down[1]), FadeIn(down[2]), run_time=0.9)
    scene.play(GrowArrow(net[0]), Create(net[1]), FadeIn(net[2]), run_time=0.9)
    uphill = chip('Gas-phase transfer: uphill', cfg.REQUIRED, cfg.FONT["small"]).move_to([LEDGER_X, 2.55, 0])
    scene.play(FadeIn(uphill, shift=DOWN * 0.1), run_time=0.7)

    # --- 8. What comes next: a crystal ------------------------------------------------------------------------------
    beat(scene, t, 7)
    head = swap_heading(scene, head, "Many ions: a crystal")
    ledger = VGroup(start_shelf, start_tag, up, down, net, uphill, ledger_unit)
    scene.play(FadeOut(ledger), FadeOut(attract), FadeOut(VGroup(na_ion, cl_ion)), run_time=0.7)
    sites, kinds = rock_salt_sites(1)
    crystal = ProjectedCrystal(sites, kinds, {"Na+": 0.24, "Cl-": 0.44}, {"Na+": cfg.CATION, "Cl-": cfg.ANION},
                               spacing=1.3, center=[0.0, -0.1, 0], spin=0.25)
    scene.play(FadeOut(sodium, scale=0.5), FadeOut(chlorine, scale=0.5), FadeIn(crystal, scale=0.7), run_time=1.6)
    key = VGroup(VGroup(shaded_ball(0.17, cfg.CATION), eq(r"\mathrm{Na}^{+}", cfg.FONT["small"], cfg.CATION)).arrange(RIGHT, buff=0.2),
                 VGroup(shaded_ball(0.24, cfg.ANION), eq(r"\mathrm{Cl}^{-}", cfg.FONT["small"], cfg.ANION)).arrange(RIGHT, buff=0.2))
    key.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([5.6, 1.8, 0])
    scene.play(FadeIn(key), run_time=0.6)

    # --- 9. Six neighbours each -------------------------------------------------------------------------------------
    beat(scene, t, 8)
    centre_index = int(np.argmin(np.linalg.norm(sites, axis=1)))
    neighbours = [i for i, site in enumerate(sites) if abs(np.linalg.norm(site) - 1) < 1e-6]
    balls = crystal._all_balls
    scene.play(balls[centre_index][0].animate.set_stroke(cfg.WHITE, width=5),
               *[balls[i][0].animate.set_stroke(cfg.GOLD, width=5) for i in neighbours], run_time=1.0)
    six = chip(f"{len(neighbours)} nearest neighbours", cfg.GOLD, cfg.FONT["small"]).move_to([-5.0, 1.8, 0])
    scene.play(FadeIn(six, scale=1.1), run_time=0.7)

    # --- 10. The lattice pays the bill --------------------------------------------------------------------------------
    beat(scene, t, 9)
    pays = glow_arrow([-5.0, 0.9, 0], [-5.0, -2.6, 0], cfg.RELEASED, 9, tip=0.36)
    pays_tag = VGroup(txt('Lattice formation', cfg.FONT["small"], cfg.RELEASED),
                      txt('releases energy', cfg.FONT["small"], cfg.RELEASED)).arrange(DOWN, buff=0.08)
    pays_tag.next_to(pays, DOWN, buff=0.15)
    scene.play(GrowArrow(pays.arrow), FadeIn(pays[0]), FadeIn(pays_tag), run_time=1.2)

    # --- 11. Direction versus the whole story ---------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(VGroup(six, pays, pays_tag)), Glide(crystal, [1.4, -0.1, 0]), run_time=0.5)
    lessons = VGroup(
        VGroup(txt("ionization + electron gain", cfg.FONT["small"], cfg.GOLD), txt('electron-transfer tendency', cfg.FONT["small"], cfg.WHITE))
        .arrange(DOWN, buff=0.1),
        VGroup(txt("the whole energy story", cfg.FONT["small"], cfg.GREEN), txt('compound stability', cfg.FONT["small"], cfg.WHITE))
        .arrange(DOWN, buff=0.1),
    ).arrange(DOWN, buff=0.45).move_to([-4.6, 0.2, 0])
    scene.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in lessons], lag_ratio=0.5), run_time=1.6)

    # --- 12. Similar pairs ------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    pairs = VGroup(*[eq_chip(tex, cfg.WHITE, cfg.FONT["small"], stroke=cfg.MUTED) for tex in
                     (r"\mathrm{KCl}", r"\mathrm{NaBr}", r"\mathrm{KBr}")]).arrange(DOWN, buff=0.3).move_to([5.6, -1.2, 0])
    scene.play(FadeOut(lessons), LaggedStart(*[FadeIn(p, shift=LEFT * 0.2) for p in pairs], lag_ratio=0.3), run_time=1.4)

    # --- 13. The table predicts the chemistry -------------------------------------------------------------------------------
    beat(scene, t, 12)
    table = periodic_table(pitch=0.235, center=[-4.65, 0.75, 0], zs=range(1, 87), symbols=False, style="silhouette")
    scene.play(FadeIn(table), run_time=0.8)
    group_1 = [table.tiles[z] for z in pm.group_members(1) if z not in (1, 87)]
    group_17 = [table.tiles[z] for z in pm.group_members(17) if z <= 86]
    scene.play(*recolor_tiles(group_1, lambda z: cfg.CATION, fill=0.9), *recolor_tiles(group_17, lambda z: cfg.ANION, fill=0.9),
               run_time=1.0)
    predict = VGroup(txt("the table predicts", cfg.FONT["small"], cfg.WHITE),
                     txt("the chemistry", cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.1).next_to(table, DOWN, buff=0.4)
    scene.play(FadeIn(predict, shift=UP * 0.1), run_time=0.8)
    scene.play(*[Indicate(tile, color=cfg.WHITE, scale_factor=1.3) for tile in group_1 + group_17], run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["16"])
