# Vel r10: r9 8x | r10 8x | model verkleind 8x; close-ups 12x boven en links naast het model; 1x op licht/donker naast Magnemite/Claydol.
import numpy as np
from PIL import Image, ImageDraw
M = Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')
S = 12.703
G = '../../../../../../graphics/pokemon/'

def rgb(p, bg=(255, 255, 255)):
    im = Image.open(p).convert('RGBA'); b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im); return b.convert('RGB')

def model(x0, y0, x1, y1):
    return M.crop(tuple(int(round(v)) for v in (103 + x0 * S, 143 + (y0 - 7) * S, 103 + x1 * S, 143 + (y1 - 7) * S)))

def raster(im, x0, y0, Z):
    d = ImageDraw.Draw(im)
    for i in range(im.width // Z + 1): d.line([(i * Z, 0), (i * Z, im.height)], fill=(255, 0, 0) if (x0 + i) % 5 == 0 else (190, 190, 190))
    for j in range(im.height // Z + 1): d.line([(0, j * Z), (im.width, j * Z)], fill=(255, 0, 0) if (y0 + j) % 5 == 0 else (190, 190, 190))
    return im

def paar(x0, y0, x1, y1, Z=12):
    w, h = (x1 - x0) * Z, (y1 - y0) * Z
    a = raster(rgb('sprite.png').crop((x0, y0, x1, y1)).resize((w, h), Image.NEAREST), x0, y0, Z)
    b = raster(model(x0, y0, x1, y1).resize((w, h), Image.LANCZOS), x0, y0, Z)
    c = Image.new('RGB', (2 * w + 12, h), (120, 120, 120)); c.paste(a, (0, 0)); c.paste(b, (w + 12, 0)); return c

rij1 = [rgb('../r9/sprite.png').resize((512, 512), Image.NEAREST), rgb('sprite.png').resize((512, 512), Image.NEAREST),
        model(0, 0, 64, 64).resize((64, 64), Image.LANCZOS).resize((512, 512), Image.NEAREST)]
top = paar(14, 4, 52, 24); links = paar(0, 14, 30, 40); koep = paar(8, 24, 40, 48)

def mon(p):  # eerste frame van een Gen 3-sprite, transparant = palet 0
    im = Image.open(p).crop((0, 0, 64, 64)); a = np.array(im); r = im.convert('RGBA'); m = np.array(r); m[a == 0, 3] = 0; return Image.fromarray(m)
klein = []
for bg in [(255, 255, 255), (48, 48, 56)]:
    c = Image.new('RGBA', (3 * 72, 72), bg + (255,))
    for i, im in enumerate([Image.open('sprite.png').convert('RGBA'), mon(G + 'magnemite/anim_front_gba.png'), mon(G + 'claydol/anim_front_gba.png')]):
        if i == 0:
            a = np.array(Image.open('sprite.png')); m = np.array(im); m[a == 0, 3] = 0; im = Image.fromarray(m)
        c.alpha_composite(im, (4 + 72 * i, 4))
    klein.append(c.convert('RGB').resize((3 * 72 * 3, 72 * 3), Image.NEAREST))
W = max(3 * 512 + 40, top.width, links.width + koep.width + 20)
H = 512 + 30 + top.height + 20 + max(links.height, 24 * 12) + 20 + 2 * klein[0].height + 30
vel = Image.new('RGB', (W, H), (235, 235, 235)); d = ImageDraw.Draw(vel)
for i, im in enumerate(rij1): vel.paste(im, (i * 532, 20))
d.text((4, 4), 'r9 8x', fill=(0, 0, 0)); d.text((536, 4), 'r10 8x', fill=(0, 0, 0)); d.text((1068, 4), 'model verkleind 8x', fill=(0, 0, 0))
y = 542; d.text((4, y - 14), 'boven 12x (x14-52, y4-24): r10 | model', fill=(0, 0, 0)); vel.paste(top, (0, y)); y += top.height + 20
d.text((4, y - 14), 'links 12x (x0-30, y14-40): r10 | model', fill=(0, 0, 0)); vel.paste(links, (0, y)); d.text((links.width + 24, y - 14), 'koepel 12x (x8-40, y24-48): r10 | model', fill=(0, 0, 0)); vel.paste(koep, (links.width + 20, y)); y += max(links.height, koep.height) + 20
d.text((4, y - 14), '1x (3x vergroot): r10 | Magnemite | Claydol, licht en donker', fill=(0, 0, 0))
vel.paste(klein[0], (0, y)); vel.paste(klein[1], (0, y + klein[0].height + 6))
vel.save('vel.png'); print(vel.size)
