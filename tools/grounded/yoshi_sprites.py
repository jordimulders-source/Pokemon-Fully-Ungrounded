#!/usr/bin/env python3
"""Project Grounded: sprites voor Yoshi's Island (Spacetime-sidequest, tools/grounded/maptools/yoshis_island.py).

Overworlds (32x32, 9 frames: voor, achter, opzij (kijkt naar links), 2x stap voor, 2x stap achter, 2x stap opzij):
  yoshi_ow  Yoshi uit de SMW2-sheet van A.J. Nitro (origin/master: graphics/images (3).png): rij 1 = voor,
            rij 2 = achter, rij 3 = opzij. De sheet is zacht geschaald: de lichtgrijze rand buiten de omlijning
            valt weg (floodfill vanaf de rand).
  boo_ow    Commander Boo: de Boo uit graphics/grounded/trainers/guests/boo_bron.png; achter = het lijf zonder
            gezicht (hij schaamt zich); lopen = 1 px zweven.
  wario_ow  Wario: voor uit wario_bron.png, opzij uit wario_side_bron.png (gespiegeld), achter = voor met pet/haar
            over het gezicht.
  poochy_ow Poochy (64x32) uit de SMA3-sheet van A.J. Nitro (poochy_sma3.png, uit origin/master graphics/).
  qcloud_ow gevleugelde ?-wolk (64x32) uit sma3_objects.png; de vleugelslag zit in de stapframes.
  nep_enut_ow Nep-Enut: de Yoshi-frames blauw gekleurd, met boze wenkbrauwen.
Back pic (64x64, 4 frames, zoals Calyrex): Yoshi van achteren uit de 'Pokemon RS-stijl'-sheet van Freakyplanet
  (origin/master: graphics/images (4).png, rij 2 kolom 1).
De bronnen staan in graphics/grounded/yoshis_island/ (gekopieerd uit origin/master).
Gebruik: python3 tools/grounded/yoshi_sprites.py [voorbeeld.png]"""
import os, re, sys
import numpy as np
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SRC = os.path.join(ROOT, 'graphics/grounded/yoshis_island')
GUEST = os.path.join(ROOT, 'graphics/grounded/trainers/guests')
OW = os.path.join(ROOT, 'graphics/object_events/pics/people')
PAL = os.path.join(ROOT, 'graphics/object_events/palettes')


def strip_halo(im, bg_thresh=100, rings=2):
    """RGBA: de witte achtergrond (floodfill vanaf de rand, alleen zuiver wit) -> transparant, daarna nog `rings`
    lagen lichtgrijze zachte rand die aan de achtergrond grenzen (de sheet is zacht geschaald)."""
    a = np.array(im.convert('RGBA')).astype(int)
    h, w = a.shape[:2]
    rgb = a[..., :3]
    white = (rgb.min(2) >= 250) | (a[..., 3] == 0)
    grey = (rgb.min(2) >= bg_thresh) & ((rgb.max(2) - rgb.min(2)) < 40)
    out = np.zeros((h, w), bool)
    st = [(y, x) for y in range(h) for x in (0, w - 1)] + [(y, x) for x in range(w) for y in (0, h - 1)]
    while st:
        y, x = st.pop()
        if not (0 <= y < h and 0 <= x < w) or out[y, x] or not white[y, x]:
            continue
        out[y, x] = True
        st += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
    for _ in range(rings):
        nb = np.zeros_like(out)
        nb[1:] |= out[:-1]; nb[:-1] |= out[1:]; nb[:, 1:] |= out[:, :-1]; nb[:, :-1] |= out[:, 1:]
        out |= nb & grey
    a[out, 3] = 0
    a[~out, 3] = 255
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


def bbox(im):
    return im.crop(im.getbbox())


def place(spr, dy=0, size=32):
    f = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    w, h = spr.size
    if h > size:
        spr = spr.crop((0, h - size, w, h)); h = size
    f.alpha_composite(spr, ((size - w) // 2, size - h - dy))
    return f


def quantize(frames, n=15):
    """Gezamenlijk palet (index 0 = transparant) voor een lijst RGBA-frames -> (P-afbeelding 32*k x 32, palet)."""
    W = sum(f.width for f in frames)
    strip = Image.new('RGBA', (W, frames[0].height), (0, 0, 0, 0))
    x = 0
    for f in frames:
        strip.alpha_composite(f, (x, 0)); x += f.width
    a = np.array(strip)
    opaque = a[..., 3] > 127
    cols = a[..., :3][opaque]
    q = Image.fromarray(cols.reshape(1, -1, 3).astype(np.uint8), 'RGB').quantize(n, method=Image.MEDIANCUT, dither=0)
    pal = np.array(q.getpalette()[:n * 3]).reshape(-1, 3)
    pal = (pal // 8) * 8
    d = ((a[..., :3][:, :, None, :].astype(int) - pal[None, None]) ** 2).sum(3)
    idx = np.where(opaque, d.argmin(2) + 1, 0).astype(np.uint8)
    im = Image.fromarray(idx, 'P')
    full = [(0, 0, 0)] + [tuple(int(v) for v in c) for c in pal]
    full += [(0, 0, 0)] * (16 - len(full))
    full[0] = (115, 197, 164)
    im.putpalette([v for c in full for v in c] + [0] * (768 - 48))
    return im, full


def write_pal(path, cols):
    with open(path, 'w') as fh:
        fh.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % tuple(c) for c in cols))


def sheet9(front, back, side, f1, f2, b1, b2, s1, s2):
    return [place(front), place(back), place(side), place(f1), place(f2), place(b1), place(b2), place(s1), place(s2)]


# ---------------------------------------------------------------------------------------------- Yoshi
def yoshi():
    sh = Image.open(os.path.join(SRC, 'yoshi_smw2.png')).convert('RGB')
    # exacte vakken (componenten van de sheet); de oneven frames zijn scherp, de even frames zijn tussenbeelden
    fx = [(8, 24), (28, 43), (47, 63), (67, 82), (86, 102), (106, 121), (125, 141), (145, 160)]
    sx = [(8, 32), (37, 60), (64, 86), (90, 113), (117, 142), (146, 169), (173, 195), (199, 222)]

    def cut(x0, x1, y0, y1):
        return bbox(strip_halo(sh.crop((x0 - 1, y0 - 1, x1 + 1, y1 + 1))))
    front = [cut(a, b, 6, 37) for a, b in fx]
    back = [cut(a, b, 46, 78) for a, b in fx]
    side = [cut(a, b, 84, 116) for a, b in sx]
    return sheet9(front[1], back[1], side[1], front[3], front[7], back[3], back[7], side[3], side[7])


# ---------------------------------------------------------------------------------------------- Boo
def boo():
    b = Image.open(os.path.join(GUEST, 'boo_bron.png')).convert('RGBA')
    b = bbox(b)
    a = np.array(b).astype(int)
    # achterkant: alles binnen de omlijning wordt lijfkleur (wit), de schaduwtint onderaan blijft
    body = a.copy()
    rgb = a[..., :3]
    inner = (a[..., 3] > 0) & (rgb.sum(2) > 60)
    dark_face = inner & ((rgb[..., 0] > 150) & (rgb[..., 1] < 140))       # rode mond / tong
    eyes = (a[..., 3] > 0) & (rgb.sum(2) <= 60)
    # ogen/mond-omlijning binnen het lijf: alleen pixels die niet aan de buitenkant grenzen
    h, w = a.shape[:2]
    outer = np.zeros((h, w), bool)
    for y in range(h):
        for x in range(w):
            if a[y, x, 3] > 0 and rgb[y, x].sum() <= 60:
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if not (0 <= ny < h and 0 <= nx < w) or a[ny, nx, 3] == 0:
                        outer[y, x] = True
    white = np.array([248, 248, 248])
    shadow = (rgb[..., 2] > rgb[..., 0] + 10)
    sel = (a[..., 3] > 0) & ~outer & ~shadow
    body[sel, :3] = white
    back = Image.fromarray(body.astype(np.uint8), 'RGBA').transpose(Image.FLIP_LEFT_RIGHT)
    front = b
    side = b                                       # Boo kijkt al schuin; naar links = zoals de bron (spiegelen voor rechts)
    return [place(front, 1), place(back, 1), place(side, 1), place(front, 2), place(front, 0), place(back, 2),
            place(back, 0), place(side, 2), place(side, 0)]


# ---------------------------------------------------------------------------------------------- Wario
def wario():
    f = bbox(Image.open(os.path.join(GUEST, 'wario_bron.png')).convert('RGBA'))
    s = bbox(Image.open(os.path.join(GUEST, 'wario_side_bron.png')).convert('RGBA')).transpose(Image.FLIP_LEFT_RIGHT)
    a = np.array(f).astype(int)
    h, w = a.shape[:2]
    # achterkant: bovenste ~45% = pet (geel), daaronder de nek (huid) tot het tuinbroek begint
    back = a.copy()
    rgb = a[..., :3]
    cap = np.array([248, 216, 40]); hair = np.array([120, 72, 24]); dark = np.array([0, 0, 0])
    for y in range(h):
        for x in range(w):
            if a[y, x, 3] == 0:
                continue
            edge = any(not (0 <= y + dy < h and 0 <= x + dx < w) or a[y + dy, x + dx, 3] == 0
                       for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge:
                back[y, x, :3] = dark
            elif y < h * 0.30:
                back[y, x, :3] = cap
            elif y < h * 0.46 and abs(x - w / 2) < 8:
                back[y, x, :3] = hair
    back = Image.fromarray(back.astype(np.uint8), 'RGBA')

    def step(im, side_):
        """1 px omhoog, één voet blijft staan (zoals de Shy Guy)."""
        w_, h_ = im.size
        out = Image.new('RGBA', (w_, h_), (0, 0, 0, 0))
        out.alpha_composite(im.crop((0, 1, w_, h_)), (0, 0))
        for x in range(w_):
            if (x < w_ // 2) == (side_ == 0):
                for y in range(h_ - 3, h_):
                    out.putpixel((x, y), im.getpixel((x, y)))
        return out
    return sheet9(f, back, s, step(f, 0), step(f, 1), step(back, 0), step(back, 1), step(s, 0), step(s, 1))


# ---------------------------------------------------------------------------------------------- back pic
def yoshi_back():
    sh = Image.open(os.path.join(SRC, 'yoshi_rs_style.png')).convert('RGB')
    cell = np.array(sh.crop((1, 100, 65, 164))).astype(int)
    bgc = cell[0, 0].copy()
    alpha = np.where((np.abs(cell - bgc).sum(2) == 0), 0, 255)
    rgba = np.dstack([cell, alpha]).astype(np.uint8)
    im = Image.fromarray(rgba, 'RGBA')
    q, pal = quantize([im])
    pal[0] = tuple(int(v) for v in bgc)
    out = Image.new('P', (64, 256), 0)
    for k in range(4):
        out.paste(q, (0, 64 * k))
    out.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    out.save(os.path.join(ROOT, 'graphics/trainers/back_pics/yoshi.png'))
    return out



# ---------------------------------------------------------------------------------------------- Poochy, ?-wolk, Nep-Enut
POOCHY_SRC = os.path.join(SRC, 'poochy_sma3.png')
OBJ_SRC = os.path.join(SRC, 'sma3_objects.png')


def key_white(im, bg=(255, 255, 255)):
    a = np.array(im.convert('RGBA')).astype(int)
    m = (np.abs(a[..., :3] - np.array(bg)).sum(2) == 0)
    a[m, 3] = 0
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


def wide(im, dy=0, up=0):
    f = Image.new('RGBA', (64, 32), (0, 0, 0, 0))
    f.alpha_composite(im, ((64 - im.width) // 2, 32 - im.height - dy - up))
    return f


def poochy():
    """Poochy (SMA3-sheet van A.J. Nitro, origin/master graphics/): de sheet kijkt naar rechts -> gespiegeld (Gen 3
    opzij = links). Rij 2 = lopen, het losse vak rechtsboven = voor; achter = voor met het gezicht weggepoetst."""
    sh = Image.open(POOCHY_SRC).convert('RGB')

    def cut(box):
        return bbox(key_white(sh.crop(box)))
    walk = [cut(b).transpose(Image.FLIP_LEFT_RIGHT) for b in
            ((5, 40, 42, 64), (47, 39, 81, 64), (86, 40, 123, 64), (128, 40, 167, 64))]
    front = cut((177, 5, 205, 33))
    a = np.array(front).astype(int)
    h, w = a.shape[:2]
    back = a.copy()
    rgb = a[..., :3]
    body, dark, spot, light = (np.array(c) for c in ((248, 152, 32), (200, 96, 16), (216, 40, 24), (255, 216, 120)))
    for y in range(h):
        for x in range(w):
            if a[y, x, 3] == 0:
                continue
            edge = any(not (0 <= y + dy < h and 0 <= x + dx < w) or a[y + dy, x + dx, 3] == 0
                       for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge or y < 3 or y >= h - 6:          # omlijning, antenne en pootjes blijven
                continue
            back[y, x, :3] = light if y < 8 else (dark if y > h - 10 else body)
            if (x - w // 2) ** 2 + (y - 12) ** 2 <= 6 or (x - 6) ** 2 + (y - 16) ** 2 <= 3 \
                    or (x - w + 7) ** 2 + (y - 15) ** 2 <= 3:
                back[y, x, :3] = spot                # rode vlekken op de rug
    back = Image.fromarray(back.astype(np.uint8), 'RGBA')
    return [wide(front), wide(back), wide(walk[0]), wide(front, 1), wide(front, 1), wide(back, 1), wide(back, 1),
            wide(walk[1]), wide(walk[3])]


def qcloud():
    """Gevleugelde ?-wolk uit de SMA3-objectensheet; de vleugelstanden zijn de stapframes (WALK_IN_PLACE = fladderen)."""
    sh = Image.open(OBJ_SRC).convert('RGB')
    bg = sh.getpixel((65, 104))

    def cut(box):
        return bbox(key_white(sh.crop(box), bg))
    f = [cut(b) for b in ((71, 108, 101, 129), (106, 112, 142, 129), (147, 113, 189, 129), (194, 113, 228, 132),
                          (233, 113, 275, 129), (280, 112, 310, 129))]
    return [wide(f[0], 0, 6), wide(f[0], 0, 6), wide(f[0], 0, 6), wide(f[2], 1, 6), wide(f[3], 2, 6),
            wide(f[2], 1, 6), wide(f[3], 2, 6), wide(f[2], 1, 6), wide(f[3], 2, 6)]


def nep_enut(frames):
    """Nep-Enut: Yoshi, maar blauw (groen -> blauw, rood -> paars) met boze wenkbrauwen. Overduidelijk nep."""
    out = []
    for fr in frames:
        a = np.array(fr).astype(int)
        r, g, b = a[..., 0].copy(), a[..., 1].copy(), a[..., 2].copy()
        op = a[..., 3] > 0
        green = op & (g > r + 20) & (g > b + 10)
        red = op & (r > g + 60) & (r > b + 40)
        a[green, 0] = (r[green] * 0.35).astype(int)
        a[green, 1] = (g[green] * 0.55).astype(int)
        a[green, 2] = np.minimum(255, g[green] + 40)
        a[red, 0] = (r[red] * 0.55).astype(int)
        a[red, 1] = (g[red] * 0.4).astype(int)
        a[red, 2] = np.minimum(255, r[red])
        out.append(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA'))
    for k in (0, 3, 4):                      # boze wenkbrauwen boven het oogwit (vooraanzicht)
        a = np.array(out[k]).astype(int)
        ys, xs = np.where((a[..., 3] > 0) & (a[..., :3].sum(2) > 690) & (np.arange(32)[:, None] < 16))
        if len(ys):
            y0, xa, xb = ys.min(), xs.min(), xs.max()
            for x in range(xa, xb + 1):
                yy = y0 - 1 - int(abs(x - (xa + xb) / 2) > (xb - xa) / 4)
                if yy >= 0:
                    a[yy, x] = (24, 16, 48, 255)
        out[k] = Image.fromarray(a.astype(np.uint8), 'RGBA')
    return out


# ---------------------------------------------------------------------------------------------- registratie (idempotent)
OWS = [  # (constante, symboolnaam, bestand, paletlabel-tag, omschrijving)
    ('YOSHI', 'YoshiOw', 'yoshi_ow', 0x1170, "Yoshi (Yoshi's Island)"),
    ('COMMANDER_BOO', 'BooOw', 'boo_ow', 0x1171, "Commander Boo (Yoshi's Island)"),
    ('WARIO', 'WarioOw', 'wario_ow', 0x1172, "Wario (Yoshi's Island)"),
    ('POOCHY', 'PoochyOw', 'poochy_ow', 0x1173, "Poochy (Yoshi's Island)"),
    ('QCLOUD', 'QCloudOw', 'qcloud_ow', 0x1174, "gevleugelde ?-wolk (Yoshi's Island)"),
    ('NEP_ENUT', 'NepEnutOw', 'nep_enut_ow', 0x1175, "Nep-Enut, de nep-blauwe Yoshi (Yoshi's Island)"),
]
WIDE = {'POOCHY', 'QCLOUD'}          # 64x32 (Poochy en de vleugels zijn breder dan 32 px)
NOTE = 'Project Grounded: %s (tools/grounded/yoshi_sprites.py)'


def _edit(path, fn):
    p = os.path.join(ROOT, path)
    s = open(p).read()
    t = fn(s)
    if t != s:
        open(p, 'w').write(t)


def register():
    def consts(s):
        for k, (c, sym, f, tag, why) in enumerate(OWS):
            if 'OBJ_EVENT_GFX_%s ' % c not in s:
                n = int(re.search(r'#define NUM_OBJ_EVENT_GFX\s+(\d+)', s).group(1))
                line = '#define OBJ_EVENT_GFX_%-34s%d // %s\n' % (c, n, NOTE % why)
                s = re.sub(r'(\n)(\n#define NUM_OBJ_EVENT_GFX\s+)(\d+)', lambda m: '\n' + line + m.group(2) + str(n + 1), s, count=1)
            pt = 'OBJ_EVENT_PAL_TAG_%s' % c
            if pt + " " not in s:          # met spatie: POOCHY zit ook in POOCHYENA
                a = s.index('#define OBJ_EVENT_PAL_TAG_GEN1_GHOST')
                s = s[:a] + '#define %-42s0x%04X // %s\n' % (pt, tag, NOTE % why) + s[a:]
        return s
    _edit('include/constants/event_objects.h', consts)

    def gfx(s):
        for c, sym, f, tag, why in OWS:
            if 'gObjectEventPic_%s[]' % sym not in s:
                a = s.index('const u32 gObjectEventPic_Gen1Ghost[]')
                s = s[:a] + ('const u32 gObjectEventPic_%s[] = INCBIN_U32("graphics/object_events/pics/people/%s.4bpp"); // %s\n'
                             'const u16 gObjectEventPal_%s[] = INCBIN_U16("graphics/object_events/palettes/%s.gbapal");\n'
                             % (sym, f, NOTE % why, sym, f)) + s[a:]
        return s
    _edit('src/data/object_events/object_event_graphics.h', gfx)

    def pics(s):
        for c, sym, f, tag, why in OWS:
            if 'sPicTable_%s[]' % sym not in s:
                a = s.index('static const struct SpriteFrameImage sPicTable_Gen1Ghost[]')
                s = s[:a] + ('static const struct SpriteFrameImage sPicTable_%s[] = { // %s\n'
                             '    overworld_ascending_frames(gObjectEventPic_%s, %d, 4),\n};\n\n'
                             % (sym, NOTE % why, sym, 8 if c in WIDE else 4)) + s[a:]
        return s
    _edit('src/data/object_events/object_event_pic_tables.h', pics)

    def info(s):
        for c, sym, f, tag, why in OWS:
            if 'gObjectEventGraphicsInfo_%s =' % sym not in s:
                a = s.index('const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Gen1Ghost')
                wd = 64 if c in WIDE else 32
                s = s[:a] + ('// %s, %dx32\nconst struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_%s = {\n'
                             '    .tileTag = TAG_NONE,\n    .paletteTag = OBJ_EVENT_PAL_TAG_%s,\n'
                             '    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,\n    .size = %d,\n    .width = %d,\n'
                             '    .height = 32,\n    .paletteSlot = PALSLOT_NPC_SPECIAL,\n    .shadowSize = SHADOW_SIZE_%s,\n'
                             '    .inanimate = FALSE,\n    .compressed = FALSE,\n    .tracks = TRACKS_%s,\n'
                             '    .oam = &gObjectEventBaseOam_%dx32,\n    .subspriteTables = sOamTables_%dx32,\n'
                             '    .anims = sAnimTable_Standard,\n    .images = sPicTable_%s,\n'
                             '    .affineAnims = gDummySpriteAffineAnimTable,\n};\n\n'
                             % (NOTE % why, wd, sym, c, wd * 16, wd, 'L' if c == 'POOCHY' else 'M',
                                'NONE' if c in ('COMMANDER_BOO', 'QCLOUD') else 'FOOT', wd, wd, sym)) + s[a:]
        return s
    _edit('src/data/object_events/object_event_graphics_info.h', info)

    def ptrs(s):
        for c, sym, f, tag, why in OWS:
            if 'gObjectEventGraphicsInfo_%s;' % sym not in s:
                a = s.index('extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Gen1Ghost;')
                s = s[:a] + 'extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_%s;\n' % sym + s[a:]
            if '[OBJ_EVENT_GFX_%s]' % c not in s:
                a = s.index('    [OBJ_EVENT_GFX_GEN1_GHOST]')
                a = s.index('\n', a) + 1
                s = s[:a] + '    [OBJ_EVENT_GFX_%s] = &gObjectEventGraphicsInfo_%s, // %s\n' % (c, sym, NOTE % why) + s[a:]
        return s
    _edit('src/data/object_events/object_event_graphics_info_pointers.h', ptrs)

    def pals(s):
        for c, sym, f, tag, why in OWS:
            if 'gObjectEventPal_%s,' % sym not in s:
                a = s.index('    {gObjectEventPal_Gen1Ghost,')
                s = s[:a] + '    {gObjectEventPal_%-22s OBJ_EVENT_PAL_TAG_%s}, // %s\n' % (sym + ',', c, NOTE % why) + s[a:]
        return s
    _edit('src/event_object_movement.c', pals)

    def rules(s):
        for c, sym, f, tag, why in OWS:
            r = '$(OBJEVENTGFXDIR)/people/%s.4bpp: %%.4bpp: %%.png' % f
            if r not in s:
                wd = 8 if c in WIDE else 4
                s = s.rstrip('\n') + '\n\n# %s (%dx32)\n%s\n\t$(GFX) $< $@ -mwidth %d -mheight 4\n' % (
                    NOTE % why, wd * 8, r, wd)
        return s
    _edit('spritesheet_rules.mk', rules)

    # back pic van Yoshi (partner)
    def bconst(s):
        if 'TRAINER_BACK_PIC_YOSHI' not in s:
            a = s.index('#define TRAINER_BACK_PIC_CALYREX')
            a = s.index('\n', a) + 1
            n = int(re.search(r'#define TRAINER_BACK_PIC_CALYREX\s+(\d+)', s).group(1))
            s = s[:a] + '#define TRAINER_BACK_PIC_YOSHI                  %d // %s\n' % (
                n + 1, NOTE % "Yoshi als partner (Yoshi's Island)") + s[a:]
        return s
    _edit('include/constants/trainers.h', bconst)

    def bgfx(s):
        if 'gTrainerBackPic_Yoshi[]' not in s:
            a = s.index('const u16 gTrainerBackPicPalette_Calyrex[]')
            a = s.index('\n', a) + 1
            s = s[:a] + ('const u8 gTrainerBackPic_Yoshi[] = INCBIN_U8("graphics/trainers/back_pics/yoshi.4bpp"); // %s\n'
                         'const u16 gTrainerBackPicPalette_Yoshi[] = INCBIN_U16("graphics/trainers/back_pics/yoshi.gbapal");\n'
                         % (NOTE % 'Yoshi als partner')) + s[a:]
        if 'TRAINER_BACK_PIC_YOSHI,' not in s:
            a = s.index('    TRAINER_BACK_SPRITE(TRAINER_BACK_PIC_CALYREX')
            a = s.index('\n', a) + 1
            s = s[:a] + ('    TRAINER_BACK_SPRITE(TRAINER_BACK_PIC_YOSHI, 4, gTrainerBackPic_Yoshi, gTrainerBackPicPalette_Yoshi, '
                         'sBackAnims_Hoenn),\n') + s[a:]
        return s
    _edit('src/data/graphics/trainers.h', bgfx)


def main():
    prev = []
    yf = yoshi()
    for name, frames in (('yoshi_ow', yf), ('boo_ow', boo()), ('wario_ow', wario()), ('poochy_ow', poochy()),
                         ('qcloud_ow', qcloud()), ('nep_enut_ow', nep_enut(yf))):
        im, pal = quantize(frames)
        im.save(os.path.join(OW, name + '.png'))
        write_pal(os.path.join(PAL, name + '.pal'), pal)
        prev.append(im.convert('RGB'))
    bp = yoshi_back()
    register()
    if len(sys.argv) > 1:
        out = Image.new('RGB', (288 + 70, 32 * 3 + 0 if False else 100), (60, 60, 90))
        out = Image.new('RGB', (576 + 72, 32 * len(prev) + 4), (60, 60, 90))
        for i, p in enumerate(prev):
            out.paste(p, (0, 32 * i + 2))
        out.paste(bp.convert('RGB').crop((0, 0, 64, 64)), (292, 2))
        out.resize((out.width * 4, out.height * 4), Image.NEAREST).save(sys.argv[1])
    print('yoshi_sprites klaar')


if __name__ == '__main__':
    main()
