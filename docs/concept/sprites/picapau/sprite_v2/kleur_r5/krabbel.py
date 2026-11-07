"""krabbel_over_r5.png: Jordi's krabbel (getekend op r2) teruggerekend naar spritecoördinaten en in magenta over r2 en r5 (8x).
Schaal/offset uit de omhullende van de r2-sprite in zijn screenshot (x13-50 -> 1047-1338 px, y3-57 -> 45-465 px)."""
import numpy as np
from PIL import Image, ImageDraw
K = np.asarray(Image.open('../../referenties/jordi_krabbel_r2_model_genegeerd.png').convert('RGB')).astype(int)
sx = (1339 - 1047) / 38; ox = 1047 - 13 * sx; sy = (466 - 45) / 55; oy = 45 - 3 * sy
m = K.sum(-1) < 45; m[:, :960] = False
ys, xs = np.where(m)
def schoon(p):
    s = Image.open(p).convert('RGBA'); px = s.load()
    for y in range(64):
        for x in range(64):
            if px[x, y][:3] == (152, 208, 160): px[x, y] = (232, 232, 232, 255)
    return s.resize((512, 512), Image.NEAREST)
v = Image.new('RGBA', (512 * 2 + 20, 530), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
for i, (p, naam) in enumerate([('../kleur_r2/picapau.png', 'r2 (waarop Jordi tekende)'), ('picapau.png', 'r5')]):
    im = schoon(p); dd = ImageDraw.Draw(im)
    for X, Y in zip(xs, ys):
        u = (X - ox) / sx * 8; w = (Y - oy) / sy * 8
        dd.point((u, w), fill=(255, 0, 255, 255))
    v.alpha_composite(im, (i * 532, 18)); d.text((4 + i * 532, 2), 'krabbel Jordi in magenta over ' + naam, fill=(0, 0, 0))
v.save('krabbel_over_r5.png')
