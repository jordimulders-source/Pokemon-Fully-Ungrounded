"""Nachtaap fase 3: de kop als los onderdeel op het opgeslagen model (snel: ±20 s i.p.v. alles herbouwen).
Opent muriqui.blend, haalt de oude kop uit het lijf, bouwt de kop opnieuw naar foto 4/5 (Jordi: "het gezicht lijkt
nog steeds niet op een muriqui"), rendert een close-up + het hele model klein, slaat op.
Muriqui-gezicht (foto 4/5): groot kaal gezicht (±60% kopbreedte, wenkbrauw tot kin) dat als geheel naar voren
steekt, ingelijst door vacht; kleine diepe ogen onder een wenkbrauwrichel, dicht bij elkaar; lichte neusrug van
tussen de ogen naar een lange, brede snuit; brede rechte mond; donkere kin.
Gebruik: python3 kop.py [--niet-opslaan]"""
import math, os, sys, time
import numpy as np
import bpy
from mathutils import Vector

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import muriqui as M  # noqa: E402   (alleen hulpfuncties; bouwt niets bij import)

# ---- knoppen (kop-lokaal, in kopstralen R; -x = gezicht, y = omhoog, z = breedte) ----
R = 20.0                                 # schedel iets kleiner dan de oude bol (22)
GEZICHT = dict(c=(-0.50, -0.18, 0), r=(0.62, 0.80, 0.66))     # het hele kale gezicht steekt naar voren
SNUIT = dict(c=(-0.98, -0.62, 0), r=(0.42, 0.42, 0.44))        # lange, brede snuit
RICHEL = dict(c=(-0.92, 0.22, 0), r=(0.22, 0.14, 0.62))        # wenkbrauwrichel (vacht), rechte lijn
WANG = dict(c=(-0.45, -0.30, 0.55), r=(0.30, 0.45, 0.28))      # vachtlijst opzij van het gezicht (klein: geen oren/koptelefoon)
OOG_Z, OOG_Y, OOG_R, PUPIL_R = 0.27, 0.06, 0.13, 0.085         # klein, dicht bij elkaar, diep onder de richel
SIKKEL = True                                                    # kleine maansikkel van de lijn op het voorhoofd

t0 = time.time()
bpy.ops.wm.open_mainfile(filepath=os.path.join(HIER, 'muriqui.blend'))
pv, off = np.array((-4.0, 62.0, 0.0)), np.array((-42.0, -74.0, 0.0))
Rh = M.rot_y(math.radians(M.HEAD_EXTRA))
HC = pv + Rh @ (M.HEAD_C - pv) + off                       # kopmidden (dier)
Hp = lambda p: HC + Rh @ (np.asarray(p, float) * R)         # kop-lokaal (in R) -> dier
mats = {m.name: m for m in bpy.data.materials}

# opruimen: oude kopdelen, ogen, neus, mond, bladeren (Jordi: bladeren -> te Oranguru)
for o in list(bpy.data.objects):
    if o.name.split('_')[0].split('.')[0] in ('eye', 'pupil', 'glint', 'lid', 'neusgat', 'mond', 'blad', 'kop'):
        bpy.data.objects.remove(o, do_unlink=True)
lijf = bpy.data.objects['muriqui']
import bmesh
if not lijf.get('kop_los'):
    bm = bmesh.new(); bm.from_mesh(lijf.data)
    hcB = M.B(HC)
    weg = [v for v in bm.verts if (v.co - hcB).length < 21.5]
    bmesh.ops.delete(bm, geom=weg, context='VERTS'); bm.to_mesh(lijf.data); bm.free()
    lijf['kop_los'] = True

def ell(d, naam):
    c = np.array(d['c']); r = np.array(d['r']) * R
    return M.ellipsoid(Hp(c), r, Rh, naam)

delen = [M.ellipsoid(HC, (R, R * 1.02, R), Rh, 'kop'), ell(GEZICHT, 'kop_g'), ell(SNUIT, 'kop_s'), ell(RICHEL, 'kop_r')]
for sz in (1, -1):
    w = dict(WANG); w['c'] = (WANG['c'][0], WANG['c'][1], WANG['c'][2] * sz); delen.append(ell(w, 'kop_w'))
bpy.ops.object.select_all(action='DESELECT')
for d in delen: d.select_set(True)
bpy.context.view_layer.objects.active = delen[0]
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.join()
kop = bpy.context.object; kop.name = 'kop'
rm = kop.modifiers.new('rm', 'REMESH'); rm.mode = 'VOXEL'; rm.voxel_size = 0.3
M.pas_toe(kop)
sm = kop.modifiers.new('gl', 'LAPLACIANSMOOTH'); sm.iterations = 20; sm.lambda_factor = 1.0; sm.use_volume_preserve = True
M.pas_toe(kop)
bpy.ops.object.shade_smooth()

# kleurzones (kop-lokaal, in R)
for z in ('fur', 'mask', 'snuit', 'moon'): kop.data.materials.append(mats[z])
P = np.array([tuple(p.center) for p in kop.data.polygons]) @ M.C
u = ((P - HC) @ Rh) / R                                     # = Rh^T (P - HC) / R
def binnen(d, f=1.0):
    return np.linalg.norm((u - np.array(d['c'])) / (np.array(d['r']) * f), axis=1) < 1.0
idx = np.zeros(len(P), int)
gezicht = (binnen(GEZICHT, 1.06) | binnen(SNUIT, 1.08)) & (u[:, 0] < -0.35) & (u[:, 1] < 0.20) & ~binnen(RICHEL, 1.15)
idx[gezicht] = 1
# lichte neusrug: smal tussen de ogen, breder naar de snuit, tot de bovenlip (foto 5)
br = 0.07 + np.clip(0.10 - u[:, 1], 0, 1) * 0.30
idx[gezicht & (np.abs(u[:, 2]) < br) & (u[:, 1] < 0.04) & (u[:, 1] > -0.70) & (u[:, 0] < -0.75)] = 2
if SIKKEL:   # kleine maansikkel op het voorhoofd (lijn), ∩ met de punten omlaag, ruim boven de richel
    s, v = u[:, 2], u[:, 1]
    idx[(u[:, 0] < -0.2) & (s ** 2 + (v - 0.50) ** 2 < 0.30 ** 2) & (s ** 2 + (v - 0.42) ** 2 > 0.27 ** 2) & (v > 0.56)] = 3
kop.data.polygons.foreach_set('material_index', idx); kop.data.update()

# ogen: klein en diep onder de richel; lichtblauwe iris (Jordi), grote donkere pupil, glansje
for sz in (1, -1):
    x = -math.sqrt(max(0.0, 1 - OOG_Z ** 2 - OOG_Y ** 2)) - 0.30          # op het gezichtsvlak, dat naar voren steekt
    e = np.array((x, OOG_Y, OOG_Z * sz))
    for naam, pos, r in (('eye', e, OOG_R), ('pupil', e + np.array((-0.05, 0, 0)), PUPIL_R),
                         ('glint', e + np.array((-0.10, 0.04, -0.03 * sz)), 0.03)):
        o = M.ellipsoid(Hp(pos), (r * R, r * R, r * R), naam=f'{naam}_{sz}', seg=20)
        o.data.materials.append(mats[naam]); bpy.ops.object.shade_smooth()
    o = M.ellipsoid(Hp(SNUIT['c'] + np.array((-0.36, 0.18, 0.10 * sz))), (1.0, 1.3, 1.0), Rh, f'neusgat_{sz}', seg=12)
    o.data.materials.append(mats['neus'])
for zz in np.linspace(-0.30, 0.30, 15):     # brede, rechte mond onderaan de snuit (neutraal)
    yy = SNUIT['c'][1] - 0.22
    xx = SNUIT['c'][0] - SNUIT['r'][0] * math.sqrt(max(0.0, 1 - ((yy - SNUIT['c'][1]) / SNUIT['r'][1]) ** 2 - (zz / SNUIT['r'][2]) ** 2))
    o = M.ellipsoid(Hp((xx, yy, zz)), (0.5, 0.5, 0.5), naam='mond', seg=10); o.data.materials.append(mats['neus'])

# renders: close-up van de kop en het hele model klein
sc = bpy.context.scene; cam = sc.camera
oud = (cam.location.copy(), cam.data.ortho_scale)
fwd = cam.matrix_world.to_3x3() @ Vector((0, 0, -1))
cam.location = M.B(HC) - fwd * 400; cam.data.ortho_scale = 62
sc.render.resolution_x = sc.render.resolution_y = 420; sc.cycles.samples = 8
sc.render.filepath = os.path.join(HIER, 'render_kop.png'); bpy.ops.render.render(write_still=True)
cam.location, cam.data.ortho_scale = oud
sc.render.resolution_x = sc.render.resolution_y = 560; sc.cycles.samples = 6
if '--heel' in sys.argv:
    sc.render.filepath = os.path.join(HIER, 'render_snel.png'); bpy.ops.render.render(write_still=True)
if '--niet-opslaan' not in sys.argv:
    bpy.ops.wm.save_mainfile(compress=True)
print(f'KLAAR in {time.time() - t0:.0f} s')
