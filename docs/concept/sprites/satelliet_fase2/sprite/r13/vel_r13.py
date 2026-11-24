# vel r13: r12 8x | r13 8x | model 8x ; daaronder r13 2x naast Gen 3 (GBA) op 2x ; 1x op licht en donker
import numpy as np
from PIL import Image, ImageDraw
from studie import laad, NAMEN
M = Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB'); k = 12.703
def mb(x0, y0, x1, y1): return (int(103 + x0 * k), int(143 + (y0 - 7) * k), int(103 + x1 * k), int(143 + (y1 - 7) * k))
m64 = M.crop(mb(0, 0, 64, 64)).resize((512, 512), Image.LANCZOS)
def on(im, bg):
    b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im.convert('RGBA')); return b.convert('RGB')
def gen3(n):
    a, pal = laad(n); rgba = np.zeros((64, 64, 4), 'uint8')
    for y in range(64):
        for x in range(64):
            if a[y, x]: rgba[y, x] = pal[a[y, x]] + (255,)
    return Image.fromarray(rgba)
R12 = Image.open('../r12/sprite.png').convert('RGBA'); R13 = Image.open('sprite.png').convert('RGBA')
W = 3 * 520; out = Image.new('RGB', (W, 1120), (205, 205, 205)); d = ImageDraw.Draw(out)
for i, (n, im) in enumerate((('r12 8x', on(R12, (255, 255, 255)).resize((512, 512), Image.NEAREST)),
                             ('r13 8x', on(R13, (255, 255, 255)).resize((512, 512), Image.NEAREST)),
                             ('model (panelen_80b, verkleind beeld)', m64))):
    out.paste(im, (i * 520, 0)); d.text((i * 520 + 4, 516), n, fill=(0, 0, 0))
y = 540; d.text((4, y), '2x: r13 | Magnemite | Magneton | Claydol | Glalie | Beldum | Metang | Lunatone (Gen 3 GBA)', fill=(0, 0, 0))
sp = [R13] + [gen3(n) for n in NAMEN]
for i, im in enumerate(sp):
    out.paste(on(im, (255, 255, 255)).resize((128, 128), Image.NEAREST), (4 + i * 136, y + 16))
y += 160; d.text((4, y), '1x op licht en donker: r12 | r13 | Gen 3', fill=(0, 0, 0))
for j, bg in enumerate(((255, 255, 255), (40, 40, 48))):
    for i, im in enumerate([R12, R13] + sp[1:]):
        out.paste(on(im, bg), (4 + i * 70, y + 16 + j * 70))
out = out.crop((0, 0, W, y + 16 + 140 + 6)); out.save('vel.png'); print(out.size)
