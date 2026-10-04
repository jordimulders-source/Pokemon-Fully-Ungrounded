"""The Spire: biomes, ontmoetingen en bazen (zie SPIRE_DESIGN.md, 'Vijanden').

Elke ontmoeting is een kleine puzzel, naar het voorbeeld van Slay the Spire 1 en 2, maar met Pokémon-mechanics
(abilities, items, moves, totem-boosts) en een vast patroon waar dat helpt. Vijanden lijken op de monsters uit
Slay the Spire (Vine Shambler = Tangela, Fogmog = Amoonguss, ...).

Gebruik:
    python3 encounters.py          # controleert alles, schrijft src/data/spire_encounters.h en het rapport
                                   # (onderaan SPIRE_BALANS.md, sectie 'Ontmoetingen')

Velden per vijand:
    s  soort                    m  moves (moeten in de leerset staan; verboden moves mogen niet)
    a  ability (uit de eigen lijst; leeg = normaal)          i  vasthoud-item
    lv level t.o.v. het act-level (48/50/52)               hp HP-vermenigvuldiger (1 = normaal)
    b  totem-boosts bij de start, bijv. {'def': 1}          p  vast patroon: slots 1-4 die herhalen (intentie!)
    g  'SLEEP3' = begint 3 beurten in slaap (gewone slaapstatus); 'HIDDEN' = intentie onleesbaar (Wobbuffet: steen-papier-schaar). Verder alleen Pokémon-mechanics (Jordi): Ritual = Rage,
       opladen = Quiver Dance/Machine Learning/Acupressure, start-buff = totem-boost, Gremlin Nob = Defiant.
Per ontmoeting: field = beginstatus (TRICK_ROOM, TAILWIND_OPPONENT, GRASSY_TERRAIN, ...), hint = uitleg (codex).
"""
import math, os, re, sys
import spiredata
import spire_pool as P

ROOT = spiredata.ROOT
SPECIES, MOVES = P.SPECIES, P.MOVES
ITEMS = set(re.findall(r'#define (ITEM_\w+)', open(os.path.join(ROOT, 'include/constants/items.h')).read()))
ITEMS |= set(re.findall(r'\b(ITEM_\w+)\s*[=,]', open(os.path.join(ROOT, 'include/constants/items.h')).read()))

ACT_LEVEL = {1: 100, 2: 100, 3: 100}   # Jordi: alles lv 100, level is geen knop

# aliassen (SPECIES_SHELLOS = SPECIES_SHELLOS_WEST) en de volledige leersets uit alle games (van expansion)
ALIAS = dict(re.findall(r'#define SPECIES_(\w+)\s+SPECIES_(\w+)', open(os.path.join(ROOT, 'include/constants/species.h')).read()))
for _a, _b in list(ALIAS.items()):
    if _a not in SPECIES and _b in SPECIES:
        SPECIES[_a] = SPECIES[_b]
import json as _json
_ALL = _json.load(open(os.path.join(ROOT, 'tools/learnset_helpers/build/all_learnables.json')))
UNIVERSAL = {'BIDE', 'FRUSTRATION', 'HIDDEN_POWER', 'MIMIC', 'NATURAL_GIFT', 'RAGE', 'RETURN', 'SECRET_POWER',
             'SUBSTITUTE', 'TERA_BLAST'}

# ---------------------------------------------------------------------------------------------
# Biomes: twee per act (zoals Overgrowth/Underdocks in StS2), ieder met eigen vijanden en kaartachtergrond.

BIOMES = [
    dict(key='GROVE', act=1, name='Overgrown Grove', desc='Moss, fungus and things that bite.'),
    dict(key='DOCKS', act=1, name='Sunken Docks', desc='Brine, rust and something in the fog.'),
    dict(key='HIVE', act=2, name='The Hive', desc='Sand, wax and a lot of legs.'),
    dict(key='FROST', act=2, name='Frostbite Hollow', desc='Ice that remembers every footstep.'),
    dict(key='COURT', act=3, name='Gilded Court', desc='Knights, clocks and a judge who never blinks.'),
    dict(key='ABYSS', act=3, name='The Abyss', desc='Where the tower keeps what it ate.'),
]

E = lambda **k: k  # noqa: E731

# ---------------------------------------------------------------------------------------------
# Ontmoetingen. kind: weak (eerste twee verdiepingen), normal, elite.

ENCOUNTERS = {
    # ===== ACT 1 – OVERGROWN GROVE =========================================================
    'GROVE': [
        E(kind='weak', name='Fuzzy Crawlers', hint='Cutiefly saps your Sp. Atk first. Grubbin just bites.',
          foes=[dict(s='GRUBBIN', m=['BUG_BITE', 'MUD_SLAP', 'STRING_SHOT', 'BITE']),
                dict(s='CUTIEFLY', m=['STRUGGLE_BUG', 'FAIRY_WIND', 'ABSORB', 'STUN_SPORE'], p=[1, 2, 2, 3])]),
        E(kind='weak', name='Snapping Berries', hint='Cherubi grows every other turn. Pick it first.',
          foes=[dict(s='CHERUBI', m=['GROWTH', 'MAGICAL_LEAF', 'TACKLE', 'HELPING_HAND'], p=[1, 2]),
                dict(s='BOUNSWEET', m=['RAZOR_LEAF', 'RAPID_SPIN', 'MAGICAL_LEAF', 'TEETER_DANCE'])]),
        E(kind='weak', name='Leaf Slimes', hint='Slow, sticky and full of powder.',
          foes=[dict(s='GULPIN', m=['POISON_GAS', 'SLUDGE', 'POUND_', 'YAWN']),
                dict(s='SHROOMISH', m=['ABSORB', 'STUN_SPORE', 'HEADBUTT', 'LEECH_SEED'])]),
        E(kind='normal', name='Vine Shambler', hint='Tangela traps you, then drains you. Bring fire.',
          foes=[dict(s='TANGELA', m=['VINE_WHIP', 'BIND', 'MEGA_DRAIN', 'INGRAIN'], a='REGENERATOR', p=[1, 2, 3, 3]),
                dict(s='SEWADDLE', m=['BUG_BITE', 'RAZOR_LEAF', 'STRING_SHOT', 'PROTECT'])]),
        E(kind='normal', name='Fogmog', hint='Amoonguss pulls every hit towards itself. Spread moves ignore it.',
          foes=[dict(s='FOONGUS', m=['RAGE_POWDER', 'MEGA_DRAIN', 'ASTONISH', 'GROWTH'], a='EFFECT_SPORE', p=[1, 2, 1, 4]),
                dict(s='PARAS', m=['FURY_CUTTER', 'LEECH_LIFE', 'STUN_SPORE', 'SCRATCH_'], a='DRY_SKIN')]),
        E(kind='normal', name='Overgrown Statue', hint='Sudowoodo hardens before it hits. Hit it before the third turn.',
          foes=[dict(s='SUDOWOODO', m=['ROCK_POLISH', 'ROCK_THROW', 'LOW_KICK', 'SLAM'], a='STURDY', p=[1, 2, 2, 3]),
                dict(s='BONSLY', m=['ROCK_THROW', 'FAKE_TEARS', 'COPYCAT', 'TACKLE'])]),
        E(kind='normal', name='Slithering Strangler', hint='Ekans wraps you up and paralyses you. Kill it, the rest is noise.',
          foes=[dict(s='EKANS', m=['WRAP', 'GLARE', 'POISON_STING', 'BITE'], p=[1, 2, 3, 4]),
                dict(s='SEEDOT', m=['BULLET_SEED', 'GROWTH', 'HARDEN', 'NATURE_POWER'])]),
        E(kind='normal', name='Mawler', hint='Teddiursa roars once, then claws. A plain damage race.',
          foes=[dict(s='TEDDIURSA', m=['FURY_SWIPES', 'LICK', 'BABY_DOLL_EYES', 'SLASH'], a='QUICK_FEET'),
                dict(s='SKWOVET', m=['BITE', 'STUFF_CHEEKS', 'TAIL_WHIP', 'BULLET_SEED'], i='ITEM_ORAN_BERRY')]),
        E(kind='normal', name='Jungle Ambush', hint='Two in the grass. Grass Terrain heals them every turn.',
          field='GRASSY_TERRAIN',
          foes=[dict(s='BELLSPROUT', m=['VINE_WHIP', 'WRAP', 'ACID', 'SLEEP_POWDER'], p=[1, 3, 1, 4]),
                dict(s='HOPPIP', m=['FAIRY_WIND', 'BULLET_SEED', 'TAILWIND', 'STUN_SPORE'], p=[3, 1, 2, 4])]),
        E(kind='normal', name='Moonlight Recital', hint='Two Clefairy wave their fingers. Nobody knows what happens next. Not even them.',
          foes=[dict(s='CLEFAIRY', m=['METRONOME', 'MOONLIGHT', 'FOLLOW_ME', 'DISARMING_VOICE'], a='MAGIC_GUARD', p=[1, 1, 3, 1, 2]),
                dict(s='CLEFAIRY', m=['METRONOME', 'MOONLIGHT', 'COSMIC_POWER', 'DISARMING_VOICE'], a='FRIEND_GUARD', p=[1, 1, 1, 2])]),
        E(kind='elite', name='Gremlin Nob', hint='Primeape hates being lowered (Defiant) and every hit makes it angrier (Rage).',
          foes=[dict(s='PRIMEAPE', m=['RAGE', 'CROSS_CHOP', 'SCREECH', 'STOMPING_TANTRUM'], a='DEFIANT', hp=2.4, lv=-2,
                     p=[1, 3, 2, 1, 4]),
                dict(s='MANKEY', m=['RAGE', 'LOW_KICK', 'FOCUS_ENERGY', 'SEISMIC_TOSS_'], a='ANGER_POINT')]),
        E(kind='elite', name='Byrdonis', hint='Trumbeak shouts louder every turn. Echoed Voice doubles until it is stopped.',
          foes=[dict(s='TRUMBEAK', m=['ECHOED_VOICE', 'PECK', 'ROCK_BLAST', 'SUPERSONIC'], a='SKILL_LINK', hp=2.5,
                     p=[1, 1, 1, 1, 4]),
                dict(s='PIKIPEK', m=['PECK', 'GROWL', 'ECHOED_VOICE', 'SUPERSONIC'])]),
        E(kind='elite', name='Bygone Effigy', hint='Snorlax sleeps for three turns. Prepare, then pray.',
          foes=[dict(s='SNORLAX', m=['CURSE', 'BODY_SLAM', 'HEAVY_SLAM', 'YAWN'], a='THICK_FAT', hp=2.0, lv=-4, g='SLEEP3',
                     p=[1, 2, 1, 3]),
                dict(s='MUNCHLAX', m=['METRONOME', 'LICK', 'DEFENSE_CURL', 'RECYCLE_'])]),
        E(kind='elite', name='Phrog Parasite', hint='Pyukumuku spits its guts at whoever lands the killing blow.',
          foes=[dict(s='PYUKUMUKU', m=['COUNTER', 'MIRROR_COAT', 'PURIFY', 'TOXIC'], a='INNARDS_OUT', hp=2.5,
                     p=[4, 1, 2, 3]),
                dict(s='CROAGUNK', m=['POISON_JAB', 'MUD_SLAP', 'TAUNT', 'FEINT_ATTACK_'], a='DRY_SKIN')]),
    ],
    # ===== ACT 1 – SUNKEN DOCKS ============================================================
    'DOCKS': [
        E(kind='weak', name='Corpse Slugs', hint='When one falls, the other grows. Kill them together.',
          foes=[dict(s='SHELLOS', m=['MUD_SLAP', 'WATER_PULSE', 'RECOVER', 'MUD_BOMB_'], a='STORM_DRAIN'),
                dict(s='SHELLOS', m=['MUD_SLAP', 'WATER_PULSE', 'HARDEN', 'BODY_SLAM'], a='STICKY_HOLD')]),
        E(kind='weak', name='Toadpoles', hint='Spiky in front, splashing behind.',
          foes=[dict(s='TYMPOLE', m=['BUBBLE_BEAM', 'ROUND', 'UPROAR', 'GROWL']),
                dict(s='POLIWAG', m=['WATER_GUN', 'HYPNOSIS', 'DOUBLE_SLAP', 'BUBBLE_BEAM'], p=[1, 1, 2])]),
        E(kind='weak', name='Seapunks', hint='Tentacool kicks, Clauncher shoots. Neither is very brave.',
          foes=[dict(s='TENTACOOL', m=['ACID', 'WRAP', 'SUPERSONIC', 'WATER_PULSE']),
                dict(s='CLAUNCHER', m=['WATER_GUN', 'VISE_GRIP', 'AQUA_JET', 'SWORDS_DANCE'], a='MEGA_LAUNCHER')]),
        E(kind='weak', name='Just Two Magikarp', hint='Two Magikarp. Flail gets scary at low HP: finish them, do not tickle them.',
          foes=[dict(s='MAGIKARP', m=['TACKLE', 'FLAIL', 'BOUNCE_'], a='RATTLED', p=[1, 2]),
                dict(s='MAGIKARP', m=['TACKLE', 'FLAIL'], a='SWIFT_SWIM', p=[2, 1])]),
        E(kind='normal', name='Secret Santa', hint='Delibird hands out Presents. Some explode, some heal you. Delibird does not know which.',
          foes=[dict(s='DELIBIRD', m=['PRESENT', 'ICE_SHARD', 'DRILL_PECK', 'FAKE_OUT'], a='HUSTLE', p=[1, 1, 1, 3]),
                dict(s='WINGULL', m=['WATER_PULSE', 'AIR_CUTTER', 'MIST', 'SUPERSONIC'], a='HYDRATION')]),
        E(kind='normal', name='Gremlin Mercs', hint='Purrloin steals and flees with your gold. Stop it first.',
          foes=[dict(s='PURRLOIN', m=['FAKE_OUT', 'FURY_SWIPES', 'SAND_ATTACK', 'ASSURANCE'], a='UNBURDEN', i='ITEM_AMULET_COIN',
                     p=[1, 4, 3, 4]),
                dict(s='IMPIDIMP', m=['FAKE_TEARS', 'DRAINING_KISS', 'FLATTER', 'SUCKER_PUNCH'], a='PRANKSTER')]),
        E(kind='normal', name='Living Fog', hint='Koffing wipes every boost with Clear Smog and Haze. Plan without them.',
          foes=[dict(s='KOFFING', m=['SMOG', 'CLEAR_SMOG', 'SLUDGE', 'HAZE'], a='NEUTRALIZING_GAS', p=[2, 3, 4, 3]),
                dict(s='STUNKY', m=['POISON_GAS', 'BITE', 'SCREECH', 'FEINT']) ]),
        E(kind='normal', name='Haunted Ship', hint='Dhelmise anchors down and swings. Its partner keeps it company.',
          foes=[dict(s='DHELMISE', m=['ANCHOR_SHOT', 'GIGA_DRAIN', 'GROWTH', 'SHADOW_BALL'], a='STEELWORKER', lv=-6, p=[3, 1, 2, 4]),
                dict(s='FRILLISH', m=['WATER_PULSE', 'HEX', 'WILL_O_WISP', 'RECOVER'], a='CURSED_BODY')]),
        E(kind='normal', name='Sewer Clam', hint='Shellder shells up and sharpens. Break it before it opens.',
          foes=[dict(s='SHELLDER', m=['WITHDRAW', 'ICICLE_SPEAR', 'WATER_GUN', 'SUPERSONIC'], a='SKILL_LINK', p=[1, 2, 1, 2]),
                dict(s='CLAMPERL', m=['WHIRLPOOL', 'WATER_PULSE', 'IRON_DEFENSE', 'CONFUSE_RAY_'])]),
        E(kind='normal', name='Two-Tailed Rats', hint='Tandemaus never stops. Rattata just bites.',
          foes=[dict(s='TANDEMAUS', m=['POPULATION_BOMB', 'ECHOED_VOICE', 'SUPER_FANG_', 'TICKLE']),
                dict(s='RATTATA_ALOLA', m=['BITE', 'QUICK_ATTACK', 'FOCUS_ENERGY', 'PURSUIT'], a='HUSTLE')]),
        E(kind='normal', name='Cultists', hint='Wooper and Lotad chant for rain. Then the water hits harder every turn.',
          foes=[dict(s='WOOPER', m=['RAIN_DANCE', 'MUD_SHOT', 'WATER_PULSE', 'YAWN'], a='DAMP', p=[1, 2, 3, 2]),
                dict(s='LOTAD', m=['RAIN_DANCE', 'BUBBLE_BEAM', 'MEGA_DRAIN', 'GROWL'], a='SWIFT_SWIM', p=[2, 2, 3])]),
        E(kind='elite', name='Terror Eel', hint='Eelektross holds back until half HP, then lets go. Burst it from half to zero.',
          foes=[dict(s='EELEKTROSS', m=['CRUNCH', 'DISCHARGE', 'COIL', 'WILD_CHARGE'], a='LEVITATE', lv=-6, hp=2.0,
                     i='ITEM_PETAYA_BERRY', p=[3, 1, 2]),
                dict(s='TYNAMO', m=['SPARK', 'TACKLE', 'THUNDER_WAVE', 'CHARGE_BEAM'])]),
        E(kind='elite', name='Skulking Colony', hint='Corsola ignores small hits. Hit hard or not at all.',
          foes=[dict(s='CORSOLA_GALAR', m=['CURSE', 'HEX', 'STRENGTH_SAP', 'NIGHT_SHADE_'], a='WEAK_ARMOR', hp=2.5,
                     i='ITEM_EVIOLITE', p=[2, 3, 2, 1]),
                dict(s='MAREANIE', m=['TOXIC', 'POISON_JAB', 'BITE', 'RECOVER'], a='MERCILESS')]),
        E(kind='elite', name='Phantasmal Gardeners', hint='Two ghosts that hide behind Substitute. Multi-hit moves break it.',
          foes=[dict(s='FRILLISH', m=['SUBSTITUTE', 'WATER_PULSE', 'HEX', 'WILL_O_WISP'], a='CURSED_BODY', hp=1.6, p=[1, 4, 3, 2]),
                dict(s='DREEPY', m=['SUBSTITUTE', 'INFESTATION', 'ASTONISH', 'QUICK_ATTACK'], a='INFILTRATOR', hp=1.6, p=[1, 2, 3, 2])]),
    ],
    # ===== ACT 2 – THE HIVE ================================================================
    'HIVE': [
        E(kind='weak', name='Bowlbugs', hint='Shuckle carries a bowl of juice. It will drink it.',
          foes=[dict(s='SHUCKLE', m=['STICKY_WEB_', 'ROCK_THROW', 'TOXIC', 'POWER_TRICK_'], a='CONTRARY', i='ITEM_BERRY_JUICE'),
                dict(s='DWEBBLE', m=['ROCK_TOMB', 'BUG_BITE', 'SHELL_SMASH', 'SMACK_DOWN'], p=[3, 1, 2])]),
        E(kind='weak', name='Exoskeletons', hint='Nincada barely notices one big hit. Many small ones work.',
          foes=[dict(s='NINCADA', m=['FURY_SWIPES', 'MUD_SLAP', 'HARDEN', 'DIG_'], a='COMPOUND_EYES', i='ITEM_FOCUS_SASH'),
                dict(s='NINCADA', m=['FURY_SWIPES', 'SAND_ATTACK', 'ABSORB', 'SCRATCH_'], i='ITEM_FOCUS_SASH')]),
        E(kind='weak', name='Tunneler', hint='Drilbur digs in. Excavated foes hit from below.',
          foes=[dict(s='DRILBUR', m=['METAL_CLAW', 'MUD_SLAP', 'HONE_CLAWS', 'ROCK_SLIDE'], a='SAND_RUSH', p=[3, 1, 4]),
                dict(s='SANDILE', m=['SAND_TOMB', 'BITE', 'SANDSTORM', 'TORMENT'], a='MOXIE', p=[3, 1, 2])]),
        E(kind='normal', name='Hunter Killer', hint='Yanmega gets faster every turn. Kill it or out-wall it.',
          foes=[dict(s='YANMEGA', m=['AIR_SLASH', 'BUG_BUZZ', 'DETECT', 'ANCIENT_POWER'], a='SPEED_BOOST', lv=-4),
                dict(s='COMBEE', m=['BUG_BITE', 'GUST', 'SWEET_SCENT_', 'STRUGGLE_BUG'], a='HUSTLE')]),
        E(kind='normal', name='Louse Progenitor', hint='Forretress curls up, then hits you with its own Defense.',
          foes=[dict(s='FORRETRESS', m=['IRON_DEFENSE', 'BUG_BITE', 'GYRO_BALL', 'BODY_PRESS'], a='STURDY', p=[1, 2, 1, 4, 3]),
                dict(s='VENONAT', m=['STRUGGLE_BUG', 'POISON_POWDER', 'PSYBEAM', 'SIGNAL_BEAM'])]),
        E(kind='normal', name='Mytes', hint='Ariados and Galvantula web you up and poison everything.',
          foes=[dict(s='ARIADOS', m=['TOXIC_THREAD', 'POISON_JAB', 'SUCKER_PUNCH', 'BUG_BITE'], a='SNIPER', p=[1, 2, 3, 2]),
                dict(s='GALVANTULA', m=['ELECTROWEB', 'BUG_BUZZ', 'THUNDER_WAVE', 'ENERGY_BALL'], a='COMPOUND_EYES', lv=-4)]),
        E(kind='normal', name='Ovicopter', hint='Vespiquen heals and powers up her drones. Drones first? Or the queen?',
          foes=[dict(s='VESPIQUEN', m=['HEAL_ORDER', 'DEFEND_ORDER', 'ATTACK_ORDER', 'POWER_GEM'], a='PRESSURE', p=[2, 3, 1, 3]),
                dict(s='COMBEE', m=['BUG_BITE', 'GUST', 'STRUGGLE_BUG', 'BUG_BUZZ'], a='HUSTLE')]),
        E(kind='normal', name='Spiny Toad', hint='Ferrothorn hurts you every time you touch it. Use special moves.',
          foes=[dict(s='FERROTHORN', m=['GYRO_BALL', 'POWER_WHIP', 'LEECH_SEED', 'SPIKY_SHIELD_'], a='IRON_BARBS', lv=-6,
                     i='ITEM_ROCKY_HELMET', p=[3, 1, 2]),
                dict(s='CACNEA', m=['NEEDLE_ARM', 'SAND_ATTACK', 'LEECH_SEED', 'SUCKER_PUNCH'], a='WATER_ABSORB')]),
        E(kind='normal', name='Sandpit Worms', hint='Sandstorm, Sand Tomb and a pit full of jaws.',
          foes=[dict(s='TRAPINCH', m=['SAND_TOMB', 'BITE', 'BULLDOZE', 'FEINT'], a='ARENA_TRAP'),
                dict(s='SILICOBRA', m=['SANDSTORM', 'SAND_TOMB', 'COIL', 'BRUTAL_SWING'], a='SAND_SPIT', p=[1, 3, 2, 4])]),
        E(kind='elite', name='Decimillipede', hint='Scolipede accelerates and sharpens. Steelworkers and Ghosts laugh.',
          foes=[dict(s='SCOLIPEDE', m=['MEGAHORN', 'POISON_JAB', 'SWORDS_DANCE', 'PROTECT'], a='SPEED_BOOST', hp=2.4, lv=-2,
                     p=[3, 1, 4, 2, 1]),
                dict(s='WHIRLIPEDE', m=['IRON_DEFENSE', 'POISON_TAIL', 'BUG_BITE', 'TOXIC'], a='POISON_POINT')]),
        E(kind='elite', name='Entomancer', hint='Every hit on Ribombee scatters pollen. Few big hits beat many small ones.',
          foes=[dict(s='RIBOMBEE', m=['QUIVER_DANCE', 'POLLEN_PUFF', 'MOONBLAST', 'STUN_SPORE'], a='SHIELD_DUST', hp=2.2,
                     i='ITEM_LEFTOVERS', p=[1, 3, 2, 3]),
                dict(s='VOLBEAT', m=['TAIL_GLOW', 'BUG_BUZZ', 'ENCORE', 'THUNDERBOLT'], a='PRANKSTER')]),
        E(kind='elite', name='The Insatiable', hint='Sandaconda swallows the pit around you. Five turns, then it bites for real.',
          foes=[dict(s='SANDACONDA', m=['COIL', 'SAND_TOMB', 'STONE_EDGE', 'EARTHQUAKE'], a='SAND_SPIT', hp=2.6, lv=-2,
                     p=[2, 1, 1, 3, 4]),
                dict(s='GLIGAR', m=['U_TURN_', 'KNOCK_OFF_', 'POISON_JAB', 'DIG_'], a='HYPER_CUTTER')]),
    ],
    # ===== ACT 2 – FROSTBITE HOLLOW ========================================================
    'FROST': [
        E(kind='weak', name='Snow Hares', hint='Two that hide in the snow and bite your ankles.',
          foes=[dict(s='SNORUNT', m=['ICE_SHARD', 'BITE', 'HEADBUTT', 'PROTECT']),
                dict(s='CUBCHOO', m=['FROST_BREATH', 'BRINE', 'FURY_SWIPES', 'CHARM'], a='SLUSH_RUSH')]),
        E(kind='weak', name='Living Icicles', hint='Bergmite hardens. Its friend hits the cracks.',
          foes=[dict(s='BERGMITE', m=['IRON_DEFENSE', 'ICY_WIND', 'BITE', 'RAPID_SPIN'], a='STURDY', p=[1, 2, 3]),
                dict(s='SNOM', m=['STRUGGLE_BUG', 'POWDER_SNOW_', 'ICY_WIND', 'BUG_BITE'], a='ICE_SCALES')]),
        E(kind='weak', name='Seal Pups', hint='Spheal rolls faster every turn. Interrupt it.',
          foes=[dict(s='SPHEAL', m=['ICE_BALL_', 'BRINE', 'DEFENSE_CURL', 'ROLLOUT'], a='THICK_FAT'),
                dict(s='SEEL', m=['ICY_WIND', 'HEADBUTT', 'ENCORE', 'AQUA_JET'], a='HYDRATION')]),
        E(kind='normal', name='Frost Byrds', hint='Delibird hands out presents. One of them is a bomb.',
          foes=[dict(s='DELIBIRD', m=['PRESENT', 'ICE_SHARD', 'DRILL_PECK', 'BRAVE_BIRD'], a='HUSTLE'),
                dict(s='SWABLU', m=['SING', 'MIST', 'DRAGON_BREATH', 'ROUND'], a='CLOUD_NINE', p=[1, 3, 2, 3])]),
        E(kind='normal', name='Glass Sentries', hint='Three crystals in a row: Cryogonal and its reflection. Haze erases your work.',
          foes=[dict(s='CRYOGONAL', m=['REFLECT', 'LIGHT_SCREEN', 'FREEZE_DRY', 'HAZE'], a='SNOW_WARNING', lv=-6, p=[1, 3, 2, 3, 4]),
                dict(s='SNOVER', m=['ICE_SHARD', 'RAZOR_LEAF', 'MIST', 'INGRAIN'], a='SNOW_WARNING')]),
        E(kind='normal', name='Beartic Brute', hint='Beartic rolls up its sleeves twice, then swings.',
          foes=[dict(s='BEARTIC', m=['SWORDS_DANCE', 'ICICLE_CRASH', 'SUPERPOWER', 'AQUA_JET'], a='SWIFT_SWIM', lv=-6, p=[1, 2, 2, 1, 3]),
                dict(s='CUBCHOO', m=['FROST_BREATH', 'CHARM', 'FURY_SWIPES', 'BRINE'], a='SLUSH_RUSH')]),
        E(kind='normal', name='The Lost and the Forgotten', hint='Froslass and Glalie steal your strength with every turn you wait.',
          foes=[dict(s='FROSLASS', m=['WILL_O_WISP', 'ICE_SHARD', 'HEX', 'CONFUSE_RAY'], a='CURSED_BODY', lv=-6, p=[1, 3, 4, 3]),
                dict(s='GLALIE', m=['FREEZE_DRY', 'CRUNCH', 'SCARY_FACE', 'ICE_FANG'], a='MOODY', lv=-6)]),
        E(kind='normal', name='Avalanche', hint='Piloswine thaws slowly, then rolls downhill.',
          foes=[dict(s='PILOSWINE', m=['ICICLE_CRASH', 'EARTHQUAKE', 'AMNESIA', 'ICE_SHARD'], a='THICK_FAT', p=[3, 1, 2]),
                dict(s='SWINUB', m=['POWDER_SNOW_', 'MUD_SLAP', 'ICE_SHARD', 'ENDURE'], a='OBLIVIOUS')]),
        E(kind='normal', name='Rock, Paper, Wobbuffet', hint='You cannot read Wobbuffet. Counter or Mirror Coat? Hit the other way, or wait it out.',
          foes=[dict(s='WOBBUFFET', m=['COUNTER', 'MIRROR_COAT', 'SAFEGUARD', 'ENCORE'], a='SHADOW_TAG', hp=1.4, g='HIDDEN'),
                dict(s='WYNAUT', m=['CHARM', 'ENCORE', 'AMNESIA', 'SAFEGUARD'], a='SHADOW_TAG', p=[1, 2, 4, 3])]),
        E(kind='normal', name='Ice Dancers', hint='Spinda makes everyone dizzy, Jynx kisses the dizzy ones to sleep.',
          foes=[dict(s='SPINDA', m=['TEETER_DANCE', 'SUCKER_PUNCH', 'ICE_PUNCH', 'FAKE_OUT'], a='TANGLED_FEET', p=[4, 1, 3, 2, 3]),
                dict(s='JYNX', m=['LOVELY_KISS', 'ICE_BEAM', 'FAKE_TEARS', 'PSYCHIC'], a='DRY_SKIN', p=[3, 1, 2, 4, 2])]),
        E(kind='elite', name='Lagavulin Matriarch', hint='Avalugg sleeps behind a shell. Wake it on your terms.',
          foes=[dict(s='AVALUGG', m=['CURSE', 'AVALANCHE', 'BODY_PRESS', 'RECOVER'], a='STURDY', hp=2.6, lv=-4, g='SLEEP3',
                     p=[1, 3, 2, 3, 4]),
                dict(s='BERGMITE', m=['ICY_WIND', 'BITE', 'IRON_DEFENSE', 'PROTECT'])]),
        E(kind='elite', name='Frozen Knight', hint='Glalie freezes your moves with Torment, then Explosion if it must.',
          foes=[dict(s='GLALIE', m=['TORMENT', 'FREEZE_DRY', 'CRUNCH', 'ICE_FANG'], a='MOODY', hp=2.4, lv=-2,
                     i='ITEM_SITRUS_BERRY', p=[1, 2, 3, 2, 3, 4]),
                dict(s='SNOVER', m=['BLIZZARD', 'INGRAIN', 'RAZOR_LEAF', 'MIST'], a='SNOW_WARNING')]),
        E(kind='elite', name='Kaiser Crab', hint='Crabominable and Kingler fight as one. Kill one and the other goes berserk.',
          foes=[dict(s='CRABOMINABLE', m=['ICE_HAMMER', 'CLOSE_COMBAT', 'BULK_UP', 'PROTECT'], a='ANGER_POINT', hp=1.7, lv=-4,
                     p=[3, 1, 2]),
                dict(s='KINGLER', m=['CRABHAMMER', 'X_SCISSOR', 'SWORDS_DANCE', 'PROTECT'], a='HYPER_CUTTER', hp=1.7, lv=-4,
                     p=[1, 2, 3, 1])]),
    ],
    # ===== ACT 3 – GILDED COURT ============================================================
    'COURT': [
        E(kind='weak', name='Turret Operator', hint='Bastiodon guards, Octillery fires. Through the shield or around it?',
          foes=[dict(s='BASTIODON', m=['WIDE_GUARD', 'IRON_DEFENSE', 'METAL_BURST', 'BODY_PRESS'], a='STURDY', lv=-6, p=[1, 2, 4, 3]),
                dict(s='OCTILLERY', m=['OCTAZOOKA', 'BULLET_SEED', 'ROCK_BLAST', 'LOCK_ON_'], a='SNIPER', lv=-6)]),
        E(kind='weak', name='Scrolls of Biting', hint='Unown and Bronzor. One reads, one rings.',
          foes=[dict(s='BRONZOR', m=['CONFUSE_RAY', 'GYRO_BALL', 'EXTRASENSORY', 'IRON_DEFENSE'], a='LEVITATE'),
                dict(s='SIGILYPH', m=['AIR_SLASH', 'PSYSHOCK', 'COSMIC_POWER', 'TAILWIND'], a='MAGIC_GUARD', lv=-6)]),
        E(kind='weak', name='Devoted Sculptor', hint='Smeargle paints itself stronger every turn. Two turns is all it needs.',
          foes=[dict(s='SMEARGLE', m=['SWORDS_DANCE', 'SHELL_SMASH', 'EXTREME_SPEED', 'SPORE'], a='MOODY', p=[1, 3, 1, 3]),
                dict(s='MR_MIME', m=['REFLECT', 'LIGHT_SCREEN', 'PSYCHIC', 'DAZZLING_GLEAM'], a='FILTER', lv=-6)]),
        E(kind='normal', name='Axebots', hint='Two blades that sharpen each other. Kill one quickly.',
          foes=[dict(s='BISHARP', m=['SWORDS_DANCE', 'IRON_HEAD', 'SUCKER_PUNCH', 'NIGHT_SLASH'], a='DEFIANT', lv=-4, p=[1, 2, 3, 2]),
                dict(s='DOUBLADE', m=['SWORDS_DANCE', 'SHADOW_SNEAK', 'SACRED_SWORD', 'IRON_HEAD'], a='NO_GUARD', i='ITEM_EVIOLITE')]),
        E(kind='normal', name='Fabricator', hint='Magnezone builds an electric field. Ground types are not impressed.',
          field='ELECTRIC_TERRAIN',
          foes=[dict(s='MAGNEZONE', m=['DISCHARGE', 'FLASH_CANNON', 'MAGNET_RISE_', 'THUNDER_WAVE'], a='ANALYTIC', lv=-4),
                dict(s='KLINKLANG', m=['SHIFT_GEAR', 'GEAR_GRIND', 'WILD_CHARGE', 'SCREECH'], a='CLEAR_BODY', p=[1, 2, 3, 2])]),
        E(kind='normal', name='Owl Magistrate', hint='Noctowl flies up for a turn, then delivers the verdict.',
          foes=[dict(s='NOCTOWL', m=['ROOST', 'AIR_SLASH', 'HYPNOSIS', 'MOONBLAST'], a='TINTED_LENS', p=[3, 2, 2, 4, 1]),
                dict(s='XATU', m=['FUTURE_SIGHT', 'TAILWIND', 'PSYCHIC', 'NIGHT_SHADE_'], a='MAGIC_BOUNCE', p=[2, 1, 3, 3])]),
        E(kind='normal', name='Frog Knight', hint='Sirfetch\'d charges at half HP. Keep your guard up when it bleeds.',
          foes=[dict(s='SIRFETCHD', m=['SWORDS_DANCE', 'LEAF_BLADE', 'BRAVE_BIRD', 'CLOSE_COMBAT'], a='SCRAPPY', lv=-4,
                     i='ITEM_SALAC_BERRY', p=[3, 2, 1, 4]),
                dict(s='TOXICROAK', m=['FAKE_OUT', 'POISON_JAB', 'SUCKER_PUNCH', 'TAUNT'], a='DRY_SKIN', lv=-4)]),
        E(kind='normal', name='Globe Head', hint='Rotom swaps your items around. Then it hits the weak spot.',
          foes=[dict(s='ROTOM_WASH', m=['HYDRO_PUMP', 'THUNDERBOLT', 'WILL_O_WISP', 'PROTECT'], a='LEVITATE', lv=-4),
                dict(s='CHIMECHO', m=['HEAL_PULSE', 'PSYCHIC', 'YAWN', 'HEAL_BELL'], a='LEVITATE', p=[3, 2, 1, 2])]),
        E(kind='normal', name='Slimed Berserker', hint='Goodra just keeps coming. Its slime makes contact hurt.',
          foes=[dict(s='GOODRA', m=['DRAGON_PULSE', 'SLUDGE_BOMB', 'RAIN_DANCE', 'POWER_WHIP'], a='GOOEY', lv=-6),
                dict(s='MUK', m=['GUNK_SHOT', 'CURSE', 'SHADOW_SNEAK', 'TOXIC'], a='STICKY_HOLD', lv=-6, p=[4, 2, 1, 2])]),
        E(kind='normal', name='The Sloth', hint='Slaking hits like a truck every other turn and naps in between (Truant). Guard, then punish.',
          foes=[dict(s='SLAKING', m=['DOUBLE_EDGE', 'EARTHQUAKE', 'SLACK_OFF', 'BULK_UP'], a='TRUANT', hp=1.2),
                dict(s='VIGOROTH', m=['ENCORE', 'SLASH', 'TAUNT', 'BULK_UP'], a='VITAL_SPIRIT', p=[3, 2, 1, 2])]),
        E(kind='elite', name='Knights Trio', hint='Aegislash shields, Escavalier smashes. Kill order is everything.',
          foes=[dict(s='AEGISLASH', m=['KINGS_SHIELD', 'SHADOW_BALL', 'SACRED_SWORD', 'SHADOW_SNEAK'], a='STANCE_CHANGE', hp=2.0,
                     lv=-4, p=[2, 1, 3, 1]),
                dict(s='ESCAVALIER', m=['SWORDS_DANCE', 'MEGAHORN', 'IRON_HEAD', 'DRILL_RUN'], a='OVERCOAT', hp=1.6, lv=-4,
                     p=[1, 2, 3, 2])]),
        E(kind='elite', name='Mecha Knight', hint='Metagross charges, then hammers. Telegraphed, but very loud.',
          foes=[dict(s='METAGROSS', m=['AGILITY', 'METEOR_MASH', 'ZEN_HEADBUTT', 'BULLET_PUNCH'], a='CLEAR_BODY', hp=2.4, lv=-4,
                     i='ITEM_ASSAULT_VEST_', p=[1, 2, 2, 3]),
                dict(s='BRONZONG', m=['TRICK_ROOM', 'GYRO_BALL', 'HYPNOSIS', 'EXTRASENSORY'], a='HEATPROOF', p=[1, 3, 2, 4])]),
        E(kind='elite', name='Soul Nexus', hint='Chandelure. No tricks. Just a lot of fire.',
          foes=[dict(s='CHANDELURE', m=['FLAMETHROWER', 'SHADOW_BALL', 'WILL_O_WISP', 'HEAT_WAVE'], a='FLASH_FIRE', hp=2.6, lv=-2,
                     i='ITEM_LIFE_ORB'),
                dict(s='LAMPENT', m=['HEX', 'WILL_O_WISP', 'CONFUSE_RAY', 'FLAME_BURST_'], a='FLAME_BODY')]),
    ],
    # ===== ACT 3 – THE ABYSS ===============================================================
    'ABYSS': [
        E(kind='weak', name='Darklings', hint='Three Zubat would revive each other. Here it is two, and they drain.',
          foes=[dict(s='GOLBAT', m=['LEECH_LIFE', 'CONFUSE_RAY', 'CROSS_POISON', 'MEAN_LOOK_'], a='INFILTRATOR', lv=-6),
                dict(s='SABLEYE', m=['FAKE_OUT', 'RECOVER', 'SHADOW_CLAW', 'WILL_O_WISP'], a='PRANKSTER', lv=-6)]),
        E(kind='weak', name='Writhing Mass', hint='Ditto becomes whatever hits it hardest.',
          foes=[dict(s='DITTO', m=['TRANSFORM'], a='IMPOSTER', i='ITEM_CHOICE_SCARF', lv=-2),
                dict(s='MUK_ALOLA', m=['KNOCK_OFF_', 'POISON_JAB', 'CRUNCH', 'MINIMIZE'], a='POISON_TOUCH', lv=-8)]),
        E(kind='weak', name='Exploders', hint='Electrode charges, taunts, zaps. Knock it out with a punch and it pops (Aftermath).',
          foes=[dict(s='ELECTRODE', m=['CHARGE', 'THUNDERBOLT', 'TAUNT', 'ELECTRO_BALL'], a='AFTERMATH', lv=-6, p=[1, 2, 3, 4]),
                dict(s='SPIRITOMB', m=['NASTY_PLOT', 'DARK_PULSE', 'SHADOW_SNEAK', 'PAIN_SPLIT_'], a='INFILTRATOR', lv=-8)]),
        E(kind='normal', name='Transient', hint='Shedinja takes no damage from most moves. Find the one that works.',
          foes=[dict(s='SHEDINJA', m=['SHADOW_CLAW', 'X_SCISSOR', 'GRUDGE_', 'SHADOW_SNEAK'], a='WONDER_GUARD', i='ITEM_FOCUS_SASH'),
                dict(s='DUSKNOIR', m=['SHADOW_PUNCH', 'ICE_PUNCH', 'WILL_O_WISP', 'PROTECT'], a='FRISK', lv=-6)]),
        E(kind='normal', name='Nemesis', hint='Gengar hides behind Substitute every other turn.',
          foes=[dict(s='GENGAR', m=['SUBSTITUTE', 'SHADOW_BALL', 'SLUDGE_BOMB', 'HYPNOSIS'], a='CURSED_BODY', lv=-6, p=[1, 2, 1, 3, 4]),
                dict(s='BANETTE', m=['SHADOW_SNEAK', 'TRICK_', 'CURSE', 'GUNK_SHOT'], a='CURSED_BODY', lv=-4)]),
        E(kind='normal', name='Reptomancer', hint='Salazzle\'s daggers poison everything. Steel types are immune.',
          foes=[dict(s='SALAZZLE', m=['TOXIC', 'VENOSHOCK', 'FLAMETHROWER', 'NASTY_PLOT'], a='CORROSION', lv=-4, p=[1, 4, 2, 3]),
                dict(s='SALANDIT', m=['TOXIC', 'EMBER', 'POISON_FANG', 'SWEET_SCENT_'], a='CORROSION')]),
        E(kind='normal', name='Giant Head', hint='Golurk counts down. At zero, it is time.',
          foes=[dict(s='GOLURK', m=['ROCK_POLISH', 'SHADOW_PUNCH', 'HIGH_HORSEPOWER', 'DYNAMIC_PUNCH'], a='NO_GUARD', lv=-4,
                     p=[1, 1, 2, 3, 4]),
                dict(s='GOLETT', m=['DEFENSE_CURL', 'MUD_SLAP', 'SHADOW_PUNCH', 'IRON_DEFENSE'], a='KLUTZ')]),
        E(kind='normal', name='Spire Growth', hint='Tangrowth chokes the floor. Trapped, drained, regrown.',
          field='GRASSY_TERRAIN',
          foes=[dict(s='TANGROWTH', m=['POWER_WHIP', 'GIGA_DRAIN', 'SLEEP_POWDER', 'ANCIENT_POWER'], a='REGENERATOR', lv=-4),
                dict(s='TREVENANT', m=['WOOD_HAMMER', 'PHANTOM_FORCE_', 'WILL_O_WISP', 'HORN_LEECH'], a='NATURAL_CURE', lv=-6)]),
        E(kind='normal', name='The Maw', hint='Swalot swallows everything. Including your boosts.',
          foes=[dict(s='SWALOT', m=['STOCKPILE', 'SWALLOW', 'SPIT_UP', 'SLUDGE_BOMB'], a='GLUTTONY', lv=-4, p=[1, 1, 3, 4]),
                dict(s='GULPIN', m=['YAWN', 'ACID_SPRAY', 'ENCORE', 'GUNK_SHOT'], a='LIQUID_OOZE')]),
        E(kind='normal', name='Nightmare', hint='Hypno puts one of you to sleep and eats the dream. Wake up, or make it miss.',
          foes=[dict(s='HYPNO', m=['HYPNOSIS', 'DREAM_EATER', 'DISABLE', 'PSYCHIC'], a='BAD_DREAMS', p=[1, 2, 3, 4]),
                dict(s='MISMAGIUS', m=['CONFUSE_RAY', 'SHADOW_BALL', 'MYSTICAL_FIRE', 'HEX'], a='LEVITATE')]),
        E(kind='normal', name='The Costume', hint='The first hit always lands on Mimikyu\'s disguise. Spend a weak one on it.',
          foes=[dict(s='MIMIKYU', m=['SWORDS_DANCE', 'SHADOW_CLAW', 'PLAY_ROUGH', 'SHADOW_SNEAK'], a='DISGUISE', p=[1, 2, 3, 2]),
                dict(s='BANETTE', m=['WILL_O_WISP', 'SHADOW_SNEAK', 'KNOCK_OFF_', 'CURSE'], a='CURSED_BODY')]),
        E(kind='elite', name='Time Eater', hint='Celebi-less clockwork: Bronzong reverses time. Slow Pokémon move first.',
          field='TRICK_ROOM',
          foes=[dict(s='BRONZONG', m=['TRICK_ROOM', 'GYRO_BALL', 'EARTHQUAKE', 'IRON_DEFENSE'], a='LEVITATE', hp=2.6, lv=-2,
                     p=[4, 2, 3, 2, 1]),
                dict(s='CONKELDURR', m=['MACH_PUNCH', 'DRAIN_PUNCH', 'ICE_PUNCH', 'BULK_UP'], a='IRON_FIST', lv=-6)]),
        E(kind='elite', name='Awakened One', hint='Honchkrow rises twice as angry when you buff in front of it.',
          foes=[dict(s='HONCHKROW', m=['NASTY_PLOT', 'DARK_PULSE', 'HEAT_WAVE', 'SUCKER_PUNCH'], a='MOXIE', hp=2.4, lv=-2,
                     p=[1, 2, 3, 2]),
                dict(s='MURKROW', m=['TAILWIND', 'FEINT_ATTACK_', 'HAZE', 'PECK_'], a='PRANKSTER')]),
        E(kind='elite', name='Donu and Deca', hint='Solrock buffs, Lunatone shields. They are twins: both must fall.',
          foes=[dict(s='SOLROCK', m=['COSMIC_POWER', 'ROCK_SLIDE', 'ZEN_HEADBUTT', 'WILL_O_WISP'], a='LEVITATE', hp=1.8, p=[1, 2, 3, 4]),
                dict(s='LUNATONE', m=['LIGHT_SCREEN', 'POWER_GEM', 'PSYCHIC', 'HYPNOSIS'], a='LEVITATE', hp=1.8, p=[1, 3, 2, 4])]),
    ],
}

# ---------------------------------------------------------------------------------------------
# Bazen per act (Jordi + Claude). Één baas per act per run (op de seed). Duo's: allebei moeten vallen.

BOSSES = {
    1: [
        E(name='Venusaur & Blastoise', hint='Rain for one, sun for the other. They fight over the weather.',
          foes=[dict(s='BLASTOISE', m=['RAIN_DANCE', 'WATER_PULSE', 'AURA_SPHERE', 'PROTECT'], a='RAIN_DISH', hp=2.4, lv=-6,
                     p=[1, 2, 3, 2, 4]),
                dict(s='VENUSAUR', m=['SUNNY_DAY', 'GIGA_DRAIN', 'SLUDGE_BOMB', 'LEECH_SEED'], a='CHLOROPHYLL', hp=2.4, lv=-6,
                     p=[4, 1, 2, 3, 2])]),
        E(name='Totem Wishiwashi', hint='A school of fish with an aura. Below a quarter HP it falls apart: race it there.',
          foes=[dict(s='WISHIWASHI', m=['SOAK', 'LIQUIDATION', 'AQUA_RING', 'BEAT_UP'], a='SCHOOLING', hp=2.0, b={'atk': 1, 'def': 1},
                     p=[2, 4, 2, 1, 3]),
                dict(s='ARAQUANID', m=['WIDE_GUARD', 'LIQUIDATION', 'LEECH_LIFE', 'MIRROR_COAT'], a='WATER_BUBBLE', lv=-6,
                     p=[1, 2, 3, 4])]),
        E(name='Totem Marowak', hint='A bone club, a flame dance and a lizard that poisons everything it touches.',
          foes=[dict(s='MAROWAK_ALOLA_TOTEM', m=['FLARE_BLITZ', 'SHADOW_BONE', 'BONEMERANG', 'WILL_O_WISP'], 
                     hp=3.2, lv=-4, i='ITEM_THICK_CLUB', b={'def': 1}, p=[4, 2, 1, 3]),
                dict(s='SALAZZLE', m=['TOXIC', 'FLAMETHROWER', 'VENOSHOCK', 'FAKE_TEARS'], a='CORROSION', lv=-8, p=[1, 4, 3, 3])]),
        E(name='Gigantamax Pikachu', hint='Huge, loud and charged. Ground types are a very good idea.',
          foes=[dict(s='PIKACHU_GMAX', m=['CHARGE', 'THUNDERBOLT', 'IRON_TAIL', 'NUZZLE'], a='LIGHTNING_ROD', hp=4.0, lv=2,
                     i='ITEM_LIGHT_BALL', p=[4, 1, 2, 2, 3]),
                dict(s='PLUSLE', m=['HELPING_HAND', 'ENCORE', 'ELECTRO_BALL', 'NASTY_PLOT'], a='PLUS', lv=-8, p=[1, 2, 1, 3])]),
    ],
    2: [
        E(name='Mega Metagross', hint='Bronze Automaton: it charges, it fires, it rests. Strike in the rest.',
          foes=[dict(s='METAGROSS_MEGA', m=['IRON_DEFENSE', 'METEOR_MASH', 'HYPER_BEAM', 'ZEN_HEADBUTT'], a='TOUGH_CLAWS', hp=3.6,
                     lv=-2, p=[1, 2, 4, 3, 2]),
                dict(s='BELDUM', m=['TAKE_DOWN', 'IRON_HEAD', 'ZEN_HEADBUTT', 'IRON_DEFENSE'], a='CLEAR_BODY')]),
        E(name='Darkrai', hint='It puts one of you to sleep and feeds on the nightmare. Wake up.',
          foes=[dict(s='DARKRAI', m=['DARK_VOID', 'DARK_PULSE', 'NASTY_PLOT', 'SLUDGE_BOMB'], a='BAD_DREAMS', hp=4.2, lv=-6,
                     p=[1, 2, 3, 2, 4, 2]),
                dict(s='MISDREAVUS', m=['HEX', 'CONFUSE_RAY', 'SHADOW_BALL', 'PROTECT'], a='LEVITATE', lv=-2, p=[2, 1, 3, 4])]),
        E(name='Mewtwo & Mew', hint='The clone hits, the original copies. Kill order?',
          foes=[dict(s='MEWTWO', m=['PSYSTRIKE', 'AURA_SPHERE', 'CALM_MIND', 'RECOVER'], a='PRESSURE', hp=2.4, lv=-6, p=[3, 1, 2, 1, 4]),
                dict(s='MEW', m=['TRANSFORM', 'HELPING_HAND', 'PSYCHIC', 'METRONOME'], a='SYNCHRONIZE', hp=1.8, lv=-8, p=[2, 3, 4])]),
        E(name='Dialga & Palkia', hint='Time and space. One reverses the turn order, the other warps it.',
          foes=[dict(s='DIALGA', m=['TRICK_ROOM', 'ROAR_OF_TIME', 'FLASH_CANNON', 'DRAGON_PULSE'], a='PRESSURE', hp=2.2, lv=-8,
                     p=[1, 3, 4, 2]),
                dict(s='PALKIA', m=['SPACIAL_REND', 'HYDRO_PUMP', 'AQUA_TAIL', 'DRAGON_CLAW'], a='PRESSURE', hp=2.2, lv=-8)]),
    ],
    3: [
        E(name='Mega Mewtwo Y', hint='Calm Mind, then Psystrike. Every buff is a step on the clock.',
          foes=[dict(s='MEWTWO_MEGA_Y', m=['CALM_MIND', 'PSYSTRIKE', 'FLAMETHROWER', 'RECOVER'], a='INSOMNIA', hp=4.0, lv=-4,
                     p=[1, 2, 3, 2, 4]),
                dict(s='MEW', m=['HELPING_HAND', 'AFTER_YOU', 'PSYCHIC', 'REFLECT'], a='SYNCHRONIZE', lv=-8, p=[4, 1, 2, 1])]),
        E(name='Ultra Necrozma', hint='Blinding light. It ignores your abilities and grows with every hit.',
          foes=[dict(s='NECROZMA_ULTRA', m=['DRAGON_DANCE', 'PHOTON_GEYSER', 'PSYCHO_CUT', 'EARTHQUAKE'], a='NEUROFORCE', hp=4.0,
                     lv=-6, p=[1, 2, 3, 2, 4]),
                dict(s='LUNATONE', m=['LIGHT_SCREEN', 'POWER_GEM', 'PSYCHIC', 'HYPNOSIS'], a='LEVITATE', lv=-4, p=[1, 3, 2, 4])]),
        E(name='Eternamax Eternatus', hint='The heart of the tower. Meteor Beam charges first: that is your window.',
          foes=[dict(s='ETERNATUS_ETERNAMAX', m=['DYNAMAX_CANNON', 'SLUDGE_BOMB', 'FLAMETHROWER', 'METEOR_BEAM'], a='PRESSURE', hp=3.2,
                     b={'spa': 1}, p=[4, 1, 2, 3, 1])]),
        E(name='Mega Rayquaza', hint='Delta Stream: no weather but its own. Dragon Ascent costs it defense.',
          foes=[dict(s='RAYQUAZA_MEGA', m=['DRAGON_DANCE', 'DRAGON_ASCENT', 'EXTREME_SPEED', 'EARTHQUAKE'], a='DELTA_STREAM', hp=4.0,
                     lv=-6, p=[1, 2, 3, 4, 2]),
                dict(s='ALTARIA', m=['TAILWIND', 'COTTON_GUARD', 'DRAGON_PULSE', 'ROOST'], a='CLOUD_NINE', lv=-6)]),
        E(name='Terapagos', hint='Stellar crown: its shell reflects every first hit. Then it opens up.',
          foes=[dict(s='TERAPAGOS_TERASTAL', m=['CALM_MIND', 'TERA_STARSTORM', 'EARTH_POWER', 'RAPID_SPIN'], a='TERA_SHELL', hp=4.2,
                     lv=-6, p=[1, 2, 3, 2, 4]),
                dict(s='CARBINK', m=['REFLECT', 'LIGHT_SCREEN', 'TRICK_ROOM', 'MOONBLAST'], a='STURDY', lv=-4, p=[1, 2, 4])]),
    ],
}

FIELDS = {None: 'STARTING_STATUS_NONE', 'GRASSY_TERRAIN': 'STARTING_STATUS_GRASSY_TERRAIN', 'ELECTRIC_TERRAIN': 'STARTING_STATUS_ELECTRIC_TERRAIN',
          'MISTY_TERRAIN': 'STARTING_STATUS_MISTY_TERRAIN', 'PSYCHIC_TERRAIN': 'STARTING_STATUS_PSYCHIC_TERRAIN',
          'TRICK_ROOM': 'STARTING_STATUS_TRICK_ROOM', 'TAILWIND_OPPONENT': 'STARTING_STATUS_TAILWIND_OPPONENT',
          }
GIMMICKS = {None: 'SPIRE_GIMMICK_NONE', 'SLEEP3': 'SPIRE_GIMMICK_SLEEP', 'HIDDEN': 'SPIRE_GIMMICK_HIDDEN'}
STATS = ['atk', 'def', 'spe', 'spa', 'spd']   # volgorde van de totem-boosts (STAT_ATK ... STAT_SPDEF)


# ---------------------------------------------------------------------------------------------
# Controle

def learnable(species, move):
    if move in UNIVERSAL or species == 'SMEARGLE':          # Smeargle schetst alles
        return True
    if (species, move) in {('ROTOM_WASH', 'HYDRO_PUMP')}:   # vormmove
        return True
    key = species
    while key:
        if key in _ALL and 'MOVE_' + move in _ALL[key]:
            return True
        key = key.rsplit('_', 1)[0] if '_' in key else None
    pre = SPECIES.get(species, {}).get('pre')
    if pre and pre != species and learnable(pre, move):
        return True
    return learnable_src(species, move)


def learnable_src(species, move):
    seen, cur = set(), species
    base = species.split('_')[0]
    cands = {species}
    for name in SPECIES:   # vormen (MAROWAK_ALOLA_TOTEM -> MAROWAK_ALOLA), voorgangers
        if species.startswith(name + '_') or name == base:
            cands.add(name)
    while cur and cur not in seen:
        seen.add(cur)
        cands.add(cur)
        cur = SPECIES.get(cur, {}).get('pre')
    for c in list(cands):
        cur = c
        while cur:
            cands.add(cur)
            cur = SPECIES.get(cur, {}).get('pre')
            if cur in seen:
                break
            if cur:
                seen.add(cur)
    for c in cands:
        s = SPECIES.get(c)
        if not s:
            continue
        if move in {m for _, m in s['levelup']} or move in s['teach'] or move in s['egg']:
            return True
    return False


def check(enc, where, warns):
    for f in enc['foes']:
        s = f['s']
        if s not in SPECIES:
            warns.append('%s: onbekende soort %s' % (where, s))
            continue
        f['m'] = [m for m in f['m'] if not m.endswith('_')]       # '_' achter een move = bewust weggelaten
        for m in f['m']:
            if m not in MOVES:
                warns.append('%s: onbekende move %s' % (where, m))
            elif m in P.BANNED_SET:
                warns.append('%s: verboden move %s (%s)' % (where, m, s))
            elif not learnable(s, m):
                warns.append('%s: %s leert %s niet' % (where, s, m))
        a = f.get('a')
        if a and a not in SPECIES[s]['abilities']:
            warns.append('%s: %s heeft ability %s niet (%s)' % (where, s, a, SPECIES[s]['abilities']))
        i = f.get('i')
        if i and i.endswith('_'):
            f.pop('i')
        elif i and i not in ITEMS:
            warns.append('%s: onbekend item %s' % (where, i))
        for slot in f.get('p', []):
            if not 1 <= slot <= len(f['m']):
                warns.append('%s: patroon %s verwijst naar een lege slot (%s)' % (where, f.get('p'), s))


# ---------------------------------------------------------------------------------------------
# Moeilijkheid (zelfde schadeformule als balance.py; referentieteam = mediaan van de act)

REF_BASE = {1: 62, 2: 82, 3: 92}       # gemiddelde base stat van een spelersvorm per act (mediaan-rating)
REF_POWER = {1: 45, 2: 70, 3: 85}      # STAB-kracht van de speler (startmove -> beloningen)
PLAYER_HP_MULT = 4.0


def stat(base, level, hp=False, iv=20, ev=0):
    x = (2 * base + iv + ev // 4) * level // 100
    return x + level + 10 if hp else x + 5


def dmg(level, power, atk, df, stab=1.5):
    return ((2 * level // 5 + 2) * power * atk // max(df, 1) // 50 + 2) * stab * 0.925


ITEM_MULT = {'ITEM_LIGHT_BALL': 2.0, 'ITEM_LIFE_ORB': 1.3, 'ITEM_CHOICE_BAND': 1.5, 'ITEM_CHOICE_SPECS': 1.5,
             'ITEM_THICK_CLUB': 2.0, 'ITEM_MUSCLE_BAND': 1.1, 'ITEM_WISE_GLASSES': 1.1, 'ITEM_EXPERT_BELT': 1.1}


# moves zonder vaste kracht: gemiddelde verwachte kracht
MODEL_POWER = {'METRONOME': 80, 'PRESENT': 52, 'COUNTER': 55, 'MIRROR_COAT': 55, 'METAL_BURST': 50, 'BIDE': 40,
               'FLAIL': 70, 'ELECTRO_BALL': 80, 'GYRO_BALL': 80, 'SPIT_UP': 100}


def move_power(f, m):
    if m in MODEL_POWER:
        mv = MOVES[m]
        return MODEL_POWER[m] * (1.5 if mv['type'] in SPECIES[f['s']]['types'] else 1)
    mv = MOVES.get(m)
    if not mv or mv['power'] <= 1 or mv['cat'] == 'STATUS':
        return 0
    p = mv['power'] * (1.5 if mv['type'] in SPECIES[f['s']]['types'] else 1) * ((mv['acc'] or 100) / 100)
    p *= mv['strikes'] if mv['effect'] != 'MULTI_HIT' else 3
    if mv['target'] in ('BOTH', 'FOES_AND_ALLY'):
        p *= 0.75 * 2
    return p


def avg_power(f):
    """Gemiddelde kracht per beurt: bij een patroon het gemiddelde over het patroon (statusbeurten = 0),
    anders de beste aanval in 80% van de beurten. Plus items en totem-boosts op Atk/SpA."""
    if f.get('p'):
        p = sum(move_power(f, f['m'][i - 1]) for i in f['p'] if i <= len(f['m'])) / len(f['p'])
    else:
        p = best_power(f) * 0.8
    p *= ITEM_MULT.get(f.get('i'), 1.0)
    b = max(f.get('b', {}).get('atk', 0), f.get('b', {}).get('spa', 0))
    return p * (2 + b) / 2


def best_power(f):
    best = 0
    for m in f['m']:
        mv = MOVES.get(m)
        if not mv or mv['power'] <= 1 or mv['cat'] == 'STATUS':
            continue
        p = mv['power'] * (1.5 if mv['type'] in SPECIES[f['s']]['types'] else 1) * ((mv['acc'] or 100) / 100)
        p *= mv['strikes'] if mv['effect'] != 'MULTI_HIT' else 3
        if mv['target'] in ('BOTH', 'FOES_AND_ALLY'):
            p *= 0.75 * 2
        best = max(best, p)
    return best


# vormwissel bij de start (Schooling): rekenen met de vorm waarin hij vecht
MODEL_AS = {'WISHIWASHI': 'WISHIWASHI_SCHOOL'}

# stat-opbouw per move (stages op de aanvalsstat), voor de beurt-voor-beurt-simulatie
SETUP = {'SWORDS_DANCE': 2, 'NASTY_PLOT': 2, 'TAIL_GLOW': 3, 'SHELL_SMASH': 2, 'BELLY_DRUM': 6, 'CALM_MIND': 1,
         'DRAGON_DANCE': 1, 'QUIVER_DANCE': 1, 'BULK_UP': 1, 'CURSE': 1, 'COIL': 1, 'HONE_CLAWS': 1, 'GROWTH': 1,
         'WORK_UP': 1, 'SHIFT_GEAR': 1, 'HOWL': 1, 'MEDITATE': 1, 'SHARPEN': 1, 'VICTORY_DANCE': 1, 'NO_RETREAT': 1,
         'CLANGOROUS_SOUL': 1, 'TIDY_UP': 1, 'FILLET_AWAY': 2, 'CHARGE': 0, 'STOCKPILE': 0, 'MACHINE_LEARNING': 1,
         'ACUPRESSURE': 1}


def foe_turn_power(f, t, stage):
    """Kracht in beurt t (0-based) en de nieuwe stage. Rage: +1 per beurt (hij wordt geraakt);
    Echoed Voice: verdubbelt per opeenvolgende beurt (max 200)."""
    if f.get('p'):
        slot = f['p'][t % len(f['p'])] - 1
        m = f['m'][slot] if slot < len(f['m']) else None
    else:
        m = max(f['m'], key=lambda x: move_power(f, x))
        if move_power(f, m) == 0 or t % 5 == 4:   # vrije AI: 1 op de 5 beurten iets anders
            m = None
    if m is None:
        return 0, stage
    if m in SETUP:
        return 0, min(6, stage + SETUP[m])
    p = move_power(f, m)
    if m == 'ECHOED_VOICE':
        p = min(p * (2 ** min(t, 4)), 200 * 1.5)
    if m == 'RAGE':
        stage = min(6, stage + 1)
    mult = (2 + stage) / 2 if stage >= 0 else 2 / (2 - stage)
    return p * ITEM_MULT.get(f.get('i'), 1.0) * mult, stage


def difficulty(enc, act, kind, dlv=0, hfac=1.0):
    lv = ACT_LEVEL[act] + dlv
    rb = REF_BASE[act]
    p_hp = stat(rb, 100, True, 31, 84) * PLAYER_HP_MULT
    p_atk = stat(rb, 100, False, 31, 84)
    p_def = stat(rb, 100, False, 31, 84)
    foes = []
    for f in enc['foes']:
        s = SPECIES.get(MODEL_AS.get(f['s'], f['s']))
        if not s:
            continue
        L = lv
        hp = stat(s['hp'], L, True) * f.get('hp', 1.0) * hfac
        off = max(stat(s['atk'], L), stat(s['spa'], L))
        dfn = (stat(s['def'], L) + stat(s['spd'], L)) / 2
        take = dmg(100, REF_POWER[act], p_atk, dfn)
        b = max(f.get('b', {}).get('atk', 0), f.get('b', {}).get('spa', 0))
        if f.get('g') == 'SLEEP3':
            b -= 0   # slaapt 3 beurten: zie hieronder
        foes.append(dict(f=f, hp=hp, off=off, take=take, stage=b, sleep=3 if f.get('g') == 'SLEEP3' else 0))
    # speler: 2 aanvallen per beurt op de gevaarlijkste vijand (hoogste schade per beurt die het kost om hem te doden)
    lost, t = 0.0, 0
    while any(x['hp'] > 0 for x in foes) and t < 40:
        for x in foes:
            if x['hp'] <= 0:
                continue
            if x['sleep'] > 0:
                x['sleep'] -= 1
                continue
            if x['f'].get('a') == 'TRUANT' and t % 2 == 1:
                continue   # Truant: elke andere beurt niets
            pw, x['stage'] = foe_turn_power(x['f'], t, x['stage'])
            if pw:
                lost += dmg(lv, pw, x['off'], p_def, stab=1.0)
        alive = [x for x in foes if x['hp'] > 0]
        target = max(alive, key=lambda x: (x['off'] * (2 + max(x['stage'], 0))) / max(x['hp'] / x['take'], 0.3))
        shots = 2.0
        while shots > 0 and alive:
            need = target['hp'] / target['take']
            use = min(need, shots)
            target['hp'] -= use * target['take']
            shots -= use
            alive = [x for x in foes if x['hp'] > 1e-6]
            if alive:
                target = alive[0]
        t += 1
    # het laatste beurtje telt half (de speler slaat vaak eerst)
    return dict(turns=t - 0.5, lost=100 * lost / (2 * p_hp))


TARGET = {'weak': (3, 12), 'normal': (6, 18), 'elite': (15, 35), 'boss': (40, 75)}
# doel voor de mediaan per groep: (beurten, HP-verlies %) – uit SPIRE_DESIGN.md (normaal ±3 beurten/15%, elite ±4-5/25%,
# baas ±10/60%); zwakke gevechten iets korter en lichter.
TARGET_MID = {'weak': (2.5, 7), 'normal': (3.0, 11), 'elite': (4.5, 24), 'boss': (9.0, 55)}
# v0.8.107 (runsim.py, vergelijking met Slay): elk soort gevecht wordt per act zwaarder, zoals in Slay
# (act-2-gangen doen pijn, act-3-bazen het meest). Kalibratie op HP-verlies (beurten wegen mee). Eerder viel act 2
# goedkoper uit dan act 1 (gewoon 11% / zwak 5%) en waren act-3-elites lichter dan act-1-elites (20% / 21%),
# terwijl de speler per act sterker wordt (relics, upgrades, items). Act-1-elites op het oude doel (24%).
TARGET_ACT = {('weak', 1): (2.5, 8), ('weak', 2): (2.5, 8), ('weak', 3): (2.5, 10),
              ('normal', 1): (3.0, 12), ('normal', 2): (3.5, 14), ('normal', 3): (4.0, 16),
              ('elite', 1): (4.5, 24), ('elite', 2): (5.0, 27), ('elite', 3): (5.5, 30),
              ('boss', 1): (9.0, 55), ('boss', 2): (9.0, 60), ('boss', 3): (9.0, 65)}
CALIB = {}   # (act, kind) -> (levelverschuiving, HP-factor)


def calibrate(groups):
    import statistics as st
    for key, encs in groups.items():
        act, kind = key
        tt, tl = TARGET_ACT.get((kind.split(':')[0], act), TARGET_MID[kind.split(':')[0]])
        best = None
        for dlv in (0,):
            for h10 in range(3, 81):
                h = h10 / 10
                ds = [difficulty(e, act, kind, dlv, h) for e in encs]
                mt = st.median(d['turns'] for d in ds)
                ml = st.median(d['lost'] for d in ds)
                if kind.startswith('boss'):
                    # een baas is uniek: op HP-verlies, maar binnen 7-13 beurten
                    err = math.log(max(ml, 0.1) / tl) ** 2 + 0.3 * math.log(mt / tt) ** 2
                    if not 7 <= mt <= 13:
                        err += 10
                else:
                    # mediaan van de groep op het doel; de verschillen binnen de groep (de puzzel) blijven staan
                    err = math.log(max(ml, 0.1) / tl) ** 2 + 0.3 * math.log(mt / tt) ** 2
                if best is None or err < best[0]:
                    best = (err, dlv, h, mt, ml)
        CALIB[key] = best[1:]


# ---------------------------------------------------------------------------------------------
# Uitvoer

def c_str(s):
    return s.replace('"', '\\"')


def foe_c(f, dlv=0, hfac=1.0):
    moves = (f['m'] + ['NONE'] * 4)[:4]
    boosts = ', '.join(str(f.get('b', {}).get(k, 0)) for k in STATS)
    pat = (f.get('p', []) + [0] * 8)[:8]
    return ('{SPECIES_%s, {%s}, ABILITY_%s, %s, %d, %d, %s, {%s}, {%s}}'
            % (f['s'], ', '.join('MOVE_' + m for m in moves), f.get('a', 'NONE'), f.get('i', 'ITEM_NONE'),
               0, round(f.get('hp', 1.0) * hfac * 10), GIMMICKS[f.get('g')], boosts, ', '.join(map(str, pat))))


def enc_c(e, biome, kind, cal=(0, 1.0)):
    foes = e['foes'] + [dict(s='NONE', m=[])] * (2 - len(e['foes']))
    return ('    {%s, %s, %s, COMPOUND_STRING("%s"), COMPOUND_STRING("%s"),\n     {%s,\n      %s}},'
            % (biome, kind, FIELDS[e.get('field')], c_str(e['name']), c_str(e['hint']),
               foe_c(foes[0], *cal) if foes[0]['s'] != 'NONE' else '{SPECIES_NONE}',
               foe_c(foes[1], *cal) if foes[1]['s'] != 'NONE' else '{SPECIES_NONE}'))


def totem_elites():
    """Elites zijn totems (Jordi: binnen de Pokémon-wereld): de eerste vijand krijgt de totem-aura,
    +1 op zijn hoogste aanvalsstat, tenzij de ontmoeting zelf al boosts heeft."""
    for lst in ENCOUNTERS.values():
        for e in lst:
            if e['kind'] != 'elite':
                continue
            f = e['foes'][0]
            if 'b' not in f and f['s'] in SPECIES:
                s = SPECIES[f['s']]
                f['b'] = {'atk': 1} if s['atk'] >= s['spa'] else {'spa': 1}


def main():
    totem_elites()
    warns = []
    rows = []
    for b in BIOMES:
        for i, e in enumerate(ENCOUNTERS[b['key']]):
            check(e, '%s/%s' % (b['key'], e['name']), warns)
            d = difficulty(e, b['act'], e['kind'])
            rows.append((b, e, d))
    for act, lst in BOSSES.items():
        for e in lst:
            check(e, 'BOSS%d/%s' % (act, e['name']), warns)
            e['kind'] = 'boss'
            rows.append((dict(key='BOSS', act=act, name='Boss'), e, difficulty(e, act, 'boss')))
    for w in warns:
        print('!', w)
    groups = {}
    for b, e, d in rows:
        # bazen elk apart (iedere baas moet zelf op het doel uitkomen), de rest per act en soort
        key = (b['act'], e['kind'] if e['kind'] != 'boss' else 'boss:' + e['name'])
        e['calkey'] = key
        groups.setdefault(key, []).append(e)
    calibrate(groups)
    rows = [(b, e, difficulty(e, b['act'], e['kind'], *CALIB[e['calkey']][:2])) for b, e, _ in rows]
    # C
    L = ['// Gegenereerd door tools/grounded/spire/encounters.py - niet met de hand bewerken.', '']
    L.append('const struct SpireBiome gSpireBiomes[SPIRE_BIOME_COUNT] =')
    L.append('{')
    for b in BIOMES:
        L.append('    [SPIRE_BIOME_%s] = {%d, COMPOUND_STRING("%s"), COMPOUND_STRING("%s")},' % (b['key'], b['act'], b['name'], c_str(b['desc'])))
    L.append('};')
    L.append('')
    L.append('static const struct SpireEncounter sSpireEncounters[] =')
    L.append('{')
    for b in BIOMES:
        for e in ENCOUNTERS[b['key']]:
            L.append(enc_c(e, 'SPIRE_BIOME_' + b['key'], 'SPIRE_ENC_' + e['kind'].upper(), CALIB[e['calkey']][:2]))
    L.append('};')
    L.append('')
    L.append('static const struct SpireEncounter sSpireBosses[] =')
    L.append('{')
    for act, lst in BOSSES.items():
        for e in lst:
            L.append(enc_c(e, str(act), 'SPIRE_ENC_BOSS', CALIB[e['calkey']][:2]))
    L.append('};')
    with open(os.path.join(ROOT, 'src/data/spire_encounters.h'), 'w') as f:
        f.write('\n'.join(L) + '\n')
    # rapport
    R = ['', '## Ontmoetingen (gegenereerd door encounters.py)', '',
         'Geschat HP-verlies van een gemiddeld team in die act (zelfde schadeformule; speler ×4 HP, 2 aanvallen per beurt op de gevaarlijkste vijand eerst; vijanden vallen in 80% van de beurten aan). '
         'Gimmicks (patronen, totem, abilities) zitten er niet in: die maken een gevecht makkelijker als je ze doorziet en zwaarder als je ze negeert. Doel per gevecht: zwak 3–12%, gewoon 6–18%, elite 15–35%, baas 40–75%.', '',
         '**Kalibratie** (automatisch): per act en soort gevecht een levelverschuiving en HP-factor zodat de mediaan precies op het doel valt '
         '(in act 1/2/3: zwak 8/8/10%, gewoon 12/14/16%, elite 24/27/30%, baas 55/60/65% bij ±9 beurten; zoals Slay: gewone gevechten kosten weinig, elites en bazen veel, en elke act doet meer pijn). Level hooguit ±6 (een Grubbin op lv 66 klopt niet). Zo blijft de verhouding tussen de gevechten in een groep (de puzzel) staan, '
         'en ligt het gemiddelde vast.', '',
         '| act | soort | level | HP-factor | mediaan beurten | mediaan HP-verlies |', '|---|---|---|---|---|---|']
    for (act, kind), (dlv, h, mt, ml) in sorted(CALIB.items()):
        R.append('| %d | %s | %+d | ×%.1f | %.1f | %.0f%% |' % (act, kind, dlv, h, mt, ml))
    R += ['', '| act | biome | soort | ontmoeting | beurten | HP-verlies | |', '|---|---|---|---|---|---|---|']
    for b, e, d in rows:
        lo, hi = TARGET[e['kind']]
        flag = '' if lo <= d['lost'] <= hi else ('te makkelijk' if d['lost'] < lo else 'te zwaar')
        R.append('| %d | %s | %s | %s (%s) | %.1f | %.0f%% | %s |' % (b['act'], b['name'], e['kind'], e['name'],
                 ' + '.join(SPECIES[f['s']]['dispname'] if f['s'] in SPECIES else f['s'] for f in e['foes']), d['turns'], d['lost'], flag))
        if flag:
            print('%-6s %-28s %5.1f%% %s' % (e['kind'], e['name'], d['lost'], flag))
    path = os.path.join(ROOT, 'SPIRE_BALANS.md')
    txt = open(path).read()
    keep = ''
    if '\n## Vergelijking met Slay the Spire' in txt:   # sectie van runsim.py laten staan
        keep = '\n## Vergelijking met Slay the Spire' + txt.split('\n## Vergelijking met Slay the Spire', 1)[1]
    txt = txt.split('\n## Ontmoetingen')[0].rstrip('\n') + '\n' + '\n'.join(R) + '\n' + keep
    open(path, 'w').write(txt)
    print('ontmoetingen: %d, bazen: %d, waarschuwingen: %d' % (sum(len(v) for v in ENCOUNTERS.values()),
                                                               sum(len(v) for v in BOSSES.values()), len(warns)))


if __name__ == '__main__':
    main()
