#!/usr/bin/env python3
"""Project Grounded: gevechtsintro van Wario (Yoshi's Island-fort en Battle Stadium), v2 in WarioWare-stijl.

Jordi: "doe de hele intro opnieuw en maak het heel goofy en Wario Ware achtig", "kijk in Wario Ware naar de filmpjes
die er al in zitten", "Wario moet echt als een soort gekke superheld/alleskunner uit de intro komen".
Een razendsnelle reeks microgames: elke kaart heeft een opdracht in grote letters, een bom met een brandende lont
onderin (de WarioWare-timer) en een Wario-moment uit de filmpjes van WarioWare, Inc.:
  EAT!     Wario op de bank (openingsfilm) eet een knoflookbol in drie happen
  INVENT!  Wario aan zijn bureau met dollartekens in zijn ogen en het Game-idee in een denkwolk (openingsfilm)
  FLY!     Wario die door de lucht vliegt (verhaal na het naam invoeren)
  FLEX!    de dubbele biceps (Wario Land-art, al in de game; Jordi: "die flex is wel goed")
  WIN!     de grote close-up-grijns (de "Think you can beat my games?"-scène); de lont is op: BOEM
en dan de W als superheldenembleem die het beeld overneemt.

Art: de WarioWare-art is schoon uit VRAM/OAM/BG gerenderd (tools/grounded/warioware_rip.py) en staat in
graphics/grounded/trainers/guests/warioware/. Grote Wario-sprites zijn 128 x 128-objecten van vier 64x64-sprites, elk
kwadrant met zijn eigen palet (de WarioWare-sprites hebben tot 22 kleuren).

Uitvoer (graphics/battle_transitions/): wario_intro (kaarten + close-up, BG-palet 10-15), wario_crest (het embleem,
BG-palet 13-15 met een draaiende stralenkrans), wario_<sprite>.png/.pal.
Gebruik: python3 tools/grounded/wario_intro.py [voorbeeldmap]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
from gym_intro_lib import Encoder, text, text_width, preview_strip, OUT, KEY, gba, ROOT
from legend_intros2 import EncoderN, quantize3, write_pal

PREVIEW = sys.argv[1] if len(sys.argv) > 1 else None
SRC = os.path.join(ROOT, 'graphics/grounded/trainers/guests/')
WW = SRC + 'warioware/'

# ------------------------------------------------------------------ hulpjes
def rgba(name):
    return np.array(Image.open(WW + name + '.png').convert('RGBA'))


def grow(m, n):
    g = m.copy()
    for _ in range(n):
        g = g | np.roll(g, 1, 0) | np.roll(g, -1, 0) | np.roll(g, 1, 1) | np.roll(g, -1, 1)
    return g


def paste(a, src, x, y):
    """RGBA-art op een RGB-beeld (alleen dekkende pixels)."""
    h, w = min(src.shape[0], a.shape[0] - y), min(src.shape[1], a.shape[1] - x)
    s = src[:h, :w]
    m = s[:, :, 3] > 0
    a[y:y + h, x:x + w][m] = s[:, :, :3][m]


def word(a, s, cx, y, scale=3, fg=(248, 248, 248), edge=(16, 16, 16), shadow=(16, 16, 16)):
    """Een opdracht in grote letters: wit met een dikke zwarte rand (de WarioWare-opdrachten)."""
    tmp = Image.new('RGB', (240, 60), KEY)
    sp = 1
    text(tmp, cx - text_width(s, 'normal', scale, sp) // 2, 0, s, fg, None, 'normal', scale, sp)
    t = np.array(tmp)
    m = ~(t == np.array(KEY)).all(2)
    m = m[:max(1, 60 - 0)]
    hgt = min(60, a.shape[0] - y)
    reg = a[y:y + hgt]
    mm = m[:hgt]
    reg[grow(mm, 3) & ~mm] = edge
    sh = np.roll(np.roll(mm, 3, 0), 3, 1)
    reg[sh & ~grow(mm, 3)] = shadow
    reg[mm] = fg


def bar(a, fuse=True):
    """De WarioWare-timer onderin: zwarte balk, bom links, lont naar rechts."""
    a[144:160] = (16, 16, 16)
    paste(a, rgba('bombonly'), 4, 144)
    if fuse:
        f = rgba('fuse')
        for x in range(34, 236, 32):
            paste(a, f[:, :min(32, 236 - x)], x, 150)


def card(pattern, cmd):
    a = pattern.copy()
    word(a, cmd, 120, 4)
    bar(a)
    return a


def stripes(c1, c2, w=12):
    yy, xx = np.mgrid[0:160, 0:240]
    a = np.zeros((160, 240, 3), np.uint8)
    m = ((xx + yy) // w) % 2 == 0
    a[m], a[~m] = c1, c2
    return a


def dots(c1, c2, r=5, step=24):
    yy, xx = np.mgrid[0:160, 0:240]
    a = np.zeros((160, 240, 3), np.uint8)
    a[:] = c1
    ox = (yy // step % 2) * step // 2
    m = (((xx + ox) % step - step // 2) ** 2 + (yy % step - step // 2) ** 2) < r * r
    a[m] = c2
    return a


def checker(c1, c2, s=16):
    yy, xx = np.mgrid[0:160, 0:240]
    a = np.zeros((160, 240, 3), np.uint8)
    m = ((xx // s + yy // s) % 2) == 0
    a[m], a[~m] = c1, c2
    return a


def sky():
    a = np.zeros((160, 240, 3), np.uint8)
    for y in range(160):
        a[y] = (40, 72, 232) if (y // 16) % 2 == 0 else (64, 104, 240)
    # snelheidslijnen
    rnd = np.random.RandomState(4)
    for k in range(18):
        y, x, L = rnd.randint(30, 140), rnd.randint(0, 200), rnd.randint(24, 60)
        a[y:y + 2, x:x + L] = (232, 240, 248)
    return a


# ------------------------------------------------------------------ BG-set A: vier kaarten, de lege balk, de close-up
def set_a():
    cards = [card(stripes((248, 152, 32), (248, 200, 56)), 'EAT!'),
             card(dots((56, 184, 88), (120, 232, 136)), 'INVENT!'),
             card(sky(), 'FLY!'),
             card(checker((248, 120, 200), (192, 40, 136)), 'FLEX!')]
    empty = cards[0].copy()
    bar(empty, fuse=False)
    f = rgba('face')
    face = f[:, :, :3].copy()
    # de blauwe verloopachtergrond is in WarioWare een HBlank-effect (geen tiles): hier één effen blauw
    BLUE = (40, 72, 184)
    face[f[:, :, 3] == 0] = BLUE
    face[(face == 0).all(2)] = (8, 8, 8)   # zuiver zwart is in BG-beelden doorzichtig
    WIN = [(248, 224, 48), (96, 24, 136), (16, 16, 16)]
    word(face, 'WIN!', 206, 4, scale=2, fg=WIN[0], edge=WIN[1], shadow=WIN[2])
    imgs = cards + [empty, face]

    def cols(arrs, box=None):
        out = []
        for x in arrs:
            x = x if box is None else x[box[1]:box[3], box[0]:box[2]]
            for c in map(tuple, x.reshape(-1, 3)):
                c = gba(c)
                if c not in out:
                    out.append(c)
        return out
    face_cols = cols([face[f[:, :, 3] > 0].reshape(1, -1, 3)]) + [gba(BLUE)]
    bar_cols = cols(cards + [empty], (0, 144, 240, 160))
    c01 = cols(cards[0:2], (0, 0, 240, 144))
    c23 = cols(cards[2:4], (0, 0, 240, 144))
    pals = [face_cols, [gba(BLUE)] + [gba(c) for c in WIN], c01, c23, bar_cols, [(248, 248, 248)]]
    for p_ in pals:
        assert len(p_) <= 15, (len(p_), p_)
    enc = EncoderN('intro', pals, 10, prefix='wario_')
    for im, lbl in zip(imgs, ['eat', 'invent', 'fly', 'flex', 'balk', 'close-up']):
        enc.add(Image.fromarray(im), None, lbl)
    enc.save()
    return [enc.render(m) for m in enc.maps]


# ------------------------------------------------------------------ BG-set B: het embleem (palet 13-15)
PHASES = [(8 + i * 24, 200, 16 + i * 8) for i in range(8)]
WCOL = [(248, 224, 48), (248, 248, 160), (224, 160, 24), (128, 48, 168), (72, 16, 104), (32, 8, 40), (248, 248, 248)]


def burst():
    yy, xx = np.mgrid[0:160, 0:240]
    ang = np.arctan2(yy - 79.5, xx - 119.5)
    ph = (((ang / (2 * math.pi) + 1) * 16).astype(int) % 16) % 8
    ph[:, 120:] = ph[:, :120][:, ::-1]
    ph[80:] = ph[:80][::-1]
    a = np.zeros((160, 240, 3), np.uint8)
    for i in range(8):
        a[ph == i] = PHASES[i]
    return a


def crest(scale):
    """De W als superheldenembleem: een geel schild met een paarse rand en een paarse W erin."""
    a = burst()
    yy, xx = np.mgrid[0:160, 0:240]
    S = [(-62, -46), (62, -46), (84, -16), (0, 62), (-84, -16)]
    W = [(-50, -30), (-30, -30), (-20, 4), (-8, -30), (8, -30), (20, 4), (30, -30), (50, -30), (26, 30), (10, 30),
         (0, 2), (-10, 30), (-26, 30)]

    def poly(pts):
        im = Image.new('L', (240, 160), 0)
        ImageDraw.Draw(im).polygon([(120 + x * scale, 76 + y * scale) for x, y in pts], fill=255)
        return np.array(im) > 0
    sh, w = poly(S), poly(W)
    o = max(2, int(4 * scale))
    a[grow(sh, o + 2) & ~grow(sh, o)] = WCOL[5]
    a[grow(sh, o) & ~sh] = WCOL[3]
    a[sh] = WCOL[0]
    a[sh & (yy < 76 - 30 * scale)] = WCOL[1]
    a[sh & (yy > 76 + 30 * scale)] = WCOL[2]
    a[grow(w, max(1, o // 2)) & ~w & sh] = WCOL[5]
    a[w] = WCOL[3]
    a[w & (yy < 76 - 18 * scale)] = WCOL[4] if False else WCOL[3]
    return a


def set_b():
    enc = Encoder('crest', [PHASES, PHASES + WCOL, PHASES + WCOL], prefix='wario_')
    imgs = [crest(1.0), crest(2.4), crest(6.0)]
    for im, lbl in zip(imgs, ['embleem', 'groot', 'reus']):
        enc.add(Image.fromarray(im), None, lbl)
    enc.save()
    return imgs


# ------------------------------------------------------------------ sprites
def big_sheet(name, arts, crop_bottom=0):
    """Grote objecten (128 x 128, kwadranten LB/RB/LO/RO onder elkaar), elk kwadrant met een eigen palet van 15 kleuren
    (samen max. 4 paletten; alle arts in dezelfde sheet delen die vier paletten)."""
    canvases = []
    for a in arts:
        if crop_bottom:
            a = a[:a.shape[0] - crop_bottom]
        h, w = a.shape[:2]
        assert h <= 128 and w <= 128, (name, a.shape)
        c = np.zeros((128, 128, 4), np.uint8)
        c[128 - h:, 64 - w // 2:64 - w // 2 + w] = a
        canvases.append(c)
    pals = []
    for q in range(4):
        qs = [c[(q >> 1) * 64:(q >> 1) * 64 + 64, (q & 1) * 64:(q & 1) * 64 + 64] for c in canvases]
        px = np.concatenate([x[x[:, :, 3] > 0][:, :3] for x in qs] + [np.zeros((0, 3), np.uint8)])
        cols = []
        for c in map(tuple, (px >> 3 << 3)):
            if c not in cols:
                cols.append(c)
        if len(cols) > 15:   # te veel kleuren in dit kwadrant: median cut
            im = Image.fromarray(px.reshape(1, -1, 3).astype(np.uint8)).quantize(15, method=Image.Quantize.MEDIANCUT)
            p = im.getpalette()[:45]
            cols = [gba(p[i * 3:i * 3 + 3]) for i in range(15)]
            print('  %s kwadrant %d: %d kleuren -> 15' % (name, q, len(set(map(tuple, px >> 3 << 3)))))
        pals.append(cols)
    sheet = []
    for c in canvases:
        for q in range(4):
            sub = c[(q >> 1) * 64:(q >> 1) * 64 + 64, (q & 1) * 64:(q & 1) * 64 + 64]
            idx = np.zeros((64, 64), np.uint8)
            m = sub[:, :, 3] > 0
            P = np.array(pals[q], np.int32)
            g = (sub[:, :, :3].astype(np.int32) >> 3) << 3
            d = ((g[:, :, None, :] - P[None, None]) ** 2).sum(3)
            idx[m] = d.argmin(2)[m] + 1
            # geen gaten: elke dekkende pixel krijgt een kleur (index > 0)
            assert (idx[m] > 0).all()
            sheet.append(idx)
    im = Image.fromarray(np.concatenate(sheet, 0), 'P')
    full = []
    for p in pals:
        full += [(0, 0, 0)] + list(p) + [(0, 0, 0)] * (15 - len(p))
    im.putpalette([v for c in full[:16] for v in c] + [0] * (768 - 48))
    im.save(OUT + 'wario_%s.png' % name)
    write_pal(OUT + 'wario_%s.pal' % name, full)
    return [big_preview(np.concatenate(sheet[k * 4:k * 4 + 4], 0), full) for k in range(len(arts))]


def big_preview(sheet, full):
    q = [sheet[i * 64:(i + 1) * 64] for i in range(4)]
    out = np.zeros((128, 128, 3), np.uint8)
    out[:] = (255, 0, 255)
    for i in range(4):
        pal = np.array(full[i * 16:(i + 1) * 16], np.uint8)
        rgb = pal[q[i]]
        m = q[i] > 0
        out[(i >> 1) * 64:(i >> 1) * 64 + 64, (i & 1) * 64:(i & 1) * 64 + 64][m] = rgb[m]
    return Image.fromarray(out)


def small_sheet(name, frames, size):
    """Kleine sprite (size x size), frames onder elkaar, één palet."""
    cols = []
    for a in frames:
        for c in map(tuple, (a[a[:, :, 3] > 0][:, :3] >> 3 << 3)):
            if c not in cols:
                cols.append(c)
    assert len(cols) <= 15, (name, len(cols))
    out = []
    for a in frames:
        c = np.zeros((size, size), np.uint8)
        h, w = a.shape[:2]
        y0, x0 = (size - h) // 2, (size - w) // 2
        rgb = (a[:, :, :3] >> 3) << 3
        for i, col in enumerate(cols):
            m = (rgb == np.array(col)).all(2) & (a[:, :, 3] > 0)
            c[y0:y0 + h, x0:x0 + w][m] = i + 1
        out.append(c)
    im = Image.fromarray(np.concatenate(out, 0), 'P')
    pal = [(0, 0, 0)] + cols + [(0, 0, 0)] * (15 - len(cols))
    im.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    im.save(OUT + 'wario_%s.png' % name)
    write_pal(OUT + 'wario_%s.pal' % name, pal)


GARLIC = [(248, 240, 216), (248, 248, 248), (200, 168, 216), (144, 104, 176), (200, 168, 112), (64, 32, 80)]


def garlic_frames():
    """Een kleine knoflookbol (32 x 32) met 0-3 happen: geen Pokémon of personage, dus met de hand getekend."""
    out = []
    for bites in range(4):
        im = Image.new('L', (32, 32), 0)
        d = ImageDraw.Draw(im)
        d.ellipse((5, 10, 27, 29), fill=255)
        d.polygon([(10, 13), (16, 2), (22, 13)], fill=255)
        m = np.array(im) > 0
        yy, xx = np.mgrid[0:32, 0:32]
        for bx, by, r in [(26, 10, 7), (5, 18, 7), (17, 18, 9)][:bites]:
            ang = np.arctan2(yy - by, xx - bx)
            m &= (xx - bx) ** 2 + (yy - by) ** 2 >= (r + 1.2 * np.cos(ang * 7)) ** 2
        a = np.zeros((32, 32, 4), np.uint8)
        a[m] = GARLIC[0] + (255,)
        for x0 in (11, 16, 21):
            ln = m & (np.abs(xx - x0) < 1) & (yy > 11)
            a[ln] = GARLIC[3] + (255,)
        a[m & ((xx - 11) ** 2 + (yy - 16) ** 2 < 6)] = GARLIC[1] + (255,)
        for k in range(-2, 3):
            if m[27, 16 + k * 3]:
                a[29:31, 16 + k * 3] = GARLIC[4] + (255,)
        solid = a[:, :, 3] > 0
        a[grow(solid, 1) & ~solid] = GARLIC[5] + (255,)
        out.append(a)
    return out


def flex():
    """De dubbele biceps uit de Wario Land-art (wario_flex_bron) op 3x met Scale3x, zoals in v1."""
    from guest_trainer_pics import scale3x
    a = np.array(Image.open(SRC + 'wario_flex_bron.png').convert('RGBA'))
    big = np.array(scale3x(Image.fromarray(a, 'RGBA')))
    cols_used = np.where((big[:, :, 3] > 0).any(0))[0]
    big = big[:, cols_used[0]:cols_used[-1] + 1]
    if big.shape[1] > 128:
        o = (big.shape[1] - 128) // 2
        big = big[:, o:o + 128]
    return big


def sprites():
    prev = []
    prev += big_sheet('couch', [rgba('couch_a')])
    prev += big_sheet('cash', [rgba('idea_cash')], crop_bottom=12)     # onderkant van de stoel eraf: 128 hoog
    prev += big_sheet('fly', [rgba('fly_a'), rgba('fly_b')])
    prev += big_sheet('flex', [flex()])
    small_sheet('garlic', garlic_frames(), 32)
    small_sheet('spark', [rgba('spark')], 16)
    small_sheet('boom', [rgba('boom')], 64)
    return prev


def main():
    a = set_a()
    b = set_b()
    s = sprites()
    if PREVIEW:
        preview_strip(a + [Image.fromarray(x) for x in b], os.path.join(PREVIEW, 'wario_intro_bg.png'), k=2, cols=3)
        W = Image.new('RGB', (len(s) * 132, 128), (40, 40, 40))
        for i, im in enumerate(s):
            W.paste(im, (i * 132, 0))
        W.resize((W.width * 2, W.height * 2), Image.NEAREST).save(os.path.join(PREVIEW, 'wario_intro_sprites.png'))


if __name__ == '__main__':
    main()
