"""Project Grounded: liefdesdagen met Enamorus (post-game, src/enamorus.c + data/scripts/enamorus.inc).

Zet per stadje Enamorus (FLAG_ENAMORUS_HIDE), een verliefd koppel en Prof. Birch met zijn drol (FLAG_LOVEDAY_HIDE)
achteraan object_events. src/enamorus.c zet of wist die flags bij elke binnenkomst. Idempotent; controleert vrije
tegels, of alle warps en kaartranden bereikbaar blijven met de nieuwe objecten erbij, en de 16-objectengrens.
Draaien vanuit de root van de repo: python3 tools/grounded/maptools/enamorus_towns.py
"""
import json
import sys
sys.path.insert(0, 'tools/grounded/maptools')
from landlib import Kaart, obj

ENA = ('OBJ_EVENT_GFX_SPECIES(ENAMORUS_INCARNATE)', 'Enamorus_EventScript_Enamorus', 'FLAG_ENAMORUS_HIDE', 'MOVEMENT_TYPE_FACE_DOWN')
L, R = 'MOVEMENT_TYPE_FACE_LEFT', 'MOVEMENT_TYPE_FACE_RIGHT'
LOVE = 'FLAG_LOVEDAY_HIDE'


def town(couple_a, couple_b, script, birch, enamorus):
    """couple_* = (gfx, x, y); birch = (x, y): de drol ligt rechts van hem; enamorus = (x, y)."""
    (ga, xa, ya), (gb, xb, yb) = couple_a, couple_b
    bx, by = birch
    return [
        ('OBJ_EVENT_GFX_' + ga, xa, ya, script, LOVE, R),
        ('OBJ_EVENT_GFX_' + gb, xb, yb, script, LOVE, L),
        ('OBJ_EVENT_GFX_PROF_BIRCH', bx, by, 'Enamorus_EventScript_Birch', LOVE, R),
        ('OBJ_EVENT_GFX_TURD', bx + 1, by, 'Enamorus_EventScript_Turd', LOVE, 'MOVEMENT_TYPE_FACE_DOWN'),
        (ENA[0], enamorus[0], enamorus[1], ENA[1], ENA[2], ENA[3]),
    ]


TOWNS = {
    'OldaleTown': town(('OLD_MAN', 3, 13), ('OLD_WOMAN', 4, 13), 'Enamorus_EventScript_OldaleCouple', (10, 17), (13, 3)),
    'DewfordTown': town(('SAILOR', 2, 13), ('BEAUTY', 3, 13), 'Enamorus_EventScript_DewfordCouple', (13, 16), (16, 17)),
    'FallarborTown': town(('HIKER', 16, 10), ('PICNICKER', 17, 10), 'Enamorus_EventScript_FallarborCouple', (3, 13), (12, 17)),
    'LavaridgeTown': town(('PSYCHIC_M', 14, 9), ('HEX_MANIAC', 15, 9), 'Enamorus_EventScript_LavaridgeCouple', (11, 10), (16, 17)),
}
MINE = {'Enamorus_EventScript_Enamorus', 'Enamorus_EventScript_Birch', 'Enamorus_EventScript_Turd',
        'Enamorus_EventScript_OldaleCouple', 'Enamorus_EventScript_DewfordCouple',
        'Enamorus_EventScript_FallarborCouple', 'Enamorus_EventScript_LavaridgeCouple'}


def targets(k):
    """Warps en open randtegels: die moeten bereikbaar blijven."""
    t = {(w['x'], w['y']) for w in k.d['warp_events']}
    for x in range(k.w):
        for y in (0, k.h - 1):
            if not k.blocked(x, y): t.add((x, y))
    for y in range(k.h):
        for x in (0, k.w - 1):
            if not k.blocked(x, y): t.add((x, y))
    return t


def main():
    for m, items in TOWNS.items():
        k = Kaart(m)
        others = [o for o in k.d['object_events'] if o['script'] not in MINE]
        taken = {(o['x'], o['y']) for o in others} | k.event_tiles()
        start = next(((w['x'], w['y'] + 1) for w in k.d['warp_events'] if not k.blocked(w['x'], w['y'] + 1)), None)
        olds = {(o['x'], o['y']) for o in others}
        before = k.walk(start, solid=olds)
        new = {(x, y) for _, x, y, _, _, _ in items}
        after = k.walk(start, solid=new | olds)
        for t in targets(k):
            if t in before:
                # een warp-/randtegel mag naast een object liggen, maar moet nog te bereiken zijn
                assert t in after or any((t[0] + dx, t[1] + dy) in after for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))), \
                    '%s: %s niet meer bereikbaar' % (m, t)
        objs = []
        for gfx, x, y, script, flag, move in items:
            assert not k.blocked(x, y), '%s (%d,%d) geblokkeerd' % (m, x, y)
            b = k.beh(x, y)
            assert b in ('MB_NORMAL', 'MB_SHORT_GRASS', 'MB_SAND'), '%s (%d,%d): gedrag %s' % (m, x, y, b)
            assert (x, y) not in taken, '%s (%d,%d) bezet' % (m, x, y)
            assert (x, y) in k.walk(start), '%s (%d,%d) niet bereikbaar' % (m, x, y)
            objs.append(obj(gfx, x, y, script, elev=k.elev(x, y), move=move, flag=flag))
        m_ = json.load(open(k.path))
        m_['object_events'] = [o for o in m_['object_events'] if o['script'] not in MINE] + objs
        # kleine stadjes: alles staat tegelijk in beeld (+ speler + volger; Fallarbor ook de Burglar: 2 extra)
        assert len(m_["object_events"]) + 2 + (2 if m == "FallarborTown" else 0) <= 16, '%s: te veel objecten (%d)' % (m, len(m_['object_events']))
        open(k.path, 'w').write(json.dumps(m_, indent=2, ensure_ascii=False) + '\n')
        print(m, len(m_['object_events']), [(o['x'], o['y'], o['script'][19:]) for o in objs])


if __name__ == '__main__':
    main()
