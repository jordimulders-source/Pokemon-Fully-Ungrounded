"""Coathief ronde 8b (Jordi op overtrekvel r8, `referenties/krabbel_jordi_overtrek2.png`): "je hebt het een beetje
aangepast waardoor dit weg kan, rood omcirkelde 3 pixels" -> (32, 54-56) weg; x 31 wordt daar de omlijning (1),
x 30 de schaduwkant (2), zoals op y 57-58. Silhouet ronde 10 = ronde 9 min deze 3 px."""
import numpy as np
from PIL import Image
src = Image.open('kleur/ronde8/coathief.png'); a = np.array(src); b = a.copy()
for y in (54, 55, 56):
    b[y, 32] = 0; b[y, 31] = 1; b[y, 30] = 2
o = Image.fromarray(b, 'P'); o.putpalette(src.getpalette()); o.save('kleur/ronde8b/coathief.png', transparency=0)
sil = [list(l.rstrip('\n')) for l in open('silhouet/ronde9.txt')]
for y in (54, 55, 56):
    sil[y][32] = '.'
open('silhouet/ronde10.txt', 'w').write('\n'.join(''.join(r) for r in sil) + '\n')
s = np.array([[c == '#' for c in ''.join(r)] for r in sil])
print('gewijzigd', int((a != b).sum()), '| silhouet', s.sum(), '| alpha-diff', int(((b > 0) != s).sum()))
