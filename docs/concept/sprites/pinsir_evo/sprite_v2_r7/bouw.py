# Pinsir-evolutie v2 r7 = r6 + de 4 reparaties uit sprite_v2_r6/KEURING.md, per script met assert op de oude index.
# Draaien vanuit docs/concept/sprites/pinsir_evo/:  python3 sprite_v2_r7/bouw.py
import sys; sys.path.insert(0, 'sprite_v2_r6')
import numpy as np
from PIL import Image
from scipy import ndimage as nd
from collections import Counter
from palet import lijst
R6 = np.array(Image.open('sprite_v2_r6/pinsir_evo_v2_r6.png')); A = R6.copy()
WIJZ = {}
def zet(lijst_, oud, nieuw, reden):
    for x, y in lijst_:
        assert R6[y, x] == oud, (x, y, R6[y, x], oud, reden); A[y, x] = nieuw; WIJZ[(x, y)] = reden

# --- 2. nabije arm een tint lichter dan het lijf ---
R2 = 'arm'
zet([(x, y) for x in (33, 34, 35) for y in (37, 38, 39) if R6[y, x] == 4] + [(33,40),(34,40),(33,41),(34,41)], 4, 5, R2)
zet([(35,39),(36,38),(36,39)], 3, 4, R2)
zet([(39,45),(40,45)], 1, 3, R2)
# --- 3. knie als gesloten ring in 3, hooglicht binnen de ring ---
R3 = 'knie'
zet([(37,50),(38,50),(39,50),(36,51),(35,52),(35,53)], 5, 3, R3)
zet([(35,54)], 4, 3, R3)
zet([(36,52)], 14, 5, R3); zet([(38,52)], 5, 14, R3)
assert R6[52, 37] == 14            # (37,52) is al 14 en blijft
# --- 4. buitenrand ---
zet([(37,62)], 6, 1, 'buitenrand')
# --- 1b. lichte randstreep schild doorlopend ---
zet([(29,20)], 4, 5, 'randstreep'); zet([(31,19)], 4, 5, 'randstreep')

# --- 1. korrel: bruine vlakjes (3/4/5) < 3 px nemen de meest voorkomende buurtint ---
# Laten staan: gezicht (x11-22, y20-33), klauwen (room), stekelflanken (bruin binnen 2 px van transparant boven y31), hooglichten 14,
# de randstreep van het schild en alle pixels van de reparaties 2-4. Lijnpixels (1/2) worden nooit aangeraakt.
BESCHERM = np.zeros((64, 64), bool)
BESCHERM[20:34, 11:23] = True
rand = nd.binary_dilation(A == 0, np.ones((5, 5))); rand[31:, :] = False; BESCHERM |= rand
for x, y in WIJZ: BESCHERM[y, x] = True
for x, y in [(34,18),(32,19),(33,19),(26,20),(27,20),(28,20)]: BESCHERM[y, x] = True
# uitzondering op de stekelbescherming: de keurder noemt deze kopschildpixels als korrel
for x, y in [(30,20),(31,20),(35,18),(34,19),(34,23),(35,23)]: BESCHERM[y, x] = False
def vlakjes(a):
    uit = []
    for v in (3, 4, 5):
        lab, n = nd.label(a == v)
        for i in range(1, n + 1):
            pts = np.argwhere(lab == i)
            if len(pts) < 3: uit.append((v, [(int(x), int(y)) for y, x in pts]))
    return uit
for ronde in range(4):
    veranderd = 0
    for v, pts in vlakjes(A):
        if any(BESCHERM[y, x] for x, y in pts): continue
        bu = Counter()
        for x, y in pts:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    xx, yy = x + dx, y + dy
                    if (xx, yy) in pts or not (0 <= xx < 64 and 0 <= yy < 64): continue
                    if A[yy, xx] in (3, 4, 5, 14) and A[yy, xx] != v: bu[int(A[yy, xx])] += 1
        if not bu: continue
        w = bu.most_common(1)[0][0]
        if w == 14: w = 5          # hooglicht niet uitbreiden
        for x, y in pts: A[y, x] = w; WIJZ[(x, y)] = 'korrel'
        veranderd += 1
    if not veranderd: break

# los bruin pixel midden in de buik (alleen room eromheen): wordt room 6, de buurtint
assert A[50, 25] == 5; A[50, 25] = 6; WIJZ[(25, 50)] = 'korrel'

if __name__ == '__main__':
    o = Image.fromarray(A, 'P'); o.putpalette(lijst()); o.save('sprite_v2_r7/pinsir_evo_v2_r7.png', transparency=0)
    c = Image.open('sprite_v2_r7/pinsir_evo_v2_r7.png'); assert (np.array(c) == A).all()
    d = np.argwhere(A != R6)
    assert all((x, y) in WIJZ for y, x in d)
    assert not np.isin(R6[A != R6], (1, 2)).any() or set(map(tuple, np.argwhere((A != R6) & np.isin(R6, (1, 2)))[:, ::-1])) <= {(39,45),(40,45),(37,62)}
    print('gewijzigd:', len(d), Counter(WIJZ[(int(x), int(y))] for y, x in d))
    rest = [(v, p) for v, p in vlakjes(A) if not all(BESCHERM[y, x] for x, y in p)]
    print('bruine vlakjes < 3 px (r6):', len(vlakjes(R6)), ' r7:', len(vlakjes(A)), ' waarvan niet (geheel) beschermd:', rest)
    K = [(38,33),(38,34),(39,35),(41,35),(44,35),(40,36),(41,37),(45,37),(41,38),(45,39),(46,40),(46,41),(52,37),(52,38),(52,39),(52,40),(52,41),(45,44),(48,45),
         (33,28),(36,28),(34,28),(35,28),(36,27),(37,27),(34,23),(35,23),(28,23),(29,23),(35,46),(37,47),(38,47),(40,49),(40,50),(33,50),(33,51),(45,52),(46,52),(40,55),(41,55),
         (18,49),(19,49),(18,50),(19,50),(23,51),(22,53),(16,56),(30,20),(31,20),(35,18),(34,19)]
    print('keurderlijst: niet gewijzigd:', [(x, y, int(A[y, x])) for x, y in K if A[y, x] == R6[y, x]])
