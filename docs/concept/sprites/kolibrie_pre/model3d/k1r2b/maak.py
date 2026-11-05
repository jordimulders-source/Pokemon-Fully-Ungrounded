"""K1-R2b: model zo aangepast dat het platte silhouet dezelfde vormen toont als de render (Jordi: "silhouet is gewoon niet
hetzelfde als het 3d model"): lijf onder de kop lager (nek), kop iets hoger/voor, staartstompje los, bekje langer en verder open.
Het silhouet is de render direct verkleind, zonder handwerk. python3 k1r2b/maak.py (vanuit model3d/)"""
import sys, numpy as np
sys.path.insert(0, ".")
from PIL import Image, ImageDraw, ImageFont
import kop3d as K, model as M
KW = dict(rond=2.5, nek=3, staart_uit=(2, 1), c=(22.8, 16.6), gaap=55, snavel=9.5)
img, al = K.render(15, 14, **KW)
rgba = Image.fromarray(np.dstack([img, al * 255]).astype(np.uint8))
rgba.save('k1r2b/onderlaag_384.png'); rgba.resize((64, 64), Image.LANCZOS).save('k1r2b/onderlaag_64.png')
m = M.naar64(al)
open('k1r2b/silhouet.txt', 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in m) + '\n')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
BG = (236, 234, 228)
def bg(im):
    v = Image.new('RGB', im.size, BG); v.paste(im, (0, 0), im); return v
def sil(mm, k): return Image.fromarray(np.where(mm, 40, 236).astype(np.uint8)).convert('RGB').resize((64 * k, 64 * k), Image.NEAREST)
st = Image.open('../../../../../graphics/pokemon/starly/anim_front.png'); sa = np.array(st.crop((0, 0, 64, 64))) != 0
s_rgba = np.array(st.convert('RGBA').crop((0, 0, 64, 64))); s_rgba[..., 3] = sa * 255; s_rgba = Image.fromarray(s_rgba)
V = Image.new('RGB', (16 + 4 * 272, 48 + 256 + 30 + 64 + 40), 'white'); d = ImageDraw.Draw(V)
d.text((16, 12), f'Kolibrie pre-evo K1-R2b: silhouet = het model zelf, direct verkleind (geen handwerk) · {m.sum()} px', font=FB, fill=(40, 36, 50))
rij = [(bg(rgba.resize((256, 256), Image.LANCZOS)), 'model (4x)'), (sil(m, 4), 'silhouet (4x)'),
       (bg(s_rgba).resize((256, 256), Image.NEAREST), 'Starly'), (sil(sa, 4), 'Starly silhouet')]
for i, (im, l) in enumerate(rij):
    V.paste(im, (16 + i * 272, 44)); d.text((16 + i * 272, 44 + 260), l, font=F, fill=(90, 86, 100))
y = 44 + 290
V.paste(bg(rgba.resize((64, 64), Image.LANCZOS)), (16, y)); V.paste(sil(m, 1), (90, y))
V.paste(bg(s_rgba), (16 + 2 * 272, y)); V.paste(sil(sa, 1), (90 + 2 * 272, y))
d.text((170, y + 20), '1x: model en silhouet', font=F, fill=(90, 86, 100))
V.save('k1r2b/vel.png'); print(m.sum())
