# Opdracht: kleurvarianten ("skins") voor een generatie Pokémon

Je bouwt kleurvarianten voor Pokémon Ungrounded (Emerald-romhack). De eigenaar, Jordi, keurt alles op contactvellen. Hij is kritisch en heeft een duidelijke smaak; deze brief vat zijn feedback van vier keuringsrondes samen. Lees hem helemaal.

## Hoe het werkt
- Elke Pokémon met een recept krijgt naast normaal en shiny **6 varianten**: 10% / 6% / 4% / 3% / 1,5% / 0,5% (in die volgorde in de lijst). Hoe zeldzamer, hoe opvallender.
- Varianten zijn **paletwissels**: per kleurgroep (paletindexen) een doelkleur. Geen sprite-aanpassingen tenzij echt nodig (zie `sprite_fixes.py`, en meld het).
- Recepten: zie `tools/grounded/variants/recipes.py` voor het formaat en tientallen voorbeelden (lees er een paar, bijv. `'ledyba'`, `'mareep'`, `'togepi'`, `'tauros_paldea'`, `'corsola_galar'`, `'birds_galar'`).
  - `'species': {map: {onderdeel: [indexen]}}` (map onder `graphics/pokemon/`, ook submappen zoals `'zorua/hisui'`).
  - `'variants'`: 6 dicts met `'naam'` (Nederlands, met de inspiratie erin) en per onderdeel een doelkleur `'#rrggbb'` of `('#rrggbb', {'l': ..., 'c': ..., 'h': 0})`.
    - De doelkleur geldt voor de **meest gebruikte index** van de groep; de rest houdt zijn lichtheids-/tintverschil.
    - `'l'`: schaal van de lichtheidsverschillen (1.3–1.5 bij vlakke/donkere varianten, anders lijkt het Gen 2).
    - `'h': 0`: geen tintverloop (tegen lime/oranje-drift).
    - `'soort:onderdeel'` (bijv. `'raichu/alola:body'`) geldt maar voor één map.
    - `'_base': {onderdeel: index}` in de species-dict: vaste basisindex (als de meest gebruikte index een schaduw of lijn is).
    - `'<map>:parts'` in een variant: eigen kleurgroepen voor die variant.
- Jij schrijft **alleen** in je eigen bestand `tools/grounded/variants/recipes_<jouwgen>.py`, met bovenaan `ALBINO = {'l': 1.0}` en een dict `LINES = {...}`. `recipes.py` laadt het automatisch. Lijnnamen moeten uniek zijn (gebruik bijv. de naam van de eerste soort).

## Gereedschap (draai alles vanuit de hoofdmap van de repo, met `python3`)
- `python3 tools/grounded/variants/ramps.py <map>`: per index kleur, aantal pixels, lichtheid en buren.
- `python3 tools/grounded/variants/ramps.py --grid uit.png map1 map2 ...`: indexkaarten (welk getal staat waar). **Kijk hier altijd naar** vóór je groepen kiest.
- `python3 tools/grounded/variants/variants.py`: genereert alle paletten (nodig vóór een contactvel).
- `python3 tools/grounded/variants/sheet.py uit.png map1 map2 ...`: contactvel (normaal | shiny | 6 varianten).
- `python3 tools/grounded/variants/zoom.py uit.png map:n map:3 ...`: 4x ingezoomd (n = normaal, s = shiny, 1..6 = variant), om lijnen te controleren.
- Bekijk de PNG's met je Read-tool.

## Jordi's regels (belangrijk, hier ging het telkens mis)
1. **Alles kleurt mee.** Loop per soort elke kleurgroep langs die geen zwarte omlijning is: lijf, buik, ogen, neus, snavel, tong, wangen, bladeren, bloemen, katoen, ei, hoorns, stekels, vinnen, vlammen (ook de vlamrand), rook, edelstenen. Geef elke variant er een **bewuste** kleur voor. Een variant waarin alleen het lijf verandert en de accenten hetzelfde blijven, noemt Jordi "lui".
2. **Lijnen blijven zichtbaar**, vooral bij witte/albino/lichte varianten. Controleer elke lichte en elke heel donkere variant met `zoom.py`. Valt een lijn weg, kies een donkerder doel (de basis is soms de schaduwtint) of een `'_base'`. Bij donkere varianten mag het lijf niet zo donker worden dat de zwarte omlijning erin opgaat (gebruik bijv. `{'l': 0.7}` en een iets lichtere kleur).
3. **Skins, geen tintjes.** Herkenbaar anders dan normaal én dan de shiny (kijk naar de shiny-kolom!), passend bij de soort. Nooit een variant die nauwelijks van normaal of de shiny verschilt. Binnen een lijn moeten de zes varianten duidelijk van elkaar verschillen (niet twee keer wit, niet twee keer goud). Geen vloekende kleuren tenzij het een grap is.
4. **Inspiratie per kleur.** Elke variant heeft een concrete inspiratie: echte dieren/planten/mineralen (bijv. koraalslang, Holstein-koe, lapis lazuli), cultuur en kunst (Van Gogh, Klimt, Día de los Muertos, Kinder Surprise), popcultuur en games (Ultraman/Kamen Rider, Smash Bros.-kleuren, Team Magma/Aqua, Pennywise, Twitch Plays). Jordi waardeert creatieve, passende referenties; generiek "groen/blauw/paars" vindt hij saai. Albino mag, maar niet bij elke lijn, en altijd met goede lijnen.
5. **Hele evolutielijn in één recept**, met dezelfde 6 thema's; per soort mag de uitwerking verschillen (`'soort:onderdeel'`).
6. **Moderne sprites** (Gen 8+, alleen `front.png`, ruizige schaduw, vaak geen zwarte omlijning): donkere groepen donker houden, maar lijf en accenten wél laten meekleuren; extra goed zoomen op lijnen.
7. **Overslaan en vormen (besluiten van Jordi):**
   - Overslaan: Mega, Gmax, Primal, Totem, Ultra; Minior-kernen, Flabébé/Floette/Florges-kleuren (alleen de rode basisvorm krijgt varianten), Alcremie, Pikachu-petjes, Furfrou-trims (de trims zíjn de varianten; Furfrou krijgt geen extra varianten).
   - **Arceus en Silvally** krijgen wél varianten: de typekleur hangt van het item af, het lijfdeel dat bij elk type gelijk blijft verandert per variant, met **exact dezelfde doelkleuren voor alle typemappen** (één recept met de basis + alle types), zodat de variant meegaat als het item wisselt.
   - **Vivillon**: de basisvorm krijgt zes bestaande patroonpaletten als varianten (`'vivillon:palfile': '<patroon>/normal.pal'`); de patroonvormen zelf niet.
   - **Deerling/Sawsbuck**: alleen de lentevorm krijgt varianten; de seizoensvormen krijgen de shiny van de lentevorm mét hun seizoensdelen (per index: gelijk aan de lente-normal → lente-shiny, anders de eigen seizoenskleur).
   - **Squawkabilly**: de vier verenkleden zijn vormen; geef ze samen zes extra papegaaivarianten (dezelfde doelkleuren voor alle vier, zodat elke vorm dezelfde zes skins krijgt).
   - Overige vormen met een eigen palet (regionaal, therian/origin, enz.): gewoon meenemen. Bij twijfel: noem het in je rapport.
8. Kijk of een soort een **Pokémon-revisie** heeft in `CHANGELOG.md` (grep "Pokémon Revisie: <Naam>"): het type kan anders zijn dan in de echte games. Laat je thema's daarop aansluiten.

## Werkwijze
- Werk in batches van ±8 lijnen: indexkaarten bekijken → recept schrijven → `variants.py` → contactvel → zelf kritisch keuren tegen de regels hierboven (alles meegekleurd? lijnen? verschil met shiny/normaal/elkaar?) → zoom op witte/donkere varianten → verbeteren → volgende batch.
- Maak aan het eind **keuringsvellen** van ±10 soorten per vel in je eigen scratchmap: `<jouw scratchmap>/keuring_<jouwgen>_01.png`, `_02.png`, ...
- Schrijf `tools/grounded/variants/keuring_<jouwgen>.md`: per lijn één regel in de stijl van `KEURING.md` (onderdelen die meekleuren + per percentage de inspiratie).

## Git
- Begin met `git reset --hard claude/serene-wozniak-63k7ym` (worktrees starten soms op een oude commit).
- Commit **alleen** `recipes_<jouwgen>.py`, `keuring_<jouwgen>.md` en (zelden) `sprite_fixes.py`/aangepaste sprites. **Niet** committen: `variants.pal`, `variant_palettes.h`, `CHANGELOG.md`, `CLAUDE.md`, `KEURING.md`. Niet pushen.
- Shellregels met `$VAR`, `for` of `cd` worden geweigerd: schrijf hulpscripts naar je scratchmap en draai die.
- Gebruik een eigen submap in de scratchpad (de scratchpad wordt gedeeld).

## Rapport
Eindig met: commit-hash, lijst van lijnen, overgeslagen vormen (met reden), paden van de keuringsvellen, en twijfelgevallen.
