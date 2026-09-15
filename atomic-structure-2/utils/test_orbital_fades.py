"""Regression: camera lighting must never overwrite animation transparency.

Run with: python -m unittest utils.test_orbital_fades
"""
from types import SimpleNamespace
import unittest

import numpy as np
from manim import FadeIn, FadeOut, config, linear

from manim_scenes.common import orbital


class OrbitalFadeTests(unittest.TestCase):
    def setUp(self):
        self.height = config.pixel_height
        config.pixel_height = 480

    def tearDown(self):
        config.pixel_height = self.height

    def test_fades_survive_updates_to_animation_copies(self):
        states = ((1, 0, 0), (2, 0, 0),
                  (2, 1, 0), (2, 1, 1), (2, 1, -1),
                  (3, 2, -2), (3, 2, 1), (3, 2, -1), (3, 2, 2), (3, 2, 0))
        for state in states:
            for opacity in (1.0, 0.42):
                for fade in (FadeIn, FadeOut):
                    with self.subTest(state=state, opacity=opacity, fade=fade.__name__):
                        surface = orbital(None, *state, opacity=opacity)
                        animation = fade(surface, rate_func=linear)
                        animation.begin()
                        for alpha in np.linspace(0, 1, 9):
                            # Manim updates hidden start and target meshes too.
                            animation.update_mobjects(1 / 15)
                            animation.interpolate(alpha)
                            expected = opacity * (alpha if fade is FadeIn else 1 - alpha)
                            actual = [face.fill_rgbas[0, 3] for face in surface]
                            np.testing.assert_allclose(actual, expected, atol=1e-12)
                        animation.finish()

    def test_camera_relighting_preserves_per_face_alpha(self):
        angle = [0.9, -0.6]
        scene = SimpleNamespace(camera=SimpleNamespace(
            get_phi=lambda: angle[0], get_theta=lambda: angle[1]))
        surface = orbital(scene, 3, 2, 0)
        expected = np.linspace(0, 1, len(surface))
        for face, alpha in zip(surface, expected):
            face.fill_rgbas[0, 3] = alpha
        old_rgb = np.array([face.fill_rgbas[0, :3].copy() for face in surface])
        angle[:] = [1.2, 0.8]
        surface.update(1 / 15)
        np.testing.assert_allclose([face.fill_rgbas[0, 3] for face in surface], expected)
        new_rgb = np.array([face.fill_rgbas[0, :3] for face in surface])
        self.assertGreater(float(np.max(np.abs(new_rgb - old_rgb))), 0.01)


if __name__ == "__main__":
    unittest.main()
