"""Ronde 10: ruwe silhouetschetsen (alleen ter keuze; het eindresultaat is met de hand getekend).
Gebruik: python3 schetsen.py <uit.png> <referentiefoto>
Schetsen A/B/C naast de verkleinde referentiefoto, 64x64 op 4x."""
import sys
from PIL import Image, ImageDraw

ref = Image.open(sys.argv[2]).convert('RGB')
# foto bijsnijden rond de alpaca, spiegelen (sprite kijkt naar links) en verkleinen tot spritemaat
ref = ref.crop((300, 180, 1500, 1440)).transpose(Image.FLIP_LEFT_RIGHT).resize((61, 64), Image.LANCZOS)
r64 = Image.new('RGB', (64, 64), (255, 255, 255)); r64.paste(ref, (1, 0))


def schets(spec):
    im = Image.new('RGB', (64, 64), (255, 255, 255)); d = ImageDraw.Draw(im)
    for kind, box, col in spec:
        getattr(d, kind)(box, fill=col)
    return im


W, F, R = (225, 215, 190), (200, 140, 90), (210, 70, 60)
A = [  # rechtop, nek verticaal (zoals de foto)
    ('ellipse', (26, 30, 54, 46), W),
    ('rectangle', (44, 42, 47, 58), F), ('rectangle', (50, 41, 53, 56), F),
    ('polygon', [(17, 22), (29, 20), (32, 38), (20, 40)], W),
    ('ellipse', (12, 8, 31, 25), F),
    ('ellipse', (15, 3, 29, 13), W),
    ('polygon', [(14, 10), (16, 1), (19, 9)], F), ('polygon', [(25, 8), (29, 0), (30, 9)], F),
    ('ellipse', (7, 16, 17, 25), F),
    ('rectangle', (20, 40, 25, 50), F), ('ellipse', (16, 47, 28, 58), R),
    ('rectangle', (29, 42, 33, 49), F), ('ellipse', (27, 46, 37, 56), R),
]
B = [  # nek iets naar voren gebogen, lijf klein en rond
    ('ellipse', (28, 31, 52, 47), W),
    ('rectangle', (43, 43, 46, 58), F), ('rectangle', (48, 42, 51, 56), F),
    ('polygon', [(14, 24), (25, 20), (34, 36), (24, 42)], W),
    ('ellipse', (9, 9, 27, 26), F),
    ('ellipse', (12, 4, 26, 14), W),
    ('polygon', [(11, 12), (12, 2), (16, 10)], F), ('polygon', [(22, 9), (26, 1), (27, 10)], F),
    ('ellipse', (5, 17, 15, 26), F),
    ('rectangle', (22, 41, 27, 50), F), ('ellipse', (17, 47, 29, 58), R),
    ('rectangle', (31, 43, 35, 50), F), ('ellipse', (29, 47, 39, 56), R),
]
C = [  # chibi: grote kop, kortere nek
    ('ellipse', (24, 32, 54, 48), W),
    ('rectangle', (44, 44, 47, 58), F), ('rectangle', (50, 43, 53, 56), F),
    ('polygon', [(16, 26), (30, 24), (32, 38), (20, 40)], W),
    ('ellipse', (10, 8, 34, 30), F),
    ('ellipse', (14, 2, 32, 14), W),
    ('polygon', [(12, 10), (13, 0), (17, 9)], F), ('polygon', [(28, 8), (33, 0), (34, 10)], F),
    ('ellipse', (5, 18, 17, 29), F),
    ('rectangle', (20, 40, 25, 50), F), ('ellipse', (15, 47, 28, 58), R),
    ('rectangle', (30, 44, 34, 50), F), ('ellipse', (28, 47, 38, 56), R),
]
items = [('foto', r64), ('A rechtop', schets(A)), ('B nek naar voren', schets(B)), ('C chibi', schets(C))]
out = Image.new('RGB', (4 * 266 + 10, 64 * 4 + 24), (255, 255, 255))
dd = ImageDraw.Draw(out)
for i, (n, im) in enumerate(items):
    out.paste(im.resize((256, 256), Image.NEAREST), (10 + i * 266, 20))
    dd.text((10 + i * 266, 4), n, fill=(0, 0, 0))
out.save(sys.argv[1])
