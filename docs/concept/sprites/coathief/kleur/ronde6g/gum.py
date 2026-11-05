"""Coathief ronde 6g: Jordi gumde op 6f de strook van de verre poot rechts van de bovenarm weg
(`referenties/krabbel_jordi_gum.png`, 20 schermpx per spritepixel): "heb nu onnodige pixels uitgegumd".
(32, 50-54) -> transparant; silhouet ronde7 = ronde6 min deze 5 px."""
import numpy as np
from PIL import Image
src = Image.open('kleur/ronde6f/coathief.png'); a = np.array(src); b = a.copy()
for y in range(50, 55):
    b[y, 32] = 0
o = Image.fromarray(b, 'P'); o.putpalette(src.getpalette()); o.save('kleur/ronde6g/coathief.png', transparency=0)
sil = [list(l.rstrip('\n')) for l in open('silhouet/ronde6.txt')]
for y in range(50, 55):
    sil[y][32] = '.'
open('silhouet/ronde7.txt', 'w').write('\n'.join(''.join(r) for r in sil) + '\n')
s = np.array([[c == '#' for c in ''.join(r)] for r in sil])
print('gewijzigd', int((a != b).sum()), '| silhouet', s.sum(), '| alpha-diff', int(((b > 0) != s).sum()))
