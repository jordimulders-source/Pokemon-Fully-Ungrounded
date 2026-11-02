"""Nachtaap fase 2: 3D-poppetje in de Lairon-pose (laag gehurkt, rug boven de kop, kop recht naar de kijker).
Werkwijze: SPRITE_WERKWIJZE stap 1 (poppetje -> raster van hoeken -> Jordi kiest -> silhouet).
Diercoördinaten: x = naar achteren, y = omhoog, z = naar de kijker bij 0° (profiel naar links).
Draaien vanuit de repo-root: python3 docs/concept/sprites/nachtaap_evo/pop3d/nachtaap3d.py"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pop3d as P  # noqa: E402

P.COL = {
    'fur': '#5E4488', 'arm': '#5E4488', 'far': '#45306A', 'head': '#5E4488', 'disc': '#7C66A6', 'ring': '#2E2048', 'moon': '#FFFFFF',
    'stripe': '#3A2858', 'eye': '#E0508A', 'pupil': '#1A1020', 'glint': '#FFFFFF', 'nose': '#8A6070',
    'hand': '#EAD8BE', 'buik': '#E9A866', 'maan': '#D8D0EC', 'farhand': '#B8A48C', 'ear': '#523A7A', 'earin': '#E2C4BC',
}
P.NOSHADE = {'ring', 'disc', 'moon', 'stripe', 'eye', 'pupil', 'glint', 'nose'}
P.LINED = {'eye', 'nose'}

HEAD_C = np.array((-46.0, 6.0, 0.0))
HEAD_R = 24.0
SPIR_R = 15.0


def nachtaap(head_extra=30, tail='omlaag', motief=None, cam=(40, 8)):
    m = P.Model()
    # lijf: borst/schouders, hoge gebogen rug (hoger dan de kop), achterwerk
    m.ell((-16, 8, 0), 24, 'fur')
    m.ell((8, 22, 0), (36, 28, 28), 'fur', P.rot_z(math.radians(-6)))
    m.ell((34, 8, 0), (27, 26, 26), 'fur')
    m.ell((-4, -6, 0), (24, 18, 22), 'fur')   # buik/borst onder, sluit aan bij de armen
    # staart
    if tail == 'omlaag':
        path = P.qb((56, 4, 0), (74, -10, 0), (70, -20, 0), 9)
        c = np.array((80.0, -20.0, 0.0)); a0 = math.pi
    else:  # omhoog achter de rug
        path = P.qb((54, 18, 0), (84, 30, 0), (78, 62, 0), 9)
        c = np.array((93.0, 62.0, 0.0)); a0 = math.pi
    spir = []
    for i in range(44):
        t = i / 43
        a = a0 - t * 1.6 * 2 * math.pi
        rr = SPIR_R * (1 - 0.75 * t)
        spir.append((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a), 0))
    pts = path[:-1] + spir
    n = len(pts)
    m.chain([(x, y, z, 6.5 - 3.3 * i / (n - 1)) for i, (x, y, z) in enumerate(pts)], 'fur')
    # armen (nabij +z): lang en dun, handen plat voor het lijf met lange vingers
    for sz, g, gh in ((1, 'arm', 'hand'), (-1, 'far', 'farhand')):
        dx = 0 if sz > 0 else 8
        m.chain([(-20 + dx, 4, 15 * sz, 9.5), (-26 + dx, -10, 18 * sz, 8), (-32 + dx, -21, 19 * sz, 6.5)], g)
        m.ell((-37 + dx, -25, 19 * sz), (9, 4, 7.5), gh)
        for k in (-5, -1.7, 1.7, 5):
            m.chain([(-42 + dx, -25, 19 * sz + k, 2.3), (-50 + dx, -27.5, 19 * sz + k * 1.3, 1.9)], gh, 0.8)
    # achterpoten gehurkt: dij, knie naar voren, voet plat
    for sz, g, gh in ((1, 'fur', 'hand'), (-1, 'far', 'farhand')):
        m.chain([(32, 2, 19 * sz, 18), (12, -8, 24 * sz, 12), (24, -21, 23 * sz, 8)], g)
        m.ell((14, -26, 23 * sz), (12, 4, 7), gh)
    # kop: rond, laag en vooraan; draait extra naar de kijker rond de nek
    pv = np.array((-30.0, 10.0, 0.0))
    Rh = P.rot_y(math.radians(head_extra))
    Hp = lambda p: pv + Rh @ (np.array(p, float) - pv)
    hc = Hp(HEAD_C)
    m.ell(hc, (HEAD_R, HEAD_R * 0.96, HEAD_R), 'head', Rh)
    fwd = np.array((-1.0, 0, 0))
    m.ell(Hp(HEAD_C + np.array((-HEAD_R * 0.86, -HEAD_R * 0.36, 0))), (7, 6, 8), 'disc', Rh)   # snoetje
    m.ell(Hp(HEAD_C + np.array((-HEAD_R * 0.98, -HEAD_R * 0.30, 0))), (2.6, 2.0, 3.2), 'nose', Rh)
    eyes = []
    for sz in (1, -1):
        d = np.array((-0.84, 0.06, 0.40 * sz)); d /= np.linalg.norm(d)
        e = HEAD_C + d * HEAD_R * 0.93
        eyes.append(e)
        m.ell(Hp(e), 6.8, 'eye')
        m.ell(Hp(e + d * 2.6), 3.9, 'pupil')
        m.ell(Hp(e + d * 4.2 + np.array((0, 2.4, -1.2 * sz))), 1.3, 'glint')
    for sz in (1, -1):   # kleine ronde oren aan de zijkant
        c = Hp(HEAD_C + np.array((2, 12, 21 * sz)))
        m.ell(c, (5, 8, 4), 'ear', Rh)
        m.ell(c + Rh @ np.array((-1.5, 0, 1.6 * sz)), (3.2, 5.5, 2.6), 'earin', Rh)

    def texfn(q, groups):
        ql = (q - pv) @ Rh + pv     # terug naar ongedraaide kopcoördinaten (Rh^T)
        u = (ql - HEAD_C) / HEAD_R
        g = np.full(len(q), groups.index('head'))
        # Jordi 2 nov (krabbel referenties/jordi_krabbel_halvemaan.png): het enige witte op de kop is één grote
        # halve maan die de helft van de kop bedekt en over de ogen heen valt, punten omlaag.
        # Ontworpen in het gezichtsvlak (z, y) van de voorkant: buitencirkel min een lagere binnencirkel.
        # Halve maan als echte 3D-tekening op de kop, spiegelsymmetrisch om het middenvlak z = 0 van de kop.
        # Ontworpen in bolcoördinaten rond de kijkas van het gezicht (-x): lon = hoek opzij, lat = hoek omhoog.
        lon = np.degrees(np.arctan2(u[:, 2], -u[:, 0]))
        lat = np.degrees(np.arcsin(np.clip(u[:, 1], -1, 1)))
        # buitenboog: door de kruin (lat 90) en de punten (lon ±56, lat -12); binnenboog: door het voorhoofd
        # (lat 15) en dezelfde punten, en over de bovenkant van de ogen (lon ±25 -> lat ±10). Ogen: lon ±25°, lat 3°.
        a1 = np.hypot(lon, lat - 23.6)
        a2 = np.hypot(lon, lat + 48.6)
        g[(a1 < 66.4) & (a2 > 63.6) & (np.abs(lon) < 95)] = groups.index('moon')
        for e in eyes:
            ue = (e - HEAD_C) / HEAD_R
            g[np.linalg.norm(u - ue, axis=1) < 0.33] = groups.index('ring')
        return g

    m.texfn = texfn

    def bodyfn(q, groups):
        g = np.full(len(q), groups.index('fur'))
        x, y, z = q[:, 0], q[:, 1], q[:, 2]
        if motief == 'buik':
            # oranje borst/buik zoals de echte nachtaap (foto 4), voorkant onder de kop
            g[(x < 4) & (y < 12) & (z > -14) & (x + 0.6 * y < 2)] = groups.index('buik')
        # patroon in 'uitgerolde' rugcoördinaten: x langs de ruggengraat, sa = booglengte vanaf de rugmiddenlijn
        # (z = 0 bovenop). Daardoor is het van bovenaf gecentreerd en loopt het langs de flanken omlaag.
        th = np.arctan2(z, y - 6)
        sa = th * 30
        top = np.abs(th) < 1.45
        if motief == 'kene':
            # Shipibo-kené: lijn over de ruggengraat + getrapte dwarsbanden die over beide flanken omlaag lopen
            k = (np.abs(sa) < 2.8) & (x > -16) & (x < 52)
            for xa in (-6, 16, 38):
                k |= (np.abs(x - xa) < 2.8) & (np.abs(sa) < 17)
                k |= (np.abs(np.abs(sa) - 17) < 2.8) & (x > xa - 0.5) & (x < xa + 8.5)
                k |= (np.abs(x - xa - 8) < 2.8) & (np.abs(sa) > 15) & (np.abs(sa) < 36)
            g[top & k] = groups.index('maan')
        if motief == 'chakana':
            # Andeskruis (chakana) midden op de rug, getrapt, met een rond gat; armen lopen over de flanken
            dx, dz = np.abs(x - 14), np.abs(sa)
            inside = lambda w: ((dx < 24 - w) & (dz < 9 - w)) | ((dx < 16.5 - w) & (dz < 22 - w)) | ((dx < 9 - w) & (dz < 34 - w))
            ring = inside(0) & ~inside(3.6)
            rr = np.hypot(x - 14, sa)
            ring |= (rr < 7) & (rr > 3.5)
            g[top & ring] = groups.index('maan')
        return g

    m.bodyfn = bodyfn
    return m


def grid(yaws=(30, 40, 50), extras=(25, 40), pitch=8, tail='omlaag', name='hoeken.png'):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
    W = 10 + 266 * len(yaws)
    im = Image.new('RGB', (W, 40 + (256 + 26) * len(extras)), 'white')
    d = ImageDraw.Draw(im)
    d.text((10, 10), f'Nachtaap fase 2: 3D-poppetje (Lairon-pose), staart {tail}', font=FB, fill=(30, 30, 30))
    for j, ex in enumerate(extras):
        for i, yaw in enumerate(yaws):
            v = P.view(nachtaap(ex, tail), yaw, pitch)
            x, y = 10 + 266 * i, 40 + (256 + 26) * j
            im.paste(v, (x, y))
            d.text((x, y + 258), f'lijf {yaw}°, kop {yaw + ex}°', font=F, fill=(60, 60, 60))
    im.save(os.path.join(HERE, name))


if __name__ == '__main__':
    grid()
