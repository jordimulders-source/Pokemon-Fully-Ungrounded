# Eindkeuring r17 (16 nov, verse eindkeurder)

r17 = r16 opgeschoond met `sprite_r16/eind_moet.py`. Daarin staan alleen bestaande paletindexen en asserts: groen-diff 0, gezichtslijnen-diff 0, rij 0–19 diff 0, geen nieuwe index. Er zijn 127 px gewijzigd: 95 in de koeienvanger en 32 in de kop. Vel: `eindkeuring_vel.png` (8×: r17 | r16 | model; koeienvanger 12×: r17 | r16 | r14 | model natief; 2×/1× naast Gengar, Magcargo, Claydol, Forretress).

**Oordeel: FAIL.** r17 is iets beter dan r16, maar het is nog geen geslaagde eindversie voor Jordi.

## 1. Hoofdvraag (eerst op 1×/2×, dan 8×)
- **r17 vs r16/r14, koeienvanger: beter.** De korrel is weg. In r16 stonden 19 1-px-eilandjes en 4 losse zwarte pixels, in r17 nog 2 en 1. De roestband heeft nu een doorlopende zwarte V-lijn uit het model: per kolom staat de lijn op de rij met het meeste modelzwart, met een dip bij x13 (y49) en een kleine dip bij x19–21. Daaronder ligt een lichte plaatrand, alleen waar het model licht is. Op 2× lees je band → platen → spleten. r16/r14 lazen als puin.
- **Lijkt het op het model? Half.** Het model is één puntige kaak: diepe V-bovenranden met een dikke zwarte lijn, schuine naden die naar de punt linksonder waaieren en een middentand met een punt omlaag. r17 leest nog steeds als **een rij grijze blokken met zwarte gaten**:
  - de V is maar 2–3 px diep en de lichte rand loopt bijna horizontaal (y48–49, x15–24);
  - de middentand (x14–17) heeft geen zichtbare punt;
  - de spleten x8, x13 en x18 staan recht, niet schuin.
  Jordi's schets (V-randen, "<"-naad rechts) is dus nog niet gehaald.
- **Kop: niet opgelost.** Het bruin is goed van kleur: de mediaan in het model is (157,102,71) en index 8 is (154,101,72). Toch leest de kop niet als een bolle pompoen met licht linksboven:
  - de linkerhelft is grotendeels bleekgrijs (index 10/7, 84 px);
  - de schaduw die ik uit het grove model haalde (onderste kwart → 9) geeft vooral een donkere band onder de voorhoofdplaat (y24–28, x16–23), geen verloop van links naar rechts.
- **Naast Gen 3:** veel drukker dan Gengar en Claydol en het vult het hele vak. Op 1× lezen de grijns en de wielen goed, de koeienvanger is een donkere vlek.

## 2. Metingen (r16 → r17)
| | r16 | r17 |
|---|---|---|
| Kleuren | 13 | 13 |
| Kop-tinten 1/7/8/9/10/11/12 | 94/34/175/40/50/9/57 | 94/34/144/71/50/8/58 |
| Koeienvanger 1/7/8/9/10/11/12 | 89/2/14/53/22/55/32 | 95/0/12/38/32/68/22 |
| 1-px-eilandjes kop / kv | 3 / 19 | 2 / 2 (randselout (4,28), wigtop (4,44), (8,48), (7,54)) |
| Losse zwarte pixels | 1 / 4 | 1 / 1 ((25,31) en (9,45): beide bevroren gezichts-/grijnslijn) |
| Dambord (echt, niet diagonaal) | 3 | 1 ((21,51) 12/9) |
| Bijna-zwart totaal | 10,3 % | 10,5 % (Gengar ±7, Magcargo ±14) |
| Buitenlijn ijzer zwart | 47 % | 56 % (Gen 3: 45–68 %; selout 9/12 linksboven) |
| Contrast (lum) | 8→9 37, 10→11 46, 11→12 30 | gelijk |
| Licht linksboven | kop: nee (vlak 8); kv: ja | kop: zwak; kv: ja |

## 3. Wat er nog mis is (MOET, precies)
1. **Koeienvanger-vorm** (x3–25, y46–57):
   - de V-bovenranden moeten dieper en dikker, zoals in het model (natief ±2 px lijn), van (6,46) naar de punt bij (13,50) en terug naar (17,46);
   - de lichte bovenrand van elke plaat moet die schuine lijn volgen;
   - de naden x8, x13 en x18 moeten naar de punt linksonder leunen;
   - de middentand moet eindigen op een punt van 1–2 px op y56–57.

   Mijn script haalt dit niet zonder vormen te verzinnen. 0,744× is te grof voor het natieve model: de lijnen zijn daar ½–1 spritepixel. Voorstel: dezelfde ijskomeet-reductie (donkerste wint), maar met de V-lijn en de naden als **2-px-lijnen uit het natieve model getrokken (polylijn op natief.png, omgerekend)**. Laat dat door een maker doen met overlay-controle.
2. **Kop-volume:**
   - de bleekgrijze platen linksboven (10/7) maken de kop vlak en grijs. Het model heeft daar roze-lichte platen, maar kleiner en met bruin ertussen;
   - het verloop licht links → donker rechts/onder ontbreekt.

   Dit vraagt een makerronde op de kop met de toonkaart van het model. Opschoonregels lossen het niet op.
3. Ter info, bevroren: (25,31) is een losse zwarte pixel in het bruin. Volgens de definitie is het een gezichtslijn, maar het leest als een stip. Vraag aan Jordi of die weg mag.

## MAG
- (21,51) dambord 12/9; (8,48) en (7,54) eilandjes.
