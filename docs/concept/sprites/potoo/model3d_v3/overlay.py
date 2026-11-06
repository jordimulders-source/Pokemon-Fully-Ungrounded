"""Omtrek van de leidraadfoto (kop tegen de lucht) over de render, uitgelijnd op het nabije oog.
python3 overlay.py render.png uit.png   (render van hoek kop_leidraad_r: vogel kijkt naar rechts, zoals de foto)"""
import sys
import numpy as np
from PIL import Image, ImageDraw
REF = '../referenties/jordi_great_potoo_bek_open_duo.webp'
OOG_F = (380.0, 225.0, 30.0)                       # oogmidden en straal op de foto (gemeten op raster)
foto = np.asarray(Image.open(REF).convert('RGB')).astype(int)[:, :640]
R, G, B = foto[..., 0], foto[..., 1], foto[..., 2]
lucht = (B > 150) & (B > R + 35) & (B > G + 5)
vogel = ~lucht
rand_f = vogel & (np.roll(lucht, 1, 0) | np.roll(lucht, -1, 0) | np.roll(lucht, 1, 1) | np.roll(lucht, -1, 1))
r = np.asarray(Image.open(sys.argv[1]).convert('RGBA')).astype(int)
a = r[..., 3] > 128
zw = a & (r[..., :3].max(-1) < 45) & ((r[..., 2] - r[..., 0]) < 10)
ys, xs = np.nonzero(zw)
# grootste zwarte vlek = nabije oog: neem de vlek rond het meest rechtse zwarte gebied (vogel kijkt naar rechts, nabij oog groter)
from collections import deque
lab = np.zeros(zw.shape, int); n = 0; best = None
for y0, x0 in zip(ys, xs):
    if lab[y0, x0]: continue
    n += 1; q = deque([(y0, x0)]); lab[y0, x0] = n; pts = []
    while q:
        y, x = q.popleft(); pts.append((y, x))
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < zw.shape[0] and 0 <= xx < zw.shape[1] and zw[yy, xx] and not lab[yy, xx]:
                lab[yy, xx] = n; q.append((yy, xx))
    if best is None or len(pts) > len(best): best = pts
p = np.array(best); cy, cx = p.mean(0); rr = np.sqrt(len(p) / np.pi)
s = OOG_F[2] / rr
img = Image.open(sys.argv[1]).convert('RGBA')
img = img.resize((int(img.width * s), int(img.height * s)))
W, H = 640, 720
bg = Image.fromarray(foto.astype(np.uint8)).convert('RGBA').resize((640, 720)) if False else Image.fromarray(np.asarray(Image.open(REF).convert('RGB'))[:, :640]).convert('RGBA')
links = Image.new('RGBA', (W, H), (60, 80, 60, 255))
links.alpha_composite(img, (int(OOG_F[0] - cx * s), int(OOG_F[1] - cy * s)))
d = ImageDraw.Draw(links)
from score import LIJN
d.line(LIJN, fill=(255, 40, 40, 255), width=2)
# rechts: foto met render-omtrek
ar = np.asarray(links.convert('RGBA'))[..., :3]
al = np.zeros((H, W), bool)
ai = np.asarray(img)[..., 3] > 128
ox, oy = int(OOG_F[0] - cx * s), int(OOG_F[1] - cy * s)
for y, x in zip(*np.nonzero(ai)):
    yy, xx = y + oy, x + ox
    if 0 <= yy < H and 0 <= xx < W: al[yy, xx] = True
rand_r = al & ~(np.roll(al, 1, 0) & np.roll(al, -1, 0) & np.roll(al, 1, 1) & np.roll(al, -1, 1))
rechts = bg.copy(); d2 = ImageDraw.Draw(rechts); d2.line(LIJN, fill=(255, 40, 40, 255), width=1)
for y, x in zip(*np.nonzero(rand_r)): d2.point((x, y), fill=(40, 255, 255, 255))
o = Image.new('RGB', (W * 2, H)); o.paste(links.convert('RGB'), (0, 0)); o.paste(rechts.convert('RGB'), (W, 0))
o.crop((0, 40, W * 2, 560)).save(sys.argv[2])
print('schaal', round(s, 3), 'oog render', round(cx), round(cy), round(rr, 1))
