"""Check that every narration beat can be spoken comfortably inside its window.

A beat's window runs from its start to the next beat (or, for the last beat,
to the start of the chapter's closing fade). The narrator's cloned
ElevenLabs voice reads about 100 words in 35 seconds (2.86 words per second),
so any beat above ``MAX_RATE`` would make the voice run past its picture.
This film carries about 4,300 words across 38 minutes, leaving separate
holds for 3D flights, derivations and viewer predictions. VOICE_RATE
estimates the generated speech, not the finished-video rate: the rest of
each cue is an editorial visual hold.

    python -m utils.narration_audit
"""

from __future__ import annotations

import re

import config as cfg
from narration import SCRIPT

VOICE_RATE = 100 / 35
MAX_RATE = 2.85  # words per second, ceiling for any single beat (the narrator's natural pace)
SPOKEN_NUMBER = re.compile(r"[A-Za-z0-9']+")


def words(line: str) -> int:
    return len(SPOKEN_NUMBER.findall(line))


def windows(key: str) -> list[tuple[float, float, str]]:
    beats = SCRIPT[key]
    end = cfg.SCENE_DURATIONS[key] - cfg.TIMING["transition"]
    result = []
    for index, (start, line) in enumerate(beats):
        stop = beats[index + 1][0] if index + 1 < len(beats) else end
        result.append((start, stop, line))
    return result


def main() -> int:
    failed = False
    total_words = 0
    for key in cfg.SCENE_DURATIONS:
        if key not in SCRIPT:
            print(f"scene_{key}: no narration")
            failed = True
            continue
        worst = 0.0
        for start, stop, line in windows(key):
            span = stop - start
            count = words(line)
            total_words += count
            if span <= 0:
                print(f"scene_{key} @ {start:5.1f}s: beat out of order or past the closing fade")
                failed = True
                continue
            rate = count / span
            worst = max(worst, rate)
            if rate > MAX_RATE:
                print(f"scene_{key} @ {start:5.1f}s: {count} words in {span:.1f}s = {rate:.2f} w/s  «{line[:60]}»")
                failed = True
        count = sum(words(line) for _, line in SCRIPT[key])
        print(f"scene_{key}: {len(SCRIPT[key]):2d} beats, {count:3d} words, "
              f"{60 * count / cfg.SCENE_DURATIONS[key]:.0f} words per finished minute; "
              f"fastest beat {worst:.2f} w/s")
    seconds = sum(cfg.SCENE_DURATIONS.values())
    print(f"\nEstimated speech at your voice pace: {total_words / VOICE_RATE:.1f}s; "
          f"visual pauses / closing card: {seconds - total_words / VOICE_RATE:.1f}s")
    print(f"\n{total_words} words over {seconds:.0f}s — average {total_words / seconds:.2f} w/s")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
