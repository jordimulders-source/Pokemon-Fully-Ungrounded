import sys, json, statistics
"""Gebruik: python3 tools/grounded/levelcurve_smooth.py <delta.json>  (droge run: per trainer het nieuwe ace-level; toepassen deed apply2.py in de sessie van 12 okt, zie CHANGELOG)."""
sys.path.insert(0, "tools/grounded")
import levelcurve as L
import levelcurve_route as C
D = L.D
L.WILD_PER_MAP = 2
CAL = 1.5                       # simulatie − reguliere speler (Jordi: na Petalburg 9–10)
ROUTE_OFF, GYMTR_OFF, BOSS_OFF = 0.0, 1.0, 2.5
SKIP = {'TRAINER_MAY_ROUTE_103_TREECKO'} | set(L.FIXED_ACE) | L.JOKES
trainers = D.parse_party()[0]; species = D.parse_species()
sched = C.schedule(trainers)
def ace(t): return max(m['level'] for m in trainers[t]['mons'])
delta = {}; log = []
sim = L.Sim(species); sim.team.append(L.Mon(L.TEAM[0][0], 5))
for ci, ev in enumerate(sched):
    b = next(e[1] for e in ev if e[0] == 'boss')
    tb = 'TRAINER_CHAMPION_STEVEN' if b == 'TRAINER_DRAKE' else b
    tops = [ace(e[1]) for e in ev if e[0] == 'trainer']
    med = statistics.median(tops) if tops else 0
    for e in ev:
        sim.target = ace(tb) + delta.get(tb, 0)
        if e[0] == 'join': sim.team.append(L.Mon(e[1], e[2])); continue
        if e[0] == 'share': sim.nshares = e[1]; continue
        if e[0] in ('wild', 'trainer_raw'): sim.defeat(e[1], e[2], e[0] != 'wild'); continue
        t = e[1]
        R = sim.snapshot()['avg'] - CAL
        keep = t in SKIP or L.is_joke(trainers, t, ci) or (e[0] == 'trainer' and t not in L.STORY and ace(t) < med - L.LOW_MARGIN)
        if not keep:
            off = BOSS_OFF if (e[0] == 'boss' or t in L.STORY) else GYMTR_OFF if '_Gym' in e[2] else ROUTE_OFF
            delta[t] = int(round(R + off)) - ace(t)
            log.append((ci, t, e[0], ace(t), ace(t) + delta[t], R))
        for m in trainers[t]['mons']:
            sim.defeat(m['species'], min(100, max(2, m['level'] + delta.get(t, 0))), True)
json.dump({k: v for k, v in delta.items() if v}, open(sys.argv[1], "w"))
cur = None
for ci, t, kind, a0, a1, R in log:
    if ci != cur:
        cur = ci; print('==', L.CHAPTERS[ci][0])
    print(f'  {t[8:]:28} {a0:3} -> {a1:3}  (speler {R:5.1f}){" BOSS" if kind == "boss" or t in L.STORY else ""}')
