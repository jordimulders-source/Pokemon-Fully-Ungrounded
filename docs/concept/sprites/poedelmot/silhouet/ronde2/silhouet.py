"""Poedelmot silhouet ronde 2, stap 2: het silhouet (64x64, één kleur).
- Massa (lijf, wol, vleugels) = het poppetje ronde 5b op de 50%-grens (bron.py -> dekking_kaal.npy), alleen korrels weg.
- Kop: eigen ronde wolbol (inspiratie vilt-mot, Jordi 6 nov: "dit mag als inspiratie voor hoofd, gezicht en oren"),
  op de plek en maat van de poppetjekop. Ogen als kleine kraaloogjes zoals het vilt (Jordi 6 nov: "zoals in deze foto"); alleen in delen.txt.
- Oren (kamsprieten): met de hand. Plek, lengte en richting opzij uit het poppetje (spriet_as.npy), bladvorm naar de
  vilt-mot (breed blad met spitse punt, schuin omhoog opzij), tanden van de kam zichtbaar in de omtrek (1 px tand, 1 px lucht) aan de bovenkant; onderkant gesloten bladrand.
- Poten: met de hand naar de tak-foto (poppetje/ronde3/overlay_poten.png) en Jordi: "2 voorste poten zijn zichtbaarder, de
  andere vier staan dichter op elkaar per twee". Dik en wollig, pompon onderaan; verre poten hoger en kleiner.
- Daarna het geheel omlaag geschoven zodat de onderste pompon op y62 staat (zoals Gen 3-sprites op de grond staan).
Schrijft ronde2.txt, delen.txt (per onderdeel), silhouet_1x.png, silhouet_8x.png, delen_8x.png.
Draaien: python3 docs/concept/sprites/poedelmot/silhouet/ronde2/silhouet.py"""
import os, math
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
SS = 12   # subpixels per spritepixel voor de handvormen

yy, xx = (np.mgrid[0:64 * SS, 0:64 * SS] + 0.5) / SS
def bol(cx, cy, r): return (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r
def capsule(p, q, r0, r1):
    p, q = np.array(p, float), np.array(q, float); d = q - p; L2 = d @ d
    t = np.clip(((xx - p[0]) * d[0] + (yy - p[1]) * d[1]) / L2, 0, 1)
    r = r0 + (r1 - r0) * t
    return (xx - p[0] - t * d[0]) ** 2 + (yy - p[1] - t * d[1]) ** 2 <= r * r
def naar1x(m): return m.reshape(64, SS, 64, SS).mean((1, 3)) >= 0.5

# --- poten: (punten heup -> knie -> voet met straal), pompon = (cx, cy, r) + twee zijlobben
POTEN = {
    'voor ver':      ([(15.6, 41.0, 2.3), (12.0, 46.0, 2.0), (10.6, 50.0, 1.9)], (10.3, 52.2, 2.9)),
    'midden ver':    ([(18.0, 43.0, 1.6), (16.6, 45.6, 1.5)], (16.3, 47.0, 1.9)),
    'achter ver':    ([(19.6, 43.0, 1.5), (18.8, 45.4, 1.4)], (18.6, 46.4, 1.7)),
    'voor nabij':    ([(21.5, 42.0, 2.9), (20.0, 48.0, 2.6), (20.6, 52.6, 2.4)], (20.8, 55.0, 4.0)),
    'midden nabij':  ([(30.0, 44.0, 2.5), (31.6, 49.0, 2.2), (31.3, 52.0, 2.1)], (31.3, 54.2, 3.4)),
    'achter nabij':  ([(35.2, 43.0, 2.3), (37.3, 47.4, 2.1), (37.4, 50.0, 1.9)], (37.6, 52.0, 3.0)),
}
def poot(pts, pp):
    m = np.zeros_like(xx, bool)
    for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]): m |= capsule((x0, y0), (x1, y1), r0, r1)
    cx, cy, r = pp
    m |= bol(cx, cy, r) | bol(cx - r * 0.55, cy + r * 0.3, r * 0.7) | bol(cx + r * 0.55, cy + r * 0.3, r * 0.7)
    return m

# --- kop: ronde wolbol op de plek van de poppetjekop
KOP = (24.0, 24.4, 9.3)

# --- ogen (Jordi 6 nov: "zoals in deze foto" = vilt_hoofd_gezicht_oren.png): kleine zwarte kraaloogjes, iets onder het
# midden van de kop, uit elkaar. Vilt: oog 0,15 x kopbreedte (22/145 px), hart-op-hart 0,34 (50/145), hoogte 0,47 van de kop.
# Op 45° het verre oog smaller en dichterbij. Alleen in delen (binnen de kop, het silhouet verandert er niet door).
OGEN = [(24.2, 24.0, 1.5, 2.0), (19.4, 23.8, 1.0, 1.6)]   # (cx, cy, halve breedte, halve hoogte): nabij, ver
def ovaal(cx, cy, rx, ry): return ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1

# --- oren: basis, punt (uit de spriet-as van het poppetje, punt iets hoger: vilt-blad schuin omhoog), halve breedte
OREN = {'nabij': ((30.0, 20.6), (47.0, 14.0), 4.2), 'ver': ((18.0, 20.2), (3.2, 14.2), 3.8)}
def oor(basis, punt, W):
    b, p = np.array(basis), np.array(punt); u = (p - b) / np.linalg.norm(p - b); n = np.array((u[1], -u[0]))
    Ln = np.linalg.norm(p - b)
    t = ((xx - b[0]) * u[0] + (yy - b[1]) * u[1]) / Ln; s = (xx - b[0]) * n[0] + (yy - b[1]) * n[1]
    prof = W * np.clip(np.sin(math.pi * np.clip(t, 0, 1) ** 0.75), 0, 1) ** 0.8 + 0.6 * (1 - np.clip(t, 0, 1))
    op = -1.0 if n[1] > 0 else 1.0   # teken van s aan de bovenkant van het oor
    # onderkant: gesloten bladrand (ligt grotendeels over kop en vleugel; losse tanden gaven daar gaatjes van 1 px);
    # bovenkant: kern + kamtanden
    kern = (t >= 0) & (t <= 1) & (((s * op <= 0) & (-s * op <= prof)) | ((s * op > 0) & (s * op <= np.maximum(prof - 2.0, 0.55))))
    m1 = naar1x(kern)
    # tanden: elke 2 px langs de as, 1 px breed, schuin naar de punt (zoals de strepen op het vilt), tot de bladrand
    tand = np.zeros((64, 64), bool)
    for ti in np.arange(2.0, Ln - 1.0, 2.0):
        tt = ti / Ln; w = W * math.sin(math.pi * tt ** 0.75) ** 0.8 + 0.6 * (1 - tt)
        if w < 1.6: continue
        for sg in (op,):
            for j in np.linspace(0, w, 12):
                q = b + u * (ti + 0.45 * j) + n * sg * j
                tand[int(q[1]), int(q[0])] = True
    return m1 | tand, m1

def bouw():
    kaal = np.load(os.path.join(HERE, 'dekking_kaal.npy')) >= 0.5
    delen = np.zeros((64, 64), '<U1'); delen[:] = '.'
    delen[kaal] = 'L'
    kop = naar1x(bol(*KOP)); delen[kop] = 'K'
    S = kaal | kop
    for naam, (pts, pp) in POTEN.items():
        m = naar1x(poot(pts, pp)); S |= m
        delen[m & (delen == '.')] = 'p' if 'ver' in naam else 'P'
    for naam, (b, p, W) in OREN.items():
        m, _ = oor(b, p, W); S |= m; delen[m] = 'S'
    for o in OGEN: delen[naar1x(ovaal(*o))] = 'O'
    return S, delen

_k = open(os.path.join(HERE, 'korrel.py')).read(); exec(_k[_k.index('def sq'):_k.index('for p in sys.argv')])

def oorzone(dy):
    z = np.zeros((64, 64), bool)
    for b, p, W in OREN.values():
        bb, pp = np.array(b), np.array(p); u = (pp - bb) / np.linalg.norm(pp - bb); n = np.array((u[1], -u[0]))
        Ln = np.linalg.norm(pp - bb)
        t = ((xx - bb[0]) * u[0] + (yy - bb[1]) * u[1]) / Ln; s = (xx - bb[0]) * n[0] + (yy - bb[1]) * n[1]
        op = -1.0 if n[1] > 0 else 1.0
        z |= naar1x((t > -0.05) & (t < 1.08) & (s * op >= 0.3) & (s * op <= W + 1.6))   # alleen de kamkant (boven)
    return np.roll(z, dy, 0)

def glad(S, cov, vrij):
    """Korrels weg buiten de oren (daar zijn de tanden juist de bedoeling). Probeert 1- en 2-px-flips rond elke korrel;
    kiest op minste korrels en dan op kosten: in de poppetjemassa |dekking - 0,5|, in de handvormen (poten, kop) 0,5."""
    import itertools
    def tel(T):
        u, i, t = korrels(T)
        return int((u & ~vrij).sum() + (i & ~vrij).sum()) + sum(1 for x, y, _ in t if not vrij[y, x])
    S0 = S.copy(); log = []
    kost = lambda T: float(np.where(np.isnan(cov), 0.5, np.abs(np.nan_to_num(cov) - 0.5))[T != S0].sum())
    while True:
        k0 = tel(S)
        if k0 == 0: break
        u, i, t = korrels(S)
        pts = {(y, x) for y, x in zip(*np.nonzero((u | i) & ~vrij))} | {(y, x) for x, y, _ in t if not vrij[y, x]}
        cand = sorted({(y + a, x + b) for y, x in pts for a in range(-2, 3) for b in range(-2, 3)
                       if 0 <= y + a < 64 and 0 <= x + b < 64 and not vrij[y + a, x + b]})
        best = None
        for fl in [(p,) for p in cand] + [q for q in itertools.combinations(cand, 2) if abs(q[0][0] - q[1][0]) <= 2 and abs(q[0][1] - q[1][1]) <= 2]:
            T = S.copy()
            for p in fl: T[p] = ~T[p]
            sc = (tel(T), kost(T))
            if best is None or sc < best[0]: best = (sc, fl)
        if best[0][0] >= k0: log.append(f'vast op {k0} korrels'); break
        for p in best[1]: S[p] = ~S[p]
        log.append(' '.join(f'{"+" if S[y, x] else "-"}x{x} y{y}' for y, x in best[1]))
    return S, log

if __name__ == '__main__':
    S, D = bouw()
    ys, xs = np.nonzero(S); dy = 62 - ys.max()
    S = np.roll(S, dy, 0); D = np.roll(D, dy, 0)
    cov = np.roll(np.load(os.path.join(HERE, 'dekking_kaal.npy')), dy, 0)
    cov = np.where(np.isin(D, ['L', '.']), cov, np.nan)   # alleen poppetjemassa telt op dekking
    S, log = glad(S, cov, oorzone(dy))
    for y, x in zip(*np.nonzero(S & (D == '.'))):   # door glad() bijgekomen pixels: label van de buren
        b = [c for c in D[max(0, y - 1):y + 2, max(0, x - 1):x + 2].ravel() if c not in '.O']
        D[y, x] = max(set(b), key=b.count) if b else 'L'
    D[~S] = '.'
    print('glad:', '; '.join(log))
    open(os.path.join(HERE, 'glad_log.txt'), 'w').write('\n'.join(log) + '\n')
    Image.fromarray(np.where(S, 0, 255).astype(np.uint8)).save(os.path.join(HERE, 'silhouet_1x.png'))
    Image.fromarray(np.where(S, 0, 255).astype(np.uint8)).resize((512, 512), Image.NEAREST).save(os.path.join(HERE, 'silhouet_8x.png'))
    KL = {'.': (255, 255, 255), 'L': (60, 60, 60), 'K': (95, 95, 150), 'S': (140, 85, 45), 'P': (40, 110, 40),
          'p': (130, 170, 130), 'O': (220, 40, 40)}
    Image.fromarray(np.array([[KL[c] for c in r] for r in D], np.uint8)).resize((512, 512), Image.NEAREST).save(
        os.path.join(HERE, 'delen_8x.png'))
    print('verschoven', dy, 'px omlaag; px', int(S.sum()), 'box x', xs.min(), xs.max(), 'y', ys.min() + dy, ys.max() + dy)
    open(os.path.join(HERE, 'ronde2.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in S) + '\n')
    open(os.path.join(HERE, 'delen.txt'), 'w').write('\n'.join(''.join(r) for r in D) + '\n')
