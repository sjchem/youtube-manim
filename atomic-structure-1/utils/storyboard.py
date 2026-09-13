"""Render three representative endpoint frames per scene for visual review."""
from pathlib import Path
import importlib
import gc
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from PIL import Image, ImageDraw
from manim import config, FadeOut
import config as cfg
from main import SCENE_MAP
from utils.timing_audit import TimingRenderer, camera_class_for

class StoryboardRenderer(TimingRenderer):
    def __init__(self, key):
        super().__init__(camera_class=camera_class_for(key))
        self.key = key
        fractions = {'07': (0.2, 0.5, 0.78), '13': (0.2, 0.5, 0.94)}.get(key, (0.2, 0.5, 0.83))
        self.thresholds = [cfg.SCENE_DURATIONS[key]*f for f in fractions]
        self.images = []
    def play(self, scene, *args, **kwargs):
        super().play(scene, *args, **kwargs)
        visible = any(not getattr(m, "_is_project_background", False) for m in scene.mobjects)
        clearing = scene.animations and all(isinstance(a, FadeOut) for a in scene.animations)
        if visible and not clearing and self.thresholds and self.time >= self.thresholds[0]:
            self.update_frame(scene)
            self.images.append((Image.fromarray(self.get_frame()).convert('RGB'), self.time))
            self.thresholds.pop(0)

def main():
    config.pixel_width, config.pixel_height = 640, 360
    config.frame_rate = 15
    config.progress_bar = 'none'
    output = ROOT/'output/storyboard'
    output.mkdir(parents=True, exist_ok=True)
    tiles = []
    for scene_key, (module, cls, title) in SCENE_MAP.items():
        if len(sys.argv)>1 and scene_key[-2:] not in [n.zfill(2) for n in sys.argv[1:]]:
            continue
        key = scene_key[-2:]
        renderer = StoryboardRenderer(key)
        scene = getattr(importlib.import_module(module), cls)(renderer=renderer)
        scene.construct()
        for i,(frame,t) in enumerate(renderer.images):
            frame.save(output/f'scene_{key}_{i+1}.png')
        print(f'{scene_key}: {len(renderer.images)} frames', flush=True)
        del scene, renderer
        gc.collect()
    tiles = []
    for file in sorted(output.glob('scene_??_?.png')):
        frame = Image.open(file).convert('RGB')
        tile = Image.new('RGB',(320,204),'#041A2F')
        tile.paste(frame.resize((320,180)),(0,24))
        ImageDraw.Draw(tile).text((8,6),file.stem.replace('_',' '),fill='white')
        tiles.append(tile)
    for page,start in enumerate(range(0,len(tiles),21),1):
        board = Image.new('RGB',(960,1428),'#041A2F')
        for i,tile in enumerate(tiles[start:start+21]):
            board.paste(tile,((i%3)*320,(i//3)*204))
        board.save(output/f'board_{page}.jpg',quality=95)
    print(output)
if __name__=='__main__':
    main()
