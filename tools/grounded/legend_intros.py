#!/usr/bin/env python3
"""Project Grounded: lichte gevechtsintro's van vijf legendaries (Lugia, Ho-Oh, Volcanion, Hoopa, Forces of Nature).
Zelfde aanpak als de gymleider-intro's (gym_intro_lib.py): een paar stilstaande BG0-beelden (paletten 13-15) en de
beweging in C (src/data/legend_intros.h): sprites (echte frontsprites en gevechtsanimatie-art uit de ROM), paletcycli,
tilemap-blokken, vensters en scanline-effecten.

Uitvoer in graphics/battle_transitions/legend_<naam>.png/.pal + legend_<naam>_maps.bin (+ eigen sprites).
- lugia:     ZEE (lichtbundels van boven, banden die in C donkerder worden), HOOFD (Lugia's eigen kop uit de frontsprite,
             Scale2x x2), WERVEL (spiraal met fasen 1-8 in palet 15 voor de paletcyclus)
- hooh:      SCHEMER (Bell Tower-silhouet bij zonsondergang), REGENBOOG (zelfde + regenboog achter de toren)
- volcanion: METER (manometer op een geklonken plaat), GATEN (zelfde, klinknagels eruit); sprites naald en klinknagel
- hoopa:     PORTAAL (gouden ring met een wervel van fasen in palet 14); sprite hand (Hoopa's hand uit de
             gevechtsanimatie, x4)
- forces:    TV (weerbericht met de echte Hoenn-kaart uit de PokéNav), TV_T/TV_TH/TV_L (andere onderbalk), SCHEUR
             (Landorus: barsten), BRAND (Thundurus: inslagen), KAART_T/KAART_I (usage stats)
Gebruik: python3 tools/grounded/legend_intros.py [voorbeeldmap]"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
from gym_intro_lib import Encoder, text, text_width, outlined_text, save_sprite, preview_strip, scale, OUT, KEY, gba, ROOT

PREVIEW = sys.argv[1] if len(sys.argv) > 1 else None
PFX = 'legend_'


def jasc(path):
    L = open(path).read().split('\n')
    n = int(L[2])
    return [tuple(int(v) for v in l.split()[:3]) for l in L[3:3 + n]]


def mon_frame(name, frame=0, sub=None):
    """Frontsprite (frame 0) als RGB met KEY als doorzichtig."""
    d = os.path.join(ROOT, 'graphics/pokemon', name)
    im = Image.open(os.path.join(d, 'anim_front.png'))
    pal = jasc(os.path.join(d, 'normal.pal'))
    a = np.array(im)[frame * 64:frame * 64 + 64]
    rgb = np.array(pal, np.uint8)[a]
    rgb[a == 0] = KEY
    return Image.fromarray(rgb), a, pal


def scale2x(a):
    """Scale2x (EPX) op een indexbeeld."""
    h, w = a.shape
    p = np.pad(a, 1, mode='edge')
    B, D, E, F, H = p[:-2, 1:-1], p[1:-1, :-2], p[1:-1, 1:-1], p[1:-1, 2:], p[2:, 1:-1]
    o = np.zeros((h * 2, w * 2), a.dtype)
    c = (B != H) & (D != F)
    o[0::2, 0::2] = np.where(c & (D == B), D, E)
    o[0::2, 1::2] = np.where(c & (B == F), F, E)
    o[1::2, 0::2] = np.where(c & (D == H), D, E)
    o[1::2, 1::2] = np.where(c & (H == F), F, E)
    return o


def ctext(im, cx, y, s, fg, shadow=None, font='normal', sc=1, sp=0):
    text(im, cx - text_width(s, font, sc, sp) // 2, y, s, fg, shadow, font, sc, sp)


def dither(y, x, f):
    """Bayer 4x4: TRUE als f (0..1) deze pixel 'aan' zet."""
    B = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))
    return f * 16 > B[y & 3][x & 3]


def save_preview(name, imgs):
    if PREVIEW:
        preview_strip(imgs, os.path.join(PREVIEW, 'legend_%s.png' % name), k=2, cols=3)


# ================================================================== Lugia
LUGIA_SEA = [(120, 200, 240), (88, 168, 224), (64, 136, 208), (40, 104, 184), (24, 72, 152), (16, 48, 120)]
LUGIA_RAY = [(184, 232, 248), (144, 216, 248)]
LUGIA_VORTEX = [(248, 248, 248), (200, 224, 248), (152, 192, 240), (104, 152, 224), (64, 112, 200), (40, 72, 160),
                (24, 48, 120), (16, 32, 88)]


LUGIA_CROP = (2, 30, 30, 58)   # x0, y0, x1, y1 in de frontsprite: de kop met de oogvlek (x4 = 112 x 112)


def lugia():
    # --- zee: banden van boven naar beneden (index 1-6), lichtbundels (7, 8) schuin van boven
    sea = Image.new('RGB', (240, 160))
    px = sea.load()
    rays = [(40, 18, 0.30), (96, 12, 0.22), (150, 22, 0.34), (206, 14, 0.26)]
    for y in range(160):
        f = y * 6 / 160
        for x in range(240):
            b = int(f)
            if b < 5 and dither(y, x, (f - b - 0.6) / 0.4):
                b += 1
            c = LUGIA_SEA[min(b, 5)]
            for rx, rw, sl in rays:
                cx = rx + (y - 0) * sl
                w = rw * (1 - y / 190)
                if abs(x - cx) < w and y < 150:
                    edge = abs(x - cx) > w * 0.55
                    if y < 120 or dither(y, x, (150 - y) / 30):
                        c = LUGIA_RAY[1 if edge else 0]
            px[x, y] = c
    # --- Lugia's kop uit de eigen frontsprite (frame 0), Scale2x twee keer (x4)
    _, a, pal = mon_frame('lugia')
    crop = a[LUGIA_CROP[1]:LUGIA_CROP[3], LUGIA_CROP[0]:LUGIA_CROP[2]]
    big = scale2x(scale2x(crop))
    head = Image.new('RGB', (240, 160), (0, 0, 0))
    hp = head.load()
    oy, ox = 80 - big.shape[0] // 2, 120 - big.shape[1] // 2
    for y in range(big.shape[0]):
        for x in range(big.shape[1]):
            if big[y, x]:
                hp[ox + x, oy + y] = pal[big[y, x]]
    head_cols = [pal[i] for i in range(1, 16)]
    # --- wervel: tweearmige logaritmische spiraal (180 graden symmetrisch: de helft van de tiles via flips), fasen 1-8
    vort = Image.new('RGB', (240, 160), (0, 0, 0))
    vp = vort.load()
    for y in range(160):
        for x in range(240):
            dx, dy = x - 119.5, y - 79.5
            r = math.hypot(dx, dy)
            if r < 6:
                vp[x, y] = LUGIA_VORTEX[0]
                continue
            th = math.atan2(dy, dx)
            ph = (th / (2 * math.pi) * 2 + math.log(r) * 1.6) % 1.0
            vp[x, y] = LUGIA_VORTEX[int(ph * 8) % 8]
    enc = Encoder('lugia', [LUGIA_SEA + LUGIA_RAY, head_cols, LUGIA_VORTEX], prefix=PFX)
    enc.add(sea, 0, 'zee')
    enc.add(head, 1, 'kop')
    enc.add(vort, 2, 'wervel')
    enc.save()
    # welke index is de donkerblauwe oogvlek (licht op in C)?
    print('  lugia: oogvlek = palet 14 index', [i for i in range(1, 16) if pal[i] == (40, 48, 136)])
    save_preview('lugia', [sea, head, vort])


# ================================================================== Ho-Oh
HOOH_SKY = [(72, 40, 104), (136, 56, 120), (208, 80, 104), (240, 128, 72), (248, 184, 88)]
HOOH_SIL, HOOH_SIL2, HOOH_WIN = (24, 8, 24), (48, 16, 40), (248, 224, 120)
HOOH_SUN = [(248, 240, 176), (248, 208, 120)]
HOOH_EMBER = [(248, 216, 96), (240, 144, 48), (200, 72, 32)]   # drie fasen (fonkelen in C)
HOOH_RAIN = [(232, 48, 48), (248, 136, 40), (248, 224, 64), (88, 200, 72), (56, 160, 232), (80, 88, 216), (152, 72, 200)]


def hooh_scene(rainbow):
    im = Image.new('RGB', (240, 160))
    px = im.load()
    # lucht: banden met dither, horizon op y 132
    for y in range(160):
        f = y / 132 * 5
        for x in range(240):
            b = int(f)
            if b < 4 and dither(y, x, (f - b - 0.55) / 0.45):
                b += 1
            px[x, y] = HOOH_SKY[min(b, 4)]
    d = ImageDraw.Draw(im)
    # zon laag aan de horizon
    d.ellipse((34, 104, 82, 152), fill=HOOH_SUN[1])
    d.ellipse((40, 110, 76, 146), fill=HOOH_SUN[0])
    if rainbow:
        cx, cy = 120, 196
        for y in range(160):
            for x in range(240):
                r = math.hypot(x - cx, y - cy)
                k = int((r - 150) // 4)
                if 0 <= k < 7 and y < 136:
                    px[x, y] = HOOH_RAIN[6 - k]   # rood buiten
    # heuvels en bomen
    for x in range(240):
        h = 136 + 6 * math.sin(x / 23) + 4 * math.sin(x / 9 + 1)
        d.line((x, int(h), x, 159), fill=HOOH_SIL)
    rnd = random.Random(7)
    for tx in list(range(4, 100, 13)) + list(range(206, 240, 11)):
        th = rnd.randint(14, 24)
        base = 136 + 6 * math.sin(tx / 23)
        d.polygon([(tx - 6, base), (tx + 6, base), (tx, base - th)], fill=HOOH_SIL)
    # de Bell Tower (Tin Tower): negen lagen, opgekrulde dakranden, spits
    cx, base = 156, 140
    y = base
    for i in range(9):
        w = 30 - i * 2.4
        hh = 11 - i * 0.4
        top = y - hh
        d.rectangle((cx - w * 0.62, top + 3, cx + w * 0.62, y), fill=HOOH_SIL)
        # dak: breder, met opgekrulde punten
        d.polygon([(cx - w - 4, top + 4), (cx - w, top + 1), (cx + w, top + 1), (cx + w + 4, top + 4),
                   (cx + w * 0.7, top + 2), (cx - w * 0.7, top + 2)], fill=HOOH_SIL)
        d.polygon([(cx - w * 0.82, top + 1), (cx + w * 0.82, top + 1), (cx + w * 0.55, top - 3), (cx - w * 0.55, top - 3)],
                  fill=HOOH_SIL)
        d.line((cx - w - 4, top + 4, cx - w - 5, top + 1), fill=HOOH_SIL)
        d.line((cx + w + 4, top + 4, cx + w + 5, top + 1), fill=HOOH_SIL)
        # verlichte ramen
        for wx in (-w * 0.35, 0, w * 0.35):
            if i % 2 == 0 or wx == 0:
                d.rectangle((cx + wx - 1, top + 6, cx + wx, top + 8), fill=HOOH_WIN)
        y = top - 2
    d.line((cx, y, cx, y - 14), fill=HOOH_SIL)
    d.line((cx - 1, y - 4, cx + 1, y - 4), fill=HOOH_SIL)
    d.line((cx - 2, y, cx + 2, y), fill=HOOH_SIL)
    # rand van het silhouet tegen de lucht (warm randlicht aan de zonkant)
    a = np.array(im)
    sil = (a == HOOH_SIL).all(2)
    edge = sil & ~np.roll(sil, 1, 1)
    edge[:, 0] = False
    a[edge] = HOOH_SIL2
    # gloeiende sintels rond de toren (onder de regenboog), drie fasen
    rnd = random.Random(21)
    for k in range(28):
        x, y = rnd.randrange(112, 204), rnd.randrange(84, 134)
        c = HOOH_EMBER[k % 3]
        a[y, x] = c
        if k % 4 == 0:
            a[y + 1, x] = c
    return Image.fromarray(a)


def hooh():
    dusk, rain = hooh_scene(False), hooh_scene(True)
    p13 = HOOH_SKY + [HOOH_SIL, HOOH_SIL2, HOOH_WIN] + HOOH_SUN + HOOH_EMBER
    p14 = HOOH_SKY + HOOH_RAIN + [HOOH_SIL, HOOH_SIL2, HOOH_WIN]
    enc = Encoder('hooh', [p13, p14, [(248, 248, 248)]], prefix=PFX)
    enc.add(dusk, 0, 'schemer')
    m = enc.add(rain, None, 'regenboog')
    enc.save()
    # gouden veren (White Feather uit de ROM, eigen palet): wordt in C gebruikt
    save_preview('hooh', [dusk, rain])


# ================================================================== Volcanion
VOL_PLATE = [(56, 52, 60), (72, 68, 76), (88, 84, 92), (40, 36, 44)]
VOL_RIVET = [(168, 160, 152), (112, 104, 100), (32, 28, 32)]
VOL_HOLE = [(16, 12, 16)]
VOL_TEXT = (216, 200, 168)
VOL_BRASS = [(232, 192, 96), (184, 136, 56), (120, 80, 32)]
VOL_FACE = [(240, 232, 208), (208, 196, 168)]
VOL_INK = (40, 32, 32)
VOL_ZONES = [(96, 176, 80), (232, 192, 48), (216, 48, 32), (136, 24, 16)]
RIVETS = [(1, 1), (27, 1), (1, 17), (27, 17), (5, 1), (23, 1), (1, 9), (27, 9), (5, 17), (23, 17)]  # in tiles (2x2)
GAUGE_C, GAUGE_R = (120, 76), 58


def volcanion_img(holes):
    im = Image.new('RGB', (240, 160), VOL_PLATE[1])
    d = ImageDraw.Draw(im)
    px = im.load()
    # geborstelde plaat met een rand (patroon herhaalt per tile: weinig tiles)
    for y in range(160):
        for x in range(240):
            v = ((x & 7) * 5 + (y & 7) * 3 + ((x & 7) * (y & 7))) % 23
            if v == 0:
                px[x, y] = VOL_PLATE[2]
            elif v == 11:
                px[x, y] = VOL_PLATE[0]
    d.rectangle((0, 0, 239, 159), outline=VOL_PLATE[3], width=3)
    d.rectangle((4, 4, 235, 155), outline=VOL_PLATE[2])
    for tx, ty in RIVETS:
        x, y = tx * 8 + 8, ty * 8 + 8
        if holes:
            d.ellipse((x - 4, y - 4, x + 3, y + 3), fill=VOL_HOLE[0], outline=VOL_PLATE[3])
        else:
            d.ellipse((x - 5, y - 5, x + 4, y + 4), fill=VOL_RIVET[1], outline=VOL_RIVET[2])
            d.ellipse((x - 4, y - 4, x + 1, y + 1), fill=VOL_RIVET[0])
    # de meter: messing rand, wijzerplaat, zones, streepjes
    cx, cy = GAUGE_C
    R = GAUGE_R
    d.ellipse((cx - R - 2, cy - R - 2, cx + R + 2, cy + R + 2), fill=VOL_BRASS[2])
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=VOL_BRASS[1])
    d.ellipse((cx - R + 2, cy - R + 1, cx + R - 3, cy + R - 4), fill=VOL_BRASS[0])
    d.ellipse((cx - R + 5, cy - R + 5, cx + R - 5, cy + R - 5), fill=VOL_BRASS[2])
    d.ellipse((cx - R + 6, cy - R + 6, cx + R - 6, cy + R - 6), fill=VOL_FACE[0])
    # zones langs de rand: hoek -135 (links onder) .. +135 (rechts onder), 0 = boven
    for y in range(cy - R, cy + R):
        for x in range(cx - R, cx + R):
            r = math.hypot(x - cx + 0.5, y - cy + 0.5)
            if R - 15 <= r < R - 8:
                ang = math.degrees(math.atan2(x - cx + 0.5, -(y - cy + 0.5)))
                if -135 <= ang <= 135:
                    z = 0 if ang < 20 else 1 if ang < 70 else 2 if ang < 112 else 3
                    px[x, y] = VOL_ZONES[z]
    for k in range(28):
        ang = math.radians(-135 + k * 10)
        r0 = R - 22 if k % 3 == 0 else R - 18
        x0, y0 = cx + r0 * math.sin(ang), cy - r0 * math.cos(ang)
        x1, y1 = cx + (R - 15) * math.sin(ang), cy - (R - 15) * math.cos(ang)
        d.line((x0, y0, x1, y1), fill=VOL_INK)
    ctext(im, cx, cy + 14, 'PSI', VOL_INK, None, 'small')
    ctext(im, cx, cy + 24, 'x1000', VOL_FACE[1], None, 'small')
    for s, ang in (('fine', -100), ('hm', 45), ('NOPE', 105)):
        a = math.radians(ang)
        r = R - 30
        x, y = cx + r * math.sin(a), cy - r * math.cos(a)
        ctext(im, int(x), int(y) - 8, s, VOL_ZONES[2] if s == 'NOPE' else VOL_INK, None, 'small')
    # opschrift onder op de plaat
    ctext(im, 120, 137, 'VOLCANION STEAM WORKS', VOL_TEXT, VOL_PLATE[3], 'small')
    ctext(im, 120, 2, 'DO NOT TAP THE GLASS', VOL_TEXT, VOL_PLATE[3], 'small')
    return im


def volcanion():
    a, b = volcanion_img(False), volcanion_img(True)
    p13 = VOL_PLATE + VOL_RIVET + VOL_HOLE + [VOL_TEXT]
    p14 = VOL_BRASS + VOL_FACE + [VOL_INK] + VOL_ZONES + [VOL_PLATE[3], VOL_PLATE[1], VOL_TEXT, VOL_PLATE[0], VOL_PLATE[2]]
    enc = Encoder('volcanion', [p13, p14, [(248, 248, 248)]], prefix=PFX)
    enc.add(a, None, 'meter')
    enc.add(b, None, 'gaten')
    enc.save()
    # naald (64x64, affine; wijst omhoog, draaipunt in het midden)
    nd = Image.new('RGB', (64, 64), KEY)
    d = ImageDraw.Draw(nd)
    d.polygon([(31, 3), (33, 3), (35, 32), (29, 32)], fill=(200, 32, 24))
    d.polygon([(32, 3), (33, 3), (34, 30), (32, 30)], fill=(248, 96, 72))
    d.polygon([(30, 32), (34, 32), (33, 42), (31, 42)], fill=(64, 24, 24))
    d.ellipse((27, 27, 36, 36), fill=(40, 32, 32))
    d.ellipse((29, 29, 33, 33), fill=(184, 136, 56))
    save_sprite('volcanion_needle', nd, prefix=PFX)
    # klinknagel (16x16), vliegt weg
    rv = Image.new('RGB', (16, 16), KEY)
    d = ImageDraw.Draw(rv)
    d.ellipse((3, 3, 12, 12), fill=VOL_RIVET[1], outline=VOL_RIVET[2])
    d.ellipse((4, 4, 9, 9), fill=VOL_RIVET[0])
    d.rectangle((7, 12, 8, 15), fill=VOL_RIVET[1])
    save_sprite('volcanion_rivet', rv, prefix=PFX)
    save_preview('volcanion', [a, b])


# ================================================================== Hoopa
HOOPA_BG = [(16, 8, 32), (40, 24, 64), (120, 96, 168), (216, 208, 240)]
HOOPA_SWIRL = [(248, 200, 248), (216, 128, 232), (176, 80, 208), (128, 48, 176), (96, 32, 152), (56, 24, 112),
               (80, 40, 136), (160, 72, 200)]
HOOPA_GOLD = [(248, 232, 120), (232, 184, 48), (176, 120, 24), (96, 56, 16)]
RING_C, RING_R, RING_W = (120, 68), 46, 7


def hoopa():
    im = Image.new('RGB', (240, 160), HOOPA_BG[0])
    px = im.load()
    rnd = random.Random(11)
    # nachtlucht met wat sterren en een woestijnhorizon (Mirage Bazaar)
    for _ in range(60):
        x, y = rnd.randrange(240), rnd.randrange(120)
        px[x, y] = HOOPA_BG[rnd.choice((2, 2, 3))]
    for x in range(240):
        h = int(138 + 6 * math.sin(x / 31) + 3 * math.sin(x / 11))
        for y in range(h, 160):
            px[x, y] = HOOPA_BG[1]
    cx, cy = RING_C
    for y in range(160):
        for x in range(240):
            dx, dy = x - cx + 0.5, y - cy + 0.5
            r = math.hypot(dx, dy)
            if r < RING_R:
                th = math.atan2(dy, dx)
                ph = (th / (2 * math.pi) * 2 - math.log(max(r, 1)) * 1.4) % 1.0
                px[x, y] = HOOPA_SWIRL[int(ph * 8) % 8] if r > 4 else HOOPA_SWIRL[0]
            elif r < RING_R + RING_W:
                # gouden ring met licht van linksboven
                k = r - RING_R
                lit = (-dx - dy) / r
                if k < 1 or k >= RING_W - 1:
                    c = HOOPA_GOLD[3]
                elif lit > 0.4 and k < 4:
                    c = HOOPA_GOLD[0]
                elif lit < -0.4:
                    c = HOOPA_GOLD[2]
                else:
                    c = HOOPA_GOLD[1]
                px[x, y] = c
    enc = Encoder('hoopa', [HOOPA_BG, HOOPA_SWIRL + HOOPA_GOLD + [HOOPA_BG[0], HOOPA_BG[2], HOOPA_BG[3]], [(248, 248, 248)]], prefix=PFX)
    enc.add(im, None, 'portaal')
    # binnen in de ring: de wervel over het hele scherm (180 graden symmetrisch)
    full = Image.new('RGB', (240, 160))
    fp = full.load()
    for y in range(160):
        for x in range(240):
            dx, dy = x - 119.5, y - 79.5
            r = math.hypot(dx, dy)
            th = math.atan2(dy, dx)
            ph = (th / (2 * math.pi) * 2 - math.log(max(r, 1)) * 1.4) % 1.0
            fp[x, y] = HOOPA_SWIRL[int(ph * 8) % 8] if r > 4 else HOOPA_SWIRL[0]
    enc.add(full, 1, 'binnen')
    enc.save()
    # Hoopa's hand uit de gevechtsanimatie (16x16), Scale2x x2 = 64x64
    h = Image.open(os.path.join(ROOT, 'graphics/battle_anims/sprites/hoopa_hand.png'))
    pal = h.getpalette()[:48]
    a = scale2x(scale2x(np.array(h)))
    rgb = np.array([tuple(pal[i * 3:i * 3 + 3]) for i in range(16)], np.uint8)[a]
    rgb[a == 0] = KEY
    save_sprite('hoopa_hand', Image.fromarray(rgb), prefix=PFX)
    save_preview('hoopa', [im, full])


# ================================================================== Forces of Nature (weerbericht)
FN_SEA = [(80, 136, 208), (104, 160, 224)]
FN_LAND = [(72, 152, 72), (112, 184, 80), (160, 208, 104), (152, 128, 72), (200, 176, 112)]
FN_CRACK = [(32, 24, 16), (96, 64, 40)]
FN_BURN = [(40, 32, 40), (248, 232, 128)]
FN_LBL = [(248, 248, 248), (32, 48, 96)]
FN_TV = [(16, 24, 56), (32, 48, 104), (248, 248, 248), (200, 208, 224), (216, 40, 40), (248, 200, 56),
         (24, 24, 32), (120, 136, 176)]   # banier, banier licht, wit, grijs, LIVE rood, geel, onderbalk, onderbalk rand
FN_CARD = [(24, 24, 40), (248, 248, 248), (248, 200, 56), (88, 216, 120), (160, 168, 200), (216, 72, 56)]
FN_TEMPS = [(48, 46, '21'), (124, 30, '19'), (188, 60, '23'), (92, 86, '20')]
FN_CHYRON = {
    'base': 'Mild breeze from the west. Lovely.',
    't': 'UPDATE: the front has a face.',
    'th': 'UPDATE: 100% chance of Thundurus.',
    'l': 'UPDATE: the ground is weather now.',
}


def region_map():
    """De echte Hoenn-kaart uit de PokéNav (graphics/pokenav/region_map), omgezet naar weerkaartkleuren."""
    im = Image.open(os.path.join(ROOT, 'graphics/pokenav/region_map/map.png'))
    P = im.getpalette()
    tiles = [np.array(im)[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] for ty in range(im.height // 8) for tx in range(16)]
    m = open(os.path.join(ROOT, 'graphics/pokenav/region_map/map.bin'), 'rb').read()
    out = np.zeros((256, 256, 3), np.uint8)
    for i, v in enumerate(m):
        tx, ty = i % 64, i // 64
        if tx >= 32 or ty >= 32:
            continue
        t = tiles[v] if v < len(tiles) else tiles[0]
        out[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] = np.array([P[c * 3:c * 3 + 3] for c in t.reshape(64)]).reshape(8, 8, 3)
    return out


def classify(c):
    r, g, b = [int(v) for v in c]
    if b > r + 20 and b > g - 10:  # zee en zeeroutes
        return FN_SEA[0] if (r + g + b) < 480 else FN_SEA[1]
    if r > 180 and g > 120 and b < 120 and r > g:  # wegen (oranje) -> licht land
        return FN_LAND[2]
    if g > r + 10:
        lum = r + g + b
        return FN_LAND[0] if lum < 300 else FN_LAND[1] if lum < 420 else FN_LAND[2]
    if r > 150 and g < 120:  # steden (rood) -> land
        return FN_LAND[1]
    lum = r + g + b
    return FN_LAND[3] if lum < 420 else FN_LAND[4]


def forces_tv(chyron, extra=None):
    rm = region_map()
    im = Image.new('RGB', (240, 160), FN_SEA[0])
    px = im.load()
    # kaartuitsnede: x 0..240, y 8..128 van de kaart naar y 16..136 van het scherm
    cache = {}
    for y in range(16, 136):
        for x in range(240):
            c = tuple(rm[y - 8, x])
            if c not in cache:
                cache[c] = classify(c)
            px[x, y] = cache[c]
    if extra:
        extra(im)
    d = ImageDraw.Draw(im)
    # temperatuurlabels
    for x, y, s in FN_TEMPS:
        w = text_width(s, 'small') + 4
        d.rectangle((x, y + 16, x + w, y + 16 + 10), fill=FN_LBL[1])
        text(im, x + 2, y + 14, s, FN_LBL[0], None, 'small')
    # banier boven
    d.rectangle((0, 0, 239, 15), fill=FN_TV[0])
    d.line((0, 15, 239, 15), fill=FN_TV[1])
    text(im, 4, -1, 'HOENN WEATHER', FN_TV[2], FN_TV[7], 'normal')
    text(im, 138, -1, '7-DAY FORECAST', FN_TV[3], None, 'small')
    d.rectangle((210, 3, 235, 12), fill=FN_TV[4])
    text(im, 213, -1, 'LIVE', FN_TV[2], None, 'small')
    # onderbalk
    d.rectangle((0, 136, 239, 159), fill=FN_TV[6])
    d.line((0, 136, 239, 136), fill=FN_TV[7])
    d.rectangle((0, 137, 5, 159), fill=FN_TV[5])
    text(im, 10, 140, chyron, FN_TV[2], None, 'normal' if text_width(chyron) < 224 else 'narrow')
    return im


def forces_cracks(im):
    d = ImageDraw.Draw(im)
    rnd = random.Random(5)
    # barsten vanuit het midden (Route 111 / Mt. Chimney) naar buiten, vertakt
    def crack(x, y, ang, n, w):
        for _ in range(n):
            nx, ny = x + 6 * math.cos(ang), y + 6 * math.sin(ang)
            d.line((x, y, nx, ny), fill=FN_CRACK[0], width=w)
            if w > 1:
                d.line((x + 1, y + 1, nx + 1, ny + 1), fill=FN_CRACK[1])
            x, y = nx, ny
            ang += rnd.uniform(-0.5, 0.5)
            if rnd.random() < 0.25 and n > 4:
                crack(x, y, ang + rnd.choice((-0.8, 0.8)), n // 2, max(1, w - 1))
    for k in range(5):
        crack(112, 70, k * 2 * math.pi / 5 + 0.4, 14, 3)


def forces_burns(im):
    d = ImageDraw.Draw(im)
    for x, y in FN_STRIKES:
        d.ellipse((x - 9, y - 6, x + 9, y + 6), fill=FN_BURN[0])
        d.ellipse((x - 3, y - 2, x + 3, y + 2), fill=FN_BURN[1])


FN_STRIKES = [(64, 70), (160, 54), (112, 104)]   # inslagen (schermpixels), ook in C (FN_STRIKE_*)


def forces_card(name, lines):
    im = Image.new('RGB', (240, 160), (0, 0, 0))
    d = ImageDraw.Draw(im)
    # kaart van 14 x 8 tiles op (0, 0)
    d.rectangle((0, 0, 111, 63), fill=FN_CARD[0], outline=FN_CARD[4])
    d.rectangle((2, 2, 109, 15), fill=FN_CARD[5])
    text(im, 5, -1, 'USAGE STATS', FN_CARD[1], None, 'small')
    text(im, 5, 14, name, FN_CARD[2], None, 'normal')
    y = 28
    for k, v, c in lines:
        x = text(im, 5, y, k, FN_CARD[4], None, 'small')
        text(im, x + 2, y, v, FN_CARD[c], None, 'small')
        y += 10
    return im


def forces():
    base = forces_tv(FN_CHYRON['base'])
    tvs = [forces_tv(FN_CHYRON[k]) for k in ('t', 'th', 'l')]
    cracked = forces_tv(FN_CHYRON['l'], forces_cracks)
    burnt = forces_tv(FN_CHYRON['th'], forces_burns)
    card_t = forces_card('LANDORUS-T', [('OU usage:', 'very yes', 3), ('Intimidate:', 'yes', 3),
                                        ('Counterplay:', 'lol', 5)])
    card_i = forces_card('LANDORUS', [('Usage:', 'Ubers (sorry)', 3), ('Sheer Force:', 'yes', 3),
                                      ('Counterplay:', 'pray', 5)])
    p13 = FN_SEA + FN_LAND + FN_CRACK + FN_BURN + FN_LBL
    enc = Encoder('forces', [p13, FN_TV, FN_CARD], prefix=PFX)
    for im, lbl in [(base, 'tv'), (tvs[0], 'tv_t'), (tvs[1], 'tv_th'), (tvs[2], 'tv_l'), (cracked, 'scheur'),
                    (burnt, 'brand'), (card_t, 'kaart_t'), (card_i, 'kaart_i')]:
        enc.add(im, None, lbl)
    enc.save()
    save_preview('forces', [base, tvs[0], tvs[1], cracked, burnt, card_t, card_i])


if __name__ == '__main__':
    which = [a for a in sys.argv[2:]] or ['lugia', 'hooh', 'volcanion', 'hoopa', 'forces']
    for w in which:
        globals()[w]()
