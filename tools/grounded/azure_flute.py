#!/usr/bin/env python3
"""Project Grounded: de hintlijst van de Azure Flute (Arceus, SPACETIME_PLAN §3 stap 5-6).

Zoekt in de code welke legendaries en mythicals nu echt te krijgen zijn:
  - setwildbattle / seteventmon / givemon / giveegg met een legendary/mythical-soort in data/maps en data/scripts,
  - gifts via `setvar VAR_0x8004, SPECIES_X` + `call Grounded_EventScript_GiveGiftMon`,
  - wilde tabellen (src/data/wild_encounters.json) en de rondzwervende Lati (src/roamer.c).
Paradox-Pokemon tellen niet mee (SPACETIME_PLAN), Arceus zelf ook niet (de eindbaas). Soorten die niet in de game zitten
(Galar-vogels, Ultra Beasts, ...) worden niet gevonden en tellen dus vanzelf niet mee. Vormen van dezelfde soort
(Hoopa Confined/Unbound, Deoxys, Giratina) vallen samen: het Pokedex-nummer telt.

Per soort staat hieronder een hinttekst (huisstijl, kort) en eventueel een 'gone'-flag: de ontmoeting is voorgoed op
(verslagen zonder terugkeer, of de gift is al gegeven). Dan telt de soort ook als afgehandeld, anders zou de
Hall of Origin nooit opengaan. Volgorde = volgorde waarin de fluit hints geeft (ongeveer de volgorde in de game).

Schrijft src/data/azure_flute_hints.h en het icoon graphics/items/icons/azure_flute.png (+ .pal).
Een gevonden soort zonder hint geeft een waarschuwing en een algemene hint met de kaart; een hint voor een soort die
niet (meer) te krijgen is, valt weg.

Gebruik: python3 tools/grounded/azure_flute.py [--list]"""
import glob, importlib.util, json, os, re, sys

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
os.chdir(REPO)
_spec = importlib.util.spec_from_file_location('dialogen_import', 'tools/dialogen/import.py')
dimp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dimp)

# basissoort (zonder SPECIES_) -> (gone-flag of None, hint). Volgorde = volgorde van de hints.
HINTS = [
    # --- verhaal en post-game Hoenn
    ('RAIKOU', 'FLAG_HIDE_NEW_MAUVILLE_RAIKOU',
     "Under NEW MAUVILLE, past the vault, there's a thunderstorm that doesn't fit indoors. Something yellow is eating "
     "the bandwidth."),
    ('ENTEI', 'FLAG_HIDE_MT_CHIMNEY_ENTEI',
     "Somewhere beneath MT. CHIMNEY, a lava cave is hiding a dog that is also a volcano."),
    ('SUICUNE', 'FLAG_HIDE_ROUTE136_SUICUNE',
     "Dive off ROUTE 136. Under the ice there's a crystal cave, and in it a very clean, very judgmental dog."),
    ('REGIROCK', 'FLAG_DEFEATED_REGIROCK',
     "The DESERT RUINS on ROUTE 111 want to be read. In braille. Bring a patient POKéMON."),
    ('REGICE', 'FLAG_DEFEATED_REGICE',
     "ISLAND CAVE, off ROUTE 105. The walls are cold and full of dots. So is the tenant."),
    ('REGISTEEL', 'FLAG_DEFEATED_REGISTEEL',
     "The ANCIENT TOMB on ROUTE 120 is not a tomb. Nobody died. Something just refuses to move."),
    ('REGIELEKI', 'FLAG_DEFEATED_REGIELEKI',
     "A sealed cave on ROUTE 110 has been charging for three thousand years. Mind the dots."),
    ('REGIDRAGO', 'FLAG_DEFEATED_REGIDRAGO',
     "A sealed cave on ROUTE 130 hides a dragon that is mostly head. Solve the dots."),
    ('REGIGIGAS', 'FLAG_DEFEATED_REGIGIGAS',
     "Under the igloo in ASHFROST, a giant waits behind a wall of ice. Catch its five little ones and the ice melts "
     "out of respect."),
    ('KYOGRE', 'FLAG_DEFEATED_KYOGRE',
     "MARINE CAVE wanders beneath the eastern sea. Look for the spot where the rain won't stop crying."),
    ('GROUDON', 'FLAG_DEFEATED_GROUDON',
     "TERRA CAVE wanders beneath the eastern routes. Look for the spot where the sun refuses to set."),
    ('RAYQUAZA', None,
     "SKY PILLAR. You've been. It's still there, and so is RAYQUAZA. Beat the LEAGUE again if it left in a huff."),
    ('LATIAS', None,
     "Your rival's EON TICKET sails to SOUTHERN ISLAND. If the red one isn't there, it's flying around HOENN, "
     "avoiding you personally."),
    ('LATIOS', None,
     "Your rival's EON TICKET sails to SOUTHERN ISLAND. If the blue one isn't there, it's flying around HOENN, "
     "pretending to be a plane."),
    ('JIRACHI', None,
     "At night, the old crater in FALLARBOR TOWN takes wishes. Stand in it. Wish responsibly. MT. PYRE's summit has "
     "been known to grant one too."),
    ('DEOXYS', None,
     "The SPACE CENTER in MOSSDEEP launches more than satellites these days. Ask about the meteorite."),
    ('MEW', None,
     "The BATTLE FRONTIER sells an OLD SEA MAP. It leads to FARAWAY ISLAND, where something pink giggles in the "
     "grass."),
    ('LUGIA', None,
     "The SILVER WING from the SEA TEMPLE points at WHIRL ISLAND. Bring it. LUGIA doesn't come out for people "
     "without accessories."),
    ('HO_OH', None,
     "The MYSTICTICKET (BATTLE FRONTIER) sails to NAVEL ROCK. Climb. Then climb more. Rainbow at the top."),
    ('DARKRAI', 'FLAG_DEFEATED_DARKRAI',
     "Fall asleep on the summit of MT. PYRE, at night. The nightmare will take care of the rest."),
    ('CRESSELIA', None,
     "East of ROUTE 105 lies a half-moon island. Visit at night. Bring a lullaby, or a ball."),
    ('HEATRAN', 'FLAG_HIDE_FIERY_PATH_HEATRAN',
     "FIERY PATH has a back room, top left. Very hot. Very heavy. Very awake."),
    ('MANAPHY', None,
     "Dive under ROUTE 128 and find the SEA TEMPLE. A prince has waited there since 2006 for a ranger who never "
     "came. LAVARIDGE hands out eggs, too."),
    ('PHIONE', None,
     "After MANAPHY, the SEA TEMPLE's altar leaves you an egg. Hatch it. Or let MANAPHY have a family, if you're "
     "that kind of person."),
    ('KUBFU', None,
     "The dojo on ROUTE 112 hands a bear cub to the worthy. If you were worthy and lost it: the grass on ROUTE 115 "
     "is generous. Rarely."),
    ('HOOPA', None,
     "Out in the desert of ROUTE 111, a bazaar appears out of thin air. Someone there steals through rings. Follow "
     "the rings."),
    ('TORNADUS', 'FLAG_FORCES_TORNADUS_DONE',
     "Fog on ROUTE 113, 118 or 121. Not normal fog. Rude fog, with a tail."),
    ('THUNDURUS', 'FLAG_FORCES_THUNDURUS_DONE',
     "A thunderstorm on ROUTE 119, 120 or 123, and something in it laughing."),
    ('LANDORUS', 'FLAG_FORCES_LANDORUS_DONE',
     "A sandstorm on ROUTE 112, 114 or 117, with a cloud that has a face."),
    ('COBALION', 'FLAG_DEFEATED_COBALION',
     "Deep in GRANITE CAVE there's a sword chamber. A knight of steel wants a duel. Not a fight. A duel. "
     "Apparently there's a difference."),
    ('TERRAKION', 'FLAG_DEFEATED_TERRAKION',
     "VICTORY ROAD hides a sword chamber. Its tenant is a rock with a sense of honour."),
    ('VIRIZION', 'FLAG_DEFEATED_VIRIZION',
     "Somewhere in MANGROVE MIRE there's a glade where a green swordsman stands very elegantly in the mud."),
    ('KELDEO', 'FLAG_DEFEATED_KELDEO',
     "After the three swords, MR. BRINEY calls. Pick up. He knows an island that wasn't there yesterday."),
    ('MELTAN', 'FLAG_RECEIVED_MELTAN',
     "RIVET the welder in STERN's shipyard has a nut that moves. Ask nicely."),
    ('MAGEARNA', 'FLAG_RECEIVED_MAGEARNA',
     "Sink the PLASMA FRIGATE, then beat COLRESS in MAUVILLE. He built a robot that works. He's surprised too."),
    ('TYPE_NULL', 'FLAG_RECEIVED_TYPE_NULL',
     "DEVON CORPORATION, 2F. Someone in a lab coat wants to get rid of a 'prototype'. Don't ask about the helmet."),
    ('GENESECT', 'FLAG_HIDE_NEW_MAUVILLE_GENESECT',
     "NOTHING ISLAND, in the fog west of ROUTE 105. There's a ship there that insists it isn't one."),
    ('SHAYMIN', None,
     "The BLOOM TICKET (BATTLE FRONTIER) sails from LILYCOVE to FLOWER PARADISE. The hedgehog in the meadow is also "
     "a flower. Or the other way around."),
    ('VICTINI', None,
     "The VICTORY commissioner at LILYCOVE's harbor hands out a LIBERTY PASS. Win five in a row. Rumour says it also "
     "hangs around ROUTE 130 when the island shows."),
    ('VOLCANION', None,
     "The volcano on STEAM ISLAND, off ROUTE 131, has a pressure problem. The pressure problem has legs."),
    ('ZARUDE', None,
     "FORTREE JUNGLE, the clearing in the southwest. A monkey with a vine and a grudge."),
    ('OKIDOGI', None,
     "GRANITE CAVE: a very muscular dog sits on a stolen mask. Persuade it."),
    ('MUNKIDORI', None,
     "FIERY PATH, EMBER HOLLOW: a monkey with a stolen mask and too much attitude."),
    ('FEZANDIPITI', None,
     "Under ROUTE 127 there's a grotto with a bird that thinks it's gorgeous. It's holding a stolen mask."),
    ('OGERPON', None,
     "FORTREE JUNGLE has a mask festival with three empty hooks. Bring back the masks the LOYAL THREE stole."),
    ('TAPU_KOKO', None,
     "TAPU ISLE, north of ROUTE 132. Four guardians wake one after another. The yellow one always goes first. "
     "It insists."),
    ('TAPU_LELE', None,
     "TAPU ISLE, north of ROUTE 132. The pink guardian wakes when the yellow one is done with you."),
    ('TAPU_BULU', None,
     "TAPU ISLE, north of ROUTE 132. The red guardian is not a morning POKéMON. It wakes third."),
    ('TAPU_FINI', None,
     "TAPU ISLE, north of ROUTE 132. The last guardian sits by the water and has been waiting. Unsettlingly."),
    ('WO_CHIEN', 'FLAG_HIDE_RUIN_WO_CHIEN',
     "PETALBURG WOODS hides a sealed shrine. The snail inside is not grateful for visitors."),
    ('CHIEN_PAO', 'FLAG_HIDE_RUIN_CHIEN_PAO',
     "ROUTE 135 has a sealed shrine in the snow. The cat inside has swords for teeth."),
    ('TING_LU', 'FLAG_HIDE_RUIN_TING_LU',
     "Under the desert, in the DESERT UNDERPASS, a shrine holds a moose made of grudges."),
    ('CHI_YU', 'FLAG_HIDE_RUIN_CHI_YU',
     "Visit all four ruin shrines and the seal in JAGGED PASS breaks. The fish inside is on fire. Emotionally too."),
    ('RESHIRAM', 'FLAG_HIDE_TAO_RESHIRAM',
     "TAO ISLAND, the tower roof. Two brothers sleep on opposite sides because they can't share a room. The white "
     "one snores fire."),
    ('ZEKROM', 'FLAG_HIDE_TAO_ZEKROM',
     "TAO ISLAND, the tower roof. The black brother sleeps on the other side. He snores in thunder."),
    ('KYUREM', 'FLAG_HIDE_TAO_KYUREM',
     "Under the DRAGON'S DEN on TAO ISLAND lies FROST HOLLOW. GHETSIS is guarding it like it's his. It isn't."),
    ('ZACIAN', 'FLAG_HIDE_MEGA_FOREST_ZACIAN',
     "The MINI FOREST on ROUTE 102 has a rusty sword and a lot of snoring. The snoring lives in the forest behind it."),
    ('ZAMAZENTA', 'FLAG_HIDE_MEGA_FOREST_ZAMAZENTA',
     "The MINI FOREST on ROUTE 102 has a rusty shield and a second snore, in harmony."),
    ('GIRATINA', None,
     "SKY PILLAR has a basement that goes the wrong way. Follow it down. The bottom is the top, down there."),
    # --- Spacetime Cave
    ('MEWTWO', 'FLAG_SPACETIME_CERULEAN_DONE',
     "SPACETIME CAVE, the CERULEAN CAVE rift. TEAM ROCKET wants what sleeps at the bottom. Get there first."),
    ('ZERAORA', 'FLAG_HIDE_CHARGESTONE_ZERAORA',
     "SPACETIME CAVE, the CHARGESTONE CAVE rift. Something is eating the electricity, and COLRESS is taking notes."),
    ('CELEBI', None,
     "SPACETIME CAVE, NATIONAL PARK. The woods behind it are ILEX FOREST, and its shrine answers to the time-lost."),
    ('ETERNATUS', 'FLAG_NATIONAL_PARK_DONE',
     "SPACETIME CAVE, NATIONAL PARK. In another dimension it's on fire. Help it stop."),
    ('XERNEAS', None,
     "SPACETIME CAVE, GLIMWOOD TANGLE. The light is dying. Find the stag that turns it back on."),
    ('YVELTAL', None,
     "GLIMWOOD TANGLE again, after XERNEAS. Life got all the attention. Death is waiting its turn."),
    ('UXIE', 'FLAG_HIDE_LAKE_ACUITY_UXIE',
     "SPACETIME CAVE, the lakes. LAKE ACUITY: surf to the cave in the middle and try not to forget why."),
    ('MESPRIT', 'FLAG_HIDE_LAKE_VERITY_MESPRIT',
     "SPACETIME CAVE, the lakes. LAKE VERITY: surf to the cave in the middle. Bring feelings."),
    ('AZELF', 'FLAG_HIDE_LAKE_VALOR_AZELF',
     "SPACETIME CAVE, the lakes. LAKE VALOR: surf to the cave in the middle. Bring courage, or at least snacks."),
    ('KORAIDON', None,
     "AREA ZERO, the past. Something at the bottom is very proud of its tail."),
    ('MIRAIDON', None,
     "AREA ZERO, the future. Something at the bottom has wheels where its manners should be."),
    ('TERAPAGOS', None,
     "AREA ZERO: shut down both security systems and the TERA CAVE opens. Something shiny is locked in."),
    ('PECHARUNT', None,
     "YOSHI'S ISLAND, the hills. A tiny stall sells mochi. Don't eat the mochi."),
    ('DIALGA', 'FLAG_CORONET_DIALGA_DONE',
     "SPEAR PILLAR, the diamond altar. Time is waiting, impatiently."),
    ('PALKIA', 'FLAG_CORONET_PALKIA_DONE',
     "SPEAR PILLAR, the pearl altar. Space is waiting, in all directions."),
]
EXCLUDE = {'ARCEUS'}   # de eindbaas zelf


def species_info():
    """SPECIES_X -> (natdex, legendary?, mythical?, paradox?, base-naam)."""
    info, macros = {}, {}
    files = sorted(glob.glob('src/data/pokemon/species_info/gen_*_families.h'))
    for f in files:
        t = open(f).read()
        for m in re.finditer(r'#define (\w+_SPECIES_INFO)\(.*?\n((?:.*\\\n)*.*)', t):
            macros[m.group(1)] = m.group(2)
    for f in files:
        t = open(f).read()
        parts = re.split(r'\n    \[(SPECIES_\w+)\]\s*=', t)
        for i in range(1, len(parts), 2):
            sp, body = parts[i], parts[i + 1]
            body = body[:body.find('\n    [')] if '\n    [' in body else body
            mm = re.match(r'\s*(\w+_SPECIES_INFO)\(', body)
            full = body + (macros.get(mm.group(1), '') if mm else '')
            nd = re.search(r'\.natDexNum\s*=\s*NATIONAL_DEX_(\w+)', full)
            if not nd:
                continue
            flag = lambda k: bool(re.search(k + r'\s*=\s*TRUE', full))  # noqa: E731
            info[sp] = (nd.group(1), flag('isLegendary'), flag('isMythical'), flag('isParadox'))
    alias = {}
    for m in re.finditer(r'#define (SPECIES_\w+)\s+(SPECIES_\w+)', open('include/constants/species.h').read()):
        alias[m.group(1)] = m.group(2)
    return info, alias


def resolve(sp, alias):
    seen = 0
    while sp in alias and seen < 5:
        sp, seen = alias[sp], seen + 1
    return sp


def scan():
    """natdex-naam -> [bron, ...] voor alle verkrijgbare legendaries/mythicals (geen paradoxen)."""
    info, alias = species_info()
    found = {}

    def add(sp, src):
        sp = resolve(sp, alias)
        if sp not in info:
            return
        nd, leg, myth, para = info[sp]
        if not (leg or myth) or (para and not leg) or nd in EXCLUDE:
            return
        found.setdefault(nd, []).append(src)

    cmd = re.compile(r'^\s*(setwildbattle|seteventmon|givemon|giveegg|setdoublewildbattle)\s+(SPECIES_\w+)')
    gift = re.compile(r'^\s*setvar VAR_0x8004, (SPECIES_\w+)')
    for f in sorted(glob.glob('data/maps/*/scripts.inc') + glob.glob('data/scripts/*.inc')):
        if f.endswith('debug.inc'):
            continue
        L = open(f, errors='ignore').read().split('\n')
        where = f.split('/')[-2] if '/maps/' in f else os.path.basename(f)
        for i, line in enumerate(L):
            m = cmd.match(line)
            if m:
                add(m.group(2), where)
            m = gift.match(line)
            if m and any('GiveGiftMon' in k for k in L[i + 1:i + 6]):
                add(m.group(1), where)
    wj = json.load(open('src/data/wild_encounters.json'))
    for grp in wj['wild_encounter_groups']:
        for e in grp['encounters']:
            for k, v in e.items():
                if isinstance(v, dict) and 'mons' in v:
                    for mon in v['mons']:
                        add(mon['species'], 'wild:%s' % e.get('map', '?'))
    for m in re.finditer(r'TryAddRoamer\((SPECIES_\w+)', open('src/roamer.c').read()):
        add(m.group(1), 'roamer')
    return found, info, alias


def generic_hint(srcs):
    maps = sorted({s for s in srcs if not s.startswith(('wild:', 'roamer'))})
    where = maps[0] if maps else srcs[0].replace('wild:MAP_', '')
    where = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', where.replace('_', ' ')).upper()
    return "Something old stirs near %s. The flute is vague about it. So is everyone." % where


def c_string(s):
    parts = dimp.to_strings(s)
    parts[-1] = parts[-1].rstrip('$')
    return ''.join(parts)


def write_header(entries):
    out = ['// Project Grounded: gegenereerd door tools/grounded/azure_flute.py; niet met de hand bewerken.',
           '// Hints van de Azure Flute: {soort, gone-flag (0 = geen), tekst}. Volgorde = volgorde van de hints.',
           '// %d soorten.' % len(entries),
           'static const struct AzureFluteHint sAzureFluteHints[] =', '{']
    for sp, gone, text, srcs in entries:
        out.append('    // %s: %s' % (sp, ', '.join(sorted(set(srcs)))))
        out.append('    {SPECIES_%s, %s, COMPOUND_STRING("%s")},' % (sp, gone or '0', c_string(text)))
    out.append('};')
    open('src/data/azure_flute_hints.h', 'w').write('\n'.join(out) + '\n')


# ---------------------------------------------------------------- icoon (24x24, eigen tekening)
PAL = [(180, 180, 180), (24, 36, 74), (41, 90, 164), (74, 148, 222), (139, 205, 246), (230, 246, 255),
       (156, 115, 24), (238, 197, 74), (16, 16, 41), (255, 255, 255)] + [(0, 0, 0)] * 6


def draw_icon():
    from PIL import Image
    import math
    W = 24
    px = [[0] * W for _ in range(W)]
    ax, ay, bx, by = 3.5, 19.5, 19.5, 4.5           # schuine dwarsfluit, linksonder -> rechtsboven
    L = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / L, (by - ay) / L
    nx, ny = uy, -ux                                  # normaal (wijst naar linksboven)
    for y in range(W):
        for x in range(W):
            cx, cy = x + 0.5 - ax, y + 0.5 - ay
            t = cx * ux + cy * uy
            d = cx * nx + cy * ny
            if t < -1.2 or t > L + 1.2:
                continue
            r = 2.0 if 0 <= t <= L else 2.0 - (abs(t - (L if t > L else 0)))
            if abs(d) <= r + 1.0:
                px[y][x] = 1
            if abs(d) <= r:
                f = t / L
                if 0.06 < f < 0.13 or 0.87 < f < 0.94 or 0.47 < f < 0.52:
                    px[y][x] = 7 if d > 0 else 6           # gouden ringen
                else:
                    px[y][x] = 4 if d > 0.9 else (3 if d > -0.6 else 2)
                if 0.15 < f < 0.85 and d > 1.2:
                    px[y][x] = 5                          # glans
    for f in (0.24, 0.33, 0.42, 0.62, 0.72):              # vingergaten op de middellijn
        x, y = ax + ux * f * L, ay + uy * f * L
        px[int(y)][int(x)] = 8
    body = [row[:] for row in px]
    for y in range(W):                                    # omlijning rondom
        for x in range(W):
            if body[y][x] == 0 and any(0 <= x + a < W and 0 <= y + b < W and body[y + b][x + a] >= 2
                                       for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[y][x] = 1
    for (x, y) in ((20, 1), (21, 2), (19, 2), (20, 3), (22, 7), (3, 12)):   # sterretjes
        if px[y][x] == 0:
            px[y][x] = 9
    im = Image.new('P', (W, W))
    flat = []
    for c in PAL:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.putdata([v for row in px for v in row])
    im.save('graphics/items/icons/azure_flute.png')
    with open('graphics/items/icon_palettes/azure_flute.pal', 'w') as f:
        f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in PAL))


def main():
    found, info, alias = scan()
    hinted = {k for k, *_ in HINTS}
    entries = []
    for key, gone, text in HINTS:
        if key not in found:
            print('let op: hint voor %s, maar die is (nog) niet te krijgen; valt weg' % key)
            continue
        entries.append((key, gone, text, found[key]))
    for key in sorted(found):
        if key not in hinted:
            print('let op: %s is te krijgen (%s) maar heeft geen hint; algemene hint gebruikt' %
                  (key, ', '.join(found[key])))
            entries.append((key, None, generic_hint(found[key]), found[key]))
    # elke gone-flag moet bestaan
    flags = open('include/constants/flags.h').read()
    for key, gone, *_ in entries:
        assert gone is None or re.search(r'#define %s\b' % gone, flags), ('onbekende flag', key, gone)
    # elke soort moet een SPECIES_-constante zijn
    sp = open('include/constants/species.h').read()
    for key, *_ in entries:
        assert re.search(r'#define SPECIES_%s\b' % key, sp), ('onbekende soort', key)
    write_header(entries)
    draw_icon()
    print('%d legendaries/mythicals in de hintlijst' % len(entries))
    if '--list' in sys.argv:
        for key, gone, text, srcs in entries:
            print('  %-12s %-34s %s' % (key, gone or '-', ', '.join(sorted(set(srcs)))))


if __name__ == '__main__':
    main()
