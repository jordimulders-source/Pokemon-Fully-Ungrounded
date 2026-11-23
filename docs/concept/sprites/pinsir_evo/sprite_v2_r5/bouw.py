# Pinsir-evolutie v2 r5: start = r4 B (pixelgelijk), alleen HOOFD, ARMEN en BENEN opnieuw vanuit het model.
# Draaien vanuit docs/concept/sprites/pinsir_evo/:  python3 sprite_v2_r5/bouw.py
# Elke wijziging staat als rij: zet(y, x0, "waarden"), waarden: '.' = r4 houden, 0-9 = index, E = 14 (hooglicht bruin), Y = 13 (oog).
# Plaatsen gemeten met sprite_v2_r5/meet.py + toon.py (model per spritepixel: lijnfractie en helderheid, positie = natieve cel x 64/91).
# Palet r4 (niet gewijzigd): 1 zwart, 2 lijnbruin, 3 schaduw, 4 midden, 5 licht, 14 hooglicht, 6/7/8 room, 9-12 rood, 13 oog.
import numpy as np
from PIL import Image
r4 = Image.open('sprite_v2_r4/pinsir_evo_v2_r4_B.png'); R4 = np.array(r4); A = R4.copy()
ZONE = {}   # (x,y) -> onderdeel
def zet(y, x0, s, deel):
    for i, t in enumerate(s.split()):
        if t == '.': continue
        x = x0 + i; v = {'E': 14, 'Y': 13}.get(t, None)
        v = int(t) if v is None else v
        A[y, x] = v; ZONE[(x, y)] = deel

# ---------------- 1. HOOFD (kopschild + voorhoofd/wenkbrauwen) ----------------
# Model: het schild is links licht tot aan de onderrand (r4: donkere band over de hele breedte op y19-20 = 'recht'),
# rechterhelft vanaf een schuine grens (27,16)->(22,19) in schaduw, lichte randstreep langs de rechteronderkant
# (34,18)->(32,19)->(26-28,20), onderrand rechts schuin omhoog naar de punt: (24-28,22) -> (29-32,21) -> (33-34,20).
# Voorhoofd tussen de wenkbrauwen is een lichte wig (14-19,20), (15-18,21); boze V-wenkbrauwen (13,20) en (21,20)->(19,22).
# Ogen, mond, tanden en kaken = r4 (pixelgelijk).
H = 'hoofd'
#          x: 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
# bovenrand van het schild (tussen de stekels, y13-14) is in het model donkerder (83-108) dan de middenband (130-155):
# daardoor leest het schild gewelfd. r4 had hier 5/14 (vlak verlicht = 'recht'). Stekelflanken x19 en x27 blijven licht.
# Dal tussen middelste en rechterstekel ligt in het model op y13 (r4: y12): silhouet -2 px naar het model.
zet(12, 21, "1 . 0 0", H)
zet(13, 13, "4 4 . . . 4 E 4 4 1 1 1", H)                                      # x13..24
zet(14, 13, "5 4 4 4 4 4 5 4 4 3 4 4 4 4 5 4 4", H)                            # x13..29
zet(15, 12, "5 5  5  E  E  E  5  5  4  3  4  5  5  5  5  E  4  4  4  4", H)
zet(16, 11, "4 5 5 E E E E E 5 5 5 5 5 5 5 5 4 2 2 3 4 4 4", H)                 # x11..33
zet(17, 10, "5 5 5 5 E E E 5 5 5 5 5 5 5 5 5 5 4 4 4 4 4 4 4 4", H)             # x10..34
zet(18,  9, "5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 4 4 4 4 4 4 4 4 4 5 4", H)         # x9..35
zet(19,  9, "5 5 5 5 5 5 5 5 5 5 5 5 5 2 4 4 4 4 4 4 4 4 4 5 5 3 1", H)           # x9..35 ; (12,19) los zwart weg
zet(20, 10, "5 5 5 1 5 5 5 5 5 5 2 1 . 4 4 4 5 E 5 4 3 3 2 1 1", H)             # x10..34 ; (22,20) oog blijft
zet(21, 12, "4 . . 5 E E 5 1 1 . . 3 4 4 4 4 4 1 1 1 1", H)                     # x12..32 ; ogen (13,14),(21,22) blijven
zet(22, 12, "1 Y 1 1 2 2 2 1 1 1 Y 2 1 1 1 1 1 4 3 4", H)                       # x12..31 ; balk onder het voorhoofd x16-18 lijnbruin
zet(23, 25, "4 4 4", H)                                                         # schaduw onder de rand

# ---------------- 2. ARMEN ----------------
NA = 'nabije arm'
# schouderkoepel: model x33-37 (r4 een px te ver links), hooglicht linksboven, schaduw rechtsonder, rand 2.
#          x: 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44
zet(30, 30, "3 3 2 E E 5 5 2", NA)
zet(31, 30, "3 3 2 5 E E 5 2 3", NA)
zet(32, 30, "3 3 2 5 E 5 5 5 2", NA)
zet(33, 30, "3 3 2 5 5 5 5 4 3 2 3 4 4 4", NA)
zet(34, 30, ". 3 2 4 5 5 4 4 3 2 3 4 4 4", NA)
zet(35, 30, ". 4 2 2 4 4 4 4 5 3 2 3 4", NA)
# bovenarm (achter, schaduwkant tegen de buik) + onderarm (diagonaal van elleboog (42,38) naar pols (35,41), lichte rug in het midden,
# bovenarm 4 met lichte linkerrand 5 en schaduw 3 tegen de onderarmlijn; schaduw rechtsonder, rechterrand zwart aan de schaduwkant, onderrand zwart (37-41,44)). Buikrand links blijft de r4-lijn.
zet(36, 31, "4 4 2 2 2 2 2 5 4 3 1 3 3", NA)        # x31..43
zet(37, 32, "5 4 4 4 4 3 2 5 4 3 1 3", NA)          # x32..43
zet(38, 32, "5 4 4 4 3 3 2 E E 5 3 1 3", NA)        # x32..44
zet(39, 32, "4 4 4 3 3 2 E 5 5 4 3 1 3", NA)        # x32..44
zet(40, 33, "4 4 3 2 E 5 4 4 3 3 1", NA)            # x33..43
zet(41, 33, "4 3 5 5 4 4 4 3 3 1", NA)              # x33..42
zet(42, 37, "2 4 3 3 3 1", NA)                      # x37..42 (klauwen x33-36 = r4)
zet(43, 37, "1 1 2 3 1", NA)                        # x37..41
zet(44, 37, "1 1 1 1 1", NA)                        # x37..41
zet(45, 37, "1 6 1 1 2", NA)                        # x37..41
zet(40, 39, "5", NA); zet(41, 38, "5 5", NA)       # lichte onderarm breder (model 121-139 op x37-41)
# lijf rechts/onder de arm in de schaduw (model 82-89), zodat de arm loskomt van het lijf
zet(40, 44, "3 3", NA + ' (slagschaduw)'); zet(41, 43, "3 3 3", NA + ' (slagschaduw)'); zet(42, 43, "3 3 3", NA + ' (slagschaduw)')
VA = 'verre arm'
zet(42, 10, "2 3 2 5 5 4 3 3", VA)                  # x10..17
zet(43, 13, "4 5", VA)
zet(44, 13, "3", VA)
zet(45, 12, "3", VA)

# ---------------- 3. BENEN ----------------
VB = 'verre been'   # een stap donkerder dan het nabije been; knieschijf x15-17 y51-53 met ring (16-17,50) en (18,51-53)
#          x: 15 16 17 18 19 20 21 22 23 24
zet(47, 17, "4 5 5", VB)
zet(48, 16, "4 5 5 4 4 2 6", VB)                    # (21,48) buiklijn, (22,48) buik
zet(49, 16, "4 4 3 3 4 3 2", VB)                    # (22,49) buiklijn
zet(50, 16, "2 2 4 4 3 3 2", VB)
zet(51, 15, "5 5 4 2 3 3 3 2", VB)                  # (23,51) buiklijn, (24,51) r4
zet(52, 15, "5 4 4 2 3 3 3 3 3 3", VB)
zet(53, 15, "4 4 3 2 3 3 3", VB)
zet(54, 16, "3 2 2", VB)
zet(55, 16, "2 2 4 4 4 3 3 3", VB)
zet(56, 16, "5 4 4 4 3 3 3 3", VB)
zet(57, 16, "4 4 4 3 3 3 3 3", VB)
zet(58, 16, "2 4 4 2 4 3 3 3 2", VB)                # teenlijnen (16,58),(19,58)
zet(59, 16, "6 1 7 2", VB)                          # klauw 1 = (14-16,59), klauw 2 = (18,59)+(17-19,60)
zet(60, 15, "2 1 7 6 6 1", VB)
NB = 'nabije been'  # dij licht (model ~125), heuplijn (37-41,48)->(44,50), knie-ring open linksboven, scheen licht links / schaduw rechts
#          x: 33 34 35 36 37 38 39 40 41 42 43 44 45
zet(46, 39, "2", NB)
zet(47, 34, "E 5 5 4 4 3 3 3", NB)                  # x34..41
zet(48, 34, "5 5 5 2 2 2 2 2 4 4 4", NB)            # x34..44
zet(49, 33, "2 E 5 5 5 5 5 4 3 2 2 3", NB)          # x33..44
zet(50, 33, "4 5 5 5 5 5 5 4 3 3 3 2", NB)          # x33..44
zet(51, 33, "4 5 5 5 5 5 4 2 3 3 3 2", NB)
zet(52, 34, "5 5 E E 5 5 4 2 2 3 2", NB)            # x34..44
zet(53, 35, "5 5 E 5 5 5 4 3 3 2", NB)              # x35..44
zet(54, 35, "4 5 5 5 4 4 4 3 3 2", NB)
zet(55, 34, "4 4 4 2 4 4 3 3 2 3 3 2", NB)          # x34..45
zet(56, 35, "4 5 4 2 2 2 2 3 4 3", NB)              # x35..44
zet(57, 36, "E 5 5 4 4 4 4 3 3", NB)
zet(58, 36, "5 5 4 4 4 4 4 3 3 3", NB)
zet(59, 37, "2 2 5 4 4 4 4 3 3", NB)
zet(60, 37, "7 6 2 4 4 4 3 2 3", NB)
zet(61, 35, "2 6 7 6 2 1 1 1 2 7 7", NB)
zet(62, 37, "6", NB)

# ---------------- 4. BUITEN DE OPDRACHT (zelfde blik over de hele sprite) ----------------
# Buikplaatlijnen uit het model (L 131-143 op room): horizontaal y41 x21-26 -> (27-28,40), verticaal x23 y42-46, horizontaal y47 x22-27.
BU = 'buiklijnen (buiten opdracht)'
zet(41, 21, "E E E E E E", BU); zet(40, 27, "E E", BU)
for y in range(42, 47): zet(y, 23, "E", BU)
zet(47, 22, "E E E E E E", BU)

# ---------------- 5. OPSCHONEN ----------------
# Losse 1-px-vlekjes in schaduw/midden (index 3 of 4) binnen de gewijzigde zones nemen de meest voorkomende buurtint (3/4/5/14).
# Bewust klein en blijft: lichtranden/hooglichten (5, 14), klauwen, ogen, lijnen.
from scipy import ndimage as nd
from collections import Counter as _C
OPGESCHOOND = []
for v in (3, 4):
    lab, n = nd.label(A == v)
    for i in range(1, n + 1):
        pts = np.argwhere(lab == i)
        if len(pts) != 1: continue
        y, x = pts[0]
        if (x, y) not in ZONE: continue
        bu = [int(A[y + dy, x + dx]) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy or dx) and A[y + dy, x + dx] in (3, 4, 5, 14)]
        if not bu: continue
        w = _C(bu).most_common(1)[0][0]
        if w != v: A[y, x] = w; OPGESCHOOND.append((int(x), int(y), v, w))

if __name__ == '__main__':
    print('opgeschoond (x,y,oud,nieuw):', OPGESCHOOND)
    o = Image.fromarray(A, 'P'); o.putpalette(r4.getpalette())
    o.save('sprite_v2_r5/pinsir_evo_v2_r5.png', transparency=0)
    c = Image.open('sprite_v2_r5/pinsir_evo_v2_r5.png'); assert (np.array(c) == A).all()
    d = np.argwhere(A != R4)
    buiten = [(x, y) for y, x in d if (x, y) not in ZONE]
    assert not buiten, buiten          # alles buiten de drie onderdelen pixelgelijk aan r4 B
    from collections import Counter
    print('gewijzigd per onderdeel:', Counter(ZONE[(x, y)] for y, x in d))
    print('silhouet: +', int(((A > 0) & (R4 == 0)).sum()), ' -', int(((A == 0) & (R4 > 0)).sum()),
          ' kleuren:', len(set(A.flatten())))
