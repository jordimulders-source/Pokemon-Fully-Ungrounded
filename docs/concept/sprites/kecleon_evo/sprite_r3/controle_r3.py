# Controles r3: silhouet-diff met r2, zwart-aandeel, p90 helderheid, stappen per ramp, losse pixels,
# kleine tintvlakjes (<3 px), dubbele lijnen (lijnpixel met lijnpixel aan beide kanten in dezelfde richting).
import numpy as np
from PIL import Image
from bouw_r3_palet import PAL
T = np.load('raster_r3.npy', allow_pickle=True)
R2 = np.load('../sprite_r2/raster_r2.npy', allow_pickle=True)
print('silhouet-diff met r2:', int(((T!='.') != (R2!='.')).sum()), 'px')
sil = T != '.'
n = sil.sum()
Y = lambda c: 0.299*c[0] + 0.587*c[1] + 0.114*c[2]
ys = np.array([Y(PAL[T[y,x]]) for y,x in zip(*np.nonzero(sil))])
print('pixels', n, '| zwart (k) %.1f%%' % (100*(T=='k').sum()/n), '| zeer donker (Y<60) %.1f%%' % (100*(ys<60).mean()))
print('p90 helderheid %.0f | mediaan %.0f' % (np.percentile(ys,90), np.median(ys)))
for naam, ramp in [('oranje', 'rHGF'), ('mosterd', 'ECBA'), ('roze', 'qp')]:
    v = [round(Y(PAL[c])) for c in ramp]
    print(naam, ramp, v, 'stappen', [b-a for a,b in zip(v, v[1:])])
cnt = {c: int((T==c).sum()) for c in 'krHGFECBApqw'}
print('aantallen', cnt)
# losse pixels: geen enkele 4-buur met dezelfde kleur (lijnen k/r/E uitgezonderd want 1 px breed)
los = []
for y in range(63):
    for x in range(63):
        c = T[y,x]
        if c in '.krEw': continue
        if not any(0<=y+dy<63 and 0<=x+dx<63 and T[y+dy,x+dx]==c for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))):
            los.append((x,y,c))
print('losse pixels (x,y,kleur; y = rasterrij, beeld-y = +1):', los)
# kleine clusters (<3) van vultinten
from collections import deque
seen = np.zeros((63,63), bool); klein = []
for y in range(63):
    for x in range(63):
        c = T[y,x]
        if seen[y,x] or c in '.krEw': continue
        q = deque([(y,x)]); seen[y,x] = True; comp = []
        while q:
            a,b = q.popleft(); comp.append((b,a))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx = a+dy, b+dx
                if 0<=yy<63 and 0<=xx<63 and not seen[yy,xx] and T[yy,xx]==c:
                    seen[yy,xx] = True; q.append((yy,xx))
        if len(comp) < 3: klein.append((c, comp))
print('vlakjes < 3 px:', klein)
# zwarte klonten 2x2
kl = [(x,y) for y in range(62) for x in range(62) if all(T[y+a,x+b]=='k' for a in (0,1) for b in (0,1))]
print('2x2 zwarte klonten:', kl)
