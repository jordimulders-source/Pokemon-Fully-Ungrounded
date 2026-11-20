# ontdam.py: 2x2-dambord (a b / b a) oplossen door één mauve-pixel (2-5) gelijk te maken aan zijn diagonale buur,
# zodat een van de twee diagonale lijnen een trapje wordt. Kuif, gezicht, oog, poten en lijn (1) blijven onaangeroerd.
import numpy as np; from PIL import Image
from geom import PAL
a = np.load('poten.npy'); n = 0
for ronde in range(5):
    gew = 0
    for y in range(63):
        for x in range(63):
            p, q, r, s = a[y,x], a[y,x+1], a[y+1,x], a[y+1,x+1]
            if not (p and q and p == s and q == r and p != q): continue
            # kies de pixel die het minst kapotmaakt: een mauve-pixel (2..5) die aan de kant van de donkerste tint ligt
            for (yy, xx), nieuw in (((y, x+1), p), ((y+1, x), p), ((y, x), q), ((y+1, x+1), q)):
                if a[yy, xx] in (2, 3, 4, 5) and nieuw in (2, 3, 4, 5):
                    a[yy, xx] = nieuw; gew += 1; break
            else:
              if {int(p), int(q)} & {6, 7} and {int(p), int(q)} & {1, 2}:
                # diagonale pluk van 1 px: trapje maken aan de schaduwkant (rechtsonder) met de middentint 6
                cand = [(yy, xx) for (yy, xx) in ((y, x), (y, x+1), (y+1, x), (y+1, x+1)) if a[yy, xx] in (1, 2)]
                yy, xx = max(cand, key=lambda t: t[0] + t[1]); a[yy, xx] = 6; gew += 1
              else:
                # binnen-scheidingslijn (1, niet aan de achtergrond) in staart/vleugel -> donkerste mauve
                for (yy, xx) in ((y, x), (y, x+1), (y+1, x), (y+1, x+1)):
                  if a[yy, xx] == 1 and xx > 30 and all(a[yy+dy, xx+dx] != 0 for dy, dx in ((1,0),(-1,0),(0,1),(0,-1))):
                    a[yy, xx] = 2; gew += 1; break
    n += gew
    if not gew: break
print('ontdamd', n)
np.save('ontdam.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('hoatzin.png', transparency=0)
