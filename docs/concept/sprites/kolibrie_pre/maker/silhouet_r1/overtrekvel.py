"""Overtrekvel (Coathief-methode): foto 1 als onderlaag op het 64-raster met spritecoördinaten, het silhouet erover
(halfdoorzichtig + rode omtrek) en de zones waar bewust van de foto is afgeweken. Ernaast foto 5 (gespiegeld) en foto 3
(bek, gespiegeld) op dezelfde kopgrootte, en het silhouet los op hetzelfde raster.
Gebruik: python3 overtrekvel.py [uit.png]"""
import sys
from PIL import Image, ImageDraw, ImageFont
REF = '../../referenties/'
S, X0, Y0, Z = 10.0, 238, 46, 12          # foto 1: 10 foto-px per spritepixel; kop van de foto = kop van het silhouet
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
# zones: (x0, y0, x1, y1, label) in spritecoördinaten
ZONES = [l.rstrip('\n').split(' ', 4) for l in open('zones.txt') if l.strip() and not l.startswith('#')]
rows = [l.rstrip('\n') for l in open('silhouet.txt')][:64]
M = [[c == '#' for c in r] for r in rows]

def grid(img, ox, oy, d, labels=True):
    for k in range(65):
        c = (40, 90, 200) if k % 4 == 0 else (150, 180, 230)
        d.line([(ox + k * Z, oy), (ox + k * Z, oy + 64 * Z)], fill=c); d.line([(ox, oy + k * Z), (ox + 64 * Z, oy + k * Z)], fill=c)
        if labels and k < 64 and k % 2 == 0:
            d.text((ox + k * Z + 1, oy - 14), str(k), fill=(40, 90, 200), font=F); d.text((ox - 18, oy + k * Z + 1), str(k), fill=(40, 90, 200), font=F)

def overlay(base):
    base = base.convert('RGBA'); ov = Image.new('RGBA', base.size); d = ImageDraw.Draw(ov)
    for y in range(64):
        for x in range(64):
            if M[y][x]:
                d.rectangle([x * Z, y * Z, x * Z + Z - 1, y * Z + Z - 1], fill=(60, 20, 120, 70))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < 64 and 0 <= ny < 64 and M[ny][nx]):
                        if dx == 1: d.line([(x * Z + Z - 1, y * Z), (x * Z + Z - 1, y * Z + Z - 1)], fill=(230, 20, 20, 255), width=2)
                        if dx == -1: d.line([(x * Z, y * Z), (x * Z, y * Z + Z - 1)], fill=(230, 20, 20, 255), width=2)
                        if dy == 1: d.line([(x * Z, y * Z + Z - 1), (x * Z + Z - 1, y * Z + Z - 1)], fill=(230, 20, 20, 255), width=2)
                        if dy == -1: d.line([(x * Z, y * Z), (x * Z + Z - 1, y * Z)], fill=(230, 20, 20, 255), width=2)
    base.alpha_composite(ov); return base.convert('RGB')

f1 = Image.open(REF + 'jordi_1_zittend_jong.webp').convert('RGB')
u = f1.crop((X0, Y0, int(X0 + 64 * S), int(Y0 + 64 * S))).resize((64 * Z, 64 * Z), Image.LANCZOS)
W = 64 * Z
out = Image.new('RGB', (2 * W + 3 * 40 + 330, W + 90), 'white'); d = ImageDraw.Draw(out)
ox, oy = 40, 50
out.paste(overlay(u), (ox, oy)); grid(out, ox, oy, d)
for x0, y0, x1, y1, lab in ZONES:
    x0, y0, x1, y1 = map(int, (x0, y0, x1, y1))
    d.rectangle([ox + x0 * Z, oy + y0 * Z, ox + (x1 + 1) * Z, oy + (y1 + 1) * Z], outline=(255, 140, 0), width=3)
    d.text((ox + x0 * Z + 3, oy + y0 * Z + 2), lab.split(':')[0], fill=(255, 140, 0), font=FB)
d.text((ox, 6), 'Foto 1 (onderlaag, 10 foto-px = 1 spritepixel) + silhouet (rood). Oranje = bewuste afwijking, zie legenda.', fill='black', font=FB)
# silhouet los op raster
ox2 = ox + W + 40
s = Image.new('RGB', (W, W), (236, 236, 230)); ds = ImageDraw.Draw(s)
for y in range(64):
    for x in range(64):
        if M[y][x]: ds.rectangle([x * Z, y * Z, x * Z + Z - 1, y * Z + Z - 1], fill=(40, 30, 60))
out.paste(s, (ox2, oy)); grid(out, ox2, oy, d)
d.text((ox2, 6 + 16), 'silhouet op hetzelfde raster', fill='black', font=FB)
# rechterkolom: foto 5 (gespiegeld), foto 3 bek (gespiegeld), legenda
ox3 = ox2 + W + 40
f5 = Image.open(REF + 'jordi_5_uitvlieger_hand.webp').convert('RGB').crop((480, 760, 900, 1120)).transpose(Image.FLIP_LEFT_RIGHT).resize((300, 257))
f3 = Image.open(REF + 'jordi_3_nestjongen.png').convert('RGB').crop((60, 235, 200, 345)).transpose(Image.FLIP_LEFT_RIGHT).resize((300, 236))
out.paste(f5, (ox3, oy)); d.text((ox3, oy + 260), 'foto 5 gespiegeld: kop+lijf een bol, dons', fill='black', font=F)
out.paste(f3, (ox3, oy + 280)); d.text((ox3, oy + 520), 'foto 3 gespiegeld: bedelbek, brede basis', fill='black', font=F)
ty = oy + 545
for x0, y0, x1, y1, lab in ZONES:
    for i in range(0, len(lab), 52):
        d.text((ox3, ty), lab[i:i + 52], fill=(200, 100, 0), font=F); ty += 12
    ty += 4
out.save(sys.argv[1] if len(sys.argv) > 1 else 'overtrekvel.png')
