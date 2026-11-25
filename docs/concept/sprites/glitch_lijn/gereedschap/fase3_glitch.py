# Fase 3 (Jordi, 25 nov): "ik wil dat je de vorige versie gaat bouwen ... alle magneten ga je compleet anders
# inkleuren, daar blijft niks meer van over, dat mag je allemaal glitch inkleuren, ga maar helemaal los, maar ik
# wil dat er geen magneten meer in te herkennen zijn"; "dus ook de ruimtes ertussen mag je meekleuren, alleen
# alle gezichten moeten intact blijven".
# Basis = Gemini r1 (natief). Beschermd = de gezichten (clusters van gekleurde pixels + rand van 3 px).
# Al het andere binnen het silhouet krijgt glitchvulling uit fase 1 (rijen van fase 1 zonder doorzichtige
# pixels achter elkaar geplakt = onze eigen MissingNo-data), met varianten.
# Jordi daarna: "er is teveel aan de hoofden gezeten, ook waar de magneten de hoofden overlapten mag je
# onderdeel van de hoofden maken" -> beschermd = hele hoofden (ellips om elk gezicht), en de hoofdpixels komen
# uit Gemini r2 (daar zijn de hoofden heel, zonder magneten ervoor).
# Gebruik: IN UITMAP [R2]
import sys, os, random; from PIL import Image; import numpy as np
IN, UIT = sys.argv[1], sys.argv[2]; os.makedirs(UIT, exist_ok=True)
a = np.asarray(Image.open(IN).convert('RGB')).astype(int); H, W, _ = a.shape
L = a.mean(2); sat = a.max(2) - a.min(2); fg = L < 235
kl = fg & (sat > 45)
ys, xs = np.where(kl)
dicht = np.zeros_like(kl)
for y, x in zip(ys, xs):
    if kl[max(0, y-4):y+5, max(0, x-4):x+5].sum() >= 7: dicht[y, x] = True
geel = kl & (a[..., 0] > 150) & (a[..., 1] > 150) & (a[..., 2] < 120)   # gezichten hebben geel (ogen/mond)
for y, x in zip(*np.where(dicht)):
    if not geel[max(0, y-5):y+6, max(0, x-5):x+6].any(): dicht[y, x] = False   # cyaan magneetpunt is geen gezicht
gez = np.zeros_like(kl)
for y, x in zip(*np.where(dicht)):
    gez[max(0, y-3):y+4, max(0, x-3):x+4] = True
gez &= fg
if len(sys.argv) > 3:
    r2 = np.asarray(Image.open(sys.argv[3]).convert('RGB')).astype(int); fg2 = r2.mean(2) < 235
    # gezichtsclusters (flood fill op 'dicht', buren binnen 3 px)
    rest = set(zip(*np.where(dicht))); hoofd = np.zeros_like(kl)
    while rest:
        st = [rest.pop()]; cl = list(st)
        while st:
            y, x = st.pop()
            for q in [p for p in rest if abs(p[0]-y) <= 3 and abs(p[1]-x) <= 3]:
                rest.discard(q); st.append(q); cl.append(q)
        if len(cl) < 10: continue
        cy = np.array([c[0] for c in cl]); cx = np.array([c[1] for c in cl])
        my, mx = (cy.min() + cy.max()) / 2 - 1.5, (cx.min() + cx.max()) / 2
        ry, rx = (cy.max() - cy.min()) / 2 + 5.5, (cx.max() - cx.min()) / 2 + 3.5
        yy, xx = np.mgrid[0:H, 0:W]
        hoofd |= ((yy - my) / ry) ** 2 + ((xx - mx) / rx) ** 2 <= 1
    hoofd &= fg2 & ~((r2.mean(2) > 110) & ((r2.max(2) - r2.min(2)) < 45) & ~gez)   # lichte staafresten in r2 niet
    gez = hoofd | gez
    a = a.copy(); a[hoofd] = r2[hoofd]; fg = fg | hoofd
glitch = fg & ~gez
# fase 1 als data
f1 = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../fase1_glitch/af/glitch_fase1.png')).convert('RGBA')
f = np.asarray(f1).astype(int)
data = np.concatenate([f[y][f[y, :, 3] > 0, :3] for y in range(64)])
FOUT = {'c': (16, 240, 248), 'C': (140, 246, 246), 'p': (230, 40, 220), 'P': (240, 140, 240), 'y': (248, 240, 64)}
def vul(seed, stap):
    rnd = random.Random(seed); out = a.copy(); off = rnd.randrange(len(data))
    for y in range(H):
        rij = off + y * stap
        for x in range(W):
            if glitch[y, x]: out[y, x] = data[(rij + x) % len(data)]
    return out
def foutbanden(out, seed, n=4):
    rnd = random.Random(seed)
    for _ in range(n):
        y0 = rnd.randrange(10, H - 10); h = rnd.choice((1, 2, 2, 3)); x0 = rnd.randrange(0, W - 20); w = rnd.randrange(8, 24)
        k1, k2 = rnd.sample(list(FOUT.values()), 2)
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                if glitch[y, x]: out[y, x] = k1 if out[y, x].mean() < 110 else k2
    return out
def rijen(out, seed, m=2):
    rnd = random.Random(seed); res = out.copy()
    for y in range(H):
        d = rnd.randint(-m, m)
        if not d: continue
        for x in range(W):
            if glitch[y, x]: res[y, x] = 255
        for x in range(W):
            if glitch[y, x] and 0 <= x + d < W and not gez[y, x + d]: res[y, x + d] = out[y, x]
    return res
B = vul(1, 23)
var = {'A_data': B, 'B_data_fout': foutbanden(B.copy(), 2), 'C_data_rijen': rijen(B, 3),
       'D_data_fout_rijen': rijen(foutbanden(B.copy(), 2), 3),
       'E_veel_fout_rijen': rijen(foutbanden(B.copy(), 4, 14), 5, 3)}
for n, o in var.items(): Image.fromarray(o.astype('uint8')).save(f'{UIT}/{n}.png')
Image.fromarray(np.where(gez[..., None], a, 255).astype('uint8')).save(f'{UIT}/_gezichten.png')
