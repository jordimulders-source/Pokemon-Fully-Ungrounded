"""Wasbeer silhouet ronde 9 (Jordi, 2 nov): "Het moet puur de klauw zijn in koevoet vorm, verder mag het vrij
vergelijkbaar met een klauwen van sneasel, weavile/sandslash etc. Lichaamspose kan wel redelijk in de buurt komen
van Gumshoos, al heeft onze pokemon net wat langere benen, wat meer de weavile lengte, al wil wel dat we echt die
typische crab eating raccoon hoofd aanhouden."
Opbouw (spritecoördinaten, kijkt naar links):
- romp + armen = de echte massa van Gumshoos (gelijk hoog als zijn lijf, zonder kop/staart/voeten), 3 px omhoog
  zodat de poten langer kunnen;
- poten op Weavile-lengte (heup tot voet ±19 px);
- kop = omtrek van Jordi's wasbeerillustratie (kop_illustratie.py), spritegroot (±35% van de hoogte);
- klauwen = gewone handklauwen (2 per hand, Sneasel-maat) in koevoetvorm: rechte steel, J-bocht aan de punt;
- staart = geringd, laag naar achteren (Gumshoos) met de haak omhoog; op de rug een omgekeerde kangoeroebuidel
  (Jordi: "wat echt onderdeel van zn lichaam is maar toch goed bij een dief past"), aansluitend op de rug.
Draaien: python3 silhouet_r9.py -> ronde9.txt, ronde9_1x.png, vel_ronde9.png"""
import os
import numpy as np
from PIL import Image, ImageDraw
import kop_illustratie as KI
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../../..'))
SS = 8
LIFT = 3


def sprite_mask(name):
    r = Image.open(os.path.join(ROOT, 'graphics/pokemon', name, 'anim_front.png')).convert('RGBA').crop((0, 0, 64, 64))
    a = np.array(r); bg = a[0, 0, :3].copy()
    return ~(a[..., :3] == bg).all(-1), Image.fromarray(np.where((~(a[..., :3] == bg).all(-1))[..., None], a, 0).astype(np.uint8))


# kop: illustratie (720x405) -> ±22 px breed, neus links op (5, 19)
KS = 0.058
def kp(p): return (5 + (p[0] - 192) * KS, 20 + (p[1] - 290) * KS)
NECK = [(22, 22, 5.2), (27, 27, 6.0)]
JAW = [(9, 21, 2.2), (14, 24, 3.2), (19, 25, 4.0)]                 # kin/keel dicht (geen open-mondgat)
EAR_BACK = (24.5, 6.5, 3.0, 3.8)                                    # nabije oor rond achter-boven op de kop (foto 11)

LEG_NEAR = [(21, 41, 5.0), (17, 49, 3.6), (20, 56, 2.6), (19, 59.5, 2.4)]
FOOT_NEAR = [(19, 60, 2.4), (14, 60.5, 2.0)]
LEG_FAR = [(32, 41, 4.6), (35, 49, 3.3), (34, 56, 2.4), (33, 59.5, 2.2)]
FOOT_FAR = [(33, 60, 2.2), (29, 60.5, 1.9)]
# koevoetklauwen: 2 per hand, rechte steel schuin omlaag-vooruit, punt buigt terug (J)
CLAWS_NEAR = [[(11, 39.5, 1.1), (8.5, 44, 1.0), (7.5, 46.5, 0.9), (8.8, 48, 0.8)],
              [(13, 40.5, 1.1), (11, 45, 1.0), (10.3, 47.5, 0.9), (11.6, 48.8, 0.8)]]
CLAWS_FAR = [[(25, 39, 1.0), (23.5, 43.5, 0.9), (23, 45.8, 0.8), (24.3, 46.8, 0.7)],
             [(27, 39.5, 1.0), (26, 44, 0.9), (25.6, 46.2, 0.8), (26.8, 47.2, 0.7)]]
TAIL = [(36, 41, 4.4), (43, 44, 4.2), (50, 45, 3.8), (56, 42, 3.4), (59, 36, 3.0), (57, 31, 2.6), (53, 30, 2.2), (52, 34, 1.9)]
PACK = (35.0, 28, 5.5, 8.0)          # buidel op de rug (omgekeerde kangoeroebuidel, deel van het lijf; Jordi): volgt de rug


def tube(d, pts):
    for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
        for i in range(13):
            t = i / 12
            x, y, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            d.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=255)


def build():
    G, _ = sprite_mask('gumshoos')
    body = np.zeros_like(G)
    yy, xx = np.mgrid[0:64, 0:64]
    keep = G & (yy >= 27) & (yy <= 47) & (xx <= 38)          # romp + armen, zonder kop, staart, voeten
    body[:64 - LIFT][keep[LIFT:]] = True
    im = Image.fromarray((body * 255).astype(np.uint8)).resize((64 * SS, 64 * SS), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for t in (NECK, TAIL, LEG_FAR, FOOT_FAR, LEG_NEAR, FOOT_NEAR) + tuple(CLAWS_FAR) + tuple(CLAWS_NEAR):
        tube(d, t)
    x, y, rx, ry = PACK
    d.ellipse([(x - rx) * SS, (y - ry) * SS, (x + rx) * SS, (y + ry) * SS], fill=255)
    d.polygon([(kp(p)[0] * SS, kp(p)[1] * SS) for p in KI.HEADI], fill=255)
    # verre oor: 70% en ronder (illustratie is spits)
    bx, by = KI.EARI_FAR[0][0] / 2 + KI.EARI_FAR[-1][0] / 2, KI.EARI_FAR[0][1] / 2 + KI.EARI_FAR[-1][1] / 2
    ear = [(bx + (x - bx) * 0.7, by + (y - by) * 0.7) for x, y in KI.EARI_FAR]
    d.polygon([(kp(p)[0] * SS, kp(p)[1] * SS) for p in ear], fill=255)
    ex, ey, erx, ery = EAR_BACK
    d.ellipse([(ex - erx) * SS, (ey - ery) * SS, (ex + erx) * SS, (ey + ery) * SS], fill=255)
    tube(d, JAW)
    a = np.array(im.resize((64, 64), Image.BOX)) >= 128
    # gaatjes binnen de omtrek dichten (alles wat niet vanaf de rand bereikbaar is)
    out = np.zeros_like(a); stack = [(0, 0)]
    while stack:
        y, x = stack.pop()
        if 0 <= y < 64 and 0 <= x < 64 and not out[y, x] and not a[y, x]:
            out[y, x] = True; stack += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
    return ~out


if __name__ == '__main__':
    a = build()
    open(os.path.join(HERE, 'ronde9.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in row) for row in a) + '\n')
    blk = Image.new('RGBA', (64, 64), (34, 30, 30, 255)); blk.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    blk.save(os.path.join(HERE, 'ronde9_1x.png'))
    G, gum = sprite_mask('gumshoos'); W_, wea = sprite_mask('weavile')
    S = 4
    ov = np.full((64, 64, 4), (236, 234, 228, 255), np.uint8)
    ov[G] = (240, 200, 60, 255); ov[a] = (34, 30, 30, 210); ov[a & G] = (120, 60, 140, 255)
    sheet = Image.new('RGB', (20 + (64 * S + 20) * 4 + 90, 64 * S + 60), (236, 234, 228))
    d = ImageDraw.Draw(sheet)
    x = 20
    for lab, img in (('Gumshoos (lijf)', gum), ('Weavile (beenlengte)', wea), ('silhouet ronde 9', blk),
                     ('over Gumshoos (geel = alleen Gumshoos)', Image.fromarray(ov))):
        big = img.resize((64 * S, 64 * S), Image.NEAREST)
        sheet.paste(big, (x, 40), big if big.mode == 'RGBA' else None); d.text((x, 20), lab, fill=(30, 30, 30)); x += 64 * S + 20
    sheet.paste(blk, (x, 40), blk); d.text((x, 110), f'1x ({int(a.sum())} px)', fill=(30, 30, 30))
    sheet.save(os.path.join(HERE, 'vel_ronde9.png'))
    print(int(a.sum()))
