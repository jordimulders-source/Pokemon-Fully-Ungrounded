# Hauntflare sprite v2 (maker, 15 nov)

Basis: `../basis/basis_64.png` (bevroren vorm). Niets getekend: elke pixel krijgt een paletkleur op zijn plek, gekozen uit de modelpixels (`../model/model_claude_natief.png`) die in die basispixel vallen. Uitzonderingen volgens de opdracht: Haunters ogen en mond 1-op-1 (Gen 3, frame 1, schaal 1,0).

## Reproduceren (vanuit de repo-root)
```
python3 docs/concept/sprites/hauntflare/sprite_v2/bouw.py   # -> hauntflare_v2.png, _8x, bouw_log.json (MOND9=11 of 15: mondvariant)
python3 docs/concept/sprites/hauntflare/sprite_v2/vel.py    # -> vel.png
python3 docs/concept/sprites/hauntflare/sprite_v2/meet.py   # controles
```
Hulpjes: `toon.py` (raster 10x naast de basis), `zoom.py` (gezicht 16x naast Haunter).

## Palet (15 + transparant, zelfde als r1)
0 transparant · 1 omlijning 24161a · 2 ring donker / Haunters donkere ooglijn 5a2a33 · 3 ring midden 8a4e55 · 4 ring licht b0747a · 5 bol-selout c8435b · 6/7/8 bol schaduw/midden/licht f04482/fa76a2/f8aec2 · 9 bol glans f9ccd8 · 10 donkerrood 9a2a22 (vlam-/handselout, mondopening) · 11 rood d84030 · 12 oranje f48659 · 13 geel-oranje f8b850 · 14 oogwit ffffff · 15 hand licht ee747c.

## Stappen en gewijzigde pixels (alles gelogd in `bouw_log.json`)
0. **Oud modelgezicht weg, in het model zelf** (99x99): 160 modelpixels (lijnen, mondrood, oogwitten in het gezichtsvak x25-46, y35-53 binnen de bol) opnieuw gevuld met het gemiddelde van hun bolburen, van buiten naar binnen (tintverloop blijft). Resultaat: `model_zonder_gezicht.png`.
1. **Groepen** in de basis: bol 761, ring 423, kuif 181, staart 169, handen 232 px; niets onbekend.
2. **Buitenlijn**: elke randpixel van de basis krijgt de randkleur die het model daar heeft (zwart, roze selout c8435b bij de bol, donkerrood bij vlammen/handen). Daardoor 1 px en dicht. **Binnenlijnen**: zwarte/donkerrode modellijnen op hun plek doorgezet (voorwaartse afbeelding model -> basis, zodat dunne lijnen niet wegmiddelen).
3. **Vulling**: bol = gemiddelde van de niet-lijnmodelpixels in de voetafdruk -> dichtstbijzijnde boltint; vlammen en handen = meest voorkomende modelklasse -> warmer (r1-regels: f8856c -> geel-oranje, e85f80 -> oranje, cb435a -> rood); ring = helderheid van de r4_c-ring per voetafdruk, 3x3 binnen de ring, drempels 15/80 % -> donker/midden/licht.
4. **Handen**: r4_a-kleurgebruik (r1-regel): 38 px oranje op de binnenrand van de bogen en onderranden.
5. **Gezicht**: Haunter x13-33, y28-45, 161 px, offset (+6, -8) -> v2 x19-39, y20-37. f -> oogwit, e -> zwart, 5 en d -> 5a2a33, Haunters donkere huid tegen het smalle oogwit -> c8435b, mond a en 9 -> donkerrood 9a2a22; tanden (Haunters huid in de mond) blijven bolroze = de V'tjes. Weggelaten: Haunters wang-/kaakomtrek (15,38), (33,37), rij 45 behalve de mondlijn (27-28,45), en zijn linkerhand (x<=14, y>=38). Plek: dichtst bij het oude modelgezicht waar alles op de bol valt, >=1 px van ring en rand, >=2 px bolroze links van het linker oog.
6. **Opruimen**: 64 px in tintvlakjes < 3 px (8-verbonden, binnen de groep, niet op rand/lijn/gezicht) -> buurtint; 2 randpixels om-en-om gelijkgetrokken.

## Controle (`meet.py`)
- Silhouet t.o.v. de basis: **0 eraf**, 10 erbij = het gat in de bol op x19-21, y20-24 (de witte glans van het model viel in `basis.py` als achtergrond weg; het buitensilhouet is ongewijzigd).
- 16 kleuren incl. transparant; geen lichte kleur op de buitenrand; buitenrand 100 % lijnkleur; geen om-en-om.
- Tintvlakjes < 3 px: 1 (24,32) = Haunters losse tand in de mond (hoort zo).
- `meet.py` meldt 8 plekken met zwart achter een zwarte rand: allemaal aansluitingen (vingerlijnen rechterhand, ring/kuif, ringonderkant), geen verdikte buitenlijn.

## Eigen zwakke punten (eerlijk)
1. De modelglans (wit, linksboven) ligt precies waar Haunters smalle oog moet: het Haunter-gezicht (21x18) is groter dan het modelgezicht (±17x14) en past alleen hoger en iets rechts (offset 9 px van het oude midden). De glans is daardoor grotendeels weg; de rest van de bol heeft alleen de lichte wervel.
2. Het smalle oog ligt op lichte boltint (8/9): wit tegen lichtroze, weinig contrast aan de linkerkant (bij Haunter ook zo, maar daar is de huid donkerder).
3. Mond: Haunters 2 mondtinten zijn allebei donkerrood geworden ("donkere mondopening"); de tong valt weg. Varianten: `MOND9=11` (rode tong) of `MOND9=15` (lichte tong).
4. Bol heeft 4 tinten + selout (glans/wervel f9ccd8 is breed, zoals r1) en de wervel geeft onrustige vlekken op 8x; de ring-voorkant heeft vlekkerige lichte stukken uit r4_c.
5. Ring rechts achter de bol: lijnen van het model rond kuif/ringgat geven een kluwen zwart/donkerrood bij x45-50, y23-28.
6. Palet vol (15 + transparant).
