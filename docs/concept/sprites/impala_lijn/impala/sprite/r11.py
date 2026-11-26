# r11: EINDKEURING Dragonfly Cave (schaduw + belijning + kleurtinten) op r9 (= r10).
# Jordi (26 nov): "nee je mag nu gaan beginnen met de eindkeuring, dus netter maken".
# Alleen uitvoering: niets getekend, geen vormwijziging (alpha-diff 0), geen AA op de buitenrand, geen vlakken gemiddeld.
# Elke pixelwijziging hieronder is gemeten: modellijn (kaal_lf = aandeel zwarte modellijn in de cel) of modelhelderheid
# (kaal_nla = vlakgemiddelde zonder lijn), of de 1-px-regel van de gids.
# Coordinaten = absolute spritecoordinaten (64x64); model-cel = (x-OX, y-OY) met OX=10, OY=1.
import os, json, numpy as np
from PIL import Image
RN = 'r11'
src = Image.open('r9/impala_r9.png')
a0 = np.array(src); a = a0.copy()
pal0 = src.getpalette()[:48]
# indexen r9: 0 transp, 1 zwart '0', 2 D, 3 S, 4 M, 5 N, 6 L, 7 H, 8 W, 9 '1' (ongebruikt), 10 A, 11 staal 3, 12 staal 4, 13 staal 5
NAAM = {1: '0', 2: 'D', 3: 'S', 4: 'M', 5: 'N', 6: 'L', 7: 'H', 8: 'W', 10: 'A', 11: '3', 12: '4', 13: '5'}
IDX = {v: k for k, v in NAAM.items()}
LF = np.load('kaal_lf.npy'); NLA = np.load('kaal_nla.npy'); LUM = (NLA * [.299, .587, .114]).sum(2)
OX, OY = 10, 1
log = []
def zet(zone, x, y, oud, nieuw, waarom):
    assert NAAM[a[y, x]] == oud, (x, y, NAAM[a[y, x]], oud)
    a[y, x] = IDX[nieuw]
    log.append((zone, x, y, oud, nieuw, int(round(LUM[y - OY, x - OX])), int(round(100 * LF[y - OY, x - OX])), waarom))

# ---- 1. BELIJNING ----
# 1a. dubbele hoekpixels: lijnpixel zonder transparante 4-buur waarvan de twee lijnburen diagonaal al aansluiten
#     (gids: "remove the clusters so that the outline is always one pixel wide"); vulling = buurtint die bij de modelhelderheid past
zet('kin/hals', 19, 30, '0', 'N', '1px: (18,30)-(19,31) sluiten diagonaal; model 140 -> N zoals buren (20,30),(19,29)')
zet('manen/rug', 33, 33, '0', 'S', '1px: (33,32)-(34,33) sluiten diagonaal; model 93 -> S zoals buren')
zet('kuif', 21, 14, 'D', 'S', '1px: (21,13)-(22,14) sluiten diagonaal; model 110 -> S (kuifvulling)')
# 1b. zwart aan de lichtkant: bovenhoek rechteroor, transparant erboven (normaal omhoog) -> selout D zoals de rest van de oorrand
zet('oor rechts', 28, 18, '0', 'D', 'lichtkant (boven): zwart -> outline base D, sluit aan op D-bovenrand (29-31,17)')
# 1c. binnenlijn buik over verre achterpoot (gids/E2: vorm over vorm -> lijn in de outline base, niet zwart);
#     de modellijn loopt door (36,46)D .. (40,45)D; per kolom de cel met de hoogste lijnfractie
zet('buik/verre achterpoot', 37, 45, 'M', 'D', 'modellijn (lf 39%, kolom 37 hoogste) verbindt (36,46)D met (40,45)D')
zet('buik/verre achterpoot', 38, 45, 'N', 'D', 'modellijn (lf 49%)')
zet('buik/verre achterpoot', 39, 45, 'M', 'D', 'modellijn (lf 23%, rij 46 = 0%)')

# ---- 2. SCHADUW ----
zet('buiksikkel', 36, 45, 'M', 'N', 'boven de nieuwe buiklijn: M-vlakje was donkerder dan beide kanten (model 196); N sluit de bestaande buiksikkel (37-40,44) aan op (33-34,45-46)')
zet('bil', 43, 39, 'H', 'L', 'los H-vlakje van 2 px (restant strepen-weg); model 193 = flank L')
zet('bil', 44, 39, 'H', 'L', 'idem; model 197 = flank L')

# ---- BEVROREN (asserts) ----
d = a != a0
assert ((a0 == 0) == (a == 0)).all(), 'silhouet gewijzigd'
assert not d[21:28, 18:26].any(), 'oogzone gewijzigd'
ex = json.load(open('extra_r9.json'))
STREEP = [(x + OX, y + OY) for _, x, y in ex]
assert all(not d[y, x] for x, y in STREEP), 'strepen gewijzigd'
assert all(a0[y, x] == 1 for x, y in STREEP)
wit = [(x, y) for y in range(31, 48) for x in range(18, 30) if a0[y, x] == 8]
assert all(not d[y + j, x + i] for x, y in wit for i in (-1, 0, 1) for j in (-1, 0, 1)), 'witte borst/buik of grens gewijzigd'

# ---- 3. KLEURTINTEN ----
# staal lag in helderheid en kleur bovenop de vacht (CIELAB-afstand: 3~D 4,7; 4~N 3,9; 5~H 2,1 = bijna-dubbel).
# Nieuw: koel staal naar Steelix (normal_gba.pal: blauw in de schaduw #4A5A7B b* -21, lichter = neutraler), zelfde rol per tint;
# gekozen uit 3 proeven (blauwer A te blauw t.o.v. het zilveren model, C te dicht bij H): CIELAB-afstand tot elke vachttint nu 7,2–12,5 (was 2,1–4,7).
STAAL = {11: (0x3E, 0x4A, 0x68), 12: (0x7E, 0x8D, 0xAA), 13: (0xCC, 0xD7, 0xEA)}
# palet compact: ongebruikte index 9 ('1' #1C2436, bijna gelijk aan zwart) eruit
used = [0] + sorted(set(np.unique(a)) - {0})
remap = np.zeros(256, 'uint8'); pal = []
for n, i in enumerate(used):
    remap[i] = n
    pal += list(STAAL.get(i, tuple(pal0[3 * i:3 * i + 3])))
pal += [0, 0, 0] * (16 - len(used))
out = remap[a]
os.makedirs(RN, exist_ok=True)
im = Image.fromarray(out, 'P'); im.putpalette(pal); im.save(f'{RN}/impala_{RN}.png', transparency=0)
r = Image.open(f'{RN}/impala_{RN}.png'); rgba = np.array(r.convert('RGB').convert('RGBA')); rgba[np.array(r) == 0, 3] = 0
Image.fromarray(rgba).resize((512, 512), Image.NEAREST).save(f'{RN}/impala_{RN}_8x.png')
with open(f'{RN}/wijzigingen.txt', 'w') as f:
    for e in log: f.write('%s (%d,%d) %s->%s  model %d, lijn %d%%  %s\n' % e)
from collections import Counter
print(RN, len(log), 'px', dict(Counter(z for z, *_ in log)), 'kleuren', len(used) - 1, '+ transparant')
