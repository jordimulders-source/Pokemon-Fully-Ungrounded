"""vel.png: r7b, r8 (drie kapgrenzen) naast Taillow en Starly op 3x en 1x, licht en donker."""
from PIL import Image, ImageDraw, ImageFont
G = '../../../../../../graphics/pokemon/'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
def on(p, bg):
    im = Image.open(p); c = im.crop((0, 0, 64, 64)); a = c.convert('RGBA'); px = a.load(); idx = c.load()
    for y in range(64):
        for x in range(64):
            if idx[x, y] == 0: px[x, y] = (0, 0, 0, 0)
    b = Image.new('RGBA', (64, 64), bg + (255,)); b.alpha_composite(a); return b.convert('RGB')
refs = [('r7b', '../kleur_r7/kolibrie_pre_r7b.png'), ('r8', 'kolibrie_pre.png'), ('r8 hoger', 'kolibrie_pre_hoger.png'), ('r8 lager', 'kolibrie_pre_lager.png'),
        ('taillow', G + 'taillow/anim_front.png'), ('starly', G + 'starly/anim_front.png')]
v = Image.new('RGB', (6 * 200 + 20, 2 * 200 + 2 * 74 + 50), 'white'); d = ImageDraw.Draw(v)
for j, (n, p) in enumerate(refs):
    for i, bg in enumerate(((236, 236, 230), (44, 44, 52))):
        v.paste(on(p, bg).resize((192, 192), Image.NEAREST), (10 + j * 200, 24 + i * 200)); v.paste(on(p, bg), (10 + j * 200 + 64, 424 + i * 74))
    d.text((10 + j * 200, 4), n + ' (3x en 1x)', fill='black', font=F)
v.save('vel.png')
