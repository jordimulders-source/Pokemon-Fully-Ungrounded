"""vergelijk_8x.png: koppen r7b | r8 lager | r9 op 8x (licht), plus r9 op donker en foto 3.
vel.png: r7b, r8 lager, r9 naast Taillow op 3x en 1x, licht en donker."""
from PIL import Image, ImageDraw, ImageFont
G = '../../../../../../graphics/pokemon/'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
def on(p, bg=(236, 236, 230)):
    im = Image.open(p); c = im.crop((0, 0, 64, 64)); a = c.convert('RGBA'); px = a.load(); idx = c.load()
    for y in range(64):
        for x in range(64):
            if idx[x, y] == 0: px[x, y] = (0, 0, 0, 0)
    b = Image.new('RGBA', (64, 64), bg + (255,)); b.alpha_composite(a); return b.convert('RGB')
box, Z = (7, 8, 37, 27), 8
W, H = (box[2] - box[0]) * Z, (box[3] - box[1]) * Z
ks = [('r7b', on('../kleur_r7/kolibrie_pre_r7b.png')), ('r8 lager', on('../kleur_r8/kolibrie_pre_lager.png')), ('r9', on('kolibrie_pre.png')),
      ('r9 donker', on('kolibrie_pre.png', (44, 44, 52)))]
f3 = Image.open('../../referenties/jordi_3_nestjongen.png').convert('RGB').crop((60, 235, 200, 345)).transpose(Image.FLIP_LEFT_RIGHT).resize((int(H * 140 / 110), H))
out = Image.new('RGB', (4 * (W + 16) + f3.size[0] + 32, H + 36), 'white'); d = ImageDraw.Draw(out)
for i, (n, im) in enumerate(ks):
    x = 16 + i * (W + 16); out.paste(im.crop(box).resize((W, H), Image.NEAREST), (x, 28)); d.text((x, 6), n + ' (8x)', fill='black', font=F)
x = 16 + 4 * (W + 16); out.paste(f3, (x, 28)); d.text((x, 6), 'foto 3 (gespiegeld)', fill='black', font=F)
out.save('vergelijk_8x.png')
refs = [('r7b', '../kleur_r7/kolibrie_pre_r7b.png'), ('r8 lager', '../kleur_r8/kolibrie_pre_lager.png'), ('r9', 'kolibrie_pre.png'), ('taillow', G + 'taillow/anim_front.png')]
v = Image.new('RGB', (4 * 200 + 20, 2 * 200 + 2 * 74 + 50), 'white'); d = ImageDraw.Draw(v)
for j, (n, p) in enumerate(refs):
    for i, bg in enumerate(((236, 236, 230), (44, 44, 52))):
        v.paste(on(p, bg).resize((192, 192), Image.NEAREST), (10 + j * 200, 24 + i * 200)); v.paste(on(p, bg), (10 + j * 200 + 64, 424 + i * 74))
    d.text((10 + j * 200, 4), n + ' (3x en 1x)', fill='black', font=F)
v.save('vel.png')
