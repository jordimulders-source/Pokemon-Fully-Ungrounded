# Gnometrotter Rock: sprite r6 (23 nov)

**Basis = r5** (koerswijziging Jordi: "hij is niet slecht hoor, maar het wijkt veel meer af van het model dan nodig is. Ga niet dingen opnieuw bouwen die niet nodig zijn, gebruik al wat je hebt, maar het moet beter. Het kleurgebruik is grotendeels wat beter al, maar je hebt vaak wel minimaal 3 kleurtinten nodig voor perspectief" · "de maker moet gewoon nooit opnieuw tekenen tenzij expliciet verzocht").
Alleen de onderdelen die in vorm afweken zijn teruggezet naar de verkleining van het model: **haar L, haar R, baard, riem, broek (dijen + voetballen), schouderovaal rechts en arm R**. Muts, neus, lijf (behalve het schouderovaal), arm L/vuist, hand R, stok en zolen zijn r5 gebleven. Niets getekend.

Leveringen: `gnometrotter_rock.png` (64×64, P, palet byte-gelijk aan r5), `gnometrotter_rock_8x.png`, `naast_model.png` (r6 | model, 8×, zelfde uitsnede), `stap2.png` (= r6).

## Werkwijze (scripts in deze map)
1. `reductie_gedeeld.py` op `r8/gemini_r8.png` → `red_r8_kaal.png`: **identiek aan `sprite/kaal.png`** (0 px verschil); silhouet = r4 op de 8 stokpixels na (drempel 0,35, zoals GEDEELD.md).
2. `meet6.py`: per spritepixel uit het model (gedeelde geometrie) de dominante familie/zone, het lijnaandeel (zwart of onder de familielijndrempel: roze < 115, blauw < 112, licht steen < 100, donker steen < 60) en de helderheid van de vlakpixels.
3. `r6.py`: r5 als onderlaag; in de doelzones per pixel:
   - **lijn** waar het model lijn heeft (lijnaandeel ≥ 0,45, of ≥ 0,18 en lokaal maximum = 1 px op de pixel met de meeste modellijn), in de donkere eigen tint (steen 2, licht steen 4, roze 6, blauw 9; zwart alleen bij ≥ 0,8);
   - anders **tint uit de gemeten modelhelderheid**, 3 tinten: steen 3/4/5 (< 110 / < 140), licht steen c/d/e (< 160 / < 196; het modelvlak van de baard, 193, valt zo in het midden d), roze 7/8/f (< 155 / < 178), blauw 9/a/b (< 124 / < 145), riem 3/4/5 (< 112 / < 131: gemeten lichte bovenkant 133–151, onderkant 95–110);
   - de **buitenrand bleef r5** (silhouet en omlijning bevroren);
   - **ring**: 1 px rond de teruggezette delen (in r5-onderdelen) krijgt lijn waar het model daar lijn heeft (41 px; o.a. omlijning boven haar R tegen de muts, onderrand van de voetballen op de zolen);
   - **ruis**: vlakjes < 3 px van één index gaan op in de buurkleur van hetzelfde materiaal; losse pixels idem (twee 1-px hooglichten in het haar bewust gehouden, zoals r5).
4. `controle.py`: levert af en telt.

## Controles
- Silhouet: **alpha-diff 0 met r5 en met r4.** Palet gelijk aan r5.
- Losse pixels (8-buren): 2, beide bewust hooglicht e in het haar ((15,15) haar L, (38,17) haar R).
- Tinten per onderdeel (+ lijn): haar L/R c/d/e + 4; baard c/d/e + 4; riem 3/4/5 + 2; broek 9/a/b (9 is ook de lijnkleur: blauw heeft in het gedeelde palet maar 3 indexen); schouderovaal 7/8/f + 6.

## Afwijking per onderdeel (pixels)
| onderdeel | ≠ r5 | ≠ kale reductie | (r5 ≠ kaal) | niet uit het model |
|---|---|---|---|---|
| muts+rugkam | 11 | 185 | 185 | 0 (ringlijn haar R + 1 ruis) |
| haar L | 6 | 26 | 24 | 5 ruis |
| haar R | 28 | 24 | 24 | 8 ruis |
| baard | 84 | 96 | 108 | 21 ruis |
| neus | 0 | 22 | 22 | 0 |
| lijf | 59 | 184 | 193 | 14 ruis (schouderovaal + ring) |
| arm L+hand | 1 | 54 | 54 | 0 |
| arm R | 4 | 22 | 21 | 3 ruis |
| hand R | 0 | 31 | 31 | 0 |
| riem | 128 | 86 | 136 | **58 gesp-vervanging** + 17 ruis |
| stok | 0 | 66 | 66 | 0 |
| broek/benen | 130 | 115 | 190 | 12 ruis |
| zool L | 8 | 50 | 50 | 1 ruis (ringlijn onder de voetbal) |
| zool R | 5 | 48 | 47 | 0 (ringlijn onder de voetbal) |
| **totaal** | **464** | | | |

"≠ kale reductie" telt ook pixels die alleen in kleurindex verschillen (de kale reductie kwantiseert op het hele palet, dus een lijn of tint in een ander materiaal telt mee); de teruggezette onderdelen liggen nu dichter bij de reductie dan r5 (baard 96 i.p.v. 108, riem 86 i.p.v. 136, broek 115 i.p.v. 190).

**Pixels die niet uit het model komen:**
- **Gesp weg (Jordi: "je mag de gesp trouwens bij rock en ijs weglaten"):** 58 px, gesp in het model x 22–31, y 37–42 (+ onderrand x 26–29, y 43). Per rij het riemprofiel van kolom 33 (eerste schone riemkolom rechts); de 4 px op y 43 kregen de blauwe waarde eronder (y 44).
- **Ruis**: 86 px samengevoegd met hun eigen vlak (lijst per pixel in `bron.pkl`, code 'R').
- Verder niets: alle andere gewijzigde pixels zijn modellijn (138 + 41 ring) of modeltint (522).

## Per onderdeel (vorm t.o.v. het model)
- **Baard:** het schild met zigzag van r5 is weg; nu de hangende baard uit het model: licht vlak d met de donkere strengen (c) en de V-inkeping uit het model, lichte strepen e, punten onderaan boven de riem.
- **Haar L / R:** uit het model, c/d/e met lijn 4; haar R heeft nu de omlijning tegen de muts. De spitse uitsteeksels zijn op 1/8,1 maar deels zichtbaar (haar R leest nog als kleine wolk; de zaagtanden van het model vallen tussen de pixels).
- **Riem:** model-breedte (lijn, 3 tintrijen 5/4/3, lijn) en buigt mee (links hoger, rechts omhoog naar de flank); gesp weg.
- **Broek:** twee dijen met de naden uit het model, opening ertussen (silhouet), voetballen in b met 9-lijn tussen dij en bal en onder de bal.
- **Schouderovaal R / arm R:** opnieuw uit de meting; verschilt weinig van r5 (bovenvlak f, midden 8, rand 7, lijn 6).

## Eigen kanttekeningen (zwakke punten)
- Haar R is geen duidelijk spits blad; de punten van het model zijn kleiner dan een spritepixel.
- De broek heeft meer 9 (schaduw + naden) dan r5; de naden zijn wat korrelig, omdat 9 tegelijk lijn en schaduw is.
- Het schouderovaal heeft geen gesloten omlijning (de dikke modellijn valt verdeeld over twee pixels).
