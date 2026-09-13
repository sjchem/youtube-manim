"""Export spoken narration, without Markdown or production directions, for TTS."""
from __future__ import annotations
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADING = re.compile(r'^## Scene (?P<scene>\d{2}) — (?P<title>.*?) — (?P<sm>\d+):(?P<ss>\d{2})–(?P<em>\d+):(?P<es>\d{2})$', re.M)
WORD = re.compile(r"\b[\w']+\b")

def read_sections():
    text = (ROOT/'narration_script.md').read_text(encoding='utf-8')
    matches = list(HEADING.finditer(text))
    sections = []
    for i, match in enumerate(matches):
        body = text[match.end():matches[i+1].start() if i+1<len(matches) else len(text)].strip()
        sections.append(dict(key=match['scene'], title=match['title'], text=body,
            start=60*int(match['sm'])+int(match['ss']), end=60*int(match['em'])+int(match['es'])))
    return sections

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if committed exports differ from the script')
    args = parser.parse_args()
    sections = read_sections()
    if len(sections) != 15 or [s['key'] for s in sections] != [f'{i:02d}' for i in range(1,16)]:
        raise ValueError('Expected fifteen ordered narration sections')
    folder = ROOT/'assets/narration'
    expected = {f"scene_{s['key']}.txt": s['text']+'\n' for s in sections}
    expected['full_narration.txt'] = '\n\n'.join(s['text'] for s in sections)+'\n'
    if not args.check:
        folder.mkdir(parents=True, exist_ok=True)
        for name, content in expected.items():
            (folder/name).write_text(content, encoding='utf-8')
    stale = [name for name, content in expected.items() if not (folder/name).exists() or (folder/name).read_text(encoding='utf-8') != content]
    print('Narration exports: '+(', '.join(stale)+' need updating' if stale else '15 scene files and full script match'))
    return bool(stale)

if __name__ == '__main__':
    raise SystemExit(main())
