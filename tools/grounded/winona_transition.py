#!/usr/bin/env python3
"""Project Grounded: gymleider-intro Winona (budgetvliegmaatschappij, jetlag, "I just want to retreat to my tree
house"). Het vertrekbord van WINAIR: FORTREE staat op DELAYED, de flappen ratelen om naar BOARDING (ding-dong). Dan de
gate: door het raam vliegt haar 'vliegtuig' over (Altaria), Winona staat op het tapijt met haar koffertje, dat openspringt:
veren alle kanten op. "BAGGAGE FEE!" / "No miles earned."

BG0 (paletten 13-15): het vertrekbord in vier standen van de statusflap (palet 13), de gate (palet 14) met de
ondertitels in de zwarte balken (palet 15).
Sprites: Winona (trainerfoto), Altaria (frontsprite), het koffertje (eigen, 2 frames), veren (White Feather uit de
gevechtsanimaties).
Paletindexen die de C-code animeert (src/data/gym_intros_b.h, "Winona"): BG 13 index STATUS = de statusflap van WN001.
Gebruik: python3 tools/grounded/winona_transition.py [voorbeeld.png]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
from gym_intro_lib import outlined_text as outlined, Encoder, text, text_width, _font, _CM, save_sprite, preview_strip, OUT, KEY, gba

PREVIEW = sys.argv[1] if len(sys.argv) > 1 else None

BGK, CELL, CELL_LINE, YELLOW, WHITE, GRAY, STATUS, RED = (16, 16, 24), (48, 48, 56), (24, 24, 32), (248, 216, 64), \
    (232, 232, 232), (128, 128, 144), (232, 64, 48), (200, 48, 40)
LILAC, ORANGE, PANEL = (176, 128, 216), (248, 144, 40), (32, 32, 48)
P13 = [BGK, CELL, CELL_LINE, YELLOW, WHITE, GRAY, STATUS, RED, LILAC, ORANGE, PANEL]

SKY = [(96, 144, 224), (128, 176, 232), (168, 208, 240)]
CLOUD, CLOUD_S = (248, 248, 248), (208, 224, 240)
RUNWAY, DASH, GRASS = (104, 104, 112), (232, 200, 64), (96, 152, 80)
FRAME, FRAME_L = (48, 48, 64), (88, 88, 104)
CARPET = [(64, 40, 80), (96, 64, 120), (48, 112, 144)]
P14 = SKY + [CLOUD, CLOUD_S, RUNWAY, DASH, GRASS, FRAME, FRAME_L] + CARPET

WHITE15, GRAY15, YELLOW15, RED15, DARK15, DISC = (240, 240, 240), (160, 160, 168), (248, 224, 72), (216, 40, 32), \
    (48, 8, 8), (136, 128, 144)
P15 = [WHITE15, GRAY15, YELLOW15, RED15, DARK15, DISC]


def idx(pal, c):
    return [gba(x) for x in pal].index(gba(c)) + 1


def ctext(im, cx, y, s, fg, shadow=None, font='normal', scale=1, spacing=0):
    text(im, cx - text_width(s, font, scale, spacing) // 2, y, s, fg, shadow, font, scale, spacing)




# ------------------------------------------------------------------ het vertrekbord (split-flap: elk teken een vakje)
PITCH, X0 = 8, 8
ROWS = [('WN001', 'FORTREE', None), ('WN007', 'TREE HOUSE', 'CANCELLED'), ('WN013', 'LILYCOVE', 'LOST BAGS'),
        ('WN404', 'YOUR MILES', 'NOT FOUND'), ('WN666', 'ANYWHERE', 'SOLD OUT')]
ROW_Y = [44, 64, 84, 104, 124]
STATUS_COL = 17
FLAPS = ['DELAYED', '#?&%!@$', '&%$#?!@', 'BOARDING']


def flap_char(im, col, y, ch, fg):
    d = ImageDraw.Draw(im)
    x = X0 + col * PITCH
    d.rectangle((x, y, x + PITCH - 2, y + 13), fill=CELL)
    d.line((x, y + 7, x + PITCH - 2, y + 7), fill=CELL_LINE)
    if ch != ' ':
        if ch not in _CM:
            ch = '?'
        _, w = _font('normal')
        cw = w[_CM[ch]]
        text(im, x + (PITCH - 1 - cw) // 2, y - 2, ch, fg, None)


def flap_text(im, col, y, s, n, fg):
    for i in range(n):
        flap_char(im, col + i, y, s[i] if i < len(s) else ' ', fg)


def board(status):
    im = Image.new('RGB', (240, 160), BGK)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 239, 23), fill=PANEL)
    x = text(im, 6, -4, 'WIN', LILAC, None, scale=2, spacing=1)
    text(im, x, -4, 'AIR', ORANGE, None, scale=2, spacing=1)
    s = 'DEPARTURES'
    text(im, 234 - text_width(s, font='narrow'), 4, s, WHITE, None, font='narrow')
    text(im, 8, 26, 'FLIGHT', GRAY, None, font='small')
    text(im, X0 + 6 * PITCH, 26, 'TO', GRAY, None, font='small')
    text(im, X0 + STATUS_COL * PITCH, 26, 'STATUS', GRAY, None, font='small')
    for (fl, dest, st), y in zip(ROWS, ROW_Y):
        flap_text(im, 0, y, fl, 5, WHITE)
        flap_text(im, 6, y, dest, 10, YELLOW)
        flap_text(im, STATUS_COL, y, status if st is None else st, 11, STATUS if st is None else RED)
    s = 'Seat: 2,000P.  Armrest: 500P.  Air: 50P/min.'
    ctext(im, 120, 143, s, GRAY, None, font='small')
    return im


# ------------------------------------------------------------------ de gate: raam met lucht en startbaan, tapijt
def gate(sub=0):
    im = Image.new('RGB', (240, 160), (0, 0, 0))
    d = ImageDraw.Draw(im)
    px = im.load()
    for y in range(24, 104):
        for x in range(240):
            b = 0 if y < 50 else (1 if y < 78 else 2)
            if b < 2 and (50, 78)[b] - y <= 3 and (x + y) % 2 == 0:
                b += 1
            px[x, y] = SKY[b]
    for cx, cy, r in ((40, 44, 10), (54, 40, 13), (70, 46, 9), (176, 64, 9), (190, 60, 12), (204, 66, 8)):
        d.ellipse((cx - r, cy - r * 2 // 3, cx + r, cy + r * 2 // 3), fill=CLOUD)
    for cx, cy, r in ((54, 46, 12), (190, 66, 10)):
        d.line((cx - r, cy + 2, cx + r, cy + 2), fill=CLOUD_S, width=2)
    d.rectangle((0, 96, 239, 99), fill=GRASS)
    d.rectangle((0, 100, 239, 111), fill=RUNWAY)
    for x in range(4, 240, 24):
        d.rectangle((x, 105, x + 11, 106), fill=DASH)
    d.rectangle((0, 112, 239, 115), fill=GRASS)
    # raamstijlen
    for x0 in (0, 76, 156, 232):
        d.rectangle((x0, 24, x0 + 7, 119), fill=FRAME)
        d.line((x0 + 2, 24, x0 + 2, 119), fill=FRAME_L)
    d.rectangle((0, 24, 239, 29), fill=FRAME)
    d.rectangle((0, 116, 239, 119), fill=FRAME)
    d.line((0, 117, 239, 117), fill=FRAME_L)
    # het beruchte vliegveldtapijt
    for y in range(120, 144):
        for x in range(240):
            u, v = x % 16, (y - 120) % 16
            c = CARPET[0]
            if (u + v) % 16 in (0, 1) or (u - v) % 16 in (0, 1):
                c = CARPET[1]
            if u in (7, 8) and v in (7, 8):
                c = CARPET[2]
            px[x, y] = c
    if sub == 1:
        im = outlined(im, 120, 3, 'Elegant. Soaring. Delayed.', WHITE15, GRAY15, DARK15, scale=1)
    elif sub == 2:
        im = outlined(im, 120, -4, 'BAGGAGE FEE!', YELLOW15, RED15, DARK15, scale=2)
    s = 'No miles earned. WINAIR: we fly, you pay.' if sub == 2 else 'WINAIR: we fly, you pay.'
    text(im, 238 - text_width(s, font='narrow'), 146, s, DISC, None, font='narrow')
    return im


enc = Encoder('winona', [P13, P14, P15])
for k, im in [('flap%d' % i, board(f)) for i, f in enumerate(FLAPS)] + [('gate', gate(0)), ('gate1', gate(1)), ('gate2', gate(2))]:
    enc.add(im, label=k)
enc.save()
print('BG13 STATUS=%d  status: kolom %d-29, rij %d-%d' % (idx(P13, STATUS), (X0 + STATUS_COL * PITCH) // 8, ROW_Y[0] // 8,
                                                         (ROW_Y[0] + 13) // 8))

# ------------------------------------------------------------------ het koffertje (2 frames: dicht, open)
SHELL, SHELL_D, SHELL_L, METAL, INSIDE, SOCK, OUTL = (152, 72, 168), (104, 48, 120), (200, 128, 216), (208, 208, 216), \
    (56, 32, 64), (248, 168, 48), (32, 16, 40)
case = Image.new('RGB', (32, 64), KEY)
d = ImageDraw.Draw(case)
# dicht
d.rectangle((12, 10, 19, 13), outline=OUTL)
d.rounded_rectangle((3, 13, 28, 31), radius=3, fill=SHELL, outline=OUTL)
d.line((6, 15, 6, 29), fill=SHELL_L)
d.line((4, 21, 27, 21), fill=SHELL_D)
d.rectangle((14, 20, 17, 22), fill=METAL)
d.line((10, 15, 10, 29), fill=SHELL_D)
d.line((21, 15, 21, 29), fill=SHELL_D)
# open: deksel omhoog, binnenkant, een sok
d.rounded_rectangle((3, 32 + 2, 28, 32 + 12), radius=3, fill=SHELL_D, outline=OUTL)
d.line((6, 32 + 4, 25, 32 + 4), fill=SHELL)
d.rounded_rectangle((3, 32 + 21, 28, 32 + 31), radius=3, fill=SHELL, outline=OUTL)
d.rectangle((5, 32 + 13, 26, 32 + 21), fill=INSIDE, outline=OUTL)
d.polygon([(9, 32 + 18), (15, 32 + 15), (17, 32 + 17), (12, 32 + 21)], fill=SOCK)
d.rectangle((14, 32 + 24, 17, 32 + 26), fill=METAL)
save_sprite('winona_case', case)

if PREVIEW:
    shots = [enc.render(m) for m in enc.maps]
    def pic(src):
        a = np.array(src.convert('RGBA'))
        a[np.array(src) == 0] = 0
        return Image.fromarray(a)
    win = pic(Image.open(os.path.join(OUT, '..', 'trainers/front_pics/leader_winona.png')))
    alt = pic(Image.open(os.path.join(OUT, '..', 'pokemon/altaria/anim_front.png')).crop((0, 0, 64, 64)))
    ca = np.array(case.convert('RGBA'))
    ca[(np.array(case) == KEY).all(2)] = 0
    cs = Image.fromarray(ca)
    comp = shots[6].copy()
    comp.paste(alt, (140, 28), alt)
    comp.paste(win, (60, 76), win)
    comp.paste(cs.crop((0, 32, 32, 64)), (110, 112), cs.crop((0, 32, 32, 64)))
    shots.append(comp)
    preview_strip(shots, PREVIEW)
