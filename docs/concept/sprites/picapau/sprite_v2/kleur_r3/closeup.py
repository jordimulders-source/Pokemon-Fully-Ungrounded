"""close-ups 16x per onderdeel: render-uitsnede | r2 | r3 (+ krabbel van Jordi teruggerekend op r3)."""
from PIL import Image, ImageDraw
Z = 16
DELEN = [('1-2 kop + kuif', 18, 2, 42, 26), ('3-4 oog + wang', 20, 15, 32, 29), ('5 snavel + verre oog', 12, 14, 24, 26),
         ('6 borst/buik/dij', 22, 26, 40, 48), ('7 vleugel + stippen', 32, 23, 51, 47), ('8 poten', 22, 42, 40, 51), ('9 staart', 42, 43, 52, 58)]
def schoon(p):
    s = Image.open(p).convert('RGBA'); px = s.load()
    for y in range(64):
        for x in range(64):
            if px[x, y][:3] == (152, 208, 160): px[x, y] = (220, 220, 220, 255)
    return s
REN = Image.open('../../blender/B1/b1.png').convert('RGBA'); R2 = schoon('../kleur_r2/picapau.png'); R3 = schoon('picapau.png')
tegels = []
for naam, x0, y0, x1, y1 in DELEN:
    W, H = (x1 - x0) * Z, (y1 - y0) * Z
    bg = Image.new('RGBA', (W, H), (220, 220, 220, 255)); bg.alpha_composite(REN.crop((x0*8, y0*8, x1*8, y1*8)).resize((W, H), Image.LANCZOS))
    tegels.append((naam, [bg, R2.crop((x0, y0, x1, y1)).resize((W, H), Image.NEAREST), R3.crop((x0, y0, x1, y1)).resize((W, H), Image.NEAREST)]))
BW = max(sum(t.size[0] for t in ims) + 60 for _, ims in tegels); BH = sum(ims[0].size[1] + 30 for _, ims in tegels)
v = Image.new('RGBA', (BW, BH), (255, 255, 255, 255)); d = ImageDraw.Draw(v); y = 0
for naam, ims in tegels:
    d.text((4, y + 2), naam + '   (render | r2 | r3)', fill=(0, 0, 0)); x = 0
    for im in ims:
        v.alpha_composite(im, (x, y + 16)); x += im.size[0] + 20
    y += ims[0].size[1] + 30
v.save('closeup.png')
