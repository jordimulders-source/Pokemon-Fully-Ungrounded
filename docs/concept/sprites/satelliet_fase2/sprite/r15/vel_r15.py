# vel r15: (a) r15 | model op 64-raster | model (hoofd), (b) ringen: r15 | model met cirkels, (c) r14 | r15 op 8x, (d) 1x licht/donker
import numpy as np, sys
from PIL import Image, ImageDraw
M = Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB'); k = 12.703
def mb(x0, y0, x1, y1): return (int(round(103 + x0 * k)), int(round(143 + (y0 - 7) * k)), int(round(103 + x1 * k)), int(round(143 + (y1 - 7) * k)))
def on(im, bg):
    b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im.convert('RGBA')); return b.convert('RGB')
SP = sys.argv[1] if len(sys.argv) > 1 else 'sprite.png'
R14 = Image.open('../r14/sprite.png').convert('RGBA'); R15 = Image.open(SP).convert('RGBA')
# 64-raster van het model (blokgemiddelde)
Mn = np.array(M).astype(float); m64 = np.zeros((64, 64, 3))
for y in range(64):
    for x in range(64):
        x0, y0, x1, y1 = mb(x, y, x + 1, y + 1); b = Mn[max(0, y0):max(1, y1), max(0, x0):max(1, x1)]
        m64[y, x] = b.reshape(-1, 3).mean(0) if b.size else 255
M64 = Image.fromarray(m64.clip(0, 255).astype('uint8'))
# (a) drieluik hoofd x4-36 y12-48
X0, X1, Y0, Y1, Z = 4, 36, 14, 49, 16; w, h = (X1 - X0) * Z, (Y1 - Y0) * Z
A1 = on(R15, (255, 255, 255)).crop((X0, Y0, X1, Y1)).resize((w, h), Image.NEAREST)
A2 = M64.crop((X0, Y0, X1, Y1)).resize((w, h), Image.NEAREST)
A3 = M.crop(mb(X0, Y0, X1, Y1)).resize((w, h), Image.LANCZOS)
# (b) ringen: cirkels om het irismidden (18,5; 34,9), zelfde stralen als ringen_r14
cx, cy = 18.5, 34.9; RX0, RX1, RY0, RY1, RZ = 4, 33, 20, 49, 20
CIR = ((5.75, (0, 160, 0)), (8.5, (230, 0, 0)), (11, (0, 90, 255)), (13, (255, 140, 0)))
def ringen(img):
    img = img.copy(); d = ImageDraw.Draw(img)
    for r, c in CIR:
        px, py = (cx - RX0) * RZ, (cy - RY0) * RZ; d.ellipse([px - r * RZ, py - r * RZ, px + r * RZ, py + r * RZ], outline=c, width=2)
    return img
rw, rh = (RX1 - RX0) * RZ, (RY1 - RY0) * RZ
B1 = ringen(on(R15, (255, 255, 255)).crop((RX0, RY0, RX1, RY1)).resize((rw, rh), Image.NEAREST))
B2 = ringen(M.crop(mb(RX0, RY0, RX1, RY1)).resize((rw, rh), Image.LANCZOS))
W = max(3 * w + 20, 2 * rw + 10, 1040)
out = Image.new('RGB', (W, 16 + h + 26 + rh + 26 + 512 + 26 + 90), (205, 205, 205)); d = ImageDraw.Draw(out)
d.text((4, 2), '(a) r15 | model op 64-raster | model (x4-36, y14-49)', fill=(0, 0, 0))
for i, t in enumerate((A1, A2, A3)): out.paste(t, (i * (w + 10), 16))
y = 16 + h + 10; d.text((4, y), '(b) r15 | model, cirkels om het irismidden (18,5; 34,9): groen r5,75 lensring, rood r8,5, blauw r11, oranje r13', fill=(0, 0, 0))
out.paste(B1, (0, y + 14)); out.paste(B2, (rw + 10, y + 14))
y += 14 + rh + 12; d.text((4, y), '(c) r14 | r15 op 8x', fill=(0, 0, 0)); y += 14
for i, im in enumerate((R14, R15)): out.paste(on(im, (255, 255, 255)).resize((512, 512), Image.NEAREST), (i * 528, y))
y += 512 + 10; d.text((4, y), '(d) 1x op licht en donker: r14 | r15', fill=(0, 0, 0))
for j, bg in enumerate(((255, 255, 255), (40, 40, 48))):
    for i, im in enumerate((R14, R15)): out.paste(on(im, bg), (4 + i * 70 + j * 150, y + 16))
out.save(sys.argv[2] if len(sys.argv) > 2 else 'vel.png'); print(out.size)
