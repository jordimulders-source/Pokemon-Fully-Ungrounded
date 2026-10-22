"""Fully Ungrounded: haalt de hele Hoenn-wereld weg (PLAN_HOENN_ERUIT.md, stap 5).

Wat blijft staat in skelet_keep.py (kaarten in gMapGroup_FullyUngrounded, bewaarde layouts). Weg:
- alle andere kaartgroepen uit map_groups.json en hun mappen in data/maps/;
- hun `.include`s uit data/event_scripts.s;
- layouts die niet in KEEP_LAYOUTS staan (layouts.json + data/layouts/);
- heal locations behalve die van de skeletkaarten, wilde encounters (gWildMonHeaders) behalve die van de
  skeletkaarten (Battle Pyramid/Pike blijven, die hangen niet aan een kaart);
- FLAG_HIDE_*-regels in data/scripts/new_game.inc die geen bewaarde kaart meer gebruikt;
- gegenereerde bestanden die make niet altijd opnieuw maakt.
Daarna: berry_tree_locations.py, debug_zone_warps.py en map_compat.py. Tilesets en graphics blijven staan.
Idempotent. Gebruik: python3 tools/grounded/maptools/hoenn_eruit.py
"""
import glob, json, os, re, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skelet_keep import GROUP, MAPS, KEEP_LAYOUTS  # noqa: E402


def dump(path, data):
    open(path, 'w').write(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def map_groups():
    p = 'data/maps/map_groups.json'
    d = json.load(open(p))
    assert d[GROUP] == MAPS, 'groep wijkt af van skelet_keep.MAPS'
    t = '{\n  "group_order": [\n    "%s"\n  ],\n  "%s": [\n%s\n  ]\n}\n' % (
        GROUP, GROUP, ',\n'.join('    "%s"' % m for m in MAPS))
    open(p, 'w').write(t)
    json.load(open(p))


def map_dirs():
    n = 0
    for d in sorted(glob.glob('data/maps/*/')):
        name = d.rstrip('/').split('/')[-1]
        if name not in MAPS:
            shutil.rmtree(d)
            n += 1
    for f in ['connections.inc', 'events.inc', 'groups.inc', 'headers.inc']:
        if os.path.exists('data/maps/' + f):
            os.remove('data/maps/' + f)
    return n


def event_scripts():
    p = 'data/event_scripts.s'
    out, n = [], 0
    for l in open(p).read().split('\n'):
        m = re.match(r'\s*\.include "data/maps/([^/]+)/', l)
        if m and m.group(1) not in MAPS:
            n += 1
            continue
        out.append(l)
    open(p, 'w').write('\n'.join(out))
    return n


def layouts():
    p = 'data/layouts/layouts.json'
    d = json.load(open(p))
    keep = [l for l in d['layouts'] if l and l.get('id') in KEEP_LAYOUTS]
    assert len(keep) == len(KEEP_LAYOUTS), set(KEEP_LAYOUTS) - {l['id'] for l in keep}
    d['layouts'] = keep
    dump(p, d)
    used = {os.path.dirname(l[k]) for l in keep for k in ('border_filepath', 'blockdata_filepath')}
    n = 0
    for dd in sorted(glob.glob('data/layouts/*/')):
        if dd.rstrip('/') not in used:
            shutil.rmtree(dd)
            n += 1
    return n


def map_ids():
    return {json.load(open('data/maps/%s/map.json' % m))['id'] for m in MAPS}


def heal_locations():
    p = 'src/data/heal_locations.json'
    d = json.load(open(p))
    ids = map_ids()
    d['heal_locations'] = [h for h in d['heal_locations'] if h['map'] in ids]
    dump(p, d)
    return len(d['heal_locations'])


def wild():
    p = 'src/data/wild_encounters.json'
    d = json.load(open(p))
    ids = map_ids()
    for g in d['wild_encounter_groups']:
        if g.get('for_maps'):
            g['encounters'] = [e for e in g['encounters'] if e['map'] in ids]
    dump(p, d)


def hide_flags():
    """FLAG_HIDE_*-regels in new_game.inc weg als geen bewaarde kaart die flag nog gebruikt."""
    used = set()
    for m in MAPS:
        used.update(re.findall(r'FLAG_HIDE_\w+', open('data/maps/%s/map.json' % m).read()))
        used.update(re.findall(r'FLAG_HIDE_\w+', open('data/maps/%s/scripts.inc' % m).read()))
    p = 'data/scripts/new_game.inc'
    out, n = [], 0
    for l in open(p).read().split('\n'):
        m = re.match(r'\s*setflag (FLAG_HIDE_\w+)\s*$', l)
        if m and m.group(1) not in used:
            n += 1
            continue
        out.append(l)
    open(p, 'w').write('\n'.join(out))
    return n


def generated():
    for f in ['build/emerald/data/maps.o', 'build/emerald/data/map_events.o', 'include/constants/map_groups.h',
              'include/constants/layouts.h', 'include/constants/map_event_ids.h', 'data/layouts/layouts.inc',
              'data/layouts/layouts_table.inc', 'src/data/map_group_count.h']:
        if os.path.exists(f):
            os.remove(f)


def main():
    map_groups()
    print('kaartmappen weg:', map_dirs())
    print('includes weg:', event_scripts())
    print('layoutmappen weg:', layouts())
    print('heal locations over:', heal_locations())
    wild()
    print('FLAG_HIDE-regels weg:', hide_flags())
    generated()
    py = sys.executable
    for s in ['tools/grounded/berry_tree_locations.py', 'tools/grounded/debug_zone_warps.py',
              'tools/grounded/maptools/map_compat.py']:
        subprocess.run([py, s], check=True)


if __name__ == '__main__':
    main()
