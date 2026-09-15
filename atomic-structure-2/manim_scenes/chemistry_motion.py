"""Scene 16: moving shell markers and turning views of schematic density.

Only the historical shell picture has orbiting electrons. Density samples are
rigidly reoriented as a viewing aid, preserving their radii and relative
geometry. Colour and brightness distinguish the valence region from the core.
"""
from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import cloud, glow_dot, nucleus

OUTER_CYAN = "#A1F6FF"
OUTER_GOLD = "#FFE36A"
INNER_BLUE = "#74ACD2"
DENSITY_SCALE = 0.60


class ShellRotation(VMobject):
    """Move every bead on its live ring, including during narration holds."""

    def __init__(self, atom: VGroup) -> None:
        super().__init__()
        self.tracks = []
        for shell, beads in atom.electrons.items():
            ring = atom.rings[shell]
            centre = ring.get_center()
            tone = OUTER_GOLD if shell == 3 else OUTER_CYAN
            radius = 0.089 if shell == 3 else 0.064
            for bead in beads:
                point = bead.get_center()
                phase = np.arctan2(point[1]-centre[1],point[0]-centre[0])
                bright = glow_dot(point,radius=radius,color=tone)
                bright.add(Dot(point,radius=0.032 if shell == 3 else 0.024,color=cfg.WHITE))
                bead.become(bright)
                self.tracks.append([ring,bead,phase,4.0+2.0*shell])
        atom.rings[3].set_stroke(OUTER_GOLD,opacity=0.48)
        self.add_updater(self._advance)

    def _advance(self, _mob, dt: float) -> None:
        for item in self.tracks:
            ring,bead,phase,period = item
            phase += TAU*dt*cfg.SPEED/period
            item[2] = phase % TAU
            start = ring.point_from_proportion(0)
            centre = (start+ring.point_from_proportion(0.5))/2
            horizontal = start-centre
            vertical = ring.point_from_proportion(0.25)-centre
            bead.move_to(centre+np.cos(phase)*horizontal+np.sin(phase)*vertical)


def _density_layer(n: int, l: int, m: int, count: int, scale: float,
                   colour: str, outer: bool) -> VGroup:
    """Style fixed samples at a common display scale, with no sample motion."""
    samples = cloud(n,l,m,count=count,scale=scale)
    layer = VGroup()
    radius = 0.047 if outer else 0.027
    for sample in samples:
        point = sample.get_center()*DENSITY_SCALE
        if outer:
            layer.add(VGroup(
                Dot(point,radius=radius*1.95,color=colour,fill_opacity=0.12),
                Dot(point,radius=radius,color=colour,fill_opacity=0.96),
            ))
        else:
            layer.add(Dot(point,radius=radius,color=colour,fill_opacity=0.60))
    return layer


def neon_density(centre) -> VGroup:
    """A compact core and a bright closed outer-shell schematic."""
    core = _density_layer(1,0,0,100,0.40,INNER_BLUE,False)
    outer = VGroup(_density_layer(2,0,0,100,0.72,OUTER_CYAN,True))
    outer.add(*[_density_layer(2,1,m,100,0.72,OUTER_CYAN,True) for m in (-1,0,1)])
    atom = VGroup(nucleus(0.24).set_z_index(2),core,outer).shift(centre)
    atom.density_layers = [core,*outer]
    atom.view_centre = np.array(centre,dtype=float)
    return atom


def sodium_density(centre) -> VGroup:
    """A blue compact core and a gold, more extended 3s schematic."""
    core = _density_layer(1,0,0,210,0.55,INNER_BLUE,False)
    outer = _density_layer(3,0,0,180,1.0,OUTER_GOLD,True)
    atom = VGroup(nucleus(0.24).set_z_index(2),core,outer).shift(centre)
    atom.density_layers = [core,outer]
    atom.view_centre = np.array(centre,dtype=float)
    return atom


class DensityViewMotion(VMobject):
    """Rigid viewing rotation; these points do not trace electron trajectories.

    Each atom turns about its nucleus. Every sample's radius and every pairwise
    distance stays fixed. This updater changes positions only, leaving the
    sodium valence FadeOut in full control of opacity during ionization.
    """

    def __init__(self, atoms) -> None:
        super().__init__()
        self.elapsed = 0.0
        self.samples = []
        for atom in atoms:
            centre = atom.view_centre
            for layer in atom.density_layers:
                for bead in layer:
                    self.samples.append((bead,centre,bead.get_center()-centre))
        self.add_updater(self._advance)

    def _advance(self, _mob, dt: float) -> None:
        self.elapsed += dt*cfg.SPEED
        angle = 0.085*self.elapsed
        # A fixed tilted axis gives a slow, coherent change in viewpoint.
        transform = rotation_matrix(angle,np.array([0.35,1.0,0.20]))
        for bead,centre,original in self.samples:
            bead.move_to(centre+transform@original)
