"""A spacious mathematical synthesis: each operation is one membership test."""
from manim_scenes.story_world import *

class Scene12WhyItMatters(Scene):
    def construct(self): play_scene(self)


def play_scene(scene):
    t,head=start(scene,'12','One test connects every rule')
    accent=Line([-5.3,2.72,0],[5.3,2.72,0],stroke_color=cfg.CYAN,stroke_width=2.5)
    scene.play(Create(accent),run_time=.5)
    current=math_expression(r'x\in U',88,cfg.GOLD).move_to([0,.25,0])
    scene.play(FadeIn(current,shift=UP*.15),run_time=.8)
    cap=change(scene,None,'First, choose the universe U')
    cue(scene,t,12)

    def next_rule(title, tex, note, color, mark):
        nonlocal current,cap
        scene.play(FadeOut(current,cap),run_time=.35)
        replace_text(scene,head,heading(title),run_time=.6)
        current=math_expression(tex,68,color).move_to([0,.25,0])
        scene.play(FadeIn(current,shift=UP*.15),run_time=.7)
        cap=change(scene,None,note,color)
        cue(scene,t,mark)

    next_rule('Subset: every member passes',
              r'A\subseteq B\;\Longleftrightarrow\;\forall x\,(x\in A\Rightarrow x\in B)',
              'A whole set fits when every member fits',cfg.BLUE,25)
    next_rule('Union: either rule',
              r'x\in A\cup B\;\Longleftrightarrow\;(x\in A)\lor(x\in B)',
              'OR includes an element in both sets',cfg.GREEN,38)
    next_rule('Intersection: both rules',
              r'x\in A\cap B\;\Longleftrightarrow\;(x\in A)\land(x\in B)',
              'AND keeps the shared members',cfg.GOLD,51)
    next_rule('Complement: inside U, outside A',
              r'x\in A^{c}\;\Longleftrightarrow\;(x\in U)\land(x\notin A)',
              'NOT is always measured inside U',cfg.PURPLE,64)

    scene.play(FadeOut(current,cap),run_time=.35)
    replace_text(scene,head,heading('The two laws for NOT'),run_time=.6)
    first=math_expression(r'(A\cup B)^{c}=A^{c}\cap B^{c}',66,cfg.GREEN).move_to([0,1.1,0])
    second=math_expression(r'(A\cap B)^{c}=A^{c}\cup B^{c}',66,cfg.GOLD).move_to([0,-.85,0])
    scene.play(FadeIn(first,shift=UP*.15),run_time=.6)
    scene.play(FadeIn(second,shift=UP*.15),run_time=.6)
    cap=change(scene,None,'Negating the whole rule swaps OR and AND',cfg.CYAN)
    cue(scene,t,82.5)
    end_scene(scene,t,cfg.SCENE_DURATIONS['12']); finish(scene)
