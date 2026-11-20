"""Attach a finished chapter recording, or place beat recordings at their cues.

Full chapter: assets/audio/scene_01.wav
Cue-aligned:  assets/audio/scene_01/beat_001.wav, beat_002.wav, ...
Beat recordings keep their original speed; visual breathing room is silence.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess

import config as cfg
from narration import SCRIPT

AUDIO_FOLDER = cfg.PROJECT_ROOT / 'assets' / 'audio'
EXTENSIONS = ('.wav', '.mp3', '.m4a')


def _one_clip(stem: Path) -> Path | None:
    found = [stem.with_suffix(ext) for ext in EXTENSIONS if stem.with_suffix(ext).is_file()]
    if len(found) > 1:
        raise ValueError(f'Keep one recording for {stem.name}; found {", ".join(p.name for p in found)}')
    return found[0] if found else None


def find_audio(key: str) -> Path | None:
    return _one_clip(AUDIO_FOLDER / f'scene_{key}')


def audio_duration(path: Path) -> float:
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                             '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    return float(json.loads(result.stdout)['format']['duration'])


def narration_clips(key: str) -> list[tuple[Path, float, float]]:
    """Return (clip, cue start, available seconds), validating a complete mode.

    Refuse partial beat sets and overlaps instead of silently rendering gaps
    where words are missing. Never stretch the cloned voice to fill a scene.
    """
    full = find_audio(key)
    folder = AUDIO_FOLDER / f'scene_{key}'
    beat_files = [p for p in folder.glob('beat_*') if p.suffix.lower() in EXTENSIONS]
    if full and beat_files:
        raise ValueError(f'Scene {key}: choose a chapter clip or beat recordings, not both.')
    closing = cfg.SCENE_DURATIONS[key] - cfg.TIMING['transition']
    if not beat_files:
        return [(full, 0.0, closing)] if full else []
    expected = {f'beat_{i + 1:03d}' for i in range(len(SCRIPT[key]))}
    unexpected = [p.name for p in beat_files if p.stem not in expected]
    if unexpected:
        raise ValueError(f'Scene {key}: unexpected beat files: {", ".join(unexpected)}')
    clips = []
    missing = []
    for i, (start, _) in enumerate(SCRIPT[key]):
        stem = folder / f'beat_{i + 1:03d}'
        clip = _one_clip(stem)
        if clip is None:
            missing.append(stem.name)
            continue
        end = SCRIPT[key][i + 1][0] if i + 1 < len(SCRIPT[key]) else closing
        clips.append((clip, start, end - start))
    if missing:
        raise ValueError(f'Scene {key}: incomplete beat audio; missing {", ".join(missing)}')
    return clips


def checked_clips(key: str) -> list[tuple[Path, float, float, float]]:
    checked = []
    for clip, start, available in narration_clips(key):
        length = audio_duration(clip)
        if length > available + 0.02:
            raise ValueError(f'{clip}: {length:.2f}s exceeds its {available:.2f}s voice window '
                             f'at {start:.2f}s. Edit the recording or retime the cue.')
        checked.append((clip, start, available, length))
    return checked


def attach_voiceover(scene, key: str) -> None:
    # Validate the entire set before adding any sound.
    for clip, start, _, _ in checked_clips(key):
        scene.add_sound(str(clip), time_offset=start)


def main() -> int:
    failed = False
    for key, target in cfg.SCENE_DURATIONS.items():
        try:
            clips = checked_clips(key)
            if not clips:
                print(f'scene_{key}: MISSING — target {target:.1f}s')
                failed = True
                continue
            if len(clips) > 1 or clips[0][0].parent.name == f'scene_{key}':
                print(f'scene_{key}: {len(clips)} beat recording(s), cue-aligned; '
                      f'{sum(c[3] for c in clips):.2f}s spoken')
            else:
                length = clips[0][3]
                status = 'SHORT — check internal cue alignment' if target - length > 3 else 'FITS'
                print(f'scene_{key}: {length:.2f}s / {target:.1f}s — {status}')
        except (ValueError, KeyError, subprocess.CalledProcessError) as error:
            print(f'scene_{key}: {error}')
            failed = True
    print('Chapter recordings need an internal cue check; beat recordings are placed at cue starts.')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
