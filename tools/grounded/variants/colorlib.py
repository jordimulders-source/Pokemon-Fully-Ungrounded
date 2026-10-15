"""Kleurhulp voor de varianten: OKLab/OKLCh en het herkleuren van een kleurgroep
met behoud van de schaduwopbouw (lichtheidsverschillen, verzadiging, tintverloop)."""
import math


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gam(c):
    c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    return c * 255


def to_oklch(rgb):
    r, g, b = (_lin(v) for v in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(A, B), math.degrees(math.atan2(B, A)) % 360


def _from_oklch(L, C, h):
    A, B = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l = (L + 0.3963377774 * A + 0.2158037573 * B) ** 3
    m = (L - 0.1055613458 * A - 0.0638541728 * B) ** 3
    s = (L - 0.0894841775 * A - 1.2914855480 * B) ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return r, g, b


def from_oklch(L, C, h):
    """Terug naar sRGB; buiten het gamut eerst de verzadiging verlagen."""
    L = max(0.0, min(1.0, L))
    for _ in range(40):
        rgb = _from_oklch(L, C, h)
        if all(-1e-4 <= v <= 1.0001 for v in rgb):
            break
        C *= 0.9
    return tuple(int(round(max(0, min(255, _gam(max(0.0, min(1.0, v))))))) for v in rgb)


def hexrgb(s):
    s = s.lstrip('#')
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def gba(c):
    return tuple((v >> 3) << 3 for v in c)


def recolor(colors, idxs, base, target, lscale=1.0, cscale=None, hshift=1.0):
    """Herkleur de indexen `idxs` zodat `base` de doelkleur krijgt en de andere
    indexen hun verschil t.o.v. base (lichtheid, verzadiging, tint) houden."""
    tL, tC, th = to_oklch(hexrgb(target) if isinstance(target, str) else target)
    bL, bC, bh = to_oklch(colors[base])
    # Lichtheid: verschil t.o.v. base behouden; loopt de groep boven wit of onder
    # zwart uit, dan die kant samendrukken i.p.v. afkappen (anders vallen tinten weg).
    dL = {i: (to_oklch(colors[i])[0] - bL) * lscale for i in idxs}
    hi, lo = max(dL.values()), min(dL.values())
    up = (0.97 - tL) / hi if hi > 0 and tL + hi > 0.97 else 1.0
    down = (tL - 0.12) / -lo if lo < 0 and tL + lo < 0.12 else 1.0
    out = {}
    for i in idxs:
        L, C, h = to_oklch(colors[i])
        nL = tL + dL[i] * (max(0.0, up) if dL[i] > 0 else max(0.0, down))
        if cscale is not None:
            nC = tC * cscale
        elif bC > 0.02:
            nC = tC * min(2.0, C / bC)
        else:
            nC = tC
        dh = ((h - bh + 180) % 360) - 180 if C > 0.02 and bC > 0.02 else 0
        nL = max(0.10, min(0.985, nL))
        out[i] = gba(from_oklch(nL, nC, th + dh * hshift))
    return out
