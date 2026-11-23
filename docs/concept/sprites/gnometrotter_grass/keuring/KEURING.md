# Keuring Gnometrotter Grass – r2 en hybride (23 nov, verse eindkeurder)

Gekeurd:
- **A** `sprite_r2/gnometrotter_grass.png` tegen `r4/gemini_r4_lijf.png`
- **B** `sprite_hybride/gnometrotter_grass_hybride.png` tegen `hybride/model_hybride.png`

Maatstaf: Rock `gnometrotter_rock/sprite_r4/` (PASS, zelfde pose) en Gnomad; niet strenger dan die.
Eigen beelden in deze map: `A_8x.png` / `B_8x.png` (sprite | model op 64 px | model op schaal, raster per 8), `A_8x_1x3.png` / `B_8x_1x3.png` (1× licht/donker naast het model, 3×), close-ups `A_z_kop.png`, `A_z_lijf.png`, `B_z_lijf.png`, `B_z_romp.png`, `B_z_benen.png`, `AB_z_arml.png` (sprite | model, rode lijn elke 5 px). Metingen: modelhelderheid per spritepixel via `sprite_r2/kijk.py` (gedeelde geometrie).

## Dragonfly Cave-omlijning (getoetst)
Gids, r. 80–170: het palet van de Scyther heeft de tinten "shadows/Outline highlights", "Outline base" en "Outline shadows"; "The "outline shadows" are always black (or ever-so-slightly off-black)"; "The outline base and outline highlight colors are also colors ... you must also recolor the outlines"; "The outlines must be reasonably dark". R. 340–470: "Don't stick to the original sprite's outlining under any circumstances" / "With the outlining all-black, it looks very 2D and cartoony - not how we want the end" (geen volledig zwarte lijnen). Samen met SPRITE_KERN: outline base in de donkerste eigen tint, zwart alleen aan de schaduwkant, binnenlijnen niet zwart, 1 px, outline highlight = de schaduwtint, nooit zwart en lijnkleur om en om op één rand.

Beide sprites volgen dezelfde aanpak als Rock r4 (muts/rugkam/baard: base linksboven, zwart rechts/onder; binnenlijnen in 5/6/9, nergens zwart als binnenlijn; benen base 9, zwart rechtsonder; neus als bal met zwarte boog linksonder). Drie plekken wijken af van Rock r4 en zijn dezelfde fouten die bij Rock in keuring r3 zijn gerepareerd: stok-linkerrand om en om (punt 1), hand R zonder outline shadow (punt 2), en een middentint op de buitenrand (punt 3/5).

---

## A. Grass r2 — **BIJNA**

**Op het oog (eerst):** op 1× leest de sprite als het model: bladmuts met gat onder de omgevallen punt, haar L als blad, neus als roze bal, bladbaard, haar R, rugplank met twijg en knopjes, roze plaatlijf met schouderovaal, stok met vuist, hand R, riem, blauwe broek met twee knoesten, lichte voetballen en houten zolen. Niets toegevoegd of weggelaten dat op 64 px zichtbaar is; oogstrook dicht volgens afspraak.

**Eis 1 (trouw):** in orde. Muts gemeten: model is links ±100–140 en rechts ±50–85, zonder lichter kruinvlak; sprite 13/12 volgt dat. Knoesten (19–20,45–46) en (47–48,43–45) staan op de modelknoesten.

**Eis 2 (Gen 3 / volume):** muts licht links/donker rechts (zoals het model, geen eigen hooglicht nodig), baard E/D met lijnen in 5, broek B met A-sikkel rechts, voetballen licht, zolen 4/3/2. Het lijf heeft 8 + 7-sikkel + plaatlijnen, maar geen enkel hooglicht op het grote vlak (alleen op het schouderovaal); Rock r4 heeft er wel een (punt 4).

### Reparaties (belangrijkste eerst; alles "neem over uit het model", niets hertekenen)
1. **Stok, linkerrand één tint (2).** Linkerrand van boven naar onder: (5,38)1 (5,39)1 (6,40)2 (3–5,41)2 (3,42)1 (4,43)1 (5,44)1 (6,45)1 (6,46)2 (6,47)2 (6,48)1 (7,49)1 (7,50–55)2 = zwart en 2 om en om in blokjes (dezelfde fout als Rock r3, punt 1). Het model toont aan de lichtkant een gewone donkere randlijn. Zet (5,38) (5,39) (3,42) (4,43) (5,44) (6,45) (6,48) (7,49) op 2, zoals Rock r4 (hele linkerrand 2); zwart alleen rechts (x 9–12) en onderaan (rij 56). Silhouet 0.
2. **Hand R, outline shadow rechtsonder (1).** Rechterrand (60,37) (60,38) (60,39), hoek (59,40) en onderrand (57,41) (58,41) zijn 6. Model: zwarte lijn rondom de hand; Rock r4 sluit dezelfde hand rechts vanaf y 37 en onderaan in 1. Zet die 6 px op 1; boven/links 6 laten, vulling 7 op (56–58,40) laten.
3. **Middentint op de buitenrand bij de vuist.** (5,30) is 7 op de buitenhoek linksboven van de vuist; model daar = rand (lichtgrijze overgang, 169/162/162). Rock r4 heeft hier 6. Zet (5,30) op 6.
4. **Hooglicht op het lijf.** Het lijf (±200 px 8) heeft geen 15. Lichtste modelplekken op het lijf: (36,26) 187, (36,27) 183, (35,27) 171 (helderheid; omgeving 140–165). Neem daar een 15-vlakje van 3 px over (nu 8), zoals Rock r4 op de buik.
5. **Outline highlights muts in de schaduwtint.** Op de linker buitenrand van de muts staan drie pixels in de lichte basistint 13: (21,6), (20,7), (17,12). De gids noemt de outline highlight = de schaduwtint ("shadows/Outline highlights"); Rock r4 gebruikt op dezelfde plekken zijn schaduwtint 3. Zet ze op 12.
6. (klein) **Gaatje in de dijlijn links.** (23,43) is B tussen 9-lijnpixels (22,43) en (24,43); model (23,43) = 103, donker zoals de lijn. Zet op 9.

Niet aanpassen: silhouet, oogstrook, muts en bladgrenzen, haar L/R, neus, baard, rugplank, twijg, schouderovaal, riem, knoesten, voetballen, zolen.
Na 1–6 (±22 px, alleen lijn/tint, silhouet 0) is A voor mij **PASS**; een diffcontrole (alleen deze pixels gewijzigd) volstaat.

---

## B. Grass hybride — **BIJNA**

**Op het oog (eerst):** op 1× leest de sprite als het hybride model: zelfde kop/muts/baard/rugplank als A, lijf met verticale planknerf (de dubbele naad op x 29/31 staat zo in het model), schoudercapsule rechtsboven als omlijnd langwerpig ovaal (x 40–49, y 22–28; model x 40–50, y 21–30), broek met ribbelstructuur en de horizontale ribbellijn over de rechterdij (39–44,47), die in het model staat. Niets toegevoegd of weggelaten dat op 64 px zichtbaar is. Elleboogcapsules: op 64 px vallen ze samen met de arm; geen afwijking die 64 px kan tonen.

**Eis 1 (trouw):** in orde. Lijfkleur lichter dan het model (gedeeld roze): toegestaan (kleur mag afwijken). Volume: lijf 8 links, 7-sikkel rechtsonder, planken in 6; het modellijf heeft zelf geen lichter vlak (±130 overal), dus geen hooglicht-eis.

**Eis 2 (Gen 3):** als A, plus één eigen punt: de ribbels in de broek staan voor een deel als losse 10-pixels (1–2 px) die op 8× als spikkels/dambord lezen (bv. rij 45: (34,45)B (35,45)A (36,45)B (37,45)A). SPRITE_KERN: geen tintvlakjes < 3 px behalve glans; herhaalde kleine patronen worden op 64 px een dambord.

### Reparaties (belangrijkste eerst; alles "neem over uit het model", niets hertekenen)
1. **Stok, linkerrand één tint (2).** Precies als A punt 1 (stok is identiek): (5,38) (5,39) (3,42) (4,43) (5,44) (6,45) (6,48) (7,49) van 1 naar 2.
2. **Hand R, outline shadow rechtsonder (1).** Als A punt 2: (60,37) (60,38) (60,39) (59,40) (57,41) (58,41) van 6 naar 1.
3. **Ribbels broek zonder losse spikkels.** Losse 10-clusters < 3 px: (45–46,40), (43–44,42), (46,42), (36–37,43), (47,43), (26,44), (21–22,45), (27–28,45), (35,45), (37–38,45), (19–20,47). Het model toont de ribbels als doorlopende donkere banden, niet als stippen. Laat alleen de ribbelstukken van ≥ 3 px staan (bv. (31–34,43–46), de A-sikkels rechts op beide dijen, de lijn (39–44,47)); verleng een losse ribbel alleen als de modelband daar doorloopt (meet op de donkerste modelpixels), anders terug naar 11.
4. **Vuist L, losse zwarte pixel en dambordje aan de onderkant.** (7,35) is 1 midden in de vuist; model daar licht roze (234,163,174) → zet op 8. Rij 36 x 7–10 wisselt 3,2,3,2; model meet daar (110,84,76) (75,62,49) (99,85,67) (78,62,52) = donker hout van de stoktop → één tint: (8,36) en (10,36) op 3, zoals rij 36 in A.
5. **Middentint op de buitenrand bij de vuist.** (5,30) is 7; zet op 6 (als A punt 3).
6. **Outline highlights muts in de schaduwtint.** Als A punt 5: (21,6), (20,7), (17,12) van 13 naar 12.

Niet aanpassen: silhouet, kop en muts, planknerf (x 29, 31, 35, 43), schoudercapsule, ribbellijn (39–44,47), riem, voetballen, zolen.
Na 1–6 (±40 px, alleen lijn/tint, silhouet 0) is B voor mij **PASS**; een diffcontrole volstaat.

## Ter info voor Jordi (geen eis)
- B: het modellijf is dieper rozerood en de schoudercapsule is in het model duidelijk lichter dan het lijf; in de sprite hebben lijf en capsule dezelfde 8. Op 1× leest de capsule nog als eigen vorm door de omlijning; een donkerder lijf (7 als basis) zou hem sterker maken, maar is een kleurkeuze.
- A en B delen kop, muts, stok en hand R pixel voor pixel; reparaties 1, 2, 5/6 kunnen in één script op beide.
