"""vergelijk17.py <repo-root>: maakt ronde17/compare.png. Rij 1 (3x): ronde 16, ronde 17 f1/f2, variant_ogen,
Aipom en Sentret (staartreferentie), Poochyena en Umbreon (Dark-types). Rij 2: dezelfde op 1x, licht en donker.
Rij 3: koppen 6x (ronde 16, ronde 17, variant_ogen) met hulplijnen op de oogmiddens en de neus."""
import sys
from PIL import Image, ImageDraw

R = sys.argv[1]
O = R + '/docs/concept/sprites/olinguito/'
BG, DONKER = (152, 208, 160), (40, 40, 48)


def frames(p, n=2, bg=BG):
    im = Image.open(p)
    pal = im.getpalette()[:48]
    uit = []
    for i in range(n):
        c = im.crop((0, 64 * i, 64, 64 * i + 64))
        f = Image.new('RGB', (64, 64), bg)
        for y in range(64):
            for x in range(64):
                v = c.getpixel((x, y))
                if v:
                    f.putpixel((x, y), tuple(pal[v * 3:v * 3 + 3]))
        uit.append(f)
    return uit


def panelen(bg):
    r16 = frames(O + 'ronde16/anim_front.png', bg=bg)
    r17 = frames(O + 'ronde17/anim_front.png', bg=bg)
    var = frames(O + 'ronde17/variant_ogen/anim_front.png', bg=bg)
    g = lambda n: frames(R + '/graphics/pokemon/%s/anim_front.png' % n, 1, bg)[0]
    return [('ronde 16 f1', r16[0]), ('ronde 17 f1', r17[0]), ('ronde 17 f2', r17[1]), ('variant_ogen f1', var[0]),
            ('Aipom', g('aipom')), ('Sentret', g('sentret')), ('Poochyena', g('poochyena')), ('Umbreon', g('umbreon'))]


S, K = 3, 6
licht, donker = panelen(BG), panelen(DONKER)
koppen = [('ronde 16 kop', licht[0][1]), ('ronde 17 kop', licht[1][1]), ('variant_ogen kop', licht[3][1])]
KW, KH = 36 * K, 26 * K
W = Image.new('RGB', (len(licht) * (64 * S + 8) + 8, 64 * S + 64 + 44 + KH + 30), (255, 255, 255))
d = ImageDraw.Draw(W)
for i, ((t, p), (_, q)) in enumerate(zip(licht, donker)):
    x = 8 + i * (64 * S + 8)
    d.text((x, 4), t, fill=(0, 0, 0))
    W.paste(p.resize((64 * S, 64 * S), Image.NEAREST), (x, 18))
    W.paste(p, (x + 32, 64 * S + 28))
    W.paste(q, (x + 32 + 64 + 4, 64 * S + 28))
d.text((8, 64 * S + 28 + 66), '1x op licht en donker; koppen 6x: blauwe lijnen = oogmiddens, rode lijn = neusmidden', fill=(0, 0, 0))
y0 = 64 * S + 28 + 84
# hulplijnen: oogmiddens (verre, nabije) en neusmidden in doekcoordinaten
lijnen = {0: (17, 26, 10), 1: (17, 26, 21), 2: (15, 26, 21)}
for i, (t, p) in enumerate(koppen):
    x = 8 + i * (KW + 16)
    d.text((x, y0), t, fill=(0, 0, 0))
    W.paste(p.crop((6, 18, 42, 44)).resize((KW, KH), Image.NEAREST), (x, y0 + 14))
    for j, cx in enumerate(lijnen[i]):
        xx = x + (cx - 6) * K + K // 2
        d.line([(xx, y0 + 14), (xx, y0 + 14 + KH)], fill=(255, 40, 40) if j == 2 else (40, 80, 255))
W.save(O + 'ronde17/compare.png')
