> Status (9 okt, tweede meting): gegenereerd met `tools/grounded/dex_check.py` (herbruikbaar; na `make` draaien, `--md` print de lijsten, `--waarom SPECIES_X` toont de bronnen). Machineleesbaar: `tools/grounded/dex_beschikbaar.json`. De analyse van 6 okt (zee, types, weglaatkandidaten) staat in de git-geschiedenis van dit bestand.

# DEX_ANALYSE: wat is er zonder ruilen te krijgen

Telling over alle 1025 soorten + 57 regionale vormen (wat in `species_enabled.h` aan staat; Mega/Gmax/Primal/Ultra Burst/Tera/Totem en vormen die alleen in gevechten bestaan tellen niet):

| | aantal |
|---|---|
| te krijgen | **1050** |
| niet te krijgen | **0** |
| alleen via ruilen | 0 (alle ruil-evoluties hebben in deze rom een item-alternatief) |
| in de maak (andere agents) | 26 |
| bewust weggelaten (elemental monkeys) | 6 |

Eerste gevonden bron: wild 861, evolutie 90, statisch/legendary-script 80, fokken 14, gift 4. Alleen via fokken (de rest van hun lijn is wel wild/te krijgen): Pidgey, Nidoran♂, Bellsprout, Ponyta (Galar), Sentret, Natu, Snubbull, Azurill, Shinx, Mime Jr., Shelmet, Yungoos, Wooloo, Flittle.

Methode (kort): wilde tabellen (land/surf/vissen/Rock Smash), `setwildbattle`/`seteventmon`/legendary-specials (`setvar VAR_0x8004`), `givemon`/`giveegg`/keuzegifts, roamers; daarna evoluties (items moeten ergens liggen: kaarten, scripts, winkels, Floating Market, Fishing Tournament, Frontier-ruil, Pickup), fokken (Daycare-baby, geen Undiscovered, genderloos/alleen-mannelijk via Ditto, incense-baby's alleen met incense), vormwissels buiten gevechten en fusies (DNA Splicers e.d.). Aanname: tijd/plek/move-voorwaarden van evoluties zijn haalbaar.

## In de maak (andere agents, 9 okt)

- **Gen 1:** Articuno, Zapdos, Moltres en hun Galar-vormen `legendary`
- **Gen 5:** Meloetta `mythical`
- **Gen 6:** Zygarde (incl. 10%/Complete) `legendary`, Diancie `mythical`
- **Gen 7:** Cosmog, Cosmoem, Solgaleo, Lunala, Necrozma (incl. Dusk Mane/Dawn Wings) `legendary`, Marshadow `mythical`; Ultra Beasts: Nihilego, Buzzwole, Pheromosa, Xurkitree, Celesteela, Kartana, Guzzlord, Poipole, Naganadel, Stakataka, Blacephalon

Geen enkele legendary/mythical buiten deze lijst ontbreekt nog.

## Gerepareerd in deze ronde

- **Indeedee ♀** (aparte vorm; fokken met Ditto geeft altijd ♂): Route 123, slot 9 (4%, lv 50–53), in plaats van Medicham (zat in 10 andere tabellen).
- **Rockruff (Own Tempo) → Lycanroc (Dusk):** Route 112, Own Tempo op het 4%-slot van Rockruff; Rockruff schuift naar het 5%-slot van Torkoal (zat in 13 andere tabellen).
- **Vormwissel-items die nergens lagen** (`nieuwe_items.py`, FLAG_GROUNDED 1580–1583): Rotom Catalog (kelder van Rotom in Mauville, `MauvilleCity_House2_B1F`), Reveal Glass (Weather Institute 2F: Therian-vormen van de Forces en Enamorus), Pink en Purple Nectar (Pretty Petal-bloemenwinkel, Route 104: Oricorio Pa'u/Sensu).
- **Silvally-Memories:** de 14 die nergens lagen (alle behalve Ice/Ghost/Water, die al in de Crown Tundra en het Abandoned Ship liggen) krijg je na Type: Null van de Devon-wetenschapper (2F), in één keer naar de pc (scheelt 14 tasvakjes; FLAG_GROUNDED 1584).
- Caterpie en (Kanto-)Rattata zaten al early game: Rattata Route 101/104, Caterpie Route 104/Petalburg Woods. Alola-Rattata/-Meowth blijven gifts (Paradiso Resort).

## Vormen zonder route (cosmetisch/kleur/event, Jordi beslist)

Niet meegeteld in de 1050; alleen ter info (117 vormen): Pikachu-petjes/cosplay (15), Starter-Pikachu/-Eevee, Spiky-eared Pichu, Deerling/Sawsbuck-seizoenen (6), Scatterbug/Spewpa/Vivillon-patronen (3×19; fokken geeft altijd de ene vaste vorm), Flabébé/Floette/Florges-kleuren (13, incl. Eternal Floette), Furfrou-trims (9), Pumpkaboo/Gourgeist-maten (6), Squawkabilly-kleuren (3), Sinistea/Polteageist Antique, Poltchageist Artisan/Sinistcha Masterpiece, Original Color Magearna, Dada Zarude. Goedkope oplossingen als Jordi ze wil: kleuren/maten als extra wilde slots, Furfrou-trims/seizoenen via een NPC-vormwissel.
