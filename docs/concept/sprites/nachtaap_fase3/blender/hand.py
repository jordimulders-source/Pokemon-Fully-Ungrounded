"""Nachtaap fase 3: echte 3D-hand in Blender (bpy). Skelet met kootjes (FK) -> Skin-modifier -> voxel-remesh -> glad.
Gebruik: python3 hand.py  (pip install bpy). Schrijft hand.blend + renders in deze map.
Assen (hand-lokaal): pols in de oorsprong, vingers langs +Y, palm kijkt naar -Z (naar de camera), duimkant = -X.
Maten in 'cm' van een apenhand: muriqui-vingers lang, duim klein (echte muriqui heeft bijna geen duim, maar
Jordi's referenties (Drowzee Gen 1, anime-healerhand) hebben er een: die volgen we)."""
import bpy, math, os, sys
from mathutils import Vector, Matrix

HIER = os.path.dirname(os.path.abspath(__file__))

# vinger: (naam, knokkelpositie op de palm (x,y), lengtes 3 kootjes, dikte)
VINGERS = [
    ('wijs',  (-2.6, 8.1), (2.8, 1.9, 1.5), 0.92),
    ('mid',   (-0.85, 8.5), (3.1, 2.1, 1.6), 0.95),
    ('ring',  ( 0.9, 8.2), (2.9, 2.0, 1.5), 0.90),
    ('pink',  ( 2.6, 7.4), (2.3, 1.6, 1.3), 0.80),
]

POSES = {
    # spreid = waaierhoek per vinger (graden, rond de palmnormaal), krom = buiging per kootje (graden, naar de palm)
    'healer_drowzee': dict(spreid=(-7, -2, 3, 9), krom=[(5, 10, 8)] * 4, lengte=0.8, dikte=1.25, taps=(1.0, 0.84, 0.64), duim_abd=40, duim_krom=(15, 15), pols=0),
    'healer_anime':   dict(spreid=(-8, -2, 4, 10), krom=[(-3, 6, 6)] * 4, duim_abd=45, duim_krom=(5, 10), pols=0),
    'voet_ontspannen': dict(spreid=(0, 0, 0, 0), krom=[(18, 22, 15)] * 4, duim_abd=20, duim_krom=(10, 10), pols=0,
                            xs=0.62, ys=1.35, dikte=1.3, lengte=0.75, palm=(2.6, 5.6, 1.35)),   # hangt lang en slap (foto 2 onder)
    'voet_greep':     dict(spreid=(0, 0, 0, 0), krom=[(70, 80, 50)] * 4, duim_abd=25, duim_krom=(40, 40), pols=0,
                            xs=0.62, ys=1.35, dikte=1.3, lengte=0.8, palm=(2.6, 5.6, 1.35)),     # haakt om de tak (foto 2 links, foto 5)
    'vuist':          dict(spreid=(-2, 0, 2, 5), krom=[(80, 95, 60)] * 4, duim_abd=20, duim_krom=(40, 50), pols=0),
}

TOPPEN = []   # indices van de vingertoppen (laatste skeletpunt), gevuld door skelet()

def rot_z(a):  # waaier in het palmvlak
    return Matrix.Rotation(math.radians(a), 3, 'Z')
def rot_x(a):  # buigen naar de palm (palm = -Z): positieve hoek draait +Y naar -Z
    return Matrix.Rotation(math.radians(-a), 3, 'X')

def skelet(pose, stomp=True):
    """Geeft (verts, edges, radii) voor de Skin-modifier."""
    V, E, R = [], [], []
    TOPPEN.clear()
    def add(p, r, parent=None):
        V.append(Vector(p)); R.append(r)
        i = len(V) - 1
        if parent is not None: E.append((parent, i))
        return i
    pols = add((0, 0, 0), 1.5)
    hiel = add((0, 2.0, 0.15), 1.0, pols)
    for k, (naam, (kx, ky), lens, dik) in enumerate(VINGERS):
        kx, ky = kx * pose.get('xs', 1.0), ky * pose.get('ys', 1.0)   # voet: tenen dichter op elkaar, langere zool
        mc = add((kx * 0.55, 3.0 * pose.get('ys', 1.0), 0.15), 0.9, hiel)          # middenhandsbeentje
        knok = add((kx, ky, 0.15), dik * pose.get('dikte', 1.0), mc)
        M = rot_z(-pose['spreid'][k])
        p = Vector((kx, ky, 0.15)); last = knok
        Lm, Dm = pose.get('lengte', 1.0), pose.get('dikte', 1.0)
        hoek = 0
        for j, L in enumerate(lens):
            hoek += pose['krom'][k][j]
            d = M @ rot_x(hoek) @ Vector((0, 1, 0))
            p = p + d * L * Lm
            r = dik * Dm * pose.get('taps', (0.92, 0.85, 0.75))[j]
            last = add(p, r, last)
        TOPPEN.append(last)
    # duim: vanaf de palmhiel aan de -X-kant, schuin naar buiten, iets naar de camera
    basis = Vector((-2.1 * pose.get('xs', 1.0), 3.0, -0.3))
    b = add(basis, 1.35, hiel)
    a = pose['duim_abd']
    M = rot_z(a) @ Matrix.Rotation(math.radians(-25), 3, 'Y')  # duim draait iets naar de palmkant
    p = basis.copy(); last = b; hoek = 0
    for j, L in enumerate((2.0, 1.8, 1.5)):
        if j: hoek += pose['duim_krom'][j - 1]
        d = M @ rot_x(hoek) @ Vector((0, 1, 0))
        p = p + d * L
        last = add(p, (1.0, 0.88, 0.78)[j], last)
    TOPPEN.append(last)
    if stomp:   # onderarm-stompje (alleen voor losse handrenders)
        add((0, -3.5, 0.2), 1.9, pols)
    return V, E, R

def bouw(naam, pose, remesh=True, stomp=True):
    V, E, R = skelet(pose, stomp)
    toppen = [V[i].copy() for i in TOPPEN]
    me = bpy.data.meshes.new(naam); me.from_pydata([tuple(v) for v in V], E, []); me.update()
    ob = bpy.data.objects.new(naam, me); bpy.context.collection.objects.link(ob)
    sk = ob.modifiers.new('skin', 'SKIN')
    for i, r in enumerate(R):
        sv = me.skin_vertices[0].data[i]; sv.radius = (r, r * 0.8)   # iets plat (vingers zijn niet rond)
    me.skin_vertices[0].data[0].use_root = True
    sub = ob.modifiers.new('sub', 'SUBSURF'); sub.levels = 2; sub.render_levels = 2
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    for m in ('skin', 'sub'):
        bpy.ops.object.modifier_apply(modifier=m)
    ys = pose.get('ys', 1.0)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=(0, 4.7 * ys, 0.2))
    palm = bpy.context.object; palm.scale = pose.get('palm', (3.6, 4.1 * ys, 1.2))
    palm.select_set(True); ob.select_set(True); bpy.context.view_layer.objects.active = ob
    bpy.ops.object.join()
    if not remesh:
        ob.select_set(False)
        return ob, toppen
    rm = ob.modifiers.new('remesh', 'REMESH'); rm.mode = 'VOXEL'; rm.voxel_size = 0.07
    bpy.ops.object.modifier_apply(modifier='remesh')
    sm = ob.modifiers.new('glad', 'CORRECTIVE_SMOOTH'); sm.iterations = 8
    bpy.ops.object.modifier_apply(modifier='glad')
    bpy.ops.object.shade_smooth()
    ob.select_set(False)
    return ob

def materiaal(kleur):
    m = bpy.data.materials.new('vacht'); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = kleur; b.inputs['Roughness'].default_value = 0.9
    return m

def scene():
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 24
    sc.render.film_transparent = True
    sc.render.use_freestyle = True; sc.render.line_thickness_mode = 'ABSOLUTE'; sc.render.line_thickness = 1.5
    ls = sc.view_layers[0].freestyle_settings.linesets[0]
    ls.select_by_visibility = True; ls.select_silhouette = True; ls.select_border = True; ls.select_crease = True
    if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new('lijn')
    ls.linestyle.color = (0.1, 0.06, 0.15)
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.35
    zon = bpy.data.lights.new('zon', 'SUN'); zon.energy = 3.0
    zo = bpy.data.objects.new('zon', zon); sc.collection.objects.link(zo)
    d = Vector((0.45, -0.6, 1.0)).normalized()   # licht reist naar de palm, vanaf linksboven-voor (Game Freak)
    zo.rotation_euler = (-d).to_track_quat('Z', 'Y').to_euler()
    cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'; cam.ortho_scale = 22
    co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    co.location = (0, 6, -40); co.rotation_euler = Vector((0, 0, -1)).to_track_quat('Z', 'Y').to_euler()   # kijkt langs +Z naar de palm, +Y omhoog
    return sc

if __name__ == '__main__':
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = scene()
    mat = materiaal((0.30, 0.20, 0.55, 1))   # violet van de lijn (handkleur fase 2, #5E4488)
    welke = sys.argv[1:] or list(POSES)
    obs = {}
    for i, n in enumerate(POSES):
        ob = bouw(n, POSES[n]); ob.data.materials.append(mat); obs[n] = ob
    for n in welke:
        for m, ob in obs.items(): ob.hide_render = (m != n)
        sc.render.resolution_x = sc.render.resolution_y = 480
        sc.render.filepath = os.path.join(HIER, f'render_{n}.png')
        bpy.ops.render.render(write_still=True)
    for ob in obs.values(): ob.hide_render = False
    for i, ob in enumerate(obs.values()): ob.location.x = i * 16   # naast elkaar in het .blend-bestand
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HIER, 'hand.blend'), compress=True)
    print('KLAAR')
