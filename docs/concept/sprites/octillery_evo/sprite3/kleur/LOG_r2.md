# Krassault – kleurfase r2 (LOG)

Uitgangspunt `r1.png`; model `../nat_A.png` (spritepixel (x,y) = modelblok vanaf (24+2x, 21+2y)). Silhouet en palet niet aangeraakt. Reproduceren: `python3 maak_r2.py` (alle wijzigingen als data "zone rij x0 tekens", stopt bij een pixel buiten het silhouet), vel: `python3 maak_vel_r2.py`.

Jordi over r1: "Beide tentakelkanonnen mogen nog wat netter, evenals de consistentie in de belijning, de kleinere tentakels en de zuignappen op de de rupsbanden ook, hoofd is bijna helemaal goed, mond mag nog iets beter".

## Diff t.o.v. r1: 254 pixels
| zone | px | |
|---|---|---|
| kl linkerkanon | 15 | |
| kr rechterkanon | 12 | |
| mo mond | 21 | |
| tl kleine tentakels links | 24 | |
| tr tentakels rechts | 12 | |
| rl rupsband links | 56 | |
| rr rupsband rechts | 105 | |
| lb losse lijncorrecties | 5 | |
| kop kop-rand | 4 | zie "Hoofd" |

Lijn erbij 20, lijn weg 46, zwart → lijnrood 97, lijnrood → zwart 1; geel erbij 15, geel weg 7 (alleen zuignappen).

## Hoofd (bevroren)
Kopkoepel, ogen, leden, wenkbrauwen, mantel en vin: index-diff 0. Vier pixels op de **rand** van de kop zijn van zwart naar lijnrood gegaan, elk omdat dezelfde rand erboven/eronder al lijnrood was (om en om op één rand):
- (23,29) (22,30): linkerrand van de kop tegen de dunne tentakel; de rand is erboven (24,27) en eronder (22,31–33) lijnrood. Model: donkerrood, niet zwart.
- (43,34) (43,35): lijn rechts naast het rechteroog; loopt door in (42,36) (42,37) (41,38) (40,39), die al lijnrood waren. Model: donkerrood.
De zwarte kop-rand bij het linkeroog, (21,34–36) (22,37) (23,38), is niet aangeraakt (model: zwart).
`maak_r2.py` meldt met zijn eigen kopmasker "kop-diff: 2" (de twee bij het rechteroog); de twee links liggen net buiten dat masker (x < 24).

## 1. Tentakelkanonnen (één recept)
Recept: lip 1 px, licht linksboven (H, dichtbij met glans W), rechts H→B, onder B→S; opening zwart en rond; achterlijn van de ring in lijnrood; onderrand zwart.
- **Links (dichtbij):** opening was een scheef blok, nu ovaal 2-3-3-2 (rijen 26–29, x 5–7), binnenwand (5,26) lijnrood. Glans van twee losse W naar één streepje (4,25)(4,26). Rechterlip H,H,B,S, onderlip B,B,S. Achterlijn van de ring gesloten: (9,26) erbij, (8,30) zwart → lijnrood: loopt nu (10,25)→(9,26–29)→(8,30).
- **Arm links:** hooglichtstreep van 5 px, (14,31) (15,32–35), midden op de basisband; de schaduwbaan links en de S-rand rechts stonden er al (model). Het model heeft daar geen roze streep, alleen de lichtste armtint: dit is op verzoek toegevoegd.
- **Rechts (ver):** opening was 4-5-4-2 en scheef, nu 3-4-4-2 (rijen 27–30) zoals het model (zwart x 46–49, rijen 27–29); binnenwand S boven en rechts. Hoek (45,25) H → B (ring ronder). Rechterlip H,H,B,B; onder B met S rechtsonder (50,30) (49,31). Geen W (verder weg).
- **Arm rechts:** linkerrand (45,32–34) en (46,36–37) zwart → lijnrood (lichtkant, één doorlopende run tot (47,38–40)); (45,35) blijft zwart (onderrand boven het gat).
- Niet gedaan: een lijn boven/links om de verre ring. Het model heeft daar geen lijn (lichte lip tegen de donkere kop) en die pixels horen bij de kop.

## 2. Belijning
Regel: buitenrand lijnrood waar boven of links open, zwart waar onder of rechts open; binnenlijnen lijnrood; zwart binnenin alleen voor openingen, pupil en overlap in schaduw (beide kanten schaduwtint).
- Buitenrand (script): r1 had 20 afwijkingen, r2 heeft er 10, alle bewust: de doorlopende zwarte run onder het linkerkanon en langs de onder-/linkerkant van de arm ((8,32–33) (12,37–38) (13,40) (8,41)), de onderkant van het gat bij (19,38) (20,40), en de onderste helft van de linkerrand van de linkerrol ((10,55) (11,57)).
- Gewijzigd op de rand: (8,38) punt kleine tentakel; (46,36–37) (45–46,41) rond het gat rechts; (54,37) (61,43); (15,46) (14,47) rond het gaatje onder de arm; (12,50) (11,51) (10,52) linkerrand linkerrol (was zwart-lijnrood-zwart, nu boven lijnrood, onder zwart).
- Binnen: (21,24) (55,25–26) (54,40) (54,43) (53,44) lijntjes onder/naast wratten en het begin van de lage tentakel rechts; plooi (40–42,45) tussen twee basisvlakken; lijn (14–15,47) → (16–18,48) doorgetrokken ((16,48) was een gat).
- Dubbele lijnen weg: (23,27) zwart naast de koprand → vulling; (21,31) zwart naast de wenkbrauwrand → vulling; (4–6,46) lijnrood boven de zwarte onderrand → schaduw; (19,54–55) in de linkerrol; (28,53) (28,55) (28,56) naast de rand van de rechterrol; (46–47,48) en (52–54,50) bij de rechterrol; (52,40).
- Losse lijnpixels weg: (49,40) boven een wrat, (50,37) naast een wrat (nu slagschaduw).

## 3. Kleinere tentakels
- **Linksonder:** de bovenste tentakel (rijen 44–46) had een lijnrode streep boven zijn zwarte onderrand en liep zonder scheiding over in de stomp eronder. Nu: rij 44–45 licht, rij 46 schaduw (x 4–10), daaronder de stomp met lichte bovenkant (rij 47) en schaduw (rij 48). (8,48) H → B en (9,48) lijn → schaduw (model: schaduw).
- Rij 49 x 13–17 was basis + lijnrood: in het model is dat de lichte bovenrand van de rol → B,H,H,H,B.
- **Rechts:** zie belijning (wratlijntjes, (52,40), begin van de lage tentakel in lijnrood).
- De dunne tentakel achter de kanonarm: alleen de dubbele lijn bij (23,27) en (21,31).

## 4. Rupsbanden en zuignappen
- **Zuignappen:** de ruitjes van 4 px (lazen als kruisjes) zijn ovale ringen van 3×4 met een donkere spleet van 2 px, zoals het model (ring ±3×3,5 px): boven c, links c/b, rechts b/a, onder a. Links op x 13–15, rijen 50–53 en 55–58; rechts op x 32–34, rijen 52–55 en 57–60. Alle vier gelijk van maat, 1 rij tussenruimte. Halve ringen tegen de rand blijven staafjes van 2 px, nu b boven en a onder ((11,52–53) (11,55–56)). Boog en streepjes onderaan ongewijzigd.
- **Spiraal:** alle spiraallijnen van zwart naar lijnrood, behalve de onderboog van de buitenste ovaal: die blijft zwart (schaduwkant, zelfde regel als de buitenrand). Lijnposities zijn die van r1/model.
- **Scheidingslijn loopvlak/zijkant** (lijnrood, 1 px naast de ovaal) is weg op de rijen 51–58: het vlak wisselt daar van basis naar schaduw, dat is de rand. Onderaan rechts ((36,59) (37,60)) staat hij nog (schaduw tegen diepe schaduw).
- **Volume:** binnen de ovaal de bovenste rijen basis (rechts rijen 52–54, links 52–54), daaronder schaduw, onderkant diepe schaduw. Het model heeft de zijkant in één donkere tint; dit is toegevoegd zodat lijnrood leest.
- (28,54): lijnrood → zwart, rand van de rechterrol op zijn breedste punt.

## 5. Mond
- Ribbels waren vijf streepjes van 1 px (H,L,B,L,K). Nu: lip (2 px H), lijn, ribbel 1 (H + B), lijn, ribbel 2 (B, onderaan S), zwarte eindlijn. De twee lijnen waaieren uit: lijn 1 (26,40) (27,41–43) (28,44–45), lijn 2 (28,39) (29,40) (30,41–45).
- Lip, opening en de schaduwstrepen in de opening: ongewijzigd.

## Controle
- 1×/2×/4× op licht, donker en wit en 2× tussen Octillery, Scizor, Crawdaunt en Groudon: zie `vel_r2.png`.
- Palet identiek aan r1, 10 kleuren.

## bewaak.py
```
silhouet-diff: 0
geel-diff (plek): 41 (mag binnen mond/zuignappen, verantwoord in LOG.md)
lijnpixels weg: 78 erbij: 183 (binnenlijnen mogen scherper; elk blok verantwoord in LOG.md met het model als bron)
omgekleurd 1<->2: 125 | vulpixels gewijzigd: 714 | kleuren: 10
OK
```
(telt t.o.v. basis.png)

## Zwakke punten
1. **Spiraal op 1×:** in lijnrood valt de krul in het midden van de rollen op 1× weg; op 2× lees je de ovaal, de krul nauwelijks. Dat is de prijs van "rustiger". De krul in de rechterrol (x 40–43, rijen 53–56) is ook op 8× een kluwen van losse pixels.
2. **Ribbels van de mond:** lezen op 2× als twee ringen achter de lip, op 1× nog steeds niet.
3. **Verre kanonring** heeft boven en links geen lijn (model heeft die ook niet); de nabije ring heeft daar de buitenrand. Het recept is dus niet helemaal gelijk.
4. **Zwarte lijnen tussen tentakels in schaduw** zijn gebleven ((18,34–37), (13,41–43), de rechterrand van de verre arm (52,38)…(50,44)): lijnrood valt daar weg tegen de schaduwtint.
5. **Donkerder dan echte Gen 3-sprites** (zelfde als r1): palet mocht niet wijzigen.
