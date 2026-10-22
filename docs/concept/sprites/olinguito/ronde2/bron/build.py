"""Olinguito ronde 2 ("Zakkenroller"): bouwt anim_front.png + normal.pal.

  python3 build.py <uitmap>

Vormen + automatische schaduw/selout via tools/concept/sprites/shapepaint.py,
daarna gezicht, munt en details met de hand als ASCII-patches.
"""
import sys, os
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
import numpy as np
from shapepaint import Canvas, patch, fix_outline, save_indexed, save_pal, hexc, hooks

PAL = [hexc(h) for h in [
    '#7BD5A4',  # 0 transparant
    '#C8805A', '#A65A34', '#7A3E2A', '#4E2621',   # 1-4 vacht: hooglicht, BASIS, schaduw, donkerst (selout, plooien, mond)
    '#5A4A5E', '#2E2436',                         # 5-6 donker: handschoenen, sokken, masker, ringen (BASIS 5? zie notities)
    '#EAD2A4', '#B8946A',                         # 7-8 crème: snuit, buik, binnenoor
    '#FFF2C4', '#F5C842', '#B0802C',              # 9-11 goud: ivoor-hooglicht, GOUD (iris, munt, klauwen), schaduw
    '#4A9E58', '#28683E',                         # 12-13 halsdoek: BASIS, schaduw
    '#FFFFFF',                                    # 14 wit: glans, hoektand
    '#101010',                                    # 15 omlijning
]]

RAMPS = {
    'vacht': [1, 2, 3, 4],
    'donker': [5, 5, 6, 6],
    'creme': [7, 7, 8, 8],
    'klauw': [9, 9, 11, 11],
    'munt': [9, 10, 11, 11],
    'doek': [12, 12, 13, 13],
}
K = {'h': 1, 'v': 2, 's': 3, 'd': 4, 'm': 5, 'M': 6, 'c': 7, 'C': 8,
     'i': 9, 'g': 10, 'G': 11, 'n': 12, 'N': 13, 'w': 14, 'o': 15}


def ringed_tail(c, pts, widths, rings, tip):
    o = c.tube('staart', 'vacht', pts, widths, shade=2.5)
    t = o.t

    def paint(x, y, cur):
        tv = t[y, x]
        for a, b in rings:
            if a <= tv < b:
                return 6 if cur in (3, 4) else 5
        return None
    o.paint = paint
    # donkere, getande staartpunt (eigen object zonder lijn ertussen)
    p = c.poly('staartpunt', 'donker', tip, shade=1.5)
    p.paint = None
    return o


def head(c, dy=0):
    c.ellipse('oor1', 'vacht', 17, 14.5 + dy, 3.4, 4.4, rot=-25, shade=2)
    c.poly('oor1', 'vacht', [(14, 13 + dy), (15, 9 + dy), (19, 12 + dy)])
    c.ellipse('oor2', 'vacht', 34.5, 13 + dy, 4, 4.8, rot=25, shade=2)
    c.poly('oor2', 'vacht', [(32, 10 + dy), (37, 7 + dy), (37, 12 + dy)])
    c.ellipse('kop', 'vacht', 26, 23 + dy, 11.5, 10.5, shade=3, hl=(21, 16 + dy, 4))
    # pluk: één naar achteren gestreken lok
    c.poly('kop', 'vacht', [(22, 14 + dy), (25, 9 + dy), (29, 6 + dy), (33, 5 + dy), (31, 8 + dy), (33, 9 + dy), (30, 13 + dy)])
    c.ellipse('snuit', 'creme', 16.5, 26.5 + dy, 5, 3.7, shade=2)


def face(idx, dy=0, closed=False):
    # binnenoren donker
    patch(idx, 15, 11 + dy, ['.M', 'MM', 'MM'], K)
    patch(idx, 34, 9 + dy, ['.M', 'MM', 'MM', 'M.'], K)
    # masker: donkere band over beide ogen met punten naar achteren
    patch(idx, 12, 16 + dy, [
        '.........mmmm.....mmmmmmm..',
        '.....mmmmmmmmmm.mmmmmmmmmmm',
        '...mmmmmmmmmmmmmmmmmmmmmmmM',
        '..mmmmmmmmmmmmmmmmmmmmmmmM.',
        '..MmmmmmmmmmMMmmmmmmmmmMM..',
        '...MMMMMMMM..MMMMMMMMMM....',
    ], K)
    if not closed:
        # verste oog (klein, driekwart) en dichtste oog: zware leden, gouden iris, spleetpupil, glans
        patch(idx, 14, 18 + dy, ['ooooo', 'owggo', '.oGo.'], K)
        patch(idx, 24, 17 + dy, [
            'ooooooo',
            'owgggGo',
            'oggogGo',
            '.ooooo.',
        ], K)
        # opgetrokken wenkbrauw
        patch(idx, 25, 14 + dy, ['..dd.', '.d..d', 'd....'], K)
    else:
        patch(idx, 14, 18 + dy, ['.o.', 'ogo', 'o.o'], K)
        patch(idx, 25, 17 + dy, ['..oo..', '.oggo.', 'og..go', 'o....o'], K)
        patch(idx, 25, 14 + dy, ['..dd.', '.d..d', 'd....'], K)


def common_body(c, dy=0):
    c.ellipse('voet2', 'donker', 39, 56, 4, 2.2, line='black')
    c.ellipse('lijf', 'vacht', 31, 45, 10, 11, shade=3, hl=(26, 39, 3))
    b = c.ellipse('buik', 'creme', 27.5, 47.5, 5, 7, shade=2)
    b.mask &= c.ellipse_mask(31, 45, 9.5, 10.5)
    c.poly('doek', 'doek', [(19, 31 + dy), (37, 30 + dy), (37, 34 + dy), (30, 41 + dy), (27, 41 + dy), (21, 35 + dy)], shade=2, line='dark')
    c.poly('doek', 'doek', [(36, 31 + dy), (41, 32 + dy), (42, 36 + dy), (39, 37 + dy), (36, 35 + dy)])


def frame1():
    c = Canvas(64, 64, RAMPS)
    Canvas.selout_parts = {'vacht', 'creme', 'doek'}
    ringed_tail(c, [(37, 53), (46, 52), (51.5, 46), (53.5, 38), (52, 30), (48, 25.5)],
                [6.5, 7, 7, 6.5, 6, 5.5], rings=[(0.24, 0.31), (0.47, 0.54), (0.69, 0.76)],
                tip=[(50, 28), (45, 23), (47, 22), (43, 20), (47, 19), (45, 17), (50, 20), (53, 25)])
    common_body(c)
    head(c)
    # verste arm (bungelt voor de borst), zwarte handschoen tot de elleboog
    c.tube('arm1', 'vacht', [(25, 38), (21, 39.5)], [5.5, 5], line='dark', shade=2)
    c.tube('hand1', 'donker', [(22, 39.5), (15, 41)], [5, 4.5], line='black', shade=2)
    c.ellipse('hand1', 'donker', 13, 42, 3.6, 3)
    # munt op schoot
    c.ellipse('munt', 'munt', 24.5, 50.5, 4.6, 4.6, line='black', shade=2, hl=(23, 48.5, 2))
    # dichtste arm naar de munt
    c.tube('arm2', 'vacht', [(37, 39), (38, 44)], [6, 5.5], line='dark', shade=2)
    c.tube('hand2', 'donker', [(38, 44), (35, 48.5), (31.5, 50)], [5.5, 5, 4.5], line='black', shade=2)
    c.ellipse('voet1', 'donker', 22, 55.5, 5.5, 2.6, line='black', shade=1.5)
    idx = c.render()
    face(idx)
    # munt: geslagen teken (ster/kroon) en rand
    patch(idx, 22, 49, ['.G.', 'GgG', '.G.'], K)
    # klauwen: bungelend (3), om de munt (2), achtervoet (2)
    hooks(idx, [
        [(10, 45), (10, 46), (10, 47), (9, 48), (9, 49), (8, 50), (7, 51), (6, 51)],
        [(13, 45), (13, 46), (13, 47), (13, 48), (13, 49), (12, 50), (12, 51), (11, 52)],
        [(16, 44), (16, 45), (16, 46), (16, 47), (17, 48), (17, 49), (16, 50), (16, 51)],
        [(30, 47), (29, 46), (28, 46), (27, 45), (26, 45), (25, 45), (24, 46)],
        [(30, 51), (29, 52), (28, 53), (27, 54), (26, 54), (25, 54)],
        [(17, 55), (16, 55), (15, 55), (14, 56), (13, 56)],
        [(18, 57), (17, 58), (16, 58), (15, 58)],
    ], keep=(5, 6))
    return fix_outline(idx)


def frame2():
    c = Canvas(64, 64, RAMPS)
    Canvas.selout_parts = {'vacht', 'creme', 'doek'}
    ringed_tail(c, [(37, 53), (47, 53), (53, 47), (56, 39), (55, 31), (52, 27)],
                [6.5, 7, 7, 6.5, 6, 5.5], rings=[(0.24, 0.31), (0.47, 0.54), (0.69, 0.76)],
                tip=[(53, 30), (49, 25), (51, 24), (47, 22), (51, 21), (50, 18), (54, 22), (57, 27)])
    common_body(c, dy=-1)
    head(c, dy=-1)
    # verste arm wijd naar links-omhoog
    c.tube('arm1', 'vacht', [(24, 37), (19, 36)], [5.5, 5], line='dark', shade=2)
    c.tube('hand1', 'donker', [(20, 36), (13, 34.5)], [5, 4.5], line='black', shade=2)
    c.ellipse('hand1', 'donker', 11, 34, 3.2, 3.2)
    # dichtste arm omhoog rechts, munt opgegooid
    c.tube('arm2', 'vacht', [(36, 38), (40, 34)], [6, 5.5], line='dark', shade=2)
    c.tube('hand2', 'donker', [(40, 34), (43, 29)], [5.5, 4.5], line='black', shade=2)
    c.ellipse('hand2', 'donker', 43.5, 28, 3.3, 3)
    c.ellipse('munt', 'munt', 47, 8.5, 2.6, 4.2, line='black', shade=1.5)
    c.ellipse('voet1', 'donker', 22, 55.5, 5.5, 2.6, line='black', shade=1.5)
    idx = c.render()
    face(idx, dy=-1, closed=True)
    # open bek met hoektand ("hehe")
    patch(idx, 12, 26, [
        'Cc........o',
        '.oCcccccoo.',
        '..owddddo..',
        '...oddddo..',
        '....oooo...',
    ], K)
    patch(idx, 46, 7, ['i', 'g', 'G'], K)
    hooks(idx, [
        [(8, 32), (7, 31), (6, 30), (5, 29), (5, 28), (4, 27), (4, 26)],
        [(8, 34), (7, 34), (6, 34), (5, 33), (4, 33), (3, 32), (2, 31)],
        [(9, 37), (8, 37), (7, 38), (6, 38), (5, 38), (4, 37), (3, 36)],
        [(41, 25), (41, 24), (40, 23), (40, 22), (40, 21), (41, 20), (42, 19)],
        [(44, 25), (44, 24), (45, 23), (45, 22), (46, 21), (47, 20), (48, 20)],
        [(46, 27), (47, 26), (48, 26), (49, 25), (50, 25), (51, 26)],
        [(17, 55), (16, 55), (15, 55), (14, 56), (13, 56)],
        [(18, 57), (17, 58), (16, 58), (15, 58)],
    ], keep=(5, 6))
    return fix_outline(idx)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    f1, f2 = frame1(), frame2()
    save_indexed(os.path.join(out, 'anim_front.png'), [f1, f2], PAL)
    save_pal(os.path.join(out, 'normal.pal'), PAL)
    print('ok', out)
