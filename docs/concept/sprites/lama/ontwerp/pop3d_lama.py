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


# ---------------------------------------------------------------- ronde 2 (Jordi 2 nov: "doe 1 + 2")
# 1 = bouw: fase 2 slungelige tiener (lange dunne poten, smal lijf, wilde wolplukken),
#     fase 3 zware kampioen (brede borst, dikke poten, kortere krachtige hals, geschoren lijf; wol alleen als kleding).
# 2 = pose: fase 2 onrustig in dekking (nabije voorpoot opgetild, kop laag en naar voren),
#     fase 3 geworteld (breed op vier poten, borst vooruit, kop hoog).

def kop(m, top, hs, fase, head_extra, piv):
    h0 = len(m.parts)
    cr = top + np.array((-6, 9, 0)) * hs
    m.ell(cr, np.array((13, 11.5, 11)) * hs, 'head')
    if fase == 2:
        fluff(m, cr + np.array((2, 6, 0)) * hs, np.array((8, 6, 8)) * hs, 'head', 14, 3.6 * hs, 7, ymin=0.1)
    m.chain([(cr[0] - 9 * hs, cr[1] - 3 * hs, 0, 8.5 * hs), (cr[0] - 18 * hs, cr[1] - 6 * hs, 0, 6.5 * hs)], 'head')
    m.ell(cr + np.array((-21, -7, 0)) * hs, np.array((4, 5, 6)) * hs, 'muzzle')
    m.ell(cr + np.array((-23.5, -5.5, 0)) * hs, 1.6 * hs, 'nose')
    for sz in (1, -1):
        d = np.array((-0.35, 0.25, 0.9 * sz)); d /= np.linalg.norm(d)
        e = cr + d * np.array((13, 11.5, 11)) * hs * 0.95
        m.ell(e, 3.1 * hs, 'eye')
        m.ell(e + np.array((-0.8, 1.2, 1.6 * sz)) * hs, 0.9 * hs, 'glint')
    for sz in (1, -1):
        b = cr + np.array((4, 9, 6 * sz)) * hs
        if fase == 2:   # oren plat naar achteren (boos, klaar om te spugen/stoten)
            pts = [(b[0], b[1], b[2], 3.6 * hs), (b[0] + 9 * hs, b[1] + 6 * hs, b[2] + 2.5 * sz * hs, 3.2 * hs),
                   (b[0] + 16 * hs, b[1] + 9 * hs, b[2] + 1 * sz * hs, 2.2 * hs), (b[0] + 20 * hs, b[1] + 9 * hs, b[2] - 1 * sz * hs, 1.2 * hs)]
            m.chain(pts, 'ear', 0.8)
            m.ell((b[0] + 11 * hs, b[1] + 8.5 * hs, b[2] + 3.5 * sz * hs), np.array((4.6, 3.6, 3.6)) * hs, 'tassel')
        else:           # oren rechtop, de bombín ervoor
            pts = [(b[0], b[1], b[2], 3.6 * hs), (b[0] + 1 * hs, b[1] + 10 * hs, b[2] + 2.5 * sz * hs, 3.4 * hs),
                   (b[0] - 1 * hs, b[1] + 18 * hs, b[2] + 1 * sz * hs, 2.4 * hs), (b[0] - 3 * hs, b[1] + 22 * hs, b[2] - 2 * sz * hs, 1.2 * hs)]
            m.chain(pts, 'ear', 0.8)
    if fase == 3:
        hc = cr + np.array((2, 12.5, 0)) * hs
        m.ell(hc, np.array((10.5, 1.4, 10.5)) * hs, 'hat')
        m.ell(hc + np.array((0, 1.8, 0)) * hs, np.array((6.6, 1.6, 6.6)) * hs, 'hatband')
        m.ell(hc + np.array((0, 4.5, 0)) * hs, np.array((6.2, 5.6, 6.2)) * hs, 'hat')
        for dx in (-9, -6, -3):
            m.ell(cr + np.array((dx, 9, 0)) * hs, 2.6 * hs, 'pony')
        for sz in (1, -1):
            b = cr + np.array((6, 4, 9 * sz)) * hs
            pts = [b + np.array((2 * i * hs, -5.5 * i * hs, 0.6 * sz * i * hs)) for i in range(6)]
            for i, q in enumerate(pts):
                m.ell(q, np.array((3.4, 3.6, 3.4)) * hs * (1 - 0.04 * i), 'braid')
            m.ell(pts[-1] + np.array((0.5, -4.5, 0)) * hs, np.array((3, 4.2, 3)) * hs, 'tassel')
    Rh = P.rot_y(math.radians(head_extra))
    m.parts[h0:] = [(piv + Rh @ (c - piv), r, Rh @ R0, g) for c, r, R0, g in m.parts[h0:]]


def poot(m, pts, g, k, voet, x0=0):
    m.chain([(x, y, z, r * k) for x, y, z, r in pts], g)
    x, y, z = pts[-1][:3]
    if voet == 'mma':
        m.ell((x - 1, y - 2, z), np.array((11, 9, 10.5)) * k ** 0.6, 'glove')
        m.ell((x + 1, y + 7, z), np.array((8.5, 3.2, 8.5)) * k ** 0.6, 'strap')
        for dz in (-2.6, 2.6):
            m.ell((x - 11, y - 6.5, z + dz * 1.3), np.array((3.4, 2.6, 2.6)), 'nail')
    elif voet == 'wrap':
        m.ell((x - 2, y - 4, z), np.array((7, 3.8, 6)) * k ** 0.6, 'hoof')
        for j in range(4):
            m.ell((x + 0.5 + j * 0.6, y + 2 + j * 4.4, z), np.array((7.4, 2.6, 7.4)) * k, f'ag{j}')
    else:
        m.ell((x - 2, y - 4, z), np.array((6.5, 3.5, 5.5)) * k ** 0.6, 'hoof')


def halsband(m, a, b, t, rr, banden, pompons=0):
    """Leitmotif van de alpaca: aguayo-halsband (gestreepte ring loodrecht op de hals), eventueel met pompons eronder."""
    a, b = np.array(a, float), np.array(b, float)
    ax = (b - a) / np.linalg.norm(b - a)
    u = np.array((ax[1], -ax[0], 0.0)); v = np.array((0, 0, 1.0))
    for j, g in enumerate(banden):
        c = a + (b - a) * t + ax * (j - (len(banden) - 1) / 2) * 3.2
        for th in np.arange(0, 360, 9):
            q = math.radians(th)
            m.ell(c + rr * (math.cos(q) * u + math.sin(q) * v), np.array((2.6, 2.6, 2.6)), g)
    c = a + (b - a) * t - ax * (len(banden) / 2 * 3.2 + 2.5)
    for i, th in enumerate(np.linspace(-70, 70, pompons) if pompons else []):
        q = math.radians(th + 180)   # voorkant van de hals (naar -x)
        m.ell(c + (rr + 1) * (math.cos(q) * u + math.sin(q) * v), 3.3, ['pp_r', 'pp_y', 'pp_g', 'pp_p'][i % 4])


def tilt(m, i0, i1, piv, deg):
    Rt = P.rot_z(math.radians(deg))
    m.parts[i0:i1] = [(piv + Rt @ (c - piv), r, Rt @ R0, g) for c, r, R0, g in m.parts[i0:i1]]


def fase2_r2(hs=1.25):
    """Slungelige tiener in dekking."""
    m = P.Model()
    for c, r in (((-26, 4, 0), (19, 18, 16)), ((2, 4, 0), (30, 17, 16)), ((28, 6, 0), (18, 18, 16))):
        m.ell(c, r, 'body')
        fluff(m, c, r, 'body', 55, 7.5, int(abs(c[0])) + 11, ymin=-0.7)   # wilde plukken
    m.chain([(44, 12, 0, 6.5), (51, 22, 0, 7), (49, 31, 0, 5)], 'tail')
    n0 = len(m.parts)
    top = np.array((-44, 72, 0.0))
    nk = [(-30, 14, 0, 14), (-38, 44, 0, 11.5), (top[0], top[1], 0, 10)]
    m.chain(nk, 'neck')
    for i, (x, y, z, r) in enumerate(nk[1:]):
        fluff(m, (x, y, z), (r, r, r), 'neck', 22, 5.5, 60 + i)
    halsband(m, nk[0][:3], nk[1][:3], 0.32, 15.5, ['ag0', 'ag1', 'ag2'], pompons=5)
    kop(m, top, hs, 2, 24, np.array(nk[1][:3], float))
    tilt(m, n0, len(m.parts), np.array((-30, 14, 0.0)), 24)   # kop laag en naar voren
    # pomponsnoer en aguayo-bundel (lastdier, draagt zijn eigen spullen)
    for th in np.arange(-70, 71, 7):
        t = math.radians(th)
        band = int((th + 70) // 24) % len(AGUAYO)
        m.ell(np.array((4, 6 + 21 * math.cos(t), 20 * math.sin(t))), np.array((15, 3, 5)), f'ag{band}', P.rot_x(t))
    k = 1.05   # dunne, lange poten (grond op y = -70)
    poot(m, [(-30, -8, 11, 8), (-50, -24, 16, 6), (-56, -42, 18, 5.5)], 'leg', k, 'mma')        # nabije voor: in dekking
    poot(m, [(-18, -8, -11, 8), (-12, -40, -12, 6), (-10, -66, -12, 5.5)], 'far', k, 'mma')     # verre voor: draagt
    poot(m, [(30, -6, 11, 9.5), (40, -36, 12, 6), (34, -66, 12, 5.5)], 'leg', k, None)
    poot(m, [(36, -6, -11, 9.5), (46, -36, -12, 6), (42, -66, -12, 5.5)], 'far', k, None)
    return m


def fase3_r2(hs=1.2, voet='wrap'):
    """Zware kampioen, geworteld."""
    m = P.Model()
    for c, r in (((-26, 2, 0), (28, 29, 26)), ((4, 2, 0), (34, 25, 24)), ((34, 4, 0), (22, 25, 24))):
        m.ell(c, r, 'body')                                                   # geschoren: glad, geen plukken
    m.chain([(52, 14, 0, 6), (57, 22, 0, 6), (56, 28, 0, 4.5)], 'tail')
    n0 = len(m.parts)
    top = np.array((-44, 72, 0.0))
    nk = [(-34, 16, 0, 21), (-40, 44, 0, 16.5), (top[0], top[1], 0, 13.5)]   # korter en krachtig
    m.chain(nk, 'neck')
    halsband(m, nk[0][:3], nk[1][:3], 0.62, 19.5, ['ag3', 'ag0', 'ag1', 'ag2', 'ag0'], pompons=7)
    kop(m, top, hs, 3, 22, np.array(nk[1][:3], float))
    tilt(m, n0, len(m.parts), np.array((-34, 16, 0.0)), -8)                  # borst vooruit, kop hoog
    # manta = de halswol als omslagdoek (wolrand), pollera = de heupwol in drie ruches
    for th in np.arange(-100, 101, 8):
        t = math.radians(th)
        c = np.array((-24, 6 + 30 * math.cos(t), 28 * math.sin(t)))
        m.ell(c, np.array((15, 3.4, 6.5)), 'manta', P.rot_x(t))
        m.ell(c + np.array((-13, -2, 0)), np.array((4, 3.4, 5.5)), 'mantarand', P.rot_x(t))
    for j, (yy, ext) in enumerate(((0, 0), (-12, 3), (-24, 6))):
        for th in np.arange(0, 360, 7):
            t = math.radians(th)
            rr = 29 + ext
            m.ell(np.array((26 + rr * 0.9 * math.cos(t), yy, rr * math.sin(t))), np.array((7, 7.5, 7)), f'pol{j}')
    k = 1.6   # dikke poten, brede stand (grond op y = -66)
    poot(m, [(-30, -12, 16, 10), (-38, -40, 19, 7), (-40, -62, 20, 6.5)], 'leg', k, voet)
    poot(m, [(-18, -12, -16, 10), (-12, -40, -19, 7), (-8, -62, -20, 6.5)], 'far', k, voet)
    poot(m, [(34, -10, 16, 11), (42, -38, 19, 7), (38, -62, 20, 6.5)], 'leg', k, None)
    poot(m, [(40, -10, -16, 11), (48, -38, -19, 7), (46, -62, -20, 6.5)], 'far', k, None)
    return m


def lijn_r2():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    ref = os.path.join(HERE, '../referenties')
    W, base = 12 + 300 * 4, 380
    im = Image.new('RGB', (W, 420), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 10), 'Lama-lijn ronde 2: fase 2 slungelig in dekking, fase 3 zwaar en geworteld (op schaal)', font=FB, fill=(30, 30, 30))
    def plak(img, a, i, h, lab):
        bb = Image.fromarray((a * 255).astype(np.uint8)).resize(img.size).getbbox()
        img = img.crop(bb); k = h / img.height
        img = img.resize((max(1, int(img.width * k)), int(h)), Image.LANCZOS)
        im.paste(img, (12 + 300 * i + (300 - img.width) // 2, base - img.height))
        d.text((12 + 300 * i + 6, base + 12), lab, font=F, fill=(60, 60, 60))
    f1 = Image.open(os.path.join(ref, 'fase1_alpaca.png')).convert('RGBA')
    f1 = f1.crop(f1.getbbox()); k = 320 * 0.62 / f1.height
    f1 = f1.resize((int(f1.width * k), int(f1.height * k)), Image.NEAREST)
    bg = Image.new('RGBA', f1.size, 'white'); bg.alpha_composite(f1)
    im.paste(bg.convert('RGB'), (12 + (300 - f1.width) // 2, base - f1.height)); d.text((18, base + 12), 'fase 1: alpaca (af)', font=F, fill=(60, 60, 60))
    set_vacht('karamel (foto 1)'); m = fase2_r2(); img, a = view(m, 40)
    plak(img, a, 1, 320 * 0.8, f'fase 2: tiener, kop {kopaandeel(m, 40):.0%}')
    set_vacht('bont (foto 4)')
    for i, (voet, lab) in enumerate((('wrap', 'Y windsels'), ('mma', 'X MMA'))):
        m = fase3_r2(voet=voet); img, a = view(m, 40)
        plak(img, a, 2 + i, 320 * 1.0, f'fase 3{lab}: kampioen, kop {kopaandeel(m, 40):.0%}')
    im.save(os.path.join(HERE, 'lijn_ronde2.png'))


# ---------------------------------------------------------------- ronde 3 (Jordi 3 nov): de kop was "meer een paard dan een lama"
# Naar foto 1: kleine, smalle kop haaks op een kaarsrechte hals; snuit stomp en rond (geen taps paardenhoofd),
# geen donker snuitmasker; neus klein bovenaan de snuitpunt, hangende onderlip; oog hoog op de zijkant, groot,
# zwaar half gesloten bovenlid (droge blik); lange banaanoren; korte kuif. Hals en lijf ruig/fluffy.

COL.setdefault('lid', '#A86A3A'); COL.setdefault('lip', '#8A5530')
LINED.add('lid')


def kop_lama(m, top, hs, yaw_extra, piv, pitch=-8, lid=0.55, kleding=True):
    h0 = len(m.parts)
    cr = top + np.array((-4, 5, 0)) * hs                       # schedel: klein, smal (zijdelings platter)
    m.ell(cr, np.array((10, 9, 7.5)) * hs, 'head')
    fluff(m, cr + np.array((1, 7, 0)) * hs, np.array((6, 3, 6)) * hs, 'head', 8, 2.6 * hs, 3, ymin=0.3)   # korte kuif
    # gezicht: recht naar voren, blijft dik tot de punt (stomp), licht bol neusprofiel
    m.chain([(cr[0] - 6 * hs, cr[1] - 1 * hs, 0, 7.2 * hs), (cr[0] - 13 * hs, cr[1] - 2.5 * hs, 0, 6.4 * hs),
             (cr[0] - 18 * hs, cr[1] - 3.5 * hs, 0, 6.0 * hs)], 'head')
    m.ell(cr + np.array((-20.5, -4, 0)) * hs, np.array((4.6, 5.6, 5.4)) * hs, 'head')      # ronde snuitpunt
    m.ell(cr + np.array((-19, -9.2, 0)) * hs, np.array((4.2, 2.2, 4.0)) * hs, 'lip')        # hangende onderlip
    for sz in (1, -1):                                                                          # neusgaten: klein, boven-voor
        m.ell(cr + np.array((-23.6, -2.2, 2.0 * sz)) * hs, np.array((0.9, 1.4, 0.9)) * hs, 'nose')
    for sz in (1, -1):                                                                          # oog hoog op de zijkant
        e = cr + np.array((-3.5, 2.2, 6.6 * sz)) * hs
        m.ell(e, np.array((2.8, 2.6, 1.6)) * hs, 'eye')
        m.ell(e + np.array((-0.6, 0.4, 0.9 * sz)) * hs, 0.55 * hs, 'glint')
        # zwaar bovenlid: dekt de bovenste helft (droge blik)
        m.ell(e + np.array((0, 2.6 - 2.6 * lid, 0.35 * sz)) * hs, np.array((3.2, 1.6, 1.9)) * hs, 'lid')
    for sz in (1, -1):                                                                          # lange banaanoren
        b = cr + np.array((3, 7.5, 4.5 * sz)) * hs
        pts = [(b[0], b[1], b[2], 2.6 * hs), (b[0] + 0.5 * hs, b[1] + 8 * hs, b[2] + 2.6 * sz * hs, 2.7 * hs),
               (b[0] - 0.8 * hs, b[1] + 15 * hs, b[2] + 1.6 * sz * hs, 2.0 * hs), (b[0] - 2.6 * hs, b[1] + 19 * hs, b[2] - 1.2 * sz * hs, 1.0 * hs)]
        m.chain(pts, 'ear', 0.7)
        if kleding:
            m.ell((b[0] - 0.6 * hs, b[1] + 11 * hs, b[2] + 3.2 * sz * hs), np.array((2.8, 3.6, 2.8)) * hs, 'tassel')
    Rp = P.rot_z(math.radians(pitch))   # neus iets omlaag (foto 1)
    Ry = P.rot_y(math.radians(yaw_extra))
    m.parts[h0:] = [(piv + Ry @ (top + Rp @ (c - top) - piv), r, Ry @ Rp @ R0, g) for c, r, R0, g in m.parts[h0:]]


def fase2_r3(hs=1.45, neck=62, lid=0.55, bk=1.0, nr=0.0):
    """Fase 2 ronde 3: kaarsrechte ruige hals, lamakop, fluffy lijf; poten, kleding en pose als ronde 2.
    bk = lijf voller (wol), nr = hals dikker (wol)."""
    m = P.Model()
    for c, r in (((-26, 4, 0), (20, 19, 17)), ((2, 4, 0), (30, 18, 17)), ((28, 6, 0), (19, 19, 17))):
        r = (r[0] * bk ** 0.5, r[1] * bk, r[2] * bk)
        m.ell(c, r, 'body')
        fluff(m, c, r, 'body', 70, 6.5, int(abs(c[0])) + 11, ymin=-0.85)   # ruig, ook aan de buik
    m.chain([(44, 12, 0, 6.5), (51, 22, 0, 7.5), (49, 31, 0, 5.5)], 'tail')
    fluff(m, (50, 24, 0), (6, 8, 6), 'tail', 10, 3.2, 5)
    top = np.array((-36, 8 + neck, 0.0))
    nk = [(-32, 14, 0, 14.5 + nr), (-34, 8 + neck * 0.5, 0, 12.5 + nr), (top[0], top[1], 0, 11 + nr * 0.6)]   # kaarsrecht omhoog
    m.chain(nk, 'neck')
    for i, (x, y, z, r) in enumerate(nk):
        fluff(m, (x, y, z), (r, r, r), 'neck', 26, 5.2, 70 + i)
    halsband(m, nk[0][:3], nk[1][:3], 0.30, 16.5, ['ag0', 'ag1', 'ag2'], pompons=5)
    kop_lama(m, top, hs, 12, np.array(top, float), lid=lid)
    for th in np.arange(-70, 71, 7):   # aguayo-doek op de rug
        t = math.radians(th)
        band = int((th + 70) // 24) % len(AGUAYO)
        m.ell(np.array((4, 6 + 21.5 * math.cos(t), 20.5 * math.sin(t))), np.array((15, 3, 5)), f'ag{band}', P.rot_x(t))
    k = 1.05
    poot(m, [(-30, -8, 11, 8.5), (-50, -24, 16, 6), (-56, -42, 18, 5.5)], 'leg', k, 'mma')
    poot(m, [(-18, -8, -11, 8.5), (-12, -40, -12, 6), (-10, -66, -12, 5.5)], 'far', k, 'mma')
    poot(m, [(30, -6, 11, 10), (40, -36, 12, 6), (34, -66, 12, 5.5)], 'leg', k, None)
    poot(m, [(36, -6, -11, 10), (46, -36, -12, 6), (42, -66, -12, 5.5)], 'far', k, None)
    return m


def vel_r3():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    ref = os.path.join(HERE, '../referenties')
    set_vacht('karamel (foto 1)'); COL['lid'] = COL['head']; COL['lip'] = '#8A5530'
    cell = 262
    im = Image.new('RGB', (12 + cell * 4, 44 + (cell + 24) * 2), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), 'Lama fase 2, poppetje ronde 3: lamakop + kaarsrechte ruige hals (naar foto 1)', font=FB, fill=(30, 30, 30))
    foto = Image.open(os.path.join(ref, 'foto1_lama_driekwart_POSE.png')).convert('RGB')
    w, h = foto.size
    kopfoto = foto.crop((int(w * 0.18), int(h * 0.1), int(w * 0.55), int(h * 0.4)))
    panelen = [('foto 1', foto, None), ('oud (ronde 2): paard', None, fase2_r2(hs=1.18)),
               ('nieuw: lid half', None, fase2_r3(lid=0.55)), ('nieuw: lid zwaarder', None, fase2_r3(lid=0.7))]
    for i, (lab, img, m) in enumerate(panelen):
        x = 12 + cell * i
        if img is None:
            img, _ = view(m, 40)
        else:
            img = img.copy(); img.thumbnail((256, 256))
        im.paste(img, (x, 44)); d.text((x + 4, 44 + 258), lab, font=F, fill=(60, 60, 60))
        # kop-uitsnede
        if m is None:
            kz = kopfoto.copy(); kz.thumbnail((256, 256))
        else:
            big, _ = view(m, 40, size=236)
            bb = Image.fromarray((_ * 255).astype(np.uint8)).resize(big.size).getbbox(); kz = big.crop((bb[0] - 4, bb[1] - 4, bb[0] + 116, bb[1] + 116)).resize((256, 256), Image.LANCZOS)
        im.paste(kz, (x, 44 + cell + 24))
    im.save(os.path.join(HERE, 'vel_ronde3_kop.png'))


# ---------------------------------------------------------------- ronde 4 (Jordi 3 nov): dynamischere pose, wol gladder
# "geen fan van de pose. De poten lijken net gebroken. Kan je nadenken over een iets dynamischere pose? Kijk vooral naar
# andere sprites" + "nog steeds veel golvender dan bij de schapen". Posestudie: posestudie/gen3_viervoeters.png.

def _rot(m, i0, i1, piv, Rm):
    m.parts[i0:i1] = [(piv + Rm @ (c - piv), r, Rm @ R0, g) for c, r, R0, g in m.parts[i0:i1]]


POSES = {
    # A: Ponyta-steigerstap: nabije voorpoot hoog opgetrokken, knie naar voren, onderbeen hangt recht omlaag
    'A_stap': dict(rear=0, legs=[
        ('leg', [(-30, -8, 11, 8.5), (-46, -22, 15, 6), (-46, -42, 16, 5.5)], 'mma'),
        ('far', [(-18, -8, -11, 8.5), (-17, -38, -12, 6), (-18, -66, -12, 5.5)], 'mma'),
        ('leg', [(30, -6, 11, 10), (40, -36, 12, 6), (38, -66, 12, 5.5)], None),
        ('far', [(36, -6, -11, 10), (44, -36, -12, 6), (42, -66, -12, 5.5)], None)]),
    # B: steigeren (Stantler; lama's vechten echt zo): lijf 28 graden omhoog op de achterpoten, voorpoten in dekking
    'B_steigeren': dict(rear=36, legs=[
        ('leg', [(-30, -8, 11, 8.5), (-48, -8, 18, 6), (-62, 6, 20, 5.5)], 'mma'),
        ('far', [(-18, -8, -11, 8.5), (-38, -24, -15, 6), (-52, -30, -15, 5.5)], 'mma'),
        ('leg', [(30, -6, 11, 10), (16, -30, 13, 6.5), (24, -62, 13, 5.5)], None),
        ('far', [(36, -6, -11, 10), (32, -32, -13, 6.5), (42, -62, -13, 5.5)], None)]),
    # C: telgang (Girafarig; kameelachtigen lopen echt in telgang): nabije kant vooruit, verre kant achteruit
    'C_telgang': dict(rear=0, legs=[
        ('leg', [(-30, -8, 11, 8.5), (-40, -36, 12, 6), (-46, -66, 12, 5.5)], 'mma'),
        ('far', [(-18, -8, -11, 8.5), (-10, -36, -12, 6), (-4, -62, -12, 5.5)], 'mma'),
        ('leg', [(30, -6, 11, 10), (26, -36, 12, 6), (20, -66, 12, 5.5)], None),
        ('far', [(36, -6, -11, 10), (50, -34, -12, 6), (56, -60, -12, 5.5)], None)]),
    # D: achterwaartse trap (lama's trappen echt): nabije achterpoot schopt naar achteren, voorpoten gezet
    'D_trap': dict(rear=-6, legs=[
        ('leg', [(-30, -8, 11, 8.5), (-42, -36, 13, 6), (-48, -66, 13, 5.5)], 'mma'),
        ('far', [(-18, -8, -11, 8.5), (-22, -38, -12, 6), (-26, -66, -12, 5.5)], 'mma'),
        ('leg', [(30, -6, 11, 10), (52, -16, 12, 6.5), (70, -8, 12, 5.5)], None),
        ('far', [(36, -6, -11, 10), (40, -36, -12, 6), (36, -66, -12, 5.5)], None)]),
    # ronde 5 (Jordi 3 nov, foto 8): lijf horizontaal (bijna zijaanzicht, Manectric/Rapidash/Umbreon), kop driekwart
    # naar de kijker; alle poten op de grond (Girafarig/Ponyta), geen opgetilde poot.
    'E_staand': dict(rear=0, legs=[
        ('leg', [(-30, -8, 11, 8.5), (-34, -36, 12, 6), (-36, -66, 12, 5.5)], 'mma'),
        ('far', [(-20, -8, -11, 8.5), (-22, -36, -12, 6), (-24, -66, -12, 5.5)], 'mma'),
        ('leg', [(30, -6, 11, 10), (38, -36, 12, 6), (34, -66, 12, 5.5)], None),
        ('far', [(38, -6, -11, 10), (46, -36, -12, 6), (44, -66, -12, 5.5)], None)]),
    'F_pas': dict(rear=0, legs=[    # Girafarig: nabije voor iets vooruit, verre voor recht; achter gespreid
        ('leg', [(-30, -8, 11, 8.5), (-38, -36, 12, 6), (-44, -66, 12, 5.5)], 'mma'),
        ('far', [(-20, -8, -11, 8.5), (-18, -36, -12, 6), (-16, -66, -12, 5.5)], 'mma'),
        ('leg', [(30, -6, 11, 10), (40, -36, 12, 6), (40, -66, 12, 5.5)], None),
        ('far', [(38, -6, -11, 10), (44, -36, -12, 6), (50, -64, -12, 5.5)], None)]),
    'G_ponyta': dict(rear=0, legs=[  # Ponyta: voorpoten bijna samen en recht, verre achterpoot op de punt naar achteren
        ('leg', [(-30, -8, 11, 8.5), (-33, -36, 12, 6), (-35, -66, 12, 5.5)], 'mma'),
        ('far', [(-22, -8, -11, 8.5), (-26, -36, -12, 6), (-28, -66, -12, 5.5)], 'mma'),
        ('leg', [(30, -6, 11, 10), (36, -36, 12, 6), (32, -66, 12, 5.5)], None),
        ('far', [(38, -6, -11, 10), (52, -32, -12, 6), (58, -62, -12, 5.5)], None)]),
}


def fase2_r4(pose='A_stap', hs=1.45, neck=52, lid=0.55, bk=1.2, nr=2, head_yaw=12):
    """Fase 2 ronde 4: kop/hals/kleding als ronde 3, gladdere wol (minder, grotere bobbels), pose uit POSES."""
    m = P.Model()
    lx = 1.15 if pose in ('E_staand', 'F_pas', 'G_ponyta') else 1.0   # ronde 5: langer lijf (foto 8)
    for c, r in (((-26, 4, 0), (20, 19, 17)), ((2, 4, 0), (30, 18, 17)), ((28, 6, 0), (19, 19, 17))):
        c = (c[0] * lx, c[1], c[2]); r = (r[0] * bk ** 0.5 * lx, r[1] * bk, r[2] * bk)
        m.ell(c, r, 'body')
        fluff(m, c, r, 'body', 16, 9.5, int(abs(c[0])) + 11, ymin=-0.85)   # weinig, groot: glad zoals Mareep
    m.chain([(44, 12, 0, 6.5), (51, 22, 0, 7.5), (49, 31, 0, 5.5)], 'tail')
    m.ell((50, 30, 0), 7.5, 'tail')
    top = np.array((-36, 8 + neck, 0.0))
    nk = [(-32, 14, 0, 14.5 + nr), (-34, 8 + neck * 0.5, 0, 12.5 + nr), (top[0], top[1], 0, 11 + nr * 0.6)]
    h0 = len(m.parts)
    m.chain(nk, 'neck')
    for i, (x, y, z, r) in enumerate(nk):
        fluff(m, (x, y, z), (r, r, r), 'neck', 7, 7.5, 70 + i)
    halsband(m, nk[0][:3], nk[1][:3], 0.30, 16.5 + nr, ['ag0', 'ag1', 'ag2'], pompons=5)
    kop_lama(m, top, hs, head_yaw, np.array(top, float), lid=lid)
    h1 = len(m.parts)
    for th in np.arange(-70, 71, 7):
        t = math.radians(th)
        band = int((th + 70) // 24) % len(AGUAYO)
        m.ell(np.array((4, 6 + 21.5 * bk * math.cos(t), 20.5 * bk * math.sin(t))), np.array((15, 3, 5)), f'ag{band}', P.rot_x(t))
    pz = POSES[pose]
    n_lijf = len(m.parts)
    for g, pts, voet in pz['legs'][:2]:     # voorpoten draaien mee met het lijf
        poot(m, pts, g, 1.05, voet)
    if pz['rear']:
        _rot(m, 0, len(m.parts), np.array((32, -6, 0.0)), P.rot_z(math.radians(-pz['rear'])))
        # hals blijft kaarsrecht omhoog: kop+hals terugdraaien om de (gedraaide) halsbasis
        piv = np.array((32, -6, 0.0)) + P.rot_z(math.radians(-pz['rear'])) @ (np.array(nk[0][:3], float) - np.array((32, -6, 0.0)))
        _rot(m, h0, h1, piv, P.rot_z(math.radians(pz['rear'])))
    for g, pts, voet in pz['legs'][2:]:
        poot(m, pts, g, 1.05, voet)
    return m


def vel_r4():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    set_vacht('karamel (foto 1)'); COL['lid'] = COL['head']; COL['lip'] = '#8A5530'
    labels = {'A_stap': 'A: steigerstap (Ponyta)', 'B_steigeren': 'B: steigeren in dekking (Stantler)',
              'C_telgang': 'C: telgang (Girafarig)', 'D_trap': 'D: trap naar achteren (lama-gedrag)'}
    cell = 262
    im = Image.new('RGB', (12 + cell * 5, 44 + cell + 30), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), 'Lama fase 2, poppetje ronde 4: pose-opties (kop, hals en kleding als ronde 3)', font=FB, fill=(30, 30, 30))
    oud, _ = view(fase2_r3(neck=52, bk=1.2, nr=2), 40)
    im.paste(oud, (12, 44)); d.text((16, 44 + 258), 'nu: "gebroken" poot', font=F, fill=(60, 60, 60))
    for i, k in enumerate(POSES):
        img, _ = view(fase2_r4(k), 40)
        im.paste(img, (12 + cell * (i + 1), 44)); d.text((16 + cell * (i + 1), 44 + 258), labels[k], font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, 'vel_ronde4_pose.png'))


def vel_r5():
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    set_vacht('karamel (foto 1)'); COL['lid'] = COL['head']; COL['lip'] = '#8A5530'
    ref = os.path.join(HERE, '../referenties')
    cell = 262
    opts = [('E_staand', 8, 55, 'E: staand, lijf 8°, kop +55°'), ('F_pas', 8, 55, 'F: pas (Girafarig), lijf 8°'),
            ('G_ponyta', 8, 55, 'G: Ponyta-stand, lijf 8°'), ('F_pas', 20, 45, 'F2: pas, lijf 20°, kop +45°')]
    im = Image.new('RGB', (12 + cell * 5, 44 + cell + 30), 'white'); d = ImageDraw.Draw(im)
    d.text((12, 12), 'Lama fase 2, poppetje ronde 5: lijf horizontaal, kop driekwart naar je toe (foto 8)', font=FB, fill=(30, 30, 30))
    foto = Image.open(os.path.join(ref, 'foto8_lama_zij_kop_driekwart_POSE.webp')).convert('RGB'); foto.thumbnail((256, 256))
    im.paste(foto, (12, 44 + (256 - foto.height) // 2)); d.text((16, 44 + 258), 'foto 8 (Jordi)', font=F, fill=(60, 60, 60))
    for i, (k, yaw, hy, lab) in enumerate(opts):
        img, _ = view(fase2_r4(k, head_yaw=hy), yaw)
        im.paste(img, (12 + cell * (i + 1), 44)); d.text((16 + cell * (i + 1), 44 + 258), lab, font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, 'vel_ronde5_pose.png'))


if __name__ == '__main__':
    vel()
    lijn()
    lijn_r2()
    vel_r3()
