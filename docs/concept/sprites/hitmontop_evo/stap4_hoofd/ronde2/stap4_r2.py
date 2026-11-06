"""Stap 4 ronde 2 (6 nov): een goed hoofd op de vorm van stap 3b optie C.
Jordi: "we gaan er eerst een goed hoofd op zetten. Gebaseerd op Hitmontop, die maken we zodat die goed past in de hoek
en de pose die we van plan zijn. De stekel bovenop het hoofd van Hitmontop wordt iets minder aanwezig en de 'haren'
kammen we naar achteren in een klein staartje of knotje [...] voor de rest gaan we nog nergens aan zitten".
De hoofden zijn met de hand als tekstraster getekend (kleuren = Hitmontops normal.pal; zie NOTITIES.md).
Alles buiten het hoofd komt ongewijzigd uit stap3b (bouw('chan', True, KOP_OW), dan zonder kop).
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/stap4_hoofd/ronde2/stap4_r2.py"""
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
'1L': """22 2 .FFFF......FF
23 2 F3344F....F34F
24 2 F3454F...F345F
25 2 F4545F..FF344FFFF
26 2 F4455FFF444444444FF
27 2 .FFFFF5555555344444FF
28 2 ....F4553555555555544F
29 2 ...F333453445535554555FF
30 2 ...F43444555555555555544F
31 2 ...F444455223333333333555F
32 2 ...F444522333333333343344F
33 2 ...F445233335333333433344F
34 2 ...F44233333355333533334FF
35 2 ...F5533333333355533FFFF4F
36 2 ...F223333F333333333FF1F4F
37 2 ...F3333333FFFF33333FFFFFF
38 2 ...F3333333FF1F333333FF4FF
39 2 ...F3333333FFFF33335333F4F
40 2 ...F33333333FF33333355F44F
41 2 ...F33333353333F333333344F
42 2 ...F333333355FF3353335344F
43 2 ....F3333333333333FFF334F
44 2 .....F333333333333344444F
45 2 ......FF33333344444444FF
46 2 ........FF3333444444FF
47 2 ..........FFFFFFFFFF""",   # stand 1 (±15°), mond licht
'1M': """22 2 .FFFF......FF
23 2 F3344F....F34F
24 2 F3454F...F345F
25 2 F4545F..FF344FFFF
26 2 F4455FFF444444444FF
27 2 .FFFFF5555555344444FF
28 2 ....F4553555555555544F
29 2 ...F333453445535554555FF
30 2 ...F43444555555555555544F
31 2 ...F444455223333333333555F
32 2 ...F444522333333333343344F
33 2 ...F445233335333333433344F
34 2 ...F44233333355333533334FF
35 2 ...F5533333333355533FFFF4F
36 2 ...F223333F333333333FF1F4F
37 2 ...F3333333FFFF33333FFFFFF
38 2 ...F3333333FF1F333333FF4FF
39 2 ...F3333333FFFF33335333F4F
40 2 ...F33333333FF33333355F44F
41 2 ...F33333353333F333333344F
42 2 ...F333333355FF35F333F544F
43 2 ....F3333333333333FFF334F
44 2 .....F333333333333344444F
45 2 ......FF33333344444444FF
46 2 ........FF3333444444FF
47 2 ..........FFFFFFFFFF""",   # stand 1 (±15°), mond iets meer
'2L': """24 0 ........FF
25 0 .......F34F.FFFFFF
26 0 .......F345F444444FFF
27 0 ........F344444444445FF
28 0 .FFFF..F334444445555555FF
29 0 F3344FF334445555455333345F
30 0 F3454FF3555555555333333F4F
31 0 F4545F5555445553334FFFF344F
32 0 F4455F5455553333334FF1F344F
33 0 .FFFFF5444523333353FFFFF344F
34 0 .....F45452353555533FF33344F
35 0 .....F44523333333333333F344F
36 0 .....F442333F333333533F3344F
37 0 ......F533333FFFF3335533344F
38 0 ......F233333FF1F3333333344F
39 0 ......F333333FFFF3333333344F
40 0 .......F333333FF3333333344F
41 0 .......F333335333F33333344F
42 0 ........F3333355F33333544F
43 0 ........F333333333333F44F
44 0 .........F333333335FF44F
45 0 ..........F4444444444FF
46 0 ...........FF444444FF
47 0 .............FFFFFF""",   # stand 2 (±40°), mond licht
'2M': """24 0 ........FF
25 0 .......F34F.FFFFFF
26 0 .......F345F444444FFF
27 0 ........F344444444445FF
28 0 .FFFF..F334444445555555FF
29 0 F3344FF334445555455333345F
30 0 F3454FF3555555555333333F4F
31 0 F4545F5555445553334FFFF344F
32 0 F4455F5455553333334FF1F344F
33 0 .FFFFF5444523333353FFFFF344F
34 0 .....F45452353555533FF33344F
35 0 .....F44523333333333333F344F
36 0 .....F442333F333333533F3344F
37 0 ......F533333FFFF3335533344F
38 0 ......F233333FF1F3333333344F
39 0 ......F333333FFFF3333333344F
40 0 .......F333333FF3333333344F
41 0 .......F333335333F33333544F
42 0 ........F3333355F33333F44F
43 0 ........F333333333333F44F
44 0 .........F33333335F4F44F
45 0 ..........F44444444F4FF
46 0 ...........FF444444FF
47 0 .............FFFFFF""",   # stand 2 (±40°), mond iets meer
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
    '1L': 'stand 1 (±15°), knotje, mond licht',
    '1M': 'stand 1 (±15°), knotje, mond iets meer',
    '2L': 'stand 2 (±40°), knotje, mond licht',
    '2M': 'stand 2 (±40°), knotje, mond iets meer',
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
