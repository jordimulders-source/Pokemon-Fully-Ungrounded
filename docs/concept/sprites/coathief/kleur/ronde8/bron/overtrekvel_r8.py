"""Overtrekvel voor de voorpoten (Jordi, 25 okt: "blijf vooral naar de meest linkse kijken, daar zijn de lijnen van de
poten echt perfect. De sprites wijken daar telkens net teveel van af"). De onderlaag (zelfde render, zelfde coördinaten
als de sprite: 4 onderlaag-px = 1 spritepixel) met een 64-raster en spritecoördinaten, naast de huidige sprite op
hetzelfde raster. Zone x 8-35, y 44-63."""
from PIL import Image, ImageDraw, ImageFont
X0, X1, Y0, Y1, Z = 8, 36, 44, 64, 24
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
u = Image.open('silhouet/onderlaag_b1c_256.png').convert('RGB').crop((X0 * 4, Y0 * 4, X1 * 4, Y1 * 4))
u = u.resize(((X1 - X0) * Z, (Y1 - Y0) * Z), Image.LANCZOS)
s = Image.open('kleur/ronde8/coathief.png').convert('RGBA').crop((X0, Y0, X1, Y1)).resize(((X1 - X0) * Z, (Y1 - Y0) * Z), Image.NEAREST)
sb = Image.new('RGBA', s.size, (236, 236, 230, 255)); sb.alpha_composite(s); s = sb.convert('RGB')
W, H = (X1 - X0) * Z, (Y1 - Y0) * Z
out = Image.new('RGB', (2 * W + 60, H + 40), (255, 255, 255)); d = ImageDraw.Draw(out)
for i, im in enumerate((u, s)):
    ox = 30 + i * (W + 10); out.paste(im, (ox, 20))
    for k, x in enumerate(range(X0, X1 + 1)):
        d.line([(ox + k * Z, 20), (ox + k * Z, 20 + H)], fill=(120, 160, 220) if x % 4 else (40, 90, 200), width=1)
        if x % 2 == 0 and x < X1: d.text((ox + k * Z + 4, 4), str(x), fill=(40, 90, 200), font=F)
    for k, y in enumerate(range(Y0, Y1 + 1)):
        d.line([(ox, 20 + k * Z), (ox + W, 20 + k * Z)], fill=(120, 160, 220) if y % 4 else (40, 90, 200), width=1)
        if i == 0 and y < Y1: d.text((4, 20 + k * Z + 6), str(y), fill=(40, 90, 200), font=F)
out.save('kleur/ronde8/overtrekvel_r8.png')
# afwijkingen van de onderlaag (alleen waar 1x anders niet leest), rood omkaderd op beide helften + legenda
AFW = {(20, 58): 'lucht tussen de hangende klauwen (onderlaag: zwarte rand)',
       (21, 59): 'punt rechterklauw 1 px naar rechts: blijft vast aan de klauw',
       (18, 60): 'puntje van 1 px weggelaten (leest als kruimel)',
       (20, 60): 'puntje van 1 px weggelaten (leest als kruimel)',
       (25, 60): 'donkere scheiding tussen de klauwen van de staande voet',
       (25, 61): 'donkere scheiding tussen de klauwen van de staande voet',
       (25, 62): 'lucht onder de scheiding',
       (24, 63): 'puntje van 1 px weggelaten'}
out = Image.open('kleur/ronde8/overtrekvel_r8.png'); W0, H0 = out.size
JORDI = [(28, 52), (28, 53), (32, 54), (32, 55), (32, 56), (27, 57), (27, 58)]
KEUZE = ['groen = Jordi\'s cellen (vaste eis): (28,52) (28,53) donker; (32,54-56) poot; (27,57-58) zaten al in ronde 8.',
         '(32,53) NIET toegevoegd: de rechterrand van de staande poot ligt in de onderlaag op y 53 bij x 31,5-31,75,',
         '   dus binnen cel 31, niet in cel 32 (vanaf y 55,9 komt de onderlaag tot x 32).']
big = Image.new('RGB', (W0, H0 + 20 + 14 * (len(AFW) + len(KEUZE) + 1)), (255, 255, 255)); big.paste(out, (0, 0)); d = ImageDraw.Draw(big)
for (x, y), t in AFW.items():
    for i in range(2):
        ox = 30 + i * (W + 10)
        d.rectangle([ox + (x - X0) * Z + 1, 20 + (y - Y0) * Z + 1, ox + (x - X0 + 1) * Z - 1, 20 + (y - Y0 + 1) * Z - 1], outline=(230, 0, 0), width=2)
for (x, y) in JORDI:
    for i in range(2):
        ox = 30 + i * (W + 10)
        d.rectangle([ox + (x - X0) * Z + 4, 20 + (y - Y0) * Z + 4, ox + (x - X0 + 1) * Z - 4, 20 + (y - Y0 + 1) * Z - 4], outline=(0, 170, 0), width=2)
for k, t in enumerate(KEUZE):
    d.text((30, H0 + 6 + 14 * (len(AFW) + 1 + k)), t, fill=(0, 120, 0), font=F)
for k, ((x, y), t) in enumerate(AFW.items()):
    d.text((30, H0 + 6 + 14 * k), '(%d,%d): %s' % (x, y, t), fill=(200, 0, 0), font=F)
big.save('kleur/ronde8/overtrekvel_r8.png')
