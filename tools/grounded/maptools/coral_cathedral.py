"""Project Grounded: Koraalkathedraal (Route 126) + Sea Shard-verzamelquest. Deterministisch en idempotent.

  Route126_CoralCathedral   Duikgrot onder Route 126: kopie van ShoalCave_HighTideEntranceRoom (hoge zaal met een
                            meer, terrassen en een ondiepe lagune; uitgangen dicht) met koraalbomen (Ekat's Coral Tiles,
                            rood + paars, achteraan de Cave-tileset op palet 12). Ingang: zwemgat in Underwater_Route126
                            (64,18); je komt surfend boven in het diepe water; terug = duiken.
                            Twee trainers, items, een Sea Shard, wilde Pokemon (land/surfen/vissen).
  Sea Shards                Key Item ITEM_SEA_SHARD (slot van de Fame Checker). Acht stuks, een per duikplek (SHARDS).
                            De Diving Treasure Hunter (Route 124) neemt ze in en geeft beloningen bij 2/4/6/8 gevonden.
                            Het aantal = het aantal gezette vondst-flags (geen var nodig).

Let op: de shards in kaarten van andere generatoren (dungeon_extra.py, sootopolis_craters.py, ...) worden hier in hun
map.json gezet; draai dit script opnieuw nadat je zo'n generator opnieuw draait.
Flags: FLAG_GROUNDED 660-699. Trainers: 1080-1081.
Gebruik: python3 tools/grounded/maptools/coral_cathedral.py [rendermap]"""
import json, os, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beacon_dragon as bd          # zet ook de werkmap op de repo-root
from PIL import Image

sms, cx, oq = bd.sms, bd.cx, bd.oq
Scr, ball, sign, hidden, warp, obj, tr, mon = bd.Scr, bd.ball, bd.sign, bd.hidden, bd.warp, bd.obj, bd.tr, bd.mon
reach, next_to = cx.reach, cx.next_to

NAME, CONST = 'Route126_CoralCathedral', 'ROUTE126_CORAL_CATHEDRAL'
COL = 0x400

# ====================================================================== flags
SHARDS = [  # (flag, kaart, doelplek (x, y), soort) -- de plek wordt de dichtstbijzijnde vrije, bereikbare cel
    (665, 'Route128_BubbleGrotto', (16, 6), 'ball'),
    (666, 'Underwater_Route127_Trench', (12, 40), 'hidden'),
    (667, 'ShipwreckShoals', (20, 24), 'ball'),
    (668, 'Underwater_SeaTemple', (11, 8), 'hidden'),
    (669, 'Route126_SilentCrater', (12, 12), 'ball'),
    (670, 'Route127_WellspringGrotto', (16, 7), 'ball'),
    (671, 'Underwater_Route136', (11, 20), 'hidden'),
]
SHARD_FLAG = lambda m: 'FLAG_ITEM_SEA_SHARD_' + re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', m).upper()
FLAGS = [
    (660, SHARD_FLAG(NAME), 'Koraalkathedraal: Sea Shard'),
    (661, 'FLAG_ITEM_CORAL_CATHEDRAL_LUMINOUS_MOSS', 'Koraalkathedraal: Luminous Moss'),
    (662, 'FLAG_ITEM_CORAL_CATHEDRAL_SHELL_BELL', 'Koraalkathedraal: Shell Bell'),
    (663, 'FLAG_ITEM_CORAL_CATHEDRAL_PEARL_STRING', 'Koraalkathedraal: Pearl String'),
    (664, 'FLAG_HIDDEN_ITEM_CORAL_CATHEDRAL_BIG_PEARL', 'Koraalkathedraal: verborgen Big Pearl'),
] + [(n, SHARD_FLAG(m), 'Sea Shard in ' + m) for n, m, _, _ in SHARDS] + [
    (680, 'FLAG_SEA_SHARD_REWARD_2', 'Sea Shards: beloning 2 (Dive Balls)'),
    (681, 'FLAG_SEA_SHARD_REWARD_4', 'Sea Shards: beloning 4 (Heavy-Duty Boots)'),
    (682, 'FLAG_SEA_SHARD_REWARD_6', 'Sea Shards: beloning 6 (Gold Bottle Cap)'),
    (683, 'FLAG_SEA_SHARD_REWARD_8', 'Sea Shards: beloning 8 (Master Ball)'),
    (684, 'FLAG_SEA_SHARDS_EXPLAINED', 'Sea Shards: Treasure Hunter heeft de quest uitgelegd'),
]
ALL_SHARD_FLAGS = [SHARD_FLAG(NAME)] + [SHARD_FLAG(m) for _, m, _, _ in SHARDS]
REWARDS = [(2, 'ITEM_DIVE_BALL', 10), (4, 'ITEM_HEAVY_DUTY_BOOTS', 1), (6, 'ITEM_GOLD_BOTTLE_CAP', 1),
           (8, 'ITEM_MASTER_BALL', 1)]


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// coral_cathedral { (tools/grounded/maptools/coral_cathedral.py; FLAG_GROUNDED 660-699, 685-699 nog vrij)\n'
    for n, name, why in FLAGS:
        assert 660 <= n <= 699
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// coral_cathedral {' in s:
        i = s.index('// coral_cathedral {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('// mega_forest {')
        s = s[:anchor] + blk + '\n' + s[anchor:]
    s = s.replace('620-659 Mega Forest (mega_forest.py), 660+ vrij.',
                  '620-659 Mega Forest (mega_forest.py), 660-699 Koraalkathedraal + Sea Shards (coral_cathedral.py), 700+ vrij.')
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)


# ====================================================================== koraal in de Cave-tileset
EKAT = os.environ.get('EKAT_CORAL', '')          # pad naar "Coral Tiles.png" (Ekat's Public Tiles); alleen nodig om
CORAL_PNG = 'graphics/grounded/tilesets/ekat/coral_trees.png'   # de uitsnede opnieuw te maken
CROPS = {'red': (160, 176, 2, 5), 'purple': (192, 288, 2, 4)}   # (x, y, breedte, hoogte in metatiles) in de bronsheet
CAVE = 'data/tilesets/secondary/cave/'
BASE_TILES, BASE_METATILES = 449, 426           # Cave-tileset vóór dit script
PAL = 12                                         # vrij palet in de Cave-tileset
BASES = {'shallow': 0x19e, 'water': 0x170}
MB_NORMAL, LAYER_COVERED = 0, 1


def coral_sheet():
    """Uitsnede (alleen de gebruikte koralen) naast elkaar in graphics/grounded/tilesets/ekat/."""
    if EKAT:
        src = Image.open(EKAT).convert('RGBA')
        W = sum(16 * w for _, _, w, _ in CROPS.values()); H = max(16 * h for *_, h in CROPS.values())
        out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x0 = 0
        for k, (x, y, w, h) in CROPS.items():
            out.paste(src.crop((x, y, x + 16 * w, y + 16 * h)), (x0, 0)); x0 += 16 * w
        os.makedirs(os.path.dirname(CORAL_PNG), exist_ok=True)
        out.save(CORAL_PNG)
    im = Image.open(CORAL_PNG).convert('RGBA')
    res, x0 = {}, 0
    for k, (_, _, w, h) in CROPS.items():
        res[k] = (im.crop((x0, 0, x0 + 16 * w, 16 * h)), w, h); x0 += 16 * w
    return res


def coral_tileset():
    sheets = coral_sheet()
    cols = sorted({im.getpixel((x, y))[:3] for im, _, _ in sheets.values() for y in range(im.height) for x in range(im.width) if im.getpixel((x, y))[3] >= 128})
    assert len(cols) <= 15, len(cols)
    cidx = {c: i + 1 for i, c in enumerate(cols)}
    # palet 12
    pal = [(0, 0, 0)] + [tuple(v & 0xf8 for v in c) for c in cols]
    pal += [(0, 0, 0)] * (16 - len(pal))
    open(CAVE + 'palettes/%02d.pal' % PAL, 'w').write(
        'JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in pal))

    # tiles: eerst terug naar de basis, dan de koraaltegels erachter (ontdubbeld, ook gespiegeld)
    tim = Image.open(CAVE + 'tiles.png')
    assert tim.mode == 'P' and tim.width == 128
    tpx = tim.load()
    old = [[[tpx[(i % 16) * 8 + x, (i // 16) * 8 + y] for x in range(8)] for y in range(8)] for i in range(BASE_TILES)]
    new, seen = [], {}

    def tile_id(t):
        variants = [(t, 0, 0), ([r[::-1] for r in t], 1, 0), (t[::-1], 0, 1), ([r[::-1] for r in t[::-1]], 1, 1)]
        for v, hf, vf in variants:
            k = repr(v)
            if k in seen:
                return seen[k], hf, vf
        seen[repr(t)] = BASE_TILES + len(new); new.append(t)
        return seen[repr(t)], 0, 0

    cells = {}                                   # (koraal, cx, cy) -> 4 tile-entries of None (leeg)
    for k, (im, w, h) in sheets.items():
        px = im.load()
        for cy in range(h):
            for cxx in range(w):
                ents, empty = [], True
                for sy in range(2):
                    for sx in range(2):
                        t = [[cidx[px[cxx * 16 + sx * 8 + x, cy * 16 + sy * 8 + y][:3]]
                              if px[cxx * 16 + sx * 8 + x, cy * 16 + sy * 8 + y][3] >= 128 else 0
                              for x in range(8)] for y in range(8)]
                        if any(v for r in t for v in r):
                            empty = False
                            i, hf, vf = tile_id(t)
                            ents.append((0x200 + i) | hf << 10 | vf << 11 | PAL << 12)
                        else:
                            ents.append(0)
                cells[(k, cxx, cy)] = None if empty else ents
    n = BASE_TILES + len(new)
    assert n <= 512, ('te veel tegels in de Cave-tileset', n)
    rows = (n + 15) // 16
    out = Image.new('P', (128, rows * 8), 0)
    out.putpalette(tim.getpalette())
    opx = out.load()
    for i, t in enumerate(old + new):
        for y in range(8):
            for x in range(8):
                opx[(i % 16) * 8 + x, (i // 16) * 8 + y] = t[y][x]
    out.save(CAVE + 'tiles.png')
    mk = open('graphics_file_rules.mk').read()
    mk2 = re.sub(r'(secondary/cave/tiles\.4bpp: %\.4bpp: %\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )\d+', r'\g<1>%d' % n, mk)
    assert mk2 != mk or ('-num_tiles %d' % n) in mk
    open('graphics_file_rules.mk', 'w').write(mk2)

    # metatiles: per koraalcel en per ondergrond een metatile (onderlaag = ondergrond, middenlaag = koraal)
    mt = open(CAVE + 'metatiles.bin', 'rb').read()[:BASE_METATILES * 16]
    at = open(CAVE + 'metatile_attributes.bin', 'rb').read()[:BASE_METATILES * 2]
    gmt = open('data/tilesets/primary/general/metatiles.bin', 'rb').read()

    def bottom(base):
        src, i = (gmt, base) if base < 0x200 else (mt, base - 0x200)
        return list(struct.unpack_from('<4H', src, i * 16))

    ids, nxt = {}, BASE_METATILES
    for (k, cxx, cy), ents in sorted(cells.items()):
        if ents is None:
            continue
        for bname, base in BASES.items():
            mt += struct.pack('<8H', *(bottom(base) + ents))
            at += struct.pack('<H', MB_NORMAL | LAYER_COVERED << 12)
            ids[(k, cxx, cy, bname)] = 0x200 + nxt; nxt += 1
    assert nxt <= 512, nxt
    open(CAVE + 'metatiles.bin', 'wb').write(mt)
    open(CAVE + 'metatile_attributes.bin', 'wb').write(at)
    print('koraal: %d tegels (Cave nu %d), %d metatiles (Cave nu %d)' % (len(new), n, nxt - BASE_METATILES, nxt))
    return ids, {k: (w, h) for k, (_, w, h) in sheets.items()}


def credits():
    p = 'CREDITS.md'
    s = open(p).read()
    line = ("- **Koraalbomen in de Koraalkathedraal**: **Ekat99**, *Coral Tiles* uit Ekat's Public Tiles (met "
            "**Heartlessdragoon** en **Vurtax**; uitsnede in `graphics/grounded/tilesets/ekat/coral_trees.png`).\n")
    s = ''.join(l for l in s.splitlines(True) if 'coral_trees.png' not in l)
    anchor = s.index('\n', s.index('- **Dode bomen in Lavender Town**')) + 1
    s = s[:anchor] + line + s[anchor:]
    open(p, 'w').write(s)


# ====================================================================== de kathedraal
UW = 'Underwater_Route126'
UW_SRC = (45, 65)                   # bestaand zwemgat (naar Underwater_SootopolisCity) als bron
HOLE = (64, 18)                     # nieuw zwemgat; bovenrij op y-1
DEEP = [(14, 10), (15, 10), (16, 10), (14, 11), (15, 11), (16, 11)]   # duikwater (0x294) midden in het meer
ARRIVE = (15, 11)
# koralen: (soort, x, y linksboven, ondergrond)
CORALS = [
    ('red', 10, 8, 'water'), ('purple', 19, 8, 'water'), ('purple', 24, 10, 'water'), ('red', 17, 18, 'water'), ('purple', 12, 19, 'water'),
    ('red', 26, 15, 'shallow'), ('purple', 15, 26, 'shallow'), ('red', 21, 24, 'shallow'),
]


def uw_hole():
    L = bd.layout_of(UW)
    uw = oq.read_layout(L['blockdata_filepath'], L['width'], L['height'])
    sx, sy = UW_SRC
    x, y = HOLE
    src = [[uw[sy - 1 + r][sx - 1 + c] for c in range(3)] for r in range(2)]
    assert [[t & 0x3ff for t in row] for row in src] == [[0x265, 0x266, 0x267], [0x26d, 0x26e, 0x26f]], src
    for r in range(2):
        for c in range(3):
            cur = uw[y - 1 + r][x - 1 + c] & 0x3ff
            assert cur in (0x21b, 0x216, 0x265, 0x266, 0x267, 0x26d, 0x26e, 0x26f), ('zwemgat-plek', hex(cur))
            uw[y - 1 + r][x - 1 + c] = src[r][c]
    assert cx.walkable(uw[y + 1][x]), 'onder het zwemgat ligt geen zeebodem'
    cx.save_grid(uw, L['blockdata_filepath'])
    return oq.edit_map(UW, lambda m: oq.warp_to(m, x, y, 'MAP_' + CONST))


TRAINERS = [
    (1080, 'SWIMMER_CORINNE', 'Koraalkathedraal: zwemt al jaren rondjes om hetzelfde koraal', 'CORINNE',
     'Swimmer F', 'Swimmer F', 'Female', 'Swimmer', bd.AI, None, [
        mon('Alomomola', 48, ['Scald', 'Wish', 'Protect', 'Knock Off']),
        mon('Lumineon', 48, ['Waterfall', 'U-turn', 'Ice Beam', 'Aqua Ring']),
        mon('Cursola', 49, ['Shadow Ball', 'Power Gem', 'Strength Sap', 'Hex'])]),
    (1081, 'FISHERMAN_DORIAN', 'Koraalkathedraal: vist in een kerk, voelt zich er niet schuldig over', 'DORIAN',
     'Fisherman', 'Fisherman', 'Male', 'Hiker', bd.AI, None, [
        mon('Corsola', 48, ['Power Gem', 'Recover', 'Scald', 'Stealth Rock']),
        mon('Bruxish', 48, ['Psychic Fangs', 'Aqua Jet', 'Crunch', 'Ice Fang']),
        mon('Lanturn', 49, ['Discharge', 'Scald', 'Ice Beam', 'Thunder Wave'])]),
]


def trainers():
    p = 'include/constants/opponents.h'
    s = open(p).read()
    blk = "// coral_cathedral { (tools/grounded/maptools/coral_cathedral.py; id's 1080-1089)\n"
    for n, const, why, *_ in TRAINERS:
        assert 1080 <= n <= 1089
        blk += '#define TRAINER_%-28s%d // Project Grounded: %s\n' % (const, n, why)
    blk += '// }'
    if '// coral_cathedral {' in s:
        i = s.index('// coral_cathedral {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    for n, *_ in TRAINERS:
        assert len(re.findall(r'^#define TRAINER_\w+\s+%d\b' % n, s, re.M)) == 1, ('trainer-id dubbel', n)
    open(p, 'w').write(s)

    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- coral_cathedral (tools/grounded/maptools/coral_cathedral.py) --- */\n\n'
    for n, const, why, nm, cls, pic, gender, music, ai, items, team in TRAINERS:
        hdr = ['Name: ' + nm, 'Class: ' + cls, 'Pic: ' + pic, 'Gender: ' + gender, 'Music: ' + music]
        if items:
            hdr.append('Items: ' + items)
        hdr += ['Double Battle: No', ai]
        blk += '=== TRAINER_%s ===\n%s\n\n%s\n\n' % (const, '\n'.join(hdr), '\n\n'.join(team))
    blk = blk.rstrip('\n') + '\n\n/* --- einde coral_cathedral --- */'
    s = bd.replace_block(s, '/* --- coral_cathedral', '/* --- einde coral_cathedral --- */', blk)
    open(p, 'w').write(s)


def check(g, start, objs, bgs, tag):
    blocked = {(o['x'], o['y']) for o in objs}
    walk = reach(g, [start], blocked=blocked)
    for o in objs:
        assert next_to((o['x'], o['y']), walk), (tag, 'object onbereikbaar', o['x'], o['y'], o['script'])
    for b in bgs:
        if b['type'] == 'hidden_item':
            assert (b['x'], b['y']) in walk, (tag, 'verborgen item onbereikbaar', b)
        else:
            assert next_to((b['x'], b['y']), walk) and not cx.walkable(g[b['y']][b['x']]), (tag, 'bord', b)
    return walk


def cathedral(ids, sizes):
    g, W, H, prim, sec = bd.copy_layout('ShoalCave_HighTideEntranceRoom', NAME)
    wall = g[1][4]
    assert (wall & 0x3ff) == 0x219
    for x0 in (5, 26):                           # de twee openingen bovenin dicht
        for x in range(x0, x0 + 3):
            g[1][x] = wall; g[2][x] = wall
    assert (g[30][20] & 0x3ff) == 0x275          # uitgang onderin: lagune + gesloten wand
    g[30][20] = g[30][19]
    for x in (19, 20, 21):
        g[31][x] = g[31][18]
    for x, y in DEEP:
        assert (g[y][x] & 0x3ff) == 0x170, (x, y, hex(g[y][x]))
        g[y][x] = 0x294 | (g[y][x] & 0xf000)
    for kind, x0, y0, base in CORALS:
        w, h = sizes[kind]
        for cy in range(h):
            for cxx in range(w):
                key = (kind, cxx, cy, base)
                if key not in ids:
                    continue                     # lege cel van het koraal: ondergrond blijft
                x, y = x0 + cxx, y0 + cy
                assert (g[y][x] & 0x3ff) == BASES[base] and cx.walkable(g[y][x]), ('koraal-ondergrond', kind, x, y, hex(g[y][x]))
                g[y][x] = ids[key] | COL | (g[y][x] & 0xf000)

    S = Scr(NAME, '''@ Project Grounded: Koraalkathedraal onder Route 126 (kopie van ShoalCave_HighTideEntranceRoom + koraal).
@ Ingang: zwemgat in Underwater_Route126 (%d,%d); terug = duiken. Kaart en scripts: tools/grounded/maptools/coral_cathedral.py.
%s_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, %s_OnResume
	.byte 0

%s_OnResume:
	setdivewarp MAP_UNDERWATER_ROUTE126, %d, %d
	setescapewarp MAP_UNDERWATER_ROUTE126, %d, %d
	end
''' % (HOLE[0], HOLE[1], NAME, NAME, NAME, HOLE[0], HOLE[1] + 1, HOLE[0], HOLE[1] + 1))
    P = S.P
    S.npc('Plaque', "THE CORAL CATHEDRAL\n\n"
                    "Services every Sunday. Current congregation: forty CORSOLA and one very confused LUVDISC.\n\n"
                    "Please do not touch the pews. The pews are alive.", 'MSGBOX_SIGN')
    tA = S.trainer('Corinne', 'SWIMMER_CORINNE',
                   "I've been swimming laps around this coral since I was six.\n\nIt has not grown. I have. "
                   "Neither of us is happy about it.",
                   "Fine. I'll go back to my laps.",
                   "Coral grows one centimeter a year.\n\nI did the math. I will be dead before it reaches the ceiling. "
                   "So will you. Sleep well.")
    tB = S.trainer('Dorian', 'FISHERMAN_DORIAN',
                   "Fishing in a cathedral? The sign didn't say I couldn't.\n\nThe sign also didn't say I could. "
                   "That's what lawyers call a gray area.",
                   "My line snapped. A sign from above.",
                   "I caught a LUVDISC here once. It looked at me like I'd ruined its wedding.\n\n"
                   "I let it go. I still think about it.")
    objs = [tr('OBJ_EVENT_GFX_SWIMMER_F', 22, 12, tA, 'LEFT', 4, elev=1),
            tr('OBJ_EVENT_GFX_FISHERMAN', 31, 10, tB, 'LEFT', 1),
            ball(4, 4, 'ITEM_SEA_SHARD', SHARD_FLAG(NAME)),
            ball(29, 7, 'ITEM_LUMINOUS_MOSS', 'FLAG_ITEM_CORAL_CATHEDRAL_LUMINOUS_MOSS'),
            ball(4, 26, 'ITEM_SHELL_BELL', 'FLAG_ITEM_CORAL_CATHEDRAL_SHELL_BELL', elev=4),
            ball(13, 4, 'ITEM_PEARL_STRING', 'FLAG_ITEM_CORAL_CATHEDRAL_PEARL_STRING')]
    bgs = [sign(9, 6, P + 'Plaque'),
           hidden(24, 29, 'ITEM_BIG_PEARL', 'FLAG_HIDDEN_ITEM_CORAL_CATHEDRAL_BIG_PEARL')]
    check(g, ARRIVE, objs, bgs, NAME)
    cx.save_grid(g, 'data/layouts/%s/map.bin' % NAME)
    bd.register_layout(NAME, CONST, W, H, prim, sec)
    ui = uw_hole()
    sms.write_map(NAME, CONST, objs, [warp(ARRIVE[0], ARRIVE[1], 'UNDERWATER_ROUTE126', ui)], [], bgs,
                  music='MUS_SEALED_CHAMBER', weather='WEATHER_NONE', map_type='MAP_TYPE_UNDERGROUND',
                  region_map_section='MAPSEC_ROUTE_126', show_map_name=False, allow_cycling=False,
                  allow_escaping=False)
    oq.register_map(NAME)
    S.write()


# ====================================================================== Sea Shards in de andere duikplekken
def behaviors(L):
    names = [m.group(1) for m in re.finditer(r'^\s*(MB_\w+)', open('include/constants/metatile_behaviors.h').read(), re.M)]

    def ts(sym, kind):
        return 'data/tilesets/%s/%s/' % (kind, re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', sym[len('gTileset_'):]).lower())
    pa = open(ts(L['primary_tileset'], 'primary') + 'metatile_attributes.bin', 'rb').read()
    sa = open(ts(L['secondary_tileset'], 'secondary') + 'metatile_attributes.bin', 'rb').read()

    def beh(t):
        t &= 0x3ff
        src, i = (pa, t) if t < 0x200 else (sa, t - 0x200)
        return names[struct.unpack_from('<H', src, 2 * i)[0] & 0xff]
    return beh


def place_shards():
    for n, m, target, kind in SHARDS:
        L = bd.layout_of(m)
        g = oq.read_layout(L['blockdata_filepath'], L['width'], L['height'])
        beh = behaviors(L)
        mj = json.load(open('data/maps/%s/map.json' % m))
        flag = SHARD_FLAG(m)
        mj['object_events'] = [o for o in mj['object_events'] if o.get('flag') != flag]
        mj['bg_events'] = [b for b in mj['bg_events'] if b.get('flag') != flag]
        taken = {(o['x'], o['y']) for o in mj['object_events']} | {(b['x'], b['y']) for b in mj['bg_events']} | \
                {(w['x'], w['y']) for w in mj['warp_events']}
        w0 = mj['warp_events'][0]
        walk = reach(g, [(w0['x'], w0['y'])], blocked=taken - {(w0['x'], w0['y'])})
        under = m.startswith('Underwater_')
        ok = [c for c in walk if c not in taken and
              (under or not any(s in beh(g[c[1]][c[0]]) for s in ('WATER', 'WARP', 'DOOR', 'LADDER', 'STAIRS', 'ARROW')))
              and all(abs(c[0] - w['x']) + abs(c[1] - w['y']) > 2 for w in mj['warp_events'])]
        assert ok, m
        c = min(ok, key=lambda c: ((c[0] - target[0]) ** 2 + (c[1] - target[1]) ** 2, c))
        if kind == 'ball':
            o = ball(c[0], c[1], 'ITEM_SEA_SHARD', flag, elev=g[c[1]][c[0]] >> 12 or 3)
            mj['object_events'].append(o)
            assert len(mj['object_events']) < 16
        else:
            mj['bg_events'].append(hidden(c[0], c[1], 'ITEM_SEA_SHARD', flag))
        open('data/maps/%s/map.json' % m, 'w').write(json.dumps(mj, indent=2, ensure_ascii=False) + '\n')
        print('Sea Shard: %-28s %s %s' % (m, kind, c))


# ====================================================================== Diving Treasure Hunter (Route 124)
HUNTER = 'Route124_DivingTreasureHuntersHouse'


def hunter():
    p = 'data/maps/%s/scripts.inc' % HUNTER
    s = open(p).read()
    P, T = HUNTER + '_EventScript_', HUNTER + '_Text_'
    hook = '%sTreasureHunter::\n\tlock\n\tfaceplayer\n' % P
    jump = '\tcheckitem ITEM_SEA_SHARD\n\tgoto_if_eq VAR_RESULT, TRUE, %sSeaShards\n' % P
    assert hook in s
    if jump not in s:
        s = s.replace(hook, hook + jump)
    code = ['%sSeaShards::' % P,
            '\tgoto_if_set FLAG_SEA_SHARDS_EXPLAINED, %sSeaShardsAgain' % P,
            '\tmsgbox %sSeaShardsFirst, MSGBOX_DEFAULT' % T,
            '\tsetflag FLAG_SEA_SHARDS_EXPLAINED',
            '\tgoto %sSeaShardsTake' % P, '',
            '%sSeaShardsAgain::' % P,
            '\tmsgbox %sSeaShardsAgain, MSGBOX_DEFAULT' % T, '',
            '%sSeaShardsTake::' % P,
            '\tremoveitem ITEM_SEA_SHARD',
            '\tcheckitem ITEM_SEA_SHARD',
            '\tgoto_if_eq VAR_RESULT, TRUE, %sSeaShardsTake' % P,
            '\tsetvar VAR_TEMP_2, 0']
    for f in ALL_SHARD_FLAGS:
        code.append('\tcall_if_set %s, %sSeaShardCount' % (f, P))
    code += ['\tbuffernumberstring STR_VAR_1, VAR_TEMP_2',
             '\tmsgbox %sSeaShardsCount, MSGBOX_DEFAULT' % T]
    for need, item, qty in REWARDS:
        code += ['\tgoto_if_lt VAR_TEMP_2, %d, %sSeaShardsDone' % (need, P),
                 '\tcall_if_unset FLAG_SEA_SHARD_REWARD_%d, %sSeaShardReward%d' % (need, P, need)]
    code += ['\tmsgbox %sSeaShardsAll, MSGBOX_DEFAULT' % T, '\trelease', '\tend', '',
             '%sSeaShardsDone::' % P, '\tmsgbox %sSeaShardsMore, MSGBOX_DEFAULT' % T, '\trelease', '\tend', '',
             '%sSeaShardCount::' % P, '\taddvar VAR_TEMP_2, 1', '\treturn', '']
    for need, item, qty in REWARDS:
        code += ['%sSeaShardReward%d::' % (P, need),
                 '\tmsgbox %sSeaShardReward%d, MSGBOX_DEFAULT' % (T, need),
                 '\tgiveitem %s, %d' % (item, qty),
                 '\tgoto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull',
                 '\tsetflag FLAG_SEA_SHARD_REWARD_%d' % need, '\treturn', '']
    texts = [
        ('SeaShardsFirst', "Hold on. Is that a SEA SHARD?\n\n"
                           "Nobody knows what they are. Not me, not the professors, not the shards themselves.\n\n"
                           "But they glow, and in my line of work, glowing means money. I'll take every one you have.\n\n"
                           "In return you get things from the seabed that don't glow. That's called a business model."),
        ('SeaShardsAgain', "More SEA SHARDS! Hand them over. Slowly. I've been hurt before."),
        ('SeaShardsCount', "That makes {STR_VAR_1} out of the eight I'm sure exist.\n\n"
                           "I'm sure because I made a list, and lists are never wrong."),
        ('SeaShardReward2', "Two already! Have some DIVE BALLS. They work best underwater. Like me. Unlike my marriage."),
        ('SeaShardReward4', "Four! Take these HEAVY-DUTY BOOTS.\n\n"
                            "I found them on a skeleton on the seabed. He won't miss them. He isn't going anywhere."),
        ('SeaShardReward6', "Six! Here's a GOLD BOTTLE CAP.\n\n"
                            "It sealed the captain's private rum on a sunken ship. The rum is gone. So is the captain. "
                            "The cap stayed loyal."),
        ('SeaShardReward8', "All eight.\n\n"
                            "Thirty years I searched for these. You did it between two naps. I hate you a little.\n\n"
                            "Take my greatest treasure: a MASTER BALL from a sunken bank vault.\n\n"
                            "I never used it. I never met anything worth it. That includes people."),
        ('SeaShardsMore', "There are more down there. Check every place you can dive.\n\n"
                          "I'll be here. Slowly drying out. Like a sponge with regrets."),
        ('SeaShardsAll', "That's every SEA SHARD in HOENN. I can finally retire.\n\n"
                         "Where to? Underwater, obviously. Where else would I go?"),
    ]
    blk = '\n'.join(code) + '\n' + ''.join(bd.text(T + k, v) for k, v in texts)
    start, end = '@ --- coral_cathedral (', '@ --- einde coral_cathedral ---'
    new = '@ --- coral_cathedral (Sea Shards; gegenereerd door tools/grounded/maptools/coral_cathedral.py) ---\n' + \
          blk.rstrip('\n') + '\n' + end
    s = bd.replace_block(s, start, end, new)
    open(p, 'w').write(s.rstrip('\n') + '\n')


# ====================================================================== wilde Pokemon
WILD = {
    CONST: dict(
        land=(8, [('CORSOLA', 46, 48), ('PYUKUMUKU', 46, 48), ('TOXAPEX', 46, 48), ('BARBARACLE', 46, 48),
                  ('PALOSSAND', 46, 48), ('CRABRAWLER', 46, 48), ('KINGLER', 47, 49), ('SLOWBRO', 47, 49),
                  ('SHUCKLE', 47, 49), ('DHELMISE', 48, 50), ('GOLISOPOD', 49, 51), ('CURSOLA', 50, 52)]),
        water=(4, [('LUVDISC', 45, 48), ('ALOMOMOLA', 46, 49), ('LUMINEON', 46, 49), ('MANTINE', 47, 50),
                   ('LANTURN', 48, 51)]),
        fishing=(25, [('LUVDISC', 20, 24), ('FINNEON', 20, 24), ('CHINCHOU', 26, 30), ('QWILFISH', 26, 30),
                      ('CORSOLA', 26, 30), ('ALOMOMOLA', 40, 45), ('LUMINEON', 40, 45), ('LANTURN', 42, 46),
                      ('BRUXISH', 43, 47), ('CLAWITZER', 45, 48)])),
}


# ====================================================================== main
if __name__ == '__main__':
    flags()
    ids, sizes = coral_tileset()
    credits()
    trainers()
    cathedral(ids, sizes)
    place_shards()
    hunter()
    bd.WILD = WILD
    bd.wild()
    if len(sys.argv) > 1:
        for n in [NAME, UW]:
            L = bd.layout_of(n)
            subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), n,
                            os.path.join(sys.argv[1], n + '.png'), '0', str(L['height'])], check=True)
    print('klaar')
