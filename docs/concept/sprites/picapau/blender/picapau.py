"""Picapau (Electric/Flying) als 3D-model in Blender (bpy). Opzet en hulpfuncties overgenomen van
docs/concept/sprites/kolibrie_pre/blender/kolibrie_pre.py (tak claude/fervent-keller-4cfbrk).
Eenheden = spritepixels: Blender (X, Z) = (x - 32, 32 - y) van de 64x64-sprite, Y = diepte; de vogel kijkt naar -X.
Bron: Jordi's foto's (referenties/, vooral foto 4: rechtop, vleugels dicht, snavel omhoog) + Pikipek-houding.
Jordi: "vleugels dicht, snavel wat meer omhoog, en maak het nog iets meer pikachu dan de echte vogel";
"de top van de kuif zwart ... zoals pikachu's oren".
Huid = één oppervlak (smooth union van afstandsvelden); kleurvlakken per vlak; snavel, ogen en pootjes los.
Draaien: python3.11 picapau.py [uitmap] [hoeken...]"""
import bpy, math, sys, os
from mathutils import Vector, Euler

KLEUR = dict(geel=(1.0, 0.84, 0.22), vleugel=(0.30, 0.17, 0.08), staart=(0.50, 0.20, 0.07), wang=(0.86, 0.12, 0.10),
             kuiftop=(0.06, 0.05, 0.05), snavel=(0.94, 0.86, 0.50), oog=(0.02, 0.01, 0.01), glans=(1, 1, 1),
             poot=(0.25, 0.25, 0.27), schub=(0.93, 0.80, 0.50))

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
    lo = np.array([-30.0, -16.0, -32.0]); hi = np.array([30.0, 16.0, 32.0])
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


# ---------------- Picapau ----------------
KC = Vector((-4.0, 0, 11.0))          # kopmidden
KR = (9.0, 8.4, 8.6)                  # kop: groot en rond (meer Pikachu)

def delen_picapau():
    d = [('lijf', ('ell', (2.0, 0, -5.0), (9.2, 8.4, 11.6), (0, -18, 0)), 0),
         ('kop', ('ell', tuple(KC), KR, (0, 0, 0)), 3.0)]
    # kuif = twee punten naar achter-boven, iets uit elkaar (Pikachu-oren); toppen zwart
    for kant in (-1, 1):
        d.append(('kuif', ('blad', (-1.0, kant * 2.4, 17.0), (5.5, kant * 4.2, 27.5), 3.2, 0.5, 0.55), 1.4))
    # rafelige achterkuif: kort, naar achteren
    for (a, b, ra) in [((1.0, 0, 16.0), (8.5, 0, 19.0), 3.0), ((2.5, 0, 13.0), (10.0, 0, 13.5), 3.0), ((2.5, 0, 9.5), (9.0, 0, 7.0), 2.6)]:
        d.append(('kuif2', ('blad', a, b, ra, 0.8, 1.6), 1.8))
    # vleugels dicht tegen het lijf (Pikachu-rugstrepen = geschubde dekveren)
    for kant in (-1, 1):
        d.append(('vleugel', ('blad', (-1.5, kant * 8.0, 2.5), (10.5, kant * 6.0, -17.0), 5.4, 1.6, 0.34), 0.8))
    # stijve steunstaart met een knik (bliksem-hint)
    d.append(('staart', ('blad', (8.0, 0, -15.0), (12.0, 0, -22.0), 2.6, 2.2, 1.7), 1.0))
    d.append(('staart', ('blad', (10.5, 0, -22.0), (13.5, 0, -29.0), 2.3, 0.6, 1.7), 0.6))
    return d

def bouw_picapau(kop_draai=0.0, snavel_hoek=32, snavel_lengte=8.0):
    leeg()
    wortel = bpy.data.objects.new('wortel', None); bpy.context.collection.objects.link(wortel)
    delen = delen_picapau()
    huid = huid_sdf(delen)
    bpy.ops.object.shade_smooth()
    namen = ['geel', 'vleugel', 'staart', 'wang', 'kuiftop', 'schub']
    for n in namen: huid.data.materials.append(mat(n))
    C = np.array([tuple(p.center) for p in huid.data.polygons])
    afst = np.stack([sdf_deel(C, deel) for _, deel, _ in delen], 1)
    welk = [delen[i][0] for i in afst.argmin(1)]
    az = math.radians(50); el = math.radians(14)
    for poly, w in zip(huid.data.polygons, welk):
        p = poly.center; idx = 0
        if w == 'vleugel':
            idx = 1
            # schubben: lichte randjes op de dekveren (bovenste helft van de vleugel)
            if p.z > -7 and (math.sin(p.x * 1.1 + p.z * 0.4) + math.sin(p.z * 1.4)) > 1.2: idx = 5
        elif w == 'staart': idx = 2
        elif w == 'kuif' and p.z > 24.0: idx = 4
        elif w == 'kop':
            q = p - KC
            # wangvlek: rond, onder en achter het oog, naar de snavelhoek
            for kant in (-1, 1):
                c = Vector((-5.2, kant * 6.2, -3.4))
                if ((q - c).x / 3.0) ** 2 + ((q - c).y / 3.0) ** 2 + ((q - c).z / 2.6) ** 2 < 1: idx = 3
        poly.material_index = idx
    huid.parent = wortel
    # snavel: beitel, schuin omhoog
    basis = KC + Vector((-7.6, 0, -1.2))
    wig('Snavel', basis, snavel_hoek, snavel_lengte, 2.6, 2.2, 'snavel', wortel)
    # ogen: groot en donker met glans (Pikachu), aan beide kanten
    for kant in (-1, 1):
        dd = Vector((-math.cos(az) * math.cos(el), kant * math.sin(az) * math.cos(el), math.sin(el)))
        p = KC + Vector((dd.x * KR[0], dd.y * KR[1], dd.z * KR[2])) * 0.97
        o = bol('Oog', p, (2.0, 0.6, 2.4), 'oog', wortel)
        o.rotation_euler = Vector((0, 1, 0)).rotation_difference(Vector((dd.x, dd.y, 0)).normalized()).to_euler()
        bol('Glans', p + Vector((dd.x, dd.y, 0)).normalized() * 0.4 + Vector((-0.4, 0, 0.8)), (0.6, 0.3, 0.7), 'glans', wortel)
    # pootjes: kort, donkergrijs, onder de voorkant van het lijf; tenen 2 voor 2 achter
    for kant in (-1, 1):
        familie('Poot', [((-2.5, kant * 3.0, -17.5), (1.1, 1.1, 2.2)),
                         ((-4.6, kant * 3.0, -19.6), (2.4, 0.9, 0.7)),
                         ((-0.6, kant * 3.0, -19.8), (1.6, 0.9, 0.6))], 'poot', wortel, voxel=0.15, glad=2)
    return wortel

def render(pad, lijf=0, kantel=8, res=512, **kw):
    wortel = bouw_picapau(**kw)
    wortel.rotation_euler = (0, 0, math.radians(lijf))
    camera_licht(res, kantel)
    bpy.context.scene.render.filepath = pad
    bpy.ops.render.render(write_still=True)

if __name__ == '__main__':
    uit = sys.argv[1] if len(sys.argv) > 1 else '.'
    hoeken = [int(a) for a in sys.argv[2:]] or [0, 45, 90, 135, 180, 225, 270, 315]
    os.makedirs(uit, exist_ok=True)
    for h in hoeken:
        render(os.path.join(uit, f'rond_{h:03d}.png'), lijf=h)
