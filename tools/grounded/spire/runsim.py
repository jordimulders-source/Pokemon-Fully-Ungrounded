#!/usr/bin/env python3
"""The Spire: hele runs naspelen (Monte Carlo) en vergelijken met Slay the Spire (StS 1, A0).

Leest de echte getallen uit de broncode (geen eigen kopieën):
  include/spire.h      verdiepingen, heal na gevecht, rustplek, act-heal, startgeld
  src/spire_run.c      kaartgenerator (kansen per kamertype), geld na gevechten
  src/spire_shop.c     prijzen
  encounters.py        HP-verlies per ontmoeting (zelfde model en kalibratie als SPIRE_BALANS.md)
  events.py            alle events met hun effecten
  src/data/spire_pool.h  rentals (voor type-eisen van events)

Speler = bot met een padplanner (zoals een Slay-speler: elites als je gezond bent, rust voor de baas,
winkel als je geld hebt), drie niveaus: goed (×0,8 HP-verlies: DEFEND, gimmicks doorzien), gemiddeld
(×1,0 = het ontmoetingsmodel) en slordig (×1,5: gimmicks negeren, zie SPIRE_DESIGN.md).

Gebruik:
    python3 runsim.py                 # sectie 'Vergelijking met Slay the Spire' onderaan SPIRE_BALANS.md
    python3 runsim.py --runs 4000     # meer runs
    python3 runsim.py --set heal_after=10 act_heal=40 --no-write   # andere instelling proberen
Volgorde na wijzigingen: spire_pool.py -> encounters.py -> runsim.py (encounters.py laat deze sectie staan).
runsim_before.txt = kerngetallen van v0.8.114 (vóór de 50 relics), voor de voor/na-tabel; --save schrijft een nieuwe.
Relics (lijst, zeldzaamheid, rekenmodel): relics.py.
"""
import argparse, math, os, random, re, statistics, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import encounters as ENC  # noqa: E402
import relics as RELICDATA  # noqa: E402

ROOT = ENC.ROOT
SECTION = '## Vergelijking met Slay the Spire'
VERSION = 'v0.9.70'


def _read(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return f.read()


# ---------------------------------------------------------------------------------------------
# Getallen uit de C-code

def c_define(txt, name, default=None):
    m = re.search(r'#define\s+%s\s+(-?\d+)' % name, txt)
    if m:
        return int(m.group(1))
    if default is None:
        raise SystemExit('%s niet gevonden' % name)
    return default


def load_config():
    h = _read('include/spire.h')
    run = _read('src/spire_run.c')
    shop = _read('src/spire_shop.c')
    cfg = dict(
        floors=c_define(h, 'SPIRE_FLOORS'),
        weak_floors=c_define(h, 'SPIRE_WEAK_FLOORS', 2),
        treasure_floor=c_define(h, 'SPIRE_TREASURE_FLOOR', -1),
        heal_after=c_define(h, 'SPIRE_HEAL_AFTER'),
        rest_heal=c_define(h, 'SPIRE_REST_HEAL'),
        start_gold=c_define(h, 'SPIRE_START_GOLD', 0),
    )
    # act-overgang: Spire_HealRun(X) in NextAct
    m = re.search(r'static void NextAct\(void\)\n\{(.*?)\n\}', run, re.S)
    arg = re.search(r'Spire_HealRun\(.*?(\w+)\);', m.group(1)).group(1)   # (Gracidea ? 100 : SPIRE_ACT_HEAL)
    cfg['act_heal'] = int(arg) if arg.isdigit() else c_define(h, arg)
    # geld na gevechten (CB2_EndSpireBattle)
    cfg['gold_boss'] = int(re.search(r'case SPIRE_ROOM_BOSS:\s*gold = (\d+)', run).group(1))
    a, b = re.search(r'case SPIRE_ROOM_ELITE:\s*gold = (\d+) \+ Random\(\) % (\d+)', run).groups()
    cfg['gold_elite'] = (int(a), int(a) + int(b) - 1)
    a, b = re.search(r'default:\s*gold = (\d+) \+ Random\(\) % (\d+)', run).groups()
    cfg['gold_fight'] = (int(a), int(a) + int(b) - 1)
    # kaartgenerator: drempels in volgorde (gevecht, event, elite, winkel, rest) en verdiepingsregels
    gen = re.search(r'void Spire_GenerateMap\(.*?\n\}\n', run, re.S).group(0)
    cfg['map_src'] = gen
    cfg['odds'] = [int(x) for x in re.findall(r'else if \(r < (\d+)\)', gen)]
    for room in ('ELITE', 'SHOP', 'REST'):
        x = re.search(r'\(f >= (\w+)(?: && [^)]*)?\) \? SPIRE_ROOM_%s' % room, gen).group(1)
        cfg[room.lower() + '_from'] = int(x) if x.isdigit() else c_define(h, x)
    assert len(cfg['odds']) == 4, cfg['odds']
    # winkel
    cfg['move_price'] = [int(x) for x in re.search(r'sMovePrice\[\] = \{([^}]*)\}', shop).group(1).split(',')]
    cfg['item_price'] = [int(x) for x in re.search(r'sItemPrice\[\] = \{([^}]*)\}', shop).group(1).split(',')]
    cfg['relic_price'] = c_define(shop, 'RELIC_PRICE')
    cfg['potion_price'] = c_define(shop, 'POTION_PRICE')
    cfg['potion_heal'] = int(re.search(r'case WARE_POTION:.*?Spire_HealRun\((\d+)\)', shop, re.S).group(1))
    return cfg


# ---------------------------------------------------------------------------------------------
# Kaartgenerator (port van Spire_GenerateMap; controle: zelfde uitvoer als de C-code, zie --check-map)

FIGHT, ELITE, REST, SHOP, EVENT, BOSS, TREASURE = 1, 2, 3, 4, 5, 6, 7
NAMES = {FIGHT: 'gevecht', ELITE: 'elite', REST: 'rust', SHOP: 'winkel', EVENT: 'event', BOSS: 'baas', TREASURE: 'schatkist'}

_MAPLIB = {}


def _map_lib(cfg):
    """Spire_GenerateMap uit src/spire_run.c (Lcg t/m Spire_GenerateMap), gecompileerd met gcc en via ctypes
    aangeroepen: de kaart in het rekenwerk is precies de kaart in de game (schatkist, Spire_WeighMap, ...)."""
    import ctypes, subprocess, tempfile, hashlib
    run = _read('src/spire_run.c')
    a = run.index('static u32 Lcg(u32 *state)')
    b = run.index('\n}\n', run.index('void Spire_GenerateMap(')) + 3
    h = _read('include/spire.h')
    defs = ''.join('#define %s %d\n' % (n, c_define(h, n, 0)) for n in
                   ('SPIRE_FLOORS', 'SPIRE_MAX_NODES', 'SPIRE_TREASURE_FLOOR', 'SPIRE_ELITE_FROM', 'SPIRE_WEAK_FLOORS'))
    src = ('#include <stdint.h>\ntypedef uint32_t u32; typedef uint8_t u8; typedef int32_t bool32;\n#define TRUE 1\n#define FALSE 0\n' + defs +
           'enum {SPIRE_ROOM_NONE,SPIRE_ROOM_FIGHT,SPIRE_ROOM_ELITE,SPIRE_ROOM_REST,SPIRE_ROOM_SHOP,SPIRE_ROOM_EVENT,SPIRE_ROOM_BOSS,SPIRE_ROOM_TREASURE};\n'
           'struct SpireMapNode{u8 type,x,links;};\n'
           'struct SpireActMap{u8 count[SPIRE_FLOORS];struct SpireMapNode nodes[SPIRE_FLOORS][SPIRE_MAX_NODES];};\n'
           + run[a:b] + '\nvoid gen(u32 seed, u8 *out){struct SpireActMap m;Spire_GenerateMap(&m,seed);'
           'for(int f=0;f<SPIRE_FLOORS;f++){out[f*9]=m.count[f];for(int i=0;i<SPIRE_MAX_NODES;i++){out[f*9+1+2*i]=m.nodes[f][i].type;out[f*9+2+2*i]=m.nodes[f][i].links;}}}\n')
    key = hashlib.md5(src.encode()).hexdigest()
    if key not in _MAPLIB:
        d = tempfile.mkdtemp()
        open(os.path.join(d, 'm.c'), 'w').write(src)
        subprocess.check_call(['gcc', '-O1', '-shared', '-fPIC', '-o', os.path.join(d, 'm.so'), os.path.join(d, 'm.c')])
        _MAPLIB[key] = ctypes.CDLL(os.path.join(d, 'm.so'))
    return _MAPLIB[key]


def generate_map(cfg, seed):
    import ctypes
    lib = _map_lib(cfg)
    F = cfg['floors']
    buf = (ctypes.c_uint8 * (F * 9))()
    lib.gen(ctypes.c_uint32(seed & 0xFFFFFFFF), buf)
    return [[dict(type=buf[f * 9 + 1 + 2 * i], links=buf[f * 9 + 2 + 2 * i]) for i in range(buf[f * 9])] for f in range(F)]


def check_map(cfg, n=5000):
    """Controle van de kaartregels (Jordi): geen rust/elite/winkel twee keer achter elkaar op een route, schatkist op de
    middelste verdieping, Snorlax (rust) vlak voor de baas, minstens één elite vóór en één na de schatkist, elke kamer
    bereikbaar."""
    F, T = cfg['floors'], cfg['treasure_floor']
    bad = Counter()
    for s_ in range(1, n + 1):
        nodes = generate_map(cfg, (s_ * 2654435761) & 0xFFFFFFFF)
        for f in range(F - 1):
            for i, nd in enumerate(nodes[f]):
                for j, nx in enumerate(nodes[f + 1]):
                    if nd['links'] & (1 << j) and nd['type'] == nx['type'] and nd['type'] in (ELITE, REST, SHOP) and f + 1 != F - 1:
                        bad['%s twee keer op rij' % NAMES[nd['type']]] += 1
        if T >= 0 and any(nd['type'] != TREASURE for nd in nodes[T]):
            bad['schatkist niet op verdieping %d' % (T + 1)] += 1
        if any(nd['type'] != REST for nd in nodes[F - 1]):
            bad['geen rust vlak voor de baas'] += 1
        if not any(nd['type'] == ELITE for f in range(T) for nd in nodes[f]):
            bad['geen elite vóór de schatkist'] += 1
        if not any(nd['type'] == ELITE for f in range(T + 1, F - 1) for nd in nodes[f]):
            bad['geen elite na de schatkist'] += 1
        for f in range(1, F):
            inc = 0
            for nd in nodes[f - 1]:
                inc |= nd['links']
            if inc != (1 << len(nodes[f])) - 1:
                bad['onbereikbare kamer'] += 1
    for k, v in bad.items():
        print('kaart: %s in %d van %d kaarten' % (k, v, n))
    print('kaartgenerator (C-code via ctypes): %d kaarten gecontroleerd, %d fouten' % (n, sum(bad.values())))
    return bad


# ---------------------------------------------------------------------------------------------
# Ontmoetingen (HP-verlies uit encounters.py, zelfde kalibratie als de header)

def load_encounters():
    ENC.totem_elites()
    rows = []
    for b in ENC.BIOMES:
        for e in ENC.ENCOUNTERS[b['key']]:
            rows.append((b, e))
    for act, lst in ENC.BOSSES.items():
        for e in lst:
            e['kind'] = 'boss'
            rows.append((dict(key='BOSS', act=act, name='Boss'), e))
    groups = {}
    for b, e in rows:
        key = (b['act'], e['kind'] if e['kind'] != 'boss' else 'boss:' + e['name'])
        e['calkey'] = key
        groups.setdefault(key, []).append(e)
    # v0.9.70: HP-verlies per ontmoeting uit echte gevechten (matchups.py, geschreven door encounters.py)
    import matchups as M
    _, stats = M.load_calib()
    out = defaultdict(list)   # (biome of 'BOSS<act>', kind) -> [(verlies 0-1, beurten)]
    for b, e in rows:
        d = stats[e['name']]
        k = b['key'] if b['key'] != 'BOSS' else 'BOSS%d' % b['act']
        out[(k, e['kind'])].append((d['loss'] / 100, d['turns'], e['name']))
    return out


# ---------------------------------------------------------------------------------------------
# Events (events.py zonder de uitvoer)

def load_events():
    src = open(os.path.join(HERE, 'events.py'), encoding='utf-8').read().split('# --- controle en uitvoer')[0]
    g = {'__file__': os.path.join(HERE, 'events.py'), '__name__': 'events_data'}
    exec(compile(src, 'events.py', 'exec'), g)
    return g['E']


def load_rental_types():
    txt = _read('src/data/spire_pool.h').split('sSpireEventRentals')[0]
    out = []
    for s in re.findall(r'\{SPECIES_(\w+), \d,', txt):
        sp = ENC.SPECIES.get(s)
        if sp:
            out.append(set(sp['types']))
    return out


# ---------------------------------------------------------------------------------------------
# Waarde-eenheden (¥), afgeleid van de winkelprijzen

def unit_values(cfg):
    hp = cfg['potion_price'] / cfg['potion_heal']           # ¥ per % HP (Super Potion)
    return dict(
        hp=hp,
        relic=cfg['relic_price'],
        move=[p * 0.5 for p in cfg['move_price']],          # willekeurige move: half de prijs (niet zelf gekozen)
        movetype=[p * 0.7 for p in cfg['move_price']],      # van een eigen type
        item=[p * 0.7 for p in cfg['item_price']],
        upgrade=40 * hp,                                    # upgrade ≈ 40% HP over de rest van de run (SPIRE_BALANS.md)
        forget=-0.6 * cfg['move_price'][1],
        remove=15,
        maxhp=3.0 * hp,                                     # 1 procentpunt blijvend ≈ 3x eenmalig (buffer bij elke baas)
        bp=4,
        recruit=40,
        evolve=70,
        run=900,                                            # waarde van de rest van de run (doodsrisico)
        reward_move=35,                                     # beloningsmove na een gevecht (kies 1 uit 3)
    )


# Relics: lijst, zeldzaamheid en rekenmodel uit relics.py (dezelfde bron als de C-tabel)
RELIC = {r['key']: r for r in RELICDATA.R}
RELICS = list(RELIC)
TIER_ROLL = [('COMMON', 50), ('UNCOMMON', 33), ('RARE', 17)]   # Spire_RandomRelic (elite, event, winkel)

# Speelduur van een mens (seconden), voor de schatting van de runlengte (zie report)
DUR = dict(turn=35, battle=25, reward=25, relic=20, event=60, shop=90, rest=25, room=10, draft=120, act=45)

SKILL = {'goed': 0.8, 'gemiddeld': 1.0, 'slordig': 1.5}
CV = {'weak': 0.45, 'normal': 0.45, 'elite': 0.5, 'boss': 0.3}   # spreiding per gevecht (balance.py: 0,6 incl. teamverschil)
MATCHUP_SD = 0.25                                                  # team vs biome/baas (types), per act


def lognorm(rng, mean, cv):
    s = math.sqrt(math.log(1 + cv * cv))
    return mean * math.exp(rng.gauss(-s * s / 2, s))


def p_exceed(mean, cv, x):
    """P(verlies >= x) bij een lognormale verdeling."""
    if mean <= 0:
        return 0.0
    if x <= 0:
        return 1.0
    s = math.sqrt(math.log(1 + cv * cv))
    z = (math.log(x / mean) + s * s / 2) / s
    return 0.5 * math.erfc(z / math.sqrt(2))


# ---------------------------------------------------------------------------------------------
# Eén run

class Run:
    def __init__(self, sim, rng, skill):
        self.sim, self.rng, self.skill = sim, rng, skill
        self.hp = 1.0          # deel van de max HP van het team
        self.maxf = 1.0        # blijvende max-HP-factor (events)
        self.gold = sim.cfg['start_gold']
        self.relics = []
        self.upgrades = 0
        self.items = 0
        self.moves = 0         # gekochte/extra moves
        self.poison = 0        # vergiftigde Pokémon (blijft tot een heal >= 40%)
        self.toxic = 0         # gevechten met Toxic Spikes
        self.sleep = 0.0       # verwacht aantal slapende Pokémon in het volgende gevecht
        self.types = rng.sample(sim.rental_types, 2)
        self.relics_out = False
        self.log = sim.log

    # -- hulpjes
    def has(self, r):
        return r in self.relics

    def rs(self, key, default=0):
        """Som (of product voor factoren) van een rekenmodel-veld over je relics."""
        return sum(RELIC[r]['sim'].get(key, 0) for r in self.relics) or default

    def power(self, kind='normal'):
        p = 0.93 ** min(self.upgrades, 6) * 0.95 ** min(self.items, 2) * 0.97 ** min(self.moves, 3)
        for r in self.relics:
            loss = RELIC[r]['sim'].get('loss', 1.0)
            p *= loss.get(kind, 1.0) if isinstance(loss, dict) else loss
        return p

    def has_type(self, t):
        return any(t in s for s in self.types)

    def heal(self, pct, source):
        before = self.hp
        self.hp = min(1.0, self.hp + pct / 100)
        self.log['heal'][(self.act, source)] += self.hp - before
        if pct >= self.sim.cfg['rest_heal']:
            self.poison = 0

    def can_offer(self, r, source, exclude):
        info = RELIC[r]
        if r in self.relics or r in exclude or any(c in self.relics for c in info['conflicts']):
            return False
        return not (source in ('winkel', 'winkel2') and info['noshop'])

    def random_relic(self, source, exclude=()):
        """Port van Spire_RandomRelic: zeldzaamheid per bron, terugvallen op de naastgelegen."""
        if source == 'baas':
            order = ['BOSS', 'RARE', 'UNCOMMON', 'COMMON', 'SHOP']
        elif source == 'winkel2':
            order = ['SHOP', 'UNCOMMON', 'COMMON', 'RARE', 'BOSS']
        else:
            x = self.rng.randrange(100)
            tier = 'COMMON' if x < 50 else 'UNCOMMON' if x < 83 else 'RARE'
            rest = {'COMMON': ['UNCOMMON', 'RARE'], 'UNCOMMON': ['COMMON', 'RARE'], 'RARE': ['UNCOMMON', 'COMMON']}[tier]
            order = [tier] + rest + (['SHOP'] if source == 'winkel' else []) + ['BOSS']
        for t in order:
            cands = [r for r in RELICS if RELIC[r]['tier'] == t and self.can_offer(r, source, exclude)]
            if cands:
                return self.rng.choice(cands)
        return None

    def take_relic(self, r):
        self.relics.append(r)
        sim = RELIC[r]['sim']
        if sim.get('maxhp'):
            self.apply_fx([('maxhp', sim['maxhp'])])
        if sim.get('upgrades'):
            self.upgrades += sim['upgrades']
        if sim.get('fullheal'):
            self.heal(100, 'event')

    def add_relic(self, source):
        # elite/baas: kies 1 uit 3 kaarten; event: 1 willekeurige; winkel: zie shop()
        offers = []
        for _ in range(3 if source in ('elite', 'baas') else 1):
            r = self.random_relic(source, offers)
            if r:
                offers.append(r)
        self.log['relicoffers'] += 1
        if not offers:
            if not self.relics_out:
                self.relics_out = True
                self.log['relicsout'] += 1
            return False
        self.log['relicshort'] += len(offers) < (3 if source in ('elite', 'baas') else 1)
        self.take_relic(max(offers, key=lambda r: RELIC[r]['sim'].get('pick', 0)))
        return True

    def gold_in(self, amount, source):
        if self.has('AMULET_COIN') and source in ('gevecht', 'elite', 'baas'):
            amount = amount * 3 // 2
        if self.rs('nogold') and source in ('gevecht', 'elite', 'baas'):
            amount = 0
        self.gold += amount
        self.log['gold'][(self.act, source)] += amount

    # -- verwacht verlies
    def exp_loss(self, kind, turns=3.5):
        base = self.sim.mean_loss[(self.biome if kind != 'boss' else 'BOSS%d' % self.act, kind)]
        if kind == 'boss':
            base = self.boss_loss
        m = base * self.skill * self.matchup * self.power(kind) / self.maxf * self.sim.cfg.get('act_scale', {}).get((self.act, kind), 1.0)
        m += self.poison * 0.0625 * turns / self.maxf * 0.5
        return m

    # -- gevecht
    def fight(self, kind):
        S = self.sim
        if kind == 'boss':
            loss, turns = self.boss_loss, self.boss_turns
        else:
            loss, turns, _ = self.rng.choice(S.enc[(self.biome, kind)])
        # Toxic Spikes (events): 40% per Pokémon (Poison/Steel veilig)
        if self.toxic:
            safe = sum(1 for t in self.types if 'POISON' in t or 'STEEL' in t)
            for _ in range(2 - safe - self.poison):
                if self.rng.random() < 0.4:
                    self.poison += 1
            self.toxic -= 1
        m = loss * self.skill * self.matchup * self.power(kind) * S.cfg.get('act_scale', {}).get((self.act, kind), 1.0)
        m *= 1 + 0.35 * self.sleep
        self.sleep = 0
        L = lognorm(self.rng, m, CV[kind]) / self.maxf
        # gif: 1/8 van de (x4) max HP per beurt = 12,5% van de balk; voor het team de helft
        L += self.poison * 0.0625 * turns / self.maxf
        room = {'weak': 'gevecht', 'normal': 'gevecht', 'elite': 'elite', 'boss': 'baas'}[kind]
        self.log['loss'][(self.act, room)].append(min(L, self.hp))
        # speelduur: beurten (relics die vijanden minder HP geven maken het gevecht korter), plus intro/beloning
        hpf = 0.8 if (kind == 'elite' and self.has('RING_TARGET')) else 0.85 if (kind in ('weak', 'normal') and self.has('QUICK_BALL')) else 1.0
        self.time += turns * hpf * DUR['turn'] + DUR['battle'] + DUR['reward'] + (DUR['relic'] if kind in ('elite', 'boss') else 0)
        self.turns += turns * hpf
        if L >= self.hp:
            self.dead = (self.act, room)
            return False
        self.hp -= L
        heal = S.cfg['heal_after'] + (10 if self.has('BERRY_POUCH') else 0)
        if self.rs('noheal'):
            heal = 0
        self.heal(heal, 'na gevecht')
        if self.rs('oran') and self.hp < 0.5:
            self.heal(self.rs('oran') / 2, 'na gevecht')   # per Pokémon onder 50%: ±de helft van het team
        lo, hi = S.cfg['gold_fight'] if room == 'gevecht' else S.cfg['gold_elite'] if room == 'elite' else (S.cfg['gold_boss'],) * 2
        self.gold_in(self.rng.randint(lo, hi), room)
        if room == 'baas':
            self.add_relic('baas')
        elif room == 'elite':
            for _ in range(max(1, self.rs('elite_relics'))):
                self.add_relic('elite')
        return True

    # -- rust
    def rest_amount(self):
        return self.sim.cfg['rest_heal'] + (30 if self.has('SOOTHE_BELL') else 0)

    def rest(self, next_is_boss):
        need = 0.9 if next_is_boss else 0.6
        self.time += DUR['rest']
        if (self.hp < need or self.poison or self.rs('noupgrade')) and not self.rs('norest'):
            self.heal(self.rest_amount(), 'rust')
            self.upgrades += self.rs('rest_upgrade')
            self.log['restchoice'][(self.act, 'heal')] += 1
        elif not self.rs('noupgrade'):
            self.upgrades += 1 + self.rs('upgrade_bonus')
            self.log['restchoice'][(self.act, 'upgrade')] += 1

    # -- winkel
    def shop(self):
        cfg, V = self.sim.cfg, self.sim.V
        f = self.rs('shop', 1.0) if self.has('RAINBOW_PASS') else 1.0
        price = lambda x: int(x * f)
        spent0 = self.gold
        bought = 0
        self.time += DUR['shop']
        if self.hp < 0.65 and self.gold >= price(cfg['potion_price']):
            self.gold -= price(cfg['potion_price'])
            self.heal(cfg['potion_heal'], 'winkel')
            bought += 1
        # twee relics in de winkel: een gewone en een winkel-relic; de bot koopt de beste die hij kan betalen
        offers = []
        for src in ('winkel', 'winkel2'):
            r = self.random_relic(src, offers)
            if r:
                offers.append(r)
        self.log['relicoffers'] += 1
        if not offers and not self.relics_out:
            self.relics_out = True
            self.log['relicsout'] += 1
        if offers and self.gold >= price(cfg['relic_price']):
            self.gold -= price(cfg['relic_price'])
            self.take_relic(max(offers, key=lambda r: RELIC[r]['sim'].get('pick', 0)))
            bought += 1
        if self.items < 2 and self.gold >= price(cfg['item_price'][1]):
            self.gold -= price(cfg['item_price'][1])
            self.items += 1
            bought += 1
        if self.moves < 3 and self.gold >= price(cfg['move_price'][1]):
            self.gold -= price(cfg['move_price'][1])
            self.moves += 1
            bought += 1
        if self.items < 2 and self.gold >= price(cfg['item_price'][0]):
            self.gold -= price(cfg['item_price'][0])
            self.items += 1
            bought += 1
        self.log['spent'][self.act] += spent0 - self.gold
        self.log['bought'][self.act].append(bought)

    # -- event: beste optie op verwachtingswaarde
    def fx_value(self, fx):
        V, cfg = self.sim.V, self.sim.cfg
        val, hp = 0.0, self.hp
        for f in fx:
            k, a = f[0], (f[1] if len(f) > 1 else 0)
            if k == 'gold':
                val += a
            elif k == 'goldpct':
                val += self.gold * a / 100
            elif k == 'heal':
                if a > 0:
                    val += min(a / 100, 1 - hp) * 100 * V['hp']
                    hp = min(1, hp + a / 100)
                else:
                    d = min(-a / 100, hp - 0.01)
                    val -= d * 100 * V['hp'] * (1 + 2 * max(0, 0.5 - hp))
                    hp -= d
            elif k == 'hurt1':
                val -= a / 2 * V['hp']
            elif k == 'maxhp':
                val += a * V['maxhp']
            elif k == 'bp':
                val += a * V['bp']
            elif k == 'relic':
                val += V['relic']
            elif k == 'loserelic':
                val -= V['relic'] if self.relics else 0
            elif k == 'item':
                val += V['item'][a] if self.items < 2 else V['item'][a] * 0.3
            elif k == 'give':
                val += V['item'][1] if self.items < 2 else 0
            elif k == 'loseitems':
                val -= self.items * V['item'][1]
            elif k == 'teach':
                val += V['move'][a]
            elif k == 'teachtype':
                val += V['movetype'][a]
            elif k == 'teachmove':
                val += V['move'][1]
            elif k == 'upgrade':
                val += a * V['upgrade']
            elif k == 'forget':
                val += a * V['forget']
            elif k == 'remove':
                val += V['remove']
            elif k == 'fullheal':
                val += (1 - hp) * 100 * V['hp']
                hp = 1
            elif k == 'pp':
                val += 8
            elif k == 'sleep':
                val -= 2 * a / 100 * 0.35 * self.sim.mean_loss[(self.biome, 'normal')] * 100 * V['hp']
            elif k == 'toxic':
                safe = sum(1 for t in self.types if 'POISON' in t or 'STEEL' in t)
                # kans dat een Pokémon gif oploopt in a gevechten, daarna ±1,5 gevecht tot de volgende heal
                p = 1 - 0.6 ** a
                val -= (2 - safe) * p * 0.0625 * 3.5 * 1.5 * 100 * V['hp']
            elif k == 'elite':
                m = self.exp_loss('elite', 4.5)
                pd = p_exceed(m, CV['elite'], hp)
                val += (1 - pd) * (V['relic'] + 40 + V['reward_move'] - m * 100 * V['hp']) - pd * V['run']
            elif k in ('recruit', 'recruitspecies', 'ditto'):
                val += V['recruit'] + (1 - hp) * 50 * V['hp']
            elif k == 'wonder':
                val += (1 - hp) * 50 * V['hp']
            elif k == 'evolve':
                val += V['evolve'] if self.act < 3 else 60
            elif k == 'wheel':
                val += (100 + V['relic'] + (1 - hp) * 100 * V['hp'] - 15 * V['hp'] + V['upgrade'] + V['forget']) / 6
        return val

    def apply_fx(self, fx):
        V, cfg = self.sim.V, self.sim.cfg
        for f in fx:
            k, a = f[0], (f[1] if len(f) > 1 else 0)
            if k == 'gold':
                if a > 0:
                    self.gold_in(a, 'event')
                else:
                    self.gold = max(0, self.gold + a)
            elif k == 'goldpct':
                d = self.gold * a // 100
                if d > 0:
                    self.gold_in(d, 'event')
                else:
                    self.gold += d
            elif k == 'heal':
                if a > 0:
                    self.heal(a, 'event')
                else:
                    self.hp = max(0.01, self.hp + a / 100)
                    self.log['eventdmg'][self.act] += -a / 100
            elif k == 'hurt1':
                self.hp = max(0.01, self.hp - a / 200)
            elif k == 'maxhp':
                old = self.maxf
                self.maxf = max(0.4, min(1.6, self.maxf + a / 100))
                if a > 0:
                    self.hp = min(1.0, (self.hp * old + (self.maxf - old)) / self.maxf)
            elif k == 'relic':
                self.add_relic('event')
            elif k == 'loserelic':
                if self.relics:
                    r = self.rng.choice(self.relics)
                    self.relics.remove(r)
                    if RELIC[r]['sim'].get('maxhp'):
                        self.maxf = max(0.4, self.maxf - RELIC[r]['sim']['maxhp'] / 100)
            elif k in ('item', 'give'):
                self.items = min(2, self.items + 1)
            elif k == 'loseitems':
                self.items = 0
            elif k in ('teach', 'teachtype', 'teachmove'):
                self.moves += 1 if (a >= 1 or k == 'teachmove') else 0
            elif k == 'upgrade':
                self.upgrades += a
            elif k == 'forget':
                self.moves -= a
            elif k == 'fullheal':
                self.heal(100, 'event')
            elif k == 'sleep':
                self.sleep += 2 * a / 100
            elif k == 'toxic':
                self.toxic = max(self.toxic, a)
            elif k == 'elite':
                if not self.fight('elite'):
                    return False
                self.log['eventelite'][self.act] += 1
            elif k in ('recruit', 'recruitspecies', 'ditto', 'wonder'):
                # nieuwe Pokémon met volle HP vervangt er één (de zwakste)
                self.hp = min(1.0, self.hp + (1 - self.hp) / 2)
                self.poison = max(0, self.poison - 1)
            elif k == 'wheel':
                w = self.rng.randrange(6)
                self.apply_fx([[('gold', 100)], [('relic',)], [('fullheal',)], [('heal', -15)], [('upgrade', 1)], [('forget', 1)]][w])
        return True

    def event(self):
        S = self.sim
        self.time += DUR['event']
        pool = [e for e in S.events if self.act in e['acts'] and e['key'] not in self.seen]
        if not pool:
            self.seen = set()
            pool = [e for e in S.events if self.act in e['acts']]
        e = self.rng.choice(pool)
        self.seen.add(e['key'])
        best, bv = None, -1e9
        for o in e['options']:
            if o['need'] and not self.has_type(o['need']):
                continue
            cost = -sum(f[1] for f in o['fx'] if f[0] == 'gold' and f[1] < 0)
            if cost > self.gold:
                continue
            if 'chance' in o:
                v = o['chance'] / 100 * self.fx_value(o['fx']) + (1 - o['chance'] / 100) * self.fx_value(o['fxb'])
            else:
                v = self.fx_value(o['fx'])
            if v > bv:
                best, bv = o, v
        if best is None:
            # alles op slot (geen geld, geen type): in de C-code kun je dan niet verder (zie rapport)
            self.log['event'][e['key']].append(0.0)
            self.log['softlock'][e['key']] += 1
            return True
        self.log['event'][e['key']].append(bv)
        fx = best['fx']
        chance = min(95, best['chance'] + self.rs('gamble')) if 'chance' in best and best['chance'] < 100 and self.rs('gamble') else best.get('chance')
        if 'chance' in best and self.rng.random() * 100 >= chance:
            fx = best['fxb']
        return self.apply_fx(fx)

    # -- padplanner
    def plan_value(self, path, F):
        """Verwachte waarde van een pad (lijst kamertypes tot en met de baas)."""
        V, cfg = self.sim.V, self.sim.cfg
        hp, gold, alive, val = self.hp, self.gold, 1.0, 0.0
        heal_after = 0 if self.rs('noheal') else cfg['heal_after'] + (10 if self.has('BERRY_POUCH') else 0)
        for idx, t in enumerate(path):
            if t in (FIGHT, ELITE, BOSS):
                kind = 'boss' if t == BOSS else 'elite' if t == ELITE else ('weak' if self.floor + idx < self.sim.cfg['weak_floors'] else 'normal')
                m = self.exp_loss(kind)
                pd = p_exceed(m, CV[kind], hp)
                alive *= 1 - pd
                hp = max(0.02, hp - m)
                if t != BOSS:
                    hp = min(1, hp + heal_after / 100)
                g = sum(cfg['gold_fight']) / 2 if t == FIGHT else sum(cfg['gold_elite']) / 2 if t == ELITE else cfg['gold_boss']
                gold += g
                val += alive * (g * 0.6 + V['reward_move'] + (V['relic'] if t in (ELITE, BOSS) else 0))
            elif t == REST:
                nxt_boss = idx + 1 < len(path) and path[idx + 1] == BOSS
                if hp < (0.9 if nxt_boss else 0.6) and not self.rs('norest'):
                    gain = min(self.rest_amount() / 100, 1 - hp)
                    hp += gain
                    val += alive * gain * 100 * V['hp']
                else:
                    val += alive * V['upgrade']
            elif t == SHOP:
                spend = min(gold, 250)
                if hp < 0.65 and gold >= cfg['potion_price']:
                    hp = min(1, hp + cfg['potion_heal'] / 100)
                val += alive * spend * 0.4
                gold -= spend
            elif t == EVENT:
                val += alive * self.sim.event_ev
            elif t == TREASURE:
                val += alive * V['relic']
        val += alive * hp * 100 * V['hp'] * 0.5      # HP na de baas (act-overgang heelt maar deels)
        val -= (1 - alive) * V['run']
        return val

    def paths_from(self, nodes, f, i, depth=7):
        """Alle paden vanaf kamer i op verdieping f (types), hooguit depth verdiepingen vooruit (13 verdiepingen geven
        anders duizenden paden; een Slay-speler kijkt ook een stuk vooruit, niet tot de baas)."""
        t = nodes[f][i]['type']
        if f == len(nodes) - 1 or depth <= 1:
            return [[t]]
        out = []
        for j in range(len(nodes[f + 1])):
            if nodes[f][i]['links'] & (1 << j):
                for p in self.paths_from(nodes, f + 1, j, depth - 1):
                    out.append([t] + p)
        return out

    def play_act(self, act):
        S = self.sim
        self.act = act
        self.biome = self.rng.choice([b['key'] for b in ENC.BIOMES if b['act'] == act])
        self.matchup = math.exp(self.rng.gauss(0, MATCHUP_SD))
        bosses = S.enc[('BOSS%d' % act, 'boss')]
        self.boss_loss, self.boss_turns, self.boss_name = self.rng.choice(bosses)
        nodes = generate_map(S.cfg, self.rng.getrandbits(32))
        F = S.cfg['floors']
        cur = None
        self.taken = []
        for f in range(F):
            self.floor = f
            cands = range(len(nodes[f])) if cur is None else [j for j in range(len(nodes[f])) if nodes[f - 1][cur]['links'] & (1 << j)]
            best, bv = None, -1e18
            for j in cands:
                for p in self.paths_from(nodes, f, j):
                    v = self.plan_value(p + ([BOSS] if f + len(p) >= F else []), F)
                    if v > bv:
                        best, bv = j, v
            cur = best
            t = nodes[f][cur]['type']
            self.taken.append(t)
            self.time += DUR['room']
            self.log['rooms'][(act, t)] += 1
            if t == FIGHT:
                ok = self.fight('weak' if f < S.cfg['weak_floors'] else 'normal')
            elif t == ELITE:
                ok = self.fight('elite')
            elif t == REST:
                self.rest(f == F - 1)
                ok = True
            elif t == SHOP:
                self.shop()
                self.log['shopvisit'][act] += 1
                ok = True
            elif t == TREASURE:
                self.add_relic('elite')     # schatkist: één relic (Spire_OpenCards, bron elite)
                ok = True
            else:
                ok = self.event()
            if not ok:
                return False
        self.log['arrive'][act].append(self.hp)
        if self.rs('boss_heal'):
            self.heal(self.rs('boss_heal'), 'event')   # Hyper Potion
        if not self.fight('boss'):
            return False
        self.log['afterboss'][act].append(self.hp)
        if act < 3:
            self.heal(max(S.cfg['act_heal'], self.rs('act_heal')), 'act-overgang')
            self.time += DUR['act']
        return True

    def play(self):
        self.seen = set()
        self.dead = None
        self.time = DUR['draft']
        self.turns = 0.0
        for act in (1, 2, 3):
            self.log['reached'][act] += 1
            if not self.play_act(act):
                self.log['died'][self.dead] += 1
                self.log['time_lost'].append(self.time)
                return act
            self.log['cleared'][act] += 1
        self.log['time_won'].append(self.time)
        self.log['turns_won'].append(self.turns)
        self.log['relics_won'].append(len(self.relics))
        return 4


class Sim:
    def __init__(self, cfg):
        self.cfg = cfg
        self.V = unit_values(cfg)
        self.enc = load_encounters()
        self.mean_loss = {k: statistics.mean(x[0] for x in v) for k, v in self.enc.items()}
        self.events = load_events()
        self.rental_types = load_rental_types()
        self.event_ev = 50.0

    def run_many(self, n, skill, seed=1):
        self.log = dict(rooms=Counter(), loss=defaultdict(list), heal=Counter(), gold=Counter(), spent=Counter(),
                        bought=defaultdict(list), shopvisit=Counter(), event=defaultdict(list), restchoice=Counter(),
                        reached=Counter(), cleared=Counter(), died=Counter(), arrive=defaultdict(list),
                        afterboss=defaultdict(list), eventdmg=Counter(), eventelite=Counter(), softlock=Counter())
        self.log['relicsout'] = 0
        self.log['relicoffers'] = 0
        self.log['relicshort'] = 0
        self.log['time_won'], self.log['time_lost'], self.log['turns_won'], self.log['relics_won'] = [], [], [], []
        rng = random.Random(seed)
        ends = Counter()
        for _ in range(n):
            r = Run(self, rng, SKILL[skill])
            ends[r.play()] += 1
        self.log['n'] = n
        self.log['ends'] = ends
        return self.log


# ---------------------------------------------------------------------------------------------
# Rapport

STS = {
    # per act, StS 1 A0 (Ironclad/Silent), typisch pad van 15 kamers + baas
    'rooms': {FIGHT: '5-7', ELITE: '1-3', EVENT: '3-5', SHOP: '1-2', REST: '2-4'},
    'map': 'gevecht ±45%, event 22%, elite 8% (A0) / 13% (A1+), rust 12%, winkel 5%; verdieping 1 gevecht, 9 schatkist, 15 rust; geen elite/rust vóór verdieping 6',
    'loss': {'gevecht': '5-15%', 'elite': '20-35%', 'baas': '30-50%'},
    'heal_after': 'Ironclad 6 HP (7,5%), Silent 0',
    'rest': '30%',
    'act_heal': '100% (A0-4), 75% van het tekort (A5+)',
    'gold': 'gevecht 10-20, elite 25-35, baas 95-105; start 99',
    'gold_act': '±250 (+99 start)',
    'shop': 'kaart 45-55 / 68-82 / 135-165, relic 143-315, verwijderen 75+25n, potion 48-105',
    'win': '40-60% (redelijke speler, A0)',
}


def pct(x):
    return '%.0f%%' % (100 * x)


def fmt_range(vals):
    if not vals:
        return '-'
    v = sorted(vals)
    return '%.0f%% (p10 %.0f%%, p90 %.0f%%)' % (100 * statistics.mean(v), 100 * v[len(v) // 10], 100 * v[len(v) * 9 // 10])


def report(sim, logs, changes, before, sens=None):
    cfg = sim.cfg
    L = ['', SECTION + ' (%s)' % VERSION, '',
         'Gegenereerd door `tools/grounded/spire/runsim.py` (Monte Carlo over de echte kaartgenerator, ontmoetingen, events, '
         'geld en prijzen uit de C-code; %d runs per niveau). Referentie: Slay the Spire 1, A0 (Ironclad/Silent).' % logs['gemiddeld']['n'], '',
         '**Bot:** padplanner zoals een Slay-speler (elites als je gezond bent, rust vóór de baas, winkel met geld); kiest per event de optie met '
         'de hoogste verwachtingswaarde. HP-verlies per gevecht = ontmoetingsmodel (hierboven) × niveau × teamfactor (lognormaal, sd 0,25 per act: '
         'types tegen biome/baas) × relics/upgrades/items, met spreiding per gevecht (CV 0,45 gewoon, 0,5 elite, 0,3 baas; '
         '`balance.py` meet 0,6 inclusief teamverschil). Niveaus: **goed** ×0,8 (DEFEND, gimmicks doorzien), **gemiddeld** ×1,0, **slordig** ×1,5.', '',
         '**Waarde-eenheden (¥)**, uit de winkelprijzen: 1%% HP = %.1f¥ (Super Potion %d¥ voor %d%%), relic %d¥, upgrade %d¥ (±40%% HP over de rest van de run), '
         'willekeurige move = halve prijs, vasthouditem 70%% van de prijs, 1 procentpunt max HP = 3× 1%% HP (buffer bij elke baas).' % (sim.V['hp'], cfg['potion_price'], cfg['potion_heal'], cfg['relic_price'], sim.V['upgrade']), '']
    g = logs['gemiddeld']
    n = g['n']

    def per_act(log, key, act):
        return log[key][act] / max(1, log['reached'][act])

    # kamers
    L += ['### Kamers per act (gekozen pad)', '',
          '| kamer | Slay (15 + baas) | Spire act 1 | act 2 | act 3 | Spire ×15/%d |' % cfg['floors'], '|---|---|---|---|---|---|']
    for t in (FIGHT, ELITE, EVENT, SHOP, REST):
        vals = [g['rooms'][(a, t)] / max(1, g['reached'][a]) for a in (1, 2, 3)]
        L.append('| %s | %s | %.1f | %.1f | %.1f | %.1f |' % (NAMES[t], STS['rooms'][t], *vals, statistics.mean(vals) * 15 / cfg['floors']))
    L += ['', 'Kaart: %s. Spire: %d verdiepingen + baas; verdieping 1 gevecht, %d rust; elites vanaf verdieping %d, rust vanaf %d; '
          'kansen gevecht/event/elite/winkel/rust = %d/%d/%d/%d/%d%%.' % (
              STS['map'], cfg['floors'], cfg['floors'], cfg['elite_from'] + 1, cfg['rest_from'] + 1,
              cfg['odds'][0], cfg['odds'][1] - cfg['odds'][0], cfg['odds'][2] - cfg['odds'][1], cfg['odds'][3] - cfg['odds'][2], 100 - cfg['odds'][3]), '']
    # HP
    L += ['### HP per kamer (gemiddeld niveau, % van de team-HP)', '',
          '| | Slay | act 1 | act 2 | act 3 |', '|---|---|---|---|---|']
    for room in ('gevecht', 'elite', 'baas'):
        L.append('| verlies %s | %s | %s |' % (room, STS['loss'][room], ' | '.join(fmt_range(g['loss'][(a, room)]) for a in (1, 2, 3))))
    L.append('| aankomst bij de baas | ±70-90%% | %s |' % ' | '.join(fmt_range(g['arrive'][a]) for a in (1, 2, 3)))
    L.append('| na de baas | ±40-70%% | %s |' % ' | '.join(fmt_range(g['afterboss'][a]) for a in (1, 2, 3)))
    for src, ref in (('na gevecht', STS['heal_after'] + ' per gevecht'), ('rust', STS['rest'] + ' per rustplek'),
                     ('event', 'wisselend'), ('winkel', 'potions'), ('act-overgang', STS['act_heal'])):
        L.append('| heal: %s (effectief, per act) | %s | %s |' % (src, ref, ' | '.join(pct(g['heal'][(a, src)] / max(1, g['reached'][a])) for a in (1, 2, 3))))
    L.append('| schade uit events (per act) | ±5-15%% | %s |' % ' | '.join(pct(per_act(g, 'eventdmg', a)) for a in (1, 2, 3)))
    rc = [(g['restchoice'][(a, 'heal')], g['restchoice'][(a, 'upgrade')]) for a in (1, 2, 3)]
    L.append('| rustplek: heal / upgrade | ±60/40 (act 1) | %s |' % ' | '.join('%d/%d' % (100 * h / max(1, h + u), 100 * u / max(1, h + u)) for h, u in rc))
    L.append('')
    # geld
    L += ['### Geld en winkel (gemiddeld niveau)', '',
          '| | Slay | act 1 | act 2 | act 3 |', '|---|---|---|---|---|']
    for src in ('gevecht', 'elite', 'baas', 'event'):
        L.append('| geld uit %s | %s | %s |' % (src, {'gevecht': '±90', 'elite': '±60', 'baas': '±100', 'event': '±30'}[src],
                                               ' | '.join('%.0f¥' % (g['gold'][(a, src)] / max(1, g['reached'][a])) for a in (1, 2, 3))))
    tot = [sum(g['gold'][(a, s)] for s in ('gevecht', 'elite', 'baas', 'event')) / max(1, g['reached'][a]) for a in (1, 2, 3)]
    L.append('| totaal per act | %s | %s |' % (STS['gold_act'], ' | '.join('%.0f¥' % x for x in tot)))
    L.append('| uitgegeven per act | ±200-300 | %s |' % ' | '.join('%.0f¥' % per_act(g, 'spent', a) for a in (1, 2, 3)))
    L.append('| aankopen per winkelbezoek | 2-3 | %s |' % ' | '.join('%.1f' % (statistics.mean(g['bought'][a]) if g['bought'][a] else 0) for a in (1, 2, 3)))
    L.append('| relic-prijs / geld per act | 0,6-1,2 | %s |' % ' | '.join('%.2f' % (cfg['relic_price'] / max(1, x)) for x in tot))
    L.append('| goedkoopste move / geld per act | ±0,2 | %s |' % ' | '.join('%.2f' % (cfg['move_price'][0] / max(1, x)) for x in tot))
    L += ['', 'Prijzen Slay: %s. Spire: move %s¥, item %s¥, relic %d¥, Super Potion %d¥ (%d%%), Move Relearner 50+25n¥; startgeld %d¥.' % (
        STS['shop'], '/'.join(map(str, cfg['move_price'])), '/'.join(map(str, cfg['item_price'])), cfg['relic_price'],
        cfg['potion_price'], cfg['potion_heal'], cfg['start_gold']), '']
    # winkans
    L += ['### Winkans per act en run', '', '| niveau | act 1 gehaald | act 2 | act 3 | hele run | Slay |', '|---|---|---|---|---|---|']
    for k in ('goed', 'gemiddeld', 'slordig'):
        lg = logs[k]
        L.append('| %s | %s | %s | %s | **%s** | %s |' % (k, *(pct(lg['cleared'][a] / max(1, lg['reached'][a])) for a in (1, 2, 3)),
                                                         pct(lg['cleared'][3] / lg['n']), {'goed': '±70-90% (ervaren, A0)', 'gemiddeld': STS['win'], 'slordig': '<15%'}[k]))
    if sens:
        L += ['', '**Gevoeligheid** (winkans van de hele run tegen de HP-verliesfactor van de speler; 1,0 = het ontmoetingsmodel): ' +
              ', '.join('×%.2f → %s' % (m, pct(w)) for m, w in sorted(sens.items())) +
              '. De curve is steil, zoals in Slay: hoeveel spelkwaliteit scheelt, bepalen de gimmicks van de ontmoetingen (puzzels), niet de economie.']
    # speelduur
    tw, tl, tu = g['time_won'], g['time_lost'], g['turns_won']
    if tw:
        other = statistics.mean(tw) - statistics.mean(tu) * DUR['turn']
        L += ['', '### Speelduur van een run (schatting voor een mens)', '',
              'Doel (Jordi): een run duurt voor een mens ±1u-1u20. Een mens denkt per beurt veel langer na dan de bot. Aannames per beurt: '
              'twee keuzes (FIGHT/DEFEND, move, doel) met de intenties lezen ±2×10 s plus ±15 s animaties en berichten (tekst Fast, '
              'gevechtsanimaties al ingekort) = **%d s per beurt**. Per gevecht %d s intro/uitslag en %d s beloningsscherm (+%d s relic), '
              'event %d s, winkel %d s, rustplek %d s, kaart %d s per kamer, draft %d s, act-overgang %d s.' % (
                  DUR['turn'], DUR['battle'], DUR['reward'], DUR['relic'], DUR['event'], DUR['shop'], DUR['rest'], DUR['room'], DUR['draft'], DUR['act']), '',
              '| | beurten | duur bij 25 s/beurt | 35 s/beurt | 45 s/beurt |', '|---|---|---|---|---|']
        for label, turns, rest in (('gewonnen run', statistics.mean(tu), other),):
            L.append('| %s | %.0f | %.0f min | %.0f min | %.0f min |' % (label, turns, (turns * 25 + rest) / 60, (turns * 35 + rest) / 60, (turns * 45 + rest) / 60))
        L += ['', 'Verloren runs duren gemiddeld %.0f min (35 s/beurt). Per act: ±%.0f beurten in gevechten, ±%.0f min buiten gevechten. '
              'Conclusie: een gewonnen run zit met %.0f min (25-45 s per beurt: %.0f-%.0f min) %s het doel van 60-80 min; '
              'de actlengte (%d verdiepingen) blijft zoals hij is.' % (
                  statistics.mean(tl) / 60 if tl else 0, statistics.mean(tu) / 3, other / 3 / 60, statistics.mean(tw) / 60,
                  (statistics.mean(tu) * 25 + other) / 60, (statistics.mean(tu) * 45 + other) / 60,
                  'binnen' if 60 <= statistics.mean(tw) / 60 <= 80 else 'buiten', cfg['floors'])]
        L[-1] = L[-1].replace('de actlengte (%d verdiepingen) blijft zoals hij is.' % cfg['floors'],
                              'de acts zijn bewust langer (%d verdiepingen, Jordi); zie *Voor Jordi*.' % cfg['floors'])
    L += ['', '**Waar runs eindigen** (gemiddeld niveau; Slay: act-1-elites en de act-1/2-baas zijn de grote killers, act 2 ook gewone gevechten):', '']
    deaths = g['died']
    tot_d = max(1, sum(deaths.values()))
    L.append(', '.join('act %d %s %s' % (a, r, pct(c / tot_d)) for (a, r), c in sorted(deaths.items(), key=lambda x: -x[1])))
    L += ['', '### Events (verwachtingswaarde van de beste optie voor de bot, ¥)', '',
          'Slay: een event is gemiddeld ±50-100 goud waard, met gemene uitzonderingen. Doel hier (events.py): ±60-120¥; >180 = te gul, <15 = zinloos.', '']
    evs = sorted(((statistics.mean(v), k) for k, v in g['event'].items()), reverse=True)
    allv = [x for v in g['event'].values() for x in v]
    L.append('Gemiddeld **%.0f¥** per event (%d events). Hoogste: %s. Laagste: %s.' % (
        statistics.mean(allv), len(evs), ', '.join('%s %.0f' % (k, v) for v, k in evs[:6]), ', '.join('%s %.0f' % (k, v) for v, k in evs[-6:])))
    L.append('')
    if before:
        L += ['### Voor en na', '', '| | vóór | na |', '|---|---|---|']
        for row in before:
            L.append('| %s | %s | %s |' % row)
        L.append('')
    if changes:
        L += ['### Aanpassingen (%s) en waarom' % VERSION, '']
        L += ['- ' + c for c in changes]
        L.append('')
    L += ['### Conclusies', '']
    L += ['- ' + c for c in conclusions(sim, logs)]
    L += ['', '### Voor Jordi (beslissen of testen)', '']
    L += ['- ' + c for c in OPEN]
    L.append('')
    return L


def summary_rows(sim, logs):
    """Kerngetallen voor de voor/na-tabel."""
    g = logs['gemiddeld']
    out = {}
    for t in (FIGHT, ELITE, EVENT, SHOP, REST):
        out['%s per act' % NAMES[t]] = '%.2f' % statistics.mean(g['rooms'][(a, t)] / max(1, g['reached'][a]) for a in (1, 2, 3))
    out['geld per act'] = '%.0f¥' % statistics.mean(sum(g['gold'][(a, s)] for s in ('gevecht', 'elite', 'baas', 'event')) / max(1, g['reached'][a]) for a in (1, 2, 3))
    out['aankomst baas act 1'] = statistics.mean(g['arrive'][1]) if g['arrive'][1] else 0
    for room in ('gevecht', 'elite', 'baas'):
        out['verlies %s act 1/2/3' % room] = ' / '.join('%.0f%%' % (100 * statistics.mean(g['loss'][(a, room)])) for a in (1, 2, 3))
    out['aankopen per winkel act 1'] = '%.1f' % (statistics.mean(g['bought'][1]) if g['bought'][1] else 0)
    out['rust: heal act 1'] = g['restchoice'][(1, 'heal')] / max(1, g['restchoice'][(1, 'heal')] + g['restchoice'][(1, 'upgrade')])
    out['relic-pool leeg (runs)'] = g['relicsout'] / max(1, g['reached'][3])
    out['relics per gewonnen run'] = '%.1f' % (statistics.mean(g['relics_won']) if g['relics_won'] else 0)
    out['speelduur gewonnen run (min)'] = '%.0f' % (statistics.mean(g['time_won']) / 60 if g['time_won'] else 0)
    for k in ('goed', 'gemiddeld', 'slordig'):
        out['winkans %s' % k] = logs[k]['cleared'][3] / logs[k]['n']
        out['act 1 gehaald (%s)' % k] = logs[k]['cleared'][1] / logs[k]['n']
    allv = [x for v in g['event'].values() for x in v]
    out['event-EV (gemiddeld)'] = '%.0f¥' % statistics.mean(allv)
    return out


def fmtv(v):
    if isinstance(v, str):
        return v
    return ('%.1f' % v) if v > 1.5 else pct(v)


CHANGES = [
    '**Acts 7 -> 13 verdiepingen + baas** (Jordi, 5 okt: "de acts mogen wat langer, zoals in Slay the Spire"): schatkist op verdieping 7, '
    'Snorlax op 13, elites en rust vanaf verdieping 5, zwakke gevechten op 1-3. Per act nu ±6 gevechten, ±1,9 elites, ±1,9 events (Slay 5-7 / 1-3 / 3-5). '
    'De kaart in dit rekenwerk is nu de C-code zelf (`Spire_GenerateMap` via gcc/ctypes, met schatkist en `Spire_WeighMap`), geen port meer.',
    '**HP-verlies per gevecht uit echte gevechten** (`matchups.py`, via `spire_calib.json`): types, abilities, patronen, DEFEND, '
    'openingsbescherming en klap-limiet tellen mee; eerder kwam het uit het gemiddelde-teammodel van encounters.py.',
    '**Doelen per gevecht** (encounters.py, `TARGET_ACT`): gewone gevechten 12/14/16 -> 15/17/19% (Jordi: "alle reguliere encounters waren super makkelijk"), '
    'elites 24/27/30 -> 22/24/26%, bazen 55/60/65 -> 35/38/40% (met types verliest een slecht passend team ±2x het gemiddelde; zie *Slechtste startcombinatie*). '
    'Per act zijn er bijna twee keer zoveel gevechten, dus de druk over een act blijft.',
]

OPEN = [
    '**Speelduur:** met 13 verdiepingen duurt een gewonnen run volgens het model ±2 uur (was ±75 min). Korter kan met `SPIRE_FLOORS` 11 '
    '(alles schaalt mee: kaart, schatkist in het midden, rekenwerk).',
    '**Winkans:** het model zit (gemiddeld niveau ±80%) nog boven Slay A0 (40-60%); de spreiding tussen teams komt nu uit echte gevechten. '
    'Houd in een paar runs bij hoeveel HP elk gevecht kost; dan kan `matchups.py` (de bot) geijkt worden.',
    '**Vastloper:** in een event waarvan elke optie geld of een type vraagt (*The Vending Machine*/Rotom) kun je niet verder zonder geld of Electric-type. '
    'Voorstel: B = weglopen als alles op slot zit (`spire_event.c`).',
]


def conclusions(sim, logs):
    g = logs['gemiddeld']
    arr = statistics.mean(g['arrive'][1]) if g['arrive'][1] else 0
    rooms = {t: statistics.mean(g['rooms'][(a, t)] / max(1, g['reached'][a]) for a in (1, 2, 3)) for t in (FIGHT, ELITE, EVENT, SHOP, REST)}
    rest = [(g['restchoice'][(a, 'heal')], g['restchoice'][(a, 'upgrade')]) for a in (1, 2, 3)]
    deaths = g['died']
    tot_d = max(1, sum(deaths.values()))
    boss = sum(c for (a, r), c in deaths.items() if r == 'baas') / tot_d
    elite = sum(c for (a, r), c in deaths.items() if r == 'elite') / tot_d
    allv = [x for v in g['event'].values() for x in v]
    return [
        'Per kamer zit de Spire in de Slay-banden: gang ±%s, elite ±%s, baas ±%s van de team-HP (gemiddeld niveau, alle acts).' % (
            pct(statistics.mean(x for a in (1, 2, 3) for x in g['loss'][(a, 'gevecht')])),
            pct(statistics.mean(x for a in (1, 2, 3) for x in g['loss'][(a, 'elite')])),
            pct(statistics.mean(x for a in (1, 2, 3) for x in g['loss'][(a, 'baas')]))),
        'Kamerverdeling per act (×15/%d om met Slay te vergelijken): %.1f gevechten, %.1f elites, %.1f events, %.1f winkels, %.1f rustplekken. '
        'Elites en rust kloppen; events en winkels zitten aan de onderkant van Slay.' % (
            sim.cfg['floors'], rooms[FIGHT] * 15 / sim.cfg['floors'], rooms[ELITE] * 15 / sim.cfg['floors'], rooms[EVENT] * 15 / sim.cfg['floors'],
            rooms[SHOP] * 15 / sim.cfg['floors'], rooms[REST] * 15 / sim.cfg['floors']),
        'HP-economie: aankomst bij de act-1-baas %s (Slay ±70-90%%); rustplekken heal/upgrade %s per act (Slay: vroeg vaak rusten, later smeden).' % (
            pct(arr), ', '.join('%d/%d' % (100 * h / max(1, h + u), 100 * u / max(1, h + u)) for h, u in rest)),
        'Doodsoorzaken: baas %s, elite %s, gang %s. In Slay zijn act-1-elites een grotere killer; hier weegt de bot het risico mee (elites alleen als je gezond bent).' % (
            pct(boss), pct(elite), pct(1 - boss - elite)),
        'Events zijn gemiddeld %.0f¥ waard (Slay ±50-100): iets minder dan een gevecht (±20¥ + een move). De dure ruil-events (betaal X voor Y tegen winkelprijs) '
        'zijn bewust neutraal; de type-opties maken ze voor het juiste team goed.' % statistics.mean(allv),
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runs', type=int, default=3000)
    ap.add_argument('--set', nargs='*', default=[])
    ap.add_argument('--no-write', action='store_true')
    ap.add_argument('--print', action='store_true')
    ap.add_argument('--save', help='kerngetallen naar dit bestand (de vóór-kolom van de voor/na-tabel)')
    ap.add_argument('--check-map', action='store_true')
    ap.add_argument('--events', action='store_true', help='EV per event tonen')
    args = ap.parse_args()
    cfg = load_config()
    for kv in args.set:
        k, v = kv.split('=')
        cfg[k] = eval(v)
    # kaartregels altijd controleren (Jordi: geen twee Marts/rustplekken/elites achter elkaar, ...)
    if check_map(cfg, 3000 if not args.check_map else 20000):
        raise SystemExit('kaartgenerator breekt een kaartregel (zie hierboven)')
    sim = Sim(cfg)
    # event-EV voor de planner: eerst een korte ronde
    lg = sim.run_many(400, 'gemiddeld', seed=7)
    sim.event_ev = statistics.mean(x for v in lg['event'].values() for x in v)
    logs = {k: sim.run_many(args.runs, k, seed=11) for k in SKILL}
    rows = summary_rows(sim, logs)
    rows = {k: fmtv(v) for k, v in rows.items()}
    for k, v in rows.items():
        print('%-28s %s' % (k, v))
    if args.events:
        g = logs['gemiddeld']
        for v, k in sorted(((statistics.mean(v), k) for k, v in g['event'].items()), reverse=True):
            print('  %-12s %6.0f' % (k, v))
    if args.save:
        with open(args.save, 'w', encoding='utf-8') as f:
            for k, v in rows.items():
                f.write('%s\t%s\n' % (k, v))
    sens = {}
    if not args.no_write or args.print:
        for m in (0.65, 1.25, 2.0):
            SKILL['×%.2f' % m] = m
            lg = sim.run_many(max(500, args.runs // 2), '×%.2f' % m, seed=13)
            sens[m] = lg['cleared'][3] / lg['n']
            del SKILL['×%.2f' % m]
        for k, m in (('goed', 0.8), ('gemiddeld', 1.0), ('slordig', 1.5)):
            sens[m] = logs[k]['cleared'][3] / logs[k]['n']
    if args.print:
        print('\n'.join(report(sim, logs, CHANGES, [], sens)))
    if args.no_write:
        return
    before = []
    bpath = os.path.join(HERE, 'runsim_before.txt')
    if os.path.exists(bpath):
        old = dict(l.rstrip('\n').split('\t') for l in open(bpath, encoding='utf-8'))
        for k, v in rows.items():
            if k in old:
                before.append((k, old[k], v))
    L = report(sim, logs, [c for c in CHANGES], before, sens)
    path = os.path.join(ROOT, 'SPIRE_BALANS.md')
    txt = open(path, encoding='utf-8').read()
    txt = txt.split('\n' + SECTION)[0].rstrip('\n') + '\n' + '\n'.join(L).rstrip('\n') + '\n'
    open(path, 'w', encoding='utf-8').write(txt)
    print('SPIRE_BALANS.md: sectie bijgewerkt')


if __name__ == '__main__':
    main()
