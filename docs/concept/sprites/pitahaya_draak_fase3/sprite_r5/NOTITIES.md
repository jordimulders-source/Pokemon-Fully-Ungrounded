# Pitahaya-draak fase 3, sprite r5 (maker): reparaties van de keurder op r4 + buikvariant van Jordi

Basis = `../sprite_r4/pitahaya3_r4.png` (+ `_zonder_tong.png`). Script `maak_r5.py`; de log per pixel en stap staat in
`pitahaya3_r5_afwijkingen.txt`, `pitahaya3_r5_zonder_tong_afwijkingen.txt` en `pitahaya3_r5_buik_afwijkingen.txt`.
```
python3 maak_r5.py ../sprite_r4/pitahaya3_r4.png pitahaya3_r5.png
python3 maak_r5.py ../sprite_r4/pitahaya3_r4_zonder_tong.png pitahaya3_r5_zonder_tong.png
python3 maak_r5.py ../sprite_r4/pitahaya3_r4.png pitahaya3_r5_buik.png --buik
python3 ../sprite_r2/controle.py pitahaya3_r5.png ; python3 vel.py <tijdelijke map>
```
Nieuw meetgereedschap:
- `meet.py MODEL x0 y0 x1 y1` geeft per spritepixel de dichtstbijzijnde paletkleur van het modelgemiddelde, van de donkerste 25 % en de zwartfractie (0-9).
- `grid.py` maakt een modeluitsnede met het spritepixelraster naast de sprite.
- `kijk.py` toont sprites op 1×, 2× en 6×.
- `lijf5.py` is de lijfopruiming.
- `buik.py` maakt de buikzone en de pitjes.

## Stand
- Het silhouet is gelijk aan r4 (alfa-diff 0).
- Kleuren: 16 (zonder tong 13); palet ongewijzigd, dus nog steeds het teju-palet.
- Zwart binnen het silhouet 3,6 % (r4 2,8 %; komt van de armcontour). Buitenrand 48 % zwart. Geen dambord.
- Losse pixels zijn alleen nog tanden, pitjes, tongpunten en de 3 klauwpunten van de nabije hand.
- Met en zonder tong verschillen 27 px, allemaal in de bekzone (x 0-12, y 26-38); erbuiten 0.
- Afwijking t.o.v. r4 per zone (met tong, 180 px):

| zone | px |
|---|---|
| lijf | 78 |
| nabije arm | 63 |
| nabije hand | 22 |
| dij | 6 |
| keel | 6 |
| kop | 2 |
| verre hand | 2 |
| opruimen | 1 |

De buikvariant heeft daarbovenop 81 px.

## Per punt (keurder r4)
1. **Nabije arm en hand.** Met `meet.py` gemeten in het model (zwartfractie):
   - bovencontour elleboog: zwart op (29-31,35) en (32-33,36);
   - bovenarm tussen x 34-38: alleen een zwakke lijn, dus donkergroen (34-35,36) en (36-38,35);
   - achterrand: zwart op (39,35-37), (38,38-39), (37,40), (36,41-42), (35,43-48);
   - voorrand onderarm: zwart op (32,37-38) en (31,39), daarna donkergroen (31,40), (30,41-42), (29,43-45).

   De onderarm is licht: H langs de voorrand, dan h, en G als sikkel tegen de achterrand. Het lijf erachter (x 37-40) is G. De hand heeft 3 hangende klauwen: x30 en x32 op y45-47, x34 op y45-46. Ze zijn donkergroen g met een lichte punt h, de tussenruimte is G en de onderrand op rij 48 is zwart. De limoenpixels (31-32,43) en (31,44) zijn weg.
2. **Keel.**
   - De kaakonderrand (12-16,30) blijft een zwarte lijn van 1 px.
   - Het kaakscharnier loopt diagonaal (16,30), (17,29), (18,28); (16,29) is nu d en (18,29) g.
   - De nekvoorrand is 1 px zwart: (16,31), (17,32), (17,33).
   - Wat daarbinnen zwart was, is g of G geworden: (17,31), (18,32), (18,33), (19,33).
3. **Dijvoorrand.** Model D: g op (40,40-41), (39,42-43) en (38,44-45), daaronder het bestaande zwart (38,46-49). De rib op x45 (y41-50) blijft staan.
4. **Lijfribben** (`lijf5.py`).
   - g die niet op een lange modelrib ligt, wordt vulling.
   - G en h krijgen een modusfilter van 3×3 (2×), zodat er brede schaduwvlakken ontstaan in plaats van vlekken.
   - Ribben = het modelribskelet, alleen stukken van ≥ 6 px (8-samenhang).
   - In de borst en schouder (x 16-31, y 26-40) tellen alleen modellijnen van ≥ 60 natieve px; daar zaten de meeste korte stukjes. Elders ≥ 40 px, zodat de dijrib x45 en de staartstrepen blijven.
   - Toonclusters < 3 px gaan naar hun buren.
   - Proef 25/4, 40/6 en 60/6 naast elkaar op 1× en 6×: 60/6 in de borst is het rustigst.
5. **Verre hand.** (10,44) is nu g en (12,44) G. Het model meet daar G/g, geen limoen.
6. **Kop.** De 4-burencontrole vond twee losse lichte pixels: (2,25) P → p en (19,25) h → d. Volgens het model zijn het roze randen.
   - Kolom 13 (y15-19) is d en ligt op de zwarte flaprand van het model. Die is dus geen losse lichte pixel en blijft staan.
   - De pixels die controle.py nog als los meldt in de kop zijn tanden, pitjes en de tong.

## Buikvariant (`pitahaya3_r5_buik.png`; Jordi 17 nov: "Maak nog een extra versie ernaast waar de buik de kleur krijgt van het vruchtvlees. Dus wit met zwarte spikkels")
- Basis is de versie met tong.
- **Buikzone** (`buik.py`, `RIJEN`): alleen groene pixels (zwart blijft). Per rij x van-tot:

  | rij | x |
  |---|---|
  | 30 | 17-22 |
  | 31 | 17-23 |
  | 32 | 18-24 |
  | 33 | 18-25 |
  | 34 | 21-26 |
  | 35 | 22-26 |
  | 36 | 23-27 |
  | 37 | 24-29 |
  | 38 | 24-30 |
  | 39 | 25-30 |
  | 40 | 25-30 |
  | 41 | 25-29 |
  | 42 | 26-29 |
  | 43 | 26-28 |

- Dat is de buikkant van keel, borst en buik tussen de poten:
  - links/voor: de buitenlijn van onderkaak/nek en de zwarte lijn langs de verre arm;
  - rechts: de eerste lange modelrib (23,29)→(28,36) en de voorrand van de nabije onderarm;
  - onder: de bovenlijn van de verre achterpoot (24-25,42).
- Kleuren uit het teju-palet:
  - W vruchtvlees;
  - w schaduw aan de schaduwkant (rechterrand van de zone tegen rib/onderarm, en rij 42-43);
  - s pitjes. Er zijn 10 pitjes op 81 px (±1 per 7, zoals de bek van de teju). Ze staan los, nooit tegen elkaar: (19,31), (22,32), (20,33), (24,34), (23,36), (26,37), (29,38), (25,39), (28,40), (27,42).
- Buitenlijn en zwarte lijnen blijven zoals in r5.

## Zwakke punten (eerlijk)
- Lijf:
  - Het lijf is nu rustig, maar de borst/schouder (x 19-35, y 26-34) is een groot effen h-vlak. Het model heeft daar meer ribben; die bleken op 64 px alleen als korte stukjes te vertalen.
  - De verre achterpoot (x 20-28, y 43-49) is effen h en heeft geen ribben meer.
- Nabije arm:
  - De arm leest nu als ledemaat, met een lichte onderarm tussen twee contouren.
  - De H-streep langs de voorrand is een diagonale limoenlijn. Die kan te scherp zijn; H → h is mogelijk als de keurder dat vindt.
  - De klauwen zijn 1 px breed met een lichte punt. Op 1× lezen ze als een rand van 3 tandjes.
- Buikvariant: de witte buik leest op 1× als een bef/strook langs de borst. Het model heeft geen buikkleur, dus de vorm van de zone is een keuze van de maker (zie boven) en geen meting.
- Leggat onder de verre arm: in het model ligt het ±1 px verder naar rechts dan in de sprite (silhouet uit eerdere rondes; niet aangeraakt).
