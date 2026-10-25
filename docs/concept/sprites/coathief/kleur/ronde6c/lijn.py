"""Coathief ronde 6c: Jordi's lijn (`referenties/krabbel_jordi_belijning.png`, schaal 6x, gemeten via het oog) als
omlijning tussen de nabije schouder en de staande verre poot: "het zit hem in de belijning [...] Daar zit de poot ook
nog iets meer over de ander heen". Alleen x 27-31, y 50-54; rechtsonder de lijn wordt verre poot (schaduwtinten)."""
import numpy as np
from PIL import Image
src = Image.open('kleur/ronde6b/coathief.png'); a = np.array(src); b = a.copy()
SET = {(30, 51): 1, (29, 52): 1, (28, 53): 1, (28, 54): 1,          # de lijn (index 1 = bijna-zwart)
       (30, 52): 4, (31, 52): 2, (29, 53): 3, (30, 53): 4, (29, 54): 3, (30, 54): 4}   # verre poot onder de lijn
for (x, y), v in SET.items():
    assert a[y, x] != 0
    b[y, x] = v
o = Image.fromarray(b, 'P'); o.putpalette(src.getpalette()); o.save('kleur/ronde6c/coathief.png', transparency=0)
d = np.argwhere(a != b); print('gewijzigd', len(d), 'alpha gelijk', ((a > 0) == (b > 0)).all())
u = Image.open('silhouet/onderlaag_b1c_256.png').convert('RGBA')
W = Image.new('RGBA', (3 * 266 + 10, 266), (236, 236, 230, 255)); W.alpha_composite(u, (5, 5))
o = Image.open('kleur/ronde6c/coathief.png')
for i, im in enumerate((src, o)):
    W.alpha_composite(im.convert('RGBA').resize((256, 256), Image.NEAREST), (271 + 266 * i, 5))
W.convert('RGB').save('kleur/ronde6c/onderlaag_6b_6c.png')
z = Image.new('RGBA', (2 * 250 + 10, 200), (236, 236, 230, 255))
o = Image.open('kleur/ronde6c/coathief.png')
for i, im in enumerate((src, o)):
    z.alpha_composite(im.convert('RGBA').crop((12, 42, 37, 62)).resize((250, 200), Image.NEAREST), (260 * i, 0))
z.convert('RGB').save('kleur/ronde6c/uitsnede_6b_6c.png')
