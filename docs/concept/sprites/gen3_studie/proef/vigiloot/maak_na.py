"""Vigiloot tintzone-proef: gerichte pixellijst op het origineel (geen kwantiseren/blur).
Draai vanuit de repo-root: python3 docs/concept/sprites/gen3_studie/proef/vigiloot/maak_na.py"""
from PIL import Image
SRC = 'docs/concept/sprites/wasbeer/af/wasbeer.png'
OUT = 'docs/concept/sprites/gen3_studie/proef/vigiloot/na.png'
H = '0123456789ABCDEF'

# zone -> lijst van (x, y, nieuwe index); per rij als (y, x_start, 'tekst')
ZONES = {
 'schouder (licht 7 zonder los 6-pixeltje)': [(22, 16, '7')],
 'borst (schaduwsikkel 5 rechts, harde grens)': [(20, 27, '5'), (21, 27, '5'), (23, 28, '5'), (24, 28, '55')],
 'heup/verre dij (licht als wig i.p.v. streep)': [
     (37, 32, '7'), (38, 31, '77'), (39, 30, '77'), (40, 29, '77'), (41, 29, '7'), (42, 28, '7')],
 'nabije dij (licht linksboven, 6 grond, 5 sikkel onder)': [
     (39, 23, '77'), (40, 22, '77'),
     (41, 21, '77'), (41, 24, '66'),
     (42, 20, '777'), (42, 23, '666'),
     (43, 20, '77'), (43, 22, '6666'),
     (44, 19, '77'), (44, 21, '66666'),
     (45, 18, '66666'),
     (46, 17, '6666'),
     (47, 17, '66'),
     (48, 16, '66')],
 'buitenlijn lichtkant (zwart -> donkerste eigen tint)': [
     (30, 14, '2'), (31, 13, '2'), (32, 12, '2'), (33, 11, '2'),          # onderarm
     (18, 53, '2'), (19, 50, '2'), (20, 49, '2'),                        # staart boven
     (21, 48, '2'), (22, 48, '2'), (23, 48, '2'), (24, 48, '2'), (25, 48, '2'), (26, 48, '2'),
     (29, 51, '2'), (30, 50, '4'),
     (34, 48, '2'), (35, 48, '2'), (36, 47, '2'), (37, 46, '2'),          # staart onder
     (53, 44, '2'), (54, 44, '2'), (55, 43, '2'), (56, 42, '2'),          # rechtervoet
     (57, 25, '2'), (58, 24, '2'), (59, 23, '2')],                       # linkervoet
}
FUR = set(H.index(c) for c in '34567')

im = Image.open(SRC); px = im.load()
orig = im.copy(); op = orig.load()
tel = {}
for zone, segs in ZONES.items():
    n = 0
    for (y, x0, s) in segs:
        for i, ch in enumerate(s):
            x = x0 + i; old = op[x, y]; new = H.index(ch)
            assert old != 0, (zone, x, y)
            if 'buitenlijn' in zone: assert old == 1, (zone, x, y, old)
            else: assert old in FUR and new in FUR, (zone, x, y, old)
            if old != new: n += 1
            px[x, y] = new
    tel[zone] = n
im.save(OUT)
for z, n in tel.items(): print(f'{n:3d}  {z}')
print('totaal', sum(tel.values()))
