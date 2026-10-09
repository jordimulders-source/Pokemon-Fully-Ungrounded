#!/usr/bin/env python3
"""Project Grounded: oog in de muur van het Stakataka-doolhof (Ultra Space, OBJ_EVENT_GFX_ULTRA_EYE, 16x16, 9 frames).

Een amandelvormig oog met een cyaan iris (de kleur van Stakataka's ogen) in een stenen oogkas. De pupil kijkt per
frame een andere kant op (frame 0 zuid, 1 noord, 2 west; oost = west gespiegeld); src/ultra_worlds.c draait de ogen
elke frame naar de speler. Frames 3-8 (lopen) zijn kopieën.
Registreert zichzelf (event_objects.h, pics, info, pointers, palet, spritesheet_rules.mk); idempotent.
Gebruik: python3 tools/grounded/ultra_eye_sprite.py [voorbeeld.png]"""
import math, os, re, sys  # noqa: E401
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
os.chdir(ROOT)
GFX_ID = 350
PAL_TAG = '0x11B5'
PAL = [(115, 197, 164),                                   # 0 transparant
       (16, 16, 24), (40, 40, 52), (72, 72, 84), (112, 112, 124),       # 1-4 oogkas (steen, donker -> licht)
       (152, 40, 48), (208, 96, 96),                                    # 5-6 rood (adertjes, binnenooghoek)
       (184, 176, 160), (232, 224, 200), (248, 248, 232),               # 7-9 oogwit
       (16, 72, 104), (32, 152, 200), (120, 224, 248), (200, 248, 255),  # 10-13 iris cyaan
       (8, 8, 8)]                                                       # 14 pupil


def frame(px, py):
    """oog met de pupil verschoven over (px, py) pixels"""
    img = [[0] * 16 for _ in range(16)]
    cx, cy = 7.5, 7.5
    for y in range(16):
        for x in range(16):
            dx, dy = (x - cx) / 7.6, (y - cy) / 5.2
            # amandel: bovenkant boller dan onderkant
            e = dx * dx + (dy * (1.15 if dy < 0 else 0.95)) ** 2 + 0.25 * abs(dx) * abs(dy)
            if e > 1.28:
                continue
            if e > 0.92:                                   # oogkas/ooglid
                img[y][x] = 2 if y < cy else 3
                if e > 1.12:
                    img[y][x] = 1
                continue
            v = 8
            if y <= cy - 3:
                v = 7                                      # schaduw van het bovenooglid
            if y >= cy + 3:
                v = 9 if x > cx else 8
            img[y][x] = v
    # adertjes
    for (x, y) in ((2, 7), (3, 7), (3, 8), (13, 8), (12, 8), (12, 9), (2, 9)):
        if img[y][x] in (7, 8, 9):
            img[y][x] = 5
    # iris + pupil
    ix, iy = cx + px, cy + py
    for y in range(16):
        for x in range(16):
            if img[y][x] not in (7, 8, 9, 5):
                continue
            d = math.hypot(x - ix, (y - iy) * 1.05)
            if d < 1.6:
                img[y][x] = 14
            elif d < 2.3:
                img[y][x] = 10
            elif d < 3.6:
                ang = math.atan2(y - iy, x - ix)
                img[y][x] = 12 if ang > 0.4 else 11
            elif d < 4.1:
                img[y][x] = 10
    # glimlicht
    gx, gy = int(round(ix - 1)), int(round(iy - 2))
    if 0 <= gx < 16 and 0 <= gy < 16 and img[gy][gx] in (10, 11, 12, 14):
        img[gy][gx] = 13
    # bovenooglid valt een beetje over de iris (kijkt dreigend)
    for x in range(16):
        for y in range(16):
            if img[y][x] in (7, 8, 9, 10, 11, 12, 13, 14, 5):
                img[y][x] = 3 if img[y][x] not in (10, 11, 12, 13, 14) else 2
                break
    return img


def sheet():
    fr = [frame(0, 1.6), frame(0, -1.9), frame(-2.6, 0)]
    order = [0, 1, 2, 0, 0, 1, 1, 2, 2]
    im = Image.new('P', (16 * 9, 16), 0)
    p = im.load()
    for i, f in enumerate(order):
        for y in range(16):
            for x in range(16):
                p[i * 16 + x, y] = fr[f][y][x]
    flat = [v for c in PAL for v in c]
    im.putpalette(flat + [0] * (768 - len(flat)))
    return im


def patch(path, anchor, text, after=True):
    s = open(path).read()
    if text.strip().split('\n')[0] in s:
        return
    i = s.index(anchor)
    if after:
        i += len(anchor)
    s = s[:i] + text + s[i:]
    open(path, 'w').write(s)


def register():
    note = ' // Project Grounded: oog in het Stakataka-doolhof (Ultra Space, tools/grounded/ultra_eye_sprite.py)'
    p = 'include/constants/event_objects.h'
    s = open(p).read()
    if 'OBJ_EVENT_GFX_ULTRA_EYE' not in s:
        s = s.replace('\n#define NUM_OBJ_EVENT_GFX ', '\n#define OBJ_EVENT_GFX_ULTRA_EYE                         %d%s\n\n#define NUM_OBJ_EVENT_GFX ' % (GFX_ID, note), 1)
        n = int(re.search(r'#define NUM_OBJ_EVENT_GFX\s+(\d+)', s).group(1))
        if n <= GFX_ID:
            s = re.sub(r'(#define NUM_OBJ_EVENT_GFX\s+)\d+', r'\g<1>%d' % (GFX_ID + 1), s)
        s = s.replace('#define OBJ_EVENT_PAL_TAG_ULTRA_WORMHOLE ', '#define OBJ_EVENT_PAL_TAG_ULTRA_EYE               %s%s\n#define OBJ_EVENT_PAL_TAG_ULTRA_WORMHOLE ' % (PAL_TAG, note), 1)
        open(p, 'w').write(s)
    patch('src/data/object_events/object_event_graphics.h',
          '// Project Grounded: Ultra Wormhole (Ultra Space, tools/grounded/ultra_wormhole_sprite.py)\n',
          'const u32 gObjectEventPic_UltraEye[] = INCBIN_U32("graphics/object_events/pics/misc/ultra_eye.4bpp");%s\n'
          'const u16 gObjectEventPal_UltraEye[] = INCBIN_U16("graphics/object_events/palettes/ultra_eye.gbapal");%s\n' % (note, note))
    s = open('src/data/object_events/object_event_pic_tables.h').read()
    if 'sPicTable_UltraEye' not in s:
        s = s.rstrip('\n') + '\n\nstatic const struct SpriteFrameImage sPicTable_UltraEye[] = {%s\n    overworld_ascending_frames(gObjectEventPic_UltraEye, 2, 2),\n};\n' % note
        open('src/data/object_events/object_event_pic_tables.h', 'w').write(s)
    s = open('src/data/object_events/object_event_graphics_info.h').read()
    if 'gObjectEventGraphicsInfo_UltraEye' not in s:
        s = s.rstrip('\n') + '''

//%s
const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_UltraEye = {
    .tileTag = TAG_NONE,
    .paletteTag = OBJ_EVENT_PAL_TAG_ULTRA_EYE,
    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,
    .size = 128,
    .width = 16,
    .height = 16,
    .paletteSlot = PALSLOT_NPC_SPECIAL,
    .shadowSize = SHADOW_SIZE_S,
    .inanimate = FALSE,
    .compressed = FALSE,
    .tracks = TRACKS_NONE,
    .oam = &gObjectEventBaseOam_16x16,
    .subspriteTables = sOamTables_16x16,
    .anims = sAnimTable_Standard,
    .images = sPicTable_UltraEye,
    .affineAnims = gDummySpriteAffineAnimTable,
};
''' % note
        open('src/data/object_events/object_event_graphics_info.h', 'w').write(s)
    p = 'src/data/object_events/object_event_graphics_info_pointers.h'
    s = open(p).read()
    if 'gObjectEventGraphicsInfo_UltraEye' not in s:
        s = s.replace('extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_UltraWormhole;\n',
                      'extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_UltraWormhole;\n'
                      'extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_UltraEye;\n', 1)
        i = s.index('    [OBJ_EVENT_GFX_ULTRA_WORMHOLE]')
        j = s.index('\n', i) + 1
        s = s[:j] + '    [OBJ_EVENT_GFX_ULTRA_EYE] = &gObjectEventGraphicsInfo_UltraEye,%s\n' % note + s[j:]
        open(p, 'w').write(s)
    p = 'src/event_object_movement.c'
    s = open(p).read()
    if 'gObjectEventPal_UltraEye' not in s:
        i = s.index('    {gObjectEventPal_UltraWormhole,')
        j = s.index('\n', i) + 1
        s = s[:j] + '    {gObjectEventPal_UltraEye,              OBJ_EVENT_PAL_TAG_ULTRA_EYE},%s\n' % note + s[j:]
        open(p, 'w').write(s)
    p = 'spritesheet_rules.mk'
    s = open(p).read()
    if 'misc/ultra_eye.4bpp' not in s:
        s = s.rstrip('\n') + '\n\n# Project Grounded: oog in het Stakataka-doolhof (16x16, tools/grounded/ultra_eye_sprite.py)\n' \
            '$(OBJEVENTGFXDIR)/misc/ultra_eye.4bpp: %.4bpp: %.png\n\t$(GFX) $< $@ -mwidth 2 -mheight 2\n'
        open(p, 'w').write(s)


def main():
    im = sheet()
    im.save('graphics/object_events/pics/misc/ultra_eye.png')
    with open('graphics/object_events/palettes/ultra_eye.pal', 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in PAL + [(0, 0, 0)] * (16 - len(PAL)):
            f.write('%d %d %d\n' % c)
    register()
    if len(sys.argv) > 1:
        im.convert('RGB').resize((16 * 9 * 8, 128), Image.NEAREST).save(sys.argv[1])


if __name__ == '__main__':
    main()
