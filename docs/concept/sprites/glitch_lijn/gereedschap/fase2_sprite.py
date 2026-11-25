# Van Gemini-afgeleide 63x63 naar Gen 3-sprite: 64x64, doorzichtig, 15 kleuren + doorzichtig.
# Kleuren van ogen/mond/losse pixels (verzadigd) krijgen eigen paletplekken, de grijzen de rest (k-means).
import sys; from PIL import Image; import numpy as np
IN, OUT, NK = sys.argv[1], sys.argv[2], 15
a = np.asarray(Image.open(IN).convert('RGB')).astype(float); H, W, _ = a.shape
fg = a.mean(2) < 235
sat = a.max(2) - a.min(2); kleur = fg & (sat > 45)
def kmeans(X, k, it=40):
    rng = np.random.default_rng(0); C = X[rng.choice(len(X), k, replace=False)]
    for _ in range(it):
        lab = ((X[:, None] - C[None]) ** 2).sum(2).argmin(1)
        C = np.array([X[lab == i].mean(0) if (lab == i).any() else C[i] for i in range(k)])
    return C
nk = 5
Ck = kmeans(a[kleur], nk); Cg = kmeans(a[fg & ~kleur], NK - nk)
P = np.vstack([Cg, Ck]).round()
out = np.zeros((64, 64, 4), 'uint8')
lab = np.full((H, W), -1)
lab[kleur] = ((a[kleur][:, None] - Ck[None]) ** 2).sum(2).argmin(1) + (NK - nk)
lab[fg & ~kleur] = ((a[fg & ~kleur][:, None] - Cg[None]) ** 2).sum(2).argmin(1)
for y in range(H):
    for x in range(W):
        if lab[y, x] >= 0: out[y, x] = list(P[lab[y, x]]) + [255]   # linksboven geplaatst; rij/kolom 64 leeg
im = Image.fromarray(out)
bb = im.getbbox(); body = im.crop(bb)
c = Image.new('RGBA', (64, 64)); c.paste(body, ((64 - body.width) // 2, 64 - body.height - 2))
c.save(OUT); print('kleuren', len(P), 'bbox', bb, 'maat', body.size)
