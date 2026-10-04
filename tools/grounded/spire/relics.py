#!/usr/bin/env python3
"""The Spire: relics (Project Grounded). Genereert include/spire_relics.h (enum) en src/data/spire_relics.h (tabel).

Relics = trainerspullen voor het hele team (zoals relics in Slay the Spire). De effecten zelf zitten in de C-code
(zoek op SPIRE_RELIC_<NAAM>); hier staan naam, icoon (item), zeldzaamheid, uitleg en het rekenmodel voor runsim.py.

Zeldzaamheid (zoals Slay):
  COMMON / UNCOMMON / RARE   elites (kies 1 uit 3; kans 50/33/17%), events, winkel
  SHOP                       alleen in de winkel (tweede relic-plek)
  BOSS                       na een baas (kies 1 uit 3): sterk, vaak met een nadeel
'conflicts': deze relic wordt niet aangeboden als je een van deze al hebt (anders is hij nutteloos).
'noshop': nooit in de winkel.

Het rekenmodel ('sim') gebruikt runsim.py:
  loss       factor op het HP-verlies per gevecht (getal of {'weak'/'normal'/'elite'/'boss': factor})
  heal_after extra procent heal na een gevecht      noheal  geen heal na een gevecht
  gold       factor op geld uit gevechten           nogold  geen geld uit gevechten
  rest       extra procent heal bij rusten           norest / noupgrade  die keuze bestaat niet meer
  maxhp      procentpunt max HP (beide)              upgrades  willekeurige upgrades bij het oppakken
  fullheal   volle heal bij het oppakken             act_heal  heal bij een nieuwe act (procent)
  shop       factor op winkelprijzen                 boss_heal heal vóór elk baasgevecht
  oran       extra heal na een gevecht onder 50%     elite_relics  aantal relic-beloningen per elite
  rest_upgrade / upgrade_bonus  extra upgrades bij rust / bij upgraden;  gamble  +procentpunt bij event-gokken
  pick       voorkeur van de bot bij het kiezen (hoger = liever)

Breedtes (FONT_SMALL_NARROW): naam max 62 px (kaart van 64 px; anders FONT_SMALL_NARROWER), uitleg max 2 regels van 216 px.

Gebruik: python3 tools/grounded/spire/relics.py
"""
import os, re, sys

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
OUT_ENUM = os.path.join(REPO, 'include/spire_relics.h')
OUT_DATA = os.path.join(REPO, 'src/data/spire_relics.h')

NAME_W = 62
DESC_W = 216
TIERS = ['COMMON', 'UNCOMMON', 'RARE', 'SHOP', 'BOSS']

R = []


def relic(key, name, item, tier, desc, sim=None, conflicts=(), noshop=False):
    R.append(dict(key=key, name=name, item=item, tier=tier, desc=desc, sim=sim or {}, conflicts=list(conflicts), noshop=noshop))


# --- COMMON (16) -------------------------------------------------------------------------------------
relic('BERRY_POUCH', 'Berry Pouch', 'BERRY_POUCH', 'COMMON', 'Heal 10% more HP\nafter every battle.',
      dict(heal_after=10, pick=6), conflicts=['MAX_MUSHROOMS'])
relic('AMULET_COIN', 'Amulet Coin', 'AMULET_COIN', 'COMMON', 'Earn 50% more money\nin every battle.',
      dict(gold=1.5, pick=4), conflicts=['RELIC_CROWN'])
relic('GUARD_SPEC', 'Guard Spec.', 'GUARD_SPEC', 'COMMON', 'DEFEND gives 30%\nmore Block.',
      dict(loss=0.96, pick=5))
relic('SOOTHE_BELL', 'Soothe Bell', 'SOOTHE_BELL', 'COMMON', 'Resting at camp heals\n30% more HP.',
      dict(rest=30, pick=3), conflicts=['AWAKENING'])
relic('X_SPEED', 'X Speed', 'X_SPEED', 'COMMON', 'Both your Pokémon start\nevery battle with +1 Speed.',
      dict(loss=0.95, pick=5))
relic('BLACK_FLUTE', 'Black Flute', 'BLACK_FLUTE', 'COMMON', 'Foes start every battle with -1 Speed.\nIt is that out of tune.',
      dict(loss=0.96, pick=4))
relic('RING_TARGET', 'Ring Target', 'RING_TARGET', 'COMMON', 'Elites start with 20% less HP.\nThey feel watched.',
      dict(loss={'elite': 0.82}, pick=5))
relic('QUICK_BALL', 'Quick Ball', 'QUICK_BALL', 'COMMON', 'Foes in normal battles start\nwith 15% less HP.',
      dict(loss={'weak': 0.87, 'normal': 0.87}, pick=5))
relic('IRON_PLATE', 'Iron Plate', 'IRON_PLATE', 'COMMON', 'First turn: both your Pokémon start\nwith Block, as if both DEFENDED.',
      dict(loss={'weak': 0.85, 'normal': 0.85, 'elite': 0.9, 'boss': 0.96}, pick=6))
relic('ADRENALINE_ORB', 'Adrenaline Orb', 'ADRENALINE_ORB', 'COMMON', 'First turn of every battle:\nyour moves deal 30% more.',
      dict(loss={'weak': 0.92, 'normal': 0.92, 'elite': 0.95, 'boss': 0.98}, pick=5))
relic('LAVA_COOKIE', 'Lava Cookie', 'LAVA_COOKIE', 'COMMON', 'Super-effective hits on your team\ndeal 20% less. Crunchy armor.',
      dict(loss=0.93, pick=5))
relic('HP_UP', 'HP Up', 'HP_UP', 'COMMON', '+8% max HP for both your Pokémon.\nTastes like chalk.',
      dict(maxhp=8, pick=5))
relic('PP_MAX', 'PP Max', 'PP_MAX', 'COMMON', 'When you get it: two random\nmoves are upgraded (+).',
      dict(upgrades=2, pick=6))
relic('ORAN_BERRY', 'Oran Berry', 'ORAN_BERRY', 'COMMON', 'After a battle, a Pokémon below\n50% HP heals 12% more.',
      dict(oran=12, pick=4), conflicts=['MAX_MUSHROOMS'])
relic('LEPPA_BERRY', 'Leppa Berry', 'LEPPA_BERRY', 'COMMON', 'After every battle, each move\ngets 3 PP back.',
      dict(loss=0.99, pick=2))
relic('LUCK_INCENSE', 'Luck Incense', 'LUCK_INCENSE', 'COMMON', 'Gambles in events succeed 20%\nmore often than the odds say.',
      dict(gamble=20, pick=2))

# --- UNCOMMON (15) -----------------------------------------------------------------------------------
relic('DIRE_HIT', 'Dire Hit', 'DIRE_HIT', 'UNCOMMON', 'Your Pokémon land\ncritical hits more often.',
      dict(loss=0.95, pick=6))
relic('MUSCLE_BAND', 'Muscle Band', 'MUSCLE_BAND', 'UNCOMMON', 'Your Pokémon deal\n10% more damage.',
      dict(loss=0.92, pick=7))
relic('WIDE_LENS', 'Wide Lens', 'WIDE_LENS', 'UNCOMMON', 'Your moves that hit\nboth foes lose no power.',
      dict(loss=0.97, pick=4))
relic('X_DEFENSE', 'X Defense', 'X_DEFENSE', 'UNCOMMON', 'Both your Pokémon start\nevery battle with +1 Defense.',
      dict(loss=0.87, pick=7))
relic('X_SP_DEF', 'X Sp. Def', 'X_SP_DEF', 'UNCOMMON', 'Both your Pokémon start\nevery battle with +1 Sp. Def.',
      dict(loss=0.87, pick=7))
relic('RUSTED_SHIELD', 'Rusted Shield', 'RUSTED_SHIELD', 'UNCOMMON', 'DEFEND on both Pokémon gives each\n85% of the Block instead of 60%.',
      dict(loss=0.96, pick=4))
relic('BERSERK_GENE', 'Berserk Gene', 'BERSERK_GENE', 'UNCOMMON', 'Below 50% HP, your Pokémon\ndeal 25% more damage.',
      dict(loss=0.96, pick=5))
relic('REAPER_CLOTH', 'Reaper Cloth', 'REAPER_CLOTH', 'UNCOMMON', 'Your moves deal 25% more to foes\nwith a status condition.',
      dict(loss=0.96, pick=5))
relic('POKE_FLUTE', 'Poké Flute', 'POKE_FLUTE', 'UNCOMMON', 'Resting at camp also upgrades\na random move. Snorlax hates it.',
      dict(rest_upgrade=1, pick=5), conflicts=['AWAKENING'])
relic('UP_GRADE', 'Up-Grade', 'UP_GRADE', 'UNCOMMON', 'Upgrading at camp also upgrades\na second, random move.',
      dict(upgrade_bonus=1, pick=5), conflicts=['DUBIOUS_DISC'])
relic('TM_CASE', 'TM Case', 'TM_CASE', 'UNCOMMON', 'Better move rewards: 25% rare and\n45% uncommon (normally 10/30).',
      dict(loss=0.97, pick=4))
relic('SWEET_HEART', 'Sweet Heart', 'SWEET_HEART', 'UNCOMMON', 'Skip a move reward (B) and both\nPokémon get +3% max HP instead.',
      dict(maxhp=4, pick=3))
relic('FOCUS_BAND', 'Focus Band', 'FOCUS_BAND', 'UNCOMMON', 'A Pokémon fighting alone deals 30%\nmore damage and takes 20% less.',
      dict(loss=0.96, pick=4))
relic('HYPER_POTION', 'Hyper Potion', 'HYPER_POTION', 'UNCOMMON', 'Before every boss battle,\nheal 30% HP.',
      dict(boss_heal=30, pick=5))

relic('SCANNER', 'Scanner', 'SCANNER', 'UNCOMMON', 'Your super-effective hits\ndeal 25% more damage.',
      dict(loss=0.92, pick=7))

# --- RARE (8) ----------------------------------------------------------------------------------------
relic('SACRED_ASH', 'Sacred Ash', 'SACRED_ASH', 'RARE', 'Fainted Pokémon come back\nwith 30% HP, not 1 HP.',
      dict(loss=0.98, pick=3))
relic('X_ATTACK', 'X Attack', 'X_ATTACK', 'RARE', 'Both your Pokémon start elite and\nboss battles with +1 Attack.',
      dict(loss={'elite': 0.85, 'boss': 0.87}, pick=7))
relic('X_SP_ATK', 'X Sp. Atk', 'X_SP_ATK', 'RARE', 'Both your Pokémon start elite and\nboss battles with +1 Sp. Atk.',
      dict(loss={'elite': 0.85, 'boss': 0.87}, pick=7))
relic('SHED_SHELL', 'Shed Shell', 'SHED_SHELL', 'RARE', 'Block no longer vanishes at the\nend of a turn: half of it stays.',
      dict(loss=0.93, pick=6))
relic('RESIST_FEATHER', 'Resist Feather', 'RESIST_FEATHER', 'RARE', 'Once per battle, each Pokémon\nsurvives a knockout hit with 1 HP.',
      dict(loss=0.92, pick=8))
relic('ACRO_BIKE', 'Acro Bike', 'ACRO_BIKE', 'RARE', '3 times: hop to any room on the\nnext floor, path or no path.',
      dict(loss=0.98, pick=3))
relic('RAZOR_CLAW', 'Razor Claw', 'RAZOR_CLAW', 'RARE', 'Your critical hits deal 2x\ndamage instead of 1.5x.',
      dict(loss=0.96, pick=4))

relic('IRON_BALL', 'Iron Ball', 'IRON_BALL', 'RARE', 'Every hit on your team does 2% of\nmax HP less. Heavy, but worth it.',
      dict(loss=0.86, pick=7))

# --- SHOP (3) ----------------------------------------------------------------------------------------
relic('RAINBOW_PASS', 'Rainbow Pass', 'RAINBOW_PASS', 'SHOP', 'Everything in the Poké Mart\ncosts 30% less.',
      dict(shop=0.7, pick=3))
relic('HEART_SCALE', 'Heart Scale', 'HEART_SCALE', 'SHOP', 'The Move Relearner always\ncosts 25¥. It is in love.',
      dict(pick=1))
relic('BIG_MALASADA', 'Big Malasada', 'BIG_MALASADA', 'SHOP', 'When you get it: +10% max HP\nand a full heal. Alolan cardio.',
      dict(maxhp=10, fullheal=1, pick=5))

# --- BOSS (8) ----------------------------------------------------------------------------------------
relic('AWAKENING', 'Awakening', 'AWAKENING', 'BOSS', 'Your Pokémon deal 20% more damage.\nNo more resting at camp.',
      dict(loss=0.84, norest=1, pick=7), conflicts=['DUBIOUS_DISC'], noshop=True)
relic('RELIC_CROWN', 'Relic Crown', 'RELIC_CROWN', 'BOSS', 'Start every battle with +1 Attack and\n+1 Sp. Atk. Battles pay no money.',
      dict(loss=0.72, nogold=1, pick=8), noshop=True)
relic('ODD_KEYSTONE', 'Odd Keystone', 'ODD_KEYSTONE', 'BOSS', 'Start every battle with +1 Defense and\n+1 Sp. Def. All intents read ???.',
      dict(loss=0.8, pick=7), noshop=True)
relic('METEORITE', 'Meteorite', 'METEORITE', 'BOSS', 'Your Pokémon deal 35% more damage,\nbut also take 15% more.',
      dict(loss=0.86, pick=6), noshop=True)
relic('DUBIOUS_DISC', 'Dubious Disc', 'DUBIOUS_DISC', 'BOSS', 'Your team takes 20% less damage.\nPorygon2 refuses to upgrade moves.',
      dict(loss=0.8, noupgrade=1, pick=7), conflicts=['AWAKENING'], noshop=True)
relic('MAX_MUSHROOMS', 'Max Mushrooms', 'MAX_MUSHROOMS', 'BOSS', '+25% max HP for both Pokémon.\nNo more healing after battles.',
      dict(maxhp=25, noheal=1, pick=5), noshop=True)
relic('STAR_PIECE', 'Star Piece', 'STAR_PIECE', 'BOSS', 'Elites give two relic rewards\ninstead of one.',
      dict(elite_relics=2, pick=6), noshop=True)
relic('GRACIDEA', 'Gracidea', 'GRACIDEA', 'BOSS', 'Every new act fully heals your\nteam (normally 40%).',
      dict(act_heal=100, pick=4), noshop=True)


# De eerste acht (v0.8.103) houden hun nummer, zodat een gepauzeerde run zijn relics houdt (bitveld in de save).
FIRST = ['BERRY_POUCH', 'AMULET_COIN', 'GUARD_SPEC', 'DIRE_HIT', 'MUSCLE_BAND', 'WIDE_LENS', 'SOOTHE_BELL', 'SACRED_ASH']
R.sort(key=lambda r: FIRST.index(r['key']) if r['key'] in FIRST else len(FIRST))


# --- controle en uitvoer ---------------------------------------------------------------------------
def load_widths(name):
    src = open(os.path.join(REPO, 'src/fonts.c')).read()
    m = re.search(name + r'\[\]\s*=\s*\{(.*?)\};', src, re.S)
    widths = [int(x) for x in re.findall(r'\d+', re.sub(r'//.*', '', m.group(1)))]
    cm = {}
    for line in open(os.path.join(REPO, 'charmap.txt'), encoding='utf-8'):
        mm = re.match(r"^'(.+?)'\s*=\s*([0-9A-Fa-f]{2})\s*$", line)
        if mm:
            ch = mm.group(1).replace("\\'", "'")
            code = int(mm.group(2), 16)
            if len(ch) == 1 and code < len(widths):
                cm.setdefault(ch, widths[code])
    return cm


def width(s, table):
    return sum(table.get(ch, 6) for ch in s)


def check():
    errors = []
    ws = load_widths('gFontSmallNarrowLatinGlyphWidths')
    wsn = load_widths('gFontSmallNarrowerLatinGlyphWidths')
    items_h = open(os.path.join(REPO, 'include/constants/items.h')).read()
    keys = [r['key'] for r in R]
    if len(set(keys)) != len(keys):
        errors.append('dubbele sleutel')
    for r in R:
        if r['tier'] not in TIERS:
            errors.append('%s: onbekende zeldzaamheid %s' % (r['key'], r['tier']))
        if not re.search(r'#define ITEM_%s\b' % r['item'], items_h):
            errors.append('%s: onbekend item ITEM_%s' % (r['key'], r['item']))
        # te breed in FONT_SMALL_NARROW: de kaart valt terug op FONT_SMALL_NARROWER (zoals Heavy-Duty Boots)
        if width(r['name'], ws) > NAME_W and width(r['name'], wsn) > NAME_W:
            errors.append('%s: naam te breed (%d px)' % (r['key'], width(r['name'], wsn)))
        lines = r['desc'].split('\n')
        if len(lines) > 2:
            errors.append('%s: uitleg heeft %d regels' % (r['key'], len(lines)))
        for line in lines:
            if width(line, ws) > DESC_W:
                errors.append('%s: uitlegregel te breed (%d px): %s' % (r['key'], width(line, ws), line))
        if '"' in r['desc'] or '"' in r['name']:
            errors.append('%s: geen " in teksten (charmap)' % r['key'])
        for c in r['conflicts']:
            if c not in keys:
                errors.append('%s: onbekend conflict %s' % (r['key'], c))
        if len(r['conflicts']) > 2:
            errors.append('%s: max 2 conflicten' % r['key'])
    return errors


def c_str(s):
    return 'COMPOUND_STRING("%s")' % s.replace('\n', '\\n')


def write():
    enum = ['// Gegenereerd door tools/grounded/spire/relics.py; niet met de hand bewerken.',
            '#ifndef GUARD_SPIRE_RELICS_H', '#define GUARD_SPIRE_RELICS_H', '',
            '// Relics = trainerspullen voor het hele team (vasthouditems zijn iets anders: één per Pokémon, zie de winkel).',
            'enum SpireRelic', '{']
    for r in R:
        enum.append('    SPIRE_RELIC_%s, // %s: %s' % (r['key'], r['tier'].lower(), r['desc'].replace('\n', ' ')))
    enum += ['    SPIRE_RELIC_COUNT,', '};', '',
             'enum SpireRelicTier', '{'] + ['    SPIRE_RELIC_TIER_%s,' % t for t in TIERS] + \
            ['    SPIRE_RELIC_TIER_COUNT,', '};', '', '#endif // GUARD_SPIRE_RELICS_H', '']
    with open(OUT_ENUM, 'w', encoding='utf-8') as f:
        f.write('\n'.join(enum))
    data = ['// Gegenereerd door tools/grounded/spire/relics.py; niet met de hand bewerken.',
            '// {icoon (item), naam, uitleg, zeldzaamheid, niet in de winkel, niet aanbieden als je deze al hebt}', '',
            'const struct SpireRelicInfo gSpireRelics[SPIRE_RELIC_COUNT] =', '{']
    for r in R:
        conf = (['SPIRE_RELIC_' + c for c in r['conflicts']] + ['SPIRE_RELIC_COUNT'] * 2)[:2]
        data.append('    [SPIRE_RELIC_%s] = {ITEM_%s, %s, %s, SPIRE_RELIC_TIER_%s, %s, {%s}},' % (
            r['key'], r['item'], c_str(r['name']), c_str(r['desc']), r['tier'], 'TRUE' if r['noshop'] else 'FALSE', ', '.join(conf)))
    data += ['};', '']
    with open(OUT_DATA, 'w', encoding='utf-8') as f:
        f.write('\n'.join(data))


def main():
    errors = check()
    if errors:
        print('\n'.join(errors))
        sys.exit(1)
    write()
    count = {t: sum(1 for r in R if r['tier'] == t) for t in TIERS}
    print('%d relics %s -> %s, %s' % (len(R), count, os.path.relpath(OUT_ENUM, REPO), os.path.relpath(OUT_DATA, REPO)))


if __name__ == '__main__':
    main()
