"""Project Grounded: Forces-trio op routes (post-game, src/forces.c + data/scripts/forces.inc).

Zet per kandidaatroute het object van de Force (verborgen met FLAG_FORCES_HIDE_*, dat src/forces.c bij elke
binnenkomst zet of wist) en per Force één hint-NPC. Idempotent; controleert bereikbaarheid en vrije tegels.
Draaien vanuit de root van de repo: python3 tools/grounded/maptools/forces_routes.py
"""
import json
import sys
sys.path.insert(0, 'tools/grounded/maptools')
import landlib
from landlib import Kaart, obj

# (kaart, x, y, gfx, script, flag, bereikbaar-vanaf)
FORCES = [
    # Tornadus: open, winderige vlaktes
    ('Route113', 33, 11, 'OBJ_EVENT_GFX_SPECIES(TORNADUS_INCARNATE)', 'Forces_EventScript_Tornadus', 'FLAG_FORCES_HIDE_TORNADUS'),
    ('Route118', 60, 11, 'OBJ_EVENT_GFX_SPECIES(TORNADUS_INCARNATE)', 'Forces_EventScript_Tornadus', 'FLAG_FORCES_HIDE_TORNADUS'),
    ('Route121', 5, 9, 'OBJ_EVENT_GFX_SPECIES(TORNADUS_INCARNATE)', 'Forces_EventScript_Tornadus', 'FLAG_FORCES_HIDE_TORNADUS'),
    # Thundurus: de regenroutes rond het Weather Institute
    ('Route119', 38, 9, 'OBJ_EVENT_GFX_SPECIES(THUNDURUS_INCARNATE)', 'Forces_EventScript_Thundurus', 'FLAG_FORCES_HIDE_THUNDURUS'),
    ('Route120', 8, 7, 'OBJ_EVENT_GFX_SPECIES(THUNDURUS_INCARNATE)', 'Forces_EventScript_Thundurus', 'FLAG_FORCES_HIDE_THUNDURUS'),
    ('Route123', 112, 14, 'OBJ_EVENT_GFX_SPECIES(THUNDURUS_INCARNATE)', 'Forces_EventScript_Thundurus', 'FLAG_FORCES_HIDE_THUNDURUS'),
    # Landorus: berghelling, rotsvlakte bij Meteor Falls, akkers bij Verdanturf
    ('Route112', 28, 9, 'OBJ_EVENT_GFX_SPECIES(LANDORUS_INCARNATE)', 'Forces_EventScript_Landorus', 'FLAG_FORCES_HIDE_LANDORUS'),
    ('Route114', 35, 11, 'OBJ_EVENT_GFX_SPECIES(LANDORUS_INCARNATE)', 'Forces_EventScript_Landorus', 'FLAG_FORCES_HIDE_LANDORUS'),
    ('Route117', 22, 8, 'OBJ_EVENT_GFX_SPECIES(LANDORUS_INCARNATE)', 'Forces_EventScript_Landorus', 'FLAG_FORCES_HIDE_LANDORUS'),
    # Hint-NPC's
    ('FortreeCity', 36, 9, 'OBJ_EVENT_GFX_WOMAN_5', 'Forces_EventScript_HintTornadus', '0'),
    ('Route119_WeatherInstitute_1F', 5, 10, 'OBJ_EVENT_GFX_SCIENTIST_1', 'Forces_EventScript_HintThundurus', '0'),
    ('VerdanturfTown', 16, 9, 'OBJ_EVENT_GFX_OLD_MAN', 'Forces_EventScript_HintLandorus', '0'),
]


def main():
    bymap = {}
    for m, x, y, gfx, script, flag in FORCES:
        bymap.setdefault(m, []).append((x, y, gfx, script, flag))
    for m, items in bymap.items():
        k = Kaart(m)
        mine = {s for _, _, _, s, _ in items}
        others = [o for o in k.d['object_events'] if o['script'] not in mine]
        taken = {(o['x'], o['y']) for o in others} | k.event_tiles()
        objs = []
        for x, y, gfx, script, flag in items:
            assert not k.blocked(x, y), '%s (%d,%d) geblokkeerd' % (m, x, y)
            b = k.beh(x, y)
            assert b in ('MB_NORMAL', 'MB_SHORT_GRASS'), '%s (%d,%d): gedrag %s' % (m, x, y, b)
            assert (x, y) not in taken, '%s (%d,%d) bezet' % (m, x, y)
            # bereikbaar: minstens één vrije buur van dezelfde hoogte die zelf weer verder kan
            r = k.walk((x, y), solid=())
            assert len(r) > 50, '%s (%d,%d) ligt in een klein afgesloten stuk' % (m, x, y)
            elev = k.elev(x, y)
            move = 'MOVEMENT_TYPE_FACE_DOWN' if 'SPECIES' in gfx else 'MOVEMENT_TYPE_LOOK_AROUND'
            objs.append(obj(gfx, x, y, script, elev=elev, move=move, flag=flag))
        # zoals landlib.apply_events (achteraan, idempotent), maar de 16-objectengrens alleen rond onze objecten
        # controleren: Route 123 zit elders al op de grens.
        m_ = json.load(open(k.path))
        m_['object_events'] = [o for o in m_['object_events'] if o['script'] not in mine] + objs
        for o in objs:
            near = [p for p in m_['object_events'] if abs(p['x'] - o['x']) <= 12 and abs(p['y'] - o['y']) <= 9]
            assert len(near) <= 15, '%s: te veel objecten rond (%d,%d)' % (m, o['x'], o['y'])
        open(k.path, 'w').write(json.dumps(m_, indent=2, ensure_ascii=False) + '\n')
        print(m, [(o['x'], o['y'], o['script']) for o in objs])


if __name__ == '__main__':
    main()
