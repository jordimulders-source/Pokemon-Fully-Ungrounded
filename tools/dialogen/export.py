#!/usr/bin/env python3
"""Exporteert alle dialogen uit de scripts naar JSON voor de dialoog-editor.

Gebruik: python3 tools/dialogen/export.py <uitvoer.json>
"""
import glob, json, os, re, subprocess, sys

BASE = '1cbbb304'  # vanilla pokeemerald-expansion
LABEL_RE = re.compile(r'(?m)^(\w+)::?\n((?:[ \t]*\.string[ \t]+".*"[ \t]*\n?)+)')


def strings(body):
    return ''.join(re.findall(r'\.string\s+"(.*)"', body))


def to_plain(s):
    s = s.rstrip('$')
    s = s.replace('\\p', '\n\n')
    s = re.sub(r'\\[nl]', ' ', s)
    s = re.sub(r' +', ' ', s)
    return '\n\n'.join(p.strip() for p in s.split('\n\n'))


def nice(name):
    name = re.sub(r'(?<=[a-z])(?=[A-Z0-9])|(?<=[0-9])(?=[A-Z])', ' ', name)
    return name.replace('_', ' · ')


def gfx_name(g):
    return g.replace('OBJ_EVENT_GFX_', '').replace('_', ' ').title()


def main(out):
    base_text = {}
    files = sorted(glob.glob('data/maps/*/scripts.inc')) + ['data/text/trainers.inc']
    for f in files:
        try:
            old = subprocess.run(['git', 'show', f'{BASE}:{f}'], capture_output=True, text=True).stdout
        except Exception:
            old = ''
        for lab, body in LABEL_RE.findall(old):
            base_text[lab] = strings(body)

    # welke scriptlabels gebruiken een tekst, en welke NPC hoort erbij
    npc_by_script = {}
    for mj in glob.glob('data/maps/*/map.json'):
        d = json.load(open(mj))
        for o in d.get('object_events', []):
            if o.get('script'):
                npc_by_script.setdefault(o['script'], gfx_name(o.get('graphics_id', '')))
        for b in d.get('bg_events', []):
            if b.get('script'):
                npc_by_script.setdefault(b['script'], {'sign': 'Bord', 'hidden_item': 'Item'}.get(b.get('type'), 'Object'))
    users = {}
    trainer_of = {}
    all_scripts = sorted(glob.glob('data/maps/*/scripts.inc')) + sorted(glob.glob('data/scripts/*.inc'))
    for f in all_scripts:
        t = open(f).read()
        labels = [(m.start(), m.group(1)) for m in re.finditer(r'(?m)^(\w+)::?\s*$', t) if '_Text_' not in m.group(1)]
        for m in re.finditer(r'\b(\w*_Text_\w+)\b', t):
            pos = m.start()
            if t[m.end():m.end() + 1] == ':':
                continue  # dit is de definitie zelf, geen gebruik
            owner = None
            for p, l in labels:
                if p > pos:
                    break
                owner = l
            if owner and not owner.endswith(m.group(1)):
                users.setdefault(m.group(1), set()).add(owner)
        for m in re.finditer(r'trainerbattle\w*\s+(TRAINER_\w+)\s*,\s*([^\n]*)', t):
            for lab in re.findall(r'\w+_Text_\w+', m.group(2)):
                trainer_of[lab] = m.group(1)

    lines = []
    maps = {}
    for f in files:
        t = open(f).read()
        is_trainers = f.endswith('trainers.inc')
        for lab, body in LABEL_RE.findall(t):
            raw = strings(body)
            if is_trainers:
                mp = lab.split('_Text_')[0] if '_Text_' in lab else 'Trainers'
            else:
                mp = f.split('/')[2]
            kind = 'Dialoog'
            low = lab.lower()
            for k, v in [('intro', 'Intro'), ('defeat', 'Verslagen'), ('postbattle', 'Na gevecht'),
                         ('rematch', 'Rematch'), ('register', 'Match Call'), ('needtwomons', 'Te weinig Pokémon'),
                         ('sign', 'Bord')]:
                if k in low:
                    kind = v
                    break
            who = []
            for s in sorted(users.get(lab, [])):
                n = npc_by_script.get(s)
                if n and n not in who:
                    who.append(n)
            tr = trainer_of.get(lab)
            scripts = []
            for s in sorted(users.get(lab, [])):
                short = re.sub(r'^\w*?_EventScript_', '', s)
                short = nice(short).replace(' · ', ' ')
                if short not in scripts:
                    scripts.append(short)
            lines.append({
                'id': lab,
                'map': mp,
                'kind': kind,
                'npc': ', '.join(who[:2]),
                'script': ', '.join(scripts[:3]),
                'trainer': tr[8:].replace('_', ' ').title() if tr else '',
                'text': to_plain(raw),
                'changed': base_text.get(lab) is not None and base_text.get(lab) != raw,
                'new': lab not in base_text,
            })
            maps.setdefault(mp, 0)
            maps[mp] += 1
    json.dump({'maps': [{'id': k, 'name': nice(k), 'count': v} for k, v in sorted(maps.items())],
               'lines': lines}, open(out, 'w'), ensure_ascii=False, separators=(',', ':'))
    print(len(lines), 'dialogen,', len(maps), 'kaarten')


if __name__ == '__main__':
    main(sys.argv[1])
