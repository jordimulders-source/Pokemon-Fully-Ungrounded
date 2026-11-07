"""Stap 4 ronde 3b (6 nov, pixelreparaties op ronde 3 optie 1M-r3-knot): een goed hoofd op de vorm van stap 3b optie C.
Jordi: "we gaan er eerst een goed hoofd op zetten. Gebaseerd op Hitmontop, die maken we zodat die goed past in de hoek
en de pose die we van plan zijn. De stekel bovenop het hoofd van Hitmontop wordt iets minder aanwezig en de 'haren'
kammen we naar achteren in een klein staartje of knotje [...] voor de rest gaan we nog nergens aan zitten".
De hoofden zijn met de hand als tekstraster getekend (kleuren = Hitmontops normal.pal; zie NOTITIES.md).
Alles buiten het hoofd komt ongewijzigd uit stap3b (bouw('chan', True, KOP_OW), dan zonder kop).
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/stap4_hoofd/ronde3b/stap4_r3b.py"""
import os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../../..')
S3B = os.path.join(HERE, '../../stap3b/stap3b.py')
g = {'__file__': os.path.abspath(S3B)}
exec(compile(open(S3B).read().replace('\nmain()\n', '\n'), 'stap3b.py', 'exec'), g)
LEEG = (Image.new('RGBA', (64, 64), (0, 0, 0, 0)), (10, 10), (10, 20))
BASIS = g['bouw']('chan', True, LEEG)                     # stap 3b optie C zonder hoofd
OPTIE_C = Image.open(os.path.join(HERE, '../../stap3b/optie_C.png')).convert('RGBA')

# Hitmontops palet (graphics/pokemon/hitmontop/normal.pal): 1 wit, 2/3/4 huid licht/midden/schaduw, 5 donkerbruin, F omlijning
PAL = {'1': (255, 255, 255), '2': (255, 222, 156), '3': (222, 189, 131), '4': (180, 139, 90), '5': (131, 90, 41), 'F': (16, 16, 16)}

# rijen: "y x0 pixels" ('.' = leeg), schermcoordinaten. Met de hand opgebouwd: gezicht = Hitmontops gezicht
# (gespiegeld, ogen/plooien/fronslijnen exact uit anim_front.png) + zware bovenrand; haar glad naar achteren gekamd naar
# het knotje; Hitmontops hoorn in het klein. Zie NOTITIES.md.
HOOFD = {
'1M-r3b': """20 1 ..FFF
21 1 .F344F
22 1 F33444F.....FF
23 1 F444455F...F34F
24 1 F4455FFFF.F345F
25 1 .F455F544FF344FFFF
26 1 ..FFF5445555544444FF
27 1 .....FF5455335555444FF
28 1 ......F544455444455544F
29 1 ......F5444445444444544FF
30 1 .....F4544444444443333344F
31 1 .....F44544443333333333444F
32 1 .....F44532233333333343344F
33 1 .....F45332335333333433344F
34 1 ....F4533333335533353333F4F
35 1 ....F553333333335553FFFF34F
36 1 ....F333333F33333333FF1F34F
37 1 ....F3333333FFFF3333FFFFF4F
38 1 ....F3333333FF1F33333FF3F4F
39 1 .....F333333FFFF3333533F34F
40 1 .....F3333333FF3333355F344F
41 1 .....F3333353333F333333344F
42 1 .....F33333355FF34F333F334F
43 1 ......F333333333333FFF334F
44 1 .......FF33333333333333FF
45 1 .........FF3333444444FF
46 1 ...........FF334444FF
47 1 .............FFFFFF""",   # r3-knot met pixelreparaties ronde 3b
}


def lees(txt):
    d = {}
    for regel in txt.strip().split('\n'):
        y, x0, r = regel.split(' ', 2)
        for i, c in enumerate(r):
            if c in PAL:
                d[(int(x0) + i, int(y))] = c
    return d


def hoofd(naam):
    """dict (x,y) -> paletletter van het hele hoofd (incl. knotje en hoorn)."""
    return lees(HOOFD[naam])


def plak(d):
    im = BASIS.copy()
    for p, c in d.items():
        im.putpixel(p, PAL[c] + (255,))
    return im


OPTIES = {
    '1M-r3b': 'stand 1, mond 1M, knot achter/boven, reparaties 3b',
}


def wit(im, z, bg=(255, 255, 255)):
    b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im)
    return b.resize((im.width * z, im.height * z), Image.NEAREST).convert('RGB')


def controle(im, d):
    """pixeldiff t.o.v. stap3b optie C buiten de hoofdzone (nieuw hoofd + wat het oude hoofd vrijgeeft) moet 0 zijn."""
    oud = {(x, y) for y in range(64) for x in range(64) if OPTIE_C.getpixel((x, y)) != BASIS.getpixel((x, y))}
    zone = oud | set(d)
    buiten = [(x, y) for y in range(64) for x in range(64)
              if (x, y) not in zone and im.getpixel((x, y)) != OPTIE_C.getpixel((x, y))]
    xs = [p[0] for p in zone]; ys = [p[1] for p in zone]
    return len(buiten), (min(xs), min(ys), max(xs), max(ys)), len(oud), len(d)


def main():
    TOP = Image.open(os.path.join(ROOT, 'graphics/pokemon/hitmontop/anim_front.png')).convert('RGBA').crop((0, 0, 64, 64))
    ow = Image.open(os.path.join(ROOT, 'graphics/pokemon/hitmontop/overworld.png')).convert('RGBA').crop((0, 0, 32, 32))
    bgc = ow.getpixel((0, 0)); ow.putdata([(0, 0, 0, 0) if q == bgc else q for q in ow.get_flattened_data()])
    TOPKOP = TOP.crop((10, 26, 56, 58)); OWKOP = ow.crop((5, 8, 27, 30))
    rapport = []
    Z = 8; tegels = []
    for naam, oms in OPTIES.items():
        d = hoofd(naam); im = plak(d)
        im.save(os.path.join(HERE, 'optie.png'))
        n, box, noud, nnieuw = controle(im, d)
        rapport.append('optie_%s: %s | buiten zone anders: %d | zone (x0,y0,x1,y1) %s (oud hoofd %d px, nieuw hoofd %d px)'
                       % (naam, oms, n, box, noud, nnieuw))
        los = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        for p, c in d.items():
            los.putpixel(p, PAL[c] + (255,))
        los = los.crop(los.getchannel('A').getbbox())
        panelen = [(los, 'optie %s: hoofd los' % naam, (255, 255, 255)), (TOPKOP, 'Hitmontop front', (152, 208, 160)),
                   (OWKOP, 'Hitmontop overworld', (152, 208, 160))]
        H = max(p.height for p, t, b in panelen) * Z + 40; Wd = sum(p.width * Z + 20 for p, t, b in panelen) + 20
        v = Image.new('RGB', (Wd, H), (235, 235, 240)); dr = ImageDraw.Draw(v); x = 20
        for p, t, b in panelen:
            v.paste(wit(p, Z, b), (x, 30)); dr.text((x, 10), t, fill=(0, 0, 0)); x += p.width * Z + 20
        v.save(os.path.join(HERE, 'hoofd.png'))
        tegels.append((naam, oms, im))
    # vel: per optie 8x (uitsnede rond het hoofd), 1x en 2x van de hele sprite, naast Hitmontop
    CROP = (0, 14, 40, 50); cw, ch = (CROP[2] - CROP[0]) * Z, (CROP[3] - CROP[1]) * Z
    kol = 1; TW = max(cw, 420) + 20; TH = ch + 180
    rijen = (len(tegels) + kol - 1) // kol
    vel = Image.new('RGB', (20 + TW * kol, 20 + TH * rijen), (235, 235, 240)); dr = ImageDraw.Draw(vel)
    for k, (naam, oms, im) in enumerate(tegels):
        x = 20 + (k % kol) * TW; y = 20 + (k // kol) * TH
        dr.text((x, y), 'optie_%s: %s' % (naam, oms), fill=(0, 0, 0))
        vel.paste(wit(im.crop(CROP), Z), (x, y + 16))
        yy = y + 16 + ch + 8
        vel.paste(wit(im, 1), (x, yy)); vel.paste(wit(TOP, 1, (152, 208, 160)), (x + 70, yy))
        vel.paste(wit(im, 2), (x + 140, yy)); vel.paste(wit(TOP, 2, (152, 208, 160)), (x + 275, yy))
        dr.text((x, yy + 132), '1x optie | 1x Hitmontop | 2x optie | 2x Hitmontop', fill=(0, 0, 0))
    vel.save(os.path.join(HERE, 'vel_hoofd.png'))
    open(os.path.join(HERE, 'controle.txt'), 'w').write('\n'.join(rapport) + '\n')
    print('\n'.join(rapport))


main()
