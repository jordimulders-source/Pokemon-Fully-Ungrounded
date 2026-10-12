#!/usr/bin/env python3
"""Project Grounded: gymleider-intro Wattson (alles wat hij doet is een scam). De serverfarm in zijn gym (racks met
knipperende ledjes, de gele Mauville-gymvloer met een 'rigged door': de elektrische barrière tussen twee pylonen), dan
een spervuur van pop-ups (gratis badge, WATTCOIN +9000%, Magnemite in je buurt, de gymdeur kost geld, ...), de
WATTCOIN-koers schiet naar de maan en crasht (-99%, RUGPULLED), meer pop-ups, een SCAM-stempel slaat erop en Wattson
lacht het uit: "Wahahahah!".
BG0 (paletten 13-15): de serverfarm, twee atlassen met pop-ups (+ de tekstballon), de koersgrafiek leeg en vol (de C-code
onthult hem kolom voor kolom). Sprites: Wattson (trainerfoto) en de SCAM-stempel (eigen sprite, gedraaid via affine).
Paletindexen die de C-code animeert: BG 13 index 6-8 = ledjes (drie groepen), BG 15 index 1-3 = de barrière.
Gebruik: python3 tools/grounded/wattson_transition.py [voorbeeld.png]"""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
from gym_intro_lib import Encoder, metatiles, text, text_width, save_sprite, preview_strip, OUT, KEY, gba

PREVIEW = sys.argv[1] if len(sys.argv) > 1 else None

# ------------------------------------------------------------------ kleuren
R_BG, R_FACE, R_EDGE, R_SLOT, R_CABLE = (8, 8, 24), (40, 44, 64), (72, 76, 104), (16, 16, 32), (24, 72, 120)
LED = [(48, 248, 96), (248, 184, 40), (80, 200, 248)]          # drie groepen (de C-code laat ze knipperen)
P13 = [R_BG, R_FACE, R_EDGE, R_SLOT, R_CABLE] + LED + [(120, 128, 160)]
W_NAVY, W_WHITE, W_GRAY, W_DGRAY, W_BLACK, W_RED, W_GREEN, W_YEL, W_LGRAY = (
    (16, 32, 136), (248, 248, 248), (192, 192, 200), (104, 104, 112), (8, 8, 8), (232, 32, 32), (40, 216, 72),
    (248, 224, 48), (224, 224, 232))
C_BG, C_GRID = (8, 24, 16), (24, 64, 40)
P14 = [W_NAVY, W_WHITE, W_GRAY, W_DGRAY, W_BLACK, W_RED, W_GREEN, W_YEL, W_LGRAY, C_BG, C_GRID]

# ------------------------------------------------------------------ vloer met barrière (echte Mauville-gymtiles)
BEAM = [(80, 232, 248), (176, 248, 248), (248, 248, 248)]


def floor():
    grid = [[0x20a] * 15 for _ in range(4)]
    grid[1] = [0x20a, 0x236] + [0x220, 0x221] * 6 + [0x237]
    grid[2] = [0x20a, 0x246] + [0x228, 0x229] * 6 + [0x247]
    im = metatiles('building', 'mauville_gym', grid)
    return im


fl = floor().crop((0, 8, 240, 64))                     # 56 px hoog (y 104-159)
q = fl.quantize(15, method=Image.Quantize.MEDIANCUT)
fpal = [tuple(q.getpalette()[i * 3:i * 3 + 3]) for _, i in q.getcolors()]
fl = q.convert('RGB')
# de drie felste cyaankleuren worden index 1-3 (de C-code laat ze golven)
def is_cyan(c):
    return c[2] > 150 and c[1] > 150 and c[0] < 200
fp = [gba(c) for c in fpal]
cy = sorted([c for c in fp if is_cyan(c)], key=lambda c: sum(c))
rest = [c for c in fp if c not in cy]
cy = sorted(cy, key=lambda c: -c[1] - c[2] + c[0])[:1]      # het felle cyaan van de barrière
P15 = cy + [c for c in dict.fromkeys(fp) if c not in cy]
print('vloer: %d kleuren, barrière %s' % (len(P15), cy))

# ------------------------------------------------------------------ serverfarm
def servers():
    rr = random.Random(5)
    im = Image.new('RGB', (240, 160), R_BG)
    d = ImageDraw.Draw(im)
    # kabelgoot boven
    d.rectangle((0, 0, 239, 5), fill=R_FACE)
    for x in range(0, 240, 12):
        d.line((x, 6, x + 6, 14), fill=R_CABLE, width=2)
    # vier racks
    for k in range(4):
        x0 = 6 + k * 58
        d.rectangle((x0, 14, x0 + 51, 104), fill=R_FACE)
        d.rectangle((x0, 14, x0 + 51, 15), fill=R_EDGE)
        d.rectangle((x0, 14, x0 + 1, 104), fill=R_EDGE)
        for u in range(10):
            y = 19 + u * 8
            d.rectangle((x0 + 4, y, x0 + 47, y + 5), fill=R_SLOT)
            for l in range(4):
                g = rr.randint(0, 2)
                d.rectangle((x0 + 6 + l * 4, y + 2, x0 + 7 + l * 4, y + 3), fill=LED[g])
            d.rectangle((x0 + 26, y + 2, x0 + 44, y + 3), fill=R_EDGE)
    im.paste(fl, (0, 104))
    return im


# ------------------------------------------------------------------ pop-ups (Windows 95-stijl), tile-uitgelijnd
def popup(w, h, title, lines, button=None, big=None):
    im = Image.new('RGB', (w * 8, h * 8), W_GRAY)
    d = ImageDraw.Draw(im)
    W, H = w * 8, h * 8
    d.rectangle((0, 0, W - 1, H - 1), outline=W_BLACK)
    d.line((1, 1, W - 2, 1), fill=W_WHITE)
    d.line((1, 1, 1, H - 2), fill=W_WHITE)
    d.line((1, H - 2, W - 2, H - 2), fill=W_DGRAY)
    d.line((W - 2, 1, W - 2, H - 2), fill=W_DGRAY)
    d.rectangle((3, 3, W - 4, 13), fill=W_NAVY)
    text(im, 5, 1, title, W_WHITE, None, font='narrow')
    d.rectangle((W - 12, 4, W - 5, 11), fill=W_GRAY, outline=W_BLACK)
    d.line((W - 10, 6, W - 7, 9), fill=W_BLACK)
    d.line((W - 10, 9, W - 7, 6), fill=W_BLACK)
    y = 15
    if big:
        s, col = big
        text(im, 6, y - 4, s, col, W_DGRAY, scale=2)
        y += 24
    for s, col in lines:
        text(im, 6, y - 2, s, col, None, font='narrow')
        y += 11
    if button:
        bw = text_width(button, font='narrow') + 10
        bx = W - bw - 6
        by = H - 15
        d.rectangle((bx, by, bx + bw, by + 11), fill=W_GRAY, outline=W_BLACK)
        d.line((bx + 1, by + 1, bx + bw - 1, by + 1), fill=W_WHITE)
        text(im, bx + 5, by - 3, button, W_BLACK, None, font='narrow')
    return im


POPUPS = [
    ('winner', 15, 6, 'WINNER!!!', [('YOU WON A FREE BADGE!', W_BLACK)], 'CLAIM', None),
    ('coin', 13, 7, 'WATTCOIN', [('to the moon, trust me', W_DGRAY)], None, ('+9000%', W_GREEN)),
    ('magne', 15, 5, 'ALERT', [('3 HOT MAGNEMITE', W_RED), ('IN YOUR AREA', W_BLACK)], None, None),
    ('door', 14, 5, 'GYM DOOR', [('Locked. Pay ¥500', W_BLACK), ('to open. (rigged)', W_DGRAY)], None, None),
    ('virus', 15, 5, 'ROTOM DEFENDER', [('VIRUS FOUND:', W_RED), ('your savings', W_BLACK)], None, None),
    ('like', 13, 4, 'LIVE NOW', [('SMASH THAT LIKE!', W_BLACK)], None, None),
    ('code', 13, 4, 'SPONSORED', [('USE CODE: WATT10', W_NAVY)], None, None),
    ('hodl', 8, 4, 'HODL', [('HODL!!!', W_RED)], None, None),
]
# atlasplekken (kolom, rij) van elke pop-up, twee atlassen van 30 x 20
SLOTS = {'winner': (0, 0, 0), 'coin': (0, 15, 0), 'magne': (0, 0, 6), 'door': (0, 15, 7), 'virus': (0, 0, 11),
         'like': (0, 15, 12), 'code': (0, 0, 16), 'hodl': (0, 15, 16)}


def bubble():
    im = Image.new('RGB', (96, 24), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 95, 19), radius=6, fill=W_WHITE, outline=W_BLACK)
    d.polygon([(80, 18), (92, 23), (86, 18)], fill=W_WHITE, outline=W_BLACK)
    d.line((81, 18, 86, 18), fill=W_WHITE)
    text(im, 6, 1, 'Wahahahah!', W_BLACK, W_GRAY)
    return im


atlas = [Image.new('RGB', (240, 160), (0, 0, 0)), Image.new('RGB', (240, 160), (0, 0, 0))]
for name, w, h, title, lines, button, big in POPUPS:
    a, c, r = SLOTS[name]
    atlas[a].paste(popup(w, h, title, lines, button, big), (c * 8, r * 8))
# de tekstballon op de serverfarm zelf (kolom 12-23, rij 12-14), zodat de hoeken niet zwart zijn


# ------------------------------------------------------------------ de koersgrafiek (venster kolom 3-26, rij 2-12)
CX, CY, CW, CH = 3, 2, 24, 11


def chart(full, labels=False):
    im = Image.new('RGB', (240, 160), (0, 0, 0))
    win = popup(CW, CH, 'WATTCOIN / ¥ - LIVE', [], None, None)
    d = ImageDraw.Draw(win)
    px0, py0, px1, py1 = 5, 15, CW * 8 - 6, CH * 8 - 5
    d.rectangle((px0, py0, px1, py1), fill=C_BG)
    for gx in range(px0 + 8, px1, 16):
        d.line((gx, py0, gx, py1), fill=C_GRID)
    for gy in range(py0 + 8, py1, 16):
        d.line((px0, gy, px1, gy), fill=C_GRID)
    if full:
        # exponentieel omhoog met wat ruis, dan een verticale crash
        pts = []
        n = 150
        rnd = random.Random(3)
        for i in range(n):
            x = px0 + 2 + i
            v = (i / n) ** 3.2
            y = py1 - 3 - v * (py1 - py0 - 10) + rnd.randint(-1, 1) * (1 if i > 10 else 0)
            pts.append((x, int(y)))
        d.line(pts, fill=W_GREEN, width=2)
        xc = pts[-1][0]
        d.line((xc, pts[-1][1], xc + 4, py1 - 3), fill=W_RED, width=2)
        d.line((xc + 4, py1 - 3, px1 - 2, py1 - 2), fill=W_RED, width=2)
        text(win, xc - 66, py0 - 1, 'TO THE MOON', W_YEL, None, font='narrow')
    if labels:
        text(win, px0 + 8, py0 + 4, '-99%', W_RED, W_DGRAY, scale=2)
        text(win, px0 + 10, py0 + 30, 'RUGPULLED', W_RED, None, font='narrow')
    im.paste(win, (CX * 8, CY * 8))
    return im


enc = Encoder('wattson', [P13, P14, P15])
enc.add(servers(), label='servers')      # 0
enc.add(atlas[0], label='atlas0')        # 1
sv = servers()
bb = bubble()
sv.paste(bb, (96, 96), Image.fromarray(((np.array(bb) != 0).any(2) * 255).astype(np.uint8)))
enc.add(sv, label='bubble')              # 2: serverfarm met de tekstballon
enc.add(chart(False), label='chart0')    # 3
enc.add(chart(True), label='chart1')     # 4
enc.add(chart(True, True), label='chart2')   # 5: met -99% en RUGPULLED
enc.save()
# atlasplekken voor de C-code
for name, w, h, *_ in POPUPS:
    a, c, r = SLOTS[name]
    print('  pop-up %-6s atlas %d, kolom %2d, rij %2d, %2d x %d' % (name, a, c, r, w, h))

# ------------------------------------------------------------------ SCAM-stempel (64 x 32)
st = Image.new('RGB', (64, 32), KEY)
d = ImageDraw.Draw(st)
STR, STD = (224, 24, 32), (152, 8, 16)
d.rounded_rectangle((1, 1, 62, 30), radius=4, outline=STR, width=3)
tmp = Image.new('RGB', (64, 32), KEY)
text(tmp, 32 - text_width('SCAM', scale=2, spacing=1) // 2, -1, 'SCAM', STR, STD, scale=2, spacing=1)
ta = np.array(tmp)
sa = np.array(st)
m = (ta != KEY).any(2)
sa[m] = ta[m]
# gekrast stempeleffect: wat gaatjes
rnd = random.Random(9)
for _ in range(60):
    x, y = rnd.randint(2, 61), rnd.randint(2, 29)
    if (sa[y, x] != KEY).any():
        sa[y, x] = KEY
st = Image.fromarray(sa)
save_sprite('wattson_scam', st)

if PREVIEW:
    shots = [enc.render(m) for m in enc.maps]
    comp = shots[0].copy()
    def put(src_map, c, r, w, h, dx, dy):
        img = enc.render(enc.maps[src_map]).crop((c * 8, r * 8, (c + w) * 8, (r + h) * 8))
        comp.paste(img, (dx * 8, dy * 8))
    comp.paste(shots[5].crop((CX * 8, CY * 8, (CX + CW) * 8, (CY + CH) * 8)), (CX * 8, CY * 8))
    put(1, 0, 0, 15, 5, 14, 12)
    put(1, 15, 6, 14, 5, 1, 14)
    src = Image.open(os.path.join(OUT, '..', 'trainers/front_pics/leader_wattson.png'))
    ra = np.array(src.convert('RGBA'))
    ra[np.array(src) == 0] = 0
    wa = Image.fromarray(ra)
    comp.paste(wa, (168, 96), wa)
    put(2, 12, 12, 12, 3, 12, 12)
    sa2 = np.array(st.convert('RGBA'))
    sa2[(np.array(st) == KEY).all(2)] = 0
    sti = Image.fromarray(sa2).rotate(14, expand=True)
    comp.paste(sti, (80, 40), sti)
    shots.append(comp)
    preview_strip(shots, PREVIEW, cols=3)
