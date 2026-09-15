"""Scene 13: screening, separated radial plots and moving reading highlights.

All geometry carrying scientific information stays fixed during a hold.
Motion directs reading: it is not an electron trajectory or a fluctuating
stationary-state density. The force comparison is explicitly schematic.
"""
from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import cloud, equation, glow_dot, glow_curve, nucleus, outlined_text
from utils.physics_models import radial_distribution


class ScreeningView(VGroup):
    """Add screening at one fixed sample position; retain the nuclear force."""

    def __init__(self) -> None:
        super().__init__()
        self.strength = ValueTracker(0)
        self.elapsed = 0.0
        core = np.array([-4.0, 0.0, 0.0])
        self.density = cloud(count=200, scale=0.55, center=core, color=cfg.CYAN)
        # This is a projection of a diffuse inner distribution, without an orbit.
        self.haze = VGroup(*[
            Circle(radius=r, stroke_width=0, fill_color=cfg.CYAN, fill_opacity=0.014)
            .move_to(core) for r in np.linspace(0.3, 1.65, 18)
        ])
        self.density_base = [float(m.get_fill_opacity()) for m in self.density]
        bead = glow_dot([-0.65, 0, 0], radius=0.105, color=cfg.CYAN)
        bead.add(Dot(bead.get_center(), radius=0.037, color=cfg.WHITE))
        nucleus_mark = nucleus(0.29).move_to(core)
        labels = VGroup(
            outlined_text('PARTIAL SCREENING', 40, cfg.GOLD).move_to([0,3.45,0]),
            outlined_text('inner electron density', 29, cfg.CYAN).move_to([-4,2.05,0]),
            outlined_text('nucleus', 28, cfg.GOLD).move_to([-4,-2.1,0]),
            outlined_text('outer electron', 25, cfg.CYAN).move_to([-0.65,-0.62,0]),
            outlined_text('sample position', 23, cfg.MUTED).move_to([-0.65,-1.05,0]),
            outlined_text('schematic forces at this position', 25, cfg.MUTED)
                .move_to([3.95,-2.55,0]),
        )
        divider = Line([1.0,-2.65,0],[1.0,2.55,0],color=cfg.MUTED,
                       stroke_width=1.4,stroke_opacity=0.3)
        self.force_labels = VGroup()
        self.arrows, self.flow = VGroup(), VGroup()
        self.rows = ((1.3, cfg.GOLD, 'nuclear attraction'),
                     (-0.15, cfg.PURPLE, 'electron repulsion'),
                     (-1.60, cfg.GREEN, 'net inward pull'))
        for y, tone, words in self.rows:
            self.force_labels.add(outlined_text(words, 28, tone).move_to([4.25,y+0.52,0]))
            self.arrows.add(Arrow([5.6,y,0],[2.4,y,0],buff=0,color=tone,stroke_width=5))
            self.flow.add(glow_dot(radius=0.05,color=tone))
        self.add(self.haze,self.density,nucleus_mark,bead,divider,labels,
                 self.force_labels,self.arrows,self.flow)
        self._advance(self, 0)

    def start_motion(self) -> None:
        self.add_updater(self._advance)

    def _advance(self, _mob, dt: float) -> None:
        self.elapsed += dt * cfg.SPEED
        strength = self.strength.get_value()
        for dot, opacity in zip(self.density, self.density_base):
            dot.set_fill(opacity=opacity*strength)
        self.haze.set_fill(opacity=0.014*strength)
        # All arrows are schematic vectors at the same fixed electron position.
        # Nuclear attraction is unchanged; adding repulsion reduces the sum.
        lengths = (3.2, 1.35*strength, 3.2-1.35*strength)
        for index, ((y, tone, _), length, arrow, light) in enumerate(
                zip(self.rows, lengths, self.arrows, self.flow)):
            direction = RIGHT if index == 1 else LEFT
            start = np.array([3.0 if index == 1 else 5.6, y, 0])
            arrow.put_start_and_end_on(start,start+direction*max(length,0.01))
            visibility = strength if index == 1 else 1.0
            arrow.set_opacity(visibility)
            phase = (self.elapsed/2.6) % 1.0
            light.move_to(start+direction*length*phase)
            light.set_opacity(visibility*np.sin(PI*phase)**2)


class RadialComparison(VGroup):
    """Three small multiples, with one common physical x scale and y scale.

    Numeric peak labels live in their own column, never on top of another
    curve. The red strips share the same illustrative core radius. The moving
    vertical guides compare P(r) at a common r; they do not move any curve.
    """

    def __init__(self, core: float, peaks: dict[int,float]) -> None:
        super().__init__()
        self.elapsed = 0.0
        self.axes, self.data, self.curves = [], [], []
        tones = (cfg.GOLD,cfg.CYAN,cfg.PURPLE)
        self.span = 26.0
        grid = np.linspace(0,self.span,4000)
        self.ymax = max(float(radial_distribution(3,l,grid).max()) for l in range(3))*1.12
        self.add(outlined_text('HOW CLOSE DOES EACH STATE REACH?', 36, cfg.GOLD)
                 .move_to([0,3.70,0]))
        self.add(outlined_text('Hydrogen examples · same scales · red band = illustrative core',
                               25,cfg.MUTED).move_to([0,3.13,0]))
        for l, (baseline,tone) in enumerate(zip((1.35,-0.30,-1.95),tones)):
            axes = Axes(x_range=[0,self.span,5],y_range=[0,self.ymax,self.ymax],
                        x_length=8.1,y_length=1.05,tips=False,
                        axis_config=dict(color=cfg.MUTED,stroke_width=1.6,include_ticks=False))
            axes.shift(np.array([-5.45,baseline,0])-axes.c2p(0,0))
            band = Rectangle(width=8.1*core/self.span,height=1.05,stroke_width=1.2,
                             stroke_color=cfg.RED,fill_color=cfg.RED,fill_opacity=0.08)
            band.move_to((axes.c2p(0,0)+axes.c2p(core,self.ymax))/2)
            self.add(band,axes)
            self.axes.append(axes)
            curve = axes.plot(lambda r,l=l:float(radial_distribution(3,l,r)),
                              x_range=[0,self.span,self.span/600],color=tone,stroke_width=3.4)
            self.curves.append(curve)
            peak_point = axes.c2p(peaks[l],float(radial_distribution(3,l,peaks[l])))
            marker = glow_dot(peak_point,radius=0.055,color=tone)
            name = equation(('3s','3p','3d')[l],42,tone).move_to([-6.5,baseline+0.50,0])
            card = VGroup(
                outlined_text('innermost peak',24,cfg.MUTED),
                equation(rf'{peaks[l]:.2f}\,a_0',40,tone),
                outlined_text(('inside the core band','outside the core band','small inner tail')[l],
                              23,tone),
            ).arrange(DOWN,buff=0.13).move_to([5.10,baseline+0.50,0])
            self.data.append(VGroup(glow_curve(curve,tone),marker,name,card))
        bottom = self.axes[-1]
        for value in (0,5,10,15,20,25):
            pos = bottom.c2p(value,0)
            self.add(Line(pos+DOWN*0.04,pos+UP*0.04,color=cfg.MUTED,stroke_width=1.3))
            self.add(equation(str(value),23,cfg.WHITE).move_to(pos+DOWN*0.27))
        self.add(equation(r'r/a_0',27,cfg.WHITE).move_to([3.10,-2.22,0]))
        self.add(equation(r'P(r)=r^2|R_{n\ell}(r)|^2',30,cfg.CYAN)
                 .move_to([-2.65,-2.88,0]))
        self.add(outlined_text('compare at the same radius',24,cfg.MUTED)
                 .move_to([4.30,-2.88,0]))
        self.readers = VGroup()
        for axes,tone in zip(self.axes,tones):
            guide = Line(axes.c2p(0,0),axes.c2p(0,self.ymax),color=tone,
                         stroke_width=1.3,stroke_opacity=0.45)
            point = glow_dot(radius=0.045,color=tone)
            self.readers.add(VGroup(guide,point))

    def start_motion(self) -> None:
        self.add(self.readers)
        self.add_updater(self._advance)

    def _advance(self, _mob, dt: float) -> None:
        self.elapsed += dt*cfg.SPEED
        phase = (self.elapsed/11.0) % 1.0
        radius = self.span*phase
        opacity = min(1.0,phase*18,(1-phase)*18)
        for l,(axes,(guide,point)) in enumerate(zip(self.axes,self.readers)):
            guide.put_start_and_end_on(axes.c2p(radius,0),axes.c2p(radius,self.ymax))
            guide.set_stroke(opacity=0.40*opacity)
            point.move_to(axes.c2p(radius,float(radial_distribution(3,l,radius))))
            point.set_opacity(opacity)


class ShelfLight(VGroup):
    """A light sweep along fixed levels; energies and occupations never move."""

    def __init__(self, shelves: dict, colour: str = cfg.CYAN) -> None:
        super().__init__()
        self.elapsed = 0.0
        self.segments = []
        for shelf in shelves.values():
            start,end = shelf.get_left(),shelf.get_right()
            beam = VGroup(Line(start,start+RIGHT*0.65,color=colour,stroke_width=10,
                               stroke_opacity=0.12),
                          Line(start,start+RIGHT*0.65,color=colour,stroke_width=3.5))
            self.segments.append((beam,start,end))
            self.add(beam)
        self.add_updater(self._advance)
        self._advance(self,0)

    def _advance(self, _mob, dt: float) -> None:
        self.elapsed += dt*cfg.SPEED
        phase = (self.elapsed/4.0) % 1.0
        opacity = np.sin(PI*phase)**2
        for beam,start,end in self.segments:
            beam.move_to(start+RIGHT*0.325+(end-start-RIGHT*0.65)*phase)
            beam[0].set_stroke(opacity=0.17*opacity)
            beam[1].set_stroke(opacity=0.9*opacity)
