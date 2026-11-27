# Extra hulpjes frame 2 per script, batch B (27 nov). Alles verplaatst alleen bestaande pixels:
# verschuiven, rekken (rij dubbel), knijpen (rij weg), per rij/kolom schuiven (buigen) en draaien
# met drie shears (Paeth): een permutatie van het raster, dus geen gaten en geen dubbele pixels.
import math, numpy as np
import scipy.ndimage as nd

YY, XX = np.mgrid[0:64, 0:64]

def comps(x, mask=None):
    m = (x > 0) if mask is None else mask
    lab, n = nd.label(m, np.ones((3, 3)))
    return [lab == i for i in range(1, n+1)]

def schuif(x, mask, dx, dy, wis=True):
    """mask-pixels dx,dy verplaatsen; oude plek leeg (wis) of laten staan (rek)."""
    o = x.copy()
    if wis: o[mask] = 0
    ys, xs = np.where(mask); ny, nx = ys+dy, xs+dx
    ok = (ny >= 0) & (ny < 64) & (nx >= 0) & (nx < 64)
    assert ok.all(), 'deel valt uit het vak'
    o[ny, nx] = x[ys, xs]
    return o

def rek(x, r, d, mask=None):
    """Alles boven rij r (binnen mask) d px omhoog; rijen r-d..r-1 blijven ook staan (rij dubbel)."""
    m = (YY < r) & (x > 0)
    if mask is not None: m &= mask
    o = x.copy(); o[m & (YY < r-d)] = 0
    ys, xs = np.where(m); assert (ys-d >= 0).all(), 'deel valt uit het vak'
    o[ys-d, xs] = x[ys, xs]
    return o

def knijp(x, r, d, mask=None):
    """Alles boven rij r (binnen mask) d px omlaag; rijen r..r+d-1 verdwijnen (rij weg)."""
    m = (YY < r) & (x > 0)
    if mask is not None: m &= mask
    o = x.copy()
    o[m] = 0
    band = (YY >= r) & (YY < r+d)
    if mask is not None: band &= mask
    o[band] = 0
    ys, xs = np.where(m); o[ys+d, xs] = x[ys, xs]
    return o

def rijschuif(x, mask, dxf):
    """Per rij y de mask-pixels dxf(y) px horizontaal (buigen/zwiepen); hele rij gaat mee, dus omlijning blijft."""
    o = x.copy(); o[mask] = 0
    ys, xs = np.where(mask)
    for y, c in zip(ys, xs):
        nc = c+dxf(y); assert 0 <= nc < 64
        o[y, nc] = x[y, c]
    return o

def kolomschuif(x, mask, dyf):
    o = x.copy(); o[mask] = 0
    ys, xs = np.where(mask)
    for y, c in zip(ys, xs):
        ny = y+dyf(c); assert 0 <= ny < 64
        o[ny, c] = x[y, c]
    return o

def _paeth(u, v, th):
    a = -math.tan(th/2); b = math.sin(th)
    u = u + np.round(a*v).astype(int)
    v = v + np.round(b*u).astype(int)
    u = u + np.round(a*v).astype(int)
    return u, v

def draai(x, mask, graden, cx, cy, dx=0, dy=0):
    """Deel draaien met drie shears rond (cx,cy) (+ = tegen de klok in, zoals PIL), daarna dx,dy schuiven."""
    o = x.copy(); o[mask] = 0
    ys, xs = np.where(mask)
    u, v = xs-int(cx), ys-int(cy)
    u2, v2 = _paeth(u, -v, math.radians(graden))   # y-as omhoog
    nx, ny = u2+int(cx)+dx, -v2+int(cy)+dy
    ok = (nx >= 0) & (nx < 64) & (ny >= 0) & (ny < 64)
    assert ok.all(), 'draaien valt uit het vak'
    o[ny, nx] = x[ys, xs]
    return o

def baan(x, delen, graden, cx, cy, knip=False):
    """Losse delen als geheel langs een baan om (cx,cy) verplaatsen (deel zelf draait niet: geen rafels)."""
    o = x.copy()
    for m in delen: o[m] = 0
    th = math.radians(graden)
    for m in delen:
        ys, xs = np.where(m); mx, my = xs.mean()-cx, ys.mean()-cy
        nx = mx*math.cos(th)+my*math.sin(th); ny = -mx*math.sin(th)+my*math.cos(th)
        dx, dy = int(round(nx-mx)), int(round(ny-my))
        ok = (ys+dy >= 0) & (ys+dy < 64) & (xs+dx >= 0) & (xs+dx < 64)
        assert knip or ok.all(), 'baan valt uit het vak'
        o[ys[ok]+dy, xs[ok]+dx] = x[ys[ok], xs[ok]]
    return o

def radiaal(x, delen, cx, cy, n=1, wis=True):
    """Losse delen n px van het midden af (wis=False: deel wordt langer, de voet blijft staan)."""
    o = x.copy()
    if wis:
        for m in delen: o[m] = 0
    for m in delen:
        ys, xs = np.where(m); mx, my = xs.mean()-cx, ys.mean()-cy; L = math.hypot(mx, my) or 1
        dx, dy = int(round(n*mx/L)), int(round(n*my/L))
        o[ys+dy, xs+dx] = x[ys, xs]
    return o

def epx(x):
    """Scale2x (EPX) op indexwaarden: 2x groter, diagonalen blijven glad."""
    H, W = x.shape; p = np.pad(x, 1, mode='edge')
    P = p[1:-1, 1:-1]; A = p[:-2, 1:-1]; B = p[1:-1, 2:]; C = p[1:-1, :-2]; D = p[2:, 1:-1]
    o = np.zeros((2*H, 2*W), x.dtype)
    o[0::2, 0::2] = np.where((C == A) & (C != D) & (A != B), A, P)
    o[0::2, 1::2] = np.where((A == B) & (A != C) & (B != D), B, P)
    o[1::2, 0::2] = np.where((D == C) & (D != B) & (C != A), C, P)
    o[1::2, 1::2] = np.where((B == D) & (B != A) & (D != C), D, P)
    return o

def rotsprite(x, mask, graden, cx, cy, dx=0, dy=0, knip=False):
    """Deel draaien zoals RotSprite: 8x met Scale2x, nearest draaien, terug met de middelste pixel per 8x8-vak.
    Geen nieuwe kleuren; randen blijven doorlopende lijnen. + = tegen de klok in."""
    from PIL import Image
    deel = np.where(mask, x, 0).astype(np.uint8)
    g = epx(epx(epx(deel)))
    G = Image.fromarray(g, 'L').rotate(graden, resample=Image.NEAREST, center=(cx*8+4, cy*8+4), fillcolor=0)
    r = np.array(G)[4::8, 4::8]
    o = x.copy(); o[mask] = 0
    ys, xs = np.where(r > 0)
    ny, nx = ys+dy, xs+dx
    ok = (ny >= 0) & (ny < 64) & (nx >= 0) & (nx < 64)
    assert knip or ok.all(), 'draaien valt uit het vak'
    o[ny[ok], nx[ok]] = r[ys[ok], xs[ok]]
    return o

def rotsprite_gezicht(x, mask, gezicht, graden, cx, cy, dx=0, dy=0):
    """Als rotsprite, maar het gezicht (ogen/mond) draait niet mee: het gaat als vast blok mee naar zijn
    nieuwe plek, zodat ogen 1-op-1 blijven. De plek eronder wordt vóór het draaien dichtgezet met de
    dichtstbijzijnde huidpixel van hetzelfde deel."""
    src = x.copy()
    huid = mask & ~gezicht
    _, (iy, ix) = nd.distance_transform_edt(~huid, return_indices=True)
    src[gezicht] = x[iy[gezicht], ix[gezicht]]
    o = rotsprite(src, mask, graden, cx, cy, dx, dy)
    ys, xs = np.where(gezicht); u, v = xs.mean()-cx, ys.mean()-cy; th = math.radians(graden)
    ddx = int(round(u*math.cos(th)+v*math.sin(th)-u))+dx; ddy = int(round(-u*math.sin(th)+v*math.cos(th)-v))+dy
    o[ys+ddy, xs+ddx] = x[ys, xs]
    return o

def gaten_dicht(o, a, deel):
    """Losse gaatjes (transparant, ≥3 van 4 buren gevuld, in frame 1 bezet door het deel) dicht met de
    meest voorkomende buurkleur."""
    o = o.copy()
    for _ in range(2):
        p = np.pad(o, 1); bur = np.stack([p[:-2, 1:-1], p[2:, 1:-1], p[1:-1, :-2], p[1:-1, 2:]])
        gat = (o == 0) & deel & ((bur > 0).sum(0) >= 3)
        for y, c in zip(*np.where(gat)):
            v = [b for b in bur[:, y, c] if b > 0]; o[y, c] = max(set(v), key=v.count)
    return o
