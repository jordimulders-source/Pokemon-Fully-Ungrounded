"""Gedeelde hulpfuncties voor de sprite-studie en -controles (Fully Ungrounded).

Sprites staan als 4bpp-PNG (modus P, 16 kleuren, index 0 = transparant) in
graphics/pokemon/<soort>/. Twee sets:
  'gba' = anim_front_gba.png / back_gba.png / normal_gba.pal: de originele
          Ruby/Sapphire/Emerald- (en FRLG-)sprites; staat in de game UIT
          (P_GBA_STYLE_SPECIES_GFX = FALSE).
  'new' = anim_front.png / back.png / normal.pal: wat de game nu toont
          (DPPt/HGSS/BW-sprites, door expansion naar 64x64/16 kleuren gezet).
"""
import os, colorsys
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
GFX = os.path.join(ROOT, 'graphics', 'pokemon')


def hoenn_species():
    """De 202 soorten van de Hoenn-dex (HOENN_DEX_TREECKO..DEOXYS), mapnamen."""
    txt = open(os.path.join(ROOT, 'include/constants/pokedex.h')).read()
    i = txt.index('HOENN_DEX_TREECKO'); j = txt.index('HOENN_DEX_DEOXYS', i)
    out = []
    import re
    for m in re.finditer(r'HOENN_DEX_([A-Z_]+)', txt[i:j + 30]):
        s = m.group(1).lower()
        if s not in out and os.path.exists(os.path.join(GFX, s, 'back_gba.png')):
            out.append(s)
    return out


def read_pal(path):
    lines = open(path).read().split('\n')
    n = int(lines[2])
    return [tuple(int(v) for v in lines[3 + k].split()[:3]) for k in range(n)]


def load_png(path):
    im = Image.open(path)
    assert im.mode == 'P', path
    a = np.array(im)
    p = im.getpalette()[:48]
    pal = [tuple(p[3 * k:3 * k + 3]) for k in range(16)]
    return a, pal


def front_path(sp, which='gba'):
    d = os.path.join(GFX, sp)
    names = (['anim_front_gba.png', 'front_gba.png'] if which == 'gba'
             else ['anim_front.png', 'front.png'])
    for n in names:
        if os.path.exists(os.path.join(d, n)):
            return os.path.join(d, n)
    return None


def normal_pal(sp, which='gba'):
    """Het echte normale palet (het in de PNG ingebedde palet is soms de shiny)."""
    d = os.path.join(GFX, sp)
    for n in (['normal_gba.pal', 'normal.pal'] if which == 'gba' else ['normal.pal']):
        if os.path.exists(os.path.join(d, n)):
            return read_pal(os.path.join(d, n))
    return None


def load_front(sp, which='gba'):
    """-> (lijst frames als 64x64 indexarrays, palet)."""
    a, pal = load_png(front_path(sp, which))
    pal = normal_pal(sp, which) or pal
    frames = [a[k * 64:(k + 1) * 64] for k in range(a.shape[0] // 64)]
    return frames, pal


def load_back(sp, which='gba'):
    n = 'back_gba.png' if which == 'gba' else 'back.png'
    a, pal = load_png(os.path.join(GFX, sp, n))
    pal = normal_pal(sp, which) or pal
    return a[:64], pal


def load_icon(sp, which='gba'):
    n = 'icon_gba.png' if which == 'gba' else 'icon.png'
    p = os.path.join(GFX, sp, n)
    if not os.path.exists(p):
        return None, None
    im = Image.open(p).convert('RGBA')
    return np.array(im), None


def rgb_img(idx, pal, bg=(0, 0, 0, 0)):
    h, w = idx.shape
    out = np.zeros((h, w, 4), np.uint8)
    for k in range(16):
        m = idx == k
        if k == 0:
            out[m] = bg
        else:
            out[m] = (*pal[k], 255)
    return Image.fromarray(out, 'RGBA')


def lum(c):
    r, g, b = [v / 255 for v in c]
    return 0.299 * r + 0.587 * g + 0.114 * b


def hsl(c):
    r, g, b = [v / 255 for v in c]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s, l


def bbox(mask):
    ys, xs = np.nonzero(mask)
    if len(ys) == 0:
        return None
    return xs.min(), ys.min(), xs.max(), ys.max()


def edge_mask(mask):
    """Opake pixels die (4-buren) aan transparant of de rand grenzen."""
    p = np.pad(mask, 1, constant_values=False)
    nb = p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    return mask & ~nb


def checker_bg(w, h, s=4, c1=(232, 232, 232), c2=(208, 208, 208)):
    yy, xx = np.mgrid[0:h, 0:w]
    m = ((yy // s + xx // s) % 2).astype(bool)
    a = np.zeros((h, w, 4), np.uint8)
    a[m] = (*c1, 255); a[~m] = (*c2, 255)
    return Image.fromarray(a, 'RGBA')


def scaled(img, z):
    return img.resize((img.width * z, img.height * z), Image.NEAREST)
