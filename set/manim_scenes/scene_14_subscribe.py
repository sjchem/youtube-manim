"""A small, friendly closing card in the user's Oceanic theme."""
from manim_scenes.story_world import *
class Scene14Subscribe(Scene):
    def construct(self): play_scene(self)

def play_scene(scene):
    t,head=start(scene,'14')
    thanks=label('Thanks for watching',44,cfg.WHITE).move_to([0,1.8,0])
    pie=pizza(.9,[0,-.1,0]); subscribe=label('More visual mathematics',34,cfg.GOLD).move_to([0,-2,0])
    scene.play(FadeIn(thanks),GrowFromCenter(pie),run_time=1)
    scene.play(FadeIn(subscribe),run_time=.7)
    cue(scene,t,7.5)
    end_scene(scene,t,cfg.SCENE_DURATIONS['14']); finish(scene)
