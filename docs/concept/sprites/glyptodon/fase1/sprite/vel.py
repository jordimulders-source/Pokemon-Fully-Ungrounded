# Vel: sprite 8x | model op dezelfde schaal 8x; close-ups kop/nek en staart op 12x naast het model; 1x op licht en donker.
# gebruik: python3 vel.py sprite.png uit.png [S]
import sys, numpy as np
from PIL import Image, ImageDraw
D = __file__.rsplit('/', 1)[0]
spr_f, uit = sys.argv[1], sys.argv[2]
S = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
X0, Y0 = 10, 24           # bbox-hoek van het model op het natieve raster
W, H = int(np.ceil(85 * S)), int(np.ceil(52 * S))
OX, OY = (64 - W) // 2, 64 - H - 4
P = 10.24 / S              # modelpixels per spritepixel
model = Image.fromarray(np.load(D + '/nat.npy')).resize((1024, 1024), Image.NEAREST).convert('RGBA')  # natief raster, scherp

def rgba(f):
    im = Image.open(f)
    if im.mode == 'P':
        a = np.array(im); pal = np.array(im.getpalette()[:48]).reshape(16, 3)
        rgb = pal[a]; al = (a != 0) * 255
        return Image.fromarray(np.dstack([rgb, al]).astype('uint8'), 'RGBA')
    return im.convert('RGBA')

spr = rgba(spr_f)
def op(bg, im):
    b = Image.new('RGBA', im.size, bg); b.alpha_composite(im); return b

def modeluitsnede(sx0, sy0, sx1, sy1, z):
    # spritecoordinaten -> modelpixels
    mx0 = (X0 + (sx0 - OX) / S) * 10.24; my0 = (Y0 + (sy0 - OY) / S) * 10.24
    mx1 = (X0 + (sx1 - OX) / S) * 10.24; my1 = (Y0 + (sy1 - OY) / S) * 10.24
    c = model.crop((int(mx0), int(my0), int(mx1), int(my1)))
    return op((255, 255, 255, 255), c.resize(((sx1 - sx0) * z, (sy1 - sy0) * z), Image.NEAREST))

def raster(im, z):
    d = ImageDraw.Draw(im)
    for k in range(0, im.width, z): d.line([(k, 0), (k, im.height)], fill=(200, 200, 200, 255))
    for k in range(0, im.height, z): d.line([(0, k), (im.width, k)], fill=(200, 200, 200, 255))
    return im

# rij 1: hele sprite 8x | model
bb = (OX - 2, OY - 2, OX + W + 2, OY + H + 2)
s8 = op((255, 255, 255, 255), spr.crop(bb)).resize(((bb[2]-bb[0]) * 8, (bb[3]-bb[1]) * 8), Image.NEAREST)
m8 = modeluitsnede(*bb, 8)
# close-ups (spritecoordinaten)
kop = (OX - 1, OY + 11, OX + 16, OY + H + 1)
staart = (OX + 37, OY + 10, OX + W + 1, OY + H - 2)
def paar(box, z=12):
    a = raster(op((255, 255, 255, 255), spr.crop(box)).resize(((box[2]-box[0]) * z, (box[3]-box[1]) * z), Image.NEAREST), z)
    b = raster(modeluitsnede(*box, z), z)
    return a, b
k1, k2 = paar(kop); t1, t2 = paar(staart)
een = [op((248, 248, 240, 255), spr), op((40, 48, 64, 255), spr)]

breed = max(s8.width + m8.width + 30, k1.width * 2 + 30 + t1.width * 2 + 30)
hoog = s8.height + 20 + max(k1.height, t1.height) + 20 + 64 * 2 + 30
vel = Image.new('RGBA', (breed, hoog), (255, 255, 255, 255))
vel.paste(s8, (0, 0)); vel.paste(m8, (s8.width + 30, 0))
y = s8.height + 20
vel.paste(k1, (0, y)); vel.paste(k2, (k1.width + 10, y))
x = k1.width * 2 + 40
vel.paste(t1, (x, y)); vel.paste(t2, (x + t1.width + 10, y))
y += max(k1.height, t1.height) + 20
for k, e in enumerate(een):
    vel.paste(e.resize((128, 128), Image.NEAREST), (k * 140, y))
    vel.paste(e, (300 + k * 80, y))
vel.convert('RGB').save(uit)
print(uit, vel.size)
