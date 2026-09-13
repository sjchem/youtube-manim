"""Render a separate four-second ManimGL check using the active Python environment.

Run: python utils/manimgl_smoke.py
Uses EGL on machines without a display; the film itself remains Manim CE.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('XDG_CACHE_HOME', str(ROOT/'media/gl-cache'))
os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'media/matplotlib'))
headless = '--headless' in sys.argv or not os.environ.get('DISPLAY')
if '--headless' in sys.argv:
    sys.argv.remove('--headless')
if headless:
    os.environ['PYGLET_HEADLESS'] = '1'
    import moderngl
    _create = moderngl.create_standalone_context
    def _egl_context(**kwargs):
        kwargs.setdefault('backend', 'egl')
        return _create(**kwargs)
    moderngl.create_standalone_context = _egl_context

from manimlib import Scene, Sphere, Circle, Group, FadeIn, Rotate, OUT, TAU, linear
from importlib.metadata import version

class ManimGLSmoke(Scene):
    def construct(self):
        self.frame.reorient(25, 60)
        core = Sphere(radius=0.3, color='#FF6B6B')
        track = Circle(radius=1.8, color='#8ED4FF').set_stroke(width=2)
        electron = Sphere(radius=0.12, color='#8ED4FF').shift([1.8, 0, 0])
        self.play(FadeIn(Group(core, track, electron)), run_time=1)
        self.play(Rotate(electron, TAU, axis=OUT, about_point=[0,0,0]), run_time=3, rate_func=linear)

if __name__ == '__main__':
    scene = ManimGLSmoke(camera_config=dict(resolution=(854,480), fps=30, background_color='#041A2F'),
        file_writer_config=dict(write_to_movie=True, output_directory=str(ROOT/'media/manimgl'), file_name='ManimGLSmoke'))
    print('ManimGL', version('manimgl'), scene.camera.ctx.info['GL_RENDERER'])
    scene.run()
