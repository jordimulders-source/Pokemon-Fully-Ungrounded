"""Bouwt model_v1.png uit onderdelen van gemini_gekozen_r5.png (alleen r5-pixels).
Kop/mantel/ogen/mond: pixelkopie binnen KOP_POLY. Tentakels: r5-tentakelstroken langs nieuwe banen gelegd.
Kanonnen: r5-uitsneden (vrijgemaakt, verplaatst/gedraaid)."""
import math, os
import numpy as np
from PIL import Image, ImageDraw

HIER = os.path.dirname(os.path.abspath(__file__))
R5 = Image.open(os.path.join(HIER, '..', 'referenties', 'gemini_gekozen_r5.png')).convert('RGB')
A = np.array(R5)
H, W = A.shape[:2]
WIT = np.array([255, 255, 255], np.uint8)

def niet_wit(a):
    return ~np.all(a > 238, axis=2)

def poly_mask(pts, w=W, h=H):
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).polygon(pts, fill=255)
    return np.array(m) > 0

# ---------- kop ----------
KOP_POLY = [(468,158),(470,120),(600,10),(1020,10),(1020,200),(800,204),(732,202),(712,231),
            (662,235),(634,245),(631,300),(636,340),(634,375),(624,394),(604,402),(560,403),(540,400),(518,378),(500,350),(492,362),
            (470,370),(380,374),(356,345),(355,300),(372,273),(410,263),(406,200),(455,197)]
def achtergrond(a):
    """wit dat met de rand verbonden is (gaten in de kop, zoals oogglans, horen bij de kop)."""
    wit = ~niet_wit(a); bg = np.zeros_like(wit)
    bg[0, :] = wit[0, :]; bg[-1, :] = wit[-1, :]; bg[:, 0] = wit[:, 0]; bg[:, -1] = wit[:, -1]
    while True:
        g = bg.copy()
        g[1:] |= bg[:-1]; g[:-1] |= bg[1:]; g[:, 1:] |= bg[:, :-1]; g[:, :-1] |= bg[:, 1:]
        g &= wit
        if (g == bg).all(): return bg
        bg = g
BG = achtergrond(A)
kop_m = poly_mask(KOP_POLY) & ~BG

# ---------- strook-sweep ----------
def polyline_dense(pts, step=0.5):
    pts = np.array(pts, float); out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(1, int(np.linalg.norm(b - a) / step))
        for i in range(1, n + 1): out.append(a + (b - a) * i / n)
    return np.array(out)

def bezier(p, n=400):
    p = np.array(p, float); t = np.linspace(0, 1, n)[:, None]
    if len(p) == 3: return (1-t)**2*p[0] + 2*(1-t)*t*p[1] + t**2*p[2]
    return (1-t)**3*p[0] + 3*(1-t)**2*t*p[1] + 3*(1-t)*t**2*p[2] + t**3*p[3]

def keten(*segs):
    pts = [segs[0][0]]
    for s in segs: pts.extend(list(s[1:]))
    return polyline_dense(pts, 0.5)

def frames(c):
    d = np.gradient(c, axis=0); d /= np.linalg.norm(d, axis=1)[:, None] + 1e-9
    n = np.stack([d[:, 1], -d[:, 0]], 1)   # links van de looprichting (in beeld)
    s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(c, axis=0), axis=1))])
    return d, n, s

class Strook:
    def __init__(self, p0, p1, hw, flip=False):
        self.p0 = np.array(p0, float); self.p1 = np.array(p1, float); self.hw = hw
        d = self.p1 - self.p0; self.L = np.linalg.norm(d); self.d = d / self.L
        self.n = np.array([self.d[1], -self.d[0]]) * (-1 if flip else 1)
    def sample(self, s, v):  # s in [0,L], v in [-1,1]
        p = self.p0 + self.d * s + self.n * v * self.hw
        x = int(round(p[0])); y = int(round(p[1]))
        return A[min(max(y, 0), H-1), min(max(x, 0), W-1)]

LIJN = np.array([10, 0, 0], np.uint8)   # meest voorkomende lijnkleur van r5

def sweep(canvas, cmask, curve, hw_fun, strook, side=1, s_off=0.0, scale=1.0, rand=3.0):
    """leg strook langs curve; side=+1: strook-normaal = links van looprichting.
    De buitenste `rand` px worden r5-lijnkleur (schone omlijning), binnenin de bronstrook zonder haar eigen lijn."""
    d, n, s = frames(curve); Ltot = s[-1]; L = strook.L
    binnen_src = (strook.hw - 3.0) / strook.hw
    for i in range(len(curve)):
        t = s[i] / Ltot; hw = hw_fun(t)
        if hw <= 0.3: continue
        # ping-pong langs de bron
        u = (s[i] * scale + s_off) % (2 * L); u = u if u <= L else 2 * L - u
        nv = max(2, int(hw * 4))
        for k in range(-nv, nv + 1):
            v = k / nv
            p = curve[i] + n[i] * side * v * hw
            x = int(round(p[0])); y = int(round(p[1]))
            if 0 <= x < W and 0 <= y < H:
                o = abs(v) * hw
                if hw - o < rand:
                    col = LIJN
                else:
                    vs = v * hw / max(hw - rand, 0.5) * binnen_src
                    vs = max(-binnen_src, min(binnen_src, vs)); col = strook.sample(u, vs)
                    f = 0.85
                    while np.all(col > 200) and f > 0.1:      # lichte randpixels van r5 overslaan: binnenwaarts bemonsteren
                        col = strook.sample(u, vs * f); f -= 0.15
                canvas[y, x] = col; cmask[y, x] = True
    gaatjes_dicht(canvas, cmask)
    return canvas

def laag():
    return np.zeros_like(A), np.zeros((H, W), bool)

def uitsnede(poly):
    m = poly_mask(poly) & niet_wit(A)
    ys, xs = np.where(m); x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    rgba = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    rgba[..., :3] = A[y0:y1, x0:x1]; rgba[..., 3] = m[y0:y1, x0:x1] * 255
    return Image.fromarray(rgba, 'RGBA'), (x0, y0)

def plak(canvas, cmask, img, pos):
    a = np.array(img); h, w = a.shape[:2]; x, y = pos
    m = a[..., 3] > 127
    sub = canvas[y:y+h, x:x+w]; sm = cmask[y:y+h, x:x+w]
    mm = m[:sub.shape[0], :sub.shape[1]]
    sub[mm] = a[:sub.shape[0], :sub.shape[1], :3][mm]; sm[mm] = True

def gaatjes_dicht(c, m, rondes=2):
    """bemonsteringsgaatjes in een getekende laag (>= 3 van 4 buren gevuld) vullen met een buurkleur."""
    for _ in range(rondes):
        nb = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        cnt = sum(_schuif(m, dx, dy).astype(int) for dx, dy in nb)
        gat = ~m & ((cnt >= 3) | (_schuif(m, 1, 0) & _schuif(m, -1, 0)) | (_schuif(m, 0, 1) & _schuif(m, 0, -1)))
        for dx, dy in nb:
            src = gat & _schuif(m, dx, dy)
            ys, xs = np.where(src)
            c[ys, xs] = c[ys - dy, xs - dx]; gat[ys, xs] = False; m[ys, xs] = True

def samen(lagen):
    out = np.tile(WIT, (H, W, 1)).copy()
    for c, m in lagen: out[m] = c[m]
    return out

def plaats_rot(canvas, cmask, srcmask, angle, src_anchor, dst_anchor):
    if angle == 0:
        return plaats_nn(canvas, cmask, srcmask, angle, src_anchor, dst_anchor)
    ys, xs = np.where(srcmask); x0, x1, y0, y1 = xs.min(), xs.max()+1, ys.min(), ys.max()+1
    rgba = np.zeros((y1-y0, x1-x0, 4), np.uint8); rgba[..., :3] = A[y0:y1, x0:x1]; rgba[..., 3] = srcmask[y0:y1, x0:x1]*255
    pal = np.unique(A[srcmask].reshape(-1, 3), axis=0).astype(int)
    im = Image.fromarray(rgba, 'RGBA')
    # premultiplied draaien om witte randen te vermijden
    big = im.resize((im.width*4, im.height*4), Image.NEAREST)
    cx, cy = (src_anchor[0]-x0)*4, (src_anchor[1]-y0)*4
    rot = big.rotate(angle, resample=Image.BICUBIC, center=(cx, cy), expand=False)
    pad = 400
    canvas4 = Image.new('RGBA', (big.width + 2*pad, big.height + 2*pad), (0, 0, 0, 0))
    big2 = Image.new('RGBA', canvas4.size, (0, 0, 0, 0)); big2.paste(big, (pad, pad))
    rot = big2.rotate(angle, resample=Image.BICUBIC, center=(cx+pad, cy+pad))
    small = np.array(rot.resize((rot.width//4, rot.height//4), Image.BOX)).astype(int)
    ox = dst_anchor[0] - (cx+pad)//4; oy = dst_anchor[1] - (cy+pad)//4
    hh, ww = small.shape[:2]
    for yy in range(hh):
        for xx in range(ww):
            a = small[yy, xx, 3]
            if a < 140: continue
            col = small[yy, xx, :3] * 255 / max(a, 1)
            k = np.argmin(((pal - col)**2).sum(1))
            qx, qy = xx + ox, yy + oy
            if 0 <= qx < W and 0 <= qy < H:
                canvas[qy, qx] = pal[k]; cmask[qy, qx] = True
    glad_rand(canvas, cmask)

def _schuif(m, dx, dy):
    o = np.zeros_like(m)
    o[max(dy,0):H+min(dy,0), max(dx,0):W+min(dx,0)] = m[max(-dy,0):H+min(-dy,0), max(-dx,0):W+min(-dx,0)]
    return o

def glad_rand(canvas, cmask, r=5, lijn=3):
    """zaagtanden van het draaien weg: masker vervagen + drempel, gaten vullen met buurkleur, buitenrand r5-lijnkleur."""
    f = cmask.astype(float)
    k = 2 * r + 1
    for ax in (0, 1):
        c = np.cumsum(np.pad(f, [(r + 1, r)] if False else ([(r + 1, r), (0, 0)] if ax == 0 else [(0, 0), (r + 1, r)])), axis=ax)
        f = (np.take(c, range(k, c.shape[ax]), axis=ax) - np.take(c, range(0, c.shape[ax] - k), axis=ax)) / k
    nieuw = (f > 0.5) & (cmask | (f > 0.5))
    # vullen
    todo = nieuw & ~cmask
    while todo.any():
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            bron = _schuif(cmask, dx, dy) & todo
            ys, xs = np.where(bron)
            canvas[ys, xs] = canvas[ys - dy, xs - dx]; cmask[ys, xs] = True; todo[ys, xs] = False
    cmask &= nieuw
    # rand
    e = cmask.copy()
    for _ in range(lijn):
        e = e & _schuif(e, 1, 0) & _schuif(e, -1, 0) & _schuif(e, 0, 1) & _schuif(e, 0, -1)
    band = cmask & ~e
    canvas[band] = LIJN

def plaats_nn(canvas, cmask, srcmask, angle, src_anchor, dst_anchor):
    """kopieer r5-pixels onder srcmask, gedraaid (graden, tegen de klok in beeld) zodat src_anchor op dst_anchor valt."""
    th = math.radians(angle); c, s = math.cos(th), math.sin(th)
    ys, xs = np.where(srcmask)
    pts = np.stack([xs - src_anchor[0], ys - src_anchor[1]], 1)
    fx = pts[:, 0]*c + pts[:, 1]*s; fy = -pts[:, 0]*s + pts[:, 1]*c
    x0, x1 = int(fx.min() + dst_anchor[0]) - 2, int(fx.max() + dst_anchor[0]) + 3
    y0, y1 = int(fy.min() + dst_anchor[1]) - 2, int(fy.max() + dst_anchor[1]) + 3
    for qy in range(max(0, y0), min(H, y1)):
        for qx in range(max(0, x0), min(W, x1)):
            dx, dy = qx - dst_anchor[0], qy - dst_anchor[1]
            sx = dx*c - dy*s + src_anchor[0]; sy = dx*s + dy*c + src_anchor[1]
            ix, iy = int(round(sx)), int(round(sy))
            if 0 <= ix < W and 0 <= iy < H and srcmask[iy, ix]:
                canvas[qy, qx] = A[iy, ix]; cmask[qy, qx] = True

def stadion(cl, cr, R, start_x, n=1200):
    """gesloten lus met de klok mee (boven naar rechts), begint en eindigt bij start_x op de bovenkant."""
    pts = []
    top = cl[1] - R; bot = cl[1] + R
    seg = []
    seg += [(x, top) for x in np.linspace(start_x, cr[0], 80)]
    seg += [(cr[0] + R*math.cos(a), cr[1] + R*math.sin(a)) for a in np.linspace(-math.pi/2, math.pi/2, 120)]
    seg += [(x, bot) for x in np.linspace(cr[0], cl[0], 120)]
    seg += [(cl[0] + R*math.cos(a), cl[1] + R*math.sin(a)) for a in np.linspace(math.pi/2, 3*math.pi/2, 120)]
    seg += [(x, top) for x in np.linspace(cl[0], start_x + 6, 80)]
    return polyline_dense(seg, 0.5)

def tip_dicht(canvas, cmask, curve, kleur, r=3):
    p = curve[-1]; d = curve[-1] - curve[-4]; d /= np.linalg.norm(d)
    for k in range(0, r + 2):
        q = p + d * k * 0.6
        for yy in range(int(q[1]) - r, int(q[1]) + r + 1):
            for xx in range(int(q[0]) - r, int(q[0]) + r + 1):
                if (xx - q[0])**2 + (yy - q[1])**2 <= (r - k*0.5)**2 + 0.5 and 0 <= xx < W and 0 <= yy < H:
                    if not cmask[yy, xx]:
                        canvas[yy, xx] = kleur; cmask[yy, xx] = True

# bronstroken uit r5
dA = np.array([0.65, 0.76]) / np.linalg.norm([0.65, 0.76])
pA = np.array([296.5, 285.0]) + dA * 14
STROOK_A = Strook(pA, pA + dA * 48, 15)                 # dunne kanontentakel (bovenste kanon r5)
STROOK_B = Strook((530, 458), (636, 458), 23)            # onderste tentakel r5 met gele wratten
ZWART = A[401, 560].copy()

def kop_snijrand(dikte=3):
    """band net buiten de kop, alleen waar de snede door r5-inhoud liep (oude krullen/kanonnen): daar krijgt de kop
    een r5-lijn op de tentakel die eronder ligt. Kop-pixels zelf blijven onaangeroerd."""
    d = kop_m.copy()
    for _ in range(dikte):
        d = d | _schuif(d, 1, 0) | _schuif(d, -1, 0) | _schuif(d, 0, 1) | _schuif(d, 0, -1)
    donker = kop_m & (A.astype(int).sum(2) < 150)
    for _ in range(dikte):
        donker = donker | _schuif(donker, 1, 0) | _schuif(donker, -1, 0) | _schuif(donker, 0, 1) | _schuif(donker, 0, -1)
    return d & ~kop_m & ~BG & ~donker

def bouw():
    lagen = []; voor = []          # voor = indices van lagen die vóór de kop liggen
    # 1 verre kanon (achter de kop; alleen langs de verre kopzijde ervoor, zoals de oude krul)
    c, m = laag()
    pad = keten(bezier([(300, 141), (385, 118), (452, 140), (440, 180)]),
                bezier([(440, 180), (430, 198), (402, 200), (399, 235)]),
                bezier([(399, 235), (397, 290), (405, 340), (430, 375)]))
    sweep(c, m, pad, lambda t: 15, STROOK_A, side=1)
    far_src = poly_mask([(150, 200), (240, 200), (299, 237), (269, 317), (150, 300)]) & (A.min(2) <= 200)
    plaats_rot(c, m, far_src, 28, (285, 280), (316, 138))
    lagen.append((c, m))
    BAND = poly_mask([(380, 150), (470, 150), (470, 203), (414, 206), (414, 266), (380, 266)])
    far_front = (c.copy(), m & BAND)
    # 2 rupsband: twee lussen onder het lijf
    for cl, cr, sx in [((370, 444), (500, 444), 440), ((530, 438), (690, 438), 610)]:
        c, m = laag()
        pad = stadion(cl, cr, 30, sx)
        sweep(c, m, pad, lambda t: 23, STROOK_B, side=1)
        lagen.append((c, m))
    # 3 nabije kanon: tentakel + loop
    cn, mn = laag()
    pad = keten(bezier([(630, 146), (690, 146), (668, 215), (652, 275)]),
                bezier([(652, 275), (642, 310), (645, 350), (625, 385)]))
    sweep(cn, mn, pad, lambda t: 22, STROOK_A, side=1, scale=15/22)
    near_src = poly_mask([(236, 381), (330, 381), (345, 386), (450, 386), (450, 472), (236, 488)]) & (A.min(2) <= 200)
    plaats_rot(cn, mn, near_src, 0, (272, 433), (455, 150))
    yy = np.arange(H)[:, None] * np.ones((1, W))
    lagen.append((cn, mn & (yy >= 300)))          # onderste deel achter de kop (wortel onder de kop)
    # 4 gespreide tentakels (wortel onder de kop)
    hwf = lambda t: 21 * (1 - t) ** 0.8 + 4
    for pts, side in [([(565, 352), (450, 392), (320, 405), (215, 485)], -1),
                      ([(600, 345), (715, 410), (800, 420), (865, 485)], 1)]:
        c, m = laag(); pad = bezier(pts, 900)
        sweep(c, m, pad, hwf, STROOK_B, side=side, scale=0.9)
        tip_dicht(c, m, pad, LIJN)
        lagen.append((c, m))
    # 5 r5-lijn langs de snijranden van de kop (buiten de kop)
    onder = np.zeros((H, W), bool)
    for _, mm in lagen: onder |= mm
    c, m = laag(); band = kop_snijrand() & onder; c[band] = LIJN; m |= band; lagen.append((c, m))
    # 6 kop
    c, m = laag(); c[kop_m] = A[kop_m]; m |= kop_m; lagen.append((c, m))
    # 7 voor de kop: verre kanon langs de verre kopzijde, nabije kanon bovendeel
    voor.append(len(lagen)); lagen.append(far_front)
    voor.append(len(lagen)); lagen.append((cn, mn & (yy < 300)))
    return samen(lagen), lagen, voor

if __name__ == '__main__':
    out, lagen, voor = bouw()
    Image.fromarray(out).save(os.path.join(HIER, 'model_v1.png'))
    # vel: r5 | model_v1
    v = Image.new('RGB', (W * 2 + 20, H), 'white'); v.paste(R5, (0, 0)); v.paste(Image.fromarray(out), (W + 20, 0))
    v.resize((1000, int(H * 1000 / (W * 2 + 20))), Image.LANCZOS).save(os.path.join(HIER, 'vel_v1.png'))
    # pixeldiff kop
    kop_vis = np.ones((H, W), bool)
    bedekt = np.zeros((H, W), bool)
    for i in voor: bedekt |= lagen[i][1]
    diff = np.any(out != A, axis=2) & kop_m
    print('kopgebied px:', kop_m.sum(), 'afwijkend:', diff.sum(), 'waarvan door tentakels ervoor bedekt:', (diff & bedekt).sum(),
          'afwijkend en niet bedekt:', (diff & ~bedekt).sum())
