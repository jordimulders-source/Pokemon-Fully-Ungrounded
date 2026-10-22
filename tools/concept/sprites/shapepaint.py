"""shapepaint: een fakemon-sprite opbouwen uit vormen met onderdelen (Pokémon-stijl).

Idee: teken objecten (ellips, polygoon, dikke lijn) in z-volgorde; elk object hoort
bij een onderdeel (ramp in het palet). Daarna automatisch:
- egale vlakken met een schaduwsikkel rechtsonder (verschoven masker, licht linksboven);
- 1 px omlijning (index 15) met selout: boven/links de donkerste tint van het onderdeel;
- binnenlijnen waar een object vóór een ander object ligt (zwart of donkerste tint);
- daarna handwerk per pixel via ASCII-patches (`patch`).

Gebruik (zie docs/concept/sprites/olinguito/ronde2/bron/build.py):
    c = Canvas(64, 64, ramps)        # ramps: {'vacht': [hl, basis, schaduw, donker], ...}
    c.ellipse('kop', 'vacht', 26, 23, 11.5, 10.5)
    ...
    idx = c.render()                  # 64x64 indexarray
    patch(idx, x, y, ['..a', ...], {'a': 15})
"""
import math
import numpy as np
from PIL import Image

OUTLINE = 15


def gba(c):
    """Rond een (r,g,b) af op 15-bit GBA-kleuren."""
    return tuple(round(v / 255 * 31) * 255 // 31 for v in c)


def hexc(h):
    h = h.lstrip('#')
    return gba(tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)))


class Obj:
    def __init__(self, name, part, mask, line=None, shade=2.0, hl=None, flat=False, tone=1, z=0):
        self.name, self.part, self.mask = name, part, mask
        self.line, self.shade, self.hl, self.flat, self.tone, self.z = line, shade, hl, flat, tone, z
        self.nocast = False  # True: werpt geen slagschaduw (render3)
        self.paint = None   # optionele functie (x, y) -> index of None (eigen patroon, bijv. ringen)


class Canvas:
    def __init__(self, w, h, ramps):
        self.w, self.h, self.ramps = w, h, ramps
        self.objs = []
        yy, xx = np.mgrid[0:h, 0:w]
        self.xx, self.yy = xx + 0.5, yy + 0.5

    # ---- vormen -------------------------------------------------------
    def _add(self, name, part, mask, **kw):
        for o in self.objs:            # zelfde naam = zelfde object (vorm samenvoegen)
            if o.name == name:
                o.mask |= mask
                return o
        o = Obj(name, part, mask, **kw)
        self.objs.append(o)
        return o

    def ellipse_mask(self, cx, cy, rx, ry, rot=0.0):
        x, y = self.xx - cx, self.yy - cy
        if rot:
            a = math.radians(rot)
            x, y = x * math.cos(a) + y * math.sin(a), -x * math.sin(a) + y * math.cos(a)
        return (x / rx) ** 2 + (y / ry) ** 2 <= 1.0

    def poly_mask(self, pts):
        from PIL import ImageDraw
        im = Image.new('L', (self.w, self.h), 0)
        ImageDraw.Draw(im).polygon([(x, y) for x, y in pts], fill=1)
        return np.array(im).astype(bool)

    def tube_mask(self, pts, widths, steps=12):
        """Dikke lijn langs een polyline; breedte lineair per segment. Geeft ook t (0..1) per pixel."""
        m = np.zeros((self.h, self.w), bool)
        tmap = np.full((self.h, self.w), -1.0)
        dbest = np.full((self.h, self.w), 1e9)
        seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        L = sum(seg)
        acc = 0.0
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            for k in range(steps + 1):
                f = k / steps
                x, y = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
                r = (widths[i] + (widths[i + 1] - widths[i]) * f) / 2
                d = np.hypot(self.xx - x, self.yy - y)
                inside = d <= r
                m |= inside
                better = inside & (d < dbest)
                dbest[better] = d[better]
                tmap[better] = (acc + seg[i] * f) / L
            acc += seg[i]
        return m, tmap

    def ellipse(self, name, part, cx, cy, rx, ry, rot=0.0, **kw):
        return self._add(name, part, self.ellipse_mask(cx, cy, rx, ry, rot), **kw)

    def poly(self, name, part, pts, **kw):
        return self._add(name, part, self.poly_mask(pts), **kw)

    def tube(self, name, part, pts, widths, **kw):
        m, t = self.tube_mask(pts, widths)
        o = self._add(name, part, m, **kw)
        o.t = t
        return o

    def claw(self, name, pts, w0=2.0, w1=0.9, part='klauw', **kw):
        """Gekromde haakklauw: dikke basis, dunne punt."""
        widths = [w0 + (w1 - w0) * i / (len(pts) - 1) for i in range(len(pts))]
        kw.setdefault('line', 'black')
        kw.setdefault('shade', 1.0)
        return self.tube(name, part, pts, widths, **kw)

    # ---- renderen -----------------------------------------------------
    def render(self, dither=False):
        h, w = self.h, self.w
        owner = np.full((h, w), -1)
        for i, o in enumerate(self.objs):
            owner[o.mask] = i
        idx = np.zeros((h, w), np.uint8)
        fig = owner >= 0

        def at(m, x, y):
            return 0 <= x < w and 0 <= y < h and m[y, x]

        for i, o in enumerate(self.objs):
            r = self.ramps[o.part]
            base = r[o.tone] if len(r) > o.tone else r[-1]
            sh = r[min(o.tone + 1, len(r) - 1)]
            ys, xs = np.nonzero(owner == i)
            for y, x in zip(ys, xs):
                c = base
                if not o.flat:
                    s = o.shade
                    dx, dy = int(round(s * 0.6)), int(round(s))
                    if not at(o.mask, x + dx, y + dy) or not at(o.mask, x + dx + 1, y + dy // 2):
                        c = sh
                    if o.hl is not None and o.tone > 0:
                        hx, hy, hr = o.hl
                        if (x + 0.5 - hx) ** 2 + (y + 0.5 - hy) ** 2 <= hr * hr and at(o.mask, x - 1, y - 1):
                            c = r[o.tone - 1]
                if o.paint is not None:
                    p = o.paint(x, y, c)
                    if p is not None:
                        c = p
                idx[y, x] = c
        # binnenlijnen: object vóór een eerder object
        out = idx.copy()
        for i, o in enumerate(self.objs):
            if not o.line:
                continue
            ys, xs = np.nonzero(owner == i)
            for y, x in zip(ys, xs):
                for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + ddx, y + ddy
                    if 0 <= nx < w and 0 <= ny < h and 0 <= owner[ny, nx] < i and not o.mask[ny, nx]:
                        if self.objs[owner[ny, nx]].part in getattr(o, 'noline_against', ()):
                            continue
                        out[y, x] = OUTLINE if o.line == 'black' else self.ramps[o.part][-1]
                        break
        idx = out
        # buitenrand + selout
        shell = np.zeros((h, w), bool)
        for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sh_ = np.zeros((h, w), bool)
            ys, xs = np.nonzero(fig)
            for y, x in zip(ys, xs):
                nx, ny = x + ddx, y + ddy
                if 0 <= nx < w and 0 <= ny < h and not fig[ny, nx]:
                    sh_[ny, nx] = True
            shell |= sh_
        ys, xs = np.nonzero(shell)
        for y, x in zip(ys, xs):
            c = OUTLINE
            # figuur rechts of onder deze randpixel en niet links/boven -> lichtkant -> selout
            right = x + 1 < w and fig[y, x + 1]
            below = y + 1 < h and fig[y + 1, x]
            left = x - 1 >= 0 and fig[y, x - 1]
            above = y - 1 >= 0 and fig[y - 1, x]
            if (right or below) and not left and not above:
                ny_, nx_ = (y + 1, x) if below else (y, x + 1)
                o = self.objs[owner[ny_, nx_]]
                if o.part in self.selout_parts:
                    c = self.ramps[o.part][-1]
            idx[y, x] = c
        self.owner = owner
        return idx

    selout_parts = set()

    def render3(self):
        """Gen 3-schaduw (Teddiursa/Poochyena als voorbeeld): vaste schaduwvlakken langs
        onder/rechts (verschoven masker), een extra donkere binnenrand onderaan, slagschaduw
        onder voorliggende delen (kop op lijf, arm op buik), een strak hooglicht linksboven.
        Geen verlopen of dithering. Daarna dezelfde binnenlijnen, omlijning en selout als render()."""
        h, w = self.h, self.w
        owner = np.full((h, w), -1)
        for i, o in enumerate(self.objs):
            owner[o.mask] = i
        idx = np.zeros((h, w), np.uint8)

        def at(m, x, y):
            return 0 <= x < w and 0 <= y < h and m[y, x]

        for i, o in enumerate(self.objs):
            r = self.ramps[o.part]
            t = o.tone
            ys, xs = np.nonzero(owner == i)
            for y, x in zip(ys, xs):
                c = r[t]
                if not o.flat:
                    s = o.shade
                    dx, dy = int(round(s * 0.6)), int(round(s))
                    shadow = not at(o.mask, x + dx, y + dy) or not at(o.mask, x + dx + 1, y + dy // 2)
                    for ddx, ddy in ((0, -1), (0, -2), (-1, -1)):
                        nx, ny = x + ddx, y + ddy
                        if 0 <= nx < w and 0 <= ny < h and owner[ny, nx] > i and not self.objs[owner[ny, nx]].nocast:
                            shadow = True
                    deep = not at(o.mask, x, y + 1) and not at(o.mask, x + 1, y + 1)
                    if deep and len(r) > t + 2:
                        c = r[t + 2]
                    elif shadow:
                        c = r[min(t + 1, len(r) - 1)]
                    elif o.hl is not None and t > 0:
                        hx, hy, hr = o.hl
                        if (x + 0.5 - hx) ** 2 + (y + 0.5 - hy) ** 2 <= hr * hr:
                            c = r[t - 1]
                if o.paint is not None:
                    p = o.paint(x, y, c)
                    if p is not None:
                        c = p
                idx[y, x] = c
        return self._lines_and_outline(idx, owner)

    def _lines_and_outline(self, idx, owner):
        h, w = self.h, self.w
        fig = owner >= 0
        out = idx.copy()
        for i, o in enumerate(self.objs):
            if not o.line:
                continue
            ys, xs = np.nonzero(owner == i)
            for y, x in zip(ys, xs):
                for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + ddx, y + ddy
                    if 0 <= nx < w and 0 <= ny < h and 0 <= owner[ny, nx] < i and not o.mask[ny, nx]:
                        out[y, x] = OUTLINE if o.line == 'black' else self.ramps[o.part][-1]
                        break
        idx = out
        ys, xs = np.nonzero(fig)
        shell = np.zeros((h, w), bool)
        for y, x in zip(ys, xs):
            for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + ddx, y + ddy
                if 0 <= nx < w and 0 <= ny < h and not fig[ny, nx]:
                    shell[ny, nx] = True
        ys, xs = np.nonzero(shell)
        for y, x in zip(ys, xs):
            c = OUTLINE
            right = x + 1 < w and fig[y, x + 1]
            below = y + 1 < h and fig[y + 1, x]
            left = x - 1 >= 0 and fig[y, x - 1]
            above = y - 1 >= 0 and fig[y - 1, x]
            if (right or below) and not left and not above:
                ny_, nx_ = (y + 1, x) if below else (y, x + 1)
                o = self.objs[owner[ny_, nx_]]
                if o.part in self.selout_parts:
                    c = self.ramps[o.part][-1]
            idx[y, x] = c
        self.owner = owner
        return idx



def patch(idx, x0, y0, rows, key):
    """ASCII-patch: elk teken in `key` zet die index; '.' laat staan; ' ' = transparant (0)."""
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            if ch == '.':
                continue
            v = 0 if ch == ' ' else key[ch]
            y, x = y0 + dy, x0 + dx
            if 0 <= y < idx.shape[0] and 0 <= x < idx.shape[1]:
                idx[y, x] = v


def hooks(idx, claws, light=9, shade=11, keep=(), wide=2):
    """Haakklauwen per pixel tekenen (na render).
    claws: lijst pixelpaden [(x,y), ...] van basis naar punt. De eerste `wide` pixels
    krijgen rechts een schaduwpixel erbij (dikke basis). Daarna krijgt elke buurpixel
    die geen klauw is en niet in `keep` (bijv. de handschoenkleuren) de omlijning,
    zodat klauwen naast elkaar altijd door zwart gescheiden zijn."""
    pix = {}
    for path in claws:
        for k, (x, y) in enumerate(path):
            pix[(x, y)] = light
            if k < wide:
                pix[(x + 1, y)] = shade
        # onderste/rechter helft van de bocht iets donkerder: punt blijft licht
    for (x, y), v in pix.items():
        if 0 <= x < idx.shape[1] and 0 <= y < idx.shape[0]:
            idx[y, x] = v
    for (x, y) in list(pix):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) in pix or not (0 <= nx < idx.shape[1] and 0 <= ny < idx.shape[0]):
                continue
            if idx[ny, nx] in keep:
                continue
            idx[ny, nx] = OUTLINE
    return pix


def fix_outline(idx, selout=()):
    """Pixels die buiten de figuur uitsteken zonder rand krijgen er alsnog een (na patches).
    Een randpixel met een selout-kleur (`selout`, bijv. de donkerste vachttint) aan de
    boven- of linkerkant geldt al als omlijning en krijgt geen extra zwarte rand."""
    h, w = idx.shape
    fig = idx > 0
    out = idx.copy()
    for y in range(h):
        for x in range(w):
            if fig[y, x] and idx[y, x] != OUTLINE:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and not fig[ny, nx]:
                        if idx[y, x] in selout and (dx, dy) in ((-1, 0), (0, -1)):
                            continue
                        out[ny, nx] = OUTLINE
    return out


def save_indexed(path, frames, pal):
    """frames: lijst 64x64-indexarrays onder elkaar; pal: 16 (r,g,b); index 0 transparant."""
    a = np.concatenate(frames, axis=0).astype(np.uint8)
    im = Image.fromarray(a, 'P')
    flat = []
    for c in pal:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.info['transparency'] = 0
    im.save(path, transparency=0)


def save_pal(path, pal):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in pal:
            f.write('%d %d %d\n' % c)


def to_rgba(idx, pal, z=1, bg=None):
    h, w = idx.shape
    a = np.zeros((h, w, 4), np.uint8)
    for i, c in enumerate(pal):
        if i == 0:
            continue
        a[idx == i, :3] = c
        a[idx == i, 3] = 255
    im = Image.fromarray(a, 'RGBA')
    if bg is not None:
        b = Image.new('RGBA', im.size, bg)
        b.alpha_composite(im)
        im = b
    return im.resize((w * z, h * z), Image.NEAREST)
