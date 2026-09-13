"""Check every narration window, sequence, and approximate delivery rate."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config as cfg
from utils.narration_export import read_sections, WORD

def main():
    sections = read_sections()
    failed = [s['key'] for s in sections] != list(cfg.SCENE_DURATIONS)
    elapsed = 0
    total_words = 0
    print('scene  words  seconds  words/minute  status')
    for s in sections:
        duration = s['end']-s['start']
        words = len(WORD.findall(s['text']))
        rate = words*60/duration if duration>0 else 0
        ok = (s['start']==elapsed and duration==cfg.SCENE_DURATIONS.get(s['key']) and 98<=rate<=135)
        failed |= not ok
        total_words += words
        elapsed = s['end']
        print(f"{s['key']:>5} {words:6} {duration:8} {rate:13.1f}  {'OK' if ok else 'CHECK'}")
    print(f'{total_words} spoken words; {elapsed//60}:{elapsed%60:02d} planned runtime. Measure generated audio before final sync.')
    return int(failed)
if __name__ == '__main__':
    raise SystemExit(main())
