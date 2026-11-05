"""close-up 16x: render-uitsnede | r2 | r3 voor snavel (x12-24, r14-26) en poten (x22-40, r42-51)."""
from PIL import Image, ImageDraw
Z = 16
def uits(x0, y0, x1, y1):
    W, H = (x1 - x0) * Z, (y1 - y0) * Z
    r = Image.open('../../blender/B1/b1.png').convert('RGBA').crop((x0*8, y0*8, x1*8, y1*8)).resize((W, H), Image.LANCZOS)
    bg = Image.new('RGBA', (W, H), (220, 220, 220, 255)); bg.alpha_composite(r); out = [bg]
    for p in ('../kleur_r2/picapau.png', 'picapau.png'):
        s = Image.open(p).convert('RGBA'); px = s.load()
        for y in range(64):
            for x in range(64):
                if px[x, y][:3] == (152, 208, 160): px[x, y] = (220, 220, 220, 255)
        out.append(s.crop((x0, y0, x1, y1)).resize((W, H), Image.NEAREST))
    return out
rows = [uits(12, 14, 24, 26), uits(22, 42, 40, 51)]
W = sum(max(r[i].size[0] for r in rows) for i in range(3)) + 40
H = sum(r[0].size[1] for r in rows) + 60
v = Image.new('RGBA', (W, H), (255, 255, 255, 255)); d = ImageDraw.Draw(v); y = 14
for r in rows:
    x = 0
    for im, n in zip(r, ['render', 'r2', 'r3']):
        v.alpha_composite(im, (x, y)); d.text((x + 2, y - 12), n, fill=(0, 0, 0)); x += im.size[0] + 20
    y += r[0].size[1] + 24
v.save('closeup.png')
