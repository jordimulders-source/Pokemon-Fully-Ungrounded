"""Coathief ronde 9 = af: de 5 klauwpixels uit de laatste keuring (`kleur/ronde8b/LAATSTE_KEURING.md`), silhouet ronde10."""
import numpy as np
from PIL import Image
src = Image.open('kleur/ronde8b/coathief.png'); a = np.array(src); b = a.copy()
SET = {(18, 56): (0xB, 0xA), (18, 57): (0xB, 0xA), (18, 58): (0xB, 0xA), (21, 58): (0xB, 0xA), (28, 61): (0xA, 0xF)}
for (x, y), (old, new) in SET.items():
    assert a[y, x] == old, ((x, y), a[y, x])
    b[y, x] = new
for p in ('kleur/ronde9/coathief.png', 'af/coathief.png'):
    o = Image.fromarray(b, 'P'); o.putpalette(src.getpalette()); o.save(p, transparency=0)
sil = np.array([[c == '#' for c in l.rstrip()] for l in open('silhouet/ronde10.txt')])
print('gewijzigd', int((a != b).sum()), '| alpha-diff', int(((b > 0) != sil).sum()), '| kleuren', len(np.unique(b)))
o = Image.open('af/coathief.png')
W = Image.new('RGBA', (4 * 266 + 10, 350), (236, 236, 230, 255))
W.alpha_composite(Image.open('silhouet/onderlaag_b1c_256.png').convert('RGBA'), (5, 5))
W.alpha_composite(Image.open('../olinguito_v2/af/olinguito.png').convert('RGBA').resize((256, 256), Image.NEAREST), (271, 5))
W.alpha_composite(o.convert('RGBA').resize((256, 256), Image.NEAREST), (537, 5))
D = Image.new('RGBA', (256, 256), (36, 38, 52, 255)); D.alpha_composite(o.convert('RGBA').resize((256, 256), Image.NEAREST)); W.alpha_composite(D, (803, 5))
for i, (im, bgc) in enumerate(((Image.open('../olinguito_v2/af/olinguito.png'), (236, 236, 230, 255)), (o, (236, 236, 230, 255)), (o, (36, 38, 52, 255)))):
    s = Image.new('RGBA', (64, 64), bgc); s.alpha_composite(im.convert('RGBA')); W.alpha_composite(s, (271 + 266 * i + 96, 275))
W.convert('RGB').save('af/vel.png')
