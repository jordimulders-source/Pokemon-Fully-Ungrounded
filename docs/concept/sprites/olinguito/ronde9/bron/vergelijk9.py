"""vergelijk9.py <soortmap> ref1 ref2 ref3 : compare.png met ronde 8, ronde 9 en 3 echte Gen 3-sprites, 1x en 3x."""
import sys, os
from PIL import Image, ImageDraw
REPO = '/home/user/projectgrounded/.claude/worktrees/agent-a8826cf9ffddf4d78'
d = sys.argv[1]
items = [('ronde 8', os.path.join(d, 'ronde8/anim_front.png')), ('ronde 9', os.path.join(d, 'ronde9/anim_front.png'))]
items += [(n, os.path.join(REPO, 'graphics/pokemon', n, 'anim_front_gba.png')) for n in sys.argv[2:]]
BG = (232, 232, 224)
W = 64 * 3 + 12
cv = Image.new('RGB', (W * len(items), 64 + 64 * 3 + 24), BG)
dr = ImageDraw.Draw(cv)
for i, (n, p) in enumerate(items):
    t = Image.open(p)
    idx = t.crop((0, 0, 64, 64))
    im = idx.convert('RGB')
    px, ip = im.load(), idx.load()
    for y in range(64):
        for x in range(64):
            if ip[x, y] == 0:
                px[x, y] = BG
    x0 = i * W
    cv.paste(im, (x0 + 70, 2))
    cv.paste(im.resize((192, 192), Image.NEAREST), (x0 + 6, 68))
    dr.text((x0 + 8, 262), n, fill=(40, 40, 40))
cv.save(os.path.join(d, 'ronde9/compare.png'))
