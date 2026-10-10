#!/usr/bin/env python3
"""Project Grounded: debugmenu Utilities > "Zone warp…": warpt naar elke kaart van de game, per kaartgroep
(eerst gMapGroup_Grounded, gMapGroup_Spacetime, gMapGroup_UltraSpace). Doel = warp 0 van de kaart (zonder warps: het midden).
Genereert src/data/debug_zone_warps.h. Opnieuw draaien na nieuwe kaarten."""
import json, re
G = json.load(open('data/maps/map_groups.json'))
FIRST = [('gMapGroup_Grounded', 'Eilanden/quests'), ('gMapGroup_Spacetime', 'Spacetime'), ('gMapGroup_UltraSpace', 'Ultra Space')]
# Jordi: 'eigenlijk alle areas in de game': eerst de post-game/eigen groepen, daarna elke andere kaartgroep
GROUPS = FIRST + [(g, g[len('gMapGroup_'):][:18]) for g in G['group_order'] if g not in dict(FIRST)]
def const(m):
    return 'MAP_' + re.sub(r'(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', '_', m).upper().replace('__', '_')
out = ['// Gegenereerd door tools/grounded/debug_zone_warps.py, niet met de hand bewerken.', '']
menus = []
for g, label in GROUPS:
    maps = G[g]
    for part in range(0, len(maps), 45):
        chunk = maps[part:part + 45]
        name = 'sDebugMenu_ZoneWarp_%s_%d' % (g[len('gMapGroup_'):], part // 45)
        title = label + ('' if len(maps) <= 45 else ' %d' % (part // 45 + 1)) + '…'
        out.append('static const struct DebugMenuOption %s[] =\n{' % name)
        for m in chunk:
            mid = json.load(open('data/maps/%s/map.json' % m))['id']
            out.append('    { COMPOUND_STRING("%s"), DebugAction_Util_ZoneWarp, (const void *)(uintptr_t)%s },' % (m[:22], mid))
        out += ['    { NULL }', '};', '']
        menus.append((title, name))
out.append('static const struct DebugMenuOption sDebugMenu_Actions_ZoneWarp[] =\n{')
for title, name in menus:
    out.append('    { COMPOUND_STRING("%s"), DebugAction_OpenSubMenu, %s },' % (title, name))
out += ['    { NULL }', '};', '']
open('src/data/debug_zone_warps.h', 'w').write('\n'.join(out))
print(sum(len(G[g]) for g, _ in GROUPS), 'kaarten,', len(menus), 'submenu\'s')
