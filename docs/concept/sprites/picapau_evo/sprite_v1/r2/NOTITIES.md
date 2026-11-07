# Picapau-evolutie: sprite r2 (reparaties op v1)

v1 (`../`) blijft staan. Hier alleen de punten 1–6 van de coördinator. Jordi bij Picapau (geldt hier ook): "het lichaam moet echt bol, dat is juist een kenmerk van pikachu".

## Bestanden
- `teken_r2.py`: zet `raster_v1.txt` (kopie van v1) om in `raster.txt`, met alle reparaties per punt.
- `palet.py`: de bliksembasis Y is vervallen en die plek is nu C (wangschaduw).
- `bouw.py` → `picapau_evo.png` (geïndexeerd, 16 kleuren, index 0 transparant) + `normal.pal`.
- `controle.py` → `controle_uitvoer.txt`; `diff.py` → `diff_uitvoer.txt`.
- `vel.py` → `vel.png` (r2, Picapau af, Raichu Gen 1, Taillow, v1; 1× en 8×).
- Draaien: `python3.11 teken_r2.py && python3.11 bouw.py && python3.11 diff.py && python3.11 controle.py && python3.11 vel.py`.

## Bevroren omtrek (`diff.py`)
- **Alpha-diff buiten de zones: 0 px.**
- Binnen de zones: KOP (punt 1: kop, oren, snavel) 47 px, STROOK (punt 4) 6 px, POTEN (punt 6) 8 px.
- Bliksem: zelfde masker als v1 (0 px alpha-diff). De linkerrand loopt al precies 1:1, de rechterrand 1-2-1-2; alleen opnieuw gekleurd.
- 688 px hebben een andere kleur.

## Per punt
1. **Kop leest meer als vogel.**
   - Snavel als bij Picapau: grijs-hoorn g/a/G, donkere punt, schaduw (G) aan de onderkant, donkere voet tegen de kop, 9 px lang. Niet meer bleek-vlak.
   - Kop is een eigen ellips (midden 19,5/26,2, stralen 9,2 × 8,4) en daardoor ronder aan de achterkant en bovenop.
   - Oren aan de voet smaller (4 px), breder in het midden, lopen door tot op de ronde schedel. De krul aan de punt is gebleven (zelfde haak met gaatje als v1).
   - Op 1× leest de grijze snavel met donkere punt duidelijk als vogel. De oren blijven Raichu-achtig, maar zijn smaller dan in v1.
2. **Volume.**
   - Kop en lijf krijgen hun tint uit de afstand tot een lichtpunt linksboven. Daardoor zijn de grenzen cirkelbogen: licht linksboven, schaduw als sikkel rechtsonder, zonder horizontale banden.
   - De buik is een ellips (vloeiende grens met het lijf) met dezelfde lichtval, bol.
   - Helderheid per tint: kastanje 173/128/87 (stappen 45 en 41), crème 243/214/165 (29 en 49). Taillow zit op ±30–40.
3. **Vleugel.**
   - De voorrand (linksboven) is licht (3), de basis v, en de schaduw (4) zit alleen aan de onder- en rechterrand.
   - Drie korte veerlijnen (4) vanuit de inkepingen van de omtrek suggereren ronde veren.
   - Stippen: 10 stuks, rond (2×2 en 3×3 zonder hoeken, één tint a zoals Picapau), onregelmatig verspreid, plus één b-stip op de verre vleugel.
4. **Strook achter de kop:** de verre vleugel is daar nu 3/v (geen 4-vlak meer) en de ronde kop dekt een deel ervan af. De blootgekomen bovenrand is selout 4. Geen zwarte manen meer.
5. **Wang:** twee tinten c/C, met de schaduw rechtsonder (5×4, rond). De paletplek kwam vrij door de bliksembasis Y te laten vervallen (bliksem = y licht + 1 oranje schaduw, zoals Pikachu's staart).
6. **Bliksem en pootjes.**
   - Bliksem: rand links consequent oranje en rechts/onder zwart; vulling y met een oranje sikkel rechtsonder.
   - Pootjes klein, met 2 tenen naar voren (links) en 2 naar achteren. De verre poot staat hoger en is alleen G (schaduwtint).

## Controle (`controle_uitvoer.txt`)
- Geen lichte kleur op de buitenrand, geen losse of alleen-diagonale pixels.
- Geen tintclusters kleiner dan 3 px (8-verbonden; oog en glans uitgezonderd).
- 15 kleuren + transparant, 1829 px.
- Gekleurde selout op de rand: g aan de bovenkant van de snavel en de pootjes, e aan de buik, 1 aan de bliksem (lichtkant).

## Eerlijke zwakke punten (nog niet klaar voor Jordi)
1. **Schaduw nog niet op Taillow-niveau.** De cirkelbogen zijn vloeiend, maar voelen mechanisch (pillow-achtig rond het lichtpunt). De kop heeft geen eigen binnenvormen (wangbol, schedel-overgang), en de buik is een glad ovaal zonder de bolle onderkant van Picapau.
2. **Kop:** leest door de snavel meer als vogel, maar het oranje gezicht met twee puntige oren blijft op 1× wat "vos". Smallere en lagere oren, of een lichtere kuiftint, zouden helpen; dat raakt Jordi's oorkeuze, dus eerst vragen.
3. **Vleugel:** veel effen v. De veerlijnen zijn kort en vallen op 1× bijna weg, en de stippen zijn klein naast de render.
4. **Snavel–kop-overgang en kopbovenkant:** rond de oorvoeten nog wat rommelige pixels.
5. **Pootjes:** de tenen zijn 1-px uitsteeksels en lezen op 1× nauwelijks als 2+2.
6. Deze ronde is grotendeels met regels in code gemaakt (lichtpunt, ellipsen). Voor echte Gen 3-kwaliteit moet een volgende ronde de schaduw van kop, buik en vleugel met de hand tekenen op dit silhouet.
