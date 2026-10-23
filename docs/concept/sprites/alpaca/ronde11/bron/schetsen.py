"""schetsen.png: verkleinde foto (gespiegeld) + drie ruwe silhouetschetsen (PIL-vormen, alleen als schets).
Gebruik (vanuit de repo-root): python3 docs/concept/sprites/alpaca/ronde11/bron/schetsen.py"""
from PIL import Image, ImageDraw
R = 'docs/concept/sprites/alpaca/ronde11/'
foto = Image.open('docs/concept/ontwerp/alpaca/referentie_alpaca.webp').convert('RGB')
foto = foto.crop((300, 180, 1500, 1440)).transpose(Image.FLIP_LEFT_RIGHT).resize((61, 64), Image.LANCZOS)
f64 = Image.new('RGB', (64, 64), (255, 255, 255)); f64.paste(foto, (1, 0))
C = (90, 70, 60)


def schets(delen):
    im = Image.new('RGB', (64, 64), (255, 255, 255)); d = ImageDraw.Draw(im)
    for soort, a in delen:
        getattr(d, soort)(a, fill=C)
    return im


# A: cria rechtop, nek verticaal, kop met pompon, klein lijf, dunne poten, handschoenen voor
A = schets([('ellipse', (27, 31, 50, 45)), ('polygon', [(25, 22), (33, 22), (34, 36), (26, 37)]),
            ('ellipse', (17, 9, 34, 24)), ('ellipse', (13, 17, 23, 24)), ('ellipse', (21, 6, 33, 14)),
            ('polygon', [(22, 9), (21, 2), (25, 8)]), ('polygon', [(30, 8), (33, 1), (33, 9)]),
            ('rectangle', (28, 43, 30, 52)), ('rectangle', (33, 43, 35, 51)), ('rectangle', (43, 43, 45, 54)),
            ('rectangle', (47, 42, 49, 53)), ('ellipse', (24, 50, 33, 57)), ('ellipse', (31, 48, 38, 54)),
            ('ellipse', (49, 33, 53, 39))])
# B: grote babykop, korte nek (chibi)
B = schets([('ellipse', (24, 32, 50, 48)), ('ellipse', (12, 8, 36, 32)), ('ellipse', (8, 20, 20, 29)),
            ('polygon', [(16, 12), (14, 2), (20, 10)]), ('polygon', [(30, 10), (34, 1), (34, 12)]),
            ('rectangle', (28, 46, 31, 52)), ('rectangle', (44, 46, 47, 55)), ('ellipse', (24, 50, 34, 57))])
# C: nek schuin naar voren, kop vooruit (lama/paard)
C2 = schets([('ellipse', (28, 30, 52, 45)), ('polygon', [(20, 20), (28, 18), (35, 35), (28, 37)]),
             ('ellipse', (12, 10, 28, 24)), ('ellipse', (6, 16, 16, 23)),
             ('polygon', [(16, 11), (15, 3), (19, 10)]), ('polygon', [(23, 10), (26, 2), (26, 11)]),
             ('rectangle', (30, 43, 32, 53)), ('rectangle', (46, 43, 48, 54)), ('ellipse', (26, 50, 35, 57))])
items = [('foto', f64), ('A rechtop (gekozen)', A), ('B chibi', B), ('C nek vooruit', C2)]
out = Image.new('RGB', (len(items) * 202 + 10, 16 + 74 + 192 + 20), (255, 255, 255))
d = ImageDraw.Draw(out)
for i, (n, im) in enumerate(items):
    x = 10 + i * 202
    d.text((x, 2), n, fill=(0, 0, 0)); out.paste(im, (x, 18)); out.paste(im.resize((192, 192), Image.NEAREST), (x, 96))
out.save(R + 'schetsen.png')
