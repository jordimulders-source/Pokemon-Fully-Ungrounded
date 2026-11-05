"""Coathief ronde 6f (Jordi over 6e, krabbel `referenties/krabbel_jordi_belijning3.png`, schaal 6,4x via het oog):
"bijna, heb nog een nieuwe lijn ter indicatie getekend, mag iets rechter qua vorm, ipv een bolling". De omlijning van
de nabije bovenarm loopt op x 31 (y 50-53) i.p.v. de bolling naar x 32; x 32 wordt de verre poot die erachter uitsteekt.
Alleen x 29-32, y 50-53; silhouet gelijk (ronde6)."""
import numpy as np
from PIL import Image
src = Image.open('kleur/ronde6e/coathief.png'); a = np.array(src); b = a.copy()
SET = {(31, 50): 1, (31, 51): 1, (31, 52): 1, (30, 53): 1,      # rechtere omlijning
       (32, 50): 2, (32, 51): 2, (32, 52): 2, (32, 53): 2,      # verre poot erachter (donker, rand)
       (30, 50): 6, (30, 51): 6}                                 # schaduw langs de lijn
for (x, y), v in SET.items():
    assert a[y, x] != 0, (x, y)
    b[y, x] = v
o = Image.fromarray(b, 'P'); o.putpalette(src.getpalette()); o.save('kleur/ronde6f/coathief.png', transparency=0)
print('gewijzigd', int((a != b).sum()), '| alpha gelijk', bool(((a > 0) == (b > 0)).all()))
o = Image.open('kleur/ronde6f/coathief.png')
u = Image.open('silhouet/onderlaag_b1c_256.png').convert('RGB').crop((60, 170, 140, 250)).resize((320, 320), Image.LANCZOS)
W = Image.new('RGB', (3 * 330, 320), (236, 236, 230)); W.paste(u, (0, 0))
for i, im in enumerate((src, o)):
    s = im.convert('RGBA').crop((15, 42, 35, 62)).resize((320, 320), Image.NEAREST)
    bg = Image.new('RGBA', s.size, (236, 236, 230, 255)); bg.alpha_composite(s); W.paste(bg.convert('RGB'), (330 * (i + 1), 0))
W.save('kleur/ronde6f/onderlaag_6e_6f_zoom.png')
V = Image.new('RGBA', (3 * 266 + 10, 266), (236, 236, 230, 255))
V.alpha_composite(Image.open('silhouet/onderlaag_b1c_256.png').convert('RGBA'), (5, 5))
V.alpha_composite(o.convert('RGBA').resize((256, 256), Image.NEAREST), (271, 5))
D = Image.new('RGBA', (256, 256), (36, 38, 52, 255)); D.alpha_composite(o.convert('RGBA').resize((256, 256), Image.NEAREST)); V.alpha_composite(D, (537, 5))
V.convert('RGB').save('kleur/ronde6f/vel_kort.png')
