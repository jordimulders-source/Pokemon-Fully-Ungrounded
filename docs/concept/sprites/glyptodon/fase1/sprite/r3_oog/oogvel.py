# oogvel: model | r2 | varianten, kop-uitsnede op 12x, plus 2x van de hele kop op licht
import numpy as np, sys
from PIL import Image, ImageDraw
D = __file__.rsplit('/', 2)[0]
src = open(D + '/vel.py').read().split('# rij 1')[0]
src = src.replace("D = __file__.rsplit('/', 1)[0]", f"D = {D!r}").replace("spr_f, uit = sys.argv[1], sys.argv[2]", "spr_f = D + \"/r2.png\"").replace("float(sys.argv[3]) if len(sys.argv) > 3 else 0.6", "0.6")
exec(src)
box = (6, 42, 18, 53); z = 12
lijst = [('r2', D + '/r2.png'), ('A_180', D + '/r3_oog/r3_A_180.png'), ('B_hor', D + '/r3_oog/r3_B_hor.png'), ('C_ver', D + '/r3_oog/r3_C_ver.png')]
ims = [('model', raster(modeluitsnede(*box, z), z))]
for n, f in lijst:
    s = rgba(f); ims.append((n, raster(op((255, 255, 255, 255), s.crop(box)).resize(((box[2]-box[0])*z, (box[3]-box[1])*z), Image.NEAREST), z)))
w, h = ims[0][1].size
v = Image.new('RGB', (len(ims)*(w+10), h + 20 + 150), 'white'); d = ImageDraw.Draw(v)
for k, (n, im) in enumerate(ims):
    v.paste(im, (k*(w+10), 18)); d.text((k*(w+10)+2, 2), n, fill=(200, 0, 0))
for k, (n, f) in enumerate(lijst):
    s = op((248, 248, 240, 255), rgba(f)).crop((0, 26, 64, 64)).resize((128, 76), Image.NEAREST)
    v.paste(s, ((k+1)*(w+10), h + 25))
    s1 = op((248, 248, 240, 255), rgba(f)).crop((0, 26, 64, 64))
    v.paste(s1, ((k+1)*(w+10), h + 25 + 85))
v.save(D + '/r3_oog/oog_varianten_12x.png'); print(v.size)
