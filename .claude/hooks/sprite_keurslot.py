#!/usr/bin/env python3
"""Keurslot (Jordi 3 nov: "het is elke keer opnieuw dat we instructies vastleggen die je elke keer opnieuw weer
overslaat"). PreToolUse-hook op SendUserFile: een afbeelding uit docs/concept/sprites/ gaat pas naar Jordi als er
naast staat: <bestand>.keuring.md, nieuwer dan de afbeelding, met
  Bron: <welke echte sprites/foto's/krabbels>        (referentie per onderdeel)
  8×: ... / 1×: ...                                   (bekeken op 8× en 1×, keurvel: tools/grounded/keurvel.py)
  per onderdeel één regel 'lijkt op ... / wijkt af in ...'
  Oordeel: PASS                                       (één afwijking of twijfel = niet sturen)
Zie docs/lessen/SPRITE_WERKWIJZE.md, "Checklist". Exit 2 blokkeert de tool en toont de melding aan Claude."""
import json, os, re, sys

data = json.load(sys.stdin)
files = (data.get('tool_input') or {}).get('files') or []
root = os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd()
fout = []
for f in files:
    p = f if os.path.isabs(f) else os.path.join(root, f)
    p = os.path.normpath(p)
    rel = os.path.relpath(p, root)
    if not rel.startswith('docs/concept/sprites/') or not re.search(r'\.(png|jpe?g|gif|webp)$', rel, re.I):
        continue
    k = p + '.keuring.md'
    if not os.path.exists(k):
        fout.append(f'{rel}: geen {os.path.basename(k)}')
        continue
    if os.path.exists(p) and os.path.getmtime(k) < os.path.getmtime(p):
        fout.append(f'{rel}: keuring is ouder dan de afbeelding (opnieuw keuren)')
        continue
    t = open(k, encoding='utf-8').read()
    mist = [n for n, pat in (('Bron:', r'(?im)^\s*[-*]?\s*Bron:'), ('8×', r'8\s*[×x]'), ('1×', r'1\s*[×x]'),
                             ('Oordeel: PASS', r'(?im)^\s*[-*]?\s*Oordeel:\s*PASS\b')) if not re.search(pat, t)]
    if mist:
        fout.append(f'{rel}: keuring mist ' + ', '.join(mist))
if fout:
    sys.stderr.write('KEURSLOT: niet sturen.\n' + '\n'.join(fout) +
                     '\nMaak eerst het keurvel (tools/grounded/keurvel.py), bekijk het zelf op 8× en 1× naast de bron, '
                     'schrijf per onderdeel "lijkt op / wijkt af in" en alleen bij geen enkele afwijking "Oordeel: PASS". '
                     'Mijlpaal (pose, silhouet, kleur)? Eerst een onafhankelijke keurder. Zie SPRITE_WERKWIJZE.md, Checklist.\n')
    sys.exit(2)
