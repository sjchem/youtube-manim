"""Return to the pizza and the friends, with the mathematics now earned."""
from manim_scenes.story_world import *
class Scene13Finale(Scene):
    def construct(self): play_scene(self)

def play_scene(scene):
    t,head=start(scene,'13','One pizza, ready to share')
    pie=pizza(2,[0,-.25,0]); friends=VGroup(friend(cfg.BLUE,[-4.8,-.5,0]),friend(cfg.ORANGE,[4.8,-.5,0]))
    scene.play(FadeIn(counter(),friends),GrowFromCenter(pie),run_time=1.4)
    cap=change(scene,None,'Neither dairy nor meat',cfg.GREEN)
    cue(scene,t,12)
    law=formula('(D ∪ M)ᶜ = Dᶜ ∩ Mᶜ',55,cfg.GOLD).move_to([0,2.6,0])
    scene.play(FadeIn(law),run_time=.8)
    cue(scene,t,25)
    cap=change(scene,cap,'Belongs. Overlaps. Remains.',cfg.GOLD)
    scene.play(FadeIn(checkmark([-4.8,1.3,0])),FadeIn(checkmark([4.8,1.3,0])),run_time=.8)
    cue(scene,t,38.5)
    end_scene(scene,t,cfg.SCENE_DURATIONS['13']); finish(scene)
