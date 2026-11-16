# Pitahaya-draak r7 (op sprite_r6/pitahaya_r6.png)

Jordi: "rechterarm zit vast aan het lichaam, kijk nog beter naar schaduw, kleur, belijning". r6 loste dat half op (gaatje van 4 px; bovenarm vloeide in de romp).
Regel: "niks zelf tekenen, totdat er een vorm staat" · "MODEL OVERNEMEN, NOOIT HERTEKENEN". Geen pixel getekend: alles komt uit het natieve model (`natief.png`, pitch 5,118, factor 3; spritepixel (X,Y) = natief blok (3X+4, 3Y+6)) of is een technische opschoning.

## Bestanden
- `maak_r7.py` (aanroep `python3 maak_r7.py`), invoer `pitahaya_r6.png`, `natief.png`, `groepen.py` (kopieën). Elke gewijzigde pixel met stap en zone: `pitahaya_r7_afwijkingen.txt`.
- `stats.py` (zwart, vulvlakjes, dambord, tinten), `vel.py` → `vel.png` (r7 | r6 | model op 8×; beide armen op 12× naast het natieve model; 1× en 2× op licht en donker).
- Palet ongewijzigd t.o.v. r6 (geïndexeerd, index 0 transparant, opgeslagen met transparency=0).

## Bevroren (assert in het script)
Ooggebied x 18–36 / y 22–27 en mond/kin/tandje x 18–34 / y 28–34: 233 px, diff 0. Silhouet-diff met r6: 0 (het gat stond al in r6; het model toont geen extra achtergrond).

## Gen 3-studie (Treecko, Cacnea, Bagon, Oddish op 8×)
Grote tintvlakken die de vorm volgen; binnenlijnen dun en in de donkerste vlaktint, zwart vooral als buitenlijn aan de schaduwkant en waar een vorm over een andere valt (kop over lijf). De r6-kop en -romp hadden te veel zwart binnen de figuur (6,9 %; Treecko 4,1, Larvitar 5,0, Cacnea 7,7) en losse vlekjes.

## Stappen
1. **Lijnen uit het skelet van het model** (GEMINI.md, spooktrein fase 3 punt 2): modellijnpixels (zwart, of groen/roze lum < 70) natief geskeletteerd; stukjes < 12 natieve px (= 4 spritepx) zijn vlekjes en tellen niet. Elk skeletpunt wordt geprojecteerd op zijn spritepixel; waar dat 2 px dik wordt (diagonaal over een blokgrens) op spriteniveau gedund tot 1 px.
   - Kleur: **zwart alleen waar de modellijn ≥ 3 natieve px dik is** (afstandstransform ≥ 2), anders de donkerste tint van het vlak (roze 2, groen 8). Dunne zwarte modelstreepjes (schubranden rechts op de kop) worden zo donkerroze.
   - 1a: de modellijn tussen kop (roze) en lijf (groen) op y 33–38 is de onderrand van de kop aan de schaduwkant: zwart (het model heeft daar zwart; zoals r6).
   - Dikke zwarte lijnen worden niet gedund.
2. **Gat**: achtergrond die het model tussen arm en romp insluit → transparant bij ≥ 3/9 (zelfde 4 px als r6).
3. **Vulling uit de toonkaart**: per groep (roze kop, groen kop, groen lijf) de luminantie van de modelpixels binnen de groep gladgestreken (σ 1,6 natieve px), 3 tinten (roze 3/4/5, groen 9/10/11; de donkerste modeltoon valt in de schaduwtint). Drempels = kwantielen: elke tint krijgt hetzelfde aandeel als de natieve modelpixels in die blokken (roze kop 30/49/21 %, groen lijf 52/31/17 %), dus het volume van het model.
4. **Ruis**: vulvlakjes < 3 px (4-verbonden) → meest voorkomende 4-buur uit dezelfde groep. Losse groene schubpunten tussen roze hebben geen groene buur en blijven.
5. **Wit**: areolen alleen waar het model ≥ 2 witte px heeft (niet het gat): (25,38), (29,39), (30,48), als in r6.
6. **Buitenlijn** 1 px: zwart waar de normaal naar rechts/onder wijst, selout (2/8) naar links/boven (bij een diagonale normaal rechtsboven: selout, linksonder: zwart). Om-en-om gecontroleerd: 0. Lichte tint op de rand: 0.

## Afwijkingen t.o.v. r6 (230 px; per pixel de laatste stap)
| Stap | kop (y ≤ 36) | romp | linkerarm | rechterarm | poten | totaal |
|---|---|---|---|---|---|---|
| 1 lijn uit het modelskelet | 33 | 5 | 4 | 7 | 7 | 56 |
| 3 toonkaart | 52 | 20 | 8 | 22 | 25 | 127 |
| 4 ruis (< 3 px) | 14 | 2 | 6 | 4 | 8 | 34 |
| 6 buitenlijn licht/schaduw | 1 | 0 | 1 | 8 | 3 | 13 |
| totaal | 100 | 27 | 19 | 41 | 43 | 230 |

Zones: kop y ≤ 36; rechterarm x 35–46 / y 37–48; linkerarm x ≤ 24 / y 37–47; poten y ≥ 48; romp de rest. Getekend: 0.

## Per punt van de opdracht
1. **Rechterarm**: de binnenkontour loopt nu als doorlopende 1-px lijn van de schouder (39,38), waar hij diagonaal op de bovenlijn (40,37) aansluit, langs x 39 en (38,44–45) tot de klauwen (39,46)–(39,47), donkerste groen waar het model een dunne donkere lijn heeft en zwart waar het dik zwart is (onderaan, naar de klauwen). Het gat (38,41–43), (39,43) en het gat onder de klauwen (40,47), (41,48) zoals in het model; het model toont niet meer achtergrond. De bovenarm is lichter (modeltoon), waardoor hij als eigen vorm tegen de donkerdere romp staat.
   **Linkerarm**: leest los zoals het model: gat x 23–24 / y 41–45 met lijn eromheen; de binnenrand van de bovenarm heeft de modellijn (x 22, y 37–39 → x 23, y 40–41, daarna zwart langs het gat).
2. **Lijf/poten**: grotere tintvlakken (licht op rechterbovenarm, dijen en linkervoet zoals het model; schaduw onder de kop en tussen de benen). Vulvlakjes < 3 px: 45 → 22 (de rest zijn 1-px groene schubpunten in de kop en pixels in het bevroren gezicht; in het lijf alleen (20,45) klauw en (41,53) teenlicht). Zwart in het lijf 92 → 63 px.
3. **Kop** (buiten oog en mond): zwart 87 → 77 px, rechts (x ≥ 37) 44 → 36; dunne schubrandstreepjes zijn donkerroze; de lichte schubbulten op voorhoofd en kruin staan waar het model licht is; groene schubpunten en de echte naden blijven.
4. **Belijning**: zwart van de figuur 16,5 % → 12,9 %, binnen de figuur 6,9 % → 4,0 % (Gen 3-band 1–8 %). Buitenlijn: 97 zwart, 76 selout, 0 om-en-om.

## Metingen (`stats.py`)
| | r6 | r7 |
|---|---|---|
| zwart van de figuur | 16,5 % | 12,9 % |
| zwart binnen de figuur | 6,9 % | 4,0 % |
| vulvlakjes < 3 px | 45 | 22 |
| dambord 2×2 | 3 | 9 |
| lichtste groen (11) / roze (5) | 34 / 71 | 61 / 80 |

## Zelf vergeleken (r7 naast r6 en het model op 1×, 2×, 8×)
- **Beter:** de rechterarm leest op 2× los over de hele lengte (lichte arm, lijn naar de romp, gat); de romp is rustiger en minder zwart, met het licht waar het model het heeft; de rechterkant van de kop is minder streperig. Volume niet platter: er is meer licht (groen 11: 34 → 61 px) en de schaduwsikkel rechts en onder de kop blijft.
- **Zwak punt / open:** dambord 3 → 9. Eén zit in het bevroren gezicht (21,31); twee zijn een Λ-knoop van twee schubnaden (39–40,20) en een naadkruising (30,14); de andere vijf zijn 1-px diagonale ribbellijnen in de romp en poten (Gen 3-refs 4–14, ook diagonale lijnen). Ik heb ze niet weggehaald, omdat dat de modellijnen zou breken.
- Bovenrand van de rechterschouder (40–41,37) is nu selout (bovenkant, lichtkant) waar r6 zwart had; het model heeft daar een dunne zwarte lijn onder de kop. Als de keurder dat als slagschaduw wil: 2 px terug naar zwart.
