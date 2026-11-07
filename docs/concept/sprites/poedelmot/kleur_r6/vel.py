"""vel.png: r6 | r5 | bron op 8x, 1x/2x op licht en donker, en close-ups per onderdeel (r2 naast bron)."""
import os, sys
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__))
R1 = os.path.join(H, '..', 'kleur_r5', 'poedelmot.png')
R2 = os.path.join(H, 'poedelmot.png')
SRC = os.path.join(H, '..', 'referenties', 'samengesteld.png')
k = (854-139)/62; X0, Y0 = 139 - k*1, 150 - k*17          # zelfde schaal als silhouet/sil.py
src = Image.open(SRC).convert('RGB')
def sprite(path, col=(152, 208, 160, 255)):
    p = Image.open(path); rgba = p.convert('RGBA'); idx = p.load()
    m = Image.new('L', (64, 64), 0); mp = m.load()
    for y in range(64):
        for x in range(64): mp[x, y] = 255 if idx[x, y] else 0
    b = Image.new('RGBA', (64, 64), col); b.paste(rgba, (0, 0), m); return b.convert('RGB')
def bron(x0, y0, x1, y1, S):
    return src.crop((int(X0+x0*k), int(Y0+y0*k), int(X0+x1*k), int(Y0+y1*k))).resize(((x1-x0)*S, (y1-y0)*S), Image.LANCZOS)
def deel(im, x0, y0, x1, y1, S): return im.crop((x0, y0, x1, y1)).resize(((x1-x0)*S, (y1-y0)*S), Image.NEAREST)
s2, s1 = sprite(R2), sprite(R1)
S = 8; W = 64*S*3 + 32
CU = [('ogen en gezicht', 12, 28, 40, 46), ('sprieten', 0, 16, 56, 32), ('pootjes', 12, 42, 58, 62), ('vleugels', 34, 17, 64, 48)]
cs = 12
hcu = sum((y1-y0)*cs + 28 for _, x0, y0, x1, y1 in CU)
V = Image.new('RGB', (W + 300, 64*S + 40 + hcu), (255, 255, 255)); d = ImageDraw.Draw(V)
for i, (im, t) in enumerate([(s2.resize((512, 512), Image.NEAREST), 'kleur_r6 (8x)'), (s1.resize((512, 512), Image.NEAREST), 'kleur_r5 (8x)'), (bron(0, 0, 64, 64, S), 'bron: samengesteld.png (8x)')]):
    V.paste(im, (i*(512+16), 24)); d.text((i*(512+16)+4, 6), t, fill=(0, 0, 0))
x0 = W + 8; d.text((x0, 6), 'r6 1x / 2x', fill=(0, 0, 0))
for j, col in enumerate([(232, 232, 224, 255), (40, 40, 56, 255)]):
    V.paste(sprite(R2, col), (x0 + j*72, 24)); V.paste(sprite(R2, col).resize((128, 128), Image.NEAREST), (x0 + j*136, 100))
y = 64*S + 40
for t, a, b_, c, e in CU:
    d.text((4, y), f'close-up {t}: r6 (links) - bron (rechts), {cs}x', fill=(0, 0, 0)); y += 16
    L = deel(s2, a, b_, c, e, cs); R = bron(a, b_, c, e, cs)
    V.paste(L, (0, y)); V.paste(R, (L.width + 12, y)); y += L.height + 12
V.save(os.path.join(H, 'vel.png'))
