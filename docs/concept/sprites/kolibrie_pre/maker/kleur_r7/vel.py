"""Vel r4: r3 | r4 op 8x (lijnvergelijking, met raster) en r4 op 3x en 1x naast Gen 3-referenties, licht en donker."""
from PIL import Image, ImageDraw, ImageFont
G = '../../../../../../graphics/pokemon/'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
L, D = (236, 236, 230), (44, 44, 52)
def on(p, bg):
    im = Image.open(p); c = im.crop((0, 0, 64, 64)); a = c.convert('RGBA'); px = a.load(); idx = c.load()
    for y in range(64):
        for x in range(64):
            if idx[x, y] == 0: px[x, y] = (0, 0, 0, 0)
    b = Image.new('RGBA', (64, 64), bg + (255,)); b.alpha_composite(a); return b.convert('RGB')
X0, Y0, X1, Y1, Z = 6, 7, 48, 47, 8
W, H = (X1 - X0) * Z, (Y1 - Y0) * Z
refs = [('r6', 'kolibrie_pre.png'), ('taillow', G + 'taillow/anim_front.png'), ('swablu', G + 'swablu/anim_front.png'),
        ('wingull', G + 'wingull/anim_front.png'), ('natu', G + 'natu/anim_front.png'), ('pidgey', G + 'pidgey/anim_front.png'),
        ('starly', G + 'starly/anim_front.png')]
out = Image.new('RGB', (max(2 * W + 60, 7 * 200 + 20), H + 40 + 2 * 200 + 2 * 74 + 60), 'white'); d = ImageDraw.Draw(out)
for i, (p, t) in enumerate((('../kleur_r5/kolibrie_pre.png', 'r5 (8x)'), ('kolibrie_pre.png', 'r6 (8x)'))):
    ox = 20 + i * (W + 20)
    out.paste(on(p, L).crop((X0, Y0, X1, Y1)).resize((W, H), Image.NEAREST), (ox, 30)); d.text((ox, 10), t, fill='black', font=F)
    for k in range(X1 - X0 + 1): d.line([(ox + k * Z, 30), (ox + k * Z, 30 + H)], fill=(205, 205, 215))
    for k in range(Y1 - Y0 + 1): d.line([(ox, 30 + k * Z), (ox + W, 30 + k * Z)], fill=(205, 205, 215))
y = H + 60; d.text((20, y - 16), '3x en 1x op licht en donker: r6 naast Gen 3 (Taillow, Swablu, Wingull, Natu, Pidgey, Starly)', fill='black', font=F)
for j, (n, p) in enumerate(refs):
    for i, bg in enumerate((L, D)):
        out.paste(on(p, bg).resize((192, 192), Image.NEAREST), (20 + j * 200, y + i * 200))
        out.paste(on(p, bg), (20 + j * 200 + 64, y + 400 + i * 74))
    d.text((20 + j * 200, y + 400 + 2 * 74), n, fill='black', font=F)
out.save('vel.png')
