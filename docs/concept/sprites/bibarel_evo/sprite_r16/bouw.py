# bouw.py ronde 16 (vanaf sprite_r15): keuring van de hele sprite tegen Gen 3-vachtsprites en onze goedgekeurde sprites.
# Jordi: "ja de hele sprite moet goed gekeurd worden, hij moet consistent zijn met andere sprites".  Meting + oordeel: keuring_r15/rapport.md.
# Enige afwijking: in de kraagbol onder rechts ligt een lichte d-strook ONDER de c-schaduw (licht van onderen),
# terwijl het model daar donker is (L 72-88, boven 108-113). Tint naar c; vorm en lijnen ongewijzigd. Palet ongewijzigd.
# Draaien vanuit docs/concept/sprites/bibarel_evo:  python3 sprite_r16/bouw.py
import sys; sys.path.insert(0, 'keuring_r15')
import numpy as np
from PIL import Image, ImageDraw
from laad import gen3, ons, rgb as rgbref
ch = '.KbcdfSCeLMogWwD'; I = {c: i for i, c in enumerate(ch)}
im15 = Image.open('sprite_r15/sprite.png'); PAL = np.array(im15.getpalette()[:48]).reshape(16, 3).astype('uint8')
r15 = np.asarray(im15).astype(int); o = r15.copy()
ZONES = {
    'kraagbol onder rechts (licht-van-onderen weg)': {(32, 31): ('d', 'c'), (33, 31): ('d', 'c'), (34, 31): ('d', 'c')},
}
alle = {}
for z, W in ZONES.items():
    for (x, y), (oud, nieuw) in W.items():
        assert r15[y, x] == I[oud], (x, y, ch[r15[y, x]]); o[y, x] = I[nieuw]; alle[(x, y)] = z
def save(idx, pad, z=None):
    im = Image.new('P', (64, 64)); im.putpalette(PAL.ravel().tolist() + [0] * 3 * 240)
    im.putdata(idx.astype('uint8').ravel().tolist()); im.save(pad, transparency=0)
    if z: Image.fromarray(PAL[idx]).resize((64 * z, 64 * z), Image.NEAREST).save(pad.replace('.png', f'_{z}x.png'))
save(o, 'sprite_r16/sprite.png', 8)
# ---- bewijs: px per zone, diff 0 erbuiten, silhouet en lijnen ongewijzigd
diff = {(int(x), int(y)) for y, x in np.argwhere(o != r15)}
for z, W in ZONES.items(): print(f'{z}: {len(diff & set(W))} px')
print('diff buiten de zones:', sorted(diff - set(alle)), '| silhouet gewijzigd:', int(((o > 0) != (r15 > 0)).sum()),
      '| lijnpixels (K/b) aangeraakt:', sum(r15[y, x] in (I['K'], I['b']) for (x, y) in diff))
assert diff == set(alle) and ((o > 0) == (r15 > 0)).all()
assert not any(r15[y, x] in (I['K'], I['b']) or o[y, x] in (I['K'], I['b']) for (x, y) in diff)
# ---- vel: r16 | r15 8x (magenta = gewijzigd) ; kraag 16x ; naast referenties 2x ; 1x licht/donker
BG = (152, 208, 160)
def rgb(idx, bg=BG):
    t = Image.new('RGB', (64, 64), bg); t.paste(Image.fromarray(PAL[idx]), (0, 0), Image.fromarray(((idx > 0) * 255).astype('uint8'))); return t
def big(img, z, box=(0, 0, 64, 64)): return img.crop(box).resize(((box[2]-box[0])*z, (box[3]-box[1])*z), Image.NEAREST)
def mark(img, z, box, pts):
    d = ImageDraw.Draw(img)
    for (x, y) in pts:
        if box[0] <= x < box[2] and box[1] <= y < box[3]:
            X, Y = (x-box[0])*z, (y-box[1])*z; d.rectangle([X, Y, X+z-1, Y+z-1], outline=(255, 0, 255), width=2)
    return img
V = Image.new('RGB', (1060, 1330), 'white'); d = ImageDraw.Draw(V)
for i, (img, t) in enumerate([(mark(big(rgb(o), 8), 8, (0, 0, 64, 64), diff), 'r16 8x (magenta = gewijzigd)'), (mark(big(rgb(r15), 8), 8, (0, 0, 64, 64), diff), 'r15 8x')]):
    V.paste(img, (10 + i*522, 22)); d.text((10 + i*522, 6), t, fill='black')
kb = (22, 24, 40, 36); y0 = 548
for i, (idx, t) in enumerate([(o, 'kraag onder r16 16x'), (r15, 'kraag onder r15 16x')]):
    V.paste(mark(big(rgb(idx), 16, kb), 16, kb, diff), (10 + i*300, y0 + 16)); d.text((10 + i*300, y0), t, fill='black')
y1 = y0 + 16 + 12*16 + 14
d.text((10, y1), 'naast referenties 2x: r16 | Bibarel | Ursaring | Swampert | Linoone | Furret | Alphyena | Dundragoon', fill='black')
refs = [gen3(n) for n in ['bibarel', 'ursaring', 'swampert', 'linoone', 'furret']] + [ons('docs/concept/sprites/' + f) for f in ['mightyena_evo/af/alphyena.png', 'dundragoon/af/dundragoon.png']]
V.paste(big(rgb(o), 2), (10, y1 + 16))
for i, (a, p) in enumerate(refs): V.paste(rgbref(a, p).resize((128, 128), Image.NEAREST), (10 + (i+1)*130, y1 + 16))
y2 = y1 + 16 + 130 + 10
d.text((10, y2), '1x licht / donker (r16, Bibarel, Ursaring, Swampert)', fill='black')
for j, bg in enumerate([(248, 248, 248), (24, 24, 32)]):
    V.paste(rgb(o, bg), (10 + j*300, y2 + 16))
    for i, (a, p) in enumerate(refs[:3]): V.paste(rgbref(a, p, bg), (10 + j*300 + (i+1)*66, y2 + 16))
V.crop((0, 0, 1060, y2 + 16 + 64 + 10)).save('sprite_r16/vel.png')
