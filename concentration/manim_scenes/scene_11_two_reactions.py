"""Scene 11 — one acid stock, two neutralisation stoichiometries.

The structures track proton equivalents, not the full ionic speciation in
water. One equivalent per acid formula unit gives 0.500 N; two give 1.00 N.
The constant 0.500 M label belongs to the original stock before adding base.
"""

from manim_scenes.common import *
from manim_scenes.scene_10_normality import acid_stage
from manim_scenes.stage3d import Ball, Rod

MOLARITY = pm.ACID_MOLARITY
ACID = pm.sulfuric_acid()
# The acidic hydrogen nearest +x leaves first (toward the right-hand hydroxide).
PAIRS = sorted(ACID.acidic, key=lambda i: -ACID.positions[i][0])


class Scene11TwoReactions(Scene):
    def construct(self) -> None:
        play_scene(self)


def hydroxide(stage: Stage, at) -> dict:
    """OH- with a spectator Na+, invisible until faded in."""
    at = np.asarray(at, dtype=float)
    o = Ball(at, 0.36, cfg.ELEMENT_COLORS["O"], "O")
    h = Ball(at + np.array([0.0, -0.75, 0.0]), 0.24, cfg.ELEMENT_COLORS["H"], "H")
    na = Ball(at + np.array([0.0, 1.25, 0.0]), 0.42, cfg.ELEMENT_COLORS["Na"], "Na")
    rod = Rod(o, h, 1, width=11)
    parts = [rod, o, h, na]
    for p in parts:
        p.presence = 0.0
    stage.add_body(*parts)
    return {"o": o, "h": h, "na": na, "parts": parts}


def transfer(stage: Stage, model: dict, index: int, base: dict, **kwargs) -> list[Animation]:
    """Move acidic hydrogen ``index`` onto the hydroxide oxygen: H2O forms."""
    o = base["o"].where()
    target = o + 0.8 * mu.unit(-o + np.array([0.0, 0.5, 0.0]))
    ball = model["balls"][index]
    rod = next(r for r in model["rods"] if r.b is ball or r.a is ball)
    new = Rod(base["o"], ball, 1, width=11)
    new.presence = 0.0
    stage.add_body(new)
    return [move_ball(stage, ball, target, **kwargs), stage.fade(rod, 0.0, **kwargs), stage.fade(new, 1.0, **kwargs)]


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "11", "One acid, two normalities")
    label = eq_chip(rf"\text{{acid stock}}\quad {fx(MOLARITY, 3)}\ \mathrm{{M}}", cfg.WHITE, stroke=cfg.VOLUME).move_to([0, 2.95, 0])
    left, lmodel, lhalos = acid_stage([-4.3, 0.25, 0], zoom=1.28, spin=0.0)
    right, rmodel, rhalos = acid_stage([4.3, 0.25, 0], zoom=1.28, spin=0.0)
    for st in (left, right):
        st.yaw, st.pitch = 0.25, 0.25
    for h in lhalos + rhalos:
        h.presence = 1.0
    scene.play(FadeIn(label, shift=DOWN * 0.2), run_time=0.8)
    show(scene, left, 1.0)
    show(scene, right, 1.0)

    # --- 2. Left: one hydroxide per acid ---------------------------------------------------------------------
    beat(scene, t, 1)
    lbase = hydroxide(left, [1.9, -0.5, 0.3])
    scene.play(*[left.fade(p, 1.0) for p in lbase["parts"]], run_time=1.2)
    one_base = txt("1 NaOH per acid", cfg.FONT["small"], cfg.MUTED).move_to([-4.0, -2.55, 0])
    scene.play(FadeIn(one_base), run_time=0.6)

    # --- 3. The equation ----------------------------------------------------------------------------------------
    beat(scene, t, 2)
    eq_a = eq(pm.REACTIONS["partial"]["tex"], cfg.FONT["small"])
    fit_width(eq_a, 7.3)
    eq_a.move_to([-4.0, -2.55, 0])
    scene.play(FadeOut(one_base), run_time=0.4)
    scene.play(Write(eq_a), run_time=1.4)

    # --- 4. One proton moves; the other stays ------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(*transfer(left, lmodel, PAIRS[0], lbase, run_time=2.4),
               left.fade(lhalos[ACID.acidic.index(PAIRS[0])], 0.0, run_time=2.4))
    kept = lmodel["balls"][PAIRS[1]]
    stays = txt("stays", cfg.FONT["small"], cfg.EQUIVALENT).move_to(left.screen_point(kept.where()) + DOWN * 0.6)
    water = txt("water", cfg.FONT["small"], cfg.SOLVENT).move_to(left.screen_point(lbase["o"].where()) + UP * 0.6 + RIGHT * 0.75)
    scene.play(FadeIn(water), FadeIn(stays), run_time=0.8)

    # --- 5. z = 1: 0.500 N --------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    n_a = eq([r"z = 1", r"\Rightarrow", rf"N = {fx(pm.normality(MOLARITY, 1), 3)}"], cfg.FONT["label"])
    n_a[0].set_color(cfg.EQUIVALENT)
    n_a[2].set_color(cfg.RESULT)
    n_a.move_to([-4.0, -3.45, 0])
    scene.play(Write(n_a), run_time=1.4)

    # --- 6. Right: twice the base ---------------------------------------------------------------------------------------
    beat(scene, t, 5)
    rbase = [hydroxide(right, [1.9, -0.5, 0.3]), hydroxide(right, [-1.9, -0.5, -0.3])]
    scene.play(*[right.fade(p, 1.0) for b in rbase for p in b["parts"]], FadeOut(VGroup(water, stays)), run_time=1.2)
    two_base = txt("2 NaOH per acid", cfg.FONT["small"], cfg.MUTED).move_to([4.0, -2.55, 0])
    scene.play(FadeIn(two_base), run_time=0.6)

    # --- 7. Its equation -----------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    eq_b = eq(pm.REACTIONS["complete"]["tex"], cfg.FONT["small"])
    fit_width(eq_b, 7.3)
    eq_b.move_to([4.0, -2.55, 0])
    scene.play(FadeOut(two_base), run_time=0.4)
    scene.play(Write(eq_b), run_time=1.4)

    # --- 8. Both protons move: z = 2, 1.00 N --------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(*transfer(right, rmodel, PAIRS[0], rbase[0], run_time=2.4),
               *transfer(right, rmodel, PAIRS[1], rbase[1], run_time=2.4),
               *[right.fade(h, 0.0, run_time=2.4) for h in rhalos])
    n_b = eq([r"z = 2", r"\Rightarrow", rf"N = {fx(pm.normality(MOLARITY, 2), 2)}"], cfg.FONT["label"])
    n_b[0].set_color(cfg.EQUIVALENT)
    n_b[2].set_color(cfg.RESULT)
    n_b.move_to([4.0, -3.45, 0])
    scene.play(Write(n_b), run_time=1.4)

    # --- 9. The molarity never moved ---------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    rays = VGroup(glow_line(label.get_left() + LEFT * 0.1, [-4.3, 2.2, 0], cfg.VOLUME, 2.0),
                  glow_line(label.get_right() + RIGHT * 0.1, [4.3, 2.2, 0], cfg.VOLUME, 2.0))
    scene.play(Create(rays), Indicate(label, color=cfg.VOLUME, scale_factor=1.08), run_time=1.4)
    scene.play(Indicate(label, color=cfg.WHITE, scale_factor=1.05), run_time=1.0)

    # --- 10. Same molecules, two normalities -----------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(Indicate(n_a[2], color=cfg.WHITE, scale_factor=1.15), Indicate(n_b[2], color=cfg.WHITE, scale_factor=1.15),
               run_time=1.4)

    # --- 11-13. Two different questions ----------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    hide(scene, left, 0.6, FadeOut(VGroup(eq_a, eq_b, n_a, n_b, rays)))
    hide(scene, right, 0.4)
    rows = VGroup(
        VGroup(txt("molarity", cfg.FONT["body"], cfg.VOLUME), txt("moles per litre", cfg.FONT["body"], cfg.WHITE)),
        VGroup(txt("normality", cfg.FONT["body"], cfg.EQUIVALENT), txt("equivalents per litre", cfg.FONT["body"], cfg.WHITE)),
    )
    for row in rows:
        row.arrange(RIGHT, buff=0.6)
    rows.arrange(DOWN, buff=0.8, aligned_edge=LEFT).move_to([0, 0.2, 0])
    scene.play(FadeIn(rows[0], shift=RIGHT * 0.2), run_time=1.0)
    beat(scene, t, 11)
    scene.play(FadeIn(rows[1], shift=RIGHT * 0.2), run_time=1.0)
    beat(scene, t, 12)
    which = result_label("…for which reaction?", cfg.GOLD, cfg.FONT["body"]).next_to(rows, DOWN, buff=0.7)
    scene.play(FadeIn(which, shift=UP * 0.15), run_time=1.0)

    # --- 14. "1 N" on a bottle ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    bottle_label = eq_chip(r"1\ \mathrm{N}\ \ \mathrm{H_2SO_4}", cfg.WHITE, stroke=cfg.EQUIVALENT)
    scene.play(FadeOut(rows), which.animate.move_to([0, -1.2, 0]), FadeOut(label), run_time=0.8)
    bottle_label.move_to([0, 0.6, 0])
    scene.play(FadeIn(bottle_label, scale=1.1), run_time=0.9)
    scene.play(Indicate(which, color=cfg.WHITE, scale_factor=1.06), run_time=1.2)

    # --- 15. A crowd of molecules next ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 14)
    scene.play(FadeOut(VGroup(bottle_label, which)), run_time=0.7)
    crowd = Stage([0, -0.3, 0], zoom=1.0, yaw=0.3, pitch=0.35, spin=0.25, sway=0.08)
    Swarm(crowd, Box(half=2.0), solvent=100, solute=1, seed=cfg.SEED + 11, style="spheres", solvent_radius=0.11,
          solute_radius=0.17, amplitude=0.1)
    show(scene, crowd, 1.6)
    scene.play(crowd.zoom_to(1.35), run_time=11.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["11"])
