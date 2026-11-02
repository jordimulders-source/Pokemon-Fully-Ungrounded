"""Vel kleur r1: sprite 4x en 1x op licht en donker, naast Fletchling, Taillow, Natu, de eindvorm en foto 1."""
from PIL import Image, ImageDraw, ImageFont
G = '../../../../../../graphics/pokemon/'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
L, D = (236, 236, 230), (44, 44, 52)
def on(p, bg):
    im = Image.open(p)
    a = im.crop((0, 0, 64, 64)).convert('RGBA') if im.mode != 'P' else None
    if im.mode == 'P':
        c = im.crop((0, 0, 64, 64)); a = c.convert('RGBA'); px = a.load(); idx = c.load()
        for y in range(64):
            for x in range(64):
                if idx[x, y] == 0: px[x, y] = (0, 0, 0, 0)
    b = Image.new('RGBA', (64, 64), bg + (255,)); b.alpha_composite(a); return b.convert('RGB')
refs = [('kolibrie pre r1', 'kolibrie_pre.png'), ('fletchling', G + 'fletchling/anim_front.png'), ('taillow', G + 'taillow/anim_front.png'),
        ('natu', G + 'natu/anim_front.png'), ('eindvorm', '../../../kolibrie/af/kolibrie.png')]
out = Image.new('RGB', (2 * 276 + 5 * 150 + 40, 600), 'white'); d = ImageDraw.Draw(out)
for i, bg in enumerate((L, D)):
    out.paste(on('kolibrie_pre.png', bg).resize((256, 256), Image.NEAREST), (10 + i * 276, 30))
d.text((10, 8), 'kolibrie pre-evo kleur r1, 4x op licht en donker', fill='black', font=F)
x0 = 2 * 276 + 20
for j, (n, p) in enumerate(refs):
    for i, bg in enumerate((L, D)):
        out.paste(on(p, bg).resize((128, 128), Image.NEAREST), (x0 + j * 150, 30 + i * 140))
    d.text((x0 + j * 150, 8), n + ' (2x)', fill='black', font=F)
# 1x-rij
y1 = 320; d.text((10, y1 - 18), '1x op licht en donker (zelfde volgorde)', fill='black', font=F)
for j, (n, p) in enumerate(refs):
    for i, bg in enumerate((L, D)):
        out.paste(on(p, bg), (10 + j * 80, y1 + i * 74))
f1 = Image.open('../../referenties/jordi_1_zittend_jong.webp').convert('RGB').crop((200, 120, 760, 720)).resize((240, 257))
out.paste(f1, (440, y1 - 10)); d.text((690, y1), 'foto 1', fill='black', font=F)
out.save('vel.png')
