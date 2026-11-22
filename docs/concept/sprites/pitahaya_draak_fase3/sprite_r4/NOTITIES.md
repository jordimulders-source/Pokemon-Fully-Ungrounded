# Pitahaya-draak fase 3, sprite r4 (maker): benoemde reparaties op r3

Basis = `../sprite_r3/pitahaya3_r3.png` (+ `_zonder_tong.png`). Script `maak_r4.py`, log per pixel en stap in
`pitahaya3_r4_afwijkingen.txt` en `pitahaya3_r4_zonder_tong_afwijkingen.txt`.
```
python3 maak_r4.py ../sprite_r3/pitahaya3_r3.png pitahaya3_r4.png
python3 maak_r4.py ../sprite_r3/pitahaya3_r3_zonder_tong.png pitahaya3_r4_zonder_tong.png --zonder-tong
python3 ../sprite_r2/controle.py pitahaya3_r4.png ; python3 vel.py pitahaya3_r4.png pitahaya3_r4_zonder_tong.png vel.png
```
Nieuw meetgereedschap: `vlees.py` (vruchtvlees-/zwart-/achtergrondfractie per spritepixel), `ribben.py` (lange donkergroene
modellijnen → skelet → spriteraster), `lijf4.py` (lijfvulling r4), `proef2.py` (4 ribinstellingen naast het verkleinde model).

## Stand
- 1797 px (zonder tong 1780), silhouet = r3 op 2 px na ((11,13) en (10,14): `masker.py` alleen sprite, model achtergrond). 16 kleuren (zonder tong 13), palet ongewijzigd.
- Zwart binnen 2,8 %, buitenrand 48 %, dambord 0; losse pixels alleen tanden, pitjes, tongpunten en de klauwpunten van de voorhand.
- 306 px t.o.v. r3: bek 11, kopschubben 25, lijf 272 (incl. 5 opruimen). Met en zonder tong verschillen 27 px, buiten de bekzone (x 0-12, y 26-38) 0.

## Per punt
1. **Bek.** `vlees.py` op beide modellen: vlees ≥ 0,6 op (9-11,26), (8-11,27), (8-11,28), (9-10,29); de som van de vleesfracties is ±13 px, 4 rijen hoog (rij 26-29). r3 had 14 px op dezelfde plek. **Het oppervlak klopte dus al.** Wat het klein liet lijken:
   - het vlees was grijs (w);
   - de bovenlip was een zwarte balk van 5 px, terwijl het model daar 0-20 % zwart heeft (een lijn van ±¼ px op de rijgrens 25/26).
   Nu is de bovenlip (8-12,25) een dunne donkerroze lijn en het vlees helder wit, met 2 pitjes. Hoektanden: boven (13,25); onder met tong (8-9,31), zonder tong (6,30-31), (8,31) en (9,31), zoals r3.
2. **Kopschubben.** Volgens de rasteruitsnede 30× en `klas.py` heeft het model drie hoorns aan de rand: boven (10,15)→(15,13), links (3,19)→(7,16) en achter (16,20)→(19,15). Binnen het silhouet liggen nog twee bladen: voorhoofd (10-12,19)→(12,18) en wang (16-18,21-23). Ze staan er dus echt, maar met een donkere onderrand.
   - Elk blad heeft nu een lichte kant (h) en een donkere rand en punt (g); de punt is 1 px scherp.
   - (15,16) en (16,16) zijn weer roze: het model heeft daar geen groen.
   - De hoorns steken uit het silhouet zoals in het model. Verder uitsteken zou buiten het modelsilhouet vallen.
3. **Lijf** (`lijf4.py`).
   - Vulling vooral middengroen h.
   - Schaduw G voor de laagste 30 % van de volume-toonkaart uit r3 (rechtsonder en onder de rugrand).
   - Licht H alleen binnen 2 px van een boven- of linkerrand: nek, rug, staartbovenkant.
   - Ribben g: skelet van de lange donkergroene modellijnen (lum < 80, ≥ 25 natieve px), op spriteniveau verdund tot 1 px; stukjes < 4 px zijn weg.
   - Overlay op het model (`../sprite_r2/overlay.py`): de ribben liggen op de modelribben van nek, dij en staart, met evenwijdige strepen langs de staart.
   - Toonclusters < 3 px en losse groentonen gaan naar de meerderheid van hun buren.
4. **Zelf genoemde punten.**
   - Rugstekels: blijven op modelhoogte (2 px boven het roze). Langer zou buiten het modelsilhouet vallen.
   - Nabije hand: blijft 2 klauwen. De 3-4 modelvingers (x 29,2 / 30,8 / 32,3 / 33,9) passen op 64 px alleen als H#H#H#-streep, en die werd in r2 juist afgekeurd.

## Zwakke punten
- Bek: het oppervlak klopt, maar de modelbek leest groter door de dunne zwarte omlijning. De onderlip/onderkaak (6-12,30-33) is nog donker en druk (tong, tanden, lijnen).
- Lijf: de ribben zijn hier en daar hoekig, bijvoorbeeld onder de borst (y 33-35), en de buikrand (y 46-49) leest als franje van ribuiteinden.
- Lijf: het lichte vlak op de nek onder de rugrand (x 25-32, y 24-26) blijft vrij groot.
- De nabije bovenarm/onderarm is in het model een duidelijke vorm met zwarte omlijning. In de sprite valt hij nauwelijks op, omdat het model daar alleen dunne donkergroene lijnen heeft (`ribben.py`, zwart-skelet ≥ 20 px, geeft er niets).
