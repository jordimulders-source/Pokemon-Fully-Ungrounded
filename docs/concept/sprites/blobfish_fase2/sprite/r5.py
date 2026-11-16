# r5 = r4 + MOET/MAG uit keuring_r4: buitenrand bultje (lichtkant) terug naar r3 (selout, index 9).
from PIL import Image
import numpy as np
r = Image.open('r4.png'); R = np.array(r); R3 = np.array(Image.open('r3.png'))
for x, y in [(7,41),(8,41),(6,42),(6,43),(6,44)]: R[y, x] = R3[y, x]
o = Image.fromarray(R, 'P'); o.putpalette(r.getpalette()); o.save('r5.png', transparency=0)
print('diff r4->r5:', int((R != np.array(r)).sum()), [int(R3[y,x]) for x,y in [(7,41),(8,41),(6,42),(6,43),(6,44)]])
