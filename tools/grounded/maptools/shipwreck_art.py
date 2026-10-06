"""Project Grounded: tileset `shipwreck_shoals` (secondary bij General) voor het scheepswrakkenkerkhof.

- Het spookschip: de 19 metatiles van het Abandoned Ship-wrak op Route 108 (Slateport 0x351-0x36b), met eigen,
  bleekgroen getinte kopieen van de Slateport-paletten 6/8/10 (zusterschip: zelfde bouw, maar dood).
- Wrakdecor (palet 7, met de hand getekend): masten die uit het water steken (met gescheurd zeil en kraaiennest),
  geraamte van een romp (spanten), een gekapseisde romp met zeepokken, een boeg die schuin omhoogsteekt, tonnen en
  kisten. Elk stuk op zee (water van General 0x170, geanimeerd) en de mast/ton/kist ook op een ondiepte (0x19e).

`build()` schrijft de tileset en geeft {naam: metatile-id} terug; `shipwreck_shoals.py` gebruikt dat.
Los gedraaid: python3 tools/grounded/maptools/shipwreck_art.py [voorbeeld.png] (vergroot voorbeeld van alle stukken)."""
import os, struct, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jungle_tileset as J

TS = 'data/tilesets/secondary/shipwreck_shoals'
SLATE = 'data/tilesets/secondary/slateport'
GEN = 'data/tilesets/primary/general'
P_WRECK = 7
COVERED = 1 << 12

# palet 7: wrakhout, zeil, schuim, zeepokken
WRECK_PAL = [(0, 0, 0),
             (36, 28, 24), (64, 44, 32), (92, 64, 44), (124, 90, 60), (156, 120, 80),   # 1-5 hout (omlijning..licht)
             (104, 104, 92), (148, 144, 124), (188, 184, 164),                          # 6-8 zeil
             (236, 244, 248), (168, 196, 232),                                          # 9-10 schuim
             (72, 96, 64), (140, 148, 124),                                             # 11-12 wier, zeepok
             (84, 80, 84), (148, 124, 84), (100, 44, 44)]                               # 13 ijzer, 14 touw, 15 vlag

SHIP = [0x351, 0x352, 0x353, 0x354, 0x358, 0x359, 0x35a, 0x35b, 0x35c, 0x35d,
        0x360, 0x361, 0x362, 0x363, 0x364, 0x365, 0x369, 0x36a, 0x36b]


def ghost(c, i):
    """Spooktint: ontkleurd, naar bleek zeegroen; index 0 (achtergrond) ongemoeid."""
    if i == 0:
        return c
    r, g, b = c
    lum = 0.3 * r + 0.59 * g + 0.11 * b
    t = (150, 214, 190)
    k = 0.55
    out = []
    for ch, tc in zip((r, g, b), t):
        v = lum * (1 - k) + (lum / 255 * tc) * k
        out.append(max(0, min(255, int(v * 1.08 + 10))))
    return tuple(out)


def tiles_of(cv):
    """Canvas (w x h pixels) -> lijst rijen van 8x8-tiles."""
    return [[[[cv.p[ty * 8 + y][tx * 8 + x] for x in range(8)] for y in range(8)] for tx in range(cv.w // 8)]
            for ty in range(cv.h // 8)]


class Builder:
    def __init__(self):
        self.tiles = [[[0] * 8 for _ in range(8)]]          # tile 0 leeg
        self.tidx = {self.key(self.tiles[0]): (0, 0)}
        self.mts, self.attrs = bytearray(), bytearray()
        self.names = {}
        self.gm = open(GEN + '/metatiles.bin', 'rb').read()
        self.sm = open(SLATE + '/metatiles.bin', 'rb').read()
        self.sa = open(SLATE + '/metatile_attributes.bin', 'rb').read()
        self.stiles, self.pngpal = J.png_tiles(SLATE + '/tiles.png')
        self.pals = [[(0, 0, 0)] * 16 for _ in range(16)]
        for p in (6, 8, 10):
            self.pals[p] = [ghost(c, i) for i, c in enumerate(J.read_pal('%s/palettes/%02d.pal' % (SLATE, p)))]
        self.pals[P_WRECK] = list(WRECK_PAL)

    @staticmethod
    def key(t):
        return tuple(tuple(r) for r in t)

    def tile(self, t):
        """Geeft (index, flipbits) voor een 8x8-tile; ontdubbelt ook gespiegelde tiles."""
        for hf in (0, 1):
            for vf in (0, 1):
                tt = [row[::-1] if hf else row[:] for row in t]
                if vf:
                    tt = tt[::-1]
                k = self.key(tt)
                if k in self.tidx:
                    i, _ = self.tidx[k]
                    return i, (hf << 10) | (vf << 11)
        self.tiles.append([r[:] for r in t])
        i = len(self.tiles) - 1
        self.tidx[self.key(t)] = (i, 0)
        return i, 0

    def add(self, name, entries, attr):
        mid = 0x200 + len(self.mts) // 16
        self.mts += struct.pack('<8H', *entries)
        self.attrs += struct.pack('<H', attr)
        self.names[name] = mid
        return mid

    def bottom_of(self, gid):
        return list(struct.unpack_from('<4H', self.gm, gid * 16))

    def ship(self):
        for m in SHIP:
            e = list(struct.unpack_from('<8H', self.sm, (m - 0x200) * 16))
            out = []
            for v in e:
                t = v & 0x3FF
                if t >= 512:
                    i, fl = self.tile(self.stiles[t - 512])
                    v = (v & 0xF000) | ((v & 0xC00) ^ fl) | (512 + i)
                out.append(v)
            self.add('ship_%03x' % m, out, struct.unpack_from('<H', self.sa, (m - 0x200) * 2)[0])

    def art(self, name, cv, bases=('sea',)):
        """Canvas -> metatiles (bovenlaag), per ondergrond: zee 0x170 of ondiepte 0x19e."""
        rows = tiles_of(cv)
        for base in bases:
            bot = self.bottom_of(0x170 if base == 'sea' else 0x19e)
            for my in range(cv.h // 16):
                for mx in range(cv.w // 16):
                    top = []
                    for k in range(4):
                        t = rows[my * 2 + k // 2][mx * 2 + k % 2]
                        if not any(any(r) for r in t):
                            top.append(0)
                            continue
                        i, fl = self.tile(t)
                        top.append((P_WRECK << 12) | fl | (512 + i))
                    self.add('%s_%s_%d_%d' % (name, base, mx, my), bot + top, COVERED)

    def save(self):
        os.makedirs(TS + '/palettes', exist_ok=True)
        n = len(self.tiles)
        rows = (n + 15) // 16
        out = Image.new('P', (128, rows * 8), 0)
        out.putpalette(self.pngpal)
        for k, t in enumerate(self.tiles):
            for y in range(8):
                for x in range(8):
                    out.putpixel(((k % 16) * 8 + x, (k // 16) * 8 + y), t[y][x])
        out.save(TS + '/tiles.png')
        for i in range(16):
            J.write_pal('%s/palettes/%02d.pal' % (TS, i), self.pals[i])
        open(TS + '/metatiles.bin', 'wb').write(self.mts)
        open(TS + '/metatile_attributes.bin', 'wb').write(self.attrs)
        register()
        return n


def register():
    hdr = open('src/data/tilesets/headers.h').read()
    if 'gTileset_ShipwreckShoals' not in hdr:
        hdr += '''
const struct Tileset gTileset_ShipwreckShoals = // Project Grounded: scheepswrakkenkerkhof + spookschip (shipwreck_art.py)
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_ShipwreckShoals,
    .palettes = gTilesetPalettes_ShipwreckShoals,
    .metatiles = gMetatiles_ShipwreckShoals,
    .metatileAttributes = gMetatileAttributes_ShipwreckShoals,
    .callback = NULL,
};
'''
        open('src/data/tilesets/headers.h', 'w').write(hdr)
    gfx = open('src/data/tilesets/graphics.h').read()
    if 'gTilesetTiles_ShipwreckShoals' not in gfx:
        gfx += '\nconst u32 gTilesetTiles_ShipwreckShoals[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n\n' % TS
        gfx += 'const u16 gTilesetPalettes_ShipwreckShoals[][16] =\n{\n'
        gfx += ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (TS, i) for i in range(16)) + '};\n'
        open('src/data/tilesets/graphics.h', 'w').write(gfx)
    mh = open('src/data/tilesets/metatiles.h').read()
    if 'gMetatiles_ShipwreckShoals' not in mh:
        mh += '\nconst u16 gMetatiles_ShipwreckShoals[] = INCBIN_U16("%s/metatiles.bin");\n' % TS
        mh += 'const u16 gMetatileAttributes_ShipwreckShoals[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % TS
        open('src/data/tilesets/metatiles.h', 'w').write(mh)


# ---------------------------------------------------------------- tekenen
C = J.Canvas


def hline(cv, x0, x1, y, c):
    for x in range(x0, x1 + 1):
        cv.set(x, y, c)


def vline(cv, x, y0, y1, c):
    for y in range(y0, y1 + 1):
        cv.set(x, y, c)


def foam(cv, cx, y, half, rng_seed=0):
    """Schuimkraag op de waterlijn: een platte ellips met lichte en blauwe pixels."""
    for dx in range(-half, half + 1):
        a = abs(dx) / max(1, half)
        h = 1 if a > 0.7 else 2
        for dy in range(h):
            c = 9 if (dx + dy + rng_seed) % 3 else 10
            if not cv.get(cx + dx, y + dy) or cv.get(cx + dx, y + dy) in (9, 10):
                cv.set(cx + dx, y + dy, c)
    for dx in (-half - 2, half + 2, -half - 4, half + 3):
        cv.set(cx + dx, y + 1, 10)


def pole(cv, x, y0, y1):
    """Mast van 4 px breed: omlijning, hout, licht."""
    for y in range(y0, y1 + 1):
        cv.set(x, y, 1); cv.set(x + 1, y, 3); cv.set(x + 2, y, 4); cv.set(x + 3, y, 1)
    for y in range(y0 + 3, y1, 7):
        cv.set(x + 1, y, 2); cv.set(x + 2, y, 3)


def mast():
    cv = C(16, 48)
    # gescheurd zeil onder de ra (eerst, de mast komt eroverheen)
    import random
    r = random.Random(5)
    for y in range(21, 36):
        x0, x1 = 2 + (y - 21) // 5, 13 - (y - 21) // 4
        for x in range(x0, x1 + 1):
            if y > 30 and r.random() < 0.45:
                continue
            if (x, y) in ((5, 25), (6, 25), (5, 26), (11, 28), (11, 29), (10, 29), (4, 31)):
                continue
            c = 8 if x < 6 else 7 if x < 11 else 6
            if y % 4 == 0:
                c = 6 if c == 7 else 7
            cv.set(x, y, c)
    for x in range(2, 14):                      # rafelige onderrand
        yb = max(y for y in range(21, 36) if cv.get(x, y)) if any(cv.get(x, y) for y in range(21, 36)) else None
        if yb and r.random() < 0.6:
            cv.set(x, yb + 1, 6)
    pole(cv, 6, 3, 43)
    # ra (dwarshout), links afgeknakt
    for x in range(1, 15):
        y = 18 + (1 if x < 4 else 0) + (1 if x < 2 else 0)
        cv.set(x, y, 1); cv.set(x, y + 1, 4 if x % 3 else 3); cv.set(x, y + 2, 1)
    # kraaiennest
    for x in range(3, 13):
        cv.set(x, 7, 1); cv.set(x, 12, 1)
        for y in range(8, 12):
            cv.set(x, y, 2 if y == 11 else 4 if y == 8 else 3)
    vline(cv, 3, 7, 12, 1); vline(cv, 12, 7, 12, 1)
    for x in (5, 8, 11):
        vline(cv, x, 8, 11, 2)
    # vlag (gescheurde wimpel) bovenaan
    for y in range(0, 5):
        for x in range(10, 10 + (5 - y if y > 1 else 5)):
            if (x + y) % 5 != 3:
                cv.set(x, y, 15)
    vline(cv, 9, 0, 6, 1)
    # touwen van het nest naar de ra-uiteinden
    for (xa, ya), (xb, yb) in (((3, 13), (1, 18)), ((12, 13), (14, 18))):
        for p in J.polyline([(xa, ya), (xb, yb)]):
            cv.set(p[0], p[1], 14)
    # wier en zeepokken boven de waterlijn, schuim
    for y in range(38, 44):
        if y % 2 == 0:
            cv.set(7, y, 11)
        else:
            cv.set(8, y, 12)
    foam(cv, 8, 43, 5)
    for y in range(45, 48):
        for x in range(16):
            if cv.get(x, y) not in (9, 10):
                cv.set(x, y, 0)
    return cv


def ribs():
    """Geraamte van een romp: vier spanten en een kiel die net boven het water komen."""
    cv = C(48, 32)
    import math
    for i, bx in enumerate((7, 18, 29, 40)):
        hgt = (20, 25, 23, 17)[i]
        lean = (-3, -1, 1, 3)[i]
        for t in range(hgt + 1):
            f = t / hgt
            x = bx + lean * f + 3 * math.sin(f * math.pi * 0.9) * (1 if i < 2 else -1)
            y = 27 - t
            w = 3 if t < hgt - 2 else 2
            for k in range(w):
                cv.set(x + k, y, 3 if k == 1 else 4 if k == 2 else 2)
        # spant breekt af: splinters
        top_x = bx + lean + (0 if i < 2 else -1)
        cv.set(top_x + 1, 27 - hgt - 1, 4)
        cv.set(top_x, 27 - hgt - 2, 3)
    grow_outline(cv)
    # kiel
    for x in range(3, 45):
        cv.set(x, 25, 1); cv.set(x, 26, 4 if x % 6 else 3); cv.set(x, 27, 3); cv.set(x, 28, 1)
    for x in range(5, 44, 7):
        cv.set(x, 27, 12); cv.set(x + 1, 26, 11)
    for cx in (10, 24, 37):
        foam(cv, cx, 28, 6, cx)
    return cv


def grow_outline(cv):
    J.grow(cv, 1, only={2, 3, 4, 5})


def hull():
    """Gekapseisde romp: de bolle onderkant steekt boven water, met kiel, planken, zeepokken en een gat."""
    cv = C(48, 32)
    cx, cy, rx, ry = 23.5, 27.0, 21.5, 20.0
    for y in range(32):
        for x in range(48):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d <= 1 and y <= 27:
                plank = (y - 7) // 3
                c = 4 if plank % 2 else 3
                if (y - 7) % 3 == 0:
                    c = 2
                if x > cx + 8 and c == 4:
                    c = 3
                if x < cx - 12 and c == 3:
                    c = 4
                cv.set(x, y, c)
    # kiel bovenop
    for x in range(6, 42):
        if cv.get(x, 8):
            yk = min(y for y in range(32) if cv.get(x, y))
            cv.set(x, yk - 1, 5); cv.set(x, yk - 2, 2)
    # gat
    for (x, y) in [(28, 16), (29, 16), (30, 16), (27, 17), (28, 17), (29, 17), (30, 17), (31, 17), (28, 18), (29, 18),
                   (30, 18), (31, 18), (29, 19), (30, 19)]:
        cv.set(x, y, 1)
    cv.set(27, 15, 5); cv.set(31, 15, 2); cv.set(32, 18, 5)
    # zeepokken en wier
    for (x, y) in [(10, 22), (13, 24), (16, 21), (35, 23), (38, 21), (21, 25), (40, 24), (8, 25), (26, 23)]:
        cv.set(x, y, 12); cv.set(x + 1, y, 13)
    for x in range(4, 44, 3):
        if cv.get(x, 26):
            cv.set(x, 26, 11)
    J.grow(cv, 1, only={2, 3, 4, 5, 11, 12, 13})
    for x in range(48):
        for y in range(28, 32):
            cv.set(x, y, 0)
    for cx2 in (8, 20, 32, 41):
        foam(cv, cx2, 27, 6, cx2)
    return cv


def bow():
    """Boeg die schuin omhoog uit zee steekt, met boegspriet."""
    cv = C(32, 32)
    # romp als driehoek: punt linksboven, basis op de waterlijn
    for y in range(6, 28):
        f = (y - 6) / 21
        x0 = int(8 + 2 * f)
        x1 = int(10 + 18 * f)
        for x in range(x0, x1 + 1):
            band = (x - x0) * 4 // max(1, x1 - x0 + 1)
            c = (5, 4, 3, 2)[band]
            if (y + x // 3) % 4 == 0 and band > 0:
                c = max(2, c - 1)
            cv.set(x, y, c)
    # reling
    for y in range(6, 28):
        f = (y - 6) / 21
        cv.set(int(10 + 18 * f) - 1, y, 5)
    # boegspriet
    for p in J.polyline([(9, 7), (2, 1)]):
        cv.set(p[0], p[1], 3); cv.set(p[0] + 1, p[1], 4)
    # naam half weggevreten
    for x, y in [(15, 20), (16, 20), (18, 20), (19, 21), (21, 21)]:
        cv.set(x, y, 8)
    for (x, y) in [(12, 24), (15, 25), (20, 26), (24, 25)]:
        cv.set(x, y, 12)
    J.grow(cv, 1, only={2, 3, 4, 5, 8, 12})
    for x in range(32):
        for y in range(28, 32):
            cv.set(x, y, 0)
    foam(cv, 13, 27, 6, 1)
    foam(cv, 24, 27, 6, 2)
    return cv


def barrel():
    cv = C(16, 16)
    for y in range(3, 13):
        w = 4 if y in (3, 12) else 5
        for x in range(8 - w, 8 + w):
            c = 4 if x < 7 else 3
            if x in (8 - w,):
                c = 5
            cv.set(x, y, c)
        if y in (5, 10):
            hline(cv, 8 - w, 7 + w, y, 13)
    J.grow(cv, 1, only={3, 4, 5, 13})
    for x in range(16):
        for y in range(13, 16):
            cv.set(x, y, 0)
    foam(cv, 8, 12, 5, 0)
    return cv


def crate():
    cv = C(16, 16)
    for y in range(4, 12):
        for x in range(3, 13):
            c = 4 if (y - 4) % 3 else 2
            if x in (3, 12):
                c = 3
            cv.set(x, y, c)
    for i in range(8):
        cv.set(4 + i, 4 + i, 5)
    for y in range(1, 4):
        for x in range(4 + (3 - y), 14 - (3 - y)):
            cv.set(x, y, 5 if y > 1 else 4)
    J.grow(cv, 1, only={2, 3, 4, 5})
    for x in range(16):
        for y in range(12, 16):
            cv.set(x, y, 0)
    foam(cv, 8, 11, 6, 1)
    return cv


PIECES = [('mast', mast, ('sea', 'shoal')), ('ribs', ribs, ('sea',)), ('hull', hull, ('sea',)),
          ('bow', bow, ('sea',)), ('barrel', barrel, ('sea', 'shoal')), ('crate', crate, ('sea', 'shoal'))]


def build():
    b = Builder()
    b.ship()
    for name, fn, bases in PIECES:
        b.art(name, fn(), bases)
    n = b.save()
    return b.names, n


if __name__ == '__main__':
    names, n = build()
    print('tiles', n, 'metatiles', len(names))
    if len(sys.argv) > 1:
        from gridrender import render
        groups = []
        for name, fn, bases in PIECES:
            cv = fn()
            for base in bases:
                groups.append([[names['%s_%s_%d_%d' % (name, base, mx, my)] for mx in range(cv.w // 16)]
                               for my in range(cv.h // 16)])
        W = sum(len(g[0]) + 1 for g in groups) + 1
        H = max(len(g) for g in groups) + 2
        grid = [[0x170] * W for _ in range(H)]
        x = 1
        for g in groups:
            for my, row in enumerate(g):
                for mx, m in enumerate(row):
                    grid[1 + my][x + mx] = m
            x += len(g[0]) + 1
        ship = [[names['ship_%03x' % m] if m else 0x19e for m in row] for row in
                [[0, 0x351, 0x352, 0x353, 0x354, 0], [0x358, 0x359, 0x35a, 0x35b, 0x35c, 0x35d],
                 [0x360, 0x361, 0x362, 0x363, 0x364, 0x365], [0, 0x369, 0x36a, 0x36b, 0, 0]]]
        grid += [[0x170] * W for _ in range(6)]
        for my, row in enumerate(ship):
            for mx, m in enumerate(row):
                grid[H + 1 + my][1 + mx] = m
        render(grid, 'general', 'shipwreck_shoals', 3).save(sys.argv[1])
