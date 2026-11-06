"""MODELRONDE 3 (6 nov): alleen kuif en staart, naar Raichu Gen 1 (hoofdbron, Jordi: "nee de gen 1 raichu sprite moet je
ook naar kijken") en Gen 3 (aanvulling). Jordi over C2: "de oren en staart zijn geen raichu staart". De rest = ronde 2 (bevroren).
- kuif: platte driehoekige oren (prisma, scherpe vorm), kastanje buitenkant, gedempt lichte binnenkant, spiraal aan de punt
- staart: dikke donkerbruine koord in een S om het lijf, eindigend in een grote platte bliksem linksonder (prisma, scherpe hoeken)
Hieronder de kop van ronde 2:
MODELRONDE 2 (5 nov) van de Picapau-evolutie; ronde 1 = ../picapau_evo.py (blijft zoals het was).
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
Huid = één oppervlak (smooth union van afstandsvelden); kleurvlakken per vlak; snavel in de huid; ogen en pootjes los.
Draaien: python3.11 picapau_evo.py [uitmap] [hoeken...]   (rondom-vel)"""
import bpy, math, sys, os
import numpy as np
from mathutils import Vector, Euler, Matrix

def lin(r, g, b):
    """sRGB 0-255 -> lineair (diffuse_color is lineair)"""
    f = lambda c: (c / 255) / 12.92 if c / 255 <= 0.04045 else (((c / 255) + 0.055) / 1.055) ** 2.4
    return (f(r), f(g), f(b))

# Workbench (studio, zonder glans) rendert een belicht vlak ±0,73x zo licht: invoer = doelkleur / 0,73 (gemeten)
KLEUR = dict(lijf=lin(255, 142, 52),      # doel ±(206, 104, 38): warm oranje-kastanje (Celeus elegans)
             kuifmid=lin(255, 214, 150),  # r3: gedempt lichte binnenkant van de kuif-oren (doel ±(215, 160, 110), niet wit)
             koord=lin(100, 50, 28),      # r3: staartkoord donkerbruin (doel ±(72, 36, 20))
             vleugel=lin(190, 80, 32),    # doel ±(140, 58, 24): donkerder kastanje
             stip=lin(255, 245, 205),     # ronde lichte stippen (familie Picapau)
             staart=lin(220, 92, 38),     # doel ±(164, 68, 28): roodbruin
             bliksem=lin(255, 236, 70),   # bliksem: geel (Electric)
             creme=lin(255, 250, 222),    # buik en (klein) kuiftopje
             wang=lin(255, 54, 48), snavel=lin(255, 245, 196), oog=lin(8, 6, 6), glans=(1, 1, 1),
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
    if deel[0] == 'plaat':
        # platte prisma: 2D-veelhoeken (unie) in het vlak (oorsprong, e1, e2), halve dikte t, randafronding r
        _, o, e1, e2, polys, t, r = deel
        o, e1, e2 = (np.array(v, np.float32) for v in (o, e1, e2)); n = np.cross(e1, e2)
        q = P - o; a = q @ e1; b = q @ e2; c = q @ n
        d2 = None
        for poly in polys:
            di = sd_veelhoek(a, b, poly)
            d2 = di if d2 is None else np.minimum(d2, di)
        w1 = d2 + r; w2 = np.abs(c) - t + r
        return np.minimum(np.maximum(w1, w2), 0) + np.sqrt(np.maximum(w1, 0) ** 2 + np.maximum(w2, 0) ** 2) - r
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

def sd_veelhoek(a, b, v):
    """getekende afstand tot een 2D-veelhoek (Inigo Quilez, sdPolygon), gevectoriseerd"""
    v = np.array(v, np.float32); N = len(v)
    d = (a - v[0, 0]) ** 2 + (b - v[0, 1]) ** 2; sgn = np.ones_like(a)
    j = N - 1
    for i in range(N):
        ex, ey = v[j, 0] - v[i, 0], v[j, 1] - v[i, 1]; wx, wy = a - v[i, 0], b - v[i, 1]
        h = np.clip((wx * ex + wy * ey) / (ex * ex + ey * ey), 0, 1)
        bx, by = wx - ex * h, wy - ey * h
        d = np.minimum(d, bx * bx + by * by)
        c1 = b >= v[i, 1]; c2 = b < v[j, 1]; c3 = ex * wy > ey * wx
        flip = (c1 & c2 & c3) | (~c1 & ~c2 & ~c3)
        sgn = np.where(flip, -sgn, sgn)
        j = i
    return sgn * np.sqrt(d)

def band(A, B, wa, wb):
    A = np.array(A, float); B = np.array(B, float); u = (B - A) / np.linalg.norm(B - A); n = np.array([-u[1], u[0]])
    return [tuple(A + n * wa), tuple(B + n * wb), tuple(B - n * wb), tuple(A - n * wa)]

def smin(a, b, k):
    if k <= 0: return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


# ---------------- de evolutie ----------------
NEK = Vector((-3.0, 0, 5.0))           # draaipunt van de kop
HEUP = Vector((-1.5, 0, -16.5))       # draaipunt van de romp (voorover)
KC = Vector((-8.8, 0, 12.8))           # kopmidden (kop-lokaal); r1 (-8.5, 0, 12.5)
KR = (10.1, 9.7, 9.8)                  # kop licht groter dan r1 (9.6, 9.2, 9.3)

SNAVEL_HOEK = 8; SNAVEL_L = 19.0       # beitelsnavel (lengte vanaf de basis in de kop)

def kop_matrix(kop_draai, kop_kantel=0.0):
    """kop-lokaal -> lijf: draai om Z (naar de kijker) en een kleine kanteling, rond NEK"""
    R = Matrix.Rotation(math.radians(kop_draai), 3, 'Z') @ Matrix.Rotation(math.radians(kop_kantel), 3, 'Y')
    return R

def vleugel(s, schuif=(0.0, 0.0, 0.0)):
    """vogelvleugel, half open en opgetrokken (Jordi r1: "iets te draconian"): dikke ronde voorrand (arm),
    één gesloten vlak (hand- en armplaat), vier zachte ronde handpennen die grotendeels samensmelten"""
    schouder = (5.0, s * 9.5, 4.0); pols = (8.0, s * 18.5, 20.0)
    arm = np.array(pols) - np.array(schouder)
    n = np.cross(arm, np.array([1.0, 0, -0.2])); n = tuple(n / np.linalg.norm(n))
    d = [('vleugel', ('buis', [(schouder, 5.2), (pols, 4.8)], n, 0.45), 1.4),                              # ronde voorrand
         ('vleugel', ('buis', [((7.0, s * 13.0, 11.0), 6.8), ((16.0, s * 17.5, 3.0), 6.0), ((21.0, s * 19.0, -2.5), 4.0)], n, 0.36), 1.6),
         ('vleugel', ('buis', [(pols, 6.0), ((20.5, s * 23.0, 19.0), 7.6)], n, 0.36), 1.8)]               # handplaat (gesloten vlak)
    for tip in [(16.0, 23.0, 30.0), (22.5, 24.5, 26.0), (26.5, 24.0, 18.5), (27.0, 22.0, 9.5)]:
        tip = (tip[0], s * tip[1], tip[2])
        mid = tuple(np.array(pols) + 0.75 * (np.array(tip) - np.array(pols)))
        d.append(('vleugel', ('buis', [(pols, 5.0), (mid, 4.8), (tip, 3.4)], n, 0.36), 2.8))           # ronde, overlappende pennen
    if any(schuif):
        o = np.array(schuif)
        d = [(nm, ('buis', [(tuple(np.array(p) + o), r) for p, r in dl[1]], dl[2], dl[3]), k) for nm, dl, k in d]
    return d

VERRE_VLEUGEL = (5.0, 0.0, -11.0)   # r3: alleen de verre vleugel iets naar achteren en lager, zodat de kuif vrij staat

def staart_keten():
    """r3 (Raichu Gen 1): dikke donkerbruine koord (±4 px op 1x) in een S om het lijf: rechts achter het lijf vandaan,
    rechts omlaag, onder het lijf door naar links, naar de bliksem linksonder"""
    return [((11.0, 1.0, -8.0), 2.4), ((19.0, 1.0, -8.5), 2.4), ((26.5, 0.0, -11.5), 2.4), ((30.5, -0.5, -17.5), 2.4),
            ((28.5, 0.5, -24.5), 2.4), ((20.0, 2.5, -29.0), 2.4), ((8.0, 4.0, -30.0), 2.3), ((-3.0, 4.0, -28.5), 2.2),
            ((-9.0, 2.5, -25.5), 2.1)]

# bliksem: grote platte prisma met scherpe hoeken, in het beeldvlak van stand C (lijf 40) zodat hij vlak naar de kijker staat
BL_O = (-9.5, 2.0, -24.5)                                   # aanzet aan het eind van de koord
BL_E1 = (math.cos(math.radians(40)), -math.sin(math.radians(40)), 0.0)   # beeld-horizontaal bij lijf 40
BL_E2 = (0.0, 0.0, 1.0)
def bliksem_vlakken():
    u = np.array([-1.0, 1.15]); u /= np.linalg.norm(u); n = np.array([-u[1], u[0]]); P0 = np.zeros(2)
    return [band(P0, P0 + u * 17, 3.0, 3.4),                               # onderste band
            band(P0 + u * 13.5 - n * 3.2, P0 + u * 13.5 - n * 3.2 + u * 21, 3.6, 0.3)]   # verspringing + lange punt naar linksboven

def delen(kop_draai=25.0, kop_kantel=0.0):
    """lijst (naam, deel, k, groep); groep 'kop' wordt met de kopdraai rond NEK geëvalueerd"""
    d = [('lijf', ('ell', (3.0, 0, -5.0), (14.0, 13.5, 13.5), -15), 0, 'lijf'),        # = ronde 1
         ('lijf', ('ell', (-5.2, 0, -1.8), (10.2, 11.0, 11.5), -10), 3.0, 'lijf'),     # borst licht hoger en voller dan r1
         ('lijf', ('ell', (-3.0, 0, 5.5), (6.5, 7.5, 6.5), 0), 3.0, 'lijf')]          # dikke nek (= r1)
    # dijen in de huid: de poten groeien uit het lijf
    for s in (-1, 1):
        d.append(('lijf', ('ell', (-1.5, s * 4.5, -16.5), (3.2, 3.0, 3.2), 0), 1.5, 'lijf'))
    for naam, deel, k in vleugel(-1) + vleugel(1, VERRE_VLEUGEL):
        d.append((naam, deel, k, 'lijf'))
    d.append(('staart', ('buis', staart_keten(), (0, 1, 0), 1.0), 1.0, 'lijf'))
    d.append(('bliksem', ('plaat', BL_O, BL_E1, BL_E2, bliksem_vlakken(), 0.9, 0.35), 0.6, 'lijf'))
    # kop-groep (kop-lokale coördinaten)
    d.append(('kop', ('ell', tuple(KC), KR, 0), 3.5, 'kop'))
    # r3 kuif = Raichu-oren (Gen 1): brede platte driehoek (prisma) met aan de punt een spiraal naar buiten.
    # Maat als C2 (Jordi: "too much", "te wit, te groot"): top ±29,5, spiraal tot ±12,5 opzij.
    for s in (-1, 1):
        A = np.array([-9.5, s * 1.5, 20.5]); B = np.array([-7.5, s * 8.5, 18.5]); T = np.array([-5.6, s * 7.6, 28.4])
        e1 = (B - A) / np.linalg.norm(B - A); nn = np.cross(B - A, T - A); nn /= np.linalg.norm(nn)
        e2 = np.cross(nn, e1)
        v2 = [((p - A) @ e1, (p - A) @ e2) for p in (A, B, T)]
        d.append(('kuif', ('plaat', tuple(A), tuple(e1), tuple(e2), [v2], 0.75, 0.3), 1.2, 'kop'))
        # spiraal aan de punt: over de top naar buiten, omlaag en terug naar binnen, straal krimpt
        c = np.array([-5.4, s * 10.6, 29.4]); keten = []
        for i, hoek in enumerate(range(200, -210, -25)):
            rr = 3.0 - 1.3 * i / 16
            keten.append((tuple(c + np.array([0, s * math.cos(math.radians(hoek)) * rr, math.sin(math.radians(hoek)) * rr])), 0.75))
        d.append(('kuifkrul', ('buis', keten, (1, 0, 0), 1.0), 0.6, 'kop'))
    # beitelsnavel IN de huid (smooth union met de kop): een losse kegel stak schuin uit de gedraaide kop en gaf een
    # donker schaduwvlak dat als open snavel las. Iets plat van opzij (beitel).
    a = math.radians(SNAVEL_HOEK); dsn = np.array([-math.cos(a), 0, math.sin(a)])
    basis = np.array(KC) + np.array([-7.5, 0, -1.7])
    d.append(('snavel', ('buis', [(tuple(basis), 3.3), (tuple(basis + dsn * SNAVEL_L * 0.55), 1.9), (tuple(basis + dsn * SNAVEL_L), 0.35)],
                         (0, 1, 0), 0.85), 0.9, 'kop'))
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
    namen = ['lijf', 'vleugel', 'stip', 'staart', 'bliksem', 'creme', 'wang', 'kuifmid', 'snavel', 'koord']
    for n in namen: huid.data.materials.append(mat(n))
    C = np.array([tuple(p.center) for p in huid.data.polygons], np.float32)
    Rinv = np.array(kop_matrix(kop_draai, kop_kantel).transposed(), np.float32)
    nek = np.array(NEK, np.float32)
    Ck = (C - nek) @ Rinv.T + nek
    afst = np.stack([sdf_deel(Ck if g == 'kop' else C, deel) for _, deel, _, g in dl], 1)
    welk = [dl[i][0] for i in afst.argmin(1)]
    idx = np.zeros(len(C), int)
    Nk = np.array([tuple(p.normal) for p in huid.data.polygons], np.float32) @ Rinv.T   # normalen in kop-lokaal
    kopvlak = np.array([w == 'kop' for w in welk])
    if (np.einsum('ij,ij->i', Nk[kopvlak], Ck[kopvlak] - np.array(KC, np.float32))).mean() < 0: Nk = -Nk   # naar buiten
    for j, w in enumerate(welk):
        p = C[j]; q = Ck[j]
        if w == 'lijf':
            # crème buik: groot ovaal aan de voorkant (Raichu-buik, borst opgezet)
            b = ((p[0] + 9.5) / 9.2) ** 2 + (p[1] / 9.8) ** 2 + ((p[2] + 4.5) / 13.0) ** 2
            idx[j] = 5 if b < 1 else 0
        elif w == 'vleugel':
            idx[j] = 1
            # ronde lichte stippen (familie Picapau): rooster van stippen op de dekveren
            # minder en grotere stippen, alleen op de dekveren (binnenste deel van de vleugel), zoals Picapau
            # weinig, grote stippen (op 1x >= 2x2 px) op de dekveren
            if p[2] > 4 and p[0] < 20:
                g = np.array([p[0] / 8.5, p[2] / 8.5 + 0.5 * (round(p[0] / 8.5) % 2)])
                if np.hypot(*(g - np.round(g))) < 0.30: idx[j] = 2
        elif w == 'staart': idx[j] = 9
        elif w == 'bliksem': idx[j] = 4
        elif w == 'kuif':
            # binnenkant (voorvlak, normaal naar voren) gedempt licht, met een kastanje rand; buitenkant kastanje
            s_ = 1 if q[1] > 0 else -1
            A = np.array([-9.5, s_ * 1.5, 20.5]); B = np.array([-7.5, s_ * 8.5, 18.5]); T = np.array([-5.6, s_ * 7.6, 28.4])
            nn = np.cross(B - A, T - A); nn /= np.linalg.norm(nn)
            if nn[0] > 0: nn = -nn
            midden = (A + B + T) / 3
            binnen = Nk[j] @ nn > 0.5 and np.linalg.norm((q - midden) - ((q - midden) @ nn) * nn) < 3.2 and q[2] > 21.0
            idx[j] = 7 if binnen else 0
        elif w == 'kuifkrul': idx[j] = 0
        elif w == 'kuif2': idx[j] = 0
        elif w == 'snavel': idx[j] = 8
        elif w == 'kop':
            for s in (-1, 1):
                c = np.array([KC.x - 5.2, s * 6.5, KC.z - 3.8])
                r = q - c
                if (r[0] / 3.3) ** 2 + (r[1] / 3.3) ** 2 + (r[2] / 2.9) ** 2 < 1: idx[j] = 6
    for poly, i in zip(huid.data.polygons, idx): poly.material_index = int(i)

def bouw(kop_draai=25.0, kop_kantel=0.0, voorover=0.0, oog_az=75):
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
    # snavel zit in de huid (delen()); de tong-variant is in ronde 2 vervallen (op 1x een worm)
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
    sc.display.shading.show_specular_highlight = False      # glans maakte alle kleuren grijs
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
