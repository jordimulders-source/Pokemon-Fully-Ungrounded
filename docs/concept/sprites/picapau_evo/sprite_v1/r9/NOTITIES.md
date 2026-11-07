# Picapau-evolutie: sprite r9 (kop naar Swellow en nieuwe krullen, op r7)

r7 en r8 blijven staan.

## Jordi letterlijk
- Over r6: **"ik wil beide krullen bovenop naar achteren en die snavel is geen snavel, kijk bijv naar fearow of andere vogels, echt lelijk. Voor de rest is die wel prima. Alleen de buik is niet meer mooi ovaal. De pose is prima"**
- Over de snavel van r7: **"niet mooi, past niet bij het hoofd en is niet zo mooi als bij normale pokemon sprites"**
- Over r8: **"nee ik vind het ook nog niet zo mooi, hoe kunnen we dit beter maken, daarnaast is 1 van die slingers op zijn hoofd bijna een rechte lijn"**
- Op het voorstel van de coördinator (gezicht als geheel naar Swellow): **"probeer maar"**

## Diagnose (coördinator)
De snavel werd steeds los op een bevroren gezicht gezet. Bij echte sprites horen snavel, snavelvoet, oog en wang bij één ontwerp. Daarom verandert het gezicht nu mee.

## Werkwijze
- `basis.txt` = r7 zonder snavel en oren.
- `kop.txt` (met de hand) bevat het gezicht, de snavel en beide oren.
- `maak.py` maakt daarvan `tekening.txt` en draait `zet.py`, `bouw.py`, `controle.py` en `diff.py`.
- `platen.py` maakt `vel.png` (1× en 8×: r9, r7, Swellow, Pidgeotto en Picapau) en `kop_closeup.png` (16×: kop r9, kop r7, Swellow, Pidgeotto en Picapau).
- Het palet is ongewijzigd (`normal.pal`).

## Bevroren: bewijs
- `diff_uitvoer.txt`: **0 px verschil buiten de zones**, in het raster én in de png. De zones zijn de kop (x4-32, y4-18) en de krullen (x14-46, y0-14).
- Binnen de zones veranderen 89 px aan de kop en 83 px aan de krullen; de lijst per pixel staat in `diff_uitvoer.txt`.
- Rij 15-18 (keel en buik) zijn niet aangeraakt, hoewel ze in de kopzone liggen.

## Controle (`controle_uitvoer.txt`)
- Geen lichte kleur op de buitenrand.
- Geen losse pixels.
- Geen tintclusters kleiner dan 3 px.
- 15 kleuren + transparant, 1740 px.
- Alleen-diagonaal verbonden: 2 px (de spiraallijnen).

## Swellow (eerste frame), opbouw van de kop
- **Snavel**: 9 px lang, punt op (5,15).
  - Bovenrand in een donkere snaveltint (g, donkerbruin), een steile, licht bolle boog van de voet naar de punt.
  - Licht (j, en m als lichtste tint) bovenop in het midden, donkerder (n) naar de voet en de onderkant.
  - De mondlijn (g, gekleurd, niet zwart) loopt van de punt schuin omlaag naar de mondhoek onder het oog.
  - De ondersnavel is korter en heeft zwart (f) aan de schaduwkant linksonder.
- **Voet**: 6-7 rijen hoog. Hij gaat met een donkerrode naad (e) over in het rode gezichtsmasker, dat de voet aan alle kanten omsluit.
- **Oog**: direct rechtsboven de voet, op de hoogte van de bovenrand van de snavel. Een half gesloten oog met een lila ooglid.
- **Wang/gezicht**: het rode masker loopt van het voorhoofd om de snavelvoet heen naar de keel. De blauwe kop zit erboven en erachter.
- **Verre oog**: niet zichtbaar.

## r9 naast Swellow, per onderdeel
| Onderdeel | Lijkt op | Wijkt af in |
|---|---|---|
| Snavel, omtrek | Bovenrand in een donkere snaveltint (G), een boog die naar de punt steiler wordt (trappen 4-2-2-1); ondersnavel korter (punt x14 tegen x11). | 12 px lang in plaats van 9, en rechter (beitel, geen bolle haak), zoals gevraagd. |
| Snavel, licht/schaduw | Licht (a) als vlek bovenop, donkerder (g) naar de voet en de onderkant, G aan de schaduwkant van de ondersnavel. | Maar 3 tinten (a/g/G) in plaats van 4 bij Swellow (m/j/n/g); de overgang van a naar g is harder. |
| Mondlijn | Loopt van de punt schuin omlaag naar de mondhoek (rij 12 → rij 13). De mondhoek is rood en loopt over in de wang. | Zwart (k) in plaats van een gekleurde snaveltint: ons palet heeft geen donkere hoorntint naast G. |
| Voet | 7 rijen hoog (rij 8-14), direct tegen het gezicht, zonder voeg. | Geen gekleurde naad (Swellow: donkerrood e). Grijs grenst direct aan oranje. |
| Oog | Direct rechtsboven de voet, op de hoogte van de bovenrand (oog van Picapau, 1 px naar links). | Het oog is open (Picapau), niet half gesloten. |
| Wang/gezicht | De rode wang ligt nu tegen de voet (2 px naar links geschoven) en de rode mondhoek loopt erin over. | Geen masker dat om de voet heen loopt. Ons gezicht is oranje (2/3), alleen de wang is rood; het voorhoofd boven de snavel is gewoon oranje met een lichte rand (1). |
| Verre oog | Vervalt, zoals bij Swellow. Daar loopt nu de lichte rand (1) van de kop. | — |

## Krullen
- **Verre oor**:
  - begint op de kruin (wortel kGGGk);
  - loopt een korte boog over de bovenkant (rij 0, x26-34);
  - krult meteen om in de spiraal met gat boven de achterkop (x31-36, rij 1-6).
  - In r7 was het een rechte steel van 15 px.
- **Nabij oor**: om plaats te maken is het één verdieping lager gezet. Het vertrekt vanaf de achterkop (rij 8) en eindigt in dezelfde spiraal (x33-38, rij 8-14), net boven de vleugeltop.
- Op 1× lezen beide oren als slinger, boven elkaar zoals bij Raichu Gen 1.

## Eerlijke zwakke punten
1. **Nog steeds lang.** De snavel is 12 px. Naast Swellow (9) is hij groot voor de ronde kop. Op 8× domineert hij het gezicht nog.
   - Als Jordi hem nog te lang vindt: 10 px is de volgende stap.
2. **Licht als band.** De lichte vlek (a) loopt in drie diagonale rijen langs de bovenrand. Op 16× is dat nog een beetje een strook, geen ronde vlek zoals Swellows m/j.
3. **Geen echt masker.** Swellows gezichtsmasker omsluit de voet; bij ons is alleen de wang rood. Het voorhoofd boven de snavel blijft oranje. De snavel zit daardoor minder "in" het gezicht dan bij Swellow.
4. **Zwarte mondlijn.** Hij is zwart, niet gekleurd. Op 8× is hij duidelijk zichtbaar.
5. **Nabij oor.**
   - Het zit nu op de achterkop op ooghoogte, niet meer bovenop. Dat leest meer als een oor aan de zijkant.
   - Zijn steel (rij 8, x31-36) is weer een recht stuk van 6 px.
6. **Rechte stukken in het verre oor.** De boog bovenop heeft nog een recht stuk van 9 px op rij 0. Hoger kan niet, want rij 0 is de rand van het beeld. Op 1× leest het als een krul, op 8× zie je het rechte stuk.
7. **Vleugel onder de punt.** Onder de snavelpunt zijn twee lichte vleugelpixels (13,13) en (13,14) schaduw (4) geworden, om clusters van 2 px te voorkomen.
8. **Niet gekeurd.** Er is nog geen onafhankelijke keuring gedaan.

Er is niets gecommit en niets verwijderd.
