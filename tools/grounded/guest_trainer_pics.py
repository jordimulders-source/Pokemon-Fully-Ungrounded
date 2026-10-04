#!/usr/bin/env python3
"""Project Grounded: trainerfoto's voor de gasten en trio-compagnons van het Battle Stadium.

- Gasten (Wario, Yoshi, Golbat, Grimer, Boo, Mew, Shy Guys): bronnen in graphics/grounded/trainers/guests/*_bron.png.
  Dat zijn de oorspronkelijke sprites op hun echte pixelgrootte (de geüploade plaatjes waren vergroot en/of
  JPEG/WebP; eenmalig teruggezet op hun pixelraster: Yoshi 12x, Golbat 6,5x, Grimer 3,5x, Mew 4x, Wario 2x,
  Boo en Shy Guys 1x; per cel de mediaan, ruiskleuren samengevoegd, achtergrond transparant). Hier alleen nog een
  gehele vergroting (nearest neighbour), onderaan gecentreerd in 64x64, max. 15 kleuren + transparant.
- Ditto: de Youngster met een Ditto-gezicht (stipogen, simpele glimlach) en Ditto-paarse kleren.
- Burglar: graphics/grounded/trainers/burglar/burglar_gen3.png (tools/grounded/burglar_sprite.py).
- Trio's: het voorplaatje (frame 1, normal.pal) van de eerste Pokémon van de collectie.
Gebruik: python3 tools/grounded/guest_trainer_pics.py [contactsheet.png]
"""
import os, sys
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SRC = os.path.join(ROOT, 'graphics/grounded/trainers/guests/')
OUT = os.path.join(ROOT, 'graphics/trainers/front_pics/')
BG = (115, 197, 164)   # index 0, zoals de andere trainerfoto's

# naam: (bron, vergroting, onderste bronrijen weglaten)
GUESTS = {
    'guest_wario': ('wario_flex_bron.png', 1.5, 0),  # dubbele biceps (Jordi); 43x34, te breed voor 2x: zie scale3x
    'guest_yoshi': ('yoshi_bron.png', 2, 0),
    'guest_golbat': ('golbat_bron.png', 1, 0),     # Game Boy-sprite, al 56 px
    'guest_grimer': ('grimer_bron.png', 1, 0),
    'guest_boo': ('boo_bron.png', 2, 0),
    'guest_mew': ('mew_bron.png', 1, 0),
    'guest_shy_guy_red': ('shyguy_red_bron.png', 2, 0),
    'guest_shy_guy_green': ('shyguy_green_bron.png', 2, 0),
    'guest_shy_guy_pink': ('shyguy_pink_bron.png', 2, 0),
    'guest_shy_guy_black': ('shyguy_black_bron.png', 2, 0),
}

# bronrijen die maar 1x i.p.v. 2x hoog worden, zodat een figuur van 34 rijen precies in 64 past (rustige rijen in het lijf)
SLIM = {}
# gespiegeld, zodat ze in het gevecht naar de speler (links) kijken
FLIP = {'guest_wario'}

# trio-compagnons: uitvoernaam -> soortmap (eerste Pokémon van de collectie)
TRIOS = {
    'trio_mascots': 'pikachu', 'trio_starters': 'charizard', 'trio_fossils': 'aerodactyl', 'trio_eevees': 'jolteon',
    'trio_lake': 'mesprit', 'trio_regis': 'regirock', 'trio_birds': 'zapdos', 'trio_beasts': 'suicune',
    'trio_pseudos': 'dragonite', 'trio_swords': 'cobalion', 'trio_loyal': 'okidogi', 'trio_tapus': 'tapu_koko',
    'trio_genies': 'landorus', 'trio_ultras': 'nihilego', 'trio_ruin': 'chien_pao', 'trio_weather': 'rayquaza',
    'trio_creators': 'giratina',
}


def gba(c):
    return tuple((v >> 3) << 3 for v in c[:3])


def to_indexed(rgba):
    """RGBA 64x64 -> P met index 0 = transparant; faalt bij meer dan 15 kleuren."""
    cols = []
    for c in rgba.get_flattened_data():
        if c[3] and gba(c) not in cols:
            cols.append(gba(c))
    assert len(cols) <= 15, len(cols)
    cols.sort(key=lambda c: sum(c))
    out = Image.new('P', rgba.size, 0)
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            if px[x, y][3]:
                out.putpixel((x, y), cols.index(gba(px[x, y])) + 1)
    pal = list(BG)
    for c in cols:
        pal += c
    pal += [0] * (768 - len(pal))
    out.putpalette(pal)
    return out


def scale3x(img):
    """Scale3x (pixel-art-vergroting die schuine randen netjes houdt); daarna halveren geeft een nette 1,5x."""
    W, H = img.size
    p = img.load()
    out = Image.new('RGBA', (W * 3, H * 3))
    q = out.load()
    g = lambda x, y: p[min(max(x, 0), W - 1), min(max(y, 0), H - 1)]
    for y in range(H):
        for x in range(W):
            A, B, C, D, E, F, G, Hh, I = [g(x + dx, y + dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1)]
            e = [E] * 9
            if B != Hh and D != F:
                e[0] = D if D == B else E
                e[1] = B if (D == B and E != C) or (B == F and E != A) else E
                e[2] = F if B == F else E
                e[3] = D if (D == B and E != G) or (D == Hh and E != A) else E
                e[5] = F if (B == F and E != I) or (Hh == F and E != C) else E
                e[6] = D if D == Hh else E
                e[7] = Hh if (D == Hh and E != I) or (Hh == F and E != G) else E
                e[8] = F if Hh == F else E
            for i in range(9):
                q[x * 3 + i % 3, y * 3 + i // 3] = e[i]
    return out


def guest(src, k, trim, slim=()):
    im = Image.open(SRC + src).convert('RGBA')
    if trim:
        im = im.crop((0, 0, im.width, im.height - trim))
    if k == 1.5:
        big = scale3x(im)
        big = big.resize((big.width // 2, big.height // 2), Image.NEAREST)
    else:
        big = im.resize((im.width * k, im.height * k), Image.NEAREST)
    if slim:
        rows = [big.crop((0, y * k, big.width, y * k + (1 if y in slim else k))) for y in range(im.height)]
        big = Image.new('RGBA', (big.width, sum(r.height for r in rows)))
        y = 0
        for r in rows:
            big.paste(r, (0, y))
            y += r.height
    im = big
    assert im.width <= 64 and im.height <= 64, (src, im.size)
    out = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    out.alpha_composite(im, ((64 - im.width) // 2, 64 - im.height))
    return to_indexed(out)


def ditto():
    """Youngster als Ditto: kleren/pet Ditto-paars, gezicht = twee stipjes en een kleine glimlach."""
    im = Image.open(OUT + 'youngster.png')
    pal = im.getpalette()[:48]
    purple = {5: (216, 168, 240), 12: (192, 128, 224), 13: (152, 96, 200), 6: (120, 72, 168),
              8: (88, 48, 128), 7: (64, 40, 96), 10: (232, 192, 248), 11: (200, 144, 232), 9: (240, 216, 248)}
    for i, c in purple.items():
        pal[i * 3:i * 3 + 3] = list(gba(c))
    px = im.load()
    LIGHT, SKIN, INK = 1, 2, 15
    # gezicht (x 28-36, rijen 24-28) leegmaken: lichte huid, rechts de schaduw
    for y in range(24, 29):
        for x in range(28, 35):
            px[x, y] = LIGHT
        px[35, y] = SKIN
    px[28, 28] = 4
    # Ditto: twee stipjes en een kleine zachte glimlach (Jordi: derpy, niet gemeen)
    for p in ((30, 25), (33, 25)):
        px[p] = INK
    for p in ((30, 27), (31, 28), (32, 28), (33, 27)):
        px[p] = INK
    im.putpalette(pal + [0] * (768 - len(pal)))
    return im


def trio(folder):
    d = os.path.join(ROOT, 'graphics/pokemon', folder)
    f = 'anim_front.png' if os.path.exists(os.path.join(d, 'anim_front.png')) else 'front.png'
    im = Image.open(os.path.join(d, f)).crop((0, 0, 64, 64))
    lines = open(os.path.join(ROOT, 'graphics/pokemon', folder, 'normal.pal')).read().split('\n')[3:19]
    pal = []
    for l in lines:
        pal += [int(v) for v in l.split()]
    im.putpalette(pal + [0] * (768 - len(pal)))
    return im


def main():
    pics = {}
    for name, (src, k, trim) in GUESTS.items():
        pics[name] = guest(src, k, trim, SLIM.get(name, ()))
        if name in FLIP:
            pics[name] = pics[name].transpose(Image.FLIP_LEFT_RIGHT)
    pics['guest_ditto'] = ditto()
    pics['guest_burglar'] = Image.open(os.path.join(ROOT, 'graphics/grounded/trainers/burglar/burglar_gen3.png'))
    for name, folder in TRIOS.items():
        pics[name] = trio(folder)
    for name, im in pics.items():
        im.save(OUT + name + '.png')
    if len(sys.argv) > 1:   # contactsheet, 3x vergroot
        n = len(pics); cols = 9; rows = (n + cols - 1) // cols
        sheet = Image.new('RGB', (cols * 200, rows * 200), (40, 40, 48))
        for i, (name, im) in enumerate(pics.items()):
            z = im.convert('RGBA').resize((192, 192), Image.NEAREST)
            tile = Image.new('RGB', (192, 192), (200, 216, 232))
            mask = Image.new('L', (64, 64), 0)
            mask.putdata([0 if v == 0 else 255 for v in im.get_flattened_data()])
            tile.paste(z.convert('RGB'), (0, 0), mask.resize((192, 192), Image.NEAREST))
            sheet.paste(tile, ((i % cols) * 200 + 4, (i // cols) * 200 + 4))
        sheet.save(sys.argv[1])
    print(len(pics), 'trainerfoto\'s geschreven')


if __name__ == '__main__':
    main()
