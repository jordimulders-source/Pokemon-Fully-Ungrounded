"""Kalibratie: Rattata als 3D-poppetje (vergelijken met graphics/pokemon/rattata/anim_front.png)."""
import math
import numpy as np
from model3d import Model, rot_y, rot_z, qb


def build():
    m = Model()
    # lijf: laag en lang (borst, buik, romp)
    m.ell((-4, -2, 0), 10, 'fur', 'lijf')
    m.ell((10, 0, 0), (17, 8.5, 9.5), 'fur', 'lijf', rot_z(math.radians(8)))
    m.ell((22, 3, 0), 10, 'fur', 'lijf')
    # staart: omhoog, krul aan het eind
    t = qb((30, 6, 0), (50, 10, 0), (47, 32, 0), 8)[:-1] + qb((47, 32, 0), (45, 47, 0), (33, 45, 0), 7)[:-1] \
        + qb((33, 45, 0), (25, 41, 0), (32, 36, 0), 6)
    m.chain([(x, y, z, 3.4 - 0.8 * i / (len(t) - 1)) for i, (x, y, z) in enumerate(t)], 'fur', 'lijf')
    # kop (groot, op lijfhoogte), crème snuit
    cr = np.array((-17, 4, 0.0))
    m.ell(cr, (14, 13, 17), 'fur', 'kop')
    m.ell((-27, -2, 0), (7, 6.5, 10), 'cream', 'kop')
    for sz in (1, -1):
        d = np.array((-0.72, 0.18, 0.68 * sz)); d /= np.linalg.norm(d)
        m.points['oog' if sz > 0 else 'oog_ver'] = tuple(cr + d * np.array((14, 13, 17)) * 0.98)
        Re = rot_y(math.radians(20 * sz))
        m.ell((-12, 18, 12 * sz), (2.5, 7.5, 7), 'fur', 'oor_n' if sz > 0 else 'oor_v', Re)
    # poten: nabij (+z), ver (-z); wijd uit elkaar zoals Rattata
    m.chain([(-8, -8, 8, 4.5), (-17, -15, 10, 3.2)], 'fur', 'voorpoot_n')
    m.ell((-21, -17, 11), (5, 2.2, 3.2), 'cream', 'voorpoot_n')
    m.chain([(-6, -7, -8, 4), (-12, -13, -9, 3)], 'fur', 'voorpoot_v')
    m.ell((-15, -15, -10), (4, 2, 3), 'cream', 'voorpoot_v')
    m.chain([(21, -2, 8, 8.5), (27, -11, 9, 4)], 'fur', 'achterpoot_n')
    m.ell((31, -14, 10), (6, 2.2, 3.2), 'cream', 'achterpoot_n')
    m.chain([(22, -2, -8, 7.5), (32, -9, -9, 3.5)], 'fur', 'achterpoot_v')
    m.ell((36, -12, -10), (5, 2, 3), 'cream', 'achterpoot_v')

    def tex(q, names):
        out = names.copy()
        for sz in (1, -1):   # oor-binnenkant crème
            c = np.array((-14.5, 18, 12 * sz))
            d = np.linalg.norm((q - c) * np.array((1, 0.6, 0.8)), axis=1)
            out[(d < 3.6) & (names == 'fur') & (q[:, 0] < -13.5)] = 'cream'
        return out
    m.texture = tex
    # dikker maken (Rattata is mollig): stralen x1.25, posities gelijk
    m.parts = [(c, r * (1.25 if mat != 'cream' or part == 'kop' else 1.15), R0, mat, part) for c, r, R0, mat, part in m.parts]
    m.points = {k: tuple(cr + (np.array(v) - cr) * 1.25) for k, v in m.points.items()}
    return m


SPEC = dict(yaw=55, pitch=12, height=39, bottom=13, dx=-1, pin=['cream'], pin_cov=0.4,
            tones=(0.28, 0.35), rough_shade=0.12, rough_edge=0.0, lined_parts=['voorpoot_n', 'achterpoot_n', 'oor_n', 'kop'], far=['voorpoot_v', 'achterpoot_v', 'oor_v'],
            palette={'K': (16, 16, 16),
                     'furh': (208, 152, 208), 'furb': (180, 115, 189), 'furs': (139, 74, 139), 'furl': (74, 41, 65),
                     'creamh': (238, 222, 180), 'creamb': (230, 205, 115), 'creams': (205, 172, 98), 'creaml': (164, 115, 8),
                     'eyer': (230, 90, 115), 'eyed': (164, 24, 57), 'w': (255, 255, 255)},
            templates=[('oog', ['KK', 'rw', 'dr'], {'K': 'K', 'r': 'eyer', 'w': 'w', 'd': 'eyed'}),
                       ('oog_ver', ['K', 'r'], {'K': 'K', 'r': 'eyer'})])
