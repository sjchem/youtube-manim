"""Join already rendered 480p chapters after checking size, rate and duration."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile

import config as cfg
from main import SCENE_MAP


def main() -> int:
    files = []
    for key, (module, name, _) in SCENE_MAP.items():
        path = cfg.PROJECT_ROOT / 'media/videos' / module.rsplit('.', 1)[-1] / '480p15' / f'{name}.mp4'
        if not path.is_file():
            raise FileNotFoundError(f'Missing {path}; run python main.py preview all first')
        result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                                 '-show_entries', 'stream=width,height,r_frame_rate,nb_frames:format=duration',
                                 '-of', 'json', str(path)], capture_output=True, text=True, check=True)
        metadata = json.loads(result.stdout)
        stream = metadata['streams'][0]
        if (stream['width'], stream['height'], stream['r_frame_rate']) != (854, 480, '15/1'):
            raise ValueError(f'Unexpected preview format: {path}')
        actual = float(metadata['format']['duration'])
        expected = cfg.SCENE_DURATIONS[key[-2:]]
        # Manim/encoder rounding can add a few frames even when the scene
        # clock is exact. Reject larger discrepancies; normalize small ones.
        target_frames = round(expected * 15)
        if abs(int(stream['nb_frames']) - target_frames) > 3 or abs(actual - expected) > 0.21:
            raise ValueError(f'{key}: {actual:.3f}s rendered, expected {expected:.3f}s')
        print(f'{key}: {actual:.3f}s source; normalize to {expected:.3f}s', flush=True)
        files.append((path, target_frames))
    destination = cfg.PROJECT_ROOT / 'output/function_480p_review.mp4'
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='function-concat-') as temporary:
        normalized = []
        for index, (path, frames) in enumerate(files):
            clip = Path(temporary) / f'{index:02d}.mp4'
            # Re-encode the existing picture, not the Manim animations. Make
            # every chapter's timestamps and codec parameters identical.
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-threads', '2', '-i', str(path),
                            '-an', '-vf', f'fps=15,tpad=stop_mode=clone:stop_duration=0.2,trim=end_frame={frames},setpts=N/(15*TB)',
                            '-c:v', 'libx264', '-threads', '2', '-preset', 'veryfast', '-crf', '18',
                            '-pix_fmt', 'yuv420p', str(clip)], check=True)
            normalized.append(clip)
        manifest = Path(temporary) / 'chapters.txt'
        manifest.write_text(''.join("file '" + str(p).replace("'", "'\\''") + "'\n" for p in normalized))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0',
                        '-i', str(manifest), '-c', 'copy', '-movflags', '+faststart', str(destination)], check=True)
    result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                             '-show_entries', 'stream=nb_frames:format=duration', '-of', 'json',
                             str(destination)], capture_output=True, text=True, check=True)
    metadata = json.loads(result.stdout)
    expected_total = sum(cfg.SCENE_DURATIONS.values())
    if (int(metadata['streams'][0]['nb_frames']) != round(expected_total * 15)
            or abs(float(metadata['format']['duration']) - expected_total) > 1 / 15):
        raise ValueError('Assembled preview does not match the chapter map')
    print(f'Complete preview: {expected_total:.3f}s, {round(expected_total * 15)} frames verified')
    print(destination)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
