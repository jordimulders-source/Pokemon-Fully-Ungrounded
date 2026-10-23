# Lessen: Naslag: Ungrounded-systemen die eruit zijn

Spire, Battle Stadium, Spacetime e.d.; alleen nodig als die terugkomen. Opgesplitst uit CLAUDE.md (23 okt); nieuwe lessen hier toevoegen.

- **Spire-rekenscripts:** `tools/grounded/spire/spire_pool.py` en `encounters.py` genereren `src/data/spire_pool.h`, `spire_encounters.h` en `SPIRE_BALANS.md`; na een wijziging in soorten/moves of ontmoetingen opnieuw draaien. Leerbaarheid controleren met `tools/learnset_helpers/build/all_learnables.json` (alle games), niet alleen de TM's van deze rom. `SPECIES_X`-aliassen (Shellos, Wishiwashi, Minior) staan als `#define` in `species.h`.
- **Spire testen:** `special Spire_DebugOpen` met `VAR_0x8004` (0 kamp, 1 winkel, 2 event, 3 kaart, 4 elite, 5 baas, 6 relic-beloning met VAR_0x8005 0 elite / 1 baas) in een `testrom.py`-script; zonder run maakt hij er een.
- **Battle Stadium-gevechten:** `gStadiumBattle` schakelt geld/white-out (battle_scripts_1.s via `jumpifbyte`), EXP en het singles/doubles-type van de trainer uit; het team van een tegenstander komt uit `Stadium_BuildTrainerParty` (masker uit pool.py). Party-bestanden gaan door de C-preprocessor: markeringen als `/* */`, nooit `#`.
- **Spire-rekenscripts in een worktree:** `tools/learnset_helpers/build/all_learnables.json` ontbreekt daar; kopieer het uit de hoofdcheckout. Vijandkracht per act staat vast in `klap_check` (`matchups.py`), zie SPIRE_DESIGN.md.
- **Spire-events:** alleen `tools/grounded/spire/events.py` bewerken en opnieuw draaien; het script controleert breedtes. Contactvel van alle events: `gSpecialVar_0x8005` in het geheugen zetten vóór `debug_script` (script: `setvar VAR_0x8004, 2; special Spire_DebugOpen`).
- **Sprites in de Stadium-arena:** rij 5 valt onder de bovenrand van het veld (hoofd weg); het midden ligt tussen x 8/9 en y 6/7.
- **Stadium-gevecht testen:** debugscript `givemon` ×3; `setvar VAR_0x8004, STADIUM_DOUBLES`; `special Stadium_PrepareChooseParty`; `special Stadium_StartTournament`; `special Stadium_StartMatch`; `waitstate`. Vooraf in het geheugen `gPlayerParty` (600 bytes) en `gPlayerPartyCount` wissen, `gSelectedOrderFromParty` = 1,2,3, compagnon in `sT`+5. Bij HP-hacks alleen `hp > 1` op 1 zetten (een flauwgevallen Pokémon op 1 zetten haalt hem terug).
- **Stadium-teksten:** verliesteksten breken niet vanzelf goed af; met de hand afbreken (200 px). In doubles praat vóór de eerste beurt alleen tegenstander A, tenzij `BattleScript_StadiumTrainerABSlideMsgEnd2`.
- **Nieuwe Spacetime-locatie koppelen:** in `spacetime_cave.py` de scheur op `'warp'` in `RIFT_STATE`, bestemming in `RIFTS` + de dict in de warp-lus, klaar-flag in `SIDEQUESTS`; in het locatiescript de terugwarp naar de warp-index van die scheur (zie hub-map.json). Daarna beide scripts draaien.

- **(Ungrounded, voorlopig niet van toepassing) Battle Stadium-pool (Jordi):** alleen echt iconische personages komen in de toernooipool (met hun sterkste team): iets bijzonders zoals een eigen sprite, een eigen verhaal/quest of een gevecht dat je onthoudt (bijv. Colress, Zinnia, Mimi, Keccles, Grimsby). Geen gewone NPC's of routetrainers met alleen een naam en een standaardsprite (Jordi, 6 okt: "geen nono's en NPC's").

## Dialogen (Dialoogstudio)
- Jordi schrijft dialogen in de Dialoogstudio: https://claude.ai/artifact/LP3qyGyvhaj6p5GS32Gjxz (bewerkingen staan in de database van die pagina: collectie `edits`, per tekstlabel `{text, note, status, map}`; wensen per kaart in `verzoeken`).
- "Verwerk de dialogen": lees `edits` met status `klaar` (ArtifactData), schrijf `{label: text}` naar een JSON-bestand en draai `python3 tools/dialogen/import.py <bestand>`. Dat breekt de tekst automatisch af (zelfde regels als het voorbeeld in de editor). Bouw, controleer, commit, zet de verwerkte documenten op status `verwerkt` en voer de notities/wensen uit.
- **Niet vóór de beta:** dialogen in het Trick House (`Route110_TrickHouse*`), de Battle Frontier (`BattleFrontier_*`) en de Battle Tents (`*_BattleTent*`) blijven bewust vanilla tot na de beta. Niet aanpassen, tenzij Jordi erom vraagt. De Dialoogstudio verbergt deze gebieden standaard.
- De Dialoogstudio **niet** automatisch bijwerken na scriptwijzigingen (bespaart tokens). Alleen op verzoek van Jordi: `python3 tools/dialogen/export.py <dialogen.json>` en dat bestand opnieuw publiceren bij de pagina.


