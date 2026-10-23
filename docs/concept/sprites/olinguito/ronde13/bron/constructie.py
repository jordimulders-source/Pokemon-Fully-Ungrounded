"""Constructieschets ronde 13 (hulplaag, alleen schets): romp als boon schuin de diepte in."""
import sys
from PIL import Image, ImageDraw
D = sys.argv[1]  # olinguito-map
S = 8
r12 = Image.open(D + '/ronde12/anim_front.png').crop((0, 0, 64, 64))
ip = r12.load()
base = r12.convert('RGB').load()
im = Image.new('RGB', (64 * S, 64 * S), (240, 240, 232))
px = im.load()
# ronde 12 dof als ondergrond
for y in range(64):
    for x in range(64):
        if ip[x, y]:
            r, g, b = base[x, y]
            c = ((r + 480) // 3, (g + 480) // 3, (b + 480) // 3)
            for j in range(S):
                for i in range(S):
                    px[x * S + i, y * S + j] = c
d = ImageDraw.Draw(im, 'RGBA')
P = lambda x, y: (x * S, y * S)
def ell(cx, cy, rx, ry, col):
    d.ellipse([P(cx - rx, cy - ry), P(cx + rx, cy + ry)], outline=col, width=3)
# romp: borst (dichtbij, groot) en heup (ver, kleiner, hoger)
ell(31, 43.5, 8, 6, (200, 40, 40, 255))
ell(46.5, 39, 7.5, 6.5, (40, 80, 200, 255))
# ruggengraat / middellijn van de boon (de diepte in)
d.line([P(24, 46), P(31, 43.5), P(46.5, 39), P(53, 35)], fill=(120, 0, 160, 255), width=3)
# dwarsas (schouder- en heupas): dichtbij = rechtsonder, ver = linksboven
for (a, b) in (((27.5, 45), (24, 41.5)), ((47.5, 42), (42, 38))):
    d.line([P(*a), P(*b)], fill=(0, 140, 0, 255), width=3)
# poten: dichtbij dik groen, ver dun oranje
legs = [
    ((27.5, 45), (24, 48), (20, 49), (0, 140, 0)),       # dichtbije voorpoot (klauwarm)
    ((24, 41.5), (19, 43), (15, 45), (230, 120, 0)),     # verre voorpoot (opgetrokken)
    ((47.5, 42), (44, 48), (48, 52), (0, 140, 0)),       # dichtbije achterpoot: knie naar voren, hiel naar achteren
    ((42, 38), (38, 46), (40, 50), (230, 120, 0)),       # verre achterpoot, links-hoger, achter het lijf
]
for a, b, c, col in legs:
    d.line([P(*a), P(*b), P(*c)], fill=col + (255,), width=4)
    for q in (a, b, c):
        d.ellipse([P(q[0] - .4, q[1] - .4), P(q[0] + .4, q[1] + .4)], fill=col + (255,))
# grondvlak: voetpunten (dichtbij laag, ver hoger)
for (x, y, col) in ((19, 55, (0, 140, 0)), (15, 47, (230, 120, 0)), (44, 55, (0, 140, 0)), (37, 52, (230, 120, 0))):
    d.rectangle([P(x - 2, y), P(x + 3, y + .5)], fill=col + (255,))
d.line([P(14, 55.5), P(50, 52.5)], fill=(90, 90, 90, 160), width=2)
# staartaanzet aan de heup
d.line([P(52, 37), P(56, 22)], fill=(150, 90, 0, 255), width=3)
d.text((6, 6), 'rood: borst (dichtbij)  blauw: heup (ver, hoger)  paars: middellijn de diepte in', fill=(0, 0, 0))
d.text((6, 20), 'groen: dichtbije poten + schouder/heupas  oranje: verre poten (links-hoger, achter)', fill=(0, 0, 0))
im.save(D + '/ronde13/constructie.png')
