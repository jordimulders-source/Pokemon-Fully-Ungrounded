"""Project Grounded: tilesets voor de drie nieuwe Safari-zones (Fairy Forest, Thunder Plains, Haunted Camp).

Per zone:
- een primary `safari_<zone>_general`: tiles en metatiles van General (BASE-bestand voor render_map.py), alleen eigen
  paletten (pastel / dor savannegeel / mistig donker);
- een secondary `safari_<zone>`: kopie van Fortree / Fallarbor / Lilycove (tiles, metatiles, attributen) met eigen
  paletten en eigen metatiles achteraan (pijlwarps, droog hoog gras, glinsterbloemen).
Daarnaast krijgt Lilycove zelf (de tileset van de Safari Zone) achteraan één metatile: gras met een westpijl-warp, voor de
openingen in SafariZone_Northwest en SafariZone_Southwest.

Wordt aangeroepen door safari_zones.py; los draaien kan ook (idempotent).
Geeft de nummers van de nieuwe metatiles terug via `build()`."""
import colorsys, math, os, shutil, struct
from PIL import Image

PRIM = 'data/tilesets/primary'
SEC = 'data/tilesets/secondary'
MB_TALL_GRASS, MB_EAST_ARROW, MB_WEST_ARROW = 0x02, 0x62, 0x63


# ---------------------------------------------------------------- paletten
def read_pal(path):
    lines = open(path).read().split('\n')[3:19]
    return [tuple(map(int, l.split())) for l in lines]


def write_pal(path, cols):
    with open(path, 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % tuple(max(0, min(255, int(v))) // 8 * 8 for v in c)
                                                for c in cols))


def hsv(c):
    h, s, v = colorsys.rgb_to_hsv(*(x / 255 for x in c))
    return h * 360, s, v


def rgb(h, s, v):
    return tuple(int(round(x * 255)) for x in colorsys.hsv_to_rgb((h % 360) / 360, max(0, min(1, s)), max(0, min(1, v))))


def fairy(c):
    """Pastel feeënbos: bladeren roze-lila, grond zacht mint, water iets paarser, rots/hout bleker."""
    h, s, v = hsv(c)
    if s < 0.1:
        return rgb(280, s + 0.04, v)
    if 60 <= h < 140:                       # bladgroen -> roze/lila (licht = roze, donker = pruim)
        return rgb(312 - 30 * (1 - v), s * 0.38 + 0.06, min(1, v * 1.02 + 0.1))
    if 140 <= h < 190:                      # grondgroen -> pastelmint
        return rgb(158, s * 0.55, min(1, v * 1.03 + 0.05))
    if 190 <= h < 260:                      # water
        return rgb(h + 18, s * 0.8, min(1, v * 1.02))
    return rgb(h + 6, s * 0.75, min(1, v * 1.04 + 0.03))


def thunder(c):
    """Savanne onder onweer: groen wordt olijf/goudgeel, grijze as wordt stro, rots oker; alles iets donkerder."""
    h, s, v = hsv(c)
    if s < 0.08:
        return rgb(45, s + 0.05, v * 0.95)
    if 30 <= h < 140 and s < 0.3:           # as (Fallarbor) en vale tinten -> stro
        return rgb(44, 0.34 + s * 0.4, min(1, v * 0.98))
    if 60 <= h < 140:                       # bladgroen -> olijf
        return rgb(62 - 10 * (1 - v), s * 0.8, v * 0.9)
    if 140 <= h < 190:                      # grondgroen -> droog stro
        return rgb(46, 0.32 + s * 0.25, min(1, v * 0.9))
    if 190 <= h < 260:                      # water: troebel
        return rgb(h - 8, s * 0.7, v * 0.85)
    return rgb(h + 4, min(1, s * 1.05), v * 0.92)


def spook(c):
    """Mistig spookkamp: koud, ontkleurd en donker; warm licht (lampen) blijft een beetje gloeien."""
    h, s, v = hsv(c)
    if 35 <= h < 65 and s > 0.4 and v > 0.7:  # lamplicht
        return rgb(h - 5, s * 0.8, v * 0.85)
    L = v * (0.55 + 0.1 * (1 - s))
    if 60 <= h < 200:                       # groen -> grijsblauw/violet
        return rgb(232 - 30 * v, 0.22 + s * 0.12, L * 0.82 + 0.04)
    if 200 <= h < 260:                      # water: inktblauw
        return rgb(235, s * 0.55, v * 0.45)
    return rgb(260, s * 0.25 + 0.06, L * 0.8 + 0.03)


ZONES = {
    'fairy': dict(base='fortree', tf=fairy, Sym='SafariFairy', cb='InitTilesetAnim_Fortree'),
    'thunder': dict(base='fallarbor', tf=thunder, Sym='SafariThunder', cb='InitTilesetAnim_Fallarbor'),
    'spook': dict(base='lilycove', tf=spook, Sym='SafariSpook', cb='InitTilesetAnim_Lilycove'),
}


def make_palettes(src, dst, tf, idx):
    os.makedirs(dst + '/palettes', exist_ok=True)
    for i in range(16):
        cols = read_pal('%s/palettes/%02d.pal' % (src, i))
        if i in idx:
            cols = [cols[0]] + [tf(c) for c in cols[1:]] if i else [tf(c) for c in cols]
        write_pal('%s/palettes/%02d.pal' % (dst, i), cols)


# ---------------------------------------------------------------- nieuwe tiles (Fairy Forest: glinsterbloemen)
GLOW_PAL = [(0, 0, 0), (255, 255, 255), (206, 255, 255), (120, 222, 246), (66, 140, 214), (255, 222, 246),
            (246, 148, 214), (200, 90, 180), (190, 238, 214), (120, 190, 170), (255, 246, 160), (230, 200, 255),
            (170, 130, 230)]
GLOW_PAL += [(0, 0, 0)] * (16 - len(GLOW_PAL))


def glow_flower(px, cx, cy, kind, r=3.4):
    """Klein lichtgevend bloempje: vier ronde blaadjes, een wit hart; kind 0 = blauw, 1 = roze, 2 = lila."""
    petal = [(3, 2), (6, 5), (7, 7), (12, 11)][kind] if kind < 3 else None
    light, dark = {0: (2, 3), 1: (5, 6), 2: (11, 12)}[kind]
    for y in range(16):
        for x in range(16):
            dx, dy = x - cx, y - cy
            d = math.hypot(dx, dy)
            if d < 1.0:
                px[y][x] = 1
            elif d <= r:
                a = math.atan2(dy, dx)
                lobe = abs(math.cos(2 * a))
                if d <= 1.6 + (r - 1.6) * lobe:
                    px[y][x] = light if d < r - 1.0 else dark
                elif d <= r + 0.6 and not px[y][x]:
                    px[y][x] = 2 if kind == 0 else 5 if kind == 1 else 11   # gloed tussen de blaadjes


def stem(px, x, y0, y1):
    for y in range(y0, y1 + 1):
        if 0 <= y < 16 and not px[y][x]:
            px[y][x] = 9 if y % 2 else 8


def sparkle(px, x, y, big):
    if big:
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            px[y + dy][x + dx] = 10 if (dx or dy) else 1
        for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
            if 0 <= x + dx < 16 and 0 <= y + dy < 16:
                px[y + dy][x + dx] = 2
    else:
        px[y][x] = 1


GLOW_VARIANTS = [
    # bloemen (x, y, soort), stengels (x, y0, y1), glinsters (x, y, groot)
    ([(4.5, 4.5, 0), (11.5, 10.5, 1)], [(4, 7, 9), (11, 13, 15)], [(12, 3, True), (3, 12, False)]),
    ([(10.5, 4.5, 2), (4.5, 11.5, 0)], [(10, 7, 9), (4, 14, 15)], [(3, 3, False), (12, 12, True)]),
    ([(7.5, 7.5, 1), (12.5, 2.5, 0), (2.5, 13.0, 2)], [(7, 10, 12)], [(2, 4, True), (13, 12, False)]),
]
SPARKLE_VARIANTS = [[(4, 4, True), (12, 12, False)], [(11, 4, False), (4, 11, True)]]   # elk maar twee kwarten


def build_glow_tiles():
    imgs = []
    for flowers, stems, sparks in GLOW_VARIANTS:
        px = [[0] * 16 for _ in range(16)]
        for fx, fy, k in flowers:
            glow_flower(px, fx, fy, k)
        for sx, y0, y1 in stems:
            stem(px, sx, y0, y1)
        for x, y, b in sparks:
            sparkle(px, x, y, b)
        imgs.append(px)
    for sparks in SPARKLE_VARIANTS:
        px = [[0] * 16 for _ in range(16)]
        for x, y, b in sparks:
            sparkle(px, x, y, b)
        imgs.append(px)
    return imgs


# ---------------------------------------------------------------- opbouw
def meta(path, i):
    m = open(path + '/metatiles.bin', 'rb').read()
    return list(struct.unpack_from('<8H', m, i * 16))


def attr(path, i):
    return struct.unpack_from('<H', open(path + '/metatile_attributes.bin', 'rb').read(), i * 2)[0]


def ensure_lilycove_arrow():
    """Lilycove (Safari Zone): achteraan gras met westpijl-warp. Geeft het metatilenummer."""
    gen = PRIM + '/general'
    ent = meta(gen, 0x001)
    rec = struct.pack('<8H', *ent)
    mpath, apath = SEC + '/lilycove/metatiles.bin', SEC + '/lilycove/metatile_attributes.bin'
    m, a = open(mpath, 'rb').read(), open(apath, 'rb').read()
    n = len(m) // 16
    if m[-16:] == rec and struct.unpack_from('<H', a, (n - 1) * 2)[0] == MB_WEST_ARROW:
        return 0x200 + n - 1
    open(mpath, 'wb').write(m + rec)
    open(apath, 'wb').write(a + struct.pack('<H', MB_WEST_ARROW))
    return 0x200 + n


def build():
    out = {'lilycove_west_arrow': ensure_lilycove_arrow()}
    gen = PRIM + '/general'
    for zone, z in ZONES.items():
        # primary: alleen paletten (0-5 omgekleurd)
        pdir = '%s/safari_%s_general' % (PRIM, zone)
        os.makedirs(pdir, exist_ok=True)
        open(pdir + '/BASE', 'w').write('general\n')
        make_palettes(gen, pdir, z['tf'], range(6))
        # secondary: volledige kopie + eigen metatiles achteraan
        src, dst = SEC + '/' + z['base'], '%s/safari_%s' % (SEC, zone)
        os.makedirs(dst, exist_ok=True)
        make_palettes(src, dst, z['tf'], range(6, 13))
        mts = bytearray(open(src + '/metatiles.bin', 'rb').read())
        att = bytearray(open(src + '/metatile_attributes.bin', 'rb').read())
        first = 0x200 + len(mts) // 16
        new = {}

        def add(name, ent, a):
            new[name] = 0x200 + len(mts) // 16
            mts.extend(struct.pack('<8H', *ent))
            att.extend(struct.pack('<H', a))

        im = Image.open(src + '/tiles.png')
        if zone == 'fairy':
            write_pal(dst + '/palettes/06.pal', GLOW_PAL)
            ntiles = 493                                       # Fortree heeft 493 tiles; nieuwe vanaf 493
            out_im = Image.new('P', (128, 256), 0)
            out_im.putpalette(im.getpalette())
            out_im.paste(im, (0, 0))
            tidx = {}
            ents = []
            for px in build_glow_tiles():
                e = []
                for k in range(4):
                    ox, oy = (k % 2) * 8, (k // 2) * 8
                    t = tuple(px[oy + y][ox + x] for y in range(8) for x in range(8))
                    if not any(t):
                        e.append(0x0000)                       # lege tile (General-tile 0)
                        continue
                    if t not in tidx:
                        tidx[t] = ntiles + len(tidx)
                        n = tidx[t]
                        for p, v in enumerate(t):
                            out_im.putpixel(((n % 16) * 8 + p % 8, (n // 16) * 8 + p // 8), v)
                    e.append(0x6000 | (512 + tidx[t]))
                ents.append(e)
            assert ntiles + len(tidx) <= 512, len(tidx)
            out_im.save(dst + '/tiles.png')
            grass = meta(gen, 0x001)[:4]
            for i, e in enumerate(ents[:3]):
                add('glow%d' % i, grass + e, 0x1000)
            for i, e in enumerate(ents[3:]):
                add('sparkle%d' % i, grass + e, 0x1000)
            add('east_arrow', meta(gen, 0x001), MB_EAST_ARROW)
            print('fairy: %d nieuwe tiles' % len(tidx))
        else:
            shutil.copy(src + '/tiles.png', dst + '/tiles.png')
            if zone == 'thunder':
                add('dry_grass', meta(src, 0x20a - 0x200), MB_TALL_GRASS)
            if zone == 'spook':
                add('east_arrow', meta(gen, 0x001), MB_EAST_ARROW)
        open(dst + '/metatiles.bin', 'wb').write(mts)
        open(dst + '/metatile_attributes.bin', 'wb').write(att)
        out[zone] = new
        register(zone, z)
    return out


def register(zone, z):
    Sym, ts = z['Sym'], 'safari_' + zone
    hdr = open('src/data/tilesets/headers.h').read()
    if 'gTileset_%sGeneral ' % Sym not in hdr:
        hdr += '''
// Project Grounded: Safari Zone, %s (tools/grounded/maptools/safari_tilesets.py)
const struct Tileset gTileset_%sGeneral =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_General,
    .palettes = gTilesetPalettes_%sGeneral,
    .metatiles = gMetatiles_General,
    .metatileAttributes = gMetatileAttributes_General,
    .callback = InitTilesetAnim_General,
};

const struct Tileset gTileset_%s =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_%s,
    .palettes = gTilesetPalettes_%s,
    .metatiles = gMetatiles_%s,
    .metatileAttributes = gMetatileAttributes_%s,
    .callback = %s,
};
''' % (zone, Sym, Sym, Sym, Sym, Sym, Sym, Sym, z['cb'])
        open('src/data/tilesets/headers.h', 'w').write(hdr)
    gfx = open('src/data/tilesets/graphics.h').read()
    if 'gTilesetTiles_%s[]' % Sym not in gfx:
        gfx += '\nconst u16 gTilesetPalettes_%sGeneral[][16] =\n{\n' % Sym
        gfx += ''.join('    INCBIN_U16("%s/%s_general/palettes/%02d.gbapal"),\n' % (PRIM, ts, i) for i in range(16)) + '};\n'
        gfx += '\nconst u32 gTilesetTiles_%s[] = INCBIN_U32("%s/%s/tiles.4bpp.fastSmol");\n' % (Sym, SEC, ts)
        gfx += '\nconst u16 gTilesetPalettes_%s[][16] =\n{\n' % Sym
        gfx += ''.join('    INCBIN_U16("%s/%s/palettes/%02d.gbapal"),\n' % (SEC, ts, i) for i in range(16)) + '};\n'
        open('src/data/tilesets/graphics.h', 'w').write(gfx)
    mh = open('src/data/tilesets/metatiles.h').read()
    if 'gMetatiles_%s[]' % Sym not in mh:
        mh += '\nconst u16 gMetatiles_%s[] = INCBIN_U16("%s/%s/metatiles.bin");\n' % (Sym, SEC, ts)
        mh += 'const u16 gMetatileAttributes_%s[] = INCBIN_U16("%s/%s/metatile_attributes.bin");\n' % (Sym, SEC, ts)
        open('src/data/tilesets/metatiles.h', 'w').write(mh)


if __name__ == '__main__':
    print(build())
