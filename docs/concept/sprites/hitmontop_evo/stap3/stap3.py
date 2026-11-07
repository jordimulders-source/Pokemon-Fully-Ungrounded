"""Stap 3 (Jordi, 6 nov): op het D14-skelet van stap 2 (benen 24, romp 20, kop 14) bestaande sprite-onderdelen plakken.
Kop = Hitmontop, armen = Hitmonchan (tot de pols), benen = Hitmonlee (tot de enkel), romp = Hitmonchan of Tyrogue.
Handen en voeten = die van stap 2 (goedgekeurd), ongewijzigd. Bewust knip- en plakwerk; draaien met nearest-neighbour, niet schalen.
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/stap3/stap3.py"""
import os, math
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
S2 = os.path.join(HERE, '../stap2/stap2.py')
_src = open(S2).read().replace('\nmain()\n', '\n')          # stap2 importeren zonder main() te draaien
s2 = {'__file__': os.path.abspath(S2)}; exec(compile(_src, 'stap2.py', 'exec'), s2)
laad, plak = s2['laad'], s2['plak']
Q0, R0 = s2['OPTIES']['D14: benen 24, romp 20, kop 14']
Q = s2['plaats'](Q0, R0)

TOP, LEE = s2['TOP'], s2['LEE']
CHAN, TYRO = laad('hitmonchan'), laad('tyrogue')


def masker(im, keep):
    """keep(x, y, px) -> bool, coördinaten in de uitsnede."""
    im = im.copy(); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            if px[x, y][3] and not keep(x, y, px[x, y]):
                px[x, y] = (0, 0, 0, 0)
    return im


def stuk(bron, box, a, b, keep=None):
    """uitsnede + as (a -> b) in spritecoördinaten; as wordt omgerekend naar de uitsnede."""
    im = bron.crop(box)
    if keep: im = masker(im, keep)
    return im, (a[0] - box[0], a[1] - box[1]), (b[0] - box[0], b[1] - box[1])


rood = lambda x, y, p: not (p[0] > 150 and p[1] < 130)      # bokshandschoen (rood/oranje) weg
# --- ARM: Hitmonchans linkerarm (schouder -> elleboog), zonder handschoen
ARM = stuk(CHAN, (22, 20, 30, 35), (26, 20), (25, 34), rood)
ARM_BOVEN = stuk(CHAN, (22, 20, 30, 28), (26, 20), (26, 27), rood)      # schouder + bovenarm
ARM_ONDER = stuk(CHAN, (22, 25, 30, 35), (26, 25), (25, 34), rood)      # onderarm, ronde elleboog onderaan
# --- BEEN: Hitmonlee's rechterbeen (windsels), dij en scheen apart
DIJ = stuk(LEE, (36, 36, 45, 45), (40, 36), (39, 44))
SCHEEN = stuk(LEE, (32, 44, 43, 54), (39, 44), (37, 53))
# --- ROMP
ROMP_CHAN = stuk(CHAN, (24, 24, 46, 43), (35, 24), (35, 42),
                 lambda x, y, p: y + 24 >= 34 or 29 <= x + 24 <= 40)    # armen naast de borst weg
ROMP_TYRO = stuk(TYRO, (26, 30, 41, 46), (32, 30), (33, 45),
                 lambda x, y, p: y + 30 >= 38 or 27 <= x + 26 <= 36)    # armen naast het shirt weg
# --- KOP (Hitmontop), ref = punt tussen de ogen, komt op het midden van de kopcirkel
KOP_HEEL = TOP.crop((16, 35, 53, 58)); KOP_HEEL_REF = (31 - 16, 44 - 35)
KOP_GEZICHT = TOP.crop((21, 35, 40, 58)); KOP_GEZICHT_REF = (31 - 21, 44 - 35)


def kop(soort, draai):
    im, ref = (KOP_GEZICHT, KOP_GEZICHT_REF) if soort == 'gezicht' else (KOP_HEEL, KOP_HEEL_REF)
    if soort == 'klein':   # GESCHAALD (50%, nearest): de 1:1-kop past niet op de kopcirkel van D14
        im = im.resize((im.width // 2, im.height // 2), Image.NEAREST); ref = (ref[0] // 2, ref[1] // 2)
    if draai:
        im = im.rotate(180); ref = (im.width - 1 - ref[0], im.height - 1 - ref[1])
    return im, ref


def langs(laag, part, A, B, spiegel=False, modus='beide'):
    """plak part (im, a, b) zo dat as a->b langs segment A->B ligt, 1:1, nearest-neighbour gedraaid.
    modus: 'begin' (a op A), 'eind' (b op B), 'midden', 'beide' (twee kopieën als het segment langer is)."""
    im, a, b = part
    if spiegel:
        im = im.transpose(Image.FLIP_LEFT_RIGHT); a = (im.width - 1 - a[0], a[1]); b = (im.width - 1 - b[0], b[1])
    ls = math.hypot(b[0] - a[0], b[1] - a[1]); ld = math.hypot(B[0] - A[0], B[1] - A[1])
    th = math.atan2(B[1] - A[1], B[0] - A[0]) - math.atan2(b[1] - a[1], b[0] - a[0])
    c, s = math.cos(-th), math.sin(-th)
    if modus == 'beide':
        ankers = [(b, B), (a, A)] if ld > ls + 1 else [(a, A)]
    elif modus == 'midden':
        ankers = [(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2))]
    else:
        ankers = [(a, A)] if modus == 'begin' else [(b, B)]
    src = im.load()
    for (sa, da) in ankers:
        lay = Image.new('RGBA', laag.size, (0, 0, 0, 0)); dp = lay.load()
        for y in range(64):
            for x in range(64):
                dx, dy = x - da[0], y - da[1]
                sx = round(sa[0] + c * dx - s * dy); sy = round(sa[1] + s * dx + c * dy)
                if 0 <= sx < im.width and 0 <= sy < im.height and src[sx, sy][3]:
                    dp[x, y] = src[sx, sy]
        laag.alpha_composite(lay)
    return ls, ld


def bouw(kopsoort, kopdraai, romp):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); log = []
    # 1 verre been (been 1, naar linksboven), gespiegeld zodat de schaduwkant buiten ligt
    log.append(('dij1', langs(im, DIJ, Q['heup'], Q['knie1'], spiegel=True)))
    log.append(('scheen1', langs(im, SCHEEN, Q['knie1'], Q['enkel1'], spiegel=True)))
    # 2 steunarm (schouder -> pols) en romp (schouder -> heup)
    log.append(('steunarm', langs(im, ARM, Q['schouder'], Q['pols'])))
    log.append(('romp', langs(im, ROMP_CHAN if romp == 'chan' else ROMP_TYRO, Q['schouder'], Q['heup'], modus='midden')))
    # 3 nabije been (been 2, naar rechtsboven)
    log.append(('dij2', langs(im, DIJ, Q['heup'], Q['knie2'])))
    log.append(('scheen2', langs(im, SCHEEN, Q['knie2'], Q['enkel2'])))
    # 4 koord: rode lijn
    ImageDraw.Draw(im).line([Q['heup'], Q['koord']], fill=(200, 60, 40, 255))
    # 5 vrije arm voor de romp: bovenarm schouder -> elleboog, onderarm met de elleboog op v_elleboog
    log.append(('v_bovenarm', langs(im, ARM_BOVEN, Q['v_schouder'], Q['v_elleboog'], modus='begin')))
    log.append(('v_onderarm', langs(im, ARM_ONDER, Q['v_pols'], Q['v_elleboog'])))
    # 6 kop voor de steunarmschouder
    k, ref = kop(kopsoort, kopdraai)
    im.alpha_composite(k, (int(round(Q['kop'][0] - ref[0])), int(round(Q['kop'][1] - ref[1]))))
    # 7 handen en voeten van stap 2, ongewijzigd
    plak(im, s2['HAND'], *Q['hand']); plak(im, s2['HAND'], *Q['v_hand'])
    ex, ey = Q['enkel1']
    im.alpha_composite(s2['VOET_L'], (int(round(ex - s2['VOET_L_ENKEL'][0])), int(round(ey - s2['VOET_L_ENKEL'][1]))))
    plak(im, s2['VOET'], *Q['voet2'])
    return im, log


OPTIES = {
    'A: kop a (hoorn omlaag), romp Hitmonchan': ('heel', False, 'chan'),
    'B: kop b (180 gr, hoorn omhoog), romp Hitmonchan': ('heel', True, 'chan'),
    'C: kop c (gezicht, hoorn omlaag), romp Tyrogue': ('gezicht', False, 'tyro'),
    'D: kop c (gezicht, 180 gr), romp Tyrogue': ('gezicht', True, 'tyro'),
    # getest en afgevallen: ('klein', False, 'tyro') = kop a op 50% geschaald -> onleesbare brij (zie NOTITIES)
}


def main():
    Z = 8; W = 64 * Z; tiles = []
    for naam, arg in OPTIES.items():
        im, log = bouw(*arg)
        im.save(os.path.join(HERE, 'optie_%s.png' % naam[0]))
        print(naam, 'bbox', im.getchannel('A').getbbox())
        for n, (ls, ld) in log: print('   %-11s stuk %.1f  segment %.1f' % (n, ls, ld))
        tiles.append((naam, im))
    vel = Image.new('RGB', (20 + (W + 20) * len(tiles), W + 200), (235, 235, 240)); d = ImageDraw.Draw(vel)
    for i, (naam, im) in enumerate(tiles):
        x = 20 + i * (W + 20)
        bg = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); bg.alpha_composite(im)
        g = bg.resize((W, W), Image.NEAREST).convert('RGB'); gd = ImageDraw.Draw(g)
        for a, b, t in s2['SEG']:      # dun skelet erover om de gewrichten te controleren
            gd.line([(Q[a][0] * Z + 4, Q[a][1] * Z + 4), (Q[b][0] * Z + 4, Q[b][1] * Z + 4)], fill=(0, 200, 0))
        for p in Q.values():
            gd.ellipse([p[0] * Z + 1, p[1] * Z + 1, p[0] * Z + 7, p[1] * Z + 7], outline=(0, 200, 0))
        vel.paste(g, (x, 30)); d.text((x, 10), naam + '   (groen = skelet D14)', fill=(0, 0, 0))
        y = W + 45
        for j, ref in enumerate((im, TOP, CHAN, LEE)):
            b2 = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); b2.alpha_composite(ref)
            vel.paste(b2.convert('RGB'), (x + j * 70, y))
        vel.paste(bg.resize((128, 128), Image.NEAREST).convert('RGB'), (x + 300, y))
        d.text((x, y + 70), '1x: optie | Hitmontop | Hitmonchan | Hitmonlee', fill=(0, 0, 0))
        d.text((x + 300, y + 132), '2x', fill=(0, 0, 0))
    vel.save(os.path.join(HERE, 'vel_stap3.png'))


main()
