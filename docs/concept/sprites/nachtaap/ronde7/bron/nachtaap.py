"""Nachtaap fase 1, ronde 7: pixel-over van concept B, per lichaamsdeel met de hand getekend.

Elk lichaamsdeel is een eigen tekstraster (pixel voor pixel gekozen, inclusief schaduw en omlijning).
Volgorde van tekenen = van achter naar voren. Draaien vanuit de repo-root:
    python3 docs/concept/sprites/nachtaap/ronde7/bron/nachtaap.py docs/concept/sprites/nachtaap/ronde7
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Canvas, save, zoom

# Palet: violette ramp = Aipom (213,131,255 / 180,98,230 / 139,57,180 / 82,32,106) een stap dieper en iets
# naar blauw (concept B: 'dieper violet'); lila gezicht = Espeon-crème (238,222,238) naar lila;
# cyaan oog met lichte weerkaatsing en donkere onderrand. Alle waarden op GBA-stappen (veelvouden van 8, +-).
PAL = [
    (152, 208, 160),  # 0  transparant
    (180, 123, 246),  # 1  h violet hooglicht
    (148, 90, 222),   # 2  b violet basis
    (106, 57, 180),   # 3  s violet schaduw (ook omlijnings-hooglicht)
    (57, 32, 115),    # 4  o omlijningsbasis (indigo)
    (246, 238, 255),  # 5  W lila hooglicht
    (222, 205, 246),  # 6  L lila basis
    (172, 156, 222),  # 7  l lila schaduw
    (189, 255, 255),  # 8  C cyaan weerkaatsing
    (57, 213, 238),   # 9  c cyaan iris
    (16, 131, 180),   # 10 d cyaan donker (onderrand iris)
    (16, 41, 98),     # 11 P pupil
    (255, 172, 213),  # 12 R roze
    (205, 106, 164),  # 13 r roze schaduw
    (255, 255, 255),  # 14 w glans
    (16, 16, 24),     # 15 K omlijning (schaduwkant)
]
KEYS = dict(h=1, b=2, s=3, o=4, W=5, L=6, l=7, C=8, c=9, d=10, P=11, R=12, r=13, w=14, K=15)

# ---- staart (achter alles): Nazca-spiraal, groeit laag uit de stuit achter de rechterdij ----
# de buis komt dik (3 px) achter de dij vandaan, loopt over de grond naar rechts, klimt omhoog en draait
# als spiraal naar binnen; het puntje (1 px dun, taps) krult omhoog in het midden van de krul.
TAIL = (37, 33, [
    "........ssssoo....",
    "......sshhhhbbsK..",
    ".....shhbbbbbbbsK.",
    "....shbbsKKKKsbbsK",
    "....ohbsK....KsbsK",
    "....obsK..oo..KbsK",
    "....obsK.ohsK.KbsK",
    "....obsK.obsK.KbsK",
    "....obssbbbsK.KbsK",
    ".....KssssssK.KbsK",
    "......KKKKKK..KbsK",
    "..............obsK",
    ".............obbsK",
    "...........oobbssK",
    ".....sssoobbbbssK.",
    ".....bbbbbbbsssK..",
    ".....sssssssssK...",
    ".....KKKKKKKKK....",
])

# ---- verre oor (linksboven, half achter de kop) ----
EAR_FAR = (16, 21, [
    ".ss..",
    "shbo.",
    "obRo.",
    "obRr.",
    ".osK.",
    "..K..",
])

# ---- nabije oor (rechtsboven, aan de achterkant van de kop) ----
EAR_NEAR = (38, 19, [
    "..sso..",
    ".shhbo.",
    "sbRRRsK",
    "obRrrsK",
    "osRrrsK",
    ".osrsK.",
    "..KKK..",
])

# ---- romp: gebogen tarsierrug, lila buik; onder de kop slagschaduw ----
TORSO = (25, 36, [
    "...oossssssK....",
    "..osssssssssK...",
    ".obbllllllssssK.",
    "shhbWLLLLLllsssK",
    "shhbWWLLLLLlsssK",
    "sbhbWLLLLLLlsssK",
    "obbbLLLLLLLlsssK",
    "obbbLLLLLLllsssK",
    "obbbLLLLLLllsssK",
    "osbbLLLLLlllsssK",
    "osbbLLLLLlllsssK",
    "ossbLLLLllllsssK",
    "KssbllllllllsssK",
    ".KssllllllllssK.",
    "..KKssssssssKK..",
    "....KKKKKKKK....",
])

# ---- nabije been (rechts): hoge knie, scheen terug omlaag, lange voet naar links ----
LEG_NEAR = (32, 41, [
    "...sssoo...",
    ".shhhhbbo..",
    "shhhhbbbbsK",
    "shhbbbbbbsK",
    "ohbbbbbbssK",
    "obbbbbbsssK",
    "obbbbbssssK",
    "osbbbssssK.",
    "ossbsssssK.",
    ".KssssssK..",
    "..KKsssK...",
    ".oobbsK....",
    "ohhRbbbooo.",
    "obRRrbbbbsK",
    "KsRrsKsssK.",
    ".KKK..KKK..",
])

# ---- verre been (links): dij schuin naar voren, voet plat op de grond naar links ----
LEG_FAR = (14, 47, [
    ".......sssoo.",
    ".....sshhbbbo",
    "...sshbbbbbsK",
    "..shbbbbbssK.",
    ".ohbbbbsssK..",
    "oohbbsssKK...",
    "ohRRbbbbbsK..",
    "oRRrbbbbsK...",
    "KsrrssssK....",
    ".KKKKKKK.....",
])

# ---- kop (23x21): 3/4 naar links, gezichtsschijf met indigo rand, halfgesloten cyaan ogen ----
HEAD = (19, 18, [
    "........sssssooo.......",
    ".....shhhhhhbbbbboo....",
    "...sshhhhhhbbbbbbbbo...",
    "..shhhhhhhhbbbbbbbbso..",
    ".shhhhhhhbbbbbbbbbsbsK.",
    ".sbooossssooooosbbsbssK",
    "oboWWLossoWLLLLosbsbssK",
    "oboWLLLooLLLLLLosbbsssK",
    "oLlllLLLllllllLLosbsssK",
    "oLKKKlLLKKKKKKlLosbsssK",
    "oKwccKLLKwccPcKLosssssK",
    "oKcPclLLdcccPCdLosssssK",
    "oldcClLLldccCdLLosssssK",
    "oLldlLLLLlddlLLlosssssK",
    "oLLLLooLLLlllLLlosssssK",
    ".oLLLLLLLLLlllllossssK.",
    ".oLLooLLLllllllosssssK.",
    "..olLLllllllllosssssK..",
    "...KKllllllllKsssssK...",
    ".....KKKKKKKKsssssK....",
    ".............KKKKK.....",
])

# ---- onderarm: van de pols omlaag naar de schouder; loopt achter de kin langs (getekend vóór de kop) ----
FOREARM = (14, 33, [
    "..sbbsK.....",
    "..sbbbsK....",
    "...obbbsK...",
    "...osbbbsK..",
    "....KssbbbsK",
    ".....KKsssbs",
])

# ---- geheven hand tegen de wang (links): korte vingers met roze kussentjes, de middelste het langst ----
HAND = (11, 27, [
    "....ss....",
    ".ssoRRsoo.",
    "sRRoRRoRrK",
    "shbohbobsK",
    "shbbbbbbsK",
    ".obbbbbsK.",
    "..obbbsK..",
    "...obbsK..",
])

# ---- hand op de knie (rechts) ----
HAND_KNEE = (33, 40, [
    ".ss.so.",
    "ohRohRo",
    "obbbbbsK",
    ".KssssK",
])

# ---- frame 2: het ooglid zakt een rij (de blik wordt nog trager) en de spiraal veert 1 px op ----
F2_HEAD = (19, 28, [
    "oKKKKKLLlKKKKKKLosssssK",
])
ORDER = [TAIL, EAR_FAR, EAR_NEAR, TORSO, FOREARM, LEG_FAR, LEG_NEAR, HEAD, HAND, HAND_KNEE]


def frame(f=0):
    c = Canvas(KEYS)
    for part in ORDER:
        x, y, rows = part
        if f and part is TAIL:
            # spiraal (bovenste 11 rijen) 1 px omhoog; de stuit blijft liggen
            c.put(x, y - 1, rows[:11])
            c.put(x, y + 10, rows[10:12])
            c.put(x, y + 11, rows[11:])
            continue
        c.put(x, y, rows)
    if f:
        x, y, rows = F2_HEAD
        c.put(x, y, rows)
    return c


if __name__ == '__main__':
    out = sys.argv[1]
    f1 = frame(0)
    f2 = frame(1)
    print('oppervlak', f1.area())
    save([f1, f2], PAL, os.path.join(out, 'anim_front.png'), os.path.join(out, 'normal.pal'))
    if len(sys.argv) > 2:
        zoom(f1, PAL, sys.argv[2])
