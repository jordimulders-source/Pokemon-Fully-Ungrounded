#!/usr/bin/env python3
"""Project Grounded: itemiconen (24x24, 16 kleuren) voor de Rotom-apparaten.

Schrijft graphics/items/icons/rotom_<naam>.png en icon_palettes/rotom_<naam>.pal.
Vormen worden gevuld, daarna krijgt elke vorm automatisch een donkere rand en
een lichte bovenrand / donkere onderrand (schaduw).
"""
import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
W = H = 24

T, OUT, DARK, BODY, LIGHT, WHITE, GREY, DGREY, GLASS, GLASS2, ACC = range(11)


def base_pal(dark, body, light, glass=(40, 64, 96), glass2=(98, 156, 213), acc=(230, 60, 40)):
    pal = [(180, 180, 180), (32, 32, 40), dark, body, light, (248, 248, 248),
           (176, 184, 192), (104, 112, 120), glass, glass2, acc]
    while len(pal) < 16:
        pal.append((0, 0, 0))
    return pal


class Icon:
    def __init__(self):
        self.px = [[T] * W for _ in range(H)]
        self.shape = [[0] * W for _ in range(H)]  # vorm-id per pixel
        self.n = 0

    def put(self, x, y, c, sid=None):
        if 0 <= x < W and 0 <= y < H:
            self.px[y][x] = c
            if sid is not None:
                self.shape[y][x] = sid

    def rect(self, x0, y0, x1, y1, c, shaded=True):
        self.n += 1
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, c, self.n)
        if shaded:
            self.outline(self.n, c)

    def circle(self, cx, cy, r, c, shaded=True):
        self.n += 1
        for y in range(H):
            for x in range(W):
                if (x - cx + 0.5) ** 2 + (y - cy + 0.5) ** 2 <= r * r:
                    self.put(x, y, c, self.n)
        if shaded:
            self.outline(self.n, c)

    def outline(self, sid, c):
        inside = lambda x, y: 0 <= x < W and 0 <= y < H and self.shape[y][x] == sid
        new = {}
        for y in range(H):
            for x in range(W):
                if not inside(x, y):
                    continue
                if not (inside(x - 1, y) and inside(x + 1, y) and inside(x, y - 1) and inside(x, y + 1)):
                    new[(x, y)] = OUT
                elif c == BODY and not inside(x, y - 2):
                    new[(x, y)] = LIGHT
                elif c == BODY and not inside(x, y + 2):
                    new[(x, y)] = DARK
        for (x, y), v in new.items():
            self.px[y][x] = v

    def line(self, pts, c):
        for x, y in pts:
            self.put(x, y, c)

    def save(self, name, pal):
        im = Image.new('P', (W, H))
        flat = []
        for col in pal:
            flat += list(col)
        im.putpalette(flat + [0] * (768 - len(flat)))
        im.putdata([v for row in self.px for v in row])
        im.save(os.path.join(ROOT, 'graphics/items/icons', name + '.png'))
        with open(os.path.join(ROOT, 'graphics/items/icon_palettes', name + '.pal'), 'w', newline='\r\n') as f:
            f.write('JASC-PAL\n0100\n16\n')
            for col in pal:
                f.write('%d %d %d\n' % col)


def oven():
    i = Icon()
    i.rect(1, 5, 22, 19, BODY)
    i.rect(3, 7, 15, 17, GLASS)
    for y in range(8, 11):
        i.put(5 + (y - 8), y, GLASS2)
    i.put(4, 8, GLASS2)
    i.rect(17, 7, 20, 17, GREY, shaded=False)
    for y in (8, 11, 14):
        i.rect(18, y, 19, y + 1, DGREY, shaded=False)
    i.put(18, 16, ACC); i.put(19, 16, ACC)
    i.rect(3, 20, 5, 20, OUT, shaded=False)
    i.rect(18, 20, 20, 20, OUT, shaded=False)
    i.save('rotom_microwave_oven', base_pal((168, 56, 24), (240, 112, 48), (255, 184, 120), acc=(80, 208, 96)))


def washer():
    i = Icon()
    i.rect(3, 1, 20, 22, BODY)
    i.rect(5, 3, 18, 5, GREY, shaded=False)
    i.rect(15, 3, 17, 5, DGREY, shaded=False)
    i.put(6, 4, ACC); i.put(8, 4, GLASS2)
    i.circle(12, 14, 6.6, OUT, shaded=False)
    i.circle(12, 14, 5.4, DGREY, shaded=False)
    i.circle(12, 14, 4.4, GLASS2, shaded=False)
    i.circle(12, 15, 3.0, GLASS, shaded=False)
    i.put(10, 11, WHITE); i.put(9, 12, WHITE)
    i.save('rotom_washing_machine', base_pal((120, 136, 160), (216, 224, 236), (248, 252, 255), glass=(32, 88, 184), glass2=(96, 168, 240)))


def fridge():
    i = Icon()
    i.rect(5, 0, 18, 23, BODY)
    i.line([(x, 8) for x in range(6, 18)], OUT)
    i.line([(x, 9) for x in range(6, 18)], LIGHT)
    i.rect(15, 3, 16, 6, DGREY, shaded=False)
    i.rect(15, 11, 16, 17, DGREY, shaded=False)
    i.put(7, 2, WHITE); i.put(7, 3, WHITE); i.put(7, 11, WHITE); i.put(7, 12, WHITE)
    i.rect(6, 21, 17, 22, DARK, shaded=False)
    i.save('rotom_refrigerator', base_pal((112, 168, 200), (200, 236, 248), (240, 252, 255)))


def fan():
    i = Icon()
    i.rect(6, 20, 17, 22, BODY)
    i.rect(11, 15, 12, 19, DGREY, shaded=False)
    i.circle(12, 9, 8.6, OUT, shaded=False)
    i.circle(12, 9, 7.6, GREY, shaded=False)
    i.circle(12, 9, 6.6, GLASS2, shaded=False)
    # drie wieken (poolcoordinaten rond de naaf)
    import math
    for y in range(H):
        for x in range(W):
            dx, dy = x + 0.5 - 12, y + 0.5 - 9
            r = math.hypot(dx, dy)
            if r < 1.5 or r > 6.2:
                continue
            ang = math.degrees(math.atan2(dy, dx)) % 360
            for bl in (270, 30, 150):
                d = (ang - bl + 180) % 360 - 180
                if -28 <= d <= 22 + r * 2:
                    i.put(x, y, DARK if d > 12 + r * 2 else BODY)
    i.line([(11, 8), (12, 8), (11, 9), (12, 9)], OUT)
    i.save('rotom_electric_fan', base_pal((88, 64, 144), (152, 120, 216), (208, 192, 248), glass2=(200, 228, 248)))


def mower():
    i = Icon()
    # handgreep
    for k in range(10):
        i.put(16 + k // 2, 12 - k, OUT)
        i.put(17 + k // 2, 12 - k, DGREY)
    i.rect(19, 1, 23, 2, OUT, shaded=False)
    i.rect(2, 13, 18, 18, BODY)
    i.rect(6, 9, 13, 13, DGREY, shaded=False)
    i.rect(7, 8, 12, 9, OUT, shaded=False)
    i.put(8, 10, GREY); i.put(9, 10, GREY)
    i.circle(5, 19, 2.8, OUT, shaded=False)
    i.circle(5, 19, 1.4, GREY, shaded=False)
    i.circle(16, 19, 2.8, OUT, shaded=False)
    i.circle(16, 19, 1.4, GREY, shaded=False)
    i.save('rotom_lawn_mower', base_pal((40, 112, 48), (88, 184, 72), (168, 232, 128)))


if __name__ == '__main__':
    for f in (oven, washer, fridge, fan, mower):
        f()
