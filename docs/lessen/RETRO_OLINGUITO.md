# Retrospectief: het olinguito-proces (23 okt)

Ruim 23 rondes voor één fase-1-sprite, met steeds terugkerende fouten. Jordi: "het hele olinguito-proces loopt gewoon super slecht, daar moeten we echt van leren." Dit bestand legt vast waarom, en wat er vanaf nu anders gaat. Geldt voor elke sprite.

## Wat er misging (oorzaken, niet symptomen)
1. **Geen referentie aan het begin.** Pas rond ronde 17 kwam Galar-Linoone (gezicht, poten), Sandslash (klauwen), Poochyena (lijf). Daarvoor gokten agents naar een "coati in Pokémon-stijl". Cuyby/Cuychu/alpaca gingen snel zodra er foto's waren.
2. **Geen vaste specificatie.** Wat goedgekeurd was (masker, oren, kop ronde 16) stond nergens als bevroren; elke ronde kon het weer veranderen. Het ontwerp dreef weg van concept B.
3. **Claude parafraseerde Jordi.** Instructies werden samengevat tot een eigen lijstje; eerdere punten vielen weg; een nieuwe referentie werd als vervanging behandeld i.p.v. aanvulling (oogpositie, masker boven de neus, wenkbrauw). Soms gaf Claude zelf een foute instructie (verre voorpoot naar achteren, achterpoot naar achteren).
4. **Agents tekenen opnieuw in plaats van te bewerken.** "Kop kleiner" of "één oog" werd een herbouw; goedgekeurde delen gingen mee onderuit (rondes 12, 17, 19: "Chernobyl").
5. **Te grote en te kleine stappen afwisselend.** Herbouw → Jordi boos → micro-fix (alleen het neusje) → "prutswerk" → weer herbouw. Geen middenweg: een onderdeel met de vorm eromheen.
6. **Claude's controle was holistisch en soms afwezig.** "Is het een dier, is het niet vreemder?" in plaats van per onderdeel; agent-kanttekeningen ("poot 5 px smal") werden doorgegeven in plaats van afgekeurd; rondes 17/18 gingen ongezien door.
7. **Grenzen wonnen van vorm.** Om onder een pixeldoel te blijven werd een poot dun en recht.
8. **Elke ronde een verse agent.** Context en eerdere afkeuringen gingen verloren; dezelfde fouten kwamen terug (beige vlak, telgang, stokpoten).
9. **Te veel tegelijk lopend.** Meerdere sprites en agents parallel; Claude's aandacht per resultaat werd te dun.

## Wat er vanaf nu anders gaat
1. **Referenties eerst** (al in FAKEMON_DESIGN.md): foto + skelet-sprite + per kenmerk een sprite, vóór de eerste pixel. Elk onderdeel heeft een referentie die de specificatie is.
2. **Specificatieblad per sprite** (`SPEC.md` in de map): per onderdeel (kop, ogen, masker, oren, romp, elke poot, klauwen, staart) de referentie, de status (goedgekeurd/bevroren of open) en Jordi's letterlijke woorden. Elke agent werkt alleen aan de open onderdelen; bevroren = pixeldiff 0.
3. **Eén onderdeel per ronde, inclusief de vorm eromheen**, op de referentie overgetekend; niet herbouwen, niet micro-fixen.
4. **Dezelfde agent per sprite** zolang hij loopt (SendMessage), zodat hij zijn eigen afkeuringen onthoudt; anders AFGEKEURD.md + SPEC.md meegeven.
5. **Claude's controle per onderdeel**, 8× per ledemaat: vast aan het lijf? rechte lijn? dikte gelijk aan tegenhanger? diagonaal (geen telgang)? bevroren delen diff 0? AFGEKEURD-punten? Eén "nee" = terugsturen, niet doorgeven.
6. **Drie keer mis op hetzelfde onderdeel = stoppen** en Jordi om een "zo bedoel ik het"-referentie vragen in plaats van een vierde gok.
7. **Maximaal één sprite tegelijk in pixelwerk**, zodat elke controle de volle aandacht krijgt.
