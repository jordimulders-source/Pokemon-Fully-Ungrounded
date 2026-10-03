"""Mockups van Spire-schermen op GBA-resolutie (240x160): beloningsscherm en act-kaart.
Gebruik: python3 mockups.py <uitmap> [v2]   -> reward/map/legend (v2: reward, map2 in Town Map-stijl, legend2, relics), 4x vergroot"""
import os, sys
from PIL import Image, ImageDraw
import mockfont as F

ROOT = F.ROOT
W, H = 240, 160
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'

DARK = (64, 64, 72)
SHADOW = (208, 208, 216)
WHITE = (248, 248, 248)


def jasc(path):
    lines = open(path).read().split('\n')[3:]
    return [tuple(int(v) for v in l.split()) for l in lines if l.strip()]




def item_icon(name):
    """Item-icoon met het echte palet uit graphics/items/icon_palettes (zoals in src/data/graphics/items.h)."""
    import re
    hdr = open(os.path.join(ROOT, 'src/data/graphics/items.h')).read()
    m = re.search(r'icons/%s\.4bpp[^\n]*\n[^\n]*icon_palettes/(\w+)' % name, hdr)
    return load_pal(os.path.join(ROOT, 'graphics/items/icons/%s.png' % name),
                    os.path.join(ROOT, 'graphics/items/icon_palettes/%s.pal' % m.group(1)))


def load_pal(path, palpath=None):
    """P-afbeelding met index 0 transparant (zoals in de game)."""
    im = Image.open(path)
    if palpath:
        pal = jasc(palpath)
        im.putpalette([c for rgb in pal for c in rgb] + [0] * (768 - 3 * len(pal)))
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


ICON_PAL = {'tyranitar': 4, 'gardevoir': 1, 'swampert': 0, 'ditto': 2, 'unown/question': 0}


def mon_icon(species):
    """Pokémon-icoon (eerste frame) met het echte icoonpalet uit graphics/pokemon/icon_palettes."""
    src = Image.open(os.path.join(ROOT, 'graphics/pokemon/%s/icon.png' % species))
    pal = jasc(os.path.join(ROOT, 'graphics/pokemon/icon_palettes/pal%d.pal' % ICON_PAL[species]))
    out = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    sp = src.load()
    for j in range(32):
        for i in range(32):
            v = sp[i, j]
            if v:
                out.putpixel((i, j), pal[v] + (255,))
    return out


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
    F.text(img, 138, 4, '+1 BP', fg=(40, 120, 200), shadow=(184, 216, 240))
    F.text(img, 178, 4, '+20% HP', fg=(40, 152, 72), shadow=(184, 232, 192))

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
            hand = load_pal(os.path.join(ROOT, 'graphics/pokemon_storage/hand_cursor.png')).crop((0, 0, 32, 32))
            img.paste(hand, (x + 22, y - 24), hand)

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
        ii = item_icon(it)
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


# ---------------------------------------------------------------------------
# Versie 2: act-kaart in Town Map-stijl, zoveel mogelijk met assets uit de game.

def oldale_emblems():
    """Pokémon Center- en Mart-embleem (16x16) uit een render van Oldale Town."""
    import subprocess, tempfile
    tmp = os.path.join(tempfile.gettempdir(), 'spire_oldale.png')
    if not os.path.exists(tmp):
        subprocess.run([sys.executable, os.path.join(ROOT, 'tools/grounded/maptools/render_map.py'),
                        'OldaleTown', tmp, '0', '20'], cwd=ROOT, check=True)
    im = Image.open(tmp).convert('RGBA')
    return im.crop((104, 232, 120, 248)), im.crop((231, 71, 247, 87))


def tile(n):
    sheet = Image.open(os.path.join(ROOT, 'graphics/pokenav/region_map/map.png')).convert('RGBA')
    return sheet.crop(((n % 16) * 8, (n // 16) * 8, (n % 16) * 8 + 8, (n // 16) * 8 + 8))


def fill(img, box, n):
    if n is None:  # gelopen route: effen rood zoals de stadsblokjes
        ImageDraw.Draw(img).rectangle((box[0], box[1], box[2] - 1, box[3] - 1), fill=(224, 72, 56))
        return
    t = tile(n)
    x0, y0, x1, y1 = box
    for y in range(y0 - y0 % 8, y1, 8):
        for x in range(x0 - x0 % 8, x1, 8):
            piece = t.crop((max(0, x0 - x), max(0, y0 - y), min(8, x1 - x), min(8, y1 - y)))
            img.paste(piece, (max(x, x0), max(y, y0)))


def node_icons():
    pc, mart = oldale_emblems()
    ball = item_icon('poke_ball').crop((3, 3, 21, 21))
    marker = load_pal(os.path.join(ROOT, 'graphics/pokedex/area_marker.png'))
    unown = mon_icon('unown/question')
    unown = unown.crop(unown.getbbox())
    return {'fight': ball, 'elite': marker, 'rest': pc, 'shop': mart, 'event': unown}


def paste_c(img, im, cx, cy):
    img.paste(im, (cx - im.width // 2, cy - im.height // 2), im)


def map_screen2():
    img = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(img)
    icons = node_icons()
    SEA, LAND, ROUTE, ROUTE_DONE = 0, 19, 16, None
    MW = 168
    fill(img, (0, 0, MW, H), SEA)
    # eiland onder het netwerk (rechthoek met ingesprongen randen, Town Map-tegels)
    for (x0, y0, x1, y1) in [(8, 24, 160, 152), (16, 16, 152, 160), (0, 40, 168, 136)]:
        fill(img, (x0, y0, x1, y1), LAND)

    layout = [
        [('fight', 32), ('fight', 84), ('event', 136)],
        [('fight', 20), ('shop', 60), ('fight', 108), ('fight', 148)],
        [('event', 32), ('fight', 84), ('elite', 136)],
        [('fight', 20), ('rest', 60), ('fight', 108)],
        [('elite', 32), ('event', 84), ('fight', 136)],
        [('shop', 32), ('fight', 84), ('elite', 136)],
        [('rest', 56), ('rest', 112)],
    ]
    edges = {0: [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3)],
             1: [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)],
             2: [(0, 0), (0, 1), (1, 1), (2, 2)],
             3: [(0, 0), (1, 1), (2, 1), (2, 2)],
             4: [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
             5: [(0, 0), (1, 0), (1, 1), (2, 1)]}
    ys = [148 - 19 * f for f in range(7)]
    BOSS = (84, 16)
    path = [(0, 1), (1, 1), (2, 1)]
    cur = path[-1]
    nexts = [(3, 1), (3, 2)]

    def pos(f, i):
        return layout[f][i][1], ys[f]

    def route(x0, y0, x1, y1, n):
        # Town Map-route: eerst omhoog tot halverwege, dan opzij, dan omhoog (4 px breed)
        ym = (y0 + y1) // 2
        fill(img, (x0 - 2, ym - 2, x0 + 2, y0), n)
        fill(img, (min(x0, x1) - 2, ym - 2, max(x0, x1) + 2, ym + 2), n)
        fill(img, (x1 - 2, y1, x1 + 2, ym + 2), n)

    # eerst gewone routes, dan de gelopen route eroverheen
    for done in (False, True):
        for f, es in edges.items():
            for a, b in es:
                taken = (f, a) in path and (f + 1, b) in path
                if taken != done:
                    continue
                route(*pos(f, a), *pos(f + 1, b), ROUTE_DONE if taken else ROUTE)
        if not done:
            for _, x in layout[6]:
                route(x, ys[6], BOSS[0], BOSS[1] + 8, ROUTE)

    # baas: groot rood stadsblok met de baas erop
    fill(img, (BOSS[0] - 20, BOSS[1] - 8, BOSS[0] + 20, BOSS[1] + 8), 76)
    d.rectangle((BOSS[0] - 21, BOSS[1] - 9, BOSS[0] + 20, BOSS[1] + 8), outline=(64, 32, 32))
    boss = mon_icon('tyranitar')
    img.paste(boss, (BOSS[0] - 16, BOSS[1] - 22), boss)

    # kamers
    for f, row in enumerate(layout):
        for i, (kind, x) in enumerate(row):
            ic = icons[kind]
            past = f < cur[0] or (f, i) == cur
            if past and (f, i) not in path:
                ic = ic.copy()
                ic.putalpha(ic.getchannel('A').point(lambda a: a * 2 // 5))
            paste_c(img, ic, x, ys[f])

    # speler (Brendan-hoofdje van de Town Map) en de Town Map-cursor op de keuze
    head = load_pal(os.path.join(ROOT, 'graphics/pokenav/region_map/brendan_icon.png'))
    cx, cy = pos(*cur)
    img.paste(head, (cx - 18, cy - 10), head)
    cursor = load_pal(os.path.join(ROOT, 'graphics/pokenav/region_map/cursor_small.png'),
                      os.path.join(ROOT, 'graphics/pokenav/region_map/cursor.pal')).crop((0, 0, 16, 16))
    for k, (f, i) in enumerate(nexts):
        x, y = pos(f, i)
        if k == 1:  # Town Map-cursor (knippert in de game), hier rood ingekleurd
            for (ox, oy, sx, sy) in ((-11, -11, 1, 1), (10, -11, -1, 1), (-11, 10, 1, -1), (10, 10, -1, -1)):
                for t in range(2):  # hoekhaken zoals de Town Map-cursor
                    d.line((x + ox, y + oy + t * sy, x + ox + 5 * sx, y + oy + t * sy), fill=(248, 72, 40))
                    d.line((x + ox + t * sx, y + oy, x + ox + t * sx, y + oy + 5 * sy), fill=(248, 72, 40))

    d.rectangle((0, 0, MW - 1, H - 1), outline=(40, 56, 96))

    # rechterpaneel
    frame(img, 168, 0, 72, 114)
    F.text(img, 174, 3, 'ACT 1')
    F.text(img, 174, 16, 'Floor 4/7', name='small')
    for k, (sp, hp) in enumerate([('gardevoir', 0.64), ('swampert', 0.88)]):
        y = 30 + k * 24
        ic = mon_icon(sp).crop((4, 6, 28, 30))
        img.paste(ic, (170, y), ic)
        F.text(img, 196, y, '%d%%' % (hp * 100), name='small')
        hpbar(img, 196, y + 15, 36, hp)
    F.text(img, 174, 78, 'BP 14', name='small')
    relics = ['leftovers', 'quick_claw', 'wide_lens', 'scope_lens', 'kings_rock']
    for k, it in enumerate(relics[:2]):
        ii = item_icon(it)
        img.paste(ii, (170 + k * 22, 88), ii)
    F.text(img, 216, 94, '+%d' % (len(relics) - 2), name='small')

    # uitleg van de gekozen kamer
    frame(img, 168, 114, 72, 46)
    paste_c(img, icons['fight'], 182, 126)
    F.text(img, 193, 118, 'Battle', name='small')
    F.text(img, 174, 131, '2 wild', name='small')
    F.text(img, 174, 143, 'Win: new move', name='small')
    return img


def legend2():
    icons = node_icons()
    img = Image.new('RGB', (240, 24), (248, 248, 248))
    x = 6
    for kind, lab in [('fight', 'Battle'), ('elite', 'Elite'), ('rest', 'Rest'), ('shop', 'Shop'), ('event', 'Event')]:
        paste_c(img, icons[kind], x + 9, 12)
        x = F.text(img, x + 20, 4, lab, name='small') + 8
    return img


def relic_list():
    """R op de kaart: alle relics met uitleg (lijst die scrolt)."""
    img = Image.new('RGB', (W, H))
    fill(img, (0, 0, W, H), 1)
    frame(img, 0, 0, 240, 24)
    F.text(img, 8, 4, 'RELICS  (5)')
    F.text(img, 236 - F.width('B: Back', 'small'), 6, 'B: Back', name='small')
    frame(img, 0, 24, 240, 136)
    rows = [('leftovers', 'Leftovers', 'Heal 5% HP after each turn.'),
            ('quick_claw', 'Quick Claw', 'First turn: you move first.'),
            ('wide_lens', 'Wide Lens', 'Spread moves lose no power.'),
            ('scope_lens', 'Scope Lens', 'Critical hits more often.'),
            ('kings_rock', "King's Rock", '+1 Block on every DEFEND.')]
    for k, (it, name, desc) in enumerate(rows):
        y = 30 + k * 25
        ii = item_icon(it)
        img.paste(ii, (8, y), ii)
        F.text(img, 36, y - 2, name, name='small')
        F.text(img, 36, y + 9, desc, fg=(104, 104, 112), shadow=(216, 216, 224), name='small')
    hand = load_pal(os.path.join(ROOT, 'graphics/pokemon_storage/hand_cursor.png')).crop((0, 0, 32, 32))
    for k in range(5):  # icoontjes iets naar rechts, hand wijst naar de gekozen relic
        pass
    img.paste(hand, (-6, 26), hand)
    return img


if __name__ == '__main__' and len(sys.argv) > 2 and sys.argv[2] == 'v2':
    for name, im in (('reward', reward_screen()), ('map2', map_screen2()), ('legend2', legend2()), ('relics', relic_list())):
        im.resize((im.width * 4, im.height * 4), Image.NEAREST).save(os.path.join(OUT, name + '.png'))
