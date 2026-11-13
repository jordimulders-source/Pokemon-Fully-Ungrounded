# Poesrups: kleur r1

Eerste kleurronde op het bevroren silhouet (`../silhouet/silhouet.png`) en het model (`../referenties/model_gekozen.png`). Eindstand: `stappen/r1c.txt` → `raster.txt`.

## Werkwijze
- **Meetgereedschap eerst** (`stappen/`), gekopieerd van de poedellarve en omgezet naar x0 69, y0 240, 16,648 modelpx per spritepixel, links 5, boven 29: `px`, `rgb`, `box1x`, `lijnkaart`, `ov`, `tl`, `grid`, `meet`, `kwart`, `fijn`, `klas`. Nieuw: `bg.py` (witte achtergrond: vulling vanaf de rand over min(R,G,B) ≥ 244, zoals `sil.py`), `klas2.py` (mediaan-toonkaart + aandeel donkere lijn per blok) en `mal.py` (meetmal met randpixels). Alleen `rgb`, `fijn`, `klas`, `klas2`, `mal` en `box1x` zijn in deze ronde echt gedraaid; de rest is omgezet maar niet getest.
- **Met de hand** als tekstraster per rij: `r1.txt` (eerste versie), `r1b` (krulhaakjes), `r1c` (losse pixels opgeruimd). `bouw.py` → `raster.txt`, `palet.py` → png + pal, `controle.py`, `vel.py`.
- **Palet** = poedellarve (`../../poedellarve/af/normal.pal`), 8 kleuren + transparant gebruikt (1 2 3 4 5 6 7 A). Niets aangepast. Het model is geler/olijver in de schaduw ((200,192,168) en (168,152,128)) dan de roze-beige familietinten 6 (206,194,182) en 5 (182,162,152); helderheid klopt (187↔194, 150↔165), kleurzweem bewust die van de familie.

## Gemeten plekken (rgb.py, gemiddelde helderheid van het modelblok)
- Koepel/pony: vlak wit 236–243 → A, zonder vormschaduw (het model heeft die ook niet).
- Strook links op de rand (6, rij 46–49): 195–209 → 7.
- Naden: A x27–30 (rij 38–52; 212→188→150), B x34–36 (rij 40–54; 163–222), C x40–41 (rij 43–53; 220→125), D x45 (rij 47–52; 185–212). Boven in 7, midden 6, onder 5; taps.
- Wervelstreepjes op de pony: rij 39 x22–26 en rij 41 x23–25 (205–222) → 7.
- Schaduw onder krul 1: rij 34–36, x16–21 (156–208) → 6 met onderlijn in 3/4 op (19–21,36).
- Onderzone lijf rij 51–57: 176–190 → 6; staart onder rij 54–56: 150–175 → 5 met streep in 4 (rij 55, x51–54: 131–148).
- Gezicht rij 55–58, x8–21: ±150 → 5 (palet 165; 4 = 131 was te donker).
- Haarlijnen (alleen de sterkste, tegen het zebra-effect): x9 (rij 50–54), x14/15 (rij 50–55), x20→22 (rij 48–57), x26→27 (rij 52–57), verlengde naad A (30,52)→(33,57), naad B (35,55)→(37,57), naadbocht C (41,54)→(46,57). Weggelaten: de lijn (38,55)→(41,58) en de fijne diagonalen in de pony (rij 43–49).
- Pootjes: 2 (x22–24, rij 59–60; 202–223 → 7/A) en 3 (x29–30; 150/216) licht; 1, 4 en 5 in 5 (130–169).

## Ogen (afwijking van het model, opdracht Jordi)
- Modelogen gemeten: nabij zwart op (16–17, 55–56) met glans linksboven; ver oog (10, 55–56).
- **A (in de sprite):** nabije oog = oog van **Weedle** (`graphics/pokemon/weedle/anim_front_gba.png`, x16–17, y34–35: wit/zwart boven, zwart/zwart onder), pixel voor pixel op (16–17, 55–56). Verre oog = alleen de rechterkolom daarvan (2 zwarte pixels op (10,55),(10,56)); de linkerkolom zou op de buitenlijn vallen. Dat verre oog is dus niet 1-op-1 een heel oog van een echte sprite.
- **B** (`poesrups_oogB.png`): nabij = oog van **Sewaddle** (`sewaddle/anim_front.png`, x30–33, y32–35, 4×4 rond met glans; donkergrijs → index 3) op (15–18, 54–57); ver = Weedle 2×2 op (10–11, 55–56). Groter dan het modeloog.
- **C** (`poesrups_oogC.png`): als A, maar de glans lichtgrijs (7) i.p.v. wit, zoals bij **Snom** (`snom/front.png`, x20–21, y38–39).
- Geen oogwit, ooglid, wenkbrauw, neus of mond; tussen de ogen is het gezicht vlak 5.

## Alphawijzigingen (9 px erbij, 0 eraf; `alpha_wijzigingen.txt`)
- Krullen, omdat de toppen in het silhouet alleen uit randpixels bestonden (geen wit, geen haak): (22,30) rechterlijn krul 1 zodat (21,30) wit kan zijn; (18,30) haak krul 1; (26,31) haak krul 2; (29,32) rechterlijn krul 2 zodat (28,32) wit kan zijn; (33,34), (38,37), (42,41) top van krul 3, 4, 5 één pixel breder naar links (model: de punt krult naar voren).
- Pootje 5: (40,60), (41,60) als onderlijn, anders was het pootje alleen buitenlijn.

## Controle (`controle_uitvoer.txt`)
- onbenoemde alpha-diff 0 (9 benoemde); open randen 0; losse omlijningspixels 0; losse pixels 0; tintclusters < 3 px 0; 8 kleuren + transparant.
- Uitgezonderd van de clustertelling: `lijnwerk.txt` (naden, wervelstreepjes, haarlijnen, de witte punt van krul 4 op (39,38)), `pootjes.txt` (binnenwerk van de 5 pootjes, 2–6 px per pootje) en de oogglans (16,55).
- Belijning: buitenlijn 2 rechts en onder (model: zwart), selout 3 boven en linksboven (model: grijze lijn), 7 reeksen van 3–22 px, geen afwisseling.

## Zelf gerepareerd
- r1: krultoppen waren dichte blokjes buitenlijn → r1b haakjes en wit in de top (zie alpha).
- r1b: 40 losse pixels/60 kleine clusters → r1c opgeruimd tot schone vlakken.

## Resterende zwakke punten (eerlijk)
1. **Kam leest als stekels, niet als krullen.** Krul 1 en 2 hebben een haakje, 3–6 zijn op deze maat driehoekjes van 2–4 px met een donkere rechterlijn. Het BOX-verkleinde model is daar zachter (grijze lijn, ronder). Beter kan alleen met meer alphawerk aan de kam of een lichtere rechterlijn (3 i.p.v. 2); niet gedaan zonder opdracht.
2. **Grote vlakke witte koepel** (zoals het model): weinig Gen 3-vormschaduw; alleen naden en streepjes geven vorm.
3. **Pootjes 1, 4 en 5** zijn bultjes van 2 px; alleen pootje 2 en 3 lezen als rond.
4. **Ponypunten**: de puntige lokken boven het gezicht zijn teruggebracht tot drie lokken met wiggen in 6; het model heeft er meer en spitser. De schaduwzone begint in het model links iets hoger dan in de sprite.
5. **Kleurzweem** schaduw: familie-roze-beige i.p.v. het olijfbeige van het model (keuze; zie Palet).
6. **Verre oog** (1×2) staat direct tegen de buitenlijn en valt op 1× bijna weg; variant B heeft daar 2×2.
7. Niet gedaan: lijnkaart/overlay per onderdeel op 12×; vergeleken is op het 8×-vel en op 1× (box1x).
