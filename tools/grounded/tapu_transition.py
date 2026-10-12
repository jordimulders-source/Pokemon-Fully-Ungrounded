"""Project Grounded: genereert de gevechtsintro's van de vier Tapu's (B_TRANSITION_TAPU_KOKO/LELE/BULU/FINI).
Lichte intro's (zoals de Regi's en het weertrio, geen film): het gesloten schild van de Tapu (uit Jordi's
png's in graphics/, van origin/master) staat midden op een donkere achtergrond in de kleur van de Tapu,
met een achtergrondmotief uit het schildpatroon dat via paletcycli beweegt. Op de grote drumslag gaat
het schild open (twee helften uit elkaar), licht, flits, gevecht. De animatie zelf staat in
src/battle_transition.c (zoek op TAPU_HIT_FRAME).

Per Tapu:
  graphics/battle_transitions/tapu_<naam>.png    tiles (palet 15 = schild, 14 = motief; tile 0 leeg)
  graphics/battle_transitions/tapu_<naam>.pal    schildpalet (index 11-13 = patroon dat oplicht, 15 = licht)
  graphics/battle_transitions/tapu_<naam>.bin    beginbeeld 32x20 (motief + schild)
  graphics/battle_transitions/tapu_<naam>_shell.bin  lichttile + alleen het schild (w x h), voor het openen
Het schild wordt symmetrisch gemaakt (linkerhelft gespiegeld), zodat de rechterhelft uit gespiegelde tiles
bestaat. Gebruik: python3 tools/grounded/tapu_transition.py <bronmap met koko.png lele.png bulu.png fini.png>
[voorbeeldmap]"""
import math, os, struct, sys
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
OUT = os.path.join(ROOT, 'graphics', 'battle_transitions')

# schildgrootte in tiles (breedte even, het midden ligt op x = 120)
# palet: index 1 omlijning, 2-10 lijf, 11-13 patroon (licht op op de beat), 14 reserve, 15 licht
TAPUS = {
    'koko': dict(src='koko.png', w=12, h=18, pal=[
        (40, 34, 30),                                   # 1 omlijning
        (150, 142, 58), (205, 198, 88), (228, 224, 140), # 2-4 geel lijf
        (110, 85, 83), (70, 58, 56),                     # 5-6 patroonlijn bruin
        (66, 63, 57), (130, 126, 118),                   # 7-8 snavel
        (160, 78, 52), (120, 60, 48),                    # 9-10 veren donker
        (244, 240, 210), (226, 130, 70), (250, 180, 90), # 11-13 wit, oranje, licht oranje
        (0, 0, 0), (255, 255, 200)]),
    'lele': dict(src='lele.png', w=12, h=18, pal=[
        (48, 40, 44),
        (242, 192, 216), (214, 158, 184), (176, 120, 140),
        (102, 97, 91), (72, 69, 68),
        (52, 48, 52), (120, 112, 118),
        (160, 82, 98), (196, 140, 160),
        (244, 240, 242), (228, 112, 136), (248, 160, 184),
        (0, 0, 0), (255, 230, 248)]),
    'bulu': dict(src='bulu.png', w=18, h=16, pal=[
        (22, 16, 16),
        (242, 52, 55), (150, 40, 36), (255, 120, 104),
        (37, 34, 30), (90, 84, 76),
        (149, 122, 58), (110, 92, 50),
        (200, 60, 48), (60, 50, 44),
        (244, 242, 228), (210, 196, 30), (232, 226, 136),
        (0, 0, 0), (240, 255, 200)]),
    'fini': dict(src='fini.png', w=14, h=17, pal=[
        (32, 28, 44),
        (152, 127, 192), (112, 94, 152), (182, 162, 218),
        (107, 98, 109), (76, 72, 86),
        (88, 80, 118), (60, 54, 80),
        (140, 150, 178), (160, 140, 200),
        (238, 238, 244), (192, 200, 216), (214, 226, 246),
        (0, 0, 0), (220, 240, 255)]),
}

LIGHT = 15


def load_shell(path, wt, ht):
    im = Image.open(path).convert('RGBA')
    im = im.crop(im.split()[3].getbbox())
    # passend in wt x ht tiles (met 1 px rand), verhouding behouden
    W, H = wt * 8 - 2, ht * 8 - 2
    s = min(W / im.width, H / im.height)
    nw, nh = max(2, int(round(im.width * s))), max(2, int(round(im.height * s)))
    small = im.convert('RGBa').resize((nw, nh), Image.LANCZOS).convert('RGBA')
    canvas = Image.new('RGBA', (wt * 8, ht * 8), (0, 0, 0, 0))
    canvas.paste(small, ((wt * 8 - nw) // 2, (ht * 8 - nh) // 2))
    return canvas


def nearest(c, pal):
    best, bi = None, 1
    for i, p in enumerate(pal):
        if i == 0 or i in (14, LIGHT):
            continue
        d = 2 * (c[0] - p[0]) ** 2 + 4 * (c[1] - p[1]) ** 2 + 3 * (c[2] - p[2]) ** 2
        if best is None or d < best:
            best, bi = d, i
    return bi


def quantize(canvas, pal):
    w, h = canvas.size
    px = canvas.load()
    img = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w // 2):  # linkerhelft, daarna spiegelen
            r, g, b, a = px[x, y]
            if a >= 110:
                img[y][x] = nearest((r, g, b), pal)
    for y in range(h):
        for x in range(w // 2):
            img[y][w - 1 - x] = img[y][x]
    # omlijning: elke dekkende pixel naast transparant
    out = [row[:] for row in img]
    for y in range(h):
        for x in range(w):
            if img[y][x]:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if not (0 <= xx < w and 0 <= yy < h) or img[yy][xx] == 0:
                        out[y][x] = 1
                        break
    return out


# ---- achtergrondmotieven: geven per pixel een fase 1..8 (paletcyclus) of 0 (leeg)
def motif_koko(x, y):
    # kolommen met een ruitenketting (het middenpatroon van het schild); de energie stroomt omlaag
    for cx in (22, 58, 182, 218):
        dx = abs(x + 0.5 - cx)
        yy = y % 32
        dy = abs(yy + 0.5 - 16)
        d = dx / 10 + dy / 16
        if 0.72 <= d <= 1.0:
            return 1 + (y // 4) % 8
    return 0


def motif_lele(x, y):
    # ruitvormige ringen (het X-/ruitpatroon) die vanuit het midden uitdijen
    d = abs(x + 0.5 - 120) + abs(y + 0.5 - 80) * 1.25
    if d % 18 < 4:
        return 1 + int(d // 18) % 8
    return 0


def motif_bulu(x, y):
    # zaagtandbanden (de driehoeken op het schild) die omhoog groeien
    tri = abs((x % 16) - 7.5)
    yy = y + tri * 0.9
    if yy % 20 < 5:
        return 1 + int(yy // 20) % 8
    return 0


def motif_fini(x, y):
    # golven met de zigzag van de schildrand; ze rollen naar beneden
    tri = abs((x % 32) - 15.5) / 15.5  # 0..1, periode 32 (tiles herhalen per 64 px)
    yy = y + 6 * tri + 3 * math.sin(x * math.pi / 32)
    if yy % 16 < 3:
        return 1 + int(yy // 16) % 8
    return 0


MOTIFS = dict(koko=motif_koko, lele=motif_lele, bulu=motif_bulu, fini=motif_fini)


def build(name, srcdir, preview=None):
    cfg = TAPUS[name]
    wt, ht = cfg['w'], cfg['h']
    pal = [(0, 0, 0)] + cfg['pal']
    assert len(pal) == 16
    shell = quantize(load_shell(os.path.join(srcdir, cfg['src']), wt, ht), pal)
    x0, y0 = 15 - wt // 2, (20 - ht) // 2
    motif0 = MOTIFS[name]
    # halo: geen motief binnen HALO px van het schild, zodat motief en schild nooit in dezelfde tile vallen
    # (een tile heeft maar een palet) en de donkere rand de vorm van het schild volgt
    HALO = 9
    near = set()
    for sy in range(ht * 8):
        for sx in range(wt * 8):
            if shell[sy][sx]:
                X, Y = x0 * 8 + sx, y0 * 8 + sy
                for dy in range(-HALO, HALO + 1):
                    for dx in range(-HALO, HALO + 1):
                        if dx * dx + dy * dy <= HALO * HALO:
                            near.add((X + dx, Y + dy))

    def motif(x, y):
        return 0 if (x, y) in near else motif0(x, y)

    tiles, index = [], {}

    def add(t):
        variants = [(t, 0)]
        tf = tuple(t[py * 8 + 7 - px] for py in range(8) for px in range(8))
        tv = tuple(t[(7 - py) * 8 + px] for py in range(8) for px in range(8))
        tb = tuple(t[(7 - py) * 8 + 7 - px] for py in range(8) for px in range(8))
        variants += [(tf, 1), (tv, 2), (tb, 3)]
        for v, fl in variants:
            if v in index:
                return index[v] | (fl << 10)
        index[t] = len(tiles)
        tiles.append(t)
        return index[t]

    add(tuple([0] * 64))
    full = [0] * (32 * 20)
    shellmap = [0] * (wt * ht)
    for ty in range(20):
        for tx in range(30):
            sx, sy = tx - x0, ty - y0
            t = None
            if 0 <= sx < wt and 0 <= sy < ht:
                t = tuple(shell[sy * 8 + py][sx * 8 + px] for py in range(8) for px in range(8))
                if any(t):
                    e = add(t) | (15 << 12)
                    shellmap[sy * wt + sx] = e
                    full[ty * 32 + tx] = e
                else:
                    t = None
            if t is None:
                t = tuple(motif(tx * 8 + px, ty * 8 + py) for py in range(8) for px in range(8))
                full[ty * 32 + tx] = add(t) | (14 << 12) if any(t) else 0
    # volle lichttile (palet 15, index 15) voor de spleet als het schild opengaat
    light = add(tuple([LIGHT] * 64))
    assert light < 1024
    print('%s: %d tiles, lichttile %d' % (name, len(tiles), light))

    rows = (len(tiles) + 15) // 16
    out = Image.new('P', (128, rows * 8))
    for n, t in enumerate(tiles):
        for p, v in enumerate(t):
            out.putpixel(((n % 16) * 8 + p % 8, (n // 16) * 8 + p // 8), v)
    out.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    base = os.path.join(OUT, 'tapu_' + name)
    out.save(base + '.png')
    open(base + '.bin', 'wb').write(struct.pack('<%dH' % len(full), *full))
    # eerste u16 = de lichttile (met palet 15), daarna het schild
    shellbin = [light | (15 << 12)] + shellmap
    open(base + '_shell.bin', 'wb').write(struct.pack('<%dH' % len(shellbin), *shellbin))
    with open(base + '.pal', 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n16\n')
        for c in pal:
            fp.write('%d %d %d\n' % c)
    if preview:
        bgc = dict(koko=(255, 230, 60), lele=(255, 120, 190), bulu=(170, 230, 60), fini=(150, 170, 255))[name]
        p = Image.new('RGB', (240, 160), (20, 20, 20))
        for y in range(160):
            for x in range(240):
                sx, sy = x - x0 * 8, y - y0 * 8
                v = shell[sy][sx] if 0 <= sx < wt * 8 and 0 <= sy < ht * 8 else 0
                if v:
                    p.putpixel((x, y), pal[v])
                else:
                    m = motif(x, y)
                    if m:
                        k = 0.25 + 0.75 * (m == 1)
                        p.putpixel((x, y), tuple(int(c * k) for c in bgc))
        p.resize((720, 480), Image.NEAREST).save(os.path.join(preview, 'preview_%s.png' % name))
    return shell


if __name__ == '__main__':
    srcdir = sys.argv[1]
    preview = sys.argv[2] if len(sys.argv) > 2 else None
    for n in ('koko', 'lele', 'bulu', 'fini'):
        build(n, srcdir, preview)
