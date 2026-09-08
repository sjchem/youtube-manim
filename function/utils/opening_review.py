"""Draw opening cue frames without encoding the intervening video frames."""
from pathlib import Path
import json

from manim import ThreeDCamera, config as manim_config
from utils.timing_audit import TimingRenderer
from manim_scenes.scene_01_everyday_machines import Scene01EverydayMachines


def main():
    manim_config.pixel_width = 854
    manim_config.pixel_height = 480
    manim_config.frame_rate = 15
    manim_config.progress_bar = 'none'
    root = Path('output/review/gateway')
    root.mkdir(parents=True, exist_ok=True)
    scene = Scene01EverydayMachines(renderer=TimingRenderer(camera_class=ThreeDCamera))
    cues = []

    def snapshot(scene, name, seconds):
        scene.camera.reset()
        scene.camera.capture_mobjects(scene.mobjects)
        scene.camera.get_image().save(root / f'{name}.png')
        cues.append({'name':name,'seconds':round(seconds,3)})
        print(f'{seconds:5.2f}s {name}',flush=True)

    scene._opening_review = snapshot
    scene.construct()
    (root / 'cues.json').write_text(json.dumps(cues,indent=2)+'\n')
    cards = ''.join(
        f'<article><img src="{cue["name"]}.png" alt="{cue["name"].split("_", 1)[1]}">'
        f'<p>{cue["seconds"]:.2f}s · {cue["name"].split("_", 1)[1].title()}</p></article>'
        for cue in cues
    )
    (root / 'index.html').write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>The universal translator — opening review</title>'
        '<style>body{margin:32px auto;padding:0 20px;max-width:1200px;background:#020814;'
        'color:#eaf5ff;font:18px/1.5 system-ui}a{color:#57deff}'
        'main{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}'
        'img,video{width:100%}article{border:1px solid #17334d}p{padding:0 14px}</style>'
        '<h1>The universal translator</h1><p>66-second opening · 480p cue frames · '
        '<a href="../../../assets/audio/scripts/scene_01.txt">Continuous narration</a></p>'
        '<video controls preload="none" poster="03_gateway.png" '
        'src="../../../media/videos/scene_01_everyday_machines/480p15/Scene01EverydayMachines.mp4"></video>'
        f'<main>{cards}</main></html>'
    )
    print(f'Finished at {scene.time:.3f}s; {len(scene.mobjects)} foreground objects remain.')


if __name__ == '__main__':
    main()
