# La Paz (startstad): concept-tileset

Secondary bij de General-primary (paletten 6–12). Opnieuw maken: `python3 tools/concept/tiles/la_paz_tiles.py`
(vaste seed, gedeelde hulpjes in `tools/concept/tiles/tilelib.py`). Nog niet in de game; geen kaarten.

## Bestanden
- `tiles.png`, `palettes/06–12.pal`, `metatiles.bin`, `metatile_attributes.bin`: zoals een GBA-secondary ze heeft.
- `metatile_names.json`: naam → metatile-id (voor kaartbouwscripts later).
- `sheet.png`: alle metatiles (8 per rij, 2×). `tiles_sheet.png`: de 8×8-tegels in hun eigen palet. `paletten.png`: de 7 paletten.
- `mockup.png` / `mockup_2x.png`: voorbeeldscène 30×24 metatiles. `vergelijking.png`: mock-up naast Slateport (zelfde schaal).

## Wat erin zit
- **Straat (palet 6):** kasseien (3 varianten, één met onkruid), stoeptegels, stoepranden (4 richtingen), plaza-platen,
  kleigrond (2), trappenstraat (met/zonder wangen, gele trapranden), stenen keermuur, kleiwand in Hoenn-rotsstijl
  (rand/midden/voet, stukken a/b herhalen per 32 px, linker-/rechtereind) met trap erin.
- **Huizen (palet 7, varianten 8 en 9 zonder extra tegels):** modulaire bouwstukken.
  - Plat betonnen dak (2 rijen diep) met watertank (tinaco), wasgoed, schotel, wachtijzers.
  - Golfplaatdak (2 rijen) met stenen erop.
  - Gevels per verdieping (1 rij) en begane grond (2 rijen): onafgewerkte baksteen met betonnen kolommen en vloerplaten,
    of gepleisterd; ramen, gordijn, deur, rolluik, open winkeltje, open ruwbouwverdieping (obra gruesa).
  - Palet 7 = rode baksteen + zinken dak; 8 = oker gepleisterd + roestig dak; 9 = lichtblauw + rood plaatijzer.
    Elk stuk bestaat in alle drie (`naam@8`, `naam@9`). Baksteen in palet 8/9 leest als geverfde baksteen.
  - Breedte en hoogte vrij: 2–N breed, 1–N verdiepingen; dus veel huistypes uit weinig tegels.
- **Cholets (palet 10):** modulair: dak, kroonlijst (3 kleurensets), verdiepingen met spiegelglas (3 kleurensets,
  met ruitmotief), feestzaal op de begane grond met gouden deur, en het 'chalet' van de eigenaar bovenop (3×2).
  Elke breedte ≥ 3 en elke hoogte.
- **Kabelbaan (palet 11):** station (Ekat 'Cable Car', omgekleurd), masten voor oost-west en noord-zuid, kabels
  (bovenlaag, dus boven de speler en over elk dak heen), gondels in rood/geel/groen (1×2).
- **Markt (palet 11):** kraam met blauw zeil en rood-wit gestreept zeil (de Slateport-tent als basis), aardappels in
  alle kleuren met weegschaal, fruit, kleed (aguayo), zakken, kist, gedroogde kruiden.
- **Straatmeubilair en groen:** lantaarn, bank, putdeksel, plantenbak met bloemen, eucalyptus (2×3).
- **Decor (palet 12):** de Illimani (12×5, drie toppen) en een herhaalbare lagere bergkam (2×5) voor de rest van de rand.

## Budget
- **504 / 512 tegels, 409 / 512 metatiles** (inclusief 10 tegels en 29 metatiles voor de kabelcombinaties van de mock-up).
- Per onderdeel (tegels): cholets 63+19 (chalet), kleiwand 48, station 48, Illimani + bergkam 48, begane grond 43,
  tenten 37, daken 35, verdiepingen 34, masten 19, waren 19, eucalyptus 17, golfplaat 16, rest (grond, meubilair) ±60.
- Paletten: alle 7 vol (6 straat, 7–9 gebouwen in drie kleuren, 10 cholet, 11 kabelbaan + markt, 12 natuur/bergen).
- Kabels over iets met een bovenlaag (boom, tent, lantaarn, dak-rand) kosten nieuwe tegels per combinatie; kabels over
  grond of daken in de onderlaag kosten alleen een metatile. In de mock-up: 10 tegels.

## Hergebruik en credits
- Kabelbaanstation: **Ekat (Ekat99) en Heartlessdragoon**, sheet 'Cable Car' (`tilesets/nieuw/ekat/`), omgekleurd naar palet 11.
- Marktkraam: de tent van **Slateport City** (Game Freak, Pokémon Emerald), omgekleurd.
- Al het andere is zelf getekend. De kleiwand volgt de vorm van de General-rotswanden (brokken met licht linksboven).
- Gras, water en bomen kunnen uit General blijven komen (niet in de mock-up gebruikt).

## Wat ik zelf nog niet goed vind
- **Tegelbudget is op.** Voor een enorme stad met meerdere wijken is 8 tegels vrij te krap (gymgebouw, Pokémon Center
  in eigen stijl, kerk/koloniaal centrum, meer cholets). Voorstel: een eigen **Andes-primary** (zoals Ashfrost) met
  grond, kliffen, trappen, bergen en straatmeubilair, gedeeld met de altiplano; dan houdt de secondary ±300 tegels
  voor gebouwen. Alternatief: twee secondaries per wijk (centrum vs. El Alto) die alleen via warps aansluiten.
- **Kleiwand** leest als rotswand, maar nog wat te regelmatig (zelfde brokken per 32 px); echte La Paz-hellingen hebben
  grillige geulen. Een tweede variant (c/d) zou helpen.
- **Platte daken** zijn grijze vlakken: klopt met La Paz, maar is minder kleurrijk dan Hoenn. Meer dakrommel
  (gasflessen, kratten, halve verdiepingen) zou het levendiger maken.
- **Gondels** hangen nu als tegels; in de game horen ze een bewegend object (sprite) te zijn langs de kabel. Dan kosten
  ze geen tegels en wordt de lijn ook levend.
- **Kabels** lopen alleen recht (oost-west of noord-zuid). Schuine lijnen zouden per tegel nieuwe tegels kosten.
- **Illimani-lucht** is een vlakke lichtblauwe band. In een top-down kaart is dat een keuze: werkt als rand van de kaart,
  maar de speler mag er niet heen kunnen (botsing).
- **Station** is één ontwerp (Ekat, blauw dak). Mi Teleférico heeft per lijn een kleur; een tweede, eigen modern station
  past niet meer in het budget.
- Ramen op de verdiepingen zijn klein (7 px hoog); gevels lezen goed, maar het is druk als alles baksteen is: afwisselen
  met gepleisterd (zoals in de mock-up) werkt beter.
- Deuren hebben gedrag `MB_NORMAL`; bij echte kaarten de deurtegels `MB_NON_ANIMATED_DOOR` (of een deuranimatie) geven
  (les: deur-tile = de tile met deurgedrag).
