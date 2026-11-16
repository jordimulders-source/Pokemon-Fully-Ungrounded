# Viscacha (Zapacha) frame 2: notities (16 nov)

Bron: `../gemini/frame2_ronde1.png` (Gemini-bewerking van de 8×-sprite), frame 1 `../af/viscacha.png` (bevroren, alleen gelezen; sha256 voor en na gelijk, assert). Script: `maak_frame2.py` (draait opnieuw met `python3 maak_frame2.py`).

## Werkwijze
1. **Overnemen:** middelste pixel per 16×16-vak (`a[8::16, 8::16]`), dichtstbijzijnde kleur uit het palet van frame 1, wit → index 0 → `gemini64_ruw.png`. Controle: de modus van het binnenste 8×8 per vak wijkt maar op 10 vakken af van de middelste pixel; middelste pixel aangehouden.
2. **Zones:**
   - *Vast* (alles buiten x 0–35, y 14–52: lijf, achterpoten, staart, staartpluim): Gemini wijkt hier op **0 px** af van frame 1; toch expliciet frame 1 ingezet (assert: diff 0).
   - *Bewogen* (kop, oren, snuitpluk, wangpluk, open bek, voorpoten tegen de borst, borstlijn): uit Gemini. 592 px anders dan frame 1. De onderste voorpoot van frame 1 (rij 50–52) is weg, want de poten zitten nu tegen de borst.
3. **Snorharen:** Gemini's stompje (8 px index 15, x ≤ 6, rij 24–27) weg. De 37 snorhaarpixels van frame 1 als groep verschoven met **(dx 0, dy −11)**, geen rotatie: de snuit staat 11 rijen hoger en die verschuiving valt precies samen met Gemini's stompje. Vorm en aantal gelijk aan frame 1 (assert). Linkergroep loopt over de lucht zoals in frame 1; de rechtergroep loopt vanaf de mondhoek over de wang onder het oog.
   - Let op: 7 pixels van de rechtergroep vallen nu over de gele wangpluk (frame 1: eronder), omdat de pluk minder meebewoog dan de snuit; 1 pixel (7,26) ligt op de linkerrand van de gele snuitpluk. Niet opgelost (zou de vorm van de snorharen veranderen); punt voor de keuring.
   - De grijze pixel (11,25) in de open bek is tandschaduw uit het model (index 15, maar geen snorhaar); blijft staan.
4. **Technische opschoning (6 px):**
   - (23,21) en (11,38): wit dat aan de rand doorschemert (achtergrond) → transparant.
   - (12,21), (13,21), (25,21), (9,24): buitenlijn in `e` (anti-aliasing) → selout `2`, zoals frame 1. Assert: buitenrand alleen in 1, 2, 8 en 15, net als frame 1.
   - Verder niets aangeraakt: de 1-px tintjes in kop en poten komen uit het model en blijven (overnemen, niet hertekenen).

## Afwijking van de kale reductie
37 px in totaal (`wijzigingen.txt` per pixel): snorharen (stompje weg, haren van frame 1 erbij; deels overlappend) en 6 px opschoning. Bek-binnenkant (roze/donkerrood in Gemini) is naar het palet gebracht (`e`, `c`, `1`, `d`): er zit geen roze in het palet van frame 1.

## Uitvoer
`viscacha_frame2.png` (64×64), `viscacha_anim_front.png` (64×128, frame 1 boven, frame 2 onder, palet van frame 1), `vel.png` (frame 1 | Gemini ruw | frame 2, 6×), `viscacha_frame2.gif` (700/250 ms, 6×), `gemini64_ruw.png`, `wijzigingen.txt`.
