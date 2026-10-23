#!/usr/bin/env python3

"""
Usage: python3 make_teachable.py SOURCE_DIR

Build a C-header defining the set of teachable moves for each configured-on
species-family based on the learnable moves defined in SOURCE_DIR/all_learnables.json.

A move is "teachable" if it is:
    1. Can be taught by some Move Tutor in the overworld, which is identified by
       using the ChooseMonForMoveTutor special in a script and setting VAR_0x8005
       to the offered MOVE constant. (e.g., MOVE_SWAGGER)
    2. Assigned to some TM or HM in include/constants/tms_hms.h using the
       FOREACH_TM macro.
    3. A universal move, as defined by universalMoves in
       src/data/pokemon/special_movesets.json

For a given species, a move is considered teachable to that species if:
    1. The species can learn the move via *any* method within any Expansion-
       supported game.
    2. The species rule defined by their teachingType in the species_info folder
"""

from itertools import chain
from textwrap import dedent

import glob
import json
import pathlib
import re
import sys
import typing


CONFIG_ENABLED_PAT = re.compile(r"^#define P_LEARNSET_HELPER_TEACHABLE\s+(?P<cfg_val>[^ ]*)", flags=re.MULTILINE)
ALPHABETICAL_ORDER_ENABLED_PAT = re.compile(r"^#define HGSS_SORT_TMS_BY_NUM\s+(?P<cfg_val>[^ ]*)", flags=re.MULTILINE)
TM_LITERACY_PAT = re.compile(r"^#define P_TM_LITERACY\s+GEN_(?P<cfg_val>[^ ]*)", flags=re.MULTILINE)
TMHM_MACRO_PAT = re.compile(r"F\((\w+)\)")
SNAKIFY_PAT = re.compile(r"(?!^)([A-Z]+)")

def enabled() -> bool:
    """
    Check if the user has explicitly enabled this opt-in helper.
    """
    with open("./include/config/pokemon.h", "r") as cfg_pokemon_fp:
        cfg_pokemon = cfg_pokemon_fp.read()
        cfg_defined = CONFIG_ENABLED_PAT.search(cfg_pokemon)
        return cfg_defined is not None and cfg_defined.group("cfg_val") in ("TRUE", "1")

def extract_repo_tms() -> typing.Generator[str, None, None]:
    """
    Yield MOVE constants assigned to a TM or HM in the user's repo.
    """
    with open("./include/constants/tms_hms.h", "r") as tmshms_fp:
        tmshms = tmshms_fp.read()
        match_it = TMHM_MACRO_PAT.finditer(tmshms)
        if not match_it:
            return

        for match in match_it:
            yield f"MOVE_{match.group(1)}"

def extract_tm_litteracy_config() -> bool:
    config = False
    with open("./include/config/pokemon.h", "r") as cfg_pokemon_fp:
        cfg_pokemon = cfg_pokemon_fp.read()
        cfg_defined = TM_LITERACY_PAT.search(cfg_pokemon)
        if cfg_defined:
            cfg_val = cfg_defined.group("cfg_val")
            if ((cfg_val == "LATEST") or (int(cfg_val) > 6)):
                config = True
    return config

# Project Grounded: eigen TM-moves die in geen enkele officiële game bestaan.
# Een soort kan zo'n move leren als hij de "like"-move kan leren (in welke game dan ook)
# of als hij (in dit project) een van de genoemde types heeft.
GROUNDED_CUSTOM_TEACHABLES = {
    "MOVE_SELTZER_SURGE": {"like": "MOVE_SCALD", "types": {"TYPE_WATER"}},
}
# Lager Lagoon (bier) en Vintage Spill (wijn): iedereen die water kan maken, plus soorten die dicht bij
# het brouw- of wijnproces staan (taak "learnsets" in de changelog).
# Water Gun als criterium gaf Rattata, Clefairy enz. (Gen 1-TM); daarom Water-types plus deze natuurlijke watermakers.
WATER_MAKERS = {
    "Azurill", "Phanpy", "Donphan", "Dewgong", "Dragalge",  # sproeien water, of leven erin
    "Goomy", "Sliggoo", "Goodra", "SliggooHisui", "GoodraHisui",
}
GROUNDED_CUSTOM_TEACHABLES["MOVE_LAGER_LAGOON"] = {"like": set(), "types": {"TYPE_WATER"}, "species": WATER_MAKERS | {
    "Hoppip", "Skiploom", "Jumpluff",                       # hop
    "Skwovet", "Greedent",                                  # graanvoorraad
    "Paras", "Parasect", "Shroomish", "Breloom",            # gist en schimmels
    "Foongus", "Amoonguss", "Morelull", "Shiinotic", "Toedscool", "Toedscruel",
    "Gulpin", "Swalot",                                     # gisting in de maag
    "Spinda", "Snorlax", "Munchlax",                        # vaste klanten
}}
GROUNDED_CUSTOM_TEACHABLES["MOVE_VINTAGE_SPILL"] = {"like": set(), "types": {"TYPE_WATER"}, "species": WATER_MAKERS | {
    "Bounsweet", "Steenee", "Tsareena",                     # druiven treden
    "Shuckle",                                              # laat bessen gisten in zijn schild
    "Cherubi", "Cherrim", "Tropius",                        # fruit
    "Applin", "Flapple", "Appletun", "Dipplin", "Hydrapple",
    "Phantump", "Trevenant", "Dhelmise",                    # eikenhouten vaten en scheepsladingen
    "Gulpin", "Swalot", "Spinda",                           # gisting en proeverij
}}
# Laser Beam (TM55, Tate & Liza): alles wat lasers kan afschieten (schietarmen, kanonnen, stralen) plus logische Psychic-soorten.
GROUNDED_CUSTOM_TEACHABLES["MOVE_LASER_BEAM"] = {"like": set(), "types": set(), "species": {
    "Porygon", "Porygon2", "PorygonZ", "Magnemite", "Magneton", "Magnezone", "Remoraid", "Octillery",
    "Magmortar", "Blastoise", "Clauncher", "Clawitzer", "Genesect", "Staryu", "Starmie", "Metang", "Metagross",
    "Registeel", "Probopass", "Bronzor", "Bronzong", "Vikavolt", "Golett", "Golurk", "Duraludon", "Archaludon",
    "DeoxysNormal", "DeoxysAttack", "DeoxysDefense", "DeoxysSpeed", "Necrozma", "Solgaleo", "Lunala", "Celesteela",
    "Abra", "Kadabra", "Alakazam", "Espeon", "Elgyem", "Beheeyem", "Mewtwo", "Kirlia", "Gardevoir", "Gallade",
    "Natu", "Xatu", "Baltoy", "Claydol", "Lunatone", "Solrock", "Gothitelle", "Reuniclus", "Sigilyph", "Orbeetle",
    "Inkay", "Malamar", "Hatterene", "Espathra", "Calyrex", "CalyrexIce", "CalyrexShadow", "Girafarig", "Farigiraf",
}}
# Machine Learning (TM54, Wattson): machine-Pokémon, vooral die door een soort AI bestuurd kunnen worden.
# Pyukumuku is Water maar kan geen water spuiten (Jordi): geen water-aanvallen via TM.
NO_WATER_ATTACKS = {"Pyukumuku"}
for _m in ("MOVE_SELTZER_SURGE", "MOVE_LAGER_LAGOON", "MOVE_VINTAGE_SPILL"):
    GROUNDED_CUSTOM_TEACHABLES[_m]["exclude"] = NO_WATER_ATTACKS
GROUNDED_CUSTOM_TEACHABLES["MOVE_MACHINE_LEARNING"] = {"like": set(), "types": set(), "species": {
    "Porygon", "Porygon2", "PorygonZ", "Magnemite", "Magneton", "Magnezone", "Rotom", "Klink", "Klang", "Klinklang",
    "Genesect", "Magearna", "IronBundle", "IronHands", "IronJugulis", "IronMoth", "IronThorns", "IronValiant",
    "IronLeaves", "IronBoulder", "IronCrown", "IronTreads", "Golett", "Golurk", "Beldum", "Metang", "Metagross",
    "Registeel", "Regieleki", "Regigigas", "Voltorb", "Electrode", "VoltorbHisui", "ElectrodeHisui", "Varoom", "Revavroom",
}}
# Shadow Siphon (TM56, Mt. Pyre): zuigt op afstand de schaduw/levenskracht weg, zonder contact.
# Special Dark-aanvallers plus sinistere soorten die op afstand griezelige dingen doen.
GROUNDED_CUSTOM_TEACHABLES["MOVE_SHADOW_SIPHON"] = {"like": set(), "types": set(), "species": {
    "Houndour", "Houndoom", "Murkrow", "Honchkrow", "Zorua", "Zoroark", "ZoruaHisui", "ZoroarkHisui",
    "Deino", "Zweilous", "Hydreigon", "Darkrai", "Yveltal", "Nickit", "Thievul", "MoltresGalar",
    "Inkay", "Malamar", "HoopaUnbound", "ChiYu", "Pecharunt", "Spiritomb", "Misdreavus", "Mismagius",
    "Impidimp", "Morgrem", "Grimmsnarl", "Shuppet", "Banette", "Zubat", "Golbat", "Crobat",
    "Sableye", "Gastly", "Haunter", "Gengar", "Duskull", "Dusclops", "Dusknoir", "Drifloon",
    "Drifblim", "Litwick", "Lampent", "Chandelure", "Froslass", "Noibat", "Noivern", "Sinistea",
    "Polteageist", "Dreepy", "Drakloak", "Dragapult", "Gimmighoul", "Gholdengo"
}}
# Acid Rain (TM57, Aqua-grunt): alle Poison-types plus soorten die met vervuiling of weer te maken hebben.
GROUNDED_CUSTOM_TEACHABLES["MOVE_ACID_RAIN"] = {"like": set(), "types": {"TYPE_POISON"}, "species": {
    "Castform", "Torkoal", "Rolycoly", "Carkol", "Coalossal", "Slugma", "Magcargo",
}}
# Pollen Haze (TM58, Bug Maniac op Route 119): alle Bug- en Grass-types.
GROUNDED_CUSTOM_TEACHABLES["MOVE_POLLEN_HAZE"] = {"like": set(), "types": {"TYPE_BUG", "TYPE_GRASS"}}
# Rolling Thunder (TM73, Mustard in de Kubfu-dojo): de MMA-draaitrap. Iedereen die al een echte trap kan leren,
# plus de Hitmonlee-lijn.
GROUNDED_CUSTOM_TEACHABLES["MOVE_ROLLING_THUNDER"] = {"like": {
    "MOVE_HIGH_JUMP_KICK", "MOVE_JUMP_KICK", "MOVE_BLAZE_KICK", "MOVE_ROLLING_KICK",  # zonder Triple Axel/Kick (Milotic, Articuno)
}, "types": set(), "species": {"Tyrogue", "Hitmonlee", "Sawk"}}
# Moves 920-924 (TM89-92, TM96), voorstel geactiveerd 19 okt.
# Cold Shoulder (TM89): Ice-types plus koude/afstandelijke soorten die iemand links laten liggen.
GROUNDED_CUSTOM_TEACHABLES["MOVE_COLD_SHOULDER"] = {"like": set(), "types": {"TYPE_ICE"}, "species": {
    "Persian", "Liepard", "Purrloin", "MeowsticM", "MeowsticF", "Espeon", "Umbreon", "Glameow", "Purugly",
    "Absol", "Houndoom", "Zangoose", "Seviper", "Milotic", "Tsareena", "ToxtricityAmped", "ToxtricityLowKey",
    "Gothita", "Gothorita", "Gothitelle", "Hatterene", "Grimmsnarl", "Mandibuzz", "Kingambit", "Bisharp",
    "Empoleon", "Prinplup", "Piplup", "Dewgong", "Lapras", "Walrein", "Kingdra", "Gyarados",
}}
# Jump Scare (TM90): Ghost-types plus schrikaanjagers (verstoppen zich, springen tevoorschijn, bang maken).
GROUNDED_CUSTOM_TEACHABLES["MOVE_JUMP_SCARE"] = {"like": set(), "types": {"TYPE_GHOST"}, "species": {
    "Zorua", "Zoroark", "ZoruaHisui", "ZoroarkHisui", "Kecleon", "Sudowoodo", "Ditto", "Smeargle",
    "Gengar", "Sableye", "Mawile", "Murkrow", "Honchkrow", "Noibat", "Noivern", "Woobat", "Swoobat",
    "Zubat", "Golbat", "Crobat", "Gligar", "Gliscor", "Spinarak", "Ariados", "Joltik", "Galvantula",
    "Trapinch", "Wobbuffet", "Wynaut", "Impidimp", "Morgrem", "Grimmsnarl", "Mimikyu", "Hoothoot", "Noctowl",
    "Exploud", "Loudred", "Whismur", "Jigglypuff", "Wigglytuff", "Ekans", "Arbok", "Krookodile", "Sandaconda",
}}
# Dim Mak (TM91): vechtsporters/kungfu en Psychic-soorten met handen.
GROUNDED_CUSTOM_TEACHABLES["MOVE_DIM_MAK"] = {"like": {"MOVE_FORCE_PALM", "MOVE_DRAIN_PUNCH"}, "types": set(), "species": {
    "Mienfoo", "Mienshao", "Hitmonlee", "Hitmonchan", "Hitmontop", "Tyrogue", "Meditite", "Medicham",
    "Riolu", "Lucario", "Throh", "Sawk", "Kubfu", "UrshifuSingleStrike", "UrshifuRapidStrike", "Pangoro", "Hawlucha",
    "Gallade", "Abra", "Kadabra", "Alakazam", "MrMime", "MrMimeGalar", "MrRime", "MimeJr", "Hypno", "Drowzee",
    "Jynx", "Smoochum", "Gothitelle", "Malamar", "Grumpig", "Oranguru", "Slowking", "Lopunny", "Infernape",
}}
# Updraft (TM92): vliegers die met hun vleugels wind maken (zweefvliegers en windmakers), geen ballonnen/zwevers.
GROUNDED_CUSTOM_TEACHABLES["MOVE_UPDRAFT"] = {"like": {"MOVE_GUST", "MOVE_TAILWIND", "MOVE_AIR_SLASH"}, "types": set(), "species": {
    "Pelipper", "Wingull", "Swanna", "Ducklett", "Unfezant", "Tranquill", "Pidove", "Braviary", "Mandibuzz",
    "Vullaby", "Rufflet", "Skarmory", "Corviknight", "Altaria", "Swablu", "Tropius", "Mantine", "Mantyke",
    "Kilowattrel", "Wattrel", "Bombirdier", "Flamigo", "Tornadus", "Lugia", "HoOh", "Rayquaza",
}}
# Counterfeit Ball (TM96, wens Jordi): Pokemon die oplichten of voor de gek houden, plus dieven met handen die kunnen gooien.
GROUNDED_CUSTOM_TEACHABLES["MOVE_COUNTERFEIT_BALL"] = {"like": set(), "types": set(), "species": {
    "Meowth", "Persian", "MeowthAlola", "PersianAlola", "MeowthGalar", "Perrserker",
    "Purrloin", "Liepard", "Zorua", "Zoroark", "ZoruaHisui", "ZoroarkHisui", "Sableye", "Mimikyu",
    "Impidimp", "Morgrem", "Grimmsnarl", "Croagunk", "Toxicroak", "Nickit", "Thievul", "Grafaiai",
    "Murkrow", "Honchkrow", "Sneasel", "Weavile", "SneaselHisui", "Sneasler", "Scraggy", "Scrafty",
    "Sandile", "Krokorok", "Krookodile", "Inkay", "Malamar", "Gastly", "Haunter", "Gengar", "Banette",
    "MrMime", "MrMimeGalar", "MrRime", "MimeJr", "Shiftry", "Cottonee", "Whimsicott", "Spinda",
    "Kecleon", "Gimmighoul", "Gholdengo", "Aipom", "Ambipom", "HoopaConfined", "HoopaUnbound",
}}
# Overkill (TM45, was Attract): fysieke Dark-types (Attack >= Sp. Atk, in dit project) plus brute, genadeloze soorten.
GROUNDED_CUSTOM_TEACHABLES["MOVE_OVERKILL"] = {"like": set(), "types": set(), "phys_types": {"TYPE_DARK"}, "species": {
    "Arbok", "Houndoom", "Hydreigon", "Larvitar", "Pupitar", "Tyranitar", "Gyarados", "Teddiursa", "Ursaring",
    "Ursaluna", "UrsalunaBloodmoon", "Axew", "Fraxure", "Haxorus", "Gible", "Gabite", "Garchomp", "Salamence",
    "Tyrunt", "Tyrantrum", "Rhydon", "Rhyperior", "Machamp", "Conkeldurr", "Hariyama", "Primeape", "Annihilape",
    "Scizor", "Kleavor", "Zangoose", "Seviper", "Escavalier", "Golisopod", "Darmanitan", "Mamoswine",
    "Feraligatr", "Bewear", "Granbull", "Barraskewda", "KommoO", "Guzzlord",
}}
# Disco Inferno (TM99): alleen dansers. Vuur-dansers, plus iedereen met Dancer of een dansmove (geen Swords Dance).
GROUNDED_CUSTOM_TEACHABLES["MOVE_DISCO_INFERNO"] = {"like": {
    "MOVE_QUIVER_DANCE", "MOVE_FEATHER_DANCE", "MOVE_TEETER_DANCE", "MOVE_LUNAR_DANCE", "MOVE_VICTORY_DANCE",
    "MOVE_REVELATION_DANCE", "MOVE_PETAL_DANCE", "MOVE_DRAGON_DANCE", "MOVE_FIERY_DANCE", "MOVE_AQUA_STEP",
}, "types": set(), "abilities": {"ABILITY_DANCER"}, "species": {
    "Magby", "Magmar", "Magmortar", "Cyndaquil", "Quilava", "Typhlosion", "TyphlosionHisui",
    "Torchic", "Combusken", "Blaziken", "Chimchar", "Monferno", "Infernape", "Pansear", "Simisear",
    "Fennekin", "Braixen", "Delphox", "Litten", "Torracat", "Incineroar", "Scorbunny", "Raboot", "Cinderace",
    "Charcadet", "Armarouge", "Ceruledge", "Charmander", "Charmeleon", "Charizard", "Cubone", "MarowakAlola",
    "Oricorio", "Blacephalon", "Victini", "Capsakid", "Scovillain",
}}
# Super Splash (TM100, Devon): alleen wie Splash via level-up leert (gen_9.h).
GROUNDED_CUSTOM_TEACHABLES["MOVE_SUPER_SPLASH"] = {"like": set(), "types": set(), "levelup": {"MOVE_SPLASH"}}
# Set-audit (Jordi 19 okt): bestaande TM's die deze soorten van Jordi ook mogen leren.
GROUNDED_EXTRA_TM_SPECIES = {
    "MOVE_BATON_PASS": {"Skarmory"},   # TM79 (19 okt): Skarmory-sets van Jordi
    "MOVE_KNOCK_OFF": {"Dusknoir"},    # TM81 (19 okt): Dusknoir-sets van Jordi
    "MOVE_BRICK_BREAK": {"Farfetchd"},
    "MOVE_TRICK_ROOM": {"Wynaut", "Wobbuffet"},
    "MOVE_CALM_MIND": {"Regice"},
    "MOVE_VOLT_SWITCH": {"Porygon", "Porygon2", "PorygonZ"},
    "MOVE_THUNDERBOLT": {"Abra", "Kadabra", "Alakazam"},
    "MOVE_DAZZLING_GLEAM": {"Woobat", "Swoobat"},
    "MOVE_FLAMETHROWER": {"Helioptile", "Heliolisk"},
    "MOVE_IRON_HEAD": {"Ursaluna"},
    # TM93 Power Gem: edelstenen, kristallen en parels.
    "MOVE_POWER_GEM": {"Lileep", "Cradily", "Omanyte", "Omastar", "Roggenrola", "Bergmite", "Avalugg", "AvaluggHisui",
                       "Dwebble", "Crustle", "Clamperl", "Huntail", "Gorebyss", "Cryogonal"},
    # TM94 Wood Hammer (lijst van Jordi) plus evolutielijnen.
    "MOVE_WOOD_HAMMER": {"Bonsly", "Tropius", "Turtwig", "Grotle", "Dartrix", "Decidueye", "DecidueyeHisui",
                         "Nuzleaf", "Shiftry", "Breloom", "Lombre", "Ludicolo"},
    # TM95 Dragon Rush: draken die kunnen aanstormen en draakachtigen.
    "MOVE_DRAGON_RUSH": {"Aerodactyl", "Tyrunt", "Tyrantrum", "Sceptile", "Seadra", "Kingdra", "Axew", "Fraxure",
                         "Haxorus", "Druddigon", "Feraligatr", "JangmoO", "HakamoO", "KommoO", "Turtonator",
                         "ExeggutorAlola", "Tropius", "Dreepy", "Rayquaza", "Latias", "Latios", "Zekrom", "Reshiram",
                         "Kyurem", "Dialga", "Palkia", "Giratina", "Koraidon", "Miraidon", "Regidrago", "Zygarde",
                         "RagingBolt"},
    # TM97 Shell Smash: schelpen en pantsers.
    "MOVE_SHELL_SMASH": {"Kabuto", "Kabutops", "Slowbro", "SlowbroGalar", "Shelmet", "Escavalier"},
    # TM98 Fake Out: handen/poten om te verrassen (apen, katten, vechters, dieven, Normal-types met armen).
    "MOVE_FAKE_OUT": {
        "Mankey", "Primeape", "Annihilape", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour",
        "Oranguru", "Passimian", "Sprigatito", "Floragato", "Meowscarada", "Litleo", "Pyroar",
        "Machop", "Machoke", "Machamp", "Riolu", "Lucario", "Throh", "Sawk", "Timburr", "Gurdurr", "Conkeldurr",
        "Pancham", "Pangoro", "Hawlucha", "Crabrawler", "Crabominable", "Kubfu", "UrshifuSingleStrike",
        "UrshifuRapidStrike", "Stufful", "Bewear", "Nickit", "Thievul", "Zorua", "Zoroark", "ZoruaHisui",
        "ZoroarkHisui", "Shroodle", "Grafaiai", "Teddiursa", "Ursaring", "Slakoth", "Vigoroth", "Slaking",
        "Zangoose", "Smeargle", "Lickitung", "Lickilicky", "Miltank", "Loudred", "Exploud", "Snubbull", "Granbull",
    },
}
# TM_COMPAT_VOORSTEL.md, door Jordi goedgekeurd op 19 okt (zonder Wood Hammer en Super Splash; voorstellen met een verkeerd type eruit: Gyarados, Clefable, Pinsir, Lopunny, Grimer/Muk, Rotom).
GROUNDED_COMPAT_VOORSTEL = {
    "MOVE_FLARE_BLITZ": {"Groudon", "Sizzlipede"},
    "MOVE_ROCK_TOMB": {"Nacli", "Naclstack"},
    "MOVE_SNARL": {"Huntail", "Noctowl", "Hypno", "Cacturne", "Banette", "Dusknoir", "Inkay", "Malamar", "Greninja", "Grimmsnarl", "Impidimp", "Morgrem", "Overqwil"},
    "MOVE_ROOST": {"Torchic", "Combee", "Delibird", "Celesteela", "Tornadus", "Thundurus", "Landorus", "Rayquaza", "ArticunoGalar", "ZapdosGalar", "MoltresGalar"},
    "MOVE_BULK_UP": {"Spinda", "Farfetchd", "FarfetchdGalar", "Sirfetchd", "Pawmo", "LilligantHisui", "Cobalion", "Terrakion", "Virizion"},
    "MOVE_CHARGE_BEAM": {"Loudred", "Exploud", "Nosepass", "Probopass", "Starmie", "Yamper", "Boltund", "Toxel", "Stunfisk", "Zeraora", "TapuKoko"},
    "MOVE_THUNDER_WAVE": {"Loudred", "Exploud", "Toxel", "Oricorio"},
    "MOVE_ICY_WIND": {"DarumakaGalar", "DarmanitanGalar"},
    "MOVE_POISON_JAB": {"Muk", "Grimer", "Crobat", "Golbat", "Zubat", "Weedle", "Kakuna"},
    "MOVE_WILL_O_WISP": {"Volbeat", "Parasect", "Golett", "Golurk", "Honedge", "Doublade", "Aegislash", "Sandygast", "Palossand", "Annihilape", "Dreepy", "Decidueye"},
    "MOVE_TAILWIND": {"Torchic", "Rowlet", "Ninjask", "Celesteela", "Thundurus", "Landorus"},
    "MOVE_X_SCISSOR": {"Heracross", "Pheromosa", "Buzzwole", "Wimpod", "Flygon", "Vibrava", "Trapinch", "Shelmet"},
    "MOVE_WILD_CHARGE": {"Loudred", "Nosepass", "Tynamo", "Porygon"},
    "MOVE_HEAVY_SLAM": {"Loudred", "Mawile", "Scizor", "Kingambit", "Bisharp", "Excadrill", "Durant", "SandslashAlola", "Klinklang"},
    "MOVE_ENERGY_BALL": {"Applin"},
    "MOVE_BUG_BUZZ": {"Crustle", "Shuckle", "Kricketot", "Paras"},
    "MOVE_HEX": {"Parasect", "Honedge", "Doublade", "Aegislash", "Annihilape", "Oricorio", "Dreepy"},
    "MOVE_FOCUS_BLAST": {"Spinda", "Farfetchd", "Tyrogue"},
    "MOVE_KNOCK_OFF": {"Huntail", "Sharpedo", "Carvanha", "Mightyena", "Poochyena", "Honchkrow", "Murkrow", "Kingambit", "Deino", "Zweilous", "Sandile", "Spiritomb"},
    "MOVE_STONE_EDGE": {"Sableye", "Anorith"},
    "MOVE_HIGH_HORSEPOWER": {"Dodrio", "Doduo", "Golurk", "Golett", "Cubone", "Marowak", "Marshtomp", "Seismitoad", "Trapinch", "Garchomp", "Gible", "Gabite", "Larvitar", "TingLu", "Dunsparce", "Dudunsparce"},
    "MOVE_DRAGON_DANCE": {"Druddigon", "Gible", "Gabite", "Garchomp", "Deino", "Zweilous", "Dracozolt", "Dracovish", "Frigibax", "Arctibax", "Koraidon", "Giratina", "Guzzlord"},
    "MOVE_CLOSE_COMBAT": {"Throh", "Tyrogue", "Pancham", "Pawmo", "Stufful", "Spinda"},
    "MOVE_POWER_GEM": {"Kabuto", "Amaura", "Aurorus", "Golem", "Shuckle"},
    "MOVE_DRAGON_RUSH": {"Applin"},
    "MOVE_FAKE_OUT": {"Blaziken", "Combusken", "Emboar", "Breloom", "Heracross", "Gallade", "Poliwrath", "Chesnaught", "Quaquaval", "Okidogi", "Clobbopus", "Grapploct"},
}
for _m, _sp in GROUNDED_COMPAT_VOORSTEL.items():
    GROUNDED_EXTRA_TM_SPECIES[_m] = GROUNDED_EXTRA_TM_SPECIES.get(_m, set()) | _sp
for _m, _sp in GROUNDED_EXTRA_TM_SPECIES.items():
    _r = GROUNDED_CUSTOM_TEACHABLES.setdefault(_m, {"like": set(), "types": set()})
    _r["species"] = _r.get("species", set()) | _sp
SPECIES_BLOCK_PAT = re.compile(r"\[SPECIES_\w+\]\s*=")
LEARNSET_REF_PAT = re.compile(r"\.teachableLearnset\s*=\s*s(\w+)TeachableLearnset")
TYPE_PAT = re.compile(r"TYPE_[A-Z]+")


def grounded_learnset_types() -> dict[str, set[str]]:
    """
    Map each teachable-learnset name (e.g. "Magikarp") to the union of types of the
    species that use it, read from src/data/pokemon/species_info/*.h.
    """
    result: dict[str, set[str]] = {}
    for fname in glob.glob("./src/data/pokemon/species_info/*.h"):
        with open(fname, "r") as fp:
            text = fp.read()
        starts = [m.start() for m in SPECIES_BLOCK_PAT.finditer(text)] + [len(text)]
        for b, e in zip(starts, starts[1:]):
            block = text[b:e]
            ref = LEARNSET_REF_PAT.search(block)
            types_line = re.search(r"\.types\s*=[^\n]*", block)
            if ref and types_line:
                result.setdefault(ref.group(1), set()).update(TYPE_PAT.findall(types_line.group(0)))
    return result


LEVELUP_REF_PAT = re.compile(r"\.levelUpLearnset\s*=\s*s(\w+)LevelUpLearnset")
LEVELUP_ARRAY_PAT = re.compile(r"static const struct LevelUpMove s(\w+)LevelUpLearnset\[\] = \{(.*?)\};", re.S)


def grounded_learnset_info() -> dict[str, dict]:
    """
    Per teachable-learnset name: "physical" (baseAttack >= baseSpAttack of the first species using it),
    "abilities" (all abilities) and "levelup" (moves learned by level-up in gen_9.h).
    """
    with open("./src/data/pokemon/level_up_learnsets/gen_9.h", "r") as fp:
        levelup = {m.group(1): set(re.findall(r"MOVE_\w+", m.group(2))) for m in LEVELUP_ARRAY_PAT.finditer(fp.read())}
    result: dict[str, dict] = {}
    for fname in glob.glob("./src/data/pokemon/species_info/*.h"):
        with open(fname, "r") as fp:
            text = fp.read()
        starts = [m.start() for m in SPECIES_BLOCK_PAT.finditer(text)] + [len(text)]
        for b, e in zip(starts, starts[1:]):
            block = text[b:e]
            ref = LEARNSET_REF_PAT.search(block)
            if not ref:
                continue
            entry = result.setdefault(ref.group(1), {"abilities": set(), "levelup": set()})
            atk = re.search(r"\.baseAttack\s*=\s*(\d+)", block)
            spa = re.search(r"\.baseSpAttack\s*=\s*(\d+)", block)
            if atk and spa and "physical" not in entry:
                entry["physical"] = int(atk.group(1)) >= int(spa.group(1))
            abil = re.search(r"\.abilities\s*=\s*\{([^}]*)\}", block)
            if abil:
                entry["abilities"].update(re.findall(r"ABILITY_\w+", abil.group(1)))
            lvl = LEVELUP_REF_PAT.search(block)
            if lvl:
                entry["levelup"] |= levelup.get(lvl.group(1), set())
    return result


def prepare_output(all_learnables: dict[str, set[str]], tms: list[str], tutors: list[str], special_movesets, repo_teaching_types, header: str) -> str:
    """
    Build the file content for teachable_learnsets.h.
    """

    tm_litteracy_config = extract_tm_litteracy_config()

    cursor = 0
    new = header + dedent("""
    static const u16 sNoneTeachableLearnset[] = {
        MOVE_UNAVAILABLE,
    };
    """)

    joinpat = ",\n    "
    learnset_types = grounded_learnset_types()  # Project Grounded
    info = grounded_learnset_info()  # Project Grounded
    for species_data in repo_teaching_types:
        if isinstance(species_data, str):
            new += (species_data)
            continue
        species = species_data["name"]
        teaching_type = species_data["teaching_type"]
        new += f"static const u16 s{species}TeachableLearnset[] = "
        new += "{\n"
        species_upper =  SNAKIFY_PAT.sub(r"_\1", species).upper()
        if teaching_type == "ALL_TEACHABLES":
            part1 = list(filter(lambda m: m not in special_movesets["signatureTeachables"], tms))
            part2 = list(filter(lambda m: m not in special_movesets["signatureTeachables"], tutors))
        else:
            if teaching_type == "TM_ILLITERATE":
                learnables = all_learnables[species_upper]
                if not tm_litteracy_config:
                    learnables = filter(lambda m: m not in special_movesets["universalMoves"], learnables)
            else:
                learnables = all_learnables[species_upper] + special_movesets["universalMoves"]
            part1 = list(filter(lambda m: m in learnables, tms))
            part2 = list(filter(lambda m: m in learnables, tutors))


        repo_species_teachables = part1 + part2
        if species_upper == "TERAPAGOS":
             repo_species_teachables = filter(lambda m: m != "MOVE_TERA_BLAST", repo_species_teachables)

        # Project Grounded: eigen TM-moves en extra compatibiliteit (GROUNDED_CUSTOM_TEACHABLES)
        repo_species_teachables = list(repo_species_teachables)
        repo_teachables = set(tms) | set(tutors)
        species_learnables = set(all_learnables.get(species_upper, []))
        for move, rule in GROUNDED_CUSTOM_TEACHABLES.items():
            if move in repo_teachables and move not in repo_species_teachables and species not in rule.get("exclude", set()) and (
                ({rule["like"]} if isinstance(rule["like"], str) else rule["like"]) & species_learnables
                or learnset_types.get(species, set()) & rule["types"]
                or species in rule.get("species", set())
                or (info.get(species, {}).get("physical") and learnset_types.get(species, set()) & rule.get("phys_types", set()))
                or info.get(species, {}).get("abilities", set()) & rule.get("abilities", set())
                or info.get(species, {}).get("levelup", set()) & rule.get("levelup", set())
            ):
                repo_species_teachables.append(move)

        repo_species_teachables = list(dict.fromkeys(repo_species_teachables))
        new += "\n".join([
            f"    {joinpat.join(chain(repo_species_teachables, ('MOVE_UNAVAILABLE',)))},",
            "};\n",
        ])

    return new

def prepare_header(h_align: int, tmshms: list[str], tutors: list[str], universals: list[str]) -> str:
    universals_title = "Near-universal moves found in data/special_movesets.json:"
    tmhm_title = "TM/HM moves found in \"include/constants/tms_hms.h\":"
    tutor_title = "Tutor moves found from map scripts:"
    h_align = max(h_align, len(universals_title), len(tmhm_title), len(tutor_title))

    lines = [
         "//",
         "// DO NOT MODIFY THIS FILE! It is auto-generated by tools/learnset_helpers/make_teachables.py",
         "//",
         "",
        f"// {'*' * h_align} //",
        f"// {tmhm_title: >{h_align}} //",
    ]
    lines.extend([f"// - {move: <{h_align - 2}} //" for move in tmshms])
    lines.extend([
        f"// {'*' * h_align} //",
        f"// {tutor_title: <{h_align}} //",
    ])
    lines.extend([f"// - {move: <{h_align - 2}} //" for move in sorted(tutors)])
    lines.extend([
        f"// {'*' * h_align} //",
        f"// {universals_title: <{h_align}} //",
    ])
    lines.extend([f"// - {move: <{h_align - 2}} //" for move in universals])
    lines.extend([
        f"// {'*' * h_align} //",
         "",
    ])

    return "\n".join(lines)

def create_tutor_moves_array(tutors):
    """
    Generate gTutorMoves[].
    """
    header = dedent("""\
        // DO NOT MODIFY THIS FILE! It is auto-generated by tools/learnset_helpers/make_teachables.py
        // Needed by tutor moves relearner!

        const u16 gTutorMoves[] = {
    """)

    lines = [f"    {move}," for move in tutors]
    lines.append("    MOVE_UNAVAILABLE\n};\n")
    with open("./src/data/tutor_moves.h", "w") as f:
        f.write(header + "\n".join(lines))

def make_move_tutors(build_dir, special_movesets):
    SOURCE_TUTORS_JSON = build_dir / "all_tutors.json"

    assert SOURCE_TUTORS_JSON.exists(), f"{SOURCE_TUTORS_JSON=} does not exist"
    assert SOURCE_TUTORS_JSON.is_file(), f"{SOURCE_TUTORS_JSON=} is not a file"

    with open(SOURCE_TUTORS_JSON, "r") as fp:
        repo_tutors = json.load(fp)

    repo_tutors = sorted(list(set(repo_tutors + special_movesets["extraTutors"])))
    create_tutor_moves_array(repo_tutors)

    return repo_tutors

def main():
    if not enabled():
        quit()

    tutor_mode = False
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Invalid number of arguments", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        quit(1)

    if len(sys.argv) == 3:
        if sys.argv[1] != "--tutors":
            print("Unknown make_teachables mode", file=sys.stderr)
            quit(1)
        tutor_mode = True

    SOURCE_DIR = pathlib.Path(sys.argv[-1])

    with open("src/data/pokemon/special_movesets.json", "r") as file:
        special_movesets = json.load(file)

    repo_tutors = make_move_tutors(SOURCE_DIR, special_movesets)
    if tutor_mode:
        quit(0)

    SOURCE_LEARNSETS_JSON = pathlib.Path("./src/data/pokemon/all_learnables.json")
    SOURCE_TEACHING_TYPES_JSON = SOURCE_DIR / "all_teaching_types.json"

    assert SOURCE_LEARNSETS_JSON.exists(), f"{SOURCE_LEARNSETS_JSON=} does not exist"
    assert SOURCE_LEARNSETS_JSON.is_file(), f"{SOURCE_LEARNSETS_JSON=} is not a file"

    assert SOURCE_TEACHING_TYPES_JSON.exists(), f"{SOURCE_TEACHING_TYPES_JSON=} does not exist"
    assert SOURCE_TEACHING_TYPES_JSON.is_file(), f"{SOURCE_TEACHING_TYPES_JSON=} is not a file"

    repo_tms = list(extract_repo_tms())

    with open("./include/config/pokedex_plus_hgss.h", "r") as cfg_pokemon_fp:
        cfg_pokemon = cfg_pokemon_fp.read()
        cfg_defined = ALPHABETICAL_ORDER_ENABLED_PAT.search(cfg_pokemon)
        if cfg_defined is None or cfg_defined.group("cfg_val") in ("FALSE", "0"):
            repo_tms = sorted(repo_tms)

    h_align = max(map(lambda move: len(move), chain(special_movesets["universalMoves"], repo_tms, repo_tutors))) + 2
    header = prepare_header(h_align, repo_tms, repo_tutors, special_movesets["universalMoves"])

    with open(SOURCE_LEARNSETS_JSON, "r") as source_fp:
        all_learnables = json.load(source_fp)

    with open(SOURCE_TEACHING_TYPES_JSON, "r") as source_fp:
        repo_teaching_types = json.load(source_fp)

    content = prepare_output(all_learnables, repo_tms, repo_tutors, special_movesets, repo_teaching_types, header)
    with open("./src/data/pokemon/teachable_learnsets.h", "w") as teachables_fp:
        teachables_fp.write(content)

if __name__ == "__main__":
    main()
