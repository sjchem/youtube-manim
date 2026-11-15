"""Scene 15 — a gallery of shapes. Three uncluttered views compare round
bodies, spheres, and rods about dashed cyan axes, with short names and moments
of inertia (the coefficients come
from ``physics_models.SHAPES``, which re-derives each one by integration):
thin ring M R^2; solid disc and solid cylinder 1/2 M R^2; solid sphere 2/5
M R^2 and thin spherical shell 2/3 M R^2 (a cloud of points on a sphere);
thin rod about its middle 1/12 M L^2 and about one end 1/3 M L^2. The round
bodies then line up as bars of I / M R^2, and the ring's bar is twice the
disc's.
"""

from manim_scenes.common import *

R = 0.9
ROD_L = 2.6


class Scene15Shapes(Scene):
    def construct(self) -> None:
        play_scene(self)


def formula(key: str) -> MathTex:
    sh = pm.shape(key)
    size = "L" if sh.length == "L" else "R"
    return eq(rf"{ftex(sh.coefficient)}M{size}^2", cfg.FONT["body"], cfg.INERTIA)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "15", "A gallery of shapes")
    stage = Stage((0.0, -0.2, 0.0), zoom=1.35, yaw=-0.15, pitch=0.22, sway=0.02)
    spin = Knob(0.0)
    drive(stage, spin, 0.9)
    spots = {"ring": (-3.8, 0), "disc": (0, 0), "cylinder": (3.8, 0),
             "sphere": (-2.5, 0), "shell": (2.5, 0), "rod_mid": (-3.5, 0), "rod_end": (2.1, 0)}
    P = {k: np.array([x, y, 0.0]) for k, (x, y) in spots.items()}
    tilt = mu.rotation_x(0.35)
    parts: dict[str, list] = {}

    def axis(key: str, through: np.ndarray, direction: np.ndarray, half: float = 1.35):
        seg = Segment(through - direction * half, through + direction * half, cfg.ANGLE, width=3, opacity=0.9, dashed=True)
        seg.bias = 5.0
        return seg

    ring = Hoop(P["ring"], R, cfg.RING_BODY, pose=lambda: tilt, spin=lambda: spin.value, width=16)
    parts["ring"] = [ring, axis("ring", P["ring"], tilt @ np.array([0, 0, 1.0]))]
    disc = Drum(P["disc"], R, 0.08, cfg.DISC_BODY, pose=lambda: tilt, spin=lambda: spin.value, stripe=cfg.DISC_STRIPE, sectors=8)
    parts["disc"] = [disc, axis("disc", P["disc"], tilt @ np.array([0, 0, 1.0]))]
    cyl = Drum(P["cylinder"], R * 0.75, 0.75, cfg.DISC_BODY, pose=lambda: mu.rotation_y(0.6) @ mu.rotation_x(0.2),
               spin=lambda: spin.value, stripe=cfg.DISC_STRIPE, sectors=6)
    parts["cylinder"] = [cyl, axis("cylinder", P["cylinder"], mu.rotation_y(0.6) @ mu.rotation_x(0.2) @ np.array([0, 0, 1.0]), 1.4)]
    ball = Ball(P["sphere"], R, cfg.DISC_BODY)
    meridian = Curve(lambda: np.array([P["sphere"] + mu.rotation_y(spin.value) @ (R * 1.01 * np.array([np.sin(a), np.cos(a), 0.0]))
                                       for a in np.linspace(0, np.pi, 24)]), cfg.DISC_STRIPE, width=3, glow=False)
    meridian.bias = 1.0
    parts["sphere"] = [ball, meridian, axis("sphere", P["sphere"], np.array([0, 1.0, 0]))]
    golden = np.pi * (3 - np.sqrt(5))
    n_shell = 160
    shell_local = np.array([[np.sqrt(1 - z * z) * np.cos(golden * k), z, np.sqrt(1 - z * z) * np.sin(golden * k)]
                            for k, z in enumerate(np.linspace(-0.98, 0.98, n_shell))])
    shell = Dots(lambda: P["shell"] + (shell_local * R) @ mu.rotation_y(spin.value).T, cfg.DISC_STRIPE, radius=0.045)
    parts["shell"] = [shell, axis("shell", P["shell"], np.array([0, 1.0, 0]))]

    def rod(key: str, pivot_frac: float):
        centre = P[key]

        def end(s: float) -> np.ndarray:
            along = mu.rotation_y(spin.value) @ np.array([1.0, 0.0, 0.0])
            return centre + along * ROD_L * (s - pivot_frac)

        a, b = Ball(lambda: end(-0.5), 0.07, cfg.STEEL, layers=6), Ball(lambda: end(0.5), 0.07, cfg.STEEL, layers=6)
        return [a, b, Rod(a, b, width=18, dark="#2E5873", light="#BFE3F7"), axis(key, centre, np.array([0, 1.0, 0]), 1.1)]

    parts["rod_mid"] = rod("rod_mid", 0.0)
    parts["rod_end"] = rod("rod_end", -0.5)
    for items in parts.values():
        hidden(*items)
        stage.add_body(*items)
    names = {"ring": "thin ring", "disc": "solid disc", "cylinder": "solid cylinder",
             "sphere": "solid sphere", "shell": "thin spherical shell", "rod_mid": "rod: midpoint", "rod_end": "rod: end"}
    labels, name_tags = {}, {}
    for key in parts:
        lab = formula(key)
        labels[key] = Tag(lab, P[key] + np.array([0, -1.55, 0]))
        name_tags[key] = Tag(txt(names[key], cfg.FONT["small"], cfg.WHITE), P[key] + np.array([0, 1.65, 0]))
        labels[key].presence = 0.0
        name_tags[key].presence = 0.0
        stage.add_overlay(labels[key], name_tags[key])
    scene.add(stage)
    three = VGroup(chip("shape", cfg.WHITE), chip("mass distribution", cfg.MASS), chip("axis", cfg.ANGLE)).arrange(RIGHT, buff=0.5)
    three.move_to(DOWN * 3.75)
    scene.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in three], lag_ratio=0.35), run_time=1.6)

    def reveal(*keys: str, run_time: float = 1.0) -> None:
        anims = [stage.fade(item, 1.0) for k in keys for item in parts[k]]
        anims += [stage.fade(label, 1.0) for k in keys for label in (labels[k], name_tags[k])]
        scene.play(*anims, run_time=run_time)

    def retire(*keys: str) -> None:
        scene.play(*[stage.fade(item, 0.0) for k in keys for item in (*parts[k], labels[k], name_tags[k])], run_time=0.6)

    # --- 2. Ring ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(FadeOut(three), run_time=0.5)
    reveal("ring")
    rim = caption("every bit of mass at distance R", cfg.RING_BODY)
    scene.play(FadeIn(rim), run_time=0.6)

    # --- 3. Disc and cylinder -------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(rim), run_time=0.4)
    reveal("disc")
    scene.wait(1.6)
    reveal("cylinder")
    length = caption("central axis: independent of cylinder length", cfg.DISC_STRIPE)
    scene.play(FadeIn(length), run_time=0.6)

    # --- 4. Sphere and shell ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(length), run_time=0.4)
    retire("ring", "disc", "cylinder")
    reveal("sphere")
    scene.wait(1.2)
    reveal("shell")

    # --- 5. Rods ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    retire("sphere", "shell")
    reveal("rod_mid")
    scene.wait(1.6)
    reveal("rod_end")
    scene.play(*stage.turn(pitch=0.32), run_time=2.0)

    # --- 6. Bars: more mass near the rim, larger I -----------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    hide(scene, stage, 0.8)
    order = ["sphere", "disc", "cylinder", "shell", "ring"]
    values = [float(pm.shape(k).coefficient) for k in order]
    names = ["sphere", "disc", "cylinder", "shell", "ring"]
    colors = [cfg.DISC_BODY, cfg.DISC_BODY, cfg.DISC_BODY, cfg.DISC_STRIPE, cfg.RING_BODY]
    chart = bar_chart(values, names, colors, at=DOWN * 0.75, width=11.0, height=4.2, top=1.0, bar_width=1.2,
                      value_labels=None, name_size=34)
    tops = VGroup(*[eq(rf"{ftex(pm.shape(k).coefficient) or '1'}", cfg.FONT["body"], cfg.INERTIA).next_to(bar, UP, buff=0.15)
                    for k, bar in zip(order, chart.bars)])
    axis_name = eq(r"I \,/\, MR^2", cfg.FONT["section"], cfg.INERTIA).move_to([-5.6, 2.9, 0])
    scene.play(Create(chart.base), FadeIn(chart.names), FadeIn(axis_name), run_time=0.8)
    scene.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in chart.bars], lag_ratio=0.2), run_time=2.0)
    scene.play(FadeIn(tops, lag_ratio=0.15), run_time=1.0)
    rim_rule = caption("more mass near the rim → larger I", cfg.WHITE)
    scene.play(FadeIn(rim_rule), run_time=0.7)

    # --- 7. Ring = 2 x disc ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    ring_bar, disc_bar = chart.bars[4], chart.bars[1]
    copy = disc_bar.copy().set_fill(cfg.DISC_STRIPE, opacity=0.9)
    scene.play(*[b.animate.set_opacity(0.25) for k, b in enumerate(chart.bars) if k not in (1, 4)], FadeOut(rim_rule), run_time=0.8)
    scene.play(copy.animate.next_to(ring_bar.get_bottom(), UP, buff=0).shift(RIGHT * 0.0), run_time=1.0)
    copy2 = disc_bar.copy().set_fill(cfg.DISC_STRIPE, opacity=0.9)
    scene.play(copy2.animate.next_to(copy, UP, buff=0), run_time=1.0)
    twice = eq(rf"I_{{\text{{ring}}}} = {fx(pm.shape('ring').coefficient / pm.shape('disc').coefficient)}\, I_{{\text{{disc}}}}",
               cfg.FONT["section"], cfg.RESULT)
    twice_box = boxed(twice, cfg.RESULT).move_to([2.6, 3.25, 0])
    scene.play(Write(twice), run_time=1.2)
    scene.play(Create(twice_box.frame), run_time=0.6)
    farther = caption("equal M and R · ring has twice the I", cfg.RING_BODY)
    scene.play(FadeIn(farther), run_time=0.6)

    # --- 8. Where the mass sits ----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    final = result_label("where the mass sits matters", cfg.RESULT, cfg.FONT["section"]).move_to(DOWN * 3.7)
    scene.play(fade_through(farther, final), run_time=1.0)
    finish(scene, t, fill=lambda sec: [Indicate(twice, color=cfg.WHITE, scale_factor=1.04)])
