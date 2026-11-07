"""Poppetje passend maken op het goedgekeurde silhouet v3A (= foto 1 + kop x1,45 + open bek).
Parameters van de grote vormen (lijf, buik, kop, staart, vleugel) worden gezocht op maximale overlap (IoU)
met het silhouet; daarna komen dons, ogen en kleur erop zonder de omtrek te veranderen."""
import math, json, numpy as np
import pop3d_kuiken as K, overlay as O
P = K.P
START = dict(bx=8, by=0, brx=21, bry=28, brz=20, bt=26, ex=-1, ey=-5, erx=17, ery=22, et=22,
             hx=-12, hy=30, hr=19, tx=36, ty=-26, tl=12, tt=-38, wx=18, wy=-4, wl=25, wt=36)
def model(p, dons=False, ogen=True):
    m = P.Model(); rz = P.rot_z
    m.ell((p['bx'], p['by'], 0), (p['brx'], p['bry'], p['brz']), 'body', rz(math.radians(p['bt'])))
    m.ell((p['ex'], p['ey'], 5), (p['erx'], p['ery'], 16), 'belly', rz(math.radians(p['et'])))
    if dons:
        K.fluff(m, (p['ex'], p['ey'], 5), (p['erx'], p['ery'], 16), 'belly', 14, 4.5, 3, ymin=-0.9, R0=rz(math.radians(p['et'])))
    hc = np.array((p['hx'], p['hy'], 0.0)); HR = p['hr']
    m.ell(hc, (HR, HR * 0.95, HR * 0.92), 'head')
    if dons:
        K.fluff(m, hc, (HR, HR * 0.95, HR * 0.92), 'head', 16, 2.8, 11, ymin=0.3)
    m.ell(hc + np.array((-3, -0.6 * HR, 0)), (0.55 * HR, 0.42 * HR, 0.62 * HR), 'belly')
    base = hc + np.array((-HR * 0.84, -0.12 * HR, 0))
    def snavel(hoek, L, r0):
        d = np.array((math.cos(hoek), math.sin(hoek), 0))
        return [tuple(base + d * L * t) + (r0 * (1 - t) + 0.9 * t,) for t in np.linspace(0, 1, 7)]
    a = math.radians(180 - 18)
    m.chain(snavel(a - math.radians(30), 1.2 * HR, 0.24 * HR), 'beak', 0.8)
    m.chain(snavel(a + math.radians(18), 0.95 * HR, 0.21 * HR), 'beak', 0.8)
    m.ell(base + np.array((-1, 0, 0)), np.array((0.3, 0.32, 0.26)) * HR, 'gape')
    m.ell(base + np.array((-4, 0, 0)), np.array((0.26, 0.2, 0.17)) * HR, 'mouth')
    if ogen:
        for sz in (1, -1):
            d = np.array((-0.45, 0.20, 0.87 * sz)); d /= np.linalg.norm(d)
            e = hc + d * HR * 0.88
            m.ell(e, 0.27 * HR, 'eye'); m.ell(e + d * 0.18 * HR + np.array((-1.4, 2.2, 0)), 0.09 * HR, 'glint')
    t0 = hc + np.array((0.25 * HR, HR * 0.9, 0))
    m.chain([tuple(t0) + (0.17 * HR,), tuple(t0 + np.array((7, 4, 0))) + (0.11 * HR,), tuple(t0 + np.array((12, 4.5, 0))) + (1.0,)], 'tuft', 0.8)
    for sz, g in ((1, 'wing'), (-1, 'far')):
        m.ell((p['wx'], p['wy'], 15 * sz), (7, p['wl'], 5), g, rz(math.radians(p['wt'])))
    m.ell((p['wx'] - 13, p['wy'] + 17, 17.0), (6, 3.2, 4), 'shoulder', rz(math.radians(30)))
    m.ell((p['tx'], p['ty'], 0), (p['tl'], 4.5, 8), 'tail', rz(math.radians(p['tt'])))
    fy = p['by'] - p['bry'] * 0.92
    for dz in (7, -7):
        m.chain([(p['bx'] - 6, fy + 2, dz, 2.6), (p['bx'] - 8, fy - 3, dz, 2.0)], 'feet', 0.8)
        m.chain([(p['bx'] - 8, fy - 3, dz, 1.8), (p['bx'] - 15, fy - 4, dz, 1.3)], 'feet', 0.8)
    return m
YAW, PITCH = 15, 4
def score(p): return O.vergelijk(model(p, ogen=False), YAW, PITCH)[0]
if __name__ == '__main__':
    K.set_palet('fluweel (als eindvorm)')
    p = dict(START); best = score(p); print('start', round(best, 3))
    steps = {k: (4 if k[-1] in 'xy' or k[-1] == 'l' else 3) for k in p}
    for k in p:
        if k.endswith('t'): steps[k] = 6
    for rnd in range(4):
        for k in p:
            for s in (steps[k], -steps[k]):
                while True:
                    q = dict(p); q[k] += s; sc = score(q)
                    if sc > best + 1e-4: p, best = q, sc
                    else: break
        steps = {k: v / 2 for k, v in steps.items()}
        print('ronde', rnd, round(best, 3))
    json.dump(p, open('pas_params.json', 'w'), indent=1)
    O.vergelijk(model(p), YAW, PITCH, 'overlay_pas.png')
