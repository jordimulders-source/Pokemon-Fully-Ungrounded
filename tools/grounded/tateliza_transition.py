#!/usr/bin/env python3
"""Project Grounded: gymleider-intro Tate & Liza ("Twin Flame energy", tarot, "your aura screaming in lowercase").
Jordi: tarotkaarten, ouijaborden en allerlei vage spirituele shit, uitlopend op een psychic overload.
Een ouijabord bij paarse kaarsvlammen: de planchette spelt R-I-P en schiet naar GOOD BYE. Dan drie tarotkaarten die
een voor een omdraaien (THE TWINS, THE MOON, DEATH (yours)): "TATE: The cards have spoken..." / "LIZA: ...and they hate
you." Dan de overload: psychische ringen razen naar buiten (paletcyclus), ogen gaan open, lepels buigen en draaien om de
tweeling, "TWIN FLAME ENERGY: PEAK PERFORMANCE", en dan alleen nog "aaaaaaaaaah" (your aura, screaming in lowercase).

BG0 (paletten 13-15): het ouijabord (met de onthulde letters), de tarotkaarten in vijf standen (achterkant, half,
zijkant, half voorkant, voorkant), het ringenveld (palet 14, 8 indexen die de C-code laat rondlopen), ondertitels in
de zwarte balken (palet 15).
Sprites: Tate & Liza (trainerfoto), de planchette (eigen), kaarsvlammen (Purple Flame), ogen (Opening Eye) en lepels
(Bent Spoon) uit de gevechtsanimaties.
Gebruik: python3 tools/grounded/tateliza_transition.py [voorbeeld.png]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
from gym_intro_lib import outlined_text as outlined, Encoder, text, text_width, save_sprite, preview_strip, OUT, KEY, gba

PREVIEW = sys.argv[1] if len(sys.argv) > 1 else None

WOOD, WOOD_D, WOOD_L, INK = (152, 104, 56), (104, 64, 32), (192, 144, 88), (48, 24, 16)
CLOTH, CARD_B, CARD_BL, GOLD, CREAM = (40, 16, 56), (88, 32, 120), (136, 72, 168), (232, 184, 72), (232, 216, 176)
CANDLE, CANDLE_D, BLOOD = (224, 216, 200), (168, 152, 136), (176, 32, 48)
P13 = [WOOD, WOOD_D, WOOD_L, INK, CLOTH, CARD_B, CARD_BL, GOLD, CREAM, CANDLE, CANDLE_D, BLOOD]
RINGS = [(248, 120, 200), (216, 80, 200), (168, 64, 200), (112, 56, 192), (72, 48, 160), (112, 56, 192), (168, 64, 200),
         (216, 80, 200)]
# twee gelijke kleuren mogen niet: de encoder kiest altijd de eerste. Daarom licht verschillend
RINGS = [(r, g, b + (8 if i >= 5 else 0)) for i, (r, g, b) in enumerate(RINGS)]
P14 = RINGS + [(24, 8, 32)]
WHITE15, GRAY15, YELLOW15, PINK15, DARK15, DISC = (240, 240, 240), (160, 160, 168), (248, 224, 72), (248, 112, 200), \
    (48, 8, 40), (136, 128, 144)
P15 = [WHITE15, GRAY15, YELLOW15, PINK15, DARK15, DISC]
for p in (P13, P14, P15):
    assert len(set(gba(c) for c in p)) == len(p), p


def ctext(im, cx, y, s, fg, shadow=None, font='normal', scale=1, spacing=0):
    return text(im, cx - text_width(s, font, scale, spacing) // 2, y, s, fg, shadow, font, scale, spacing)




def sun(d, cx, cy, r, col):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col)
    for k in range(8):
        a = k * math.pi / 4
        d.line((cx + math.cos(a) * (r + 2), cy + math.sin(a) * (r + 2), cx + math.cos(a) * (r + 4), cy + math.sin(a) * (r + 4)), fill=col)


def moon(d, cx, cy, r, col, bg):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
    d.ellipse((cx - r + r // 2, cy - r - 1, cx + r + r // 2, cy + r - 1), fill=bg)


# ------------------------------------------------------------------ het ouijabord
LETTERS = {}
SPELL_COLS = [21, 23, 25]       # vakken voor R, I, P in "THE SPIRITS SAY:"


def ouija(revealed=0):
    im = Image.new('RGB', (240, 160), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 4, 231, 155), radius=14, fill=WOOD_D)
    d.rounded_rectangle((11, 7, 228, 152), radius=12, fill=WOOD)
    for y in range(14, 150, 9):
        d.line((20, y, 220, y + 2), fill=WOOD_L)
    text(im, 22, 8, 'YES', INK, None)
    text(im, 218 - text_width('NO'), 8, 'NO', INK, None)
    sun(d, 64, 18, 6, INK)
    moon(d, 176, 18, 7, INK, WOOD)
    # letters in twee bogen
    for row, (letters, xa, xb, base, ry, rx) in enumerate((('ABCDEFGHIJKLM', 28, 212, 82, 50, 100), ('NOPQRSTUVWXYZ', 46, 194, 86, 28, 80))):
        for i, ch in enumerate(letters):
            cx = xa + (xb - xa) * i / (len(letters) - 1)
            cy = base - ry * math.sqrt(max(0.0, 1 - ((cx - 120) / rx) ** 2))
            w = text_width(ch)
            text(im, int(cx - w / 2), int(cy - 9), ch, INK, None)
            LETTERS[ch] = (int(cx), int(cy - 2))
    s = '1234567890'
    ctext(im, 120, 88, s, INK, None, spacing=2)
    ctext(im, 120, 105, 'GOOD BYE', INK, None, spacing=1)
    LETTERS['BYE'] = (120, 112)
    text(im, 44, 126, 'THE SPIRITS SAY:', INK, None, font='narrow')
    for k, ch in enumerate('RIP'[:revealed]):
        text(im, SPELL_COLS[k] * 8 + (8 - text_width(ch)) // 2, 126, ch, BLOOD, None)
    # kaarsen (de vlammen zijn sprites)
    for cx in (24, 215):
        d.rectangle((cx - 4, 128, cx + 3, 147), fill=CANDLE)
        d.line((cx + 2, 128, cx + 2, 147), fill=CANDLE_D)
        d.line((cx, 126, cx, 127), fill=INK)
    return im


# ------------------------------------------------------------------ tarot
CARD_COLS = [4, 12, 20]         # 7 vakken breed
CARD_Y0, CARD_Y1 = 32, 127      # rij 4..15


def cloth():
    im = Image.new('RGB', (240, 160), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 24, 239, 147), fill=CLOTH)
    import random
    r = random.Random(3)
    for _ in range(40):
        x, y = r.randint(2, 237), r.randint(26, 145)
        d.point((x, y), fill=GOLD)
    return im


def card(im, col, state, k):
    d = ImageDraw.Draw(im)
    x0, x1 = col * 8 + 2, col * 8 + 53
    cx = (x0 + x1) // 2
    y0, y1 = CARD_Y0 + 2, CARD_Y1 - 2
    if state in ('half_b', 'half_f'):
        x0, x1 = cx - 11, cx + 12
    if state == 'edge':
        d.rectangle((cx - 1, y0, cx + 2, y1), fill=GOLD)
        return
    face = state in ('front', 'half_f')
    d.rounded_rectangle((x0, y0, x1, y1), radius=4, fill=CREAM if face else CARD_B, outline=GOLD)
    if state == 'back':
        d.rounded_rectangle((x0 + 4, y0 + 4, x1 - 4, y1 - 4), radius=2, outline=CARD_BL)
        # een oog met stralen
        d.ellipse((cx - 10, 72, cx + 10, 86), outline=GOLD)
        d.ellipse((cx - 3, 76, cx + 3, 82), fill=GOLD)
        for a in range(0, 360, 45):
            r = math.radians(a)
            d.line((cx + math.cos(r) * 14, 79 + math.sin(r) * 12, cx + math.cos(r) * 20, 79 + math.sin(r) * 18), fill=CARD_BL)
        moon(d, cx, 46, 5, GOLD, CARD_B)
        sun(d, cx, 112, 4, GOLD)
    if state == 'front':
        d.rounded_rectangle((x0 + 3, y0 + 3, x1 - 3, y1 - 3), radius=2, outline=INK)
        title = ['THE TWINS', 'THE MOON', 'DEATH'][k]
        ctext(im, cx, 98, title, INK, None, font='small')
        ctext(im, cx, y0 + 3, ['XVII', 'XVIII', 'XIII'][k], INK, None, font='small')
        if k == 0:
            sun(d, cx - 10, 72, 7, INK)
            moon(d, cx + 12, 72, 8, INK, CREAM)
        elif k == 1:
            moon(d, cx - 2, 72, 15, CARD_B, CREAM)
            for sx, sy in ((cx + 12, 58), (cx + 16, 84), (cx - 16, 92)):
                d.point((sx, sy), fill=GOLD)
                d.point((sx + 1, sy), fill=GOLD)
        else:
            # schedel
            d.ellipse((cx - 11, 58, cx + 11, 80), fill=INK)
            d.rectangle((cx - 7, 78, cx + 7, 88), fill=INK)
            d.ellipse((cx - 7, 66, cx - 2, 72), fill=CREAM)
            d.ellipse((cx + 2, 66, cx + 7, 72), fill=CREAM)
            d.polygon([(cx, 74), (cx - 2, 78), (cx + 2, 78)], fill=CREAM)
            for tx in range(cx - 5, cx + 6, 3):
                d.line((tx, 83, tx, 87), fill=CREAM)
            ctext(im, cx, 108, '(yours)', BLOOD, None, font='small')


def tarot(states, sub=0):
    im = cloth()
    for k, st in enumerate(states):
        card(im, CARD_COLS[k], st, k)
    if sub == 1:
        im = outlined(im, 120, 3, 'TATE: The cards have spoken...', WHITE15, GRAY15, DARK15, scale=1)
    elif sub == 2:
        im = outlined(im, 120, 3, 'LIZA: ...and they hate you.', WHITE15, GRAY15, DARK15, scale=1)
    return im


# ------------------------------------------------------------------ overload: ringen rond de tweeling
def rings(sub=0):
    im = Image.new('RGB', (240, 160), (0, 0, 0))
    a = np.zeros((160, 240, 3), np.uint8)
    for y in range(24, 148):
        for x in range(240):
            r = math.hypot((x + 0.5 - 120) * 0.9, (y + 0.5 - 88) * 1.1)
            band = int(r / 7) % 8
            a[y, x] = RINGS[band]
    im = Image.fromarray(a)
    if sub == 1:
        im = outlined(im, 120, 3, 'TWIN FLAME ENERGY: PEAK PERFORMANCE', YELLOW15, PINK15, DARK15, scale=1, font='narrow')
    elif sub == 2:
        im = outlined(im, 120, -5, 'aaaaaaaaaaaaah', WHITE15, PINK15, DARK15, scale=2)
        s = '(your aura, screaming in lowercase)'
        text(im, 238 - text_width(s, font='narrow'), 146, s, DISC, None, font='narrow')
    return im


enc = Encoder('tateliza', [P13, P14, P15])
ORDER = [('ouija0', ouija(0)), ('ouija1', ouija(1)), ('ouija2', ouija(2)), ('ouija3', ouija(3))]
STATES = ['back', 'half_b', 'edge', 'half_f', 'front']
for st in STATES:
    ORDER.append(('tarot_' + st, tarot([st] * 3)))
ORDER += [('tarot_s1', tarot(['front', 'back', 'back'], 1)), ('tarot_s2', tarot(['front'] * 3, 2)),
          ('rings', rings(0)), ('rings1', rings(1)), ('rings2', rings(2))]
for k, im in ORDER:
    enc.add(im, label=k)
enc.save()
print('letters:', {k: LETTERS[k] for k in ('R', 'I', 'P', 'BYE')}, 'spell cols', SPELL_COLS, 'card cols', CARD_COLS)

# ------------------------------------------------------------------ planchette (gat bovenin: wijst op (16, 11))
PL, PL_D, PL_L = (232, 216, 176), (152, 120, 88), (248, 240, 216)
pl = Image.new('RGB', (32, 32), KEY)
d = ImageDraw.Draw(pl)
d.polygon([(16, 1), (29, 20), (25, 29), (7, 29), (3, 20)], fill=PL_D)
d.polygon([(16, 3), (27, 20), (24, 27), (8, 27), (5, 20)], fill=PL)
d.line((9, 20, 16, 5), fill=PL_L)
d.ellipse((12, 7, 20, 15), fill=PL_D)
d.ellipse((13, 8, 19, 14), fill=KEY)
for fx in (8, 24):
    d.rectangle((fx - 1, 29, fx, 30), fill=INK)
save_sprite('tateliza_planchette', pl)

if PREVIEW:
    shots = [enc.render(m) for m in enc.maps]
    src = Image.open(os.path.join(OUT, '..', 'trainers/front_pics/leader_tate_and_liza.png'))
    a = np.array(src.convert('RGBA'))
    a[np.array(src) == 0] = 0
    tl = Image.fromarray(a)
    pa = np.array(pl.convert('RGBA'))
    pa[(np.array(pl) == KEY).all(2)] = 0
    pls = Image.fromarray(pa)
    comp = shots[3].copy()
    x, y = LETTERS['P']
    comp.paste(pls, (x - 16, y - 11), pls)
    shots.append(comp)
    comp = shots[-2].copy()
    comp.paste(tl, (88, 60), tl)
    shots.append(comp)
    preview_strip(shots, PREVIEW)
