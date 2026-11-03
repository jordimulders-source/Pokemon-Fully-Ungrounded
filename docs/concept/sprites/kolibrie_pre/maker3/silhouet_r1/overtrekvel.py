"""Overtrekvel: foto 5 gespiegeld (kijkt naar links) als onderlaag op het 64-raster met spritecoördinaten,
silhouet erover (rode omtrek), oranje zones = bewuste afwijkingen (zones.txt). Rechts: silhouet los op hetzelfde raster
en foto 3 (bek). Uitlijning: kruin (y16) en borst links (x13-14) van foto en silhouet vallen samen.
Gebruik: python3 overtrekvel.py"""
from PIL import Image, ImageDraw, ImageFont
REF = '../../referenties/'
S, X0, Y0, Z = 7.5, 597, 770, 12        # 7,5 foto-px per spritepixel
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
ZONES = [l.rstrip('\n').split(' ', 4) for l in open('zones.txt') if l.strip() and not l.startswith('#')]
rows = [l.rstrip('\n') for l in open('silhouet.txt')][:64]
M = [[c == '#' for c in r] for r in rows]
W = 64 * Z

def grid(d, ox, oy):
    for k in range(65):
        c = (40, 90, 200) if k % 4 == 0 else (160, 185, 230)
        d.line([(ox + k * Z, oy), (ox + k * Z, oy + W)], fill=c); d.line([(ox, oy + k * Z), (ox + W, oy + k * Z)], fill=c)
        if k < 64 and k % 2 == 0:
            d.text((ox + k * Z + 1, oy - 13), str(k), fill=(40, 90, 200), font=F); d.text((ox - 20, oy + k * Z), str(k), fill=(40, 90, 200), font=F)

def omtrek(d, ox, oy, col=(230, 20, 20)):
    for y in range(64):
        for x in range(64):
            if not M[y][x]: continue
            X, Y = ox + x * Z, oy + y * Z
            if x == 63 or not M[y][x + 1]: d.line([(X + Z - 1, Y), (X + Z - 1, Y + Z - 1)], fill=col, width=3)
            if x == 0 or not M[y][x - 1]: d.line([(X, Y), (X, Y + Z - 1)], fill=col, width=3)
            if y == 63 or not M[y + 1][x]: d.line([(X, Y + Z - 1), (X + Z - 1, Y + Z - 1)], fill=col, width=3)
            if y == 0 or not M[y - 1][x]: d.line([(X, Y), (X + Z - 1, Y)], fill=col, width=3)

f5 = Image.open(REF + 'jordi_5_uitvlieger_hand.webp').convert('RGB').transpose(Image.FLIP_LEFT_RIGHT)
u = f5.crop((X0, Y0, int(X0 + 64 * S), int(Y0 + 64 * S))).resize((W, W), Image.LANCZOS)
out = Image.new('RGB', (2 * W + 380, W + 70), 'white'); d = ImageDraw.Draw(out)
ox, oy = 30, 45
out.paste(u, (ox, oy)); grid(d, ox, oy); omtrek(d, ox, oy)
for x0, y0, x1, y1, lab in ZONES:
    x0, y0, x1, y1 = map(int, (x0, y0, x1, y1))
    d.rectangle([ox + x0 * Z, oy + y0 * Z, ox + (x1 + 1) * Z, oy + (y1 + 1) * Z], outline=(255, 140, 0), width=3)
    d.text((ox + x0 * Z + 3, oy + y0 * Z + 2), lab.split(':')[0], fill=(255, 120, 0), font=FB)
d.text((ox, 6), 'Foto 5 gespiegeld (onderlaag, 7,5 foto-px = 1 spritepixel) + silhouet (rood). Oranje = bewuste afwijking.', fill='black', font=FB)
ox2 = ox + W + 30
s = Image.new('RGB', (W, W), (236, 236, 230)); ds = ImageDraw.Draw(s)
for y in range(64):
    for x in range(64):
        if M[y][x]: ds.rectangle([x * Z, y * Z, x * Z + Z - 1, y * Z + Z - 1], fill=(40, 30, 60))
out.paste(s, (ox2, oy)); grid(d, ox2, oy)
for x0, y0, x1, y1, lab in ZONES:
    x0, y0, x1, y1 = map(int, (x0, y0, x1, y1))
    d.rectangle([ox2 + x0 * Z, oy + y0 * Z, ox2 + (x1 + 1) * Z, oy + (y1 + 1) * Z], outline=(255, 140, 0), width=2)
d.text((ox2, 24), 'silhouet op hetzelfde raster', fill='black', font=FB)
ox3 = ox2 + W + 20
f3 = Image.open(REF + 'jordi_3_nestjongen.png').convert('RGB').crop((60, 235, 200, 345)).transpose(Image.FLIP_LEFT_RIGHT).resize((300, 236))
out.paste(f3, (ox3, oy)); d.text((ox3, oy + 240), 'foto 3 gespiegeld: bedelbek', fill='black', font=F)
ty = oy + 270
for x0, y0, x1, y1, lab in ZONES:
    for i in range(0, len(lab), 50):
        d.text((ox3, ty), lab[i:i + 50], fill=(200, 90, 0), font=F); ty += 13
    ty += 6
out.save('overtrekvel.png')
