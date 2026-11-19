# poten12.py (r12): voeten pixel voor pixel met de hand (vorm uit het model, modelgrid 12 46 42 64 30).
# Verre voet (links, achter): lange teen naar links + korte teen omlaag, zwarte klauwen, E/2 (een stap donkerder, geen F).
# Nabije voet (rechts, vóór, lager): 3 gespreide tenen (links, omlaag, rechts) met transparante gaten, F/E/2,
# zwarte klauwen omlaag/naar buiten. Schenen (y49-53) blijven van r11. Leest nek12.npy, schrijft poten12.npy.
import numpy as np; from PIL import Image
from geom import PAL
a = np.load('nek12.npy'); P = np.load('part.npy')
X0 = 12
VOET = {  # x12..x39
 54: ".....22222EEE21...2FEE21....",
 55: "....2EEEEEEEE21222FFEEE22...",
 56: "....12222222E2FFEEEEEEEFFE1.",
 57: "...11111111E21222EEE2222221.",
 58: "...1......1E211111FE2111111.",
 59: "..........121.1..1FE21.....1",
 60: "...........1.....1E21.......",
 61: "...........1.....1E21.......",
 62: "..................11........",
 63: "..................1.........",
}
H = '0123456789ABCDEF'
for y, rij in VOET.items():
    assert len(rij) == 28, (y, len(rij))
    for i, ch in enumerate(rij):
        x = X0 + i
        if ch == '.' and P[y, x] == 1 and a[y, x] not in (14, 15): continue   # staart blijft
        a[y, x] = 0 if ch == '.' else H.index(ch)
np.save('poten12.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('stap_poten.png', transparency=0)
