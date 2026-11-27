# Vel r5: model-oog natief 12x | r5-oog 12x | referentie-ogen (Donphan, Golem, Tauros, Rhydon) 12x | r5 op 2x en 1x
import numpy as np
from PIL import Image, ImageDraw
D = __file__.rsplit('/', 1)[0]; G = D + '/../../../../../../graphics/pokemon/'
Z = 12
def raster(im):
    d = ImageDraw.Draw(im)
    for k in range(0, im.width + 1, Z): d.line([(k, 0), (k, im.height)], fill=(200, 200, 200))
    for k in range(0, im.height + 1, Z): d.line([(0, k), (im.width, k)], fill=(200, 200, 200))
    return im
def pidx(f, box):
    im = Image.open(f); a = np.array(im); pal = np.array(im.getpalette()[:48]).reshape(16, 3)
    rgb = pal[a]; rgb[a == 0] = 255
    x0, y0, x1, y1 = box
    return raster(Image.fromarray(rgb[y0:y1, x0:x1].astype('uint8')).resize(((x1-x0)*Z, (y1-y0)*Z), Image.NEAREST))
nat = np.load(D + '/nat.npy')
panelen = [('model natief (kol 16-26, rij 52-62)', raster(Image.fromarray(nat[52:62, 16:26]).resize((10*Z, 10*Z), Image.NEAREST))),
           ('r5 (x8-17, y43-52)', pidx(D + '/r5.png', (8, 43, 17, 52))),
           ('Donphan', pidx(G + 'donphan/anim_front_gba.png', (22, 29, 31, 38))),
           ('Golem', pidx(G + 'golem/anim_front_gba.png', (19, 29, 28, 38))),
           ('Tauros', pidx(G + 'tauros/anim_front_gba.png', (14, 26, 23, 35))),
           ('Rhydon', pidx(G + 'rhydon/anim_front_gba.png', (18, 17, 27, 26)))]
bw = sum(p.width + 12 for _, p in panelen); bh = max(p.height for _, p in panelen) + 20
s = Image.open(D + '/r5.png').convert('RGBA'); licht = Image.new('RGBA', (64, 64), (248, 248, 240, 255)); licht.alpha_composite(s)
vel = Image.new('RGB', (max(bw, 400), bh + 150), 'white'); d = ImageDraw.Draw(vel); x = 0
for t, p in panelen:
    vel.paste(p, (x, 18)); d.text((x, 2), t, fill=(200, 0, 0)); x += p.width + 12
vel.paste(licht.resize((128, 128), Image.NEAREST).convert('RGB'), (0, bh + 10)); vel.paste(licht.convert('RGB'), (150, bh + 10))
vel.save(D + '/vel_r5.png'); print(vel.size)
