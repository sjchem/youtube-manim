"""Scene 02 — the puzzle. Up close, one gold molecule zigzags unpredictably;
step back and the gauges hold steady (pressure, volume, temperature, all read
from the model). A crowd of commuters makes the same point as a metaphor:
no single walker is predictable, yet the gate's count climbs steadily. The
four driving questions of the film appear as a road map.
"""

from manim_scenes.common import *


class Scene02Puzzle(Scene):
    def construct(self) -> None:
        play_scene(self)


class Commuters(VGroup):
    """A metaphor, not a model: walkers drift right with random sway; a counter
    tallies those passing the gate. Each walker is unpredictable; the count is not."""

    def __init__(self, at, width: float = 6.0, height: float = 2.6, count: int = 46, seed: int = cfg.SEED) -> None:
        super().__init__()
        rng = np.random.default_rng(seed)
        self.at, self.w, self.h = np.asarray(at, dtype=float), width, height
        self.x0 = rng.uniform(0, width, count)
        self.v = rng.uniform(0.35, 0.9, count)
        self.y0 = rng.uniform(-height / 2 + 0.2, height / 2 - 0.2, count)
        self.f = rng.uniform(0.6, 1.8, count)
        self.p = rng.uniform(0, TAU, count)
        self.clock = Knob(0.0)
        self.gate_x = 0.62 * width
        frame = RoundedRectangle(width=width + 0.3, height=height + 0.3, corner_radius=0.2, stroke_color=cfg.MUTED,
                                 stroke_width=2, stroke_opacity=0.5, fill_color=cfg.PANEL, fill_opacity=0.6).move_to(self.at)
        gate = VGroup(*[Line([0, y, 0], [0, y + 0.42, 0], stroke_color=cfg.GOLD, stroke_width=6)
                        for y in np.linspace(-height / 2, height / 2 - 0.42, 4)])
        gate.move_to(self.at + RIGHT * (self.gate_x - width / 2))
        self.dots = VGroup(*[Dot(radius=0.07, color=cfg.WHITE, fill_opacity=0.85) for _ in range(count)])
        self.counter = Integer(0, font_size=56, color=cfg.GOLD)
        self.counter.set_stroke(cfg.BG, width=0.6, opacity=0.85, background=True)
        self.add(frame, gate, self.dots, self.counter)
        self.frame = frame
        self.add_updater(lambda m: m.refresh())
        self.refresh()

    def refresh(self) -> "Commuters":
        t = self.clock.value
        travelled = self.x0 + self.v * t
        x = np.mod(travelled, self.w) - self.w / 2
        y = self.y0 + 0.28 * np.sin(self.f * t + self.p) * self.h / 2.6
        for dot, xi, yi in zip(self.dots, x, y):
            dot.move_to(self.at + np.array([xi, yi, 0]))
        passed = np.floor((travelled - self.gate_x) / self.w) - np.floor((self.x0 - self.gate_x) / self.w)
        self.counter.set_value(int(passed.sum()))
        self.counter.next_to(self.frame, DOWN, buff=0.2)
        return self


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "02", "Random parts, a precise whole")
    box = GasBox((-2.2, -0.45, 0.0), count=110, half_x=1.9, half_z=1.35, height=3.3, floor=-1.65, follow=23,
                 trail=5.0, zoom=1.2, yaw=-0.55, pitch=0.3, speed=1.7)
    box.cloud.follow_alpha = 0.0
    show(scene, box.stage, 1.2)
    scene.play(*box.stage.turn(yaw=-0.4), run_time=2.4)

    # --- 2. Follow one molecule: an unpredictable zigzag ------------------------------------------------------
    beat(scene, t, 1)
    random_tag = txt("one molecular path", cfg.FONT["label"], cfg.FOLLOWED).move_to([3.6, 2.9, 0])
    scene.play(box.cloud.tween("follow_alpha", 1.0), box.stage.zoom_to(1.55), box.stage.glide([0.0, -0.45, 0]),
               FadeIn(random_tag, shift=DOWN * 0.1), run_time=1.6)
    scene.play(box.cloud.tween("alpha", 0.35), run_time=1.2)
    scene.play(*box.stage.turn(yaw=-0.2), run_time=4.5)

    # --- 3. Step back: steady gauges ------------------------------------------------------------------------------
    beat(scene, t, 2)
    gauge = Gauge(box.pressure, [3.4, 1.15, 0], top=3.0, radius=1.0)
    therm = Thermo(box.kelvin, [6.1, 0.9, 0], height=2.4)
    vol = readout("V", lambda: 2.0 * box.chamber.volume_ratio(), 2, "L", cfg.VOLUME).move_to([4.4, -2.55, 0])
    steady = txt("the crowd: steady", cfg.FONT["label"], cfg.PRESSURE).move_to([2.4, 3.45, 0])
    scene.play(FadeOut(random_tag), box.cloud.tween("alpha", 1.0), box.stage.zoom_to(1.15),
               box.stage.glide([-2.6, -0.45, 0]), run_time=1.6)
    scene.play(FadeIn(gauge, shift=LEFT * 0.2), FadeIn(therm, shift=LEFT * 0.2), run_time=1.0)
    scene.play(FadeIn(vol, shift=UP * 0.1), FadeIn(steady), run_time=0.9)
    scene.play(Indicate(gauge.readout, color=cfg.PRESSURE), run_time=1.2)

    # --- 4. A crowd of people: the same idea (a metaphor) ----------------------------------------------------------
    beat(scene, t, 3)
    walkers = Commuters([2.9, 0.1, 0], width=6.6, height=2.9)
    tag = txt("a busy station (a metaphor)", cfg.FONT["small"], cfg.MUTED).next_to(walkers.frame, UP, buff=0.25)
    scene.play(FadeOut(VGroup(gauge, therm, vol, steady)), box.stage.glide([-4.7, -0.45, 0]), box.stage.zoom_to(0.85),
               run_time=0.7)
    scene.play(FadeIn(walkers), FadeIn(tag), run_time=0.9)
    scene.play(walkers.clock.to(walkers, 12.0, run_time=12.0, rate_func=linear), run_time=12.0)

    # --- 5. The laws describe the crowd ----------------------------------------------------------------------------
    beat(scene, t, 4)
    crowd = result_label("laws describe the crowd", cfg.GOLD, cfg.FONT["body"]).move_to([2.9, 3.0, 0])
    scene.play(FadeOut(tag), FadeIn(crowd, scale=0.95), walkers.clock.to(walkers, 15.5, run_time=3.5, rate_func=linear),
               run_time=3.5)

    # --- 6. Four questions ------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    questions = VGroup(
        chip("1  Why attraction?", cfg.ATTRACT),
        chip("2  Why pressure?", cfg.IMPULSE),
        chip("3  Why gas laws?", cfg.PRESSURE),
        chip("4  One equation?", cfg.WHITE),
    ).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
    fit_width(questions, 7.8)
    questions.move_to([2.7, -0.1, 0])
    scene.play(FadeOut(VGroup(walkers, crowd)), box.stage.glide([-3.6, -0.45, 0]), box.stage.zoom_to(1.0), run_time=1.0)
    for q, wait in zip(questions, (3.4, 4.6, 4.6, 3.6)):
        scene.play(FadeIn(q, shift=LEFT * 0.3), run_time=0.8)
        scene.wait(wait)

    # --- 7. Begin with the forces between molecules ---------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(questions[0].animate.scale(1.08), *[q.animate.set_opacity(0.35) for q in questions[1:]], run_time=0.9)
    finish(scene, t, box.stage)
