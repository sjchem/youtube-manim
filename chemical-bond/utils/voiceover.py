"""Find user-recorded narration clips, validate their length, and attach them to scenes."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess

import config as cfg

AUDIO_FOLDER = cfg.PROJECT_ROOT / 'assets' / 'audio'
EXTENSIONS = ('.wav', '.mp3', '.m4a')


def find_audio(key: str) -> Path | None:
    clips = [AUDIO_FOLDER / f'scene_{key}{ext}' for ext in EXTENSIONS]
    found = [p for p in clips if p.is_file()]
    if len(found) > 1:
        raise ValueError(f'Scene {key}: keep one narration clip; found {", ".join(p.name for p in found)}')
    return found[0] if found else None


def audio_duration(path: Path) -> float:
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                             '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    return float(json.loads(result.stdout)['format']['duration'])


def attach_voiceover(scene, key: str) -> None:
    clip = find_audio(key)
    if clip is None:
        return  # Silent previews remain useful before the user's recording is ready.
    length = audio_duration(clip)
    if length > cfg.SCENE_DURATIONS[key] + 0.05:
        raise ValueError(f'{clip.name}: {length:.2f}s exceeds scene {key} ({cfg.SCENE_DURATIONS[key]:.2f}s). '
                         'Edit the audio or retime the scene before rendering.')
    scene.add_sound(str(clip), time_offset=0)


def main() -> int:
    failed = False
    for key, target in cfg.SCENE_DURATIONS.items():
        try:
            clip = find_audio(key)
            if clip is None:
                print(f'scene_{key}: MISSING — target {target:.1f}s')
                failed = True
                continue
            length = audio_duration(clip)
            status = 'TOO LONG' if length > target + 0.05 else ('SHORT — check pauses' if target - length > 3 else 'FITS')
            print(f'scene_{key}: {length:.2f}s / {target:.1f}s — {status}')
            failed |= length > target + 0.05
        except (ValueError, KeyError, subprocess.CalledProcessError) as error:
            print(f'scene_{key}: {error}')
            failed = True
    print('Length checks do not verify spoken-word alignment; compare against narration_cues.md.')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
