import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import concepts as C

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../..')) + '/'
OUT = REPO + 'docs/concept/ontwerp/olinguito/'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
FS = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)

INFO = {
    'A': ('A  Klauwdief', [
        'Idee: een ronde teddybeer-olinguito met één uitvergroot lichaamsdeel: drie te lange, gebogen klauwen per poot.',
        'Pokémon: het silhouet is de opgeheven klauwhand (vgl. Makuhita\'s handen, Sneasels klauwen); babykop ±45% van de hoogte.',
        'Dark: de klauwen zelf, het masker als één vachtband over de ogen, sluwe halfdichte gouden ogen en een scheve grijns met hoektand.']),
    'B': ('B  Haakstaart', [
        'Idee: zit onschuldig rechtop met de klauwen gevouwen en kijkt opzij; de rechtopstaande coati-staart vormt achter zijn rug een haak.',
        'Pokémon: het silhouet is de vraagteken-staart (vgl. Sentret, Aipom); de lichaamstaal vertelt de dief, niet een rekwisiet.',
        'Dark: het verschil tussen voor- en achterkant (braaf vs. grijpend), het masker, de zijdelingse blik en de donkere weerhaak.']),
    'C': ('C  Borstelrug', [
        'Idee: sluipt laag op vier poten; een donkere getande manenvacht loopt van de kruin over de rug en groeit later uit tot kap en mantel.',
        'Pokémon: tweekleurige vacht met getande rand (vgl. Poochyena, Zigzagoon); het silhouet is de borstelige rug.',
        'Dark: masker, schedel en rug zijn één doorlopende donkere tekening; sluippose en smalle ogen.']),
}
EVO = {'A': ('fase 2: coati, klauw vooruit', 'fase 3: wasbeer, klauwen als dolken'),
       'B': ('fase 2: coati, herdersstaf-staart', 'fase 3: staart als boog over de schouder'),
       'C': ('fase 2: coati, manen tot de staart', 'fase 3: manen worden kap + mantel')}


def render(name):
    im, sil = getattr(C, 'concept_' + name if len(name) == 1 else 'evo_' + name)().finish()
    return im, sil


def concept_sheet(k):
    title, lines = INFO[k]
    W, H = 768, 256 + 40 + 24 + 18 * len(lines) + 10
    W = max(W, int(max(ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(ln, font=F) for ln in lines)) + 24)
    sheet = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(sheet)
    d.text((10, 8), title, font=FB, fill=(30, 30, 30))
    d.text((180, 12), 'fase 1 als modeltekening, fase 2 en 3 als ruwe silhouetschets', font=FS, fill=(90, 90, 90))
    im, _ = render(k)
    sheet.paste(im, (0, 36))
    e2, _ = render(k + '2')
    e3, _ = render(k + '3')
    sheet.paste(e2, (256, 36))
    sheet.paste(e3, (512, 36))
    d.text((10, 36 + 256), 'fase 1: olinguito', font=FS, fill=(90, 90, 90))
    d.text((266, 36 + 256 + 0), EVO[k][0], font=FS, fill=(90, 90, 90))
    d.text((522, 36 + 256), EVO[k][1], font=FS, fill=(90, 90, 90))
    y = 36 + 256 + 22
    for ln in lines:
        d.text((10, y), ln, font=F, fill=(30, 30, 30))
        y += 18
    sheet.save(OUT + 'concept_%s.png' % k)
    return im, sil_of(k)


def sil_of(k):
    return render(k)[1]


def gen3(species):
    p = REPO + 'graphics/pokemon/%s/anim_front_gba.png' % species
    im = Image.open(p)
    fr = im.crop((0, 0, 64, 64))
    idx = np.array(fr)
    rgba = fr.convert('RGBA')
    a = np.array(rgba)
    a[..., 3] = np.where(idx == 0, 0, 255)
    return Image.fromarray(a), idx != 0


def to_1x(im, sil, target_area=900):
    """Concept naar GBA-formaat: zo geschaald dat het silhouet ±900 px beslaat (Gen 3-starters: ±808)."""
    a = np.array(sil) > 127
    area256 = a.sum()
    s = (target_area / area256) ** 0.5
    size = max(8, int(round(256 * s)))
    small = im.resize((size, size), Image.BOX)
    ssil = sil.resize((size, size), Image.BOX)
    m = np.array(ssil) > 110
    canvas = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    sm = small.convert('RGBA')
    arr = np.array(sm)
    arr[..., 3] = np.where(m, 255, 0)
    sm = Image.fromarray(arr)
    ys, xs = np.nonzero(m)
    ox = (64 - (xs.max() + xs.min() + 1)) // 2
    oy = 60 - ys.max()
    canvas.paste(sm, (ox, oy), sm)
    mm = np.zeros((64, 64), bool)
    for y, x in zip(ys, xs):
        if 0 <= y + oy < 64 and 0 <= x + ox < 64:
            mm[y + oy, x + ox] = True
    return canvas, mm, s


def compare(concepts):
    real = ['totodile', 'cyndaquil', 'teddiursa', 'zigzagoon', 'sneasel', 'poochyena']
    names = ['concept A', 'concept B', 'concept C'] + [r.capitalize() + ' (G3)' for r in real]
    big, one, sils = [], [], []
    for k in 'ABC':
        im, sil = concepts[k]
        big.append(im.resize((192, 192), Image.LANCZOS).convert('RGBA'))
        c1, m1, s = to_1x(im, sil)
        one.append(c1)
        sils.append(m1)
    for r in real:
        im, m = gen3(r)
        big.append(im.resize((192, 192), Image.NEAREST))
        one.append(im)
        sils.append(m)
    n = len(names)
    TW = 200
    W, H = TW * n + 20, 506
    sheet = Image.new('RGB', (W, H), (236, 238, 242))
    d = ImageDraw.Draw(sheet)
    for i in range(n):
        x = 10 + i * TW
        d.text((x + 4, 8), names[i], font=F, fill=(30, 30, 30))
        sheet.paste(big[i], (x + 4, 30), big[i])
        y = 30 + 200 + 8
        if i == 0:
            d.text((2, y - 2), '', font=FS)
        # 1x kleur, 1x silhouet, 2x silhouet
        sheet.paste(one[i], (x + 4, y + 18), one[i])
        sil = Image.fromarray(np.where(sils[i], 0, 255).astype(np.uint8))
        sheet.paste(sil, (x + 74, y + 18))
        sheet.paste(sil.resize((128, 128), Image.NEAREST), (x + 4, y + 90))
        d.text((x + 4, y + 2), '1×        1× silhouet', font=FS, fill=(90, 90, 90))
        d.text((x + 4, y + 222), '%d px' % sils[i].sum(), font=FS, fill=(90, 90, 90))
    d.text((10, H - 24), 'Boven: concepten (modeltekening, verkleind) naast echte Gen 3-sprites (3×). Onder: 1× in kleur (concept verkleind tot ±900 px oppervlak), 1× silhouet en 2× silhouet.',
           font=FS, fill=(60, 60, 60))
    sheet.save(OUT + 'vergelijking.png')


if __name__ == '__main__':
    import os
    os.makedirs(OUT, exist_ok=True)
    res = {}
    for k in 'ABC':
        res[k] = concept_sheet(k)
    compare(res)
