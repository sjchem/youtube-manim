"""Procedural 3D props for the Universal Translator opening; core Manim only."""
from __future__ import annotations

import numpy as np
from manim import *
import config as cfg

METAL = '#12334D'
DARK = '#061423'
ICE = '#57DEFF'
VIOLET = '#9671FF'


def label(text, size=34, color=cfg.WHITE):
    return Text(text, font='DejaVu Sans', font_size=size, color=color, weight=BOLD)


def beam(a, b, color=ICE, width=3):
    return VGroup(Line(a,b,color=color,stroke_width=width*4,stroke_opacity=.10),
                  Line(a,b,color=color,stroke_width=width))


def solid(dimensions, color=METAL, opacity=1):
    return Prism(dimensions=dimensions, fill_color=color, fill_opacity=opacity,
                 stroke_color=color, stroke_width=.5)


def gear(radius=.5, teeth=12, color=ICE):
    points=[]
    for i in range(teeth*4):
        a=TAU*i/(teeth*4)
        r=radius*(1 if i%4 in (1,2) else .83)
        points.append([r*np.cos(a),r*np.sin(a),0])
    rim=Polygon(*points,stroke_color=color,stroke_width=2.5,fill_color=color,fill_opacity=.14)
    hub=Circle(radius=radius*.26,color=color,stroke_width=3,fill_color=DARK,fill_opacity=1)
    spokes=VGroup(*[Line(radius*.30*np.array([np.cos(a),np.sin(a),0]),
                        radius*.72*np.array([np.cos(a),np.sin(a),0]),color=color,stroke_width=2)
                   for a in np.linspace(0,TAU,6,endpoint=False)])
    return VGroup(rim,hub,spokes)


def gateway():
    """A translucent architectural gate with real depth and moving logic inside."""
    frame=VGroup()
    for x in (-1.55,1.55):
        for z in (-.65,.65):
            frame.add(solid([.12,2.85,.12]).move_to([x,0,z]))
    for y in (-1.38,1.38):
        for z in (-.65,.65):
            frame.add(solid([3.2,.12,.12]).move_to([0,y,z]))
    for x in (-1.55,1.55):
        for y in (-1.38,1.38):
            frame.add(beam([x,y,-.65],[x,y,.65],width=2))
    for z in (-.67,.67):
        for y in (-1.4,1.4):
            frame.add(beam([-1.6,y,z],[1.6,y,z],width=3))
        for x in (-1.6,1.6):
            frame.add(beam([x,-1.4,z],[x,1.4,z],width=3))
    panels=VGroup(
        Polygon([-1.5,-1.32,.69],[0,-1.32,.69],[0,1.32,.69],[-1.5,1.32,.69],
                fill_color=ICE,fill_opacity=.055,stroke_color=ICE,stroke_width=1),
        Polygon([0,-1.32,.69],[1.5,-1.32,.69],[1.5,1.32,.69],[0,1.32,.69],
                fill_color=ICE,fill_opacity=.055,stroke_color=ICE,stroke_width=1))
    gears=VGroup(gear(.62,14).move_to([-.47,.15,0]),
                 gear(.41,11,VIOLET).move_to([.57,-.10,.05]),
                 gear(.26,9,cfg.GOLD).move_to([.05,-.69,.05]))
    # Two nested, differently oriented rings give the logic a volumetric core.
    orbit=VGroup(Circle(radius=1.08,color=ICE,stroke_width=1.5,stroke_opacity=.45).rotate(PI/3,RIGHT),
                 Circle(radius=.95,color=VIOLET,stroke_width=1.5,stroke_opacity=.45).rotate(PI/3,UP))
    logic=VGroup(gears,orbit)
    g=VGroup(frame,panels,logic)
    g.frame,g.panels,g.logic,g.gears=frame,panels,logic,gears
    g.rotate(-.24,RIGHT).rotate(-.55,UP)
    return g


def slot(x, color):
    body=solid([.14,1.55,.65],DARK).move_to([x,0,0])
    rim=VGroup(beam([x,-.8,.36],[x,.8,.36],color,4),
               beam([x,-.8,-.36],[x,.8,-.36],color,2))
    return VGroup(body,rim)


def rough_shape():
    angles=np.linspace(0,TAU,7,endpoint=False)
    radii=[.45,.33,.49,.32,.44,.30,.40]
    front=[np.array([r*np.cos(a),r*np.sin(a),.15]) for a,r in zip(angles,radii)]
    back=[p-np.array([0,0,.30]) for p in front]
    faces=VGroup(Polygon(*front,fill_color=cfg.GOLD,fill_opacity=1,stroke_width=1,stroke_color='#FFE4A5'),
                 Polygon(*back,fill_color='#926B25',fill_opacity=1,stroke_width=0))
    for i in range(len(front)):
        j=(i+1)%len(front)
        faces.add(Polygon(front[i],front[j],back[j],back[i],fill_color='#B38434',fill_opacity=1,
                          stroke_color=cfg.GOLD,stroke_width=.7))
    return faces.rotate(.3,UP)


def bottle():
    heights=np.array([0,.08,.16,.66,.84,1.0,1.15,1.22])
    radii=np.array([.19,.245,.245,.225,.20,.095,.095,.10])
    surface=Surface(lambda h,a: np.array([np.interp(h,heights,radii)*np.cos(a),h,
                                         np.interp(h,heights,radii)*np.sin(a)]),
                    u_range=[0,1.22],v_range=[0,TAU],resolution=(16,24),
                    checkerboard_colors=False,fill_color='#36AD91',fill_opacity=.95,
                    stroke_width=0)
    cap=solid([.23,.12,.23],'#ED7674').move_to([0,1.25,0])
    band=Rectangle(width=.45,height=.29,fill_color=cfg.GOLD,fill_opacity=1,stroke_width=0).move_to([0,.53,.25])
    name=label('SODA',15,DARK).scale_to_fit_width(.36).move_to([0,.53,.27])
    shine=Line([-.13,.19,.21],[-.11,.77,.21],color='#D0FFF3',stroke_width=2,stroke_opacity=.7)
    return VGroup(surface,cap,band,name,shine).move_to(ORIGIN)


def vending_machine():
    body=solid([2.95,4.0,1.35])
    window=RoundedRectangle(width=1.83,height=2.62,corner_radius=.12,
                            fill_color='#123D59',fill_opacity=.85,stroke_color=ICE,stroke_width=2)
    window.move_to([-.34,.37,.70])
    shelves=VGroup()
    for y in (-.15,.65,1.43):
        shelves.add(beam([-1.19,y-.37,.78],[.52,y-.37,.78],ICE,1.5))
        for x in (-.85,-.3,.25):
            mini=Polygon([-.13,-.24,0],[.13,-.24,0],[.12,.15,0],[.06,.24,0],
                         [.06,.35,0],[-.06,.35,0],[-.06,.24,0],[-.12,.15,0],
                         color='#7CF3C7',stroke_width=.8,fill_opacity=.65)
            mini.move_to([x,y,.81]);shelves.add(mini)
    plate=solid([.52,1.0,.08],'#31536C').move_to([1.02,.54,.74])
    coin_slot=RoundedRectangle(width=.10,height=.52,corner_radius=.03,fill_color='#000812',fill_opacity=1,
                               stroke_color=cfg.GOLD,stroke_width=2).move_to([1.02,.69,.81])
    button=solid([.35,.32,.12],cfg.GOLD).move_to([1.02,-.13,.79])
    button_text=label('A',22,DARK).move_to([1.02,-.13,.87])
    tray=solid([2.22,.47,.65],DARK).move_to([-.20,-1.55,.73])
    tray_light=beam([-1.22,-1.77,1.07],[.81,-1.77,1.07],cfg.GREEN,3)
    rim=RoundedRectangle(width=2.85,height=3.9,corner_radius=.16,stroke_color=ICE,stroke_width=3.5)
    rim.move_to([0,0,.71])
    name=label('SELECT',23,ICE).move_to([1.02,1.31,.83]).scale(.62)
    g=VGroup(body,window,shelves,plate,coin_slot,button,button_text,tray,tray_light,rim,name)
    g.slot,g.button,g.tray,g.rim=coin_slot,button,tray,rim
    g.rotate(-.11,RIGHT).rotate(-.24,UP)
    return g


def coin():
    disc=Cylinder(radius=.34,height=.08,direction=OUT,resolution=(1,24),fill_color=cfg.GOLD,
                  checkerboard_colors=False,stroke_width=0)
    ring=Circle(radius=.27,color='#FFF1B5',stroke_width=2).shift(OUT*.055)
    mark=label('$',27,DARK).shift(OUT*.065)
    return VGroup(disc,ring,mark).rotate(.3,UP)


def gauge():
    casing=Cylinder(radius=1.86,height=.45,direction=OUT,resolution=(1,40),
                    fill_color='#254960',checkerboard_colors=False,stroke_width=0)
    face=Circle(radius=1.72,fill_color=DARK,fill_opacity=1,stroke_color=ICE,stroke_width=3).shift(OUT*.25)
    bezel=Circle(radius=1.83,stroke_color=ICE,stroke_width=4).shift(OUT*.26)
    ticks=VGroup()
    for a in np.linspace(PI*.15,PI*.85,29):
        ticks.add(Line([1.43*np.cos(a),1.43*np.sin(a),.28],
                       [1.60*np.cos(a),1.60*np.sin(a),.28],color=cfg.MUTED,stroke_width=2))
    for value,a in zip(['32','50','68'],[3*PI/4,PI/2,PI/4]):
        ticks.add(label(value,24).move_to([1.19*np.cos(a),1.19*np.sin(a),.29]))
    units=label('°F',25,ICE).move_to([.82,-.35,.31])
    cogs=VGroup(gear(.46,12,ICE).move_to([-.60,-.68,.31]),
                gear(.32,10,VIOLET).move_to([.30,-.90,.31]))
    needle=VGroup(Line([0,0,.42],[1.12,0,.42],color=cfg.GOLD,stroke_width=5),
                  Dot([0,0,.43],radius=.11,color=cfg.GOLD))
    needle.rotate(3*PI/4,OUT,about_point=[0,0,.42])
    g=VGroup(casing,face,bezel,ticks,units,cogs,needle)
    g.needle,g.cogs,g.pivot=needle,cogs,np.array([0,0,.42])
    return g


def network():
    columns=VGroup();links=VGroup()
    for i,count in enumerate([4,5,4,2]):
        col=VGroup()
        for j,y in enumerate(np.linspace(-1.2,1.2,count)):
            dot=Dot3D([i*1.15-1.725,y,.28*(-1)**j],radius=.115,color=ICE,resolution=(4,6))
            col.add(dot)
        columns.add(col)
    for a,b in zip(columns[:-1],columns[1:]):
        links.add(VGroup(*[Line(p.get_center(),q.get_center(),stroke_width=1.5,
                               stroke_opacity=.38,color=VIOLET) for p in a for q in b]))
    g=VGroup(links,columns)
    g.columns,g.links=columns,links
    g.rotate(-.13,RIGHT).rotate(-.22,UP)
    return g


def pixel_cat():
    mask=['01000010','01100110','01111110','11111111','11011011','11111111','01100110','00111100']
    pixels=VGroup()
    for y,row in enumerate(mask):
        for x,value in enumerate(row):
            pixels.add(Square(side_length=.145,fill_color=cfg.GOLD if value=='1' else '#133246',
                              fill_opacity=1,stroke_width=.35,stroke_color=DARK).move_to([(x-3.5)*.155,(3.5-y)*.155,.1]))
    back=solid([1.34,1.34,.15],METAL)
    return VGroup(back,pixels).rotate(-.15,UP)
