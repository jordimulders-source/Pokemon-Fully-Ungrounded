# kop12.py (r12): kop met de hand op het raster (vorm uit het model): blauwe vlek 7x7 (x10-16, y19-25, hoeken weg),
# rond oog 5x5 (x11-15, y20-24): zwarte ring, rood binnenin met een eigen zwart puntje (13,22);
# snavel x5-10, y22-27: bovensnavel licht grijs met haak linksonder, bekspleet 1 px zwart (y25), lichte onderkaak.
# '=' = laten staan, '.' = transparant. Leest kuif12.npy, schrijft kop12.npy.
import numpy as np; from PIL import Image
from geom import PAL
a = np.load('kuif12.npy')
X0, Y0 = 5, 19
KOP = [  # x5..x19
 "======99999====",   # 19
 "=====9911199===",   # 20
 "=====91AAA18===",   # 21
 ".1FFE91A1A18===",   # 22
 "1FFEE91AAA18===",   # 23
 "1FEEE99111988==",   # 24
 "1E11119988882==",   # 25
 "11FFEE2========",   # 26
 "..1111=========",   # 27
]
H = '0123456789ABCDEF'
for j, row in enumerate(KOP):
    for i, ch in enumerate(row):
        if ch == '=': continue
        a[Y0+j, X0+i] = 0 if ch == '.' else H.index(ch)
np.save('kop12.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('stap_kop.png', transparency=0)
