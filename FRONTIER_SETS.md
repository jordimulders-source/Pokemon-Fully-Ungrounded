# Frontier-sets afgestemd op Project Grounded (TODO 14)

Controle en reparatie: `python3 tools/grounded/frontier_sets.py` (controle, exitcode 1 bij meldingen) en `--fix` (repareert in de bestanden). Na een revisie van soorten, learnsets of TM's opnieuw draaien.

**Gecontroleerd:** 1554 sets in `battle_frontier_mons.h` (882, Tower/Dome/Palace/Arena/Factory/Pike), `battle_tent.h` (160), beide Pyramid-wildbestanden (2×160) en `trainer_hill.h` (192; het ongebruikte JP-blok niet). Indexen en aantallen zijn gelijk gebleven.

**Legaal** = level-up (`gen_9.h`) + TM/tutor (`teachable_learnsets.h`) + egg moves, ook van voorgangers, plus `sUniversalMoves` (Return, Substitute, ...). Smeargle mag alles (Sketch).

## Resultaat (eerste run → na reparatie)
| melding | voor | na |
|---|---|---|
| move niet leerbaar | 515 | 0 |
| categorie (revisie maakte fysiek/speciaal onzinnig) | 68 | 0 |
| soort weg / item / ability / dubbel / revisie van move-type | 0 | 0 |

- 586 moves vervangen in 464 sets (341 Frontier-pool, 88 Tents, 2×44 Pyramid, 66 Trainer Hill), 227 soorten; 33× EV's en 41× nature omgedraaid (Atk ↔ SpA) waar alle hoofdaanvallen daarna van de andere categorie waren.
- Geen elemental monkeys of verwijderde soorten in de pool (de pool is Gen 1–3). Geen ongeldige items of abilityNums.
- Geen move veranderde in dit project van type of categorie; de move-revisies (Acid, Crush Claw, Slam, Flash, ...) zijn buffs en maken geen set onzinnig.

## Meest vervangen (geen TM/tutor meer in deze rom)
Aerial Ace 87 (meestal → Wing Attack/Peck/Dual Wingbeat, anders dekking van een ander type), Roar 27 (→ Toxic, Dragon Tail of Whirlwind waar leerbaar), Rock Tomb 27 (→ Rock Slide), Feint Attack 24 (→ Sucker Punch/Bite/Night Slash), Water Pulse 16 (→ Vintage Spill, het TM53-equivalent), Iron Tail 14, Spark 14, Shock Wave 11, Will-O-Wisp 11, Torment 11 (→ Taunt).

## Categorie door revisies
Volbeat (Fire/Electric, speciaal), Sableye (Rock/Ghost, fysiek), Shiftry (Grass/Ice, speciaal), Seviper, Cacturne, Parasect, Banette, Mightyena, Crawdaunt, Swellow, Aggron (SpA 40) e.a.: hun hoofdaanvallen van de verkeerde categorie zijn vervangen (bijv. Aggron_3 Surf/Thunder/Fire Blast/Blizzard → Iron Head + elementpunches, Sableye Shadow Ball → Shadow Claw, Cacturne/Parasect Giga Drain → Drain Punch, Volbeat Ice Punch → Fiery Dance).

## Handmatig (ability-revisies)
- Swellow_1/_2: Fly/Aerial Ace → **Brave Bird** (Gale Wings).
- Spinda: Psybeam → **Brick Break** (Pure Power, nu Normal/Fighting).

## Vervangregels (`--fix`)
Zelfde rol eerst: status → zelfde effect/groep (slaap, verlamming, wegblazen, schermen, ...), anders een algemeen nuttige move (Toxic, Protect, Taunt, ...); schade → gewenste categorie, zelfde type, ongeveer dezelfde kracht, geen laadbeurt; vaste-schademoves onderling (Night Shade → Seismic Toss; Psywave → Night Shade/Seismic Toss waar leerbaar, anders een Psychic-aanval zoals Laser Beam of Psybeam). Nooit gekozen: gokwerk en rommel (Rage, Mimic, Metronome, Attract, Focus Punch, ...).
