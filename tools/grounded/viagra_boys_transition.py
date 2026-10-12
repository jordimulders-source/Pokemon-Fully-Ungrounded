"""Viagra Boys-logo (yin-yang met V en B) voor de transitie van Youngster Calvin (Route 102).
Bron: Jordi's logo (scratchpad). Maakt graphics/battle_transitions/viagra_boys.png (64x64, 4bpp: 0 transparant,
1 wit, 2 zwart) en viagra_boys_bg.png (2 tiles: leeg + vlak in kleur 1)."""
import sys
from PIL import Image
src = sys.argv[1]
im = Image.open(src).convert('L')
w, h = im.size
# cirkel zoeken: bounding box van de lichte pixels
px = im.load()
xs = [x for x in range(w) for y in range(0, h, 4) if px[x, y] > 128]
ys = [y for y in range(h) for x in range(0, w, 4) if px[x, y] > 128]
x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
side = max(x1 - x0, y1 - y0)
cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
crop = im.crop((int(cx - side / 2), int(cy - side / 2), int(cx + side / 2), int(cy + side / 2))).resize((62, 62), Image.LANCZOS)
out = Image.new('P', (64, 64), 0)
pal = [255, 0, 255, 247, 247, 247, 16, 16, 16] + [0] * (3 * 13)
out.putpalette(pal)
for y in range(62):
    for x in range(62):
        dx, dy = x - 30.5, y - 30.5
        if dx * dx + dy * dy > 31 * 31:
            continue
        out.putpixel((x + 1, y + 1), 1 if crop.getpixel((x, y)) > 128 else 2)
out.save('graphics/battle_transitions/viagra_boys.png')
bg = Image.new('P', (16, 8), 0)
bg.putpalette([0, 0, 0, 16, 16, 16] + [0] * (3 * 14))
for y in range(8):
    for x in range(8, 16):
        bg.putpixel((x, y), 1)
bg.save('graphics/battle_transitions/viagra_boys_bg.png')
print('ok')
