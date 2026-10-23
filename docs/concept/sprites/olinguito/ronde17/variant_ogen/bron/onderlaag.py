"""onderlaag.py <repo-root> [dx dy]: zet het lijf van Poochyena (graphics/pokemon/poochyena, frame 1)
om naar olinguito-tekens en print het als delen_abs-rijen ('y x pixels'), verschoven met dx,dy.
Alleen romp en achterpoot (kop en voorpoten weggelaten). Dit is de onderlaag (skelet) die daarna
met de hand is overgetekend; niet geschaald.
Kleurvertaling: zwart (2) -> 0, donkergrijs (1, 5) -> 2 schaduw, grijs (4) -> 3 basis, lichtgrijs (3) -> 4.
"""
import sys
from PIL import Image

R = sys.argv[1]
dx = int(sys.argv[2]) if len(sys.argv) > 2 else 0
dy = int(sys.argv[3]) if len(sys.argv) > 3 else 5
im = Image.open(R + '/graphics/pokemon/poochyena/anim_front.png')
MAP = {2: '0', 1: '2', 5: '2', 13: '2', 4: '3', 3: '4', 11: '2', 12: '3'}


def romp(x, y):
    """Masker: romp + achterpoot van Poochyena, zonder kop en voorpoten."""
    if y < 21:
        return False
    if x < 36 and y < 35:          # kop
        return False
    if x >= 44 and y < 33:         # staartpluim (olinguito heeft eigen staart)
        return False
    if y < 28:                     # nekkraag (vachtpieken, geen anatomie)
        return False
    if x < 21:                     # verre voorpoot
        return False
    if y >= 44 and x < 39:         # dichtbije voorpoot
        return False
    if y >= 38 and x < 27:         # borst/voorpoot links
        return False
    return True


def pixels():
    out = {}
    for y in range(64):
        for x in range(64):
            c = im.getpixel((x, y))
            if c and romp(x, y):
                out[(x + dx, y + dy)] = MAP.get(c, '3')
    return out


if __name__ == '__main__':
    px = pixels()
    for y in sorted({k[1] for k in px}):
        xs = [k[0] for k in px if k[1] == y]
        x0, x1 = min(xs), max(xs)
        print(y, x0, ''.join(px.get((x, y), '.') for x in range(x0, x1 + 1)))
