"""Accelerated, silent review of every scene; never used for voiceover timing.

Render: python -m manim -ql --fps 15 -r 854,480 manim_scenes/review_video.py ReviewVideo
All teaching animations remain, but narration holds are removed and movements
are shortened. Production durations and FullVideo are unchanged.
"""
from contextlib import ExitStack
from importlib import import_module
import os
from unittest.mock import patch

from manim import FadeOut, ThreeDScene

import config as cfg
from main import SCENE_MAP


class ReviewVideo(ThreeDScene):
    def play(self, *animations, **kwargs):
        kwargs['run_time'] = min(float(kwargs.get('run_time', 1.0)), 0.65)
        return super().play(*animations, **kwargs)

    def construct(self):
        def close(scene, started, duration, **kwargs):
            visible = list(scene.mobjects)
            for mob in visible:
                mob.clear_updaters()
            scene.play(FadeOut(*visible), run_time=0.3)
            scene.remove(*visible)

        cfg.apply_project_theme(self, bubbles=False)
        with ExitStack() as stack:
            selected = os.environ.get("SET_REVIEW_SCENES", "").split()
            for key, (module_name, _, _) in SCENE_MAP.items():
                if selected and str(int(key[-2:])) not in selected:
                    continue
                module = import_module(module_name)
                if hasattr(module, 'cue'):
                    stack.enter_context(patch.object(module, 'cue', lambda *args: None))
                stack.enter_context(patch.object(module, 'end_scene', close))
                module.play_scene(self)
