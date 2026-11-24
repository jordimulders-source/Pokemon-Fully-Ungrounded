# bouw.py ronde 15 (vanaf sprite_r14): vachtvlekjes getoetst aan de Dragonfly Cave-gids r.1459-1465 (fur shading).
# Jordi: "maar kloppen de vlekjes op het lichaam ook met de dragonflycave regels?"  Toetsing per vlek: eindkeuring_r13/rapport.md.
# Alleen tinten in de vacht; lijnen, tuinbroek, gezicht, potlood, staart, klep: diff 0. Palet ongewijzigd.
# Draaien vanuit docs/concept/sprites/bibarel_evo:  python3 sprite_r15/bouw.py
import numpy as np
from PIL import Image, ImageDraw
ch = '.KbcdfSCeLMogWwD'; I = {c: i for i, c in enumerate(ch)}
im14 = Image.open('sprite_r14/sprite.png'); PAL = np.array(im14.getpalette()[:48]).reshape(16, 3).astype('uint8')
r14 = np.asarray(im14).astype(int); o = r14.copy()
WIJZIG = {
    (29, 27): ('d', 'c'),   # losse lichte pixel ingesloten door lijnen in de slagschaduw onder de snuit (licht-tegen-de-richting) -> opgenomen in die schaduw (30,26)(31,26)(30,27)
    (45, 38): ('e', 'd'),   # pootkleur (donker) midden in de bruine onderarm, naast de armlijn (44,38)/(45,37) die al doorloopt -> onderarmvulling d zoals (46,38)
}
for (x, y), (oud, nieuw) in WIJZIG.items():
    assert r14[y, x] == I[oud], (x, y, ch[r14[y, x]]); o[y, x] = I[nieuw]
def save(idx, pad, z=None):
    im = Image.new('P', (64, 64)); im.putpalette(PAL.ravel().tolist() + [0] * 3 * 240)
    im.putdata(idx.astype('uint8').ravel().tolist()); im.save(pad, transparency=0)
    if z: Image.fromarray(PAL[idx]).resize((64 * z, 64 * z), Image.NEAREST).save(pad.replace('.png', f'_{z}x.png'))
save(o, 'sprite_r15/sprite.png', 8)
diff = {(int(x), int(y)) for y, x in np.argwhere(o != r14)}
print('gewijzigd:', sorted(diff), '| buiten de lijst:', sorted(diff - set(WIJZIG)), '| silhouet gewijzigd:', int(((o > 0) != (r14 > 0)).sum()))
assert diff == set(WIJZIG) and ((o > 0) == (r14 > 0)).all()
assert not any(r14[y, x] in (I['K'], I['b']) for (x, y) in diff)   # geen lijnpixel (zwart/b) aangeraakt

BG = (152, 208, 160)
def rgb(idx):
    t = Image.new('RGB', (64, 64), BG); t.paste(Image.fromarray(PAL[idx]), (0, 0), Image.fromarray(((idx > 0) * 255).astype('uint8'))); return t
def big(img, z, box=(0, 0, 64, 64)): return img.crop(box).resize(((box[2]-box[0])*z, (box[3]-box[1])*z), Image.NEAREST)
def mark(img, z, box, pts):
    d = ImageDraw.Draw(img)
    for (x, y) in pts:
        if box[0] <= x < box[2] and box[1] <= y < box[3]:
            X, Y = (x-box[0])*z, (y-box[1])*z; d.rectangle([X, Y, X+z-1, Y+z-1], outline=(255, 0, 255), width=2)
    return img
# getoetste vlekken (geel omkaderd in het vachtvak), gewijzigd = magenta
GETOETST = [(28,26),(17,27),(27,27),(49,27),(50,28),(21,31),(18,34),(19,35),(28,35),(26,34),(27,34),(29,27),(45,38),(51,42),(49,43),(50,44),(50,45),(43,45),(44,45)]
V = Image.new('RGB', (1060, 1080), 'white'); d = ImageDraw.Draw(V)
for i, (img, t) in enumerate([(mark(big(rgb(o), 8), 8, (0,0,64,64), diff), 'r15 8x (magenta = gewijzigd)'), (big(rgb(r14), 8), 'r14 8x')]):
    V.paste(img, (10 + i*522, 22)); d.text((10 + i*522, 6), t, fill='black')
vb = (14, 24, 54, 47); y0 = 560
for i, (idx, t) in enumerate([(o, 'vacht r15 12x (geel = getoetste vlek, magenta = gewijzigd)'), (r14, 'vacht r14 12x')]):
    img = big(rgb(idx), 12, vb); dd = ImageDraw.Draw(img)
    for (x, y) in GETOETST:
        X, Y = (x-vb[0])*12, (y-vb[1])*12; dd.rectangle([X+2, Y+2, X+9, Y+9], outline=(255, 220, 0), width=1)
    if idx is o: mark(img, 12, vb, diff)
    V.paste(img.crop((0, 0, 480, 276)), (10 + i*500, y0 + 18)); d.text((10 + i*500, y0), t, fill='black')
V.crop((0, 0, 1060, y0 + 18 + 286)).save('sprite_r15/vel.png')
