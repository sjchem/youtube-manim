"""Animatable objects and environments for the Oceanic pizza-club story.

Pictures occupy y=-2.7..2.5, the question lives at y=3.65, and one brief
caption/formula occupies y=-3.65. Characters and ingredients are objects,
not rectangular cards. Prose uses the project's Arial-compatible font; mathematics is typeset.
"""
from __future__ import annotations
import numpy as np
from manim import *
import config as cfg
from manim_scenes.icons import icon
from manim_scenes.common import begin_scene, cue, end_scene


def label(words, size=34, color=cfg.WHITE):
    text = Text(words, font=cfg.FONT_FAMILY, font_size=size, color=color, weight=BOLD)
    text.set_z_index(20)
    return text


def formula(words, size=52, color=cfg.GOLD):
    return label(words, size, color)


def heading(words):
    mob = label(words, 40).move_to([0, 3.65, 0])
    if mob.width > 13.5: mob.scale_to_fit_width(13.5)
    return mob


def footer(words, color=cfg.CYAN):
    mob = label(words, 36, color).move_to([0, -3.78, 0])
    if mob.width > 13.2: mob.scale_to_fit_width(13.2)
    return mob


def start(scene, key, title=None):
    at = begin_scene(scene, key)
    if isinstance(scene, ThreeDScene):
        scene.set_camera_orientation(phi=0, theta=-PI/2, zoom=1, frame_center=ORIGIN)
    # Use the user's actual local theme bubbles, with no replacement grid.
    bubbles = cfg.oceanic_bubbles().set_z_index(-30)
    bubbles._is_project_background = True
    scene.add(bubbles)
    if isinstance(scene, ThreeDScene):
        scene.add_fixed_in_frame_mobjects(bubbles)
    head = heading(title) if title else None
    if head is not None:
        head._is_project_hud = True
        if isinstance(scene, ThreeDScene): scene.add_fixed_in_frame_mobjects(head)
        scene.add(head)
    return at, head


def clear(scene, *keep):
    preserve = {id(m) for m in keep if m is not None}
    visible = [m for m in scene.mobjects if id(m) not in preserve and not getattr(m,'_is_project_background',False)]
    if visible: scene.play(FadeOut(*visible), run_time=.65)
    if isinstance(scene, ThreeDScene):
        for mob in visible: scene.remove_fixed_in_frame_mobjects(mob)


def finish(scene):
    # Clean up fixed registrations as well as objects when composing FullVideo.
    if isinstance(scene, ThreeDScene):
        scene.set_camera_orientation(phi=0,theta=-PI/2,zoom=1,frame_center=ORIGIN)
        for mob in list(scene.camera.fixed_in_frame_mobjects):
            scene.remove_fixed_in_frame_mobjects(mob)
    scene.clear()


def change(scene, old, words, color=cfg.CYAN):
    new = footer(words, color)
    new._is_project_hud = True
    if isinstance(scene,ThreeDScene): scene.add_fixed_in_frame_mobjects(new); scene.remove(new)
    if old is not None:
        scene.play(FadeOut(old), run_time=.22)
        if isinstance(scene, ThreeDScene): scene.remove_fixed_in_frame_mobjects(old)
        scene.play(FadeIn(new, shift=UP*.1), run_time=.33)
    else:
        scene.play(FadeIn(new, shift=UP*.1), run_time=.55)
    return new


def food(name, size=1.0, point=ORIGIN):
    art = icon(name, size, aspect=1.35).move_to(point).set_z_index(6)
    art.element = name
    # Solid pigment and restrained strokes give objects their own visual weight.
    for part in art.family_members_with_points():
        if part.get_fill_opacity() > 0: part.set_fill(opacity=1)
        if part.get_stroke_width() > 0: part.set_stroke(width=min(part.get_stroke_width(),2.4))
    return art


def row(names, size=1.0, center=(0,0,0), gap=.65):
    return VGroup(*[food(name,size) for name in names]).arrange(RIGHT,buff=gap).move_to(center)


def tray(width=5.2, height=3.5, color=cfg.CYAN, center=ORIGIN, title=None):
    shadow = RoundedRectangle(width=width,height=height,corner_radius=.25,fill_color='#020F1D',fill_opacity=.65,stroke_width=0).shift(DOWN*.12)
    base = RoundedRectangle(width=width,height=height,corner_radius=.25,fill_color=cfg.PANEL_2,fill_opacity=1,stroke_color=color,stroke_width=3)
    rim = RoundedRectangle(width=width-.18,height=height-.18,corner_radius=.20,fill_opacity=0,stroke_color=color,stroke_width=1,stroke_opacity=.35)
    group = VGroup(shadow,base,rim).move_to(center).set_z_index(0)
    group.base = base
    if title:
        tag=label(title,32,color).next_to(base,UP,buff=.22)
        group.add(tag); group.tag=tag
    return group


def basket(width=4.4,height=2.15,center=ORIGIN):
    # Woven basket with an open upper rim; fruit can land inside its silhouette.
    body=Polygon([-width/2,height/2,0],[width/2,height/2,0],[width*.40,-height/2,0],[-width*.40,-height/2,0],fill_color='#A76E3D',fill_opacity=1,stroke_color=cfg.GOLD,stroke_width=3)
    weave=VGroup(*[Line([-width*.40,y,0],[width*.40,y,0],stroke_color='#DBAA62',stroke_width=3) for y in np.linspace(-height*.35,height*.3,5)])
    rim=RoundedRectangle(width=width+.1,height=.22,corner_radius=.08,fill_color=cfg.GOLD,fill_opacity=1,stroke_width=0).move_to([0,height/2,0])
    handle=Arc(radius=width*.34,start_angle=0,angle=PI,stroke_color='#DBAA62',stroke_width=8).shift(UP*height*.30)
    return VGroup(handle,body,weave,rim).move_to(center).set_z_index(0)


def friend(shirt=cfg.BLUE,center=ORIGIN):
    # Friendly half-body illustration, rather than a name or rule card.
    shoulders=Ellipse(width=1.6,height=1.1,fill_color=shirt,fill_opacity=1,stroke_width=0).shift(DOWN*.5)
    face=Circle(radius=.49,fill_color='#EDBA86',fill_opacity=1,stroke_width=0).shift(UP*.36)
    hair=Arc(radius=.49,start_angle=.12,angle=PI-.24,stroke_color='#473633',stroke_width=13).shift(UP*.43)
    eyes=VGroup(*[Dot([x,.40,0],radius=.038,color=cfg.BG) for x in [-.16,.16]])
    smile=Arc(radius=.19,start_angle=PI+.25,angle=PI-.5,stroke_color='#804A38',stroke_width=3).move_to([0,.16,0])
    return VGroup(shoulders,face,hair,eyes,smile).move_to(center).set_z_index(7)


def speech(words,center,color=cfg.CYAN):
    text=label(words,33,color)
    box=RoundedRectangle(width=max(2.5,text.width+.55),height=.72,corner_radius=.18,fill_color=cfg.PANEL,fill_opacity=1,stroke_color=color,stroke_width=2).move_to(center)
    text.move_to(box)
    return VGroup(box,text).set_z_index(15)


def counter():
    top=RoundedRectangle(width=13.8,height=.3,corner_radius=.08,fill_color='#AE8158',fill_opacity=1,stroke_width=0).move_to([0,-2.85,0])
    front=Rectangle(width=13.4,height=.45,fill_color='#74513B',fill_opacity=1,stroke_width=0).move_to([0,-3.2,0])
    return VGroup(front,top).set_z_index(-1)


def pizza(radius=2.05, center=ORIGIN, toppings=('mushroom','olive','pepper','onion')):
    # Top-down pizza with a golden crust, tomato base, herbs, and real ingredient art.
    shadow=Circle(radius=radius*1.06,fill_color='#020F1D',fill_opacity=.6,stroke_width=0).shift(DOWN*.12)
    plate=Circle(radius=radius*1.08,fill_color=cfg.WHITE,fill_opacity=1,stroke_color=cfg.CYAN,stroke_width=2)
    crust=Circle(radius=radius,fill_color='#DE984A',fill_opacity=1,stroke_color=cfg.GOLD,stroke_width=5)
    sauce=Circle(radius=radius*.86,fill_color='#ED6B4F',fill_opacity=1,stroke_width=0)
    seasoning=VGroup(*[Dot([radius*.65*np.cos(t),radius*.65*np.sin(t),0],radius=.055,color=cfg.GOLD) for t in np.linspace(0,TAU,12,endpoint=False)])
    arts=VGroup()
    for i,name in enumerate(toppings):
        t=TAU*i/max(len(toppings),1)+PI/4
        art=food(name,radius*.48,[radius*.48*np.cos(t),radius*.48*np.sin(t),0]); arts.add(art)
    group=VGroup(shadow,plate,crust,sauce,seasoning,arts).move_to(center)
    group.toppings=arts
    return group


def pizza_3d():
    plate=Cylinder(radius=2.5,height=.09,direction=OUT,resolution=(2,48),fill_color=cfg.WHITE,fill_opacity=1,stroke_width=0).shift(IN*.15)
    crust=Cylinder(radius=2.3,height=.28,direction=OUT,resolution=(2,48),fill_color='#DE984A',fill_opacity=1,stroke_width=0)
    sauce=Circle(radius=2.04,fill_color='#ED6B4F',fill_opacity=1,stroke_width=0).shift(OUT*.15)
    herbs=VGroup(*[Dot([1.55*np.cos(t),1.55*np.sin(t),.17],radius=.065,color=cfg.GOLD) for t in np.linspace(0,TAU,14,endpoint=False)])
    group=VGroup(plate,crust,sauce,herbs)
    # Real depth ordering, not screen overlays, for the 3D object.
    group.set_z_index(0)
    return group


def habitat(width=5,height=3.7,center=ORIGIN,color=cfg.GREEN):
    grass=Ellipse(width=width,height=height,fill_color=color,fill_opacity=.20,stroke_color=color,stroke_width=3).move_to(center)
    fence=VGroup()
    for t in np.linspace(0,TAU,26,endpoint=False):
        pos=np.array(center)+np.array([width*.5*np.cos(t),height*.5*np.sin(t),0])
        fence.add(Line(pos+DOWN*.10,pos+UP*.13,stroke_color=color,stroke_width=3))
    return VGroup(grass,fence).set_z_index(0)


def token(n,color=cfg.CYAN,point=ORIGIN):
    disc=Circle(radius=.46,fill_color=color,fill_opacity=1,stroke_color=cfg.WHITE,stroke_width=1.5)
    number=label(str(n),38,cfg.BG).move_to(disc)
    return VGroup(disc,number).move_to(point).set_z_index(6)


def conveyor():
    belt=RoundedRectangle(width=13.2,height=1.35,corner_radius=.25,fill_color=cfg.PANEL_2,fill_opacity=1,stroke_color=cfg.CYAN,stroke_width=3).move_to([0,-1.65,0])
    rollers=VGroup(*[Circle(radius=.12,fill_color=cfg.GRAY,fill_opacity=1,stroke_width=0).move_to([x,-2.05,0]) for x in np.linspace(-6,6,17)])
    return VGroup(belt,rollers)


def checkmark(point=ORIGIN,color=cfg.GREEN):
    return VMobject().set_points_as_corners([[-.22,0,0],[-.04,-.2,0],[.35,.28,0]]).set_stroke(color,width=7).move_to(point).set_z_index(15)


def venn(a='A',b='B',center=(0,-.2,0),scale=1):
    # Mathematics stage, introduced only after the concrete example.
    from manim_scenes.common import VennStage
    stage=VennStage(a,b,'U',radius=1.65,separation=1.9,center=center,board_width=11.8,board_height=5.35,label_size=36)
    stage.universe.tag.become(label("U",32,cfg.MUTED).move_to(stage.universe.tag))
    stage.scale(scale)
    return stage


def mask(stage,kind,color=cfg.PURPLE):
    return stage.region(kind,color,fill_opacity=.5,glow=False).set_z_index(1)


def countdown(scene,point=(0,-3.6,0)):
    dial=Circle(radius=.25,stroke_color=cfg.GOLD,stroke_width=4).move_to(point)
    scene.play(Create(dial),run_time=3,rate_func=linear)
    scene.play(FadeOut(dial),run_time=.25)


def move_camera(scene, **kwargs):
    # Transform can replace Text glyphs. Register the current family before
    # moving the camera so every letter remains fixed in screen coordinates.
    for mob in scene.mobjects:
        if getattr(mob, '_is_project_hud', False):
            scene.add_fixed_in_frame_mobjects(mob)
    scene.move_camera(**kwargs)


def replace_text(scene, old, new, run_time=.6):
    """Change words without overlapping lines or morphing glyphs."""
    fixed = isinstance(scene, ThreeDScene) and getattr(old, '_is_project_hud', False)
    scene.play(FadeOut(old), run_time=run_time*.45)
    if fixed: scene.remove_fixed_in_frame_mobjects(old)
    old.become(new)
    if fixed:
        scene.add_fixed_in_frame_mobjects(old)
        scene.remove(old)
    scene.play(FadeIn(old), run_time=run_time*.55)
    return old


def math_expression(tex, size=68, color=cfg.WHITE, max_width=13.1):
    """One large typeset statement, sized for a phone screen."""
    result = MathTex(tex, font_size=size, color=color)
    result.set_stroke(cfg.BG, width=3, opacity=.9, background=True)
    if result.width > max_width: result.scale_to_fit_width(max_width)
    result.set_z_index(20)
    return result


def math_beat(scene, head, title, expressions, note, colors=None):
    """Give the rule earned by an example its own uncluttered screen."""
    clear(scene, head)
    replace_text(scene, head, heading(title), run_time=.6)
    separator = Line([-5.3,2.72,0],[5.3,2.72,0],stroke_color=cfg.CYAN,stroke_width=2.5)
    scene.play(Create(separator), run_time=.35)
    positions = {1: (.1,), 2: (1.14,-.86), 3: (1.55,0,-1.55)}[len(expressions)]
    sizes = {1: 74, 2: 68, 3: 60}
    for index,(tex,y) in enumerate(zip(expressions,positions)):
        color = (colors or [cfg.GOLD]*len(expressions))[index]
        mob = math_expression(tex,sizes[len(expressions)],color).move_to([0,y,0])
        if isinstance(scene,ThreeDScene):
            mob._is_project_hud = True
            scene.add_fixed_in_frame_mobjects(mob);scene.remove(mob)
        scene.play(FadeIn(mob,shift=UP*.14),run_time=.7)
    change(scene,None,note,cfg.CYAN)
