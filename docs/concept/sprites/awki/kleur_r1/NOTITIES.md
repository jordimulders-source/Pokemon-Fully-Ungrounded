# Awki – kleur ronde 1

**Bestanden:** `awki.png` (64×64, geïndexeerd, index 0 transparant), `normal.pal` (JASC, 16), `raster.txt` (handraster, 0–F per pixel), `vel.png` (sprite | model op 8×, close-ups kop+kuif en opgeheven vleugel op 12×, 1× en 2× op licht/donker + model 1×).
**Gereedschap** (`stappen/`, gekopieerd van hatun runa): `tl.py` (model-bbox x19 y19, schaal 6.232, top 2, left 4 = `silhouet/sil.py 56`), `onderlaag.py` (modelmediaan midden 40 % per spritepixel → palet, alleen positiegids: `onder2.txt`), `fijn.py` (model op halve spritepixels als paletletter: hiermee is elke lijn/grens/glans gemeten), `gem.py` (gemiddelde modelkleur per spritepixel naast het raster), `meet.py`, `zie.py`, `ed.py`/`zet.py` (handmatige rijsegmenten/pixels, melden silhouetafwijking), `controle.py` (clusters < 3 px + silhouet-diff), `rand.py` (lichte kleur op de buitenrand; toegestaan 1,2,3,5,6,8,D,F), `los1.py` (omlijningspixels 1 midden in een vlak), `toon.py`/`toon2.py` (toon per zone; toon2 = alleen vlakpixels zonder 0/1 tegen de mediaan van het modelblok), `vel.py`.
Handwerk per onderdeel: `e_vl.txt` (opgeheven vleugel), `e_kuif.txt`, `e_kop.txt`, `e_lijf.py` → `e_lijf.txt` (lijf, gevouwen vleugel, poten, staart), `e_rep1.txt` (reparaties, o.a. Jordi's tussenfeedback). Volgorde: `onder2.txt` → e_vl → e_kuif → e_kop → e_lijf → e_rep1 = `r1.txt` = `raster.txt`.

## Werkwijze per onderdeel
- **Opgeheven vleugel (links):** veerpunten geel A met selout 8 aan de lichtkant (boven/links) en een zwarte onderrand per veer op de gemeten modelplekken (F1|F2-naad (8,9)–(8,11); F2-onderrand (6,15)→(9,18); F3 (6,21)→(7,22); F4 (6,25)→(9,26); F5 (8,30); F6 (10–14,31/34); F7 (14–16,36); F8 (17–19,37–38)). Banden per veerrij zoals het model: geel → oranje 7 → rood 6 → bruine voorrand 4/3 met zwarte omlijning (13,10)→(21,18) → bruine schouder 2/3 tot x21.
- **Kuif:** basis perzik 9 (gemeten gemiddelde ±240,170,95, los van het gele voorhoofdsrandje A), midden oranje 7, uiteinde rood 6 met oranje lengtebanen op de modelplekken; lavendel punt E met donkerpaarse schaduwband F (39,5)→(43,9) zoals het model; Gemini's gloed is gewone pixels geworden.
- **Kop:** geel voorhoofdsrandje A (rij 16–19, x24–30, selout 8); snavelrug zwart (24–26,19); snavel grijs C (x22–27, rij 20–21) met punt (21,21); ondersnavel/kin bruin 2/3 (rij 22, gemeten bruin, niet zwart); gaplijn (28,21); rood vlakje (28–29,19) 6 + (28–29,20) 5 (model x27.5–29.5, y19.5–21); masker D x30–34 rij 17–21; witte keel B x26–33 met schaduw C onder het masker (rij 22) en langs de rechterrand; gouden oorvlek A/9/8 rij 19–22 x35–37; kruin bruin 4/3.
- **Lijf:** borst/nek bruin 3 met de bruine V (4) in de buik (x26–29, rij 29–33); buik goud 9 boven, 8 onder (rij 40+), sikkel volgt de buik; scheidingslijn 2/1 tussen buik en gevouwen vleugel op de modelplekken (x34 rij 30–36 → (43,48)).
- **Gevouwen vleugel (rechts):** dekveren 4 (rij 28–32 en een vlekje rij 36–37), vulling 3, rand 2 binnen de zwarte omlijning; slagpennen onderaan: donkere binnenpen 2 en twee lichte pennen 3 (x42–44 en x46–48) zoals het gemiddelde model.
- **Staart:** roest 6 met licht 7 onder de bovenrand, bovenrand 5, onderrand 2/1, twee veerlijnen 5 ((48,50)→(51,53) en (52,50)→(54,52)); staartbasis onder de vleugelpunt 5 (rij 49, model 5).
- **Poten:** 1 px omlijning, poot 3/4; linkervoet met lichte teenrug C (26,56) en tweede teen (rij 57–58); rechtervoet drie tenen (rij 57–60).

## Jordi's tussenfeedback (letterlijk: "lijnen in de vleugels, aansluiting buik op linkervleugel, poten, uiteinde kuif aan de onderkant, belijning en schaduw van kuif en oog")
1. **Lijnen in de vleugels:** opgeheven vleugel: de grens rood|bruine voorrand is nu een donkere lijn 5 (14,14)→(19,25)→(20,26) (model x14.5→19.5); de donkerrode veerlijnen staan op de gemeten modelpixels: S1 (14,17)→(16,20), S2 (14–15,21)/(15–16,22), S3 (14–16,24)+(14–17,25) met 2 in het midden (model "5222255"), S4 (14–18,28). Gevouwen vleugel: scheidingen in 2 (donkere tint van het vlak) i.p.v. zwart; de twee losse zwarte modelpixels ((40,40),(44,41)) ook 2 (geen losse zwarte pixels in donker vlak, hatun runa-les).
2. **Aansluiting buik op linkervleugel:** F6-onderrand zwart (12–14,34), F7 (14–18,35) en F8 (18–20,36–38) op hun modelplek; tussen de laatste veerpunt en de buik een bruine lijn 4 op x21 (model x21.5, "3/4") met 8 als buikrand op x22; rood/oranje (21–22,31–34) direct tegen het goud zoals het model.
3. **Poten:** tenen grijsbruin 4/3 met lichte teenrug C en schaduw 2, onderkant zwart (model "111111"), geen lichte kleur op de randen.
4. **Uiteinde kuif aan de onderkant:** onderrand van de rode punt is nu de schaduwkant: zwart 1 op (42–43,10), (41,11), (39–40,12), (36–38,13), (35,14); lavendel onderkant F (42–43,8), (43,9) zoals het model.
5. **Belijning en schaduw kuif:** lichtkant selout 6 (rood deel) / 8 (perzikbasis), schaduwkant zwart; binnenschaduw met 6 (37–38,12) i.p.v. extra 5; lanen gladgemaakt (geen losse 9/A-stipjes); toon kuif gemeten (toon2) 125 vs model 137, lavendel lichter gezet.
6. **Oog:** pupil 1 (30–31,18), glans B (30,19) (model: grijze glans x30.0 y19.0–19.5), iris 8 twee pixels hoog (31,19–20) (model: tan x31–32 y19–20.5), masker D eronder (30,20).

## Palet (16)
0 transparant · 1 omlijning (35,18,17) · bruin 2/3/4 · 5 donkerrood (115,38,34) · 6 rood (184,60,44) · 7 oranje (232,122,54) · 8 oker (178,136,64) · 9 goud/perzik (226,168,80) · A geel (248,226,110) · B wit · C grijs (140,138,140; snavel, keelschaduw, teenrug) · D masker (45,44,50) · E lavendel (190,176,244) · F donkerpaars (88,64,152).

## Controle
- Silhouet-diff **0** (1396 px), `rand.py` 0, `los1.py`: alleen lijnuiteinden (veernaden, pupil, gaplijn, buiklijn).
- Toon (alleen vlakpixels): opgeheven vleugel 135/135, kop 126/126, buik 127/127, gevouwen vleugel 77/77, poten 91/87, staart 79/84, kuif 125/137, lavendel 123/147.

## Afwijkingen van het model
- **Zak tussen vleugel en hals** (x23–24, rij 23–26, 8 px): in het model witte achtergrond (gemeten 250+, de keel is 232), maar het bevroren silhouet heeft het gat gevuld. Silhouet-diff 0 gehouden: wit B met zwarte rand. Op een gekleurde achtergrond leest dit als wit lijf naast de keel; alternatief = 8 px transparant (silhouet-diff 8). **Beslissing voor Claude/Jordi.**
- Lavendel punt: zwart/paarse omlijning F rondom (geen lichte kleur op de buitenrand); het model heeft daar gloed, dus de punt is donkerder (toon 123 vs 147).
- Kuifrand: zwart aan de schaduwkant, model heeft donkerrood met gloed.
- Keelschaduw C (140) iets donkerder dan het model (172); de chin-crème van het model (±200,182,160) is wit geworden (geen paletplek).
- Gevouwen vleugel: de twee losse zwarte modelpixels zijn 2 geworden.

## Open zwakke punten (voor ronde 2)
- Zak (zie boven) en de witte keel lezen daardoor samen breder dan in het model.
- Kuif en lavendel nog wat donkerder dan het model (gloed meegemeten).
- Staart iets donkerder/roder dan het roestoranje van het model.
- Oog: op 1× leesbaar door de glans, maar de tan iris van het model is iets groter.
