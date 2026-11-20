# vel12.py: vel.png = s11 | s10 | model (8x); daaronder per onderdeel de voorbeelden (8x) naast s11 en s10 (8x)
from PIL import Image, ImageDraw
P = '/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
nu = Image.open('hoatzin.png').convert('RGBA'); vor = Image.open('../s10/hoatzin.png').convert('RGBA')
mod = Image.open('../../MODEL.png').convert('RGB')
def wit(im):
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im); return bg.convert('RGB')
def ref(n, box): return wit(Image.open(P + n + '/anim_front.png').convert('RGBA').crop((0, 0, 64, 64)).crop(box))
DELEN = [  # titel, [(voorbeeld, uitsnede)], uitsnede hoatzin
    ('hoofd: Spearow-kuif (licht linksboven, donkere streng, bruine selout boven), Murkrow-haaksnavel, Mandibuzz-kale kop',
     [('spearow', (28, 10, 48, 32)), ('murkrow', (10, 30, 26, 44)), ('mandibuzz', (28, 2, 46, 20))], (0, 16, 20, 37)),
    ('poten: Dodrio/Doduo (selout lichtkant, zwart schaduwkant, klauw ingesloten), Skarmory, Unfezant',
     [('dodrio', (16, 44, 44, 64)), ('doduo', (24, 44, 52, 58)), ('skarmory', (14, 50, 34, 62)), ('unfezant', (22, 48, 44, 62))], (16, 48, 46, 62)),
    ('verre vleugel: Pidgeot/Fearow (lichte veertoppen, penlijn + lichte rand per veer), Honchkrow (donkere onderzone)',
     [('pidgeot', (0, 0, 22, 26)), ('fearow', (0, 0, 22, 26)), ('honchkrow', (0, 8, 22, 30))], (12, 6, 32, 30)),
]
S = 8
rijen = []
for titel, refs, box in DELEN:
    ims = [ref(n, b) for n, b in refs] + [wit(nu.crop(box)), wit(vor.crop(box))]
    rijen.append((titel, [i.resize((i.width * S, i.height * S), Image.NEAREST) for i in ims], len(refs)))
W = max(1580, max(sum(i.width + 16 for i in ims) + 30 for _, ims, _ in rijen))
H = 530 + sum(max(i.height for i in ims) + 40 for _, ims, _ in rijen)
V = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(V)
for i, im in enumerate((nu, vor)):
    V.paste(wit(im).resize((512, 512), Image.NEAREST), (i * 528, 0))
V.paste(mod.resize((512, 512), Image.LANCZOS), (1056, 0))
d.text((4, 514), 's12 | s10 | model', fill=(0, 0, 0))
y = 530
for titel, ims, nref in rijen:
    d.text((4, y + 2), titel + '   [voorbeelden | s12 | s10]', fill=(0, 0, 0))
    x = 4
    for k, im in enumerate(ims):
        if k == nref: x += 24
        V.paste(im, (x, y + 18)); x += im.width + 16
    y += max(i.height for i in ims) + 40
V.save('vel.png')
