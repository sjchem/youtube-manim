"""Scene 18 — dilution as conservation: 100 mL of 2.00 M stock is poured into
a 500 mL volumetric flask and made up to the mark. The same twenty gold
particles (a picture: one bead per 0.0100 mol) travel from one flask to the
other and spread out; none vanish, none appear. M1 V1 = M2 V2 follows.
"""

from manim_scenes.common import *

D = pm.DILUTION
M2 = pm.dilute(D["M1"], D["V1_mL"], D["V2_mL"])
N_MOL = D["M1"] * D["V1_mL"] / 1000
SMALL = pm.flask_profile(bulb=0.85, neck=0.17, neck_top=3.2, mark_y=2.6, capacity=D["V1_mL"])
BIG = pm.flask_profile(bulb=1.6, neck=0.27, neck_top=5.0, mark_y=4.2, capacity=D["V2_mL"])
BEADS = 20
RX = 4.95


class Scene18Dilution(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "18", "Dilution")
    stage = Stage([-1.9, -3.65, 0], zoom=0.95, yaw=0.0, pitch=0.25, spin=0.0, sway=0.05)
    small = Glassware(stage, SMALL, origin=[-4.0, 0, 0], volume=D["V1_mL"], mark=True)
    big = Glassware(stage, BIG, origin=[2.4, 0, 0], volume=0.0, mark=True)
    stock = Swarm(stage, small, solvent=110, solute=BEADS, seed=cfg.SEED + 18, solute_radius=0.11, amplitude=0.05)
    stock.target = big
    added = Swarm(stage, big, solvent=420, solute=0, seed=cfg.SEED + 81, amplitude=0.06)
    added.solvent_alpha = 0.0
    show(scene, stage, 1.4)

    # --- 2. 100 mL of 2.00 M stock -------------------------------------------------------------------------------
    beat(scene, t, 1)
    label = VGroup(txt("stock", cfg.FONT["label"], cfg.WHITE),
                   eq(rf"{D['V1_mL']:.0f}\ \mathrm{{mL}},\ {fx(D['M1'], 2)}\ \mathrm{{M}}", cfg.FONT["body"], cfg.VOLUME))
    label.arrange(DOWN, buff=0.12)
    fit_width(label, 3.4)
    label.move_to([-5.6, 1.2, 0])
    scene.play(FadeIn(label, shift=DOWN * 0.15), small.set_glow(1.0), run_time=1.0)

    # --- 3. 0.200 mol: the particles we follow ----------------------------------------------------------------------------
    beat(scene, t, 2)
    moles = eq(rf"n = {fx(D['M1'], 2)} \times {fx(D['V1_mL'] / 1000, 3)} = {fx(N_MOL, 3)}\ \mathrm{{mol}}", cfg.FONT["body"],
               cfg.AMOUNT)
    fit_width(moles, 7.0)
    moles.move_to([-3.4, 2.6, 0])
    scene.play(small.set_glow(0.0), set_attr(stage, stock, "solute_glow", 1.4), Write(moles), run_time=1.6)
    picture = txt(f"{BEADS} particles · a picture", cfg.FONT["small"], cfg.SOLUTE).next_to(label, DOWN, buff=0.25)
    scene.play(FadeIn(picture), run_time=0.7)

    # --- 4. Pour into the 500 mL flask, fill to the mark -----------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(picture), set_attr(stage, stock, "transfer", 1.0), small.set_volume(0.0), big.set_volume(D["V1_mL"]),
               run_time=3.2)
    scene.play(big.set_volume(D["V2_mL"]), set_attr(stage, added, "solvent_alpha", 1.0), big.set_attr("mark_glow", 1.0),
               run_time=3.6)

    # --- 5. Not one vanishes, not one appears --------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(big.set_attr("mark_glow", 0.0), set_attr(stage, added, "solvent_alpha", 0.35), run_time=1.0)
    count = VGroup(txt(f"still {BEADS} particles", cfg.FONT["body"], cfg.SOLUTE),
                   txt("none vanish · none appear", cfg.FONT["small"], cfg.RESULT)).arrange(DOWN, buff=0.28)
    count.move_to([RX, 1.3, 0])
    fit_width(count, 4.9)
    scene.play(FadeIn(count[0], shift=LEFT * 0.2), Indicate(label, color=cfg.MUTED), run_time=1.0)
    scene.play(FadeIn(count[1]), set_attr(stage, stock, "solute_glow", 2.2), run_time=1.0)
    scene.play(set_attr(stage, stock, "solute_glow", 1.2), set_attr(stage, added, "solvent_alpha", 1.0), run_time=1.0)

    # --- 6. 0.200 mol in 0.500 L = 0.400 M --------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    after = numbers_fraction(rf"{fx(N_MOL, 3)}\ \mathrm{{mol}}", rf"{fx(D['V2_mL'] / 1000, 3)}\ \mathrm{{L}}",
                             rf"{fx(M2, 3)}\ \mathrm{{M}}", cfg.AMOUNT, cfg.VOLUME, cfg.FONT["section"])
    fit_width(after, 4.9)
    after.move_to([RX, -0.6, 0])
    scene.play(Write(after), big.set_glow(1.0), run_time=1.6)

    # --- 7. Moles before = moles after: M1 V1 = M2 V2 --------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(VGroup(count, after, moles, label)), big.set_glow(0.0), run_time=0.7)
    steps = VGroup(eq(r"n_{\text{before}} = n_{\text{after}}", cfg.FONT["section"], cfg.AMOUNT),
                   eq(r"n = M \times V", cfg.FONT["body"], cfg.WHITE),
                   eq([r"M_1 V_1", "=", r"M_2 V_2"], cfg.FONT["title"], cfg.WHITE)).arrange(DOWN, buff=0.45)
    steps[2][0].set_color(cfg.GOLD)
    steps[2][2].set_color(cfg.GOLD)
    for s in steps:
        fit_width(s, 4.9)
    steps.move_to([RX, 0.6, 0])
    scene.play(Write(steps[0]), run_time=1.2)
    scene.play(FadeIn(steps[1], shift=UP * 0.15), run_time=0.8)
    scene.play(Write(steps[2]), run_time=1.3)

    # --- 8. 2.00 x 100 / 500 = 0.400 M ------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    nums = eq([rf"M_2 = \frac{{{fx(D['M1'], 2)} \times {D['V1_mL']:.0f}}}{{{D['V2_mL']:.0f}}}", "=", rf"{fx(M2, 3)}\ \mathrm{{M}}"],
              cfg.FONT["section"])
    nums[2].set_color(cfg.RESULT)
    fit_width(nums, 4.5)
    nums_box = boxed(nums).move_to([RX, -2.4, 0])
    scene.play(FadeIn(nums_box, scale=1.06), run_time=1.4)

    # --- 9. Conservation, not a rule to memorise ---------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    conserve = VGroup(txt("conservation", cfg.FONT["section"], cfg.RESULT),
                      txt("nothing reacts or escapes", cfg.FONT["small"], cfg.MUTED)).arrange(DOWN, buff=0.15)
    conserve.move_to([-3.4, 2.5, 0])
    scene.play(FadeIn(conserve, shift=DOWN * 0.15), Indicate(steps[0], color=cfg.WHITE), run_time=1.2)

    # --- 10. Five times the volume, one fifth the concentration ---------------------------------------------------------------------------------
    beat(scene, t, 9)
    fifth = result_label("5 × the volume  →  ⅕ the concentration", cfg.GOLD, cfg.FONT["label"]).move_to([-1.6, 2.5, 0])
    fit_width(fifth, 9.4)
    scene.play(FadeOut(conserve), run_time=0.4)
    scene.play(FadeIn(fifth, shift=DOWN * 0.15), run_time=0.6)
    scene.play(set_attr(stage, stock, "speed", 2.0), set_attr(stage, added, "speed", 2.0), run_time=5.5)
    scene.play(set_attr(stage, stock, "speed", 1.0), set_attr(stage, added, "speed", 1.0), Indicate(nums_box), run_time=5.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["18"])
