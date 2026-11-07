"""vel.png: sprite (8x) | model op 8x, close-ups (kop/sprieten, pootjes, achterlijf) op 14x naast het model, en 1x/2x op licht en donker naast het verkleinde model.
Gebruik: python3 vel.py [vorige_ronde.png]  (met vorige ronde: rN | rN-1 | model)"""
import os, sys
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__))
R2 = os.path.join(H, 'poedellarve.png')
R1 = sys.argv[1] if len(sys.argv) > 1 else None
SRC = os.path.join(H, '..', 'referenties', 'model_gekozen.png')
k = 13.55; X0, Y0 = 236 - k*12, 346 - k*33          # zelfde schaal als silhouet/sil.py
src = Image.open(SRC).convert('RGB')
def sprite(path, col=(152, 208, 160, 255)):
    p = Image.open(path); rgba = p.convert('RGBA'); idx = p.load()
    m = Image.new('L', (64, 64), 0); mp = m.load()
    for y in range(64):
        for x in range(64): mp[x, y] = 255 if idx[x, y] else 0
    b = Image.new('RGBA', (64, 64), col); b.paste(rgba, (0, 0), m); return b.convert('RGB')
def bron(x0, y0, x1, y1, S, f=Image.LANCZOS):
    return src.crop((int(X0+x0*k), int(Y0+y0*k), int(X0+x1*k), int(Y0+y1*k))).resize(((x1-x0)*S, (y1-y0)*S), f)
def deel(im, x0, y0, x1, y1, S): return im.crop((x0, y0, x1, y1)).resize(((x1-x0)*S, (y1-y0)*S), Image.NEAREST)
s2 = sprite(R2)
cols = [(s2, 'kleur_r1 (8x)')] + ([(sprite(R1), 'vorige ronde (8x)')] if R1 else [])
# uitsnede x 8-56, y 30-64 op 8x
BX0, BY0, BX1, BY1, S = 8, 30, 56, 64, 8
panels = [(deel(im, BX0, BY0, BX1, BY1, S), t) for im, t in cols] + [(bron(BX0, BY0, BX1, BY1, S), 'model (8x)')]
pw, ph = (BX1-BX0)*S, (BY1-BY0)*S
CU = [('kop, ogen, snuit en sprieten', 31, 32, 53, 54), ('voorpootjes en borst', 30, 46, 53, 63), ('achterlijf, bolletjes en pootjes', 10, 43, 35, 63)]
cs = 14
hcu = sum((y1-y0)*cs + 28 for _, x0, y0, x1, y1 in CU)
W = max(len(panels)*(pw+16), max((x1-x0)*cs*2+12 for _, x0, y0, x1, y1 in CU)) + 8
V = Image.new('RGB', (W, ph + 40 + hcu + 200), (255, 255, 255)); d = ImageDraw.Draw(V)
for i, (im, t) in enumerate(panels):
    V.paste(im, (i*(pw+16), 24)); d.text((i*(pw+16)+4, 6), t, fill=(0, 0, 0))
y = ph + 40
for t, a, b_, c, e in CU:
    d.text((4, y), f'close-up {t}: sprite (links) - model (rechts), {cs}x', fill=(0, 0, 0)); y += 16
    L = deel(s2, a, b_, c, e, cs); R = bron(a, b_, c, e, cs)
    V.paste(L, (0, y)); V.paste(R, (L.width + 12, y)); y += L.height + 12
d.text((4, y), '1x en 2x op licht en donker, naast het model verkleind (BOX) naar 1x/2x', fill=(0, 0, 0)); y += 16
mod1 = src.crop((int(X0), int(Y0), int(X0+64*k), int(Y0+64*k))).resize((64, 64), Image.BOX)
x = 0
for col in [(232, 232, 224, 255), (40, 40, 56, 255)]:
    V.paste(sprite(R2, col), (x, y)); x += 72
V.paste(mod1, (x, y)); x += 80
for col in [(232, 232, 224, 255), (40, 40, 56, 255)]:
    V.paste(sprite(R2, col).resize((128, 128), Image.NEAREST), (x, y)); x += 136
V.paste(mod1.resize((128, 128), Image.NEAREST), (x, y))
V = V.crop((0, 0, W, y + 136))
V.save(os.path.join(H, 'vel.png'))
