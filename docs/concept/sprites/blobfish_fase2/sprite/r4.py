# r4 = r3 + keurderreparaties (keuring_r3/KEURING.md), per pixel uit model/reductie, geen tekenwerk.
from PIL import Image
import numpy as np
r = Image.open('r3.png'); R = np.array(r); K = np.array(Image.open('kaal.png'))
for x, y in [(49,36),(50,37),(50,38)]: R[y, x] = 1                      # MOET: model zwart
for x, y in [(2,58),(3,59),(10,59),(11,60),(12,60),(13,61)]: R[y, x] = 1  # MAG: schaduwkant zwart
R[29, 14] = K[29, 14]                                                     # MAG: oog terug naar reductie
R[41:46, 6:9] = K[41:46, 6:9]                                             # MAG: bultje terug naar reductie
o = Image.fromarray(R, 'P'); o.putpalette(r.getpalette()); o.save('r4.png', transparency=0)
print('diff r3->r4:', int((R != np.array(r)).sum()), 'px; silhouet gelijk:', bool(((R>0)==(np.array(r)>0)).all()))
