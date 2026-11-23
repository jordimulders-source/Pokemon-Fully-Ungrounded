# r4 = r3 + reparaties uit sprite_v2_r3/KEURING.md, per script met assert op de oude index.
import numpy as np
from PIL import Image
def laad(v):
    im = Image.open(f'sprite_v2_r3/pinsir_evo_v2_r3_{v}.png'); return im, np.array(im)
def zet(a, lijst, oud, nieuw):
    for x, y in lijst:
        assert a[y, x] == oud, (x, y, a[y, x], oud); a[y, x] = nieuw
def basis(a):
    # 1 buitenlijn rugrand dicht
    for x, y in [(48,24),(54,29),(55,29),(56,29)]:
        assert a[y, x] != 0; a[y, x] = 1
    zet(a, [(15,49)], 14, 1)                          # 2 hooglicht van de buitenlijn
    for x, y in [(36,y) for y in range(56,60)] + [(37,y) for y in range(55,59)]:    # 3 scheen licht links (alleen index 4)
        if a[y, x] == 4: a[y, x] = 5
    for x, y in [(44,y) for y in range(55,60)] + [(43,59),(43,60)]:                   # 3 scheen schaduw rechts
        if a[y, x] == 4: a[y, x] = 3
    zet(a, [(16,21)], 14, 4)                          # 4 licht pixel tussen de ogen
    zet(a, [(12,14)], 1, 2)                           # 5 selout kopschild
imA, A = laad('A'); imB, B = laad('B')
A0, B0 = A.copy(), B.copy()
basis(A); basis(B)
# rug B: volume per plaat; zone = waar B van A verschilt (bounding box), naden = index 2 in die zone
d = np.argwhere(B0 != A0); y0, x0 = d.min(0); y1, x1 = d.max(0)
zone = np.zeros_like(B, bool); zone[y0:y1+1, x0:x1+1] = True
naad = zone & (B0 == 2)
n5 = n3 = 0
for y, x in np.argwhere(naad):
    for dy in (1, 2):                                  # onder de naad: lichte bovenrand van de plaat
        if y+dy < 64 and zone[y+dy, x] and B[y+dy, x] == 4: B[y+dy, x] = 5; n5 += 1
    if y-1 >= 0 and zone[y-1, x] and B[y-1, x] == 4: B[y-1, x] = 3; n3 += 1   # boven de naad: schaduwrand
print('rug B:', n5, 'px -> 5,', n3, 'px -> 3; zone', (x0, y0, x1, y1))
for v, im, a in [('A', imA, A), ('B', imB, B)]:
    o = Image.fromarray(a, 'P'); o.putpalette(im.getpalette()); o.save(f'sprite_v2_r4/pinsir_evo_v2_r4_{v}.png', transparency=0)
    c = Image.open(f'sprite_v2_r4/pinsir_evo_v2_r4_{v}.png'); assert (np.array(c) == a).all()
    z = zone & (a > 0) & (a != 1) & (a != 2)
    print(v, 'rug gem. index-helderheid', round(np.mean([0.3*p[0]+0.59*p[1]+0.11*p[2] for p in np.array(im.getpalette()).reshape(-1,3)[a[z]]]), 1))
