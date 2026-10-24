"""Olinguito (Dark-starter, fase 1): het goedgekeurde 3D-poppetje (docs/concept/ontwerp/olinguito_v2/ONTWERP.md),
nu met deel-labels en materialen voor de spritegenerator."""
import math
import numpy as np
from model3d import Model, rot_y, rot_z, qb

HEAD_SCALE = 1.35
HEAD_SHIFT = np.array((-6, 30, 0.0))
LEG_K = 1.15      # sprite: dikkere poten (geen stokpoten)
BODY_LEN = 1.25
HEAD_TURN = 0    # graden extra draai van de kop t.o.v. het lijf


def build():
    m = Model()
    L = lambda pts: [(x, y, z, r * LEG_K) for x, y, z, r in pts]
    m.ell((-30, 0, 0), 26, 'fur', 'lijf')
    m.ell((2, 6, 0), (34, 24, 23), 'fur', 'lijf', rot_z(math.radians(8)))
    m.ell((34, 12, 0), 25, 'fur', 'lijf')
    tail = qb((52, 18, 0), (88, 22, 0), (84, 74, 0), 10)[:-1] + qb((84, 74, 0), (80, 116, 0), (48, 110, 0), 8)[:-1] \
        + qb((48, 110, 0), (22, 104, 0), (26, 84, 0), 6)
    n = len(tail)
    m.chain([(x, y, z, 10.5 - 5 * i / (n - 1)) for i, (x, y, z) in enumerate(tail)], 'fur', 'staart')
    hs, piv = HEAD_SCALE, np.array((-46, -2, 0.0))
    H = lambda p: piv + (np.array(p, float) - piv) * hs + HEAD_SHIFT
    m.chain([(-36, 0, 0, 22), tuple(piv + HEAD_SHIFT) + (20,)], 'fur', 'lijf')
    cr = H((-64, -6, 0))
    m.ell(cr, np.array((25, 28, 25)) * hs, 'head', 'kop')
    m.chain([tuple(H(q[:3])) + (q[3] * hs,) for q in [(-76, -16, 0, 20), (-88, -22, 0, 14.5), (-98, -28, 0, 9.5)]], 'head', 'kop')
    nose = H((-105, -31, 0))
    m.ell(nose, 6.0 * hs, 'nose', 'kop')
    eyes = []
    for sz in (1, -1):
        d = np.array((-0.70, -0.28, 0.66 * sz)); d /= np.linalg.norm(d)
        eyes.append(cr + d * 25 * hs)
    m.points['oog'] = tuple(eyes[0])
    for sz in (1, -1):
        Re = rot_y(math.radians(25 if sz > 0 else 0))
        c = H((-58, 16, 13 * sz))
        k = 1.0 if sz > 0 else 0.6
        m.ell(c, np.array((4, 12, 11)) * hs * k, 'ear', 'oor_n' if sz > 0 else 'oor_v', Re)
        m.ell(c + Re @ np.array((-1.8, 0.5, 0)) * hs * k, np.array((2.6, 8, 7.5)) * hs * k, 'earin', 'oor_n' if sz > 0 else 'oor_v', Re)
    m.chain(L([(-34, -2, 13, 16), (-48, -28, 15, 11.5), (-62, -52, 17, 9)]), 'fur', 'voorpoot_n')
    m.ell((-66, -55, 18), (10, 6, 8), 'paw', 'voorpoot_n')
    m.points['klauw_n'] = (-70, -60, 18)
    m.chain(L([(-28, -2, -13, 14), (-20, -28, -15, 11), (-34, -42, -17, 8.5)]), 'fur', 'voorpoot_v')
    m.ell((-38, -45, -17), (9, 6, 7.5), 'paw', 'voorpoot_v')
    m.points['klauw_v'] = (-42, -50, -17)
    m.chain(L([(30, 10, 18, 20), (6, -20, 21, 13), (30, -42, 21, 9)]), 'fur', 'achterpoot_n')
    m.chain(L([(30, -42, 21, 7.5), (10, -48, 22, 6.5)]), 'paw', 'achterpoot_n')
    m.chain(L([(36, 12, -17, 18), (18, -16, -19, 11.5), (40, -36, -19, 8.5)]), 'fur', 'achterpoot_v')
    m.chain(L([(40, -36, -19, 7), (24, -42, -20, 6)]), 'paw', 'achterpoot_v')
    arc = []
    for t in np.linspace(-1.3, 1.3, 53):
        d = np.array((-0.72, -0.10, 0.69 * t)); d /= np.linalg.norm(d)
        arc.append(cr + d * 26.5 * hs)

    # lijf langer maken (sprite-verhouding; in 3/4 oogt een echt lijf te kort), kop en voorpoten niet
    new = []
    for c, r, R0, mat, part in m.parts:
        if part in ('lijf', 'staart', 'achterpoot_n', 'achterpoot_v') and c[0] > -30:
            c = c.copy(); c[0] = -30 + (c[0] + 30) * BODY_LEN
            if part == 'lijf':
                r = r * np.array((BODY_LEN, 1, 1)) if c[0] > -20 else r
        new.append((c, r, R0, mat, part))
    m.parts = new
    # kop draait verder naar de kijker dan het lijf (scharnier in de nek)
    neck = piv + HEAD_SHIFT
    Rh = rot_y(math.radians(HEAD_TURN))
    m.turn({'kop', 'oor_n', 'oor_v'}, neck, Rh, points=('oog',))
    cr = neck + Rh @ (cr - neck)
    nose = neck + Rh @ (nose - neck)
    eyes = [neck + Rh @ (e - neck) for e in eyes]

    def tex(q, names):
        out = names.copy()
        head = names == 'head'
        qh = q[head]
        u = (qh - cr) / (25 * hs)
        g = out[head]
        g[u @ np.array((0.75, 0.66, 0)) > 0.72] = 'fur'                       # warme kruin achter op de kop
        g[np.linalg.norm(qh - nose, axis=1) < 9 * hs] = 'muzzle'
        de = np.min([np.linalg.norm(qh - e, axis=1) for e in eyes], axis=0)
        band = (np.abs(u[:, 1] + 0.24) < 0.19) & (u[:, 0] < -0.50)            # Zigzagoon-band over beide ogen
        g[(de < 9.5 * hs) | band] = 'mask'
        out[head] = g
        return out
    m.texture = tex
    return m


SPEC = dict(yaw=52, pitch=8, min_line=4,
             width=54, height=52, bottom=9, occl=40, pin=['claw', 'nose', 'paw'], pin_cov=0.35,
            tones=(0.30, 0.35), rough_shade=0.10, rough_edge=0.0,
            far=['voorpoot_v', 'achterpoot_v', 'oor_v'],
            lined_parts=['voorpoot_n', 'voorpoot_v', 'oor_n', 'kop'],
            palette={'K': (16, 16, 16),
                     # vacht: donkerbruine helling uit Sentret
                     'furh': (164, 115, 74), 'furb': (139, 90, 65), 'furs': (98, 65, 49), 'furl': (57, 24, 16),
                     # kop: grijsbruin (Zigzagoon-familie)
                     'headh': (180, 160, 142), 'headb': (148, 123, 106), 'heads': (115, 98, 90), 'headl': (57, 24, 16),
                     'maskh': (16, 16, 16), 'maskb': (16, 16, 16), 'masks': (16, 16, 16), 'maskl': (16, 16, 16),
                     'muzzleh': (90, 82, 74), 'muzzleb': (90, 82, 74), 'muzzles': (90, 82, 74), 'muzzlel': (16, 16, 16),
                     'noseh': (142, 79, 88), 'noseb': (142, 79, 88), 'noses': (142, 79, 88), 'nosel': (16, 16, 16),
                     'pawh': (208, 154, 142), 'pawb': (208, 154, 142), 'paws': (142, 79, 88), 'pawl': (142, 79, 88),
                     'clawh': (242, 234, 214), 'clawb': (242, 234, 214), 'claws': (180, 160, 142), 'clawl': (98, 65, 49),
                     'earh': (57, 24, 16), 'earb': (57, 24, 16), 'ears': (57, 24, 16), 'earl': (16, 16, 16),
                     'earinh': (148, 123, 106), 'earinb': (148, 123, 106), 'earins': (115, 98, 90), 'earinl': (57, 24, 16),
                     'eyed': (168, 64, 26), 'eyel': (184, 87, 44), 'w': (255, 255, 255)},
            templates=[('oog', ['KK.', 'wdK', 'llK'], {'K': 'K', 'w': 'w', 'd': 'eyed', 'l': 'eyel'}),
                       # 2 klauwen per voorpoot: de voorste lang als haak, de achterste korter (Linoone)
                       ('klauw_n', ['..clKclK', '.clK.clK', 'clK...lK', 'clK....K', '.lK.....', '.K......'],
                        {'c': 'clawb', 'l': 'claws', 'K': 'K'}, (3, 0), 'always'),
                       ('klauw_v', ['lKlK', 'lKlK', 'lKl.', 'K...'], {'l': 'claws', 'K': 'K'}, (1, 0), 'always')])
