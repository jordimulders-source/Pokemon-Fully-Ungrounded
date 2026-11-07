"""3D-poppetjes uit ellipsoïden en buizen (bollenketens), met een z-buffer-render.
Elk onderdeel heeft een materiaal (kleurgroep) en een deel-label (voor binnenlijnen: een poot vóór het lijf
krijgt een lijn, lijf en staart die in elkaar overlopen niet). Diercoördinaten: x naar achteren, y omhoog,
z naar de kijker bij yaw 0 (dier kijkt naar links)."""
import math
import numpy as np


def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_x(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rot_z(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def qb(a, c, b, n):
    a, c, b = map(np.array, (a, c, b))
    return [tuple((1 - t) ** 2 * a + 2 * (1 - t) * t * c + t * t * b) for t in np.linspace(0, 1, n)]


class Model:
    def __init__(self):
        self.parts = []      # (center, radii, R0, materiaal, deel)
        self.points = {}     # benoemde punten (oog, neus) voor sjablonen
        self.texture = None  # f(q_dier[N,3], materiaal_namen[N]) -> materiaal_namen[N]

    def ell(self, c, r, mat, part, R0=None):
        self.parts.append((np.array(c, float), np.array(r if np.ndim(r) else (r, r, r), float),
                           np.eye(3) if R0 is None else R0, mat, part))

    def turn(self, parts, pivot, R, points=()):
        """Draai een groep delen (bijv. de kop) om een scharnierpunt: in Gen 3-sprites draait de kop
        verder naar de kijker dan het lijf."""
        pv = np.array(pivot, float)
        new = []
        for c, r, R0, mat, part in self.parts:
            if part in parts:
                c = pv + R @ (c - pv)
                R0 = R @ R0
            new.append((c, r, R0, mat, part))
        self.parts = new
        for k in points:
            self.points[k] = tuple(pv + R @ (np.array(self.points[k]) - pv))

    def chain(self, pts, mat, part, step=1.5):
        """Getaperde buis: bollen langs punten (x, y, z, straal)."""
        for a, b in zip(pts, pts[1:]):
            a, b = np.array(a, float), np.array(b, float)
            n = max(2, int(np.linalg.norm(b[:3] - a[:3]) / step))
            for i in range(n):
                p = a + (b - a) * i / n
                self.ell(p[:3], p[3], mat, part)
        p = np.array(pts[-1], float)
        self.ell(p[:3], p[3], mat, part)


def camera(yaw, pitch, stretch_x=1.0):
    """stretch_x > 1: beeld breder maken (spriteverhoudingen; in 3/4 oogt een lijf anders te kort)."""
    return np.diag((stretch_x, 1, 1)) @ rot_x(math.radians(pitch)) @ rot_y(math.radians(yaw))


def bbox(m, Rc):
    pts = np.array([Rc @ c for c, *_ in m.parts])
    rs = np.array([r.max() for _, r, *_ in m.parts])
    return (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()


def render(m, Rc, size, scale, origin):
    """Render op een raster van size x size. origin = wereldcoördinaat (x, y) van pixel (0, 0); scale = px per eenheid.
    Geeft: materiaal-index, deel-index, diepte, normaal (camera), dierpunt per pixel, plus de namenlijsten."""
    mats = sorted({p[3] for p in m.parts})
    parts = sorted({p[4] for p in m.parts})
    z = np.full((size, size), -1e9, np.float32)
    mat = np.full((size, size), -1, np.int16)
    prt = np.full((size, size), -1, np.int16)
    nrm = np.zeros((size, size, 3), np.float32)
    wpt = np.zeros((size, size, 3), np.float32)
    ys, xs = np.mgrid[0:size, 0:size]
    wx = origin[0] + (xs + 0.5) / scale
    wy = origin[1] - (ys + 0.5) / scale
    for c, r, R0, mname, pname in m.parts:
        cw = Rc @ c
        M = np.diag(1 / r) @ R0.T @ Rc.T
        ext = r.max()
        x0 = max(0, int((cw[0] - ext - origin[0]) * scale) - 2); x1 = min(size, int((cw[0] + ext - origin[0]) * scale) + 3)
        y0 = max(0, int((origin[1] - cw[1] - ext) * scale) - 2); y1 = min(size, int((origin[1] - cw[1] + ext) * scale) + 3)
        if x0 >= x1 or y0 >= y1:
            continue
        px = wx[y0:y1, x0:x1] - cw[0]
        py = wy[y0:y1, x0:x1] - cw[1]
        a = M[:, 0, None, None] * px + M[:, 1, None, None] * py
        b = M[:, 2]
        A = b @ b
        B = 2 * (a * b[:, None, None]).sum(0)
        C = (a * a).sum(0) - 1
        disc = B * B - 4 * A * C
        hit = disc >= 0
        zz = (-B + np.sqrt(np.where(hit, disc, 0))) / (2 * A) + cw[2]
        sub = z[y0:y1, x0:x1]
        win = hit & (zz > sub)
        sub[win] = zz[win]
        mat[y0:y1, x0:x1][win] = mats.index(mname)
        prt[y0:y1, x0:x1][win] = parts.index(pname)
        p = np.stack([px, py, zz - cw[2]], -1)
        n = p @ (M.T @ M).T
        n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9
        nrm[y0:y1, x0:x1][win] = n[win]
        q = np.stack([wx[y0:y1, x0:x1], wy[y0:y1, x0:x1], zz], -1)
        wpt[y0:y1, x0:x1][win] = q[win]
    animal = wpt @ np.linalg.inv(Rc).T
    if m.texture is not None:
        sel = mat >= 0
        names = np.array(mats + [''], dtype=object)[mat[sel]]
        new = m.texture(animal[sel], names)
        allm = sorted(set(mats) | set(new))
        remap = np.array([allm.index(n) for n in mats], np.int16)
        mat2 = mat.copy()
        mat2[sel] = np.array([allm.index(n) for n in new], np.int16)
        mat, mats = mat2, allm
    return dict(mat=mat, part=prt, z=z, n=nrm, animal=animal, mats=mats, parts=parts)
