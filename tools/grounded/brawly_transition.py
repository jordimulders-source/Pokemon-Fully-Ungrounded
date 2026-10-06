#!/usr/bin/env python3
"""Project Grounded: gymleider-intro Brawly (UFC: "Let me see if you're worth the contract!").
1. De walkout: de camera loopt door de spelerstunnel (lichtringen razen op je af via een paletcyclus, het beeld deint
   mee met de passen), LIVE-logo in de hoek. 2. Wit: de arena in. 3. De octagon: Brawly in de kooi, publiek met
   cameraflitsen, de omroeperbalk "BRAWLY - DOUBLE CHAMP" schuift in beeld. 4. Close-up van het kooigaas: zijn vuist
   komt van achter het gaas op de camera af, het gaas bolt (tweede beeld) en de klap flitst.
BG0 (paletten 13-15): tunnel, octagon, gaas en gaas met deuk, plus een atlas met de omroeperbalk en flitsen.
Sprites: Brawly (trainerfoto), zijn vuist (de vuist uit de gevechtsanimaties, 2x, in huidskleur) en de Punch-
inslag (gevechtsanimatie, staat al in de ROM).
Paletindexen die de C-code animeert: BG 13 index 4-7 = lichtringen in de tunnel (één felle per stand).
Gebruik: python3 tools/grounded/brawly_transition.py [voorbeeld.png]"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
from gym_intro_lib import Encoder, text, text_width, save_sprite, preview_strip, scale, OUT, KEY, gba

PREVIEW = sys.argv[1] if len(sys.argv) > 1 else None

# ------------------------------------------------------------------ kleuren
# tunnel (BG 13)
T_WALL = [(72, 72, 80), (56, 56, 64), (40, 40, 48)]          # dichtbij -> veraf
T_RING = [(248, 248, 232), (120, 120, 128), (96, 96, 104), (80, 80, 88)]   # 4 cyclusstanden (de C-code draait ze)
T_FLOOR = [(32, 32, 40), (48, 40, 40)]
T_OPEN = [(248, 248, 248), (176, 208, 248), (24, 24, 32)]
P13 = T_WALL + T_RING + T_FLOOR + T_OPEN                      # 3 + 4 + 2 + 3 = 12
# octagon (BG 14)
O_CROWD = [(16, 16, 32), (32, 32, 56)]
O_MESH = [(136, 136, 152), (88, 88, 104)]
O_POST = [(16, 16, 24), (40, 72, 160)]
O_CANVAS = [(216, 216, 216), (184, 184, 192), (40, 40, 48)]
O_RED = (200, 32, 32)
O_FLASH = (248, 248, 248)
P14 = O_CROWD + O_MESH + O_POST + O_CANVAS + [O_RED, O_FLASH, (176, 184, 208)]   # 13
# omroeperbalk, LIVE-logo (BG 15)
B_RED, B_DRED, B_GOLD, B_DGOLD, B_WHITE, B_BLACK, B_GRAY = (200, 24, 24), (112, 8, 16), (248, 200, 48), (168, 112, 16), (248, 248, 248), (16, 16, 16), (160, 160, 168)
P15 = [B_RED, B_DRED, B_GOLD, B_DGOLD, B_WHITE, B_BLACK, B_GRAY]

VX, VY = 120, 68   # verdwijnpunt


# ------------------------------------------------------------------ 1. tunnel
def tunnel():
    im = Image.new('RGB', (240, 160), (0, 0, 0))
    px = im.load()
    for y in range(160):
        for x in range(240):
            dx, dy = (x + 0.5 - VX) / 120.0, (y + 0.5 - VY) / 92.0
            m = max(abs(dx), abs(dy))
            z = 1.0 / max(m, 1e-3)          # diepte
            if z > 7.0:
                # de opening: fel licht, met het gaas van de octagon als silhouet
                ox, oy = x - VX, y - VY
                if (ox + oy) % 4 == 0 or (ox - oy) % 4 == 0:
                    px[x, y] = T_OPEN[1]
                else:
                    px[x, y] = T_OPEN[0]
                if abs(ox) > 15 or abs(oy) > 11:
                    px[x, y] = T_OPEN[1]
                continue
            band = z * 3.0
            b = int(band)
            frac = band - b
            if abs(dy) >= abs(dx) and dy > 0:
                # vloer: donker met een loper
                px[x, y] = T_FLOOR[1] if abs(dx) < 0.18 * m * 1.0 + 0.0 and abs(dx / m) < 0.25 else T_FLOOR[0]
                if frac < 0.12:
                    px[x, y] = T_RING[b % 4]
                continue
            near = 0 if z < 2 else (1 if z < 4 else 2)
            px[x, y] = T_WALL[near]
            # ringen (deurlijsten) en lichtpanelen in het plafond
            if frac < 0.10:
                px[x, y] = T_RING[b % 4]
            elif abs(dy) >= abs(dx) and dy < 0 and abs(dx / m) < 0.35 and frac < 0.45:
                px[x, y] = T_RING[b % 4]
            elif abs(dx) > abs(dy) and abs(dy / m) < 0.55 and 0.2 < frac < 0.32 and ((x // 2 + y) % 2 == 0):
                px[x, y] = T_WALL[min(2, near + 1)]
    return im


def live_bug(im):
    d = ImageDraw.Draw(im)
    d.rectangle((8, 8, 55, 23), fill=B_BLACK)
    d.ellipse((12, 12, 19, 19), fill=B_RED)
    text(im, 22, 6, 'LIVE', B_WHITE, None)
    return im


# ------------------------------------------------------------------ 2. octagon
rr = random.Random(11)


def octagon():
    im = Image.new('RGB', (240, 160), (0, 0, 0))
    d = ImageDraw.Draw(im)
    # publiek in tribunes (drie rijen silhouetten)
    for row, (y0, col, r) in enumerate(((10, O_CROWD[0], 4), (26, O_CROWD[0], 5), (44, O_CROWD[1], 6))):
        x = -rr.randint(0, 6)
        while x < 250:
            d.ellipse((x - r, y0 - r, x + r, y0 + r), fill=col)
            d.ellipse((x - r * 2, y0 + r - 1, x + r * 2, y0 + r * 4), fill=col)
            x += r * 3 + rr.randint(0, 4)
    # kooi (de verre kant van de octagon): bovenrand, palen, gaas
    a = np.array(im)
    for y in range(32, 104):
        for x in range(240):
            if (x + y) % 8 == 0 or (x - y) % 8 == 0:
                a[y, x] = O_MESH[1] if y > 90 else O_MESH[0]
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 28, 239, 33), fill=O_POST[0])
    d.rectangle((0, 30, 239, 31), fill=O_POST[1])
    for px_ in (16, 224):
        d.rectangle((px_ - 5, 28, px_ + 5, 104), fill=O_POST[0])
        d.rectangle((px_ - 3, 36, px_ + 3, 100), fill=O_POST[1])
    # canvas met de octagonlijn in perspectief en DEWFORD op de mat
    d.rectangle((0, 104, 239, 159), fill=O_CANVAS[0])
    d.polygon([(0, 104), (239, 104), (239, 107), (0, 107)], fill=O_CANVAS[1])
    d.line([(0, 118), (36, 106), (204, 106), (239, 118)], fill=O_CANVAS[2], width=2)
    for k, ch in enumerate('DEWFORD'):
        pass
    s = 'DEWFORD'
    w = text_width(s, scale=2, spacing=3)
    tmp = Image.new('RGB', (240, 32), KEY)
    text(tmp, 120 - w // 2, 0, s, O_RED, None, scale=2, spacing=3)
    ta = np.array(tmp)
    # plat in perspectief: rijen samendrukken
    ia = np.array(im)
    for y in range(26):
        sy = int(y * 1.25)
        if sy >= 32:
            break
        row = ta[sy]
        m = (row != KEY).any(1)
        ia[128 + y][m] = O_RED
    im = Image.fromarray(ia)
    return im


def flash_tiles():
    """twee cameraflitsen (16x16): ster en kleine ster"""
    out = []
    for size in (7, 4):
        im = Image.new('RGB', (16, 16), (0, 0, 0))
        d = ImageDraw.Draw(im)
        d.line((8 - size, 8, 8 + size, 8), fill=O_FLASH)
        d.line((8, 8 - size, 8, 8 + size), fill=O_FLASH)
        d.line((8 - size // 2, 8 - size // 2, 8 + size // 2, 8 + size // 2), fill=(176, 184, 208))
        d.line((8 - size // 2, 8 + size // 2, 8 + size // 2, 8 - size // 2), fill=(176, 184, 208))
        d.ellipse((6, 6, 10, 10), fill=O_FLASH)
        out.append(im)
    return out


# ------------------------------------------------------------------ omroeperbalk (atlas: rij 0-4)
def banner():
    im = Image.new('RGB', (240, 40), (0, 0, 0))
    d = ImageDraw.Draw(im)
    # naamblok
    d.rectangle((0, 0, 151, 23), fill=B_RED)
    d.rectangle((0, 22, 151, 23), fill=B_DRED)
    text(im, 6, -3, 'BRAWLY', B_WHITE, B_DRED, scale=2, spacing=1)
    # gouden label
    d.rectangle((152, 4, 239, 23), fill=B_GOLD)
    d.rectangle((152, 22, 239, 23), fill=B_DGOLD)
    text(im, 158, 4, 'DOUBLE CHAMP', B_BLACK, None, font='narrow')
    # onderregel: het citaat
    d.rectangle((0, 24, 239, 39), fill=B_BLACK)
    text(im, 6, 23, '“Let me see if you’re worth the contract!”', B_WHITE, B_GRAY, font='narrow')
    return im


# ------------------------------------------------------------------ 4. kooigaas van dichtbij (met en zonder deuk)
def mesh(dent):
    im = Image.new('RGB', (240, 160), (0, 0, 0))
    px = im.load()
    cx, cy = 120, 80
    for y in range(160):
        for x in range(240):
            u, v = x - cx, y - cy
            k = 1.0
            if dent:
                r = math.sqrt(u * u + v * v * 1.3)
                k = 1.0 - 0.55 * (1 - r / 72.0) ** 2 if r < 72 else 1.0   # bol naar de camera: midden uitvergroot
                u, v = u * k, v * k
            a = (u + v) / 32.0
            b = (u - v) / 32.0
            fa, fb = a - math.floor(a), b - math.floor(b)
            w = 0.11
            on_a, on_b = fa < w, fb < w
            if on_a or on_b:
                hl = (fa < w * 0.45) if on_a else (fb < w * 0.45)
                px[x, y] = O_MESH[0] if hl else O_MESH[1]
                if dent and k < 0.8 and hl:
                    px[x, y] = O_FLASH
    return im


enc = Encoder('brawly', [P13, P14, P15])
tun = live_bug(tunnel())
enc.add(tun, label='tunnel')                         # 0
octo = octagon()
enc.add(octo, label='octagon')                       # 1
atlas = Image.new('RGB', (240, 160), (0, 0, 0))
atlas.paste(banner(), (0, 0))                        # rij 0-4: balk (30 x 5)
live = live_bug(Image.new('RGB', (64, 32), (0, 0, 0)))
atlas.paste(live, (0, 64))                           # rij 8-11: LIVE-logo (8 x 4)
enc.add(atlas, label='atlas')                        # 2
enc.add(mesh(False), label='mesh')                   # 3
enc.add(mesh(True), label='dent')                    # 4
enc.save()

# ------------------------------------------------------------------ vuist: de gevechtsanimatievuist, 2x, huidskleur
hf = Image.open(os.path.join(OUT, '..', 'battle_anims/sprites/hands_and_feet.png'))
fist_idx = np.array(hf)[0:32, 0:32]
# index 2 = vulling, 4 = omlijning (in de gevechten krijgt hij een ander palet): huid met licht en schaduw
SKIN, SKIN_L, SKIN_D, LINE = (216, 152, 96), (240, 192, 136), (168, 104, 56), (64, 32, 16)
fist = Image.new('RGB', (64, 64), KEY)
for y in range(32):
    for x in range(32):
        v = fist_idx[y, x]
        if not v:
            continue
        if v == 4:
            c = LINE
        elif y > 0 and fist_idx[y - 1, x] == 4:
            c = SKIN_L
        elif y < 31 and fist_idx[y + 1, x] == 4:
            c = SKIN_D
        else:
            c = SKIN
        for k in range(4):
            fist.putpixel((x * 2 + k % 2, y * 2 + k // 2), c)
# polsband (tape) onderaan de vuist
save_sprite('brawly_fist', fist)
# cameraflits als sprite (16 x 32: twee standen, groot en klein), zodat hij doorzichtig over publiek en gaas ligt
fl = Image.new('RGB', (16, 32), KEY)
for i, f in enumerate(flash_tiles()):
    fa = np.array(f)
    m = (fa != 0).any(2)
    sub = np.array(fl)
    sub[i * 16:i * 16 + 16][m] = fa[m]
    fl = Image.fromarray(sub)
save_sprite('brawly_flash', fl)

if PREVIEW:
    shots = [enc.render(m) for m in enc.maps]
    src = Image.open(os.path.join(OUT, '..', 'trainers/front_pics/leader_brawly.png'))
    ra = np.array(src.convert('RGBA'))
    ra[np.array(src) == 0] = 0
    br = Image.fromarray(ra)
    comp = shots[1].copy()
    comp.paste(br, (88, 44), br)
    bn = enc.render(enc.maps[2]).crop((0, 0, 240, 40))
    comp.paste(bn.crop((0, 0, 240, 40)), (0, 112))
    shots.append(comp)
    fa = np.array(fist.convert('RGBA'))
    fa[(np.array(fist) == KEY).all(2)] = 0
    fi = Image.fromarray(fa).resize((128, 128), Image.NEAREST)
    comp2 = Image.new('RGB', (240, 160))
    comp2.paste(fi, (56, 16), fi)
    m = shots[4]
    ma = np.array(m)
    mk = (ma != 0).any(2)
    c2 = np.array(comp2)
    c2[mk] = ma[mk]
    shots.append(Image.fromarray(c2))
    preview_strip(shots, PREVIEW)
