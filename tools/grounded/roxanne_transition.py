#!/usr/bin/env python3
"""Project Grounded: gymleider-intro Roxanne ("Yo! Put your lighters up!"). De gym gaat op zwart, een zee van aanstekers
gaat aan in de zaal, een spotlight klikt aan op Roxanne, de tekst verschijnt op de maat, twee rotsblokken zakken als
gitaarversterkers omlaag en de powerchord geeft een flits.

BG0 (paletten 13-15): de zaal (podium van de Rustboro-gymtiles, publiek met aanstekers), het publiek in twee standen
(wiegen), de tekst in twee stappen en een disclaimer. De lichtkegel is geen art maar hardware: venster 0 per beeldlijn
(HBlank-DMA op WIN0H) met 'lichter maken' (BLDY) erin. Sprites: Roxanne (haar eigen trainerfoto) en de versterker (de
Rock Slide-steen uit de gevechtsanimaties, als kast met luidspreker).
Paletindexen die de C-code animeert (src/battle_transition.c, "Roxanne"): BG 13 index 4-9 = vlammen (groep 1-3,
kern + buitenkant).
Gebruik: python3 tools/grounded/roxanne_transition.py [voorbeeld.png]"""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
from gym_intro_lib import Encoder, metatiles, text, text_width, save_sprite, preview_strip, OUT, KEY, gba

PREVIEW = sys.argv[1] if len(sys.argv) > 1 else None
STAGE_Y = 96            # bovenkant podium (rij 12)
CROWD_Y = 112           # bovenkant van de publieksrijen (rij 14)

# ------------------------------------------------------------------ podium: de verhoogde vloer van de Rustboro-gym
stage_src = metatiles('building', 'rustboro_gym', [[0x219] * 15, [0x229] * 15])   # 240 x 32
q = stage_src.quantize(6, method=Image.Quantize.MEDIANCUT)
rock_raw = [tuple(q.getpalette()[i * 3:i * 3 + 3]) for i in range(6)]
rock = [gba(c) for c in rock_raw]
ROCK_DIM = [gba(tuple(int(v * 0.5) + 2 for v in c)) for c in rock]
a = np.array(q.convert('RGB'))
b = a.copy()
for i, c in enumerate(rock_raw):
    b[(a == c).all(2)] = ROCK_DIM[i]
stage = Image.fromarray(b)

# ------------------------------------------------------------------ kleuren
BACK, FRONT, LIGHTER = (16, 8, 24), (32, 24, 48), (96, 96, 112)
FLAME = [((248, 248, 168), (248, 144, 40)), ((248, 232, 136), (232, 112, 32)), ((248, 248, 200), (248, 168, 64))]
WHITE, YELLOW, RED, DARK = (248, 248, 248), (248, 216, 64), (200, 32, 24), (40, 8, 8)
GRAY = (136, 128, 144)
TRUSS, TRUSS_D, LAMP, LAMP_GLASS = (88, 88, 96), (48, 48, 56), (32, 32, 40), (248, 248, 208)
P13 = [BACK, FRONT, LIGHTER] + [c for f in FLAME for c in f] + ROCK_DIM
P14 = [WHITE, YELLOW, RED, DARK, TRUSS, TRUSS_D, LAMP, LAMP_GLASS]
P15 = [GRAY, BACK, FRONT, LIGHTER]

# ------------------------------------------------------------------ publiek: twee rijen silhouetten met aanstekers
rr = random.Random(7)
people = []
for y0, col, n, hr in ((CROWD_Y + 12, BACK, 13, 6), (CROWD_Y + 30, FRONT, 9, 9)):
    for i in range(n):
        x = int((i + 0.5) * 240 / n + rr.randint(-5, 5))
        people.append(dict(x=x, y=y0 + rr.randint(-2, 2), col=col, r=hr, arm=rr.random() < 0.8,
                           side=rr.choice((-1, 1)), group=rr.randint(0, 2), ph=rr.randint(0, 1)))


def crowd(sway):
    im = Image.new('RGB', (240, 48), KEY)
    d = ImageDraw.Draw(im)
    for p in people:
        x, y, r = p['x'], p['y'] - CROWD_Y, p['r']
        d.ellipse((x - r * 2, y + r, x + r * 2, y + r * 5), fill=p['col'])
        d.ellipse((x - r, y - r, x + r, y + r), fill=p['col'])
    # armen met aanstekers erboven (hoger dan de bovenkant van de publieksrijen: die tekenen we in het podium)
    arms = Image.new('RGB', (240, 80), KEY)
    da = ImageDraw.Draw(arms)
    for p in people:
        if not p['arm']:
            continue
        x, y, r = p['x'], p['y'] - CROWD_Y + 32, p['r']
        sx = x + p['side'] * r * 1.4
        off = (2 if (sway + p['ph']) % 2 else -2) * p['side']
        hx, hy = sx + p['side'] * 3 + off, y - r * 3 - 2
        da.line((sx, y + r * 1.6, hx, hy + 3), fill=p['col'], width=3)
        da.rectangle((hx - 2, hy - 2, hx + 1, hy + 3), fill=LIGHTER)
        core, outer = FLAME[p['group']]
        da.ellipse((hx - 3, hy - 11, hx + 3, hy - 2), fill=outer)
        da.ellipse((hx - 1, hy - 8, hx + 1, hy - 3), fill=core)
    return im, arms


def paste_key(dst, src, pos):
    m = Image.fromarray(((np.array(src) != KEY).any(2) * 255).astype(np.uint8))
    dst.paste(src, pos, m)


def truss(im):
    d = ImageDraw.Draw(im)
    d.rectangle((0, 1, 239, 2), fill=TRUSS)
    d.rectangle((0, 9, 239, 10), fill=TRUSS)
    for x in range(0, 240, 8):
        d.line((x, 3, x + 7, 8), fill=TRUSS_D)
        d.line((x + 7, 3, x, 8), fill=TRUSS_D)
    # lampen aan de truss (de middelste is de spot)
    for x in (24, 72, 120, 168, 216):
        d.rectangle((x - 5, 11, x + 4, 17), fill=LAMP)
        d.rectangle((x - 3, 17, x + 2, 18), fill=LAMP_GLASS if x == 120 else TRUSS_D)


def compose(sway, words=0, disclaimer=False):
    im = Image.new('RGB', (240, 160), (0, 0, 0))
    truss(im)
    im.paste(stage, (0, STAGE_Y))
    cim, arms = crowd(sway)
    paste_key(im, cim, (0, CROWD_Y))
    paste_key(im, arms, (0, CROWD_Y - 32))
    for i, s in enumerate(['PUT YOUR', 'LIGHTERS UP!'][:words]):
        w = text_width(s, scale=2, spacing=1)
        tmp = Image.new('RGB', (240, 32), KEY)
        text(tmp, 120 - w // 2, 0, s, YELLOW, RED, scale=2, spacing=1)
        ta = np.array(tmp)
        m = (ta != KEY).any(2)
        m2 = m.copy()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            m2 |= np.roll(np.roll(m, dy, 0), dx, 1)
        ia = np.array(im)
        y = 24 + i * 28
        reg = ia[y:y + 32]
        reg[m2 & ~m] = DARK
        reg[m] = ta[m]
        im = Image.fromarray(ia)
    if disclaimer:
        s = 'Lighters kindly provided by TEAM MAGMA.'
        ia = np.array(im)
        ia[149:160] = 0
        im = Image.fromarray(ia)
        text(im, 238 - text_width(s, font='narrow'), 146, s, GRAY, None, font='narrow')
    return im


enc = Encoder('roxanne', [P13, P14, P15])
ORDER = [('a', (0,)), ('b', (1,)), ('w1', (0, 1)), ('w2a', (0, 2)), ('w2b', (1, 2)),
         ('da', (0, 0, True)), ('db', (1, 0, True))]
for k, args in ORDER:
    enc.add(compose(*args), label=k)
enc.save()

# ------------------------------------------------------------------ versterker: de Rock Slide-steen als kast
idx = np.array(Image.open(os.path.join(OUT, '..', 'battle_anims/sprites/big_rock.png')))
ramp = [None, (16, 12, 12), (40, 32, 32), (56, 48, 44), (72, 60, 52), (88, 72, 60), (104, 88, 72), (120, 100, 84),
        (136, 112, 92), (152, 128, 104), (168, 144, 116), (184, 156, 124), (200, 172, 136), (208, 184, 148),
        (216, 196, 160), (232, 216, 184)]
amp = Image.new('RGB', (64, 64), KEY)
ap = amp.load()
box = Image.new('L', (64, 64), 0)
ImageDraw.Draw(box).rounded_rectangle((4, 16, 59, 62), radius=7, fill=255)
bp = box.load()
for y in range(64):
    for x in range(64):
        if bp[x, y]:
            v = idx[min(63, max(0, (y - 16) * 64 // 47 + 8)), x]
            ap[x, y] = ramp[max(3, v)] if v else ramp[4]
d = ImageDraw.Draw(amp)
d.rounded_rectangle((4, 16, 59, 62), radius=7, outline=ramp[1])
d.rectangle((9, 20, 54, 26), fill=ramp[2])
for k in range(5):
    d.ellipse((12 + k * 8, 21, 16 + k * 8, 25), fill=ramp[14])
    ap[14 + k * 8, 22] = ramp[1]
d.ellipse((17, 30, 46, 59), fill=ramp[1])
d.ellipse((20, 33, 43, 56), fill=ramp[3])
d.ellipse((25, 38, 38, 51), fill=ramp[2])
d.ellipse((29, 42, 34, 47), fill=ramp[5])
for cx in (14, 49):
    for y in range(0, 16, 4):
        d.rectangle((cx - 1, y, cx + 1, y + 2), outline=ramp[9])
save_sprite('roxanne_amp', amp)

if PREVIEW:
    shots = [enc.render(m) for m in enc.maps]
    src = Image.open(os.path.join(OUT, '..', 'trainers/front_pics/leader_roxanne.png'))
    ra = np.array(src.convert('RGBA'))
    ra[np.array(src) == 0] = 0
    rox = Image.fromarray(ra)
    ampa = np.array(amp.convert('RGBA'))
    ampa[(np.array(amp) == KEY).all(2)] = 0
    ampi = Image.fromarray(ampa)
    comp = shots[5].copy()
    # lichtkegel zoals de hardware hem maakt (lichter maken, BLDY 6)
    ca = np.array(comp).astype(int)
    for y in range(120):
        if y < 18:
            continue
        half = 4 + (y - 18) * 40 // 78 if y < STAGE_Y else 44
        x0, x1 = max(0, 120 - half), min(240, 120 + half)
        ca[y, x0:x1] += (255 - ca[y, x0:x1]) * 6 // 16
    comp = Image.fromarray(ca.astype(np.uint8))
    comp.paste(rox, (88, 42), rox)
    comp.paste(ampi, (20, 50), ampi)
    fl = ampi.transpose(Image.FLIP_LEFT_RIGHT)
    comp.paste(fl, (156, 50), fl)
    shots.append(comp)
    preview_strip(shots, PREVIEW)
