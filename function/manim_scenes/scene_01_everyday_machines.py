"""A procedural 3D cold open: complexity becomes a universal translator."""
from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import begin_scene, clear_background, end_scene
from manim_scenes.gateway_models import (
    ICE, VIOLET, beam, bottle, coin, gateway, gauge, label, network,
    pixel_cat, rough_shape, slot, vending_machine,
)


class Scene01EverydayMachines(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: ThreeDScene) -> None:
    started = begin_scene(scene, '01')
    clear_background(scene)
    scene.camera.background_color = '#020814'
    scene.set_camera_orientation(phi=0, theta=-PI/2, zoom=1, frame_center=ORIGIN)
    overlays = []

    def hud(text, position, size=32, color=cfg.WHITE):
        mob = label(text, size, color).move_to(position)
        scene.add_fixed_in_frame_mobjects(mob)
        scene.remove(mob)
        overlays.append(mob)
        return mob

    def until(seconds):
        remaining = seconds - (float(scene.time) - started)
        if remaining < -.14:
            raise ValueError(f'Opening cue {seconds}s overrun by {-remaining:.3f}s')
        if remaining > 1e-6:
            scene.wait(remaining)

    def checkpoint(name):
        callback = getattr(scene, '_opening_review', None)
        if callback:
            callback(scene, name, float(scene.time) - started)

    # Layered colour banks give the void a visible, soft nebula, with depth.
    rng = np.random.default_rng(19)
    stars = VGroup(*[Dot([rng.uniform(-7.6,7.6),rng.uniform(-4.2,4.2),rng.uniform(-3,-1)],
                         radius=rng.uniform(.009,.027),color=ICE,fill_opacity=rng.uniform(.25,.8))
                    for _ in range(110)])
    clouds = VGroup()
    for color, center, angle in [('#257EAA',[-2.4,-.7,-4],.35),
                                  ('#7944BA',[2.5,.9,-4],-.36),
                                  ('#2D588E',[.4,-1.8,-4],.13)]:
        for i in range(18):
            cloud = Ellipse(width=12-i*.38,height=6.2-i*.23,stroke_width=0,
                            fill_color=color,fill_opacity=.027)
            cloud.rotate(angle).move_to(center)
            clouds.add(cloud)
    atmosphere = VGroup(clouds,stars)
    scene.add(atmosphere)

    # 0–4: mathematics first, with large calculus forms beneath a bold title.
    integrals = VGroup()
    for formula, position in zip(
        [r'\int_a^b f(x)\,dx',r'\frac{d}{dx}f(x)',r'\iint_D f\,dA',r'\int_{-\infty}^{\infty}f(x)\,dx'],
        [[-3.6,.8,0],[3.6,.8,0],[-3.6,-1.6,0],[3.6,-1.6,0]],
    ):
        tex = MathTex(formula,font_size=82,color=cfg.GOLD)
        if tex.width > 6.5:
            tex.scale_to_fit_width(6.5)
        tex.move_to(position)
        integrals.add(tex)
    heading = hud('MATHEMATICS',[0,3.12,0],62,cfg.GOLD)
    subheading = hud('CALCULUS',[0,2.38,0],28)
    scene.play(LaggedStart(*[Write(m) for m in integrals],lag_ratio=.17),
               FadeIn(heading,subheading),run_time=4)
    checkpoint('01_mathematics')

    # 4–7: larger Maxwell equations occupy three rows across the frame.
    formulas = [r'\nabla\!\cdot\!\mathbf E=\frac{\rho}{\varepsilon_0}',
                r'\nabla\!\cdot\!\mathbf B=0',
                r'\nabla\!\times\!\mathbf E=-\frac{\partial\mathbf B}{\partial t}',
                r'\nabla\!\times\!\mathbf B=\mu_0\mathbf J+\mu_0\varepsilon_0\frac{\partial\mathbf E}{\partial t}']
    maxwell = VGroup()
    for i,(formula,position) in enumerate(zip(formulas,
                    [[-3.5,1.35,0],[3.5,1.35,0],[0,-.3,0],[0,-2.05,0]])):
        eq = MathTex(formula,font_size=72 if i<2 else 68,color=ICE)
        limit = 6.6 if i<2 else 12.8
        if eq.width > limit:
            eq.scale_to_fit_width(limit)
        eq.move_to(position)
        maxwell.add(eq)
    # These remnants intentionally become the layered complexity behind each
    # new subject. The readable foreground equations are checked separately.
    for mob in integrals:
        mob._is_decorative = True
    physics_heading = hud('PHYSICS',[0,3.12,0],64,ICE)
    scene.play(integrals.animate.set_opacity(.10).shift(IN*.5),
               LaggedStart(*[Write(m) for m in maxwell],lag_ratio=.16),
               FadeOut(heading,subheading),FadeIn(physics_heading),run_time=2)
    scene.wait(1)
    checkpoint('02_physics')

    # 7–10: neural networks and AI are the final layer before condensation.
    for mob in maxwell:
        mob._is_decorative = True
    net = network().scale(1.6).shift(DOWN*.3)
    ai_heading = hud('NEURAL NETWORKS',[0,3.12,0],52,VIOLET)
    ai_subheading = hud('ARTIFICIAL INTELLIGENCE',[0,2.38,0],28)
    scene.play(maxwell.animate.set_opacity(.22),FadeIn(net,scale=1.1),
               FadeOut(physics_heading),FadeIn(ai_heading,ai_subheading),run_time=1)
    scene.play(LaggedStart(*[Indicate(c,color=cfg.WHITE,scale_factor=1.1) for c in net.columns],lag_ratio=.18),run_time=2)
    checkpoint('02_neural_ai')
    # Each system follows its own spiral before the empty centre becomes a gate.
    scene.play(*[Transform(m,m.copy().scale(.015).move_to(ORIGIN).set_opacity(0),
                           path_arc=(-1)**i*PI*.65) for i,m in enumerate([integrals,maxwell,net])],
               FadeOut(ai_heading,ai_subheading),run_time=2,rate_func=rate_functions.ease_in_expo)
    scene.remove(maxwell,net,integrals)
    gate = gateway()
    name = hud('THE FUNCTION',[0,2.65,0],42)
    scene.play(FadeIn(gate,scale=.08),FadeIn(name,shift=UP*.2),run_time=1)
    scene.play(Rotate(gate,angle=.20,axis=UP),run_time=2)
    checkpoint('03_gateway')

    # 15–30: the same object becomes a visible input–rule–output action.
    ports = VGroup(slot(-2.7,cfg.GOLD),slot(2.7,cfg.GREEN))
    words = VGroup(hud('INPUT',[-4.9,1.4,0],30,cfg.GOLD),
                   hud('RULE',[0,2.2,0],30,ICE),hud('OUTPUT',[4.9,1.4,0],30,cfg.GREEN))
    arrows = VGroup(Arrow([-4.1,0,0],[-2.9,0,0],buff=0,color=cfg.GOLD),
                    Arrow([2.9,0,0],[4.1,0,0],buff=0,color=cfg.GREEN))
    scene.play(FadeOut(name),FadeIn(ports),FadeIn(words),GrowFromCenter(arrows),
               gate.frame.animate.set_opacity(.6),run_time=1)
    raw = rough_shape().move_to([-5,0,0])
    scene.play(FadeIn(raw,shift=RIGHT*.4),run_time=1)
    scene.play(raw.animate.move_to([-2.7,0,0]),run_time=1)
    scene.play(raw.animate.move_to(ORIGIN).scale(.7).set_opacity(0),run_time=1)
    scene.remove(raw)
    scene.play(*[Rotate(g,angle=(-1)**i*PI,axis=OUT) for i,g in enumerate(gate.gears)],
               Indicate(gate.panels,color=cfg.WHITE,scale_factor=1),run_time=2)
    smooth = Sphere(radius=.43,resolution=(16,24),checkerboard_colors=False,fill_color=cfg.GREEN,stroke_width=0).move_to(ORIGIN)
    scene.play(FadeIn(smooth,scale=.2),run_time=.6)
    scene.play(smooth.animate.move_to([5,0,0]),run_time=1.4)
    promise = hud('One specified input. One determined output.',[0,-2.3,0],29)
    scene.play(FadeIn(promise),run_time=1)
    checkpoint('04_action')
    until(25)
    fields = hud('CALCULUS  ·  PHYSICS  ·  STATISTICS\nMACHINE LEARNING  ·  AI',[0,-2.9,0],27,ICE)
    scene.play(FadeOut(promise),FadeIn(fields),run_time=1)
    scene.play(*[Rotate(g,angle=(-1)**i*.7,axis=OUT) for i,g in enumerate(gate.gears)],run_time=3)
    scene.play(FadeOut(ports,words,arrows,smooth,fields),run_time=1)

    # 30–36: the device itself is the function, with coin AND selection specified.
    vending = vending_machine()
    heading = hud('A VENDING MACHINE',[0,3.25,0],34)
    inp = hud('COIN + SELECTION',[-4.65,1.45,0],24,cfg.GOLD)
    out = hud('DRINK A',[4.7,1.45,0],27,cfg.GREEN)
    money = coin().move_to([-4.65,.3,0])
    scene.play(ReplacementTransform(gate,vending),FadeIn(heading,inp,money),run_time=1)
    scene.move_camera(zoom=1.08,added_anims=[money.animate.move_to(vending.slot.get_center()).scale(.35)],run_time=1)
    scene.play(FadeOut(money),Indicate(vending.button,color=cfg.WHITE,scale_factor=1.3),run_time=.6)
    drink = bottle().scale(1.35).move_to(vending.tray.get_center()+UP*.6+OUT*.5)
    scene.play(Indicate(vending.rim,color=cfg.WHITE,scale_factor=1.02),FadeIn(drink,shift=DOWN*.3),run_time=.6)
    scene.play(drink.animate.shift(DOWN*.65),run_time=.5,rate_func=rate_functions.ease_in_quad)
    scene.play(drink.animate.move_to([4.5,-.2,.5]).scale(1.25),FadeIn(out),run_time=.8)
    checkpoint('05_vending')
    scene.move_camera(zoom=1,run_time=.5)
    until(36)

    # 36–42: mechanical temperature translator, 10°C -> 50°F.
    dial = gauge()
    next_heading = hud('A TEMPERATURE CONVERTER',[0,3.25,0],34)
    temp = label('10°C',54,cfg.GOLD).move_to([-4.7,0,0])
    fahrenheit = label('50°F',54,cfg.GREEN).move_to([4.7,0,0])
    scene.play(ReplacementTransform(vending,dial),FadeOut(heading,inp,out,drink),FadeIn(next_heading,temp),run_time=1)
    scene.play(temp.animate.move_to([0,0,.5]).scale(.5).set_opacity(0),run_time=1)
    scene.remove(temp)
    scene.play(Rotate(dial.needle,angle=-TAU-PI/4,about_point=dial.pivot),
               *[Rotate(g,angle=(-1)**i*TAU) for i,g in enumerate(dial.cogs)],run_time=2)
    scene.play(FadeIn(fahrenheit,shift=RIGHT*.6),run_time=.6)
    checkpoint('06_temperature')
    until(42)

    # 42–48: a fixed network returns an illustrative score, not an accuracy claim.
    net = network()
    heading = hud('A FIXED IMAGE MODEL',[0,3.25,0],34)
    pixels = pixel_cat().move_to([-4.7,0,0])
    image_label = hud('PIXEL VALUES',[-4.7,1.45,0],25,cfg.GOLD)
    score = hud('98% CAT',[4.65,0,0],43,cfg.GREEN)
    caveat = hud('Illustrative prediction',[0,-2.7,0],25,cfg.MUTED)
    scene.play(ReplacementTransform(dial,net),FadeOut(next_heading,fahrenheit),
               FadeIn(heading,pixels,image_label),run_time=1)
    scene.play(pixels.animate.move_to(net.columns[0].get_center()).scale(.25).set_opacity(0),run_time=1)
    scene.remove(pixels)
    scene.play(LaggedStart(*[AnimationGroup(Indicate(net.columns[i],color=cfg.WHITE,scale_factor=1.2),
                 ShowPassingFlash(net.links[i].copy().set_color(cfg.GREEN),time_width=.6)) for i in range(3)],
                 lag_ratio=.4),run_time=1.8)
    scene.play(Indicate(net.columns[-1],color=cfg.GREEN),FadeIn(score,shift=RIGHT*.5),FadeIn(caveat),run_time=.8)
    checkpoint('07_network')
    until(48)

    # 48–60: unfold the same architecture into a table, coordinates and a graph.
    gate = gateway()
    heading2 = hud('NUMBERS. TABLES. GRAPHS.',[0,3.25,0],34)
    scene.play(ReplacementTransform(net,gate),FadeOut(heading,score,caveat,image_label),FadeIn(heading2),run_time=.8)
    scene.play(Rotate(gate.panels[0],angle=-PI/2,axis=UP,about_point=gate.panels[0].get_left()),
               Rotate(gate.panels[1],angle=PI/2,axis=UP,about_point=gate.panels[1].get_right()),
               gate.frame.animate.stretch(1.5,0),run_time=1.2)
    table = MathTable([['-2','4'],['0','0'],['2','4']],col_labels=[MathTex('x'),MathTex('y')],
                      include_outer_lines=True,h_buff=.75,v_buff=.22).scale(.72).move_to([-4.8,0,0])
    table.get_columns()[0].set_color(cfg.GOLD)
    table.get_columns()[1].set_color(cfg.GREEN)
    scene.play(FadeIn(table,shift=LEFT*.3),run_time=1)
    checkpoint('08_unfold')
    plane = NumberPlane(x_range=[-3,3,1],y_range=[-1,5,1],x_length=8,y_length=4.7,
                        background_line_style={'stroke_color':ICE,'stroke_opacity':.17,'stroke_width':1},
                        axis_config={'stroke_color':cfg.MUTED,'stroke_width':2},tips=False).move_to([0,-.25,0])
    axis_labels = VGroup(MathTex('x',color=cfg.GOLD).next_to(plane.x_axis.get_end(),RIGHT,buff=.15),
                         MathTex('y',color=cfg.GREEN).next_to(plane.y_axis.get_end(),UP,buff=.12))
    curve = plane.plot(lambda x:x*x,x_range=[-2,2,.025],color=ICE,stroke_width=4)
    point = Dot(plane.c2p(-2,4),radius=.09,color=cfg.GOLD)
    # Separate owned parts before transformations to avoid duplicate parent draws.
    scene.remove(gate)
    metal = VGroup(*gate.frame[:8])
    lattice = VGroup(*gate.frame[8:])
    scene.add(metal,lattice,gate.panels,gate.logic)
    # Unfold the luminous edges, rather than interpolating filled prism faces
    # into open grid lines (which produces opaque triangular flashes).
    scene.play(lattice.animate.stretch(1.8,0).stretch(.04,2).set_opacity(0),
               Create(plane),FadeOut(metal,gate.panels,table),
               gate.logic.animate.scale(.03).move_to(point.get_center()).set_opacity(0),
               FadeIn(point,scale=.2),FadeIn(axis_labels),run_time=2)
    scene.remove(lattice,gate.logic)
    point_name = MathTex('P(x,y)',font_size=30).next_to(point,UR,buff=.12)
    point_name.add_updater(lambda m:m.next_to(point,UR,buff=.12))
    scene.add(point_name)
    scene.play(Create(curve),MoveAlongPath(point,curve),run_time=4,rate_func=linear)
    point_name.clear_updaters()
    checkpoint('09_graph')
    until(58.5)
    scene.play(FadeOut(plane,axis_labels,curve,point,point_name,heading2),run_time=1)
    until(60)

    # A six-second question card gives the viewer a breath before the first lesson.
    title = VGroup(label('WHAT DOES A',45),label('FUNCTION',84,ICE),label('ACTUALLY DO?',51))
    title.arrange(DOWN,buff=.24).move_to([0,.45,0])
    subtitle = label('INPUT  →  RULE  →  OUTPUT',28,cfg.GOLD).move_to([0,-1.65,0])
    underline = beam([-2.4,-2.15,0],[2.4,-2.15,0],ICE,2)
    scene.play(FadeIn(title,shift=UP*.2),GrowFromCenter(underline),run_time=.8)
    scene.play(FadeIn(subtitle),run_time=.6)
    checkpoint('10_title')
    until(65.3)
    end_scene(scene,started,cfg.SCENE_DURATIONS['01'])
    scene.remove_fixed_in_frame_mobjects(*overlays)
    scene.set_camera_orientation(phi=0,theta=-PI/2,zoom=1,frame_center=ORIGIN)
    scene.camera.background_color = cfg.BG
