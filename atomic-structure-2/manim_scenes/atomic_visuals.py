"""Shared lit classical markers for the opening and experimental recap."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import QuantumScene


def lit_sphere(scene: QuantumScene, radius: float, colour: str,
               resolution: tuple[int, int] = (28, 20), *,
               shadow_colour: str = "#17334D", ambient: float = 0.24) -> Surface:
    """Light an actual sphere independently of Manim's disabled face shading.

    The mesh is modest because these are small classical model markers, not
    calculated orbital surfaces. Normals stay valid under translation; callers
    move the centre rather than rotating or deforming the mesh.
    """
    ball = Sphere(radius=radius, resolution=resolution, fill_opacity=1, stroke_width=0.45)
    normals = np.array([face.get_center() for face in ball])
    normals /= np.linalg.norm(normals, axis=1)[:, None]
    base = np.array(ManimColor(colour).to_rgb())
    shadow = np.array(ManimColor(shadow_colour).to_rgb())
    white = np.array(ManimColor(cfg.WHITE).to_rgb())
    for face in ball:
        face.set_shade_in_3d(True)

    def relight(mob: Mobject, dt: float = 0.0) -> None:
        phi, theta = scene.camera.get_phi(), scene.camera.get_theta()
        eye = np.array([np.sin(phi) * np.cos(theta), np.sin(phi) * np.sin(theta), np.cos(phi)])
        up = np.array([0., 0., 1.]) - eye * eye[2]
        up = up / np.linalg.norm(up) if np.linalg.norm(up) > 1e-6 else np.array([0., 1., 0.])
        light = eye * 0.7 + up * 0.6 - np.cross(up, eye) * 0.45
        light /= np.linalg.norm(light)
        halfway = light + eye
        halfway /= np.linalg.norm(halfway)
        diffuse = np.clip(normals @ light, 0, 1)
        rim = (1 - np.abs(normals @ eye)) ** 3
        brightness = np.clip(ambient + 0.70 * diffuse + 0.15 * rim, 0, 1)
        colours = shadow + (base - shadow) * brightness[:, None]
        specular = (np.clip(normals @ halfway, 0, 1) ** 30) * 0.80
        colours += (white - colours) * specular[:, None]
        for face, rgb in zip(mob, colours):
            # Leave alpha to FadeIn/FadeOut; relighting must never undo a fade.
            face.fill_rgbas[:, :3] = rgb
            # A same-colour edge seals Cairo antialias gaps between patches.
            face.stroke_rgbas[:, :3] = rgb

    relight(ball)
    ball.add_updater(relight)
    return ball




def nucleon_cluster(scene: QuantumScene) -> VGroup:
    """A compact, lit 12-proton / 12-neutron nucleus for the opening model.

    Close-packed spheres are a visual convention, not a microscopic image of
    nucleons. Warm red distinguishes protons from golden neutrons. The 2,8,2
    electron picture has matching charge; no isotope lesson is implied.
    """
    sites = [
        np.array([x, y, z], dtype=float)
        for x in range(-2, 3)
        for y in range(-2, 3)
        for z in range(-2, 3)
        if (x + y + z) % 2 == 0
    ]
    sites.sort(key=lambda point: (np.dot(point, point), point[2], point[1], point[0]))
    centers = np.array(sites[:24])
    centers -= centers.mean(axis=0)
    centers *= 0.265 / np.sqrt(2)
    cluster = VGroup()
    for index, center in enumerate(centers):
        colour = "#FF542B" if index % 2 == 0 else "#FFD43B"
        bead = lit_sphere(scene, 0.145, colour, resolution=(16, 12),
                          shadow_colour="#6A2506", ambient=0.46)
        bead.move_to(center)
        cluster.add(bead)
    cluster._needs_depth_sort = True
    return cluster
