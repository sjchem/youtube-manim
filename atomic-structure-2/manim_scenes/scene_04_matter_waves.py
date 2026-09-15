"""Chapter 4: de Broglie turns the wave-particle question around.

Light was a wave that arrives in lumps. So could a lump have a wavelength? The
chapter earns lambda = h / p, then spends Bohr's own number on it. The electron
in the first shell was given a speed in chapter 3; put that speed into this
relation and a wavelength comes out that is the size of an atom. A cricket ball
gets exactly the same arithmetic and produces a wavelength twenty powers of ten
below a nucleus, which is why nobody has ever noticed one.
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    QuantumScene,
    electron,
    equation,
    glow_dot,
    glow_line,
    outlined_text,
    scale_ruler,
)

from manim_scenes.matter_wave_visuals import (
    BRIGHT_CYAN, BRIGHT_GOLD, CrystalDiffraction, TravellingWave,
)
from manim_scenes.scientist_portraits import scientist_portrait
from utils.quantum_examples import bohr_speed, de_broglie_wavelength, electron_wavelength

SCREEN_X = 5.05

BALL_MASS, BALL_SPEED = 0.160, 40.0
BALL_LAMBDA = de_broglie_wavelength(BALL_MASS, BALL_SPEED)
ELECTRON_LAMBDA = de_broglie_wavelength(9.1093837015e-31, bohr_speed(1))


def _number(latex: str, size: int = 46, color: str = BRIGHT_CYAN) -> MathTex:
    """Bright mathematical labels with enough weight for the low-res preview."""
    label = equation(latex, max(size, 44), color)
    return label.set_stroke(color, width=0.35, opacity=1)


def _crystal(model: CrystalDiffraction) -> VGroup:
    """The gold scattering sites used by the coherent array calculation."""
    return VGroup(*[
        glow_dot(site, radius=0.095, color=BRIGHT_GOLD)
        for site in model.sites
    ])


def _screen() -> VGroup:
    """A phosphor-like detection strip with a clear rim and a dark interior."""
    plate = RoundedRectangle(width=0.46, height=5.7, corner_radius=0.10,
                             stroke_color=BRIGHT_CYAN, stroke_width=2,
                             fill_color="#0C2B42", fill_opacity=0.85)
    plate.move_to([SCREEN_X, 0, 0])
    return VGroup(plate.copy().set_fill(opacity=0).set_stroke(width=12, opacity=0.10), plate)


def _source() -> VGroup:
    """An illuminated aperture gives the opening light a visible origin."""
    body = RoundedRectangle(width=0.72, height=1.05, corner_radius=0.14,
                            fill_color="#244761", fill_opacity=1,
                            stroke_color=BRIGHT_CYAN, stroke_width=2)
    rim = Ellipse(width=0.26, height=0.76, color=BRIGHT_GOLD,
                  stroke_width=3).shift(RIGHT * 0.32)
    core = glow_dot(RIGHT * 0.32, radius=0.16, color=BRIGHT_GOLD)
    return VGroup(body, rim, core).move_to([-6.3, 0, 0])


class Scene04MatterWaves(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("04")

    # -- Beat 1: light is a wave, and light also arrives ----------------------
    light = TravellingWave(width=10.5, k=4.8, amplitude=0.65,
                           center=[-0.4, 0, 0])
    scene.morph(light, seconds=1.4)
    detector, source = _screen(), _source()
    scene.show(VGroup(source, detector), seconds=0.7)
    labels = VGroup(
        outlined_text("LIGHT", 42, BRIGHT_GOLD).move_to([-3.6, 2.7, 0]),
        outlined_text("individual detections", 30, BRIGHT_CYAN, limit=4.3)
        .move_to([4.3, -3.25, 0]),
    )
    scene.show(labels, seconds=0.5)
    arrivals = VGroup()
    for height in (-0.18, 0.14, -0.05, 0.24):
        position = ValueTracker(-5.5)
        pulse = TravellingWave(width=10.5, k=4.8, amplitude=0.67,
                               center=[-0.4, 0, 0], color=BRIGHT_GOLD,
                               packet=position.get_value)
        scene.add(pulse)
        # The glowing packet is a field envelope, with no bead following the
        # sine curve. Only the detector supplies a localized recorded event.
        scene.playq(position.animate.set_value(5.2), seconds=1.5, rate_func=linear)
        pulse.clear_updaters()
        hit = glow_dot([SCREEN_X, height, 0], radius=0.055, color=BRIGHT_GOLD)
        scene.playq(FadeOut(pulse), FadeIn(hit),
                    Flash(hit.get_center(), color=BRIGHT_GOLD, flash_radius=0.24),
                    seconds=0.45)
        scene.remove(hit)
        arrivals.add(hit)
        scene.add(arrivals)
    scene.local.append(arrivals)
    scene.at(15)
    scene.drop(source, detector, labels, arrivals, seconds=0.6)
    # VGroup(source, detector) was only the entrance carrier.
    scene.local = [mob for mob in scene.local if source not in mob.get_family()]
    light.clear_updaters()

    # -- Beat 2: name the physicist, then let the relation take over ----------
    portrait_wave = TravellingWave(width=5.3, k=4, center=[2.5, -1.6, 0])
    scene.morph(portrait_wave, seconds=0.8)
    portrait = scene.pin(scientist_portrait("de_broglie.jpg", "Louis de Broglie"))
    scene.playq(FadeIn(portrait), seconds=0.7)
    card = scene.headline(r"\lambda=\frac{h}{p}", position=[2.4, 0.7, 0])
    scene.hold(3.6)
    scene.drop(portrait, seconds=0.6)
    scene.playq(card.animate.move_to([-1.5, 2.75, 0]), seconds=0.7)

    # -- Beat 3: double the speed, halve the wavelength -----------------------
    # One tracker drives the wave, its bracket and both numerical readouts.
    momentum = ValueTracker(4.0)
    moving = TravellingWave(k=momentum.get_value, width=10, amplitude=0.62,
                            center=[0, -0.55, 0])
    portrait_wave.clear_updaters()
    scene.dissolve(moving, seconds=1.0)

    def _span() -> VGroup:
        length = TAU / momentum.get_value()
        bar = DoubleArrow([-4.0, -1.85, 0], [-4.0 + length, -1.85, 0], buff=0,
                          color=BRIGHT_GOLD, stroke_width=4, tip_length=0.18)
        tag = MathTex(r"\lambda", font_size=44, color=BRIGHT_GOLD).next_to(bar, DOWN, buff=0.12)
        return VGroup(bar, tag)

    bracket = always_redraw(_span)
    scene.show(bracket, seconds=0.5)
    speed = DecimalNumber(1.0, num_decimal_places=1, color=BRIGHT_CYAN, font_size=48)
    wavelength = DecimalNumber(electron_wavelength(1e6) * 1e9, num_decimal_places=3,
                               color=BRIGHT_GOLD, font_size=48)
    speed.add_updater(lambda mob: mob.set_value(momentum.get_value() / 4).move_to([-3.75, -3.25, 0]))
    wavelength.add_updater(lambda mob: mob.set_value(electron_wavelength(momentum.get_value() * 2.5e5) * 1e9)
                           .move_to([3.15, -3.25, 0]))
    values = VGroup(
        MathTex("v=", font_size=48, color=BRIGHT_CYAN).move_to([-4.7, -3.25, 0]), speed,
        MathTex(r"\times10^6\ \mathrm{m/s}", font_size=44, color=BRIGHT_CYAN).move_to([-1.65, -3.25, 0]),
        MathTex(r"\lambda\approx", font_size=48, color=BRIGHT_GOLD).move_to([1.65, -3.25, 0]), wavelength,
        MathTex(r"\mathrm{nm}", font_size=44, color=BRIGHT_GOLD).move_to([4.5, -3.25, 0]),
    )
    values.update(0)
    scene.show(values, seconds=0.5)
    mass = scene.formula(r"p\approx m_e v", position=[3.4, 2.75, 0], size=48, color=BRIGHT_CYAN)
    scene.at(34)
    scene.playq(momentum.animate.set_value(8.0), seconds=6.5, rate_func=rate_functions.ease_in_out_sine)
    scene.at(45)
    scene.playq(momentum.animate.set_value(4.0), seconds=4.0, rate_func=rate_functions.ease_in_out_sine)
    scene.at(52)
    moving.clear_updaters()
    bracket.clear_updaters()
    values.clear_updaters()
    scene.drop(bracket, values, mass, card, seconds=0.7)

    # -- Beat 4: the same relation, applied to something we can hold ----------
    # The comparison is no longer qualitative. A cricket ball gets the identical
    # arithmetic, and the answer is what rules it out of ordinary experience.
    ball = ImageMobject(str(cfg.ROOT / "assets/images/cricket_ball.png")).set_height(2.1)
    ball.move_to([-4.4, 0.85, 0])
    tiny = TravellingWave(width=5.2, k=38, amplitude=0.26, center=[2.3, 0.55, 0])
    scene.dissolve(tiny, seconds=1.5)
    ball_tag = outlined_text("cricket ball", cfg.FONT["tiny"], BRIGHT_CYAN).next_to(ball, DOWN, buff=0.24)
    scene.show(Group(ball, ball_tag), seconds=0.8)

    working = scene.pin(VGroup(
        _number(rf"m={BALL_MASS:.3f}\ \mathrm{{kg}}", 38, BRIGHT_CYAN),
        _number(rf"v={BALL_SPEED:.0f}\ \mathrm{{m/s}}", 38, BRIGHT_CYAN),
        _number(rf"\lambda=\frac{{h}}{{mv}}\approx{BALL_LAMBDA * 1e34:.2f}\times10^{{-34}}\ \mathrm{{m}}",
                 40, BRIGHT_GOLD),
    ).arrange(DOWN, buff=0.34, aligned_edge=LEFT).move_to([2.2, -1.55, 0]))
    scene.playq(LaggedStart(*(FadeIn(line, shift=RIGHT * 0.14) for line in working), lag_ratio=0.5), seconds=2.6)
    scene.at(66)

    tiny.clear_updaters()
    # Compress the amplitude illustration while the logarithmic ruler supplies
    # the honest numerical scale. Crests keep moving during the comparison.
    unresolved = TravellingWave(width=5.2, k=38, amplitude=0.045,
                                center=[2.3, 0.55, 0])
    scene.morph(unresolved, seconds=1.2)
    scene.drop(working, seconds=0.5)

    # A logarithmic axis is the only way to hold both wavelengths in one frame.
    ruler = scale_ruler(
        [
            ("ball λ", BALL_LAMBDA, BRIGHT_CYAN),
            ("nucleus", 1e-15, cfg.RED),
            ("atom", 1e-10, BRIGHT_GOLD),
            ("electron λ", ELECTRON_LAMBDA, BRIGHT_CYAN),
        ],
        center=[0, -2.25, 0],
    )
    for label in ruler.get_family():
        if isinstance(label, (Text, MathTex)):
            label.set_color(BRIGHT_CYAN)
    scene.show(ruler, seconds=1.0)
    scene.playq(Indicate(ruler.pins["ball λ"], color=cfg.WHITE, scale_factor=1.10), seconds=1.2)
    scene.playq(Indicate(ruler.pins["nucleus"], color=cfg.WHITE, scale_factor=1.10), seconds=1.2)
    gap = scene.pin(outlined_text("far below a nucleus", cfg.FONT["tiny"], BRIGHT_CYAN, limit=5.0)
                    .move_to([-4.3, 2.95, 0]))
    scene.playq(FadeIn(gap), seconds=0.6)
    scene.at(84)
    scene.drop(ball, ball_tag, gap, seconds=0.7)

    # -- Beat 5: now spend Bohr's own speed on the same relation --------------
    bead = electron(0.19).move_to([-4.6, 1.30, 0])
    visible = TravellingWave(width=5.6, k=4, amplitude=0.60, center=[1.2, 1.30, 0])
    unresolved.clear_updaters()
    scene.morph(VGroup(bead, visible), seconds=1.8)
    inherited = scene.pin(VGroup(
        _number(rf"v_1={bohr_speed(1) / 1e6:.3f}\times10^6\ \mathrm{{m/s}}", 38, BRIGHT_CYAN),
        _number(rf"\lambda\approx{ELECTRON_LAMBDA * 1e10:.2f}\ \text{{\AA}}", 44, BRIGHT_CYAN),
    ).arrange(DOWN, buff=0.30).move_to([0, -0.35, 0]))
    scene.playq(LaggedStart(*(FadeIn(line) for line in inherited), lag_ratio=0.6), seconds=1.8)
    scene.playq(Indicate(ruler.pins["electron λ"], color=cfg.WHITE, scale_factor=1.10), seconds=1.2)
    scene.playq(Indicate(ruler.pins["atom"], color=cfg.WHITE, scale_factor=1.10), seconds=1.2)
    matched = scene.pin(outlined_text("the size of the atom itself", cfg.FONT["small"], BRIGHT_GOLD)
                        .move_to([0, 3.45, 0]))
    scene.playq(FadeIn(matched), seconds=0.6)
    scene.at(100)
    scene.drop(inherited, matched, ruler, seconds=0.8)

    # -- Beat 6: periodic scattering adds amplitudes, then detections ---------
    # The visible angular lobes and every sampled arrival use the same complex
    # finite-lattice amplitude. This is a far-field schematic, not a plotted
    # electron trajectory or a material-specific diffraction measurement.
    visible.clear_updaters()
    model = CrystalDiffraction()
    crystal = _crystal(model)
    incident = model.incoming()
    field = model.field()
    detector = _screen()
    apparatus = Group(field, incident, crystal, detector)
    scene.morph(apparatus, seconds=2.0)

    labels = VGroup(
        outlined_text("incident wave", 32, BRIGHT_CYAN).move_to([-3.5, 3.1, 0]),
        outlined_text("periodic crystal", 30, BRIGHT_GOLD).move_to([0, -2.95, 0]),
        outlined_text("detections", 28, BRIGHT_CYAN).move_to([5.05, -3.1, 0]),
        outlined_text("intensity", 26, BRIGHT_CYAN).move_to([6.35, 3.0, 0]),
    )
    scene.show(labels, seconds=0.7)
    addition = scene.formula(r"I\propto\left|\sum_j A_j\right|^2",
                             position=[2.5, 3.2, 0], size=46, color=cfg.WHITE)
    profile_points = np.column_stack((
        5.6 + 1.30 * model.profile / model.profile.max(),
        model.screen_y, np.zeros_like(model.screen_y),
    ))
    profile = VMobject(color=BRIGHT_GOLD, stroke_width=3)
    profile.set_points_as_corners(profile_points)
    profile_axis = Line([5.6, -2.65, 0], [5.6, 2.65, 0],
                        color=BRIGHT_CYAN, stroke_width=1, stroke_opacity=0.4)
    scene.show(VGroup(profile_axis, profile), seconds=0.8)

    rng = np.random.default_rng(cfg.SEED + 4)
    hits = VGroup(*[
        Dot([SCREEN_X + rng.uniform(-0.17, 0.17), y, 0],
            radius=0.035, color=BRIGHT_CYAN)
        for y in model.sample(rng, 240)
    ])
    # Accumulation occupies the explanation, while incident and scattered
    # crests continue to propagate. Sparse early counts resolve into bands.
    scene.playq(LaggedStart(*(FadeIn(dot) for dot in hits), lag_ratio=0.045),
                seconds=23.0)
    scene.remove(*hits)
    scene.add(hits)
    scene.local.append(hits)
    scene.cue("INTERFERENCE → BRIGHT BANDS AND GAPS", BRIGHT_GOLD,
              hold=2.4, position=DOWN * 3.85)
    scene.at(136)
    scene.drop(hits, labels, addition, profile_axis, profile, seconds=0.8)
    scene.local = [mob for mob in scene.local if profile not in mob.get_family()]

    # -- Beat 7: carry the amplitude into the one-electron question ----------
    incident.clear_updaters()
    field.clear_updaters()
    outgoing = TravellingWave(width=11, k=4.6, amplitude=0.72)
    scene.morph(outgoing, seconds=2.6)
    guide = VGroup(
        Line([-5.8, 0, 0], [5.8, 0, 0], color=BRIGHT_CYAN,
             stroke_width=1, stroke_opacity=0.3),
        outlined_text("wave amplitude", 32, BRIGHT_CYAN).move_to([0, -1.65, 0]),
    )
    scene.show(guide, seconds=0.5)
    scene.cue("ONE ELECTRON AT A TIME?", BRIGHT_GOLD,
              hold=3.0, position=UP * 3.1)
    scene.drop(guide, seconds=0.6)
    scene.finish()
    outgoing.clear_updaters()
