"""Stap 4 hoofd ronde 4 (6 nov): nieuw hoofd op de vorm van stap 3b optie C, na Jordi's krabbel over ronde 3b.
Jordi: "De kleinere hoorn moet nog steeds door de haren heen zichtbaar blijven. Het enige wat deze nieuwe vorm heeft is de
haren die hij al had wat langer laten groeien en opgeknot, om een kleinere punt heen. Plus de hoofdvorm is anders. Daarnaast
mag het hele hoofd sowieso counterclockwise draaien [...] De ogen blijven zwarte rondjes met een wit puntje erin [...] De mond
is gewoon een streepje". Aanvulling: "het hoofd onderste boven is wel erg gek" -> het hoofd moet onmiskenbaar rechtop lezen.
Rasters met de hand als tekst (kleuren = Hitmontops normal.pal); de omtrek van kop/haarmassa/knot/hoorn is eerst als gids
gedraaid tegen de klok in (A/C 27 graden, B 42 graden t.o.v. rechtop; ronde 3b stond al ~12 graden), daarna alle lijnen,
ogen, mond en tinten per pixel geplaatst. Zie NOTITIES.md.
Alles buiten het hoofd komt ongewijzigd uit stap3b (bouw('chan', True, KOP_OW), dan zonder kop).
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/stap4_hoofd/ronde4/stap4_r4.py"""
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

# rijen: "y x0 pixels" ('.' = leeg), schermcoordinaten. Ogen = Hitmontops ronde oog (4x4, wit puntje) uit anim_front.png.
HOOFD = {
'A': """22 7 F
23 6 F2F
24 6 F23F
25 6 F34FFFF
26 5 F3FF3444FFFFFF
27 5 F3344544F33333FF
28 5 F344445F33354333FF
29 5 F444454F3333554333F
30 6 FF44FF3543333543FF
31 6 F3FF35435433335F3F
32 5 F35433543543333F33F
33 5 F3543354335433F3334F
34 5 F354333543354F33334F
35 4 F333543354333F333334F
36 4 F3335433FFFFF333FF34F
37 4 F33FFFFF3333333F1FF4F
38 4 FFF333333333333FFFF4F
39 6 F333333FF33333FF34F
40 6 F32233F1FF3333334F
41 6 F32333FFFF3333334F
42 7 F33333FF33333F3F
43 8 F3333333F33F33F
44 9 FF333333FF33F
45 11 FFF33333FF
46 14 FFFFF""",
'B': """24 4 F
25 3 F2F
26 3 F23FFFFF.FFFFFFF
27 4 FFF3344F3335543FF
28 5 F334454F3333554F
29 5 F344445F3333335FF
30 5 F444445F333333F33F
31 5 F444455F543333F333F
32 5 FF4455F335433F3333F
33 5 F3FFFF333354F33FF34F
34 4 FF33335433335F3F1FF4F
35 4 F35433354333F33FFFF4F
36 4 F335433543FF3333FF34F
37 4 F33543335F3333333334F
38 4 F33354FF333333333334F
39 4 F333FF3333FF33333334F
40 5 FFF33333F1FF333334F
41 6 F322333FFFF3333F3F
42 7 F233333FF3F33F33F
43 8 F333333333FF33F
44 9 F33333333333F
45 10 FFF3333FFFF
46 13 FFFF""",
'C': """24 9 F
25 8 F2F
26 8 F23FFFFFFFF
27 2 FFFF.F334F3333333FF
28 1 F3344F45554F33533333FF
29 1 F3444F3333353345533333F
30 1 F4445F333334533445533FF
31 1 F445F333533345333445F3F
32 2 F55F33345333453333F33F
33 3 FFF3533453334533F3334F
34 5 F345334533345F33334F
35 4 F333533345333F333334F
36 4 F3334533FFFFF333FF34F
37 4 F33FFFFF3333333F1FF4F
38 4 FFF333333333333FFFF4F
39 6 F333333FF33333FF34F
40 6 F32233F1FF3333334F
41 6 F32333FFFF3333334F
42 7 F33333FF33333F3F
43 8 F3333333F33F33F
44 9 FF333333FF33F
45 11 FFF33333FF
46 14 FFFFF""",
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
    'A': '27 gr tegen de klok in, knot op de kruin om de kleine punt',
    'B': '42 gr tegen de klok in, knot op de kruin om de kleine punt',
    'C': '27 gr tegen de klok in, punt door het haar, knot achterop (links)',
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
    ANIME = Image.open(os.path.join(HERE, '../../referenties/hitmontop_anime.webp')).convert('RGBA').crop((320, 40, 1000, 500))
    ANIME = ANIME.resize((ANIME.width * 300 // ANIME.height, 300))
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
        panelen = [(los, 'optie %s: hoofd los (8x)' % naam, (255, 255, 255)), (TOPKOP, 'Hitmontop front (8x)', (152, 208, 160))]
        H = max(p.height for p, t, b in panelen) * Z + 40; Wd = sum(p.width * Z + 20 for p, t, b in panelen) + 20
        v = Image.new('RGB', (Wd, H), (235, 235, 240)); dr = ImageDraw.Draw(v); x = 20
        for p, t, b in panelen:
            v.paste(wit(p, Z, b), (x, 30)); dr.text((x, 10), t, fill=(0, 0, 0)); x += p.width * Z + 20
        v2 = Image.new('RGB', (v.width + ANIME.width + 20, max(v.height, ANIME.height + 40)), (235, 235, 240))
        v2.paste(v, (0, 0)); v2.paste(ANIME.convert('RGB'), (v.width, 30))
        ImageDraw.Draw(v2).text((v.width, 10), 'anime (referentie)', fill=(0, 0, 0))
        v2.save(os.path.join(HERE, 'hoofd_%s.png' % naam))
        tegels.append((naam, oms, im))
    # vel: per optie 8x (uitsnede rond het hoofd), 1x en 2x van de hele sprite, naast Hitmontop
    CROP = (0, 14, 40, 50); cw, ch = (CROP[2] - CROP[0]) * Z, (CROP[3] - CROP[1]) * Z
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
        dr.text((x, yy + 146), 'controle: ' + rapport[k].split('|')[1].strip(), fill=(0, 0, 0))
    vel.save(os.path.join(HERE, 'vel_hoofd.png'))
    open(os.path.join(HERE, 'controle.txt'), 'w').write('\n'.join(rapport) + '\n')
    print('\n'.join(rapport))


main()
