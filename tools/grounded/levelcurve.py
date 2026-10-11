#!/usr/bin/env python3
"""Project Grounded: levelcurve-simulatie van een reguliere playthrough.

Gebruik:
  python3 tools/grounded/levelcurve.py                 # tabel per mijlpaal
  python3 tools/grounded/levelcurve.py --plot uit.png  # plus grafiek (matplotlib)
  python3 tools/grounded/levelcurve.py --json uit.json

Model (zie LEVELCURVE.md):
- Volgorde = het Emerald-verhaal in hoofdstukken (CHAPTERS), elk eindigt bij een mijlpaal.
- Alle trainers op de kaarten van het hoofdstuk (uit data/maps/*/scripts.inc, zonder
  rematches) worden verslagen, mits hun mediaan-level <= ace van de mijlpaal + GATE;
  hogere trainers (watertrainers op vroege routes) schuiven door naar het eerste hoofdstuk
  waar dat wel geldt. Mediaan > kampioen of POSTGAME = post-game, telt niet mee.
- Per kaart met wilde Pokémon WILD_PER_MAP wilde gevechten (gemiddelde van de tabel).
- EXP zoals de engine (B_SCALED_EXP GEN_5, B_SPLIT_EXP GEN_5, trainer x1.5, vastgehouden
  Exp. Share: helft voor de vechter(s), helft verdeeld over de houders; per ontvanger
  geschaald met ((2L+10)/(L+Lp+10))^2.5).
- Team van 6 dat stap voor stap groeit (TEAM), twee Exp. Shares (Birch voor gym 1,
  Mr. Stone na de brief), strategieën 'evenwichtig' en 'ace'.
"""
import argparse
import json
import math
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(__file__))
import levelcurve_data as D  # noqa: E402

GATE = 3
WILD_PER_MAP = 6
TRAINER_MULT = 0.5   # B_TRAINER_EXP_PERCENT (was 1.5: B_TRAINER_EXP_MULTIPLIER GEN_7)
WILD_MULT = 1.0
CATCHUP = True        # B_GROUNDED_CATCHUP_EXP
CATCHUP_STEP = 100    # B_CATCHUP_EXP_STEP: procent extra EXP per level onder de ace van de volgende mijlpaal
CATCHUP_MAX = 900     # B_CATCHUP_EXP_MAX
LAND_RATES = [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]

# (naam, [kaarten], mijlpaal-trainer)
CHAPTERS = [
    ('Roxanne', ['Route101', 'Route103', 'Route102', 'Route104', 'PetalburgWoods', 'RustboroCity',
                 'Route116', 'RustboroCity_Gym'], 'TRAINER_ROXANNE_1'),
    ('Brawly', ['RusturfTunnel', 'DewfordTown', 'Route106', 'GraniteCave_1F', 'GraniteCave_B1F',
                'DewfordTown_Gym'], 'TRAINER_BRAWLY_1'),
    ('Wattson', ['Route109', 'Route109_SeashoreHouse', 'SlateportCity', 'SlateportCity_OceanicMuseum_2F',
                 'Route110', 'MauvilleCity', 'Route117', 'MauvilleCity_Gym'], 'TRAINER_WATTSON_1'),
    ('Flannery', ['VerdanturfTown', 'Route111', 'Route112', 'FieryPath', 'Route113', 'Route114',
                  'MeteorFalls_1F_1R', 'Route115', 'MtChimney', 'MtChimney_Summit', 'JaggedPass', 'JaggedPass_LavaTube',
                  'LavaridgeTown_Gym_1F'], 'TRAINER_FLANNERY_1'),
    ('Norman', ['PetalburgCity', 'PetalburgCity_Gym'], 'TRAINER_NORMAN_1'),
    ('Winona', ['Route105', 'Route107', 'Route108', 'AbandonedShip_Corridors_1F', 'AbandonedShip_Rooms_1F',
                'AbandonedShip_Corridors_B1F', 'AbandonedShip_Rooms2_1F', 'Route118', 'Route119',
                'Route119_WeatherInstitute_1F', 'Route119_WeatherInstitute_2F', 'FortreeCity', 'Route120',
                'FortreeCity_Gym'], 'TRAINER_WINONA_1'),
    ('Tate & Liza', ['Route121', 'Route122', 'MtPyre_1F', 'MtPyre_2F', 'MtPyre_3F', 'MtPyre_4F', 'MtPyre_5F',
                     'MtPyre_6F', 'MtPyre_Summit', 'Route123', 'LilycoveCity', 'MagmaHideout_1F',
                     'MagmaHideout_2F_1R', 'MagmaHideout_2F_2R', 'MagmaHideout_2F_3R', 'MagmaHideout_3F_1R',
                     'MagmaHideout_3F_2R', 'MagmaHideout_4F', 'AquaHideout_1F', 'AquaHideout_B1F',
                     'AquaHideout_B2F', 'Route124', 'MossdeepCity', 'Route125', 'ShoalCave_LowTideEntranceRoom',
                     'ShoalCave_LowTideIceRoom', 'ShoalCave_LowTideInnerRoom', 'MossdeepCity_Gym'],
     'TRAINER_TATE_AND_LIZA_1'),
    ('Wallace', ['MossdeepCity_SpaceCenter_1F', 'MossdeepCity_SpaceCenter_2F', 'Route127', 'Route128',
                 'Underwater_Route128', 'SeafloorCavern_Room1', 'SeafloorCavern_Room2', 'SeafloorCavern_Room3',
                 'SeafloorCavern_Room4', 'SeafloorCavern_Room9', 'SootopolisCity', 'Route126',
                 'Underwater_Route126', 'CaveOfOrigin_1F', 'Route129', 'Route130', 'Route131',
                 'SkyPillar_Outside', 'Route132', 'Route133', 'Route134', 'SootopolisCity_Gym_B1F',
                 'SootopolisCity_Gym_1F'], 'TRAINER_WALLACE_1'),
    ('Elite Four', ['EverGrandeCity', 'VictoryRoad_1F', 'VictoryRoad_B1F', 'VictoryRoad_B2F',
                    'VictoryRoad_WaitingRoom', 'EverGrandeCity_SidneysRoom', 'EverGrandeCity_PhoebesRoom',
                    'EverGrandeCity_GlaciasRoom', 'EverGrandeCity_DrakesRoom'], 'TRAINER_DRAKE'),
    ('Kampioen', ['EverGrandeCity_ChampionsRoom'], 'TRAINER_CHAMPION_STEVEN'),
]

# tussentijdse story-gevechten die als mijlpaal in de tabel komen
STORY = ['TRAINER_MAY_ROUTE_103_TREECKO', 'TRAINER_MAY_RUSTBORO_TREECKO', 'TRAINER_MAY_ROUTE_110_TREECKO',
         'TRAINER_WALLY_MAUVILLE', 'TRAINER_BIRCH_VERDANTURF', 'TRAINER_WALLY_METEOR_FALLS',
         'TRAINER_MAXIE_MT_CHIMNEY', 'TRAINER_DAVE_PETALBURG', 'TRAINER_MAY_ROUTE_119_TREECKO',
         'TRAINER_WALLY_MT_PYRE', 'TRAINER_MAY_LILYCOVE_TREECKO', 'TRAINER_MAXIE_MAGMA_HIDEOUT',
         'TRAINER_MATT', 'TRAINER_MAXIE_MOSSDEEP', 'TRAINER_ARCHIE', 'TRAINER_MAXIE_SOOTOPOLIS',
         'TRAINER_ZINNIA', 'TRAINER_WALLY_VR_1', 'TRAINER_SIDNEY', 'TRAINER_PHOEBE', 'TRAINER_GLACIA']

# post-game of rematch-achtig, ook al staat het op een kaart van het hoofdpad
POSTGAME = {'TRAINER_WALLY_VR_2', 'TRAINER_ZINNIA_DELTA', 'TRAINER_NONE',
            'TRAINER_RIVAL_POSTGAME_TREECKO', 'TRAINER_RIVAL_POSTGAME_TORCHIC', 'TRAINER_RIVAL_POSTGAME_MUDKIP'} | {
    f'TRAINER_{w}_SERVICE_{i}' for w in ('ARCHIE', 'MAXIE') for i in range(1, 5)}

# team: (groeicurve, hoofdstuk-index waarin hij erbij komt, kaart waar hij gevangen wordt)
TEAM = [('GROWTH_MEDIUM_SLOW', 0, None),          # starter lv 5
        ('GROWTH_MEDIUM_FAST', 0, 'Route102'),
        ('GROWTH_MEDIUM_FAST', 0, 'PetalburgWoods'),
        ('GROWTH_MEDIUM_SLOW', 1, 'GraniteCave_1F'),
        ('GROWTH_MEDIUM_FAST', 2, 'Route110'),
        ('GROWTH_SLOW', 3, 'Route111')]


def exp_for_level(growth, n):
    if n <= 1:
        return 0
    if growth == 'GROWTH_MEDIUM_FAST':
        return n ** 3
    if growth == 'GROWTH_MEDIUM_SLOW':
        return int(6 * n ** 3 / 5 - 15 * n ** 2 + 100 * n - 140)
    if growth == 'GROWTH_SLOW':
        return 5 * n ** 3 // 4
    if growth == 'GROWTH_FAST':
        return 4 * n ** 3 // 5
    if growth == 'GROWTH_ERRATIC':
        if n <= 50:
            return n ** 3 * (100 - n) // 50
        if n <= 68:
            return n ** 3 * (150 - n) // 100
        if n <= 98:
            return n ** 3 * ((1911 - 10 * n) // 3) // 500
        return n ** 3 * (160 - n) // 100
    if growth == 'GROWTH_FLUCTUATING':
        if n <= 15:
            return n ** 3 * ((n + 1) // 3 + 24) // 50
        if n <= 36:
            return n ** 3 * (n + 14) // 50
        return n ** 3 * (n // 2 + 32) // 50
    return n ** 3


class Mon:
    def __init__(self, growth, level):
        self.growth = growth
        self.level = level
        self.exp = exp_for_level(growth, level)

    def gain(self, amount):
        self.exp += amount
        while self.level < 100 and self.exp >= exp_for_level(self.growth, self.level + 1):
            self.level += 1

    @property
    def flevel(self):
        """level met fractie (voor de grafiek)."""
        if self.level >= 100:
            return 100.0
        lo, hi = exp_for_level(self.growth, self.level), exp_for_level(self.growth, self.level + 1)
        return self.level + (self.exp - lo) / max(1, hi - lo)


def scale(base, foe_lv, my_lv):
    v = base * ((2 * foe_lv + 10) ** 2.5) / ((foe_lv + my_lv + 10) ** 2.5)
    return int(v) + 1


class Sim:
    def __init__(self, species, strategy='evenwichtig', shares=True):
        self.sp = species
        self.strategy = strategy
        self.shares = shares
        self.team = []
        self.chapter = 0
        self.nshares = 0
        self.target = 0   # ace van de volgende mijlpaal (inhaal-EXP)

    def catchup(self, amount, my_lv):
        """B_GROUNDED_CATCHUP_EXP: onder het doel +CATCHUP_STEP% per level achterstand, max. +CATCHUP_MAX%."""
        if CATCHUP and my_lv < self.target:
            return amount * (100 + min(CATCHUP_MAX, CATCHUP_STEP * (self.target - my_lv))) // 100
        return amount

    def yield_of(self, const):
        if const in self.sp:
            return self.sp[const]['yield']
        for k, v in self.sp.items():
            if k.startswith(const + '_'):
                return v['yield']
        return 150

    def defeat(self, species, level, trainer):
        if not self.team:
            return
        base = self.yield_of(species) * level // 5
        if trainer:
            base = int(base * TRAINER_MULT)
        else:
            base = int(base * WILD_MULT)
        lv_sorted = sorted(range(len(self.team)), key=lambda i: self.team[i].level)
        if self.strategy == 'ace':
            fighter = 0
        else:
            fighter = lv_sorted[0] if len(self.team) > 1 else 0
            # de zwakste vecht niet als hij > 8 levels onder de tegenstander zit: dan vecht de sterkste
            if self.team[fighter].level < level - 8:
                fighter = lv_sorted[-1]
        holders = [i for i in lv_sorted if i != fighter][:self.nshares] if self.shares else []
        if holders:
            fexp = max(1, base // 2)
            sexp = max(1, base // 2 // len(holders))
        else:
            fexp, sexp = max(1, base), 0
        self.team[fighter].gain(self.catchup(scale(fexp, level, self.team[fighter].level), self.team[fighter].level))
        for h in holders:
            self.team[h].gain(self.catchup(scale(sexp, level, self.team[h].level), self.team[h].level))

    def snapshot(self):
        lv = [m.flevel for m in self.team]
        top6 = sorted(lv)[-6:]
        return {'avg': sum(lv) / len(lv), 'max': max(lv), 'min': min(lv), 'n': len(lv), 'top6': sum(top6) / len(top6)}


def wild_mons(wild, mapname):
    const = D.map_const(mapname)
    d = wild.get(const)
    if not d:
        return None
    mons = d.get('land_mons') or d.get('water_mons')
    if not mons:
        return None
    rates = LAND_RATES if len(mons) == 12 else [1] * len(mons)
    return [(r, (a + b) / 2, s) for r, (a, b, s) in zip(rates, mons)]


def build_schedule(trainers=None, extra=None, team=None, postgame=False):
    """Volgorde van alle gevechten: per hoofdstuk een lijst ('wild'|'trainer'|'join'|'share', ...).
    extra: {hoofdstuk: [kaarten]} (zijgebieden, profiel completionist); team: TEAM of TEAM_ROTATIE;
    postgame: na de kampioen ook de post-game (POST_MAPS, oplopend) en de superbosses."""
    trainers = trainers or D.parse_party()[0]
    team = team or TEAM
    extra = extra or {}
    wild = D.parse_wild()
    champ_ace = max(m['level'] for m in trainers['TRAINER_CHAMPION_STEVEN']['mons'])

    def median(t):
        return statistics.median([m['level'] for m in trainers[t]['mons']])

    pending, beaten, sched = [], set(), []
    for ci, (name, maps, boss) in enumerate(CHAPTERS):
        gate = max(m['level'] for m in trainers[boss]['mons']) + GATE
        ev = []
        maps = maps[:-1] + extra.get(ci, []) + maps[-1:]
        for mp in maps:
            for g, c, where in team[1:]:
                if c == ci and where == mp:
                    wm = wild_mons(wild, mp)
                    lv = int(sum(r * l for r, l, _ in wm) / sum(r for r, _, _ in wm)) if wm else 5
                    ev.append(('join', g, lv))
            if ci == 0 and mp == 'PetalburgWoods':
                ev.append(('share', 1))
            if ci == 2 and mp == 'SlateportCity':
                ev.append(('share', 2))
            wm = wild_mons(wild, mp)
            if wm:
                tot = sum(r for r, _, _ in wm)
                for k in range(WILD_PER_MAP):
                    acc = (k + 0.5) / WILD_PER_MAP * tot
                    for r, lv, s in wm:
                        acc -= r
                        if acc <= 0:
                            ev.append(('wild', s, int(round(lv))))
                            break
            for t in D.dedup_rival(D.map_trainers(mp)):
                if t in POSTGAME or t not in trainers or not trainers[t]['mons'] or t in beaten or t == boss:
                    continue
                if median(t) > champ_ace and t not in STORY:
                    beaten.add(t)
                    continue
                if median(t) <= gate or t in STORY:
                    ev.append(('trainer', t, mp))
                    beaten.add(t)
                elif t not in [x for x, _ in pending]:
                    pending.append((t, mp))
        for t, mp in list(pending):
            if median(t) <= gate:
                ev.append(('trainer', t, mp))
                beaten.add(t)
                pending.remove((t, mp))
        ev.append(('boss', boss, maps[-1]))
        beaten.add(boss)
        sched.append(ev)
    if postgame:
        post = []
        for mp in POST_MAPS:
            for t in D.dedup_rival(D.map_trainers(mp)):
                if t in trainers and trainers[t]['mons'] and t not in beaten and t not in post:
                    post.append(t)
        for name in GYM_REMATCH_NAMES:
            for i in range(2, 6):
                if f'TRAINER_{name}_{i}' in trainers:
                    post.append(f'TRAINER_{name}_{i}')
        post += [t for t in POST_TRAINERS if t in trainers and t not in post]
        def top(t):
            return max(m['level'] for m in trainers[t]['mons'])
        post.sort(key=top)
        ev = [('trainer', t, 'post') for t in post if top(t) < 100]
        supers = [t for t in post if top(t) >= 100]
        ev.append(('boss', supers[0], 'post'))
        ev += [('trainer', t, 'post') for t in supers[1:]]
        sched.append(ev)
    return sched


_SPECIES = None


def simulate(sched, trainers, delta=None, strategy='evenwichtig', shares=True):
    """delta: dict trainer -> levelverschuiving (of None)."""
    global _SPECIES
    if _SPECIES is None:
        _SPECIES = D.parse_species()
    species = _SPECIES
    delta = delta or {}
    sim = Sim(species, strategy, shares)
    sim.team.append(Mon(TEAM[0][0], 5))
    rows = []
    for ci, ev in enumerate(sched):
        foes = []
        b = next(e[1] for e in ev if e[0] == 'boss')
        if b == 'TRAINER_DRAKE':   # na badge 8 is het doel de kampioen (de E4 is één reeks)
            b = 'TRAINER_CHAMPION_STEVEN'
        sim.target = max(min(100, max(2, m['level'] + delta.get(b, 0))) for m in trainers[b]['mons'])
        for e in ev:
            if e[0] == 'join':
                sim.team.append(Mon(e[1], e[2]))
            elif e[0] == 'share':
                if shares:
                    sim.nshares = e[1]
            elif e[0] == 'wild':
                sim.defeat(e[1], e[2], False)
            else:
                t = e[1]
                lv = [min(100, max(2, m["level"] + delta.get(t, 0))) for m in trainers[t]["mons"]]
                if e[0] == 'boss' or t in STORY:
                    row = dict(chapter=ci, name=t, ace=max(lv), **sim.snapshot())
                    if e[0] == 'boss':
                        row['milestone'] = CHAPTERS[ci][0] if ci < len(CHAPTERS) else "Superbosses"
                        row['foes'] = statistics.median(foes) if foes else 0
                        row['nfoes'] = len(foes)
                    rows.append(row)
                if e[0] == 'trainer' and '_Gym' not in e[2] and t not in STORY and t not in E4:
                    foes.append(sim.snapshot()['avg'] - max(lv))
                for m, l in zip(trainers[t]['mons'], lv):
                    sim.defeat(m['species'], l, True)
    return rows


def run(strategy='evenwichtig', shares=True, delta=None, profile='hoofdpad', postgame=False):
    trainers = D.parse_party()[0]
    if profile == 'completionist':
        sched = build_schedule(trainers, extra=SIDE_BY_CHAPTER, team=TEAM_ROTATIE, postgame=postgame)
    elif profile == 'compleet6':
        sched = build_schedule(trainers, extra=SIDE_BY_CHAPTER, postgame=postgame)
    else:
        sched = build_schedule(trainers, postgame=postgame)
    return simulate(sched, trainers, delta, strategy, shares)


# profiel completionist: ook alle zijgebieden vóór de E4, met een rotatie van 12 Pokémon
SIDE_BY_CHAPTER = {
    1: ['ToadstoolHollow'],
    3: ['Route112_Dojo', 'Route112_TowerOfDarkness', 'Route112_TowerOfWaters'],
    5: ['FortreeJungle', 'MangroveMire', 'RocketHideout_1F', 'RocketHideout_B1F', 'RocketHideout_B2F',
        'ScorchedSlab_SunHall', 'ScorchedSlab_Spring', 'ScorchedSlab_Sanctum', 'Route135', 'Route136'],
    7: ['BeaconIsle', 'BeaconIsle_Lighthouse_1F', 'BeaconIsle_Lighthouse_2F', 'BeaconIsle_Lighthouse_Top',
        'BeaconIsle_Grotto', 'GhostShip_Deck', 'GhostShip_Corridors', 'GhostShip_Cabins', 'GhostShip_CaptainsOffice',
        'ShipwreckShoals', 'Route126_CoralCathedral', 'Route126_HermitCrater', 'WhirlIsland', 'Underwater_Route105',
        'Underwater_Route124', 'Underwater_Route125', 'Underwater_Route127_Trench'],
    8: ['MeteorFalls_1F_2R', 'MeteorFalls_B1F_2R', 'MeteorFalls_Tunnels', 'MeteorFalls_DraconidShrine',
        'VictoryRoad_Hermit'],
}
TEAM_ROTATIE = TEAM + [('GROWTH_MEDIUM_FAST', 2, 'Route117'), ('GROWTH_MEDIUM_SLOW', 3, 'Route113'),
                       ('GROWTH_MEDIUM_FAST', 5, 'Route119'), ('GROWTH_SLOW', 5, 'Route120'),
                       ('GROWTH_MEDIUM_FAST', 6, 'Route123'), ('GROWTH_MEDIUM_SLOW', 7, 'Route128')]
# post-game (na de kampioen): kaarten, losse trainers en gymleider-rematches
POST_MAPS = ['Route119_WeatherInstitute_1F', 'SSTidalRooms', 'SSTidalLowerDeck', 'TaoIsland', 'TaoIsland_Den',
             'TaoIsland_Tower2F', 'TaoIsland_Tower3F', 'DesertUnderpass', 'PokemonTower_2F', 'PokemonTower_3F',
             'PokemonTower_4F', 'PokemonTower_5F', 'MegaForest', 'NothingIsland', 'CeruleanCave_1F',
             'CeruleanCave_2F', 'CeruleanCave_B1F', 'ChargestoneCave_1F', 'ChargestoneCave_B1F',
             'ChargestoneCave_B2F', 'NationalPark', 'PlasmaFrigate_Corridor', 'PlasmaFrigate_Hold', 'TapuIsle',
             'LibertyGarden', 'MirageBazaar', 'ParadisoResort', 'ParadisoResort_Bar', 'ParadisoResort_Lobby',
             'MeteorFalls_StevensCave', 'TaoIsland_FrostHollow']
POST_TRAINERS = ['TRAINER_ZINNIA_DELTA'] + [f'TRAINER_WALLY_VR_{i}' for i in range(2, 6)]
GYM_REMATCH_NAMES = ('ROXANNE', 'BRAWLY', 'WATTSON', 'FLANNERY', 'NORMAN', 'WINONA', 'TATE_AND_LIZA', 'WALLACE')


E4 = ('TRAINER_SIDNEY', 'TRAINER_PHOEBE', 'TRAINER_GLACIA', 'TRAINER_DRAKE', 'TRAINER_CHAMPION_STEVEN')
# ankerpunten van Jordi (9 okt): E4 rond 80, Steven ace 84
FIXED_ACE = {'TRAINER_SIDNEY': 78, 'TRAINER_PHOEBE': 79, 'TRAINER_GLACIA': 80, 'TRAINER_DRAKE': 81,
             'TRAINER_CHAMPION_STEVEN': 84}
BOSS_TARGET = 1.5    # teamgemiddelde hooguit zoveel boven de ace van een gymleider/E4/kampioen
STORY_TARGET = 2.5   # idem voor rivalen, Wally, Maxie/Archie, Birch, Dave
ROUTE_TARGET = 3.0   # mediaan (teamgemiddelde − ace) van de gewone trainers in een hoofdstuk
ROUTE_TARGET_E4 = 0.0  # Victory Road: trainers op spelerniveau, zodat de speler naar de E4 toe groeit


JOKES = {'TRAINER_IVAN', 'TRAINER_LYLE'}   # bewust lage grap-teams (CLAUDE.md)
LOW_MARGIN = 8       # team > 8 levels onder de rest van het hoofdstuk = bewust laag (bijv. Keccles op Route 115)


def is_joke(trainers, t, ci):
    lv = [m['level'] for m in trainers[t]['mons']]
    return t in JOKES or max(lv) - min(lv) >= 10   # grap-teams (levelspreiding >= 10) blijven staan


def classify(sched, trainers):
    """per hoofdstuk: (routegroep, [(sleutel, groep)]). Grap- en bewust lage teams vallen erbuiten."""
    out = []
    for ci, ev in enumerate(sched):
        route, keys, gym = [], [], []
        tops = [max(m['level'] for m in trainers[e[1]]['mons']) for e in ev if e[0] == 'trainer']
        med = statistics.median(tops) if tops else 0
        for e in ev:
            if e[0] == 'boss' or (e[0] == 'trainer' and (e[1] in STORY or e[1] in E4)):
                keys.append(e[1])
            elif e[0] == 'trainer':
                if is_joke(trainers, e[1], ci):
                    continue
                if max(m['level'] for m in trainers[e[1]]['mons']) < med - LOW_MARGIN:
                    continue
                (gym if '_Gym' in e[2] else route).append(e[1])
        out.append((route, [(k, [k] + (gym if k == CHAPTERS[ci][2] else [])) for k in keys]))
    return out


def solve(sched, trainers):
    """Schaalregel per hoofdstuk (zie LEVELCURVE.md), alleen omhoog:
    1. gewone trainers +r tot de mediaan van (teamgemiddelde − ace) <= ROUTE_TARGET;
    2. elk sleutelgevecht +d tot teamgemiddelde − ace <= BOSS_TARGET (gym/E4/kampioen) of STORY_TARGET;
       gymtrainers krijgen dezelfde +d als hun leider. Grap-trainers vroeg in de game blijven staan.
    """
    delta = {}
    groups = classify(sched, trainers)

    def rows():
        return simulate(sched, trainers, delta)

    for ci, (route, keys) in enumerate(groups):
        r = 0
        if route:
            for r in range(0, 31):
                for t in route:
                    delta[t] = r
                ms = [x for x in rows() if x.get('milestone')][ci]
                if ms['foes'] <= (ROUTE_TARGET_E4 if CHAPTERS[ci][2] == 'TRAINER_DRAKE' else ROUTE_TARGET):
                    break
        for k, grp in keys:
            target = BOSS_TARGET if (k in E4 or k == CHAPTERS[ci][2]) else STORY_TARGET
            ace0 = max(m['level'] for m in trainers[k]['mons'])
            if k in FIXED_ACE:   # ankerpunten (Jordi): E4 rond 80, Steven 84
                delta[k] = FIXED_ACE[k] - ace0
                continue
            for d in range(-20 if k in STORY else 0, 31):
                delta[k] = d
                for t in grp[1:]:
                    # gymtrainers: minstens +d, liefst +r (zoals de routes), maar max. ace − 2
                    top = max(m['level'] for m in trainers[t]['mons'])
                    delta[t] = max(d, min(r, ace0 + d - 2 - top))
                g = next(x for x in rows() if x['name'] == k)
                if g['avg'] - g['ace'] <= target:
                    break
    return {k: v for k, v in delta.items() if v}


# zijgebieden (niet op het hoofdpad) die met hun regio meeschuiven: kaart -> hoofdstuk-index
SIDE_SHIFT = {'ToadstoolHollow': 1,
              'Route112_Dojo': 3, 'Route112_TowerOfDarkness': 3, 'Route112_TowerOfWaters': 3,
              'FortreeJungle': 5, 'MangroveMire': 5, 'RocketHideout_1F': 5, 'RocketHideout_B1F': 5,
              'RocketHideout_B2F': 5, 'ScorchedSlab_SunHall': 5, 'ScorchedSlab_Spring': 5,
              'ScorchedSlab_Sanctum': 5}
STARTERS = ('TREECKO', 'TORCHIC', 'MUDKIP')


def expand_delta(delta, sched, trainers):
    """Verschuiving per trainer -> ook rivaal-varianten, rematches (_2.._5) en zijgebieden."""
    out = dict(delta)
    leaders = {b for _, _, b in CHAPTERS}
    for t, d in delta.items():
        m = re.match(r'TRAINER_(MAY|BRENDAN)_(\w+)_(TREECKO|TORCHIC|MUDKIP)$', t)
        if m:
            for who in ('MAY', 'BRENDAN'):
                for s in STARTERS:
                    v = f'TRAINER_{who}_{m.group(2)}_{s}'
                    if v in trainers:
                        out[v] = d
        if t.endswith('_1') and t not in leaders:
            for i in range(2, 6):
                r = t[:-2] + f'_{i}'
                if r in trainers:
                    out[r] = d
    groups = classify(sched, trainers)
    for mp, ci in SIDE_SHIFT.items():
        route = groups[ci][0]
        d = delta.get(route[0], 0) if route else 0
        for t in D.map_trainers(mp):
            if t in trainers and t not in out and not is_joke(trainers, t, ci):
                out[t] = d
    return {k: v for k, v in out.items() if v}


def apply(delta, trainers, lines, protect=()):
    """Schrijft de verschuivingen in trainers.party; evolueert waar het nieuwe level dat vraagt."""
    species = D.parse_species()
    evolved = []
    for t, d in sorted(delta.items()):
        for mon in trainers[t]['mons']:
            old = mon['level']
            if mon['species'] == 'SPECIES_MAGIKARP':   # Magikarp-levels niet aanpassen (CLAUDE.md)
                continue
            new = min(100, max(2, old + d))
            lines[mon['lineno']] = re.sub(r'Level:\s*\d+', f'Level: {new}', lines[mon['lineno']])
            spline = lines[mon['spline']]
            if 'Eviolite' in spline or t in protect or re.sub(r'_\d+$', '', t) in protect or re.match(r'^\s*[^@(]+\([A-Z][a-z]', spline):   # sleutelgevecht of bijnaam
                continue
            sp = mon['species']
            ability = None
            for ln in lines[mon['spline'] + 1:mon['lineno'] + 8]:
                if ln.startswith('Ability:'):
                    ability = 'ABILITY_' + re.sub(r'[^A-Za-z0-9]+', '_', ln.split(':', 1)[1].strip()).upper()
                if not ln.strip():
                    break
            cur = sp
            while cur in species and len(species[cur]['evos']) == 1:
                lvl, tgt = species[cur]['evos'][0]
                if not (old < lvl <= new) or tgt not in species:
                    break
                if ability and ability not in species[tgt]['abilities']:
                    break
                cur = tgt
            if cur != sp:
                lines[mon['spline']] = spline.replace(mon['raw'], D.species_name(cur), 1)
                evolved.append((t, mon['raw'], D.species_name(cur), old, new))
    return evolved


def table(rows):
    out = ['| Gevecht | Ace | Team gem. (sterkste 6) | Team max | Verschil (gem − ace) |', '|---|---|---|---|---|']
    for r in rows:
        nm = r.get('milestone') or r['name'].replace('TRAINER_', '').title()
        out.append(f"| {'**' + nm + '**' if r.get('milestone') else nm} | {r['ace']} | {r['top6']:.1f} | "
                   f"{r['max']:.1f} | {r['top6'] - r['ace']:+.1f} |")
    return '\n'.join(out)


def plot(series, path, title):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=110)
    colors = ['#2a78d6', '#d95f02', '#1b9e77', '#7570b3']
    for (label, rows), c in zip(series, colors):
        ms = [r for r in rows]
        xs = list(range(len(ms)))
        ax.plot(xs, [r['avg'] for r in ms], '-', color=c, label=f'{label}: team gemiddeld', lw=2)
        ax.plot(xs, [r['max'] for r in ms], ':', color=c, label=f'{label}: sterkste', lw=1.5)
        ax.plot(xs, [r['ace'] for r in ms], 'o', color=c, ms=4, alpha=0.7, label=f'{label}: ace tegenstander')
    rows = series[0][1]
    ticks = [i for i, r in enumerate(rows) if r.get('milestone')]
    ax.set_xticks(ticks)
    ax.set_xticklabels([rows[i]['milestone'] for i in ticks], rotation=35, ha='right')
    ax.set_ylabel('Level')
    ax.grid(alpha=0.3)
    ax.set_title(title)
    ax.legend(fontsize=8, loc='upper left')
    fig.tight_layout()
    fig.savefig(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--strategy', default='evenwichtig', choices=['evenwichtig', 'ace'])
    ap.add_argument('--no-share', action='store_true')
    ap.add_argument('--json')
    ap.add_argument('--profile', default='hoofdpad', choices=['hoofdpad', 'completionist', 'compleet6'])
    ap.add_argument('--postgame', action='store_true', help='ook de post-game en de superbosses')
    args = ap.parse_args()
    rows = run(args.strategy, not args.no_share, profile=args.profile, postgame=args.postgame)
    print(table(rows))
    if args.json:
        json.dump(rows, open(args.json, 'w'), indent=1)


if __name__ == '__main__':
    main()
