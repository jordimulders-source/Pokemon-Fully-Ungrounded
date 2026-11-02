"""Coathief ronde 7b: de reparaties uit de verse eindkeuring (`kleur/ronde7/EINDKEURING.md`), alleen kleur.
R1/R2 open randen (index 6 naast transparant) -> 1; R3 glans aan de buitenrand van de staande klauwen -> crème;
R4 hangende klauwen als haak i.p.v. spijker: de kleuroplossing van de keurder (silhouet blijft ronde8)."""
import numpy as np
from PIL import Image
src = Image.open('kleur/ronde7/coathief.png'); a = np.array(src); b = a.copy()
SET = {(32, 47): 1, (33, 47): 1, (43, 51): 1, (44, 51): 1,   # R1, R2
       (25, 59): 0xB, (25, 61): 0xB,                          # R3
       (16, 59): 0xF, (20, 59): 0xA}                          # R4 (kleur)
for (x, y), v in SET.items():
    b[y, x] = v
o = Image.fromarray(b, 'P'); o.putpalette(src.getpalette()); o.save('kleur/ronde7b/coathief.png', transparency=0)
sil = np.array([[c == '#' for c in l.rstrip()] for l in open('silhouet/ronde8.txt')])
print('gewijzigd', int((a != b).sum()), '| alpha-diff', int(((b > 0) != sil).sum()))
o = Image.open('kleur/ronde7b/coathief.png')
W = Image.new('RGBA', (4 * 266 + 10, 340), (236, 236, 230, 255))
W.alpha_composite(Image.open('silhouet/onderlaag_b1c_256.png').convert('RGBA'), (5, 5))
W.alpha_composite(Image.open('../olinguito_v2/af/olinguito.png').convert('RGBA').resize((256, 256), Image.NEAREST), (271, 5))
W.alpha_composite(o.convert('RGBA').resize((256, 256), Image.NEAREST), (537, 5))
D = Image.new('RGBA', (256, 256), (36, 38, 52, 255)); D.alpha_composite(o.convert('RGBA').resize((256, 256), Image.NEAREST)); W.alpha_composite(D, (803, 5))
for i, bgc in enumerate(((236, 236, 230, 255), (36, 38, 52, 255))):
    s = Image.new('RGBA', (64, 64), bgc); s.alpha_composite(o.convert('RGBA')); W.alpha_composite(s, (537 + 266 * i + 96, 270))
W.convert('RGB').save('kleur/ronde7b/vel_jordi.png')
