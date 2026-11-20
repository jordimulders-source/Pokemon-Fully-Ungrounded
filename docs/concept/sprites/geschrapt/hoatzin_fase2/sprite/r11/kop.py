# kop.py: kop met de hand op het raster (vorm uit het model, kop.png): snavel, blauw gezicht (vlek rond het oog), rond oog 5x5
# (Sharpedo-vorm, ring donkerblauw = oog B, rode iris, zwarte pupil, glanspixel). '.' = basis laten staan, ' ' = transparant.
import numpy as np; from PIL import Image
from geom import PAL
a = np.load('basis.npy')
X0, Y0 = 5, 19
KOP = [  # x5..x17; oog 4x4 (x11-14, y20-23) in een blauwe vlek 7x7, snavel x5-11 (model kop40)
 "......9999...",  # 19
 "......91199..",  # 20
 "..1FF91AA199.",  # 21
 ".1FFE91A1198.",  # 22
 ".1FEE9911998.",  # 23
 "1FEEEE999998.",  # 24
 "1EE222288888.",  # 25
 "1E22EE21.....",  # 26
 " 111111......",  # 27
]
H = '0123456789ABCDEF'
for j, row in enumerate(KOP):
    for i, ch in enumerate(row):
        if ch == '.': continue
        a[Y0+j, X0+i] = 0 if ch == ' ' else H.index(ch)
np.save('kop.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('hoatzin.png', transparency=0)
