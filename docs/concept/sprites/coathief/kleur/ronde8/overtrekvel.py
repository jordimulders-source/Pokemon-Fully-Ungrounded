"""Overtrekvel voor de voorpoten (Jordi, 25 okt: "blijf vooral naar de meest linkse kijken, daar zijn de lijnen van de
poten echt perfect. De sprites wijken daar telkens net teveel van af"). De onderlaag (zelfde render, zelfde coördinaten
als de sprite: 4 onderlaag-px = 1 spritepixel) met een 64-raster en spritecoördinaten, naast de huidige sprite op
hetzelfde raster. Zone x 8-35, y 44-63."""
from PIL import Image, ImageDraw, ImageFont
X0, X1, Y0, Y1, Z = 8, 36, 44, 64, 24
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
u = Image.open('silhouet/onderlaag_b1c_256.png').convert('RGB').crop((X0 * 4, Y0 * 4, X1 * 4, Y1 * 4))
u = u.resize(((X1 - X0) * Z, (Y1 - Y0) * Z), Image.LANCZOS)
s = Image.open('kleur/ronde7b/coathief.png').convert('RGBA').crop((X0, Y0, X1, Y1)).resize(((X1 - X0) * Z, (Y1 - Y0) * Z), Image.NEAREST)
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
out.save('kleur/ronde8/overtrekvel.png')
