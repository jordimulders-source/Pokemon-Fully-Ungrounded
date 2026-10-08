#!/usr/bin/env python3
"""Project Grounded: gymleider-intro Wallace (sommelier van de Crater Pub, "Your spirit has a certain... bouquet.",
"a performance of liquid illusions", "Santé!"). In de pub schenkt een zwevende fles (illusie) een groot wijnglas vol;
Wallace walst mee: "Your spirit has a certain..." / "...bouquet." De wijn kleurt Hoenn-blauw ("Notes of brine, regret
and Kyogre."), het glas springt, en een golf slaat van rechts over de pub. "SANTÉ!"

BG0 (paletten 13-15): de pub (palet 13), het glas met de wijn in 8 lagen (palet 14: de C-code vult de lagen en kleurt ze
blauw), daarna het kapotte glas en de golf (palet 15, 4 waterkleuren die rondlopen), ondertitels in de zwarte balken.
Sprites: Wallace (trainerfoto), de wijnstraal (eigen, 8x32), Splash uit de gevechtsanimaties bij de golffront.
Gebruik: python3 tools/grounded/wallace_transition.py [voorbeeld.png]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
from gym_intro_lib import outlined_text as outlined, Encoder, text, text_width, save_sprite, preview_strip, OUT, KEY, gba

PREVIEW = sys.argv[1] if len(sys.argv) > 1 else None

WALL, WALL_D, SHELF, BOT_G, BOT_A, BOT_R, LABEL = (64, 36, 28), (44, 24, 20), (112, 68, 40), (40, 88, 56), \
    (152, 96, 32), (112, 24, 48), (216, 200, 160)
COUNTER, COUNTER_L, COUNTER_D, LAMP, PUDDLE, GLASS_L, GLASS_M = (120, 72, 40), (168, 112, 64), (80, 44, 24), \
    (248, 216, 128), (48, 104, 208), (216, 232, 240), (136, 148, 160)
P13 = [WALL, WALL_D, SHELF, BOT_G, BOT_A, BOT_R, LABEL, COUNTER, COUNTER_L, COUNTER_D, LAMP, PUDDLE, GLASS_L, GLASS_M]
BANDS = [(72, 40, 32 + i * 8) for i in range(8)]       # in de C-code: leeg (wandkleur), wijn of blauw
P14 = BANDS + [GLASS_L, GLASS_M, WALL, WALL_D, BOT_R, LABEL]
WATER = [(32, 80, 184), (48, 112, 216), (80, 152, 232), (24, 56, 152)]
FOAM = (232, 240, 248)
WHITE15, GRAY15, YELLOW15, BLUE15, DARK15, DISC = (240, 240, 240), (160, 160, 168), (248, 224, 72), (64, 136, 248), \
    (8, 16, 56), (136, 128, 144)
P15 = [WHITE15, GRAY15, YELLOW15, BLUE15, DARK15, DISC] + WATER + [FOAM]
for p in (P13, P14, P15):
    assert len(p) <= 15 and len(set(gba(c) for c in p)) == len(p), p


def idx(pal, c):
    return [gba(x) for x in pal].index(gba(c)) + 1


def ctext(im, cx, y, s, fg, shadow=None, font='normal', scale=1, spacing=0):
    return text(im, cx - text_width(s, font, scale, spacing) // 2, y, s, fg, shadow, font, scale, spacing)




GX, GY, RX, RY = 176, 76, 28, 30        # de kelk (ellips), open boven y 52
RIM = 52
BOTTOM = GY + RY                         # 106
WINE_TOP = 78                            # tot hier vult de wijn (8 lagen)
STREAM_X = 172


def subtitle(im, sub):
    if sub == 1:
        im = outlined(im, 120, 3, 'Your spirit has a certain...', WHITE15, GRAY15, DARK15, scale=1)
    elif sub == 2:
        im = outlined(im, 120, 3, '...bouquet.', WHITE15, GRAY15, DARK15, scale=1)
    elif sub == 3:
        im = outlined(im, 120, 3, 'Notes of brine, regret and KYOGRE.', WHITE15, GRAY15, DARK15, scale=1, font='narrow')
    elif sub == 4:
        # 28 px hoog (accent t/m schaduw): y 1-28; de C-code toont voor SANTÉ rij 0-3 (was y 6 in een balk van 24 px:
        # de onderkant viel weg)
        im = outlined(im, 120, 2, 'SANTÉ!', YELLOW15, BLUE15, DARK15, scale=2)
    return im


def disclaimer(im):
    s = 'Please drink responsibly. Mostly.'
    text(im, 238 - text_width(s, font='narrow'), 146, s, DISC, None, font='narrow')
    return im


def pub(glass=True, sub=0):
    im = Image.new('RGB', (240, 160), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 24, 239, 119), fill=WALL)
    for x in range(0, 240, 16):
        d.line((x, 24, x, 119), fill=WALL_D)
    # schappen met flessen (links, achter Wallace)
    for sy in (54, 88):
        d.rectangle((0, sy, 111, sy + 3), fill=SHELF)
        for i, x in enumerate(range(6, 108, 12)):
            c = (BOT_G, BOT_A, BOT_R)[(i + sy // 4) % 3]
            h = 14 + (i * 5 + sy) % 6
            d.rectangle((x, sy - h, x + 6, sy - 1), fill=c)
            d.rectangle((x + 2, sy - h - 5, x + 4, sy - h), fill=c)
            d.rectangle((x + 1, sy - 9, x + 5, sy - 5), fill=LABEL)
    # hanglamp
    d.line((128, 24, 128, 34), fill=WALL_D)
    d.polygon([(120, 40), (136, 40), (132, 34), (124, 34)], fill=SHELF)
    d.rectangle((125, 40, 131, 42), fill=LAMP)
    # toog
    d.rectangle((0, 120, 239, 143), fill=COUNTER)
    d.rectangle((0, 120, 239, 123), fill=COUNTER_L)
    d.rectangle((0, 136, 239, 143), fill=COUNTER_D)
    if glass:
        px = im.load()
        for y in range(RIM, BOTTOM + 1):
            for x in range(GX - RX - 1, GX + RX + 2):
                r = ((x - GX) / RX) ** 2 + ((y - GY) / RY) ** 2
                if r <= 1.0:
                    if y >= WINE_TOP:
                        band = min(7, (BOTTOM - y) * 8 // (BOTTOM - WINE_TOP + 1))
                        px[x, y] = BANDS[band]
                    else:
                        px[x, y] = WALL
        for y in range(RIM, BOTTOM + 2):
            for x in range(GX - RX - 2, GX + RX + 3):
                r = ((x - GX) / RX) ** 2 + ((y - GY) / RY) ** 2
                if 1.0 < r <= 1.18:
                    px[x, y] = GLASS_L if x < GX else GLASS_M
        d.line((GX - RX + 6, RIM + 6, GX - RX + 4, GY + 8), fill=GLASS_L)
        d.line((GX - 8, RIM, GX + 8, RIM), fill=GLASS_M)
        d.rectangle((GX - 1, BOTTOM + 1, GX + 1, 117), fill=GLASS_M)
        d.line((GX - 1, BOTTOM + 1, GX - 1, 117), fill=GLASS_L)
        d.ellipse((GX - 14, 116, GX + 14, 122), fill=GLASS_M)
        d.line((GX - 12, 118, GX + 4, 118), fill=GLASS_L)
        # de zwevende fles (illusie) die schenkt: hals linksonder, schuin omhoog naar rechts
        d.polygon([(STREAM_X + 2, 40), (STREAM_X + 8, 36), (STREAM_X + 20, 32), (STREAM_X + 22, 38), (STREAM_X + 10, 42)], fill=BOT_R)
        d.polygon([(STREAM_X + 18, 30), (STREAM_X + 56, 26), (STREAM_X + 60, 44), (STREAM_X + 22, 42)], fill=BOT_R)
        d.polygon([(STREAM_X + 30, 31), (STREAM_X + 46, 29), (STREAM_X + 48, 39), (STREAM_X + 32, 40)], fill=LABEL)
    else:
        # scherven en een blauwe plas op de toog
        d.ellipse((GX - 34, 118, GX + 30, 126), fill=PUDDLE)
        for sx, sy, w in ((GX - 20, 119, 4), (GX - 4, 121, 3), (GX + 10, 118, 5), (GX + 22, 122, 3), (GX - 30, 123, 3)):
            d.polygon([(sx, sy + 2), (sx + w // 2, sy - 2), (sx + w, sy + 2)], fill=GLASS_L)
    return disclaimer(subtitle(im, sub))


def wave(sub=0):
    im = Image.new('RGB', (240, 160), (0, 0, 0))
    px = im.load()
    for y in range(24, 144):
        for x in range(240):
            u = y + 3 * math.sin((x + 0.5) * 2 * math.pi / 32) + (y - 24) * 0.0
            band = int(u / 6) % 4
            px[x, y] = WATER[band]
            if (x + y * 3) % 23 == 0 and band == 2:
                px[x, y] = FOAM
    return disclaimer(subtitle(im, sub))


enc = Encoder('wallace', [P13, P14, P15])
ORDER = [('pub', pub(True, 0)), ('pub1', pub(True, 1)), ('pub2', pub(True, 2)), ('pub3', pub(True, 3)),
         ('broken', pub(False, 3)), ('wave', wave(0)), ('wave4', wave(4))]
for k, im in ORDER:
    enc.add(im, label=k)
enc.save()
print('BG14 bands = 1-8; BG15 water = %d-%d' % (idx(P15, WATER[0]), idx(P15, WATER[3])))

# ------------------------------------------------------------------ de wijnstraal (8x32)
st = Image.new('RGB', (8, 32), KEY)
d = ImageDraw.Draw(st)
d.rectangle((3, 0, 5, 31), fill=(112, 16, 40))
d.line((3, 0, 3, 31), fill=(160, 40, 64))
save_sprite('wallace_stream', st)

if PREVIEW:
    shots = [enc.render(m) for m in enc.maps]
    src = Image.open(os.path.join(OUT, '..', 'trainers/front_pics/champion_wallace.png'))
    a = np.array(src.convert('RGBA'))
    a[np.array(src) == 0] = 0
    wal = Image.fromarray(a)
    comp = enc.render(enc.maps[2], pals=[enc.pals[0], [enc.pals[1][0]] + [(120, 16, 40)] * 8 + enc.pals[1][9:], enc.pals[2]])
    comp.paste(wal, (40, 64), wal)
    shots.append(comp)
    preview_strip(shots, PREVIEW)
