# r6: reparaties op r5_80b volgens keuring_r5_80b (MOET 1-6 + KAN). Alleen benoemde pixels; elke waarde gemeten op
# paneel_varianten/panelen_80b.png (raster X0=103, Y0=143, s=12.703125, TOP=7, zie cfg.py). Draaien vanuit sprite/:
#   python3 r6/repareer.py
import numpy as np
from PIL import Image

# (x, y): index   -- paletindices van r5_80b
FIX = {}
def zet(lijst, v, punt):
    for xy in lijst:
        FIX[xy] = (v, punt)

# 1. lijfrand tussen middelste en rechter gewricht: model heeft de donkere lijn diagonaal op
#    (32,17) (33,16) (34,17) (35,17) (36,17) (37,18); links: (26,16).
zet([(32,17), (33,16), (34,17), (35,17), (36,17), (37,18), (26,16)], 1, 1)
# 2. onderrand groot paneel: zwarte lijn onder de frame-pixels die de achtergrond raakten (model: lijn onder het frame).
zet([(30,50), (32,51), (37,53), (39,54)], 1, 2)
# 3. rechterrand groot paneel: hele buitenrand index 1 (model: donkerste lijn aan de buitenkant).
zet([(62,15), (62,16), (60,20), (60,21), (59,22), (59,23), (57,26), (57,27), (56,28), (56,29), (55,30), (55,31),
     (53,34), (52,36), (49,42), (46,47), (44,51), (43,53), (41,54), (42,54)], 1, 3)
# 4. lichte randlijn linkerkant linker paneel doorlopend (model: rand a/b op de tweede pixel).
zet([(9,27), (8,29), (6,32), (3,38), (2,39)], 11, 4)
# 5. omlijning bij overlap: navy paneel / lijfrand, en onderlijf / paneelrand (lijn op de modelpositie,
#    rij 44 op x=30 zoals het model; rand b erachter waar het model die heeft).
zet([(17,22), (33,40), (32,41), (32,42), (31,43), (30,44), (30,45)], 1, 5)
zet([(33,41), (31,44)], 11, 5)
# 6. rechter antennebolletje 3x3 (model x48-50, y9-11; licht linksboven, donker rechtsonder), stengel onder dicht.
FIX.update({(48,9): (6,6), (49,9): (6,6), (50,9): (7,6),
            (48,10): (7,6), (49,10): (6,6), (50,10): (8,6),
            (47,11): (8,6), (48,11): (7,6), (49,11): (8,6)})
# KAN: losse pixels -> buurtint die het model bevestigt; banding-lijn index 3 -> 2 (model: 2 > 4 > 3).
FIX.update({(14,26): (9,'K'), (11,30): (11,'K'), (14,40): (1,'K'), (21,43): (8,'K'), (12,33): (3,'K')})
zet([(21,21), (20,22), (19,23), (18,24)], 2, 'K')

def repareer(src, dst):
    im = Image.open(src)
    a = np.array(im)
    for (x, y), (v, _) in FIX.items():
        a[y, x] = v
    out = Image.fromarray(a, 'P')
    out.putpalette(im.getpalette())
    out.info['transparency'] = 0
    out.save(dst, transparency=0)
    return a

if __name__ == '__main__':
    repareer('r5_80b/sprite.png', 'r6/sprite.png')
    repareer('r5_80b/oog_b.png', 'r6/oog_b.png')
    print(len(FIX), 'pixels gezet')
