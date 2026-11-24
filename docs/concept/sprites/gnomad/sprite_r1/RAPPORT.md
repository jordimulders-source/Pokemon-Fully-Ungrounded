# Gnomad – sprite r1 (maker-agent, 22 nov)

Model: `../r1/gemini_r1.png` (bevroren; r2 niet gebruikt). Lever: `gnomad_A.png` (riem warm bruin), `gnomad_B.png` (riem donkerblauw), `AB_8x.png`, `vel.png` (A | B | model op schaal 8×; 1× op licht/groen/donker; 1× en 2× naast Gnomini).

## Werkwijze (overnemen, niet hertekenen; scripts van Gnomini hergebruikt)
1. `pitch.py` + `natief.py` → Gemini-raster 10,24 px, fase 9,25 → `natief.png` (100×100, figuur 75×68).
2. `zones_n.py` → per natieve pixel familie (zwart/lijn, lavendel, roze, blauw, crème) en onderdeel (muts, neus, snor L/R, lijf, arm L/R, broek, voet L/R); lijnpixels horen bij het voorste buuronderdeel.
3. `reductie.py` → schaal 50/68 (figuur 55×50, x4–58, y10–59, voeten op rij 58–59). `kaal.png` = kale reductie (vlakgemiddelde + dichtstbijzijnde paletkleur). `red.png` = technische onderlaag: onderdeel per meerderheid, vlaktint = meerderheidstoon van de modelvlakpixels (heldere vlakken, geen blur), buitenlijn 1 px, binnenlijn aan de rand van het voorste onderdeel, modelvouwen waar de modellijn ≥ 40 % dekt.
4. `volume.py` → `vol.png`: alleen lijf en broek krijgen Gen 3-volume zoals bij Gnomini (middentint als basis, schaduwsikkel rechts, slagschaduw onder snor/neus/mutsrand, licht linksboven); selout aan de lichtkant van de buitenlijn (muts lila, roze, blauw, snor bruin), zwart aan de schaduwkant. Muts, neus, snor, handen en benen houden de modeltonen.
5. `maak.py` → benoemde reparaties + toegestane afwijkingen → A en B. `controle.py`, `kijk.py`, `zoom.py` (uitsnede sprite | model op schaal met raster), `vel.py`.

## Palet (16 incl. transparant)
zwart · muts 4 (= Gnomini) · roze 3 (= Gnomini donker/schaduw/midden) · blauw 3 (= Gnomini donker/schaduw/midden) · crème 2 (218,198,158 / 248,242,222) · riem 2.
- A: 14 = (174,130,90) leerbruin licht, 15 = (104,68,48) leerbruin donker. 14 is ook de selout van de snor (warm, past bij crème).
- B: riem = Gnomini's donkerblauw (56,109,142) + diep indigo (40,66,104); 14 blijft de snorselout.
- Weggelaten t.o.v. Gnomini (16-kleurengrens): roze hooglicht en blauw hooglicht. Neusglans = crème licht (3 px).

## Toegestane afwijkingen (Jordi)
- **Snor iets rafeliger:** linkeruiteinde: bovenste pluk aan de onderkant 1 px ingesneden en de inkeping tussen pluk 1 en 2 schoon (geen zwart/selout om en om); onderrand linkerlob 1 inkeping (15,37); onderrand onder de neus 1 inkeping (26,38); rechteruiteinde 1 inkeping tussen twee plukjes (42,31); binnenlijn rechtersnor (37,33) in snorselout i.p.v. zwart. Geen r2-detail. (Proef: pluk 1 px verder naar buiten las op 8× als een takje → teruggedraaid.)
- **Riem:** band van 3 px in het midden, 2 px aan de flanken, glimlachboog die de bol volgt (zakt 3–4 px naar het midden, rechts iets lager zoals de modelgrens), op de grens roze/blauw. Boven de riem roze, eronder blauw (tonen opnieuw met dezelfde belichting). Schaduw: links licht, rechter derde + onderrand in het midden donker. Geen gesp, geen lijnen.
- **Keuze B = donkerblauw:** Gnomini heeft op precies die plek een donkerblauwe streep; in B wordt die streep de riem, zodat de lijn doorloopt en er geen nieuwe kleurfamilie bijkomt. Nadeel: leest meer als broekband dan als riem; A leest duidelijker als riem.

## Afwijking t.o.v. de kale reductie (A; B verschilt alleen in de riemkleur)
| zone | px anders / px zone | waarvan lijn | waarvan riem | rest |
|---|---|---|---|---|
| muts | 143 / 612 | 101 | 0 | 42 (meerderheidstoon i.p.v. gemiddelde, 5× flaprand zwart) |
| neus | 35 / 74 | 19 | 0 | 16 (incl. 3 px glans) |
| snor L | 56 / 138 | 40 | 0 | 16 (incl. rafelreparaties) |
| snor R | 27 / 68 | 21 | 0 | 6 |
| lijf | 85 / 193 | 11 | 20 | 54 (volume, slagschaduw) |
| arm L | 34 / 63 | 24 | 0 | 10 |
| arm R | 28 / 58 | 22 | 0 | 6 |
| broek | 117 / 206 | 26 | 52 | 39 (volume) |
| voet L | 24 / 67 | 19 | 0 | 5 |
| voet R | 21 / 46 | 18 | 0 | 3 |
| silhouet | 1 px (ingesneden pluk) | | | |
Buiten lijn en riem: 197 / 1525 px (13 %).

Handreparaties (`maak.py`): verdwaalde mutspixel midden in het lijf (26,43) → lijf; verdwaalde mutspixel + gat in de linkersnor (10,35),(11,35); linkerrand snor (11,33),(11,36),(12,38) zodat selout en zwart niet afwisselen; binnenrand mutsflap (44,26),(45,28),(46,30),(47,32),(42,14) → zwart (wisselde per rij met selout); linkerrand broek (14,43),(14,45) → blauwe selout.

## Controle (`controle.py`)
A en B: 64×64 geïndexeerd, transparant index 0, 16 kleuren; zwart 18,0 % (Gen 3 ±12–19 %); geen lichte kleur op de buitenrand; geen losse zwarte pixels. Vlekjes < 3 px zijn modeldetails (vouwstreepjes muts, pluklijntjes snor, selout-hoekjes).

## Eigen zwakke punten (voor de keurder)
- Rechtersnor leest op 8× wat "sterachtig" door de binnenlijntjes uit het model; op 1× als pluizige pluk.
- Broek is op Gnomini's middenblauw gezet (model is donkerder blauw); kleur mag afwijken, maar keurder laten kijken.
- Handen hebben geen hooglicht (roze hooglicht viel af door de 16-kleurengrens).
