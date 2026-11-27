# Guaraná fase 2, ronde 4 (maker): benoemde reparaties van de coördinator op r3

Bestanden: `guarana2_r4_A.png` (oogrand rechts/onder lijnrood), `guarana2_r4_B.png` (zwart), `normal.pal` (= r3, 16 kleuren), `vel.png` (r4A | r3A | model 8×,
trossen 12× naast het natieve model, 1× licht/donker + B), `voor_jordi_r4_8x.png` (A | B, wit).
Bouwen vanuit `guarana_fase2/`: `python3 sprite_r4/kaal.py && ZWARTRAND=1 python3 sprite_r4/bouw.py && python3 sprite_r4/bouw.py && python3 sprite_r4/controle.py && python3 sprite_r4/vel.py sprite_r4/guarana2_r4_A.png sprite_r4/vel.png sprite_r4/guarana2_r4_B.png`
(`acht.py a.png [b.png] uit.png` = snel 8×-plaatje; let op: twee sprites naast elkaar in één verkleind beeld bekijken gaf schijnverschillen, kijk per sprite).

## Reparaties
1. **Niet hoekig: buitenrand** (`glad.py` + stap 10 in `bouw.py`). Silhouet: masker licht vervaagd (gauss 0,8) en opnieuw op 0,5 gedrempeld, beschermd:
   dunne ranken/klauwtjes blijven, aantal delen gelijk, geen lusgat dicht. Daarna de hoekpixels van de buitenlijn weg (dubbele pixel in een schuine lijn).
   Alles binnen ±1 px van het model (alleen randpixels). Alpha-diff t.o.v. r3: **38 px**:
   - erbij (inhammen van 1 px dicht, 30): (46,20) (41,26) (21,27) (30,16) (34,18) (19,18) (50,19) (6,23) (31,17) (33,17) (51,46) (37,19) (41,47) (59,20) (35,13)
     (35,47) (4,19) (22,10) (45,37) (51,39) (44,30) (45,17) (9,16) (26,5) (50,20) (47,20) (26,33) (51,15) (22,44) (56,27);
   - weg (losse uitsteker, 1): (57,30); hoekpixels weg (7): (20,7) (58,15) (20,29) (56,32) (20,42) (57,47) (51,48).
2. **Rust in de stam** (`schaduw.py`): groene delen < 20 px samengevoegd met het deel waarmee ze de langste grens delen → de stam bestaat nu uit
   3 brede strengen (verticaal) en 4 (horizontaal lijf), elk als buis ingekleurd; groene lijn alleen nog waar twee strengen elkaar raken.
   Groene lijnpixels binnen één streng → vul. Vlakjes < 3 px → buurtint (stap 9).
3. **Blad in lobben**: in het natieve model zijn de lichte bladhelften (groen L≥112) losse langwerpige lobben. Per bladpixel: lichte lob → licht 8
   (hooglicht 9 midden in de lob aan de lichtkant), donkere helft/nerf → schaduw 7 (13 waar nog wat licht in zit), modelzwart ≥ 60 % → groene lijn 6;
   twee verschillende lobben naast elkaar → lijn 6. Linker en middelste cluster lezen nu als gestreepte lobben (licht/donker/lijn).
4. **Half dichte ogen M2, M3 (en L1, R4)**: ooglid = boog in schaduwrood 3 boven het wit (`.LLL.` met de hoek omlaag), ook in B; onderrand zoals de variant;
   pupil 1 px (lidk) of 2 px (lid) linksonder.

## Metingen (`controle.py`)
- 62×51, 16 kleuren incl. transparant. Lichte tint op de buitenrand: 0. Zwart aan de lichtkant: 0.
- Groene lijn 294 → 274 px, zwart 265 → 239. Anders dan r3A: 407 px (tros L 44, M 94, R 95, rest 188).

## Wat nog afwijkt naast dundragoon/skinguin (8×)
- Nog altijd veel drukker: de maatstaf heeft grote rustige vlakken, hier zijn vruchten (±6 px) en lobben (2 px) van nature klein, met veel lijn ertussen.
- **Rechter bladcluster** (x40–50, y16–22) leest nog als groene massa, niet als lobben (het model heeft daar op 64 px geen lichte lobhelften die overblijven).
- **Lussen/ranken** zijn 2 px breed en bestaan alleen uit lijn (groen links/boven, zwart rechts/onder): geen ruimte voor vulling; ze ogen wat blokkig.
- Randgladmaken was klein (38 px): de trapjes in de trossen zijn grotendeels vruchtbollen, die blijven bobbelig (zo zit het model in elkaar).
- Middelste tros blijft het drukst; de half dichte ogen lezen nu als rood lid + wit spleetje, maar zijn klein.
