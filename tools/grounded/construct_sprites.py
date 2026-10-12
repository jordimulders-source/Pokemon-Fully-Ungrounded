"""Project Grounded: de constructen van Arceus (Hall of Origin; Jordi 9 okt).

De negen emissaries (TRAINER_HOO_*) zijn geen mensen meer maar stenen golems die ARCEUS aanstuurt: een lijf van
gebeiteld gesteente, een vizier en een kern van licht, en om het middel het gouden kruiswiel van Arceus. Eén ontwerp,
per emissary een paletwissel (steen, gloed, accent) passend bij zijn thema. Het goud blijft overal hetzelfde.

Maakt:  graphics/trainers/front_pics/construct.png (64x64) + construct_<thema>.pal (9x)
        graphics/object_events/pics/people/construct.png (9 frames 16x32) + palettes/construct_<thema>.pal (9x)
Registreert: TRAINER_PIC_CONSTRUCT_<THEMA>, trainerklasse TRAINER_CLASS_CONSTRUCT ("CONSTRUCT"),
             OBJ_EVENT_GFX_CONSTRUCT_<THEMA> + OBJ_EVENT_PAL_TAG_CONSTRUCT_<THEMA> (0x1180-0x1188).
Gebruik: python3 tools/grounded/construct_sprites.py [voorbeeld.png]"""
import os, re, sys
import numpy as np
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
FRONT = os.path.join(ROOT, 'graphics/trainers/front_pics')
OW = os.path.join(ROOT, 'graphics/object_events/pics/people')
OWPAL = os.path.join(ROOT, 'graphics/object_events/palettes')
NOTE = 'Project Grounded: construct van Arceus, %s (tools/grounded/construct_sprites.py)'

# kleurindex: 1 omlijning, 2-5 steen (donker -> licht), 6-8 goud, 9-11 gloed, 12-13 accent, 14 wit, 15 voegen
OUT, S1, S2, S3, S4, G1, G2, G3, L1, L2, L3, A1, A2, WH, SEAM = range(1, 16)
GOLD = [(152, 104, 32), (224, 176, 64), (248, 228, 136)]
# thema: (sleutel, trainer, omschrijving, steen x4, gloed x3, accent x2)
THEMES = [
    ('SKY', 'STRATOS', 'lucht', [(92, 108, 140), (136, 156, 188), (180, 200, 226), (226, 236, 248)],
     [(56, 152, 200), (112, 208, 240), (216, 248, 255)], [(72, 136, 104), (128, 200, 152)]),
    ('SEA', 'THALASSA', 'zee', [(36, 64, 116), (60, 104, 164), (100, 148, 204), (164, 198, 238)],
     [(32, 136, 156), (72, 204, 208), (184, 248, 240)], [(168, 48, 64), (232, 104, 112)]),
    ('LAND', 'BEDROCK', 'land', [(100, 62, 38), (148, 102, 62), (190, 146, 94), (228, 196, 148)],
     [(184, 48, 24), (240, 112, 40), (255, 212, 112)], [(72, 96, 56), (124, 156, 88)]),
    ('MIND', 'NOUS', 'geest', [(104, 84, 132), (152, 124, 180), (196, 172, 222), (236, 224, 248)],
     [(184, 48, 120), (240, 104, 176), (255, 204, 232)], [(48, 96, 168), (100, 156, 220)]),
    ('DREAM', 'SOMNIA', 'dromen', [(38, 36, 70), (62, 62, 108), (100, 100, 156), (148, 148, 200)],
     [(196, 156, 52), (240, 216, 112), (255, 248, 204)], [(152, 36, 60), (216, 88, 104)]),
    ('JUSTICE', 'GLADIUS', 'rechtvaardigheid', [(84, 92, 102), (132, 140, 150), (182, 190, 200), (228, 232, 238)],
     [(36, 136, 72), (88, 204, 120), (204, 250, 204)], [(48, 88, 168), (100, 148, 220)]),
    ('FORGE', 'HEPHAEST', 'smidse', [(46, 38, 38), (78, 66, 62), (120, 104, 96), (168, 148, 136)],
     [(200, 68, 16), (248, 144, 40), (255, 232, 136)], [(100, 100, 110), (152, 152, 162)]),
    ('ORDER', 'ORDO', "de zes Regi's", [(140, 108, 70), (182, 150, 102), (214, 190, 142), (240, 228, 192)],
     [(176, 40, 40), (232, 76, 56), (255, 180, 124)], [(84, 132, 176), (144, 192, 226)]),
    ('SPACETIME', 'KAIROS', 'tijd en ruimte', [(60, 70, 120), (94, 110, 168), (142, 158, 208), (200, 212, 242)],
     [(200, 72, 128), (240, 128, 176), (255, 216, 234)], [(52, 116, 176), (108, 182, 220)]),
]
PAL_TAG0 = 0x1180


def palette(theme):
    _, _, _, stone, glow, acc = theme
    out = [(255, 0, 255), (32, 30, 44)] + stone + GOLD + glow + acc + [(248, 248, 248)]
    out.append(tuple(int(c * 0.55) for c in stone[0]))
    assert len(out) == 16
    return out


def write_pal(path, cols):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % tuple(c) for c in cols))


# ---------------------------------------------------------------------------- tekenhulpjes
def ell(img, cx, cy, rx, ry, fn, half=None):
    h, w = img.shape
    for y in range(h):
        for x in range(w):
            dx, dy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            if dx * dx + dy * dy <= 1.0:
                if half == 'back' and dy > 0:
                    continue
                if half == 'front' and dy <= 0:
                    continue
                c = fn(dx, dy, x, y)
                if c:
                    img[y, x] = c


def box(img, x0, y0, x1, y1, fn):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if 0 <= y < img.shape[0] and 0 <= x < img.shape[1]:
                c = fn((x - x0) / max(1, x1 - x0), (y - y0) / max(1, y1 - y0), x, y)
                if c:
                    img[y, x] = c


def stone(u, v):
    """Licht van linksboven: u, v in 0..1 over het vlak."""
    t = 0.65 * u + 0.35 * v
    return S4 if t < 0.18 else S3 if t < 0.48 else S2 if t < 0.8 else S1


def outline(img):
    out = img.copy()
    h, w = img.shape
    for y in range(h):
        for x in range(w):
            if img[y, x]:
                continue
            if any(0 <= y + dy < h and 0 <= x + dx < w and img[y + dy, x + dx] for dx, dy in
                   ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y, x] = OUT
    return out


def ring(img, cx, cy, rx, ry, half, thick=2.2, gems=True):
    """Het gouden kruiswiel van Arceus (ellips), achterste of voorste helft, met vier juwelen."""
    h, w = img.shape
    for y in range(h):
        for x in range(w):
            dx, dy = (x + 0.5 - cx), (y + 0.5 - cy)
            r = (dx * dx / (rx * rx) + dy * dy / (ry * ry)) ** 0.5
            inner = 1 - thick / ry
            if inner <= r <= 1.0:
                if (half == 'back') != (dy < 0):
                    continue
                k = (r - inner) / (1 - inner)
                img[y, x] = G3 if k < 0.3 else G2 if k < 0.75 else G1
    for jx, jy in ((cx - rx + 1, cy), (cx + rx - 2, cy), (cx - 0.5, cy + ry - 1.5)):
        if half == 'front' and gems:
            ell(img, jx, jy, 2.2, 2.0, lambda dx, dy, x, y: L3 if dx + dy < -0.6 else L2 if dx + dy < 0.4 else L1)


# ---------------------------------------------------------------------------- trainerfoto 64x64
def front():
    img = np.zeros((64, 64), np.uint8)
    ring(img, 32, 39, 29, 9, 'back', 3)
    # gloed onder de voeten (zweeft net)
    ell(img, 32, 61.5, 15, 2.2, lambda dx, dy, x, y: L2 if abs(dx) < 0.5 else L1)
    # benen (zuilen) en voeten
    for lx in (22, 34):
        box(img, lx, 44, lx + 7, 55, lambda u, v, x, y: stone(u, v * 0.4))
        box(img, lx - 1, 55, lx + 8, 59, lambda u, v, x, y: stone(u, 0.3 + v * 0.5) if v > 0 else S4)
        for y in range(46, 54, 3):
            img[y, lx + 2] = SEAM
    # romp (trapezium, smaller naar onder)
    for y in range(19, 46):
        t = (y - 19) / 26.0
        x0, x1 = int(15 + 7 * t), int(48 - 7 * t)
        for x in range(x0, x1 + 1):
            img[y, x] = stone((x - x0) / max(1, x1 - x0), t)
    # accentplaten (borst) en gordel
    box(img, 20, 19, 43, 22, lambda u, v, x, y: A2 if v < 0.4 else A1)        # kraag
    for x in range(21, 43, 4):
        img[22, x] = SEAM
    for (x0, x1) in ((18, 22), (41, 45)):                                    # accentstrepen op de flanken
        for y in range(25, 38):
            for x in range(x0, x1):
                if (x - x0) == 1 or (x - x0) == 2:
                    img[y, x] = A2 if x - x0 == 1 else A1
    box(img, 21, 40, 42, 44, lambda u, v, x, y: A1 if v > 0.5 else A2)
    # kern van licht (ruit) midden op de borst
    for y in range(26, 37):
        half = 5 - abs(y - 31) * 1.0
        for x in range(32 - 6, 32 + 6):
            d = abs(x + 0.5 - 32)
            if d <= half:
                img[y, x] = L3 if d < half - 3 else L2 if d < half - 1.2 else L1
    img[29, 31] = WH
    # voegen / scheuren in de romp
    for (x, y) in ((19, 33), (20, 34), (20, 35), (21, 36), (44, 30), (43, 31), (43, 32), (27, 38), (36, 37)):
        img[y, x] = SEAM
    # schouders
    for cx in (14, 49):
        ell(img, cx, 23, 8, 6.5, lambda dx, dy, x, y: S4 if dy < -0.5 and dx < 0.2 else S3 if dy < 0.1 else S2)
        ell(img, cx, 21, 4.5, 2.2, lambda dx, dy, x, y: G3 if dx < 0 else G2)
    # armen + vuisten
    for ax, sgn in ((8, -1), (49, 1)):
        box(img, ax, 27, ax + 6, 42, lambda u, v, x, y: stone(u, 0.2 + v * 0.5))
        for y in (31, 32, 36, 37):
            for x in range(ax, ax + 7):
                img[y, x] = L2 if y in (31, 36) else L1
        ell(img, ax + 3.5, 46, 5, 4.5, lambda dx, dy, x, y: S4 if dx + dy < -0.7 else S3 if dx + dy < 0.3 else S2)
    # hoofd: blok met kam (zoals de kop van Arceus) en vizier
    box(img, 24, 8, 39, 20, lambda u, v, x, y: stone(u, v))
    for y in range(1, 9):                                         # kam
        half = (y - 1) * 0.55
        for x in range(32 - 6, 32 + 6):
            d = x + 0.5 - 32
            if abs(d) <= half:
                img[y, x] = G3 if d < -half * 0.3 else G2 if d < half * 0.4 else G1
    for x in range(26, 38):                                       # vizier
        img[13, x] = L2
        img[14, x] = L1 if x in (26, 37) else L3
    img[14, 29] = img[14, 34] = WH
    box(img, 24, 18, 39, 20, lambda u, v, x, y: S1 if v > 0.5 else S2)
    for x in range(24, 40, 3):
        img[19, x] = SEAM
    # voorste helft van het wiel over het lijf
    ring(img, 32, 39, 29, 9, 'front', 3)
    img = outline(img)
    return img


# ---------------------------------------------------------------------------- overworld 16x32 (9 frames)
def ow_frame(facing, step):
    """facing: down/up/left; step: 0 staan, 1/2 lopen (benen verspringen)."""
    img = np.zeros((32, 16), np.uint8)
    side = facing == 'left'
    # ring achter
    if not side:
        ring(img, 8, 19, 7.6, 2.4, 'back', 1.3, False)
    # benen
    legs = ((4, 7), (9, 12)) if not side else ((5, 8), (8, 11))
    for i, (x0, x1) in enumerate(legs):
        dy = (-1 if (step == 1 and i == 0) or (step == 2 and i == 1) else 0)
        box(img, x0, 22 + dy, x1, 28 + dy, lambda u, v, x, y: stone(u, 0.3))
        box(img, x0, 28 + dy, x1, 29 + dy, lambda u, v, x, y: S1)
    # romp
    for y in range(11, 23):
        t = (y - 11) / 11.0
        if side:
            x0, x1 = 4, 11
        else:
            x0, x1 = int(2 + 2 * t), int(13 - 2 * t)
        for x in range(x0, x1 + 1):
            img[y, x] = stone((x - x0) / max(1, x1 - x0), t)
    if facing == 'down':
        img[14, 7] = img[14, 8] = L3
        img[15, 7] = img[15, 8] = L2
        img[13, 7] = img[13, 8] = L1
        img[13, 4] = img[13, 11] = A2
        img[14, 4] = img[14, 11] = A1
    elif facing == 'up':
        for y in range(13, 19):
            img[y, 7] = img[y, 8] = A1
    else:
        img[14, 5] = L2
        img[15, 5] = L1
    # armen
    if side:
        swing = (0, 1, -1)[step]
        box(img, 7, 12 + swing, 9, 19 + swing, lambda u, v, x, y: stone(u, 0.5))
        img[16 + swing, 7] = img[16 + swing, 8] = L2
    else:
        for ax in (0, 14):
            swing = (0, 1, -1)[step] * (1 if ax == 0 else -1)
            box(img, ax, 12 + swing, ax + 1, 19 + swing, lambda u, v, x, y: stone(u, 0.4))
            img[15 + swing, ax] = img[15 + swing, ax + 1] = L2
    # hoofd + kam
    hx0, hx1 = (4, 11) if not side else (3, 10)
    box(img, hx0, 4, hx1, 10, lambda u, v, x, y: stone(u, v))
    for y in range(1, 4):
        cx = 7.5 if not side else 6.5
        for x in range(16):
            if abs(x + 0.5 - cx - 0.5) <= (y - 0.5) * 0.7:
                img[y, x] = G3 if x < cx else G2
    if facing == 'down':
        for x in range(hx0 + 1, hx1):
            img[7, x] = L3
        img[7, hx0 + 1] = img[7, hx1 - 1] = L1
    elif facing == 'left':
        for x in range(hx0, hx0 + 4):
            img[7, x] = L3
        img[7, hx0 + 3] = L1
    else:
        for x in range(hx0 + 1, hx1):
            img[8, x] = S1
    # ring voor
    if side:
        ring(img, 8, 19, 5.5, 2.2, 'front', 1.3, False)
        ring(img, 8, 19, 5.5, 2.2, 'back', 1.3, False)
    else:
        ring(img, 8, 19, 7.6, 2.4, 'front', 1.3, False)
    img = outline(img)
    return img


def ow_sheet():
    frames = [ow_frame('down', 0), ow_frame('up', 0), ow_frame('left', 0),
              ow_frame('down', 1), ow_frame('down', 2), ow_frame('up', 1), ow_frame('up', 2),
              ow_frame('left', 1), ow_frame('left', 2)]
    return np.concatenate(frames, axis=1)


def save_png(arr, path, pal):
    im = Image.fromarray(arr.astype(np.uint8), 'P')
    flat = []
    for c in pal:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.save(path)


# ---------------------------------------------------------------------------- registratie
def _edit(path, fn):
    p = os.path.join(ROOT, path)
    s = open(p).read()
    t = fn(s)
    if t != s:
        open(p, 'w').write(t)


def sym(key):
    return 'Construct' + key.title().replace('time', 'Time')


def register():
    def tconst(s):
        for key, *_ in THEMES:
            c = 'TRAINER_PIC_CONSTRUCT_' + key
            if c + ' ' not in s:
                m = re.search(r'#define TRAINER_PIC_COUNT\s+(\d+)', s)
                n = int(m.group(1))
                s = s.replace(m.group(0), '#define %-33s %d // %s\n#define TRAINER_PIC_COUNT                 %d'
                              % (c, n, NOTE % key.lower(), n + 1), 1)
        if 'TRAINER_CLASS_CONSTRUCT,' not in s:
            s = s.replace('    TRAINER_CLASS_COUNT,', '    TRAINER_CLASS_CONSTRUCT, // %s\n    TRAINER_CLASS_COUNT,'
                          % (NOTE % 'Hall of Origin'), 1)
        return s
    _edit('include/constants/trainers.h', tconst)

    def tgfx(s):
        if 'gTrainerFrontPic_Construct[]' not in s:
            a = 'const u16 gTrainerPalette_ZeroAlarm[] = INCBIN_U16("graphics/trainers/front_pics/zero_alarm.gbapal");\n'
            assert a in s
            add = 'const u32 gTrainerFrontPic_Construct[] = INCBIN_U32("graphics/trainers/front_pics/construct.4bpp.smol"); // %s\n' % (NOTE % 'alle thema\'s')
            for key, *_ in THEMES:
                add += 'const u16 gTrainerPalette_%s[] = INCBIN_U16("graphics/trainers/front_pics/construct_%s.gbapal");\n' % (sym(key), key.lower())
            s = s.replace(a, a + add, 1)
        b = '    TRAINER_SPRITE(TRAINER_PIC_ZERO_ALARM, gTrainerFrontPic_ZeroAlarm, gTrainerPalette_ZeroAlarm),\n'
        for key, *_ in reversed(THEMES):
            line = '    TRAINER_SPRITE(TRAINER_PIC_CONSTRUCT_%s, gTrainerFrontPic_Construct, gTrainerPalette_%s),\n' % (key, sym(key))
            if line not in s:
                assert b in s
                s = s.replace(b, b + line, 1)
        return s
    _edit('src/data/graphics/trainers.h', tgfx)

    def bmain(s):
        a = '    [TRAINER_CLASS_ZERO_LAB] = { _("ZERO LAB"), 0, BALL_MASTER }, // Project Grounded: Area Zero\n'
        if 'TRAINER_CLASS_CONSTRUCT]' not in s:
            assert a in s
            s = s.replace(a, a + '    [TRAINER_CLASS_CONSTRUCT] = { _("CONSTRUCT"), 40, BALL_CHERISH }, // %s\n'
                          % (NOTE % 'Hall of Origin'), 1)
        return s
    _edit('src/battle_main.c', bmain)

    def consts(s):
        for k, (key, *_r) in enumerate(THEMES):
            c = 'CONSTRUCT_' + key
            if 'OBJ_EVENT_GFX_%s ' % c not in s:
                n = int(re.search(r'#define NUM_OBJ_EVENT_GFX\s+(\d+)', s).group(1))
                line = '#define OBJ_EVENT_GFX_%-34s%d // %s\n' % (c, n, NOTE % key.lower())
                s = re.sub(r'(\n)(\n#define NUM_OBJ_EVENT_GFX\s+)(\d+)', lambda m: '\n' + line + m.group(2) + str(n + 1),
                           s, count=1)
            pt = 'OBJ_EVENT_PAL_TAG_' + c
            if pt + ' ' not in s:
                a = s.index('#define OBJ_EVENT_PAL_TAG_GEN1_GHOST')
                s = s[:a] + '#define %-42s0x%04X // %s\n' % (pt, PAL_TAG0 + k, NOTE % key.lower()) + s[a:]
        return s
    _edit('include/constants/event_objects.h', consts)

    def gfx(s):
        if 'gObjectEventPic_Construct[]' not in s:
            a = s.index('const u32 gObjectEventPic_Gen1Ghost[]')
            add = 'const u32 gObjectEventPic_Construct[] = INCBIN_U32("graphics/object_events/pics/people/construct.4bpp"); // %s\n' % (NOTE % 'alle thema\'s')
            for key, *_ in THEMES:
                add += 'const u16 gObjectEventPal_%s[] = INCBIN_U16("graphics/object_events/palettes/construct_%s.gbapal");\n' % (sym(key), key.lower())
            s = s[:a] + add + s[a:]
        return s
    _edit('src/data/object_events/object_event_graphics.h', gfx)

    def pics(s):
        if 'sPicTable_Construct[]' not in s:
            a = s.index('static const struct SpriteFrameImage sPicTable_Gen1Ghost[]')
            s = s[:a] + ('static const struct SpriteFrameImage sPicTable_Construct[] = { // %s\n'
                         '    overworld_ascending_frames(gObjectEventPic_Construct, 2, 4),\n};\n\n' % (NOTE % 'alle thema\'s')) + s[a:]
        return s
    _edit('src/data/object_events/object_event_pic_tables.h', pics)

    def info(s):
        for key, *_ in THEMES:
            if 'gObjectEventGraphicsInfo_%s =' % sym(key) not in s:
                a = s.index('const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Gen1Ghost')
                s = s[:a] + ('// %s, 16x32\nconst struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_%s = {\n'
                             '    .tileTag = TAG_NONE,\n    .paletteTag = OBJ_EVENT_PAL_TAG_CONSTRUCT_%s,\n'
                             '    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,\n    .size = 256,\n    .width = 16,\n'
                             '    .height = 32,\n    .paletteSlot = PALSLOT_NPC_SPECIAL,\n    .shadowSize = SHADOW_SIZE_M,\n'
                             '    .inanimate = FALSE,\n    .compressed = FALSE,\n    .tracks = TRACKS_FOOT,\n'
                             '    .oam = &gObjectEventBaseOam_16x32,\n    .subspriteTables = sOamTables_16x32,\n'
                             '    .anims = sAnimTable_Standard,\n    .images = sPicTable_Construct,\n'
                             '    .affineAnims = gDummySpriteAffineAnimTable,\n};\n\n' % (NOTE % key.lower(), sym(key), key)) + s[a:]
        return s
    _edit('src/data/object_events/object_event_graphics_info.h', info)

    def ptrs(s):
        for key, *_ in THEMES:
            if 'gObjectEventGraphicsInfo_%s;' % sym(key) not in s:
                a = s.index('extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Gen1Ghost;')
                s = s[:a] + 'extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_%s;\n' % sym(key) + s[a:]
            if '[OBJ_EVENT_GFX_CONSTRUCT_%s]' % key not in s:
                a = s.index('    [OBJ_EVENT_GFX_GEN1_GHOST]')
                a = s.index('\n', a) + 1
                s = s[:a] + '    [OBJ_EVENT_GFX_CONSTRUCT_%s] = &gObjectEventGraphicsInfo_%s, // %s\n' % (
                    key, sym(key), NOTE % key.lower()) + s[a:]
        return s
    _edit('src/data/object_events/object_event_graphics_info_pointers.h', ptrs)

    def pals(s):
        for key, *_ in THEMES:
            if 'gObjectEventPal_%s,' % sym(key) not in s:
                a = s.index('    {gObjectEventPal_Gen1Ghost,')
                s = s[:a] + '    {gObjectEventPal_%-22s OBJ_EVENT_PAL_TAG_CONSTRUCT_%s}, // %s\n' % (
                    sym(key) + ',', key, NOTE % key.lower()) + s[a:]
        return s
    _edit('src/event_object_movement.c', pals)

    def rules(s):
        r = '$(OBJEVENTGFXDIR)/people/construct.4bpp: %.4bpp: %.png'
        if r not in s:
            s = s.rstrip('\n') + '\n\n# %s (16x32)\n%s\n\t$(GFX) $< $@ -mwidth 2 -mheight 4\n' % (NOTE % 'alle thema\'s', r)
        return s
    _edit('spritesheet_rules.mk', rules)


def main():
    fr = front()
    ow = ow_sheet()
    pals = [palette(t) for t in THEMES]
    save_png(fr, os.path.join(FRONT, 'construct.png'), pals[0])
    save_png(ow, os.path.join(OW, 'construct.png'), pals[0])
    for t, p in zip(THEMES, pals):
        write_pal(os.path.join(FRONT, 'construct_%s.pal' % t[0].lower()), p)
        write_pal(os.path.join(OWPAL, 'construct_%s.pal' % t[0].lower()), p)
    register()
    if len(sys.argv) > 1:                                         # alle negen paletten naast elkaar, 4x
        W = 9 * 68 + 4
        out = Image.new('RGB', (W, 64 + 32 * 1 + 16), (70, 76, 96))
        for i, p in enumerate(pals):
            def rgb(a):
                return Image.fromarray(np.array([[p[v] if v else (70, 76, 96) for v in row] for row in a], np.uint8))
            out.paste(rgb(fr), (4 + i * 68, 4))
            out.paste(rgb(ow[:, :48]), (4 + i * 68 + 8, 72))
        out.resize((out.width * 4, out.height * 4), Image.NEAREST).save(sys.argv[1])
    print('construct_sprites klaar')


if __name__ == '__main__':
    main()
