"""vergelijk_8x.png: bek r7b | r8 (licht, donker) naast echte bekken (Pelipper, Wingull, Spearow, Taillow) op 8x en foto 3."""
from PIL import Image, ImageDraw, ImageFont
G = '../../../../../../graphics/pokemon/'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
def on(p, box, bg=(236, 236, 230)):
    im = Image.open(p); c = im.crop((0, 0, 64, 64)); a = c.convert('RGBA'); px = a.load(); idx = c.load()
    for y in range(64):
        for x in range(64):
            if idx[x, y] == 0: px[x, y] = (0, 0, 0, 0)
    b = Image.new('RGBA', (64, 64), bg + (255,)); b.alpha_composite(a); return b.convert('RGB').crop(box)
Z = 8
items = [('r7b', on('../kleur_r7/kolibrie_pre_r7b.png', (7, 10, 25, 24))), ('r8', on('kolibrie_pre.png', (7, 10, 25, 24))),
         ('r8 donker', on('kolibrie_pre.png', (7, 10, 25, 24), (44, 44, 52))),
         ('Pelipper (open bek)', on(G + 'pelipper/anim_front.png', (9, 14, 27, 28))), ('Wingull', on(G + 'wingull/anim_front.png', (10, 27, 28, 41))),
         ('Spearow', on(G + 'spearow/anim_front.png', (16, 16, 34, 30))), ('Taillow', on(G + 'taillow/anim_front.png', (12, 19, 30, 33)))]
W, H = 18 * Z, 14 * Z
f3 = Image.open('../../referenties/jordi_3_nestjongen.png').convert('RGB').crop((60, 235, 200, 345)).transpose(Image.FLIP_LEFT_RIGHT).resize((W, H))
items.append(('foto 3 (gespiegeld)', f3))
out = Image.new('RGB', (len(items) * (W + 14) + 14, H + 40), 'white'); d = ImageDraw.Draw(out)
for i, (n, im) in enumerate(items):
    x = 14 + i * (W + 14); out.paste(im if im.size == (W, H) else im.resize((W, H), Image.NEAREST), (x, 28)); d.text((x, 6), n, fill='black', font=F)
out.save('vergelijk_8x.png')
