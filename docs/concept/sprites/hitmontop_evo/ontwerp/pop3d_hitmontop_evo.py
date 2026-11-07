"""Hitmontop-evolutie (capoeira, Fighting/Ground): 3D-poppetje voor pose, verhoudingen en kenmerken.
Zelfde aanpak als de lama (lama/ontwerp/pop3d_lama.py); renderer = olinguito_v2/silhouet_kolibriemethode/pop3d.py
(via de render/shade/view van pop3d_lama, met ons eigen kleurenschema).

Pose = referenties/pose_eenhandsstand.webp, horizontaal gespiegeld (kop links): eenarmige handstand, lijf horizontaal
met de borst naar de kijker, benen in een brede V-split omhoog, vrije arm gebogen over de heup, cordão hangt omlaag.
Coördinaten worden geschreven als pixels in de GESPIEGELDE foto (1580 breed; x rechts, y omlaag) plus een diepte z
(photo-px, + = naar de kijker) en omgezet met W(). Bij yaw = YAW_FOTO kijk je precies zoals de foto.
Familiekenmerken en kleuren: graphics/pokemon/hitmontop/anim_front.png + normal.pal.
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/ontwerp/pop3d_hitmontop_evo.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../lama/ontwerp'))
sys.path.insert(0, os.path.join(HERE, '../../olinguito_v2/silhouet_kolibriemethode'))
import pop3d as P
import pop3d_lama as L
ROOT = os.path.join(HERE, '../../../../..')

# Hitmontop normal.pal: huid 222,189,131 / licht 255,222,156 / donker 180,139,90 / 131,90,41; blauw 139,189,238 / 98,156,222 / 74,115,197;
# grijs 205,205,205 / 148,148,156; rood 197,74,49 (koordjes: kleur nog open in de SPEC)
COL = {
    'skin': '#DEBD83', 'arm2': '#DEBD83', 'head': '#DEBD83', 'ankle': '#DEBD83',
    'hand': '#FFDE9C', 'hand2': '#FFDE9C', 'horn': '#FFDE9C',
    'hair': '#835A29', 'hair2': '#835A29', 'dread': '#835A29', 'dread2': '#835A29', 'hairband': '#C54A31',
    'brow': '#B48B5A', 'eye': '#101010', 'glint': '#FFFFFF',
    'pants': '#629CDE', 'leg1': '#629CDE', 'leg2': '#629CDE', 'cuff': '#4A73C5',
    'foot': '#8BBDEE', 'foot2': '#8BBDEE', 'claw': '#CDCDCD',
    'cord': '#C54A31', 'cordknot': '#C54A31', 'band': '#C54A31', 'band2': '#C54A31',
}
NOSHADE = {'eye', 'glint'}
LINED = {'arm2', 'hand', 'hand2', 'head', 'hair', 'hair2', 'dread', 'dread2', 'hairband', 'horn', 'brow', 'eye', 'leg1', 'leg2', 'cuff',
         'foot', 'foot2', 'claw', 'cord', 'cordknot', 'band', 'band2', 'ankle'}
L.COL.clear(); L.COL.update(COL)
L.NOSHADE.clear(); L.NOSHADE.update(NOSHADE)
L.LINED.clear(); L.LINED.update(LINED)
L.LINE = np.array((30, 22, 18), np.uint8)

YAW_FOTO = 70          # de foto zelf: borst bijna recht naar de kijker
LIMB_K = 1.15          # ledematen/romp iets voller dan de foto (Pokémon-massa, leesbaar op 64 px)
HEAD_K = 1.0           # extra kopschaal (1.0 = de Pokémon-kop hieronder, ±2,3x de fotokop)


def W(x, y, z=0.0):
    """Gespiegelde-fotopixel -> wereldcoördinaat (x rechts, y omhoog, z naar de kijker), 10 px = 1 eenheid."""
    return np.array(((x - 800) / 10.0, -(y - 900) / 10.0, z / 10.0))


def tube(m, pts, g, step=1.2):
    """Doorlopende getaperde buis langs (x, y, z, straal) in foto-px (catmull-rom, dus geen knikken)."""
    p = [np.array(q, float) for q in pts]
    if len(p) > 2:
        q = [p[0]] + p + [p[-1]]
        dense = []
        for i in range(1, len(q) - 2):
            p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
            for t in np.linspace(0, 1, 8, endpoint=False):
                dense.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
        dense.append(p[-1])
        p = dense
    k = LIMB_K if g in ('skin', 'arm2', 'leg1', 'leg2', 'ankle') else 1.0
    m.chain([tuple(W(*a[:3])) + (a[3] * k / 10.0,) for a in p], g, step)


def ball(m, c, r, g, R0=None):
    rr = np.array(r if np.ndim(r) else (r, r, r), float) / 10.0
    m.ell(W(*c), rr, g, R0)


def axis_rot(ax):
    """Rotatie die de y-as op richting ax legt."""
    ax = np.array(ax, float); ax /= np.linalg.norm(ax)
    yv = np.array((0, 1.0, 0)); v = np.cross(yv, ax)
    if np.linalg.norm(v) < 1e-6:
        return np.eye(3)
    v /= np.linalg.norm(v); ang = math.acos(np.clip(yv @ ax, -1, 1))
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * K @ K


def ring(m, a, b, t, rr, g, dik=16):
    """Band om een ledemaat: platte schijf loodrecht op de as a->b (foto-px), op fractie t."""
    a, b = np.array(a, float), np.array(b, float)
    c = a + (b - a) * t
    ax = W(*b) - W(*a)
    m.ell(W(*c), np.array((rr, dik, rr)) / 10.0, g, axis_rot(ax))
    return c


def staart(m, c, pts, g, r0=20, r1=14):
    """Hangend koordje vanaf c (foto-px), punten relatief; eindigt in een klein knopje."""
    n = len(pts)
    q = [(c[0], c[1], c[2], r0)] + [(c[0] + dx, c[1] + dy, c[2] + dz, r0 + (r1 - r0) * (i + 1) / n) for i, (dx, dy, dz) in enumerate(pts)]
    tube(m, q, g)
    e = q[-1]
    ball(m, e[:3], r1 * 1.35, 'cordknot')


def voet(m, ankle, toe, g, up, k=1.0):
    """Hitmontop-voet: blauwe ronde voet met drie grijze klauwen aan de punt (kleiner dan bij Hitmontop t.o.v. het been)."""
    a, t = np.array(ankle, float), np.array(toe, float)
    d = t - a; L_ = np.linalg.norm(d); d /= L_
    c = a + d * L_ * 0.45
    R0 = axis_rot(W(*t) - W(*a))
    m.ell(W(*c), np.array((48, L_ * 0.62, 44)) * k / 10.0, g, R0)
    up = np.array(up, float); up /= np.linalg.norm(up)
    side = np.cross(np.append(d[:2], 0) if len(d) == 3 else d, np.array((0, 0, 1.0)))
    side = side / (np.linalg.norm(side) + 1e-9)
    for j, s in enumerate((-1, 0, 1)):   # drie klauwen, licht gespreid, de middelste het langst
        b = t - d * 18 + side * s * 26 + np.array((0, 0, 14 * (1 - abs(s)) - 4))
        e = b + d * (70 if s == 0 else 56) + side * s * 22
        tube(m, [(*b, 22), (*((b + e) / 2), 16), (*e, 5)], 'claw', 0.6)


def hitmontop_evo(head_k=HEAD_K, dreads=True):
    m = P.Model()
    # --- romp: lijf ligt horizontaal, heup rechts (hoogste punt), schouders links-onder; borst naar de kijker.
    # langer dan Hitmontop (SPEC): heup -> borst -> schouders als één getaperde buis
    tube(m, [(835, 800, 6, 86), (760, 870, 10, 108), (680, 950, 8, 112), (630, 1010, 0, 96)], 'skin')
    ball(m, (640, 1060, 0), 52, 'skin')                 # schouder steunarm
    ball(m, (700, 735, 10), 50, 'skin')                 # schouder vrije arm (bovenkant)
    tube(m, [(640, 960, 0, 62), (585, 905, -5, 58)], 'skin')   # hals naar de kop
    # --- broek: heup/zitvlak, aansluitend
    ball(m, (895, 700, 0), (118, 104, 100), 'pants', P.rot_z(math.radians(38)))
    # cordão om de taille + knoop vooraan + twee hangende einden (zwaartekracht = omlaag)
    for th in np.arange(0, 360, 12):
        tr = math.radians(th)
        c = np.array((858, 778, 0.0)) + np.array((math.cos(tr) * 0.78, math.cos(tr) * 0.62, math.sin(tr))) * 96
        ball(m, tuple(c), 19, 'cord')
    knot = (900, 770, 92)
    ball(m, knot, 30, 'cordknot')
    staart(m, knot, [(4, 60, 6), (0, 120, 4), (-8, 175, 0)], 'cord', 20, 15)
    staart(m, knot, [(30, 55, -6), (62, 110, -14), (80, 160, -20)], 'cord', 20, 15)
    # --- benen: lange aansluitende broek, V-split; enkel even bruin (Hitmontop-been), daarna de blauwe voet
    # nabije been (naar linksboven, foto: gebogen voet) en verre been (naar rechtsboven, gestrekte voet)
    tube(m, [(860, 650, 30, 78), (720, 565, 32, 64), (560, 470, 30, 52), (400, 375, 26, 44), (312, 322, 24, 38)], 'leg1')
    ring(m, (400, 375, 26), (300, 315, 24), 0.85, 50, 'cuff', 14)
    tube(m, [(300, 315, 24, 30), (262, 292, 24, 27)], 'ankle')
    voet(m, (262, 292, 24), (180, 395, 30), 'foot', (-1, 0, 0))        # geflexed: tenen naar beneden/links
    tube(m, [(920, 640, -30, 74), (1010, 575, -32, 62), (1110, 500, -32, 50), (1200, 432, -30, 42), (1250, 395, -30, 36)], 'leg2')
    ring(m, (1200, 432, -30), (1258, 388, -30), 0.85, 48, 'cuff', 14)
    tube(m, [(1255, 390, -30, 29), (1275, 360, -30, 26)], 'ankle')
    voet(m, (1275, 360, -30), (1322, 222, -30), 'foot2', (1, 0, 0))   # gestrekt: punt doorlopend omhoog
    # --- steunarm: recht en verticaal, ronde hand plat op de grond (grondlijn = onderkant hand)
    tube(m, [(640, 1060, 0, 44), (632, 1180, 0, 40), (615, 1300, 0, 36), (592, 1405, 0, 33)], 'skin')
    ball(m, (578, 1458, 8), (66, 60, 62), 'hand')
    c = ring(m, (640, 1080, 0), (615, 1300, 0), 0.22, 50, 'band', 15)       # prajiad steunarm
    staart(m, (c[0] - 30, c[1] + 6, 30), [(-14, 50, 10), (-22, 100, 14)], 'band', 15, 11)
    # --- vrije arm: schouder bovenaan -> elleboog boven de heup -> onderarm omlaag over de heup, ronde hand
    tube(m, [(700, 735, 30, 42), (770, 690, 70, 40), (835, 668, 95, 37), (858, 760, 115, 34), (852, 860, 125, 31)], 'arm2')
    ball(m, (842, 918, 135), 56, 'hand2')
    c = ring(m, (700, 735, 30), (835, 668, 95), 0.45, 46, 'band2', 15)      # prajiad vrije arm
    staart(m, (c[0], c[1] + 30, c[2] + 20), [(-4, 50, 6), (-14, 100, 10)], 'band2', 15, 11)
    # --- kop: Pokémon-kop (±2,3x de fotokop), gekanteld zoals op de foto (kruin naar linksboven), gezicht naar de kijker
    hk = head_k
    H = np.array((470.0, 845.0, 25.0))
    rs = np.array((128, 136, 120)) * hk
    Rh = P.rot_z(math.radians(28))          # kanteling: kruin naar linksboven
    hl = lambda v: H + Rh @ (np.array(v, float))   # kop-lokaal (x rechts, y kruin, z gezicht) -> foto-px (y omlaag!)
    # let op: foto-y loopt omlaag; kop-lokaal y omhoog -> omzetten
    def HL(v):
        v = np.array(v, float)
        q = Rh @ np.array((v[0], v[1], v[2]))
        return np.array((H[0] + q[0], H[1] - q[1], H[2] + q[2]))
    ball(m, tuple(HL((0, 0, 0))), rs, 'head', Rh)
    ball(m, tuple(HL((0, -70 * hk, 18 * hk))), np.array((92, 70, 92)) * hk, 'head', Rh)   # kaak/kin, iets breder (Hitmontop-kop is breed)
    # Hitmontop-ogen: groot, zwart, zwaar lid erboven; licht schuin (boos); glans linksboven
    for sx in (-1, 1):
        d = np.array((0.40 * sx, 0.02, 0.92)); d /= np.linalg.norm(d)
        e = HL(d * rs * 0.97)
        Re = Rh @ P.rot_z(math.radians(-14 * sx))
        ball(m, tuple(e), np.array((27, 31, 16)) * hk, 'eye', Re)
        ball(m, tuple(e + np.array((-9, -10, 14)) * hk), 7 * hk, 'glint')
        b = HL(np.array((0.40 * sx, 0.30, 0.90)) * rs * 0.97)
        ball(m, tuple(b), np.array((40, 11, 18)) * hk, 'brow', Re)
    # haar: afro-Braziliaans, Eddy Gordo: locs naar achteren gebonden (voorhoofd vrij), dikke bundel dreads uit een band
    # achter op de kruin. Locs om en om in twee groepen (zelfde kleur) zodat elke loc een eigen lijn krijgt.
    gold = (1 + 5 ** 0.5) / 2
    N = 90
    for i in range(N):
        yv = 1 - 2 * (i + 0.5) / N; rr = math.sqrt(1 - yv * yv); th = 2 * math.pi * i / gold
        d = np.array((math.cos(th) * rr, yv, math.sin(th) * rr))
        face = d[2] > 0.15 and d[1] < 0.62
        if d[1] < -0.05 or face:
            continue
        ball(m, tuple(HL(d * rs * 0.98)), np.array((44, 44, 44)) * hk, 'hair' if i % 2 else 'hair2')
    # kleine hoorn (niet meer functioneel): kort kegeltje midden op de kruin, steekt net boven de locs uit
    hb = HL(np.array((0.0, 1.0, 0.18)) * rs)
    ht = HL(np.array((0.0, 1.0, 0.18)) * rs + np.array((-4, 72, 14)) * hk)
    tube(m, [(*hb, 30 * hk), (*((hb + ht) / 2), 20 * hk), (*ht, 7 * hk)], 'horn', 0.6)
    if dreads:
        tie = HL(np.array((-0.55, 0.62, -0.50)) * rs * 1.08)
        ball(m, tuple(tie), 40 * hk, 'hairband')
        # bundel: 4 dikke dreads, eerst naar achteren-links uit de band, dan door de zwaartekracht omlaag; taps, ongelijk
        for j, (dx, dz, ln) in enumerate(((-70, -20, 230), (-30, -50, 270), (-105, 5, 190), (-5, -75, 210))):
            a = np.array(tie, float)
            pts = [(*a, 34)]
            for t in (0.2, 0.45, 0.75, 1.0):
                pts.append((a[0] + dx * min(1, t * 2.2), a[1] - 30 * math.sin(math.pi * min(1, t * 1.6)) + ln * t * t, a[2] + dz * t, 36 - 16 * t))
            tube(m, pts, 'dread' if j % 2 else 'dread2')
    # pre-rotatie: bij yaw = YAW_FOTO staat het poppetje exact zoals de foto
    Rp = P.rot_y(math.radians(-YAW_FOTO))
    m.parts[:] = [(Rp @ c, r, Rp @ R0, g) for c, r, R0, g in m.parts]
    return m


def render_foto(m, out=768):
    """Render op dezelfde schaal en positie als de gespiegelde foto (768 px), voor de overlay."""
    sc = L.R / 1580.0 * 10.0
    cx, cy = (L.R / 2 / (L.R / 1580.0) - 800) / 10.0, -(L.R / 2 / (L.R / 1580.0) - 900) / 10.0
    img, a = L.shade(*L.render(m, YAW_FOTO, 0, sc, (cx, cy)), out=out)
    return img, a


def frame64(m, yaw, pitch=6):
    """Verklein naar een 64x64-frame: figuur ±58 px hoog, hand op de grondlijn (rij 62)."""
    img, a = L.view(m, yaw, pitch, size=232)
    s = img.resize((64, 64), Image.LANCZOS)
    return s


def vel():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    m = hitmontop_evo()
    foto = Image.open(os.path.join(HERE, '../referenties/pose_eenhandsstand.webp')).convert('RGB').crop((0, 0, 1580, 1580))
    foto = foto.transpose(Image.FLIP_LEFT_RIGHT)
    cell = 262
    im = Image.new('RGB', (12 + cell * 5, 44 + (cell + 30) * 3), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), 'Hitmontop-evolutie, poppetje ronde 1: pose van de foto (gespiegeld), Hitmontop-kenmerken volgens de SPEC', font=FB, fill=(30, 30, 30))

    def tegel(img, i, rij, lab):
        x, y = 12 + cell * i, 44 + rij * (cell + 30)
        im.paste(img, (x + (256 - img.width) // 2, y + (256 - img.height) // 2)); d.text((x + 4, y + 260), lab, font=F, fill=(60, 60, 60))
    yaws = (70, 55, 40)
    for i, yaw in enumerate(yaws):
        img, _ = L.view(m, yaw, 6)
        lab = {70: 'A70: zoals de foto', 55: 'B55: 15° meer naar links', 40: 'C40: 30° meer naar links'}[yaw]
        tegel(img, i, 0, lab)
    # foto en overlay (rode omtrek van het poppetje over de foto, zelfde schaal)
    f256 = foto.resize((256, 256), Image.LANCZOS)
    tegel(f256, 3, 0, 'foto, gespiegeld (bron pose)')
    big, a = render_foto(m)
    ov = foto.resize((768, 768), Image.LANCZOS)
    ova = np.asarray(ov).copy()
    aa = a
    rand = aa & ~(np.roll(aa, 1, 0) & np.roll(aa, -1, 0) & np.roll(aa, 1, 1) & np.roll(aa, -1, 1))
    for _ in range(2):
        rand = rand | np.roll(rand, 1, 0) | np.roll(rand, 1, 1)
    ova[rand] = (220, 30, 30)
    tegel(Image.fromarray(ova).resize((256, 256), Image.LANCZOS), 4, 0, 'A70 als rode omtrek over de foto')
    # rij 2: uitsneden (kop, voeten) op A70 en B55
    for i, yaw in enumerate((70, 55)):
        big, _ = L.view(m, yaw, 6, size=236)
        big = big.resize((768, 768), Image.LANCZOS)
        Image.Image.save(big, os.path.join(HERE, f'pop_{yaw}.png'))
        # zoek de kop: bovenste-linker kwadrant van het lijf
        tegel(big.crop((90, 220, 346, 476)), i * 2, 1, f'{"A70" if yaw == 70 else "B55"}: kop, haar, hoorn')
        tegel(big.crop((20, 30, 276, 286)), i * 2 + 1, 1, f'{"A70" if yaw == 70 else "B55"}: voet linksboven')
    ht = Image.open(os.path.join(ROOT, 'graphics/pokemon/hitmontop/anim_front.png')).convert('RGBA').crop((0, 0, 64, 64)).resize((256, 256), Image.NEAREST)
    bg = Image.new('RGBA', ht.size, (255, 255, 255, 255)); bg.alpha_composite(ht); tegel(bg.convert('RGB'), 4, 1, 'Hitmontop (4x), de pre-evolutie')
    # rij 3: op 64 px (ruwe verkleining), plus Hitmontop op 1x ernaast
    for i, yaw in enumerate(yaws):
        s = frame64(m, yaw)
        s.save(os.path.join(HERE, f'pop_{yaw}_64.png'))
        tegel(s.resize((256, 256), Image.NEAREST), i, 2, f'{ {70: "A70", 55: "B55", 40: "C40"}[yaw]} op 64 px (ruw, 4x)')
    een = Image.new('RGB', (256, 256), 'white')
    for i, yaw in enumerate(yaws):
        een.paste(frame64(m, yaw), (4 + 84 * i, 20))
    h1 = Image.open(os.path.join(ROOT, 'graphics/pokemon/hitmontop/anim_front.png')).convert('RGBA').crop((0, 0, 64, 64))
    t = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); t.alpha_composite(h1)
    een.paste(t.convert('RGB'), (96, 150))
    ImageDraw.Draw(een).text((4, 4), 'A70  B55  C40 op 1x', font=F, fill=(60, 60, 60))
    ImageDraw.Draw(een).text((4, 170), 'Hitmontop 1x', font=F, fill=(60, 60, 60))
    tegel(een, 3, 2, '1x naast Hitmontop')
    # Hitmontop op 8x apart (formaat zoals gevraagd)
    h8 = Image.new('RGBA', (512, 512), (255, 255, 255, 255)); h8.alpha_composite(h1.resize((512, 512), Image.NEAREST))
    im.save(os.path.join(HERE, 'vel_pop_ronde1.png'))
    # tweede vel: groot, B55 op 8x naast de gespiegelde foto en Hitmontop 8x
    big, _ = L.view(m, 55, 6, size=232); big = big.resize((512, 512), Image.LANCZOS)
    v2 = Image.new('RGB', (12 + 524 * 3, 560), 'white'); d2 = ImageDraw.Draw(v2)
    for i, (img, lab) in enumerate(((big, 'poppetje B55 (8x)'), (foto.resize((512, 512), Image.LANCZOS), 'foto, gespiegeld'), (h8.convert('RGB'), 'Hitmontop (8x)'))):
        v2.paste(img, (12 + 524 * i, 36)); d2.text((12 + 524 * i, 12), lab, font=FB, fill=(30, 30, 30))
    v2.save(os.path.join(HERE, 'vel_pop_ronde1_8x.png'))


if __name__ == '__main__':
    vel()
