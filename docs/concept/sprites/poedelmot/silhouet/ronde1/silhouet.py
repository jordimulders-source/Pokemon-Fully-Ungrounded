"""Poedelmot (eindvorm), stap 3 ronde 1: silhouet uit de tak-foto (pose P1, Jordi 5 nov).
Kolibrie-/wasbeermethode: omtrek punt voor punt in fotocoördinaten (referenties/foto_tak_katoen.webp, 1500x1500),
per onderdeel apart, zodat de handaanpassingen uit de SPEC los te zien en te verschuiven zijn:
  - lijf/kop (wol) en poten: uit de foto (massa is heilig), alleen een wollige plukjesrand erop;
  - pootuiteinden: pompons van de poedelknip (iets groter dan op de foto);
  - voorvleugels: uit de foto (links schuin, rechts omhoog = de V), iets breder zodat ze op 1x lezen;
  - achtervleugels: met de hand toegevoegd (de foto toont ze niet), rond zoals bij de vilt-mot;
  - sprieten: niet uit de foto, als oren naar de zijkant (vilt_hand / foto_sprieten), groot genoeg voor 1x;
  - ogen: alleen plek en maat (uit de foto), groot en rond.
Draaien: python3 docs/concept/sprites/poedelmot/silhouet/ronde1/silhouet.py
Uitvoer (in deze map): silhouet_1x.png, silhouet_8x.png, delen_1x.png, delen_8x.png, controle_foto.png, vel.png"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../../../..'))
FOTO = os.path.join(HERE, '../../referenties/foto_tak_katoen.webp')
W = 1700                       # werkdoek in fotocoördinaten (foto 1500 + marge rechts voor de achtervleugel)

# ---- omtrekken in fotocoördinaten ----
LIJF = [(705, 720), (722, 662), (762, 628), (820, 604), (880, 597), (940, 601), (990, 624), (1022, 664), (1042, 722),
        (1058, 782), (1104, 805), (1150, 842), (1176, 900), (1182, 962), (1174, 1022), (1148, 1080), (1080, 1110),
        (1000, 1122), (900, 1130), (800, 1128), (705, 1108), (652, 1060), (640, 990), (660, 918), (690, 850), (700, 780)]
# voorvleugels: voorrand uit de foto (zelfde hoek = zelfde pose), achterrand met de hand verbreed tot een
# echte motvleugel (op de foto zie je ze bijna op de kant, dan lezen ze op 1x als stekels); k = korter t.o.v. de wortel
VOORVL_L = dict(wortel=(720, 780), k=0.72,
                pts=[(720, 700), (680, 690), (600, 628), (500, 545), (400, 468), (300, 398), (200, 334), (140, 312),
                     (100, 322), (96, 370), (150, 470), (240, 590), (350, 700), (470, 790), (590, 850), (700, 870)])
VOORVL_R = dict(wortel=(900, 660), k=0.80,
                pts=[(780, 650), (774, 540), (790, 420), (826, 290), (874, 170), (916, 100), (950, 82), (990, 100),
                     (1040, 200), (1090, 330), (1116, 460), (1104, 590), (1050, 680)])
# achtervleugels (met de hand, vilt-mot): rond, onder/achter de voorvleugel, aan beide kanten zichtbaar
ACHTERVL_L = [(700, 800), (580, 800), (460, 822), (370, 870), (330, 940), (346, 1010), (410, 1060), (510, 1078),
              (610, 1060), (690, 1010)]
ACHTERVL_R = [(1110, 780), (1190, 728), (1290, 708), (1380, 730), (1426, 800), (1420, 890), (1360, 960),
              (1270, 996), (1190, 990), (1150, 960)]
# poten: dikke wollige bovenpoot (foto) -> dun 'geschoren' enkeltje -> pompon (poedelknip)
POTEN = {
    'ver_links':  ([(672, 1060, 44), (640, 1130, 36), (628, 1160, 28), (620, 1176, 28)], (594, 1200, 60)),
    'links_voor': ([(752, 1030, 56), (736, 1110, 46), (726, 1150, 34), (718, 1170, 34)], (704, 1228, 84)),
    'rechts_voor': ([(920, 1060, 58), (980, 1120, 48), (1020, 1150, 36), (1036, 1168, 36)], (1064, 1232, 90)),
    'ver_rechts': ([(1150, 990, 44), (1186, 1056, 36), (1202, 1090, 28), (1210, 1106, 28)], (1230, 1150, 60)),
}
OREN = {'links': ((776, 676), (452, 560)), 'rechts': ((990, 660), (1300, 572))}
OGEN = {'links': (872, 868, 66), 'rechts': (1032, 862, 48)}    # (x, y, r) op de foto; rechts deels weggedraaid


def catmull(pts, steps=12, closed=True):
    P = list(pts) + ([pts[0], pts[1], pts[2]] if closed else [])
    out = []
    n = len(pts) if closed else len(pts) - 1
    for i in range(n):
        p0, p1, p2, p3 = P[i - 1] if (i or closed) else P[0], P[i], P[i + 1], P[min(i + 2, len(P) - 1)]
        for k in range(steps):
            t = k / steps
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    return out


def doek():
    im = Image.new('L', (W, W), 0)
    return im, ImageDraw.Draw(im)


def schaal_om(pts, c, k):
    return [(c[0] + (x - c[0]) * k, c[1] + (y - c[1]) * k) for x, y in pts]


def plukrand(d, pts, r, stap, inwaarts=0.35):
    """Wollige rand: rondjes langs de omtrek (iets naar binnen), zoals de plukken op de foto."""
    c = catmull(pts, 24)
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    acc, prev = 0.0, c[0]
    for p in c:
        acc += math.dist(p, prev); prev = p
        if acc >= stap:
            acc = 0
            dx, dy = cx - p[0], cy - p[1]; L = math.hypot(dx, dy) or 1
            x, y = p[0] + dx / L * r * inwaarts, p[1] + dy / L * r * inwaarts
            d.ellipse([x - r, y - r, x + r, y + r], fill=255)


def buis(d, pts):
    for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
        for i in range(21):
            t = i / 20
            x, y, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            d.ellipse([x - r, y - r, x + r, y + r], fill=255)


def pompon(d, x, y, r):
    """Pompon van de poedelknip: rond, met 7 plukken rondom (onderkant iets afgeplat, hij staat erop)."""
    d.ellipse([x - r * 0.8, y - r * 0.8, x + r * 0.8, y + r * 0.8], fill=255)
    for a in range(7):
        ang = math.radians(-90 + a * 360 / 7)
        px, py = x + math.cos(ang) * r * 0.55, y + math.sin(ang) * r * 0.55 * 0.85
        rr = r * 0.45
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=255)


def oor(d, wortel, punt):
    """Kamvormige spriet als oor: blad dat naar boven bolt, breed bij de wortel, taps naar de punt."""
    (x0, y0), (x1, y1) = wortel, punt
    L = math.dist(wortel, punt); ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = uy, -ux                       # normaal; kies de kant die naar boven wijst
    if ny > 0:
        nx, ny = -nx, -ny
    boven, onder = [], []
    for i in range(31):
        t = i / 30
        bol = math.sin(math.pi * t) * L * 0.10          # middenlijn bolt omhoog
        hw = L * 0.25 * (math.sin(math.pi * (0.12 + 0.88 * t)) ** 0.8) * (1 - 0.45 * t) + 6
        mx, my = x0 + ux * L * t + nx * bol, y0 + uy * L * t + ny * bol
        boven.append((mx + nx * hw * 1.05, my + ny * hw * 1.05))
        onder.append((mx - nx * hw * 0.85, my - ny * hw * 0.85))
    d.polygon(boven + onder[::-1], fill=255)


def maskers():
    M = {}
    im, d = doek()
    d.polygon(catmull(ACHTERVL_L), fill=255)
    d.polygon(catmull(ACHTERVL_R), fill=255)
    M['achtervleugel'] = np.array(im) > 0
    im, d = doek()
    for v in (VOORVL_L, VOORVL_R):
        d.polygon(catmull(schaal_om(v['pts'], v['wortel'], v['k'])), fill=255)
    M['voorvleugel'] = np.array(im) > 0
    im, d = doek()
    d.polygon(catmull(LIJF), fill=255)
    plukrand(d, LIJF, 30, 52)
    for buisp, (px, py, pr) in POTEN.values():
        buis(d, buisp)
        pompon(d, px, py, pr)
    M['lijf'] = np.array(im) > 0
    im, d = doek()
    for w, p in OREN.values():
        oor(d, w, p)
    M['oor'] = np.array(im) > 0
    im, d = doek()
    for x, y, r in OGEN.values():
        d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    M['oog'] = np.array(im) > 0
    return M


def kader(M):
    alles = np.zeros((W, W), bool)
    for k in ('achtervleugel', 'voorvleugel', 'lijf', 'oor'):
        alles |= M[k]
    ys, xs = np.nonzero(alles)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    zijde = max(x1 - x0, y1 - y0) / 62.0 * 64.0         # 1 px marge rondom, onderkant op y=62
    cx = (x0 + x1) / 2
    bx0 = cx - zijde / 2
    by0 = y1 + zijde / 64.0 * 1.5 - zijde
    return bx0, by0, zijde


def naar(mask, kad, n):
    bx0, by0, z = kad
    im = Image.fromarray((mask * 255).astype(np.uint8))
    return np.array(im.transform((n, n), Image.EXTENT, (bx0, by0, bx0 + z, by0 + z), Image.BILINEAR))


def bouw():
    M = maskers()
    kad = kader(M)
    lagen = {}
    for k, m in M.items():
        lagen[k] = naar(m, kad, 512) > 127
    # 1x: per laag BOX-verkleinen, dunne delen (oorpunten, vleugelpunten) iets royaler meetellen
    een = {}
    for k, m in M.items():
        big = naar(m, kad, 512)
        drempel = {'oor': 95, 'voorvleugel': 105}.get(k, 118)
        een[k] = np.array(Image.fromarray(big).resize((64, 64), Image.BOX)) > drempel
    vul_gaatjes(een)
    return M, kad, lagen, een


def vul_gaatjes(een, maxpx=4):
    """Gaatjes < maxpx in het totaal (afrondingsruis tussen poten/lijf) dichtzetten in de laag 'lijf'."""
    alles = een['achtervleugel'] | een['voorvleugel'] | een['lijf'] | een['oor']
    leeg = ~alles; gezien = np.zeros_like(leeg)
    for y in range(64):
        for x in range(64):
            if leeg[y, x] and not gezien[y, x]:
                stapel, comp, rand = [(y, x)], [], False
                gezien[y, x] = True
                while stapel:
                    cy, cx = stapel.pop(); comp.append((cy, cx))
                    if cy in (0, 63) or cx in (0, 63):
                        rand = True
                    for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                        if 0 <= ny < 64 and 0 <= nx < 64 and leeg[ny, nx] and not gezien[ny, nx]:
                            gezien[ny, nx] = True; stapel.append((ny, nx))
                if not rand and len(comp) < maxpx:
                    for cy, cx in comp:
                        een['lijf'][cy, cx] = True


GRIJS = {'achtervleugel': (150, 150, 150), 'voorvleugel': (105, 105, 105), 'lijf': (25, 25, 25), 'oor': (70, 45, 30)}


def delen_rgba(L, scheiding=True):
    n = L['lijf'].shape[0]
    out = np.zeros((n, n, 4), np.uint8)
    for k in ('achtervleugel', 'voorvleugel', 'oor', 'lijf'):      # oren achter de kop, vóór de vleugels
        m = L[k]
        if scheiding and k in ('lijf', 'oor'):
            # 1 laag 'lucht' (wit) rond lijf/oren waar ze over de vleugels vallen: lijf leest los
            r = 1 if n == 64 else 6
            grow = np.array(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * r + 1))) > 0
            rand = grow & ~m & (out[..., 3] > 0)
            out[rand] = (255, 255, 255, 255)
        out[m] = GRIJS[k] + (255,)
    return out


def main():
    M, kad, L8, L1 = bouw()
    sil1 = np.zeros((64, 64, 4), np.uint8)
    alles1 = L1['achtervleugel'] | L1['voorvleugel'] | L1['lijf'] | L1['oor']
    sil1[alles1] = (16, 16, 16, 255)
    Image.fromarray(sil1).save(os.path.join(HERE, 'silhouet_1x.png'))
    Image.fromarray(sil1).resize((512, 512), Image.NEAREST).save(os.path.join(HERE, 'silhouet_8x.png'))
    d1 = delen_rgba(L1)
    # ogen: alleen plek en maat (rode stip/ring) op de delenversie
    oog1 = L1['oog']
    d1m = d1.copy(); d1m[oog1] = (200, 40, 40, 255)
    Image.fromarray(d1m).save(os.path.join(HERE, 'delen_1x.png'))
    big = Image.fromarray(d1m).resize((512, 512), Image.NEAREST)
    dr = ImageDraw.Draw(big)
    for x in range(0, 513, 64):
        dr.line([(x, 0), (x, 512)], fill=(0, 160, 255, 120)); dr.line([(0, x), (512, x)], fill=(0, 160, 255, 120))
    big.save(os.path.join(HERE, 'delen_8x.png'))
    # controle: omtrek van alle delen over de foto (zelfde uitsnede als de sprite)
    foto = Image.open(FOTO).convert('RGB')
    doekf = Image.new('RGB', (W, W), (40, 40, 40)); doekf.paste(foto, (0, 0))
    bx0, by0, z = kad
    fc = doekf.transform((512, 512), Image.EXTENT, (bx0, by0, bx0 + z, by0 + z), Image.BILINEAR)
    kleuren = {'achtervleugel': (0, 200, 255), 'voorvleugel': (255, 220, 0), 'lijf': (255, 40, 40), 'oor': (255, 0, 255), 'oog': (0, 255, 0)}
    fca = np.array(fc)
    for k, col in kleuren.items():
        m = L8[k]
        er = np.array(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5))) > 0
        fca[m & ~er] = col
    Image.fromarray(fca).save(os.path.join(HERE, 'controle_foto.png'))
    vel(fc, Image.fromarray(fca), sil1, d1m)
    print('kader (fotocoördinaten): x0=%.0f y0=%.0f zijde=%.0f  -> %.1f fotopx per spritepx' % (bx0, by0, z, z / 64))
    print('pixels silhouet:', int(alles1.sum()), ' lijf:', int(L1['lijf'].sum()))


def gen3(naam):
    p = os.path.join(ROOT, 'graphics/pokemon', naam, 'anim_front.png')
    if not os.path.exists(p):
        p = os.path.join(ROOT, 'graphics/pokemon', naam, 'front.png')
    im = Image.open(p)
    idx = np.array(im)[:64, :64]
    rgba = np.array(im.convert('RGBA'))[:64, :64]
    rgba[idx == 0, 3] = 0
    sil = np.zeros_like(rgba); sil[rgba[..., 3] > 0] = (16, 16, 16, 255)
    return rgba, sil


def vel(foto512, controle512, sil1, delen1):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    S = 4
    namen = ['venomoth', 'butterfree', 'dustox', 'frosmoth']
    tegels = [('foto (uitsnede = spritekader)', foto512.resize((256, 256))),
              ('omtrek over foto', controle512.resize((256, 256)))]
    def t(a, bg):
        im = Image.fromarray(a).resize((64 * S, 64 * S), Image.NEAREST)
        b = Image.new('RGB', im.size, bg); b.paste(im, (0, 0), im); return b
    tegels.append(('poedelmot silhouet 4x', t(sil1, (235, 235, 235))))
    tegels.append(('delen (ogen rood) 4x', t(delen1, (235, 235, 235))))
    rij2 = []
    for n in namen:
        rgba, sil = gen3(n)
        rij2.append((n + ' 4x', t(sil, (235, 235, 235))))
    rij3 = [('poedelmot', sil1)] + [(n, gen3(n)[1]) for n in namen]
    Wd = 4 * 256 + 5 * 12
    H = 12 + 20 + 256 + 12 + 20 + 256 + 12 + 20 + 80 + 12
    out = Image.new('RGB', (Wd, H), (250, 250, 250))
    dr = ImageDraw.Draw(out)
    y = 12
    for rij in (tegels, rij2):
        x = 12
        for lab, im in rij:
            dr.text((x, y), lab, fill=(0, 0, 0), font=F); out.paste(im, (x, y + 20)); x += 256 + 12
        y += 20 + 256 + 12
    dr.text((12, y), '1x (zelfde schaal als in de game): poedelmot, ' + ', '.join(namen) + '  (frosmoth = Gen 8, front.png)', fill=(0, 0, 0), font=F)
    x = 12
    for lab, a in rij3:
        for bg in ((235, 235, 235), (60, 60, 70)):
            im = Image.fromarray(a); b = Image.new('RGB', (64, 64), bg); b.paste(im, (0, 0), im)
            out.paste(b, (x, y + 20)); x += 70
        x += 20
    out.save(os.path.join(HERE, 'vel.png'))


if __name__ == '__main__':
    main()
