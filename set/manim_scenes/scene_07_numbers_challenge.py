"""A handful of colourful number counters becomes a sorting puzzle."""
from manim_scenes.story_world import *
from utils import set_models as sets
class Scene07NumbersChallenge(Scene):
    def construct(self): play_scene(self)

def play_scene(scene):
    t,head=start(scene,'07','Ten counters. Two rules.')
    counters={n:token(n,cfg.CYAN,[-4.4+(n-1)%5*2.2,1.2-(n-1)//5*1.8,0]) for n in range(1,11)}
    scene.play(LaggedStart(*[GrowFromCenter(m) for m in counters.values()],lag_ratio=.1),run_time=1.5)
    cap=change(scene,None,'U = {1, 2, …, 10}')
    cue(scene,t,13)
    left=Circle(radius=2.25,stroke_color=cfg.BLUE,stroke_width=4,fill_color=cfg.BLUE,fill_opacity=.1).move_to([-1.45,0,0])
    right=Circle(radius=2.25,stroke_color=cfg.ORANGE,stroke_width=4,fill_color=cfg.ORANGE,fill_opacity=.1).move_to([1.45,0,0])
    tags=VGroup(label('Prime',36,cfg.BLUE).move_to([-2,2.6,0]),label('Even',36,cfg.ORANGE).move_to([2,2.6,0]))
    seats={3:[-2.6,.85,0],5:[-2.6,-.85,0],7:[-1.55,1.35,0],4:[1.95,.8,0],6:[3.02,.8,0],8:[1.95,-.8,0],10:[3.02,-.8,0],1:[-5.4,0,0],9:[5.4,0,0],2:[0,-2.85,0]}
    # Reveal the sorted positions without number labels crossing in transit.
    scene.play(FadeOut(*counters.values()),FadeIn(left,right,tags),run_time=.6)
    for n,m in counters.items(): m.move_to(seats[n])
    scene.play(LaggedStart(*[FadeIn(m) for m in counters.values()],lag_ratio=.08),run_time=1)
    cap=change(scene,cap,'Prime AND even?',cfg.GOLD)
    cue(scene,t,33)
    replace_text(scene,head,heading('Where does the number 2 belong?'),run_time=.5)
    scene.play(FadeOut(cap),run_time=.4); countdown(scene)
    cue(scene,t,44)
    lens=Intersection(left,right,fill_color=cfg.GOLD,fill_opacity=.55,stroke_width=0).set_z_index(1)
    scene.play(counters[2].animate.move_to([0,0,0]),FadeIn(lens),*[m.animate.set_opacity(.27) for n,m in counters.items() if n!=2],run_time=1.4)
    cap=change(scene,None,'2 is the only even prime',cfg.GOLD)
    cue(scene,t,58)
    replace_text(scene,head,heading('One shared member'),run_time=.6)
    cap=change(scene,cap,'P ∩ E = {2}     |P ∩ E| = 1',cfg.GOLD)
    cue(scene,t,70)
    union=Union(left,right,fill_color=cfg.GREEN,fill_opacity=.3,stroke_width=0).set_z_index(1)
    scene.play(FadeOut(cap),run_time=.2)
    scene.play(FadeOut(lens),FadeIn(union),*[m.animate.set_opacity(1) for n,m in counters.items() if str(n) in sets.union(sets.PRIMES,sets.EVENS)],run_time=.8)
    cap=change(scene,None,'P ∪ E has 8 distinct members',cfg.GREEN)
    cue(scene,t,83.5)
    math_beat(scene,head,'Read the two results',['P\\cap E=\\{2\\}', '|P\\cup E|=8'],'One shared number; eight in either group')
    cue(scene,t,99.5)
    end_scene(scene,t,cfg.SCENE_DURATIONS['07']); finish(scene)
