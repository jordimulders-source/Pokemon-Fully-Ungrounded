"""Evolutie van Picapau (Electric/Flying, eindvorm) als 3D-model in Blender (bpy).
Opbouw, eenheden en render overgenomen van ../../picapau/blender/picapau.py (dat model is bevroren en blijft ongemoeid).
Eenheden = spritepixels: Blender (X, Z) = (x - 32, 32 - y) van de 64x64-sprite, Y = diepte (camera aan -Y); de vogel kijkt naar -X.
Jordi (SPEC): "imposant, groot, opgeblazen" · vleugels half open (dreigend) · "krullende oren" (= kuif) ·
"echt zon krullende staart met een bliksemschicht" · kastanje lijf, kuif en buik licht crème.
Nieuw t.o.v. Picapau: de kop (met kuif, snavel, ogen, wang) heeft een EIGEN draai om de nek (kop_draai), zodat
de kop meer naar de kijker staat dan het lijf (les Picapau: profielkop zonder kopdraai gaf geen 3/4).
Huid = één oppervlak (smooth union van afstandsvelden); kleurvlakken per vlak; snavel, ogen, tong en pootjes los.
Draaien: python3.11 picapau_evo.py [uitmap] [hoeken...]   (rondom-vel)"""
import bpy, math, sys, os
import numpy as np
from mathutils import Vector, Euler, Matrix

KLEUR = dict(lijf=(0.96, 0.46, 0.10),      # oranje-kastanje (Celeus elegans)
             vleugel=(0.50, 0.19, 0.05),   # donkerder kastanje
             stip=(0.96, 0.84, 0.58),      # ronde lichte stippen (familie Picapau)
             staart=(0.62, 0.24, 0.06),    # pluim: donker roodbruin
             bliksem=(1.0, 0.82, 0.10),    # bliksempunt: geel (Electric)
             creme=(1.0, 0.94, 0.70),     # kuif en buik
             wang=(0.88, 0.10, 0.10), snavel=(0.94, 0.86, 0.50), oog=(0.02, 0.01, 0.01), glans=(1, 1, 1),
             poot=(0.25, 0.25, 0.27), tong=(0.95, 0.45, 0.55))

def mat(naam):
    m = bpy.data.materials.get(naam) or bpy.data.materials.new(naam)
    c = KLEUR[naam]; m.diffuse_color = (*c, 1); m.roughness = 0.6
    return m

def leeg():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def koppel(ob, ouder):
    bpy.context.view_layer.update(); w = ob.matrix_world.copy(); ob.parent = ouder; ob.matrix_world = w

def bol(naam, co, schaal, kleur, ouder=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=co)
    ob = bpy.context.object; ob.name = naam; ob.scale = schaal; ob.rotation_euler = rot
    bpy.ops.object.shade_smooth(); ob.data.materials.append(mat(kleur))
    if ouder: koppel(ob, ouder)
    return ob

def wig(naam, basis, d, lengte, breed, hoog, kleur, ouder):
    """snavelhelft: kegel met platte doorsnede, punt in richting d (vector)"""
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=1.0, radius2=0.08, depth=lengte, location=(0, 0, 0))
    ob = bpy.context.object; ob.name = naam
    ob.scale = (hoog, breed, 1)
    d = Vector(d).normalized()
    ob.rotation_euler = Vector((0, 0, 1)).rotation_difference(d).to_euler()
    ob.location = Vector(basis) + d * (lengte / 2)
    bpy.ops.object.shade_smooth(); ob.data.materials.append(mat(kleur))
    koppel(ob, ouder)
    return ob

def familie(naam, elementen, kleur, ouder=None, voxel=0.15, glad=2):
    obs = []
    for co, r in elementen:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=co)
        ob = bpy.context.object; ob.scale = r; obs.append(ob)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in obs: ob.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if len(obs) > 1: bpy.ops.object.join()
    ob = bpy.context.object; ob.name = naam
    m = ob.modifiers.new('remesh', 'REMESH'); m.mode = 'VOXEL'; m.voxel_size = voxel
    sm = ob.modifiers.new('glad', 'SMOOTH'); sm.factor = 1.0; sm.iterations = glad
    bpy.ops.object.shade_smooth(); ob.data.materials.append(mat(kleur))
    if ouder: koppel(ob, ouder)
    return ob


# ---------------- afstandsvelden ----------------
def sdf_deel(P, deel):
    """('ell', midden, stralen, rot_y) | ('buis', [(punt, straal), ...], normaal, plat)
    buis = keten van taps toelopende capsules, plat langs 'normaal' (plat<1 = dunner in die richting)"""
    if deel[0] == 'ell':
        _, co, r, ry = deel
        p = P - np.array(co, np.float32)
        a = math.radians(ry); c, s = math.cos(-a), math.sin(-a)
        px, py, pz = p[..., 0] * c + p[..., 2] * s, p[..., 1], -p[..., 0] * s + p[..., 2] * c
        q = np.sqrt((px / r[0]) ** 2 + (py / r[1]) ** 2 + (pz / r[2]) ** 2)
        return (q - 1) * min(r)
    _, keten, n, plat = deel
    n = np.array(n, np.float32); n /= np.linalg.norm(n)
    best = None
    for (A, ra), (B, rb) in zip(keten[:-1], keten[1:]):
        A = np.array(A, np.float32); B = np.array(B, np.float32); ab = B - A; L2 = ab @ ab
        u = ab / math.sqrt(L2); m = n - (n @ u) * u; m /= np.linalg.norm(m)   # plat alleen in de doorsnede
        t = np.clip(((P - A) @ ab) / L2, 0, 1)
        q = P - (A + t[..., None] * ab)
        qn = q @ m
        q = q + (qn / plat - qn)[..., None] * m
        d = np.linalg.norm(q, axis=-1) - (ra + (rb - ra) * t)
        best = d if best is None else smin(best, d, 0.8)      # glad in elkaar: geen ribbels op de knikken
    return best

def smin(a, b, k):
    if k <= 0: return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


# ---------------- de evolutie ----------------
NEK = Vector((-3.0, 0, 5.0))           # draaipunt van de kop
HEUP = Vector((-1.5, 0, -16.5))       # draaipunt van de romp (voorover)
KC = Vector((-8.5, 0, 12.5))           # kopmidden (kop-lokaal)
KR = (9.6, 9.2, 9.3)                   # grote ronde kop

def kop_matrix(kop_draai, kop_kantel=0.0):
    """kop-lokaal -> lijf: draai om Z (naar de kijker) en een kleine kanteling, rond NEK"""
    R = Matrix.Rotation(math.radians(kop_draai), 3, 'Z') @ Matrix.Rotation(math.radians(kop_kantel), 3, 'Y')
    return R

def vleugel(s):
    """half open, dreigend opgetrokken: arm schuin omhoog naar buiten, handpennen waaieren naar achter-onder;
    een brede handplaat houdt de pennen bij elkaar (alleen de punten komen los)"""
    schouder = (6.0, s * 9.5, 3.0); pols = (9.0, s * 19.0, 20.0)
    arm = np.array(pols) - np.array(schouder)
    n = np.cross(arm, np.array([1.0, 0, -0.35])); n = tuple(n / np.linalg.norm(n))
    d = [('vleugel', ('buis', [(schouder, 4.4), (pols, 3.4)], n, 0.45), 1.2),
         ('vleugel', ('buis', [((7.0, s * 12.0, 9.0), 5.5), ((15.0, s * 16.0, -3.0), 3.6), ((17.5, s * 17.0, -6.0), 2.6)], n, 0.4), 1.0)]
    # zes handpennen in een waaier; dik en overlappend aan de basis, alleen de punten los
    # vijf brede handpennen met ronde punten (naalden werden op 1x een egel)
    for tip in [(19.5, 24.5, 26.5), (24.5, 24.5, 18.0), (26.5, 23.5, 9.0), (25.0, 21.0, 0.5), (21.0, 18.5, -6.5)]:
        tip = (tip[0], s * tip[1], tip[2])
        mid = tuple(np.array(pols) + 0.6 * (np.array(tip) - np.array(pols)))
        d.append(('vleugel', ('buis', [(pols, 3.8), (mid, 3.2), (tip, 1.5)], n, 0.42), 1.4))
    return d

def staart_keten():
    """lange pluim: uit de stuit naar rechts-onder, onder het lijf door naar voren (S-boog), dan de bliksem"""
    return [((13.0, 1.0, -12.0), 4.0), ((20.0, 1.5, -14.0), 4.2), ((23.5, 2.5, -20.5), 3.8), ((20.0, 3.0, -26.5), 3.2),
            ((11.0, 3.5, -28.5), 2.7), ((1.0, 4.0, -27.5), 2.3), ((-6.5, 4.0, -24.5), 1.9), ((-10.5, 3.5, -21.0), 1.8)]

BLIKSEM = [((-10.5, 3.5, -21.0), 2.0), ((-19.0, 3.5, -18.0), 2.8), ((-14.0, 3.5, -14.0), 2.7), ((-23.5, 3.5, -6.0), 0.6)]

def delen(kop_draai=25.0, kop_kantel=0.0):
    """lijst (naam, deel, k, groep); groep 'kop' wordt met de kopdraai rond NEK geëvalueerd"""
    d = [('lijf', ('ell', (3.0, 0, -5.0), (14.0, 13.5, 13.5), -15), 0, 'lijf'),
         ('lijf', ('ell', (-4.5, 0, -3.0), (9.5, 10.5, 11.0), -10), 3.0, 'lijf'),     # opgezette borst
         ('lijf', ('ell', (-3.0, 0, 5.5), (6.5, 7.5, 6.5), 0), 3.0, 'lijf')]          # dikke nek
    # dijen in de huid: de poten groeien uit het lijf
    for s in (-1, 1):
        d.append(('lijf', ('ell', (-1.5, s * 4.5, -16.5), (3.2, 3.0, 3.2), 0), 1.5, 'lijf'))
    for naam, deel, k in vleugel(-1) + vleugel(1):
        d.append((naam, deel, k, 'lijf'))
    d.append(('staart', ('buis', staart_keten(), (0, 1, 0), 0.55), 1.2, 'lijf'))
    d.append(('bliksem', ('buis', BLIKSEM, (0, 1, 0), 0.42), 0.4, 'lijf'))
    # kop-groep (kop-lokale coördinaten)
    d.append(('kop', ('ell', tuple(KC), KR, 0), 3.5, 'kop'))
    # grote kuif: twee lange punten omhoog-achter, top krult naar buiten (Raichu-oren), plat van voor gezien
    for s in (-1, 1):
        keten = [((-7.5, s * 3.8, 19.5), 4.4), ((-6.0, s * 5.4, 25.0), 4.0), ((-4.5, s * 7.0, 29.5), 3.2),
                 ((-2.5, s * 9.5, 32.5), 2.9), ((-0.5, s * 13.0, 33.5), 2.8), ((0.5, s * 16.5, 31.5), 2.6),
                 ((0.5, s * 17.5, 27.5), 2.3), ((-0.5, s * 16.0, 24.0), 1.6)]   # haak: krult naar buiten en terug omlaag
        d.append(('kuif', ('buis', keten, (1, 0, 0.3), 0.34), 1.6, 'kop'))
    # korte rafelige achterkuif (familie Picapau)
    for a, b, ra in [((-2.0, 0, 18.0), (5.5, 0, 21.5), 3.0), ((-0.5, 0, 14.0), (6.5, 0, 15.0), 2.8)]:
        d.append(('kuif2', ('buis', [(a, ra), (b, 0.9)], (0, 1, 0), 1.6), 1.8, 'kop'))
    return d

def huid_sdf(dl, kop_draai, kop_kantel, stap=0.3):
    from skimage import measure
    lo = np.array([-36.0, -26.0, -36.0], np.float32); hi = np.array([36.0, 26.0, 38.0], np.float32)
    xs, ys, zs = [np.arange(lo[i], hi[i], stap, dtype=np.float32) for i in range(3)]
    Rinv = np.array(kop_matrix(kop_draai, kop_kantel).transposed(), np.float32)
    nek = np.array(NEK, np.float32)
    D = np.empty((len(xs), len(ys), len(zs)), np.float32)
    for i0 in range(0, len(xs), 24):
        P = np.stack(np.meshgrid(xs[i0:i0 + 24], ys, zs, indexing='ij'), -1)
        Pk = (P - nek) @ Rinv.T + nek
        d = None
        for naam, deel, k, groep in dl:
            di = sdf_deel(Pk if groep == 'kop' else P, deel)
            d = di if d is None else smin(d, di, k)
        D[i0:i0 + 24] = d
    v, f, _, _ = measure.marching_cubes(D, 0.0, spacing=(stap, stap, stap))
    v += lo
    me = bpy.data.meshes.new('Huid'); me.from_pydata([tuple(p) for p in v], [], [tuple(t[::-1]) for t in f]); me.update()
    ob = bpy.data.objects.new('Huid', me); bpy.context.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    return ob

def kleur_vlakken(huid, dl, kop_draai, kop_kantel):
    namen = ['lijf', 'vleugel', 'stip', 'staart', 'bliksem', 'creme', 'wang']
    for n in namen: huid.data.materials.append(mat(n))
    C = np.array([tuple(p.center) for p in huid.data.polygons], np.float32)
    Rinv = np.array(kop_matrix(kop_draai, kop_kantel).transposed(), np.float32)
    nek = np.array(NEK, np.float32)
    Ck = (C - nek) @ Rinv.T + nek
    afst = np.stack([sdf_deel(Ck if g == 'kop' else C, deel) for _, deel, _, g in dl], 1)
    welk = [dl[i][0] for i in afst.argmin(1)]
    idx = np.zeros(len(C), int)
    for j, w in enumerate(welk):
        p = C[j]; q = Ck[j]
        if w == 'lijf':
            # crème buik: groot ovaal aan de voorkant (Raichu-buik, borst opgezet)
            b = ((p[0] + 9.0) / 9.0) ** 2 + (p[1] / 9.5) ** 2 + ((p[2] + 5.0) / 12.5) ** 2
            idx[j] = 5 if b < 1 else 0
        elif w == 'vleugel':
            idx[j] = 1
            # ronde lichte stippen (familie Picapau): rooster van stippen op de dekveren
            # minder en grotere stippen, alleen op de dekveren (binnenste deel van de vleugel), zoals Picapau
            if p[2] > -1 and p[0] < 19:
                g = np.array([p[0] / 6.5, p[2] / 6.5 + 0.5 * (round(p[0] / 6.5) % 2)])
                if np.hypot(*(g - np.round(g))) < 0.30: idx[j] = 2
        elif w == 'staart': idx[j] = 3
        elif w == 'bliksem': idx[j] = 4
        elif w in ('kuif', 'kuif2'): idx[j] = 5
        elif w == 'kop':
            for s in (-1, 1):
                c = np.array([KC.x - 5.0, s * 6.0, KC.z - 3.6])
                r = q - c
                if (r[0] / 3.2) ** 2 + (r[1] / 3.2) ** 2 + (r[2] / 2.8) ** 2 < 1: idx[j] = 6
    for poly, i in zip(huid.data.polygons, idx): poly.material_index = int(i)

def bouw(kop_draai=25.0, kop_kantel=0.0, voorover=0.0, tong=False, snavel_hoek=6, snavel_lengte=15.0, oog_az=75):
    leeg()
    wortel = bpy.data.objects.new('wortel', None); bpy.context.collection.objects.link(wortel)
    dl = delen(kop_draai, kop_kantel)
    huid = huid_sdf(dl, kop_draai, kop_kantel)
    bpy.ops.object.shade_smooth()
    kleur_vlakken(huid, dl, kop_draai, kop_kantel)
    # romp (huid + kop) kantelt als geheel voorover rond de heup; de pootjes blijven staan
    romp = bpy.data.objects.new('romp', None); bpy.context.collection.objects.link(romp)
    romp.location = HEUP; romp.parent = wortel
    koppel(huid, romp)
    # kop-onderdelen: aan een leeg object op de nek, dat de kopdraai krijgt
    kopas = bpy.data.objects.new('kopas', None); bpy.context.collection.objects.link(kopas)
    kopas.location = NEK; koppel(kopas, romp)
    a = math.radians(snavel_hoek)
    d = Vector((-math.cos(a), 0, math.sin(a)))
    basis = KC + Vector((-6.8, 0, -1.6))
    # beitelsnavel: boven- en ondersnavel (bij de tong-variant iets open)
    if tong:
        wig('Snavel', basis + Vector((0, 0, 0.5)), d + Vector((0, 0, 0.06)), snavel_lengte, 2.9, 1.7, 'snavel', kopas)
        wig('Onder', basis + Vector((0.3, 0, -0.9)), d + Vector((0, 0, -0.18)), snavel_lengte * 0.86, 2.5, 1.2, 'snavel', kopas)
        # spechtentong: lang, half uit de snavel, hangt in een boog naar beneden met een bliksempuntje
        familie('Tong', [(basis + Vector((-snavel_lengte * 0.5 - t, 0, -0.8 - 0.11 * t * t)), (1.15 - 0.03 * t,) * 3)
                         for t in [i * 0.4 for i in range(24)]], 'tong', None, voxel=0.12, glad=6)
        koppel(bpy.data.objects['Tong'], kopas)
    else:
        wig('Snavel', basis, d, snavel_lengte, 3.2, 3.0, 'snavel', kopas)
    az = math.radians(oog_az); el = math.radians(16)
    for s in (-1,):      # alleen het nabije oog: het verre oog stak als bultje uit de omtrek (Gen 3: één oog bij een snavel)
        dd = Vector((-math.cos(az) * math.cos(el), s * math.sin(az) * math.cos(el), math.sin(el)))
        p = KC + Vector((dd.x * KR[0], dd.y * KR[1], dd.z * KR[2])) * 0.97
        o = bol('Oog', p, (2.1, 0.6, 2.5), 'oog', kopas)
        o.rotation_euler = Vector((0, 1, 0)).rotation_difference(Vector((dd.x, dd.y, 0)).normalized()).to_euler()
        bol('Glans', p + Vector((dd.x, dd.y, 0)).normalized() * 0.4 + Vector((-0.5, 0, 0.9)), (0.65, 0.3, 0.75), 'glans', kopas)
    bpy.context.view_layer.update()
    kopas.rotation_euler = kop_matrix(kop_draai, kop_kantel).to_euler()
    romp.rotation_euler = (0, math.radians(-voorover), 0)     # + = voorover (kop omlaag/naar voren)
    # pootjes: kort en stevig, tenen 2 voor 2 achter (specht)
    for s in (-1, 1):
        familie('Poot', [((-2.0, s * 4.6, -19.5), (1.5, 1.5, 3.0)),
                         ((-5.6, s * 4.6, -22.8), (2.8, 1.1, 0.9)),
                         ((0.8, s * 4.6, -23.0), (2.0, 1.1, 0.8))], 'poot', wortel)
    return wortel

def camera_licht(res=512, kantel=8):
    sc = bpy.context.scene
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = 64
    k = math.radians(kantel)
    cam.location = (0, -100 * math.cos(k), 100 * math.sin(k)); cam.rotation_euler = (math.radians(90) - k, 0, 0)
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'MATERIAL'
    sc.display.shading.show_object_outline = True; sc.display.shading.object_outline_color = (0.05, 0.03, 0.08)
    sc.display.shading.show_cavity = True; sc.display.shading.cavity_type = 'WORLD'
    sc.render.film_transparent = True
    sc.view_settings.view_transform = 'Standard'
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'

def render(pad, lijf=30, kantel=8, res=512, schaal=1.0, schuif=(0, 0), **kw):
    """lijf = draai van het lijf naar de kijker; kop_draai (kw) komt daar bovenop"""
    wortel = bouw(**kw)
    wortel.rotation_euler = (0, 0, math.radians(lijf))
    wortel.scale = (schaal, schaal, schaal); wortel.location = (schuif[0], 0, schuif[1])
    camera_licht(res, kantel)
    bpy.context.scene.render.filepath = pad
    bpy.ops.render.render(write_still=True)

if __name__ == '__main__':
    uit = sys.argv[1] if len(sys.argv) > 1 else 'rond_v1'
    hoeken = [int(a) for a in sys.argv[2:]] or [0, 30, 90, 180, 330]
    os.makedirs(uit, exist_ok=True)
    for h in hoeken:
        render(os.path.abspath(os.path.join(uit, f'rond_{h:03d}.png')), lijf=h, kop_draai=0)
