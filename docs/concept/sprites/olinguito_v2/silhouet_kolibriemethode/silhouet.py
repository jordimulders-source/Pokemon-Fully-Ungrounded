"""Olinguito v2: silhouet met de kolibriemethode (25 okt).
Het 3D-poppetje (pop3d.py, Jordi's gekozen ontwerp op 52°) is de onderlaag, niet de bron om te verkleinen.
Eerst 'sprite-proof' (Pokémon-verhoudingen): dikkere poten, grotere klauwen, verre poten iets los;
dan per onderdeel naar 64x64 met een minimale dikte, zodat dunne delen op 1x blijven lezen."""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pop3d as P

HERE = os.path.dirname(os.path.abspath(__file__))
YAW, PITCH, BOX = 40, 8, 64
HEAD_EXTRA, TILT = 9, 8   # B2 (Jordi, 25 okt)


def olinguito_sprite(leg_k=1.45, claw_k=1.9, far_dx=6, legs=True, head_extra=0, tilt=0):
    """Kopie van pop3d.olinguito() met spriteverhoudingen; alleen poten/klauwen anders."""
    m = P.Model()
    L = lambda pts: [(x, y, z, r * leg_k) for x, y, z, r in pts]
    m.ell((-30, 0, 0), 26, 'fur')
    m.ell((2, 6, 0), (34, 24, 23), 'fur', P.rot_z(math.radians(8)))
    m.ell((34, 12, 0), 25, 'fur')
    tail = P.qb((52, 18, 0), (88, 22, 0), (84, 74, 0), 10)[:-1] + P.qb((84, 74, 0), (80, 116, 0), (48, 110, 0), 8)[:-1] \
        + P.qb((48, 110, 0), (22, 104, 0), (26, 84, 0), 6)
    n = len(tail)
    m.chain([(x, y, z, 10.5 - 5 * i / (n - 1)) for i, (x, y, z) in enumerate(tail)], 'fur')
    hs, piv = P.HEAD_SCALE, np.array((-46, -2, 0.0))
    H = lambda p: piv + (np.array(p, float) - piv) * hs + P.HEAD_SHIFT
    m.chain([(-36, 0, 0, 22), tuple(piv + P.HEAD_SHIFT) + (20,)], 'fur')
    h0 = len(m.parts)
    cr = H((-64, -6, 0))
    m.ell(cr, np.array((25, 28, 25)) * hs, 'head')
    m.chain([tuple(H(q[:3])) + (q[3] * hs,) for q in [(-76, -16, 0, 20), (-88, -22, 0, 14.5), (-98, -28, 0, 9.5)]], 'head')
    nose = H((-105, -31, 0))
    m.ell(nose, 6.0 * hs, 'nose')
    eyes = []
    for sz in (1, -1):
        d = np.array((-0.70, -0.28, 0.66 * sz)); d /= np.linalg.norm(d)
        e = cr + d * 23.5 * hs
        eyes.append(e)
        m.ell(e, 4.4 * hs, 'eye')
    arc = []
    for t in np.linspace(-1.3, 1.3, 53):
        d = np.array((-0.72, -0.10, 0.69 * t)); d /= np.linalg.norm(d)
        arc.append(cr + d * 26.5 * hs)
    m.tex = dict(cr=cr, eyes=eyes, arc=np.array(arc), nose=nose, hs=hs)
    for sz in (1, -1):
        Re = P.rot_y(math.radians(25 if sz > 0 else 0))
        c = H((-58, 16, 13 * sz))
        k = 1.0 if sz > 0 else 0.6
        m.ell(c, np.array((4, 12, 11)) * hs * k, 'ear', Re)
    if head_extra:
        # kop draait meer naar de kijker dan het lijf (Pokémon-regel): kopdelen extra draaien rond de nek
        pv = piv + P.HEAD_SHIFT; Rh = P.rot_y(math.radians(head_extra))
        m.parts[h0:] = [(pv + Rh @ (c - pv), r, Rh @ R0, g) for c, r, R0, g in m.parts[h0:]]
        t = m.tex
        rot = lambda p: pv + Rh @ (np.array(p) - pv)
        m.tex = dict(cr=rot(t['cr']), eyes=[rot(e) for e in t['eyes']], arc=np.array([rot(a) for a in t['arc']]), nose=rot(t['nose']), hs=t['hs'])
    if not legs:
        return _tilt(m, tilt)
    # poten: dikker (leg_k); verre poten far_dx naar achteren zodat er lucht tussen nabij en ver komt
    m.chain(L([(-34, -2, 13, 16), (-48, -28, 15, 11.5), (-62, -52, 17, 9)]), 'fur')
    m.ell((-66, -55, 18), np.array((10, 6, 8)) * leg_k ** 0.5, 'paw')
    for dz in (-4.5, 4.5):   # 2 lange Linoone-klauwen, groter (claw_k)
        m.chain([(-72, -57, 18 + dz, 3.6 * claw_k), (-82, -68, 18 + dz, 2.6 * claw_k), (-85, -82, 18 + dz, 1.0 * claw_k)], 'claw', 0.8)
    fx = far_dx
    m.chain(L([(-28 + fx, -2, -13, 14), (-20 + fx, -28, -15, 11), (-34 + fx, -42, -17, 8.5)]), 'far')
    m.ell((-38 + fx, -45, -17), np.array((9, 6, 7.5)) * leg_k ** 0.5, 'farpaw')
    for dz in (-4, 4):
        m.chain([(-44 + fx, -48, -17 + dz, 3.2 * claw_k), (-51 + fx, -58, -17 + dz, 2.2 * claw_k), (-53 + fx, -69, -17 + dz, 0.9 * claw_k)], 'claw', 0.8)
    m.chain(L([(30, 10, 18, 20), (6, -20, 21, 13), (30, -42, 21, 9)]), 'fur')
    m.chain(L([(30, -42, 21, 7.5), (10, -48, 22, 6.5)]), 'paw')
    m.chain(L([(36 + fx, 12, -17, 18), (18 + fx, -16, -19, 11.5), (40 + fx, -36, -19, 8.5)]), 'far')
    m.chain(L([(40 + fx, -36, -19, 7), (24 + fx, -42, -20, 6)]), 'farpaw')
    return _tilt(m, tilt)


def _tilt(m, tilt):
    """Hele poppetje kantelen in het beeldvlak: positief = kop omhoog (Jordi: 'ietsje meer naar boven')."""
    if not tilt:
        return m
    Rt = P.rot_z(math.radians(-tilt))
    m.parts = [(Rt @ c, r, Rt @ R0, g) for c, r, R0, g in m.parts]
    t = m.tex
    m.tex = dict(cr=Rt @ t['cr'], eyes=[Rt @ e for e in t['eyes']], arc=np.array([Rt @ a for a in t['arc']]), nose=Rt @ t['nose'], hs=t['hs'])
    return m


def gid_render(m, fill=0.86):
    x0, x1, y0, y1 = P.bbox(m, YAW, PITCH)
    scale = P.R * fill / max(x1 - x0, y1 - y0)
    zbuf, gid, nrm, groups = P.render(m, YAW, PITCH, scale, ((x0 + x1) / 2, (y0 + y1) / 2))
    return gid, groups


def to64(gid, groups, thin=('claw',), min_px=1.6):
    """Per onderdeel naar 64: dunne delen eerst 'opblazen' tot min_px sprite-pixels, dan samen tellen."""
    R = gid.shape[0]; k = R // BOX
    alls = gid >= 0
    m = np.array(Image.fromarray((alls * 255).astype(np.uint8)).resize((BOX, BOX), Image.BOX)) > 110
    for g in thin:
        tm = gid == groups.index(g)
        big = Image.fromarray((tm * 255).astype(np.uint8))
        r = int(k * min_px / 2)
        from PIL import ImageFilter
        big = big.filter(ImageFilter.MaxFilter(2 * r + 1))
        m |= np.array(big.resize((BOX, BOX), Image.BOX)) > 90
    near = np.isin(gid, [groups.index(g) for g in groups if g not in ('far', 'farpaw')])
    far = np.array(Image.fromarray((np.isin(gid, [groups.index('far'), groups.index('farpaw')]) * 255).astype(np.uint8)).resize((BOX, BOX), Image.BOX)) > 140
    return m, far & m


# Skelet uit het ontwerp (zelfde punten als pop3d.olinguito, ongewijzigd), per poot: (schouder/heup, knie, voet, klauwpunt)
LEGS = {
    'far_hind':  ([(36, 12, -17), (18, -16, -19), (40, -36, -19), (24, -42, -20)], (6.0, 4.6, 4.0)),
    'far_front': ([(-28, -2, -13), (-20, -28, -15), (-34, -42, -17), (-38, -45, -17)], (5.5, 4.4, 4.0)),
    'near_hind': ([(30, 10, 18), (6, -20, 21), (30, -42, 21), (10, -48, 22)], (8.0, 5.6, 4.8)),
    'near_front': ([(-34, -2, 13), (-48, -28, 15), (-62, -52, 17), (-66, -55, 18)], (7.0, 5.6, 5.0)),
}
CLAWS = {'far_front': [(-44, -48, -17), (-51, -66, -17)], 'near_front': [(-72, -57, 18), (-82, -78, 18)]}


def projector(m, fill=0.86):
    x0, x1, y0, y1 = P.bbox(m, YAW, PITCH)
    scale = P.R * fill / max(x1 - x0, y1 - y0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    Rc = P.rot_x(math.radians(PITCH)) @ P.rot_y(math.radians(YAW))
    Rt = P.rot_z(math.radians(-TILT))
    def proj(p):
        q = Rc @ (Rt @ np.array(p, float))
        return ((q[0] - cx) * scale + P.R / 2) * BOX / P.R, (-(q[1] - cy) * scale + P.R / 2) * BOX / P.R
    return proj, scale, (cx, cy)


def build_v2():
    """Romp/kop/staart als render (die lezen al goed), poten en klauwen met de hand getekend op
    het geprojecteerde skelet, met minimale spritedikten en lucht tussen de poten."""
    from silhouet_tekenen import tube_mask
    full = olinguito_sprite(1.0, 1.0, 0, head_extra=HEAD_EXTRA, tilt=TILT)
    proj, scale, c = projector(full)
    torso = olinguito_sprite(1.0, 1.0, 0, legs=False, head_extra=HEAD_EXTRA, tilt=TILT)
    zbuf, gid, nrm, groups = P.render(torso, YAW, PITCH, scale, c)
    body = np.array(Image.fromarray(((gid >= 0) * 255).astype(np.uint8)).resize((BOX, BOX), Image.BOX)) > 110
    layers = {}
    for name, (pts, (w0, w1, w2)) in LEGS.items():
        sp = [proj(p) for p in pts]
        mm = tube_mask([sp[0], sp[1]], w0, w1) | tube_mask([sp[1], sp[2]], w1, w2) | tube_mask([sp[2], sp[3]], w2, w2 * 0.9)
        if name in CLAWS:
            a, b = [proj(p) for p in CLAWS[name]]
            dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
            for off in (-1.3, 1.3):
                # klauw: dicht driehoekje (basis 2 px, punt), uit elkaar zodat er 2 lezen
                mm |= tube_mask([(a[0] + nx * off, a[1] + ny * off), (b[0] + nx * off * 1.6, b[1] + ny * off * 1.6)], 2.2, 0.6)
        layers[name] = mm
    # oor: dominant oor als duidelijke ronde bult op de kruin (in de render valt hij op 64 weg)
    hs, piv = P.HEAD_SCALE, np.array((-46, -2, 0.0))
    pv = piv + P.HEAD_SHIFT
    ear = piv + (np.array((-58, 16, 13.0)) - piv) * hs + P.HEAD_SHIFT
    ear = pv + P.rot_y(math.radians(HEAD_EXTRA)) @ (ear - pv)
    ex, ey = proj(ear)
    body |= tube_mask([(ex, ey + 1.5), (ex, ey - 1.2)], 5.2, 4.6)
    return body, layers


if __name__ == '__main__':
    body, layers = build_v2()
    far = layers['far_hind'] | layers['far_front']
    m = body | far | layers['near_hind'] | layers['near_front']
    far = far & ~(layers['near_hind'] | layers['near_front'] | body)
    # vel: ontwerp | oud silhouet | nieuw silhouet (1 kleur) | nieuw met verre poten lichter | 1x
    sil = np.zeros((64, 64, 4), np.uint8); sil[m] = (40, 32, 44, 255)
    two = sil.copy(); two[far] = (110, 100, 116, 255)
    S, T = Image.fromarray(sil), Image.fromarray(two)
    S.save(os.path.join(HERE, 'silhouet_1x.png')); T.save(os.path.join(HERE, 'silhouet_tweekleur_1x.png'))
    oud = Image.open(os.path.join(HERE, 'oud_silhouet_950.png')).convert('RGB')
    ont = P.view(olinguito_sprite(1.0, 1.0, 0, head_extra=HEAD_EXTRA, tilt=TILT), YAW, PITCH)
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    W = Image.new('RGB', (4 * 266 + 10, 256 + 120), (236, 236, 230)); d = ImageDraw.Draw(W)
    W.paste(ont, (5, 5))
    for i, im in enumerate((oud, S, T)):
        big = im.convert('RGBA').resize((256, 256), Image.NEAREST); W.paste(big, (5 + 266 * (i + 1), 5), big)
    for i, im in enumerate((oud, S)):
        s = im.convert('RGBA'); W.paste(s, (5 + 266 * (i + 1), 290), s)
    for x, t in ((5, 'B2: poppetje lijf 40°, kop 49°, kantel 8°'), (271, 'oud silhouet (verkleinde render)'), (537, 'nieuw: sprite-proof, 1 kleur'), (803, 'nieuw: verre poten lichter')):
        d.text((x, 265), t, fill='black', font=F)
    d.text((271 + 70, 300), '1x oud', fill='black', font=F); d.text((537 + 70, 300), '1x nieuw  (%d px)' % m.sum(), fill='black', font=F)
    W.save(os.path.join(HERE, 'vel_b2.png'))
    ov = P.view(olinguito_sprite(1.0, 1.0, 0, head_extra=HEAD_EXTRA, tilt=TILT), YAW, PITCH, size=256 * 0.86).convert('RGBA')
    ov.putalpha(90); o = Image.new('RGBA', (256, 256), (255, 255, 255, 255)); o.alpha_composite(S.convert('RGBA').resize((256, 256), Image.NEAREST)); o.alpha_composite(ov); o.save(os.path.join(HERE, 'overlay_b2.png'))
    print('px', m.sum())
