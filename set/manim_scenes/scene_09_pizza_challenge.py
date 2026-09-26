"""Return to the two friends and build their pizza from an eight-topping menu."""
from manim_scenes.story_world import *
from utils import set_models as sets
class Scene09PizzaChallenge(Scene):
    def construct(self): play_scene(self)

def play_scene(scene):
    t,head=start(scene,'09','Back to our two friends')
    pie=pizza(1.8,[0,-.3,0],())
    friends=VGroup(friend(cfg.BLUE,[-5.4,-.6,0]),friend(cfg.ORANGE,[5.4,-.6,0]))
    rules=VGroup(speech('No meat',[-5.4,1.1,0],cfg.BLUE),speech('No dairy',[5.4,1.1,0],cfg.ORANGE))
    scene.play(FadeIn(counter(),pie,friends,rules),run_time=1.2)
    cue(scene,t,10)
    clear(scene,head)
    menu=tray(12.6,4.7,cfg.CYAN,[0,-.1,0])
    foods={}
    for i,name in enumerate(sets.TOPPINGS):
        x=-4.7+(i%4)*3.15; y=1.1-(i//4)*2.2
        item=food(name,1.0,[x,y,0]); tag=label(name,31,cfg.WHITE).move_to([x,y-.78,0])
        foods[name]=VGroup(item,tag)
    scene.play(FadeIn(menu),LaggedStart(*[FadeIn(m) for m in foods.values()],lag_ratio=.07),run_time=1.5)
    cap=change(scene,None,'Which toppings are neither dairy nor meat?',cfg.GOLD)
    cue(scene,t,28)
    scene.play(FadeOut(cap),run_time=.4); countdown(scene)
    cue(scene,t,35)
    banned=sets.union(sets.DAIRY,sets.MEAT)
    marks=VGroup(*[label('×',42,cfg.RED).move_to(foods[n][0]) for n in sorted(banned)])
    scene.play(FadeIn(marks),*[foods[n].animate.set_opacity(.35) for n in banned],run_time=1)
    cap=change(scene,None,'First exclude D ∪ M',cfg.RED)
    cue(scene,t,48)
    scene.play(FadeOut(marks),*[FadeOut(foods[n]) for n in banned],run_time=.8)
    cap=change(scene,cap,'Keep (D ∪ M)ᶜ',cfg.GREEN)
    cue(scene,t,59)
    clear(scene,head)
    pie=pizza(2.25,[0,-.2,0],('mushroom','olive','onion','pepper'))
    scene.play(FadeIn(pie,scale=.85),run_time=1)
    cap=change(scene,None,'Mushroom · olive · onion · pepper',cfg.GREEN)
    cue(scene,t,71)
    scene.play(pie.animate.scale(.8).move_to([-3,-.2,0]),run_time=1)
    checks=VGroup(label('Not dairy',30,cfg.BLUE),label('AND',32,cfg.WHITE),label('Not meat',30,cfg.ORANGE)).arrange(DOWN,buff=.35).move_to([3,.1,0])
    scene.play(FadeIn(checks),run_time=.8)
    cue(scene,t,88.5)
    math_beat(scene,head,'One answer, two descriptions',['S=U\\setminus(D\\cup M)', 'S=D^{c}\\cap M^{c}'],'S is the set of toppings both friends can eat')
    cue(scene,t,106.5)
    end_scene(scene,t,cfg.SCENE_DURATIONS['09']); finish(scene)
