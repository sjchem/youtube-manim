"""Check that every narration beat can be spoken comfortably inside its window.

A beat's window runs from its start to the next beat (or, for the last beat,
to the start of the chapter's closing fade). A relaxed documentary read is
about 2.3 words per second; anything above ``MAX_RATE`` is refused, because a
voice actor would have to rush and the picture would drift ahead of the words.

    python -m utils.narration_audit
"""

from __future__ import annotations

import re

import config as cfg
from narration import SCRIPT

MAX_RATE = 2.75  # words per second, ceiling for any single beat
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
        print(f"scene_{key}: {len(SCRIPT[key]):2d} beats, fastest {worst:.2f} w/s")
    seconds = sum(cfg.SCENE_DURATIONS.values())
    print(f"\n{total_words} words over {seconds:.0f}s — average {total_words / seconds:.2f} w/s")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
