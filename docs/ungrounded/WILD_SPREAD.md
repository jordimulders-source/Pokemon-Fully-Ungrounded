# Verspreiding wilde Pokémon (9 okt)

Meten: `python3 tools/grounded/wild_spread.py` (rapport), `--alles` (alle soorten), `--soort SPECIES_X` (waar komt hij voor).
Telt per soort het aantal **unieke** tabellen (identieke verdiepingen tellen één keer), het gewicht (som van de kans per
ontmoeting; vissen per hengel genormaliseerd) en de fase (vroeg ≤ lv 30, midden 31–55, laat 56–80, post-game > 80), plus
hetzelfde per evolutielijn. `ALLEDAAGS` in het script = soorten die logisch overal zitten (Magikarp, Zubat, Tentacool, …).

## Gewijzigd (50 slots)

**Legendaries/mythicals uit gewone tabellen** (alle vier nog te krijgen via hun event, `dex_check.py`):
| Tabel | Weg | Nieuw | Eigen event |
|---|---|---|---|
| Mt. Pyre Summit land (1%) | Jirachi | Gardevoir 58 | Fallarbor |
| Route 130 land (1%) | Victini | Florges 73 | Liberty Garden |
| Route 131 Super Rod (1%) | Manaphy | Gyarados 71–73 | Zeetempel (Sanctum) + ei in Lavaridge |
| Route 115 land (1%) | Kubfu | Munchlax 56 | Dojo Route 112 |

Volcanion stond al niet meer in een tabel (Steam Island-grot). Paradoxen (Scream Tail, Iron Bundle, Roaring Moon e.d.)
blijven staan: tellen niet als legendary. Altering Cave 1 had Roaring Moon dubbel: slot 10 is nu Flutter Mane.

**Elemental monkeys** (steen ligt in hetzelfde gebied of is te koop in Lilycove):
| Soort | Tabel | Slot | Steen |
|---|---|---|---|
| Pansage 49–50 | Fortree Jungle (i.p.v. Komala) | 10% | Leaf Stone ligt in de jungle |
| Panpour 41–44 | Route 119 (i.p.v. Komala; regenroute) | 10% | Water Stone: Abandoned Ship, Lilycove |
| Pansear 25–28 | Fiery Path (i.p.v. Turtonator) | 10% | Fire Stone ligt op Fiery Path |
| Simisage 84–86 | Yoshi's Island Jungle (i.p.v. Lurantis; naast Ambipom/Passimian/Oranguru) | 10% | – |
| Simisear 82–83 | Steam Island (i.p.v. Heatmor) | 5% | – |
| Simipour 87–88 | Yoshi's Island Beach (i.p.v. Ludicolo) | 4% | – |

**Magikarp aan de Old Rod** (lv 12–19, onder zijn evolutielevel 20): Route 118, 119, 121, 125, 126, 130, 133,
Lilycove, Sootopolis, Mossdeep, Ever Grande, Pacifidlog. Magikarp stond maar in 4 tabellen; nu 16 (lijn: 36).
Vervangen: vooral Mareanie/Arrokuda/Chinchou/Shellder die in dezelfde tabel nog een tweede slot hadden, Pelipper
(vissen?) en Togepi (vissen??). `check_levels.py` meldt deze Old Rod-slots als "omlaag": bewust (plus Graveler lv 36 i.p.v. 37 in de Lava Tube, zodat hij niet al Golem had moeten zijn).

**Te vaak → minder** (niet-alledaagse soorten in veel tabellen):
- Relicanth 18 → 13 (levend fossiel): Route 107/126/128/134 en Mossdeep → Wailord, Sharpedo, Clamperl, Kingler.
- Bronzong 19 → 14: Chargestone 1F/B2F → Gigalith/Klinklang, Meteor Falls 1F_2R (gevist!) → Gyarados,
  Victory Road Waiting Room en omgekeerde Sky Pillar B1F → Crobat.
- Probopass 13 → 10: Chargestone B2F → Ferrothorn, Yoshi's Island Cave → Steelix, Sky Pillar-ingang → Crobat.
- Dhelmise 19 → 17: Route 134 Surf → Tentacruel, Mossdeep Super Rod → Wailord.
- Garchomp 9 → 7 (pseudo-legendary): Mt. Coronet 4F Room 1/2 → Steelix, Mt. Coronet buiten → Ursaring.
- Bruxish 14 → 12: Aqua Hideout 1F → Wailord (Surf) en Gyarados (vissen); Lapras 12 → 11: Route 127 Surf 60% → Tentacruel.

**Te weinig → vaker** (alledaags, maar bijna nergens):
- Zubat-lijn (Golbat 1 tabel, Crobat alleen post-game): Crobat in Seafloor Cavern 1–3 (i.p.v. Glimmet lv 60–66, dat al
  op 35 evolueert), Sky Pillar-ingang, Victory Road Waiting Room, omgekeerde Sky Pillar.
- Geodude-lijn (Geodude 1, Graveler 2): Graveler op Mt. Chimney (i.p.v. Litwick) en in de Lava Tube (i.p.v. Heatmor).
- Taillow-lijn (2): Swellow op Route 120 (i.p.v. Oricorio, dat ook op Route 124 en Hermit Crater zit, plus twee Pom-Pom-plekken).

## Bewust laten staan
- **Vroege tabellen van Jordi** (Route 101–104, 116, Petalburg Woods, Rusturf, Granite Cave): geen wijzigingen.
- **Thematische clusters:** Solrock/Lunatone (Meteor Falls), Dragonair/Kingdra/Dragalge (drakenroutes 129/131, Tao),
  Ditto (Route 115, waar je hem ook drie keer opvist, en Cerulean Cave), Clefable (maan/grotten), Carbink (kristalgrotten),
  Dusclops/Mismagius/Spiritomb (spookplekken), Gorebyss/Huntail/Clawitzer/Toxapex/Barbaracle (late zee: weinig andere
  soorten op lv 60+), Smeargle in Artisan Cave en de één-soort-tabellen van Altering Cave (vanilla-opzet).
- **Milotic** (15 tabellen, overal 1%): de "zeldzame vangst" van zoet water; bij weinig gewicht is dat te verdedigen.
- **Alledaagse lijnen die toch weinig voorkomen** (Bellsprout, Lillipup, Pidove, Seedot, Weedle, Makuhita, Sentret,
  Pidgey, Patrat, Grimer, Trubbish: 2–3 tabellen): de opzet van deze rom is veel variatie per tabel (12 unieke soorten);
  ze komen in de vroege tabellen voor en hun evoluties staan in latere. Kandidaten voor een volgende ronde.
- **Vorm/evolutie-mismatches** die de check zag maar niet de opdracht waren: o.a. Roggenrola lv 33–36 (Lava Tube),
  Flabebe lv 62 (Route 130), Glimmet lv 66 (Seafloor Cavern 4–6).

## Nog te doen (niet in deze ronde)
- NPC in het Petalburg-Pokémon Center klaagt dat de apen ontbreken (`PetalburgCity_PokemonCenter_1F_Text_ManyTypesOfPokemon`):
  die grap klopt niet meer; Jordi beslist (Dialoogstudio).
- Spire-draft en `frontier_sets.py` (`REMOVED`) sluiten de apen nog uit.
