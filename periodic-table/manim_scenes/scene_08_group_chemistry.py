"""Why a column shares its chemistry: alkali metals lose one electron, noble gases keep theirs.

The alkali atoms are drawn to scale from their covalent radii (Cordero et al.,
2008); the closed core is a shaded 3D sphere and the lone outer electron sits
in a soft cloud around it. The noble-gas sizes are schematic.
"""

from manim_scenes.common import *

ALKALI = ("Li", "Na", "K")
NOBLE = ("Ne", "Ar", "Kr")
X = (-4.7, 0.0, 4.7)
ATOM_Y = 0.55
SCALE = 0.0095  # display units per picometre


class Scene08GroupChemistry(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _core(radius: float, color: str) -> Sphere:
    core = Sphere(radius=radius, resolution=(12, 24))
    core.set_fill(color, opacity=1).set_stroke(width=0)
    return core


def _alkali(symbol: str, x: float) -> VGroup:
    outer = pm.COVALENT_RADII_PM[symbol] * SCALE
    centre = np.array([x, ATOM_Y, 0])
    cloud = electron_cloud(outer, cfg.ELECTRON_COLOR, opacity=0.16).move_to(centre)
    rim = Circle(radius=outer, stroke_color=cfg.CYAN, stroke_width=2, stroke_opacity=0.35).move_to(centre)
    core = _core(outer * 0.45, cfg.GREEN).move_to(centre)
    angle = 40 * DEGREES
    electron = glow_dot(centre + outer * 0.82 * np.array([np.cos(angle), np.sin(angle), 0]), 0.13)
    label = txt(symbol, cfg.FONT["section"], cfg.WHITE).move_to([x, -2.0, 0])
    atom = VGroup(cloud, rim, core, electron, label)
    atom.cloud, atom.rim, atom.core, atom.electron, atom.label, atom.outer = cloud, rim, core, electron, label, outer
    return atom


def _noble(symbol: str, x: float, radius: float) -> VGroup:
    centre = np.array([x, ATOM_Y, 0])
    core = _core(radius * 0.45, cfg.GREEN).move_to(centre)
    shell = Sphere(radius=radius, resolution=(12, 24)).move_to(centre)
    shell.set_fill(cfg.GREEN, opacity=0.16).set_stroke(width=0)
    rim = VGroup(
        Circle(radius=radius, stroke_color=cfg.GREEN, stroke_width=10, stroke_opacity=0.15),
        Circle(radius=radius, stroke_color=cfg.GREEN, stroke_width=3.5),
    ).move_to(centre)
    label = txt(symbol, cfg.FONT["section"], cfg.WHITE).move_to([x, -2.0, 0])
    atom = VGroup(shell, core, rim, label)
    atom.shell, atom.core, atom.rim, atom.label, atom.radius = shell, core, rim, label, radius
    return atom


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "08", "One outer electron")

    atoms = [_alkali(sym, x) for sym, x in zip(ALKALI, X)]
    scene.play(LaggedStart(*[AnimationGroup(FadeIn(a.cloud, scale=0.6), FadeIn(a.rim), FadeIn(a.core, scale=0.5),
                                            FadeIn(a.label, shift=UP * 0.2)) for a in atoms], lag_ratio=0.35),
               run_time=2.4)
    sizes = VGroup(*[txt(f"{pm.COVALENT_RADII_PM[s]} pm", cfg.FONT["tiny"], cfg.MUTED).next_to(a.label, DOWN, buff=0.2)
                     for s, a in zip(ALKALI, atoms)])
    to_scale = txt("relative covalent sizes", cfg.FONT["tiny"], cfg.MUTED).move_to(DOWN * 3.55)
    scene.play(FadeIn(sizes), FadeIn(to_scale), run_time=0.6)

    beat(scene, t, 1)
    scene.play(LaggedStart(*[FadeIn(a.electron, scale=0.4) for a in atoms], lag_ratio=0.3), run_time=1.2)
    rings = VGroup(*[Circle(radius=0.32, stroke_color=cfg.GOLD, stroke_width=4).move_to(a.electron) for a in atoms])
    scene.play(Create(rings), run_time=0.8)
    core_tags = VGroup(*[txt("closed core", cfg.FONT["tiny"], cfg.GREEN).move_to(a.core.get_center() + DOWN * (a.core.height / 2 + 0.28))
                         for a in atoms])
    scene.play(FadeIn(core_tags), *[Indicate(a.core, color=cfg.GREEN) for a in atoms], run_time=1.2)

    # --- Held loosely --------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(rings), FadeOut(core_tags), run_time=0.5)
    tugs = []
    for a in atoms:
        direction = a.electron.get_center() - a.core.get_center()
        tugs.append(a.electron.animate(rate_func=there_and_back).shift(direction / np.linalg.norm(direction) * 0.45))
    scene.play(*tugs, run_time=1.4)
    scene.play(*[a.electron.animate(rate_func=there_and_back).shift(UR * 0.3) for a in atoms], run_time=1.2)

    # --- Each becomes a positive ion -----------------------------------------
    beat(scene, t, 3)
    ions = []
    for symbol, a in zip(ALKALI, atoms):
        away = a.electron.get_center() + UR * 1.4
        ion_label = VGroup(txt(symbol, cfg.FONT["section"], cfg.WHITE), txt("+", cfg.FONT["label"], cfg.GOLD))
        ion_label.arrange(RIGHT, buff=0.06, aligned_edge=UP).move_to(a.label)
        scene.play(a.electron.animate.move_to(away).set_opacity(0), FadeOut(a.cloud), FadeOut(a.rim),
                   ReplacementTransform(a.label, ion_label), run_time=1.1)
        ions.append(ion_label)
        a.label = ion_label

    beat(scene, t, 4)
    reaction = eq(r"\mathrm{M}\ \rightarrow\ \mathrm{M}^{+}\ +\ e^{-}", cfg.FONT["title"], cfg.WHITE).move_to(DOWN * 3.5)
    scene.play(FadeOut(sizes), FadeOut(to_scale), Write(reaction), run_time=1.4)
    scene.play(Indicate(reaction, color=cfg.GOLD, scale_factor=1.06), run_time=1.2)

    # --- Water: fizzing, more violent going down --------------------------------
    beat(scene, t, 5)
    water = txt("Water → hydrogen gas", cfg.FONT["small"], cfg.CYAN).move_to(DOWN * 4.08)
    scene.play(ReplacementTransform(reaction, water), run_time=0.7)
    bubbles = VGroup()
    rises = []
    for index, a in enumerate(atoms):
        count = (3, 7, 13)[index]
        for k in range(count):
            r = 0.05 + 0.02 * ((k * 7) % 4)
            start_point = a.core.get_center() + np.array([((k * 37) % 11 - 5) * 0.12, -0.2, 0])
            bubble = Circle(radius=r, stroke_color=cfg.CYAN, stroke_width=2, fill_color=cfg.CYAN,
                            fill_opacity=0.15).move_to(start_point)
            bubbles.add(bubble)
            rises.append(bubble.animate(rate_func=linear).shift(UP * (1.6 + 0.4 * index)).set_opacity(0))
    scene.play(LaggedStart(*rises, lag_ratio=0.06), run_time=4.4)
    scene.remove(bubbles)
    trend = Arrow([X[0] - 0.6, -2.85, 0], [X[2] + 0.6, -2.85, 0], buff=0, color=cfg.ORANGE, stroke_width=5)
    violent = VGroup(trend, txt("more vigorous", cfg.FONT["small"], cfg.ORANGE).next_to(trend, UP, buff=0.1))
    violent[1].next_to(trend, DOWN, buff=0.18)
    scene.play(GrowArrow(trend), FadeIn(violent[1]), run_time=0.8)

    # --- Noble gases ----------------------------------------------------------
    beat(scene, t, 6)
    head = swap_heading(scene, head, "A closed outer s + p set")
    scene.play(*[FadeOut(VGroup(a.core, a.label)) for a in atoms], FadeOut(water), FadeOut(violent), run_time=0.8)
    nobles = [_noble(sym, x, r) for sym, x, r in zip(NOBLE, X, (1.15, 1.45, 1.7))]
    scene.play(LaggedStart(*[AnimationGroup(FadeIn(n.core, scale=0.5), FadeIn(n.shell, scale=0.8), Create(n.rim),
                                            FadeIn(n.label, shift=UP * 0.2)) for n in nobles], lag_ratio=0.3),
               run_time=2.2)

    beat(scene, t, 7)
    pattern = eq(r"ns^{2}\,np^{6}", cfg.FONT["title"], cfg.GREEN).move_to(DOWN * 3.35)
    schematic = txt("sizes schematic", cfg.FONT["tiny"], cfg.MUTED).to_corner(DR, buff=0.4)
    scene.play(Write(pattern), FadeIn(schematic), run_time=1.2)
    scene.play(*[Indicate(n.rim, color=cfg.WHITE, scale_factor=1.05) for n in nobles], run_time=1.2)

    # --- Nothing to give, no gap to fill ------------------------------------
    beat(scene, t, 8)
    leaving = glow_dot(nobles[0].core.get_center() + UR * nobles[0].radius * 0.62, 0.12)
    scene.play(FadeIn(leaving, scale=0.4), run_time=0.4)
    scene.play(leaving.animate(rate_func=there_and_back).shift(UR * 0.75), run_time=1.4)
    stays = txt("stays", cfg.FONT["small"], cfg.GREEN).next_to(nobles[0].rim, UP, buff=0.15)
    scene.play(FadeIn(stays), run_time=0.5)
    incoming = glow_dot(np.array([X[1] - 2.4, ATOM_Y + 2.6, 0]), 0.12)
    scene.play(FadeIn(incoming), run_time=0.3)
    path = ArcBetweenPoints(incoming.get_center(), np.array([X[1] + 0.4, ATOM_Y + 2.7, 0]), angle=-PI * 0.9)
    scene.play(MoveAlongPath(incoming, path), run_time=1.6)
    no_gap = txt("next state higher", cfg.FONT["small"], cfg.GREEN).next_to(nobles[1].rim, UP, buff=0.15).shift(RIGHT * 0.9)
    scene.play(FadeOut(incoming), FadeIn(no_gap), run_time=0.6)

    beat(scene, t, 9)
    inert = chip("usually unreactive", cfg.GREEN, cfg.FONT["label"]).move_to(np.array([X[2], ATOM_Y + 2.45, 0]))
    scene.play(FadeIn(inert, scale=1.2), FadeOut(leaving), run_time=0.8)

    # --- Same pattern, similar chemistry --------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(VGroup(stays, no_gap, inert, schematic)), run_time=0.5)
    summary = VGroup(txt("same pattern", cfg.FONT["body"], cfg.GOLD), eq(r"\Rightarrow", cfg.FONT["title"]),
                     txt("similar chemistry", cfg.FONT["body"], cfg.WHITE))
    summary.arrange(RIGHT, buff=0.35).move_to(DOWN * 3.35)
    scene.play(FadeOut(pattern, shift=DOWN * 0.2), FadeIn(summary, shift=UP * 0.2), run_time=1.2)
    scene.play(*[Indicate(n.rim, color=cfg.WHITE, scale_factor=1.04) for n in nobles], run_time=1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["08"])
