"""Project Grounded: kleine hulpjes om bestaande game-graphics als RGB-beeld te tekenen (voor filmtransities):
gevechtsachtergronden (tiles + tilemap + palet), Pokémon- en trainerplaatjes met hun palet, en tekst in het
gamelettertype."""
import os, re, struct
import numpy as np
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))


def jasc(path):
    lines = open(path).read().split()
    n = int(lines[2])
    v = list(map(int, lines[3:3 + n * 3]))
    return [tuple(v[i * 3:i * 3 + 3]) for i in range(n)]


def battle_env(name, w=30, h=20):
    """Gevechtsachtergrond graphics/battle_environment/<name> als RGB (h*8 x w*8), linksboven in de tilemap."""
    d = os.path.join(ROOT, 'graphics/battle_environment', name)
    tiles = np.array(Image.open(os.path.join(d, 'tiles.png')))
    pal = jasc(os.path.join(d, 'palette.pal'))
    raw = open(os.path.join(d, 'map.bin'), 'rb').read()
    m = struct.unpack('<%dH' % (len(raw) // 2), raw)
    pals = [v >> 12 for v in m]
    base = 2                      # het gevecht laadt het palet op BG-palet 2
    tw = tiles.shape[1] // 8
    out = np.zeros((h * 8, w * 8, 3), np.uint8)
    P = np.array(pal + [(0, 0, 0)] * 64, np.uint8)
    for r in range(h):
        for c in range(w):
            v = m[r * 32 + c]
            t = v & 0x3FF
            ty, tx = divmod(t, tw)
            blk = tiles[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            if v & 0x400:
                blk = blk[:, ::-1]
            if v & 0x800:
                blk = blk[::-1, :]
            pi = max(0, (v >> 12) - base) * 16
            idx = np.where((blk & 15) == 0, 1, pi + (blk & 15))   # index 0 = achtergrond (lichtste kleur)
            out[r * 8:r * 8 + 8, c * 8:c * 8 + 8] = P[idx]
    return out


def sprite(path, pal_path=None, frame=0, size=64):
    """Een 4bpp-plaatje (index 0 = doorzichtig) als RGBA; frame = welk 64x64-frame (anim_front heeft er twee)."""
    im = Image.open(os.path.join(ROOT, path))
    a = np.array(im)
    a = a[frame * size:(frame + 1) * size]
    if pal_path:
        pal = jasc(os.path.join(ROOT, pal_path))
    else:
        p = im.getpalette()
        pal = [tuple(p[i * 3:i * 3 + 3]) for i in range(16)]
    P = np.array(pal[:16] + [(0, 0, 0)] * (16 - len(pal[:16])), np.uint8)
    out = np.zeros(a.shape + (4,), np.uint8)
    out[..., :3] = P[a & 15]
    out[..., 3] = np.where(a == 0, 0, 255)
    return Image.fromarray(out, 'RGBA')


_CM = None


def _charmap():
    global _CM
    if _CM is None:
        _CM = {}
        for line in open(os.path.join(ROOT, 'charmap.txt'), encoding='utf-8'):
            m = re.match(r"^'(.|…)'\s*=\s*([0-9A-F]{2})\s*(@.*)?$", line.strip())
            if m and m.group(1) not in _CM:
                _CM[m.group(1)] = int(m.group(2), 16)
        _CM['é'] = _CM.get('é', 0x1B)
    return _CM


_FONTS = {}


def font(name='normal'):
    if name not in _FONTS:
        arr = {'normal': 'gFontNormalLatinGlyphWidths', 'narrow': 'gFontNarrowLatinGlyphWidths',
               'small': 'gFontSmallLatinGlyphWidths', 'short': 'gFontShortLatinGlyphWidths'}[name]
        src = open(os.path.join(ROOT, 'src/fonts.c')).read().split('const u8 %s[] = {' % arr)[1].split('};')[0]
        widths = [int(v, 0) for v in re.findall(r'0x[0-9A-Fa-f]+|\d+', src)]
        img = np.array(Image.open(os.path.join(ROOT, 'graphics/fonts/latin_%s.png' % name)))
        _FONTS[name] = (img, widths)
    return _FONTS[name]


def text(img, x, y, s, fg, shadow=None, name='normal'):
    """Tekent tekst in het gamelettertype op een RGB-array (fg = letter, shadow = schaduw). Geeft de eindpositie x."""
    glyphs, widths = font(name)
    cm = _charmap()
    for ch in s:
        g = cm.get(ch, 0)
        gx, gy = (g % 16) * 16, (g // 16) * 16
        for yy in range(16):
            for xx in range(widths[g]):
                v = glyphs[gy + yy, gx + xx]
                px, py = x + xx, y + yy
                if 0 <= px < img.shape[1] and 0 <= py < img.shape[0]:
                    if v == 1:
                        img[py, px] = fg
                    elif v == 2 and shadow is not None:
                        img[py, px] = shadow
        x += widths[g]
    return x
