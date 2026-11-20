# kijk.py in.png uit.png [K]: 8x (of K) op grijs, met 1x en 2x op licht/donker eronder
import sys, numpy as np; from PIL import Image
f, o = sys.argv[1], sys.argv[2]; K = int(sys.argv[3]) if len(sys.argv) > 3 else 8
im = Image.open(f); a = np.asarray(im)[:64]; pal = np.array(im.getpalette()[:768]).reshape(-1,3)
rgba = np.zeros(a.shape+(4,), 'uint8'); rgba[..., :3] = pal[a]; rgba[..., 3] = (a != 0)*255
s = Image.fromarray(rgba, 'RGBA')
W = Image.new('RGBA', (64*K, 64*K+140), (200,200,200,255))
W.alpha_composite(s.resize((64*K, 64*K), Image.NEAREST))
for j, bg in enumerate([(248,248,248), (40,40,48)]):
    b = Image.new('RGBA', (64,64), bg+(255,)); b.alpha_composite(s); W.paste(b, (8+j*72, 64*K+8))
    b = Image.new('RGBA', (128,128), bg+(255,)); b.alpha_composite(s.resize((128,128), Image.NEAREST)); W.paste(b, (160+j*136, 64*K+8))
W.save(o)
