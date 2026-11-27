# Ledian-evolutie, frontsprite ronde 1 (27 nov)

Model: `../gemini/r6.png` (bevroren). Sprite = verkleining van het model zelf, niets hertekend.

## Stappen (scripts, vanuit de repo-root draaien)
1. `natief.py`: natief raster terug. Gemeten via randsterkte: pitch 10,24 (100×100-raster), fase x 9,3 / y 9,2; midden van elke cel (mediaan 5×5). Bijna-wit (≥e0) = wit. Figuur-bbox 66×66 (kolom 17–82, rij 15–80).
2. `bouw.py`: elke pixel naar de dichtstbijzijnde modelkleur (12 kleuren + transparant, gemeten met k-means op het natieve raster); achtergrond = wit dat (4-verbonden) met de rand samenhangt.
   - Ingesloten wit dat in het model achtergrond is, is transparant gemaakt: de spleet tussen de linkerarm en de onderkant van het hoofd (16 px) en de spleet tussen de benen (8 px). Het wit in de vuisten en de twee oogglansjes blijft wit.
   - 66→64 (Gengas-methode): rijen **54 en 57** geschrapt (rechte stukken van de benen, 11–12 px verschil met de buur) en kolommen **61 en 63** (recht stuk van de vleugel vóór de punt, 4 px verschil). Niet door sprieten, sterhoofd, ogen, mond, vuisten of voeten: de goedkoopste rijen (9/10, 3 px) liepen door de bovenpunt van het sterhoofd en zijn dus bewust niet gekozen. → `kaal.png`
3. `reparaties.py`: alleen de buitenrand (geen lichte kleur op de buitenlijn). → `ledian_evo_r1.png`
4. `vel.py`: `vel.png` (r1 8× | kaal 8× | model; 1× en 2× op licht en donker), `vergelijk.png` (r1 | Dundragoon | Skinguin | Princadee | Ledian G3 | Scizor G3).

## Palet (13 incl. transparant)
0 transparant · 1 zwart 101010 · 2 donkergrijs 2a2929 · 3 grijs 646464 · 4 a0a1a2 · 5 c3c4c5 · 6 wit f8f8f8 · 7 donkerrood 8d1922 (selout/lijn) · 8 b0272e · 9 e54444 · 10 f47371 · 11 geel fae375 · 12 goud d5ae36. Allemaal modelkleuren (zwart iets opgelicht).

## Afwijkingen t.o.v. de kale reductie (52 px, allemaal alleen kleur, geen vorm)
| Zone | px | Waarom |
|---|---|---|
| Hoofd | 15 | rode buitenrand (b0) linksboven en op de rechterpunt → selout 8d (de modelkleur van de vleugelrand) |
| Oog/mond | 0 | 1-op-1 model; mond blijft de subtiele modellijn |
| Voelsprieten | 0 | |
| Vuisten | 29 | lichtgrijze buitenrand (a0/c3) → grijs 64 |
| Armen | 5 | rand langs de transparante spleet: rood → 8d, lichtgrijs → 64 |
| Romp/schouder | 1 | losse grijze gewrichtspixel rechts van het hoofd op de rand: a0 → 64 |
| Vleugel | 0 | |
| Benen/voeten | 2 | rode buitenrand → 8d |

## Zwakke punten (eerlijk)
- Kleur is nog die van het model: donkerder en zwaarder dan Gen 3 (veel donkergrijze binnenlijnen, rood zonder duidelijk hooglicht linksboven); naast Scizor/Skinguin leest het donker. Geen kleurronde gedaan: dat is het volgende werk (schaduw/selout naar Gen 3, kleur mag afwijken).
- Losse 1-px tintjes van het model (bijv. donkerrode puntjes op kop en romp) zijn niet opgeruimd; volgens de "rustiger = pixelblur"-regel bewust laten staan tot een keuring ze benoemt.
- Kolom 63 ligt 2 px vóór de vleugelpunt; de punt zelf is heel, maar de vleugel is 2 px korter dan in het model.
- Transparante spleten (arm/hoofd, tussen de benen) zijn een interpretatie van het witte model; als Jordi ze als wit onderdeel bedoelde (manchet), terugzetten in `bouw.py`.
