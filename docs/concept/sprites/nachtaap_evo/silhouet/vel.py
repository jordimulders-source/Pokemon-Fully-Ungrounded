"""Vel voor Jordi: poppetje | silhouet 4x | silhouet over poppetje | 1x/2x, plus echte Gen 3-silhouetten."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..', '..', '..')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
s = np.load(os.path.join(HERE, 'hand_sil.npy')); f = np.load(os.path.join(HERE, 'hand_far.npy'))


def silimg(sil, far=None, col=(40, 32, 56)):
    a = np.zeros((64, 64, 4), np.uint8); a[sil] = (*col, 255)
    if far is not None:
        a[far] = (110, 94, 136, 255)
    return Image.fromarray(a)


silimg(s, f).save(os.path.join(HERE, 'silhouet_1x.png'))
und = Image.open(os.path.join(HERE, 'onderlaag_256.png')).convert('RGB')
o = Image.new('RGB', (10 + 4 * 266, 500), 'white'); d = ImageDraw.Draw(o)
o.paste(und, (10, 30)); d.text((10, 8), 'poppetje (zelfde schaal)', font=F, fill=(40, 40, 40))
b = silimg(s).resize((256, 256), Image.NEAREST); bg = Image.new('RGB', (256, 256), 'white'); bg.paste(b, (0, 0), b)
o.paste(bg, (276, 30)); d.text((276, 8), f'silhouet 4× ({int(s.sum())} px)', font=F, fill=(40, 40, 40))
ov = np.array(und).astype(float); m = np.kron(s, np.ones((4, 4))).astype(bool); ov[m] = ov[m] * 0.45 + np.array((255, 60, 60)) * 0.55
o.paste(Image.fromarray(ov.astype(np.uint8)), (542, 30)); d.text((542, 8), 'silhouet over het poppetje', font=F, fill=(40, 40, 40))
s1 = silimg(s); o.paste(s1, (808, 30), s1); s2 = s1.resize((128, 128), Image.NEAREST); o.paste(s2, (880, 30), s2)
d.text((808, 8), '1× en 2×', font=F, fill=(40, 40, 40))
d.text((10, 300), 'echte sprites als silhouet (1× en 2×), zelfde bouwtype / fase:', font=F, fill=(40, 40, 40))
x = 10
for n in ['lairon', 'sandslash', 'vigoroth', 'zigzagoon', 'aipom']:
    im = Image.open(os.path.join(ROOT, f'graphics/pokemon/{n}/anim_front.png')).crop((0, 0, 64, 64))
    ss = np.array(list(im.get_flattened_data())).reshape(64, 64) != 0
    a = silimg(ss); o.paste(a, (x, 330), a); a2 = a.resize((128, 128), Image.NEAREST); o.paste(a2, (x + 66, 330), a2)
    d.text((x, 465), f'{n} ({int(ss.sum())})', font=F, fill=(40, 40, 40)); x += 205
o.save(os.path.join(HERE, 'vel_silhouet.png'))
