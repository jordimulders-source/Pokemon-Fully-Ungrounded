#!/usr/bin/env python3
"""Project Grounded: gymleider-intro Flannery. Een camping in de schemering: een rood tentje (met de Poké Ball van de
Red Tent), een kampvuur, een bordje "NO WIFI. JUST ANALOG HEAT." en op de achtergrond Mt. Chimney. De grond rommelt,
de vulkaan ontploft (pluim, lavabommen, de lucht kleurt rood), Flannery: "Totally planned!", en een stuk vulkanisch
gesteente vliegt recht op de camera af: de lens barst.
BG0 (paletten 13-15): de camping, dezelfde camping met de barst in de lens, en met de tekstballon.
Sprites: Flannery (trainerfoto), het kampvuur en de pluim (Fire / Fire Plume uit de gevechtsanimaties), lavabommen
(Warm Rock) en de steen die de camera raakt (de Rock Slide-steen, met een eigen basaltpalet).
Paletindexen die de C-code animeert: BG 13 index 1-5 = lucht (naar rood bij de uitbarsting), 8-9 = lavagloed.
Gebruik: python3 tools/grounded/flannery_transition.py [voorbeeld.png]"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
from gym_intro_lib import Encoder, text, text_width, save_sprite, preview_strip, OUT, KEY, gba

PREVIEW = sys.argv[1] if len(sys.argv) > 1 else None

SKY = [(56, 40, 96), (104, 56, 120), (168, 80, 112), (224, 120, 88), (248, 176, 96)]   # boven -> horizon
V_DARK, V_MID = (32, 24, 40), (56, 40, 56)
LAVA = [(248, 112, 24), (248, 216, 64)]
SMOKE = [(88, 72, 96), (120, 104, 120)]
P13 = SKY + [V_DARK, V_MID] + LAVA + SMOKE                      # 11
TENT = [(200, 40, 48), (136, 24, 40), (248, 248, 248), (24, 16, 24)]
GRASS = [(24, 48, 40), (40, 72, 48), (56, 96, 56)]
WOOD = [(120, 72, 40), (80, 48, 32)]
STONE = (72, 64, 72)
P14 = SKY[2:] + TENT + GRASS + WOOD + [STONE, (232, 200, 136)]        # 3 + 4 + 3 + 2 + 2 = 14
GLASS = [(248, 248, 248), (184, 192, 208)]
P15 = GLASS + [(24, 16, 24)] + SKY + [V_DARK, GRASS[0], GRASS[1], TENT[0], LAVA[0], WOOD[0]]
HORIZON = 104


def dither_band(y, edges):
    """kleurindex van de lucht op hoogte y met een geditherde overgang"""
    for i, e in enumerate(edges):
        if y < e:
            return i
    return len(edges)


def camp():
    im = Image.new('RGB', (240, 160), (0, 0, 0))
    px = im.load()
    edges = [22, 44, 66, 86]
    for y in range(HORIZON):
        for x in range(240):
            b = dither_band(y, edges)
            # 4 px boven elke grens: om en om de volgende kleur
            if b < 4 and edges[b] - y <= 4 and (x + y) % 2 == 0:
                b += 1
            px[x, y] = SKY[b]
    d = ImageDraw.Draw(im)
    # Mt. Chimney: silhouet met krater (rechts van het midden), lavagloed op de rand, rookpluim
    d.polygon([(96, HORIZON), (150, 40), (166, 36), (186, 36), (200, 40), (254, HORIZON)], fill=V_DARK)
    d.polygon([(150, 40), (166, 36), (186, 36), (200, 40), (190, 52), (160, 52)], fill=V_MID)
    d.line([(158, 38), (166, 35), (186, 35), (194, 38)], fill=LAVA[0], width=2)
    d.line([(170, 35), (182, 35)], fill=LAVA[1])
    for i, (sx, sy, r) in enumerate(((176, 26, 7), (184, 16, 9), (196, 8, 10), (210, 4, 9))):
        d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=SMOKE[i % 2])
    # grond
    d.rectangle((0, HORIZON, 239, 159), fill=GRASS[0])
    rr = random.Random(4)
    for _ in range(140):
        x, y = rr.randint(0, 239), rr.randint(HORIZON + 2, 159)
        d.line((x, y, x + rr.choice((-1, 1)), y - 2), fill=GRASS[1 + (y > 132)])
    d.line((0, HORIZON, 239, HORIZON), fill=GRASS[1])
    # tentje (zijaanzicht, A-vorm) met de Poké Ball van de Red Tent op de flap
    tx, ty = 62, 142
    d.polygon([(tx, ty), (tx + 44, ty - 70), (tx + 92, ty)], fill=TENT[0])
    d.polygon([(tx + 44, ty - 70), (tx + 92, ty), (tx + 70, ty)], fill=TENT[1])
    d.polygon([(tx + 30, ty), (tx + 44, ty - 38), (tx + 58, ty)], fill=TENT[3])
    d.line([(tx, ty), (tx + 44, ty - 70), (tx + 92, ty)], fill=TENT[3])
    cx, cy = tx + 34, ty - 50
    d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=TENT[2], outline=TENT[3])
    d.chord((cx - 7, cy - 7, cx + 7, cy + 7), 180, 360, fill=TENT[0], outline=TENT[3])
    d.line((cx - 7, cy, cx + 7, cy), fill=TENT[3])
    d.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=TENT[2], outline=TENT[3])
    d.line((tx - 6, ty + 1, tx + 100, ty + 1), fill=GRASS[2])
    # bordje
    sx, sy = 4, 110
    d.rectangle((sx + 24, sy + 33, sx + 28, sy + 46), fill=WOOD[1])
    d.rectangle((sx, sy, sx + 54, sy + 35), fill=WOOD[0], outline=WOOD[1])
    for i, line in enumerate(('NO WIFI.', 'JUST ANALOG', 'HEAT.')):
        text(im, sx + 28 - text_width(line, font='narrow') // 2, sy - 2 + i * 11, line, P14[-1], None, font='narrow')
    # houtblokken van het kampvuur
    fx, fy = 168, 142
    d.line((fx - 14, fy + 6, fx + 14, fy - 2), fill=WOOD[1], width=4)
    d.line((fx - 14, fy - 2, fx + 14, fy + 6), fill=WOOD[0], width=4)
    for k in range(7):
        a = k * math.pi * 2 / 7
        d.ellipse((fx + 22 * math.cos(a) - 3, fy + 2 + 6 * math.sin(a) - 2, fx + 22 * math.cos(a) + 3, fy + 2 + 6 * math.sin(a) + 2), fill=STONE)
    # het bordje en de stenen kunnen dezelfde rookkleur gebruiken: stenen in P14? -> donkerhout
    return im


def crack(base):
    """de lens barst: breuklijnen vanuit het inslagpunt (120, 80) met een lichte rand, op het beeld"""
    im = base.copy()
    d = ImageDraw.Draw(im)
    rr = random.Random(21)
    cx, cy = 120, 80
    for k in range(9):
        ang = k * 2 * math.pi / 9 + rr.uniform(-0.25, 0.25)
        x, y = cx, cy
        L = rr.randint(70, 150)
        pts = [(x, y)]
        for s in range(8):
            ang += rr.uniform(-0.35, 0.35)
            x += math.cos(ang) * L / 8
            y += math.sin(ang) * L / 8
            pts.append((x, y))
        d.line(pts, fill=GLASS[1], width=3)
        d.line(pts, fill=GLASS[0], width=1)
    # kringen (spinnenweb)
    for r in (16, 34):
        pts = []
        for k in range(19):
            a = k * 2 * math.pi / 18
            rj = r + rr.randint(-3, 3)
            pts.append((cx + rj * math.cos(a), cy + rj * math.sin(a) * 0.8))
        d.line(pts, fill=GLASS[0], width=1)
    d.ellipse((cx - 6, cy - 5, cx + 6, cy + 5), fill=GLASS[1])
    return im


def bubble():
    s = 'Totally planned!'
    w = text_width(s) + 12
    im = Image.new('RGB', (((w + 7) // 8) * 8, 24), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, 19), radius=6, fill=GLASS[0], outline=P15[2])
    d.polygon([(w - 22, 18), (w - 12, 23), (w - 14, 18)], fill=GLASS[0], outline=P15[2])
    d.line((w - 21, 18, w - 15, 18), fill=GLASS[0])
    text(im, 6, 1, s, P15[2], GLASS[1])
    return im


enc = Encoder('flannery', [P13, P14, P15])
base = camp()
enc.add(base, label='camp')               # 0
enc.add(crack(base), label='crack')       # 1
b = bubble()
withb = base.copy()
ba = np.array(b)
m = Image.fromarray(((ba != 0).any(2) * 255).astype(np.uint8))
withb.paste(b, (104, 56), m)                # kolom 13, rij 7 (de C-code kopieert dat blok)
enc.add(withb, label='bubble')            # 2
enc.save()
print('  tekstballon: %d x 3 vakken' % (b.width // 8))

# ------------------------------------------------------------------ de steen: Rock Slide-steen met basaltpalet (gloeiend)
src = Image.open(os.path.join(OUT, '..', 'battle_anims/sprites/big_rock.png'))
basalt = [(0, 0, 0), (16, 8, 8), (32, 16, 16), (48, 24, 24), (64, 32, 32), (80, 40, 40), (96, 48, 40),
          (112, 56, 48), (128, 64, 48), (152, 72, 40), (184, 80, 32), (216, 96, 24), (240, 120, 24),
          (248, 160, 40), (248, 200, 72), (248, 232, 120)]
with open(os.path.join(OUT, 'gym_flannery_rock.pal'), 'w', newline='\r\n') as fp:
    fp.write('JASC-PAL\n0100\n16\n')
    for c in basalt:
        fp.write('%d %d %d\n' % gba(c))

if PREVIEW:
    shots = [enc.render(m) for m in enc.maps]
    comp = shots[0].copy()
    fl = Image.open(os.path.join(OUT, '..', 'trainers/front_pics/leader_flannery.png'))
    fa = np.array(fl.convert('RGBA'))
    fa[np.array(fl) == 0] = 0
    fli = Image.fromarray(fa)
    comp.paste(fli, (176, 78), fli)
    comp.paste(enc.render(enc.maps[2]).crop((104, 56, 104 + b.width, 80)), (104, 56))
    shots.append(comp)
    preview_strip(shots, PREVIEW, cols=2)
