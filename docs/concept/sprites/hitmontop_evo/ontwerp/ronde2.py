"""Hitmontop-evolutie, poppetje ronde 2 (5 nov). Pose en standen bevroren (B55 hoofdstand, A70 ernaast).
Coördinator (na ronde 1: "leest als een cartoonmensje met paardenstaart, niet als een Hitmon-familielid"):
1. kop = Hitmontops kop (brede bruine koepel op een platte, puntige rand; schuine boze ogen; mond), kleine stompe hoorn, groter;
2. haar: 4-6 dikke, korte, simpele dreads die als kroon uit die kop komen en door de zwaartekracht omlaag hangen;
3. lijf: één volle, compacte vorm (geen schouderbult, geen mensenborst), ledematen voller, V-split blijft lang;
4. familiedetails: blauwe voeten met witte klauwen, lichte ronde handen, wit-grijze polsmanchetten zoals Hitmontop;
5. cordão dikker en duidelijker, armkoordjes blijven.
Kop zoals in de Hitmontop-sprite: koepel (gezicht) boven, rand eronder, hoorn onderaan. Hij staat op zijn hand,
dus de kruin wijst naar de grond: de dreads hangen vanaf de rand omlaag.
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/ontwerp/ronde2.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pop3d_hitmontop_evo as E
from pop3d_hitmontop_evo import L, P, W, tube, ball, ring, staart, axis_rot

E.COL.update({
    'dome': '#DEBD83', 'brim': '#B48B5A', 'brimtip': '#B48B5A', 'mouth': '#835A29', 'browd': '#835A29',
    'loc': '#835A29', 'loc2': '#835A29', 'pantsb': '#629CDE', 'cuffw': '#E8E8E8', 'claw2': '#FFFFFF',
})
E.LINED |= {'dome', 'brim', 'mouth', 'browd', 'loc', 'loc2', 'cuffw', 'claw2', 'pantsb'}
L.COL.clear(); L.COL.update(E.COL)
L.LINED.clear(); L.LINED.update(E.LINED)
L.NOSHADE.add('mouth')


def voet2(m, ankle, toe, g):
    """Hitmontop-voet: ronde blauwe voet, drie witte klauwen aan de punt; kleiner t.o.v. het been maar duidelijk."""
    a, t = np.array(ankle, float), np.array(toe, float)
    d = t - a; Ln = np.linalg.norm(d); d /= Ln
    m.ell(W(*(a + d * Ln * 0.45)), np.array((64, Ln * 0.62, 58)) / 10.0, g, axis_rot(W(*t) - W(*a)))
    side = np.cross(np.append(d[:2], 0), np.array((0, 0, 1.0))); side /= np.linalg.norm(side) + 1e-9
    for s in (-1, 0, 1):
        b = t - d * 22 + side * s * 34 + np.array((0, 0, 16 * (1 - abs(s))))
        e = b + d * (82 if s == 0 else 66) + side * s * 26
        tube(m, [(*b, 28), (*((b + e) / 2), 20), (*e, 6)], 'claw2', 0.6)


def kop(m, H, hk=1.15, tilt=-8, alpha=40, ndread=5, dlen=1.0, dk=1.0):
    """Hitmontop-kop: koepel (gezicht) op een brede platte rand met puntige zijkanten; stompe hoorn onder de rand.
    Zoals in de sprite is de rand naar de kijker gekanteld (alpha), zodat hij als brede lens rond de onderkant van het
    gezicht leest. Lokaal: x rechts, y = koepelas, z naar de kijker; omgezet naar foto-px (y omlaag)."""
    Rh = P.rot_z(math.radians(tilt)) @ P.rot_x(math.radians(alpha))
    Rf = P.rot_x(math.radians(-alpha))   # gezichtsrichtingen in wereldzin -> lokaal

    def HL(v):
        q = Rh @ np.array(v, float) * hk
        return np.array((H[0] + q[0], H[1] - q[1], H[2] + q[2]))
    rd = np.array((150, 132, 136))
    ball(m, tuple(HL((0, 0, 0))), rd * hk, 'dome', Rh)
    ball(m, tuple(HL((0, -88, 10))), np.array((215, 34, 196)) * hk, 'brim', Rh)
    for sx in (-1, 1):
        tube(m, [(*HL((sx * 180, -88, 10)), 36 * hk), (*HL((sx * 226, -85, 10)), 23 * hk), (*HL((sx * 272, -78, 10)), 7 * hk)], 'brim', 0.6)
    # kleine stompe hoorn midden onder de rand (= kruin; de kop hangt omgekeerd zoals bij Hitmontop)
    tube(m, [(*HL((0, -100, 0)), 34 * hk), (*HL((0, -130, 0)), 26 * hk), (*HL((0, -150, 0)), 17 * hk)], 'horn', 0.6)
    # gezicht: richting in wereldzin (naar de kijker), terug naar lokaal
    def F(v, k=0.98):
        v = np.array(v, float); v /= np.linalg.norm(v)
        return HL(Rf @ v * 0 + (Rf @ v) * rd * k) if False else HL((Rf @ v) * rd * k)
    for sx in (-1, 1):
        e = F((0.37 * sx, -0.10, 0.92))
        Re = P.rot_z(math.radians(tilt - 16 * sx))
        ball(m, tuple(e), np.array((30, 27, 16)) * hk, 'eye', Re)
        ball(m, tuple(e + np.array((-10, -8, 15)) * hk), 8 * hk, 'glint')
        b = F((0.34 * sx, 0.20, 0.92), 1.0)
        ball(m, tuple(b), np.array((46, 10, 16)) * hk, 'browd', P.rot_z(math.radians(tilt + 24 * sx)))
    ball(m, tuple(F((0.05, -0.45, 0.89), 1.0)), np.array((28, 7, 14)) * hk, 'mouth', P.rot_z(math.radians(tilt + 4)))
    # dreads: 5 dikke korte strengen onder de rand vandaan (de kruin wijst naar de grond), door de zwaartekracht omlaag,
    # als een omgekeerde kroon licht uitwaaierend; ongelijke lengtes, ronde punten; om en om eigen groep (eigen lijn)
    xs = np.linspace(-165, 125, ndread)
    for j, x0 in enumerate(xs):
        a = HL((x0, -112, 150 * math.sqrt(max(0.0, 1 - (x0 / 215) ** 2)) - 60))   # net onder de rand: geen bollen óp de rand
        ln = (150 + 32 * ((j * 2) % 3)) * dlen * hk
        sp = math.radians(32 * x0 / 150)
        e = (a[0] + math.sin(sp) * ln, a[1] + math.cos(sp) * ln, a[2] + 20)
        mid = (a[0] + math.sin(sp) * ln * 0.45, a[1] + math.cos(sp) * ln * 0.5, a[2] + 12)
        g = 'loc' if j % 2 else 'loc2'
        tube(m, [(*a, 38 * dk), (*mid, 36 * dk), (*e, 31 * dk)], g)
        ball(m, e, 32 * dk, g)
    return HL


def r2(hk=1.15, ndread=5, dlen=1.0, dk=1.0):
    E.LIMB_K = 1.0
    m = P.Model()
    # --- romp + broek als één volle vorm langs de foto-as (heup rechtsboven -> schouders linksonder)
    tube(m, [(910, 690, 0, 136), (822, 790, 4, 128)], 'pantsb')
    tube(m, [(822, 790, 4, 126), (735, 880, 8, 132), (655, 975, 4, 112), (625, 1030, 0, 82)], 'skin')
    # cordão: dikke ring om de taille (grens broek/huid), knoop vooraan, twee dikke hangende einden
    ax = np.array((822 - 910, 790 - 690, 0.0)); ax /= np.linalg.norm(ax)
    u = np.array((-ax[1], ax[0], 0.0))
    for th in np.arange(0, 360, 9):
        tr = math.radians(th)
        c = np.array((822, 790, 4.0)) + (u * math.cos(tr) + np.array((0, 0, 1.0)) * math.sin(tr)) * 128
        ball(m, tuple(c), 28, 'cord')
    knot = (880, 800, 120)
    ball(m, knot, 40, 'cordknot')
    staart(m, knot, [(0, 70, 4), (-6, 140, 2), (-12, 200, 0)], 'cord', 26, 20)
    staart(m, knot, [(34, 62, -6), (70, 125, -14), (92, 185, -20)], 'cord', 26, 20)
    # --- benen: lange aansluitende broek, voller; V-split zoals de foto
    tube(m, [(860, 640, 30, 96), (720, 560, 32, 80), (560, 468, 30, 66), (400, 375, 26, 56), (312, 322, 24, 50)], 'leg1')
    ring(m, (400, 375, 26), (300, 315, 24), 0.85, 62, 'cuff', 16)
    tube(m, [(300, 315, 24, 38), (262, 292, 24, 34)], 'ankle')
    voet2(m, (262, 292, 24), (180, 395, 30), 'foot')
    tube(m, [(930, 630, -30, 92), (1010, 572, -32, 78), (1110, 500, -32, 64), (1200, 432, -30, 54), (1250, 395, -30, 48)], 'leg2')
    ring(m, (1200, 432, -30), (1258, 388, -30), 0.85, 60, 'cuff', 16)
    tube(m, [(1255, 390, -30, 36), (1275, 360, -30, 33)], 'ankle')
    voet2(m, (1275, 360, -30), (1322, 222, -30), 'foot2')
    # --- steunarm: start binnen de romp (geen schouderbal), recht omlaag; manchet + ronde lichte hand op de grond
    tube(m, [(640, 1000, 0, 56), (632, 1150, 0, 52), (615, 1290, 0, 46), (594, 1388, 0, 42)], 'skin')
    ring(m, (615, 1290, 0), (590, 1410, 0), 0.82, 48, 'cuffw', 16)
    ball(m, (578, 1452, 8), (74, 66, 70), 'hand')
    c = ring(m, (640, 1060, 0), (615, 1290, 0), 0.25, 60, 'band', 18)
    staart(m, (c[0] - 36, c[1] + 8, 36), [(-16, 55, 10), (-24, 110, 14)], 'band', 20, 15)
    # --- vrije arm: wortel binnen de romp, over de heup, manchet + ronde hand
    tube(m, [(720, 790, 40, 52), (775, 705, 80, 50), (838, 680, 105, 46), (860, 765, 125, 42), (854, 860, 135, 39)], 'arm2')
    ring(m, (858, 765, 125), (852, 880, 135), 0.75, 44, 'cuffw', 15)
    ball(m, (842, 925, 145), 64, 'hand2')
    c = ring(m, (720, 790, 40), (838, 680, 105), 0.6, 56, 'band2', 18)
    staart(m, (c[0], c[1] + 34, c[2] + 24), [(-4, 55, 6), (-14, 110, 10)], 'band2', 20, 15)
    # --- kop: Hitmontop-kop, ±1,4x de ronde-1-kop, links van de steunarm; korte nek erin
    tube(m, [(650, 960, 0, 70), (560, 880, 0, 70)], 'skin')
    kop(m, np.array((440.0, 812.0, 40.0)), hk, ndread=ndread, dlen=dlen, dk=dk)
    Rp = P.rot_y(math.radians(-E.YAW_FOTO))
    m.parts[:] = [(Rp @ c, r, Rp @ R0, g) for c, r, R0, g in m.parts]
    return m


def vel2():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    E.LIMB_K = 1.15
    m1 = E.hitmontop_evo()
    m = r2()
    cell = 262
    im = Image.new('RGB', (12 + cell * 5, 44 + (cell + 30) * 3), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), 'Hitmontop-evolutie, poppetje ronde 2: Hitmontop-kop met hangende dreads, compact lijf, familiedetails', font=FB, fill=(30, 30, 30))

    def tegel(img, i, rij, lab):
        x, y = 12 + cell * i, 44 + rij * (cell + 30)
        im.paste(img, (x + (256 - img.width) // 2, y + (256 - img.height) // 2)); d.text((x + 4, y + 260), lab, font=F, fill=(60, 60, 60))
    img, _ = L.view(m1, 55, 6); tegel(img, 0, 0, 'ronde 1, B55 (ter vergelijking)')
    img, _ = L.view(m, 55, 6); tegel(img, 1, 0, 'ronde 2, B55 (hoofdstand)')
    img, _ = L.view(m, 70, 6); tegel(img, 2, 0, 'ronde 2, A70 (zoals de foto)')
    foto = Image.open(os.path.join(HERE, '../referenties/pose_eenhandsstand.webp')).convert('RGB').crop((0, 0, 1580, 1580)).transpose(Image.FLIP_LEFT_RIGHT)
    tegel(foto.resize((256, 256), Image.LANCZOS), 3, 0, 'foto, gespiegeld')
    big, a = E.render_foto(m)
    ova = np.asarray(foto.resize((768, 768), Image.LANCZOS)).copy()
    rand = a & ~(np.roll(a, 1, 0) & np.roll(a, -1, 0) & np.roll(a, 1, 1) & np.roll(a, -1, 1))
    for _ in range(2):
        rand = rand | np.roll(rand, 1, 0) | np.roll(rand, 1, 1)
    ova[rand] = (220, 30, 30)
    tegel(Image.fromarray(ova).resize((256, 256), Image.LANCZOS), 4, 0, 'A70 als rode omtrek over de foto')
    big, _ = L.view(m, 55, 6, size=236); big = big.resize((768, 768), Image.LANCZOS); big.save(os.path.join(HERE, 'pop2_55.png'))
    tegel(big.crop((50, 270, 306, 526)), 0, 1, 'B55: kop, dreads, hoorn (3x)')
    tegel(big.crop((20, 30, 276, 286)), 1, 1, 'B55: voet linksboven (3x)')
    tegel(big.crop((300, 180, 556, 436)), 2, 1, 'B55: cordão, vrije arm (3x)')
    h1 = Image.open(os.path.join(E.ROOT, 'graphics/pokemon/hitmontop/anim_front.png')).convert('RGBA').crop((0, 0, 64, 64))
    hk = h1.crop((10, 28, 56, 62)).resize((46 * 5, 34 * 5), Image.NEAREST)
    bg = Image.new('RGBA', (256, 256), (255, 255, 255, 255)); bg.alpha_composite(hk, (13, 40)); tegel(bg.convert('RGB'), 3, 1, 'Hitmontop-kop (5x), de bron')
    bg = Image.new('RGBA', (256, 256), (255, 255, 255, 255)); bg.alpha_composite(h1.resize((256, 256), Image.NEAREST)); tegel(bg.convert('RGB'), 4, 1, 'Hitmontop (4x)')
    s55 = E.frame64(m, 55); s70 = E.frame64(m, 70); s1 = E.frame64(m1, 55)
    s55.save(os.path.join(HERE, 'pop2_55_64.png')); s70.save(os.path.join(HERE, 'pop2_70_64.png'))
    tegel(s55.resize((256, 256), Image.NEAREST), 0, 2, 'ronde 2 B55 op 64 px (4x)')
    tegel(s70.resize((256, 256), Image.NEAREST), 1, 2, 'ronde 2 A70 op 64 px (4x)')
    een = Image.new('RGB', (256, 256), 'white'); de = ImageDraw.Draw(een)
    t = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); t.alpha_composite(h1)
    een.paste(s1, (10, 40)); een.paste(s55, (96, 40)); een.paste(t.convert('RGB'), (182, 40))
    de.text((10, 20), 'r1 B55     r2 B55    Hitmontop', font=F, fill=(60, 60, 60))
    een.paste(s1.resize((128, 128), Image.NEAREST).crop((0, 0, 120, 128)), (0, 120)); een.paste(s55.resize((128, 128), Image.NEAREST), (124, 120))
    tegel(een, 2, 2, '1x (boven) en 2x (onder), ronde 1 en 2')
    tegel(s1.resize((256, 256), Image.NEAREST), 3, 2, 'ronde 1 B55 op 64 px (4x)')
    im.save(os.path.join(HERE, 'vel_pop_ronde2.png'))
    # 8x-vel: B55 naast foto en Hitmontop
    b8, _ = L.view(m, 55, 6, size=232); b8 = b8.resize((512, 512), Image.LANCZOS)
    h8 = Image.new('RGBA', (512, 512), (255, 255, 255, 255)); h8.alpha_composite(h1.resize((512, 512), Image.NEAREST))
    v2 = Image.new('RGB', (12 + 524 * 3, 560), 'white'); d2 = ImageDraw.Draw(v2)
    for i, (img, lab) in enumerate(((b8, 'poppetje ronde 2, B55 (8x)'), (foto.resize((512, 512), Image.LANCZOS), 'foto, gespiegeld'), (h8.convert('RGB'), 'Hitmontop (8x)'))):
        v2.paste(img, (12 + 524 * i, 36)); d2.text((12 + 524 * i, 12), lab, font=FB, fill=(30, 30, 30))
    v2.save(os.path.join(HERE, 'vel_pop_ronde2_8x.png'))


def vel_dreads():
    """Drie dreadvarianten naast elkaar (B55), groot en op 64 px: de dreads zijn het open punt van ronde 2."""
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    vs = [('D1: 5 lang (hoofdversie)', dict()), ('D2: 5 kort en dik', dict(dlen=0.55, dk=1.2)), ('D3: 4 halflang, dik', dict(ndread=4, dlen=0.8, dk=1.25))]
    cell = 262
    im = Image.new('RGB', (12 + cell * 3, 44 + (cell + 30) * 2), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), 'Ronde 2: dreadvarianten (B55), boven 3x uitsnede, onder op 64 px (4x)', font=FB, fill=(30, 30, 30))
    for i, (lab, kw) in enumerate(vs):
        m = r2(**kw)
        big, _ = L.view(m, 55, 6, size=236); big = big.resize((768, 768), Image.LANCZOS)
        x = 12 + cell * i
        im.paste(big.crop((50, 270, 306, 526)), (x, 44)); d.text((x + 4, 44 + 260), lab, font=F, fill=(60, 60, 60))
        im.paste(E.frame64(m, 55).resize((256, 256), Image.NEAREST), (x, 44 + cell + 30)); d.text((x + 4, 44 + cell + 30 + 260), lab + ', 64 px', font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, 'vel_pop_ronde2_dreads.png'))


if __name__ == '__main__':
    vel2()
    vel_dreads()
