# Meetscript eindkeuring r13 -> r14. Draaien vanuit docs/concept/sprites/bibarel_evo:  python3 eindkeuring_r13/meet.py
# 1) buitenlijn per kant (licht = normaal naar links/boven, schaduw = rechts/onder), 2) om-en-om K/kleur op de buitenrand,
# 3) 2x2-zwartklonten, 4) zwarte binnenpixels, 5) kopvel: model (Gemini r10, 1024 px) geprojecteerd op het spriteraster | r13 | r14.
import numpy as np
from PIL import Image, ImageDraw
ch = '.KbcdfSCeLMogWwD'
def laad(p): return np.asarray(Image.open(p)).astype(int)
def rand(a):
    op = a > 0; pad = np.pad(op, 1); out = {}
    for y in range(64):
        for x in range(64):
            if not op[y, x] or pad[y:y+3, x:x+3].all(): continue
            s = sum(dx+dy for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) if not (0 <= x+dx < 64 and 0 <= y+dy < 64) or not op[y+dy, x+dx])
            out[(x, y)] = 'schaduw' if s > 0 else ('licht' if s < 0 else 'zij')
    return out
for naam in ('sprite_r13/sprite.png', 'sprite_r14/sprite.png'):
    a = laad(naam); R = rand(a); print('==', naam)
    for k in ('licht', 'schaduw', 'zij'):
        c = {}
        for p, kk in R.items():
            if kk == k: c[ch[a[p[1], p[0]]]] = c.get(ch[a[p[1], p[0]]], 0) + 1
        print(f'  buitenrand {k}:', dict(sorted(c.items(), key=lambda t: -t[1])))
    E = set(R); om = []
    for (x, y) in E:
        nb = [a[y+dy, x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dx or dy) and (x+dx, y+dy) in E]
        if a[y, x] == 1 and nb and all(v != 1 for v in nb): om.append((x, y, 'K tussen kleur'))
        if a[y, x] not in (1, 8) and len(nb) >= 2 and all(v == 1 for v in nb) and R[(x, y)] != 'zij': om.append((x, y, ch[a[y, x]] + ' tussen K'))
    print('  om-en-om op de buitenrand:', sorted(om))
    k = a == 1; print('  2x2 zwartklonten:', [(x, y) for y in range(63) for x in range(63) if k[y:y+2, x:x+2].all()])
    pad = np.pad(a > 0, 1)
    print('  zwarte binnenpixels:', [(x, y) for y in range(64) for x in range(64) if a[y, x] == 1 and pad[y:y+3, x:x+3].all()])

# kopvel
REF = np.asarray(Image.open('referenties/gemini_gekozen_r10.png').convert('RGB'))
s_, P, O = 64/90, 10.3, 5          # model/r10_k8 -> sprite: x = X/s_, y = 9+(y-6)/s_ ; natief -> 1024: *10.3+5 (gemeten, fout 5/255)
def refvak(x0, y0, x1, y1, Z):
    H, W = (y1-y0)*Z, (x1-x0)*Z; py, px = np.mgrid[0:H, 0:W]
    X = (((x0+(px+.5)/Z)/s_)*P+O).astype(int); Y = ((9+(y0+(py+.5)/Z-6)/s_)*P+O).astype(int)
    o = np.full((H, W, 3), 255, 'uint8'); ok = (X >= 0) & (X < 1024) & (Y >= 0) & (Y < 1024); o[ok] = REF[Y[ok], X[ok]]; return Image.fromarray(o)
def spritevak(pad, x0, y0, x1, y1, Z):
    im = Image.open(pad); a = np.asarray(im); Pl = np.array(im.getpalette()[:48]).reshape(16, 3).astype('uint8')
    rgb = Pl[a]; rgb[a == 0] = (152, 208, 160); return Image.fromarray(rgb[y0:y1, x0:x1]).resize(((x1-x0)*Z, (y1-y0)*Z), Image.NEAREST)
def raster(img, x0, y0, Z):
    d = ImageDraw.Draw(img)
    for i in range(img.width//Z+1): d.line([(i*Z, 0), (i*Z, img.height)], fill=(255,0,255) if (x0+i) % 5 == 0 else (70,70,70))
    for j in range(img.height//Z+1): d.line([(0, j*Z), (img.width, j*Z)], fill=(255,0,255) if (y0+j) % 5 == 0 else (70,70,70))
    for i in range(0, img.width//Z, 5): d.text((i*Z+2, 1), str(x0+i), fill=(255,0,255))
    for j in range(0, img.height//Z, 5): d.text((2, j*Z+10), str(y0+j), fill=(255,0,255))
    return img
b = (14, 10, 48, 34); Z = 16
vakken = [('model (Gemini r10 op spriteraster)', refvak(*b, Z)), ('r13', spritevak('sprite_r13/sprite.png', *b, Z)), ('r14', spritevak('sprite_r14/sprite.png', *b, Z))]
V = Image.new('RGB', (3*(34*Z+10), 24*Z+20), 'white'); d = ImageDraw.Draw(V)
for i, (t, im) in enumerate(vakken):
    V.paste(raster(im, b[0], b[1], Z), (i*(34*Z+10), 18)); d.text((i*(34*Z+10), 2), t + ' 16x', fill='black')
V.save('eindkeuring_r13/kop_model_r13_r14.png')
