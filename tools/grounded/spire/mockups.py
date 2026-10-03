"""Mockups van Spire-schermen op GBA-resolutie (240x160): beloningsscherm en act-kaart.
Gebruik: python3 mockups.py <uitmap>   -> reward.png, map.png (4x vergroot)"""
import os, sys
from PIL import Image, ImageDraw
import mockfont as F

ROOT = F.ROOT
W, H = 240, 160
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'

DARK = (64, 64, 72)
SHADOW = (208, 208, 216)
WHITE = (248, 248, 248)


def load_pal(path):
    """P-afbeelding met index 0 transparant (zoals in de game)."""
    im = Image.open(path)
    if im.mode == 'P':
        im.info.pop('transparency', None)
        rgba = im.convert('RGBA')
        px, src = rgba.load(), im.load()
        for j in range(im.height):
            for i in range(im.width):
                if src[i, j] == 0:
                    px[i, j] = (0, 0, 0, 0)
        return rgba
    return im.convert('RGBA')


def frame(img, x, y, w, h, fill=WHITE, style=1):
    """9-slice-kader uit graphics/text_window/<style>.png (8x8-tegels)."""
    src = load_pal(os.path.join(ROOT, 'graphics/text_window/%d.png' % style))
    d = ImageDraw.Draw(img)
    d.rectangle((x + 4, y + 4, x + w - 5, y + h - 5), fill=fill)
    tl, tm, tr = src.crop((0, 0, 8, 8)), src.crop((8, 0, 16, 8)), src.crop((16, 0, 24, 8))
    ml, mr = src.crop((0, 8, 8, 16)), src.crop((16, 8, 24, 16))
    bl, bm, br = src.crop((0, 16, 8, 24)), src.crop((8, 16, 16, 24)), src.crop((16, 16, 24, 24))
    for i in range(x + 8, x + w - 8, 8):
        img.paste(tm, (i, y), tm); img.paste(bm, (i, y + h - 8), bm)
    for j in range(y + 8, y + h - 8, 8):
        img.paste(ml, (x, j), ml); img.paste(mr, (x + w - 8, j), mr)
    img.paste(tl, (x, y), tl); img.paste(tr, (x + w - 8, y), tr)
    img.paste(bl, (x, y + h - 8), bl); img.paste(br, (x + w - 8, y + h - 8), br)


def mon_icon(species):
    im = load_pal(os.path.join(ROOT, 'graphics/pokemon/%s/icon.png' % species))
    return im.crop((0, 0, 32, 32))


def hpbar(img, x, y, w, frac):
    d = ImageDraw.Draw(img)
    d.rectangle((x, y, x + w, y + 3), fill=(80, 80, 88))
    col = (88, 208, 128) if frac > 0.5 else (248, 200, 40) if frac > 0.2 else (240, 80, 64)
    d.rectangle((x + 1, y + 1, x + 1 + int((w - 2) * frac), y + 2), fill=col)


TYPE_COL = {'GROUND': (224, 192, 104), 'FAIRY': (238, 153, 172), 'ICE': (152, 216, 216),
            'WATER': (104, 144, 240), 'PSYCHIC': (248, 88, 136), 'STEEL': (184, 184, 208)}


def type_chip(img, x, y, t):
    d = ImageDraw.Draw(img)
    c = TYPE_COL[t]
    d.rectangle((x, y, x + 33, y + 10), fill=c, outline=tuple(v * 2 // 3 for v in c))
    name = t.capitalize()
    F.text(img, x + 17 - F.width(name, 'small') // 2, y - 3, name, fg=WHITE, shadow=tuple(v // 2 for v in c), name='small')


def gradient(img, top, bottom):
    d = ImageDraw.Draw(img)
    for j in range(H):
        t = j / (H - 1)
        d.line((0, j, W, j), fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))


# ---------------------------------------------------------------------------
def reward_screen():
    img = Image.new('RGB', (W, H))
    gradient(img, (40, 32, 72), (16, 16, 32))
    d = ImageDraw.Draw(img)
    # torenstenen op de achtergrond
    for j in range(0, H, 8):
        for i in range((j // 8 % 2) * 8, W, 16):
            d.rectangle((i, j, i + 15, j + 7), outline=(52, 44, 88))

    # kop
    frame(img, 0, 0, 240, 24)
    F.text(img, 8, 4, 'VICTORY!')
    F.text(img, 70, 4, '+1 BP', fg=(40, 120, 200), shadow=(184, 216, 240))
    F.text(img, 112, 4, 'Team +20% HP', fg=(40, 152, 72), shadow=(184, 232, 192))
    F.text(img, 236 - F.width('Act 1-3', 'small'), 4, 'Act 1-3', name='small')

    # drie movekaarten
    cards = [('Earth Power', 'GROUND', 'Spec.', 90, 10, 'COMMON', (160, 160, 168)),
             ('Freeze-Dry', 'ICE', 'Spec.', 70, 20, 'UNCOMMON', (64, 128, 232)),
             ('Moonblast', 'FAIRY', 'Spec.', 95, 5, 'RARE', (208, 144, 16))]
    sel = 1
    for k, (name, typ, cat, pwr, pp, rar, rcol) in enumerate(cards):
        x, y = 4 + k * 78, 30
        frame(img, x, y, 76, 62)
        d.rectangle((x + 3, y + 3, x + 72, y + 6), fill=rcol)
        F.text(img, x + 38 - F.width(name, 'small') // 2, y + 6, name, name='small')
        type_chip(img, x + 6, y + 24, typ)
        F.text(img, x + 44, y + 21, cat, name='small')
        F.text(img, x + 6, y + 33, 'PWR %d' % pwr, name='small')
        F.text(img, x + 44, y + 33, 'PP %d' % pp, name='small')
        F.text(img, x + 38 - F.width(rar, 'small') // 2, y + 44, rar, fg=rcol, shadow=tuple(min(255, v + 120) for v in rcol), name='small')
        if k == sel:
            d.rectangle((x + 1, y + 1, x + 74, y + 60), outline=(248, 80, 64))
            d.rectangle((x + 2, y + 2, x + 73, y + 59), outline=(248, 80, 64))
            F.text(img, x + 33, y - 9, '↓', fg=(248, 248, 248), shadow=(120, 40, 40))

    # onderste vak: beschrijving + wie leert hem
    frame(img, 0, 96, 240, 64)
    F.text(img, 8, 99, 'Freeze-Dry: super effective', name='small')
    F.text(img, 8, 109, 'on Water too. May freeze.', name='small')
    team = [('gardevoir', 'Gardevoir', 0.64, False), ('swampert', 'Swampert', 0.88, False)]
    for k, (sp, nm, hp, stab) in enumerate(team):
        x = 8 + k * 92
        ic = mon_icon(sp)
        img.paste(ic, (x - 4, 119), ic)
        F.text(img, x + 26, 121, nm, name='small')
        if sp == 'gardevoir' and cards[sel][1] == 'FAIRY':
            F.text(img, x + 66, 121, 'STAB', fg=(200, 64, 56), shadow=(248, 200, 192), name='small')
        hpbar(img, x + 26, 136, 44, hp)
        F.text(img, x + 72, 129, '%d%%' % (hp * 100), name='small')
    F.text(img, 196, 119, 'A: Pick', name='small')
    F.text(img, 196, 131, 'B: Skip', name='small')
    F.text(img, 190, 143, 'SEL: Map', name='small')
    return img


# ---------------------------------------------------------------------------
ICONS = {
    'fight': ["....XXXXX....", "..XXRRRRRXX..", ".XRRRRRRRRRX.", ".XRRRRRRRRRX.", "XRRRRRRRRRRRX",
              "XXXXXWWWXXXXX", "XWWWXW.WXWWWX", "XWWWWXWXWWWWX", ".XWWWWWWWWWX.", ".XWWWWWWWWWX.",
              "..XXWWWWWXX..", "....XXXXX...."],
    'elite': ["..X.......X..", "..XX.....XX..", "..XXXXXXXXX..", ".XPPPPPPPPPX.", "XPPPPPPPPPPPX",
              "XPPYYPPPYYPPX", "XPPYYPPPYYPPX", "XPPPPPPPPPPPX", "XPPPPXXXPPPPX", ".XPPPPPPPPPX.",
              "..XXPPPPPXX..", "....XXXXX...."],
    'shop': ["....XXXXX....", "..XXGGGGGXX..", ".XGGGGGGGGGX.", ".XGGXXXXGGGX.", "XGGGXGGGXGGGX",
             "XGGGXGGGXGGGX", "XGGGXXXXGGGGX", "XGGGXGGGGGGGX", ".XGGXGGGGGGX.", ".XGGGGGGGGGX.",
             "..XXGGGGGXX..", "....XXXXX...."],
    'rest': ["....XXXXX....", "..XXWWWWWXX..", ".XWWWWRWWWWX.", ".XWWWWRWWWWX.", "XWWWWWRWWWWWX",
             "XWRRRRRRRRRWX", "XWWWWWRWWWWWX", "XWWWWWRWWWWWX", ".XWWWWRWWWWX.", ".XWWWWWWWWWX.",
             "..XXWWWWWXX..", "....XXXXX...."],
    'event': ["....XXXXX....", "..XXBBBBBXX..", ".XBBBWWWBBBX.", ".XBBWBBBWBBX.", "XBBBBBBBWBBBX",
              "XBBBBBBWBBBBX", "XBBBBBWBBBBBX", "XBBBBBWBBBBBX", ".XBBBBBBBBBX.", ".XBBBBWBBBBX.",
              "..XXBBBBBXX..", "....XXXXX...."],
}
ICOL = {'X': (40, 40, 48), 'R': (232, 64, 56), 'W': (248, 248, 248), 'P': (120, 72, 176), 'Y': (248, 216, 64),
        'G': (240, 192, 48), 'B': (72, 136, 232)}


def icon(img, cx, cy, kind, dim=False):
    rows = ICONS[kind]
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == '.':
                continue
            c = ICOL[ch]
            if dim:
                c = tuple((v + 2 * 200) // 3 for v in c)
            img.putpixel((cx - 6 + i, cy - 6 + j), c)


def map_screen():
    import random
    rnd = random.Random(4)
    img = Image.new('RGB', (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    # perkament
    PAPER, INK, FADED = (232, 216, 168), (120, 88, 56), (200, 176, 128)
    d.rectangle((0, 0, 167, 159), fill=PAPER)
    for _ in range(260):
        x, y = rnd.randrange(168), rnd.randrange(160)
        img.putpixel((x, y), (220, 202, 150))
    d.rectangle((0, 0, 167, 159), outline=INK)
    d.rectangle((1, 1, 166, 158), outline=(176, 144, 96))

    # kaart: verdieping 1 onderaan, baas bovenaan
    layout = [
        [('fight', 40), ('fight', 84), ('event', 128)],
        [('fight', 28), ('shop', 72), ('fight', 116), ('fight', 148)],
        [('event', 40), ('fight', 84), ('elite', 128)],
        [('fight', 28), ('rest', 72), ('fight', 116)],
        [('elite', 40), ('event', 84), ('fight', 128)],
        [('shop', 28), ('fight', 72), ('elite', 116), ('event', 148)],
        [('fight', 52), ('fight', 104)],
        [('rest', 52), ('rest', 104)],
    ]
    edges = {0: [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3)],
             1: [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)],
             2: [(0, 0), (0, 1), (1, 1), (2, 2)],
             3: [(0, 0), (1, 1), (2, 1), (2, 2)],
             4: [(0, 0), (0, 1), (1, 1), (2, 2), (2, 3)],
             5: [(0, 0), (1, 0), (2, 1), (3, 1)],
             6: [(0, 0), (1, 1), (1, 0)],
             7: [(0, 0), (1, 0)]}
    ys = [146 - 15 * f for f in range(8)]
    BOSS_Y = 18
    path = [(0, 1), (1, 1), (2, 1)]          # gekozen route tot nu toe (verdieping, index)
    cur = path[-1]
    nexts = [(3, 1), (3, 2)]                 # bereikbaar vanaf de huidige plek

    def pos(f, i):
        return layout[f][i][1], ys[f]

    # lijnen
    for f, es in edges.items():
        for a, b in es:
            x0, y0 = pos(f, a)
            if f == 7:
                x1, y1 = 84, BOSS_Y + 10
            else:
                x1, y1 = pos(f + 1, b)
            taken = (f, a) in path and ((f + 1, b) in path or (f, a) == cur and (f + 1, b) in nexts)
            n = max(abs(x1 - x0), abs(y1 - y0))
            for s in range(3, n - 3):
                if not taken and s % 3:
                    continue
                x = x0 + (x1 - x0) * s // n
                y = y0 + (y1 - y0) * s // n
                img.putpixel((x, y), INK if taken else FADED)
    # knopen
    for f, row in enumerate(layout):
        for i, (kind, x) in enumerate(row):
            y = ys[f]
            done = (f, i) in path and (f, i) != cur
            icon(img, x, y, kind, dim=f < cur[0] and not done)
            if done:
                d.line((x - 5, y - 5, x + 5, y + 5), fill=INK)
                d.line((x - 5, y + 5, x + 5, y - 5), fill=INK)
    # huidige plek: speler, volgende keuzes omcirkeld
    cx, cy = pos(*cur)
    d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), outline=(232, 64, 56))
    for (f, i) in nexts:
        x, y = pos(f, i)
        d.ellipse((x - 8, y - 8, x + 8, y + 8), outline=(40, 120, 200))
    sel = nexts[1]
    x, y = pos(*sel)
    F.text(img, x + 9, y - 9, '←', fg=(40, 120, 200), shadow=PAPER)
    # baas
    boss = mon_icon('tyranitar')
    d.ellipse((84 - 18, BOSS_Y - 15, 84 + 18, BOSS_Y + 15), fill=(200, 72, 64), outline=INK)
    img.paste(boss, (84 - 16, BOSS_Y - 18), boss)
    F.text(img, 108, BOSS_Y - 10, 'BOSS', fg=(168, 40, 40), shadow=(232, 200, 160), name='small')

    # rechterpaneel
    frame(img, 168, 0, 72, 114)
    F.text(img, 174, 3, 'ACT 1')
    F.text(img, 174, 16, 'Floor 4/8', name='small')
    for k, (sp, hp) in enumerate([('gardevoir', 0.64), ('swampert', 0.88)]):
        y = 30 + k * 24
        ic = mon_icon(sp).crop((4, 6, 28, 30))
        img.paste(ic, (170, y), ic)
        F.text(img, 196, y, '%d%%' % (hp * 100), name='small')
        hpbar(img, 196, y + 15, 36, hp)
    F.text(img, 174, 78, 'BP 14', name='small')
    for k, it in enumerate(['leftovers', 'quick_claw']):
        ii = load_pal(os.path.join(ROOT, 'graphics/items/icons/%s.png' % it))
        img.paste(ii, (184 + k * 24, 86), ii)

    # uitleg van de gekozen kamer
    frame(img, 168, 114, 72, 46)
    icon(img, 180, 125, 'fight')
    F.text(img, 190, 118, 'Battle', name='small')
    F.text(img, 174, 131, '2 foes', name='small')
    F.text(img, 174, 143, '→ move drop', name='small')
    return img


def legend():
    img = Image.new('RGB', (240, 24), (232, 216, 168))
    labels = [('fight', 'Battle'), ('elite', 'Elite'), ('shop', 'Shop'), ('rest', 'Rest'), ('event', 'Event')]
    x = 10
    for kind, lab in labels:
        icon(img, x, 12, kind)
        x = F.text(img, x + 9, 4, lab, name='small') + 10
    return img


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, im in (('reward', reward_screen()), ('map', map_screen()), ('legend', legend())):
        im.resize((im.width * 4, im.height * 4), Image.NEAREST).save(os.path.join(OUT, name + '.png'))
