# Sapa Inca – ronde 3 (kleine pixelbewerking op ronde 2)

Bestanden: `sapa_inca.png` (hoofdresultaat), `sapa_inca.txt` (raster van ronde 2 + onderaan het blok "ronde 3"), `bouw.py`, `controle3.py` (diff per zone, staf-eind, staartpuntje), `vel.py` → `vel.png`, `kijk.py`, `variant_gezicht.png/.txt` (variant b). Draaien vanuit de repo-root.
Leidraad (Jordi): "het zijn echt kleine aanpassingen van de sprite die we eerder hadden". De onderlaag `poppetje_staf_256.png` is alleen gebruikt om te zien waar de staf en de hand komen; niets is ervan overgetrokken. De kroonvariant (5a) is overgeslagen (Jordi: "dat komt nog").

## Wat er veranderde
1. **Linkervleugel:** het bovenste deel van de hangende vleugel uit ronde 2 (rij 32–41) staat letterlijk stil. Het onderste deel met de gekartelde vleugelpunt (rij 46–55: m-selout, d-vulling, K-penscheidingen) is ongewijzigd 6 rijen omhoog en 2 px naar links verplaatst (rij 40–49). Daar vouwt het vóór de staf, op heuphoogte. De oude onderkant (rij 42–55) is gewist.
2. **Staf/staartveer (hybride):** 3 px breed. Lichte schacht (y), roestbruine vaan (t) aan één kant en een okeromlijning (a). Bovenaan zit een gouden zonneschijf (Inti) met vier stralen als veerpuntjes met een lavendel punt (echo van de kroon). Onder de hand wordt hij veer: 3 px roestbruin, die naar rechts buigt en tegen het donkere lijf verdwijnt. Hij ligt nergens over lichaamsdelen; alleen de vleugelpunt ligt eroverheen.
3. **Lijf linksonder:** een opvulling in de donkere lijftinten (d, zwarte buitenrand) tussen hand, buik en dij. De omtrek loopt van x19 (rij 44) in een bolle lijn naar x24 (rij 53) en sluit aan op de linkerdij.
4. **Staart:** de roestbruine staart rechts is weg en de flankonderkant is dichtgemaakt. Tussen de poten hangt een gouden puntje van 2 px breed en 4 px lang dat in een punt eindigt (x27–28, y57–60).

## Controles (`controle3.py`, `bouw.py`)
- (i) **Eind van de staf:** de laatste veerpixels (18,49) en (19,50) hebben rechts zwart (K) van het **donkere lijf**, dat zelf d is; de gele buik ligt er 3–5 px vandaan. Onder het eind ligt lucht.
- (ii) **Staartpuntje:** per rij minimaal **1 px lucht links en rechts** naar de poten (rij 57: 1/1; rij 58–60: 1–2 px). Boven het puntje ligt lucht (rij 56): het puntje hangt los tussen de poten en raakt de onderkant van het lijf niet; zie de zwakke punten.
- (iii) **Diff met ronde 2 per zone:**

| Zone | Gewijzigd |
|---|---|
| kroon (incl. kwastjes) | **0 px** |
| gezicht/kop | **0 px** |
| opgeheven rechtervleugel | **0 px** |
| buik (alle gouden pixels) | **0 px** |
| poten | 7 px: 6 = staartpuntje in de lucht tussen de poten, 1 = grensrandje (24,53) waar de opvulling op de linkerdij aansluit; de poten zelf zijn ongewijzigd |
| oude staart | 16 px (weg) |
| flank rechtsonder | 17 px: staartresten weg en de onderkant van de flank dicht (4 px K/d op x34–38, y51–52) |
| linkervleugel + staf + zon + opvulling (x12–24, y23–56) | 149 px in totaal (geschat: ±50 gewist van de oude cape-onderkant, ±45 verplaatste vleugelpunt, ±35 staf, ±25 zon, ±22 opvulling) |

- Silhouet: 1617 px (ronde 2: 1560); +105 / −48. De opvulling linksonder voegt ±22 silhouetpixels toe.
- 15 kleuren + transparant (t wordt nu door de staf gebruikt); aandeel zwart 0,14.
- Open randen (5): de 2 px dunne linkerscheen (al sinds ronde 1) en de linkerkant van het staartpuntje (g, pseudo-omlijning).

## Variant b (gezicht 1 px groter, los, hoofdresultaat ongewijzigd)
`variant_gezicht.png`: het rode masker is 1 rij hoger, de ogen 3 rijen hoog (iris d, glans w, okertint a) en de snavelhaak 1 rij langer; 31 px anders dan het hoofdresultaat, alpha-diff 0. Op 1× zijn de ogen beter te zien; de blik oogt iets verbaasder. Keuze voor Jordi.

## Zelf gekeken (1× en 4× naast ronde 2, licht en donker)
- Kroon, gezicht, buik, poten en rechtervleugel zijn identiek. Op 1× leest de staf met zonneschijf, en de hand houdt hem op heuphoogte vast. Linksonder houdt het lijf niet meer opeens op.

## Eerlijk: wat nog niet klopt
- **Staartpuntje hangt los:** het hangt in de lucht tussen de poten. Een verbinding met de onderkant van het lijf kan niet met 1 px lucht naar beide poten (de spleet tussen de dijen is op rij 54–56 maar 1–2 px). Het kan op 1× als los geel stipje lezen.
- **Hybride staf/staart is sober, misschien te sober:** de roestbruine vaan is op 1× een donker randje aan de staf. Het veerdeel onderaan is maar 5 px en leest op 4× als een bruin klodderje onder de hand, niet duidelijk als staart die achter het lijf verdwijnt.
- **Zonneschijf is klein** (5×5 + stralen van 1 px); op 1× een gouden knop met paarse puntjes, het Inti-gezicht ontbreekt.
- **Hand:** de verplaatste vleugelpunt steekt 4 px links uit het bovenste vleugeldeel. Dat leest als een gebalde vuist/hand om de staf, niet als een duidelijke elleboog links naast het lijf (die zit niet in de ronde-2-vleugel).

## Lessen
- "Kleine aanpassing" bij een verplaatst onderdeel = het bestaande blok letterlijk verschuiven (hier vleugelpunt −2, −6) en alleen de naad bijwerken; geen nieuwe vorm uit de onderlaag tekenen.
- Een lichte staf van 2 px zonder omlijning verdwijnt op een lichte achtergrond; 3 px (omlijning a, schacht y, vaan t) leest op licht én donker.
- Een staartpuntje tussen dijen die op 1–2 px van elkaar staan kan niet tegelijk aan het lijf vastzitten en lucht naar beide poten hebben: kies vooraf welke eis wint.
