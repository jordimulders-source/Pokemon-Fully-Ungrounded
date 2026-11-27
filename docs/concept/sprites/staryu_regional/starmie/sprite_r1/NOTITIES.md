# Regionale Starmie (versierd koekje), frontsprite ronde 1 (kandidaat)

Bestanden: `starmie_r1.png` (64×64, mode P, index 0 transparant, 16 kleuren incl. transparant), `kaal.png` (kale samenstelling vóór reparaties), `vel.png` (r1 8× | kaal 8× | model op schaal 8× | Gen 3 Starmie 8× / close-ups 12×: bovenarm+juweel en linkerarm naast het model, achterpunten naast de Gen 3 Starmie / 1× op wit, crème, donker, zwart + model, Gen 3 Starmie, Staryu, skinguin, dundragoon, zapacha, princadee / 2× sprite, Starmie, Staryu), `bouw.py`, `chips.json`.
Gereedschap (`../gereedschap/`, gekopieerd van Dundragoon en aangepast): `pitch.py`, `natief.py` (→ `natief.png`), `voor.py` (masker voorste ster in het model), `gen3.py` (Gen 3 Starmie in punten verdelen), `gemeen.py` (schaal, klassen, palet), `kaal.py` (kale samenstelling), `chips.py` (plaatsing chips), `vel.py`, `controle.py`, `zones.py`.
Bouwen: `cd starmie && python3 sprite_r1/bouw.py` (schrijft ook `kaal.png`); controle: `python3 gereedschap/controle.py sprite_r1/starmie_r1.png`, `python3 gereedschap/zones.py sprite_r1/kaal.png sprite_r1/starmie_r1.png lijst`.

## Metingen
- **Model r3:** randsterkte per kolom/rij gaf één kam op **10,24 px** (1024/100), fase 9,25 (x en y); natief raster 99×99, figuur x12–86, y12–84. De voorste ster (glazuur + koekrand) is in het natieve raster gescheiden van de achterste koekpunten met een veelhoek waarvan alleen de randen langs de grens voorste ster/achterpunt tellen (gemeten op `natief.png`: bovenarm links x40→43, rechts x54→59, armen boven y34,5, inkepingen (71,5,55) en (26,5,55)); elders begrenst de modelfiguur. Witte glazuurlijnen tellen als figuur (gaten gevuld). Voorste ster natief 2657 cellen.
- **Gen 3 Starmie** (`anim_front_gba.png` frame 1): figuur x5–59, y7–57 (**55×51, 1673 px**). Punten op hoek vanaf de kern (31,5; 30): set A op 99/28/−37/−118/176° = de donkere **achterste** ster van de Gen 3 Starmie; set B op 61/−2/−81/−150/140° = de lichte **voorste** ster.
- **Belangrijk (twijfel 1):** het model draait de ster 36° ten opzichte van de Gen 3 Starmie. De voorste ster van het model heeft zijn punten in de richtingen van de Gen 3-**achterste** ster (set A: boven, rechts, rechtsonder, linksonder, links), en de achterste koekpunten van het model (en r4) zitten in de richtingen van de Gen 3-**voorste** ster (set B: linksboven, rechtsboven, rechts-laag, onder, links-laag). De echte achterste Gen 3-punten (set A) vallen dus vrijwel helemaal achter de modelster; letterlijk overnemen kan niet. Gekozen: de achterpunten zijn de Gen 3-punten van set B, pixel voor pixel (vorm, hoek en positie van de echte Starmie), op de plekken waar het model ook zijn achterpunten heeft. De Gen 3-set A verdwijnt achter de modelster (de stukjes die er in de Gen 3 rechtsboven en rechtsonder buiten zouden steken, zijn weggelaten). Claude: graag bevestigen dat dit de bedoeling is.
- **Schaal 0,66** (geprobeerd 0,62 / 0,66 / 0,68 / 0,70): juweelmidden model (50,49) → sprite (31,30), de Gen 3-kern. Voorste ster 1295 px (sprite x6–52, y6–52), zichtbare achterpunten 370 px. **Figuur x6–59, y6–57: 54×52, 1665 px** (Gen 3 Starmie 55×51 / 1673). Bij 0,70 wordt de bovenarm hoger dan de Gen 3 Starmie en blijven er minder achterpunten over (308 px).
- Alle vijf achterpunten zijn zichtbaar, ook de onderste (in het model r3 verborgen, in r4 en de Gen 3 Starmie wel zichtbaar).

## Kale samenstelling (`kaal.png`)
- **Voorste ster:** oppervlakgewogen reductie van het natieve raster binnen het masker. Klassen per modelcel: wit, hagelslag (rood/groen/blauw/geel), paarse lijn (paars, L<85), paars, zwart, koek. Regels: zwart ≥30 %, hagelslag ≥30 %, wit ≥35 %, paarse lijn ≥30 %, anders paars of koek met de tint naar de gemiddelde modelhelderheid (koek 100/118/150/185, paars 138/185).
- **Achterpunten:** Gen 3-pixels van set B die niet onder de voorste ster vallen; Gen 3-tint → koektint: lichtste paars → koek midden, 2e → oranje, 3e → schaduw, donkerste paars → koek donker, zwart → zwart. 17 Gen 3-goudpixels (de gouden kernpunt lag in de Gen 3 over de punt rechtsboven, x36–39, y15–20) krijgen de tint van de dichtstbijzijnde paarse pixel van dezelfde punt; silhouet blijft de Gen 3-figuur.

## Afwijkingen van de kale samenstelling: 358 px (silhouet-diff 0)
Per zone (`zones.py`): **voorste ster 206, juweel 46, achterste punten 106.** Per stap (`bouw.py`):
- **witte glazuurlijnen (86 px):** elke witte modelcel geprojecteerd op het spriteraster en uitgedund tot 1 px (Zhang-Suen + L-hoekjes weg); 5 lijnen, net als het model (5 zigzaggen), allemaal doorlopend. De kale reductie gaf 2 px dikke stukken; weggevallen wit krijgt de paarse ondergrondtint uit het model.
- **juweel (24 px):** omtrek en facetlijnen (paarse lijn + zwart in het model, natief u35–60, v38–61) op dezelfde manier geprojecteerd en uitgedund; de reductie maakte er een vage vlek van. Nu: achthoek met donkere rand, licht facet linksboven, onderste facetten donker, zoals het model.
- **ontkorrelen (127 px):** tintvlekjes < 3 px in glazuur en koekrand van de voorste ster nemen de buurtint van dezelfde groep (alleen voorste ster; de Gen 3-achterpunten niet).
- **buitenlijn (109 px):** rand naar transparant rechts/onder = zwart, links/boven = koek donker (gekleurde selout).
- **binnenlijn achter (33 px):** achterpixel die aan de voorste ster grenst = koek donker (zoals de donkerbruine lijn in het model).
- **losse zwarte pixels (11 px) → koek donker:** vooral Gen 3-zwartjes op de lichte bovenrand van de punten linksboven en onder, die tussen de nieuwe donkerbruine selout zwart/bruin om en om gaven.
- **koek in glazuur (3 px):** (26,18), (41,24), (18,45) koektint midden in het glazuur (mengpixel) → paars.
- **chocoladechips (22 px):** zie hieronder.

## Pixels die niet uit een bron komen
- **Chips (22 px, 11 chips van 2 px, koek donker):** het model heeft chips op de achterpunten linksboven/rechtsboven en Jordi koos chips op alle punten, maar de Gen 3-punten liggen anders dan de modelpunten, dus de modelplekken zijn niet over te nemen (de chips van het model komen boven de Gen 3-punt uit). Plaatsing per script (`chips.py`): op vulpixels zonder lijnbuur, zo ver mogelijk uit elkaar: rechtsboven 3, linksboven 3, rechts-laag 2, links-laag 2, onder 1 (onderpunt te smal voor 2). Vorm = 2 px (modelchip is 2×2 natief = 1,3 spritepixel). Plekken: (40–41,14) (41–42,9) (37–38,16) (52–53,33) (56–57,32) (34–35,53) (10–11,41) (12,38–39) (16–17,16) (21–22,17) (13–14,14).
- De 17 goudpixels → koek (zie boven).
- Geen andere pixels die niet uit het model of de Gen 3 Starmie komen; alle 370 achterpixels liggen binnen de Gen 3-figuur (0 erbuiten), 254 hebben exact de omgezette Gen 3-tint.

## Palet (index: kleur)
0 transparant (152,208,160) · 1 zwart (24,16,16) · koek 2 donker lijn/chip (116,58,24) 3 schaduw (178,102,40) 4 oranje (214,136,62) 5 midden (236,182,100) 6 licht (250,220,152) · paars 7 lijn (76,34,92) 8 donker (132,70,156) 9 midden (172,112,198) 10 licht (214,168,232) · 11 wit (252,252,252) · hagelslag 12 rood (228,44,44) 13 groen (72,196,64) 14 blauw (44,124,220) 15 geel (250,214,40).
**Palet is vol (16).** Koek heeft 4 vultinten + lijn omdat voorrand (licht goud) en achterpunten (oranje) in het model verschillen; daardoor delen chips de lijntint. Ruimte maken kan door koek licht en midden samen te nemen of geel hagel te schrappen (geen van beide gedaan).

## Controle (`controle.py`)
64×64, P, transparency 0, 16 kleuren incl. transparant; 1665 px; zwart 8,3 % van de figuur; geen lichte kleur op de buitenrand; geen losse zwarte pixels. Tintvlekjes < 3 px die over zijn (4-samenhang): koek S/O/M in de achterpunten zijn de schuine 1-px facetlijnen van de Gen 3 Starmie (niet aangeraakt); in de voorste ster: L (27,9) randglans in de punt van de bovenarm, d (29,14) (19,24) (38,42) en m (28,15) (14,25) paars tussen twee witte zigzagbochten of naast hagelslag (zo in het model), d (41,21) naast de lijn; M (11,30) (13,31) (14,32) is een schuine 1-px glanslijn op de koekrand linksonder.
Hagelslag: 17 stukjes in het model (4 rood, 5 groen, 5 blauw, 3 geel), alle op hun modelplek, 1–4 px (reductie, niet aangepast).

## Eerlijke twijfels
1. **Oriëntatie** (zie Metingen): de achterpunten zijn de Gen 3-voorste-sterpunten (set B), niet de Gen 3-achterste-sterpunten, omdat het model 36° gedraaid is. Vorm/hoek/positie zijn wel exact Gen 3.
2. **Achterpunten lezen als Gen 3-kristalpunten met facet, minder als koekdeeg:** de Gen 3-toonkaart geeft scherpe licht/donker-facetten; het model heeft zachte koekpunten met een lichte rand. Chips helpen; de facetten zijn bewust 1-op-1 Gen 3 (Jordi: "zoals de echte starmie").
3. **Chips zijn klein en donkerbruin** (zelfde tint als de lijnen): op 1× lezen ze als stipjes/streepjes; een eigen chocoladetint kan pas als er een paletplek vrijkomt.
4. **Witte zigzaglijnen 1 px:** trouw aan het model (modellijn ≈ 0,7–1 spritepixel) en scherp, maar de Z-vormen in de bovenarm zijn op 1× fijn; de dikkere variant staat in `kaal.png` (2 px op plekken, blokkeriger). Niet "rustiger" gemaakt.
5. **Glazuur heeft weinig volume** (vooral middenpaars, donker langs de onderrand en rond het juweel, wat lichtpaars linksonder): zo is het model; geen eigen schaduw toegevoegd.
6. Close-ups van het model in `vel.png` zijn uitsneden van het 1024-plaatje op dezelfde spritecoördinaten; op de randen kan het een halve pixel verschillen.
