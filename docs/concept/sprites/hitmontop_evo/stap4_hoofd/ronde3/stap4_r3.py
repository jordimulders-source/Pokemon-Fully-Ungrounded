"""Stap 4 ronde 3 (6 nov, reparatieronde vanaf ronde 2 optie 1M): een goed hoofd op de vorm van stap 3b optie C.
Jordi: "we gaan er eerst een goed hoofd op zetten. Gebaseerd op Hitmontop, die maken we zodat die goed past in de hoek
en de pose die we van plan zijn. De stekel bovenop het hoofd van Hitmontop wordt iets minder aanwezig en de 'haren'
kammen we naar achteren in een klein staartje of knotje [...] voor de rest gaan we nog nergens aan zitten".
De hoofden zijn met de hand als tekstraster getekend (kleuren = Hitmontops normal.pal; zie NOTITIES.md).
Alles buiten het hoofd komt ongewijzigd uit stap3b (bouw('chan', True, KOP_OW), dan zonder kop).
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/stap4_hoofd/ronde3/stap4_r3.py"""
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
'1M-r3': """21 3 ..FFFF
22 3 .F3334F...FF
23 3 F333445F.F34F
24 3 F334455FF345F
25 3 F3445FFFF344FFFF
26 3 .F45F54455544444FF
27 3 ..FF55445335555444FF
28 3 ....F544455444455544F
29 3 ....F5444445444444544FF
30 3 ...F3544444555555554444F
31 3 ...F33544333333333333444F
32 3 ...F44532233333333343344F
33 3 ...F45332335333333433344F
34 3 ..F4533333335533353333F4F
35 3 ..F553333333335553FFFF34F
36 3 ..F333333F33333333FF1F34F
37 3 ..F3333333FFFF3333FFFFF4F
38 3 ..F3333333FF1F33333FF3F4F
39 3 ...F333333FFFF3333533F34F
40 3 ...F3333333FF3333355F344F
41 3 ...F3333353333F333333344F
42 3 ...F33333355FF35F333F534F
43 3 ....F333333333333FFF334F
44 3 .....FF33333333333444FF
45 3 .......FF3333444444FF
46 3 .........FF334444FF
47 3 ...........FFFFFF""",   # 1M gerepareerd (ronde 3)
'1M-r3-knot': """20 0 ..FFFF
21 0 .F3334F
22 0 F333445F.....FF
23 0 F334455F....F34F
24 0 F3445FFFF..F345F
25 0 .F45F5544F.F344FFFF
26 0 ..FFF54444F55544444FF
27 0 .....FF54455335555444FF
28 0 .......F544455444455544F
29 0 .......F5444445444444544FF
30 0 ......F3544444555555554444F
31 0 ......F33544333333333333444F
32 0 ......F44532233333333343344F
33 0 ......F45332335333333433344F
34 0 .....F4533333335533353333F4F
35 0 .....F553333333335553FFFF34F
36 0 .....F333333F33333333FF1F34F
37 0 .....F3333333FFFF3333FFFFF4F
38 0 .....F3333333FF1F33333FF3F4F
39 0 ......F333333FFFF3333533F34F
40 0 ......F3333333FF3333355F344F
41 0 ......F3333353333F333333344F
42 0 ......F33333355FF35F333F534F
43 0 .......F333333333333FFF334F
44 0 ........FF33333333333444FF
45 0 ..........FF3333444444FF
46 0 ............FF334444FF
47 0 ..............FFFFFF""",   # idem, knot meer naar achter/boven
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
    '1M-r3': 'stand 1, mond 1M, reparaties ronde 3',
    '1M-r3-knot': 'idem, knot meer naar achter/boven',
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
        im.save(os.path.join(HERE, 'optie_%s.png' % naam))
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
        v.save(os.path.join(HERE, 'hoofd_%s.png' % naam))
        tegels.append((naam, oms, im))
    # vel: per optie 8x (uitsnede rond het hoofd), 1x en 2x van de hele sprite, naast Hitmontop
    CROP = (0, 14, 40, 50); cw, ch = (CROP[2] - CROP[0]) * Z, (CROP[3] - CROP[1]) * Z
    kol = 2; TW = max(cw, 420) + 20; TH = ch + 180
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
