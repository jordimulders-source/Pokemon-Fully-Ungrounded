#!/usr/bin/env python3
"""Battle Stadium (Project Grounded): toernooipool en compagnons. Zie STADIUM_DESIGN.md.

Genereert:
- src/data/stadium_pool.h: de deelnemers (trainer, sterkte) en de compagnons (partner, vrijspelen)
- de PARTNER_STADIUM_*-blokken onderaan src/data/battle_partners.party (tussen de markeringen)
  en hun constanten in include/constants/battle_partner.h: per personage zijn 3 sterkste Pokémon
  (de ace altijd), op level 50.

Sterkte = gemiddelde BST van de 4 sterkste Pokémon (dezelfde keuze als de C-code maakt: de ace
plus de hoogste BST, in de volgorde van het team). De simulatie van NPC-wedstrijden gebruikt die.

Nieuwe personages (CLAUDE.md): voeg ze toe aan POOL (en eventueel aan COMPANIONS) en draai opnieuw;
geef ze ook een omroepzin in tools/grounded/stadium/announcer.py.
Gebruik: python3 tools/grounded/stadium/pool.py
"""
import os, re, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools/grounded/spire'))
from spiredata import load_species

LEVEL = 50
PARTY = os.path.join(ROOT, 'src/data/trainers.party')
PARTNERS = os.path.join(ROOT, 'src/data/battle_partners.party')
PARTNER_H = os.path.join(ROOT, 'include/constants/battle_partner.h')
OUT = os.path.join(ROOT, 'src/data/stadium_pool.h')
BEGIN = '/* --- Battle Stadium (gegenereerd door tools/grounded/stadium/pool.py) --- */'
END = '/* --- einde Battle Stadium --- */'

# Deelnemers: de sterkste versie van elk personage. 'rival' = alleen als de speler het andere geslacht is.
POOL = [
    # Hoenn-gymleiders (laatste rematch)
    'ROXANNE_5', 'BRAWLY_5', 'WATTSON_5', 'FLANNERY_5', 'NORMAN_5', 'WINONA_5', 'TATE_AND_LIZA_5', 'JUAN_5',
    # Elite Four en kampioenen
    'SIDNEY', 'PHOEBE', 'GLACIA', 'DRAKE', 'WALLACE', 'STEVEN',
    # verhaal
    'WALLY_VR_5', 'ARCHIE_SOOTOPOLIS', 'MAXIE_SOOTOPOLIS', 'BIRCH_UNDERWATER', 'KECCLES_3', 'COLRESS_MAGMA',
    'ZINNIA', 'MIMI', 'GABBY_AND_TY_6', 'STADIUM_JOEY', 'STADIUM_WINSTON', 'STADIUM_MUSTARD',
    # Aqua- en Magma-admins (sterkste versie)
    'MATT', 'SHELLY_SEAFLOOR_CAVERN', 'TABITHA_MOSSDEEP',
    # geïmporteerd voor het Stadium (v0.8.108): Kanto (FRLG), Sinnoh (Platinum), Frontier Brains
    'STADIUM_BROCK', 'STADIUM_MISTY', 'STADIUM_LT_SURGE', 'STADIUM_ERIKA', 'STADIUM_KOGA', 'STADIUM_SABRINA',
    'STADIUM_BLAINE', 'STADIUM_GIOVANNI', 'STADIUM_LORELEI', 'STADIUM_BRUNO', 'STADIUM_AGATHA', 'STADIUM_LANCE',
    'STADIUM_BLUE', 'STADIUM_RED', 'STADIUM_OAK',
    'STADIUM_ROARK', 'STADIUM_GARDENIA', 'STADIUM_MAYLENE', 'STADIUM_WAKE', 'STADIUM_FANTINA', 'STADIUM_BYRON',
    'STADIUM_CANDICE', 'STADIUM_VOLKNER', 'STADIUM_AARON', 'STADIUM_BERTHA', 'STADIUM_FLINT', 'STADIUM_LUCIAN',
    'STADIUM_CYNTHIA', 'STADIUM_CYRUS', 'STADIUM_BARRY', 'STADIUM_MARS', 'STADIUM_JUPITER', 'STADIUM_SATURN',
    'STADIUM_PALMER', 'STADIUM_THORTON', 'STADIUM_ARGENTA', 'STADIUM_DAHLIA', 'STADIUM_RILEY',
    'STADIUM_ANABEL', 'STADIUM_TUCKER', 'STADIUM_SPENSER', 'STADIUM_GRETA', 'STADIUM_NOLAND', 'STADIUM_LUCY', 'STADIUM_BRANDON',
    # Jordi en zijn maten (Ace Trainers in Victory Road)
    'ALBERT', 'SAMUEL', 'OWEN',
    # gasten (graphics/grounded/trainers/guests/, tools/grounded/guest_trainer_pics.py)
    'STADIUM_WARIO', 'STADIUM_YOSHI', 'STADIUM_GOLBAT', 'STADIUM_GRIMER', 'STADIUM_BOO', 'STADIUM_MEW',
    'STADIUM_SHY_GUY_RED', 'STADIUM_SHY_GUY_GREEN', 'STADIUM_SHY_GUY_PINK', 'STADIUM_SHY_GUY_BLACK',
    'STADIUM_BURGLAR', 'STADIUM_DITTO',
    # meme-trainers uit de game (Stadium-versie: de grap blijft, level 50)
    'STADIUM_DONALD', 'STADIUM_IVAN', 'STADIUM_JOHNSON', 'STADIUM_LYLE',
    # post-game: de leider van de Victory-gauntlet (alleen V-Pokémon)
    'VICTORY_V',
]
RIVALS = {'BRENDAN_ROUTE_136_TREECKO': 'FEMALE', 'MAY_ROUTE_136_TORCHIC': 'MALE'}   # speler-geslacht waarvoor dit de rivaal is

# Compagnons: (partnernaam, bron-trainer, vrijspelen). Vrijspelen: 'start', ('beat', TRAINER) of ('points', n).
# Iedereen uit de pool wordt compagnon zodra je hem in het Stadium verslaat (Vampire Survivors-stijl).
COMPANIONS = [('BRENDAN', 'BRENDAN_ROUTE_136_TREECKO', 'start'), ('MAY', 'MAY_ROUTE_136_TORCHIC', 'start'),
              ('KECCLES', 'KECCLES_3', 'start'), ('WALLY', 'WALLY_VR_5', 'start')]
def companion_name(t):
    special = {'TATE_AND_LIZA_5': 'TATE_AND_LIZA', 'GABBY_AND_TY_6': 'GABBY_AND_TY', 'LT_SURGE': 'LT_SURGE',
               'SHY_GUY_RED': 'SHY_GUY_RED', 'SHY_GUY_GREEN': 'SHY_GUY_GREEN', 'SHY_GUY_PINK': 'SHY_GUY_PINK',
               'SHY_GUY_BLACK': 'SHY_GUY_BLACK'}
    t2 = t[len('STADIUM_'):] if t.startswith('STADIUM_') else t
    return special.get(t, special.get(t2, t2.split('_')[0]))


COMPANIONS += [(companion_name(t), t, ('beat', t)) for t in POOL if t not in ('KECCLES_3', 'WALLY_VR_5')]

# Collecties zonder trainer (Vampire Survivors-stijl): drie Pokémon die samen met je vechten, vrijgespeeld met
# Stadium-punten (+1 per gewonnen gevecht, +5 per titel; een gewonnen toernooi = 10). Van zwak naar sterk.
# Elk: (partnernaam, naam in de game (max 10), trainerfoto (voorplaatje van de eerste), punten, team).
# Het team: per Pokémon 'Soort @ Item / Ability / Nature / EV's / moves' (level 50, IV's 31).
TRIOS = [
    ('MASCOTS', 'MASCOTS', 'Trio Mascots', 1, [
        ('Pikachu @ Light Ball', 'Static', 'Timid', '4 HP / 252 SpA / 252 Spe', ['Thunderbolt', 'Volt Switch', 'Grass Knot', 'Fake Out']),
        ('Eevee @ Eviolite', 'Adaptability', 'Jolly', '252 HP / 252 Atk / 4 Def', ['Double-Edge', 'Quick Attack', 'Bite', 'Protect']),
        ('Psyduck @ Eviolite', 'Cloud Nine', 'Modest', '252 HP / 252 SpA / 4 SpD', ['Surf', 'Psychic', 'Ice Beam', 'Calm Mind'])]),
    ('STARTERS', 'STARTERS', 'Trio Starters', 3, [
        ('Charizard @ Life Orb', 'Blaze', 'Timid', '4 HP / 252 SpA / 252 Spe', ['Flamethrower', 'Air Slash', 'Dragon Pulse', 'Focus Blast']),
        ('Venusaur @ Black Sludge', 'Chlorophyll', 'Calm', '252 HP / 4 Def / 252 SpD', ['Giga Drain', 'Sludge Bomb', 'Sleep Powder', 'Leech Seed']),
        ('Blastoise @ White Herb', 'Torrent', 'Modest', '4 HP / 252 SpA / 252 Spe', ['Shell Smash', 'Hydro Pump', 'Flash Cannon', 'Ice Beam'])]),
    ('FOSSILS', 'FOSSILS', 'Trio Fossils', 6, [
        ('Aerodactyl @ Focus Sash', 'Unnerve', 'Jolly', '4 HP / 252 Atk / 252 Spe', ['Rock Slide', 'Dual Wingbeat', 'Tailwind', 'Taunt']),
        ('Armaldo @ Leftovers', 'Battle Armor', 'Adamant', '252 HP / 252 Atk / 4 SpD', ['Stone Edge', 'X-Scissor', 'Knock Off', 'Rapid Spin']),
        ('Cradily @ Leftovers', 'Storm Drain', 'Calm', '252 HP / 4 Def / 252 SpD', ['Giga Drain', 'Rock Slide', 'Recover', 'Stealth Rock'])]),
    ('EEVEES', 'EEVEES', 'Trio Eevees', 10, [
        ('Jolteon @ Life Orb', 'Volt Absorb', 'Timid', '4 HP / 252 SpA / 252 Spe', ['Thunderbolt', 'Shadow Ball', 'Volt Switch', 'Hyper Voice']),
        ('Vaporeon @ Leftovers', 'Water Absorb', 'Bold', '252 HP / 252 Def / 4 SpD', ['Scald', 'Wish', 'Protect', 'Ice Beam']),
        ('Flareon @ Flame Orb', 'Guts', 'Adamant', '252 HP / 252 Atk / 4 SpD', ['Flare Blitz', 'Facade', 'Superpower', 'Quick Attack'])]),
    ('LAKE', 'LAKE TRIO', 'Trio Lake', 15, [
        ('Mesprit @ Leftovers', 'Levitate', 'Calm', '252 HP / 4 Def / 252 SpD', ['Psychic', 'Ice Beam', 'Calm Mind', 'Stealth Rock']),
        ('Uxie @ Light Clay', 'Levitate', 'Bold', '252 HP / 252 Def / 4 SpD', ['Reflect', 'Light Screen', 'Psychic', 'U-turn']),
        ('Azelf @ Life Orb', 'Levitate', 'Naive', '4 Atk / 252 SpA / 252 Spe', ['Psychic', 'Fire Blast', 'Nasty Plot', 'Explosion'])]),
    ('REGIS', 'REGIS', 'Trio Regis', 20, [
        ('Regirock @ Leftovers', 'Sturdy', 'Careful', '252 HP / 4 Atk / 252 SpD', ['Stone Edge', 'Body Press', 'Curse', 'Stealth Rock']),
        ('Regice @ Leftovers', 'Ice Body', 'Modest', '252 HP / 252 SpA / 4 SpD', ['Ice Beam', 'Thunderbolt', 'Focus Blast', 'Rest']),
        ('Registeel @ Leftovers', 'Clear Body', 'Impish', '252 HP / 252 Def / 4 SpD', ['Iron Head', 'Body Press', 'Iron Defense', 'Toxic'])]),
    ('BIRDS', 'BIRDS', 'Trio Birds', 25, [
        ('Zapdos @ Heavy-Duty Boots', 'Static', 'Timid', '4 HP / 252 SpA / 252 Spe', ['Thunderbolt', 'Hurricane', 'Heat Wave', 'Roost']),
        ('Articuno @ Leftovers', 'Pressure', 'Calm', '252 HP / 4 Def / 252 SpD', ['Freeze-Dry', 'Hurricane', 'Roost', 'Haze']),
        ('Moltres @ Heavy-Duty Boots', 'Flame Body', 'Modest', '4 HP / 252 SpA / 252 Spe', ['Flamethrower', 'Hurricane', 'Roost', 'Will-O-Wisp'])]),
    ('BEASTS', 'BEASTS', 'Trio Beasts', 30, [
        ('Suicune @ Leftovers', 'Inner Focus', 'Bold', '252 HP / 252 Def / 4 SpD', ['Scald', 'Ice Beam', 'Calm Mind', 'Rest']),
        ('Raikou @ Life Orb', 'Inner Focus', 'Timid', '4 HP / 252 SpA / 252 Spe', ['Thunderbolt', 'Shadow Ball', 'Extrasensory', 'Volt Switch']),
        ('Entei @ Choice Band', 'Inner Focus', 'Adamant', '4 HP / 252 Atk / 252 Spe', ['Sacred Fire', 'Extreme Speed', 'Stone Edge', 'Stomping Tantrum'])]),
    ('PSEUDOS', 'PSEUDOS', 'Trio Pseudos', 35, [
        ('Dragonite @ Heavy-Duty Boots', 'Multiscale', 'Adamant', '4 HP / 252 Atk / 252 Spe', ['Dragon Dance', 'Extreme Speed', 'Earthquake', 'Fire Punch']),
        ('Tyranitar @ Smooth Rock', 'Sand Stream', 'Adamant', '252 HP / 252 Atk / 4 SpD', ['Rock Slide', 'Crunch', 'Earthquake', 'Stealth Rock']),
        ('Salamence @ Life Orb', 'Intimidate', 'Naive', '4 Atk / 252 SpA / 252 Spe', ['Draco Meteor', 'Fire Blast', 'Earthquake', 'Roost'])]),
    ('SWORDS', 'SWORDS', 'Trio Swords', 40, [
        ('Cobalion @ Leftovers', 'Justified', 'Jolly', '4 HP / 252 Atk / 252 Spe', ['Iron Head', 'Close Combat', 'Swords Dance', 'Stealth Rock']),
        ('Terrakion @ Choice Scarf', 'Justified', 'Jolly', '4 HP / 252 Atk / 252 Spe', ['Stone Edge', 'Close Combat', 'Earthquake', 'Quick Attack']),
        ('Virizion @ Life Orb', 'Justified', 'Jolly', '4 HP / 252 Atk / 252 Spe', ['Leaf Blade', 'Close Combat', 'Swords Dance', 'Stone Edge'])]),
    ('LOYAL', 'LOYAL 3', 'Trio Loyal', 45, [
        ('Okidogi @ Leftovers', 'Toxic Chain', 'Adamant', '252 HP / 252 Atk / 4 SpD', ['Drain Punch', 'Gunk Shot', 'Knock Off', 'Bulk Up']),
        ('Munkidori @ Life Orb', 'Toxic Chain', 'Timid', '4 HP / 252 SpA / 252 Spe', ['Sludge Bomb', 'Psychic', 'Focus Blast', 'Fake Out']),
        ('Fezandipiti @ Heavy-Duty Boots', 'Toxic Chain', 'Jolly', '4 HP / 252 Atk / 252 Spe', ['Gunk Shot', 'Play Rough', 'Roost', 'U-turn'])]),
    ('TAPUS', 'TAPUS', 'Trio Tapus', 50, [
        ('Tapu_Koko @ Life Orb', 'Electric Surge', 'Timid', '4 HP / 252 SpA / 252 Spe', ['Thunderbolt', 'Dazzling Gleam', 'U-turn', 'Roost']),
        ('Tapu_Lele @ Choice Specs', 'Psychic Surge', 'Modest', '4 HP / 252 SpA / 252 Spe', ['Psychic', 'Moonblast', 'Focus Blast', 'Psyshock']),
        ('Tapu_Fini @ Leftovers', 'Misty Surge', 'Calm', '252 HP / 4 Def / 252 SpD', ['Moonblast', 'Surf', 'Calm Mind', 'Taunt'])]),
    ('GENIES', 'GENIES', 'Trio Genies', 55, [
        ('Landorus @ Life Orb', 'Sheer Force', 'Modest', '4 HP / 252 SpA / 252 Spe', ['Earth Power', 'Sludge Wave', 'Rock Slide', 'Stealth Rock']),
        ('Thundurus @ Life Orb', 'Prankster', 'Timid', '4 HP / 252 SpA / 252 Spe', ['Thunderbolt', 'Thunder Wave', 'Taunt', 'Nasty Plot']),
        ('Tornadus @ Leftovers', 'Prankster', 'Timid', '4 HP / 252 SpA / 252 Spe', ['Tailwind', 'Bleakwind Storm', 'Taunt', 'Heat Wave'])]),
    ('ULTRAS', 'ULTRAS', 'Trio Ultras', 60, [
        ('Nihilego @ Focus Sash', 'Beast Boost', 'Timid', '4 HP / 252 SpA / 252 Spe', ['Power Gem', 'Sludge Wave', 'Stealth Rock', 'Toxic Spikes']),
        ('Buzzwole @ Leftovers', 'Beast Boost', 'Impish', '252 HP / 4 Atk / 252 Def', ['Drain Punch', 'Leech Life', 'Ice Punch', 'Bulk Up']),
        ('Pheromosa @ Life Orb', 'Beast Boost', 'Naive', '4 Atk / 252 SpA / 252 Spe', ['Close Combat', 'U-turn', 'Ice Beam', 'Poison Jab'])]),
    ('RUIN', 'TREASURES', 'Trio Ruin', 70, [
        ('Chien_Pao @ Focus Sash', 'Sword of Ruin', 'Jolly', '4 HP / 252 Atk / 252 Spe', ['Icicle Crash', 'Sucker Punch', 'Sacred Sword', 'Ice Shard']),
        ('Ting_Lu @ Leftovers', 'Vessel of Ruin', 'Careful', '252 HP / 4 Atk / 252 SpD', ['Earthquake', 'Ruination', 'Stealth Rock', 'Whirlwind']),
        ('Chi_Yu @ Choice Specs', 'Beads of Ruin', 'Timid', '4 HP / 252 SpA / 252 Spe', ['Fire Blast', 'Dark Pulse', 'Psychic', 'Flamethrower'])]),
    ('WEATHER', 'WEATHER', 'Trio Weather', 85, [
        ('Rayquaza @ Life Orb', 'Air Lock', 'Adamant', '4 HP / 252 Atk / 252 Spe', ['Dragon Ascent', 'Extreme Speed', 'Earthquake', 'Dragon Dance']),
        ('Kyogre @ Choice Specs', 'Drizzle', 'Modest', '4 HP / 252 SpA / 252 Spe', ['Water Spout', 'Origin Pulse', 'Thunder', 'Ice Beam']),
        ('Groudon @ Leftovers', 'Drought', 'Adamant', '252 HP / 252 Atk / 4 SpD', ['Precipice Blades', 'Heat Crash', 'Stone Edge', 'Swords Dance'])]),
    ('CREATORS', 'CREATORS', 'Trio Creators', 100, [
        ('Giratina @ Leftovers', 'Pressure', 'Bold', '252 HP / 252 Def / 4 SpD', ['Shadow Ball', 'Draco Meteor', 'Will-O-Wisp', 'Defog']),
        ('Dialga @ Life Orb', 'Pressure', 'Modest', '4 HP / 252 SpA / 252 Spe', ['Draco Meteor', 'Flash Cannon', 'Fire Blast', 'Thunderbolt']),
        ('Palkia @ Choice Specs', 'Pressure', 'Timid', '4 HP / 252 SpA / 252 Spe', ['Spacial Rend', 'Hydro Pump', 'Fire Blast', 'Thunder'])]),
]
TRIO_HEADER = 'Class: Collection\nGender: Male\nMusic: Male\nAI: Check Bad Move / Try To Faint / Check Viability / Smart Switching / Smart Mon Choices'


def trio_mons(team):
    out = []
    for head, ab, nat, evs, moves in team:
        out.append('\n'.join([head, f'Level: {LEVEL}', f'Ability: {ab}', 'IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                              f'EVs: {evs}', f'Nature: {nat}'] + [f'- {mv}' for mv in moves]))
    return out


for pname, name, pic, pts, team in TRIOS:
    COMPANIONS.append((pname, None, ('points', pts)))

# Rugplaatjes die bestaan; de rest staat met zijn voorplaatje naast je (zoals de Frontier-tag battles)
BACK_PICS = {'Brendan': 'Brendan', 'May': 'May', 'Red': 'Red', 'Leaf': 'Leaf', 'Steven': 'Steven', 'Wally': 'Wally', 'Kecleon': 'Kecleon'}

# Overworld-sprite in de arena: eigen sprite waar die bestaat, anders een Pokémon of een passende generieke
GFX = {
    'ROXANNE': 'ROXANNE', 'BRAWLY': 'BRAWLY', 'WATTSON': 'WATTSON', 'FLANNERY': 'FLANNERY', 'NORMAN': 'NORMAN',
    'WINONA': 'WINONA', 'TATE_AND_LIZA': 'TATE', 'JUAN': 'JUAN', 'SIDNEY': 'SIDNEY', 'PHOEBE': 'PHOEBE',
    'GLACIA': 'GLACIA', 'DRAKE': 'DRAKE', 'WALLACE': 'WALLACE', 'STEVEN': 'STEVEN', 'WALLY': 'WALLY',
    'ARCHIE': 'ARCHIE', 'MAXIE': 'MAXIE', 'BIRCH': 'PROF_BIRCH', 'KECCLES': 'KECLEON', 'COLRESS': 'COLRESS',
    'ZINNIA': 'ZINNIA', 'MIMI': 'SPECIES(MIMIKYU)', 'BROCK': 'BROCK', 'OAK': 'PROF_OAK', 'RED': 'RED',
    'LEAF': 'LEAF', 'JOEY': 'YOUNGSTER', 'BRENDAN': 'RIVAL_BRENDAN_NORMAL', 'MAY': 'RIVAL_MAY_NORMAL',
    'GABBY': 'REPORTER_F', 'MATT': 'AQUA_MEMBER_M', 'SHELLY': 'AQUA_MEMBER_F', 'TABITHA': 'MAGMA_MEMBER_M',
    'ANABEL': 'ANABEL', 'TUCKER': 'TUCKER', 'SPENSER': 'SPENSER', 'GRETA': 'GRETA', 'NOLAND': 'NOLAND',
    'LUCY': 'LUCY', 'BRANDON': 'BRANDON', 'BRUNO': 'BRUNO', 'MAYLENE': 'BLACK_BELT', 'MISTY': 'MISTY',
    'LT_SURGE': 'LT_SURGE', 'WAKE': 'SAILOR', 'KOGA': 'KOGA', 'SABRINA': 'SABRINA', 'BLAINE': 'BLAINE',
    'GIOVANNI': 'GIOVANNI', 'CYRUS': 'GENTLEMAN', 'AGATHA': 'AGATHA', 'BERTHA': 'OLD_WOMAN',
    'LORELEI': 'LORELEI', 'LANCE': 'LANCE', 'BLUE': 'BLUE', 'BARRY': 'BOY_3', 'ROARK': 'HIKER', 'BYRON': 'HIKER',
    'GARDENIA': 'PICNICKER', 'ERIKA': 'ERIKA', 'FANTINA': 'BEAUTY', 'CANDICE': 'GIRL_3', 'VOLKNER': 'MAN_5',
    'AARON': 'BUG_CATCHER', 'FLINT': 'MAN_5', 'LUCIAN': 'PSYCHIC_M', 'CYNTHIA': 'WOMAN_5', 'MARS': 'WOMAN_2',
    'JUPITER': 'WOMAN_2', 'SATURN': 'MAN_2', 'PALMER': 'MAN_4', 'THORTON': 'SCIENTIST_2', 'ARGENTA': 'WOMAN_3',
    'DAHLIA': 'WOMAN_4', 'RILEY': 'MAN_3', 'ALBERT': 'MAN_3', 'SAMUEL': 'MAN_3', 'OWEN': 'MAN_3', 'WINSTON': 'RICH_BOY',
    # gasten en meme-trainers
    'WARIO': 'FAT_MAN', 'YOSHI': 'SPECIES(TREECKO)', 'GOLBAT': 'SPECIES(GOLBAT)', 'GRIMER': 'SPECIES(GRIMER)',
    'BOO': 'SPECIES(SHUPPET)', 'MEW': 'MEW', 'SHY_GUY': 'NINJA_BOY', 'BURGLAR': 'BURGLAR', 'DITTO': 'SPECIES(DITTO)',
    'MUSTARD': 'MUSTARD',
    'DONALD': 'BUG_CATCHER', 'IVAN': 'FISHERMAN', 'JOHNSON': 'YOUNGSTER', 'LYLE': 'BUG_CATCHER',
    'VICTORY_V': 'EXPERT_M',
}


def gfx_for(t, header):
    t2 = t[len('STADIUM_'):] if t.startswith('STADIUM_') else t
    for key, g in GFX.items():
        if t2 == key or t2.startswith(key + '_'):
            return 'OBJ_EVENT_GFX_' + g
    female = (header_field(header, 'Gender') or '').lower() == 'female'
    return 'OBJ_EVENT_GFX_' + ('WOMAN_5' if female else 'MAN_3')


species = load_species()
# Ogerpon staat via een macro in species_info en mist in load_species: met de hand (80/120/84/60/96/110)
for _form, _type in (('TEAL', 'GRASS'), ('WELLSPRING', 'WATER'), ('HEARTHFLAME', 'FIRE'), ('CORNERSTONE', 'ROCK')):
    species.setdefault('OGERPON_' + _form, {'dispname': 'Ogerpon', 'hp': 80, 'atk': 120, 'def': 84, 'spa': 60, 'spd': 96,
                                            'spe': 110, 'types': sorted({'GRASS', _type}), 'abilities': []})
species.setdefault('OGERPON', species['OGERPON_TEAL'])
by_disp = {}
for key, d in species.items():
    by_disp.setdefault(d['dispname'].upper(), key)


def species_key(line):
    s = line.split(' @ ')[0].strip()
    m = re.search(r'\(([^()]+)\)\s*(\((?:M|F)\))?\s*$', s)
    if m and m.group(1) not in ('M', 'F'):
        s = m.group(1)
    s = re.sub(r'\s*\((?:M|F)\)\s*$', '', s).strip()
    k = s.upper().replace(' ', '_').replace('-', '_').replace('.', '').replace("'", '').replace('é', 'E')
    for cand in (k, k + '_STANDARD', k + '_NORMAL', k.replace('_HOENN', '')):
        if cand in species:
            return cand
    return by_disp.get(s.upper())


def bst(key):
    d = species.get(key)
    return sum(d[s] for s in ('hp', 'atk', 'def', 'spa', 'spd', 'spe')) if d else 400


def parse_trainers():
    txt = open(PARTY, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'^=== TRAINER_(\w+) ===\n(.*?)(?=^=== |\Z)', txt, re.S | re.M):
        name, body = m.group(1), m.group(2)
        parts = re.split(r'\n\s*\n', body.strip('\n'))
        header = parts[0]
        mons = [p for p in parts[1:] if p.strip() and not p.lstrip().startswith('/*')]
        out[name] = dict(header=header, mons=mons)
    return out


# --- synergie (Jordi: "een trainer die met een rain team speelt moet altijd een drizzle mon hebben") ---
# per archetype: zetters (abilities/moves) en wie ervan profiteert (abilities/moves/types)
ARCHETYPES = {
    'regen': dict(set_ab={'DRIZZLE', 'PRIMORDIAL_SEA'}, set_mv={'RAIN_DANCE'},
                  use_ab={'SWIFT_SWIM', 'RAIN_DISH', 'HYDRATION', 'DRY_SKIN'}, use_mv={'THUNDER', 'HURRICANE', 'ELECTRO_SHOT', 'WEATHER_BALL'}, use_type={'WATER'}),
    'zon': dict(set_ab={'DROUGHT', 'DESOLATE_LAND', 'ORICHALCUM_PULSE'}, set_mv={'SUNNY_DAY'},
                use_ab={'CHLOROPHYLL', 'SOLAR_POWER', 'FLOWER_GIFT', 'LEAF_GUARD', 'PROTOSYNTHESIS', 'HARVEST'},
                use_mv={'SOLAR_BEAM', 'SOLAR_BLADE', 'WEATHER_BALL', 'GROWTH'}, use_type={'FIRE'}),
    'zand': dict(set_ab={'SAND_STREAM', 'SAND_SPIT'}, set_mv={'SANDSTORM'},
                 use_ab={'SAND_RUSH', 'SAND_FORCE', 'SAND_VEIL'}, use_mv={'SHORE_UP', 'WEATHER_BALL'}, use_type={'ROCK'}),
    'sneeuw': dict(set_ab={'SNOW_WARNING'}, set_mv={'HAIL', 'SNOWSCAPE', 'CHILLY_RECEPTION'},
                   use_ab={'SLUSH_RUSH', 'ICE_BODY', 'SNOW_CLOAK'}, use_mv={'BLIZZARD', 'AURORA_VEIL', 'WEATHER_BALL'}, use_type={'ICE'}),
    'zure regen': dict(set_ab={'AIR_POLLUTION'}, set_mv={'ACID_RAIN'}, use_ab=set(), use_mv=set(), use_type={'POISON'}),
    'stuifmeel': dict(set_ab={'POLLEN_SEASON'}, set_mv={'POLLEN_HAZE'}, use_ab=set(), use_mv=set(), use_type={'BUG', 'GRASS'}),
    'elektrisch terrein': dict(set_ab={'ELECTRIC_SURGE', 'HADRON_ENGINE'}, set_mv={'ELECTRIC_TERRAIN'},
                               use_ab={'SURGE_SURFER', 'QUARK_DRIVE'}, use_mv={'RISING_VOLTAGE'}, use_type=set()),
    'psychisch terrein': dict(set_ab={'PSYCHIC_SURGE'}, set_mv={'PSYCHIC_TERRAIN'}, use_ab=set(), use_mv={'EXPANDING_FORCE'}, use_type=set()),
    'gras-terrein': dict(set_ab={'GRASSY_SURGE', 'SEED_SOWER'}, set_mv={'GRASSY_TERRAIN'}, use_ab={'GRASS_PELT'}, use_mv={'GRASSY_GLIDE'}, use_type=set()),
    'mist-terrein': dict(set_ab={'MISTY_SURGE'}, set_mv={'MISTY_TERRAIN'}, use_ab=set(), use_mv={'MISTY_EXPLOSION'}, use_type=set()),
}


def mon_info(block):
    first = block.split('\n')[0]
    key = species_key(first)
    d = species.get(key, {})
    ab = re.search(r'^Ability:\s*(.+)$', block, re.M)
    ability = ab.group(1).strip().upper().replace(' ', '_').replace('-', '_') if ab else (d.get('abilities') or ['NONE'])[0]
    moves = {m.strip().upper().replace(' ', '_').replace('-', '_') for m in re.findall(r'^- (.+)$', block, re.M)}
    return dict(key=key, bst=bst(key), ability=ability, moves=moves, types=set(d.get('types', [])), spe=d.get('spe', 80))


def score(sub, infos, notes=None):
    sc = sum(infos[i]['bst'] for i in sub)
    sc += 15 * len(set().union(*(infos[i]['types'] for i in sub)))
    for name, a in ARCHETYPES.items():
        setter = any(infos[i]['ability'] in a['set_ab'] or infos[i]['moves'] & a['set_mv'] for i in sub)
        hard = sum(1 for i in sub if infos[i]['ability'] in a['use_ab'] or infos[i]['moves'] & a['use_mv'])
        soft = sum(1 for i in sub if infos[i]['types'] & a['use_type'])
        if setter and (hard or soft):
            sc += 40 + 60 * hard + 15 * soft
            if notes is not None:
                notes.add(name)
        elif hard and not setter:
            sc -= 60 * hard
    tr = [i for i in sub if 'TRICK_ROOM' in infos[i]['moves']]
    if tr:
        slow = sum(1 for i in sub if infos[i]['spe'] <= 50 and i not in tr)
        if slow:
            sc += 40 * slow
            if notes is not None:
                notes.add('Trick Room')
    return sc


# Pokémon die altijd meedoen, ook als ze zwak zijn: de grap of het thema van de trainer (teamplek, 0 = eerste)
KEEP = {
    'STADIUM_DITTO': [4],     # PEAKYCHU
    'STADIUM_IVAN': [0],      # Magikarp met Hydro Pump
    'STADIUM_LYLE': [0, 1],   # Scizor en Yanmega: de lv 6-grap uit Petalburg Woods, nu getraind
    'STADIUM_MEW': [0],       # PIKABLU
    'STADIUM_JOEY': [1, 2, 0],  # Mightyena en Obstagoon (Jordi), Rattata (top percentage)
    'STADIUM_GOLBAT': [0],    # Zubat: de grot in Red/Blue
}
# Sterkte met de hand: zes keer Ditto met Imposter is zo sterk als de tegenstander (gemiddelde van de pool)
RATING = {'STADIUM_DONALD': 520, 'STADIUM_JOEY': 480}  # Joey: Poochyena is top percentage


def pick(mons, n, notes=None, keep=()):
    """Beste n Pokémon met synergie (de ace = laatste en KEEP altijd mee), in teamvolgorde. De C-code neemt deze keuze over."""
    from itertools import combinations
    infos = [mon_info(m) for m in mons]
    keys = [x['key'] for x in infos]
    if len(mons) <= n:
        if notes is not None:
            score(list(range(len(mons))), infos, notes)
        return list(range(len(mons))), keys
    ace = len(mons) - 1
    fixed = [ace] + [k for k in keep if k != ace][:n - 1]
    rest = [i for i in range(ace) if i not in fixed]
    best = max((list(c) + fixed for c in combinations(rest, n - len(fixed))), key=lambda sub: score(sub, infos))
    if notes is not None:
        score(best, infos, notes)
    return sorted(best), keys


def header_field(header, field):
    m = re.search(r'^%s:\s*(.*)$' % field, header, re.M)
    return m.group(1).strip() if m else None


trainers = parse_trainers()
errors = []
for t in POOL + list(RIVALS) + [c[1] for c in COMPANIONS if c[1]]:
    if t not in trainers:
        errors.append(f'onbekende trainer TRAINER_{t}')
if errors:
    print('\n'.join(errors)); sys.exit(1)

rows = []
report = ['# Battle Stadium: teams (gegenereerd door tools/grounded/stadium/pool.py)', '',
          'Per trainer de keuze voor singles (4) en doubles/compagnon (3): de ace (laatste) altijd, verder sterkte +',
          'synergie (weer/terrein met zijn zetter, Trick Room met trage Pokémon, typedekking). Level 50.', '',
          '| Trainer | Sterkte | Singles (4) | Doubles (3) | Synergie |', '|---|---|---|---|---|']
masks = {}
for t in POOL + list(RIVALS):
    notes = set()
    idx, keys = pick(trainers[t]['mons'], 4, notes, KEEP.get(t, ()))
    # doubles: dezelfde groep min één (Jordi): de 3 komen uit de 4 van singles
    sub = [trainers[t]['mons'][i] for i in idx]
    j, _ = pick(sub, 3, notes, [idx.index(k) for k in KEEP.get(t, ()) if k in idx])
    idx3 = [idx[x] for x in j]
    masks[t] = (sum(1 << i for i in idx), sum(1 << i for i in idx3))
    nm = lambda i: species[keys[i]]['dispname'] if keys[i] in species else '?'
    report.append(f'| {t} | {{r}} | {", ".join(nm(i) for i in idx)} | {", ".join(nm(i) for i in idx3)} | {", ".join(sorted(notes)) or "-"} |')
    unknown = [trainers[t]['mons'][i].split('\n')[0] for i in idx if keys[i] is None]
    if unknown:
        print(f'let op: {t}: soort niet herkend: {unknown}')
    rating = RATING.get(t) or round(sum(bst(keys[i]) for i in idx) / len(idx))
    report[-1] = report[-1].replace('{r}', str(rating))
    gender = RIVALS.get(t)
    rows.append((t, rating, {'MALE': 1, 'FEMALE': 2}.get(gender, 0), gfx_for(t, trainers[t]['header'])))

# partners
blocks, consts = [], []
scores = {}     # pname -> 'episch-heid' (volgorde van vrijspelen: van gewoon naar episch)
CLASS_BONUS = {'Champion': 80, 'Elite Four': 50, 'Boss': 60, 'Leader': 30, 'Salon Maiden': 60, 'Dome Ace': 60,
               'Palace Maven': 60, 'Arena Tycoon': 60, 'Factory Head': 60, 'Pike Queen': 60, 'Pyramid King': 60,
               'Tower Tycoon': 60, 'Hall Matron': 60, 'Arcade Star': 60, 'Commander': 20, 'Rival': 20}
NAME_BONUS = {'RED': 120, 'BLUE': 40, 'CYNTHIA': 40, 'STEVEN': 40, 'WALLACE': 30, 'OAK': 30, 'GIOVANNI': 30,
              'LANCE': 30, 'ZINNIA': 20}
trio_by_name = {t[0]: t for t in TRIOS}
for i, (pname, src, unlock) in enumerate(COMPANIONS):
    if src is None:   # collectie zonder trainer: voorplaatje van de eerste Pokémon
        _, name, pic, _, team = trio_by_name[pname]
        lines = [f'=== PARTNER_STADIUM_{pname} ===', f'Name: {name}', f'Pic: {pic}', TRIO_HEADER, 'Back Pic: Brendan', '']
        for mon in trio_mons(team):
            lines += [mon, '']
        blocks.append('\n'.join(lines))
        consts.append((f'PARTNER_STADIUM_{pname}', True))
        tkeys = [species_key(m[0].split(' @ ')[0]) for m in team]
        scores[pname] = sum(bst(k) for k in tkeys) / len(tkeys) + unlock[1]   # legendarische sets later
        continue
    tr = trainers[src]
    idx4, keys = pick(tr['mons'], 4, keep=KEEP.get(src, ()))   # compagnon = zijn doubles-drie (uit zijn singles-vier)
    j, _ = pick([tr['mons'][i] for i in idx4], 3, keep=[idx4.index(k) for k in KEEP.get(src, ()) if k in idx4])
    idx = [idx4[x] for x in j]
    pic = header_field(tr['header'], 'Pic')
    back = BACK_PICS.get(pic)
    lines = [f'=== PARTNER_STADIUM_{pname} ===']
    for f in ('Name', 'Class'):
        lines.append(f'{f}: {header_field(tr["header"], f)}')
    lines.append(f'Pic: {pic}')
    g = header_field(tr['header'], 'Gender') or 'Male'
    lines += [f'Gender: {g}', f'Music: {header_field(tr["header"], "Music") or g}', f'Back Pic: {back or "Brendan"}']
    ai = header_field(tr['header'], 'AI')
    if ai:
        lines.append(f'AI: {ai}')
    lines.append('')
    for j in idx:
        mon = re.sub(r'^Level:\s*\d+', f'Level: {LEVEL}', tr['mons'][j], flags=re.M)
        lines.append(mon.strip('\n'))
        lines.append('')
    blocks.append('\n'.join(lines))
    consts.append((f'PARTNER_STADIUM_{pname}', back is None))
    scores[pname] = (sum(bst(keys[j]) for j in idx) / len(idx) + CLASS_BONUS.get(header_field(tr['header'], 'Class'), 0)
                     + NAME_BONUS.get(pname, 0))

STEP = 100
EPIC_LAST = ['CYNTHIA', 'RED', 'WEATHER', 'CREATORS']     # de laatste vier, in deze volgorde
order = sorted((p for p, src, u in COMPANIONS if u != 'start' and p not in EPIC_LAST), key=lambda p: (scores[p], p))
order += [p for p in EPIC_LAST if p in scores]
threshold = {p: (1 if i == 0 else i * STEP) for i, p in enumerate(order)}
report += ['', '## Volgorde van vrijspelen (Stadium-punten: 70 per toernooi, +10 per gewonnen wedstrijd, +20 voor een titel)', '',
           '| Punten | Compagnon |', '|---|---|'] + [f'| {threshold[p]} | {p} |' for p in order]

party = open(PARTNERS, encoding='utf-8').read()
for old in (BEGIN, '# --- Battle Stadium (gegenereerd door tools/grounded/stadium/pool.py) ---'):
    if old in party:
        party = party[:party.index(old)].rstrip('\n') + '\n'
party = party.rstrip('\n') + '\n\n' + BEGIN + '\n\n' + '\n'.join(blocks) + '\n' + END + '\n'
open(PARTNERS, 'w', encoding='utf-8').write(party)

h = open(PARTNER_H, encoding='utf-8').read()
h = re.sub(r'\n// Battle Stadium \(pool\.py\)\n.*?(?=#define PARTNER_COUNT)', '\n', h, flags=re.S)
base = int(re.search(r'#define PARTNER_COUNT (\d+)', h).group(1)) if 'PARTNER_STADIUM' not in h else None
first = max(int(x) for x in re.findall(r'#define PARTNER_\w+ (\d+)', h.split('#define PARTNER_COUNT')[0])) + 1
defs = '// Battle Stadium (pool.py)\n' + ''.join(f'#define {c} {first + i}\n' for i, (c, _) in enumerate(consts))
h = re.sub(r'#define PARTNER_COUNT \d+', defs + f'#define PARTNER_COUNT {first + len(consts)}', h)
open(PARTNER_H, 'w', encoding='utf-8').write(h)

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('// Gegenereerd door tools/grounded/stadium/pool.py; niet met de hand bewerken.\n\n')
    f.write('// {trainer, sterkte (gem. BST van de singles-keuze), rivaal voor speler-geslacht (0 = altijd, 1 = man, 2 = vrouw),\n')
    f.write('//  keuze singles (bitmasker teamplekken), keuze doubles, overworld-sprite in de arena}\n')
    f.write('static const struct StadiumEntrant sStadiumPool[] =\n{\n')
    for t, r, g, gfx in rows:
        f.write(f'    {{TRAINER_{t}, {r}, {g}, 0x{masks[t][0]:02X}, 0x{masks[t][1]:02X}, {gfx}}},\n')
    f.write('};\n\n')
    f.write('// {partner, bron-trainer, voorplaatje i.p.v. rugplaatje, vrijspelen: STADIUM_UNLOCK_*, waarde}\n')
    f.write('static const struct StadiumCompanion sStadiumCompanions[] =\n{\n')
    for (pname, src, unlock), (c, front) in zip(COMPANIONS, consts):
        if unlock == 'start':
            u = 'STADIUM_UNLOCK_START, 0'
        else:
            u = f'STADIUM_UNLOCK_POINTS, {threshold[pname]}'
        if src:
            gfx = gfx_for(src, trainers[src]['header'])
        else:   # collectie: de eerste Pokémon als overworld-sprite
            lead = next(t for t in TRIOS if t[0] == pname)[4][0][0].split(' @ ')[0]
            gfx = f"OBJ_EVENT_GFX_SPECIES({species_key(lead) or 'PIKACHU'})"
        f.write(f'    {{{c}, {"TRAINER_" + src if src else "TRAINER_NONE"}, {"TRUE" if front else "FALSE"}, {u}, {gfx}}},\n')
    f.write('};\n')
open(os.path.join(ROOT, 'STADIUM_TEAMS.md'), 'w', encoding='utf-8').write('\n'.join(report) + '\n')
print(f'{len(rows)} deelnemers, {len(COMPANIONS)} compagnons -> {os.path.relpath(OUT, ROOT)}')
for t, r, g, gfx in sorted(rows, key=lambda x: -x[1]):
    print(f'  {r:4d}  {t}')
