"""Stap 4 (6 nov): een goed hoofd op de vorm van stap 3b optie C.
Jordi: "we gaan er eerst een goed hoofd op zetten. Gebaseerd op Hitmontop, die maken we zodat die goed past in de hoek
en de pose die we van plan zijn. De stekel bovenop het hoofd van Hitmontop wordt iets minder aanwezig en de 'haren'
kammen we naar achteren in een klein staartje of knotje [...] voor de rest gaan we nog nergens aan zitten".
De hoofden zijn met de hand als tekstraster getekend (kleuren = Hitmontops normal.pal; zie NOTITIES.md).
Alles buiten het hoofd komt ongewijzigd uit stap3b (bouw('chan', True, KOP_OW), dan zonder kop).
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/stap4_hoofd/stap4.py"""
import os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../..')
S3B = os.path.join(HERE, '../stap3b/stap3b.py')
g = {'__file__': os.path.abspath(S3B)}
exec(compile(open(S3B).read().replace('\nmain()\n', '\n'), 'stap3b.py', 'exec'), g)
LEEG = (Image.new('RGBA', (64, 64), (0, 0, 0, 0)), (10, 10), (10, 20))
BASIS = g['bouw']('chan', True, LEEG)                     # stap 3b optie C zonder hoofd
OPTIE_C = Image.open(os.path.join(HERE, '../stap3b/optie_C.png')).convert('RGBA')

# Hitmontops palet (graphics/pokemon/hitmontop/normal.pal): 1 wit, 2/3/4 huid licht/midden/schaduw, 5 donkerbruin, F omlijning
PAL = {'1': (255, 255, 255), '2': (255, 222, 156), '3': (222, 189, 131), '4': (180, 139, 90), '5': (131, 90, 41), 'F': (16, 16, 16)}

# rijen: "y x0 pixels" ('.' = leeg). Met de hand getekend.
STAND = {
'1': """
22 9 ....F
23 9 ...F3F
24 9 ...F34FFFFF
25 9 ..F33454544F
26 9 .F3354544544FF
27 9 F3354445444544F
28 9 F35444454444544F
29 9 F444222333333344F
30 9 F4225333333333334F
31 9 F2233553333333334F
32 9 F23333335553FF334F
33 9 F2333333333F1FF34F
34 9 F333FF33333FFFFF4F
35 9 F33F1FF33333FF334F
36 9 .F3FFFF3333333334F
37 9 .F33FF33333333344F
38 9 ..F3333F33333344F
39 9 ..F55FF333333444F
40 9 ...F44433333344F
41 9 ....FF4444444FF
42 9 ......FFFFFFF
""",   # ±15 graden: meer naar de kijker
'2': """
23 8 ..F
24 8 .F3FF..FFF
25 8 ..F34FF334FF
26 8 ...F33534443FF
27 8 ...F3445422333FF
28 8 ..F3354422333333F
29 8 ..F35442333333334F
30 8 .F33542233333FF34F
31 8 .F4442233333F1FF44F
32 8 F44255533333FFFFF4F
33 8 F222333333333FF334F
34 8 F23333333333333344F
35 8 F333333FF333333344F
36 8 .F333F1FF33333344F
37 8 .F333FFFF3333334F
38 8 ..F333FF33F33344F
39 8 ..F33333FF33444F
40 8 ...FF35544444FF
41 8 .....FF4444FF
42 8 .......FFFF
""",   # ±40 graden: zoals de foto (as nek -> kruin van het skelet)
'3': """
24 6 ..........FFFF
25 6 .......FFF2223FF
26 6 ......F332223333FF
27 6 .....F335422333333F
28 6 .FFFF335443333FF33F
29 6 F334444423333F1FF33F
30 6 .FFF444423333FFFFF4F
31 6 ...F4544233333FF334F
32 6 ...F452223553333334F
33 6 ...F442553333333334F
34 6 ...F425333333333334F
35 6 ...F422333333333334F
36 6 ...F333333FF3333344F
37 6 ...F33333F1FF33F34F
38 6 ....F3333FFFF3F444F
39 6 ....F33333FF33F44F
40 6 .....FF333335544F
41 6 .......FF4444FFF
42 6 .........FFFF
""",   # ±65 graden: kruin naar links, kin bij de nek
}
# knotje achterop (achter het hoofd getekend: alleen de rand steekt uit); anker = linksboven, per stand
KNOT = [".FF.", "F34F", "F45F", ".FF."]
KNOT_ANKER = {'1': (7, 25), '2': (5, 30), '3': (6, 34)}
# uitdrukking e2: het donkerbruine staartje van Hitmontops mond weg (kortere, rechte mondstreep: rustiger/ouder)
E2 = {'1': {(12, 39): '4', (13, 39): '3'}, '2': {(14, 40): '4', (15, 40): '4'}, '3': {(18, 40): '3', (19, 40): '3'}}


def lees(txt):
    d = {}
    for regel in txt.strip().split('\n'):
        y, x0, r = regel.split(' ', 2)
        for i, c in enumerate(r):
            if c in PAL:
                d[(int(x0) + i, int(y))] = c
    return d


def hoofd(stand, knot=False, uitdr='e1'):
    """dict (x,y) -> paletletter van het hele hoofd (incl. knotje)."""
    d = {}
    if knot:
        ax, ay = KNOT_ANKER[stand]
        for j, r in enumerate(KNOT):
            for i, c in enumerate(r):
                if c in PAL:
                    d[(ax + i, ay + j)] = c
    d.update(lees(STAND[stand]))                          # hoofd over het knotje
    if uitdr == 'e2':
        d.update(E2[stand])
    return d


def plak(d):
    im = BASIS.copy()
    for p, c in d.items():
        im.putpixel(p, PAL[c] + (255,))
    return im


OPTIES = {}
for s, hoek in (('1', '15'), ('2', '40'), ('3', '65')):
    OPTIES[s + 'a'] = (s, False, 'e1', 'stand %s (±%s°), geen knotje, e1 = Hitmontop' % (s, hoek))
    OPTIES[s + 'b'] = (s, True, 'e1', 'stand %s (±%s°), knotje net zichtbaar, e1' % (s, hoek))
    OPTIES[s + 'c'] = (s, False, 'e2', 'stand %s (±%s°), geen knotje, e2 rustiger mond' % (s, hoek))


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
    for naam, (s, knot, e, oms) in OPTIES.items():
        d = hoofd(s, knot, e); im = plak(d)
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
    CROP = (2, 14, 42, 50); cw, ch = (CROP[2] - CROP[0]) * Z, (CROP[3] - CROP[1]) * Z
    kol = 3; TW = max(cw, 420) + 20; TH = ch + 180
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
