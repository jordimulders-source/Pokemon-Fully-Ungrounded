# Review: sprites maken voor Fully Ungrounded

24 okt 2026 · Jordi (ook als Claude Doc: https://claude.ai/artifact/PBr1ykGXdA4dg4qsHJriR8)

## Samenvatting

Bol- en vachtvormen lukten snel; viervoeters met ledematen liepen vast op constructie, en het proces (doorgeven via agents, te milde keuring) maakte dat erger. Stand op 24 okt, Gen 3-sprites 64×64:

| Sprite | Bouwtype | Rondes | Uitkomst |
| --- | --- | --- | --- |
| Cuyby | bol | 3 (+2 kleurstappen) | goedgekeurd |
| Cuychu (evolutie) | vachtberg | 4 (+2 checklist) | goedgekeurd |
| Nachtaap | zittende aap | 12 | goedgekeurd |
| Alpaca | langnek-viervoeter | 17 | goedgekeurd |
| Olinguito | viervoeter met klauwen en staart | ±30 + 3 herbouwen | geschrapt |
| Kolibrie | zwevende vogel | concept | wacht op keuze |

Kernconclusie: het werk zit niet in kleur of shading (dat ging vanaf ronde 6 goed), maar in de vorm. Hoe meer losse ledematen in 3/4 perspectief, hoe vaker het misging.

## Wat goed werkte

Referentiemateriaal was de grootste versneller: zodra er een foto of een echte sprite als maatstaf was, ging het binnen een paar rondes goed.

1. **Foto's van het echte dier.** Cuychu was na de langhaar-caviafoto's in 2 rondes klaar; de alpaca werd pas een alpaca na de alpacafoto ("één vachtkleur").
2. **Een echte Pokémon als specificatie.** Galar-Linoone (gezicht, poten), Sandslash (klauwen) en Poochyena (lijf) gaven de olinguito in een paar stappen een betere kop en poten.
3. **Kleur en shading.** De techniek uit de Dragonfly Cave-gids (omlijning per kleurgroep, licht linksboven, glans in de ogen) werkte vanaf ronde 6; Jordi noemde het shading- en kleurwerk van Cuychu "geweldig".
4. **Kleine, gerichte ingrepen op een goedgekeurde sprite.** Kleurwissel en zwart rond het oog (Cuyby), het mondje en de kleinere spiraal (nachtaap), de schuine hals (alpaca): weinig pixels, direct goed.
5. **Varianten naast het origineel.** Jordi kon kiezen (pluk bij Cuychu, kleinere spiraal, grotere kop) zonder dat het goedgekeurde verloren ging.
6. **Een keuring tegen echte sprites met metingen.** De vormstudie van alle 1024 sprites en de checklist gaven harde maatstaven (formaat per fase, kopverhouding, één oog bij een lange snuit, diagonale gang).
7. **Jordi's precieze, letterlijke feedback met een voorbeeld-Pokémon** ("zoals de poot onder de tong van Linoone").

## Wat niet werkte

De meeste rondes gingen verloren aan dezelfde oorzaken, niet aan gebrek aan regels.

1. **Zonder referentie beginnen.** Bij de olinguito kwamen Linoone, Sandslash en Poochyena pas rond ronde 17; daarvoor gokten agents naar "coati in Pokémon-stijl".
2. **Zelf geconstrueerde lijven** (ovalen, bonen, losse blokken) in plaats van een echte sprite als skelet: Escher-poten, doos-romp, stokpoten, telgang.
3. **Doorfluisteren.** Jordi → Claude → agent → Claude → Jordi. Claude vatte instructies samen, liet punten vallen (oogpositie, masker boven de neus) en gaf soms zelf foute instructies (verre voorpoot naar achteren).
4. **Herbouwen in plaats van bewerken.** "Kop kleiner" of "meer Pokémon" werd een nieuwe kop; goedgekeurde delen gingen mee onderuit ("Chernobyl").
5. **Afwisselend te grote en te kleine stappen.** Herbouw, dan alleen het neusje verschuiven ("prutswerk"), dan weer herbouw.
6. **Te milde keuring.** Agents keurden zichzelf goed en noemden fouten "zwak punt"; Claude gaf die door in plaats van ze terug te sturen (verre achterpoot als schaduw, "er mist een been").
7. **Getallen boven vorm.** Om onder een pixelgrens te blijven werd een poot dun en recht; om de kop kleiner te laten lijken werden de poten stelten.
8. **Elke ronde een verse agent.** Context en eerdere afkeuringen gingen verloren; dezelfde fouten kwamen terug.
9. **Te veel tegelijk** (drie herbouwen parallel) en grote vergelijkingsvellen: veel tokens, weinig winst. Eén makersessie voor de olinguito kostte ±650.000 tokens.

## Waar de AI-aanpak sterk en zwak is

Claude en de agents tekenen sprites als tekstrasters (pixel voor pixel in code) en bekijken het resultaat daarna als plaatje. Dat geeft een duidelijk patroon:

| Sterk | Zwak |
| --- | --- |
| Palet, kleurwissels, shading volgens regels | Natuurlijke constructie van ledematen in 3/4 |
| Meetbare dingen: formaat, open randen, symmetrie, pixeldiff | Beoordelen of iets **leest** (een poot die er technisch staat maar als schaduw leest) |
| Kleine, exacte bewerkingen op een bestaande sprite | Kenmerken op 64×64 laten lezen (klauwen, kop in perspectief) |
| Analyse: vormstudie, checklist, vergelijken met 1000+ sprites | Smaak: "mooi", "schattig", "Pokémon genoeg" |
| Documenteren, opschonen, inbouwen in de ROM | Zichzelf streng genoeg keuren |

Gevolg: bol- en vachtvormen (één silhouet, werk zit in kleur en gezicht) gaan goed; viervoeters en wezens met armen en klauwen niet, tenzij een echte sprite de constructie volledig levert.

## Aanbevelingen voor de aanpakken die Jordi test

Kies een aanpak waarin de vorm al vaststaat vóór de AI begint, en laat de AI doen waar hij sterk in is.

1. **Vorm komt van buiten de AI.** Een ruwe schets of silhouet van Jordi, een aangepaste bestaande sprite (zoals bij een regional form), of een fan-sprite als basis. De AI doet daarna palet, shading, omlijning, opschonen en inbouwen.
2. **Altijd referenties vóór de eerste pixel**: foto van het echte dier + een echte sprite van hetzelfde bouwtype + per kenmerk een voorbeeld.
3. **Direct werken, niet doorfluisteren**: één sessie die zelf de sprite bewerkt en kleine plaatjes laat zien, liefst een nieuw gesprek per sprite (korte context, minder tokens).
4. **Eén onderdeel per stap**, goedgekeurde delen bevroren (pixeldiff 0), grote wijzigingen als variant.
5. **Feedback in één bericht per stap**, met een voorbeeld-Pokémon erbij.
6. **Keuring = wat je op 1× ziet**: elk zelfgenoemd zwak punt is een fail; nooit doorsturen met kanttekeningen.

Aanpakken vergelijken: houd per test bij hoeveel rondes en ongeveer hoeveel tokens het kostte tot goedkeuring, en of het resultaat op 1× naast Poochyena/Cyndaquil als Pokémon leest. De afspraken en lessen staan in `docs/lessen/SPRITE_NORM.md`, `FAKEMON_CHECKLIST.md`, `RETRO_OLINGUITO.md` en deze review.
