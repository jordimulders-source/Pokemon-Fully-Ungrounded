# staart12.py (r12): staart rustiger: 3 veren als lange vlakken (3) met één donkere scheidingslijn (2) ertussen,
# schuin langs de staartas (model: van onder de vleugel naar rechtsonder); bovenin (onder vleugel/buik) schaduw 2;
# omlijning opnieuw: 1 rechts/onder, selout 2 links. Leest poten12.npy, schrijft staart12.npy.
import numpy as np; from PIL import Image
from geom import PAL
a = np.load('poten12.npy'); P = np.load('part.npy')
st = (P == 1) & (a != 0)
st[:44] = False
# staartpixels zonder buitenrand opnieuw kleuren
bg = a == 0
def rand(y, x):
    return any(0 <= y+dy < 64 and 0 <= x+dx < 64 and bg[y+dy, x+dx] for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)))
# as van de staart: van (39,44) naar (50,63); u = afstand dwars op de as
ax, ay = 11.0, 19.0; n = np.hypot(ax, ay); ux, uy = ay/n, -ax/n     # dwarsrichting (naar rechtsboven)
for y, x in zip(*np.nonzero(st)):
    if rand(y, x): continue
    u = (x - 39) * ux + (y - 44) * uy
    c = 3
    if abs(u - 2.6) < 0.5 or abs(u + 1.4) < 0.5: c = 2          # twee scheidingen -> drie veren
    if y < 48 and a[y, x] != 1: c = 2 if (u > -1 or y < 46) else c   # schaduw onder de vleugel
    a[y, x] = c
for y, x in zip(*np.nonzero(st)):
    if not rand(y, x): continue
    lb = (0 <= x-1 and bg[y, x-1]) and not (y+1 < 64 and bg[y+1, x])
    a[y, x] = 2 if lb else 1
# sikkelschaduw: binnenste pixel tegen de rechterrand en de onderste punt donker (2)
for y, x in zip(*np.nonzero(st)):
    if a[y, x] == 3 and x+2 < 64 and a[y, x+1] == 1 and bg[y, x+2] and y >= 48:
        a[y, x] = 2
np.save('staart12.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('stap_staart.png', transparency=0)
