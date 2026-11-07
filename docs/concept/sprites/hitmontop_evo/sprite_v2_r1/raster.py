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
put(9, 12, "KSDnnn")
put(10,12, "KKNBbbnn")
put(11,13, "KKNBbbbnn")
put(12,14, "KKNBBbbbnn")
put(13,16, "KKNBBbbbnn")
put(14,18, "KKNNBbbbnn")
put(15,20, "KKNBBbbbnn")
put(16,22, "KKNBBbbWnn")
put(17,23, "KKNNBBBbbnn")
put(18,25, "KKNNBBBbbnn")
put(19,27, "KKNNBBBBbnn")
put(20,29, "KKNNBBBbbnn")
put(21,31, "KKNNNBBbbnn")
put(22,32, "KKNNNBBBBbnn")

# ---------------- ver been + voet (rechtsboven) ----------------
put(3, 56, "K.K.K")
put(4, 55, "KgKgKgK")
put(5, 54, "nbbBBNNK")
put(6, 54, "nbBBBNNK")
put(7, 54, "nBBBNNK")
put(8, 54, "KKNNNK")
put(9, 54, "oSDK")
put(10,53, "oSDDK")
put(11,52, "nbBNK.")
put(12,52, "nbBBNK")
put(13,51, "nbbBNNK")
put(14,51, "nbBBNK.")
put(15,50, "nbBBNK.")
put(16,50, "nWbBNK.")
put(17,49, "nbbBNNK")
put(18,48, "nbbBBNNK")
put(19,47, "nbbBBBNK")
put(20,47, "nbBBBNNK")
put(21,46, "nbbBBNNK")
put(22,44, "nnbbBBNNK")

def blok(x0, y0, regels):
    """Blok als tekening: ' ' = niets veranderen."""
    for i, r in enumerate(regels):
        for j, c in enumerate(r):
            if c != ' ':
                put(y0+i, x0+j, c)

# ---------------- romp (huid): schouders links, taille rechtsboven; basis S, licht alleen linksboven ----------------
put(25,33, "oooo")
put(26,31, "ooLLLLo")
put(27,30, "oLLLLSSSo")
put(28,29, "oLLLSSSSSSo")
put(29,28, "oLLSSSSSSSSSo")
put(30,28, "oLSSSSSSSSSSSo")
put(31,28, "oSSSSSSSSSSSSSo")
put(32,28, "oSSSSSSSSSSSDDK")
put(33,28, "oSSSSSSSSSSDDDK")
put(34,28, "oSSSSSSSSSSDDK")
put(35,28, "oSSSSSSSSSDDDK")
put(36,28, "oSSSSSSSSDDDK")
put(37,28, "oSSSSSSSDDDK")
put(38,28, "oSSSSSSDDDK")
put(39,28, "oSSSSSDDDK")
put(40,28, "oSSSDDDDK")
put(41,28, "oSDDDDDK")
put(42,28, "oSDDDK")

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

# ---------------- vrije arm: gebogen over de borst, elleboog rechtsonder, hand op de heup ----------------
# lichter dan de romp (arm ligt ervoor), binnenlijn o, buitenrand K
put(28,29, "ooo")
put(29,28, "oLLLD")
put(30,28, "oSLLLD")
put(31,28, "oSLLLLD")
put(32,28, "oSSLLLLD")
put(33,29, "oSSLLLLD")
put(34,30, "oDSSLLLD")
put(35,31, "oDSSLLLD")
put(36,32, "oDSSLLLD")
put(37,33, "oDSSSLLD")
put(38,34, "KDDSSSSD")
put(39,35, "KDDDDDK")
put(40,36, "KKKKK")
# prajiad om de bovenarm (dwars over de arm, staartje hangt)
put(29,32, "r")
put(30,31, "rR")
put(31,30, "rR")
put(32,29, "RR")
put(33,29, "R")
# onderarm omhoog naar de hand
put(33,40, "oLLSK")
put(34,40, "oLLSK")
put(35,40, "oLLSDK")
put(36,40, "oLSSDK")
put(37,40, "oSSDK")
# ronde hand op de heup (licht op blauw)
put(27,41, "ooooK")
put(28,40, "oLLLLSK")
put(29,40, "oLWLLSDK")
put(30,40, "oLLLSSDK")
put(31,40, "oSLSSDDK")
put(32,41, "KSSDDK")

# ---------------- hals (achter de kaak, in de schaduw) ----------------
put(35,25, "DDSS")
put(36,25, "DDSS")
put(37,25, "DDSS")
put(38,25, "DDSS")
put(39,25, "KDDS")
put(40,25, "KKDS")
put(41,26, "KKo")

# ---------------- cordao (hangt van de tailleband omlaag) ----------------
put(31,47, "rK")
put(32,47, "rRK")
put(33,47, "rRK")
put(34,47, "rRK")
put(35,47, "rRK")
put(36,47, "rRK")
put(37,47, "rRK")
put(38,47, "rRK")
put(39,46, "KrrRK")
put(40,46, "KRrRK")
put(41,47, "KKK")

# ---------------- steunarm + ronde hand ----------------
put(43,28, "oLLSDK")
put(44,28, "rrrrRK")
put(45,28, "oLSDRK")
put(46,28, "oLSDRK")
put(47,28, "oLSDK")
put(48,28, "oLSDK")
put(49,28, "oSSDK")
put(50,28, "oSDDK")
put(51,28, "oLSDK")
put(52,28, "oLSK")
put(53,28, "oLSK")
put(54,28, "oSDK")
put(55,28, "oSDK")
put(56,26, "ooLLLSDK")
put(57,26, "oLWLLSDK")
put(58,26, "oLLLSSDK")
put(59,26, "oSLSSDDK")
put(60,26, "KSSSDDDK")
put(61,27, "KDDDDK")
put(62,28, "KKKK")

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
 "         hhhhhhKK",
 "      hhDoohDoooohKK",
 "    hhDooooohDooooohDoK",
 "   hDohDoooohDooooohDoK",
 "  hDoohDoooohDooooohDohK",
 " hDhDoohDoooohDoooohDohK",
 "hDohDoohDoooohDooohDohoK",
 "hDohDoohohoohhoohohDohoK",
 "hDohDoohK          hDohK",
 "hDohDooK            ohK",
 "hDohDoK              oK",
 "hDohDK",
 "hoDhoK",
 "hDohDK",
 "hoDhoK",
 "hDoKK",
 "hoDK",
 "hDoK",
 "hDK",
 "KK",
])
# rechterpunt: korte lok achter het oor (eindigt boven de hals)
put(31,25, "ohK")
put(32,25, "hoK")
put(33,26, "hK")
put(34,26, "K")
# kleine hoorn (Hitmontops punt, klein, niet-functioneel)
put(18,17, "K")
put(19,16, "oSK")
put(20,16, "oSDK")

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
