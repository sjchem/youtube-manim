"""A pizza for two friends: the question comes before any set notation."""
from manim_scenes.story_world import *

class Scene01Hook(ThreeDScene):
    def construct(self): play_scene(self)

def play_scene(scene):
    t,head=start(scene,'01','Can one pizza make everyone happy?')
    pie=pizza(1.85,toppings=())
    kitchen=counter()
    scene.play(FadeIn(kitchen),GrowFromCenter(pie),run_time=1.6)
    ingredients=row(('mozzarella','sausage','mushroom','olive','onion','pepper'),.72,(0,2.3,0),.35)
    scene.play(LaggedStart(*[FadeIn(m,shift=DOWN*.5) for m in ingredients],lag_ratio=.12),run_time=1.8)
    cue(scene,t,7)
    friends=VGroup(friend(cfg.BLUE,[-5,-.45,0]),friend(cfg.ORANGE,[5,-.45,0]))
    requests=VGroup(speech('No meat',[-5,1.45,0],cfg.BLUE),speech('No dairy',[5,1.45,0],cfg.ORANGE))
    scene.play(FadeIn(friends,shift=UP*.3),FadeIn(requests),run_time=1.2)
    cue(scene,t,17)
    replace_text(scene,head,heading('Which toppings can both friends eat?'),run_time=.6)
    countdown(scene)
    cue(scene,t,22)
    scene.play(ingredients[0].animate.move_to([5,-2,0]).set_opacity(.4),ingredients[1].animate.move_to([-5,-2,0]).set_opacity(.4),run_time=1)
    seats=[[-.7,.65,0],[.7,.65,0],[-.7,-.65,0],[.7,-.65,0]]
    scene.play(LaggedStart(*[m.animate.move_to(p) for m,p in zip(ingredients[2:],seats)],lag_ratio=.2),run_time=2)
    scene.play(FadeIn(checkmark([-5,2.35,0])),FadeIn(checkmark([5,2.35,0])),run_time=.7)
    cue(scene,t,31)
    clear(scene,head)
    replace_text(scene,head,heading('Both friends. One pizza.'),run_time=.5)
    pie3=pizza_3d().shift(DOWN*.25)
    accepted=VGroup(*[food(name,.9,[x,y-.25,.20]).set_z_index(0) for name,(x,y,_) in zip(('mushroom','olive','onion','pepper'),seats)])
    scene.play(FadeIn(pie3,accepted),run_time=1)
    move_camera(scene,phi=52*DEGREES,theta=-78*DEGREES,zoom=.95,run_time=2.3)
    scene.play(Rotate(VGroup(pie3,accepted),angle=20*DEGREES,axis=OUT),run_time=2.8)
    cue(scene,t,42)
    clear(scene,head)
    scene.set_camera_orientation(phi=0,theta=-PI/2,zoom=1)
    # Match the reference title treatment: gold serif, offset shadow,
    # a fine cyan divider, and a white question underneath.
    title=Text('SET THEORY',font='Nimbus Roman',weight=BOLD,
               font_size=70,color=cfg.GOLD).move_to([0,1.05,0]).set_z_index(20)
    shadow=title.copy().set_opacity(.24).shift(RIGHT*.10+DOWN*.08).set_z_index(19)
    shadow._is_decorative=True  # Intentional title shadow, not a second caption.
    divider=Line([-6.2,.33,0],[6.2,.33,0],stroke_color=cfg.CYAN,stroke_width=2.5)
    sub=Text('How do we decide what belongs?',font='Nimbus Roman',weight=BOLD,
             font_size=38,color=cfg.WHITE).move_to([0,-.25,0]).set_z_index(20)
    if sub.width > 13.2: sub.scale_to_fit_width(13.2)
    scene.play(FadeOut(head),FadeIn(shadow,title,divider,sub),run_time=.8)
    cue(scene,t,46.5)
    end_scene(scene,t,cfg.SCENE_DURATIONS['01']); finish(scene)
