"""Stap 1 van r6 (Jordi: "verder mag die nog iets meer achterover leunen"): het bovenlijf van r5 achterover zetten door de
handgetekende segmenten van ../r5/tekening.txt per rij naar rechts te schuiven: schuif(y) = round((HEUP - y) * tan(HOEK))
voor rijen boven de heup. Dat is een scheve (shear) draaiing van ±HOEK graden om de heup; elke rij blijft heel, dus oog,
spiraal en stippen breken niet (een echte draaiing met dichtstbijzijnde pixel deed dat wel, zie draai_proef.py).
Poten, steunstaart, staartlus en bliksem schuiven niet; de kop (met snavel en oren) schuift als één geheel. Uitvoer: tekening_basis.txt; tekening.txt = die basis, daarna met de
hand bijgewerkt (snavel, verre oor, naden). Draaien: python3.11 schuin.py"""
import math
HOEK = 8.0; HEUP = 38
VAST = ('# --- poten', '# --- steunstaart', '# --- bliksem', '# --- onderbuik')
STIJF = ('# --- kop', '# --- snavel', '# --- oren')   # kop als één stijf geheel: overal dezelfde schuif (die van rij 8), anders breken oog en spiraal
def schuif(y): return int(math.floor((HEUP - y) * math.tan(math.radians(HOEK)) + 0.5)) if y < HEUP else 0
uit = ['# Sprite r6 = r5 met het bovenlijf 8 graden achterover (schuin.py), daarna met de hand bijgewerkt. Per regel "rij kolom pixels".']
vast = False; stijf = False
for l in open('../r5/tekening.txt'):
    l = l.rstrip('\n')
    if l.startswith('# Sprite r5') or l.startswith('# Overgetrokken') or l.startswith('# ingetypt'): continue
    if l.startswith('#'):
        vast = l.startswith(VAST); stijf = l.startswith(STIJF)
        uit.append(l + ('   [blijft staan]' if vast else ('   [schuift als geheel ' + str(schuif(8)) + ']' if stijf else '   [schuift mee]'))); continue
    if not l.strip(): continue
    y, x, s = l.split(); y, x = int(y), int(x)
    uit.append(f'{y} {x if vast else x + (schuif(8) if stijf else schuif(y))} {s}')
open('tekening_basis.txt', 'w').write('\n'.join(uit) + '\n')
print('schuif per rij:', {y: schuif(y) for y in range(0, 38, 4)})
