"""Bron voor sprite v1 uit het C3-model (bevroren, ../../blender/r3/picapau_evo_r3.py), zelfde camera en kader als C3_8x:
(1) labels.png: elk onderdeel een vlakke eigen kleur (FLAT, geen omlijning/cavity), (2) wit.png: model wit (toonkaart).
Draaien: python3.11 renders.py"""
import os, sys, importlib.util
import numpy as np
HIER = os.path.dirname(os.path.abspath(__file__))
R3 = os.path.join(HIER, '../../blender/r3')
sys.path.insert(0, R3)
import maak_r3
spec = importlib.util.spec_from_file_location('r3', os.path.join(R3, 'picapau_evo_r3.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
import bpy

LABEL = dict(lijf=(1, 0.5, 0), buik=(1, 1, 0.5), kop=(1, 0, 0.5), wang=(1, 0, 0), kuif=(0.5, 0, 0), kuifbinnen=(1, 0.5, 0.5),
             snavel=(0, 1, 1), vleugel_n=(0, 0.5, 0), vleugel_v=(0, 0, 0.5), stip=(0.5, 1, 0.5), koord=(0.5, 0, 1),
             bliksem=(1, 1, 0), oog=(0, 0, 1), glans=(0, 0, 1), poot=(1, 1, 1))

orig = m.kleur_vlakken
def labels_vlakken(huid, dl, kop_draai, kop_kantel):
    orig(huid, dl, kop_draai, kop_kantel)
    oud = [huid.data.materials[p.material_index].name for p in huid.data.polygons]
    C = np.array([tuple(p.center) for p in huid.data.polygons], np.float32)
    Rinv = np.array(m.kop_matrix(kop_draai, kop_kantel).transposed(), np.float32); nek = np.array(m.NEK, np.float32)
    Ck = (C - nek) @ Rinv.T + nek
    afst = np.stack([m.sdf_deel(Ck if g == 'kop' else C, deel) for _, deel, _, g in dl], 1)
    welk = [dl[i][0] for i in afst.argmin(1)]
    namen = list(LABEL)
    huid.data.materials.clear()
    for n in namen:
        mm = bpy.data.materials.get('L_' + n) or bpy.data.materials.new('L_' + n); mm.diffuse_color = (*LABEL[n], 1); huid.data.materials.append(mm)
    for j, (p, w, o) in enumerate(zip(huid.data.polygons, welk, oud)):
        if w == 'lijf': n = 'buik' if o == 'creme' else 'lijf'
        elif w == 'vleugel': n = 'stip' if o == 'stip' else ('vleugel_n' if C[j][1] < 0 else 'vleugel_v')
        elif w == 'staart': n = 'koord'
        elif w == 'bliksem': n = 'bliksem'
        elif w in ('kuif', 'kuifkrul', 'kuif2'): n = 'kuifbinnen' if o == 'kuifmid' else 'kuif'
        elif w == 'kop': n = 'wang' if o == 'wang' else 'kop'
        elif w == 'snavel': n = 'snavel'
        else: n = 'lijf'
        p.material_index = namen.index(n)

if __name__ == '__main__':
    s, sch = maak_r3.kader_c2()
    print('kader C2/C3:', s, sch)
    C = maak_r3.C
    # labels
    m.kleur_vlakken = labels_vlakken
    for k in ('oog', 'glans', 'poot'): m.KLEUR[k] = LABEL[k]
    m.bouw.__globals__['kleur_vlakken'] = labels_vlakken
    w = m.bouw(kop_draai=C['kop_draai'], voorover=C['voorover'])
    import math
    w.rotation_euler = (0, 0, math.radians(C['lijf'])); w.scale = (s, s, s); w.location = (sch[0], 0, sch[1])
    m.camera_licht(512, C['kantel'])
    sh = bpy.context.scene.display.shading; sh.light = 'FLAT'; sh.show_object_outline = False; sh.show_cavity = False
    bpy.context.scene.render.filepath = os.path.join(HIER, 'labels.png'); bpy.ops.render.render(write_still=True)
    # wit (toonkaart)
    m.kleur_vlakken = orig; m.bouw.__globals__['kleur_vlakken'] = orig
    for k in list(m.KLEUR): m.KLEUR[k] = (0.8, 0.8, 0.8)
    m.render(os.path.join(HIER, 'wit.png'), schaal=s, schuif=sch, **C)
