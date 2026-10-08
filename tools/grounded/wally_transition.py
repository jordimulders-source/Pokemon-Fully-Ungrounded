#!/usr/bin/env python3
"""Project Grounded: B_TRANSITION_WALLY_VHS (het laatste Wally-gevecht, Victory Road).

Een oude VHS-band. Blauw scherm, "PLAY", het etiket ("WALLY - 1ST POKEMON / DAD: DO NOT TAPE OVER"). Dan de beelden van
Route 102: Wally gooit met de geleende Zigzagoon een Poké Ball naar Ralts, de bal wiebelt, "Gotcha!". De band spoelt
door (>> FF) door zijn groei: Mauville (Kirlia komt de bal uit), Meteor Falls (Wally draait zijn rondje: "Fall of
Meteor."), Kirlia evolueert tot Gallade. Dan PLAY, een snelle zoom op zijn vastberaden gezicht in Victory Road, PAUSE
(het beeld trilt), sneeuw, gevecht.

Gameplay-graphics uit de game zelf (gevechtsachtergronden, tekstvak, Pokémon- en trainerplaatjes). VHS-look: kleur
loopt uit (chroma verschoven en vervaagd), iets valer, een sporingsband met ruis. De C-kant (battle_transition.c) laat
de beeldlijnen in die band horizontaal verspringen (HBlank) en het beeld trillen bij PAUSE; per gameframe staat dat in
film_wally_fx.bin (u8 band-y of 255, u8 sterkte | vlaggen).
Gebruik: python3 tools/grounded/wally_transition.py [voorbeeldmap]
"""
import math, os, struct, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film
import gbagfx_render as gr
from film import W, H, text35, text35_width

ROOT = film.ROOT
FX_SHAKE = 0x40     # PAUSE: verticaal trillen
FX_WOBBLE = 0x80    # doorspoelen: het hele beeld golft
STEP = 3            # gameframes per beeld van de band

WHITE, BLACK, GREY = (248, 248, 248), (8, 8, 8), (120, 120, 128)
FIXED = [BLACK, WHITE, GREY]
BLUE = (16, 40, 200)

# ------------------------------------------------------------------ bouwstenen
def sp(path, frame=0, pal=None, flip=False):
    im = gr.sprite(path, pal, frame)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im


RALTS = sp('graphics/pokemon/ralts/anim_front_gba.png')
KIRLIA = sp('graphics/pokemon/kirlia/anim_front_gba.png')
GALLADE = sp('graphics/pokemon/gallade/anim_front.png')
ZIGZAG_BACK = sp('graphics/pokemon/zigzagoon/back_gba.png')
WALLY_BACK = [sp('graphics/trainers/back_pics/wally.png', k) for k in range(4)]
WALLY = sp('graphics/trainers/front_pics/wally.png')

ENV = {n: gr.battle_env(n) for n in ('tall_grass', 'building', 'cave')}


def textbox_layer():
    raw = open(os.path.join(ROOT, 'graphics/battle_interface/textbox_map.bin'), 'rb').read()
    m = struct.unpack('<%dH' % (len(raw) // 2), raw)
    tiles = np.array(Image.open(os.path.join(ROOT, 'graphics/battle_interface/textbox.png')))
    P = np.array(gr.jasc(os.path.join(ROOT, 'graphics/battle_interface/textbox_0.pal')), np.uint8)
    tw = tiles.shape[1] // 8
    out = np.zeros((48, 240, 3), np.uint8)
    for r in range(6):
        for c in range(30):
            v = m[(14 + r) * 32 + c]
            ty, tx = divmod(v & 0x3FF, tw)
            b = tiles[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            if v & 0x400:
                b = b[:, ::-1]
            if v & 0x800:
                b = b[::-1, :]
            out[r * 8:r * 8 + 8, c * 8:c * 8 + 8] = P[b & 15]
    return out


TEXTBOX = textbox_layer()


def battle(env, sprites, lines=()):
    """Gevechtsbeeld: achtergrond, plaatjes [(RGBA, x, y)] en het tekstvak met max. twee regels."""
    img = Image.fromarray(ENV[env].copy())
    for s, x, y in sprites:
        if s is not None:
            img.paste(s, (int(x), int(y)), s)
    a = np.array(img)
    a[112:160] = TEXTBOX
    for i, l in enumerate(lines):
        gr.text(a, 16, 118 + i * 16, l, WHITE, (104, 104, 120))
    return a


def ball_sprite(open_=0, rot=0):
    """Poké Ball (12x12) getekend; rot: -1/0/1 kantelen (wiebelen); open_: 1 = open (rode flits)."""
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([2, 2, 13, 13], fill=(240, 40, 40), outline=(40, 32, 40))
    d.chord([2, 2, 13, 13], 0, 180, fill=(248, 248, 248), outline=(40, 32, 40))
    d.line([(2, 8), (13, 8)], fill=(40, 32, 40))
    d.ellipse([6, 6, 9, 9], fill=(248, 248, 248), outline=(40, 32, 40))
    d.point([(4, 4), (5, 4)], fill=(255, 200, 200))
    if rot:
        im = im.rotate(-22 * rot, resample=Image.NEAREST)
    return im


def white_silhouette(s, col=(248, 248, 248)):
    a = np.array(s)
    a[a[..., 3] > 0, :3] = col
    return Image.fromarray(a, 'RGBA')


def shrink(s, k):
    w = max(1, int(64 * k))
    t = s.resize((w, w), Image.NEAREST)
    out = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    out.paste(t, ((64 - w) // 2, 64 - w - 4 + int(4 * k)), t)
    return out


# ------------------------------------------------------------------ VHS-bewerking
def vhs(a, seed=0):
    """Kleur loopt uit naar rechts en vervaagt, iets valer en minder contrast (een oude band)."""
    f = a.astype(np.float64)
    Y = f @ np.array([0.299, 0.587, 0.114])
    C = f - Y[..., None]
    Cs = np.roll(C, 2, axis=1)
    Cb = (np.roll(Cs, -1, axis=1) + Cs * 2 + np.roll(Cs, 1, axis=1)) / 4.0
    Ys = (np.roll(Y, 1, axis=1) * 0.2 + Y * 0.8)
    out = Ys[..., None] + Cb * 0.8
    out = out * 0.9 + 14
    return np.clip(out, 0, 255).astype(np.uint8)


def noise_band(a, y0, h, rng, amount=0.5):
    """Sporingsband: horizontale ruisstrepen (wit/grijs/zwart) over h lijnen vanaf y0."""
    a = a.copy()
    for y in range(max(0, y0), min(H, y0 + h)):
        x = 0
        while x < W:
            run = rng.randint(2, 18)
            r = rng.rand()
            if r < amount * 0.45:
                a[y, x:x + run] = WHITE
            elif r < amount * 0.7:
                a[y, x:x + run] = GREY
            elif r < amount * 0.85:
                a[y, x:x + run] = BLACK
            x += run + rng.randint(0, 10)
    return a


SNOW_TILES = None


def snow(rng):
    """Sneeuw (geen signaal) uit een vaste set ruistiles: goedkoop, ziet er toch willekeurig uit."""
    global SNOW_TILES
    if SNOW_TILES is None:
        r0 = np.random.RandomState(99)
        SNOW_TILES = []
        for k in range(24):
            t = np.zeros((8, 8, 3), np.uint8)
            v = r0.rand(8, 8)
            t[v < 0.35] = BLACK
            t[(v >= 0.35) & (v < 0.7)] = GREY
            t[v >= 0.7] = WHITE
            SNOW_TILES.append(t)
    a = np.zeros((H, W, 3), np.uint8)
    for r in range(20):
        for c in range(30):
            a[r * 8:r * 8 + 8, c * 8:c * 8 + 8] = SNOW_TILES[rng.randint(len(SNOW_TILES))][::rng.choice([1, -1]), ::rng.choice([1, -1])]
    return a


def osd(a, text, x, y, scale=2):
    """VHS-schermtekst: wit met zwarte rand."""
    def px(cx, cy, col):
        if 0 <= cx < W and 0 <= cy < H:
            a[cy, cx] = col
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (1, 1)):
        text35(lambda u, v: px(u + dx, v + dy, BLACK), x, y, text, scale)
    text35(lambda u, v: px(u, v, WHITE), x, y, text, scale)
    return a


def play_tri(a, x, y, n=1, scale=2):
    """Afspeeldriehoek(en) ▶ / ▶▶ in OSD-stijl."""
    for k in range(n):
        ox = x + k * 6 * scale
        for j in range(5 * scale):
            half = min(j, 5 * scale - 1 - j)
            for i in range(half + 1):
                for dx, dy, col in ((1, 0, BLACK), (0, 1, BLACK), (0, 0, WHITE)):
                    px, py = ox + i + dx, y + j + dy
                    if 0 <= px < W and 0 <= py < H:
                        a[py, px] = col
    return a


def pause_bars(a, x, y, scale=2):
    for k in (0, 3):
        for j in range(5 * scale):
            for i in range(2 * scale):
                for dx, dy, col in ((1, 0, BLACK), (0, 1, BLACK), (0, 0, WHITE)):
                    px, py = x + k * scale + i + dx, y + j + dy
                    if 0 <= px < W and 0 <= py < H:
                        a[py, px] = col
    return a


def timecode(a, sec):
    s = 'SP %d:%02d:%02d' % (sec // 3600, (sec // 60) % 60, sec % 60)
    return osd(a, s, W - 12 - film.text35_width(s, 2), 8)


# ------------------------------------------------------------------ het vastberaden gezicht (Victory Road)
def scale2x(img):
    W0, H0 = img.size
    p = img.load()
    out = Image.new('RGBA', (W0 * 2, H0 * 2))
    q = out.load()
    g = lambda x, y: p[min(max(x, 0), W0 - 1), min(max(y, 0), H0 - 1)]
    for y in range(H0):
        for x in range(W0):
            B, D, E, F, Hh = g(x, y - 1), g(x - 1, y), g(x, y), g(x + 1, y), g(x, y + 1)
            e0 = e1 = e2 = e3 = E
            if B != Hh and D != F:
                e0 = D if D == B else E
                e1 = F if B == F else E
                e2 = D if D == Hh else E
                e3 = F if Hh == F else E
            q[x * 2, y * 2], q[x * 2 + 1, y * 2], q[x * 2, y * 2 + 1], q[x * 2 + 1, y * 2 + 1] = e0, e1, e2, e3
    return out


def determined_wally():
    """Wally's trainerplaatje met een vastberaden gezicht: wenkbrauwen die schuin naar het midden aflopen (de ogen
    worden smaller) en de mond dicht. Bewerkt op 1x, daarna Scale2x twee keer (4x) voor de 'digitale zoom'."""
    im = WALLY.copy()
    px = im.load()
    brow = (65, 106, 24)      # donkergroen van zijn haar
    lip = (123, 90, 82)       # donkerbruin (lijnen in het gezicht)
    # linkerwenkbrauw (ogen 29-30): hoog buiten, laag bij de neus
    for (x, y) in ((28, 19), (29, 20), (30, 20), (31, 21)):
        px[x, y] = brow + (255,)
    # rechterwenkbrauw (oog 35-36): laag bij de neus, hoog buiten; het oogwit erboven valt weg
    for (x, y) in ((34, 21), (35, 20), (36, 20), (37, 19)):
        px[x, y] = brow + (255,)
    # mond dicht: een strakke lijn in plaats van de open mond
    px[33, 26] = lip + (255,)
    px[33, 24] = (222, 180, 164, 255)   # geen 'o' meer: de bovenrand van de open mond wordt huid
    px[34, 25] = (189, 148, 115, 255)   # mondhoek iets omlaag
    return im


BIG_WALLY = None


def face_frame(zoom):
    """Victory Road (grot) met Wally; zoom (2.5..6) rond zijn gezicht, uit een Scale2x^3-vergroting (8x)."""
    global BIG_WALLY
    if BIG_WALLY is None:
        BIG_WALLY = scale2x(scale2x(scale2x(determined_wally())))
    u = (zoom - 2.5) / 3.0
    bgz = 2 + u
    cave = Image.fromarray(ENV['cave'][0:100, 40:200])
    bg = cave.resize((int(160 * bgz), int(100 * bgz)), Image.NEAREST)
    img = Image.new('RGB', (W, H))
    img.paste(bg, (int(120 - bg.width / 2), int(70 - bg.height / 2 - u * 10)))
    k = zoom / 8.0
    s = BIG_WALLY.resize((max(1, int(512 * k)), max(1, int(512 * k))), Image.NEAREST)
    fx, fy = 33 * 8, 22 * 8              # gezicht in 8x-coördinaten
    cx = 132 - u * 8
    cy = 56 + u * 26
    img.paste(s, (int(round(cx - fx * k)), int(round(cy - fy * k))), s)
    return np.array(img)


# ------------------------------------------------------------------ tijdlijn
def build(preview=None):
    f = film.Film('wally')
    rng = np.random.RandomState(5)
    fx = []

    def add(img, ps, n=1, band=255, strength=0, flags=0):
        for _ in range(n):
            f.add(img, ps)
            fx.append((band, strength | flags))

    def pal_for(imgs):
        p = film.auto_palettes(imgs, FIXED)
        return f.palset(p[0][:15], p[1][:15], p[2][:15])

    # 0-7: leeg (de wereld wordt zwart)
    blank_ps = f.palset([BLACK], [BLACK], [BLACK])
    for t in range(8):
        f.add(None, blank_ps)
        fx.append((255, 0))

    # 8-23: blauw scherm, PLAY, het etiket
    blue = np.zeros((H, W, 3), np.uint8)
    blue[:] = BLUE
    b1 = blue.copy()
    osd(b1, 'PLAY', 16, 14)
    play_tri(b1, 52, 14)
    lbl = 'WALLY - 1ST POKEMON'
    osd(b1, lbl, (W - text35_width(lbl, 2)) // 2, 68)
    lbl2 = '(DAD: DO NOT TAPE OVER)'
    osd(b1, lbl2, (W - text35_width(lbl2, 1)) // 2, 86, 1)
    ps_blue = f.palset([BLUE, WHITE, BLACK, GREY], [BLUE, WHITE, BLACK, GREY], [BLUE, WHITE, BLACK, GREY])
    add(b1, ps_blue, 18)

    # 26-31: sneeuw, dan de band begint
    sn = [snow(rng) for _ in range(3)]
    ps_snow = f.palset(FIXED, FIXED, FIXED)
    for k in range(6):
        add(sn[k % 3], ps_snow)

    # ---------------- Route 102: Wally vangt Ralts met de geleende Zigzagoon
    S1 = 92
    def s1(t):
        spr = []
        lines = []
        zig = (ZIGZAG_BACK, 40, 52)
        ralts = (RALTS, 144, 22)
        if t < 16:
            # Wally gooit (achterkant, werpanimatie)
            k = min(3, t // 4)
            spr = [(WALLY_BACK[k], 30 - t, 48), ralts]
            lines = ['WALLY threw a POKé BALL!']
            if t >= 10:
                bx, by = 60 + (t - 10) * 10, 70 - (t - 10) * 6
                spr.append((ball_sprite(), bx, by))
            return battle('tall_grass', spr, lines)
        lines = ['WALLY threw a POKé BALL!']
        if t < 30:
            u = (t - 16) / 14.0
            bx = 120 + u * 50
            by = 34 - math.sin(u * math.pi) * 22 + u * 4
            spr = [zig, ralts, (ball_sprite(rot=int(t / 2) % 3 - 1), bx, by)]
        elif t < 38:
            # Ralts wordt rood-wit en krimpt de bal in
            k = (t - 30) / 8.0
            r = white_silhouette(RALTS, (248, 160, 160) if t % 2 else (248, 248, 248))
            spr = [zig, (shrink(r, 1 - k * 0.9), 144, 22), (ball_sprite(), 170, 36)]
        elif t < 48:
            # de bal valt op het platform
            k = (t - 38) / 10.0
            spr = [zig, (ball_sprite(), 170, 36 + k * k * 28)]
        elif t < 72:
            # drie keer wiebelen
            w = ((t - 48) // 4) % 4
            rot = [0, -1, 0, 1][w] if (t - 48) < 22 else 0
            spr = [zig, (ball_sprite(rot=rot), 170 + rot, 64)]
        else:
            spr = [zig, (ball_sprite(), 170, 64)]
            lines = ['Gotcha!', 'RALTS was caught!']
        a = battle('tall_grass', spr, lines)
        if 72 <= t < 80:
            # klik: sterretjes rond de bal
            d = ImageDraw.Draw(Image.fromarray(a))
            for k, (dx, dy) in enumerate(((-8, -8), (16, -10), (20, 6), (-10, 8))):
                x, y = 176 + dx * (1 + (t - 72) / 8.0), 70 + dy * (1 + (t - 72) / 8.0)
                for (ox, oy) in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = int(x + ox), int(y + oy)
                    if 0 <= xx < W and 0 <= yy < 112:
                        a[yy, xx] = (248, 232, 96)
        return a

    # beelden van de band: 20 per seconde (elke 3 gameframes), dat voelt als een oude videoband
    raw1 = {}
    for t in range(0, S1, STEP):
        raw1[t] = vhs(s1(t))
    ps1 = pal_for(list(raw1.values()))
    band_y = -10
    for t in range(S1):
        t0 = t - (t % STEP)
        base = raw1[t0]
        # sporingsband rolt omhoog in de eerste halve seconde
        if t < 30:
            band_y = 150 - t0 * 5
            if t == t0:
                a = noise_band(base, band_y, 6, rng, 0.6)
                if t < 12:
                    a = osd(a.copy(), 'PLAY', 16, 14)
                    a = play_tri(a, 52, 14)
                a = timecode(a, 12)
                cur = a
            add(cur, ps1, band=max(0, band_y), strength=4)
        else:
            if t == t0:
                cur = timecode(base.copy(), 12 + (t + 30) // 60)
            add(cur, ps1, band=255, strength=0)

    # ---------------- doorspoelen (>> FF)
    def ff_overlay(a, t):
        a = noise_band(a, (len(fx) * 23) % 140, 10, rng, 0.8)
        a = noise_band(a, (len(fx) * 23 + 70) % 140, 4, rng, 0.6)
        osd(a, 'FF', 16, 14)
        play_tri(a, 34, 14, 2)
        return timecode(a, 60 + max(0, t - 120) * 47)

    def s2(t):   # Mauville: Wally stuurt Kirlia de bal uit
        lines = ['WALLY sent out', 'KIRLIA!']
        spr = [(WALLY, 150 + t * 6, 8)]
        if t >= 6:
            k = min(1.0, (t - 6) / 6.0)
            spr.append((shrink(white_silhouette(KIRLIA) if t < 12 else KIRLIA, 0.2 + 0.8 * k), 144, 22))
        return battle('building', spr, lines)

    def s3(t):   # Meteor Falls: Wally draait zijn rondje
        lines = ['WALLY: Fall of Meteor.'] if t < 13 else ['WALLY: Wow! Very beaut!', 'Train much team.']
        flip = (t // 2) % 2 == 1
        return battle('cave', [(WALLY.transpose(Image.FLIP_LEFT_RIGHT) if flip else WALLY, 144 + (t % 4 - 2), 8)], lines)

    def s4(t):   # Kirlia evolueert tot Gallade
        a = np.zeros((H, W, 3), np.uint8)
        a[:] = (24, 24, 40)
        img = Image.fromarray(a)
        rate = max(1, 4 - t // 6)
        if t < 24:
            s = white_silhouette(KIRLIA if (t // rate) % 2 == 0 else GALLADE)
        else:
            s = GALLADE
        img.paste(s, (88, 30), s)
        a = np.array(img)
        a[112:160] = TEXTBOX
        if t < 24:
            gr.text(a, 16, 118, 'What? KIRLIA is evolving!', WHITE, (104, 104, 120))
        else:
            gr.text(a, 16, 118, 'KIRLIA evolved into', WHITE, (104, 104, 120))
            gr.text(a, 16, 134, 'GALLADE!', WHITE, (104, 104, 120))
        # fonkelingen
        r2 = np.random.RandomState(t // 2)
        for _ in range(14):
            x, y = r2.randint(0, W), r2.randint(0, 110)
            a[y, x] = WHITE
        return a

    for fn, n in ((s2, 26), (s3, 26), (s4, 40)):
        raws = {t: vhs(fn(t)) for t in range(0, n, STEP)}
        ps = pal_for(list(raws.values()))
        for t in range(n):
            t0 = t - (t % STEP)
            if t == t0:
                cur = ff_overlay(raws[t0].copy(), t + len(fx))
                by = (len(fx) * 23) % 140
            add(cur, ps, band=by, strength=6, flags=FX_WOBBLE)
        # korte sneeuwflits tussen de stukken
        for k in range(2):
            add(sn[k], ps_snow)

    # ---------------- Victory Road: PLAY, inzoomen op zijn gezicht, PAUSE
    zooms = {}
    ZN = 14
    for t in range(0, ZN, 2):
        z = 2.5 + 3.0 * min(1.0, (t + 2) / float(ZN - 2)) ** 0.7
        zooms[t] = vhs(face_frame(z))
    still = zooms[ZN - 2]
    ps5 = pal_for(list(zooms.values()))
    for t in range(ZN):
        if t % 2 == 0:
            cur = zooms[t].copy()
            osd(cur, 'PLAY', 16, 14)
            play_tri(cur, 52, 14)
            cur = timecode(cur, 2 * 3600 + 7 * 60 + 41)
        add(cur, ps5)
    # PAUSE: twee ruisbalken die licht verspringen, het beeld trilt verticaal (C)
    pa = []
    for k in range(2):
        a = still.copy()
        a = noise_band(a, 118 + k, 5, rng, 0.7)
        a = noise_band(a, 140 - k, 3, rng, 0.5)
        osd(a, 'PAUSE', 16, 14)
        pause_bars(a, 64, 14)
        a = timecode(a, 2 * 3600 + 7 * 60 + 41)
        pa.append(a)
    for t in range(34):
        add(pa[(t // 3) % 2], ps5, flags=FX_SHAKE)
    # sneeuw, eind
    for k in range(10):
        add(sn[k % 3], ps_snow, band=rng.randint(0, 150), strength=7)

    f.encode(preview)
    with open(os.path.join(film.OUT, 'film_wally_fx.bin'), 'wb') as fp:
        for b, s in fx:
            fp.write(struct.pack('<BB', b if 0 <= b < 160 else 255, s))
    assert len(fx) == len(f.frames), (len(fx), len(f.frames))
    print('wally: %d frames (%.1f s)' % (len(fx), len(fx) / 60.0))
    return f


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else None
    f = build(d)
    if d:
        fr = f.preview_frames
        n = len(fr)
        film.sheet(fr, [12, 34, 48, 64, 84, 110, 130, 150, 176, 200, 236, n - 30], os.path.join(d, 'wally_keys.png'))
