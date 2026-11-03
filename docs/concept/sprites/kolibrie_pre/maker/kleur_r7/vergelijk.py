"""vergelijk_8x.png: koppen r6 | r7a | r7b | Taillow | Pidgey op 8x, en een rij kandidaat-ogen (8x) met de keuze.
vel.png: r6, r7a, r7b naast Taillow, Pidgey, Starly op 3x en 1x, licht en donker."""
from PIL import Image, ImageDraw, ImageFont
G = '../../../../../../graphics/pokemon/'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
L, D = (236, 236, 230), (44, 44, 52)
def on(p, bg=L):
    im = Image.open(p); c = im.crop((0, 0, 64, 64)); a = c.convert('RGBA'); px = a.load(); idx = c.load()
    for y in range(64):
        for x in range(64):
            if idx[x, y] == 0: px[x, y] = (0, 0, 0, 0)
    b = Image.new('RGBA', (64, 64), bg + (255,)); b.alpha_composite(a); return b.convert('RGB')
heads = [('r6', '../kleur_r6/kolibrie_pre.png', (7, 7, 39, 29)), ('r7a', 'kolibrie_pre_r7a.png', (7, 7, 39, 29)),
         ('r7b', 'kolibrie_pre_r7b.png', (7, 7, 39, 29)), ('Taillow', G + 'taillow/anim_front.png', (12, 15, 44, 37)),
         ('Pidgey', G + 'pidgey/anim_front.png', (16, 10, 48, 32))]
eyes = [('Taillow', 'taillow', (19, 21, 29, 30)), ('Starly (gekozen)', 'starly', (24, 24, 34, 33)), ('Swablu', 'swablu', (29, 27, 39, 36)),
        ('Pidgey', 'pidgey', (24, 16, 34, 25)), ('Fletchling', 'fletchling', (36, 24, 46, 33)), ('Natu', 'natu', (25, 30, 35, 39)),
        ('Pichu', 'pichu', (26, 28, 36, 37)), ('Togepi', 'togepi', (24, 19, 34, 28))]
Z = 8; W = 32 * Z; H = 22 * Z
out = Image.new('RGB', (5 * (W + 16) + 16, 30 + H + 40 + 10 * Z + 40), 'white'); d = ImageDraw.Draw(out)
for i, (n, p, box) in enumerate(heads):
    x = 16 + i * (W + 16); out.paste(on(p).crop(box).resize((W, H), Image.NEAREST), (x, 28)); d.text((x, 8), n + ' (kop, 8x)', fill='black', font=F)
y = 28 + H + 40; d.text((16, y - 22), 'kandidaat-ogen (8x, eerste frame); gekozen: Starly, omgezet naar ons palet', fill='black', font=F)
for i, (n, sp, box) in enumerate(eyes):
    x = 16 + i * (10 * Z + 30); out.paste(on(G + sp + '/anim_front.png').crop(box).resize((10 * Z, 9 * Z), Image.NEAREST), (x, y))
    d.text((x, y + 9 * Z + 4), n, fill=(180, 0, 0) if 'gekozen' in n else 'black', font=F)
    if 'gekozen' in n: d.rectangle([x - 3, y - 3, x + 10 * Z + 2, y + 9 * Z + 2], outline=(200, 0, 0), width=3)
out.save('vergelijk_8x.png')
refs = [('r6', '../kleur_r6/kolibrie_pre.png'), ('r7a', 'kolibrie_pre_r7a.png'), ('r7b', 'kolibrie_pre_r7b.png'),
        ('taillow', G + 'taillow/anim_front.png'), ('pidgey', G + 'pidgey/anim_front.png'), ('starly', G + 'starly/anim_front.png')]
v = Image.new('RGB', (6 * 200 + 20, 2 * 200 + 2 * 74 + 50), 'white'); d = ImageDraw.Draw(v)
for j, (n, p) in enumerate(refs):
    for i, bg in enumerate((L, D)):
        v.paste(on(p, bg).resize((192, 192), Image.NEAREST), (10 + j * 200, 24 + i * 200))
        v.paste(on(p, bg), (10 + j * 200 + 64, 424 + i * 74))
    d.text((10 + j * 200, 4), n + ' (3x en 1x)', fill='black', font=F)
v.save('vel.png')
