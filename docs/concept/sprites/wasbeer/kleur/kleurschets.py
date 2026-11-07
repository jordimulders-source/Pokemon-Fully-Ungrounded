"""Wasbeer kleurschets r1 op silhouet ronde 11 (Jordi, 2 nov: "Fix deze laatste dingetjes en kleur het in, geef me
daarna ook een raster zodat ik kan schetsen wat anders moet" + "en blijf vergelijken met bron fotos").
Een snelle ontwerpkleuring om pose, buidel en verhoudingen te beoordelen (nog niet de eindsprite van de maker-agent).
Kleuren van de foto's: grijsbruine rug/flank, geelbruine borst/buik (foto 2, 7, 10, 12), donkerbruine onderarmen
en onderbenen, grijze kop met zwart masker over ogen en neusrug, witte wenkbrauwband en witte snuitrand (foto 7, 11),
geringde staart licht/donker, crème koevoetklauwen (lijnkenmerk), buidel warmer bruin met donkere opening.
Draaien: python3 kleurschets.py -> kleurschets_r3.png (1x), vel_kleurschets_r3.png, raster_r3.png"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../silhouet'))
import silhouet_r11 as R
import kop_illustratie as KI
import kop11 as K11

SS = R.SS
OUT = (28, 22, 22)
C = {  # basis, schaduw, licht
    'fur': ((122, 114, 104), (92, 85, 78), (150, 142, 132)),
    'chest': ((200, 170, 120), (168, 138, 92), (222, 196, 150)),
    'dark': ((62, 50, 44), (42, 34, 30), (84, 70, 62)),
    'head': ((140, 134, 126), (106, 100, 94), (170, 164, 156)),
    'pouch': ((122, 114, 104), (92, 85, 78), (150, 142, 132)),   # zelfde vacht als het lijf: alleen de opening toont de buidel
    'tl': ((168, 156, 136), (134, 122, 104), (190, 178, 160)),
    'td': ((58, 51, 47), (40, 35, 32), (78, 70, 64)),
    'claw': ((237, 227, 204), (189, 178, 154), (250, 244, 230)),
}
WHITE, MASK, NOSE, EYE, GLINT = (232, 226, 214), (30, 26, 26), (58, 42, 42), (110, 42, 26), (255, 255, 255)


def part(fn):
    im = Image.new('L', (64 * SS, 64 * SS), 0)
    d = ImageDraw.Draw(im)
    fn(d)
    return np.array(im.resize((64, 64), Image.BOX)) >= 128


def tubes(*ts):
    def f(d):
        for t in ts:
            R.tube(d, t)
    return f


def head_fn(d):
    d.polygon([(R.kp(p)[0] * SS, R.kp(p)[1] * SS) for p in KI.HEADI], fill=255)
    R.tube(d, R.JAW)


def ears_fn(d):
    hx = [R.kp(p)[0] for p in KI.HEADI]; hy = [R.kp(p)[1] for p in KI.HEADI]
    fx = [p[0] for p in K11.HEAD11]; fy = [p[1] for p in K11.HEAD11]
    sx = (max(hx) - min(hx)) / (max(fx) - min(fx)); sy = (max(hy) - min(hy)) / (max(fy) - min(fy))
    for ear, dy in ((K11.EAR11_NEAR, 0), (K11.EAR11_FAR, 1.5)):
        d.polygon([((min(hx) + (x - min(fx)) * sx) * SS, (min(hy) + (y - min(fy)) * sy + dy) * SS) for x, y in ear], fill=255)


def pack_fn(d):
    x, y, rx, ry = R.PACK
    d.ellipse([(x - rx) * SS, (y - ry) * SS, (x + rx) * SS, (y + ry) * SS], fill=255)


def build():
    a = R.build()
    yy, xx = np.mgrid[0:64, 0:64]
    lab = np.full((64, 64), 'fur', object)
    parts = {
        'tail': part(tubes(R.TAIL)), 'legfar': part(tubes(R.LEG_FAR, R.FOOT_FAR)), 'pouch': part(pack_fn),
        'armfar': part(tubes(R.ARM_FAR)), 'legnear': part(tubes(R.LEG_NEAR, R.FOOT_NEAR)),
        'armnear': part(tubes(R.ARM_NEAR)), 'head': part(head_fn), 'ears': part(ears_fn),
    }
    order = ['tail', 'legfar', 'pouch', 'armfar', 'legnear', 'armnear', 'ears', 'head']
    pid = np.full((64, 64), 'body', object)
    for k in order:
        pid[parts[k] & a] = k
    claws = np.zeros((64, 64), bool)
    for cx, cy in R.CROWBAR_AT:
        for j, row in enumerate(R.CROWBAR):
            for i, ch in enumerate(row):
                if ch == '#':
                    claws[cy + j, cx + i] = True
    pid[claws] = 'claw'
    # kleurgroepen
    for y in range(64):
        xs = [x for x in range(64) if pid[y, x] == 'body']
        if xs and 20 <= y <= 47:          # borst/buik: voorste helft van de romp (driekwart: borst naar de kijker)
            w = xs[-1] - xs[0] + 1
            for x in xs:
                if x < xs[0] + max(3, int(w * 0.45)) and y >= 22:
                    lab[y, x] = 'chest'
    lab[pid == 'pouch'] = 'pouch'
    for k, knee in (('legnear', 48), ('legfar', 48)):
        lab[(pid == k) & (yy >= knee)] = 'dark'
        lab[(pid == k) & (yy < knee)] = 'fur'
    lab[(pid == 'armnear') & (xx <= 16)] = 'dark'
    lab[(pid == 'armnear') & (xx > 16)] = 'fur'
    lab[(pid == 'armfar') & (xx <= 17)] = 'dark'
    lab[(pid == 'armfar') & (xx > 17)] = 'fur'
    lab[pid == 'head'] = 'head'
    lab[pid == 'ears'] = 'head'
    lab[pid == 'claw'] = 'claw'
    # staartringen: afstand langs de staartlijn
    pts = []
    for (x0, y0, r0), (x1, y1, r1) in zip(R.TAIL, R.TAIL[1:]):
        for i in range(10):
            t = i / 10; pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    pts = np.array(pts); acc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    for y, x in zip(*np.where(pid == 'tail')):
        i = np.argmin(np.hypot(pts[:, 0] - x, pts[:, 1] - y))
        lab[y, x] = 'td' if (acc[i] // 3.2) % 2 else 'tl'
    # tint per pixel
    rgb = np.zeros((64, 64, 3), np.uint8)
    for y, x in zip(*np.where(a)):
        base, sh, li = C[lab[y, x]]
        col = base
        same = lambda yy_, xx_: 0 <= yy_ < 64 and 0 <= xx_ < 64 and a[yy_, xx_] and pid[yy_, xx_] == pid[y, x]
        if not same(y + 1, x) or not same(y, x + 1) or not same(y + 1, x + 1):
            col = sh                       # schaduw rechtsonder (licht van linksboven)
        elif not same(y - 1, x) or not same(y, x - 1):
            col = li
        rgb[y, x] = col
    # kop: masker over ogen en neusrug, witte wenkbrauwband, witte snuitrand, neus, oog
    ex, ey = R.kp(KI.EYEI); ex, ey = int(round(ex)), int(round(ey))
    nx, ny = R.kp(KI.NOSEI); nx, ny = int(round(nx)), int(round(ny))
    hd = (pid == 'head')
    for y, x in zip(*np.where(hd)):
        band = abs((y - ey) - (x - ex) * 0.18) <= 1.6 and x <= ex + 3       # band van de neus tot achter het oog
        if band:
            rgb[y, x] = MASK
        elif -3.6 <= (y - ey) - (x - ex) * 0.18 < -1.6 and nx + 1 <= x <= ex + 3:
            rgb[y, x] = WHITE              # wenkbrauwband
        elif 1.6 < (y - ey) - (x - ex) * 0.18 <= 3.4 and x <= ex + 1:
            rgb[y, x] = WHITE              # snuitrand/kaak
    for y, x in ((ny, nx), (ny, nx + 1), (ny - 1, nx), (ny - 1, nx + 1)):
        if 0 <= y < 64 and a[y, x]:
            rgb[y, x] = NOSE
    rgb[ey, ex] = EYE; rgb[ey, ex + 1] = EYE; rgb[ey - 1, ex] = GLINT
    # oorrand licht
    for y, x in zip(*np.where(pid == 'ears')):
        if not (y - 1 >= 0 and a[y - 1, x]):
            rgb[y, x] = WHITE
    # buidel: opening = donkere boog aan de bovenkant, rand licht eronder
    pk = pid == 'pouch'
    py0 = np.where(pk.any(1))[0][0]
    for x in range(64):
        ys = np.where(pk[:, x])[0]
        if len(ys) and ys[0] <= py0 + 3:
            rgb[min(ys[0] + 2, 63), x] = C['pouch'][1]          # opening: schaduwplooi, geen harde lijn
            rgb[min(ys[0] + 1, 63), x] = C['pouch'][2]
    # klauwen: onderste rij en haak in de schaduwtint
    for y, x in zip(*np.where(claws)):
        rgb[y, x] = C['claw'][0] if (y < 64 and claws[y - 1, x] is not None and (y + 1 < 64 and claws[y + 1, x])) else C['claw'][1]
    # omlijning: buitenrand + grenzen tussen voor- en achterdelen
    front = {'armnear': 6, 'armfar': 4, 'legnear': 5, 'head': 2, 'ears': 2, 'claw': 8, 'pouch': 2, 'body': 2, 'tail': 2, 'legfar': 2}   # alleen ledematen vóór het lijf krijgen een binnenlijn
    res = rgb.copy()
    for y, x in zip(*np.where(a)):
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            y2, x2 = y + dy, x + dx
            if not (0 <= y2 < 64 and 0 <= x2 < 64) or not a[y2, x2]:
                res[y, x] = C['claw'][1] if pid[y, x] == 'claw' else OUT
                break
            if front.get(pid[y, x], 2) > front.get(pid[y2, x2], 2) + 0 and pid[y2, x2] != pid[y, x] and pid[y, x] != 'claw':
                res[y, x] = (np.array(rgb[y, x]) * 0.45).astype(np.uint8)
                break
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    for y, x in zip(*np.where(a)):
        img.putpixel((int(x), int(y)), tuple(int(v) for v in res[y, x]) + (255,))
    return img


if __name__ == '__main__':
    img = build()
    img.save(os.path.join(HERE, 'kleurschets_r3.png'))
    S = 4
    ref = os.path.join(HERE, '../referenties')
    fotos = [('foto 10', 'foto10_staand_reikend.jpg', True), ('foto 11', 'foto11_driekwart_kop.webp', False),
             ('foto 7', 'foto7_frontaal_lange_poten.png', False), ('foto 12', 'foto12_rechtop_driekwart_lijf.png', False)]
    sheet = Image.new('RGB', (20 + (64 * S + 20) * 2 + 90 + 4 * 200, 64 * S + 60), (236, 234, 228))
    d = ImageDraw.Draw(sheet)
    x = 20
    for lab, bg in (('kleurschets r3 (licht)', (236, 234, 228)), ('donker', (40, 44, 60))):
        cell = Image.new('RGB', (64 * S, 64 * S), bg)
        big = img.resize((64 * S, 64 * S), Image.NEAREST); cell.paste(big, (0, 0), big)
        sheet.paste(cell, (x, 40)); d.text((x, 20), lab, fill=(30, 30, 30)); x += 64 * S + 20
    sheet.paste(img, (x, 40), img); d.text((x, 110), '1x', fill=(30, 30, 30)); x += 90
    for lab, fn, flip in fotos:
        f = Image.open(os.path.join(ref, fn)).convert('RGB')
        if flip:
            f = f.transpose(Image.FLIP_LEFT_RIGHT)
        f.thumbnail((190, 250)); sheet.paste(f, (x, 40)); d.text((x, 20), lab, fill=(30, 30, 30)); x += 200
    sheet.save(os.path.join(HERE, 'vel_kleurschets_r3.png'))
    # raster om op te schetsen: 10x met rasterlijnen en coördinaten
    Z = 10
    r = Image.new('RGB', (64 * Z + 40, 64 * Z + 40), (255, 255, 255))
    big = img.resize((64 * Z, 64 * Z), Image.NEAREST); r.paste(big, (30, 30), big)
    dr = ImageDraw.Draw(r)
    for i in range(65):
        c = (150, 150, 170) if i % 8 == 0 else (215, 215, 225)
        dr.line([(30 + i * Z, 30), (30 + i * Z, 30 + 64 * Z)], fill=c); dr.line([(30, 30 + i * Z), (30 + 64 * Z, 30 + i * Z)], fill=c)
        if i % 8 == 0 and i < 64:
            dr.text((32 + i * Z, 14), str(i), fill=(90, 90, 110)); dr.text((6, 32 + i * Z), str(i), fill=(90, 90, 110))
    r.save(os.path.join(HERE, 'raster_r3.png'))
