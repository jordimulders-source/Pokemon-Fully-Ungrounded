"""POSE-PROEF r7pose (6 nov), kopie van r6pose (blijft staan). Jordi over de poseproef, letterlijk: "ik kies p3, en hij mag
nog iets meer naar rechts draaien, net als gen 1 raichu beide ogen in beeld, of gaat het niet passen om ook de linkervleugel
in de sprite te krijgen lichtjes? Zijn er vogel sprites die dat hebben?"
Nieuw (instelbaar vanuit maak_pose.py): TWEE_OGEN (ook het verre oog), SNAVEL_HOEK (negatief = snavel schuin naar links-onder,
zoals Ho-Oh, zodat hij bij een frontale kop niet verkort), VERRE_VLEUGEL (verre vleugel opgetild, zodat hij links achter
borst en kop uitsteekt).
Hieronder de kop van r6pose:
POSE-PROEF r6pose (6 nov), kopie van r5 (r5 en r6 blijven ongewijzigd). Jordi over sprite r4, letterlijk: "dit is geen
driekwart aanzicht, laten we daar mee beginnen. Zijn mond is gewoon een rode wolk, de kuif staat teveel rechtop, die mag
meer naar beneden buigen. Maar het begint met het driekwart aanzicht wat niet klopt en de hele sprite mag wat meer
achterover leunen zoals raichu in gen 1".
Alleen in dit bestand veranderd: de oren buigen naar achteren-opzij en iets omlaag (punt T lager en verder naar buiten);
de pose zelf (lijfdraai, achterover, kopdraai, oog) zit in de stand (maak_pose.py).
Hieronder de kop van ronde 5:
MODELRONDE 5 (6 nov), kopie van r4 V2 (r4 blijft ongewijzigd). Jordi over r4 V2, letterlijk: "ja nu komen we ergens!
de snavel mag open, dat geeft wat karakter. Vergeet mijn eerdere instructies over de oren, die mogen dunner en wat verder
doorkrullen, iets meer zoals de onderkant van de oren van raichu"; imposant-ronde: "ja".
Nieuw in r5: lijf meer voorover (Talonflame-diagonaal, in de vorm zelf: romp/borst/nek kantelen, kop blijft rechtop),
vleugels hoger en breder open, bliksem kleiner (0,75), grote voeten met klauwen (verre poot hoger en verder naar achteren),
open beitelsnavel (boven- en ondersnavel + donkere mond), dunnere oren met een echte spiraal (±1 slag) onder aan de punt.
Hieronder de kop van ronde 4:
MODELRONDE 4 (6 nov), kopie van r3 (r3 blijft ongewijzigd). Jordi over sprite r2, letterlijk: "het ding is, het is nog
niet echt een vogel he. De staart mag wat dunner en wat meer vogelachtig, desnoods zwart. De oren mogen ook naar achter
bewegen, zwart en meer op de raichu lijken, verder mag die wat graden naar links draaien, want nu zien we een flink stuk
hoofd met het oog helemaal aan de zijkant. De vleugel mag iets vogel achtiger"
Nieuw in r4 (de rest = r3: lijf, buik, kop, snavel, kleuren, bliksem):
- oren: verder naar achteren op de schedel, zwart, Gen 1-vorm: de oorpunt loopt zelf uit in de krul (geen ring op een steel);
  binnenkant lijfkleur (zoals Gen 3, geel = lijfkleur), niet wit; maat als r3. De rafelige achterkuif (kuif2) vervalt: daar staan nu de oren.
- staart: steunstaart van 3 stijve spechtenveren aan de stuit + één dunne zwarte veerschacht (zoals een racketstaart:
  drongo/motmot) in dezelfde S om het lijf, met de bliksem als 'racket' aan het eind.
- vleugel: echte vogelvleugel uit platte lagen: ronde voorrand (arm), rij kleine dekveren, rij grote dekveren (met de ronde
  lichte stippen), armpennen en zes handpennen in een waaier; elke laag ligt iets dichter naar de kijker dan de laag eronder.
- draaien: lijf/kop_draai via de stand (maak_r4.py); oog_az iets kleiner zodat het oog meer naar de snavel zit.
AANVULLING Jordi (6 nov), letterlijk: "ja het lijkt nu iets meer een alien dan een vogel, en ik heb liever eigenlijk een
grote vogel met raichu motief" -> het ronde ei-lijf van r3 vervalt. Nieuw lijf = grote vogel (Talonflame, Staraptor,
Braviary, Pidgeot; echte grote specht Dryocopus/Campephilus): borst die naar voren steekt, duidelijke nek, lijf dat schuin
naar achteren-onder loopt naar stuit en steunstaart, dijen en poten onder het zwaartepunt, kop klein in verhouding.
Raichu = alleen motief: zwarte oren met krul, dunne zwarte staart die krult met de grote bliksem, kleur, wangvlek.
Hieronder de kop van ronde 3:
MODELRONDE 3 (6 nov): alleen kuif en staart, naar Raichu Gen 1 (hoofdbron, Jordi: "nee de gen 1 raichu sprite moet je
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
             koord=lin(44, 34, 32),       # r4: staartschacht zwart (doel ±(32, 25, 24)); Jordi: "desnoods zwart"
             oor=lin(44, 34, 32),         # r4: oren zwart (Jordi: "zwart en meer op de raichu lijken")
             mond=lin(70, 22, 26),       # r5: donkere mondopening tussen boven- en ondersnavel
             klauw=lin(40, 36, 40),      # r5: klauwen
             pen=lin(130, 52, 26),        # r4: arm- en handpennen + steunstaart, donker kastanje (doel ±(96, 40, 20))
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
# r4 grote vogel: kop kleiner en hoger, op een duidelijke nek boven de vooruitstekende borst
NEK = Vector((-12.0, 0, 7.0))          # draaipunt van de kop (onder in de nek)
HEUP = Vector((-2.0, 0, -16.0))        # draaipunt van de romp (voorover)
KC = Vector((-15.0, 0, 18.5))          # kopmidden (kop-lokaal); r3 (-8.8, 0, 12.8)
KR = (8.2, 7.6, 7.8)                   # r3 (10.1, 9.7, 9.8): kop in verhouding tot een vogel
OOR_F = 1.0                            # oormaat (Jordi eerder: "too much", "te wit, te groot": op 1x niet groter dan r2)

SNAVEL_HOEK = 6; SNAVEL_L = 15.5
TWEE_OGEN = False
VERRE_OPEN = 0.0     # graden; r7pose: verre vleugel naar buiten klappen       # beitelsnavel (lengte vanaf de basis in de kop)

def kop_matrix(kop_draai, kop_kantel=0.0):
    """kop-lokaal -> lijf: draai om Z (naar de kijker) en een kleine kanteling, rond NEK"""
    R = Matrix.Rotation(math.radians(kop_draai), 3, 'Z') @ Matrix.Rotation(math.radians(kop_kantel), 3, 'Y')
    return R

def veer(basis, tip, w, punt=0.5, n=7):
    """2D-veer: van de basis (breedte 0,7w) naar een afgeronde punt (halve cirkel, punt<1 = iets spitser)"""
    B = np.array(basis, float); T = np.array(tip, float); u = (T - B) / np.linalg.norm(T - B); v = np.array([-u[1], u[0]])
    r = w / 2; C = T - u * r
    pts = [tuple(B + v * w * 0.35), tuple(B + (C - B) * 0.55 + v * r)]
    for i in range(n + 1):
        h = math.pi * i / n; pts.append(tuple(C + v * r * math.cos(h) + u * r * math.sin(h) * (1 + punt)))
    pts += [tuple(B + (C - B) * 0.55 - v * r), tuple(B - v * w * 0.35)]
    return pts[::-1]

STIPPEN = []   # 3D-middelpunten (lijf-lokaal) van de ronde lichte stippen, gevuld door vleugel()

def vleugel(s, schuif=(0.0, 0.0, 0.0)):
    """r4: echte vogelvleugel, half open en opgetrokken (Jordi: "De vleugel mag iets vogel achtiger"), als platte lagen in
    het vleugelvlak (a = langs de arm van schouder naar pols, b = naar de achterrand):
    voorrand (dikke ronde arm) > kleine dekveren > grote dekveren (stippen) > armpennen > handpennen (waaier).
    Elke hogere laag ligt 0,8 BU dichter naar de kijker (-Y), zodat de randen als lagen over elkaar lezen."""
    o = np.array(schuif, float)
    S = np.array([1.0, s * 7.5, 3.0]) + o; P = np.array([5.0, s * 17.0, 21.0]) + o; Q = np.array([29.0, s * 22.5, 13.0]) + o   # r5: hoger, breder open
    if s > 0 and VERRE_OPEN:     # r7pose: verre vleugel om de schouder (as X) naar buiten geklapt, zoals Pidgeot links achter de kop
        h = math.radians(VERRE_OPEN); c_, s_ = math.cos(h), math.sin(h)
        def klap(p):
            d = p - S; return S + np.array([d[0], d[1] * c_ + d[2] * s_, -d[1] * s_ + d[2] * c_])
        P = klap(P); Q = klap(Q)
    e1 = (P - S) / np.linalg.norm(P - S); nn = np.cross(P - S, Q - S); nn /= np.linalg.norm(nn)
    if nn[1] > 0: nn = -nn                        # nn wijst naar de kijker (-Y)
    e2 = np.cross(nn, e1)
    if (Q - S) @ e2 < 0: e2 = -e2
    WS = VLEUGEL_S
    def plaat(polys, laag, t=0.7):
        polys = [[(x * WS, y * WS) for x, y in pl] for pl in polys]
        org = S + nn * (0.8 * laag)
        return ('plaat', tuple(org), tuple(e1), tuple(e2), polys, t, 0.3)
    def w3(a, b, laag): return tuple(S + e1 * a * WS + e2 * b * WS + nn * (0.8 * laag + 0.7))
    d = [('vleugel', ('buis', [(tuple(S), 4.2), (tuple(P), 3.4), (tuple(P + e1 * 3.0 * WS + e2 * 2.0 * WS), 2.6)], tuple(nn), 0.5), 1.4)]
    # handpennen: zes lange veren in een waaier vanuit de hand, buitenste het langst; elk 0,15 laag hoger (dakpansgewijs)
    hand = [((17.0, 3.0), (32.5, 4.5), 5.0), ((16.0, 5.0), (31.5, 10.0), 5.2), ((15.0, 6.5), (28.5, 15.0), 5.2),
            ((13.5, 8.0), (24.5, 19.0), 5.2), ((12.0, 9.0), (19.5, 21.5), 5.0), ((10.0, 9.5), (14.0, 22.5), 5.0)]
    for i, (B, T, w) in enumerate(hand):
        d.append(('pen', plaat([veer(B, T, w, 0.35)], -1.0 + 0.15 * i, 0.55), 0.25))
    # armpennen: korter, breder, ronde eind, vanaf de arm naar de achterrand
    for B, T, w in [((8.5, 7.0), (9.5, 21.5), 5.2), ((5.0, 6.0), (4.5, 20.0), 5.4), ((1.5, 5.0), (0.0, 17.5), 5.4)]:
        d.append(('pen', plaat([veer(B, T, w, 0.0)], -0.2, 0.55), 0.25))
    # grote dekveren: rij korte brede veren met ronde eind (geschulpte rand), elk met een ronde lichte stip
    grote = [((17.5, 1.0), (21.0, 8.0)), ((14.0, 1.0), (16.0, 11.5)), ((10.0, 1.0), (11.0, 12.5)), ((6.0, 1.0), (6.5, 12.5)),
             ((2.0, 1.0), (2.0, 11.5)), ((-1.5, 1.0), (-2.0, 9.5))]
    for B, T in grote:
        d.append(('dekveer', plaat([veer(B, T, 4.8, 0.0)], 0.6, 0.6), 0.35))
        B_ = np.array(B); T_ = np.array(T); m = B_ + (T_ - B_) * 0.68
        STIPPEN.append((w3(m[0], m[1], 0.6), 1.45 * WS))
    # kleine dekveren: smalle rij langs de voorrand, ook met kleine stippen (zoals Picapau)
    for a in (16.0, 12.0, 8.0, 4.0, 0.0):
        d.append(('dekveer', plaat([veer((a + 0.5, -1.0), (a - 0.5, 5.5), 4.2, 0.0)], 1.4, 0.6), 0.35))
    for a in (12.0, 4.0):
        STIPPEN.append((w3(a - 0.3, 3.4, 1.4), 1.1 * WS))
    return d

VLEUGEL_S = 1.32                   # r5: grotere vleugels (r4 1,2)
VERRE_POOT = (3.5, 0.0, 4.0)        # r5: verre poot hoger en verder naar achteren (niet naast de nabije)
VERRE_VLEUGEL = (14.0, 0.0, -5.0)   # r5: verre vleugel verder naar achteren, zodat de zwarte oorkrullen niet tegen de donkere vleugel vallen

def staart_keten():
    """r4: dunne zwarte veerschacht (r 1,3 i.p.v. 2,4; Jordi: "De staart mag wat dunner en wat meer vogelachtig, desnoods
    zwart") in dezelfde S als r3: uit de steunstaart naar rechts, rechts omlaag, onder het lijf door naar de bliksem"""
    return [((28.0, 1.5, -21.5), 1.2), ((32.5, 1.0, -23.0), 1.25), ((34.0, 0.5, -28.5), 1.3), ((30.0, 1.0, -34.0), 1.3),
            ((20.0, 2.5, -36.0), 1.3), ((8.0, 3.5, -36.0), 1.3), ((-4.0, 2.0, -34.5), 1.35), ((-12.0, -1.5, -31.5), 1.4), ((-15.5, -3.0, -30.0), 1.5)]

def steunstaart():
    """stijve spechtenstaart (familie Picapau): drie spitse veren uit de stuit, plat naar de kijker (vlak van de bliksem)"""
    o = (21.5, 2.0, -13.0)   # r5: stuit van het voorovergekantelde lijf
    vv = [veer((0.0, 0.0), (10.0, -6.5), 4.2, 1.2), veer((-0.5, -1.0), (8.0, -9.5), 4.2, 1.2), veer((-1.0, -2.0), (5.0, -11.0), 4.0, 1.2)]
    return ('plaat', o, bl_e1(), BL_E2, vv, 0.8, 0.3)

# bliksem: grote platte prisma met scherpe hoeken, in het beeldvlak van stand C (lijf 40) zodat hij vlak naar de kijker staat
BL_O = (-16.0, -3.0, -29.5)   # r5: verder naar links, zodat de grote buik de bliksem niet bedekt
BL_S = 0.75                                                  # r5: bliksem kleiner, zodat de vogel groter in het frame staat                                   # aanzet aan het eind van de koord
LIJF = 40.0   # r4: wordt door render() gezet, zodat bliksem en steunstaart vlak naar de kijker blijven staan
BL_E1 = (math.cos(math.radians(40)), -math.sin(math.radians(40)), 0.0)   # beeld-horizontaal bij lijf 40 (zie bl_e1())
def bl_e1(): return (math.cos(math.radians(LIJF)), -math.sin(math.radians(LIJF)), 0.0)
BL_E2 = (0.0, 0.0, 1.0)
def bliksem_vlakken():
    u = np.array([-1.0, 1.15]); u /= np.linalg.norm(u); n = np.array([-u[1], u[0]]); P0 = np.zeros(2)
    k = BL_S; w = max(BL_S, 0.85)    # breedte minder krimpen dan lengte: op 1x >= 2-3 px
    return [band(P0, P0 + u * 17 * k, 3.0 * w, 3.4 * w),                               # onderste band
            band(P0 + u * 13.5 * k - n * 3.2 * w, P0 + u * 13.5 * k - n * 3.2 * w + u * 21 * k, 3.6 * w, 0.3)]   # verspringing + lange punt naar linksboven

OOR_SCHUIF = 0.0   # varianten: oor iets naar voren/achteren (BU langs X, kop-lokaal)

def oor_punten(s):
    # r4: zelfde oor als hierboven ontworpen op de r3-kop (midden (-8,8; 12,8)), nu meegeschaald naar de kleinere kop
    k = np.array(KC); f = OOR_F; sh = np.array([OOR_SCHUIF, 0, 0])
    # A = voorste voet, B = achterste voet (achter op de schedel), T = punt, schuin naar achteren-boven (Raichu)
    return [k + f * np.array(v) + sh for v in ((1.5, s * 2.0, 7.6), (5.5, s * 3.2, 5.4), (12.5, s * 8.5, 6.5))]   # r6pose: punt naar achteren-opzij, iets omlaag (was (12,0; 6,5; 12,5))

def oor_vlak(s):
    A, B, T = oor_punten(s)
    e1 = (B - A) / np.linalg.norm(B - A); nn = np.cross(B - A, T - A); nn /= np.linalg.norm(nn); e2 = np.cross(nn, e1)
    return A, B, T, e1, e2, nn

def oor(s):
    """Raichu Gen 1-oor: platte brede driehoek (basis A-B op de schedel, punt T naar achteren-boven) die aan de punt
    zelf overgaat in een krul naar achteren en omlaag (spiraal in het oorvlak, straal krimpt)"""
    A, B, T, e1, e2, nn = oor_vlak(s)
    v2 = [((p - A) @ e1, (p - A) @ e2) for p in (A, B, T)]
    a_, b_, t_ = (np.array(p) for p in v2); uu = (t_ - (a_ + b_) / 2)
    blad = [tuple(a_), tuple(b_), tuple(b_ + uu * 0.5 + (a_ - b_) * 0.02), tuple(t_), tuple(a_ + uu * 0.55 - (a_ - b_) * 0.15)]
    d = [('kuif', ('plaat', tuple(A), tuple(e1), tuple(e2), [blad], 0.7, 0.3), 1.2)]
    t2 = np.array(v2[2]); m2 = (np.array(v2[0]) + np.array(v2[1])) / 2
    u = (t2 - m2) / np.linalg.norm(t2 - m2); v = np.array([u[1], -u[0]])       # v: naar de achterrand (B-kant)
    if v @ (np.array(v2[1]) - np.array(v2[0])) < 0: v = -v
    if (e1 * v[0] + e2 * v[1])[2] > 0: v = -v                                # r5: de krul hangt ónder de punt (Raichu), bij beide oren
    r0 = 4.6 * OOR_F; c = t2 + v * r0; a0 = math.atan2(*(t2 - c)[::-1])
    rot = 1 if (u[0] * v[1] - u[1] * v[0]) < 0 else -1                        # eerst langs u, dan naar v toe
    keten = []
    for i in range(18):                     # r5: ±410 graden, echte spiraal die naar binnen rolt (Raichu: onderkant van het oor), straal 4,6 -> 1,9
        h = a0 + rot * math.radians(-24 * i); rr = r0 * (1 - 0.59 * i / 17)
        p2 = c + rr * np.array([math.cos(h), math.sin(h)])
        keten.append((tuple(A + e1 * p2[0] + e2 * p2[1]), 1.2 - 0.35 * i / 17))   # lijn >= 2 px op 1x
    d.append(('kuifkrul', ('buis', keten, tuple(nn), 0.6), 0.5))
    return d

def delen(kop_draai=25.0, kop_kantel=0.0):
    """lijst (naam, deel, k, groep); groep 'kop' wordt met de kopdraai rond NEK geëvalueerd"""
    STIPPEN.clear()
    # r4 grote vogel: borst steekt naar voren, romp loopt schuin naar achteren-onder naar de stuit, duidelijke nek
    # r5: lijf 15-20 graden meer voorover (Talonflame-diagonaal): de lijfas ligt platter (romp 35 -> 18 graden onder de
    # horizontaal), de borst is langgerekt langs die as en steekt naar voren, de nek staat schuin naar voren
    d = [('lijf', ('ell', (-7.0, 0, -2.0), (12.5, 10.0, 10.0), 22), 0, 'lijf'),          # vooruitstekende borst
         ('lijf', ('ell', (5.5, 0, -7.0), (15.0, 9.0, 8.0), 18), 4.0, 'lijf'),           # romp, schuin naar achteren
         ('lijf', ('ell', (17.5, 0, -11.5), (6.5, 6.0, 4.8), 18), 3.0, 'lijf'),          # stuit
         # r5 Jordi: "de buik echt naar voren ... een beetje op die gen 1 raichu pose": grote bolle buik vooraan-onder,
         # puilt naar voren (-X) en iets naar de kijker (-Y) uit; het lijf buigt er gedrongen omheen
         ('lijf', ('ell', (-13.0, -2.5, -7.5), (12.0, 12.0, 12.5), 0), 4.0, 'lijf'),
         ('lijf', ('buis', [((-10.0, 0, 2.5), 6.8), ((-13.0, 0, 8.5), 5.4), ((-14.0, 0, 13.5), 5.0)], (0, 1, 0), 1.0), 3.0, 'lijf')]  # nek
    # bevederde dijen onder het zwaartepunt (onder de borst/romp-overgang)
    for s in (-1, 1):
        o = np.array(VERRE_POOT if s > 0 else (0.0, 0.0, 0.0))
        d.append(('lijf', ('ell', tuple(np.array((-1.5, s * 4.5, -13.0)) + o * 0.5), (4.5, 3.6, 4.8), 0), 2.0, 'lijf'))
    for naam, deel, k in vleugel(-1) + vleugel(1, VERRE_VLEUGEL):
        d.append((naam, deel, k, 'lijf'))
    d.append(('staartveer', steunstaart(), 1.0, 'lijf'))
    d.append(('staart', ('buis', staart_keten(), (0, 1, 0), 1.0), 0.5, 'lijf'))
    d.append(('bliksem', ('plaat', BL_O, bl_e1(), BL_E2, bliksem_vlakken(), 0.9, 0.35), 0.6, 'lijf'))
    # kop-groep (kop-lokale coördinaten)
    d.append(('kop', ('ell', tuple(KC), KR, 0), 3.5, 'kop'))
    # r4 kuif = Raichu-oren (Gen 1), verder naar achteren op de schedel, zwart; de oorpunt loopt zelf uit in de krul
    for s in (-1, 1):
        for naam, deel, k in oor(s): d.append((naam, deel, k, 'kop'))
    # beitelsnavel IN de huid (smooth union met de kop): een losse kegel stak schuin uit de gedraaide kop en gaf een
    # donker schaduwvlak dat als open snavel las. Iets plat van opzij (beitel).
    # r5 open beitelsnavel (Jordi: "de snavel mag open, dat geeft wat karakter"): bovensnavel iets omhoog, ondersnavel
    # omlaag, beide >= 2 px op 1x; daartussen een donkere mondopening (plaat in het middenvlak van de kop)
    basis = np.array(KC) + np.array([-6.0, 0, -1.3])
    for naam, hoek, L, r in (('snavel', SNAVEL_HOEK + 5, SNAVEL_L, (2.4, 1.5, 0.35)), ('ondersnavel', SNAVEL_HOEK - 15, SNAVEL_L * 0.88, (1.9, 1.25, 0.35))):
        a = math.radians(hoek); dsn = np.array([-math.cos(a), 0, math.sin(a)])
        b0 = basis + np.array([0, 0, 0.9 if naam == 'snavel' else -1.0])
        d.append(('snavel', ('buis', [(tuple(b0), r[0]), (tuple(b0 + dsn * L * 0.55), r[1]), (tuple(b0 + dsn * L), r[2])],
                             (0, 1, 0), 0.85), 0.6, 'kop'))
    a1 = math.radians(SNAVEL_HOEK + 5); a2 = math.radians(SNAVEL_HOEK - 15)
    p1 = (-math.cos(a1) * SNAVEL_L * 0.8, math.sin(a1) * SNAVEL_L * 0.8 + 0.2); p2 = (-math.cos(a2) * SNAVEL_L * 0.66, math.sin(a2) * SNAVEL_L * 0.66 - 0.2)
    d.append(('mond', ('plaat', tuple(basis + np.array([1.0, 0, 0])), (1, 0, 0), (0, 0, 1), [[(0, 1.2), p1, p2, (0, -1.4)]], 1.5, 0.3), 0.3, 'kop'))
    # r4: de rafelige achterkuif (kuif2) vervalt; daar staan nu de oren
    return d

STAP = float(os.environ.get("STAP", 0.3))   # grover (bijv. 0.5) voor snelle proeven
def huid_sdf(dl, kop_draai, kop_kantel, stap=None):
    stap = stap or STAP
    from skimage import measure
    lo = np.array([-40.0, -32.0, -40.0], np.float32); hi = np.array([40.0, 32.0, 44.0], np.float32)
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
    namen = ['lijf', 'vleugel', 'stip', 'staart', 'bliksem', 'creme', 'wang', 'kuifmid', 'snavel', 'koord', 'oor', 'pen', 'mond']
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
            b = ((p[0] + 19.0) / 12.0) ** 2 + ((p[1] + 3.5) / 11.5) ** 2 + ((p[2] + 6.0) / 14.5) ** 2   # r5: grote crème buikovaal (Raichu Gen 1)   # r5: crème borst/buik (meegekanteld)
            idx[j] = 5 if b < 1 else 0
        elif w == 'vleugel': idx[j] = 1                      # voorrand (arm)
        elif w == 'dekveer':
            idx[j] = 1
            if any(np.linalg.norm(p - np.array(c)) < r for c, r in STIPPEN): idx[j] = 2   # ronde lichte stippen
        elif w == 'pen': idx[j] = 11
        elif w == 'staartveer': idx[j] = 11
        elif w == 'staart': idx[j] = 9
        elif w == 'bliksem': idx[j] = 4
        elif w == 'kuif':
            # zwart oor met een binnenvlak in lijfkleur (Gen 3: binnenkant = lijfkleur), alleen op het voorvlak, ingesprongen
            s_ = 1 if q[1] > 0 else -1
            A, B, T, e1, e2, nn = oor_vlak(s_)
            vn = nn if nn[0] < 0 else -nn
            v2 = np.array([((pp - A) @ e1, (pp - A) @ e2) for pp in (A, B, T)]); zw = v2.mean(0) * 0.8 + v2[:2].mean(0) * 0.2
            klein = [tuple(zw + (pp - zw) * 0.45) for pp in v2]
            a_, b_ = np.array([(q - A) @ e1]), np.array([(q - A) @ e2])
            binnen = Nk[j] @ vn > 0.4 and sd_veelhoek(a_, b_, klein)[0] < 0
            idx[j] = 0 if binnen else 10
        elif w == 'kuifkrul': idx[j] = 10
        elif w == 'snavel': idx[j] = 8
        elif w == 'mond': idx[j] = 12
        elif w == 'kop':
            for s in (-1, 1):
                c = np.array([KC.x - 4.2, s * 5.0, KC.z - 3.0])
                r = q - c
                if (r[0] / 2.8) ** 2 + (r[1] / 2.8) ** 2 + (r[2] / 2.4) ** 2 < 1: idx[j] = 6
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
    for s in ((-1, 1) if TWEE_OGEN else (-1,)):      # r7pose: ook het verre oog (Raichu Gen 1, Ho-Oh); r5: alleen het nabije oog: het verre oog stak als bultje uit de omtrek (Gen 3: één oog bij een snavel)
        dd = Vector((-math.cos(az) * math.cos(el), s * math.sin(az) * math.cos(el), math.sin(el)))
        p = KC + Vector((dd.x * KR[0], dd.y * KR[1], dd.z * KR[2])) * 0.97
        o = bol('Oog', p, (1.8, 0.6, 2.1), 'oog', kopas)
        o.rotation_euler = Vector((0, 1, 0)).rotation_difference(Vector((dd.x, dd.y, 0)).normalized()).to_euler()
        bol('Glans', p + Vector((dd.x, dd.y, 0)).normalized() * 0.4 + Vector((-0.5, 0, 0.9)), (0.55, 0.3, 0.65), 'glans', kopas)
    bpy.context.view_layer.update()
    kopas.rotation_euler = kop_matrix(kop_draai, kop_kantel).to_euler()
    romp.rotation_euler = (0, math.radians(-voorover), 0)     # + = voorover (kop omlaag/naar voren)
    # pootjes: kort en stevig, tenen 2 voor 2 achter (specht)
    # r5: grote voeten met klauwen (2 tenen voor, 2 achter: specht), verre poot hoger en verder naar achteren
    for s in (-1, 1):
        o = Vector(VERRE_POOT if s > 0 else (0, 0, 0)); y = s * 4.6
        tenen = [((-6.6, y - 1.4, -23.6), (3.6, 1.2, 1.1)), ((-6.9, y + 1.2, -23.6), (3.8, 1.2, 1.1)),
                 ((1.9, y - 0.9, -23.8), (2.6, 1.1, 1.0)), ((1.6, y + 1.0, -23.8), (2.4, 1.1, 1.0))]
        familie('Poot', [(tuple(Vector(c) + o), r) for c, r in [((-2.0, y, -19.0), (1.9, 1.9, 4.4)), ((-2.2, y, -23.0), (2.6, 2.4, 1.4))] + tenen],
                'poot', wortel)
        klauwen = [((-10.4, y - 1.6, -24.3), (1.3, 0.75, 1.0)), ((-10.9, y + 1.3, -24.3), (1.3, 0.75, 1.0)),
                   ((4.6, y - 1.0, -24.3), (1.1, 0.7, 0.9)), ((4.2, y + 1.1, -24.3), (1.1, 0.7, 0.9))]
        familie('Klauw', [(tuple(Vector(c) + o), r) for c, r in klauwen], 'klauw', wortel, voxel=0.1, glad=1)
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
    global LIJF
    LIJF = float(lijf)
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
