# kop13.py (r13): alleen de kop, de rest blijft r12 (pixeldiff 0 buiten x4-19, y16-28).
# Gemeten op het model (modelgrid 2 14 22 30 40): blauwe vlek x10.0-16.0 × y19.5-25.5 (6x6), oog (ring+iris)
# x11.5-13.75 × y20.6-23.75 (±2.5x3), snavel zichtbaar x6.4-10 × y22-27.5 (haakpunt 7.1,27.3), bekspleet y25.5 x7.8-10.
# Oog 3x3 (x11-13, y21-23) zonder zwarte ring, direct in het blauw; rand alleen donkerblauw (8) waar nodig.
# Kruin: donkere ronde massa (2) met een bruine boog (6) linksboven; alleen de veerbases (7/6) in de bovenste rij.
# Gebruik: python3 kop13.py [oogvariant]  ('.' = transparant, '=' = r12 laten staan)
import sys, numpy as np; from PIL import Image
from geom import PAL
a = np.array(Image.open('../r12/hoatzin.png')).astype(int)
X0, Y0 = 4, 16
KOP = [  # x4..x19
 "===227672762727=",   # 16 veerbases F1 F2 F3 F4 F5 in de bovenrij van de kruin
 "===26622222222==",   # 17
 "===262222222====",   # 18
 "..26622222222===",   # 19
 "..26622999922===",   # 20  x11-14
 "..26229000982===",   # 21  x10-15, rand 8 rechts  (oog x11-13 wordt hieronder gezet)
 "...2FF9000982===",   # 22
 "..2FFE9000982===",   # 23
 ".1FEEE99988833==",   # 24
 ".1EE1118888333==",   # 25
 ".1E2FEE23=======",   # 26
 "..121111========",   # 27
 "...1============",   # 28
]
OOG = {  # x11-13, y21-23
 'A': ["FAA", "A1A", "AA8"],     # glans linksboven (licht), pupil midden, schaduwhoek rechtsonder donkerblauw
 'B': ["8FA", "1AA", "AA8"],     # pupil iets naar voren (naar de snavel)
 'C': ["AFA", "A1A", "8A8"],     # onderhoeken donkerblauw
}
H = '0123456789ABCDEF'
for j, row in enumerate(KOP):
    assert len(row) == 16, (j, len(row))
    for i, ch in enumerate(row):
        if ch == '=': continue
        a[Y0+j, X0+i] = 0 if ch == '.' else H.index(ch)
v = sys.argv[1] if len(sys.argv) > 1 else 'A'
for j, row in enumerate(OOG[v]):
    for i, ch in enumerate(row): a[21+j, 11+i] = H.index(ch)
np.save('r13.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('hoatzin.png', transparency=0)
