#!/usr/bin/env python3
"""Project Grounded: tiles, tilemaps, balsprite en baltabel voor B_TRANSITION_DAVE (Dave, Freed From Desire).

Penalty vanuit de schutter: voetbalveld met maaistrepen, goal frontaal met net, reclameborden en een volle tribune.
De bal vliegt vanaf de stip (groot, onderin) strak in de linkerbovenhoek, het net bolt, dan GOAL! groot in beeld.

Uitvoer (graphics/battle_transitions/):
- route_dave.png / .pal: ontdubbelde tiles (ook gespiegeld) en 2 paletten (normaal; GOAL! fel/wit voor het knipperen).
- route_dave.bin: DAVE_KEYS tilemaps van 32x22 (u16, palet 15 ingevuld; kolom 30/31 en rij 20/21 zijn aangevuld zodat
  het beeld kan schudden zonder randen), op volgorde: 0 = veld, 1..NET_KEYS = net bolt, daarna GOAL! op GOAL_SCALES.
- sprite_dave_ball.png / .pal: de bal (64x64, straal 30).
- route_dave_ball.bin: per vliegframe (FLIGHT frames) s16 x, y, schaal (256 = 1x) voor RT_SetSprite.
De baan wordt in 3D berekend (perspectief, steeds kleiner) en daarna geprojecteerd: geen delingen in de game.
Gebruik: python3 tools/grounded/dave_transition.py [voorbeeldmap]
"""
import math, os, random, struct, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as nd

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT = os.path.join(ROOT, 'graphics/battle_transitions/')
FONT = '/usr/share/fonts/truetype/freefont/FreeSansBoldOblique.ttf'
W, H = 240, 160
TW, TH = 32, 22                     # opgeslagen tilemapmaat (30x20 + aanvulling voor het schudden)

# palet (8-bit, wordt afgerond op GBA); index 0 = leeg (nergens gebruikt: het beeld is overal dekkend)
PAL = [(0, 0, 0), (16, 16, 24), (48, 128, 48), (80, 168, 64), (248, 248, 248), (184, 192, 208), (104, 112, 128),
       (24, 32, 64), (56, 80, 152), (208, 56, 48), (232, 184, 128), (112, 176, 240), (248, 224, 40), (248, 136, 24),
       (144, 24, 24), (40, 48, 88)]
OUTLINE, GDARK, GLIGHT, WHITE, LGREY, MGREY, NAVY, BLUE, RED, SKIN, SKY, YEL, ORA, DRED, SHADE = range(1, 16)
PAL_FLASH = list(PAL)               # GOAL! knippert: geel -> wit, oranje -> geel
PAL_FLASH[YEL] = (255, 255, 255)
PAL_FLASH[ORA] = (248, 224, 40)

# perspectief: f = brandpuntsafstand in px, camera 1 m hoog, goal op 13 m
F = 330.0
CAM_H = 1.0
GOAL_D = 13.0
YH = 96 - F * CAM_H / GOAL_D        # horizon (74,3; valt achter de tribune)
CX = 120


def proj(x, y, d):
    """wereld (x opzij, y hoogte, d diepte) -> scherm"""
    return CX + F * x / d, YH + F * (CAM_H - y) / d


def ground_y(d):
    return YH + F * CAM_H / d


# goalframe (voorkant, 7,32 x 2,44 m), achternet op 15 m
GL, GR = proj(-3.66, 0, GOAL_D)[0], proj(3.66, 0, GOAL_D)[0]       # 40,6 / 199,4
GTOP, GBOT = proj(0, 2.44, GOAL_D)[1], ground_y(GOAL_D)            # 43 / 96
BACK_D = 15.0
BL, BR = proj(-3.66, 0, BACK_D)[0], proj(3.66, 0, BACK_D)[0]
BTOP, BBOT = proj(0, 2.2, BACK_D)[1], ground_y(BACK_D)
POST = 4                                                          # paal-/latdikte in px
L0, R0, T0 = int(round(GL)) - POST + 1, int(round(GR)), int(round(GTOP)) - POST + 1
IMPACT = (L0 + POST + 8, T0 + POST + 8)                           # waar de bal het net raakt (de winkelhaak)

# ------------------------------------------------------------------ het veld (sleutelbeeld 0, zonder net)


def background():
    img = np.zeros((H, W), np.uint8)
    rng = random.Random(7)
    # dak van de tribune
    img[0:6, :] = NAVY
    img[6, :] = MGREY
    img[7, :] = SHADE
    # tribune: rijen supporters van 6 px, patroon herhaalt elke 32 px (ontdubbelt goed)
    shirts = [RED, BLUE, RED, SKY, BLUE, ORA, RED, MGREY]
    rows = {}
    by0, by1 = int(round(proj(0, 1, 17)[1])), int(round(ground_y(17)))
    for r in range(14):
        y0 = 8 + r * 6
        if y0 >= by0 - 2:
            break
        img[y0:y0 + 6, :] = SHADE if r % 2 else NAVY
        key = r % 4
        if key not in rows:
            rows[key] = [(x, rng.choice(shirts), rng.random() < 0.15) for x in range(1, 32, 4)]
        for x0, shirt, hands in rows[key]:
            for rep in range(0, W, 32):
                x = x0 + rep + (2 if r % 2 else 0)
                if x + 2 >= W:
                    continue
                img[y0 + 1:y0 + 3, x:x + 2] = SKIN                 # hoofd
                img[y0 + 3:y0 + 6, x - 1 if x > 0 else x:x + 3] = shirt
                if hands:                                          # juichende armen
                    img[y0, x - 1] = SKIN
                    img[y0, x + 2] = SKIN
    img[by0 - 2:by0, :] = OUTLINE
    # reclameborden (1 m hoog op 17 m): blokken van 48 px, eenvoudige witte logo's
    cols = [RED, BLUE, SKY, BLUE]                                # geen GOAL!-geel: dat knippert straks
    for i, x0 in enumerate(range(0, W, 48)):
        c = cols[i % 4]
        img[by0:by1, x0:x0 + 48] = c
        mark = WHITE if c != SKY else BLUE
        mid = (by0 + by1) // 2
        if i % 2 == 0:                                             # streep + bol
            img[mid - 1:mid + 2, x0 + 10:x0 + 30] = mark
            img[mid - 4:mid + 5, x0 + 33:x0 + 40] = mark
        else:                                                      # pijltjes
            for k in range(3):
                for j in range(5):
                    img[mid - 4 + j, x0 + 12 + k * 9 + j] = mark
                    img[mid + 4 - j, x0 + 12 + k * 9 + j] = mark
        img[by0, x0:x0 + 48] = LGREY
    img[by1 - 1, :] = OUTLINE
    # gras met maaistrepen (banden van 1,5 m evenwijdig aan de doellijn)
    y = by1
    d = 17.0
    while y < H:
        d -= 1.5
        yn = int(round(ground_y(d))) if d > 0.5 else H
        band = int(round((17.0 - d) / 1.5)) % 2
        img[y:min(yn, H), :] = GLIGHT if band else GDARK
        y = yn
    # lijnen: doellijn en de voorkant van het doelgebied (5,5 m), de stip onderin
    gy = int(round(GBOT))
    img[gy:gy + 2, :] = WHITE
    y6 = int(round(ground_y(GOAL_D - 5.5)))
    img[y6:y6 + 3, :] = WHITE
    yy, xx = np.mgrid[:H, :W]
    spot = ((xx - CX) / 9.0) ** 2 + ((yy - 155) / 3.0) ** 2 < 1
    img[spot] = WHITE
    return img


def mesh(x, y):
    """ruitjesnet, periode 8 (ontdubbelt per tile)"""
    return (x + y) % 8 == 0 or (x - y) % 8 == 0


def net_layer(img, bulge=0.0, sigma=11.0):
    """net in het goal; bulge > 0 = het net bolt bij IMPACT (ruitjes duwen naar buiten, schaduw in het midden)"""
    out = img.copy()
    l, r, t, b = int(round(GL)), int(round(GR)), int(round(GTOP)), int(round(GBOT))
    ix, iy = IMPACT
    for y in range(t, b):
        for x in range(l, r):
            dx, dy = x - ix, y - iy
            rr = math.hypot(dx, dy)
            sx, sy = x, y
            if bulge and rr < 3 * sigma:
                k = bulge * math.exp(-(rr * rr) / (sigma * sigma))
                if rr > 0:
                    sx, sy = x - dx / rr * k, y - dy / rr * k      # ruitjes van het midden af geduwd
                if abs(bulge) > 1 and rr < sigma * 0.9 * min(1.0, abs(bulge) / 5):
                    out[y, x] = NAVY if out[y, x] not in (WHITE,) else SHADE   # de kuil in het net
            # zijnetten en dak: donkerder ruitjes, achternet licht
            inback = BL <= x < BR and BTOP <= y
            on = mesh(int(round(sx)), int(round(sy)))
            if on:
                out[y, x] = LGREY if inback else MGREY
    # naden waar zijnet en dak aan het achternet vastzitten
    for (x0, y0, x1, y1) in ((GL, GTOP, BL, BTOP), (GR, GTOP, BR, BTOP), (GL, GBOT, BL, BBOT), (GR, GBOT, BR, BBOT)):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(n + 1):
            out[int(round(y0 + (y1 - y0) * i / n)), int(round(x0 + (x1 - x0) * i / n))] = LGREY
    out[int(round(BTOP)), int(round(BL)):int(round(BR))] = LGREY
    out[int(round(BTOP)):int(round(BBOT)), int(round(BL))] = LGREY
    out[int(round(BTOP)):int(round(BBOT)), int(round(BR)) - 1] = LGREY
    return out


def frame_layer(img):
    """palen en lat: wit met grijze schaduwkant en een donkere omlijning"""
    out = img.copy()
    gb = int(round(GBOT)) + 1
    for x0 in (L0, R0):
        out[T0:gb, x0 - 1] = OUTLINE
        out[T0:gb, x0 + POST] = OUTLINE
        out[T0:gb, x0:x0 + POST] = WHITE
        out[T0:gb, x0 + POST - 1] = LGREY
    out[T0 - 1, L0 - 1:R0 + POST + 1] = OUTLINE
    out[T0 + POST, L0 + POST:R0] = OUTLINE
    out[T0:T0 + POST, L0:R0 + POST] = WHITE
    out[T0 + POST - 1, L0 + POST:R0] = LGREY
    # schaduw van de lat op het net
    for x in range(L0 + POST, R0):
        if out[T0 + POST + 1, x] != OUTLINE:
            out[T0 + POST + 1, x] = SHADE
    # voet van de palen op het gras
    out[gb, L0 - 1:L0 + POST + 1] = OUTLINE
    out[gb, R0 - 1:R0 + POST + 1] = OUTLINE
    return out


def field(bulge=0.0):
    return frame_layer(net_layer(background(), bulge))


# ------------------------------------------------------------------ GOAL!

def goal_text(scale):
    """GOAL! met verloop (geel -> oranje), dikke zwarte rand en een donkerrode schaduw. Geeft (indexen, masker)."""
    size = int(round(58 * scale))
    font = ImageFont.truetype(FONT, size)
    x0, y0, x1, y1 = font.getbbox('GOAL!')
    m = Image.new('L', (x1 - x0 + 4, y1 - y0 + 4), 0)
    ImageDraw.Draw(m).text((2 - x0, 2 - y0), 'GOAL!', font=font, fill=255)
    a = np.array(m) > 110
    a = nd.binary_dilation(a, iterations=max(1, int(round(1.4 * scale))))      # zwaarder lettertype
    h, w = a.shape
    pad = 6
    core = np.zeros((h + 2 * pad, w + 2 * pad), bool)
    core[pad:pad + h, pad:pad + w] = a
    ys = np.nonzero(core.any(1))[0]
    top, bot = ys[0], ys[-1]
    idx = np.zeros(core.shape, np.uint8)
    # verloop in drie banden, glansstreep bovenin
    for y in range(core.shape[0]):
        f = (y - top) / max(1, bot - top)
        c = WHITE if f < 0.12 else (YEL if f < 0.55 else ORA)
        idx[y][core[y]] = c
    rim = nd.binary_dilation(core, iterations=2) & ~core
    shadow = np.zeros_like(core)
    sh = max(2, int(round(3 * scale)))
    shadow[sh:, sh:] = (core | rim)[:-sh, :-sh]
    shadow &= ~(core | rim)
    shrim = nd.binary_dilation(shadow) & ~(core | rim | shadow)
    idx[shadow] = DRED
    idx[shrim] = OUTLINE
    idx[rim] = OUTLINE
    return idx


GOAL_SCALES = [0.55, 1.15, 1.0]
GOAL_CY = 112                         # midden van de tekst (onder de bal in de winkelhaak)


def with_goal(base, scale):
    img = base.copy()
    t = goal_text(scale)
    h, w = t.shape
    ox, oy = CX - w // 2, GOAL_CY - h // 2
    for y in range(h):
        for x in range(w):
            if t[y, x] and 0 <= y + oy < H and 0 <= x + ox < W:
                img[y + oy, x + ox] = t[y, x]
    return img


# ------------------------------------------------------------------ bal (sprite) en zijn baan

BALL_R = 30


def ball_sprite():
    """klassieke bal: wit met zwarte vijfhoeken, schaduw rechtsonder, glans linksboven"""
    S = 4
    N = 64 * S
    yy, xx = np.mgrid[:N, :N]
    cx = cy = 32 * S
    r = BALL_R * S
    dx, dy = (xx + 0.5 - cx) / r, (yy + 0.5 - cy) / r
    rr = dx * dx + dy * dy
    inside = rr < 1
    dz = np.sqrt(np.clip(1 - rr, 0, 1))
    # vijfhoeken: punten op een icosaëder (12 hoekpunten), vlakjes rond de hoekpunten die naar ons toe staan
    phi = (1 + 5 ** 0.5) / 2
    verts = []
    for a in (-1, 1):
        for b in (-phi, phi):
            verts += [(0, a, b), (a, b, 0), (b, 0, a)]
    verts = np.array(verts, float)
    verts /= np.linalg.norm(verts[0])
    rot = 0.35
    c, s = math.cos(rot), math.sin(rot)
    verts = verts @ np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]) @ np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    pent = np.zeros((N, N), bool)
    seam = np.zeros((N, N), bool)
    pts = np.stack([dx, dy, dz], -1)
    dots = np.einsum('ijk,vk->ijv', pts, verts)
    best = dots.max(-1)
    pent = inside & (best > 0.955)
    second = np.sort(dots, -1)[..., -2]
    seam = inside & (best - second < 0.03) & ~pent
    light = np.clip(-dx * 0.45 - dy * 0.55 + dz * 0.75, 0, 1)
    out = np.zeros((64, 64), np.uint8)
    # palet: 0 leeg, 1 omlijning, 2 zwart vlak, 3 donkergrijs, 4 grijs, 5 lichtgrijs, 6 wit
    big = np.zeros((N, N), np.uint8)
    big[inside] = np.where(light[inside] > 0.62, 6, np.where(light[inside] > 0.35, 5, np.where(light[inside] > 0.15, 4, 3)))
    big[seam] = np.where(light[seam] > 0.4, 4, 3)
    big[pent] = 2
    for y in range(64):
        for x in range(64):
            blk = big[y * S:(y + 1) * S, x * S:(x + 1) * S]
            ins = inside[y * S:(y + 1) * S, x * S:(x + 1) * S].mean()
            if ins >= 0.5:
                vals, cnt = np.unique(blk[blk > 0], return_counts=True)
                out[y, x] = vals[cnt.argmax()]
    rim = nd.binary_dilation(out > 0) & (out == 0)
    out[rim] = 1
    # glansplek
    for (x, y) in ((22, 20), (23, 20), (22, 21), (21, 21), (24, 19), (21, 22)):
        if out[y, x] not in (2,):
            out[y, x] = 7
    return out


BALL_PAL = [(0, 0, 0), (16, 16, 24), (24, 24, 32), (72, 72, 88), (152, 152, 168), (208, 208, 216), (248, 248, 248),
            (255, 255, 255)] + [(0, 0, 0)] * 8

FLIGHT = 28          # frames van trap tot net (= 1 tel bij 128 BPM; zie RTDave_* in battle_transition.c)
START = (128, 140, 2.0)     # schermpositie + diepte (m) van de bal op de stip
START_R = 25.0


def flight():
    """3D-baan (rechtlijnig + een beetje effect), geprojecteerd; schaal = straal / BALL_R * 256"""
    sx, sy, d0 = START
    R = START_R * d0 / F                               # balstraal in meters (fictief: de bal is wat groot)
    X0, Y0 = (sx - CX) * d0 / F, CAM_H - (sy - YH) * d0 / F
    ex, ey = IMPACT
    d1 = GOAL_D + 0.35                                 # net in
    X1, Y1 = (ex - CX) * d1 / F, CAM_H - (ey - YH) * d1 / F
    rows = []
    for i in range(FLIGHT + 1):
        u = i / FLIGHT
        d = d0 + (d1 - d0) * u
        curl = math.sin(u * math.pi) * 0.45             # effect: buigt eerst naar buiten (links) en draait terug
        X = X0 + (X1 - X0) * u - curl
        Y = Y0 + (Y1 - Y0) * u + math.sin(u * math.pi) * 0.25
        x, y = proj(X, Y, d)
        r = R * F / d + 2.5 * u                        # iets groter dan echt, anders verdwijnt hij in het net
        rows.append((int(round(x)), int(round(y)), int(round(r / BALL_R * 256))))
    return rows


# ------------------------------------------------------------------ opslaan


def gba(c):
    return tuple(min(248, (v >> 3) << 3) for v in c)


def tiles_of(img):
    return [tuple(img[r * 8:(r + 1) * 8, c * 8:(c + 1) * 8].flatten()) for r in range(20) for c in range(30)]


NET_BULGE = [5.5, 7.5, 3.0, -2.5]     # net bolt (impact, uiterst, terug, doorzwaaien)


def build():
    keys = [field()]
    for b in NET_BULGE:
        keys.append(field(b))
    for s in GOAL_SCALES:
        keys.append(with_goal(keys[0], s))
    for k in keys:
        assert (k > 0).all(), 'gat in het beeld'
    tiles, lookup, maps = [], {}, []
    for img in keys:
        tm = []
        for t in tiles_of(img):
            if t not in lookup:
                a = np.array(t).reshape(8, 8)
                n = len(tiles) + 1
                tiles.append(t)
                lookup[t] = n
                for flip, arr in ((1 << 10, a[:, ::-1]), (2 << 10, a[::-1, :]), (3 << 10, a[::-1, ::-1])):
                    lookup.setdefault(tuple(arr.flatten()), n | flip)
            tm.append(lookup[t] | (15 << 12))
        # aanvullen tot 32x22: kolom 30 = kolom 29, 31 = kolom 0; rij 20 = rij 19, 21 = rij 0 (schudden zonder gaten)
        full = []
        rows = [tm[r * 30:(r + 1) * 30] for r in range(20)]
        rows = rows + [rows[19], rows[0]]
        for row in rows:
            full += row + [row[29], row[0]]
        maps.append(full)
    return keys, tiles, maps


def save(tiles, maps, path):
    allt = [(0,) * 64] + tiles
    assert len(allt) <= 767, 'te veel tiles: %d' % len(allt)
    cols = 16
    rows = (len(allt) + cols - 1) // cols
    img = Image.new('P', (cols * 8, rows * 8))
    for i, t in enumerate(allt):
        ox, oy = (i % cols) * 8, (i // cols) * 8
        for p, v in enumerate(t):
            img.putpixel((ox + p % 8, oy + p // 8), int(v))
    img.putpalette([v for c in PAL for v in gba(c)] + [0] * (768 - 48))
    img.save(OUT + 'route_dave.png')
    with open(OUT + 'route_dave.pal', 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n32\n')
        for pal in (PAL, PAL_FLASH):
            for c in pal:
                fp.write('%d %d %d\n' % gba(c))
    with open(OUT + 'route_dave.bin', 'wb') as fp:
        for tm in maps:
            fp.write(struct.pack('<%dH' % (TW * TH), *tm))
    b = ball_sprite()
    bi = Image.fromarray(b, 'P')
    bi.putpalette([v for c in BALL_PAL for v in gba(c)] + [0] * (768 - 48))
    bi.save(OUT + 'sprite_dave_ball.png')
    with open(OUT + 'sprite_dave_ball.pal', 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n16\n')
        for c in BALL_PAL:
            fp.write('%d %d %d\n' % gba(c))
    fl = flight()
    with open(OUT + 'route_dave_ball.bin', 'wb') as fp:
        for x, y, s in fl:
            fp.write(struct.pack('<3h', x, y, s))
    print('dave:', len(allt), 'tiles,', len(maps), 'tilemaps; bal', len(fl), 'frames, schaal', fl[0][2], '->', fl[-1][2])
    return b, fl


def preview(keys, ball, fl, d):
    pal = [gba(c) for c in PAL]
    bpal = [gba(c) for c in BALL_PAL]
    for i, k in enumerate(keys):
        im = Image.fromarray(np.array([[pal[v] for v in row] for row in k], np.uint8))
        if i == 0:
            # baan van de bal erop (elke 4e frame)
            for x, y, s in fl[::4] + [fl[-1]]:
                r = max(1, int(round(s / 256 * BALL_R)))
                bimg = Image.fromarray(np.array([[bpal[v] for v in row] for row in ball], np.uint8))
                mask = Image.fromarray(((ball > 0) * 255).astype(np.uint8))
                sz = max(2, 2 * r)
                im.paste(bimg.resize((sz * 64 // 60, sz * 64 // 60), Image.NEAREST), (x - sz * 32 // 60, y - sz * 32 // 60),
                         mask.resize((sz * 64 // 60, sz * 64 // 60), Image.NEAREST))
        im.resize((W * 3, H * 3), Image.NEAREST).save(os.path.join(d, 'dave_key%02d.png' % i))


if __name__ == '__main__':
    keys, tiles, maps = build()
    ball, fl = save(tiles, maps, None)
    seen = set()
    for i, m in enumerate(maps):
        new = set(x & 0x3FF for x in m) - seen
        seen |= new
        print('  tilemap %d: %d nieuwe tiles' % (i, len(new)))
    if len(sys.argv) > 1:
        os.makedirs(sys.argv[1], exist_ok=True)
        preview(keys, ball, fl, sys.argv[1])
