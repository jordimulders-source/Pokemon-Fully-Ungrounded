#!/usr/bin/env python3
"""Zet dialogen uit de Dialoogstudio terug in de scripts.

Invoer: een JSON-bestand {label: tekst} met platte tekst zoals in de editor:
een lege regel = nieuw tekstvak (\\p), een enkele Enter = geforceerde nieuwe regel,
verder breekt de tekst automatisch af op de breedte van het tekstvak.

Gebruik: python3 tools/dialogen/import.py <edits.json>
"""
import glob, json, re, sys

LIMIT = 208          # pixels per regel in het tekstvak (zelfde als de editor)
PLACEHOLDER_W = 42   # {PLAYER}/{RIVAL}/{STR_VAR_n}: ruimte voor 7 tekens


def load_widths():
    src = open('src/fonts.c').read()
    m = re.search(r'gFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};', src, re.S)
    widths = [int(x) for x in re.findall(r'\d+', re.sub(r'//.*', '', m.group(1)))]
    cm = {}
    for line in open('charmap.txt'):
        mm = re.match(r"^'(.+?)'\s*=\s*([0-9A-Fa-f]{2})\s*$", line)
        if mm:
            ch = mm.group(1).replace("\\'", "'")
            code = int(mm.group(2), 16)
            if len(ch) == 1 and code < len(widths):
                cm.setdefault(ch, widths[code])
    return cm


W = load_widths()


def text_width(s):
    w = 0
    for part in re.split(r'(\{[^}]*\})', s):
        if not part:
            continue
        if part.startswith('{'):
            w += PLACEHOLDER_W if re.fullmatch(r'\{(PLAYER|RIVAL|STR_VAR_\d)\}', part) else 0
        else:
            w += sum(W.get(ch, 6) for ch in part)
    return w


def wrap_line(line):
    out, cur = [], ''
    for word in [x for x in line.split(' ') if x]:
        attempt = f'{cur} {word}' if cur else word
        if text_width(attempt) <= LIMIT or not cur:
            cur = attempt
        else:
            out.append(cur)
            cur = word
    out.append(cur)
    return out


def layout(text):
    boxes = [p.strip() for p in re.split(r'\n\s*\n', text.replace('\r', '')) if p.strip()]
    result = []
    for p in boxes:
        lines = []
        for forced in p.split('\n'):
            lines += wrap_line(forced.strip())
        result.append(lines)
    return result


def curly_quotes(text):
    """Het lettertype van de game kent geen rechte " — zet ze om naar “ en ”."""
    parts = text.split('"')
    return ''.join(p + ('“' if i % 2 == 0 else '”') for i, p in enumerate(parts[:-1])) + parts[-1]


def to_strings(text):
    """Platte tekst -> lijst van .string-regels (zonder aanhalingstekens)."""
    text = curly_quotes(text)
    out = []
    boxes = layout(text)
    for b, lines in enumerate(boxes):
        for i, line in enumerate(lines):
            last_line = i == len(lines) - 1
            if last_line:
                end = '$' if b == len(boxes) - 1 else '\\p'
            else:
                end = '\\n' if i == 0 else '\\l'
            out.append(line.replace('"', '\\"') + end)
    return out


LABEL_RE = r'(?m)^({label}::?\n)((?:[ \t]*\.string[ \t]+".*"[ \t]*\n?)+)'


def apply(edits):
    files = sorted(glob.glob('data/maps/*/scripts.inc')) + ['data/text/trainers.inc']
    contents = {f: open(f).read() for f in files}
    done, missing, too_wide = [], [], []
    for label, text in edits.items():
        pattern = re.compile(LABEL_RE.format(label=re.escape(label)))
        for f, t in contents.items():
            m = pattern.search(t)
            if not m:
                continue
            strings = to_strings(text)
            for s in strings:
                if text_width(s.rstrip('$').replace('\\n', '').replace('\\l', '').replace('\\p', '')) > LIMIT:
                    too_wide.append(label)
            block = ''.join(f'\t.string "{s}"\n' for s in strings)
            contents[f] = t[:m.start(2)] + block + t[m.end(2):]
            done.append(label)
            break
        else:
            missing.append(label)
    for f, t in contents.items():
        if t != open(f).read():
            open(f, 'w').write(t)
    return done, missing, sorted(set(too_wide))


if __name__ == '__main__':
    edits = json.load(open(sys.argv[1]))
    done, missing, too_wide = apply(edits)
    print(f'{len(done)} dialogen verwerkt')
    if missing:
        print('Niet gevonden:', ', '.join(missing))
    if too_wide:
        print('Te lange woorden (passen niet op één regel):', ', '.join(too_wide))
