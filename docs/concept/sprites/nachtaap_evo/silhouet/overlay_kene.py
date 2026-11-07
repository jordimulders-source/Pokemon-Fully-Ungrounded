import os, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
def ov(sprite, mask, z=7):
    im = Image.open(sprite).convert('RGBA'); bg = Image.new('RGBA', (64, 64), (240, 240, 244, 255)); bg.alpha_composite(im)
    big = bg.convert('RGB').resize((64 * z, 64 * z), Image.NEAREST); d = ImageDraw.Draw(big)
    for y in range(64):
        for x in range(64):
            if mask[y, x]:
                for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < 64 and 0 <= ny < 64 and mask[ny, nx]):
                        if dx == 1: d.line([((x+1)*z-1, y*z), ((x+1)*z-1, (y+1)*z-1)], fill=(230, 30, 30), width=2)
                        if dx == -1: d.line([(x*z, y*z), (x*z, (y+1)*z-1)], fill=(230, 30, 30), width=2)
                        if dy == 1: d.line([(x*z, (y+1)*z-1), ((x+1)*z-1, (y+1)*z-1)], fill=(230, 30, 30), width=2)
                        if dy == -1: d.line([(x*z, y*z), ((x+1)*z-1, y*z)], fill=(230, 30, 30), width=2)
    return big.crop((12 * z, 20 * z, 52 * z, 50 * z))
if __name__ == '__main__':
    sprite, mask, out, title = sys.argv[1], np.load(sys.argv[2]), sys.argv[3], sys.argv[4]
    a = ov(sprite, mask); o = Image.new('RGB', (a.width, a.height + 24), 'white'); o.paste(a, (0, 24))
    ImageDraw.Draw(o).text((6, 4), title, font=F, fill=(30, 30, 30)); o.save(out)
