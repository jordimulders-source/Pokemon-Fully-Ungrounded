# Project Grounded – werkafspraken voor Claude

Pokémon Emerald-romhack op basis van pokeemerald-expansion. De eigenaar (Jordi) communiceert in het Nederlands; antwoord en schrijf de changelog in het Nederlands.

## Vaste regels
- **Changelog:** zet elke wijziging onderaan in `CHANGELOG.md`, als een nieuwe `### [v.x.y.z] - ...`-sectie. Dit is Jordi's eigen logboek; het mag "vervuild" zijn (codeblokken, learnsets). Niet opschonen of herstructureren.
- **Debugmenu blijft aan** (`DEBUG_OVERWORLD_MENU` en `DEBUG_BATTLE_MENU` in `include/config/debug.h`).
- **Mail en Magikarp-levels** niet aanpassen.
- **Grap-trainers blijven een grap:** extreem lage levels op sterke Pokémon zijn bewust (bijv. Ivan's Gyarados lv 3, Lyle's Scizor/Yanmega lv 6). Ze moeten schrikken, niet onverslaanbaar zijn.
- **Humor:** dialogen zijn bewust absurd en donker-humoristisch. Niet "netjes maken"; wel tekstregels afbreken zodat ze passen (`\n`, `\l`, `\p`).
- **Intro kort houden:** geen truck-intro, geen tv-scène. Mom houdt haar humoristische standaardtekst; healen, PokéNav-registratie en post-game-dialoog werken wel.
- **Elemental monkeys** (Pansage/Pansear/Panpour-lijnen) zijn bewust weggelaten.
- **National Dex** is vanaf het begin beschikbaar.

## Speelervaring
- Filosofie à la Shin Megami Tensei / Slay the Spire: gevechten mogen pittig zijn, maar de speler krijgt veel tools en mogelijkheden om ze op te lossen.
- Move-aanpassingen gebeuren per move; er is geen algemene regel (zoals "altijd 100% bijeffect").

## Samenwerken
- Merk je een nieuw designprincipe op, stel het eerst aan Jordi voor en voeg het pas na bevestiging toe aan dit bestand.

## Quality of life
- **De game respecteert de tijd van de speler.** Pokémon is een JRPG vol herhaling; schrap die herhaling zodat speed-up-knoppen niet nodig zijn. Animaties (aanvallen, schermtransities) zijn tof en blijven; wachttijden, overbodige teksten, ja/nee-vragen en minigames gaan eruit.
- Al gedaan: korte intro, geen tutorial, instant heal bij de verpleegster, vissen zonder minigame (Old Rod blijft bewust slecht), tekstsnelheid standaard Fast, B zet de cursor op Run, korter flitsen vóór transities, Itemfinder als ORAS-dowsing, sneller fietsen/surfen, geen vluchtende Safari-/rondzwervende Pokémon, Wailmer Pail toont rijpe bessen, Repel "Use another?", EV/IV in het summary-scherm, kaartnaam-popup niet herhalen, itembeschrijving bij eerste keer oppakken, Fly vanuit de Town Map/PokéNav-kaart na de 6e badge.
- Bewust níet: Exp. Share als Key Item, pc in het menu, type-effectiviteit altijd tonen, zwakke encounters ontlopen (zwakkere routes afzoeken kan een bewuste keuze zijn), uitleg van de laatst-gebruikte-bal-knop, een echte levelcap.
- Goedgekeurd, nog te doen: HM-moves zonder HM in je team (met een dialoog die de speler sowieso tegenkomt en het uitlegt), Move Deleter bij de Move Relearner, Rare Candy/vitamines in één keer meerdere gebruiken, kortere berichten na het vangen (bijnaam alleen op verzoek, volle party direct naar de pc), tas sorteren, twee registratieknoppen, nature/ability zichtbaar in de pc, hele team in één keer healen met een item, aanwijzing van het level van de volgende gym-ace, rematch-overzicht in de PokéNav, moves én ability zien van wilde Pokémon die je al gevangen hebt, nieuw gevangen Pokémon automatisch op een vrije plek in de pc, hengel en fiets zonder menu, bessen planten in één handeling, korte melding bij items oppakken (zonder tekstvak), gevechtsmenu onthoudt de laatst gekozen move.
- Gedaan (events): Wally-gevecht in Meteor Falls en tag battle met Wally tegen Maxie + Tabitha op Mt. Chimney, Prof. Birch op het strand van Route 109, gevechtsmuziek kiezen in het optiemenu. Belangrijke gevechten (rivalen, gymleiders, Archie, Maxie, Wally, Birch) krijgen de mugshot-slide (`Mugshot:` in `trainers.party`).
- Testen in de emulator kan headless: `pip install mgba` (libmgba staat al op het systeem) en screenshots maken met de Python-bindings; het debugmenu zit in het startmenu (DEBUG → Scripts voor tijdelijke testscripts, niet committen).
- Later proberen: kortere pauzes tussen gevechtsberichten (`B_WAIT_TIME_MULTIPLIER` 10 → 8) en snellere schermtransities.

## Wilde encounters (`src/data/wild_encounters.json`)
- Land heeft precies **12 slots** met kansen 20/20/10/10/10/10/5/5/4/4/1/1. Meer of minder entries = bug (extra entries komen nooit voor).
- **Design-filosofie:** elke tabel heeft **12 unieke soorten**, geen soort in twee slots. De 1%-slots zijn dus echte zeldzaamheden.
- In oudere tabellen die nog dubbele soorten hebben: vervang bij voorkeur zo'n dubbel slot, zodat er geen soort verdwijnt.
- Elke entry heeft `min_level` én `max_level` (ontbrekende `max_level` gaf eerder lv 100-encounters).
- Schuif je slots door, behoud dan de zeldzaamheidsvolgorde (wie het zeldzaamst was, blijft dat).
- Houd rekening met evolutielevels (bijv. Deino evolueert op 32, Zweilous op 53).

## Pokémon-revisies
- Types, stats, abilities en learnsets van veel soorten zijn aangepast; dat staat per soort in `CHANGELOG.md` ("Pokémon Revisie: ..."). De code in `src/data/pokemon/species_info/` moet overeenkomen met de changelog. Controleer dat bij twijfel (Swellow had Wind Rider in de changelog maar niet in de code).
- Level-up learnsets staan in `src/data/pokemon/level_up_learnsets/gen_9.h` (actief via `P_LVL_UP_LEARNSETS` = GEN_LATEST). Wijzigingen in `gen_1.h` t/m `gen_8.h` hebben geen effect.
- Een `Ability:` in `src/data/trainers.party` moet in de abilitylijst van die soort staan.

## Trainer parties (`src/data/trainers.party`)
- **Taakverdeling:** Jordi doet de humor (grap-teams, grappige dialogen); Claude doet het serieuze werk. Verzin zelf geen grappen, maar laat Jordi's grappen staan.
- **Elk gevecht moet engaging zijn**, serieus óf als grap. De speler mag niet op de automatische piloot raken zoals in de echte games. Placeholders moeten ook al vermakelijk zijn; na de beta wordt alles echt uniek gemaakt.
- **Levels:** gelijk aan Jordi's eigen trainers op dezelfde route (meestal 5–6 boven vanilla). Binnen een team vlakke levels, de ace eventueel 1–2 hoger.
- **Evoluties:** een Pokémon op een level waarop hij al geëvolueerd had kunnen zijn, is geëvolueerd. Gebruik de evolutielevels van dit project (`src/data/pokemon/species_info/`), die wijken soms af van de officiële games. Uitzondering: een bewuste grap van Jordi.
- **Variatie:** soorten die al vaak voorkomen (bijv. Wingull, Marill, Tentacool, Machop, Meditite, Makuhita) vervangen door soorten die nog weinig of niet voorkomen.
- **Thema:** grounded per trainerklasse, maar het mag out of the box (bijv. een Tuber met een niet-water-Pokémon).
- Teams die Jordi al niet-Emerald Pokémon heeft gegeven, laten staan, tenzij de levels echt te laag zijn.
- **Rematches:** team van de eerste versie behouden; per rematchronde +1 Pokémon (max 6) en evoluties passend bij het level. Level = vanilla-rematchlevel + dezelfde marge als de eerste versie (4–8); gymleiders +12. Door Jordi zelf ontworpen rematches (Calvin, Gabby & Ty, Miguel, Isaiah_2, Amy & Liv_2, Kira & Dan_2–5) blijven staan.

## Moves (`src/data/moves_info.h`)
- Stat-drops op de tegenstander: gebruik losse effecten per stat (`MOVE_EFFECT_DEF_MINUS_1`, `MOVE_EFFECT_SP_DEF_MINUS_1`, ...). Gecombineerde effecten zoals `MOVE_EFFECT_DEF_SPDEF_DOWN` (Close Combat) en `MOVE_EFFECT_ATK_DEF_DOWN` (Superpower) werken altijd op de gebruiker.
- `additionalEffects` worden alleen uitgevoerd bij aanvallende moves (en bij `onChargeTurnOnly` op de laadbeurt van two-turn moves), niet bij statusmoves zoals Flash.
- Eigen tests staan in `test/battle/grounded/`.

## Bouwen en testen
- Bouwen: `make -j4` (moet zonder fouten slagen vóór elke push).
- `make check` (CI-job `build`) faalt ook op `master`, met honderd-en-zoveel tests die de bewust gewijzigde mechanics en soorten niet meer verwachten. Nieuwe failures ten opzichte van master zijn wel een probleem.
- Werk op een branch en open een PR naar `master`.
- Meld de bekende, al bestaande `make check`-failures niet aan Jordi; alleen nieuwe failures die door een wijziging komen zijn het vermelden waard.

## Dialogen (Dialoogstudio)
- Jordi schrijft dialogen in de Dialoogstudio: https://claude.ai/artifact/LP3qyGyvhaj6p5GS32Gjxz (bewerkingen staan in de database van die pagina: collectie `edits`, per tekstlabel `{text, note, status, map}`; wensen per kaart in `verzoeken`).
- "Verwerk de dialogen": lees `edits` met status `klaar` (ArtifactData), schrijf `{label: text}` naar een JSON-bestand en draai `python3 tools/dialogen/import.py <bestand>`. Dat breekt de tekst automatisch af (zelfde regels als het voorbeeld in de editor). Bouw, controleer, commit, zet de verwerkte documenten op status `verwerkt` en voer de notities/wensen uit.
- **Niet vóór de beta:** dialogen in het Trick House (`Route110_TrickHouse*`), de Battle Frontier (`BattleFrontier_*`) en de Battle Tents (`*_BattleTent*`) blijven bewust vanilla tot na de beta. Niet aanpassen, tenzij Jordi erom vraagt. De Dialoogstudio verbergt deze gebieden standaard.
- Na wijzigingen in de scripts: `python3 tools/dialogen/export.py <dialogen.json>` en publiceer dat bestand opnieuw bij de pagina, zodat de editor de actuele game-tekst toont.
- Nieuwe NPC-teksten die Claude toevoegt zijn neutrale placeholders, totdat Jordi ze zelf schrijft.

## Sessies en overdracht
- Elke sessie begint vers; dit bestand is het geheugen. Werk de sectie **Stand van zaken** hieronder bij aan het eind van elk afgerond stuk werk (in dezelfde commit), zodat een nieuwe sessie direct verder kan.
- Branch: `claude/hopeful-brahmagupta-hsth8c` (PR 5 naar `master`). Is die PR gemerged, begin dan een nieuwe branch vanaf `master`.
- Commit en push na elk afgerond stuk, met een changelogsectie.

## Kaarten maken
- Jordi wil van **elke kaart die af is** screenshots (een render van de hele kaart en een paar emulatorbeelden), zodat hij kan tweaken.
- Gereedschap en testrecept staan in `tools/grounded/maptools/README.md` (renderen, `snowlib.py` voor sneeuwkaarten, ijspuzzel-zoeker, headless emulator).
- Routegrootte: ongeveer gemiddeld of net onder gemiddeld (landroutes zijn meestal 2400–3200 tiles, bijv. 40×80 of 60×40).
- Randen van routes: de vaste Hoenn-randbomen (op sneeuwkaarten de besneeuwde versie `htree_*`), ook als `border.bin`. Geen losse bomen die elkaar overlappen.
- Watervallen zoals bij Ever Grande/Meteor Falls: breed, in een massieve rotswand (`fall()` en `terrace(face=...)` in `snowlib.py`).
- Sneeuwtileset (`tools/grounded/snow_tileset.py`): nieuwe metatiles **alleen achteraan** toevoegen (anders verschuiven alle nummers). Na genereren eerst `make data/tilesets/secondary/snow/tiles.4bpp`. Tile-budget max. 512 (nu ~431).
- Valkuilen: savestates zijn ongeldig na een rebuild; `data/scripts/debug.inc` nooit committen; `wild_encounters.json` en andere grote JSON-bestanden tekstueel bewerken (niet via `json.dump`, dat herformatteert het hele bestand); trainer-AI in `trainers.party` met bestaande namen (bijv. `Check Bad Move / Try To Faint`).

## Stand van zaken
- **Af:** Coldstep Cave (Route 115 → tunnel → ijskamer 1 → ijskamer 2, puzzel van 28 zetten, oplosbaar voor elke combinatie van opgepakte items), Keccles 1 en 2, Seltzer Surge (TM51), muziekcredits.
- **Route 135** (60×40, sneeuw, bouwscript `tools/grounded/maptools/route135.py`): terrassen, brede waterval met Life Orb erboven, meer met oevers, besneeuwde Hoenn-randbomen, huisje rechtsboven (`Route135_House`, nog leeg), hikers Edmund & Tenzing (dubbel), Birch-gevecht 2 (Macarena). Wacht op Jordi's reactie op randbomen en huisje.
  - Ook: Swimmer Bram (Wim Hof, Water/IJs-team) in de inham onder het meer, Lapras-static midden in het meer, oud stel zonder elektronica in het huisje.
  - Nog van Jordi: definitieve teksten van Birch 2, Edmund, Tenzing, Bram en het oude stel (nu placeholders).
  - Route 136 sluit aan op de zuidoostelijke uitgang (x 50–53, onderrand, connectie `down`).
  - `MAPSEC_ROUTE_135` valt op de Town Map nog onder Route 115 (alias in `src/region_map.c`).

## Openstaande taken (in volgorde)
1. **Route 136** (sneeuw, klimt verder de bergen in; hoog maar niet hoger dan Mt. Chimney): bomengang met een item, geblokkeerd door een onzichtbare Keccles (Devon Scope, zoals bij Fortree); rivaalgevecht May/Brendan; een Bird Keeper; een zwemmer aan de waterkant ("Wim Hof"-idee van Jordi); dynamisch weer met sneeuw en as afwisselend (ook voor Route 135).
2. **Ashfrost Town:** paradijselijk dal met een meertje in het midden, een man die daar vist, huizen eromheen (sommige op verhoging), Pokémon Center, Mart en een paar huizen. De sneeuwpop hoort hier. Gebouwen staan in de bronsheet `graphics/grounded/snow_src` (rijen 104–134); waarschijnlijk is een eigen stads-tileset nodig vanwege het tile-budget.
3. **Town Map:** Route 135/136 en Ashfrost toevoegen (lege hooglanden rond mapsec x3–4, y1–4; regionmap-coördinaat = tile − (1,2)).
4. **Bier- en wijnversie van Surf/Muddy Water** met hoge kans op confusion (idee van Jordi; details nog afstemmen, zie Seltzer Surge als voorbeeld).
5. **Ditto-trainer** (Pokopia-idee), **gepauzeerd** door Jordi. Besproken opties: vermomde trainer met onthulling, team van Imposter-Ditto's met verschillende items, of een trainer die jouw team kopieert. Plek: Route 115 (hengeltabel vol Ditto) of Ashfrost.
