"""Nachtaap fase 3 (muriqui): het hele model in Blender, één doorlopende huid (Jordi 3 nov: "je mag het hele model
in blender bouwen" / "zodat het 1 geheel wordt").
Pose en maten komen uit het goedgekeurde poppetje (`../pop3d/muriqui3d.py`, pose 'krabbel', lijf 40° / kop 80°):
dezelfde gewrichten, staartspiraal, kop met masker en sikkel. Leidend: SPEC.md (Jordi's woorden) en dat poppetje.
Opbouw: romp-bollen + ledematen (Skin) + handen/voeten uit hand.py -> één voxel-remesh -> glad -> kleurzones per vlak.
Ogen en bladeren blijven losse objecten (scherpe randen). Schrijft muriqui.blend + render_muriqui.png.
Gebruik: python3 muriqui.py   (pip install bpy)
Diercoördinaten (zoals het poppetje): x = naar achteren, y = omhoog, z = naar de kijker bij 0°.
Blender: B(x, y, z) = (x, -z, y)."""
import math, os, sys
import numpy as np
import bpy
from mathutils import Matrix, Vector

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import hand as H  # noqa: E402

C = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], float)   # dier -> Blender
YAW, PITCH, HEAD_EXTRA = 40.0, 6.0, 40.0
HEAD_C, HEAD_R = np.array((-8.0, 80.0, 0.0)), 22.0
LIMB = 10.5
SPIR_R, SPIR_YAW = 24.0, 40.0
POLSEN = []   # (middelpunt, straal) van handen/voeten: daar niet gladstrijken

KLEUR = {   # lijnkleuren van fase 2 (zoals het poppetje)
    'fur': '#5E4488', 'mask': '#2E2048', 'moon': '#FFFFFF', 'snuit': '#8C6A9C', 'tip': '#EAD8BE',
    'healer': '#E4DDF0', 'eye': '#D83C3C', 'pupil': '#1A1020', 'glint': '#FFFFFF', 'blad': '#5E9A4A',
}


def rot_y(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
def rot_x(a):
    c, s = math.cos(a), math.sin(a); return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
def rot_z(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
def qb(a, c, b, n):
    a, c, b = map(np.array, (a, c, b))
    return [(1 - t) ** 2 * a + 2 * (1 - t) * t * c + t * t * b for t in np.linspace(0, 1, n)]
def B(p):
    return Vector(C @ np.asarray(p, float))
def mat4(R3, t):
    M = Matrix.Identity(4)
    for i in range(3):
        for j in range(3):
            M[i][j] = R3[i, j]
        M[i][3] = t[i]
    return M


def ellipsoid(c, r, R0=None, naam='bol', seg=48):
    R0 = np.eye(3) if R0 is None else R0
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2)
    ob = bpy.context.object; ob.name = naam
    ob.matrix_world = mat4(C @ R0 @ np.diag(r) @ C.T, C @ np.asarray(c, float))
    return ob


def meta(bollen, naam='meta'):
    """Metaballs: ellipsoïden die vloeiend in elkaar overlopen (één romp i.p.v. losse bollen) -> mesh."""
    mb = bpy.data.metaballs.new(naam); mb.resolution = 1.0; mb.threshold = 0.6
    for c, r in bollen:
        el = mb.elements.new(); el.type = 'ELLIPSOID'; el.co = B(c)
        rb = np.abs(C @ np.asarray(r, float)); m = rb.max()
        el.radius = m * 1.25; el.size_x, el.size_y, el.size_z = rb / m
    ob = bpy.data.objects.new(naam, mb); bpy.context.collection.objects.link(ob)
    bpy.context.view_layer.update()
    bpy.ops.object.select_all(action='DESELECT'); bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    bpy.ops.object.convert(target='MESH')
    return bpy.context.object


def keten(pts, naam='keten'):
    """pts: [(x, y, z, straal)] in diercoördinaten -> buis via de Skin-modifier (verdicht: vloeiend taps)."""
    if len(pts) == 3:   # schouder-elleboog-pols: kwadratische boog die door het middelste gewricht gaat
        a, m, b = (np.array(p, float) for p in pts)
        c = 2 * m - (a + b) / 2
        pts = [tuple(v) for v in qb(a, c, b, 9)]
    dicht = []
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(2, int(np.linalg.norm(np.subtract(b[:3], a[:3])) / 2.0))
        dicht += [tuple(np.add(np.multiply(a, 1 - k / n), np.multiply(b, k / n))) for k in range(n)]
    pts = dicht + [pts[-1]]
    V = [tuple(B(p[:3])) for p in pts]
    E = [(i, i + 1) for i in range(len(V) - 1)]
    me = bpy.data.meshes.new(naam); me.from_pydata(V, E, []); me.update()
    ob = bpy.data.objects.new(naam, me); bpy.context.collection.objects.link(ob)
    ob.modifiers.new('skin', 'SKIN')
    for i, p in enumerate(pts):
        me.skin_vertices[0].data[i].radius = (p[3], p[3])
    me.skin_vertices[0].data[0].use_root = True
    ob.modifiers.new('sub', 'SUBSURF').levels = 3
    pas_toe(ob)
    return ob


def pas_toe(ob):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    for m in list(ob.modifiers):
        bpy.ops.object.modifier_apply(modifier=m.name)


def hand_op(pols, vingers, palm_naar, pose, schaal, spiegel=False, naam='hand'):
    """Plaatst een hand uit hand.py: pols = punt in diercoördinaten, vingers = richting van de vingers,
    palm_naar = de kant waar de handpalm naar kijkt, spiegel = duim aan de andere kant."""
    ob, toppen = H.bouw(naam, H.POSES[pose], remesh=False, stomp=False)
    f = np.asarray(vingers, float); f /= np.linalg.norm(f)
    n = np.asarray(palm_naar, float); n = n - (n @ f) * f; n /= np.linalg.norm(n)
    Z = -n; X = np.cross(f, Z)
    Rd = np.stack([X, f, Z], 1)            # hand-lokaal (X duimkant-, Y vingers, Z van de palm af) -> dier
    S = np.diag((-schaal if spiegel else schaal, schaal, schaal))
    M = mat4(C @ Rd @ S, C @ np.asarray(pols, float))
    ob.data.transform(M)
    if spiegel:
        ob.data.flip_normals()
    ob.data.update()
    POLSEN.append((np.asarray(pols, float) + f * 8 * schaal * 0.5, 9.5 * schaal))   # hand niet gladstrijken
    return ob, [M @ v for v in toppen], schaal


def bouw():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    view = np.array((-math.sin(math.radians(YAW)), 0, math.cos(math.radians(YAW))))   # naar de kijker (dier)
    delen, toppen = [], []
    # romp (pose 'krabbel'): borst/schouders, buik/rug, heup
    # (zelfde massa als de drie bollen van het poppetje, maar als één vloeiende romp: borst -> buik -> heup)
    romp = [((-12, 2, 0), (22, 22, 24)), ((14, 4, 0), (24, 22, 22)), ((32, 0, 0), (17, 18, 19))]
    # Jordi: "1 been en staart zitten niet goed smooth vast aan het lichaam": de wortel van elk lid groeit uit de
    # romp (metaball-elementen langs het eerste stuk), zodat er geen naad/insnoering is
    wortels = [((-16, 14, -20), (-24, 34, -26), LIMB), ((-18, -8, 20), (-28, -36, 26), LIMB),
               ((18, 14, -14), (12, 40, -18), LIMB + 4), ((36, -6, 14), (52, -24, 18), LIMB + 4),
               ((46, 6, 0), (46, -8, 0) + 34 * np.array((math.cos(math.radians(SPIR_YAW)), 0, math.sin(math.radians(SPIR_YAW)))), 7.5)]
    for a, b, r in wortels:
        a, b = np.array(a, float), np.array(b, float)
        for k, s in ((0.0, 1.25), (0.22, 1.1), (0.42, 1.0)):
            romp.append((tuple(a + (b - a) * k), (r * s, r * s, r * s)))
    delen.append(meta(romp, 'romp'))
    # verre arm omhoog-voor, vuist om een onzichtbare tak
    delen.append(keten([(-16, 14, -20, LIMB), (-24, 34, -26, LIMB - 2.5), (-40, 46, -24, LIMB - 4)]))
    h, t, s = hand_op((-40, 46, -24), (-0.55, 1, 0), (0.3, 0, -1), 'vuist', 2.4, naam='hand_ver'); delen.append(h); toppen += [(p, s) for p in t]
    # nabije arm naar linksonder; healerhand: vingers omhoog, palm naar de tegenstander (kijker), duim links
    delen.append(keten([(-18, -8, 20, LIMB), (-28, -36, 26, LIMB - 2.5), (-50, -60, 26, LIMB - 4)]))
    h, t, s = hand_op((-51, -61, 27), (-0.15, 1, 0.1), view, 'healer_drowzee', 2.7, spiegel=True, naam='hand_healer')   # duim links (krabbel)
    delen.append(h); toppen += [(p, s) for p in t]
    healer_pts = np.array([tuple(v.co) for v in h.data.vertices]) @ C      # handoppervlak (dier), voor de kleurzone
    # verre been omhoog, voet gekruld om een onzichtbare tak
    delen.append(keten([(18, 14, -14, LIMB + 4), (12, 40, -18, LIMB), (24, 58, -20, LIMB - 3)]))
    h, t, s = hand_op((24, 58, -20), (0.3, 1, 0), (1, 0, 0), 'voet_greep', 2.2, naam='voet_ver'); delen.append(h); toppen += [(p, s) for p in t]
    # nabije been sleept naar achteren-omlaag, voet ontspannen
    delen.append(keten([(36, -6, 14, LIMB + 4), (52, -24, 18, LIMB), (70, -22, 20, LIMB - 3)]))
    h, t, s = hand_op((70, -22, 20), (1, -0.5, 0), (0, -1, 0.3), 'voet_ontspannen', 2.2, naam='voet_nabij'); delen.append(h); toppen += [(p, s) for p in t]
    # staart: vanaf de heup naar achteren en omhoog, dan een volle spiraal (Nazca), binnenste slag iets naar de kijker
    ph = math.radians(SPIR_YAW)
    e1 = np.array((math.cos(ph), 0, math.sin(ph)))
    nrm = np.cross(e1, (0, 1, 0)); nrm = -nrm if nrm[2] < 0 else nrm
    T = np.array((28.0, 6, 0))
    path = qb((18, 0, 0), np.array((18, -14, 0)) + 34 * e1, np.array((0, 22, 0)) + 46 * e1, 9)
    c = np.array((0, 22.0, 0)) + (46 + SPIR_R) * e1
    spir = []
    for i in range(70):
        u = i / 69; a = math.pi - u * 1.6 * 2 * math.pi; rr = SPIR_R * (1 - 0.78 * u)
        spir.append(c + rr * math.cos(a) * e1 + np.array((0, rr * math.sin(a), 0)) + nrm * 7 * u)
    pts = path[:-1] + spir
    delen.append(keten([tuple(p + T) + (7.5 - 4.0 * i / (len(pts) - 1),) for i, p in enumerate(pts)], 'staart'))
    # kop: draait extra naar de kijker rond de nek en zit direct op de schouders (off)
    pv, off = np.array((-4.0, 62.0, 0.0)), np.array((-42.0, -74.0, 0.0))
    Rh = rot_y(math.radians(HEAD_EXTRA))
    Hp = lambda p: pv + Rh @ (np.asarray(p, float) - pv) + off
    kop_c = Hp(HEAD_C)
    delen.append(ellipsoid(kop_c, (HEAD_R, HEAD_R * 1.02, HEAD_R * 0.98), Rh, 'kop'))
    snuit_c = Hp(HEAD_C + np.array((-HEAD_R * 0.80, -HEAD_R * 0.42, 0)))
    delen.append(ellipsoid(snuit_c, (7, 7.5, 10), Rh, 'snuit'))
    # één geheel: samenvoegen, voxel-remesh, glad
    bpy.ops.object.select_all(action='DESELECT')
    for d in delen: d.select_set(True)
    bpy.context.view_layer.objects.active = delen[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)   # schaal in de mesh, niet in het object
    bpy.ops.object.join()
    lijf = bpy.context.object; lijf.name = 'muriqui'
    rm = lijf.modifiers.new('remesh', 'REMESH'); rm.mode = 'VOXEL'; rm.voxel_size = 0.45
    pas_toe(lijf)
    vg = lijf.vertex_groups.new(name='glad')
    W = np.array([tuple(v.co) for v in lijf.data.vertices])
    w = np.ones(len(W))
    for pols, r in POLSEN:
        dist = np.linalg.norm(W - np.array(tuple(B(pols))), axis=1)
        w = np.minimum(w, np.clip((dist - r) / r, 0, 1))
    for i, x in enumerate(w):
        vg.add([i], float(x), 'REPLACE')
    # Jordi: "smooth het ook uit ... niet een verzameling bollen": volumebehoudend (Laplace), buiten de handen
    sm = lijf.modifiers.new('glad', 'LAPLACIANSMOOTH'); sm.iterations = 60; sm.lambda_factor = 2.0
    sm.use_volume_preserve = True; sm.use_normalized = True; sm.vertex_group = 'glad'
    pas_toe(lijf)
    sm = lijf.modifiers.new('glad2', 'SMOOTH'); sm.iterations = 3; sm.factor = 0.4   # zachte afwerking overal
    pas_toe(lijf)
    bpy.ops.object.shade_smooth()
    # kleurzones per vlak (zelfde regels als texfn van het poppetje)
    mats = {k: materiaal(k) for k in KLEUR}
    zones = ['fur', 'mask', 'moon', 'snuit', 'tip', 'healer']
    for z in zones: lijf.data.materials.append(mats[z])
    me = lijf.data
    P = np.array([tuple(p.center) for p in me.polygons]) @ C          # Blender -> dier (C orthogonaal)
    idx = np.zeros(len(P), int)
    ql = (P - off - pv) @ Rh + pv                                      # terug naar kop-lokaal
    u = (ql - HEAD_C) / HEAD_R
    un = u / (np.linalg.norm(u, axis=1, keepdims=True) + 1e-9)
    cap = lambda lat, r: np.degrees(np.arccos(np.clip(un @ np.array((-math.cos(math.radians(lat)), math.sin(math.radians(lat)), 0)), -1, 1))) < r
    lon = np.degrees(np.arctan2(u[:, 2], -u[:, 0]))
    opkop = np.linalg.norm(u, axis=1) < 1.18
    mask = opkop & cap(-14.0, 52.0)
    idx[mask] = 1
    idx[opkop & cap(16.0, 70.0) & ~mask & ~cap(-30.0, 50.0) & (np.abs(lon) < 100) & (u[:, 1] > -0.55)] = 2
    sl = ((P - snuit_c) @ Rh) / np.array((7, 7.5, 10))
    idx[np.linalg.norm(sl, axis=1) < 1.15] = 3
    for p, s in toppen:   # laatste kootjes crème (vingertoppen, zoals fase 2)
        q = np.asarray(C.T @ np.array(tuple(p)))
        idx[np.linalg.norm(P - q, axis=1) < 1.5 * s] = 4
    # Jordi: "de healerhand mag best lichter zijn" / "leuk idee zelfs": de hele healerhand maanzilver (vanaf de pols)
    # per vlak: licht waar het dichter bij het handoppervlak ligt dan bij de onderarm (pols = lichaamskleur, Jordi)
    from mathutils import kdtree
    kd = kdtree.KDTree(len(healer_pts))
    for i, v in enumerate(healer_pts): kd.insert(v, i)
    kd.balance()
    hc, hr = POLSEN[1]
    kand = np.where(np.linalg.norm(P - hc, axis=1) < hr * 1.2)[0]
    a0, a1 = np.array((-28.0, -36, 26)), np.array((-51.0, -61, 27))       # onderarm (elleboog -> pols)
    for i in kand:
        d_hand = kd.find(P[i])[2]
        u = np.clip((P[i] - a0) @ (a1 - a0) / ((a1 - a0) @ (a1 - a0)), 0, 1)
        d_arm = np.linalg.norm(P[i] - (a0 + u * (a1 - a0))) - (LIMB - 4)
        if d_hand < 1.5 and d_hand < d_arm - 0.5:
            idx[i] = 5
    me.polygons.foreach_set('material_index', idx)
    me.update()
    # ogen: rode Espurr-ringogen met pupil en glans (fase 2), los object op het masker
    for sz in (1, -1):
        d = np.array((-0.88, 0.14, 0.40 * sz)); d /= np.linalg.norm(d)
        e = HEAD_C + d * HEAD_R * 0.94
        for k, (pos, r) in {'eye': (e, 3.9), 'pupil': (e + d * 1.6, 2.4), 'glint': (e + d * 2.8 + np.array((0, 1.3, -0.6 * sz)), 0.9)}.items():
            o = ellipsoid(Hp(pos), (r, r, r), naam=f'{k}_{sz}', seg=24); o.data.materials.append(mats[k]); bpy.ops.object.shade_smooth()
    # bladbundel in de krul
    cc = spir[-1] + T
    for ang, ln in ((50, 1.0), (82, 1.15), (114, 0.95)):
        a = math.radians(ang)
        d = math.cos(a) * e1 + np.array((0, math.sin(a), 0))
        o = ellipsoid(cc + d * 20 * ln + nrm * 3, (17 * ln, 6, 2.5), rot_y(-ph) @ rot_z(a), 'blad')
        o.data.materials.append(mats['blad']); bpy.ops.object.shade_smooth()
    return lijf


def materiaal(k):
    m = bpy.data.materials.new(k); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    h = KLEUR[k].lstrip('#'); rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    b.inputs['Base Color'].default_value = [c ** 2.2 for c in rgb] + [1]
    b.inputs['Roughness'].default_value = 0.85
    if k in ('mask', 'moon', 'eye', 'pupil', 'glint'):   # vlak, zoals NOSHADE in het poppetje
        b.inputs['Emission Color'].default_value = [c ** 2.2 for c in rgb] + [1]
        b.inputs['Emission Strength'].default_value = 0.6
    return m


def scene(res=720):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 12
    sc.render.film_transparent = True
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.use_freestyle = True; sc.render.line_thickness_mode = 'ABSOLUTE'; sc.render.line_thickness = 2.0
    fs = sc.view_layers[0].freestyle_settings
    ls = fs.linesets[0] if len(fs.linesets) else fs.linesets.new('lijn')
    ls.select_by_visibility = True
    ls.select_silhouette = True; ls.select_border = True; ls.select_crease = False; ls.select_material_boundary = True
    if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new('lijn')
    ls.linestyle.color = (0.08, 0.05, 0.12)
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.45
    # camera zoals het poppetje: Rc = rot_x(pitch) @ rot_y(yaw); kijker op +z na Rc
    Rc = rot_x(math.radians(PITCH)) @ rot_y(math.radians(YAW))
    naar_kijker, op = Rc.T @ np.array((0, 0, 1.0)), Rc.T @ np.array((0, 1.0, 0))
    cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'; cam.ortho_scale = 230
    co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    # kader: alle objecten, geprojecteerd op het beeldvlak
    rechts = np.cross(op, naar_kijker)
    pts = np.array([tuple(o.matrix_world @ v.co) for o in bpy.data.objects if o.type == 'MESH' for v in o.data.vertices]) @ C
    sx, sy = pts @ rechts, pts @ op
    midden = rechts * (sx.min() + sx.max()) / 2 + op * (sy.min() + sy.max()) / 2
    cam.ortho_scale = max(sx.max() - sx.min(), sy.max() - sy.min()) * 1.08
    co.location = B(midden + naar_kijker * 400)
    co.rotation_euler = (-B(naar_kijker)).to_track_quat('-Z', 'Y').to_euler()
    # rol goed zetten: camera-Y moet 'op' zijn
    co.rotation_euler = Matrix(np.stack([np.cross(C @ op, C @ naar_kijker), C @ op, C @ naar_kijker], 1).tolist()).to_euler()
    # licht van linksboven-voor (Game Freak), in schermrichting
    licht_naar = Rc.T @ np.array((0.5, -0.6, -1.0)); licht_naar /= np.linalg.norm(licht_naar)
    zon = bpy.data.lights.new('zon', 'SUN'); zon.energy = 3.2
    zo = bpy.data.objects.new('zon', zon); sc.collection.objects.link(zo)
    zo.rotation_euler = (-B(licht_naar)).to_track_quat('Z', 'Y').to_euler()
    return sc


if __name__ == '__main__':
    bouw()
    sc = scene(int(sys.argv[1]) if len(sys.argv) > 1 else 720)
    sc.render.filepath = os.path.join(HIER, 'render_muriqui.png')
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HIER, 'muriqui.blend'), compress=True)
    print('KLAAR')
