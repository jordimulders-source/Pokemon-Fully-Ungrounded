# Kleur ronde 8 (maker-agent, 3 nov)

Basis: ronde 7. Alles met de hand in tekstrijen (`rijen_ronde8.py`: een kopblok + losse rijen, één teken per paletindex). Het palet is gelijk aan ronde 7. Er zijn 181 px gewijzigd: 134 in lijf/kop (#) en 47 in de staart (S). In de buidel, klauwen/handen, buikcrème en het verre oog is niets gewijzigd (script: "bevroren zones geraakt: []").

Jordi letterlijk: "het uiteinde van de staart is een beetje slordig he. Het pixelwerk rondom de ogen ook, plus de ogen zijn ook nog niet helemaal pokemon like. Pixelwerk rondom de oren is niet helemaal netjes. Het stuk lichaam aan de linkerkant tussen arm en hoofd is ook slordig, rechte lijn en lichaam sluit niet helemaal aan, ook qua kleur niet helemaal. De neus is ook een beetje een gekke streep ipv een echte neus. Plus er zijn wat willekeurige vlekken hier en daar, dit moet wat meer pokemon shading zijn."

## Controles (script)
- Alpha-diff met `silhouet_v2/direct_s1a.txt`: **0**.
- Open randen (een randpixel die niet 1/2/4/b/c is): **geen**.
- Losse binnenpixels (raken geen transparant en hebben geen 4-buur met dezelfde index): ronde 7 77, ronde 8 96. Ter vergelijking: Zigzagoon 131 op 1127 px, Mightyena 129 op 1647 px, Linoone 142 op 1089 px. De stijging komt van de 1-px crème oorrand, het oog (lid, glans, iris, onderlid), de neusglans en de ring in de staartbocht. Allemaal bewust, er zit geen dither tussen.

## Per punt
1. **Staartpunt (x 48–57, y 18–29).** De lichte "dop" bovenop (y 19–21) is weg. Nu:
   - een donkere koepel met licht linksboven (5/4);
   - die lichte kant loopt als één boog door langs de punt die links omlaag hangt (x 49–50, y 21–27);
   - een spleet (1) loopt schuin van (53,22) naar (51,27) en geeft de binnenkant van de haak;
   - rechts in de bocht staat de ring op de schacht (crème a/9/8), met boven- en onderrand als boog (∩), net als de ringen eronder;
   - de punt sluit rond af op (49–50,28).
   Bronnen: de render (donkere haak met lichte ring aan de binnenkant), plus Sentret/Furret voor ringen die de buis volgen.
2. **Ogen.**
   - Nabij oog: zwart lid over 4 px (20–23,10), met ooghoeken 1 op (19,11) en (23,11).
   - Iris: boven e-a-e, met de glans 1 px midden boven (21,11) en niet meer in de binnenhoek; onder f-f-f.
   - Een lichter onderlid 4 (20–22,13) zit tussen oog en masker, zoals de lichtere ring om het oog van Zigzagoon.
   - Verre oog: e/f ongewijzigd; alleen een lid 1 op (13,10) en een onderlid 4 op (13,13).
   - Het crème vlekje op de wang (25,10) is 6 geworden.
   - Het masker heeft nog 2 lobben met een brug.
3. **Oren.**
   - Beide oren hebben een crème rand van 1 px (a aan de lichte kant, 9 aan de schaduwkant) en een donkere binnenkant (5 met kern 4). Die binnenkant gaat onderaan op in de schedellijn, zodat het oor op de kop staat zonder losse traplijn.
   - Het oker pixeltje (8) is uit het rechteroor.
   - Omlijning: 4 aan de lichte kant, 1 aan de schaduwkant.
4. **Borst/schouder links (x 14–22, y 19–30).**
   - De rechte 4-lijn onder de kaak (y 20, x 15–21) is weg. Er zit nu een schaduw 5 onder de kaak die schuin taps in het lijf loopt: (15–17,20) → (16–17,21).
   - Het harde 3-blok is een bolling geworden: 7 met een kleine kern 3 op (17,23–24) en (18,23), midden langs de lichte rand. Boven (onder de kaak) en onder (naar de verre arm) wordt het 6, zodat de rechte silhouetrand bol leest.
   - Naar de nabije arm loopt het via 6 naar 5.
5. **Neus.** Ronde neus van 3x2 met punt: (11–13,16) 2-6-2 met glans 6, (10–13,17) 1-2-2-2. Er staat crème snuit omheen: (12–14,15) en (14,16–17). Zo staat hij los van het masker en is hij geen 4-streep meer (bron: Zigzagoon/Raticate, donkere neus met 1 lichtere glanspixel).
6. **Vlekken/shading.**
   - Het zwevende 7-vlak midden op de nabije dij is weg. Het hooglicht staat nu als sikkel linksboven (onder de buik, langs de overlaplijn met de verre dij).
   - De schaduwgrens 5 van de nabije dij is gebogen (x 37 → 36 → 35) in plaats van een rechte kolom op x 36.
   - Verder: de 6-stip op (15,28) en de 5-stip op (23,39) zijn weg, net als de crème dop op de staart en de wangvlek.

## Bevroren: niet aangeraakt (bewezen met het script)
Silhouet, pose, warme grijsbruine familie, buidel (b/c/d incl. zakmond en plooi), crème handen en klauwen (vorm en inkeping), verre oog (13,11–12) en borst-/buikcrème.

## Eerlijke zwakke punten
- **Staarthaak:** het silhouet is in de bocht dicht (geen lucht tussen punt en schacht). De haak leest daardoor alleen door kleur: de lichte boog langs de hangende punt + de ring in de bocht. Op 2x/4x leest hij als een omkrullende donkere punt, maar op 1x vooral als een donkere staartkop met een lichte vlek. Op donkere achtergrond valt de bovenkant van de koepel weg tegen de achtergrond. Een echte haak op 1x vraagt 1–2 px lucht in het silhouet, en dat ligt buiten mijn opdracht.
- **Bovenlid op het masker:** het zwarte lid (1) op het masker (2) blijft op 1x/2x onzichtbaar. Het oog leest door de glans, de iris en het lichtere onderlid, niet door het lid zelf. Op 1x blijft het oog een rood puntje in het masker, zoals bij Coathief.
- **Linkerrand van de borst** (x 15, y 21–27) is in het bevroren silhouet een rechte lijn van 7 px. De kleur verzacht hem (bolling), maar haalt hem niet weg.
- Niet aangepakt, want niet genoemd of bevroren:
  - de buidelplooi (een diagonaal van b/d-paartjes, leest op 8x als stippellijn);
  - de 1-px hooglichtstreep op de nabije bovenarm (4-3-6-5-4);
  - de schuine ringen van de onderste staarthelft;
  - de 4-streep op de verre onderpoot.
  Een keurder kan die als "vlekken" aanwijzen.
- **Geen onafhankelijke keuring gedaan:** ik heb als subagent geen agent-tool om een keurder te starten. De keuring door een verse agent moet Claude nog regelen vóór Jordi.

## Lessen
- Het aantal losse pixels (geteld per 4-buren) zegt weinig: echte Gen 3-sprites hebben er méér (anti-aliasing, omlijningstrapjes). Het gaat om *vormloze* vlakjes. Bekijk elke losse pixel en vraag: is het glans, iris, rand of overgang? Zo niet, dan weg.
- In een dicht silhouet leest een haak alleen als de lichte kant als één doorlopende boog van de koepel langs de punt loopt; een losse lichte dop bovenop (ronde 7) maakt er een knots van.
- Een glans in de binnenhoek van een oog van 3 px leest als wit oogwit; midden boven in de iris leest hij als Pokémon-oog.
- Patchblokken met volle rijen overschrijven ongemerkt bevroren delen (ronde 8 concept: de nabije hand). Gebruik spaties voor "houden" en draai altijd de bevroren-zonecheck.
