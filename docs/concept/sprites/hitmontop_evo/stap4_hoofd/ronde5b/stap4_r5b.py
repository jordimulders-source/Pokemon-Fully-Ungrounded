"""Stap 4 hoofd ronde 5b (6 nov): alleen reparaties op ronde 5 optie 2 (zie ronde5/vel_hoofd.png.keuring.md).
Ronde 5: alleen het hoofd, los (Jordi: "design eerst maar puur het hoofd zonder de rest" / "dan keuren we dat").
Jordi: "het haar is niet anders dan het hoofd, het is hetzelfde materiaal en dezelfde kleur, er zit dus geen streep tussen";
"kijk aub een keer goed naar hitmontop en stop met dingen verzinnen"; "rare kippenpoot heeft die ook in zijn haar";
"de enige streep is wat nu boven zijn ogen zit, maar gezien die haren nu dus naar achter gaan, komt die streep veel hoger te
staan, een beetje als een fade". Kop = een glad geheel (schedel, kleine punt, knot) in Hitmontops huidtinten; de enige streep
is de flaprand, naar achteren gekamd hoog op het voorhoofd, als fade (midden 5, uitlopend in 4, los van de omtrek).
Omtrek eerst als gids 27 graden tegen de klok in gedraaid, daarna per pixel met de hand. Coordinaten = schermpixels van de
64x64-sprite, zodat het hoofd later zo op de vorm (stap3b optie C) kan.
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/stap4_hoofd/ronde5b/stap4_r5b.py"""
import os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../../..')
# Hitmontops palet (graphics/pokemon/hitmontop/normal.pal): 1 wit, 2/3/4 huid licht/midden/schaduw, 5 donkerste huid, F omlijning
PAL = {'1': (255, 255, 255), '2': (255, 222, 156), '3': (222, 189, 131), '4': (180, 139, 90), '5': (131, 90, 41), 'F': (16, 16, 16)}
BG = (152, 208, 160)
HOOFD = {
'2b': """22 8 F
23 3 FFF.F3F
24 2 F223F33F
25 1 F2333F334F
26 1 F333333333F
27 1 F3333333333FFFFFF
28 1 F3333333333333333FFF
29 2 F333333333333333334F
30 2 F3333333333334333334F
31 3 F3333333333533333334F
32 4 F333333455333333334F
33 4 F3333333333333333334F
34 4 F3333333333333333334F
35 3 F333333333333333FF334F
36 3 F33333333333333F1FF34F
37 3 F33333333333333FFFF34F
38 3 F333333333333333FF334F
39 3 F33333333FF3333333334F
40 4 F333333F1FF333333334F
41 4 F333333FFFF33333334F
42 5 F333333FF333333334F
43 5 F3333333333333FF33F
44 6 F3333333333FF333F
45 7 F3333333333333F
46 8 FF3333333333F
47 10 FFFFFFFFFF""",
}
OPTIES = {'2b': 'ronde 5b: optie 2 met de benoemde reparaties'}


def hoofd(naam):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    for regel in HOOFD[naam].strip().split('\n'):
        y, x0, r = regel.split(' ', 2)
        for i, c in enumerate(r):
            if c in PAL:
                im.putpixel((int(x0) + i, int(y)), PAL[c] + (255,))
    return im


def op(im, z):
    b = Image.new('RGBA', im.size, BG + (255,)); b.alpha_composite(im)
    return b.resize((im.width * z, im.height * z), Image.NEAREST).convert('RGB')


def main():
    top = Image.open(os.path.join(ROOT, 'graphics/pokemon/hitmontop/anim_front.png')).convert('RGBA').crop((0, 0, 64, 64))
    topkop = top.crop((10, 26, 56, 58))
    anime = Image.open(os.path.join(HERE, '../../referenties/hitmontop_anime.webp')).convert('RGB').crop((320, 40, 1000, 500))
    anime = anime.resize((anime.width * 260 // anime.height, 260))
    koppen = {}
    for n in OPTIES:
        im = hoofd(n); im.save(os.path.join(HERE, 'hoofd.png'))
        koppen[n] = im.crop(im.getchannel('A').getbbox())
    # vel: per rij een optie (8x, 2x, 1x), onderaan Hitmontops kop (8x, 2x, 1x), rechts de anime
    Z = 8
    rijen = [('optie %s: %s' % (n, OPTIES[n]), koppen[n]) for n in OPTIES] + [('Hitmontop (sprite, kop)', topkop)]
    W = 20 + 46 * Z + 20 + 46 * 2 + 20 + 46 + 20 + anime.width + 20
    H = 20 + sum(k.height * Z + 40 for _, k in rijen)
    v = Image.new('RGB', (W, max(H, anime.height + 60)), (235, 235, 240)); dr = ImageDraw.Draw(v); y = 20
    for t, k in rijen:
        dr.text((20, y), t + '   (8x | 2x | 1x)', fill=(0, 0, 0))
        x = 20; v.paste(op(k, Z), (x, y + 16)); x += 46 * Z + 20
        v.paste(op(k, 2), (x, y + 16)); x += 46 * 2 + 20
        v.paste(op(k, 1), (x, y + 16))
        y += k.height * Z + 40
    ax = W - anime.width - 20
    v.paste(anime, (ax, 36)); dr.text((ax, 20), 'anime (referentie)', fill=(0, 0, 0))
    v.save(os.path.join(HERE, 'vel_hoofd.png'))


main()
