"""Render parts.py -> anim_front (64x128) + normal.pal + zoom-preview. Gebruik: render.py parts.py out.png [zoom.png]"""
import sys, importlib.util
from PIL import Image

PAL = [
    (152, 208, 160),  # 0 transparant
    (255, 222, 156),  # 1 oranje glans
    (246, 176, 100),  # 2 oranje licht
    (226, 138, 66),   # 3 oranje basis
    (186, 98, 40),    # 4 oranje schaduw
    (142, 70, 28),    # 5 oranje diep / omlijning lichtkant
    (255, 250, 222),  # 6 creme licht
    (246, 222, 166),  # 7 creme
    (210, 172, 112),  # 8 creme schaduw
    (126, 74, 44),    # 9 chocolade (masker, sokken, ringen)
    (78, 42, 22),     # A chocolade donker
    (255, 214, 40),   # B goud (ogen)
    (204, 136, 8),    # C goud donker
    (255, 255, 255),  # D wit (glans, hoektand)
    (220, 196, 166),  # E klauw schaduw
    (40, 22, 14),     # F omlijning donker
]

def load(path):
    spec = importlib.util.spec_from_file_location('parts', path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def grid(layers):
    g = [[0] * 64 for _ in range(64)]
    for L in layers:
        for y, x, s in L:
            for i, c in enumerate(s):
                if c == '_':
                    continue
                g[y][x + i] = 0 if c == '.' else int(c, 16)
    return g

def save(out, g1, g2, pal=PAL):
    im = Image.new('P', (64, 128))
    flat = [v for c in pal for v in c]
    im.putpalette(flat + [0] * (768 - len(flat)))
    for y in range(64):
        for x in range(64):
            im.putpixel((x, y), g1[y][x]); im.putpixel((x, y + 64), g2[y][x])
    im.save(out, transparency=0)
    return im

if __name__ == '__main__':
    m = load(sys.argv[1])
    g1, g2 = grid(m.FRAME1), grid(m.FRAME2)
    dx, dy = getattr(m, 'SHIFT', (0, 0))
    def sh(g):
        n = [[0] * 64 for _ in range(64)]
        for y in range(64):
            for x in range(64):
                if g[y][x]: n[y + dy][x + dx] = g[y][x]
        return n
    g1, g2 = sh(g1), sh(g2)
    im = save(sys.argv[2], g1, g2, getattr(m, 'PAL', PAL))
    print('oppervlak', sum(1 for r in g1 for v in r if v))
    if len(sys.argv) > 3:
        z = 8
        big = im.convert('RGBA').resize((64 * z, 128 * z), Image.NEAREST)
        c = Image.new('RGBA', (64 * z * 2 + 40, 128 * z), (152, 208, 160, 255))
        c.alpha_composite(big, (0, 0))
        one = im.convert('RGBA')
        for k, s in enumerate((1, 2, 3)):
            c.alpha_composite(one.resize((64 * s, 128 * s), Image.NEAREST), (64 * z + 20, sum((128 * t + 10) for t in (1, 2, 3)[:k])))
        c.save(sys.argv[3])
