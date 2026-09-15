"""Chapter 18: the opening question, answered by replaying the whole film.

Every station the argument passed through comes back in order, fast, and the
spine strip names them. The answer is not a picture of an electron; it is the
chain itself.
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    QuantumScene,
    boxes,
    equation,
    _orbital_resolution,
    orbit,
    outlined_text,
    periodic_table,
)

from manim_scenes.uncertainty_visuals import OrbitMotion
from manim_scenes.matter_wave_visuals import TravellingWave
from utils.physics_models import orbital_geometry, sample_positions

ANSWER_CYAN = "#B7F3FF"
ANSWER_GOLD = "#FFE58A"
ORBITAL_SIZE = 2.4
STATE = (2, 1, 0)


def detection_cloud() -> VGroup:
    """Reveal fixed detections from the same 2p state as the next surface.

    The mesh and detections share a physical-to-display scale. Samples outside
    the viewing window are cropped, not moved inward or given trajectories.
    Both lobes use the same positive probability color.
    """
    triangles, _, _, _ = orbital_geometry(*STATE, resolution=_orbital_resolution())
    factor = ORBITAL_SIZE / np.linalg.norm(triangles.reshape(-1, 3), axis=1).max()
    positions = sample_positions(*STATE, count=650) * factor
    visible = positions[np.linalg.norm(positions, axis=1) < 3.0]
    detections = VGroup()
    for point in visible:
        halo = Dot(point, radius=0.090, color=ANSWER_CYAN, fill_opacity=0.11)
        core = Dot(point, radius=0.045, color=ANSWER_CYAN, fill_opacity=0.94)
        detections.add(VGroup(halo, core))
    detections.quantum_state = STATE
    detections.display_factor = factor
    return detections


class Scene18Answer(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("18")

    # -- Beat 1: the old question arrives as a living classical picture ------
    classical = orbit(2.3, nucleus_radius=0.25, electron_radius=0.14)
    classical[1].set_stroke(ANSWER_CYAN, opacity=0.62)
    rotation = OrbitMotion(classical)
    scene.add(rotation)
    scene.morph(classical, seconds=1.8)
    question = scene.pin(outlined_text("WHERE IS THE ELECTRON?", cfg.FONT["label"], ANSWER_GOLD)
                         .move_to([0, 3.45, 0]))
    scene.playq(FadeIn(question), seconds=0.6)
    scene.hold(1.2)
    scene.drop(question, seconds=0.5)

    # -- Beat 2: unwrap the road, then build a probability map from detections -
    travelling = TravellingWave(k=5, amplitude=0.72, color=ANSWER_CYAN)
    scene.morph(travelling, seconds=1.8)
    rotation.clear_updaters()
    scene.remove(rotation)
    answer = scene.pin(outlined_text("A STATE THAT PREDICTS PROBABILITIES", 38, ANSWER_GOLD)
                       .move_to([0, 3.5, 0]))
    probability = scene.pin(equation(r"|\psi|^2", 54, ANSWER_CYAN).move_to([0, -3.45, 0]))
    detections = detection_cloud()
    # Camera-facing dots retain their round glow as the 3D view opens. Their
    # projected centers still come from the original fixed detection positions.
    scene.camera.add_fixed_orientation_mobjects(*detections, use_static_center_func=True)
    # Interleaved batches preserve the random detection order. Points appear
    # where they are sampled; they never fly out from the nucleus.
    batches = [VGroup(*detections[index:index + 26]) for index in range(0, len(detections), 26)]
    scene.playq(
        FadeOut(travelling),
        LaggedStart(*(FadeIn(batch) for batch in batches), lag_ratio=0.12),
        FadeIn(answer), FadeIn(probability),
        seconds=1.8,
    )
    travelling.clear_updaters()
    scene.remove(*batches)
    scene.anchor = detections
    scene.add(detections)

    # The camera opens the two-lobed map, then its matching lit surface emerges.
    # Keeping the state and scale identical makes this a change of representation.
    scene.view3d(phi=68, theta=-50, seconds=1.4)
    surface = scene.orbital(*STATE, size=ORBITAL_SIZE)
    scene.begin_ambient_camera_rotation(rate=0.11 * cfg.SPEED)
    scene.dissolve(surface, seconds=1.8)
    scene.camera.remove_fixed_orientation_mobjects(*detections)
    scene.hold(2.2)
    scene.playq(FadeOut(scene.anchor), FadeOut(answer), FadeOut(probability), seconds=0.8)
    scene.remove_fixed_in_frame_mobjects(answer, probability)
    scene.local.remove(answer)
    scene.local.remove(probability)
    scene.anchor = VGroup()
    scene.add(scene.anchor)
    scene.stop_ambient_camera_rotation()
    surface.clear_updaters()
    scene.flat(seconds=1.0)

    # Draw the allowed occupations into their boxes before chemistry returns.
    occupied = boxes(10)
    arrows = list(occupied.arrows.values())
    occupied.remove(*arrows)
    scene.playq(
        FadeOut(scene.anchor), FadeIn(occupied),
        LaggedStart(*(GrowArrow(arrow) for arrow in arrows), lag_ratio=0.12),
        seconds=1.5,
    )
    scene.anchor = occupied
    scene.adopt(*arrows)
    scene.morph(periodic_table(), seconds=2.0)
    scene.at(25)

    # -- Beat 3: name the chain, and point at what comes next -----------------
    scene.spine(len(cfg.SPINE) - 1, hold=2.0, position=DOWN * 3.40)

    teaser = scene.pin(outlined_text("NEXT VIDEO", cfg.FONT["small"], cfg.GOLD).move_to([0, 3.55, 0]))
    title = scene.pin(outlined_text("Why does the periodic table have this shape?",
                                    cfg.FONT["label"], cfg.WHITE).move_to([0, 2.85, 0]))
    scene.playq(FadeIn(teaser), FadeIn(title, shift=DOWN * 0.1), seconds=0.8)
    scene.at(33)

    scene.finish()
