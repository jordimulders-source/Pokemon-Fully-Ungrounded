#!/usr/bin/env python3
# Project Grounded: maakt src/data/berry_tree_locations.h uit data/maps/*/map.json.
# Draai opnieuw als er bessenbomen worden toegevoegd of verplaatst: python3 tools/grounded/berry_tree_locations.py
import glob, json, re

ids = {}
for line in open('include/constants/berry.h'):
    m = re.match(r'#define (BERRY_TREE_\w+)\s+(\d+)', line)
    if m:
        ids[m.group(1)] = int(m.group(2))

rows = {}
for f in sorted(glob.glob('data/maps/*/map.json')):
    d = json.load(open(f))
    for o in d.get('object_events', []):
        if o.get('script') == 'BerryTreeScript':
            rows[o['trainer_sight_or_berry_tree_id']] = d['region_map_section']

out = ['// Project Grounded: gegenereerd door tools/grounded/berry_tree_locations.py, niet met de hand aanpassen.',
       '// Op welke kaart staat welke bessenboom; gebruikt door de Wailmer Pail (overzicht rijpe bessen).',
       'static const mapsec_u16_t sBerryTreeMapSecs[BERRY_TREES_COUNT] =',
       '{']
byid = {ids[t]: (t, sec) for t, sec in rows.items()}
for i in range(128):  # BERRY_TREES_COUNT
    if i in byid:
        out.append(f'    [{byid[i][0]}] = {byid[i][1]},')
    else:
        out.append(f'    [{i}] = MAPSEC_NONE,')
out.append('};')
open('src/data/berry_tree_locations.h', 'w').write('\n'.join(out) + '\n')
print(f'{len(rows)} bessenbomen')
