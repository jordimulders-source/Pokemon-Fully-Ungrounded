"""Vel: onderlaag 4x | silhouet 4x | overlay 4x | silhouet 2x en 1x | Taillow, Starly, oud B2 r1 (3x, 1x)."""
import os, numpy as np
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(D, *['..'] * 7))  # repo-root
def txt(p): return np.array([[c == '#' for c in r] for r in open(p).read().split()])
sil = txt(os.path.join(D, 'silhouet.txt'))
prof = txt(os.path.join(D, '..', '..', 'b2', 'silhouet_r1', 'silhouet.txt'))
def mon(n):
    im = Image.open(os.path.join(R, 'graphics', 'pokemon', n, 'anim_front.png'))
    return np.array(im)[:64, :64] != 0
BG = (236, 236, 240); INK = (40, 36, 60)
def maskimg(m, s):
    im = Image.new('RGB', (64, 64), BG); a = np.array(im); a[m] = INK
    return Image.fromarray(a).resize((64 * s, 64 * s), Image.NEAREST)
Image.fromarray(np.where(sil[..., None], np.array(INK, np.uint8), np.array(BG, np.uint8)).astype(np.uint8)).save(os.path.join(D, 'silhouet_1x.png'))
ond = Image.open(os.path.join(D, '..', 'onderlaag_256.png')).convert('RGBA')
ondbg = Image.new('RGBA', ond.size, BG + (255,)); ondbg.alpha_composite(ond)
ov = ondbg.copy(); lay = Image.new('RGBA', ov.size, (0, 0, 0, 0))
la = np.array(lay); big = np.kron(sil, np.ones((4, 4), bool)); la[big] = (20, 10, 60, 130); ov.alpha_composite(Image.fromarray(la))
panels = [('onderlaag 4x', ondbg.convert('RGB')), ('silhouet r1 4x', maskimg(sil, 4)), ('over onderlaag', ov.convert('RGB'))]
W = 4 * 280 + 30
top = 30; H = top + 256 + 20 + 30 + 192 + 20
vel = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(vel)
x = 10
for t, p in panels:
    vel.paste(p, (x, top)); d.text((x, 8), t, fill=(0, 0, 0)); x += p.width + 20
vel.paste(maskimg(sil, 2), (x, top)); d.text((x, 8), '2x / 1x', fill=(0, 0, 0)); vel.paste(maskimg(sil, 1), (x, top + 140))
y2 = top + 256 + 40; x = 10
for t, m in [('K1R2 r1', sil), ('Taillow', mon('taillow')), ('Starly', mon('starly')), ('oud B2 r1', prof)]:
    vel.paste(maskimg(m, 3), (x, y2)); vel.paste(maskimg(m, 1), (x + 200, y2 + 128))
    d.text((x, y2 - 16), f'{t} ({int(m.sum())} px)', fill=(0, 0, 0)); x += 280
vel = vel.crop((0, 0, max(W, x), H))
vel.save(os.path.join(D, 'vel.png')); print(vel.size)
