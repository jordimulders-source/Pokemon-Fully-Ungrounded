"""Rekenscript voor de balans van The Spire (zie SPIRE_DESIGN.md).

Simuleert gevechten met de echte schadeformule (Gen 5+, zoals expansion):
2 rentals van de speler (altijd doubles) tegen lakeien, elites of een baas,
per act, met HP-vermenigvuldigers en DEFEND (blok).

Gebruik:
    python3 balance.py                 # standaardtabel
    python3 balance.py --hp 3 2.5 4 5  # HP-mult speler, lakei, elite, baas
    python3 balance.py --sweep         # rooster van HP-vermenigvuldigers
    python3 balance.py --run           # hele acts naspelen (heal na gevecht, rustplek)
"""
import argparse, random, statistics
import gamedata

SPECIES = gamedata.load_species()
CHART = gamedata.load_typechart()

LEVEL = 50
EV = 84          # Factory-achtig: 84 in elke stat
IV = 31
CRIT_CHANCE = 1 / 24
SPREAD = 0.75

# --- pools -----------------------------------------------------------------
PLAYER = {
    1: ['IVYSAUR', 'CHARMELEON', 'WARTORTLE', 'GROVYLE', 'COMBUSKEN', 'MARSHTOMP', 'HAUNTER', 'MACHOKE',
        'GRAVELER', 'KADABRA', 'LAIRON', 'VIBRAVA', 'SHELGON', 'GABITE', 'MONFERNO', 'PRINPLUP', 'GROTLE',
        'LUXIO', 'ZWEILOUS', 'FRAXURE', 'SLIGGOO', 'KIRLIA', 'DRAGONAIR', 'PUPITAR', 'METANG',
        'CORVISQUIRE', 'RABOOT', 'DRIZZILE', 'THWACKEY', 'HATTREM'],
    2: ['VENUSAUR', 'CHARIZARD', 'BLASTOISE', 'SCEPTILE', 'BLAZIKEN', 'SWAMPERT', 'GENGAR', 'MACHAMP',
        'GOLEM', 'ESPEON', 'AGGRON', 'FLYGON', 'SALAMENCE', 'GARCHOMP', 'INFERNAPE', 'EMPOLEON', 'TORTERRA',
        'LUXRAY', 'HYDREIGON', 'HAXORUS', 'GOODRA', 'GARDEVOIR', 'DRAGONITE', 'TYRANITAR', 'METAGROSS',
        'CORVIKNIGHT', 'CINDERACE', 'INTELEON', 'RILLABOOM', 'HATTERENE'],
}
PLAYER[3] = PLAYER[2]

LACKEY = {
    1: ['PIDGEOTTO', 'NUZLEAF', 'LOMBRE', 'ELECTRIKE', 'GLOOM', 'FLAAFFY', 'SKIPLOOM', 'SWABLU', 'NUMEL',
        'SPOINK', 'BALTOY', 'CORPHISH', 'SHUPPET', 'DUSKULL', 'SNORUNT', 'GRAVELER', 'MACHOKE', 'LAIRON'],
    2: ['PIDGEOT', 'SHIFTRY', 'LUDICOLO', 'MANECTRIC', 'VILEPLUME', 'AMPHAROS', 'JUMPLUFF', 'ALTARIA',
        'CAMERUPT', 'GRUMPIG', 'CLAYDOL', 'CRAWDAUNT', 'BANETTE', 'DUSCLOPS', 'GLALIE', 'GOLEM', 'MACHAMP'],
    3: ['STARAPTOR', 'BRELOOM', 'GYARADOS', 'ROTOM_WASH', 'ROSERADE', 'AMPHAROS', 'TOGEKISS', 'ALTARIA',
        'TORKOAL', 'BRONZONG', 'CLAYDOL', 'SCIZOR', 'MISMAGIUS', 'DUSKNOIR', 'WEAVILE', 'RHYPERIOR', 'CONKELDURR'],
}
ELITE = {
    1: ['ARCANINE', 'GYARADOS', 'SCIZOR', 'LUCARIO', 'MAMOSWINE', 'MAGNEZONE', 'TOXICROAK', 'HERACROSS'],
    2: ['SALAMENCE', 'METAGROSS', 'GARCHOMP', 'TYRANITAR', 'DRAGONITE', 'VOLCARONA', 'KINGDRA', 'GENGAR'],
    3: ['DIALGA', 'PALKIA', 'GROUDON', 'KYOGRE', 'ZEKROM', 'RESHIRAM', 'LUNALA', 'SOLGALEO'],
}
BOSS = {
    1: ['MILOTIC', 'AGGRON', 'FLYGON', 'ABSOL', 'CRADILY', 'ARMALDO', 'SHIFTRY', 'CLAYDOL'],
    2: ['GROUDON', 'KYOGRE', 'DIALGA', 'GIRATINA_ALTERED', 'ZEKROM', 'RESHIRAM'],
    3: ['RAYQUAZA', 'ETERNATUS', 'NECROZMA_ULTRA', 'ZACIAN_CROWNED', 'MEWTWO'],
}

# movekracht per act: (STAB, dekking)
PLAYER_POWER = {1: (70, 60), 2: (85, 75), 3: (95, 85)}
ENEMY_POWER = {'lackey': {1: (65, 0), 2: (75, 0), 3: (85, 0)},
               'elite': {1: (80, 70), 2: (90, 80), 3: (100, 90)},
               'boss': {1: (75, 65), 2: (80, 70), 3: (85, 75)}}


def stat(base, hp=False, level=LEVEL):
    x = (2 * base + IV + EV // 4) * level // 100
    return x + level + 10 if hp else x + 5


class Mon:
    def __init__(self, name, hp_mult, power, level=LEVEL, spread_every=0, boost=0):
        s = SPECIES[name]
        self.name, self.types = name, s['types']
        self.maxhp = int(stat(s['hp'], True, level) * hp_mult)
        self.hp = self.maxhp
        self.atk, self.df = stat(s['atk'], level=level), stat(s['def'], level=level)
        self.spa, self.spd = stat(s['spa'], level=level), stat(s['spd'], level=level)
        self.spe = stat(s['spe'], level=level)
        self.level = level
        # totem-achtige boost voor bazen: +boost stages op beide aanvalsstats
        mult = (2 + boost) / 2
        self.atk, self.spa = int(self.atk * mult), int(self.spa * mult)
        cat = 'PHYSICAL' if s['atk'] >= s['spa'] else 'SPECIAL'
        stab, cov = power
        self.moves = [(t, stab, cat, False) for t in self.types]
        if cov:
            # dekking: het type dat zo veel mogelijk soorten super effectief raakt, geen STAB
            best = max((t for t in gamedata.TYPES[1:-1] if t not in self.types and t != 'MYSTERY'),
                       key=lambda t: sum(CHART[t][d] for d in gamedata.TYPES[1:-1] if d != 'MYSTERY'))
            self.moves.append((best, cov, cat, False))
        self.spread_every = spread_every
        if spread_every:
            self.moves.append((self.types[0], stab, cat, True))
        self.block = 0
        self.support = False   # lakei in een baasgevecht: buft liever de baas
        self.rage = 1.0        # schademultiplier door buffs van lakeien

    @property
    def alive(self):
        return self.hp > 0

    def defense_factor(self):
        # verhouding tot een "gemiddelde" verdediging (base 80 → ±100 op lv 50)
        return ((self.df + self.spd) / 2) / stat(80, level=self.level)


def eff(mtype, target):
    e = 1.0
    for t in target.types:
        e *= CHART[mtype][t]
    return e


def damage(att, move, target, rng=None, spread=False, crit=None):
    mtype, power, cat, _ = move
    a, d = (att.atk, target.df) if cat == 'PHYSICAL' else (att.spa, target.spd)
    base = ((2 * att.level // 5 + 2) * power * a // d) // 50 + 2
    if spread:
        base = int(base * SPREAD)
    if rng is not None:
        if crit is None:
            crit = rng.random() < CRIT_CHANCE
        if crit:
            base = int(base * 1.5)
        base = base * rng.randint(85, 100) // 100
    else:
        base = base * 0.925 * (1 + CRIT_CHANCE * 0.5)
    if mtype in att.types:
        base = base * 1.5
    return int(base * eff(mtype, target) * att.rage)


def best_move(att, foes, turn):
    """Beste (move, doel) op verwachte schade; spread als die er is en het de beurt is."""
    live = [f for f in foes if f.alive]
    if not live:
        return None
    opts = []
    for mv in att.moves:
        if mv[3]:
            if att.spread_every and turn % att.spread_every == 0:
                return (mv, None)
            continue
        for f in live:
            dmg = damage(att, mv, f)
            kill = dmg >= f.hp
            opts.append(((kill, dmg / f.maxhp if not kill else 1 + 1 / f.hp), mv, f))
    opts.sort(key=lambda o: o[0], reverse=True)
    return (opts[0][1], opts[0][2])


def apply_hit(att, mv, target, rng, spread):
    if rng.random() * 100 >= 100:   # (accuracy 100 aangenomen)
        return 0
    dmg = damage(att, mv, target, rng, spread)
    absorbed = min(dmg, target.block)
    target.block -= absorbed
    dmg -= absorbed
    target.hp = max(0, target.hp - dmg)
    return dmg


def block_amount(mon, act, cfg):
    return int(mon.maxhp * cfg['defend_pct'] * mon.defense_factor() * cfg['act_block'][act])


def fight(players, foes, act, cfg, rng, reserve=(), max_turns=40):
    """Eén gevecht. players/foes: lijsten met Mon. reserve: golven voor de tegenstander."""
    reserve = list(reserve)
    turns = 0
    defends = 0
    for turn in range(1, max_turns + 1):
        turns = turn
        # intenties van de tegenstander (vastgelegd vóór de speler kiest)
        intents = []
        for f in foes:
            if f.alive and f.support and rng.random() < cfg['support_rate']:
                intents.append((f, ('SUPPORT', None)))
            elif f.alive:
                bm = best_move(f, players, turn) if rng.random() < 0.7 else \
                    (rng.choice([m for m in f.moves if not m[3]]), rng.choice([p for p in players if p.alive]))
                intents.append((f, bm))
        # speler: DEFEND-beleid
        actions = []
        live_p = [p for p in players if p.alive]
        incoming = {id(p): 0 for p in live_p}
        for f, (mv, tgt) in intents:
            if mv == 'SUPPORT':
                continue
            for p in (live_p if mv[3] else [tgt]):
                incoming[id(p)] += damage(f, mv, p, spread=mv[3])
        for p in live_p:
            p.block = 0
        if cfg['defend'] and len(live_p) == 2:
            # verdedig als een klap > drempel van een maxhp, met de zwakste aanvaller
            danger = [p for p in live_p if incoming[id(p)] >= cfg['defend_threshold'] * p.maxhp]
            if danger:
                dmg_out = {id(p): max(damage(p, mv, f) for mv in p.moves for f in foes if f.alive)
                           if any(f.alive for f in foes) else 0 for p in live_p}
                defender = min(live_p, key=lambda p: dmg_out[id(p)])
                defends += 1
                amt = block_amount(defender, act, cfg)
                if len(danger) == 2:
                    for p in live_p:
                        p.block += int(amt * cfg['split'])
                else:
                    danger[0].block += amt
                actions.append(('defend', defender))
        acting = [p for p in live_p if not any(a[1] is p for a in actions)]
        order = [(p, 'p') for p in acting] + [(f, 'f') for f, _ in intents]
        order.sort(key=lambda x: x[0].spe + rng.random(), reverse=True)
        intent_of = {id(f): bm for f, bm in intents}
        for mon, side in order:
            if not mon.alive:
                continue
            if side == 'p':
                bm = best_move(mon, foes, turn)
                if not bm:
                    break
                mv, tgt = bm
                for t in ([f for f in foes if f.alive] if mv[3] else [tgt]):
                    if t.alive:
                        apply_hit(mon, mv, t, rng, mv[3])
            else:
                mv, tgt = intent_of[id(mon)]
                if mv == 'SUPPORT':
                    for ally in foes:
                        if ally.alive and ally is not mon:
                            ally.rage = min(cfg['rage_cap'], ally.rage + cfg['rage_step'])
                    continue
                targets = [p for p in players if p.alive] if mv[3] else [tgt if tgt.alive else None]
                if targets == [None]:
                    alt = [p for p in players if p.alive]
                    targets = alt[:1]
                for t in targets:
                    apply_hit(mon, mv, t, rng, mv[3])
        # golven: gevallen lakei vervangen
        for i, f in enumerate(foes):
            if not f.alive and reserve:
                foes[i] = reserve.pop(0)
        for p in players:
            p.block = 0
        if not any(p.alive for p in players):
            return dict(win=False, turns=turns, defends=defends)
        if not any(f.alive for f in foes) and not reserve:
            return dict(win=True, turns=turns, defends=defends)
    return dict(win=False, turns=turns, defends=defends, timeout=True)


def make_players(act, cfg, rng):
    names = rng.sample(PLAYER[act], 2)
    return [Mon(n, cfg['hp_player'], PLAYER_POWER[act]) for n in names]


def make_foes(kind, act, cfg, rng):
    lv = cfg['enemy_level'][act]
    if kind == 'normal':
        names = rng.sample(LACKEY[act], cfg['normal_count'])
        mons = [Mon(n, cfg['hp_lackey'], ENEMY_POWER['lackey'][act], lv) for n in names]
        return mons[:2], mons[2:]
    if kind == 'elite':
        return [Mon(rng.choice(ELITE[act]), cfg['hp_elite'], ENEMY_POWER['elite'][act], lv)], []
    boss = Mon(rng.choice(BOSS[act]), cfg['hp_boss'], ENEMY_POWER['boss'][act], lv, spread_every=3,
               boost=cfg['boss_boost'])
    lackeys = [Mon(n, cfg['hp_lackey'], ENEMY_POWER['lackey'][act], lv) for n in rng.sample(LACKEY[act], 2)]
    for l in lackeys:
        l.support = True
    return [boss, lackeys[0]], lackeys[1:]


DEFAULT = dict(hp_player=4.0, hp_lackey=1.0, hp_elite=2.5, hp_boss=4.5, defend=True, defend_pct=0.15,
               defend_threshold=0.25, split=0.6, act_block={1: 1.0, 2: 1.25, 3: 1.5},
               enemy_level={1: 48, 2: 50, 3: 52}, boss_boost=0,
               support_rate=0.6, rage_step=0.15, rage_cap=1.6,
               normal_count=2, heal_after=0.20, rest_heal=0.50)


def summarize(kind, act, cfg, n=600, seed=1):
    rng = random.Random(seed)
    res = []
    for _ in range(n):
        p = make_players(act, cfg, rng)
        f, r = make_foes(kind, act, cfg, rng)
        out = fight(p, f, act, cfg, rng, r)
        out['lost'] = sum(1 - x.hp / x.maxhp for x in p) / 2
        out['fainted'] = sum(1 for x in p if not x.alive)
        res.append(out)
    wins = [r for r in res if r['win']]
    return dict(kind=kind, act=act, win=len(wins) / n, turns=statistics.mean(r['turns'] for r in res),
                lost=statistics.mean(r['lost'] for r in wins) if wins else 1.0,
                ko1=sum(1 for r in wins if r['fainted']) / max(1, len(wins)),
                defends=statistics.mean(r['defends'] for r in res))


def hit_table(cfg):
    """Gemiddelde % HP per klap (neutraal, gemiddelde rol) per act."""
    rows = []
    for act in (1, 2, 3):
        lv = cfg['enemy_level'][act]
        pl = [Mon(n, cfg['hp_player'], PLAYER_POWER[act]) for n in PLAYER[act]]
        for kind, pool, hpm, pw in (('lakei', LACKEY, cfg['hp_lackey'], ENEMY_POWER['lackey']),
                                    ('elite', ELITE, cfg['hp_elite'], ENEMY_POWER['elite']),
                                    ('baas', BOSS, cfg['hp_boss'], ENEMY_POWER['boss'])):
            en = [Mon(n, hpm, pw[act], lv, boost=cfg['boss_boost'] if kind == 'baas' else 0) for n in pool[act]]
            # STAB-klap, typevoordeel uitgemiddeld
            p2e = statistics.mean(damage(p, p.moves[0], e) / e.maxhp for p in pl for e in en)
            e2p = statistics.mean(damage(e, e.moves[0], p) / p.maxhp for p in pl for e in en)
            blk = statistics.mean(block_amount(p, act, cfg) / p.maxhp for p in pl)
            rows.append((act, kind, p2e, e2p, blk))
    return rows


def print_tables(cfg):
    print('HP-mult: speler %.1f, lakei %.1f, elite %.1f, baas %.1f | DEFEND %d%% × verdediging × act %s'
          % (cfg['hp_player'], cfg['hp_lackey'], cfg['hp_elite'], cfg['hp_boss'], cfg['defend_pct'] * 100,
             cfg['act_block']))
    print('\nGemiddelde STAB-klap (incl. typevoordeel/-nadeel), in % van max HP:')
    print('act  vijand   speler→vijand  vijand→speler  blok')
    for act, kind, p2e, e2p, blk in hit_table(cfg):
        print('%3d  %-6s  %12.0f%%  %12.0f%%  %4.0f%%' % (act, kind, p2e * 100, e2p * 100, blk * 100))
    print('\nGevechten (vers team, %s):' % ('met DEFEND' if cfg['defend'] else 'zonder DEFEND'))
    print('act  soort    winst  beurten  HP kwijt  ≥1 flauw  defends')
    for act in (1, 2, 3):
        for kind in ('normal', 'elite', 'boss'):
            s = summarize(kind, act, cfg)
            print('%3d  %-7s %5.0f%%  %7.1f  %7.0f%%  %7.0f%%  %7.1f'
                  % (act, kind, s['win'] * 100, s['turns'], s['lost'] * 100, s['ko1'] * 100, s['defends']))


def run_act(act, cfg, rng, layout=('normal', 'normal', 'elite', 'normal', 'rest', 'normal', 'elite', 'rest', 'boss')):
    heal_after, rest_heal = cfg['heal_after'], cfg['rest_heal']
    players = make_players(act, cfg, rng)
    for step in layout:
        if step == 'rest':
            for p in players:
                p.hp = min(p.maxhp, max(1, p.hp) + int(p.maxhp * rest_heal))
            continue
        for p in players:
            if not p.alive:
                p.hp = 1
        f, r = make_foes(step, act, cfg, rng)
        out = fight(players, f, act, cfg, rng, r)
        if not out['win']:
            return step
        for p in players:
            if p.alive:
                p.hp = min(p.maxhp, p.hp + int(p.maxhp * heal_after))
    return 'klaar'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hp', nargs=4, type=float, metavar=('SPELER', 'LAKEI', 'ELITE', 'BAAS'))
    ap.add_argument('--defend', type=float, help='blok als fractie van max HP (standaard 0.15)')
    ap.add_argument('--nodefend', action='store_true')
    ap.add_argument('--sweep', action='store_true')
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--set', nargs='*', default=[], metavar='SLEUTEL=WAARDE',
                    help='andere instelling, bijv. normal_count=2 heal_after=0.2')
    a = ap.parse_args()
    cfg = dict(DEFAULT)
    if a.hp:
        cfg.update(hp_player=a.hp[0], hp_lackey=a.hp[1], hp_elite=a.hp[2], hp_boss=a.hp[3])
    if a.defend is not None:
        cfg['defend_pct'] = a.defend
    if a.nodefend:
        cfg['defend'] = False
    for kv in a.set:
        k, v = kv.split('=')
        cfg[k] = type(DEFAULT[k])(eval(v))
    if a.sweep:
        print('HP speler  lakei/elite/baas  | act1 normaal/elite/baas: beurten, HP kwijt, winst')
        for hp in (2, 2.5, 3, 4):
            for scale in (0.67, 1.0, 1.33):
                c = dict(cfg, hp_player=hp, hp_lackey=hp * scale * 0.67, hp_elite=hp * scale * 1.33,
                         hp_boss=hp * scale * 2)
                line = ['%.1f  %.1f/%.1f/%.1f |' % (hp, c['hp_lackey'], c['hp_elite'], c['hp_boss'])]
                for kind in ('normal', 'elite', 'boss'):
                    s = summarize(kind, 1, c, n=300)
                    line.append('%4.1f %3.0f%% %3.0f%%' % (s['turns'], s['lost'] * 100, s['win'] * 100))
                print('  '.join(line))
        return
    if a.run:
        rng = random.Random(7)
        for act in (1, 2, 3):
            outs = [run_act(act, cfg, rng) for _ in range(400)]
            print('act %d: gehaald %.0f%%, gestrand: %s' % (
                act, outs.count('klaar') / 4,
                ', '.join('%s %.0f%%' % (k, outs.count(k) / 4) for k in ('normal', 'elite', 'boss'))))
        return
    print_tables(cfg)


if __name__ == '__main__':
    main()
