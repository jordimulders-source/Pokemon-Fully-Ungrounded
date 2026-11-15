# vel: sprite 8x | model op dezelfde schaal | kop 12x sprite naast model | 1x op licht en donker
import numpy as np
from PIL import Image, ImageDraw
S = Image.open('steenjaguar_r1.png').convert('RGBA')
nat = Image.open('../natief_zonder_wangoog.png').convert('RGB')
bb = S.getbbox()                    # sprite x0 = i - 4 + 2, y0 = j - 11 + 15  (raster i,j)
W, H = 1600, 900
v = Image.new('RGB', (W, H), (236, 236, 236)); d = ImageDraw.Draw(v)
s8 = S.resize((512, 512), Image.NEAREST); v.paste(s8, (10, 30), s8); d.text((10, 10), 'sprite 8x (64x64)', fill=(0, 0, 0))
m = nat.crop((4, 0, 132, 128)).resize((512, 512), Image.NEAREST)   # model: 1 natieve px = 4 = halve spritepixel op 8x
mm = Image.new('RGB', (512, 512), (255, 255, 255)); mm.paste(m.crop((0, 0, 512, 512)), (0, 0))
# lijn het model uit op de sprite: raster i -> sprite x = i-2 ; natief x = 2i -> op 4x: 8i ; sprite 8x x = 8(i-2)
mod = nat.resize((132 * 4, 132 * 4), Image.NEAREST)
off_x = -8 * 2 - 0; off_y = 8 * (15 - 11)
canvas = Image.new('RGB', (512, 512), (255, 255, 255)); canvas.paste(mod, (8 * (-2), 8 * 4))
v.paste(canvas, (532, 30)); d.text((532, 10), 'model (natief raster) zelfde schaal', fill=(0, 0, 0))
# kop 12x: raster j 11..35, i 3..27 -> sprite x = i-2, y = j+4
ks = S.crop((1, 15, 25, 39)).resize((288, 288), Image.NEAREST)
km = nat.crop((6, 22, 54, 70)).resize((288, 288), Image.NEAREST)
v.paste(Image.new('RGB', (288, 288), (255, 255, 255)), (1054, 30)); v.paste(ks, (1054, 30), ks); v.paste(km, (1054, 330))
d.text((1054, 10), 'kop 12x: sprite (boven) / model (onder)', fill=(0, 0, 0))
# 1x en 2x op licht en donker
for k, bgc in enumerate([(248, 248, 248), (40, 44, 52)]):
    x0 = 1360; y0 = 30 + k * 200
    d.rectangle([x0, y0, x0 + 230, y0 + 180], fill=bgc)
    v.paste(S, (x0 + 10, y0 + 10), S); s2 = S.resize((128, 128), Image.NEAREST); v.paste(s2, (x0 + 90, y0 + 30), s2)
d.text((1360, 10), '1x en 2x op licht en donker', fill=(0, 0, 0))
v.save('vel.png')
