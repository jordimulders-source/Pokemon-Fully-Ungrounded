"""MODELRONDE 2 (5 nov) van de Picapau-evolutie; ronde 1 = ../picapau_evo.py (blijft zoals het was).
Reparaties (coördinator, op basis van stand C): 1 kuif = brede platte veerkuiven (kastanje basis, crème top, alleen
het bovenste derde krult); 2 imposanter: borst hoger/voller, kop groter, lijf minder ei-op-pootjes, vleugels groter en
breder gespreid met 4 brede handpennen en minder, grotere stippen; 3 staart = platte veerpluim die breder wordt, echte S,
grotere bliksem; 4 langere beitelsnavel zonder donkere onderkant; 5 kleuren als lineaire waarden van de echte sRGB-kleur.
Evolutie van Picapau (Electric/Flying, eindvorm) als 3D-model in Blender (bpy).
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

def lin(r, g, b):
    """sRGB 0-255 -> lineair (diffuse_color is lineair)"""
    f = lambda c: (c / 255) / 12.92 if c / 255 <= 0.04045 else (((c / 255) + 0.055) / 1.055) ** 2.4
    return (f(r), f(g), f(b))

KLEUR = dict(lijf=lin(206, 104, 38),      # warm oranje-kastanje (Celeus elegans)
             kuifmid=lin(232, 170, 96),   # overgang kastanje -> crème in de kuif
             vleugel=lin(140, 58, 24),    # donkerder kastanje
             stip=lin(246, 226, 172),     # ronde lichte stippen (familie Picapau)
             staart=lin(164, 68, 28),     # pluim: roodbruin
             bliksem=lin(252, 212, 48),   # bliksem: geel (Electric)
             creme=lin(250, 236, 196),    # kuiftop en buik
             wang=lin(222, 40, 36), snavel=lin(240, 226, 170), oog=lin(8, 6, 6), glans=(1, 1, 1),
             poot=lin(96, 92, 96), tong=lin(240, 140, 150))

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
HEUP = Vector((-1.5, 0, -17.5))       # draaipunt van de romp (voorover)
KC = Vector((-9.5, 0, 13.5))           # kopmidden (kop-lokaal)
KR = (11.0, 10.6, 10.7)                # grotere ronde kop (Pokémon-verhouding)

def kop_matrix(kop_draai, kop_kantel=0.0):
    """kop-lokaal -> lijf: draai om Z (naar de kijker) en een kleine kanteling, rond NEK"""
    R = Matrix.Rotation(math.radians(kop_draai), 3, 'Z') @ Matrix.Rotation(math.radians(kop_kantel), 3, 'Y')
    return R

def vleugel(s):
    """groot en breed gespreid, hoog opgetrokken (Ho-Oh/Braviary/Talonflame): arm omhoog naar buiten,
    brede handplaat met vier brede handpennen met ronde punten, brede armpennen naar achter-onder"""
    schouder = (5.0, s * 9.5, 4.0); pols = (8.0, s * 19.5, 21.0)
    arm = np.array(pols) - np.array(schouder)
    n = np.cross(arm, np.array([1.0, 0, -0.2])); n = tuple(n / np.linalg.norm(n))
    d = [('vleugel', ('buis', [(schouder, 5.0), (pols, 4.2)], n, 0.42), 1.2),
         ('vleugel', ('buis', [((7.0, s * 13.0, 11.0), 6.5), ((16.0, s * 18.0, 2.0), 5.5), ((21.0, s * 19.0, -3.0), 3.4)], n, 0.36), 1.2),
         ('vleugel', ('buis', [(pols, 5.4), ((19.0, s * 23.0, 17.0), 6.0)], n, 0.36), 1.2)]
    for tip in [(15.0, 24.0, 34.0), (23.0, 26.0, 29.0), (28.5, 26.0, 20.0), (29.0, 23.5, 9.0)]:
        tip = (tip[0], s * tip[1], tip[2])
        mid = tuple(np.array(pols) + 0.6 * (np.array(tip) - np.array(pols)))
        d.append(('vleugel', ('buis', [(pols, 4.6), (mid, 4.0), (tip, 2.3)], n, 0.36), 1.6))
    return d

def staart_keten():
    """platte veerpluim, breder naar de punt: uit de stuit omhoog naar rechts, over een boog omlaag langs de
    rechterkant, onder het lijf door naar voren (S), dan de bliksem linksonder"""
    return [((12.0, 1.0, -10.0), 3.0), ((19.0, 2.0, -5.0), 3.4), ((25.5, 2.5, -4.0), 3.8), ((29.5, 3.0, -10.0), 4.2),
            ((28.0, 3.5, -19.5), 4.5), ((19.0, 4.0, -26.5), 4.7), ((7.0, 4.5, -28.5), 4.6), ((-3.5, 4.5, -26.5), 4.2),
            ((-10.0, 4.0, -22.0), 3.6)]

BLIKSEM = [((-10.0, 4.0, -22.0), 3.4), ((-20.5, 4.0, -18.5), 3.6), ((-14.5, 4.0, -12.5), 3.4), ((-26.0, 4.0, -2.5), 1.6)]

def delen(kop_draai=25.0, kop_kantel=0.0):
    """lijst (naam, deel, k, groep); groep 'kop' wordt met de kopdraai rond NEK geëvalueerd"""
    d = [('lijf', ('ell', (3.0, 0, -6.5), (14.5, 14.0, 13.0), -15), 0, 'lijf'),
         ('lijf', ('ell', (-6.0, 0, 1.0), (11.0, 12.0, 12.0), -10), 3.5, 'lijf'),     # opgezette borst: hoog en vol naar voren
         ('lijf', ('ell', (-4.0, 0, 7.0), (8.0, 9.0, 7.5), 0), 3.0, 'lijf')]          # dikke nek
    # dijen in de huid: de poten groeien uit het lijf
    for s in (-1, 1):
        d.append(('lijf', ('ell', (-1.5, s * 4.8, -17.5), (3.6, 3.3, 3.0), 0), 1.5, 'lijf'))
    for naam, deel, k in vleugel(-1) + vleugel(1):
        d.append((naam, deel, k, 'lijf'))
    d.append(('staart', ('buis', staart_keten(), (0, 1, 0), 0.34), 1.2, 'lijf'))
    d.append(('bliksem', ('buis', BLIKSEM, (0, 1, 0), 0.32), 0.5, 'lijf'))
    # kop-groep (kop-lokale coördinaten)
    d.append(('kop', ('ell', tuple(KC), KR, 0), 3.5, 'kop'))
    # grote kuif: twee lange punten omhoog-achter, top krult naar buiten (Raichu-oren), plat van voor gezien
    for s in (-1, 1):
        # brede platte lob (Raichu-oor): brede basis, recht omhoog-achter; alleen het bovenste derde krult naar buiten
        keten = [((-8.0, s * 4.0, 20.5), 6.0), ((-6.5, s * 5.0, 26.0), 6.0), ((-5.0, s * 6.0, 31.0), 5.0),
                 ((-3.5, s * 7.5, 35.0), 3.6), ((-2.5, s * 10.5, 37.5), 2.8), ((-2.0, s * 13.5, 37.0), 2.2),
                 ((-2.0, s * 15.0, 34.5), 1.6)]
        d.append(('kuif', ('buis', keten, (1, 0, 0.25), 0.2), 1.8, 'kop'))
    # korte rafelige achterkuif (familie Picapau)
    for a, b, ra in [((-2.0, 0, 18.0), (5.5, 0, 21.5), 3.0), ((-0.5, 0, 14.0), (6.5, 0, 15.0), 2.8)]:
        d.append(('kuif2', ('buis', [(a, ra), (b, 0.9)], (0, 1, 0), 1.6), 1.8, 'kop'))
    return d

def huid_sdf(dl, kop_draai, kop_kantel, stap=0.3):
    from skimage import measure
    lo = np.array([-38.0, -32.0, -36.0], np.float32); hi = np.array([38.0, 32.0, 44.0], np.float32)
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
    namen = ['lijf', 'vleugel', 'stip', 'staart', 'bliksem', 'creme', 'wang', 'kuifmid']
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
            b = ((p[0] + 11.0) / 9.5) ** 2 + (p[1] / 10.5) ** 2 + ((p[2] + 3.0) / 14.0) ** 2
            idx[j] = 5 if b < 1 else 0
        elif w == 'vleugel':
            idx[j] = 1
            # ronde lichte stippen (familie Picapau): rooster van stippen op de dekveren
            # minder en grotere stippen, alleen op de dekveren (binnenste deel van de vleugel), zoals Picapau
            # weinig, grote stippen (op 1x >= 2x2 px) op de dekveren
            if p[2] > 4 and p[0] < 20:
                g = np.array([p[0] / 8.5, p[2] / 8.5 + 0.5 * (round(p[0] / 8.5) % 2)])
                if np.hypot(*(g - np.round(g))) < 0.30: idx[j] = 2
        elif w == 'staart': idx[j] = 3
        elif w == 'bliksem': idx[j] = 4
        elif w == 'kuif': idx[j] = 0 if q[2] < 25.5 else (7 if q[2] < 29.5 else 5)   # kastanje basis -> crème top
        elif w == 'kuif2': idx[j] = 0
        elif w == 'kop':
            for s in (-1, 1):
                c = np.array([KC.x - 5.5, s * 7.0, KC.z - 4.2])
                r = q - c
                if (r[0] / 3.6) ** 2 + (r[1] / 3.6) ** 2 + (r[2] / 3.1) ** 2 < 1: idx[j] = 6
    for poly, i in zip(huid.data.polygons, idx): poly.material_index = int(i)

def bouw(kop_draai=25.0, kop_kantel=0.0, voorover=0.0, tong=False, snavel_hoek=8, snavel_lengte=19.0, oog_az=75):
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
    basis = KC + Vector((-7.5, 0, -1.8))
    # beitelsnavel: boven- en ondersnavel (bij de tong-variant iets open)
    if tong:
        wig('Snavel', basis + Vector((0, 0, 0.5)), d + Vector((0, 0, 0.06)), snavel_lengte, 2.9, 1.7, 'snavel', kopas)
        wig('Onder', basis + Vector((0.3, 0, -0.9)), d + Vector((0, 0, -0.18)), snavel_lengte * 0.86, 2.5, 1.2, 'snavel', kopas)
        # spechtentong: lang, half uit de snavel, hangt in een boog naar beneden met een bliksempuntje
        familie('Tong', [(basis + Vector((-snavel_lengte * 0.5 - t, 0, -0.8 - 0.11 * t * t)), (1.15 - 0.03 * t,) * 3)
                         for t in [i * 0.4 for i in range(24)]], 'tong', None, voxel=0.12, glad=6)
        koppel(bpy.data.objects['Tong'], kopas)
    else:
        wig('Snavel', basis, d, snavel_lengte, 3.6, 3.3, 'snavel', kopas)
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
        familie('Poot', [((-2.0, s * 4.8, -20.5), (1.7, 1.7, 2.2)),
                         ((-5.8, s * 4.8, -22.6), (3.0, 1.2, 1.0)),
                         ((0.8, s * 4.8, -22.8), (2.2, 1.2, 0.9))], 'poot', wortel)
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
