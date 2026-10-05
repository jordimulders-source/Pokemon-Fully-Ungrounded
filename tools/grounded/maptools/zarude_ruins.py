"""Project Grounded: vervallen stenen ruine voor de Zarude-open plek in Fortree Jungle (gebruikt door fortree_jungle.py).

Alles is getekend (procedureel) in General-palet 3: grijze steen (1-5), donkere omlijning (8) en mintgroen mos (6, 7, 15).
Zo is er geen eigen palet nodig (fortree_jungle heeft er geen meer vrij). Stukken (Canvas, veelvouden van 16 px):
- dais(): stenen plateau van 3x2 (bovenvlak met platen en mos, voorkant met blokken) waar Zarude op landt.
- pillar(broken): zuil van 1x2 (kapiteel boven, voet onder) met klimop; broken = afgebroken, kortere zuil.
- fallen(): omgevallen zuil van 2x1.
- block(variant): losse bemoste steenblok van 1x1.
- paving(variant): oude vloerplaten met gras ertussen (begaanbaar, 1x1).
- claws(): drie klauwkrassen in een steen (1x1) voor het waarschuwingsplekje.
Gebruik los: python3 tools/grounded/maptools/zarude_ruins.py voorbeeld.png"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jungle_tileset as J

PAL = 3
LIGHT, STONE, SHADE, DARK, OUT = 2, 3, 4, 5, 8
MOSS_D, MOSS, MOSS_L = 6, 15, 7
rng = random.Random(893)


def _stone_rect(cv, x0, y0, x1, y1, seed, mortar=True):
    """Gevulde steenmassa met lichte bovenrand, schaduw onder/rechts en hier en daar een voeg."""
    rr = random.Random(seed)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c = STONE
            if y == y0 or x == x0:
                c = LIGHT
            elif y == y1 or x == x1:
                c = DARK
            elif rr.random() < 0.10:
                c = SHADE
            cv.p[y][x] = c
    if mortar:
        for y in range(y0 + 5, y1, 6):
            for x in range(x0 + 1, x1):
                cv.p[y][x] = SHADE
            off = x0 + 3 + (y * 5) % 7
            for yy in range(y - 5, y):
                if y0 < yy < y1 and x0 < off < x1:
                    cv.p[yy][off] = SHADE


def _moss(cv, n, seed, region=None):
    rr = random.Random(seed)
    x0, y0, x1, y1 = region or (0, 0, cv.w - 1, cv.h - 1)
    for _ in range(n):
        cx, cy = rr.randint(x0, x1), rr.randint(y0, y1)
        r = rr.choice((1, 1, 2))
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r - 1, cx + r + 2):
                if 0 <= x < cv.w and 0 <= y < cv.h and cv.p[y][x] not in (0, OUT):
                    d = abs(x - cx) + abs(y - cy)
                    if d <= r + 1:
                        cv.p[y][x] = MOSS_L if (d == 0 and y < cy + 1) else (MOSS if d <= r else MOSS_D)


def _ivy(cv, x, y0, y1, seed):
    """Klimop die langs een zuil naar beneden hangt (stengel donker mos, blaadjes mint)."""
    rr = random.Random(seed)
    for y in range(y0, y1):
        xx = x + int(round(math.sin(y * 0.7 + seed)))
        if 0 <= xx < cv.w and cv.p[y][xx]:
            cv.p[y][xx] = MOSS_D
            if (y + seed) % 3 == 0:
                for dx in (-1, 1):
                    if 0 <= xx + dx < cv.w and cv.p[y][xx + dx] and rr.random() < 0.8:
                        cv.p[y][xx + dx] = MOSS


def _outline(cv):
    J.grow(cv, OUT)


def dais():
    cv = J.Canvas(48, 32)
    # bovenvlak (platen)
    for i in range(3):
        _stone_rect(cv, 2 + i * 15, 4, 2 + i * 15 + 14, 19, 10 + i, mortar=False)
    for x in range(2, 46):
        cv.p[11][x] = SHADE if x % 9 else STONE
    # voorkant: donkerdere blokken, met in het midden drie treden
    _stone_rect(cv, 2, 20, 45, 30, 20)
    for y in range(20, 31):
        for x in range(2, 46):
            if cv.p[y][x] == STONE:
                cv.p[y][x] = SHADE
            elif cv.p[y][x] == LIGHT and y > 20:
                cv.p[y][x] = STONE
    for k, y in enumerate((22, 25, 28)):
        for x in range(18 - k * 2, 30 + k * 2):
            cv.p[y][x] = LIGHT
            cv.p[y + 1][x] = STONE
            cv.p[y + 2][x] = DARK
    # klauwkrassen in het bovenvlak (Zarude's plek)
    for k in range(3):
        for i in range(7):
            x, y = 20 + k * 3 + i // 2, 6 + i
            cv.p[y][x] = DARK
    # scheuren
    for x, y in ((8, 7), (9, 8), (9, 9), (10, 10), (38, 14), (39, 15), (39, 16)):
        cv.p[y][x] = DARK
    _moss(cv, 9, 31, (2, 4, 45, 30))
    _outline(cv)
    return cv


def pillar(broken):
    cv = J.Canvas(16, 32)
    top = 10 if broken else 3
    _stone_rect(cv, 4, top + 3, 11, 29, 40 + broken)
    if broken:                                      # afgebroken, scheve breukrand
        for x, dy in zip(range(4, 12), (0, 1, 2, 1, 3, 2, 1, 0)):
            for y in range(top + 3, top + 3 + dy):
                cv.p[y][x] = 0
    else:                                           # kapiteel
        _stone_rect(cv, 2, top, 13, top + 3, 42, mortar=False)
    for x in range(3, 13):                          # voet
        cv.p[29][x] = DARK
        cv.p[28][x] = SHADE if cv.p[28][x] else 0
    for y in range(top + 5, 28, 4):                 # cannelures
        cv.p[y][7] = SHADE
        cv.p[y + 1][8] = SHADE
    _ivy(cv, 5, top + 2, 27, 3)
    _ivy(cv, 10, top + 6, 24, 7)
    _moss(cv, 3, 44 + broken, (3, top, 12, top + 6))
    _outline(cv)
    return cv


def fallen():
    cv = J.Canvas(32, 16)
    _stone_rect(cv, 2, 4, 28, 12, 50)
    for y in range(4, 13):                          # ronde doorsnede links (breukvlak)
        cv.p[y][2] = SHADE
        cv.p[y][3] = LIGHT if 6 <= y <= 10 else SHADE
    for x in range(6, 28, 5):
        for y in range(5, 12):
            cv.p[y][x] = SHADE
    _moss(cv, 4, 52, (4, 4, 28, 12))
    _outline(cv)
    return cv


def block(variant):
    cv = J.Canvas(16, 16)
    rr = random.Random(60 + variant)
    _stone_rect(cv, 2 + variant, 4, 13, 13, 61 + variant)
    _moss(cv, 3, 62 + variant, (3, 4, 13, 8))
    _outline(cv)
    return cv


def paving(variant):
    cv = J.Canvas(16, 16)
    rr = random.Random(70 + variant)
    slabs = ((1, 1, 7, 6), (9, 1, 14, 7), (1, 8, 6, 14), (8, 9, 14, 14))
    for i, (x0, y0, x1, y1) in enumerate(slabs):
        if (i + variant) % 4 == 3:
            continue                                # een plaat ontbreekt: gras eronder
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c = STONE if rr.random() > 0.15 else SHADE
                if y == y1 or x == x1:
                    c = SHADE
                cv.p[y][x] = c
    _moss(cv, 2, 71 + variant)
    return cv


def preview(path, scale=4):
    from PIL import Image
    pal = J.read_pal('data/tilesets/primary/general/palettes/03.pal')
    items = [dais(), pillar(False), pillar(True), fallen(), block(0), block(1), paving(0), paving(1)]
    W = sum(c.w + 4 for c in items)
    img = Image.new('RGB', (W, 36), (164, 213, 197))
    x = 0
    for cv in items:
        for y in range(cv.h):
            for xx in range(cv.w):
                if cv.p[y][xx]:
                    img.putpixel((x + xx, y), pal[cv.p[y][xx]])
        x += cv.w + 4
    img.resize((W * scale, 36 * scale), Image.NEAREST).save(path)


if __name__ == '__main__':
    preview(sys.argv[1] if len(sys.argv) > 1 else 'ruins_preview.png')
