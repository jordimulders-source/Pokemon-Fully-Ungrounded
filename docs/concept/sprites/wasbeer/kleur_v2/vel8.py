"""Vergelijkingsvel kleur ronde 8 -> vel_ronde8.png.
Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/vel8.py"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.join(HERE, '../../../../../graphics/pokemon')
SP = os.path.join(HERE, '../..')
LICHT, DONKER = (236, 236, 236), (32, 32, 40)


def echt(n):
    im = Image.open(os.path.join(G, n, 'anim_front.png')).crop((0, 0, 64, 64))
    pal = [tuple(int(v) for v in l.split()) for l in open(os.path.join(G, n, 'normal.pal')).read().split('\n')[3:19]]
    o = Image.new('RGBA', (64, 64))
    o.putdata([(0, 0, 0, 0) if i == 0 else pal[i] + (255,) for i in im.getdata()])
    return o


def eigen(p):
    return Image.open(p).convert('RGBA').crop((0, 0, 64, 64))


def op(im, bg, k, box=None, raster=False):
    if box:
        im = im.crop(box)
    b = Image.new('RGBA', im.size, bg + (255,))
    b.alpha_composite(im)
    b = b.resize((im.size[0] * k, im.size[1] * k), Image.NEAREST)
    if raster and k >= 6:
        d = ImageDraw.Draw(b)
        for i in range(0, b.size[0], k):
            d.line([(i, 0), (i, b.size[1])], fill=(200, 200, 225))
        for i in range(0, b.size[1], k):
            d.line([(0, i), (b.size[0], i)], fill=(200, 200, 225))
    return b.convert('RGB')


def main():
    r8 = eigen(os.path.join(HERE, 'ronde8.png'))
    r7 = eigen(os.path.join(HERE, 'ronde7.png'))
    rijen = []
    # 1. ronde 8 en 7 op 4x, licht en donker
    rijen.append(('ronde 8 | ronde 7 (4x, licht) | ronde 8 | ronde 7 (4x, donker)',
                  [op(r8, LICHT, 4), op(r7, LICHT, 4), op(r8, DONKER, 4), op(r7, DONKER, 4)]))
    # 2. uitsneden 8x naast echte sprites
    uit = [
        ('staartpunt: r8 | r7 | sentret | furret', [(r8, (45, 16, 59, 34)), (r7, (45, 16, 59, 34)),
                                                    (echt('sentret'), (14, 40, 34, 60)), (echt('furret'), (0, 20, 20, 46))]),
        ('ogen: r8 | r7 | zigzagoon | mightyena | linoone', [(r8, (9, 6, 27, 16)), (r7, (9, 6, 27, 16)),
                                                             (echt('zigzagoon'), (8, 30, 26, 40)), (echt('mightyena'), (2, 12, 20, 22)),
                                                             (echt('linoone'), (2, 26, 16, 36))]),
        ('oren: r8 | r7 | raticate | teddiursa', [(r8, (11, 0, 31, 8)), (r7, (11, 0, 31, 8)),
                                                  (echt('raticate'), (8, 23, 24, 33)), (echt('teddiursa'), (14, 11, 34, 19))]),
        ('borst/schouder links: r8 | r7 | zangoose | mightyena', [(r8, (9, 15, 25, 32)), (r7, (9, 15, 25, 32)),
                                                               (echt('zangoose'), (14, 26, 32, 44)), (echt('mightyena'), (0, 18, 16, 35))]),
        ('neus: r8 | r7 | zigzagoon | raticate', [(r8, (8, 12, 18, 21)), (r7, (8, 12, 18, 21)),
                                                  (echt('zigzagoon'), (6, 31, 16, 40)), (echt('raticate'), (8, 26, 18, 35))]),
    ]
    for t, lst in uit:
        rijen.append((t + ' (8x)', [op(im, LICHT, 8, box, raster=True) for im, box in lst]))
    # 3. geheel 1x en 2x naast de lijn en 6 Gen 3-sprites
    lijn = [eigen(os.path.join(SP, 'olinguito_v2/af/olinguito.png')), eigen(os.path.join(SP, 'coathief/af/coathief.png')), r8]
    lijn += [echt(n) for n in ('zangoose', 'sneasel', 'linoone', 'mightyena', 'ursaring', 'furret')]
    rijen.append(('1x: olinguito, coathief, ronde 8, zangoose, sneasel, linoone, mightyena, ursaring, furret',
                  [op(i, LICHT, 1) for i in lijn]))
    rijen.append(('2x: idem', [op(i, LICHT, 2) for i in lijn]))
    rijen.append(('2x op donker', [op(i, DONKER, 2) for i in lijn]))
    W = max(sum(i.size[0] + 10 for i in ims) for _, ims in rijen) + 10
    H = sum(max(i.size[1] for i in ims) + 26 for _, ims in rijen) + 10
    vel = Image.new('RGB', (W, H), (255, 255, 255))
    d = ImageDraw.Draw(vel)
    y = 6
    for t, ims in rijen:
        d.text((10, y), t, fill=(0, 0, 0))
        y += 16
        x = 10
        for i in ims:
            vel.paste(i, (x, y))
            x += i.size[0] + 10
        y += max(i.size[1] for i in ims) + 10
    vel.save(os.path.join(HERE, 'vel_ronde8.png'))
    print('vel_ronde8.png', vel.size)


if __name__ == '__main__':
    main()
