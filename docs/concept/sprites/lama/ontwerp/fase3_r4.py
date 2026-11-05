"""Lama fase 3, poppetje ronde 4 (5 nov). Jordi koos pose C (bijna frontaal, lijf 55 graden) en zei letterlijk:
"C is wel een goede, belangrijk is dat de bombin en vlechten echt duidelijk te zien zijn. Plus dat alls op het lichaam
echt op een worsteloutfit lijkt en dat de banden om de voorpoten beide even goed afgewerkt zijn".
- bombín groter en hoger (leesbaar op 64 px), vlechten dik, gevlochten, over de schouders naar voren tot op de borst;
- windsels: eigen ringen langs de as van elke voorpoot (beide gelijk), met een afgewerkte manchet boven en onder;
- worsteloutfit (cholita-luchadora): manta als intocht-cape met knoop op de borst, gouden kampioensriem om het middel,
  pollera als korte worstelrok; variant Y: daarbij een worstelpak (singlet) over het lijf.
Draaien vanuit de repo-root: python3 docs/concept/sprites/lama/ontwerp/fase3_r4.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pop3d_lama as L
import fase3_r3 as F3
P = L.P

L.COL.update(franje='#C9509E', franje2='#F2C84A', kant='#F6F0E6', gold='#F0C23A', goldd='#B8862A', plate='#FFE27A', gem='#D8243C', knot='#6E1A52', suit='#2F4FA8', suitrand='#D8243C')
L.LINED |= {'gold', 'goldd', 'plate', 'gem', 'knot', 'suit', 'suitrand', 'braid'}
YAW, HEAD_YAW, BORST = 55, 10, 6


def kop4(m, top, hs, yaw_extra, lid):
    h0 = len(m.parts)
    L.kop_lama(m, top, hs, 0, top, pitch=0, lid=lid, kleding=False)
    cr = top + np.array((-4, 5, 0)) * hs
    hc = cr + np.array((-0.5, 9.4, 0)) * hs                    # bombín: groter, hoog, licht schuin
    m.ell(hc, np.array((9.6, 1.3, 8.4)) * hs, 'hat')
    m.ell(hc + np.array((0, 1.7, 0)) * hs, np.array((6.3, 1.6, 5.7)) * hs, 'hatband')
    m.ell(hc + np.array((0, 4.6, 0)) * hs, np.array((5.9, 5.4, 5.3)) * hs, 'hat')
    for dx in (-6.5, -3.5):
        m.ell(cr + np.array((dx, 7.2, 0)) * hs, np.array((2.6, 2.2, 3.4)) * hs, 'pony')
    Rp = P.rot_z(math.radians(-8)); Ry = P.rot_y(math.radians(yaw_extra))
    m.parts[h0:] = [(top + Ry @ (top + Rp @ (c - top) - top), r, Ry @ Rp @ R0, g) for c, r, R0, g in m.parts[h0:]]


def vlechten(m, top, hs, yaw_extra):
    """Dikke vlechten vanachter de oren, over de schouders naar voren, met rode tullma; gevlochten (verspringende knotten)."""
    Ry = P.rot_y(math.radians(yaw_extra))
    for sz in (1, -1):
        a = top + Ry @ (np.array((-4 + 4, 5 + 3, 8.5 * sz)) * hs)          # start achter het oor
        b = np.array((-46, 14, 17 * sz), float)                            # eind vóór de schouder, op de borst
        n = 9
        for i in range(n):
            t = i / (n - 1)
            q = a + (b - a) * t + np.array((0, 0, 4 * sz)) * math.sin(math.pi * t)   # ligt over de hals heen
            q = q + np.array((0.9 * (-1) ** i, 0, 0)) * hs                          # vlechtknot
            m.ell(q, np.array((3.4, 3.0, 3.4)) * hs * (1 - 0.025 * i), 'braid')
        m.ell(b + np.array((-1, -5.5, 0)), np.array((3.6, 5.5, 3.6)), 'tassel')
        m.ell(b + np.array((-1, -1.5, 0)), np.array((3.4, 1.4, 3.4)), 'gold')


def windsel(m, pts, k):
    """Aguayo-windsels langs de as van het onderbeen (knie -> hoef), afgewerkt met een gouden manchet boven en onder."""
    p1, p2 = np.array(pts[1][:3], float), np.array(pts[2][:3], float)
    ax = (p1 - p2) / np.linalg.norm(p1 - p2)
    Rax = np.eye(3)
    yv = np.array((0, 1.0, 0)); v = np.cross(yv, ax)
    if np.linalg.norm(v) > 1e-6:
        v /= np.linalg.norm(v); ang = math.acos(np.clip(yv @ ax, -1, 1))
        K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        Rax = np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * K @ K
    rl = pts[2][3] * k
    banden = ['gold', 'ag0', 'ag1', 'ag2', 'ag4', 'ag0', 'gold']
    for j, g in enumerate(banden):
        c = p2 + ax * (3 + j * 3.1)
        dik = 1.6 if g == 'gold' else 1.3
        m.ell(c, np.array((rl + 2.4 * dik, 1.9, rl + 2.4 * dik)), g, Rax)


def fase3_r4(outfit='X', hs=1.55, neck=46, lid=0.55, franje=None, flen=18, kopk=1.0, legk=1.5, nr=0.0, persp=0.0, schouder=0.0, hb_hoog=False, breed=1.0):
    """kopk: kop (+bombín, vlechten) relatief kleiner/groter; legk: dikte poten; nr: hals dikker (ronde 6: buffer)."""
    m = P.Model()
    lx = 1.12
    for c, r in (((-26, 2, 0), (27, 27, 25)), ((4, 2, 0), (33, 24, 23)), ((33, 4, 0), (22, 24, 23))):
        m.ell((c[0] * lx, c[1], c[2]), (r[0] * lx, r[1], r[2]), 'suit' if outfit == 'Y' else 'body')
    if outfit == 'Y':   # worstelpak: rode bies langs de flank
        for x in np.arange(-44, 42, 3):
            m.ell((x, -4, 24.5), (2.2, 2.6, 1.2), 'suitrand'); m.ell((x, -4, -24.5), (2.2, 2.6, 1.2), 'suitrand')
    m.chain([(54, 14, 0, 5.5), (59, 22, 0, 6), (58, 28, 0, 4.5)], 'tail')
    m.ell((58, 28, 0), 5.5, 'tail')
    top = np.array((-38, 10 + neck, 0.0))
    nk = [(-34, 14, 0, 19.5 + nr), (-36, 10 + neck * 0.5, 0, 16 + nr), (top[0], top[1], 0, 13 + nr * 0.6)]
    h0 = len(m.parts)
    m.chain(nk, 'neck')
    hb = (nk[1][:3], nk[2][:3], 0.12) if hb_hoog else (nk[0][:3], nk[1][:3], 0.95)   # korte hals: band hoger, anders zakt hij in de cape
    L.halsband(m, *hb, 16.5 + nr * 0.8, ['ag3', 'ag0', 'ag1', 'ag2', 'ag0'], pompons=7)
    hk0 = len(m.parts)
    kop4(m, top, hs, HEAD_YAW, lid)
    vlechten(m, top, hs, HEAD_YAW)
    h1 = len(m.parts)
    if kopk != 1.0:   # kop relatief kleiner = lijf massiever; schaal om de halstop
        m.parts[hk0:h1] = [(top + kopk * (c - top), r * kopk, R0, g) for c, r, R0, g in m.parts[hk0:h1]]
    # manta als intocht-cape: over schouders en rug, open aan de borst, knoop vooraan
    for th in np.arange(-110, 111, 7):
        t = math.radians(th)
        c = np.array((-30 * lx + 3 * abs(math.sin(t)), 4 + 28.5 * math.cos(t), 26.5 * math.sin(t)))
        m.ell(c, np.array((13, 3.4, 6.5)), 'manta', P.rot_x(t))
        m.ell(c + np.array((12, -1, 0)), np.array((3.0, 3.4, 5.5)), 'mantarand', P.rot_x(t))
        m.ell(c + np.array((-11, -1, 0)), np.array((3.6, 3.4, 5.5)), 'mantarand', P.rot_x(t))
    m.ell((-49, 12, 0), np.array((5, 6, 7)), 'knot')
    for sz in (1, -1):
        m.chain([(-49, 8, 3 * sz, 3.6), (-50, -2, 6 * sz, 3.2), (-49, -10, 7 * sz, 2.6)], 'manta')
    # kampioensriem om het middel, met grote gouden plaat aan de kijkkant
    for th in np.arange(0, 360, 6):
        t = math.radians(th)
        m.ell(np.array((-2, 2 + 25 * math.cos(t), 24.5 * math.sin(t))), np.array((6.5, 3.2, 3.2)), 'goldd', P.rot_x(t))
    m.ell((-2, 2, 25), np.array((10, 10, 3.2)), 'gold')
    m.ell((-2, 2, 26.9), np.array((6.5, 6.5, 1.6)), 'plate')
    m.ell((-2, 2, 28.1), np.array((2.4, 2.4, 1)), 'gem')
    # pollera: korte worstelrok in drie ruches, vanaf de riem naar achteren uitwaaierend
    for j, (yy, ext) in enumerate(((0, 0), (-9, 3), (-18, 6))):
        for th in np.arange(0, 360, 7):
            t = math.radians(th)
            rr = 26 + ext
            m.ell(np.array((32 * lx * 0.95 + rr * 0.85 * math.cos(t), yy, rr * math.sin(t))), np.array((6.5, 6.5, 6.5)), f'pol{j}')
    if franje in ('manta', 'beide'):   # foto 9: franje aan de onderrand van de manta (accent, eindigt boven de buik)
        for th in (-112, 112):
            t = math.radians(th); sz = 1 if th > 0 else -1
            for x in np.arange(-44, -15, 1.7):
                y0 = 4 + 28.5 * math.cos(t) - 1
                m.ell((x, y0 - flen / 2, 27 * sz), np.array((1.3, flen / 2, 1.3)), 'franje')
        for x in np.arange(-50, -43, 2):   # borst, onder de knoop
            for sz in (1, -1):
                m.ell((x, 8 - 2 - flen / 2, 9 * sz), np.array((1.3, flen / 2, 1.3)), 'franje')
    if franje in ('pollera', 'beide'):  # foto 10: korte franje + kanten onderrand onder de onderste ruche
        rr = 32
        for th in np.arange(0, 360, 3.5):
            t = math.radians(th)
            c = np.array((32 * lx * 0.95 + rr * 0.85 * math.cos(t), -24, rr * math.sin(t)))
            m.ell(c, np.array((3.2, 2.4, 3.2)), 'kant')
            m.ell(c + np.array((0, -2 - flen * 0.35, 0)) * np.array((0, 1, 0)) + np.array((0.6 * math.cos(t), 0, 0.6 * math.sin(t))),
                  np.array((1.3, flen * 0.35, 1.3)), 'franje2')
    if breed != 1.0:   # ronde 7: lijf + kleding dikker (y/z), lengtes gelijk; hals, kop en poten niet geschaald
        def sc(c, r):
            return np.array((c[0], -10 + (c[1] + 10) * breed, c[2] * breed)), r * breed
        m.parts[:h0] = [(*sc(c, r), R0, g) for c, r, R0, g in m.parts[:h0]]
        m.parts[h1:] = [(*sc(c, r), R0, g) for c, r, R0, g in m.parts[h1:]]
    piv = np.array((30, -8, 0.0))
    L._rot(m, 0, len(m.parts), piv, P.rot_z(math.radians(-BORST)))
    pv = piv + P.rot_z(math.radians(-BORST)) @ (np.array(nk[0][:3], float) - piv)
    L._rot(m, h0, h1, pv, P.rot_z(math.radians(BORST)))
    for g, pts, voet in F3.POSES3['W_breed']:
        L.poot(m, pts, g, legk, None)        # hoeven vrij
        if voet == 'wrap':
            windsel(m, pts, legk)
            if schouder:   # schouderspier/biceps bovenaan de voorpoot (Entei/Arcanine)
                x, y, z = pts[0][:3]
                m.ell((x - 2, y - 6, z + 3 * np.sign(z)), np.array((13, 17, 9)) * schouder, g)
    if persp:   # geforceerd perspectief (Entei/Arcanine): voorkant groter, achterlijf kleiner; kop blijft gelijk
        out = []
        for i, (c, r, R0, g) in enumerate(m.parts):
            if hk0 <= i < h1:
                out.append((c, r, R0, g)); continue
            sx = 1 + persp * float(np.clip(-c[0] / 50, -1.2, 1.2))
            out.append((np.array((c[0], c[1] * sx, c[2] * sx)), r * sx, R0, g))
        m.parts[:] = out
    return m


def vel():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    L.set_vacht('bont (foto 4)'); L.COL['lid'] = L.COL['head']; L.COL['lip'] = '#C9A982'
    cell = 262
    im = Image.new('RGB', (12 + cell * 5, 44 + (cell + 30) * 2), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), 'Lama fase 3, poppetje ronde 4: pose C, bombín + vlechten leesbaar, worsteloutfit, windsels gelijk', font=FB, fill=(30, 30, 30))
    def tegel(img, i, rij, lab):
        x, y = 12 + cell * i, 44 + rij * (cell + 30)
        im.paste(img, (x + (256 - img.width) // 2, y + (256 - img.height) // 2)); d.text((x + 4, y + 260), lab, font=F, fill=(60, 60, 60))
    oud = F3.fase3_r3('W_breed', borst=6, head_yaw=10); img, _ = L.view(oud, YAW); tegel(img, 0, 0, 'ronde 3, optie C (gekozen)')
    mx = fase3_r4('X'); my = fase3_r4('Y')
    img, _ = L.view(mx, YAW); tegel(img, 1, 0, 'X: cape + riem + worstelrok')
    img, _ = L.view(my, YAW); tegel(img, 2, 0, 'Y: als X + worstelpak (singlet)')
    for i, (m, lab) in enumerate(((mx, 'X'), (my, 'Y'))):   # uitsneden: kop/vlechten en voorpoten
        big, a = L.view(m, YAW, size=236)
        big = big.resize((512, 512), Image.LANCZOS)
        tegel(big.crop((96, 20, 352, 276)), 3 + i, 0, f'{lab}: kop, bombín, vlechten')
    big, a = L.view(mx, YAW, size=236); big = big.resize((512, 512), Image.LANCZOS)
    tegel(big.crop((80, 250, 336, 506)), 0, 1, 'X: windsels beide voorpoten')
    # op spritegrootte (64 px) om leesbaarheid te toetsen
    for i, (m, lab) in enumerate(((mx, 'X'), (my, 'Y'))):
        img, a = L.view(m, YAW, size=250)
        sm = img.resize((64, 64), Image.LANCZOS).resize((256, 256), Image.NEAREST)
        tegel(sm, 1 + i, 1, f'{lab} op 64 px (ruwe verkleining)')
    ref = os.path.join(HERE, '../referenties')
    s = Image.open(os.path.join(HERE, '../fase2/af/lama.png')).convert('RGBA'); s = s.resize((256, 256), Image.NEAREST)
    bg = Image.new('RGBA', s.size, 'white'); bg.alpha_composite(s); tegel(bg.convert('RGB'), 3, 1, 'fase 2 (af), ter vergelijking')
    im.save(os.path.join(HERE, 'vel_fase3_ronde4.png'))


def vel5():
    """Ronde 5 (5 nov): franje (foto 9/10). Jordi: "zorg dat het niet volledig een jurk wordt" -> franje als accent."""
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    L.set_vacht('bont (foto 4)'); L.COL['lid'] = L.COL['head']; L.COL['lip'] = '#C9A982'
    ref = os.path.join(HERE, '../referenties')
    cell = 262
    im = Image.new('RGB', (12 + cell * 5, 44 + (cell + 30) * 3), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), 'Lama fase 3, poppetje ronde 5: franje als accent (foto 9 en 10), geen jurk; X (bont) of Y (blauw pak)', font=FB, fill=(30, 30, 30))
    def tegel(img, i, rij, lab):
        x, y = 12 + cell * i, 44 + rij * (cell + 30)
        im.paste(img, (x + (256 - img.width) // 2, y + (256 - img.height) // 2)); d.text((x + 4, y + 260), lab, font=F, fill=(60, 60, 60))
    opts = [(None, 'zonder franje'), ('manta', 'F1: franje manta'), ('pollera', 'F2: franje + kant rok'), ('beide', 'F3: beide')]
    for r, uit in enumerate('XY'):
        for i, (fr, lab) in enumerate(opts):
            m = fase3_r4(uit, franje=fr); img, _ = L.view(m, YAW); tegel(img, i, r, f'{uit} ({"bont" if uit == "X" else "blauw pak"}), {lab}')
    for j, (naam, lab) in enumerate((('foto9_cholitas_luchadoras_manta_franje.webp', 'foto 9: manta-franje'),
                                     ('foto10_cholita_sprong_pollera_kant.webp', 'foto 10: kant onder de pollera'))):
        f = Image.open(os.path.join(ref, naam)).convert('RGB'); f.thumbnail((256, 256)); tegel(f, 4, j, lab)
    for i, uit in enumerate('XY'):
        img, _ = L.view(fase3_r4(uit, franje='beide'), YAW, size=250)
        tegel(img.resize((64, 64), Image.LANCZOS).resize((256, 256), Image.NEAREST), i, 2, f'{uit} F3 op 64 px (ruw)')
    s = Image.open(os.path.join(HERE, '../fase2/af/lama.png')).convert('RGBA').resize((256, 256), Image.NEAREST)
    bg = Image.new('RGBA', s.size, 'white'); bg.alpha_composite(s); tegel(bg.convert('RGB'), 2, 2, 'fase 2 (af)')
    im.save(os.path.join(HERE, 'vel_fase3_ronde5.png'))


if __name__ == '__main__':
    vel()
    vel5()
