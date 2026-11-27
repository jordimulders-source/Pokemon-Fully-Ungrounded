# r5 = r2 met een nieuw oog, 1-op-1 uit het model (Jordi: "kijk naar het model" / "kijk naar pokemon met kleine ogen").
# Model natief, kolom 20-22 x rij 56-58 (meet.py / nat.npy):
#   r56: zwart(2)   donkergrijs(81)  zwart(28)      -> ooglid/wenkbrauw   -> lijn in donkerste kopgrijs (5), zoals Onix (lid = donkere lijftint 82/74/74, niet zwart)
#   r57: wit(245)   zwart(2)         creme(232)     -> glans, pupil, oogwit
#   r58: zwart(1)   zwart(1)         creme(228)     -> pupil, pupil, oogwit
# Op natieve grootte (3x3) neergezet op sprite x12-14, y47-49: de glans landt zo op (12,48), de gemeten glansplek op spriteschaal.
# Pupil (zwart) linksonder in de lichte vlek, oogwit (creme) rechts -> kijkt naar linksbeneden zoals het model.
# Het oude Sandshrew-vak buiten dit blok (x10-11, y47-49) opnieuw gemeten: lijn (>=30% zwart) -> 5 (ooglidlijn), anders meerderheid.
# Zwarte kop-pixels direct rond het oog (x10-15, y46-50, niet op de silhouetrand) -> 5. Pupil is het enige zwart.
import sys, numpy as np
from PIL import Image
D = __file__.rsplit('/', 1)[0]; sys.path.insert(0, D)
import meet
r2 = np.load(D + '/r2.npy'); a = r2.copy(); H, W = a.shape
pal = Image.open(D + '/r2.png').getpalette()
PAL = [tuple(pal[3*i:3*i+3]) for i in range(16)]
VUL = [2, 3, 4, 5, 6, 7, 8, 9, 10]
bron = {}
for y in range(47, 50):
    for x in (10, 11):
        c = meet.cellen(x, y); tot = sum(w for w, _, _ in c)
        lijn = sum(w for w, _, k in c if k == 'K') / tot
        if lijn >= 0.30: a[y, x] = 5; bron[(x, y)] = f'model: {lijn:.0%} zwart = ooglidlijn -> 5'
        else:
            m, _ = meet.meerderheid(x, y, PAL, VUL); a[y, x] = m; bron[(x, y)] = f'model: meerderheid -> {m}'
BLOK = {(12, 47): (5, 'nat (20,56) zwart, lid -> 5'), (13, 47): (5, 'nat (21,56) donkergrijs 81 -> 5'), (14, 47): (5, 'nat (22,56) zwart, lid -> 5'),
        (12, 48): (11, 'nat (20,57) wit 245 = glans'), (13, 48): (1, 'nat (21,57) zwart = pupil'), (14, 48): (10, 'nat (22,57) creme 232 = oogwit'),
        (12, 49): (1, 'nat (20,58) zwart = pupil'), (13, 49): (1, 'nat (21,58) zwart = pupil'), (14, 49): (10, 'nat (22,58) creme 228 = oogwit')}
for (x, y), (v, b) in BLOK.items(): a[y, x] = v; bron[(x, y)] = b
PUPIL = {(13, 48), (12, 49), (13, 49)}
def rand(y, x):
    return any(a[yy, xx] == 0 for yy in range(y-1, y+2) for xx in range(x-1, x+2) if 0 <= yy < H and 0 <= xx < W)
for y in range(46, 51):
    for x in range(10, 16):
        if a[y, x] == 1 and (x, y) not in PUPIL and not rand(y, x):
            a[y, x] = 5; bron[(x, y)] = 'r2 zwart rond het oog -> 5 (lid/omlijning in donkere kopgrijs, Onix)'
buiten = (a != r2); buiten[46:51, 10:16] = False
assert buiten.sum() == 0
np.save(D + '/r5.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(pal); im.save(D + '/r5.png', transparency=0)
rgb = Image.open(D + '/r5.png').convert('RGBA'); bg = Image.new('RGBA', rgb.size, (255, 255, 255, 255)); bg.alpha_composite(rgb)
bg.resize((512, 512), Image.NEAREST).save(D + '/r5_8x.png')
print('diff t.o.v. r2:', (a != r2).sum())
for (x, y) in sorted(bron, key=lambda p: (p[1], p[0])):
    print(f'  ({x},{y}) r2={r2[y,x]:2d} r5={a[y,x]:2d}  {bron[(x,y)]}')
for y in range(45, 52): print('  ', y, ''.join({0: '.', 1: '#', 11: 'O', 10: 'x', 5: '+', 12: 'z'}.get(int(v), chr(ord('a') + int(v) - 2)) for v in a[y, 7:17]))
