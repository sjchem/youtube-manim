"""Scene 19 — absolute zero by extrapolation. Volume against Celsius
temperature for three samples (different amounts or pressures): measured
points between 0 and 150 C lie on straight lines with different slopes.
Extended backward (dashed, purple), every line reaches zero volume at the same
point, -273.15 C. Sliding the vertical axis there gives the Kelvin scale,
T = theta + 273.15, and every line passes through the origin. A caution: real
gases condense long before; the meeting point is an extrapolation.
"""

from manim_scenes.common import *

T0 = pm.T_ICE
SAMPLES = ((1.0, cfg.VOLUME), (1.6, cfg.CYAN), (2.3, cfg.TEAL))   # volume at 0 C, in litres


class Scene19AbsoluteZero(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "19", "Absolute zero")
    axes = plot_axes((-300, 200), (0, 3.6), x_length=11.6, y_length=4.8, at=[-0.6, 0.15, 0], x_label=r"\theta\ (^\circ\mathrm{C})",
                     y_label="V", x_color=cfg.TEMPERATURE, y_color=cfg.VOLUME, x_ticks=(-200, -100, 100))
    # The y axis of an Axes sits at x = -300 here; draw a Celsius zero line where theta = 0.
    zero_c = DashedLine(axes.c2p(0, 0), axes.c2p(0, 3.5), stroke_color=cfg.MUTED, stroke_width=2, dash_length=0.12)
    zero_tag = txt("0 °C", cfg.FONT["tiny"], cfg.MUTED).next_to(axes.c2p(0, 0), DOWN, buff=0.12)
    scene.play(Create(axes), Create(zero_c), FadeIn(zero_tag), run_time=1.6)

    def line_for(v0: float, start: float, stop: float, color: str, dashed: bool = False):
        a, b = axes.c2p(start, v0 * (1 + start / T0)), axes.c2p(stop, v0 * (1 + stop / T0))
        if dashed:
            return DashedLine(a, b, stroke_color=color, stroke_width=4, dash_length=0.14)
        return Line(a, b, stroke_color=color, stroke_width=6)

    measured = [VGroup(*[glow_dot(axes.c2p(th, v0 * (1 + th / T0)), color, 0.08) for th in (0, 50, 100, 150)])
                for v0, color in SAMPLES]
    fits = [line_for(v0, 0, 180, color) for v0, color in SAMPLES]

    # --- 2. One gas: points on a straight line ------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(LaggedStart(*[FadeIn(p, scale=1.4) for p in measured[0]], lag_ratio=0.3), run_time=1.8)
    scene.play(Create(fits[0]), run_time=1.2)
    straight = txt("a straight line", cfg.FONT["label"], cfg.WHITE).move_to([3.2, 3.0, 0])
    scene.play(FadeIn(straight), run_time=0.8)

    # --- 3. Other amounts or pressures: other slopes ------------------------------------------------------------------------------------
    beat(scene, t, 2)
    for points, fit in zip(measured[1:], fits[1:]):
        scene.play(LaggedStart(*[FadeIn(p, scale=1.4) for p in points], lag_ratio=0.2), run_time=1.3)
        scene.play(Create(fit), run_time=1.0)
    other = txt("different slopes", cfg.FONT["label"], cfg.WHITE).move_to([3.2, 3.0, 0])
    scene.play(fade_through(straight, other), run_time=0.9)

    # --- 4. Extend backward ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    extensions = [line_for(v0, 0, -T0, cfg.LIMIT, dashed=True) for v0, _ in SAMPLES]
    scene.play(*[Create(e) for e in extensions], FadeOut(other), run_time=3.2, rate_func=rate_functions.ease_in_out_sine)

    # --- 5. They meet at zero volume, -273.15 C ------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    meet = glow_dot(axes.c2p(-T0, 0), cfg.LIMIT, 0.14)
    zero = eq(rf"-{fx(T0, 2)}\ ^\circ\mathrm{{C}}", cfg.FONT["section"], cfg.LIMIT).next_to(axes.c2p(-T0, 0), UP, buff=0.9)
    pointer = Arrow(zero.get_bottom(), axes.c2p(-T0, 0.12), stroke_color=cfg.LIMIT, stroke_width=4, buff=0.1)
    scene.play(FadeIn(meet, scale=2.0), run_time=0.9)
    scene.play(FadeIn(zero, shift=DOWN * 0.15), GrowArrow(pointer), run_time=1.2)
    scene.play(Indicate(meet, color=cfg.WHITE, scale_factor=1.5), run_time=1.2)

    # --- 6. Absolute zero: the Kelvin scale -------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    name = result_label("absolute zero", cfg.LIMIT, cfg.FONT["section"]).move_to([-2.6, 2.75, 0])
    fit_width(name, 3.6)
    kelvin = eq(rf"T = \theta + {fx(T0, 2)}", cfg.FONT["body"], cfg.TEMPERATURE).move_to([-2.6, 1.85, 0])
    fit_width(kelvin, 3.6)
    new_axis = Line(axes.c2p(-T0, 0), axes.c2p(-T0, 3.5), stroke_color=cfg.TEMPERATURE, stroke_width=5)
    zero_k = txt("0 K", cfg.FONT["small"], cfg.TEMPERATURE).next_to(axes.c2p(-T0, 0), DOWN, buff=0.15)
    ice_k = txt(f"{fx(T0, 2)} K", cfg.FONT["tiny"], cfg.TEMPERATURE).next_to(zero_tag, DOWN, buff=0.22)
    scene.play(FadeIn(name, scale=0.95), run_time=1.0)
    scene.play(FadeIn(kelvin, shift=UP * 0.1), run_time=1.0)
    scene.play(FadeOut(pointer), FadeOut(zero), run_time=1.0)
    scene.play(Create(new_axis), FadeIn(zero_k), FadeIn(ice_k), run_time=1.6)

    # --- 7. On the Kelvin scale, every line passes through the origin ----------------------------------------------------------------------
    beat(scene, t, 6)
    origin = txt("Kelvin origin", cfg.FONT["small"], cfg.WHITE).move_to([-2.6, 1.0, 0])
    fit_width(origin, 3.6)
    scene.play(*[e.animate.set_stroke(opacity=1.0, width=5) for e in extensions], FadeIn(origin), run_time=1.2)
    scene.play(Indicate(meet, color=cfg.TEMPERATURE, scale_factor=1.6), run_time=1.2)

    # --- 8. Caution: phase changes intervene: an extrapolation -------------------------------------------------------------------------------
    beat(scene, t, 7)
    condense = VGroup(*[glow_dot(axes.c2p(th, v0 * (1 + th / T0)), cfg.WARNING, 0.11) for (v0, _), th in zip(SAMPLES, (-190, -170, -150))])
    liquid = txt("phase changes", cfg.FONT["small"], cfg.WARNING).move_to([-2.6, 1.0, 0])
    caveat = txt("ideal-gas extrapolation", cfg.FONT["small"], cfg.LIMIT).move_to([4.1, 3.05, 0])
    fit_width(liquid, 3.6)
    fit_width(caveat, 5.4)
    scene.play(fade_through(origin, liquid), LaggedStart(*[FadeIn(c, scale=1.6) for c in condense], lag_ratio=0.3), run_time=1.6)
    scene.play(FadeIn(caveat, shift=UP * 0.1), run_time=1.0)
    finish(scene, t, fill=lambda s: [Indicate(meet, color=cfg.LIMIT, scale_factor=1.3)])
