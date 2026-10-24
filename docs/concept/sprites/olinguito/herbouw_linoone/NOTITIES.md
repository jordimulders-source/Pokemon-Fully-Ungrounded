# Olinguito herbouw op Galar-Linoone (fase 1, Dark)

Basis: `../referenties/galar_linoone_front.png`, als geheel als onderlaag gebruikt (kop vooraan laag, één oog, vier poten in Linoone's volgorde, 3/4-hoek naar links). Overheen getekend met het palet van ronde 23 (`normal.pal`, ongewijzigd gekopieerd).

## Bestanden
- `anim_front.png`: 64×128, 2 frames, P-modus, transparency=0. Frame 2: nabije voorpoot 1 px opgetild (stap); verder gelijk.
- `bron/bouw.py`: **met de hand getekende tekstblokken per onderdeel** (staart-, poot-, romp- en kopblokken plus een lijst fijnwerk-pixels), gestapeld van achter naar voor in Linoone-coördinaten → `bron/raster_f1.txt`/`raster_f2.txt`. `bron/export.py` schuift alles (+4, +3) naar het midden en maakt alle PNG's. `bron/check.py`: open randen, formaat en rechte silhouetlijnen. `schets.py`/`silhouet.py` zijn alleen de eerste opzet (staan niet in het resultaat).
- `onderlaag.png`: basis | overtekening (Linoone vaag, resultaat halfdoorzichtig in dezelfde coördinaten) | resultaat.
- `compare.png`: nieuw f1, f2, ronde 23 en Galar-Linoone op 1× en 3×.
- `zelfcheck/`: uitsnede per poot, van de kop en de staart op 8×, plus `naast_1x.png`/`naast_3x.png` (nieuw | Galar-Linoone | ronde 23 | Poochyena).

## Wat van de basis is en wat anders
- **Hetzelfde als Linoone:** kop links laag met de neus als meest linkse punt (x0, Linoone x1); het oog op Linoone's plek, net achter de snuit; nabije voorpoot onder de kin, schuin naar links-voor, laagste voet; verre voorpoot er vlak achter, 1 rij hoger; verre achterpoot als klein donker stompje onder de buik, hoger; nabije achterpoot achteraan. Diagonaal paar vooruit: nabije voor + verre achter (zoals Linoone), dus geen telgang.
- **Bewust anders:** (1) het achterlijf (achterpoten, romp, staart) staat 3 px meer naar links (verre achterpoot 1 px) voor een compactere fase-1-romp; volgorde en hoeken van de poten blijven. (2) De kop is een eigen ronde vorm met nekinham en omlijning tegen het lijf (Jordi: kop geen verlengstuk van het lijf). (3) Rug licht gewelfd (top bij de heup) i.p.v. Linoone's platte rug. (4) Staart: de hangende J i.p.v. Linoone's rechtopstaande pluim. (5) Geen tong.

## Onderdelen
- **Kop:** kleine ronde oren met crème binnenkant (verre oor kleiner, links), masker (2) als band over de neusbrug tot direct boven de neus, rond het oog, met een lob achter het oog; licht boogje (6/7/7/7/6, uiteinden buigen langs de rand omlaag) direct op de maskerrand boven het oog; amandeloog in de stijl van ronde 16 (donker bovenlid, E-bovenrij met glans C, D onder, pupil 1); crème snuit en kaak; scheve grijns (mondlijn met omhooggekrulde mondhoek rechts, geen tong); neus zwart met één glanspixel.
- **Klauwen:** 2 per voorpoot, Sandslash-stijl (wit B met grijze A-onderkant en 9-omlijning, schuin naar links-onder, punt omlaag gekruld). Nabij ±5 px lang; ver klein en donkerder, hangend onder de verre teen.
- **Staart:** begint boven op de heup als voortzetting van de ruglijn, hangt rechts naar beneden, krult onderaan terug omhoog naar links met een ronde lichte punt (7/8/6). Lucht tussen staart en romp, en 1 kolom tussen de punt en de nabije achterpoot.

## Zelfcheck (8×, `zelfcheck/`)
| Onderdeel | Vast aan het lijf | Rechte lijn ≥ 4 | Dikte vs. tegenhanger | Opmerking |
|---|---|---|---|---|
| Nabije voorpoot | ja, komt onder de kin uit de borst | nee (randen 3-2-1-trap) | 6–9 px | Elleboog-knik zwak; poot loopt vrij gelijkmatig taps |
| Verre voorpoot | ja, achter de nabije, top in de borst | nee | 6–8 px, donkerder | Grotendeels achter de nabije; leest als donkere tweede poot |
| Verre achterpoot | ja, onder de buik | nee | klein stompje (zoals Linoone) | Klein, maar Linoone heeft hetzelfde |
| Nabije achterpoot | ja, dij als bolling in de romp | nee | 6–10 px | Knie voor, hak naar achteren, voet weer naar voren |
| Kop | eigen vorm, overlapt het lijf | nee (onderkaak in een boog) | – | 3/4 zoals Linoone: één oog, snuit naar links-onder |
- **Diagonaal:** nabije voor (voet x8–16) en verre achter (x22–28) staan vóór; verre voor en nabije achter erachter. Klopt met Linoone.
- **Voethoogtes:** nabije voor y48, verre voor y47, verre achter y45, nabije achter y48 (Linoone-coördinaten).
- **check.py:** open randen 0 (beide frames); enige rechte silhouetlijn ≥ 4 is de ruglijn bovenop de heup (4 px, romp, A6 staat ≤ 4 toe). Voetzolen hebben een inkeping tussen de tenen.
- **Maten:** 1041 px (f2 1036) ✓; box 55×33 (D4 ≤ 48 gehaald? **nee**: lage, lange vorm zoals Linoone 61 en Zigzagoon 56); soliditeit 0,73 ✓; symmetrie 0,64 ✓; donkere pixels 0,47 (Dark/donkere vacht, ronde 23 0,52).
- **Kop te groot (D2):** kop met oren beslaat ±60% van de hoogte (fase 1: 40–55%). Komt doordat Linoone laag is; ronde 23 zat ook op ±58%. Niet opgelost.

## Eerlijk oordeel
- Op 1× en 3× leest het als een echte Pokémon: een lage, sluipende marterachtige met een duidelijke snuit en één oog, poten die logisch onder schouder en heup staan en geen Escher-constructie. De pose en de diagonale gang zijn die van Linoone en dat helpt duidelijk.
- Zwakker: (1) het masker steekt minder af dan in ronde 23, omdat de kop als geheel donker is; (2) het lijf is lang voor fase 1 (box 55 breed); het lijkt meer op een wezel/marter dan op een gedrongen beertje; (3) de kop is groot (±60%); (4) de nabije voorpoot is een lange, vrij gelijkmatige poot zonder echte elleboog-knik.
- Mogelijke volgende stap (één onderdeel per ronde): de romp nog 2–3 px inkorten, of de kop iets kleiner, als Jordi die richting goed vindt.

## Lessen
- Een volledige sprite als onderlaag nemen werkt veel sneller dan een skelet uit losse referenties: de pootvolgorde, voethoogtes en diagonale gang kloppen meteen.
- Teken in tekstblokken per onderdeel (achter → voor) en houd fijnwerk als losse lijst (x, y, kleur); dan kun je een onderdeel vervangen zonder de rest te raken.
- Klauwen van de verre poot nooit als laatste laag tekenen: ze komen dan over de nabije poot heen (Escher). Laag tekenen direct na de verre poot.
- Een rechte voetzool ≥ 4 px los je op met een teen-inkeping (1 transparant pixel, erboven omlijning).
