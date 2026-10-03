"""Why the rows repeat: every period fills a fresh shell's s and p states, then closes.

The period lengths are counted by the model and explained with explicit
subshell recipes, showing why one period can fill several principal shells.
"""

from manim_scenes.common import *

PITCH = 0.62
CENTER = DOWN * 0.45
GAP_CENTER = np.array([-1.2, 2.0, 0])  # the empty top-centre of the table


class Scene13Periods(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _row_tiles(table: VGroup, p: int) -> list[VGroup]:
    """Main-table tiles of a period, left to right (f strips excluded)."""
    members = [z for z in pm.period_members(p) if pm.position(z)[0] <= 7]
    return [table.tiles[z] for z in sorted(members, key=lambda z: pm.position(z)[1])]


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "13", "The rows repeat")
    table = periodic_table(pitch=PITCH, center=CENTER)
    scene.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in table], lag_ratio=0.008), run_time=1.8)

    beat(scene, t, 1)
    start_tag = eq(r"ns^{1}", cfg.FONT["label"], cfg.BLUE).next_to(table.tiles[3], LEFT, buff=0.3)
    start_note = txt("new shell", cfg.FONT["tiny"], cfg.BLUE).next_to(start_tag, UP, buff=0.18).align_to(start_tag, RIGHT)
    scene.play(FadeIn(start_tag, shift=RIGHT * 0.2), FadeIn(start_note), Indicate(table.tiles[3], color=cfg.BLUE),
               run_time=1.2)

    beat(scene, t, 2)
    end_tag = eq(r"ns^{2}np^{6}", cfg.FONT["small"], cfg.GREEN).next_to(table.tiles[10], RIGHT, buff=0.25)
    end_note = txt("closed", cfg.FONT["tiny"], cfg.GREEN).next_to(end_tag, UP, buff=0.18).align_to(end_tag, LEFT)
    scene.play(FadeIn(end_tag, shift=LEFT * 0.2), FadeIn(end_note), Indicate(table.tiles[10], color=cfg.GREEN),
               run_time=1.2)

    # --- Sweep, return, sweep ---------------------------------------------------
    cursor = glow_frame(table.tiles[3], cfg.GOLD, buff=0.05)
    returns = VGroup()

    def sweep(p: int, run: float) -> None:
        row = _row_tiles(table, p)
        scene.play(cursor.animate.move_to(row[0]), run_time=0.3)
        scene.play(LaggedStart(*[Indicate(m, color=cfg.GOLD, scale_factor=1.25) for m in row], lag_ratio=0.3),
                   cursor.animate.move_to(row[-1]), run_time=run, rate_func=linear)

    beat(scene, t, 3)
    scene.play(FadeIn(cursor), run_time=0.3)
    sweep(2, 2.2)
    for index, p in ((4, 3), (5, 4)):
        beat(scene, t, index)
        last, first = _row_tiles(table, p - 1)[-1], _row_tiles(table, p)[0]
        back = CurvedArrow(last.get_right() + RIGHT * 0.1, first.get_left() + LEFT * 0.1, angle=-PI / 7,
                           color="#FF4FD8", stroke_width=5)
        returns.add(back)
        scene.play(Create(back), run_time=0.8)
        sweep(p, 2.4 if p == 3 else 2.8)

    # --- The cycle ---------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(cursor), FadeOut(returns), run_time=0.4)
    steps = VGroup(chip("ns¹  new shell", cfg.BLUE, cfg.FONT["tiny"]),
                   chip("fill the available states", cfg.CYAN, cfg.FONT["tiny"]),
                   chip("ns²np⁶  closed s + p", cfg.GREEN, cfg.FONT["tiny"])).arrange(DOWN, buff=0.24)
    steps.move_to(GAP_CENTER)
    links = VGroup(*[Arrow(steps[i].get_bottom(), steps[i + 1].get_top(), buff=0.04, color=cfg.MUTED, stroke_width=4,
                           max_tip_length_to_length_ratio=0.4) for i in range(2)])
    loop = CurvedArrow(steps[2].get_right() + RIGHT * 0.1, steps[0].get_right() + RIGHT * 0.1, angle=PI / 1.6,
                       color=cfg.GOLD, stroke_width=4)
    again = txt("again", cfg.FONT["tiny"], cfg.GOLD).next_to(loop, RIGHT, buff=0.12)
    scene.play(LaggedStart(FadeIn(steps[0]), GrowArrow(links[0]), FadeIn(steps[1]), GrowArrow(links[1]),
                           FadeIn(steps[2]), lag_ratio=0.3), run_time=2.0)
    scene.play(Create(loop), FadeIn(again), run_time=1.0)
    cycle = VGroup(steps, links, loop, again)

    # --- Chemistry cycles too ----------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(cycle), FadeOut(VGroup(start_tag, start_note, end_tag, end_note)), run_time=0.6)
    flow = VGroup(txt("reactive metal", cfg.FONT["small"], cfg.ORANGE),
                  txt("gradual change", cfg.FONT["small"], cfg.MUTED),
                  txt("unreactive gas", cfg.FONT["small"], cfg.GREEN)).arrange(DOWN, buff=0.3).move_to(GAP_CENTER + RIGHT * 0.3)
    reactive, inert = flow[0], flow[2]
    rail = Arrow(flow.get_corner(UL) + LEFT * 0.35, flow.get_corner(DL) + LEFT * 0.35, buff=0, stroke_width=5,
                 color=cfg.MUTED, max_tip_length_to_length_ratio=0.12)
    rail.set_color([cfg.ORANGE, cfg.GREEN])
    gradual = VGroup(rail, flow[1])
    scene.play(LaggedStart(FadeIn(reactive), FadeIn(gradual), FadeIn(inert), lag_ratio=0.3), run_time=1.2)
    for p in (2, 3, 4, 5):
        row = _row_tiles(table, p)
        scene.play(Indicate(row[0], color=cfg.ORANGE, scale_factor=1.35),
                   LaggedStart(*[Indicate(m, color=cfg.MUTED, scale_factor=1.05) for m in row[1:-1]], lag_ratio=0.05),
                   Indicate(row[-1], color=cfg.GREEN, scale_factor=1.35), run_time=1.6)

    # --- PERIODIC ------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(VGroup(reactive, gradual, inert)), run_time=0.4)
    word = Text("PERIODIC", font=cfg.TITLE_FONT, weight=BOLD, font_size=92, color=cfg.GOLD)
    word.set_stroke("#351F05", width=3, opacity=0.8, background=True)
    fit_width(word, 5.6)
    word.move_to(GAP_CENTER + UP * 0.45)
    recur = txt("properties recur", cfg.FONT["small"], cfg.WHITE).next_to(word, DOWN, buff=0.18)
    scene.play(LaggedStart(*[FadeIn(letter, shift=UP * 0.3, scale=1.4) for letter in word], lag_ratio=0.12), run_time=1.6)
    scene.play(FadeIn(recur, shift=UP * 0.15), run_time=0.6)

    # --- 2, 8, 8, 18, 18, 32, 32 ----------------------------------------------------
    beat(scene, t, 9)
    lengths = pm.period_lengths()
    xs = grid_point(1, 18, pitch=PITCH, center=CENTER)[0] + 0.95
    counts = VGroup(*[number(n, cfg.FONT["small"], cfg.GOLD).move_to([xs, grid_point(p, 18, pitch=PITCH, center=CENTER)[1], 0])
                      for p, n in zip(range(1, 8), lengths)])
    scene.play(FadeOut(VGroup(word, recur)), LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in counts], lag_ratio=0.25),
               run_time=2.0)
    note = txt("elements per period", cfg.FONT["tiny"], cfg.MUTED).rotate(-PI / 2).next_to(counts, RIGHT, buff=0.3)
    scene.play(FadeIn(note), run_time=0.5)

    beat(scene, t, 10)
    def recipe_card(period: int) -> VGroup:
        parts = []
        for index, (shell, count) in enumerate(pm.period_recipe(period)):
            if index:
                parts.append(eq("+", cfg.FONT["label"]))
            parts.append(eq(str(count), cfg.FONT["section"], cfg.BLOCK_COLORS[shell.letter]))
        parts.extend([eq("=", cfg.FONT["label"]), eq(str(len(pm.period_members(period))), cfg.FONT["section"], cfg.WHITE)])
        formula = VGroup(*parts).arrange(RIGHT, buff=0.22)
        family = VGroup(*[eq(shell.label, cfg.FONT["small"], cfg.BLOCK_COLORS[shell.letter])
                         for shell, _ in pm.period_recipe(period)]).arrange(RIGHT, buff=0.55)
        card = VGroup(family, formula).arrange(DOWN, buff=0.4).move_to(GAP_CENTER)
        return card

    card = recipe_card(2)
    scene.play(FadeOut(note), FadeIn(card), run_time=1.0)
    scene.play(*[Indicate(tiles_of(table, pm.period_members(p)), color=cfg.CYAN, scale_factor=1.05)
                 for p in (2, 3)], run_time=1.6)

    beat(scene, t, 11)
    longer = recipe_card(4)
    scene.play(ReplacementTransform(card, longer), run_time=1.0)
    scene.play(*[Indicate(tiles_of(table, pm.period_members(p)), color=cfg.GOLD, scale_factor=1.05)
                 for p in (4, 5)], run_time=1.6)

    beat(scene, t, 12)
    longest = recipe_card(6)
    scene.play(ReplacementTransform(longer, longest), run_time=1.0)
    scene.play(*[Indicate(tiles_of(table, pm.period_members(p)), color=cfg.PURPLE, scale_factor=1.05)
                 for p in (6, 7)], run_time=1.6)
    rhythm = caption("New shell. Repeating chemistry.", cfg.GOLD, cfg.FONT["small"], y=-4.12)
    hud(scene, rhythm)
    scene.play(FadeIn(rhythm, shift=UP * 0.2), run_time=0.9)
    end_scene(scene, t, cfg.SCENE_DURATIONS["13"])
