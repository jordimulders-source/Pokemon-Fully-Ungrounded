# Pinsir-evolutie v2 r6 = r5 + (1) palet naar de modeltinten (palet.py), (2) rug B zonder banding: elke rugplaat een bolle vorm.
# Draaien vanuit docs/concept/sprites/pinsir_evo/:  python3 sprite_v2_r6/bouw.py
import sys; sys.path.insert(0, 'sprite_v2_r6'); sys.path.insert(0, 'sprite_v2_r5')
import numpy as np
from PIL import Image
from scipy import ndimage as nd
from palet import lijst
R5 = np.array(Image.open('sprite_v2_r5/pinsir_evo_v2_r5.png')); A = R5.copy()
ZONE = {}
def zet(y, x0, s, deel):
    for i, t in enumerate(s.split()):
        if t == '.': continue
        x = x0 + i; A[y, x] = {'E': 14, 'Y': 13}.get(t) or int(t); ZONE[(x, y)] = deel

# ---------------- 2. RUG ----------------
# Rugzone: rug van r4 B (x34-57, y18-46) zonder schouderkoepel/arm (r5-zones), zonder stekels en rugrand (pixels binnen 2 px van transparant),
# zonder dij/staart (y >= 42 links van x 46 hoort bij heup/dij). Naden (1/2) blijven op hun plek; alleen de vultinten 3/4/5/14 worden opnieuw verdeeld.
import bouw as r5bouw   # r5-zones (hoofd/arm/benen) ophalen; bouw.py van r5 schrijft niets bij import
ARM = np.zeros((64, 64), bool)
for (x, y), d in r5bouw.ZONE.items():
    if 'arm' in d: ARM[y, x] = True
ARM = nd.binary_dilation(ARM, np.ones((3, 3)))
RUG = np.zeros((64, 64), bool); RUG[18:46, 34:58] = True
RUG &= ~ARM
RUG[42:, :46] = False
RUG &= ~nd.binary_dilation(R5 == 0, np.ones((5, 5)))
VUL = np.isin(R5, (3, 4, 5, 14)) & RUG
# alleen voor het indelen in platen: de twee lange naden doorgetrokken tot de rand van de rugzone (geen pixelwijziging)
SCHEID = np.zeros((64, 64), bool)
for x, y in [(37,27),(36,28),(53,37),(54,38),(55,39), (42,34),(41,33),(56,43),(57,44)]: SCHEID[y, x] = True
lab, n = nd.label(VUL & ~SCHEID)
PLATEN = []
for i in range(1, n + 1):
    pts = np.argwhere(lab == i)
    if len(pts) < 8: continue
    ys, xs = pts[:, 0].astype(float), pts[:, 1].astype(float)
    # positie in de plaat: t langs (1,1) (0 = linksboven, 1 = rechtsonder), u dwars (0 = bovenkant, 1 = onderkant van de strook)
    t = xs + ys; t = (t - t.min()) / max(1, t.max() - t.min())
    u = ys - xs; u = (u - u.min()) / max(1, u.max() - u.min())
    s = 0.85 * t + 0.15 * u                      # licht vlak linksboven, schaduw rechtsonder
    q = np.argsort(np.argsort(s)) / max(1, len(s) - 1)
    nieuw = np.where(q < 0.28, 5, np.where(q > 0.72, 3, 4))
    if len(pts) >= 20:                           # grote plaat: hooglicht 2-3 px in de linkerbovenhoek
        nieuw[np.argsort(s)[:max(2, len(pts) // 25)]] = 14
    for (y, x), v in zip(pts, nieuw):
        A[y, x] = v; ZONE[(x, y)] = 'rug'
    PLATEN.append((i, len(pts), (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))))

# ---------------- verre scheen ----------------
# r5 maakte het verre been een stap donkerder; de scheen kwam daarmee 16 onder het model (helderheid.md). Midden 3 -> 4, rechterrand x23 blijft 3.
zet(55, 20, "4 4", 'verre scheen'); zet(56, 20, "4 4", 'verre scheen'); zet(57, 19, "4 4", 'verre scheen')

if __name__ == '__main__':
    o = Image.fromarray(A, 'P'); o.putpalette(lijst()); o.save('sprite_v2_r6/pinsir_evo_v2_r6.png', transparency=0)
    c = Image.open('sprite_v2_r6/pinsir_evo_v2_r6.png'); assert (np.array(c) == A).all()
    d = np.argwhere(A != R5); assert all((x, y) in ZONE for y, x in d)
    print('platen:', len(PLATEN), PLATEN); print('gewijzigd:', len(d))
