"""Olinguito (Dark-starter fase 1): opbouw uit vormen + belichting + selout.

Elk onderdeel = ellips of reeks cirkels (staart) met een z-volgorde en een
ramp. Schaduw per pixel uit een pseudo-normaal (bolvorm) met licht van
linksboven, gekwantiseerd naar de ramp. Daarna omlijning (selout) en handwerk
(ogen, neus, klauwen, bes) als losse pixels.
"""
import sys, os, math
import numpy as np
from PIL import Image
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
from ramp import gba, write_pal

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------- palet ----------------
PAL = [gba((152, 208, 160))] + [gba(c) for c in [
    (255, 189, 106),  # 1 vacht hooglicht
    (213, 131, 57),   # 2 vacht basis
    (164, 90, 41),    # 3 vacht schaduw
    (123, 57, 41),    # 4 vacht donkerst (selout / plooien)
    (255, 230, 180),  # 5 snuit/buik licht
    (230, 189, 139),  # 6 snuit/buik basis
    (180, 131, 98),   # 7 snuit/buik schaduw
    (246, 238, 222),  # 8 klauw licht
    (164, 148, 131),  # 9 klauw schaduw
    (98, 57, 49),     # 10 oog (iris)
    (139, 32, 49),    # 11 bes donker / mondbinnenkant
    (255, 123, 106),  # 12 bes licht
    (205, 41, 57),    # 13 bes basis
    (255, 255, 255),  # 14 wit (glans)
]] + [(16, 16, 16)]   # 15 omlijning
FUR = [1, 2, 3, 4]
CREAM = [5, 6, 7]
CLAW = [8, 9]
BERRY = [12, 13, 4]   # donkerste van de bes = vacht4? nee: zie DARK
OUT = 15

SCALE_BODY, SCALE_HEAD = 0.82, 0.9
LIGHT = np.array([-0.55, -0.70, 0.50]); LIGHT /= np.linalg.norm(LIGHT)


class Canvas:
    def __init__(s):
        s.part = np.zeros((64, 64), np.int16) - 1   # onderdeel-id
        s.inten = np.zeros((64, 64))
        s.parts = []        # (ramp, dark-index, thresholds)

    def new_part(s, ramp, dark, th):
        s.parts.append((ramp, dark, th)); return len(s.parts) - 1

    xf = None

    def ellipse(s, pid, cx, cy, rx, ry, bias=0.0, under=False, tilt=0.0):
        if s.xf: cx, cy, k = s.xf(cx, cy); rx *= k; ry *= k
        for y in range(64):
            for x in range(64):
                dx = (x + 0.5 - cx); dy = (y + 0.5 - cy)
                if tilt:
                    c, sn = math.cos(tilt), math.sin(tilt)
                    dx, dy = c * dx + sn * dy, -sn * dx + c * dy
                nx, ny = dx / rx, dy / ry
                r2 = nx * nx + ny * ny
                if r2 > 1: continue
                if under and s.part[y, x] >= 0: continue
                nz = math.sqrt(max(0, 1 - r2))
                n = np.array([nx, ny, nz * 1.1]); n /= np.linalg.norm(n)
                s.part[y, x] = pid
                s.inten[y, x] = float(n @ LIGHT) + bias

    def chain(s, pid, pts, bias=0.0, under=False, jag=None):
        """Reeks cirkels (cx, cy, r) = staart; normaal = afstand tot de as."""
        for y in range(64):
            for x in range(64):
                best = None
                for (cx, cy, r) in pts:
                    d = math.hypot(x + 0.5 - cx, y + 0.5 - cy) / r
                    if d <= 1 and (best is None or d < best[0]):
                        best = (d, (x + 0.5 - cx) / r, (y + 0.5 - cy) / r)
                if best is None: continue
                if under and s.part[y, x] >= 0: continue
                d, nx, ny = best
                nz = math.sqrt(max(0, 1 - d * d))
                n = np.array([nx, ny, nz * 1.1]); n /= np.linalg.norm(n)
                s.part[y, x] = pid
                s.inten[y, x] = float(n @ LIGHT) + bias

    def tube(s, pid, pts, bias=0.0, fluff=0.10, period=5.0, bands=None):
        """Buis langs een polylijn (x, y, r); normaal loodrecht op de as.
        fluff = getande rand (plukken), bands = (periode, breedte, bias) ringen."""
        if s.xf:
            pts = [(*s.xf(x, y)[:2], r * s.xf(x, y)[2]) for (x, y, r) in pts]
        seg = []
        acc = 0.0
        for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
            L = math.hypot(x1 - x0, y1 - y0); seg.append((x0, y0, r0, x1, y1, r1, L, acc)); acc += L
        for y in range(64):
            for x in range(64):
                px, py = x + 0.5, y + 0.5
                best = None
                for (x0, y0, r0, x1, y1, r1, L, a0) in seg:
                    t = max(0, min(1, ((px - x0) * (x1 - x0) + (py - y0) * (y1 - y0)) / (L * L)))
                    ax, ay = x0 + t * (x1 - x0), y0 + t * (y1 - y0)
                    r = r0 + t * (r1 - r0)
                    sarc = a0 + t * L
                    d = math.hypot(px - ax, py - ay)
                    # plukken: alleen aan de buitenkant, zaagtand langs de boog
                    ph = (sarc / period) % 1.0
                    rr = r * (1 + fluff * (1 - 2 * abs(ph - 0.5)) * 2 - fluff)
                    q = d / rr
                    if q <= 1 and (best is None or q < best[0]):
                        best = (q, (px - ax) / rr, (py - ay) / rr, sarc)
                if best is None: continue
                q, nx, ny, sarc = best
                nz = math.sqrt(max(0, 1 - q * q))
                n = np.array([nx, ny, nz * 1.1]); n /= np.linalg.norm(n)
                b = bias
                if bands and (sarc % bands[0]) < bands[1] and sarc > bands[0] * 0.6:
                    b += bands[2]
                s.part[y, x] = pid
                s.inten[y, x] = float(n @ LIGHT) + b

    def render(s):
        img = np.zeros((64, 64), np.uint8)
        for y in range(64):
            for x in range(64):
                p = s.part[y, x]
                if p < 0: continue
                ramp, dark, th = s.parts[p]
                v = s.inten[y, x]
                k = 0
                while k < len(th) and v < th[k]: k += 1
                img[y, x] = ramp[min(k, len(ramp) - 1)]
        return img


def outline(img, part, parts, inner_pairs=()):
    """Buitenlijn: pixels van de figuur die aan transparant grenzen.
    Kant boven/links -> donkerste tint van het onderdeel (selout), anders zwart."""
    m = img > 0
    out = img.copy()
    for y in range(64):
        for x in range(64):
            if not m[y, x]: continue
            def tr(dx, dy):
                xx, yy = x + dx, y + dy
                return not (0 <= xx < 64 and 0 <= yy < 64) or not m[yy, xx]
            up, dn, lf, rt = tr(0, -1), tr(0, 1), tr(-1, 0), tr(1, 0)
            if not (up or dn or lf or rt): continue
            dark = parts[part[y, x]][1] if part[y, x] >= 0 else OUT
            if dn or rt:
                out[y, x] = OUT
            else:
                out[y, x] = dark
    return out


def inner_lines(img, part, parts, order):
    """Scheiding tussen overlappende onderdelen: de pixel van het voorste deel die
    aan een achterliggend deel grenst krijgt de donkerste tint van dat voorste
    deel; onder/rechts (waar het voorste deel over het achterste valt) zwart."""
    out = img.copy()
    for y in range(64):
        for x in range(64):
            p = part[y, x]
            if p < 0: continue
            for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                xx, yy = x + dx, y + dy
                if not (0 <= xx < 64 and 0 <= yy < 64): continue
                q = part[yy, xx]
                if q < 0 or q == p: continue
                if (p, q) in order:          # p ligt voor q
                    col = order[(p, q)]
                    if col == 'dark':
                        out[y, x] = parts[p][1]
                    elif col == 'black':
                        out[y, x] = OUT if (dx, dy) in ((0, 1), (1, 0)) else parts[p][1]
                    elif col == 'shade':      # alleen schaduw op het achterste deel
                        pass
    return out


def put(img, pts, c):
    for x, y in pts:
        if 0 <= x < 64 and 0 <= y < 64:
            img[y, x] = c


def claw(img, pts, ring=False):
    """Klauw van basis naar punt: basis schaduwtint, rest licht; met ring=True
    zwarte rand eromheen waar hij buiten de figuur steekt."""
    for i, (x, y) in enumerate(pts):
        img[y, x] = 9 if i == 0 else 8
    if ring:
        S = set(pts)
        for (x, y) in pts:
            for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                xx, yy = x + dx, y + dy
                if (xx, yy) in S or not (0 <= xx < 64 and 0 <= yy < 64): continue
                if img[yy, xx] == 0:
                    img[yy, xx] = OUT


def build(frame):
    C = Canvas()
    TF = [0.80, 0.30, -0.40]     # vacht: drempels hooglicht/basis/schaduw
    tailF = C.new_part(FUR, 4, [0.82, 0.30, -0.38])
    legFar = C.new_part(FUR, 4, [9, 0.45, -0.3])
    armFar = C.new_part(FUR, 4, [9, 0.45, 0.05])
    body = C.new_part(FUR, 4, TF)
    belly = C.new_part(CREAM, 7, [0.55, 0.05])
    legNear = C.new_part(FUR, 4, TF)
    earFar = C.new_part(FUR, 4, [9, 0.40, -0.4])
    earNear = C.new_part(FUR, 4, TF)
    earIn = C.new_part(CREAM, 7, [9, 0.2])
    head = C.new_part(FUR, 4, [0.78, 0.25, -0.45])
    muzzle = C.new_part(CREAM, 7, [0.55, 0.0])
    berry = C.new_part([12, 13, 11], 11, [0.70, 0.10])
    armNear = C.new_part(FUR, 4, TF)
    armUp = C.new_part(FUR, 4, TF)

    if frame == 1:
        tail = [(40, 52, 4.5), (45, 50, 5.0), (49, 46, 5.2), (52, 41, 5.3), (53, 35, 5.2),
                (52, 29, 5.0), (49, 24, 4.6), (46, 21, 4.0), (43, 21, 3.3)]
        hx, hy = 24, 24; armraise = False
    else:
        tail = [(40, 52, 4.5), (46, 50, 5.0), (51, 46, 5.2), (55, 41, 5.3), (57, 35, 5.2),
                (57, 29, 5.0), (56, 24, 4.6), (54, 20, 4.0), (51, 18, 3.3)]
        hx, hy = 23, 23; armraise = True
    SB, SH = SCALE_BODY, SCALE_HEAD
    PX, PY = 31, 57
    def body_xf(x, y): return PX + (x - PX) * SB, PY + (y - PY) * SB, SB
    hcx, hcy, _ = body_xf(hx, hy)
    def head_xf(x, y): return hcx + (x - hx) * SH, hcy + (y - hy) * SH, SH
    C.xf = body_xf
    C.tube(tailF, tail, fluff=0.16, period=3.5, bands=(7.0, 2.0, -0.28))
    # verste poten (achter het lijf)
    C.ellipse(legFar, 36, 51, 5, 5.5)
    C.ellipse(legFar, 38, 55.5, 4.5, 2.2)
    # lijf: peervorm, iets naar rechts (driekwart)
    C.ellipse(body, 30, 42, 11.5, 12.5)
    C.ellipse(belly, 26, 41, 5, 8, bias=0.15)
    # voorste achterpoot (zit; dij rond, voet naar voren)
    C.ellipse(legNear, 23, 50, 6, 6)
    C.ellipse(legNear, 19.5, 55, 5.5, 2.5, bias=0.1)
    # kop
    C.xf = head_xf
    C.ellipse(earFar, hx + 9, hy - 9, 3.6, 3.6)
    C.ellipse(earNear, hx - 6, hy - 8.5, 3.8, 3.8)
    C.ellipse(earIn, hx - 6.3, hy - 8.6, 2.0, 2.0, bias=-0.3)
    C.ellipse(earIn, hx + 8.6, hy - 9, 1.7, 1.9, bias=-0.3)
    C.ellipse(head, hx, hy, 11.5, 9.5)
    C.ellipse(muzzle, hx - 5, hy + 4.5, 5.5, 3.6, bias=0.1)
    C.xf = body_xf
    # gestolen bes op schoot
    bx, by = 25, 46
    C.ellipse(berry, bx, by, 4.3, 4.1)
    if not armraise:
        # voorste arm: van de rechterschouder omlaag, poot om de bes
        C.ellipse(armNear, 31.5, 41, 3.3, 5.6, tilt=0.38)
        C.ellipse(armNear, 29, 46.3, 3.1, 2.5)
    else:
        # voorste arm omhoog naast de kop: graai met gespreide klauwen
        C.ellipse(armNear, 36.5, 30.5, 3.0, 6.0, tilt=0.42)
        C.ellipse(armNear, 39.5, 24.5, 3.0, 2.7)
    # verste arm voor de borst, pols gebogen: de 'inbrekershouding'
    C.ellipse(armUp, 17.5, 36.3, 5.2, 2.7, tilt=0.06)
    C.ellipse(armUp, 11.8, 37.8, 3.0, 2.8)
    img = C.render()
    parts = C.parts
    order = {}
    for front in (body, legNear, head, earNear, earFar, muzzle, belly, berry, armNear, armFar, legFar, armUp):
        for back in (tailF, legFar, armFar, body, belly, earFar, earNear, head, muzzle, berry, armNear, legNear):
            if front > back:
                order[(front, back)] = 'black'
    # binnen dezelfde vacht: zachte scheiding (donkerste vachttint), behalve onder/rechts
    for f, b, col in [(head, body, 'black'), (legNear, body, 'dark'), (belly, body, None),
                      (muzzle, head, 'dark'), (earNear, head, None), (earFar, head, None),
                      (armNear, body, 'dark'), (armNear, belly, 'dark'), (body, tailF, 'black'),
                      (armFar, body, 'dark'), (armFar, belly, 'dark'), (armNear, legNear, 'black'), (legNear, belly, 'dark')]:
        if col is None: order.pop((f, b), None)
        else: order[(f, b)] = col
    img = inner_lines(img, C.part, parts, order)
    img = outline(img, C.part, parts)
    XF = dict(body=body_xf, head=head_xf)
    return img, C, dict(xf=XF, head=(hx, hy), berry=(bx, by), raise_=armraise,
                        ids=dict(head=head, belly=belly, berry=berry, body=body, tail=tailF))


def details(img, C, info, frame):
    hx, hy = info['head']; bx, by = info['berry']
    # ogen: groot en donker (verste oog smaller), glans linksboven
    ex1, ey = hx - 9, hy - 1    # verste oog (links)
    ex2 = hx + 1                # dichtstbijzijnde oog
    if frame == 1:
        put(img, [(ex1, ey), (ex1 + 1, ey), (ex1, ey + 1), (ex1 + 1, ey + 1), (ex1, ey + 2), (ex1 + 1, ey + 2), (ex1, ey - 1)], OUT)
        put(img, [(ex1 + 1, ey + 2)], 10)
        put(img, [(ex1, ey)], 14)
        e2 = [(ex2 + dx, ey - 1 + dy) for dx in range(3) for dy in range(4)] + [(ex2 + 1, ey - 2), (ex2 + 3, ey), (ex2 + 3, ey + 1)]
        put(img, e2, OUT)
        put(img, [(ex2 + 1, ey + 2), (ex2 + 2, ey + 2), (ex2 + 2, ey + 1)], 10)
        put(img, [(ex2, ey - 1), (ex2 + 1, ey - 1)], 14)
    else:
        # blije/ondeugende ogen: half dichtgeknepen (grijns)
        put(img, [(ex1, ey), (ex1 + 1, ey), (ex1, ey + 1), (ex1 + 1, ey + 1), (ex1, ey - 1)], OUT)
        put(img, [(ex1, ey)], 14)
        e2 = [(ex2 + dx, ey + dy) for dx in range(3) for dy in range(3)] + [(ex2 + 3, ey + 1)]
        put(img, e2, OUT)
        put(img, [(ex2 + 2, ey + 2)], 10)
        put(img, [(ex2, ey), (ex2 + 1, ey)], 14)
    # neus op de snuitpunt
    nx, ny = hx - 10, hy + 3
    put(img, [(nx, ny), (nx + 1, ny), (nx, ny + 1), (nx + 1, ny + 1), (nx + 2, ny)], OUT)
    put(img, [(nx + 1, ny)], 10)
    # mond
    if frame == 1:
        put(img, [(nx + 2, ny + 3), (nx + 3, ny + 3), (nx + 4, ny + 2), (nx + 5, ny + 2)], 4)   # grijnsje
    else:
        put(img, [(nx + 1, ny + 3), (nx + 2, ny + 3), (nx + 3, ny + 4), (nx + 4, ny + 4), (nx + 5, ny + 3), (nx + 6, ny + 2)], OUT)
        put(img, [(nx + 2, ny + 4), (nx + 3, ny + 5), (nx + 4, ny + 5)], OUT)
        put(img, [(nx + 3, ny + 4) if False else (nx + 2, ny + 4)], 11)
    # inbrekerspoot: drie lange haken die omlaag hangen
    for x in (9, 11, 13):
        claw(img, [(x + 1, 40), (x + 1, 41), (x, 42), (x, 43)][:4 if x != 13 else 3], ring=True)
    if not info['raise_']:
        # voorste poot om de bes: twee haken over de voorkant
        claw(img, [(27, 45), (26, 45), (25, 46)])
        claw(img, [(27, 47), (26, 47), (25, 48)])
    else:
        # gespreide klauwen boven de opgeheven poot
        claw(img, [(38, 22), (37, 21), (37, 20), (36, 19)], ring=True)
        claw(img, [(40, 21), (40, 20), (40, 19), (39, 18)], ring=True)
        claw(img, [(42, 22), (43, 21), (43, 20), (44, 19)], ring=True)
    # achtervoet: twee klauwen naar voren
    claw(img, [(13, 54), (12, 54), (11, 55)], ring=True)
    claw(img, [(13, 56), (12, 56), (11, 57)], ring=True)
    # bes: hooglicht + steeltje
    put(img, [(bx - 2, by - 2)], 14)
    put(img, [(bx, by - 4), (bx + 1, by - 5)], 4)
    return img


def save(frames, d):
    a = np.vstack(frames)
    im = Image.fromarray(a, 'P')
    flat = []
    for c in PAL: flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.save(os.path.join(d, 'anim_front.png'), transparency=0)
    write_pal(os.path.join(d, 'normal.pal'), PAL)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else HERE
    os.makedirs(out, exist_ok=True)
    fr = []
    for f in (1, 2):
        img, C, info = build(f)
        fr.append(img if '--bare' in sys.argv else details(img, C, info, f))
    save(fr, out)
    print('ok', out)
