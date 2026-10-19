#!/usr/bin/env python3

"""
Usage: python3 make_teachable.py SOURCE_LEARNSETS_JSON

Build a C-header defining the set of teachable moves for each configured-on
species-family based on the learnable moves defined in SOURCE_LEARNSETS_JSON.

A move is "teachable" if it is:
    1. Can be taught by some Move Tutor in the overworld, which is identified by
       using the ChooseMonForMoveTutor special in a script and setting VAR_0x8005
       to the offered MOVE constant. (e.g., MOVE_SWAGGER)
    2. Assigned to some TM or HM in include/constants/tms_hms.h using the
       FOREACH_TM macro.
    3. Not a universal move, as defined by sUniversalMoves in src/pokemon.c.

For a given species, a move is considered teachable to that species if:
    1. The species is not NONE -- which learns nothing -- nor MEW -- which
       learns everything.
    2. The species can learn the move via *any* method within any Expansion-
       supported game.
"""

from itertools import chain
from textwrap import dedent

import glob
import json
import pathlib
import re
import sys
import typing


CONFIG_ENABLED_PAT = re.compile(r"#define P_LEARNSET_HELPER_TEACHABLE\s+(?P<cfg_val>[^ ]*)")
INCFILE_HAS_TUTOR_PAT = re.compile(r"special ChooseMonForMoveTutor")
INCFILE_MOVE_PAT = re.compile(r"setvar VAR_0x8005, (MOVE_.*)")
TMHM_MACRO_PAT = re.compile(r"F\((\w+)\)")
UNIVERSAL_MOVES_PAT = re.compile(r"static const u16 sUniversalMoves\[\]\s*=\s*{((.|\n)*?)\n};")
TEACHABLE_ARRAY_DECL_PAT = re.compile(r"(?P<decl>static const u16 s(?P<name>\w+)TeachableLearnset\[\]) = {[\s\S]*?};")
SNAKIFY_PAT = re.compile(r"(?!^)([A-Z]+)")
TUTOR_ARRAY_ENABLED_PAT = re.compile(r"#define\s+P_TUTOR_MOVES_ARRAY\s+(?P<cfg_val>[^ ]*)")


def enabled() -> bool:
    """
    Check if the user has explicitly enabled this opt-in helper.
    """
    with open("./include/config/pokemon.h", "r") as cfg_pokemon_fp:
        cfg_pokemon = cfg_pokemon_fp.read()
        cfg_defined = CONFIG_ENABLED_PAT.search(cfg_pokemon)
        return cfg_defined is not None and cfg_defined.group("cfg_val") in ("TRUE", "1")


def extract_repo_tutors() -> typing.Generator[str, None, None]:
    """
    Yield MOVE constants which are *likely* assigned to a move tutor. This isn't
    foolproof, but it's suitable.
    """
    for inc_fname in chain(glob.glob("./data/scripts/*.inc"), glob.glob("./data/maps/*/scripts.inc")):
        with open(inc_fname, "r") as inc_fp:
            incfile = inc_fp.read()
            if not INCFILE_HAS_TUTOR_PAT.search(incfile):
                continue

            for move in INCFILE_MOVE_PAT.finditer(incfile):
                yield move.group(1)


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


def extract_repo_universals() -> list[str]:
    """
    Return a list of MOVE constants which are deemed to be universal and can
    thus be learned by any species.
    """
    with open("./src/pokemon.c", "r") as pokemon_fp:
        if match := UNIVERSAL_MOVES_PAT.search(pokemon_fp.read()):
            return list(filter(lambda s: s, map(lambda s: s.strip(), match.group(1).split(','))))
        return list()


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
    "MOVE_HIGH_JUMP_KICK", "MOVE_JUMP_KICK", "MOVE_BLAZE_KICK", "MOVE_ROLLING_KICK", "MOVE_TRIPLE_KICK", "MOVE_TRIPLE_AXEL",
}, "types": set(), "species": {"Tyrogue", "Hitmonlee"}}
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
}
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


def prepare_output(all_learnables: dict[str, set[str]], repo_teachables: set[str], header: str) -> str:
    """
    Build the file content for teachable_learnsets.h.
    """
    with open("./src/data/pokemon/teachable_learnsets.h", "r") as teachables_fp:
        old = teachables_fp.read()

    cursor = 0
    learnset_types = grounded_learnset_types()
    new = header + dedent("""
    static const u16 sNoneTeachableLearnset[] = {
        MOVE_UNAVAILABLE,
    };
    """)

    joinpat = ",\n    "
    for species in TEACHABLE_ARRAY_DECL_PAT.finditer(old):
        match_b, match_e = species.span()
        species_upper = SNAKIFY_PAT.sub(r"_\1", species.group("name")).upper()
        if species_upper == "NONE":
            # NONE is hard-coded to be at the start of the file to keep this code simple.
            cursor = match_e + 1
            continue

        if species_upper == "MEW":
            new += old[cursor:match_e + 1] # copy the original content and skip.
            cursor = match_e + 1
            continue

        repo_species_teachables = list(filter(lambda m: m in repo_teachables, all_learnables[species_upper]))
        for move, rule in GROUNDED_CUSTOM_TEACHABLES.items():
            if move in repo_teachables and move not in repo_species_teachables and species.group("name") not in rule.get("exclude", set()) and (
                ({rule["like"]} if isinstance(rule["like"], str) else rule["like"]) & set(all_learnables[species_upper])
                or learnset_types.get(species.group("name"), set()) & rule["types"]
                or species.group("name") in rule.get("species", set())
            ):
                repo_species_teachables.append(move)

        new += old[cursor:match_b]
        new += "\n".join([
            f"{species.group('decl')} = {{",
            f"    {joinpat.join(chain(repo_species_teachables, ('MOVE_UNAVAILABLE',)))},",
            "};\n",
        ])
        cursor = match_e + 1

    new += old[cursor:]

    return new


def create_tutor_moves_array(tutors: list[str]) -> None:
    """
    Generate gTutorMoves[] if P_TUTOR_MOVES_ARRAY is enabled.
    """
    # Check if the config is enabled
    with open("./include/config/pokemon.h", "r") as cfg_pokemon_fp:
        cfg_pokemon = cfg_pokemon_fp.read()
        cfg_defined = TUTOR_ARRAY_ENABLED_PAT.search(cfg_pokemon)
        if not (cfg_defined and cfg_defined.group("cfg_val") in ("TRUE", "1")):
            return

    # If enabled, generate the tutor moves array
    header = dedent("""\
        // DO NOT MODIFY THIS FILE! It is auto-generated by tools/learnset_helpers/make_teachables.py
        // Set the config P_TUTOR_MOVES_ARRAY in include/config/pokemon.h to TRUE to enable this array!
        // Also need by tutor moves relearner!

        const u16 gTutorMoves[] = {
    """)

    lines = [f"    {move}," for move in sorted(tutors)]
    lines.append("    MOVE_UNAVAILABLE\n};\n")

    with open("./src/data/tutor_moves.h", "w") as f:
        f.write(header + "\n".join(lines))


def prepare_header(h_align: int, tmshms: list[str], tutors: list[str], universals: list[str]) -> str:
    universals_title = "Near-universal moves found from sUniversalMoves:"
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


def main():
    if not enabled():
        quit()

    if len(sys.argv) < 2:
        print("Missing required arguments", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        quit(1)

    SOURCE_LEARNSETS_JSON = pathlib.Path(sys.argv[1])

    assert SOURCE_LEARNSETS_JSON.exists(), f"{SOURCE_LEARNSETS_JSON=} does not exist"
    assert SOURCE_LEARNSETS_JSON.is_file(), f"{SOURCE_LEARNSETS_JSON=} is not a file"

    repo_universals = extract_repo_universals()
    repo_tms = list(extract_repo_tms())
    repo_tutors = list(extract_repo_tutors())
    repo_teachables = set(filter(
        lambda move: move not in set(repo_universals),
        chain(repo_tms, repo_tutors)
    ))

    create_tutor_moves_array(repo_tutors)

    h_align = max(map(lambda move: len(move), chain(repo_universals, repo_teachables))) + 2
    header = prepare_header(h_align, repo_tms, repo_tutors, repo_universals)

    with open(SOURCE_LEARNSETS_JSON, "r") as source_fp:
        all_learnables = json.load(source_fp)

    content = prepare_output(all_learnables, repo_teachables, header)
    with open("./src/data/pokemon/teachable_learnsets.h", "w") as teachables_fp:
        teachables_fp.write(content)


if __name__ == "__main__":
    main()
