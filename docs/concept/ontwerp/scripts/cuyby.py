import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdl import *

CFG = {
    'A': dict(fur='#b07443', cream='#f6dca6', accent='#7a4424', pink='#f2909c', line='#45240f', eye='#2a160c'),
    'B': dict(fur='#c9553a', cream='#fff0c8', accent='#7d1f22', pink='#f59aa6', line='#3d1510', eye='#2a1210'),
    'C': dict(fur='#fbf7ee', cream='#fbf7ee', accent='#ec8a2c', dark='#34292a', pink='#f2909c', line='#3a2a22',
              eye='#2a1a14'),
}


def petal(cv, cx, cy, ang, length, width, bend=0.35):
    """Gebogen druppel van (cx,cy) in richting ang (graden), punt buigt met de klok mee."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    tip = (cx + ux * length + nx * length * bend, cy + uy * length + ny * length * bend)
    mid1 = (cx + ux * length * 0.5 + nx * width * 0.5, cy + uy * length * 0.5 + ny * width * 0.5)
    mid2 = (cx + ux * length * 0.45 - nx * width * 0.55 + nx * length * bend * 0.4,
            cy + uy * length * 0.45 - ny * width * 0.55 + ny * length * bend * 0.4)
    b1 = (cx + nx * width * 0.45, cy + ny * width * 0.45)
    b2 = (cx - nx * width * 0.45, cy - ny * width * 0.45)
    return cv.m_blob([b1, mid1, tip, mid2, b2])


def rosette(cv, cx, cy, angs, length, width, c, center=True, line=True):
    m = cv.m_ellipse(cx, cy, width * 0.55, width * 0.55)
    for a in angs:
        m |= petal(cv, cx, cy, a, length, width)
    return m


def eye(cv, x, y, r, c, look=-0.15):
    e = cv.m_ellipse(x, y, r * 0.78, r)
    cv.fill(e, c['eye'], lw=1.6)
    cv.dot(x + r * 0.22, y - r * 0.36, r * 0.3, '#ffffff')
    cv.dot(x - r * 0.25, y + r * 0.42, r * 0.13, '#ffffff')


def ear(cv, x, y, rot, s, c):
    m = cv.m_ellipse(x, y, 13 * s, 9 * s, rot=rot)
    cv.fill(m, c['fur'] if 'dark' not in c else c['dark'])
    cv.fill(cv.m_ellipse(x + 1, y + 1.5, 8 * s, 5 * s, rot=rot), c['pink'], line=False, clip=m)


def tuft_rosette(cv, cx, cy, angs, length, width, c, tip=True):
    """Rozet = vachtwervel als molentje: puntige plukken rondom, allemaal met de klok mee gebogen."""
    m = cv.m_ellipse(cx, cy, width * 0.5, width * 0.5)
    for a in angs:
        m |= petal(cv, cx, cy, a, length, width, bend=0.38)
    cv.fill(m, c['fur'])
    if tip:
        core = cv.m_ellipse(cx, cy, length * 0.62, length * 0.62)
        for a in angs:
            cv.fill(petal(cv, cx, cy, a, length, width, bend=0.38) & ~core, c['cream'], line=False)
        # de wervel: scheidingslijntjes die naar het midden draaien
        for a in angs:
            r = math.radians(a - 28)
            cv.stroke([(cx + math.cos(r + 0.5) * length * 0.5, cy + math.sin(r + 0.5) * length * 0.5),
                       (cx + math.cos(r) * 3, cy + math.sin(r) * 3)], 1.5)
    return m


def ruff(cv, cx, cy, rx, ry, angs, length, width, bend=0.3):
    m = cv.m_ellipse(cx, cy, rx, ry)
    for a in angs:
        r = math.radians(a)
        x, y = cx + rx * 0.8 * math.cos(r), cy + ry * 0.8 * math.sin(r)
        m |= petal(cv, x, y, a, length, width, bend=bend)
    return m


def fan(cv, cx, cy, angs, length, width, bend=0.38):
    m = cv.m_ellipse(cx, cy, width * 0.5, width * 0.5)
    for a in angs:
        m |= petal(cv, cx, cy, a, length, width, bend=bend)
    return m


def whorl_lines(cv, cx, cy, angs, length):
    """Scheidingslijntjes van een vachtwervel: kort, gebogen, vanuit één punt."""
    for a in angs:
        r = math.radians(a + 16)
        pts = [(cx + math.cos(r + t * 0.35) * (3 + t * length), cy + math.sin(r + t * 0.35) * (3 + t * length))
               for t in (0, 0.5, 1)]
        cv.stroke(pts, 1.6)


def draw_A(c):
    cv = Canvas(line=c['line'], lw=2.6)
    cv.fill(cv.m_ellipse(156, 214, 15, 8), c['fur'])
    # rozetten op heup en schouder: puntige waaiers die uit de rugrand steken
    for (x, y, angs, L, W) in ((168, 170, [-40, 5, 50, 95], 34, 18), (166, 112, [-75, -30, 15], 30, 17)):
        m = fan(cv, x, y, angs, L, W)
        cv.fill(m, c['fur'])
        cv.fill(m & ~cv.m_ellipse(x, y, L * 0.6, L * 0.6), c['cream'], line=False)
    body = cv.m_blob([(116, 64), (84, 74), (64, 102), (62, 136), (72, 176), (90, 206), (124, 216),
                      (160, 208), (176, 178), (178, 130), (164, 88), (142, 68)])
    cv.fill(body, c['fur'])
    cv.fill(cv.m_blob([(72, 132), (96, 126), (118, 150), (120, 190), (100, 210), (78, 196), (66, 160)]),
            c['cream'], line=False, clip=body)
    cv.fill(cv.m_ellipse(82, 126, 22, 15, rot=-8), c['cream'], line=False, clip=body)
    # kruinrozet: de grote, rechtopstaande kroon van de Abessijn
    angs = [-158, -122, -86, -50, -14]
    crown = fan(cv, 116, 70, angs, 40, 22)
    cv.fill(crown, c['fur'])
    cv.fill(crown & ~body, c['cream'], line=False)
    whorl_lines(cv, 116, 76, [-150, -90, -30], 9)
    ear(cv, 80, 86, -35, 1.0, c)
    ear(cv, 152, 82, 30, 1.15, c)
    for (x, y) in ((86, 182), (114, 188)):
        cv.fill(cv.m_ellipse(x, y, 9, 7), c['fur'])
        cv.stroke([(x - 3, y + 2), (x - 3, y + 6)], 1.4)
        cv.stroke([(x + 2, y + 2), (x + 2, y + 6)], 1.4)
    cv.fill(cv.m_ellipse(102, 216, 15, 7.5), c['fur'])
    eye(cv, 90, 106, 9.5, c)
    eye(cv, 127, 104, 11, c)
    cv.fill(cv.m_ellipse(70, 122, 6, 4.5), c['pink'], lw=1.8)
    cv.stroke([(71, 127), (72, 132)], 1.6)
    cv.stroke([(65, 131), (72, 134), (80, 131)], 1.6)
    return cv


def draw_B(c):
    cv = Canvas(line=c['line'], lw=2.6)
    cv.fill(cv.m_ellipse(156, 214, 15, 8), c['fur'])
    body = cv.m_blob([(120, 58), (88, 66), (70, 92), (70, 130), (76, 176), (94, 208), (126, 218),
                      (160, 210), (178, 176), (180, 124), (168, 80), (148, 62)])
    cv.fill(body, c['fur'])
    cv.fill(cv.m_blob([(90, 150), (126, 146), (138, 180), (126, 210), (96, 208), (84, 180)]),
            c['cream'], line=False, clip=body)
    # oren
    ear(cv, 92, 64, -30, 1.0, c)
    ear(cv, 156, 66, 34, 1.15, c)
    # de fluitsnuit: twee opgeblazen wangzakken die buiten de kop uitsteken
    far = cv.m_ellipse(66, 120, 24, 22)
    near = cv.m_ellipse(140, 128, 30, 27)
    cv.fill(far, c['cream'])
    # snuitbuis met de ronde fluitmond, voor de wangen
    cv.fill(near, c['cream'])
    tube = cv.m_ellipse(98, 132, 20, 17)
    cv.fill(tube, c['cream'])
    cv.fill(cv.m_ellipse(94, 136, 9, 9.5), c['accent'], lw=2.2)
    cv.fill(cv.m_ellipse(93, 139, 4.5, 4), c['pink'], line=False)
    cv.fill(cv.m_ellipse(98, 118, 5.5, 4), c['pink'], lw=1.8)
    # ogen boven de wangen
    eye(cv, 84, 94, 9, c)
    eye(cv, 124, 92, 10.5, c)
    # voorpootjes tegen de wangen
    for (x, y) in ((80, 160), (120, 162)):
        cv.fill(cv.m_ellipse(x, y, 9, 7), c['fur'])
        cv.stroke([(x - 3, y + 2), (x - 3, y + 6)], 1.4)
        cv.stroke([(x + 2, y + 2), (x + 2, y + 6)], 1.4)
    cv.fill(cv.m_ellipse(100, 218, 15, 7.5), c['fur'])
    return cv


def draw_C(c):
    cv = Canvas(line=c['line'], lw=2.6)
    for (x, y) in ((100, 214), (144, 214)):
        cv.fill(cv.m_ellipse(x, y, 11, 6.5), c['pink'])
        cv.stroke([(x - 3, y + 1), (x - 3, y + 5)], 1.4)
        cv.stroke([(x + 3, y + 1), (x + 3, y + 5)], 1.4)
    # langhaar-bol: lokken rondom, die door hun gewicht naar beneden vallen
    cx, cy, R = 122, 130, 66
    m = cv.m_ellipse(cx, cy, R, R * 0.92)
    locks = []
    for k in range(18):
        a = -90 + k * 20
        r = math.radians(a)
        x, y = cx + R * 0.85 * math.cos(r), cy + R * 0.8 * math.sin(r)
        # punt buigt naar beneden (zwaartekracht), langer aan de zijkant
        L = 20 + 10 * abs(math.cos(r))
        tip = (x + math.cos(r) * L * 0.7, y + math.sin(r) * L * 0.5 + L * 0.55)
        lock = cv.m_blob([(x - math.sin(r) * 11, y + math.cos(r) * 11), tip, (x + math.sin(r) * 11, y - math.cos(r) * 11)])
        m |= lock
        locks.append((x, y, tip))
    coat = m & ~cv.m_poly([(0, 208), (256, 208), (256, 256), (0, 256)])
    coat |= cv.m_blob([(60, 190), (184, 190), (190, 208), (54, 208)]) & m
    cv.fill(coat, c['fur'])
    # driekleurvlakken als grote ronde vormen (geen banen): oranje rug, zwart om het verre oog
    cv.fill(cv.m_ellipse(176, 112, 70, 92, rot=-10), c['accent'], line=False, clip=coat)
    cv.fill(cv.m_ellipse(72, 92, 34, 40, rot=20), c['dark'], line=False, clip=coat)
    # loklijnen
    for (x, y, tip) in locks[3:16]:
        cv.stroke([(x + (cx - x) * 0.25, y + (cy - y) * 0.25), ((x + tip[0]) / 2, (y + tip[1]) / 2 + 2)], 1.5)
    # snuit + ogen onder de pony
    snout = cv.m_ellipse(96, 138, 22, 16)
    cv.fill(snout, c['fur'])
    cv.fill(cv.m_ellipse(88, 136, 6, 4.5), c['pink'], lw=1.8)
    cv.stroke([(89, 141), (90, 146)], 1.6)
    cv.stroke([(83, 144), (90, 147), (98, 144)], 1.6)
    eye(cv, 78, 116, 8, c)
    eye(cv, 118, 114, 9.5, c)
    ear(cv, 70, 70, -40, 0.85, dict(c, fur=c['dark'], dark=c['dark']))
    ear(cv, 158, 66, 30, 0.95, dict(c, fur=c['accent'], dark=c['accent']))
    return cv


# ---- silhouetten van de evoluties (schets) ----
def sil_canvas():
    return Canvas(line='#16161a', lw=0)


def evo(key, stage):
    cv = sil_canvas()
    k = '#16161a'
    def f(m):
        cv.fill(m, k, line=False)
    if key == 'A':
        if stage == 2:
            # rechtop op de achterpoten, kruin + schouderrozetten groter
            f(cv.m_blob([(120, 70), (90, 84), (78, 130), (84, 190), (104, 226), (150, 226), (168, 190), (166, 120), (148, 80)]))
            f(rosette(cv, 120, 70, [-160, -125, -90, -55, -20], 46, 22, {}))
            f(rosette(cv, 82, 130, [180, 140, 220], 32, 16, {}))
            f(rosette(cv, 166, 128, [0, -40, 40], 32, 16, {}))
            f(cv.m_ellipse(104, 230, 18, 8) | cv.m_ellipse(150, 230, 18, 8))
        else:
            # groot en rond, een krans van rozetten als zonnekroon om de kop
            f(cv.m_blob([(128, 82), (82, 100), (58, 160), (70, 216), (128, 236), (186, 216), (198, 160), (174, 100)]))
            for a in range(-180, 1, 30):
                x = 128 + 52 * math.cos(math.radians(a)); y = 96 + 46 * math.sin(math.radians(a))
                f(rosette(cv, x, y, [a - 30, a, a + 30], 28, 14, {}))
            f(cv.m_ellipse(128, 96, 50, 44))
    elif key == 'B':
        if stage == 2:
            f(cv.m_blob([(124, 64), (90, 76), (80, 130), (86, 196), (124, 226), (162, 196), (168, 130), (156, 76)]))
            f(cv.m_ellipse(76, 132, 30, 28) | cv.m_ellipse(170, 132, 32, 30))
            f(cv.m_ellipse(98, 68, 13, 9, rot=-30) | cv.m_ellipse(150, 68, 13, 9, rot=30))
            f(cv.m_ellipse(106, 228, 18, 8) | cv.m_ellipse(146, 228, 18, 8))
        else:
            # forse fluiter: snorharen als holle buizen (siku/panfluit) die naar opzij waaieren
            f(cv.m_blob([(128, 70), (86, 88), (68, 150), (78, 214), (128, 234), (178, 214), (188, 150), (170, 88)]))
            for i, L in enumerate([34, 46, 58, 46]):
                y = 116 + i * 12
                f(cv.m_poly([(90, y - 5), (90 - L, y - 9 - i * 3), (90 - L, y + 1 - i * 3), (90, y + 5)]))
                f(cv.m_poly([(166, y - 5), (166 + L, y - 9 - i * 3), (166 + L, y + 1 - i * 3), (166, y + 5)]))
            f(cv.m_ellipse(102, 74, 14, 10, rot=-30) | cv.m_ellipse(154, 74, 14, 10, rot=30))
    else:
        def shag(cx, cy, R, ry, n, drop):
            m = cv.m_ellipse(cx, cy, R, ry)
            for k in range(n):
                a = -90 + k * 360 / n
                r = math.radians(a)
                x, y = cx + R * 0.85 * math.cos(r), cy + ry * 0.85 * math.sin(r)
                L = drop * (0.6 + 0.6 * abs(math.cos(r)))
                tip = (x + math.cos(r) * L * 0.7, y + math.sin(r) * L * 0.5 + L * 0.55)
                m |= cv.m_blob([(x - math.sin(r) * 12, y + math.cos(r) * 12), tip,
                                (x + math.sin(r) * 12, y - math.cos(r) * 12)])
            return m
        if stage == 2:
            # grotere, bredere bol op vier stompe pootjes
            f(shag(128, 130, 84, 70, 20, 30) & ~cv.m_poly([(0, 206), (256, 206), (256, 256), (0, 256)]))
            for x in (78, 110, 146, 178):
                f(cv.m_ellipse(x, 214, 12, 10))
            f(cv.m_ellipse(86, 66, 13, 9, rot=-40) | cv.m_ellipse(170, 64, 13, 9, rot=40))
        else:
            # wandelende hooiberg: hoge koepel, lokken tot op de grond, een snuit die naar voren steekt
            f(shag(132, 120, 96, 104, 22, 34) & ~cv.m_poly([(0, 236), (256, 236), (256, 256), (0, 256)]))
            f(cv.m_ellipse(46, 148, 24, 18))
            f(cv.m_ellipse(84, 34, 14, 9, rot=-40) | cv.m_ellipse(180, 30, 14, 9, rot=40))
    return cv


def draw(key):
    return {'A': draw_A, 'B': draw_B, 'C': draw_C}[key](CFG[key])


if __name__ == '__main__':
    out = sys.argv[1]
    for k in sys.argv[2:] or 'ABC':
        cv = draw(k)
        cv.image().save(os.path.join(out, 'cuyby_%s_raw.png' % k))
        np.save(os.path.join(out, 'cuyby_%s_rgb.npy' % k), cv.img)
        np.save(os.path.join(out, 'cuyby_%s_a.npy' % k), cv.alpha)
        for st in (2, 3):
            e = evo(k, st)
            e.image().save(os.path.join(out, 'cuyby_%s_evo%d.png' % (k, st)))
