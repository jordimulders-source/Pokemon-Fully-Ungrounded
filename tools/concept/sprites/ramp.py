"""Palet-/rampgenerator in Hoenn-stijl (gekalibreerd op de 202 GBA-sprites).

  python3 tools/concept/sprites/ramp.py uit_basis [--ramp naam=#rrggbb:n ...] [--white] [--hue K]
     -> uit_basis.pal (JASC, 16 kleuren) + uit_basis.png (stalen, 16x vergroot, met indexnummers)

Elke --ramp maakt n tinten (3-5; standaard 4) rond de opgegeven basiskleur
(= de middentint die het meest voorkomt). Volgorde in het palet zoals in de
GBA-sprites: per ramp van licht naar donker, index 15 = omlijning #101010,
index 0 = transparant (vaste opvulkleur). --white voegt een los wit
(oog-hooglicht) toe. --hue K = tintverschuiving per stap (standaard 4 graden:
lichter -> richting geel, donkerder -> weg van geel). Alle kleuren worden naar
GBA-15-bit afgerond (zoals gbagfx).

Gemeten in Hoenn (ramps van 4): V = .48/.71/.87/1.00, S = .58/.60/.54/.39;
de lichtste tint heeft bijna altijd V = 1 (97% van de sprites heeft er een).
"""
import sys, os, colorsys
from PIL import Image, ImageDraw

PROFILE = {  # (V, S-factor t.o.v. middentint) van donker naar licht
    2: ([0.80, 1.00], [1.00, 0.70]),     # klein accent (klauw, neus): basis + hooglicht
    3: ([0.55, 0.84, 1.00], [0.94, 1.00, 0.80]),
    4: ([0.48, 0.71, 0.87, 1.00], [0.97, 1.00, 0.90, 0.65]),
    5: ([0.45, 0.67, 0.84, 0.93, 1.00], [0.81, 1.00, 0.87, 0.78, 0.54]),
}
TRANSPARENT = (152, 208, 160)
OUTLINE = (16, 16, 16)


def gba(c):
    """Rond af naar 15-bit GBA-kleur en terug (zoals de JASC-bestanden in de repo)."""
    return tuple(int(round(v / 255 * 31)) * 255 // 31 for v in c)


def shift_hue(h, deg):
    """Verschuif tint h (0-360) 'deg' graden richting geel (60); negatief = weg van geel."""
    d = (60 - h + 540) % 360 - 180          # kortste weg naar geel
    if abs(d) < 1e-6:
        return h if deg >= 0 else (h - deg) % 360
    step = min(abs(deg), abs(d)) if deg > 0 else abs(deg)
    return (h + step * (1 if d > 0 else -1) * (1 if deg > 0 else -1)) % 360


def ramp(base, n=4, hue=4.0):
    """Ramp van n tinten; 'base' = de meest gebruikte tint = de op een na lichtste
    (zo is het in de Hoenn-sprites: Treecko 9cd54a, Mudkip 5aace6)."""
    if n == 1:                                   # los accent (bijv. iris): alleen de basis
        return [gba(base)]
    r, g, b = [v / 255 for v in base]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h *= 360
    V, SF = PROFILE[n]
    bp = n - 2                                  # positie van de basis (donker -> licht)
    out = []
    for i in range(n):
        if i == bp:
            vi, si, hi = v, s, h
        else:
            vi = max(0.12, min(1.0, v + (V[i] - V[bp])))
            if i == n - 1:                       # hooglicht: in Hoenn bijna altijd V = 1
                vi = 1.0 if v >= 0.70 else min(1.0, v + 0.18)
            si = max(0.0, min(1.0, s * SF[i] / SF[bp]))
            hi = shift_hue(h, hue * (i - bp))
        c = colorsys.hsv_to_rgb(hi / 360, si, vi)
        out.append(gba(tuple(int(round(x * 255)) for x in c)))
    return out[::-1]  # licht -> donker


def write_pal(path, cols):
    cols = (cols + [(0, 0, 0)] * 16)[:16]
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in cols:
            f.write('%d %d %d\n' % c)


def main():
    a = sys.argv[1:]
    out = a.pop(0)
    hue = 4.0; ramps = []; white = False
    while a:
        k = a.pop(0)
        if k == '--ramp':
            name, spec = a.pop(0).split('=')
            col, _, n = spec.partition(':')
            col = col.lstrip('#')
            ramps.append((name, tuple(int(col[i:i + 2], 16) for i in (0, 2, 4)), int(n or 4)))
        elif k == '--hue':
            hue = float(a.pop(0))
        elif k == '--white':
            white = True
    cols = [TRANSPARENT]; names = ['transparant']
    for name, base, n in ramps:
        for i, c in enumerate(ramp(base, n, hue)):
            cols.append(c); names.append('%s%d' % (name, i + 1))
    if white:
        cols.append((255, 255, 255)); names.append('wit')
    if len(cols) > 15:
        sys.exit('te veel kleuren: %d (max 14 + omlijning)' % (len(cols) - 1))
    while len(cols) < 15:
        cols.append((0, 0, 0)); names.append('-')
    cols.append(OUTLINE); names.append('omlijning')
    write_pal(out + '.pal', cols)
    z = 40
    img = Image.new('RGB', (16 * z, z + 30), 'white'); d = ImageDraw.Draw(img)
    for i, c in enumerate(cols):
        d.rectangle([i * z, 0, i * z + z - 1, z - 1], fill=c)
        d.text((i * z + 2, z + 2), str(i), fill='black')
        d.text((i * z + 2, z + 14), names[i][:6], fill='black')
    img.save(out + '.png')
    for i, (c, n) in enumerate(zip(cols, names)):
        print('%2d %-12s #%02x%02x%02x' % (i, n, *c))


if __name__ == '__main__':
    main()
