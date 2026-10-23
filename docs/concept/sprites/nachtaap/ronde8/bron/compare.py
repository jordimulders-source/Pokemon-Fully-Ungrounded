# Vergelijkingsvel: nachtaap ronde 8 naast 5 echte Gen 3-sprites, op 1x en 3x, plus metingen.
import sys
from PIL import Image, ImageDraw

R = '/home/user/projectgrounded/.claude/worktrees/agent-ab9a9a71a2e83a756/'
REFS = ['jigglypuff', 'aipom', 'espeon', 'abra', 'smoochum']


def load(path):
    im = Image.open(path)
    im.info['transparency'] = 0
    return im.convert('RGBA').crop((0, 0, 64, 64))


def metrics(im):
    px = im.load()
    solid = lambda x, y: 0 <= x < 64 and 0 <= y < 64 and px[x, y][3] > 0
    area = sum(solid(x, y) for x in range(64) for y in range(64))
    edge = dark = 0
    for y in range(64):
        for x in range(64):
            if solid(x, y) and not all(solid(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                edge += 1
                r, g, b, _ = px[x, y]
                if r + g + b < 160:
                    dark += 1
    return area, dark / edge


def main(out):
    sprites = [('nachtaap r8', load(R + 'docs/concept/sprites/nachtaap/ronde8/anim_front.png'))]
    sprites += [(n, load(R + f'graphics/pokemon/{n}/anim_front_gba.png')) for n in REFS]
    bg = (232, 240, 232, 255)
    W = Image.new('RGBA', (len(sprites) * 200, 64 + 192 + 40), bg)
    d = ImageDraw.Draw(W)
    for i, (n, im) in enumerate(sprites):
        a, k = metrics(im)
        W.alpha_composite(im, (i * 200 + 68, 0))
        W.alpha_composite(im.resize((192, 192), Image.NEAREST), (i * 200 + 4, 64))
        d.text((i * 200 + 6, 64 + 194), f'{n}', fill=(0, 0, 0, 255))
        d.text((i * 200 + 6, 64 + 208), f'{a} px, zwart rand {k:.2f}', fill=(0, 0, 0, 255))
        print(n, a, round(k, 2))
    W.save(out)


if __name__ == '__main__':
    main(sys.argv[1])
