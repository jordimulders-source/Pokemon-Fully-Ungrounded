"""Bron voor sprite r3 uit het r5-model (bevroren, ../../../blender/r5/picapau_evo_r5.py), zelfde stand en kader als R5_8x:
(1) labels.png: elk onderdeel een vlakke eigen kleur (FLAT, geen omlijning), (2) wit.png: model wit (toonkaart),
(3) kleur.png: de gewone render (= R5_8x). Draaien: python3.11 renders.py"""
import os, sys, math
import numpy as np
HIER = os.path.dirname(os.path.abspath(__file__))
R5 = os.path.join(HIER, '../../../blender/r5'); sys.path.insert(0, os.path.join(HIER, '../../../blender/r3'))
import maak_r3
m = maak_r3.laad(os.path.join(R5, 'picapau_evo_r5.py'), 'r5')
import bpy
STAND = dict(lijf=35, kop_draai=5, oog_az=65, voorover=0, kantel=8)     # = maak_r5.STAND
LABEL = dict(lijf=(1, 0.5, 0), buik=(1, 1, 0.5), kop=(1, 0, 0.5), wang=(1, 0, 0), kuif=(0.5, 0, 0), kuifbinnen=(1, 0.5, 0.5),
             snavel=(0, 1, 1), mond=(0.5, 0.5, 0.5), vleugel_n=(0, 0.5, 0), vleugel_v=(0, 0, 0.5), pen_n=(0.5, 0.5, 0),
             pen_v=(0, 0.5, 0.5), stip=(0.5, 1, 0.5), koord=(0.5, 0, 1), staartveer=(1, 0, 1), bliksem=(1, 1, 0),
             oog=(0, 0, 1), glans=(0, 0, 1), poot=(1, 1, 1), klauw=(0, 0, 0))

def kader():
    """zelfde berekening als maak_r5.render(): proef op 0,6, centreren, passen in 61 px"""
    proef = os.path.join(HIER, '_proef.png'); s0 = 0.6
    m.render(proef, schaal=s0, **STAND); x0, y0, x1, y1 = maak_r3.bbox1x(proef); os.remove(proef)
    cx, cy = ((x0 + x1) / 2 - 32) / s0, ((y0 + y1) / 2 - 32) / s0
    s = 61.0 / (max(x1 - x0, y1 - y0) / s0)
    return s, (-cx * s, cy * s)

orig = m.kleur_vlakken
def labels_vlakken(huid, dl, kop_draai, kop_kantel):
    orig(huid, dl, kop_draai, kop_kantel)
    oud = [huid.data.materials[p.material_index].name for p in huid.data.polygons]
    C = np.array([tuple(p.center) for p in huid.data.polygons], np.float32)
    Rinv = np.array(m.kop_matrix(kop_draai, kop_kantel).transposed(), np.float32); nek = np.array(m.NEK, np.float32)
    Ck = (C - nek) @ Rinv.T + nek
    afst = np.stack([m.sdf_deel(Ck if g == 'kop' else C, deel) for _, deel, _, g in dl], 1)
    welk = [dl[i][0] for i in afst.argmin(1)]
    namen = list(LABEL); huid.data.materials.clear()
    for n in namen:
        mm = bpy.data.materials.get('L_' + n) or bpy.data.materials.new('L_' + n); mm.diffuse_color = (*LABEL[n], 1); huid.data.materials.append(mm)
    for j, (p, w, o) in enumerate(zip(huid.data.polygons, welk, oud)):
        kant = 'n' if C[j][1] < 0 else 'v'
        if w == 'lijf': n = 'buik' if o == 'creme' else 'lijf'
        elif w in ('vleugel', 'dekveer'): n = 'stip' if o == 'stip' else 'vleugel_' + kant
        elif w == 'pen': n = 'pen_' + kant
        elif w == 'staartveer': n = 'staartveer'
        elif w == 'staart': n = 'koord'
        elif w == 'bliksem': n = 'bliksem'
        elif w in ('kuif', 'kuifkrul'): n = 'kuifbinnen' if o == 'lijf' else 'kuif'
        elif w == 'kop': n = 'wang' if o == 'wang' else 'kop'
        elif w == 'snavel': n = 'snavel'
        elif w == 'mond': n = 'mond'
        else: n = 'lijf'
        p.material_index = namen.index(n)

if __name__ == '__main__':
    s, sch = kader(); print('kader r5:', s, sch)
    C = STAND
    m.kleur_vlakken = labels_vlakken; m.bouw.__globals__['kleur_vlakken'] = labels_vlakken
    kl = dict(m.KLEUR)
    for k in ('oog', 'glans', 'poot', 'klauw'): m.KLEUR[k] = LABEL[k]
    m.LIJF = float(C['lijf'])
    w = m.bouw(kop_draai=C['kop_draai'], voorover=C['voorover'], oog_az=C['oog_az'])
    w.rotation_euler = (0, 0, math.radians(C['lijf'])); w.scale = (s, s, s); w.location = (sch[0], 0, sch[1])
    m.camera_licht(512, C['kantel'])
    sh = bpy.context.scene.display.shading; sh.light = 'FLAT'; sh.show_object_outline = False; sh.show_cavity = False
    bpy.context.scene.render.filepath = os.path.join(HIER, 'labels.png'); bpy.ops.render.render(write_still=True)
    m.kleur_vlakken = orig; m.bouw.__globals__['kleur_vlakken'] = orig
    for k in list(m.KLEUR): m.KLEUR[k] = (0.8, 0.8, 0.8)
    m.render(os.path.join(HIER, 'wit.png'), schaal=s, schuif=sch, **C)
