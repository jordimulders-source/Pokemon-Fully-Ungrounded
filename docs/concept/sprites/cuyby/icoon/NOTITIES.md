# Cuyby-icoon (proefrit bak C, 28 nov)

Af: `af/icon.png` (32×64, 2 frames, modus P, index 0 transparant), `af/icon_8x.png` (front 4× | frame 1 en 2 op 8× | 1× en 2× tussen pikachu, dedenne, pachirisu en rattata), `af/icon_anim.gif`.
**Palet: pal0** (`.iconPalIndex = 0`). Bouwscript: `schrap/schrap.py` (`python3 docs/concept/sprites/cuyby/icoon/schrap/schrap.py s8B` = af).

## Onmisbare kenmerken (vooraf opgeschreven)
1. **Driekleurige vacht:** zwart linksboven (met het linkeroor), oranje rechterhelft (met het rechteroor), crème/wit gezicht en onderkant, met een crème bles van boven tussen zwart en oranje.
2. **Twee kleine ronde oortjes** bovenop, ±3 px boven de kop (regel 2 + 0,29 × 3), met roze binnenkant; zwart oor 1 px hoger dan oranje.
3. **Grote glanzende ogen**, laag in het ronde lijf, het linker in het zwart. Opbouw (front): zwart blok 5×6, witte glans 2×2 linksboven, bruine onderglans onderin; in het icoon 4×4 (min. 1 + 0,26 × 5 = 2,3).
4. **Rond bolletje zonder zichtbare poten**, rafelige crème franje onderaan met roze voetkussentjes; roze neusje.

## Werkwijze (na Jordi's verbod op zelf tekenen)
Elke pixel is een frontpixel: frame 1 van de front met **rijen en kolommen geschrapt** (bewaard: kolommen 16,17,19,20,21,23,24,26,27,28,30,31,33,34,36,38,40,42,44,46; rijen 15,16,18,19,20,22,24,26,28,29,31,33,34,36,38,40,42,44,45,46). Factor ±0,6 (kop ×1,15 t.o.v. gewone verkleining 0,53); het oog verschuift niet binnen de kop. Doelhoogte front 33 → 17 (±3): 20. Breedte 19.
Kleur = dichtstbijzijnde pal0-index, met twee benoemde afwijkingen hieronder.

### Ingrepen na de reductie (alle automatisch in `schrap.py`, gelogd bij het draaien)
| Ingreep | Waar | Soort |
|---|---|---|
| bungelende randpixels (≤ 1 buur) weg, 8 px | franje onderaan, rechterrand | losse pixels weghalen |
| 2 schaduwspikkels (lichtroze 11) midden in crème → crème | gezicht | losse pixels weghalen |
| 20 lichte randpixels → omlijning (15 boven, 14 onder) waar de geschrapte front-omlijning (1, 5) ontbrak; roze kussentjes/oortjes uitgezonderd | linker- en onderrand, oren | omlijning sluiten |
| oranje front-omlijning 9 (148,57,0) → 15 i.p.v. dichtstbijzijnde 6 (licht oranje): anders valt de hele rechterrand open | rechterrand | omlijning sluiten |
| **zwarte vacht** front 11 → 14 en vachtglans 10 → 1 (dichtstbijzijnde zou 15 en 14 zijn) | zwarte vlek | **afwijking van "dichtstbijzijnde", ter keuze** |
| frame 2: alles t/m y26 1 px omlaag, rij 27 vervalt, y28-29 blijven; oranje oor als geheel op zijn plek (spitst 1 px) | — | onderdelen als geheel verschuiven (stap 7) |

**Keuze A/B voor Jordi (zwarte vacht):** strikt dichtstbijzijnd (`schrap/variant_A_strikt.png`) maakt vacht = omlijning = oogzwart (15); dan verdwijnt het linkeroog in de zwarte vlek (alleen de glanspixel blijft) en zijn de oortjes vlakken. Af = B: vacht 14 met glans 1, precies zoals Game Freak Houndour (ook pal0) doet; beide ogen blijven leesbaar.

## Controle
`icoon_check.py`: **15/17 OK.** Niet OK: *niet hoekig* (0,61) en *rond* (34,4). Terecht: de front zelf is een afgerond vierkant met rechte zijkanten; alleen het frontsilhouet al verkleind naar 19×20 scoort 0,37 recht, dus zonder vormen te tekenen (verboden) haalt geen reductie dit. Alle andere checks OK (palet pal0, hoogte 20, onderkant 29, midden 16,0, 7 kleuren, omlijning 0,98, binnenlijnen 0,24, vlakken 12, frame 2 0,11, pose-IoU 0,91). `vorm_meet.py`: compact 0,98, vlakken 12 (front 28), geen gaten.
Eis 0 (zelf op 8× en 1× bekeken naast de front en knaagdier-iconen): driekleur met bles, twee oortjes met roze, twee ogen met glans, neusje en franje met kussentjes zijn er; leest op 1× als Cuyby. Zwakke punten: de zwarte vlek is gespikkeld (de randglans van de front valt verspreid), de bles boven krijgt een lichtroze plek (front licht oranje 6 → dichtstbij lichtroze 11), en de franje is maar 2 rijen. Geen verse keurder gedaan (geen agent beschikbaar in deze proefrit).

## Rondes en moeite
- **Rondes:** 7 getekende rondes (`poets/r1–r7`, 17/17 checks) zijn **verworpen** na Jordi's nieuwe regel (zelf tekenen verboden); daarna 8 reductierondes (`schrap/s1–s8B`). Onderlaag via de onderdelen-methode met meerderheidskleur: `onderdelen/bouw.py` (a1; oog viel weg tot een streep, niet gebruikt).
- **Wat moeite kostte:** (1) het oog: elke middelende verkleining verliest de 2×2-glans; alleen rijen/kolommen schrappen houdt het oog intact (kies de rij met glans en de rij zonder bruine onderglans, anders wordt die rood: front-bruin → 6). (2) De paletregel: pal0 heeft geen crème, geen bruin en geen echt zwart naast de omlijning; strikt dichtstbij geeft perzik-schaduw en een zwarte vlek die met omlijning en oog samenvalt. (3) De hoekigheidschecks zijn bij een vierkante front zonder tekenen niet te halen.
- **Wat bak C sneller maakt:** een vast script "rijen/kolommen schrappen + dichtstbijzijnde kleur + automatische opschoning (los weg, omlijning dicht)" zoals `schrap.py`, met alleen de keep-lijsten per soort als invoer (oogrijen eerst kiezen); vooraf per palet beslissen hoe front-zwart en front-omlijningskleuren (zoals oranje 9) vallen; de hoekigheidschecks laten meten tegen het verkleinde frontsilhouet in plaats van een vaste norm.
