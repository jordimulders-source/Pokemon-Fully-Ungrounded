"""Fully Ungrounded: overgangsheader voor verdwenen kaarten en layouts (PLAN_HOENN_ERUIT.md, stap 4).

Zoekt alle MAP_*- en LAYOUT_*-constanten die in src/, include/, data/, asm/ en test/ gebruikt worden maar niet meer
bestaan (niet meer in map_groups.json / layouts.json), en schrijft include/constants/map_compat.h met voor elke oude
kaart een EIGEN waarde in een groep die niet bestaat: groep 0x40 + de oude groep, met het oude kaartnummer. Zo blijven
switches met meerdere oude kaarten geldig (geen dubbele case-waarden) en is een test op zo'n kaart gewoon nooit waar.
Layouts krijgen 0x4000 + hun oude index. De oude nummering komt uit git (commit BASE).

Code die zo'n waarde als index gebruikt (gMapGroups[MAP_GROUP(x)], gMapLayouts[LAYOUT_X - 1]) leest buiten de tabel:
dat is code voor verdwenen kaarten en hoort bij stap 7 (opruimen); de header krimpt dan vanzelf.
Gebruik: python3 tools/grounded/maptools/map_compat.py (na elke kaartwijziging; make ziet het bestand als gewone header).
"""
import json, os, re, subprocess

BASE = 'a64c32e28d'
OUT = 'include/constants/map_compat.h'
SCAN = ['src', 'include', 'data', 'asm', 'test']
SKIP = {OUT, 'include/constants/map_groups.h', 'include/constants/layouts.h', 'src/data/debug_zone_warps.h',
        'src/data/map_group_count.h'}
EXT = ('.c', '.h', '.s', '.inc', '.json', '.party', '.txt')


def git(path):
    return subprocess.run(['git', 'show', '%s:%s' % (BASE, path)], capture_output=True, check=True, text=True).stdout


def old_maps():
    """Oude kaart-id -> (groep, nummer) zoals in BASE."""
    groups = json.loads(git('data/maps/map_groups.json'))
    res = {}
    for gi, g in enumerate(groups['group_order']):
        for mi, name in enumerate(groups[g]):
            mid = json.loads(git('data/maps/%s/map.json' % name))['id']
            res[mid] = (gi, mi)
    return res


def old_layouts():
    lay = json.loads(git('data/layouts/layouts.json'))['layouts']
    return {l['id']: i + 1 for i, l in enumerate(lay) if l and 'id' in l}


def current():
    groups = json.load(open('data/maps/map_groups.json'))
    maps = set()
    for g in groups['group_order']:
        for name in groups[g]:
            maps.add(json.load(open('data/maps/%s/map.json' % name))['id'])
    lays = {l['id'] for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l and 'id' in l}
    return maps, lays


def used():
    found = set()
    pat = re.compile(r'\b(?:MAP|LAYOUT)_[A-Z0-9_]+\b')
    for top in SCAN:
        for root, _dirs, files in os.walk(top):
            for f in files:
                p = os.path.join(root, f)
                if p in SKIP or not f.endswith(EXT):
                    continue
                try:
                    found.update(pat.findall(open(p, errors='ignore').read()))
                except OSError:
                    pass
    return found


def main():
    cache = 'build/map_compat_base.json'  # oude nummering uit git, alleen een cache
    os.makedirs('build', exist_ok=True)
    if os.path.exists(cache):
        c = json.load(open(cache))
        maps, lays = {k: tuple(v) for k, v in c['maps'].items()}, c['layouts']
    else:
        maps, lays = old_maps(), old_layouts()
        json.dump({'maps': maps, 'layouts': lays}, open(cache, 'w'))
    cur_maps, cur_lays = current()
    u = used()
    gone_maps = sorted(m for m in u if m in maps and m not in cur_maps)
    gone_lays = sorted(l for l in u if l in lays and l not in cur_lays)
    lines = [
        '#ifndef GUARD_CONSTANTS_MAP_COMPAT_H',
        '#define GUARD_CONSTANTS_MAP_COMPAT_H',
        '',
        '// Gegenereerd door tools/grounded/maptools/map_compat.py, niet met de hand bewerken.',
        '// Fully Ungrounded: verdwenen Hoenn-kaarten/-layouts die de code nog noemt. Elke kaart heeft een eigen waarde',
        '// in een groep die niet bestaat (0x40 + oude groep), dus een test erop is nooit waar. Opruimen per systeem',
        '// (PLAN_HOENN_ERUIT.md, stap 7) laat deze lijst krimpen tot hij leeg is en weg kan.',
        '// %d kaarten, %d layouts.' % (len(gone_maps), len(gone_lays)),
        '',
    ]
    for m in gone_maps:
        g, n = maps[m]
        lines.append('#define %s (%d | (0x%X << 8))' % (m, n, 0x40 + g))
    if gone_lays:
        lines.append('')
    for l in gone_lays:
        lines.append('#define %s 0x%X' % (l, 0x4000 + lays[l]))
    lines += ['', '#endif // GUARD_CONSTANTS_MAP_COMPAT_H', '']
    text = '\n'.join(lines)
    if not os.path.exists(OUT) or open(OUT).read() != text:
        open(OUT, 'w').write(text)
    print('map_compat.h: %d kaarten, %d layouts' % (len(gone_maps), len(gone_lays)))


if __name__ == '__main__':
    main()
