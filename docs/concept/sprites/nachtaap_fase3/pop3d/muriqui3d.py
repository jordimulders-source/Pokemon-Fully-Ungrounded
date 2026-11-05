"""Nachtaap fase 3 (muriqui): 3D-poppetje in pose P1 'zwevend hangen' (Jordi, 3 nov).
Eén lange arm omhoog alsof hij aan een onzichtbare tak hangt (foto 2), de andere reikt naar de kijker
(helend gebaar), benen hangen los, staart krult achter het lijf tot een volle Nazca-spiraal met een
bladbundel in de krul. Kop: muriqui-masker (donker) met de witte sikkel als lichte vachtrand erboven.
Werkwijze: SPRITE_WERKWIJZE stap 1 (poppetje -> raster van hoeken -> Jordi kiest -> silhouet).
Diercoördinaten: x = naar achteren, y = omhoog, z = naar de kijker bij 0° (profiel naar links).
Draaien vanuit de repo-root: python3 docs/concept/sprites/nachtaap_fase3/pop3d/muriqui3d.py"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pop3d as P  # noqa: E402

P.COL = {
    'fur': '#5E4488', 'far': '#45306A', 'head': '#5E4488', 'mask': '#2E2048', 'moon': '#FFFFFF',
    'snuit': '#8C6A9C', 'eye': '#D83C3C', 'pupil': '#1A1020', 'glint': '#FFFFFF',
    'hand': '#5E4488', 'farhand': '#45306A', 'tip': '#EAD8BE', 'fartip': '#B8A48C',
    'hand2': '#5E4488', 'farhand2': '#45306A', 'tip2': '#EAD8BE', 'fartip2': '#B8A48C',
    'blad': '#5E9A4A', 'nerf': '#3C6E34', 'tak': '#8A6A4A', 'bol': '#B9935E',
}
P.NOSHADE = {'mask', 'moon', 'eye', 'pupil', 'glint'}
P.LINED = {'eye', 'snuit', 'blad', 'tak', 'bol', 'hand2', 'farhand2', 'tip2', 'fartip2'}   # *2: om-en-om vingers, lijn ertussen

HEAD_C = np.array((-8.0, 80.0, 0.0))
HEAD_R = 22.0
LIMB = 10.5         # straal bovenarm/dij (sprite: geen stokpoten, ≥ 5 px na verkleinen)
SPIR_R = 24.0
SPIR_YAW = 40.0
FLIP = 160.0        # pose 'omhoog': kanteling van romp en benen om de schouders     # spiraalvlak draait naar de kijker (hoek om de y-as)


def hand(m, wrist, fwd, side, g, gt, curl=0.0, spread=1.0, k_=1.0):
    """Lange apenhand: handpalm + 4 vingers (muriqui: bijna geen duim). fwd = richting van de vingers."""
    fwd = np.array(fwd, float); fwd /= np.linalg.norm(fwd)
    side = np.array(side, float); side /= np.linalg.norm(side)
    up = np.cross(fwd, side)
    pc = wrist + fwd * 6 * k_
    m.ell(pc, 7.5 * k_, g)
    for k in (-1.5, -0.5, 0.5, 1.5):
        b = pc + (fwd * 5 + side * k * 3.4 * spread) * k_
        mid = b + (fwd * 7 + up * (-curl * 4)) * k_
        tip = mid + (fwd * (6 - curl * 3) + up * (-curl * 6)) * k_
        m.chain([(*b, 3.2 * k_), (*mid, 2.8 * k_)], g, 0.8)
        m.chain([(*mid, 2.8 * k_), (*tip, 2.6 * k_)], gt, 0.8)


def open_hand(m, wrist, up, nrm, g, gt, spread=1.0, k_=1.0, duim=False, ln_=1.0, drie=False, greep=0.0, vijf=False, krul=0.0, palm=True):
    """Healergebaar: platte handpalm naar de kijker, lange vingers gespreid omhoog (Mega Alakazam, Mr. Mime)."""
    up = np.array(up, float); up /= np.linalg.norm(up)
    nrm = np.array(nrm, float); nrm -= up * (nrm @ up); nrm /= np.linalg.norm(nrm)
    side = np.cross(up, nrm)
    Rp = np.stack([side, up, nrm], 1)          # lokale assen -> wereld
    pc = wrist + up * 7 * k_
    m.ell(pc, np.array((7.5 if krul else 9.5 if drie else 8, 7.5 if krul else 8.5, 4)) * k_, g, Rp)
    # drie=True (studie referenties/handen_studie.png: Ambipom, Hariyama, Mega Alakazam): brede palm, 3 korte
    # dikke vingers in een waaier, vingers korter dan de palm
    fingers = ((-1.25, 0.9), (0, 1.0), (1.25, 0.9)) if drie else ((-1.6, 0.85), (-0.55, 1.0), (0.55, 1.0), (1.6, 0.85))
    fr = 4.3 if drie else 3.3
    if vijf:   # Mr. Mime/Machamp/Dusknoir (referenties/handen_vijf_vingers.png): 4 dikke vingers TEGEN elkaar, kleine
        # waaier, middelste het langst, + duim dicht bij de palm (Jordi: niet 'gebroken', vingers niet ver uit elkaar)
        fingers = ((-1.5, 0.8), (-0.5, 0.95), (0.5, 1.0), (1.5, 0.85)); fr = 4.2
    for fi, (k, ln) in enumerate(fingers):
        gg, ggt = (g + '2', gt + '2') if (vijf and fi % 2) else (g, gt)
        if krul:   # Drowzee: hand van één kleur; vingers om en om eigen groep voor de lijn ertussen
            gg = ggt = g + '2' if fi % 2 else g
        fd = up + side * k * 0.32 * spread; fd /= np.linalg.norm(fd)
        b = pc + side * k * (4.6 if drie else 3.9 if vijf else 3.6) * k_ + up * 6 * k_
        if vijf:   # gekromde hand: buitenste vingers iets naar achteren -> eigen omlijning, geen gaten
            b = b - nrm * abs(k) * 2.2 * k_
        mid = b + fd * 6 * ln * k_ * ln_
        # greep: tweede kootje krult over een onzichtbare tak, naar achteren (weg van de kijker) en omlaag
        fd2 = fd * (1 - greep) + (-nrm * 0.8 - up * 0.6) * greep; fd2 /= np.linalg.norm(fd2)
        if krul:   # Drowzee: vingers krommen zacht naar de tegenstander (palmkant)
            fd2 = fd * (1 - krul) + (nrm * 0.8 - up * 0.2) * krul; fd2 /= np.linalg.norm(fd2)
        tip = mid + fd2 * 6 * ln * k_ * max(ln_, 0.8 if greep else 0)
        m.chain([(*b, fr * k_), (*mid, (fr - 0.3) * k_)], gg, 0.8)
        m.chain([(*mid, (fr - 0.3) * k_), (*tip, (fr - 0.6) * k_)], ggt, 0.8)
    if duim:   # duim opzij: maakt van de vlakke hand op 1× een leesbare open hand
        td = -side * (0.6 if vijf else 0.85) + up * (0.7 if vijf else 0.5); td /= np.linalg.norm(td)
        b = pc - side * (7 if vijf else 6) * k_ - (nrm * 2 * k_ if vijf else 0)
        if vijf:   # korte ronde duim dicht bij de palm, geen spies
            m.chain([(*b, 3.9 * k_), (*(b + td * 4 * k_), 3.7 * k_), (*(b + td * 7 * k_), 3.4 * k_)], g, 0.8)
        else:
            m.chain([(*b, 3.3 * k_), (*(b + td * 6 * k_), 3.0 * k_), (*(b + td * 11 * k_), 2.7 * k_)], g, 0.8)
    if duim and palm:   # handpalm (licht) naar de kijker
        m.ell(pc + nrm * 2.2 * k_ + (up * 2.5 * k_ if vijf else 0), np.array((6.2, 6.6, 2.4)) * k_, gt, Rp)


def muriqui(head_extra=30, arm='ver_omhoog', blad=True, pose='p1', yaw=40, gebaar='A'):
    m = P.Model()
    # romp: groot buikje onder (muriqui), brede borst en schouders, korte nek; massa zoals Hariyama/Slaking
    if pose != 'krabbel':
        m.ell((-3, 8, 0), (24, 26, 23), 'fur')
        m.ell((0, 36, 0), (21, 22, 23), 'fur')
        m.ell((1, 54, 0), (16, 11, 26), 'fur')        # schouders
        m.chain([(0, 58, 0, 13), (-5, 66, 0, 13)], 'fur')
    view = np.array((-math.sin(math.radians(yaw)), 0, math.cos(math.radians(yaw))))   # richting naar de kijker
    if pose == 'p1':
        # benen: lang en ontspannen (Jordi: "de benen zijn ook te recht", "mogen veel relaxter"): knieën gebogen en
        # uit elkaar, nabije knie hoger naar voren, onderbenen hangen slap, voeten bungelen met de tenen omlaag
        m.chain([(0, -2, 14, LIMB + 2), (-30, -12, 20, LIMB), (-26, -40, 22, LIMB - 2)], 'fur')
        hand(m, np.array((-26.0, -43, 22)), (-0.35, -1, 0.1), (0, 0, 1), 'hand', 'tip', curl=0.9)
        m.chain([(6, -2, -14, LIMB + 2), (-18, -18, -20, LIMB), (-8, -44, -22, LIMB - 2)], 'far')
        hand(m, np.array((-8.0, -47, -22)), (-0.1, -1, -0.1), (0, 0, 1), 'farhand', 'fartip', curl=0.9)
        # armen: heel lang (muriqui), dik genoeg voor de sprite
        up_pts = [(2, 56, -22, LIMB), (14, 84, -32, LIMB - 1.5), (0, 106, -24, LIMB - 2.5)]   # omhoog, elleboog opzij, hangt
        reach = [(-2, 54, 24, LIMB), (-12, 38, 44, LIMB - 1.5), (-26, 26, 60, LIMB - 2.5)]   # reikt naar voren en naar de kijker, open hand
        if arm == 'ver_omhoog':
            m.chain(up_pts, 'far')
            hand(m, np.array(up_pts[-1][:3]), (-0.4, 1, 0), (0, 0, 1), 'farhand', 'fartip', curl=1.0)
            m.chain(reach, 'fur')
            hand(m, np.array(reach[-1][:3]), (-0.6, -0.2, 0.75), (0, 1, 0.2), 'hand', 'tip', curl=0.15, spread=1.15)
        else:   # nabije arm omhoog, verre reikt
            up = [(x, y, -z, r) for x, y, z, r in up_pts]
            rc = [(-2, 54, -24, LIMB), (-28, 44, -26, LIMB - 1.5), (-54, 34, -22, LIMB - 2.5)]
            m.chain(rc, 'far')
            hand(m, np.array(rc[-1][:3]), (-1, -0.1, 0.1), (0, 1, 0), 'farhand', 'fartip', curl=0.15, spread=1.15)
            m.chain(up, 'fur')
            hand(m, np.array(up[-1][:3]), (-0.4, 1, 0), (0, 0, 1), 'hand', 'tip', curl=1.0)
    elif pose == 'lotus':
        # zwevend in kleermakerszit (Mega Alakazam, Meditite): lange benen gekruist, knieën wijd;
        # beide armen opzij omhoog, handpalmen open naar de kijker
        m.chain([(0, -2, 14, LIMB + 2), (-16, -10, 42, LIMB), (-30, -18, -6, LIMB - 2)], 'fur')
        hand(m, np.array((-30.0, -18, -6)), (0, -0.2, -1), (1, 0, 0), 'hand', 'tip', curl=0.5)
        m.chain([(6, -2, -14, LIMB + 2), (-8, -8, -42, LIMB), (-26, -12, 8, LIMB - 2)], 'far')
        hand(m, np.array((-26.0, -12, 8)), (0, -0.2, 1), (1, 0, 0), 'farhand', 'fartip', curl=0.5)
        # nabije hand: palm naar de kijker op borsthoogte, naast (niet voor) het gezicht: het healergebaar
        m.chain([(-2, 54, 24, LIMB), (-6, 32, 44, LIMB - 1.5), (-16, 40, 62, LIMB - 2.5)], 'fur')
        open_hand(m, np.array((-16.0, 42, 62)), (0.0, 1, 0.25), view, 'hand', 'tip')
        # verre hand: laag opzij, palm naar de kijker, vingers schuin omlaag (geeft de genezing af)
        m.chain([(-2, 54, -24, LIMB), (-22, 34, -34, LIMB - 1.5), (-40, 18, -30, LIMB - 2.5)], 'far')
        open_hand(m, np.array((-40.0, 18, -30)), (-0.6, -1, -0.1), view, 'farhand', 'fartip')
    elif pose == 'zweef':
        # zwevend (Deoxys): knieën opgetrokken naar voren, onderbenen slepen naar achteren, tenen omlaag,
        # niets onder het lijf; nabije hand vooruit met de palm naar de kijker (healergebaar),
        # verre arm laag opzij met de palm omlaag (geeft energie af)
        m.chain([(0, -2, 14, LIMB + 2), (-26, -6, 22, LIMB), (-4, -30, 26, LIMB - 2)], 'fur')
        hand(m, np.array((-4.0, -32, 26)), (0.5, -1, 0), (0, 0, 1), 'hand', 'tip', curl=0.1)
        m.chain([(6, -2, -14, LIMB + 2), (-14, -12, -20, LIMB), (10, -32, -22, LIMB - 2)], 'far')
        hand(m, np.array((10.0, -34, -22)), (0.6, -1, 0), (0, 0, 1), 'farhand', 'fartip', curl=0.1)
        # nabije hand: palm naar de kijker op borsthoogte, naast (niet voor) het gezicht: het healergebaar
        m.chain([(-2, 54, 24, LIMB), (-6, 32, 44, LIMB - 1.5), (-16, 40, 62, LIMB - 2.5)], 'fur')
        open_hand(m, np.array((-16.0, 42, 62)), (0.0, 1, 0.25), view, 'hand', 'tip')
        # verre hand: laag opzij, palm naar de kijker, vingers schuin omlaag (geeft de genezing af)
        m.chain([(-2, 54, -24, LIMB), (-22, 34, -34, LIMB - 1.5), (-40, 18, -30, LIMB - 2.5)], 'far')
        open_hand(m, np.array((-40.0, 18, -30)), (-0.6, -1, -0.1), view, 'farhand', 'fartip')
    elif pose == 'vlucht':
        # Jordi: "de benen nog hoger ... alsof die in een soort van vlucht staat zit": knieën hoog opgetrokken
        # tot bij de buik, onderbenen en voeten slepen naar achteren-omlaag; armen als bij 'zweef'
        m.chain([(-2, 2, 14, LIMB + 2), (-30, 16, 22, LIMB), (-10, -6, 26, LIMB - 2)], 'fur')
        hand(m, np.array((-8.0, -8, 26)), (0.7, -1, 0), (0, 0, 1), 'hand', 'tip', curl=0.1)
        m.chain([(6, 0, -14, LIMB + 2), (-20, 10, -20, LIMB), (4, -12, -22, LIMB - 2)], 'far')
        hand(m, np.array((6.0, -14, -22)), (0.8, -1, 0), (0, 0, 1), 'farhand', 'fartip', curl=0.1)
        # nabije hand: palm naar de kijker op borsthoogte, naast (niet voor) het gezicht: het healergebaar
        m.chain([(-2, 54, 24, LIMB), (-6, 32, 44, LIMB - 1.5), (-16, 40, 62, LIMB - 2.5)], 'fur')
        open_hand(m, np.array((-16.0, 42, 62)), (0.0, 1, 0.25), view, 'hand', 'tip')
        # verre hand: laag opzij, palm naar de kijker, vingers schuin omlaag (geeft de genezing af)
        m.chain([(-2, 54, -24, LIMB), (-22, 34, -34, LIMB - 1.5), (-40, 18, -30, LIMB - 2.5)], 'far')
        open_hand(m, np.array((-40.0, 18, -30)), (-0.6, -1, -0.1), view, 'farhand', 'fartip')
    elif pose == 'omhoog':
        # Jordi (foto 2): hangt met de benen omhoog aan een onzichtbare tak (lore: kanaliseert planten en takken
        # met psychische kracht), lijf hangt eronder, kop onderaan kijkt rechtop, armen vrij.
        # Gebouwd als 'staand' en daarna om de schouders gekanteld (zie FLIP hieronder).
        m.chain([(0, -2, 14, LIMB + 2), (-20, -26, 20, LIMB), (-8, -54, 24, LIMB - 2)], 'fur')
        hand(m, np.array((-8.0, -57, 24)), (-0.3, -1, 0), (0, 0, 1), 'hand', 'tip', curl=1.0)
        m.chain([(6, -2, -14, LIMB + 2), (12, -30, -20, LIMB), (2, -58, -22, LIMB - 2)], 'far')
        hand(m, np.array((2.0, -61, -22)), (-0.3, -1, 0), (0, 0, 1), 'farhand', 'fartip', curl=1.0)
    elif pose == 'krabbel':
        # Jordi's krabbel (referenties/jordi_krabbel_pose.png): lijf horizontaal in de lucht, kop vooraan links;
        # verre arm omhoog-voor en één been recht omhoog uit de rug houden elk een (psychische) tak vast
        # (Jordi: "misschien dat 1 arm en 1 been takken vasthouden"); nabije arm reikt omlaag-voor met een
        # kiemend bolletje; ander been sleept naar achteren-omlaag; staart krult rechtsboven tot spiraal.
        # Studie referenties/dynamische_poses.png (Zeraora, Infernape, Mew, Celebi, Ambipom, Primeape): compact,
        # ledematen gebogen en dicht bij het lijf, grote handen/voeten, kop groot op de schouders, taps (dikke dij/
        # bovenarm, knie/elleboog zichtbaar). Geen zeester.
        m.ell((-12, 2, 0), (22, 22, 24), 'fur')             # borst/schouders
        m.ell((14, 4, 0), (24, 22, 22), 'fur')              # buik/rug (bolt boven uit, krabbel)
        m.ell((32, 0, 0), (17, 18, 19), 'fur')              # heup
        # verre arm omhoog-voor, elleboog gebogen, hand gekruld om een onzichtbare tak
        m.chain([(-16, 14, -20, LIMB + 1.5), (-24, 34, -26, LIMB - 0.5), (-40, 46, -24, LIMB - 3)], 'far')
        open_hand(m, np.array((-40.0, 46, -24)), (-0.55, 1, 0), view, 'farhand', 'fartip', spread=0.3, k_=1.4, duim=True, ln_=0.75, vijf=True, greep=0.95)   # vuist om de tak (Machamp)   # grijpende hand, vingers zichtbaar (Jordi)
        # nabije arm (schets): van onder de nek schuin naar linksonder, elleboog gebogen; hand plat, vingers
        # gespreid, palm omlaag-voor naar het doel (anime-still, één hand)
        m.chain([(-18, -8, 20, LIMB + 1.5), (-28, -36, 26, LIMB - 0.5), (-50, -60, 26, LIMB - 3)], 'fur')
        # leesbaarheid (Simipour, Ambipom): hand plat naar de kijker, vingers wijd, groot
        # Jordi's handkrabbel (referenties/jordi_krabbel_hand.png): pols knikt naar achteren, vingers OMHOOG, duim
        # links, palm naar de tegenstander (= de kijker): het stop-/healgebaar onder de kop
        if gebaar != 'geen':
          open_hand(m, np.array((-52.0, -62, 28)), (-0.15, 1, 0.1), view, 'hand', 'tip',
                  spread=0.4, k_=1.3, duim=True, ln_=1.3, vijf=True, krul=0.4, palm=False)   # Gen 1-Drowzee (Jordi): 4 vingers + duim, zacht gekromd
        # verre been omhoog, knie gebogen naar voren, voet gekruld om een onzichtbare tak
        m.chain([(18, 14, -14, LIMB + 4), (12, 40, -18, LIMB), (24, 58, -20, LIMB - 3)], 'far')
        hand(m, np.array((24.0, 58, -20)), (0.3, 1, 0), (0, 0, 1), 'farhand', 'fartip', curl=1.0, k_=1.4)
        # nabije been sleept naar achteren-omlaag, knie gebogen, voet ontspannen
        m.chain([(36, -6, 14, LIMB + 4), (52, -24, 18, LIMB), (70, -22, 20, LIMB - 3)], 'fur')
        hand(m, np.array((70.0, -22, 20)), (1, -0.5, 0), (0, 0, 1), 'hand', 'tip', curl=0.5, k_=1.4)
    n_lijf = len(m.parts)
    # staart: vanaf de stuit naar achteren en omhoog, dan een volle spiraal (2 slagen) achter het lijf
    ph = math.radians(SPIR_YAW)
    e1 = np.array((math.cos(ph), 0, math.sin(ph)))         # 'naar achteren' in het spiraalvlak
    path = [tuple(p) for p in P.qb(np.array((18, 0, 0)), np.array((18, -14, 0)) + 34 * e1, np.array((0, 22, 0)) + 46 * e1, 9)]
    c = np.array((0, 22.0, 0)) + (46 + SPIR_R) * e1
    spir = []
    nrm = np.cross(e1, (0, 1, 0))
    if nrm[2] < 0:
        nrm = -nrm
    for i in range(70):
        t = i / 69
        a = math.pi - t * 1.6 * 2 * math.pi
        rr = SPIR_R * (1 - 0.78 * t)
        # binnenste slag iets naar de kijker (helix), zodat de windingen een eigen omlijning krijgen
        spir.append(tuple(c + rr * math.cos(a) * e1 + np.array((0, rr * math.sin(a), 0)) + nrm * 7 * t))
    pts = path[:-1] + spir
    n = len(pts)
    m.chain([(x, y, z, 7.5 - 4.0 * i / (n - 1)) for i, (x, y, z) in enumerate(pts)], 'fur')
    if blad:   # bundel van 3 grote bladeren in de krul, waaier naar boven-achter
        # bladeren steken uit de krul naar boven-achter, voorbij de buitenste slag (anders lezen ze niet)
        cc = np.array(spir[-1])
        for ang, ln in ((50, 1.0), (82, 1.15), (114, 0.95)):
            a = math.radians(ang)
            d = math.cos(a) * e1 + np.array((0, math.sin(a), 0))
            Rb = P.rot_y(-ph) @ P.rot_z(a)
            m.ell(cc + d * 20 * ln + nrm * 3, (17 * ln, 6, 2.5), 'blad', Rb)
    off = np.zeros(3)
    if pose == 'krabbel':
        T = np.array((28.0, 6, 0))          # staart vanaf de heup, spiraal rechtsboven
        m.parts = m.parts[:n_lijf] + [(c + T, r, R0, g) for c, r, R0, g in m.parts[n_lijf:]]
        off = np.array((-42.0, -74.0, 0.0))  # kop direct op de schouders
    if pose == 'omhoog':
        # FLIP: alles tot nu toe (romp, benen, staart) draait om de schouders: heupen en benen omhoog
        piv, Rz = np.array((0.0, 54.0, 0.0)), P.rot_z(math.radians(FLIP))
        fl = lambda c: piv + Rz @ (c - piv)
        T = fl(np.array((16.0, 2, 0))) - np.array((16.0, 2, 0))   # staart gaat mee met de heup, kantelt niet
        m.parts = [(fl(c), r, Rz @ R0, g) for c, r, R0, g in m.parts[:n_lijf]] + \
                  [(c + T, r, R0, g) for c, r, R0, g in m.parts[n_lijf:]]
        # nabije hand: palm naar de kijker naast de kop (healergebaar); verre arm reikt opzij-omlaag (foto 2)
        m.chain([(-2, 54, 24, LIMB), (-6, 34, 44, LIMB - 1.5), (-16, 44, 62, LIMB - 2.5)], 'fur')
        open_hand(m, np.array((-16.0, 46, 62)), (0.0, 1, 0.25), view, 'hand', 'tip')
        m.chain([(-2, 54, -24, LIMB), (-24, 36, -32, LIMB - 1.5), (-46, 26, -28, LIMB - 2.5)], 'far')
        open_hand(m, np.array((-46.0, 26, -28)), (-1, 0.3, 0), view, 'farhand', 'fartip')
        off = np.array((-2.0, -50.0, 0.0))     # kop onder de schouders
    # kop: rond, iets voor de borst, draait extra naar de kijker rond de nek
    pv = np.array((-4.0, 62.0, 0.0))
    Rh = P.rot_y(math.radians(head_extra))
    Hp = lambda p: pv + Rh @ (np.array(p, float) - pv) + off
    m.ell(Hp(HEAD_C), (HEAD_R, HEAD_R * 1.02, HEAD_R * 0.98), 'head', Rh)
    m.ell(Hp(HEAD_C + np.array((-HEAD_R * 0.80, -HEAD_R * 0.42, 0))), (7, 7.5, 10), 'snuit', Rh)   # brede snuit
    eyes = []
    for sz in (1, -1):
        d = np.array((-0.88, 0.14, 0.40 * sz)); d /= np.linalg.norm(d)
        e = HEAD_C + d * HEAD_R * 0.94
        eyes.append(e)
        m.ell(Hp(e), 3.9, 'eye')
        m.ell(Hp(e + d * 1.6), 2.4, 'pupil')
        m.ell(Hp(e + d * 2.8 + np.array((0, 1.3, -0.6 * sz))), 0.9, 'glint')

    def texfn(q, groups):
        ql = (q - off - pv) @ Rh + pv
        u = (ql - HEAD_C) / HEAD_R
        un = u / (np.linalg.norm(u, axis=1, keepdims=True) + 1e-9)
        cap = lambda lat_c, r: np.degrees(np.arccos(np.clip(un @ np.array(
            (-math.cos(math.radians(lat_c)), math.sin(math.radians(lat_c)), 0)), -1, 1))) < r
        lon = np.degrees(np.arctan2(u[:, 2], -u[:, 0]))
        g = np.full(len(q), groups.index('head'))
        mask = cap(-14.0, 52.0)                      # kaal donker gezicht (foto 1/4)
        g[mask] = groups.index('mask')
        # witte sikkel = lichte vachtrand boven het masker (foto 1), punten omlaag langs de wangen
        g[cap(16.0, 70.0) & ~mask & ~cap(-30.0, 50.0) & (np.abs(lon) < 100) & (u[:, 1] > -0.55)] = groups.index('moon')
        return g

    m.texfn = texfn
    return m


def grid(yaws=(30, 40, 50), extras=(20, 35), pitch=6, arm='ver_omhoog', name='hoeken.png', titel='', rows=None):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
    W = 10 + 266 * len(yaws)
    im = Image.new('RGB', (W, 40 + (256 + 26) * len(extras)), 'white')
    d = ImageDraw.Draw(im)
    d.text((10, 10), titel or f'Nachtaap fase 3 (muriqui), pose P1 zwevend hangen, {arm.replace("_", " ")}',
           font=FB, fill=(30, 30, 30))
    rows = rows or [(ex, arm) for ex in extras]
    im = Image.new('RGB', (W, 40 + (256 + 26) * len(rows)), 'white')
    d = ImageDraw.Draw(im)
    d.text((10, 10), titel or 'Nachtaap fase 3 (muriqui), pose P1 zwevend hangen', font=FB, fill=(30, 30, 30))
    for j, (ex, arm) in enumerate(rows):
        for i, yaw in enumerate(yaws):
            v = P.view(muriqui(ex, arm), yaw, pitch, size=220)
            x, y = 10 + 266 * i, 40 + (256 + 26) * j
            # zweefschaduw: ±7/64 van de spritehoogte onder het laagste punt (Mega Alakazam/Dusknoir)
            a = np.array(v.convert('L')) < 250
            ys = np.where(a.any(1))[0]
            gy = min(255, ys.max() + 22)
            xs = np.where(a.any(0))[0]
            cx = (xs.min() + xs.max()) // 2
            dd = ImageDraw.Draw(v)
            dd.ellipse((cx - 40, gy - 5, cx + 40, gy + 5), fill=(205, 205, 212))
            im.paste(v, (x, y))
            lab = 'verre arm omhoog' if arm == 'ver_omhoog' else 'nabije arm omhoog'
            d.text((x, y + 258), f'lijf {yaw}°, kop {yaw + ex}°, {lab}', font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, name))


def raster(name='pose_40_80_hand.png'):
    """Jordi 3 nov: P1 'lijkt gewoon alsof die staat' -> vier zweefposes; elk label noemt pose en hoeken."""
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
    cells = [('krabbel', 40, 40, 'A'), ('krabbel', 40, 40, 'B')]
    naam = {'krabbel': 'krabbel Jordi', 'omhoog': 'benen omhoog', 'lotus': 'kleermakerszit', 'zweef': 'zweven', 'vlucht': 'in vlucht'}
    im = Image.new('RGB', (10 + 330 * 3, 40 + (256 + 26) * ((len(cells) + 2) // 3)), 'white')
    d = ImageDraw.Draw(im)
    d.text((10, 10), 'Nachtaap fase 3: pose krabbel, lijf 40° / kop 80°, geen takken', font=FB, fill=(30, 30, 30))
    for k, (pose, yaw, ex, gb) in enumerate(cells):
        v = P.view(muriqui(ex, pose=pose, yaw=yaw, gebaar=gb), yaw, 6, size=220)
        a = np.array(v.convert('L')) < 250
        ys = np.where(a.any(1))[0]; xs = np.where(a.any(0))[0]
        gy = min(253, ys.max() + 18); cx = (xs.min() + xs.max()) // 2
        ImageDraw.Draw(v).ellipse((cx - 40, gy - 4, cx + 40, gy + 4), fill=(205, 205, 212))
        x, y = 10 + 330 * (k % 3), 40 + (256 + 26) * (k // 3)
        im.paste(v, (x, y))
        d.text((x, y + 258), f'lijf {yaw}°, kop {yaw + ex}°, hand {gb}: ' + ('vingers gespreid' if gb == 'A' else 'vingers wijd gespreid'), font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, name))


if __name__ == '__main__':
    raster()
