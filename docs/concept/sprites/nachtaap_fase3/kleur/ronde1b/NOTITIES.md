# Nachtaap fase 3: kleurronde 1b (5 nov)

Bestanden: `nachtaap_fase3.png`, `normal.pal` (zelfde palet als ronde 1, zie `../ronde1/NOTITIES.md`), `raster.txt`, `vel.png` (ronde 1b 4× licht/donker, model, 3× ronde 1b naast 3× ronde 1, 1× licht/donker naast fase 2 en Primeape/Medicham/Alakazam/Slaking/Aipom).
Bron: `bron/delen.txt` (alle rijen opnieuw met de hand geschreven) → `bron/bouw.py` → `bron/check.py` → `bron/vel.py`. Ronde 1 is onaangeroerd.

Opdracht: Claude-check ronde 1 (zes zones) + Jordi: "let ook op verhouding van benen, armen met lichaam, strepen etc, dat het er natuurlijk uit blijft zien" en "ja vooral verbinding van onderste been met lichaam, strepen laat maar weg, want daar maken we een ander patroon van".

## Werkwijze
Ik heb een waardekaart van het model gemaakt (`onderlaag_256.png` → helderheid per 64-pixel, in 4 klassen) en die naast het raster gelegd als gids voor licht en schaduw per zone. De rijen heb ik daarna met de hand geschreven: ruis weggelaten, banden doorgetrokken en gezicht, hand en spiraal zelf getekend. De kaart is dus alleen een onderlaag, geen automatische shading.

## Per zone
1. **Lijf, poten, armen (volume):** alle vier vachttinten gebruikt (L 166, V 365, S 400, D 303 px; ronde 1 had 492 V).
   - Bovenste been: lichtband links (2–3 px), schaduw rechts. De want-voet heeft een lichte bovenkant en een kreukel rechts.
   - Vuistarm: zoals in het model grotendeels in de schaduw (de arm ligt achter de kop), met een lichtstreep over de bovenkant van de onderarm.
   - Heup en achterwerk onder de staartwortel: licht, zoals in het model.
   - Romp naast de kop: S/V met een lichte band, D als sikkel langs kop en onderkant.
   - Healerarm: lichtband links, schaduw rechts.
   - Onderbeen: lichtband langs de bovenkant van het scheenbeen, schaduw en D-sikkel aan de onderkant.
   - De dikte van armen en benen volgt het silhouet (bevroren); er zijn geen vlakken die een ledemaat dunner of dikker laten lijken.
2. **Aansluiting onderste been (Jordi):** de K-naad tussen romp en dij (ronde 1: x31–33, rij 40–46) is weg.
   - De dij loopt nu als één vorm over in heup en romp: lichte vlek linksboven op de dij, V eromheen, S naar onder.
   - Er is een D-schaduwsikkel onder de dij en de bil (rij 47–52).
   - Tussen romp en dij zit alleen een zachte D-plooi van 1–2 px, die overgaat in de bestaande spleet van het silhouet bij rij 47.
   - De lijn onder de staartwortel is D in plaats van K.
3. **Kop als bol, geen ring:**
   - Vacht licht linksboven (L-rand links), V boven, rechts S en D. De rechterkant heb ik één tint lichter gemaakt dan in de eerste opzet, anders werd hij een zwarte ring.
   - Het gezichtsschild heeft afgeronde hoeken: de wenkbrauw loopt recht van x5 tot x13 (Jordi: rechte wenkbrauwlijn), de zijkanten en kaak zijn gebogen.
4. **Maan:**
   - Sikkel met de punten omlaag, x5–14 (10 px breed, groter dan in het model).
   - Dik midden van 3 px (rij 30–32, W met M-onderrand) en twee spitse hoorns tot rij 34; de linker (nabije kant) is dikker.
   - Aan de onderkant een rand in vachtschaduw (S, rij 33) tussen de hoorns, zodat het een tekening is.
   - Erboven 1 rij vacht (rij 29). Meer kan niet: daarboven ligt meteen de kopomtrek van het bevroren silhouet.
5. **Healerhand** (Gen 1-Drowzee + model):
   - Vijf vingers: duim linksonder plus vier vingers, waarvan de pink 1 px.
   - Vingertoppen afgerond. De toppen zijn 2 px, zonder omlijning op de hoeken; de gloed loopt boven en tussen de toppen door (rij 47–50), zodat de vingers vrij staan.
   - Lichte waaier: de middelste twee vingers zijn het hoogst.
   - De lijnen tussen de vingers zijn D bij de toppen en vervagen naar m in de palm.
   - Duim met een schuine naad, en een gloedinham tussen wijsvinger en duim.
   - Palm met volume: licht midden (M, glimlicht W op 14,54), schaduw m naar de pols rechtsonder.
6. **Spiraal:**
   - Windinglijn K van de inkeping onderaan langs links omhoog, over de bovenkant, rechts omlaag en eindigend tegen het gat. De segmenten lopen geleidelijk (6 recht, 1-1-1 diagonaal, 4 recht, 1-1, 5 recht, 1-1).
   - De staart is een cilinder: buitenwinding licht langs de buitenkant links/boven, schaduw aan de binnenkant; de binnenwinding is licht linksboven.
   - Gat: zijkanten in omlijning (K boven/links, D rechts/onder). **Afwijking van de opdracht:** de vier hoekpixels rond het gat heb ik níet in omlijningskleur gezet maar in S. Met donkere hoeken werd de donkere rand een vierkant kader; met lichtere hoeken leest het gat als een rondje/achthoek (getest op 8× en 3×; de variant met donkere hoeken staat in de scratchpad, `delen_hoekdonker.txt`). Claude kan kiezen.
7. **Gezicht:**
   - Snuit lichter en ronder, met één M-glimlicht op (7,40).
   - Neusgaten duidelijk als twee K-pixels (7,41) en (9,41).
   - Mondlijn van 1 px (K, rij 44).
   - Wenkbrauw strak (f).
   - Kin in gezichtsbasis F met f-schaduw, niet meer de donkerste tint.
8. **Rugwiggen:** helemaal weg (Jordi). De rug is gewoon vacht met volume.

## Controles (`bron/check.py`)
- 1796 px, **alpha-diff 0** met `silhouet/ronde1.txt`. Geen afwijking nodig.
- Open randen: 0. Losse pixels: 32, allemaal bewust (ogen, glans, neusgaten, lip, knokkelgroeven, pink, pols, glimlicht palm, randhoeken).
- Zwart-aandeel van de omtrek: 0,50.

## Eerlijk: wat nog niet klopt (op 1× en 3× naast het model, ronde 1 en echte sprites)
- **Kop leest nog steeds als helm met vizier.** De bolshading helpt, maar de ronde vachtkap om het donkere gezicht met een witte boog bovenop blijft op 1× een astronautenhelm. De maan leest op 3× als sikkel (hoorns en schaduwrand zichtbaar), op 1× als witte boog/glimlicht.
- **Healerhand:** de vingers staan nu vrij en de gloed loopt ertussen, maar op 1× is het nog een lichte vlek met streepjes. Op 3× lezen vier vingers + duim, al lijken ze eerder stompjes dan Drowzee-vingers (2 px breed is het minimum). De wijsvinger is maar 3 rijen lang en valt weg.
- **Spiraal:** leest op 3× als krul/"@", op 1× als lus. Het gat blijft hoekig (3×4, bevroren).
- **Romp/dij:** de aansluiting is nu één vorm, maar de D-plooi tussen romp en dij (x29–31) leest op 3× nog als een donkere voor. Dat is wel waar het silhouet de spleet heeft. Het lijf is nog wat korrelig (D/S-wisselingen aan de rand van de dij).
- **Gezicht:** snuit en neusgaten lezen. De ogen zijn 2×2 en minder sprekend dan in het model; het verre oog verschilt maar één pixel van het nabije.
- **Vuistarm:** donkerder dan in ronde 1 (volgt het model), waardoor de vuist minder opvalt.

## Lessen
- Een waardekaart van het model per 64-pixel (4 klassen op kwantielen van de vachtpixels) is een snelle gids voor licht en schaduw, maar letterlijk overnemen geeft ruis en te veel D. Daarna met de hand banden trekken en D alleen als sikkel gebruiken.
- Rond een rechthoekig gat lezen lichte hoekpixels (en alleen de zijkanten in omlijning) ronder dan een volledige donkere rand.
- Vingertoppen van 2 px lezen als vrij als de gloed of band op de hoekpixels boven de top doorloopt; de lijn tussen de vingers begint pas één rij lager.
