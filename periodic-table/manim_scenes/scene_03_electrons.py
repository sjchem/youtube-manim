"""The real puzzle: each new element brings one more electron. Where does it go?"""

from manim_scenes.common import *


class Scene03Electrons(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


# Scattered, not orbiting: deterministic positions inside the cloud.
ELECTRON_SPOTS = [np.array(p) for p in ((0.95, 0.55, 0), (-0.9, -0.6, 0), (0.15, -1.05, 0), (-0.4, 1.0, 0))]


def _atom(z: int, center, scale: float = 1.0) -> VGroup:
    cloud = electron_cloud(1.45 * scale, opacity=0.22).move_to(center)
    core = nucleus(z, radius=0.17 * scale).move_to(center)
    electrons = VGroup(*[glow_dot(np.asarray(center) + ELECTRON_SPOTS[i] * scale, 0.085 * scale + 0.02)
                         for i in range(z)])
    atom = VGroup(cloud, core, electrons)
    atom.cloud, atom.core, atom.electrons = cloud, core, electrons
    return atom


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "03", "A neutral atom")

    # --- Charges balance ---------------------------------------------------
    atom = _atom(3, LEFT * 3.4 + DOWN * 0.2, 1.35)
    scene.play(FadeIn(atom.cloud, scale=0.6), GrowFromCenter(atom.core), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(e, scale=0.3) for e in atom.electrons], lag_ratio=0.3), run_time=1.0)
    plus = txt("3 protons   +3", cfg.FONT["label"], cfg.PROTON_COLOR)
    minus = txt("3 electrons   −3", cfg.FONT["label"], cfg.ELECTRON_COLOR)
    total = txt("net charge   0", cfg.FONT["label"], cfg.GREEN)
    ledger = VGroup(plus, minus, total).arrange(DOWN, aligned_edge=RIGHT, buff=0.38).move_to(RIGHT * 3.2 + UP * 0.4)
    bar = Line(LEFT * 2.2, RIGHT * 2.2, stroke_color=cfg.MUTED, stroke_width=3).move_to(
        (minus.get_bottom() + total.get_top()) / 2).align_to(ledger, RIGHT)
    scene.play(FadeIn(plus, shift=LEFT * 0.3), run_time=0.6)
    scene.play(FadeIn(minus, shift=LEFT * 0.3), run_time=0.6)
    scene.play(Create(bar), FadeIn(total, shift=UP * 0.2), run_time=0.7)

    # --- Each step adds one proton and one electron ------------------------
    beat(scene, t, 1)
    step = VGroup(eq(r"Z", cfg.FONT["title"], cfg.GOLD), eq(r"\rightarrow", cfg.FONT["title"]),
                  eq(r"Z+1", cfg.FONT["title"], cfg.GOLD)).arrange(RIGHT, buff=0.35).move_to(RIGHT * 3.2 + UP * 1.0)
    add_p = chip(" +1 proton", cfg.PROTON_COLOR, cfg.FONT["small"])
    add_e = chip(" +1 electron", cfg.ELECTRON_COLOR, cfg.FONT["small"])
    adds = VGroup(add_p, add_e).arrange(DOWN, buff=0.35).next_to(step, DOWN, buff=0.6)
    scene.play(FadeOut(VGroup(plus, minus, total, bar), shift=RIGHT * 0.3), FadeIn(step), run_time=0.8)
    beryllium = _atom(4, LEFT * 3.4 + DOWN * 0.2, 1.35)
    proton = nucleon(cfg.PROTON_COLOR, 0.23).move_to(LEFT * 7 + UP * 2.5)
    electron = glow_dot(LEFT * 7 + DOWN * 2.8, 0.13)
    scene.play(FadeIn(add_p, shift=UP * 0.2), FadeIn(proton), run_time=0.6)
    scene.play(proton.animate.move_to(atom.core.get_center()).scale(0.7),
               ReplacementTransform(atom.core, beryllium.core), run_time=1.0)
    scene.remove(proton)
    scene.play(FadeIn(add_e, shift=UP * 0.2), FadeIn(electron), run_time=0.6)
    scene.play(ReplacementTransform(electron, beryllium.electrons[3]),
               ReplacementTransform(atom.electrons, beryllium.electrons[:3]),
               ReplacementTransform(atom.cloud, beryllium.cloud), run_time=1.0)

    # --- H, He, Li, Be ------------------------------------------------------
    beat(scene, t, 2)
    head = swap_heading(scene, head, "One more electron each step")
    row = VGroup(*[_atom(z, ORIGIN, 0.85) for z in range(1, 5)]).arrange(RIGHT, buff=0.85).move_to(UP * 0.75)
    tiles = VGroup(*[element_tile(z, 1.05, cfg.CYAN, number=True).next_to(row[z - 1], DOWN, buff=0.3)
                     for z in range(1, 5)])
    counts = VGroup(*[txt(f"{z} e⁻", cfg.FONT["label"], cfg.ELECTRON_COLOR).next_to(tiles[z - 1], DOWN, buff=0.3)
                      for z in range(1, 5)])
    scene.play(FadeOut(VGroup(step, adds)), ReplacementTransform(beryllium, row[3]), run_time=1.0)
    for z in range(1, 4):
        scene.play(FadeIn(row[z - 1], scale=0.7), FadeIn(tiles[z - 1], shift=UP * 0.2),
                   FadeIn(counts[z - 1]), run_time=0.8)
    scene.play(FadeIn(tiles[3], shift=UP * 0.2), FadeIn(counts[3]), run_time=0.8)

    # --- The proton is easy; the electron is the question -------------------
    beat(scene, t, 3)
    cores = VGroup(*[a.core for a in row])
    clouds = VGroup(*[VGroup(a.cloud, a.electrons) for a in row])
    checks = VGroup(*[txt("✓", 40, cfg.GREEN).next_to(c, UR, buff=0.02) for c in cores])
    scene.play(Indicate(cores, color=cfg.GOLD, scale_factor=1.15), run_time=1.0)
    scene.play(FadeIn(checks), cores.animate.set_opacity(0.45), run_time=0.7)
    scene.play(Indicate(clouds, color=cfg.CYAN, scale_factor=1.08), run_time=1.3)

    beat(scene, t, 4)
    question = txt("Where does the electron go?", cfg.FONT["title"], cfg.GOLD)
    fit_width(question, 13.4)
    question.move_to(ORIGIN)
    scene.play(FadeOut(VGroup(row, tiles, counts, checks), shift=DOWN * 0.3), FadeOut(head), run_time=0.7)
    scene.play(Write(question), run_time=1.6)
    scene.play(question.animate.scale(1.05), rate_func=there_and_back, run_time=1.0)

    # --- Bring back the orbitals from Part 2 --------------------------------
    beat(scene, t, 5)
    labels = ("1s", "2s", "2p", "3s", "3p", "4s", "3d")
    ladder = box_ladder(labels, bottom=-3.4, step=0.98, box=0.74, x=-1.3)
    filling_axis = Arrow([-6.6, -3.8, 0], [-6.6, 3.0, 0], buff=0, color=cfg.MUTED, stroke_width=4)
    filling_tag = txt("fill order", cfg.FONT["small"], cfg.MUTED).rotate(PI / 2).next_to(filling_axis, LEFT, buff=0.15)
    recall = chip("From Part 2", cfg.PURPLE, cfg.FONT["small"]).move_to(RIGHT * 4.6 + UP * 1.6)
    head = heading("The usual filling sequence")
    hud(scene, head)
    scene.play(question.animate.scale(0.5).move_to(UP * 3.85).set_opacity(0), FadeIn(head), FadeIn(recall), run_time=0.8)
    scene.remove(question)
    scene.play(GrowArrow(filling_axis), FadeIn(filling_tag), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(r, shift=UP * 0.25) for r in ladder], lag_ratio=0.18), run_time=2.6)

    # --- Lowest available state first ---------------------------------------
    beat(scene, t, 6)
    arrows = {label: row_arrows(ladder.rows[label], ladder.rows[label].boxes.__len__() * 2) for label in labels}
    source = RIGHT * 6.4 + UP * 2.6
    electron_arrives(scene, arrows["1s"][0], source, 1.2)
    electron_arrives(scene, arrows["1s"][1], source, 1.0)
    electron_arrives(scene, arrows["2s"][0], source, 1.0)

    beat(scene, t, 7)
    z_counter = VGroup(eq("Z =", cfg.FONT["section"], cfg.GOLD), number(3, cfg.FONT["section"]))
    z_counter.arrange(RIGHT, buff=0.2).move_to(RIGHT * 4.6 + DOWN * 0.4)
    scene.play(FadeIn(z_counter), run_time=0.4)
    sequence = [arrows["2s"][1]] + arrows["2p"] + arrows["3s"] + arrows["3p"]
    for index, arrow in enumerate(sequence):
        scene.play(drop_in(arrow), z_counter[1].animate.set_value(4 + index), run_time=0.32)

    # --- How many can each hold? -------------------------------------------
    beat(scene, t, 8)
    marks = VGroup()
    for label in ("1s", "2p", "3d"):
        row_mob = ladder.rows[label]
        mark = txt("?", cfg.FONT["title"], cfg.GOLD).next_to(row_mob.boxes, RIGHT, buff=0.45)
        marks.add(mark)
    scene.play(LaggedStart(*[FadeIn(m, scale=0.4) for m in marks], lag_ratio=0.3), run_time=1.2)
    scene.play(*[Circumscribe(ladder.rows[label].boxes, color=cfg.GOLD) for label in ("1s", "2p", "3d")], run_time=1.6)

    beat(scene, t, 9)
    table = periodic_table(pitch=0.32, center=RIGHT * 4.75 + DOWN * 0.9, style="block", symbols=False)
    hint = chip("capacity  →  width", cfg.GOLD, cfg.FONT["small"]).next_to(table, UP, buff=0.35)
    scene.play(FadeOut(z_counter), FadeOut(recall), FadeIn(table, scale=0.8), run_time=1.2)
    scene.play(FadeIn(hint, shift=DOWN * 0.2), run_time=0.6)
    scene.play(LaggedStart(*[Indicate(block_tiles(table, b), color=cfg.WHITE, scale_factor=1.06) for b in "sdpf"],
                           lag_ratio=0.3), run_time=2.4)
    scene.play(Circumscribe(hint, color=cfg.GOLD), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["03"])
