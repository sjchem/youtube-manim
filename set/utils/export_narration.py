"""Export one uninterrupted, direction-free ElevenLabs text file per scene."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def main():
    source = (ROOT / 'narration_script.md').read_text()
    sections = re.split(r'^## (\d{2}) · [^\n]+\n', source, flags=re.M)
    destination = ROOT / 'assets/audio/scripts'
    destination.mkdir(parents=True, exist_ok=True)
    if sections[1::2] != [f'{n:02}' for n in range(1, 15)]:
        raise ValueError('Expected exactly 14 ordered narration scenes')
    total = 0
    for key, prose in zip(sections[1::2], sections[2::2]):
        prose = ' '.join(prose.split())
        if any(marker in prose for marker in ('[pause', '**', '##', '> ')):
            raise ValueError(f'Scene {key} contains non-spoken markup')
        (destination / f'scene_{key}.txt').write_text(prose + '\n')
        words = len(prose.split())
        total += words
        print(f'scene_{key}: {words} words')
    print(f'Total: {total} spoken words. Audio alignment still requires generated voice tracks.')

if __name__ == '__main__':
    main()
