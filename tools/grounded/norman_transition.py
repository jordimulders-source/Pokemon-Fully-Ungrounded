#!/usr/bin/env python3
"""Project Grounded: gymleider-intro Norman ("Hm... a new season of BLACK MIRROR... Ok, I'm sick of you, face my
SLAKING!"). Het startscherm van NORMFLIX (Continue watching for DAD), dan "Are you still watching?": de cursor gaat
even naar "Go outside", springt vanzelf terug, Continue. Pauze. Het beeld krimpt terug in de tv in de woonkamer: daar
hangt Slaking op de bank (Zzz), Norman met de afstandsbediening: "OK, I'M SICK OF YOU." / "FACE MY SLAKING!".

BG0 (paletten 13-15): het startscherm (palet 13; de C-code dimt dat palet achter de vraag), de vraag en de pauzeknop
(palet 15), de woonkamer (palet 14) met de ondertitels in de zwarte balken (palet 15).
Sprites: Norman (trainerfoto), Slaking (zijn eigen frontsprite), Zzz (Snore uit de gevechtsanimaties).
Paletindexen die de C-code animeert (src/data/gym_intros_b.h, "Norman"): BG 13 index HL = rand van de geselecteerde
titel; BG 15 index BTN_A/BTN_B = de knoppen; BG 14 index WALL_LIT/SCREEN = tv-licht in de kamer.
Gebruik: python3 tools/grounded/norman_transition.py [voorbeeld.png]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
from gym_intro_lib import outlined_text as outlined, Encoder, text, text_width, preview_strip, OUT, KEY, gba

PREVIEW = sys.argv[1] if len(sys.argv) > 1 else None

# ------------------------------------------------------------------ paletten
BG, RED, WHITE, LGRAY, MGRAY, HL = (16, 16, 16), (224, 8, 16), (248, 248, 248), (184, 184, 184), (96, 96, 96), (232, 232, 232)
TC = [(24, 40, 80), (48, 72, 128), (32, 88, 80), (64, 128, 112), (104, 72, 40), (144, 104, 64), (88, 32, 88),
      (128, 64, 120), (40, 64, 40)]
THUMBS = [(TC[0], TC[1]), (TC[2], TC[3]), (TC[4], TC[5]), (TC[6], TC[7]), (TC[8], MGRAY), (TC[0], TC[7])]
P13 = [BG, RED, WHITE, LGRAY, MGRAY, HL] + TC   # 15

WALL, WALL_LIT, FLOOR, FLOOR2 = (32, 32, 56), (56, 64, 104), (64, 44, 40), (44, 30, 32)
COUCH, COUCH_D, COUCH_L = (136, 64, 48), (96, 40, 32), (176, 96, 64)
TVF, SCREEN, RED14, WHITE14 = (56, 56, 64), (40, 56, 112), (216, 16, 24), (232, 232, 240)
POSTER, INK, STAND = (208, 192, 152), (72, 48, 40), (96, 72, 56)
P14 = [WALL, WALL_LIT, FLOOR, FLOOR2, COUCH, COUCH_D, COUCH_L, TVF, SCREEN, RED14, WHITE14, POSTER, INK, STAND]

MODAL, MBORDER, WHITE15, GRAY15, BTN_A, BTN_B = (48, 48, 48), (88, 88, 88), (240, 240, 240), (160, 160, 160), (64, 64, 64), (64, 64, 72)
YELLOW, RED15, DARK15, DISC = (248, 216, 64), (200, 32, 24), (40, 8, 8), (136, 128, 144)
P15 = [MODAL, MBORDER, WHITE15, GRAY15, BTN_A, BTN_B, YELLOW, RED15, DARK15, DISC]
for n, p in (('P13', P13), ('P14', P14), ('P15', P15)):
    assert len(p) <= 15, n


def idx(pal, c):
    return [gba(x) for x in pal].index(gba(c)) + 1


def ctext(im, cx, y, s, fg, shadow=None, font='normal', scale=1, spacing=0):
    text(im, cx - text_width(s, font, scale, spacing) // 2, y, s, fg, shadow, font, scale, spacing)




# ------------------------------------------------------------------ het startscherm
TITLES = [('BLACK MIRROR', 'S7 E4', 70), ('WHITE LOTUS', '4th rewatch', 95), ('SLAKING:', 'TOO TIRED TO DIE', 40),
          ('PETALBURG', 'HOUSEWIVES', 60), ('HOW TO BE', 'A DAD', 0), ('THE OFFICE', '13th time', 85)]
TX = [8, 84, 160]           # 72 breed
TY = [48, 112]              # 32 hoog


def home():
    im = Image.new('RGB', (240, 160), BG)
    d = ImageDraw.Draw(im)
    text(im, 6, -5, 'NORMFLIX', RED, None, scale=2, spacing=1)
    d.rectangle((216, 6, 231, 21), fill=RED)
    text(im, 219, 5, 'D', WHITE, None, font='narrow')
    text(im, 190, 6, 'DAD', LGRAY, None, font='narrow')
    text(im, 8, 30, 'Continue watching for DAD', WHITE, None, font='narrow')
    text(im, 8, 94, 'Because you watched everything', WHITE, None, font='narrow')
    for i, (a, b, prog) in enumerate(TITLES):
        x, y = TX[i % 3], TY[i // 3]
        c0, c1 = THUMBS[i]
        d.rectangle((x, y, x + 71, y + 31), fill=c0)
        d.polygon([(x + 40, y), (x + 71, y), (x + 71, y + 31), (x + 56, y + 31)], fill=c1)
        text(im, x + 3, y + 1, a, WHITE, None, font='small')
        text(im, x + 3, y + 13, b, LGRAY, None, font='small')
        if i < 3:
            d.rectangle((x, y + 34, x + 71, y + 35), fill=MGRAY)
            if prog:
                d.rectangle((x, y + 34, x + prog * 71 // 100, y + 35), fill=RED)
    # 0% gezien
    text(im, TX[1] + 50, TY[1] + 18, '0%', RED, None, font='small')
    # rand om de eerste titel (HL)
    d.rectangle((TX[0] - 2, TY[0] - 2, TX[0] + 73, TY[0] + 33), outline=HL)
    d.rectangle((TX[0] - 1, TY[0] - 1, TX[0] + 72, TY[0] + 32), outline=HL)
    return im


def still(base):
    im = base.copy()
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 32, 40, 207, 135        # vakken 4..25, rijen 5..16
    d.rectangle((x0, y0, x1, y1), fill=MODAL)
    d.rectangle((x0, y0, x1, y1), outline=MBORDER)
    ctext(im, 120, y0 + 4, 'Are you still watching', WHITE15)
    ctext(im, 120, y0 + 18, 'BLACK MIRROR?', WHITE15)
    d.rectangle((48, 76, 191, 95), fill=BTN_A)
    ctext(im, 120, 78, 'Continue watching', WHITE15)
    d.rectangle((48, 102, 191, 121), fill=BTN_B)
    ctext(im, 120, 104, 'Go outside', WHITE15)
    ctext(im, 120, 121, '(not recommended)', GRAY15, font='small')
    return im


def paused(base):
    im = base.copy()
    d = ImageDraw.Draw(im)
    d.rectangle((96, 56, 143, 103), fill=(0, 0, 0))
    d.rectangle((106, 64, 115, 95), fill=WHITE15)
    d.rectangle((124, 64, 133, 95), fill=WHITE15)
    return im


# ------------------------------------------------------------------ de woonkamer (letterbox: tekst in de zwarte balken)
SCR = (24, 48, 96, 96)     # tv-scherm (x0, y0, x1, y1): hierin krimpt het startscherm


def living(subtitle=0, disclaimer=True):
    im = Image.new('RGB', (240, 160), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 32, 239, 127), fill=WALL)
    # tv-licht op de muur (gedithered rond de tv)
    px = im.load()
    for y in range(32, 128):
        for x in range(0, 140):
            dx, dy = (x - 60) / 78.0, (y - 72) / 46.0
            r = dx * dx + dy * dy
            if r < 0.55 or (r < 1.0 and (x + y) % 2 == 0):
                px[x, y] = WALL_LIT
    d.rectangle((0, 128, 239, 143), fill=FLOOR)
    for y in range(128, 144, 5):
        d.line((0, y, 239, y), fill=FLOOR2)
    # tv op een kastje
    d.rectangle((SCR[0] - 4, SCR[1] - 4, SCR[2] + 3, SCR[3] + 3), fill=TVF)
    d.rectangle((SCR[0], SCR[1], SCR[2] - 1, SCR[3] - 1), fill=SCREEN)
    d.rectangle((SCR[0] + 4, SCR[1] + 4, SCR[0] + 27, SCR[1] + 7), fill=RED14)
    d.rectangle((52, 62, 56, 81), fill=WHITE14)
    d.rectangle((63, 62, 67, 81), fill=WHITE14)
    d.rectangle((SCR[0] + 4, SCR[3] - 7, SCR[2] - 5, SCR[3] - 6), fill=TVF)
    d.rectangle((SCR[0] + 4, SCR[3] - 7, SCR[0] + 50, SCR[3] - 6), fill=RED14)
    d.rectangle((16, 100, 103, 127), fill=STAND)
    d.rectangle((20, 106, 99, 108), fill=INK)
    d.rectangle((20, 116, 99, 118), fill=INK)
    d.rectangle((14, 128, 19, 133), fill=INK)
    d.rectangle((100, 128, 105, 133), fill=INK)
    # poster boven de bank
    d.rectangle((136, 38, 191, 61), fill=POSTER)
    d.rectangle((136, 38, 191, 61), outline=INK)
    ctext(im, 164, 36, "LIVE LAUGH", INK, None, font='small')
    ctext(im, 164, 47, "LOAF", INK, None, font='small')
    # bank
    d.rounded_rectangle((128, 84, 235, 116), radius=6, fill=COUCH_D)
    d.rounded_rectangle((132, 88, 231, 112), radius=5, fill=COUCH)
    d.line((182, 90, 182, 110), fill=COUCH_D)
    d.rectangle((124, 110, 239, 131), fill=COUCH)
    d.rectangle((124, 110, 239, 113), fill=COUCH_L)
    d.rounded_rectangle((120, 100, 136, 134), radius=4, fill=COUCH_D)
    d.rounded_rectangle((228, 100, 239, 134), radius=4, fill=COUCH_D)
    d.rectangle((130, 132, 135, 137), fill=INK)
    d.rectangle((226, 132, 231, 137), fill=INK)
    if subtitle == 1:
        im = outlined(im, 120, 2, 'OK, I’M SICK OF YOU.', WHITE15, GRAY15, DARK15, scale=1)
    elif subtitle == 2:
        im = outlined(im, 120, 0, 'FACE MY SLAKING!', YELLOW, RED15, DARK15, scale=2)
    if disclaimer:
        s = 'Your free trial expires in 10 minutes.'
        text(im, 238 - text_width(s, font='narrow'), 146, s, DISC, None, font='narrow')
    return im


enc = Encoder('norman', [P13, P14, P15])
H = home()
for k, im in (('home', H), ('still', still(H)), ('pause', paused(H)), ('room', living(0)), ('room1', living(1)),
              ('room2', living(2))):
    enc.add(im, label=k)
enc.save()
print('BG13 HL=%d  BG15 BTN_A=%d BTN_B=%d  BG14 WALL_LIT=%d SCREEN=%d' % (
    idx(P13, HL), idx(P15, BTN_A), idx(P15, BTN_B), idx(P14, WALL_LIT), idx(P14, SCREEN)))

if PREVIEW:
    shots = [enc.render(m) for m in enc.maps]
    def pic(path, pal_from=None):
        src = Image.open(path)
        a = np.array(src.convert('RGBA'))
        a[np.array(src) == 0] = 0
        return Image.fromarray(a)
    nor = pic(os.path.join(OUT, '..', 'trainers/front_pics/leader_norman.png'))
    sl = Image.open(os.path.join(OUT, '..', 'pokemon/slaking/anim_front.png')).crop((0, 0, 64, 64))
    sa = np.array(sl.convert('RGBA'))
    sa[np.array(sl) == 0] = 0
    sl = Image.fromarray(sa)
    comp = shots[5].copy()
    comp.paste(sl, (148, 66), sl)
    comp.paste(nor, (76, 80), nor)
    shots.append(comp)
    preview_strip(shots, PREVIEW)
