"""Glassware, flowing liquid and cold condensation for the cryogenic experiments.

The liquid follows the existing seeded magnetic-capture paths. White mist is
an atmospheric condensation effect, not the colour of either gas. All motion
is deterministic; the beaker lip coincides with the simulated stream source.
"""
from __future__ import annotations

import numpy as np
from manim import (Arc, Circle, Ellipse, Group, ImageMobject, LEFT, Line,
                   ORIGIN, Polygon, RIGHT, UP, VGroup, VMobject)
from scipy.ndimage import gaussian_filter

import config as cfg
from utils import math_utils as mu
from utils import physics_models as pm


def _clip_below(points: np.ndarray, level: float) -> np.ndarray:
    """Clip the vessel's interior by a horizontal, gravity-level liquid surface."""
    result = []
    for a, b in zip(points, np.roll(points, -1, axis=0)):
        inside_a, inside_b = a[1] <= level, b[1] <= level
        if inside_a:
            result.append(a)
        if inside_a != inside_b:
            result.append(a + (b-a) * ((level-a[1]) / (b[1]-a[1])))
    return np.array(result)


def _mist_texture(seed: int) -> np.ndarray:
    """A soft, transparent turbulent wisp, generated from seeded density noise."""
    rng = np.random.default_rng(seed)
    h, w = 96, 192
    yy, xx = np.mgrid[-1:1:complex(h), -1:1:complex(w)]
    noise = gaussian_filter(rng.normal(size=(h, w)), 5.0)
    noise /= max(float(noise.std()), 1e-8)
    fine = gaussian_filter(rng.normal(size=(h, w)), 1.5)
    fine /= max(float(fine.std()), 1e-8)
    curl = yy + .18*np.sin(4*xx + seed % 7)
    envelope = np.exp(-2.8*xx*xx - 6.0*curl*curl)
    density = np.clip(.50 + .21*noise + .055*fine, 0, 1)*envelope
    density = gaussian_filter(density, 1.1)
    rgba = np.empty((h, w, 4), dtype=np.uint8)
    rgba[..., :3] = [220, 237, 246]
    rgba[..., 3] = np.uint8(np.clip(density*145, 0, 255))
    return rgba


class GlassBeaker(VGroup):
    """An inclined transparent cylinder with an elliptical rim and a pouring lip."""

    def __init__(self, lip, scale: float, color: str, *, shadow: str = "#408CB8") -> None:
        super().__init__()
        self.lip = np.asarray(lip, dtype=float)
        self.unit = .80*scale
        angle = -.65
        self.rotation = np.array([[np.cos(angle), -np.sin(angle), 0],
                                  [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
        self.offset = self.lip - self._vector([.88, .82, 0])

        def world(p):
            return self._vector(p)+self.offset
        self.world = world

        # The rear rim is visible through the body; the front lip is redrawn last.
        rim = Ellipse(width=1.53, height=.28, stroke_color="#C8E5F2", stroke_width=2.2,
                      stroke_opacity=.65, fill_color="#7FAEC8", fill_opacity=.045).shift(UP*.82)
        rim.rotate(angle, about_point=ORIGIN).scale(self.unit, about_point=ORIGIN).shift(self.offset)
        shell = VMobject(stroke_color="#BCDCEB", stroke_width=2.0, stroke_opacity=.64,
                         fill_color="#A5CEE0", fill_opacity=.055)
        shell.start_new_path(world([-.75, .82, 0]))
        shell.add_line_to(world([-.67, -.68, 0]))
        shell.add_cubic_bezier_curve_to(world([-.64, -.88, 0]), world([.64, -.88, 0]), world([.67, -.68, 0]))
        shell.add_line_to(world([.75, .73, 0]))
        self.inner = np.array([world(p) for p in ((-.66,.76,0),(.66,.76,0),(.59,-.68,0),(-.59,-.68,0))])
        self.water = VGroup(*[VMobject(stroke_width=0, fill_color=mu.mix(shadow, color, k/11),
                                      fill_opacity=.07 if k else .42) for k in range(12)])
        self.meniscus = Ellipse(width=1, height=.10, stroke_color="#DCFAFF", stroke_width=1.0,
                                stroke_opacity=.65, fill_color=color, fill_opacity=.45)
        reflections = VGroup()
        for x, width, alpha in ((-.55,.075,.18),(-.45,.025,.25),(.53,.035,.22)):
            band = Polygon(*[world(p) for p in ((x-width/2,.56,0),(x+width/2,.56,0),
                                               (x+width/2,-.58,0),(x-width/2,-.58,0))],
                           stroke_width=0, fill_color=cfg.WHITE, fill_opacity=alpha)
            reflections.add(band)
        # Etched graduations, without tiny text competing with the explanation.
        for i, y in enumerate(np.linspace(-.42,.42,5)):
            reflections.add(Line(world([-.26,y,0]),world([-.04 if i%2==0 else -.12,y,0]),
                                 stroke_color="#D8EEF6",stroke_width=1.2,stroke_opacity=.48))
        foot = Arc(radius=.66, start_angle=np.pi, angle=np.pi, stroke_color="#DDF4FF",stroke_width=2.2,
                   stroke_opacity=.4).stretch(.23,1).shift(UP*-.68)
        foot.rotate(angle,about_point=ORIGIN).scale(self.unit,about_point=ORIGIN).shift(self.offset)
        lip_rim = VMobject(stroke_color="#E2F5FD",stroke_width=2.8,stroke_opacity=.9)
        lip_rim.set_points_smoothly(np.array([world(p) for p in ((-.72,.80,0),(-.20,.70,0),(.52,.75,0),(.88,.82,0))]))
        lip_glint = Line(world([.71,.80,0]),self.lip,stroke_color=cfg.WHITE,stroke_width=2.3,stroke_opacity=.8)
        self.add(rim,self.water,self.meniscus,shell,reflections,foot,lip_rim,lip_glint)
        self.set_fill_level(0)

    def _vector(self, point):
        return np.asarray(point,dtype=float) @ self.rotation.T*self.unit

    def set_fill_level(self, progress: float) -> None:
        level = self.lip[1] + .035*(1-np.clip(progress,0,1))
        for k, layer in enumerate(self.water):
            pts=self.inner.copy()
            # Nested refraction bands stay within the same glass interior.
            centre=pts.mean(axis=0)
            pts[:,0]=centre[0]+(pts[:,0]-centre[0])*(1-.035*k)
            poly=_clip_below(pts,level)
            if len(poly)>=3:
                layer.set_points_as_corners(np.vstack([poly,poly[:1]]))
        poly=_clip_below(self.inner,level)
        crossings=poly[np.abs(poly[:,1]-level)<1e-6]
        if len(crossings)>=2:
            left,right=crossings[:,0].min(),crossings[:,0].max()
            self.meniscus.stretch_to_fit_width(max(right-left,.02))
            self.meniscus.move_to([(left+right)/2,level,0])
        else:
            self.meniscus.set_opacity(0)


class CryogenicPour(Group):
    """A readable laboratory illustration with a glass beaker and cold mist."""

    def __init__(self, magnet, *, paramagnetic: bool=True, drops: int=90, seed: int=0, duration: float=8.0) -> None:
        super().__init__()
        self.magnet=magnet
        self.paramagnetic=paramagnetic
        self.sim=pm.pour(paramagnetic,drops=drops,seed=seed,duration=duration,geo=magnet.geo)
        self.origin=magnet.gap_center-UP*magnet.geo.gap_y*magnet.scale_factor
        self.color=cfg.LIQUID_O2 if paramagnetic else cfg.LIQUID_N2
        self.clock,self.running=0.0,False
        s=magnet.scale_factor
        lip=self.origin+np.array([magnet.geo.nozzle_x,magnet.geo.nozzle_y,0])*s
        self.flask=GlassBeaker(lip,s,self.color,shadow="#408CB8" if paramagnetic else "#819BA7")
        self.mist=Group()
        self.mist_specs=[]
        for i in range(22):
            image=ImageMobject(_mist_texture(seed+i*17))
            image.stretch_to_fit_width(1);image.stretch_to_fit_height(1)
            template=image.points.copy()-image.get_center()
            phase=(i*.61803398875)%1
            self.mist.add(image)
            self.mist_specs.append((image,template,phase,i>=14))
        jet_tones=("#64B5DC","#9DDAF4","#E4FAFF") if paramagnetic else ("#9FB7C4","#E3EEF5","#FFFFFF")
        self.jet=VGroup(*[VMobject(stroke_color=color,stroke_width=width,stroke_opacity=0)
                               for color,width in zip(jet_tones,(12,5.5,1.6))])
        # Oxygen joins the supported liquid; nitrogen continues through the gap.
        path=self.sim.paths[0]
        end=(next((i for i,p in enumerate(path) if p[1]<magnet.geo.gap_y+.25),len(path)-1)
             if paramagnetic else len(path)-1)
        self.jet_local=path[:end+1]
        self.jet_ages=np.arange(len(self.jet_local))*self.sim.dt
        self.drops=VGroup()
        for i in range(drops):
            body=Ellipse(width=.075*s,height=.12*s,stroke_width=0,fill_color=self.color,fill_opacity=0)
            shine=Ellipse(width=.025*s,height=.047*s,stroke_width=0,fill_color="#E9FAFF",fill_opacity=0)
            self.drops.add(VGroup(body,shine))
        self.bridge=VGroup(*[VMobject(stroke_width=0,fill_color=mu.mix("#3C86B4","#C1EBFF",k/15),fill_opacity=0)
                                  for k in range(16)])
        self.water_line=VMobject(stroke_color="#E6FCFF",stroke_width=1.5,stroke_opacity=0)
        self.caustics=VGroup(*[VMobject(stroke_color="#D5F5FF",stroke_width=1.0,stroke_opacity=0) for _ in range(3)])
        self.add(self.mist,self.jet,self.bridge,self.water_line,self.caustics,self.drops,self.flask)
        self.apply_clock()
        self.add_updater(lambda m,dt:m._advance(dt))

    def _advance(self,dt:float)->None:
        if self.running:
            self.clock+=dt
            self.apply_clock()

    def apply_clock(self)->None:
        t=self.clock;s=self.magnet.scale_factor;c=self.magnet.gap_center
        pts,seen=self.sim.positions(t)
        caught=self.sim.captured_by(t)/max(len(self.sim.paths),1)
        fill=np.clip(caught*3.0,0,1)
        # Captured droplets coalesce into a connected volume instead of staying
        # as bright particle dots, which could be mistaken for electrons.
        for i,(drop,p,v) in enumerate(zip(self.drops,pts,seen)):
            age=t-self.sim.births[i]
            rest=age-(len(self.sim.paths[i])-1)*self.sim.dt
            alpha=float(v)*(max(0,1-rest/.18) if self.sim.captured[i] and rest>0 else 1)
            drop[0].move_to(self.origin+np.array([p[0],p[1],0])*s).set_fill(opacity=.68*alpha)
            drop[1].move_to(drop[0].get_center()+np.array([-.014,.022,0])*s).set_fill(opacity=.65*alpha)
        ages=self.jet_ages
        tail=max(0,t-float(self.sim.births[-1]))
        valid=(ages<=t)&(ages>=tail)
        jet=self.jet_local[valid]
        if len(jet)>=2:
            points=self.origin+np.column_stack([jet,np.zeros(len(jet))])*s
            points[:,0]+=.008*np.sin(points[:,1]*13-t*11)
            for layer,opacity in zip(self.jet,(.11,.5,.55)):
                layer.set_points_smoothly(points).set_stroke(opacity=opacity)
        else:
            self.jet.set_stroke(opacity=0)
        # A curved underside and bright meniscus convey a liquid bridge.
        xs=np.linspace(-.71,.71,42)
        ripple=.012*np.sin(10*xs+t*2.2)
        for k,body in enumerate(self.bridge):
            f=1-k*.025
            half=.71*(.25+.75*fill)*f
            x=xs/.71*half
            top=.15+.065*(x/max(half,.01))**2+ripple
            bottom=-.17-.22*(1-(x/max(half,.01))**2)
            ytop=top*(.3+.7*fill)*f+.018*k
            ybottom=bottom*(.3+.7*fill)*f+.018*k
            outline=np.vstack([np.column_stack([x,ytop,np.zeros(len(x))]),
                               np.column_stack([x[::-1],ybottom[::-1],np.zeros(len(x))])])
            world=c+outline*s
            body.set_points_smoothly(np.vstack([world,world[:1]])).set_fill(opacity=fill*(.72 if k==0 else .065))
        line=c+np.column_stack([xs*(.25+.75*fill),.15+.065*(xs/.71)**2+ripple,np.zeros(len(xs))])*s
        self.water_line.set_points_smoothly(line).set_stroke(opacity=.75*fill)
        for k,curve in enumerate(self.caustics):
            x=np.linspace(-.52,.52,30)
            y=-.05-.065*k+.012*np.sin(x*9+t*2+k)
            curve.set_points_smoothly(c+np.column_stack([x,y,np.zeros(len(x))])*s)
            curve.set_stroke(opacity=(.13+.07*np.sin(t+k)**2)*fill)
        self.flask.set_fill_level(np.clip(t/(self.sim.duration*.8),0,1))
        for i,(image,template,phase,at_lip) in enumerate(self.mist_specs):
            age=(t/(3.6 if at_lip else 5.0)+phase)%1
            if at_lip:
                centre=self.flask.lip+np.array([.22*np.sin(i*2+age*5),-.08-age*1.65,0])
                width=.60+.75*age;height=.28+.40*age
                strength=min(t/1.2,1)*.52
            else:
                side=-1 if i%2 else 1
                centre=c+np.array([side*(.15+age*.95)+.12*np.sin(age*6+i),-.30-age*1.30,0])*s
                width=.75+age*1.35;height=.35+age*.52
                strength=min(t/2.0,1)*((.18+.65*fill) if self.paramagnetic else .35)
            fade=np.sin(np.pi*age)**1.3
            image.points=template*np.array([width,height,1])+centre
            image.set_opacity(strength*fade)

    def run(self,on:bool=True)->None:
        self.running=on
