# Met de hand geplaatste pixels: per rij (y) segmenten (x_start, "tekens").
# Tekens -> paletindex: zie TEKENS. Later geschreven segmenten overschrijven eerdere.
import numpy as np
from PIL import Image

TEKENS = {'.':0,'W':1,'L':2,'S':3,'D':4,'o':5,'b':6,'B':7,'N':8,'n':9,'r':10,'R':11,
          'g':12,'G':13,'h':14,'K':15}
PAL = [(152,208,160),(255,255,255),(255,222,156),(222,189,131),(180,139,90),(131,90,41),
       (139,189,238),(98,156,222),(74,115,197),(82,90,148),(197,74,49),(123,32,24),
       (205,205,205),(148,148,156),(90,52,24),(16,16,16)]

R = {}
def put(y, x, s):
    R.setdefault(y, []).append((x, s))

# ---------------- nabij been + voet (linksboven) ----------------
put(2, 7, "K.K.K")
put(3, 6, "KgKgKgK")
put(4, 5, "nbbbbBBNK")
put(5, 5, "nbbBBBNNK")
put(6, 6, "nbBBBNNNK")
put(7, 7, "KNNNNNKK")
put(8, 11, "KoSSK")
put(9, 12, "KSDnnb")
put(10,12, "KKNBbbnn")
put(11,13, "KKNBbbbnn")
put(12,14, "KKNBBbbbnn")
put(13,16, "KKNBBbbbnn")
put(14,18, "KKNBBbbbnn")
put(15,20, "KKNNBBbbnn")
put(16,22, "KKNBBbbWbnn")
put(17,24, "KKNBBBbbbnn")
put(18,26, "KKNNBBBbbbnn")
put(19,28, "KKNNBBBbbbnn")
put(20,30, "KKNNBBBBbbnn")
put(21,32, "KKNNBBBBbbn")
put(22,34, "KNNNBBBbbn")

# ---------------- ver been + voet (rechtsboven) ----------------
put(3, 56, "K.K.K")
put(4, 55, "KgKgKgK")
put(5, 54, "nbbBBNNK")
put(6, 54, "nbBBBNNK")
put(7, 54, "nBBBNNK")
put(8, 54, "KKNNNK")
put(9, 54, "oSDK")
put(10,53, "oSDDK")
put(11,52, "nbBNK")
put(11,52, "nbBNNK")
put(12,52, "nbBNNK")
put(13,51, "nbBBNK")
put(14,51, "nbBBNNK")
put(15,50, "nbBBNNK")
put(16,50, "nbBBNNK")
put(17,49, "nbBBBNK")
put(18,48, "nbbBBNNK")
put(19,48, "nbBBBNNK")
put(20,47, "nbBBBNNK")
put(21,46, "nbbBBNNK")
put(22,44, "nbbBBBNNK")

def blok(x0, y0, regels):
    """Blok als tekening: ' ' = niets veranderen."""
    for i, r in enumerate(regels):
        for j, c in enumerate(r):
            if c != ' ':
                put(y0+i, x0+j, c)

# ---------------- romp (huid): schouders links, taille rechtsboven ----------------
put(25,33, "oooo")
put(26,31, "ooLLLLo")
put(27,30, "oLLLLLLSo")
put(28,29, "oLLLLLLSSSo")
put(29,28, "oLLLLLLSSSSSo")
put(30,28, "oLLLLLSSSSSSSo")
put(31,28, "oLLLLSSSSSSSSSo")
put(32,28, "oLLLSSSSSSSSSDK")
put(33,28, "oLLSSSSSSSSSDDK")
put(34,28, "oLSSSSSSSSSDDK")
put(35,28, "oSSSSSSSSSSDK")
put(36,28, "oSSSSSSSSSDDK")
put(37,28, "oSSSSSSSSDDK")
put(38,28, "oSSSSSSSDDK")
put(39,28, "oSSSSSSDDK")
put(40,28, "oSSSSDDDK")
put(41,28, "oSSDDDDK")
put(42,28, "oSSDDK")

# ---------------- heup / broek ----------------
put(23,35, "KNBBBbbbbbbBBNNK")
put(24,36, "KNBBbbbbbBBBNNK")
put(25,37, "nBBBbbbBBBBNNK")
put(26,38, "nBBBBBBBBNNK")
put(27,39, "nNBBBBBBNNK")
put(28,40, "nnNBBBNNK")
put(29,41, "nnNNNNNK")
put(30,42, "nnNNNK")
put(31,43, "nnNK")

# ---------------- vrije arm: gebogen over de buik, elleboog rechtsonder, hand op de heup ----------------
put(30,29, "ooo")
put(31,28, "oLLLo")
put(32,28, "oLLLLo")
put(33,29, "oLLLSo")
put(34,30, "oLLSSo")
put(35,31, "oLLSSo")
put(36,32, "oLSSDo")
put(37,33, "oLSSDDo")
put(38,34, "oSSSDDDK")
put(39,35, "KDDDDDK")
put(40,36, "KKKKK")
# prajiad om de bovenarm
put(32,31, "r")
put(33,31, "rR")
put(34,32, "R")
# onderarm omhoog naar de hand
put(34,40, "oSDK")
put(35,40, "oLSDK")
put(36,39, "oLSDK")
put(37,39, "oLSDK")
# ronde hand op de heup
put(28,41, "oooK")
put(29,40, "oLWLSK")
put(30,40, "oLLLSDK")
put(31,40, "oLLSSDK")
put(32,40, "oSSSDDK")
put(33,41, "oSDDK")

# ---------------- hals (achter de kaak, in de schaduw) ----------------
put(35,25, "DDSS")
put(36,25, "DDSS")
put(37,25, "DDSS")
put(38,25, "DDSS")
put(39,25, "KDDS")
put(40,25, "KKDS")
put(41,26, "KKo")

# ---------------- cordao (hangt van de tailleband omlaag) ----------------
put(32,46, "rK")
put(33,46, "rRK")
put(34,46, "rRK")
put(35,46, "rRK")
put(36,46, "rRK")
put(37,46, "rRK")
put(38,46, "rRK")
put(39,45, "KrrRK")
put(40,45, "KRrRK")
put(41,46, "KKK")

# ---------------- steunarm + hand ----------------
put(43,28, "oSSDK")
put(44,28, "rrrRKr")
put(45,28, "oSDDKR")
put(46,28, "oSDDKR")
put(47,28, "oSDK")
put(48,28, "oLSDK")
put(49,28, "oLSDK")
put(50,28, "oLSDK")
put(51,28, "oLSDK")
put(52,28, "oLSDK")
put(53,28, "oLSDK")
put(54,28, "oSSDK")
put(55,27, "ooSDDKK")
put(56,26, "oLLLSSK")
put(57,25, "oLWLSSSDK")
put(58,25, "oLLSSSSDK")
put(59,25, "oSSSSSDDK")
put(60,25, "oSSSSDDDK")
put(61,26, "KDDDDDK")
put(62,27, "KKKK")

# ---------------- kop (Hitmontop-trekken, kleinere kop) ----------------
put(29,13, "oLLLLLLLSK")
put(30,12, "oLLLLLLLLSSK")
put(31,11, "oLLLLLLLLLSSDK")
put(32,11, "oLLLLLLLLSSSDK")
put(33,11, "oLLLLLLLSSSSDDK")
put(34,11, "oLLLLLLSSSSSSDK")
put(35,11, "oLLLLLSSSSSSDDK")
put(36,12, "oLLSSSSSSSSDDK")
put(37,12, "oSSSSSSSSSDDK")
put(38,13, "oSSSSSSSSDDK")
put(39,14, "KDSSSSSDDK")
put(40,15, "KKDDDDKK")
put(41,17, "KKKK")
# ogen: Hitmontop pixel voor pixel (links 5 breed, rechts 4 breed)
put(32,15, "KK")
put(33,14, "KWKK")
put(34,13, "KKKKK")
put(35,13, "KSKK")
put(33,21, "KK")
put(34,20, "KWKK")
put(35,20, "KKKK")
put(36,21, "KK")
# mond
put(38,17, "ooo")

# ---------------- haar: Hitmontops brede puntige rand met strepen, gerestyled ----------------
# Radiale strepen van Hitmontop worden de scheidingen tussen dikke lokken; de linkerpunt valt
# als twee gedraaide lokken langs de slaap omlaag, de rechterpunt blijft kort achter het oor.
blok(4, 21, [
 "         hhhhhhKK        ",
 "      hhSDohSDDDohKK     ",
 "    hhSDDDohSDDDDohDoK   ",
 "   hSDhSDDDohSDDDDohSoK  ",
 "  hSDohSDDDohSDDDDohSDoK ",
 " hShSDohSDDDohSDDDohSDhK ",
 "hSohSDohSDDDohSDDohSohDK ",
 "hSohSDohDhoohhooohhDohDK ",
 "hSohSDoDK          DohDK ",
 "hSohSDoK            oDK  ",
 "hSohSDK              oK  ",
 "hSohSK",
 "hDohDK",
 "hoSoSK",
 "hSohDK",
 "hDoKK",
 "hoSK",
 "hSoK",
 "hDK",
 "KK",
])
# kleine hoorn (Hitmontops punt, klein, niet-functioneel)
put(17,17, "K")
put(18,16, "oSK")
put(19,16, "oSDK")

def bouw():
    a = np.zeros((64, 64), np.uint8)
    for y in sorted(R):
        for x, s in R[y]:
            for i, c in enumerate(s):
                if c != ' ':
                    a[y, x+i] = TEKENS[c]
    return a

def opslaan(pad):
    a = bouw()
    im = Image.fromarray(a, 'P')
    flat = [v for c in PAL for v in c]
    im.putpalette(flat)
    im.info['transparency'] = 0
    im.save(pad)
    return a

if __name__ == '__main__':
    import sys
    a = opslaan(sys.argv[1] if len(sys.argv) > 1 else 'sprite.png')
    inv = {v: k for k, v in TEKENS.items()}
    with open('raster.txt', 'w') as f:
        for y in range(64):
            f.write(''.join(inv[v] for v in a[y]) + '\n')
