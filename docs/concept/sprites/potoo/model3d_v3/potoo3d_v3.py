"""Great potoo 3D v3: de bek als echte snavel uit onderdelen (Jordi: "de bek is geen snavel ... pacman zeehond").
- Bovensnavel: de kop zelf, met een harde lichte rand (tomium) langs de gaplijn, recht van de mondhoek onder het oog naar
  een donker haakje dat omlaag krult; daaronder het gehemelte.
- Onderkaak: twee duidelijke kaaktakken (harde lichte rand) die als een V naar een spitse donkere punt lopen; de huid
  (de muil) hangt ertussen als een buidel. Van voren is de open bek een schild: rechte bovenkant, V-onderkant.
- Kop: brede, vlakkere kruin (superellipsoïde), ogen voor-opzij, rug met veertjes tussen de ogen.
Lijf en render-hulpmiddelen uit ../model3d_v2/potoo3d.py.
Gebruik: python3.11 potoo3d_v3.py uitmap A hoek1,hoek2   (PARAM=sleutel=waarde,... voor overrides)"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../model3d_v2'))
import numpy as np
import potoo3d as V2
from potoo3d import ell, smin, capsule, rot_y, blad
import bpy

def params(var):
    P = dict(r_oog=2.4, oog_mul=1.0, open=58, kop_op=0, voorover=0, lijf_len=1.0, kaak_len=16.0, kaak_w=11.0,
             oog_h=5.0, oog_az=46, kruin=11.0, kop_p=2.3)
    if var == 'B': P.update(oog_mul=1.25, kaak_len=19.0, kaak_w=12.5, lijf_len=0.85)
    return P

def supell(q, c, r, p):
    """superellipsoïde: rond in het horizontale vlak, vlakker boven/onder met exponent p"""
    d = (q - np.array(c, float)) / np.array(r, float)
    k = (d[..., 0] ** 2 + d[..., 1] ** 2) ** (p / 2) + np.abs(d[..., 2]) ** p
    return (k ** (1 / p) - 1) * min(r) * 0.85

def keten(q, pts, ra, rb):
    """buis langs een reeks punten, straal van ra naar rb"""
    d = None; n = len(pts) - 1
    for i in range(n):
        a = ra + (rb - ra) * i / n; b = ra + (rb - ra) * (i + 1) / n
        c = capsule(q, pts[i], pts[i + 1], a, b)
        d = c if d is None else np.minimum(d, c)
    return d

class Potoo3:
    def __init__(s, P):
        s.P = P; r = P['r_oog']
        s.ro = r * P['oog_mul']
        s.kc = np.array([0.0, 0, 4.0]); s.kr = (11.0, 12.5, P['kruin'] - 0.5)   # brede ronde bol, oog midden in de kop   # kop: gaplijn ~ z=0, kruin ~ z=P['kruin']+4
        s.hoek = np.array([-2.0, 0, 0.0])                                        # mondhoeken (scharnier // Y)
        # voorpunt van de kop op gaplijnhoogte
        xs = np.linspace(0, 20, 801); pts = np.stack([xs, 0 * xs, 0 * xs + 0.8], -1)
        s.voor = xs[np.where(s.kop_sdf(pts) < 0)[0].max()]
        # gaplijn-rand: punten op het kopoppervlak, van mondhoek naar voorpunt (rechte lijn in zijaanzicht, licht stijgend)
        s.rand = {}
        for kant in (-1, 1):
            pp = []
            for t in np.linspace(0, 1, 14):
                x = s.hoek[0] + (s.voor - s.hoek[0]) * t; z = 0.8 * t
                ys = np.linspace(0, 16, 641); P3 = np.stack([0 * ys + x, ys, 0 * ys + z], -1)
                inn = np.where(s.kop_sdf(P3) < 0)[0]
                y = ys[inn.max()] if len(inn) else 0
                pp.append((x, kant * y * (1 - 0.04 * t), z))
            s.rand[kant] = pp
        s.hoek_y = s.rand[1][0][1]

    def kop_sdf(s, q):
        return supell(q, s.kc, s.kr, s.P['kop_p'])

    def gap(s, q):                       # >0 boven de gaplijn (licht stijgend naar voren)
        u = np.clip((q[..., 0] - s.hoek[0]) / 16.0, 0, 1)
        return q[..., 2] - 0.8 * u

    def kaak_plan(s, u):
        """halve breedte van de onderkaak (tussen de kaaktakken): V, licht bol, kleine golf naar de punt"""
        W0 = s.hoek_y
        return W0 * np.clip(1 - u, 0, 1) ** 0.7 * (1 + 0.30 * np.sin(math.pi * np.clip(u, 0, 1))) \
               + 0.25 * np.sin(np.clip(u, 0, 1) * math.pi * 4) * np.clip(u, 0, 1) ** 1.5 * (1 - np.clip(u, 0, 1))

    def velden(s, p):
        P = s.P; d = {}
        q = rot_y(p, (0, 0, -6), P['kop_op'])
        kop = s.kop_sdf(q)
        # wangen/keel onder de gaplijn achter de mondhoeken
        wang = ell(q, (-5.0, 0, -2.0), (9.0, s.hoek_y + 0.8, 6.5))
        d['kop'] = smin(np.maximum(kop, -s.gap(q)), np.maximum(wang, -s.gap(q) - 0.0) if False else wang, 3.0)
        d['koepel'] = kop; d['gap_q'] = s.gap(q)
        # harde rand van de bovensnavel (beide kanten) + haakje
        rnd = np.minimum(keten(q, s.rand[1], 0.45, 0.4), keten(q, s.rand[-1], 0.45, 0.4))
        d['rand_boven'] = rnd
        fx = s.voor
        A = (fx - 1.0, 0, 1.6); M = (fx + 0.6, 0, 1.0); E = (fx + 0.5, 0, -1.6)
        d['haak'] = np.minimum(capsule(q, A, M, 0.75, 0.55), capsule(q, M, E, 0.55, 0.06))
        # ---- onderkaak (in gesloten stand gedefinieerd, dan open gedraaid om de mondhoeken) ----
        qo = rot_y(q, s.hoek, -P['open'])
        L = P['kaak_len']
        u = (qo[..., 0] - s.hoek[0]) / L
        W = s.kaak_plan(u)
        # kaaktakken: buizen langs de planvorm
        tak = None
        for kant in (-1, 1):
            pts = [(s.hoek[0] + L * t, kant * float(s.kaak_plan(np.array(t))), -0.15 - 0.2 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 16)]
            k_ = keten(qo, pts, 0.5, 0.28)
            tak = k_ if tak is None else np.minimum(tak, k_)
        d['tak'] = tak
        # buidel: huid tussen de takken, hangt door (diep bij de mondhoeken, ondiep naar de punt)
        yn = np.clip(np.abs(qo[..., 1]) / np.maximum(W, 0.3), 0, 1.5)
        diep = 5.5 * np.clip(1 - yn ** 2, 0, 1) ** 0.6 * np.clip(1 - u, 0, 1) ** 0.8 * (u > -0.02)
        zb = -0.2 - diep
        buidel = np.maximum(np.abs(qo[..., 2] - zb + 0.45) - 0.45, np.maximum(np.abs(qo[..., 1]) - W, np.maximum(-u * L, (u - 1) * L)))
        d['buidel'] = buidel; d['buidel_z'] = qo[..., 2] - zb; d['kaak_u'] = u
        # mondruimte: volume boven de buidel tot de gaplijn, meegedraaid -> niets van kop/lijf in de open muil
        ruimte = None
        for i in range(0, 9):
            qi = rot_y(q, s.hoek, -P['open'] * i / 8)
            ui = (qi[..., 0] - s.hoek[0]) / L; Wi = s.kaak_plan(ui)
            yi = np.clip(np.abs(qi[..., 1]) / np.maximum(Wi, 0.3), 0, 1.5)
            di = 5.5 * np.clip(1 - yi ** 2, 0, 1) ** 0.6 * np.clip(1 - ui, 0, 1) ** 0.8
            v = np.maximum.reduce([np.abs(qi[..., 1]) - Wi + 0.6, -(qi[..., 2] - (-0.2 - di)) + 0.3, qi[..., 2] - 0.0 - 0.0 * ui,
                                   (s.hoek[0] + 1.5) - qi[..., 0], (ui - 1) * L])
            ruimte = v if ruimte is None else np.minimum(ruimte, v)
        keel = ell(qo, (s.hoek[0] + 2.0, 0, -1.5), (4.5, s.hoek_y * 0.75, 3.5))
        gewelf = ell(q, (4.0, 0, 0.0), (8.5, s.hoek_y * 0.72, 2.2))
        d['ruimte'] = np.minimum.reduce([ruimte, keel, gewelf])
        # ---- ogen ----
        ogen = None; s.oog_c = []
        for kant in (-1, 1):
            az = math.radians(P['oog_az']); z0 = P['oog_h']
            dirn = np.array([math.cos(az), kant * math.sin(az), 0.0])
            ts = np.linspace(0, 20, 801); pts = s.kc * np.array([1, 0, 0]) + np.array([0, 0, z0]) + ts[:, None] * dirn
            t_ = ts[np.where(s.kop_sdf(pts) < 0)[0].max()]
            pnt = s.kc * np.array([1, 0, 0]) + np.array([0, 0, z0]) + t_ * dirn
            n = dirn.copy(); n /= np.linalg.norm(n)
            c = pnt - n * 0.30 * s.ro; s.oog_c.append((c, n))
            e = np.linalg.norm(q - c, axis=-1) - s.ro
            ogen = e if ogen is None else np.minimum(ogen, e)
        d['oog'] = ogen
        # ---- rug met korte veertjes tussen de ogen, naar het haakje ----
        rug = ell(q, (fx - 2.8, 0, P['oog_h'] + 1.2), (3.4, 3.0, 4.6))
        veer = rug
        for t in np.linspace(0.0, 1.0, 6):
            zz = P['oog_h'] + 4.0 - t * 4.5
            for kant in (-1, 1):
                yy = kant * (2.4 - 1.4 * t)
                xs = np.linspace(0, 20, 401); pts = np.stack([xs, 0 * xs + yy, 0 * xs + zz], -1)
                inn = np.where(np.minimum(s.kop_sdf(pts), ell(pts, (fx - 2.8, 0, P['oog_h'] + 1.2), (3.4, 3.0, 4.6))) < 0)[0]
                if not len(inn): continue
                b = np.array([xs[inn.max()] - 0.2, yy, zz]); e = b + np.array([0.8, kant * 0.3, -0.45])
                veer = smin(veer, capsule(q, b, e, 0.30, 0.04), 0.2)
        d['veer'] = veer
        # ---- lijf uit v2 ----
        lijf = V2.Potoo(dict(V2.params('A'), **{k: P[k] for k in ('voorover', 'lijf_len')}))
        dl = lijf.velden_lijf(p) if hasattr(lijf, 'velden_lijf') else None
        if dl is None:
            dv = lijf.velden(p); dl = {k: dv[k] for k in ('lijf', 'vleugel', 'staart')}
        d.update(dl)
        return d

    def huid(s, p):
        d = s.velden(p)
        romp = smin(smin(d['lijf'], d['vleugel'], 1.2), d['staart'], 1.5)
        kop = smin(d['kop'], d['veer'], 0.5)
        g = smin(kop, romp, 5.0)
        g = np.maximum(g, -d['ruimte'])
        g = smin(g, d['rand_boven'], 0.25)
        g = np.minimum(g, smin(d['buidel'], d['tak'], 0.4))
        g = smin(g, d['haak'], 0.3)
        g = np.minimum(g, d['oog'])
        return g, d

KLEUR = dict(V2.KLEUR); KLEUR.update(rand=(0.90, 0.88, 0.93), punt=(0.22, 0.20, 0.26))
NAMEN = list(KLEUR)

def kleur(po, C):
    g, d = po.huid(C)
    lab = np.full(len(C), NAMEN.index('vacht'))
    def zet(m, n): lab[m] = NAMEN.index(n)
    near = lambda f, e=0.4: np.abs(f) < e
    zet(d['vleugel'] < 0.4, 'vleugel'); zet(d['staart'] < 0.4, 'vleugel')
    geh = near(d['ruimte'], 0.45) & (d['oog'] > 0.3) & (d['haak'] > 0.3) & (d['rand_boven'] > 0.2)
    zet(geh, 'mond')
    zet(geh & (np.abs(C[:, 1]) < 0.45) & (C[:, 0] > 0) & (C[:, 0] < 8), 'keel')
    bui = near(d['buidel'], 0.4) & (d['tak'] > 0.15)
    zet(bui & (d['buidel_z'] > -0.45), 'mond')                 # bovenkant van de huid = binnenkant muil
    zet(bui & (d['buidel_z'] > -0.45) & (d['kaak_u'] < 0.18), 'keel')
    zet(near(d['tak'], 0.4) | near(d['rand_boven'], 0.35), 'rand')
    zet(near(d['tak'], 0.4) & (d['kaak_u'] > 0.86), 'punt')
    zet(near(d['haak'], 0.3), 'haak')
    zet(d['oog'] < 0.3, 'oog')
    return lab

def bouw(po, stap=0.28, alleen_kop=False):
    from skimage import measure
    lo = np.array([-34.0, -24.0, -100.0 if not alleen_kop else -34.0]); hi = np.array([22.0, 24.0, 20.0])
    xs, ys, zs = [np.arange(lo[i], hi[i], stap) for i in range(3)]
    vals = np.empty((len(xs), len(ys), len(zs)), np.float32)
    for i in range(len(xs)):
        Pp = np.stack(np.meshgrid([xs[i]], ys, zs, indexing='ij'), -1).reshape(-1, 3)
        vals[i] = po.huid(Pp)[0].reshape(len(ys), len(zs))
    v, f, _, _ = measure.marching_cubes(vals, 0.0, spacing=(stap,) * 3); v += lo
    bpy.ops.wm.read_factory_settings(use_empty=True)
    me = bpy.data.meshes.new('Potoo'); me.from_pydata(v.tolist(), [], f[:, ::-1].tolist()); me.update()
    ob = bpy.data.objects.new('Potoo', me); bpy.context.collection.objects.link(ob)
    for n in NAMEN:
        m = bpy.data.materials.new(n); m.diffuse_color = (*KLEUR[n], 1); ob.data.materials.append(m)
    C = np.array([tuple(pl.center) for pl in me.polygons])
    me.polygons.foreach_set('material_index', kleur(po, C).astype(np.int32))
    me.polygons.foreach_set('use_smooth', np.ones(len(me.polygons), bool)); me.update()
    sm = ob.modifiers.new('glad', 'SMOOTH'); sm.factor = 0.5; sm.iterations = 2
    return ob

HOEKEN = dict(V2.HOEKEN); HOEKEN.update({'kop_leidraad_r': (-62, -10), 'kop_close_r': (-35, -12), 'kop_zij': (90, 0), 'kop_voor': (0, -8)})

if __name__ == '__main__':
    uit = sys.argv[1]; var = sys.argv[2]; namen = sys.argv[3].split(',')
    os.makedirs(uit, exist_ok=True)
    P = params(var)
    for kv in os.environ.get('PARAM', '').split(','):
        if kv: k_, v_ = kv.split('='); P[k_] = float(v_)
    po = Potoo3(P)
    bouw(po)
    cam = V2.camera()
    for n in namen:
        kop = n.startswith('kop')
        V2.kijk(cam, *HOEKEN[n], doel=(3, 0, 0) if kop else (-6, 0, -38))
        cam.data.ortho_scale = 44 if kop else 125
        bpy.context.scene.render.filepath = os.path.join(uit, f'{var}_{n}.png')
        bpy.ops.render.render(write_still=True)
