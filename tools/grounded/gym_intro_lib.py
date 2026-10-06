"""Project Grounded: gedeelde hulpjes voor de gymleider-intro's (roxanne/brawly/wattson/flannery_transition.py).

Aanpak (zuinig, ±10-25 KB per intro): een paar stilstaande BG0-beelden (tiles + tilemaps) met drie BG-paletten (13, 14,
15) en de beweging in C (sprites, paletcycli, tilemap-blokken, trillen). Beelden worden in RGB getekend en per tile naar
het best passende van de drie paletten omgezet; tiles worden ontdubbeld (ook gespiegeld) over alle beelden samen.

Uitvoer in graphics/battle_transitions/:
- gym_<naam>.png + gym_<naam>.pal: de tiles (tile 0 = leeg) en de drie paletten (make: .4bpp.smol en .gbapal)
- gym_<naam>_maps.bin: alle tilemaps achter elkaar, elk W x H u16 (tile | flip << 10 | palet << 12) (make: .smol)
- sprites: gym_<naam>_<sprite>.png + .pal (make: .4bpp.smol en .gbapal)
"""
import os, re, struct
import numpy as np
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT = os.path.join(ROOT, 'graphics/battle_transitions/')
KEY = (255, 0, 255)          # doorzichtig (index 0); zuiver zwart (0, 0, 0) is in BG-beelden ook doorzichtig
PAL_BASE = 13                # BG-paletten 13, 14, 15


def gba(c):
    return tuple((int(v) >> 3) << 3 for v in c[:3])


def pad16(cols):
    cols = [gba(c) for c in cols]
    assert len(cols) <= 15, len(cols)
    return [(0, 0, 0)] + cols + [(0, 0, 0)] * (15 - len(cols))


# ------------------------------------------------------------------ tekst in het lettertype van de game
_CM = {}
for _line in open(os.path.join(ROOT, 'charmap.txt'), encoding='utf-8'):
    _m = re.match(r"^'(.|…)'\s*=\s*([0-9A-F]{2})\s*(@.*)?$", _line.strip())
    if _m and _m.group(1) not in _CM:
        _CM[_m.group(1)] = int(_m.group(2), 16)
_FONTS = {}


def _font(name):
    if name not in _FONTS:
        key = {'normal': 'Normal', 'narrow': 'Narrow', 'short': 'Short', 'small': 'Small'}[name]
        src = open(os.path.join(ROOT, 'src/fonts.c')).read()
        w = [int(v, 0) for v in re.findall(r'0x[0-9A-Fa-f]+|\d+',
             src.split('const u8 gFont%sLatinGlyphWidths[] = {' % key)[1].split('};')[0])]
        _FONTS[name] = (Image.open(os.path.join(ROOT, 'graphics/fonts/latin_%s.png' % name)), w)
    return _FONTS[name]


def text_width(s, font='normal', scale=1, spacing=0):
    im, w = _font(font)
    return sum((w[_CM[ch]] + spacing) * scale for ch in s)


def text(img, x, y, s, fg, shadow=None, font='normal', scale=1, spacing=0, outline=None):
    """Tekent s op img (PIL RGB) met de bovenkant van de 16 px hoge glyphcel op y. Geeft de eind-x."""
    im, w = _font(font)
    px = im.load()
    for ch in s:
        g = _CM[ch]
        gx, gy = (g % 16) * 16, (g // 16) * 16
        for yy in range(16):
            for xx in range(w[g]):
                v = px[gx + xx, gy + yy]
                col = fg if v == 1 else (shadow if v == 2 else None)
                if col is None:
                    continue
                for sy in range(scale):
                    for sx in range(scale):
                        X, Y = x + xx * scale + sx, y + yy * scale + sy
                        if 0 <= X < img.width and 0 <= Y < img.height:
                            img.putpixel((X, Y), col)
        x += (w[g] + spacing) * scale
    if outline is not None:
        pass
    return x


def outline(img, box, inner_cols, col):
    """Zet een rand van 1 px in kleur col rond alle pixels in box die een van inner_cols hebben."""
    x0, y0, x1, y1 = box
    a = np.array(img)
    mask = np.zeros(a.shape[:2], bool)
    for c in inner_cols:
        mask |= (a[:, :, 0] == c[0]) & (a[:, :, 1] == c[1]) & (a[:, :, 2] == c[2])
    m2 = mask.copy()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        m2 |= np.roll(np.roll(mask, dy, 0), dx, 1)
    edge = m2 & ~mask
    edge[:y0] = edge[y1:] = False
    edge[:, :x0] = edge[:, x1:] = False
    a[edge] = col
    return Image.fromarray(a)



def outlined_text(im, cx, y, s, fg, shadow, edge, scale=2, font='normal'):
    """Tekst gecentreerd op cx met een rand van 1 px in kleur edge (bijv. ondertitels op een zwarte balk); y mag
    negatief zijn (de bovenkant valt dan weg). Geeft een nieuw beeld."""
    sp = 1 if scale > 1 else 0
    H = 16 * scale + 2
    tmp = Image.new('RGB', (im.width, H), KEY)
    text(tmp, cx - text_width(s, font, scale, sp) // 2, 1, s, fg, shadow, font, scale, sp)
    ta = np.array(tmp)
    m = (ta != KEY).any(2)
    m2 = m.copy()
    m2[1:] |= m[:-1]
    m2[:-1] |= m[1:]
    m2[:, 1:] |= m[:, :-1]
    m2[:, :-1] |= m[:, 1:]
    y -= 1
    if y < 0:
        ta, m, m2 = ta[-y:], m[-y:], m2[-y:]
        y = 0
    ia = np.array(im)
    reg = ia[y:y + m.shape[0]]
    n = reg.shape[0]
    ta, m, m2 = ta[:n], m[:n], m2[:n]
    reg[m2 & ~m] = edge
    reg[m] = ta[m]
    return Image.fromarray(ia)

# ------------------------------------------------------------------ metatiles van een tileset (echte game-art)
def _tileset(d):
    im = Image.open(os.path.join(ROOT, d, 'tiles.png'))
    w, h = im.size
    a = np.array(im) & 15
    return [a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] for ty in range(h // 8) for tx in range(w // 8)]


def _jasc(fn):
    L = open(fn).read().split('\n')[3:19]
    return [tuple(int(v) for v in l.split()[:3]) for l in L if l.strip()]


def metatiles(primary, secondary, grid, bg=(0, 0, 0), sec_mt=None):
    """Tekent een raster metatile-nummers (lijst van rijen; None = leeg) met de tiles en paletten van de tilesets."""
    pdir, sdir = 'data/tilesets/primary/' + primary, 'data/tilesets/secondary/' + secondary
    T = _tileset(pdir)
    T += [np.zeros((8, 8), int)] * (512 - len(T))
    T += _tileset(sdir)
    pals = []
    for i in range(16):
        f = os.path.join(ROOT, pdir if i < 6 else sdir, 'palettes', '%02d.pal' % i)
        pals.append(_jasc(f) if os.path.exists(f) else [(0, 0, 0)] * 16)
    mtp = open(os.path.join(ROOT, pdir, 'metatiles.bin'), 'rb').read()
    sm = sec_mt or os.path.join(sdir, 'metatiles.bin')
    if not os.path.exists(os.path.join(ROOT, sm)):
        sm = os.path.join(os.path.dirname(sdir), 'metatiles.bin')
    mts = open(os.path.join(ROOT, sm), 'rb').read()
    H, W = len(grid), len(grid[0])
    img = Image.new('RGB', (W * 16, H * 16), bg)
    for r, row in enumerate(grid):
        for c, m in enumerate(row):
            if m is None:
                continue
            b = mtp[m * 16:m * 16 + 16] if m < 512 else mts[(m - 512) * 16:(m - 512) * 16 + 16]
            e = struct.unpack('<8H', b)
            for layer in range(2):
                for q in range(4):
                    v = e[layer * 4 + q]
                    t, hf, vf, p = v & 0x3FF, v >> 10 & 1, v >> 11 & 1, v >> 12
                    tl = T[t] if t < len(T) else np.zeros((8, 8), int)
                    if hf:
                        tl = tl[:, ::-1]
                    if vf:
                        tl = tl[::-1]
                    for y in range(8):
                        for x in range(8):
                            ci = tl[y][x]
                            if ci == 0:
                                if layer == 0:
                                    img.putpixel((c * 16 + (q % 2) * 8 + x, r * 16 + (q // 2) * 8 + y), tuple(pals[p][0]))
                                continue
                            img.putpixel((c * 16 + (q % 2) * 8 + x, r * 16 + (q // 2) * 8 + y), tuple(pals[p][ci]))
    return img


def scale(img, k):
    return img.resize((img.width * k, img.height * k), Image.NEAREST)


# ------------------------------------------------------------------ omzetten naar tiles en tilemaps
class Encoder:
    def __init__(self, name, pals, prefix='gym_'):
        """pals: drie lijsten van max. 15 kleuren (BG-palet 13, 14, 15). prefix: begin van de bestandsnamen."""
        self.name = name
        self.prefix = prefix
        self.pals = [pad16(p) for p in pals]
        self.tiles = [np.zeros(64, np.uint8)]
        self.index = {self.tiles[0].tobytes(): (0, 0)}
        self.maps = []
        self.worst = 0
        self.bad = 0

    def _tile(self, t):
        for flip in range(4):
            u = t
            if flip & 1:
                u = u[:, ::-1]
            if flip & 2:
                u = u[::-1]
            k = np.ascontiguousarray(u).reshape(64).tobytes()
            if k in self.index:
                return self.index[k][0] | (flip << 10)
        n = len(self.tiles)
        self.tiles.append(t.reshape(64).astype(np.uint8))
        self.index[t.reshape(64).tobytes()] = (n, 0)
        return n

    def add(self, img, force_pal=None, label=''):
        """img: PIL RGB (veelvoud van 8). Geeft de tilemap (lijst u16) en voegt hem toe aan self.maps."""
        n0 = len(self.tiles)
        a = np.array(img.convert('RGB')).astype(np.int32)
        H, W = a.shape[0] // 8, a.shape[1] // 8
        out = []
        key = np.array(KEY)
        for ty in range(H):
            for tx in range(W):
                t = a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].reshape(64, 3)
                transp = (t == key).all(1) | (t == 0).all(1)
                g = (t >> 3) << 3
                best = None
                for k in range(3):
                    if force_pal is not None and k != force_pal:
                        continue
                    pal = np.array(self.pals[k][1:], np.int32)
                    d = ((g[:, None, :] - pal[None, :, :]) ** 2 * np.array([3, 6, 2])).sum(2)
                    idx = d.argmin(1) + 1
                    err = d.min(1)
                    err[transp] = 0
                    e = err.sum()
                    if best is None or e < best[0]:
                        best = (e, k, idx)
                e, k, idx = best
                idx = idx.astype(np.uint8)
                idx[transp] = 0
                self.worst = max(self.worst, e)
                if e > 4000 and self.bad < 12:
                    self.bad += 1
                    print('  %s %s tile (%d,%d): fout %d (palet %d)' % (self.name, label, tx, ty, e, PAL_BASE + k))
                if not idx.any():
                    out.append(0)
                    continue
                out.append(self._tile(idx.reshape(8, 8)) | ((PAL_BASE + k) << 12))
        self.maps.append(out)
        print('  %s %s: +%d tiles' % (self.name, label, len(self.tiles) - n0))
        return out

    def save(self, maps_name='maps'):
        tiles = self.tiles
        cols = 16
        rows = (len(tiles) + cols - 1) // cols
        img = Image.new('P', (cols * 8, rows * 8))
        for i, t in enumerate(tiles):
            img.paste(Image.fromarray(t.reshape(8, 8)), ((i % cols) * 8, (i // cols) * 8))
        img.putpalette([v for c in self.pals[2] for v in c] + [0] * (768 - 48))
        img.save(OUT + '%s%s.png' % (self.prefix, self.name))
        with open(OUT + '%s%s.pal' % (self.prefix, self.name), 'w', newline='\r\n') as fp:
            fp.write('JASC-PAL\n0100\n48\n')
            for pal in self.pals:
                for c in pal:
                    fp.write('%d %d %d\n' % c)
        allm = sum(self.maps, [])
        open(OUT + '%s%s_%s.bin' % (self.prefix, self.name, maps_name), 'wb').write(struct.pack('<%dH' % len(allm), *allm))
        print('%s: %d tiles, %d tilemap-vakken' % (self.name, len(tiles), len(allm)))
        assert len(tiles) <= 700, len(tiles)  # noqa

    def render(self, m, w=30, pals=None):
        """Een tilemap terug naar RGB (voorbeeld)."""
        pals = pals or self.pals
        h = len(m) // w
        img = Image.new('RGB', (w * 8, h * 8), (0, 0, 0))
        for i, v in enumerate(m):
            t = self.tiles[v & 0x3FF].reshape(8, 8)
            if v & 0x400:
                t = t[:, ::-1]
            if v & 0x800:
                t = t[::-1]
            p = pals[(v >> 12) - PAL_BASE] if v else pals[0]
            rgb = np.array(p, np.uint8)[t]
            rgb[t == 0] = (0, 0, 0)
            img.paste(Image.fromarray(rgb), ((i % w) * 8, (i // w) * 8))
        return img


# ------------------------------------------------------------------ sprites
def save_sprite(name, img, bg=KEY, prefix='gym_'):
    """img: PIL RGB met KEY als doorzichtig; max. 15 kleuren. Schrijft gym_<name>.png/.pal (4bpp-tiles in 8x8-volgorde
    zoals gbagfx ze uit een png van w x h leest)."""
    a = np.array(img.convert('RGB'))
    cols = []
    for c in map(tuple, a.reshape(-1, 3)):
        c = gba(c)
        if c != gba(bg) and c not in cols:
            cols.append(c)
    assert len(cols) <= 15, (name, len(cols))
    pal = [(0, 0, 0)] + cols + [(0, 0, 0)] * (15 - len(cols))
    out = Image.new('P', img.size)
    px = out.load()
    for y in range(img.height):
        for x in range(img.width):
            c = gba(a[y, x])
            px[x, y] = 0 if c == gba(bg) else cols.index(c) + 1
    out.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    out.save(OUT + '%s%s.png' % (prefix, name))
    with open(OUT + '%s%s.pal' % (prefix, name), 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n16\n')
        for c in pal:
            fp.write('%d %d %d\n' % c)
    return pal


def preview_strip(images, path, k=2, cols=4):
    W = Image.new('RGB', (240 * cols, 160 * ((len(images) + cols - 1) // cols)), (40, 40, 40))
    for i, im in enumerate(images):
        W.paste(im, ((i % cols) * 240, (i // cols) * 160))
    scale(W, k).save(path)
