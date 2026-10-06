"""Project Grounded: schets van een vuurtoren in Emerald-stijl (voor het vuurtoreneiland, Route 133/134).

Nog niet in de game: dit maakt alleen de art en previews voor Jordi.

- lighthouse.png       48x128 (3x8 metatiles), geindexeerd, 1 palet van 15 kleuren + transparant (index 0).
- lighthouse.pal/.pla  JASC-palet; .pla markeert de glaskleuren (11, 12) als licht: de DNS van expansion laat die
                       's nachts naar geel gloeien i.p.v. donker te kleuren (zie docs/tutorials/dns.md). De nachtversie
                       kost dus geen extra tiles of palet.
- lighthouse_beam.png  64x32 lichtbundel als los object (eigen OBJ-palet, alpha-blend zoals de lichtsprites).
- previews: *_4x.png, lighthouse_night_4x.png (gesimuleerde nacht-DNS), compare_day.png / compare_night.png
  (naast een stuk Lilycove: gebouwen en kust).

Stijl overgenomen van de Lilycove/Slateport-gebouwen: navy omlijning (65,74,106), licht van linksboven
(highlight links van het midden, schaduw rechts), witte muren in de lavendelgrijze Hoenn-tinten, rood als de PC.

Gebruik: python3 tools/grounded/lighthouse_art.py [lilycove_render.png]
(zonder argument rendert hij Lilycove zelf met maptools/render_map.py; daarvoor moeten de tiles.4bpp gebouwd zijn).
"""
import os, subprocess, sys, tempfile
from PIL import Image

OUT = 'graphics/grounded/lighthouse'
W, H = 48, 128

PAL = [(115, 197, 164),                                   # 0 transparant
       (65, 74, 106),                                     # 1 omlijning (navy)
       (98, 98, 123), (131, 131, 139),                    # 2-3 grijs (schaduw, metaal)
       (156, 180, 222), (189, 205, 230), (222, 230, 238), (255, 255, 255),  # 4-7 wit (schaduw..licht)
       (148, 41, 57), (205, 65, 82), (238, 123, 106),     # 8-10 rood
       (90, 131, 197), (238, 226, 164),                   # 11 glas, 12 lens  (licht 's nachts)
       (98, 65, 82), (156, 115, 115), (222, 180, 164)]    # 13-15 rots
LIT = [11, 12]
O, G2, G3, W4, W5, W6, W7, R8, R9, R10, GL, LE, K13, K14, K15 = range(1, 16)

BEAM_PAL = [(0, 0, 0), (255, 250, 214), (248, 230, 140), (232, 200, 96)]

CX = 23.5   # midden van de toren (kolom 23|24)


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.p = [[0] * w for _ in range(h)]

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.p[y][x] = c

    def get(self, x, y):
        return self.p[y][x] if 0 <= x < self.w and 0 <= y < self.h else 0

    def outline(self, c=O, only_empty=True):
        """Omlijning rond alles wat niet transparant is (alleen op lege pixels)."""
        add = []
        for y in range(self.h):
            for x in range(self.w):
                if self.p[y][x] == 0:
                    if any(self.get(x + dx, y + dy) not in (0, c) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                        add.append((x, y))
        for x, y in add:
            self.p[y][x] = c

    def image(self, pal):
        im = Image.new('P', (self.w, self.h))
        flat = []
        for c in pal:
            flat += list(c)
        im.putpalette(flat + [0] * (768 - len(flat)))
        im.putdata([c for row in self.p for c in row])
        return im


def shade(u, ramp):
    """Cilinder: u = -1 (links) .. 1 (rechts); licht van linksboven."""
    for limit, c in ramp:
        if u < limit:
            return c
    return ramp[-1][1]


WHITE = [(-0.62, W6), (-0.08, W7), (0.38, W6), (0.68, W5), (9, W4)]
RED = [(-0.62, R9), (-0.1, R10), (0.42, R9), (9, R8)]
ROCK = [(-0.3, K15), (0.35, K14), (9, K13)]


def cylinder(cv, y0, y1, hw0, hw1, ramp_at, edge=O):
    """Afgeknotte cilinder van y0 tot y1 met halve breedte hw0 -> hw1; ramp_at(x, y, u) geeft de kleur."""
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        hw = hw0 + (hw1 - hw0) * t
        xl, xr = int(round(CX - hw + 0.5)), int(round(CX + hw - 0.5))
        for x in range(xl, xr + 1):
            u = (x - CX) / hw
            cv.set(x, y, edge if x in (xl, xr) else ramp_at(x, y, u))


def tower(cv):
    # stroken: grens buigt omlaag naar het midden (we kijken er schuin van boven op)
    bands = [44, 56, 68, 80, 92]                # rood vanaf 44, wit vanaf 56, ...; vanaf 104 de stenen voet

    def body(x, y, u):
        sag = round(2.2 * (1 - u * u))
        if y >= 104 + sag:                      # stenen voet met voegen
            c = shade(u, WHITE)
            row = (y - 104 - sag) // 5
            if (y - 104 - sag) % 5 == 4 or (y >= 104 + sag and (x + 4 * (row % 2)) % 8 == 0):
                c = W4 if u < 0.68 else G3
            if y == 104 + sag:
                c = G2
            return c
        k = sum(1 for b in bands if y >= b + sag)
        if k == 0:
            return R9
        if y == bands[k - 1] + sag and k > 1:
            return W4 if k % 2 == 1 else R8      # dunne schaduwlijn onder elke rand
        return shade(u, RED if k % 2 == 1 else WHITE)
    cylinder(cv, 42, 125, 13.0, 18.5, body)

    # raampjes in de witte stroken (licht 's nachts)
    for wy in (59, 83):
        for y in range(wy, wy + 9):
            for x in range(21, 27):
                edge = x in (21, 26) or y in (wy, wy + 8)
                cv.set(x, y, O if edge else (LE if (y > wy + 3 and x < 24) else GL))
        cv.set(22, wy + 1, W6)
        for x in range(21, 27):                     # vensterbank
            cv.set(x, wy + 9, G3)

    # deur: middelste tile van de onderste rij (x 16-31, y 112-127)
    for y in range(109, 126):
        for x in range(17, 31):
            if y == 109 or x in (17, 30):
                c = O
            elif y == 110:
                c = G3                               # latei
            elif x in (18, 29):
                c = G2 if x == 29 else G3            # kozijn
            elif x == 24:
                c = O                                # dubbele deur
            elif y in (113, 120) and x not in (19, 28):
                c = R8                               # panelen
            else:
                c = R10 if x < 22 else (R9 if x < 27 else R8)
            cv.set(x, y, c)
    cv.set(23, 117, W7); cv.set(25, 117, W7)        # klinken
    for x in range(16, 32):                          # stoep
        cv.set(x, 125, G3 if 16 < x < 31 else O)
        cv.set(x, 126, G2 if 16 < x < 31 else O)
        cv.set(x, 127, O)


def gallery(cv):
    # ijzeren consoles onder de galerij
    cylinder(cv, 38, 44, 18.0, 13.5, lambda x, y, u: O if (x % 4 == 1) else (G3 if u < 0.2 else G2))
    # vloer (ellips van boven) + voorkant
    for y in range(30, 42):
        for x in range(0, W):
            dx, dy = (x - CX) / 22.5, (y - 35.5) / 3.6
            if dx * dx + dy * dy <= 1:
                cv.set(x, y, W5 if dx < 0.3 else W4)
    for x in range(0, W):
        dx = (x - CX) / 22.5
        if abs(dx) <= 1:
            yb = int(35.5 + 3.6 * (1 - dx * dx) ** 0.5)
            cv.set(x, yb, G3)
            cv.set(x, yb + 1, G2)
            cv.set(x, yb + 2, O)


def lantern(cv):
    # voet van het lantaarnhuis
    cylinder(cv, 28, 34, 11.0, 11.5, lambda x, y, u: shade(u, WHITE) if y > 28 else G3)

    # glas met stijlen en een ovale lens (Fresnel-ringen)
    def glass(x, y, u):
        if y == 27:
            return G2
        if x in (15, 32):
            return O
        lx, ly = (x - CX) / 4.6, (y - 21.5) / 5.2
        if lx * lx + ly * ly <= 1:
            return GL if (y - 17) % 3 == 0 and abs(lx) < 0.8 else LE
        if x in (19, 28):
            return O
        return GL
    cylinder(cv, 16, 28, 10.0, 10.0, glass)
    for y in range(17, 22):                          # glinstering op het linkerglas
        cv.set(16 + (y - 17) // 2, y, W6)
    # dakrand
    cylinder(cv, 13, 16, 12.5, 12.5, lambda x, y, u: R8 if y == 15 else shade(u, RED))
    # koepel met ribben (zoals het PC-dak)
    for y in range(3, 13):
        t = (y - 3) / 9.0
        hw = 2.5 + 9.5 * t ** 0.7
        xl, xr = int(round(CX - hw + 0.5)), int(round(CX + hw - 0.5))
        for x in range(xl, xr + 1):
            u = (x - CX) / max(hw, 1)
            c = shade(u, RED)
            if any(abs(u - r) < 0.09 for r in (-0.5, 0.15, 0.62)) and y > 4:
                c = R8 if u > -0.2 else R9
            cv.set(x, y, c)
    # ventilatiebol + piek
    for y in range(0, 4):
        for x in range(22, 26):
            if y == 0 and x in (22, 25):
                continue
            cv.set(x, y, G3 if x < 24 else G2)
    cv.set(23, 1, W6)


def railing(cv):
    """Reling langs de voorrand van de galerij (staat over de voet van het lantaarnhuis)."""
    for x in range(1, W - 1):
        dx = (x - CX) / 22.0
        if abs(dx) > 1:
            continue
        yb = int(35.0 + 3.4 * (1 - dx * dx) ** 0.5)
        top = yb - 6
        cv.set(x, top, O)
        cv.set(x, top + 1, G3 if dx < 0.4 else G2)
        if x % 4 == 1 or x in (1, W - 2):
            for y in range(top + 2, yb):
                cv.set(x, y, O)
        else:
            cv.set(x, top + 3, G2 if dx < 0.4 else O)  # tussenregel


def rocks(cv):
    """Rotsvoet links en rechts van de deur: losse Hoenn-rotsblokken (licht van linksboven, donkerrode rand,
    een schuine ribbel zoals de rotsen in Lilycove). Achter naar voor getekend, zodat de randen ze scheiden."""
    lumps = ((4, 110, 6, 6), (42, 109, 6, 6), (11, 117, 6, 5), (37, 117, 6, 5),
             (3, 122, 5, 5), (45, 122, 4, 5), (14, 124, 3, 3), (34, 124, 3, 3))
    for bx, by, rx, ry in lumps:
        for y in range(by - ry - 1, min(H, by + ry + 2)):
            for x in range(bx - rx - 1, bx + rx + 2):
                if not 0 <= x < W or (15 < x < 32 and y > 108):
                    continue
                dx, dy = (x - bx) / rx, (y - by) / ry
                d = dx * dx + dy * dy
                if d > 1.25:
                    continue
                if d > 1.0:
                    c = K13                                  # rand
                else:
                    lit = -(dx * 0.75 + dy * 0.65)          # licht van linksboven
                    c = K15 if lit > 0.45 else (K14 if lit > -0.35 else K13)
                    if c != K13 and abs((x - bx) + (y - by) * 1.2 + 1) < 0.6 and d < 0.7:
                        c = K13                              # ribbel
                cv.set(x, y, c)


def build():
    cv = Canvas(W, H)
    tower(cv)
    gallery(cv)
    lantern(cv)
    railing(cv)
    rocks(cv)
    cv.outline(O)
    # rotsen omlijnen met donkerrood i.p.v. navy (zoals de Hoenn-rotsen)
    for y in range(96, H):
        for x in range(W):
            if cv.p[y][x] == O and any(cv.get(x + dx, y + dy) in (K14, K15) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) \
                    and not any(cv.get(x + dx, y + dy) in (W4, W5, W6, W7, R8, R9, R10) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                cv.p[y][x] = K13
    return cv


def beam():
    """Lichtbundel 64x32, wijst naar rechts (links = OAM-hflip). Smal bij de lamp, breder en vager naar buiten."""
    cv = Canvas(64, 32)
    for x in range(64):
        half = 2 + x * 0.22
        for y in range(32):
            d = abs(y - 15.5) / half
            if d > 1:
                continue
            fade = x / 63.0
            c = 1 if d < 0.35 and fade < 0.5 else (2 if d < 0.7 and fade < 0.8 else 3)
            bayer = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))[y % 4][x % 4]
            if bayer < (fade - 0.45) * 30 + max(0.0, d - 0.6) * 25:
                continue                                 # zachte rand en uitlopend eind via Bayer-dither
            cv.set(x, y, c)
    return cv


def write_pal(path, pal):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in pal + [(0, 0, 0)] * (16 - len(pal)):
            f.write('%d %d %d\n' % c)


def tile_count(cv):
    """Unieke 8x8-tiles (met h/v-flip ontdubbeld, lege tile niet meegeteld) en niet-lege metatiles."""
    seen, mts = set(), 0
    for ty in range(cv.h // 8):
        for tx in range(cv.w // 8):
            t = tuple(tuple(cv.p[ty * 8 + j][tx * 8:tx * 8 + 8]) for j in range(8))
            if not any(any(r) for r in t):
                continue
            hf = tuple(tuple(reversed(r)) for r in t)
            forms = {t, hf, tuple(reversed(t)), tuple(reversed(hf))}
            if not forms & seen:
                seen.add(t)
    for my in range(cv.h // 16):
        for mx in range(cv.w // 16):
            if any(cv.p[my * 16 + j][mx * 16 + i] for j in range(16) for i in range(16)):
                mts += 1
    return len(seen), mts


def night_rgb(c, lit):
    """Benadering van de expansion-DNS 's nachts: tint (0.456, 0.456, 0.615); lichtkleuren 20/32 naar geel."""
    if lit:
        y = (248, 224, 120)
        return tuple(int(a + (b - a) * 20 / 32) for a, b in zip(c, y))
    return (int(c[0] * 0.456), int(c[1] * 0.456), int(c[2] * 0.615))


def to_rgba(cv, pal, night=False):
    im = Image.new('RGBA', (cv.w, cv.h), (0, 0, 0, 0))
    px = im.load()
    for y in range(cv.h):
        for x in range(cv.w):
            i = cv.p[y][x]
            if i:
                c = pal[i]
                if night:
                    c = night_rgb(c, i in LIT)
                px[x, y] = c + (255,)
    return im


def add_glow(base, cx, cy, r, strength=0.55):
    """Lichtbol (zoals LIGHT_TYPE_BALL, alpha-blend) over de lamp."""
    px = base.load()
    for y in range(max(0, cy - r), min(base.size[1], cy + r)):
        for x in range(max(0, cx - r), min(base.size[0], cx + r)):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / r
            if d < 1:
                a = strength * (1 - d) ** 1.5
                p = px[x, y]
                px[x, y] = tuple(int(p[k] + (BEAM_PAL[2][k] - p[k]) * a) for k in range(3)) + p[3:]


def add_beam(base, bm, x0, y0, flip=False, alpha=0.6):
    img = bm.image(BEAM_PAL)
    if flip:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    src = img.load()
    px = base.load()
    for y in range(bm.h):
        for x in range(bm.w):
            i = src[x, y]
            X, Y = x0 + x, y0 + y
            if i and 0 <= X < base.size[0] and 0 <= Y < base.size[1]:
                p = px[X, Y]
                c = BEAM_PAL[i]
                px[X, Y] = tuple(min(255, int(p[k] + c[k] * alpha)) for k in range(3)) + p[3:]


def main():
    os.makedirs(OUT, exist_ok=True)
    cv = build()
    cv.image(PAL).save(f'{OUT}/lighthouse.png', transparency=0)
    write_pal(f'{OUT}/lighthouse.pal', PAL)
    with open(f'{OUT}/lighthouse.pla', 'w') as f:
        f.write('# glas en lens gloeien s nachts\n' + '\n'.join(str(i) for i in LIT) + '\n')
    bm = beam()
    bm.image(BEAM_PAL).save(f'{OUT}/lighthouse_beam.png', transparency=0)

    bg = (115, 197, 164, 255)
    day = Image.new('RGBA', (W, H), bg); day.alpha_composite(to_rgba(cv, PAL))
    day.resize((W * 4, H * 4), Image.NEAREST).save(f'{OUT}/lighthouse_4x.png')
    # nacht: tegen een donker getinte zee, met lichtbol en bundels
    nbg = night_rgb((106, 131, 213), False) + (255,)
    nw = 48 + 2 * 64
    night = Image.new('RGBA', (nw, H), nbg)
    night.alpha_composite(to_rgba(cv, PAL, night=True), (64, 0))
    add_glow(night, 64 + 24, 22, 20)
    add_beam(night, bm, 64 + 34, 6)
    add_beam(night, bm, 64 + 14 - 64, 6, flip=True, alpha=0.35)
    night.resize((nw * 4, H * 4), Image.NEAREST).save(f'{OUT}/lighthouse_night_4x.png')
    night.save(f'{OUT}/lighthouse_night.png')

    # vergelijking naast Lilycove (Contest Hall, huizen, strand)
    if len(sys.argv) > 1:
        lily = sys.argv[1]
    else:
        lily = os.path.join(tempfile.mkdtemp(), 'lily.png')
        subprocess.run([sys.executable, 'tools/grounded/maptools/render_map.py', 'LilycoveCity', lily, '0', '40'],
                       check=True)
    city = Image.open(lily).convert('RGBA').crop((30 * 16, 10 * 16, 62 * 16, 40 * 16))
    # vuurtoren op het strand/de ondiepte ten oosten van de Contest Hall
    pos = ((56 - 30) * 16, (30 - 10 - 7) * 16)   # deur op kaarttegel (57, 30), op het strand
    cday = city.copy(); cday.alpha_composite(to_rgba(cv, PAL), pos)
    cday.resize((cday.size[0] * 2, cday.size[1] * 2), Image.NEAREST).save(f'{OUT}/compare_day.png')
    cpx = city.load()
    cn = Image.new('RGBA', city.size)
    npx = cn.load()
    for y in range(city.size[1]):
        for x in range(city.size[0]):
            npx[x, y] = night_rgb(cpx[x, y][:3], False) + (255,)
    cn.alpha_composite(to_rgba(cv, PAL, night=True), pos)
    add_glow(cn, pos[0] + 24, pos[1] + 22, 20)
    add_beam(cn, bm, pos[0] + 34, pos[1] + 6)
    add_beam(cn, bm, pos[0] + 14 - 64, pos[1] + 6, flip=True, alpha=0.35)
    cn.resize((cn.size[0] * 2, cn.size[1] * 2), Image.NEAREST).save(f'{OUT}/compare_night.png')

    n8, nm = tile_count(cv)
    nb, _ = tile_count(bm)
    print(f'vuurtoren: {nm} metatiles, {n8} unieke 8x8-tiles (flips ontdubbeld); bundel: {nb} OBJ-tiles (64x32 = 32)')


if __name__ == '__main__':
    main()
