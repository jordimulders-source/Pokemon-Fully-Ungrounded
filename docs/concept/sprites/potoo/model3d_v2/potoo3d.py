"""Great potoo (Ghost/Normal) als 3D-model: één doorlopende huid uit afstandsvelden (smooth union), marching cubes,
Blender Workbench-render met omlijning. Wereld: X = voorwaarts (snavel), Y = links, Z = omhoog; eenheden: oogstraal r = 2.4.
Maten gemeten op de foto's (oogstraal r): oogafstand ~5r, kruin ~4r boven het oogmidden, mondhoek ~2r achter en ~1,2r onder
het oog, snaveltip ~4r voor het oog, onderkaak ~6r lang; lijf ~1,4x kopbreedte; kop-kruin tot staartpunt ~4 kopbreedtes.
De bek: kop = schedel + brede platte bovensnavel (het gezicht); de gaplijn loopt van de mondhoek (achter het oog) naar het
haakje; de onderkaak is het deel onder de gaplijn, scharniert in de mondhoeken en is een holle schep met spitse punt.
Gebruik: python3.11 potoo3d.py uitmap [A|B]   (A = gemeten echte vogel, B = Pokémon-aanpassingen)"""
import bpy, math, sys, os
import numpy as np
from mathutils import Vector

# ---------------- parameters ----------------
def params(variant):
    P = dict(r_oog=2.4, kop=1.0, oog_mul=1.0, open=68, voorover=8, kop_op=6, lijf_len=1.0, kaak_len=16.5)
    if variant == 'B':          # Pokémon-stap: kop 10% groter, ogen 25% groter, lijf 10% korter
        P.update(kop=1.08, oog_mul=1.25, lijf_len=0.85, kaak_len=21.0)
    return P

# ---------------- SDF-bouwstenen ----------------
def ell(p, c, r):
    q = (p - np.array(c, float)) / np.array(r, float)
    k0 = np.linalg.norm(q, axis=-1)
    k1 = np.linalg.norm(q / np.array(r, float), axis=-1)
    return k0 * (k0 - 1) / np.maximum(k1, 1e-6)          # goede benadering van ellipsoïde-afstand

def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)

def blad(p, A, B, ra, rb, plat, as_plat=1):
    """taps blad: capsule van A naar B, straal ra->rb, platgedrukt langs as_plat (0=x,1=y)"""
    A, B = np.array(A, float), np.array(B, float); ab = B - A
    t = np.clip(((p - A) @ ab) / (ab @ ab), 0, 1)
    q = p - (A + t[..., None] * ab)
    s = np.ones(3); s[as_plat] = 1 / plat
    return np.linalg.norm(q * s, axis=-1) * 1.0 - (ra + (rb - ra) * t)

def capsule(p, A, B, ra, rb):
    return blad(p, A, B, ra, rb, 1.0)

def rot_y(p, c, hoek):
    """draai punten p om de as // Y door c over 'hoek' graden (positief = voorkant omlaag)"""
    a = math.radians(hoek); co, si = math.cos(a), math.sin(a)
    d = p - np.array(c, float)
    x = d[..., 0] * co + d[..., 2] * si; z = -d[..., 0] * si + d[..., 2] * co
    return np.stack([x + c[0], d[..., 1] + c[1], z + c[2]], -1)

# ---------------- de vogel ----------------
class Potoo:
    """Kop volgens de leidraad (linkerhelft duo-foto): hoge ronde koepel zonder nek, gaplijn op de breedste plek,
    mondhoeken ver opzij/achter, ogen voor-opzij; onderkaak = ondiepe schep met spitse punt die bijna verticaal openhangt.
    Lijf uit de nachtfoto: ~1,5x kopbreedte, breedst 1,5-2 kopbreedtes onder de kruin, staartpunt ~4 kopbreedtes."""
    def __init__(s, P):
        s.P = P; s.K = P['kop']; K = s.K; r = P['r_oog']
        s.koepel = ((2.5 * K, 0, 4.0 * K), (12.5 * K, 12.0 * K, 12.8 * K))   # ogen op de breedste plek, gaplijn eronder     # kruin 3r boven het oog, kop 10r breed
        s.hoek_x = -2.0 * K                                         # mondhoeken: ~2r achter het oog (projectie)
        s.hinge = np.array([s.hoek_x, 0, 0.0])
        s.kaak_len = P['kaak_len'] * K
        s.ro = r * P['oog_mul']
        s.oog_h = 5.2 * K                                           # oogmidden 2r boven de gaplijn
        s.oog_az = math.radians(47)

    def gaplijn(s, q):
        """>0 boven de gaplijn; stijgt licht naar voren (leidraad), kleine golf naar de punt"""
        u = np.clip((q[..., 0] - s.hoek_x) / (17.0 * s.K), 0, 1)
        return q[..., 2] - (1.4 * s.K * u ** 1.5 + 0.25 * s.K * np.sin(u * math.pi * 3) * u ** 2)

    def kop_boven(s, q):
        return np.maximum(ell(q, *s.koepel), -s.gaplijn(q))

    def kaak_dicht(s, q):
        """onderkaak in gesloten stand: ondiepe schep, planvorm breed bij de mondhoeken, holle zijkanten naar een spitse punt"""
        K = s.K; L = s.kaak_len
        u = (q[..., 0] - s.hoek_x) / L
        uc = np.clip(u, 0, 1)
        W = 12.8 * K * np.minimum(np.clip(1 - uc ** 1.8, 0, 1) ** 0.6 * (1 + 0.32 * np.sin(math.pi * uc)), 3.4 * (1 - uc))   # buidel bolt opzij uit   # bolle U, spitse punt
        plan = np.maximum.reduce([np.abs(q[..., 1]) - W, -u * L, (u - 1) * L])
        schaal = ell(q, (s.hoek_x + L * 0.5, 0, 0.6 * K), (L * 0.62, 16.2 * K, 6.0 * K))
        return np.maximum.reduce([schaal, plan, s.gaplijn(q)])

    def velden(s, p):
        P = s.P; K = s.K; d = {}
        q = rot_y(p, (0, 0, -8), P['kop_op'])          # + = kop achterover (snavel omhoog)                       # kop-assenstelsel (kop iets omhoog)
        d['kop'] = smin(s.kop_boven(q), ell(q, (-5.0 * K, 0, -1.0 * K), (9.0 * K, 11.8 * K, 7.0 * K)), 4.0)   # + wangen/keel
        qo = rot_y(q, s.hinge, -P['open'])
        dicht = s.kaak_dicht(qo)
        d['kaak_binnen'] = ell(qo, (s.hoek_x + s.kaak_len * 0.5, 0, 0.6 * K), (s.kaak_len * 0.62 - 0.9 * K, 15.3 * K, 5.1 * K))
        d['kaak'] = np.maximum(dicht, -d['kaak_binnen'])     # holle schep, open aan de bovenkant
        d['kaak_gap'] = s.gaplijn(qo); d['gap_q'] = s.gaplijn(q); d['koepel'] = ell(q, *s.koepel)
        d['kaak_u'] = (qo[..., 0] - s.hoek_x) / s.kaak_len
        ruimte = None
        for i in range(0, 11):
            qi = rot_y(q, s.hinge, -P['open'] * i / 10)
            v = np.maximum(s.kaak_dicht(qi), s.hoek_x + 1.2 * K - qi[..., 0]) + 0.2
            ruimte = v if ruimte is None else np.minimum(ruimte, v)
        keel = ell(qo, (s.hoek_x + 2.5 * K, 0, -1.0 * K), (5.5 * K, 9.0 * K, 4.5 * K))   # holte achter in de muil
        gewelf = ell(q, (4.0 * K, 0, 0.2 * K), (8.5 * K, 7.5 * K, 2.6 * K))      # gehemelte hol, niet plat
        d['ruimte'] = np.minimum(np.minimum(ruimte, keel), gewelf)
        # klein donker haakje op de punt van de bovensnavel, krult omlaag
        fx = 2.5 * K + 12.5 * K * math.sqrt(1 - (2.6 / 12.8) ** 2) - 0.2; fz = 1.4 * K
        A = (fx - 1.2 * K, 0, fz + 0.9 * K); M = (fx + 0.3 * K, 0, fz + 0.1 * K); E = (fx + 0.1 * K, 0, fz - 1.9 * K)
        d['haak'] = np.minimum(capsule(q, A, M, 0.8 * K, 0.5 * K), capsule(q, M, E, 0.5 * K, 0.07 * K))
        # ogen: bolle kralen op de koepel, voor-opzij
        s.oog_c = []; ogen = None
        a, R = s.koepel[1], None
        for kant in (-1, 1):
            c0 = s.koepel[0]; el_ = math.asin((s.oog_h - c0[2]) / a[2])
            n0 = np.array([math.cos(el_) * math.cos(s.oog_az), kant * math.cos(el_) * math.sin(s.oog_az), math.sin(el_)])
            pnt = n0 * np.array(a) + np.array(c0)
            n = (pnt - np.array(c0)) / np.array(a) ** 2; n /= np.linalg.norm(n)
            c = pnt - n * 0.32 * s.ro
            s.oog_c.append((c, n))
            e = np.linalg.norm(q - c, axis=-1) - s.ro
            ogen = e if ogen is None else np.minimum(ogen, e)
        d['oog'] = ogen
        # kleine veertjes tussen de ogen (Jordi): korte pluimpjes in een V van tussen de ogen naar het haakje
        veer = None
        for i, t in enumerate(np.linspace(0.0, 1.0, 6)):
            zz = s.oog_h + 3.0 * K - t * 4.5 * K
            for kant in (-1, 1):
                yy = kant * (2.6 - 1.6 * t) * K
                xx = 2.5 * K + 12.5 * K * math.sqrt(max(0.0, 1 - (yy / (12 * K)) ** 2 - ((zz - 4.0 * K) / (12.8 * K)) ** 2)) + 0.6
                b = np.array([xx, yy, zz]); e = b + np.array([0.9 * K, kant * 0.35 * K, -0.5 * K])
                c_ = capsule(q, b, e, 0.32 * K, 0.04 * K)
                veer = c_ if veer is None else smin(veer, c_, 0.2)
        # bevederde rug tussen de ogen tot aan het haakje (close-up en leidraad: verbergt het verre oog van opzij)
        fx0 = 2.5 * K + 12.5 * K * math.sqrt(1 - (2.6 / 12.8) ** 2)
        rug = smin(ell(q, (fx0 - 2.4 * K, 0, s.oog_h + 2.0 * K), (3.6 * K, 3.6 * K, 4.6 * K)),
                   ell(q, (fx0 - 1.2 * K, 0, 2.6 * K), (2.4 * K, 2.4 * K, 2.4 * K)), 1.5)
        veer = smin(veer, rug, 1.0)
        d['veer'] = veer
        # ---- lijf (voorover gekanteld) ----
        b = rot_y(p, (0, 0, -10), -P['voorover'])      # + = bovenlijf naar voren
        L = P['lijf_len']
        z = lambda v: v * L
        # lijf: één gladde taps toelopende vorm; halve breedte W, halve diepte D en midden X per hoogte (nachtfoto, H = 24)
        prof = np.array([  # z,    W,    D,    X
            [9.0, 0.5, 0.5, -9.0], [5.0, 9.5, 7.0, -11.5], [0.0, 12.5, 8.0, -13.0], [-6, 16.0, 10.0, -14.5], [-14, 18.5, 11.5, -14.0],
            [-26, 19.5, 12.5, -12.0], [-40, 18.5, 12.5, -11.5], [-52, 16.0, 11.0, -11.5], [-62, 12.5, 8.5, -12.5],
            [-70, 8.0, 5.5, -13.5], [-76, 0.5, 0.5, -14.0]])
        zz = b[..., 2] / L
        zf = np.linspace(-80, 10, 361); kern = np.hanning(41); kern /= kern.sum()
        glad = lambda col: np.convolve(np.pad(np.interp(zf, prof[::-1, 0], prof[::-1, col]), 20, mode='edge'), kern, 'valid')
        W = np.interp(zz, zf, glad(1)); D = np.interp(zz, zf, glad(2)); X = np.interp(zz, zf, glad(3))
        rr = np.sqrt((b[..., 1] / W) ** 2 + ((b[..., 0] - X) / D) ** 2)
        d['lijf'] = (rr - 1) * np.minimum(W, D) * 0.9 + np.maximum(0, zz - 9) + np.maximum(0, -76 - zz)
        vl = None
        for kant in (-1, 1):       # vleugels plat tegen de flanken, van net onder de kop tot over de staartbasis
            v = smin(smin(blad(b, (-8.0, kant * 15.5, z(-4)), (-10.0, kant * 18.5, z(-22)), 5.5, 6.5, 0.32),
                          blad(b, (-10.0, kant * 18.5, z(-22)), (-12.5, kant * 15.5, z(-52)), 6.5, 5.0, 0.32), 2.0),
                     blad(b, (-12.5, kant * 15.5, z(-52)), (-15.5, kant * 6.0, z(-76)), 5.0, 1.0, 0.32), 2.0)
            vl = v if vl is None else np.minimum(vl, v)
        d['vleugel'] = vl
        d['staart'] = blad(b, (-14.0, 0, z(-60)), (-17.5, 0, z(-92)), 7.5, 4.5, 0.25, as_plat=0)
        return d

    def huid(s, p):
        d = s.velden(p)
        romp = smin(smin(d['lijf'], d['vleugel'], 1.2), d['staart'], 1.5)
        kop = smin(d['kop'], d['veer'], 0.3)
        geheel = smin(kop, romp, 5.0 * s.K)
        geheel = np.maximum(geheel, -d['ruimte'])          # niets van lijf/kop in de open muil
        geheel = smin(geheel, d['kaak'], 0.9)          # kaak loopt glad over in de mondhoeken
        geheel = smin(geheel, d['haak'], 0.3)
        geheel = np.minimum(geheel, d['oog'])
        return geheel, d

# ---------------- kleuren ----------------
KLEUR = dict(vacht=(0.93, 0.92, 0.96), buik=(0.98, 0.97, 1.0), vleugel=(0.70, 0.68, 0.78), vlek=(0.52, 0.47, 0.50),
             oog=(0.0, 0.0, 0.0), mond=(0.40, 0.34, 0.86), keel=(0.14, 0.10, 0.36), rand=(0.86, 0.84, 0.92),
             haak=(0.16, 0.14, 0.18), punt=(0.30, 0.27, 0.34))
NAMEN = list(KLEUR)

def kleur_per_vlak(potoo, C):
    g, d = potoo.huid(C)
    lab = np.full(len(C), NAMEN.index('vacht'))
    def zet(m, n): lab[m] = NAMEN.index(n)
    near = lambda f, e=0.35: np.abs(f) < e
    zet(d['vleugel'] < 0.4, 'vleugel'); zet(d['staart'] < 0.4, 'vleugel')
    # schorsvlekken: een paar onregelmatige vlekken op vleugels en kruin (Hisui-Zorua-idee), vast patroon
    rng = np.random.default_rng(7)
    vlekken = [(-8, 13, -22, 2.2), (-9, 12, -32, 1.8), (-10, 9, -46, 2.0), (-8, -13, -24, 2.0), (-10, -10, -42, 1.9),
               (-12, 0, -60, 2.2), (-5, 4, 7, 1.6), (-7, -5, 5, 1.4)]
    for x, y, z, rr in vlekken:
        c = np.array([x, y, z], float)
        m = np.linalg.norm((C - c) * np.array([1, 1, 0.55]), axis=-1) < rr
        zet(m & (d['oog'] > 0.3), 'vlek')
    buik = (d['lijf'] < 0.4) & (d['vleugel'] > 0.6) & (C[:, 0] > -2) & (C[:, 2] < -12)
    zet(buik, 'buik')
    # bek: mondkleur alleen binnen de mondrand
    opk = near(d['kaak'], 0.4)
    zet(opk & (d['kaak_binnen'] < 0.45), 'mond')                       # binnenkant van de schep
    zet(opk & (np.abs(d['kaak_gap']) < 0.45) & (d['kaak_binnen'] > 0.25) & (d['kaak_u'] > 0.06), 'rand')   # dunne lichte rand
    zet(opk & (d['kaak_u'] > 0.9) & (d['kaak_binnen'] > 0.3), 'punt')
    geh = (np.abs(d['ruimte']) < 0.45) & ~opk & (d['oog'] > 0.3) & (d['haak'] > 0.3)
    zet(geh, 'mond')                                                    # gehemelte
    zet(geh & (np.abs(C[:, 1]) < 0.45) & (C[:, 0] > 0) & (C[:, 0] < 8), 'keel')   # donkere spleet in het gehemelte
    zet(near(d['haak'], 0.3) & (d['haak'] <= d['kop'] + 0.1), 'haak')
    zet(d['oog'] < 0.3, 'oog')
    return lab

# ---------------- Blender ----------------
def bouw_mesh(potoo, stap=0.3, draai=0.0):
    from skimage import measure
    lo = np.array([-36.0, -27.0, -100.0]); hi = np.array([18.0, 27.0, 16.0])
    xs, ys, zs = [np.arange(lo[i], hi[i], stap) for i in range(3)]
    vals = np.empty((len(xs), len(ys), len(zs)), np.float32)
    for i in range(len(xs)):                 # per plak om geheugen te sparen
        P = np.stack(np.meshgrid([xs[i]], ys, zs, indexing='ij'), -1).reshape(-1, 3)
        vals[i] = potoo.huid(P)[0].reshape(len(ys), len(zs))
    v, f, _, _ = measure.marching_cubes(vals, 0.0, spacing=(stap, stap, stap))
    v += lo
    bpy.ops.wm.read_factory_settings(use_empty=True)
    me = bpy.data.meshes.new('Potoo'); me.from_pydata(v.tolist(), [], f[:, ::-1].tolist()); me.update()
    ob = bpy.data.objects.new('Potoo', me); bpy.context.collection.objects.link(ob)
    for n in NAMEN:
        m = bpy.data.materials.new(n); m.diffuse_color = (*KLEUR[n], 1); m.roughness = 0.7
        ob.data.materials.append(m)
    C = np.array([tuple(pl.center) for pl in me.polygons])
    lab = kleur_per_vlak(potoo, C)
    me.polygons.foreach_set('material_index', lab.astype(np.int32))
    me.polygons.foreach_set('use_smooth', np.ones(len(me.polygons), bool))
    me.update()
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    sm = ob.modifiers.new('glad', 'SMOOTH'); sm.factor = 0.5; sm.iterations = 2
    return ob

def camera(res=600, schaal=110, hoogte=-34):
    sc = bpy.context.scene
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = schaal
    sc.render.engine = 'BLENDER_WORKBENCH'
    sh = sc.display.shading
    sh.light = 'STUDIO'; sh.color_type = 'MATERIAL'
    sh.show_object_outline = True; sh.object_outline_color = (0.08, 0.06, 0.12)
    sh.show_cavity = True; sh.cavity_type = 'WORLD'
    sc.render.film_transparent = True; sc.view_settings.view_transform = 'Standard'
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    return cam

def kijk(cam, yaw, pitch, doel=(0, 0, -34)):
    """camera op horizontale hoek yaw (0 = recht van voren, +90 = van links van de vogel) en hoogte pitch"""
    a, b = math.radians(yaw), math.radians(pitch)
    d = Vector((math.cos(a) * math.cos(b), math.sin(a) * math.cos(b), math.sin(b)))
    cam.location = Vector(doel) + d * 200
    cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()

HOEKEN = {   # naam: (yaw, pitch)  -- de vogel kijkt naar +X; 'sprite' = 3/4 naar links op het scherm
    'sprite_34': (40, 8), 'voor': (0, 5), 'zij_links': (90, 0), 'zij_rechts': (-90, 0), 'achter': (180, 5),
    'schuin_achter': (140, 15), 'boven': (30, 60), 'onder_voor': (25, -25), 'kop_34': (40, 8), 'kop_leidraad': (62, -15), 'kop_zij': (90, 0), 'kop_voor': (0, -10), 'kop_leidraad_r': (-62, -15)}

if __name__ == '__main__':
    uit = sys.argv[1]; var = sys.argv[2] if len(sys.argv) > 2 else 'A'
    namen = sys.argv[3].split(',') if len(sys.argv) > 3 else list(HOEKEN)
    os.makedirs(uit, exist_ok=True)
    P = params(var)
    for kv in os.environ.get('PARAM', '').split(','):
        if kv: k_, v_ = kv.split('='); P[k_] = float(v_)
    po = Potoo(P)
    ob = bouw_mesh(po)
    cam = camera()
    for n in namen:
        kijk(cam, *HOEKEN[n], doel=(2, 0, -2) if n.startswith('kop') else (-6, 0, -38))
        cam.data.ortho_scale = 46 if n.startswith('kop') else 125
        bpy.context.scene.render.filepath = os.path.join(uit, f'{var}_{n}.png')
        bpy.ops.render.render(write_still=True)
