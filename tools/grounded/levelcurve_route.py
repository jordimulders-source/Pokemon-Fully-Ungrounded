"""Levelcurve in looproute: hoofdstuk 1 expliciet, Route 103-oost naar het Wattson-hoofdstuk."""
import sys, statistics
sys.path.insert(0, 'tools/grounded')
import levelcurve as L
D = L.D

CH0 = [  # (kaart, trainers in looproute); 'JOIN'/'SHARE'/'FIRST' zijn gebeurtenissen
    ('FIRST', None),
    ('Route101', []), ('Route103', ['TRAINER_MAY_ROUTE_103_TREECKO']),
    ('Route102', ['TRAINER_CALVIN_1', 'TRAINER_RICK', 'TRAINER_TIANA', 'TRAINER_ALLEN']),
    ('WALLY', None),
    ('Route104', ['TRAINER_BILLY', 'TRAINER_DARIAN', 'TRAINER_CINDY_1', 'TRAINER_SICKBLIK_BEACH']),
    ('PetalburgWoods', ['TRAINER_GRUNT_PETALBURG_WOODS', 'TRAINER_LYLE', 'TRAINER_JAMES_1']),
    ('Route104N', ['TRAINER_HALEY_1', 'TRAINER_WINSTON_1', 'TRAINER_GINA_AND_MIA_1', 'TRAINER_SICKBLIK_ROUTE_104', 'TRAINER_IVAN']),
    ('RustboroCity', ['TRAINER_MAY_RUSTBORO_TREECKO']),
    ('Route116', None), ('RustboroCity_Gym', None),
]

def schedule(trainers):
    s = L.build_schedule(trainers)
    late = [e for e in s[0] if e[0] == 'trainer' and e[2] == 'Route103' and 'ROUTE_103' not in e[1]]
    idx = max(i for i, e in enumerate(s[2]) if e[0] == 'trainer' and e[2] == 'Route110') + 1
    s[2] = s[2][:idx] + late + s[2][idx:]
    wild = D.parse_wild()
    ev = []
    for mp, ts in CH0:
        if mp == 'FIRST':
            ev.append(('wild', 'SPECIES_JIGGLYPUFF', 2)); continue
        if mp == 'WALLY':
            ev.append(('trainer_raw', 'SPECIES_RALTS', 5)); continue
        real = 'Route104' if mp == 'Route104N' else mp
        for g, c, where in L.TEAM[1:]:
            if c == 0 and where == mp:
                wm = L.wild_mons(wild, mp)
                lv = int(sum(r * l for r, l, _ in wm) / sum(r for r, _, _ in wm)) if wm else 5
                ev.append(('join', g, lv))
        if mp == 'PetalburgWoods':
            ev.append(('share', 1))
        wm = L.wild_mons(wild, real) if mp != 'Route104N' else None
        if wm:
            tot = sum(r for r, _, _ in wm)
            for k in range(L.WILD_PER_MAP):
                acc = (k + 0.5) / L.WILD_PER_MAP * tot
                for r, lv, sp in wm:
                    acc -= r
                    if acc <= 0:
                        ev.append(('wild', sp, int(round(lv)))); break
        if ts is None:
            ts = [e[1] for e in s[0] if e[0] in ('trainer', 'boss') and e[2] == mp]
        for t in ts:
            ev.append(('boss' if t == 'TRAINER_ROXANNE_1' else 'trainer', t, mp))
    s[0] = ev
    return s

def team_at(trainers, sched, stop):
    species = D.parse_species()
    sim = L.Sim(species); sim.team.append(L.Mon(L.TEAM[0][0], 5))
    sim.target = max(m['level'] for m in trainers['TRAINER_ROXANNE_1']['mons'])
    for e in sched[0]:
        if e[0] in ('trainer', 'boss') and e[1] == stop:
            return [round(m.flevel, 1) for m in sim.team]
        if e[0] == 'join': sim.team.append(L.Mon(e[1], e[2]))
        elif e[0] == 'share': sim.nshares = e[1]
        elif e[0] in ('wild', 'trainer_raw'): sim.defeat(e[1], e[2], e[0] != 'wild')
        else:
            for m in trainers[e[1]]['mons']: sim.defeat(m['species'], m['level'], True)

if __name__ == '__main__':
    tr = D.parse_party()[0]
    for w in (1, 2, 3, 4, 6):
        L.WILD_PER_MAP = w
        s = schedule(tr)
        print(w, 'vóór Billy:', team_at(tr, s, 'TRAINER_BILLY'), ' vóór Roxanne:', team_at(tr, s, 'TRAINER_ROXANNE_1'))
