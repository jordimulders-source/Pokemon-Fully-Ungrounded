# Kudu sprite ronde 5 (maker)
Start: r4 (`r4/grid.json`, oog B). Model: `r3/model_A3.png`. Script: `sprite/r5.py`. Vel: `vel5.py`.
- Oog wisselen: `python3 r5.py A|B|C|D`.
  - `HOOFD='B'` bepaalt `kudu_r5.png`.
  - De andere varianten worden `kudu_r5_oog{A,C,D}.png`.
  - Het oogvlak wordt eerst voor alle varianten leeggemaakt (vacht/wit uit het model) en daarna gevuld.

Coördinaten in de keuring zijn beeldcoördinaten; hieronder staan **rastercoördinaten** (beeld x = raster x + 6, y gelijk). De tintnummers van de keurder zijn paletindexen: 1 = lijn 0, 2 = L, 3 = M, 4 = D.

## Per reparatie
1. **Manenlokken** (raster x9-29, rij 25-46). De lok- en kamregel van r4 (87 + 41 px) is weg.
   - Tint per cel komt uit de box-reductie van het model: gemiddelde helderheid van de haarpixels zonder lijnpixels. l ≥ 135, m ≥ 112, anders d.
   - Strenglijn d staat alleen waar het model een lijn heeft: cel met ≥ 28% modellijn die samen met buurcellen een lijn van ≥ 3 cellen vormt. Losse lijncellen krijgen haartint.
   - Netheid:
     - 1-px-wisselingen l|m|l in een rij (modeltextuur smaller dan 2 px) krijgen de tint van beide buren: 15 px.
     - Vlakjes < 3 px gaan naar de buurtint: 16 px.
   - Resultaat: de massa is licht linksboven en donker rechtsonder, met strengen op de modellijnen.
2. **Hals.**
   - **Gemeten:** het kanaal is in het model 2 cellen breed 100% vacht (185,145,63; lum 147). Het ligt op x13-14 rij 29-34, schuift naar x14-15 op rij 35-36 en naar x15-16 op rij 37-38.
   - **Gedaan zoals de keurder vroeg:** 1 px vachtlijn in M op de linkerste kolom met ≥ 75% vacht: (13,28-34), (14,35-36), (15,37-38), 11 px. Dat omvat de gemeten punten van de keurder.
   - De rest van het kanaal krijgt de haartint uit het model (lum 147 → l/m).
   - **Afwijking van het model:** de vachtstrook is daar 2 px. De tweede kolom is nu haartint, omdat beide kleuren in het model bijna even licht zijn.
   - **Leest de nek?** Kaaklijn + lichte schuine lijn van onder de kaak naar de borst. Op 8x leest de hals beter dan in r4 (geen bruine band meer), op 1x subtiel.
3. **Flank** (x35-41, rij 32-41): L wordt M (15 px). L blijft alleen in rij 32-33 waar het model ≥ 181 geeft. De strepen zijn niet veranderd.
4. **Kam.**
   - Model op halve cellen: punten op (25-26,25), (27-28,26) en (29,27). De inkepingen ertussen zijn kleiner dan 1 px.
   - (29,27) en (29,28) ontbraken (28% / 75% voorgrond) en zijn erbij gezet.
   - Onder twee punten loopt in het model een lijn terug de massa in; die staat nu als d op (25,26) (50% lijn) en (27,27) (38%). (28,27) (27%) is buitenlijn gebleven.
   - Echte inkepingen passen niet op 1 px; het profiel is nu een trap van punten met lijnen eronder.
5. **Buiksikkel** (rij 43-45, x28-39): vachttint uit het model met D < 150 (was 160). Geeft een gebogen grens uit de modelhelderheid: in het midden ligt de grens een rij lager dan bij de poten (5 px).
6. **Belijning.**
   - **Oren:** de selout aan de lichtkant is goud D in plaats van roze r (rand in modelgoud).
   - **Linkerrand linkeroor** (1,20) en (1,21): selout D.
   - **Niet uitgevoerd: rij 22, x2-5.** Dit is de onderrand van het oor, die recht omlaag wijst. Bij licht linksboven is dat de schaduwkant; SPRITE_KERN: zwart aan de schaduwkant. Graag oordeel van Claude/de keurder.
7. **Oog:** niet aangepast. Variant B staat erin; wisselen met het argument.
8. **Linkerhoorn middenstuk.** Lichte voorkant 4 waar het model ≥ 20% licht heeft in of naast de cel:
   - rij 7-9: rechterkolom x9 (licht ligt in het model bij x9-10);
   - rij 10-11: linkerkolom (7,10) en (6,11) (licht bij x5-7).
   - 5 px. De draai wisselt dus van kant, zoals in het model.

## Pixels (telling.txt)
**T.o.v. de kale reductie van model A3: 600 van 1362 px.**

| Zone | Pixels |
|---|---|
| vacht | 202 |
| manen | 153 |
| staal | 137 |
| lijn | 83 |
| oog | 11 |
| donker | 11 |
| roze | 3 |

**T.o.v. r4: 169 px.**

| Zone | Pixels |
|---|---|
| manen | 122 |
| vacht | 39 |
| staal | 5 |
| oog | 2 |
| lijn | 1 |

De 2 oog-px komen van het leegmaken van het oogvlak voor alle varianten.

## Niet uit het model (benoemd)
- **streep (15) en ontkorrel (16):** netheid; tint van de buren, geen middeling.
- **Halslijn:** 1 px breed in plaats van de gemeten 2 px (keurder).
- **Oorselout D en linkeroorrand:** de kleur volgt de keurder ("goud uit het model").
- **Oog:** Ponyta-pixels (variant B).
- **Uit r3/r4 ongewijzigd:**
  - poten volgens Kirlia
  - hoeven volgens de impala
  - flankstrepen
  - hoornband
  - kaaklijn
  - de buitenlijnregel buiten kam en oren

## Eigen zwakke punten
- De hals leest op 1x nog subtiel. Een tweede M-kolom (de gemeten 2 px) zou hem duidelijker maken, maar dat gaat tegen de keurder in. Dit is een keuze voor Claude/Jordi.
- De kampunten zijn trappen, geen echte punten met inkepingen; dat past niet op 1 px.
- Het midden van de manen (x14-24, rij 31-38) is een vrij groot l-vlak, licht linksboven volgens het model. Daar zitten weinig strengen, omdat het model daar weinig lijnen heeft die ≥ 28% van een cel vullen.
