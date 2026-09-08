"""Export clean per-scene narration and report pacing or local audio duration."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess

import config as cfg


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check existing exports without rewriting')
    args = parser.parse_args()
    root = cfg.PROJECT_ROOT
    source = (root / 'narration_script.md').read_text()
    sections = re.findall(r'^## Scene (\d{2})[^\n]*\n(.*?)(?=^## Scene |\Z)', source, re.M | re.S)
    if [key for key, _ in sections] != list(cfg.SCENE_DURATIONS):
        raise ValueError('Narration chapters must match SCENE_DURATIONS in order')
    directory = root / 'assets/audio/scripts'
    directory.mkdir(parents=True, exist_ok=True)
    failed = False
    elapsed = 0
    print('Scene      Start  Target  Words  Words/min  Local audio')
    for key, body in sections:
        body = body.strip() + '\n'
        path = directory / f'scene_{key}.txt'
        if args.check:
            if not path.exists() or path.read_text() != body:
                print(f'STALE: {path}')
                failed = True
        else:
            path.write_text(body)
        words = len(body.split())
        duration = cfg.SCENE_DURATIONS[key]
        audio = next((root / 'assets/audio' / f'scene_{key}{suffix}' for suffix in ('.wav', '.mp3', '.m4a')
                      if (root / 'assets/audio' / f'scene_{key}{suffix}').exists()), None)
        audio_note = 'not supplied'
        if audio:
            result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                     '-of', 'default=noprint_wrappers=1:nokey=1', str(audio)],
                                    capture_output=True, text=True, check=True)
            actual = float(result.stdout)
            audio_note = f'{actual:.1f}s ({duration - actual:+.1f}s room)'
            if actual > duration:
                failed = True
                audio_note += ' TOO LONG'
        print(f'scene_{key}  {elapsed // 60:02d}:{elapsed % 60:02d}  {duration:5.0f}s  {words:5d}  {words * 60 / duration:9.0f}  {audio_note}')
        elapsed += int(duration)
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
