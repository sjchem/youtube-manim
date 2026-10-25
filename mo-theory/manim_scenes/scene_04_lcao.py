"""Chapter 04 — LCAO: sums and differences of atomic wave functions.

Every map is computed from ``utils.orbital_models``: two normalised 1s
orbitals, their normalised sum and difference, and their squares. The colour
of a phase map is the sign of psi (blue +, rose -); a density map is |psi|^2
in cyan. The four-atom row uses Huckel coefficients
(``physics_models.huckel_chain``): four orbitals in, four combinations out,
with 0, 1, 2 and 3 nodes.
"""

from manim_scenes.common import *

EXTENT = (4.6, 2.5)
BOND = om.MOSpec("s", 1.0, om.R_S)
ANTI = om.MOSpec("s", -1.0, om.R_S)


class Scene04Lcao(Scene):
    def construct(self) -> None:
        play_scene(self)


def orbital_map(spec: om.MOSpec, width: float, mode: str = "phase", at=ORIGIN, vmax: float | None = None) -> PhaseMap:
    m = PhaseMap(spec_func(spec), extent=EXTENT, width=width, mode=mode, vmax=vmax)
    return m.move_to(at)


def tile(spec: om.MOSpec, width: float, at, label: str, color: str) -> Group:
    m = orbital_map(spec, width, at=at, vmax=om.ao_peak("s"))
    frame = RoundedRectangle(width=m.width + 0.1, height=m.height + 0.1, corner_radius=0.15, stroke_color=color,
                             stroke_width=3, fill_opacity=0).move_to(m)
    name = eq(label, cfg.FONT["label"], color).next_to(frame, DOWN, buff=0.15)
    return Group(m, frame, name)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "04", "Adding atomic waves")

    # --- 1. Linear Combination of Atomic Orbitals -----------------------------------------------------------------------
    words = VGroup(*[txt(w, cfg.FONT["title"], cfg.WHITE) for w in ("Linear", "Combination", "of", "Atomic", "Orbitals")])
    words.arrange(RIGHT, buff=0.35).move_to([0, 0.6, 0])
    fit_width(words, 14.4)
    scene.play(LaggedStart(*[FadeIn(w, shift=UP * 0.2) for w in words], lag_ratio=0.18), run_time=1.8)
    dismiss_opening_title(scene, t, head, at=2.6)
    initials = VGroup(*[w[0] for w in (words[0], words[1], words[3], words[4])])
    scene.play(initials.animate.set_color(cfg.GOLD), run_time=0.8)
    lcao = result_label("LCAO", cfg.GOLD, cfg.FONT["hero"]).move_to([0, -1.5, 0])
    scene.play(FadeIn(lcao, shift=UP * 0.3), run_time=1.2)

    # --- 2. phi_A and phi_B ------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    phi_a = tile(om.MOSpec("s", 1.0, om.R_S, single="A"), 6.0, [-3.8, 0.5, 0], r"\phi_A", cfg.PHASE_PLUS)
    phi_b = tile(om.MOSpec("s", 1.0, om.R_S, single="B"), 6.0, [3.8, 0.5, 0], r"\phi_B", cfg.PHASE_PLUS)
    scene.play(FadeOut(words), run_time=0.4)
    scene.play(lcao.animate.scale(0.5).move_to([-6.2, 3.7, 0]), run_time=0.6)
    scene.play(FadeIn(phi_a, shift=RIGHT * 0.3), FadeIn(phi_b, shift=LEFT * 0.3), run_time=1.4)

    # --- 3. Sum and difference ----------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    plus_eq = eq([r"\psi_+", r"\propto", r"\phi_A + \phi_B"], cfg.FONT["title"])
    minus_eq = eq([r"\psi_-", r"\propto", r"\phi_A - \phi_B"], cfg.FONT["title"])
    plus_eq[0].set_color(cfg.BONDING)
    minus_eq[0].set_color(cfg.ANTIBONDING)
    equations = VGroup(plus_eq, minus_eq).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([0, 0.2, 0])
    scene.play(FadeOut(phi_a), FadeOut(phi_b), run_time=0.8)
    scene.play(Write(plus_eq), run_time=1.4)
    scene.play(Write(minus_eq), run_time=1.4)

    # --- 4. The proportional sign: a left-out normalisation --------------------------------------------------------------------------
    beat(scene, t, 3)
    frames = VGroup(glow_frame(plus_eq[1], cfg.GOLD, buff=0.1), glow_frame(minus_eq[1], cfg.GOLD, buff=0.1))
    normal = caption("A scaling factor is left out: it normalises each orbital", cfg.GOLD)
    scene.play(Create(frames), FadeIn(normal), run_time=1.2)

    # --- 5. Wave functions, not charges --------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    waves = caption("We add waves, not electric charges", cfg.RED)
    scene.play(FadeOut(frames), fade_through(normal, waves), run_time=0.9)
    scene.remove(normal)
    scene.play(Indicate(VGroup(plus_eq[2], minus_eq[2]), color=cfg.PHASE_PLUS, scale_factor=1.06), run_time=1.4)

    # --- 6. What we measure: psi squared ---------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    square = eq([r"\text{electron density}", r"=", r"|\psi|^2"], cfg.FONT["title"])
    square[2].set_color(cfg.DENSITY)
    square.move_to([0, 0.2, 0])
    scene.play(FadeOut(waves), equations.animate.arrange(RIGHT, buff=1.2).scale(0.55).move_to([0.6, 3.4, 0]), run_time=1.0)
    scene.play(Write(square), run_time=1.6)
    scene.play(Indicate(square[2], color=cfg.WHITE, scale_factor=1.15), run_time=1.0)

    # --- 7. Square the sum: density between the nuclei ------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    dense_plus = orbital_map(BOND, 7.2, mode="density", at=[-3.9, -0.15, 0])
    dense_minus = orbital_map(ANTI, 7.2, mode="density", at=[3.9, -0.15, 0])
    label_plus = eq(r"|\psi_+|^2", cfg.FONT["section"], cfg.BONDING).next_to(dense_plus, UP, buff=0.1)
    label_minus = eq(r"|\psi_-|^2", cfg.FONT["section"], cfg.ANTIBONDING).next_to(dense_minus, UP, buff=0.1)
    scene.play(FadeOut(square), run_time=0.6)
    scene.play(FadeIn(dense_plus), FadeIn(label_plus), run_time=1.4)
    between = Circle(radius=0.62, stroke_color=cfg.GREEN, stroke_width=5).move_to(dense_plus.to_screen(0, 0))
    gathers = caption("Density gathers between the nuclei", cfg.GREEN)
    scene.play(Create(between), FadeIn(gathers), run_time=1.0)

    # --- 8. Square the difference: pushed outward, an empty plane ----------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeIn(dense_minus), FadeIn(label_minus), run_time=1.4)
    node_line = DashedLine(dense_minus.to_screen(0, 2.3), dense_minus.to_screen(0, -2.3), stroke_color=cfg.NODE,
                           stroke_width=4, dash_length=0.12)
    empty = caption("Density pushed outward; an empty plane in the middle", cfg.ANTIBONDING)
    scene.play(Create(node_line), fade_through(gathers, empty), run_time=1.2)
    scene.remove(gathers)

    # --- 9. The same orbitals as phase maps ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    phase_plus = orbital_map(BOND, 7.2, at=dense_plus.get_center())
    phase_minus = orbital_map(ANTI, 7.2, at=dense_minus.get_center())
    key = VGroup(eq("+", cfg.FONT["section"], cfg.PHASE_PLUS), txt("positive", cfg.FONT["small"], cfg.PHASE_PLUS),
                 eq("-", cfg.FONT["section"], cfg.PHASE_MINUS), txt("negative", cfg.FONT["small"], cfg.PHASE_MINUS))
    key.arrange(RIGHT, buff=0.25).move_to([0, -2.75, 0])
    key[2].shift(RIGHT * 0.5)
    key[3].shift(RIGHT * 0.5)
    lab_plus = eq(r"\psi_+", cfg.FONT["section"], cfg.BONDING).move_to(label_plus)
    lab_minus = eq(r"\psi_-", cfg.FONT["section"], cfg.ANTIBONDING).move_to(label_minus)
    phase_note = caption("Colour shows phase, not charge", cfg.WHITE)
    scene.play(FadeOut(dense_plus), FadeIn(phase_plus), FadeOut(dense_minus), FadeIn(phase_minus), FadeOut(between),
               Transform(label_plus, lab_plus), Transform(label_minus, lab_minus), run_time=1.6)
    scene.play(FadeIn(key), fade_through(empty, phase_note), run_time=1.0)
    scene.remove(empty)

    # --- 10. Two in, two out ---------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(Group(phase_plus, phase_minus, label_plus, label_minus, key, node_line, phase_note)), run_time=0.8)
    ins = Group(tile(om.MOSpec("s", 1.0, om.R_S, single="A"), 3.6, [-4.9, 1.2, 0], r"\phi_A", cfg.PHASE_PLUS),
                tile(om.MOSpec("s", 1.0, om.R_S, single="B"), 3.6, [-4.9, -1.6, 0], r"\phi_B", cfg.PHASE_PLUS))
    outs = Group(tile(BOND, 3.6, [4.9, 1.2, 0], r"\psi_+", cfg.BONDING),
                 tile(ANTI, 3.6, [4.9, -1.6, 0], r"\psi_-", cfg.ANTIBONDING))
    funnel = VGroup(*[glow_arrow([-2.7, y, 0], [2.7, y2, 0], cfg.MUTED, width=5) for y, y2 in ((1.2, 1.2), (-1.6, -1.6))])
    count = eq(r"2 \rightarrow 2", cfg.FONT["hero"], cfg.WHITE).move_to([0, -0.2, 0])
    scene.play(FadeIn(ins, shift=RIGHT * 0.2), run_time=1.0)
    scene.play(GrowFromEdge(funnel, LEFT), FadeIn(outs, shift=RIGHT * 0.2), run_time=1.6)
    scene.play(Write(count), run_time=1.0)

    # --- 11. Not one, not three: two ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    wrong = VGroup(txt("1", 110, cfg.MUTED), txt("3", 110, cfg.MUTED)).arrange(RIGHT, buff=3.0).move_to([0, 2.25, 0])
    scene.play(FadeIn(wrong[0]), run_time=0.4)
    scene.play(Create(cross_mark(0.4).move_to(wrong[0])), FadeIn(wrong[1]), run_time=0.6)
    scene.play(Create(cross_mark(0.4).move_to(wrong[1])), count.animate.set_color(cfg.GREEN).scale(1.15), run_time=0.8)

    # --- 12. Four in, four out; N in, N out ----------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    scene.play(*[FadeOut(m) for m in scene.mobjects if not getattr(m, "_is_project_background", False) and m is not lcao],
               run_time=0.8)
    energies, vectors = pm.huckel_chain(4)
    spacing = 2.3
    rows = Group()
    for j in range(4):
        m = PhaseMap(lambda X, Y, c=vectors[:, j]: om.chain_section(c, spacing, X, Y), extent=(6.4, 1.35), width=7.4,
                     vmax=0.5)
        m.move_to([1.2, -2.35 + 1.55 * j, 0])
        nodes = txt(f"{j} node" + ("s" if j != 1 else ""), cfg.FONT["small"], cfg.MUTED).next_to(m, RIGHT, buff=0.35)
        rows.add(Group(m, nodes))
    atoms = VGroup(*[nucleus_dot(rows[0][0].to_screen((i - 1.5) * spacing, 0), radius=0.06) for i in range(4)])
    energy = Arrow([-3.4, -2.8, 0], [-3.4, 2.6, 0], buff=0, color=cfg.MUTED, stroke_width=5, tip_length=0.26)
    e_label = eq("E", cfg.FONT["label"], cfg.MUTED).next_to(energy, LEFT, buff=0.15)
    four = eq(r"4 \rightarrow 4", cfg.FONT["title"], cfg.WHITE).move_to([-6.0, 0.8, 0])
    scene.play(Create(energy), FadeIn(e_label), FadeIn(rows[0]), FadeIn(atoms), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in rows[1:]], lag_ratio=0.35), Write(four), run_time=2.0)
    n_chip = eq_chip(r"N \rightarrow N", cfg.PURPLE, cfg.FONT["section"]).move_to([-6.0, -0.8, 0])
    scene.play(FadeIn(n_chip, scale=0.9), run_time=0.9)

    # --- 13. An approximation, with an exact count ----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    approx = caption("An approximation. Within the chosen basis, the count is exact.", cfg.PURPLE)
    scene.play(FadeIn(approx), Indicate(n_chip, color=cfg.WHITE, scale_factor=1.06), run_time=1.2)

    # --- 14. One helps, one works against -------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    scene.play(*[FadeOut(m) for m in (rows, atoms, energy, e_label, four, n_chip, approx)], run_time=0.8)
    helps = tile(BOND, 5.6, [-3.6, 0.4, 0], r"\psi_+", cfg.BONDING)
    hurts = tile(ANTI, 5.6, [3.6, 0.4, 0], r"\psi_-", cfg.ANTIBONDING)
    verdicts = VGroup(txt("holds them together", cfg.FONT["body"], cfg.GREEN).next_to(helps, DOWN, buff=0.3),
                      txt("works against it", cfg.FONT["body"], cfg.ANTIBONDING).next_to(hurts, DOWN, buff=0.3))
    scene.play(FadeIn(helps), FadeIn(hurts), run_time=1.0)
    scene.play(FadeIn(verdicts[0], shift=UP * 0.15), run_time=0.8)
    scene.play(FadeIn(verdicts[1], shift=UP * 0.15), run_time=0.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["04"])
