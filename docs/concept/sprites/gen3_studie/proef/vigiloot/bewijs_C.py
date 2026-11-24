"""voor_na_C.png + bewijs voor variant C. Draai vanuit de repo-root."""
from PIL import Image
from collections import Counter
D = 'docs/concept/sprites/gen3_studie/proef/vigiloot/'
v = Image.open('docs/concept/sprites/wasbeer/af/wasbeer.png'); A = Image.open(D + 'na.png'); C = Image.open(D + 'na_C.png')
vp, ap, cp = v.load(), A.load(), C.load()
R = [(x, y) for x in range(64) for y in range(64)]
print('mode/size/kleuren', C.mode, C.size, len(set(cp[q] for q in R)))
print('alfa-diff', sum((vp[q] == 0) != (cp[q] == 0) for q in R))
print('gezicht index-diff (kop rij 0-19, x 9-33)', sum(vp[x, y] != cp[x, y] for x in range(9, 34) for y in range(20)))
print('onderdelen (index 8-F) gewijzigd', sum(vp[q] != cp[q] and vp[q] >= 8 for q in R))
vpal, cpal = v.getpalette(), C.getpalette()
print('andere paletkleuren', [(i, tuple(vpal[3*i:3*i+3]), tuple(cpal[3*i:3*i+3])) for i in range(16) if vpal[3*i:3*i+3] != cpal[3*i:3*i+3]])
print('pixeldiff C t.o.v. origineel', sum(vp[q] != cp[q] for q in R), '| t.o.v. A', sum(ap[q] != cp[q] for q in R))
lijf = lambda im: Counter(im.load()[x, y] for x in range(10, 43) for y in range(20, 52))
for nm, im in (('voor', v), ('C', C)):
    c = lijf(im); print(nm, 'lijf rij 20-51: licht7', c[7], 'grond6', c[6], 'schaduw5', c[5], 'glans3', c[3])
def rgb(im):
    p = im.getpalette(); q = im.load(); o = Image.new('RGB', (64, 64), (255, 255, 255)); oo = o.load()
    for (x, y) in R:
        if q[x, y]: oo[x, y] = tuple(p[3*q[x, y]:3*q[x, y]+3])
    return o
ims = [rgb(v), rgb(A), rgb(C)] + [rgb(Image.open(f'graphics/pokemon/{s}/anim_front_gba.png').crop((0, 0, 64, 64))) for s in ('ursaring', 'linoone')]
k, g = 6, 8
vel = Image.new('RGB', (len(ims)*(64*k + g) + g, 64*k + 64 + 3*g), (232, 232, 224))
for i, im in enumerate(ims):
    x = g + i*(64*k + g); vel.paste(im.resize((64*k, 64*k), Image.NEAREST), (x, g)); vel.paste(im, (x, 64*k + 2*g))
vel.save(D + 'voor_na_C.png')
