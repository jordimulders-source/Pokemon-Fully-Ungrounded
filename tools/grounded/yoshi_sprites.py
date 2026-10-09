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


# ---------------------------------------------------------------------------------------------- registratie (idempotent)
OWS = [  # (constante, symboolnaam, bestand, paletlabel-tag, omschrijving)
    ('YOSHI', 'YoshiOw', 'yoshi_ow', 0x1170, "Yoshi (Yoshi's Island)"),
    ('COMMANDER_BOO', 'BooOw', 'boo_ow', 0x1171, "Commander Boo (Yoshi's Island)"),
    ('WARIO', 'WarioOw', 'wario_ow', 0x1172, "Wario (Yoshi's Island)"),
]
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
            if pt not in s:
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
                             '    overworld_ascending_frames(gObjectEventPic_%s, 4, 4),\n};\n\n' % (sym, NOTE % why, sym)) + s[a:]
        return s
    _edit('src/data/object_events/object_event_pic_tables.h', pics)

    def info(s):
        for c, sym, f, tag, why in OWS:
            if 'gObjectEventGraphicsInfo_%s =' % sym not in s:
                a = s.index('const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Gen1Ghost')
                s = s[:a] + ('// %s, 32x32\nconst struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_%s = {\n'
                             '    .tileTag = TAG_NONE,\n    .paletteTag = OBJ_EVENT_PAL_TAG_%s,\n'
                             '    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,\n    .size = 512,\n    .width = 32,\n'
                             '    .height = 32,\n    .paletteSlot = PALSLOT_NPC_SPECIAL,\n    .shadowSize = SHADOW_SIZE_M,\n'
                             '    .inanimate = FALSE,\n    .compressed = FALSE,\n    .tracks = TRACKS_%s,\n'
                             '    .oam = &gObjectEventBaseOam_32x32,\n    .subspriteTables = sOamTables_32x32,\n'
                             '    .anims = sAnimTable_Standard,\n    .images = sPicTable_%s,\n'
                             '    .affineAnims = gDummySpriteAffineAnimTable,\n};\n\n'
                             % (NOTE % why, sym, c, 'NONE' if c == 'COMMANDER_BOO' else 'FOOT', sym)) + s[a:]
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
                s = s.rstrip('\n') + '\n\n# %s (32x32)\n%s\n\t$(GFX) $< $@ -mwidth 4 -mheight 4\n' % (NOTE % why, r)
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
    for name, frames in (('yoshi_ow', yoshi()), ('boo_ow', boo()), ('wario_ow', wario())):
        im, pal = quantize(frames)
        im.save(os.path.join(OW, name + '.png'))
        write_pal(os.path.join(PAL, name + '.pal'), pal)
        prev.append(im.convert('RGB'))
    bp = yoshi_back()
    register()
    if len(sys.argv) > 1:
        out = Image.new('RGB', (288 + 70, 32 * 3 + 0 if False else 100), (60, 60, 90))
        out = Image.new('RGB', (288 + 72, 100), (60, 60, 90))
        for i, p in enumerate(prev):
            out.paste(p, (0, 32 * i + 2))
        out.paste(bp.convert('RGB').crop((0, 0, 64, 64)), (292, 2))
        out.resize((out.width * 4, out.height * 4), Image.NEAREST).save(sys.argv[1])
    print('yoshi_sprites klaar')


if __name__ == '__main__':
    main()
