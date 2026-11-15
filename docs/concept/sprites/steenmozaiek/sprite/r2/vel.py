# vel r2: r2 8x | r1 8x | model zelfde schaal ; kop 12x r2 / model ; 1x en 2x op licht en donker
from PIL import Image, ImageDraw
S = Image.open('steenjaguar_r2.png').convert('RGBA'); R1 = Image.open('../r1/steenjaguar_r1.png').convert('RGBA')
nat = Image.open('../natief_zonder_wangoog.png').convert('RGB')
v = Image.new('RGB', (1960, 940), (236, 236, 236)); d = ImageDraw.Draw(v)
for k, (im, t) in enumerate([(S, 'r2 8x'), (R1, 'r1 8x')]):
    s8 = im.resize((512, 512), Image.NEAREST); v.paste(s8, (10 + k * 522, 30), s8); d.text((10 + k * 522, 10), t, fill=(0, 0, 0))
canvas = Image.new('RGB', (512, 512), (255, 255, 255)); canvas.paste(nat.resize((528, 528), Image.NEAREST), (-16, 32))
v.paste(canvas, (1054, 30)); d.text((1054, 10), 'model (natief raster), zelfde schaal', fill=(0, 0, 0))
ks = S.crop((1, 15, 25, 39)).resize((288, 288), Image.NEAREST); km = nat.crop((6, 22, 54, 70)).resize((288, 288), Image.NEAREST)
v.paste(Image.new('RGB', (288, 288), (255, 255, 255)), (1576, 30)); v.paste(ks, (1576, 30), ks); v.paste(km, (1576, 330))
d.text((1576, 10), 'kop 12x: r2 (boven) / model (onder)', fill=(0, 0, 0))
for k, bgc in enumerate([(248, 248, 248), (40, 44, 52)]):
    x0 = 10 + k * 260; y0 = 580
    d.rectangle([x0, y0, x0 + 240, y0 + 180], fill=bgc)
    v.paste(S, (x0 + 10, y0 + 10), S); s2 = S.resize((128, 128), Image.NEAREST); v.paste(s2, (x0 + 100, y0 + 30), s2)
d.text((10, 560), 'r2 1x en 2x op licht en donker', fill=(0, 0, 0))
v.save('vel.png')
