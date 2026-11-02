"""Onderlaag foto 1 op het 64-raster (s photo-px per spritepixel), voor het overtrekken met de hand."""
import sys
from PIL import Image, ImageDraw, ImageFont
REF = '../../referenties/'
S, X0, Y0, Z = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), 12
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)
f = Image.open(REF + 'jordi_1_zittend_jong.webp').convert('RGB')
u = f.crop((int(X0), int(Y0), int(X0 + 64 * S), int(Y0 + 64 * S))).resize((64 * Z, 64 * Z), Image.LANCZOS)
out = Image.new('RGB', (64 * Z + 30, 64 * Z + 30), 'white'); out.paste(u, (30, 30)); d = ImageDraw.Draw(out)
for k in range(65):
    c = (40, 90, 200) if k % 4 == 0 else (150, 180, 230)
    d.line([(30 + k * Z, 30), (30 + k * Z, 30 + 64 * Z)], fill=c); d.line([(30, 30 + k * Z), (30 + 64 * Z, 30 + k * Z)], fill=c)
    if k < 64 and k % 2 == 0: d.text((30 + k * Z + 1, 14), str(k), fill=(40, 90, 200), font=F); d.text((4, 30 + k * Z + 1), str(k), fill=(40, 90, 200), font=F)
out.save(sys.argv[4])
