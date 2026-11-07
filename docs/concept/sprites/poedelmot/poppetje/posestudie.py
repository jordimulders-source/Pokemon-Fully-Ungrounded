"""Poedelmot posestudie: 16 echte Gen 3-sprites van vergelijkbaar bouwtype (vleugels / ronde wollige zitters), frame 1,
op 4x met een raster van 8 px. Per sprite: kop (incl. oren/sprieten) als aandeel van de hoogte zonder vleugels,
waar de vleugels staan in 3/4, en hoe de poten in perspectief staan (op het oog gemeten op het 8px-raster).
Draaien vanuit de repo-root: python3 docs/concept/sprites/poedelmot/poppetje/posestudie.py"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../../..'))
METING = [  # naam, kop/hoogte (zonder vleugels), vleugels, poten
    ('venomoth', '±35%', 'nabij paar groot rechts, ver paar klein links-achter', 'verborgen'),
    ('butterfree', '±40%', 'nabij rechts groot, ver links kleiner; voor+achter overlappen', 'klein, onder lijf'),
    ('dustox', '±55%', 'breed opzij, ver deel achter het lijf', 'kort, rijtje onder'),
    ('beautifly', '±35%', 'nabij rechts groot, ver links half achter kop', 'dun, weinig'),
    ('masquerain', '±40%', 'V omhoog, verre vleugel lager en kleiner', 'vier, gespreid'),
    ('ninjask', '±40%', 'nabij rechts boven, ver links lager', 'nabij lager'),
    ('volbeat', '±40%', 'klein, achter de rug, rechts', 'nabij lager/groter, ver hoger'),
    ('illumise', '±45%', 'klein, achter de rug', 'nabij lager, ver hoger'),
    ('swablu', '±60%', 'wolvleugels opzij, nabij groter', 'piepklein onder'),
    ('altaria', '±25%', 'wolk om het lijf', 'onder de wolk'),
    ('skitty', '±50%', '-', 'nabij voor, ver hoger achter'),
    ('wynaut', '±50%', '-', 'nabij lager'),
    ('spinda', '±55%', '-', 'nabij lager, ver half verborgen'),
    ('teddiursa', '±50%', '-', 'nabij voet lager en groter'),
    ('clefairy', '±55%', 'vleugeltjes achter de rug', 'nabij lager, ver hoger'),
    ('whismur', '±60%', '-', 'nabij lager, ver hoger'),
]
CONCL = [
    'Conclusies voor de poedelmot (ronde wollige zitter met vleugels):',
    '1. Kop (met sprieten) ±45% van de hoogte zonder vleugels: tussen de insecten (35-40%) en de ronde zitters (50-60%).',
    '2. Vleugels in 3/4 links-voor: nabij paar (dier-links) groot rechts achter het lijf, voor- en achtervleugel overlappen',
    '   tot één vorm; ver paar kleiner links, half achter kop/lijf; de verre punt eindigt naast de kop, niet erboven.',
    '3. Poten: nabije voet lager en groter, verre voet hoger en half verborgen; nooit op één lijn.',
    '4. Ronde zitters vullen ±70-80% van de kaderhoogte; de vleugels mogen het kader in de breedte vullen (Butterfree).',
]


def main():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
    S = 3; T = 64 * S; cw = T + 14; ch = T + 52
    W = 12 + 8 * cw; H = 40 + 2 * ch + 20 * len(CONCL) + 10
    im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 10), 'Poedelmot posestudie: Gen 3-sprites, frame 1, 3x (raster 8 px)', font=FB, fill=(30, 30, 30))
    for i, (n, kop, vl, pt) in enumerate(METING):
        p = Image.open(os.path.join(ROOT, 'graphics/pokemon', n, 'anim_front.png')); idx = np.array(p)[:64, :64]
        rgba = np.array(p.convert('RGBA'))[:64, :64]; rgba[idx == 0, 3] = 0
        t = Image.fromarray(rgba).resize((T, T), Image.NEAREST)
        bg = Image.new('RGB', (T, T), (232, 232, 238)); g = ImageDraw.Draw(bg)
        for k in range(0, T, 8 * S):
            g.line([(0, k), (T, k)], fill=(205, 205, 215)); g.line([(k, 0), (k, T)], fill=(205, 205, 215))
        bg.paste(t, (0, 0), t)
        r, c = divmod(i, 8); x = 12 + c * cw; y = 40 + r * ch
        im.paste(bg, (x, y))
        d.text((x, y + T + 2), f'{n}: kop {kop}', font=F, fill=(0, 0, 0))
        d.text((x, y + T + 15), 'vl: ' + vl[:34], font=F, fill=(70, 70, 70))
        d.text((x, y + T + 28), 'poten: ' + pt, font=F, fill=(70, 70, 70))
    y = 40 + 2 * ch + 4
    for l in CONCL:
        d.text((12, y), l, font=F if not l.startswith('Concl') else FB, fill=(0, 0, 0)); y += 20
    im.save(os.path.join(HERE, 'posestudie.png'))


if __name__ == '__main__':
    main()
