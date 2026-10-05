"""Project Grounded: de Ogerpon-quest (post-game). Bouwt de drie schuilplaatsen van de Loyal Three en de
ingangen ernaartoe. Deterministisch (vaste seed) en idempotent.

  GraniteCave_CornerstoneRoom  Okidogi + CORNERSTONE MASK. Kopie van de kamer van Steven (Granite Cave).
                               Ingang: een zuidpijl-uitgang in de zuidwand van Granite Cave B2F (8,22).
  FieryPath_EmberHollow        Munkidori + HEARTHFLAME MASK. Kleine lavagrot (18x14, General + Lavaridge,
                               dezelfde autotiler als de lavabuis van chimney_ext.py) met een magmapoel in de
                               noordwand. Ingang: grotopening in de noordwand van de doodlopende zak linksonder in
                               Fiery Path (8,26-27).
  Route127_WellspringGrotto    Fezandipiti + WELLSPRING MASK. Kopie van de ingang van de Seafloor Cavern
                               (zandgrot met poel), noordelijke doorgang dichtgemaakt. Ingang: zwemgat in de
                               noordwand van de zuidoostelijke kom van Underwater_Route127 (72,45); terug = duiken.

De openingen zelf worden pas gezet (setmetatile in de ON_LOAD-scripts) zodra de maskerhoedster in Fortree Jungle
het verhaal heeft verteld (FLAG_OGERPON_QUEST_STARTED). Dit script legt alleen de kaarten, warps en registratie.
Gebruik: python3 tools/grounded/maptools/ogerpon_quest.py [rendermap]"""
import json, os, random, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chimney_ext as cx          # zet ook de werkmap op de repo-root

T, walkable, reach = cx.T, cx.walkable, cx.reach

# ---------------------------------------------------------------- hulpjes
def read_layout(path, W, H):
    b = open(path, 'rb').read()[:W * H * 2]
    v = struct.unpack('<%dH' % (W * H), b)
    return [list(v[y * W:(y + 1) * W]) for y in range(H)]

def register_layout(name, const, W, H, secondary):
    lj = open('data/layouts/layouts.json').read()
    entry = '''    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (const, name, W, H, secondary, name, name)
    if '"LAYOUT_%s"' % const in lj:
        i = lj.index('"id": "LAYOUT_%s"' % const); s = lj.rindex('    {', 0, i); e = lj.index('    }', i) + 5
        lj = lj[:s] + entry + lj[e:]
    else:
        i = lj.rindex('    }\n  ]')
        lj = lj[:i + 5] + ',\n' + entry + lj[i + 5:]
    open('data/layouts/layouts.json', 'w').write(lj)
    json.loads(lj)

def obj(gfx, x, y, script, flag, local_id, elev=3, move='MOVEMENT_TYPE_FACE_DOWN'):
    return {'local_id': local_id, 'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': move,
            'movement_range_x': 0, 'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE',
            'trainer_sight_or_berry_tree_id': '0', 'script': script, 'flag': flag}

def warp_to(m, x, y, dest):
    """Zet (of vervang) een warp naar `dest` op (x,y) in kaart-dict m; geeft de index terug."""
    for i, w in enumerate(m['warp_events']):
        if w['dest_map'] == dest:
            w.update({'x': x, 'y': y, 'elevation': 0, 'dest_warp_id': '0'}); return i
    m['warp_events'].append({'x': x, 'y': y, 'elevation': 0, 'dest_map': dest, 'dest_warp_id': '0'})
    return len(m['warp_events']) - 1

def edit_map(name, fn):
    p = 'data/maps/%s/map.json' % name
    m = json.load(open(p)); r = fn(m)
    open(p, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    return r

def write_map(name, const, base, layout_const, objs, warps, **kw):
    b = json.load(open('data/maps/%s/map.json' % base))
    m = {k: b[k] for k in b}
    m.update({'id': 'MAP_' + const, 'name': name, 'layout': 'LAYOUT_' + layout_const, 'connections': None,
              'object_events': objs, 'warp_events': warps, 'coord_events': [], 'bg_events': [],
              'show_map_name': False})
    m.update(kw)
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')

def register_map(name):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        i = g.index('"gMapGroup_Grounded": ['); j = g.index(']', i)
        g = g[:i] + g[i:j].rstrip() + ',\n    "%s"\n  ' % name + g[j:]
        open('data/maps/map_groups.json', 'w').write(g)
        assert len(json.loads(g)['gMapGroup_Grounded']) <= 128
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/MangroveMire/scripts.inc"\n'
        assert anchor in es
        es = es.replace(anchor, anchor + inc, 1)
        open('data/event_scripts.s', 'w').write(es)

def save(g, name, border_from):
    os.makedirs('data/layouts/' + name, exist_ok=True)
    cx.save_grid(g, 'data/layouts/%s/map.bin' % name)
    b = open(border_from, 'rb').read()
    open('data/layouts/%s/border.bin' % name, 'wb').write(b)

# ---------------------------------------------------------------- 1. Cornerstone (Granite Cave)
GC_EXIT = (8, 22)          # zuidpijl-uitgang in Granite Cave B2F
def cornerstone():
    name, const = 'GraniteCave_CornerstoneRoom', 'GRANITE_CAVE_CORNERSTONE_ROOM'
    W, H = 15, 14
    g = read_layout('data/layouts/GraniteCave_StevensRoom/map.bin', W, H)
    save(g, name, 'data/layouts/GraniteCave_StevensRoom/border.bin')
    register_layout(name, const, W, H, 'gTileset_Cave')
    # B2F: zuidwand openen (zoals de ingang van de kamer van Steven in 1F: 258/259/25a + 23c), warp erop
    b2 = read_layout('data/layouts/GraniteCave_B2F/map.bin', 32, 26)
    x, y = GC_EXIT
    assert walkable(b2[y][x]) and (b2[y + 1][x] & 0x3ff) == 0x209, 'B2F-uitgang staat niet tegen de zuidwand'
    gi = edit_map('GraniteCave_B2F', lambda m: warp_to(m, x, y, 'MAP_' + const))
    write_map(name, const, 'GraniteCave_StevensRoom', const,
              [obj('OBJ_EVENT_GFX_SPECIES(OKIDOGI)', 7, 8, name + '_EventScript_Okidogi', 'FLAG_DEFEATED_OKIDOGI',
                   'LOCALID_CORNERSTONE_ROOM_OKIDOGI')],
              [{'x': 7, 'y': 3, 'elevation': 0, 'dest_map': 'MAP_GRANITE_CAVE_B2F', 'dest_warp_id': str(gi)}],
              music='MUS_SEALED_CHAMBER')
    register_map(name)
    assert (7, 8) in reach(g, [(7, 4)]), 'Okidogi onbereikbaar'
    return name

# ---------------------------------------------------------------- 2. Hearthflame (Fiery Path)
FP_DOOR = (8, 27)          # grotopening in Fiery Path (bovenhelft op (8,26))
EH_W, EH_H = 18, 14
EH_DOOR = (3, 2)
EH_MUNKIDORI = (8, 6)
def ember_mask():
    m = [['.'] * EH_W for _ in range(EH_H)]
    def carve(x0, y0, x1, y1, c='#'):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                m[yy][xx] = c
    carve(2, 3, 15, 11)                      # de kamer
    for c in ((2, 3), (15, 3), (2, 11), (15, 11), (14, 11), (3, 11)):
        m[c[1]][c[0]] = '.'                  # afgeronde hoeken
    carve(5, 3, 12, 4, '.'); carve(6, 3, 11, 4, 'L')        # magmapoel in de noordwand
    carve(13, 9, 14, 10, '.')                # rotsuitsteeksel rechtsonder
    return [''.join(r) for r in m]

def hearthflame():
    name, const = 'FieryPath_EmberHollow', 'FIERY_PATH_EMBER_HOLLOW'
    random.seed(4242)
    mask = ember_mask()
    g = cx.cave_tiles(mask)
    cx.cave_door(g, *EH_DOOR)
    start = (EH_DOOR[0], EH_DOOR[1] + 1)
    o = obj('OBJ_EVENT_GFX_SPECIES(MUNKIDORI)', EH_MUNKIDORI[0], EH_MUNKIDORI[1], name + '_EventScript_Munkidori',
            'FLAG_DEFEATED_MUNKIDORI', 'LOCALID_EMBER_HOLLOW_MUNKIDORI')
    keep = cx.keep_cells([o], [], cx.area([start]) | cx.area([EH_MUNKIDORI], 2))
    cx.decorate(g, cx.FLOOR, 'cave', keep, [start], [
        ('sulfur_a', 2, 'muur'), ('sulfur_b', 2, 'muur'), ('rock', 2, 'muur'), ('ash_a', 2, 'vrij'),
        ('crack_a', 3, 'vrij'), ('crack_b', 3, 'vrij'), ('basalt', 1, 'open')], random.Random(99))
    assert EH_MUNKIDORI in reach(g, [start]), 'Munkidori onbereikbaar'
    save(g, name, 'data/layouts/FieryPath_HeatranLair/border.bin')
    register_layout(name, const, EH_W, EH_H, 'gTileset_Lavaridge')
    fp = read_layout('data/layouts/FieryPath/map.bin', 35, 38)
    x, y = FP_DOOR
    assert (fp[y][x] & 0x3ff) == 0x274 and walkable(fp[y + 1][x]), 'Fiery Path-opening staat niet in een noordwand'
    fi = edit_map('FieryPath', lambda m: warp_to(m, x, y, 'MAP_' + const))
    write_map(name, const, 'FieryPath_HeatranLair', const, [o],
              [{'x': EH_DOOR[0], 'y': EH_DOOR[1], 'elevation': 0, 'dest_map': 'MAP_FIERY_PATH', 'dest_warp_id': str(fi)}],
              music='MUS_SEALED_CHAMBER')
    register_map(name)
    return name

# ---------------------------------------------------------------- 3. Wellspring (Route 127, onderwater)
UW_HOLE = (72, 45)         # zwemgat in Underwater_Route127 (bovenkant op rij 44)
def wellspring():
    name, const = 'Route127_WellspringGrotto', 'ROUTE127_WELLSPRING_GROTTO'
    W, H = 20, 20
    g = read_layout('data/layouts/SeafloorCavern_Entrance/map.bin', W, H)
    for x in (9, 10, 11):                     # noordelijke doorgang dicht (rotswand zoals ernaast)
        g[0][x] = T(0x2f9, True); g[1][x] = T(0x2f9, True)
    save(g, name, 'data/layouts/SeafloorCavern_Entrance/border.bin')
    register_layout(name, const, W, H, 'gTileset_Cave')
    uw = read_layout('data/layouts/Underwater_Route127/map.bin', 80, 80)
    x, y = UW_HOLE
    assert walkable(uw[y + 1][x]), 'onder het zwemgat ligt geen zeebodem'
    ui = edit_map('Underwater_Route127', lambda m: warp_to(m, x, y, 'MAP_' + const))
    write_map(name, const, 'SeafloorCavern_Entrance', const,
              [obj('OBJ_EVENT_GFX_SPECIES(FEZANDIPITI)', 10, 5, name + '_EventScript_Fezandipiti',
                   'FLAG_DEFEATED_FEZANDIPITI', 'LOCALID_WELLSPRING_GROTTO_FEZANDIPITI')],
              [{'x': 10, 'y': 18, 'elevation': 3, 'dest_map': 'MAP_UNDERWATER_ROUTE127', 'dest_warp_id': str(ui)}],
              music='MUS_SEALED_CHAMBER', region_map_section='MAPSEC_ROUTE_127')
    register_map(name)
    land = [(xx, yy) for yy in range(H) for xx in range(W) if (g[yy][xx] & 0x3ff) == 0x124]
    assert (10, 5) in reach(g, [(10, 6)]) and (10, 6) in land
    return name

if __name__ == '__main__':
    names = [cornerstone(), hearthflame(), wellspring()]
    if len(sys.argv) > 1:
        import subprocess
        for n in names:
            subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), n,
                            os.path.join(sys.argv[1], n + '.png'), '0', '40'], check=True)
    print('klaar:', ', '.join(names))
