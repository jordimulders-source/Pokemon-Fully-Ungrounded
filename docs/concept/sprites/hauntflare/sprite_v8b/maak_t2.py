"""Kandidaat T2: T, alleen herkleurd: de 2x5 zwarte balk in de linker mondhoek wordt een 1-px mondlijn die schuin
naar de hoek loopt (zoals v7/C3 en Haunter G3): (20,33),(20-21,34),(21,35),(21,36),(22,37),(23,38).
Binnenste kolom -> binnenkant (donker 10 / tong 5), buitenste overbodige lijnpixels -> hoofdroze 7.
Hoektandje (22,34) blijft (v7), zijn tweede (gedupliceerde) rij (22,35) wordt binnenkant.
Rechter mondhoek is al een 1-px lijn: ongewijzigd."""
from PIL import Image
import numpy as np, os
H = os.path.dirname(os.path.abspath(__file__))
W = {(20, 35): 7, (22, 35): 10, (23, 35): 10,   # rij 35: alleen (21,35) blijft lijn
     (22, 36): 5,                               # rij 36: (21,36) lijn, rest tong
     (21, 37): 7,                               # rij 37: lijn schuift naar (22,37)
     (21, 38): 7}                               # rij 38: lijn op (23,38)
im = Image.open(os.path.join(H, 'kandidaat_T.png')); a = np.array(im)
for (x, y), c in W.items(): a[y, x] = c
o = Image.fromarray(a, 'P'); o.putpalette(im.getpalette()); o.save(os.path.join(H, 'kandidaat_T2.png'), transparency=0)
print('ok')
