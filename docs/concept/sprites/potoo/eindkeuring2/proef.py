"""Eindkeuring 2: proef van de voorgestelde reparaties (schrijft alleen eindkeuring2/proef.png; de sprite blijft ongewijzigd)."""
import numpy as np; from PIL import Image, ImageDraw
D = 'docs/concept/sprites/potoo/'
im = Image.open(D + 'eind_r1/potoo.png'); a = np.array(im); pal = im.getpalette()
R = [(1, [(37, 3)], 2, 1), (2, [(42, 9)], 4, 1),
     (3, [(22, 40)], 1, 2), (3, [(22, 38)], 2, 8), (3, [(22, 39)], 2, 4),
     (4, [(44, 33), (44, 34), (44, 35)], 5, 6), (4, [(43, 46), (43, 47)], 6, 5),
     (5, [(24, 40), (25, 40), (27, 40)], 8, 7), (5, [(24, 41), (25, 41)], 4, 6),
     (6, [(34, 21)], 2, 4)]
b = a.copy()
for k, ps, old, new in R:
    for x, y in ps:
        assert a[y, x] == old, (k, x, y, a[y, x]); b[y, x] = new
z = 8; v = Image.new('RGB', (2 * 64 * z + 10, 64 * z + 80), (255, 255, 255)); d = ImageDraw.Draw(v)
for i, arr in enumerate((a, b)):
    t = Image.fromarray(arr, 'P'); t.putpalette(pal); m = Image.fromarray(((arr != 0) * 255).astype('uint8'))
    for j, bg in enumerate(((200, 208, 216), (248, 248, 248), (40, 40, 48))):
        g = Image.new('RGB', (64, 64), bg); g.paste(t.convert('RGB'), (0, 0), m)
        if j == 0: v.paste(g.resize((64 * z, 64 * z), Image.NEAREST), (i * (64 * z + 10), 0))
        else: v.paste(g, (i * (64 * z + 10) + 5 + (j - 1) * 70, 64 * z + 8))
for k, ps, _, _ in R:
    for x, y in ps:
        X = 64 * z + 10 + x * z; d.rectangle([X, y * z, X + z - 1, y * z + z - 1], outline=(255, 0, 0))
v.save(D + 'eindkeuring2/proef.png')
