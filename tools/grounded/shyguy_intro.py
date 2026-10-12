#!/usr/bin/env python3
"""Project Grounded: gevechtsintro van de Shy Guys (Shy Squad op Yoshi's Island, de Stadium-Shy Guys, de Shy Guy in de
woestijn), op de maat van Sunset Wilds (src/data/shyguy_intro.h).

Jordi: "Shy Guy gevechtsintro mag op de maat van Sunset Wilds, lekker droog diverse soorten shy guys uit Yoshi's Island
die op een level staan, vervolgens draait er 1 om van oh shit het is mijn beurt om te vechten. Gebruik net als bij Wario
de rom als bron en maak het humoristisch".

Art, alles uit Super Mario Advance 3: Yoshi's Island:
- het level (begin van 1-1) en het hint-bord met zijn letters: schoon uit VRAM/OAM gerenderd door
  tools/grounded/yi_shyguy_rip.py (graphics/grounded/yoshis_island/shyguy_intro/);
- de Shy Guys: het spriteblad 'Game Boy Advance - Super Mario Advance 3_ Yoshi's Island - Enemies - Shy Guy.png'
  (in graphics/, door A.J. Nitro uit dezelfde ROM geript): gewone Shy Guys (rood, geel), een Stilt Guy (groen), een
  Fat Guy (roze), een Spear Guy, een Shy Guy in een struik, een Fly Guy (groen) en de grote Shy Guy voor de close-up;
- het '!' boven zijn hoofd is het echte Pokémon-uitroepteken (graphics/field_effects/pics/emotion_exclamation.png).

Uitvoer (graphics/battle_transitions/): shyguy_intro (BG0: het level, en het level met het bord; BG-palet 10-15),
shyguy_s32 / shyguy_s64 / shyguy_big (sprites 32x32, 32x64, 64x32) met één gedeeld palet-bestand shyguy_obj.pal, en
src/data/shyguy_intro_gen.h (framenummers en het palet per frame).
Gebruik: python3 tools/grounded/shyguy_intro.py [voorbeeldmap]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from gym_intro_lib import OUT, KEY, gba, ROOT, preview_strip
from legend_intros2 import EncoderN, quantize3, write_pal

PREVIEW = sys.argv[1] if len(sys.argv) > 1 else None
RIP = os.path.join(ROOT, 'graphics/grounded/yoshis_island/shyguy_intro/')
SHEET = os.path.join(ROOT, "graphics/Game Boy Advance - Super Mario Advance 3_ Yoshi's Island - Enemies - Shy Guy.png")
PINK, GREEN, YELLOW = 315, 631, 946      # verticale afstand van de kleurblokken op het blad (rood staat bovenaan)
BOARD_POS = (40, 4)
BOARD_TEXT = ["Wait.", "It's my turn."]

_sheet = np.array(Image.open(SHEET).convert('RGBA'))
_bgcol = _sheet[0, 0, :3]


def cut(x, y, w, h, dy=0):
    """Een sprite van het blad (achtergrond doorzichtig), kleuren al naar GBA (5 bits)."""
    a = _sheet[y + dy:y + dy + h, x:x + w].copy()
    m = (a[:, :, :3] == _bgcol).all(2) | (a[:, :, 3] == 0)
    a[:, :, :3] = (a[:, :, :3] >> 3) << 3
    a[m] = 0
    a[~m, 3] = 255
    ys, xs = np.where(a[:, :, 3] > 0)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def stilt(x0, x1, y0, y1, dy):
    """Een Stilt Guy (lijf en stelten zijn losse stukken op het blad); de stelten worden korter (58 px hoog, anders past hij
    niet in een sprite van 64 px)."""
    a = cut(x0, y0, x1 - x0, y1 - y0, dy)
    cnt = (a[:, :, 3] > 0).sum(1)
    legs = [y for y in range(a.shape[0] // 2, a.shape[0] - 10) if cnt[y] <= 8]
    n = a.shape[0] - 58
    if n > 0:
        assert len(legs) >= n, (len(legs), n)
        mid = legs[(len(legs) - n) // 2:(len(legs) - n) // 2 + n]
        a = np.delete(a, mid, 0)
    return a


SMALL = [(8, 16, 18, 21), (29, 16, 18, 21), (50, 16, 18, 21), (71, 17, 18, 20), (92, 19, 23, 18)]
BIG = (8, 205, 39, 30)
SPEAR_FRONT = (312, 1343, 25, 34)    # de Spear Guy die recht in de camera kijkt (armen wijd)
FLY = [(x, 120, 18, 29) for x in (8, 29, 50, 71)]


def achromatic(row):
    px = row[row[:, 3] > 0][:, :3].astype(int)
    return len(px) == 0 or (np.abs(px[:, 0] - px[:, 1]).max() < 24 and np.abs(px[:, 1] - px[:, 2]).max() < 24)


def flyturn(i):
    """Een roze Fly Guy van voren, verschrikt: het lijf van de verschrikte roze Shy Guy (frame 4) met de propeller van
    de roze Fly Guy (stand i) erop. Het blad heeft geen Fly Guy van voren."""
    body = cut(92, 19, 23, 18, PINK)
    fly = cut(*FLY[i], dy=PINK)
    n = 0
    while achromatic(fly[n]):
        n += 1
    prop = fly[:n]
    ys, xs = np.where(prop[:, :, 3] > 0)
    shaft = prop[n - 1, :, 3] > 0                      # onderste rij van de propeller = de as
    sx = int(np.where(shaft)[0].mean())
    top = np.where(body[0, :, 3] > 0)[0]
    bx = int(top.mean())                               # midden van de capuchon
    w = max(body.shape[1], bx - sx + prop.shape[1], prop.shape[1]) + abs(min(0, bx - sx))
    off = max(0, sx - bx)
    out = np.zeros((n + body.shape[0], w + off, 4), np.uint8)
    out[n:, off:off + body.shape[1]] = body
    px = off + bx - sx
    m = prop[:, :, 3] > 0
    out[:n, px:px + prop.shape[1]][m] = prop[m]
    ys, xs = np.where(out[:, :, 3] > 0)
    return out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


# ------------------------------------------------------------------ de cast
def cast():
    """Per figuur: lijst frames (RGBA, voeten onderaan). Kijkrichting op het blad: zie FACING in shyguy_intro.h."""
    c = {}
    c['red'] = [cut(*b) for b in SMALL]                       # staan, 3x lopen, verschrikt (van voren)
    c['yellow'] = [cut(*b, dy=YELLOW) for b in SMALL[:4]]
    c['fly'] = [cut(*b, dy=GREEN) for b in FLY]   # propeller draait
    c['bush'] = [cut(8, 253, 26, 19), cut(66, 247, 26, 25), cut(95, 244, 26, 28), cut(124, 244, 26, 28)]
    c['spear'] = [cut(207, 1343, 21, 33), cut(233, 1343, 24, 33)]       # dansen
    c['fat'] = [cut(x, y, w, h, PINK) for x, y, w, h in
                [(371, 231, 27, 34), (433, 233, 29, 32)]]   # twee stappen (OBJ-VRAM is krap)
    xs = [371, 399, 425, 451, 476, 501, 525, 549, 575]
    # van voren -> opzij (rechts) in vijf standen (0, 1, 3, 5, 7 van de acht op het blad)
    c['stilt'] = [stilt(xs[i] - 1, xs[i + 1] - 1, 2, 78, GREEN) for i in (0, 1, 3, 5, 7)]
    c['big'] = [cut(*BIG)]
    # de gekozen Shy Guy als hij een Fly Guy (roze) of Spear Guy is: zijn 'van voren, verschrikt'-frames
    c['flyturn'] = [flyturn(i) for i in (0, 2)]
    c['spearturn'] = [cut(*SPEAR_FRONT)]
    ex = Image.open(os.path.join(ROOT, 'graphics/field_effects/pics/emotion_exclamation.png'))
    pal = ex.getpalette()[:48]
    idx = np.array(ex)
    e = np.zeros(idx.shape + (4,), np.uint8)
    for i in range(1, 16):
        e[idx == i, :3] = gba(pal[i * 3:i * 3 + 3])
        e[idx == i, 3] = 255
    ys, xs_ = np.where(e[:, :, 3] > 0)
    c['excl'] = [e[ys.min():ys.max() + 1, xs_.min():xs_.max() + 1]]
    return c


SHAPE = {'red': 32, 'yellow': 32, 'fly': 32, 'bush': 32, 'excl': 32, 'flyturn': 32, 'spear': 64, 'fat': 64, 'stilt': 64,
         'spearturn': 64, 'big': 'big'}
ORDER = ['red', 'yellow', 'fly', 'bush', 'excl', 'flyturn', 'spear', 'fat', 'stilt', 'spearturn', 'big']

# ------------------------------------------------------------------ de gekozen Shy Guy (src/data/shyguy_intro.h, SG_V_*)
# Per variant een palet voor de gekozen kleine figuur (een omgekleurde kopie van zijn palet) en een voor de grote Shy Guy
# van de close-up. Groen en roze: de echte kleuren van het blad (dezelfde frames in het groene/roze blok, pixel voor
# pixel); zwart staat niet op het blad: grijstinten zoals de trainerfoto (guest_shy_guy_black: 0..136).
VARIANTS = ['RED', 'GREEN', 'PINK', 'BLACK', 'FLY', 'SPEAR']


def sheetmap(src, dst):
    """Kleur -> kleur uit twee reeksen gelijke frames (meerderheid per bronkleur)."""
    from collections import Counter
    cnt = {}
    for a, b in zip(src, dst):
        assert a.shape == b.shape, (a.shape, b.shape)
        m = (a[:, :, 3] > 0) & (b[:, :, 3] > 0)
        for ca, cb in zip(map(tuple, a[m][:, :3]), map(tuple, b[m][:, :3])):
            cnt.setdefault(ca, Counter())[cb] += 1
    return {k: v.most_common(1)[0][0] for k, v in cnt.items()}


def greymap(cols):
    out = {}
    for c in cols:
        L = 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
        g = 0 if L < 16 else min(136, int(24 + L * 112 / 248)) >> 3 << 3
        out[c] = (g, g, g)
    return out


def gbacol(c):
    r, g, b = (int(v) for v in c[:3])
    return (r >> 3) | (g >> 3) << 5 | (b >> 3) << 10


def variant_pals(c, pals, where):
    small = [cut(*b) for b in SMALL]
    big = [cut(*BIG)]
    fly_g, fly_p = [cut(*b, dy=GREEN) for b in FLY], [cut(*b, dy=PINK) for b in FLY]
    maps = {
        'RED': ({}, {}),
        'GREEN': (sheetmap(small, [cut(*b, dy=GREEN) for b in SMALL]), sheetmap(big, [cut(*BIG, dy=GREEN)])),
        'PINK': (sheetmap(small, [cut(*b, dy=PINK) for b in SMALL]), sheetmap(big, [cut(*BIG, dy=PINK)])),
        'BLACK': (greymap(colours(small)), greymap(colours(big))),
        'FLY': (sheetmap(fly_g, fly_p), {}),
        'SPEAR': ({}, {}),
    }
    src = {'FLY': 'fly', 'SPEAR': 'spear'}
    rows = []
    for v in VARIANTS:
        ms, mb = maps[v]
        p = pals[where[src.get(v, 'red')]]
        q = pals[where['big']]
        rows.append([[0] + [gbacol(ms.get(col, col)) for col in p] + [0] * (15 - len(p)),
                     [0] + [gbacol(mb.get(col, col)) for col in q] + [0] * (15 - len(q))])
    return rows


def colours(frames):
    s = set()
    for f in frames:
        s |= set(map(tuple, f[f[:, :, 3] > 0][:, :3]))
    return s


def pack(c):
    """Figuren in zo weinig mogelijk paletten van 15 kleuren (gulzig, grootste eerst)."""
    pals, where = [], {}
    for k in sorted(c, key=lambda k: -len(colours(c[k]))):
        cs = colours(c[k])
        assert len(cs) <= 15, (k, len(cs))
        for i, p in enumerate(pals):
            if len(p | cs) <= 15:
                p |= cs
                where[k] = i
                break
        else:
            pals.append(set(cs))
            where[k] = len(pals) - 1
    return [sorted(p) for p in pals], where


def place(f, w, h):
    """Frame in een vak van w x h: horizontaal in het midden, voeten op de onderrand."""
    out = np.zeros((h, w, 4), np.uint8)
    fh, fw = f.shape[:2]
    assert fh <= h and fw <= w, (f.shape, w, h)
    x0 = (w - fw) // 2
    out[h - fh:, x0:x0 + fw] = f
    return out


def sprites():
    c = cast()
    pals, where = pack({k: v for k, v in c.items() if k != 'big'})
    bp, bw = pack({'big': c['big']})
    where['big'] = len(pals) + bw['big']
    pals += bp
    print('sprites: %d paletten (%s)' % (len(pals), ', '.join('%s=%d' % (k, where[k]) for k in ORDER)))
    sheets = {32: [], 64: [], 'big': []}
    first, palof = {}, []
    for k in ORDER:
        first[k] = (SHAPE[k], len(sheets[SHAPE[k]]))
        for f in c[k]:
            w, h = {32: (32, 32), 64: (32, 64), 'big': (64, 32)}[SHAPE[k]]
            if SHAPE[k] == 'big':
                g = np.zeros((32, 64, 4), np.uint8)       # in het midden (affine: schaalt rond het midden)
                fh, fw = f.shape[:2]
                g[16 - fh // 2:16 - fh // 2 + fh, 32 - fw // 2:32 - fw // 2 + fw] = f
            elif k == 'excl':
                g = np.zeros((32, 32, 4), np.uint8)
                g[8:8 + f.shape[0], 16 - f.shape[1] // 2:16 - f.shape[1] // 2 + f.shape[1]] = f
            else:
                g = place(f, w, h)
            sheets[SHAPE[k]].append((g, where[k]))
    full = []
    for p in pals:
        full += [(0, 0, 0)] + p + [(0, 0, 0)] * (15 - len(p))
    write_pal(OUT + 'shyguy_obj.pal', full)
    prev, counts = [], {}
    for key, name in ((32, 's32'), (64, 's64'), ('big', 'big')):
        idx_frames = []
        for g, pi in sheets[key]:
            P = np.array(pals[pi], np.int32)
            idx = np.zeros(g.shape[:2], np.uint8)
            m = g[:, :, 3] > 0
            d = ((g[:, :, :3].astype(np.int32)[:, :, None] - P[None, None]) ** 2).sum(3)
            idx[m] = d.argmin(2)[m] + 1
            assert (d.min(2)[m] == 0).all()
            idx_frames.append(idx)
            pr = np.zeros(g.shape[:2] + (3,), np.uint8)
            pr[:] = (255, 0, 255)
            pr[m] = g[:, :, :3][m]
            prev.append(Image.fromarray(pr))
        im = Image.fromarray(np.concatenate(idx_frames, 0), 'P')
        im.putpalette([v for col in full[:16] for v in col] + [0] * (768 - 48))
        im.save(OUT + 'shyguy_%s.png' % name)
        print('  shyguy_%s: %d frames' % (name, len(idx_frames)))
        counts[name] = len(idx_frames)
    # framenummers en palet per frame voor C
    lines = ['// Project Grounded: gegenereerd door tools/grounded/shyguy_intro.py (niet met de hand bewerken)',
             '#define SG_NUM_PALS %d' % len(pals)] + ['#define SG_N_%s %d' % (n.upper(), counts[n]) for n in ('s32', 's64', 'big')]
    for k in ORDER:
        lines.append('#define SG_F_%s %d // %s, %d frames' % (k.upper(), first[k][1], {32: 's32', 64: 's64', 'big': 'big'}[first[k][0]], len(c[k])))
    lines.append('#define SG_PAL_%s %d' % ('X', 0))
    for k in ORDER:
        lines.append('#define SG_PAL_%s %d' % (k.upper(), where[k]))
    lines.append('#define SG_H_%s %d' % ('X', 0))
    for k in ORDER:
        lines.append('#define SG_H_%s %d // hoogte van de figuur (frame 0)' % (k.upper(), c[k][0].shape[0]))
    lines.append('// de gekozen Shy Guy: [variant][0] = palet van de kleine figuur, [1] = palet van de grote (close-up)')
    lines.append('enum { %s, SG_NUM_VARIANTS };' % ', '.join('SG_V_' + v for v in VARIANTS))
    lines.append('static const u16 sSG_VarPal[SG_NUM_VARIANTS][2][16] =\n{')
    for v, (a, b) in zip(VARIANTS, variant_pals(c, pals, where)):
        lines.append('    [SG_V_%s] = {' % v)
        for r in (a, b):
            lines.append('        {%s},' % ', '.join('0x%04X' % x for x in r))
        lines.append('    },')
    lines.append('};')
    open(os.path.join(ROOT, 'src/data/shyguy_intro_gen.h'), 'w').write('\n'.join(lines) + '\n')
    return prev


# ------------------------------------------------------------------ BG: het level, en het level met het bord
def font():
    f = np.array(Image.open(RIP + 'font.png')) > 0
    g = {}
    for ln in open(RIP + 'font.txt'):
        ch, x, w = ln.rstrip('\n').split(' ')
        g[ch] = f[:, int(x):int(x) + int(w)]
    return g


def board():
    b = np.array(Image.open(RIP + 'board.png').convert('RGBA'))
    b = np.concatenate([b[:26], b[-26:]], 0)       # twee regels: middenstuk eruit (de rand is een herhalend patroon)
    g = font()
    ink = (248, 248, 248)
    for i, s in enumerate(BOARD_TEXT):
        w = sum(g[ch].shape[1] + 1 if ch != ' ' else 4 for ch in s) - 1
        x = (b.shape[1] - w) // 2
        y = 11 + i * 16
        for ch in s:
            if ch == ' ':
                x += 4
                continue
            gl = g[ch]
            m = np.zeros(b.shape[:2], bool)
            m[y:y + gl.shape[0], x:x + gl.shape[1]] = gl
            b[m, :3] = ink
            x += gl.shape[1] + 1
    return b


def backgrounds():
    lvl = np.array(Image.open(RIP + 'level.png').convert('RGB'))
    lvl = (lvl >> 3) << 3
    lvl[(lvl == 0).all(2)] = (8, 8, 8)            # zuiver zwart is in BG-beelden doorzichtig
    withb = lvl.copy()
    b = board()
    x0, y0 = BOARD_POS
    m = b[:, :, 3] > 0
    reg = withb[y0:y0 + b.shape[0], x0:x0 + b.shape[1]]
    col = (b[:, :, :3] >> 3) << 3
    col[(col == 0).all(2)] = (8, 8, 8)
    reg[m] = col[m]
    imgs = [Image.fromarray(lvl), Image.fromarray(withb)]
    pals = quantize3(imgs, n=6, shared=2, iters=10)
    enc = EncoderN('intro', pals, 10, prefix='shyguy_')
    for im, lbl in zip(imgs, ['level', 'bord']):
        enc.add(im, None, lbl)
    enc.save()
    print('  bord: %d x %d op %s' % (b.shape[1], b.shape[0], BOARD_POS))
    return [enc.render(mp) for mp in enc.maps] + imgs


def main():
    bgs = backgrounds()
    sp = sprites()
    if PREVIEW:
        preview_strip(bgs, os.path.join(PREVIEW, 'shyguy_intro_bg.png'), k=2, cols=2)
        W = Image.new('RGB', (sum(s.width + 4 for s in sp), 64), (40, 40, 40))
        x = 0
        for s in sp:
            W.paste(s, (x, 64 - s.height))
            x += s.width + 4
        W.resize((W.width * 2, W.height * 2), Image.NEAREST).save(os.path.join(PREVIEW, 'shyguy_intro_sprites.png'))


if __name__ == '__main__':
    main()
