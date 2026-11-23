# Pinsir-evolutie v2, frontsprite r3 (23 nov)

Reparaties uit `sprite_v2_r2/KEURING.md` (FAIL), plus het besluit van Claude over de rugstekels. Bouwen vanuit `docs/concept/sprites/pinsir_evo/`:
`python3 sprite_v2_r3/bouw.py A && python3 sprite_v2_r3/bouw.py B && python3 sprite_v2_r3/reparaties.py && python3 sprite_v2_r3/vellen.py`
(`reparaties.py zonder` levert de variant zonder pupil voor `ogen_8x.png`.)

- `pinsir_evo_v2_r3_A.png`: rug trouw (alle modelnaden). Jordi wilde eerst "zoveel mogelijk het schild na te maken".
- `pinsir_evo_v2_r3_B.png`: rug rustig (keurdersvoorkeur), platen in banden langs de rugrand.
- A en B verschillen alleen in de rug (175 px). Beide geïndexeerd, index 0 transparant, 15 kleuren.
- `*_basis.png` is de uitvoer van `bouw.py` vóór `reparaties.py`. Per reparatie het aantal pixels staat in `reparaties.txt`.
- Vellen:
  - `vel.png`: A | B | model op 6×; 1× en 2× naast r2, Tyranitar, Aggron en Pinsir op wit en donker.
  - `rug_8x.png`: A | B | model + Aggron/Turtonator/Tyranitar.
  - `onderdelen_12x.png`: r2 A | r3 A | model per onderdeel.
  - `ogen_8x.png`: met/zonder pupil | model.
  - `helderheid.md`: helderheid per vlak, sprite tegen model.

## Uitgevoerd (volgorde van de opdracht)
1. **Te licht.**
   - Vaste verschuivingen per onderdeel eruit.
   - Palet volgens de keurder: index 5 = (150,126,98), nieuw index 14 = (178,156,124) alleen als klein bruin hooglicht, index 6 alleen voor room (buiklijnen, klauwschaduw, buiksikkel), index 12 (kaak licht) = (172,98,82).
   - Drempels bruin 90/115/141 gekozen op de meting.
   - Buik: vlak 7, hooglicht 8 alleen rond (23–27,36–39), sikkel 6 onder (y ≥ 47) en langs de rechterrand (2 px).
   - Meting in `helderheid.md`: 10 van 13 vlakken binnen ±5. Daarbuiten: nabije arm −6, knie +6, buik +6 (r2 lag op +16, +20, +14).
2. **Kopschild.**
   - Vlak 5 met een lichte schuine bovenband 14: (12–16,14), (13–19,15), (16–22,16).
   - Onderrand y 19–20 = 4 over de hele breedte, ook links (9–13).
   - Rechteronderhoek 4, lichte streep rechtsonder op de rand (26–30,18) 14.
   - Geen verticale grens meer op x 20–21. Stekelflanken blijven.
   - 6 selout-pixels 1→2: (12,12) (12,13) (14,12) (15,13) (16,13) (19,9).
3. **Ogen.** Keurdersrecept 1-op-1: (19,22) (15,22) (20,22) (13,20) → zwart; geel links (13,21) (14,21) (13,22), rechts (22,20) (21,21) (22,21) (22,22); doorlopende zwarte balk (14..21,22) met de pupillen (14,22) en (21,22). Probeersel met en zonder pupil in `ogen_8x.png`. Gekozen: met pupil (het model heeft binnen in elk oog een donker vlekje).
4. **Verre been.**
   - Been vlak 4, knobbel (15–17,49–53) 5 met hooglicht (15,49) (16,49).
   - Modellijnen (19–23,54) en (18,51–53).
   - Sikkel 3 langs de rechterrand en de onderkant; de knip 5|3 is weg.
   - Voet: (16,59) (16,60) zwart als scheiding tussen twee klauwen, punten 7, onderkant 6.
5. **Nabije hand.** Drie klauwen naar de gemeten room- en zwartfracties van het model per spritepixel:
   - klauw 1: (33,42) (34,42) (33,43), punt (32,44);
   - klauw 2: (36,42) (35,43), (36,43) 6, punt (35,44) 6;
   - klauw 3: (34,45), punt (33,46) 6.
   Elke klauw heeft zwart eromheen. Geen afwisseling per pixel meer.
6. **Kleine punten.**
   - Knie: binnenkant 5, hooglicht (38–39,52) 14, onderste helft en de rand eronder 4. Daarmee is de dubbele lijn weg: (36,53) en (36,54) zijn 5.
   - Stroken y 47 (dij) en y 46–47 (staart) zijn geen lichte band meer.
   - Koepel 5 met hooglicht (32–34,30–31).
   - Onderarm 4 met een lichte linker- en bovenrand (2 rijen).
   - Verre hand in de schaduwtint: (10,43) en (10,44) 8→7, (11,43) en (10,45) 7→6.
   - Tintvlakjes kleiner dan 3 px (3/4/5) worden de buurtint. Index 14 is bewust klein en blijft.
7. **Rugstekels** (besluit Claude):
   - De rugrand van r1 (trapje met losse 1-px-bultjes) is vervangen door een gladde rand door de inkepingen van het model: e(x) door (37,21) (41,21) (45,23) (49,26) (53,29), en een steile rand op x 53 (y 29–37).
   - Daarop staan 6 driehoekige stekels, 3 px hoog (punt 1 px zwart, rij van 3, rij van 4 die naar rechts leunt). Lichte flank 2/14/5 links, donkere flank 3/1 rechts. Vijf staan omhoog op x 39, 42, 46, 50 en 54; één wijst naar rechts op (56,32). De plekken komen van de toppen die op het 1024-model gemeten zijn: (39.0,21.2) (41.8,20.6) (46.0,22.0) (50.2,24.8) (54.4,28.3) (55.8,31.8).
   - **Silhouetwijziging: +47 px, 0 px weg, alleen langs de rugrand** (lijst in `reparaties.txt`). De dichte gaatjes onder de schildrand (32–35,20–21) zijn gelijk aan r1.
8. **Rug B**:
   - 2 naden evenwijdig aan de rugrand, op de afstand tot de rugrand waar de modelnaden van A het vaakst liggen.
   - Platen in middentint 4 (een tint donkerder dan r2), hooglicht 5 alleen op de bovenrand, schaduw 3 op de rij boven de volgende naad.
   - Rug B meet 106 tegen model 102.
9. **Rug A**: zelfde tinten, stekels en reparaties. De modelnaden zijn gebleven (trouw, op verzoek van Jordi).

## Zelf gezien / zwakke punten
- **A:** de rug blijft een kriskras-net van naden. Op 2× is hij drukker dan B, Tyranitar en Aggron. Dat is de trouwe variant.
- **Stekels:** zichtbaar als gekartelde rij, maar kleiner dan de modelstekels. Groter zou het silhouet verder laten groeien.
- **Ogen:** het recept geeft kleine ogen (3–4 px geel). In het model lijken ze iets groter.
- **Hand:** leest als drie klauwjes, maar blijft op 1× klein.
- **Geen keurder:** geen nieuwe keurder gebruikt.
