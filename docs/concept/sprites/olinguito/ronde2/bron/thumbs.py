"""Drie snelle silhouetten (zwart, 64x64) voor de olinguito ronde 2.
A Zakkenroller (zit, bungelende klauwpoot, munt op schoot, geringde krulstaart, pluk, halsdoekknoop)
B Sluiper (laag op vier poten, Nickit-houding, klauwen vooruit, staart hoog)
C Taxateur (rechtop, munt omhoog tegen het oog, staart als S)
python3 thumbs.py <uit.png>"""
import sys, os
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
import numpy as np
from PIL import Image, ImageDraw
from shapepaint import Canvas

R = {'x': [1, 1, 1, 1]}

def claws(c, n, base, dirs, L=7):
    for k, (bx, by) in enumerate(base):
        dx, dy = dirs[k]
        c.claw('%s%d' % (n, k), [(bx, by), (bx + dx * L * .6, by + dy * L * .6), (bx + dx * L * .6 - dy * 2, by + dy * L)], part='x')

def A():
    c = Canvas(64, 64, R)
    c.tube('staart', 'x', [(38, 52), (47, 50), (52, 43), (53, 34), (51, 27), (47, 23), (43, 23)], [7, 7, 7, 6, 6, 5, 4])
    c.poly('staart', 'x', [(43, 20), (40, 22), (42, 24), (39, 26), (44, 26)])
    c.ellipse('lijf', 'x', 31, 45, 10, 11)
    c.poly('knoop', 'x', [(36, 31), (43, 28), (41, 32), (44, 36), (36, 34)])
    c.ellipse('kop', 'x', 26, 23, 11.5, 10.5)
    c.ellipse('o1', 'x', 17, 14, 3.5, 4); c.ellipse('o2', 'x', 34, 13, 4, 4.5)
    c.poly('pluk', 'x', [(22, 14), (24, 7), (26, 12), (29, 6), (31, 13)])
    c.ellipse('snuit', 'x', 17, 26, 5, 4)
    c.tube('arm', 'x', [(24, 38), (14, 40)], [5, 4]); c.ellipse('hand', 'x', 12, 41, 2.8, 2.6)
    claws(c, 'k', [(10, 43), (12, 43.5), (14, 43)], [(-.3, 1), (0, 1), (.3, 1)])
    c.ellipse('munt', 'x', 27, 49, 4, 4)
    c.ellipse('voet', 'x', 21, 55, 5, 2.5)
    return c

def B():
    c = Canvas(64, 64, R)
    c.tube('staart', 'x', [(44, 44), (50, 36), (52, 26), (49, 18), (44, 16)], [7, 7, 6, 5, 4])
    c.ellipse('lijf', 'x', 36, 46, 13, 7.5)
    c.ellipse('kop', 'x', 18, 40, 10, 9)
    c.ellipse('o1', 'x', 12, 31, 3, 4); c.ellipse('o2', 'x', 24, 31, 3.5, 4)
    c.poly('pluk', 'x', [(15, 32), (18, 26), (20, 31), (23, 27), (24, 33)])
    c.ellipse('snuit', 'x', 10, 43, 4.5, 3.5)
    for i, x in enumerate((22, 30, 42, 47)):
        c.tube('poot%d' % i, 'x', [(x, 50), (x - 1, 56)], [4, 4])
    claws(c, 'k', [(20, 57), (22, 57), (28, 57)], [(-1, .3), (-1, .3), (-1, .3)], L=6)
    return c

def C():
    c = Canvas(64, 64, R)
    c.tube('staart', 'x', [(36, 54), (46, 54), (50, 46), (46, 38), (48, 30), (54, 26)], [6, 6, 6, 5, 5, 4])
    c.ellipse('lijf', 'x', 31, 43, 8.5, 12)
    c.ellipse('kop', 'x', 28, 22, 11, 10)
    c.ellipse('o1', 'x', 20, 13, 3.5, 4); c.ellipse('o2', 'x', 36, 13, 4, 4.5)
    c.poly('pluk', 'x', [(25, 14), (27, 7), (29, 12), (32, 6), (33, 13)])
    c.ellipse('snuit', 'x', 19, 25, 5, 4)
    c.tube('arm', 'x', [(25, 38), (17, 32), (13, 24)], [5, 4, 4])
    c.ellipse('munt', 'x', 11, 18, 4.5, 4.5)
    claws(c, 'k', [(12, 24), (14, 25), (16, 25)], [(-.6, -1), (-.2, -1), (.2, -1)], L=6)
    c.ellipse('voet1', 'x', 25, 56, 5, 2.5); c.ellipse('voet2', 'x', 36, 56, 4, 2.5)
    return c

def sil(c):
    m = np.zeros((64, 64), bool)
    for o in c.objs: m |= o.mask
    return m

if __name__ == '__main__':
    out = sys.argv[1]
    z = 4; names = ['A Zakkenroller', 'B Sluiper', 'C Taxateur']
    sheet = Image.new('RGB', (3 * (64 * z + 8) + 3 * 72, 64 * z + 20), (240, 238, 230)); d = ImageDraw.Draw(sheet)
    for i, f in enumerate((A, B, C)):
        m = sil(f()); a = np.full((64, 64, 3), 240, np.uint8); a[..., 1] = 238; a[..., 2] = 230; a[m] = (20, 20, 20)
        im = Image.fromarray(a)
        sheet.paste(im.resize((64 * z, 64 * z), Image.NEAREST), (i * (64 * z + 8), 16)); d.text((i * (64 * z + 8) + 4, 2), names[i] + '  %d px' % m.sum(), fill=(0, 0, 0))
        sheet.paste(im, (3 * (64 * z + 8) + i * 72, 16))
    sheet.save(out); print(out)
