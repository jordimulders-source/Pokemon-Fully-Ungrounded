# vel r3: r3A 8x | basis (r2 + keuring MOET/MAG) 8x | model zelfde schaal | oog A/B 16x | 1x en 2x op licht en donker
from PIL import Image, ImageDraw
A = Image.open('steenjaguar_r3_A.png').convert('RGBA'); B = Image.open('steenjaguar_r3_B.png').convert('RGBA')
basis = Image.open('../r2/keuring/voorstel_moet_mag.png').convert('RGBA')
nat = Image.open('../natief_zonder_wangoog.png').convert('RGB')
v = Image.new('RGB', (1580, 840), (236, 236, 236)); d = ImageDraw.Draw(v)
for k, (im, t) in enumerate([(A, 'r3 A (zonder wenkbrauw) 8x'), (basis, 'basis: r2 + keuring 8x')]):
    s8 = im.resize((512, 512), Image.NEAREST); v.paste(s8, (10 + k * 522, 30), s8); d.text((10 + k * 522, 10), t, fill=(0, 0, 0))
canvas = Image.new('RGB', (512, 512), (255, 255, 255)); canvas.paste(nat.resize((528, 528), Image.NEAREST), (-16, 32))
v.paste(canvas, (1054, 30)); d.text((1054, 10), 'model (natief raster), zelfde schaal', fill=(0, 0, 0))
for k, (im, t) in enumerate([(A, 'oog A'), (B, 'oog B (wenkbrauw)')]):
    c = im.crop((8, 15, 18, 24)).resize((160, 144), Image.NEAREST)
    x0 = 10 + k * 180; v.paste(Image.new('RGB', (160, 144), (255, 255, 255)), (x0, 580)); v.paste(c, (x0, 580), c); d.text((x0, 562), t + ' 16x', fill=(0, 0, 0))
for k, bgc in enumerate([(248, 248, 248), (40, 44, 52)]):
    x0 = 400 + k * 330; y0 = 580
    d.rectangle([x0, y0, x0 + 310, y0 + 180], fill=bgc)
    v.paste(A, (x0 + 10, y0 + 10), A); v.paste(B, (x0 + 10, y0 + 90), B)
    s2 = A.resize((128, 128), Image.NEAREST); v.paste(s2, (x0 + 120, y0 + 30), s2)
d.text((400, 562), '1x (A boven, B onder) en 2x A, op licht en donker', fill=(0, 0, 0))
v.save('vel.png')
