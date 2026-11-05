"""closeup.png: 16x per gewijzigde zone: render | oud | r5 (kop rechts: render | r2 | r4 | r5)."""
from PIL import Image, ImageDraw
Z = 16
def schoon(p):
    s = Image.open(p).convert('RGBA'); px = s.load()
    for y in range(64):
        for x in range(64):
            if px[x, y][:3] == (152, 208, 160): px[x, y] = (220, 220, 220, 255)
    return s
REN = Image.open('../../blender/B1/b1.png').convert('RGBA')
R2 = schoon('../kleur_r2/picapau.png'); R4 = schoon('../kleur_r4/picapau.png'); R5 = schoon('picapau.png')
DELEN = [('kop rechts + kuif (render | r2 | r4 | r5)', 26, 2, 43, 25, [R2, R4, R5]),
         ('lijfvolume borst/buik/dij (render | r4 | r5)', 22, 27, 47, 47, [R4, R5]),
         ('vleugel, ongewijzigd (render | r4 | r5)', 32, 23, 51, 47, [R4, R5]),
         ('tenen (render | r4 | r5)', 24, 43, 40, 51, [R4, R5])]
tegels = []
for naam, x0, y0, x1, y1, ims in DELEN:
    W, H = (x1 - x0) * Z, (y1 - y0) * Z
    bg = Image.new('RGBA', (W, H), (220, 220, 220, 255)); bg.alpha_composite(REN.crop((x0*8, y0*8, x1*8, y1*8)).resize((W, H), Image.LANCZOS))
    rij = [bg] + [s.crop((x0, y0, x1, y1)).resize((W, H), Image.NEAREST) for s in ims]
    for t in rij:
        dt = ImageDraw.Draw(t)
        for x in range(x0, x1 + 1):
            if x % 5 == 0: dt.line([((x - x0) * Z, 0), ((x - x0) * Z, H)], fill=(120, 120, 255))
        for y in range(y0, y1 + 1):
            if y % 5 == 0: dt.line([(0, (y - y0) * Z), (W, (y - y0) * Z)], fill=(120, 120, 255))
    tegels.append((naam + f'  (x{x0}-{x1}, r{y0}-{y1}; blauwe lijnen om de 5 px)', rij))
BW = max(sum(t.size[0] + 20 for t in ims) for _, ims in tegels); BH = sum(ims[0].size[1] + 30 for _, ims in tegels)
v = Image.new('RGBA', (BW, BH), (255, 255, 255, 255)); d = ImageDraw.Draw(v); y = 0
for naam, ims in tegels:
    d.text((4, y + 2), naam, fill=(0, 0, 0)); x = 0
    for im in ims:
        v.alpha_composite(im, (x, y + 16)); x += im.size[0] + 20
    y += ims[0].size[1] + 30
v.save('closeup.png')
