import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdl import *

CFG = {
    # A: kleuren van de echte nachtaap (Aotus): grijsbruin-violet, bleke gezichtsschijf met donkere rand,
    #    oranje keel/borst, zwarte staartpunt.
    'A': dict(fur='#6b5478', dark='#2e2236', face='#f6efdc', belly='#f0974e', eye='#ff4fa3', pupil='#4a1036',
              line='#21182a', pose='peer', ears=False, tailtip='#2e2236', brow='lobes', pad='#d9b9a6'),
    # B: dicht bij de goedgekeurde kleur, maar verzadigd violet met donkere indigo kap en bleke schijf.
    'B': dict(fur='#8a5fd6', dark='#432c86', face='#f4ecff', belly='#f4ecff', eye='#3fe6ef', pupil='#123a5a',
              line='#261a44', pose='wave', ears=True, tailtip=None, brow='lobes', pad='#f4b8d8'),
    # C: nachtblauw, gezichtsschijf als maansikkel + losse snuit, zilveren staartkrul.
    'C': dict(fur='#41429a', dark='#22205a', face='#e9eefb', belly='#e9eefb', eye='#c58cff', pupil='#3a1468',
              line='#171636', pose='cling', ears=False, tailtip='#e9eefb', brow='moon', pad='#b9c3f0'),
}


def limb(cv, pts, w0, w1, c):
    return cv.fill(cv.m_tube(catmull(pts, closed=False), w0, w1), c['fur'])


def hand(cv, x, y, ang, c, s=1.0):
    """Tarsierhand: kleine palm, drie lange vingers met grote ronde kussens."""
    a = math.radians(ang)
    m = cv.m_ellipse(x, y, 6.5 * s, 6.5 * s)
    tips = []
    for k in (-30, 0, 30):
        b = a + math.radians(k)
        fx, fy = x + math.cos(b) * 12 * s, y + math.sin(b) * 12 * s
        m |= cv.m_tube([(x, y), (fx, fy)], 4.2 * s)
        m |= cv.m_ellipse(fx, fy, 4.6 * s, 4.6 * s)
        tips.append((fx, fy))
    cv.fill(m, c['fur'], lw=2.2)
    for fx, fy in tips:
        cv.dot(fx, fy, 2.4 * s, c['pad'])


def foot(cv, heel, ang, c, s=1.0):
    """Lange tarsiervoet met drie grote teenkussens, wijst in richting ang."""
    hx, hy = heel
    a = math.radians(ang)
    tx, ty = hx + math.cos(a) * 16 * s, hy + math.sin(a) * 16 * s
    m = cv.m_tube([(hx, hy), (tx, ty)], 10 * s, 9 * s)
    tips = []
    for k in (-34, 0, 34):
        b = a + math.radians(k)
        fx, fy = tx + math.cos(b) * 8 * s, ty + math.sin(b) * 8 * s * 0.6
        m |= cv.m_tube([(tx, ty), (fx, fy)], 4.4 * s)
        m |= cv.m_ellipse(fx, fy, 5.0 * s, 4.6 * s)
        tips.append((fx, fy))
    cv.fill(m, c['fur'], lw=2.2)
    for fx, fy in tips:
        cv.dot(fx, fy + 0.6, 2.5 * s, c['pad'])


def draw(key):
    c = CFG[key]
    cv = Canvas(line=c['line'], lw=2.6)
    pose = c['pose']

    # ---- staart (achter alles); krulletje, nog geen volle spiraal ----
    if pose == 'cling':
        t = cv.m_curl(208, 58, 3.5, 20, 1.15, 9, 7, start=2.2, direction=-1,
                      tail=[(214, 92), (204, 150), (168, 200)])
        cv.fill(t, c['fur'])
        cv.fill(cv.m_curl(208, 58, 3.5, 10, 0.6, 7.5, 7, start=2.2, direction=-1), c['tailtip'], lw=1.8)
    else:
        t = cv.m_curl(214, 148, 3.5, 22, 1.2, 10, 7, start=0.6, direction=-1,
                      tail=[(226, 186), (206, 214), (166, 210)])
        cv.fill(t, c['fur'])
        if c['tailtip']:
            cv.fill(cv.m_curl(214, 148, 3.5, 11, 0.55, 8.5, 7, start=0.6, direction=-1), c['tailtip'], lw=1.8)

    # ---- verre been ----
    if pose == 'cling':
        limb(cv, [(152, 202), (174, 160), (160, 214)], 16, 8, c)
        foot(cv, (160, 216), 158, c, 1.35)
    else:
        limb(cv, [(152, 202), (170, 166), (158, 214)], 16, 8, c)
        foot(cv, (158, 216), 158, c, 1.35)

    # ---- verre arm (achter lijf) ----
    if pose == 'wave':
        limb(cv, [(150, 150), (170, 166), (172, 180)], 7.5, 6.5, c)
        hand(cv, 172, 186, 95, c)
    if pose == 'cling':
        pass

    # ---- lijf: klein peertje ----
    body = cv.m_blob([(104, 140), (126, 134), (150, 140), (164, 168), (160, 204), (140, 220),
                      (112, 220), (94, 202), (90, 170)])
    cv.fill(body, c['fur'])
    cv.fill(cv.m_blob([(110, 136), (138, 136), (146, 170), (140, 206), (124, 214), (108, 206), (102, 170)]),
            c['belly'], line=False, clip=body)

    if pose == 'cling':
        limb(cv, [(156, 150), (176, 166), (178, 182)], 7.5, 6.5, c)
        hand(cv, 178, 188, 95, c)

    # ---- nabije been ----
    if pose == 'cling':
        limb(cv, [(112, 202), (88, 160), (104, 214)], 17, 8, c)
        foot(cv, (104, 218), 165, c, 1.45)
    else:
        limb(cv, [(112, 202), (90, 166), (104, 214)], 17, 8, c)
        foot(cv, (104, 218), 165, c, 1.45)

    # ---- armen/handen voor ----
    if pose == 'wave':
        limb(cv, [(102, 150), (82, 166), (62, 150), (58, 128)], 7.5, 6.5, c)
        hand(cv, 58, 122, -90, c)
    elif pose == 'peer':
        # handen onder de kin, vingers tegen de wangen: 'gluren'
        limb(cv, [(150, 150), (160, 168), (142, 146)], 7.5, 6.5, c)
        limb(cv, [(100, 150), (90, 168), (96, 146)], 7.5, 6.5, c)
        hand(cv, 96, 140, -80, c, 1.0)
        hand(cv, 142, 140, -100, c, 1.0)
    else:
        limb(cv, [(100, 152), (80, 168), (78, 182)], 7.5, 6.5, c)
        hand(cv, 76, 188, 85, c)

    # ---- oren ----
    if c['ears']:
        cv.fill(cv.m_ellipse(177, 76, 11, 13, rot=20), c['fur'])
        cv.fill(cv.m_ellipse(178, 77, 5.5, 7, rot=20), c['pad'], line=False)

    # ---- kop ----
    head = cv.m_ellipse(120, 92, 62, 55)
    if key == 'A':
        # wangplukken: de vacht van de nachtaap staat opzij uit
        head |= cv.m_blob([(62, 96), (46, 118), (74, 124)]) | cv.m_blob([(176, 94), (194, 116), (168, 124)])
    cv.fill(head, c['fur'])
    if c['brow'] == 'lobes':
        disc = (cv.m_ellipse(110, 107, 45, 38) | cv.m_ellipse(86, 82, 21, 16, rot=-15) |
                cv.m_ellipse(134, 80, 25, 17, rot=12))
        # donkere rand om de schijf (de zijstrepen van de nachtaap), dan de schijf zelf
        cv.fill(cv.dilate(disc, 3.2 * SS) & head, c['dark'], line=False)
        cv.fill(disc, c['face'], line=False, clip=head)
        # korte donkere wig tussen de wenkbrauwen
        cv.fill(cv.m_blob([(102, 54), (118, 54), (110, 88)]), c['dark'], line=False, clip=disc)
    else:
        # donker masker om de ogen, bleke snuit, en boven elk oog een bleke sikkel (de witte
        # 'wenkbrauw' van de nachtaap als twee maansikkels)
        mask = cv.m_ellipse(110, 100, 50, 34)
        cv.fill(mask, c['dark'], line=False, clip=head)
        snout = cv.m_ellipse(109, 122, 25, 17)
        cv.fill(snout, c['face'], line=False, clip=head)
        for (x, y, rx, rot) in ((86, 78, 22, -14), (134, 76, 26, 10)):
            cres = cv.m_ellipse(x, y, rx, 13, rot=rot) & ~cv.m_ellipse(x, y + 7, rx * 0.92, 11, rot=rot)
            cv.fill(cres, c['face'], line=False, clip=head)

    # ---- ogen: egaal gloeiend, kleine pupil, één glans ----
    for (x, y, r) in ((86, 102, 17), (132, 102, 20)):
        eye = cv.m_ellipse(x, y, r * 0.9, r * 1.1)
        cv.fill(eye, c['eye'], lw=2.6)
        # zwaar bovenooglid: mysterieus, niet slaperig
        lid = cv.m_ellipse(x, y - r * 1.62, r * 1.4, r * 0.8) & cv.dilate(eye, 1.2 * SS)
        cv.fill(lid, c['line'], line=False)
        cv.dot(x - r * 0.12, y + r * 0.12, r * 0.22, c['pupil'])
        cv.dot(x + r * 0.32, y - r * 0.28, r * 0.14, '#ffffff')

    # ---- neus en mond ----
    cv.fill(cv.m_blob([(103, 121), (114, 121), (108.5, 127)]), c['line'], line=False)
    cv.stroke([(102, 134), (108.5, 136.5), (116, 133)], 1.8)
    return cv


if __name__ == '__main__':
    out = sys.argv[1]
    for k in sys.argv[2:] or 'ABC':
        cv = draw(k)
        cv.image().save(os.path.join(out, 'nachtaap_%s_raw.png' % k))
        np.save(os.path.join(out, 'nachtaap_%s_rgb.npy' % k), cv.img)
        np.save(os.path.join(out, 'nachtaap_%s_a.npy' % k), cv.alpha)
