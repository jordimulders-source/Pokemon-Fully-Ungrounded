# Jordi (25 nov): "hij mist de pupillen die fase 2 heeft, probeer die netjes voor elk hoofd te doen, passend bij
# de vorm en het perspectief". Niets getekend: de ogen van fase 2 (oogkas, geel, pupil) worden als blok
# overgenomen op de hoofden die net als fase 2 naar voren kijken (ogenpaar naast elkaar); de gedraaide hoofden
# (ogen schuin boven elkaar, smalle spleten) houden hun eigen ogen, omdat het fase 2-oog daar niet in past.
import sys; from PIL import Image; import numpy as np
IN, OUT = sys.argv[1], sys.argv[2]
R, Y, B = (74, 24, 27), (221, 252, 70), (137, 84, 59)
f2 = np.asarray(Image.open('fase2_bug/af/glitch_fase2.png').convert('RGBA')).astype(int)
a = np.asarray(Image.open(IN).convert('RGBA')).astype(int).copy(); H, W = a.shape[:2]
def is_(arr, c): return (arr[..., :3] == c).all(-1) & (arr[..., 3] > 0)
def oogblok(x0, x1, y0, y1):
    s = f2[y0:y1, x0:x1]; m = is_(s, R) | is_(s, Y) | is_(s, B)
    ys, xs = np.where(m); return s[ys.min():ys.max()+1, xs.min():xs.max()+1], m[ys.min():ys.max()+1, xs.min():xs.max()+1]
SMAL, BREED = oogblok(25, 32, 31, 38), oogblok(34, 45, 31, 38)
oog = is_(a, R) | is_(a, Y); rood = is_(a, R)
seen = np.zeros_like(oog); cl = []
for y, x in zip(*np.where(rood)):
    if seen[y, x]: continue
    st = [(y, x)]; seen[y, x] = True; c = []
    while st:
        cy, cx = st.pop(); c.append((cy, cx))
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = cy+dy, cx+dx
                if 0 <= ny < H and 0 <= nx < W and oog[ny, nx] and not seen[ny, nx]: seen[ny, nx] = True; st.append((ny, nx))
    if len(c) >= 5: cl.append(np.array(c))
ogen = sorted([(c[:, 1].min(), c[:, 1].max(), c[:, 0].min(), c[:, 0].max(), c) for c in cl], key=lambda t: t[0])
gebruikt = set(); n = 0
for i, l in enumerate(ogen):
    for j, r in enumerate(ogen):
        if j <= i or i in gebruikt or j in gebruikt: continue
        dy = abs((l[2]+l[3])/2 - (r[2]+r[3])/2); dx = (r[0]+r[1])/2 - (l[0]+l[1])/2
        if dy <= 2 and 6 <= dx <= 14:                     # naar voren kijkend hoofd
            gebruikt |= {i, j}; n += 1
            for t, (s, m) in ((l, SMAL), (r, BREED)):
                x0, x1, y0, y1, c = t
                if m.shape[1] > (x1 - x0 + 1) + 1: s, m = SMAL[0][:, ::-1], SMAL[1][:, ::-1]   # klein hoofd: breed oog past niet
                for cy, cx in c: a[cy, cx, :3] = R
                h, w = m.shape; ty = (y0+y1+1)//2 - h//2; tx = (x0+x1+1)//2 - w//2
                for yy in range(h):
                    for xx in range(w):
                        if m[yy, xx]: a[ty+yy, tx+xx] = s[yy, xx]
print('hoofden met fase 2-ogen', n)
Image.fromarray(a.astype('uint8')).save(OUT)
