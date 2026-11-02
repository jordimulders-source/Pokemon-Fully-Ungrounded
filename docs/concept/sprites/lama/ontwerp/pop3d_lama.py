"""Lama (alpaca-evolutie, Fighting fase 2): 3D-poppetje voor pose, verhoudingen en kledinglijn.
Op basis van coathief/ontwerp/pop3d_coati.py en olinguito_v2/silhouet_kolibriemethode/pop3d.py.
Diercoördinaten: x = naar achteren, y = omhoog, z = naar de kijker bij 0°. Grond op y = -64.
Pose = foto 1 (referenties/foto1_lama_driekwart_POSE.png): staand, lijf driekwart naar links-voor, kop naar de kijker.
Kleding (Jordi 2 nov, SPEC): oorkwasten, pomponsnoer, aguayo over de rug, MMA-handschoenen met de teennagels eruit.
Draaien vanuit de repo-root: python3 docs/concept/sprites/lama/ontwerp/pop3d_lama.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../olinguito_v2/silhouet_kolibriemethode'))
import pop3d as P

R = 768
LINE = np.array((40, 26, 22), np.uint8)
AGUAYO = ['#D8243C', '#F2B02A', '#2E9C5A', '#E85A9A', '#2F5FB8', '#D8243C', '#F2B02A']
VACHT = {   # varianten van de lamavacht (Jordi: iets donkerder dan de alpaca)
    'licht karamel': dict(body='#E2B985', neck='#E2B985', head='#C99560', leg='#D6A672'),
    'karamel (foto 1)': dict(body='#C88E55', neck='#C88E55', head='#A86A3A', leg='#B57A45'),
    'bont (foto 4)': dict(body='#8E5530', neck='#EAD8B8', head='#EAD8B8', leg='#EAD8B8'),
}
COL = {
    'body': '', 'neck': '', 'head': '', 'leg': '', 'far': '', 'muzzle': '#5A3A2A', 'nose': '#241612',
    'eye': '#1C1414', 'glint': '#FFFFFF', 'ear': '', 'earin': '#7A4A3A', 'hoof': '#2E2420',
    'glove': '#D02A2A', 'strap': '#231C1C', 'nail': '#3A2E2A', 'tassel': '#E0264E', 'tail': '',
    'pp_r': '#D8243C', 'pp_y': '#F2B02A', 'pp_g': '#2E9C5A', 'pp_p': '#E85A9A',
    **{f'ag{i}': c for i, c in enumerate(AGUAYO)},
    'hat': '#3A2A26', 'hatband': '#8E1F33', 'pony': '#F2E2BE', 'braid': '#2A1E1A', 'manta': '#8A2466',
    'mantarand': '#E8B83A', 'pol0': '#D8243C', 'pol1': '#F2B02A', 'pol2': '#2E9C5A',
}
NOSHADE = {'eye', 'glint', 'nose'}
LINED = {'hat', 'hatband', 'manta', 'mantarand', 'pol0', 'pol1', 'pol2', 'eye', 'nose', 'glove', 'strap', 'tassel', 'pp_r', 'pp_y', 'pp_g', 'pp_p', 'nail'} | {f'ag{i}' for i in range(len(AGUAYO))}


def set_vacht(naam):
    v = VACHT[naam]
    COL.update(v)
    dark = lambda h: '#%02X%02X%02X' % tuple(int(c * 0.8) for c in P.hexc(h))
    COL.update(far=dark(v['leg']), ear=v['head'], tail=v['body'])


def fluff(m, c, r, g, n, rs, seed, ymin=-1.0):
    """Wolbobbels op het oppervlak van een ellipsoïde (geeft een wollige omtrek)."""
    rng = np.random.default_rng(seed)
    for _ in range(n):
        d = rng.normal(size=3); d /= np.linalg.norm(d)
        if d[1] < ymin:
            continue
        m.ell(np.array(c) + d * np.array(r) * 0.9, rs * rng.uniform(0.8, 1.15), g)


def lama(hs=1.35, neck=62, head_extra=24, leg_k=1.2, kleding=True, fase=2, body_k=1.0, hand='mma'):
    m = P.Model()
    # wollig lijf (foto 1: dikke vacht, rug recht, kont rond)
    for c, r in (((-28, 2, 0), (22, 22, 20)), ((2, 2, 0), (34, 21, 20)), ((32, 4, 0), (21, 22, 20))):
        r = (r[0], r[1] * body_k, r[2] * body_k)
        m.ell(c, r, 'body')
        fluff(m, c, r, 'body', 40, 6.5, int(abs(c[0])) + 3, ymin=-0.6)
    # korte staart omhoog (foto 1)
    m.chain([(48, 10, 0, 7), (54, 20, 0, 7.5), (53, 28, 0, 5.5)], 'tail')
    # hals: dik en wollig, licht naar voren
    top = np.array((-46, 4 + neck, 0.0))
    nk = [(-32, 12, 0, 18), (-40, 4 + neck * 0.55, 0, 15), (top[0], top[1], 0, 12.5)]
    m.chain(nk, 'neck')
    for i, (x, y, z, r) in enumerate(nk[1:]):
        fluff(m, (x, y, z), (r, r, r), 'neck', 18, 5, 50 + i)
    h0 = len(m.parts)
    cr = top + np.array((-6, 9, 0)) * hs
    m.ell(cr, np.array((13, 11.5, 11)) * hs, 'head')
    fluff(m, cr + np.array((2, 6, 0)) * hs, np.array((8, 6, 8)) * hs, 'head', 10, 3.2 * hs, 7, ymin=0.2)  # kruin
    m.chain([(cr[0] - 9 * hs, cr[1] - 3 * hs, 0, 8.5 * hs), (cr[0] - 18 * hs, cr[1] - 6 * hs, 0, 6.5 * hs)], 'head')
    m.ell(cr + np.array((-21, -7, 0)) * hs, np.array((4, 5, 6)) * hs, 'muzzle')
    m.ell(cr + np.array((-23.5, -5.5, 0)) * hs, 1.6 * hs, 'nose')
    for sz in (1, -1):   # grote, bijna zwarte ogen
        d = np.array((-0.35, 0.25, 0.9 * sz)); d /= np.linalg.norm(d)
        e = cr + d * np.array((13, 11.5, 11)) * hs * 0.95
        m.ell(e, 3.1 * hs, 'eye')
        m.ell(e + np.array((-0.8, 1.2, 1.6 * sz)) * hs, 0.9 * hs, 'glint')
    for sz in (1, -1):   # banaanoren: omhoog, punten krommen naar binnen
        b = cr + np.array((4, 9, 6 * sz)) * hs
        pts = [(b[0], b[1], b[2], 3.6 * hs), (b[0] + 1 * hs, b[1] + 10 * hs, b[2] + 2.5 * sz * hs, 3.4 * hs),
               (b[0] - 1 * hs, b[1] + 18 * hs, b[2] + 1 * sz * hs, 2.4 * hs), (b[0] - 3 * hs, b[1] + 22 * hs, b[2] - 2 * sz * hs, 1.2 * hs)]
        m.chain(pts, 'ear', 0.8)
        if kleding and fase == 2:   # oorkwast (foto 3: rode wolkwast bovenin het oor)
            m.ell((b[0] - 1.5 * hs, b[1] + 13 * hs, b[2] + 3.5 * sz * hs), np.array((3.6, 4.6, 3.6)) * hs, 'tassel')
    if kleding and fase == 3:   # bombín (verhard uit de kuif), pony, vlechten met rode tullma's
        hc = cr + np.array((2, 12.5, 0)) * hs
        m.ell(hc, np.array((10.5, 1.4, 10.5)) * hs, 'hat')               # rand
        m.ell(hc + np.array((0, 1.8, 0)) * hs, np.array((6.6, 1.6, 6.6)) * hs, 'hatband')
        m.ell(hc + np.array((0, 4.5, 0)) * hs, np.array((6.2, 5.6, 6.2)) * hs, 'hat')  # bol
        for dx in (-9, -6, -3):
            m.ell(cr + np.array((dx, 9, 0)) * hs, 2.6 * hs, 'pony')
        for sz in (1, -1):
            b = cr + np.array((6, 4, 9 * sz)) * hs
            pts = [b + np.array((2 * i * hs, -5.5 * i * hs, 0.6 * sz * i * hs)) for i in range(6)]
            for i, q in enumerate(pts):
                m.ell(q, np.array((3.4, 3.6, 3.4)) * hs * (1 - 0.04 * i), 'braid')
            m.ell(pts[-1] + np.array((0.5, -4.5, 0)) * hs, np.array((3, 4.2, 3)) * hs, 'tassel')
    if head_extra:   # kop draait meer naar de kijker dan het lijf (foto 1)
        piv = np.array(nk[1][:3], float)
        Rh = P.rot_y(math.radians(head_extra))
        m.parts[h0:] = [(piv + Rh @ (c - piv), r, Rh @ R0, g) for c, r, R0, g in m.parts[h0:]]
    # poten: lang, onderbeen zonder wol; staand zoals foto 1 (nabije voorpoot iets naar voren)
    L = lambda pts: [(x, y, z, r * leg_k) for x, y, z, r in pts]
    legs = [('leg', [(-32, -10, 12, 9), (-42, -36, 13, 6.5), (-48, -57, 13, 5.5)], True),
            ('far', [(-20, -10, -12, 9), (-10, -36, -13, 6.5), (-4, -57, -13, 5.5)], True),
            ('leg', [(32, -8, 12, 10.5), (38, -32, 13, 6.5), (35, -57, 13, 5.5)], False),
            ('far', [(38, -8, -12, 10.5), (44, -32, -13, 6.5), (42, -57, -13, 5.5)], False)]
    for g, pts, front in legs:
        m.chain(L(pts), g)
        x, y, z = pts[-1][:3]
        if front and hand == 'wrap':   # fase 3-variant: hoef vrij, aguayo-windsels om het onderbeen
            m.ell((x - 2, y - 4, z), np.array((6.5, 3.5, 5.5)) * leg_k, 'hoof')
            for j in range(4):
                m.ell((x + 1 + j * 0.6, y + 2 + j * 4.2, z), np.array((6.6, 2.4, 6.6)) * leg_k, f'ag{j}')
        elif front and hand == 'mma':   # MMA-handschoen: kort, open, de twee teennagels steken eruit
            m.ell((x - 1, y - 2, z), np.array((11, 9, 10.5)) * leg_k, 'glove')
            m.ell((x + 1, y + 7, z), np.array((8.5, 3.2, 8.5)) * leg_k, 'strap')
            for dz in (-2.6, 2.6):
                m.ell((x - 11, y - 6.5, z + dz * 1.3), np.array((3.4, 2.6, 2.6)), 'nail')
        else:
            m.ell((x - 2, y - 4, z), np.array((6.5, 3.5, 5.5)) * leg_k, 'hoof')
    if kleding and fase == 3:
        # pollera: drie ruches om het achterlijf, klokvorm (rood, goud, groen)
        for j, (yy, ext) in enumerate(((2, 0), (-9, 2.5), (-20, 5))):
            for th in np.arange(0, 360, 10):
                t = math.radians(th)
                c = np.array((24, yy, 0)) + np.array((0, 0, 0))
                rr = 23 * body_k + ext
                m.ell(c + np.array((0, rr * 0.55 * math.cos(t) * 0, rr * math.sin(t))) + np.array((rr * 0.9 * math.cos(t), 0, 0)),
                      np.array((5.5, 6, 5.5)), f'pol{j}')
        # manta over de schouders: omslagdoek, hangt over de borst, gouden zoom
        for th in np.arange(-96, 97, 8):
            t = math.radians(th)
            c = np.array((-26, 8 + 23 * body_k * math.cos(t), 22 * body_k * math.sin(t)))
            m.ell(c, np.array((13, 3.2, 6)), 'manta', P.rot_x(t))
            m.ell(c + np.array((-10, -3, 0)), np.array((3.5, 3, 5)), 'mantarand', P.rot_x(t))
    if kleding and fase == 2:
        # pomponsnoer om de halsbasis
        c0, ring = np.array((-36, 18, 0.0)), ['pp_r', 'pp_y', 'pp_g', 'pp_p']
        for i, a in enumerate(np.linspace(0, 2 * math.pi, 14, endpoint=False)):
            p = c0 + np.array((math.cos(a) * 6 - 2 * math.sin(a), math.sin(a) * 2 - 1, math.sin(a) * 19 + 0 * math.cos(a)))
            p[0] += math.cos(a) * 11
            m.ell(p, 3.4, ring[i % 4])
        # aguayo over de rug: gestreepte doek (strepen in de lengte van de rug), hangt tot halverwege de flank
        for th in np.arange(-78, 79, 6):
            t = math.radians(th)
            band = int((th + 78) // 26) % len(AGUAYO)
            c = np.array((2, 4 + 25.5 * math.cos(t), 24.5 * math.sin(t)))
            m.ell(c, np.array((19, 3.2, 5.5)), f'ag{band}', P.rot_x(t))
    return m


def render(m, yaw, pitch, scale, center):
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    zbuf = np.full((R, R), -1e9, np.float32); gid = np.full((R, R), -1, np.int16)
    nrm = np.zeros((R, R, 3), np.float32); groups = list(COL)
    ys, xs = np.mgrid[0:R, 0:R]
    wx = (xs - R / 2) / scale + center[0]; wy = -((ys - R / 2) / scale) + center[1]
    for c, r, R0, g in m.parts:
        cw = Rc @ c
        M = np.diag(1 / r) @ R0.T @ Rc.T
        ext = r.max()
        x0 = int(max(0, (cw[0] - ext - center[0]) * scale + R / 2 - 2)); x1 = int(min(R, (cw[0] + ext - center[0]) * scale + R / 2 + 3))
        y0 = int(max(0, (-(cw[1] + ext) + center[1]) * scale + R / 2 - 2)); y1 = int(min(R, (-(cw[1] - ext) + center[1]) * scale + R / 2 + 3))
        if x0 >= x1 or y0 >= y1:
            continue
        px = wx[y0:y1, x0:x1] - cw[0]; py = wy[y0:y1, x0:x1] - cw[1]
        a = M[:, 0, None, None] * px + M[:, 1, None, None] * py
        b = M[:, 2]; A = b @ b
        B = 2 * (a * b[:, None, None]).sum(0); C = (a * a).sum(0) - 1
        disc = B * B - 4 * A * C; hit = disc >= 0
        z = (-B + np.sqrt(np.where(hit, disc, 0))) / (2 * A) + cw[2]
        sub = zbuf[y0:y1, x0:x1]; win = hit & (z > sub)
        sub[win] = z[win]; gid[y0:y1, x0:x1][win] = groups.index(g)
        p = np.stack([px, py, z - cw[2]], -1)
        n = p @ (M.T @ M).T
        n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9
        nrm[y0:y1, x0:x1][win] = n[win]
    return zbuf, gid, nrm, groups


def shade(zbuf, gid, nrm, groups, out=256):
    a = gid >= 0
    rgb = np.ones((R, R, 3), np.float32) * 255
    Lt = np.array((-0.45, 0.65, 0.62)); Lt /= np.linalg.norm(Lt)
    lit = (nrm @ Lt) > -0.2
    for i, g in enumerate(groups):
        mm = gid == i; col = P.hexc(COL[g]); rgb[mm] = col
        if g not in NOSHADE:
            rgb[mm & ~lit] = col * 0.78
    edge = np.zeros((R, R), bool); z = np.where(a, zbuf, -1e9)
    lined = np.isin(gid, [groups.index(g) for g in LINED])
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        z2 = np.roll(np.roll(z, -dy, 0), -dx, 1); g2 = np.roll(np.roll(gid, -dy, 0), -dx, 1); l2 = np.roll(np.roll(lined, -dy, 0), -dx, 1)
        e = (np.abs(z - z2) > 6) | ((gid != g2) & (lined | l2))
        edge |= e; edge |= np.roll(np.roll(e, dy, 0), dx, 1)
    for _ in range(2):
        edge = edge | np.roll(edge, 1, 0) | np.roll(edge, 1, 1)
    inner = a.copy()
    for _ in range(7):
        inner = inner & np.roll(inner, 1, 0) & np.roll(inner, -1, 0) & np.roll(inner, 1, 1) & np.roll(inner, -1, 1)
    edge = (edge & a) | (a & ~inner)
    rgb[edge] = LINE; rgb[~a] = 255
    return Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).resize((out, out), Image.LANCZOS), a


def view(m, yaw, pitch=8, size=236):
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
    x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
    scale = R * (size / 256) / max(x1 - x0, y1 - y0)
    img, a = shade(*render(m, yaw, pitch, scale, ((x0 + x1) / 2, (y0 + y1) / 2)))
    return img, a


def kopaandeel(m, yaw, pitch=8):
    """Kophoogte (oren tot kin) / totale hoogte, zoals D2 in FAKEMON_CHECKLIST."""
    Rc = P.rot_x(math.radians(pitch)) @ P.rot_y(math.radians(yaw))
    yy = [((Rc @ c)[1] - r.max(), (Rc @ c)[1] + r.max(), g) for c, r, R0, g in m.parts]
    lo, hi = min(y[0] for y in yy), max(y[1] for y in yy)
    hd = [y for y in yy if y[2] in ('head', 'ear', 'eye', 'muzzle')]
    return (max(y[1] for y in hd) - min(y[0] for y in hd)) / (hi - lo)


VARIANTEN = {'A': dict(hs=1.15, neck=70), 'B': dict(hs=1.35, neck=60), 'C': dict(hs=1.55, neck=50)}


def vel():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    ref = os.path.join(HERE, '../referenties')
    cell, W = 262, 12 + 262 * 4
    im = Image.new('RGB', (W, 44 + (cell + 24) * 2), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), 'Lama (fase 2): poppetje in de hoek van foto 1. Rij 1: verhoudingen, rij 2: vacht (op B)', font=FB, fill=(30, 30, 30))
    yaw = 40
    set_vacht('karamel (foto 1)')
    for i, (k, v) in enumerate(VARIANTEN.items()):
        m = lama(**v); img, _ = view(m, yaw)
        x, y = 12 + cell * i, 44; im.paste(img, (x, y))
        d.text((x + 4, y + 258), f'{k}: kop {kopaandeel(m, yaw):.0%} van de hoogte, hals {v["neck"]}', font=F, fill=(60, 60, 60))
    foto = Image.open(os.path.join(ref, 'foto1_lama_driekwart_POSE.png')).convert('RGB')
    foto.thumbnail((256, 256)); im.paste(foto, (12 + cell * 3, 44)); d.text((16 + cell * 3, 44 + 258), 'foto 1 (pose)', font=F, fill=(60, 60, 60))
    for i, naam in enumerate(VACHT):
        set_vacht(naam); img, _ = view(lama(**VARIANTEN['B']), yaw)
        x, y = 12 + cell * i, 44 + cell + 24; im.paste(img, (x, y)); d.text((x + 4, y + 258), naam, font=F, fill=(60, 60, 60))
    f1 = Image.open(os.path.join(ref, 'fase1_alpaca.png')).convert('RGBA').resize((256, 256), Image.NEAREST)
    bg = Image.new('RGBA', f1.size, 'white'); bg.alpha_composite(f1)
    im.paste(bg.convert('RGB'), (12 + cell * 3, 44 + cell + 24)); d.text((16 + cell * 3, 44 + 2 * cell + 26), 'fase 1 (alpaca, af)', font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, 'vel_ronde1.png'))


FASE3 = dict(hs=1.2, neck=80, leg_k=1.45, fase=3, body_k=1.12)


def lijn():
    """Fase 1 (sprite) - fase 2 (B, karamel) - fase 3 (varianten) op schaal (hoogte ~ wortel van het doel-oppervlak)."""
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    ref = os.path.join(HERE, '../referenties')
    W, H, base = 12 + 300 * 4, 400, 360
    im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 10), 'Lama-lijn op schaal: fase 1 (af) - fase 2 (B, karamel) - fase 3 (bont, twee varianten)', font=FB, fill=(30, 30, 30))
    def plak(img, a, i, h, lab):
        bb = Image.fromarray((a * 255).astype(np.uint8)).resize(img.size).getbbox()
        img = img.crop(bb); k = h / img.height
        img = img.resize((max(1, int(img.width * k)), int(h)), Image.LANCZOS)
        x = 12 + 300 * i + (300 - img.width) // 2
        im.paste(img, (x, base - img.height)); d.text((12 + 300 * i + 6, base + 12), lab, font=F, fill=(60, 60, 60))
    f1 = Image.open(os.path.join(ref, 'fase1_alpaca.png')).convert('RGBA')
    f1 = f1.crop(f1.getbbox()); k = 300 * 0.62 / f1.height
    f1 = f1.resize((int(f1.width * k), int(f1.height * k)), Image.NEAREST)
    bg = Image.new('RGBA', f1.size, 'white'); bg.alpha_composite(f1)
    im.paste(bg.convert('RGB'), (12 + (300 - f1.width) // 2, base - f1.height)); d.text((18, base + 12), 'fase 1: alpaca (sprite, af)', font=F, fill=(60, 60, 60))
    set_vacht('karamel (foto 1)'); img, a = view(lama(**VARIANTEN['B']), 40)
    plak(img, a, 1, 300 * 0.78, f'fase 2: B, kop {kopaandeel(lama(**VARIANTEN["B"]), 40):.0%}')
    set_vacht('bont (foto 4)')
    for i, (hand, lab) in enumerate((('mma', 'MMA-handschoenen'), ('wrap', 'windsels, hoeven vrij'))):
        m = lama(**FASE3, hand=hand); img, a = view(m, 40)
        plak(img, a, 2 + i, 300 * 0.98, f'fase 3{"XY"[i]}: {lab}, kop {kopaandeel(m, 40):.0%}')
    im.save(os.path.join(HERE, 'lijn_ronde1.png'))


if __name__ == '__main__':
    vel()
    lijn()
