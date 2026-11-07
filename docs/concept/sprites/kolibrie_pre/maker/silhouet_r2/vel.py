"""r2: uitsnede r1 | r2 (8x met raster, zone x<=22 y8-23 in oranje), en vel 4x/1x naast foto 3 (gespiegeld)."""
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
BG, INK = (236, 236, 230), (40, 30, 60)
def load(p):
    rows = [l.rstrip('\n') for l in open(p)][:64]
    im = Image.new('RGB', (64, 64), BG)
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c == '#': im.putpixel((x, y), INK)
    return im
r1, r2 = load('../silhouet_r1/silhouet.txt'), load('silhouet.txt')
# uitsnede x4-37, y6-30 op 8x
X0, Y0, X1, Y1, Z = 4, 6, 38, 30, 8
W, H = (X1 - X0) * Z, (Y1 - Y0) * Z
out = Image.new('RGB', (2 * W + 90, H + 50), 'white'); d = ImageDraw.Draw(out)
for i, (im, t) in enumerate(((r1, 'r1'), (r2, 'r2'))):
    ox, oy = 30 + i * (W + 30), 30
    out.paste(im.crop((X0, Y0, X1, Y1)).resize((W, H), Image.NEAREST), (ox, oy)); d.text((ox, 4), t, fill='black', font=F)
    for k, x in enumerate(range(X0, X1 + 1)):
        d.line([(ox + k * Z, oy), (ox + k * Z, oy + H)], fill=(40, 90, 200) if x % 4 == 0 else (170, 190, 230))
        if x % 4 == 0 and x < X1: d.text((ox + k * Z + 1, 16), str(x), fill=(40, 90, 200), font=F)
    for k, y in enumerate(range(Y0, Y1 + 1)):
        d.line([(ox, oy + k * Z), (ox + W, oy + k * Z)], fill=(40, 90, 200) if y % 4 == 0 else (170, 190, 230))
        if i == 0 and y % 4 == 0 and y < Y1: d.text((4, oy + k * Z + 1), str(y), fill=(40, 90, 200), font=F)
    d.rectangle([ox, oy + (8 - Y0) * Z, ox + (23 - X0) * Z, oy + (24 - Y0) * Z], outline=(255, 140, 0), width=2)
out.save('uitsnede_r1_r2.png')
# vel: r2 4x, 1x, naast foto 3 (gespiegeld) en r1 1x
f3 = Image.open('../../referenties/jordi_3_nestjongen.png').convert('RGB').crop((60, 235, 200, 345)).transpose(Image.FLIP_LEFT_RIGHT).resize((256, 201))
v = Image.new('RGB', (256 + 20 + 256 + 20 + 160, 300), 'white'); d = ImageDraw.Draw(v)
v.paste(r2.resize((256, 256), Image.NEAREST), (0, 24)); d.text((0, 4), 'r2 4x', fill='black', font=F)
v.paste(f3, (276, 24)); d.text((276, 4), 'foto 3 (gespiegeld)', fill='black', font=F)
v.paste(r2, (552, 60)); d.text((552, 40), 'r2 1x', fill='black', font=F)
v.paste(r1, (552, 170)); d.text((552, 150), 'r1 1x', fill='black', font=F)
v.save('vel.png')
