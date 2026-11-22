# Pitahaya-draak fase 3, sprite r2 (maker): benoemde reparaties op r1

Zelfde opzet als r1 (natief raster 3,998 → reductie S 3,661 → regels), script `maak_r2.py` (r1-pijplijn + r2-stappen). Model = overnemen: elke gewijzigde pixel staat met stap in `pitahaya3_r2_afwijkingen.txt`; handpixels met meting in de lijst `R2` in het script. `r1.png` = vorige ronde ter vergelijking (587 px verschil).

```
python3 maak_r2.py kaal.png natief.png pitahaya3_r2.png
python3 maak_r2.py kaal_zonder_tong.png natief_zonder_tong.png zonder_tong_pijplijn.png
python3 zonder_tong.py pitahaya3_r2.png zonder_tong_pijplijn.png pitahaya3_r2_zonder_tong.png   # assert: buiten x 0-12, y 26-38 diff 0 (29 px anders)
python3 controle.py pitahaya3_r2.png ; python3 vel.py
```
Meetgereedschap nieuw: `meet.py` (per spritepixel achtergrond/zwart/groen-fractie + helderheid groen), `raster.py` (model met spriteraster), `print.py` (sprite als tekstraster), `stekels.py` (stekel-/klauwpunten uit het model).

## Maat, palet, metingen
- 61×50 px, 1801 px (zonder tong 1784), x 1–61, y 13–62. 16 kleuren incl. transparant (zonder tong 13).
- **Palet = teju-sprite (fase 2, af)** voor zwart, roze (104,24,56) (177,40,84) (231,78,123) (248,160,192), groen (48,88,48) (79,128,64) (120,168,80) (176,208,104), vlees (191,189,192) (237,234,237), pit (44,42,46). Tong blijft modelgeel (122,100,25) (203,175,83) (250,222,143). Vultonen: groen 50/40/10 %, roze 40/55/5 % (schaduw/midden/licht), licht linksboven uit de modeltoonkaart.
- Zwart binnen de figuur **2,8 %** (r1 8,3 %); buitenrand 45 % zwart (Gen 3 45–68 %; lichtkant-drempel 0,4). Dambord 0. Langste recht randstuk 9 px (bovenkant staart rij 57, model).

## Per reparatie
1. **Kop** (zone x ≤ 21, y ≤ 34, roze):
   - zwart alleen in de bek-/kaakzone (x 1–15, y 25–34) voor modelcomponenten ≥ 15 px. Overige kopnaden worden donkerroze en alleen gezet als de modellijn ≥ 15 skeletpx lang is. Daardoor zijn de losse zwarte streepjes op voorhoofd en wang weg.
   - Bracteeën op kop, rug en knots: `BR` (groene modelcomponenten los van het lijf, ≥ 25 % van het venster) → lichtgroen, aan de achtergrond donkergroen.
   - Handpixels met meting: (3,27) zwart (40 %): de kaaklijn onder de snuit is dicht. (2,28) achtergrond (91 %). (3,28) tand 1 wit (model x 24–26, y 102–106; < 1 px). (5,25) neusgat donkerroze (22 % zwart). (11,29) zwart (35 %): bekhoek. (10,30) zwart (31 %): onderlip-lijn, scheidt vruchtvlees en tong van de onderkaak.
   - Opbouw nu, van boven naar onder:
     - bovenkaak met kaaklijn (2–7,27) en (8–12,25), met tand 2 (6,27) en hoektand (13,25);
     - vruchtvlees (8–11,26–29), grijs bovenin, met 2 pitjes;
     - onderlip-lijn (10,30)+(12–16,30);
     - onderkaak (7–10,31–32) met tanden;
     - onderrand (7–9,33).
2. **Lijnkleur lijf:** zwart alleen voor natieve zwarte componenten ≥ 30 px (structuurlijnen nek/borst/arm en de staartranden); alle andere lijnen in het lijf en de ribben zijn donkergroen. Op romp en nek wisselt zwart/donkergroen niet meer af.
3. **Rugstekels:** `stekels.py` vindt 6 rugpunten in het model. Het stuk voet→punt wordt geprojecteerd: de punt donkergroen, de voet lichtgroen het roze in (`SP` + `BR`, 108 px).
4. **Handen/klauwen:**
   - **Voorhand:** 2 lichte klauwen (10,44) en (12,44) (lum 101/98 tegen de hand 80–95), met lijnen (11,44) en (13,44) (48 %/42 % zwart), klauwpunten (10,45) en (12,45) zwart, inkeping (11,45) achtergrond, en (12,46)/(13,45) achtergrond (66 %/82 %). Het model heeft 3 klauwen; op 64 px passen er 2 met een inkeping.
   - **Nabije hand** (x 27–35, y 44–48): zwart wordt donkergroen bij ≥ 30 % zwart (rij 46–48 ≥ 25 %), anders groen naar de modelhelderheid, met lichte punten onderaan (lum ≥ 90). Rij 47 leest H H g H g H H g H: 4 klauwpunten met lijnen ertussen.
   - **Voeten:** de achtervoet zit in het model achter de knots en heeft geen zichtbare klauwen (`raster.py`, x 18–34, y 44–58). Daar is dus niets toegevoegd.
5. **Palet:** teju-tinten, zie boven.
6. **Opruimen:**
   - De losse vulpixels (30,47) en (20,58) zijn weg. Er is een losse-pixel-pass na de dambordstap. Wat overblijft aan losse pixels hoort bij oog, tanden, pitjes, tongpunt en klauwpunten.
   - Staartonderkant rij 62: alleen nog x 40–45 (6 px), uiteinden 1 px hoger.
   - Staart rechts kolom 61: (46),(47),(54),(55) weg (achtergrond 42/9/12/44 %), nu 6 px recht.

## Tong
Ongewijzigd t.o.v. r1: 26 px, vork (1–4,35–37), modeltinten.

## Zwakke punten (eerlijk)
- **Kop leest op 1×–2× nog als ronde roze massa:**
  - de snuit steekt wel uit (x 1–7, y 24–27), maar het model haalt zijn vorm uit een dunne zwarte omlijning en anti-aliasing die op 20 px niet overkomen;
  - het voorhoofd (x 4–9, y 15–21) is een groot vlak met een lichtroze vlek.
  Volgende stap zou een expliciete keuze zijn: de snuitbovenrand zwart in plaats van selout, of het lichtroze naar de snuitrug.
- **Rugstekels:** nog korte punten (1–2 px boven het roze); de modelstekels zijn smaller dan een spritepixel.
- **Nabije hand:** leest als gestreepte lichte rand, nog niet als losse klauwen.
- **Tand 1** (3,28) hangt als enkel wit pixel onder de snuit.
- **Model zonder tong:** heeft daar geen wit (0 %), maar de tand is voor beide versies gelijk gehouden.
