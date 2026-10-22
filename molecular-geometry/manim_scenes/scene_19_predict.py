"""Chapter 19 — predict the shape yourself: SO2, PF3, BrF3.

Each question shows only the Lewis structure and a countdown ring, so the
viewer has a few seconds to guess. The reveal follows the recipe strip at
the top: count the regions, show the electron geometry (lobes), hide the
lone pairs, name the shape. Every answer is the library molecule — its
lone-pair count comes from valence electrons, its angle from measured data —
and the closing line-up puts BF3, PF3 and BrF3 side by side.
"""

from manim_scenes.common import *

LEWIS_AT = np.array([-4.3, 0.1, 0])
MODEL_AT = np.array([3.0, 0.25, 0])
STEPS = ("Lewis structure", "count regions", "electron geometry", "hide lone pairs")


class Scene19Predict(Scene):
    def construct(self) -> None:
        play_scene(self)


def recipe_strip() -> VGroup:
    chips = [chip(s, cfg.CYAN, cfg.FONT["small"]) for s in STEPS]
    parts = []
    for k, c in enumerate(chips):
        parts.append(c)
        if k < len(chips) - 1:
            parts.append(eq(r"\rightarrow", cfg.FONT["small"], cfg.MUTED))
    strip = VGroup(*parts).arrange(RIGHT, buff=0.18)
    fit_width(strip, 15.2)
    strip.move_to([0, 3.35, 0])
    strip.chips = chips
    return strip


def countdown(at) -> VGroup:
    ring = Circle(radius=0.85, stroke_color=cfg.GOLD, stroke_width=8).rotate(PI / 2).flip(UP).move_to(at)
    mark = txt("?", 110, cfg.GOLD).move_to(at)
    return VGroup(ring, mark)


def question(scene: Scene, t: float, strip: VGroup, number: int, key: str, lewis: Lewis, hint_beat: int,
             reveal_beat: int, view: dict, orient=None) -> tuple[Stage, MoleculeModel, list]:
    """Pose a question, run the countdown, and reveal the electron geometry."""
    mol = ml.molecule(key)
    badge = chip(f"Question {number} of 3", cfg.GOLD, cfg.FONT["label"]).move_to([-4.3, 2.45, 0])
    name = formula(key, cfg.FONT["section"]).move_to([-4.3, -2.9, 0])
    scene.play(FadeIn(badge, shift=DOWN * 0.1), Write(lewis), FadeIn(name), run_time=1.6)
    scene.play(Indicate(strip.chips[0], color=cfg.WHITE, scale_factor=1.08), run_time=0.8)
    beat(scene, t, hint_beat)
    timer = countdown(MODEL_AT + UP * 0.3)
    scene.play(FadeIn(timer[1], scale=0.6), run_time=0.4)
    scene.play(Create(timer[0]), run_time=3.0, rate_func=linear)
    beat(scene, t, reveal_beat)
    stage = Stage(MODEL_AT, zoom=0.85, **view)
    model = MoleculeModel(stage, mol, domains=True, orient=orient)
    count = VGroup(chip(f"{mol.regions} regions", cfg.CYAN, cfg.FONT["label"]),
                   txt(mol.electron_geometry, cfg.FONT["body"], cfg.CYAN)).arrange(DOWN, buff=0.25)
    count.move_to([MODEL_AT[0], -2.85, 0])
    scene.play(FadeOut(timer), Indicate(strip.chips[1], color=cfg.WHITE, scale_factor=1.08), run_time=0.8)
    show(scene, stage, 1.0, FadeIn(count[0]))
    scene.play(Indicate(strip.chips[2], color=cfg.WHITE, scale_factor=1.08), FadeIn(count[1]), run_time=1.0)
    return stage, model, [badge, name, count, lewis]


def answer(scene: Scene, strip: VGroup, stage: Stage, model: MoleculeModel, key: str, extras: list,
           arc_pair: tuple[int, int] | None, angle_key: str | None) -> VGroup:
    """Hide the lone pairs and name the shape, with its measured angle."""
    mol = ml.molecule(key)
    scene.play(*model.show_lone_pairs(0.0), *model.fade("domains", 0.0), *model.fade("guides", 0.0),
               Indicate(strip.chips[3], color=cfg.WHITE, scale_factor=1.08), run_time=1.4)
    shape = shape_name(mol.shape, size=cfg.FONT["section"]).move_to([MODEL_AT[0], -2.85, 0])
    anims = [fade_through(extras[2], shape)]
    if arc_pair:
        value = gd.BOND_ANGLE_DEG[angle_key] if angle_key in gd.BOND_ANGLE_DEG else model.angle(*arc_pair)
        arc = model.arc(*arc_pair, radius=1.05, label=degrees_label(value, cfg.FONT["body"]), label_gap=0.55)
        anims.append(stage.fade(arc, 1.0))
    scene.play(*anims, run_time=1.2)
    scene.remove(extras[2])
    return shape


def clear(scene: Scene, stage: Stage, *mobs: Mobject) -> None:
    hide(scene, stage, 0.7, *[FadeOut(m) for m in mobs])


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "19", "Predict the shape")
    dismiss_opening_title(scene, t, head, at=1.6)
    strip = recipe_strip()
    scene.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.15) for p in strip], lag_ratio=0.2), run_time=2.4)

    # --- Question 1: sulfur dioxide ----------------------------------------------------------------------------------
    beat(scene, t, 1)
    so2 = ml.molecule("SO2")
    lewis = Lewis("S", [("O", 205, 2), ("O", 335, 2)], central_lone=[90], at=LEWIS_AT, bond=1.8, size=88,
                  ligand_size=76)
    stage, model, extras = question(scene, t, strip, 1, "SO2", lewis, 2, 3, dict(yaw=0.2, pitch=0.25, sway=0.12),
                                    orient=bisect_down(so2.sites[1].direction, so2.sites[2].direction))
    beat(scene, t, 4)
    shape = answer(scene, strip, stage, model, "SO2", extras, (1, 2), "SO2")

    # --- Question 2: phosphorus trifluoride -----------------------------------------------------------------------------
    beat(scene, t, 5)
    clear(scene, stage, shape, *extras[:2], extras[3])
    lewis = Lewis("P", [("F", 180, 1), ("F", 0, 1), ("F", 270, 1)], central_lone=[90], at=LEWIS_AT, bond=1.7, size=88,
                  ligand_size=72)
    stage, model, extras = question(scene, t, strip, 2, "PF3", lewis, 6, 7, dict(yaw=0.5, pitch=0.3, sway=0.12))
    shape = answer(scene, strip, stage, model, "PF3", extras, (1, 2), "PF3")

    # --- Question 3: bromine trifluoride ---------------------------------------------------------------------------------
    beat(scene, t, 8)
    clear(scene, stage, shape, *extras[:2], extras[3])
    brf3 = ml.molecule("BrF3")
    lewis = Lewis("Br", [("F", 180, 1), ("F", 0, 1), ("F", 270, 1)], central_lone=[55, 125], at=LEWIS_AT, bond=1.8,
                  size=88, ligand_size=72)
    badge = chip("Question 3 of 3", cfg.GOLD, cfg.FONT["label"]).move_to([-4.3, 2.45, 0])
    name = formula("BrF3", cfg.FONT["section"]).move_to([-4.3, -2.9, 0])
    scene.play(FadeIn(badge, shift=DOWN * 0.1), Write(lewis), FadeIn(name), run_time=1.6)
    beat(scene, t, 9)
    stage = Stage(MODEL_AT, zoom=0.85, yaw=0.5, pitch=0.3, sway=0.12)
    model = MoleculeModel(stage, brf3, guides=True, lone_pairs=False)
    for i in model.bonded():
        model.atoms[i].presence = model.rods[i].presence = 0.0
    five = chip(f"{brf3.regions} regions", cfg.CYAN, cfg.FONT["label"]).move_to([MODEL_AT[0], -2.85, 0])
    show(scene, stage, 1.0, FadeIn(five), Indicate(strip.chips[1], color=cfg.WHITE, scale_factor=1.08))
    beat(scene, t, 10)
    timer = countdown(MODEL_AT + RIGHT * 3.0)
    hint = caption("Think back to the equator", cfg.PURPLE)
    scene.play(FadeIn(timer[1], scale=0.6), FadeIn(hint), run_time=0.4)
    scene.play(Create(timer[0]), run_time=3.0, rate_func=linear)
    beat(scene, t, 11)
    scene.play(FadeOut(timer), FadeOut(hint), *model.fade("atoms", 1.0), *model.fade("rods", 1.0),
               *model.show_lone_pairs(1.0), *stage.turn(yaw=-np.pi / 2, pitch=0.15), run_time=1.8)
    shape = shape_name(brf3.shape, size=cfg.FONT["section"]).move_to([MODEL_AT[0], -2.85, 0])
    scene.play(*model.show_lone_pairs(0.0), *model.fade("guides", 0.0), fade_through(five, shape),
               Indicate(strip.chips[3], color=cfg.WHITE, scale_factor=1.08), run_time=1.4)
    scene.remove(five)

    # --- The three trifluorides side by side ------------------------------------------------------------------------------
    beat(scene, t, 12)
    clear(scene, stage, shape, badge, name, lewis, strip)
    keys = ("BF3", "PF3", "BrF3")
    minis, mini_models = [], []
    for k, key in enumerate(keys):
        small, mini = mini_model(key, [(k - 1) * 4.6, 1.2, 0], zoom=0.66, lone_pairs=0.0,
                              yaw=-np.pi / 2 if key == "BrF3" else 0.5, pitch=0.25, spin=0.0)
        small.sway = 0.2
        minis.append(small)
        mini_models.append(mini)
        scene.add(small)
    names = VGroup(*[formula(key, cfg.FONT["section"]).move_to([(k - 1) * 4.6, -1.2, 0]) for k, key in enumerate(keys)])
    scene.play(*[m.fade(m, 1.0) for m in minis], FadeIn(names), run_time=1.4)
    beat(scene, t, 13)
    three = top_caption("Three fluorines around one central atom", cfg.WHITE)
    scene.play(FadeIn(three), run_time=1.0)
    beat(scene, t, 14)
    shapes = VGroup()
    for k, key in enumerate(keys):
        mol = ml.molecule(key)
        lone = len(mol.lone_pairs)
        shapes.add(VGroup(shape_name(mol.shape, size=cfg.FONT["body"]),
                          txt(f"{lone} lone pair" + ("" if lone == 1 else "s"), cfg.FONT["label"], cfg.PURPLE))
                   .arrange(DOWN, buff=0.25).move_to([(k - 1) * 4.6, -2.45, 0]))
    scene.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in shapes], lag_ratio=0.35), run_time=2.0)
    scene.play(*[a for mini in mini_models for a in mini.show_lone_pairs(0.7)], run_time=1.2)

    # --- You predicted them ---------------------------------------------------------------------------------------------------
    beat(scene, t, 15)
    predicted = caption("Not memorised. Predicted, by counting electrons.", cfg.GREEN)
    scene.play(fade_through(three, predicted), run_time=1.0)
    scene.remove(three)
    scene.play(*[m.set_spin(0.3) for m in minis], run_time=2.6)
    scene.play(Indicate(predicted, color=cfg.WHITE, scale_factor=1.04), run_time=1.4)
    end_scene(scene, t, cfg.SCENE_DURATIONS["19"])
