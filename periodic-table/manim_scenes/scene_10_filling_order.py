"""The filling order, and the n + l guide that captures most of it.

The chain, the scores and the diagonal chart are all generated from
``pm.madelung_order()``, so the chart cannot disagree with the order the film
uses everywhere else.
"""

from manim_scenes.common import *

GRID_X0 = -0.75
GRID_DX = 2.05
GRID_Y0 = 2.55
GRID_DY = 0.93
NOTES_X = -4.5
FLOW_COLOR = "#FF4FD8"  # Neon pink stays distinct from all four block colours.


class Scene10FillingOrder(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _chip(shell: pm.Subshell, size: int | None = None) -> VGroup:
    colour = cfg.BLOCK_COLORS[shell.letter]
    label = eq(shell.label, size or cfg.FONT["small"], colour)
    pill = RoundedRectangle(width=label.width + 0.32, height=label.height + 0.26, corner_radius=0.14,
                            stroke_color=colour, stroke_width=2.5, fill_color=cfg.PANEL, fill_opacity=1)
    return VGroup(pill, label.move_to(pill))


def _chain(order, per_line: int = 10) -> VGroup:
    lines = VGroup()
    for start in range(0, len(order), per_line):
        line = VGroup()
        for index, shell in enumerate(order[start:start + per_line]):
            if index:
                line.add(eq(r"\rightarrow", cfg.FONT["tiny"], cfg.MUTED))
            line.add(_chip(shell))
        line.arrange(RIGHT, buff=0.12)
        lines.add(line)
    lines.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
    return lines


def _grid_point(shell: pm.Subshell) -> np.ndarray:
    return np.array([GRID_X0 + shell.l * GRID_DX, GRID_Y0 - (shell.n - 1) * GRID_DY, 0])


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "10", "The filling order")
    order = pm.madelung_order()

    naive = VGroup(*[_chip(pm.subshell(x), cfg.FONT["label"]) for x in ("3s", "3p", "3d", "4s")]).arrange(RIGHT, buff=0.35)
    naive.move_to(UP * 0.4)
    naive_tag = txt("shell by shell?", cfg.FONT["label"], cfg.MUTED).next_to(naive, UP, buff=0.4)
    scene.play(FadeIn(naive_tag), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in naive], lag_ratio=0.2), run_time=1.4)
    cross = cross_mark(0.5).move_to(naive)
    scene.play(FadeIn(cross, scale=1.5), naive.animate.set_opacity(0.35), run_time=0.8)

    # --- The real order -------------------------------------------------------
    beat(scene, t, 1)
    chain = _chain(order[:14], per_line=7).move_to(DOWN * 0.1)
    fit_width(chain, 14.6)
    scene.play(FadeOut(VGroup(naive, naive_tag, cross)), run_time=0.5)
    items = [m for line in chain for m in line]
    scene.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in items], lag_ratio=0.18), run_time=10.0)
    spot = [m for m in items if isinstance(m, VGroup) and len(m) == 2]
    surprises = VGroup(*[spot[i] for i, s in enumerate(order[:14]) if s.label in ("4s", "3d", "4f")])
    scene.play(*[Indicate(m, color=cfg.ORANGE, scale_factor=1.2) for m in surprises], run_time=1.4)

    # --- n + l ----------------------------------------------------------------
    beat(scene, t, 2)
    head = swap_heading(scene, head, "A shortcut: n + l")
    scene.play(FadeOut(chain), run_time=1.0)
    name = txt("Madelung rule", cfg.FONT["section"], cfg.GOLD).move_to(UP * 1.35)
    scene.play(FadeIn(name, scale=1.1), run_time=0.8)

    beat(scene, t, 3)
    score = VGroup(txt("score", cfg.FONT["body"], cfg.MUTED), eq("=", cfg.FONT["section"]),
                   eq("n", cfg.FONT["section"], cfg.CYAN), eq("+", cfg.FONT["section"]),
                   eq("l", cfg.FONT["section"], cfg.GOLD)).arrange(RIGHT, buff=0.25).move_to(UP * 0.2)
    legend = VGroup(*[VGroup(eq(letter, cfg.FONT["label"], cfg.BLOCK_COLORS[letter]),
                             eq(rf"= {i}", cfg.FONT["label"], cfg.GOLD)).arrange(RIGHT, buff=0.15)
                      for i, letter in enumerate("spdf")]).arrange(RIGHT, buff=0.9).move_to(DOWN * 1.05)
    l_tag = eq("l:", cfg.FONT["label"], cfg.GOLD).next_to(legend, LEFT, buff=0.5)
    scene.play(ReplacementTransform(name, score), run_time=1.0)
    scene.play(FadeIn(l_tag), LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in legend], lag_ratio=0.25), run_time=1.6)

    beat(scene, t, 4)
    s4, d3 = pm.subshell("4s"), pm.subshell("3d")
    compare = VGroup(
        VGroup(_chip(s4, cfg.FONT["label"]), eq(rf"4 + 0 = {s4.madelung}", cfg.FONT["label"])).arrange(RIGHT, buff=0.35),
        VGroup(_chip(d3, cfg.FONT["label"]), eq(rf"3 + 2 = {d3.madelung}", cfg.FONT["label"])).arrange(RIGHT, buff=0.35),
    ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 2.75)
    scene.play(FadeIn(compare[0], shift=UP * 0.2), run_time=0.8)
    scene.play(FadeIn(compare[1], shift=UP * 0.2), run_time=0.8)
    win = txt("first", cfg.FONT["small"], cfg.GREEN).next_to(compare[0], RIGHT, buff=0.4)
    scene.play(FadeIn(win), Indicate(compare[0], color=cfg.GREEN), run_time=1.0)

    beat(scene, t, 5)
    rules = VGroup(chip("lower n + l first", cfg.GREEN, cfg.FONT["small"]),
                   chip("tie: smaller n first", cfg.CYAN, cfg.FONT["small"])).arrange(RIGHT, buff=0.5)
    rules.move_to(DOWN * 1.05)
    scene.play(FadeOut(VGroup(legend, l_tag)), FadeIn(rules[0], shift=UP * 0.2), run_time=0.8)
    scene.play(FadeIn(rules[1], shift=UP * 0.2), run_time=0.8)

    # --- The diagonal chart --------------------------------------------------
    beat(scene, t, 6)
    # The chain was removed at beat 2; fading it again would bring it back.
    scene.play(FadeOut(VGroup(score, compare, win, rules)), run_time=0.7)
    head = swap_heading(scene, head, "Read the diagonals")
    cells = {shell: _chip(shell, cfg.FONT["label"]).move_to(_grid_point(shell)).set_z_index(2) for shell in order}
    column_tags = VGroup(*[txt(f"l = {l}", cfg.FONT["tiny"], cfg.MUTED).move_to(_grid_point(pm.Subshell(1, l)) + UP * 0.0)
                           for l in range(4)])
    for tag_mob, l in zip(column_tags, range(4)):
        tag_mob.move_to(np.array([GRID_X0 + l * GRID_DX, GRID_Y0 + 0.75, 0]))
    column_tags[0].set_opacity(0)
    scene.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in cells.values()], lag_ratio=0.05), run_time=2.0)

    diagonals = {}
    for shell in order:
        diagonals.setdefault(shell.madelung, []).append(shell)
    arrows = VGroup()
    for k, members in sorted(diagonals.items()):
        members.sort(key=lambda s: s.n)
        start_point = _grid_point(members[0]) + UR * 0.35
        end_point = _grid_point(members[-1]) + DL * 0.35
        if len(members) == 1:
            start_point, end_point = _grid_point(members[0]) + UR * 0.5, _grid_point(members[0]) + UR * 0.18
        arrows.add(Arrow(start_point, end_point, buff=0, color=FLOW_COLOR, stroke_width=4.5,
                         max_tip_length_to_length_ratio=0.12 if len(members) > 1 else 0.5).set_z_index(1))

    beat(scene, t, 7)
    counter = VGroup(eq("n + l =", cfg.FONT["label"], cfg.GOLD), number(1, cfg.FONT["label"]))
    counter.arrange(RIGHT, buff=0.2).move_to(np.array([NOTES_X, 1.7, 0]))
    scene.play(FadeIn(counter), run_time=0.4)
    for (k, members), arrow in zip(sorted(diagonals.items()), arrows):
        scene.play(GrowArrow(arrow), counter[1].animate.set_value(k),
                   *[cells[m][0].animate.set_fill(interpolate_color(ManimColor(cfg.PANEL), ManimColor(cfg.BLOCK_COLORS[m.letter]), 0.28))
                     for m in members],
                   *[cells[m][1].animate.set_color(cfg.WHITE) for m in members], run_time=0.62)

    # --- A guide, not a law ----------------------------------------------------
    beat(scene, t, 8)
    caveat = VGroup(chip("A guide, not a law", cfg.ORANGE, cfg.FONT["small"]),
                    txt("neutral ground states", cfg.FONT["small"], cfg.MUTED),
                    txt("occupancy changes energies", cfg.FONT["small"], cfg.MUTED))
    caveat.arrange(DOWN, buff=0.3)
    fit_width(caveat, 5.3)
    caveat.move_to(np.array([NOTES_X, -0.9, 0]))
    scene.play(FadeOut(counter), LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in caveat], lag_ratio=0.3), run_time=1.6)

    beat(scene, t, 9)
    late = VGroup(cells[pm.subshell("4s")], cells[pm.subshell("3d")])
    scene.play(FadeOut(caveat), *[Circumscribe(m, color=cfg.GOLD) for m in late], run_time=1.2)
    late_note = VGroup(eq(r"\mathrm{Fe}:\ 3d^6\,4s^2", cfg.FONT["small"], cfg.WHITE),
                       eq(r"\mathrm{Fe}^{2+}:\ 3d^6", cfg.FONT["small"], cfg.GOLD)).arrange(DOWN, buff=0.25)
    late_note.move_to(np.array([NOTES_X, 0.2, 0]))
    scene.play(FadeIn(late_note, shift=RIGHT * 0.2), run_time=0.8)

    beat(scene, t, 10)
    s6, f4 = cells[pm.subshell("6s")], cells[pm.subshell("4f")]
    jump = CurvedArrow(s6.get_right() + RIGHT * 0.05, f4.get_left() + LEFT * 0.05, angle=-PI / 3,
                       color=FLOW_COLOR, stroke_width=5).set_z_index(3)
    jump.set_fill(opacity=0, family=False)
    jump_glow = jump.copy().set_fill(opacity=0).set_stroke(width=14, opacity=0.18).set_z_index(1)
    scene.play(FadeOut(late_note), Create(jump_glow), Create(jump), run_time=1.2)
    scene.play(Indicate(f4, color=FLOW_COLOR, scale_factor=1.35), run_time=1.0)

    beat(scene, t, 11)
    fourteen = VGroup(eq("4f", cfg.FONT["section"], cfg.PURPLE), eq(r"\rightarrow\ 14", cfg.FONT["section"], cfg.GOLD))
    fourteen.arrange(RIGHT, buff=0.3).move_to(np.array([NOTES_X, 0.6, 0]))
    where = txt("Where do they fit?", cfg.FONT["label"], cfg.GOLD).next_to(fourteen, DOWN, buff=0.4)
    scene.play(FadeIn(fourteen, shift=RIGHT * 0.2), run_time=0.8)
    scene.play(FadeIn(where), run_time=0.7)
    scene.play(Indicate(f4, color=cfg.PURPLE, scale_factor=1.3), Indicate(where, color=cfg.GOLD), run_time=1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["10"])
