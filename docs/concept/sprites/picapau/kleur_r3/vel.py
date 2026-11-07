"""Vergelijkingsvel r3: 1x (boven) en 8x (onder): Taillow, r2-A, r3-A, r3-B, Pikachu."""
import os
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(D, '..', '..', '..', '..', '..')
def load(p):
    im = Image.open(p); f = im.crop((0, 0, 64, 64)); r = f.convert('RGBA'); px = r.load()
    for y in range(64):
        for x in range(64):
            if f.getpixel((x, y)) == 0: px[x, y] = (0, 0, 0, 0)
    return r
L = [('Taillow', os.path.join(R, 'graphics/pokemon/taillow/anim_front.png')),
     ('r2-A', os.path.join(D, '..', 'kleur_r2', 'picapau_A.png')),
     ('r3-A', os.path.join(D, 'picapau_A.png')),
     ('r3-B (voorstel)', os.path.join(D, 'picapau_B.png')),
     ('Pikachu', os.path.join(R, 'graphics/pokemon/pikachu/anim_front.png'))]
out = Image.new('RGBA', (len(L) * 532 + 20, 64 + 40 + 512 + 30), (255, 255, 255, 255)); d = ImageDraw.Draw(out)
for i, (n, p) in enumerate(L):
    im = load(p)
    out.alpha_composite(im, (20 + i * 80, 10))
    out.alpha_composite(im.resize((512, 512), Image.NEAREST), (20 + i * 532, 104))
    d.text((20 + i * 532, 88), n, fill=(0, 0, 0, 255))
out.save(os.path.join(D, 'vel.png'))
