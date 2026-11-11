# Charlatan-Alakazam: af_r1 (grafische afwerking)

Basis: `basis_S1.txt` (= `../lijf_r2/opt_S1.txt`, Jordi: "doe maar s1"). Opdracht, Jordi letterlijk: "ga daarna naar de grafische afwerking, dragonflycave vergelijking en vergelijking met andere gen 3 sprites, en zorg dat het qua kleurgebruik allemaal netjes klopt en check het nog even geometrisch". Eerder: "licht/contrast maar dat is standaard en fixen we zelf later".

Bouwen: `python3 af.py` (basis → `raster.txt`, met diff per zone), `python3 pal.py raster.txt alakazam_charlatan.png alakazam_charlatan_8x.png`, `python3 vel.py`. Controle: `python3 controle.py raster.txt`. Close-up voor/na: `python3 cmp.py basis_S1.txt raster.txt uit.png x0 y0 x1 y1 schaal`. Rastersnede met coördinaten: `python3 show.py raster.txt x0 y0 x1 y1`. Echte sprites: `gen3.py` (anim_front_gba + normal_gba.pal waar aanwezig).

Het ontwerp is niet veranderd: pose, kop, ogen, pupil, snor, handen, armzones, platen, rug/flank, borstplaat, keelwam en knieën staan op dezelfde plek in dezelfde kleurzone. Alleen tinten, selout en één randpixel.

## Wijzigingen per zone (pixeldiff tegen opt_S1, met `af.py` bewezen)
Totaal 202 px gewijzigd, 0 px buiten de zones.

| zone | px | waar | wat |
|---|---|---|---|
| palet n→d | 56 | x12–47, y19–47 | licht van het zwarte materiaal = dezelfde tint als de grijze selout (zie Kleur) |
| palet p→c | 4 | x16–18, y19–20 | glans op de linkerplaat = c |
| kop | 100 | x18–42, y3–24 | licht van linksboven i.p.v. rechtsboven (zie hieronder) |
| geometrie oor | 2 | (23,3), (23,4) | bovenrand linkeroor, 1 px silhouet (zie Geometrie) |
| verre bovenarm | 8 | x35–38, y29–32 | geen hooglicht a meer; c als slagschaduw onder de verre plaat, b alleen links |
| verre onderarm | 3 | x40–42, y34–35 | lichte tint bij de elleboog weg (verre arm donkerder) |
| verre been | 14 | x30–34, y49–56 | a → b op scheen en voet, schaduwkant c 1 kolom breder |
| nabij been | 10 | x15–18, y52–61 | buitenlijn links o → selout d (lichtkant) |
| netheid | 5 | x28–38, y27–34 | verre plaat één tint m (was 2+2 px); losse a (27,34) sluit aan op de a-sikkel; elleboog d-vlakje (37–38,34) → c |

### Kop in detail
- Hooglicht a als ovale vlek linksboven op de schedel: rij 9 x25–29, rij 10 x24–29, rij 11 x25–28, rij 12 x26–27 (loopt over in de lichtband van het linkeroor, zoals de Y-vlek bij Alakazam).
- De a-band rechtsboven (x33–39, rij 9–13) is b geworden; rechts een c-sikkel langs de rand: rij 10 x37, rij 11–12 x37–38, rij 13 x37–39, rij 14 x38–39, rij 15 x39–40, rij 16 x40; loopt uit in het ooglid van het verre oog.
- Linkerkant van de schedel c → b (lichtkant); de c-band onderlangs (rij 17–20, achterhoofd/kaak) blijft.
- Rechteroor: b aan de linkerkant, c rechts (was omgekeerd).
- Selout: links van oorpunt tot rij 15 d (was o): (18,3)…(23,15); rechts vanaf rij 6 o (was d): (35,6)…(40,14). Eén overgang per rand, nergens o en d om en om.
- Snuit: rechtsonder c i.p.v. b: (40,19), (40–41,20), (39–41,21), (41,22), (42,23), (42,24).
- Ongewijzigd: wenkbrauwrichel, beide ogen, pupil, de c-lijnen rond het oog (37,16–17) en (35–37,18), mondlijnen, snor, keelwam.

## Kleur
Palet: 11 kleuren + transparant (was 13).

| teken | RGB | helderheid | rol |
|---|---|---|---|
| o | 16,14,22 | 16 | omlijning |
| k | 42,40,56 | 42 | zwart: schaduw (was 34,32,46) |
| m | 66,64,86 | 67 | zwart: basis (was 54,52,70) |
| d | 96,88,124 | 94 | zwart: licht én grijs: selout/slagschaduw (was n 88,86,112 en d 106,96,136: bijna gelijk, samengevoegd) |
| c | 146,140,170 | 145 | grijs: schaduw (violet) én glans op zwart (p 130,128,156 was bijna gelijk aan c) |
| b | 184,184,196 | 185 | grijs: basis |
| a | 220,220,230 | 221 | grijs: hooglicht, wit: schaduw (was 224,224,232) |
| w | 252,252,252 | 252 | wit |
| t | 232,88,88 | 131 | rood: licht (was 248,112,104: stap 55 te groot) |
| r | 208,48,56 | 97 | rood: basis |
| s | 128,24,40 | 57 | rood: schaduw |

- **Stappen** (helderheid): grijs a→b 36, b→c 40, c→d 49; wit w→a 31; rood t→r 34, r→s 40; zwart o→k 26, k→m 25, m→d 27. Gemeten tegen Alakazam (bruin 58→101→133→179: 43/32/46; geel 99→169→221→240) en Taillow (51→92→109→142). Zwart heeft kleinere stappen, net als Umbreon (43→59→84, omlijning 16): bij zwart materiaal kan het niet anders zonder grijs te worden.
- **≤3 tinten per materiaal + omlijning:** zwart k/m/d (+ c als glans, 3 px), grijs a/b/c + d/o, wit w/a (+ b/c onderaan waar het grijze lijf begint), rood t/r/s. PASS.
- **Geen bijna gelijke tinten:** kleinste RGB-afstand nu 45 (k–m); n≈d en p≈c zijn samengevoegd. PASS.
- **Eén lichtrichting, linksboven:** kop omgezet (was rechtsboven zoals het model); platen, borstplaat, keelwam, armen, benen en kaarten waren al linksboven. PASS.
- **Selout:** d aan de lichtkant (kop links/boven, oren boven, nabije scheen links, kaarten links/boven, voeten boven), o aan de schaduwkant. Zwart materiaal houdt o rondom (een k-rand naast transparant zou als open rand tellen en is bij Umbreon ook zwart). PASS.
- **Verre ledematen donkerder:** verre bovenarm zonder a en met slagschaduw onder de plaat, verre onderarm minder licht, verre scheen/voet zonder a, verre dij en knie al donkerder. PASS.
- **Zwart leest op 1× los van de omlijning:** m 67 en d 94 tegen o 16 (was m 54); op het 1×-vel op licht duidelijk; op donker vervaagt het zwart, net als Umbreon. PASS.
- **Banding/pillow:** geen concentrische ringen; kop-hooglicht ligt linksboven met de sikkel rechts, niet in het midden. De dijen hebben verticale b/c-stroken (cilinder van links belicht), geen banding. PASS.
- **Vlakjes < 3 px:** 8 over, alle in dunne delen of glans uit de basis: snorkrul (47,19–20), kaartrand (10,37–38), vingerlijnen (13,38) en (15–16,41), teenlijn (40,57), klauwen (42,57)/(41,58) en (25,61–62), selout (24,59). Geen nieuwe.
- Donkeraandeel (L<40): 0,29 = alleen o (Alakazam 0,14, Kadabra 0,19). Hoog door de dunne strengen, kaarten en vingers met elk een eigen omlijning; E3 staat hoger toe bij Dark.

## Geometrie
Randen per rij gemeten (`show.py` en een randscript).
- **Linkeroor bovenrand** liep 3‑3‑1‑2‑2‑2 (x18–20 rij 2, x21–23 rij 3, x24 rij 4, …): de losse 1 gaf een knikje. **Gecorrigeerd met 1 px:** (23,3) eraf, (23,4) wordt rand d → 3‑2‑2‑2‑2‑2. Alpha-diff: eraf (23,3), verder 0.
- Kop rechts (rij 8–21): x‑stappen 1,1,1,2,2,5: gelijkmatig. PASS.
- Linkerplaat: 4‑2‑1 horizontaal, dan 2‑3 verticaal en terug: gladde boog. PASS.
- Romp rechts (rij 38–45): 32,32,32,33,34,36,37: oplopend, dijbolling. PASS.
- Nabije scheen links: 2‑3‑1‑4 (scheen, dan uitwaaieren naar de hiel): S-vorm, geen knik. PASS.
- Verre scheen links: 4‑2‑1‑1‑1: gelijkmatig. PASS.
- Rechteroor rechts: 2‑1‑1‑2 bij de punt, dan de kop: aanvaardbaar bij een punt.
- **Gemeld, niet gewijzigd (te groot voor 1–2 px):** onderrand verre onderarm rij 38 x42–49 is 8 px recht (na 4 px op rij 37). Leest als de vlakke onderkant van een onderarm; ronder maken kost meer dan 2 px silhouet.
- Lijndikte: overal 1 px, geen klonten. Perspectief: verre arm, plaat, been en voet hoger, kleiner en nu ook donkerder. Verhoudingen tegenover Alakazam: oppervlak 1454 (Alakazam 1388), box 56×63 (57×56), soliditeit 0,62 (0,64), kop ±44 % van de hoogte (Alakazam ±45 %).

## Controle (`controle.py raster.txt`)
- Kleuren: 11 + transparant. Open randen: 0. Losse o: 0.
- Alpha-diff tegen het silhouet: erbij 0, eraf 1: (23,3), de gemelde oorcorrectie.
- `alakazam_charlatan.png`: 64×64, geïndexeerd (P), index 0 transparant.

## Dragonfly Cave-checklist (SPRITING.md)
**§0**
1. 3/4-houding: lijf en blik diagonaal, verre kant korter en donkerder. PASS (kijkt naar rechts; Jordi: niet spiegelen).
2. Alles geteld en verbonden: 2 oren, 2 ogen, 2 armen, 2 handen, 2 platen, 2 benen, 2 voeten. PASS.
3. Geen rechte lijnen waar het rond is: PASS, behalve de gemelde onderrand van de verre onderarm.
4. Ogen geïntegreerd: lid, pupil, oogwit; verre oog half dicht, geen kopie. PASS (ongewijzigd).
5. Silhouet leest op 1× als Alakazam-familie (oren, snor, kaarten, platen). PASS.
6. Formaat: als Alakazam (zie Geometrie). PASS.
7. Pose niet stijf: gewicht op het nabije been, armen doen elk iets anders. PASS.

**§1–2** Met de hand als tekstraster, per zone. PASS. **§3** Curven: zie Geometrie; oorknik hersteld. PASS. **§4** 3 tinten + omlijning per kleur, schaduw iets naar violet (c/d), overbodige tinten samengevoegd. PASS. **§5** Licht linksboven, schaduwgrens volgt de vorm (kop-sikkel, platen, dijen), slagschaduw onder platen in schaduwtint, R/S-hooglicht op kop, oor, scheen en borstplaat. PASS. **§6** Glans alleen op de linkerplaat (3 px c) en de ogen. PASS. **§7** Geen vacht/schubben; platen als vlakke vlakken met eigen omlijning. PASS. **§8** Omlijning 1 px, zwart aan de schaduwkant en selout d aan de lichtkant, anti-aliasing alleen binnen. PASS.

## Fakemon-checklist (FAKEMON_CHECKLIST.md)
Bouwtype grote tweevoeter fase 3 (Psychic: Alakazam, Gardevoir, Gothitelle), Dark/Psychic, charlatan; pose en kenmerken liggen vast (SPEC).
- A1 PASS (Alakazam-familie). A2 PASS (oren + snorkrullen + kaarten breken de omtrek). A3 PASS met reden: kijkt naar rechts op Jordi's verzoek; diagonaal blijft (kop rechtsboven, kaart links laag als tegenwicht). A4 PASS (soliditeit 0,62, lucht tussen armen, romp en benen). A5 PASS (symmetrie 0,57). A6 PASS (de 8 px onderarmrand is gemeld).
- B1 PASS. B2 PASS (korte snuit, twee ogen). B3 PASS (verre oog smaller, half dicht). B4 PASS. B5 PASS (oren verschillen in vorm en hoogte). B6 PASS. B7 PASS.
- C1 PASS. C2 n.v.t. (tweevoeter). C3 PASS. C4 PASS (ellebogen en knieën geknikt). C5 PASS (platen als schouderbollingen). C6 PASS (verre ledematen nu ook donkerder). C7 PASS. C8 n.v.t. C9 PASS (gebaar met kaarten).
- D1 R: 1454 px, onder de 1700 van de tabel, maar boven Alakazam zelf (1388). D2 R: kop ±44 %, zoals Alakazam (±45 %); de tabel-20–30 % past niet bij de Abra-lijn. D3 n.v.t. D4 PASS. D5 n.v.t. (alleen de eindvorm).
- E1 PASS (nu ook verre arm en been). E2 PASS (binnenlijnen tussen nabij en ver). E3 R: 0,29, hoger dan Gen 3 door de veel omlijnde dunne delen; Dark-type.

## Vergelijking met echte Gen 3-sprites (vel.png)
- Naast Alakazam en Kadabra: zelfde formaat, zelfde lichtrichting nu, vergelijkbare stappen. Alakazam gebruikt meer hooglicht (grote Y-vlakken op kop en dijen); de charlatan heeft hooglicht op kop, oor, scheen en borstplaat, de grijze buik blijft b.
- Naast Umbreon/Gothitelle (zwart materiaal): zelfde aanpak, zwart met kleine stappen en een lichte bovenkant; los van de omlijning op licht.
- Naast Mr. Mime/Sneasel/Gardevoir: wit en rood als vlakken met sikkel rechtsonder, zoals daar.

## Zwakke punten
- Onderrand verre onderarm: 8 px recht (silhouet, niet gewijzigd).
- Grijze buik en dijen zijn grotendeels één tint b met c-sikkel; Alakazam zou daar meer hooglicht zetten. Bewust niet gedaan om geen nieuwe vlakken in het goedgekeurde lijf te zetten.
- Op een donkere achtergrond vervagen de zwarte platen en onderarmen (ook bij Umbreon).
- Het hooglicht op de kop is een duidelijke ovale vlek; een keurder kan het iets te nadrukkelijk vinden.
- Oude dunne-deel-vlakjes (vingerlijnen, klauwen, snorkrul) blijven < 3 px; dat zijn details uit eerdere, goedgekeurde rondes.
