"""Kolibrie pre-evo als echt 3D-model in Blender (bpy), van alle kanten kloppend (Jordi: "als je dit model helemaal
zou draaien zou het er heel raar uitzien"). Eenheden = spritepixels: Blender (X, Z) = (x - 32, 32 - y) van de 64x64-sprite,
Y = diepte (camera kijkt vanaf -Y). De vogel kijkt naar -X. Maten uit het goedgekeurde K1-R2b (kop ~8 px straal, mond open).
Delen: lijf en kop als aparte metaball-families (eigen bol, naad bij de nek), buik/kap/vleugel als gekleurde lagen,
snavel als twee wiggen, ogen aan beide kanten, staart groeit uit het achterlijf, pootjes.
Draaien: python3.11 kolibrie_pre.py [uitmap] [hoeken...]"""
import bpy, math, sys, os
from mathutils import Vector, Euler

KLEUR = dict(lila=(0.50, 0.42, 0.85), kap=(0.24, 0.20, 0.62), buik=(0.95, 0.93, 1.0), vleugel=(0.26, 0.22, 0.64),
             boven=(0.22, 0.20, 0.30), onder=(0.88, 0.40, 0.05), gaap=(0.96, 0.66, 0.06), oog=(0.01, 0.01, 0.02),
             glans=(1, 1, 1), poot=(0.06, 0.05, 0.09), mond=(0.80, 0.20, 0.30))

def mat(naam):
    m = bpy.data.materials.get(naam) or bpy.data.materials.new(naam)
    c = KLEUR[naam]; m.diffuse_color = (*c, 1); m.roughness = 0.6
    return m

def leeg():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def familie(naam, elementen, kleur, ouder=None, voxel=0.22, glad=6):
    """vorm uit ellipsoiden met exacte stralen (spritepx), samengevoegd tot een gladde huid (remesh + smooth).
    elementen = [(midden, (rx, ry, rz), stijfheid-genegeerd)] of met rotatie als 4e element"""
    obs = []
    for el in elementen:
        co, r = el[0], el[1]
        rot = el[3] if len(el) > 3 else (0, 0, 0)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=20, location=co)
        ob = bpy.context.object; ob.scale = r if isinstance(r, tuple) else (r, r, r); ob.rotation_euler = [math.radians(v) for v in rot]
        obs.append(ob)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in obs: ob.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if len(obs) > 1: bpy.ops.object.join()
    ob = bpy.context.object; ob.name = naam
    m = ob.modifiers.new('remesh', 'REMESH'); m.mode = 'VOXEL'; m.voxel_size = voxel
    if glad:
        sm = ob.modifiers.new('glad', 'SMOOTH'); sm.factor = 1.0; sm.iterations = glad
    bpy.ops.object.shade_smooth()
    ob.data.materials.append(mat(kleur))
    if ouder:
        bpy.context.view_layer.update(); wereld = ob.matrix_world.copy(); ob.parent = ouder; ob.matrix_world = wereld
    return ob

def bol(naam, co, schaal, kleur, ouder=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=co)
    ob = bpy.context.object; ob.name = naam; ob.scale = schaal; ob.rotation_euler = rot
    bpy.ops.object.shade_smooth(); ob.data.materials.append(mat(kleur))
    if ouder:
        bpy.context.view_layer.update(); w = ob.matrix_world.copy(); ob.parent = ouder; ob.matrix_world = w
    return ob

def wig(naam, basis, richting, lengte, breed, hoog, kleur, ouder):
    """snavelhelft: kegel met platte doorsnede, punt in 'richting' (graden omhoog t.o.v. -X)"""
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=1.0, radius2=0.05, depth=lengte, location=(0, 0, 0))
    ob = bpy.context.object; ob.name = naam
    ob.scale = (hoog, breed, 1)                       # kegel langs lokale Z; plat in hoogte
    # lokale Z naar -X draaien en 'richting' omhoog kantelen
    a = math.radians(richting)
    d = Vector((-math.cos(a), 0, math.sin(a)))
    ob.rotation_euler = Vector((0, 0, 1)).rotation_difference(d).to_euler()
    ob.location = Vector(basis) + d * (lengte / 2)
    bpy.ops.object.shade_smooth(); ob.data.materials.append(mat(kleur))
    bpy.context.view_layer.update(); w = ob.matrix_world.copy(); ob.parent = ouder; ob.matrix_world = w
    return ob

def bouw(kop_draai=0.0, snavel_open=40, snavel_lengte=5.0):
    leeg()
    wortel = bpy.data.objects.new('wortel', None); bpy.context.collection.objects.link(wortel)
    # ---- lijf (maten uit K1-R2b: borst ~10 px breed/hoog, totale hoogte lijf ~24 px), licht voorover ----
    familie('Lijf', [((-4.0, 0, -1.6), (10.0, 8.0, 10.4)),         # bolle borst
                     ((3.0, 0, 0.0), (8.6, 7.2, 9.4), 0, (0, -28, 0)),   # rug/romp, schuin
                     ((7.4, 0, -6.6), (5.4, 5.2, 4.6)),          # achterlijf
                     ((-6.8, 0, 7.2), (6.4, 6.0, 5.4))],         # nek, in de kop
            'lila', wortel)
    familie('Buik', [((-7.2, 0, -2.4), (8.0, 6.8, 8.8)), ((-2.0, 0, -8.2), (7.0, 5.8, 3.8))], 'buik', wortel)
    for kant in (-1, 1):
        familie('Vleugel', [((4.6, kant * 5.4, -0.6), (9.0, 2.2, 5.2), 0, (0, -36, 0))], 'vleugel', wortel)
    familie('Staart', [((10.8, 0, -9.2), (5.6, 2.8, 2.0), 0, (0, -38, 0))], 'vleugel', wortel)
    for kant in (-1, 1):
        familie('Poot', [((-1.5, kant * 2.6, -11.2), (0.9, 0.9, 1.8)), ((-2.6, kant * 2.6, -12.6), (1.8, 0.8, 0.6))], 'poot', wortel, voxel=0.15, glad=2)
    # ---- kop: eigen bol, eigen draaipunt bij de nek ----
    nek = bpy.data.objects.new('nek', None); bpy.context.collection.objects.link(nek); nek.parent = wortel
    nek.location = (-6.5, 0, 6.5)
    kc = Vector((-9.2, 0, 14.6))
    familie('Kop', [(kc, (8.2, 7.9, 7.6))], 'lila', nek)
    familie('Kap', [(kc + Vector((3.8, 0, 3.4)), (6.0, 7.0, 5.2))], 'kap', nek)
    familie('Keel', [(kc + Vector((-2.6, 0, -4.2)), (4.4, 5.4, 3.6))], 'buik', nek)
    basis = kc + Vector((-6.9, 0, -0.8))
    wig('Bovensnavel', basis + Vector((0, 0, 0.4)), snavel_open / 2 + 6, snavel_lengte, 2.3, 0.85, 'boven', nek)
    wig('Ondersnavel', basis + Vector((0, 0, -0.4)), -snavel_open / 2 + 6, snavel_lengte * 0.85, 2.6, 1.2, 'onder', nek)
    bol('Mond', basis + Vector((0.6, 0, 0)), (1.0, 1.6, 0.9), 'mond', nek)
    for kant in (-1, 1):
        bol('Gaap', basis + Vector((0.7, kant * 2.0, 0.0)), (0.8, 0.6, 0.8), 'gaap', nek)
    for kant in (-1, 1):
        az = math.radians(52); el = math.radians(12)
        d = Vector((-math.cos(az) * math.cos(el), kant * math.sin(az) * math.cos(el), math.sin(el)))
        p = kc + Vector((d.x * 8.2, d.y * 7.9, d.z * 7.6)) * 0.97
        o = bol('Oog', p, (1.7, 0.5, 2.5), 'oog', nek)
        o.rotation_euler = Vector((0, 1, 0)).rotation_difference(Vector((d.x, d.y, 0)).normalized()).to_euler()
        bol('Glans', p + Vector((d.x, d.y, 0)).normalized() * 0.3 + Vector((-0.3, 0, 0.6)), (0.5, 0.3, 0.6), 'glans', nek)
    nek.rotation_euler = (0, 0, math.radians(kop_draai))
    return wortel, nek

import numpy as np

def sdf_deel(P, deel):
    """afstand tot één deel. P = (..., 3). deel = ('ell', midden, stralen, rot) of ('blad', A, B, ra, rb, plat)"""
    if deel[0] == 'ell':
        _, co, r, rot = deel
        p = P - np.array(co)
        ay = math.radians(rot[1]); az = math.radians(rot[2])
        px, py, pz = p[..., 0], p[..., 1], p[..., 2]
        cz, sz = math.cos(-az), math.sin(-az); px, py = px * cz - py * sz, px * sz + py * cz
        cy, sy = math.cos(-ay), math.sin(-ay); px, pz = px * cy + pz * sy, -px * sy + pz * cy
        q = np.sqrt((px / r[0]) ** 2 + (py / r[1]) ** 2 + (pz / r[2]) ** 2)
        return (q - 1) * min(r)
    _, A, B, ra, rb, plat = deel                      # taps blad (vleugel): capsule die dunner wordt, plat in y
    A, B = np.array(A, float), np.array(B, float); ab = B - A; L2 = ab @ ab
    t = np.clip(((P - A) @ ab) / L2, 0, 1)
    q = P - (A + t[..., None] * ab)
    q = q * np.array([1, 1 / plat, 1])
    return np.linalg.norm(q, axis=-1) - (ra + (rb - ra) * t)

def smin(a, b, k):
    if k <= 0: return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)

def huid_sdf(delen, stap=0.22):
    """Huid als één oppervlak: smooth union van alle delen (k per deel = hoe ver het in de rest vloeit), marching cubes."""
    from skimage import measure
    lo = np.array([-24.0, -15.0, -18.0]); hi = np.array([24.0, 15.0, 28.0])
    xs, ys, zs = [np.arange(lo[i], hi[i], stap) for i in range(3)]
    P = np.stack(np.meshgrid(xs, ys, zs, indexing='ij'), -1)
    d = None
    for naam, deel, k in delen:
        di = sdf_deel(P, deel)
        d = di if d is None else smin(d, di, k)
    v, f, _, _ = measure.marching_cubes(d, 0.0, spacing=(stap, stap, stap))
    v += lo
    me = bpy.data.meshes.new('Huid'); me.from_pydata([tuple(p) for p in v], [], [tuple(t[::-1]) for t in f]); me.update()
    ob = bpy.data.objects.new('Huid', me); bpy.context.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    return ob

def bouw_geheel(kop_draai=0.0, snavel_open=8, snavel_lengte=9.0, snavel_hoek=12, kh=11.8, vleugel_k=1.2):
    """Eén doorlopende huid (Jordi: "maak het echt een geheel en niet een soort verzameling aan bollen"):
    lijf, borst, nek, kop, staart en vleugelbolling als vormen samengevoegd (voxel-remesh) en daarna glad gestreken,
    zodat de overgangen vloeien. Buik, kap, keel en vleugel zijn kleurvlakken op die huid, geen losse delen.
    Alleen snavel, ogen en pootjes zijn aparte delen (zoals bij een echte vogel)."""
    leeg()
    wortel = bpy.data.objects.new('wortel', None); bpy.context.collection.objects.link(wortel)
    piv = Vector((-6.5, 0, 6.5)); R = Euler((0, 0, math.radians(kop_draai))).to_matrix()
    kop = lambda v: piv + R @ (Vector(v) - piv)               # kopcoördinaat -> lijf (kop draait rond de nek)
    kc0 = Vector((-9.4, 0, kh)); kc = kop(kc0)
    # lijf = één bolletje (Jordi: "het lichaam moet ook meer een bolletje zijn, waarvan de vleugels deel uit maken")
    delen = [('lijf', ('ell', (-0.5, 0, -2.0), (11.2, 9.0, 10.6), (0, -10, 0)), 0),
             ('staart', ('ell', (10.6, 0, -9.6), (4.6, 2.4, 1.6), (0, -38, 0)), 1.6),       # kort, onder de vleugelpunten
             ('kop', ('ell', tuple(kc), (8.2, 7.9, 7.6), (0, 0, kop_draai)), 4.0)]          # kop zonder nek op het bolletje
    for kant in (-1, 1):            # vleugels plat in de ronding van het bolletje, punten steken achter/onder uit (foto 6/7)
        delen.append(('vleugel', ('blad', (-1.0, kant * 7.1, 3.2), (6.8, kant * 5.9, -4.2), 4.2, 3.4, 0.24), vleugel_k))
        delen.append(('vleugel', ('blad', (6.8, kant * 5.9, -4.2), (14.0, kant * 2.4, -10.6), 3.4, 0.7, 0.24), vleugel_k))
    huid = huid_sdf(delen)
    bpy.ops.object.shade_smooth()
    # kleurvlakken per vlak, regels in lijf- en kopcoördinaten
    namen = ['lila', 'buik', 'kap', 'vleugel']
    for n in namen: huid.data.materials.append(mat(n))
    Rinv = R.transposed()
    def ell(p, c, r, rot=0):
        d = p - Vector(c); a = math.radians(rot)
        x = d.x * math.cos(a) - d.z * math.sin(a); z = d.x * math.sin(a) + d.z * math.cos(a)
        return (x / r[0]) ** 2 + (d.y / r[1]) ** 2 + (z / r[2]) ** 2
    C = np.array([tuple(p.center) for p in huid.data.polygons])
    afst = np.stack([sdf_deel(C, deel) for _, deel, _ in delen], 1)
    welk = [delen[i][0] for i in afst.argmin(1)]
    for poly, w in zip(huid.data.polygons, welk):
        p = poly.center
        idx = 0
        if w == 'kop':
            k = piv + Rinv @ (p - piv)
            d = Vector(((k - kc0).x / 8.2, (k - kc0).y / 7.9, (k - kc0).z / 7.6)).normalized()
            if d.z * 0.8 + d.x * 0.6 - 0.35 * d.x * d.x > 0.22: idx = 2       # kap boven/achter, gebogen grens
            elif d.z < -0.3 and d.x < -0.15: idx = 1                           # witte keel onder de snavel (foto 7)
        elif w in ('vleugel', 'staart'):
            idx = 3
        elif ell(p, (-10.0, 0, -1.0), (10.4, 7.6, 12.4)) < 1:
            idx = 1                                                          # buik tot de keel
        poly.material_index = idx
    huid.parent = wortel
    for kant in (-1, 1):
        familie('Poot', [((-1.5, kant * 2.6, -11.2), (0.9, 0.9, 1.8)), ((-2.6, kant * 2.6, -12.6), (1.8, 0.8, 0.6))], 'poot', wortel, voxel=0.15, glad=2)
    nek = bpy.data.objects.new('nek', None); bpy.context.collection.objects.link(nek); nek.parent = wortel
    nek.location = piv
    basis = kc0 + Vector((-6.9, 0, -0.8))
    nek.location = piv
    # naaldsnavel zoals op foto 6/7 (Jordi: "iets meer langere snavel toch zoals op mijn fotos"), licht open, schuin omhoog
    wig('Bovensnavel', basis + Vector((0.4, 0, 0.25)), snavel_hoek + snavel_open / 2, snavel_lengte, 1.7, 1.0, 'boven', nek)
    wig('Ondersnavel', basis + Vector((0.4, 0, -0.25)), snavel_hoek - snavel_open / 2, snavel_lengte * 0.9, 1.5, 0.8, 'boven', nek)
    bol('Mond', basis + Vector((0.6, 0, 0)), (1.0, 1.6, 0.9), 'mond', nek)
    for kant in (-1, 1):
        bol('Gaap', basis + Vector((0.7, kant * 2.0, 0.0)), (0.8, 0.6, 0.8), 'gaap', nek)
        az = math.radians(52); el = math.radians(12)
        d = Vector((-math.cos(az) * math.cos(el), kant * math.sin(az) * math.cos(el), math.sin(el)))
        p = kc0 + Vector((d.x * 8.2, d.y * 7.9, d.z * 7.6)) * 0.97
        o = bol('Oog', p, (1.7, 0.5, 2.5), 'oog', nek)
        o.rotation_euler = Vector((0, 1, 0)).rotation_difference(Vector((d.x, d.y, 0)).normalized()).to_euler()
        bol('Glans', p + Vector((d.x, d.y, 0)).normalized() * 0.3 + Vector((-0.3, 0, 0.6)), (0.5, 0.3, 0.6), 'glans', nek)
    nek.rotation_euler = (0, 0, math.radians(kop_draai))
    return wortel, nek

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

def render(pad, lijf=0, kop=0, kantel=8, res=512, **kw):
    wortel, nek = bouw_geheel(kop_draai=kop, **kw)
    wortel.rotation_euler = (0, 0, math.radians(lijf))
    camera_licht(res, kantel)
    bpy.context.scene.render.filepath = pad
    bpy.ops.render.render(write_still=True)

if __name__ == '__main__':
    uit = sys.argv[1] if len(sys.argv) > 1 else '.'
    hoeken = [int(a) for a in sys.argv[2:]] or [0, 45, 90, 135, 180, 225, 270, 315]
    os.makedirs(uit, exist_ok=True)
    for h in hoeken:
        render(os.path.join(uit, f'rond_{h:03d}.png'), lijf=h, kop=0)
