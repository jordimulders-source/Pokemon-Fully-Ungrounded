"""Bouwt concept_A/B/C.png en vergelijking.png voor nachtaap en Cuyby.
Gebruik: python3 sheets.py <repo-root>"""
import sys, os, textwrap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdl import *
import nachtaap, cuyby

ROOT = sys.argv[1]
G = os.path.join(ROOT, 'graphics/pokemon/')
OUT = {'nachtaap': os.path.join(ROOT, 'docs/concept/ontwerp/nachtaap/'),
       'cuyby': os.path.join(ROOT, 'docs/concept/ontwerp/cuyby/')}

TXT = {
    'nachtaap': {
        'A': ("Nachtaap naar de natuur",
              "Kleuren van de echte nachtaap (Aotus): grijsbruin-violette vacht met een bleke gezichtsschijf, "
              "donkere rand en een korte wig tussen de wenkbrauwen; oranje keel en buik, zwarte staartpunt. "
              "Roze, egaal gloeiende ogen. Tarsierhouding: zit te gluren met de handen onder de kin; dunne "
              "ledematen, grote vinger- en teenkussens. Wangplukken geven de kop een eigen silhouet."),
        'B': ("Lavendel, maar dieper",
              "De goedgekeurde paarse richting, maar verzadigd violet met een donkerindigo rand om een bleke "
              "lila gezichtsschijf (licht gezicht in donkere vacht). Cyaan, egaal gloeiende ogen, rond oortje. "
              "Eén hand geheven bij de wang, de andere op de knie; tarsierhurk in plaats van sumohurk. "
              "Het dichtst bij ronde 3-5."),
        'C': ("Twee maansikkels",
              "Nachtblauwe vacht. De witte wenkbrauwvlekken van de echte nachtaap zijn twee maansikkels "
              "(maan in plaats van zon, uit de anatomie, geen sieraad); donker masker om de lila gloeiende "
              "ogen, bleke snuit. Hurkt als een tarsier met de handen bij de voeten; staart hoog opgekruld "
              "met een zilveren punt."),
    },
    'cuyby': {
        'A': ("Rozetkruin",
              "De Abessijnse cavia: zijn rozetten (vachtwervels) staan als puntige waaiers rechtop, op de kruin, "
              "de schouder en de heup, en breken het silhouet zoals Zigzagoons vacht. Agouti-bruin met "
              "creme punten. Evolutie: rechtop met een grotere kroon, dan een forse cavia met een krans van "
              "rozetten om de kop."),
        'B': ("Fluitsnuit",
              "Het 'wheeken': twee opgeblazen wangzakken met een ronde fluitmond ertussen, breder dan de kop. "
              "Rood (de 'red'-cavia) met creme wangen en buik. Normal met geluidsmoves. Evolutie: grotere "
              "wangzakken, dan snorharen als holle buizen van een siku (panfluit) die opzij uitwaaieren."),
        'C': ("Langhaarbol",
              "De Peruaanse langhaarcavia: het lijf is een bol vacht, de lokken vallen door hun gewicht "
              "omlaag. Driekleur als strakke grafische vlakken: wit, een oranje rug en zwart om het verre oog "
              "en oor. Evolutie: een bredere bol op vier stompe pootjes, dan een wandelende hooiberg "
              "(ichu-gras van de puna)."),
    },
}

TITLE = {'nachtaap': 'Nachtaap (Psychic-starter, fase 1)', 'cuyby': 'Cuyby (Normal, fase 1)'}
REFS = {'nachtaap': ['abra', 'aipom', 'ralts', 'natu', 'spoink'],
        'cuyby': ['sentret', 'zigzagoon', 'skitty', 'whismur', 'bidoof']}
FILL = {'nachtaap': 0.66, 'cuyby': 0.58}


def canvas_of(mod, k):
    cv = mod.draw(k)
    return cv


def frame0(name):
    p = G + name + '/anim_front_gba.png'
    lab = name.capitalize() + ' (G3)'
    if not os.path.exists(p):
        p = G + name + '/anim_front.png'
        lab = name.capitalize() + ' (DS)'
    im = Image.open(p).convert('RGBA')
    im = im.crop((0, 0, 64, 64))
    # achtergrond (index 0) transparant
    pal = Image.open(p)
    idx = np.array(pal)[:64, :64]
    a = np.array(im)
    a[idx == 0, 3] = 0
    return Image.fromarray(a), lab


def palette_of(cfg):
    keys = [k for k in ('fur', 'dark', 'face', 'cream', 'belly', 'accent', 'eye', 'pink', 'line') if k in cfg]
    seen = []
    for k in keys:
        if cfg[k] not in seen:
            seen.append(cfg[k])
    return seen


def concept_sheet(species, k, mod, cfgs):
    cv = canvas_of(mod, k)
    big = cv.image()
    W, H = 660, 440
    s = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(s)
    d.text((16, 10), '%s  -  concept %s: %s' % (TITLE[species], k, TXT[species][k][0]), fill=(30, 30, 30), font=font(15, True))
    s.paste(big, (16, 40))
    d.rectangle([15, 39, 16 + 256, 40 + 256], outline=(200, 200, 200))
    x0 = 290
    spr = sprite_scale(cv, 64, FILL[species])
    sil = silhouette(spr)
    d.text((x0, 40), 'sprite-formaat 1x / 2x', fill=(90, 90, 90), font=font(12))
    s.paste(spr, (x0, 58), spr)
    s2 = spr.resize((128, 128), Image.NEAREST)
    s.paste(s2, (x0 + 76, 58), s2)
    d.text((x0, 194), 'silhouet 1x / 2x', fill=(90, 90, 90), font=font(12))
    s.paste(sil, (x0, 212), sil)
    s3 = sil.resize((128, 128), Image.NEAREST)
    s.paste(s3, (x0 + 76, 212), s3)
    if species == 'cuyby':
        d.text((x0 + 214, 40), 'evolutie (schets)', fill=(90, 90, 90), font=font(12))
        for i, st in enumerate((2, 3)):
            e = mod.evo(k, st).image().resize((104 + i * 16, 104 + i * 16), Image.LANCZOS)
            s.paste(e, (x0 + 214, 58 + i * 116))
    # palet
    pal = palette_of(cfgs[k])
    px = 290 if species == 'cuyby' else 510
    py = 345 if species == 'cuyby' else 58
    d.text((16, 304), 'palet', fill=(90, 90, 90), font=font(12))
    for i, col in enumerate(pal):
        d.rectangle([56 + i * 20, 304, 72 + i * 20, 319], fill=hexc(col), outline=(60, 60, 60))
    y = 350
    for line in textwrap.wrap(TXT[species][k][1], 96):
        d.text((16, y), line, fill=(40, 40, 40), font=font(12))
        y += 16
    s.save(OUT[species] + 'concept_%s.png' % k)
    return spr


def comparison(species, mod, sprs):
    refs = [frame0(n) for n in REFS[species]]
    items = [(sprs[k], 'concept ' + k) for k in 'ABC'] + [(im, lab) for im, lab in refs]
    n = len(items)
    cw = 140
    W = cw * n + 20
    H = 470
    s = Image.new('RGB', (W, H), (236, 238, 242))
    d = ImageDraw.Draw(s)
    d.text((10, 8), '%s: concepten (verkleind tot spriteformaat) naast echte sprites, 2x en 1x; onder: silhouetten 1x'
           % TITLE[species], fill=(30, 30, 30), font=font(14, True))
    for i, (im, lab) in enumerate(items):
        x = 10 + i * cw
        d.text((x, 34), lab, fill=(40, 40, 40), font=font(12))
        s.paste(im.resize((128, 128), Image.NEAREST), (x, 52), im.resize((128, 128), Image.NEAREST))
        s.paste(im, (x + 32, 190), im)
        sil = silhouette(im)
        s.paste(sil, (x + 32, 290), sil)
        # opp. in pixels (1x)
        area = int((np.array(im)[:, :, 3] > 0).sum())
        d.text((x + 20, 262), 'opp. %d px' % area, fill=(90, 90, 90), font=font(11))
    # silhouetten op een rij, 1x, zonder labels (blinde rij)
    d.text((10, 368), 'blinde rij (1x, door elkaar):', fill=(60, 60, 60), font=font(12))
    order = [3, 0, 5, 1, 6, 4, 2, 7]
    for j, i in enumerate(order):
        im = items[i][0]
        s.paste(im, (10 + j * 70, 390), im)
    s.save(OUT[species] + 'vergelijking.png')


for species, mod in (('nachtaap', nachtaap), ('cuyby', cuyby)):
    os.makedirs(OUT[species], exist_ok=True)
    sprs = {k: concept_sheet(species, k, mod, mod.CFG) for k in 'ABC'}
    comparison(species, mod, sprs)
print('klaar')
