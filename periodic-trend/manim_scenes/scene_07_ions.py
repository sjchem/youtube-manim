"""Ionic radius: sodium loses its outer shell and shrinks; fluorine gains an
electron and swells.

Both atoms and both ions share one screen scale (NCERT atomic and ionic
radii). A dashed ring keeps each neutral atom's size on screen. The two
measuring conventions are named on screen, not hidden.
"""

from manim_scenes.common import *

SCALE = 0.0105
NA_AT = np.array([-3.7, 0.45, 0])
F_AT = np.array([3.7, 0.45, 0])
NAME_Y = -2.3
COUNT_Y = -3.22


class Scene07Ions(Scene):
    def construct(self) -> None:
        play_scene(self)


def size(key: str) -> float:
    pm_value = ed.IONIC_RADII_PM[key] if key in ed.IONIC_RADII_PM else ed.ATOMIC_RADII_PM[key]
    return pm_value * SCALE


def ring(radius: float, at) -> DashedVMobject:
    return DashedVMobject(Circle(radius=radius, stroke_color=cfg.MUTED, stroke_width=3, stroke_opacity=0.8),
                          num_dashes=48).move_to(at)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "07", "Losing an electron")

    # --- 1. Sodium: one loosely held outer electron -------------------------------------------
    sodium = Atom(size("Na"), NA_AT, charge="+11", core=size("Na+"), count=170, core_count=360, seed=71,
                  nucleus_radius=0.32, glow=0.1)
    name = eq(r"\mathrm{Na}", cfg.FONT["section"], cfg.BLUE).move_to([NA_AT[0], NAME_Y, 0])
    counts = txt("11 protons · 11 electrons", cfg.FONT["small"], cfg.MUTED).move_to([NA_AT[0], COUNT_Y, 0])
    scene.play(FadeIn(sodium, scale=0.6), FadeIn(name), run_time=1.2)
    scene.play(FadeIn(counts, shift=UP * 0.1), run_time=0.7)

    head = dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    spot = NA_AT + size("Na") * 0.8 * np.array([np.cos(0.7), np.sin(0.7), 0])
    electron = glow_dot(spot, 0.15)
    scene.play(FadeIn(electron, scale=0.4), run_time=0.6)
    zap = chip("+ energy", cfg.GOLD, cfg.FONT["small"]).move_to(spot + np.array([0.6, 1.3, 0]))
    scene.play(FadeIn(zap, scale=1.2), Flash(spot, color=cfg.GOLD, flash_radius=0.45), run_time=0.9)
    _, path = escape_electron(spot, np.array([0.3, 3.1, 0]))
    scene.play(MoveAlongPath(electron, path), FadeOut(zap), run_time=1.4, rate_func=rush_into)

    # --- 2. The equation ---------------------------------------------------------------------
    beat(scene, t, 2)
    reaction = eq(r"\mathrm{Na} \;\rightarrow\; \mathrm{Na}^{+} + e^{-}", cfg.FONT["label"], cfg.WHITE)
    reaction.move_to([NA_AT[0], 3.0, 0])
    scene.play(Write(reaction), FadeOut(electron), run_time=1.2)

    # --- 3. Dramatically smaller --------------------------------------------------------------
    beat(scene, t, 3)
    was = ring(size("Na"), NA_AT)
    ion_name = eq(r"\mathrm{Na}^{+}", cfg.FONT["section"], cfg.CATION).move_to(name)
    scene.add(was)
    scene.play(sodium.cloud.fade_to(0), FadeThrough(name, ion_name), run_time=1.6)
    name = ion_name
    smaller = chip("much smaller", cfg.GOLD, cfg.FONT["small"]).move_to([0.5, 1.9, 0])
    scene.play(FadeIn(smaller, scale=1.1), Indicate(was, color=cfg.WHITE, scale_factor=1.0), run_time=1.0)

    # --- 4. The numbers ---------------------------------------------------------------------
    beat(scene, t, 4)
    na_values = VGroup(txt(f"{ed.ATOMIC_RADII_PM['Na']} pm", cfg.FONT["label"], cfg.MUTED), eq(r"\rightarrow", cfg.FONT["label"]),
                       txt(f"{ed.IONIC_RADII_PM['Na+']} pm", cfg.FONT["label"], cfg.WHITE)).arrange(RIGHT, buff=0.3)
    na_values.move_to([NA_AT[0], COUNT_Y, 0])
    scene.play(*fade_labels(counts, na_values), run_time=0.9)

    # --- 5. Why: the outer shell is gone, 11 protons hold 10 electrons -------------------------------
    beat(scene, t, 5)
    gone = chip("outer shell gone", cfg.CYAN, cfg.FONT["small"])
    hold = chip("11 protons · 10 electrons", cfg.PROTON_COLOR, cfg.FONT["small"])
    reasons = VGroup(gone, hold).arrange(DOWN, buff=0.22).move_to([0.6, 0.45, 0])
    scene.play(FadeOut(smaller), FadeIn(gone, shift=LEFT * 0.2), run_time=0.8)
    arrows = pull_arrows(NA_AT, size("Na+"), pm.slater_zeff(11, 10), count=8)
    scene.play(FadeIn(hold, shift=LEFT * 0.2), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08),
               run_time=1.2)
    scene.play(*sodium.resize(size("Na"), size("Na+") * 0.92), run_time=1.2, rate_func=there_and_back)

    # --- 6. Fluorine gains an electron ---------------------------------------------------------------
    beat(scene, t, 6)
    head = swap_heading(scene, head, "Gaining an electron")
    scene.play(FadeOut(reasons), FadeOut(arrows), FadeOut(reaction), run_time=0.6)
    fluorine = Atom(size("F"), F_AT, charge="+9", core=0.16, count=420, core_count=90, seed=72, nucleus_radius=0.28,
                    glow=0.2)
    f_name = eq(r"\mathrm{F}", cfg.FONT["section"], cfg.GREEN).move_to([F_AT[0], NAME_Y, 0])
    f_counts = txt("9 protons · 9 electrons", cfg.FONT["small"], cfg.MUTED).move_to([F_AT[0], COUNT_Y, 0])
    scene.play(FadeIn(fluorine, scale=0.6), FadeIn(f_name), FadeIn(f_counts), run_time=1.2)
    f_reaction = eq(r"\mathrm{F} + e^{-} \;\rightarrow\; \mathrm{F}^{-}", cfg.FONT["label"], cfg.WHITE)
    f_reaction.move_to([F_AT[0], 3.0, 0])
    scene.play(Write(f_reaction), run_time=1.1)

    # --- 7. Nine protons, ten electrons: the cloud swells ----------------------------------------------
    beat(scene, t, 7)
    newcomer = glow_dot(np.array([0.6, 2.4, 0]), 0.15)
    arrive = ArcBetweenPoints(np.array([0.6, 2.4, 0]), F_AT + np.array([-0.5, 0.35, 0]), angle=PI / 3)
    scene.play(FadeIn(newcomer, scale=0.4), run_time=0.4)
    scene.play(MoveAlongPath(newcomer, arrive), run_time=1.3, rate_func=rush_from)
    f_was = ring(size("F"), F_AT)
    f_ion_name = eq(r"\mathrm{F}^{-}", cfg.FONT["section"], cfg.ANION).move_to(f_name)
    f_new_counts = txt("9 protons · 10 electrons", cfg.FONT["small"], cfg.WHITE).move_to(f_counts)
    scene.add(f_was)
    pushes = VGroup(*[Arrow(F_AT + 0.75 * d, F_AT + 1.55 * d, buff=0, color=cfg.ANION, stroke_width=6, tip_length=0.2)
                      for d in (UR, UL, DL, DR)])
    scene.play(FadeOut(newcomer, scale=0.5), *fluorine.resize(size("F-")), FadeThrough(f_name, f_ion_name),
               FadeThrough(f_counts, f_new_counts), LaggedStart(*[GrowArrow(p) for p in pushes], lag_ratio=0.1),
               run_time=2.2)
    f_name, f_counts = f_ion_name, f_new_counts
    repel = chip("more electron repulsion", cfg.ANION, cfg.FONT["small"]).move_to([0.6, 0.45, 0])
    scene.play(FadeIn(repel, scale=1.1), run_time=0.8)

    # --- 8. The numbers --------------------------------------------------------------------------------
    beat(scene, t, 8)
    f_values = VGroup(txt(f"{ed.ATOMIC_RADII_PM['F']} pm", cfg.FONT["label"], cfg.MUTED), eq(r"\rightarrow", cfg.FONT["label"]),
                      txt(f"{ed.IONIC_RADII_PM['F-']} pm", cfg.FONT["label"], cfg.WHITE)).arrange(RIGHT, buff=0.3)
    f_values.move_to([F_AT[0], COUNT_Y, 0])
    scene.play(*fade_labels(f_counts, f_values), FadeOut(pushes), run_time=0.9)
    scene.play(Indicate(f_was, color=cfg.WHITE, scale_factor=1.0), run_time=1.0)

    # --- 9. An honest note --------------------------------------------------------------------------------
    beat(scene, t, 9)
    note = VGroup(txt('Atomic: bonded atoms', cfg.FONT["tiny"], cfg.CYAN),
                  txt('Ionic: crystals', cfg.FONT["tiny"], cfg.PURPLE)).arrange(RIGHT, buff=0.75)
    note.move_to([0, -3.95, 0])
    scene.play(FadeOut(repel), FadeOut(f_reaction), na_values.animate.shift(UP * 0.25), f_values.animate.shift(UP * 0.25),
               name.animate.shift(UP * 0.25), f_name.animate.shift(UP * 0.25), run_time=0.6)
    scene.play(FadeIn(note, shift=UP * 0.1), run_time=0.9)
    pattern = chip('Different radius conventions', cfg.WHITE, cfg.FONT["small"]).move_to([0, 3.0, 0])
    scene.play(FadeIn(pattern, shift=DOWN * 0.15), run_time=0.8)

    # --- 10. The rule --------------------------------------------------------------------------------------
    beat(scene, t, 10)
    rule = VGroup(txt("lose electrons → shrink", cfg.FONT["body"], cfg.GOLD),
                  txt("gain electrons → swell", cfg.FONT["body"], cfg.CYAN)).arrange(RIGHT, buff=1.4).move_to([0, 3.0, 0])
    fit_width(rule, 13.4)
    scene.play(*fade_labels(pattern, rule), run_time=0.9)
    scene.play(Indicate(rule[0], color=cfg.WHITE, scale_factor=1.05), Indicate(rule[1], color=cfg.WHITE, scale_factor=1.05),
               run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["07"])
