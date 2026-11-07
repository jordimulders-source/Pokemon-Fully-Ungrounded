# Eindkeuring ronde 7: metingen (leest alleen)
import numpy as np, os
from PIL import Image
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
a = np.array(Image.open(D + '/nachtaap.png'))
sil = np.load(D + '/../../silhouet/silhouet_bevroren.npy')
H, W = a.shape
op = a > 0
print('pixels', op.sum(), 'kleuren gebruikt', len(np.unique(a[op])), sorted(np.unique(a[op]).tolist()))
print('alpha-diff tegen bevroren silhouet:', int((op != sil).sum()))

def nb(y, x):
    for dy, dx in ((-1,0),(1,0),(0,-1),(0,1)):
        yy, xx = y+dy, x+dx
        yield (a[yy, xx] if 0 <= yy < H and 0 <= xx < W else 0)

OUTL = {1, 2}
rand = [(y, x) for y in range(H) for x in range(W) if op[y, x] and any(v == 0 for v in nb(y, x))]
open_ = [(x, y, int(a[y, x])) for y, x in rand if a[y, x] not in OUTL]
print('randpixels', len(rand), 'zwart(1)', sum(a[y,x]==1 for y,x in rand), 'donkerviolet(2)', sum(a[y,x]==2 for y,x in rand))
print('aandeel index1 op de rand: %.2f' % (sum(a[y,x]==1 for y,x in rand)/len(rand)))
print('aandeel (1+2) totaal in sprite: %.3f, index1: %.3f' % (np.isin(a,[1,2]).sum()/op.sum(), (a==1).sum()/op.sum()))
print('open randen (niet-omlijning naast transparant) (x,y,idx):', open_)
# omlijningsbasis-tinten: welke randpixels links/boven (lichtkant) zijn 1?
los = []
for y in range(H):
    for x in range(W):
        if op[y, x] and all(v != a[y, x] for v in nb(y, x)) and a[y, x] not in (1, 2):
            los.append((x, y, int(a[y, x])))
print('losse pixels (geen 4-buur met dezelfde index, excl. omlijning):', len(los), los)
# rechte stukken op de omtrek (horizontaal/verticaal, >=4) -- rand = pixel met transparante buur
def runs(mask, label):
    out = []
    for y in range(H):
        x = 0
        while x < W:
            if mask[y, x]:
                s = x
                while x < W and mask[y, x]: x += 1
                if x - s >= 4: out.append((label, 'y=%d x=%d..%d (%d)' % (y, s, x-1, x-s)))
            else: x += 1
    return out
top = np.zeros_like(op); bot = np.zeros_like(op); lef = np.zeros_like(op); rig = np.zeros_like(op)
for y in range(H):
    for x in range(W):
        if op[y, x]:
            if y == 0 or not op[y-1, x]: top[y, x] = 1
            if y == H-1 or not op[y+1, x]: bot[y, x] = 1
            if x == 0 or not op[y, x-1]: lef[y, x] = 1
            if x == W-1 or not op[y, x+1]: rig[y, x] = 1
r = runs(top, 'boven') + runs(bot, 'onder') + [(l, t.replace('y=', 'X=').replace(' x=', ' y=')) for l, t in runs(lef.T, 'links')] + [(l, t.replace('y=', 'X=').replace(' x=', ' y=')) for l, t in runs(rig.T, 'rechts')]
print('rechte omtrekstukken >=4:'); [print('  ', l, t) for l, t in r]
# kene: index 6/7 op het lijf (y<=42, x>=17)
kz = np.zeros_like(op); kz[24:43, 17:50] = 1
k = np.isin(a, [6, 7]) & kz.astype(bool)
print('kene px (6/7 in lijfzone x17-49,y24-42):', int(k.sum()))
# bandbreedte: per kene-pixel de kortste run (horizontaal of verticaal) van 6/7
bw = []
for y, x in zip(*np.nonzero(k)):
    hx = 1; xx = x-1
    while xx >= 0 and k[y, xx]: hx += 1; xx -= 1
    xx = x+1
    while xx < W and k[y, xx]: hx += 1; xx += 1
    vy = 1; yy = y-1
    while yy >= 0 and k[yy, x]: vy += 1; yy -= 1
    yy = y+1
    while yy < H and k[yy, x]: vy += 1; yy += 1
    bw.append(min(hx, vy))
from collections import Counter
print('bandbreedte 6/7 (min run) verdeling:', sorted(Counter(bw).items()))
k5 = np.isin(a, [5, 6, 7]) & kz.astype(bool)
bw = []
for y, x in zip(*np.nonzero(k & True)):
    hx = 1; xx = x-1
    while xx >= 0 and k5[y, xx]: hx += 1; xx -= 1
    xx = x+1
    while xx < W and k5[y, xx]: hx += 1; xx += 1
    bw.append(hx)
print('horizontale breedte incl. rand 5:', sorted(Counter(bw).items()))
def L(c):
    r, g, b = [v/255 for v in c]; return 0.2126*r + 0.7152*g + 0.0722*b
pal = [tuple(int(v) for v in s.split()) for s in open(D + '/normal.pal').read().split('\n')[3:19]]
print('luminantie basis4 %.2f hl5 %.2f kene6 %.2f kene7 %.2f wit8 %.2f schaduw3 %.2f' % tuple(L(pal[i]) for i in (4,5,6,7,8,3)))
# oogkopie
le = a[43:49, 5:12]; re = a[43:49, 14:21]
print('ogen: verschil tussen linker (x5-11) en rechter (x14-20) oogblok, y43-48:', int((le != re).sum()), 'van', le.size)
# symmetrie kop x4..24 rond as x=13.5
kop = a[36:56, 3:25]
print('kopsymmetrie: gelijke pixels bij spiegelen', int((kop == kop[:, ::-1]).sum()), 'van', kop.size)
