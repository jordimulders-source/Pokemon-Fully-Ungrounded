"""Stap 3 opnieuw (Jordi, 6 nov: "je kan het hoofd niet zomaar op of neer zetten, dat moet ook meedraaien zoals bij de
andere assets. Daarnaast heb je ook de handen meegeknipt. Prutswerk. [...] De armen heb je ook niet netjes geknipt.
De benen kan ik in elk geval zien dat dat klopt").
- Elk onderdeel netjes geknipt: alleen de eigen kleuren binnen een eigen vak, omlijning (zwart) alleen waar die aan
  het onderdeel grenst, en op de knipnaad een nieuwe omlijning. Losse onderdelen apart te zien op vel_delen.png.
- Alles draait mee langs zijn as (ook de kop: as nek -> kruin/hoorn langs het skelet nek -> kop).
- Een onderdeel dat korter is dan zijn segment wordt langs de as gerekt (nearest), niet twee keer geplakt.
- Benen = Hitmonlee (zoals stap 3, Jordi akkoord). Handen en voeten = stap 2, ongewijzigd.
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/stap3b/stap3b.py"""
import os, math
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
S2 = os.path.join(HERE, '../stap2/stap2.py')
_src = open(S2).read().replace('\nmain()\n', '\n')
s2 = {'__file__': os.path.abspath(S2)}; exec(compile(_src, 'stap2.py', 'exec'), s2)
laad, plak = s2['laad'], s2['plak']
Q0, R0 = s2['OPTIES']['D14: benen 24, romp 20, kop 14']
Q = s2['plaats'](Q0, R0)
TOP, LEE, CHAN, TYRO = s2['TOP'], s2['LEE'], laad('hitmonchan'), laad('tyrogue')
ZWART = (16, 16, 16, 255)


def knip(bron, box, keep, a, b, zwart_mee=False):
    """onderdeel uit bron: pixels in box (x0,y0,x1,y1 incl.) waarvoor keep(x,y,kleur); zwarte pixels blijven alleen als
    ze aan een gehouden pixel grenzen. Op de knipnaad (gehouden pixel naast een weggeknipte niet-lege pixel) komt zwart."""
    x0, y0, x1, y1 = box
    src = bron.load()
    hou = set()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            p = src[x, y]
            if p[3] and (zwart_mee or p[:3] != ZWART[:3]) and keep(x, y, p):
                hou.add((x, y))
    zw = set()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if src[x, y][:3] == ZWART[:3] and src[x, y][3] and any((x + dx, y + dy) in hou for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                zw.add((x, y))
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = im.load()
    for (x, y) in hou:
        d[x, y] = src[x, y]
    for (x, y) in zw:
        d[x, y] = ZWART
    # knipnaad: buurpixel was deel van de sprite maar is weggeknipt -> deze rand zwart
    for (x, y) in hou:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if 0 <= n[0] < 64 and 0 <= n[1] < 64 and src[n][3] and n not in hou and n not in zw:
                d[x, y] = ZWART
                break
    return im, a, b


KLEUR = lambda *cs: (lambda x, y, p: p[:3] in cs)
NIET = lambda *cs: (lambda x, y, p: p[:3] not in cs)
EN = lambda *fs: (lambda x, y, p: all(f(x, y, p) for f in fs))

# --- KOP: Hitmontop, zonder zijn handen, polsbanden, armstokjes en blauwe lijf
blauw = lambda x, y, p: p[2] > p[0] + 40
KOP = knip(TOP, (12, 34, 54, 58),
           lambda x, y, p: not blauw(x, y, p) and not (x <= 17 and y <= 36) and (x - 47) ** 2 + (y - 38) ** 2 > 15
           and not (43 <= x <= 48 and y <= 35),
           (32, 35), (31, 57), zwart_mee=True)                      # as: nek (bovenkant, waar het lijf zat) -> hoorntop
# --- KOP klein: Hitmontops overworld-sprite (frame 1, 32x32): dezelfde kop met haar en hoorn, 18 px breed
_ow = Image.open(os.path.join(HERE, '../../../../../graphics/pokemon/hitmontop/overworld.png')).convert('RGBA').crop((0, 0, 32, 32))
_bg = _ow.getpixel((0, 0)); _ow.putdata([(0, 0, 0, 0) if q == _bg else q for q in _ow.get_flattened_data()])
OW = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); OW.alpha_composite(_ow, (16, 16))     # in een 64-vak, verschuiving 16
KOP_OW = knip(OW, (16 + 6, 16 + 8, 16 + 25, 16 + 24),
              lambda x, y, p: not blauw(x, y, p) and not (y >= 16 + 22 and (x <= 16 + 10 or x >= 16 + 20)),
              (16 + 15, 16 + 24), (16 + 15, 16 + 9), zwart_mee=True)   # as: nek (onder de mond) -> hoorntop
# --- ARM: Hitmonchans linkerarm, schouder -> pols, zonder handschoen, lijf en gezicht
HANDSCHOEN = {(139, 32, 0), (189, 49, 74), (230, 98, 74), (255, 148, 90), (255, 246, 255)}
PAARS_C = {(98, 74, 115), (164, 156, 164), (197, 180, 197)}
# Hitmonchans eigen arm is sterk verkort (schouderstuk + onderarm achter de handschoen) en leest los niet als arm
ARM_CHAN = knip(CHAN, (19, 20, 29, 35), lambda x, y, p: p[:3] not in HANDSCHOEN and p[:3] not in PAARS_C and not (x >= 27 and y <= 21),
                (26, 21), (22, 33))
# daarom: Hitmonchans (bruine) linkerbeen tot boven de laars als arm
BRUIN_C = {(90, 65, 16), (164, 139, 115), (205, 180, 123), (238, 213, 156)}
ARM = knip(CHAN, (19, 41, 28, 53), lambda x, y, p: p[:3] in BRUIN_C, (25, 42), (22, 53))
# --- ROMP Hitmonchan: paarse tuniek, zonder armen
ROMP_CHAN = knip(CHAN, (24, 26, 46, 44), lambda x, y, p: p[:3] in PAARS_C, (35, 26), (35, 44))
# --- ROMP Tyrogue: wit shirt + bruine broek, zonder paarse huid
PAARS_T = {(112, 64, 96), (152, 104, 152), (192, 152, 184), (232, 192, 248)}
ROMP_TYRO = knip(TYRO, (24, 33, 41, 43), lambda x, y, p: p[:3] not in PAARS_T, (33, 33), (33, 43))
# --- BENEN Hitmonlee (zoals stap 3, akkoord): dij en scheen
LEE_HUID = None
DIJ = knip(LEE, (36, 36, 44, 44), lambda x, y, p: True, (40, 36), (39, 44))
SCHEEN = knip(LEE, (32, 44, 42, 53), lambda x, y, p: True, (39, 44), (37, 53))
DELEN = dict(kop=KOP, kop_overworld=KOP_OW, arm_chan_eigen=ARM_CHAN, arm=ARM, romp_chan=ROMP_CHAN, romp_tyro=ROMP_TYRO, dij=DIJ, scheen=SCHEEN)


def langs(laag, part, A, B, spiegel=False, rek=True):
    """as a->b van het onderdeel langs segment A->B; rek=True: langs de as gerekt tot de segmentlengte (nearest)."""
    im, a, b = part
    if spiegel:
        im = im.transpose(Image.FLIP_LEFT_RIGHT); a = (63 - a[0], a[1]); b = (63 - b[0], b[1])
    ls = math.hypot(b[0] - a[0], b[1] - a[1]); ld = math.hypot(B[0] - A[0], B[1] - A[1])
    f = ls / ld if rek else 1.0
    us = ((b[0] - a[0]) / ls, (b[1] - a[1]) / ls); vs = (-us[1], us[0])
    ud = ((B[0] - A[0]) / ld, (B[1] - A[1]) / ld); vd = (-ud[1], ud[0])
    src = im.load(); lay = Image.new('RGBA', laag.size, (0, 0, 0, 0)); dp = lay.load()
    for y in range(64):
        for x in range(64):
            dx, dy = x - A[0], y - A[1]
            u = (dx * ud[0] + dy * ud[1]) * f; v = dx * vd[0] + dy * vd[1]
            if not (-1.5 <= u <= ls + 1.5):          # niets voorbij de uiteinden van de as (geen slierten)
                continue
            sx = round(a[0] + u * us[0] + v * vs[0]); sy = round(a[1] + u * us[1] + v * vs[1])
            if 0 <= sx < 64 and 0 <= sy < 64 and src[sx, sy][3]:
                dp[x, y] = src[sx, sy]
    laag.alpha_composite(lay)


def schoon(im):
    """pixels met hooguit 1 buur (draairesten, slierten) weghalen; 2 rondes."""
    for _ in range(2):
        a = im.getchannel('A').load(); px = im.load()
        weg = [(x, y) for y in range(64) for x in range(64) if a[x, y] and
               sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < 64 and 0 <= y + dy < 64 and a[x + dx, y + dy]) <= 1]
        for q in weg:
            px[q] = (0, 0, 0, 0)


def bouw(romp, kop_voor=True, kop=None):
    KOPD = kop or KOP
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    langs(im, DIJ, Q['heup'], Q['knie1'], spiegel=True)            # verre been achter
    langs(im, SCHEEN, Q['knie1'], Q['enkel1'], spiegel=True)
    langs(im, ARM, Q['schouder'], Q['pols'])                        # steunarm
    if not kop_voor:
        langs(im, KOPD, Q['nek'], Q['kop'], rek=False)
    langs(im, ROMP_CHAN if romp == 'chan' else ROMP_TYRO, Q['schouder'], Q['heup'])
    langs(im, DIJ, Q['heup'], Q['knie2'])                           # nabije been
    langs(im, SCHEEN, Q['knie2'], Q['enkel2'])
    ImageDraw.Draw(im).line([Q['heup'], Q['koord']], fill=(200, 60, 40, 255))
    langs(im, ARM, Q['v_schouder'], Q['v_elleboog'])                 # vrije arm: boven- en onderarm
    langs(im, ARM, Q['v_elleboog'], Q['v_pols'])
    if kop_voor:
        langs(im, KOPD, Q['nek'], Q['kop'], rek=False)                # kop draait mee langs nek -> kop
    schoon(im)                                                       # draairesten (losse/uitstekende pixels) weg
    plak(im, s2['HAND'], *Q['hand']); plak(im, s2['HAND'], *Q['v_hand'])
    ex, ey = Q['enkel1']
    im.alpha_composite(s2['VOET_L'], (int(round(ex - s2['VOET_L_ENKEL'][0])), int(round(ey - s2['VOET_L_ENKEL'][1]))))
    plak(im, s2['VOET'], *Q['voet2'])
    return im


OPTIES = {
    'A: romp Hitmonchan, kop frontsprite (37 px)': ('chan', True),
    'B: romp Tyrogue, kop frontsprite (37 px)': ('tyro', True),
    'C: romp Hitmonchan, kop overworld (18 px)': ('chan', True, KOP_OW),
    'D: romp Tyrogue, kop overworld (18 px)': ('tyro', True, KOP_OW),
}


def wit(im, z):
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    return bg.resize((im.width * z, im.height * z), Image.NEAREST).convert('RGB')


def main():
    # vel met de losse geknipte delen (8x), om het knippen te controleren
    Z = 8; xs = 10; stukken = []
    for n, (im, a, b) in DELEN.items():
        bb = im.getchannel('A').getbbox(); stukken.append((n, im.crop(bb)))
    dv = Image.new('RGB', (sum(c.width * Z + 20 for n, c in stukken) + 10, 26 * Z + 40), (235, 235, 240)); dd = ImageDraw.Draw(dv)
    for n, c in stukken:
        dv.paste(wit(c, Z), (xs, 25)); dd.text((xs, 8), n, fill=(0, 0, 0)); xs += c.width * Z + 20
    dv.save(os.path.join(HERE, 'vel_delen.png'))
    Z = 8; W = 64 * Z; tiles = []
    for naam, arg in OPTIES.items():
        im = bouw(*arg); im.save(os.path.join(HERE, 'optie_%s.png' % naam[0])); tiles.append((naam, im))
        print(naam, im.getchannel('A').getbbox())
    vel = Image.new('RGB', (20 + (W + 20) * len(tiles), W + 200), (235, 235, 240)); d = ImageDraw.Draw(vel)
    for i, (naam, im) in enumerate(tiles):
        x = 20 + i * (W + 20)
        vel.paste(wit(im, Z), (x, 30)); d.text((x, 10), naam, fill=(0, 0, 0))
        y = W + 45
        for j, ref in enumerate((im, TOP, CHAN, TYRO, LEE)):
            vel.paste(wit(ref, 1), (x + j * 70, y))
        vel.paste(wit(im, 2), (x + 370, y))
        d.text((x, y + 70), '1x: optie | Hitmontop | Hitmonchan | Tyrogue | Hitmonlee', fill=(0, 0, 0))
    vel.save(os.path.join(HERE, 'vel_stap3b.png'))


main()
