"""Project Grounded: back sprites voor Archie en Maxie (Battle Stadium-doubles), getekend op de pose van Steven's back.
Per frame: haar (index 9/A/B boven de nek) wordt bandana + zwart haar (Archie) of glad rood haar (Maxie), het pak krijgt
de kleuren van het personage, Archie krijgt baard en bandanaknoop, Maxie een bril. Gebruik: python3 tools/grounded/archie_maxie_backs.py [preview.png]"""
import sys
from PIL import Image

SRC = 'graphics/trainers/back_pics/steven.png'
HAIR = {9, 10, 11}
SKIN = {1, 2, 3, 4}

PALS = {
    'archie': [(115, 197, 164), (238, 190, 150), (206, 150, 110), (166, 110, 80), (106, 70, 54),
               (232, 240, 255), (150, 196, 238), (64, 76, 128), (34, 40, 74), (126, 178, 236),
               (66, 118, 206), (40, 74, 150), (70, 62, 70), (36, 30, 38), (255, 255, 255), (12, 12, 28)],
    'maxie': [(115, 197, 164), (255, 222, 205), (222, 180, 148), (189, 148, 115), (123, 90, 82),
              (90, 90, 100), (60, 60, 70), (206, 52, 60), (128, 26, 40), (246, 124, 108),
              (210, 62, 58), (146, 34, 44), (230, 230, 240), (40, 40, 48), (255, 255, 255), (16, 10, 14)],
}


KNOT = [  # bandanaknoop met twee slippen, linksboven = (KX, KY) t.o.v. het oog
    '...FFF.....',
    '..FA99F....',
    '.FAAAAAF...',
    'FBAAAAABF..',
    'FBBAAABBF..',
    '.FBBFBBAF..',
    '.FABFFBAAF.',
    'FAABF.FBAF.',
    'FABF..FBBF.',
    'FBBF...FBF.',
    '.FF.....F..',
]
KX, KY = -33, -9
# Maxie: haarpunten die in de nek naar buiten krullen (links = achterkant)
FLICK = [
    '.....FF',
    '...FFAF',
    '.FFAABF',
    'FBABBF.',
    '.FFFF..',
]


def frame_edit(px, fy, who):
    """Tekent het hoofd opnieuw rond het oog (index 14) van dit frame."""
    eye = [(x, y) for y in range(fy, fy + 40) for x in range(64) if px[x, y] == 14]
    if not eye:
        return
    ax, ay = min(eye, key=lambda p: (p[1], p[0]))
    cx, cy = ax - 12, ay - 7
    rx, ry = (17.0, 12.0) if who == 'archie' else (15.0, 11.5)

    def inell(x, y):
        return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0

    orig = {(x, y): px[x, y] for y in range(fy, fy + 64) for x in range(64)}

    def is_face(x, y):
        return orig[(x, y)] in SKIN | {14, 15} and x >= ax - 6 and y >= ay - 6
    # oud haar (en zijn omlijning) weg, ook de lok vóór het gezicht
    for y in range(fy, min(ay + 4, fy + 64)):
        for x in range(64):
            c = orig[(x, y)]
            if c in HAIR or (c == 7 and (y < ay - 1 or x > ax + 2)):
                px[x, y] = 0
    for y in range(fy, fy + 64):
        for x in range(64):
            if not inell(x, y) or is_face(x, y):
                continue
            c = orig[(x, y)]
            if y >= ay + 1 and c not in HAIR | {0}:
                continue  # niet over het lichaam/de kraag
            if x > ax + 3 and y > ay - 6:
                continue  # niet vóór het gezicht
            edge = any(not inell(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            relx = (x - (cx - rx)) / (2 * rx)
            rely = (y - (cy - ry)) / (2 * ry)
            if edge:
                px[x, y] = 15
                continue
            if who == 'archie':
                band = (ay - 7) + (ax - 4 - x) * 0.25   # onderrand bandana: achter lager
                if y < band:
                    if y >= band - 1:
                        px[x, y] = 11
                    elif rely < 0.2 and 0.1 < relx < 0.7:
                        px[x, y] = 9
                    elif relx > 0.85 or y > band - 3:
                        px[x, y] = 11 if (relx > 0.85 or x % 3) else 10
                    else:
                        px[x, y] = 10
                else:
                    # zwart haar: effen, met een paar strengen
                    px[x, y] = 12 if (x % 5 == 1 and y < band + 3) else 13
            else:
                if rely < 0.2 and 0.15 < relx < 0.8:
                    px[x, y] = 9
                elif rely < 0.3 and 0.25 < relx < 0.6 and (x + y) % 2 == 0:
                    px[x, y] = 9
                elif relx > 0.9 or rely > 0.82:
                    px[x, y] = 11
                elif rely > 0.6 and relx < 0.45:
                    px[x, y] = 11 if (x + 2 * y) % 6 == 0 else 10
                else:
                    px[x, y] = 10
    # losse pixels (oude omlijning die nergens meer aan vastzit) weg
    for _ in range(2):
        for y in range(fy, fy + 40):
            for x in range(1, 63):
                if px[x, y] in (7, 15) and sum(px[x + dx, y + dy] not in (0, 7, 15) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) == 0:
                    px[x, y] = 0
    face = [(x, y) for (x, y), c in orig.items() if is_face(x, y) and c in SKIN]
    if who == 'archie':
        fy1 = max(y for x, y in face)
        fx0 = min(x for x, y in face)
        # volle zwarte baard: kaak, kin en bakkebaard; wang blijft huid
        for x, y in face:
            if y >= ay + 1 or (x <= fx0 + 2 and y >= ay - 3):
                px[x, y] = 12 if (x + y) % 4 == 0 and orig[(x, y)] in (1, 2) else 13
        for j, row in enumerate(KNOT):
            for i, ch in enumerate(row):
                if ch != '.':
                    x, y = ax + KX + i, ay + KY + j
                    if 0 <= x < 64 and (ch != 'F' or px[x, y] in (0, 15, 13, 12)):
                        px[x, y] = {'F': 15, 'A': 10, 'B': 11, '9': 9}[ch]
    else:
        for j, row in enumerate(FLICK):
            for i, ch in enumerate(row):
                if ch != '.':
                    x, y = int(cx - rx) - 3 + i, ay + 1 + j
                    if 0 <= x < 64 and (ch != 'F' or px[x, y] == 0):
                        px[x, y] = {'F': 15, 'A': 10, 'B': 11}[ch]
        # bril: montuur van het oog naar het oor, glas vóór het oog
        for x in range(ax - 7, ax):
            if px[x, ay - 1] not in (0,):
                px[x, ay - 1] = 13
        for d in (-1, 0, 1, 2):
            px[ax + 2, ay + d] = 12 if d in (0, 1) else 13
        px[ax + 1, ay - 1] = 13
        px[ax + 1, ay + 2] = 13


def make(who):
    im = Image.open(SRC)
    im = im.copy(); px = im.load()
    h = im.size[1]
    for f in range(h // 64):
        frame_edit(px, f * 64, who)
    pal = []
    for c in PALS[who]:
        pal += list(c)
    im.putpalette(pal + [0] * (768 - len(pal)))
    return im


if __name__ == '__main__':
    out = {}
    for who in ('archie', 'maxie'):
        out[who] = make(who)
        out[who].save('graphics/trainers/back_pics/%s.png' % who)
    if len(sys.argv) > 1:
        W = Image.new('RGB', (64 * 4 * 4, 64 * 4 * 2), (200, 200, 200))
        for r, who in enumerate(('archie', 'maxie')):
            im = out[who].convert('RGBA')
            for f in range(4):
                fr = im.crop((0, f * 64, 64, f * 64 + 64))
                al = Image.new('RGBA', fr.size, (200, 200, 200, 255))
                px = out[who].load()
                for y in range(64):
                    for x in range(64):
                        if px[x, f * 64 + y] != 0:
                            al.putpixel((x, y), fr.getpixel((x, y)))
                W.paste(al.resize((256, 256), Image.NEAREST), (f * 256, r * 256))
        W.save(sys.argv[1])
